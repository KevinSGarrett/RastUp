import sys, io
REPO = r"C:\RastUp\RastUp"
if REPO not in sys.path: sys.path.insert(0, REPO)
from orchestrator.cursor_runner import run_cursor
with io.open(r"C:\RastUp\RastUp\ops\prompts\write-proof.txt","r",encoding="utf-8") as f:
    prompt = f.read().lstrip("\ufeff")
print(run_cursor(REPO, prompt, agent_name="AGENT-1", model="gpt-5"))