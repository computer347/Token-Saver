# Battery report — v8 · claude-opus-5-5 · small suite

240 completed runs across 8 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

## Method checks (read these first)

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

## Ratio vs A0 by task (pooled over wordings)

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0b | 0.48 | 1.01 | 0.88 | 1.00 | 0.91 | 0.99 | 1.09 | 0.97 |
| A1 | 0.96 | 0.94 | 0.95 | 1.02 | 0.84 | 0.76 | 0.84 | 0.97 |
| A5 | 0.95 | 1.01 | 1.10 | 0.98 | 0.85 | 1.33 | 1.07 | 1.02 |
| P1 | 0.94 | 1.04 | 0.99 | 1.04 | 0.92 | 1.29 | 1.08 | 1.01 |

## Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.93 | 1.01 | 0.97 |
| A1 | 0.88 | 0.95 | 0.85 |
| A5 | 1.01 | 1.00 | 1.15 |
| P1 | 0.97 | 1.05 | 1.12 |

## Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 16 | 88% | 41,050 | 15,472 | 46,914 |
| v2 | 16 | 88% | 42,668 | 16,670 | 48,763 |
| v3 | 16 | 88% | 52,448 | 21,245 | 59,941 |

## Success rate by task

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 6/6 | 6/6 |
| A0b | 2/6 | 6/6 | 6/6 | 6/6 | 6/6 | 5/6 | 6/6 | 6/6 |
| A1 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| A5 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |
| P1 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |

## Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 12 | 2,597 | 140,166 | 10,327 | 8 | 3 | 5.2 | 40 | 0.00 | 7% |
| A0b | 12 | 2,498 | 138,131 | 10,262 | 8 | 2 | 5.1 | 40 | 0.00 | 7% |
| A1 | 12 | 2,155 | 139,150 | 10,052 | 8 | 3 | 4.8 | 28 | 0.00 | 9% |
| A5 | 12 | 2,462 | 137,539 | 10,266 | 8 | 2 | 5.1 | 37 | 0.00 | 12% |
| P1 | 12 | 2,720 | 139,114 | 10,604 | 8 | 3 | 5.0 | 39 | 0.00 | 7% |

Cells with run-to-run spread above ±30% (worth more reps): A1 T7/v2 (38%), A5 T3/v1 (33%), A5 T7/v1 (31%), A5 T7/v3 (38%), P1 T3/v3 (42%)


## Instruction arms against the placebo

Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?

| Arm | Ratio vs P1 | 95% CI |
| --- | --- | --- |
| A1 | 0.87 | 0.74–∞ |

## Did the technique actually happen?

Runs where the arm's mechanism is visible in the transcript. A cost result for an arm whose mechanism rarely fired says little about the technique itself. Skills can load without an explicit tool call, so a low skill count is a hint, not proof.

| Arm | Evidence | Runs |
| --- | --- | --- |
| A1 | lean-code skill tool calls | 8/48 |
| A5 | trimmed tool output seen | 0/48 |

## Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 10.00 | 5.50 | 0.00 | not installed |
| A0b | 9.00 | 6.50 | 0.00 | not installed |
| A1 | 5.50 | 5.00 | 0.00 | not installed |
| A5 | 10.00 | 6.00 | 0.00 | not installed |
| P1 | 10.00 | 5.00 | 0.00 | not installed |

## What these results do and don't show

- **Measured:** 240 runs of Claude Code 2.1.311 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-27, on one Python repo of 417 lines (8 tasks × 3 wordings), each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** behaviour on larger codebases, other languages, other models or other Claude Code versions. Context-saving techniques (A6a, A6b, A8, A10, A13) are likely understated on a repo this small.
- **Effort arms** are configured via `--effort`, not verified per run.

