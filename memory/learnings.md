# Learnings — system evolution log

Every bug/rework converted into a permanent upgrade.

- **2026-06-20** — Progression captured reasoning-only sessions as 'no detectable activity' — lost the 6-framework comparison
  → upgrade (code): added _summarize_transcript fallback (topics + decisions) to mem_capture.extract_handoff

- **2026-06-20** — Progression: concurrent same-day sessions clobbered one shared digest file
  → upgrade (code): per-session digest naming via session_id in mem_capture.main

- **2026-06-20** — Progression: work in a sub-repo bled into the parent's .agent (lost Dharma3 into Product Dev)
  → upgrade (code): resolve_root() — a git-root/marked dir gets its own .agent; bare subdirs still share ancestor

- **2026-06-20** — Progression: project resolution relied on possibly-empty CLAUDE_PROJECT_DIR; HOME guard compared unresolved path
  → upgrade (code): unified start via hook cwd + HOME.resolve() in guards (mem_capture)

- **2026-06-20** — Progression: deep synthesis (decisions) required a manual mem_synthesize run
  → upgrade (code): deterministic _extract_decisions → CANDIDATE entries in .agent/DECISIONS.md on capture (promotion stays human-gated, O6)

- **2026-06-20** — Progression: long live sessions were a blind spot until SessionEnd/PreCompact
  → upgrade (code): added --checkpoint mode + throttled Stop hook → mid-session capture (updates CURRENT+digest, skips daily)
