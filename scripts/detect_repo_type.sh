#!/usr/bin/env bash
set -euo pipefail

# Outputs lines like:
#   is_node=1
#   is_python=0
#   is_frontend=1
#   has_dockerfile=0

is_node=0
is_python=0
is_frontend=0
has_dockerfile=0

[ -f package.json ] && is_node=1
([ -f requirements.txt ] || [ -f pyproject.toml ]) && is_python=1 || true

# Frontend heuristics
if [ -f package.json ]; then
  grep -q '"next"' package.json && is_frontend=1 || true
  grep -q '"vite"' package.json && is_frontend=1 || true
  grep -q '"react-scripts"' package.json && is_frontend=1 || true
fi
([ -d apps/web ] || [ -d apps/frontend ] || [ -d frontend ] || [ -d web ]) && is_frontend=1 || true

# Dockerfile
([ -f Dockerfile ] || [ -f docker/Dockerfile ]) && has_dockerfile=1 || true

cat <<EOF
is_node=$is_node
is_python=$is_python
is_frontend=$is_frontend
has_dockerfile=$has_dockerfile
EOF
