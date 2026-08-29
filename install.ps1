param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$suite = Split-Path -Parent $MyInvocation.MyCommand.Path
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path $env:USERPROFILE ".model-cowork\backups\$stamp"
$report = [ordered]@{ timestamp = $stamp; dryRun = [bool]$DryRun; installed = @(); backups = @(); warnings = @() }

function Copy-OwnedDirectory([string]$source, [string]$target) {
    if (Test-Path -LiteralPath $target) {
        $relative = $target.Replace($env:USERPROFILE, '').TrimStart('\')
        $backup = Join-Path $backupRoot $relative
        $report.backups += $backup
        if (-not $DryRun) {
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $backup) | Out-Null
            Copy-Item -LiteralPath $target -Destination $backup -Recurse -Force
            Remove-Item -LiteralPath $target -Recurse -Force
        }
    }
    $report.installed += $target
    if (-not $DryRun) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
        Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
        New-Item -ItemType File -Force -Path (Join-Path $target '.model-cowork-owned') | Out-Null
    }
}

function Copy-OwnedFile([string]$source, [string]$target) {
    if (Test-Path -LiteralPath $target) {
        $relative = $target.Replace($env:USERPROFILE, '').TrimStart('\')
        $backup = Join-Path $backupRoot $relative
        $report.backups += $backup
        if (-not $DryRun) {
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $backup) | Out-Null
            Copy-Item -LiteralPath $target -Destination $backup -Force
        }
    }
    $report.installed += $target
    if (-not $DryRun) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target) | Out-Null
        Copy-Item -LiteralPath $source -Destination $target -Force
    }
}

# Codex editable plugin and personal marketplace.
$codexSource = Join-Path $suite 'packs\codex\model-cowork'
$codexTarget = Join-Path $env:USERPROFILE 'plugins\model-cowork'
Copy-OwnedDirectory $codexSource $codexTarget
$marketplace = Join-Path $env:USERPROFILE '.agents\plugins\marketplace.json'
$report.installed += $marketplace
if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $marketplace) | Out-Null
    if (Test-Path -LiteralPath $marketplace) {
        $backup = Join-Path $backupRoot '.agents\plugins\marketplace.json'
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $backup) | Out-Null
        Copy-Item -LiteralPath $marketplace -Destination $backup -Force
        $report.backups += $backup
        $catalog = Get-Content -Raw -LiteralPath $marketplace | ConvertFrom-Json
    } else {
        $catalog = [pscustomobject]@{ name = 'personal'; interface = [pscustomobject]@{ displayName = 'Personal' }; plugins = @() }
    }
    if (-not $catalog.name -or $catalog.name -notmatch '^[A-Za-z0-9_-]+$') { throw 'Invalid personal marketplace name.' }
    $entry = [pscustomobject]@{
        name = 'model-cowork'
        source = [pscustomobject]@{ source = 'local'; path = './plugins/model-cowork' }
        policy = [pscustomobject]@{ installation = 'AVAILABLE'; authentication = 'ON_INSTALL' }
        category = 'Developer Tools'
    }
    $others = @($catalog.plugins | Where-Object { $_.name -ne 'model-cowork' })
    $catalog.plugins = @($others + $entry)
    $marketplaceJson = $catalog | ConvertTo-Json -Depth 20
    [System.IO.File]::WriteAllText($marketplace, $marketplaceJson, [System.Text.UTF8Encoding]::new($false))
}

# Claude Code: editable source plus directly discovered skill, agents, and command.
$claudeSource = Join-Path $suite 'packs\claude\model-cowork'
Copy-OwnedDirectory $claudeSource (Join-Path $env:USERPROFILE '.claude\model-cowork')
Copy-OwnedDirectory (Join-Path $claudeSource 'skills\model-cowork') (Join-Path $env:USERPROFILE '.claude\skills\model-cowork')
Get-ChildItem -LiteralPath (Join-Path $claudeSource 'agents') -File | ForEach-Object { Copy-OwnedFile $_.FullName (Join-Path $env:USERPROFILE ".claude\agents\$($_.Name)") }
Copy-OwnedFile (Join-Path $claudeSource 'commands\model-cowork.md') (Join-Path $env:USERPROFILE '.claude\commands\model-cowork.md')

# Copilot personal agent-skill and custom agent profiles.
$copilotSource = Join-Path $suite 'packs\copilot\model-cowork\.github'
Copy-OwnedDirectory (Join-Path $copilotSource 'skills\model-cowork') (Join-Path $env:USERPROFILE '.copilot\skills\model-cowork')
Get-ChildItem -LiteralPath (Join-Path $copilotSource 'agents') -File | ForEach-Object { Copy-OwnedFile $_.FullName (Join-Path $env:USERPROFILE ".copilot\agents\$($_.Name)") }

# Antigravity native plugin location detected on Windows.
Copy-OwnedDirectory (Join-Path $suite 'packs\antigravity\model-cowork') (Join-Path $env:USERPROFILE '.gemini\config\plugins\model-cowork')

# Ollama adapter; Ollama itself is optional and discovered at runtime.
Copy-OwnedDirectory (Join-Path $suite 'packs\ollama\model-cowork') (Join-Path $env:USERPROFILE '.model-cowork\ollama')

$commands = 'codex', 'claude', 'copilot', 'agy', 'ollama'
foreach ($command in $commands) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) { $report.warnings += "$command executable not found on PATH; its pack was installed but runtime verification is pending." }
}
if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path (Join-Path $env:USERPROFILE '.model-cowork') | Out-Null
    $reportPath = Join-Path $env:USERPROFILE '.model-cowork\install-report.json'
    [System.IO.File]::WriteAllText($reportPath, ($report | ConvertTo-Json -Depth 10), [System.Text.UTF8Encoding]::new($false))
}
$report | ConvertTo-Json -Depth 10
