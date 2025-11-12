# Orchestrator Agent-1 smoke (Windows PowerShell 5.1+ compatible)
$ErrorActionPreference = 'Stop'

# Resolve repo root from this script's location
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir  # scripts/smoke -> scripts
$Root = Split-Path -Parent $Root       # scripts -> repo root

$ReportDir = Join-Path $Root 'docs\test-reports\smoke'
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null
$Log = Join-Path $ReportDir 'agent1-windows.log'

function Write-Log($Text) { $Text | Out-File -FilePath $Log -Append -Encoding UTF8 }

"== Agent-1 Smoke (Windows) ==" | Out-File -FilePath $Log -Encoding UTF8
Write-Log ("UTC: " + ([DateTime]::UtcNow.ToString("s") + "Z"))
Write-Log ("ROOT=" + $Root)
Write-Log ""

# Local FS write (hard PASS)
try {
  $Tmp = Join-Path $ScriptDir ("_smoke_write_test." + (Get-Random) + ".txt")
  "ok" | Out-File -FilePath $Tmp -Encoding UTF8
  Remove-Item -Force $Tmp
  Write-Log "PASS: local fs write"
} catch {
  Write-Log ("FAIL: local fs write: " + $_.Exception.Message)
  $Log
  exit 1
}

# Python version (optional)
try {
  $py = (& python --version) 2>&1
  Write-Log ("python: " + $py)
} catch {
  Write-Log "WARN: python not found on PATH"
}

# Git version (optional)
if (Get-Command git -ErrorAction SilentlyContinue) {
  $gv = (& git --version) 2>&1
  Write-Log ("git: " + $gv)
} else {
  Write-Log "WARN: git not found"
}

# Docker presence (optional)
if (Get-Command docker -ErrorAction SilentlyContinue) {
  try {
    $dv = (& docker --version) 2>&1
    Write-Log ("PASS: docker present - " + $dv)
  } catch {
    Write-Log "WARN: docker CLI present but not responding"
  }
} else {
  Write-Log "WARN: docker not present"
}

Write-Log ""
Write-Log "SMOKE DONE"

# Print the log path so humans/CI can find it
$Log
