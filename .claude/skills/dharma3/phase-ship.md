# Phase: SHIP  (owner: D0 + GSD)

Covers `/dharma3 ship <phase>`. Ship with rollback. Turn every issue into a permanent upgrade.

## Gate stack (run the machinery)

Run the deterministic ship gate — it composes G6 (evidence), economics, and G7 (SME) into a G8 verdict:

```bash
python3 scripts/ship_gate.py <phase> [--ceiling <usd>]
```

- **G6 evidence** — every done task must carry proof (reuses `evidence.py`). Fail → **NO-GO**.
- **Economics** — over the ceiling → **HOLD**.
- **G7 SME** — if the diff/PRD touches legal / medical / patient / financial / auth / brand, a
  domain-expert sign-off is required. Missing → **CONDITIONAL**. Record it by adding a line
  `SME: approved — <name>, <date>` to STATE.md, then re-run.
- **G8 verdict** — `GO` (exit 0) means proceed to human approval; anything else blocks with the fix list.

4. **Human approval.** On GO, present a one-screen summary (what shipped · evidence · risks ·
   rollback) and wait for the project owner's explicit GO. Never deploy to production without it.

## Release (GSD ship)
- Open a PR with: what changed, why, evidence links, and a **rollback path**.
- Archive the phase: mark roadmap status `done` in STATE.md, move plans to `plans/archive/`.
- Observe after release (manual check or canary) before calling it closed.

## System evolution (mandatory)
Every bug, rework, or failed verification from this phase becomes a permanent upgrade. Capture it:

```bash
python3 scripts/evolve.py "<what went wrong>" --as <rule|hook|skill|test|doc> --do "<the fix>"
```

This appends to `memory/learnings.md` so the same failure can't recur. Also note it in STATE.md `Decisions`.

## Exit evidence
- PR open with rollback path · human approval recorded · roadmap updated · ≥1 system improvement logged.
