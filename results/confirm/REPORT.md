# Token battery — v8-confirm · claude-opus-5-5

## Does each effect hold across suites?

Ratio vs A0 (95% CI) in each suite. A technique worth recommending should be cheaper in both small edits and full builds, or at least not more expensive in either.

| Arm | small | build | Consistent? |
| --- | --- | --- | --- |
| A0b | 0.97 (0.81–1.17) | 0.98 (0.92–1.04) | not established |
| P1 | 0.92 (0.77–1.07) | 1.00 (0.91–1.09) | not established |
| X1 | 0.93 (0.74–∞) | 0.99 (0.91–1.06) | not established |
| X2 | 1.15 (0.91–∞) | 0.97 (0.90–1.02) | not established |
| X3 | 0.93 (0.76–∞) | n/a | not established |


## Battery report — v8-confirm · claude-opus-5-5 · small suite

571 completed runs across 8 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

### Method checks (read these first)

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

### Ratio vs A0 by task (pooled over wordings)

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0b | 0.60 | 1.00 | 1.01 | 1.05 | 0.99 | 1.16 | 1.07 | 0.99 |
| P1 | 0.51 | 1.06 | 1.17 | 1.06 | 0.98 | 0.74 | 1.04 | 1.03 |
| X1 | 2.18 | 0.85 | 1.07 | 0.66 | 0.77 | 0.86 | 0.87 | 0.74 |
| X2 | 2.83 | 1.03 | 1.01 | 1.09 | 1.00 | 0.99 | 0.99 | 0.98 |
| X3 | 0.89 | 0.91 | 0.96 | 1.02 | 0.89 | 0.93 | 0.82 | 1.00 |

### Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.97 | 1.03 | 1.03 |
| P1 | 0.99 | 1.04 | 0.89 |
| X1 | 0.96 | 0.81 | 0.82 |
| X2 | 1.05 | 1.03 | 1.04 |
| X3 | 0.91 | 0.92 | 0.89 |

### Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 31 | 94% | 41,194 | 14,293 | 44,035 |
| v2 | 32 | 88% | 42,884 | 19,029 | 49,011 |
| v3 | 32 | 81% | 49,515 | 18,813 | 60,941 |

### Success rate by task

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 3/12 | 12/12 | 12/12 | 12/12 | 12/12 | 8/11 | 12/12 | 12/12 |
| A0b | 5/12 | 12/12 | 12/12 | 12/12 | 12/12 | 7/11 | 12/12 | 12/12 |
| P1 | 6/12 | 12/12 | 12/12 | 12/12 | 12/12 | 11/11 | 12/12 | 12/12 |
| X1 | 1/12 | 12/12 | 12/12 | 12/12 | 12/12 | 8/11 | 12/12 | 12/12 |
| X2 | 1/12 | 12/12 | 12/12 | 12/12 | 12/12 | 9/12 | 12/12 | 12/12 |
| X3 | 3/12 | 12/12 | 12/12 | 12/12 | 12/12 | 7/11 | 12/12 | 12/12 |

### Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 12 | 2,474 | 139,001 | 10,278 | 8 | 3 | 5.1 | 39 | 0.00 | 11% |
| A0b | 12 | 2,498 | 139,425 | 10,177 | 8 | 2 | 5.0 | 40 | 0.00 | 10% |
| P1 | 14 | 2,487 | 161,072 | 10,647 | 8 | 3 | 5.2 | 39 | 0.00 | 8% |
| X1 | 14 | 2,719 | 86,545 | 8,007 | 9 | 3 | 5.7 | 40 | 0.00 | 11% |
| X2 | 12 | 2,544 | 139,412 | 10,348 | 8 | 3 | 4.9 | 40 | 0.00 | 8% |
| X3 | 8 | 2,175 | 94,035 | 10,548 | 6 | 3 | 4.0 | 40 | 0.00 | 5% |

Cells with run-to-run spread above ±30% (worth more reps): A0 T5/v3 (31%), A0b T3/v1 (30%), X1 T3/v2 (31%), X1 T3/v3 (30%)


### Instruction arms against the placebo

Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?

| Arm | Ratio vs P1 | 95% CI |
| --- | --- | --- |
| X3 | 1.00 | 0.87–∞ |

### Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 5.00 | 5.00 | 0.00 | not installed |
| A0b | 4.00 | 5.00 | 0.00 | not installed |
| P1 | 5.00 | 5.00 | 0.00 | not installed |
| X1 | 5.00 | 6.00 | 0.00 | not installed |
| X2 | 13.50 | 7.00 | 0.00 | not installed |
| X3 | 4.00 | 5.00 | 0.00 | not installed |

### What these results do and don't show

- **Measured:** 571 runs of Claude Code 2.1.311 (Claude Code), 2.1.312 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-28, on one Python repo of 417 lines (8 tasks × 3 wordings), each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** behaviour on larger codebases, other languages, other models or other Claude Code versions. Context-saving techniques (A6a, A6b, A8, A10, A13) are likely understated on a repo this small.
- **Effort arms** are configured via `--effort`, not verified per run.


