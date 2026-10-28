# Battery report — v8 · claude-opus-5-5 · build suite

18 completed runs across 1 tasks × 3 wordings. **Ratio** = cost-weighted tokens per successful task vs A0, pooled over wordings within each task and combined across tasks by geometric mean; below 1.0 is cheaper. An arm **wins** only if its whole 95% interval is below 1.0 and its success rate is at least the baseline's.

## Method checks (read these first)

- **A/A check:** A0b is an exact copy of A0. Ratio 1.02 (0.90–1.16). Pass: the interval includes 1.0, so the method isn't inventing differences.
- **Placebo:** P1 adds a CLAUDE.md with no instructions. Ratio vs A0 1.00 (0.88–1.14). Instruction arms are also compared against P1 below, which removes the effect of merely having extra text.
- **Multiple comparisons:** 0 arms tested. At 95% intervals, roughly 0.0 could exclude 1.0 by chance alone. Treat a win as established only after it repeats in the independent `confirm` mode.


| Arm | Runs | Success (95% CI) | Ratio vs A0 | 95% CI | Cheaper in tasks | Cheaper in task×wording cells | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 6 | 100% (61%–100%) | 1.00 | — | — | — | baseline |
| A0b | 6 | 100% (61%–100%) | 1.02 | 0.90–1.16 | 0/1 | 1/3 | inconclusive |
| P1 | 6 | 100% (61%–100%) | 1.00 | 0.88–1.14 | 0/1 | 1/3 | inconclusive |

## Ratio vs A0 by task (pooled over wordings)

| Arm | B1 |
| --- | --- |
| A0b | 1.02 |
| P1 | 1.00 |

## Does the effect survive rewording? Ratio vs A0 by wording (pooled over tasks)

v1 = precise spec, v2 = casual/terse, v3 = goal or user-story style.

| Arm | v1 | v2 | v3 |
| --- | --- | --- | --- |
| A0b | 0.99 | 1.03 | 1.05 |
| P1 | 0.91 | 1.09 | 1.01 |

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
| P1 | 6 | 98% (98%–99%) | 100% | 100% | 96% | 94% | 100% | 1788.50 | 1440.00 |

## Success rate by task

| Arm | B1 |
| --- | --- |
| A0 | 6/6 |
| A0b | 6/6 |
| P1 | 6/6 |

## Where the tokens go (medians per run)

| Arm | Input | Output | Cache read | Cache write | Tool calls | Files read | Tool-result KB | Lines added | Comment share | Run-to-run spread (CV) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A0 | 53 | 77,506 | 1,713,744 | 94,518 | 52 | 0 | 12.9 | 3,238 | 0.02 | 11% |
| A0b | 58 | 76,537 | 2,024,384 | 94,917 | 54 | 0 | 14.4 | 3,304 | 0.02 | 9% |
| P1 | 53 | 76,910 | 1,686,766 | 96,980 | 54 | 1 | 17.3 | 3,251 | 0.03 | 11% |

Cells with run-to-run spread above ±30% (worth more reps): none


## Code quality of what was changed (medians per run)

Complexity is summed cyclomatic complexity of changed Python files (after minus before). Cheaper is only better if these don't get worse.

| Arm | Complexity change | Max function complexity | Unused imports | Ruff issues |
| --- | --- | --- | --- | --- |
| A0 | 925.00 | 27.00 | 0.00 | not installed |
| A0b | 942.00 | 22.50 | 0.00 | not installed |
| P1 | 938.00 | 23.00 | 0.00 | not installed |

## What these results do and don't show

- **Measured:** 18 runs of Claude Code 2.1.311 (Claude Code) with claude-opus-5-5, 2026-10-27 to 2026-10-27, building a project from an empty folder (1 build task(s) × 3 wordings, multi-step sessions), graded by hidden acceptance tests; success means a pass rate of at least 90%, each run in a fresh, isolated configuration.
- **Cost is a proxy:** weighted tokens use API price ratios. How a Pro or Max plan's limits weigh each token type is not published, so plan-percentage savings may differ.
- **Not shown:** other projects, languages, models or Claude Code versions. Each build follows one fixed interface contract, so this measures building to a spec, not open-ended design.
- **Effort arms** are configured via `--effort`, not verified per run.

