---
ticket: "#10"
date: 2026-07-23
status: implemented
grilled: 2026-07-23
architect: LGTM
branch: feature/10-contract-sharpening
base: develop
---

# Review-report contract sharpening — design

## Overview

Six contract-level decisions closing the gaps that dogfooding the 0.2.0
severity-in-tag model exposed: the counting convention, single-citation
findings, a plugin-level `rule: none` form, a justify-not-critical
clause, the candidate-gap marker, and background review dispatch. All
changes live in the review-reports contract, the two `*-code-review`
skills' grading procedures, and the two review commands. No rule
content changes — new rules, sub-rules, and audit-mode semantics are
domain work tracked separately.

## Motivation

Post-#8 dogfooding (2026-07-23, seven agent runs across six real
codebases, python + salesforce) confirmed the severity-in-tag model:
zero fabricated ids, `findings:` counts matching the body in every
complete report, kind labels 100% tag-consistent, the bare-citation
failure mode closed by a direct A/B on the same code. The residual
variance is contract-level — places where two honest runs produce
incomparable reports because the contract does not regulate the choice:

- The same codebase audited twice on the same day returned counts of
  35/39/3 (per-file enumeration) vs 10/8/6 (one finding per violation
  class, cross-file `## Cross-cutting` sections bending the per-file
  layout); the second run declared its own "Counting convention"
  Summary section — the agent noticed the contract's silence.
- One finding cited two rule ids of different severities
  (Important + Minor in a single entry), another used a plural
  `rules:` key, another cited two standards at once.
- A run met findings no loaded skill's domain covers and spontaneously
  cited the plugin name: `(standard: python-standards, rule: none)` —
  a form the contract does not define.
- One run justified an Important grade on a data-integrity `rule: none`
  finding ("Not critical only because …"); another graded a comparable
  finding with no justification — only the first is auditable.
- One report annotated `rule: none` findings "candidate gap, see
  reply"; another, for the same class of findings, did not.
