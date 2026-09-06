"""
PROMYACHIK TRANSFER AUTOPILOT - АДМИНКА

Локальная панель для разбора того, что автопилот не смог опубликовать сам,
и для управления уже опубликованными трансферами.

Публикация происходит автоматически и кнопки "опубликовать" здесь нет
намеренно: панель нужна только для исключений.

Запуск:
    python admin_server.py
    открыть http://127.0.0.1:8788

Сервер слушает только localhost.
"""
from __future__ import annotations

import html
import json
import re
import secrets
import subprocess
import sys
import threading
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
from transfer_discovery import ACTIVE_PROJECT, PARSER_ROOT, RECORDS_DIR  # noqa: E402

HOST = "127.0.0.1"
PORT = 8788
JOBS_DIR = PARSER_ROOT / "jobs"
ACTION_LOG = PARSER_ROOT / "state" / "admin_actions.jsonl"

# PF520A — ЗАЩИТА ОТ ЧУЖОЙ СТРАНИЦЫ
#
# Сервер слушает 127.0.0.1, то есть из интернета и даже из домашней сети до
# него не достучаться. Но это защищает не от всего. Пока админка запущена,
# ЛЮБОЙ сайт, открытый в том же браузере, мог отправить сюда обычную форму:
# браузер послушно шлёт её на localhost вместе с запросом. Проверок не было
# никаких, а действия здесь настоящие — «unpublish» снимает статью с сайта,
# и слуг для него брать неоткуда не нужно, он и есть публичный адрес
# страницы. То есть чужая страница могла удалять наши материалы, зная только
# ссылку на них.
#
# Три замка, каждый закрывает свою щель:
#   1. одноразовый ключ, живущий с запуска сервера. Чужая страница его не
#      знает: чтобы прочитать, нужно уметь читать ответ с localhost, а этого
#      кросс-доменные правила браузера не дают;
#   2. проверка, откуда пришёл запрос. Современный браузер честно пишет в
#      Origin и Sec-Fetch-Site, что форма чужая;
#   3. разбор параметров. entity_id раньше уходил прямо в имя файла, а слуг —
#      в аргумент publisher.py.
ADMIN_KEY = secrets.token_urlsafe(24)
SAFE_ID = re.compile(r"^[A-Za-z0-9._-]{1,120}$")
ALLOWED_ACTIONS = {"reject", "unpublish", "retry", "republish"}
SELF_ORIGINS = {"http://%s:%d" % (HOST, PORT), "http://localhost:%d" % PORT}

# Что означает каждое состояние и что с ним делать.
STATE_INFO = {
    "ENRICHED": ("Готов к публикации", "Данные собраны, ждёт ближайшего запуска.", "ok"),
    "PUBLISHED": ("Опубликован", "Статья на сайте.", "ok"),
    "DISCOVERED": ("Найден", "Ещё не проверялся.", "wait"),
    "AWAITING_CONFIRMATION": (
        "Договорённость, ждём закрытия сделки",
        "Это ещё не переход. Как только игрок появится в составе нового клуба "
        "на Transfermarkt, он опубликуется автоматически.", "wait"),
    "RETRY": ("Повтор по расписанию", "Временная причина, автопилот попробует сам.", "wait"),
    "SKIPPED_DUPLICATE": ("Пропущен как дубль", "Такой трансфер уже есть на сайте.", "muted"),
    "NEEDS_REVIEW": ("Нужен разбор", "Автоматически не решается, требуется решение.", "warn"),
    "REJECTED": ("Отклонён", "Снят с обработки вручную.", "muted"),
    "RUMOR_READY": (
        "Готов к публикации в Слухи",
        "Данные собраны, выйдет как слух при ближайшем прогоне.", "ok"),
    "PUBLISHED_AS_RUMOR": (
        "Опубликован в Слухах",
        "Страница в разделе «Слухи». Автопилот продолжает проверять, "
        "не закрылась ли сделка: как только игрок появится в составе нового "
        "клуба, выйдет полноценный трансфер, а слух будет снят с редиректом.",
        "ok"),
}

REASON_RU = {
    "PLAYER_NOT_IN_DESTINATION_SQUAD":
        "Игрок не числится в составе клуба назначения на Transfermarkt — "
        "переход не подтверждён. Если сделка реальна, попробуйте позже.",
    "TM_CLUB_UNRESOLVED":
        "Клуб назначения не опознан в справочнике Transfermarkt.",
    "AMBIGUOUS_PLAYER":
        "В составе несколько однофамильцев, однозначно выбрать нельзя.",
    "BLOCKED_NO_PLAYER_PHOTO":
        "Портрет на Transfermarkt ещё не опубликован. Публикация без фото запрещена.",
    "TM_SQUAD_UNAVAILABLE":
        "Transfermarkt временно не ответил.",
    "AGREEMENT_NOT_YET_COMPLETED":
        "Стороны договорились, но игрок ещё не заявлен за новый клуб. "
        "Публиковать как состоявшийся переход нельзя. Кнопка «Проверить сейчас» "
        "перепроверит состав немедленно, иначе автопилот сделает это сам.",
}

