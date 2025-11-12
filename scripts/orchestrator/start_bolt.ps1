#requires -Version 5.1
Set-StrictMode -Version Latest

# ---- UTF-8 everywhere: fixes 'charmap' decode/encode issues ----
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# ---- Paths ----
$Root   = "C:\RastUp\RastUp"
$VenvPy = Join-Path $Root ".venv\Scripts\python.exe"
$Main   = "orchestrator.socket_main"
$LogDir = Join-Path $Root "scripts\orchestrator"
$Log    = Join-Path $LogDir "app_live.log"
$Lock   = Join-Path $Root "ops\flags\socket.lock"

# ---- Ensure folders exist ----
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $Lock) -Force | Out-Null

# ---- Single-instance guard: stop any old socket_main runners (system/global) ----
Get-CimInstance Win32_Process | Where-Object {
  $_.CommandLine -match "-m orchestrator\.socket_main"
} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

# ---- Write lock with our PID ----
Set-Content -Path $Lock -Value $PID -Encoding ascii

# ---- Banner to log ----
$ts = Get-Date -Format "s"
"$ts START start_bolt.ps1; log=$Log" | Out-File -FilePath $Log -Encoding utf8 -Append

try {
  # -X dev + -u (unbuffered) makes logs more immediate
  & $VenvPy -X dev -u -m $Main *>> $Log
}
finally {
  Remove-Item $Lock -Force -ErrorAction SilentlyContinue
}
