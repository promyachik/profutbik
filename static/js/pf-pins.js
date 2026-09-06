/*
 * PF519A — ТОЧКИ ЗАМЕЧАНИЙ ПРЯМО НА СТРАНИЦЕ
 *
 * Идея Дмитрия: вместо того чтобы описывать словами, где и что не так
 * («в слухах там то есть, то то надо исправить»), ткнуть в само место,
 * написать в точку короткий комментарий, а когда сделано — точку удалить.
 *
 * Что точка запоминает, кроме текста. Координаты сами по себе бесполезны:
 * после первой же правки вёрстки они уедут. Поэтому точка цепляется за
 * элемент — селектор, классы, соседний текст, кусок разметки — и хранит
 * положение внутри него долей от ширины и высоты. Именно классы и решают
 * дело: `.pf-home-panel--rumors .pf-club-logo` говорит мне, какое правило
 * править, точнее любого описания словами.
 *
 * Где живут. В localStorage браузера Дмитрия. Не на сервере: сайт
 * статический, а тащить ради заметок бэкенд — несоразмерно. Переживают
 * перезагрузку, выкладку и закрытие браузера.
 *
 * Как попадают ко мне. Кнопкой «скопировать» — в буфер ложится готовый
 * текст, который остаётся вставить в чат одним сообщением. Это ручной шаг,
 * и он временный: следующим заходом заметки будут уезжать в файл через
 * локальную админку, и вставлять не придётся вовсе.
 *
 * Посетителям это не грузится: в шаблоне стоит крошечный включатель,
 * который подтягивает файл только по Ctrl+Alt+P или по ?pins=1.
 */
