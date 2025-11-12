#!/usr/bin/env bash
# Agent-1 smoke (Linux/WSL). LF endings required.
# Robust Docker detection for WSL integration.

# Try to enable pipefail; if unavailable, continue without it.
(set -Eeuo pipefail) 2>/dev/null || set -Eeuo

IFS=$'\n\t'
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
REPORT="$ROOT/docs/test-reports/smoke"
mkdir -p "$REPORT"
LOG="$REPORT/agent1-linux.log"

{
  echo "== Agent-1 Smoke (Linux) =="
  date -u +"UTC: %Y-%m-%dT%H:%M:%SZ"
  echo "ROOT=$ROOT"
  echo

  # Local FS write/delete
  TMP="$ROOT/.tmp.smoke.$$"
  if echo ok > "$TMP" && rm -f "$TMP"; then
    echo "PASS: local fs write"
  else
    echo "FAIL: local fs write"
  fi

  # Python
  if command -v python3 >/dev/null 2>&1; then
    printf 'python: '; python3 --version
  elif command -v python >/dev/null 2>&1; then
    printf 'python: '; python --version
  else
    echo "WARN: python not present"
  fi

  # Git
  if command -v git >/dev/null 2>&1; then
    printf 'git: '; git --version
  else
    echo "WARN: git not present"
  fi

  # Docker (WSL integration friendly)
  if command -v docker >/dev/null 2>&1; then
    if docker --version >/dev/null 2>&1; then
      printf 'docker: '; docker --version
      echo "PASS: docker usable"
    else
      echo "WARN: docker on PATH but not usable (enable Docker Desktop WSL integration for this distro)"
    fi
  else
    echo "WARN: docker not present"
  fi

  echo
  echo "SMOKE DONE"
} > "$LOG" 2>&1

# Print the path so callers/CI can easily cat it
echo "$LOG"
exit 0
