"""Seed the bug: ledgers written before 'kind' existed crash on load."""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "taskbench_app" / "models.py"
src = path.read_text()
old = 'kind=data.get("kind", "expense"),'
assert old in src, "T8 setup: anchor not found"
path.write_text(src.replace(old, 'kind=data["kind"],'))
