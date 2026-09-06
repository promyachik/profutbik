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

  const save = (list) => {
    try {
      // `node` — живая ссылка на элемент, она нужна только в памяти: в JSON
      // это циклическая структура, и сериализация упала бы.
      localStorage.setItem(STORE, JSON.stringify(list, (key, value) =>
        (key === "node" ? undefined : value)));
    } catch (error) {
      alert("Не удалось сохранить точку: в браузере кончилось место.");
    }
  };

  let pins = load();
  // Ключ страницы — только путь. С хвостом запроса точка, поставленная на
  // /?pins=1, не нашлась бы на / — а это одна и та же страница.
  const here = () => location.pathname;

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

  const classesOf = (element) =>
    (typeof element.className === "string" ? element.className : "")
      .trim().split(/\s+/).filter(Boolean);

  /* Классы-состояния в путь не годятся: `is-measuring` живёт полсекунды,
     пока скрипт разворачивания меряет высоту таблицы, а `is-active` меняется
     от щелчка по фильтру. Путь с таким классом наутро уже ни к чему не
     ведёт. Структурные `is-player`, `is-club`, `is-status` оставляем — они
     от состояния не зависят. */
  const TRANSIENT = new Set([
    "is-measuring", "is-active", "is-open", "is-expanded", "is-collapsed",
    "is-hidden", "is-visible", "is-lost", "is-current", "is-selected",
  ]);

  const stepFor = (element) => {
    if (element.id) return "#" + CSS.escape(element.id);
    let part = element.tagName.toLowerCase();
    const cls = classesOf(element)
      .filter((c) => !TRANSIENT.has(c) && !/^pfp-/.test(c))
      .slice(0, 3);
    if (cls.length) part += "." + cls.map((c) => CSS.escape(c)).join(".");
    const siblings = element.parentElement
      ? [...element.parentElement.children].filter((n) => n.tagName === element.tagName)
      : [];
    if (siblings.length > 1) {
      part += ":nth-of-type(" + (siblings.indexOf(element) + 1) + ")";
    }
    return part;
  };

  /* Точный путь — чтобы точка после перезагрузки села на своё место.
     Растём вверх, пока путь не станет единственным на странице, и на этом
     останавливаемся. Обрезать по числу уровней нельзя: путь
     `tr:nth-of-type(1) > td.is-from > a > img.pf-club-logo` описывает первую
     строку и в трансферах, и в слухах, querySelector берёт первую — и точка,
     поставленная в слухах, всплывала слева, в трансферах. Уникальным он
     становится, когда доходит до `.pf-home-panel--rumors`. */
  const selectorFor = (element) => {
    if (!element || element === document.body) return "body";

    const parts = [];
    let current = element;
    while (current && current !== document.body) {
      parts.unshift(stepFor(current));
      const path = parts.join(" > ");
      try {
        if (document.querySelectorAll(path).length === 1) return path;
      } catch (error) {
        return path;
      }
      if (current.id) return path;
      current = current.parentElement;
    }
    return "body > " + parts.join(" > ");
  };

  /* PF519C: а вот это — главное, ради чего всё затевалось. Путь из ближайших
     осмысленных предков: `.pf-home-panel--rumors › .pf-club-cell ›
     .pf-club-logo`. По нему сразу видно, какое правило править, — тогда как
     `tr:nth-of-type(1) > td:nth-of-type(2) > a > img` не говорит даже, в
     каком из двух блоков главной поставлена точка. */
  // Крупные ориентиры страницы. Без них путь обрезается на середине и
  // теряет главное: в каком блоке поставлена точка.
  const LANDMARK = ".pf-home-panel--transfers, .pf-home-panel--rumors,"
    + " .pf-transfer-page, .pf-rumor-page, .player-brief, header, footer,"
    + " .home-player-bottom-strip, .bottom-transfer-strip-v3";

  /* Имя элемента для чтения. Из нескольких классов берём самый говорящий:
     модификатор с двумя дефисами, если он есть. `.pf-home-panel` есть у обоих
     блоков главной и не различает их, а `.pf-home-panel--rumors` различает. */
  const nameOf = (element) => {
    if (element.id) return "#" + element.id;
    const pf = classesOf(element).filter((c) => /^pf/i.test(c));
    if (!pf.length) return element.tagName.toLowerCase();
    const modifier = pf.find((c) => c.includes("--"));
    return "." + (modifier || pf.slice(0, 2).join("."));
  };

  const whereFor = (element) => {
    const chain = [];
    let current = element;
    while (current && current !== document.body && chain.length < 3) {
      if (current.id || classesOf(current).some((c) => /^pf/i.test(c))) {
        chain.unshift(current);
      }
      current = current.parentElement;
    }

    const landmark = element.closest && element.closest(LANDMARK);
    if (landmark && chain.indexOf(landmark) === -1) chain.unshift(landmark);
    if (!chain.length) return "<" + element.tagName.toLowerCase() + ">";
    return chain.map(nameOf).join(" › ");
  };

  /* Подпись «рядом текст». У картинки своего текста нет, а у контейнера его
     бывает на пол-экрана — и то и другое бесполезно. Берём короткий текст
     самого элемента, а если его нет, короткую подпись ближайшей строки:
     «Marcus Rashford Manchester United Arsenal» говорит, о какой именно
     строке речь, а первые девяносто символов таблицы — ни о чём. */
  const labelFor = (element) => {
    const own = (element.textContent || "").replace(/\s+/g, " ").trim();
    if (own && own.length <= 120) return own;
    const row = element.closest && element.closest("tr, li, article, figure, h1, h2, h3");
    const near = row ? (row.textContent || "").replace(/\s+/g, " ").trim() : "";
    return near && near.length <= 160 ? near : "";
  };

  const describe = (element) => ({
    selector: selectorFor(element),
    where: whereFor(element),
    classes: classesOf(element).join(" "),
    label: labelFor(element),
    html: (element.outerHTML || "").replace(/\s+/g, " ").slice(0, 320),
  });

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
      let target = (() => {
        try {
          return document.querySelector(pin.selector);
        } catch (error) {
          return null;
        }
      })();

      // Самолечение: пока живая ссылка на элемент при нас, а путь к нему
      // перестал вести — перевязываем. Так точка переживает правку вёрстки,
      // случившуюся у неё на глазах, а не только перезагрузку.
      if (!target && pin.node && pin.node.isConnected) {
        target = pin.node;
        pin.selector = selectorFor(target);
        save(pins);
      }
      if (target) pin.node = target;

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
      lines.push("   куда: " + (pin.where || pin.selector));
      if (pin.label) lines.push("   рядом текст: «" + pin.label + "»");
      lines.push("   точный путь: " + pin.selector);
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
        + "<span>" + pin.page + " · "
        + (pin.where || pin.selector).replace(/</g, "&lt;") + "</span>";
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
  /* PF519H: явный выход. Сочетание клавиш свободно в браузере, и попасть по
     нему случайно может кто угодно; человеку, который не понял, что это
     такое, нужна очевидная дверь наружу, а не догадка про ?pins=0. */
  button("Выключить точки", () => {
    try {
      localStorage.removeItem("pf-pins-on");
    } catch (error) { /* приватный режим — флага и так нет */ }
    delete window.__pfPins;
    root.remove();
    document.removeEventListener("click", place, true);
    document.documentElement.classList.remove("pfp-placing");
  });
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
