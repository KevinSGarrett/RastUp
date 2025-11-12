#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
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
  if echo ok >"$TMP" && rm -f "$TMP"; then
    echo "PASS: local fs write"
  else
    echo "FAIL: local fs write"
  fi

  # Python
  if command -v python3 >/dev/null 2>&1; then
    echo -n "python: "
    python3 --version
  else
    echo "WARN: python3 not present"
  fi

  # Git
  if command -v git >/dev/null 2>&1; then
    echo -n "git: "
    git --version
  else
    echo "WARN: git not present"
  fi

  # Docker
  if command -v docker >/dev/null 2>&1; then
    echo -n "docker: "
    docker --version
    echo "PASS: docker present"
  else
    echo "WARN: docker not present"
  fi

  echo
  echo "SMOKE DONE"
} >"$LOG" 2>&1

# As a convention, print the absolute log path for callers
echo "$LOG"
