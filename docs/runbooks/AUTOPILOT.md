### Autopilot: Planner / Builder / Tester / Releaser

This runbook describes the main project autopilot that stitches together planning, building, testing, and release preparation for WBS-2.0.

- **Planner**: builds and audits normalized blueprints and knowledge indices.
- **Builder**: builds and audits repository-wide index for search and coverage.
- **Tester**: runs `make ci` (lint, types, security, tests).
- **Releaser**: prepares a GitHub PR (skipped when SAFE-MODE is on).

#### Safety
- **SAFE-MODE**: if `ops/flags/safe-mode.json` exists, the releaser step is skipped.
- Writes are confined to `docs/**` for indices, reports, and logs.

#### Usage
From repo root:

```bash
# Run all stages (releaser obeys SAFE-MODE and ALLOW_RELEASE)
./tools/autopilot.sh --all

# Only planner + builder
./tools/autopilot.sh --planner --builder

# Tester only
./tools/autopilot.sh --tester

# Releaser (preview by default; set ALLOW_RELEASE=1 to attempt PR)
ALLOW_RELEASE=1 ./tools/autopilot.sh --releaser
```

#### Logs
- JSONL log: `docs/logs/autopilot.jsonl`
- CI output is streamed to the terminal; see `docs/PROGRESS.md` for a brief summary appended per run.

#### Prerequisites
- `python3` (or `python`) for planner/builder stages.
- `make` for CI.
- `gh` (GitHub CLI) for release (optional).
