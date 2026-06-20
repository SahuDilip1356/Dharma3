#!/usr/bin/env python3
"""Dharma3 SessionStart hook — auto-load the project STATE into context.

Machinery, not instruction: the orchestrator never has to remember to read STATE.md;
this injects it on every session start so any fresh session resumes cold.
Zero-dependency. Fails open (never blocks a session).
"""
import json
import sys
from pathlib import Path


def find_state():
    # project root = nearest ancestor containing memory/STATE.md, starting from cwd
    here = Path.cwd()
    for d in [here, *here.parents]:
        candidate = d / "memory" / "STATE.md"
        if candidate.exists():
            return candidate
    return None


def main():
    try:
        _ = sys.stdin.read()  # consume hook input (unused)
    except Exception:
        pass

    state = find_state()
    if not state:
        # No project yet — nudge toward starting one, but don't block.
        ctx = "No Dharma3 STATE.md found. Start a project with `/dharma3 new \"<intent>\"`."
    else:
        text = state.read_text(encoding="utf-8", errors="replace")
        # Keep it lean — STATE.md is meant to be small. Cap to avoid context bloat.
        if len(text) > 6000:
            text = text[:6000] + "\n…[STATE.md truncated — open the file for full detail]"
        ctx = "## Dharma3 — resumed STATE (auto-loaded)\n\n" + text

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": ctx,
        }
    }
    print(json.dumps(out))
    sys.exit(0)


if __name__ == "__main__":
    main()
