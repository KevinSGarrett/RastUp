import os, sys, json
from pathlib import Path
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from orchestrator.config import SETTINGS
from orchestrator.app import app  # reuse your configured app

def mask(t):
    if not t: return "None"
    s = str(t)
    return s[:6] + "…" + s[-4:] if len(s) > 12 else "***"

print("== DEBUG START ==")
print("BOT token  :", mask(SETTINGS.slack_bot_token))
print("APP token  :", mask(SETTINGS.slack_app_token))
print("SIGN secret:", "set" if SETTINGS.slack_signing_secret else "None")
try:
    print("starting Socket Mode handler…")
    h = SocketModeHandler(app, SETTINGS.slack_app_token)
    h.start()  # should block here if OK
except Exception as e:
    print("!! Socket Mode failed:", repr(e))
    import traceback; traceback.print_exc()
    sys.exit(2)
