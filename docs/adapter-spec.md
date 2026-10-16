# Project tool adapter spec

The review page talks to the project tool through a connector (MCP server) in the user's Claude account. To support a new tool, it needs these six operations. The MVP maps them to Linear (see [linear.md](linear.md)).

| # | Operation | Used for | Linear tool |
|---|---|---|---|
| 1 | List stories in a project | Weekly run: find user stories by title prefix | `list_issues` |
| 2 | Read a story's description and status | Weekly run and apply: read the current text fresh | `get_issue` |
| 3 | Patch a description in place (replace text, insert before an anchor, append) | Apply: add criteria, questions, context | `save_issue` with `patch` |
| 4 | Comment on a story | Apply: one comment per story listing the changes | `save_comment` |
| 5 | Create an issue in a milestone (or equivalent bucket), linked to other issues | Future enhancements and new stories | `save_issue` without `id`, with `milestone` and `relatedTo` |
| 6 | Cancel an issue | Restore a future enhancement before sending | `save_issue` with `state: "Canceled"` |

Plus one setup-time operation: list and create milestones (`list_milestones`, `save_milestone`).

## Rules an adapter must keep

- Descriptions are treated as markdown with `## Heading` sections. Tools that store rich text need a conversion step on read and write, and must round-trip text the page didn't touch unchanged.
- Patch anchors must match exactly once, or the whole patch fails. The page reads the description fresh right before patching and skips any update whose anchor no longer matches.
- Created issues carry a `Ref: fbr/<date>/<feedback id>` line so later runs can find them by text search.

## Adding an adapter

1. Add `docs/<tool>.md` with the mapping table above.
2. Make the page's Linear calls (`call(...)` in `review-page.html`) go through a small adapter object keyed by `tracker.type`.
3. Extend `feedback-review-setup` with the tool's discovery questions.
4. Add a mocked browser test like `tests/page.test.mjs`.
