"""Turn results/runs.jsonl into REPORT.md, summary.csv and a headline chart.

Headline: cost-weighted tokens per successful task, relative to A0. Per task, runs are pooled across
wordings (the design is balanced, so every arm sees the same mix); tasks are combined by geometric
mean. Confidence intervals come from a bootstrap that resamples runs within each arm × task × wording.

Usage: python3 harness/report.py [--dry-run] [--runs-file PATH] [--out-dir DIR]
"""
import argparse
import csv
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ARMS, RESULTS, RUNS_FILE, load_config, read_jsonl, suite_spec, target_dir

BOOT = 2000


def cps(rows):
    """Cost-weighted tokens per success."""
    wins = sum(1 for r in rows if r.get("success"))
    total = sum(r.get("weighted_tokens") or 0 for r in rows)
    return total / wins if wins else math.inf


def wilson(k, n, z=1.96):
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def geo_mean(values):
    if any(math.isinf(v) for v in values):
        return math.inf
    values = [v for v in values if v > 0 and math.isfinite(v)]
    return math.exp(sum(map(math.log, values)) / len(values)) if values else math.nan


def ratio_by(strata, arm, groups, rng=None, base="A0"):
    """Ratio arm/base of cost per success for each group of stratum keys.

    With rng, runs are resampled within each group (pooled across the group's wordings), so every
    resample carries real run-to-run variation even when a single task × wording cell has one run.
    """
    out = {}
    for name, keys in groups.items():
        a = [r for k in keys for r in strata.get((arm,) + k, [])]
        b = [r for k in keys for r in strata.get((base,) + k, [])]
        if not a or not b:
            continue
        if rng is not None:
            a = [rng.choice(a) for _ in a]
            b = [rng.choice(b) for _ in b]
        ca, cb = cps(a), cps(b)
        if math.isinf(ca) and math.isinf(cb):
            continue
        out[name] = math.inf if math.isinf(ca) else (0.0 if math.isinf(cb) else ca / cb)
    return out


MIN_RUNS_PER_TASK = 3


def enough_data(strata, arm, groups, base="A0"):
    for keys in groups.values():
        na = sum(len(strata.get((arm,) + k, [])) for k in keys)
        nb = sum(len(strata.get((base,) + k, [])) for k in keys)
        if (na or nb) and min(na, nb) < MIN_RUNS_PER_TASK:
            return False
    return True


def boot_ci(strata, arm, groups, seed=11, base="A0"):
    if not enough_data(strata, arm, groups, base):
        return (math.nan, math.nan)
    rng = random.Random(seed)
    vals = []
    for _ in range(BOOT):
        r = ratio_by(strata, arm, groups, rng, base)
        if r:
            vals.append(geo_mean(list(r.values())))
    vals = sorted(v for v in vals if not math.isnan(v))
    if not vals:
        return (math.nan, math.nan)
    return (vals[int(0.025 * len(vals))], vals[min(len(vals) - 1, int(0.975 * len(vals)))])


def fmt(v, pct=False):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    if isinstance(v, float) and math.isinf(v):
        return "∞"
    return f"{v:.0%}" if pct else f"{v:.2f}"


def ci_str(lo, hi):
    return "—" if (isinstance(lo, float) and math.isnan(lo)) else f"{fmt(lo)}–{fmt(hi)}"


def med(rows, *path):
    vals = []
    for r in rows:
        v = r
        for p in path:
            v = v.get(p) if isinstance(v, dict) else None
        if isinstance(v, (int, float)):
            vals.append(v)
    return statistics.median(vals) if vals else None


