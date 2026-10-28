# Token battery — v8 · claude-opus-5-5


## Battery report — v8 · claude-opus-5-5 · small suite

240 completed runs across 8 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

### Method checks (read these first)

- **A/A check:** not run in this mode (A0b missing).
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 1.03 (0.89–1.21). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 4 arms tested. At 95% intervals, roughly 0.2 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 48 | 83% (70%–91%) | 1.00 | — | — | — | baseline |
| P1 | 48 | 88% (75%–94%) | 1.03 | 0.89–1.21 | 3/8 | 6/21 | inconclusive |
| X1 | 48 | 88% (75%–94%) | 0.77 | 0.66–0.91 | 8/8 | 21/22 | **wins** |
| X2 | 24 | 83% (64%–93%) | 1.00 | 0.85–∞ | 3/7 | 11/20 | inconclusive |
| X3 | 48 | 88% (75%–94%) | 0.92 | 0.79–1.07 | 7/8 | 15/21 | inconclusive |
| X4 | 24 | 83% (64%–93%) | 0.97 | 0.82–∞ | 4/7 | 13/20 | inconclusive |

### Ratio vs A0 by task (pooled over wordings)

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | 0.00 | 1.04 | 0.97 | 1.03 | 1.05 | 0.98 | 1.12 | 1.04 |
| X1 | 0.00 | 0.83 | 0.84 | 0.62 | 0.76 | 0.82 | 0.86 | 0.71 |
| X2 | — | 1.02 | 0.87 | 1.07 | 1.12 | 0.95 | 1.04 | 0.98 |
| X3 | 0.00 | 0.90 | 0.99 | 0.98 | 0.90 | 0.78 | 0.89 | 1.01 |
| X4 | — | 1.08 | 0.81 | 1.01 | 0.99 | 0.93 | 1.06 | 0.92 |

### Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| P1 | 0.93 | 1.03 | 1.01 |
| X1 | 0.75 | 0.78 | 0.73 |
| X2 | 0.97 | 1.08 | 0.92 |
| X3 | 0.78 | 0.90 | 0.90 |
| X4 | 0.91 | 1.04 | 0.97 |

### Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 16 | 88% | 41,780 | 15,838 | 47,749 |
| v2 | 16 | 88% | 43,755 | 19,775 | 50,006 |
| v3 | 16 | 75% | 50,383 | 18,837 | 67,178 |

### Success rate by task

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 0/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |
| P1 | 2/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |
| X1 | 2/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |
| X2 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 |
| X3 | 2/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |
| X4 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 |

### Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 12 | 2,562 | 136,964 | 10,136 | 8 | 3 | 5.1 | 42 | 0.00 | 5% |
| P1 | 12 | 2,670 | 141,754 | 10,714 | 9 | 3 | 5.3 | 40 | 0.00 | 7% |
| X1 | 14 | 2,646 | 89,320 | 7,196 | 8 | 3 | 5.0 | 42 | 0.00 | 9% |
| X2 | 12 | 2,511 | 138,274 | 10,337 | 8 | 3 | 5.0 | 40 | 0.00 | — |
| X3 | 8 | 2,194 | 94,067 | 10,403 | 6 | 3 | 4.0 | 40 | 0.00 | 6% |
| X4 | 12 | 2,604 | 140,564 | 9,762 | 8 | 2 | 5.6 | 40 | 0.01 | — |

Cells with run-to-run spread above ±30% (worth more reps): X1 T3/v1 (35%), X1 T4/v3 (37%), X3 T3/v3 (44%)


### Instruction arms against the placebo

Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?

| Arm | Ratio vs P1 | 95% CI |
| --- | --- | --- |
| X3 | 0.88 | 0.72–∞ |

### Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 10.50 | 7.00 | 0.00 | not installed |
| P1 | 9.50 | 6.00 | 0.00 | not installed |
| X1 | 11.00 | 7.00 | 0.00 | not installed |
| X2 | 10.00 | 6.00 | 0.00 | not installed |
| X3 | 9.50 | 6.50 | 0.00 | not installed |
| X4 | 11.00 | 6.00 | 0.00 | not installed |

### What these results do and don't show

- **Measured:** 240 runs of Claude Code 2.1.311 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-27, on one Python repo of 417 lines (8 tasks × 3 wordings), each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** behaviour on larger codebases, other languages, other models or other Claude Code versions. Context-saving techniques (A6a, A6b, A8, A10, A13) are likely understated on a repo this small.
- **Effort arms** are configured via `--effort`, not verified per run.

