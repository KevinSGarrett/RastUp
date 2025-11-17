Write-Host "Checking Docker access..."
docker version 2>$null
if ($LASTEXITCODE -ne 0) {
  Write-Host "Docker NOT available or not running."
} else {
  Write-Host "Docker is available."
}
