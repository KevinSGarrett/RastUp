# orchestrator/llm.py
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any, List, Optional

import textwrap
import requests  # install into the Windows venv: pip install requests

REPO_ROOT = Path(os.environ.get("REPO_ROOT", r"C:\RastUp\RastUp")).resolve()
DOCS_DIR = REPO_ROOT / "docs"
OPS_DIR = REPO_ROOT / "ops"


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def _summarize_queue() -> str:
    """Summarize WBS-1.* and WBS-2.* items from ops/queue.jsonl."""
    queue_path = OPS_DIR / "queue.jsonl"
    items = _load_jsonl(queue_path)
    lines: List[str] = []
    for item in items:
        wbs_id = str(item.get("id") or "")
        if not (wbs_id.startswith("WBS-1.") or wbs_id.startswith("WBS-2.")):
            continue
        line = (
            f"- {wbs_id}: {item.get('title', '').strip()} "
            f"(status={item.get('status', 'todo')}, owner={item.get('owner', '?')})"
        )
        lines.append(line)
    if not lines:
        return "(no explicit WBS-1.* or WBS-2.* items found in ops/queue.jsonl)"
    return "\n".join(lines)


def _progress_excerpt(max_chars: int = 2000) -> str:
    p = DOCS_DIR / "PROGRESS.md"
    if not p.exists():
        return "(docs/PROGRESS.md not present yet)"
    text = p.read_text(encoding="utf-8", errors="ignore")
    if len(text) > max_chars:
        return text[:max_chars] + "\n… (truncated)"
    return text


def _call_openai(system_prompt: str, user_prompt: str) -> Tuple[str, str, Dict[str, Any]]:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set in the environment")

    model = os.environ.get("RU_OPENAI_MODEL", "gpt-4.1")
    url = "https://api.openai.com/v1/chat/completions"
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.4,
        "max_tokens": 1500,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, headers=headers, json=body, timeout=90)
    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise RuntimeError(f"OpenAI API error {resp.status_code}: {detail}")
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage") or {}
    return content, model, usage


def _call_anthropic(system_prompt: str, user_prompt: str) -> Tuple[str, str, Dict[str, Any]]:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set in the environment")

    model = os.environ.get("RU_ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
    url = "https://api.anthropic.com/v1/messages"
    body = {
        "model": model,
        "max_tokens": 1500,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_prompt},
        ],
    }
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    resp = requests.post(url, headers=headers, json=body, timeout=90)
    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise RuntimeError(f"Anthropic API error {resp.status_code}: {detail}")
    data = resp.json()
    blocks = data.get("content") or []
    text_parts: List[str] = []
    for block in blocks:
        if isinstance(block, dict) and block.get("type") == "text":
            text_parts.append(block.get("text", ""))
    content = "\n".join(text_parts) if text_parts else str(data)
    usage = data.get("usage") or {}
    return content, model, usage


def generate_llm_plan(user_request: Optional[str] = None) -> Tuple[str, str, Dict[str, Any]]:
    """
    Generate a 3–5 day plan for WBS-1.* and WBS-2.* and save it under docs/runbooks/.
    Returns (path_str, model_used, usage_dict).
    """
    docs = DOCS_DIR
    docs.mkdir(parents=True, exist_ok=True)
    runbooks_dir = docs / "runbooks"
    runbooks_dir.mkdir(parents=True, exist_ok=True)

    queue_summary = _summarize_queue()
    progress = _progress_excerpt()

    system_prompt = textwrap.dedent(
        """
        You are the Project Orchestrator for the RastUp project.

        Goal:
        - Plan the next 3–5 days of work specifically for WBS-1.* (Dev platform & infra bootstrap)
          and WBS-2.* (Architecture & ADRs), using the queue items and current progress.

        Constraints:
        - Assume work is executed by four Cursor agents (AGENT-1..AGENT-4) plus this Orchestrator.
        - Respect non-interference: each task should have a clear owner and scope.
        - Optimize for steady progress, not heroics: realistic daily slices.
        - For each day, list:
          * concrete tasks (with WBS ids),
          * expected artifacts (file paths or PRs),
          * tests or checks to run,
          * any access prerequisites.

        Output format:
        - Markdown.
        - Top-level sections: Day 1, Day 2, Day 3, (optionally Day 4, Day 5).
        - Under each day, bullet lists grouped by agent (PO / AGENT-1..4).
        - Reference WBS ids and any NT/TD ids if you can infer them from context.
        """
    ).strip()

    if not user_request:
        user_request = (
            "Plan the next 3–5 days of work for WBS-1.* and WBS-2.* "
            "based on the project queue and progress."
        )

    user_prompt = textwrap.dedent(
        f"""
        High-level request:
        {user_request}

        Queue excerpt (WBS-1.* and WBS-2.*):
        {queue_summary}

        Current PROGRESS.md (excerpt):
        {progress}
        """
    ).strip()

    content: str
    model_used: str
    usage: Dict[str, Any] = {}

    try:
        content, model_used, usage = _call_openai(system_prompt, user_prompt)
    except Exception:
        if os.environ.get("ANTHROPIC_API_KEY"):
            content, model_used, usage = _call_anthropic(system_prompt, user_prompt)
        else:
            raise

    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    fname = f"AUTOPLAN-{ts}.md"
    out_path = runbooks_dir / fname

    header = textwrap.dedent(
        f"""
        # Autopilot plan — WBS-1.*, WBS-2.*

        - Generated at: {datetime.utcnow().isoformat()}Z
        - Model: {model_used}
        - Source: /orchestrator llm-plan
        - Queue source: ops/queue.jsonl
        - Progress source: docs/PROGRESS.md

        ---
        """
    ).lstrip()

    out_path.write_text(header + "\n\n" + content.strip() + "\n", encoding="utf-8")

    return str(out_path), model_used, usage
