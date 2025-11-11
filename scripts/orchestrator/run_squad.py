# -*- coding: utf-8 -*-
"""
orchestrator/prompt_pack.py

Exports:
  - compile_pack(slug, repo_root, agent_name, model, query="")
  - write_out(slug, prompt, repo_root) -> Path

Used by:
  scripts/orchestrator/run_agent_with_pack.py
  scripts/orchestrator/run_squad.py

This module returns a HEADLESS prompt string that your cursor runner will hand
to the Cursor Agent. Packs are deterministic and reference repo paths so the
agent can discover knowledge assets and CI rules without asking questions.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Callable, Dict

__all__ = ["compile_pack", "write_out"]

# --------------------------------------------------------------------
# Utilities
# --------------------------------------------------------------------
def _nlfix(s: str) -> str:
    # Normalize to LF and strip BOM if present
    return s.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")

def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def _exists(p: Path) -> bool:
    try:
        return p.exists()
    except Exception:
        return False

# --------------------------------------------------------------------
# Pack: WBS-1.3 Knowledge (index + readers + CI guard)
# --------------------------------------------------------------------
def _pack_wbs_1_3_knowledge(repo_root: str, agent_name: str, model: str, query: str) -> str:
    RR = Path(repo_root)
    # Known files the agent should use/maintain
    manifest = RR / "docs" / "index" / "manifest.json"
    chunks   = RR / "docs" / "index" / "chunks.jsonl"
    segments = RR / "docs" / "index" / "segments.jsonl"
    plain_md = RR / "docs" / "blueprints" / "plain"
    ci_gate  = RR / ".github" / "workflows" / "ci-knowledge.yml"
    nt_idx   = RR / "docs" / "blueprints" / "nt-index.json"
    td_idx   = RR / "docs" / "blueprints" / "td-index.json"

    # Detect what already exists (purely advisory in the prompt)
    have_manifest = _exists(manifest)
    have_chunks   = _exists(chunks)
    have_segments = _exists(segments)
    have_plain    = _exists(plain_md)
    have_ci_gate  = _exists(ci_gate)
    have_nt       = _exists(nt_idx)
    have_td       = _exists(td_idx)

    # Small hint string for the agent (no branching; just FYI)
    status_hint = json.dumps({
        "have_manifest": have_manifest,
        "have_chunks": have_chunks,
        "have_segments": have_segments,
        "have_plain_markdown": have_plain,
        "have_ci_knowledge_gate": have_ci_gate,
        "have_nt_index": have_nt,
        "have_td_index": have_td,
    }, indent=2)

    # Prompt body:
    return _nlfix(f"""HEADLESS RUN — DO NOT ASK QUESTIONS.

Agent: {agent_name}
Model: {model}
Repo: {repo_root}

Task (WBS-1.3 Knowledge):
- Ensure ALL project knowledge (technical and non-technical) is normalized and indexed for agent access.
- Keep changes PR-sized and additive; do not break existing workflows.
- Prefer existing scripts if present; create only what's missing.

Deliverables (idempotent):
1) Normalize & index blueprints:
   - Use: scripts/blueprints/build_index.py
   - Expect outputs:
     - docs/blueprints/plain/*.md
     - docs/blueprints/nt-index.json
     - docs/blueprints/td-index.json
     - docs/index/manifest.json
     - docs/index/chunks.jsonl
     - docs/index/segments.jsonl (alias of chunks.jsonl)

2) Orchestrator knowledge readers:
   - Use/ensure: orchestrator/knowledge.py (read/show/query CLI already expected)
   - Must be able to:
     - `python -m orchestrator.knowledge show --path <file> --first 40`
     - `python -m orchestrator.knowledge query --text "<terms>" --k 5`

3) CI guard (knowledge coverage):
   - Ensure or create: .github/workflows/ci-knowledge.yml
   - Gate on presence of docs/index/manifest.json and segments.jsonl.
   - Print a short summary table.

4) Health report:
   - Ensure: scripts/orchestrator/check_coverage.py emits docs/orchestrator/HEALTH.md
   - Must include PASS/FAIL lines for:
     R-INDEX-NT, R-INDEX-TD, R-NORMALIZED-PLAIN,
     R-CI-KNOWLEDGE, and any other existing checks.

5) Commit policy (if diff exists):
   - Stage only new/updated files under docs/index, docs/blueprints/plain, docs/orchestrator/HEALTH.md,
     relevant scripts, and ci-knowledge.yml.
   - Conventional Commit:
       chore: knowledge index/coverage (WBS-1.3)
     Trailers:
       NT: NT-1.3
       TD: TD-1.3
       WBS: WBS-1.3

Conventions & Safety:
- Respect SAFE-MODE: if ops/flags/safe-mode.json exists, do NOT push; only prepare the branch & summary.
- Approvals: only write files if an approval exists in ops/approvals/ matching the operation (e.g., "write").
- If a tool is missing (python-docx, odfpy, PyPDF2), scaffold steps with TODO notes and continue-on-error: true.
- Keep Windows/WSL compatibility: do not rely on interactive tools.

Hints (detected state):
{status_hint}

Exact Output Requirements:
- Print a concise summary of actions and created/updated paths.
- Print DONE on success.
- Exit non-zero on failure with a brief reason.
""")

# --------------------------------------------------------------------
# Pack registry & compiler
# --------------------------------------------------------------------
_PACKS: Dict[str, Callable[[str, str, str, str], str]] = {
    "wbs-1-3-knowledge": _pack_wbs_1_3_knowledge,
}

def compile_pack(
    slug: str,
    repo_root: str,
    agent_name: str,
    model: str,
    query: str = "",
) -> str:
    """Return the fully rendered prompt string for the given pack slug."""
    key = str(slug).strip().lower()
    if key not in _PACKS:
        available = ", ".join(sorted(_PACKS.keys()))
        raise KeyError(f"Unknown prompt pack '{slug}'. Available: {available}")
    return _PACKS[key](repo_root, agent_name, model, query or "")

def write_out(slug: str, prompt: str, repo_root: str) -> Path:
    """
    Write the prompt to ops/prompts/<slug>.txt, BOM-free (UTF-8).
    """
    repo = Path(repo_root)
    outdir = repo / "ops" / "prompts"
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"{slug}.txt"
    # Ensure BOM-free, LF newlines
    text = _nlfix(prompt)
    out.write_text(text, encoding="utf-8")
    return out
