set -Eeuo pipefail

# Ensure non-interactive shells see ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"

cd /mnt/c/RastUp/RastUp

# Accept a Windows-side hint (embedded here) but resolve inside WSL
CB_HINT_RAW='~/.local/bin/cursor-agent'
CB="$CB_HINT_RAW"
if [ -n "$CB" ]; then
  case "$CB" in "~/"*) CB="$HOME/${CB#~/}";; esac
fi

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

PROMPT_PATH=/mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762923739-2f3dba.txt
if ! [ -s "$PROMPT_PATH" ]; then
  echo "ERROR: prompt file missing/empty: $PROMPT_PATH" >&2
  exit 3
fi

# Diagnostics
echo "USING cursor-agent: $CB"
echo "PROMPT_PATH: $PROMPT_PATH"
echo "PROMPT_BYTES=$(wc -c < "$PROMPT_PATH")"

# Read prompt and strip any CR to avoid argument splitting
PROMPT="$(tr -d '\r' < "$PROMPT_PATH")"

export NO_OPEN_BROWSER=1

# Decide on line-buffering (stdbuf) and soft timeout (timeout)
_has_stdbuf=0
_has_timeout=0
command -v stdbuf >/dev/null 2>&1 && _has_stdbuf=1
command -v timeout >/dev/null 2>&1 && _has_timeout=1

TIMEOUT_SECS="${TIMEOUT_SECS:-1200}"  # 20 minutes default

if [ "$_has_timeout" -eq 1 ] && [ "$_has_stdbuf" -eq 1 ]; then
  timeout "$TIMEOUT_SECS" stdbuf -oL -eL "$CB" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" ||   timeout "$TIMEOUT_SECS" stdbuf -oL -eL "$CB" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"
elif [ "$_has_timeout" -eq 1 ]; then
  timeout "$TIMEOUT_SECS" "$CB" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" ||   timeout "$TIMEOUT_SECS" "$CB" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"
elif [ "$_has_stdbuf" -eq 1 ]; then
  stdbuf -oL -eL "$CB" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" ||   stdbuf -oL -eL "$CB" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"
else
  "$CB" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" ||   "$CB" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"
fi