(() => {
  "use strict";

  if (window.__pfPins) {
    window.__pfPins.toggle();
    return;
  }

  const STORE = "pf-pins-v1";
  const GOLD = "#f1bd29";

  /* ------------------------------------------------------------------ хранение */

  const load = () => {
    try {
      const raw = JSON.parse(localStorage.getItem(STORE) || "[]");
      return Array.isArray(raw) ? raw : [];
    } catch (error) {
      return [];
    }
  };

  const save = (pins) => {
    try {
      localStorage.setItem(STORE, JSON.stringify(pins));
    } catch (error) {
      alert("Не удалось сохранить точку: в браузере кончилось место.");
    }
  };

  let pins = load();
  const here = () => location.pathname + location.search;

  /* ------------------------------------------------- к чему цепляется точка */

  /* Поднимаемся от места клика до элемента, за который не стыдно зацепиться:
     со своим id или с нашим классом pf*. Голый <span> внутри пяти обёрток
     после правки исчезнет, а `.pf-transfer-row__summary` переживёт. */
  const anchorFor = (node) => {
    let current = node;
    while (current && current !== document.body) {
      if (current.id) return current;
      const cls = typeof current.className === "string" ? current.className : "";
      if (/\bpf[\w-]*\b/.test(cls)) return current;
      current = current.parentElement;
    }
    return node && node !== document.body ? node : document.body;
  };

  const selectorFor = (element) => {
    if (!element || element === document.body) return "body";
    if (element.id) return "#" + CSS.escape(element.id);

    const parts = [];
    let current = element;
    for (let depth = 0; current && current !== document.body && depth < 4; depth += 1) {
      let part = current.tagName.toLowerCase();
      const cls = (typeof current.className === "string" ? current.className : "")
        .trim().split(/\s+/).filter(Boolean).slice(0, 3);
      if (cls.length) part += "." + cls.map((c) => CSS.escape(c)).join(".");
      const siblings = current.parentElement
        ? [...current.parentElement.children].filter((n) => n.tagName === current.tagName)
        : [];
      if (siblings.length > 1) {
        part += ":nth-of-type(" + (siblings.indexOf(current) + 1) + ")";
      }
      parts.unshift(part);
      if (current.id) {
        parts[0] = "#" + CSS.escape(current.id);
        break;
      }
      current = current.parentElement;
    }
    return parts.join(" > ");
  };

  const describe = (element) => {
    const text = (element.textContent || "").replace(/\s+/g, " ").trim();
    return {
      selector: selectorFor(element),
      classes: (typeof element.className === "string" ? element.className : "").trim(),
      label: text.slice(0, 90),
      html: (element.outerHTML || "").replace(/\s+/g, " ").slice(0, 320),
    };
  };

  /* ------------------------------------------------------------------ разметка */

  const root = document.createElement("div");
  root.id = "pf-pins-root";
  root.innerHTML = `
<style>
  #pf-pins-root{position:absolute;inset:0 auto auto 0;width:0;height:0;z-index:2147483000;
    font:400 13px/1.45 "Segoe UI",-apple-system,Arial,sans-serif;color:#eef3f8}
  #pf-pins-root *{box-sizing:border-box}
  .pfp-dot{position:absolute;width:24px;height:24px;margin:-12px 0 0 -12px;border-radius:50%;
    background:${GOLD};color:#12161c;font-weight:700;font-size:12px;display:grid;place-items:center;
    cursor:pointer;box-shadow:0 0 0 3px rgba(241,189,41,.28),0 4px 14px rgba(0,0,0,.5);
    pointer-events:auto;transition:transform .12s ease}
  .pfp-dot:hover{transform:scale(1.15)}
  .pfp-dot.is-lost{background:#7d8794;color:#fff}
  .pfp-card{position:absolute;width:290px;margin:16px 0 0 -14px;padding:12px;border-radius:12px;
    background:#151b23;border:1px solid rgba(241,189,41,.4);box-shadow:0 18px 46px rgba(0,0,0,.62);
    pointer-events:auto}
  .pfp-card textarea{width:100%;min-height:74px;resize:vertical;padding:8px;border-radius:8px;
    border:1px solid #2b3542;background:#0e1319;color:#eef3f8;font:inherit}
  .pfp-where{font-size:11px;color:#8d99a8;margin:0 0 7px;word-break:break-all}
  .pfp-tags{display:flex;flex-wrap:wrap;gap:5px;margin:8px 0}
  .pfp-tags button{padding:3px 8px;border-radius:99px;border:1px solid #2b3542;background:#0e1319;
    color:#b9c4d1;font:inherit;font-size:11px;cursor:pointer}
  .pfp-tags button:hover{border-color:${GOLD};color:${GOLD}}
  .pfp-row{display:flex;gap:7px;margin-top:9px}
  .pfp-row button{flex:1;padding:7px;border-radius:8px;border:0;font:inherit;font-weight:700;cursor:pointer}
  .pfp-ok{background:${GOLD};color:#12161c}
  .pfp-del{background:#2b3542;color:#e6707a}
  .pfp-bar{position:fixed;right:16px;bottom:16px;display:flex;flex-direction:column;gap:7px;
    padding:11px;border-radius:13px;background:#151b23e8;border:1px solid #2b3542;
    box-shadow:0 18px 46px rgba(0,0,0,.6);pointer-events:auto;backdrop-filter:blur(6px)}
  .pfp-bar button{padding:8px 13px;border-radius:9px;border:1px solid #2b3542;background:#0e1319;
    color:#eef3f8;font:inherit;cursor:pointer;text-align:left;white-space:nowrap}
  .pfp-bar button:hover{border-color:${GOLD}}
  .pfp-bar .pfp-primary{background:${GOLD};color:#12161c;font-weight:700;border-color:${GOLD}}
  .pfp-bar .pfp-title{font-weight:700;color:${GOLD};font-size:11px;letter-spacing:.06em;
    text-transform:uppercase;padding:0 2px 2px}
  .pfp-hint{position:fixed;left:50%;top:14px;transform:translateX(-50%);padding:9px 16px;
    border-radius:99px;background:${GOLD};color:#12161c;font-weight:700;pointer-events:none}
  .pfp-list{position:fixed;right:16px;bottom:16px;width:340px;max-height:74vh;overflow:auto;
    padding:13px;border-radius:13px;background:#151b23f2;border:1px solid #2b3542;
    box-shadow:0 18px 46px rgba(0,0,0,.66);pointer-events:auto}
  .pfp-item{padding:9px 0;border-bottom:1px solid #222b36;cursor:pointer}
  .pfp-item:last-child{border-bottom:0}
  .pfp-item b{color:${GOLD}}
  .pfp-item span{color:#8d99a8;font-size:11px;display:block;margin-top:2px;word-break:break-all}
  html.pfp-placing,html.pfp-placing *{cursor:crosshair!important}
</style>`;
  document.body.appendChild(root);

  const layer = document.createElement("div");
  root.appendChild(layer);

  let placing = false;
  let openCard = null;

  /* ---------------------------------------------------------------- отрисовка */

  const paint = () => {
    layer.querySelectorAll(".pfp-dot").forEach((n) => n.remove());
    const mine = pins.filter((p) => p.page === here());

    mine.forEach((pin) => {
      const target = (() => {
        try {
          return document.querySelector(pin.selector);
        } catch (error) {
          return null;
        }
      })();

      const dot = document.createElement("div");
      dot.className = "pfp-dot" + (target ? "" : " is-lost");
      dot.textContent = pins.indexOf(pin) + 1;
      dot.title = pin.note || "без комментария";

      if (target) {
        const box = target.getBoundingClientRect();
        dot.style.left = (box.left + window.scrollX + box.width * pin.rx) + "px";
        dot.style.top = (box.top + window.scrollY + box.height * pin.ry) + "px";
      } else {
        // Элемент исчез после правки — точку не теряем, ставим на прежнее
        // место страницы и красим серым: видно, что якорь отвалился.
        dot.style.left = pin.px + "px";
        dot.style.top = pin.py + "px";
      }

      dot.addEventListener("click", (event) => {
        event.stopPropagation();
        card(pin, dot);
      });
      layer.appendChild(dot);
    });

    const counter = root.querySelector("[data-pfp-count]");
    if (counter) counter.textContent = "Список (" + pins.length + ")";
  };

  /* ------------------------------------------------------------- карточка точки */

  const TAGS = ["убрать", "не влезает", "сдвинуть", "шрифт", "цвет",
                "размер", "на телефоне", "текст"];

  function card(pin, dot) {
    if (openCard) openCard.remove();
    const box = document.createElement("div");
    box.className = "pfp-card";
    box.style.left = dot.style.left;
    box.style.top = dot.style.top;

    const where = document.createElement("p");
    where.className = "pfp-where";
    where.textContent = pin.label ? "«" + pin.label + "»" : pin.selector;

    const area = document.createElement("textarea");
    area.value = pin.note || "";
    area.placeholder = "что тут поправить";

    const tags = document.createElement("div");
    tags.className = "pfp-tags";
    TAGS.forEach((tag) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = tag;
      button.addEventListener("click", () => {
        area.value = (area.value ? area.value.trim() + " " : "") + tag;
        area.focus();
      });
      tags.appendChild(button);
    });

    const row = document.createElement("div");
    row.className = "pfp-row";
    const ok = document.createElement("button");
    ok.className = "pfp-ok";
    ok.textContent = "Сохранить";
    ok.addEventListener("click", () => {
      pin.note = area.value.trim();
      save(pins);
      box.remove();
      openCard = null;
      paint();
    });
    const del = document.createElement("button");
    del.className = "pfp-del";
    del.textContent = "Удалить";
    del.addEventListener("click", () => {
      pins = pins.filter((p) => p !== pin);
      save(pins);
      box.remove();
      openCard = null;
      paint();
    });
    row.append(ok, del);

    box.append(where, area, tags, row);
    layer.appendChild(box);
    openCard = box;
    area.focus();

    // Ctrl+Enter — сохранить, не тянясь к мыши.
    area.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) ok.click();
      if (event.key === "Escape") { box.remove(); openCard = null; }
    });
  }

  /* -------------------------------------------------------------- постановка */

  const hint = (text) => {
    const node = document.createElement("div");
    node.className = "pfp-hint";
    node.textContent = text;
    root.appendChild(node);
    setTimeout(() => node.remove(), 2200);
  };

  const place = (event) => {
    if (!placing) return;
    if (root.contains(event.target)) return;
    event.preventDefault();
    event.stopPropagation();

    const target = anchorFor(document.elementFromPoint(event.clientX, event.clientY));
    const box = target.getBoundingClientRect();
    const info = describe(target);

    const pin = Object.assign({
      id: Date.now().toString(36),
      page: here(),
      title: document.title,
      // Доли внутри элемента: вёрстка поедет — точка останется на месте.
      rx: box.width ? (event.clientX - box.left) / box.width : 0.5,
      ry: box.height ? (event.clientY - box.top) / box.height : 0.5,
      px: event.clientX + window.scrollX,
      py: event.clientY + window.scrollY,
      viewport: window.innerWidth,
      note: "",
      created: new Date().toISOString(),
    }, info);

    pins.push(pin);
    save(pins);
    placing = false;
    document.documentElement.classList.remove("pfp-placing");
    paint();
    const dot = layer.querySelectorAll(".pfp-dot");
    card(pin, dot[dot.length - 1]);
  };

  document.addEventListener("click", place, true);

  /* ------------------------------------------------------------------ выгрузка */

  const asText = () => {
    if (!pins.length) return "Точек нет.";
    const lines = ["ТОЧКИ ДЛЯ ПРАВКИ — " + pins.length + " шт."];
    pins.forEach((pin, index) => {
      lines.push("");
      lines.push((index + 1) + ". " + location.origin + pin.page
                 + "   (окно " + pin.viewport + "px)");
      lines.push("   куда: " + pin.selector);
      if (pin.classes) lines.push("   классы: " + pin.classes);
      if (pin.label) lines.push("   рядом текст: «" + pin.label + "»");
      lines.push("   что сделать: " + (pin.note || "— комментарий не написан —"));
    });
    return lines.join("\n");
  };

  const copy = async () => {
    const text = asText();
    try {
      await navigator.clipboard.writeText(text);
      hint("Скопировано — вставляй в чат");
    } catch (error) {
      // Буфер может быть закрыт политикой страницы: показываем текст,
      // чтобы выделить руками, а не терять работу.
      const area = document.createElement("textarea");
      area.value = text;
      area.style.cssText = "position:fixed;inset:8% 8%;z-index:2147483001;"
        + "background:#0e1319;color:#eef3f8;padding:14px;font:12px monospace";
      document.body.appendChild(area);
      area.select();
      area.addEventListener("blur", () => area.remove());
    }
  };

  /* --------------------------------------------------------------------- список */

  let listBox = null;
  const list = () => {
    if (listBox) { listBox.remove(); listBox = null; return; }
    listBox = document.createElement("div");
    listBox.className = "pfp-list";
    if (!pins.length) listBox.textContent = "Пока ни одной точки.";
    pins.forEach((pin, index) => {
      const item = document.createElement("div");
      item.className = "pfp-item";
      item.innerHTML = "<b>" + (index + 1) + ".</b> "
        + (pin.note ? pin.note.replace(/</g, "&lt;") : "<i>без комментария</i>")
        + "<span>" + pin.page + " · " + pin.selector.replace(/</g, "&lt;") + "</span>";
      item.addEventListener("click", () => {
        if (pin.page !== here()) { location.href = pin.page; return; }
        const target = document.querySelector(pin.selector);
        if (target) target.scrollIntoView({ block: "center", behavior: "smooth" });
      });
      listBox.appendChild(item);
    });
    root.appendChild(listBox);
  };

  /* -------------------------------------------------------------------- панель */

  const bar = document.createElement("div");
  bar.className = "pfp-bar";
  const button = (text, handler, primary) => {
    const node = document.createElement("button");
    node.textContent = text;
    if (primary) node.className = "pfp-primary";
    node.addEventListener("click", (event) => { event.stopPropagation(); handler(node); });
    bar.appendChild(node);
    return node;
  };

  const title = document.createElement("div");
  title.className = "pfp-title";
  title.textContent = "Точки замечаний";
  bar.appendChild(title);

  button("+ Поставить точку", () => {
    placing = true;
    document.documentElement.classList.add("pfp-placing");
    hint("Ткни в место на странице");
  }, true);
  const counter = button("Список (" + pins.length + ")", list);
  counter.setAttribute("data-pfp-count", "1");
  button("Скопировать для Клода", copy);
  button("Убрать все", () => {
    if (!confirm("Удалить все точки? Их " + pins.length + ".")) return;
    pins = [];
    save(pins);
    if (listBox) { listBox.remove(); listBox = null; }
    paint();
  });
  button("Спрятать панель", () => toggle());
  root.appendChild(bar);

  /* ------------------------------------------------------------- пересчёт мест */

  let frame = 0;
  const repaint = () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(paint);
  };
  window.addEventListener("resize", repaint);
  window.addEventListener("load", repaint);
  // Картинки и шрифты доезжают позже и двигают вёрстку под точками.
  setTimeout(repaint, 1200);
  setTimeout(repaint, 3000);

  const toggle = () => {
    const hidden = root.style.display === "none";
    root.style.display = hidden ? "" : "none";
    if (hidden) repaint();
  };

  window.__pfPins = { toggle, pins: () => pins, text: asText };
  paint();
  hint("Точки включены. Ctrl+Alt+P — спрятать");
})();
