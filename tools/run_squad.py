#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

# Reuse the existing Cursor runner
try:
    from orchestrator.cursor_runner import run_cursor
except Exception as e:
    print(f"Failed to import runner: {e}", file=sys.stderr)
    sys.exit(2)

try:
    # Prompt pack compiler for building the agent prompt text
    from orchestrator.prompt_pack import compile_pack as compile_prompt_pack
except Exception as e:
    print(f"Failed to import prompt pack compiler: {e}", file=sys.stderr)
    sys.exit(2)

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the 4-agent Autopilot Squad sequentially using cursor-agent"
    )
    parser.add_argument("--model", default="gpt-5", help="Model to use (default: gpt-5)")
    parser.add_argument("--title", default="Autopilot Squad", help="Run title shown in logs")
    parser.add_argument(
        "--pack",
        default="wbs-1-3-knowledge",
        help="Prompt pack slug to compile and run (default: wbs-1-3-knowledge)",
    )
    parser.add_argument(
        "--query",
        default="",
        help="Optional focus text to include in the prompt pack",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    agents = ["AGENT-1", "AGENT-2", "AGENT-3", "AGENT-4"]
    print(f"Starting squad: {args.title} — model={args.model} — pack={args.pack}")

    overall_rc = 0
    for idx, agent in enumerate(agents, start=1):
        print(f"--- [{idx}/4] Launching {agent} ---")
        # Compile prompt for this specific agent
        try:
            prompt_text = compile_prompt_pack(
                slug=args.pack,
                repo_root=str(repo_root),
                model=args.model,
                query=args.query,
            )
        except Exception as e:
            print(f"Failed to compile prompt pack '{args.pack}' for {agent}: {e}", file=sys.stderr)
            return 3

        res = run_cursor(str(repo_root), prompt_text, agent_name=agent, model=args.model)
        rc = int(res.get("retcode", 1))
        attach = res.get("attach")
        print(f"[{idx}/4] {agent} finished — exit_code={rc}; attach={attach}")
        if rc != 0:
            overall_rc = rc
            print(f"Stopping squad after {agent} due to failure.")
            break

    print("Squad run complete.")
    return overall_rc


if __name__ == "__main__":
    sys.exit(main())
