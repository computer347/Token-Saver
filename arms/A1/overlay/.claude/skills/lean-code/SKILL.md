---
name: lean-code
description: Use whenever writing or changing code. Keeps new code to the minimum the task needs.
---
Before writing code, go down this ladder and stop at the first step that works:

1. Reuse something that already exists in this project.
2. Use the Python standard library.
3. Write the smallest new code that fully solves the task.
4. Add an abstraction (class, helper, config) only if the task clearly needs it now.

Keep correctness, validation and error handling the task requires. Don't add features, options or files nobody asked for.
