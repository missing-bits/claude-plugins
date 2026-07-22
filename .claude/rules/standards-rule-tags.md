# Standards plugins — rule tags and severity

Binding for every Standards plugin in this repo (`salesforce-standards`,
`python-standards`, and any future domain plugin). Severity is data on
the rule, not judgment at review time.

## Rule tag grammar

Every rule carries its grade in its inline tag at its definition site
(rule ids are backtick-wrapped inside tags):

(id: `<rule-id>`; severity: critical|important|minor[; kind: defect|hardening]; source: <source>)

- One id, one absolute severity. `kind` is present exactly when
  `severity: critical`: `defect` marks a genuine runtime/live-risk
  failure, `hardening` a standards-mandated protection graded critical
  by house policy.
- No `## Review severities` roll-up sections — the tag is the single
  source of truth; no other surface may restate a rule's grade.
- Cross-skill mentions of a rule cite the owning rule id and defer to
  it; they never carry a severity word of their own.

## Sub-rules

A rule whose violations grade differently splits into sub-rules: a
`Sub-rules:` list directly under the group's tag, each bullet tagged
(id: `<group-id>.<suffix>`; severity: …[; kind: …]) — dot separator,
kebab-case suffix, absolute severity (never relative to the group);
`source` may be omitted (the group's source covers it). The group id
always keeps its own severity: the default for a finding that violates
the rule but matches no listed sub-rule.

- Never create a sub-rule whose severity equals the group default.
- A group's sub-rules are mutually exclusive — a violation matches at
  most one; where two could overlap, the sub-rule wording draws the
  boundary explicitly. Distinct sub-rule violations at one code
  location are distinct findings.

## Authoring rubric

Used when assigning severity (and kind at critical) to a new or edited
rule, and when a review grades a finding no rule covers (`rule: none`):

- **critical** — a defect that corrupts data, breaks security or
  sharing, or blows a platform limit on a bulk path;
- **important** — violates a standard in a way that forces rework or
  hides bugs;
- **minor** — naming, style, documentation.

This rubric is canonical here and appears verbatim in exactly three
other places: the working-process review-reports contract and the two
code-review skills' standalone fallbacks. It is never restated anywhere
else, and a reviewer never uses it to overrule a rule tag.
