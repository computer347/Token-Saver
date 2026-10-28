"""Code-quality metrics on what the agent changed, so 'cheaper' can't quietly mean 'worse code'.

Standard library only: cyclomatic complexity and unused imports via `ast`. If `ruff` is on PATH,
its issue count on the changed files is added too.
"""
import ast
import json
import shutil
import subprocess
from pathlib import Path

BRANCHES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.IfExp, ast.ExceptHandler, ast.With, ast.AsyncWith, ast.Assert)


def _function_complexities(tree):
    out = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            score = 1
            for sub in ast.walk(node):
                if isinstance(sub, BRANCHES):
                    score += 1
                elif isinstance(sub, ast.BoolOp):
                    score += len(sub.values) - 1
                elif isinstance(sub, ast.comprehension):
                    score += 1 + len(sub.ifs)
                elif hasattr(ast, "match_case") and isinstance(sub, ast.match_case):
                    score += 1
            out.append(score)
    return out


def _unused_imports(tree):
    imported = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported[(a.asname or a.name).split(".")[0]] = node.lineno
        elif isinstance(node, ast.ImportFrom) and node.module != "__future__":
            for a in node.names:
                if a.name != "*":
                    imported[a.asname or a.name] = node.lineno
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    used |= {n.value.id for n in ast.walk(tree) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    names_in_all = {"__all__"} & {t.id for n in ast.walk(tree) if isinstance(n, ast.Assign) for t in n.targets
                                  if isinstance(t, ast.Name)}
    return 0 if names_in_all else len(set(imported) - used)


def _git(work, *args):
    return subprocess.run(["git", *args], cwd=work, capture_output=True, text=True).stdout


def code_quality(work: Path) -> dict:
    """Assumes diff_stats() already staged everything (`git add -A`)."""
    changed = [p for p in _git(work, "diff", "--cached", "--name-only", "HEAD").splitlines()
               if p.endswith(".py") and not p.startswith("_hidden/")]
    before = after = 0
    max_fn = 0
    unused = 0
    syntax_errors = 0
    for rel in changed:
        path = work / rel
        if path.exists():
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
                scores = _function_complexities(tree)
                after += sum(scores)
                max_fn = max([max_fn] + scores)
                unused += _unused_imports(tree)
            except SyntaxError:
                syntax_errors += 1
        old = _git(work, "show", f"HEAD:{rel}")
        if old:
            try:
                before += sum(_function_complexities(ast.parse(old)))
            except SyntaxError:
                pass
    ruff = None
    existing = [rel for rel in changed if (work / rel).exists()]
    if shutil.which("ruff") and existing:
        proc = subprocess.run(["ruff", "check", "--output-format", "json", "--quiet", *existing], cwd=work,
                              capture_output=True, text=True)
        try:
            ruff = len(json.loads(proc.stdout or "[]"))
        except json.JSONDecodeError:
            ruff = None
    return {"py_files_changed": len(changed), "complexity_before": before, "complexity_after": after,
            "complexity_delta": after - before, "max_function_complexity": max_fn,
            "unused_imports": unused, "syntax_errors": syntax_errors, "ruff_issues": ruff}
