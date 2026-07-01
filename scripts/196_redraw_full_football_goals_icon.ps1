$ErrorActionPreference = "Stop"

$project = "C:\Users\Dmitrii\Promyachik"
Set-Location $project

Write-Host ""
Write-Host "PROFUTBIK 196 - redraw full football goals icon"
Write-Host "Project: $project"
Write-Host ("Time: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Write-Host ""

$targetPng = Join-Path $project "static\images\stats-icons-v184\goals.png"
$sourcePng = Join-Path $project "payload\196\goals.png"
$partial = Join-Path $project "layouts\partials\transfer-player-stats.html"
$backupDir = Join-Path $project "_backup_196_redraw_full_football_goals_icon"

if (!(Test-Path $sourcePng)) {
    throw "Missing package payload: $sourcePng"
}

if (!(Test-Path $targetPng)) {
    throw "Missing target icon: $targetPng"
}

if (!(Test-Path $partial)) {
    throw "Missing partial: $partial"
}

New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$backupPng = Join-Path $backupDir "goals_before_196.png"
$backupPartial = Join-Path $backupDir "transfer-player-stats_before_196.html"

if (!(Test-Path $backupPng)) {
    Copy-Item $targetPng $backupPng -Force
    Write-Host "Backup saved: _backup_196_redraw_full_football_goals_icon\goals_before_196.png"
}

if (!(Test-Path $backupPartial)) {
    Copy-Item $partial $backupPartial -Force
    Write-Host "Backup saved: _backup_196_redraw_full_football_goals_icon\transfer-player-stats_before_196.html"
}

Copy-Item $sourcePng $targetPng -Force
Write-Host "Copied redrawn full football icon to: static\images\stats-icons-v184\goals.png"

$html = Get-Content $partial -Raw -Encoding UTF8

$html = [regex]::Replace(
    $html,
    'goals\.png"\s*\|\s*relURL\s*\}\}\?v=\d+',
    'goals.png" | relURL }}?v=196'
)

$marker = "/* 196 redrawn football goals icon no crop */"
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

Write-Host "Patched partial CSS/cache: layouts\partials\transfer-player-stats.html"
Write-Host ""
Write-Host "Touched files:"
Write-Host "- layouts\partials\transfer-player-stats.html"
Write-Host "- static\images\stats-icons-v184\goals.png"
Write-Host ""
Write-Host "DONE 196. Open De Ligt page and press Ctrl+F5."
