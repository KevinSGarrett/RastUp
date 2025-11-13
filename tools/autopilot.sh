#!/usr/bin/env bash
# tools/autopilot.sh — Main project autopilot (Planner/Builder/Tester/Releaser)
# Safe to run locally; writes confined to docs/* and logs; release step obeys SAFE-MODE.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOG_DIR="${REPO_ROOT}/docs/logs"
LOG_FILE="${LOG_DIR}/autopilot.jsonl"
SAFE_FLAG="${REPO_ROOT}/ops/flags/safe-mode.json"

mkdir -p "${LOG_DIR}"

color() { local c="$1"; shift; printf "\033[%sm%s\033[0m" "$c" "$*"; }
info()  { printf "[autopilot] %s\n" "$*"; }
warn()  { printf "[autopilot] %s\n" "$(color 33 "$*")"; }
err()   { printf "[autopilot] %s\n" "$(color 31 "$*")"; }

json_log() {
  # json_log STAGE STATUS MESSAGE DURATION_MS
  local stage="$1"; local status="$2"; local message="$3"; local dur_ms="$4"
  printf '{"ts":"%s","stage":"%s","status":"%s","ms":%s,"msg":%s}\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    "${stage}" "${status}" "${dur_ms}" \
    "$(jq -Rn --arg s "${message}" '$s')" >>"${LOG_FILE}" || true
}

find_python() {
  if command -v python3 >/dev/null 2>&1; then echo python3; return 0; fi
  if command -v python  >/dev/null 2>&1; then echo python;  return 0; fi
  return 1
}

run_cmd() {
  # run_cmd STAGE CMD...
  local stage="$1"; shift
  local start_ms end_ms dur rc
  start_ms=$(date +%s%3N)
  set +e
  "$@" 1> >(sed 's/^/[stdout] /') 2> >(sed 's/^/[stderr] /' >&2)
  rc=$?
  set -e
  end_ms=$(date +%s%3N)
  dur=$(( end_ms - start_ms ))
  if [ $rc -eq 0 ]; then
    json_log "${stage}" "ok" "success" "${dur}"
  else
    json_log "${stage}" "fail" "rc=${rc}" "${dur}"
  fi
  return $rc
}

stage_planner() {
  info "Planner: building and auditing knowledge indices"
  local py
  if ! py=$(find_python); then warn "python not found; skipping planner"; return 0; fi
  run_cmd planner-build "$py" -m orchestrator.knowledge build || return $?
  run_cmd planner-audit "$py" -m orchestrator.knowledge audit --strict || return $?
}

stage_builder() {
  info "Builder: building and auditing repository index"
  local py
  if ! py=$(find_python); then warn "python not found; skipping builder"; return 0; fi
  run_cmd builder-build "$py" -m orchestrator.index build || return $?
  run_cmd builder-audit "$py" -m orchestrator.index audit --strict || return $?
}

stage_tester() {
  info "Tester: running make ci"
  if ! command -v make >/dev/null 2>&1; then warn "make not found; skipping tests"; return 0; fi
  (cd "${REPO_ROOT}" && run_cmd tester-ci make ci) || return $?
}

stage_releaser() {
  info "Releaser: preparing PR (respects SAFE-MODE)"
  if [ -f "${SAFE_FLAG}" ]; then
    warn "SAFE-MODE is ON — release skipped"
    json_log releaser "skipped" "safe-mode" 0
    return 0
  fi
  if ! command -v gh >/dev/null 2>&1; then
    warn "GitHub CLI not available — release preview only"
    json_log releaser "skipped" "gh-missing" 0
    return 0
  fi
  # Preview only unless ALLOW_RELEASE=1
  if [ "${ALLOW_RELEASE:-0}" != "1" ]; then
    warn "ALLOW_RELEASE!=1 — not creating PR (preview mode)"
    json_log releaser "skipped" "preview" 0
    return 0
  fi
  # Best-effort PR creation (branch must already track a remote)
  run_cmd releaser-pr gh pr create --title "WBS-2.0: Autopilot bootstrap" \
    --body "Automated PR created by tools/autopilot.sh for WBS-2.0."
}

print_usage() {
  cat <<EOF
Usage: tools/autopilot.sh [--all] [--planner] [--builder] [--tester] [--releaser] [--no-color]
Default: --all (releaser obeys SAFE-MODE and ALLOW_RELEASE)
EOF
}

main() {
  local do_planner=0 do_builder=0 do_tester=0 do_releaser=0
  if [ $# -eq 0 ]; then do_planner=1; do_builder=1; do_tester=1; do_releaser=1; fi
  while [ $# -gt 0 ]; do
    case "$1" in
      --all)      do_planner=1; do_builder=1; do_tester=1; do_releaser=1 ;;
      --planner)  do_planner=1 ;;
      --builder)  do_builder=1 ;;
      --tester)   do_tester=1  ;;
      --releaser) do_releaser=1 ;;
      -h|--help)  print_usage; exit 0 ;;
      *) warn "unknown arg: $1"; print_usage; exit 2 ;;
    esac
    shift
  done

  local ok=0
  if [ $do_planner -eq 1 ];  then stage_planner  || ok=1; fi
  if [ $do_builder -eq 1 ];  then stage_builder  || ok=1; fi
  if [ $do_tester -eq 1 ];   then stage_tester   || ok=1; fi
  if [ $do_releaser -eq 1 ]; then stage_releaser || ok=1; fi

  if [ $ok -eq 0 ]; then
    info "Autopilot completed successfully"
  else
    err  "Autopilot completed with errors (see ${LOG_FILE})"
  fi
}

main "$@"