def svg_chart(items, path):
    items = [(arm, r, lo, hi) for arm, r, lo, hi in items if math.isfinite(r)]
    if not items:
        return
    top = max([1.2] + [hi for *_, hi in items if math.isfinite(hi)] + [r for _, r, *_ in items])
    w, row_h, left = 680, 32, 90
    h = 64 + row_h * len(items)
    x = lambda v: left + (w - left - 50) * min(v, top) / top
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="sans-serif" font-size="13">',
           '<rect width="100%" height="100%" fill="white"/>',
           '<text x="20" y="24" font-size="15" font-weight="600">Cost per successful task vs baseline (A0 = 1.0), 95% CI</text>',
           f'<line x1="{x(1):.1f}" y1="38" x2="{x(1):.1f}" y2="{h - 10}" stroke="#888" stroke-dasharray="4 3"/>']
    for i, (arm, r, lo, hi) in enumerate(items):
        y = 50 + i * row_h
        color = "#2a7f62" if math.isfinite(hi) and hi < 1 else ("#c0392b" if math.isfinite(lo) and lo > 1 else "#5d6d7e")
        out += [f'<text x="20" y="{y + 15}">{arm}</text>',
                f'<rect x="{left}" y="{y + 4}" width="{max(1, x(r) - left):.1f}" height="16" fill="{color}" opacity="0.8"/>']
        if math.isfinite(lo) and math.isfinite(hi):
            out.append(f'<line x1="{x(lo):.1f}" y1="{y + 12}" x2="{x(hi):.1f}" y2="{y + 12}" stroke="#222" stroke-width="1.5"/>')
        out.append(f'<text x="{min(x(r), w - 60) + 6:.1f}" y="{y + 16}" font-size="11">{r:.2f}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out))


def suite_report(rows, cfg, dry, suite):
    for r in rows:
        r.setdefault("variant", "v1")
    strata = defaultdict(list)
    for r in rows:
        strata[(r["arm"], r["task"], r["variant"])].append(r)
    arms = sorted({r["arm"] for r in rows}, key=lambda s: (s != "A0", s))
    tasks = sorted({r["task"] for r in rows})
    variants = sorted({r["variant"] for r in rows})
    by_task = {t: [(t, v) for v in variants] for t in tasks}
    by_variant = {v: [(t, v) for t in tasks] for v in variants}
    by_stratum = {f"{t}/{v}": [(t, v)] for t in tasks for v in variants}
    base_rows = [r for r in rows if r["arm"] == "A0"]
    base_success = sum(r.get("success", False) for r in base_rows) / len(base_rows) if base_rows else math.nan

    md = [f"# Battery report — {cfg['battery_version']} · {cfg['model']}{' (dry run)' if dry else ''} · {suite} suite", "",
          f"{len(rows)} completed runs across {len(tasks)} tasks × {len(variants)} wordings. "
          "**Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and "
          "combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% "
          "interval is below 1.0 and its success rate is at least the baseline's.", "",
          "| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |",
          "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    chart, per_task, per_variant, csv_rows, headline_map = [], {}, {}, [], {}
    for arm in arms:
        ar = [r for r in rows if r["arm"] == arm]
        k = sum(r.get("success", False) for r in ar)
        lo_s, hi_s = wilson(k, len(ar))
        succ = f"{k / len(ar):.0%} ({lo_s:.0%}–{hi_s:.0%})"
        if arm == "A0":
            md.append(f"| A0 | {len(ar)} | {succ} | 1.00 | — | — | — | baseline |")
            continue
        task_ratios = ratio_by(strata, arm, by_task)
        per_task[arm] = task_ratios
        per_variant[arm] = ratio_by(strata, arm, by_variant)
        cells = ratio_by(strata, arm, by_stratum)
        ratio = geo_mean(list(task_ratios.values())) if task_ratios else math.nan
        lo, hi = boot_ci(strata, arm, by_task)
        rate = k / len(ar)
        if math.isnan(lo):
            verdict = f"insufficient reps (need ≥{MIN_RUNS_PER_TASK} runs per task)"
        elif math.isfinite(hi) and hi < 1 and rate >= base_success:
            verdict = "**wins**"
        elif math.isfinite(lo) and lo > 1:
            verdict = "costs more"
        else:
            verdict = "inconclusive"
        if rate < base_success:
            verdict += " · lower success"
        cheaper_t = sum(v < 1 for v in task_ratios.values())
        cheaper_c = sum(v < 1 for v in cells.values())
        md.append(f"| {arm} | {len(ar)} | {succ} | {fmt(ratio)} | {ci_str(lo, hi)} | {cheaper_t}/{len(task_ratios)} | "
                  f"{cheaper_c}/{len(cells)} | {verdict} |")
        chart.append((arm, ratio, lo, hi))
        headline_map[arm] = (ratio, lo, hi, verdict)

    md += ["", "## Ratio vs A0 by task (pooled over wordings)", "",
           "| Arm | " + " | ".join(tasks) + " |", "| --- | " + " | ".join("---" for _ in tasks) + " |"]
    for arm in arms[1:]:
        md.append(f"| {arm} | " + " | ".join(fmt(per_task.get(arm, {}).get(t)) for t in tasks) + " |")

    md += ["", "## Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)", "",
           "v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.", "",
           "| Arm | " + " | ".join(variants) + " |", "| --- | " + " | ".join("---" for _ in variants) + " |"]
    for arm in arms[1:]:
        md.append(f"| {arm} | " + " | ".join(fmt(per_variant.get(arm, {}).get(v)) for v in variants) + " |")

    md += ["", "## Baseline cost by wording (does phrasing alone change cost?)", "",
           "| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |", "| --- | --- | --- | --- | --- | --- |"]
    for v in variants:
        vr = [r for r in base_rows if r["variant"] == v]
        if vr:
            w = [r.get("weighted_tokens") or 0 for r in vr]
            md.append(f"| {v} | {len(vr)} | {sum(r.get('success', False) for r in vr) / len(vr):.0%} | {statistics.mean(w):,.0f} | "
                      f"{statistics.stdev(w) if len(w) > 1 else 0:,.0f} | {cps(vr):,.0f} |")


    # ---------- build tasks: acceptance pass rates ----------
    if any("pass_rate" in r for r in rows):
        steps = sorted({k for r in rows for k in (r.get("step_pass_rates") or {})})
        md += ["", "## Hidden acceptance tests (build tasks)", "",
               "Mean share of hidden acceptance tests passed per run, with a bootstrap 95% interval over runs, "
               "then the mean per test file (one file per build step). A technique that saves tokens but lowers these "
               "is trading quality for cost.", "",
               "| Arm | Runs | Mean pass rate (95% CI) | " + " | ".join(steps) + " | Own tests pass | Package lines | Test lines |",
               "| --- | --- | --- | " + " | ".join("---" for _ in steps) + " | --- | --- | --- |"]
        rng_pr = random.Random(5)
        for arm in arms:
            ar = [r for r in rows if r["arm"] == arm and "pass_rate" in r]
            if not ar:
                continue
            rates = [r["pass_rate"] for r in ar]
            boots = sorted(statistics.mean(rng_pr.choice(rates) for _ in rates) for _ in range(BOOT))
            lo_p, hi_p = boots[int(0.025 * BOOT)], boots[int(0.975 * BOOT) - 1]
            per_step = [statistics.mean((r.get("step_pass_rates") or {}).get(st, 0.0) for r in ar) for st in steps]
            own = sum(1 for r in ar if r.get("own_tests_pass")) / len(ar)
            md.append(f"| {arm} | {len(ar)} | {statistics.mean(rates):.0%} ({lo_p:.0%}–{hi_p:.0%}) | "
                      + " | ".join(f"{v:.0%}" for v in per_step)
                      + f" | {own:.0%} | {fmt(med(ar, 'package_lines'))} | {fmt(med(ar, 'test_lines'))} |")

    md += ["", "## Success rate by task", "", "| Arm | " + " | ".join(tasks) + " |",
           "| --- | " + " | ".join("---" for _ in tasks) + " |"]
    for arm in arms:
        cells = []
        for t in tasks:
            tr = [r for v in variants for r in strata.get((arm, t, v), [])]
            cells.append(f"{sum(r.get('success', False) for r in tr)}/{len(tr)}" if tr else "—")
        md.append(f"| {arm} | " + " | ".join(cells) + " |")

    md += ["", "## Where the tokens go (medians per run)", "",
           "| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |",
           "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    noisy = []
    for arm in arms:
        ar = [r for r in rows if r["arm"] == arm]
        cvs = []
        for t in tasks:
            for v in variants:
                w = [r.get("weighted_tokens") or 0 for r in strata.get((arm, t, v), [])]
                if len(w) > 1 and statistics.mean(w):
                    cv = statistics.stdev(w) / statistics.mean(w)
                    cvs.append(cv)
                    if cv > 0.3:
                        noisy.append(f"{arm} {t}/{v} ({cv:.0%})")
        line = {"arm": arm, "runs": len(ar), "success_rate": sum(r.get("success", False) for r in ar) / len(ar),
                "input": med(ar, "tokens", "input"), "output": med(ar, "tokens", "output"),
                "cache_read": med(ar, "tokens", "cache_read"), "cache_write": med(ar, "tokens", "cache_write"),
                "tool_calls": med(ar, "tool_calls_total"), "files_read": med(ar, "files_read"),
                "tool_result_kb": (med(ar, "tool_result_bytes") or 0) / 1024, "lines_added": med(ar, "lines_added"),
                "comment_share": med(ar, "comment_char_share"), "mean_cv": statistics.mean(cvs) if cvs else None,
                "ratio_vs_a0": next((c[1] for c in chart if c[0] == arm), 1.0 if arm == "A0" else None)}
        csv_rows.append(line)
        cell = lambda v, d=0: "—" if v is None else (f"{v:,.{d}f}")
        md.append(f"| {arm} | {cell(line['input'])} | {cell(line['output'])} | {cell(line['cache_read'])} | "
                  f"{cell(line['cache_write'])} | {cell(line['tool_calls'])} | {cell(line['files_read'])} | "
                  f"{cell(line['tool_result_kb'], 1)} | {cell(line['lines_added'])} | {cell(line['comment_share'], 2)} | "
                  f"{fmt(line['mean_cv'], pct=True)} |")
    md += ["", "Cells with run-to-run spread above ±30% (worth more reps): " + (", ".join(noisy[:20]) or "none") +
           (" …" if len(noisy) > 20 else ""), ""]

    # ---------- method checks ----------
    checks_md = ["## Method checks (read these first)", ""]
    if "A0b" in arms:
        r = geo_mean(list(ratio_by(strata, "A0b", by_task).values()))
        lo, hi = boot_ci(strata, "A0b", by_task)
        ok = math.isfinite(lo) and math.isfinite(hi) and lo <= 1 <= hi
        checks_md.append(f"- **A/A check:** A0b is an exact copy of A0. Ratio {fmt(r)} ({ci_str(lo, hi)}). "
                         + (f"Not enough runs to check yet (need ≥{MIN_RUNS_PER_TASK} per task)." if math.isnan(lo) else
                            "Pass: the interval includes 1.0, so the method isn't inventing differences."
                            if ok else "**FAIL: an identical arm looks different. Treat every result below as unreliable "
                                       "until more reps make this interval include 1.0.**"))
    else:
        checks_md.append("- **A/A check:** not run in this mode (A0b missing).")
    if "P1" in arms:
        r = geo_mean(list(ratio_by(strata, "P1", by_task).values()))
        lo, hi = boot_ci(strata, "P1", by_task)
        checks_md.append(f"- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 {fmt(r)} ({ci_str(lo, hi)}). "
                         "Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.")
    tested = [x for x in arms if x not in ("A0", "A0b", "P1")]
    checks_md.append(f"- **Multiple comparisons:** {len(tested)} arms tested. At 95% intervals, roughly "
                     f"{len(tested) * 0.05:.1f} could exclude 1.0 by chance alone. Treat a win as established only after "
                     "it repeats in the independent `confirm` mode.")
    md[md.index("| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |") - 1:
       md.index("| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |") - 1] = [""] + checks_md + [""]

    # ---------- against the placebo ----------
    def has_instructions(arm):
        overlay = ARMS / arm / "overlay"
        return (overlay / "CLAUDE.md").exists() or (overlay / ".claude" / "skills").exists()
    instr = [x for x in tested if has_instructions(x)]
    if "P1" in arms and instr:
        md += ["", "## Instruction arms against the placebo", "",
               "Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?", "",
               "| Arm | Ratio vs P1 | 95% CI |", "| --- | --- | --- |"]
        for x in instr:
            r = geo_mean(list(ratio_by(strata, x, by_task, base="P1").values()))
            lo, hi = boot_ci(strata, x, by_task, base="P1")
            md.append(f"| {x} | {fmt(r)} | {ci_str(lo, hi)} |")

    # ---------- did the mechanism actually fire? ----------
    def share(rs, pred):
        return f"{sum(1 for r in rs if pred(r))}/{len(rs)}"
    mech = {
        "A1": ("lean-code skill tool calls", lambda r: r.get("skill_calls", 0) > 0),
        "A11": ("repo-recipes skill tool calls", lambda r: r.get("skill_calls", 0) > 0),
        "A5": ("trimmed tool output seen", lambda r: r.get("a5_trim_markers", 0) > 0),
        "A6b": ("subagent used", lambda r: r.get("subagent_calls", 0) > 0 or r.get("models_subagents")),
        "A8": ("BRIEF.md opened", lambda r: r.get("brief_reads", 0) > 0),
        "A10": ("LSP tool called", lambda r: r.get("lsp_calls", 0) > 0),
        "A12": ("scaffold.py run", lambda r: r.get("scaffold_calls", 0) > 0),
        "A13": ("Haiku model in subagent transcripts", lambda r: any("haiku" in m for m in r.get("models_subagents", []))),
    }
    rows_m = []
    for x in arms:
        if x in mech:
            label, pred = mech[x]
            ar = [r for r in rows if r["arm"] == x]
            rows_m.append(f"| {x} | {label} | {share(ar, pred)} |")
        elif x in ("A9", "A9m"):
            rows_m.append(f"| {x} | effort flag passed on the command line | configured only; Claude Code doesn't report effort per run |")
    if rows_m:
        md += ["", "## Did the technique actually happen?", "",
               "Runs where the arm's mechanism is visible in the transcript. A cost result for an arm whose mechanism "
               "rarely fired says little about the technique itself. Skills can load without an explicit tool call, "
               "so a low skill count is a hint, not proof.", "",
               "| Arm | Evidence | Runs |", "| --- | --- | --- |"] + rows_m

    # ---------- code quality ----------
    md += ["", "## Code quality of what was changed (medians per run)", "",
           "Complexity is summed cyclomatic complexity of changed Python files (after minus before). "
           "Cheaper is only better if these don't get worse.", "",
           "| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |", "| --- | --- | --- | --- | --- |"]
    for x in arms:
        ar = [r for r in rows if r["arm"] == x]
        ruff = med(ar, "ruff_issues")
        md.append(f"| {x} | {fmt(med(ar, 'complexity_delta') if med(ar, 'complexity_delta') is not None else None)} | "
                  f"{fmt(med(ar, 'max_function_complexity'))} | {fmt(med(ar, 'unused_imports'))} | "
                  f"{'not installed' if ruff is None else fmt(ruff)} |")

    # ---------- scope of the claims ----------
    versions = sorted({r.get("claude_version", "?") for r in rows})
    dates = sorted(r.get("started", "")[:10] for r in rows if r.get("started"))
    py_lines = sum(len(f.read_text().splitlines()) for f in target_dir(suite).rglob("*.py") if "__pycache__" not in f.parts)
    is_build = suite_spec(suite).get("kind") == "build"
    md += ["", "## What these results do and don't show", "",
           f"- **Measured:** {len(rows)} runs of Claude Code {', '.join(versions)} with {cfg['model']}, "
           f"{dates[0] if dates else '?'} to {dates[-1] if dates else '?'}, "
           + (f"building a project from an empty folder ({len(tasks)} build task(s) × {len(variants)} wordings, multi-step "
              f"sessions), graded by hidden acceptance tests; success means a pass rate of at least "
              f"{suite_spec(suite).get('success_threshold', 1.0):.0%}"
              if is_build else
              f"on one Python repo of {py_lines} lines ({len(tasks)} tasks × {len(variants)} wordings)")
           + ", each run in a fresh, isolated configuration.",
           "- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each "
           "token type is not published, so plan-percentage savings may differ.",
           ("- **Not shown:** other projects, languages, models or Claude Code versions. Each build follows one fixed "
            "interface contract, so this measures building to a spec, not open-ended design."
            if is_build else
            "- **Not shown:** behaviour on larger codebases, other languages, other models or other Claude Code versions. "
            "Context-saving techniques (A6a, A6b, A8, A10, A13) are likely understated on a repo this small."),
           "- **Effort arms** are configured via `--effort`, not verified per run.",
           ""]

    return md, csv_rows, chart, headline_map


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--runs-file", default=str(RUNS_FILE))
    ap.add_argument("--out-dir", default=str(RESULTS))
    ap.add_argument("--confirm", action="store_true", help="report the independent confirm battery")
    a = ap.parse_args()
    cfg = load_config()
    if a.confirm:
        cfg = {**cfg, "battery_version": cfg["battery_version"] + "-confirm"}
    out = Path(a.out_dir)
    rows = [r for r in read_jsonl(Path(a.runs_file))
            if r.get("status") in ("ok", "task_fail") and bool(r.get("dry_run")) == a.dry_run
            and r.get("battery_version") == cfg["battery_version"] and r.get("model") == cfg["model"]]
    if not rows:
        print("No completed runs yet.")
        return
    for r in rows:
        r.setdefault("suite", "small")
    suites = sorted({r["suite"] for r in rows}, key=lambda x: (x != "small", x))
    suffix = "_dry" if a.dry_run else ""
    out.mkdir(parents=True, exist_ok=True)
    combined = [f"# Token battery — {cfg['battery_version']} · {cfg['model']}{' (dry run)' if a.dry_run else ''}", ""]
    sections, headlines = [], {}
    for suite in suites:
        md, csv_rows, chart, headline_map = suite_report([r for r in rows if r["suite"] == suite], cfg, a.dry_run, suite)
        headlines[suite] = headline_map
        (out / f"REPORT_{suite}{suffix}.md").write_text("\n".join(md) + "\n")
        with (out / f"summary_{suite}{suffix}.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)
        svg_chart(chart, out / f"headline_chart_{suite}{suffix}.svg")
        sections += [""] + ["#" + line if line.startswith("#") else line for line in md]
    if len(suites) > 1:
        shared = sorted({x for h in headlines.values() for x in h}, key=lambda s: (s not in ("A0b", "P1"), s))
        combined += ["## Does each effect hold across suites?", "",
                     "Ratio vs A0 (95% CI) in each suite. A technique worth recommending should be cheaper in both "
                     "small edits and full builds, or at least not more expensive in either.", "",
                     "| Arm | " + " | ".join(suites) + " | Consistent? |", "| --- | " + " | ".join("---" for _ in suites) + " | --- |"]
        for arm in shared:
            cells, wins, losses, present = [], 0, 0, 0
            for suite in suites:
                h = headlines[suite].get(arm)
                if not h:
                    cells.append("n/a")
                    continue
                present += 1
                r, lo, hi, _ = h
                cells.append(f"{fmt(r)} ({ci_str(lo, hi)})")
                wins += math.isfinite(hi) and hi < 1
                losses += math.isfinite(lo) and lo > 1
            verdict = ("cheaper in every suite" if present > 1 and wins == present else
                       "costs more somewhere" if losses else "not established")
            combined.append(f"| {arm} | " + " | ".join(cells) + f" | {verdict} |")
        combined.append("")
    combined += sections
    (out / f"REPORT{suffix}.md").write_text("\n".join(combined) + "\n")
    print(f"Wrote {out / f'REPORT{suffix}.md'} and one report per suite")


if __name__ == "__main__":
    main()
