# Token battery — v8 · claude-opus-5-5

## Does each effect hold across suites?

Ratio vs A0 (95% CI) in each suite. A technique worth recommending should be cheaper in both small edits and full builds, or at least not more expensive in either.

| Arm | small | build | Consistent? |
| --- | --- | --- | --- |
| A0b | 0.96 (0.82–∞) | 1.02 (0.90–1.16) | not established |
| P1 | 1.05 (0.88–∞) | 1.00 (0.88–1.14) | not established |
| A1 | 0.91 (0.76–∞) | n/a | not established |
| A10 | 1.06 (0.88–∞) | n/a | not established |
| A11 | 1.04 (0.87–∞) | n/a | not established |
| A12 | 1.14 (0.93–∞) | n/a | not established |
| A13 | 1.42 (1.19–1.89) | n/a | costs more somewhere |
| A2 | 0.83 (0.72–1.01) | n/a | not established |
| A3 | 0.96 (0.81–∞) | n/a | not established |
| A4 | ∞ (1.00–∞) | n/a | not established |
| A5 | 1.11 (0.90–∞) | n/a | not established |
| A6a | 0.95 (0.81–1.18) | n/a | not established |
| A6b | 1.45 (1.21–2.00) | n/a | costs more somewhere |
| A8 | 0.80 (0.71–1.00) | n/a | not established |
| A9 | 0.73 (0.63–0.91) | n/a | not established |
| A9m | 1.08 (0.88–∞) | n/a | not established |
| X1 | 0.90 (0.72–∞) | n/a | not established |
| X3 | 1.05 (0.85–∞) | n/a | not established |


## Battery report — v8 · claude-opus-5-5 · small suite

1368 completed runs across 8 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

### Method checks (read these first)

- **A/A check:** A0b is an exact copy of A0. Ratio 0.96 (0.82–∞). **FAIL: an identical arm looks different. Treat every result below as unreliable until more reps make this interval include 1.0.**
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 1.05 (0.88–∞). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 16 arms tested. At 95% intervals, roughly 0.8 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 72 | 89% (80%–94%) | 1.00 | — | — | — | baseline |
| A0b | 72 | 89% (80%–94%) | 0.96 | 0.82–∞ | 4/8 | 13/23 | inconclusive |
| A1 | 72 | 90% (81%–95%) | 0.91 | 0.76–∞ | 7/8 | 17/23 | inconclusive |
| A10 | 72 | 88% (78%–93%) | 1.06 | 0.88–∞ | 2/8 | 7/23 | inconclusive · lower success |
| A11 | 72 | 88% (78%–93%) | 1.04 | 0.87–∞ | 3/8 | 7/23 | inconclusive · lower success |
| A12 | 72 | 85% (75%–91%) | 1.14 | 0.93–∞ | 2/8 | 9/23 | inconclusive · lower success |
| A13 | 72 | 89% (80%–94%) | 1.42 | 1.19–1.89 | 1/8 | 3/23 | costs more |
| A2 | 72 | 92% (83%–96%) | 0.83 | 0.72–1.01 | 6/8 | 16/23 | inconclusive |
| A3 | 72 | 90% (81%–95%) | 0.96 | 0.81–∞ | 6/8 | 11/23 | inconclusive |
| A4 | 72 | 81% (70%–88%) | ∞ | 1.00–∞ | 3/8 | 8/22 | inconclusive · lower success |
| A5 | 72 | 86% (76%–92%) | 1.11 | 0.90–∞ | 3/8 | 10/23 | inconclusive · lower success |
| A6a | 72 | 89% (80%–94%) | 0.95 | 0.81–1.18 | 4/8 | 11/23 | inconclusive |
| A6b | 72 | 89% (80%–94%) | 1.45 | 1.21–2.00 | 1/8 | 1/23 | costs more |
| A8 | 72 | 100% (95%–100%) | 0.80 | 0.71–1.00 | 5/8 | 13/24 | inconclusive |
| A9 | 72 | 89% (80%–94%) | 0.73 | 0.63–0.91 | 7/8 | 21/23 | **wins** |
| A9m | 72 | 88% (78%–93%) | 1.08 | 0.88–∞ | 4/8 | 13/23 | inconclusive · lower success |
| P1 | 72 | 86% (76%–92%) | 1.05 | 0.88–∞ | 2/8 | 7/23 | inconclusive · lower success |
| X1 | 72 | 85% (75%–91%) | 0.90 | 0.72–∞ | 6/8 | 18/23 | inconclusive · lower success |
| X3 | 72 | 83% (73%–90%) | 1.05 | 0.85–∞ | 3/8 | 14/23 | inconclusive · lower success |

