#!/usr/bin/env bash
set -euo pipefail

# Sovereign Canon Installer (runs INSIDE a target repo)
# Requires: gh auth, jq
#
# Usage:
#   bash pack/scripts/sovereign_install.sh --from /path/to/SOS/pack
#   (Typically invoked by SOS ops/bootstrap scripts)

FROM=""
NO_ISSUES=0
NO_PROJECT=0
NO_MILESTONES=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from) FROM="$2"; shift 2 ;;
    --no-issues) NO_ISSUES=1; shift ;;
    --no-project) NO_PROJECT=1; shift ;;
    --no-milestones) NO_MILESTONES=1; shift ;;
    *) shift ;;
  esac
done

if [ -z "$FROM" ]; then
  echo "ERROR: --from /path/to/SOS/pack is required"
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then echo "ERROR: gh missing"; exit 1; fi
if ! command -v jq >/dev/null 2>&1; then echo "ERROR: jq missing"; exit 1; fi
gh auth status >/dev/null 2>&1 || { echo "ERROR: gh not authenticated"; exit 1; }

ROOT="$(pwd)"
TMP="$(mktemp -d)"
cleanup(){ rm -rf "$TMP"; }
trap cleanup EXIT

echo "==> Installing SOS pack into: $ROOT"

# Copy pack-root files
rsync -a --exclude ".DS_Store" "$FROM/root/" "$ROOT/"

# Copy .github pack
mkdir -p "$ROOT/.github"
rsync -a --exclude ".DS_Store" "$FROM/github/.github/" "$ROOT/.github/"

# Copy scripts pack into repo scripts/
mkdir -p "$ROOT/scripts"
rsync -a --exclude ".DS_Store" "$FROM/scripts/" "$ROOT/scripts/"

# Ensure executable bits
chmod +x "$ROOT/scripts/"*.sh || true

# README marker (append if missing)
if [ -f README.md ]; then
  if ! grep -q "Sovereign Canon Compliance" README.md; then
    cat "$FROM/root/README_SNIPPET.md" >> README.md
  fi
else
  cat > README.md <<EOF
# $(basename "$ROOT")
$(cat "$FROM/root/README_SNIPPET.md")
EOF
fi

echo "==> Best-effort enable repo features (issues/projects/wiki) if permitted"
REPO_FULL="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
# Enable Issues + Projects (Wiki may be org-restricted)
gh api -X PATCH "repos/$REPO_FULL" -f has_issues=true -f has_projects=true >/dev/null 2>&1 || true
gh api -X PATCH "repos/$REPO_FULL" -f has_wiki=true >/dev/null 2>&1 || true

echo "==> Labels"
bash scripts/sovereign_labels.sh

if [ "$NO_MILESTONES" -eq 0 ]; then
  echo "==> Milestones"
  bash scripts/sovereign_milestones.sh
fi

if [ "$NO_ISSUES" -eq 0 ]; then
  echo "==> Issue seeding"
  bash scripts/sovereign_issue_seeder.sh || true
fi

if [ "$NO_PROJECT" -eq 0 ]; then
  echo "==> Project (Commercial Readiness)"
  bash scripts/sovereign_project.sh || true
fi

echo "==> Complete."
