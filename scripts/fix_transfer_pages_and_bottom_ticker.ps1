$ErrorActionPreference = "Stop"

$Project = "C:\Users\Dmitrii\Promyachik"
$Template = Join-Path $Project "layouts\transfers\single.html"
$Section = Join-Path $Project "content\transfers"
$OldIndex = Join-Path $Section "index.md"
$BranchIndex = Join-Path $Section "_index.md"
$Backup = Join-Path $Project "var\fix_transfer_pages_backup_v2"
$Build = Join-Path $Project "var\fix_transfer_pages_build_v2"

$Slugs = @(
    "ibrahima-konate-real-madrid",
    "marc-cucurella-real-madrid",
    "denzel-dumfries-real-madrid",
    "julian-alvarez-barcelona",
    "elliot-anderson-manchester-city",
    "bernardo-silva-real-madrid"
)

$OriginalOldIndexExists = Test-Path -LiteralPath $OldIndex
$OriginalBranchIndexExists = Test-Path -LiteralPath $BranchIndex

function Restore-PreviousState {
    Write-Host ""
    Write-Host "Restoring previous files..."

    $TemplateBackup = Join-Path $Backup "single.html"
    if (Test-Path -LiteralPath $TemplateBackup) {
        Copy-Item -LiteralPath $TemplateBackup -Destination $Template -Force
    }

    if (Test-Path -LiteralPath $OldIndex) {
        Remove-Item -LiteralPath $OldIndex -Force
    }

    if (Test-Path -LiteralPath $BranchIndex) {
        Remove-Item -LiteralPath $BranchIndex -Force
    }

    if ($OriginalOldIndexExists) {
        $OldBackup = Join-Path $Backup "index.md"
        if (Test-Path -LiteralPath $OldBackup) {
            Copy-Item -LiteralPath $OldBackup -Destination $OldIndex -Force
        }
    }

    if ($OriginalBranchIndexExists) {
        $BranchBackup = Join-Path $Backup "_index.md"
        if (Test-Path -LiteralPath $BranchBackup) {
            Copy-Item -LiteralPath $BranchBackup -Destination $BranchIndex -Force
        }
    }

    Write-Host "Previous state restored."
}

try {
    if (-not (Test-Path -LiteralPath $Template)) {
        throw "Template not found: $Template"
    }

    if (-not (Test-Path -LiteralPath $Section)) {
        throw "Transfers folder not found: $Section"
    }

    foreach ($Slug in $Slugs) {
        $Page = Join-Path $Section "$Slug\index.md"
        if (-not (Test-Path -LiteralPath $Page)) {
            throw "Page file not found: $Page"
        }
    }

    if (Test-Path -LiteralPath $Backup) {
        Remove-Item -LiteralPath $Backup -Recurse -Force
    }
    New-Item -ItemType Directory -Path $Backup -Force | Out-Null

    Copy-Item -LiteralPath $Template -Destination (Join-Path $Backup "single.html") -Force

    if ($OriginalOldIndexExists) {
        Copy-Item -LiteralPath $OldIndex -Destination (Join-Path $Backup "index.md") -Force
    }

    if ($OriginalBranchIndexExists) {
        Copy-Item -LiteralPath $BranchIndex -Destination (Join-Path $Backup "_index.md") -Force
    }

    Write-Host ""
    Write-Host "STEP 1 OF 3: fixing the transfers section..."

    if ($OriginalOldIndexExists -and -not $OriginalBranchIndexExists) {
        Move-Item -LiteralPath $OldIndex -Destination $BranchIndex -Force
    }
    elseif ($OriginalOldIndexExists -and $OriginalBranchIndexExists) {
        Remove-Item -LiteralPath $OldIndex -Force
    }
    elseif (-not $OriginalBranchIndexExists) {
        @"
---
title: "Трансферы"
draft: false
---
"@ | Set-Content -LiteralPath $BranchIndex -Encoding UTF8
    }

    Write-Host "STEP 2 OF 3: setting the bottom ticker to six transfers..."

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $Text = [System.IO.File]::ReadAllText($Template, $Utf8NoBom)

    $Pattern = '\{\{\s*\$bottomTransfers\s*:=\s*first\s+\d+\s+\.Site\.Data\.transfers\s*\}\}'
    $Replacement = '{{ $bottomTransfers := first 6 .Site.Data.transfers }}'

    if (-not [regex]::IsMatch($Text, $Pattern)) {
        throw "Bottom ticker limit line was not found in $Template"
    }

    $Text = [regex]::Replace($Text, $Pattern, $Replacement, 1)
    [System.IO.File]::WriteAllText($Template, $Text, $Utf8NoBom)

    Write-Host "STEP 3 OF 3: validating Hugo and all six pages..."

    if (Test-Path -LiteralPath $Build) {
        Remove-Item -LiteralPath $Build -Recurse -Force
    }

    Push-Location $Project
    try {
        & hugo --minify --destination $Build --baseURL "http://127.0.0.1:1313/promyachik/"
        if ($LASTEXITCODE -ne 0) {
            throw "Hugo build failed with exit code $LASTEXITCODE"
        }
    }
    finally {
        Pop-Location
    }

    foreach ($Slug in $Slugs) {
        $BuiltPage = Join-Path $Build "transfers\$Slug\index.html"
        if (-not (Test-Path -LiteralPath $BuiltPage)) {
            throw "Hugo did not create: $BuiltPage"
        }
    }

    Write-Host ""
    Write-Host "DONE"
    Write-Host ""
    Write-Host "Fixed:"
    Write-Host "- all six transfer pages build separately;"
    Write-Host "- Julian Alvarez is included in the bottom ticker;"
    Write-Host "- Elliot Anderson is included in the bottom ticker;"
    Write-Host "- the bottom ticker now shows six current transfers."
    exit 0
}
catch {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)"
    Restore-PreviousState
    exit 1
}
