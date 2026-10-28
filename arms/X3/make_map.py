"""Build X3's CLAUDE.md: a static map of target_repo (modules, signatures, first docstring lines). No LLM cost.

Usage: python arms/X3/make_map.py   (rerun whenever target_repo changes, and bump battery_version)
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "target_repo"


def first_line(node):
    doc = ast.get_docstring(node)
    return f" — {doc.strip().splitlines()[0]}" if doc else ""


def signature(fn):
    return f"{fn.name}({ast.unparse(fn.args)})" + (f" -> {ast.unparse(fn.returns)}" if fn.returns else "")


lines = ["# Repository map", "",
         "Generated from the source; use it to go straight to the right file instead of exploring.", ""]
for path in sorted(TARGET.rglob("*.py")):
    if "__pycache__" in path.parts:
        continue
    rel = path.relative_to(TARGET).as_posix()
    tree = ast.parse(path.read_text(encoding="utf-8"))
    lines.append(f"## {rel}{first_line(tree)}")
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            lines.append(f"- `{signature(node)}`{first_line(node)}")
        elif isinstance(node, ast.ClassDef):
            lines.append(f"- class `{node.name}`{first_line(node)}")
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("__"):
                    lines.append(f"  - `{signature(item)}`{first_line(item)}")
    lines.append("")
lines += ["## Running the tests", "", "`python -m pytest -q` from the project root.", ""]
out = Path(__file__).resolve().parent / "overlay" / "CLAUDE.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {out} ({len(lines)} lines)")
