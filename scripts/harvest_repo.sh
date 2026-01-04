#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then echo "gh missing"; exit 1; fi
if ! command -v jq >/dev/null 2>&1; then echo "jq missing"; exit 1; fi

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
OUT="${1:-telemetry.json}"

now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Issues by priority
issues_json="$(gh issue list --state open --limit 200 --json number,title,labels,createdAt,url 2>/dev/null || echo "[]")"
issues_by_priority="$(echo "$issues_json" | jq -r '
  def hasLabel(lbl): any(.labels[]?; .name==lbl);
  {
    critical: (map(select(hasLabel("priority:critical")) ) | length),
    high:     (map(select(hasLabel("priority:high")) ) | length),
    medium:   (map(select(hasLabel("priority:medium")) ) | length),
    low:      (map(select(hasLabel("priority:low")) ) | length),
    total: length
  }')"

# Releases (last 10)
releases_json="$(gh release list --limit 10 --json tagName,name,createdAt,url 2>/dev/null || echo "[]")"

# Commits (local repo)
commit_count_30="$(git rev-list --count --since="30 days ago" HEAD 2>/dev/null || echo 0)"
commit_count_7="$(git rev-list --count --since="7 days ago" HEAD 2>/dev/null || echo 0)"
last_commit="$(git log -1 --pretty=format:'%cI' 2>/dev/null || echo "")"

# Workflow health (best-effort)
runs="$(gh run list --limit 20 --json status,conclusion,createdAt,name 2>/dev/null || echo "[]")"
workflow_health="$(echo "$runs" | jq -r '
  {
    total: length,
    success: (map(select(.conclusion=="success"))|length),
    failure: (map(select(.conclusion=="failure"))|length),
    cancelled: (map(select(.conclusion=="cancelled"))|length)
  }')"

jq -n \
  --arg repo "$REPO" \
  --arg generated_at "$now" \
  --argjson issues_by_priority "$issues_by_priority" \
  --argjson releases "$releases_json" \
  --argjson workflow_health "$workflow_health" \
  --arg commit_count_7 "$commit_count_7" \
  --arg commit_count_30 "$commit_count_30" \
  --arg last_commit "$last_commit" \
  '{
    repo: $repo,
    generated_at: $generated_at,
    commits: {
      last_7_days: ($commit_count_7|tonumber),
      last_30_days: ($commit_count_30|tonumber),
      last_commit_at: $last_commit
    },
    issues_open: $issues_by_priority,
    releases: $releases,
    workflows: $workflow_health
  }' > "$OUT"

echo "Wrote $OUT"
