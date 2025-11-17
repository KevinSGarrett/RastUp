import json
import sys
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
    # utf-8-sig lets us ignore any BOM at the start
    with cfg_path.open("r", encoding="utf-8-sig") as f:
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


def save_queue(queue_path: Path, tasks):
    """Write tasks list back to JSONL."""
    with queue_path.open("w", encoding="utf-8") as f:
        for t in tasks:
            f.write(json.dumps(t))
            f.write("\n")


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


def update_progress_md(progress_path: Path, tasks):
    """
    Update docs/PROGRESS.md checkboxes based on queue status.

    - Tasks with status == 'done' -> '- [x] TASK-ID ...'
    - All other statuses        -> '- [ ] TASK-ID ...'
    """
    if not progress_path.exists():
        # If there's no PROGRESS.md yet, just skip with a notice.
        print(f"[orchestrator] WARNING: Progress file not found: {progress_path}")
        return

    text = progress_path.read_text(encoding="utf-8-sig")

    # Build a mapping from id -> status
    status_by_id = {}
    for t in tasks:
        tid = t.get("id")
        if not tid:
            continue
        status_by_id[tid] = str(t.get("status", "")).lower()

    # For each known task id, ensure checkbox matches 'done' vs not done
    for tid, status in status_by_id.items():
        done_pattern = f"- [x] {tid}"
        todo_pattern = f"- [ ] {tid}"

        if status == "done":
            # Prefer checked
            if todo_pattern in text:
                text = text.replace(todo_pattern, done_pattern)
        else:
            # Prefer unchecked
            if done_pattern in text:
                text = text.replace(done_pattern, todo_pattern)

    progress_path.write_text(text, encoding="utf-8")
    print(f"[orchestrator] Updated progress checkboxes in: {progress_path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python scripts/orchestrator_mark_task_status.py TASK_ID STATUS")
        print("Example: python scripts/orchestrator_mark_task_status.py TASK-NT-INGEST done")
        sys.exit(1)

    task_id = sys.argv[1]
    new_status = sys.argv[2].lower()

    allowed = {"todo", "doing", "review", "done"}
    if new_status not in allowed:
        print(f"[orchestrator] ERROR: status must be one of {sorted(allowed)}")
        sys.exit(1)

    cfg = load_config()
    orch = cfg["orchestrator"]

    queue_rel = orch["queue_file"]  # e.g. "ops/queue.jsonl"
    queue_path = ROOT / queue_rel

    progress_rel = orch.get("progress_file", "docs/PROGRESS.md")
    progress_path = ROOT / progress_rel

    tasks = load_queue(queue_path)
    summary_before = summarize_queue(tasks)

    found = False
    for t in tasks:
        if t.get("id") == task_id:
            t["status"] = new_status
            found = True
            break

    if not found:
        print(f"[orchestrator] ERROR: Task id not found in queue: {task_id}")
        sys.exit(1)

    save_queue(queue_path, tasks)
    summary_after = summarize_queue(tasks)

    # Update PROGRESS.md checkboxes
    update_progress_md(progress_path, tasks)

    now = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    print(f"[orchestrator] {now}")
    print(f"[orchestrator] Updated task {task_id} → status='{new_status}'")
    print(f"[orchestrator] Queue summary before: {summary_before}")
    print(f"[orchestrator] Queue summary after:  {summary_after}")


if __name__ == "__main__":
    main()
