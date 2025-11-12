#!/usr/bin/env bash
set -e

echo "[smoke] repo: $(pwd)"

SAFE_FLAG="ops/flags/safe-mode.json"

echo "[smoke] audit (non-strict)"
python3 -m orchestrator.knowledge audit || true

if [ -f "$SAFE_FLAG" ]; then
  echo "[smoke] SAFE-MODE detected -> skip build"
else
  echo "[smoke] build (if needed)"
  python3 -m orchestrator.knowledge build || true
fi

echo "[smoke] query: acceptance criteria"
python3 -m orchestrator.knowledge query --text "acceptance criteria" --k 3 --json || true

echo "[smoke] done"
