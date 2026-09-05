# UNIVERSAL TRANSFER PIPELINE

## Целевой контракт входа

- `entity_id`: стабильный идентификатор player + from + to;
- `player`: латиницей;
- `from_club_id`, `to_club_id`: известные локальные/API IDs;
- `status`: canonical (`official/completed` для состоявшейся сделки);
- `date`: ISO-8601;
- `fee`: nullable, никогда не выдумывать;
- `source_url`: внутреннее доказательство;
- routes: news/transfers/rumors.

## Правила

- Одна canonical entity.
- Upsert по entity_id.
- Никакого player-specific кода в универсальном importer.
- Не клонировать произвольные nested objects от старых игроков.
- Не добавлять lower ticker на первом этапе.
- Обязателен Hugo build.
- Обязательна rendered validation.
- Ошибка на любом этапе должна откатывать точечные изменения.

## Mario Gila — доказанный путь

1. **406A parser:** реальная официальная страница AC Milan скачана, поля распознаны, fee не выдумана.
2. **406B draft:** создан draft для news + transfers, rumors disabled.
3. **406C Hugo draft:** локальная transfer page создана и отрендерена.
4. **406D homepage:** transfer card появилась на главной и ведёт на страницу.
5. **406E/F:** неудачные попытки верхнего ticker, rollback выполнен.
6. **406G diagnostic:** контракт унифицирован.
7. **406H importer:** страница + homepage + upper ticker работают, lower ticker выключен, дубликатов нет.
8. **406I:** фикс цвета не применён из-за хрупкого source-fragment precheck.

## Не смешивать статусы

Homepage использует `status_css` (`is-done`, `is-talks`, ...), а upper ticker вычисляет собственный class через словарь в template. Добавление нового canonical status требует обновления всех relevant adapters, но не должно заставлять source data подстраиваться под один UI-компонент.
