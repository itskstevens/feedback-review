# Changelog

## 0.2.0

- Owner tagging: each piece of feedback is matched to the dev(s) who own that part of the build. Only they are tagged in Slack, under "Who needs to look at what", and each new requirement waits only on its owners' approval.
- Setup now builds the owner map with the user and tests it on real stories and feedback until the user confirms it. The weekly run won't start without a confirmed map.
- Review page: owner chips on every card, editable before sending; a new requirement can't be sent without an owner; per-owner approval ticks.

## 0.1.0

First release.

- Weekly run skill: reads a Granola session, maps feedback to Linear user stories, builds and publishes the review page, DMs the owner.
- Review page: four classifications per piece of feedback (new requirement, future enhancement, still needs discussion, already covered), Slack approval thread, apply to Linear, saved progress.
- Setup skill: connector checks, guided questions, Future Enhancements milestone, settings file, scheduled task, dry run.
- `build_page.py` validator, unit tests, and a browser test with Linear and Slack mocked.
