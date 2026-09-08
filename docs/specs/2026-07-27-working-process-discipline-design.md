---
ticket: none
date: 2026-07-27
status: draft
branch: feature/wp-process-discipline
base: develop
---

# Working-process discipline — design

## Overview

Five process changes drawn from the Private-memory backlog. Four land in
the `working-process` rules and agents; one — the
`marketplace-plan-review` checklist of decision 5 — lives at repo level,
for the domain this repository's own plans touch:

1. the **implementation-start gate** for committing process documents;
2. **branch-closeout offers** — a code review and a Project memory
   review, both offered while the integration decision is still open;
3. **background dispatch** for the architect and plan-adversary agents;
4. two **author duties** discharged before the adversary round;
5. the **`marketplace-plan-review`** checklist skill.

Every change is a text edit to an existing surface: no new rule file (the
Rules payload stays five files), no new plugin component, no change to
the report contract. Multi-domain review dispatch and the generic
reviewer — designed alongside these and split out on the architect
session's recommendation — live in
`docs/specs/2026-07-28-multi-domain-code-review-design.md`. No version
bump on the topic branch; the release PR sizes it.

## Motivation

**The commit-timing clause is too loose.** `spec-plan-lifecycle` says
to suggest committing the work's documents "when implementation is
about to start" — wide enough to read as "any time before code", which
is how documents ended up committed mid-authoring (Private-memory
session, 2026-07-20). The gate the developer actually wants has two
conditions, and neither is "the plan looks finished".

**The flow has no closeout.** It ends at step 6, Implementation.
Nothing offers a code review of what was just built, and nothing offers
to close out the Project-memory notes the work accumulated. The
obvious-looking hook — `status: implemented` — does not work here: in
this project that stamp often lands only after the PR merges, so an
offer made there arrives after the integration decision it was supposed
to inform, and after the branch where the fixes belong is gone.

**Verdict rounds still freeze the session.** #10 proved background
dispatch end-to-end for review runs: 9-to-31-minute runs with the
developer working throughout, the summary arriving as a task
notification and nothing lost. Architect and adversary rounds have the
same shape — long, self-contained, one verdict at the end — and today
block the session that dispatches them.

**Plan authoring wastes adversary rounds.** The #10 plan took three
rounds (blocking, blocking, concerns) and 17 findings, recorded in that
plan's Review rounds section. Zero were against design decisions; all
were against execution precision, and round 1 was avoidable: the plan's
verification greps were written as single-line matches against text the
plan itself wrapped across line breaks, and were never executed;
ownership claims ("X owns this", "no fork") were enumerated from memory
instead of `rg`, missing two live restatement surfaces.

That failure mode reproduced while authoring *this* spec. Enumerating
the consumers of a phrase this change edits, a fixed-string `rg` for
``notes and `INDEX.md` `` returned `ticket-frontmatter.md` but not
`process-artifacts.md` — which carries the phrase with a line break
inside it. A `-U` multiline retry found both. The class of bug the
duties below prevent cost a false-negative consumer list in the very
work that adds them.

**The adversary has no checklist for this repo's domain.** During #10
it scanned for a `*-plan-review` match, found none, and worked from an
ad-hoc dispatch prompt. Seven of the 17 findings turned on knowledge
that exists only here: that a Rules payload is read from the installed
rule file and not the plugin cache (so a dogfooding gate verifying the
cache misattributes failures); that pass criteria can be vacuously
satisfied by a target which never exercises the new paths; that a rerun
must launch through the real surface; that `description:` fields carry
invoker chains; that conditional references degrade under a Standalone
install; that a restatement dropping one clause lets the standalone
shape drift; that changing who performs an act obliges a glossary
update.

## Decisions

### 1. The implementation-start gate

`spec-plan-lifecycle`'s final paragraph is replaced. Proposed wording:

> Suggest committing the work's documents under `docs/` only at the
> implementation-start gate: the developer has decided that
> implementation begins. Authoring is never that moment — not while a
> spec is drafted, not between review rounds, not while the plan is
> written. The suggestion never becomes the act: this rule governs when
> committing may be *suggested*, never whether it may happen, and an
> open gate authorizes nothing. Only paths git tracks or would track;
> deliberately ignored documents are skipped silently.

The prohibition on authoring-time suggestions is stated rather than left
implied by "only": it is the behavior the change exists to stop, and an
implication is not greppable.

