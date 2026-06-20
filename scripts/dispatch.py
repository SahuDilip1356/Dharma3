#!/usr/bin/env python3
"""Dharma3 dispatcher — turn one wave into self-contained sub-agent briefs.

The orchestrator runs this for the current wave; it generates one brief per task that is fully
self-contained (agent contract + the task plan + a read-only STATE slice + worktree + report
instructions). The orchestrator then dispatches one sub-agent per brief — in parallel — each with
a FRESH context that contains only its brief. That is how Dharma3 runs parallel dependent agents
without hitting the dumb zone.

Pure Python 3.9+, zero dependencies.

Usage:
    python3 scripts/dispatch.py <phase> [wave] [--plans-dir plans]
    # wave defaults to the first wave whose tasks are not all marked done in WAVES.json progress
"""
import argparse
import json
import sys
from pathlib import Path

AGENTS_REL = ".claude/skills/dharma3/agents"


def project_root():
    # scripts/ is a child of the project root
    return Path(__file__).resolve().parent.parent


def load_contract(agent):
    path = project_root() / AGENTS_REL / f"{agent}.md"
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    return f"# Operating agent: {agent}\n(Generic agent — no contract file found.)"


def state_slice(root):
    state = root / "memory" / "STATE.md"
    if not state.exists():
        return "(no STATE.md found)"
    text = state.read_text(encoding="utf-8", errors="replace")
    return text[:2000] + ("\n…[truncated]" if len(text) > 2000 else "")


def make_brief(phase, task, plan_text, contract, state_excerpt):
    tid = task["id"]  # already "<phase>-<task>", e.g. "1-2"
    branch = f"d3/{tid}"
    return f"""# Dharma3 sub-agent brief — Task {tid}  [{task['agent']}]

> You are a Dharma3 **{task['agent']}** operating agent. Do ONLY this task. Work in isolation,
> then report back in the exact format below. You do not see the rest of the project on purpose.

## Isolation (worktree)
Work on branch **`{branch}`**. The orchestrator creates it via:
`python3 scripts/worktree.py create {branch}`
Make all your changes there; the orchestrator merges and cleans up after you report done.

---

## Your agent contract
{contract}

---

## Your task plan ({tid}-PLAN.md)
{plan_text}

---

## Shared state (READ-ONLY excerpt — do not rely on anything outside your plan)
```
{state_excerpt}
```

## When finished
Reply with ONLY the "Report back" block from your contract. The orchestrator uses it as the
handoff and writes the evidence into STATE.md.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase")
    ap.add_argument("wave", nargs="?", type=int, default=1)
    ap.add_argument("--plans-dir", default="plans")
    args = ap.parse_args()

    root = project_root()
    plans = Path(args.plans_dir)
    waves_file = plans / f"{args.phase}-WAVES.json"
    if not waves_file.exists():
        print(f"No {waves_file}. Run `/dharma3 route {args.phase}` first.")
        sys.exit(1)

    data = json.loads(waves_file.read_text(encoding="utf-8"))
    waves = data.get("waves", [])
    if not (1 <= args.wave <= len(waves)):
        print(f"Wave {args.wave} out of range (phase has {len(waves)} waves).")
        sys.exit(1)

    wave = waves[args.wave - 1]
    briefs_dir = plans / "briefs"
    briefs_dir.mkdir(parents=True, exist_ok=True)
    state_excerpt = state_slice(root)

    print(f"Dharma3 dispatch — phase {args.phase}, wave {args.wave}: "
          f"{len(wave)} task(s){' (PARALLEL)' if len(wave) > 1 else ''}\n")

    generated = []
    for task in wave:
        tid = task["id"]  # already "<phase>-<task>"
        plan_file = plans / f"{tid}-PLAN.md"
        plan_text = plan_file.read_text(encoding="utf-8", errors="replace") if plan_file.exists() \
            else "(plan file missing)"
        contract = load_contract(task["agent"])
        brief = make_brief(args.phase, task, plan_text, contract, state_excerpt)
        out = briefs_dir / f"{tid}.md"
        out.write_text(brief, encoding="utf-8")
        generated.append(str(out))
        print(f"  [{task['agent']:<8}] task {tid}  → {out}  (branch d3/{tid})")

    print(f"\n  ✓ {len(generated)} brief(s) ready.")
    print("  Orchestrator: dispatch ONE sub-agent per brief IN A SINGLE TURN (parallel).")
    print("  Pass each brief file's contents as the sub-agent prompt. Collect every report,")
    print("  merge each worktree, write evidence to STATE.md, THEN release the next wave.")
    sys.exit(0)


if __name__ == "__main__":
    main()
