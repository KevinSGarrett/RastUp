#!/usr/bin/env bash
# LF endings required.
(set -Eeuo pipefail) 2>/dev/null || set -Eeuo

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
REPORT="$ROOT/docs/test-reports/smoke"
mkdir -p "$REPORT"
LOG="$REPORT/agent1-linux.log"

{
  echo "== Agent-1 Smoke (Linux) =="
  date -u +"UTC: %Y-%m-%dT%H:%M:%SZ"
  echo "ROOT=$ROOT"
  echo

  TMP="$ROOT/.tmp.smoke.$$"
  if echo ok > "$TMP" && rm -f "$TMP"; then
    echo "PASS: local fs write"
  else
    echo "FAIL: local fs write"
  fi

  if command -v python3 >/dev/null 2>&1; then
    printf 'python: '; python3 --version
  elif command -v python >/dev/null 2>&1; then
    printf 'python: '; python --version
  else
    echo "WARN: python not present"
  fi

  if command -v git >/dev/null 2>&1; then
    printf 'git: '; git --version
  else
    echo "WARN: git not present"
  fi

  if command -v docker >/dev/null 2>&1; then
    if docker version >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
      printf 'docker: '; docker --version
      echo "PASS: docker usable"
    else
      echo "WARN: docker CLI found but engine not reachable (enable Docker Desktop WSL integration)"
    fi
  else
    echo "WARN: docker not present"
  fi

  echo
  echo "SMOKE DONE"
} > "$LOG" 2>&1

echo "$LOG"
exit 0
