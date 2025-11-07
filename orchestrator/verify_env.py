from orchestrator.config import SETTINGS
import os, platform
print("OS:", platform.system())
print("CURSOR_CLI (env):", os.getenv("CURSOR_CLI"))
print("SETTINGS.cursor_cli:", SETTINGS.cursor_cli)
