# Agent-1 local smoke (Windows PowerShell 5+ compatible)
# Writes: docs\test-reports\smoke\agent1-windows.log

$ErrorActionPreference = "Stop"

# Repo root
$root = (Resolve-Path "$PSScriptRoot\..\..").Path
Set-Location $root

# Log target
$reportDir = Join-Path $root "docs\test-reports\smoke"
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$log = Join-Path $reportDir "agent1-windows.log"

# Collect lines
$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("== Agent-1 Smoke (Windows) ==")
$lines.Add("date: $((Get-Date).ToUniversalTime().ToString('o'))")
$lines.Add("root: $root")

# Local FS write/delete
try {
  $tmp = Join-Path $root ".tmp.agent1.smoke.txt"
  "ok $((Get-Date).ToUniversalTime().ToString('o'))" | Set-Content -Encoding UTF8 $tmp
  Remove-Item -Force $tmp
  $lines.Add("PASS: local fs write/delete")
} catch {
  $lines.Add("FAIL: local fs write/delete — $($_.Exception.Message)")
}

# Python presence
try {
  $pyVer = (& python --version) 2>&1
  if ($LASTEXITCODE -eq 0) {
    $lines.Add($pyVer.Trim())
    $lines.Add("PASS: python present")
  } else {
    $lines.Add("WARN: python not present")
  }
} catch {
  $lines.Add("WARN: python not present")
}

# Docker presence (optional)
try {
  & docker --version *> $null
  if ($LASTEXITCODE -eq 0) {
    $lines.Add("PASS: docker present")
  } else {
    $lines.Add("WARN: docker not present")
  }
} catch {
  $lines.Add("WARN: docker not present")
}

# Write log + echo path
$lines | Set-Content -Encoding UTF8 $log
Write-Host $log
