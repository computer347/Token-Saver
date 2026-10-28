"""Seed the bug: thousands separators get turned into decimal points."""
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "taskbench_app" / "parsing.py"
src = path.read_text()
old = 'cleaned = cleaned.replace(",", "")'
assert old in src, "T1 setup: anchor not found"
path.write_text(src.replace(old, 'cleaned = cleaned.replace(",", ".")'))
