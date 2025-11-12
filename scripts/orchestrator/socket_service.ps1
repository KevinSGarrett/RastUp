# scripts/orchestrator/socket_service.ps1
# Quiet background service: logs only (blank window by design), auto-restart, UTF-8.

#requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$env:PYTHONUTF8       = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUNBUFFERED = '1'

$ScriptDir = $PSScriptRoot
$RepoRoot  = (Resolve-Path (Join-Path $ScriptDir '..\..')).Path

$LogDir = $ScriptDir
$Log    = Join-Path $LogDir 'app_live.log'
$Lock   = Join-Path $RepoRoot 'ops\flags\socket.lock'

$VenvPy = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (Test-Path $VenvPy) {
  $py = $VenvPy
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  $py = 'py -3'
} else {
  $py = 'python'
}

New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $Lock) -Force | Out-Null
'' | Out-File -FilePath $Log -Encoding utf8

# Stop any existing main
Get-CimInstance Win32_Process | Where-Object {
  $_.CommandLine -match '-m orchestrator\.socket_main'
} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

# This service window is intentionally quiet; tail the log to see activity
Write-Host ("Service supervising orchestrator - logging to {0}" -f $Log)

while ($true) {
  try {
    Set-Content -Path $Lock -Value $PID -Encoding ascii
    ($([DateTime]::UtcNow.ToString('s')) + ' SERVICE boot') |
      Out-File -FilePath $Log -Encoding utf8 -Append

    & $py -X utf8 -u -m orchestrator.socket_main 2>&1 |
      ForEach-Object { $_ | Out-File -FilePath $Log -Encoding utf8 -Append }

    $code = $LASTEXITCODE
    ($([DateTime]::UtcNow.ToString('s')) + " SERVICE exit code=$code") |
      Out-File -FilePath $Log -Encoding utf8 -Append
  }
  catch {
    ($([DateTime]::UtcNow.ToString('s')) + " SERVICE exception: " + $_.Exception.Message) |
      Out-File -FilePath $Log -Encoding utf8 -Append
  }
  finally {
    Remove-Item $Lock -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
  }
}
