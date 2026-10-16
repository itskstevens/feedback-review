# Review data format

`build_page.py` injects this JSON into `assets/review-page.html`. The full worked example is `examples/sample-data.json` at the repo root.

```jsonc
{
  "session": {
    "id": "YYYY-MM-DD",                 // meeting date; also scopes ticket references
    "dateLabel": "15 Jan 2026", "weekday": "Thursday",
    "meetingTitle": "…", "meetingUrl": "https://notes.granola.ai/d/<id>",
    "demoTopic": "the My Work page",     // what was shown, lower case
    // from settings:
    "program": "{program.name}", "shortName": "{program.short_name}", "sessionName": "{program.session_name}",
    "ownerName": "{owner.name}",
    "team": "{tracker.team}", "project": "{tracker.project}", "milestone": "{tracker.current_milestone}",
    "linearWorkspace": "{tracker.workspace_slug}",
    "futureMilestone": {"id": "…", "name": "…"}, "newStoryMilestone": {"id": "…", "name": "…"},
    "backlogState": "{tracker.backlog_state}",
    "headings": {"acceptance": "{stories.acceptance_heading}", "questions": "{stories.questions_heading}"},
    "slackChannelId": "{chat.channel_id}", "slackChannelName": "{chat.channel_name}",
    "approvers": [{"name": "…", "slackId": "U…"}]
  },
  "statusNote": "One short paragraph of context for the owner, or \"\".",
  "decisions": [{"id": "D1", "title": "Question form", "body": "The conflict: who said what, when.", "rec": "Proposed: …"}],
  "feedback": [{
    "n": "F1", "label": "2 to 5 words", "summary": "What changes for users. Goes into Slack.",
    "t": "What was said, paraphrased.", "who": "Name (team)", "by": "First name",
    "covered": "optional: what already covers it"
  }],
  "stories": {
    "US-03": {"ticket": "NW-101", "title": "Short title", "st": "fly|up|cut", "lin": "Linear status",
              "build": "What exists today, one sentence.", "desc": "Full description, copied unchanged"}
  },
  "edits": [
    {"id": "e01", "us": "US-03", "op": "ac_add|ac_change|oq_add|oq_resolve|context", "fb": ["F1"], "dec": ["D1"],
     "old": "exact text (ac_change, oq_resolve only)", "txt": "new text"},
    {"id": "e02", "op": "new_story", "fb": ["F3"], "title": "Story title", "txt": "Full story description"}
  ],
  "gaps": ["What this review didn't cover."],
  "sources": [{"label": "Focus group, 15 Jan 2026", "url": "https://notes.granola.ai/d/<id>"}]
}
```

`st`: `fly` built or being built, `up` not started, `cut` descoped.

## What the page does with each classification

| Box | Linear | Slack |
|---|---|---|
| New requirement | After dev approval: patches each story under the card, one comment per story; creates any `new_story` in the new-story milestone | Listed under "New requirements (need approval)" and in the approval request |
| Future enhancement | At send: one `[Future] <label>` ticket in the future milestone, linked to the stories, with `Ref: fbr/<date>/<F#>` | "Future enhancements (logged…, no action needed)" with the ticket link |
| Still needs discussion | Nothing | "Still needs discussion (no action yet)" |
| Already covered in app | Nothing | "Already covered by what we're building (no change)" with the owner's note |

An update shared by two feedback items goes in if either is a new requirement. The page won't send until every feedback item is classified. Progress lives in the artifact's own store, so the owner can send one day and apply another.
