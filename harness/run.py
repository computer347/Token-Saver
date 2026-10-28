"""One isolated run: fresh workspace + fresh, context-free Claude Code process -> one results row.

Usage: python3 harness/run.py ARM TASK [--rep N] [--dry-run] [--keep]
"""
import argparse
import json
import os
import shutil
import sys
import tempfile
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (RESULTS, RUNS_FILE, VENDOR, append_jsonl, claude_cmd, load_config, now, sh, suite_of,
                    suite_spec, tasks_dir, target_version)
from extract import add_usage, diff_stats, parse_result_json, transcript_stats, usage_from_result, weighted
from quality import code_quality
from workspace import arm_meta, install_hidden, prepare

HARNESS = Path(__file__).resolve().parent
STRIP_ENV = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SSE_PORT", "CLAUDE_PROJECT_DIR")
# Variables that would silently change model, effort, thinking budget or billing for some runs.
CONFOUNDING_ENV = ("CLAUDE_CODE_EFFORT_LEVEL", "ANTHROPIC_MODEL", "ANTHROPIC_DEFAULT_OPUS_MODEL",
                   "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL", "ANTHROPIC_SMALL_FAST_MODEL",
                   "CLAUDE_CODE_SUBAGENT_MODEL", "MAX_THINKING_TOKENS", "CLAUDE_CODE_MAX_OUTPUT_TOKENS",
                   "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL")
LIMIT_WORDS = ("usage limit", "rate limit", "limit reached", "limit will reset", "resets at", "hit your limit", "limit · resets", "session limit", "weekly limit")


def arm_args(arm: str) -> list[str]:
    meta = arm_meta(arm)
    args = list(meta.get("cli_args", []))
    if meta.get("plugin"):
        info_file = VENDOR / f"{meta['plugin']}.json"
        if not info_file.exists():
            raise RuntimeError(f"{arm} needs vendor/{meta['plugin']}.json: run preflight with this arm in the plan")
        info = json.loads(info_file.read_text())
        if not info.get("validated"):
            raise RuntimeError(f"{meta['plugin']} failed `claude plugin validate`: {info.get('validate_output', '')[-200:]}")
        args += ["--plugin-dir", info["plugin_dir"]]
    return args


def trusted_project_keys(work: Path) -> list[str]:
    """How Claude Code spells a project path in .claude.json: forward slashes (C:/Users/... on Windows)."""
    return list(dict.fromkeys(p.as_posix() for p in (Path(os.path.abspath(work)), Path(work).resolve())))


def make_env(cfg: dict, config_dir: Path, work: Path, task: str, step: int, dry: bool) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in STRIP_ENV + CONFOUNDING_ENV}
    if cfg.get("isolate_config", True):
        config_dir.mkdir(parents=True, exist_ok=True)
        # Merge rather than overwrite: later steps (--continue) reuse the state Claude Code saved here.
        state_file = config_dir / ".claude.json"
        state = json.loads(state_file.read_text()) if state_file.exists() else {}
        state["hasCompletedOnboarding"] = True
        # Untrusted workspaces silently skip project settings (permissions, skills, agents, hooks).
        for key in trusted_project_keys(work):
            state.setdefault("projects", {}).setdefault(key, {})["hasTrustDialogAccepted"] = True
        state_file.write_text(json.dumps(state))
        env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    env["DISABLE_AUTOUPDATER"] = "1"
    env["PYTHONUTF8"] = "1"  # Windows defaults to cp1252; prompts and code contain non-ASCII text
    if dry:
        env["TB_TASK"], env["TB_STEP"] = task, str(step)
    return env


