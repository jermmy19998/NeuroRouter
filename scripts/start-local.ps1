param(
    [Parameter(Mandatory = $false)]
    [string]$Host = "127.0.0.1",

    [Parameter(Mandatory = $false)]
    [int]$Port = 8000,

    [Parameter(Mandatory = $false)]
    [switch]$Detach
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPython = Join-Path $repoRoot ".venv\\Scripts\\python.exe"
$runDir = Join-Path $repoRoot ".neurorouter"
$pidFile = Join-Path $runDir "neurorouter.pid"
$logFile = Join-Path $runDir "neurorouter.log"
$srcPath = Join-Path $repoRoot "src"
$hfCache = Join-Path $repoRoot ".hf_cache"

if (-not (Test-Path $venvPython)) {
    throw "Virtual environment not found. Run .\\scripts\\setup-local.ps1 first."
}

if (-not (Test-Path $runDir)) {
    New-Item -ItemType Directory -Path $runDir | Out-Null
}
if (-not (Test-Path $hfCache)) {
    New-Item -ItemType Directory -Path $hfCache | Out-Null
}

$env:PYTHONPATH = $srcPath
$env:HF_HOME = $hfCache
$env:TRANSFORMERS_CACHE = (Join-Path $hfCache "transformers")
$env:HF_HUB_CACHE = (Join-Path $hfCache "hub")

$arguments = @(
    "-m", "uvicorn",
    "neurorouter.main:app",
    "--host", $Host,
    "--port", $Port
)

if ($Detach) {
    $existingPid = $null
    if (Test-Path $pidFile) {
        $existingPid = Get-Content $pidFile -ErrorAction SilentlyContinue
    }
    if ($existingPid) {
        $process = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "NeuroRouter already running with PID $existingPid"
            exit 0
        }
    }

    $process = Start-Process -FilePath $venvPython -ArgumentList $arguments -RedirectStandardOutput $logFile -RedirectStandardError $logFile -PassThru
    Set-Content -Path $pidFile -Value $process.Id
    Write-Host "NeuroRouter started in background. PID: $($process.Id)"
    Write-Host "Log file: $logFile"
    Write-Host "Health check: http://$Host`:$Port/api/v1/health"
    exit 0
}

Write-Host "Starting NeuroRouter in foreground at http://$Host`:$Port ..."
& $venvPython @arguments

