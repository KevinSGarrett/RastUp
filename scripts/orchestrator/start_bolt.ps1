#requires -version 5.1
# scripts/orchestrator/start_bolt.ps1
# One-shot quiet runner, logs to UTF-8 file, no auto-restart.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Log      = Join-Path $PSScriptRoot 'app_live.log'
$VenvPy   = Join-Path $RepoRoot '.venv\Scripts\python.exe'
$Py       = if (Test-Path $VenvPy) { $VenvPy } else { 'python' }

# UTF-8 everywhere
$env:PYTHONUTF8       = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONPATH       = $RepoRoot

# UTF-8 (no BOM) log writer
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$logWriter = New-Object System.IO.StreamWriter($Log, $true, $utf8NoBom)
$logWriter.AutoFlush = $true
function Write-Log([string]$line) { $logWriter.WriteLine($line) }

Write-Log ("[{0}] START one-shot" -f (Get-Date).ToString('s'))

try {
    & $Py -X utf8 -u -m orchestrator.socket_main 2>&1 | ForEach-Object { Write-Log $_ }
    exit $LASTEXITCODE
} finally {
    $logWriter.Dispose()
}
