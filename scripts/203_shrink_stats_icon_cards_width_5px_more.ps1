$ErrorActionPreference = "Stop"

$project = "C:\Users\Dmitrii\Promyachik"
Set-Location $project

Write-Host ""
Write-Host "PROFUTBIK 203 - shrink stats icon cards width 5px more"
Write-Host "Project: $project"
Write-Host ("Time: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Write-Host ""

$partial = Join-Path $project "layouts\partials\transfer-player-stats.html"
$backupDir = Join-Path $project "_backup_203_shrink_stats_icon_cards_width_5px_more"

if (!(Test-Path $partial)) {
    throw "Missing partial: $partial"
}

New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$backupPartial = Join-Path $backupDir "transfer-player-stats_before_203.html"
if (!(Test-Path $backupPartial)) {
    Copy-Item $partial $backupPartial -Force
    Write-Host "Backup saved: _backup_203_shrink_stats_icon_cards_width_5px_more\transfer-player-stats_before_203.html"
}

$html = Get-Content $partial -Raw -Encoding UTF8

$marker = "/* 203 shrink individual stats icon cards width 5px more */"

$css = @"

$marker
body.transfer-page #pfb-stats-v184 .pfb-stats-v184__card {
  width: calc(100% - 9px) !important;
  min-width: 0 !important;
  box-sizing: border-box !important;
  justify-self: center !important;
}
"@

if ($html -notlike "*$marker*") {
    if ($html -like "*</style>*") {
        $idx = $html.LastIndexOf("</style>")
        $html = $html.Substring(0, $idx) + $css + "`n" + $html.Substring($idx)
    } else {
        $html = $html + "`n<style>`n" + $css + "`n</style>`n"
    }

    Set-Content -Path $partial -Value $html -Encoding UTF8
    Write-Host "Patched stats card width CSS: layouts\partials\transfer-player-stats.html"
} else {
    Write-Host "Patch 203 already exists. No duplicate CSS added."
}

Write-Host ""
Write-Host "Changed visual behavior:"
Write-Host "- individual icon cards are 5px narrower than package 202"
Write-Host "- total width reduction is now about 9px"
Write-Host "- height and icons are not changed"
Write-Host "- outer wrapper removal from 201 is not touched"
Write-Host ""
Write-Host "Touched files:"
Write-Host "- layouts\partials\transfer-player-stats.html"
Write-Host ""
Write-Host "NO SITE OPENED."
Write-Host "NO PUSH MADE."
