from slack_bolt.adapter.socket_mode import SocketModeHandler
from orchestrator.config import SETTINGS
from orchestrator.app import app

if __name__ == "__main__":
    SocketModeHandler(app, SETTINGS.slack_app_token).start()