The gate carries **one** condition, deliberately. The developer's intent
was two — the decision to start plus commit authorization — and the
substance of the second is kept, as an absolute constraint on the act
rather than a condition on the suggestion. The reason is that
`working-process` defines no observable signal for "authorized", while
its sibling clauses are built on signals that are checkable (the
first-create question turns on a `.gitignore` containing exactly `*`, a
git-tracked file, or a declared instruction). The rule that governs
commit authorization lives outside this plugin — in the developer's own
environment — so a distributed rule naming it as a gate condition would
hand every other consumer an untestable term, which reads as an escape
hatch. Phrasing it as "this rule never authorizes; authorization is never
inferred" is the stronger of the two forms: it binds the act
unconditionally instead of binding the suggestion conditionally.

### 2. Branch closeout owns both offers — `workflow.md` step 7

> 7. **Implementation → branch closeout.** When implementation on the
>    topic branch is complete and the integration decision is still
>    open — where superpowers:finishing-a-development-branch runs, when
>    available — offer, each independently:
>    - a code review, naming each available `*-code-review` skill whose
>      domain the changed files touch — plugin-provided or project-level
>      alike, discovery mirroring the `*-plan-review` convention; the
>      dispatch mechanics stay with their owners, this step only makes
>      the offer;
>    - a Project memory review, when `memory-review-session` is
>      available and the project keeps a store (`docs/memory/INDEX.md`
>      or `.claude/memory/INDEX.md` — no store, no offer).
>
>    The hook is branch completion, not the `status: implemented` stamp:
>    that stamp often lands after the PR merges, too late to act on
>    either offer.

Three consequences worth stating:

- **One owner.** Step 7 is the only surface that makes these offers.
  `spec-plan-lifecycle`'s "Lifecycle offers" paragraph gains nothing —
  not even a pointer — because a second mention of a branch-time offer
  in a document-lifecycle rule is exactly the fork #10 spent a round
  removing.
- **The memory-review offer moves off the `implemented` hook** its
  backlog entry proposed, for the same reason as the code review, and
  because one closeout conversation beats two.
- **No project-memory edit.** `memory-review-session` stays
  explicit-ask-only; an offer the developer accepts *is* the explicit
  ask. Recorded here so a later reader does not mistake step 7 for a
  second trigger on that skill.

The store probe copies the candidate-gap offer's probe in
`review-reports` — the same two paths, the same no-store-no-offer rule.

### 3. Background dispatch for both verdict agents

`workflow.md` gains a paragraph beside the existing model-selection one,
which already governs "these dispatches"; steps 3 and 5 are untouched,
so the statement has one home:

> Dispatch mode for these reviews: always in the background — the
> dispatching session stays interactive, and the verdict arrives as a
> task notification the dispatcher relays when it lands. The step the
> verdict gates still waits for it: background dispatch buys the
> developer's time back, not a reordered flow — a plan is not written
> while the architect round runs, and implementation does not start
> while the adversary round runs. Stamping happens after the relay,
> never before: the self-reported model is compared against the
> dispatched and prescribed tiers at that point.

The gate is deliberately preserved. Writing a plan against a design the
architect may reject wastes exactly the work the round exists to
prevent; what background dispatch recovers is the developer's time, not
the process's ordering.

**A round in flight is recorded before it starts.** Background dispatch
opens a hole synchronous dispatch did not have: the verdict lives only in
the notification, and a session that ends before the relay takes the
round with it — the verdict agents write nothing, by design. So
`spec-plan-lifecycle` gains a pending marker, exactly as it already
carries one for grilling (`grilled: grilling`):

- the dispatcher stamps `architect: dispatched` / `adversary: dispatched`
  BEFORE dispatching, and the relayed verdict replaces it. This is not a
  verdict stamp and does not weaken the after-the-relay rule above: it
  records that a round is owed, never its outcome;
- the value set of both fields therefore extends to
  `dispatched | LGTM | concerns | blocking`, with `dispatched` documented
  as the in-flight marker;
- unfinished process work stays greppable — the rule's own promise —
  with one more pattern beside the existing two:
  `rg -l '^(architect|adversary): dispatched$' docs/`;
- a fresh dispatch overwrites the marker; a round the developer abandons
  is cleared by removing the field, the same explicit act that resolves
  any other pending marker;
- one existing sentence of the same rule is a consumer and must move with
  it: "`grilled`, `architect`, and `adversary` appear only once the
  corresponding step has run" becomes true of the step having *started*
  for the two verdict fields.

