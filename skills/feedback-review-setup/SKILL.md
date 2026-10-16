---
name: feedback-review-setup
description: Set up the weekly feedback-review workflow for a new user. Checks that Granola, Linear and Slack are connected, asks a handful of questions, builds and confirms the map of which dev owns which part of the build (with the user, never by guessing), creates the Linear milestones it needs, saves the settings file, creates the weekly scheduled task, and does a dry run that only DMs the user. Use when someone says "set up the feedback review", "install feedback-review", points you at the itskstevens/feedback-review repo, or the feedback-review skill can't find its settings or its owner map isn't confirmed.
---

# Feedback review: setup

Goal: the user goes from nothing to a working weekly review in one conversation. Ask questions with the `AskUserQuestion` tool, batching up to four at a time, and offer choices you've already looked up rather than asking them to type IDs.

**The owner map (step 3) is the most important part of setup.** It decides which dev gets tagged for each piece of feedback. Wrong owners mean devs get pinged for work that isn't theirs, or miss work that is. Build it with the user, confirm every line with them, and test it on real examples before saving. Never fill it in from guesses, assignees or channel membership alone.

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

## 2. Ask the basics, using what you found

Round 1 (look things up first and offer them as options):
1. **Which Granola folder holds the sessions?** Offer folders from `list_meeting_folders`. Allow "none".
2. **What do you call the meeting?** For example "focus group", "demo review", "UAT check-in". This drives title matching and the wording on the page and in Slack.
3. **Which Linear team and project hold the user stories?** Offer from `list_teams` and `list_projects`.
4. **How do story titles start?** Look at the project's issues with `list_issues` and propose the common prefix (for example `US-`).

Round 2:
1. **Which Slack channel gets the approval thread?** Offer from `slack_search_channels`.
2. **Which milestone gets brand-new stories?** Offer from `list_milestones`.
3. **When does the session end each week?** Day, time, timezone. Schedule the run about an hour after.

Get the user's own Slack user ID from the Slack connector (the "current logged in user") and their name from their account. Get the Linear workspace slug from any issue URL (`linear.app/<slug>/issue/...`). Read one story description to confirm its acceptance-criteria and open-questions headings.

## 3. Build the owner map with the user (critical)

The owner map lists each dev who should be tagged, in plain language, with what they own. Every piece of feedback gets matched to one or more owners; only those owners are tagged and asked to approve.

**3a. Who are the owners?** Look up the channel's members (`slack_read_channel` recent posters, `slack_search_users`) and the Linear project's assignees. Present them as candidates and ask, with multi-select: "Which of these people own a part of the build and should be tagged when feedback affects their part?" Say plainly that people who don't own anything here (a lead, an architect, someone on another project) should be left out, and that being in the channel doesn't make someone an owner. Confirm each person's Slack user ID with `slack_search_users`.

**3b. What does each one own?** For each owner, ask the user to describe their part in their own words. Help them be specific by offering what you found in Linear as options to pick from and edit:
- the project's milestones (for example "Phase 1: workflow app", "Phase 2: AI extraction"),
- its labels,
- groups of story titles that cluster together.

Ask them to include where each person's work stops and who owns the infrastructure for it. Record, per owner:
- `owns`: one plain sentence a dev would agree with ("Dynamics and everything UI-facing, plus its infrastructure").
- `signals`: the words, systems, labels and milestones that point to them ("Power Apps", "Dataverse", "SharePoint upload", milestone "1.x").
- `not`: anything easily confused that belongs to someone else, if the user mentions it.

**3c. Test the map on real examples.** Pick 6 to 8 examples that cover every owner and the likely grey areas: a mix of real user stories from the project and, if a past session exists, real feedback items from it. For each, propose the owner(s) using the map and ask the user to confirm or correct, in batches of up to four questions (options: each owner, "more than one", "nobody, it isn't dev work"). After each batch:
- If the user corrected anything, update that owner's `owns`, `signals` or `not`, say what you changed, and test two or three new examples on the same boundary.
- Stop once a full batch comes back with no corrections, or the user says the map is right.

**3d. Confirm the whole map.** Show the final map as a table (name, Slack ID, owns, signals) and ask the user to confirm it explicitly. Save the tested examples with the user's answers as `examples` in the settings, so the weekly run can learn from them. Set `owners_confirmed: true` only after this confirmation.

If the user is unsure about someone, leave that person out and say they can be added later by asking to "update the feedback review owners", which reruns this step only.

## 4. Create what Linear needs

- `list_milestones` on the project. If there is no future-enhancements milestone, create one with `save_milestone`: name "Future Enhancements", description "Feedback the team agreed to leave out of the current project. One ticket per piece of feedback, linked to the stories it would change." Record its id.
- Record the id of the new-story milestone they chose.

Tell the user what you created.

## 5. Save the settings

Fill in `config.example.yaml` (repo root) with the answers. Save it:
- to the attached Claude project as `feedback-review/config.yaml` with `project_write`, if a project is attached, or
- otherwise to a private folder the user names. Never into the repo.

Show the user the saved settings in a short table.

## 6. Create the weekly scheduled task

Use `create_trigger` (never local cron tools). Fill in `references/scheduled-run.md` as the prompt. The cron uses the user's timezone, for example `CRON_TZ=America/New_York 52 15 * * 4` for Thursdays just before 4pm (a few minutes off the hour avoids the busiest slot). Turn on push notifications. Tell the user which approval setting the task got.

## 7. Dry run

Run the `feedback-review` skill now against their most recent matching session (widen the date range to the last 14 days for this one run). It publishes a page and DMs only the user, exactly like a normal run. Nothing is posted to the channel and nothing changes in Linear until the user presses the buttons on the page.

Ask the user to check the owner on each card of the dry-run page. If any are wrong, go back to 3b for that boundary, then rebuild the page.

Finish with three lines: what was set up, when the first scheduled run happens, and the link to the dry-run page.
