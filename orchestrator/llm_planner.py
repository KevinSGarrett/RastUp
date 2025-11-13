# orchestrator/llm_planner.py
"""
LLM planner for the orchestrator.

Uses OPENAI_API_KEY first (gpt-5 by default), then falls back to ANTHROPIC_API_KEY
(claude-4.5-sonnet by default) for planning WBS-1.* and WBS-2.* work.

No extra pip dependencies: uses only Python stdlib (urllib).
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
from urllib import request as _urlreq, error as _urlerr


def _read_wbs_context(repo_root: Path) -> str:
    """Summarize WBS-1.* and WBS-2.* from ops/queue.jsonl."""
    queue = repo_root / "ops" / "queue.jsonl"
    lines: List[str] = []
    if queue.exists():
        with queue.open("r", encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    j = json.loads(raw)
                except Exception:
                    continue
                wbs_id = str(j.get("id", ""))
                if not (wbs_id.startswith("WBS-1.") or wbs_id.startswith("WBS-2.")):
                    continue
                title = j.get("title", "")
                status = j.get("status", "")
                owner = j.get("owner", "")
                lines.append(f"{wbs_id} [{status}] ({owner}) - {title}")
    if not lines:
        return "No WBS-1.* or WBS-2.* items found in ops/queue.jsonl yet."
    return "\n".join(lines)


def _http_post_json(url: str, headers: Dict[str, str], body: Dict[str, Any]) -> Dict[str, Any]:
    data = json.dumps(body).encode("utf-8")
    req = _urlreq.Request(url, data=data, headers=headers, method="POST")
    try:
        with _urlreq.urlopen(req, timeout=90) as resp:
            status = resp.getcode()
            raw = resp.read()
    except _urlerr.HTTPError as e:
        status = e.code
        raw = e.read()
    except Exception as e:
        raise RuntimeError(f"HTTP error calling {url}: {e}")
    if status >= 400:
        snippet = raw[:300]
        raise RuntimeError(f"HTTP {status} from {url}: {snippet!r}")
    try:
        return json.loads(raw.decode("utf-8", errors="ignore"))
    except Exception:
        raise RuntimeError(f"Non-JSON response from {url}: {raw[:200]!r}")


def _call_openai(prompt: str) -> Tuple[str, Dict[str, Any]]:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set for OpenAI call")

    url = "https://api.openai.com/v1/chat/completions"
    model = os.environ.get("RU_LLM_PLAN_OPENAI_MODEL", "gpt-5")

    body = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are the orchestrator's planning brain for a large multi-month build. "
                    "Produce a concrete 3–5 day plan for WBS-1.* and WBS-2.* work. "
                    "Use bullet points, include WBS ids, mention files/paths when obvious, "
                    "and keep the answer under ~1500 words."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 1200,
        "temperature": 0.3,
    }

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    data = _http_post_json(url, headers, body)
    try:
        content = data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"Unexpected OpenAI response: {data!r}")

    usage = data.get("usage") or {}
    total_tokens = int(
        usage.get("total_tokens")
        or (usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0))
        or 0
    )
    meta = {
        "provider": "openai",
        "model": model,
        "tokens": total_tokens,
    }
    return content, meta


def _call_anthropic(prompt: str) -> Tuple[str, Dict[str, Any]]:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set for Anthropic call")

    url = "https://api.anthropic.com/v1/messages"
    model = os.environ.get("RU_LLM_PLAN_ANTHROPIC_MODEL", "claude-4.5-sonnet")

    body = {
        "model": model,
        "max_tokens": 1200,
        "temperature": 0.3,
        "system": (
            "You are the orchestrator's planning brain for a large multi-month build. "
            "Produce a concrete 3–5 day plan for WBS-1.* and WBS-2.* work. "
            "Use bullet points, include WBS ids, mention files/paths when obvious, "
            "and keep the answer under ~1500 words."
        ),
        "messages": [
            {"role": "user", "content": prompt},
        ],
    }

    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    data = _http_post_json(url, headers, body)
    try:
        blocks = data["content"]
        parts: List[str] = []
        for block in blocks:
            if block.get("type") == "text":
                parts.append(block.get("text") or "")
        content = "\n".join(parts).strip()
    except Exception:
        raise RuntimeError(f"Unexpected Anthropic response: {data!r}")

    usage = data.get("usage") or {}
    total_tokens = int((usage.get("input_tokens") or 0) + (usage.get("output_tokens") or 0))
    meta = {
        "provider": "anthropic",
        "model": model,
        "tokens": total_tokens,
    }
    return content, meta


def run_llm_plan(prompt: Optional[str], repo_root: Path) -> Tuple[str, Dict[str, Any]]:
    """
    Core entrypoint used by orchestrator.app.

    Returns:
      plan_text, meta_dict
      where meta_dict includes: provider, model, tokens, rel_path
    """
    repo_root = Path(repo_root)
    wbs_context = _read_wbs_context(repo_root)

    base_prompt = (prompt or "").strip().strip('"')
    if not base_prompt:
        base_prompt = (
            "Plan the next 3–5 days of work for WBS-1.* and WBS-2.* "
            "based on the current WBS queue and blueprints."
        )

    combined = (
        base_prompt
        + "\n\nCurrent WBS items (WBS-1.* and WBS-2.*):\n"
        + wbs_context
        + "\n"
    )

    last_error: Optional[Exception] = None

    # Try OpenAI first, then Anthropic
    for fn in (_call_openai, _call_anthropic):
        try:
            text, meta = fn(combined)
            provider = meta.get("provider", "llm")
            ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            rel_path = Path("docs") / "orchestrator" / "plans" / f"llm-plan-{provider}-{ts}.md"
            abs_path = repo_root / rel_path
            abs_path.parent.mkdir(parents=True, exist_ok=True)

            header = (
                f"# LLM Plan — {provider} {meta.get('model')} — {ts}\n\n"
                "## Prompt\n\n```text\n"
                + base_prompt
                + "\n```\n\n"
                "## WBS context\n\n```text\n"
                + wbs_context
                + "\n```\n\n"
                "## Plan\n\n"
            )
            full = header + text
            abs_path.write_text(full, encoding="utf-8")

            meta["rel_path"] = rel_path.as_posix()
            return text, meta
        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(f"All LLM backends failed (last error: {last_error})")
