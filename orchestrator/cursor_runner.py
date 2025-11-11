import os, shlex, subprocess, time, uuid, zipfile, platform, pathlib, shutil
from orchestrator.logger_jsonl import append_event

WSL_DISTRO = os.environ.get("CURSOR_WSL_DISTRO", "Ubuntu")
CURSOR_BIN = os.environ.get("CURSOR_BIN", "~/.local/bin/cursor-agent")

def _win_to_wsl_path(win_path: str) -> str:
    p = pathlib.PureWindowsPath(win_path)
    drive = p.drive.replace(":", "").lower()
    rest = "/".join(p.parts[1:])
    return f"/mnt/{drive}/{rest}"

def run_cursor(
    repo_path: str,
    prompt: str,
    agent_name: str = "AGENT-1",
    model: str = None
):
    """
    Runs Cursor Agent headlessly.
    - On Windows: uses WSL cursor-agent with --print so output is capturable.
    - Else: tries native cursor-agent if available.
    Creates a log and an attach zip under docs/orchestrator/from-agents/<AGENT>/.
    """
    model = model or os.environ.get("CURSOR_AGENT_MODEL", "gpt-5")

    run_id = f"{int(time.time())}-{uuid.uuid4().hex[:6]}"
    attach_dir = os.path.join("docs","orchestrator","from-agents",agent_name)
    os.makedirs(attach_dir, exist_ok=True)
    log_txt = os.path.join(attach_dir, f"run-{run_id}.log")

    repo_abs = os.path.abspath(repo_path)
    is_windows = platform.system().lower().startswith("win")

    # Simple quoting: avoid double quotes inside the prompt for bash -lc
    prompt_q = prompt.replace('"', "'")

    if is_windows:
        repo_wsl = _win_to_wsl_path(repo_abs)
        inner = (
            f"cd {shlex.quote(repo_wsl)} && {CURSOR_BIN} "
            f"--print --output-format=text --force --approve-mcps "
            f"--model {shlex.quote(model)} {shlex.quote(prompt_q)}"
        )
        cmd = ["wsl", "-d", WSL_DISTRO, "--", "bash", "-lc", inner]
        cmd_for_log = f"wsl -d {WSL_DISTRO} -- bash -lc '{inner}'"
        cwd = None
        shell = False
    else:
        agent = shutil.which("cursor-agent")
        if agent:
            cmd = [agent, "--print", "--output-format=text", "--force", "--approve-mcps",
                   "--model", model, prompt_q]
            cmd_for_log = " ".join(shlex.quote(x) for x in cmd)
        else:
            raise RuntimeError("cursor-agent not found. Install Cursor Agent first.")
        cwd = repo_abs
        shell = False

    with open(log_txt, "w", encoding="utf-8") as lf:
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        lf.write(f"[{now}] INFO start: {agent_name} run_id={run_id}\n")
        lf.write(f"[{now}] INFO cmd: {cmd_for_log}\n")
        lf.flush()

        proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, shell=shell)
        for line in proc.stdout:
            lf.write(line)
        ret = proc.wait()
        lf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] INFO finish: exit_code={ret}\n")

    zip_path = os.path.join(attach_dir, f"run-{run_id}-attach.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(log_txt, arcname=os.path.basename(log_txt))

    append_event({"actor":agent_name,"kind":"cursor.run",
                  "status":"ok" if ret==0 else "fail",
                  "run_id":run_id,"attach":zip_path,"cmd":cmd_for_log})

    return {"run_id": run_id, "attach": zip_path, "retcode": ret}
