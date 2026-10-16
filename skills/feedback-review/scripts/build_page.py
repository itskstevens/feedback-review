#!/usr/bin/env python3
"""Validate a review data file and build the review page from the template.

Usage:
  python3 build_page.py --data review-data.json --out review-page.html
  python3 build_page.py --data review-data.json --check      # validate only

Exits 1 and prints every problem if the data breaks a rule the page relies on.
Standard library only.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(HERE, "..", "assets", "review-page.html")

STORY_OPS = {"ac_add", "ac_change", "oq_add", "oq_resolve", "context"}
ALL_OPS = STORY_OPS | {"new_story"}
REQUIRED_SESSION = [
    "id", "dateLabel", "weekday", "meetingTitle", "meetingUrl", "program", "sessionName",
    "team", "project", "linearWorkspace", "futureMilestone", "newStoryMilestone",
    "slackChannelId", "slackChannelName", "approvers", "ownerName",
]
SLOP = [
    (re.compile("[—–]"), "em or en dash"),
    (re.compile(r"\b(seamlessly|significantly|effectively|robust|leverage)\b", re.I), "filler word"),
    (re.compile(r"\bHere's what\b", re.I), "\"Here's what\" opener"),
]


def texts(obj, skip=("desc",)):
    """Yield every string in the data except story descriptions copied from the tracker."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in skip:
                continue
            yield from texts(v, skip)
    elif isinstance(obj, list):
        for v in obj:
            yield from texts(v, skip)
    elif isinstance(obj, str):
        yield obj


def validate(data):
    errs, warns = [], []
    for key in ("session", "feedback", "stories", "edits"):
        if key not in data:
            errs.append(f"missing top-level key: {key}")
    if errs:
        return errs, warns

    ses = data["session"]
    for k in REQUIRED_SESSION:
        if not ses.get(k):
            errs.append(f"session.{k} is required")
    for k in ("futureMilestone", "newStoryMilestone"):
        ms = ses.get(k) or {}
        if not (isinstance(ms, dict) and ms.get("id") and ms.get("name")):
            errs.append(f"session.{k} needs an id and a name")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(ses.get("id", ""))):
        errs.append("session.id must be the meeting date as YYYY-MM-DD")
    for a in ses.get("approvers") or []:
        if not (a.get("name") and re.fullmatch(r"U[A-Z0-9]+", str(a.get("slackId", "")))):
            errs.append(f"approver needs a name and a Slack user ID: {a}")

    fb_ids = [f.get("n") for f in data["feedback"]]
    if len(set(fb_ids)) != len(fb_ids):
        errs.append("feedback ids (n) must be unique")
    for f in data["feedback"]:
        for k in ("n", "label", "summary", "t", "who"):
            if not f.get(k):
                errs.append(f"feedback {f.get('n')} needs {k}")
    dec_ids = {d.get("id") for d in data.get("decisions", [])}

    for us, s in data["stories"].items():
        for k in ("ticket", "title", "st", "desc"):
            if not s.get(k):
                errs.append(f"story {us} needs {k}")
        if s.get("st") not in ("fly", "up", "cut"):
            errs.append(f"story {us}: st must be fly, up or cut")

    seen = set()
    for e in data["edits"]:
        eid = e.get("id")
        if eid in seen:
            errs.append(f"duplicate edit id {eid}")
        seen.add(eid)
        op = e.get("op")
        if op not in ALL_OPS:
            errs.append(f"{eid}: op must be one of {sorted(ALL_OPS)}")
            continue
        if not e.get("fb"):
            errs.append(f"{eid}: every edit names at least one feedback item in fb")
        for n in e.get("fb", []):
            if n not in fb_ids:
                errs.append(f"{eid}: unknown feedback id {n}")
        for d in e.get("dec", []):
            if d not in dec_ids:
                errs.append(f"{eid}: unknown decision id {d}")
        if op == "new_story":
            if not e.get("title") or not e.get("txt"):
                errs.append(f"{eid}: new_story needs title and txt")
            continue
        s = data["stories"].get(e.get("us"))
        if not s or not s.get("desc"):
            errs.append(f"{eid}: story {e.get('us')} missing from stories, or has no desc")
            continue
        if not e.get("txt"):
            errs.append(f"{eid}: txt is required")
        if op in ("ac_change", "oq_resolve"):
            if not e.get("old"):
                errs.append(f"{eid}: {op} needs old")
            elif s["desc"].count(e["old"]) != 1:
                errs.append(f"{eid}: old must appear exactly once in {e['us']}'s description")
        if e.get("txt") and e["txt"] in s["desc"]:
            errs.append(f"{eid}: txt already appears in {e['us']}'s description")

    for f in data["feedback"]:
        if not any(f["n"] in e.get("fb", []) for e in data["edits"]):
            warns.append(f"feedback {f['n']} has no story updates; it can still be classified")

    for t in texts(data):
        for rx, label in SLOP:
            if rx.search(t):
                warns.append(f"writing rule ({label}): {t[:70]}")
    return errs, warns


def build(data, template_path):
    html = open(template_path, encoding="utf-8").read()
    if "__AUDIT_DATA__" not in html or "__TITLE__" not in html:
        raise SystemExit("template is missing __AUDIT_DATA__ or __TITLE__")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    json.loads(payload)
    ses = data["session"]
    title = f"{ses.get('shortName') or ses['program']} {ses['sessionName']}, {ses['dateLabel'].rsplit(' ', 1)[0]}"
    return html.replace("__AUDIT_DATA__", payload, 1).replace("__TITLE__", title, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE)
    ap.add_argument("--check", action="store_true", help="validate only")
    args = ap.parse_args()

    data = json.load(open(args.data, encoding="utf-8"))
    errs, warns = validate(data)
    for w in warns:
        print("warning:", w)
    if errs:
        for e in errs:
            print("error:", e)
        sys.exit(1)
    print(f"ok: {len(data['feedback'])} feedback, {len(data['edits'])} story updates, {len(data['stories'])} stories")
    if args.check:
        return
    if not args.out:
        raise SystemExit("--out is required unless --check")
    open(args.out, "w", encoding="utf-8").write(build(data, args.template))
    print("wrote", args.out)


if __name__ == "__main__":
    main()