_running: dict[str, str] = {}
_lock = threading.Lock()


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_action(entity_id: str, action: str, result: str) -> None:
    ACTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ACTION_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"at": now(), "entity_id": entity_id,
                                 "action": action, "result": result[:2000]},
                                ensure_ascii=False) + "\n")


def load_records() -> list[dict]:
    records = []
    for path in sorted(RECORDS_DIR.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if record.get("schema_version") == 2:
            record["_path"] = str(path)
            records.append(record)
    return records


def published_slugs() -> dict[str, dict]:
    """slug -> запись. Часть исторических записей slug не имеет."""
    try:
        data = json.loads(
            (ACTIVE_PROJECT / "data" / "transfers.json").read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {row["slug"]: row for row in data
            if isinstance(row, dict) and row.get("slug")}


def transfers_total() -> int:
    """Всего записей на сайте, включая исторические без slug."""
    try:
        data = json.loads(
            (ACTIVE_PROJECT / "data" / "transfers.json").read_text(encoding="utf-8"))
    except Exception:
        return 0
    return sum(1 for row in data if isinstance(row, dict))


def job_path_for(record: dict) -> Path | None:
    slug = record.get("job_slug")
    if not slug and record.get("player_full_name") and record.get("to_club"):
        from job_builder import slugify  # локальный импорт: тяжёлые зависимости
        slug = "%s-%s" % (slugify(record["player_full_name"]),
                          slugify(record["to_club"]))
    if not slug:
        return None
    candidate = JOBS_DIR / ("autopilot_%s.json" % slug)
    return candidate if candidate.exists() else None


# ---------------------------------------------------------------------------
# Действия. Выполняются в фоне, чтобы страница не висела.
# ---------------------------------------------------------------------------

def run_step(args: list[str]) -> tuple[bool, str]:
    result = subprocess.run([sys.executable] + args, cwd=str(BIN),
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=1800)
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, output


def do_action(entity_id: str, action: str, slug: str) -> None:
    try:
        if action == "reject":
            path = RECORDS_DIR / ("%s.json" % entity_id)
            record = json.loads(path.read_text(encoding="utf-8"))
            record["pipeline_state"] = "REJECTED"
            record["rejected_at"] = now()
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
            log_action(entity_id, action, "отклонён вручную")
            return

        if action == "unpublish":
            ok, output = run_step(["publisher.py", "--unpublish", slug])
            log_action(entity_id, action, output[-1500:])
            return

        if action in ("retry", "republish"):
            # Повтор = перепроверить данные заново, затем собрать и опубликовать.
            ok, output = run_step(["transfer_enrichment.py", "--save"])
            if ok:
                ok, more = run_step(["job_builder.py", "--save", "--network"])
                output += more
            if ok:
                job = JOBS_DIR / ("autopilot_%s.json" % slug) if slug else None
                if job and job.exists():
                    ok, more = run_step(["publisher.py", "--job", str(job)])
                    output += more
                else:
                    output += "\nJOB не собран: кандидат не прошёл проверки."
            log_action(entity_id, action, output[-2500:])
            return
    except Exception as error:
        log_action(entity_id, action, "ОШИБКА: %s" % error)
    finally:
        with _lock:
            _running.pop(entity_id, None)


def start_action(entity_id: str, action: str, slug: str) -> None:
    with _lock:
        if entity_id in _running:
            return
        _running[entity_id] = action
    threading.Thread(target=do_action, args=(entity_id, action, slug),
                     daemon=True).start()


# ---------------------------------------------------------------------------
# Отрисовка
# ---------------------------------------------------------------------------

STYLE = """
*{box-sizing:border-box}
body{margin:0;background:#0b1220;color:#e6edf6;
     font:15px/1.55 -apple-system,Segoe UI,Roboto,sans-serif}
header{padding:20px 28px;border-bottom:1px solid #1e2a3d;
       display:flex;align-items:baseline;gap:18px;flex-wrap:wrap}
h1{margin:0;font-size:19px;letter-spacing:.3px}
.sub{color:#7d8ea6;font-size:13px}
main{padding:22px 28px;max-width:1180px}
.group{margin-bottom:30px}
.group h2{font-size:14px;text-transform:uppercase;letter-spacing:.8px;
          color:#8ea3bd;margin:0 0 4px}
.group p.hint{margin:0 0 12px;color:#63748c;font-size:13px}
.card{background:#111c2e;border:1px solid #1e2a3d;border-radius:8px;
      padding:14px 16px;margin-bottom:10px}
.card.warn{border-color:#6b4a12;background:#1a1710}
.card.ok{border-color:#1d4030}
.card.muted{opacity:.62}
.row{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.name{font-weight:600;font-size:16px}
.route{color:#9db2cc;font-size:14px;margin-top:2px}
.meta{color:#63748c;font-size:12.5px;margin-top:6px}
.reason{margin-top:9px;padding:9px 11px;background:#0d1725;
        border-left:3px solid #6b4a12;border-radius:3px;
        color:#d8c9a8;font-size:13.5px}
.actions{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}
button{background:#1b2a42;color:#dce7f5;border:1px solid #2b3d5a;
       border-radius:6px;padding:7px 13px;font-size:13.5px;cursor:pointer}
button:hover{background:#243755}
button.danger{border-color:#5a2b2b;color:#f0c8c8}
button.danger:hover{background:#3a1e1e}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11.5px;
       background:#1b2a42;color:#9db2cc;margin-left:8px}
.running{color:#e8c46a;font-size:13px;margin-top:8px}
a{color:#7fb3ff}
.empty{color:#63748c;padding:16px 0}
"""

SCRIPT = """
setTimeout(function(){location.reload()}, 15000);
function act(entity, action, slug, label){
  if(action==='unpublish' && !confirm('Убрать «'+label+'» с сайта?')) return;
  var f=document.createElement('form');
  f.method='POST'; f.action='/action';
  f.innerHTML='<input name=entity_id value="'+entity+'">'
            + '<input name=action value="'+action+'">'
            + '<input name=slug value="'+slug+'">'
            + '<input name=key value="__ADMIN_KEY__">';
  document.body.appendChild(f); f.submit();
}
"""


def esc(value) -> str:
    return html.escape(str(value or ""))


def render_card(record: dict, is_published: bool) -> str:
    entity_id = record.get("entity_id", "")
    state = "PUBLISHED" if is_published else record.get("pipeline_state", "DISCOVERED")
    label, _, tone = STATE_INFO.get(state, (state, "", ""))
    player = record.get("player_full_name") or record.get("player") or "?"
    slug = ""
    if record.get("player_full_name") and record.get("to_club"):
        from job_builder import slugify
        slug = "%s-%s" % (slugify(record["player_full_name"]),
                          slugify(record["to_club"]))

    source = record.get("source") or {}
    parts = ['<div class="card %s">' % tone]
    parts.append('<div class="row"><div>')
    parts.append('<div class="name">%s<span class="badge">%s</span></div>'
                 % (esc(player), esc(label)))
    parts.append('<div class="route">%s → %s</div>'
                 % (esc(record.get("from_club") or "?"), esc(record.get("to_club"))))
    meta = []
    if record.get("tm_player_id"):
        meta.append("TM %s" % record["tm_player_id"])
    if record.get("fee_raw"):
        meta.append(esc(record["fee_raw"]))
    if source.get("publisher"):
        link = source.get("url") or "#"
        meta.append('<a href="%s" target="_blank">%s</a>'
                    % (esc(link), esc(source["publisher"])))
    if record.get("discovered_at"):
        meta.append("найден %s" % esc(record["discovered_at"][:16].replace("T", " ")))
    parts.append('<div class="meta">%s</div>' % " · ".join(meta))
    parts.append("</div></div>")

    reason = record.get("block_reason")
    if reason:
        text = REASON_RU.get(reason, record.get("block_detail") or reason)
        parts.append('<div class="reason"><b>%s</b><br>%s</div>'
                     % (esc(reason), esc(text)))
    elif record.get("verdict_reason"):
        parts.append('<div class="reason">%s</div>' % esc(record["verdict_reason"]))

    with _lock:
        running = _running.get(entity_id)
    if running:
        parts.append('<div class="running">выполняется: %s…</div>' % esc(running))
    else:
        buttons = []
        if is_published:
            buttons.append(("republish", "Перепубликовать", ""))
            buttons.append(("unpublish", "Убрать с сайта", "danger"))
            if slug:
                buttons.append(("open", "Открыть", ""))
        elif state in ("AWAITING_CONFIRMATION", "PUBLISHED_AS_RUMOR"):
            buttons.append(("retry", "Проверить сейчас", ""))
            buttons.append(("reject", "Отклонить", "danger"))
        elif state in ("NEEDS_REVIEW", "RETRY", "DISCOVERED", "ENRICHED"):
            buttons.append(("retry", "Повторить", ""))
            buttons.append(("reject", "Отклонить", "danger"))
        html_buttons = []
        for action, title, css in buttons:
            if action == "open":
                html_buttons.append(
                    '<a href="http://localhost:1313/promyachik/transfers/%s/" '
                    'target="_blank"><button>Открыть</button></a>' % esc(slug))
            else:
                html_buttons.append(
                    "<button class=\"%s\" onclick=\"act('%s','%s','%s','%s')\">%s</button>"
                    % (css, esc(entity_id), action, esc(slug),
                       esc(player).replace("'", ""), title))
        if html_buttons:
            parts.append('<div class="actions">%s</div>' % "".join(html_buttons))
    parts.append("</div>")
    return "".join(parts)


def render_page() -> str:
    records = load_records()
    published = published_slugs()
    total = transfers_total()
    from job_builder import plural_ru, slugify

    groups: dict[str, list[dict]] = {}
    for record in records:
        slug = ""
        if record.get("player_full_name") and record.get("to_club"):
            slug = "%s-%s" % (slugify(record["player_full_name"]),
                              slugify(record["to_club"]))
        state = "PUBLISHED" if slug in published else record.get(
            "pipeline_state", "DISCOVERED")
        groups.setdefault(state, []).append(record)

    order = ["NEEDS_REVIEW", "RETRY", "ENRICHED", "RUMOR_READY",
             "AWAITING_CONFIRMATION", "PUBLISHED", "PUBLISHED_AS_RUMOR",
             "DISCOVERED", "SKIPPED_DUPLICATE", "REJECTED"]
    body = []
    for state in order:
        rows = groups.get(state) or []
        if not rows:
            continue
        label, hint, _ = STATE_INFO.get(state, (state, "", ""))
        body.append('<div class="group"><h2>%s — %d</h2><p class="hint">%s</p>'
                    % (esc(label), len(rows), esc(hint)))
        for record in rows:
            body.append(render_card(record, state == "PUBLISHED"))
        body.append("</div>")

    if not body:
        body.append('<div class="empty">Очередь пуста. '
                    'Запустите разведку, чтобы появились кандидаты.</div>')

    return """<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Promyachik — автопилот</title><style>%s</style></head><body>
<header><h1>Promyachik · автопилот</h1>
<span class="sub">публикация идёт сама · здесь только исключения</span>
<span class="sub">на сайте %d %s · обновлено %s</span></header>
<main>%s</main><script>%s</script></body></html>""" % (
        STYLE, total, plural_ru(total, "трансфер", "трансфера", "трансферов"),
        now(), "".join(body), SCRIPT.replace("__ADMIN_KEY__", ADMIN_KEY))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # тише в консоли
        pass

    def _send(self, code: int, body: str, content_type="text/html; charset=utf-8"):
        payload = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/":
            self._send(200, render_page())
        elif path == "/log":
            text = ACTION_LOG.read_text(encoding="utf-8") if ACTION_LOG.exists() else ""
            self._send(200, "<pre>%s</pre>" % html.escape(text[-20000:]))
        else:
            self._send(404, "not found")

    def _refuse(self, why: str) -> None:
        """Отказ пишем в журнал: если такое придёт, надо знать откуда."""
        log_action("-", "отказано", "%s | origin=%s | referer=%s" % (
            why, self.headers.get("Origin") or "нет",
            self.headers.get("Referer") or "нет"))
        self._send(403, "нет")

    def do_POST(self):
        # Замок 2: чужая форма. Браузер сам сообщает, что запрос кросс-доменный.
        origin = self.headers.get("Origin")
        if origin and origin not in SELF_ORIGINS:
            return self._refuse("чужой Origin")
        if (self.headers.get("Sec-Fetch-Site") or "same-origin") != "same-origin":
            return self._refuse("кросс-доменный запрос")

        length = int(self.headers.get("Content-Length") or 0)
        if length > 8192:
            return self._refuse("слишком большое тело")
        data = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8"))

        # Замок 1: ключ этого запуска. Чужая страница его не прочитает.
        if not secrets.compare_digest((data.get("key") or [""])[0], ADMIN_KEY):
            return self._refuse("неверный ключ")

        entity_id = (data.get("entity_id") or [""])[0]
        action = (data.get("action") or [""])[0]
        slug = (data.get("slug") or [""])[0]

        # Замок 3: разбор параметров. entity_id уходит в имя файла, slug — в
        # аргумент publisher.py; ни там, ни там косой черте и точкам делать
        # нечего.
        if action not in ALLOWED_ACTIONS:
            return self._refuse("неизвестное действие %r" % action)
        if not SAFE_ID.match(entity_id) or ".." in entity_id:
            return self._refuse("подозрительный entity_id")
        if slug and (not SAFE_ID.match(slug) or ".." in slug):
            return self._refuse("подозрительный slug")
        if not (RECORDS_DIR / ("%s.json" % entity_id)).exists():
            return self._refuse("записи нет: %s" % entity_id)

        start_action(entity_id, action, slug)
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


def main() -> int:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("\n  Админка запущена: http://%s:%d" % (HOST, PORT))
    print("  Публикация автоматическая. Здесь — только разбор исключений.")
    print("  Остановить: Ctrl+C\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Админка остановлена.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
