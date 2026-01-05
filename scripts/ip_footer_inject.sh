#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# IP Footer Injector — Tier-0++
# Modes:
#   - Default (fix): injects footer where missing
#   - --check: fails if any in-scope file is missing the footer
# Scope:
#   - Default paths: src apps packages supabase
#   - Override with: --paths "src apps packages supabase"
# Guarantees:
#   - Idempotent: never duplicates the footer (marker line)
#   - Comment-style aware per language
# ============================================================

MARKER="Use governed by IP_CANON.md. All rights reserved."

FOOTER_LINES=(
  "© Jonathan Mitchell Anderson — Confidential & Proprietary"
  "Use governed by IP_CANON.md. All rights reserved."
)

MODE="fix"
SCOPE_PATHS=("src" "apps" "packages" "supabase")

usage() {
  cat <<'EOF'
Usage:
  scripts/ip_footer_inject.sh [--check] [--paths "src apps packages supabase"]

  --check   Validate only. Exit 1 if any in-scope file lacks the footer.
  --paths   Space-separated root folders to scan (default: src apps packages supabase).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)
      MODE="check"; shift ;;
    --paths)
      shift
      [[ $# -gt 0 ]] || { echo "❌ --paths requires a value" >&2; exit 2; }
      # shellcheck disable=SC2206
      SCOPE_PATHS=($1)
      shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "❌ Unknown arg: $1" >&2
      usage
      exit 2 ;;
  esac
done

# Directories to skip (even if inside scope)
SKIP_GLOBS=(
  "*/.git/*"
  "*/node_modules/*"
  "*/dist/*"
  "*/build/*"
  "*/out/*"
  "*/.next/*"
  "*/.vercel/*"
  "*/vendor/*"
)

should_skip() {
  local f="$1"
  for g in "${SKIP_GLOBS[@]}"; do
    if [[ "$f" == $g ]]; then
      return 0
    fi
  done
  return 1
}

has_footer() {
  local f="$1"
  grep -Fq "$MARKER" "$f" 2>/dev/null
}

append_footer_block() {
  local f="$1"
  local style="$2"  # cblock | hash | html

  {
    echo ""
    case "$style" in
      cblock)
        echo "/*"
        printf '%s\n' "${FOOTER_LINES[@]}"
        echo "*/"
        ;;
      hash)
        for line in "${FOOTER_LINES[@]}"; do
          echo "# $line"
        done
        ;;
      html)
        echo "<!--"
        printf '%s\n' "${FOOTER_LINES[@]}"
        echo "-->"
        ;;
      *)
        for line in "${FOOTER_LINES[@]}"; do
          echo "# $line"
        done
        ;;
    esac
  } >> "$f"
}

inject_or_check_one() {
  local f="$1"
  local ext="${f##*.}"

  [[ -f "$f" ]] || return 0

  # Skip large files (>2MB)
  local size
  size=$(wc -c < "$f" | tr -d ' ')
  if [[ "$size" -gt 2000000 ]]; then
    return 0
  fi

  if has_footer "$f"; then
    return 0
  fi

  if [[ "$MODE" == "check" ]]; then
    echo "$f"
    return 0
  fi

  case "$ext" in
    js|ts|tsx|go|java)
      append_footer_block "$f" "cblock" ;;
    py|yml|yaml)
      append_footer_block "$f" "hash" ;;
    md)
      append_footer_block "$f" "html" ;;
    sql)
      {
        echo ""
        for line in "${FOOTER_LINES[@]}"; do
          echo "-- $line"
        done
      } >> "$f" ;;
    *)
      return 0 ;;
  esac
}

missing=()

# Build file list within scope roots
for root in "${SCOPE_PATHS[@]}"; do
  [[ -d "$root" ]] || continue
  while IFS= read -r -d '' file; do
    if should_skip "$file"; then
      continue
    fi
    out=$(inject_or_check_one "$file" || true)
    if [[ -n "$out" && "$MODE" == "check" ]]; then
      missing+=("$out")
    fi
  done < <(
    find "$root" -type f \( \
      -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o \
      -name "*.go" -o -name "*.java" -o \
      -name "*.py" -o -name "*.yml" -o -name "*.yaml" -o \
      -name "*.md" -o -name "*.sql" \
    \) -print0
  )
done

if [[ "$MODE" == "check" ]]; then
  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "❌ Missing IP footer in the following in-scope files:" >&2
    printf ' - %s\n' "${missing[@]}" >&2
    exit 1
  fi
  echo "✅ IP footer present in all in-scope files."
fi
