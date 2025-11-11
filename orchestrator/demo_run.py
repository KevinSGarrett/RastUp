from orchestrator.config import SETTINGS
from orchestrator.cursor_runner import run_cursor

if __name__ == "__main__":
    res = run_cursor(
        repo_path=".",
        prompt="Demo run: write a log and attach pack",
        cursor_cli=SETTINGS.cursor_cli,   # <-- critical
        agent_name="AGENT-1"
    )
    print(res)
