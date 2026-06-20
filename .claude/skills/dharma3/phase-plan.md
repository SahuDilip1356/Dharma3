# Phase: PLAN  (owner: GSD + GS + D0)

Covers `/dharma3 new` and `/dharma3 plan`.

## /dharma3 new "<intent>"  — open the project

1. **Interrogate intent (forcing questions — GS office-hours).** Ask, do not assume:
   - What pain is this solving, for whom? (reframe from the pain, not the proposed solution)
   - What does "done" look like — measurable success criteria?
   - What is explicitly out of scope?
   - What is the smallest version that proves value?
   Wait for answers. Do not proceed until intent + success criteria are clear.
2. **Write the PRD (D0 `pm-prd`).** Problem · target user · job stories · success metrics ·
   non-goals · risks. Use `templates/PRD_TEMPLATE.md`. Save to `plans/PRD.md`.
3. **Draft the roadmap** — phases, each a coherent shippable slice. Lean MVP first.
4. **Initialize `memory/STATE.md`** from `state-schema.md` with the roadmap and a single Next action.
5. Stop. Recommend `/dharma3 plan 1`.

## /dharma3 plan <phase>  — atomic, context-fit task plans

1. Read `memory/STATE.md` + `plans/PRD.md`.
2. **Research (GSD plan-phase).** Architecture, components, data flow, libraries, patterns.
   For unknowns, dispatch a research sub-agent (read-only) and fold its findings back.
3. **Decompose into atomic tasks (GSD + SP).** Each task:
   - 2–5 min of focused work, explicit file paths, explicit verification steps.
   - **Verify it fits a clean context** — if a task would overflow, split it. (This is the
     GSD discipline that prevents the dumb zone in parallel agents.)
4. **Write each plan to `plans/<phase>-<task>-PLAN.md` with the router frontmatter contract** so
   the deterministic router can build the graph:

   ```markdown
   ---
   task: 1-2
   depends_on: [1-1]        # tasks that must finish first; empty if none
   agent: build             # build | design | qa | research  (omit → auto-classified)
   title: Intake API endpoint
   ---
   <the implementation steps + verification checks>
   ```
5. Stop. Recommend `/dharma3 route <phase>`.

## /dharma3 route <phase>  — deterministic waves (P2)

1. Run the router (it is deterministic — same plans always yield the same waves):
   ```bash
   python3 scripts/wave_planner.py <phase>
   ```
2. It prints the wave plan, **fails (exit 1) on a cycle or missing dependency**, and on success
   writes `plans/<phase>-WAVES.json` for the executor.
3. Paste the resulting wave/dependency table into STATE.md's "Dependency graph" section.
4. If the router reports errors, fix the offending PLAN frontmatter and re-run. Do not execute a
   broken graph.
5. Stop. Recommend `/dharma3 execute <phase>`.

## Exit evidence
- PRD exists; every task plan has valid router frontmatter; `plans/<phase>-WAVES.json` generated
  with no cycle/missing-dep errors; STATE.md dependency graph updated.
