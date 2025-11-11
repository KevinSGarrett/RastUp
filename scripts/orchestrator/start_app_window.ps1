cd C:\RastUp\RastUp
$cmd = ''cd C:\RastUp\RastUp; . .\.venv\Scripts\Activate.ps1; $env:SLACK_LOG="debug"; $env:PYTHONUNBUFFERED="1"; python -X dev -u -m orchestrator.app''
Start-Process powershell.exe -ArgumentList ''-NoExit'',''-Command'', $cmd
