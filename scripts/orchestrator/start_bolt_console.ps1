# scripts/orchestrator/start_bolt_console.ps1
# Console runner: visible output + log, auto-restart loop, UTF-8 safe.

#requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Force UTF-8 for console and for Python I/O
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$env:PYTHONUTF8       = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUNBUFFERED = '1'

# Derive paths from the script directory (no Split-Path)
$ScriptDir = $PSScriptRoot
$RepoRoot  = (Resolve-Path (Join-Path $ScriptDir '..\..')).Path

$LogDir = $ScriptDir
$Log    = Join-Path $LogDir 'app_live.log'
$Lock   = Join-Path $RepoRoot 'ops\flags\socket.lock'

# Prefer venv python if present
$VenvPy = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (Test-Path $VenvPy) {
  $py = $VenvPy
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  $py = 'py -3'
} else {
  $py = 'python'
}

# Ensure dirs and pre-create a UTF-8 log
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $Lock) -Force | Out-Null
'' | Out-File -FilePath $Log -Encoding utf8

# Kill any existing orchestrator main
Get-CimInstance Win32_Process | Where-Object {
  $_.CommandLine -match '-m orchestrator\.socket_main'
} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

Write-Host ("Launching orchestrator (console mode) - logging to {0}" -f $Log) -ForegroundColor Cyan

# Auto-restart loop (Ctrl+C to stop)
while ($true) {
  try {
    Set-Content -Path $Lock -Value $PID -Encoding ascii

    $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    "[{0}] START python -m orchestrator.socket_main" -f $ts | Out-File -FilePath $Log -Encoding utf8 -Append

    # Stream child output to console AND to log
    & $py -X utf8 -u -m orchestrator.socket_main 2>&1 |
      ForEach-Object {
        $_
        $_ | Out-File -FilePath $Log -Encoding utf8 -Append
      }

    $code = $LASTEXITCODE
    $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    "[{0}] EXIT code {1}. Restarting in 3s (Ctrl+C to stop)..." -f $ts, $code |
      Out-File -FilePath $Log -Encoding utf8 -Append
  }
  catch {
    ($_.Exception.Message) | Out-File -FilePath $Log -Encoding utf8 -Append
  }
  finally {
    Remove-Item $Lock -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
  }
}
