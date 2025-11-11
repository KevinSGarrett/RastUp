# RastUp — Developer README

## Orchestrator Quick Links
- Health: `docs/orchestrator/HEALTH.md`
- Budget: `docs/orchestrator/SUMMARY.md`
- Audit: `docs/orchestrator/AUDIT.jsonl`
- Agent outputs: `docs/orchestrator/from-agents/AGENT-*/`

## Slack Commands (channel: #orchestrator)
- `/orchestrator ping` — quick alive + SAFE/Boost
- `/orchestrator status` — budget, SAFE, boost, etc.
- `/orchestrator safe on|off` — toggle SAFE‑MODE
- `/orchestrator boost <amount>|clear` — manage Boost
- `/orchestrator tail [AGENT] [--lines N]` — show end of latest agent log
- `/orchestrator run "Title" --agent AGENT-1 --model gpt-5 --timeout 600` — start a bounded Cursor run

## Blueprints (single source of truth)
- Non‑Technical: `docs/blueprints/Combined_Master_PLAIN_Non_Tech_001.docx`
- Technical: `docs/blueprints/TechnicalDevelopmentPlan.odt`
- Sections index: `docs/blueprints/sections.json` (IDs `NT-…` / `TD-…`)

## CI Expectations (overview)
- Lint, Test, Build/Push (preview only), Security, Deps/License, and Smoke workflows in `.github/workflows/`.
- PRs must include **NT/TD/WBS trailers**; required checks must be green.
