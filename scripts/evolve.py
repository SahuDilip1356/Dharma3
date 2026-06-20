#!/usr/bin/env python3
"""Dharma3 system-evolution capture — every bug becomes a permanent upgrade.

The Dharma doctrine: a bug, rework, or failed verification must convert into a durable
rule / hook / skill / test / memory entry, so the same failure can't recur. This appends a
structured improvement to memory/learnings.md (deterministic, append-only).

Usage:
    python3 scripts/evolve.py "<what went wrong>" --as <rule|hook|skill|test|doc> --do "<the fix>"
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KINDS = {"code", "rule", "hook", "skill", "test", "doc"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issue")
    ap.add_argument("--as", dest="kind", required=True, choices=sorted(KINDS))
    ap.add_argument("--do", dest="action", required=True)
    a = ap.parse_args()

    learnings = ROOT / "memory" / "learnings.md"
    learnings.parent.mkdir(parents=True, exist_ok=True)
    if not learnings.exists():
        learnings.write_text("# Learnings — system evolution log\n\n"
                             "Every bug/rework converted into a permanent upgrade.\n",
                             encoding="utf-8")
    day = dt.date.today().isoformat()
    entry = f"\n- **{day}** — {a.issue}\n  → upgrade ({a.kind}): {a.action}\n"
    with learnings.open("a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  ✓ logged system improvement → memory/learnings.md ({a.kind}: {a.action})")
    sys.exit(0)


if __name__ == "__main__":
    main()
