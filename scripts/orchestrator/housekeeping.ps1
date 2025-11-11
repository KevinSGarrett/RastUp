param(
  [int]$KeepDays = 7
)
Set-Location C:\RastUp\RastUp

# rotate Slack run logs
$logDir = "docs\orchestrator\from-agents\AGENT-1"
if (Test-Path $logDir) {
  Get-ChildItem $logDir -Filter *.log |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$KeepDays) } |
    Remove-Item -Force -ErrorAction SilentlyContinue
}

# archive attach packs older than KeepDays to backup\
$bak = "backup\attachpacks"; New-Item -ItemType Directory -Force -Path $bak | Out-Null
if (Test-Path $logDir) {
  Get-ChildItem $logDir -Filter *-attach.zip |
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$KeepDays) } |
    ForEach-Object {
      Copy-Item $_.FullName -Destination (Join-Path $bak $_.Name) -Force
      Remove-Item $_.FullName -Force
    }
}
Write-Host "Housekeeping done (KeepDays=$KeepDays)" -ForegroundColor Green
