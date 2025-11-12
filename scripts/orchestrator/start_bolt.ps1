# scripts/orchestrator/start_bolt.ps1
# Starts the quiet service runner in a new window.

#requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptRoot = $PSScriptRoot
$RepoRoot   = (Resolve-Path "$ScriptRoot\..\..").Path
$svc        = Join-Path $ScriptRoot 'socket_service.ps1'

Start-Process powershell.exe -ArgumentList @(
  '-NoProfile','-ExecutionPolicy','Bypass','-NoExit','-File', $svc
) -WorkingDirectory $RepoRoot -WindowStyle Normal
