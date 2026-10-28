# Battery report — v8 · claude-opus-5-5 · small suite

1132 completed runs across 8 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

## Method checks (read these first)

- **A/A check:** A0b is an exact copy of A0. Ratio 0.95 (0.81–∞). **FAIL: an identical arm looks different. Treat every result below as unreliable until more reps make this interval include 1.0.**
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 1.06 (0.88–∞). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 16 arms tested. At 95% intervals, roughly 0.8 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 60 | 88% (78%–94%) | 1.00 | — | — | — | baseline |
| A0b | 59 | 88% (77%–94%) | 0.95 | 0.81–∞ | 4/8 | 13/23 | inconclusive · lower success |
| A1 | 60 | 90% (80%–95%) | 0.90 | 0.75–∞ | 7/8 | 16/23 | inconclusive |
| A10 | 59 | 86% (75%–93%) | 1.06 | 0.87–∞ | 3/8 | 9/23 | inconclusive · lower success |
| A11 | 60 | 87% (76%–93%) | 1.03 | 0.85–∞ | 3/8 | 9/23 | inconclusive · lower success |
| A12 | 59 | 83% (72%–91%) | 1.16 | 0.94–∞ | 3/8 | 10/23 | inconclusive · lower success |
| A13 | 60 | 88% (78%–94%) | 1.43 | 1.22–1.89 | 1/8 | 3/23 | costs more |
| A2 | 59 | 92% (82%–96%) | 0.83 | 0.71–1.01 | 6/8 | 18/23 | inconclusive |
| A3 | 60 | 90% (80%–95%) | 0.94 | 0.78–∞ | 6/8 | 13/23 | inconclusive |
| A4 | 59 | 80% (68%–88%) | ∞ | 0.99–∞ | 3/8 | 9/22 | inconclusive · lower success |
| A5 | 60 | 85% (74%–92%) | 1.11 | 0.90–∞ | 2/8 | 9/23 | inconclusive · lower success |
| A6a | 59 | 88% (77%–94%) | 0.95 | 0.81–1.22 | 4/8 | 11/23 | inconclusive · lower success |
| A6b | 59 | 88% (77%–94%) | 1.42 | 1.18–1.93 | 1/8 | 1/23 | costs more · lower success |
| A8 | 60 | 100% (94%–100%) | 0.80 | 0.71–0.99 | 5/8 | 12/24 | **wins** |
| A9 | 59 | 88% (77%–94%) | 0.74 | 0.63–0.95 | 7/8 | 21/23 | inconclusive · lower success |
| A9m | 60 | 87% (76%–93%) | 1.08 | 0.87–∞ | 4/8 | 13/23 | inconclusive · lower success |
| P1 | 60 | 85% (74%–92%) | 1.06 | 0.88–∞ | 2/8 | 8/23 | inconclusive · lower success |
| X1 | 60 | 83% (72%–91%) | 0.90 | 0.72–∞ | 6/8 | 19/23 | inconclusive · lower success |
| X3 | 60 | 82% (70%–89%) | 1.07 | 0.87–∞ | 3/8 | 14/23 | inconclusive · lower success |

