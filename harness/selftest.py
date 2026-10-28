"""Self-test: run every task and wording through the real harness with a fake `claude`. No tokens spent.

Checks that (1) every task has all three wordings, (2) each checker passes the reference solution and
fails an untouched repo, (3) every arm overlay installs, (4) a full pilot runs in parallel, resumes
without duplicates, and the report renders.
Usage: python3 harness/selftest.py
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
os.environ["TB_CLAUDE_BIN"] = str(HERE / "fake_claude.py")
from common import ROOT as ROOT_DIR, load_config  # noqa: E402
from run import run_one, task_prompts  # noqa: E402

cfg = load_config()
TASK_IDS = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"]
problems = []


def expect(cond, label):
    print(("  ok    " if cond else "  FAIL  ") + label)
    if not cond:
        problems.append(label)


print("Every task has every wording:")
for task in TASK_IDS:
    lens = []
    for v in cfg["variants"]:
        try:
            steps = task_prompts(task, v)
            lens.append(len(steps))
        except FileNotFoundError:
            lens.append(0)
    expect(all(lens) and len(set(lens)) == 1, f"{task}: {dict(zip(cfg['variants'], lens))} step(s) per wording")

print("Every case runs isolated (the fake claude refuses to run anywhere else):")
os.environ["TB_FAKE_SOLVE"] = "1"
iso = run_one("A0", "T4", cfg=cfg, dry=True)
expect(iso.get("status") != "infra", f"a case runs in its own workspace with an empty config dir {iso.get('error', '')}")
outside = subprocess.run([sys.executable, str(HERE / "fake_claude.py"), "-p", "x"], capture_output=True, text=True,
                         cwd=tempfile.gettempdir(), env={k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"})
expect(outside.returncode == 3, "the guard really refuses a non-isolated launch")

from common import claude_cmd  # noqa: E402
with tempfile.TemporaryDirectory() as tmp:
    exe = Path(tmp) / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
    exe.parent.mkdir(parents=True)
    exe.write_text("")
    wrapper = Path(tmp) / "claude.cmd"
    wrapper.write_text('@ECHO off\r\n"%dp0%\\node_modules\\@anthropic-ai\\claude-code\\bin\\claude.exe"   %*\r\n')
    fake_bin = os.environ.pop("TB_CLAUDE_BIN")
    launcher = claude_cmd({"claude_bin": str(wrapper)})
    os.environ["TB_CLAUDE_BIN"] = fake_bin
    expect(Path(launcher[0]) == exe, f"an npm claude.cmd wrapper is bypassed (cmd.exe cuts prompts at newlines): {launcher}")

print("Checkers accept reference solutions and reject untouched repos:")
for i, task in enumerate(TASK_IDS):
    variant = cfg["variants"][i % len(cfg["variants"])]
    os.environ["TB_FAKE_SOLVE"] = "1"
    good = run_one("A0", task, cfg=cfg, dry=True, variant=variant)
    failed = [c["check"] for c in good.get("checks", []) if not c["ok"]]
    expect(good.get("success"), f"{task}/{variant} solved -> success {failed if failed else ''}{good.get('error', '')}")
    os.environ["TB_FAKE_SOLVE"] = "0"
    bad = run_one("A0", task, cfg=cfg, dry=True, variant=variant)
    expect(bad.get("status") == "task_fail", f"{task}/{variant} untouched -> fails")

print("Build suite (B1): four steps, contract inserted, graded by hidden acceptance tests:")
steps = task_prompts("B1", "v2")
expect(len(steps) == 4 and not any("{{CONTRACT}}" in x for x in steps), "B1 has 4 steps with the contract inserted")
os.environ["TB_FAKE_SOLVE"] = "1"
good = run_one("A0", "B1", cfg=cfg, dry=True, variant="v3")
expect(good.get("success") and good.get("pass_rate") == 1.0 and good.get("acceptance_total", 0) >= 80,
       f"reference build passes {good.get('acceptance_passed')}/{good.get('acceptance_total')} hidden tests {good.get('error', '')}")
expect(good.get("package_lines", 0) > 500 and good.get("own_tests_pass") is True, "build metrics recorded (lines, own tests)")
os.environ["TB_FAKE_SOLVE"] = "0"
bad = run_one("A0", "B1", cfg=cfg, dry=True, variant="v1")
expect(bad.get("status") == "task_fail" and bad.get("pass_rate") == 0.0, "an empty build scores 0% and fails")
from workspace import arm_applies, prepare  # noqa: E402
expect(not arm_applies("A8", "build") and arm_applies("A8", "small") and arm_applies("A5", "build"),
       "small-suite-only arms are skipped for builds")
with tempfile.TemporaryDirectory() as tmp:
    settings = json.loads((prepare("B1", "A0", Path(tmp), cfg, True)["work"] / ".claude" / "settings.json").read_text())
    posix = ROOT_DIR.resolve().as_posix()  # rules use forward slashes on every OS (//c/dev/... on Windows)
    if os.name == "nt":
        posix = f"{posix[0].lower()}{posix[2:]}"
    deny = settings["permissions"]["deny"]
    expect(any(rule.startswith("Read(") and rule.endswith(f"/{posix}/**)") for rule in deny),
           f"agents are denied read access to the harness folder ({posix})")
    from run import make_env  # noqa: E402
    work = Path(tmp) / "work"
    make_env(cfg, Path(tmp) / "claude-config", work, "B1", 0, True)
    state = json.loads((Path(tmp) / "claude-config" / ".claude.json").read_text())
    expect(state.get("projects", {}).get(work.resolve().as_posix(), {}).get("hasTrustDialogAccepted") is True,
           "the case workspace is marked trusted, so project settings, skills, agents and hooks load")

print("Grading can't be bent by the agent's own files; timeouts keep their cost:")
from checklib import Check  # noqa: E402
with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp)
    (work / "_hidden").mkdir()
    (work / "_hidden" / "test_probe.py").write_text(
        "import pytest\n\ndef test_a():\n    pass\n\ndef test_b():\n    pass\n\n"
        "@pytest.mark.skip\ndef test_c():\n    pass\n")
    (work / "conftest.py").write_text("raise RuntimeError('agent conftest must not load')\n")
    (work / "pyproject.toml").write_text("[tool.pytest.ini_options]\naddopts = '-k nothing_matches'\n")
    here = os.getcwd()
    os.chdir(work)
    os.environ["TB_ACCEPTANCE_TOTAL"] = "3"
    try:
        probe = Check()
        rate = probe.acceptance()
    finally:
        os.chdir(here)
        os.environ.pop("TB_ACCEPTANCE_TOTAL")
    expect(abs(rate - 2 / 3) < 1e-6 and probe.metrics.get("acceptance_total") == 3,
           f"agent conftest/addopts ignored, skipped test counts as failed (2/3 expected, got {probe.metrics})")
os.environ["TB_FAKE_HANG"] = "1"
hang_cfg = json.loads(json.dumps(cfg))
hang_cfg["suites"]["small"]["run_timeout_minutes"] = 0.1
hung = run_one("A0", "T4", cfg=hang_cfg, dry=True)
os.environ.pop("TB_FAKE_HANG")
expect(hung.get("status") == "task_fail" and "timeout" in hung.get("error", "") and (hung.get("weighted_tokens") or 0) > 0,
       f"a timed-out run keeps its token cost (weighted={hung.get('weighted_tokens')}, {hung.get('error', '')[:80]})")
for fake_err, want in (("You've hit your limit · resets 3am (Europe/Helsinki)", "limit"), ("API Error: 500 overloaded", "infra")):
    os.environ["TB_FAKE_ERROR"] = fake_err
    errored = run_one("A0", "T4", cfg=cfg, dry=True)
    os.environ.pop("TB_FAKE_ERROR")
    expect(errored.get("status") == want, f"an is_error result ({fake_err[:20]}...) is recorded as {want}, not task_fail (got {errored.get('status')})")
hook = ROOT_DIR / "arms" / "A5" / "overlay" / ".claude" / "hooks" / "a5_pretool.py"


def a5(command):
    return subprocess.run([sys.executable, str(hook)], input=json.dumps({"tool_input": {"command": command}}),
                          capture_output=True, text=True).stdout.strip()


expect(a5("python -m pytest -q") and not a5("python -m pytest -q && rm -rf x") and not a5("git diff; curl x"),
       "A5 auto-approves only single plain test/git commands, never chained ones")

print("Arm overlays install and run:")
os.environ["TB_FAKE_SOLVE"] = "1"
import build_brief  # noqa: E402
build_brief.build(cfg, dry=True)
from common import VENDOR  # noqa: E402
fake_plugin = Path(tempfile.mkdtemp())
VENDOR.mkdir(exist_ok=True)
(VENDOR / "pyright-lsp.json").write_text(json.dumps({"plugin_dir": str(fake_plugin), "validated": True}))
try:
    for arm in ["A0b", "P1", "A1", "A2", "A3", "A4", "A5", "A6a", "A6b", "A8", "A9", "A9m", "A10", "A11", "A12", "A13"]:
        row = run_one(arm, "T7", cfg=cfg, dry=True, variant="v2")
        expect(row.get("success") and "complexity_delta" in row, f"{arm} on T7/v2 {row.get('error', '')}")
    (VENDOR / "pyright-lsp.json").write_text(json.dumps({"plugin_dir": str(fake_plugin), "validated": False,
                                                          "validate_output": "invalid"}))
    row = run_one("A10", "T1", cfg=cfg, dry=True)
    expect(row.get("status") == "infra" and "validate" in row.get("error", ""), "A10 refuses to run with an unvalidated plugin")
finally:
    (VENDOR / "pyright-lsp.json").unlink(missing_ok=True)
    import shutil
    shutil.rmtree(cfg_kept := (Path(__file__).resolve().parents[1] / "results" / "kept_runs"), ignore_errors=True)

print("Pilot (1 rep per wording), parallel, resumable (dry run):")
with tempfile.TemporaryDirectory() as tmp:
    runs = Path(tmp) / "runs.jsonl"
    env = {**os.environ, "TB_FAKE_SOLVE": "1"}
    pre = subprocess.run([sys.executable, str(HERE / "preflight.py"), "--mode", "pilot", "--dry-run"],
                         capture_output=True, text=True, env=env)
    expect(pre.returncode == 0, "preflight (dry) passes" + ("" if pre.returncode == 0 else "\n" + pre.stdout[-800:]))
    expected = len(cfg["modes"]["pilot"]["arms"]) * len(cfg["modes"]["pilot"]["tasks"]) * len(cfg["variants"])
    cmd = [sys.executable, str(HERE / "battery.py"), "--mode", "pilot", "--dry-run", "--seed", "1", "--reps", "1",
           "--workers", "4", "--runs-file", str(runs)]
    bat = subprocess.run(cmd, capture_output=True, text=True, env=env)
    rows = [json.loads(l) for l in runs.read_text().splitlines()] if runs.exists() else []
    expect(bat.returncode == 0 and len(rows) == expected,
           f"pilot completes {expected} runs (got {len(rows)})" + ("" if bat.returncode == 0 else "\n" + bat.stderr[-800:]))
    cells = {(r["arm"], r["task"], r["variant"]) for r in rows}
    expect(len(cells) == expected, f"balanced: {len(cells)} arm×task×wording cells")
    again = subprocess.run(cmd, capture_output=True, text=True, env=env)
    expect(len(runs.read_text().splitlines()) == expected, "re-running resumes with no duplicate runs")
    rep = subprocess.run([sys.executable, str(HERE / "report.py"), "--dry-run", "--runs-file", str(runs),
                          "--out-dir", tmp], capture_output=True, text=True, env=env)
    report = Path(tmp) / "REPORT_dry.md"
    expect(rep.returncode == 0 and report.exists(), "report renders" + ("" if rep.returncode == 0 else "\n" + rep.stderr[-800:]))
    if report.exists():
        text = report.read_text()
        for section in ("Method checks", "A/A check", "Placebo", "against the placebo", "actually happen",
                        "Code quality", "do and don't show"):
            expect(section in text, f"report has section: {section}")

print("Build pilot + cross-suite report (dry run):")
with tempfile.TemporaryDirectory() as tmp:
    runs = Path(tmp) / "runs.jsonl"
    env = {**os.environ, "TB_FAKE_SOLVE": "1"}
    for mode, extra in (("pilot", ["--reps", "1"]), ("pilot-build", [])):
        subprocess.run([sys.executable, str(HERE / "preflight.py"), "--mode", mode, "--dry-run"],
                       capture_output=True, text=True, env=env)
        bat = subprocess.run([sys.executable, str(HERE / "battery.py"), "--mode", mode, "--dry-run", "--seed", "2",
                              "--workers", "4", "--runs-file", str(runs), *extra], capture_output=True, text=True, env=env)
        expect(bat.returncode == 0, f"{mode} dry run completes" + ("" if bat.returncode == 0 else "\n" + bat.stderr[-600:]))
    rows = [json.loads(l) for l in runs.read_text().splitlines()]
    expect(sum(r["task"] == "B1" for r in rows) == 18, f"build pilot ran 18 builds (got {sum(r['task'] == 'B1' for r in rows)})")
    rep = subprocess.run([sys.executable, str(HERE / "report.py"), "--dry-run", "--runs-file", str(runs), "--out-dir", tmp],
                         capture_output=True, text=True, env=env)
    text = (Path(tmp) / "REPORT_dry.md").read_text() if (Path(tmp) / "REPORT_dry.md").exists() else ""
    expect(rep.returncode == 0 and "hold across suites" in text and "Hidden acceptance tests" in text
           and (Path(tmp) / "REPORT_build_dry.md").exists(), "cross-suite report with build pass rates"
           + ("" if rep.returncode == 0 else "\n" + rep.stderr[-600:]))
    if text:
        print("\n" + "\n".join(text.splitlines()[:12]))

print("\nSELF-TEST " + ("PASSED" if not problems else f"FAILED ({len(problems)} problem(s))"))
sys.exit(1 if problems else 0)
