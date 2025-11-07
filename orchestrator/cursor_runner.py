import subprocess, os, uuid, zipfile, time, platform
from orchestrator.logger_jsonl import append_event

def run_cursor(repo_path:str, prompt:str, cursor_cli:str="cursor", agent_name:str="AGENT-1"):
    run_id = f"{int(time.time())}-{uuid.uuid4().hex[:6]}"
    attach_dir = os.path.join("docs","orchestrator","from-agents",agent_name)
    os.makedirs(attach_dir, exist_ok=True)
    log_txt = os.path.join(attach_dir, f"run-{run_id}.log")

    repo_abs = os.path.abspath(repo_path)
    is_windows = platform.system().lower().startswith("win")

    # Safe quote for prompt (very simple)
    prompt_q = prompt.replace('"', "'")

    # Build command
    if is_windows and cursor_cli.lower().endswith((".cmd",".bat")):
        cmdline = f'"{cursor_cli}" agent --headless --project "{repo_abs}" --prompt "{prompt_q}"'
        shell = True
        cmd_for_log = cmdline
    else:
        cmd = [cursor_cli, "agent", "--headless", "--project", repo_abs, "--prompt", prompt_q]
        cmdline = None
        shell = False
        cmd_for_log = " ".join(cmd)

    # Open log and write a START line, then stream tool output
    with open(log_txt, "w", encoding="utf-8") as lf:
        lf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] INFO start: {agent_name} run_id={run_id}\n")
        lf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] INFO cmd: {cmd_for_log}\n")
        lf.flush()

        # stream both stdout & stderr into our log file
        if shell:
            proc = subprocess.Popen(cmdline, cwd=repo_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        else:
            proc = subprocess.Popen(cmd, cwd=repo_abs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in proc.stdout:
            # keep everything for now; if you want to suppress Electron option warnings, uncomment next two lines
            # if "not in the list of known options" in line:
            #     continue
            lf.write(line)

        ret = proc.wait()
        lf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] INFO finish: exit_code={ret}\n")

    zip_path = os.path.join(attach_dir, f"run-{run_id}-attach.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(log_txt, arcname=os.path.basename(log_txt))

    append_event({"actor":agent_name,"kind":"cursor.run","status":"ok" if ret==0 else "fail",
                  "run_id":run_id,"attach":zip_path,"cmd":cmd_for_log})

    return {"run_id": run_id, "attach": zip_path, "retcode": ret}
