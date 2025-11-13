import json
import logging
import os
import re
import threading
import time
from pathlib import Path
from typing import Any, Dict, List

from slack_bolt import App

from orchestrator.config import SETTINGS  # type: ignore[import]
from orchestrator.llm_plan import llm_plan_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_default_root = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(getattr(SETTINGS, "repo_root", os.getenv("REPO_ROOT", str(_default_root))))
OPS_DIR = REPO_ROOT / "ops"
FLAGS_DIR = OPS_DIR / "flags"
FLAGS_DIR.mkdir(parents=True, exist_ok=True)
OPS_DIR.mkdir(parents=True, exist_ok=True)

LEDGER_PATH = OPS_DIR / "ledger.jsonl"
QUEUE_PATH = OPS_DIR / "queue.jsonl"
SAFE_FLAG = FLAGS_DIR / "safe.txt"
BOOST_FLAG = FLAGS_DIR / "boost.txt"


def _read_bool(path: Path, default: bool = False) -> bool:
    try:
        raw = path.read_text(encoding="utf-8").strip()
        if raw.lower() in {"1", "true", "yes", "on"}:
            return True
        if raw.lower() in {"0", "false", "no", "off"}:
            return False
    except FileNotFoundError:
        return default
    except Exception as e:  # pragma: no cover - defensive
        logger.warning(f"Failed to read bool flag %s: %s", path, e)
    return default


def _write_bool(path: Path, value: bool) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("1" if value else "0", encoding="utf-8")
    except Exception as e:  # pragma: no cover - defensive
        logger.error("Failed to write bool flag %s: %s", path, e)


def _read_float(path: Path, default: float = 1.0) -> float:
    try:
        raw = path.read_text(encoding="utf-8").strip()
        return float(raw)
    except FileNotFoundError:
        return default
    except Exception:
        return default


def _write_float(path: Path, value: float) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(value), encoding="utf-8")
    except Exception as e:  # pragma: no cover - defensive
        logger.error("Failed to write float flag %s: %s", path, e)


def _tail_file(path: Path, n: int = 20) -> List[str]:
    try:
        with path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    return [ln.rstrip("\n") for ln in lines[-n:]]


def _append_ledger(event: Dict[str, Any]) -> None:
    try:
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception as e:  # pragma: no cover - defensive
        logger.error("Failed to append ledger event: %s", e)


def _load_status() -> (bool, float):
    safe = _read_bool(SAFE_FLAG, default=False)
    boost = _read_float(BOOST_FLAG, default=1.0)
    return safe, boost


def _status_line() -> str:
    safe, boost = _load_status()
    safe_emoji = ":lock:" if safe else ":unlock:"
    return f"{safe_emoji} SAFE={'ON' if safe else 'OFF'}, BOOST={boost:.2f}"


def _say_ephemeral(respond, text: str) -> None:
    try:
        respond(text=text, response_type="ephemeral")
    except Exception as e:  # pragma: no cover - defensive
        logger.error("Failed ephemeral respond: %s", e)


def _show_help(respond) -> None:
    help_text = f"""*RastUp Orchestrator*

{_status_line()}

Commands (all start with `/orchestrator`):

• `help` – show this message
• `status` – show health + SAFE/BOOST
• `safe on|off` – toggle SAFE mode (require you to explicitly approve heavy/autonomous work)
• `boost <x>` – set aggressiveness multiplier (float), e.g. `boost 5.0`
• `boost clear` – reset BOOST back to 1.0
• `llm-plan "<prompt>"` – plan the next 3–5 days using the WBS extracted from:

    C:\\RastUp\\RastUp\\ProjectBlueprint\\Combined_Master_PLAIN_Non_Tech_001.docx
    C:\\RastUp\\RastUp\\ProjectBlueprint\\TechnicalDevelopmentPlan.odt

  (It auto-extracts WBS-1.* and WBS-2.* from those files on each call.)

• `heavy "Reason" <usd>` – manually log a big spend into ops/ledger.jsonl
• `queue` – show the last few entries in ops/queue.jsonl (if present)
"""
    _say_ephemeral(respond, help_text)


# Slack app init

bot_token = getattr(SETTINGS, "slack_bot_token", None) or os.getenv("SLACK_BOT_TOKEN")
signing_secret = getattr(SETTINGS, "slack_signing_secret", None) or os.getenv("SLACK_SIGNING_SECRET")

if not bot_token or not signing_secret:
    raise RuntimeError(
        "Slack credentials missing for orchestrator. "
        "Set SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET (or configure them via orchestrator.config.SETTINGS)."
    )

app = App(token=bot_token, signing_secret=signing_secret)


