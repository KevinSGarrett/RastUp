# orchestrator/config.py
from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

def _mask(s: str) -> str:
    s = s or ""
    if len(s) < 12:
        return s
    return f"{s[:6]}…{s[-6:]}"  # e.g., xoxb-9…pU7CYk

# --- Determine repo root & .env path -----------------------------------------
_ENV_REPO = (os.getenv("REPO_ROOT") or "").strip()
if _ENV_REPO:
    repo_root = Path(_ENV_REPO)
else:
    # this file lives at <repo>/orchestrator/config.py
    # parent of the parent should be the repo root
    repo_root = Path(__file__).resolve().parent.parent

env_file = repo_root / ".env"

# --- Capture state before we load .env (for debug) ---------------------------
_pre_bot = "SLACK_BOT_TOKEN" in os.environ and bool(os.environ.get("SLACK_BOT_TOKEN", "").strip())
_pre_app = "SLACK_APP_TOKEN" in os.environ and bool(os.environ.get("SLACK_APP_TOKEN", "").strip())

_file_bot = _file_app = False
try:
    if env_file.exists():
        txt = env_file.read_text(encoding="utf-8", errors="ignore")
        _file_bot = "SLACK_BOT_TOKEN=" in txt
        _file_app = "SLACK_APP_TOKEN=" in txt
except Exception:
    pass  # debug only

# --- Load .env (do not override process env) ---------------------------------
load_dotenv(dotenv_path=str(env_file), override=False)

def _get(name: str, default: str = "") -> str:
    return (os.getenv(name, default) or "").strip()

@dataclass
class Settings:
    slack_bot_token: str = _get("SLACK_BOT_TOKEN")
    slack_app_token: str = _get("SLACK_APP_TOKEN")
    slack_signing_secret: str = _get("SLACK_SIGNING_SECRET")
    slack_channel: str = _get("SLACK_CHANNEL_ORCH", "#orchestrator")

    weekly_usd_cap: float = float(_get("WEEKLY_USD_CAP", "75"))
    soft_alert_pct: int = int(_get("SOFT_ALERT_PCT", "80"))
    boost_stop_loss: float = float(_get("BOOST_STOP_LOSS", "5"))

    cursor_cli: str = _get("CURSOR_CLI", "cursor")
    repo_root: str = str(repo_root)

SETTINGS = Settings()

# --- Optional debug line ------------------------------------------------------
if os.getenv("RU_CONFIG_DEBUG"):
    print(
        "[config]"
        f" repo_root= {SETTINGS.repo_root}"
        f"  env_file= {env_file}"
        f"  from_env_bot= {bool(_pre_bot)}"
        f"  file_has_bot= {bool(_file_bot)}"
        f"  bot_present= {bool(SETTINGS.slack_bot_token)} { _mask(SETTINGS.slack_bot_token) if SETTINGS.slack_bot_token else '' }"
        f"  from_env_app= {bool(_pre_app)}"
        f"  file_has_app= {bool(_file_app)}"
        f"  app_present= {bool(SETTINGS.slack_app_token)} { _mask(SETTINGS.slack_app_token) if SETTINGS.slack_app_token else '' }"
    )
