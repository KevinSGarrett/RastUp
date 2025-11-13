# scripts/orchestrator/socket_service.ps1
# Single-instance supervisor for the Slack orchestrator (Windows venv only).

$ErrorActionPreference = "Stop"

$repoRoot   = "C:\RastUp\RastUp"
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$logFile    = Join-Path $repoRoot "scripts\orchestrator\app_live.log"
$lockFile   = Join-Path $repoRoot "ops\flags\socket.lock"

Write-Host "Service supervising orchestrator - logging to $logFile"
"$(Get-Date -Format o) SERVICE pythonExe = $venvPython" | Out-File $logFile -Append

# Kill any old runners (system Python or stray venv ones)
Get-CimInstance Win32_Process |
  Where-Object {
    $_.CommandLine -match "orchestrator\.socket_main" -or
    $_.CommandLine -match "socket_service\.ps1"
  } | ForEach-Object {
    try { Stop-Process -Id $_.ProcessId -Force } catch {}
  }

# Clear stale lock
Remove-Item $lockFile -ErrorAction SilentlyContinue

# Ensure venv python exists
if (-not (Test-Path $venvPython)) {
  "$(Get-Date -Format o) SERVICE fatal: venv python not found at $venvPython" | Out-File $logFile -Append
  Write-Host "SERVICE ERROR: venv python not found at $venvPython" -ForegroundColor Red
  exit 1
}

Set-Location $repoRoot

while ($true) {
  "$(Get-Date -Format o) SERVICE boot" | Out-File $logFile -Append
  try {
    $env:PYTHONUNBUFFERED = "1"
    $env:SLACK_LOG = "info"

    & $venvPython -X dev -u -m orchestrator.socket_main *>> $logFile

    $code = $LASTEXITCODE
    "$(Get-Date -Format o) SERVICE exit: $code" | Out-File $logFile -Append
  }
  catch {
    "$(Get-Date -Format o) SERVICE exception: $($_.Exception.Message)" | Out-File $logFile -Append
  }

  Start-Sleep -Seconds 3
}
