param(
    [Parameter(Mandatory = $false)]
    [switch]$SkipTests,

    [Parameter(Mandatory = $false)]
    [switch]$SkipModelWarmup
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPath = Join-Path $repoRoot ".venv"
$pythonExe = Join-Path $venvPath "Scripts\\python.exe"
$hfCache = Join-Path $repoRoot ".hf_cache"

Write-Host "[1/6] Checking Python..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    throw "Python 3.11+ is required. Install Python and re-run this script."
}

$pythonVersion = (& python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if (-not $pythonVersion) {
    throw "Cannot read Python version."
}
$versionParts = $pythonVersion.Split(".")
if ([int]$versionParts[0] -lt 3 -or ([int]$versionParts[0] -eq 3 -and [int]$versionParts[1] -lt 11)) {
    throw "Python 3.11+ is required. Current version: $pythonVersion"
}

Write-Host "[2/6] Creating virtual environment if missing..."
if (-not (Test-Path $pythonExe)) {
    & python -m venv $venvPath
}

Write-Host "[3/6] Upgrading pip and setuptools..."
& $pythonExe -m pip install --upgrade pip setuptools wheel

Write-Host "[4/6] Installing project dependencies..."
& $pythonExe -m pip install -e "$repoRoot[dev]"

Write-Host "[5/6] Preparing local model cache..."
if (-not (Test-Path $hfCache)) {
    New-Item -ItemType Directory -Path $hfCache | Out-Null
}
$env:HF_HOME = $hfCache
$env:TRANSFORMERS_CACHE = (Join-Path $hfCache "transformers")
$env:HF_HUB_CACHE = (Join-Path $hfCache "hub")

if (-not $SkipModelWarmup) {
    & $pythonExe (Join-Path $repoRoot "scripts\\warmup_model.py") --model-id "microsoft/resnet-18"
}

Write-Host "[6/6] Running tests..."
if (-not $SkipTests) {
    $env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
    & $pythonExe -m pytest -q
}

Write-Host "Setup complete. Start service with: .\\scripts\\start-local.ps1"

