#!/usr/bin/env python
"""
Project Orchestrator — Autopilot loop that drives 4 Cursor agents via CLI.

You start it, you stop it.
It figures out:
- which WBS task is next (from ops/queue.jsonl)
- which Cursor agent (AGENT-1..4) owns it (from ops/agent-registry.yaml)
- which agent prompt to use (from docs/orchestrator/agent-prompts/...)
- updates docs/PROGRESS.md so you always see % complete
- writes a small state file for restart awareness.

Cursor details (models, MAX mode, plugins, logging, tests, run reports, etc.)
are handled INSIDE the agent prompts. This script just wires everything together
and calls the Cursor CLI.

Debug mode:
- Controlled via ops/orchestrator-config.yaml -> safety.debug_mode or safety.dry_run_only
- When debug mode is ON:
  * Cursor commands are PRINTED, not executed
  * Task status still flips to "doing" only if you want (you can change that if needed)
"""

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None  # checked at runtime


# ---------------------------------------------------------------------------
# Fixed repo root (per your setup)
# ---------------------------------------------------------------------------

REPO_ROOT = Path(r"C:\RastUp\RastUp").resolve()
OPS_DIR = REPO_ROOT / "ops"
DOCS_DIR = REPO_ROOT / "docs"
STATE_DIR = DOCS_DIR / "orchestrator" / "state"
STATE_FILE = STATE_DIR / "last-run.json"


# ---------------------------------------------------------------------------
# Config dataclasses
# ---------------------------------------------------------------------------

@dataclass
class CursorConfig:
    """Subset of orchestrator-config.yaml relevant to Cursor CLI."""
    cli_path: str = "cursor"          # e.g. "cursor" in PATH or full path to cursor.exe
    workspace_root: Path = REPO_ROOT  # repo root / workspace root
    default_profile: Optional[str] = None  # optional CURSOR_PROFILE


@dataclass
class OrchestratorConfig:
    """Top-level orchestrator config loaded from ops/orchestrator-config.yaml."""
    raw: Dict[str, Any]
    cursor: CursorConfig
    poll_interval_seconds: int = 10
    debug_mode: bool = False  # when True: print Cursor commands, don't execute them

    @classmethod
    def load(cls, path: Path) -> "OrchestratorConfig":
        if yaml is None:
            raise RuntimeError(
                "PyYAML is required to load orchestrator-config.yaml. "
                "Install with: pip install pyyaml"
            )
        if not path.exists():
            raise FileNotFoundError(f"Missing orchestrator config: {path}")

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

        cursor_cfg = data.get("cursor", {})
        cursor = CursorConfig(
            cli_path=cursor_cfg.get("cli_path", "cursor"),
            workspace_root=Path(cursor_cfg.get("workspace_root", str(REPO_ROOT))),
            default_profile=cursor_cfg.get("default_profile"),
        )

        poll = int(data.get("poll_interval_seconds", 10))

        safety_cfg = data.get("safety", {})
        # Allow either name: debug_mode or dry_run_only
        debug_mode = bool(
            safety_cfg.get("debug_mode")
            or safety_cfg.get("dry_run_only")
        )

        return cls(
            raw=data,
            cursor=cursor,
            poll_interval_seconds=poll,
            debug_mode=debug_mode,
        )


