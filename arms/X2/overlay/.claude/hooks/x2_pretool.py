"""X2: A5's trimming for both the Bash and the PowerShell tool.

Agents rarely type a bare `pytest`: they write `cd "<workspace>" && python -m pytest -q 2>&1 | tail -40` (Bash) or
`python -m pytest -q 2>&1 | Select-Object -Last 40` (PowerShell). So a plain test/git command is accepted with two
harmless wrappers: a leading cd into the session's own working directory, and a trailing 2>&1 plus tail/head/
Select-Object (the trimmer replaces it). Only that shape is rewritten and auto-approved; anything else is left to the
normal permission rules, exactly as in A0.
"""
import json
import re
import sys
from pathlib import Path

NOISY = re.compile(r"^(python3? -m pytest|py(?: -3)? -m pytest|pytest|git (diff|log|show))\b")
COMPOUND = re.compile(r"[;&|<>`\n]|\$\(")
CD = {
    "Bash": re.compile(r"^\s*cd\s+(\"[^\"]*\"|'[^']*'|[^\s;&|]+)\s*&&\s*"),
    "PowerShell": re.compile(r"^\s*(?:cd|Set-Location)\s+(?:-Path\s+)?(\"[^\"]*\"|'[^']*'|[^\s;&|]+)\s*(?:;|&&)\s*", re.I),
}
TAIL = {
    "Bash": re.compile(r"\s*(?:2>&1)?\s*(?:\|\s*(?:tail|head)(?:\s+-n)?\s+-?\d+)?\s*$"),
    "PowerShell": re.compile(r"\s*(?:2>&1)?\s*(?:\|\s*Select-Object\s+-(?:Last|First)\s+\d+)?\s*$", re.I),
}


def same_dir(a: str, b: str) -> bool:
    norm = lambda p: p.strip("\"'").replace("\\", "/").rstrip("/").lower()
    return bool(a) and norm(a) == norm(b)


payload = json.load(sys.stdin)
tool = payload.get("tool_name", "Bash")
command = payload.get("tool_input", {}).get("command", "")
if tool not in CD or "trim_output.py" in command:
    sys.exit(0)
head = command
cd = CD[tool].match(head)
if cd:
    if not same_dir(cd.group(1), payload.get("cwd", "")):
        sys.exit(0)  # a cd anywhere else is not this hook's business
    head = head[cd.end():]
head = TAIL[tool].sub("", head, count=1).strip()
if not NOISY.match(head) or COMPOUND.search(head):
    sys.exit(0)  # leave everything else untouched

python = Path(sys.executable).as_posix()  # the interpreter running this hook
trimmer = (Path(__file__).resolve().parent / "trim_output.py").as_posix()
if tool == "PowerShell":
    rewritten = (f'$tbOut = & {{ {head} }} 2>&1 | ForEach-Object {{ "$_" }}; $tbCode = $LASTEXITCODE; '
                 f'$tbOut | & "{python}" "{trimmer}"; $global:LASTEXITCODE = $tbCode')
else:
    rewritten = f'set -o pipefail; ( {head} ) 2>&1 | "{python}" "{trimmer}"'
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "permissionDecisionReason": "X2 output trimming",
        "updatedInput": {**payload.get("tool_input", {}), "command": rewritten},
    }
}))
