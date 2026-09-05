/*
 * PF511A — ПЕРЕЛИСТЫВАНИЕ БЛОКОВ НА ГЛАВНОЙ
 *
 * Идея Дмитрия: если человек задержался на главной, блок работает как
 * рекламный щит — раз в минуту показывает следующую порцию материалов,
 * переворачивая строки, как страницы книги.
 *
 * Почему именно так, а не «случайные семь из шестидесяти четырёх»: при
 * случайной выборке одни и те же трансферы выпадали бы часто, а другие
 * человек не увидел бы вовсе. Здесь список проходится подряд страницами, и
 * за несколько минут показывается весь; порядок перемешивается только внутри
 * страницы, чтобы не выглядело механическим списком.
 *
 * Когда молчим:
 *   - блок развёрнут — человек читает полный список, дёргать его нельзя;
 *   - включён фильтр по лиге — он сам решает, что показывать;
 *   - вкладка не на виду — крутить анимацию в фоне незачем;
 *   - в системе просили меньше движения.
 */
(() => {
  "use strict";

  const PERIOD_MS = 60000;
  const FLIP_MS = 420;
  const STAGGER_MS = 55;

  const reduceMotion = window.matchMedia
    ? window.matchMedia("(prefers-reduced-motion: reduce)")
    : { matches: false };

  function shuffle(items) {
    const copy = items.slice();
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  function setupPanel(panel) {
    const table = panel.querySelector(".pf-home-transfers-table");
    const body = table && table.querySelector("tbody");
    if (!body) {
      return;
    }

    const order = Array.from(body.rows);
    const declared = parseInt(panel.dataset.pfCollapsedRows || "", 10);
    const pageSize = Number.isFinite(declared) && declared > 0 ? declared : 7;

    // Листать нечего, если весь список и так на виду.
    if (order.length <= pageSize) {
      return;
    }

    const toggle = panel.querySelector("[data-pf-transfer-toggle]");
    let offset = 0;
    let busy = false;

    function paused() {
      if (document.hidden || reduceMotion.matches || busy) {
        return true;
      }
      if (toggle && toggle.getAttribute("aria-expanded") === "true") {
        return true;
      }
      // Фильтр по лиге прячет часть строк — тогда выбор не наш.
      return order.some((row) => row.hidden);
    }

    function flip() {
      if (paused()) {
        return;
      }
      busy = true;

      offset = (offset + pageSize) % order.length;
      const next = [];
      for (let i = 0; i < pageSize; i += 1) {
        next.push(order[(offset + i) % order.length]);
      }

      const shown = order.slice(0, pageSize);
      shown.forEach((row, index) => {
        row.style.transition = `transform ${FLIP_MS / 2}ms ease-in, opacity ${FLIP_MS / 2}ms ease-in`;
        row.style.transformOrigin = "top center";
        window.setTimeout(() => {
          row.style.transform = "perspective(700px) rotateX(-84deg)";
          row.style.opacity = "0";
        }, index * STAGGER_MS);
      });

      const outDone = FLIP_MS / 2 + shown.length * STAGGER_MS;
      window.setTimeout(() => {
        // Порядок внутри страницы перемешиваем, чтобы не читалось как
        // механическая прокрутка одного и того же списка.
        shuffle(next).forEach((row) => body.appendChild(row));
        order.filter((row) => !next.includes(row))
          .forEach((row) => body.appendChild(row));

        next.forEach((row, index) => {
          row.style.transition = "none";
          row.style.transform = "perspective(700px) rotateX(84deg)";
          row.style.opacity = "0";
          window.setTimeout(() => {
            row.style.transition = `transform ${FLIP_MS / 2}ms ease-out, opacity ${FLIP_MS / 2}ms ease-out`;
            row.style.transform = "";
            row.style.opacity = "";
          }, 20 + index * STAGGER_MS);
        });

        window.setTimeout(() => {
          order.forEach((row) => {
            row.style.transition = "";
            row.style.transform = "";
            row.style.opacity = "";
            row.style.transformOrigin = "";
          });
          busy = false;
          // Пусть сворачивание пересчитает высоту: строки переехали.
          window.dispatchEvent(new Event("resize"));
        }, FLIP_MS + next.length * STAGGER_MS);
      }, outDone);
    }

    window.setInterval(flip, PERIOD_MS);
  }

  function boot() {
    document
      .querySelectorAll(".pf-home-panel--transfers, .pf-home-panel--rumors")
      .forEach(setupPanel);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