### Ratio vs A0 by task (pooled over wordings)

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0b | 0.64 | 1.05 | 0.97 | 1.01 | 0.90 | 1.18 | 1.05 | 0.99 |
| A1 | 0.92 | 0.96 | 0.94 | 1.02 | 0.84 | 0.81 | 0.82 | 0.98 |
| A10 | 0.95 | 1.21 | 1.16 | 1.03 | 0.92 | 1.19 | 1.02 | 1.06 |
| A11 | 0.98 | 1.07 | 1.12 | 1.05 | 0.97 | 1.07 | 0.93 | 1.18 |
| A12 | 1.76 | 1.21 | 1.09 | 0.94 | 0.97 | 1.36 | 1.02 | 1.00 |
| A13 | 0.68 | 1.61 | 1.00 | 1.92 | 1.62 | 1.78 | 1.39 | 1.97 |
| A2 | 0.37 | 1.04 | 0.84 | 0.95 | 0.92 | 1.06 | 0.82 | 0.94 |
| A3 | 0.94 | 1.07 | 0.95 | 0.98 | 0.90 | 0.92 | 0.91 | 1.02 |
| A4 | ∞ | 1.07 | 1.01 | 0.94 | 0.92 | 1.32 | 0.99 | 1.02 |
| A5 | 1.83 | 1.02 | 1.15 | 0.98 | 0.89 | 1.23 | 1.01 | 0.99 |
| A6a | 0.49 | 1.14 | 0.95 | 0.94 | 1.00 | 1.30 | 0.95 | 1.07 |
| A6b | 0.72 | 1.64 | 1.32 | 1.81 | 1.58 | 1.96 | 1.60 | 1.40 |
| A8 | 0.20 | 1.08 | 0.98 | 1.06 | 0.93 | 0.82 | 0.91 | 1.08 |
| A9 | 0.37 | 0.84 | 0.61 | 0.89 | 0.71 | 1.11 | 0.73 | 0.86 |
| A9m | 1.85 | 1.03 | 1.15 | 0.99 | 0.90 | 1.02 | 0.95 | 0.98 |
| P1 | 0.94 | 1.07 | 1.03 | 1.05 | 0.93 | 1.37 | 1.04 | 1.02 |
| X1 | 1.47 | 0.87 | 0.97 | 0.63 | 0.83 | 1.24 | 0.78 | 0.67 |
| X3 | 1.74 | 1.05 | 0.99 | 1.01 | 0.80 | 1.15 | 0.84 | 1.03 |

### Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.93 | 1.03 | 1.07 |
| A1 | 0.87 | 0.94 | 0.88 |
| A10 | 1.01 | 1.04 | 1.15 |
| A11 | 0.97 | 0.97 | 1.16 |
| A12 | 1.05 | 1.04 | 1.16 |
| A13 | 1.51 | 1.40 | 1.52 |
| A2 | 0.86 | 0.90 | 0.89 |
| A3 | 0.93 | 1.03 | 0.93 |
| A4 | 1.02 | 1.11 | 1.04 |
| A5 | 1.03 | 0.99 | 1.15 |
| A6a | 0.96 | 0.97 | 1.07 |
| A6b | 1.47 | 1.48 | 1.68 |
| A8 | 0.90 | 0.88 | 0.81 |
| A9 | 0.74 | 0.81 | 0.78 |
| A9m | 1.01 | 0.99 | 1.04 |
| P1 | 0.97 | 1.03 | 1.18 |
| X1 | 0.80 | 0.83 | 0.99 |
| X3 | 0.93 | 0.96 | 1.01 |

### Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 24 | 88% | 40,438 | 15,109 | 46,215 |
| v2 | 24 | 88% | 42,649 | 16,526 | 48,741 |
| v3 | 24 | 92% | 52,015 | 21,898 | 56,744 |

### Success rate by task

