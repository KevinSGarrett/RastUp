# Cursor Project Rules (Repo‑Level) — v0.1

Purpose
-------
Define how Cursor agents operate in this repo so the Orchestrator can run near‑autopilot and produce small, reviewable, test‑gated changes with full traceability to the blueprints.

Terminology (trailers go in commit messages and PR descriptions)
----------------------------------------------------------------
NT: NT-x.y
TD: TD-a.b
WBS: WBS-<phase>.<task>

Blueprint‑First Sources (single source of truth)
------------------------------------------------
- Non‑Technical Plan: docs/blueprints/Combined_Master_PLAIN_Non_Tech_001.docx  (IDs NT‑…)
- Technical Plan:     docs/blueprints/TechnicalDevelopmentPlan.odt              (IDs TD‑…)
- Sections index:     docs/blueprints/sections.json

Hard rule: Every plan/PR/commit must cite relevant NT and TD IDs and one WBS id in trailers.

Operating Modes
---------------
- SAFE‑MODE: when ops/flags/safe-mode.json exists → read‑only checks, dry‑runs, draft PRs; no pushes/deploys.
- Two‑Key: destructive or cost‑incurring actions require an approval artifact under ops/approvals/ before execution.

Hard Rules (must follow)
------------------------
1) Non‑Interference / Locks
   - Before edits, create ops/locks/agent-<name>.lock (JSON) with:
     task_id, scope_paths[], blueprint_refs[].
   - Do NOT modify files outside scope_paths[]. Remove the lock at end of run.

2) Access Smoke Tests (pre‑flight)
   - Run scripts/smoke/ for your scope (repo FS write, git dry‑run, optional docker build, CI workflow syntax, preview registry push).
   - If any smoke fails, STOP and output an Access Enablement Plan (automation or runbook). Do not proceed.

3) Two‑Key & Cost Control
   - Any destructive/costly step must create ops/approvals/<id>.md or .json and pause until approved.
   - Respect SAFE‑MODE: skip pushes/deploys while safe-mode.json exists.

4) Secrets
   - Never commit secrets or .env with values. Reference secrets ONLY by name (AWS Secrets Manager).

5) Traceability & Run Reports
   - Use Conventional Commits AND include trailers:
     NT: NT-x.y
     TD: TD-a.b
     WBS: WBS-<phase>.<task>
   - After substantive runs, write a report under docs/runs/YYYY‑MM‑DD/AGENT‑N/run-<timestamp>.md
     and create an attach pack zip under docs/orchestrator/from-agents/AGENT-<N>/.

6) Quality Gates
   - No merge to main unless lint, tests, security, and deps/license workflows pass.
   - Coverage target for touched code ≥ 85% (or explicit project threshold if temporary).

Soft Rules (optimize)
---------------------
Small PRs; ADRs for major decisions; preview env per PR when applicable; consistent lint/format; conservative dependencies; typed APIs; WCAG AA & Lighthouse budgets for UI work.

WBS‑1.2 — CI Pipelines (deliverables to build now)
--------------------------------------------------
Create/update these in .github/workflows/:

1) ci-lint.yml — Lint & formatting
   - Triggers: pull_request, push to main, workflow_dispatch
   - Steps: checkout; setup Python 3.11; cache pip; install tools/requirements-ci.txt if present; run:
     ruff check .
     black --check .   (if config present)
     mypy              (if pyproject.toml/mypy.ini configured)

2) ci-test.yml — Unit/integration tests
   - Triggers: same as lint
   - Steps: checkout → setup Python → install test deps → pytest -q
   - Upload JUnit + coverage artifacts; fail PR if coverage for touched files < 85% (or a temporary global threshold).

3) ci-build-push.yml — Build containers & push to preview
   - Triggers: pull_request, workflow_dispatch
   - Steps: checkout → Docker build (e.g., docker/*Dockerfile if present).
   - Push ONLY when SAFE‑MODE is OFF (skip if ops/flags/safe-mode.json exists) and ONLY to dev/preview registry.

4) ci-security.yml — SAST & secret scan
   - Triggers: PR, push to main, weekly cron
   - Steps: Bandit (e.g., bandit -r orchestrator -x tests) + secret scanning (gitleaks or GH).
   - Fail on High severity unless justified in ops/exemptions/cve-justifications.json.

5) ci-deps-license.yml — Dependencies & licenses
   - Triggers: PR, push, weekly cron
   - Steps: dependency audit (pip-audit or OSV) and license policy (deny disallowed licenses).
   - Upload short report to docs/reports/deps-license.md.

6) ci-smoke.yml — Access smoke tests
   - Triggers: PRs that touch critical paths, nightly schedule, workflow_dispatch
   - Steps: run scripts/smoke/ (Windows: PowerShell; Ubuntu: Bash).
   - Upload logs to docs/test-reports/smoke/.

Workflow Conventions to Enforce
-------------------------------
- Required PR checks: lint, test, security, deps-license, smoke (when path‑matched).
- Each PR description includes a “Blueprint Concordance” block and NT/TD/WBS trailers.
- Artifacts: coverage XML/HTML, smoke logs, and generated reports.

Commits, PRs, Ownership
-----------------------
- Required trailers in commit/PR text:
  NT: NT-x.y
  TD: TD-a.b
  WBS: WBS-<phase>.<task>
- Maintain ops/ownership.yaml and .github/CODEOWNERS (route orchestrator/** to your handle/AGENT‑1 initially).

Definition of Done for WBS‑1.2
------------------------------
- All workflows above exist and pass on PRs.
- PR template includes Access & Traceability and Blueprint Concordance; trailers present.
- A run report and attach pack are committed.
- docs/PROGRESS.md updated with rationale and percent complete.


When you need to read project files:
1) Ask the orchestrator to run one of:
   - python -m orchestrator.index read  --path <path> --first 120
   - python -m orchestrator.index read  --path <path> --start <a> --end <b>
   - python -m orchestrator.index query --text "<question>" --k 8

2) Use the returned snippets and cite as: <path>:<start>-<end>.

Do NOT try to open large files inside the prompt; always request a read/query.
