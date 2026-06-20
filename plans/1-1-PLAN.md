---
task: 1-1
depends_on: []
agent: build
title: Add transcript-summary fallback to mem_capture.extract_handoff
---
Steps:
1. Add `_summarize_transcript(transcript_path, max_topics, max_points)` to mem_capture.py:
   - user topics: first line (≤90 chars) of each user message, last N, deduped
   - key points: assistant lines matching `^#{2,4}\s+` or `**…**` verdict/decision/recommend lines
2. In `extract_handoff` fallback, add a "**Session summary:**" part from it, BEFORE the tail.
3. Ensure it never returns "no detectable activity" when the transcript has any messages.
Verify: import-clean; runs on a fixture.
