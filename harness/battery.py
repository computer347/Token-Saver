"""Run a battery: every arm × task × wording, repeated, in balanced randomized blocks, in parallel.

Each run is a fresh, context-free `claude -p` process (see run.py). Resumable: re-running the same
command skips finished cells and retries infrastructure failures.

Usage: python3 harness/battery.py --mode smoke|pilot|full|refs|confirm [--workers N] [--dry-run]
"""
import argparse
import json
import random
import statistics
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (RESULTS, RUNS_FILE, append_jsonl, claude_cmd, load_config, now, read_jsonl, resolve_mode, sh,
                    suite_of, target_version)
from run import run_one
from workspace import arm_applies, arm_meta


def build_plan(arms, tasks, variants, reps, done, infra, max_retries, rng):
    """Balanced blocks: each block is one (task, wording) with every arm once, in shuffled order."""
    plan = []
    for rep in range(1, reps + 1):
        blocks = [(t, v) for t in tasks for v in variants]
        rng.shuffle(blocks)
        for task, variant in blocks:
            for arm in rng.sample(arms, len(arms)):
                if not arm_applies(arm, suite_of(task)):
                    continue
                key = (arm, task, variant)
                if done[key] >= rep or infra[key] >= max_retries:
                    continue
                plan.append((arm, task, variant, rep))
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="smoke")
    ap.add_argument("--arms", help="comma-separated override")
    ap.add_argument("--tasks", help="comma-separated override")
    ap.add_argument("--variants", help="comma-separated override, e.g. v1,v3")
    ap.add_argument("--reps", type=int, help="override reps per wording")
    ap.add_argument("--workers", type=int)
    ap.add_argument("--max-runs", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--runs-file", default=str(RUNS_FILE))
    a = ap.parse_args()

    mode, mode_arms, cfg = resolve_mode(load_config(), a.mode)
    arms = a.arms.split(",") if a.arms else mode_arms
    tasks = a.tasks.split(",") if a.tasks else mode["tasks"]
    variants = a.variants.split(",") if a.variants else cfg["variants"]
    reps = a.reps or mode["reps_per_variant"]
    workers = max(1, a.workers or cfg.get("workers", 1))
    limits = cfg["limits"]
    max_runs = a.max_runs or limits["max_runs_per_night"]
    runs_file = Path(a.runs_file)
    rng = random.Random(a.seed)

    usable = []
    for arm in arms:
        meta = arm_meta(arm)
        if meta.get("enabled") is False:
            print(f"skip {arm}: disabled ({meta.get('notes', '')})")
        elif meta.get("combine_from_config") and not cfg.get("a7_components"):
            print(f"skip {arm}: a7_components is empty in config.json")
        else:
            usable.append(arm)
    if "A0" not in usable:
        print("warning: no baseline (A0) in this plan; ratios can't be computed")

    pre_file = RESULTS / ("preflight_dry.json" if a.dry_run else "preflight.json")
    pre = json.loads(pre_file.read_text()) if pre_file.exists() else {}
    if not pre.get("ok"):
        sys.exit(f"Preflight hasn't passed ({pre_file.name}); run harness/preflight.py first.")
    version_now = sh([*claude_cmd(cfg), "--version"]).stdout.strip()
    if version_now != pre.get("claude_version"):
        sys.exit(f"Claude Code version changed ({pre.get('claude_version')} -> {version_now}): "
                 "bump battery_version in config.json and re-run preflight.")
    if pre.get("model") != cfg["model"]:
        sys.exit("Model in config.json differs from preflight: bump battery_version and re-run preflight.")

    def same_battery(row):
        return (row.get("battery_version") == cfg["battery_version"] and row.get("model") == cfg["model"]
                and row.get("target_version") == target_version(row.get("suite", "small"))
                and bool(row.get("dry_run")) == a.dry_run)

    history = [r for r in read_jsonl(runs_file) if same_battery(r)]
    key = lambda r: (r["arm"], r["task"], r.get("variant", "v1"))
    done = Counter(key(r) for r in history if r["status"] in ("ok", "task_fail"))
    infra = Counter(key(r) for r in history if r["status"] == "infra")
    plan = build_plan(usable, tasks, variants, reps, done, infra, limits["max_retries_per_cell"], rng)
    total_planned = sum(1 for arm in usable for t in tasks if arm_applies(arm, suite_of(t, cfg))) * len(variants) * reps
    capped = len(plan) > max_runs
    plan = plan[:max_runs]

    print(f"Battery {cfg['battery_version']} · {a.mode} · model {cfg['model']} · {workers} worker(s)")
    print(f"arms {usable} · tasks {tasks} · wordings {variants} · {reps} rep(s) each")
    print(f"{total_planned} runs planned, {sum(done.values())} already done, {len(plan)} queued this session")

    started, session, stop_reason = time.time(), [], "plan complete"
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_one, arm, task, rep, cfg, a.dry_run, False, version_now, variant):
                   (arm, task, variant, rep) for arm, task, variant, rep in plan}
        stopping = False
        for fut in as_completed(futures):
            if fut.cancelled():
                continue
            arm, task, variant, rep = futures[fut]
            try:
                row = fut.result()
            except Exception as exc:  # noqa: BLE001
                row = {"arm": arm, "task": task, "variant": variant, "rep": rep, "status": "infra",
                       "error": f"harness: {exc}", "battery_version": cfg["battery_version"], "model": cfg["model"],
                       "target_version": target_version(), "dry_run": a.dry_run, "run_id": f"crash-{arm}-{task}-{variant}"}
            append_jsonl(runs_file, row)
            session.append(row)
            print(f"{now()} [{len(session)}/{len(plan)}] {arm:4} {task} {variant} r{rep} -> {row['status']:9} "
                  f"weighted={row.get('weighted_tokens')} {row.get('error', '')[:100]}", flush=True)
            if stopping:
                continue
            reason = None
            if row["status"] == "limit":
                reason = "hit the usage limit; re-run the same command after the reset to resume"
            elif time.time() - started > limits["max_hours"] * 3600:
                reason = f"reached max hours ({limits['max_hours']})"
            elif len(session) >= 5:
                rate = sum(r["status"] == "infra" for r in session) / len(session)
                if rate > limits["max_infra_failure_rate"]:
                    reason = f"infrastructure failure rate {rate:.0%}: fix the harness first"
            if reason:
                stopping, stop_reason = True, reason
                for other in futures:
                    other.cancel()  # queued runs are dropped; runs already in progress finish and are recorded
    if capped and stop_reason == "plan complete":
        stop_reason = f"session cap of {max_runs} runs reached; re-run to continue"
    write_night_report(session, stop_reason, started, a, cfg, total_planned, runs_file, same_battery)
    print(f"Stopped: {stop_reason}. See results/NIGHT_REPORT{'_dry' if a.dry_run else ''}.md")


