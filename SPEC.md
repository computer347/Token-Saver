# Token-Reduction Test Battery — Spec for Claude Code

Oct 23, 2026 · @Mike

## Purpose

This battery measures which token-reduction techniques actually save Claude subscription quota on real coding tasks, without lowering task success. The headline number is cost-weighted tokens per successful task, relative to stock Claude Code.

To use it, export this doc as Markdown, save it as `SPEC.md` in a new repo, and ask Claude Code to build the harness and run the pilot.

Rules for the agent building this:

- Build the harness first. Run nothing beyond the pilot until the pre-flight checks pass and the pilot report is reviewed.
- Never change task prompts, arms or success checks mid-battery. Any change starts a new battery version.
- Report results as measured, including arms that lose or make things worse.

## Isolation

Every run starts from an identical, clean state: no shared cache, config, memory or repo state from earlier runs. Each leak channel gets its own control.

| Leak channel | How it biases results | Control |
| --- | --- | --- |
| Repo state | Files edited by an earlier run | Fresh clone at a pinned commit per run, deleted afterwards |
| User-level config | CLAUDE.md, skills, hooks, MCP servers or settings carried between runs | Fresh container per run with an empty config directory; only the arm's own files installed |
| Project memory | Notes or CLAUDE.md content Claude wrote during a run | Fresh clone each run; assert no CLAUDE.md exists beyond the arm's own |
| Prompt cache | A warm cache makes later runs cheaper | Unique nonce at the start of each run's first message; arms interleaved in random order; cache writes and reads logged per run |
| Model or tool drift | A version change mid-battery | Pin the model ID with `--model`; record the Claude Code version; abort if either changes |
| Server load | Time-of-day variability | Randomized blocks, so every arm runs within the same time window |

The Claude Code system prompt and tool definitions are identical across arms, so they may stay cached between runs. That is acceptable because it affects every arm equally, but log it.

Container rules:

- One Docker image with pinned versions of Claude Code, Python and test tools. Each run is `docker run --rm`: clone, install arm, run task, collect, destroy.
- Inject credentials at runtime through an environment variable or a read-only mount. Never bake them into the image. Confirm the supported auth method for the installed Claude Code version.
- Use the skip-permissions mode only inside the throwaway container. Limit outbound network to the Anthropic API and package mirrors.

Don't use Claude Code subagents as the isolation mechanism. They share the session's files, hooks and settings, and run under a different system prompt from a normal session, so results wouldn't transfer.

## Pre-flight checks

All five must pass before the pilot starts. The billing check comes first because it decides whether the battery costs money.

1. **Billing.** Third-party tool docs report that headless `claude -p` runs may bill Agent SDK or API credits instead of the subscription window. This is unverified. Run one tiny headless task, then check the usage panel and any credit balance. If it bills credits, set a hard spend cap or drive interactive sessions instead.
2. **Token accounting.** Confirm per-run input, output, cache-read and cache-write tokens can be extracted from the JSON output or the session transcript. Cross-check one run against both sources.
3. **Version pin.** Record the Claude Code version and the model ID. Both stay fixed for the whole battery.
4. **Determinism probe.** Run the baseline on one task three times. If token totals vary by more than ±30%, raise the number of runs per arm.
5. **Baseline snapshot.** Collect a normal-usage receipt from the real machine before any lean skill is installed there, so a clean before picture exists.

## Test arms

Ten arms of our own plus three reference tools. Every arm except A7 differs from the baseline by exactly one change.

| ID | Arm | What gets installed | Layer |
| --- | --- | --- | --- |
| A0 | Baseline | Nothing: stock Claude Code | None |
| A1 | Lean code | Skill with a decision ladder: reuse, then standard library, then minimal new code, abstraction only when needed | Generated code |
| A2 | Concise prose | Skill: short explanations; code, commands and errors stay exact | Model output |
| A3 | Why-only comments | Rule: comment intent only; names and types carry the what | Generated code |
| A4 | Shorthand comments | Rule: compressed comments behind a marker symbol, tested fairly against A3 | Generated code |
| A5 | Shell trimming | Hook that cuts test, build and git output to failures plus a summary | Shell |
| A6a | Search first | Rule: search before reading whole files | Context |
| A6b | Subagent exploration | Rule: delegate codebase exploration to a subagent; count the subagent's own tokens, which are logged separately from the main thread | Context |
| A7 | Combined | Only the arms that won, together | All |
| A8 | Overnight brief | Project brief built in a separate earlier run and loaded at session start; build cost logged separately and spread across tasks | Context |
| R1 | Ponytail | Installed at a pinned commit | Reference |
| R2 | Caveman | Installed at a pinned commit | Reference |
| R3 | rtk | Installed at a pinned commit | Reference |

Arm rules:

- Keep each arm's instructions short and log their token size. Always-loaded text is a cost the arm has to earn back.
- Write our arms from scratch. Read the reference tools' licences and never copy their text into our arms.
- Install reference tools only inside the container, never on the real machine.

## Task suite

Six tasks on one pinned repo, each with an automated pass/fail check, chosen so every layer gets stressed at least once.

