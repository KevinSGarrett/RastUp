from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Literal, Dict

# Treat repo root as one level above /orchestrator
REPO_ROOT = Path(__file__).resolve().parents[1]
WBS_INDEX_PATH = REPO_ROOT / "docs" / "blueprints" / "wbs-index.json"
QUEUE_PATH = REPO_ROOT / "ops" / "queue.jsonl"
PROGRESS_PATH = REPO_ROOT / "docs" / "PROGRESS.md"

Status = Literal["todo", "in_progress", "review", "done", "blocked"]


@dataclass
class WbsItem:
    id: str
    root: str
    source: str
    title: str
    line: str


@dataclass
class QueueItem:
    id: str
    root: str
    source: str
    title: str
    status: Status
    agent: Optional[str]
    priority: int
    created_at: str
    updated_at: str
    nt_refs: List[str]
    td_refs: List[str]


def _utc_now() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def load_wbs_index() -> List[WbsItem]:
    if not WBS_INDEX_PATH.exists():
        raise SystemExit(
            f"[director] wbs-index.json not found at {WBS_INDEX_PATH}. "
            "Run `python -m orchestrator.wbs_indexer` first."
        )
    data = json.loads(WBS_INDEX_PATH.read_text(encoding="utf-8"))
    items: List[WbsItem] = []
    for raw in data.get("items", []):
        items.append(
            WbsItem(
                id=raw["id"],
                root=raw.get("root") or raw["id"].split(".", 1)[0],
                source=raw.get("source", "NT"),
                title=raw.get("title") or raw.get("line") or raw["id"],
                line=raw.get("line", ""),
            )
        )
    return items


def seed_queue(overwrite: bool = False, roots: Optional[List[str]] = None) -> int:
    items = load_wbs_index()
    if roots:
        wanted = set(roots)
        items = [i for i in items if i.root in wanted]

    if not items:
        print("[director] No WBS items matched the requested roots.", file=sys.stderr)
        return 1

    if QUEUE_PATH.exists() and not overwrite:
        print(f"[director] {QUEUE_PATH} already exists. Use --overwrite to rebuild.", file=sys.stderr)
        return 1

    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    now = _utc_now()

    with QUEUE_PATH.open("w", encoding="utf-8") as f:
        for idx, item in enumerate(items):
            q = QueueItem(
                id=item.id,
                root=item.root,
                source=item.source,
                title=item.title,
                status="todo",
                agent=None,
                priority=100 + idx,  # simple priority for now
                created_at=now,
                updated_at=now,
                nt_refs=[],
                td_refs=[],
            )
            f.write(json.dumps(asdict(q), ensure_ascii=False) + "\n")

    print(f"[director] wrote {len(items)} queue items to {QUEUE_PATH}")
    # Also refresh PROGRESS.md
    update_progress_from_queue()
    return 0


def load_queue() -> List[QueueItem]:
    if not QUEUE_PATH.exists():
        return []
    items: List[QueueItem] = []
    with QUEUE_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            items.append(
                QueueItem(
                    id=raw["id"],
                    root=raw["root"],
                    source=raw.get("source", "NT"),
                    title=raw.get("title", raw["id"]),
                    status=raw.get("status", "todo"),
                    agent=raw.get("agent"),
                    priority=int(raw.get("priority", 100)),
                    created_at=raw.get("created_at", _utc_now()),
                    updated_at=raw.get("updated_at", _utc_now()),
                    nt_refs=list(raw.get("nt_refs", [])),
                    td_refs=list(raw.get("td_refs", [])),
                )
            )
    return items


def dump_queue(items: List[QueueItem]) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with QUEUE_PATH.open("w", encoding="utf-8") as f:
        for q in items:
            f.write(json.dumps(asdict(q), ensure_ascii=False) + "\n")


def status_counts(items: List[QueueItem]) -> Dict[str, int]:
    counts: Dict[str, int] = {s: 0 for s in ["todo", "in_progress", "review", "done", "blocked"]}
    for q in items:
        counts[q.status] = counts.get(q.status, 0) + 1
    return counts


