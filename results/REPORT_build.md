# Battery report — v8 · claude-opus-5-5 · build suite

33 completed runs across 1 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

## Method checks (read these first)

- **A/A check:** A0b is an exact copy of A0. Ratio 1.02 (0.90–1.16). Pass: the interval includes 1.0, so the method isn't inventing differences.
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 1.00 (0.88–1.14). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 12 arms tested. At 95% intervals, roughly 0.6 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 6 | 100% (61%–100%) | 1.00 | — | — | — | baseline |
| A0b | 6 | 100% (61%–100%) | 1.02 | 0.90–1.16 | 0/1 | 1/3 | inconclusive |
| A1 | 1 | 100% (21%–100%) | 0.91 | — | 1/1 | 0/1 | insufficient reps (need ≥3 runs per task) |
| A10 | 2 | 100% (34%–100%) | 1.02 | — | 0/1 | 1/2 | insufficient reps (need ≥3 runs per task) |
| A13 | 2 | 100% (34%–100%) | 0.94 | — | 1/1 | 1/2 | insufficient reps (need ≥3 runs per task) |
| A2 | 1 | 100% (21%–100%) | 0.77 | — | 1/1 | 1/1 | insufficient reps (need ≥3 runs per task) |
| A3 | 1 | 100% (21%–100%) | 0.85 | — | 1/1 | 1/1 | insufficient reps (need ≥3 runs per task) |
| A4 | 1 | 100% (21%–100%) | 0.89 | — | 1/1 | 1/1 | insufficient reps (need ≥3 runs per task) |
| A5 | 1 | 100% (21%–100%) | 0.94 | — | 1/1 | 0/1 | insufficient reps (need ≥3 runs per task) |
| A6a | 1 | 100% (21%–100%) | 1.15 | — | 0/1 | 0/1 | insufficient reps (need ≥3 runs per task) |
| A6b | 1 | 100% (21%–100%) | 1.00 | — | 1/1 | 0/1 | insufficient reps (need ≥3 runs per task) |
| A9 | 2 | 100% (34%–100%) | 0.51 | — | 1/1 | 2/2 | insufficient reps (need ≥3 runs per task) |
| A9m | 1 | 100% (21%–100%) | 0.95 | — | 1/1 | 0/1 | insufficient reps (need ≥3 runs per task) |
| P1 | 6 | 100% (61%–100%) | 1.00 | 0.88–1.14 | 0/1 | 1/3 | inconclusive |
| X1 | 1 | 100% (21%–100%) | 0.85 | — | 1/1 | 1/1 | insufficient reps (need ≥3 runs per task) |

## Ratio vs A0 by task (pooled over wordings)

| Arm | B1 |
| --- | --- |
| A0b | 1.02 |
| A1 | 0.91 |
| A10 | 1.02 |
| A13 | 0.94 |
| A2 | 0.77 |
| A3 | 0.85 |
| A4 | 0.89 |
| A5 | 0.94 |
| A6a | 1.15 |
| A6b | 1.00 |
| A9 | 0.51 |
| A9m | 0.95 |
| P1 | 1.00 |
| X1 | 0.85 |

## Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.99 | 1.03 | 1.05 |
| A1 | — | 1.02 | — |
| A10 | 0.99 | 1.18 | — |
| A13 | 0.95 | 1.03 | — |
| A2 | — | 0.86 | — |
| A3 | — | 0.95 | — |
| A4 | — | 0.99 | — |
| A5 | — | 1.05 | — |
| A6a | — | 1.29 | — |
| A6b | — | 1.12 | — |
| A9 | 0.49 | 0.59 | — |
| A9m | — | 1.06 | — |
| P1 | 0.91 | 1.09 | 1.01 |
| X1 | — | 0.95 | — |

## Baseline cost by wording (does phrasing alone change cost?)

| Wording | Runs | Success | Mean weighted tokens | SD | Cost per success |
| --- | --- | --- | --- | --- | --- |
| v1 | 2 | 100% | 669,199 | 20,410 | 669,199 |
| v2 | 2 | 100% | 595,448 | 75,546 | 595,448 |
| v3 | 2 | 100% | 728,984 | 122,351 | 728,984 |

## Hidden acceptance tests (build tasks)

Mean share of hidden acceptance tests passed per run, with a bootstrap 95% interval over runs, then the mean per test file (one file per build step). A technique that saves tokens but lowers these is trading quality for cost.

| Arm | Runs | Mean pass rate (95% CI) | test_b1_step1_core | test_b1_step2_storage | test_b1_step3_features | test_b1_step4_cli | Own tests pass | Package lines | Test lines |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 6 | 98% (98%–99%) | 99% | 100% | 96% | 98% | 100% | 1752.50 | 1538.50 |
| A0b | 6 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1731.50 | 1601.50 |
| A1 | 1 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1403.00 | 1150.00 |
| A10 | 2 | 98% (98%–99%) | 100% | 100% | 96% | 94% | 100% | 1764.50 | 1555.50 |
| A13 | 2 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1635.00 | 1617.00 |
| A2 | 1 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1464.00 | 1107.00 |
| A3 | 1 | 100% (100%–100%) | 100% | 100% | 100% | 100% | 100% | 1394.00 | 1221.00 |
| A4 | 1 | 97% (97%–97%) | 98% | 100% | 96% | 88% | 100% | 1507.00 | 1314.00 |
| A5 | 1 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1706.00 | 1363.00 |
| A6a | 1 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1644.00 | 1440.00 |
| A6b | 1 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1673.00 | 1503.00 |
| A9 | 2 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1202.50 | 626.00 |
| A9m | 1 | 100% (100%–100%) | 100% | 100% | 100% | 100% | 100% | 1751.00 | 1602.00 |
| P1 | 6 | 98% (98%–99%) | 100% | 100% | 96% | 94% | 100% | 1788.50 | 1440.00 |
| X1 | 1 | 99% (99%–99%) | 100% | 100% | 96% | 100% | 100% | 1620.00 | 1388.00 |

