"""Turn Ponytail off in your normal Claude Code setup for the battery, restore it afterwards,
and vendor a pinned copy for the R1 reference arm.

Usage: python3 harness/ponytail.py disable|restore|vendor
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import RESULTS, VENDOR, claude_cmd, load_config, sh

STATE = RESULTS / "ponytail_state.json"
STRIP_ENV = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SSE_PORT", "CLAUDE_CONFIG_DIR")


def _env():
    return {k: v for k, v in os.environ.items() if k not in STRIP_ENV}


def disable(cfg=None) -> dict:
    cfg = cfg or load_config()
    listed = sh([*claude_cmd(cfg), "plugin", "list"], env=_env())
    text = (listed.stdout + listed.stderr).lower()
    state = {"found": "ponytail" in text, "disabled_by_harness": False, "detail": ""}
    if state["found"]:
        result = sh([*claude_cmd(cfg), "plugin", "disable", "ponytail"], env=_env())
        state["disabled_by_harness"] = result.returncode == 0
        state["detail"] = (result.stdout + result.stderr).strip()[-300:]
    RESULTS.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2))
    return state


def restore(cfg=None) -> None:
    cfg = cfg or load_config()
    if not STATE.exists():
        return
    state = json.loads(STATE.read_text())
    keep_off = os.environ.get("TB_KEEP_PONYTAIL_OFF") == "1" or not cfg.get("ponytail_restore_after_battery", True)
    if state.get("disabled_by_harness") and not keep_off:
        result = sh([*claude_cmd(cfg), "plugin", "enable", "ponytail"], env=_env())
        print("Ponytail re-enabled." if result.returncode == 0 else
              f"Could not re-enable Ponytail automatically; run: claude plugin enable ponytail\n{result.stderr[-200:]}")
        state["disabled_by_harness"] = False
        STATE.write_text(json.dumps(state, indent=2))


def vendor(cfg=None) -> dict:
    from vendor import vendor_plugin
    return vendor_plugin("ponytail", cfg)


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    if action == "disable":
        print(json.dumps(disable(), indent=2))
    elif action == "restore":
        restore()
    elif action == "vendor":
        print(json.dumps(vendor(), indent=2))
    else:
        sys.exit("usage: ponytail.py disable|restore|vendor")
