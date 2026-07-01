$ErrorActionPreference = "Stop"

$project = "C:\Users\Dmitrii\Promyachik"
Set-Location $project

Write-Host ""
Write-Host "PROFUTBIK 204 - apply approved stats block to all transfer players"
Write-Host "Project: $project"
Write-Host ("Time: " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
Write-Host ""

$backupDir = Join-Path $project "_backup_204_apply_approved_stats_block_to_all_transfer_players"
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$partial = Join-Path $project "layouts\partials\transfer-player-stats.html"
if (!(Test-Path $partial)) {
    throw "Missing approved stats partial: $partial"
}

$docsDir = Join-Path $project "docs"
New-Item -ItemType Directory -Force -Path $docsDir | Out-Null

$rulesFile = Join-Path $docsDir "PROFUTBIK_TRANSFER_PLAYER_PAGE_RULES.md"
if (Test-Path $rulesFile) {
    $backupRules = Join-Path $backupDir "PROFUTBIK_TRANSFER_PLAYER_PAGE_RULES_before_204.md"
    if (!(Test-Path $backupRules)) {
        Copy-Item $rulesFile $backupRules -Force
        Write-Host "Backup saved: _backup_204_apply_approved_stats_block_to_all_transfer_players\PROFUTBIK_TRANSFER_PLAYER_PAGE_RULES_before_204.md"
    }
}

$rules = @'
# ProFutbik / Promyachik — правила страниц игроков и трансферов

## 1. SEO для каждого нового игрока / трансфера

Каждая новая transfer/player page создаётся как SEO-страница, а не просто как визуальная карточка.

Обязательно:
- SEO title;
- meta description;
- нормальный slug;
- H1;
- SEO-вступление;
- уникальный текст новости/аналитики;
- факты перехода;
- клуб откуда / клуб куда;
- позиция игрока;
- рыночная стоимость и контекст, если данные есть;
- внутренние ссылки на клубы, лиги и связанные трансферы;
- человекочитаемая структура текста.

## 2. Утверждённый блок статистики для всех игроков

Каждая новая transfer/player page должна сразу получать утверждённый блок статистики.

Принятый вид:
- Goals — вариант 3 из пакета 200;
- внешний общий блок статистики убран пакетом 201;
- отдельные карточки с иконками сохранены;
- карточки уменьшены пакетами 202 и 203;
- итоговая ширина карточек примерно `width: calc(100% - 9px)`;
- сайт не открывается автоматически из BAT;
- BAT не спрашивает Y/N;
- push не делается автоматически.

Данные статистики должны наполняться по мере поступления парсинга/API.  
Не выдумывать статистику.  
Не показывать мусорные прочерки и фейковые значения.

## 3. Concept art для главных трансферов на главной

Если игрок/трансфер попадает на главную как один из главных трансферов, к этой новости нужно готовить отдельный concept art в стиле сайта.

Concept art нужен именно для featured transfer/news на главной, чтобы важные трансферы визуально отличались.

## 4. Формат рабочих пакетов

Для ProFutbik/Promyachik пакеты делать только ZIP.

Внутри:
- готовый BAT;
- скрипты в `scripts/`;
- payload только если нужен.

Пакеты не должны:
- открывать сайт автоматически;
- спрашивать Y/N;
- пушить автоматически;
- заставлять пользователя вручную создавать файлы.
'@

Set-Content -Path $rulesFile -Value $rules -Encoding UTF8
Write-Host "Rules written: docs\PROFUTBIK_TRANSFER_PLAYER_PAGE_RULES.md"

# Pick the template that controls transfer/player pages.
$candidates = @(
    "layouts\transfers\single.html",
    "layouts\_default\single.html",
    "layouts\transfers\list.html"
)

$target = $null
foreach ($rel in $candidates) {
    $p = Join-Path $project $rel
    if (Test-Path $p) {
        $target = $p
        break
    }
}

if ($null -eq $target) {
    throw "No transfer/default single template found. Checked: $($candidates -join ', ')"
}

$targetRel = Resolve-Path $target -Relative
$targetRel = $targetRel.TrimStart(".\")
Write-Host "Template selected: $targetRel"

$backupTemplate = Join-Path $backupDir (($targetRel -replace "[\\/:]", "_") + "_before_204.html")
if (!(Test-Path $backupTemplate)) {
    Copy-Item $target $backupTemplate -Force
    Write-Host "Backup saved: _backup_204_apply_approved_stats_block_to_all_transfer_players\$([System.IO.Path]::GetFileName($backupTemplate))"
}

$html = Get-Content $target -Raw -Encoding UTF8

if ($html -match 'transfer-player-stats\.html') {
    Write-Host "Template already contains transfer-player-stats partial. No duplicate inserted."
} else {
    $isTransferTemplate = ($targetRel -like "layouts\transfers\*")

    if ($isTransferTemplate) {
        $snippet = @'

{{/* 204 universal approved stats block for transfer/player pages */}}
{{ if not .Params.hide_stats_block }}
  {{ partial "transfer-player-stats.html" . }}
{{ end }}

'@
    } else {
        $snippet = @'

{{/* 204 universal approved stats block for transfer/player pages */}}
{{ if and (eq .Section "transfers") (not .Params.hide_stats_block) }}
  {{ partial "transfer-player-stats.html" . }}
{{ end }}

'@
    }

    $inserted = $false

    # Prefer insertion after market/chart related partial or block.
    $patterns = @(
        '(?s)(\{\{\s*partial\s+"[^"]*market[^"]*"\s+\.\s*\}\})',
        '(?s)(\{\{\s*partial\s+"[^"]*chart[^"]*"\s+\.\s*\}\})',
        '(?s)(<[^>]+class="[^"]*market[^"]*"[^>]*>.*?</[^>]+>)',
        '(?s)(<[^>]+class="[^"]*chart[^"]*"[^>]*>.*?</[^>]+>)'
    )

    foreach ($pattern in $patterns) {
        if ($html -match $pattern) {
            $html = [regex]::Replace($html, $pattern, '$1' + $snippet, 1)
            $inserted = $true
            Write-Host "Inserted stats block after market/chart area."
            break
        }
    }

    if (-not $inserted) {
        if ($html -match '\{\{\s*\.Content\s*\}\}') {
            $html = [regex]::Replace($html, '(\{\{\s*\.Content\s*\}\})', '$1' + $snippet, 1)
            $inserted = $true
            Write-Host "Inserted stats block after .Content fallback."
        }
    }

    if (-not $inserted) {
        $html = $html + "`n" + $snippet
        Write-Host "Inserted stats block at end of template fallback."
    }

    Set-Content -Path $target -Value $html -Encoding UTF8
    Write-Host "Patched template: $targetRel"
}

# Create a small report.
$varDir = Join-Path $project "var"
New-Item -ItemType Directory -Force -Path $varDir | Out-Null
$report = Join-Path $varDir "profutbik_204_apply_stats_block_report.txt"

$reportText = @"
PROFUTBIK 204 - APPLY APPROVED STATS BLOCK TO ALL TRANSFER PLAYERS

Time: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Project: $project

Approved stats partial:
- layouts\partials\transfer-player-stats.html

Template selected:
- $targetRel

Rules file:
- docs\PROFUTBIK_TRANSFER_PLAYER_PAGE_RULES.md

Important:
- This package does not open the site.
- This package does not push.
- This package does not ask Y/N.
- It only applies local template/rules changes.

Check pages manually:
- http://localhost:1313/promyachik/transfers/matthijs-de-ligt/
- other transfer/player pages
"@

Set-Content -Path $report -Value $reportText -Encoding UTF8
Write-Host "Report written: var\profutbik_204_apply_stats_block_report.txt"

Write-Host ""
Write-Host "Touched files:"
Write-Host "- $targetRel"
Write-Host "- docs\PROFUTBIK_TRANSFER_PLAYER_PAGE_RULES.md"
Write-Host "- var\profutbik_204_apply_stats_block_report.txt"
Write-Host ""
Write-Host "NO SITE OPENED."
Write-Host "NO PUSH MADE."
