# Design-shotgun reference  (from Gstack)

Use when a user-facing surface needs *exploration* before committing to one direction — a new
screen, a redesign, an unclear layout. Generate options, don't settle on the first idea.

## Method
1. **Frame the problem** — the screen's one job, the primary user action, the constraints.
2. **Generate 4–6 distinct variants** — genuinely different directions (layout, hierarchy,
   density, tone), not 6 tints of the same idea. Each as a quick mockup (HTML or static).
3. **Annotate each** — what it optimizes for and its trade-off (e.g. "scannable but dense",
   "calm but more scrolling").
4. **Recommend one** with reasoning, then converge. Hand the chosen direction to the design agent
   to build against the UI/UX checklist.

## Output
```
VARIANTS (4–6): <one-line description + trade-off each>
RECOMMENDATION: <which + why>
NEXT: build chosen variant → uiux-checklist verification
```
Keep mockups cheap and disposable — the point is range, then a decision.
