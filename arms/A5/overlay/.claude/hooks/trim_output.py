"""Keep failures, errors and the final summary line; drop the rest."""
import re
import sys

KEEP = re.compile(r"(FAIL|ERROR|Error|Traceback|assert|^E\s|^>|passed|failed|error|^diff --git|^@@|^[+-][^+-])")
MAX_LINES = 60

lines = sys.stdin.read().splitlines()
kept = [line for line in lines if KEEP.search(line)][-MAX_LINES:]
print("\n".join(kept))
print(f"[trimmed by A5: {len(lines)} lines -> {len(kept)}]")
