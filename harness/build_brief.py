"""Build the A8 'overnight brief' once per target-repo version, in its own isolated run.

Usage: python3 harness/build_brief.py [--dry-run]
"""
import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RESULTS, TARGET, VENDOR, append_jsonl, copy_tree, git, load_config, now, sh, target_version
from extract import parse_result_json, transcript_stats, usage_from_result, weighted
from run import build_cmd, make_env

PROMPT = ("Write BRIEF.md in the project root: a compact map of this project for a developer who has never seen it. "
          "List each module with its purpose and its key functions (name, file, one line each), how data flows "
          "between modules, and how to run the tests. Keep it under 60 lines. Do not change any other file.")


def build(cfg=None, dry=False) -> Path:
    cfg = cfg or load_config()
    out = VENDOR / ("briefs_dry" if dry else "briefs") / f"{target_version()}.md"
    if out.exists():
        return out
    run_dir = Path(tempfile.mkdtemp(prefix="tb-brief-"))
    try:
        work = run_dir / "work"
        copy_tree(TARGET, work)
        from workspace import expand_rules, harness_block_rules, write_run_settings
        settings = {"permissions": {"allow": expand_rules(cfg["permissions"]["allow"]),
                                    "deny": cfg["permissions"]["deny"] + harness_block_rules()}}
        (work / ".claude").mkdir(exist_ok=True)
        (work / ".claude" / "settings.json").write_text(json.dumps(settings, indent=2))
        perms = write_run_settings(run_dir, settings)
        git(work, "init", "-q")
        git(work, "add", "-A")
        git(work, "commit", "-q", "-m", "base")
        env = make_env(cfg, run_dir / "claude-config", work, "BRIEF", 0, dry)
        proc = sh(build_cmd(cfg, PROMPT, [], False, perms=perms), cwd=work, env=env, timeout=cfg["run_timeout_minutes"] * 60)
        res = parse_result_json(proc.stdout)
        brief = work / "BRIEF.md"
        if not brief.exists():
            raise RuntimeError(f"brief run produced no BRIEF.md: {(proc.stderr or proc.stdout)[-300:]}")
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(brief, out)
        stats = transcript_stats(run_dir / "claude-config")
        tokens = stats.get("tokens_total") or usage_from_result(res)
        append_jsonl(RESULTS / "brief_builds.jsonl", {
            "time": now(), "target_version": target_version(), "model": cfg["model"], "dry_run": dry,
            "tokens": tokens, "weighted_tokens": round(weighted(tokens, cfg["weights"]), 1),
            "api_cost_usd": res.get("total_cost_usd"), "brief_chars": len(brief.read_text())})
        return out
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    print(build(dry=ap.parse_args().dry_run))
