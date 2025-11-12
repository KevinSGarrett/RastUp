# Smoke Tests

## Windows
```powershell
powershell -ExecutionPolicy Bypass -File scripts\smoke\agent1.ps1
Get-Content .\docs\test-reports\smoke\agent1-windows.log
