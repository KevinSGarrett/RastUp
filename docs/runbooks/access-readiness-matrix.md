# Access Readiness Matrix — Orchestrator

**Purpose.** Before enabling near‑autopilot, prove each critical surface works end‑to‑end.  
**Gate.** Autopilot allowed only when **all critical rows are PASS** (see below).

## Critical Rows (must PASS)
- Local filesystem read/write under **repo root**
- Docker build available
- GitHub push / PR creation
- CI workflow execution (lint/test/build)
- **[SECRET_MANAGER]** (dev) read test (name-only reference)
- **[REGISTRY]** (dev) push/pull (e.g., ECR)
- Cloud auth + `terraform plan` (read‑only) for dev
- DNS read (write may be deferred behind Two‑Key)

> Evidence artifacts should be written under `docs/test-reports/smoke/` or CI logs.

## Matrix

| Resource        | Capability     | Agent(s) | Command / Check (example)                                        | Expected Result           | Status | Notes |
|----------------|----------------|----------|-------------------------------------------------------------------|---------------------------|--------|-------|
| Local FS       | read/write     | A‑1..4   | Windows: `scripts/smoke/agent1.ps1`; Linux: `scripts/smoke/agent1.sh` | `PASS: local fs write`    | PASS/TODO/FAIL |  |
| Docker         | build socket   | A‑1..4   | `docker --version`                                                | version prints            | PASS/TODO/FAIL |  |
| GitHub         | push / PR      | A‑1      | CI `actions/checkout@v4` + PR draft step                          | PR draft created          | PASS/TODO/FAIL |  |
| CI             | run workflows  | A‑1..4   | `Orchestrator Smoke` workflow                                     | green                     | PASS/TODO/FAIL |  |
| Secrets (dev)  | read by name   | A‑1..4   | (name-only) validate ARN/secret name resolves in dev              | success                   | PASS/TODO/FAIL |  |
| Registry (dev) | push/pull      | A‑1..2   | `docker login && docker pull/push` (dev tag)                      | success                   | PASS/TODO/FAIL |  |
| Cloud (dev)    | terraform plan | A‑1      | `terraform -chdir=infra/dev plan` (read‑only)                     | plan output               | PASS/TODO/FAIL |  |
| DNS            | read           | A‑1      | provider CLI `list` domains                                       | list printed              | PASS/TODO/FAIL |  |

### How to Update This File
- Paste excerpts of the latest **smoke logs** and **CI links** under each row’s Notes.
- Use `PASS` only when there’s a verifiable artifact (log path or CI URL).
- Save and commit. CI will attach this to the project heartbeat.

## Evidence Pointers
- Windows smoke: `docs/test-reports/smoke/agent1-windows.log`
- Linux smoke:   `docs/test-reports/smoke/agent1-linux.log`
- CI: GitHub Actions → “Orchestrator Smoke”
