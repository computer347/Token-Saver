"""Shared paths and helpers for the token battery."""
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if os.name == "nt" and os.environ.get("PYTHONUTF8") != "1" and not os.environ.get("TB_UTF8_REEXEC"):
    # Re-run this script in UTF-8 mode on Windows, so every file read/write handles €, → and × correctly.
    import subprocess
    import sys
    sys.exit(subprocess.call([sys.executable, *sys.argv],
                             env={**os.environ, "PYTHONUTF8": "1", "TB_UTF8_REEXEC": "1"}))
ARMS = ROOT / "arms"
TASKS = ROOT / "tasks"
TARGET = ROOT / "target_repo"
RESULTS = ROOT / "results"
VENDOR = ROOT / "vendor"
RUNS_FILE = RESULTS / "runs.jsonl"


def load_config() -> dict:
    return json.loads((ROOT / "config.json").read_text())


def claude_bin(cfg: dict) -> str:
    return os.environ.get("TB_CLAUDE_BIN") or cfg.get("claude_bin", "claude")


def claude_cmd(cfg: dict) -> list[str]:
    """The argv prefix that starts Claude Code on this machine.

    - A .py path (the self-test's fake claude) runs under this Python.
    - On Windows, an npm install is a `claude.cmd` wrapper; cmd.exe cuts the command line at the first newline
      (dropping the rest of the prompt and every flag after it) and mangles quotes and %, so the wrapper is
      bypassed: its target (bin/claude.exe in current versions, cli.js in older ones) is started directly.
    - Otherwise the executable is resolved on PATH (handles claude.exe from the native installer).
    """
    import re
    import sys
    name = claude_bin(cfg)
    if name.endswith(".py"):
        return [sys.executable, name]
    resolved = shutil.which(name) or name
    if resolved.lower().endswith((".cmd", ".bat")):
        wrapper = Path(resolved)
        targets = [wrapper.parent / m.replace("\\", "/").lstrip("/")
                   for m in re.findall(r'"%dp0%\\?([^"]+)"', wrapper.read_text(errors="replace"))]
        targets.append(wrapper.parent / "node_modules" / "@anthropic-ai" / "claude-code" / "cli.js")
        node = shutil.which("node")
        for target in targets:
            if target.suffix.lower() == ".exe" and target.exists():
                return [str(target)]
            if target.suffix.lower() in (".js", ".cjs", ".mjs") and target.exists() and node:
                return [node, str(target)]
    return [resolved]


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def sh(args, cwd=None, env=None, timeout=None, check=False) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, env=env, timeout=timeout, check=check,
                          capture_output=True, text=True)


def git(work: Path, *args) -> str:
    env = {**os.environ, "GIT_AUTHOR_NAME": "battery", "GIT_AUTHOR_EMAIL": "battery@local",
           "GIT_COMMITTER_NAME": "battery", "GIT_COMMITTER_EMAIL": "battery@local"}
    return sh(["git", *args], cwd=work, env=env, check=True).stdout


def copy_tree(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for path in src.rglob("*"):
        if path.name == ".keep":
            continue
        if "__pycache__" in path.parts or path.name == ".pytest_cache":
            continue
        target = dst / path.relative_to(src)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def deep_merge(base: dict, extra: dict) -> dict:
    out = dict(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        elif isinstance(value, list) and isinstance(out.get(key), list):
            out[key] = out[key] + value
        else:
            out[key] = value
    return out


def suite_of(task: str, cfg: dict | None = None) -> str:
    cfg = cfg or load_config()
    for name, spec in cfg["suites"].items():
        if (ROOT / spec["tasks"] / task).is_dir():
            return name
    raise KeyError(f"task {task!r} not found in any suite")


def suite_spec(suite: str, cfg: dict | None = None) -> dict:
    return (cfg or load_config())["suites"][suite]


def target_dir(suite: str = "small", cfg: dict | None = None) -> Path:
    return ROOT / suite_spec(suite, cfg)["target"]


def tasks_dir(suite: str = "small", cfg: dict | None = None) -> Path:
    return ROOT / suite_spec(suite, cfg)["tasks"]


def target_version(suite: str = "small") -> str:
    """Content hash of a suite's starting repo, so briefs and results are tied to one version."""
    import hashlib
    h = hashlib.sha256()
    target = target_dir(suite)
    for path in sorted(target.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            h.update(str(path.relative_to(target)).encode())
            h.update(path.read_bytes())
    return h.hexdigest()[:12]


def resolve_mode(cfg: dict, mode: str) -> tuple[dict, list[str], dict]:
    """Return (mode spec, arms, cfg) — confirm mode gets its own battery version so it is an independent replication."""
    spec = cfg["modes"][mode]
    if mode == "confirm":
        winners = [a for a in cfg.get("confirm_arms", []) if a not in ("A0", "A0b")]
        if not winners:
            raise SystemExit("confirm mode: list the winning arms in config.json 'confirm_arms' first")
        return spec, ["A0", "A0b"] + winners, {**cfg, "battery_version": cfg["battery_version"] + "-confirm"}
    return spec, list(spec["arms"]), cfg
