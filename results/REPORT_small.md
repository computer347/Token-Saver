# Battery report — v8 · claude-opus-5-5 · small suite

739 completed runs across 8 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

## Method checks (read these first)

- **A/A check:** A0b is an exact copy of A0. Ratio 0.89 (0.80–∞). **FAIL: an identical arm looks different. Treat every result below as unreliable until more reps make this interval include 1.0.**
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 1.03 (0.89–∞). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 16 arms tested. At 95% intervals, roughly 0.8 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 48 | 88% (75%–94%) | 1.00 | — | — | — | baseline |
| A0b | 48 | 90% (78%–95%) | 0.89 | 0.80–∞ | 5/8 | 14/23 | inconclusive |
| A1 | 48 | 90% (78%–95%) | 0.90 | 0.79–∞ | 7/8 | 18/23 | inconclusive |
| A10 | 36 | 92% (78%–97%) | 0.96 | 0.83–∞ | 3/8 | 8/22 | inconclusive |
| A11 | 35 | 94% (81%–98%) | 0.89 | 0.77–∞ | 6/8 | 12/23 | inconclusive |
| A12 | 36 | 89% (75%–96%) | ∞ | 0.95–∞ | 3/8 | 7/22 | inconclusive |
| A13 | 36 | 89% (75%–96%) | ∞ | 1.38–∞ | 1/8 | 3/22 | costs more |
| A2 | 35 | 94% (81%–98%) | 0.81 | 0.71–∞ | 8/8 | 18/23 | inconclusive |
| A3 | 36 | 94% (82%–98%) | 0.86 | 0.75–∞ | 6/8 | 13/23 | inconclusive |
| A4 | 36 | 89% (75%–96%) | ∞ | 0.88–∞ | 4/8 | 9/22 | inconclusive |
| A5 | 48 | 85% (73%–93%) | 1.03 | 0.89–∞ | 3/8 | 9/23 | inconclusive · lower success |
| A6a | 35 | 91% (78%–97%) | 0.90 | 0.78–∞ | 5/8 | 11/22 | inconclusive |
| A6b | 36 | 94% (82%–98%) | 1.22 | 1.08–∞ | 1/8 | 2/23 | costs more |
| A8 | 35 | 100% (90%–100%) | 0.76 | 0.71–1.03 | 5/8 | 12/24 | inconclusive |
| A9 | 36 | 94% (82%–98%) | 0.65 | 0.59–∞ | 8/8 | 22/23 | inconclusive |
| A9m | 35 | 89% (74%–95%) | ∞ | 0.92–∞ | 3/8 | 12/22 | inconclusive |
| P1 | 48 | 85% (73%–93%) | 1.03 | 0.89–∞ | 3/8 | 8/23 | inconclusive · lower success |
| X1 | 36 | 92% (78%–97%) | 0.73 | 0.63–∞ | 7/8 | 19/23 | inconclusive |
| X3 | 36 | 89% (75%–96%) | 0.87 | 0.77–∞ | 5/8 | 14/23 | inconclusive |

## Ratio vs A0 by task (pooled over wordings)

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0b | 0.48 | 1.01 | 0.88 | 1.00 | 0.91 | 0.99 | 1.09 | 0.97 |
| A1 | 0.96 | 0.94 | 0.95 | 1.02 | 0.84 | 0.76 | 0.84 | 0.97 |
| A10 | 0.45 | 1.18 | 0.99 | 1.04 | 0.93 | 1.17 | 1.03 | 1.17 |
| A11 | 0.45 | 0.99 | 0.97 | 1.05 | 0.95 | 0.77 | 0.90 | 1.28 |
| A12 | ∞ | 1.23 | 0.91 | 0.93 | 0.97 | 1.12 | 1.10 | 1.04 |
| A13 | ∞ | 1.57 | 0.84 | 1.95 | 1.44 | 1.70 | 1.51 | 2.07 |
| A2 | 0.49 | 0.98 | 0.80 | 0.96 | 0.88 | 0.77 | 0.82 | 0.94 |
| A3 | 0.48 | 1.08 | 0.87 | 0.95 | 0.88 | 0.91 | 0.86 | 1.03 |
| A4 | ∞ | 1.04 | 0.81 | 0.93 | 0.94 | 1.10 | 0.89 | 1.04 |
| A5 | 0.95 | 1.01 | 1.10 | 0.98 | 0.85 | 1.33 | 1.07 | 1.02 |
| A6a | 0.50 | 1.08 | 0.80 | 0.93 | 0.97 | 1.07 | 0.96 | 1.09 |
| A6b | 0.25 | 1.65 | 1.04 | 1.72 | 1.55 | 1.90 | 1.57 | 1.47 |
| A8 | 0.14 | 1.09 | 0.95 | 1.01 | 0.90 | 0.77 | 0.92 | 1.14 |
| A9 | 0.18 | 0.81 | 0.57 | 0.87 | 0.71 | 0.94 | 0.74 | 0.85 |
| A9m | ∞ | 1.03 | 1.03 | 0.98 | 0.86 | 1.17 | 0.94 | 1.00 |
| P1 | 0.94 | 1.04 | 0.99 | 1.04 | 0.92 | 1.29 | 1.08 | 1.01 |
| X1 | 0.36 | 0.88 | 0.93 | 0.63 | 0.73 | 1.00 | 0.80 | 0.71 |
| X3 | 0.43 | 1.20 | 0.91 | 1.01 | 0.80 | 0.96 | 0.88 | 1.05 |

## Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.93 | 1.01 | 0.97 |
| A1 | 0.88 | 0.95 | 0.85 |
| A10 | 1.01 | 1.00 | 1.02 |
| A11 | 0.91 | 0.94 | 0.91 |
| A12 | 1.05 | 1.05 | 1.01 |
| A13 | 1.49 | 1.34 | 1.60 |
| A2 | 0.84 | 0.88 | 0.79 |
| A3 | 0.88 | 1.03 | 0.81 |
| A4 | 0.96 | 1.01 | 0.85 |
| A5 | 1.01 | 1.00 | 1.15 |
| A6a | 0.97 | 0.94 | 0.87 |
| A6b | 1.35 | 1.51 | 1.39 |
| A8 | 0.88 | 0.94 | 0.73 |
| A9 | 0.73 | 0.80 | 0.63 |
| A9m | 0.95 | 1.04 | 0.97 |
| P1 | 0.97 | 1.05 | 1.12 |
| X1 | 0.75 | 0.88 | 0.76 |
| X3 | 0.86 | 1.02 | 0.87 |

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
| A10 | 1/3 | 4/4 | 5/5 | 6/6 | 4/4 | 3/4 | 6/6 | 4/4 |
| A11 | 1/3 | 4/4 | 5/5 | 6/6 | 4/4 | 4/4 | 5/5 | 4/4 |
| A12 | 0/3 | 4/4 | 5/5 | 6/6 | 4/4 | 3/4 | 6/6 | 4/4 |
| A13 | 0/3 | 4/4 | 5/5 | 6/6 | 4/4 | 3/4 | 6/6 | 4/4 |
| A2 | 1/3 | 4/4 | 5/5 | 6/6 | 4/4 | 4/4 | 5/5 | 4/4 |
| A3 | 1/3 | 4/4 | 5/5 | 6/6 | 4/4 | 4/4 | 6/6 | 4/4 |
| A4 | 0/3 | 4/4 | 5/5 | 6/6 | 4/4 | 3/4 | 6/6 | 4/4 |
| A5 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |
| A6a | 1/3 | 4/4 | 5/5 | 6/6 | 4/4 | 3/4 | 5/5 | 4/4 |
| A6b | 2/3 | 4/4 | 5/5 | 6/6 | 4/4 | 3/4 | 6/6 | 4/4 |
| A8 | 3/3 | 4/4 | 5/5 | 6/6 | 4/4 | 4/4 | 5/5 | 4/4 |
| A9 | 2/3 | 4/4 | 5/5 | 6/6 | 4/4 | 3/4 | 6/6 | 4/4 |
| A9m | 0/3 | 4/4 | 5/5 | 6/6 | 4/4 | 3/4 | 5/5 | 4/4 |
| P1 | 1/6 | 6/6 | 6/6 | 6/6 | 6/6 | 4/6 | 6/6 | 6/6 |
| X1 | 1/3 | 4/4 | 5/5 | 6/6 | 4/4 | 3/4 | 6/6 | 4/4 |
| X3 | 1/3 | 3/4 | 5/5 | 6/6 | 4/4 | 3/4 | 6/6 | 4/4 |

## Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 12 | 2,597 | 140,166 | 10,327 | 8 | 3 | 5.2 | 40 | 0.00 | 7% |
| A0b | 12 | 2,498 | 138,131 | 10,262 | 8 | 2 | 5.1 | 40 | 0.00 | 7% |
| A1 | 12 | 2,155 | 139,150 | 10,052 | 8 | 3 | 4.8 | 28 | 0.00 | 9% |
| A10 | 12 | 2,486 | 140,670 | 10,826 | 8 | 2 | 5.3 | 42 | 0.01 | 9% |
| A11 | 12 | 2,433 | 142,940 | 10,232 | 9 | 3 | 4.1 | 35 | 0.00 | 9% |
| A12 | 13 | 2,584 | 155,344 | 11,472 | 9 | 2 | 5.9 | 36 | 0.00 | 7% |
| A13 | 17 | 5,256 | 134,676 | 18,369 | 15 | 6 | 17.0 | 36 | 0.00 | 6% |
| A2 | 10 | 2,081 | 117,439 | 10,178 | 8 | 3 | 4.7 | 33 | 0.00 | 6% |
| A3 | 12 | 2,517 | 140,889 | 10,628 | 8 | 3 | 4.7 | 34 | 0.04 | 8% |
| A4 | 12 | 2,724 | 141,344 | 10,518 | 8 | 3 | 4.8 | 36 | 0.05 | 6% |
| A5 | 12 | 2,462 | 137,539 | 10,266 | 8 | 2 | 5.1 | 37 | 0.00 | 12% |
| A6a | 12 | 2,551 | 141,177 | 10,559 | 9 | 3 | 4.6 | 36 | 0.00 | 9% |
| A6b | 16 | 4,814 | 159,300 | 18,588 | 9 | 2 | 13.0 | 33 | 0.00 | 10% |
| A8 | 12 | 2,433 | 141,428 | 11,501 | 7 | 3 | 6.8 | 33 | 0.00 | 5% |
| A9 | 10 | 1,566 | 111,671 | 8,366 | 6 | 2 | 2.8 | 31 | 0.00 | 4% |
| A9m | 12 | 2,472 | 139,302 | 10,280 | 9 | 3 | 5.0 | 34 | 0.00 | 8% |
| P1 | 12 | 2,720 | 139,114 | 10,604 | 8 | 3 | 5.0 | 39 | 0.00 | 7% |
| X1 | 14 | 2,809 | 89,996 | 7,941 | 9 | 3 | 5.9 | 40 | 0.00 | 17% |
| X3 | 8 | 2,222 | 94,348 | 10,601 | 6 | 3 | 4.1 | 38 | 0.00 | 9% |

