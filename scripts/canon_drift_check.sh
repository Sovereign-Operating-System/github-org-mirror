#!/usr/bin/env bash
set -euo pipefail

required=(
  "canon/"            # optional in target repos; allow absence
  ".github/AGENT_INIT.md"
  ".github/pull_request_template.md"
  ".github/workflows/canon-guard.yml"
  "GOVERNANCE.md"
  "SECURITY.md"
  "docs/product/roadmap.md"
)

missing=0
for f in "${required[@]}"; do
  if [[ "$f" == "canon/" ]]; then
    continue
  fi
  if [ ! -f "$f" ]; then
    echo "Missing required: $f"
    missing=1
  fi
done

if [ "$missing" -ne 0 ]; then
  echo "Canon drift guard failed."
  exit 1
fi

# Heuristic: core change requires docs touch
changed="$(git diff --name-only origin/main...HEAD 2>/dev/null || git diff --name-only HEAD~1...HEAD || true)"
core="$(echo "$changed" | grep -Ei '^(src/|apps/|packages/|supabase/|api/|backend/|frontend/|web/)' || true)"
docs="$(echo "$changed" | grep -Ei '^(docs/|README.md|DECISIONS.md|CHANGELOG.md)' || true)"

if [ -n "$core" ] && [ -z "$docs" ]; then
  echo "Core code changed but docs/README/decisions/changelog not updated."
  exit 1
fi

echo "Canon guard passed."
