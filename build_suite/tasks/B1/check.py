import os

from checklib import Check

c = Check()
rate = c.acceptance()
threshold = float(os.environ.get("TB_SUCCESS_THRESHOLD", "0.9"))
c.require(rate >= threshold, f"hidden acceptance pass rate {rate:.0%} (threshold {threshold:.0%})")
c.metric("own_tests_pass", c.pytest("tests"))
c.metric("package_lines", c.count_lines("homeledger"))
c.metric("test_lines", c.count_lines("tests"))
c.done()
