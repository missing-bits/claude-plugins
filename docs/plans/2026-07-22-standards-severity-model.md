---
ticket: "[#6, #7, #8]"
date: 2026-07-22
status: approved
adversary: concerns (resolved 2026-07-22)
branch: feature/8-standards-severity-model
base: master
---

# Standards-Family Severity Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move review severity out of per-skill `## Review severities` roll-ups into each rule's inline tag (with dot-suffixed sub-rules, group defaults, and a `kind` facet at critical), replace the code-review skills' abstract grading with a deterministic cascade, and add candidate-gap offers — across working-process, salesforce-standards, and python-standards in one branch.

**Architecture:** Three layers change: (1) a repo authoring rule + the working-process review-reports contract carry the shared convention (canonical rubric, `rule: none`, kind rendering, offers); (2) every area skill of both Standards plugins converts its severity roll-up into per-rule tags per the mapping tables below; (3) each `*-code-review` skill, agent, and command switches to the grading cascade. The spec is `docs/specs/2026-07-22-standards-severity-model-design.md` — the authority on any ambiguity.

**Tech Stack:** Markdown skill/rule content only — no application code. Verification = tag-extraction audits (`tr` + `grep`) + `claude plugin validate`.

## Global Constraints

- Public-repo hygiene: all committed text in English; no machine paths; no company/client names.
- Commits: ONE line, conventional-commit subject (`type(scope): …`), no body, no trailers, no `Co-Authored-By`.
- Tag grammar, verbatim (note: rule ids are BACKTICK-WRAPPED in tags, matching the existing corpus): ``(id: `<rule-id>`; severity: critical|important|minor[; kind: defect|hardening]; source: <source>)`` — `kind` present **iff** severity is critical. Sub-rule tags may omit `source` (the group's source covers them).
- Sub-ids use a DOT inside the backticks: `` `<group-id>.<suffix>` `` (suffix kebab-case). Never create a sub-rule whose severity equals its group default. A group's sub-rules must be mutually exclusive — where two could overlap, the sub-rule wording must draw the boundary explicitly.
- No `## Review severities` section may survive in any area skill.
- Every formerly-listed severity bullet maps to a tagged rule or sub-rule — nothing silently dropped; no bullet's grade changes vs today's roll-up (the mapping tables are conversions, not regrades).
- Cross-skill severity mentions carry NO severity word — they cite the owning rule id and defer.
- The authoring-rubric text is canonical in `.claude/rules/standards-rule-tags.md` and appears in exactly THREE other places, each verbatim: the review-reports contract excerpt and the two code-review skills' standalone fallbacks. Nowhere else restates it.
- Version bumps ride the FIRST commit touching each plugin: `working-process` → `0.11.0`, `salesforce-standards` → `0.2.0`, `python-standards` → `0.2.0`.
- Before every commit: `claude plugin validate .` passes, and `claude plugin validate plugins/<touched-plugin>` passes for each touched plugin.
- YAML frontmatter safety: any `description:`/scalar containing `: ` is quoted.

---

## The transformation pattern (referenced by Tasks 3–6 and 8)

Every area-skill task applies this pattern with its own mapping table:

**Before** (current shape — severity lives in a bottom roll-up; note the backticked id):

```markdown
## Assertions
…rule prose…
(id: `apex-test-assertions`; source: Apex Developer Guide — Assert class)

## Review severities
- **Critical**: a test asserting only "no exception" … (`apex-test-assertions`).
- **Important**: … calls with no failure message (`apex-test-assertions`); …
- **Minor**: … `System.assert*` used in a new test instead of `Assert` (`apex-test-assertions`).
```

**After** (severity in the tag; sub-rules co-located; roll-up deleted):

```markdown
## Assertions
…rule prose (unchanged)…
(id: `apex-test-assertions`; severity: important; source: Apex Developer Guide — Assert class)

Sub-rules:
- a test asserting only "no exception", with no check on the resulting
  state (id: `apex-test-assertions.no-state-check`; severity: critical;
  kind: hardening)
- legacy `System.assert*` instead of `Assert` in a new test
  (id: `apex-test-assertions.legacy-assert`; severity: minor)
```

Steps per skill file:
1. For each rule id in the mapping table, extend its existing ``(id: `…`; source: …)`` tag with `severity:` (and `kind:` when critical) — inserted between `id` and `source`.
2. For each sub-rule row, add a `Sub-rules:` list directly under the group's tag; each bullet reuses the roll-up bullet's wording and carries the full sub-id tag.
3. Severity bullets whose meaning equals the group default (no split needed) become nothing — the group tag already carries the grade; keep their wording ONLY if the rule prose does not already describe that violation (then fold it into the prose, untagged).
4. Delete the whole `## Review severities` section.
5. Verify (per file) — tags wrap across lines, so flatten first; the expected tag count = groups + sub-rules from the mapping table:

```bash
F=plugins/<plugin>/skills/<skill>/SKILL.md
FLAT=$(tr '\n' ' ' < "$F" | tr -s ' ')
# 5a. every id carries a severity (diff of all ids vs graded ids — expect no output):
diff <(echo "$FLAT" | grep -oE 'id: `[a-z][a-z.-]*`' | sort -u) \
     <(echo "$FLAT" | grep -oE 'id: `[a-z][a-z.-]*`; severity: (critical|important|minor)' | grep -oE 'id: `[a-z][a-z.-]*`' | sort -u)
# 5b. graded-tag count equals the table's groups + sub-rules:
echo "$FLAT" | grep -oE 'severity: (critical|important|minor)' | wc -l
# 5c. kind iff critical (both directions — expect no output from each):
echo "$FLAT" | grep -oE 'severity: critical[^)]*' | grep -v 'kind: \(defect\|hardening\)' || true
echo "$FLAT" | grep -oE 'severity: (important|minor); kind:' || true
# 5d. no roll-up survives (expect no output):
grep -n '## Review severities' "$F" || true
```

---

### Task 1: Repo authoring rule (canonical rubric + tag convention) + docs ride-along

**Files:**
- Create: `.claude/rules/standards-rule-tags.md`
- Commit (ride-along, tracked-mode docs of this work): `docs/specs/2026-07-22-standards-severity-model-design.md`, `docs/plans/2026-07-22-standards-severity-model.md`, `docs/domain/glossary.md`

**Interfaces:**
- Produces: the canonical authoring-rubric text (Tasks 2, 7, 9 excerpt it VERBATIM), the tag grammar, and the sub-rule/kind conventions every later task follows.

- [ ] **Step 1: Write the rule file** with exactly this content:

```markdown
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
```

- [ ] **Step 2: Verify** — `claude plugin validate .` passes.

- [ ] **Step 3: Commit** — `git add .claude/rules/standards-rule-tags.md docs/specs/2026-07-22-standards-severity-model-design.md docs/plans/2026-07-22-standards-severity-model.md docs/domain/glossary.md && git commit -m "docs: standards rule-tag authoring rule, severity-model spec, plan, glossary terms"`

---

### Task 2: working-process review-reports contract amendment (+ bump 0.11.0)

**Files:**
- Modify: `plugins/working-process/rules/review-reports.md`
- Modify: `plugins/working-process/.claude-plugin/plugin.json` (version `0.10.0` → `0.11.0`)

**Interfaces:**
- Consumes: the rubric text from Task 1 (verbatim excerpt).
- Produces: contract sections `Finding citations` and `Candidate-gap offers` that Tasks 7 and 9 reference by name; the kind-label rendering the fallbacks subset.

- [ ] **Step 1: Read the contract**, locate the Layout section and the closing scope section that declares finding-citation sources domain-owned (around lines 96–97 and 153–156).

- [ ] **Step 2: Insert after the Layout section**:

```markdown
## Finding citations

- A finding that violates a defined rule cites its most specific id:
  `(standard: <skill>, rule: <id>)` — the sub-id when a sub-rule
  matched, the group id otherwise. When a matching rule exists, the
  specific id is mandatory; a bare `(standard: <skill>)` citation is
  not a valid finding.
- A finding no defined rule covers is still reported and counted:
  cited `(standard: <the loaded domain skill that lacks the rule>,
  rule: none)`, graded by the authoring rubric below, and — when graded
  critical — always `kind: defect` (hardening denotes a
  standards-mandated protection, and a `rule: none` finding has no
  standard mandating it). A plausible-looking rule id is never
  fabricated.
- Critical findings carry the rule's kind inline:
  `(standard: <skill>, rule: <id>, kind: defect|hardening)`; the
  Summary headline adds a prose breakdown, e.g.
  "critical: 33 — 12 defect, 21 hardening". Counts in `findings:` stay
  the three severity keys — kind adds no frontmatter field.
- When the loaded domain skill's rule tags carry no severity (a
  pre-adoption plugin version), the reviewer grades by that skill's own
  documented severities and omits the kind labels and breakdown rather
  than judging them per finding.

Authoring rubric (canonical in the owning repo's authoring rule;
this excerpt is verbatim-identical):

- **critical** — a defect that corrupts data, breaks security or
  sharing, or blows a platform limit on a bulk path;
- **important** — violates a standard in a way that forces rework or
  hides bugs;
- **minor** — naming, style, documentation.

## Candidate-gap offers

`rule: none` findings are candidate standards gaps. After writing the
report, the run's owner lists them in its reply — one line each:
violation class, proposed rule id, graded severity — and then offers,
never performs unprompted:

- **Project-memory park** — only when the reviewed project keeps a
  Project-memory store (probe `docs/memory/INDEX.md` and
  `.claude/memory/INDEX.md`). The write is done by whoever accepts,
  never by the review run. Store selection: explicit guidance wins
  (project CLAUDE.md, the developer's own instructions, the store's
  conventions); otherwise with both stores present the offer asks the
  developer which one; with one store it names that one. No store — no
  offer, and never an offer to create a store.
- **Upstream report** — always offered: a report to the standards
  plugin's source repository, resolved at offer time from the installed
  marketplace's source metadata (e.g. `claude plugin marketplace
  list`); a non-public source (a directory-source marketplace, a
  direct install) degrades the offer to a generalized draft with no
  filing target. Two gates: acceptance produces the draft, shown in
  full; only explicit approval files anything. The draft carries the
  violation class and a proposed rule — never the reviewed project's
  code, identifiers, or name.
```

- [ ] **Step 3: Reconcile the closing scope section** — where it declares finding-citation sources domain-owned, reword to: rule ids and their severities stay domain-owned (defined in the standards skills' rule tags); the `rule: none` citation form, the kind label rendering, and the candidate-gap offers are contract-owned (defined above).

- [ ] **Step 4: Bump** `plugins/working-process/.claude-plugin/plugin.json` version to `0.11.0`.

- [ ] **Step 5: Verify rubric identity** (normalized full-text comparison, not first-lines-only):

```bash
extract_rubric() { tr '\n' ' ' < "$1" | tr -s ' ' | grep -oE '\*\*critical\*\* — a defect that corrupts data.*naming, style, documentation\.' | head -1; }
[ "$(extract_rubric .claude/rules/standards-rule-tags.md)" = "$(extract_rubric plugins/working-process/rules/review-reports.md)" ] && echo RUBRIC-OK
claude plugin validate plugins/working-process
```

Expected: `RUBRIC-OK` and a passing validate.

- [ ] **Step 6: Commit** — `git commit -am "feat(working-process): contract-own rule-none citations, kind labels, and candidate-gap offers"`

---

### Task 3: Convert salesforce-apex + salesforce-apex-testing (+ bump 0.2.0)

**Files:**
- Modify: `plugins/salesforce-standards/skills/salesforce-apex/SKILL.md`
- Modify: `plugins/salesforce-standards/skills/salesforce-apex-testing/SKILL.md`
- Modify: `plugins/salesforce-standards/.claude-plugin/plugin.json` (version `0.1.0` → `0.2.0`)

Apply the transformation pattern with these mappings. Expected counts = groups + sub-rules. EVERY id defined in the file must appear in the table — verification 5a fails otherwise.

**salesforce-apex** (6 groups + 4 sub-rules → expected graded-tag count: 10):

| id | group severity | kind | sub-rules |
|---|---|---|---|
| `apex-bulkification` | important | — | `.loop-on-trigger-path` (SOQL/DML in a loop reachable from a trigger path) critical/defect |
| `apex-sharing` | important | — | `.undeclared-with-dml` (class doing SOQL/DML without a sharing declaration; PMD `ApexSharingViolations`) critical/hardening |
| `apex-error-handling` | important | — | `.swallowed-catch` (the caught exception is neither handled nor rethrown — a catch whose only content is `System.debug` counts as swallowed) critical/hardening; `.debug-only-reporting` (the catch DOES handle or rethrow, but reports only via `System.debug`) minor |
| `apex-layering` | important | — | — |
| `apex-governor-limits` | important | — | — |
| `apex-naming` | minor | — | — |

Note the `.swallowed-catch` / `.debug-only-reporting` boundary above is deliberate (mutual exclusivity): debug-only-and-nothing-else = swallowed; handled-but-debug-reported = debug-only-reporting.

Roll-up bullets absorbed by group defaults (no sub-rule; fold wording into rule prose only if absent): "a generic `Exception` catch/throw instead of a domain exception" → `apex-error-handling` group; "an undocumented `without sharing`" → `apex-sharing` group.

**salesforce-apex-testing** (7 groups + 3 sub-rules → expected graded-tag count: 10):

| id | group severity | kind | sub-rules |
|---|---|---|---|
| `apex-test-no-see-all-data` | critical | hardening | — |
| `apex-test-mocking` | important | — | `.real-callout` (a real HTTP callout reachable from a test run instead of `Test.setMock`) critical/defect |
| `apex-test-assertions` | important | — | `.no-state-check` (test asserting only "no exception", no check on resulting state) critical/hardening; `.legacy-assert` (`System.assert*` instead of `Assert` in a new test) minor |
| `apex-test-coverage` | important | — | — |
| `apex-test-data-factory` | important | — | — |
| `apex-test-start-stop` | important | — | — |
| `apex-test-structure` | minor | — | — |

Note: `apex-test-mocking` groups at important (its DI-only Stub API and
no-mocking-framework stances were never Critical in the roll-up); only
the real-callout case is critical, as today.

- [ ] **Step 1**: Apply the pattern to `salesforce-apex/SKILL.md`; run the per-file verification block (expected count 10).
- [ ] **Step 2**: Apply the pattern to `salesforce-apex-testing/SKILL.md`; run the per-file verification block (expected count 10).
- [ ] **Step 3**: Bump `plugins/salesforce-standards/.claude-plugin/plugin.json` to `0.2.0`.
- [ ] **Step 4**: `claude plugin validate plugins/salesforce-standards`
- [ ] **Step 5: Commit** — `git commit -am "feat(salesforce-standards): severity-in-tag model for apex and apex-testing skills"`

---

### Task 4: Convert salesforce-lwc + salesforce-flow

**Files:**
- Modify: `plugins/salesforce-standards/skills/salesforce-lwc/SKILL.md`
- Modify: `plugins/salesforce-standards/skills/salesforce-flow/SKILL.md`

**salesforce-lwc** (8 groups + 2 sub-rules → expected graded-tag count: 10):

| id | group severity | kind | sub-rules |
|---|---|---|---|
| `lwc-wire-vs-imperative` | important | — | `.cacheable-dml` (Apex method marked `cacheable=true` performing DML) critical/defect |
| `lwc-custom-labels` | critical | hardening | — |
| `lwc-js-conventions` | minor | — | `.cross-root-dom` (DOM access outside the component's own shadow root, incl. another component's markup) critical/hardening |
| `lwc-communication` | important | — | — |
| `lwc-styling` | important | — | — |
| `lwc-placement` | important | — | — |
| `lwc-jest` | minor | — | — |
| `lwc-structure` | minor | — | — |

Bullets absorbed by groups: event naming + LMS unsubscribe → `lwc-communication` (both important, group covers); `@track` misuse → `lwc-js-conventions` group (minor); jest `querySelector` → `lwc-jest` group.

**salesforce-flow** (7 groups + 2 sub-rules → expected graded-tag count: 9):

| id | group severity | kind | sub-rules |
|---|---|---|---|
| `flow-bulk-safe` | important | — | `.dml-in-loop` (Get/Update/Delete Records element inside a Loop) critical/defect |
| `flow-fault-paths` | critical | hardening | — |
| `flow-one-per-object-moment` | important | — | `.duplicate-trigger-flow` (second record-triggered flow on an object+moment an existing flow owns) critical/hardening |
| `flow-run-context` | important | — | — |
| `flow-retired-automation` | important | — | — |
| `flow-plan-before-build` | minor | — | — |
| `flow-naming` | minor | — | — |

- [ ] **Step 1**: Apply the pattern to both files; run the per-file verification blocks (expected counts 10 and 9).
- [ ] **Step 2**: `claude plugin validate plugins/salesforce-standards`
- [ ] **Step 3: Commit** — `git commit -am "feat(salesforce-standards): severity-in-tag model for lwc and flow skills"`

---

### Task 5: Convert salesforce-data-model + salesforce-security-model

**Files:**
- Modify: `plugins/salesforce-standards/skills/salesforce-data-model/SKILL.md`
- Modify: `plugins/salesforce-standards/skills/salesforce-security-model/SKILL.md`

**salesforce-data-model** (7 groups + 2 sub-rules → expected graded-tag count: 9):

| id | group severity | kind | sub-rules |
|---|---|---|---|
| `data-model-no-hardcoded-ids` | critical | hardening | — |
| `data-model-validation-rules` | important | — | `.no-bypass` (validation rule with no bypass strategy at all) critical/hardening; `.naming` (naming-convention deviations on validation rules, numbered names included) minor |
| `data-model-descriptions` | important | — | — |
| `data-model-global-value-sets` | important | — | — |
| `data-model-record-types` | important | — | — |
| `data-model-cmt-vs-settings` | important | — | — |
| `data-model-naming` | minor | — | — |

Notes: `data-model-no-hardcoded-ids` is `hardening` per the spec's
Motivation list (standards-mandated protections at Critical) — the
cross-org runtime-breakage argument was considered and the spec's
classification wins. `.naming` deliberately covers ALL validation-rule
naming deviations (today's Minor bullet), not only numbered names.
Bullet absorbed: "error message that doesn't tell the user what to
change" → `data-model-validation-rules` group (important).

**salesforce-security-model** (6 groups + 2 sub-rules → expected graded-tag count: 8):

| id | group severity | kind | sub-rules |
|---|---|---|---|
| `security-owd` | critical | defect | — |
| `security-fls` | critical | hardening | — |
| `security-permission-set-first` | important | — | `.naming` (permission set / group naming deviations) minor |
| `security-sharing-rules` | important | — | `.naming` (sharing-rule naming deviations) minor |
| `security-role-hierarchy` | important | — | — |
| `security-access-grant-questions` | important | — | — |

- [ ] **Step 1**: Apply the pattern to both files; run the per-file verification blocks (expected counts 9 and 8).
- [ ] **Step 2**: `claude plugin validate plugins/salesforce-standards`
- [ ] **Step 3: Commit** — `git commit -am "feat(salesforce-standards): severity-in-tag model for data-model and security-model skills"`

---

### Task 6: Convert salesforce-aura + salesforce-visualforce

**Files:**
- Modify: `plugins/salesforce-standards/skills/salesforce-aura/SKILL.md`
- Modify: `plugins/salesforce-standards/skills/salesforce-visualforce/SKILL.md`

Special handling in this task:
- The "new Aura/Visualforce surface with no named platform-forcing reason (Maintenance-first)" bullets: locate each skill's Maintenance-first policy statement; if it carries no rule id, give it one — `aura-maintenance-first` / `vf-maintenance-first` — tagged important. If an id already exists for it, use that id instead everywhere the table says `*-maintenance-first` (and keep the expected counts, which count the rule either way).
- The visualforce Critical bullet "query or DML in system context with no FLS/sharing enforcement (`salesforce-security-model`, cited there)": this is a CROSS-SKILL reference. Do NOT tag it in visualforce. Keep one deferring sentence in the vf prose: "System-context FLS in a controller or extension is graded by `security-fls` (salesforce-security-model)." — no severity word.

**salesforce-aura** (6 groups + 5 sub-rules → expected graded-tag count: 11):

| id | group severity | kind | sub-rules |
|---|---|---|---|
| `aura-controller-helper` | important | — | `.business-logic-in-client` (calculation / eligibility / status rule in controller or helper instead of Apex) critical/hardening |
| `aura-events` | important | — | `.application-event-overuse` (application event where a component event would do) critical/hardening; `.named-after-component` (event named after the firing component instead of what happened) minor |
| `aura-markup` | important | — | `.inline-expression` (markup expression doing inline arithmetic/concatenation instead of a precomputed attribute) minor; `.frequent-toggle-aura-if` (`aura:if` for a frequently-toggled stateless visibility switch CSS would serve) minor |
| `aura-lds` | important | — | — |
| `aura-migration` | important | — | — |
| `aura-maintenance-first` | important | — | — |

**salesforce-visualforce** (5 groups + 2 sub-rules → expected graded-tag count: 7):

| id | group severity | kind | sub-rules |
|---|---|---|---|
| `vf-security` | critical | defect | — |
| `vf-controller-ladder` | important | — | `.needless-extension` (extension where standard controller alone suffices) minor |
| `vf-data-binding` | important | — | `.inline-expression` (page expression doing inline arithmetic / multi-step conditional instead of a precomputed controller property) minor |
| `vf-view-state` | important | — | — |
| `vf-maintenance-first` | important | — | — |

- [ ] **Step 1**: Apply the pattern + special handling to both files; run the per-file verification blocks (expected counts 11 and 7). Additionally verify the cross-skill defer carries no severity word:

```bash
tr '\n' ' ' < plugins/salesforce-standards/skills/salesforce-visualforce/SKILL.md | tr -s ' ' | grep -oiE '.{0,60}security-fls.{0,60}' | grep -i 'critical' || echo DEFER-OK
```

Expected: `DEFER-OK`.

- [ ] **Step 2**: `claude plugin validate plugins/salesforce-standards`
- [ ] **Step 3: Commit** — `git commit -am "feat(salesforce-standards): severity-in-tag model for aura and visualforce skills"`

---

### Task 7: salesforce-code-review cascade + offers + fallback; agent, command, plan-review

**Files:**
- Modify: `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`
- Modify: `plugins/salesforce-standards/agents/salesforce-code-reviewer.md`
- Modify: `plugins/salesforce-standards/commands/salesforce-review.md`
- Modify: `plugins/salesforce-standards/skills/salesforce-plan-review/SKILL.md`

**Interfaces:**
- Consumes: contract section names from Task 2 (`Finding citations`, `Candidate-gap offers`); tags produced by Tasks 3–6; the verbatim rubric from Task 1.

- [ ] **Step 1: Replace procedure step 3** (the abstract Critical/Important/Minor definitions, currently lines ~56–64) with:

```markdown
3. Grade every finding by its rule tag — the tag is binding; no general
   intuition overrules it:
   - the finding matches a listed sub-rule → that sub-rule's severity;
     cite its sub-id (`standard: <skill>, rule: <group.suffix>`);
   - the finding violates the rule but matches no listed sub-rule → the
     group id's severity; cite the group id;
   - no defined rule covers the finding → report and count it anyway,
     cited `(standard: <the loaded skill that lacks the rule>,
     rule: none)`, graded by the authoring rubric in the review-reports
     contract; at critical its kind is always `defect`. Never invent a
     rule id.
   When a matching rule exists, citing its specific id is mandatory —
   a bare `(standard: <skill>)` citation is not a valid finding.
   Critical findings carry the rule's kind inline
   (`…, kind: defect|hardening`); the Summary headline breaks critical
   counts down by kind (e.g. "critical: 33 — 12 defect, 21 hardening").
   Content matching no loaded domain skill stays a Summary out-of-scope
   note, not a finding.
```

- [ ] **Step 2: Add a candidate-gap step** after the report-writing step (renumber the reply step accordingly):

```markdown
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
```

- [ ] **Step 3: Extend the Inline fallback section** (Standalone install) — append to its list, keeping its existing items untouched. The rubric bullets below are the sanctioned third verbatim copy — do not paraphrase them:

```markdown
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
```

- [ ] **Step 4: Agent** — in `salesforce-code-reviewer.md`, extend the reply contract sentence ("report path and findings grouped by severity") with: "…, then the candidate-gap list and offers per the skill's step 5". No severity wording added.
- [ ] **Step 5: Command** — in `salesforce-review.md`, reword the reply-shape sentence to defer: "Reply as the salesforce-code-review skill specifies (report path, severity summary, candidate gaps and offers)."
- [ ] **Step 6: plan-review** — in `salesforce-plan-review/SKILL.md` (~lines 42–46), reword the stale "the shared severity definitions" cross-reference to point at rule tags (e.g. "one grade above the severity `flow-retired-automation` carries in its rule tag"). No other change.
- [ ] **Step 7: Verify**

```bash
S=plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md
# rubric text appears ONLY in the fallback (once), not in step 3 — expect exactly 1:
tr '\n' ' ' < $S | tr -s ' ' | grep -oE '\*\*critical\*\* — a defect that corrupts data' | wc -l
grep -c 'rule: none' $S       # expected: 4 (step 3, step 5, fallback x2)
# no severity DEFINITIONS in agent/command (grouping mentions are fine) — expect no output:
grep -riE 'corrupts data|forces rework|hides bugs|naming, style' plugins/salesforce-standards/agents plugins/salesforce-standards/commands || true
claude plugin validate plugins/salesforce-standards
```

- [ ] **Step 8: Commit** — `git commit -am "feat(salesforce-standards): tag-driven grading cascade, candidate-gap offers, standalone fallback"`

---

### Task 8: Convert the python area skills (+ bump 0.2.0)

**Files:**
- Modify: `plugins/python-standards/skills/python-cli/SKILL.md`
- Modify: `plugins/python-standards/skills/python-code-style/SKILL.md`
- Modify: `plugins/python-standards/skills/python-project-layout/SKILL.md`
- Modify: `plugins/python-standards/skills/python-testing/SKILL.md`
- Modify: `plugins/python-standards/skills/python-typing/SKILL.md`
- Modify: `plugins/python-standards/skills/python-web-api/SKILL.md`
- Modify: `plugins/python-standards/.claude-plugin/plugin.json` (version `0.1.0` → `0.2.0`)

Python's roll-ups are looser than salesforce's ("Minor: everything else"), so the mapping directive is:

1. Enumerate every rule id in the file: `` tr '\n' ' ' < SKILL.md | grep -oE 'id: `[a-z-]*`' ``.
2. Ids named in the roll-up get the stated severity; **every id not named gets `severity: minor`** (that is what "everything else" means — the group default becomes explicit).
3. Untagged roll-up phrases must be resolved to their owning rule id by reading the rule prose; they become the group severity or a sub-rule of that id per the table below.
4. Then apply the standard transformation pattern (delete the roll-up, per-file verification; expected count = ids in the file + sub-rules added).

| skill | directives |
|---|---|
| `python-cli` | `cli-stderr-logs` important; `cli-exit-codes` important; `cli-errors-no-traceback` important; all other ids minor. |
| `python-code-style` | `style-ruff-only` important; "naming that misleads (`get_x()` that mutates)" → resolve to the naming rule's id, add sub-rule `.misleading-name` important with group default minor; all other ids minor. |
| `python-project-layout` | `layout-interpreter-owner` important; `layout-dep-direction` important; "uncommitted `uv.lock`" → resolve to the lockfile rule's id, group important (or sub-rule `.uncommitted-lock` important if that rule also covers minor-grade violations); all other ids minor. |
| `python-testing` | `test-mock-boundaries` important; `test-fixture-scope` important; "a behavior change shipped with no covering test" → resolve to the coverage rule's id, important; all other ids minor. |
| `python-typing` | `typing-no-any-laundering` important; "unexplained `type: ignore`" → owning id, important (sub-rule if the owning rule is otherwise minor); "public API without annotations" → owning id, important (same pattern); all other ids minor. |
| `python-web-api` | `web-async-boundaries` critical/defect (blocking IO in an async path stalls the event loop — genuine runtime failure); "layering violations", "stack traces in responses", "missing `response_model`" → their owning ids, important each (sub-rules where the owning rule is otherwise minor); all other ids minor. |

Note: python then has exactly ONE critical rule (`web-async-boundaries`, kind `defect`) — "Critical: none at this level" in python-code-style stays true by tags alone.

- [ ] **Step 1**: Apply per-skill directives + the transformation pattern to all six files; run per-file verification blocks.
- [ ] **Step 2**: Bump `plugins/python-standards/.claude-plugin/plugin.json` to `0.2.0`.
- [ ] **Step 3**: `claude plugin validate plugins/python-standards`
- [ ] **Step 4: Commit** — `git commit -am "feat(python-standards): severity-in-tag model for the area skills"`

---

### Task 9: python-code-review cascade + offers + fallback; agent, command, plan-review

**Files:**
- Modify: `plugins/python-standards/skills/python-code-review/SKILL.md`
- Modify: `plugins/python-standards/agents/python-code-reviewer.md`
- Modify: `plugins/python-standards/commands/python-review.md`
- Modify: `plugins/python-standards/skills/python-plan-review/SKILL.md` (cross-reference re-check only)

Same shape as Task 7 — the full text is repeated so this task stands alone.

- [ ] **Step 1: Replace procedure step 3** (abstract definitions, lines ~24–28) with:

```markdown
3. Grade every finding by its rule tag — the tag is binding; no general
   intuition overrules it:
   - the finding matches a listed sub-rule → that sub-rule's severity;
     cite its sub-id (`standard: <skill>, rule: <group.suffix>`);
   - the finding violates the rule but matches no listed sub-rule → the
     group id's severity; cite the group id;
   - no defined rule covers the finding → report and count it anyway,
     cited `(standard: <the loaded skill that lacks the rule>,
     rule: none)`, graded by the authoring rubric in the review-reports
     contract; at critical its kind is always `defect`. Never invent a
     rule id.
   When a matching rule exists, citing its specific id is mandatory —
   a bare `(standard: <skill>)` citation is not a valid finding.
   Critical findings carry the rule's kind inline
   (`…, kind: defect|hardening`); the Summary headline breaks critical
   counts down by kind. Content matching no loaded domain skill stays a
   Summary out-of-scope note, not a finding.
```

- [ ] **Step 2: Add a candidate-gap step** after the report-writing step (renumber the reply step accordingly):

```markdown
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
```

- [ ] **Step 3: Extend the Inline fallback section** — append, keeping existing items untouched. The rubric bullets are the sanctioned fourth verbatim copy — do not paraphrase:

```markdown
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
```

- [ ] **Step 4: Agent** — in `python-code-reviewer.md`, extend the reply contract sentence ("report path and findings grouped by severity") with: "…, then the candidate-gap list and offers per the skill's step 5". No severity wording added.
- [ ] **Step 5: Command** — in `python-review.md`, reword the reply-shape sentence to defer: "Reply as the python-code-review skill specifies (report path, severity summary, candidate gaps and offers)."
- [ ] **Step 6: plan-review** — grep `python-plan-review/SKILL.md` for references to the code-review skill's severity definitions; re-word any to cite rule tags. Its own checklist grading (Critical/Important per item) stays untouched — separate surface, out of scope.
- [ ] **Step 7: Verify** — same commands as Task 7 Step 7 with `plugins/python-standards` paths; `claude plugin validate plugins/python-standards`.
- [ ] **Step 8: Commit** — `git commit -am "feat(python-standards): tag-driven grading cascade, candidate-gap offers, standalone fallback"`

---

### Task 10: Family audit — the spec's invariants, mechanically

**Files:**
- No new files; fixes land in whichever file an audit finding names.

- [ ] **Step 1: Run the audit script** (from the worktree root; uses a failure counter, NOT `set -e` — `!`-pipelines don't trip `set -e`):

```bash
FAIL=0
SK="plugins/salesforce-standards/skills plugins/python-standards/skills"
AREA=$(grep -rl 'id: `' $SK --include=SKILL.md | grep -v 'plan-review\|code-review')
flat() { tr '\n' ' ' < "$1" | tr -s ' '; }

echo "== A. no roll-up survives =="
grep -rn '## Review severities' $SK && FAIL=$((FAIL+1))

echo "== B. every id tagged with a severity =="
for f in $AREA; do
  diff <(flat "$f" | grep -oE 'id: `[a-z][a-z.-]*`' | sort -u) \
       <(flat "$f" | grep -oE 'id: `[a-z][a-z.-]*`; severity: (critical|important|minor)' | grep -oE 'id: `[a-z][a-z.-]*`' | sort -u) \
       >/dev/null || { echo "UNTAGGED IDS IN $f"; FAIL=$((FAIL+1)); }
done

echo "== C. kind iff critical =="
for f in $AREA; do
  flat "$f" | grep -oE 'severity: critical[^)]*' | grep -vq 'kind: \(defect\|hardening\)' && { echo "CRITICAL WITHOUT KIND IN $f"; FAIL=$((FAIL+1)); }
  flat "$f" | grep -oE 'severity: (important|minor); kind:' | grep -q . && { echo "KIND OUTSIDE CRITICAL IN $f"; FAIL=$((FAIL+1)); }
done

echo "== D. no severity word on the vf cross-skill mention =="
flat plugins/salesforce-standards/skills/salesforce-visualforce/SKILL.md | grep -oiE '.{0,60}security-fls.{0,60}' | grep -qi 'critical' && { echo "VF DEFER CARRIES SEVERITY"; FAIL=$((FAIL+1)); }

echo "== E. rubric copies verbatim-identical (4 locations) =="
extract_rubric() { tr '\n' ' ' < "$1" | tr -s ' ' | grep -oE '\*\*critical\*\* — a defect that corrupts data.*naming, style, documentation\.' | head -1; }
COPIES=$(for f in .claude/rules/standards-rule-tags.md \
  plugins/working-process/rules/review-reports.md \
  plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md \
  plugins/python-standards/skills/python-code-review/SKILL.md; do extract_rubric "$f"; done | sort -u | wc -l)
[ "$COPIES" = "1" ] || { echo "RUBRIC COPIES DIVERGE ($COPIES variants)"; FAIL=$((FAIL+1)); }

echo "== F. no duplicate id definitions family-wide; sub-vs-group data for the eyeball check =="
for f in $AREA; do flat "$f" | grep -oE 'id: `[a-z][a-z.-]*`; severity: [a-z]+' | sed "s|^|$f |"; done > /tmp/all-graded-ids.txt
# field 3 is the backticked id token; a duplicate means one id defined in two places:
awk '{print $3}' /tmp/all-graded-ids.txt | sort | uniq -d | grep -q . && { echo "DUPLICATE ID DEFINITIONS:"; awk '{print $3}' /tmp/all-graded-ids.txt | sort | uniq -d; FAIL=$((FAIL+1)); }
echo "-- sub-rule (dotted) ids — eyeball each against its group's severity below:"
awk '$3 ~ /\./' /tmp/all-graded-ids.txt
echo "-- group ids:"
awk '$3 !~ /\./' /tmp/all-graded-ids.txt

echo "== G. plugin validation =="
claude plugin validate . && claude plugin validate plugins/salesforce-standards && claude plugin validate plugins/python-standards && claude plugin validate plugins/working-process || FAIL=$((FAIL+1))

echo "FAILURES: $FAIL"; [ "$FAIL" = "0" ] && echo AUDIT-CLEAN
```

Expected final output: `AUDIT-CLEAN`.

- [ ] **Step 2**: The sub-vs-group comparison is deliberately an EYEBALL check (a shell version proved fragile): for each printed dotted id, confirm its severity differs from its group's in the printed group list (the mapping tables in Tasks 3–6 already guarantee no equality; the check catches drift).
- [ ] **Step 3**: Fix anything the audit flags, re-run until `AUDIT-CLEAN`.
- [ ] **Step 4: Commit** (only if fixes were needed) — `git commit -am "fix(standards): close severity-model audit findings"`

---

## Post-plan validation (developer-driven, not tasks)

- Eval scenarios from the spec's Validation section (skill-creator evals where available): (a) swallowed catch → critical/hardening from the tag; (b) hardcoded LWC UI string → critical/hardening via `lwc-custom-labels`; (c) rule-match-no-sub-rule → group default; (d) genuine defect with no rule → `rule: none` + candidate-gap listing; (e) bare `(standard: …)` citation → rejected.
- Dogfooding before release: one review run on a real Salesforce codebase and one on a Python codebase (path-independent grades, zero fabricated ids, kind labels + Summary breakdown, offers per contract).
- Spec/plan `status:` flips to `implemented` at branch finish, not during tasks.

## Adversary findings — 2026-07-22 round 1

Dispatched on Fable 5 (prescribed tier); verdict: **blocking** — 9
Important, 5 Minor. Disposition (all applied in this revision):

1. Dead verification (backticked ids, multi-line tags, `set -e`) → tag
   grammar now states backtick-wrapping; per-file checks and the audit
   flatten tags before matching; failure counter replaces `set -e`.
2. Three unmapped ids (`apex-governor-limits`, `apex-test-coverage`,
   `flow-plan-before-build`) → added to their tables (important /
   important / minor); counts recomputed.
3. Count arithmetic (apex 8→10 with the new id, aura 10→11) → all
   counts recomputed and stated as groups + sub-rules.
4. `apex-test-mocking` whole-group critical promoted its DI/no-framework
   stances → group important + `.real-callout` critical/defect.
5. `.numbered-names` narrower than today's Minor bullet → widened to
   `.naming` (all validation-rule naming deviations).
6. `.swallowed-catch`/`.debug-only-reporting` overlap → boundary drawn
   in the sub-rule wording (debug-only-and-nothing-else = swallowed).
7. `data-model-no-hardcoded-ids` kind defect contradicted the spec's
   hardening list → changed to hardening, note records the decision.
8. Rubric copy count contradiction → constraint, Task 1 rule text, and
   glossary now sanction exactly four verbatim copies (canonical +
   contract + two standalone fallbacks); audit E compares all four.
9. Glossary/spec/plan had no carrying commit → ride-along in Task 1.
10. Rubric identity checks compared first lines only → full normalized
    extraction (`extract_rubric`).
11. Missing cross-skill duplicate-id audit → audit F extended.
12. Mixed-version window (contract 0.11.0 + pre-adoption skills) →
    degradation sentence added to the contract's Finding citations.
13. Task 7 verification grep undecidable → definition-marker grep with
    a no-output pass condition.

## Adversary findings — 2026-07-22 round 2 (verification)

Same agent, empirical test of the audit script on a synthetic corpus;
verdict: **concerns** (1 Important + 4 Minor) — 13 of 14 round-1
findings confirmed closed; finding 11's implementation was itself
broken. Disposition (all applied, no fresh round — resolution noted per
the lifecycle rule):

1. Audit F duplicate-id check selected awk field 2 (the literal `id:`
   token) — always fired, never named a real duplicate → field 3.
2. Audit F group-vs-sub while-loop was a silent no-op and the eyeball
   feed matched `.md` paths → loop deleted; eyeball fed two awk-split
   lists (dotted vs group ids); duplicates covered mechanically.
3. Task 7/9 verification expected 3 `rule: none` matches but the
   restructured fallback carries two → expectation 4.
4. DEFER checks used hard `.{60}` context (silently pass near file
   edges) → `.{0,60}`.
5. Glossary Rule tag grammar lacked the backtick-wrapping note the
   plan's regexes depend on → one-line sync.

Round-2 confirmations worth keeping: all eight expected tag counts
re-derived independently from the tables and file inventories (match);
the three previously-unmapped ids' severities sanity-checked against
their rules' prose (`apex-governor-limits` important — budget
discipline, the bulk-path catastrophe belongs to
`apex-bulkification.loop-on-trigger-path`; `apex-test-coverage`
important — the house threshold forces rework; `flow-plan-before-build`
minor — planning discipline); audit blocks A/B/C/E/G verified to catch
injected violations and pass clean content.
