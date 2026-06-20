# PRD — Progression capture: reasoning-session fallback

## Problem
mem_capture's fallback handoff = files-touched + git-diff + last-600-chars. Reasoning-only
sessions (no file writes) capture "no detectable activity" or a trailing question — not the
decisions made. This lost the entire 6-framework comparison on 2026-06-20.

## Success criteria
- A transcript with no `## Handoff` block AND no file changes produces a handoff containing the
  session's topics (from user msgs) + key points (assistant headers/verdicts).
- Existing behavior unchanged when a `## Handoff` block or file changes ARE present.

## Non-goals (deferred)
- Auto-seed `.agent/` for new dirs (changes attribution; needs human decision).
- Concurrency (CURRENT.md overwrite) redesign. LLM synthesis. Mid-session checkpoints.

## Tasks
- 1-1 (build) add `_summarize_transcript` + wire into `extract_handoff` fallback
- 1-2 (qa)    verify on a reasoning-only transcript fixture; confirm no regression
