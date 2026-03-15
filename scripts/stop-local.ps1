param()

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$pidFile = Join-Path $repoRoot ".neurorouter\\neurorouter.pid"

if (-not (Test-Path $pidFile)) {
    Write-Host "No PID file found. Service may already be stopped."
    exit 0
}

$pid = Get-Content $pidFile -ErrorAction SilentlyContinue
if (-not $pid) {
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    Write-Host "PID file was empty and has been removed."
    exit 0
}

$process = Get-Process -Id $pid -ErrorAction SilentlyContinue
if (-not $process) {
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    Write-Host "Process $pid not found. Removed stale PID file."
    exit 0
}

Stop-Process -Id $pid -Force
Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
Write-Host "Stopped NeuroRouter process $pid"

