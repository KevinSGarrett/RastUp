set -Eeuo pipefail
cd /mnt/c/RastUp/RastUp
PROMPT_FILE=/mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762838302-8a44c1.txt
PROMPT=$(tr -d '\r' < "$PROMPT_FILE")
export NO_OPEN_BROWSER=1
~/.local/bin/cursor-agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" || ~/.local/bin/cursor-agent agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"
