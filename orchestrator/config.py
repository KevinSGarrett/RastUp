from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load .env from repo root
load_dotenv()

@dataclass
class Settings:
    slack_bot_token: str = os.getenv("SLACK_BOT_TOKEN","")
    slack_app_token: str = os.getenv("SLACK_APP_TOKEN","")
    slack_signing_secret: str = os.getenv("SLACK_SIGNING_SECRET","")
    slack_channel: str = os.getenv("SLACK_CHANNEL_ORCH","#orchestrator")
    weekly_usd_cap: float = float(os.getenv("WEEKLY_USD_CAP","75"))
    soft_alert_pct: int = int(os.getenv("SOFT_ALERT_PCT","80"))
    boost_stop_loss: float = float(os.getenv("BOOST_STOP_LOSS","5"))
    cursor_cli: str = os.getenv("CURSOR_CLI","cursor")
    repo_root: str = os.getcwd()

SETTINGS = Settings()
