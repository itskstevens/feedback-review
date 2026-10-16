# Linear notes

## What the workflow expects

- One Linear **project** holds the user stories, and their titles share a prefix (default `US-`, for example `US-11 · See my work`).
- Story descriptions use markdown sections. The page looks for an acceptance-criteria section and an open-questions section (headings set in settings). It adds a `## <Session> context (<date>)` section for background notes.
- Two **milestones** in that project: one for future enhancements (setup creates "Future Enhancements" if missing) and one for brand-new stories.

## What it writes, and when

| When | Call | What |
|---|---|---|
| Send for approval | `save_issue` (create) | One `[Future] <label>` ticket per future enhancement, in the future milestone, `relatedTo` the stories it would change |
| Restore (before sending) | `save_issue` `state: "Canceled"`, `save_comment` | Cancels a future-enhancement ticket |
| Apply | `get_issue`, then `save_issue` with `patch` | Amends each story; skips any update whose anchor text changed |
| Apply | `save_comment` | One comment per story listing what changed and who approved |
| Apply | `save_issue` (create) | New stories, in the new-story milestone |

The weekly run itself never writes to Linear.

## Capabilities the page declares

```
{"mcp":{"servers":[{"server":"Linear","tools":["get_issue","save_issue","save_comment","list_issues"]},
                   {"server":"Slack","tools":["slack_send_message","slack_read_thread","slack_read_channel"]}]},
 "db":{}}
```

The first time the page calls Linear or Slack, Claude asks the viewer to allow it.

## Links

Ticket links use `https://linear.app/<workspace_slug>/issue/<ID>`. Get the slug from any issue URL.