@dataclass
class AgentConfig:
    """
    One Cursor agent, as defined in ops/agent-registry.yaml.

    Expected minimal schema per agent (keys are case-sensitive):

      - id: "AGENT-1"
      - role: "Bootstrap & DevOps"
      - prompt_path: "docs/orchestrator/agent-prompts/agent-1-bootstrap-devops.md"
      - default_model: "gpt-5-codex"
      - max_mode: true|false
      - cursor_profile: "default" (optional)
      - scopes: ["**/infra/**", ...] (optional)
    """
    id: str
    role: str
    prompt_path: Path
    default_model: str
    max_mode: bool = False
    cursor_profile: Optional[str] = None
    scopes: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def load_agent_registry(path: Path) -> Dict[str, AgentConfig]:
    """
    Load ops/agent-registry.yaml and return mapping id->AgentConfig.

    For backward compatibility, if 'id' is missing we fall back to 'name'.
    """
    if yaml is None:
        raise RuntimeError(
            "PyYAML is required to load agent-registry.yaml. "
            "Install with: pip install pyyaml"
        )
    if not path.exists():
        raise FileNotFoundError(f"Missing agent registry: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    agents_cfg: Dict[str, AgentConfig] = {}

    for entry in data.get("agents", []):
        agent_id = entry.get("id") or entry.get("name")
        if not agent_id:
            continue

        prompt_rel = entry.get("prompt_path")
        if not prompt_rel:
            raise ValueError(
                f"agent {agent_id} is missing prompt_path in ops/agent-registry.yaml"
            )

        prompt_path = REPO_ROOT / prompt_rel

        cfg = AgentConfig(
            id=agent_id,
            role=entry.get("role", ""),
            prompt_path=prompt_path,
            default_model=entry.get("default_model") or entry.get("model", ""),
            max_mode=bool(entry.get("max_mode", False)),
            cursor_profile=entry.get("cursor_profile"),
            scopes=list(entry.get("scopes", []) or []),
            raw=entry,
        )
        agents_cfg[agent_id] = cfg

    return agents_cfg


# ---------------------------------------------------------------------------
# Task / queue helpers
# ---------------------------------------------------------------------------

@dataclass
class Task:
    id: str
    title: str
    owner: str
    status: str
    weight: float
    dependencies: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def load_queue(path: Path) -> List[Task]:
    tasks: List[Task] = []
    if not path.exists():
        return tasks

    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)
        t = Task(
            id=data["id"],
            title=data.get("title", ""),
            owner=data.get("owner", ""),
            status=data.get("status", "todo"),
            weight=float(data.get("weight", 0.0)),
            dependencies=list(data.get("dependencies", []) or []),
            raw=data,
        )
        tasks.append(t)
    return tasks


def save_queue(path: Path, tasks: List[Task]) -> None:
    lines: List[str] = []
    for t in tasks:
        data = dict(t.raw)
        data["id"] = t.id
        data["title"] = t.title
        data["owner"] = t.owner
        data["status"] = t.status
        data["weight"] = t.weight
        data["dependencies"] = t.dependencies
        lines.append(json.dumps(data, ensure_ascii=False))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def deps_done(task: Task, tasks_by_id: Dict[str, Task]) -> bool:
    """Return True if all dependencies for this task are status=='done'."""
    for dep in task.dependencies:
        dep_task = tasks_by_id.get(dep)
        if not dep_task or dep_task.status != "done":
            return False
    return True


def parse_phase(task_id: str) -> int:
    """
    Extract numeric WBS phase from id like 'WBS-4.1'.
    Returns a large number if not parseable so such tasks sort last.
    """
    m = re.match(r"WBS-(\d+)", task_id)
    if not m:
        return 9999
    try:
        return int(m.group(1))
    except ValueError:
        return 9999


def choose_next_task(tasks: List[Task]) -> Optional[Task]:
    """
    Pick the next runnable task:

    - status == "todo"
    - owner starts with "AGENT-" (so PO-only tasks are not auto-run yet)
    - all dependencies are "done"
    - sort by (phase asc, weight desc, id asc)
    """
    tasks_by_id = {t.id: t for t in tasks}
    candidates: List[Task] = []

    for t in tasks:
        if t.status != "todo":
            continue
        if not t.owner.startswith("AGENT-"):
            continue
        if not deps_done(t, tasks_by_id):
            continue
        candidates.append(t)

    if not candidates:
        return None

    def sort_key(t: Task):
        return (parse_phase(t.id), -t.weight, t.id)

    candidates.sort(key=sort_key)
    return candidates[0]


# ---------------------------------------------------------------------------
# Progress computation
# ---------------------------------------------------------------------------

def compute_progress(tasks: List[Task]) -> Dict[str, Any]:
    """
    Compute overall and per-phase progress from queue weights.

    Simple model:
    - Overall % = sum(weight for status=='done') / sum(all weights)
    - Per-phase % = same but grouped by WBS phase.

    (CI / agents still enforce test gates & concordance; this is just the gauge.)
    """
    total_weight = sum(t.weight for t in tasks)
    done_weight = sum(t.weight for t in tasks if t.status == "done")
    overall_pct = (done_weight / total_weight * 100.0) if total_weight > 0 else 0.0

    phases: Dict[int, Dict[str, Any]] = {}
    for t in tasks:
        phase = parse_phase(t.id)
        if phase not in phases:
            phases[phase] = {
                "total_weight": 0.0,
                "done_weight": 0.0,
                "owner": t.owner,
            }
        phases[phase]["total_weight"] += t.weight
        if t.status == "done":
            phases[phase]["done_weight"] += t.weight

    phase_rows: List[Dict[str, Any]] = []
    for phase, info in sorted(phases.items(), key=lambda kv: kv[0]):
        tw = info["total_weight"]
        dw = info["done_weight"]
        pct = (dw / tw * 100.0) if tw > 0 else 0.0
        phase_rows.append(
            {
                "phase": phase,
                "weight": round(tw, 4),
                "pct_done": pct,
                "owner": info["owner"],
            }
        )

    return {"overall": overall_pct, "phases": phase_rows}


