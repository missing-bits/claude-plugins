---
description: Review the current diff (or named files) against the Python coding standards
---

Review Python code against the python-standards skills.

1. Load the `python-code-review` skill and follow it end to end.
2. Scope: `$ARGUMENTS` when given (named files); otherwise the current
   diff — staged plus unstaged changes, or, on a clean tree, the diff of
   the current branch against its base.
3. Python files only (`*.py`, `pyproject.toml`); note out-of-domain
   files in the report Summary as out of scope.
4. Write the review report per the skill's report contract and reply
   as the python-code-review skill specifies (report path, severity
   summary, candidate gaps and offers).
