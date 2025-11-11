from scripts.ad_hoc.py_path_helper import add_repo_root
add_repo_root()

from orchestrator.cursor_runner import run_cursor
import io
REPO = r"C:\RastUp\RastUp"
prompt = io.open(r"C:\RastUp\RastUp\ops\prompts\wbs-1-2-ci.txt", "r", encoding="utf-8").read()
print(run_cursor(REPO, prompt, agent_name="AGENT-1", model="gpt-5"))
