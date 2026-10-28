# Token battery — v8 · claude-opus-5-5

## Does each effect hold across suites?

Ratio vs A0 (95% CI) in each suite. A technique worth recommending should be cheaper in both small edits and full builds, or at least not more expensive in either.

| Arm | small | build | Consistent? |
| --- | --- | --- | --- |
| A0b | 0.89 (0.80–∞) | 1.02 (0.90–1.16) | not established |
| P1 | 1.03 (0.89–∞) | 1.00 (0.88–1.14) | not established |
| A1 | 0.90 (0.79–∞) | n/a | not established |
| A5 | 1.03 (0.89–∞) | n/a | not established |


## Battery report — v8 · claude-opus-5-5 · small suite

240 completed runs across 8 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

### Method checks (read these first)

- **A/A check:** A0b is an exact copy of A0. Ratio 0.89 (0.80–∞). **FAIL: an identical arm looks different. Treat every result below as unreliable until more reps make this interval include 1.0.**
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 1.03 (0.89–∞). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 2 arms tested. At 95% intervals, roughly 0.1 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 48 | 88% (75%–94%) | 1.00 | — | — | — | baseline |
| A0b | 48 | 90% (78%–95%) | 0.89 | 0.80–∞ | 5/8 | 14/23 | inconclusive |
| A1 | 48 | 90% (78%–95%) | 0.90 | 0.79–∞ | 7/8 | 18/23 | inconclusive |
| A5 | 48 | 85% (73%–93%) | 1.03 | 0.89–∞ | 3/8 | 9/23 | inconclusive · lower success |
| P1 | 48 | 85% (73%–93%) | 1.03 | 0.89–∞ | 3/8 | 8/23 | inconclusive · lower success |

### Ratio vs A0 by task (pooled over wordings)

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0b | 0.48 | 1.01 | 0.88 | 1.00 | 0.91 | 0.99 | 1.09 | 0.97 |
| A1 | 0.96 | 0.94 | 0.95 | 1.02 | 0.84 | 0.76 | 0.84 | 0.97 |
| A5 | 0.95 | 1.01 | 1.10 | 0.98 | 0.85 | 1.33 | 1.07 | 1.02 |
| P1 | 0.94 | 1.04 | 0.99 | 1.04 | 0.92 | 1.29 | 1.08 | 1.01 |

### Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.93 | 1.01 | 0.97 |
| A1 | 0.88 | 0.95 | 0.85 |
| A5 | 1.01 | 1.00 | 1.15 |
| P1 | 0.97 | 1.05 | 1.12 |

### Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 16 | 88% | 41,050 | 15,472 | 46,914 |
| v2 | 16 | 88% | 42,668 | 16,670 | 48,763 |
| v3 | 16 | 88% | 52,448 | 21,245 | 59,941 |

### Success rate by task

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 6/6 | 6/6 |
| A0b | 2/6 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 6/6 | 6/6 |
| A1 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| A5 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |
| P1 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |

### Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 12 | 2,597 | 140,166 | 10,327 | 8 | 3 | 5.2 | 40 | 0.00 | 7% |
| A0b | 12 | 2,498 | 138,131 | 10,262 | 8 | 2 | 5.1 | 40 | 0.00 | 7% |
| A1 | 12 | 2,155 | 139,150 | 10,052 | 8 | 3 | 4.8 | 28 | 0.00 | 9% |
| A5 | 12 | 2,462 | 137,539 | 10,266 | 8 | 2 | 5.1 | 37 | 0.00 | 12% |
| P1 | 12 | 2,720 | 139,114 | 10,604 | 8 | 3 | 5.0 | 39 | 0.00 | 7% |

Cells with run-to-run spread above ±30% (worth more reps): A1 T7/v2 (38%), A5 T3/v1 (33%), A5 T7/v1 (31%), A5 T7/v3 (38%), P1 T3/v3 (42%)


### Instruction arms against the placebo

Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?

| Arm | Ratio vs P1 | 95% CI |
| --- | --- | --- |
| A1 | 0.87 | 0.74–∞ |

### Did the technique actually happen?

Runs where the arm's mechanism is visible in the transcript. A cost result for an arm whose mechanism rarely fired says little about the technique itself. Skills can load without an explicit tool call, so a low skill count is a hint, not proof.

