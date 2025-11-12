# Quiet service runner: no console spam, logs only, auto-restart loop, UTF-8 safe
# Location: scripts/orchestrator/socket_service.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -LiteralPath $PSCommandPath -Parent
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..") | Select-Object -ExpandProperty Path

$Log = Join-Path $ScriptDir "app_live.log"
$VenvActivate = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$Py = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Py)) { $Py = "python" }

# Enforce UTF-8 for the process and output
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

if (Test-Path $VenvActivate) { . $VenvActivate }

New-Item -ItemType File -Path $Log -Force | Out-Null

# One informational line, then stay quiet
Write-Host ("Service supervising orchestrator - writing to {0}" -f $Log)

while ($true) {
    try {
        & $Py -X utf8 -u -m orchestrator.socket_main 2>&1 |
            Out-File -FilePath $Log -Append -Encoding utf8
        $code = $LASTEXITCODE
    } catch {
        $code = -1
        $_ | Out-File -FilePath $Log -Append -Encoding utf8
    }
    Start-Sleep -Seconds 3
}
