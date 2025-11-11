param([switch]$Quiet)
Set-Location -Path "C:\RastUp\RastUp"
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
. .\.venv\Scripts\Activate.ps1
$env:SLACK_LOG = "debug"
$env:PYTHONUNBUFFERED = "1"
Write-Host "Starting Slack orchestrator (Socket Mode)..." -ForegroundColor Cyan
python -X dev -u -m orchestrator.app
