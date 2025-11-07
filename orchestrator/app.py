import os, re, threading
from pathlib import Path
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from orchestrator.config import SETTINGS
from orchestrator.budget import Budget
from orchestrator.cursor_runner import run_cursor
from orchestrator.logger_jsonl import append_event

app = App(token=SETTINGS.slack_bot_token, signing_secret=SETTINGS.slack_signing_secret)
BUDGET = Budget()

def find_latest_log(agent: str = "AGENT-1"):
    base = Path("docs") / "orchestrator" / "from-agents" / agent
    if not base.exists():
        return None
    logs = sorted(base.glob("run-*.log"), key=lambda p: p.stat().st_mtime)
    return str(logs[-1]) if logs else None

def tail_last_lines(path: str, n: int = 120) -> str:
    try:
        size = os.path.getsize(path)
        if size <= 8192:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read().splitlines()
            return "\n".join(lines[-n:])
        # otherwise read from the end in 4KB blocks
        data = b""
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            block = -1
            while len(data.splitlines()) <= n and abs(block) * 4096 < size:
                f.seek(block * 4096, os.SEEK_END)
                data = f.read() + data
                block -= 1
        return b"\n".join(data.splitlines()[-n:]).decode("utf-8", errors="ignore")
    except Exception as e:
        return f"(tail error: {e})"

@app.command("/orchestrator")
def orchestrator_cmd(ack, body, respond, say, client):
    ack()
    text = (body.get("text") or "").strip()

    # status
    if text.startswith("status"):
        pct = BUDGET.percent()
        mode = "ECONOMY" if BUDGET.economy_mode() else "NORMAL"
        respond(f"*Orchestrator status*\n• Budget: ${BUDGET.week_spend:.2f}/${BUDGET.cap} ({pct:.1f}%) — mode: {mode}\n• Boosts used: {BUDGET.boosts_used}/3")
        return

    # verbosity
    if text.startswith("verbosity"):
        level = text.split(" ", 1)[1] if " " in text else "milestones"
        append_event({"actor": "ORCH", "kind": "verbosity.set", "level": level})
        respond(f"Verbosity set to *{level}*.")
        return

    # run "Title" --wbs WBS-x.y
    if text.startswith("run"):
        m = re.search(r'run\s+"(.+?)"(?:\s+--wbs\s+(\S+))?', text)
        title = m.group(1) if m else "Ad-hoc task"
        wbs = m.group(2) if m and m.group(2) else None
        respond(f"Starting agent run: *{title}*{' ('+wbs+')' if wbs else ''} …")

        def _bg():
            res = run_cursor(SETTINGS.repo_root, f"{title}", cursor_cli=SETTINGS.cursor_cli, agent_name="AGENT-1")
            say(f"Run finished: `{res['run_id']}` ret={res['retcode']} • Attach: `{res['attach']}`")
        threading.Thread(target=_bg, daemon=True).start()
        return

    # tail [agent] [lines]
    if text.startswith("tail"):
        parts = text.split()
        agent = "AGENT-1"
        lines = 120
        if len(parts) >= 2 and not parts[1].isdigit():
            agent = parts[1]
        if len(parts) >= 3 and parts[-1].isdigit():
            lines = int(parts[-1])

        log_path = find_latest_log(agent)
        if not log_path:
            respond(f"No log found for *{agent}*.")
            return

        snippet = tail_last_lines(log_path, n=lines)
        respond(f"*Latest log for* `{agent}`\n`{log_path}`\n```{snippet[-2800:]}```")

        # upload full log (v2 API; bot must be in the channel)
        try:
            client.files_upload_v2(
                channel=body["channel_id"],
                initial_comment=f"Full log for `{agent}`",
                file=log_path,
                filename=os.path.basename(log_path),
            )
        except Exception as e:
            respond(f"(file upload skipped: {e})")
        return

    # approve (stub)
    if text.startswith("approve"):
        respond("Type *APPROVE* to confirm this proposal in the thread. (Stub in MVP)")
        return

    # default help
    respond("Usage: `/orchestrator status` | `run \"Title\" --wbs WBS-x.y` | `tail [AGENT-1] [lines]` | `verbosity <milestones|summaries|quiet>` | `approve <id>`")

if __name__ == "__main__":
    handler = SocketModeHandler(app, SETTINGS.slack_app_token)
    handler.start()
