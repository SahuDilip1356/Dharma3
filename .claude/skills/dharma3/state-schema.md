# STATE.md contract

`memory/STATE.md` is the **single source of truth** shared across every operating agent and every
session. It is read on session start (auto-injected) and updated at the end of each phase/task.

## Required sections

```markdown
# STATE — <project name>

_Last updated: <ISO datetime> · <what updated it>_

## Now
- Active phase: <N — name>
- Active wave: <id or "—">
- Next action: <single concrete next step>

## Roadmap
| Phase | Goal | Status |
|---|---|---|
| 1 | ... | done / in-progress / blocked / todo |

## Dependency graph (current phase)
| Task | Depends on | Wave | Status | Evidence |
|---|---|---|---|---|
| 1-1 | — | W1 | done | <link/proof> |
| 1-2 | 1-1 | W2 | todo | — |

## Decisions (durable)
- <decision> — <why> — <date>

## Open loops
| Opened | Loop | Next action |
|---|---|---|
```

## Rules
- One STATE.md per project root (`memory/STATE.md`).
- Every executor **reads before** and **writes after** its task — this is how parallel agents stay coherent.
- `Next action` is always exactly one concrete step, so any fresh session can resume cold.
- Never store secrets here.
