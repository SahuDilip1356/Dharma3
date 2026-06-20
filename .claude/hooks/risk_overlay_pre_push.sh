#!/usr/bin/env bash
# Dharma3 — Risk Overlay (pre-push gate). Ported from Dharma 1.
# Blocks a push if the diff touches high-risk paths and required gate receipts are missing.
# Install as a git pre-push hook:  ln -sf ../../.claude/hooks/risk_overlay_pre_push.sh .git/hooks/pre-push
set -euo pipefail

REMOTE="${1:-origin}"
BASE_BRANCH="$(git symbolic-ref "refs/remotes/${REMOTE}/HEAD" 2>/dev/null | sed "s@^refs/remotes/${REMOTE}/@@" || echo "main")"
MERGE_BASE="$(git merge-base HEAD "${REMOTE}/${BASE_BRANCH}" 2>/dev/null || git rev-parse HEAD~1 2>/dev/null || echo "")"
[[ -z "${MERGE_BASE}" ]] && exit 0
CHANGED="$(git diff --name-only "${MERGE_BASE}"...HEAD || true)"
[[ -z "${CHANGED}" ]] && exit 0

# High-risk paths — touching these requires verification receipts.
RISK_REGEX='(^|/)(auth|payments|billing|migrations|prompts|llm|agents|permissions)(/|$)|\.sql$|\.policy\.'
RISKY="$(echo "${CHANGED}" | grep -E "${RISK_REGEX}" || true)"
[[ -z "${RISKY}" ]] && { echo "risk-overlay: no high-risk paths. proceeding."; exit 0; }

echo ""
echo "⚠ risk-overlay: high-risk paths detected:"
echo "${RISKY}" | sed 's/^/  - /'
echo ""
echo "Required verification receipts in memory/ (this branch, last 24h):"
MISSING=0
for gate in qa cso review; do
  RECEIPT="$(find memory -maxdepth 3 -name "${gate}*.md" -mtime -1 2>/dev/null | head -1 || true)"
  if [[ -z "${RECEIPT}" ]]; then echo "  ✗ ${gate} — missing"; MISSING=1; else echo "  ✓ ${gate} — ${RECEIPT}"; fi
done
if [[ "${MISSING}" -eq 1 ]]; then
  echo ""
  echo "Push BLOCKED. Run /dharma3 verify <phase> to produce receipts, or override with --no-verify."
  exit 1
fi
echo "risk-overlay: receipts present. proceeding."
exit 0
