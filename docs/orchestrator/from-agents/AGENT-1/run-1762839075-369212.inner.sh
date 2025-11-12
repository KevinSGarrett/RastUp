set -Eeuo pipefail
cd /mnt/c/RastUp/RastUp

# Resolve cursor-agent inside WSL
AG="${CURSOR_BIN:-''}"
if [ -n "$AG" ] && [ ! -x "$AG" ]; then AG=""; fi
if [ -z "$AG" ]; then AG="$HOME/.local/bin/cursor-agent"; fi
if [ ! -x "$AG" ]; then AG="$(command -v cursor-agent || true)"; fi
if [ -z "$AG" ]; then echo 'ERROR: cursor-agent not found in WSL PATH' >&2; exit 127; fi

PROMPT_FILE=/mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762839075-369212.txt
if [ ! -s "$PROMPT_FILE" ]; then echo 'ERROR: prompt file missing/empty' >&2; exit 2; fi

# Strip trailing CRs from CRLF and keep exact content/newlines
PROMPT_CONTENT="$(awk '{sub(/\r$/,""); print}' "$PROMPT_FILE")"

export NO_OPEN_BROWSER=1

# Try primary CLI, then older 'agent' subcommand form
"$AG" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT_CONTENT" || "$AG" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT_CONTENT"
