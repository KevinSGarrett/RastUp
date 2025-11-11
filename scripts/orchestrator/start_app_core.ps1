$ErrorActionPreference = "Stop"
cd C:\RastUp\RastUp
. .\.venv\Scripts\Activate.ps1
$env:SLACK_LOG = "debug"
$env:PYTHONUNBUFFERED = "1"
Write-Host "Starting Socket Mode…" -ForegroundColor Cyan
python -X dev -u -m orchestrator.app 2>&1 | Tee-Object -FilePath scripts\orchestrator\app_live.log
