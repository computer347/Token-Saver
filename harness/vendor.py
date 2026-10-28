"""Pin third-party plugins into vendor/ so arms can load them per run with --plugin-dir.

Two shapes are supported, matching how the real repos are laid out:
- the repo itself is a plugin (has .claude-plugin/plugin.json), e.g. Ponytail;
- the plugin is defined only by a marketplace entry ("strict": false), e.g. Anthropic's
  pyright-lsp, whose folder holds just a README and LICENSE. For those, a local plugin is built
  whose plugin.json carries the entry's component config (lspServers etc.) verbatim.
Every vendored plugin is checked with `claude plugin validate`.

Usage: python3 harness/vendor.py NAME
"""
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import VENDOR, claude_cmd, load_config, sh

COMPONENT_FIELDS = ("commands", "agents", "skills", "hooks", "mcpServers", "lspServers", "outputStyles")
STRIP = ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SSE_PORT", "CLAUDE_CONFIG_DIR")


def vendor_plugin(name: str, cfg: dict | None = None) -> dict:
    cfg = cfg or load_config()
    spec = cfg["plugins"][name]
    VENDOR.mkdir(exist_ok=True)
    info_file = VENDOR / f"{name}.json"
    repo = VENDOR / f"{name}_repo"
    if not repo.exists():
        cloned = sh(["git", "clone", "-q", "--filter=blob:none", spec["repo"], str(repo)])
        if cloned.returncode != 0:
            raise RuntimeError(f"git clone of {spec['repo']} failed: {cloned.stderr[-300:]}")
    previous = json.loads(info_file.read_text()).get("commit") if info_file.exists() else ""
    pinned = spec.get("pinned_commit") or previous
    if pinned:
        sh(["git", "checkout", "-q", pinned], cwd=repo, check=True)
    commit = sh(["git", "rev-parse", "HEAD"], cwd=repo).stdout.strip()

    if spec.get("from_marketplace_entry"):
        market = json.loads((repo / ".claude-plugin" / "marketplace.json").read_text())
        entry = next((p for p in market.get("plugins", []) if p.get("name") == name), None)
        if entry is None:
            raise RuntimeError(f"{name} not found in {spec['repo']} marketplace.json at {commit[:10]}")
        plugin_dir = VENDOR / f"{name}_plugin"
        shutil.rmtree(plugin_dir, ignore_errors=True)
        (plugin_dir / ".claude-plugin").mkdir(parents=True)
        manifest = {"name": name, "version": entry.get("version", "0.0.0"),
                    "description": entry.get("description", "")}
        manifest.update({k: entry[k] for k in COMPONENT_FIELDS if k in entry})
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text(json.dumps(manifest, indent=2))
    else:
        plugin_dir = repo / spec.get("subdir", "")
        if not (plugin_dir / ".claude-plugin" / "plugin.json").exists():
            raise RuntimeError(f"{plugin_dir} has no .claude-plugin/plugin.json")

    env = {k: v for k, v in os.environ.items() if k not in STRIP}
    check = sh([*claude_cmd(cfg), "plugin", "validate", str(plugin_dir)], env=env)
    info = {"name": name, "repo": spec["repo"], "commit": commit, "plugin_dir": str(plugin_dir),
            "validated": check.returncode == 0, "validate_output": (check.stdout + check.stderr).strip()[-600:]}
    info_file.write_text(json.dumps(info, indent=2))
    return info


if __name__ == "__main__":
    print(json.dumps(vendor_plugin(sys.argv[1]), indent=2))
