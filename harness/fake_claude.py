#!/usr/bin/env python3
"""Stand-in for the `claude` CLI so the harness can be tested without spending tokens.

TB_FAKE_SOLVE=1 applies the reference solution; otherwise the fake does nothing (the run should fail its check).
"""
import hashlib
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import selftest_solutions

args = sys.argv[1:]
if "--version" in args:
    print("9.9.9 (fake Claude Code)")
    sys.exit(0)
if args and args[0] == "plugin":
    print("No plugins installed")
    sys.exit(0)

# Isolation guard: a real case must run inside its own workspace with its own empty config directory.
# If the harness ever launches a case elsewhere, fail loudly so the self-test catches it.
if Path.cwd().name not in ("work", "probe-work") or not os.environ.get("CLAUDE_CONFIG_DIR"):
    sys.stderr.write(f"fake claude: NOT ISOLATED (cwd={Path.cwd()}, CLAUDE_CONFIG_DIR={os.environ.get('CLAUDE_CONFIG_DIR')})\n")
    sys.exit(3)

prompt = args[args.index("-p") + 1] if "-p" in args else ""
task, step = os.environ.get("TB_TASK", ""), int(os.environ.get("TB_STEP", "0"))
work = Path.cwd()
result = "done"
if "number of tests that passed" in prompt:
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], capture_output=True, text=True).stdout
    result = out.strip().splitlines()[-1].split()[0] if out.strip() else "0"
elif task == "BRIEF":
    (work / "BRIEF.md").write_text("# Brief\n\n- validation.py: validate_amount, validate_date\n- reports.py: monthly_summary\n")
elif os.environ.get("TB_FAKE_SOLVE") == "1":
    selftest_solutions.apply(task, step, work)

seed = int(hashlib.sha256(prompt.encode()).hexdigest()[:6], 16)
scale = 0.85 + (seed % 30) / 100 + (0.15 if (work / "CLAUDE.md").exists() else 0)
usage = {"input_tokens": int(40 * scale), "output_tokens": int(900 * scale),
         "cache_read_input_tokens": int(150000 * scale), "cache_creation_input_tokens": int(22000 * scale),
         "cache_creation": {"ephemeral_1h_input_tokens": int(22000 * scale), "ephemeral_5m_input_tokens": 0}}
config = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude-fake")))
transcript = config / "projects" / "fake-project" / f"{uuid.uuid4()}.jsonl"
transcript.parent.mkdir(parents=True, exist_ok=True)
entries = [
    {"type": "assistant", "isSidechain": False, "message": {"id": f"msg_{uuid.uuid4().hex[:8]}", "usage": usage,
     "model": "fake-main-model",
     "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": str(work / "README.md")}}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "file contents " * 50}]}},
]
transcript.write_text("\n".join(json.dumps(e) for e in entries) + "\n")
if os.environ.get("TB_FAKE_HANG") == "1":  # tokens are spent, then the run never finishes
    import time
    time.sleep(600)
if os.environ.get("TB_FAKE_ERROR"):  # the CLI's shape for a usage limit or API error
    print(json.dumps({"type": "result", "subtype": "success", "is_error": True, "result": os.environ["TB_FAKE_ERROR"],
                      "session_id": str(uuid.uuid4()), "total_cost_usd": 0, "num_turns": 1, "usage": usage}))
    sys.exit(1)
print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": result,
                  "session_id": str(uuid.uuid4()), "total_cost_usd": round(0.12 * scale, 4), "num_turns": 6,
                  "usage": usage,
                  "permission_denials": ([{"tool_name": "Bash", "tool_input": {"command": "python -m pytest -q"}}]
                                         if os.environ.get("TB_FAKE_DENY") == "1" else [])}))
