# Orchestrator POLICY (V1)
## Purpose
Durable, budget-aware conductor for Cursor agents with Slack control, audit logs, approvals, SAFE-MODE, and resumability.

## Approvals
Single approver (you). Typed ack phrase: `APPROVE`. Low-risk allowlist: docs updates, lint-only fixes, re-run CI, create draft PR.

## Budget
Weekly cap: $75 (OpenAI+Claude). Economy Mode at 80% (mini/Haiku-only; queue flagship). One-off Boosts with $5 stop-loss (max 3/week). Time-boxed cap raise allowed.

## SAFE-MODE
Triggers: budget soft breach, missing approvals, access smoke failures, unknown blast radius. Read-only: plans/dry-runs/draft PRs.

## Logging
JSONL event stream + cost ledger under /docs/logs; attach packs per run under /docs/orchestrator/from-agents. Redaction: no secrets; mask tokens/PII patterns. Incidents under /docs/logs/incidents.

## Recovery
Orphan lock timeout: 60 min → auto-recover with Slack notice and undo.

## Model Routing
Default: GPT-5 mini / Claude Haiku. Escalate to GPT-5 / Claude Sonnet only via Boost/cap raise. Fitness diagnostic triggers: context>8k, >20 files or >3 services, 2 cycles no artifact, 3 identical failures, or 2 CI re-fails on same root cause.

## Slack
Milestones mode + daily 6:00 PM digest; `/orchestrator tail` streams 15 min on demand; verbosity dial: milestones|summaries|quiet.

## Cursor
Use Cloud/Headless CLI; watch runs in UI; “Take Control” pauses agent and requires typed ack.
