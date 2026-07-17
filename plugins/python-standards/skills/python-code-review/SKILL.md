---
name: python-code-review
description: Use when auditing existing Python code against the python-standards skills — invoked by the /python-review command or the python-code-reviewer agent.
---

# Python code review

Audit Python code against the standards skills of this plugin and write
one Review report per run.

## Run scope

Review Python files only (`*.py` and `pyproject.toml`). Files outside
the domain that fall inside the requested scope are NOT reviewed — list
them in the report's Summary as out of scope.

## Procedure

1. Determine the scope: the current diff by default, or the files named
   by the caller.
2. Load the standards skills relevant to the code under review:
   python-code-style always; python-project-layout, python-typing,
   python-testing, python-cli, python-web-api as the content demands.
3. Grade every finding:
   - **Critical** — a defect that corrupts data, breaks security, or
     crashes the happy path.
   - **Important** — violates a standard in a way that forces rework or
     hides bugs.
   - **Minor** — naming, style, documentation.
   Cite the standard for each finding (`standard: <skill>, rule: <id>`
   where the skill defines rule ids).
4. Write the Review report (next section).
5. Reply with the report path and the findings grouped by severity; a
   zero-findings run still writes the report and states the result.

## Report contract

Run the Contract probe FIRST — do not assume the shared rule is in
context: check, in order,
`<project>/.claude/rules/working-process/review-reports.md`, then
`$HOME/.claude/rules/working-process/review-reports.md`; the first file
found wins. When the Contract probe succeeds, read that file and follow
it fully
— **the installed working-process review-reports rule supersedes the
inline fallback below.**

## Inline fallback (Standalone install)

When the Contract probe finds nothing, this minimal contract applies —
a strict subset of the shared review-reports contract, never a
different shape:

- **Location**: `<project-root>/docs/code-review/`; create the
  directory if absent (the first-create mode question belongs to
  working-process's process-artifacts rule and is absent in a
  Standalone install).
- **Filename**: `<YYYY-MM-DD-HHMMSS>-<scope-slug>-<runid>.md`,
  generated with this exact command (byte-identical to the shared
  contract's; the first 17 output characters are the timestamp, the
  final 8 hex characters the runid):

  ```sh
  printf '%s-%s\n' "$(date +%Y-%m-%d-%H%M%S)" "$(head -c 4 /dev/urandom | od -An -tx1 | tr -d ' \n')"
  ```

- **Frontmatter**: `ticket` (from context or branch, else `none`; never
  block on a question), `standards: python-standards`,
  `findings: { critical: N, important: N, minor: N }` — the counts MUST
  equal the body.
- **Body**: a Summary section (scope reviewed, out-of-scope files,
  headline counts), then per-file sections with Critical → Important →
  Minor subsections, line-ascending within a subsection; omit
  no-findings files and empty severity sections; a zero-findings run
  still writes the document.
- Never stage or commit the report — committing is the developer's
  per-report decision.
- No git root, or the file cannot be written → emit the full report in
  the reply and state why no file was written.
