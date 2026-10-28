# Token battery — handoff (state as of 2026-10-26, 23:00)

Put this file in `C:\dev\tokens` and tell Claude Code: *"Read HANDOFF.md and README.md, then work through 'Open issues' in order."*

## What this project is

A benchmark harness that measures which token-saving rules ("arms") reduce Claude Code usage without hurting success or code quality.

- **Isolated cases:** every case is a separate `claude -p` process with its own temp workspace and an empty config directory (`CLAUDE_CONFIG_DIR`). It receives only the task prompt and the arm's rules.
- **Two suites:**
  - **small:** 8 edit tasks (T1–T8) on a ~420-line app in `target_repo/`.
  - **build:** task B1, which builds `homeledger` from an empty folder in a 4-step session. It is graded by 86 hidden acceptance tests in `build_suite/tasks/B1/hidden/`.
- **Design:** 3 wordings per task (v1–v3), balanced randomized blocks, parallel workers. Method checks include an A/A arm (A0b), a placebo (P1), a canary read test, and independent `confirm` replication.
- **Entry points:**
  - `run_overnight.ps1` (Windows) or `run_overnight.sh`, which run preflight, then the battery, then the report.
  - `harness/selftest.py` runs the whole pipeline with a fake `claude`.
- **Docs:** `README.md` (full design), `RUN_PROMPT.md` (master-agent prompts), `SPEC.md` (original design).

## Folder map

| Path | Purpose |
| --- | --- |
| `config.json` | Model (`claude-opus-5-5`), modes, suites, limits, cost weights, permission allow-list. `battery_version` is currently `v6`. |
| `harness/run.py` | One isolated case. Key functions: `make_env`, `build_cmd`, `task_prompts`, `run_one`. |
| `harness/workspace.py` | Builds the case workspace. Key functions: `prepare`, `expand_rules`, `harness_block_rules`, `write_run_settings`. |
| `harness/preflight.py` | Environment checks, smoke case, canary, and the per-mechanism permission diagnosis. |
| `harness/battery.py`, `harness/report.py` | Planner/runner and statistics. |
| `harness/fake_claude.py`, `harness/selftest*.py` | Self-test. The fake refuses to run outside an isolated workspace, as a guard. |
| `arms/<ID>/` | Each arm's `arm.json` plus an overlay copied into the workspace. |
| `tasks/`, `target_repo/` | Small suite. |
| `build_suite/` | Build suite: contract, prompts, hidden tests. `reference/` is for validating tests only and must never be shown to agents. |
| `results/` | `runs.jsonl` (append-only), reports, preflight JSON, logs. |

## Verified working on Mike's Windows machine (Claude Code 2.1.310)

- **Self-test:** `.\run_overnight.ps1 -SelfTest` passes, covering all checkers, the reference build (86/86), arms, and both pilots.
- **Preflight:** passes. Isolated headless runs return JSON, token accounting matches between the JSON output and the transcript, and the main conversation uses the 1-hour cache.
- **Permissions:** granting them via **`--allowedTools` / `--disallowedTools` / `--settings`** works (preflight "Permissions allow running tests unattended" = PASS).
- **Smoke battery (small suite):** 9 cases ran, at roughly 20–40 seconds each and 29k–47k weighted tokens each.

## Open issues (do these in order)

### 1. Workspace trust: project settings are ignored (diagnosed, fix not yet applied)

Claude Code printed this on stderr:

> Ignoring 87 permissions.allow entries from .claude/settings.json: this workspace has not been trusted. Run Claude Code interactively here once and accept the trust dialog, or set `projects["C:/Users/mikbs/AppData/Local/Temp/tb-.../work"].hasTrustDialogAccepted: true` in `<CLAUDE_CONFIG_DIR>\.claude.json`.

Permissions still work through the CLI flags. The risk is that other project-level files (skills, subagents in `.claude/agents`, hooks) may also be skipped in untrusted workspaces. That would silently disable arms A1, A5, A6b, A11 and A13.

**Fix:**

- **Mark the workspace trusted.** In `run.make_env` (which currently writes `{"hasCompletedOnboarding": true}` to `<config_dir>/.claude.json`), also write `{"projects": {"<work path>": {"hasTrustDialogAccepted": true}}}`. Use the path exactly as Claude Code spells it: forward slashes, drive letter as in the message (`C:/Users/...`). On Linux/macOS, use the plain absolute path.
- **Pass the workspace path through.** `make_env` doesn't receive the workspace path yet. Add a parameter and update every caller: `run.run_one`, `preflight.main` (smoke and canary), `preflight.diagnose_permissions`, and `build_brief.build`.
- **Verify:** the "Ignoring … permissions.allow entries" warning must disappear from preflight output.
- **Watch the canary.** Once project settings load, the plain `Read` allow rule applies everywhere, so the canary becomes a real test of the deny rules. It must still say PASS. If it fails, the deny-rule path format is wrong for Windows; see issue 2.

