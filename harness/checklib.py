"""Helpers for task checks. Each tasks/Tn/check.py runs with cwd = the run's workspace."""
import json
import os
import subprocess
import sys
from pathlib import Path

IGNORED = ("_hidden/", "__pycache__", ".pytest_cache", ".claude/", "ledger.json", "_junit.xml")
HARNESS_INI = Path(__file__).resolve().parent / "hidden_support" / "pytest.ini"


def isolated_pytest_args(target):
    """Run the hidden suite with the harness's own pytest config, so nothing the agent wrote (pytest.ini,
    pyproject/setup.cfg/tox.ini sections, conftest.py, addopts) changes how it runs. PYTHONPATH covers imports."""
    return ["-c", str(HARNESS_INI), "--rootdir", target, "-o", "addopts=", "--noconftest"]


class Check:
    def __init__(self):
        self.work = Path.cwd()
        self.results = []
        self.metrics = {}

    def metric(self, name, value):
        self.metrics[name] = value

    def require(self, ok, label):
        self.results.append({"check": label, "ok": bool(ok)})

    def done(self):
        print(json.dumps({"success": all(r["ok"] for r in self.results), "checks": self.results,
                          "metrics": self.metrics}))
        sys.exit(0)

    def pytest(self, target, offline=False):
        if not (self.work / target).exists():
            return False
        env = {k: v for k, v in os.environ.items() if k != "PYTEST_ADDOPTS"}
        env["PYTHONPATH"] = os.pathsep.join([str(self.work), str(self.work / "_hidden")])
        args = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target]
        if target.startswith("_hidden"):
            args += isolated_pytest_args(target)
        if offline:
            args += ["-p", "netblock"]
        try:
            proc = subprocess.run(args, cwd=self.work, env=env, capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            return False  # a hanging suite fails its check instead of crashing check.py
        return proc.returncode == 0

    def changed(self, prefix=None):
        out = subprocess.run(["git", "status", "--porcelain=v1", "-uall"], cwd=self.work,
                             capture_output=True, text=True).stdout
        paths = []
        for line in out.splitlines():
            path = line[3:].split(" -> ")[-1].strip().strip('"')
            if any(token in path for token in IGNORED) or path.endswith(".pyc"):
                continue
            if prefix is None or path.startswith(prefix):
                paths.append(path)
        return sorted(paths)

    def exists(self, rel):
        return (self.work / rel).exists()

    def read(self, rel):
        path = self.work / rel
        return path.read_text(encoding="utf-8", errors="replace") if path.exists() else None

    def count_tests(self, rel):
        text = self.read(rel) or ""
        return text.count("def test_")

    def grep_new_tests(self, word):
        for rel in self.changed(prefix="tests/"):
            text = (self.read(rel) or "").lower()
            if word.lower() in text:
                return True
        return False

    def mutant_killed(self, rel, old, new, test_target):
        path = self.work / rel
        original = path.read_text()
        if old not in original:
            return False
        try:
            path.write_text(original.replace(old, new))
            env = {**os.environ, "PYTHONPATH": str(self.work)}
            proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", test_target],
                                  cwd=self.work, env=env, capture_output=True, text=True, timeout=300)
            return proc.returncode == 1  # tests ran and at least one failed
        finally:
            path.write_text(original)

    def acceptance(self, target="_hidden"):
        """Run the hidden acceptance tests; record the overall pass rate and one per test file.

        The denominator is fixed (TB_ACCEPTANCE_TOTAL): tests that are skipped, missing or fail to collect
        count as failed, so an agent can't raise its rate by breaking or skipping tests."""
        import xml.etree.ElementTree as ET
        expected = int(os.environ.get("TB_ACCEPTANCE_TOTAL", "0") or 0)
        report = self.work / "_junit.xml"
        env = {k: v for k, v in os.environ.items() if k != "PYTEST_ADDOPTS"}
        env["PYTHONPATH"] = os.pathsep.join([str(self.work), str(self.work / target)])
        try:
            subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target,
                            *isolated_pytest_args(target), f"--junitxml={report}"],
                           cwd=self.work, env=env, capture_output=True, text=True, timeout=900)
        except subprocess.TimeoutExpired:
            self.metric("acceptance_timeout", True)
        if not report.exists():
            self.metric("pass_rate", 0.0)
            self.metric("acceptance_passed", 0)
            self.metric("acceptance_total", expected)
            return 0.0
        passed = total = 0
        per_file = {}
        for case in ET.parse(report).getroot().iter("testcase"):
            name = (case.get("classname") or "").split(".")[-1] or "unknown"
            failed = any(child.tag in ("failure", "error") for child in case)
            skipped = any(child.tag == "skipped" for child in case)
            ok = not failed and not skipped
            total += 1
            passed += 1 if ok else 0
            f = per_file.setdefault(name, [0, 0])
            f[0] += 1 if ok else 0
            f[1] += 1
        report.unlink()
        self.metric("acceptance_collected", total)
        total = max(total, expected)
        rate = passed / total if total else 0.0
        self.metric("pass_rate", round(rate, 4))
        self.metric("acceptance_passed", passed)
        self.metric("acceptance_total", total)
        self.metric("step_pass_rates", {k: round(p / t, 4) for k, (p, t) in sorted(per_file.items())})
        return rate

    def count_lines(self, rel):
        root = self.work / rel
        files = [root] if root.is_file() else list(root.rglob("*.py")) if root.exists() else []
        return sum(len(f.read_text(errors="replace").splitlines()) for f in files if "__pycache__" not in f.parts)
