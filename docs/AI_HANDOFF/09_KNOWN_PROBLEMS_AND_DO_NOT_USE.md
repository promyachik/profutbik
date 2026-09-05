# KNOWN PROBLEMS / DO NOT USE

## Текущий известный баг

Upper ticker: `completed` -> fallback `rumour`; текст правильный, цвет жёлтый.

## Известные технические риски

- Большая рабочая копия сильно отличается от Git HEAD; нельзя делать широкие git reset/checkout.
- Hugo предупреждает о deprecated `languageCode` и `.Site.Data`; это не текущая авария и не должно смешиваться с точечным ticker fix.
- Lower ticker чувствителен к типу `from_club/to_club`: object vs string.
- Hugo build success сам по себе не гарантирует правильный runtime/DOM — нужна rendered validation.
- Нельзя патчить `public` как источник истины.
- Нельзя добавлять player-specific branches в universal importer.
- Нельзя скрывать цену общим поиском по тексту: ранее это убирало нужные жёлтые значения.
- Не использовать постоянные MutationObserver/timer locks для slider.
- Не возвращаться к старому многократно патченному publisher; успешным baseline был clean publisher V2.

## Запрещённые рабочие привычки

- Просить пользователя вручную вставлять код при простой замене.
- Выдавать новый пакет, не прочитав report предыдущего.
- Делать полный backup на каждый эксперимент.
- Менять несколько несвязанных блоков одним пакетом.
- Объявлять визуальный успех только по exit code.
- Изобретать детали проекта, которых нет в файлах/report.
