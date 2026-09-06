(() => {
    const normalize = (value) => (value || "").replace(/\s+/g, " ").trim();

    const getTransfersUrl = () => {
        const path = window.location.pathname;
        const prefix = path.startsWith("/promyachik/") ? "/promyachik/" : "/";
        return `${window.location.origin}${prefix}transfers/`;
    };

    const isGreenish = (value) => {
        const match = String(value || "").match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/i);
        if (!match) return false;

        const r = Number(match[1]);
        const g = Number(match[2]);
        const b = Number(match[3]);

        return g > 120 && g > r + 25 && g > b + 10;
    };

    /* PF519B: заголовки блоков главной этот скрипт не трогает.
       Он ищет по всей странице любой элемент с текстом «ТРАНСФЕРЫ» и красит
       его золотой плашкой бегущей строки, поднимаясь вверх, пока предок уже
       300 пикселей и ниже 100. Заголовок панели проходил этот фильтр всякий
       раз, когда скрипт успевал измерить его до того, как панель разошлась на
       свою ширину, — то есть по случайности, зависящей от порядка загрузки.
       PF516 переселил шрифты на свой домен, порядок изменился, и над блоком
       «Трансферы» встала золотая полоса, которой у «Слухов» нет.
       Заголовок блока и так ссылка на раздел, второй раз делать из него
       вкладку незачем. */
    const isPanelTitle = (node) =>
        !!(node.closest && node.closest(".pf-home-panel__header"));

    const findTransferTabs = () => {
        const nodes = Array.from(document.querySelectorAll("a, button, div, span"));

        return nodes
            .filter((node) => normalize(node.textContent) === "ТРАНСФЕРЫ")
            .filter((node) => !isPanelTitle(node))
            .map((label) => {
                let best = label;
                let current = label.parentElement;

                while (current && current !== document.body) {
                    const text = normalize(current.textContent);
                    const rect = current.getBoundingClientRect();

                    if (text.includes("ТРАНСФЕРЫ") && text.length <= 32 && rect.width <= 300 && rect.height <= 100) {
                        best = current;
                        current = current.parentElement;
                        continue;
                    }

                    break;
                }

                return best;
            })
            .filter((tab, index, list) => tab && list.indexOf(tab) === index);
    };

    const removeGreenDot = (tab) => {
        const candidates = Array.from(tab.querySelectorAll("*"));

        candidates.forEach((node) => {
            const rect = node.getBoundingClientRect();
            const style = window.getComputedStyle(node);
            const background = style.backgroundColor;
            const color = style.color;

            const looksLikeDot =
                rect.width > 0 &&
                rect.height > 0 &&
                rect.width <= 18 &&
                rect.height <= 18 &&
                Math.abs(rect.width - rect.height) <= 7 &&
                (isGreenish(background) || isGreenish(color));

            if (looksLikeDot) {
                node.classList.add("pf-transfer-tab-dot-hidden");
            }
        });
    };

    const setupTransferTabs = () => {
        const tabs = findTransferTabs();
        if (!tabs.length) return;

        const href = getTransfersUrl();

        tabs.forEach((tab) => {
            tab.classList.add("pf-transfer-tab-link");
            tab.setAttribute("role", "link");
            tab.setAttribute("tabindex", "0");
            tab.setAttribute("aria-label", "Открыть страницу трансферов");

            const existingAnchor = tab.matches("a") ? tab : tab.closest("a");

            if (existingAnchor) {
                existingAnchor.href = href;
                existingAnchor.classList.add("pf-transfer-tab-link");
            } else if (!tab.dataset.pfTransferTabBound) {
                tab.dataset.pfTransferTabBound = "1";

                tab.addEventListener("click", () => {
                    window.location.href = href;
                });

                tab.addEventListener("keydown", (event) => {
                    if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        window.location.href = href;
                    }
                });
            }

            removeGreenDot(tab);
        });
    };

    const boot = () => {
        setupTransferTabs();

        window.setTimeout(setupTransferTabs, 250);
        window.setTimeout(setupTransferTabs, 1000);
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
    } else {
        boot();
    }
})();
