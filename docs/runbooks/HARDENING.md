### Hardening Runbook

This runbook describes local security/hardening checks and how to remediate issues.

- **What’s included**:
  - Secrets scanning test in `tests/test_secrets_scan.py` to block committed secrets in code/config.
  - Local helper `tools/security_checks.sh` to run lint, type checks, Bandit, YAML lint, and a simple high‑signal secret grep.
  - CI target `make ci` installs tools and runs lint ➜ type ➜ security ➜ tests.

- **How to run everything**:
  - Install prerequisites via Make: `make ci` (installs dev tools, runs checks and tests)
  - Or run the helper script: `bash tools/security_checks.sh`

- **What is scanned for secrets**:
  - High‑signal patterns (AWS keys, GitHub PATs, Slack tokens, Google API keys, private key blocks)
  - Scopes to source/config dirs: `orchestrator/`, `ops/`, `infra/`, `scripts/`, `docker/`, `tools/`

- **If a secret is flagged**:
  - Immediately rotate the credential at the provider.
  - Remove the secret from the file and replace with an environment variable reference or secret manager.
  - If already committed, scrub history with a tool like `git filter-repo` and force‑rotate at provider.

- **YAML and code security**:
  - `Bandit` runs on `orchestrator/` to catch common Python security issues.
  - `yamllint` runs on `ops/` and `infra/` when present.

- **Notes**:
  - The helper script is best‑effort: it skips tools not installed locally and non‑existent directories.
  - The CI pipeline (via `make ci`) enforces the Python tools defined in `tools/requirements-ci.txt`.
