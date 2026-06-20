# Dharma3 — Framework Comparison & Scoring (Decision Record)

> **Status:** Living document. Designed to be revisited — add new frameworks to the registry, re-score, and the build plan updates accordingly.
> **Last updated:** 2026-06-20
> **Owner:** Dilip Sahu

Dharma3 is the multi-agent product-development framework assembled by scoring six existing
frameworks component-by-component and hand-picking the winner of each. This file is the
**decision record**: what was compared, how it was scored, and why each pick was made.

For the build mapping (which concrete files/skills to port), see **`DHARMA3_BUILD_PLAN.md`**.

---

## 1. Framework registry (the contenders)

| Code | Framework | Source | One-line identity |
|---|---|---|---|
| **D0** | Dharma 0.x | `Skills Library/Dharma/` · github.com/SahuDilip1356/Dharma | 38-skill governance + design library; instructions, not machinery |
| **D1** | Dharma 1 | `Skills Library/Gstack/` (mislabeled folder) · github.com/SahuDilip1356/dharma-1 | 23-skill, deterministic router + Python governance + 2 enforcing hooks |
| **GS** | Gstack | github.com/garrytan/gstack | Proven 7-stage TS toolkit; Conductor parallel runner, real-browser QA, GBrain |
| **OS** | Claude Product Development OS | `Ref1/claude_product_development_os.zip` | Lightweight 8-stage scaffold; clean templates + pre-tool security hook |
| **SP** | Superpowers | github.com/obra/superpowers | Composable software-dev methodology: subagent-driven, parallel dispatch, worktrees, TDD, 2-stage review |
| **GSD** | GSD-core | github.com/open-gsd/gsd-core · `Skills Library/GSD/` | Purest orchestrator: discuss→plan→execute→verify→ship, parallel fresh-context waves, prerequisite dependencies, STATE.md |
| **PROG** | Progression Memory | `~/.progression-memory/` + `.agent/` | Deterministic hook-driven memory engine (capture / resume / shared state). The memory backbone all six lack. |

> **To add a framework on revisit:** append a row here, score it through Sections 3–4 using the
> same rubric, and re-run the source tally in Section 6. If it wins or co-owns any component,
> update `DHARMA3_BUILD_PLAN.md`.

---

## 2. Scoring method

1. **Rate each component:** ● = 3 (native/strong) · ◐ = 1 (partial) · ○ = 0 (absent/weak)
2. **Normalize each layer to /10** so a layer with many components doesn't outweigh a small one.
3. **Weight each layer by relevance to the goal** — a multi-agent orchestrator with parallel,
   mutually-dependent operating agents and complete memory.
4. **Tiebreaker rule:** when scores tie → (a) enforced *machinery* beats *instruction*, then
   (b) *proven* beats *alpha*. Where two contenders are both strong and **complementary**, they
   are kept together in a **dual bucket** (e.g. `GSD / OS`).

### Layer weights

| Layer | Weight | Rationale |
|---|:--:|---|
| A Orchestration | 3.0 | The spine — parallel dependent agents |
| F Memory | 2.5 | Shared state across parallel agents = make-or-break |
| D Verification | 2.5 | Each wave must self-prove before the next depends on it |
| B Planning | 2.0 | Decomposition feeds the waves |
| E Governance | 2.0 | Every agent needs a security/risk gate |
| C Execution | 1.5 | Important but commoditized |
| H Platform/Harness | 1.5 | Hooks / portability / the owned AI layer |
| G Design | 1.0 | A specialist agent, not the spine |

---

## 3. Weighted score summary

### Normalized per-layer scores (0–10) + layer owner

| Layer | D0 | D1 | GS | OS | SP | GSD | 🏆 Owner |
|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| A Orchestration | 2.1 | 3.3 | 6.7 | 2.9 | 7.9 | **8.3** | GSD-core |
| B Planning | 2.2 | 5.0 | 7.8 | 2.8 | 7.8 | **8.9** | GSD-core |
| C Execution | 8.3 | 5.0 | 6.7 | 2.5 | **8.3** | 8.3 | Superpowers (proven+TDD) |
| D Verification | 3.3 | 6.7 | **8.9** | 2.2 | **8.9** | 6.7 | Gstack (empirical+proven) |
| E Governance | 5.3 | **7.3** | 6.0 | 4.0 | 1.3 | 2.7 | Dharma 1 |
| F Memory | 1.7 | 3.3 | **10.0** | 5.0 | 2.5 | 6.7 | Gstack → Progression engine |
| G Design | **10.0** | 3.3 | 10.0 | 0 | 0 | 0 | Dharma 0.x (8 skills deeper) |
| H Platform | 4.2 | 8.3 | 8.3 | 5.8 | **10.0** | 6.7 | Superpowers |

### Overall weighted ranking (max 160)

| Rank | Framework | Score | Read |
|:--:|---|:--:|---|
| 1 | Gstack | 127 | The all-rounder — no weak layer |
| 2 | GSD-core | 104 | Orchestration king, weak governance/memory |
| 3 | Superpowers | 98 | Execution+platform king, no governance/design |
| 4 | Dharma 1 | 83 | Governance core, thin orchestration |
| 5 | Dharma 0.x | 63 | Design+execution, no machinery |
| 6 | OS.zip | 53 | Eliminated (wins no layer outright) |