def update_progress_md(path: Path, tasks: List[Task]) -> float:
    """
    Regenerate docs/PROGRESS.md from the current queue.jsonl.

    It overwrites PROGRESS.md each time; this file is *meant* to be generated.
    """
    stats = compute_progress(tasks)
    overall = stats["overall"]
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines: List[str] = []
    lines.append("# Project Progress")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Overall completion: {overall:.2f}%")
    lines.append(f"- Last update: {ts}")
    lines.append("")
    lines.append("## Phase Breakdown (from /ops/queue.jsonl)")
    lines.append("")
    lines.append("| Phase | Total Weight | % Done | Owner |")
    lines.append("|-------|--------------|--------|-------|")
    for row in stats["phases"]:
        lines.append(
            f"| {row['phase']} | {row['weight']:.4f} | {row['pct_done']:.2f}% | {row['owner']} |"
        )
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return overall


# ---------------------------------------------------------------------------
# State file (for "where did we leave off?")
# ---------------------------------------------------------------------------

def write_last_state(
    overall_completion: float,
    task: Optional[Task] = None,
    agent_cfg: Optional[AgentConfig] = None,
    return_code: Optional[int] = None,
) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "overall_completion": round(overall_completion, 2),
        "task_id": task.id if task else None,
        "task_title": task.title if task else None,
        "task_owner": task.owner if task else None,
        "agent_id": agent_cfg.id if agent_cfg else None,
        "agent_role": agent_cfg.role if agent_cfg else None,
        "return_code": return_code,
    }
    STATE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Cursor invocation
# ---------------------------------------------------------------------------

def run_cursor_agent(
    orch_cfg: OrchestratorConfig,
    agent_cfg: AgentConfig,
    task: Task,
) -> int:
    """
    Invoke Cursor CLI for a single agent + task.

    IMPORTANT:
    - You MUST adapt the actual Cursor CLI invocation to match your environment.
    - This function supports debug_mode: when True, it only prints the command.

    Example pattern (adjust to your real CLI):

        cursor agents run ^
          --workspace C:\\RastUp\\RastUp ^
          --prompt-file docs/orchestrator/agent-prompts/agent-1-bootstrap-devops.md ^
          --task-id WBS-1.1
    """
    env = os.environ.copy()
    # Context variables for the agent prompts / environment
    env["ORCH_TASK_ID"] = task.id
    env["ORCH_TASK_OWNER"] = task.owner
    env["ORCH_TASK_TITLE"] = task.title
    env["ORCH_AGENT_ID"] = agent_cfg.id
    env["ORCH_AGENT_ROLE"] = agent_cfg.role
    env["ORCH_AGENT_PROMPT_PATH"] = str(agent_cfg.prompt_path)
    env["ORCH_DEFAULT_MODEL"] = agent_cfg.default_model
    env["ORCH_MAX_MODE"] = "1" if agent_cfg.max_mode else "0"
    env["ORCH_DEBUG_MODE"] = "1" if orch_cfg.debug_mode else "0"

    if agent_cfg.cursor_profile or orch_cfg.cursor.default_profile:
        env["CURSOR_PROFILE"] = (
            agent_cfg.cursor_profile or orch_cfg.cursor.default_profile or ""
        )

    cmd = [
        orch_cfg.cursor.cli_path,
        # !!! ADAPT THESE SUBCOMMANDS/FLAGS TO YOUR REAL CURSOR CLI !!!
        "agents",
        "run",
        "--workspace",
        str(orch_cfg.cursor.workspace_root),
        "--prompt-file",
        str(agent_cfg.prompt_path),
        "--task-id",
        task.id,
    ]

    print(f"[orchestrator] launching Cursor for {task.id} -> {agent_cfg.id}")
    print("  command:", " ".join(cmd))

    if orch_cfg.debug_mode:
        print("[orchestrator] DEBUG MODE is ON — not executing Cursor CLI.")
        return 0

    try:
        completed = subprocess.run(cmd, env=env, check=False)
        return completed.returncode
    except FileNotFoundError:
        print(
            f"[orchestrator][ERROR] Cursor CLI not found at '{orch_cfg.cursor.cli_path}'. "
            "Update ops/orchestrator-config.yaml cursor.cli_path or adjust run_cursor_agent().",
            file=sys.stderr,
        )
        return 127


