# Battery report — v8-confirm · claude-opus-5-5 · small suite

571 completed runs across 8 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

## Method checks (read these first)

- **A/A check:** A0b is an exact copy of A0. Ratio 0.97 (0.81–1.17). Pass: the interval includes 1.0, so the method isn't inventing differences.
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 0.92 (0.77–1.07). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 3 arms tested. At 95% intervals, roughly 0.2 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 95 | 87% (79%–93%) | 1.00 | — | — | — | baseline |
| A0b | 95 | 88% (80%–93%) | 0.97 | 0.81–1.17 | 4/8 | 8/23 | inconclusive |
| P1 | 95 | 94% (87%–97%) | 0.92 | 0.77–1.07 | 3/8 | 8/23 | inconclusive |
| X1 | 95 | 85% (77%–91%) | 0.93 | 0.74–∞ | 6/8 | 21/23 | inconclusive · lower success |
| X2 | 96 | 85% (77%–91%) | 1.15 | 0.91–∞ | 4/8 | 7/23 | inconclusive · lower success |
| X3 | 95 | 86% (78%–92%) | 0.93 | 0.76–∞ | 6/8 | 16/23 | inconclusive · lower success |

## Ratio vs A0 by task (pooled over wordings)

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0b | 0.60 | 1.00 | 1.01 | 1.05 | 0.99 | 1.16 | 1.07 | 0.99 |
| P1 | 0.51 | 1.06 | 1.17 | 1.06 | 0.98 | 0.74 | 1.04 | 1.03 |
| X1 | 2.18 | 0.85 | 1.07 | 0.66 | 0.77 | 0.86 | 0.87 | 0.74 |
| X2 | 2.83 | 1.03 | 1.01 | 1.09 | 1.00 | 0.99 | 0.99 | 0.98 |
| X3 | 0.89 | 0.91 | 0.96 | 1.02 | 0.89 | 0.93 | 0.82 | 1.00 |

## Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.97 | 1.03 | 1.03 |
| P1 | 0.99 | 1.04 | 0.89 |
| X1 | 0.96 | 0.81 | 0.82 |
| X2 | 1.05 | 1.03 | 1.04 |
| X3 | 0.91 | 0.92 | 0.89 |

## Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 31 | 94% | 41,194 | 14,293 | 44,035 |
| v2 | 32 | 88% | 42,884 | 19,029 | 49,011 |
| v3 | 32 | 81% | 49,515 | 18,813 | 60,941 |

## Success rate by task

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 3/12 | 12/12 | 12/12 | 12/12 | 12/12 | 8/11 | 12/12 | 12/12 |
| A0b | 5/12 | 12/12 | 12/12 | 12/12 | 12/12 | 7/11 | 12/12 | 12/12 |
| P1 | 6/12 | 12/12 | 12/12 | 12/12 | 12/12 | 11/11 | 12/12 | 12/12 |
| X1 | 1/12 | 12/12 | 12/12 | 12/12 | 12/12 | 8/11 | 12/12 | 12/12 |
| X2 | 1/12 | 12/12 | 12/12 | 12/12 | 12/12 | 9/12 | 12/12 | 12/12 |
| X3 | 3/12 | 12/12 | 12/12 | 12/12 | 12/12 | 7/11 | 12/12 | 12/12 |

## Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 12 | 2,474 | 139,001 | 10,278 | 8 | 3 | 5.1 | 39 | 0.00 | 11% |
| A0b | 12 | 2,498 | 139,425 | 10,177 | 8 | 2 | 5.0 | 40 | 0.00 | 10% |
| P1 | 14 | 2,487 | 161,072 | 10,647 | 8 | 3 | 5.2 | 39 | 0.00 | 8% |
| X1 | 14 | 2,719 | 86,545 | 8,007 | 9 | 3 | 5.7 | 40 | 0.00 | 11% |
| X2 | 12 | 2,544 | 139,412 | 10,348 | 8 | 3 | 4.9 | 40 | 0.00 | 8% |
| X3 | 8 | 2,175 | 94,035 | 10,548 | 6 | 3 | 4.0 | 40 | 0.00 | 5% |

Cells with run-to-run spread above ±30% (worth more reps): A0 T5/v3 (31%), A0b T3/v1 (30%), X1 T3/v2 (31%), X1 T3/v3 (30%)


## Instruction arms against the placebo

Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?

| Arm | Ratio vs P1 | 95% CI |
| --- | --- | --- |
| X3 | 1.00 | 0.87–∞ |

## Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 5.00 | 5.00 | 0.00 | not installed |
| A0b | 4.00 | 5.00 | 0.00 | not installed |
| P1 | 5.00 | 5.00 | 0.00 | not installed |
| X1 | 5.00 | 6.00 | 0.00 | not installed |
| X2 | 13.50 | 7.00 | 0.00 | not installed |
| X3 | 4.00 | 5.00 | 0.00 | not installed |

## What these results do and don't show

- **Measured:** 571 runs of Claude Code 2.1.311 (Claude Code), 2.1.312 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-28, on one Python repo of 417 lines (8 tasks × 3 wordings), each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** behaviour on larger codebases, other languages, other models or other Claude Code versions. Context-saving techniques (A6a, A6b, A8, A10, A13) are likely understated on a repo this small.
- **Effort arms** are configured via `--effort`, not verified per run.

