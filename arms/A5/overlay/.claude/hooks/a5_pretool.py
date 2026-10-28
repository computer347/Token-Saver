"""A5: pipe noisy test/git commands through a trimmer so only failures and a summary come back."""
import json
import re
import sys

NOISY = re.compile(r"^\s*(python3? -m pytest|pytest|git (diff|log|show))\b")
# The rewrite is auto-approved, so only single plain commands qualify; anything chained, piped or redirected
# goes through the normal permission rules, exactly as in A0.
COMPOUND = re.compile(r"[;&|<>`\n]|\$\(")

payload = json.load(sys.stdin)
command = payload.get("tool_input", {}).get("command", "")
if not NOISY.match(command) or COMPOUND.search(command) or "trim_output.py" in command:
    sys.exit(0)  # leave everything else untouched

from pathlib import Path
python = Path(sys.executable).as_posix()  # the interpreter running this hook; works where `python3` doesn't exist
trimmer = '"$CLAUDE_PROJECT_DIR/.claude/hooks/trim_output.py"'
rewritten = f'set -o pipefail; ( {command} ) 2>&1 | "{python}" {trimmer}'
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "permissionDecisionReason": "A5 output trimming",
        "updatedInput": {**payload.get("tool_input", {}), "command": rewritten},
    }
}))