def build_cmd(cfg: dict, prompt: str, extra: list[str], cont: bool, max_turns: int | None = None,
              perms: dict | None = None) -> list[str]:
    launcher = claude_cmd(cfg)
    if launcher[0].lower().endswith((".cmd", ".bat")) and "\n" in prompt:
        # cmd.exe would cut the prompt at the newline and drop every flag after it (model, JSON, permissions).
        raise RuntimeError(f"{launcher[0]} is a cmd.exe wrapper that cannot pass a multi-line prompt; "
                           "set claude_bin in config.json to the claude.exe it starts")
    cmd = [*launcher, "-p", prompt, "--output-format", "json", "--model", cfg["model"],
           "--max-turns", str(max_turns or cfg["max_turns"]), "--permission-mode", cfg["permission_mode"]]
    if cont:
        cmd.append("--continue")
    if perms:
        # Hand permissions over explicitly instead of relying on the workspace's settings file being loaded.
        cmd += ["--settings", perms["settings_file"]]
        # One argument per rule, as in the documented examples (`--allowedTools "Bash(git log *)" "Read"`);
        # the rules contain spaces, so a single comma-joined string could be split in the wrong places.
        if perms.get("allow"):
            cmd += ["--allowedTools", *perms["allow"]]
        if perms.get("deny"):
            cmd += ["--disallowedTools", *perms["deny"]]
    return cmd + extra


def task_prompts(task: str, variant: str) -> list[str]:
    """Step 1 is prompts/<variant>.md, then <variant>_step2.md, _step3.md ... If contract/stepN.md exists,
    it replaces {{CONTRACT}}, so every wording carries the identical interface."""
    base = tasks_dir(suite_of(task)) / task
    files = [base / "prompts" / f"{variant}.md"]
    n = 2
    while (base / "prompts" / f"{variant}_step{n}.md").exists():
        files.append(base / "prompts" / f"{variant}_step{n}.md")
        n += 1
    steps = []
    for i, f in enumerate(files, start=1):
        text = f.read_text().strip()
        contract = base / "contract" / f"step{i}.md"
        if "{{CONTRACT}}" in text:
            if not contract.exists():
                raise FileNotFoundError(f"{f.name} needs {contract}")
            text = text.replace("{{CONTRACT}}", contract.read_text().strip())
        steps.append(text)
    return steps