def mark_task_doing(queue_path: Path, tasks: List[Task], task: Task) -> None:
    """Flip a task from todo -> doing before we hand it to the agent."""
    for t in tasks:
        if t.id == task.id:
            t.status = "doing"
            t.raw["status"] = "doing"
            break
    save_queue(queue_path, tasks)


# ---------------------------------------------------------------------------
# Main orchestrator logic (one tick vs loop)
# ---------------------------------------------------------------------------

def orchestrator_tick(
    orch_cfg: OrchestratorConfig,
    agents: Dict[str, AgentConfig],
) -> None:
    queue_path = OPS_DIR / "queue.jsonl"
    progress_path = DOCS_DIR / "PROGRESS.md"

    tasks = load_queue(queue_path)
    if not tasks:
        print("[orchestrator] no tasks in ops/queue.jsonl yet.")
        write_last_state(overall_completion=0.0, task=None, agent_cfg=None, return_code=None)
        return

    overall = update_progress_md(progress_path, tasks)
    print(f"[orchestrator] current project completion: {overall:.2f}%")
    print(f"Project completion: {overall:.2f}%")

    next_task = choose_next_task(tasks)
    if not next_task:
        print(
            "[orchestrator] no runnable tasks "
            "(status=='todo', owner=='AGENT-*', deps done)."
        )
        write_last_state(overall_completion=overall, task=None, agent_cfg=None, return_code=None)
        return

    agent_cfg = agents.get(next_task.owner)
    if not agent_cfg:
        print(
            f"[orchestrator][WARN] no agent-registry entry for owner "
            f"'{next_task.owner}'. Skipping this task.",
            file=sys.stderr,
        )
        write_last_state(overall_completion=overall, task=next_task, agent_cfg=None, return_code=None)
        return

    print(
        f"[orchestrator] dispatching {next_task.id} "
        f"('{next_task.title}') to {agent_cfg.id} ({agent_cfg.role})"
    )

    # Mark as doing before we hand off to Cursor
    mark_task_doing(queue_path, tasks, next_task)

    rc = run_cursor_agent(orch_cfg, agent_cfg, next_task)
    if rc != 0:
        print(
            f"[orchestrator][WARN] Cursor CLI exited with code {rc} "
            f"for task {next_task.id}. "
            "Task status left as 'doing'; investigate via run reports "
            "and/or run the Recovery SOP.",
            file=sys.stderr,
        )
    else:
        print(
            f"[orchestrator] completed agent run for {next_task.id}. "
            "Per the agent prompts, the agent itself should update "
            "ops/queue.jsonl to 'review' or 'done' and write its "
            "run report + attach pack."
        )

    # Re-read tasks after agent run to get updated completion %
    updated_tasks = load_queue(queue_path)
    new_overall = update_progress_md(progress_path, updated_tasks)
    print(f"[orchestrator] updated project completion: {new_overall:.2f}%")
    print(f"Project completion: {new_overall:.2f}%")

    write_last_state(
        overall_completion=new_overall,
        task=next_task,
        agent_cfg=agent_cfg,
        return_code=rc,
    )


def orchestrator_loop() -> None:
    cfg_path = OPS_DIR / "orchestrator-config.yaml"
    orch_cfg = OrchestratorConfig.load(cfg_path)
    agents = load_agent_registry(OPS_DIR / "agent-registry.yaml")

    print("[orchestrator] starting autopilot loop")
    print(f"  repo root: {REPO_ROOT}")
    print(f"  queue:     {OPS_DIR / 'queue.jsonl'}")
    print(f"  progress:  {DOCS_DIR / 'PROGRESS.md'}")
    print(f"  poll:      {orch_cfg.poll_interval_seconds}s")
    print(f"  debug:     {orch_cfg.debug_mode}")

    try:
        while True:
            orchestrator_tick(orch_cfg, agents)
            time.sleep(orch_cfg.poll_interval_seconds)
    except KeyboardInterrupt:
        print("\n[orchestrator] received Ctrl+C, exiting cleanly.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Usage:
    #   python orchestrator\main.py          -> loop mode (autopilot)
    #   python orchestrator\main.py loop     -> same as above
    #   python orchestrator\main.py tick     -> single cycle (good for testing)
    mode = "loop"
    if len(sys.argv) > 1:
        mode = sys.argv[1].strip().lower()

    if mode == "tick":
        cfg_path = OPS_DIR / "orchestrator-config.yaml"
        orch_cfg = OrchestratorConfig.load(cfg_path)
        agents = load_agent_registry(OPS_DIR / "agent-registry.yaml")
        print("[orchestrator] running a single tick")
        print(f"  debug: {orch_cfg.debug_mode}")
        orchestrator_tick(orch_cfg, agents)
    else:
        orchestrator_loop()
