# Reliable Socket‑Mode service runner (single instance; quiet console; file logs)
\Continue = "Stop"
Set-Location C:\RastUp\RastUp

# Single‑instance lock
\ = "ops\flags\socket.lock"
if (Test-Path \) {
  try {
    \ = Get-Content \ -Raw | ConvertFrom-Json
    if (\ -and (Get-Process -Id \.pid -ErrorAction SilentlyContinue)) {
      Write-Host "Orchestrator service already running (PID \)." -ForegroundColor Yellow
      exit 0
    }
  } catch {}
}
@{ pid = \22748; started = (Get-Date).ToUniversalTime().ToString("s") + "Z" } | ConvertTo-Json | Set-Content \ -Encoding UTF8

try {
  . .\.venv\Scripts\Activate.ps1
  \ = "debug"
  \ = "1"
  \  = "C:\RastUp\RastUp\.venv\Scripts\python.exe"
  \ = "scripts\orchestrator\app_live.log"

  Write-Host "== Orchestrator Socket Service (PID \22748) ==" -ForegroundColor Cyan

  while (\True) {
    # ensure only venv runner
    Get-CimInstance Win32_Process |
      Where-Object { \.CommandLine -like "*-m orchestrator.socket_main*" -and \.CommandLine -notlike "*\.venv\Scripts\python.exe*" } |
      ForEach-Object { Stop-Process -Id \.ProcessId -Force }

    Write-Host "[restart] launching via venv python ..." -ForegroundColor Yellow

    if (Test-Path \) { Move-Item -Force \ "\.bak" -ErrorAction SilentlyContinue }

    # Inline launch; append stdout+stderr to log; block until exit
    & \ -X dev -u -m orchestrator.socket_main *>> \ 2>&1

    \ = \0
    Write-Host "[exit] socket_main exited (Code=\) — restart in 3s ..." -ForegroundColor Red
    Start-Sleep -Seconds 3
  }
}
finally {
  Remove-Item \ -Force -ErrorAction SilentlyContinue
}
