"""Pre-flight checks. Turns Ponytail off in your normal setup, then proves one isolated, context-free run works.

Usage: python3 harness/preflight.py [--mode smoke|pilot|full|refs] [--dry-run]
"""
import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ponytail
from common import RESULTS, claude_cmd, load_config, now, resolve_mode, sh
from run import CONFOUNDING_ENV
from workspace import arm_meta
from extract import parse_result_json, transcript_stats, usage_from_result
from run import build_cmd, make_env
from workspace import prepare

SMOKE_PROMPT = ("Run `" + ("python" if os.name == "nt" else "python3") +
                " -m pytest -q` in this directory and reply with only the number of tests that passed.")


def diagnose_permissions(cfg, work, run_dir, record):
    """The full setup was denied: try each way of granting permission on its own, so the report says which works."""
    rules = ["Bash(python -m pytest *)", "PowerShell(python -m pytest *)",
             "Bash(python3 -m pytest *)", "PowerShell(python3 -m pytest *)",
             "Bash(py -m pytest *)", "PowerShell(py -m pytest *)"]
    probe_settings = run_dir / "probe-settings.json"
    probe_settings.write_text(json.dumps({"permissions": {"allow": rules}}))
    bare = work.parent / "probe-work"
    shutil.copytree(work, bare)
    shutil.rmtree(bare / ".claude", ignore_errors=True)  # no project settings in the probe workspace
    probes = {
        "--allowedTools only": (bare, ["--allowedTools", *rules]),
        "--settings file only": (bare, ["--settings", str(probe_settings)]),
        "project .claude/settings.json only": (work, []),
        "--permission-mode dontAsk + --allowedTools": (bare, ["--permission-mode", "dontAsk", "--allowedTools", *rules]),
    }
    print("       Diagnosing which way of granting permission works on this machine:")
    for i, (name, (cwd, extra)) in enumerate(probes.items()):
        env = make_env(cfg, run_dir / f"claude-config-probe{i}", cwd, "PROBE", 0, False)
        cmd = build_cmd(cfg, SMOKE_PROMPT, [], False, max_turns=6) + extra
        proc = sh(cmd, cwd=cwd, env=env, timeout=600)
        res = parse_result_json(proc.stdout)
        ok = bool(res) and not res.get("permission_denials") and "21" in str(res.get("result", ""))
        detail = (str(res.get("result", ""))[:80] if res else (proc.stderr or proc.stdout)[-200:]).replace("\n", " ")
        record(f"Diagnosis: {name}", ok, detail, critical=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="smoke")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    _, plan_arms, cfg = resolve_mode(load_config(), a.mode)
    plan = {"arms": plan_arms}
    checks = []

    def record(name, ok, detail="", critical=True):
        checks.append({"check": name, "ok": bool(ok), "critical": critical, "detail": str(detail)[:500]})
        mark = "PASS" if ok else ("FAIL" if critical else "WARN")
        print(f"[{mark}] {name}" + (f" — {detail}" if detail else ""))

    version = sh([*claude_cmd(cfg), "--version"])
    claude_version = version.stdout.strip()
    record("Claude Code installed", version.returncode == 0, claude_version or version.stderr[-200:])
    launcher = claude_cmd(cfg)
    record("Claude Code starts without a cmd.exe wrapper (multi-line prompts and flags arrive intact)",
           not launcher[0].lower().endswith((".cmd", ".bat")), " ".join(launcher))

    token_set = bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"))
    record("CLAUDE_CODE_OAUTH_TOKEN set (isolated runs have no saved login)",
           token_set or a.dry_run or not cfg.get("isolate_config", True),
           "" if token_set else "run `claude setup-token`, then `export CLAUDE_CODE_OAUTH_TOKEN=...` in this terminal")

    has_pytest = sh([sys.executable, "-c", "import pytest"]).returncode == 0
    record("pytest importable", has_pytest, "" if has_pytest else f"{sys.executable} -m pip install pytest")

    if not a.dry_run:
        state = ponytail.disable(cfg)
        if state["found"]:
            record("Ponytail turned off in your normal Claude Code setup", state["disabled_by_harness"],
                   state["detail"] or "if this failed: open Claude Code → /plugin → disable Ponytail", critical=False)
        else:
            record("Ponytail not installed in your normal setup", True, critical=False)

    present = [k for k in CONFOUNDING_ENV if os.environ.get(k)]
    record("No confounding env vars leak into runs", True,
           f"present in your shell but stripped from every run: {', '.join(present)}" if present else "", critical=False)

    from vendor import vendor_plugin
    for arm in plan["arms"]:
        meta = arm_meta(arm)
        if meta.get("requires_binary") and not a.dry_run:
            found = shutil.which(meta["requires_binary"])
            record(f"{arm}: `{meta['requires_binary']}` installed", bool(found),
                   found or "install it (for pyright: npm install -g pyright)")
        if meta.get("plugin") and not a.dry_run:
            try:
                info = vendor_plugin(meta["plugin"], cfg)
                record(f"{arm}: plugin {meta['plugin']} pinned and passes `claude plugin validate`", info["validated"],
                       f"{info['commit'][:10]} · {info['validate_output'][-200:]}")
            except Exception as exc:  # noqa: BLE001
                record(f"{arm}: plugin {meta['plugin']} vendored", False, exc)

    if "A8" in plan["arms"]:
        try:
            import build_brief
            record("A8 brief available", True, build_brief.build(cfg, dry=a.dry_run).name)
        except Exception as exc:  # noqa: BLE001
            record("A8 brief available", False, exc)

    smoke = {}
    if all(c["ok"] for c in checks if c["critical"]):
        run_dir = Path(tempfile.mkdtemp(prefix="tb-preflight-"))
        try:
            prep = prepare("T4", "A0", run_dir, cfg, a.dry_run)
            work, perms = prep["work"], prep["perms"]
            env = make_env(cfg, run_dir / "claude-config", work, "SMOKE", 0, a.dry_run)
            proc = sh(build_cmd(cfg, SMOKE_PROMPT, [], False, perms=perms), cwd=work, env=env, timeout=900)
            res = parse_result_json(proc.stdout)
            warnings = (proc.stderr or "").strip()
            if warnings:
                print("       Claude Code printed on stderr:\n         " + warnings[-800:].replace("\n", "\n         "))
            record("Isolated headless run returns JSON", bool(res), (proc.stderr or proc.stdout)[-300:] if not res else "")
            if res:
                record("Run finished without error", not res.get("is_error"), str(res.get("result", ""))[:200])
                denied = res.get("permission_denials") or []
                record("Permissions allow running tests unattended", not denied,
                       json.dumps(denied)[:300] if denied else "")
                if denied and not a.dry_run:
                    diagnose_permissions(cfg, work, run_dir, record)
                record("Model actually ran the tests (answer is 21)", "21" in str(res.get("result", "")),
                       str(res.get("result", ""))[:100], critical=False)
                usage = usage_from_result(res)
                stats = transcript_stats(run_dir / "claude-config")
                trans = stats.get("tokens_total") or {}
                record("Transcript found in isolated config dir", stats.get("transcript_files", 0) > 0,
                       f"{stats.get('transcript_files', 0)} file(s)")
                record("No Ponytail inside the isolated run", stats.get("ponytail_mentions", 0) == 0,
                       f"{stats.get('ponytail_mentions', 0)} mention(s)")
                smoke = {"json_usage": usage, "transcript_usage": trans,
                         "cache_write_1h": usage.get("cache_write_1h"), "cache_write_5m": usage.get("cache_write_5m"),
                         "api_cost_usd": res.get("total_cost_usd")}
                print(f"       token accounting — JSON: {usage}\n       transcript: {trans}")
                print(f"       cache lifetime used — 1h writes: {usage.get('cache_write_1h')}, 5m writes: {usage.get('cache_write_5m')}")

            # Prove the read-block works: plant a secret in the harness folder and ask a fresh agent to read it.
            import secrets
            from common import ROOT
            canary = ROOT / "results" / ".canary"
            canary.parent.mkdir(exist_ok=True)
            token = secrets.token_hex(8)
            canary.write_text(token)
            try:
                env2 = make_env(cfg, run_dir / "claude-config-canary", work, "CANARY", 0, a.dry_run)
                ask = f"Read the file {canary.resolve()} and reply with its exact contents, nothing else."
                res2 = parse_result_json(sh(build_cmd(cfg, ask, [], False, perms=perms), cwd=work, env=env2,
                                            timeout=600).stdout)
                leaked = token in json.dumps(res2)
                record("Agents cannot read the harness folder (canary test)", not leaked,
                       "a fresh agent read a secret planted in the harness folder: hidden tests could leak"
                       if leaked else "the planted secret was not readable", critical=False)
            finally:
                canary.unlink(missing_ok=True)
        finally:
            shutil.rmtree(run_dir, ignore_errors=True)

    record("Billing check done by you (usage panel / usage credits off)", True,
           "manual: compare Settings → Usage before and after tonight", critical=False)
    ok = all(c["ok"] for c in checks if c["critical"])
    out = {"time": now(), "mode": a.mode, "dry_run": a.dry_run, "ok": ok, "claude_version": claude_version,
           "model": cfg["model"], "battery_version": cfg["battery_version"], "checks": checks, "smoke": smoke,
           "confounding_env_present": present}
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / ("preflight_dry.json" if a.dry_run else "preflight.json")).write_text(json.dumps(out, indent=2))
    print("\nPreflight", "PASSED" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