> **Interpretation:** Gstack wins as a *single tool to use*. But the goal is to *build*, so the
> decision is made at **component granularity** (Section 4), which is buildable and resolves every tie.

---

## 4. Full component scoring & picks (the Dharma3 BOM)

Score column shows the winning score(s). Dual buckets (`A / B`) keep two complementary winners.
Cell scores order: **D0 · D1 · GS · OS · SP · GSD**.

| Layer (wt) | Component | Raw (D0·D1·GS·OS·SP·GSD) | Score | ✅ Pick (bucket) | Element(s) to box | Justification |
|---|---|---|:--:|---|---|---|
| **Orchestration (3.0)** | A1 Orchestrator | 1·1·3·1·3·3 | 3/3 | **GSD / SP** | lean-main-delegates / inspect-&-review subagent | GSD purest thin-orchestrator; SP adds review rigor |
| Orchestration | A2 Parallel execution | 0·0·3·0·3·3 | 3/3 | **GSD / SP** | dependency-ordered waves / dispatching-parallel-agents | GSD owns waves; SP is the dispatch mechanism |
| Orchestration | A3 Dependency mgmt | 1·1·1·1·1·3 | 3 | **GSD** | per-task prerequisites + dep-verify | Only one with explicit inter-agent dependencies |
| Orchestration | A4 Fresh context per agent | 0·1·3·1·3·3 | 3 | **GSD** | 200k clean context per executor | Anti-context-rot core thesis |
| Orchestration | A5 Handoff artifacts | 1·1·3·3·3·3 | 3/3 | **GSD / OS** | STATE.md+CONTEXT.md / Handoff-report template | GSD machine-resumable; OS clean human report |
| Orchestration | A6 Worktree isolation | 0·0·1·0·3·1 | 3 | **SP** | using-git-worktrees (clean baseline) | Gold standard for parallel isolation |
| Orchestration | A7 Deterministic dispatch | 1·3·1·0·0·1 | 3 | **D1** | Python classifier router | Only non-model-guessed wave assignment |
| Orchestration | A8 Subagent-driven impl | 1·1·1·1·3·3 | 3/3 | **SP / GSD** | inspect-&-review / per-task focused-ctx verify | SP rigor + GSD built-in verify |
| **Planning (2.0)** | B1 Intent capture | 1·3·3·1·3·3 | 3/3 | **GS / GSD** | office-hours 6 forcing Qs / discuss-phase capture | GS interrogates; GSD captures into loop |
| Planning | B2 Scope control | 1·3·3·1·1·1 | 3 | **D1** | plan-ceo 4 modes | Owned, zero-dep |
| Planning | B3 Atomic decomposition | 1·1·1·1·3·3 | 3/3 | **GSD / SP** | context-fit plans / 2–5min file-path tasks | GSD ctx-fit; SP file-path precision |
| Planning | B4 Research sub-agents | 0·1·3·1·3·3 | 3/3 | **GS / GSD** | stack research / plan-phase gated research | GS breadth; GSD gates into planning |
| Planning | B5 Plan-fits-context verify | 0·0·1·0·1·3 | 3 | **GSD** | verify plan fits clean window | Unique — critical for parallel waves |
| Planning | B6 Forced clarifying Qs | 1·1·3·1·3·3 | 3/3 | **GS / SP** | Grill-Me/office-hours / brainstorming Qs | Both force intent alignment pre-build |
| Planning | PRD definition | 3·1·3·2·1·1 | 3/2 | **D0 / OS** (+GS) | pm-prd+PM suite / PRD_TEMPLATE (→ GS `spec`) | D0 product discipline; OS template; GS→exec spec |
| **Execution (1.5)** | C1 No-scope-creep | 3·3·3·1·3·3 | 3/3 | **GSD / D1** | executor "no-improvise" / karpathy-check gate | GSD statement; D1 enforcing gate |
| Execution | C2 TDD / test-first | 3·1·1·0·3·1 | 3 | **SP** | RED-GREEN-REFACTOR | Original source, deeper than D0 port |
| Execution | C3 Surgical / minimal change | 3·1·1·1·1·3 | 3 | **D0** | surgical-changes skill | Only dedicated minimal-diff discipline |
| Execution | C4 Checkpoint + iterate | 1·1·3·1·3·3 | 3/3 | **GSD / SP** | per-task verify→STATE / batch checkpoints | GSD parallel-safe; SP batch |
| **Verification (2.5)** | D1 Evidence enforcement | 1·3·1·1·3·3 | 3 | **D1** | evidence-ledger.sh hook | Machinery, not instruction |
| Verification | D2 Self-verification harness | 1·3·3·1·3·3 | 3 | **GS** | real-browser empirical harness | Empirical beats checklist |
| Verification | D3 Adversarial / 2-stage review | 1·3·3·1·3·1 | 3/3 | **SP / GS** (+D1) | spec-then-quality 2-stage / adversarial session / codex | SP structure; GS adversarial; D1 cross-model |
| Verification | D4 Real-world / browser check | 1·1·3·0·1·1 | 3 | **GS** | Playwright / Agent-Browser | Only true real-browser harness |
| Verification | D5 Diagnose-fix before close | 1·1·3·1·3·3 | 3/3 | **SP / GSD** | systematic-debugging 4-phase / verify→fix-plan gate | SP method; GSD gate |
| Verification | D6 Regression generation | 1·1·3·0·3·1 | 3/3 | **SP / GS** | TDD native regression / explicit regression-gen | SP built-in; GS explicit |
| **Governance (2.0)** | E1 Security pre-tool gate | 0·3·3·3·0·0 | 3/3 | **OS / D1** (+GS) | pre_tool_use_security_check.py / risk-overlay.sh (/injection-ML) | OS liftable base; D1 wrapper; GS upgrade |
| Governance | E2 Risk gating | 1·3·3·1·0·0 | 3/3 | **D1 / GS** | risk overlay + risk-gate / freeze-guard dir locks | D1 always-on; GS directory locks |
| Governance | E3 AI safety/econ/observability | 1·3·1·0·0·0 | 3 | **D1** | ai_runners Python (38 safety tests) | Only testable AI governance code |
| Governance | E4 Phase gates + SME | 3·1·1·1·1·1 | 3 | **D0** | G6–G8 + SME + lead-agent eval | Most rigorous gate stack |
| Governance | E5 Human approval | 3·1·1·1·1·3 | 3/3 | **GSD / D0** | discuss-phase front-load / phase-gate at ship | GSD upfront; D0 ship-time |
| **Memory (2.5)** | F1 Session-capture hook | 0·1·3·3·1·1 | 3 | **PROG / GS** | deterministic capture hook / dreaming-promote | Progression fills; GS promote-to-primary model |
| Memory | F2 State continuity | 0·1·3·1·1·3 | 3 | **GSD** | STATE.md shared state across parallel agents | Exactly the parallel-agent need |
| Memory | F3 Decision / pattern store | 1·1·3·1·0·1 | 3 | **PROG / GS** | decisions+patterns drawers / GBrain | Progression zero-dep; GBrain reference |
| Memory | F4 Cross-session resume | 1·1·3·1·1·3 | 3 | **PROG** | hook-driven deterministic resume | Deterministic beats instruction-resume |
| **Design (1.0)** | G1 UI/UX depth | 3·1·3·0·0·0 | 3 | **D0** | the 8 uiux-* skills | Only first-class a11y + design-system suite |
| Design | G2 Visual gen + visual-QA loop | 3·1·3·0·0·0 | 3 | **GS** | design-shotgun + screenshot-iterate | Empirical visual QA |
| **Platform/Harness (1.5)** | H1 Hooks / enforcement | 0·3·3·3·3·1 | 3/3 | **D1 / OS** (SP/GS pattern) | 2 git hooks / 3 python hooks | Own+ship zero-dep; copy event-driven model |
| Platform | H2 Skills composability | 3·3·3·1·3·1 | 3 | **SP** | composable-skill workflow chaining | Composability is its thesis |
| Platform | H3 Install / portability | 1·3·1·3·3·3 | 3/3 | **D1 / GSD** | 60s zero-dep / npm multi-runtime | D1 simplicity + GSD distribution |
| Platform | H4 Maturity reference | 1·1·3·0·3·3 | 3 | **GS** | most battle-tested patterns | Reliability benchmark |