Use a small-to-mid Python repo (roughly 2,000 to 10,000 lines) with a real test suite. Either freeze one of your own repos at a commit or use a permissively licensed public repo. Put seeded bugs on a separate branch. Store each prompt verbatim in `tasks/`, identical for every arm.

| ID | Task | Stresses | Success check |
| --- | --- | --- | --- |
| T1 | Fix a seeded bug that has a failing test | Exploration, shell output | Target test passes; full suite passes |
| T2 | Add a feature that fetches public holidays from Nager.Date (listed in public-apis), tested against a mocked response | Code written | New tests pass with network disabled |
| T3 | Refactor one module for readability without changing behaviour | Code written, re-reading | Suite passes; diff touches only that module |
| T4 | Answer an architecture question, such as where a given input is validated | File reads | Answer names the right file and function, checked against a key |
| T5 | Write tests for an untested function | Code and shell | New tests pass; a seeded mutation of the function makes at least one fail |
| T6 | Two-step session: a bug fix, then a follow-up change | Context growth | Both checks pass |

## Metrics

The headline metric is cost-weighted tokens per successful task, relative to A0. Everything else explains where the savings come from.

| Metric | Source | Why it matters |
| --- | --- | --- |
| Input, output, cache-read and cache-write tokens | Run JSON output or transcript | Core cost |
| Cost-weighted tokens | Tokens × API price multipliers for the pinned model, stored in config | Proxy for quota cost; raw counts overstate cache reads |
| Success | Task check | Savings only count if success holds |
| Turns and tool calls | Transcript | Shows where savings come from |
| Files and bytes read | Read, Grep and Glob calls in the transcript | The file-read layer |
| Lines added and removed, comment token share | `git diff` plus a comment tokenizer | The code layer, and the A3 versus A4 comparison |
| Arm overhead | Token size of the arm's always-loaded text | The cost each arm must earn back |
| Window % change (optional) | Usage panel | The real meter; coarse, only useful for large runs |
| Wall time | Harness | Secondary |

On API pricing a cache read costs 0.05× base input on Opus 5.5 and Sonnet 5.5 (0.1× on most older models), a five-minute cache write 1.25×, a one-hour write 2×, and output 5×. Read the pinned model's prices from the published pricing table.

## Run protocol and statistics

An arm wins only if it cuts cost-weighted tokens with a confidence interval below 1.0 and keeps its success rate at or above the baseline's.

1. **Randomized blocks.** Each block runs every arm once on one task, in shuffled order. Repeat blocks until every arm and task pair has n runs.
2. **Run count.** Use n = 3 for the pilot and n = 5 for the full battery. Raise n if the determinism probe showed wide spread.
3. **Fresh state.** Every run gets a fresh container and its own nonce. No run reuses another run's files or transcript.
4. **Reporting.** Per arm, report the median cost-weighted tokens, the ratio to A0 with a bootstrap 95% confidence interval, and the success rate.
5. **Combined arm.** Build A7 only from arms that won, then measure it as its own arm. Never add up individual savings.
6. **Logging.** Keep the log append-only and never delete failed runs. Record infrastructure crashes separately from task failures.

## Harness and deliverables

The harness is a Python orchestrator that turns one isolated run into one results row, and can resume a battery after an interruption.

```
token-battery/
  SPEC.md                 this document
  docker/Dockerfile       pinned Claude Code, Python, test tools
  arms/A0 … A7/           each arm's skill, rules, hooks, settings
  tasks/T1 … T6.md        verbatim prompts
  checks/                 success-check script per task
  harness/run.py          one isolated run → one results row
  harness/battery.py      randomized blocks, resume after interruption
  harness/extract.py      tokens, tool calls, diff stats from transcripts
  results/runs.sqlite     append-only results
  analysis/report.ipynb   tables, confidence intervals, charts
```

Deliverables:

- [ ] Harness passing all pre-flight checks
- [ ] Pilot report reviewed before the full battery starts
- [ ] Full report with one headline chart: cost-weighted tokens per successful task by arm, with confidence intervals
- [ ] README section covering the method, the isolation controls and the known limitations

Run battery blocks in idle overnight windows, with a per-night cap on runs.

## Budget, pilot and stop rules

The pilot is 27 runs. The full battery is 300 runs for our own arms, plus 90 for the reference tools.

| Stage | Arms | Tasks | Runs each | Total runs |
| --- | --- | --- | --- | --- |
| Pilot | A0, A1, A5 | T1, T2, T4 | 3 | 27 |
| Full battery | A0 to A7 | T1 to T6 | 5 | 300 |
| Reference tools | R1 to R3 | T1 to T6 | 5 | 90 |

Stop rules:

- Billing check unresolved: don't start.
- Weekly usage passes 60%: pause until the reset, so normal work isn't starved.
- Claude Code or model version changes: stop, and start a new battery version.
- Infrastructure failures above 10% of runs: fix the harness before continuing.

Open questions:

- Does the subscription meter weigh cache reads the way API pricing does? The later calibration work answers this.
- Percentages differ between Pro and Max plans. Ratios between arms should transfer, but validate on a Pro account before publishing "$20 plan" numbers.
