import json
import os
import sys
import subprocess
import datetime as dt
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_config():
    """Load ops/orchestrator-config.yaml."""
    cfg_path = ROOT / "ops" / "orchestrator-config.yaml"
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8-sig") as f:
        return yaml.safe_load(f)


def load_queue(queue_path: Path):
    """Read JSONL queue file into a list of task dicts."""
    tasks = []
    if not queue_path.exists():
        raise FileNotFoundError(f"Queue file not found: {queue_path}")
    with queue_path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.lstrip("\ufeff").strip()
            if not line:
                continue
            tasks.append(json.loads(line))
    return tasks


def find_task(tasks, task_id: str):
    for t in tasks:
        if t.get("id") == task_id:
            return t
    return None


def load_agent_cfg(agent_id: str):
    """Load ops/agent-registry.yaml and return config for a specific agent."""
    registry_path = ROOT / "ops" / "agent-registry.yaml"
    if not registry_path.exists():
        # Fallback: minimal info
        return {"id": agent_id, "name": agent_id, "logs_dir": f"docs/runs/{agent_id}"}
    with registry_path.open("r", encoding="utf-8-sig") as f:
        data = yaml.safe_load(f) or {}
    agents = data.get("agents", {})
    cfg = agents.get(agent_id, {})
    if not cfg:
        return {"id": agent_id, "name": agent_id, "logs_dir": f"docs/runs/{agent_id}"}
    return cfg


def run_ps_script(path: Path):
    """Run a PowerShell script and capture stdout/stderr/exit code."""
    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(path),
    ]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, proc.stdout, proc.stderr


