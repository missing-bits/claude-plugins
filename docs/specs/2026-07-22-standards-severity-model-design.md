---
ticket: "[#6, #7, #8]"
date: 2026-07-22
status: approved
grilled: 2026-07-22
architect: LGTM
branch: feature/8-standards-severity-model
base: master
---

# Standards-family severity model — design

## Overview

A family-wide redesign of how the Standards plugins (`salesforce-standards`,
`python-standards`, and any future domain plugin) express and apply review
severity. Severity moves out of the per-skill `## Review severities`
roll-ups into each rule's inline tag; multi-severity rules split into
dot-suffixed sub-ids; critical rules carry an orthogonal `kind` facet; the
code-review skills grade by a deterministic cascade instead of an abstract
definition. Shared runtime behavior lands in the working-process
review-reports contract; the authoring convention lands in a repo-level
rule; family vocabulary lands in the domain glossary.

Ships in one branch (`feature/8-standards-severity-model`) across all three
plugins, so the family never diverges: `working-process` 0.10.0 → 0.11.0,
`salesforce-standards` 0.1.0 → 0.2.0, `python-standards` 0.1.0 → 0.2.0.
Ticket #8 owns the standard; #6 (salesforce) and #7 (python) own adoption.

## Motivation

Dogfooding `salesforce-standards` 0.1.0 against five real Salesforce
codebases showed severity grading is path/attention dependent in both
directions: over-grading in the review's primary domain and under-grading
in secondary ones — the same rule (`lwc-custom-labels`) graded Critical in
one run and Minor in another; secondary-domain findings cited bare
`(standard: …)` with no rule id.

Root cause, twofold:

