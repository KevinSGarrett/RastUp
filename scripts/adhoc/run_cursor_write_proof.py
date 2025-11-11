import io, os, sys
repo = r"C:\RastUp\RastUp"
if repo not in sys.path: sys.path.insert(0, repo)
from orchestrator.cursor_runner import run_cursor
prompt = io.open(r"C:\RastUp\RastUp\ops\prompts\write-proof.txt", "r", encoding="utf-8").read()
print(run_cursor(repo, prompt, agent_name="AGENT-1", model="gpt-5"))