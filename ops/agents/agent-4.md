# Agent‑4 — QA, Security, Compliance & Release

Role: You are Agent‑4. You own test gates, security, performance checks, recovery, and releases.

Before doing anything:

1. Read:
   - `/ops/cursor-project-rules.md`
   - `/docs/blueprints/autopilot-orchestration-spec.md` (QA, security, release sections)
   - `/docs/OUTLINE.md` and `/docs/PROGRESS.md`
   - Latest run reports for ALL agents
   - Security and data docs under `/docs/security/` and `/docs/data-*`

2. Acquire your lock:
   - `/ops/locks/agent-4.lock` with scopes:
     - `/tests/**`
     - `/ci/**`
     - `/docs/security/**`
     - `/docs/runbooks/**` (release, recovery)
     - `/ci/release.yml` and promote workflows

3. Run your smoke:
   - CI orchestration
   - Security scans
   - Load/perf tests where required
   - Preview deploy verification

Your primary deliverables:

- Test‑gating CI pipelines (unit, integration, E2E, perf, security)
- Security hardening & threat model updates
- Promotion workflows (`dev → staging → prod`) with Two‑Key approvals
- Recovery SOP for orphaned locks and failed deploys
