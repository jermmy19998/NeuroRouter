param(
    [Parameter(Mandatory = $true)]
    [string]$ImagePath,

    [Parameter(Mandatory = $false)]
    [string]$Instruction = "help me use resnet to classify this image",

    [Parameter(Mandatory = $false)]
    [string]$Model = "",

    [Parameter(Mandatory = $false)]
    [int]$TopK = 5,

    [Parameter(Mandatory = $false)]
    [string]$Endpoint = "http://127.0.0.1:8000/api/v1/classify"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $ImagePath)) {
    throw "Image file not found: $ImagePath"
}

$form = @{
    image       = Get-Item $ImagePath
    instruction = $Instruction
    top_k       = $TopK
}

if (-not [string]::IsNullOrWhiteSpace($Model)) {
    $form["model"] = $Model
}

$response = Invoke-RestMethod -Method Post -Uri $Endpoint -Form $form
$response | ConvertTo-Json -Depth 8

