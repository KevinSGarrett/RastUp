# scripts/orchestrator/run_agent_with_pack.py
# Launch ONE Cursor agent using a rendered prompt pack.
# Usage:
#   python scripts/orchestrator/run_agent_with_pack.py --slug wbs-1-3-knowledge --model gpt-5 --query "..." --save-built

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Optional

# Repo root on path
REPO = str(pathlib.Path(__file__).resolve().parents[2])
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from orchestrator.prompt_pack import compile_pack, write_out  # type: ignore
from orchestrator.cursor_runner import run_cursor  # type: ignore

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run a single Cursor agent with a prompt pack.")
    ap.add_argument("--slug", required=True, help="Pack slug (e.g., wbs-1-3-knowledge)")
    ap.add_argument("--model", default="gpt-5", help="Model name")
    ap.add_argument("--query", default="", help="Optional focus to steer context inside the pack")
    ap.add_argument("--agent-name", default="AGENT-1", help="Agent name for logs")
    ap.add_argument("--save-built", action="store_true", help="Save the rendered prompt to ops/prompts/_built/")
    return ap.parse_args()

def main() -> None:
    args = parse_args()
    prompt = compile_pack(slug=args.slug, query=args.query, model=args.model)
    if args.save_built:
        out = write_out(args.slug, prompt, None)
        print(f"[saved] {out}")
    result = run_cursor(REPO, prompt, agent_name=args.agent_name, model=args.model)
    print(result)

if __name__ == "__main__":
    main()
