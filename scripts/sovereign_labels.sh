#!/usr/bin/env bash
set -euo pipefail

labels=(
  "priority:critical|d73a4a"
  "priority:high|ff8c00"
  "priority:medium|fbca04"
  "priority:low|0e8a16"

  "type:bug|d73a4a"
  "type:feature|1d76db"
  "type:enhancement|84b6eb"
  "type:chore|c5def5"
  "type:documentation|5319e7"
  "type:security|b60205"
  "type:infrastructure|0052cc"

  "scope:frontend|1d76db"
  "scope:backend|0e8a16"
  "scope:database|006b75"
  "scope:auth|8a2be2"
  "scope:devops|0052cc"
  "scope:ci|0052cc"
  "scope:api|1d76db"
  "scope:ui|fbca04"
  "scope:docs|5319e7"

  "stage:mvp|c2e0c6"
  "stage:post-mvp|bfdadc"
  "stage:hardening|f9d0c4"
  "stage:launch|0e8a16"
  "stage:scaling|d4c5f9"

  "status:blocked|e11d21"
  "status:ready|0e8a16"
  "status:in-progress|fbca04"
  "status:review|1d76db"
)

exists() { gh label list --limit 500 --json name -q '.[].name' | grep -Fxq "$1"; }

for entry in "${labels[@]}"; do
  IFS="|" read -r name color <<< "$entry"
  if exists "$name"; then
    gh label edit "$name" --color "$color" >/dev/null || true
  else
    gh label create "$name" --color "$color" --description "SOS canon label" >/dev/null || true
  fi
done

echo "Labels ensured."
