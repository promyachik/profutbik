(() => {
    "use strict";

    const VERSION = "42-pull-last-point-inside-keep-center";
    window.__PFMarketChartVersion = VERSION;

    const PLAYERS = [{"key": "mbappe", "name": "Kylian Mbappé", "paths": ["/transfers/kylian-mbappe-real-madrid/"], "points": [{"label": "2017", "value_label": "€35 млн", "value": 35, "club": {"slug": "monaco", "name": "AS Monaco", "short": "ASM", "api_id": 91, "period": "2015–2017", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "2018", "value_label": "€120 млн", "value": 120, "club": {"slug": "psg", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "2017–2024", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "2025", "value_label": "€200 млн", "value": 200, "club": {"slug": "real-madrid", "name": "Real Madrid", "short": "RMA", "api_id": 541, "period": "с 2024", "logo": "images/clubs/api/rendered/541-9a600f047317.png"}}, {"label": "2026", "value_label": "€180 млн", "value": 180, "club": {"slug": "real-madrid", "name": "Real Madrid", "short": "RMA", "api_id": 541, "period": "с 2024", "logo": "images/clubs/api/rendered/541-9a600f047317.png"}}]}, {"key": "wirtz", "name": "Florian Wirtz", "paths": ["/transfers/florian-wirtz-liverpool/"], "points": [{"label": "2023", "value_label": "€100 млн", "value": 100, "club": {"slug": "bayer-leverkusen", "name": "Bayer Leverkusen", "short": "B04", "api_id": 168, "period": "2020–2025", "logo": "images/clubs/api/rendered/168-09eb1c899095.png"}}, {"label": "июнь 2025", "value_label": "€140 млн", "value": 140, "club": {"slug": "liverpool", "name": "Liverpool", "short": "LFC", "api_id": 40, "period": "с 2025", "logo": "images/clubs/api/rendered/40-c3b13021c1ab.png"}}, {"label": "дек. 2025", "value_label": "€110 млн", "value": 110, "club": {"slug": "liverpool", "name": "Liverpool", "short": "LFC", "api_id": 40, "period": "с 2025", "logo": "images/clubs/api/rendered/40-c3b13021c1ab.png"}}, {"label": "2026", "value_label": "€100 млн", "value": 100, "club": {"slug": "liverpool", "name": "Liverpool", "short": "LFC", "api_id": 40, "period": "с 2025", "logo": "images/clubs/api/rendered/40-c3b13021c1ab.png"}}]}, {"key": "konate", "name": "Ibrahima Konaté", "paths": ["/transfers/ibrahima-konate-real-madrid/"], "points": [{"label": "2017", "value_label": "€300 тыс.", "value": 0.3, "club": {"slug": "rb-leipzig", "name": "RB Leipzig", "short": "RBL", "api_id": 173, "period": "2017–2021", "logo": "images/clubs/api/rendered/173-d38d0dff9d91.png"}}, {"label": "2021", "value_label": "€35 млн", "value": 35, "club": {"slug": "liverpool", "name": "Liverpool", "short": "LFC", "api_id": 40, "period": "2021–2026", "logo": "images/clubs/api/rendered/40-c3b13021c1ab.png"}}, {"label": "2025", "value_label": "€60 млн", "value": 60, "club": {"slug": "liverpool", "name": "Liverpool", "short": "LFC", "api_id": 40, "period": "2021–2026", "logo": "images/clubs/api/rendered/40-c3b13021c1ab.png"}}, {"label": "2026", "value_label": "€45 млн", "value": 45, "club": {"slug": "real-madrid", "name": "Real Madrid", "short": "RMA", "api_id": 541, "period": "с 2026", "logo": "images/clubs/api/rendered/541-9a600f047317.png"}}]}, {"key": "cucurella", "name": "Marc Cucurella", "paths": ["/transfers/marc-cucurella-real-madrid/"], "points": [{"label": "2018", "value_label": "€5 млн", "value": 5, "club": {"slug": "barcelona", "name": "Barcelona", "short": "FCB", "api_id": 529, "period": "до 2019", "logo": "images/clubs/api/rendered/529-921329187f25.png"}}, {"label": "2019", "value_label": "€10 млн", "value": 10, "club": {"slug": "getafe", "name": "Getafe", "short": "GET", "api_id": 546, "period": "2019–2021", "logo": "images/clubs/api/546.png"}}, {"label": "2020", "value_label": "€18 млн", "value": 18, "club": {"slug": "getafe", "name": "Getafe", "short": "GET", "api_id": 546, "period": "2019–2021", "logo": "images/clubs/api/546.png"}}, {"label": "2021", "value_label": "€20 млн", "value": 20, "club": {"slug": "brighton", "name": "Brighton & Hove Albion", "short": "BHA", "api_id": 51, "period": "2021–2022", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "2026", "value_label": "€50 млн", "value": 50, "club": {"slug": "real-madrid", "name": "Real Madrid", "short": "RMA", "api_id": 541, "period": "с 2026", "logo": "images/clubs/api/rendered/541-9a600f047317.png"}}]}, {"key": "dumfries", "name": "Дензел Дюмфрис", "paths": ["/transfers/denzel-dumfries-real-madrid/"], "points": [{"label": "2015", "value_label": "€50 тыс.", "value": 0.05, "club": {"slug": "sparta-rotterdam", "name": "Sparta Rotterdam", "short": "SPA", "api_id": null, "period": "2014–2017"}}, {"label": "2017", "value_label": "€1 млн", "value": 1, "club": {"slug": "heerenveen", "name": "SC Heerenveen", "short": "HEE", "api_id": null, "period": "2017–2018"}}, {"label": "2018", "value_label": "€4 млн", "value": 4, "club": {"slug": "psv", "name": "PSV Eindhoven", "short": "PSV", "api_id": 197, "period": "2018–2021"}}, {"label": "2021", "value_label": "€16 млн", "value": 16, "club": {"slug": "inter", "name": "Inter", "short": "INT", "api_id": 505, "period": "с 2021", "logo": "images/clubs/api/rendered/505-14c915ad4d30.png"}}, {"label": "2025", "value_label": "€35 млн", "value": 35, "club": {"slug": "inter", "name": "Inter", "short": "INT", "api_id": 505, "period": "с 2021", "logo": "images/clubs/api/rendered/505-14c915ad4d30.png"}}, {"label": "2026", "value_label": "€25 млн", "value": 25, "club": {"slug": "inter", "name": "Inter", "short": "INT", "api_id": 505, "period": "с 2021", "logo": "images/clubs/api/rendered/505-14c915ad4d30.png"}}]}, {"key": "alvarez", "name": "Julián Álvarez", "paths": ["/transfers/julian-alvarez-barcelona/"], "points": [{"label": "янв. 2022", "value_label": "€20 млн", "value": 20, "club": {"slug": "river-plate", "name": "River Plate", "short": "CARP", "api_id": null, "period": "2018–2022"}}, {"label": "июль 2022", "value_label": "€23 млн", "value": 23, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "2022–2024", "logo": "images/clubs/api/rendered/50-448f2e57b69e.png"}}, {"label": "2023", "value_label": "€90 млн", "value": 90, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "2022–2024", "logo": "images/clubs/api/rendered/50-448f2e57b69e.png"}}, {"label": "май 2026", "value_label": "€90 млн", "value": 90, "club": {"slug": "atletico-madrid", "name": "Atlético Madrid", "short": "ATM", "api_id": 530, "period": "с 2024", "logo": "images/clubs/api/rendered/530-33037c80387a.png"}}, {"label": "июнь 2026", "value_label": "€100 млн", "value": 100, "club": {"slug": "atletico-madrid", "name": "Atlético Madrid", "short": "ATM", "api_id": 530, "period": "с 2024", "logo": "images/clubs/api/rendered/530-33037c80387a.png"}}]}, {"key": "anderson", "name": "Эллиот Андерсон", "paths": ["/transfers/elliot-anderson-manchester-city/"], "points": [{"label": "2022", "value_label": "€200 тыс.", "value": 0.2, "club": {"slug": "newcastle", "name": "Newcastle United", "short": "NEW", "api_id": 34, "period": "2021–2024", "logo": "images/clubs/api/rendered/34-7cda9da7ec14.png"}}, {"label": "2024", "value_label": "€15 млн", "value": 15, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NFO", "api_id": 65, "period": "с 2024", "logo": "images/clubs/api/rendered/65-ac04faa7320d.png"}}, {"label": "2025", "value_label": "€60 млн", "value": 60, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NFO", "api_id": 65, "period": "с 2024", "logo": "images/clubs/api/rendered/65-ac04faa7320d.png"}}, {"label": "2026", "value_label": "€75 млн", "value": 75, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NFO", "api_id": 65, "period": "с 2024", "logo": "images/clubs/api/rendered/65-ac04faa7320d.png"}}]}, {"key": "bernardo", "name": "Bernardo Silva", "paths": ["/transfers/bernardo-silva-real-madrid/"], "points": [{"label": "2013", "value_label": "€600 тыс.", "value": 0.6, "club": {"slug": "tm-10330", "name": "SL Benfica B", "short": "SBB", "api_id": null, "period": "2013", "logo": "images/clubs/chart/tm-10330.png"}}, {"label": "2015", "value_label": "€3,50 млн", "value": 3.5, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2014–2016", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "2017", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2014–2016", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "2018", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2017", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2019", "value_label": "€100 млн", "value": 100.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2017", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2020", "value_label": "€80 млн", "value": 80.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2017", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2026", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2017", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}]}, {"key": "de-ligt", "name": "Matthijs de Ligt", "paths": ["/transfers/matthijs-de-ligt/"], "points": [{"label": "2016/17", "value_label": "€0,1 млн", "value": 0.1, "club": {"slug": "ajax", "name": "Ajax U21", "short": "AJX", "api_id": 194, "period": "2016–2017", "logo": "images/clubs/api/194.png"}}, {"label": "2019", "value_label": "€75 млн", "value": 75, "club": {"slug": "ajax", "name": "Ajax", "short": "AJX", "api_id": 194, "period": "2016–2019", "logo": "images/clubs/api/194.png"}}, {"label": "2022", "value_label": "€70 млн", "value": 70, "club": {"slug": "juventus", "name": "Juventus", "short": "JUV", "api_id": 496, "period": "2019–2022", "logo": "images/clubs/api/rendered/496-c2b524a66b15.png"}}, {"label": "2024", "value_label": "€65 млн", "value": 65, "club": {"slug": "bayern-munich", "name": "Bayern Munich", "short": "FCB", "api_id": 157, "period": "2022–2024", "logo": "images/clubs/api/157.png"}}, {"label": "2026", "value_label": "€30 млн", "value": 30, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "с 2024", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}]}, {"key": "ramos", "name": "Gonçalo Ramos", "paths": ["/transfers/goncalo-ramos-ac-milan/"], "points": [{"label": "2020", "value_label": "€2 млн", "value": 2, "club": {"slug": "benfica", "name": "Benfica", "short": "SLB", "api_id": 211, "period": "2019–2023", "logo": "images/clubs/api/rendered/211-2874faa514fa.png"}}, {"label": "2022", "value_label": "€24 млн", "value": 24, "club": {"slug": "benfica", "name": "Benfica", "short": "SLB", "api_id": 211, "period": "2019–2023", "logo": "images/clubs/api/rendered/211-2874faa514fa.png"}}, {"label": "2023", "value_label": "€50 млн", "value": 50, "club": {"slug": "psg", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "2023–2026", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "2026", "value_label": "€75 млн", "value": 75, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2026", "logo": "images/clubs/api/rendered/489-a0582d29e9a1.png"}}]}, {"key": "yukhym-konoplia-step4", "name": "Yukhym Konoplia", "paths": ["/transfers/yukhym-konoplia-borussia-monchengladbach/"], "points": [{"label": "май 2019", "value_label": "€50 тыс.", "value": 0.05, "club": {"slug": "shakhtar-donetsk", "name": "Shakhtar Donetsk", "short": "SHA", "api_id": 550, "logo": "images/clubs/api/rendered/550-c053c3d0dc5f.png"}}, {"label": "янв. 2020", "value_label": "€800 тыс.", "value": 0.8, "club": {"slug": "desna-chernihiv", "name": "Desna Chernihiv", "short": "DES", "api_id": null}}, {"label": "апр. 2020", "value_label": "€725 тыс.", "value": 0.725, "club": {"slug": "desna-chernihiv", "name": "Desna Chernihiv", "short": "DES", "api_id": null}}, {"label": "июнь 2021", "value_label": "€2,5 млн", "value": 2.5, "club": {"slug": "desna-chernihiv", "name": "Desna Chernihiv", "short": "DES", "api_id": null}}, {"label": "дек. 2021", "value_label": "€2,5 млн", "value": 2.5, "club": {"slug": "shakhtar-donetsk", "name": "Shakhtar Donetsk", "short": "SHA", "api_id": 550, "logo": "images/clubs/api/rendered/550-c053c3d0dc5f.png"}}, {"label": "дек. 2024", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "shakhtar-donetsk", "name": "Shakhtar Donetsk", "short": "SHA", "api_id": 550, "logo": "images/clubs/api/rendered/550-c053c3d0dc5f.png"}}, {"label": "июнь 2026", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "borussia-monchengladbach", "name": "Borussia Mönchengladbach", "short": "BMG", "api_id": 163, "period": "с 2026", "logo": "images/clubs/api/rendered/163-b218cb7ec3e8.png"}}]}, {"key": "rocco-reitz-step4", "name": "Rocco Reitz", "paths": ["/transfers/rocco-reitz-rb-leipzig/"], "points": [{"label": "авг. 2020", "value": 0.05, "value_label": "€50 тыс.", "club": {"slug": "borussia-monchengladbach", "name": "Borussia Mönchengladbach", "short": "BMG", "api_id": 163, "period": "до 2026", "logo": "images/clubs/api/rendered/163-b218cb7ec3e8.png"}}, {"label": "февр. 2021", "value": 0.5, "value_label": "€500 тыс.", "club": {"slug": "borussia-monchengladbach", "name": "Borussia Mönchengladbach", "short": "BMG", "api_id": 163, "period": "до 2026", "logo": "images/clubs/api/rendered/163-b218cb7ec3e8.png"}}, {"label": "янв. 2022", "value": 0.5, "value_label": "€500 тыс.", "club": {"slug": "sint-truiden", "name": "Sint-Truiden VV", "short": "STVV", "period": "аренда"}}, {"label": "нояб. 2022", "value": 0.65, "value_label": "€650 тыс.", "club": {"slug": "borussia-monchengladbach", "name": "Borussia Mönchengladbach", "short": "BMG", "api_id": 163, "period": "до 2026", "logo": "images/clubs/api/rendered/163-b218cb7ec3e8.png"}}, {"label": "июнь 2023", "value": 0.8, "value_label": "€800 тыс.", "club": {"slug": "sint-truiden", "name": "Sint-Truiden VV", "short": "STVV", "period": "аренда"}}, {"label": "окт. 2023", "value": 4.0, "value_label": "€4 млн", "club": {"slug": "borussia-monchengladbach", "name": "Borussia Mönchengladbach", "short": "BMG", "api_id": 163, "period": "до 2026", "logo": "images/clubs/api/rendered/163-b218cb7ec3e8.png"}}, {"label": "мар. 2026", "value": 20.0, "value_label": "€20 млн", "club": {"slug": "borussia-monchengladbach", "name": "Borussia Mönchengladbach", "short": "BMG", "api_id": 163, "period": "до 2026", "logo": "images/clubs/api/rendered/163-b218cb7ec3e8.png"}}, {"label": "май 2026", "value": 20.0, "value_label": "€20 млн", "club": {"slug": "rb-leipzig", "name": "RB Leipzig", "short": "RBL", "api_id": 173, "period": "с 2026", "logo": "images/clubs/api/rendered/173-d38d0dff9d91.png"}}]}, {"key": "piero-hincapie-step4", "name": "Piero Hincapié", "paths": ["/transfers/piero-hincapie-arsenal/"], "points": [{"label": "янв. 2020", "value": 0.1, "value_label": "€100 тыс.", "club": {"slug": "independiente-del-valle", "name": "Independiente del Valle", "short": "IDV", "api_id": 1153, "period": "до 2020"}}, {"label": "февр. 2021", "value": 0.7, "value_label": "€700 тыс.", "club": {"slug": "talleres-cordoba", "name": "CA Talleres", "short": "TAL", "api_id": 456, "period": "до 2021"}}, {"label": "дек. 2021", "value": 13.0, "value_label": "€13 млн", "club": {"slug": "bayer-leverkusen", "name": "Bayer Leverkusen", "short": "B04", "api_id": 168, "period": "2021–2026", "logo": "images/clubs/api/rendered/168-780bfce19ea9.png"}}, {"label": "сент. 2022", "value": 22.0, "value_label": "€22 млн", "club": {"slug": "bayer-leverkusen", "name": "Bayer Leverkusen", "short": "B04", "api_id": 168, "period": "2021–2026", "logo": "images/clubs/api/rendered/168-780bfce19ea9.png"}}, {"label": "дек. 2022", "value": 25.0, "value_label": "€25 млн", "club": {"slug": "bayer-leverkusen", "name": "Bayer Leverkusen", "short": "B04", "api_id": 168, "period": "2021–2026", "logo": "images/clubs/api/rendered/168-780bfce19ea9.png"}}, {"label": "мар. 2025", "value": 50.0, "value_label": "€50 млн", "club": {"slug": "bayer-leverkusen", "name": "Bayer Leverkusen", "short": "B04", "api_id": 168, "period": "2021–2026", "logo": "images/clubs/api/rendered/168-780bfce19ea9.png"}}, {"label": "дек. 2025", "value": 50.0, "value_label": "€50 млн", "club": {"slug": "arsenal", "name": "Arsenal", "short": "ARS", "api_id": 42, "period": "с 2026", "logo": "images/clubs/api/rendered/42-ba273b85e8fe.png"}}, {"label": "июнь 2026", "value": 50.0, "value_label": "€50 млн", "club": {"slug": "arsenal", "name": "Arsenal", "short": "ARS", "api_id": 42, "period": "с 2026", "logo": "images/clubs/api/rendered/42-ba273b85e8fe.png"}}]}, {"key": "oskar-wojcik-step4", "name": "Oskar Wójcik", "paths": ["/transfers/oskar-wojcik-werder-bremen/"], "points": [{"label": "2025", "value": 0.025, "value_label": "€25 тыс.", "club": {"slug": "cracovia", "name": "Cracovia", "short": "CRA", "period": "до 2026", "api_id": 350, "logo": "images/clubs/api/rendered/350-3e65f1616aa4.png"}}, {"label": "03.2026", "value": 3.0, "value_label": "€3 млн", "club": {"slug": "cracovia", "name": "Cracovia", "short": "CRA", "period": "до 2026", "api_id": 350, "logo": "images/clubs/api/rendered/350-3e65f1616aa4.png"}}, {"label": "06.2026", "value": 5.0, "value_label": "€5 млн", "club": {"slug": "werder-bremen", "name": "Werder Bremen", "short": "SVW", "api_id": 162, "period": "с 2026", "logo": "images/clubs/api/rendered/162-076ca6ba9cbf.png"}}]}, {"key": "lesley-ugochukwu-step4", "name": "Lesley Ugochukwu", "paths": ["/transfers/lesley-ugochukwu-galatasaray/"], "points": [{"label": "мар. 2021", "value_label": "€300 тыс.", "value": 0.3, "club": {"slug": "tm-8154", "name": "Stade Rennais FC B", "short": "SRF", "api_id": null, "period": "2020", "logo": "images/clubs/chart/tm-8154.png"}}, {"label": "окт. 2021", "value_label": "€1,50 млн", "value": 1.5, "club": {"slug": "stade-rennais-fc", "name": "Stade Rennais FC", "short": "SRF", "api_id": 94, "period": "2021–2022", "logo": "images/clubs/tm/rendered/273-f2f787987183.png"}}, {"label": "2023", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "2023", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2024", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "tm-180", "name": "Southampton FC", "short": "SOU", "api_id": null, "period": "2024", "logo": "images/clubs/chart/tm-180.png"}}, {"label": "мар. 2025", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "tm-180", "name": "Southampton FC", "short": "SOU", "api_id": null, "period": "2024", "logo": "images/clubs/chart/tm-180.png"}}, {"label": "окт. 2025", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "tm-1132", "name": "Burnley FC", "short": "BUR", "api_id": null, "period": "с 2025", "logo": "images/clubs/chart/tm-1132.png"}}, {"label": "2026", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "tm-1132", "name": "Burnley FC", "short": "BUR", "api_id": null, "period": "с 2025", "logo": "images/clubs/chart/tm-1132.png"}}]}, {"key": "jaidon-anthony-step4", "name": "Jaidon Anthony", "paths": ["/transfers/jaidon-anthony-brentford/"], "points": [{"label": "2020", "value_label": "€150 тыс.", "value": 0.15, "club": {"slug": "afc-bournemouth", "name": "AFC Bournemouth", "short": "BOU", "api_id": 35, "period": "2020–2022", "logo": "images/clubs/api/rendered/35-e668d998ce23.png"}}, {"label": "2022", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "afc-bournemouth", "name": "AFC Bournemouth", "short": "BOU", "api_id": 35, "period": "2020–2022", "logo": "images/clubs/api/rendered/35-e668d998ce23.png"}}, {"label": "июнь 2023", "value_label": "€9 млн", "value": 9.0, "club": {"slug": "afc-bournemouth", "name": "AFC Bournemouth", "short": "BOU", "api_id": 35, "period": "2020–2022", "logo": "images/clubs/api/rendered/35-e668d998ce23.png"}}, {"label": "дек. 2023", "value_label": "€6,50 млн", "value": 6.5, "club": {"slug": "leeds-united", "name": "Leeds United", "short": "LEE", "api_id": 63, "period": "2023", "logo": "images/clubs/api/rendered/63-9f58f9f706d4.png"}}, {"label": "2024", "value_label": "€5,50 млн", "value": 5.5, "club": {"slug": "tm-1132", "name": "Burnley FC", "short": "BUR", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-1132.png"}}, {"label": "2025", "value_label": "€14 млн", "value": 14.0, "club": {"slug": "tm-1132", "name": "Burnley FC", "short": "BUR", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-1132.png"}}, {"label": "2026", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "tm-1132", "name": "Burnley FC", "short": "BUR", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-1132.png"}}]}, {"key": "nobel-mendy-step4", "name": "Nobel Mendy", "paths": ["/transfers/nobel-mendy-hull-city/"], "points": [{"label": "июнь 2024", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "betis-deportivo", "name": "Betis Deportivo", "short": "BET", "api_id": null, "period": "2023–2024"}}, {"label": "июль 2025", "value_label": "€4 млн", "value": 4.0, "club": {"slug": "real-betis", "name": "Real Betis", "short": "BET", "api_id": 543, "period": "2024–2025", "logo": "images/clubs/api/543.png"}}, {"label": "дек. 2025", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "rayo-vallecano", "name": "Rayo Vallecano", "short": "RAY", "api_id": 728, "period": "2025–2026", "logo": "images/clubs/api/rendered/728-9b826173203d.png"}}, {"label": "июнь 2026", "value_label": "€7,5 млн", "value": 7.5, "club": {"slug": "hull-city", "name": "Hull City", "short": "HUL", "api_id": 64, "period": "с 2026", "logo": "images/clubs/api/rendered/64-e5825be5ee17.png"}}]}, {"key": "joao-gomes-step4", "name": "João Gomes", "paths": ["/transfers/joao-gomes-aston-villa/"], "points": [{"label": "фев. 2021", "value_label": "€500 тыс.", "value": 0.5, "club": {"slug": "tm-15002", "name": "CR Flamengo U20", "short": "CFU", "api_id": null, "period": "", "logo": "images/clubs/chart/tm-15002.png"}}, {"label": "май 2021", "value_label": "€3,50 млн", "value": 3.5, "club": {"slug": "tm-614", "name": "CR Flamengo", "short": "CR", "api_id": null, "period": "2020–2021", "logo": "images/clubs/chart/tm-614.png"}}, {"label": "2023", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "tm-543", "name": "Wolverhampton Wanderers", "short": "WOL", "api_id": null, "period": "с 2022", "logo": "images/clubs/chart/tm-543.png"}}, {"label": "мар. 2024", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "tm-543", "name": "Wolverhampton Wanderers", "short": "WOL", "api_id": null, "period": "с 2022", "logo": "images/clubs/chart/tm-543.png"}}, {"label": "май 2024", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "tm-543", "name": "Wolverhampton Wanderers", "short": "WOL", "api_id": null, "period": "с 2022", "logo": "images/clubs/chart/tm-543.png"}}, {"label": "окт. 2024", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "tm-543", "name": "Wolverhampton Wanderers", "short": "WOL", "api_id": null, "period": "с 2022", "logo": "images/clubs/chart/tm-543.png"}}, {"label": "2026", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "tm-543", "name": "Wolverhampton Wanderers", "short": "WOL", "api_id": null, "period": "с 2022", "logo": "images/clubs/chart/tm-543.png"}}]}, {"key": "miguel-rodriguez-step4", "name": "Miguel Rodríguez", "paths": ["/transfers/miguel-rodriguez-deportivo-alaves/"], "points": [{"label": "2020", "value_label": "€600 тыс.", "value": 0.6, "club": {"slug": "tm-8733", "name": "RC Celta Fortuna", "short": "RCF", "api_id": null, "period": "2020–2022", "logo": "images/clubs/chart/tm-8733.png"}}, {"label": "2023", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "celta-de-vigo", "name": "Celta de Vigo", "short": "CEL", "api_id": 538, "period": "2022–2023", "logo": "images/clubs/api/538.png"}}, {"label": "2024", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "tm-200", "name": "FC Utrecht", "short": "FC", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-200.png"}}, {"label": "май 2025", "value_label": "€4,50 млн", "value": 4.5, "club": {"slug": "tm-200", "name": "FC Utrecht", "short": "FC", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-200.png"}}, {"label": "дек. 2025", "value_label": "€6,50 млн", "value": 6.5, "club": {"slug": "tm-200", "name": "FC Utrecht", "short": "FC", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-200.png"}}, {"label": "мар. 2026", "value_label": "€4,50 млн", "value": 4.5, "club": {"slug": "tm-200", "name": "FC Utrecht", "short": "FC", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-200.png"}}, {"label": "май 2026", "value_label": "€4,50 млн", "value": 4.5, "club": {"slug": "tm-200", "name": "FC Utrecht", "short": "FC", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-200.png"}}]}, {"key": "alvaro-rodriguez-step4", "name": "Álvaro Rodríguez", "paths": ["/transfers/alvaro-rodriguez-bournemouth/"], "points": [{"label": "2022", "value_label": "€200 тыс.", "value": 0.2, "club": {"slug": "tm-6767", "name": "Real Madrid Castilla", "short": "RMC", "api_id": null, "period": "2021–2023", "logo": "images/clubs/chart/tm-6767.png"}}, {"label": "фев. 2023", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "tm-6767", "name": "Real Madrid Castilla", "short": "RMC", "api_id": null, "period": "2021–2023", "logo": "images/clubs/chart/tm-6767.png"}}, {"label": "мар. 2023", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "tm-6767", "name": "Real Madrid Castilla", "short": "RMC", "api_id": null, "period": "2021–2023", "logo": "images/clubs/chart/tm-6767.png"}}, {"label": "окт. 2023", "value_label": "€4 млн", "value": 4.0, "club": {"slug": "tm-6767", "name": "Real Madrid Castilla", "short": "RMC", "api_id": null, "period": "2021–2023", "logo": "images/clubs/chart/tm-6767.png"}}, {"label": "2024", "value_label": "€3 млн", "value": 3.0, "club": {"slug": "getafe-cf", "name": "Getafe CF", "short": "GET", "api_id": 546, "period": "2024", "logo": "images/clubs/api/546.png"}}, {"label": "2025", "value_label": "€4 млн", "value": 4.0, "club": {"slug": "elche-cf", "name": "Elche CF", "short": "ELC", "api_id": 797, "period": "с 2025", "logo": "images/clubs/api/rendered/797-f8f6e27d0845.png"}}, {"label": "2026", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "elche-cf", "name": "Elche CF", "short": "ELC", "api_id": 797, "period": "с 2025", "logo": "images/clubs/api/rendered/797-f8f6e27d0845.png"}}]}, {"key": "aladji-bamba-step4", "name": "Aladji Bamba", "paths": ["/transfers/aladji-bamba-newcastle/"], "points": [{"label": "2024", "value_label": "€800 тыс.", "value": 0.8, "club": {"slug": "monaco", "name": "Monaco", "short": "MON", "api_id": 91, "period": "до 2026", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "дек. 2025", "value_label": "€3,5 млн", "value": 3.5, "club": {"slug": "monaco", "name": "Monaco", "short": "MON", "api_id": 91, "period": "до 2026", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "март 2026", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "monaco", "name": "Monaco", "short": "MON", "api_id": 91, "period": "до 2026", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "июнь 2026", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "newcastle", "name": "Newcastle", "short": "NEW", "api_id": 34, "period": "с 2026", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}]}, {"key": "sankhoun-diawara-step4", "name": "Sankhoun Diawara", "paths": ["/transfers/sankhoun-diawara-ac-milan/"], "points": [{"label": "нач. 2026", "value_label": "€25 тыс.", "value": 0.025, "club": {"slug": "troyes", "name": "Troyes", "short": "TRO", "api_id": 110, "period": "до 2026", "logo": "images/clubs/api/rendered/110-66d3f62462cd.png"}}, {"label": "весна 2026", "value_label": "€500 тыс.", "value": 0.5, "club": {"slug": "troyes", "name": "Troyes", "short": "TRO", "api_id": 110, "period": "до 2026", "logo": "images/clubs/api/rendered/110-66d3f62462cd.png"}}, {"label": "май 2026", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2026", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}]}, {"key": "luca-koleosho-step4", "name": "Luca Koleosho", "paths": ["/transfers/luca-koleosho-paris-fc/"], "points": [{"label": "2022", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "tm-10773", "name": "RCD Espanyol B", "short": "REB", "api_id": null, "period": "2022", "logo": "images/clubs/chart/tm-10773.png"}}, {"label": "окт. 2023", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "tm-1132", "name": "Burnley FC", "short": "BUR", "api_id": null, "period": "2023–2024", "logo": "images/clubs/chart/tm-1132.png"}}, {"label": "дек. 2023", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "tm-1132", "name": "Burnley FC", "short": "BUR", "api_id": null, "period": "2023–2024", "logo": "images/clubs/chart/tm-1132.png"}}, {"label": "2024", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "tm-1132", "name": "Burnley FC", "short": "BUR", "api_id": null, "period": "2023–2024", "logo": "images/clubs/chart/tm-1132.png"}}, {"label": "окт. 2025", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "rcd-espanyol-barcelona", "name": "RCD Espanyol Barcelona", "short": "REB", "api_id": 540, "period": "2025", "logo": "images/clubs/tm/rendered/714-da129c0be935.png"}}, {"label": "дек. 2025", "value_label": "€4 млн", "value": 4.0, "club": {"slug": "rcd-espanyol-barcelona", "name": "RCD Espanyol Barcelona", "short": "REB", "api_id": 540, "period": "2025", "logo": "images/clubs/tm/rendered/714-da129c0be935.png"}}, {"label": "2026", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "paris-fc", "name": "Paris FC", "short": "PAR", "api_id": 114, "period": "с 2025", "logo": "images/clubs/api/rendered/114-f681a4a91d58.png"}}]}, {"key": "luka-vuskovic-step4", "name": "Luka Vušković", "paths": ["/transfers/luka-vuskovic-brighton/"], "points": [{"label": "2023", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "tm-447", "name": "HNK Hajduk Split", "short": "HHS", "api_id": null, "period": "2022–2023", "logo": "images/clubs/chart/tm-447.png"}}, {"label": "июнь 2024", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "tm-7154", "name": "Radomiak Radom", "short": "RAD", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-7154.png"}}, {"label": "окт. 2024", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "tm-968", "name": "KVC Westerlo", "short": "KVC", "api_id": null, "period": "2024", "logo": "images/clubs/chart/tm-968.png"}}, {"label": "окт. 2025", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "hamburger-sv", "name": "Hamburger SV", "short": "HAM", "api_id": 175, "period": "с 2025", "logo": "images/clubs/api/rendered/175-4997c01a94f2.png"}}, {"label": "дек. 2025", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "hamburger-sv", "name": "Hamburger SV", "short": "HAM", "api_id": 175, "period": "с 2025", "logo": "images/clubs/api/rendered/175-4997c01a94f2.png"}}, {"label": "мар. 2026", "value_label": "€60 млн", "value": 60.0, "club": {"slug": "hamburger-sv", "name": "Hamburger SV", "short": "HAM", "api_id": 175, "period": "с 2025", "logo": "images/clubs/api/rendered/175-4997c01a94f2.png"}}, {"label": "май 2026", "value_label": "€60 млн", "value": 60.0, "club": {"slug": "hamburger-sv", "name": "Hamburger SV", "short": "HAM", "api_id": 175, "period": "с 2025", "logo": "images/clubs/api/rendered/175-4997c01a94f2.png"}}]}, {"key": "romelu-lukaku-step4", "name": "Romelu Lukaku", "paths": ["/transfers/romelu-lukaku-fenerbahce/"], "points": [{"label": "2009", "value_label": "€400 тыс.", "value": 0.4, "club": {"slug": "tm-49390", "name": "RSC Anderlecht U17", "short": "RAU", "api_id": null, "period": "", "logo": "images/clubs/chart/tm-49390.png"}}, {"label": "2018", "value_label": "€100 млн", "value": 100.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "2017–2018", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}, {"label": "2021", "value_label": "€100 млн", "value": 100.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "2011–2021", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2022", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "inter-milan", "name": "Inter Milan", "short": "INT", "api_id": 505, "period": "2019–2022", "logo": "images/clubs/api/rendered/505-14c915ad4d30.png"}}, {"label": "2023", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "as-roma", "name": "AS Roma", "short": "ROM", "api_id": 497, "period": "2023", "logo": "images/clubs/api/497.png"}}, {"label": "2024", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "ssc-napoli", "name": "SSC Napoli", "short": "NAP", "api_id": 492, "period": "с 2024", "logo": "images/clubs/api/rendered/492-1ca3923a25a9.png"}}, {"label": "2026", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "ssc-napoli", "name": "SSC Napoli", "short": "NAP", "api_id": 492, "period": "с 2024", "logo": "images/clubs/api/rendered/492-1ca3923a25a9.png"}}]}, {"key": "andrey-santos-step3", "name": "Andrey Santos", "paths": ["/transfers/andrey-santos-manchester-united/"], "points": [{"label": "янв. 2023", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "chelsea", "name": "Chelsea", "short": "CHE", "api_id": 49, "period": "2023 / 2025-2026", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "март 2023", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "vasco-da-gama", "name": "Vasco da Gama", "short": "VAS", "api_id": null, "period": "2023"}}, {"label": "июнь 2023", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "chelsea", "name": "Chelsea", "short": "CHE", "api_id": 49, "period": "2023 / 2025-2026", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "авг. 2023", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NFO", "api_id": 65, "period": "2023-2024", "logo": "images/clubs/chart/nottingham-forest.png"}}, {"label": "2024", "value_label": "€14 млн", "value": 14.0, "club": {"slug": "strasbourg", "name": "Strasbourg", "short": "STR", "api_id": 95, "period": "2024-2025", "logo": "images/clubs/api/95.png"}}, {"label": "март 2025", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "strasbourg", "name": "Strasbourg", "short": "STR", "api_id": 95, "period": "2024-2025", "logo": "images/clubs/api/95.png"}}, {"label": "2026", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "chelsea", "name": "Chelsea", "short": "CHE", "api_id": 49, "period": "2023 / 2025-2026", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "июнь 2026", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "с 2026", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}]}, {"key": "anthony-gordon-step3", "name": "Anthony Gordon", "paths": ["/transfers/anthony-gordon-barcelona/"], "points": [{"label": "2019", "value_label": "€1,50 млн", "value": 1.5, "club": {"slug": "everton-fc", "name": "Everton FC", "short": "EVE", "api_id": 45, "period": "2019–2022", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "мар. 2021", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "tm-466", "name": "Preston North End", "short": "PNE", "api_id": null, "period": "2020", "logo": "images/clubs/chart/tm-466.png"}}, {"label": "дек. 2021", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "everton-fc", "name": "Everton FC", "short": "EVE", "api_id": 45, "period": "2019–2022", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "2022", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "everton-fc", "name": "Everton FC", "short": "EVE", "api_id": 45, "period": "2019–2022", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "2023", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "2022–2025", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}, {"label": "2024", "value_label": "€60 млн", "value": 60.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "2022–2025", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}, {"label": "2026", "value_label": "€80 млн", "value": 80.0, "club": {"slug": "fc-barcelona", "name": "FC Barcelona", "short": "BAR", "api_id": 529, "period": "с 2026", "logo": "images/clubs/api/rendered/529-921329187f25.png"}}]}, {"key": "johan-manzambi-step3", "name": "Johan Manzambi", "paths": ["/transfers/johan-manzambi-aston-villa/"], "points": [{"label": "2023", "value_label": "€150 тыс.", "value": 0.15, "club": {"slug": "tm-245", "name": "SC Freiburg II", "short": "SFI", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-245.png"}}, {"label": "2024", "value_label": "€750 тыс.", "value": 0.75, "club": {"slug": "sc-freiburg", "name": "SC Freiburg", "short": "FRE", "api_id": 160, "period": "2024–2025", "logo": "images/clubs/api/rendered/160-54f643a63e51.png"}}, {"label": "июнь 2025", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "sc-freiburg", "name": "SC Freiburg", "short": "FRE", "api_id": 160, "period": "2024–2025", "logo": "images/clubs/api/rendered/160-54f643a63e51.png"}}, {"label": "окт. 2025", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "sc-freiburg", "name": "SC Freiburg", "short": "FRE", "api_id": 160, "period": "2024–2025", "logo": "images/clubs/api/rendered/160-54f643a63e51.png"}}, {"label": "дек. 2025", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "sc-freiburg", "name": "SC Freiburg", "short": "FRE", "api_id": 160, "period": "2024–2025", "logo": "images/clubs/api/rendered/160-54f643a63e51.png"}}, {"label": "май 2026", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "sc-freiburg", "name": "SC Freiburg", "short": "FRE", "api_id": 160, "period": "2024–2025", "logo": "images/clubs/api/rendered/160-54f643a63e51.png"}}, {"label": "июль 2026", "value_label": "€65 млн", "value": 65.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2026", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}]}, {"key": "bazoumana-toure-step3", "name": "Bazoumana Touré", "paths": ["/transfers/bazoumana-toure-newcastle-united/"], "points": [{"label": "2024", "value_label": "€3,50 млн", "value": 3.5, "club": {"slug": "tm-1059", "name": "Hammarby IF", "short": "HAM", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-1059.png"}}, {"label": "июнь 2025", "value_label": "€9 млн", "value": 9.0, "club": {"slug": "tsg-1899-hoffenheim", "name": "TSG 1899 Hoffenheim", "short": "HOF", "api_id": 167, "period": "2024–2025", "logo": "images/clubs/api/rendered/167-d3563d9ffa1e.png"}}, {"label": "окт. 2025", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "tsg-1899-hoffenheim", "name": "TSG 1899 Hoffenheim", "short": "HOF", "api_id": 167, "period": "2024–2025", "logo": "images/clubs/api/rendered/167-d3563d9ffa1e.png"}}, {"label": "дек. 2025", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "tsg-1899-hoffenheim", "name": "TSG 1899 Hoffenheim", "short": "HOF", "api_id": 167, "period": "2024–2025", "logo": "images/clubs/api/rendered/167-d3563d9ffa1e.png"}}, {"label": "мар. 2026", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "tsg-1899-hoffenheim", "name": "TSG 1899 Hoffenheim", "short": "HOF", "api_id": 167, "period": "2024–2025", "logo": "images/clubs/api/rendered/167-d3563d9ffa1e.png"}}, {"label": "май 2026", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "tsg-1899-hoffenheim", "name": "TSG 1899 Hoffenheim", "short": "HOF", "api_id": 167, "period": "2024–2025", "logo": "images/clubs/api/rendered/167-d3563d9ffa1e.png"}}, {"label": "июль 2026", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "с 2026", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}]}, {"key": "christos-tzolis-step3", "name": "Christos Tzolis", "paths": ["/transfers/christos-tzolis-arsenal/"], "points": [{"label": "2020", "value_label": "€400 тыс.", "value": 0.4, "club": {"slug": "tm-1091", "name": "PAOK Thessaloniki", "short": "PAO", "api_id": null, "period": "2020", "logo": "images/clubs/chart/tm-1091.png"}}, {"label": "2021", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "tm-1123", "name": "Norwich City", "short": "NOR", "api_id": null, "period": "2021–2022", "logo": "images/clubs/chart/tm-1123.png"}}, {"label": "2022", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "tm-317", "name": "FC Twente Enschede", "short": "FTE", "api_id": null, "period": "2022", "logo": "images/clubs/chart/tm-317.png"}}, {"label": "июнь 2023", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "tm-1123", "name": "Norwich City", "short": "NOR", "api_id": null, "period": "2021–2022", "logo": "images/clubs/chart/tm-1123.png"}}, {"label": "дек. 2023", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "tm-38", "name": "Fortuna Düsseldorf", "short": "FOR", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-38.png"}}, {"label": "2024", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "tm-2282", "name": "Club Brugge KV", "short": "CBK", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-2282.png"}}, {"label": "2026", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "tm-2282", "name": "Club Brugge KV", "short": "CBK", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-2282.png"}}]}, {"key": "yan-diomande-step3", "name": "Yan Diomande", "paths": ["/transfers/yan-diomande-real-madrid/"], "points": [{"label": "июнь 2025", "value_label": "€1,5 млн", "value": 1.5, "club": {"slug": "cd-leganes", "name": "CD Leganés", "short": "LEG", "api_id": null, "period": "2025"}}, {"label": "окт. 2025", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "rb-leipzig", "name": "RB Leipzig", "short": "RBL", "api_id": 173, "period": "2025–2026", "logo": "images/clubs/api/rendered/173-d38d0dff9d91.png"}}, {"label": "дек. 2025", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "rb-leipzig", "name": "RB Leipzig", "short": "RBL", "api_id": 173, "period": "2025–2026", "logo": "images/clubs/api/rendered/173-d38d0dff9d91.png"}}, {"label": "март 2026", "value_label": "€75 млн", "value": 75.0, "club": {"slug": "rb-leipzig", "name": "RB Leipzig", "short": "RBL", "api_id": 173, "period": "2025–2026", "logo": "images/clubs/api/rendered/173-d38d0dff9d91.png"}}, {"label": "май 2026", "value_label": "€90 млн", "value": 90.0, "club": {"slug": "real-madrid", "name": "Real Madrid", "short": "RMA", "api_id": 541, "period": "с 2026", "logo": "images/clubs/api/rendered/541-9a1b10dacb76.png"}}]}, {"key": "julio-enciso-step4", "name": "Julio Enciso", "paths": ["/transfers/julio-enciso-ipswich-town/"], "points": [{"label": "янв. 2021", "value_label": "€0,5 млн", "value": 0.5, "club": {"slug": "club-libertad", "name": "Club Libertad", "short": "LIB", "api_id": null, "period": "2021–2022"}}, {"label": "июль 2022", "value_label": "€11 млн", "value": 11.0, "club": {"slug": "brighton-and-hove-albion", "name": "Brighton & Hove Albion", "short": "BHA", "api_id": 51, "period": "2022–2025", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "янв. 2025", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "ipswich-town", "name": "Ipswich Town", "short": "IPS", "api_id": 57, "period": "2025 / с 2026", "logo": "images/clubs/api/rendered/57-1362c589ddf7.png"}}, {"label": "сент. 2025", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "strasbourg", "name": "Strasbourg", "short": "STR", "api_id": 95, "period": "2025–2026", "logo": "images/clubs/api/rendered/95-94fa45143780.png"}}, {"label": "дек. 2025", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "strasbourg", "name": "Strasbourg", "short": "STR", "api_id": 95, "period": "2025–2026", "logo": "images/clubs/api/rendered/95-94fa45143780.png"}}, {"label": "июнь 2026", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "ipswich-town", "name": "Ipswich Town", "short": "IPS", "api_id": 57, "period": "2025 / с 2026", "logo": "images/clubs/api/rendered/57-1362c589ddf7.png"}}]}, {"key": "ferran-torres-step4", "name": "Ferran Torres", "paths": ["/transfers/ferran-torres-psg/"], "points": [{"label": "2018/19", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "valencia", "name": "Valencia", "short": "VAL", "api_id": 532, "period": "2018–2020", "logo": "images/clubs/api/532.png"}}, {"label": "авг. 2020", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "2020–2021", "logo": "images/clubs/api/50.png"}}, {"label": "янв. 2022", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "barcelona", "name": "Barcelona", "short": "BAR", "api_id": 529, "period": "2022–2026", "logo": "images/clubs/api/rendered/529-921329187f25.png"}}, {"label": "июнь 2025", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "barcelona", "name": "Barcelona", "short": "BAR", "api_id": 529, "period": "2022–2026", "logo": "images/clubs/api/rendered/529-921329187f25.png"}}, {"label": "дек. 2025", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "barcelona", "name": "Barcelona", "short": "BAR", "api_id": 529, "period": "2022–2026", "logo": "images/clubs/api/rendered/529-921329187f25.png"}}, {"label": "июнь 2026", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2026", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}]}, {"key": "cristian-romero-step4", "name": "Cristian Romero", "paths": ["/transfers/cristian-romero-atletico-madrid/"], "points": [{"label": "2016", "value_label": "€150 тыс.", "value": 0.15, "club": {"slug": "tm-61444", "name": "CA Belgrano II", "short": "CBI", "api_id": null, "period": "2015", "logo": "images/clubs/chart/tm-61444.png"}}, {"label": "2017", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "tm-2417", "name": "Club Atlético Belgrano", "short": "CAB", "api_id": null, "period": "2016–2017", "logo": "images/clubs/chart/tm-2417.png"}}, {"label": "2018", "value_label": "€4 млн", "value": 4.0, "club": {"slug": "genoa-cfc", "name": "Genoa CFC", "short": "GEN", "api_id": 495, "period": "2018–2020", "logo": "images/clubs/api/495.png"}}, {"label": "2020", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "atalanta-bc", "name": "Atalanta BC", "short": "ATA", "api_id": 499, "period": "2020–2021", "logo": "images/clubs/api/499.png"}}, {"label": "2021", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2021", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2023", "value_label": "€65 млн", "value": 65.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2021", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2026", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2021", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}]}, {"key": "djed-spence-step4", "name": "Djed Spence", "paths": ["/transfers/djed-spence-inter/"], "points": [{"label": "2020", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "tm-641", "name": "Middlesbrough FC", "short": "MID", "api_id": null, "period": "2019–2020", "logo": "images/clubs/chart/tm-641.png"}}, {"label": "2022", "value_label": "€13 млн", "value": 13.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2022", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "июнь 2023", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "stade-rennais-fc", "name": "Stade Rennais FC", "short": "SRF", "api_id": 94, "period": "2022", "logo": "images/clubs/tm/rendered/273-f2f787987183.png"}}, {"label": "окт. 2023", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "leeds-united", "name": "Leeds United", "short": "LEE", "api_id": 63, "period": "2023", "logo": "images/clubs/api/rendered/63-9f58f9f706d4.png"}}, {"label": "июнь 2024", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "genoa-cfc", "name": "Genoa CFC", "short": "GEN", "api_id": 495, "period": "2023", "logo": "images/clubs/api/495.png"}}, {"label": "дек. 2024", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2022", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2026", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2022", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}]}, {"key": "geronimo-rulli-step4", "name": "Gerónimo Rulli", "paths": ["/transfers/geronimo-rulli-manchester-city/"], "points": [{"label": "2012", "value_label": "€100 тыс.", "value": 0.1, "club": {"slug": "tm-288", "name": "Club Estudiantes de La Plata", "short": "CED", "api_id": null, "period": "2012–2013", "logo": "images/clubs/chart/tm-288.png"}}, {"label": "2017", "value_label": "€14 млн", "value": 14.0, "club": {"slug": "real-sociedad", "name": "Real Sociedad", "short": "RSO", "api_id": 548, "period": "2014–2018", "logo": "images/clubs/api/548.png"}}, {"label": "2019", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "tm-969", "name": "Montpellier HSC", "short": "MON", "api_id": null, "period": "2019", "logo": "images/clubs/chart/tm-969.png"}}, {"label": "2020", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "villarreal-cf", "name": "Villarreal CF", "short": "VIL", "api_id": 533, "period": "2020–2022", "logo": "images/clubs/api/533.png"}}, {"label": "2023", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "tm-610", "name": "Ajax Amsterdam", "short": "AJA", "api_id": null, "period": "2022–2023", "logo": "images/clubs/chart/tm-610.png"}}, {"label": "2024", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "olympique-marseille", "name": "Olympique Marseille", "short": "MAR", "api_id": 81, "period": "с 2024", "logo": "images/clubs/api/rendered/81-f781160a86a8.png"}}, {"label": "2026", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "olympique-marseille", "name": "Olympique Marseille", "short": "MAR", "api_id": 81, "period": "с 2024", "logo": "images/clubs/api/rendered/81-f781160a86a8.png"}}]}, {"key": "shea-charles-step4", "name": "Shea Charles", "paths": ["/transfers/shea-charles-fulham/"], "points": [{"label": "авг. 2023", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "southampton", "name": "Southampton", "short": "SOU", "api_id": 41, "period": "2023–2026", "logo": "images/clubs/api/rendered/41-48793bd6be9f.png"}}, {"label": "авг. 2024", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "sheffield-wednesday", "name": "Sheffield Wednesday", "short": "SHW", "api_id": 74, "period": "2024–2025", "logo": "images/clubs/api/rendered/74-762c2c99e6f1.png"}}, {"label": "май 2025", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "southampton", "name": "Southampton", "short": "SOU", "api_id": 41, "period": "2023–2026", "logo": "images/clubs/api/rendered/41-48793bd6be9f.png"}}, {"label": "дек. 2025", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "southampton", "name": "Southampton", "short": "SOU", "api_id": 41, "period": "2023–2026", "logo": "images/clubs/api/rendered/41-48793bd6be9f.png"}}, {"label": "май 2026", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "fulham", "name": "Fulham", "short": "FUL", "api_id": 36, "period": "с 2026", "logo": "images/clubs/api/rendered/36-3735bd31a6c7.png"}}]}, {"key": "brennan-johnson-step4", "name": "Brennan Johnson", "paths": ["/transfers/brennan-johnson-everton/"], "points": [{"label": "2021", "value_label": "€400 тыс.", "value": 0.4, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NOT", "api_id": 65, "period": "2020–2022", "logo": "images/clubs/api/65.png"}}, {"label": "2022", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NOT", "api_id": 65, "period": "2020–2022", "logo": "images/clubs/api/65.png"}}, {"label": "мар. 2023", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NOT", "api_id": 65, "period": "2020–2022", "logo": "images/clubs/api/65.png"}}, {"label": "окт. 2023", "value_label": "€48 млн", "value": 48.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "2023–2025", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2024", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "2023–2025", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2025", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "2023–2025", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2026", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "crystal-palace", "name": "Crystal Palace", "short": "CRY", "api_id": 52, "period": "с 2025", "logo": "images/clubs/api/rendered/52-3a5b60eb010b.png"}}]}, {"key": "dwight-mcneil-step4", "name": "Dwight McNeil", "paths": ["/transfers/dwight-mcneil-crystal-palace/"], "points": [{"label": "июль 2020", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "burnley", "name": "Burnley", "short": "BUR", "api_id": 44, "period": "2018–2022", "logo": "images/clubs/api/rendered/44-1201390c0881.png"}}, {"label": "2022/23", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "everton", "name": "Everton", "short": "EVE", "api_id": 45, "period": "2022–2026", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "2023/24", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "everton", "name": "Everton", "short": "EVE", "api_id": 45, "period": "2022–2026", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "2024/25", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "everton", "name": "Everton", "short": "EVE", "api_id": 45, "period": "2022–2026", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "дек. 2025", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "everton", "name": "Everton", "short": "EVE", "api_id": 45, "period": "2022–2026", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "июнь 2026", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "crystal-palace", "name": "Crystal Palace", "short": "CRY", "api_id": 52, "period": "с авг. 2026", "logo": "images/clubs/api/rendered/52-3a5b60eb010b.png"}}]}, {"key": "amar-dedic-step4", "name": "Amar Dedić", "paths": ["/transfers/amar-dedic-newcastle/"], "points": [{"label": "2019", "value_label": "€75 тыс.", "value": 0.07, "club": {"slug": "tm-37024", "name": "FC Liefering", "short": "FC", "api_id": null, "period": "2019–2020", "logo": "images/clubs/chart/tm-37024.png"}}, {"label": "2021", "value_label": "€1,50 млн", "value": 1.5, "club": {"slug": "tm-4441", "name": "Wolfsberger AC", "short": "WOL", "api_id": null, "period": "2021", "logo": "images/clubs/chart/tm-4441.png"}}, {"label": "2022", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "tm-409", "name": "Red Bull Salzburg", "short": "RBS", "api_id": null, "period": "2020–2024", "logo": "images/clubs/chart/tm-409.png"}}, {"label": "2023", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "tm-409", "name": "Red Bull Salzburg", "short": "RBS", "api_id": null, "period": "2020–2024", "logo": "images/clubs/chart/tm-409.png"}}, {"label": "июнь 2025", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "olympique-marseille", "name": "Olympique Marseille", "short": "MAR", "api_id": 81, "period": "2024", "logo": "images/clubs/api/rendered/81-f781160a86a8.png"}}, {"label": "сен. 2025", "value_label": "€13 млн", "value": 13.0, "club": {"slug": "sl-benfica", "name": "SL Benfica", "short": "BEN", "api_id": 211, "period": "с 2025", "logo": "images/clubs/api/rendered/211-2874faa514fa.png"}}, {"label": "2026", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "sl-benfica", "name": "SL Benfica", "short": "BEN", "api_id": 211, "period": "с 2025", "logo": "images/clubs/api/rendered/211-2874faa514fa.png"}}]}, {"key": "guglielmo-vicario-step4", "name": "Guglielmo Vicario", "paths": ["/transfers/guglielmo-vicario-juventus/"], "points": [{"label": "2013", "value_label": "€50 тыс.", "value": 0.05, "club": {"slug": "tm-10959", "name": "Udinese Primavera", "short": "UDI", "api_id": null, "period": "2013", "logo": "images/clubs/chart/tm-10959.png"}}, {"label": "2019", "value_label": "€1,20 млн", "value": 1.2, "club": {"slug": "tm-839", "name": "AC Perugia Calcio", "short": "APC", "api_id": null, "period": "2019–2020", "logo": "images/clubs/chart/tm-839.png"}}, {"label": "2020", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "cagliari-calcio", "name": "Cagliari Calcio", "short": "CAG", "api_id": 490, "period": "2020", "logo": "images/clubs/api/490.png"}}, {"label": "2021", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "tm-749", "name": "FC Empoli", "short": "FC", "api_id": null, "period": "2021–2022", "logo": "images/clubs/chart/tm-749.png"}}, {"label": "2023", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2023", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2024", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2023", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2026", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2023", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}]}, {"key": "michy-batshuayi-step4", "name": "Michy Batshuayi", "paths": ["/transfers/michy-batshuayi-abha/"], "points": [{"label": "2011", "value_label": "€50 тыс.", "value": 0.05, "club": {"slug": "tm-3057", "name": "Standard Liège", "short": "STA", "api_id": null, "period": "2011–2013", "logo": "images/clubs/chart/tm-3057.png"}}, {"label": "2018", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "borussia-dortmund", "name": "Borussia Dortmund", "short": "DOR", "api_id": 165, "period": "2017", "logo": "images/clubs/api/165.png"}}, {"label": "2021", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "besiktas-jk", "name": "Besiktas JK", "short": "BES", "api_id": 549, "period": "2021", "logo": "images/clubs/api/549.png"}}, {"label": "2022", "value_label": "€9,50 млн", "value": 9.5, "club": {"slug": "fenerbahce", "name": "Fenerbahce", "short": "FEN", "api_id": 611, "period": "2022–2023", "logo": "images/clubs/api/rendered/611-26561183c779.png"}}, {"label": "2024", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "galatasaray", "name": "Galatasaray", "short": "GAL", "api_id": 645, "period": "2024", "logo": "images/clubs/api/rendered/645-4722b4796f98.png"}}, {"label": "2025", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "eintracht-frankfurt", "name": "Eintracht Frankfurt", "short": "EIN", "api_id": 169, "period": "с 2024", "logo": "images/clubs/api/rendered/169-bdd9ff4272f0.png"}}, {"label": "2026", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "eintracht-frankfurt", "name": "Eintracht Frankfurt", "short": "EIN", "api_id": 169, "period": "с 2024", "logo": "images/clubs/api/rendered/169-bdd9ff4272f0.png"}}]}, {"key": "mahmoud-trezeguet-step4", "name": "Mahmoud Trezeguet", "paths": ["/transfers/mahmoud-trezeguet-al-riyadh/"], "points": [{"label": "июль 2019", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AVL", "api_id": 66, "period": "2019–2022", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "июль 2022", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "trabzonspor", "name": "Trabzonspor", "short": "TRA", "api_id": 998, "period": "2022–2025", "logo": "images/clubs/api/998.png"}}, {"label": "сент. 2024", "value_label": "€8,5 млн", "value": 8.5, "club": {"slug": "al-rayyan", "name": "Al-Rayyan", "short": "RAY", "api_id": 2897, "period": "2024–2025", "logo": "images/clubs/api/rendered/2897-fb02d191c0ff.png"}}, {"label": "июнь 2025", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "al-ahly", "name": "Al Ahly", "short": "AHL", "api_id": 1577, "period": "2025–2026", "logo": "images/clubs/api/rendered/1577-0f786f981cdc.png"}}, {"label": "май 2026", "value_label": "€4,5 млн", "value": 4.5, "club": {"slug": "al-riyadh", "name": "Al-Riyadh", "short": "RIY", "api_id": 10511, "period": "с авг. 2026", "logo": "images/clubs/api/rendered/10511-30496d9efb45.png"}}]}, {"key": "anthony-patterson-step4", "name": "Anthony Patterson", "paths": ["/transfers/anthony-patterson-wrexham/"], "points": [{"label": "2024/25", "value_label": "€14 млн", "value": 14.0, "club": {"slug": "sunderland", "name": "Sunderland", "short": "SUN", "api_id": 746, "period": "до авг. 2026", "logo": "images/clubs/api/rendered/746-4ebea02c3573.png"}}, {"label": "дек. 2025", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "sunderland", "name": "Sunderland", "short": "SUN", "api_id": 746, "period": "до авг. 2026", "logo": "images/clubs/api/rendered/746-4ebea02c3573.png"}}, {"label": "февр. 2026", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "millwall", "name": "Millwall", "short": "MIL", "api_id": 58, "period": "февр.–июнь 2026", "logo": "images/clubs/api/rendered/58-efc3a3c31918.png"}}, {"label": "март 2026", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "millwall", "name": "Millwall", "short": "MIL", "api_id": 58, "period": "февр.–июнь 2026", "logo": "images/clubs/api/rendered/58-efc3a3c31918.png"}}, {"label": "май 2026", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "wrexham", "name": "Wrexham", "short": "WRE", "api_id": 1837, "period": "с авг. 2026", "logo": "images/clubs/api/rendered/1837-4f30bb39094c.png"}}]}, {"key": "ollie-watkins-step4", "name": "Ollie Watkins", "paths": ["/transfers/ollie-watkins-al-hilal/"], "points": [{"label": "2016", "value_label": "€150 тыс.", "value": 0.15, "club": {"slug": "tm-6699", "name": "Exeter City", "short": "EXE", "api_id": null, "period": "2016", "logo": "images/clubs/chart/tm-6699.png"}}, {"label": "2017", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "brentford-fc", "name": "Brentford FC", "short": "BRE", "api_id": 55, "period": "2017–2019", "logo": "images/clubs/api/rendered/55-69278a7461b2.png"}}, {"label": "2020", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2020", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "2023", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2020", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "мар. 2024", "value_label": "€65 млн", "value": 65.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2020", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "дек. 2024", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2020", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "2026", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2020", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}]}, {"key": "bruno-guimaraes-step4", "name": "Bruno Guimarães", "paths": ["/transfers/bruno-guimaraes-arsenal/"], "points": [{"label": "2017", "value_label": "€50 тыс.", "value": 0.05, "club": {"slug": "tm-679", "name": "Club Athletico Paranaense", "short": "CAP", "api_id": null, "period": "2016–2018", "logo": "images/clubs/chart/tm-679.png"}}, {"label": "2019", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "tm-679", "name": "Club Athletico Paranaense", "short": "CAP", "api_id": null, "period": "2016–2018", "logo": "images/clubs/chart/tm-679.png"}}, {"label": "2020", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "olympique-lyon", "name": "Olympique Lyon", "short": "LYO", "api_id": 80, "period": "2019–2021", "logo": "images/clubs/api/80.png"}}, {"label": "июнь 2022", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "с 2021", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}, {"label": "сен. 2022", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "с 2021", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}, {"label": "2023", "value_label": "€85 млн", "value": 85.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "с 2021", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}, {"label": "2026", "value_label": "€70 млн", "value": 70.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "с 2021", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}]}, {"key": "carlos-baleba-step4", "name": "Carlos Baleba", "paths": ["/transfers/carlos-baleba-manchester-united/"], "points": [{"label": "май 2022", "value_label": "€150 тыс.", "value": 0.15, "club": {"slug": "tm-12765", "name": "LOSC Lille B", "short": "LLB", "api_id": null, "period": "2021", "logo": "images/clubs/chart/tm-12765.png"}}, {"label": "сен. 2022", "value_label": "€500 тыс.", "value": 0.5, "club": {"slug": "losc-lille", "name": "LOSC Lille", "short": "LIL", "api_id": 79, "period": "2022", "logo": "images/clubs/api/rendered/79-021579263933.png"}}, {"label": "2023", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "с 2023", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "2024", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "с 2023", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "май 2025", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "с 2023", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "окт. 2025", "value_label": "€60 млн", "value": 60.0, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "с 2023", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "2026", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "с 2023", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}]}, {"key": "bradley-barcola-step4", "name": "Bradley Barcola", "paths": ["/transfers/bradley-barcola-liverpool/"], "points": [{"label": "2022", "value_label": "€500 тыс.", "value": 0.5, "club": {"slug": "olympique-lyon", "name": "Olympique Lyon", "short": "LYO", "api_id": 80, "period": "2021–2022", "logo": "images/clubs/api/80.png"}}, {"label": "июнь 2023", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "olympique-lyon", "name": "Olympique Lyon", "short": "LYO", "api_id": 80, "period": "2021–2022", "logo": "images/clubs/api/80.png"}}, {"label": "окт. 2023", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2023", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "мар. 2024", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2023", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "июнь 2024", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2023", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "окт. 2024", "value_label": "€65 млн", "value": 65.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2023", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "2026", "value_label": "€90 млн", "value": 90.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2023", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}]}, {"key": "gabriel-jesus-barcelona-step4", "name": "Gabriel Jesus", "paths": ["/transfers/gabriel-jesus-barcelona/"], "points": [{"label": "2015", "value_label": "€750 тыс.", "value": 0.75, "club": {"slug": "tm-1023", "name": "Sociedade Esportiva Palmeiras", "short": "SEP", "api_id": null, "period": "2014–2015", "logo": "images/clubs/chart/tm-1023.png"}}, {"label": "фев. 2017", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "2016–2021", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "окт. 2017", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "2016–2021", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "янв. 2018", "value_label": "€70 млн", "value": 70.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "2016–2021", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "май 2018", "value_label": "€80 млн", "value": 80.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "2016–2021", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2022", "value_label": "€65 млн", "value": 65.0, "club": {"slug": "arsenal-fc", "name": "Arsenal FC", "short": "ARS", "api_id": 42, "period": "с 2022", "logo": "images/clubs/api/rendered/42-ba273b85e8fe.png"}}, {"label": "2026", "value_label": "€17 млн", "value": 17.0, "club": {"slug": "arsenal-fc", "name": "Arsenal FC", "short": "ARS", "api_id": 42, "period": "с 2022", "logo": "images/clubs/api/rendered/42-ba273b85e8fe.png"}}]}, {"key": "matias-fernandez-pardo-newcastle-step4", "name": "Matias Fernandez-Pardo", "paths": ["/transfers/matias-fernandez-pardo-newcastle/"], "points": [{"label": "2023", "value_label": "€400 тыс.", "value": 0.4, "club": {"slug": "tm-157", "name": "KAA Gent", "short": "KAA", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-157.png"}}, {"label": "окт. 2024", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "losc-lille", "name": "LOSC Lille", "short": "LIL", "api_id": 79, "period": "с 2024", "logo": "images/clubs/api/rendered/79-021579263933.png"}}, {"label": "дек. 2024", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "losc-lille", "name": "LOSC Lille", "short": "LIL", "api_id": 79, "period": "с 2024", "logo": "images/clubs/api/rendered/79-021579263933.png"}}, {"label": "июнь 2025", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "losc-lille", "name": "LOSC Lille", "short": "LIL", "api_id": 79, "period": "с 2024", "logo": "images/clubs/api/rendered/79-021579263933.png"}}, {"label": "окт. 2025", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "losc-lille", "name": "LOSC Lille", "short": "LIL", "api_id": 79, "period": "с 2024", "logo": "images/clubs/api/rendered/79-021579263933.png"}}, {"label": "мар. 2026", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "losc-lille", "name": "LOSC Lille", "short": "LIL", "api_id": 79, "period": "с 2024", "logo": "images/clubs/api/rendered/79-021579263933.png"}}, {"label": "июнь 2026", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "losc-lille", "name": "LOSC Lille", "short": "LIL", "api_id": 79, "period": "с 2024", "logo": "images/clubs/api/rendered/79-021579263933.png"}}]}, {"key": "alejandro-garnacho", "name": "Alejandro Garnacho", "paths": ["/transfers/alejandro-garnacho-aston-villa/"], "points": [{"label": "2022", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "2022–2024", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}, {"label": "мар. 2023", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "2022–2024", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}, {"label": "дек. 2023", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "2022–2024", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}, {"label": "мар. 2024", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "2022–2024", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}, {"label": "окт. 2024", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "2022–2024", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}, {"label": "2025", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2025", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2026", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2025", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}]}, {"key": "ansu-fati", "name": "Ansu Fati", "paths": ["/transfers/ansu-fati-monaco/"], "points": [{"label": "сен. 2019", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "tm-2470", "name": "FC Barcelona U19", "short": "FBU", "api_id": null, "period": "", "logo": "images/clubs/chart/tm-2470.png"}}, {"label": "дек. 2019", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "tm-2464", "name": "FC Barcelona Atlètic", "short": "FBA", "api_id": null, "period": "2019–2020", "logo": "images/clubs/chart/tm-2464.png"}}, {"label": "2020", "value_label": "€80 млн", "value": 80.0, "club": {"slug": "fc-barcelona", "name": "FC Barcelona", "short": "BAR", "api_id": 529, "period": "2020–2024", "logo": "images/clubs/api/rendered/529-921329187f25.png"}}, {"label": "2023", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "2023", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "2024", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "fc-barcelona", "name": "FC Barcelona", "short": "BAR", "api_id": 529, "period": "2020–2024", "logo": "images/clubs/api/rendered/529-921329187f25.png"}}, {"label": "2025", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "с 2025", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "2026", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "с 2025", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}]}, {"key": "j-r-my-jacquet", "name": "Jérémy Jacquet", "paths": ["/transfers/jeremy-jacquet-liverpool/"], "points": [{"label": "2023", "value_label": "€50 тыс.", "value": 0.05, "club": {"slug": "tm-8154", "name": "Stade Rennais FC B", "short": "SRF", "api_id": null, "period": "2022–2023", "logo": "images/clubs/chart/tm-8154.png"}}, {"label": "2024", "value_label": "€300 тыс.", "value": 0.3, "club": {"slug": "tm-3524", "name": "Clermont Foot 63", "short": "CF6", "api_id": null, "period": "2023–2024", "logo": "images/clubs/chart/tm-3524.png"}}, {"label": "мар. 2025", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "stade-rennais-fc", "name": "Stade Rennais FC", "short": "SRF", "api_id": 94, "period": "с 2024", "logo": "images/clubs/tm/rendered/273-f2f787987183.png"}}, {"label": "июнь 2025", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "stade-rennais-fc", "name": "Stade Rennais FC", "short": "SRF", "api_id": 94, "period": "с 2024", "logo": "images/clubs/tm/rendered/273-f2f787987183.png"}}, {"label": "дек. 2025", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "stade-rennais-fc", "name": "Stade Rennais FC", "short": "SRF", "api_id": 94, "period": "с 2024", "logo": "images/clubs/tm/rendered/273-f2f787987183.png"}}, {"label": "мар. 2026", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "stade-rennais-fc", "name": "Stade Rennais FC", "short": "SRF", "api_id": 94, "period": "с 2024", "logo": "images/clubs/tm/rendered/273-f2f787987183.png"}}, {"label": "июнь 2026", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "stade-rennais-fc", "name": "Stade Rennais FC", "short": "SRF", "api_id": 94, "period": "с 2024", "logo": "images/clubs/tm/rendered/273-f2f787987183.png"}}]}, {"key": "karim-adeyemi", "name": "Karim Adeyemi", "paths": ["/transfers/karim-adeyemi-barcelona/"], "points": [{"label": "2018", "value_label": "€1,50 млн", "value": 1.5, "club": {"slug": "tm-37024", "name": "FC Liefering", "short": "FC", "api_id": null, "period": "2018–2019", "logo": "images/clubs/chart/tm-37024.png"}}, {"label": "2020", "value_label": "€6,50 млн", "value": 6.7, "club": {"slug": "tm-409", "name": "Red Bull Salzburg", "short": "RBS", "api_id": null, "period": "2019–2021", "logo": "images/clubs/chart/tm-409.png"}}, {"label": "сен. 2021", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "tm-409", "name": "Red Bull Salzburg", "short": "RBS", "api_id": null, "period": "2019–2021", "logo": "images/clubs/chart/tm-409.png"}}, {"label": "дек. 2021", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "tm-409", "name": "Red Bull Salzburg", "short": "RBS", "api_id": null, "period": "2019–2021", "logo": "images/clubs/chart/tm-409.png"}}, {"label": "2022", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "borussia-dortmund", "name": "Borussia Dortmund", "short": "DOR", "api_id": 165, "period": "с 2022", "logo": "images/clubs/api/165.png"}}, {"label": "2025", "value_label": "€60 млн", "value": 60.0, "club": {"slug": "borussia-dortmund", "name": "Borussia Dortmund", "short": "DOR", "api_id": 165, "period": "с 2022", "logo": "images/clubs/api/165.png"}}, {"label": "2026", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "borussia-dortmund", "name": "Borussia Dortmund", "short": "DOR", "api_id": 165, "period": "с 2022", "logo": "images/clubs/api/165.png"}}]}, {"key": "mason-greenwood", "name": "Mason Greenwood", "paths": ["/transfers/mason-greenwood-fenerbahce/"], "points": [{"label": "2019", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "2019–2021", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}, {"label": "мар. 2020", "value_label": "€32 млн", "value": 32.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "2019–2021", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}, {"label": "июль 2020", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "2019–2021", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}, {"label": "2023", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "getafe-cf", "name": "Getafe CF", "short": "GET", "api_id": 546, "period": "2023", "logo": "images/clubs/api/546.png"}}, {"label": "2024", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "olympique-marseille", "name": "Olympique Marseille", "short": "MAR", "api_id": 81, "period": "с 2024", "logo": "images/clubs/api/rendered/81-f781160a86a8.png"}}, {"label": "мар. 2026", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "olympique-marseille", "name": "Olympique Marseille", "short": "MAR", "api_id": 81, "period": "с 2024", "logo": "images/clubs/api/rendered/81-f781160a86a8.png"}}, {"label": "июнь 2026", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "olympique-marseille", "name": "Olympique Marseille", "short": "MAR", "api_id": 81, "period": "с 2024", "logo": "images/clubs/api/rendered/81-f781160a86a8.png"}}]}, {"key": "mateus-fernandes", "name": "Mateus Fernandes", "paths": ["/transfers/mateus-fernandes-tottenham/"], "points": [{"label": "2022", "value_label": "€500 тыс.", "value": 0.5, "club": {"slug": "tm-10949", "name": "Sporting CP B", "short": "SCB", "api_id": null, "period": "2022", "logo": "images/clubs/chart/tm-10949.png"}}, {"label": "2023", "value_label": "€3 млн", "value": 3.0, "club": {"slug": "gd-estoril-praia", "name": "GD Estoril Praia", "short": "EST", "api_id": 230, "period": "2023", "logo": "images/clubs/api/230.png"}}, {"label": "июнь 2024", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "gd-estoril-praia", "name": "GD Estoril Praia", "short": "EST", "api_id": 230, "period": "2023", "logo": "images/clubs/api/230.png"}}, {"label": "окт. 2024", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "tm-180", "name": "Southampton FC", "short": "SOU", "api_id": null, "period": "2024", "logo": "images/clubs/chart/tm-180.png"}}, {"label": "дек. 2024", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "tm-180", "name": "Southampton FC", "short": "SOU", "api_id": null, "period": "2024", "logo": "images/clubs/chart/tm-180.png"}}, {"label": "2025", "value_label": "€32 млн", "value": 32.0, "club": {"slug": "tm-379", "name": "West Ham United", "short": "WHU", "api_id": null, "period": "с 2025", "logo": "images/clubs/chart/tm-379.png"}}, {"label": "2026", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "tm-379", "name": "West Ham United", "short": "WHU", "api_id": null, "period": "с 2025", "logo": "images/clubs/chart/tm-379.png"}}]}, {"key": "michael-olise", "name": "Michael Olise", "paths": ["/transfers/michael-olise-real-madrid/"], "points": [{"label": "2019", "value_label": "€200 тыс.", "value": 0.2, "club": {"slug": "tm-11994", "name": "Reading FC U18", "short": "RFU", "api_id": null, "period": "2019", "logo": "images/clubs/chart/tm-11994.png"}}, {"label": "2020", "value_label": "€900 тыс.", "value": 0.9, "club": {"slug": "tm-1032", "name": "Reading FC", "short": "REA", "api_id": null, "period": "2019–2020", "logo": "images/clubs/chart/tm-1032.png"}}, {"label": "2021", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "crystal-palace", "name": "Crystal Palace", "short": "CRY", "api_id": 52, "period": "2021–2023", "logo": "images/clubs/api/rendered/52-3a5b60eb010b.png"}}, {"label": "2024", "value_label": "€65 млн", "value": 65.0, "club": {"slug": "bayern-munich", "name": "Bayern Munich", "short": "BAY", "api_id": 157, "period": "с 2024", "logo": "images/clubs/api/157.png"}}, {"label": "июнь 2025", "value_label": "€100 млн", "value": 100.0, "club": {"slug": "bayern-munich", "name": "Bayern Munich", "short": "BAY", "api_id": 157, "period": "с 2024", "logo": "images/clubs/api/157.png"}}, {"label": "окт. 2025", "value_label": "€130 млн", "value": 130.0, "club": {"slug": "bayern-munich", "name": "Bayern Munich", "short": "BAY", "api_id": 157, "period": "с 2024", "logo": "images/clubs/api/157.png"}}, {"label": "2026", "value_label": "€170 млн", "value": 170.0, "club": {"slug": "bayern-munich", "name": "Bayern Munich", "short": "BAY", "api_id": 157, "period": "с 2024", "logo": "images/clubs/api/157.png"}}]}, {"key": "morgan-rogers", "name": "Morgan Rogers", "paths": ["/transfers/morgan-rogers-chelsea/"], "points": [{"label": "2019", "value_label": "€1,50 млн", "value": 1.5, "club": {"slug": "tm-9265", "name": "Manchester City U21", "short": "MCU", "api_id": null, "period": "2019–2022", "logo": "images/clubs/chart/tm-9265.png"}}, {"label": "2021", "value_label": "€1,80 млн", "value": 1.8, "club": {"slug": "afc-bournemouth", "name": "AFC Bournemouth", "short": "BOU", "api_id": 35, "period": "2021", "logo": "images/clubs/api/rendered/35-e668d998ce23.png"}}, {"label": "мар. 2023", "value_label": "€1,80 млн", "value": 1.8, "club": {"slug": "tm-1181", "name": "Blackpool FC", "short": "BLA", "api_id": null, "period": "2022", "logo": "images/clubs/chart/tm-1181.png"}}, {"label": "июнь 2023", "value_label": "€1,80 млн", "value": 1.8, "club": {"slug": "tm-9265", "name": "Manchester City U21", "short": "MCU", "api_id": null, "period": "2019–2022", "logo": "images/clubs/chart/tm-9265.png"}}, {"label": "окт. 2023", "value_label": "€2,20 млн", "value": 2.2, "club": {"slug": "tm-641", "name": "Middlesbrough FC", "short": "MID", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-641.png"}}, {"label": "2024", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "2023–2025", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "2026", "value_label": "€110 млн", "value": 110.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2026", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}]}, {"key": "rodri", "name": "Rodri", "paths": ["/transfers/rodri-real-madrid/"], "points": [{"label": "2016", "value_label": "€500 тыс.", "value": 0.5, "club": {"slug": "villarreal-cf", "name": "Villarreal CF", "short": "VIL", "api_id": 533, "period": "2016–2017", "logo": "images/clubs/api/533.png"}}, {"label": "2018", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "atletico-de-madrid", "name": "Atlético de Madrid", "short": "ATM", "api_id": 530, "period": "2018", "logo": "images/clubs/api/rendered/530-33037c80387a.png"}}, {"label": "июнь 2019", "value_label": "€80 млн", "value": 80.0, "club": {"slug": "atletico-de-madrid", "name": "Atlético de Madrid", "short": "ATM", "api_id": 530, "period": "2018", "logo": "images/clubs/api/rendered/530-33037c80387a.png"}}, {"label": "дек. 2019", "value_label": "€80 млн", "value": 80.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2019", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2024", "value_label": "€130 млн", "value": 130.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2019", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2025", "value_label": "€110 млн", "value": 110.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2019", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2026", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2019", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}]}, {"key": "youri-tielemans", "name": "Youri Tielemans", "paths": ["/transfers/youri-tielemans-manchester-united/"], "points": [{"label": "2013", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "tm-58", "name": "RSC Anderlecht", "short": "RSC", "api_id": null, "period": "2013–2016", "logo": "images/clubs/chart/tm-58.png"}}, {"label": "2018", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2017–2018", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "мар. 2019", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "tm-1003", "name": "Leicester City", "short": "LEI", "api_id": null, "period": "2018–2022", "logo": "images/clubs/chart/tm-1003.png"}}, {"label": "июнь 2019", "value_label": "€38 млн", "value": 38.0, "club": {"slug": "tm-1003", "name": "Leicester City", "short": "LEI", "api_id": null, "period": "2018–2022", "logo": "images/clubs/chart/tm-1003.png"}}, {"label": "дек. 2019", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "tm-1003", "name": "Leicester City", "short": "LEI", "api_id": null, "period": "2018–2022", "logo": "images/clubs/chart/tm-1003.png"}}, {"label": "2023", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "2023–2025", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "2026", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "manchester-united", "name": "Manchester United", "short": "MUN", "api_id": 33, "period": "с 2026", "logo": "images/clubs/api/rendered/33-6dff7e1a3d7d.png"}}]}, {"key": "nick-woltemade-juventus-step4", "name": "Nick Woltemade", "paths": ["/transfers/nick-woltemade-juventus/"], "points": [{"label": "2020", "value_label": "€350 тыс.", "value": 0.35, "club": {"slug": "tm-2491", "name": "SV Werder Bremen U19", "short": "SWB", "api_id": null, "period": "2019", "logo": "images/clubs/chart/tm-2491.png"}}, {"label": "2022", "value_label": "€600 тыс.", "value": 0.6, "club": {"slug": "sv-07-elversberg", "name": "SV 07 Elversberg", "short": "ELV", "api_id": 1660, "period": "2022", "logo": "images/clubs/api/1660.png"}}, {"label": "2023", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "sv-werder-bremen", "name": "SV Werder Bremen", "short": "WER", "api_id": 162, "period": "2020–2023", "logo": "images/clubs/api/rendered/162-076ca6ba9cbf.png"}}, {"label": "2024", "value_label": "€7,50 млн", "value": 7.5, "club": {"slug": "vfb-stuttgart", "name": "VfB Stuttgart", "short": "STU", "api_id": 172, "period": "2024", "logo": "images/clubs/api/172.png"}}, {"label": "окт. 2025", "value_label": "€65 млн", "value": 65.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "с 2025", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}, {"label": "дек. 2025", "value_label": "€70 млн", "value": 70.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "с 2025", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}, {"label": "2026", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "newcastle-united", "name": "Newcastle United", "short": "NEW", "api_id": null, "period": "с 2025", "logo": "images/clubs/api/rendered/34-2cdfd5d4d0e6.png"}}]}, {"key": "enzo-fernandez-manchester-city-step4", "name": "Enzo Fernández", "paths": ["/transfers/enzo-fernandez-manchester-city/"], "points": [{"label": "фев. 2021", "value_label": "€4 млн", "value": 4.0, "club": {"slug": "tm-2402", "name": "Defensa y Justicia", "short": "DYJ", "api_id": null, "period": "2020", "logo": "images/clubs/chart/tm-2402.png"}}, {"label": "окт. 2021", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "tm-209", "name": "CA River Plate", "short": "CRP", "api_id": null, "period": "2021", "logo": "images/clubs/chart/tm-209.png"}}, {"label": "сен. 2022", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "sl-benfica", "name": "SL Benfica", "short": "BEN", "api_id": 211, "period": "2022", "logo": "images/clubs/api/rendered/211-2874faa514fa.png"}}, {"label": "ноя. 2022", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "sl-benfica", "name": "SL Benfica", "short": "BEN", "api_id": 211, "period": "2022", "logo": "images/clubs/api/rendered/211-2874faa514fa.png"}}, {"label": "дек. 2022", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "sl-benfica", "name": "SL Benfica", "short": "BEN", "api_id": 211, "period": "2022", "logo": "images/clubs/api/rendered/211-2874faa514fa.png"}}, {"label": "2023", "value_label": "€85 млн", "value": 85.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2022", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2026", "value_label": "€100 млн", "value": 100.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2022", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}]}, {"key": "rafael-leao-galatasaray-step4", "name": "Rafael Leão", "paths": ["/transfers/rafael-leao-galatasaray/"], "points": [{"label": "2017", "value_label": "€500 тыс.", "value": 0.5, "club": {"slug": "tm-10949", "name": "Sporting CP B", "short": "SCB", "api_id": null, "period": "2017", "logo": "images/clubs/chart/tm-10949.png"}}, {"label": "фев. 2018", "value_label": "€1,50 млн", "value": 1.5, "club": {"slug": "sporting-cp", "name": "Sporting CP", "short": "SPO", "api_id": 228, "period": "2017", "logo": "images/clubs/api/228.png"}}, {"label": "дек. 2018", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "losc-lille", "name": "LOSC Lille", "short": "LIL", "api_id": 79, "period": "2018", "logo": "images/clubs/api/rendered/79-021579263933.png"}}, {"label": "2019", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2019", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}, {"label": "2022", "value_label": "€70 млн", "value": 70.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2019", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}, {"label": "2023", "value_label": "€90 млн", "value": 90.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2019", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}, {"label": "2026", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2019", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}]}, {"key": "christopher-nkunku-rb-leipzig-step4", "name": "Christopher Nkunku", "paths": ["/transfers/christopher-nkunku-rb-leipzig/"], "points": [{"label": "2016", "value_label": "€250 тыс.", "value": 0.25, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "2015–2018", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "2019", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "rb-leipzig", "name": "RB Leipzig", "short": "LEI", "api_id": 173, "period": "2019–2022", "logo": "images/clubs/api/rendered/173-d38d0dff9d91.png"}}, {"label": "2022", "value_label": "€80 млн", "value": 80.0, "club": {"slug": "rb-leipzig", "name": "RB Leipzig", "short": "LEI", "api_id": 173, "period": "2019–2022", "logo": "images/clubs/api/rendered/173-d38d0dff9d91.png"}}, {"label": "2023", "value_label": "€75 млн", "value": 75.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "2023–2024", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2024", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "2023–2024", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2025", "value_label": "€32 млн", "value": 32.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2025", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}, {"label": "2026", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2025", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}]}, {"key": "omar-marmoush-tottenham-hotspur-step4", "name": "Omar Marmoush", "paths": ["/transfers/omar-marmoush-tottenham-hotspur/"], "points": [{"label": "2016", "value_label": "€25 тыс.", "value": 0.03, "club": {"slug": "tm-18234", "name": "Wadi Degla FC", "short": "WDF", "api_id": null, "period": "2016–2017", "logo": "images/clubs/chart/tm-18234.png"}}, {"label": "фев. 2021", "value_label": "€750 тыс.", "value": 0.75, "club": {"slug": "tm-35", "name": "FC St. Pauli", "short": "FSP", "api_id": null, "period": "2020", "logo": "images/clubs/chart/tm-35.png"}}, {"label": "окт. 2021", "value_label": "€4 млн", "value": 4.0, "club": {"slug": "vfb-stuttgart", "name": "VfB Stuttgart", "short": "STU", "api_id": 172, "period": "2021", "logo": "images/clubs/api/172.png"}}, {"label": "2022", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "tm-82", "name": "VfL Wolfsburg", "short": "VFL", "api_id": null, "period": "2020–2022", "logo": "images/clubs/chart/tm-82.png"}}, {"label": "2023", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "eintracht-frankfurt", "name": "Eintracht Frankfurt", "short": "EIN", "api_id": 169, "period": "2023–2024", "logo": "images/clubs/api/rendered/169-bdd9ff4272f0.png"}}, {"label": "2025", "value_label": "€75 млн", "value": 75.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2024", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2026", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2024", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}]}, {"key": "joao-palhinha-sl-benfica-step4", "name": "João Palhinha", "paths": ["/transfers/joao-palhinha-sl-benfica/"], "points": [{"label": "2015", "value_label": "€75 тыс.", "value": 0.07, "club": {"slug": "tm-10949", "name": "Sporting CP B", "short": "SCB", "api_id": null, "period": "2015", "logo": "images/clubs/chart/tm-10949.png"}}, {"label": "2020", "value_label": "€9 млн", "value": 9.0, "club": {"slug": "sporting-cp", "name": "Sporting CP", "short": "SPO", "api_id": 228, "period": "2016–2021", "logo": "images/clubs/api/228.png"}}, {"label": "2022", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "fulham-fc", "name": "Fulham FC", "short": "FUL", "api_id": 36, "period": "2022–2023", "logo": "images/clubs/api/rendered/36-3735bd31a6c7.png"}}, {"label": "2023", "value_label": "€60 млн", "value": 60.0, "club": {"slug": "fulham-fc", "name": "Fulham FC", "short": "FUL", "api_id": 36, "period": "2022–2023", "logo": "images/clubs/api/rendered/36-3735bd31a6c7.png"}}, {"label": "2024", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "bayern-munich", "name": "Bayern Munich", "short": "BAY", "api_id": 157, "period": "2024", "logo": "images/clubs/api/157.png"}}, {"label": "2025", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2025", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2026", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2025", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}]}, {"key": "ethan-nwaneri-borussia-dortmund-step4", "name": "Ethan Nwaneri", "paths": ["/transfers/ethan-nwaneri-borussia-dortmund/"], "points": [{"label": "2023", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "tm-9249", "name": "Arsenal FC U21", "short": "AFU", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-9249.png"}}, {"label": "окт. 2024", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "arsenal-fc", "name": "Arsenal FC", "short": "ARS", "api_id": 42, "period": "2024–2025", "logo": "images/clubs/api/rendered/42-ba273b85e8fe.png"}}, {"label": "дек. 2024", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "arsenal-fc", "name": "Arsenal FC", "short": "ARS", "api_id": 42, "period": "2024–2025", "logo": "images/clubs/api/rendered/42-ba273b85e8fe.png"}}, {"label": "мар. 2025", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "arsenal-fc", "name": "Arsenal FC", "short": "ARS", "api_id": 42, "period": "2024–2025", "logo": "images/clubs/api/rendered/42-ba273b85e8fe.png"}}, {"label": "окт. 2025", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "arsenal-fc", "name": "Arsenal FC", "short": "ARS", "api_id": 42, "period": "2024–2025", "logo": "images/clubs/api/rendered/42-ba273b85e8fe.png"}}, {"label": "дек. 2025", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "arsenal-fc", "name": "Arsenal FC", "short": "ARS", "api_id": 42, "period": "2024–2025", "logo": "images/clubs/api/rendered/42-ba273b85e8fe.png"}}, {"label": "2026", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "olympique-marseille", "name": "Olympique Marseille", "short": "MAR", "api_id": 81, "period": "с 2025", "logo": "images/clubs/api/rendered/81-f781160a86a8.png"}}]}, {"key": "iliman-ndiaye-manchester-city-step4", "name": "Iliman Ndiaye", "paths": ["/transfers/iliman-ndiaye-manchester-city/"], "points": [{"label": "мар. 2021", "value_label": "€200 тыс.", "value": 0.2, "club": {"slug": "tm-8824", "name": "Sheffield United U21", "short": "SUU", "api_id": null, "period": "", "logo": "images/clubs/chart/tm-8824.png"}}, {"label": "ноя. 2021", "value_label": "€700 тыс.", "value": 0.7, "club": {"slug": "tm-350", "name": "Sheffield United", "short": "SHE", "api_id": null, "period": "2021–2022", "logo": "images/clubs/chart/tm-350.png"}}, {"label": "2023", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "olympique-marseille", "name": "Olympique Marseille", "short": "MAR", "api_id": 81, "period": "2023", "logo": "images/clubs/api/rendered/81-f781160a86a8.png"}}, {"label": "2024", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "everton-fc", "name": "Everton FC", "short": "EVE", "api_id": 45, "period": "с 2024", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "окт. 2025", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "everton-fc", "name": "Everton FC", "short": "EVE", "api_id": 45, "period": "с 2024", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "дек. 2025", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "everton-fc", "name": "Everton FC", "short": "EVE", "api_id": 45, "period": "с 2024", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "2026", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "everton-fc", "name": "Everton FC", "short": "EVE", "api_id": 45, "period": "с 2024", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}]}, {"key": "savio-tottenham-hotspur-step4", "name": "Sávio", "paths": ["/transfers/savio-tottenham-hotspur/"], "points": [{"label": "2021", "value_label": "€3 млн", "value": 3.0, "club": {"slug": "tm-330", "name": "Clube Atlético Mineiro", "short": "CAM", "api_id": null, "period": "2020–2021", "logo": "images/clubs/chart/tm-330.png"}}, {"label": "2022", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "tm-383", "name": "PSV Eindhoven", "short": "PSV", "api_id": null, "period": "2022", "logo": "images/clubs/chart/tm-383.png"}}, {"label": "окт. 2023", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "tm-12321", "name": "Girona FC", "short": "GIR", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-12321.png"}}, {"label": "дек. 2023", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "tm-12321", "name": "Girona FC", "short": "GIR", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-12321.png"}}, {"label": "мар. 2024", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "tm-12321", "name": "Girona FC", "short": "GIR", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-12321.png"}}, {"label": "дек. 2024", "value_label": "€55 млн", "value": 55.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2024", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2026", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2024", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}]}, {"key": "bernardo-silva-real-madrid-step4", "name": "Bernardo Silva", "paths": ["/transfers/bernardo-silva-real-madrid/"], "points": [{"label": "2013", "value_label": "€600 тыс.", "value": 0.6, "club": {"slug": "tm-10330", "name": "SL Benfica B", "short": "SBB", "api_id": null, "period": "2013", "logo": "images/clubs/chart/tm-10330.png"}}, {"label": "2015", "value_label": "€3,50 млн", "value": 3.5, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2014–2016", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "2017", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2014–2016", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "2018", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2017", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2019", "value_label": "€100 млн", "value": 100.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2017", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2020", "value_label": "€80 млн", "value": 80.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2017", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2026", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2017", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}]}, {"key": "moise-kean-como-1907-step4", "name": "Moise Kean", "paths": ["/transfers/moise-kean-como-1907/"], "points": [{"label": "2016", "value_label": "€600 тыс.", "value": 0.6, "club": {"slug": "tm-11008", "name": "Juventus Primavera", "short": "JUV", "api_id": null, "period": "2016", "logo": "images/clubs/chart/tm-11008.png"}}, {"label": "2019", "value_label": "€32 млн", "value": 32.0, "club": {"slug": "everton-fc", "name": "Everton FC", "short": "EVE", "api_id": 45, "period": "2019", "logo": "images/clubs/api/rendered/45-7d798d13ebff.png"}}, {"label": "2020", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "2020", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "2021", "value_label": "€32 млн", "value": 32.0, "club": {"slug": "juventus-fc", "name": "Juventus FC", "short": "JUV", "api_id": 496, "period": "2018–2023", "logo": "images/clubs/api/rendered/496-ea0cc8953697.png"}}, {"label": "2024", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "acf-fiorentina", "name": "ACF Fiorentina", "short": "FIO", "api_id": 502, "period": "с 2024", "logo": "images/clubs/api/502.png"}}, {"label": "2025", "value_label": "€50 млн", "value": 50.0, "club": {"slug": "acf-fiorentina", "name": "ACF Fiorentina", "short": "FIO", "api_id": 502, "period": "с 2024", "logo": "images/clubs/api/502.png"}}, {"label": "2026", "value_label": "€32 млн", "value": 32.0, "club": {"slug": "acf-fiorentina", "name": "ACF Fiorentina", "short": "FIO", "api_id": 502, "period": "с 2024", "logo": "images/clubs/api/502.png"}}]}, {"key": "exequiel-palacios-ipswich-town-step4", "name": "Exequiel Palacios", "paths": ["/transfers/exequiel-palacios-ipswich-town/"], "points": [{"label": "2016", "value_label": "€300 тыс.", "value": 0.3, "club": {"slug": "tm-14837", "name": "CA River Plate II", "short": "CRP", "api_id": null, "period": "2015–2016", "logo": "images/clubs/chart/tm-14837.png"}}, {"label": "2017", "value_label": "€1,50 млн", "value": 1.5, "club": {"slug": "tm-209", "name": "CA River Plate", "short": "CRP", "api_id": null, "period": "2017–2019", "logo": "images/clubs/chart/tm-209.png"}}, {"label": "2018", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "tm-209", "name": "CA River Plate", "short": "CRP", "api_id": null, "period": "2017–2019", "logo": "images/clubs/chart/tm-209.png"}}, {"label": "2020", "value_label": "€22 млн", "value": 22.5, "club": {"slug": "bayer-04-leverkusen", "name": "Bayer 04 Leverkusen", "short": "BAY", "api_id": 168, "period": "с 2019", "logo": "images/clubs/api/rendered/168-780bfce19ea9.png"}}, {"label": "2023", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "bayer-04-leverkusen", "name": "Bayer 04 Leverkusen", "short": "BAY", "api_id": 168, "period": "с 2019", "logo": "images/clubs/api/rendered/168-780bfce19ea9.png"}}, {"label": "2024", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "bayer-04-leverkusen", "name": "Bayer 04 Leverkusen", "short": "BAY", "api_id": 168, "period": "с 2019", "logo": "images/clubs/api/rendered/168-780bfce19ea9.png"}}, {"label": "2026", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "bayer-04-leverkusen", "name": "Bayer 04 Leverkusen", "short": "BAY", "api_id": 168, "period": "с 2019", "logo": "images/clubs/api/rendered/168-780bfce19ea9.png"}}]}, {"key": "ezri-konsa-arsenal-fc-step4", "name": "Ezri Konsa", "paths": ["/transfers/ezri-konsa-arsenal-fc/"], "points": [{"label": "2016", "value_label": "€100 тыс.", "value": 0.1, "club": {"slug": "tm-358", "name": "Charlton Athletic", "short": "CHA", "api_id": null, "period": "2016", "logo": "images/clubs/chart/tm-358.png"}}, {"label": "2018", "value_label": "€3 млн", "value": 3.0, "club": {"slug": "brentford-fc", "name": "Brentford FC", "short": "BRE", "api_id": 55, "period": "2018", "logo": "images/clubs/api/rendered/55-69278a7461b2.png"}}, {"label": "2019", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2019", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "мар. 2021", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2019", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "июнь 2021", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2019", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "2023", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2019", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "2026", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2019", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}]}, {"key": "nico-gonzalez-newcastle-united-step4", "name": "Nico González", "paths": ["/transfers/nico-gonzalez-newcastle-united/"], "points": [{"label": "2020", "value_label": "€100 тыс.", "value": 0.1, "club": {"slug": "tm-2464", "name": "FC Barcelona Atlètic", "short": "FBA", "api_id": null, "period": "2020", "logo": "images/clubs/chart/tm-2464.png"}}, {"label": "2021", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "fc-barcelona", "name": "FC Barcelona", "short": "BAR", "api_id": 529, "period": "2021", "logo": "images/clubs/api/rendered/529-921329187f25.png"}}, {"label": "2022", "value_label": "€14 млн", "value": 14.0, "club": {"slug": "valencia-cf", "name": "Valencia CF", "short": "VAL", "api_id": 532, "period": "2022", "logo": "images/clubs/api/532.png"}}, {"label": "2023", "value_label": "€9 млн", "value": 9.0, "club": {"slug": "fc-porto", "name": "FC Porto", "short": "POR", "api_id": 212, "period": "2023–2024", "logo": "images/clubs/api/212.png"}}, {"label": "мар. 2025", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2024", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "дек. 2025", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2024", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}, {"label": "2026", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "manchester-city", "name": "Manchester City", "short": "MCI", "api_id": 50, "period": "с 2024", "logo": "images/clubs/api/rendered/50-090f6609ab46.png"}}]}, {"key": "pape-matar-sarr-juventus-fc-step4", "name": "Pape Matar Sarr", "paths": ["/transfers/pape-matar-sarr-juventus-fc/"], "points": [{"label": "мар. 2021", "value_label": "€3 млн", "value": 3.0, "club": {"slug": "tm-347", "name": "FC Metz", "short": "FC", "api_id": null, "period": "2020–2021", "logo": "images/clubs/chart/tm-347.png"}}, {"label": "окт. 2021", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "tm-347", "name": "FC Metz", "short": "FC", "api_id": null, "period": "2020–2021", "logo": "images/clubs/chart/tm-347.png"}}, {"label": "2022", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2022", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2023", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2022", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2024", "value_label": "€45 млн", "value": 45.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2022", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2025", "value_label": "€32 млн", "value": 32.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2022", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}, {"label": "2026", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "tottenham-hotspur", "name": "Tottenham Hotspur", "short": "TOT", "api_id": 47, "period": "с 2022", "logo": "images/clubs/api/rendered/47-ce51d50ba9db.png"}}]}, {"key": "axel-disasi-crystal-palace-step4", "name": "Axel Disasi", "paths": ["/transfers/axel-disasi-crystal-palace/"], "points": [{"label": "2015", "value_label": "€50 тыс.", "value": 0.05, "club": {"slug": "tm-38673", "name": "Paris FC B", "short": "PFB", "api_id": null, "period": "2015", "logo": "images/clubs/chart/tm-38673.png"}}, {"label": "2020", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2020–2022", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "окт. 2023", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "2023–2025", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "дек. 2023", "value_label": "€42 млн", "value": 42.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "2023–2025", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "мар. 2025", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "2024", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "окт. 2025", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "2023–2025", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2026", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "tm-379", "name": "West Ham United", "short": "WHU", "api_id": null, "period": "с 2025", "logo": "images/clubs/chart/tm-379.png"}}]}, {"key": "benoit-badiashile-ssc-napoli-step4", "name": "Benoît Badiashile", "paths": ["/transfers/benoit-badiashile-ssc-napoli/"], "points": [{"label": "2018", "value_label": "€150 тыс.", "value": 0.15, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2018–2022", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "мар. 2019", "value_label": "€9 млн", "value": 9.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2018–2022", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "сен. 2019", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2018–2022", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "2020", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2018–2022", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "2022", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2018–2022", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "2023", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2022", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2026", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2022", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}]}, {"key": "liam-delap-nottingham-forest-step4", "name": "Liam Delap", "paths": ["/transfers/liam-delap-nottingham-forest/"], "points": [{"label": "2020", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "tm-9265", "name": "Manchester City U21", "short": "MCU", "api_id": null, "period": "2020–2022", "logo": "images/clubs/chart/tm-9265.png"}}, {"label": "июнь 2023", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "tm-9265", "name": "Manchester City U21", "short": "MCU", "api_id": null, "period": "2020–2022", "logo": "images/clubs/chart/tm-9265.png"}}, {"label": "окт. 2023", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "hull-city", "name": "Hull City", "short": "HUL", "api_id": 64, "period": "2023", "logo": "images/clubs/api/rendered/64-e5825be5ee17.png"}}, {"label": "2024", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "ipswich-town", "name": "Ipswich Town", "short": "IPS", "api_id": 57, "period": "2024", "logo": "images/clubs/api/rendered/57-1362c589ddf7.png"}}, {"label": "май 2025", "value_label": "€40 млн", "value": 40.0, "club": {"slug": "ipswich-town", "name": "Ipswich Town", "short": "IPS", "api_id": 57, "period": "2024", "logo": "images/clubs/api/rendered/57-1362c589ddf7.png"}}, {"label": "дек. 2025", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2025", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2026", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2025", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}]}, {"key": "pedro-goncalves-acf-fiorentina-step4", "name": "Pedro Gonçalves", "paths": ["/transfers/pedro-goncalves-acf-fiorentina/"], "points": [{"label": "2019", "value_label": "€800 тыс.", "value": 0.8, "club": {"slug": "fc-famalicao", "name": "FC Famalicão", "short": "FAM", "api_id": 242, "period": "2019–2020", "logo": "images/clubs/api/242.png"}}, {"label": "авг. 2020", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "fc-famalicao", "name": "FC Famalicão", "short": "FAM", "api_id": 242, "period": "2019–2020", "logo": "images/clubs/api/242.png"}}, {"label": "окт. 2020", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "sporting-cp", "name": "Sporting CP", "short": "SPO", "api_id": 228, "period": "с 2020", "logo": "images/clubs/api/228.png"}}, {"label": "янв. 2021", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "sporting-cp", "name": "Sporting CP", "short": "SPO", "api_id": 228, "period": "с 2020", "logo": "images/clubs/api/228.png"}}, {"label": "июнь 2021", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "sporting-cp", "name": "Sporting CP", "short": "SPO", "api_id": 228, "period": "с 2020", "logo": "images/clubs/api/228.png"}}, {"label": "дек. 2021", "value_label": "€38 млн", "value": 38.0, "club": {"slug": "sporting-cp", "name": "Sporting CP", "short": "SPO", "api_id": 228, "period": "с 2020", "logo": "images/clubs/api/228.png"}}, {"label": "2026", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "sporting-cp", "name": "Sporting CP", "short": "SPO", "api_id": 228, "period": "с 2020", "logo": "images/clubs/api/228.png"}}]}, {"key": "dilane-bakwa-losc-lille-step4", "name": "Dilane Bakwa", "paths": ["/transfers/dilane-bakwa-losc-lille/"], "points": [{"label": "2020", "value_label": "€300 тыс.", "value": 0.3, "club": {"slug": "tm-40", "name": "FC Girondins Bordeaux", "short": "FGB", "api_id": null, "period": "", "logo": "images/clubs/chart/tm-40.png"}}, {"label": "2023", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "rc-strasbourg-alsace", "name": "RC Strasbourg Alsace", "short": "STR", "api_id": 95, "period": "2023–2024", "logo": "images/clubs/api/rendered/95-94fa45143780.png"}}, {"label": "2024", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "rc-strasbourg-alsace", "name": "RC Strasbourg Alsace", "short": "STR", "api_id": 95, "period": "2023–2024", "logo": "images/clubs/api/rendered/95-94fa45143780.png"}}, {"label": "июнь 2025", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "rc-strasbourg-alsace", "name": "RC Strasbourg Alsace", "short": "STR", "api_id": 95, "period": "2023–2024", "logo": "images/clubs/api/rendered/95-94fa45143780.png"}}, {"label": "окт. 2025", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NOT", "api_id": 65, "period": "с 2025", "logo": "images/clubs/api/65.png"}}, {"label": "мар. 2026", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NOT", "api_id": 65, "period": "с 2025", "logo": "images/clubs/api/65.png"}}, {"label": "июнь 2026", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NOT", "api_id": 65, "period": "с 2025", "logo": "images/clubs/api/65.png"}}]}, {"key": "harvey-elliott-valencia-cf-step4", "name": "Harvey Elliott", "paths": ["/transfers/harvey-elliott-valencia-cf/"], "points": [{"label": "2019", "value_label": "€4 млн", "value": 4.0, "club": {"slug": "tm-9252", "name": "Liverpool FC U21", "short": "LFU", "api_id": null, "period": "2019–2020", "logo": "images/clubs/chart/tm-9252.png"}}, {"label": "2020", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "tm-164", "name": "Blackburn Rovers", "short": "BLA", "api_id": null, "period": "2020", "logo": "images/clubs/chart/tm-164.png"}}, {"label": "2021", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "liverpool-fc", "name": "Liverpool FC", "short": "LIV", "api_id": 40, "period": "2021–2024", "logo": "images/clubs/api/rendered/40-c3b13021c1ab.png"}}, {"label": "2022", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "liverpool-fc", "name": "Liverpool FC", "short": "LIV", "api_id": 40, "period": "2021–2024", "logo": "images/clubs/api/rendered/40-c3b13021c1ab.png"}}, {"label": "2025", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2025", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "мар. 2026", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2025", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}, {"label": "июнь 2026", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "aston-villa", "name": "Aston Villa", "short": "AST", "api_id": 66, "period": "с 2025", "logo": "images/clubs/api/rendered/66-15f20ce5969b.png"}}]}, {"key": "jean-clair-todibo-rc-lens-step4", "name": "Jean-Clair Todibo", "paths": ["/transfers/jean-clair-todibo-rc-lens/"], "points": [{"label": "2018", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "fc-toulouse", "name": "FC Toulouse", "short": "TOU", "api_id": 96, "period": "2018", "logo": "images/clubs/api/96.png"}}, {"label": "2020", "value_label": "€14 млн", "value": 14.0, "club": {"slug": "fc-barcelona", "name": "FC Barcelona", "short": "BAR", "api_id": 529, "period": "2018–2020", "logo": "images/clubs/api/rendered/529-921329187f25.png"}}, {"label": "янв. 2021", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "sl-benfica", "name": "SL Benfica", "short": "BEN", "api_id": 211, "period": "2020", "logo": "images/clubs/api/rendered/211-2874faa514fa.png"}}, {"label": "июнь 2021", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "ogc-nice", "name": "OGC Nice", "short": "NIC", "api_id": 84, "period": "2020–2023", "logo": "images/clubs/api/84.png"}}, {"label": "2023", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "ogc-nice", "name": "OGC Nice", "short": "NIC", "api_id": 84, "period": "2020–2023", "logo": "images/clubs/api/84.png"}}, {"label": "2024", "value_label": "€32 млн", "value": 32.0, "club": {"slug": "tm-379", "name": "West Ham United", "short": "WHU", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-379.png"}}, {"label": "2026", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "tm-379", "name": "West Ham United", "short": "WHU", "api_id": null, "period": "с 2024", "logo": "images/clubs/chart/tm-379.png"}}]}, {"key": "omari-hutchinson-ac-milan-step4", "name": "Omari Hutchinson", "paths": ["/transfers/omari-hutchinson-ac-milan/"], "points": [{"label": "2022", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "tm-9250", "name": "Chelsea FC U21", "short": "CFU", "api_id": null, "period": "2022", "logo": "images/clubs/chart/tm-9250.png"}}, {"label": "2023", "value_label": "€3 млн", "value": 3.0, "club": {"slug": "ipswich-town", "name": "Ipswich Town", "short": "IPS", "api_id": 57, "period": "2023–2024", "logo": "images/clubs/api/rendered/57-1362c589ddf7.png"}}, {"label": "окт. 2024", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "ipswich-town", "name": "Ipswich Town", "short": "IPS", "api_id": 57, "period": "2023–2024", "logo": "images/clubs/api/rendered/57-1362c589ddf7.png"}}, {"label": "дек. 2024", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "ipswich-town", "name": "Ipswich Town", "short": "IPS", "api_id": 57, "period": "2023–2024", "logo": "images/clubs/api/rendered/57-1362c589ddf7.png"}}, {"label": "окт. 2025", "value_label": "€35 млн", "value": 35.0, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NOT", "api_id": 65, "period": "с 2025", "logo": "images/clubs/api/65.png"}}, {"label": "дек. 2025", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NOT", "api_id": 65, "period": "с 2025", "logo": "images/clubs/api/65.png"}}, {"label": "2026", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "nottingham-forest", "name": "Nottingham Forest", "short": "NOT", "api_id": 65, "period": "с 2025", "logo": "images/clubs/api/65.png"}}]}, {"key": "robert-sanchez-como-1907-step4", "name": "Robert Sánchez", "paths": ["/transfers/robert-sanchez-como-1907/"], "points": [{"label": "2020", "value_label": "€150 тыс.", "value": 0.15, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "2020–2022", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "сен. 2022", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "2020–2022", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "ноя. 2022", "value_label": "€32 млн", "value": 32.0, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "2020–2022", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "июнь 2023", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "brighton-hove-albion", "name": "Brighton & Hove Albion", "short": "BRI", "api_id": 51, "period": "2020–2022", "logo": "images/clubs/api/rendered/51-d9b536ef13f9.png"}}, {"label": "окт. 2023", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2023", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2024", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2023", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}, {"label": "2026", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "chelsea-fc", "name": "Chelsea FC", "short": "CHE", "api_id": 49, "period": "с 2023", "logo": "images/clubs/api/rendered/49-a4353df0d456.png"}}]}, {"key": "honest-ahanor-crystal-palace-step4", "name": "Honest Ahanor", "paths": ["/transfers/honest-ahanor-crystal-palace/"], "points": [{"label": "июнь 2024", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "tm-8517", "name": "Genoa U20", "short": "GEN", "api_id": null, "period": "2023", "logo": "images/clubs/chart/tm-8517.png"}}, {"label": "окт. 2024", "value_label": "€3 млн", "value": 3.0, "club": {"slug": "genoa-cfc", "name": "Genoa CFC", "short": "GEN", "api_id": 495, "period": "2024", "logo": "images/clubs/api/495.png"}}, {"label": "дек. 2024", "value_label": "€3 млн", "value": 3.0, "club": {"slug": "genoa-cfc", "name": "Genoa CFC", "short": "GEN", "api_id": 495, "period": "2024", "logo": "images/clubs/api/495.png"}}, {"label": "июнь 2025", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "genoa-cfc", "name": "Genoa CFC", "short": "GEN", "api_id": 495, "period": "2024", "logo": "images/clubs/api/495.png"}}, {"label": "окт. 2025", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "atalanta-bc", "name": "Atalanta BC", "short": "ATA", "api_id": 499, "period": "с 2025", "logo": "images/clubs/api/499.png"}}, {"label": "дек. 2025", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "atalanta-bc", "name": "Atalanta BC", "short": "ATA", "api_id": 499, "period": "с 2025", "logo": "images/clubs/api/499.png"}}, {"label": "2026", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "atalanta-bc", "name": "Atalanta BC", "short": "ATA", "api_id": 499, "period": "с 2025", "logo": "images/clubs/api/499.png"}}]}, {"key": "ibrahim-mbaye-aston-villa-step4", "name": "Ibrahim Mbaye", "paths": ["/transfers/ibrahim-mbaye-aston-villa/"], "points": [{"label": "окт. 2024", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "tm-43570", "name": "Paris Saint-Germain Espoirs", "short": "PSG", "api_id": null, "period": "", "logo": "images/clubs/chart/tm-43570.png"}}, {"label": "дек. 2024", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "tm-43570", "name": "Paris Saint-Germain Espoirs", "short": "PSG", "api_id": null, "period": "", "logo": "images/clubs/chart/tm-43570.png"}}, {"label": "июнь 2025", "value_label": "€3 млн", "value": 3.0, "club": {"slug": "tm-43570", "name": "Paris Saint-Germain Espoirs", "short": "PSG", "api_id": null, "period": "", "logo": "images/clubs/chart/tm-43570.png"}}, {"label": "окт. 2025", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2025", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "дек. 2025", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2025", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "мар. 2026", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2025", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}, {"label": "июнь 2026", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "paris-saint-germain", "name": "Paris Saint-Germain", "short": "PSG", "api_id": 85, "period": "с 2025", "logo": "images/clubs/api/rendered/85-ca6329d951be.png"}}]}, {"key": "malick-fofana-sunderland-afc-step4", "name": "Malick Fofana", "paths": ["/transfers/malick-fofana-sunderland-afc/"], "points": [{"label": "2022", "value_label": "€400 тыс.", "value": 0.4, "club": {"slug": "tm-157", "name": "KAA Gent", "short": "KAA", "api_id": null, "period": "2022–2023", "logo": "images/clubs/chart/tm-157.png"}}, {"label": "2023", "value_label": "€6 млн", "value": 6.0, "club": {"slug": "tm-157", "name": "KAA Gent", "short": "KAA", "api_id": null, "period": "2022–2023", "logo": "images/clubs/chart/tm-157.png"}}, {"label": "мар. 2024", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "olympique-lyon", "name": "Olympique Lyon", "short": "LYO", "api_id": 80, "period": "с 2023", "logo": "images/clubs/api/80.png"}}, {"label": "июнь 2024", "value_label": "€15 млн", "value": 15.0, "club": {"slug": "olympique-lyon", "name": "Olympique Lyon", "short": "LYO", "api_id": 80, "period": "с 2023", "logo": "images/clubs/api/80.png"}}, {"label": "дек. 2024", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "olympique-lyon", "name": "Olympique Lyon", "short": "LYO", "api_id": 80, "period": "с 2023", "logo": "images/clubs/api/80.png"}}, {"label": "2025", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "olympique-lyon", "name": "Olympique Lyon", "short": "LYO", "api_id": 80, "period": "с 2023", "logo": "images/clubs/api/80.png"}}, {"label": "2026", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "olympique-lyon", "name": "Olympique Lyon", "short": "LYO", "api_id": 80, "period": "с 2023", "logo": "images/clubs/api/80.png"}}]}, {"key": "samuele-ricci-como-1907-step4", "name": "Samuele Ricci", "paths": ["/transfers/samuele-ricci-como-1907/"], "points": [{"label": "2019", "value_label": "€150 тыс.", "value": 0.15, "club": {"slug": "tm-749", "name": "FC Empoli", "short": "FC", "api_id": null, "period": "2019–2021", "logo": "images/clubs/chart/tm-749.png"}}, {"label": "2020", "value_label": "€7,50 млн", "value": 7.5, "club": {"slug": "tm-749", "name": "FC Empoli", "short": "FC", "api_id": null, "period": "2019–2021", "logo": "images/clubs/chart/tm-749.png"}}, {"label": "2022", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "torino-fc", "name": "Torino FC", "short": "TOR", "api_id": 503, "period": "2021–2024", "logo": "images/clubs/api/503.png"}}, {"label": "2024", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "torino-fc", "name": "Torino FC", "short": "TOR", "api_id": 503, "period": "2021–2024", "logo": "images/clubs/api/503.png"}}, {"label": "мар. 2025", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "torino-fc", "name": "Torino FC", "short": "TOR", "api_id": 503, "period": "2021–2024", "logo": "images/clubs/api/503.png"}}, {"label": "окт. 2025", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2025", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}, {"label": "2026", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2025", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}]}, {"key": "youssouf-fofana-sevilla-fc-step4", "name": "Youssouf Fofana", "paths": ["/transfers/youssouf-fofana-sevilla-fc/"], "points": [{"label": "2018", "value_label": "€150 тыс.", "value": 0.15, "club": {"slug": "rc-strasbourg-alsace", "name": "RC Strasbourg Alsace", "short": "STR", "api_id": 95, "period": "2018–2019", "logo": "images/clubs/api/rendered/95-94fa45143780.png"}}, {"label": "2020", "value_label": "€12 млн", "value": 12.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2019–2023", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "май 2022", "value_label": "€18 млн", "value": 18.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2019–2023", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "ноя. 2022", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2019–2023", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "июнь 2024", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "as-monaco", "name": "AS Monaco", "short": "MON", "api_id": 91, "period": "2019–2023", "logo": "images/clubs/api/rendered/91-371080d3fd97.png"}}, {"label": "дек. 2024", "value_label": "€30 млн", "value": 30.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2024", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}, {"label": "2026", "value_label": "€23 млн", "value": 23.0, "club": {"slug": "ac-milan", "name": "AC Milan", "short": "MIL", "api_id": 489, "period": "с 2024", "logo": "images/clubs/api/rendered/489-dcceb506e62c.png"}}]}, {"key": "el-hadji-malick-diouf-brentford-fc-step4", "name": "El Hadji Malick Diouf", "paths": ["/transfers/el-hadji-malick-diouf-brentford-fc/"], "points": [{"label": "2023", "value_label": "€25 тыс.", "value": 0.03, "club": {"slug": "tm-1293", "name": "Tromsø IL", "short": "TRO", "api_id": null, "period": "2022", "logo": "images/clubs/chart/tm-1293.png"}}, {"label": "июнь 2024", "value_label": "€2 млн", "value": 2.0, "club": {"slug": "tm-62", "name": "SK Slavia Prague", "short": "SSP", "api_id": null, "period": "2023–2024", "logo": "images/clubs/chart/tm-62.png"}}, {"label": "сен. 2024", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "tm-62", "name": "SK Slavia Prague", "short": "SSP", "api_id": null, "period": "2023–2024", "logo": "images/clubs/chart/tm-62.png"}}, {"label": "дек. 2024", "value_label": "€16 млн", "value": 16.0, "club": {"slug": "tm-62", "name": "SK Slavia Prague", "short": "SSP", "api_id": null, "period": "2023–2024", "logo": "images/clubs/chart/tm-62.png"}}, {"label": "окт. 2025", "value_label": "€25 млн", "value": 25.0, "club": {"slug": "tm-379", "name": "West Ham United", "short": "WHU", "api_id": null, "period": "с 2025", "logo": "images/clubs/chart/tm-379.png"}}, {"label": "дек. 2025", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "tm-379", "name": "West Ham United", "short": "WHU", "api_id": null, "period": "с 2025", "logo": "images/clubs/chart/tm-379.png"}}, {"label": "2026", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "tm-379", "name": "West Ham United", "short": "WHU", "api_id": null, "period": "с 2025", "logo": "images/clubs/chart/tm-379.png"}}]}, {"key": "jonathan-rowe-atalanta-bc-step4", "name": "Jonathan Rowe", "paths": ["/transfers/jonathan-rowe-atalanta-bc/"], "points": [{"label": "2022", "value_label": "€800 тыс.", "value": 0.8, "club": {"slug": "tm-1123", "name": "Norwich City", "short": "NOR", "api_id": null, "period": "2021–2023", "logo": "images/clubs/chart/tm-1123.png"}}, {"label": "2023", "value_label": "€5 млн", "value": 5.0, "club": {"slug": "tm-1123", "name": "Norwich City", "short": "NOR", "api_id": null, "period": "2021–2023", "logo": "images/clubs/chart/tm-1123.png"}}, {"label": "мар. 2024", "value_label": "€7 млн", "value": 7.0, "club": {"slug": "tm-1123", "name": "Norwich City", "short": "NOR", "api_id": null, "period": "2021–2023", "logo": "images/clubs/chart/tm-1123.png"}}, {"label": "окт. 2024", "value_label": "€10 млн", "value": 10.0, "club": {"slug": "olympique-marseille", "name": "Olympique Marseille", "short": "MAR", "api_id": 81, "period": "2024", "logo": "images/clubs/api/rendered/81-f781160a86a8.png"}}, {"label": "2025", "value_label": "€17 млн", "value": 17.0, "club": {"slug": "bologna-fc-1909", "name": "Bologna FC 1909", "short": "BOL", "api_id": 500, "period": "с 2025", "logo": "images/clubs/api/500.png"}}, {"label": "мар. 2026", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "bologna-fc-1909", "name": "Bologna FC 1909", "short": "BOL", "api_id": 500, "period": "с 2025", "logo": "images/clubs/api/500.png"}}, {"label": "май 2026", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "bologna-fc-1909", "name": "Bologna FC 1909", "short": "BOL", "api_id": 500, "period": "с 2025", "logo": "images/clubs/api/500.png"}}]}, {"key": "karim-coulibaly-rc-strasbourg-alsace-step4", "name": "Karim Coulibaly", "paths": ["/transfers/karim-coulibaly-rc-strasbourg-alsace/"], "points": [{"label": "авг. 2025", "value_label": "€1 млн", "value": 1.0, "club": {"slug": "sv-werder-bremen", "name": "SV Werder Bremen", "short": "WER", "api_id": 162, "period": "с 2025", "logo": "images/clubs/api/rendered/162-076ca6ba9cbf.png"}}, {"label": "окт. 2025", "value_label": "€8 млн", "value": 8.0, "club": {"slug": "sv-werder-bremen", "name": "SV Werder Bremen", "short": "WER", "api_id": 162, "period": "с 2025", "logo": "images/clubs/api/rendered/162-076ca6ba9cbf.png"}}, {"label": "дек. 2025", "value_label": "€20 млн", "value": 20.0, "club": {"slug": "sv-werder-bremen", "name": "SV Werder Bremen", "short": "WER", "api_id": 162, "period": "с 2025", "logo": "images/clubs/api/rendered/162-076ca6ba9cbf.png"}}, {"label": "мар. 2026", "value_label": "€22 млн", "value": 22.0, "club": {"slug": "sv-werder-bremen", "name": "SV Werder Bremen", "short": "WER", "api_id": 162, "period": "с 2025", "logo": "images/clubs/api/rendered/162-076ca6ba9cbf.png"}}, {"label": "май 2026", "value_label": "€28 млн", "value": 28.0, "club": {"slug": "sv-werder-bremen", "name": "SV Werder Bremen", "short": "WER", "api_id": 162, "period": "с 2025", "logo": "images/clubs/api/rendered/162-076ca6ba9cbf.png"}}]}];

    const normalizePath = (value) => {
        let path = String(value || "")
            .split("?")[0]
            .split("#")[0]
            .replace(/\\/g, "/")
            .replace(/\/+/g, "/")
            .toLowerCase();

        if (path.endsWith("/index.html")) {
            path = path.slice(0, -"index.html".length);
        }

        if (!path.endsWith("/")) {
            path += "/";
        }

        return path;
    };

    const escapeHTML = (value) => String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

    const currentPath = normalizePath(window.location.pathname);
    const basePath = currentPath.includes("/promyachik/")
        ? "/promyachik/"
        : "/";

    const player = PLAYERS.find((candidate) =>
        candidate.paths.some((path) =>
            currentPath.endsWith(normalizePath(path))
        )
    );

    if (!player) {
        return;
    }

    const logoCandidates = (club) => {
        const result = [];
        const stable = `images/clubs/chart/${club.slug}`;

        if (club.logo) {
            const localLogo = String(club.logo).replace(/^\/+/, "");
            result.push(`${basePath}${localLogo}`);
        }

        result.push(
            `${basePath}${stable}.png`,
            `${basePath}${stable}.webp`,
            `${basePath}${stable}.jpg`,
            `${basePath}${stable}.svg`
        );

        if (club.api_id) {
            result.push(
                `${basePath}images/clubs/${club.api_id}.png`,
                `${basePath}images/clubs/api/${club.api_id}.png`,
                `${basePath}images/teams/${club.api_id}.png`,
                `${basePath}images/clubs/${club.api_id}.webp`,
                `${basePath}images/clubs/${club.api_id}.svg`
            );
        }

        return Array.from(new Set(result));
    };

    const setLogoSource = (image, candidates, fallback) => {
        let index = 0;

        const showFallback = () => {
            image.hidden = true;
            image.removeAttribute("src");
            fallback.hidden = false;
        };

        const loadNext = () => {
            if (index >= candidates.length) {
                showFallback();
                return;
            }
            image.hidden = true;
            fallback.hidden = true;
            image.src = candidates[index];
            index += 1;
        };

        image.addEventListener("load", () => {
            image.hidden = false;
            fallback.hidden = true;
        });
        image.addEventListener("error", loadNext);
        loadNext();
    };

    const normalizeClubLogo = (image) => {
        if (
            image.dataset.visibleLogoNormalized === "1"
            || !image.complete
            || image.naturalWidth < 1
            || image.naturalHeight < 1
        ) {
            return;
        }

        try {
            const source = document.createElement("canvas");
            const sourceContext = source.getContext(
                "2d",
                { willReadFrequently: true }
            );

            if (!sourceContext) {
                return;
            }

            source.width = image.naturalWidth;
            source.height = image.naturalHeight;

            sourceContext.drawImage(
                image,
                0,
                0,
                source.width,
                source.height
            );

            const pixels = sourceContext.getImageData(
                0,
                0,
                source.width,
                source.height
            );

            let left = source.width;
            let right = -1;
            let top = source.height;
            let bottom = -1;

            for (let y = 0; y < source.height; y += 1) {
                for (let x = 0; x < source.width; x += 1) {
                    const alpha =
                        pixels.data[
                            ((y * source.width) + x) * 4 + 3
                        ];

                    if (alpha <= 12) {
                        continue;
                    }

                    left = Math.min(left, x);
                    right = Math.max(right, x);
                    top = Math.min(top, y);
                    bottom = Math.max(bottom, y);
                }
            }

            if (right < left || bottom < top) {
                image.dataset.visibleLogoNormalized = "1";
                return;
            }

            const cropWidth = right - left + 1;
            const cropHeight = bottom - top + 1;
            const outputSize = 160;
            const padding = 8;
            const available = outputSize - (padding * 2);
            const scale = Math.min(
                available / cropWidth,
                available / cropHeight
            );

            const drawWidth = cropWidth * scale;
            const drawHeight = cropHeight * scale;
            const drawX = (outputSize - drawWidth) / 2;
            const drawY = (outputSize - drawHeight) / 2;

            const output = document.createElement("canvas");
            const outputContext = output.getContext("2d");

            if (!outputContext) {
                return;
            }

            output.width = outputSize;
            output.height = outputSize;

            outputContext.drawImage(
                source,
                left,
                top,
                cropWidth,
                cropHeight,
                drawX,
                drawY,
                drawWidth,
                drawHeight
            );

            image.dataset.visibleLogoNormalized = "1";
            image.src = output.toDataURL("image/png");
        } catch (_error) {
            image.dataset.visibleLogoNormalized = "1";
        }
    };

    const geometry = (points) => {
        const values = points.map((point) => Number(point.value));
        const maximum = Math.max(...values, 1) * 1.12;
        const left = 20;
        const right = 300;
        const top = 52;
        const bottom = 122;

        const coordinates = points.map((point, index) => {
            const x = points.length === 1
                ? left
                : left + ((right - left) * index) / (points.length - 1);

            const y = bottom
                - ((Number(point.value) / maximum) * (bottom - top));

            return {
                x: Number(x.toFixed(2)),
                y: Number(y.toFixed(2)),
            };
        });

        const line = coordinates
            .map((point, index) =>
                `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`
            )
            .join(" ");

        const last =
            coordinates[coordinates.length - 1];

        const area =
            `${line} L ${last.x} ${bottom} `
            + `L ${coordinates[0].x} ${bottom} Z`;

        return { coordinates, line, area };
    };

    const ensureChartModal = () => {
        let modal = document.querySelector(
            ".player-market-chart-modal"
        );

        if (modal) {
            return modal;
        }

        modal = document.createElement("div");
        modal.className = "player-market-chart-modal";
        modal.hidden = true;

        modal.innerHTML = `
            <div
                class="player-market-chart-modal__backdrop"
                data-close-market-chart-modal
            ></div>

            <section
                class="player-market-chart-modal__dialog"
                role="dialog"
                aria-modal="true"
                aria-label="Увеличенный график стоимости игрока"
            >
                <button
                    class="player-market-chart-modal__close"
                    type="button"
                    aria-label="Закрыть увеличенный график"
                    data-close-market-chart-modal
                >
                    ×
                </button>

                <div
                    class="player-market-chart-modal__content"
                ></div>
            </section>
        `;

        document.body.appendChild(modal);

        const close = () => {
            modal.hidden = true;
            modal
                .querySelector(
                    ".player-market-chart-modal__content"
                )
                .replaceChildren();

            document.body.classList.remove(
                "player-market-chart-modal-open"
            );
        };

        modal.addEventListener("click", (event) => {
            if (
                event.target.closest(
                    "[data-close-market-chart-modal]"
                )
            ) {
                close();
            }
        });

        document.addEventListener("keydown", (event) => {
            if (
                event.key === "Escape"
                && !modal.hidden
            ) {
                close();
            }
        });

        return modal;
    };

    const openChartModal = (chartElement) => {
        const modal = ensureChartModal();
        const content = modal.querySelector(
            ".player-market-chart-modal__content"
        );

        const enlargedChart = chartElement.cloneNode(true);
enlargedChart.classList.add(
            "player-market-chart--enlarged"
        );

        enlargedChart.removeAttribute("tabindex");
        enlargedChart.removeAttribute("role");

        content.replaceChildren(enlargedChart);

        /* PROMYACHIK 045 PREALIGN MARKET CHART MODAL START */
        const promyachikMarketAligner045 = window.__promyachikMarketValueLabelsStandard279;
        const promyachikShouldPrealignMarketModal045 =
            promyachikMarketAligner045 &&
            enlargedChart &&
            enlargedChart.classList &&
            enlargedChart.classList.contains("player-market-chart");

        if (promyachikShouldPrealignMarketModal045) {
            modal.style.setProperty("visibility", "hidden", "important");
        }
        /* PROMYACHIK 045 PREALIGN MARKET CHART MODAL END */

        modal.hidden = false;
document.body.classList.add(
            "player-market-chart-modal-open"
        );

        
        /* PROMYACHIK 045 PREALIGN MARKET CHART MODAL START */
        if (promyachikShouldPrealignMarketModal045) {
            const promyachikShowAlignedMarketModal045 = () => {
                try {
                    promyachikMarketAligner045.alignChart(enlargedChart);
                } finally {
                    modal.style.removeProperty("visibility");
                }
            };

            window.requestAnimationFrame(() => {
                promyachikMarketAligner045.alignChart(enlargedChart);
                window.requestAnimationFrame(promyachikShowAlignedMarketModal045);
            });
        }
        /* PROMYACHIK 045 PREALIGN MARKET CHART MODAL END */
modal
            .querySelector(
                ".player-market-chart-modal__close"
            )
            .focus();
    };

    const extendFinalTransferSegment = (chart) => {
        const coordinates = chart.coordinates.map(
            (point) => ({ ...point })
        );

        if (coordinates.length < 2) {
            return chart;
        }

        const lastIndex = coordinates.length - 1;
        const previous = coordinates[lastIndex - 1];
        const originalLast = coordinates[lastIndex];

        const edgeX = 296;
        const bottom = 122;
        const horizontalDistance = Math.max(
            1,
            originalLast.x - previous.x
        );
        const extensionRatio = Math.max(
            0,
            (edgeX - originalLast.x)
            / horizontalDistance
        );
        const trendDelta =
            originalLast.y - previous.y;
        const naturalShift =
            trendDelta * extensionRatio;
        const visualShift = Math.max(
            -5,
            Math.min(
                5,
                trendDelta * 0.12
            )
        );
        const edgeY = Math.max(
            16,
            Math.min(
                bottom - 8,
                originalLast.y
                + naturalShift
                + visualShift
            )
        );

        coordinates[lastIndex] = {
            ...originalLast,
            x: edgeX,
            y: Number(edgeY.toFixed(2)),
        };

        const line = coordinates
            .map((point, index) =>
                `${index === 0 ? "M" : "L"} `
                + `${point.x} ${point.y}`
            )
            .join(" ");

        const last = coordinates[lastIndex];
        const area =
            `${line} L ${last.x} ${bottom} `
            + `L ${coordinates[0].x} ${bottom} Z`;

        return {
            ...chart,
            coordinates,
            line,
            area,
        };
    };

    const createChart = () => {
        const chart = extendFinalTransferSegment(geometry(player.points));
        const section = document.createElement("section");

        section.className = "player-market-chart";
        section.dataset.marketChartKey = player.key;
        section.setAttribute(
            "aria-label",
            `Изменение рыночной стоимости ${player.name}`
        );

        const circles = chart.coordinates.map((coordinate, index) => {
            const item = player.points[index];

            return `
                <circle
                    class="player-market-chart__dot"
                    cx="${coordinate.x}"
                    cy="${coordinate.y}"
                    r="4.4"
                >
                    <title>
                        ${escapeHTML(item.club.name)} ·
                        ${escapeHTML(item.label)} ·
                        ${escapeHTML(item.value_label)}
                    </title>
                </circle>
            `;
        }).join("");

        const labels = player.points.map((item) => `
            <span class="player-market-chart__point">
                <small>${escapeHTML(item.label)}</small>
                <strong>${escapeHTML(
                    item.value_label.replace(/^€\s*/, "€\u202F")
                )}</strong>
            </span>
        `).join("");

        section.innerHTML = `
            <div class="player-market-chart__canvas">
                <svg
                    viewBox="0 0 320 150"
                    role="img"
                    aria-label="График стоимости ${escapeHTML(player.name)}"
                    preserveAspectRatio="none"
                >
                    <defs>
                        <linearGradient
                            id="pf-market-gradient-${escapeHTML(player.key)}"
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                        >
                            <stop
                                offset="0%"
                                stop-color="#e7c65b"
                                stop-opacity="0.32"
                            ></stop>
                            <stop
                                offset="100%"
                                stop-color="#e7c65b"
                                stop-opacity="0"
                            ></stop>
                        </linearGradient>

                        
                    </defs>

                    <line class="player-market-chart__grid" x1="18" y1="52" x2="302" y2="52"></line>
                    <line class="player-market-chart__grid" x1="18" y1="86" x2="302" y2="86"></line>
                    <line class="player-market-chart__grid" x1="18" y1="122" x2="302" y2="122"></line>

                    <path
                        class="player-market-chart__area"
                        fill="url(#pf-market-gradient-${escapeHTML(player.key)})"
                        d="${escapeHTML(chart.area)}"
                    ></path>

                    <path
                        class="player-market-chart__line"
                        d="${escapeHTML(chart.line)}"
                    ></path>

                    ${circles}
                </svg>

                <div class="player-market-chart__club-layer"></div>
            </div>

            <div
                class="player-market-chart__points"
                style="--market-point-count:${player.points.length};"
            >
                ${labels}
            </div>

            <p class="player-market-chart__note">ценочная рыночная стоимость. е является суммой трансфера.</p>
        `;

        const layer = section.querySelector(".player-market-chart__club-layer");

        player.points.forEach((item, index) => {
            const coordinate = chart.coordinates[index];
            const marker = document.createElement("span");
            const image = document.createElement("img");
            const fallback = document.createElement("span");
            const fallbackName = document.createElement("span");

            marker.className =
                "player-market-chart__club-marker";

            if (index === player.points.length - 1) {
                marker.classList.add(
                    "player-market-chart__club-marker--last"
                );
            }



            marker.dataset.clubSlug = item.club.slug;
            marker.dataset.clubName = item.club.name;

            marker.style.left =
                `${(coordinate.x / 320) * 100}%`;

            marker.style.top =
                `${(coordinate.y / 150) * 100}%`;

            marker.setAttribute(
                "aria-label",
                `${item.club.name} · ${item.label} · ${item.value_label}`
            );

            image.className =
                "player-market-chart__club-logo";
            image.alt = "";
            image.setAttribute("aria-hidden", "true");
            image.loading = "eager";
            image.hidden = true;

            fallback.className =
                "player-market-chart__club-fallback";
            fallback.textContent =
                Array.from(String(item.club.name || "?").trim())[0]?.toUpperCase() || "?";
            fallback.dataset.clubName = item.club.name;
            fallback.setAttribute("aria-label", item.club.name);
            fallback.tabIndex = 0;
            fallback.hidden = true;

            fallbackName.className =
                "player-market-chart__club-fallback-name";
            fallbackName.textContent = item.club.name;
            fallbackName.setAttribute("aria-hidden", "true");

            image.addEventListener(
                "load",
                () => normalizeClubLogo(image)
            );

            if (item.club.logo) {
                setLogoSource(
                    image,
                    logoCandidates(item.club),
                    fallback
                );
            } else {
                image.hidden = true;
                image.removeAttribute("src");
                fallback.hidden = false;
            }

            marker.appendChild(image);
            marker.appendChild(fallback);
            marker.appendChild(fallbackName);
            layer.appendChild(marker);
        });

        section.classList.add(
            "player-market-chart--zoomable"
        );

        section.tabIndex = 0;
        section.setAttribute("role", "button");

        section.setAttribute(
            "aria-label",
            `Увеличить график стоимости ${player.name}`
        );

        section.addEventListener("click", (event) => {
            if (
                event.currentTarget.classList.contains(
                    "player-market-chart--enlarged"
                )
            ) {
                return;
            }

            openChartModal(section);
        });

        section.addEventListener("keydown", (event) => {
            if (
                event.key === "Enter"
                || event.key === " "
            ) {
                event.preventDefault();
                openChartModal(section);
            }
        });

        return section;
    };

    const card =
        document.querySelector(".player-brief")
        || document.querySelector(".transfer-player-card");

    if (!card) {
        return;
    }

    const existingCharts = Array.from(
        document.querySelectorAll(".player-market-chart")
    );

    existingCharts.forEach((existing) => existing.remove());

    const chart = createChart();
    const details = card.querySelector(".player-brief__list, dl");

    if (details) {
        details.insertAdjacentElement("afterend", chart);
    } else {
        card.appendChild(chart);
    }

    document.body.classList.add("transfer-page");
})();

