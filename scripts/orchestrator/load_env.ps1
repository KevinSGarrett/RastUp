# scripts/orchestrator/load_env.ps1  (UTF-8, CRLF)
# Ensure UTF-8 and surface a minimal masked preview.
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
[Environment]::SetEnvironmentVariable("PYTHONUTF8","1","Process")
function Mask([string]$s, [int]$n=6){ if([string]::IsNullOrEmpty($s)){"(unset)"} else {$s.Substring(0,[Math]::Min($n,$s.Length))+"…"} }
"WIN env masks: OPENAI=$(Mask $env:OPENAI_API_KEY)  ANTH=$(Mask $env:ANTHROPIC_API_KEY)  CUR=$(Mask $env:CURSOR_API_KEY)  SLB=$(Mask $env:SLACK_BOT_TOKEN)"
