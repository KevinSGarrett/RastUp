#!/usr/bin/env bash
# shellcheck shell=bash
# Agent-1 smoke (Linux/WSL) — writes a log and prints its path.
# Keep LF endings. If needed:
#   wsl -d Ubuntu -- bash -lc 'cd /mnt/c/RastUp/RastUp && sed -i "s/\r$//" scripts/smoke/agent1.sh && chmod +x scripts/smoke/agent1.sh'

# Strict-ish; tolerate shells without pipefail (old or BusyBox variants)
set -Eeuo pipefail 2>/dev/null || set -Eeuo
(set -o pipefail) 2>/dev/null || true

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
REPORT="$ROOT/docs/test-reports/smoke"
LOG="$REPORT/agent1-linux.log"
mkdir -p "$REPORT"

{
  echo "== Agent-1 Smoke (Linux) =="
  printf 'UTC: %s\n' "$(date -u +%FT%TZ)"
  printf 'ROOT=%s\n\n' "$ROOT"

  # Local FS write/delete
  TMP="$ROOT/tmp.smoke.$$"
  if printf "ok" > "$TMP" && rm -f "$TMP"; then
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

  # Docker (distinguish stub vs working)
  if command -v docker >/dev/null 2>&1; then
    if docker --version >/dev/null 2>&1; then
      printf 'PASS: docker present - '
      docker --version | head -n1
    else
      echo "WARN: docker CLI present but not integrated with this WSL distro"
      echo "      Enable Docker Desktop → Settings → Resources → WSL integration → check 'Ubuntu'."
    fi
  else
    echo "WARN: docker not present"
  fi

  echo ""
  echo "SMOKE DONE"
} > "$LOG" 2>&1

echo "$LOG"
exit 0
