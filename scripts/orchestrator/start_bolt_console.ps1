# Console runner: visible output + log, auto-restart loop, UTF-8 safe
# Location: scripts/orchestrator/start_bolt_console.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Resolve repo root from this script's path
$ScriptDir = Split-Path -LiteralPath $PSCommandPath -Parent
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..") | Select-Object -ExpandProperty Path

# Paths
$Log = Join-Path $ScriptDir "app_live.log"
$VenvActivate = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$Py = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Py)) { $Py = "python" }

# Enforce UTF-8 in this console and for Python
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# Activate venv if present
if (Test-Path $VenvActivate) { . $VenvActivate }

# Ensure log exists
New-Item -ItemType File -Path $Log -Force | Out-Null

Write-Host ("Launching orchestrator (console mode) - logging to {0}" -f $Log)

# Auto-restart loop (Ctrl+C to stop)
while ($true) {
    $ts = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    Write-Host ("[{0}] START python -m orchestrator.socket_main" -f $ts) -ForegroundColor Cyan

    try {
        & $Py -X utf8 -u -m orchestrator.socket_main 2>&1 |
            Tee-Object -FilePath $Log -Append
        $code = $LASTEXITCODE
    } catch {
        $code = -1
        $_ | Out-String | Tee-Object -FilePath $Log -Append | Write-Host
    }

    $ts = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    Write-Host ("[{0}] EXIT code {1}. Restarting in 3s (Ctrl+C to stop)..." -f $ts, $code) -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}
