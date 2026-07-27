---
description: Review the current diff (or named files) against the Salesforce coding standards
---

Review Salesforce code and metadata against the salesforce-standards
skills by dispatching the reviewer agent in the background — the
review must never block this session.

1. Resolve the scope: `$ARGUMENTS` when given (named files);
   otherwise the current diff — staged plus unstaged changes, or, on
   a clean tree, the diff of the current branch against its base.
2. Pre-dispatch first-create check, gated on the contract probe:
   check `<project>/.claude/rules/working-process/review-reports.md`,
   then `$HOME/.claude/rules/working-process/review-reports.md` —
   first hit wins (paths owned by the review-reports contract;
   restated here so the command is self-contained). No contract found
   (Standalone install) → skip this step entirely. Contract found and
   `docs/code-review/` carries no decision — no `.gitignore` of
   exactly `*`, no git-tracked file under it, and no
   explicit project instruction declaring the mode (signal list owned
   by the process-artifacts rule) — ask the developer now: ignored or
   tracked mode.
3. Dispatch the `salesforce-code-reviewer` agent in the BACKGROUND
   with the resolved scope. Salesforce files only, per the skill's
   run scope; the agent notes out-of-domain files in the report
   Summary as out of scope and writes the one report itself
   (`mode: agent` under the installed contract). The dispatch prompt
   carries the scope, the prior report's runid for a rerun
   (`rerun-of`), and the directory-mode decision from step 2 — never
   report-shaping instructions of its own: aggregation and counting
   policy, layout, and severity policy belong to the contract and
   the reviewer's skill, and a whole-project scope is no exception.
4. Tell the developer: the review is running in the background; the
   summary arrives as a task notification, not inline; progress via
   `/tasks`; the report will land under `docs/code-review/`.
5. When the run's notification arrives, relay its reply to the
   developer: report path, findings by severity, and the
   candidate-gap offers verbatim.
