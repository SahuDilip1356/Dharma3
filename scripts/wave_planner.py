#!/usr/bin/env python3
"""Dharma3 deterministic router — dependency graph → ordered waves.

Reads the task plans for a phase (plans/<phase>-<task>-PLAN.md), each carrying a small
machine-readable frontmatter contract:

    ---
    task: 1-2
    depends_on: [1-1]        # or: 1-1, 1-3   (empty/absent = no deps)
    agent: build             # build | design | qa | research  (absent → inferred)
    title: Build the intake form
    ---

It builds the dependency graph and groups tasks into **waves** by topological level:
  - Wave 1 = every task with no unmet prerequisite (these run in parallel)
  - Wave 2 = tasks whose prerequisites are all in earlier waves
  - ... and so on.
It detects cycles and missing dependencies, classifies each task to an agent type, writes a
machine-readable plans/<phase>-WAVES.json for the executor (P3), and prints a human summary.

Pure Python 3.9+, zero dependencies. Deterministic: same plans → same waves, every time.

Usage:
    python3 scripts/wave_planner.py <phase> [--json] [--plans-dir plans]
"""
import argparse
import json
import re
import sys
from pathlib import Path

AGENT_TYPES = {"build", "design", "qa", "research", "pm"}
PM_KW = re.compile(r"\b(prd|spec|requirements?|prioriti[sz]e|roadmap|user stor|job stor|product brief)", re.I)
DESIGN_KW = re.compile(r"\b(ui|ux|design|css|layout|screen|component|a11y|accessib|responsive|visual)", re.I)
QA_KW = re.compile(r"\b(test|qa|verify|e2e|regression|coverage)", re.I)
RESEARCH_KW = re.compile(r"\b(research|investigate|spike|explore|evaluate)", re.I)


def parse_frontmatter(text):
    """Return dict from a leading --- ... --- block, else {}."""
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm


def parse_deps(raw):
    if not raw:
        return []
    raw = raw.strip().strip("[]")
    if not raw:
        return []
    return [d.strip() for d in raw.split(",") if d.strip()]


def classify_agent(fm, title):
    a = (fm.get("agent") or "").strip().lower()
    if a in AGENT_TYPES:
        return a
    blob = f"{title} {fm.get('agent','')}"
    if PM_KW.search(blob):
        return "pm"
    if DESIGN_KW.search(blob):
        return "design"
    if QA_KW.search(blob):
        return "qa"
    if RESEARCH_KW.search(blob):
        return "research"
    return "build"


def load_tasks(phase, plans_dir):
    tasks = {}
    pattern = re.compile(rf"^{re.escape(str(phase))}-(.+)-PLAN\.md$")
    for p in sorted(Path(plans_dir).glob(f"{phase}-*-PLAN.md")):
        if not pattern.match(p.name):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        tid = fm.get("task") or p.name[:-len("-PLAN.md")]
        title = fm.get("title", tid)
        tasks[tid] = {
            "id": tid,
            "title": title,
            "depends_on": parse_deps(fm.get("depends_on")),
            "agent": classify_agent(fm, title),
            "file": str(p),
        }
    return tasks


def build_waves(tasks):
    """Kahn level-grouping. Returns (waves, errors)."""
    errors = []
    ids = set(tasks)
    # validate deps
    for t in tasks.values():
        for d in t["depends_on"]:
            if d not in ids:
                errors.append(f"task {t['id']} depends on unknown task '{d}'")
    indeg = {tid: len([d for d in t["depends_on"] if d in ids]) for tid, t in tasks.items()}
    placed = set()
    waves = []
    while len(placed) < len(tasks):
        ready = sorted(tid for tid in tasks if tid not in placed and indeg[tid] == 0)
        if not ready:
            remaining = sorted(set(tasks) - placed)
            errors.append(f"dependency cycle among: {', '.join(remaining)}")
            break
        waves.append(ready)
        for tid in ready:
            placed.add(tid)
        # decrement dependents
        for tid in tasks:
            if tid in placed:
                continue
            indeg[tid] = len([d for d in tasks[tid]["depends_on"] if d in ids and d not in placed])
    return waves, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase")
    ap.add_argument("--plans-dir", default="plans")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    tasks = load_tasks(args.phase, args.plans_dir)
    if not tasks:
        print(f"No plans found for phase {args.phase} in {args.plans_dir}/ "
              f"(expected {args.phase}-<task>-PLAN.md). Run `/dharma3 plan {args.phase}` first.")
        sys.exit(1)

    waves, errors = build_waves(tasks)

    result = {
        "phase": args.phase,
        "wave_count": len(waves),
        "waves": [
            [{"id": tid, "agent": tasks[tid]["agent"], "title": tasks[tid]["title"],
              "depends_on": tasks[tid]["depends_on"]} for tid in wave]
            for wave in waves
        ],
        "errors": errors,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Dharma3 router — phase {args.phase}: {len(tasks)} tasks → {len(waves)} wave(s)\n")
        for i, wave in enumerate(waves, 1):
            par = "parallel" if len(wave) > 1 else "single"
            print(f"  Wave {i} ({par}, {len(wave)} task{'s' if len(wave)>1 else ''}):")
            for tid in wave:
                t = tasks[tid]
                dep = f" ← {', '.join(t['depends_on'])}" if t["depends_on"] else ""
                print(f"    [{t['agent']:<8}] {tid}  {t['title']}{dep}")
            print()
        if errors:
            print("  ⚠ ERRORS (fix before executing):")
            for e in errors:
                print(f"    - {e}")

    # always emit machine plan for the executor (P3), unless graph is broken
    if not errors:
        out = Path(args.plans_dir) / f"{args.phase}-WAVES.json"
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        if not args.json:
            print(f"  ✓ wrote {out}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
