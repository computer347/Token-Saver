from checklib import Check

c = Check()
c.require(c.exists("tests/test_monthly_summary.py"), "test file exists")
c.require(c.count_tests("tests/test_monthly_summary.py") >= 3, "at least 3 test functions")
c.require(not c.changed(prefix="taskbench_app/"), "source code unchanged")
c.require(c.pytest("tests"), "whole visible suite passes")
killed = c.mutant_killed(
    "taskbench_app/reports.py",
    'months[key]["net"] = round_money(income - expense)',
    'months[key]["net"] = round_money(income + expense)',
    "tests/test_monthly_summary.py",
)
c.require(killed, "new tests catch a seeded bug in the net calculation")
c.done()
