# Cursor Project Rules (Repo‑Level)

## Purpose
Define how Cursor agents operate in this repo so the Orchestrator can run near‑autopilot and produce small, reviewable, test‑gated changes with full traceability to the blueprints.

## Blueprint‑First Sources (single source of truth)
- Non‑Technical Plan: `docs/blueprints/Combined_Master_PLAIN_Non_Tech_001.docx`  (IDs `NT‑…`)
- Technical Plan: `docs/blueprints/TechnicalDevelopmentPlan.odt`                (IDs `TD‑…`)
- Index of sections/anchors: `docs/blueprints/sections.json`

**Hard rule:** Every plan/PR/commit must cite relevant `NT-` and `TD-` IDs and one `WBS-` id in trailers.

## Hard Rules (must follow)
1. **Non‑Interference / Locks**  
   Before changing files, acquire a lock at `ops/locks/agent-<name>.lock` JSON with `task_id`, `scope_paths[]`, and `blueprint_refs[]`. Do not change files outside your declared scope. Release the lock at the end of the run.

2. **Access Smoke Tests (before edits)**  
   Run relevant checks under `/scripts/smoke/` for your scope (local FS write to repo root, Docker build if used, Git operations, etc.). If a smoke fails, stop and output an *Access Enablement Plan* instead of proceeding.

3. **Two‑Key for Destructive/Costly Actions**  
   Any destructive or cost‑incurring action must create a proposal under `ops/approvals/` and stop until approved. Default to dry‑runs and draft PRs.

4. **No Secrets in Repo**  
   Reference secrets only by name (AWS Secrets Manager). Never commit values or `.env` with values.

5. **Traceability & Run Reports**  
   - Commits use Conventional Commits **and** include trailers:  
     `NT: NT-x.y` • `TD: TD-a.b` • `WBS: WBS-p.q`  
   - After a substantive run, write a run report under `docs/runs/YYYY‑MM‑DD/AGENT‑N/run-<timestamp>.md` and produce an attach pack zip under `docs/orchestrator/from-agents/AGENT-<N>/`.

6. **Tests Gate Merges**  
   Do not merge to `main` unless lint/tests/security/coverage workflows are green.

## Soft Rules (optimize)
- Small PRs, clear ADRs for major decisions, preview envs per PR where applicable, consistent lint/format, conservative dependencies.

---

## WBS‑1.2 — CI Pipelines Deliverables (what to build now)

Create or update the following GitHub Actions workflows under `.github/workflows/`:

1. **`ci-lint.yml`** — Lint & formatting  
   - Triggers: `pull_request`, `push` to `main`, `workflow_dispatch`  
   - Steps: checkout, setup Python 3.11, cache pip, install `tools/requirements-ci.txt` if present, then run:  
     - `ruff check .`  
     - `black --check .` (if Black config present)  
     - `mypy` (if `mypy.ini` or `pyproject.toml` type hints present)

2. **`ci-test.yml`** — Unit/integration tests  
   - Triggers: same as lint  
   - Steps: checkout → setup Python → install test deps → `pytest -q` with JUnit + coverage artifact upload  
   - Fail PR if coverage for touched files < 85% (use a simple coverage threshold if global is easier).

3. **`ci-build-push.yml`** — Build container(s) and (for PRs) push to a preview registry (no prod)  
   - Triggers: `pull_request` and `workflow_dispatch`  
   - Steps: checkout → Docker build (e.g., `docker/orchestrator.Dockerfile` if present) → push to *dev/preview* registry **only** when not SAFE‑MODE (honor `ops/flags/safe-mode.json` by skipping push).

4. **`ci-security.yml`** — SAST & secret scan  
   - Triggers: PR, push to `main`, scheduled `cron`  
   - Steps: run a Python‑appropriate static analyzer (e.g., `bandit -r orchestrator -x tests`) and a secret scanner (e.g., `gitleaks` or GH secret scan if available).  
   - Fail on High‑severity findings unless an exemption file exists (e.g., `ops/exemptions/cve-justifications.json`).

5. **`ci-deps-license.yml`** — Dependency & license check  
   - Triggers: PR, push, weekly `cron`  
   - Steps: deps audit (e.g., `pip-audit` or `pipdeptree` + OSV) and license policy (deny GPL‑3.0 if incompatible, etc.). Upload a short report to `docs/reports/deps-license.md`.

6. **`ci-smoke.yml`** — Access smoke tests (scripted)  
   - Triggers: PR touching critical paths, nightly `workflow_dispatch`, `schedule`  
   - Steps: run scripts under `scripts/smoke/` (PowerShell on Windows runner and Bash on Ubuntu runner). Upload logs to `docs/test-reports/smoke/`.

### Conventions the workflows must enforce
- Required checks on PR: **lint**, **test**, **security**, **deps-license**, and **smoke** (if paths match).  
- Every PR description must include the **Blueprint Concordance** block and **trailers**.  
- Artifacts: upload coverage XML/HTML, smoke logs, and any generated reports.

---

## Commits, PRs, and Ownership

- **Commit trailers** (required):  