def run_one(arm: str, task: str, rep: int = 1, cfg: dict | None = None, dry: bool = False,
            keep: bool = False, claude_version: str = "", variant: str = "v1") -> dict:
    cfg = cfg or load_config()
    run_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{arm}-{task}-{variant}-r{rep}-{uuid.uuid4().hex[:6]}"
    run_dir = Path(tempfile.mkdtemp(prefix="tb-"))
    config_dir = run_dir / "claude-config"
    suite = suite_of(task, cfg)
    spec = suite_spec(suite, cfg)
    row = {"run_id": run_id, "battery_version": cfg["battery_version"], "model": cfg["model"], "arm": arm,
           "suite": suite, "task": task, "variant": variant, "rep": rep, "started": now(),
           "target_version": target_version(suite),
           "claude_version": claude_version, "dry_run": dry, "status": "infra", "error": ""}
    t0 = time.time()
    usage, cost, turns, step_info = {}, 0.0, 0, []
    try:
        prep = prepare(task, arm, run_dir, cfg, dry)
        work = prep["work"]
        row["arm_overhead_chars"] = prep["arm_overhead_chars"]
        extra = arm_args(arm)
        prompts = task_prompts(task, variant)

        for step, text in enumerate(prompts):
            prompt = f"[run {run_id}] {text}" if step == 0 else text  # nonce defeats cross-run cache reuse
            env = make_env(cfg, config_dir, work, task, step, dry)
            proc = sh(build_cmd(cfg, prompt, extra, cont=step > 0, max_turns=spec.get("max_turns"), perms=prep["perms"]),
                      cwd=work, env=env, timeout=spec.get("run_timeout_minutes", cfg["run_timeout_minutes"]) * 60)
            res = parse_result_json(proc.stdout)
            if not res:
                raise RuntimeError(f"no JSON from claude (exit {proc.returncode}): {(proc.stderr or proc.stdout)[-4000:]}")
            text_out = json.dumps(res, ensure_ascii=False).lower()  # keep "·" so "limit · resets" matches
            if res.get("is_error") and any(w in text_out for w in LIMIT_WORDS):
                row.update(status="limit", error=str(res.get("result", ""))[:300])
                return row
            if res.get("is_error") and res.get("subtype") == "success":  # an API error, not the agent's work
                raise RuntimeError(f"claude returned an error: {str(res.get('result', ''))[:300]}")
            usage = add_usage(usage, usage_from_result(res))
            cost += float(res.get("total_cost_usd") or 0)
            turns += int(res.get("num_turns") or 0)
            step_info.append({"stderr_tail": (proc.stderr or "")[-300:],
                              "subtype": res.get("subtype"), "is_error": res.get("is_error"),
                              "permission_denials": len(res.get("permission_denials") or []),
                              "denied": [f"{d.get('tool_name')}: {json.dumps(d.get('tool_input'))[:150]}"
                                         for d in res.get("permission_denials") or []]})

        install_hidden(task, work)
        env = {**os.environ, "PYTHONUTF8": "1", "PYTHONPATH": str(HARNESS), "TB_SUCCESS_THRESHOLD": str(spec.get("success_threshold", 1.0)),
               "TB_ACCEPTANCE_TOTAL": str(spec.get("acceptance_tests", 0))}
        check = parse_result_json(sh([sys.executable, str(tasks_dir(suite) / task / "check.py")], cwd=work, env=env,
                                     timeout=1200).stdout)
        stats = transcript_stats(config_dir) if cfg.get("isolate_config", True) else {}
        tokens = stats.get("tokens_total") or usage
        row.update({
            "status": "ok" if check.get("success") else "task_fail",
            "success": bool(check.get("success")),
            "checks": check.get("checks", []),
            **check.get("metrics", {}),
            "tokens_json": usage,
            "tokens": tokens,
            "weighted_tokens": round(weighted(tokens, cfg["weights"]), 1),
            "weighted_tokens_json": round(weighted(usage, cfg["weights"]), 1) if usage else None,
            "api_cost_usd": round(cost, 4),
            "num_turns": turns,
            "steps": step_info,
            **{k: v for k, v in stats.items() if k not in ("tokens_total",)},
            **diff_stats(work),
            **code_quality(work),
        })
    except Exception as exc:  # noqa: BLE001 - every failure must become a row
        kind = "timeout" if "timed out" in str(exc).lower() or exc.__class__.__name__ == "TimeoutExpired" else "infra"
        row.update(status="task_fail" if kind == "timeout" else "infra", success=False, error=f"{kind}: {exc}"[:4500])
        if "weighted_tokens" not in row:  # a run that timed out (or whose check hung) still spent its tokens
            try:
                stats = transcript_stats(config_dir) if cfg.get("isolate_config", True) and config_dir.exists() else {}
            except Exception:  # noqa: BLE001 - a half-written transcript must not hide the failure
                stats = {}
            tokens = stats.get("tokens_total") or usage
            if tokens:
                row.update(tokens=tokens, weighted_tokens=round(weighted(tokens, cfg["weights"]), 1),
                           api_cost_usd=round(cost, 4), num_turns=turns, steps=step_info)
    finally:
        row["wall_seconds"] = round(time.time() - t0, 1)
        if keep or row["status"] == "infra":
            dest = RESULTS / "kept_runs" / run_id
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(run_dir), dest)
            row["kept_at"] = str(dest)
        else:
            shutil.rmtree(run_dir, ignore_errors=True)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arm")
    ap.add_argument("task")
    ap.add_argument("--rep", type=int, default=1)
    ap.add_argument("--variant", default="v1")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--no-log", action="store_true")
    a = ap.parse_args()
    row = run_one(a.arm, a.task, a.rep, dry=a.dry_run, keep=a.keep, variant=a.variant)
    if not a.no_log:
        append_jsonl(RUNS_FILE, row)
    print(json.dumps({k: row.get(k) for k in ("run_id", "status", "success", "weighted_tokens", "error")}, indent=2))


if __name__ == "__main__":
    main()
