(() => {
    "use strict";

    const VERSION = "28-full-chart-zoom";
    window.__PFMarketChartVersion = VERSION;

    const PLAYERS = [{"key":"mbappe","name":"Килиан Мбаппе","paths":["/transfers/kylian-mbappe-real-madrid/"],"points":[{"label":"2017","value_label":"€35 млн","value":35,"club":{"slug":"monaco","name":"AS Monaco","short":"ASM","api_id":91,"period":"2015–2017"}},{"label":"2018","value_label":"€120 млн","value":120,"club":{"slug":"psg","name":"Paris Saint-Germain","short":"PSG","api_id":85,"period":"2017–2024"}},{"label":"2025","value_label":"€200 млн","value":200,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2024"}},{"label":"2026","value_label":"€180 млн","value":180,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2024"}}]},{"key":"wirtz","name":"Флориан Вирц","paths":["/transfers/florian-wirtz-liverpool/"],"points":[{"label":"2023","value_label":"€100 млн","value":100,"club":{"slug":"bayer-leverkusen","name":"Bayer Leverkusen","short":"B04","api_id":168,"period":"2020–2025"}},{"label":"июнь 2025","value_label":"€140 млн","value":140,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"с 2025"}},{"label":"дек. 2025","value_label":"€110 млн","value":110,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"с 2025"}},{"label":"2026","value_label":"€100 млн","value":100,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"с 2025"}}]},{"key":"konate","name":"Ибраима Конате","paths":["/transfers/ibrahima-konate-real-madrid/"],"points":[{"label":"2017","value_label":"€300 тыс.","value":0.3,"club":{"slug":"rb-leipzig","name":"RB Leipzig","short":"RBL","api_id":173,"period":"2017–2021"}},{"label":"2021","value_label":"€35 млн","value":35,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"2021–2026"}},{"label":"2025","value_label":"€60 млн","value":60,"club":{"slug":"liverpool","name":"Liverpool","short":"LFC","api_id":40,"period":"2021–2026"}},{"label":"2026","value_label":"€45 млн","value":45,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2026"}}]},{"key":"cucurella","name":"Марк Кукурелья","paths":["/transfers/marc-cucurella-real-madrid/"],"points":[{"label":"2018","value_label":"€5 млн","value":5,"club":{"slug":"barcelona","name":"Barcelona","short":"FCB","api_id":529,"period":"до 2019"}},{"label":"2019","value_label":"€10 млн","value":10,"club":{"slug":"getafe","name":"Getafe","short":"GET","api_id":546,"period":"2019–2021"}},{"label":"2020","value_label":"€18 млн","value":18,"club":{"slug":"getafe","name":"Getafe","short":"GET","api_id":546,"period":"2019–2021"}},{"label":"2021","value_label":"€20 млн","value":20,"club":{"slug":"brighton","name":"Brighton & Hove Albion","short":"BHA","api_id":51,"period":"2021–2022"}},{"label":"2026","value_label":"€50 млн","value":50,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2026"}}]},{"key":"dumfries","name":"Дензел Дюмфрис","paths":["/transfers/denzel-dumfries-real-madrid/"],"points":[{"label":"2015","value_label":"€50 тыс.","value":0.05,"club":{"slug":"sparta-rotterdam","name":"Sparta Rotterdam","short":"SPA","api_id":null,"period":"2014–2017"}},{"label":"2017","value_label":"€1 млн","value":1,"club":{"slug":"heerenveen","name":"SC Heerenveen","short":"HEE","api_id":null,"period":"2017–2018"}},{"label":"2018","value_label":"€4 млн","value":4,"club":{"slug":"psv","name":"PSV Eindhoven","short":"PSV","api_id":197,"period":"2018–2021"}},{"label":"2021","value_label":"€16 млн","value":16,"club":{"slug":"inter","name":"Inter","short":"INT","api_id":505,"period":"с 2021"}},{"label":"2025","value_label":"€35 млн","value":35,"club":{"slug":"inter","name":"Inter","short":"INT","api_id":505,"period":"с 2021"}},{"label":"2026","value_label":"€25 млн","value":25,"club":{"slug":"inter","name":"Inter","short":"INT","api_id":505,"period":"с 2021"}}]},{"key":"alvarez","name":"Хулиан Альварес","paths":["/transfers/julian-alvarez-barcelona/"],"points":[{"label":"янв. 2022","value_label":"€20 млн","value":20,"club":{"slug":"river-plate","name":"River Plate","short":"CARP","api_id":null,"period":"2018–2022"}},{"label":"июль 2022","value_label":"€23 млн","value":23,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2022–2024"}},{"label":"2023","value_label":"€90 млн","value":90,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2022–2024"}},{"label":"май 2026","value_label":"€90 млн","value":90,"club":{"slug":"atletico-madrid","name":"Atlético Madrid","short":"ATM","api_id":530,"period":"с 2024"}},{"label":"июнь 2026","value_label":"€100 млн","value":100,"club":{"slug":"atletico-madrid","name":"Atlético Madrid","short":"ATM","api_id":530,"period":"с 2024"}}]},{"key":"anderson","name":"Эллиот Андерсон","paths":["/transfers/elliot-anderson-manchester-city/"],"points":[{"label":"2022","value_label":"€200 тыс.","value":0.2,"club":{"slug":"newcastle","name":"Newcastle United","short":"NEW","api_id":34,"period":"2021–2024"}},{"label":"2024","value_label":"€15 млн","value":15,"club":{"slug":"nottingham-forest","name":"Nottingham Forest","short":"NFO","api_id":65,"period":"с 2024"}},{"label":"2025","value_label":"€60 млн","value":60,"club":{"slug":"nottingham-forest","name":"Nottingham Forest","short":"NFO","api_id":65,"period":"с 2024"}},{"label":"2026","value_label":"€75 млн","value":75,"club":{"slug":"nottingham-forest","name":"Nottingham Forest","short":"NFO","api_id":65,"period":"с 2024"}}]},{"key":"bernardo","name":"Бернарду Силва","paths":["/transfers/bernardo-silva-real-madrid/"],"points":[{"label":"2014","value_label":"€2,5 млн","value":2.5,"club":{"slug":"monaco","name":"AS Monaco","short":"ASM","api_id":91,"period":"2014–2017"}},{"label":"2015","value_label":"€3,5 млн","value":3.5,"club":{"slug":"monaco","name":"AS Monaco","short":"ASM","api_id":91,"period":"2014–2017"}},{"label":"2017","value_label":"€40 млн","value":40,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2017–2026"}},{"label":"2019","value_label":"€100 млн","value":100,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2017–2026"}},{"label":"апр. 2026","value_label":"€27 млн","value":27,"club":{"slug":"manchester-city","name":"Manchester City","short":"MCI","api_id":50,"period":"2017–2026"}},{"label":"июнь 2026","value_label":"€22 млн","value":22,"club":{"slug":"real-madrid","name":"Real Madrid","short":"RMA","api_id":541,"period":"с 2026"}}]}];

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

        const last = coordinates[coordinates.length - 1];
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

    const createChart = () => {
        const chart = geometry(player.points);
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
                <strong>${escapeHTML(item.value_label)}</strong>
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

            marker.style.left =
                `${(coordinate.x / 320) * 100}%`;

            marker.style.top =
                `${((coordinate.y - 34) / 150) * 100}%`;

            marker.title =
                `${item.club.name} · ${item.label} · ${item.value_label}`;

            image.className =
                "player-market-chart__club-logo";

            image.alt = `Логотип ${item.club.name}`;
            image.loading = "lazy";

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
