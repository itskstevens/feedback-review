# Roadmap

The MVP (v0.1) supports Granola, Linear and Slack. Everything below is a candidate, roughly in priority order within each group. Open an issue to vote or propose something.

## Next (v0.2)

- **Carry "still needs discussion" forward.** The weekly run reads the last review page's saved state and brings discussion items back as their own cards, with this week's new input added, until they're classified something else.
- **Status suggestions, opt in.** Propose ticket status moves (for example Backlog to In Progress after a demo) as a separate card the owner can switch on. Off by default.
- **Pre-flight check command.** `feedback-review doctor`: verifies connectors, the settings file, milestone IDs and the scheduled task, and reports what's broken.
- **Upgrade path.** Settings carry a version; the setup skill migrates older settings when the plugin updates.
- **Weekly digest for stakeholders.** Optional short summary of decisions for leads or change managers, sent as a DM or channel post after the owner applies.

## Project tools (adapters)

Each needs the six operations in [docs/adapter-spec.md](docs/adapter-spec.md).

- **GitHub Issues:** milestones and markdown bodies map almost one to one. Easiest after Linear.
- **Asana:** sections stand in for milestones; descriptions are rich text, so patching needs care.
- **Jira:** epics or fix versions for milestones. Descriptions use Atlassian Document Format, so the patch step needs a markdown conversion.
- **Notion databases:** stories as pages, milestones as a select property.
- **Azure DevOps:** work items with iterations as milestones.

## Meeting sources

- **Other note takers:** Fireflies, Otter, Zoom AI Companion, Google Meet transcripts. Same reading step, different connector.
- **Pasted transcript or uploaded recording:** run the review on demand without a connector.
- **Several sessions in one review:** combine two or three sessions from the same week into one page.

## Chat tools

- **Microsoft Teams** for the approval thread and DM.
- **Email** fallback for teams without a chat connector.

## Review page

- **Approvals on the page itself.** Devs approve or hold back each new requirement from a shared copy of the page, instead of replying in Slack.
- **Story diff view.** Show each story before and after all approved updates together, not one update at a time.
- **Edit an update before applying.** Change the wording of a criterion on the page, then apply.
- **Feedback trends.** Track which themes come up week after week across sessions.
- **Export.** Download the week's decisions as Markdown or CSV for status reports.

## Quality

- **Golden-set tests for the weekly run.** A fixed made-up transcript with expected feedback items, run against prompt changes.
- **Accessibility pass** on the review page (keyboard order, screen reader labels).
- **Localization** of page and Slack text.