_HEAVY_RE = re.compile(r'heavy\s+"([^"]+)"\s+([0-9]*\.?[0-9]+)', re.IGNORECASE)


@app.command("/orchestrator")
def orchestrator_cmd(ack, body, respond, logger):  # type: ignore[override]
    ack()

    user_id = body.get("user_id")
    channel_id = body.get("channel_id")
    raw_text = (body.get("text") or "").strip()
    lower = raw_text.lower()

    # No subcommand or explicit help
    if not raw_text or lower in {"help", "h", "-h", "--help"} or lower.startswith("ping"):
        _show_help(respond)
        return

    # Status / health
    if lower.startswith("status") or lower.startswith("health"):
        _say_ephemeral(respond, f":green_circle: alive — {_status_line()}")
        return

    # SAFE on/off
    if lower.startswith("safe"):
        parts = lower.split()
        if len(parts) < 2 or parts[1] not in {"on", "off"}:
            _say_ephemeral(respond, "Usage: `/orchestrator safe on` or `/orchestrator safe off`")
            return
        safe_on = parts[1] == "on"
        _write_bool(SAFE_FLAG, safe_on)
        _say_ephemeral(respond, f"SAFE mode is now *{'ON' if safe_on else 'OFF'}*.")
        return

    # BOOST <x> | clear
    if lower.startswith("boost"):
        parts = raw_text.split()
        if len(parts) == 1:
            _, boost = _load_status()
            _say_ephemeral(respond, f"Current BOOST = {boost:.2f}")
            return

        if parts[1].lower() == "clear":
            try:
                if BOOST_FLAG.exists():
                    BOOST_FLAG.unlink()
            except Exception:
                pass
            _say_ephemeral(respond, "BOOST cleared (back to default 1.0).")
            return

        try:
            value = float(parts[1])
        except ValueError:
            _say_ephemeral(respond, "Usage: `/orchestrator boost <number>` or `boost clear`.")
            return

        _write_float(BOOST_FLAG, value)
        _say_ephemeral(respond, f"BOOST set to {value:.2f}.")
        return

    # LLM planner (OpenAI / Anthropic) using blueprint WBS
    if lower.startswith("llm-plan"):
        prompt = raw_text[len("llm-plan"):].strip()
        if (prompt.startswith('"') and prompt.endswith('"')) or (
            prompt.startswith("'") and prompt.endswith("'")
        ):
            if len(prompt) >= 2:
                prompt = prompt[1:-1]

        if not prompt:
            prompt = "Plan the next 3–5 days of work for WBS-1.* and WBS-2.* based on the blueprints."

        _say_ephemeral(
            respond,
            ":hourglass_flowing_sand: Asking the orchestrator LLM to plan the next 3–5 days from the blueprint WBS…",
        )

        def _bg():
            try:
                plan_text = llm_plan_text(prompt)
                app.client.chat_postMessage(
                    channel=channel_id,
                    text=f"*LLM plan requested by <@{user_id}>:*\n{plan_text}",
                )
            except Exception as e:
                try:
                    app.client.chat_postMessage(
                        channel=channel_id,
                        text=f":x: `/orchestrator llm-plan` failed: `{e}`",
                    )
                except Exception:
                    pass

        threading.Thread(target=_bg, daemon=True).start()
        return

    # Manual heavy ledger entry
    if lower.startswith("heavy"):
        m = _HEAVY_RE.match(raw_text)
        if not m:
            _say_ephemeral(respond, 'Usage: `/orchestrator heavy "Reason" <usd>`')
            return
        reason = m.group(1)
        usd = float(m.group(2))
        event = {
            "ts": time.time(),
            "type": "manual-heavy",
            "user": user_id,
            "reason": reason,
            "usd": usd,
        }
        _append_ledger(event)
        _say_ephemeral(respond, f"Recorded heavy step: *{reason}* — ${usd:.2f} (manual ledger).")
        return

    # Queue preview
    if lower.startswith("queue"):
        if not QUEUE_PATH.exists():
            _say_ephemeral(respond, "Queue file not found at `ops/queue.jsonl`.")
            return
        lines = _tail_file(QUEUE_PATH, 12)
        if not lines:
            _say_ephemeral(respond, "Queue is empty.")
            return
        preview = "Last items in queue:\n```" + "\n".join(lines) + "```"
        _say_ephemeral(respond, preview)
        return

    _say_ephemeral(
        respond,
        f"Unrecognized subcommand: `{raw_text}`.\n"
        "Use `/orchestrator help` to see supported commands.\n\n"
        "Note: heavy Cursor/autopilot runs from Slack are intentionally not wired up yet; "
        "run them via the CLI until the blueprint+WBS integration is rock solid.",
    )
