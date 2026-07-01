$ErrorActionPreference = "Stop"

$Project = "C:\Users\Dmitrii\Promyachik"
$Layouts = Join-Path $Project "layouts"
$Partial = Join-Path $Layouts "partials\favicon.html"
$Build = Join-Path $Project "var\favicon_build_test_v2"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Backup = Join-Path $Project ("var\favicon_integration_backup_" + $Timestamp)
$Marker = '{{ partial "favicon.html" . }}'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$ModifiedFiles = New-Object System.Collections.ArrayList

$RequiredFiles = @(
    (Join-Path $Project "static\favicon.ico"),
    (Join-Path $Project "static\favicon-16x16.png"),
    (Join-Path $Project "static\favicon-32x32.png"),
    (Join-Path $Project "static\apple-touch-icon.png"),
    (Join-Path $Project "static\android-chrome-192x192.png"),
    (Join-Path $Project "static\android-chrome-512x512.png"),
    (Join-Path $Project "static\site.webmanifest"),
    $Partial
)

function Restore-Templates {
    foreach ($File in $ModifiedFiles) {
        $LayoutsPrefix = $Layouts.TrimEnd("\") + "\"
        $Relative = $File.Substring($LayoutsPrefix.Length)
        $BackupFile = Join-Path $Backup $Relative

        if (Test-Path -LiteralPath $BackupFile) {
            Copy-Item -LiteralPath $BackupFile -Destination $File -Force
        }
    }
}

try {
    foreach ($Required in $RequiredFiles) {
        if (-not (Test-Path -LiteralPath $Required)) {
            throw ("Required favicon file not found: " + $Required)
        }
    }

    New-Item -ItemType Directory -Path $Backup -Force | Out-Null

    $Templates = Get-ChildItem -LiteralPath $Layouts -Recurse -File -Filter "*.html"
    $LayoutsPrefix = $Layouts.TrimEnd("\") + "\"

    foreach ($Template in $Templates) {
        $Text = [System.IO.File]::ReadAllText($Template.FullName, $Utf8NoBom)

        $HasOpeningHead = $Text -match '(?i)<head(?:\s|>)'
        $HasClosingHead = $Text -match '(?i)</head>'
        $AlreadyInstalled = $Text.Contains($Marker)

        if ((-not $HasOpeningHead) -or (-not $HasClosingHead) -or $AlreadyInstalled) {
            continue
        }

        $Relative = $Template.FullName.Substring($LayoutsPrefix.Length)
        $BackupFile = Join-Path $Backup $Relative
        $BackupFolder = Split-Path -Parent $BackupFile

        New-Item -ItemType Directory -Path $BackupFolder -Force | Out-Null
        Copy-Item -LiteralPath $Template.FullName -Destination $BackupFile -Force

        $NewText = [regex]::Replace(
            $Text,
            '(?i)</head>',
            ($Marker + "`r`n</head>"),
            1
        )

        [System.IO.File]::WriteAllText(
            $Template.FullName,
            $NewText,
            $Utf8NoBom
        )

        [void]$ModifiedFiles.Add($Template.FullName)
        Write-Host ("Updated: " + $Relative)
    }

    if ($ModifiedFiles.Count -eq 0) {
        Write-Host "Favicon links were already installed in all templates."
    }

    if (Test-Path -LiteralPath $Build) {
        Remove-Item -LiteralPath $Build -Recurse -Force
    }

    Push-Location $Project
    try {
        & hugo --minify --destination $Build --baseURL "http://127.0.0.1:1313/promyachik/"
        if ($LASTEXITCODE -ne 0) {
            throw ("Hugo build failed with exit code " + $LASTEXITCODE)
        }
    }
    finally {
        Pop-Location
    }

    $BuiltPagesWithHead = @()

    $BuiltHtmlFiles = Get-ChildItem -LiteralPath $Build -Recurse -File -Filter "*.html"
    foreach ($BuiltFile in $BuiltHtmlFiles) {
        $Content = [System.IO.File]::ReadAllText($BuiltFile.FullName, $Utf8NoBom)

        if ($Content -match '(?i)<head(?:\s|>)') {
            $BuiltPagesWithHead += $BuiltFile

            if ($Content -notmatch 'favicon-32x32\.png') {
                throw ("Favicon link missing in built page: " + $BuiltFile.FullName)
            }
        }
    }

    if ($BuiltPagesWithHead.Count -eq 0) {
        throw "No built HTML pages with a head section were found."
    }

    Write-Host ""
    Write-Host "DONE"
    Write-Host "Favicon files installed and all HTML pages validated."
    exit 0
}
catch {
    Write-Host ""
    Write-Host ("ERROR: " + $_.Exception.Message)
    Restore-Templates
    Write-Host "Modified templates were restored."
    exit 1
}
