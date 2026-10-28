from checklib import Check

c = Check()
answer = c.read("ANSWER.md")
c.require(answer is not None, "ANSWER.md exists")
c.require(answer is not None and "validation.py" in answer, "answer names validation.py")
c.require(answer is not None and "validate_amount" in answer, "answer names validate_amount")
c.require(c.changed() == ["ANSWER.md"], f"only ANSWER.md added (changed: {c.changed()})")
c.done()
