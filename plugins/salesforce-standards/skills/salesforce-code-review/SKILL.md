---
name: salesforce-code-review
description: Use when auditing existing Salesforce code and metadata against the salesforce-standards skills — invoked by the salesforce-code-reviewer agent, which the /salesforce-review command dispatches in the background.
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
3. Grade every finding by its rule tag — the tag is binding; no general
   intuition overrules it:
   - the finding matches a listed sub-rule → that sub-rule's severity;
     cite its sub-id (`standard: <skill>, rule: <group.suffix>`);
   - the finding violates the rule but matches no listed sub-rule → the
     group id's severity; cite the group id;
   - no defined rule covers the finding → report and count it anyway,
     cited `(standard: <the loaded skill that lacks the rule>,
     rule: none)` — or `(standard: salesforce-standards, rule: none)`
     when no skill of this plugin covers the concern. A concern
     covered by the domain of an existing but not-yet-loaded skill is
     NOT a candidate gap: load that skill and grade by its tags —
     `rule: none` is never asserted against a skill the run did not
     read. Graded by the authoring rubric in the review-reports
     contract; at critical its kind is always `defect`; when graded
     below critical while touching data integrity, security or
     sharing, or a platform limit, the finding states in one clause
     why it falls short of critical. Never invent a rule id.
   When a matching rule exists, citing its specific id is mandatory —
   a bare `(standard: <skill>)` citation is not a valid finding. A
   finding cites exactly one rule id; one location violating two
   rules yields two findings. Critical findings carry the rule's kind
   inline (`…, kind: defect|hardening`); the Summary headline breaks
   critical counts down by kind (e.g. "critical: 33 — 12 defect,
   21 hardening"). The Run scope is given by the caller and never
   self-extended: within it, a Salesforce-domain concern no rule
   covers is a counted `rule: none` finding (cascade above); files
   outside the domain (Run scope section) stay Summary out-of-scope
   notes.
4. Write the Review report (next section). Three bans bind in both
   modes (installed contract and Standalone fallback); large audits
   pressure each of them, and scale never changes the unit:
   - A violation class spanning N files is N findings — one per
     file, each enumerating only its own file's sites. Never fold a
     multi-file class into one pattern-level finding, however
     systemic or mechanical; `## Project` holds only findings not
     attributable to an existing file. A full-org audit counts
     exactly like a two-file diff.
   - A rerun never adopts the prior report's counting convention:
     when the prior report counts differently, the Summary
     disposition declares that boundary and marks count deltas
     non-comparable — comparability is never a reason to deviate.
   - The `rule: none` citation is the report's only candidate-gap
     trace — no "candidate gap" wording anywhere in the report body;
     the proposals live in the reply (step 5).
5. List `rule: none` findings in the reply as candidate standards gaps
   (one line each: violation class, proposed rule id, graded severity),
   then follow the review-reports contract's Candidate-gap offers
   section: offer a Project-memory park when a store exists (probe
   `docs/memory/INDEX.md` and `.claude/memory/INDEX.md`; explicit
   guidance on store choice wins, both-stores means ask, never offer to
   create one) and always offer a generalized upstream report (target
   resolved from the installed marketplace's source; non-public source
   → target-less draft; show the full draft before anything is filed;
   never include the reviewed project's code, identifiers, or name).
6. Reply with the report path and the findings grouped by severity; a
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
  headline counts); a `## Project` section FIRST when findings are
  not attributable to an existing file (same severity subsections as
  a file section; ordered by rule id, `rule: none` last by
  violation-class name); then per-file sections
  with Critical → Important → Minor subsections — line-ascending
  within a subsection, line-less findings alphabetically by cited
  element name; omit no-findings files and empty severity sections; a
  zero-findings run still writes the document. A finding
  is one violation class in one file (or at project level), its body
  enumerating every violating site, anchored by its first site; it
  cites exactly one rule id.
- Never stage or commit the report — committing is the developer's
  per-report decision.
- No git root, or the file cannot be written → emit the full report
  in the reply and state why no file was written.
- Grading: by the rule tags via the cascade in step 3 — sub-rule →
  group → `rule: none` graded by the authoring rubric:
  - **critical** — a defect that corrupts data, breaks security or
    sharing, or blows a platform limit on a bulk path;
  - **important** — violates a standard in a way that forces rework or
    hides bugs;
  - **minor** — naming, style, documentation.
  Specific-id citations are mandatory; `rule: none` at critical is
  always `kind: defect`.
- Critical findings carry `kind:` inline and the Summary breaks critical
  counts down by kind.
- The candidate-gap listing and both offers (memory park, upstream
  report) apply in full exactly as in step 5 — they are reply behavior
  and do not depend on the shared contract being installed.
