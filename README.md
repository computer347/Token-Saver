# Token battery

Measures which token-saving rules actually reduce Claude Code usage, without lowering success or code quality. There are two kinds of work. **Small edits** are bug fixes and features on an existing app. **Full builds** have Claude Code build a whole project from an empty folder over a multi-step session, graded by hidden acceptance tests. The only thing that differs between cases is the rule set ("arm") being tested.

`SPEC.md` is the original design. This README describes what the harness does now.

## Quickstart

**Windows (PowerShell):**

```powershell
cd token-battery
py -m pip install pytest                    # or: python -m pip install pytest
npm install -g pyright                      # needed for arm A10 (code intelligence)
.\run_overnight.ps1 -SelfTest               # fake claude, costs nothing, ~4 minutes, should say PASSED

claude setup-token                          # once, while logged into the account you want to measure
$env:CLAUDE_CODE_OAUTH_TOKEN = "paste-the-token-here"

.\run_overnight.ps1 smoke smoke-build       # first: proves everything works end to end
```

If PowerShell says running scripts is disabled, use `powershell -ExecutionPolicy Bypass -File .\run_overnight.ps1 smoke smoke-build`. The `$env:` line only lasts for that window, so set it again in any new window. You also need Git for Windows (Claude Code requires it anyway) and Python 3.11+ on PATH. The script keeps the PC awake while it runs.

**macOS / Linux:**

```bash
unzip token-battery.zip && cd token-battery
python3 -m pip install pytest            # required
npm install -g pyright                   # needed for arm A10 (code intelligence)
python3 -m pip install ruff              # optional: lint counts in the quality tables
python3 harness/selftest.py              # fake claude, costs nothing, ~4 minutes, should say PASSED

claude setup-token                       # once, while logged into the account you want to measure
export CLAUDE_CODE_OAUTH_TOKEN=...

./run_overnight.sh smoke smoke-build     # first: proves everything works end to end
```

To have a master agent run it, paste the prompts from `RUN_PROMPT.md` into your Claude Code terminal.

## How cases are run

A master agent (your Claude Code session) launches the harness. The harness runs every case as its own `claude -p` process that receives **only** its task prompt and its arm's rules:

- **Fresh workspace:** a new copy of the starting repo for each case. For builds, that's an empty folder.
- **Empty config:** `CLAUDE_CONFIG_DIR` points at a new, empty directory, so the case gets no history, memory, CLAUDE.md, plugins, skills, hooks or MCP servers from your setup.
- **No shared cache:** each case's first message carries a unique nonce.
- **Clean environment:** variables that silently change behaviour (effort level, model overrides, thinking budget, `ANTHROPIC_API_KEY`) are stripped. Preflight lists any it found in your shell.
- **No peeking:** agents are denied read access to this folder, which holds the hidden tests, the reference solution and other results. Preflight proves it with a canary: it plants a secret file here and checks that a fresh agent can't read it.
- **Ponytail off:** Ponytail is turned off in your normal setup before cases start and restored afterwards.

Claude Code's built-in in-session subagents are deliberately not used for cases. They inherit the parent session's plugins and settings, so rules would leak between cases.

## The two suites

**small:** a ~420-line ledger app with eight edit tasks (T1–T8): bug fixes, a feature against a mocked API, a refactor, a code question, test writing (mutation-checked), a two-step session, a multi-file feature, and debugging from a traceback. Success means every hidden check passes.

**build:** task B1. Claude Code builds `homeledger`, a household-finance toolkit, from an empty folder in a 4-step session:

1. Core: money, dates, models, validation.
2. Storage: JSON and SQLite stores with schema migration.
3. Features: CSV import with duplicate detection, a rules engine, budgets with rollover, a search language.
4. Reports and a JSON-capable CLI.

Each step's prompt embeds a fixed interface contract (`build_suite/tasks/B1/contract/`), identical in all three wordings, so grading is fair. **86 hidden acceptance tests** grade the result. The report shows the pass rate per run and per step; a run counts as a success at 90% or more (`success_threshold`).

`build_suite/reference/` holds a reference implementation used only to prove the hidden tests are correct and achievable. The self-test checks it passes all 86, and that seeded bugs in it are caught. Agents never see it.

## Wordings and repetition

Every task comes in three wordings, all stating the same requirements:

- **v1:** a precise spec.
- **v2:** casual and terse.
- **v3:** goal or user-story style.

Each arm runs every task in every wording, several times, in balanced randomized blocks. A block is one task × wording with every arm once, in shuffled order. So results are averages over phrasing and run-to-run noise, not one-off outcomes.

## Modes

| Mode | What runs | Cases |
| --- | --- | --- |
| `smoke` | A0, A1, A5 on T1 | 9 |
| `smoke-build` | A0 builds B1 | 3 |
| `pilot` | A0, A0b, P1, A1, A5 on T1–T8, 2 reps | 240 |
| `pilot-build` | A0, A0b, P1 build B1, 2 reps | 18 |
| `full` | all 17 arms on T1–T8, 3 reps | 1,224 |
| `full-build` | the 14 arms that apply to builds, 3 reps | 126 |
| `refs` / `refs-build` | A0 vs Ponytail | 144 / 18 |
| `confirm` | A0, A0b + `confirm_arms` on both suites, 4 reps | depends |

