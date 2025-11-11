# orchestrator/prompt_pack.py
"""
Prompt pack compiler for single-agent Cursor runs.

Features
- compile_pack(slug, query="", model=None, repo_root=None) -> str
- write_out(name, content, out=None) -> str (returns file path as string)
- CLI:
    python -m orchestrator.prompt_pack build --name wbs-1-3-knowledge --out ops\prompts\wbs-1-3-knowledge.txt
    python -m orchestrator.prompt_pack print --name wbs-1-3-knowledge
    python -m orchestrator.prompt_pack list
Notes
- '--out' can be a directory OR a file path. Existing files are overwritten.
- Designed to work with scripts/orchestrator/run_agent_with_pack.py
"""

from __future__ import annotations

import argparse
import pathlib
from typing import Dict, Optional

REPO = pathlib.Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------
# Pack templates (add more slugs as needed)
# ---------------------------------------------------------------------

def _pack_wbs_1_3_knowledge(repo_root: str, query: str, model: Optional[str]) -> str:
    q = (query or "").strip()
    model_line = f"Model: {model}" if model else "Model: gpt-5 (default)"
    return f"""HEADLESS RUN — DO NOT ASK QUESTIONS.

{model_line}
Repo: {repo_root}

Task: WBS‑1.3 orchestrator knowledge plumbing & control plane (single agent).
Goal: Ensure the orchestrator can index/read both technical and non‑technical blueprints, expose a CLI, and is ready to be triggered by Slack (minimal wiring stubs OK). Respect SAFE‑MODE and approvals.

Do:
- Verify/refresh blueprint normalization and indices:
  * scripts/blueprints/build_index.py builds:
      - docs/blueprints/plain/*.md
      - docs/blueprints/nt-index.json, td-index.json, sections.json, toc-cache.json
      - docs/index/manifest.json
      - docs/index/chunks.jsonl and docs/index/segments.jsonl
- Ensure orchestrator/knowledge.py supports:
  * python -m orchestrator.knowledge build
  * python -m orchestrator.knowledge audit --strict
  * python -m orchestrator.knowledge read --path PATH --first N
  * python -m orchestrator.knowledge query --text "..." --k 5
- Respect SAFE‑MODE and approvals:
  * If ops/flags/safe-mode.json exists: do not push/publish/modify beyond allowed ops.
  * Honor explicit approvals in ops/approvals/*.json for any writes outside workflows/prompts/docs.
- Minimal Slack wiring stubs in orchestrator/app.py:
  * (non-destructive) confirm handlers or leave TODOs gated by SAFE‑MODE.
- CI gate:
  * Ensure .github/workflows/ci-knowledge.yml is present or updated without breaking existing workflows.

Conventions:
- Keep diffs additive and PR‑sized.
- If a tool is missing, scaffold steps with continue-on-error: true and TODO note.
- Commit message: "orchestrator: WBS-1.3 knowledge plumbing & control plane"
  Trailers:
    NT: NT-1.3
    TD: TD-1.3
    WBS: WBS-1.3

Output:
- Print exactly: DONE
- Exit 0 on success; non‑zero with a short reason otherwise.

{("Focus: " + q) if q else ""}
"""

PACKS: Dict[str, callable] = {
    "wbs-1-3-knowledge": _pack_wbs_1_3_knowledge,
}

# ---------------------------------------------------------------------
# API
# ---------------------------------------------------------------------

def compile_pack(
    slug: str,
    query: str = "",
    model: Optional[str] = None,
    repo_root: Optional[str] = None,
) -> str:
    """
    Build the full prompt text for the given slug.
    """
    repo_root = repo_root or str(REPO)
    slug = slug.strip()
    if slug not in PACKS:
        # Generic fallback
        base = f"""HEADLESS RUN — DO NOT ASK QUESTIONS.

Repo: {repo_root}
Model: {model or "gpt-5 (default)"}

Task: {slug}
Context:
- Respect SAFE‑MODE (ops/flags/safe-mode.json) and approvals (ops/approvals/*.json).
- Keep changes additive; do not break existing workflows.

Output:
- Print exactly: DONE
- Exit 0 on success; non‑zero on failure.
"""
        if query:
            base += f"\nFocus: {query.strip()}\n"
        return base

    return PACKS[slug](repo_root=repo_root, query=query, model=model)

def write_out(name: str, content: str, out: Optional[pathlib.Path]) -> str:
    """
    Write the prompt text to disk. If 'out' is:
      - None: write to ops/prompts/_built/{name}.txt
      - A directory: write {dir}/{name}.txt
      - A file path (has suffix): write to that file
    Overwrites existing files.
    Returns the full file path as string.
    """
    if out is None:
        target_dir = REPO / "ops" / "prompts" / "_built"
        target_dir.mkdir(parents=True, exist_ok=True)
        path = target_dir / f"{name}.txt"
    else:
        out = pathlib.Path(out)
        if out.suffix:
            # Treat as file path
            out.parent.mkdir(parents=True, exist_ok=True)
            path = out
        else:
            # Treat as directory
            out.mkdir(parents=True, exist_ok=True)
            path = out / f"{name}.txt"

    path.write_text(content, encoding="utf-8")
    return str(path)

# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def _cli_build(name: str, out: Optional[str], query: str, model: Optional[str]) -> None:
    content = compile_pack(slug=name, query=query, model=model)
    path_str = write_out(name, content, pathlib.Path(out) if out else None)
    print(path_str)

def _cli_print(name: str, query: str, model: Optional[str]) -> None:
    content = compile_pack(slug=name, query=query, model=model)
    print(content)

def _cli_list() -> None:
    for key in sorted(PACKS.keys()):
        print(key)

def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(prog="orchestrator.prompt_pack", description="Prompt pack utilities")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="Render a pack to a file path")
    b.add_argument("--name", required=True, help="Pack slug (e.g., wbs-1-3-knowledge)")
    b.add_argument("--out", default=None, help="Output directory or file path")
    b.add_argument("--query", default="", help="Optional focus text to steer the agent")
    b.add_argument("--model", default=None, help="Optional model label to embed in the prompt")

    p = sub.add_parser("print", help="Print a pack to stdout")
    p.add_argument("--name", required=True, help="Pack slug")
    p.add_argument("--query", default="", help="Optional focus text")
    p.add_argument("--model", default=None, help="Optional model label")

    sub.add_parser("list", help="List available pack slugs")

    return ap.parse_args()

def _main() -> None:
    args = _parse_args()
    if args.cmd == "build":
        _cli_build(args.name, args.out, args.query, args.model)
    elif args.cmd == "print":
        _cli_print(args.name, args.query, args.model)
    elif args.cmd == "list":
        _cli_list()

if __name__ == "__main__":
    _main()
