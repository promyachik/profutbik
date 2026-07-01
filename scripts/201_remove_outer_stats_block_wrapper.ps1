$ErrorActionPreference = "Stop"

$project = "C:\Users\Dmitrii\Promyachik"
Set-Location $project

Write-Host ""
Write-Host "PROFUTBIK 201 - remove outer stats block visual wrapper"
Write-Host "Project: $project"
Write-Host ("Time: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Write-Host ""

$partial = Join-Path $project "layouts\partials\transfer-player-stats.html"
$backupDir = Join-Path $project "_backup_201_remove_outer_stats_block_wrapper"

if (!(Test-Path $partial)) {
    throw "Missing partial: $partial"
}

New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$backupPartial = Join-Path $backupDir "transfer-player-stats_before_201.html"
if (!(Test-Path $backupPartial)) {
    Copy-Item $partial $backupPartial -Force
    Write-Host "Backup saved: _backup_201_remove_outer_stats_block_wrapper\transfer-player-stats_before_201.html"
}

$html = Get-Content $partial -Raw -Encoding UTF8

$marker = "/* 201 remove outer stats block visual wrapper */"

$css = @"

$marker
body.transfer-page #pfb-stats-v184.transfer-stats.pfb-stats-v184,
body.transfer-page #pfb-stats-v184.transfer-stats.pfb-stats-v184.transfer-stats--under-market-chart {
  padding: 0 !important;
  border: 0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  background-image: none !important;
  box-shadow: none !important;
  outline: 0 !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

@media (max-width: 640px) {
  body.transfer-page #pfb-stats-v184.transfer-stats.pfb-stats-v184,
  body.transfer-page #pfb-stats-v184.transfer-stats.pfb-stats-v184.transfer-stats--under-market-chart {
    padding: 0 !important;
    border: 0 !important;
    border-radius: 0 !important;
    background: transparent !important;
    background-image: none !important;
    box-shadow: none !important;
    outline: 0 !important;
  }
}
"@

if ($html -notlike "*$marker*") {
    if ($html -like "*</style>*") {
        $html = $html -replace "</style>", ($css + "`n</style>")
    } else {
        $html = $html + "`n<style>`n" + $css + "`n</style>`n"
    }
    Set-Content -Path $partial -Value $html -Encoding UTF8
    Write-Host "Patched outer wrapper CSS: layouts\partials\transfer-player-stats.html"
} else {
    Write-Host "Patch 201 already exists. No duplicate CSS added."
}

Write-Host ""
Write-Host "Changed visual behavior:"
Write-Host "- removed outer block background/border/shadow/padding"
Write-Host "- kept individual icon cards untouched"
Write-Host "- kept grid/layout untouched"
Write-Host ""
Write-Host "Touched files:"
Write-Host "- layouts\partials\transfer-player-stats.html"
Write-Host ""
Write-Host "NO SITE OPENED."
Write-Host "NO PUSH MADE."