- Review runs block the dispatching session either way today: the
  committed commands run the review in-session end to end, and the
  dogfooded agent dispatches ran synchronously (the CLI's default),
  freezing the session for the whole run.

## Decisions

### 1. Counting convention: one finding = one rule × one file

A finding is one violated rule in one file — or at project level when
the violation is not attributable to an existing file (a missing
lockfile, an absent manifest). Every violating site is enumerated in
the finding body: line numbers, or the domain's stable key where lines
do not apply (metadata reviewed without source lines). A line-anchored
finding sorts by its first violating line, so the existing "ascending
line order" layout text is unchanged; project-level findings live in a
single canonical `## Project` section that behaves like a file section
(same severity subsections), placed first — before the per-file
sections — its findings ordered by rule id, with `rule: none` findings
last, ordered by violation-class name.
Dogfooding showed the need: two runs invented two different pseudo-file
sections for the same absent-manifest findings.

The unit is uniformly one **violation class** per file (or project
level): for tagged rules the rule id names the class; for `rule: none`
findings — where the "rule" in the pair is literally `none` — the
class is the one the candidate-gap offer names anyway, so two
unrelated uncovered concerns in one file are two findings, each with
its own severity and rerun disposition. `findings:` counts therefore
mean: the number of (violation class, file-or-project) pairs to fix.

Rationale: this is the only convention consistent with the layout the
contract already mandates (per-file sections, line-ordered findings) —
cross-file folding cannot name a file or a line, and per-instance
enumeration makes full-audit reports unreadable. On a diff review a
file rarely violates one rule at more than one site, so the convention
degenerates to per-instance naturally — one convention covers both run
shapes without a reviewer-judged "diff vs audit" switch. Codifies what
the per-file-enumeration run already did unprompted.

Accepted cost: `findings:` no longer measures violation magnitude
(three sites of one rule in one file count as 1); magnitude stays
visible in the finding body. A systemic violation across N files is N
findings — verbose but faithful; a prose pattern note in Summary is
welcome and never affects counts.

Rerun disposition (`rerun-of`) tracks sites within a finding ("lines
42, 87 fixed; 130 remaining"); a partially fixed finding counts as
**remaining** — a finding lives until its last site is fixed.

Reports are self-describing — they may live git-ignored or in an
archive outside the repo, so rerun behavior never depends on anything
unreadable from the reports themselves. When the prior report's
findings do not follow the finding unit (a pre-convention report —
readable off the report itself), the Summary disposition says so and
maps prior findings best-effort; count deltas across that boundary are
not comparable.

### 2. One finding, one citation

A finding cites exactly one rule id — singular `rule:` key; the
finding's severity is the cited rule's severity. A code location that
violates two rules yields two findings, one per (rule, file) entry,
even when both point at the same line; each gets its own severity,
kind, counter position, and rerun disposition. This generalizes the
standards-rule-tags sentence "distinct sub-rule violations at one code
location are distinct findings" from sub-rules to rules and standards;
the generalized statement is contract-owned (report level), the repo
authoring rule keeps only its sub-rule sentence.

### 3. Plugin-level `rule: none` citation

When no loaded skill's domain covers a finding, it is cited
`(standard: <plugin-name>, rule: none)` — the standards plugin itself.
At `rule: none` the citation's only job is routing the candidate gap
(which surface would receive the new rule; which repository an
upstream report targets); when no skill covers the domain, the plugin
is exactly the right granularity, because the gap may call for a new
skill, not a new rule in an existing one. A "nearest domain skill"
rule was rejected: it forces fake precision and reintroduces a
discretionary reviewer choice. The candidate-gap offer line may then
propose a new skill instead of a new rule.

This supersedes the cascade sentence "content matching no loaded
domain skill stays a Summary out-of-scope note, not a finding" in both
code-review skills. The boundary replacing it: the Run scope is given
by the dispatch (a diff or named paths) and a run never extends it.
Within that scope, a concern covered by the domain of an existing but
not-yet-loaded skill of the plugin is NOT a candidate gap — the
cascade's own instruction (load skills as the content demands) applies:
load that skill and grade by its tags. A `rule: none` citation asserts
"no rule covers this", which cannot be asserted against a skill the
run never read. Only a concern no skill of the plugin covers is a
counted plugin-level `rule: none` finding. In a mixed run the cited
plugin is the one whose domain owns the finding's file — the same
routing that assigns files to domains; a project-level finding routes
by its violation-class domain. Files outside every loaded plugin's
domain stay Summary out-of-scope notes, exactly as today.

### 4. Justify-not-critical clause

Appended to the `rule: none` grading step, after "a critical-graded
`rule: none` finding is always `kind: defect`":

> A `rule: none` finding graded below critical while touching data
> integrity, security or sharing, or a platform limit states in one
> clause why it falls short of critical.

The predicate is observable (the critical rubric's territory, not a
judgment word), and the clause doubles as a self-check: when it cannot
be written, the finding should be critical. It lives in the grading
step of the contract and both skills' cascades — the four verbatim
authoring-rubric copies stay untouched.

### 5. Candidate-gap marker: the citation is the marker

The `rule: none` citation is the report's only candidate-gap marker;
the proposals (violation class, proposed rule id, graded severity)
live in the run's reply, never in the report. Division of labor:
report = durable facts about the code; reply = ephemeral offers;
Project memory = accepted parks. A second in-report marker is a second
surface restating the same fact — the same drift class the
`## Review severities` roll-up removal eliminated, and it had already
drifted (present in one report, absent in another).

### 6. Background review dispatch

A Standards code review never blocks the dispatching session. The
convention lives in two layers with distinct audiences:

- **Both review commands** carry the instruction self-contained
  (standalone installs have no working-process rules): dispatch the
  reviewer agent in the background; the summary arrives as a task
  notification, not inline; progress via `/tasks`; report location
  unchanged.
- **The contract** adds one family-convention sentence to the existing
  dispatcher bullet: a reviewer-agent dispatch from an interactive
  session runs in the background — a review never blocks an
  interactive dispatching session; the run's owner writes the one
  report regardless of fore/background mode. This binds any future
  interactive dispatcher, not just today's two commands;
  non-interactive dispatchers (CI, automation) stay free to run
  synchronously — the contract's existing no-interactive-dispatcher
  path is untouched.

The duplication is deliberate and role-split (standalone
self-sufficiency vs family convention), not a drifting restatement.

Command-initiated runs change ownership: today both commands run the
review in-session (`mode: solo`); dispatching a reviewer agent makes
them dispatchers of `mode: agent` runs. The dispatcher duties ride in
the self-contained command text (the contract is not in the
dispatching session's context) — chiefly the pre-dispatch first-create
check for `docs/code-review/`. The check is gated on the contract
probe: it runs only when the probe finds an installed contract — in a
Standalone install the question does not exist (as both inline
fallbacks already record) and the reviewer agent creates the directory
per its fallback, unchanged. The contract owns the probe paths; the
commands carry a justified self-contained restatement of them — the
same ownership pattern as the first-create signal list. When it runs, it asks only when the
dispatcher is interactive AND no prior decision exists; a
non-interactive dispatcher keeps the contract's existing defer
behavior. After the run's task
notification arrives, the dispatching session relays the reply's
candidate-gap offers to the developer.

The declared-decision signal is promoted into the first-create
convention itself rather than special-cased here: the convention's
"decided" signals become three — a `.gitignore` of exactly `*`, a
git-tracked file under the directory, or an explicit project
instruction declaring the mode (e.g. a CLAUDE.md note that review
reports are always git-ignored). A declared ignored mode is
materialized by whoever first acts on it — writing the `*`
`.gitignore` — so the decision becomes observable and every consumer
(the process-artifacts rule included) reads the same answer; a
declared tracked mode becomes observable with the first committed
file. Ownership: the process-artifacts rule owns the operational
signal list; the glossary term mirrors it, the contract's dispatcher
bullet and the grilling-session skill reference it, and the justified
self-contained restatements are the review commands and the
project-memory core rule (which must stand without working-process) —
one definition, no fork.

## Surfaces and changes

- `plugins/working-process/rules/review-reports.md` — Layout gains the
  finding-unit definition, first-line anchoring, and the canonical
  `## Project` section for file-less findings (decision 1);
  `rerun-of` gains partially-fixed-counts-as-remaining (1);
  Finding citations gains single-citation (2), the plugin-level
  `rule: none` form (3), and the justify-not-critical clause (4);
  Candidate-gap offers gains the marker sentence and the new-skill
  proposal sentence (5, 3); the dispatcher bullet gains the background
  sentence (6).
- `plugins/python-standards/skills/python-code-review/SKILL.md` and
  `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`
  — the grading cascade mirrors decisions 3 and 4; decision 3 replaces
  the cascades' out-of-scope-note sentence ("content matching no
  loaded domain skill…") with the Run-scope boundary stated there; the
  inline standalone fallback (a strict subset of the contract) absorbs
  the finding unit and single-citation, and its Body gains the
  canonical `## Project` section (first, same severity subsections) so
  project-level findings have a defined home in standalone runs; the
  justify clause reaches the fallback through its existing step-3
  cascade reference — no second in-file copy. A standalone install is
  never laxer than a full one.
- `plugins/working-process/rules/process-artifacts.md` — the
  first-create question gains the declared-instruction signal and its
  materialization (decision 6).
- `plugins/working-process/skills/grilling-session/SKILL.md` — its
  first-create restatement becomes a reference to the
  process-artifacts signal list (decision 6, fork closure).
- `plugins/project-memory/rules/project-memory.md` — its
  observable-decision sentence gains the declared-instruction signal
  as a self-contained restatement, it owns `docs/memory/` and must
  stand without working-process (decision 6, fork closure).
- `plugins/python-standards/commands/python-review.md` and
  `plugins/salesforce-standards/commands/salesforce-review.md` —
  background dispatch with notification expectations, the solo→agent
  run-ownership change, the pre-dispatch first-create check, and the
  candidate-gap offer relay (6).

## Invariants

- The authoring rubric stays verbatim in exactly its four existing
  places; nothing here edits or restates it.
- No new report frontmatter fields; `findings:` keeps its three keys;
  existing layout sections keep their names and order (decision 1 adds
  the `## Project` section, always first).
- `.claude/rules/standards-rule-tags.md` is unchanged.
- Inline fallbacks remain strict subsets of the contract — never a
  different shape.

## Review rounds

Architect round 1 (2026-07-23, Fable 5): **blocking** — four findings,
all amended in place: (F1) decision 3 now names the superseded cascade
sentence and states the Run-scope boundary (the scope is given by the
dispatch, never self-extended); (F2) decision 6 now states the
commands' solo→agent run-ownership change, the pre-dispatch
first-create check with its ask-conditions (observable signals and
explicit project guidance both count as decided; non-interactive
dispatchers defer), and the candidate-gap offer relay; (F3) the
`## Project` section is placed first and the layout invariant
reworded; (F4) the background-dispatch convention is scoped to
interactive dispatching sessions.

Architect round 2 (2026-07-23, Fable 5): **blocking** — four findings,
all amended in place: (F1) the round-1 "existing but unloaded skill"
citation branch dropped — a concern an existing skill's domain covers
loads that skill and re-enters the cascade; `rule: none` is never
asserted against an unread skill; (F2) the counting unit stated
uniformly as one violation class per file — the rule id names the
class for tagged rules, the candidate-gap class names it at
`rule: none`; glossary Finding term mirrored; (F3) the
declared-instruction signal promoted into the first-create convention
itself (glossary term, process-artifacts rule, contract dispatcher
bullet — one definition) with materialization semantics, instead of a
command-local special case; (F4) the justify-not-critical predicate
regains "or sharing".

Architect round 3 (2026-07-23, Fable 5): **concerns** — one Important,
four Minor, all amended in place (2026-07-24): (F1) the command's
pre-dispatch first-create check is gated on the contract probe —
Standalone installs keep no-question behavior, the fallback sentence
stays true; (F2) `## Project` ordering gains the `rule: none` tiebreak
(last, by violation-class name); (F3) the justify clause reaches the
inline fallback via its existing step-3 reference instead of a second
in-file copy; (F4) signal-list ownership stated — process-artifacts
rule owns, glossary mirrors, contract references, commands carry the
one self-contained restatement; (F5) `ticket: none` is deliberate —
this spec awaits its own ticket (created after this review cycle);
the stale `feature/8` branch context of the worktree does not source
it.

Architect round 4 (2026-07-24, Fable 5): **LGTM** — three Minor
edge-closure suggestions, applied same day: mixed-run routing for the
plugin-level citation (the plugin whose domain owns the finding's
file; project-level routes by violation-class domain), the inline
fallback Body gains the `## Project` section, and probe-path ownership
stated (contract owns, commands carry the justified self-contained
restatement).

Post-LGTM amendments (2026-07-24, from plan-adversary round 2, no new
decisions): the signal-list fork closure named its two remaining
restatement surfaces (grilling-session → reference; project-memory
core rule → self-contained restatement, and the ownership sentence
now lists both exceptions); the fallback `## Project` section
explicitly keeps the same severity subsections; the glossary Contract
probe term gains dispatching review commands as probe runners; the
empirical check requires a sync-rules update of the installed
contract first (drift is content-hash, not plugin-version) and a
command-launched run.

## Out of scope

Rule content of any kind: new rules (SOQL injection, dangerous
grants), candidate sub-rules surfaced by dogfooding, audit-mode
semantics, sub-rule boundary changes, README provenance wording,
writing-skills compliance edits — tracked in #6 (salesforce) and the
skills-rework backlog.

## Versioning and validation

- No version bumps on this branch: per the plugin-versioning rule,
  bumps happen once, in the develop→master release PR, sized by each
  plugin's total accumulated change since the last release. For the
  changes specified here the expected size is minor for all three
  touched plugins (backward-compatible contract additions; cascade and
  command changes) — the release PR decides the final numbers.
- Dogfooding from this branch mints the `-dev.10` prerelease on each
  plugin whose content it loads (e.g. `0.11.0-dev.10`); the suffix
  flows into develop and is stripped by the release PR.
- `claude plugin validate .` and per-plugin validation pass.
- Empirical check: a dogfooding rerun on a previously reviewed
  codebase produces counts with the decision-1 semantics and a
  disposition comparable to its prior report.
