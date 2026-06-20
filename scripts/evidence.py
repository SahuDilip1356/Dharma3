#!/usr/bin/env python3
"""Dharma3 evidence gate — a phase cannot close on belief.

Scans the STATE.md "Dependency graph" table for the phase: every task marked `done` must carry
real Evidence. Empty cells, dashes, or banned phrases ("should work", "probably passes", …) FAIL
the gate. This is the deterministic counterpart to the evidence-ledger commit hook — it guards the
/dharma3 verify step before a wave/phase is allowed to close.

Pure Python 3.9+, zero deps.

Usage:
    python3 scripts/evidence.py <phase> [--state memory/STATE.md]
    # exit 0 = every done task has evidence; exit 1 = gate failed (lists offenders)
"""
import argparse
import re
import sys
from pathlib import Path

BANNED = [
    "should work", "should be fine", "should pass", "probably works", "probably passes",
    "i believe it's fixed", "looks correct", "seems to work", "appears correct", "looks good",
]
EMPTY = {"", "-", "—", "todo", "tbd", "n/a", "na", "pending"}


def parse_graph_rows(text):
    """Yield (cells) for each markdown table row under the Dependency graph section."""
    in_section = False
    for line in text.splitlines():
        if line.strip().lower().startswith("## dependency graph"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            yield cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase")
    ap.add_argument("--state", default="memory/STATE.md")
    args = ap.parse_args()

    sp = Path(args.state)
    if not sp.exists():
        print(f"No {args.state}. Nothing to verify.")
        sys.exit(1)

    text = sp.read_text(encoding="utf-8", errors="replace")
    failures, checked = [], 0
    # expected columns: Task | Depends on | Wave | Status | Evidence
    for cells in parse_graph_rows(text):
        if len(cells) < 5:
            continue
        task, _dep, _wave, status, evidence = cells[0], cells[1], cells[2], cells[3], cells[4]
        if task.lower() in ("task", "") or set(task) <= set("-: "):
            continue  # header / separator
        # only enforce tasks of this phase that claim done
        if not task.startswith(f"{args.phase}-"):
            continue
        if status.strip().lower() != "done":
            continue
        checked += 1
        ev = evidence.strip().lower()
        if ev in EMPTY:
            failures.append(f"{task}: marked done but Evidence is empty")
        else:
            hit = next((b for b in BANNED if b in ev), None)
            if hit:
                failures.append(f'{task}: Evidence uses banned phrase "{hit}" — give proof, not belief')

    if checked == 0:
        print(f"evidence-gate: no done tasks for phase {args.phase} yet (nothing to close).")
        sys.exit(0)

    if failures:
        print(f"✗ evidence-gate FAILED for phase {args.phase} ({len(failures)}/{checked} done tasks lack evidence):")
        for f in failures:
            print(f"    - {f}")
        print("\n  Provide real evidence (tests pass / screenshot / browser flow / manual steps) in STATE.md,")
        print("  or downgrade the task status. A phase cannot close on belief.")
        sys.exit(1)

    print(f"✓ evidence-gate PASSED for phase {args.phase}: all {checked} done task(s) carry evidence.")
    sys.exit(0)


if __name__ == "__main__":
    main()
