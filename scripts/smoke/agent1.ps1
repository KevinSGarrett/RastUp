# Requires CRLF endings
$ErrorActionPreference = "Stop"

$Root   = (Resolve-Path "$PSScriptRoot\..\..").Path
$Report = Join-Path $Root "docs\test-reports\smoke"
New-Item -ItemType Directory -Force -Path $Report | Out-Null
$Log    = Join-Path $Report "agent1-windows.log"

$lines  = New-Object System.Collections.Generic.List[string]
$lines.Add("== Agent-1 Smoke (Windows) ==")
$lines.Add("UTC: " + [DateTime]::UtcNow.ToString("o"))
$lines.Add("ROOT=$Root")
$lines.Add("")

# Local FS
try {
  $tmp = Join-Path $Root ".tmp.smoke.$PID"
  "ok" | Set-Content -Encoding UTF8 $tmp
  Remove-Item -Force $tmp
  $lines.Add("PASS: local fs write")
} catch {
  $lines.Add("FAIL: local fs write/delete — $($_.Exception.Message)")
}

# Python
try {
  $pyVer = (& python --version) 2>&1
  if ($LASTEXITCODE -eq 0) {
    $lines.Add("python: $($pyVer.Trim())")
    $lines.Add("PASS: python present")
  } else {
    $lines.Add("WARN: python not present")
  }
} catch {
  $lines.Add("WARN: python not present")
}

# Git
try {
  $gitVer = (& git --version) 2>&1
  if ($LASTEXITCODE -eq 0) {
    $lines.Add("git: $($gitVer.Trim())")
  } else {
    $lines.Add("WARN: git not present")
  }
} catch { $lines.Add("WARN: git not present") }

# Docker Desktop (Windows engine)
try {
  $dv = (& docker version) 2>&1
  if ($LASTEXITCODE -eq 0) {
    $lines.Add("docker: " + ($dv | Select-String -Pattern "Version:" | Select-Object -First 1).ToString().Trim())
    $lines.Add("PASS: docker usable (Windows)")
  } else {
    $lines.Add("WARN: docker not usable on Windows")
  }
} catch {
  $lines.Add("WARN: docker not present on Windows")
}

$lines.Add("")
$lines.Add("SMOKE DONE")
$lines | Set-Content -Encoding UTF8 $Log
$Log