1. **Two competing authorities.** The `*-code-review` skill's abstract
   step-3 severity definition ("Critical — corrupts data…"; "Important —
   forces rework or hides bugs"; "Minor — naming, style, documentation")
   contradicts the area skills' `## Review severities` rows, which
   deliberately grade standards-mandated hardening (swallowed catch,
   assert-free test, `SeeAllData=true`, hardcoded UI string, hardcoded Id,
   missing Flow fault path) at Critical. The abstract acted as an
   attractor whenever the reviewer's attention lapsed.
2. **Severity far from the rule.** The grade lived in a roll-up section
   the reviewer had to visit separately from the rule text it actually
   read — the trip was skipped under load.

`python-code-review` carries a verbatim-identical step-3 abstract and the
same roll-up shape, so the defect is latent family-wide.

Additionally, in both end-to-end agent runs the reviewer spontaneously and
inconsistently sub-divided its Critical list into "runtime defects — fix
first" vs "hardening — critical per the house standard": the critical level
conflates two kinds that report consumers need distinguished.

### Decisions already made (recorded here, not re-opened)

- The hardening-at-Critical grades are **intentional house policy** — no
  demotions.
- The three severity levels stay. The critical-level conflation is
  answered by a **kind facet**, not a fourth level (two independent
  architect consults
  converged on this; SonarQube's abandonment of its flat 5-severity ladder
  in favor of an orthogonal per-rule facet is the external precedent).
- Family-wide in one branch — no interim divergence between the plugins.

## The rule-tag model

### Tag grammar

Every rule carries severity in its inline tag at its definition site:

```
(id: <rule-id>; severity: critical|important|minor[; kind: defect|hardening]; source: <source>)
```

- One id, one absolute severity.
- `kind` is **required when `severity: critical`**, absent otherwise:
  `defect` marks a genuine runtime/live-risk failure; `hardening` marks a
  standards-mandated protection graded critical by house policy. Kind is
  a property of the rule, assigned once at authoring time and read off
  like severity — never a per-finding judgment wherever a tag exists (a
  per-run call would reintroduce the grading variance this redesign
  removes). The sole tagless path is a candidate gap, graded and kinded
  by the authoring rubric — proto-authoring, not review-time judgment
  (see the grading cascade).
- The `## Review severities` roll-up sections are **removed** from every
  area skill. The tag is the single source of truth; no second surface
  can drift.

### Sub-rules

A rule whose violations grade differently splits into sub-rules with
dot-suffixed sub-ids, each with its own **absolute** severity (override,
not a relative modifier). The group id always keeps its own severity —
the default for a finding that matches the rule but no listed sub-rule.
Sub-rule entries live in the rule's own section, tagged, co-located with
the prose:

```markdown
## Assertions
…rule prose…
(id: apex-test-assertions; severity: important; source: …)

Sub-rules:
- a test asserting only "no exception", with no check on the resulting
  state (id: apex-test-assertions.no-state-check; severity: critical;
  kind: hardening)
- legacy `System.assert*` instead of `Assert` in a new test
  (id: apex-test-assertions.legacy-assert; severity: minor)
```

The dot separator is deliberate: existing ids are kebab-case, so a dashed
suffix would be indistinguishable from an ordinary id; `group.suffix`
makes the family structure greppable (`rg 'apex-test-assertions\.'`).

Only rules with genuinely divergent violation grades split; single-severity
rules keep their plain id. A sub-id whose severity equals its group's
default is redundant and not created (citation precision alone does not
justify one).

### Authoring rubric

The former step-3 abstract moves from grading time to authoring time and
is retitled the **authoring rubric**:

- critical — a defect that corrupts data, breaks security or sharing, or
  (domain-specific) blows a platform limit on a bulk path;
- important — violates a standard in a way that forces rework or hides
  bugs;
- minor — naming, style, documentation.

It guides the severity (and, at critical, the kind) assigned when writing
or editing a rule, and the grading of `rule: none` findings (below).
Reviewers never use it to overrule a tag. It lives in the repo-level
authoring rule and, excerpted, wherever `rule: none` grading is defined.

## The grading cascade

Each `*-code-review` skill replaces its abstract step-3 definition with:

1. **Sub-rule match** — the finding matches a listed sub-rule → that
   sub-rule's severity; cite its sub-id.
2. **Group match** — the finding violates the rule but matches no listed
   sub-rule → the group id's severity; cite the group id.
3. **No matching rule** — the finding is still reported and counted:
   cited as `(standard: <the loaded domain skill that lacks the rule>,
   rule: none)`, graded by the authoring rubric; at critical its kind is
   always `defect` — `hardening` denotes a standards-mandated
   protection, and a candidate gap by definition has no standard
   mandating it. A plausible-looking id is **never fabricated**. The
   named standard is where the candidate rule would live — it addresses
   the gap for the offers. (Content matching no domain skill at all
   stays a Summary out-of-scope note, not a finding — existing
   behavior.)

When a matching rule exists, citing its specific id is **mandatory** — a
bare `(standard: <skill>)` citation is not a valid finding.

## Candidate-gap offers

`rule: none` findings are candidate standards gaps. After writing the
report, the reviewer lists them in its reply (one line each: violation
class, proposed rule id, graded severity) and then offers — never
performs unprompted:

- **Project-memory park** — only when the reviewed project keeps a
  Project-memory store, detected by probe: `docs/memory/INDEX.md` and
  `.claude/memory/INDEX.md`. Offer to park the gaps as an idea entry;
  the write is done by whoever accepts (the developer's session), never
  by the review run itself. Store selection: explicit guidance wins
  when present (project CLAUDE.md, the developer's own instructions, or
  the store's conventions stating where a note type goes); otherwise,
  with both stores present the offer asks the developer which one; with
  one store it names that one. No store — no offer; the reviewer never
  proposes creating a store.
- **Upstream report** — always offered: drafting a report to the
  standards plugin's source repository, resolved at offer time from the
  installed marketplace's source metadata (e.g. `claude plugin
  marketplace list`) — never duplicated into plugin content, so forks
  resolve to themselves. When the source is not a public repository
  (a `directory`-source marketplace, a direct install), the offer
  degrades to the generalized draft with no filing target — the
  developer decides where it goes. Two gates: acceptance produces the
  draft, shown in full; only explicit approval of the draft files
  anything. The draft is generalized — the violation class and a
  proposed rule, never the reviewed project's code, identifiers, or
  name.

## Reports

The shared report contract stays schema- and layout-compatible: the
`findings: { critical: N, important: N, minor: N }` frontmatter, the
Critical → Important → Minor layout, and the within-subsection ordering
are unchanged; `rule: none` findings count normally. Kind surfaces
additively:

- an inline label on critical findings, e.g.
  `(standard: salesforce-apex, rule: apex-error-handling.swallowed-catch,
  kind: hardening)`;
- a prose breakdown in the Summary headline, e.g.
  "critical: 33 — 12 defect, 21 hardening".

No new frontmatter counts until a machine consumer exists.

## Where the pieces live

1. **working-process review-reports contract** (`rules/…/review-reports.md`,
   0.11.0) — the runtime-facing shared text: the `rule: none` citation
   convention, the kind label rendering, the candidate-gap offers, and
   the rubric excerpt used for `rule: none` grading. The amendment also
   reconciles the contract's closing scope section (today it declares
   finding-citation sources domain-owned; the `rule: none` convention
   becomes contract-owned). Canonical; each Standards plugin's inline
   fallback carries a strict subset for standalone installs (existing
   pattern). The fallback subset is enumerated, not left to inference —
   it explicitly includes the grading cascade, the `rule: none`
   citation, the kind labels + Summary breakdown, and the candidate-gap
   reply behavior (the listing and both offers). A Standalone install
   performs all of them — offers are reply-time behavior, not report
   shape, so the fallback names them rather than inheriting them via
   "report shape"; the memory-park offer naturally no-ops when no store
   exists.
2. **Repo authoring rule** (`.claude/rules/`, new file) — the authoring
   convention binding this repo: tag grammar, dot sub-ids, group
   defaults, kind assignment, the authoring rubric, the no-redundant-
   sub-id rule. This is repo governance, not plugin content — it ships
   to no one.
3. **Domain glossary** (`docs/domain/glossary.md`) — family vocabulary so
   the plugins cannot drift terminology: the tag grammar, *Sub-rule*,
   *Group default*, *Kind* (`defect` | `hardening`), *Authoring rubric*,
   *Candidate gap*.

## Per-plugin application

### salesforce-standards → 0.2.0 (#6)

- All 8 area skills: severity (+ kind at critical) into every rule tag;
  multi-severity rules split into sub-rules (the known set from the
  architect audit: `apex-test-assertions`, `data-model-validation-rules`,
  `flow-bulk-safe`, `flow-one-per-object-moment`, `lwc-wire-vs-imperative`,
  `lwc-js-conventions`, `aura-controller-helper`, `aura-events`,
  `security-sharing-rules`, `vf-data-binding`, `apex-error-handling`,
  `apex-sharing`, plus any found during implementation); untagged
  severity bullets (e.g. the `System.debug` Minor case) get ids;
  `## Review severities` sections removed.
- Cross-skill references defer to the owning rule id and never carry
  their own severity word (e.g. the `vf-security` FLS row → cite
  `security-fls`).
- `salesforce-code-review`: step 3 → the cascade; candidate-gap offers;
  inline fallback updated (strict subset of the amended contract).
- `salesforce-code-reviewer` agent: reply contract extended — candidate
  gaps listed after the severity summary, offers relayed; no severity
  wording of its own.
- `/salesforce-review` command: reply description deferred to the skill
  (one-line update).
- `salesforce-plan-review`: severity cross-references re-checked and
  re-worded where stale ("the shared severity definitions"); its own
  checklist grading is out of scope.

### python-standards → 0.2.0 (#7)

- Same mapping for all its area skills (the roll-up rows exist; the new
  judgment is group defaults and kind at critical — e.g. assert-free
  test → hardening, injection path → defect).
- `python-code-review`: step 3 → the cascade; offers; inline fallback.
- `python-code-reviewer` agent: reply contract extended the same way.
- `/python-review` command: reply description deferred to the skill.
- `python-plan-review`: cross-references re-checked.

### Audit invariants (implementation-time checks)

- Every rule and sub-id tag carries exactly one severity; kind present
  iff severity is critical.
- A group's sub-rules are mutually exclusive: a violation matches at
  most one sub-rule (authoring keeps sub-rule scopes disjoint); distinct
  sub-rule violations at one code location are distinct findings.
- No sub-id duplicates its group's severity.
- Every authoring-rubric excerpt — the review-reports contract and the
  two code-review skills' standalone fallbacks — is verbatim-identical
  to the canonical rubric in the repo authoring rule; no fifth copy
  exists anywhere.
- No id is defined in two skills with different severities; cross-skill
  mentions carry no severity words.
- No `## Review severities` section survives anywhere.
- Every formerly-listed severity bullet maps to a tagged rule or sub-id
  (nothing silently dropped).

## Validation

- **Eval scenarios** (skill-creator evals where available) against the
  rewritten code-review skills: (a) swallowed catch → critical/hardening
  from the tag; (b) hardcoded LWC UI string → critical/hardening via
  `lwc-custom-labels` (regression for the observed under-grade); (c) a
  finding matching a rule but no sub-rule → group default; (d) a genuine
  defect with no matching rule → `rule: none`, rubric-graded, listed in
  the reply as a candidate gap; (e) a bare `(standard: …)` citation →
  rejected, resolved to a specific id.
- **Dogfooding**: at least one review run on a real Salesforce codebase
  and one on a Python codebase before release, checked for: tag-derived
  grades (no path-dependence), zero fabricated ids, kind labels and the
  Summary breakdown present, offers behaving per contract.

## Out of scope

- `*-plan-review` checklist grading (separate surface; cross-references
  only).
- Changes to the three severity levels; new levels or sub-labels beyond
  `kind`.
- Machine-readable kind counts in report frontmatter (deferred until a
  consumer exists).
- The review→spec/plan/fix routing loop (working-process idea, parked).
- `.superpowers/**` artifacts and other working-process surfaces beyond
  the review-reports contract.

## Architect findings — 2026-07-22

Round 1, two parallel dispatches on the written, grilled spec:

- Context-bearing architect (Opus 4.8, third round on this design):
  **blocking** — sub-rule exclusivity missing from the audit invariants
  (grading variance relocatable to overlapping sub-rules); the
  Standalone-install fallback subset unspecified for the kind facet and
  the candidate-gap offers (reply-time behavior is not "report shape").
  Minor: command files out of scope, rubric multi-copy drift,
  `rule: none` critical kind left implicit, "byte-compatible" overstated.
- Fresh architect (Fable 5, no prior context): **concerns** — the
  upstream-offer target dangled on a README reference that does not
  exist. Minor: absolutist "never per-finding" wording, example sub-rule
  absent from the known set, rubric multi-copy, contract scope-section
  reconciliation unnamed.

All findings applied; the upstream target was re-designed per a
developer decision — resolved from installed-marketplace source metadata
instead of a README URL, degrading to a target-less draft for non-public
sources.

Verification round (Opus 4.8): **LGTM** — every finding confirmed
closed; the marketplace-resolution mechanism verified against the live
CLI; residual Minor (the glossary carried a third rubric copy) fixed by
pointing the glossary entry at the canonical rule.
