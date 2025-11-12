#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPORT="$ROOT/docs/test-reports/smoke"
mkdir -p "$REPORT"
LOG="$REPORT/agent1-linux.log"

echo "== Agent-1 Smoke (Linux) ==" > "$LOG"
TMP="$ROOT/tmp.smoke.txt"
( echo ok > "$TMP" && rm -f "$TMP" ) \
  && echo "PASS: local fs write" >> "$LOG" \
  || echo "FAIL: local fs write" >> "$LOG"

if command -v docker >/dev/null 2>&1; then
  docker --version >> "$LOG" 2>&1 || true
  if docker info >/dev/null 2>&1; then
    echo "PASS: docker available" >> "$LOG"
  else
    echo "WARN: docker present but daemon not reachable" >> "$LOG"
  fi
else
  echo "WARN: docker not present" >> "$LOG"
fi

python3 --version >> "$LOG" 2>&1 || true
echo "$LOG"
