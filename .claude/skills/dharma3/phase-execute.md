# Phase: EXECUTE  (owner: Superpowers + GSD + D1)

Covers `/dharma3 execute <phase>`.

## Role
You are a senior engineer executing a precise plan. You do not improvise. You do not expand
scope ("just while I'm here…"). Implement exactly what the plan specifies, verify, move on.

## P1 — single-agent execution (current scaffold)

1. Read `memory/STATE.md` and **`plans/<phase>-WAVES.json`** (the router's output from
   `/dharma3 route`). If it is missing, run `/dharma3 route <phase>` first — never execute
   without a validated wave plan.
2. Process **wave by wave, in order**. Within a wave, do the tasks one at a time (P1). For each task:
   - Read its `plans/<phase>-<task>-PLAN.md`.
   - Announce: `▶ Wave <w> · Task <id> [<agent>]: <title>`.
   - Implement each step; create/modify exactly the files named. Confirm `✓ Created/Modified: <path>`.
   - Run the task's verification steps (build/lint/test). If a check fails, fix and re-run.
   - **Update STATE.md**: mark the task done, record evidence, set the next action.
3. Only start a wave once **every task in the prior wave is done with evidence** (its dependents
   are now unblocked). After the last wave, recommend `/dharma3 verify <phase>`.

## P3 — parallel waves (built)

Run this when you want true parallelism. For each wave, the tasks are independent (the router
guaranteed it), so they run as **separate sub-agents at the same time**, each in its own worktree
with a fresh context.

For the current wave `<w>`:

0. **Governance gate (P4).** Before dispatching, run the budget gate:
   `python3 scripts/govern.py gate --ceiling <usd>` — if it exits non-zero, stop and hand off or
   raise the ceiling; do not start the wave. (The PreToolUse security/risk hook already guards
   every individual action.)
1. **Generate briefs.** `python3 scripts/dispatch.py <phase> <w>` writes one self-contained brief
   per task to `plans/briefs/<task>.md` (agent contract + the task plan + a read-only STATE slice +
   its branch name + report format).
2. **Create isolation.** For each task, `python3 scripts/worktree.py create d3/<task>` — an isolated
   git worktree + branch so parallel agents never collide.
3. **Dispatch in parallel.** In **one turn**, spawn one sub-agent per task (the Agent/Task tool),
   passing that task's brief file contents as the prompt and pointing it at its worktree. Pick the
   sub-agent persona by the brief's agent type (build / design / qa / research). Fresh context each —
   they only ever see their brief.
4. **Collect reports.** Wait for every sub-agent's "Report back" block. If any reports `blocked` or
   `fail`, resolve before merging.
5. **Merge + record.** `python3 scripts/worktree.py merge d3/<task>` for each, then
   `worktree.py remove d3/<task>`. Write each task's evidence into STATE.md and mark it done.
   Log each agent's spend: `python3 scripts/govern.py record --model <m> --in <n> --out <m> --agent <type>:<task>`.
6. **Release the next wave** — its prerequisites are now satisfied. Repeat from step 0 for wave `<w+1>`.

> Single-agent vs parallel is a choice, not a rewrite: skip steps 1–5's parallelism and just do the
> P1 loop above for small phases; use P3 when a wave has 2+ independent tasks worth fanning out.

## Discipline (D1 karpathy-check)
- Keep changes small and traceable. No unrelated rewrites. No new dependencies without a why.
- The security/risk hook will block dangerous tool calls automatically — do not work around it.

## Exit evidence
- Every task in the phase marked done in STATE.md with concrete evidence; working tree builds.
