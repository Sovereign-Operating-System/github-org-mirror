#!/usr/bin/env bash
set -euo pipefail

PROJECT="Commercial Readiness"
OWNER="$(gh repo view --json owner -q .owner.login)"

ensure_project() {
  # gh project list output varies; use best-effort JSON
  if gh project list --owner "$OWNER" --limit 200 --format json >/dev/null 2>&1; then
    local exists
    exists="$(gh project list --owner "$OWNER" --limit 200 --format json | jq -r '.projects[]?.title' | grep -Fx "$PROJECT" || true)"
    if [ -n "$exists" ]; then
      echo "Project exists: $PROJECT"
      return 0
    fi
  fi

  if gh project create --owner "$OWNER" --title "$PROJECT" >/dev/null 2>&1; then
    echo "Created project: $PROJECT"
    return 0
  fi

  echo "WARN: Could not create project (permissions/policy)."
  return 1
}

if ! ensure_project; then
  # Record blockage as issue
  if ! gh issue list --limit 200 --search "Project creation blocked in:title" --json title -q '.[].title' | grep -Fxq "Project creation blocked"; then
    gh issue create \
      --title "Project creation blocked" \
      --body "SOS attempted to create GitHub Project **$PROJECT** but was blocked by permissions or org policy.\n\n**Action**: grant permission or create project manually and re-run installer." \
      --label "priority:high,type:chore,scope:devops,status:blocked" >/dev/null || true
  fi
  exit 0
fi

echo "Project ensured (population is optional; issue lists already drive work)."
