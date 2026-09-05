# ARCHITECTURE AND PATHS

## Корни

| Назначение | Путь |
|---|---|
| Активный Hugo-проект | `C:\Users\Dmitrii\Promyachik_CLEAN` |
| AutoSync deployment root | `C:\Users\Dmitrii\Promyachik` |
| Техническая инфраструктура | `C:\Users\Dmitrii\ProFutbik` |
| Inbox | `C:\Users\Dmitrii\ProFutbik\Inbox` |
| Reports | `C:\Users\Dmitrii\ProFutbik\reports` |
| Patch backups | `C:\Users\Dmitrii\ProFutbik\patch-backups` |
| Full backups | `C:\Users\Dmitrii\Promyachik_BACKUPS` |

## Ключевые Hugo-файлы

- `layouts/index.html` — сборка главной.
- `layouts/transfers/single.html` — transfer page.
- `layouts/partials/header.html` — header.
- `layouts/partials/transfer-ticker.html` — верхний ticker.
- `layouts/partials/home-player-bottom-strip.html` — нижний ticker.
- `layouts/partials/featured-transfer-of-day.html` — featured area.
- `layouts/partials/transfer-player-stats.html` — статистика.
- `layouts/partials/transfer-player-market-value-chart.html` — market chart.
- `static/js/transfer-player-market-value-chart.js` — интерактив графика.
- `static/css/style.css` — основной CSS.
- `data/transfers.json` — canonical data верхнего/нижнего тикера.
- `data/homepage_transfer_rumor.json` — transfer/rumor blocks главной.
- `data/homepage_featured_admin.json` — approved/admin featured state.
- `data/club-logos.json` — клубные логотипы.
- `data/player-market-values.json` — данные графика.
- `content/transfers/<slug>/index.md` — страницы трансферов.

## Ключевая инфраструктура

- `ProFutbik\tools\parse-source-to-draft.py`.
- `normalize-transfer-draft-core.py`.
- `enrich-transfer-draft.py`.
- `validate-transfer-draft.py`.
- `transfer-gate-report.py`.
- `build-transfer.py`.
- `import-transfer-assets.py`.
- `safe-publish-transfer.py`.
- `validate-rendered-transfer.py`.
- `publish-transfer.py`.
- `run-transfer-pipeline.py`.
- `admin-review\admin_review_server.py`.
- `admin-review\transfer_inbox.py`.
- `admin-review\publish_slider_selected.py`.

## Data flow

```text
source -> raw record -> normalized draft -> enrichment -> validation gates
       -> Hugo content + homepage data + transfers data
       -> Hugo build -> rendered validation -> optional public publish
```

## Entity identity

Canonical identity должна быть стабильной, например:

```text
mario-gila__lazio__ac-milan
```

Повторное событие с тем же entity_id обновляет ту же историю, а не создаёт дубликат.
