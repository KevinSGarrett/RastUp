# One-shot quiet runner: blocks in this window, writes only to log, UTF-8 safe
# Location: scripts/orchestrator/start_bolt.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -LiteralPath $PSCommandPath -Parent
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..") | Select-Object -ExpandProperty Path

$Log = Join-Path $ScriptDir "app_live.log"
$VenvActivate = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$Py = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Py)) { $Py = "python" }

[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

if (Test-Path $VenvActivate) { . $VenvActivate }

New-Item -ItemType File -Path $Log -Force | Out-Null
Write-Host ("Starting orchestrator - logging to {0}" -f $Log)

& $Py -X utf8 -u -m orchestrator.socket_main 2>&1 |
    Out-File -FilePath $Log -Append -Encoding utf8

exit $LASTEXITCODE
