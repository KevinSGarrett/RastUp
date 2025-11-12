# scripts/orchestrator/socket_service.ps1
param([int]$BackoffSeconds = 3)

$ErrorActionPreference = "Stop"

# Resolve repo root (…/scripts/orchestrator -> repo)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent $ScriptDir
Set-Location $RepoRoot

# Environment for Python process
$env:PYTHONUTF8       = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"
$env:RU_CONFIG_DEBUG  = "1"

# Paths
$py   = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$log  = Join-Path $ScriptDir "app_live.log"
$lock = Join-Path $RepoRoot "ops\flags\socket.lock"

# Ensure flags/ exists and take a soft lock
New-Item -ItemType Directory -Force -Path (Split-Path $lock) | Out-Null
if (!(Test-Path $lock)) { Set-Content -Path $lock -Value "$PID" -Encoding ascii }

try {
  while ($true) {
    # -X utf8 and -u for unbuffered output
    & $py -X utf8 -u -m orchestrator.socket_main *>> $log
    $rc = $LASTEXITCODE
    Write-Host "socket_main exited with code $rc; restarting in $BackoffSeconds s..."
    Start-Sleep -Seconds $BackoffSeconds
  }
}
finally {
  Remove-Item -Force -ErrorAction SilentlyContinue $lock
}
