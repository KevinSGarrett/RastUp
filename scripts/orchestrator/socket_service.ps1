#requires -version 5.1
# scripts/orchestrator/socket_service.ps1
# Quiet service runner (no console spam), auto-restart, UTF-8 log.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Log      = Join-Path $PSScriptRoot 'app_live.log'
$LockPath = Join-Path $RepoRoot 'ops\flags\socket.lock'
$VenvPy   = Join-Path $RepoRoot '.venv\Scripts\python.exe'
$Py       = if (Test-Path $VenvPy) { $VenvPy } else { 'python' }

# UTF-8 everywhere
$env:PYTHONUTF8       = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONPATH       = $RepoRoot

# Single-instance lock
New-Item -ItemType Directory -Force -Path (Split-Path $LockPath -Parent) | Out-Null
if (Test-Path $LockPath) {
    $existing = Get-Content -Path $LockPath -ErrorAction SilentlyContinue
    $pid = ($existing -split '\s+') | Select-Object -First 1
    $alive = $false
    if ($pid -match '^\d+$') {
        try { Get-Process -Id ([int]$pid) -ErrorAction Stop | Out-Null; $alive = $true } catch { $alive = $false }
    }
    if ($alive) { exit 0 } else { Remove-Item -Force $LockPath -ErrorAction SilentlyContinue }
}
"$PID $(Get-Date -Format s)" | Set-Content -Encoding UTF8 $LockPath

# UTF-8 (no BOM) log writer
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$logWriter = New-Object System.IO.StreamWriter($Log, $true, $utf8NoBom)
$logWriter.AutoFlush = $true
function Write-Log([string]$line) { $logWriter.WriteLine($line) }

Write-Log ("[{0}] SERVICE boot" -f (Get-Date).ToString('s'))

try {
    while ($true) {
        Write-Log ("[{0}] SERVICE starting" -f (Get-Date).ToString('s'))
        try {
            & $Py -X utf8 -u -m orchestrator.socket_main 2>&1 | ForEach-Object { Write-Log $_ }
            $code = $LASTEXITCODE
        } catch {
            $code = -1
            $_ | Out-String | ForEach-Object { Write-Log $_ }
        }
        Write-Log ("[{0}] SERVICE exit code={1}" -f (Get-Date).ToString('s'), $code)
        Start-Sleep -Seconds 3
    }
} finally {
    $logWriter.Dispose()
    Remove-Item -Force $LockPath -ErrorAction SilentlyContinue
}