| Arm | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 2/9 | 9/9 | 9/9 | 9/9 | 9/9 | 8/9 | 9/9 | 9/9 |
| A0b | 3/9 | 9/9 | 9/9 | 9/9 | 9/9 | 7/9 | 9/9 | 9/9 |
| A1 | 2/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 |
| A10 | 2/9 | 9/9 | 9/9 | 9/9 | 9/9 | 7/9 | 9/9 | 9/9 |
| A11 | 2/9 | 9/9 | 9/9 | 9/9 | 9/9 | 7/9 | 9/9 | 9/9 |
| A12 | 1/9 | 9/9 | 9/9 | 9/9 | 9/9 | 6/9 | 9/9 | 9/9 |
| A13 | 3/9 | 9/9 | 9/9 | 9/9 | 9/9 | 7/9 | 9/9 | 9/9 |
| A2 | 5/9 | 9/9 | 9/9 | 9/9 | 9/9 | 7/9 | 9/9 | 9/9 |
| A3 | 2/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 |
| A4 | 0/9 | 9/9 | 8/9 | 9/9 | 9/9 | 6/9 | 8/9 | 9/9 |
| A5 | 1/9 | 9/9 | 9/9 | 9/9 | 9/9 | 7/9 | 9/9 | 9/9 |
| A6a | 4/9 | 9/9 | 9/9 | 9/9 | 9/9 | 6/9 | 9/9 | 9/9 |
| A6b | 3/9 | 9/9 | 9/9 | 9/9 | 9/9 | 7/9 | 9/9 | 9/9 |
| A8 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 |
| A9 | 4/9 | 9/9 | 9/9 | 9/9 | 9/9 | 6/9 | 9/9 | 9/9 |
| A9m | 1/9 | 9/9 | 9/9 | 9/9 | 9/9 | 8/9 | 9/9 | 9/9 |
| P1 | 2/9 | 9/9 | 9/9 | 9/9 | 9/9 | 6/9 | 9/9 | 9/9 |
| X1 | 1/9 | 9/9 | 9/9 | 9/9 | 9/9 | 6/9 | 9/9 | 9/9 |
| X3 | 1/9 | 8/9 | 9/9 | 9/9 | 9/9 | 6/9 | 9/9 | 9/9 |

### Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 12 | 2,528 | 140,082 | 10,193 | 8 | 3 | 5.2 | 40 | 0.00 | 8% |
| A0b | 12 | 2,514 | 138,131 | 10,212 | 8 | 2 | 5.0 | 38 | 0.00 | 9% |
| A1 | 12 | 2,154 | 138,453 | 9,950 | 8 | 3 | 4.8 | 28 | 0.00 | 9% |
| A10 | 12 | 2,600 | 141,980 | 10,724 | 8 | 3 | 5.2 | 42 | 0.01 | 9% |
| A11 | 14 | 2,490 | 163,460 | 10,540 | 9 | 3 | 4.7 | 36 | 0.00 | 9% |
| A12 | 12 | 2,706 | 140,516 | 11,555 | 9 | 3 | 5.9 | 40 | 0.00 | 8% |
| A13 | 18 | 5,347 | 141,974 | 18,169 | 15 | 6 | 16.1 | 37 | 0.00 | 12% |
| A2 | 12 | 2,176 | 138,028 | 10,296 | 8 | 3 | 4.7 | 33 | 0.00 | 8% |
| A3 | 12 | 2,528 | 140,889 | 10,496 | 8 | 3 | 4.9 | 34 | 0.05 | 8% |
| A4 | 12 | 2,584 | 141,214 | 10,520 | 8 | 3 | 4.8 | 36 | 0.04 | 6% |
| A5 | 12 | 2,462 | 137,296 | 10,212 | 8 | 2 | 5.0 | 38 | 0.00 | 11% |
| A6a | 14 | 2,692 | 160,754 | 10,723 | 9 | 3 | 4.7 | 36 | 0.00 | 7% |
| A6b | 16 | 4,920 | 154,791 | 18,952 | 9 | 2 | 12.5 | 36 | 0.00 | 12% |
| A8 | 10 | 2,448 | 120,614 | 11,295 | 7 | 3 | 7.3 | 33 | 0.00 | 8% |
| A9 | 10 | 1,566 | 110,288 | 8,378 | 6 | 2 | 3.0 | 31 | 0.00 | 4% |
| A9m | 12 | 2,551 | 139,166 | 10,258 | 8 | 3 | 5.0 | 35 | 0.00 | 8% |
| P1 | 12 | 2,629 | 139,766 | 10,604 | 8 | 3 | 5.2 | 38 | 0.00 | 7% |
| X1 | 14 | 2,742 | 88,218 | 7,341 | 9 | 3 | 5.6 | 42 | 0.00 | 14% |
| X3 | 8 | 2,214 | 94,304 | 10,520 | 6 | 3 | 4.0 | 38 | 0.00 | 6% |

