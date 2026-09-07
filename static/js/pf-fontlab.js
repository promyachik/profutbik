/*
 * PF530A — ПРИМЕРОЧНАЯ ШРИФТОВ
 *
 * То же, что в журнале: список шрифтов, каждый написан сам собой, выбор
 * применяется к сайту мгновенно и запоминается. Нужен, чтобы Дмитрий
 * подбирал шрифт глазами на живых страницах, а не по описаниям.
 *
 * Почему меняются переменные, а не правила. Весь шрифтовой слой сайта сведён
 * к двум значениям в pf-global-roboto.css:
 *
 *     --pf-global-font-family    основной текст
 *     --pf-display-font-family   имена игроков и заголовки
 *
 * Подменяя их на :root, мы попадаем во все правила разом, включая написанные
 * с !important, — спорить о специфичности не приходится. Именно ради этого
 * шрифты в своё время и вынесли в переменные.
 *
 * PF531A: у каждой роли теперь две ячейки — основной шрифт и запасной, на
 * случай, когда основного у читателя нет. Смотри константу SYSTEM ниже.
 *
 * Посетителям не грузится: включается Alt+F, Alt+A или адресом ?fonts=1.
 * Выбор живёт только в браузере Дмитрия, на сайт он не влияет, пока мы не
 * пропишем его в CSS руками.
 */
