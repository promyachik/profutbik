# CURRENT STATE AND NEXT ACTION

## Состояние на 23.07.2026

### Что успешно

- `406A`: официальный источник Mario Gila загружен и классифицирован как official; сайт не изменён.
- `406B`: создан структурированный draft; site write отключён.
- `406C`: создан локальный Hugo draft `content/transfers/mario-gila-ac-milan/index.md`; Hugo render успешен.
- `406D`: Mario Gila добавлен в homepage transfer data; карточка и ссылка на страницу отображаются.
- `406E`: первая попытка upper ticker не прошла rendered validation; изменения откатились.
- `406F`: выявлена несовместимость nested object schema нижнего тикера; изменения откатились.
- `406G`: выполнена диагностика и сформирован универсальный контракт.
- `406H`: универсальный importer успешно записал одну canonical entity в страницу, homepage data и upper ticker data. Дубликатов нет. Upper ticker виден. Lower ticker не изменён.

### Что неуспешно

`406I` должен был исправить статус и ссылку верхнего тикера, но precheck `status_expression` не нашёл ожидаемый исходный фрагмент. Скрипт остановился до изменения файлов.

### Фактический баг

`data/transfers.json` для Mario Gila:

```json
{
  "status": "completed",
  "status_label": "СОСТОЯЛСЯ",
  "show_in_top_ticker": true,
  "show_in_footer_ticker": false,
  "url": "transfers/mario-gila-ac-milan/"
}
```

`layouts/partials/transfer-ticker.html` содержит словари только для:

- rumour;
- negotiations;
- agreement;
- confirmed;
- official.

Строка класса:

```go-html-template
{{ $statusClass := default "rumour" (index $statusClasses $transfer.status) }}
```

Для `completed` lookup возвращает пустое значение, срабатывает fallback `rumour`. Текст берётся из `status_label`, поэтому написано `СОСТОЯЛСЯ`, но цвет остаётся жёлтым.

### Следующий пакет

Создать минимальный пакет после документации, условно `407E_FIX_COMPLETED_UPPER_TICKER_GREEN`:

1. Точечно backup только `layouts/partials/transfer-ticker.html`.
2. Добавить mapping:

```go-html-template
"completed" "СОСТОЯЛСЯ"
```

и class mapping:

```go-html-template
"completed" "official"
```

или отдельный `completed`, только если CSS-класс с зелёным стилем будет добавлен безопасно.
3. Не изменять href, структуру группы, drag JS или lower ticker.
4. Запустить Hugo.
5. Проверить rendered HTML:
   - Mario Gila присутствует;
   - href ведёт на `/promyachik/transfers/mario-gila-ac-milan/`;
   - отображается `СОСТОЯЛСЯ`;
   - class не `rumour`, а зелёный;
   - верхний ticker содержит две группы для бесшовного цикла;
   - нижний ticker не получил Mario Gila.
6. Report в `ProFutbik\reports`.
7. Полный backup только после визуального подтверждения Дмитрия.

## После исправления цвета

Следующие этапы не выполнять вслепую. Вероятная последовательность:

1. пользователь визуально подтверждает верхний ticker;
2. зафиксировать успешный шаг/backup по команде пользователя;
3. подключить player profile/photo enrichment;
4. подготовить фото игрока на чистом чёрном фоне;
5. закончить полноценную transfer article/page;
6. отдельно решить включение официальной сделки в lower ticker;
7. только затем публичная публикация.