The findings of a lost round are still lost — recovering those would mean
a durable round artifact written by the agent, which is a new artifact
kind (location, frontmatter, directory mode, lifecycle) and belongs to
its own work. What this decision refuses is the silent version, where an
interrupted round leaves the document indistinguishable from one never
reviewed.

Both agents' `description:` fields note that they are dispatched in the
background and that the verdict arrives as a task notification, and each
`## Stamping` section gains one clause: the dispatcher stamps after
relaying the run's reply. The cap-refusal flow is unaffected — a refusal
happens at dispatch time, while the session is still there to be asked.

`grilling-session` and `architect-session` are in-session consultations
with no verdict and no dispatch; they are out of this decision.

### 4. Author duties before the adversary round — `workflow.md` step 4

> 4. **Spec → plan.** Write the implementation plan with
>    superpowers:writing-plans when available; plans live in
>    `docs/plans/`. Before the adversary round, the author verifies the
>    plan against itself:
>    - every verification command the plan names is RUN against the text
>      it is meant to match — the plan's replacement texts written to
>      scratchpad files outside version control first, never into the
>      repository, whose tree stays clean and whose Process directories
>      stay undisturbed — and fixed where it misses; a command that has
>      never been executed is not a verification step;
>    - every ownership claim ("X owns this", "supersedes", "no fork")
>      carries a whole-repo `rg` result for the superseded phrase,
>      quoted in the plan — never a recollection.

Both duties are domain-agnostic: any plan that names a check can execute
it first, and any plan that claims sole ownership of a statement can
enumerate the alternatives. They sit in the flow step that produces the
plan, not in the checklist that reviews it — the point is to spend the
author's cheap minute instead of the reviewer's expensive round.

### 5. `marketplace-plan-review` at repo level

`.claude/skills/marketplace-plan-review/SKILL.md`, shaped like
`python-plan-review`: frontmatter `name` and `description` ending
"invoked by the plan-adversary agent", then dimensions carrying their
own severities, each finding citing a plan quote or file path.

Dimensions, each drawn from a #10 finding rather than invented:

1. **Rules payload and drift** — a plan that changes rule content
   verifies the *installed* rule file, not the plugin cache; content-hash
   sync and the SessionStart drift nudge are accounted for.
2. **Dogfooding gate design** — pass criteria cannot be vacuously
   satisfied; the target must exercise the new paths; runs launch through
   the real surface (the command, not a hand-rolled dispatch); every
   changed surface is exercised at least once.
3. **Version channels** — no bumps on topic branches; dogfooding
   unreleased content needs `-dev.<issue>` because the plugin cache keys
   by version; prerelease grammar respected.
4. **Restatement and conditional-reference discipline** — restatements
   carry the full clause; `description:` invoker chains stay accurate;
   conditional references degrade correctly under a Standalone install;
   the authoring rubric appears only where its owning rule permits, and
   the checklist cites that rule for the count instead of restating it —
   a second statement of the same arithmetic is the very fork the rule
   forbids.
5. **Glossary and ADR upkeep** — a plan that changes who performs an act,
   or introduces a term, updates `docs/domain/glossary.md`.
6. **Commit and hygiene rules** — one-line conventional-commit subjects;
   no machine paths, no company names, English only.

The name is kept as the backlog entry wrote it. The prefix names this
marketplace as the domain; the alternative considered and rejected was
`plugin-authoring-plan-review`, which describes the work more narrowly
than the checklist's dimensions do (channels, catalog sync and hygiene
are marketplace-level, not per-plugin).

The skill lives at repo level, next to the `.claude/rules/` files whose
conventions it checks, so consumers of `working-process` in other
repositories do not receive a checklist about this marketplace.

**One assumption to verify, not assume:** that a dispatched
`plan-adversary` — a subagent — actually discovers project-level skills
in `.claude/skills/` when it scans for `*-plan-review`. If it does not,
the dispatch prompt names the checklist path explicitly. The plan owns
this as a named check with both outcomes handled; nothing here depends
on the discovery working.

## Surfaces and changes

