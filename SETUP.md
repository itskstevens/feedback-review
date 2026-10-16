# Setup instructions for Claude

You're an agent helping a user install feedback-review. Follow these steps in order. Keep the user informed in short lines; ask questions with your question tool.

## 1. Install the plugin

- **Cowork or Claude Code with plugin support:** add the marketplace `itskstevens/feedback-review` and install `feedback-review@itskstevens`. In Claude Code that's:
  ```
  /plugin marketplace add itskstevens/feedback-review
  /plugin install feedback-review@itskstevens
  ```
  In Cowork, use the plugin tools to add the same marketplace, or ask the user to add it from the plugin settings.
- **No plugin support:** clone or download the repo, and use `skills/feedback-review/SKILL.md` and `skills/feedback-review-setup/SKILL.md` as skills (upload them as account skills if the product allows it).

Confirm both skills are available before going on.

## 2. Run the setup skill

Run `feedback-review-setup`. It:

1. checks Granola, Linear, Slack, artifacts with connector access, and scheduled tasks,
2. asks the basics (folder, meeting name, Linear team and project, story prefix, Slack channel, milestone for new stories, weekly time),
3. **builds the owner map with the user**: who owns which part of the build, tested on real stories and feedback until the user confirms it. Don't skip or shortcut this; it decides who gets tagged every week,
4. creates a Future Enhancements milestone in Linear if there isn't one,
5. saves the settings to the user's Claude project as `feedback-review/config.yaml`,
6. creates the weekly scheduled task,
7. does a dry run on the latest matching session that only DMs the user.

## 3. Hand over

Tell the user, in three lines: what's set up, when the first run happens, and the link to the dry-run page. Point them at the README's "How it works" section.

## Rules while setting up

- Never put the user's settings, meeting content or IDs into the repo or a pull request.
- Never guess the owner map. Every owner and what they own comes from the user, and the user confirms the final map.
- Don't post to any Slack channel during setup. The dry run messages only the user.
- If a connector or capability is missing, say which one and how to add it, then stop. Don't build workarounds.
