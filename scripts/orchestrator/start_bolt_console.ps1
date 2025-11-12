#requires -version 5.1
# scripts/orchestrator/start_bolt_console.ps1
# Foreground runner with console output + UTF-8 log, auto-restart loop.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

# Resolve paths using $PSScriptRoot (robust in PowerShell 5.1)
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

Write-Host ("Launching orchestrator (console mode) - logging to {0}" -f $Log)

while ($true) {
    $ts = (Get-Date).ToString('s')
    Write-Log "[$ts] CONSOLE start -> $Py"
    try {
        & $Py -X utf8 -u -m orchestrator.socket_main 2>&1 | ForEach-Object {
            $_
            Write-Log $_
        }
        $code = $LASTEXITCODE
    } catch {
        $code = -1
        $_ | Out-String | ForEach-Object { Write-Log $_; Write-Host $_ }
    }
    $ts = (Get-Date).ToString('s')
    Write-Log "[$ts] CONSOLE exit code=$code"
    Write-Host ("Exited with code {0}. Restarting in 3s (Ctrl+C to stop)..." -f $code) -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}
