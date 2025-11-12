# scripts/orchestrator/start_bolt.ps1
# Starts the quiet background service in a new window.

#requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = $PSScriptRoot
$RepoRoot  = (Resolve-Path (Join-Path $ScriptDir '..\..')).Path
$Svc       = Join-Path $ScriptDir 'socket_service.ps1'

Start-Process powershell.exe -ArgumentList @(
  '-NoProfile','-ExecutionPolicy','Bypass','-NoExit','-File', $Svc
) -WorkingDirectory $RepoRoot -WindowStyle Normal
