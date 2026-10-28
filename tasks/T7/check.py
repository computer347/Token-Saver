from checklib import Check

c = Check()
c.require(c.pytest("tests"), "visible test suite passes")
c.require(c.pytest("_hidden"), "hidden import tests pass")
c.require(c.grep_new_tests('"import"') or c.grep_new_tests("'import'"), "agent added tests that call the import command")
c.done()
