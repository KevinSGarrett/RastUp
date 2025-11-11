param(
  [ValidateSet("start","stop","tail","health","housekeep","queue","sections")]
  [string]$cmd = "health",
  [int]$KeepDays = 7
)

$ErrorActionPreference = "Stop"
Set-Location C:\RastUp\RastUp

function Start-Orch {
  Start-Process powershell.exe `
    -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-NoExit','-File','C:\RastUp\RastUp\scripts\orchestrator\socket_service.ps1' `
    -WindowStyle Normal
}

function Stop-Orch {
  Get-CimInstance Win32_Process |
    Where-Object { $_.CommandLine -like '*-m orchestrator.socket_main*' -or $_.CommandLine -like '*-m orchestrator.app*' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
}

function Tail-Orch {
  Get-Content scripts\orchestrator\app_live.log -Wait -Tail 200
}

function Health-Orch {
  . .\.venv\Scripts\Activate.ps1
  python scripts\orchestrator\report_health.py
  Get-Content docs\orchestrator\HEALTH.md -TotalCount 20
}

function Housekeep-Orch {
  powershell -ExecutionPolicy Bypass -File scripts\orchestrator\housekeeping.ps1 -KeepDays $using:KeepDays
}

function Queue-Orch {
  if (Test-Path ops\queue.jsonl) {
    Write-Host "`nQUEUE:" -ForegroundColor Cyan
    Get-Content ops\queue.jsonl
  } else { Write-Host "QUEUE: (empty)" -ForegroundColor Yellow }
}

function Sections-Orch {
  . .\.venv\Scripts\Activate.ps1
  python scripts\blueprints\build_sections.py
  ($s = Get-Content docs\blueprints\sections.json -Raw | ConvertFrom-Json) | `
    Where-Object { $_.kind -eq 'NT' } | Select-Object -First 5 id,title
}

switch ($cmd) {
  "start"     { Start-Orch }
  "stop"      { Stop-Orch }
  "tail"      { Tail-Orch }
  "health"    { Health-Orch }
  "housekeep" { Housekeep-Orch }
  "queue"     { Queue-Orch }
  "sections"  { Sections-Orch }
  default     { Health-Orch }
}

function Sync-Orch {
  . .\.venv\Scripts\Activate.ps1
  python scripts\orchestrator\sync_budget.py
  Get-Content docs\orchestrator\SUMMARY.md -TotalCount 16
}

function Audit-Orch {
  . .\.venv\Scripts\Activate.ps1
  python scripts\orchestrator\audit_rollup.py
  Get-Content docs\orchestrator\AUDIT.jsonl -Tail 12
}
