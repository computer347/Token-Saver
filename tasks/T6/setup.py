"""Seed the bug: month 13 passes validation."""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "taskbench_app" / "validation.py"
src = path.read_text()
old = "if not 1 <= month <= 12:"
assert old in src, "T6 setup: anchor not found"
path.write_text(src.replace(old, "if not 1 <= month <= 13:"))
