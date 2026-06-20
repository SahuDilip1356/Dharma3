#!/usr/bin/env python3
"""Dharma3 PreToolUse security/risk gate.

Prompts are not a permission layer. This runs before Bash/Write/Edit tool calls and DENIES
clearly destructive or secret-touching actions — the agent cannot work around an instruction,
but it cannot work around this. Conservative: blocks only high-confidence dangers, else allows.
Zero-dependency. Fail-open on parse errors (never wedge the session), fail-closed on matches.
"""
import json
import re
import sys

# High-confidence destructive / exfiltration patterns.
DANGER = [
    (r"\brm\s+-rf\s+(/|~|\$HOME|\.\.)", "recursive force-delete of a root/home/parent path"),
    (r":\(\)\s*\{\s*:\|\:&\s*\}\s*;", "fork bomb"),
    (r"\bgit\s+push\s+.*--force", "force push (history rewrite)"),
    (r"\bdd\s+if=.*of=/dev/", "raw disk write"),
    (r"\bmkfs\.", "filesystem format"),
    (r"DROP\s+(TABLE|DATABASE)\b", "destructive SQL DROP"),
    (r"TRUNCATE\s+TABLE\b", "destructive SQL TRUNCATE"),
    (r"DELETE\s+FROM\s+\w+\s*;", "unscoped SQL DELETE"),
    (r"\b(curl|wget)\b.*\|\s*(sudo\s+)?(bash|sh)\b", "pipe remote script to shell"),
]

# Secret-bearing files that must not be read/written without explicit human action.
SECRET_PATHS = re.compile(r"(^|/)(\.env(\.|$)|id_rsa|id_ed25519|\.pem$|credentials$|secrets?\.(json|ya?ml))")


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Dharma3 security gate: blocked — {reason}. "
                                        f"If intentional, the human must run it directly.",
        }
    }))
    sys.exit(0)


def main():
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        sys.exit(0)  # fail open

    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}

    if tool == "Bash":
        cmd = ti.get("command", "") or ""
        for pat, why in DANGER:
            if re.search(pat, cmd, re.IGNORECASE):
                deny(why)
        if SECRET_PATHS.search(cmd) and re.search(r"\b(cat|less|head|tail|cp|scp|curl|echo .*>)\b", cmd):
            deny("reading/exfiltrating a secret file")

    if tool in ("Write", "Edit", "Read"):
        path = ti.get("file_path", "") or ""
        if SECRET_PATHS.search(path):
            deny(f"touching a secret file ({path})")

    sys.exit(0)  # allow


if __name__ == "__main__":
    main()
