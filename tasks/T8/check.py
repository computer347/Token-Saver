from checklib import Check

c = Check()
c.require(c.pytest("tests"), "visible test suite passes")
c.require(c.pytest("_hidden"), "hidden backwards-compatibility tests pass")
c.require(bool(c.changed(prefix="tests/")), "agent added a regression test")
c.done()