(() => {
  "use strict";

  if (window.__pfFontLab) {
    window.__pfFontLab.toggle();
    return;
  }

  const STORE = "pf-fontlab";
  const GOLD = "#f1bd29";

  /* Запасной шрифт — не формальность. Corbel, Candara, Constantia и прочая
     подборка ClearType есть на Windows и на Mac с установленным Office, но её
     нет ни на одном телефоне: iOS, Android и Linux о ней не знают. На
     футбольном сайте читают в основном с телефона, то есть запасной увидит не
     край выборки, а большинство.

     Поэтому у каждой роли две ячейки: основной и запасной. Переключатель
     «Запасной» выбрасывает основной из стопки и показывает страницу ровно
     так, как её видит человек без него, — иначе на своём Windows выбираешь
     вслепую. */
  const SYSTEM = "Системный";
  const SYSTEM_STACK = 'system-ui,-apple-system,"Segoe UI",Roboto';

  // Только с кириллицей: сайт русский, и шрифт без неё отвалится на первом же
  // слове. Подмена происходит молча, поэтому проверять надо заранее.
  const FONTS = [
    ["Roboto", "web"], ["Inter", "web"], ["Manrope", "web"], ["Onest", "web"],
    ["Golos Text", "web"], ["Rubik", "web"], ["Commissioner", "web"],
    ["Mulish", "web"], ["Montserrat", "web"], ["Raleway", "web"],
    ["Nunito", "web"], ["Open Sans", "web"], ["PT Sans", "web"],
    ["Fira Sans", "web"], ["IBM Plex Sans", "web"], ["Noto Sans", "web"],
    ["Ubuntu", "web"], ["Exo 2", "web"], ["Comfortaa", "web"],
    ["Unbounded", "web"], ["Oswald", "web"], ["Roboto Condensed", "web"],
    ["Merriweather", "web"], ["Lora", "web"], ["Playfair Display", "web"],
    ["PT Serif", "web"], ["Spectral", "web"], ["Cormorant Infant", "web"],
    ["JetBrains Mono", "web"],
    ["Segoe UI", "sys"], ["Bahnschrift", "sys"], ["Georgia", "sys"],
    ["Constantia", "sys"], ["Corbel", "sys"], ["Candara", "sys"],
    ["Cambria", "sys"], ["Verdana", "sys"], ["Trebuchet MS", "sys"],
  ];

  const GOOGLE = "https://fonts.googleapis.com/css2?"
    + FONTS.filter(([, kind]) => kind === "web")
        .map(([name]) => "family=" + name.replace(/ /g, "+") + ":wght@300;400;700;800")
        .join("&") + "&display=swap";

  /* ------------------------------------------------------------ применение */

  const override = document.createElement("style");
  override.id = "pf-fontlab-override";
  document.head.appendChild(override);

  const EMPTY = {
    text: "", display: "", club: "",
    textAlt: "", displayAlt: "", clubAlt: "",
  };

  const state = (() => {
    try {
      return Object.assign({}, EMPTY,
        JSON.parse(localStorage.getItem(STORE) || "null"));
    } catch (error) {
      return Object.assign({}, EMPTY);
    }
  })();

  let target = "text";   // что сейчас подбираем: текст, заголовки или клубы
  let slot = "main";     // какую ячейку роли: основную или запасную

  /* Кто есть кто на сайте. Роли перечислены явно, потому что подмены одних
     переменных не хватает: за годы в CSS накопились правила со своими
     стопками — Impact, Arial Narrow, Trebuchet MS, часть с !important. Их
     примерочная обязана перебить, иначе половина страницы не переоденется и
     будет казаться, что выбор не работает.

     !important здесь уместен: это инструмент на вечер, а не вёрстка. Когда
     шрифт выберем, править будем сами правила, а не давить их силой. */
  const DISPLAY = [
    ".pf-home-transfers-table tbody td.is-player a", ".pf405a-player",
    ".transfer-stage__player", ".pf-transfer-player strong",
    ".pf-home-panel__title", ".pf405a-head-title",
    "h1", "h2", "h3",
  ].join(",");

  const CLUB = [
    ".pf-club-name-inline", ".pf-transfer-club strong",
    ".transfer-stage__club-name", ".pf405a-league__name",
  ].join(",");

  const keyOf = (role) => (slot === "alt" ? role + "Alt" : role);

  // Стопка для роли. В режиме «Запасной» основной шрифт из неё выброшен — это
  // и есть весь смысл режима.
  const familyFor = (role) => {
    const main = state[role];
    const alt = state[role + "Alt"];
    if (!main && !alt) return "";
    const parts = [];
    if (slot === "main" && main) parts.push(`"${main}"`);
    if (alt) parts.push(alt === SYSTEM ? SYSTEM_STACK : `"${alt}"`);
    parts.push("sans-serif");
    return parts.join(",");
  };

  const apply = () => {
    const vars = [];
    const rules = [];
    /* PF531B: почему тут ещё и --pf-font-here.

       Глобальное правило в pf-global-roboto.css заканчивается одиннадцатью
       :not() — его специфичность (0,11,1), и никакое наше правило её не
       наберёт, даже с !important. Пока примерочная давила силой, она молча
       проигрывала: менялись только фамилии игроков, потому что они эту
       переменную объявляют сами. Заголовки разделов не двигались вовсе, а
       выглядело это как «шрифт выбран».

       Поэтому не спорим, а подставляемся: переменная наследуется,
       специфичность ей не нужна. !important оставлен для мест, до которых
       глобальное правило не дотягивается. */
    const put = (role, name, selector, here) => {
      const family = familyFor(role);
      if (!family) return;
      vars.push(`${name}:${family}`);
      rules.push(`${selector}{${here ? `--pf-font-here:${family};` : ""}`
        + `font-family:${family} !important}`);
    };
    put("text", "--pf-global-font-family", "body,body *", false);
    put("display", "--pf-display-font-family", DISPLAY, true);
    put("club", "--pf-club-font-family", CLUB, true);
    // Саму панель под подмену не пускаем: иначе список перестанет показывать
    // каждый шрифт им самим, а ради этого он и нужен.
    rules.push('#pf-fontlab,#pf-fontlab *{font-family:"Segoe UI",Arial,sans-serif !important}');
    override.textContent =
      (vars.length ? `:root{${vars.join(";")}}` : "") + rules.join("");
    try {
      localStorage.setItem(STORE, JSON.stringify(state));
    } catch (error) { /* приватный режим — просто не запомним */ }

    const chosen = state[keyOf(target)];
    root.querySelectorAll(".pfl-item").forEach((button) => {
      button.classList.toggle("on", button.dataset.name === chosen);
    });
    const main = state[target];
    const alt = state[target + "Alt"];
    root.querySelector("[data-pfl-now]").textContent =
      main && alt ? `${main} → ${alt}`
        : main || (alt ? `как на сайте → ${alt}` : "как на сайте");
    mark();
  };

  /* ------------------------------------------------------------- разметка */

  const root = document.createElement("div");
  root.id = "pf-fontlab";
  root.innerHTML = `
<style>
  #pf-fontlab{position:fixed;inset:0;z-index:2147483000;pointer-events:none;
    font:400 14px/1.4 "Segoe UI",Arial,sans-serif}
  #pf-fontlab *{box-sizing:border-box}
  .pfl-box{position:absolute;right:18px;top:18px;width:min(280px,90vw);
    max-height:calc(100vh - 36px);pointer-events:auto;display:flex;
    flex-direction:column;border:1px solid #2b3542;border-radius:14px;
    background:#0d1117;box-shadow:0 24px 70px rgba(0,0,0,.7)}
  .pfl-grip{height:26px;display:grid;place-items:center;cursor:grab;
    border-bottom:1px solid #1c2531;border-radius:14px 14px 0 0;background:#121923}
  .pfl-grip:active{cursor:grabbing}
  .pfl-grip::before{content:"";width:38px;height:4px;border-radius:4px;background:#3d4756}
  .pfl-grip:hover::before{background:${GOLD}}
  .pfl-close{position:absolute;right:6px;top:2px;width:24px;height:24px;
    border:0;background:none;color:#7d8794;font-size:17px;cursor:pointer;z-index:2}
  .pfl-close:hover{color:#e8edf3}
  .pfl-tabs{display:flex;gap:4px;padding:8px 8px 6px}
  .pfl-tabs button{flex:1;padding:7px;border:1px solid #2b3542;border-radius:8px;
    background:#121923;color:#8d99a8;font:inherit;font-size:12px;cursor:pointer}
  .pfl-tabs button.on{border-color:${GOLD};color:${GOLD};background:#1a1508}
  .pfl-slot{display:flex;gap:4px;padding:0 8px 6px}
  .pfl-slot button{flex:1;padding:5px;border:1px solid #232c38;border-radius:8px;
    background:#0f151d;color:#77818e;font:inherit;font-size:11px;cursor:pointer}
  .pfl-slot button.on{border-color:#3d7dd8;color:#8fbcff;background:#0e1724}
  .pfl-hint{padding:0 12px 8px;color:#5e6874;font-size:10px;line-height:1.4}
  .pfl-hint[hidden]{display:none}
  .pfl-now{padding:0 12px 8px;color:#6f7a86;font-size:11px}
  .pfl-now b{color:#c9d2dc;font-weight:600}
  .pfl-list{overflow:auto;padding:0 6px 8px}
  .pfl-item{display:flex;align-items:baseline;width:100%;padding:7px 10px;
    margin-bottom:2px;border:1px solid transparent;border-radius:8px;
    background:none;color:#dfe6ee;font-size:15px;text-align:left;cursor:pointer}
  .pfl-item:hover{background:#141b25;border-color:#2b3542}
  .pfl-item.on{border-color:${GOLD};background:#1a1508;color:#fff}
  .pfl-item small{margin-left:auto;padding-left:8px;font-size:10px;color:#6f7a86;
    font-family:"Segoe UI",Arial,sans-serif}
  .pfl-item small:empty{display:none}
  .pfl-item.gone{opacity:.32;cursor:not-allowed}
  /* display:flex у строки перебивает служебный [hidden] — гасим явно. */
  .pfl-item[hidden]{display:none}
  .pfl-reset{margin:0 6px 8px;padding:7px;border:1px solid #2b3542;border-radius:8px;
    background:none;color:#8d99a8;font:inherit;font-size:12px;cursor:pointer}
  .pfl-reset:hover{color:#e8edf3;border-color:#3d4756}
</style>
<div class="pfl-box">
  <div class="pfl-grip"></div>
  <button class="pfl-close" type="button" aria-label="Закрыть">×</button>
  <div class="pfl-tabs">
    <button type="button" data-target="text" class="on">Текст</button>
    <button type="button" data-target="display">Заголовки</button>
    <button type="button" data-target="club">Клубы</button>
  </div>
  <div class="pfl-slot">
    <button type="button" data-slot="main" class="on">Основной</button>
    <button type="button" data-slot="alt">Запасной</button>
  </div>
  <div class="pfl-hint" hidden>Страница показана без основного шрифта — так её
    видят с телефона, Mac без Office и Linux.</div>
  <div class="pfl-now">Сейчас: <b data-pfl-now>как на сайте</b></div>
  <div class="pfl-list"></div>
  <button class="pfl-reset" type="button">Вернуть как было</button>
</div>`;
  document.body.appendChild(root);

  const box = root.querySelector(".pfl-box");
  const list = root.querySelector(".pfl-list");

  const addItem = (name, kind, extra) => {
    const button = document.createElement("button");
    button.className = "pfl-item" + (extra ? " " + extra : "");
    button.type = "button";
    button.dataset.name = name;
    button.dataset.kind = kind;
    button.style.setProperty("font-family",
      kind === "any" ? SYSTEM_STACK + ",sans-serif" : `'${name}',sans-serif`,
      "important");
    button.innerHTML = `${name}<small></small>`;
    button.addEventListener("click", () => {
      state[keyOf(target)] = name;
      apply();
    });
    list.appendChild(button);
  };

  // «Системный» — законный выбор запасного: ничего не грузится, у каждого
  // читается родным шрифтом его системы. Основным быть не может, поэтому в
  // режиме «Основной» строка спрятана.
  addItem(SYSTEM, "any", "pfl-sys");
  FONTS.forEach(([name, kind]) => addItem(name, kind));

  /* Есть ли шрифт у человека. Меряем ширину строки: совпала с запасным —
     значит подстановки не было и шрифта нет. Веб-шрифты приезжают всем. */
  const has = (name) => {
    const probe = "ЖШЩЫФЫВАПРОЛДЖЭ mmmmwwwwiiii 0123456789";
    const canvas = has.c || (has.c = document.createElement("canvas").getContext("2d"));
    canvas.font = "72px monospace";
    const base = canvas.measureText(probe).width;
    canvas.font = `72px '${name}',monospace`;
    return Math.abs(canvas.measureText(probe).width - base) > 0.01;
  };

  const mark = () => {
    root.querySelectorAll(".pfl-item").forEach((button) => {
      const kind = button.dataset.kind;
      // В запасные системные шрифты не годятся: весь смысл запасного в том,
      // что он есть у всех, а Candara или Trebuchet есть не везде.
      const banned = slot === "alt" && kind === "sys";
      const ok = !banned && (kind !== "sys" || has(button.dataset.name));
      button.classList.toggle("gone", !ok);
      button.disabled = !ok;
      button.querySelector("small").textContent =
        banned ? "не у всех" : (ok ? "" : "нет в системе");
    });
    root.querySelector(".pfl-sys").hidden = slot !== "alt";
  };

  root.querySelectorAll(".pfl-tabs button").forEach((tab) => {
    tab.addEventListener("click", () => {
      target = tab.dataset.target;
      root.querySelectorAll(".pfl-tabs button")
        .forEach((other) => other.classList.toggle("on", other === tab));
      apply();
    });
  });

  root.querySelectorAll(".pfl-slot button").forEach((pill) => {
    pill.addEventListener("click", () => {
      slot = pill.dataset.slot;
      root.querySelectorAll(".pfl-slot button")
        .forEach((other) => other.classList.toggle("on", other === pill));
      root.querySelector(".pfl-hint").hidden = slot !== "alt";
      apply();
    });
  });

  root.querySelector(".pfl-reset").addEventListener("click", () => {
    Object.assign(state, EMPTY);
    apply();
  });

  /* ----------------------------------------------------------- поведение */

  const toggle = () => {
    root.style.display = root.style.display === "none" ? "" : "none";
  };
  root.querySelector(".pfl-close").addEventListener("click", toggle);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && root.style.display !== "none") toggle();
  });

  // Тянем за полоску. Положение в долях окна: в пикселях панель, поставленная
  // на большом мониторе, на ноутбуке уехала бы за край.
  const grip = root.querySelector(".pfl-grip");
  const place = (fx, fy) => {
    const r = box.getBoundingClientRect();
    box.style.left = Math.max(8, Math.min(fx * innerWidth, innerWidth - r.width - 8)) + "px";
    box.style.top = Math.max(8, Math.min(fy * innerHeight, innerHeight - r.height - 8)) + "px";
    box.style.right = "auto";
  };
  try {
    const saved = JSON.parse(localStorage.getItem(STORE + "-pos") || "null");
    if (saved) requestAnimationFrame(() => place(saved[0], saved[1]));
  } catch (error) { /* позиции нет */ }
  grip.addEventListener("pointerdown", (event) => {
    event.preventDefault();
    const r = box.getBoundingClientRect();
    const dx = event.clientX - r.left;
    const dy = event.clientY - r.top;
    try { grip.setPointerCapture(event.pointerId); } catch (error) { /* без захвата */ }
    const move = (m) => place((m.clientX - dx) / innerWidth, (m.clientY - dy) / innerHeight);
    const stop = () => {
      grip.removeEventListener("pointermove", move);
      grip.removeEventListener("pointerup", stop);
      const n = box.getBoundingClientRect();
      try {
        localStorage.setItem(STORE + "-pos",
          JSON.stringify([n.left / innerWidth, n.top / innerHeight]));
      } catch (err) { /* не запомним */ }
    };
    grip.addEventListener("pointermove", move);
    grip.addEventListener("pointerup", stop);
  });

  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = GOOGLE;
  link.addEventListener("load", mark);
  document.head.appendChild(link);
  setTimeout(mark, 900);

  window.__pfFontLab = { toggle, state };
  apply();
})();
