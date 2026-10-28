from checklib import Check

c = Check()
c.require(c.pytest("tests"), "visible test suite passes")
c.require(c.pytest("_hidden"), "hidden behaviour tests pass")
changed = c.changed()
c.require(changed == ["taskbench_app/reports.py"], f"only reports.py changed (changed: {changed})")
c.done()
