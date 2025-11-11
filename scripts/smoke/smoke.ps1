Write-Host "SMOKE: pwd"
Get-Location | Select-Object -ExpandProperty Path
Write-Host "SMOKE: list repo root"
Get-ChildItem -Force | Select-Object Name,Length,LastWriteTime
