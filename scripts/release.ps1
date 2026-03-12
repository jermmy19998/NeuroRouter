param(
    [Parameter(Mandatory = $true)]
    [string]$Version,

    [Parameter(Mandatory = $false)]
    [string]$Title = "",

    [Parameter(Mandatory = $false)]
    [string]$Notes = ""
)

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git is required."
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "gh CLI is required to publish GitHub releases."
}

git add -A
git commit -m "release: v$Version"
git tag "v$Version"
git push origin HEAD
git push origin "v$Version"

if ([string]::IsNullOrWhiteSpace($Title)) {
    $Title = "v$Version"
}

gh release create "v$Version" --title $Title --notes $Notes
Write-Host "Release v$Version created."

