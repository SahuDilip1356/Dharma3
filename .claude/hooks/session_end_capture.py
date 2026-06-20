#!/usr/bin/env python3
"""Dharma3 SessionEnd hook — deterministic session capture.

Writes a dated session digest stub to memory/sessions/ so continuity never depends on the
model remembering to log. A richer LLM synthesis can enrich these later (P2). Fails open.
"""
import datetime as dt
import json
import sys
from pathlib import Path


def find_root():
    here = Path.cwd()
    for d in [here, *here.parents]:
        if (d / "memory").is_dir():
            return d
    return here


def main():
    payload = {}
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}

    root = find_root()
    sessions = root / "memory" / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)

    now = dt.datetime.now()
    day = now.strftime("%Y-%m-%d")
    digest = sessions / f"{day}.md"

    reason = payload.get("reason", "session end")
    transcript = payload.get("transcript_path", "—")
    line = (
        f"\n## {now.strftime('%H:%M')} — capture ({reason})\n"
        f"- transcript: {transcript}\n"
        f"- next: review `memory/STATE.md` `Now → Next action`\n"
    )
    header = f"# Sessions — {day}\n" if not digest.exists() else ""
    with digest.open("a", encoding="utf-8") as f:
        f.write(header + line)

    sys.exit(0)


if __name__ == "__main__":
    main()
