# Master agent prompts (paste into your Claude Code terminal)

Start the terminal logged into the account you want to measure, with its token set, so the
master agent passes it on to every case it launches.

Windows (PowerShell):

```powershell
cd token-battery
claude setup-token                                   # once, on the measured account
$env:CLAUDE_CODE_OAUTH_TOKEN = "paste-the-token-here"
claude
```

macOS / Linux:

```bash
cd token-battery
claude setup-token
export CLAUDE_CODE_OAUTH_TOKEN=...
claude
```

## Launching a session

Replace `MODES` with one or more modes, run in order. Suggested progression:
`smoke smoke-build` → `pilot pilot-build` → `full full-build` → `confirm` (after filling `confirm_arms`).

```
You are the master agent for the token battery in this folder. Read README.md first.

Your job is to orchestrate, never to do the cases yourself. Each case must run as a separate,
context-free agent that receives only its task prompt and its arm's rules. The harness already
does this: it launches every case as its own `claude -p` process with an empty config directory.
Never run cases with your own Task/subagent tool: in-session subagents inherit this session's
plugins and settings, which would contaminate the comparison.

Rules: don't edit tasks/, build_suite/, arms/, target_repo/, config.json or harness/ unless the
self-test fails, and never open build_suite/reference/ or any hidden/ folder.

1. Run the self-test (fake claude, costs nothing, about 4 minutes): on Windows
   `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./run_overnight.ps1 -SelfTest`, otherwise
   `python3 harness/selftest.py`. If it fails,
   fix the harness, re-run until it passes, and list exactly what you changed.
2. For each mode in MODES, run `python harness/preflight.py --mode MODE` (use `python3` on macOS/Linux). It turns Ponytail
   off, proves an isolated case works, and checks agents can't read this folder. If a critical
   check fails, explain why and stop.
3. Launch everything in the background so it outlives your tool timeouts. On Windows:
   `nohup powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./run_overnight.ps1 MODES > results/launch.log 2>&1 &`
   On macOS/Linux: `nohup ./run_overnight.sh MODES > results/launch.log 2>&1 &`
4. Wait about three minutes, show me the last 20 lines of results/launch.log, confirm cases are
   completing, then stop. Don't poll all night.
```

Re-running the same launch after any stop (usage limit, max hours, crash) resumes where it left off.

## Checking in (optional, any time)

```
Show me the last 30 lines of the newest results/overnight-*.log and results/NIGHT_REPORT.md.
How many cases are done per mode, how long does a case take on average, and are there any flags?
Don't modify anything.
```

## In the morning

```
Read results/REPORT.md (plus REPORT_small.md and REPORT_build.md if present), results/NIGHT_REPORT.md
and results/preflight.json. Don't modify files. Report only what the data shows and say when
something is uncertain. In a few short paragraphs:
- do the method checks pass (A/A, placebo, canary)? If the A/A check fails, say nothing else is reliable yet;
- which arms win, cost more, or are inconclusive in each suite, and whether any hold across both;
- for builds: hidden acceptance pass rates per arm, and whether any token saving costs build quality;
- whether each winning arm's mechanism actually fired, and whether code quality held;
- flags (infra failures, permission denials, A5 marker missing, Ponytail leaks, noisy cells);
- what to run next.
```
