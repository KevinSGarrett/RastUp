$ErrorActionPreference = "Stop"
Set-Location C:\RastUp\RastUp

# ---- single-instance lock ----
$lock = "ops\flags\socket.lock"
if (Test-Path $lock) {
  try {
    $j = Get-Content $lock -Raw | ConvertFrom-Json
    if ($j -and (Get-Process -Id $j.pid -ErrorAction SilentlyContinue)) {
      Write-Host "Orchestrator service already running (PID $($j.pid))." -ForegroundColor Yellow
      exit 0
    }
  } catch {}
}
@{ pid = $PID; started = (Get-Date).ToUniversalTime().ToString("s") + "Z" } |
  ConvertTo-Json | Set-Content $lock -Encoding UTF8

try {
  . .\.venv\Scripts\Activate.ps1
  $env:SLACK_LOG = "info"
  $env:PYTHONUNBUFFERED = "1"
  $py  = "C:\RastUp\RastUp\.venv\Scripts\python.exe"
  $log = "scripts\orchestrator\app_live.log"

  Write-Host "== Orchestrator Socket Service (PID $PID) ==" -ForegroundColor Cyan

  while ($true) {
    # ensure only venv-backed runner is alive
    Get-CimInstance Win32_Process |
      Where-Object { $_.CommandLine -like "*-m orchestrator.socket_main*" -and $_.CommandLine -notlike "*\.venv\Scripts\python.exe*" } |
      ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

    Write-Host "[restart] launching via venv python ..." -ForegroundColor Yellow

    if (Test-Path $log) { Move-Item -Force $log "$log.bak" -ErrorAction SilentlyContinue }

    # Inline launch; append stdout+stderr to log; block until exit
    & $py -X dev -u -m orchestrator.socket_main *>> $log 2>&1

    $code = $LASTEXITCODE
    Write-Host "[exit] socket_main exited (Code=$code) — restart in 3s ..." -ForegroundColor Red
    Start-Sleep -Seconds 3
  }
}
finally {
  Remove-Item $lock -Force -ErrorAction SilentlyContinue
}
