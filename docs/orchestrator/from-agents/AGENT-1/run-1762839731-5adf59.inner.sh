set -Eeuo pipefail
cd /mnt/c/RastUp/RastUp

PROMPT_PATH=/mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762839731-5adf59.txt
CB_HINT_RAW='~/.local/bin/cursor-agent'

# Expand leading "~/"
case "$CB_HINT_RAW" in
  "~/"*) CB="$HOME/${CB_HINT_RAW#~/}" ;;
  *)     CB="$CB_HINT_RAW" ;;
esac

# Pick agent binary: hint → PATH → ~/.local/bin
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

# Ensure prompt exists; strip CRs (CRLF→LF) and pass exact text as single arg
if ! [ -s "$PROMPT_PATH" ]; then
  echo "ERROR: prompt file missing/empty: $PROMPT_PATH" >&2
  exit 3
fi
PROMPT="$(tr -d '\r' < "$PROMPT_PATH")"

export NO_OPEN_BROWSER=1
"$CB" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" || "$CB" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"
