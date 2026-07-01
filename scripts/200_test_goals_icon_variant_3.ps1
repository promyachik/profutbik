$ErrorActionPreference = "Stop"

$project = "C:\Users\Dmitrii\Promyachik"
Set-Location $project

Write-Host ""
Write-Host "PROFUTBIK 200 - test goals icon variant 3"
Write-Host "Project: $project"
Write-Host ("Time: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Write-Host ""

$targetPng = Join-Path $project "static\images\stats-icons-v184\goals.png"
$sourcePng = Join-Path $project "payload\200\goals_variant_3.png"
$partial = Join-Path $project "layouts\partials\transfer-player-stats.html"
$backupDir = Join-Path $project "_backup_200_test_goals_icon_variant_3"

if (!(Test-Path $sourcePng)) { throw "Missing package payload: $sourcePng" }
if (!(Test-Path $targetPng)) { throw "Missing target icon: $targetPng" }
if (!(Test-Path $partial)) { throw "Missing partial: $partial" }

New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$backupPng = Join-Path $backupDir "goals_before_200.png"
$backupPartial = Join-Path $backupDir "transfer-player-stats_before_200.html"

if (!(Test-Path $backupPng)) {
    Copy-Item $targetPng $backupPng -Force
    Write-Host "Backup saved: _backup_200_test_goals_icon_variant_3\goals_before_200.png"
}
if (!(Test-Path $backupPartial)) {
    Copy-Item $partial $backupPartial -Force
    Write-Host "Backup saved: _backup_200_test_goals_icon_variant_3\transfer-player-stats_before_200.html"
}

Copy-Item $sourcePng $targetPng -Force
Write-Host "Copied TEST variant 3 to: static\images\stats-icons-v184\goals.png"

$html = Get-Content $partial -Raw -Encoding UTF8
$html = [regex]::Replace(
    $html,
    'goals\.png"\s*\|\s*relURL\s*\}\}\?v=\d+',
    'goals.png" | relURL }}?v=200'
)

$marker = "/* 200 test goals icon variant 3 no crop */"
$css = @"

$marker
body.transfer-page #pfb-stats-v184 .pfb-stats-v184__goals,
body.transfer-page #pfb-stats-v184 .pfb-stats-v184__goals *,
body.transfer-page #pfb-stats-v184 .pfb-stats-v184__goals .pfb-stats-v184__icon {
  overflow: visible !important;
  clip-path: none !important;
  -webkit-clip-path: none !important;
  mask: none !important;
  -webkit-mask: none !important;
}

body.transfer-page #pfb-stats-v184 .pfb-stats-v184__goals .pfb-stats-v184__icon {
  width: 72px !important;
  height: 72px !important;
  max-width: 72px !important;
  max-height: 72px !important;
  object-fit: contain !important;
  object-position: center center !important;
  transform: translateX(-1px) !important;
}
"@

if ($html -notlike "*$marker*") {
    if ($html -like "*</style>*") {
        $html = $html -replace "</style>", ($css + "`n</style>")
    } else {
        $html = $html + "`n<style>`n" + $css + "`n</style>`n"
    }
}

Set-Content -Path $partial -Value $html -Encoding UTF8

Write-Host "Patched cache/CSS to v200: layouts\partials\transfer-player-stats.html"
Write-Host ""
Write-Host "Touched files:"
Write-Host "- static\images\stats-icons-v184\goals.png"
Write-Host "- layouts\partials\transfer-player-stats.html"
Write-Host ""
Write-Host "NO SITE OPENED."
Write-Host "NO PUSH MADE."
