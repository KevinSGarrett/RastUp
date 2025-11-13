#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
PY_DIRS=("orchestrator" "ProjectBlueprint/scripts/concordance")

info() { printf "\n==> %s\n" "$*"; }
run_if_exists() { if command -v "$1" >/dev/null 2>&1; then shift; "$@"; else echo "[skip] $1 not installed"; fi }

cd "$ROOT_DIR"

info "Ruff"
run_if_exists ruff ruff check "${PY_DIRS[@]}" || true

info "Black (check)"
run_if_exists black black --check "${PY_DIRS[@]}" || true

info "Mypy"
run_if_exists mypy mypy "${PY_DIRS[@]}" || true

info "Bandit (informational)"
run_if_exists bandit bandit -q -r orchestrator || true

info "Yamllint"
if [ -d ops ] || [ -d infra ]; then
  run_if_exists yamllint yamllint -s ops infra || true
else
  echo "[skip] no ops/ or infra/ directory"
fi

info "Simple secret scan (high-signal)"
patterns=(
  'AKIA[0-9A-Z]{16}'
  'ghp_[0-9A-Za-z]{36}'
  'xox[baprs]-[0-9A-Za-z-]{10,}'
  'AIza[0-9A-Za-z\-_]{35}'
  '-----BEGIN (RSA|EC|DSA|OPENSSH|PGP) PRIVATE KEY-----'
)

if command -v rg >/dev/null 2>&1; then
  for pat in "${patterns[@]}"; do
    echo "-- pattern: $pat"
    rg -n --hidden --no-messages -g '!**/.git/**' -g '!**/node_modules/**' -g '!**/*.zip' -g '!**/*.docx' -g '!**/*.odt' "$pat" || true
  done
else
  echo "[skip] ripgrep (rg) not installed"
fi

info "Done"