Cells with run-to-run spread above ±30% (worth more reps): A1 T7/v2 (38%), A11 T8/v3 (38%), A12 T3/v1 (30%), A4 T7/v2 (30%), A5 T3/v1 (33%), A5 T7/v1 (31%), A5 T7/v3 (38%), A6b T8/v3 (56%), A9m T3/v2 (39%), P1 T3/v3 (42%), X1 T3/v1 (67%), X1 T3/v2 (47%), X1 T4/v3 (37%), X3 T3/v1 (30%)


## Instruction arms against the placebo

Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?

| Arm | Ratio vs P1 | 95% CI |
| --- | --- | --- |
| A1 | 0.87 | 0.74–∞ |
| A11 | 0.86 | 0.73–∞ |
| A12 | ∞ | 0.90–∞ |
| A13 | ∞ | 1.29–∞ |
| A2 | 0.79 | 0.67–∞ |
| A3 | 0.83 | 0.72–∞ |
| A4 | ∞ | 0.83–∞ |
| A6a | 0.87 | 0.74–∞ |
| A6b | 1.18 | 1.03–∞ |
| A8 | 0.73 | 0.67–0.98 |
| X3 | 0.84 | 0.72–∞ |

## Did the technique actually happen?

Runs where the arm's mechanism is visible in the transcript. A cost result for an arm whose mechanism rarely fired says little about the technique itself. Skills can load without an explicit tool call, so a low skill count is a hint, not proof.

| Arm | Evidence | Runs |
| --- | --- | --- |
| A1 | lean-code skill tool calls | 8/48 |
| A10 | LSP tool called | 0/36 |
| A11 | repo-recipes skill tool calls | 32/35 |
| A12 | scaffold.py run | 12/36 |
| A13 | Haiku model in subagent transcripts | 28/36 |
| A5 | trimmed tool output seen | 0/48 |
| A6b | subagent used | 26/36 |
| A8 | BRIEF.md opened | 35/35 |
| A9 | effort flag passed on the command line | configured only; Claude Code doesn't report effort per run |
| A9m | effort flag passed on the command line | configured only; Claude Code doesn't report effort per run |

## Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 10.00 | 5.50 | 0.00 | not installed |
| A0b | 9.00 | 6.50 | 0.00 | not installed |
| A1 | 5.50 | 5.00 | 0.00 | not installed |
| A10 | 10.50 | 5.00 | 0.00 | not installed |
| A11 | 7.00 | 5.00 | 0.00 | not installed |
| A12 | 9.50 | 5.00 | 0.00 | not installed |
| A13 | 8.50 | 5.00 | 0.00 | not installed |
| A2 | 3.00 | 4.00 | 0.00 | not installed |
| A3 | 8.50 | 4.50 | 0.00 | not installed |
| A4 | 8.50 | 5.00 | 0.00 | not installed |
| A5 | 10.00 | 6.00 | 0.00 | not installed |
| A6a | 4.00 | 5.00 | 0.00 | not installed |
| A6b | 8.00 | 5.00 | 0.00 | not installed |
| A8 | 4.00 | 5.00 | 0.00 | not installed |
| A9 | 7.00 | 5.00 | 0.00 | not installed |
| A9m | 5.00 | 5.00 | 0.00 | not installed |
| P1 | 10.00 | 5.00 | 0.00 | not installed |
| X1 | 9.50 | 5.00 | 0.00 | not installed |
| X3 | 9.50 | 5.00 | 0.00 | not installed |

## What these results do and don't show

- **Measured:** 739 runs of Claude Code 2.1.311 (Claude Code), 2.1.312 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-28, on one Python repo of 417 lines (8 tasks × 3 wordings), each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** behaviour on larger codebases, other languages, other models or other Claude Code versions. Context-saving techniques (A6a, A6b, A8, A10, A13) are likely understated on a repo this small.
- **Effort arms** are configured via `--effort`, not verified per run.

