set -Eeuo pipefail
cd /mnt/c/RastUp/RastUp
PROMPT_B64=$(base64 < /mnt/c/RastUp/RastUp/ops/prompts/.cursor_prompt_1762838066-4280c2.txt | tr -d '\n')
PROMPT=$(printf '%s' "$PROMPT_B64" | base64 -d)
export NO_OPEN_BROWSER=1
~/.local/bin/cursor-agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT" || ~/.local/bin/cursor-agent agent --print --output-format=text --force --approve-mcps --model gpt-5 "$PROMPT"