| Surface | Change |
| --- | --- |
| `rules/workflow.md` | step 4 author duties; new step 7; new dispatch-mode paragraph |
| `rules/spec-plan-lifecycle.md` | final paragraph replaced by the implementation-start gate; `dispatched` added to both verdict fields' value set, its frontmatter example and the unfinished-work greps |
| `rules/process-artifacts.md` | `ARCHIVE.md` added to the registry-file exemption |
| `rules/ticket-frontmatter.md` | `ARCHIVE.md` added to the Project-memory bullet |
| `agents/architect.md` | `description:` dispatch mode; stamping-after-relay clause |
| `agents/plan-adversary.md` | same two edits |
| `plugins/working-process/README.md` | architect and plan-adversary bullets and the Model selection section note background dispatch |
| `.claude/skills/marketplace-plan-review/SKILL.md` | new file |
| `.claude/rules/plugin-authoring.md` | one line pointing at the new checklist (reference, not restatement) |

`ARCHIVE.md` rides along because both enumerations read as closed lists
that omit it while the exemption already holds by delegation — a
one-line clarification each, flagged by the Fable architect re-review of
2026-07-22.

No plugin component is added or renamed, so the three component
enumerations the marketplace-sync rule keeps in step — the manifest's
`description`, the catalog entry, and the root README row — stay
untouched. They are named here because the companion spec does add
components and must edit all three.

Also unchanged and deliberately so: `rules/review-reports.md` (its
background wording is about review runs, a different subject from a
verdict agent's dispatch mode, and this spec adds no report semantics);
both standards plugins and their READMEs (`*-plan-review` discovery is
unaffected); `ARCHITECT_PERSONA.md`; and every project-memory surface.

## Invariants

- Every step in the flow stays an offer the developer may decline.
- One statement, one owner: step 7 owns the closeout offers; the
  dispatch-mode paragraph owns background dispatch; the agents' bodies
  carry only the stamping clause.
- A declined offer is never repeated uninvited — every step of the flow
  offers, and none nags.
- The Rules payload stays five files, so the README's count stays true.
- No behavior depends on a check that has not been run — the duties in
  decision 4 bind this work's own plan.

Candidate glossary terms for the grilling session, not decided here:
**branch closeout** (implementation complete on the topic branch,
integration decision still open), **implementation-start gate**,
**author duty**, **round in flight** (a dispatched review round whose
verdict has not been relayed, marked `dispatched`).

## Out of scope

- **Multi-domain review dispatch and the generic reviewer.** Designed in
  the same session and split out on the architect session's
  recommendation (2026-07-28): they add two plugin components, two report
  contract additions and two canonical-term changes, which would make
  five cheap text edits hostage to the release's riskiest part. They live
  in `docs/specs/2026-07-28-multi-domain-code-review-design.md`. Step 7's
  offer needs no change when they land — only what the offer dispatches
  does.
- The **finding router** (review → local fix / plan / spec seed) stays
  parked in Private memory: what to *do* with findings — fix locally,
  plan a sweep, or seed a spec — is its own design problem with its own
  provenance requirements.
- Encoding a verification or smoke-test step in the flow. Step 7 says
  "before the integration decision" and claims no ordering against
  project-specific verification.
- A new rule file for plan authoring.
- Ticket numbers: the authoring session had no network access to the
  issue tracker, so this spec carries `ticket: none` and the branch is
  `feature/wp-process-discipline`. Both are backfilled per
  `ticket-frontmatter`'s backfill clause once an issue exists; the branch
  is renamed to `feature/<issue>-wp-process-discipline` at that point.

## Versioning and validation

No version bump on the topic branch (plugin-versioning rule). The
accumulated change is **minor** for `working-process` — a new flow step,
a new paragraph and added author duties, all backward-compatible — sized
in the release PR.

Every change here is rule and agent text, so nothing in this spec can be
falsified by running code; what can be checked is that each edit lands
where it is meant to and forks nothing. Validation is therefore the
adversary round plus the plan's own named checks: per-phrase `rg -c`
verifications executed against the final text (decision 4's first duty
applied to this work's own plan), the whole-repo `rg` consumer lists
behind every ownership claim (its second duty), and the
checklist-discovery probe of decision 5, whose two outcomes are both
handled.

A dogfooding round would still be the only way to see the new offers
fire in a live session. It runs against the *installed* payload, which
the plugin cache keys by version, so it needs a `-dev.<issue>` string and
waits for an issue number — and it is worth one round precisely because
step 7 fires at a moment (branch complete, integration open) that no
grep can observe.

After the rule edits, installed copies emit the SessionStart drift nudge
until re-synced. That is the engine working, not a regression.