## Success rate by task

| Arm | B1 |
| --- | --- |
| A0 | 6/6 |
| A0b | 6/6 |
| A1 | 1/1 |
| A10 | 2/2 |
| A13 | 2/2 |
| A2 | 1/1 |
| A3 | 1/1 |
| A4 | 1/1 |
| A5 | 1/1 |
| A6a | 1/1 |
| A6b | 1/1 |
| A9 | 2/2 |
| A9m | 1/1 |
| P1 | 6/6 |
| X1 | 1/1 |

## Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 53 | 77,506 | 1,713,744 | 94,518 | 52 | 0 | 12.9 | 3,238 | 0.02 | 11% |
| A0b | 58 | 76,537 | 2,024,384 | 94,917 | 54 | 0 | 14.4 | 3,304 | 0.02 | 9% |
| A1 | 52 | 69,850 | 1,730,354 | 85,526 | 43 | 0 | 9.3 | 2,566 | 0.02 | — |
| A10 | 51 | 78,510 | 1,759,196 | 99,670 | 51 | 0 | 12.0 | 3,334 | 0.02 | — |
| A13 | 50 | 72,838 | 1,620,846 | 90,102 | 52 | 0 | 11.8 | 3,260 | 0.03 | — |
| A2 | 38 | 61,440 | 950,088 | 77,209 | 40 | 0 | 9.3 | 2,581 | 0.01 | — |
| A3 | 46 | 66,500 | 1,360,670 | 82,811 | 45 | 0 | 10.6 | 2,628 | 0.02 | — |
| A4 | 46 | 68,893 | 1,438,184 | 86,088 | 48 | 0 | 12.0 | 2,834 | 0.02 | — |
| A5 | 46 | 74,555 | 1,431,872 | 90,862 | 48 | 0 | 11.4 | 3,082 | 0.02 | — |
| A6a | 78 | 84,221 | 2,695,704 | 105,722 | 71 | 1 | 20.3 | 3,106 | 0.02 | — |
| A6b | 62 | 74,956 | 2,099,016 | 92,336 | 55 | 0 | 13.1 | 3,176 | 0.03 | — |
| A9 | 29 | 39,872 | 671,926 | 54,392 | 31 | 0 | 7.6 | 1,828 | 0.02 | — |
| A9m | 44 | 76,191 | 1,287,959 | 93,976 | 52 | 0 | 13.7 | 3,377 | 0.03 | — |
| P1 | 53 | 76,910 | 1,686,766 | 96,980 | 54 | 1 | 17.3 | 3,251 | 0.03 | 11% |
| X1 | 46 | 69,653 | 1,030,512 | 81,762 | 45 | 0 | 10.5 | 3,008 | 0.02 | — |

Cells with run-to-run spread above ±30% (worth more reps): none


## Instruction arms against the placebo

Ratio vs P1 instead of A0: does the specific instruction beat an equally long, instruction-free CLAUDE.md?

| Arm | Ratio vs P1 | 95% CI |
| --- | --- | --- |
| A1 | 0.91 | — |
| A13 | 0.94 | — |
| A2 | 0.77 | — |
| A3 | 0.85 | — |
| A4 | 0.88 | — |
| A6a | 1.15 | — |
| A6b | 1.00 | — |

## Did the technique actually happen?

Runs where the arm's mechanism is visible in the transcript. A cost result for an arm whose mechanism rarely fired says little about the technique itself. Skills can load without an explicit tool call, so a low skill count is a hint, not proof.

| Arm | Evidence | Runs |
| --- | --- | --- |
| A1 | lean-code skill tool calls | 0/1 |
| A10 | LSP tool called | 0/2 |
| A13 | Haiku model in subagent transcripts | 0/2 |
| A5 | trimmed tool output seen | 0/1 |
| A6b | subagent used | 0/1 |
| A9 | effort flag passed on the command line | configured only; Claude Code doesn't report effort per run |
| A9m | effort flag passed on the command line | configured only; Claude Code doesn't report effort per run |

## Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 925.00 | 27.00 | 0.00 | not installed |
| A0b | 942.00 | 22.50 | 0.00 | not installed |
| A1 | 762.00 | 25.00 | 0.00 | not installed |
| A10 | 972.50 | 30.50 | 0.00 | not installed |
| A13 | 910.00 | 17.00 | 0.50 | not installed |
| A2 | 770.00 | 22.00 | 0.00 | not installed |
| A3 | 764.00 | 19.00 | 0.00 | not installed |
| A4 | 889.00 | 24.00 | 0.00 | not installed |
| A5 | 912.00 | 26.00 | 0.00 | not installed |
| A6a | 912.00 | 26.00 | 0.00 | not installed |
| A6b | 932.00 | 17.00 | 0.00 | not installed |
| A9 | 560.00 | 18.00 | 0.00 | not installed |
| A9m | 927.00 | 22.00 | 0.00 | not installed |
| P1 | 938.00 | 23.00 | 0.00 | not installed |
| X1 | 894.00 | 20.00 | 1.00 | not installed |

## What these results do and don't show

- **Measured:** 33 runs of Claude Code 2.1.311 (Claude Code), 2.1.312 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-28, building a project from an empty folder (1 build task(s) × 3 wordings, multi-step sessions), graded by hidden acceptance tests; success means a pass rate of at least 90%, each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** other projects, languages, models or Claude Code versions. Each build follows one fixed interface contract, so this measures building to a spec, not open-ended design.
- **Effort arms** are configured via `--effort`, not verified per run.