def write_run_report(agent_cfg, task_id: str, results, project_env: str) -> Path:
    """Write a simple Agent-3 run report markdown file."""
    agent_id = agent_cfg.get("id", "AGENT-3")
    agent_name = agent_cfg.get("name", "DevOps & Access Engineer")
    logs_dir_rel = agent_cfg.get("logs_dir", f"docs/runs/{agent_id}")
    logs_dir = ROOT / logs_dir_rel
    logs_dir.mkdir(parents=True, exist_ok=True)

    now = dt.datetime.utcnow()
    started_iso = now.isoformat(timespec="seconds") + "Z"
    # For this simple script we treat started/finished as same timestamp
    finished_iso = started_iso
    run_id = f"run-{now.strftime('%Y%m%d-%H%M%S')}"

    lines = []
    lines.append(f"# Agent Run Report – {agent_id} ({agent_name})")
    lines.append("")
    lines.append(f"- **Run ID:** {run_id}")
    lines.append(f"- **Agent:** {agent_id} – {agent_name}")
    lines.append(f"- **Started:** {started_iso}")
    lines.append(f"- **Finished:** {finished_iso}")
    lines.append(f"- **Environment:** {project_env}")
    lines.append(f"- **Tasks handled:** {task_id}")
    # Simple status: success if all return codes 0, else partial
    if all(r["exit_code"] == 0 for r in results):
        status = "success"
    elif any(r["exit_code"] != 0 for r in results):
        status = "partial"
    else:
        status = "unknown"
    lines.append(f"- **Status:** {status}")
    lines.append("")

    lines.append("## 1. Objectives")
    lines.append("")
    lines.append(
        "Run access smoke tests (scripts/smoke/*.ps1) to validate local_fs, docker, "
        "git, and other critical resources described in the Access Readiness Matrix."
    )
    lines.append("")

    lines.append("## 2. Actions Taken")
    lines.append("")
    lines.append("Executed the following PowerShell smoke scripts:")
    lines.append("")
    for r in results:
        lines.append(
            f"- `{r['name']}` – exit_code={r['exit_code']} "
            f"({'OK' if r['exit_code'] == 0 else 'FAILED'})"
        )
    lines.append("")

    lines.append("## 3. Artifacts Produced")
    lines.append("")
    lines.append(
        "- This run report file (under docs/runs for AGENT-3).\n"
        "- Console logs for each smoke script are captured in the sections below.\n"
        "- Access Readiness Matrix (docs/runbooks/access-readiness-matrix.md) "
        "should be updated manually based on these results."
    )
    lines.append("")

    lines.append("## 4. Notes & Follow-ups")
    lines.append("")
    for r in results:
        if r["exit_code"] != 0:
            lines.append(
                f"- `{r['name']}` FAILED (exit_code={r['exit_code']}) – "
                "investigate stdout/stderr below and update the Access Readiness Matrix."
            )
    if all(r["exit_code"] == 0 for r in results):
        lines.append("- All smoke scripts succeeded with exit_code 0.")
    lines.append("")

    lines.append("## 5. Smoke Test Details")
    lines.append("")
    for r in results:
        lines.append(f"### {r['name']}")
        lines.append("")
        lines.append(f"- Exit code: {r['exit_code']}")
        lines.append("")
        lines.append("**Stdout:**")
        lines.append("")
        if r["stdout"]:
            lines.append("```text")
            lines.append(r["stdout"])
            lines.append("```")
        else:
            lines.append("_(no stdout)_")
        lines.append("")
        lines.append("**Stderr:**")
        lines.append("")
        if r["stderr"]:
            lines.append("```text")
            lines.append(r["stderr"])
            lines.append("```")
        else:
            lines.append("_(no stderr)_")
        lines.append("")

    out_path = logs_dir / f"{run_id}.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def mark_task_done(task_id: str):
    """Call orchestrator_mark_task_status.py to set a task to 'done' and sync PROGRESS.md."""
    script_path = ROOT / "scripts" / "orchestrator_mark_task_status.py"
    if not script_path.exists():
        print(
            "[agent3] WARNING: orchestrator_mark_task_status.py not found; "
            "queue/PROGRESS.md will not be updated automatically."
        )
        return
    cmd = [sys.executable, str(script_path), task_id, "done"]
    subprocess.run(cmd, check=True)


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/agent3_run_access_smoke.py TASK_ID")
        print("Example: python scripts/agent3_run_access_smoke.py TASK-ACCESS-SMOKE")
        sys.exit(1)

    task_id = sys.argv[1]

    cfg = load_config()
    orch = cfg["orchestrator"]
    project = cfg.get("project", {})
    access_cfg = cfg.get("access", {})

    queue_rel = orch["queue_file"]  # e.g. "ops/queue.jsonl"
    queue_path = ROOT / queue_rel

    tasks = load_queue(queue_path)
    task = find_task(tasks, task_id)

    if not task:
        print(f"[agent3] ERROR: Task id not found in queue: {task_id}")
        sys.exit(1)

    owner = task.get("owner", "AGENT-3")
    if owner != "AGENT-3":
        print(f"[agent3] WARNING: Task {task_id} owner is {owner}, expected AGENT-3")

    # Determine smoke scripts directory
    smoke_dir_rel = access_cfg.get("smoke_scripts_dir", "scripts/smoke")
    smoke_dir = ROOT / smoke_dir_rel

    if not smoke_dir.exists():
        print(f"[agent3] ERROR: Smoke scripts directory not found: {smoke_dir}")
        sys.exit(1)

    scripts = sorted(smoke_dir.glob("smoke-*.ps1"))
    if not scripts:
        print(f"[agent3] ERROR: No smoke-*.ps1 scripts found in {smoke_dir}")
        sys.exit(1)

    print("[agent3] Running access smoke tests...")
    results = []
    for script_path in scripts:
        print(f"[agent3]  - {script_path.name} ...")
        exit_code, stdout, stderr = run_ps_script(script_path)
        results.append(
            {
                "name": script_path.name,
                "exit_code": exit_code,
                "stdout": stdout,
                "stderr": stderr,
            }
        )

    agent_cfg = load_agent_cfg("AGENT-3")
    env_name = project.get("default_env", "dev")
    report_path = write_run_report(agent_cfg, task_id, results, env_name)

    print(f"[agent3] Wrote run report: {report_path}")

    # If all tests passed, mark task as done
    if all(r["exit_code"] == 0 for r in results):
        print(f"[agent3] All smoke tests passed – marking {task_id} as done.")
        try:
            mark_task_done(task_id)
        except subprocess.CalledProcessError as e:
            print(f"[agent3] WARNING: Failed to update queue/PROGRESS via orchestrator_mark_task_status.py: {e}")
    else:
        print(
            f"[agent3] One or more smoke tests failed – NOT auto-marking {task_id} as done."
        )
        print(
            "[agent3] Please review the run report and decide whether to mark the task "
            "as review or todo using orchestrator_mark_task_status.py."
        )

    now = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    print(f"[agent3] {now} – access smoke run completed.")


if __name__ == "__main__":
    main()
