# Orchestrator Runbook

## Knowledge operations
- Build: `python -m orchestrator.knowledge build`
- Audit (strict): `python -m orchestrator.knowledge audit --strict`
- Read file: `python -m orchestrator.knowledge read --path docs/blueprints/plain/TechnicalDevelopmentPlan.md`
- Peek first N lines: `python -m orchestrator.knowledge read --path docs/blueprints/plain/TechnicalDevelopmentPlan.md --first 80`
- Query segments: `python -m orchestrator.knowledge query --text "deploy pipeline" --k 5`

Notes:
- Outputs are written under `docs/blueprints/*` and `docs/index/*`.
- SAFE-MODE allows knowledge builds (docs-only writes). Other writes require explicit approval.

## Slack commands (channel: #orchestrator)
- `/orchestrator ping` — quick alive + SAFE/Boost
- `/orchestrator status` — budget, SAFE, boost, etc.
- `/orchestrator safe on|off` — toggle SAFE‑MODE (off requires approval)
- `/orchestrator boost <amount>|clear` — manage Boost (requires approval)
- `/orchestrator tail [AGENT] [--lines N]` — show recent agent log
- `/orchestrator run "Title" --agent AGENT-1 --model gpt-5` — start a bounded Cursor run
- `/agent run "Title" --agent AGENT-1 --model gpt-5` — shorthand

SAFE-MODE behavior:
- When SAFE-MODE is ON, agent runs are blocked unless a positive Boost is set.
- SAFE-OFF and Boost changes require an approved entry under `ops/approvals/*.json` with `status: approved` and `allowed: ["write"]` or `"all"`.

## Environment
Set in `.env` (see `.env.example`):
- `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `SLACK_SIGNING_SECRET`
- `CURSOR_CLI`, `CURSOR_AGENT_MODEL`, `REPO_ROOT`
- Budget knobs: `WEEKLY_USD_CAP`, `SOFT_ALERT_PCT`, `BOOST_STOP_LOSS`

## CI
- GitHub Actions workflow `CI - Knowledge` builds and audits knowledge artifacts on PRs and main.
- Build step continues on error if optional tools are missing; audit is strict.
