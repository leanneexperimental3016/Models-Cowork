param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$targets = @(
    (Join-Path $env:USERPROFILE 'plugins\model-cowork'),
    (Join-Path $env:USERPROFILE '.claude\model-cowork'),
    (Join-Path $env:USERPROFILE '.claude\skills\model-cowork'),
    (Join-Path $env:USERPROFILE '.copilot\skills\model-cowork'),
    (Join-Path $env:USERPROFILE '.gemini\config\plugins\model-cowork'),
    (Join-Path $env:USERPROFILE '.model-cowork\ollama')
)
foreach ($target in $targets) {
    if ((Test-Path -LiteralPath $target) -and (Test-Path -LiteralPath (Join-Path $target '.model-cowork-owned'))) {
        if (-not $DryRun) { Remove-Item -LiteralPath $target -Recurse -Force }
        Write-Output "removed $target"
    }
}
$files = @(
    (Join-Path $env:USERPROFILE '.claude\commands\model-cowork.md'),
    (Join-Path $env:USERPROFILE '.copilot\agents\model-cowork.agent.md'),
    (Join-Path $env:USERPROFILE '.copilot\agents\model-cowork-fast.agent.md'),
    (Join-Path $env:USERPROFILE '.copilot\agents\model-cowork-reviewer.agent.md')
)
$files += Get-ChildItem -LiteralPath (Join-Path $env:USERPROFILE '.claude\agents') -Filter 'model-cowork-*.md' -File -ErrorAction SilentlyContinue | ForEach-Object FullName
foreach ($file in $files | Select-Object -Unique) {
    if (Test-Path -LiteralPath $file) {
        if (-not $DryRun) { Remove-Item -LiteralPath $file -Force }
        Write-Output "removed $file"
    }
}
Write-Output 'Marketplace entry and backups are retained to avoid destructive shared-config edits.'

