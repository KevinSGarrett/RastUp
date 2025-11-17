import json
import uuid
import datetime as dt
from pathlib import Path

import yaml

# Repo root: this file lives in scripts/, so parents[1] is the repo root
ROOT = Path(__file__).resolve().parents[1]


def load_config():
    """Load ops/orchestrator-config.yaml."""
    cfg_path = ROOT / "ops" / "orchestrator-config.yaml"
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8-sig") as f:
        # utf-8-sig lets us ignore any BOM at the start
        return yaml.safe_load(f)


def load_queue(queue_path: Path):
    """Read JSONL queue file into a list of task dicts."""
    tasks = []
    if not queue_path.exists():
        raise FileNotFoundError(f"Queue file not found: {queue_path}")
    # utf-8-sig so a BOM at the start of the file does NOT break json.loads
    with queue_path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            # Strip BOM if it somehow appears on a line, then whitespace
            line = line.lstrip("\ufeff").strip()
            if not line:
                continue
            tasks.append(json.loads(line))
    return tasks


def summarize_queue(tasks):
    """Count tasks by status."""
    summary = {"todo": 0, "doing": 0, "review": 0, "done": 0, "_other": 0}
    for t in tasks:
        status = str(t.get("status", "")).lower()
        if status in summary:
            summary[status] += 1
        else:
            summary["_other"] += 1
    return summary


def render_template(template_path: Path, context: dict) -> str:
    """Very simple {{ key }} replacement."""
    text = template_path.read_text(encoding="utf-8-sig")
    for key, value in context.items():
        placeholder = "{{ " + key + " }}"
        if isinstance(value, (list, tuple)):
            value = ", ".join(str(v) for v in value)
        text = text.replace(placeholder, str(value))
    return text


def main():
    cfg = load_config()
    orch = cfg["orchestrator"]
    project = cfg.get("project", {})
    run_reports_cfg = cfg.get("run_reports", {})

    # Queue path (repo-relative from orchestrator-config.yaml)
    queue_rel = orch["queue_file"]  # e.g. "ops/queue.jsonl"
    queue_path = ROOT / queue_rel

    # Runs directory: docs/runs/orchestrator by default
    runs_base_rel = run_reports_cfg.get(
        "base_dir",
        orch.get("runs_dir", "docs/runs"),
    )
    runs_root = ROOT / runs_base_rel
    runs_dir = runs_root / "orchestrator"
    runs_dir.mkdir(parents=True, exist_ok=True)

    # Load queue & summarize
    tasks = load_queue(queue_path)
    summary = summarize_queue(tasks)

    # Timestamps & run ID
    now = dt.datetime.utcnow()
    now_iso = now.isoformat(timespec="seconds") + "Z"
    run_id = f"run-{now.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    # Template path for orchestrator run report
    tmpl_rel = run_reports_cfg.get(
        "orchestrator_template",
        "docs/templates/orchestrator-run-report.md",
    )
    tmpl_path = ROOT / tmpl_rel

    context = {
        "run_id": run_id,
        "started_at": now_iso,
        "finished_at": now_iso,
        "env": project.get("default_env", "dev"),
        "mode": "manual",
        "queue_total": len(tasks),
        "queue_todo_count": summary["todo"],
        "queue_doing_count": summary["doing"],
        "queue_review_count": summary["review"],
        "queue_done_count": summary["done"],
        "agent_activity": "No agent runs executed yet – this is just a dry-run queue snapshot.",
        "locks_and_recovery": "Lock monitoring not implemented yet.",
        "errors": "None in this dry-run.",
        "notes": "Initial test of the RastUp orchestrator skeleton.",
    }

    report_text = render_template(tmpl_path, context)

    out_path = runs_dir / f"{run_id}.md"
    out_path.write_text(report_text, encoding="utf-8")

    print(f"[orchestrator] Wrote run report to: {out_path}")
    print(
        f"[orchestrator] Queue: {len(tasks)} tasks "
        f"(todo={summary['todo']}, doing={summary['doing']}, "
        f"review={summary['review']}, done={summary['done']}, other={summary['_other']})"
    )


if __name__ == "__main__":
    main()