| Arm | Evidence | Runs |
| --- | --- | --- |
| A1 | lean-code skill tool calls | 8/48 |
| A5 | trimmed tool output seen | 0/48 |

### Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 10.00 | 5.50 | 0.00 | not installed |
| A0b | 9.00 | 6.50 | 0.00 | not installed |
| A1 | 5.50 | 5.00 | 0.00 | not installed |
| A5 | 10.00 | 6.00 | 0.00 | not installed |
| P1 | 10.00 | 5.00 | 0.00 | not installed |

### What these results do and don't show

- **Measured:** 240 runs of Claude Code 2.1.311 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-27, on one Python repo of 417 lines (8 tasks × 3 wordings), each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** behaviour on larger codebases, other languages, other models or other Claude Code versions. Context-saving techniques (A6a, A6b, A8, A10, A13) are likely understated on a repo this small.
- **Effort arms** are configured via `--effort`, not verified per run.


## Battery report — v8 · claude-opus-5-5 · build suite

18 completed runs across 1 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

### Method checks (read these first)

- **A/A check:** A0b is an exact copy of A0. Ratio 1.02 (0.90–1.16). Pass: the interval includes 1.0, so the method isn't inventing differences.
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 1.00 (0.88–1.14). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 0 arms tested. At 95% intervals, roughly 0.0 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 6 | 100% (61%–100%) | 1.00 | — | — | — | baseline |
| A0b | 6 | 100% (61%–100%) | 1.02 | 0.90–1.16 | 0/1 | 1/3 | inconclusive |
| P1 | 6 | 100% (61%–100%) | 1.00 | 0.88–1.14 | 0/1 | 1/3 | inconclusive |

### Ratio vs A0 by task (pooled over wordings)

| Arm | B1 |
| --- | --- |
| A0b | 1.02 |
| P1 | 1.00 |

### Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.99 | 1.03 | 1.05 |
| P1 | 0.91 | 1.09 | 1.01 |

### Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 2 | 100% | 669,199 | 20,410 | 669,199 |
| v2 | 2 | 100% | 595,448 | 75,546 | 595,448 |
| v3 | 2 | 100% | 728,984 | 122,351 | 728,984 |

### Hidden acceptance tests (build tasks)

Mean share of hidden acceptance tests passed per run, with a bootstrap 95% interval over runs, then the mean per test file (one file per build step). A technique that saves tokens but lowers these is trading quality for cost.

| Arm | Runs | Mean pass rate (95% CI) | test_b1_step1_core | test_b1_step2_storage | test_b1_step3_features | test_b1_step4_cli | Own tests pass | Package lines | Test lines |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 6 | 98% (98%–99%) | 99% | 100% | 96% | 98% | 100% | 1752.50 | 1538.50 |
| A0b | 6 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1731.50 | 1601.50 |
| P1 | 6 | 98% (98%–99%) | 100% | 100% | 96% | 94% | 100% | 1788.50 | 1440.00 |

### Success rate by task

| Arm | B1 |
| --- | --- |
| A0 | 6/6 |
| A0b | 6/6 |
| P1 | 6/6 |

### Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 53 | 77,506 | 1,713,744 | 94,518 | 52 | 0 | 12.9 | 3,238 | 0.02 | 11% |
| A0b | 58 | 76,537 | 2,024,384 | 94,917 | 54 | 0 | 14.4 | 3,304 | 0.02 | 9% |
| P1 | 53 | 76,910 | 1,686,766 | 96,980 | 54 | 1 | 17.3 | 3,251 | 0.03 | 11% |

Cells with run-to-run spread above ±30% (worth more reps): none


### Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 925.00 | 27.00 | 0.00 | not installed |
| A0b | 942.00 | 22.50 | 0.00 | not installed |
| P1 | 938.00 | 23.00 | 0.00 | not installed |

### What these results do and don't show

- **Measured:** 18 runs of Claude Code 2.1.311 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-27, building a project from an empty folder (1 build task(s) × 3 wordings, multi-step sessions), graded by hidden acceptance tests; success means a pass rate of at least 90%, each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** other projects, languages, models or Claude Code versions. Each build follows one fixed interface contract, so this measures building to a spec, not open-ended design.
- **Effort arms** are configured via `--effort`, not verified per run.

