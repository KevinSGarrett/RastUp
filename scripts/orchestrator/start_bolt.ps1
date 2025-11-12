Set-StrictMode -Version Latest
Set-Location C:\RastUp\RastUp
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "C:\RastUp\RastUp"

# Optional: show config debug
$env:RU_CONFIG_DEBUG = "1"

# Load .env into THIS process if present (shell vars still win inside config)
if (Test-Path .env) {
  Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*#|^\s*$') { return }
    if ($_ -match '^\s*([A-Za-z_]\w*)\s*=\s*(.*)\s*$') {
      $name = $matches[1]
      $val  = $matches[2].Trim()
      if ($val.StartsWith('"') -and $val.EndsWith('"')) { $val = $val.Substring(1,$val.Length-2) }
      if ($val.StartsWith("'") -and $val.EndsWith("'")) { $val = $val.Substring(1,$val.Length-2) }
      [Environment]::SetEnvironmentVariable($name,$val,"Process")
    }
  }
}

& .\.venv\Scripts\python.exe -m orchestrator.socket_main
