$ErrorActionPreference = "Stop"

$Project = "C:\Users\Dmitrii\Promyachik"
$Layouts = Join-Path $Project "layouts"
$Partial = Join-Path $Layouts "partials\favicon.html"
$Build = Join-Path $Project "var\favicon_build_test"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Backup = Join-Path $Project "var\favicon_integration_backup_$Timestamp"
$Marker = '{{ partial "favicon.html" . }}'

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

$ModifiedFiles = New-Object System.Collections.Generic.List[string]
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Restore-Templates {
    foreach ($File in $ModifiedFiles) {
        $Relative = [System.IO.Path]::GetRelativePath($Layouts, $File)
        $BackupFile = Join-Path $Backup $Relative

        if (Test-Path -LiteralPath $BackupFile) {
            Copy-Item -LiteralPath $BackupFile -Destination $File -Force
        }
    }
}

try {
    foreach ($Required in $RequiredFiles) {
        if (-not (Test-Path -LiteralPath $Required)) {
            throw "Required favicon file not found: $Required"
        }
    }

    New-Item -ItemType Directory -Path $Backup -Force | Out-Null

    $Templates = Get-ChildItem -LiteralPath $Layouts -Recurse -File -Filter "*.html"

    foreach ($Template in $Templates) {
        $Text = [System.IO.File]::ReadAllText($Template.FullName, $Utf8NoBom)

        if (
            $Text -notmatch '(?i)<head(?:\s|>)'
            -or $Text -notmatch '(?i)</head>'
            -or $Text.Contains($Marker)
        ) {
            continue
        }

        $Relative = [System.IO.Path]::GetRelativePath($Layouts, $Template.FullName)
        $BackupFile = Join-Path $Backup $Relative
        $BackupFolder = Split-Path -Parent $BackupFile

        New-Item -ItemType Directory -Path $BackupFolder -Force | Out-Null
        Copy-Item -LiteralPath $Template.FullName -Destination $BackupFile -Force

        $NewText = [regex]::Replace(
            $Text,
            '(?i)</head>',
            "$Marker`r`n</head>",
            1
        )

        [System.IO.File]::WriteAllText(
            $Template.FullName,
            $NewText,
            $Utf8NoBom
        )

        $ModifiedFiles.Add($Template.FullName)
        Write-Host "Updated: $Relative"
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
            throw "Hugo build failed with exit code $LASTEXITCODE"
        }
    }
    finally {
        Pop-Location
    }

    $BuiltPagesWithHead = Get-ChildItem -LiteralPath $Build -Recurse -File -Filter "*.html" |
        Where-Object {
            $Content = [System.IO.File]::ReadAllText($_.FullName, $Utf8NoBom)
            $Content -match '(?i)<head(?:\s|>)'
        }

    if (-not $BuiltPagesWithHead) {
        throw "No built HTML pages with a head section were found."
    }

    foreach ($Page in $BuiltPagesWithHead) {
        $Content = [System.IO.File]::ReadAllText($Page.FullName, $Utf8NoBom)
        if ($Content -notmatch 'favicon-32x32\.png') {
            throw "Favicon link missing in built page: $($Page.FullName)"
        }
    }

    Write-Host ""
    Write-Host "DONE"
    Write-Host "Favicon files installed and all HTML templates validated."
    exit 0
}
catch {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)"
    Restore-Templates
    Write-Host "Modified templates were restored."
    exit 1
}
