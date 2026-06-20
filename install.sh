#!/usr/bin/env bash
# Dharma3 installer — wires the framework into a target project (or this one).
# Usage:  ./install.sh [TARGET_DIR]   (default: current directory)
# Zero runtime deps beyond python3 + git. Idempotent.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$PWD}"

echo "Dharma3 → installing into: $TARGET"

# 1. Skills + hooks + scripts + ai_runners + settings
mkdir -p "$TARGET/.claude/skills" "$TARGET/.claude/hooks" "$TARGET/memory/sessions" "$TARGET/plans" "$TARGET/templates" "$TARGET/scripts"
cp -R "$SRC/.claude/skills/dharma3" "$TARGET/.claude/skills/"
cp -R "$SRC/ai_runners" "$TARGET/"
cp "$SRC/.claude/hooks/"*.py "$TARGET/.claude/hooks/"
cp "$SRC/.claude/hooks/"*.sh "$TARGET/.claude/hooks/" 2>/dev/null || true
cp "$SRC/scripts/"*.py "$TARGET/scripts/"
chmod +x "$TARGET/.claude/hooks/"* "$TARGET/scripts/"*.py
cp "$SRC/templates/PRD_TEMPLATE.md" "$TARGET/templates/" 2>/dev/null || true

# 2. settings.json — create if absent (do not clobber an existing one)
if [ ! -f "$TARGET/.claude/settings.json" ]; then
  cp "$SRC/.claude/settings.json" "$TARGET/.claude/settings.json"
  echo "  ✓ wrote .claude/settings.json (hooks: SessionStart/SessionEnd/PreToolUse)"
else
  echo "  ! .claude/settings.json exists — merge the \"hooks\" block manually (see $SRC/.claude/settings.json)"
fi

# 3. STATE.md — seed if absent
if [ ! -f "$TARGET/memory/STATE.md" ]; then
  cat > "$TARGET/memory/STATE.md" <<'EOF'
# STATE — <project>

_Last updated: (new) · install_

## Now
- Active phase: —
- Active wave: —
- Next action: Run `/dharma3 new "<intent>"`

## Roadmap
| Phase | Goal | Status |
|---|---|---|

## Dependency graph (current phase)
| Task | Depends on | Wave | Status | Evidence |
|---|---|---|---|---|

## Decisions (durable)

## Open loops
| Opened | Loop | Next action |
|---|---|---|
EOF
  echo "  ✓ seeded memory/STATE.md"
fi

# 3b. Activate git hooks (evidence-ledger on commit, risk-overlay on push) if target is a git repo
if [ -d "$TARGET/.git" ]; then
  ln -sf "../../.claude/hooks/evidence_ledger_commit_msg.sh" "$TARGET/.git/hooks/commit-msg" 2>/dev/null \
    && echo "  ✓ git commit-msg hook → evidence-ledger (rejects \"should work\")" || true
  ln -sf "../../.claude/hooks/risk_overlay_pre_push.sh" "$TARGET/.git/hooks/pre-push" 2>/dev/null \
    && echo "  ✓ git pre-push hook → risk-overlay" || true
else
  echo "  ! $TARGET is not a git repo — skipped git hooks (run 'git init' then re-run to enable evidence/risk gates)"
fi

# 4. Verify hooks + router + governance run
echo '{}' | python3 "$TARGET/.claude/hooks/pre_tool_use_security.py" >/dev/null && echo "  ✓ security hook OK"
python3 "$TARGET/scripts/wave_planner.py" 0 >/dev/null 2>&1 || true; echo "  ✓ router installed (scripts/wave_planner.py)"
( cd "$TARGET" && python3 scripts/govern.py pricing >/dev/null 2>&1 ) && echo "  ✓ governance runners installed (ai_runners + scripts/govern.py)"
python3 "$TARGET/scripts/evidence.py" 0 --state "$TARGET/memory/STATE.md" >/dev/null 2>&1 || true; echo "  ✓ evidence gate installed (scripts/evidence.py)"
( cd "$TARGET" && python3 scripts/ship_gate.py 0 >/dev/null 2>&1 ) || true; echo "  ✓ ship gate installed (scripts/ship_gate.py + evolve.py)"
echo "Done. Restart Claude Code in $TARGET so hooks load, then run:  /dharma3 help"
