# HISTORY — 406A to 406I

| Шаг | Результат | Изменение сайта |
|---|---|---|
| 406A | Реальный официальный source распарсен | Нет |
| 406B | Создан normalized draft и enrichment queue | Нет |
| 406C | Создан локальный Hugo draft transfer page | Да, локальный draft |
| 406D | Mario Gila появился в homepage transfers | Да |
| 406E | Upper ticker rendered check failed | Rollback |
| 406F | Неверная data shape сломала lower ticker template | Rollback |
| 406G | Диагностика universal schema | Нет |
| 406H | Universal importer: page + homepage + upper ticker | Да, успешно |
| 406I | Source-fragment precheck failed; fix не применён | Нет |

## Принципиальный урок

`406I` искал точную старую строку вместо анализа текущего AST/template fragment. Следующие патчи должны:

- проверять семантические anchors;
- показывать найденные строки в report;
- не считать отсутствие одного старого literal доказательством отсутствия логики;
- не вносить изменения, пока prechecks не пройдены;
- при необходимости выполнять диагностический пакет вместо нового blind patch.
