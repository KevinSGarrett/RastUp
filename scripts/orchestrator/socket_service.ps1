# scripts/orchestrator/socket_service.ps1
# Keeps the orchestrator running in a background window; logs in UTF-8.

#requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$env:PYTHONUTF8       = "1"
$env:PYTHONIOENCODING = "utf-8"

$Root   = "C:\RastUp\RastUp"
$VenvPy = Join-Path $Root ".venv\Scripts\python.exe"
$Main   = "orchestrator.socket_main"
$LogDir = Join-Path $Root "scripts\orchestrator"
$Log    = Join-Path $LogDir "app_live.log"
$Lock   = Join-Path $Root "ops\flags\socket.lock"

New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $Lock) -Force | Out-Null

if (Test-Path $VenvPy) {
  $py = $VenvPy
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  $py = "python"
} else {
  $py = "py -3"
}

# Stop any existing instance
Get-CimInstance Win32_Process | Where-Object {
  $_.CommandLine -match "-m orchestrator\.socket_main"
} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

while ($true) {
  try {
    Set-Content -Path $Lock -Value $PID -Encoding ascii
    "$([DateTime]::UtcNow.ToString('s')) SERVICE starting; log=$Log" |
      Out-File $Log -Encoding utf8 -Append

    & $py -X utf8 -u -m $Main 2>&1 |
      ForEach-Object { $_ | Out-File -FilePath $Log -Encoding utf8 -Append }

    $code = $LASTEXITCODE
    "$([DateTime]::UtcNow.ToString('s')) SERVICE exited code=$code" |
      Out-File $Log -Encoding utf8 -Append
  }
  catch {
    "$([DateTime]::UtcNow.ToString('s')) SERVICE exception: $($_.Exception.Message)" |
      Out-File $Log -Encoding utf8 -Append
  }
  finally {
    Remove-Item $Lock -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
  }
}
