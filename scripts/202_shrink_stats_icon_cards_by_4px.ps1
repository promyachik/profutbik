$ErrorActionPreference = "Stop"

$project = "C:\Users\Dmitrii\Promyachik"
Set-Location $project

Write-Host ""
Write-Host "PROFUTBIK 202 - shrink stats icon cards by 4px"
Write-Host "Project: $project"
Write-Host ("Time: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Write-Host ""

$partial = Join-Path $project "layouts\partials\transfer-player-stats.html"
$backupDir = Join-Path $project "_backup_202_shrink_stats_icon_cards_by_4px"

if (!(Test-Path $partial)) {
    throw "Missing partial: $partial"
}

New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$backupPartial = Join-Path $backupDir "transfer-player-stats_before_202.html"
if (!(Test-Path $backupPartial)) {
    Copy-Item $partial $backupPartial -Force
    Write-Host "Backup saved: _backup_202_shrink_stats_icon_cards_by_4px\transfer-player-stats_before_202.html"
}

$html = Get-Content $partial -Raw -Encoding UTF8

$marker = "/* 202 shrink individual stats icon cards by 4px */"

$css = @"

$marker
body.transfer-page #pfb-stats-v184 .pfb-stats-v184__card {
  width: calc(100% - 4px) !important;
  min-width: 0 !important;
  min-height: calc(100% - 4px) !important;
  box-sizing: border-box !important;
  justify-self: center !important;
  align-self: center !important;
}

body.transfer-page #pfb-stats-v184 .pfb-stats-v184__grid,
body.transfer-page #pfb-stats-v184 .pfb-stats-v184__row {
  justify-items: center !important;
  align-items: center !important;
}
"@

if ($html -notlike "*$marker*") {
    if ($html -like "*</style>*") {
        $html = $html -replace "</style>", ($css + "`n</style>")
    } else {
        $html = $html + "`n<style>`n" + $css + "`n</style>`n"
    }

    Set-Content -Path $partial -Value $html -Encoding UTF8
    Write-Host "Patched stats card size CSS: layouts\partials\transfer-player-stats.html"
} else {
    Write-Host "Patch 202 already exists. No duplicate CSS added."
}

Write-Host ""
Write-Host "Changed visual behavior:"
Write-Host "- individual icon cards are visually 4px narrower"
Write-Host "- cards are kept centered in their grid cells"
Write-Host "- icons themselves are not resized"
Write-Host "- outer wrapper removal from 201 is not touched"
Write-Host ""
Write-Host "Touched files:"
Write-Host "- layouts\partials\transfer-player-stats.html"
Write-Host ""
Write-Host "NO SITE OPENED."
Write-Host "NO PUSH MADE."
