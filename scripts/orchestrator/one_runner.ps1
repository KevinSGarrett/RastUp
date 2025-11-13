# --- one_runner.ps1 ---
# Purpose: enforce exactly ONE console runner using the venv Python,
# clean stale processes/locks, and tail UTF-8 logs automatically.

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

# Resolve repo and script paths (PS 5.1 safe)
$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptDir  = Split-Path -Parent $ScriptPath
$RepoRoot   = Resolve-Path (Join-Path $ScriptDir "..\..")

# Paths
$Runner   = Join-Path $ScriptDir "start_bolt_console.ps1"
$Lock     = Join-Path $RepoRoot "ops\flags\socket.lock"
$AppLog   = Join-Path $ScriptDir "app_live.log"
$StdOut   = Join-Path $ScriptDir "stdout.txt"
$StdErr   = Join-Path $ScriptDir "stderr.txt"
$VenvPy   = Join-Path $RepoRoot ".venv\Scripts\python.exe"

# 1) Stop anything related (older runs, service windows, stray pythons)
Get-CimInstance Win32_Process | Where-Object {
  $_.CommandLine -match 'orchestrator\.socket_main|socket_service\.ps1|start_bolt_console\.ps1'
} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

# Kill any system Python that is running orchestrator (keep venv Python only)
$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*-m orchestrator.socket_main*' }
foreach ($p in $procs) {
  $exe = $p.ExecutablePath
  if (-not $exe) { try { $exe = (Get-Process -Id $p.ProcessId -ErrorAction Stop).Path } catch {} }
  if ($exe -and (Test-Path $VenvPy) -and ($exe -ne $VenvPy)) {
    try { Stop-Process -Id $p.ProcessId -Force } catch {}
  }
}

# 2) Clear stale lock + logs (optional)
Remove-Item $Lock  -ErrorAction SilentlyContinue
Remove-Item $AppLog -ErrorAction SilentlyContinue
Remove-Item $StdOut -ErrorAction SilentlyContinue
Remove-Item $StdErr -ErrorAction SilentlyContinue

# 3) Start the console runner in a new PowerShell window
Start-Process powershell.exe -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File', $Runner `
  -WorkingDirectory $RepoRoot

# 4) Tail the log as UTF‑8 once it appears
while (-not (Test-Path $AppLog)) { Start-Sleep -Milliseconds 200 }
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
Write-Host "Tailing $AppLog (Ctrl+C to stop)..." -ForegroundColor Cyan
Get-Content $AppLog -Encoding UTF8 -Tail 120 -Wait
