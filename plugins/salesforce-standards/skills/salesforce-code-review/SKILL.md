---
name: salesforce-code-review
description: Use when auditing existing Salesforce code and metadata against the salesforce-standards skills — invoked by the /salesforce-review command or the salesforce-code-reviewer agent.
---

# Salesforce code review

Audit Salesforce code and metadata against the standards skills of
this plugin and write one Review report per run.

## Run scope

Review the files the standards skills cover:

- Apex: `*.cls`, `*.trigger`
- LWC bundles (`lwc/` directories)
- Aura bundles (`aura/` directories)
- Visualforce: `*.page`, `*.component`
- Flow metadata: `*.flow-meta.xml`
- Retired automation: `*.workflow-meta.xml` (Workflow Rules; Process
  Builder processes arrive as Flow metadata)
- Declarative data and access metadata: `*.object-meta.xml`,
  `*.field-meta.xml`, `*.recordType-meta.xml`,
  `*.validationRule-meta.xml`, `*.md-meta.xml` (Custom Metadata
  records), `*.globalValueSet-meta.xml`, `*.permissionset-meta.xml`,
  `*.permissionsetgroup-meta.xml`, `*.sharingRules-meta.xml`,
  `*.profile-meta.xml`

Static resources are in scope narrowly: flag NEW or MODIFIED custom
application JavaScript landing in a static resource (a placement
finding per salesforce-lwc); never review static-resource content
line-by-line; never review third-party libraries.

Files outside the domain that fall inside the requested scope are NOT
reviewed — list them in the report's Summary as out of scope.

## Metadata-reviewed files

Flow and declarative metadata files are reviewed from metadata, not
XML lines: findings cite elements by name (Flow elements, object and
field API names, permission-set grants). Within a severity subsection,
line-anchored findings come in ascending line order; findings without
a line anchor are ordered alphabetically by cited element name — this
domain's stable key under the shared contract's line-less-findings
provision.

## Procedure

1. Determine the scope: the current diff by default, or the files
   named by the caller.
2. Load the standards skills relevant to the content under review:
   salesforce-apex for any Apex; salesforce-apex-testing,
   salesforce-lwc, salesforce-flow, salesforce-data-model,
   salesforce-security-model, salesforce-aura, salesforce-visualforce
   as the content demands.
3. Grade every finding:
   - **Critical** — a defect that corrupts data, breaks security or
     sharing, or blows a governor limit on a bulk path.
   - **Important** — violates a standard in a way that forces rework
     or hides bugs (including new legacy-UI or retired-automation
     surface without a named platform forcing reason).
   - **Minor** — naming, style, documentation.
   Cite the standard for each finding (`standard: <skill>, rule: <id>`
   where the skill defines rule ids, e.g. PMD rule names).
4. Write the Review report (next section).
5. Reply with the report path and the findings grouped by severity; a
   zero-findings run still writes the report and states the result.

## Report contract

Run the Contract probe FIRST — do not assume the shared rule is in
context: check, in order,
`<project>/.claude/rules/working-process/review-reports.md`, then
`$HOME/.claude/rules/working-process/review-reports.md`; the first
file found wins. When the Contract probe succeeds, read that file and
follow it fully — **the installed working-process review-reports rule
supersedes the inline fallback below.**

## Inline fallback (Standalone install)

When the Contract probe finds nothing, this minimal contract applies —
a strict subset of the shared review-reports contract, never a
different shape:

- **Location**: `<project-root>/docs/code-review/`; create the
  directory if absent (the first-create mode question belongs to
  working-process's process-artifacts rule and is absent in a
  Standalone install).
- **Filename**: `<YYYY-MM-DD>-<scope-slug>-<runid>.md` — the date as
  the session knows it, `runid` 8 lowercase hex characters the run's
  owner generates itself; generated prompt-free (no shell commands, no
  questions). Never overwrite: check for an existing file with the
  session's file tools; on a collision generate a new runid and retry.
- **Frontmatter**: `ticket` (from context or branch, else `none`;
  never block on a question), `standards: salesforce-standards`,
  `findings: { critical: N, important: N, minor: N }` — the counts
  MUST equal the body.
- **Body**: a Summary section (scope reviewed, out-of-scope files,
  headline counts), then per-file sections with Critical → Important →
  Minor subsections — line-ascending within a subsection, line-less
  findings alphabetically by cited element name; omit no-findings
  files and empty severity sections; a zero-findings run still writes
  the document.
- Never stage or commit the report — committing is the developer's
  per-report decision.
- No git root, or the file cannot be written → emit the full report
  in the reply and state why no file was written.
