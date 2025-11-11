set -Eeuo pipefail
cd /mnt/c/RastUp/RastUp
PROMPT_PATH=/mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762838850-87a97f.txt
CURSOR_BIN='~/.local/bin/cursor-agent'
# expand leading ~ in CURSOR_BIN without using eval
case "$CURSOR_BIN" in
  "~/"*) CURSOR_BIN="$HOME/${CURSOR_BIN#~/}";;
  "~")   CURSOR_BIN="$HOME";;
esac
# if the provided CURSOR_BIN is not executable, try PATH
if ! [ -x "$CURSOR_BIN" ]; then
  if command -v cursor-agent >/dev/null 2>&1; then
    CURSOR_BIN="$(command -v cursor-agent)"
  fi
fi
if ! [ -x "$CURSOR_BIN" ]; then
  echo "ERROR: cursor-agent not found (CURSOR_BIN='$CURSOR_BIN')" >&2
  exit 127
fi
# read Windows-authored text; strip CR just in case
PROMPT="$(tr -d '\r' < "$PROMPT_PATH")"
export NO_OPEN_BROWSER=1
"$CURSOR_BIN" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" || "$CURSOR_BIN" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"
