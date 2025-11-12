set -Eeuo pipefail
cd /mnt/c/RastUp/RastUp

PROMPT_PATH=/mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762840730-511cb3.txt
CB_HINT_RAW='~/.local/bin/cursor-agent'

# Expand "~/" if present
case "$CB_HINT_RAW" in
  "~/"*) CB="$HOME/${CB_HINT_RAW#~/}" ;;
  "")    CB="" ;;
  *)     CB="$CB_HINT_RAW" ;;
esac

# Resolve agent binary: hint Ã¢â€ â€™ PATH Ã¢â€ â€™ ~/.local/bin
if [ -n "$CB" ] && [ -x "$CB" ]; then
  :
elif command -v cursor-agent >/dev/null 2>&1; then
  CB="$(command -v cursor-agent)"
elif [ -x "$HOME/.local/bin/cursor-agent" ]; then
  CB="$HOME/.local/bin/cursor-agent"
else
  echo "ERROR: cursor-agent not found (hint: $CB_HINT_RAW)" >&2
  exit 127
fi

echo "USING cursor-agent: $CB"
echo "PROMPT_PATH: $PROMPT_PATH"

# Require non-empty prompt; strip CR just in case
if ! [ -s "$PROMPT_PATH" ]; then
  echo "ERROR: prompt file missing/empty: $PROMPT_PATH" >&2
  exit 3
fi
PROMPT="$(tr -d '\r' < "$PROMPT_PATH")"

export NO_OPEN_BROWSER=1
"$CB" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" || "$CB" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"
