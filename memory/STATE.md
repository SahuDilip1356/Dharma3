# STATE — Dharma3 (framework self-build)

_Last updated: 2026-06-20 · P7 ship gates built + tested — DHARMA3 CORE COMPLETE_

## Now
- Active phase: — (all build phases P0–P7 complete)
- Active wave: —
- Next action: Prove the full loop on a real feature — `/dharma3 new "<intent>"` (e.g. patient intake forms).

## Roadmap
| Phase | Goal | Status |
|---|---|---|
| P0 | Memory + security hooks (wired in settings) | done |
| P1 | `/dharma3` entry orchestrator + phase playbooks | done |
| P2 | Deterministic router + dependency graph (`scripts/wave_planner.py`) | done |
| P3 | Parallel operating agents — briefs + worktrees + contracts (`dispatch.py`, `worktree.py`) | done |
| P4 | Governance runners — `ai_runners/` (38 tests) + `govern.py` budget gate + risk overlay | done |
| P5 | Verification harness — `evidence.py` gate + evidence-ledger git hook + qa agent real-use | done |
| P6 | Specialist agents — `pm` agent + uiux/design-shotgun/prd refs; router classifies pm/design | done |
| P7 | Ship gates — `ship_gate.py` (G6/G7-SME/G8 verdict) + `evolve.py` system-evolution | done |
| P6 | Specialist agents (D0 uiux-*, pm-prd; GS design-shotgun) | todo |
| P7 | Phase-gates + ship | todo |

## Dependency graph (current phase)
| Task | Depends on | Wave | Status | Evidence |
|---|---|---|---|---|
| — | — | — | — | — |

## Decisions (durable)
- Named the framework **Dharma3** — 2026-06-20
- Spine = GSD-core loop; operating agents = Superpowers; governance = Dharma 1; design/PRD = Dharma 0.x; QA = Gstack; memory = Progression — 2026-06-20 (see DHARMA3_COMPARISON.md)
- Memory + security are hooks (machinery), never instructions — 2026-06-20

## Open loops
| Opened | Loop | Next action |
|---|---|---|
| 2026-06-20 | ✅ P2 router | Done — `scripts/wave_planner.py` (waves, cycle + missing-dep detection, agent classify) |
| 2026-06-20 | ✅ P3 parallel agents | Done — `dispatch.py` (per-task briefs from WAVES.json), `worktree.py` (isolation lifecycle), 4 agent contracts (build/design/qa/research); executor dispatches per-wave sub-agents |
| 2026-06-20 | ✅ P4 governance | Done — ported `ai_runners/` (economics/safety/observability/overlay, 38 tests pass), added `govern.py` (budget gate + telemetry) + `risk_overlay_pre_push.sh` |
| 2026-06-20 | ✅ P5 verification | Done — `evidence.py` gate (scans STATE.md, blocks empty/banned evidence), ported `evidence_ledger_commit_msg.sh` git hook, qa agent wired into verify; installer activates git hooks |
| 2026-06-20 | ✅ P6 specialists | Done — `pm` agent contract + refs (uiux-checklist, design-shotgun, prd-method) distilled from D0/GS; router classifies pm/design; design agent loads refs on demand |
| 2026-06-20 | ✅ P7 ship gates | Done — `ship_gate.py` (G6 evidence + economics + G7 SME scan → G8 GO/CONDITIONAL/HOLD/NO-GO verdict), `evolve.py` (bug→permanent upgrade in learnings.md); SME scan catches healthcare/patient domains |
| 2026-06-20 | 🎯 Prove end-to-end | Run `/dharma3 new` on a real feature; first live run is the acceptance test |
| 2026-06-20 | Confirm est. pricing | opus-4-8 / fable-5 prices in `ai_runners/economics.py` are estimates — verify vs price sheet |
| 2026-06-20 | Confirm est. pricing | opus-4-8 / fable-5 prices in `ai_runners/economics.py` are estimates — verify vs price sheet |
