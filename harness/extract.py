"""Pull token usage, tool calls and diff stats out of a finished run."""
import json
import re
from collections import Counter
from pathlib import Path

from common import sh


def parse_result_json(stdout: str) -> dict:
    stdout = (stdout or "").strip()
    try:
        data = json.loads(stdout)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        for line in reversed(stdout.splitlines()):
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                continue
    return {}


def _usage_fields(u: dict) -> dict:
    cc = u.get("cache_creation") or {}
    return {
        "input": u.get("input_tokens", 0) or 0,
        "output": u.get("output_tokens", 0) or 0,
        "cache_read": u.get("cache_read_input_tokens", 0) or 0,
        "cache_write": u.get("cache_creation_input_tokens", 0) or 0,
        "cache_write_1h": cc.get("ephemeral_1h_input_tokens"),
        "cache_write_5m": cc.get("ephemeral_5m_input_tokens"),
    }


def usage_from_result(res: dict) -> dict:
    return _usage_fields(res.get("usage") or {})


def add_usage(a: dict, b: dict) -> dict:
    out = {}
    for key in set(a) | set(b):
        va, vb = a.get(key), b.get(key)
        out[key] = None if va is None and vb is None else (va or 0) + (vb or 0)
    return out


def weighted(tokens: dict, w: dict) -> float:
    w1h, w5m = tokens.get("cache_write_1h"), tokens.get("cache_write_5m")
    if w1h is None and w5m is None:
        writes = tokens.get("cache_write", 0) * w["cache_write_unknown"]
    else:
        writes = (w1h or 0) * w["cache_write_1h"] + (w5m or 0) * w["cache_write_5m"]
    return (tokens.get("input", 0) * w["input"] + tokens.get("output", 0) * w["output"]
            + tokens.get("cache_read", 0) * w["cache_read"] + writes)


def _text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(_text_of(c.get("text", c.get("content", ""))) if isinstance(c, dict) else str(c)
                         for c in content)
    return str(content or "")


def transcript_stats(config_dir: Path) -> dict:
    """Sum usage over every transcript (main thread and subagents) in an isolated config dir."""
    files = sorted((config_dir / "projects").rglob("*.jsonl")) if (config_dir / "projects").exists() else []
    by_message = {}
    tools = Counter()
    files_read = set()
    result_bytes = 0
    trim_markers = 0
    ponytail = 0
    models_main, models_side = set(), set()
    scaffold_calls = 0
    brief_reads = 0
    for path in files:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            ponytail += line.lower().count("ponytail")
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = entry.get("message") or {}
            if entry.get("type") == "assistant":
                side_entry = bool(entry.get("isSidechain")) or "subagent" in str(path)
                if msg.get("model"):
                    (models_side if side_entry else models_main).add(msg["model"])
                key = msg.get("id") or f"{path.name}:{len(by_message)}"
                if msg.get("usage"):
                    by_message[key] = (_usage_fields(msg["usage"]), bool(entry.get("isSidechain")) or "subagent" in str(path))
                for block in msg.get("content") or []:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        tools[block.get("name", "?")] += 1
                        if block.get("name") == "Read":
                            files_read.add(str((block.get("input") or {}).get("file_path", "")))
                        if block.get("name") == "Read" and str((block.get("input") or {}).get("file_path", "")).endswith("BRIEF.md"):
                            brief_reads += 1
                        if block.get("name") == "Bash" and "scaffold.py" in str((block.get("input") or {}).get("command", "")):
                            scaffold_calls += 1
            elif entry.get("type") == "user":
                for block in msg.get("content") or [] if isinstance(msg.get("content"), list) else []:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        text = _text_of(block.get("content"))
                        result_bytes += len(text.encode("utf-8"))
                        trim_markers += text.count("[trimmed by A5")
    main = {}
    side = {}
    for usage, is_side in by_message.values():
        if is_side:
            side = add_usage(side, usage)
        else:
            main = add_usage(main, usage)
    return {
        "transcript_files": len(files),
        "tokens_main": main,
        "tokens_subagents": side,
        "tokens_total": add_usage(main, side),
        "tool_calls": dict(tools),
        "tool_calls_total": sum(tools.values()),
        "files_read": len(files_read),
        "tool_result_bytes": result_bytes,
        "a5_trim_markers": trim_markers,
        "ponytail_mentions": ponytail,
        "models_main": sorted(models_main),
        "models_subagents": sorted(models_side),
        "lsp_calls": tools.get("LSP", 0),
        "skill_calls": tools.get("Skill", 0),
        "subagent_calls": tools.get("Task", 0) + tools.get("Agent", 0),
        "scaffold_calls": scaffold_calls,
        "brief_reads": brief_reads,
    }


COMMENT = re.compile(r"^\s*#")


def diff_stats(work: Path) -> dict:
    sh(["git", "add", "-A"], cwd=work)
    numstat = sh(["git", "diff", "--cached", "--numstat", "HEAD", "--", ".", ":(exclude)_hidden"], cwd=work).stdout
    added = removed = 0
    for line in numstat.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            added, removed = added + int(parts[0]), removed + int(parts[1])
    patch = sh(["git", "diff", "--cached", "-U0", "HEAD", "--", "*.py", ":(exclude)_hidden"], cwd=work).stdout
    code_chars = comment_chars = 0
    for line in patch.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            body = line[1:]
            if COMMENT.match(body):
                comment_chars += len(body.strip())
            else:
                code_chars += len(body.strip())
    total = code_chars + comment_chars
    return {"lines_added": added, "lines_removed": removed,
            "comment_char_share": round(comment_chars / total, 3) if total else 0.0}
