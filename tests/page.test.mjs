// End-to-end test of the review page with Linear and Slack mocked.
// Run: npm test   (builds examples/sample-page.html first)
import { chromium } from "playwright";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import assert from "node:assert/strict";

const page_html = readFileSync(new URL("../examples/sample-page.html", import.meta.url), "utf8");
// The Artifact tool wraps the page in a document at publish time; do the same here.
const dir = mkdtempSync(join(tmpdir(), "fbr-"));
const file = join(dir, "page.html");
writeFileSync(file, `<!doctype html><html><head><meta charset="utf-8"></head><body>${page_html}</body></html>`);

const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const page = await browser.newPage({ viewport: { width: 1100, height: 1600 } });
const errors = [], calls = [];
page.on("pageerror", e => errors.push(e.message));
await page.exposeFunction("logCall", s => calls.push(JSON.parse(s)));
await page.addInitScript(() => {
  let n = 500;
  const mcp = { callTool: async (server, tool, input) => {
    window.logCall(JSON.stringify({ server, tool, input }));
    if (tool === "save_issue" && !input.id) { n++; return { payload: { id: "NW-" + n, url: "https://linear.app/x/NW-" + n } }; }
    if (tool === "get_issue") {
      const D = JSON.parse(document.getElementById("audit-data").textContent);
      return { payload: { description: Object.values(D.stories).find(s => s.ticket === input.id).desc } };
    }
    if (tool === "slack_send_message") return { payload: { message_link: "https://x.slack.com/archives/C00000EXAMPLE/p1700000000000100", message_context: { message_ts: "1700000000.000100" } } };
    return { payload: { ok: true } };
  } };
  window.claude = { use: async k => (k === "mcp" ? mcp : null) };
});
await page.goto("file://" + file);
await page.waitForTimeout(300);

// Nothing classified: sending is blocked.
await page.click("#reviewbtn");
assert.equal(await page.$eval("#applybtn", b => b.disabled), true, "send must be blocked until everything is classified");
await page.click("#cancelbtn");

// Classify: F1 new, F2 discussion, F3 future, F4 is pre-marked covered by the data.
assert.equal(await page.isChecked('[data-fb="F4"][data-cls="cov"]'), true, "covered field pre-ticks the box");
await page.check('[data-fb="F1"][data-cls="new"]');
await page.check('[data-fb="F2"][data-cls="disc"]');
await page.check('[data-fb="F3"][data-cls="fut"]');

await page.click("#reviewbtn");
await page.waitForTimeout(100);
assert.equal(await page.$eval("#applybtn", b => b.disabled), false);
await page.click("#applybtn");
await page.waitForTimeout(800);

const thread = await page.$eval("#slackthread", t => t.value);
const ask = await page.$eval("#slackapproval", t => t.value);
assert.match(thread, /\*\*New requirements\*\*/);
assert.match(thread, /\*\*Future enhancements\*\*/);
assert.match(thread, /\*\*Still needs discussion\*\*/);
assert.match(thread, /\*\*Already covered by what we're building\*\*/);
assert.match(ask, /Filter by several statuses/);
assert.doesNotMatch(ask, /Risk heat map|Team view|Upload from the step/, "approval request lists only new requirements");

const futureTickets = calls.filter(c => c.tool === "save_issue" && !c.input.id && c.input.milestone === "00000000-0000-0000-0000-00000000f001");
assert.equal(futureTickets.length, 1, "one future-enhancement ticket per piece of feedback");
assert.equal(calls.filter(c => c.server === "Slack").length, 3, "post plus two thread replies");

// Apply after approval.
await page.click("#cancelbtn");
await page.click("#reviewbtn");
await page.check("#approvedchk");
await page.waitForTimeout(100);
await page.click("#applybtn");
await page.waitForTimeout(800);
const patched = calls.filter(c => c.tool === "save_issue" && c.input.id === "NW-101");
assert.equal(patched.length, 1, "NW-101 patched once");
assert.ok(!calls.some(c => c.tool === "save_issue" && ["NW-102", "NW-103"].includes(c.input.id)), "discussion and covered items leave Linear alone");
assert.match(await page.$eval("#tally", t => t.textContent), /applied/);
assert.deepEqual(errors, []);

await browser.close();
console.log(`ok: ${calls.length} mocked calls, no page errors`);
