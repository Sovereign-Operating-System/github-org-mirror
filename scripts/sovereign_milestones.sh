#!/usr/bin/env bash
set -euo pipefail

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"

want=(
  "SETUP-0 Bootstrap"
  "SETUP-1 CI/CD Green"
  "SETUP-2 Deploy Target Ready"
  "SETUP-3 Release Pipeline Ready"
  "SETUP-4 Telemetry Ready"
)

existing="$(gh api "repos/$REPO/milestones?state=all&per_page=100" | jq -r '.[].title')"

for title in "${want[@]}"; do
  if echo "$existing" | grep -Fxq "$title"; then
    echo "Milestone exists: $title"
  else
    gh api -X POST "repos/$REPO/milestones" -f title="$title" -f state="open" >/dev/null || true
    echo "Created milestone: $title"
  fi
done