### 2. Build cases crash immediately (infra), cause not yet confirmed

`smoke-build` cases ended about 18 seconds after starting with:

> `infra: no JSON from claude (exit 0): …n): Write(//C:/dev/tokens/**) is not matched by file permission`

Only the last 400 characters of stderr were kept, so the real error message is cut off.

**Steps:**

1. **Capture the whole error.** In `run.py`, the error raised for "no JSON from claude" keeps `[-400:]` of stderr/stdout; raise that to about 4000 characters. Then reproduce a single case:
   `python harness/run.py A0 B1 --variant v1 --keep --no-log`
   The workspace is kept under `results/kept_runs/`.
2. **Leading hypothesis.** `Write(path)` is not a valid file-permission rule, because Claude Code's file rules use `Read(...)` and `Edit(...)`, and `Edit` covers all file-writing tools. In `workspace.harness_block_rules`, drop the `Write` entries and keep `Read` and `Edit`. To check quickly by hand:
   `claude -p "say hi" --disallowedTools "Write(//C:/dev/tokens/**)"`
3. **If smoke cases pass with the same deny list, find what differs for B1.** Compare: `extra_allow` in the build suite config (`Bash(mkdir *)`, `Bash(python3 -m homeledger.cli *)`), the `--max-turns 300` setting, and the much longer multi-line prompt with the contract inserted.
4. **Confirm the Windows path forms.** Settle which absolute-path spelling Claude Code accepts on Windows (`//C:/dev/tokens/**` vs `//c/dev/tokens/**`, both generated now), then keep only the valid one(s).

### 3. Small-suite smoke: 6 of 9 T1 cases failed. Investigate before the pilot

T1 is a simple seeded bug: a thousands separator in `taskbench_app/parsing.py`. A 6/9 failure rate is suspicious. Check `results/runs.jsonl` for the failed rows: which entry in `checks` failed, plus `steps[].permission_denials` and `steps[].stderr_tail`. Hypotheses to test:

- **Windows line endings (CRLF).** If `git status` reports test files as modified after the agent touched nothing, the check "test files unchanged" fails. Fix: run `git config core.autocrlf false` (and possibly `core.safecrlf false`) right after `git init` in `workspace.prepare`, before the base commit.
- **Edits or test runs denied.** This could come from the trust issue in issue 1 or from deny rules.
- **The agent didn't verify its fix.** If it couldn't run tests (e.g. `py` vs `python`), the fix may be unverified. Check `tool_calls` and whether tests were actually run.

If the failures are genuine model failures (the checks show the bug still present), that's a real result, but rule out harness causes first.

### 4. After fixes 1–3

1. **Bump `battery_version`** in `config.json` to `v7`, so the v6 smoke data never mixes with fixed runs.
2. **Run the self-test:** `.\run_overnight.ps1 -SelfTest`. It must say SELF-TEST PASSED.
3. **Rerun smoke:** `.\run_overnight.ps1 smoke smoke-build`. Expect no "Ignoring … entries" warning, all 3 builds producing JSON (taking minutes, not seconds), and T1 mostly succeeding.
4. **Check that mechanisms fired.** Run `python harness/report.py` and read the *"Did the technique actually happen?"* section. A5 should show trim markers, and A1 may show skill calls.
5. **Move to the pilot:** `.\run_overnight.ps1 pilot pilot-build`. Read *Method checks* first.

## Rules for whoever continues

- **Never run cases with in-session subagents.** The harness's separate `claude -p` processes are the isolation.
- **Never open or show agents** `build_suite/reference/` or any `hidden/` folder.
- **Any change to tasks, arms, permissions, model or Claude Code version means bumping `battery_version`.**
- **After any harness change, run the self-test.** It catches isolation breaks: the fake `claude` exits with code 3 if a case isn't isolated.
- **Windows specifics:** use PowerShell; set the token with `$env:CLAUDE_CODE_OAUTH_TOKEN = "..."` (per window); run `Get-ChildItem -Recurse | Unblock-File` after extracting new files.

## Runbook (Windows)

```powershell
cd C:\dev\tokens
$env:CLAUDE_CODE_OAUTH_TOKEN = "..."              # from `claude setup-token`, measured account
.\run_overnight.ps1 -SelfTest
.\run_overnight.ps1 smoke smoke-build
python harness/run.py A0 B1 --variant v1 --keep --no-log   # debug a single case
python harness/report.py                                   # rebuild reports from runs.jsonl
```
