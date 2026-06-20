# PRD method reference  (from Dharma 0.x pm-prd + PM suite)

Grounded in Teresa Torres / Marty Cagan / Dan Olsen. A structured thinking process, not a template
dump. **Ask clarifying questions before writing** — tight scope beats vague expansion.

## Ask first (one at a time, stop when confident)
1. **Problem** — what specific problem, for whom exactly?
2. **Users** — which segments? their current workaround?
3. **Success** — SMART, measurable metrics?
4. **Constraints** — technical / timeline / resource?
5. **Scope** — full vs phased? v1 vs later?

## The 8-section PRD
1. **Summary** — one paragraph: what & why.
2. **Problem & opportunity** — the pain, evidence, why now.
3. **Goals & success metrics** — measurable; include counter-metrics (what must not regress).
4. **Users & job stories** — *When <situation>, I want <motivation>, so I can <outcome>.*
5. **Requirements** — prioritized (see below); each testable.
6. **Non-goals** — explicit out-of-scope. This section is mandatory.
7. **Risks & assumptions** — flag every assumption; name the riskiest.
8. **Validation & rollout** — how "done" is proven; phased plan; rollback.

## Prioritization (pm-prioritization)
- Tag each requirement **P0 (core, ship-blocker) · P1 (important) · P2 (nice-to-have)**.
- Lean MVP = P0 only. Resist building for imaginary power users. Prove value, then expand.

## User stories vs job stories
- Job story (preferred for discovery): situation → motivation → outcome.
- User story (for build): *As a <role>, I want <feature>, so that <benefit>* + acceptance criteria.

Output: `plans/PRD.md`. Every requirement testable, every assumption flagged, non-goals explicit.
