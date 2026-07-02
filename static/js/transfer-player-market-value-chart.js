(() => {
    "use strict";

    const VERSION = "42-pull-last-point-inside-keep-center";
    window.__PFMarketChartVersion = VERSION;

    const PLAYERS = [{"key":"mbappe","name":"Килиан Мбаппе","paths":["/transfers/kylian-mbappe-real-madrid/"],"points":[{"label":"2017","value_label":"€35 млн","value":35,"club":{"slug":"monaco","name":"AS Monaco","short":"ASM","api_id":91,"period":"2015–2017"}},{"label":"2018","value_label":"€120 млн","value":120,"club":{"slug":"psg","name":"Paris Saint-Germain","short":"PSG","api_id":85,"period":"2017–2024"}},{"label":"2025","value_label":"€200 млн","value":200,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2024"}},{"label":"2026","value_label":"€180 млн","value":180,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2024"}}]},{"key":"wirtz","name":"Флориан Вирц","paths":["/transfers/florian-wirtz-liverpool/"],"points":[{"label":"2023","value_label":"€100 млн","value":100,"club":{"slug":"bayer-leverkusen","name":"Bayer Leverkusen","short":"B04","api_id":168,"period":"2020–2025"}},{"label":"июнь 2025","value_label":"€140 млн","value":140,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"с 2025"}},{"label":"дек. 2025","value_label":"€110 млн","value":110,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"с 2025"}},{"label":"2026","value_label":"€100 млн","value":100,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"с 2025"}}]},{"key":"konate","name":"Ибраима Конате","paths":["/transfers/ibrahima-konate-real-madrid/"],"points":[{"label":"2017","value_label":"€300 тыс.","value":0.3,"club":{"slug":"rb-leipzig","name":"RB Leipzig","short":"RBL","api_id":173,"period":"2017–2021"}},{"label":"2021","value_label":"€35 млн","value":35,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"2021–2026"}},{"label":"2025","value_label":"€60 млн","value":60,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"2021–2026"}},{"label":"2026","value_label":"€45 млн","value":45,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2026"}}]},{"key":"cucurella","name":"Марк Кукурелья","paths":["/transfers/marc-cucurella-real-madrid/"],"points":[{"label":"2018","value_label":"€5 млн","value":5,"club":{"slug":"barcelona","name":"Barcelona","short":"FCB","api_id":529,"period":"до 2019"}},{"label":"2019","value_label":"€10 млн","value":10,"club":{"slug":"getafe","name":"Getafe","short":"GET","api_id":546,"period":"2019–2021"}},{"label":"2020","value_label":"€18 млн","value":18,"club":{"slug":"getafe","name":"Getafe","short":"GET","api_id":546,"period":"2019–2021"}},{"label":"2021","value_label":"€20 млн","value":20,"club":{"slug":"brighton","name":"Brighton & Hove Albion","short":"BHA","api_id":51,"period":"2021–2022"}},{"label":"2026","value_label":"€50 млн","value":50,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2026"}}]},{"key":"dumfries","name":"Дензел Дюмфрис","paths":["/transfers/denzel-dumfries-real-madrid/"],"points":[{"label":"2015","value_label":"€50 тыс.","value":0.05,"club":{"slug":"sparta-rotterdam","name":"Sparta Rotterdam","short":"SPA","api_id":null,"period":"2014–2017"}},{"label":"2017","value_label":"€1 млн","value":1,"club":{"slug":"heerenveen","name":"SC Heerenveen","short":"HEE","api_id":null,"period":"2017–2018"}},{"label":"2018","value_label":"€4 млн","value":4,"club":{"slug":"psv","name":"PSV Eindhoven","short":"PSV","api_id":197,"period":"2018–2021"}},{"label":"2021","value_label":"€16 млн","value":16,"club":{"slug":"inter","name":"Inter","short":"INT","api_id":505,"period":"с 2021"}},{"label":"2025","value_label":"€35 млн","value":35,"club":{"slug":"inter","name":"Inter","short":"INT","api_id":505,"period":"с 2021"}},{"label":"2026","value_label":"€25 млн","value":25,"club":{"slug":"inter","name":"Inter","short":"INT","api_id":505,"period":"с 2021"}}]},{"key":"alvarez","name":"Хулиан Альварес","paths":["/transfers/julian-alvarez-barcelona/"],"points":[{"label":"янв. 2022","value_label":"€20 млн","value":20,"club":{"slug":"river-plate","name":"River Plate","short":"CARP","api_id":null,"period":"2018–2022"}},{"label":"июль 2022","value_label":"€23 млн","value":23,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2022–2024"}},{"label":"2023","value_label":"€90 млн","value":90,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2022–2024"}},{"label":"май 2026","value_label":"€90 млн","value":90,"club":{"slug":"atletico-madrid","name":"Atlético Madrid","short":"ATM","api_id":530,"period":"с 2024"}},{"label":"июнь 2026","value_label":"€100 млн","value":100,"club":{"slug":"atletico-madrid","name":"Atlético Madrid","short":"ATM","api_id":530,"period":"с 2024"}}]},{"key":"anderson","name":"Эллиот Андерсон","paths":["/transfers/elliot-anderson-manchester-city/"],"points":[{"label":"2022","value_label":"€200 тыс.","value":0.2,"club":{"slug":"newcastle","name":"Newcastle United","short":"NEW","api_id":34,"period":"2021–2024"}},{"label":"2024","value_label":"€15 млн","value":15,"club":{"slug":"nottingham-forest","name":"Nottingham Forest","short":"NFO","api_id":65,"period":"с 2024"}},{"label":"2025","value_label":"€60 млн","value":60,"club":{"slug":"nottingham-forest","name":"Nottingham Forest","short":"NFO","api_id":65,"period":"с 2024"}},{"label":"2026","value_label":"€75 млн","value":75,"club":{"slug":"nottingham-forest","name":"Nottingham Forest","short":"NFO","api_id":65,"period":"с 2024"}}]},{"key":"bernardo","name":"Бернарду Силва","paths":["/transfers/bernardo-silva-real-madrid/"],"points":[{"label":"2014","value_label":"€2,5 млн","value":2.5,"club":{"slug":"monaco","name":"AS Monaco","short":"ASM","api_id":91,"period":"2014–2017"}},{"label":"2015","value_label":"€3,5 млн","value":3.5,"club":{"slug":"monaco","name":"AS Monaco","short":"ASM","api_id":91,"period":"2014–2017"}},{"label":"2017","value_label":"€40 млн","value":40,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2017–2026"}},{"label":"2019","value_label":"€100 млн","value":100,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2017–2026"}},{"label":"апр. 2026","value_label":"€27 млн","value":27,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2017–2026"}},{"label":"июнь 2026","value_label":"€22 млн","value":22,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2026"}}]},{"key":"de-ligt","name":"Маттейс де Лигт","paths":["/transfers/matthijs-de-ligt/"],"points":[{"label":"2016/17","value_label":"€0,1 млн","value":0.1,"club":{"slug":"ajax","name":"Ajax U21","short":"AJX","api_id":194,"period":"2016–2017"}},{"label":"2019","value_label":"€75 млн","value":75,"club":{"slug":"ajax","name":"Ajax","short":"AJX","api_id":194,"period":"2016–2019"}},{"label":"2022","value_label":"€70 млн","value":70,"club":{"slug":"juventus","name":"Juventus","short":"JUV","api_id":496,"period":"2019–2022"}},{"label":"2024","value_label":"€65 млн","value":65,"club":{"slug":"bayern-munich","name":"Bayern Munich","short":"FCB","api_id":157,"period":"2022–2024"}},{"label":"2026","value_label":"€30 млн","value":30,"club":{"slug":"manchester-united","name":"Manchester United","short":"MUN","api_id":33,"period":"с 2024"}}]}];

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

    const setLogoSource = (image, candidates) => {
        let index = 0;

        const loadNext = () => {
            if (index >= candidates.length) {
                image.removeAttribute("src");
                return;
            }

            image.src = candidates[index];
            index += 1;
        };

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

        modal.hidden = false;
document.body.classList.add(
            "player-market-chart-modal-open"
        );

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

            <p class="player-market-chart__note">
                Оценочная стоимость, не сумма трансфера.
                Обновлено 26.06.2026.
            </p>
        `;

        const layer = section.querySelector(".player-market-chart__club-layer");

        player.points.forEach((item, index) => {
            const coordinate = chart.coordinates[index];
            const marker = document.createElement("span");
            const image = document.createElement("img");

            marker.className =
                "player-market-chart__club-marker";

            if (index === player.points.length - 1) {
                marker.classList.add(
                    "player-market-chart__club-marker--last"
                );
            }



            marker.dataset.clubSlug = item.club.slug;

            marker.style.left =
                `${(coordinate.x / 320) * 100}%`;

            marker.style.top =
                `${(coordinate.y / 150) * 100}%`;

            marker.title =
                `${item.club.name} · ${item.label} · ${item.value_label}`;

            image.className =
                "player-market-chart__club-logo";

            image.alt = `Логотип ${item.club.name}`;
            image.loading = "lazy";

            image.addEventListener(
                "load",
                () => normalizeClubLogo(image)
            );

            setLogoSource(
                image,
                logoCandidates(item.club)
            );

            marker.appendChild(image);
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

function promyachikSkipKonate279(node) {
    if (!node) return false;

    var chart = null;

    if (node.matches && node.matches(".player-market-chart")) {
        chart = node;
    } else if (node.closest) {
        chart = node.closest(".player-market-chart");
    }

    if (!chart) return false;

    return chart.getAttribute("data-player-id") === "1145" ||
        chart.getAttribute("data-market-chart-key") === "konate" ||
        chart.classList.contains("player-market-chart--konate-hide-bottom-white-45") ||
        chart.classList.contains("promyachik-konate-prices-under-logos-031") ||
        /konat/i.test(chart.getAttribute("data-player") || "");
}

(function () {
  if (window.__promyachikAlignMarketPrices279Ready) {
    return;
  }
  window.__promyachikAlignMarketPrices279Ready = true;

  const CHART_SELECTOR = ".player-market-chart";
  const ROW_SELECTOR = ".player-market-chart__points";
  const ITEM_SELECTOR = ".player-market-chart__point";
  const DOT_SELECTOR = ".player-market-chart__dot";
  const CLUB_MARKER_SELECTOR = ".player-market-chart__club-marker";

  const roundPx = function (value) {
    return Math.round(value * 100) / 100;
  };

  const getElementCenterX = function (element) {
    const rect = element.getBoundingClientRect();
    return rect.left + rect.width / 2;
  };

  const getTargetCenters = function (chart) {
    const dots = Array.from(chart.querySelectorAll(DOT_SELECTOR));
    if (dots.length) {
      return dots.map(getElementCenterX);
    }

    const clubMarkers = Array.from(chart.querySelectorAll(CLUB_MARKER_SELECTOR));
    if (clubMarkers.length) {
      return clubMarkers.map(getElementCenterX);
    }

    return [];
  };

  const clearAlignment = function (row) {
    const items = Array.from(row.querySelectorAll(ITEM_SELECTOR));
    row.classList.remove("promyachik-price-align-279");
    row.style.removeProperty("position");
    row.style.removeProperty("display");
    row.style.removeProperty("height");
    row.style.removeProperty("min-height");

    items.forEach(function (item) {
        if (promyachikSkipKonate279(item)) return;
      item.classList.remove("promyachik-price-align-item-279");
      item.style.removeProperty("position");
      item.style.removeProperty("left");
      item.style.removeProperty("top");
      item.style.removeProperty("transform");
      item.style.removeProperty("width");
      item.style.removeProperty("max-width");
      item.style.removeProperty("text-align");
    });
  };

  const alignChart = function (chart) {
    const row = chart.querySelector(ROW_SELECTOR);
    if (!row) {
      return;
    }

    const items = Array.from(row.querySelectorAll(ITEM_SELECTOR));
    if (!items.length) {
      return;
    }

    const centers = getTargetCenters(chart);
    if (!centers.length) {
      clearAlignment(row);
      return;
    }

    clearAlignment(row);

    const rowRect = row.getBoundingClientRect();
    const currentHeights = items.map(function (item) {
      return item.getBoundingClientRect().height || 0;
    });
    const rowHeight = Math.max(rowRect.height || 0, currentHeights.reduce(function (max, value) {
      return Math.max(max, value);
    }, 0), 20);

    row.classList.add("promyachik-price-align-279");
    row.style.position = "relative";
    row.style.display = "block";
    row.style.minHeight = Math.ceil(rowHeight) + "px";
    row.style.height = Math.ceil(rowHeight) + "px";

    items.forEach(function (item, index) {
        if (promyachikSkipKonate279(item)) return;
      const center = centers[Math.min(index, centers.length - 1)];
      const x = roundPx(center - rowRect.left);
      item.classList.add("promyachik-price-align-item-279");
      item.style.position = "absolute";
      item.style.left = x + "px";
      item.style.top = "0";
      item.style.transform = "translateX(-50%)";
      item.style.width = "max-content";
      item.style.maxWidth = "78px";
      item.style.textAlign = "center";
    });
  };

  const alignAllCharts = function () {
    Array.from(document.querySelectorAll(CHART_SELECTOR)).forEach(alignChart);
  };

  let timer = null;
  const scheduleAlign = function () {
    if (timer) {
      window.clearTimeout(timer);
    }
    window.requestAnimationFrame(function () {
      alignAllCharts();
      timer = window.setTimeout(alignAllCharts, 120);
    });
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











/* PROMYACHIK 031 KONATE PRICES UNDER CLUB LOGOS START */
(function () {
    var PATH_RE = /ibrahima-konate-real-madrid/i;
    var GOLD = '#f5c741';

    function isKonatePage() {
        return window.location && PATH_RE.test(window.location.pathname || '');
    }

    function centerX(rect) {
        return rect.left + rect.width / 2;
    }

    function visibleRect(el) {
        if (!el || !el.getBoundingClientRect) return null;

        var r = el.getBoundingClientRect();

        if (!r || r.width < 8 || r.height < 8) return null;

        return r;
    }

    function sortByX(elements) {
        return elements
            .map(function (el) {
                return { el: el, rect: visibleRect(el) };
            })
            .filter(function (x) {
                return x.rect;
            })
            .sort(function (a, b) {
                return centerX(a.rect) - centerX(b.rect);
            });
    }

    function alignChart(chart) {
        if (!chart) return;

        var isKonateChart =
            chart.getAttribute('data-player-id') === '1145' ||
            chart.getAttribute('data-market-chart-key') === 'konate' ||
            chart.classList.contains('player-market-chart--konate-hide-bottom-white-45') ||
            /konat/i.test(chart.getAttribute('data-player') || '');

        if (!isKonateChart) return;

        var canvas = chart.querySelector('.player-market-chart__canvas');
        var row = chart.querySelector('.player-market-chart__points');
        var points = row ? Array.prototype.slice.call(row.querySelectorAll('.player-market-chart__point')) : [];

        if (!canvas || !row || !points.length) return;

        var chartRect = chart.getBoundingClientRect();

        var logos = sortByX(Array.prototype.slice.call(
            canvas.querySelectorAll('img, image, .player-market-chart__club-logo, .player-market-chart__club img')
        ));

        var dots = sortByX(Array.prototype.slice.call(
            canvas.querySelectorAll('.player-market-chart__dot, circle.player-market-chart__dot, svg circle')
        ));

        chart.classList.add('promyachik-konate-prices-under-logos-031');

        chart.style.setProperty('position', 'relative', 'important');

        row.style.setProperty('position', 'absolute', 'important');
        row.style.setProperty('left', '0', 'important');
        row.style.setProperty('top', '0', 'important');
        row.style.setProperty('right', '0', 'important');
        row.style.setProperty('bottom', '0', 'important');
        row.style.setProperty('display', 'block', 'important');
        row.style.setProperty('width', '100%', 'important');
        row.style.setProperty('height', '100%', 'important');
        row.style.setProperty('margin', '0', 'important');
        row.style.setProperty('padding', '0', 'important');
        row.style.setProperty('pointer-events', 'none', 'important');
        row.style.setProperty('z-index', '80', 'important');

        points.forEach(function (point, index) {
            var strong = point.querySelector('strong');
            var small = point.querySelector('small');

            if (!strong || !strong.textContent.trim()) return;

            var logo = logos[index] || null;
            var dot = dots[index] || null;

            var xRect = dot ? dot.rect : (logo ? logo.rect : null);
            var yRect = dot ? dot.rect : (logo ? logo.rect : null);

            if (!xRect || !yRect) return;

            var left = centerX(xRect) - chartRect.left;

            /*
              Цена должна стоять под точкой графика (под кружком),
              а не под логотипом.
            */
            var top = yRect.bottom - chartRect.top + 8;

            if (left < 34) left = 20;
            if (left > chartRect.width - 34) left = chartRect.width - 20;

            var transform = 'translateX(-50%)';

            if (left <= 22) {
                transform = 'translateX(0)';
            } else if (left >= chartRect.width - 22) {
                transform = 'translateX(-100%)';
            }

            point.style.setProperty('position', 'absolute', 'important');
            point.style.setProperty('left', left + 'px', 'important');
            point.style.setProperty('top', top + 'px', 'important');
            point.style.setProperty('right', 'auto', 'important');
            point.style.setProperty('bottom', 'auto', 'important');
            point.style.setProperty('transform', transform, 'important');
            point.style.setProperty('display', 'block', 'important');
            point.style.setProperty('visibility', 'visible', 'important');
            point.style.setProperty('opacity', '1', 'important');
            point.style.setProperty('width', 'max-content', 'important');
            point.style.setProperty('min-width', '0', 'important');
            point.style.setProperty('margin', '0', 'important');
            point.style.setProperty('padding', '0', 'important');
            point.style.setProperty('pointer-events', 'none', 'important');
            point.style.setProperty('z-index', '90', 'important');
            point.style.setProperty('text-align', 'center', 'important');

            if (small) {
                small.style.setProperty('display', 'none', 'important');
            }

            strong.style.setProperty('display', 'block', 'important');
            strong.style.setProperty('color', GOLD, 'important');
            strong.style.setProperty('-webkit-text-fill-color', GOLD, 'important');
            strong.style.setProperty('font-weight', '900', 'important');
            strong.style.setProperty('white-space', 'nowrap', 'important');
            strong.style.setProperty('text-shadow', '0 0 10px rgba(245,199,65,.45), 0 2px 8px rgba(0,0,0,.9)', 'important');
        });
    }

    function applyAll() {
        if (!isKonatePage()) return;

        Array.prototype.slice.call(document.querySelectorAll('.player-market-chart')).forEach(alignChart);
    }

    function schedule() {
        if (!isKonatePage()) return;

        window.requestAnimationFrame(applyAll);
        [0, 80, 180, 350, 700, 1200, 2000].forEach(function (delay) {
            window.setTimeout(applyAll, delay);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', schedule);
    } else {
        schedule();
    }

    window.addEventListener('load', schedule);
    window.addEventListener('resize', schedule);

    document.addEventListener('click', function () {
        schedule();
    }, true);

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' || event.key === 'Enter' || event.key === ' ') {
            schedule();
        }
    }, true);
}());
/* PROMYACHIK 031 KONATE PRICES UNDER CLUB LOGOS END */