def update_progress_from_queue() -> None:
    items = load_queue()
    total = len(items)
    counts = status_counts(items)
    done = counts.get("done", 0)
    pct = int(round((done / total) * 100)) if total else 0

    by_root: Dict[str, Dict[str, int]] = {}
    for q in items:
        root_stats = by_root.setdefault(
            q.root, {s: 0 for s in ["todo", "in_progress", "review", "done", "blocked"]}
        )
        root_stats[q.status] += 1

    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# Orchestrator Progress")
    lines.append("")
    lines.append(f"- Total WBS items: {total}")
    lines.append(f"- Done: {done}")
    lines.append(f"- Overall completion: {pct}%")
    lines.append(f"- Last updated (UTC): {_utc_now()}")
    lines.append("")
    lines.append("## Status by root")
    lines.append("")
    for root, stats in sorted(by_root.items()):
        root_total = sum(stats.values())
        root_done = stats.get("done", 0)
        root_pct = int(round((root_done / root_total) * 100)) if root_total else 0
        lines.append(f"### {root}")
        lines.append(f"- Items: {root_total}")
        lines.append(f"- Done: {root_done}")
        lines.append(f"- Completion: {root_pct}%")
        lines.append(
            f"- Breakdown: todo={stats['todo']}, in_progress={stats['in_progress']}, "
            f"review={stats['review']}, done={stats['done']}, blocked={stats['blocked']}"
        )
        lines.append("")

    PROGRESS_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[director] updated {PROGRESS_PATH}")


def show_summary() -> None:
    items = load_queue()
    total = len(items)
    counts = status_counts(items)
    done = counts.get("done", 0)
    pct = int(round((done / total) * 100)) if total else 0
    print(f"[director] Queue items: {total}  done={done}  completion={pct}%")
    for s in ["todo", "in_progress", "review", "done", "blocked"]:
        print(f"  {s:12s}: {counts.get(s, 0)}")


def next_task(agent: Optional[str] = None, root: Optional[str] = None) -> int:
    items = load_queue()
    # simple selection: earliest TODO by priority
    candidates = [q for q in items if q.status == "todo"]
    if agent:
        candidates = [q for q in candidates if (q.agent is None or q.agent == agent)]
    if root:
        candidates = [q for q in candidates if q.root == root]
    if not candidates:
        print("[director] No TODO items available for the given filters.", file=sys.stderr)
        return 1
    candidates.sort(key=lambda q: q.priority)
    task = candidates[0]
    print(json.dumps(asdict(task), ensure_ascii=False, indent=2))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m orchestrator.director",
        description="Orchestrator core CLI (queue + progress).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_seed = sub.add_parser(
        "seed-queue",
        help="Create ops/queue.jsonl from docs/blueprints/wbs-index.json",
    )
    p_seed.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing queue.jsonl if present",
    )
    p_seed.add_argument(
        "--roots",
        nargs="*",
        help=(
            "Optional list of WBS roots to include (e.g., WBS-1 WBS-2 WBS-4). "
            "If omitted, include all roots."
        ),
    )

    sub.add_parser("show-summary", help="Print a short summary of queue status")

    p_next = sub.add_parser(
        "next-task",
        help="Show next TODO task (JSON) without mutating the queue",
    )
    p_next.add_argument("--agent", help="Optional agent filter (AGENT-1..AGENT-4)")
    p_next.add_argument("--root", help="Optional WBS root filter, e.g. WBS-1")

    sub.add_parser(
        "rebuild-progress",
        help="Rebuild docs/PROGRESS.md from the current queue",
    )

    args = parser.parse_args(argv)

    if args.cmd == "seed-queue":
        return seed_queue(overwrite=args.overwrite, roots=args.roots)
    if args.cmd == "show-summary":
        show_summary()
        return 0
    if args.cmd == "next-task":
        return next_task(agent=args.agent, root=args.root)
    if args.cmd == "rebuild-progress":
        update_progress_from_queue()
        return 0

    parser.error("Unhandled command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