---

## 5. Standalone capability spotlights

| Capability | 🏆 Winner | Runner-up (better at…) |
|---|---|---|
| **PRD definition** | **Dharma 0.x** — `pm-prd` + PM suite (job-stories, user-stories, prioritization) | OS.zip (PRD template artifact) · Gstack (`spec` → executable spec) |
| **UI/UX designing** | **Dharma 0.x** — 8 uiux-* skills (a11y, responsive, interaction, design-system) | Gstack (visual generation + screenshot-iterate visual QA) |

---

## 6. Source ownership tally (final)

| Source | Components owned/co-owned | Role in Dharma3 |
|---|:--:|---|
| GSD-core | 12 | Orchestration + planning spine |
| Superpowers | 10 | Operating-agent toolkit + composability |
| Gstack | 9 | Empirical QA + visual QA + reliability |
| Dharma 1 | 8 | Governance + router + harness hooks |
| Dharma 0.x | 5 | PRD/PM + UI/UX + surgical + phase-gates |
| OS.zip | 3 | Security hook + handoff/PRD templates |
| Progression | 4 | Complete memory backbone |

**40 components · 8 layers · 6 frameworks + Progression · every tie resolved, zero overlaps.**

---

## 7. Change log (for revisits)

| Date | Change |
|---|---|
| 2026-06-20 | Initial assessment: 6 frameworks scored across 40 components; Dharma3 BOM locked; named **Dharma3**. |

> When you revisit: add a row here, update the registry (Section 1), re-score, and reconcile the
> build plan. Candidate frameworks to compare next: OpenClaude, Hermes, Conductor (standalone),
> Archon (Cole Medin), Ralph-loop variants.
