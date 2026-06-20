# Dharma3

> **Direct many agents · Ship with evidence · Remember everything.**

A multi-agent product-development framework: a lean **orchestrator** that plans work, dispatches
**operating agents** in dependency-ordered parallel waves, gates every action, verifies with
evidence, and persists everything to a **memory backbone** that survives sessions.

Assembled by scoring six frameworks component-by-component (see [`DHARMA3_COMPARISON.md`](DHARMA3_COMPARISON.md))
and grafting each layer's winner (see [`DHARMA3_BUILD_PLAN.md`](DHARMA3_BUILD_PLAN.md)).

**Lineage:** Dharma 0.x (governance + design) → Dharma 1 (discipline as machinery) → **Dharma3** (multi-agent).

## Install

```bash
./install.sh              # into this project
./install.sh /path/to/app # into another project
# then restart Claude Code so the hooks load
```

## Invoke

```text
/dharma3 new "<intent>"   Plan: forcing questions → PRD → roadmap
/dharma3 plan <phase>     Atomic, context-fit task plans + dependency graph
/dharma3 execute <phase>  Implement (single-agent now; parallel waves at P3)
/dharma3 verify <phase>   Evidence + real-use check + 2-stage review
/dharma3 ship <phase>     Phase-gates + SME + PR with rollback
/dharma3 status           Read STATE.md, show progress
/dharma3 help             Menu
```

## Automatic (machinery, never invoked)
- **Memory** — `SessionStart` loads `memory/STATE.md`; `SessionEnd` writes a session digest.
- **Security** — `PreToolUse` blocks destructive / secret-touching actions before they run.

## Status
P0 (memory + security hooks) and P1 (orchestrator + phase playbooks) are built. P2–P7
(router, parallel waves, governance runners, verification harness, specialist agents, ship gates)
are specced in the build plan and tracked in `memory/STATE.md`.
