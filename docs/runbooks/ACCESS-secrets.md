# ACCESS — Secrets Baseline (Names Only)

**Intent:** define stable secret *names* (no values) under **[APP]**/**[ENV]** so agents and CI reference names only. Actual creation requires Two‑Key approval and AWS credentials.

## Names (dev exemplar)
- **[APP]/dev/backend/DB_URL**
- **[APP]/dev/backend/JWT_SECRET**
- **[APP]/dev/ci/GITHUB_APP_PRIVATE_KEY**
- **[APP]/dev/registry/ECR_PASSWORD** (optional; prefer OIDC/ECR login)

> Keep placeholders **bold** until approved. Never commit secret *values*.

## Pre‑flight (read‑only)
- AWS CLI present: `aws --version`
- Identity (may be empty until OIDC wired): `aws sts get-caller-identity`

## Execution (idempotent) — **DRY‑RUN by default**
Scripts:
- PowerShell: `scripts/access/seed_secret_names.ps1`
- Bash:       `scripts/access/seed_secret_names.sh`

Examples:
```powershell
# Dry-run (prints actions)
powershell -ExecutionPolicy Bypass -File scripts\access\seed_secret_names.ps1

# Execute (requires AWS creds + Two-Key approval on PR)
powershell -ExecutionPolicy Bypass -File scripts\access\seed_secret_names.ps1 -Execute
