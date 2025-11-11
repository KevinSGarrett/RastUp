set -Eeuo pipefail
cd /mnt/c/RastUp/RastUp
PROMPT_FILE=/mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762839251-b6c101.txt

# Verify prompt file and show light diagnostics
if ! [ -s "$PROMPT_FILE" ]; then
  echo "PROMPT_MISSING" >&2; exit 2
fi
echo "PROMPT_BYTES=$(wc -c < "$PROMPT_FILE")"
echo "PROMPT_HEAD=$(head -c 80 "$PROMPT_FILE" | tr -d '\r' | sed 's/[^[:print:]\t]/?/g')"

# Choose cursor-agent inside WSL (order: ~/.local/bin → PATH → CURSOR_BIN if valid)
AG=""
if [ -x "$HOME/.local/bin/cursor-agent" ]; then
  AG="$HOME/.local/bin/cursor-agent"
elif command -v cursor-agent >/dev/null 2>&1; then
  AG="$(command -v cursor-agent)"
elif [ -n "${CURSOR_BIN:-}" ] && [ -x "${CURSOR_BIN}" ]; then
  AG="${CURSOR_BIN}"
fi
if [ -z "$AG" ]; then
  echo "ERROR: cursor-agent not found in ~/.local/bin, PATH, or valid CURSOR_BIN" >&2
  exit 127
fi
echo "AGENT_BIN=$AG"

export NO_OPEN_BROWSER=1

# Run (root form), then fallback to subcommand form if root fails
PROMPT_ARG="$(tr -d '\r' < "$PROMPT_FILE")"
"$AG" --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT_ARG" || "$AG" agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT_ARG"
