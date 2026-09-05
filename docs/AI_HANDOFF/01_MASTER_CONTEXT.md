# MASTER CONTEXT — ProFutbik / Promyachik

## Назначение проекта

Promyachik — тёмная футбольная трансферная платформа на Hugo. Целевая система должна автоматически находить трансферные события, объединять обновления одной истории, формировать структурированные данные, создавать страницу трансфера, показывать событие на главной и в тикерах, обогащать фото/логотипами/стоимостью/статистикой, проходить gates и только после проверки публиковаться.

## Активная среда

- Windows 10 x64.
- Python 3.14.
- Hugo 0.163.3 (`C:\Hugo\hugo.exe`).
- Git 2.54.
- Активный Hugo-проект: `C:\Users\Dmitrii\Promyachik_CLEAN`.
- Техническая инфраструктура: `C:\Users\Dmitrii\ProFutbik`.
- Корень распаковки AutoSync-пакетов: `C:\Users\Dmitrii\Promyachik`.
- Inbox: `C:\Users\Dmitrii\ProFutbik\Inbox`.
- Reports: `C:\Users\Dmitrii\ProFutbik\reports`.
- Backups: `C:\Users\Dmitrii\Promyachik_BACKUPS` и точечные `C:\Users\Dmitrii\ProFutbik\patch-backups`.
- Локальный сайт: `http://localhost:1313/promyachik/`.
- GitHub Pages: `https://promyachik.github.io/promyachik/`.

## Главные подсистемы

1. **Parser / source intake** — получает официальный источник или трансферный сигнал и создаёт canonical record.
2. **Draft builder** — создаёт нормализованный draft, не публикуя сайт преждевременно.
3. **Enrichment** — клубы, логотипы, player ID, фото, flags, fee, stats, market value.
4. **Publication gates** — проверяют схему, assets, запреты, готовность к записи.
5. **Hugo writer** — создаёт/обновляет `content/transfers/<slug>/index.md` и data-файлы.
6. **Homepage transfer/rumor block** — `data/homepage_transfer_rumor.json`.
7. **Upper ticker** — `data/transfers.json` + `layouts/partials/transfer-ticker.html`.
8. **Lower ticker** — `layouts/partials/home-player-bottom-strip.html`; отдельная стадия, не включать автоматически на раннем тесте.
9. **Featured slider / art review** — локальная админка и выбор concept art.
10. **Rendered validation** — Hugo build и проверка реального HTML.
11. **Safe publish / GitHub** — только после разрешения и прохождения gates.

## Визуальный контракт

- фон чёрный/почти чёрный;
- золото — основной акцент;
- допустимы красные и синие световые акценты;
- фото игрока и concept art — разные сущности;
- player photo для карточек/тикеров/профиля;
- concept art для hero/featured slider;
- имена футболистов в публичном интерфейсе — латиницей;
- сайт не должен выглядеть как обычная новостная лента.

## Структура главной

- header;
- верхний transfer ticker;
- hero/featured slider;
- скрытый сейчас поиск;
- transfer/rumor blocks;
- status/official sections;
- нижний player transfer ticker;
- footer/SEO.

## Страницы трансферов

Ожидаемые поля/блоки:

- title, description, canonical;
- status;
- player;
- from/to club;
- fee;
- source metadata (внутренне; технический URL не показывать пользователю);
- player photo;
- concept art при наличии;
- nationality flag;
- club logos;
- market value chart;
- stats, но не показывать пустые заглушки;
- основной текст и SEO.

## Текущий репозиторий

Снимок `407C` показал HEAD `1e10e22e0e9d3e40c721ce0dfce632a7b2c8c10a`, но рабочая копия содержит большое количество modified/untracked файлов. Поэтому commit HEAD нельзя считать текущим источником истины. Источник истины — фактические файлы `Promyachik_CLEAN` и последний report.
