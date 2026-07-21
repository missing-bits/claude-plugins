---
description: Review the current diff (or named files) against the Salesforce coding standards
---

Review Salesforce code and metadata against the salesforce-standards
skills.

1. Load the `salesforce-code-review` skill and follow it end to end.
2. Scope: `$ARGUMENTS` when given (named files); otherwise the current
   diff — staged plus unstaged changes, or, on a clean tree, the diff
   of the current branch against its base.
3. Salesforce files only, per the skill's run scope; note
   out-of-domain files in the report Summary as out of scope.
4. Write the review report per the skill's report contract and reply
   with the report path and findings by severity.
