set -Eeuo pipefail
cd /mnt/c/RastUp/RastUp
AG=''  # may be empty
if [ -z "$AG" ]; then
  AG="$(command -v cursor-agent || true)"
  if [ -z "$AG" ]; then AG="$HOME/.local/bin/cursor-agent"; fi
fi
if [ ! -x "$(printf %s "$AG" | sed 's/\"//g')" ]; then
  echo "ERROR: cursor-agent not found in WSL PATH (AG='$AG')" >&2
  exit 1
fi
PROMPT_FILE=/mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762839989-8a5b2c.txt
if [ -z "$PROMPT_FILE" ]; then echo 'PROMPT_MISSING: empty variable' >&2; exit 2; fi
if [ ! -f "$PROMPT_FILE" ]; then echo "PROMPT_MISSING: file not found: $PROMPT_FILE" >&2; exit 2; fi
if [ ! -s "$PROMPT_FILE" ]; then echo "PROMPT_MISSING: file empty: $PROMPT_FILE" >&2; exit 2; fi
echo "PROMPT_BYTES=$(wc -c < "$PROMPT_FILE")"
echo "AGENT_BIN=$AG"
PROMPT="$(tr -d '\r' < "$PROMPT_FILE")"
export NO_OPEN_BROWSER=1
"$AG" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" || "$AG" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"

