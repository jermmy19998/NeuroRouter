param(
    [Parameter(Mandatory = $false)]
    [string]$Host = "127.0.0.1",

    [Parameter(Mandatory = $false)]
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$setupScript = Join-Path $PSScriptRoot "setup-local.ps1"
$startScript = Join-Path $PSScriptRoot "start-local.ps1"

& $setupScript
& $startScript -Host $Host -Port $Port -Detach

Write-Host "NeuroRouter is ready at http://$Host`:$Port"
Write-Host "Test with: .\\scripts\\infer-local.ps1 -ImagePath .\\your-image.jpg -Instruction '帮我用resnet分类这个图像'"

