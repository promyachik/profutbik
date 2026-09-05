# SITE COMPONENT MAP

## Верхний ticker

**Data:** `data/transfers.json`  
**Template:** `layouts/partials/transfer-ticker.html`

Функции:

- фильтр `show_in_top_ticker != false`;
- status label/class dictionaries;
- club logo resolution по `club-logos`;
- href на transfer page;
- две одинаковые группы для бесшовного движения;
- drag/click поведение.

Не переписывать с нуля. При точечном статусном баге менять только adapter mapping.

## Нижний ticker

**Template:** `layouts/partials/home-player-bottom-strip.html`

На снимке `407C` он выбирает official и отдельные исторические slug. Для Mario Gila `show_in_footer_ticker=false`; этап 406H намеренно не добавлял его вниз.

Известенная проблема совместимости: некоторые старые элементы имеют nested `from_club/to_club` objects, а шаблон обращается к `.name/.logo`. Нельзя подсовывать строки вместо объектов.

## Homepage transfer/rumor blocks

**Data:** `data/homepage_transfer_rumor.json`

Разделяет `transfers` и `rumors`. У Mario Gila:

- group `transfer`;
- status `completed`;
- status_css `is-done`;
- status_display `состоялся`;
- url `transfers/mario-gila-ac-milan/`.

## Transfer page Mario Gila

`content/transfers/mario-gila-ac-milan/index.md`

Сейчас:

- draft true;
- test_mode true;
- canonical_transfer_status official;
- status completed;
- source_url внутренне сохранён;
- photo/profile/chart/stats ещё не закончены.

## Featured slider и админка

Локальная админка хранится в `ProFutbik\admin-review`. Пользователь выбирает art, одобряет и публикует выбранный вариант. Нельзя использовать fallback cover как финальный concept art или смешивать art одного игрока с данными другого.
