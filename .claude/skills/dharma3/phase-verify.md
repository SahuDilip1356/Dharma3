# Phase: VERIFY  (owner: D1 + GS + SP)

Covers `/dharma3 verify <phase>`. Verification means one thing: **prove it is actually done and working.**

## The harness (run in order; a failure loops back to EXECUTE)

1. **Evidence gate (D1).** Run `python3 scripts/evidence.py <phase>` — it scans STATE.md and
   **fails (exit 1) if any task marked `done` has empty or banned-phrase evidence** ("should work",
   "probably passes", "looks good"). Fix the evidence (or downgrade status) until it passes.
   Valid evidence = build-passes / tests-pass / lint+typecheck / screenshot / browser flow / manual
   steps. *(The `evidence_ledger_commit_msg.sh` git hook enforces the same at commit time.)*
2. **Self-verification / real-use (GS).** Ask: *how would a real user verify this?* Dispatch the
   **qa operating agent** (`agents/qa.md`) to run the real flow — for UI, spin up the app and check
   the actual flow with screenshots (the agent reads its own render); for automations, run a real
   input end-to-end. Its report is the browser/real-use evidence recorded in STATE.md.
3. **2-stage review (SP + GS + D1).**
   - Stage 1 — **spec compliance**: does it do what the PLAN/PRD specified?
   - Stage 2 — **code quality**: a separate adversarial pass ("be mean") that tries to break it;
     optionally a cross-model (codex) review.
4. **Diagnose-and-fix before close (SP systematic-debugging).** For any failure, find root cause,
   fix, then **re-test** (the fix may not have solved it). Do not skip the re-test.

## Predict edge cases
Before declaring the phase verified, ask **"how could this go wrong?"** and test the nastiest input
(e.g. a malformed webhook, empty state, concurrency). Feed failures back into the harness.

## Exit evidence
- Each task has attached proof in STATE.md; review stages passed; edge cases tested; no open defects.
- Recommend `/dharma3 ship <phase>`.