def write_night_report(session, stop_reason, started, a, cfg, total_planned, runs_file, same_battery):
    all_rows = [r for r in read_jsonl(runs_file) if same_battery(r) and r["status"] in ("ok", "task_fail")]
    by_status = Counter(r["status"] for r in session)
    lines = [f"# Night report — {a.mode}{' (dry run)' if a.dry_run else ''}", "",
             f"- Model {cfg['model']} · battery {cfg['battery_version']}",
             f"- Started {time.strftime('%Y-%m-%d %H:%M', time.localtime(started))}, ended {time.strftime('%H:%M')}",
             f"- Runs this session: {len(session)} ({', '.join(f'{k}: {v}' for k, v in by_status.items()) or 'none'})",
             f"- Stop reason: {stop_reason}",
             f"- Progress for this mode: {min(len(all_rows), total_planned)} of {total_planned} completed runs in the log",
             "", "## This session, per arm", "",
             "| Arm | Runs | Successes | Mean weighted tokens | SD | Median API-equivalent $ |",
             "| --- | --- | --- | --- | --- | --- |"]
    groups = defaultdict(list)
    for r in session:
        if r["status"] in ("ok", "task_fail"):
            groups[r["arm"]].append(r)
    for arm in sorted(groups):
        rows = groups[arm]
        w = [r.get("weighted_tokens") or 0 for r in rows]
        sd = statistics.stdev(w) if len(w) > 1 else 0
        cost = statistics.median(r.get("api_cost_usd") or 0 for r in rows)
        lines.append(f"| {arm} | {len(rows)} | {sum(r.get('success', False) for r in rows)} | "
                     f"{statistics.mean(w):,.0f} | {sd:,.0f} | {cost:.2f} |")
    flags = []
    for r in session:
        if r["status"] == "infra":
            flags.append(f"- infra failure {r.get('run_id')}: {r.get('error', '')[:200]} (kept at {r.get('kept_at', '-')})")
        if not str(r.get("arm", "")).startswith("R") and r.get("ponytail_mentions"):
            flags.append(f"- Ponytail text found inside {r['run_id']}: isolation leak, investigate")
        for step in r.get("steps") or []:
            if step.get("permission_denials"):
                flags.append(f"- {r['run_id']}: {step['permission_denials']} permission denial(s); widen config.json permissions"
                             + "".join(f"\n  - `{d}`" for d in step.get("denied", [])))
    a5 = [r for r in session if r.get("arm") == "A5" and r["status"] in ("ok", "task_fail")]
    if a5 and not any(r.get("a5_trim_markers") for r in a5):
        flags.append("- A5 trimming marker never appeared: the hook may not fire on this Claude Code version")
    lines += ["", "## Flags", ""] + (flags or ["- none"])
    (RESULTS / ("NIGHT_REPORT_dry.md" if a.dry_run else "NIGHT_REPORT.md")).write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