/* PROFUTBIK STATS UNDER MARKET CHART V154 START */
(function () {
    function moveTransferStatsUnderMarketChart() {
        const page = document.querySelector("body.transfer-page");
        if (!page) return;

        const chart = page.querySelector(".player-market-chart:not(.player-market-chart--enlarged)");
        const stats = page.querySelector(".transfer-stats");

        if (!chart || !stats) return;

        if (stats.previousElementSibling !== chart) {
            chart.insertAdjacentElement("afterend", stats);
        }

        stats.classList.add("transfer-stats--under-market-chart");

        const width = Math.round(chart.getBoundingClientRect().width);
        if (width > 0) {
            stats.style.maxWidth = width + "px";
        }
    }

    function scheduleMove() {
        moveTransferStatsUnderMarketChart();
        window.setTimeout(moveTransferStatsUnderMarketChart, 80);
        window.setTimeout(moveTransferStatsUnderMarketChart, 300);
        window.setTimeout(moveTransferStatsUnderMarketChart, 900);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", scheduleMove);
    } else {
        scheduleMove();
    }

    window.addEventListener("load", scheduleMove);
    window.addEventListener("resize", moveTransferStatsUnderMarketChart);

    const observer = new MutationObserver(moveTransferStatsUnderMarketChart);
    observer.observe(document.documentElement, {
        childList: true,
        subtree: true
    });
})();
 /* PROFUTBIK STATS UNDER MARKET CHART V154 END */

