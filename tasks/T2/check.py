from checklib import Check

c = Check()
c.require(c.exists("taskbench_app/holidays.py"), "holidays module exists")
c.require(c.pytest("tests", offline=True), "visible suite (incl. agent's new tests) passes offline")
c.require(c.pytest("_hidden", offline=True), "hidden tests pass")
c.require(c.grep_new_tests("holiday"), "agent added tests for the feature")
c.done()