## Battery report — v8-confirm · claude-opus-5-5 · build suite

50 completed runs across 1 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

### Method checks (read these first)

- **A/A check:** A0b is an exact copy of A0. Ratio 0.98 (0.92–1.04). Pass: the interval includes 1.0, so the method isn't inventing differences.
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 1.00 (0.91–1.09). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 2 arms tested. At 95% intervals, roughly 0.1 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 10 | 100% (72%–100%) | 1.00 | — | — | — | baseline |
| A0b | 10 | 100% (72%–100%) | 0.98 | 0.92–1.04 | 1/1 | 2/3 | inconclusive |
| P1 | 10 | 100% (72%–100%) | 1.00 | 0.91–1.09 | 1/1 | 2/3 | inconclusive |
| X1 | 10 | 100% (72%–100%) | 0.99 | 0.91–1.06 | 1/1 | 2/3 | inconclusive |
| X2 | 10 | 100% (72%–100%) | 0.97 | 0.90–1.02 | 1/1 | 3/3 | inconclusive |

### Ratio vs A0 by task (pooled over wordings)

| Arm | B1 |
| --- | --- |
| A0b | 0.98 |
| P1 | 1.00 |
| X1 | 0.99 |
| X2 | 0.97 |

### Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.98 | 0.96 | 1.01 |
| P1 | 1.00 | 0.97 | 1.05 |
| X1 | 1.00 | 0.94 | 1.04 |
| X2 | 0.98 | 0.95 | 0.97 |

### Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 4 | 100% | 671,655 | 33,530 | 671,655 |
| v2 | 4 | 100% | 664,382 | 80,832 | 664,382 |
| v3 | 2 | 100% | 719,843 | 43,154 | 719,843 |

### Hidden acceptance tests (build tasks)

Mean share of hidden acceptance tests passed per run, with a bootstrap 95% interval over runs, then the mean per test file (one file per build step). A technique that saves tokens but lowers these is trading quality for cost.

| Arm | Runs | Mean pass rate (95% CI) | test_b1_step1_core | test_b1_step2_storage | test_b1_step3_features | test_b1_step4_cli | Own tests pass | Package lines | Test lines |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 10 | 99% (98%–99%) | 100% | 100% | 96% | 99% | 100% | 1821.50 | 1540.00 |
| A0b | 10 | 98% (98%–99%) | 100% | 100% | 97% | 98% | 100% | 1830.00 | 1525.00 |
| P1 | 10 | 98% (98%–99%) | 99% | 100% | 97% | 96% | 100% | 1801.00 | 1660.00 |
| X1 | 10 | 99% (98%–99%) | 100% | 100% | 97% | 99% | 100% | 1829.50 | 1615.00 |
| X2 | 10 | 99% (98%–99%) | 100% | 100% | 97% | 99% | 100% | 1711.50 | 1422.00 |

### Success rate by task

| Arm | B1 |
| --- | --- |
| A0 | 10/10 |
| A0b | 10/10 |
| P1 | 10/10 |
| X1 | 10/10 |
| X2 | 10/10 |

### Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 58 | 77,075 | 1,935,508 | 94,904 | 54 | 0 | 13.8 | 3,352 | 0.02 | 8% |
| A0b | 55 | 73,858 | 1,855,518 | 91,939 | 52 | 1 | 13.3 | 3,410 | 0.03 | 5% |
| P1 | 54 | 79,328 | 1,662,592 | 95,502 | 52 | 0 | 13.9 | 3,483 | 0.03 | 10% |
| X1 | 54 | 79,624 | 1,508,648 | 92,750 | 53 | 1 | 13.7 | 3,472 | 0.03 | 8% |
| X2 | 56 | 73,232 | 1,809,759 | 91,392 | 56 | 1 | 12.7 | 3,130 | 0.02 | 4% |

Cells with run-to-run spread above ±30% (worth more reps): none


### Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 951.00 | 23.00 | 0.00 | not installed |
| A0b | 938.00 | 23.50 | 0.00 | not installed |
| P1 | 936.50 | 24.00 | 0.00 | not installed |
| X1 | 986.50 | 22.50 | 0.00 | not installed |
| X2 | 884.00 | 22.00 | 0.00 | not installed |

### What these results do and don't show

- **Measured:** 50 runs of Claude Code 2.1.311 (Claude Code), 2.1.312 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-28, building a project from an empty folder (1 build task(s) × 3 wordings, multi-step sessions), graded by hidden acceptance tests; success means a pass rate of at least 90%, each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** other projects, languages, models or Claude Code versions. Each build follows one fixed interface contract, so this measures building to a spec, not open-ended design.
- **Effort arms** are configured via `--effort`, not verified per run.