Chain modes: `./run_overnight.sh full full-build`. Re-run the same command to resume after any stop.

On time, small cases take a few minutes each. A 4-step build is far longer, probably 20–60 minutes per case, so `full-build` is likely more than a day at 3 workers. The night report shows the real pace after the first session. Raise `workers` in `config.json` to go faster (3–4 is sensible for one account).

## Arms

| ID | Technique | Applies to | Evidence the report checks |
| --- | --- | --- | --- |
| A0 | Baseline | both | — |
| A0b | **A/A check**: exact copy of A0 | both | must equal A0 |
| P1 | **Placebo**: CLAUDE.md of similar length, no instructions | both | instruction arms compared against it |
| A1 | Lean-code skill | both | skill tool calls (hint) |
| A2 | Concise prose (CLAUDE.md) | both | — |
| A3 | Why-only comments | both | comment share |
| A4 | Shorthand comments (expected negative control) | both | comment share |
| A5 | Shell-output trimming hook | both | trim marker in tool output |
| A6a | Search before reading | both | files and bytes read |
| A6b | Subagent exploration | both | subagent use |
| A8 | Overnight brief | small | BRIEF.md opened |
| A9 / A9m | `--effort low` / `medium` | both | configured only |
| A10 | Official `pyright-lsp`, pinned and validated | both | LSP tool calls |
| A11 | Repo recipe skill | small | skill tool calls (hint) |
| A12 | Generator scripts | small | scaffold.py runs |
| A13 | Haiku-pinned explorer subagent | both | Haiku in subagent transcripts |
| A7 | Combined winners (`a7_components`) | both | — |
| R1 | Ponytail reference, pinned | both | — |

A8, A11 and A12 only make sense on an existing codebase, so builds skip them.

## Reading the report

`results/REPORT.md` opens with **Does each effect hold across suites?**: each arm's ratio against A0, with its interval, for small edits and for builds side by side. Then comes one section per suite (also saved as `REPORT_small.md` and `REPORT_build.md`):

1. **Method checks:** the A/A check, the placebo, and how many intervals could exclude 1.0 by chance.
2. **Headline:** cost-weighted tokens per successful case relative to A0, with a bootstrap 95% interval. A win requires the whole interval to be below 1.0 and success at least the baseline's. With fewer than 3 runs per task, the report says so instead of guessing.
3. **Hidden acceptance tests (builds):** mean pass rate with an interval, plus the rate per build step, whether the agent's own tests pass, and lines written.
4. **Robustness:** results by task and by wording, comparison against the placebo, and whether each mechanism actually fired.
5. **Code quality, where the tokens go, and a scope statement** generated from the data.

Then replicate winners with `confirm` before treating them as established.

## Known limits

- **One build project.** B1 measures building to a fixed spec, not open-ended design. Other projects, languages and models are untested.
- **Cost is a proxy.** Cost weights use API price ratios; how Pro and Max limits weigh each token type is not published.
- **Some evidence is indirect.** Skill evidence is a hint, effort is configured but not verified per run, and A11's hand-written recipes cost human time that isn't counted.
- **Windows support is tested on PowerShell 7 under Linux.** The PowerShell runner, the UTF-8 handling and the npm-wrapper bypass were exercised there, but not on a real Windows machine. Run `.\run_overnight.ps1 -SelfTest`, then the smoke modes, before anything long; preflight's canary confirms the read-block on your machine.
- **A5 trims Bash only.** On Windows, commands Claude runs through the PowerShell tool aren't trimmed, because the rewrite is bash syntax. The "did it happen" table shows how often A5 actually fired.
- **No Docker.** Isolation uses a fresh config directory and temp workspace instead. Runs use `--permission-mode acceptEdits` with an allow-list, and web tools are denied.

## Stop rules and troubleshooting

- **When it stops.** It stops at the usage limit, after `max_hours`, above 10% infrastructure failures, or if the Claude Code version or model changes. Resume by re-running.
- **Changing the experiment.** Changing tasks, arms, permissions, the model or the Claude Code version means bumping `battery_version`.
- **Permission denials.** Command rules use the current `Bash(cmd *)` syntax. Every case automatically gets PowerShell twins and `python`/`py` variants. Each case receives its permissions three ways at once: `--allowedTools`/`--disallowedTools`, an explicit `--settings` file stored outside the workspace, and the workspace's `.claude/settings.json`. If preflight still sees a denial, it tests each way separately and prints which one works on your machine, along with anything Claude Code printed as a warning. If preflight still reports denials, the night report names the command; add it to `config.json` → `permissions.allow` and bump `battery_version`.
- **Token not set.** Isolated runs can't see your login. Run `claude setup-token` and export the token in the same terminal.
- **Your normal Claude Code asks you to log in again.** Some versions were reported to clear the macOS Keychain login when `CLAUDE_CODE_OAUTH_TOKEN` is set. Run `/login` once.
