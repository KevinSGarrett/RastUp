#!/usr/bin/env bash
# Agent-1 smoke (Linux/WSL). Works on older bash and BusyBox; tolerant to CRLF conversions.
# NOTE: Keep this file with LF line endings. In Git, use .gitattributes (see repo root).

# Try to enable pipefail; if unsupported, continue without it.
(set -Eeuo pipefail) 2>/dev/null || set -Eeuo

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
REPORT="$ROOT/docs/test-reports/smoke"
mkdir -p "$REPORT"
LOG="$REPORT/agent1-linux.log"

{
  echo "== Agent-1 Smoke (Linux) =="
  printf 'UTC: %s\n' "$(date -u +%FT%TZ)"
  printf 'ROOT=%s\n\n' "$ROOT"

  TMP="$ROOT/tmp.smoke.$$"
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
    printf 'PASS: docker present - '; docker --version
  else
    echo "WARN: docker not present"
  fi

  echo ""
  echo "SMOKE DONE"
} > "$LOG" 2>&1

echo "$LOG"
exit 0