Cells with run-to-run spread above ±30% (worth more reps): A11 T8/v3 (33%), A13 T5/v2 (33%), A6b T1/v3 (36%), A6b T8/v1 (50%), A6b T8/v3 (53%), A9m T3/v1 (31%), A9m T3/v2 (31%), X1 T3/v1 (63%), X1 T3/v2 (45%), X1 T5/v3 (33%), X3 T3/v1 (31%)


### Instruction arms against the placebo

Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?

| Arm | Ratio vs P1 | 95% CI |
| --- | --- | --- |
| A1 | 0.86 | 0.72–∞ |
| A11 | 1.00 | 0.81–∞ |
| A12 | 1.09 | 0.87–∞ |
| A13 | 1.36 | 1.12–1.77 |
| A2 | 0.79 | 0.67–0.96 |
| A3 | 0.91 | 0.76–∞ |
| A4 | ∞ | 0.92–∞ |
| A6a | 0.91 | 0.76–1.13 |
| A6b | 1.38 | 1.14–1.96 |
| A8 | 0.76 | 0.66–0.94 |
| X3 | 1.00 | 0.80–∞ |

### Did the technique actually happen?

Runs where the arm's mechanism is visible in the transcript. A cost result for an arm whose mechanism rarely fired says little about the technique itself. Skills can load without an explicit tool call, so a low skill count is a hint, not proof.

| Arm | Evidence | Runs |
| --- | --- | --- |
| A1 | lean-code skill tool calls | 10/72 |
| A10 | LSP tool called | 0/72 |
| A11 | repo-recipes skill tool calls | 67/72 |
| A12 | scaffold.py run | 19/72 |
| A13 | Haiku model in subagent transcripts | 54/72 |
| A5 | trimmed tool output seen | 0/72 |
| A6b | subagent used | 51/72 |
| A8 | BRIEF.md opened | 72/72 |
| A9 | effort flag passed on the command line | configured only; Claude Code doesn't report effort per run |
| A9m | effort flag passed on the command line | configured only; Claude Code doesn't report effort per run |

### Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 10.00 | 5.50 | 0.00 | not installed |
| A0b | 9.00 | 6.50 | 0.00 | not installed |
| A1 | 5.50 | 5.00 | 0.00 | not installed |
| A10 | 10.50 | 6.50 | 0.00 | not installed |
| A11 | 9.50 | 5.50 | 0.00 | not installed |
| A12 | 9.00 | 6.00 | 0.00 | not installed |
| A13 | 8.50 | 6.50 | 0.00 | not installed |
| A2 | 7.50 | 6.00 | 0.00 | not installed |
| A3 | 8.50 | 6.00 | 0.00 | not installed |
| A4 | 8.50 | 6.00 | 0.00 | not installed |
| A5 | 10.00 | 6.00 | 0.00 | not installed |
| A6a | 9.50 | 6.00 | 0.00 | not installed |
| A6b | 8.00 | 6.00 | 0.00 | not installed |
| A8 | 8.00 | 6.00 | 0.00 | not installed |
| A9 | 7.00 | 6.00 | 0.00 | not installed |
| A9m | 9.50 | 5.00 | 0.00 | not installed |
| P1 | 10.50 | 5.00 | 0.00 | not installed |
| X1 | 9.50 | 6.00 | 0.00 | not installed |
| X3 | 8.50 | 5.50 | 0.00 | not installed |

### What these results do and don't show

- **Measured:** 1368 runs of Claude Code 2.1.311 (Claude Code), 2.1.312 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-28, on one Python repo of 417 lines (8 tasks × 3 wordings), each run in a fresh, isolated configuration.
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

