#!/usr/bin/env bash
set -euo pipefail

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"

issue_exists() {
  local t="$1"
  gh issue list --limit 200 --search "$t in:title" --json title -q '.[].title' | grep -Fxq "$t"
}

milestone_number() {
  local title="$1"
  gh api "repos/$REPO/milestones?state=open&per_page=100" | jq -r --arg t "$title" '.[] | select(.title==$t) | .number' | head -n1
}

create_issue() {
  local title="$1"; local body="$2"; local labels="$3"; local ms_title="${4:-}"
  if issue_exists "$title"; then
    echo "Issue exists: $title"
    return 0
  fi

  local ms_num=""
  if [ -n "$ms_title" ]; then
    ms_num="$(milestone_number "$ms_title" || true)"
  fi

  if [ -n "${ms_num:-}" ]; then
    gh issue create --title "$title" --body "$body" --label "$labels" --milestone "$ms_num" >/dev/null
  else
    gh issue create --title "$title" --body "$body" --label "$labels" >/dev/null
  fi
  echo "Created issue: $title"
}

# --- Baseline canon files check
missing=()
req=(
  ".github/AGENT_INIT.md"
  ".github/pull_request_template.md"
  ".github/workflows/ci.yml"
  ".github/workflows/security.yml"
  ".github/workflows/canon-guard.yml"
  "GOVERNANCE.md"
  "SECURITY.md"
  "CONTRIBUTING.md"
  "docs/product/roadmap.md"
  "docs/architecture/overview.md"
  "docs/runbooks/deploy.md"
  "docs/runbooks/dev.md"
)

for f in "${req[@]}"; do [ -f "$f" ] || missing+=("$f"); done

if [ "${#missing[@]}" -gt 0 ]; then
  create_issue \
    "Install missing SOS canon files" \
    "Required canon files are missing:\n\n$(printf -- "- %s\n" "${missing[@]}")\n\n**Acceptance Criteria**\n- All missing files created\n- PR/issue templates reference \`.github/AGENT_INIT.md\`\n- Docs skeleton present\n" \
    "priority:critical,type:chore,scope:docs,stage:hardening,status:ready" \
    "SETUP-0 Bootstrap"
fi

# --- Detect repo posture
eval "$(bash scripts/detect_repo_type.sh)"

# Dependency / CI readiness
if [ "$is_node" -eq 1 ]; then
  create_issue \
    "Ensure Node install/build/test commands are documented and working" \
    "**Acceptance Criteria**\n- \`docs/runbooks/dev.md\` includes install + run steps\n- CI installs deps and runs tests/lint (best-effort)\n" \
    "priority:high,type:chore,scope:ci,stage:mvp,status:ready" \
    "SETUP-1 CI/CD Green"
fi

if [ "$is_python" -eq 1 ]; then
  create_issue \
    "Ensure Python environment and test path are documented and working" \
    "**Acceptance Criteria**\n- \`docs/runbooks/dev.md\` includes venv + install steps\n- CI runs tests (pytest/unittest best-effort)\n" \
    "priority:high,type:chore,scope:ci,stage:mvp,status:ready" \
    "SETUP-1 CI/CD Green"
fi

# Frontend → Vercel
if [ "$is_frontend" -eq 1 ]; then
  create_issue \
    "Configure Vercel deployment (project + env vars)" \
    "Frontend detected. SOS requires Vercel posture.\n\n**Acceptance Criteria**\n- Vercel project connected\n- Preview deploys verified\n- Production env vars configured\n- \`.env.example\` updated\n- \`docs/runbooks/vercel.md\` filled with repo specifics\n" \
    "priority:critical,type:infrastructure,scope:devops,stage:mvp,status:ready" \
    "SETUP-2 Deploy Target Ready"

  create_issue \
    "Connect production domain + SSL (Vercel)" \
    "**Acceptance Criteria**\n- Domain mapped\n- SSL active\n- README Deployment section includes production URL\n" \
    "priority:high,type:chore,scope:devops,stage:launch,status:ready" \
    "SETUP-2 Deploy Target Ready"

  create_issue \
    "Enforce preview/prod env parity checklist" \
    "**Acceptance Criteria**\n- \`docs/runbooks/deploy.md\` has env inventory\n- \`.env.example\` matches inventory\n- Preview + Production configured\n" \
    "priority:high,type:chore,scope:ci,stage:hardening,status:ready" \
    "SETUP-2 Deploy Target Ready"
fi

# Docker posture (only when Dockerfile exists)
if [ "$has_dockerfile" -eq 1 ]; then
  create_issue \
    "Verify Docker build + GHCR publish pipeline" \
    "**Acceptance Criteria**\n- Docker workflow runs on PR\n- main pushes to GHCR with tags \`sha-<sha>\` and \`latest\`\n- \`docs/runbooks/deploy.md\` includes container run instructions\n" \
    "priority:high,type:infrastructure,scope:devops,stage:hardening,status:ready" \
    "SETUP-2 Deploy Target Ready"
fi

# Release pipeline readiness (default build-tag per main)
create_issue \
  "Verify release pipeline produces build-tag releases on main" \
  "**Acceptance Criteria**\n- Push/merge to main creates tag \`build-YYYYMMDD-<shortsha>\`\n- GitHub Release is created with notes\n" \
  "priority:high,type:chore,scope:ci,stage:hardening,status:ready" \
  "SETUP-3 Release Pipeline Ready"

# Telemetry readiness
create_issue \
  "Enable telemetry harvest output for CTO dashboard" \
  "**Acceptance Criteria**\n- \`scripts/harvest_repo.sh\` runs and produces telemetry JSON\n- Output includes commits/issues/releases/workflow health (best-effort)\n" \
  "priority:high,type:chore,scope:devops,stage:hardening,status:ready" \
  "SETUP-4 Telemetry Ready"
