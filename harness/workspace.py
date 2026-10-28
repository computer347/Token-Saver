"""Build one fresh, isolated workspace: target repo + task setup + arm overlay, committed as 'base'."""
import json
import os
import re
import shutil
import sys
from pathlib import Path

from common import ARMS, ROOT, VENDOR, copy_tree, deep_merge, git, load_config, sh, suite_of, suite_spec, target_dir, tasks_dir, target_version

ARM_TEXT_FILES = ("CLAUDE.md",)



_SHELL_RULE = re.compile(r"^(Bash|PowerShell)\((.*)\)$")


def expand_rules(rules: list[str]) -> list[str]:
    """Bring command rules to the current syntax and cover every shell Claude Code may use.

    - `Tool(cmd:*)` (older prefix syntax) becomes `Tool(cmd *)`, plus the exact `Tool(cmd)`.
    - Every command rule exists for both the Bash and the PowerShell tool (Windows has both).
    - `python3 ...` also gets `python ...`, `py ...` and `py -3 ...` (Windows rarely has `python3`).
    """
    out = []
    for rule in rules:
        match = _SHELL_RULE.match(rule)
        if not match:
            out.append(rule)
            continue
        spec = match.group(2).strip()
        if spec.endswith(":*"):
            spec = spec[:-2].rstrip() + " *"
        base = spec[:-2].rstrip() if spec.endswith(" *") else spec
        commands = {base}
        if base.startswith("python3 "):
            rest = base[len("python3 "):]
            commands |= {f"python {rest}", f"py {rest}", f"py -3 {rest}"}
        for command in sorted(commands):
            for tool in ("Bash", "PowerShell"):
                out += [f"{tool}({command})", f"{tool}({command} *)"]
    return list(dict.fromkeys(out))


def arm_meta(arm: str) -> dict:
    return json.loads((ARMS / arm / "arm.json").read_text())


def arm_overlays(arm: str, cfg: dict) -> list[Path]:
    meta = arm_meta(arm)
    if meta.get("combine_from_config"):
        parts = cfg.get("a7_components", [])
        if not parts:
            raise RuntimeError("A7 has no components yet: fill 'a7_components' in config.json with the winning arms")
        return [ARMS / p / "overlay" for p in parts]
    overlay = ARMS / arm / "overlay"
    return [overlay] if overlay.exists() else []


def install_overlay(overlay: Path, work: Path) -> None:
    for path in overlay.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(overlay)
        dest = work / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if rel.as_posix() == ".claude/settings.json" and dest.exists():
            merged = deep_merge(json.loads(dest.read_text()), json.loads(path.read_text()))
            dest.write_text(json.dumps(merged, indent=2))
        elif rel.name in ARM_TEXT_FILES and dest.exists():
            dest.write_text(dest.read_text().rstrip() + "\n\n" + path.read_text())
        else:
            shutil.copy2(path, dest)


def arm_overhead_chars(work: Path) -> int:
    """Size of always-loaded arm text (CLAUDE.md + skill descriptions), a proxy for arm overhead."""
    total = 0
    claude_md = work / "CLAUDE.md"
    if claude_md.exists():
        total += len(claude_md.read_text())
    for skill in (work / ".claude" / "skills").rglob("SKILL.md") if (work / ".claude" / "skills").exists() else []:
        total += len(skill.read_text())
    return total


def harness_block_rules() -> list[str]:
    """Deny rules so agents can never read this folder (hidden tests, reference solutions, other results)."""
    posix = ROOT.resolve().as_posix()
    if os.name == "nt":  # C:/Users/... -> //c/Users/... (tested on 2.1.310: the //C:/ spelling never matches)
        roots = [f"//{posix[0].lower()}{posix[2:]}"]
    else:
        roots = [f"/{posix}"]  # /home/... -> //home/... (a leading // means an absolute path)
    # Edit rules cover every file-writing tool; Claude Code rejects Write(path) as a file rule.
    return [f"{tool}({root}/**)" for root in roots for tool in ("Read", "Edit")]


def write_run_settings(run_dir: Path, settings: dict) -> dict:
    """Store the case's final settings OUTSIDE the workspace and return what the command line needs.

    Permissions reach Claude Code three ways at once: this file via --settings, the allow/deny lists via
    --allowedTools/--disallowedTools, and the workspace's own .claude/settings.json.
    """
    path = run_dir / "run-settings.json"
    path.write_text(json.dumps(settings, indent=2))
    return {"settings_file": str(path), "allow": settings["permissions"]["allow"],
            "deny": settings["permissions"]["deny"]}


def arm_applies(arm: str, suite: str) -> bool:
    allowed = arm_meta(arm).get("suites")
    return allowed is None or suite in allowed


def prepare(task: str, arm: str, run_dir: Path, cfg: dict | None = None, dry: bool = False) -> dict:
    cfg = cfg or load_config()
    suite = suite_of(task, cfg)
    if not arm_applies(arm, suite):
        raise RuntimeError(f"arm {arm} does not apply to the {suite} suite")
    work = run_dir / "work"
    copy_tree(target_dir(suite, cfg), work)

    setup = tasks_dir(suite, cfg) / task / "setup.py"
    if setup.exists():
        sh([sys.executable, str(setup), str(work)], check=True)

    permissions = {"allow": cfg["permissions"]["allow"] + suite_spec(suite, cfg).get("extra_allow", []),
                   "deny": cfg["permissions"]["deny"] + harness_block_rules()}
    settings = {"permissions": permissions}
    (work / ".claude").mkdir(exist_ok=True)
    (work / ".claude" / "settings.json").write_text(json.dumps(settings, indent=2))

    for overlay in arm_overlays(arm, cfg):
        install_overlay(overlay, work)

    meta = arm_meta(arm)
    if meta.get("needs_brief"):
        brief = VENDOR / ("briefs_dry" if dry else "briefs") / f"{target_version(suite)}.md"
        if not brief.exists():
            raise RuntimeError(f"A8 needs a brief: run `python3 harness/build_brief.py` first ({brief.name} missing)")
        shutil.copy2(brief, work / "BRIEF.md")

    settings_file = work / ".claude" / "settings.json"
    final = json.loads(settings_file.read_text())
    final["permissions"]["allow"] = expand_rules(final["permissions"].get("allow", []))
    settings_file.write_text(json.dumps(final, indent=2))
    perms = write_run_settings(run_dir, final)

    git(work, "init", "-q")
    git(work, "add", "-A")
    git(work, "commit", "-q", "-m", "base")
    return {"work": work, "suite": suite, "arm_overhead_chars": arm_overhead_chars(work), "perms": perms}


def install_hidden(task: str, work: Path) -> None:
    hidden = work / "_hidden"
    hidden.mkdir(exist_ok=True)
    src = tasks_dir(suite_of(task)) / task / "hidden"
    if src.exists():
        for f in src.iterdir():
            if f.is_file():
                shutil.copy2(f, hidden / f.name)
    support = Path(__file__).resolve().parent / "hidden_support"
    shutil.copy2(support / "conftest.py", hidden / "conftest.py")
    shutil.copy2(support / "netblock.py", hidden / "netblock.py")
