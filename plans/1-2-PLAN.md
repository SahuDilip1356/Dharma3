---
task: 1-2
depends_on: [1-1]
agent: qa
title: Verify reasoning-only capture + no regression
---
Steps:
1. Build a JSONL fixture: user asks a comparison question, assistant replies with headers/verdicts, NO file edits.
2. Run extract_handoff on it → assert summary contains topics + key points, not "no detectable activity".
3. Regression: a transcript WITH a `## Handoff` block still returns that block verbatim.
