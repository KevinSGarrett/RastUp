import os
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


def mask(value: str) -> str:
    """Mask secrets so we never print full tokens."""
    if not value:
        return ""
    if len(value) <= 4:
        return "*" * len(value)
    # show first 4 chars, then ...
    return value[:4] + "..."


def print_row(source: str, env_name: str, present: bool, masked_value: str):
    status = "YES" if present else "NO"
    print(f"{source:10} | {env_name:24} | {status:3} | {masked_value}")


def main():
    cfg = load_config()
    apis = cfg.get("apis", {})
    cursor_cfg = cfg.get("cursor", {})

    checks = []

    # OpenAI (from config)
    openai_cfg = apis.get("openai", {})
    if openai_cfg.get("enabled", False):
        env_name = openai_cfg.get("api_key_env", "OPENAI_API_KEY")
        value = os.environ.get(env_name, "")
        checks.append(("OpenAI", env_name, bool(value), mask(value)))

    # Anthropic (from config)
    anthropic_cfg = apis.get("anthropic", {})
    if anthropic_cfg.get("enabled", False):
        env_name = anthropic_cfg.get("api_key_env", "ANTHROPIC_API_KEY")
        value = os.environ.get(env_name, "")
        checks.append(("Anthropic", env_name, bool(value), mask(value)))

    # Cursor token (from config)
    cursor_env_name = cursor_cfg.get("api_key_env", "CURSOR_API_KEY")
    cursor_val = os.environ.get(cursor_env_name, "")
    checks.append(("Cursor", cursor_env_name, bool(cursor_val), mask(cursor_val)))

    # Extra connectors: AWS, GitHub, Slack
    extra_envs = [
        ("AWS", "AWS_ACCESS_KEY_ID"),
        ("AWS", "AWS_SECRET_ACCESS_KEY"),
        ("GitHub", "GITHUB_TOKEN"),
        ("Slack", "SLACK_BOT_TOKEN"),
    ]
    for source, env_name in extra_envs:
        value = os.environ.get(env_name, "")
        checks.append((source, env_name, bool(value), mask(value)))

    print("=== Orchestrator Environment / API Key Status ===")
    print("Source     | ENV VAR                 | OK? | Value")
    print("-----------+-------------------------+-----+------------------")
    for source, env_name, present, masked_value in checks:
        print_row(source, env_name, present, masked_value)

    print()
    print("NOTE:")
    print("- This script does NOT call any APIs; it only checks environment variables.")
    print("- Make sure you run your load_env.ps1 (or equivalent) before running this.")
    print("- The orchestrator will later rely on these being present for real runs.")


if __name__ == "__main__":
    main()
