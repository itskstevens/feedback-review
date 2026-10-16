---
name: feedback-review-setup
description: Set up the weekly feedback-review workflow for a new user. Checks that Granola, Linear and Slack are connected, asks a handful of questions, creates the Linear milestones it needs, saves the settings file, creates the weekly scheduled task, and does a dry run that only DMs the user. Use when someone says "set up the feedback review", "install feedback-review", points you at the itskstevens/feedback-review repo, or the feedback-review skill can't find its settings.
---

# Feedback review: setup

Goal: the user goes from nothing to a working weekly review in one conversation. Ask questions with the `AskUserQuestion` tool, batching up to four at a time, and offer choices you've already looked up rather than asking them to type IDs.

## 1. Check what's connected

The workflow needs four things. Check each with one cheap read call:

| Need | Check | If missing |
|---|---|---|
| Granola | `list_meeting_folders` | Suggest the Granola connector. Folder filtering needs a paid Granola plan; without it, matching falls back to titles. |
| Linear | `list_teams` | Suggest the Linear connector. (Other trackers: see ROADMAP.md.) |
| Slack | `slack_search_channels` with any word | Suggest the Slack connector. |
| Artifacts with live data | The `Artifact` tool exists and the `artifact-capabilities` skill lists `mcp` and `db` | Stop and explain: the review page needs artifacts that can call connectors and keep saved state. An org admin may need to allow it. |

Also check for scheduled tasks (`create_trigger`). Without them the workflow still runs on demand ("build this week's feedback review").

Don't continue until Granola, Linear, Slack and artifacts all work.

## 2. Ask, using what you found

Round 1 (look things up first and offer them as options):
1. **Which Granola folder holds the sessions?** Offer folders from `list_meeting_folders`. Allow "none".
2. **What do you call the meeting?** For example "focus group", "demo review", "UAT check-in". This drives title matching and the wording on the page and in Slack.
3. **Which Linear team and project hold the user stories?** Offer from `list_teams` and `list_projects`.
4. **How do story titles start?** Look at the project's issues with `list_issues` and propose the common prefix (for example `US-`).

Round 2:
1. **Which Slack channel gets the approval thread?** Offer from `slack_search_channels`.
2. **Who approves?** Search people with `slack_search_users` and confirm their user IDs.
3. **Which milestone gets brand-new stories?** Offer from `list_milestones`.
4. **When does the session end each week?** Day, time, timezone. Schedule the run about an hour after.

Get the user's own Slack user ID from the Slack connector (the "current logged in user") and their name from their account. Get the Linear workspace slug from any issue URL (`linear.app/<slug>/issue/...`). Read one story description to confirm its acceptance-criteria and open-questions headings.

## 3. Create what Linear needs

- `list_milestones` on the project. If there is no future-enhancements milestone, create one with `save_milestone`: name "Future Enhancements", description "Feedback the team agreed to leave out of the current project. One ticket per piece of feedback, linked to the stories it would change." Record its id.
- Record the id of the new-story milestone they chose.

Tell the user what you created.

## 4. Save the settings

Fill in `config.example.yaml` (repo root) with the answers. Save it:
- to the attached Claude project as `feedback-review/config.yaml` with `project_write`, if a project is attached, or
- otherwise to a private folder the user names. Never into the repo.

Show the user the saved settings in a short table.

## 5. Create the weekly scheduled task

Use `create_trigger` (never local cron tools). Fill in `references/scheduled-run.md` as the prompt. The cron uses the user's timezone, for example `CRON_TZ=America/New_York 52 15 * * 4` for Thursdays just before 4pm (a few minutes off the hour avoids the busiest slot). Turn on push notifications. Tell the user which approval setting the task got.

## 6. Dry run

Run the `feedback-review` skill now against their most recent matching session (widen the date range to the last 14 days for this one run). It publishes a page and DMs only the user, exactly like a normal run. Nothing is posted to the channel and nothing changes in Linear until the user presses the buttons on the page.

Finish with three lines: what was set up, when the first scheduled run happens, and the link to the dry-run page.
