(() => {
  "use strict";

  // PF491A: было 5. После удаления раздела «Новости» блок трансферов
  // на главной смотрелся пустым при своей высоте.
  const COLLAPSED_ROWS = 7;
  const LEAGUE_BUTTON_SELECTOR = ".pf-league-selector__item";
  const CLUB_ID_TO_LEAGUES = {"157":["78"],"165":["78"],"168":["78"],"211":["94"],"212":["94"],"217":["94"],"228":["94"],"33":["39"],"34":["39"],"40":["39"],"42":["39"],"47":["39"],"489":["135"],"49":["39"],"492":["135"],"496":["135"],"50":["39"],"505":["135"],"529":["140"],"530":["140"],"541":["140"],"549":["203"],"555":["235"],"558":["235"],"560":["235"],"585":["235"],"596":["235"],"597":["235"],"611":["203"],"645":["203"],"81":["61"],"85":["61"],"91":["61"],"998":["203"]};
  const CLUB_NAME_TO_LEAGUES = {"ac milan":["135"],"arsenal":["39"],"atletico madrid":["140"],"barcelona":["140"],"bayer leverkusen":["78"],"bayern munich":["78"],"benfica":["94"],"besiktas":["203"],"borussia dortmund":["78"],"chelsea":["39"],"cska moscow":["235"],"dynamo moscow":["235"],"fc porto":["94"],"fenerbahce":["203"],"galatasaray":["203"],"inter":["135"],"juventus":["135"],"krasnodar":["235"],"liverpool":["39"],"lokomotiv moscow":["235"],"manchester city":["39"],"manchester united":["39"],"marseille":["61"],"monaco":["61"],"napoli":["135"],"newcastle":["39"],"paris saint germain":["61"],"porto":["94"],"real madrid":["140"],"sc braga":["94"],"spartak moscow":["235"],"sporting cp":["94"],"tottenham":["39"],"trabzonspor":["203"],"zenit":["235"]};

  function normalizeClubName(value) {
    return String(value || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-zа-яё0-9]+/gi, " ")
      .trim();
  }

  function extractClubIdFromImage(image) {
    const src = String(image?.getAttribute("src") || "");
    const match = src.match(/\/clubs\/api\/(\d+)\.png(?:[?#].*)?$/i);
    return match ? match[1] : "";
  }

  function addMappedLeagues(target, clubId, clubName) {
    const id = String(clubId || "").trim();
    const name = normalizeClubName(clubName);

    (CLUB_ID_TO_LEAGUES[id] || []).forEach((leagueId) => {
      target.add(String(leagueId));
    });

    (CLUB_NAME_TO_LEAGUES[name] || []).forEach((leagueId) => {
      target.add(String(leagueId));
    });
  }

  function transferLeagueIds(row) {
    const result = new Set();
    const images = Array.from(
      row.querySelectorAll("img.pf-club-logo")
    );

    images.forEach((image) => {
      addMappedLeagues(
        result,
        extractClubIdFromImage(image),
        image.getAttribute("alt")
      );
    });

    if (!images.length) {
      const cells = Array.from(
        row.querySelectorAll("td.is-center")
      );

      cells.forEach((cell) => {
        const text = cell.textContent.trim();

        if (text && text !== "→") {
          addMappedLeagues(result, "", text);
        }
      });
    }

    return result;
  }

  function rumorLeagueIds(item) {
    const result = new Set();
    const route = item.querySelector(".pf-home-rumors-route");

    if (!route) {
      return result;
    }

    const names = Array.from(route.querySelectorAll("span"))
      .filter((span) => !span.classList.contains("pf-route-arrow"))
      .map((span) => span.textContent.trim())
      .filter(Boolean);

    names.forEach((name) => {
      addMappedLeagues(result, "", name);
    });

    return result;
  }

  function matchesLeague(leagueIds, selectedLeagueId) {
    return (
      !selectedLeagueId ||
      leagueIds.has(String(selectedLeagueId))
    );
  }

  function ensureEmptyState(root, kind) {
    const attribute = `data-pf-${kind}-filter-empty`;
    let empty = root.querySelector(`[${attribute}]`);

    if (!empty) {
      empty = document.createElement("div");
      empty.className = "pf-home-filter-empty";
      empty.setAttribute(attribute, "");
      empty.hidden = true;
      empty.textContent =
        kind === "transfer"
          ? "По этой лиге пока нет трансферов."
          : "По этой лиге пока нет слухов.";

      const footer = root.querySelector(".pf-home-panel__footer");
      root.insertBefore(empty, footer || null);
    }

    return empty;
  }

  function initTransferPanel(root) {
    const viewport = root.querySelector("[data-pf-transfer-expand]");
    const table = viewport?.querySelector(".pf-home-transfers-table");
    const toggle = root.querySelector("[data-pf-transfer-toggle]");
    const empty = ensureEmptyState(root, "transfer");

    if (!viewport || !table || !toggle) {
      return null;
    }

    const rows = Array.from(
      table.querySelectorAll("tbody > tr")
    );

    const rowLeagueMap = new Map(
      rows.map((row) => [row, transferLeagueIds(row)])
    );

    let expanded = false;
    let resizeFrame = 0;

    function visibleRows() {
      return rows.filter((row) => !row.hidden);
    }

    function fullHeight() {
      return Math.ceil(table.getBoundingClientRect().height);
    }

    function collapsedHeight(currentRows = visibleRows()) {
      if (!currentRows.length) {
        return 0;
      }

      if (currentRows.length <= COLLAPSED_ROWS) {
        return fullHeight();
      }

      const finalRow = currentRows[COLLAPSED_ROWS - 1];
      const viewportRect = viewport.getBoundingClientRect();
      const rowRect = finalRow.getBoundingClientRect();

      return Math.max(
        0,
        Math.ceil(rowRect.bottom - viewportRect.top)
      );
    }

    function setHeight(value) {
      viewport.style.height = `${Math.max(0, value)}px`;
    }

    function resetToggle() {
      toggle.setAttribute("aria-expanded", "false");
      toggle.textContent = "Развернуть";
    }

    function syncWithoutAnimation() {
      const currentRows = visibleRows();

      viewport.classList.add("is-measuring");
      viewport.style.height = "auto";
      void viewport.offsetHeight;

      empty.hidden = currentRows.length !== 0;
      toggle.hidden = currentRows.length <= COLLAPSED_ROWS;

      if (!currentRows.length) {
        setHeight(0);
      } else if (
        expanded ||
        currentRows.length <= COLLAPSED_ROWS
      ) {
        viewport.style.height = "auto";
      } else {
        setHeight(collapsedHeight(currentRows));
      }

      window.requestAnimationFrame(() => {
        viewport.classList.remove("is-measuring");
      });
    }

    const overview = root.closest(".pf-home-market-overview");

    function markExpanded(state) {
      if (overview) {
        overview.classList.toggle("pf494a-transfers-expanded", state);
      }
    }

    function expand() {
      const currentRows = visibleRows();

      if (currentRows.length <= COLLAPSED_ROWS) {
        syncWithoutAnimation();
        return;
      }

      expanded = true;
      markExpanded(true);
      toggle.hidden = false;
      toggle.setAttribute("aria-expanded", "true");
      toggle.textContent = "Свернуть";

      setHeight(collapsedHeight(currentRows));
      void viewport.offsetHeight;
      viewport.classList.add("is-expanded");
      setHeight(fullHeight());
    }

    function collapse() {
      const currentRows = visibleRows();

      expanded = false;
      markExpanded(false);
      resetToggle();

      if (currentRows.length <= COLLAPSED_ROWS) {
        syncWithoutAnimation();
        return;
      }

      setHeight(fullHeight());
      void viewport.offsetHeight;
      viewport.classList.remove("is-expanded");
      setHeight(collapsedHeight(currentRows));
    }

    function applyLeague(leagueId) {
      rows.forEach((row) => {
        row.hidden = !matchesLeague(
          rowLeagueMap.get(row) || new Set(),
          leagueId
        );
      });

      expanded = false;
      markExpanded(false);
      viewport.classList.remove("is-expanded");
      resetToggle();
      syncWithoutAnimation();
    }

    toggle.addEventListener("click", () => {
      expanded ? collapse() : expand();
    });

    viewport.addEventListener("transitionend", (event) => {
      if (event.propertyName === "height" && expanded) {
        viewport.style.height = "auto";
      }
    });

    window.addEventListener("resize", () => {
      window.cancelAnimationFrame(resizeFrame);
      resizeFrame = window.requestAnimationFrame(
        syncWithoutAnimation
      );
    });

    table.querySelectorAll("img").forEach((image) => {
      if (!image.complete) {
        image.addEventListener(
          "load",
          () => {
            rowLeagueMap.set(
              image.closest("tr"),
              transferLeagueIds(image.closest("tr"))
            );
            syncWithoutAnimation();
          },
          { once: true }
        );
      }
    });

    // PF492A: высота свёрнутого блока вычислялась один раз и устаревала.
    // Строки меняют высоту позже: догружаются логотипы клубов, подключается
    // шрифт, длинные имена переносятся на вторую строку. Из-за этого под
    // последней строкой выглядывал кусок следующей.
    // ResizeObserver пересчитывает высоту при любом изменении размера таблицы.
    if (typeof ResizeObserver === "function") {
      let observerFrame = 0;
      const observer = new ResizeObserver(() => {
        if (expanded) {
          return;
        }
        window.cancelAnimationFrame(observerFrame);
        observerFrame = window.requestAnimationFrame(syncWithoutAnimation);
      });
      observer.observe(table);
    }

    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(() => {
        if (!expanded) {
          syncWithoutAnimation();
        }
      });
    }

    window.addEventListener("load", () => {
      if (!expanded) {
        syncWithoutAnimation();
      }
    });

    applyLeague("");
    return { applyLeague };
  }

  function initRumorPanel(root) {
    const list = root.querySelector(".pf-home-rumors-list");
    const empty = ensureEmptyState(root, "rumor");

    if (!list) {
      return null;
    }

    const items = Array.from(
      list.querySelectorAll(":scope > li")
    );

    const itemLeagueMap = new Map(
      items.map((item) => [item, rumorLeagueIds(item)])
    );

    function applyLeague(leagueId) {
      let visibleCount = 0;

      items.forEach((item) => {
        const visible = matchesLeague(
          itemLeagueMap.get(item) || new Set(),
          leagueId
        );

        item.hidden = !visible;

        if (visible) {
          visibleCount += 1;
        }
      });

      empty.hidden = visibleCount !== 0;
    }

    applyLeague("");
    return { applyLeague };
  }

  function setButtonState(activeButton) {
    document
      .querySelectorAll(LEAGUE_BUTTON_SELECTOR)
      .forEach((button) => {
        const active = button === activeButton;
        button.classList.toggle("is-active", active);
        button.setAttribute(
          "aria-pressed",
          active ? "true" : "false"
        );
      });
  }

  function init() {
    const transferControllers = Array.from(
      document.querySelectorAll(
        ".pf-home-panel--transfers"
      )
    )
      .map(initTransferPanel)
      .filter(Boolean);

    const rumorControllers = Array.from(
      document.querySelectorAll(
        ".pf-home-panel--rumors"
      )
    )
      .map(initRumorPanel)
      .filter(Boolean);

    let selectedLeagueId = "";

    function applyLeague(leagueId) {
      selectedLeagueId = String(leagueId || "");

      transferControllers.forEach((controller) => {
        controller.applyLeague(selectedLeagueId);
      });

      rumorControllers.forEach((controller) => {
        controller.applyLeague(selectedLeagueId);
      });

      document.documentElement.dataset.pfSelectedLeague =
        selectedLeagueId;
    }

    document.addEventListener(
      "click",
      (event) => {
        const button = event.target.closest(
          LEAGUE_BUTTON_SELECTOR
        );

        if (!button) {
          return;
        }

        event.preventDefault();
        event.stopImmediatePropagation();

        const clickedLeagueId = String(
          button.dataset.leagueId || ""
        );

        const clearSelection =
          button.classList.contains("is-active") &&
          selectedLeagueId === clickedLeagueId;

        if (clearSelection) {
          setButtonState(null);
          applyLeague("");
          return;
        }

        setButtonState(button);
        applyLeague(clickedLeagueId);
      },
      true
    );

    applyLeague("");
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      init,
      { once: true }
    );
  } else {
    init();
  }
})();
