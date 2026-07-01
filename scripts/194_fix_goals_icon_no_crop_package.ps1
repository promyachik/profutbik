$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Resolve-Path (Join-Path $ScriptDir "..")
Set-Location $Root

$Png = Join-Path $Root "static\images\stats-icons-v184\goals.png"
$Payload = Join-Path $Root "payload\194\goals_clean_full.png"
$Partial = Join-Path $Root "layouts\partials\transfer-player-stats.html"
$BackupDir = Join-Path $Root "_backup_194_fix_goals_icon_no_crop"
$Report = Join-Path $Root "_194_goals_icon_fix_report.txt"

function Write-Log($Text) {
  Write-Host $Text
  Add-Content -Path $Report -Value $Text -Encoding UTF8
}

if (Test-Path $Report) { Remove-Item $Report -Force }
Write-Log "PROFUTBIK 194 - goals icon no crop package"
Write-Log "Project: $Root"
Write-Log "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Log ""

if (!(Test-Path $Payload)) {
  throw "Payload icon not found: $Payload"
}

$PngDir = Split-Path -Parent $Png
if (!(Test-Path $PngDir)) {
  New-Item -ItemType Directory -Path $PngDir -Force | Out-Null
}

if (!(Test-Path $BackupDir)) {
  New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
}

if (Test-Path $Png) {
  Copy-Item $Png (Join-Path $BackupDir "goals_before_194.png") -Force
  Write-Log "Backup saved: _backup_194_fix_goals_icon_no_crop\goals_before_194.png"
} else {
  Write-Log "WARNING: old goals.png was not found; creating it from payload."
}

if (Test-Path $Partial) {
  Copy-Item $Partial (Join-Path $BackupDir "transfer-player-stats_before_194.html") -Force
  Write-Log "Backup saved: _backup_194_fix_goals_icon_no_crop\transfer-player-stats_before_194.html"
} else {
  Write-Log "WARNING: partial not found: layouts\partials\transfer-player-stats.html"
}

Copy-Item $Payload $Png -Force
Write-Log "Copied clean full-canvas icon to: static\images\stats-icons-v184\goals.png"

# Cache-bust every direct goals.png reference in likely site files.
$PatchRoots = @()
if (Test-Path (Join-Path $Root "layouts")) { $PatchRoots += (Join-Path $Root "layouts") }
if (Test-Path (Join-Path $Root "static")) { $PatchRoots += (Join-Path $Root "static") }

$TouchedFiles = New-Object System.Collections.Generic.List[string]
foreach ($PatchRoot in $PatchRoots) {
  Get-ChildItem -Path $PatchRoot -Recurse -File -Include *.html,*.css,*.js,*.toml,*.md | ForEach-Object {
    $File = $_.FullName
    $Text = Get-Content -Path $File -Raw -Encoding UTF8
    if ($Text -match "goals\.png") {
      $NewText = [regex]::Replace($Text, 'goals\.png("\s*\|\s*relURL\s*\}\})(\?v=\d+)?', 'goals.png$1?v=194')
      $NewText = [regex]::Replace($NewText, 'goals\.png(\?v=\d+)?', 'goals.png?v=194')
      # Undo accidental double query if a template replacement and plain replacement both touched it.
      $NewText = $NewText.Replace('goals.png?v=194" | relURL }}?v=194', 'goals.png" | relURL }}?v=194')
      if ($NewText -ne $Text) {
        Set-Content -Path $File -Value $NewText -Encoding UTF8
        $TouchedFiles.Add($File) | Out-Null
      }
    }
  }
}

# Hard anti-clipping CSS. Prefer the actual partial, because this block belongs only to stats partial.
$CssStart = "/* 194 goals icon no crop start */"
$CssEnd = "/* 194 goals icon no crop end */"
$CssBlock = @"
$CssStart
body.transfer-page #pfb-stats-v184,
body.transfer-page #pfb-stats-v184 *,
body.transfer-page #pfb-stats-v184 .pfb-stats-v184__card,
body.transfer-page #pfb-stats-v184 .pfb-stats-v184__goals,
body.transfer-page #pfb-stats-v184 .pfb-stats-v184__goals *,
body.transfer-page #pfb-stats-v184 img[src*="goals.png"] {
  overflow: visible !important;
  clip-path: none !important;
  -webkit-clip-path: none !important;
  mask: none !important;
  -webkit-mask: none !important;
}

body.transfer-page #pfb-stats-v184 .pfb-stats-v184__goals img,
body.transfer-page #pfb-stats-v184 img[src*="goals.png"] {
  display: block !important;
  width: 70px !important;
  height: 70px !important;
  max-width: 70px !important;
  max-height: 70px !important;
  object-fit: contain !important;
  object-position: center center !important;
  transform: none !important;
  padding: 0 !important;
  box-sizing: border-box !important;
}
$CssEnd
"@

if (Test-Path $Partial) {
  $Text = Get-Content -Path $Partial -Raw -Encoding UTF8
  $Pattern = [regex]::Escape($CssStart) + "(?s).*?" + [regex]::Escape($CssEnd)
  if ([regex]::IsMatch($Text, $Pattern)) {
    $Text = [regex]::Replace($Text, $Pattern, $CssBlock)
  } elseif ($Text.Contains("</style>")) {
    $Index = $Text.LastIndexOf("</style>")
    $Text = $Text.Insert($Index, "`r`n$CssBlock`r`n")
  } else {
    $Text = $Text + "`r`n<style>`r`n$CssBlock`r`n</style>`r`n"
  }
  Set-Content -Path $Partial -Value $Text -Encoding UTF8
  $TouchedFiles.Add($Partial) | Out-Null
  Write-Log "Patched partial CSS/cache: layouts\partials\transfer-player-stats.html"
}

Write-Log ""
Write-Log "Touched files:"
$TouchedFiles | Select-Object -Unique | ForEach-Object {
  $Rel = Resolve-Path $_ | ForEach-Object { $_.Path.Replace($Root.Path + "\", "") }
  Write-Log "- $Rel"
}
Write-Log "- static\images\stats-icons-v184\goals.png"
Write-Log ""
Write-Log "DONE 194. Open the De Ligt page and press Ctrl+F5."
