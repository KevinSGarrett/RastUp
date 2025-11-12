
**`scripts/access/seed_secret_names.ps1`**
```powershell
param(
  [switch]$Execute
)
$ErrorActionPreference = "Stop"

# Define names (keep placeholders **bold** until approved)
$Names = @(
  "**[APP]**/dev/backend/DB_URL",
  "**[APP]**/dev/backend/JWT_SECRET",
  "**[APP]**/dev/ci/GITHUB_APP_PRIVATE_KEY",
  "**[APP]**/dev/registry/ECR_PASSWORD"
)

Write-Host "Secrets to ensure (dev):"
$Names | ForEach-Object { Write-Host " - $_" }

if (-not $Execute) {
  Write-Host "`nDRY-RUN: add -Execute to create empty secrets ({})."
  exit 0
}

foreach ($n in $Names) {
  try {
    $exists = (aws secretsmanager describe-secret --secret-id "$n" 2>$null)
    if ($LASTEXITCODE -eq 0) {
      Write-Host "Exists: $n"
      continue
    }
  } catch {}

  Write-Host "Creating: $n"
  $tags = @("Key=created_by,Value=orchestrator","Key=env,Value=dev")
  aws secretsmanager create-secret --name "$n" `
    --secret-string '{}' `
    --tags $tags
}
Write-Host "Done."
