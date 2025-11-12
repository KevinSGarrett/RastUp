Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

Write-Host "[smoke] repo: $(Get-Location | Select-Object -ExpandProperty Path)"

$safeFlag = Join-Path "ops" "flags" "safe-mode.json"

Write-Host "[smoke] audit (non-strict)"
python -m orchestrator.knowledge audit | Out-Host

if (Test-Path $safeFlag) {
  Write-Host "[smoke] SAFE-MODE detected -> skip build"
} else {
  Write-Host "[smoke] build (if needed)"
  try { python -m orchestrator.knowledge build | Out-Host } catch { }
}

Write-Host "[smoke] query: acceptance criteria"
try { python -m orchestrator.knowledge query --text "acceptance criteria" --k 3 --json | Out-Host } catch { }

Write-Host "[smoke] done"
