from checklib import Check

c = Check()
c.require(c.pytest("tests"), "visible test suite passes")
c.require(c.pytest("_hidden"), "hidden tests pass (date fix and --json)")
c.require(bool(c.changed(prefix="tests/")), "agent added or updated tests")
c.done()
