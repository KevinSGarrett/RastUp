#requires -Version 5.1
Set-StrictMode -Version Latest

# ---- UTF-8 everywhere ----
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# ---- Paths (absolute; no current-dir surprises) ----
$Root   = "C:\RastUp\RastUp"
$VenvPy = Join-Path $Root ".venv\Scripts\python.exe"
$Main   = "orchestrator.socket_main"
$LogDir = Join-Path $Root "scripts\orchestrator"
$Log    = Join-Path $LogDir "app_live.log"
$Lock   = Join-Path $Root "ops\flags\socket.lock"

# ---- Ensure folders ----
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $Lock) -Force | Out-Null

# ---- Stop any existing instance ----
Get-CimInstance Win32_Process | Where-Object {
  $_.CommandLine -match "-m orchestrator\.socket_main"
} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

# ---- Lock and banner ----
Set-Content -Path $Lock -Value $PID -Encoding ascii
$ts = Get-Date -Format "s"
"$ts START start_bolt_console.ps1; log=$Log" | Out-File -FilePath $Log -Encoding utf8 -Append

try {
  Write-Host "Launching orchestrator (console mode) — logging to $Log" -ForegroundColor Cyan
  # Stream to console AND file
  & $VenvPy -X dev -u -m $Main 2>&1 | Tee-Object -FilePath $Log -Append
}
finally {
  Remove-Item $Lock -Force -ErrorAction SilentlyContinue
}
