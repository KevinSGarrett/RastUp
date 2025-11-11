# orchestrator/app.py
import json
import os
import re
import shlex
import threading
from pathlib import Path
from typing import Tuple

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Local modules
try:
    from orchestrator.config import SETTINGS
except Exception:
    class _Fallback:
        slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "")
        slack_app_token = os.environ.get("SLACK_APP_TOKEN", "")
        slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
        repo_root = os.environ.get("REPO_ROOT", r"C:\RastUp\RastUp")
    SETTINGS = _Fallback()

from orchestrator.cursor_runner import run_cursor

REPO_ROOT = Path(getattr(SETTINGS, "repo_root", r"C:\RastUp\RastUp"))
LEDGER = REPO_ROOT / "docs" / "logs" / "cost-ledger.jsonl"
SAFE_FLAG = REPO_ROOT / "ops" / "flags" / "safe-mode.json"
BOOST_FILE = REPO_ROOT / "ops" / "flags" / "boost.json"
AGENTS_DIR = REPO_ROOT / "docs" / "orchestrator" / "from-agents"
CAP_USD = float(os.environ.get("BUDGET_CAP_USD", "75.0"))
DEFAULT_MODEL = os.environ.get("CURSOR_AGENT_MODEL", "gpt-5")

# ------------------------------------------------------------------------------
# App setup
# ------------------------------------------------------------------------------
app = App(token=SETTINGS.slack_bot_token, signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
def _read_ledger_sum() -> float:
    if not LEDGER.exists():
        return 0.0
    total = 0.0
    with LEDGER.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                j = json.loads(line)
                total += float(j.get("usd", 0.0))
            except Exception:
                continue
    return round(total, 2)

def _safe_mode() -> bool:
    return SAFE_FLAG.exists()

def _set_safe_mode(on: bool) -> None:
    SAFE_FLAG.parent.mkdir(parents=True, exist_ok=True)
    if on:
        SAFE_FLAG.write_text(json.dumps({"reason": "manual", "by": "orchestrator", "ts": ""}))
    else:
        try:
            SAFE_FLAG.unlink()
        except FileNotFoundError:
            pass

def _get_boost() -> float:
    if not BOOST_FILE.exists():
        return 0.0
    try:
        data = json.loads(BOOST_FILE.read_text(encoding="utf-8"))
        return float(data.get("remaining", 0.0))
    except Exception:
        return 0.0

def _set_boost(amount: float) -> None:
    BOOST_FILE.parent.mkdir(parents=True, exist_ok=True)
    BOOST_FILE.write_text(json.dumps({"remaining": float(amount)}), encoding="utf-8")

def _last_log(agent: str) -> Path:
    d = AGENTS_DIR / agent
    if not d.exists():
        return None
    files = sorted(d.glob("run-*.log"), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None

def _has_write_approval() -> bool:
    """Return True if any approval in ops/approvals grants 'write' and is approved."""
    appr_dir = REPO_ROOT / "ops" / "approvals"
    if not appr_dir.exists():
        return False
    try:
        for p in appr_dir.glob("*.json"):
            try:
                data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            status = str(data.get("status", "")).lower()
            allowed = {str(x).lower() for x in (data.get("allowed") or [])}
            if status == "approved" and ("write" in allowed or "all" in allowed):
                return True
    except Exception:
        return False
    return False

def _parse_run_args(text: str) -> Tuple[str, str, str]:
    """
    Parse: run "<title words...>" --agent AGENT-1 --model gpt-5
    Title is everything after 'run' until the first option token that starts with '--'
    """
    parts = shlex.split(text)
    if not parts:
        return "", "AGENT-1", DEFAULT_MODEL
    assert parts[0] == "run"
    title_tokens = []
    i = 1
    while i < len(parts) and not parts[i].startswith("--"):
        title_tokens.append(parts[i]); i += 1
    title = " ".join(title_tokens) if title_tokens else "Untitled run"

    agent = "AGENT-1"
    model = DEFAULT_MODEL
    while i < len(parts):
        tok = parts[i]
        if tok == "--agent" and i + 1 < len(parts):
            agent = parts[i + 1]; i += 2; continue
        if tok == "--model" and i + 1 < len(parts):
            model = parts[i + 1]; i += 2; continue
        i += 1
    return title, agent, model

# ------------------------------------------------------------------------------
# Slash command
# ------------------------------------------------------------------------------
@app.command("/orchestrator")
def orchestrator_cmd(ack, body, respond, logger):
    # Ack immediately to avoid dispatch_failed
    ack()

    user_id = body.get("user_id")
    channel_id = body.get("channel_id")
    text = (body.get("text") or "").strip()

    def say_ephemeral(msg: str):
        try:
            respond(text=msg, response_type="ephemeral")
        except Exception as e:
            logger.error(f"respond error: {e}")

    if not text or text.lower().startswith("ping"):
        # minimal alive
        sm = "ON" if _safe_mode() else "OFF"
        say_ephemeral(f":green_circle: alive — SAFE={sm}, BOOST={_get_boost():.1f}")
        return

    if text.lower().startswith("status"):
        spent = _read_ledger_sum()
        pct = 0.0 if CAP_USD <= 0 else (spent / CAP_USD) * 100.0
        sm = "ON" if _safe_mode() else "OFF"
        say_ephemeral(
            "Orchestrator status\n"
            f"• Budget: ${spent:.2f}/${CAP_USD:.2f} ({pct:.1f}%) — mode: ECONOMY\n"
            f"• SAFE-MODE: {sm}\n"
            f"• Boosts used: 0/3\n"
            f"• Active Boost: {_get_boost():.1f}"
        )
        return

    if text.lower().startswith("safe"):
        if re.search(r"\bon\b", text, re.I):
            _set_safe_mode(True)
            say_ephemeral(":shield: SAFE-MODE **ON**")
        elif re.search(r"\boff\b", text, re.I):
            if not _has_write_approval():
                say_ephemeral(":no_entry: SAFE-OFF requires approval (ops/approvals/* with allowed: write).")
                return
            _set_safe_mode(False)
            say_ephemeral(":rocket: SAFE-MODE **OFF** (queue may drain)")
        else:
            say_ephemeral("Usage: `/orchestrator safe on|off`")
        return

    if text.lower().startswith("boost"):
        if not _has_write_approval():
            say_ephemeral(":no_entry: Boost changes require approval (ops/approvals/* with allowed: write).")
            return
        m = re.search(r"boost\s+clear", text, re.I)
        if m:
            _set_boost(0.0)
            say_ephemeral(":boom: Boost cleared (0.0)")
            return
        m = re.search(r"boost\s+([0-9]+(\.[0-9]+)?)", text, re.I)
        if m:
            amt = float(m.group(1))
            _set_boost(amt)
            say_ephemeral(f":boom: Boost set to {amt:.2f}")
            return
        say_ephemeral("Usage: `/orchestrator boost <amount>` or `/orchestrator boost clear`")
        return

    if text.lower().startswith("tail"):
        # /orchestrator tail [AGENT] [lines]
        parts = shlex.split(text)
        agent = parts[1] if len(parts) > 1 and not parts[1].startswith("--") else "AGENT-1"
        lines = 80
        for i, tok in enumerate(parts):
            if tok == "--lines" and i + 1 < len(parts):
                try: lines = int(parts[i + 1])
                except: pass
        p = _last_log(agent)
        if not p:
            say_ephemeral(f"No logs found for {agent}")
            return
        try:
            content = p.read_text(encoding="utf-8", errors="ignore").splitlines()[-lines:]
            preview = "```\n" + "\n".join(content) + "\n```"
            say_ephemeral(f"*{agent}* latest log: `{p.name}`\n{preview}")
        except Exception as e:
            say_ephemeral(f"Error reading log: {e}")
        return

    if text.lower().startswith("run"):
        title, agent, model = _parse_run_args(text)

        if _safe_mode() and _get_boost() <= 0.0:
            say_ephemeral(":warning: SAFE-MODE is ON and no Boost is available — run queued or requires approval.")
            return

        say_ephemeral(f":hourglass_flowing_sand: Starting *{agent}* — {title}\nModel: `{model}`")

        def _bg():
            try:
                res = run_cursor(str(REPO_ROOT), f"{title}", agent_name=agent, model=model)
                log_path = res.get("attach", "").replace("\\", "/")
                rc = res.get("retcode", 1)
                head = ":white_check_mark:" if rc == 0 else ":x:"
                msg = f"{head} *{agent}* finished — exit_code={rc}\nAttach: `{log_path}`"
            except Exception as e:
                msg = f":x: *{agent}* failed to launch: `{e}`"
            try:
                app.client.chat_postMessage(channel=channel_id, text=msg)
            except Exception:
                # fall back: ephemeral respond (command context may be gone)
                try: respond(text=msg, response_type="ephemeral")
                except Exception: pass

        threading.Thread(target=_bg, daemon=True).start()
        return

    # Unknown subcommand
    say_ephemeral("Unknown command. Try: `ping`, `status`, `safe on|off`, `boost <amount>|clear`, `tail [AGENT] [--lines N]`, `run \"Title\" --agent AGENT-1 --model gpt-5`")

# ------------------------------------------------------------------------------
# Keep the export `app` so orchestrator.socket_main can import it
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Useful for local foreground debugging: python -m orchestrator.app
    handler = SocketModeHandler(app, SETTINGS.slack_app_token)
    handler.start()