## Ratio vs A0 by task (pooled over wordings)

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0b | 0.63 | 1.06 | 0.92 | 1.02 | 0.90 | 1.21 | 1.03 | 0.97 |
| A1 | 0.92 | 0.96 | 0.95 | 1.01 | 0.84 | 0.79 | 0.79 | 0.98 |
| A10 | 0.93 | 1.23 | 1.12 | 1.03 | 0.92 | 1.26 | 0.96 | 1.05 |
| A11 | 0.98 | 1.07 | 1.02 | 1.05 | 0.96 | 1.11 | 0.90 | 1.20 |
| A12 | 1.78 | 1.21 | 1.04 | 0.94 | 0.99 | 1.53 | 1.04 | 1.00 |
| A13 | 0.68 | 1.61 | 1.02 | 2.00 | 1.56 | 1.93 | 1.38 | 1.94 |
| A2 | 0.38 | 1.03 | 0.84 | 0.97 | 0.90 | 1.11 | 0.77 | 0.95 |
| A3 | 0.92 | 1.08 | 0.92 | 0.96 | 0.90 | 0.90 | 0.84 | 1.02 |
| A4 | ∞ | 1.07 | 1.02 | 0.94 | 0.92 | 1.48 | 0.83 | 1.00 |
| A5 | 1.85 | 1.03 | 1.11 | 0.98 | 0.86 | 1.29 | 1.02 | 1.00 |
| A6a | 0.49 | 1.15 | 0.92 | 0.93 | 1.00 | 1.45 | 0.92 | 1.08 |
| A6b | 0.72 | 1.64 | 1.16 | 1.76 | 1.57 | 2.07 | 1.48 | 1.44 |
| A8 | 0.22 | 1.09 | 0.98 | 1.04 | 0.93 | 0.79 | 0.89 | 1.08 |
| A9 | 0.37 | 0.85 | 0.62 | 0.89 | 0.71 | 1.26 | 0.70 | 0.86 |
| A9m | 1.85 | 1.05 | 1.18 | 0.98 | 0.88 | 1.03 | 0.91 | 0.98 |
| P1 | 0.94 | 1.07 | 1.00 | 1.04 | 0.91 | 1.56 | 1.02 | 1.01 |
| X1 | 1.47 | 0.87 | 0.93 | 0.62 | 0.79 | 1.42 | 0.76 | 0.67 |
| X3 | 1.74 | 1.07 | 0.99 | 1.02 | 0.81 | 1.29 | 0.83 | 1.03 |

## Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.89 | 1.01 | 1.08 |
| A1 | 0.85 | 0.95 | 0.89 |
| A10 | 1.00 | 1.00 | 1.16 |
| A11 | 0.95 | 0.96 | 1.16 |
| A12 | 1.05 | 1.05 | 1.20 |
| A13 | 1.51 | 1.40 | 1.52 |
| A2 | 0.82 | 0.89 | 0.90 |
| A3 | 0.90 | 1.02 | 0.92 |
| A4 | 1.03 | 1.06 | 1.07 |
| A5 | 1.01 | 1.00 | 1.17 |
| A6a | 0.93 | 0.98 | 1.07 |
| A6b | 1.37 | 1.45 | 1.64 |
| A8 | 0.87 | 0.92 | 0.78 |
| A9 | 0.71 | 0.80 | 0.81 |
| A9m | 0.98 | 1.02 | 1.05 |
| P1 | 0.94 | 1.04 | 1.23 |
| X1 | 0.80 | 0.82 | 1.01 |
| X3 | 0.93 | 0.99 | 1.05 |

## Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 20 | 85% | 39,270 | 14,317 | 46,200 |
| v2 | 20 | 90% | 40,628 | 15,852 | 45,142 |
| v3 | 20 | 90% | 54,114 | 22,829 | 60,127 |

