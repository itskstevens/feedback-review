# Writing rules

Everything on the page goes to the owner, the devs, Slack and Linear. Write it the way a busy delivery lead writes, not the way a model writes.

- Plain, specific, active voice. Name the person, team, step or ticket.
- One idea per sentence. Mix sentence lengths.
- Summaries describe the change for users: "A step can hold later steps until it is signed off."
- No em or en dashes. Use a comma, a colon, or two sentences.
- No filler adverbs or buzzwords: seamlessly, significantly, effectively, robust, leverage.
- No "not X, but Y" contrasts, no "Here's what…", no rhetorical questions, no closing one-liners.
- Don't invent attribution. If the transcript doesn't say who, write "Attendee (likely <name>)" or "Attendee".
- Don't invent dates, decisions or tickets.

`build_page.py` flags dashes and the listed filler words as warnings. Fix them before publishing.
