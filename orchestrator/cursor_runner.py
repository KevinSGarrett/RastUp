# orchestrator/cursor_runner.py
import os
import sys
import time
import uuid
import shlex
import zipfile
import platform
import subprocess
import pathlib

# Optional event logger
try:
    from orchestrator.logger_jsonl import append_event
except Exception:
    def append_event(_):  # no-op if logger not present
        pass

WSL_DISTRO = os.environ.get("WSL_DISTRO", "Ubuntu")
CURSOR_BIN_HINT = os.environ.get("CURSOR_BIN", "~/.local/bin/cursor-agent")  # hint from Windows side (optional)

def _win_to_wsl_path(win_path: str) -> str:
    p = pathlib.PureWindowsPath(win_path)
    drive = p.drive.replace(":", "").lower()
    rest = "/".join(p.parts[1:])
    return f"/mnt/{drive}/{rest}"

def _sanitize_prompt(p: str) -> str:
    # strip BOM + normalize to LF; leave final newline optional (agent doesn't require it)
    return p.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")

def run_cursor(
    repo_path: str,
    prompt: str,
    cursor_cli: str = "cursor",
    agent_name: str = "AGENT-1",
    model: str = "gpt-5",
):
    """
    Windows: write prompt to a real file and execute an inner script in WSL using absolute paths.
    * Adds ~/.local/bin to PATH for non-interactive shells
    * Resolves cursor-agent robustly (env CURSOR_BIN inside WSL, or PATH, or ~/.local/bin)
    * Reads prompt from file, strips CR, passes as a single argument
    * Uses stdbuf (if present) for line-buffered streaming and timeout (if present) for soft cap
    Non-Windows: call cursor-agent directly or fall back to 'cursor agent --headless'.
    """
    run_id = f"{int(time.time())}-{uuid.uuid4().hex[:6]}"
    repo_abs = os.path.abspath(repo_path)

    # Use absolute attach dir so WSL path conversion is always correct
    agent_dir = os.path.join(repo_abs, "docs", "orchestrator", "from-agents", agent_name)
    os.makedirs(agent_dir, exist_ok=True)
    log_txt  = os.path.join(agent_dir, f"run-{run_id}.log")
    inner_sh = os.path.join(agent_dir, f"run-{run_id}.inner.sh")

    # Write the prompt to disk (LF newlines)
    prompt_clean = _sanitize_prompt(prompt)
    prompts_dir = os.path.join(repo_abs, "ops", "prompts")
    os.makedirs(prompts_dir, exist_ok=True)
    prompt_win = os.path.join(prompts_dir, f".cursor_prompt_{run_id}.txt")
    with open(prompt_win, "w", encoding="utf-8", newline="\n") as f:
        f.write(prompt_clean)

    # Branch by platform
    if platform.system().lower().startswith("win"):
        repo_wsl   = _win_to_wsl_path(repo_abs)
        prompt_wsl = _win_to_wsl_path(os.path.abspath(prompt_win))
        inner_wsl  = _win_to_wsl_path(os.path.abspath(inner_sh))

        # Inner script executed via "bash < script" to avoid inline quoting pitfalls
        inner = f"""\
set -Eeuo pipefail

# Ensure non-interactive shells see ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"

cd {shlex.quote(repo_wsl)}

# Accept a Windows-side hint (embedded here) but resolve inside WSL
CB_HINT_RAW={shlex.quote(CURSOR_BIN_HINT)}
CB="$CB_HINT_RAW"
if [ -n "$CB" ]; then
  case "$CB" in "~/"*) CB="$HOME/${{CB#~/}}";; esac
fi

# Resolve agent binary: hint → PATH → ~/.local/bin
if [ -n "$CB" ] && [ -x "$CB" ]; then
  :
elif command -v cursor-agent >/dev/null 2>&1; then
  CB="$(command -v cursor-agent)"
elif [ -x "$HOME/.local/bin/cursor-agent" ]; then
  CB="$HOME/.local/bin/cursor-agent"
else
  echo "ERROR: cursor-agent not found (hint: $CB_HINT_RAW)" >&2
  exit 127
fi

PROMPT_PATH={shlex.quote(prompt_wsl)}
if ! [ -s "$PROMPT_PATH" ]; then
  echo "ERROR: prompt file missing/empty: $PROMPT_PATH" >&2
  exit 3
fi

# Diagnostics
echo "USING cursor-agent: $CB"
echo "PROMPT_PATH: $PROMPT_PATH"
echo "PROMPT_BYTES=$(wc -c < "$PROMPT_PATH")"

# Read prompt and strip any CR to avoid argument splitting
PROMPT="$(tr -d '\\r' < "$PROMPT_PATH")"

export NO_OPEN_BROWSER=1

# Decide on line-buffering (stdbuf) and soft timeout (timeout)
_has_stdbuf=0
_has_timeout=0
command -v stdbuf >/dev/null 2>&1 && _has_stdbuf=1
command -v timeout >/dev/null 2>&1 && _has_timeout=1

TIMEOUT_SECS="${{TIMEOUT_SECS:-1200}}"  # 20 minutes default

if [ "$_has_timeout" -eq 1 ] && [ "$_has_stdbuf" -eq 1 ]; then
  timeout "$TIMEOUT_SECS" stdbuf -oL -eL "$CB" --print --output-format=text --force --approve-mcps --model {shlex.quote(model)} "$PROMPT" || \
  timeout "$TIMEOUT_SECS" stdbuf -oL -eL "$CB" agent --print --output-format=text --force --approve-mcps --model {shlex.quote(model)} "$PROMPT"
elif [ "$_has_timeout" -eq 1 ]; then
  timeout "$TIMEOUT_SECS" "$CB" --print --output-format=text --force --approve-mcps --model {shlex.quote(model)} "$PROMPT" || \
  timeout "$TIMEOUT_SECS" "$CB" agent --print --output-format=text --force --approve-mcps --model {shlex.quote(model)} "$PROMPT"
elif [ "$_has_stdbuf" -eq 1 ]; then
  stdbuf -oL -eL "$CB" --print --output-format=text --force --approve-mcps --model {shlex.quote(model)} "$PROMPT" || \
  stdbuf -oL -eL "$CB" agent --print --output-format=text --force --approve-mcps --model {shlex.quote(model)} "$PROMPT"
else
  "$CB" --print --output-format=text --force --approve-mcps --model {shlex.quote(model)} "$PROMPT" || \
  "$CB" agent --print --output-format=text --force --approve-mcps --model {shlex.quote(model)} "$PROMPT"
fi
"""
        # Save helper script (LF) and EXECUTE THE FILE
        with open(inner_sh, "w", encoding="utf-8", newline="\n") as f:
            f.write(inner)

        # Execute via bash reading the file to avoid quoting edge-cases
        cmd = ["wsl", "-d", WSL_DISTRO, "--", "bash", "-lc", f"bash < {shlex.quote(inner_wsl)}"]
        cmd_for_log = f"wsl -d {WSL_DISTRO} -- bash -lc 'bash < {inner_wsl}'"
        cwd = None

    else:
        # Non-Windows: call cursor-agent if present; fall back to Cursor CLI headless
        import shutil
        agent = shutil.which("cursor-agent")
        if agent:
            cmd = [agent, "--print", "--output-format", "text", "--force", "--approve-mcps", "--model", model, _sanitize_prompt(prompt)]
        else:
            cmd = [cursor_cli, "agent", "--headless", "--project", repo_abs, "--prompt", _sanitize_prompt(prompt)]
        cmd_for_log = " ".join(shlex.quote(x) for x in cmd)
        cwd = repo_abs

    # Stream to console and log
    os.makedirs(os.path.dirname(log_txt), exist_ok=True)
    with open(log_txt, "w", encoding="utf-8") as lf:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        lf.write(f"[{now}] INFO start: {agent_name} run_id={run_id}\n")
        lf.write(f"[{now}] INFO cmd: {cmd_for_log}\n"); lf.flush()

        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        try:
            for line in iter(proc.stdout.readline, ""):
                sys.stdout.write(line); sys.stdout.flush()
                lf.write(line); lf.flush()
        finally:
            if proc.stdout:
                proc.stdout.close()
        ret = proc.wait()
        lf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] INFO finish: exit_code={ret}\n")

    # Zip artifacts (log + inner script)
    zip_path = os.path.join(agent_dir, f"run-{run_id}-attach.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(log_txt,  arcname=os.path.basename(log_txt))
        try:
            zf.write(inner_sh, arcname=os.path.basename(inner_sh))
        except Exception:
            pass

    # Best-effort cleanup of the transient prompt file
    try:
        os.remove(prompt_win)
    except Exception:
        pass

    append_event({
        "actor": agent_name,
        "kind": "cursor.run",
        "status": "ok" if ret == 0 else "fail",
        "run_id": run_id,
        "attach": zip_path,
        "cmd": cmd_for_log,
    })
    return {"run_id": run_id, "attach": zip_path, "retcode": ret}
