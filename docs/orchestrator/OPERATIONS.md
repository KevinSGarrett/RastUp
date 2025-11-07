# Operations (Slack & CLI)
## Commands
/orchestrator status — snapshot (% complete, active locks, budget)
/orchestrator tail <agent|run-id> — 15m live tail
/orchestrator run "<title>" [--wbs WBS-x.y] — spawn a run
/orchestrator approve <proposal-id> — typed ack
/orchestrator verbosity <milestones|summaries|quiet>

## Attach Packs
Saved under /docs/orchestrator/from-agents/AGENT-<N>/run-<ts>-attach.zip (stdout/stderr, diffs, proofs).

## Triage Flow
- Failing smoke → SAFE-MODE + incident
- Stuck 2 cycles → propose Boost or split plan
- Overage >80% → Economy Mode; queue heavy calls
