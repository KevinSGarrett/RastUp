set -Eeuo pipefail
cd /mnt/c/RastUp/RastUp
PYBIN=$(command -v python3 || command -v python)
"$PYBIN" - <<'PY'
import os, sys, subprocess
CURSOR_BIN = os.path.expanduser('~/.local/bin/cursor-agent')
MODEL = gpt-5
PROMPT_PATH = /mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762838573-5d658d.txt

try:
    with open(PROMPT_PATH, "r", encoding="utf-8", errors="replace") as fh:
        prompt = fh.read()
except Exception as e:
    print(f"ERROR: cannot read prompt file: {e}", file=sys.stderr)
    sys.exit(2)

cmds = [
    [CURSOR_BIN, "--print", "--output-format", "text", "--force", "--approve-mcps", "--model", MODEL, prompt],
    [CURSOR_BIN, "agent", "--print", "--output-format", "text", "--force", "--approve-mcps", "--model", MODEL, prompt],
]

ret = 1
for cmd in cmds:
    try:
        cp = subprocess.run(cmd, check=True)
        ret = cp.returncode
        break
    except FileNotFoundError:
        print(f"ERROR: cursor-agent not found at {CURSOR_BIN}", file=sys.stderr)
        ret = 127
        break
    except subprocess.CalledProcessError as e:
        ret = e.returncode
        continue

sys.exit(ret)
PY
