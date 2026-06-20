#!/usr/bin/env python3
"""Dharma3 ship gate — the lead-agent release evaluation (Dharma 0.x G6–G8 + SME).

Deterministically checks release readiness for a phase and emits a verdict:
  GO          — all gates pass; proceed to human approval + PR
  CONDITIONAL — passes but SME sign-off is required and missing
  HOLD        — a soft gate failed (e.g. over budget); resolve then re-run
  NO-GO       — evidence gate failed; not shippable

Composes the already-tested machinery: evidence.py (G6 verification) + govern.py (economics) +
an SME applicability scan (G7) over the PRD and the git diff.

Usage:
    python3 scripts/ship_gate.py <phase> [--ceiling 10.0] [--state memory/STATE.md]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SME_REGEX = re.compile(
    r"\b(legal|medical|clinical|patient|health|hipaa|phi|diagnos|prescri|"
    r"financial|payment|billing|invoice|tax|auth|password|credential|brand)\b", re.I)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return r.returncode, (r.stdout + r.stderr).strip()


def changed_files():
    rc, out = run(["git", "diff", "--name-only", "HEAD~1...HEAD"])
    if rc != 0:
        rc, out = run(["git", "diff", "--name-only"])
    return out.splitlines() if out else []


def sme_required(phase):
    """G7: does this change touch a domain needing expert sign-off?"""
    hits = set()
    prd = ROOT / "plans" / "PRD.md"
    if prd.exists():
        for m in SME_REGEX.findall(prd.read_text(encoding="utf-8", errors="replace")):
            hits.add(m.lower())
    for f in changed_files():
        for m in SME_REGEX.findall(f):
            hits.add(m.lower())
    return sorted(hits)


def sme_signed(state_path):
    if not state_path.exists():
        return False
    text = state_path.read_text(encoding="utf-8", errors="replace").lower()
    return "sme: approved" in text or "sme sign-off: approved" in text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase")
    ap.add_argument("--ceiling", type=float, default=None)
    ap.add_argument("--state", default="memory/STATE.md")
    args = ap.parse_args()
    state_path = ROOT / args.state

    print(f"Dharma3 ship gate — phase {args.phase}\n")
    verdict = "GO"
    notes = []

    # G6 — evidence (hard gate)
    rc, out = run(["python3", "scripts/evidence.py", args.phase, "--state", args.state])
    if rc == 0:
        print("  ✓ G6 evidence — all done tasks carry proof")
    else:
        print("  ✗ G6 evidence — FAILED")
        for line in out.splitlines():
            if line.strip().startswith("-"):
                print(f"      {line.strip()}")
        verdict = "NO-GO"
        notes.append("fix evidence gaps (see /dharma3 verify)")

    # economics (soft gate)
    if args.ceiling is not None:
        rc, out = run(["python3", "scripts/govern.py", "gate", "--ceiling", str(args.ceiling)])
        print(f"  {'✓' if rc == 0 else '✗'} budget — {out.strip().split(':',1)[-1].strip()}")
        if rc != 0 and verdict == "GO":
            verdict = "HOLD"
            notes.append("over budget — raise ceiling or trim scope")

    # G7 — SME sign-off
    domains = sme_required(args.phase)
    if domains:
        if sme_signed(state_path):
            print(f"  ✓ G7 SME — sign-off present (domains: {', '.join(domains)})")
        else:
            print(f"  ⚠ G7 SME — REQUIRED for: {', '.join(domains)} — no sign-off found in STATE.md")
            if verdict == "GO":
                verdict = "CONDITIONAL"
            notes.append("get domain-expert sign-off; add 'SME: approved — <name>' to STATE.md")
    else:
        print("  ✓ G7 SME — not applicable (no sensitive domains touched)")

    # G8 — lead-agent verdict
    print(f"\n  ── G8 lead-agent verdict: {verdict} ──")
    if verdict == "GO":
        print("  Next: present a one-screen summary (what shipped · evidence · risks · rollback)")
        print("        for HUMAN APPROVAL, then open the PR. Log one system improvement.")
    else:
        for n in notes:
            print(f"    → {n}")
    sys.exit(0 if verdict == "GO" else 1)


if __name__ == "__main__":
    main()
