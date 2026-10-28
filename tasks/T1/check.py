from checklib import Check

c = Check()
c.require(c.pytest("tests"), "visible test suite passes")
c.require(c.pytest("_hidden"), "hidden tests pass")
c.require(not c.changed(prefix="tests/"), "test files unchanged")
c.done()