/* PROFUTBIK LOAD FONTAWESOME V162 START */
(function () {
    const id = "profutbik-fontawesome-free";
    if (document.getElementById(id)) return;

    const link = document.createElement("link");
    link.id = id;
    link.rel = "stylesheet";
    link.href = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css";
    link.crossOrigin = "anonymous";
    link.referrerPolicy = "no-referrer";
    document.head.appendChild(link);
})();
 /* PROFUTBIK LOAD FONTAWESOME V162 END */

/* PROFUTBIK STATS ICON_ONLY TOOLTIP V177 START */
(function () {
    function setupProfutbikStatsTooltips() {
        var statsBlocks = document.querySelectorAll('.transfer-stats--under-market-chart, .transfer-stats');

        statsBlocks.forEach(function (block) {
            var cards = block.querySelectorAll('.transfer-stats__card');

            var tooltipNames = {
                1: 'Матчей',
                2: 'Голов',
                3: 'Голевых передач',
                5: 'Жёлтых карточек',
                6: 'Красных карточек'
            };

            Object.keys(tooltipNames).forEach(function (key) {
                var index = parseInt(key, 10) - 1;
                var card = cards[index];

                if (!card) {
                    return;
                }

                var valueEl = card.querySelector('strong');
                var value = valueEl ? valueEl.textContent.trim() : '';

                if (!value) {
                    return;
                }

                card.setAttribute('data-profutbik-tooltip', tooltipNames[key] + ': ' + value);
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupProfutbikStatsTooltips);
    } else {
        setupProfutbikStatsTooltips();
    }

    window.addEventListener('load', function () {
        setTimeout(setupProfutbikStatsTooltips, 250);
    });
})();
/* PROFUTBIK STATS ICON_ONLY TOOLTIP V177 END */

/* PROMYACHIK 279 ALIGN MARKET PRICE LABELS TO POINTS START */
(function () {
  if (window.__promyachikMarketValueLabelsStandard279) {
    return;
  }

  const GOLD = "#f5c741";
  const CHART_SELECTOR = ".player-market-chart";
  const ROW_SELECTOR = ".player-market-chart__points";
  const ITEM_SELECTOR = ".player-market-chart__point";
  const DOT_SELECTOR = ".player-market-chart__dot, circle.player-market-chart__dot, svg circle";
  const CLUB_MARKER_SELECTOR = ".player-market-chart__club-marker";

  let timer = null;

  const centerX = (rect) => rect.left + rect.width / 2;

  const validRect = (element) => {
    if (!element || !element.getBoundingClientRect) {
      return null;
    }

    const rect = element.getBoundingClientRect();

    if (!rect || rect.width < 1 || rect.height < 1) {
      return null;
    }

    return rect;
  };

  const sortByX = (elements) => {
    return Array.from(elements)
      .map((element) => ({ element, rect: validRect(element) }))
      .filter((item) => item.rect)
      .sort((a, b) => centerX(a.rect) - centerX(b.rect));
  };

  const getTargets = (chart) => {
    const dots = sortByX(chart.querySelectorAll(DOT_SELECTOR));

    if (dots.length) {
      return dots;
    }

    return sortByX(chart.querySelectorAll(CLUB_MARKER_SELECTOR));
  };

  const applyGold = (point) => {
    const small = point.querySelector("small");
    const strong = point.querySelector("strong");

    if (small) {
      small.style.setProperty("display", "none", "important");
    }

    if (strong) {
      strong.style.setProperty("display", "block", "important");
      strong.style.setProperty("color", GOLD, "important");
      strong.style.setProperty("-webkit-text-fill-color", GOLD, "important");
      strong.style.setProperty("font-weight", "900", "important");
      strong.style.setProperty("white-space", "nowrap", "important");
      strong.style.setProperty(
        "text-shadow",
        "0 0 10px rgba(245,199,65,.45), 0 2px 8px rgba(0,0,0,.9)",
        "important"
      );
      strong.style.setProperty("transition", "none", "important");
      strong.style.setProperty("animation", "none", "important");
    }
  };

  const alignChart = (chart) => {
    if (!chart || !chart.querySelector) {
      return;
    }

    const row = chart.querySelector(ROW_SELECTOR);

    if (!row) {
      return;
    }

    const points = Array.from(row.querySelectorAll(ITEM_SELECTOR));

    if (!points.length) {
      return;
    }

    const targets = getTargets(chart);

    if (!targets.length) {
      return;
    }

    const chartRect = chart.getBoundingClientRect();

    if (!chartRect || chartRect.width < 1 || chartRect.height < 1) {
      return;
    }

    chart.classList.add("promyachik-market-chart-labels-standard-279");
    chart.style.setProperty("position", "relative", "important");

    row.classList.add("promyachik-price-align-279");
    row.style.setProperty("position", "absolute", "important");
    row.style.setProperty("inset", "0", "important");
    row.style.setProperty("display", "block", "important");
    row.style.setProperty("width", "100%", "important");
    row.style.setProperty("height", "100%", "important");
    row.style.setProperty("min-height", "0", "important");
    row.style.setProperty("margin", "0", "important");
    row.style.setProperty("padding", "0", "important");
    row.style.setProperty("pointer-events", "none", "important");
    row.style.setProperty("z-index", "80", "important");
    row.style.setProperty("transition", "none", "important");
    row.style.setProperty("animation", "none", "important");

    points.forEach((point, index) => {
      const strong = point.querySelector("strong");

      if (!strong || !strong.textContent.trim()) {
        return;
      }

      const target = targets[Math.min(index, targets.length - 1)];
      const rect = target.rect;

      let left = centerX(rect) - chartRect.left;
      let top = rect.bottom - chartRect.top + 8;

      if (left < 28) {
        left = 18;
      }

      if (left > chartRect.width - 28) {
        left = chartRect.width - 18;
      }

      let transform = "translateX(-50%)";

      if (left <= 20) {
        transform = "translateX(0)";
      } else if (left >= chartRect.width - 20) {
        transform = "translateX(-100%)";
      }

      point.classList.add("promyachik-price-align-item-279");
      point.style.setProperty("position", "absolute", "important");
      point.style.setProperty("inset", `${top}px auto auto ${left}px`, "important");
      point.style.setProperty("display", "block", "important");
      point.style.setProperty("visibility", "visible", "important");
      point.style.setProperty("opacity", "1", "important");
      point.style.setProperty("width", "max-content", "important");
      point.style.setProperty("min-width", "0", "important");
      point.style.setProperty("max-width", "78px", "important");
      point.style.setProperty("margin", "0", "important");
      point.style.setProperty("padding", "0", "important");
      point.style.setProperty("pointer-events", "none", "important");
      point.style.setProperty("z-index", "90", "important");
      point.style.setProperty("text-align", "center", "important");
      point.style.setProperty("transform", transform, "important");
      point.style.setProperty("transition", "none", "important");
      point.style.setProperty("animation", "none", "important");

      applyGold(point);
    });
  };

  const alignAllCharts = () => {
    Array.from(document.querySelectorAll(CHART_SELECTOR)).forEach(alignChart);
  };

  const scheduleAlign = () => {
    if (timer) {
      window.clearTimeout(timer);
    }

    window.requestAnimationFrame(() => {
      alignAllCharts();
      timer = window.setTimeout(alignAllCharts, 120);
    });
  };

  window.__promyachikMarketValueLabelsStandard279 = {
    alignChart,
    alignAllCharts,
    scheduleAlign
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleAlign);
  } else {
    scheduleAlign();
  }

  window.addEventListener("load", scheduleAlign);
  window.addEventListener("resize", scheduleAlign);

  const observer = new MutationObserver(scheduleAlign);
  observer.observe(document.documentElement, {
    childList: true,
    subtree: true
  });
})();
/* PROMYACHIK 279 ALIGN MARKET PRICE LABELS TO POINTS END */


/* PROMYACHIK 280 SHORTEN THOUSAND EURO LABELS TO K START */
(function () {
  "use strict";

  if (window.__promyachik280ShortenThousandEuroLabelsReady) {
    return;
  }
  window.__promyachik280ShortenThousandEuroLabelsReady = true;

  const normalizeMarketText280 = function (text) {
    if (!text || !/(тыс|тысяч)/i.test(text)) {
      return text;
    }

    return String(text)
      .replace(/€\s*([0-9]+(?:[.,][0-9]+)?)\s*(?:тысяч|тыс\.?)\s*(?:евро)?/gi, "€$1K")
      .replace(/([0-9]+(?:[.,][0-9]+)?)\s*(?:тысяч|тыс\.?)\s*евро/gi, "$1K")
      .replace(/([0-9]+(?:[.,][0-9]+)?)\s*(?:тысяч|тыс\.?)\b/gi, "$1K")
      .replace(/\s+K\b/g, "K");
  };

  const normalizeChartNode280 = function (root) {
    const base = root && root.nodeType === 1 ? root : document;
    const charts = [];

    if (base.matches && base.matches(".player-market-chart")) {
      charts.push(base);
    }

    if (base.querySelectorAll) {
      base.querySelectorAll(".player-market-chart").forEach(function (chart) {
        charts.push(chart);
      });
    }

    charts.forEach(function (chart) {
      const walker = document.createTreeWalker(chart, NodeFilter.SHOW_TEXT);
      const textNodes = [];
      let node = walker.nextNode();

      while (node) {
        textNodes.push(node);
        node = walker.nextNode();
      }

      textNodes.forEach(function (textNode) {
        const nextValue = normalizeMarketText280(textNode.nodeValue);
        if (nextValue !== textNode.nodeValue) {
          textNode.nodeValue = nextValue;
        }
      });
    });
  };

  const runNormalize280 = function () {
    normalizeChartNode280(document);
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", runNormalize280, { once: true });
  } else {
    runNormalize280();
  }

  window.requestAnimationFrame(runNormalize280);
  window.setTimeout(runNormalize280, 150);
  window.setTimeout(runNormalize280, 500);

  const observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      mutation.addedNodes.forEach(function (node) {
        normalizeChartNode280(node);
      });
    });
  });

  observer.observe(document.documentElement, {
    childList: true,
    subtree: true
  });
})();
/* PROMYACHIK 280 SHORTEN THOUSAND EURO LABELS TO K END */
/* PROFUTBIK STEP4 UNIVERSAL CLUB LOGO FALLBACK 448G */
/* PROFUTBIK STEP4 UNIVERSAL MISSING CLUB FALLBACK RENDER FIX VALIDATED 448I */
window.__PFClubFallbackVersion = "448j-data-flag";
/* PROFUTBIK STEP4 MISSING CLUB FALLBACK FROM DATA FLAG 448J */