## Success rate by task

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 2/8 | 8/8 | 8/8 | 7/7 | 7/7 | 6/7 | 7/7 | 8/8 |
| A0b | 3/8 | 8/8 | 8/8 | 7/7 | 7/7 | 5/7 | 6/6 | 8/8 |
| A1 | 2/8 | 8/8 | 8/8 | 7/7 | 7/7 | 7/7 | 7/7 | 8/8 |
| A10 | 2/8 | 8/8 | 8/8 | 7/7 | 7/7 | 5/7 | 6/6 | 8/8 |
| A11 | 2/8 | 8/8 | 8/8 | 7/7 | 7/7 | 5/7 | 7/7 | 8/8 |
| A12 | 1/8 | 8/8 | 8/8 | 7/7 | 7/7 | 4/7 | 6/6 | 8/8 |
| A13 | 3/8 | 8/8 | 8/8 | 7/7 | 7/7 | 5/7 | 7/7 | 8/8 |
| A2 | 5/8 | 8/8 | 8/8 | 7/7 | 7/7 | 5/7 | 6/6 | 8/8 |
| A3 | 2/8 | 8/8 | 8/8 | 7/7 | 7/7 | 7/7 | 7/7 | 8/8 |
| A4 | 0/8 | 8/8 | 7/8 | 7/7 | 7/7 | 4/7 | 6/6 | 8/8 |
| A5 | 1/8 | 8/8 | 8/8 | 7/7 | 7/7 | 5/7 | 7/7 | 8/8 |
| A6a | 4/8 | 8/8 | 8/8 | 7/7 | 7/7 | 4/7 | 6/6 | 8/8 |
| A6b | 3/8 | 8/8 | 8/8 | 7/7 | 7/7 | 5/7 | 6/6 | 8/8 |
| A8 | 8/8 | 8/8 | 8/8 | 7/7 | 7/7 | 7/7 | 7/7 | 8/8 |
| A9 | 4/8 | 8/8 | 8/8 | 7/7 | 7/7 | 4/7 | 6/6 | 8/8 |
| A9m | 1/8 | 8/8 | 8/8 | 7/7 | 7/7 | 6/7 | 7/7 | 8/8 |
| P1 | 2/8 | 8/8 | 8/8 | 7/7 | 7/7 | 4/7 | 7/7 | 8/8 |
| X1 | 1/8 | 8/8 | 8/8 | 7/7 | 7/7 | 4/7 | 7/7 | 8/8 |
| X3 | 1/8 | 7/8 | 8/8 | 7/7 | 7/7 | 4/7 | 7/7 | 8/8 |

## Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 12 | 2,410 | 137,766 | 10,112 | 8 | 3 | 5.2 | 40 | 0.00 | 8% |
| A0b | 12 | 2,433 | 137,835 | 10,180 | 8 | 2 | 5.0 | 33 | 0.00 | 7% |
| A1 | 12 | 2,142 | 138,231 | 9,927 | 8 | 3 | 4.8 | 28 | 0.00 | 10% |
| A10 | 12 | 2,396 | 139,505 | 10,457 | 8 | 3 | 5.0 | 34 | 0.02 | 8% |
| A11 | 14 | 2,424 | 162,580 | 10,375 | 9 | 3 | 4.5 | 36 | 0.00 | 8% |
| A12 | 12 | 2,627 | 138,609 | 11,401 | 9 | 3 | 5.6 | 31 | 0.00 | 7% |
| A13 | 16 | 5,256 | 137,778 | 18,109 | 15 | 6 | 16.1 | 36 | 0.00 | 10% |
| A2 | 12 | 2,040 | 136,388 | 10,101 | 8 | 3 | 4.7 | 32 | 0.00 | 8% |
| A3 | 12 | 2,497 | 140,436 | 10,454 | 8 | 3 | 4.8 | 30 | 0.05 | 6% |
| A4 | 12 | 2,447 | 139,903 | 10,391 | 8 | 3 | 4.8 | 30 | 0.05 | 6% |
| A5 | 12 | 2,447 | 136,730 | 10,146 | 8 | 2 | 5.0 | 36 | 0.00 | 11% |
| A6a | 12 | 2,594 | 152,267 | 10,569 | 9 | 3 | 4.6 | 34 | 0.00 | 6% |
| A6b | 16 | 4,584 | 152,412 | 18,372 | 9 | 2 | 11.4 | 31 | 0.00 | 12% |
| A8 | 10 | 2,390 | 120,239 | 11,251 | 7 | 3 | 6.9 | 33 | 0.00 | 7% |
| A9 | 10 | 1,519 | 110,221 | 8,351 | 6 | 1 | 3.0 | 31 | 0.00 | 4% |
| A9m | 12 | 2,551 | 138,542 | 10,258 | 8 | 3 | 5.0 | 34 | 0.00 | 7% |
| P1 | 12 | 2,532 | 139,074 | 10,515 | 8 | 3 | 5.0 | 38 | 0.00 | 7% |
| X1 | 14 | 2,468 | 86,967 | 7,101 | 9 | 3 | 5.3 | 34 | 0.00 | 15% |
| X3 | 8 | 2,200 | 94,222 | 10,511 | 6 | 3 | 4.0 | 35 | 0.00 | 7% |

Cells with run-to-run spread above ±30% (worth more reps): A1 T7/v2 (38%), A11 T8/v3 (38%), A13 T5/v2 (33%), A4 T7/v2 (30%), A5 T7/v1 (31%), A6b T1/v3 (36%), A6b T8/v1 (50%), A6b T8/v3 (56%), A8 T3/v3 (34%), A9m T3/v1 (31%), A9m T3/v2 (31%), P1 T3/v3 (42%), X1 T3/v1 (63%), X1 T3/v2 (45%), X1 T4/v3 (37%), X1 T5/v3 (47%), X3 T3/v1 (31%)


## Instruction arms against the placebo

Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?

| Arm | Ratio vs P1 | 95% CI |
| --- | --- | --- |
| A1 | 0.85 | 0.70–∞ |
| A11 | 0.98 | 0.79–∞ |
| A12 | 1.10 | 0.86–∞ |
| A13 | 1.36 | 1.12–1.80 |
| A2 | 0.79 | 0.65–0.96 |
| A3 | 0.89 | 0.73–∞ |
| A4 | ∞ | 0.91–∞ |
| A6a | 0.90 | 0.74–1.15 |
| A6b | 1.35 | 1.08–1.86 |
| A8 | 0.76 | 0.64–0.93 |
| X3 | 1.01 | 0.80–∞ |

## Did the technique actually happen?

Runs where the arm's mechanism is visible in the transcript. A cost result for an arm whose mechanism rarely fired says little about the technique itself. Skills can load without an explicit tool call, so a low skill count is a hint, not proof.

| Arm | Evidence | Runs |
| --- | --- | --- |
| A1 | lean-code skill tool calls | 8/60 |
| A10 | LSP tool called | 0/59 |
| A11 | repo-recipes skill tool calls | 56/60 |
| A12 | scaffold.py run | 15/59 |
| A13 | Haiku model in subagent transcripts | 44/60 |
| A5 | trimmed tool output seen | 0/60 |
| A6b | subagent used | 40/59 |
| A8 | BRIEF.md opened | 60/60 |
| A9 | effort flag passed on the command line | configured only; Claude Code doesn't report effort per run |
| A9m | effort flag passed on the command line | configured only; Claude Code doesn't report effort per run |

## Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 4.00 | 5.50 | 0.00 | not installed |
| A0b | 4.00 | 5.00 | 0.00 | not installed |
| A1 | 3.00 | 5.00 | 0.00 | not installed |
| A10 | 3.00 | 5.00 | 0.00 | not installed |
| A11 | 5.50 | 5.00 | 0.00 | not installed |
| A12 | 4.00 | 5.00 | 0.00 | not installed |
| A13 | 3.50 | 6.00 | 0.00 | not installed |
| A2 | 3.00 | 5.00 | 0.00 | not installed |
| A3 | 3.50 | 6.00 | 0.00 | not installed |
| A4 | 3.00 | 5.00 | 0.00 | not installed |
| A5 | 4.00 | 6.00 | 0.00 | not installed |
| A6a | 4.00 | 5.00 | 0.00 | not installed |
| A6b | 4.00 | 5.00 | 0.00 | not installed |
| A8 | 4.00 | 6.00 | 0.00 | not installed |
| A9 | 4.00 | 5.00 | 0.00 | not installed |
| A9m | 4.00 | 5.00 | 0.00 | not installed |
| P1 | 4.00 | 5.00 | 0.00 | not installed |
| X1 | 4.00 | 6.00 | 0.00 | not installed |
| X3 | 3.00 | 5.50 | 0.00 | not installed |

## What these results do and don't show

- **Measured:** 1132 runs of Claude Code 2.1.311 (Claude Code), 2.1.312 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-28, on one Python repo of 417 lines (8 tasks × 3 wordings), each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** behaviour on larger codebases, other languages, other models or other Claude Code versions. Context-saving techniques (A6a, A6b, A8, A10, A13) are likely understated on a repo this small.
- **Effort arms** are configured via `--effort`, not verified per run.

