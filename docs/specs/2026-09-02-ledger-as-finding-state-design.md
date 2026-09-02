---
ticket: none
date: 2026-09-02
status: draft
grilled: 2026-09-02
architect: concerns (resolved 2026-09-02)
integrity: 2026-09-02 (sha: bf41005)
revises: [./2026-08-17-autonomous-review-loop-design.md, ./2026-08-31-review-loop-errata-wave-one.md]
branch: feature/audit-errata
base: develop
---

# The disposition ledger as finding state

## Problem

An integrity audit of the autonomous review loop proved eleven defects.
Wave one closed the contradictions that made shipped rules disagree with
themselves. Five stayed open as one cluster, because they share a cause:
the ledger keeps needing tokens for paths nobody anticipated.

The cause is structural. **The grammar encodes the path in the state
token.** `fixed` means the session acted; `resolved` means a held
question closed. Add a path — the developer present in the round, ruling
without anything ever being held — and the grammar needs a fourth token,
then a fifth. Practice has already taken that path. Every `resolved`
line in wave one's record closes a `held` line nobody wrote, and two
`resolved (declined)` lines record a transition the grammar does not
define at all.

A second assumption is wrong in the same way. The grammar treats the
developer as asynchronous, reachable only through `held`. The loop runs
with the developer in the conversation.

## What this design is

The state machine is over **one finding**, not over the loop. Three
levels the shipped grammar conflates:

- a **round heading** records one dispatch and never changes;
- a **disposition line** carries the mutable state of one finding;
- a **gate line** carries the state of one hit — a smaller machine
  sharing the container and one clause, `counter:`, but neither the
  state set nor the graded and licensed slots a disposition line
  carries.

Loop state proper — the round count, the all-Minor signal, the
diff-scoped chain — is derived by folding the headings. It is stored
nowhere, and this design stores it nowhere.

## The states

Four, replacing five.

    - open — [<Severity>] <claim>
    - held — [<Severity>] <claim>; question: <one closed question>; options: <the options and the session's recommendation>
    - fixed <date> — [<Severity>] <claim>; <authorizer>; <what changed>
    - declined <date> — [<Severity>] <claim>; <authorizer>; <why the document stands>

The severity bracket is omitted on a line whose sole authorizer is
`ruling:` **and** which no reviewer graded — both legs, never one, as
below:

    - fixed <date> — <claim>; ruling: <date>; <what changed>

`open` and `held` are the non-terminal states, and the only two the
Unfinished-work list anchors. `fixed` and `declined` are terminal and
say what became of the document: it changed, or it stands.

The two dates on a terminal line record different events and are both
written even when they coincide. The leading date is when the line
reached its terminal state; `ruling:` is when the decision it cites was
taken. On an ordinary developer-authorized line the two are the same
day and say so; on a fold they differ, and that divergence is the point
of carrying both.

The severity slot is a reviewer's grade, so it is omitted exactly where
there is none: a line whose sole authorizer is `ruling:` and which no
reviewer graded — a change the developer directed mid-round — carries
its claim with no bracket at all. This is not a fourth severity value;
the glossary's three stand. It is the recognition that a developer's
instruction is not a finding, and that inventing a grade for it would be
the same manufacture the authorizer rule forbids.

`fixed` and `resolved` merge because they were never two states. Both
mean the document changed on account of this finding; they differed only
in who authorized the change, which is now a clause. Merging also frees
a word the rules currently use for two objects — `concerns (resolved
<date>)` annotates a verdict, while `resolved <date>` annotated a
finding.

## The clauses

The leading token is a queryable state. Clauses are payload.

| clause | carries | on |
|---|---|---|
| `license: <citation>` | the written decision the session acted on | `fixed` |
| `ruling: <date>` | the developer authorized it; on a fold, the prior ruling's date followed by `folding <section or line quote>` naming what it folds against | `fixed`, `declined` |
| `question:` | the question, phrased so one short answer resolves it | `held` |
| `options:` | the options and the session's recommendation | `held` |
| `counter:` | the session's evidence where the finding is disputed or contested | `held` |
| `deviation: <section>` | where the rationale for departing from a reviewer's suggestion lives | `fixed` |

`question:` and `options:` are both required on a `held` line: the batch
that relays them is a transcript, and a session that dies between the
relay and the answer leaves the next session to re-derive the options —
possibly differently, so the developer answers a question that silently
changed. `counter:` and `deviation:` are conditional, written whenever
their condition holds.

Every terminal line carries exactly one authorizer, `license:` or
`ruling:`. A `declined` line always carries `ruling:`: declining is a
decision, and triage gives a session no license to decide.

Payload costs nothing structurally. Four of the five Unfinished-work
commands anchor a frontmatter field and are held to the frontmatter
block by the list's default scope guard, so no body line reaches them at
all; the fifth is the ledger's own, anchored on `^- `, which an indented
continuation does not match. Payload under a line is therefore invisible
to every published command, and where it runs long it belongs in
indented sub-bullets rather than in a longer line.

## What the authorizer buys

Two shipped rules discriminate on the token today, and they do opposite
things: the oscillation tripwire escalates a finding re-raised against a
`fixed` line, and the relitigation clause folds one re-raised against a
`resolved` line. Merging the tokens would collapse that distinction, so
both move to the clause:

- re-raised against `license:` — two readings of one license, a
  contested reading, escalates as held with the flip named;
- re-raised against `ruling:` **without new evidence** — a recorded
  developer decision, folded and cited, never asked again;
- re-raised against `ruling:` **with new evidence** — `held`, its
  `counter:` citing the prior ruling. A session that folded this
  autonomously would be arbitrating between a reviewer and a recorded
  developer decision, which the workflow rule forbids it to do.

Evidence is new relative to what the folded line records — its claim and
the reasoning its clauses carry — not relative to the reviewer's wording.
A session that cannot tell holds rather than folds, since triage already
says a finding that could go either way is a decision, and a wrong
not-new call performs the arbitration this split exists to prevent.

This is stronger than what it replaces. Today both rules key on a proxy:
`resolved` happens to imply the developer. After the change the
predicate says what it means.

**A fold produces a line like any other disposition.** An evidence-free
re-raise is still a finding of its round, so it takes
`declined <date>` — the document stands — carrying `ruling:` with the
**prior** ruling's date and a `folding` citation of the line it folds
against. The
authorizer is cited rather than fresh, and the line says so; a session
never manufactures an authorization that did not happen. Without this
the fold has no honest production, since no developer ruled on the new
finding and `declined` admits no other authorizer — the same shape as
the audit's first defect, which this design exists to cure.

The fold is a safety net, not the primary mechanism. A reviewer is a
stateless one-shot dispatch, so it cannot remember what earlier rounds
settled — which is why the shipped rule says state prevents
relitigation, not the reviewer's memory.

## What a diff-scoped round may read

Diff-scoping forbids re-reviewing the document beyond the diff, and the
ledger is part of the document — so the reviewer has been formally cut
off from the one section recording what the developer already decided.
That is the cause of the re-raises the fold exists to absorb, and it is
cheaper to fix at the source.

**The ledger is always in scope for a diff-scoped round as context,
never as a review target.** What that protects is narrow and deliberate:

- **Settled lines** — those carrying `ruling:` — may be re-raised only
  with new evidence, which routes to `held` rather than to a fold.
  They are the developer's decisions. Historical lines written before
  this design, including `resolved <date> (declined)`, carry no
  authorizer clause and are settled by their token alone; a fold against
  one cites the date on that token, which is when the developer decided.
- **`held` lines** carry questions already put, so a round does not
  duplicate one.
- **Session fixes** — `fixed` lines carrying `license:` — get no
  protection at all. The previous round's are the diff and are named as
  the first thing to attack; older ones are simply unprotected. A
  reviewer told not to re-raise a fix would lose the property
  diff-scoping was adopted for, since repair-born defects are the
  dominant late-round class.

Narrative prose between the lines of a `## Review rounds` section is
lawful and expected. The grammar governs headings, lines and their
indented payload; a paragraph explaining why a wave went the way it did
belongs there too, and every reason this loop found worth keeping was
written as one. A lint over this section reads the anchored lines and
ignores the prose.

The reviewer learns what it may not reopen, never what it may not find.
Naming the section rather than copying its lines keeps the brief from
growing with the round count, and follows the same
point-at-files-rather-than-paste discipline the workflow rule already
applies to consultations.

## Write-ahead

**Each disposition line is written before the edit it describes, or with
it — never batched at the end of a wave.**

The dangerous failure is not a session dying mid-round; it is a fix wave
half-applied with no lines written. The body has changed, nothing says
which change belongs to which finding, and the next round's brief reads
a diff source that is silently wrong. Writing contemporaneously makes a
partial wave self-evident: `open` and `fixed` lines mixed under one
heading say exactly where the session stopped.

This costs no notation. The rule already prescribes `open` at stamp
time; this extends the same discipline to every later transition.

## The cap is best-effort

The round cap guards spend, not correctness, and it survives no
compaction — the count is derived from headings, but the reset event is
not recorded anywhere.

**Developer contact is a message from the developer.** Not a relay they
read, not an escalation the session sent, not an unanswered batch. That
matches what unattended means, and it needs no notation.

**A session that cannot count its own rounds escalates rather than
assuming.** Resetting to zero after a compaction fails in the wrong
direction: a long session could grant itself three fresh rounds after
every compaction. Treating a lost count as its own reason to ask costs
nothing and bounds the spend the cap exists to bound.

## Gate lines

The two shapes stand. One stated reason does not: the rule claims the
date tells a gate episode apart from the round's own findings, and wave
one's own record disproves it — three `hit fixed 2026-09-01` lines sit
beside six `resolved 2026-09-01` disposition lines under one heading, and
two episodes share the date 2026-08-31. **The `hit` token is the
discriminator.** A wrong stated reason invites a later session to
correct the right practice, so the sentence is replaced rather than
dropped — and only its date claim is. The same sentence concludes that
a gate never mints a heading of its own, which stands on the round
heading's grammar being closed, a reason the date never carried.

## What this does not build

Each refusal is recorded with its reason, so a later wave reopens it
with evidence rather than by taste.

- **No `hit outstanding` token.** A hit is mechanically re-derivable:
  the next gate episode regenerates it for the price of the cheapest
  agent in the system. A lost finding is gone forever; a lost hit is
  not. The state has also never occurred, and minting it would
  contradict the glossary's **Hit** entry, the one that calls a hit
  binary, and would force a second widening of **Audit agent**, whose
  bar enumerates exactly two dispositions.
- **No `why:` clause on `held`.** Its value is drawn from a closed
  four-way set — no license, a contradiction between decisions, a
  disputed finding, or one that could go either way — which the
  `question:` phrasing already carries.
- **No episode identity for gates.** One consumer needs it
  operationally — the re-dispatch bound's counter, and only across
  session loss — at a cost of at most two dispatches on the cheapest
  family. A second consumer emerged while this document was being
  written: a reader reconstructing which episode produced which line,
  who without it can draw a false conclusion from the record, as the
  closing section documents. The refusal stands on the operational
  price; the legibility price is now measured rather than assumed, and
  is what a later wave should weigh when reopening this.
- **No structured block, sidecar file, or git as the diff source.** An
  LLM hand-writes this record either way, so structure buys checkability
  the writer's nature does not deliver; and the lifecycle rule keeps
  these documents uncommitted through the rounds on purpose.

## The blocking terminator loses its self-fix prohibition

`blocking` keeps its meaning — autonomy suspended, no further round
without the developer — and drops the clause forbidding self-fixes.

The prohibition's own rationale is about findings, while the
prohibition is stated on the verdict. **A design reshape has no citable
license by construction, so triage already holds it.** Wave one's round
1 is the evidence: five wording and consistency fixes, every one with a
clean citation, none a reshape, all forbidden only because the
reviewer's grade read `blocking`.

## Severity casing

Every severity slot in this repo capitalizes, and none is lower case,
against a glossary that fixed `critical | important | minor` in lower
case. No count is stated here on purpose: a ledger grows every round, so
any repo-wide number is falsified by the next line written — this
document's own round-2 report proved it, on a figure the previous commit
had invalidated while writing it. The grilling settled
it in the glossary rather than here: the value is canonical as a word,
and its casing follows the syntax it sits in — lower case as a rule
tag's field value, capitalized in the ledger's bracket slot. One
concept, two syntaxes, two rendering conventions, and no migration.

This design therefore states no casing rule of its own; it cites the
**Severity** entry. Deferring the question to a lint would have made the
lint's first act the condemnation of every committed line.

## Changes by file

- `plugins/working-process/rules/spec-plan-lifecycle.md` — the four
  states and their shapes, the clause table, the authorizer rule, the
  write-ahead sentence, the corrected gate discriminator, the refusals,
  the relitigation clause rekeyed to `ruling:`, the sentence recording
  that pre-merge ledger lines stay as written, the retained historical
  `resolved` shapes, the lawfulness of narrative prose between ledger
  lines, and — from "What a diff-scoped round may read" — its grammar
  half: that a pre-design line is settled by its token alone and that a
  fold cites the date on it. Two further sites the grilling found: the Unfinished-work section says a ledger close is
  `open` or `held` becoming `resolved <date>`, which the merge makes
  `fixed <date>` or `declined <date>`; and two sentences call the
  list's own entry a "review-loop ledger entry", a phrase the glossary
  now bans as a name for a disposition line, so both read
  "review-loop entry" instead.
- `plugins/working-process/rules/workflow.md` — the oscillation tripwire
  rekeyed to `license:`, the `blocking` terminator's prohibition
  deleted, and the cap's contact definition with its cannot-count
  escalation. From "What a diff-scoped round may read" it takes the
  reviewer's behaviour: the ledger's permanent place in a diff-scoped
  round's context, the three protection tiers, and the base against
  which evidence counts as new. The split follows the two rules' own
  division — workflow says what a round does, the lifecycle rule says
  what the record is — so the grammar half of that section goes below
  rather than here.
- `docs/domain/glossary.md` — already changed by the grilling, not by
  the implementation: six new terms (**Adjudication** and **Ruling** as
  a level-distinguishing pair; **Disposition ledger**, **Round
  heading**, **Disposition line** and **Gate line** for the structure
  the loop had been naming without defining), plus a **Severity**
  sentence putting casing under the syntax each value sits in. Round 1
  added one more: **Ruling** admits a cited earlier ruling, which is
  what makes a fold expressible. The refusal of `hit outstanding` is
  what keeps **Hit** binary.
- `docs/specs/2026-08-31-review-loop-errata-wave-one.md` — its bare
  `- dismissed 2026-08-31` line takes the `hit dismissed` shape the
  grammar defines.

Historical ledger lines stay as written, with one sentence recording
that they predate the merge, as the `scope` token's introduction already
established. The shipped `resolved <date>` and `resolved <date>
(declined)` shapes are kept in the rule as described historical forms
rather than deleted: a reader must still parse pre-merge documents, and
a fold against a pre-design settled line cites a date off a token the
live grammar no longer produces. The bare `- dismissed 2026-08-31` line above is the one
exception, and for a different reason: it is not a line the merge
remaps but a line that never matched any shape, written before the
`hit dismissed` shape existed. Normalizing it to a shape its own wave
later defined is not a rewrite under the merge. That edit records
itself where it happens: a gate line in wave one's own ledger, under
its last round heading. Wave one carries an adjudicated verdict, and
editing a stamped document's body without a trace there is the thing
wave one itself refused to do.

Merging a published token narrows a shipped convention, so the release
carrying this takes a minor bump.

## Seams this does not close

- **The glossary has no owner on the fix-wave path.** Three collisions
  in wave one, and a fourth arrived during this design's own
  consultation. The candidates are a triage duty — a `fixed` line whose
  license is a glossary term, or whose change moves a term's meaning,
  owes a glossary check — or a standing enumeration target for the
  propagation gate, which reaches only the quoting case.
- **A stop signal cannot bind text written after it was given.** New
  design written after a stop signal should re-arm review rather than
  override it, and the signal should be scoped to the text it read.
- **A plan's owed confirming round has no Unfinished-work entry.** The
  workflow rule calls the diff-scoped LGTM heading a durable marker and
  prescribes a recovery reading, but no command matches it, so
  `process-status` reports clean while a confirming round is owed.
- **Concurrent waves on one document are undetected and unsupported.**
  The store is an uncommitted file, and the one-live-round rule is
  scoped within a session. Declaring the limit is cheap; engineering
  around it is not.
- **The deferred grammar lint.** Roughly half of this design becomes
  mechanically checkable if it ships and stays convention if it does
  not.
- **Is a plan's confirming round autonomous, and does it count against
  the cap?** Wave one routed the audit's implementer question 3 here.
  Its missing-anchor half is the seam above; this half is a decision
  about the loop's authority, not about the ledger, so it stays open
  rather than being answered in passing by a document about record
  shapes.
- **Per-round commits, with a named trigger.** The lifecycle rule
  suggests committing only at the implementation-ready gate, while
  allowing the developer to commit sooner on their own call. If a loop
  starts committing each round, `hit fixed` loses its justification —
  the gate's diff would have a durable home elsewhere — `<what changed>`
  thins to a sentence, and the round heading can carry a commit hash.
  That trades this design's shapes for fewer, so it belongs to a later
  wave and not to this one.

## Review rounds

### 2026-09-02 — architect, fable 5, concerns (round 1, full-document)

The gate episode preceding this round had no heading to write under and
deferred its line here, as the placement rule's one deferral case
prescribes.

- hit dismissed 2026-09-02 — the glossary's new `ledger entry` ban is violated by `spec-plan-lifecycle.md` lines 228 and 272; counter: both say "review-loop ledger entry" for the Unfinished-work list's own entry, not a disposition line, so the banned sense is not the one in use — and Changes by file already schedules both rewordings, the designed sequence being glossary at grilling, rules at implementation. The round confirmed the dismissal on both legs
- fixed 2026-09-02 — [Important] the relitigation fold had no expressible production: a re-raise folded against a `ruling:` line still needs its own terminal line, which must be `declined` and so must carry `ruling:` — but no developer ruled on the new finding, so the line either misreported its authorizer or could not be written. The same shape as the audit's defect 1, in the document that exists to cure it; ruling: 2026-09-02; the developer chose the cited-authorizer shape over a separate `folds:` clause and over producing no line at all — the fold now takes `declined <date>` with `ruling:` carrying the prior ruling's date and a citation of the folded line, the clause table and the glossary's **Ruling** entry both widened to admit a cited authorization
- fixed 2026-09-02 — [Minor] "the Unfinished-work commands anchor on `^- `" was true of one of five; license: the five published commands read from the rule; the claim now names the split and rests the payload-is-free conclusion on the scope guard, which is what actually defends it
- fixed 2026-09-02 — [Minor] "Historical ledger lines stay as written" sat beside a scheduled rewrite of one historical line; license: the spec's own distinction between remapping under the merge and normalizing to a shape defined later; the exception is now stated with its reason
- fixed 2026-09-02 — [Minor] wave one routed implementer question 3 here and only its missing-anchor half was carried; license: wave one's own routing sentence; the autonomy-and-cap half joins the seams, deliberately unanswered because it decides the loop's authority rather than the ledger's shape
- fixed 2026-09-02 — [Minor] "163 severity slots" counted lines, not slots; license: the recount — 164 occurrences across 163 lines, one audit line quoting two; both numbers now stated
- hit dismissed 2026-09-02 — Changes by file prescribes edits to `spec-plan-lifecycle.md` the commit does not contain; counter: this is a design document, and Changes by file is a promise about implementation rather than an edit
- hit dismissed 2026-09-02 — the same, for `workflow.md`; counter: as above
- hit dismissed 2026-09-02 — the same, for wave one's record and its bare `dismissed` line; counter: as above
- hit dismissed 2026-09-02 — that the previous gate's dismissal contradicts Changes by file by calling the rewordings "scheduled"; counter: both texts say the same thing, and the audit read "scheduled for implementation" as "scheduled for a later wave"
- fixed 2026-09-02 — the developer, reading the Important above, asked why a round re-raises a settled finding at all; the answer is that a diff-scoped round is formally cut off from the ledger, so the cause is upstream of the fold; ruling: 2026-09-02; a new section puts the ledger permanently in a diff-scoped round's context, protecting settled and `held` lines while leaving session fixes as legitimate targets

That line, and every other in this section carrying `ruling:`, is
written in the grammar this design proposes rather than the one it
replaces. The shipped `fixed` admits only `license:`, and shipped
`resolved <date>` closes a `held` line that none of these had — so a
developer-directed change mid-round had no honest production at all,
which is the audit's defect 2 exactly.

Round 2 sharpened what the cure covers. The `ruling:` clause closes the
authorizer gap; it says nothing about the grade, and a first draft of
these lines invented an `[n/a]` severity that no grammar admits. The
answer is not a fourth value but the absence of one: a line no reviewer
graded carries no bracket, because severity is a reviewer's grade and
manufacturing one would repeat the very forgery the authorizer rule
exists to prevent.

### 2026-09-02 — architect, fable 5, blocking (round 2, diff-scoped)

- fixed 2026-09-02 — [Important] the scope section licensed a re-raise "with new evidence" while the fold stayed unconditional, so the licensed path had no disposition, and an autonomous fold of an evidence-bearing challenge is the arbitration the workflow rule forbids; ruling: 2026-09-02; the fold now covers evidence-free re-raises only, and an evidence-bearing one routes to `held` with `counter:` citing the prior ruling
- fixed 2026-09-02 — [Important] `[n/a]` was lawful under neither grammar, since all four shapes require `[<Severity>]` and the glossary admits three values — the authorizer gap closed, the grade gap did not; ruling: 2026-09-02; severity is omitted entirely on a line whose sole authorizer is `ruling:` and which no reviewer graded, which is the absence of a grade rather than a fourth value
- fixed 2026-09-02 — [Minor] the fold's citation had no slot; license: the fold production this wave wrote; `ruling:` now carries the prior date followed by `folding <section or line quote>`
- fixed 2026-09-02 — [Minor] this document's own deferred gate line read bare `- dismissed 2026-09-02`, the shape it schedules normalizing away elsewhere; license: the `hit dismissed` shape wave one shipped; the token is restored
- fixed 2026-09-02 — [Minor] the recount was falsified by the commit that wrote it, which added five slots in its own ledger while stating 164; license: the recount itself; the number is gone and the universal claim stands, with the reason a frozen count cannot survive a growing ledger
- fixed 2026-09-02 — [Minor] aggregating four gate hits into one line contradicted the **Gate line** entry this design owns; license: that entry; split into four lines rather than amending the definition, which would pre-empt an open question about controlled aggregation in reports
- fixed 2026-09-02 — [Minor] "those carrying `ruling:`, and `declined` lines" was redundant and did not cover historical settled lines; license: the authorizer rule; the conjunct is gone and pre-design lines are named as settled by their token alone

### 2026-09-02 — architect, fable 5, concerns (round 3, diff-scoped)

- fixed 2026-09-02 — [Minor] the states block's caption said "a `ruling:`-only line" where the rule twelve lines below requires two legs, and this document's own three `ruling:`-only lines carry `[Important]` because a reviewer graded them; license: that fuller paragraph; the caption now carries both legs
- fixed 2026-09-02 — [Minor] a fold against a pre-design settled line had no date to cite, since historical lines carry no authorizer clause; license: this design's own statement that such lines are settled by their token alone; the fold cites the date on that token, which is when the developer decided
- fixed 2026-09-02 — [Minor] "without new evidence" named no comparison base, and a wrong not-new call silently performs the arbitration the split exists to prevent; license: the workflow rule's triage principle that a finding which could go either way is a decision; evidence is new relative to what the folded line records, and a session that cannot tell holds

Round 3 judged the symmetry sound rather than rhetorical: an authorizer
is constitutive of a terminal transition and is therefore cited when it
exists elsewhere, while a grade is a reviewer's description whose true
absence is honestly recorded by omission. One principle, two treatments
— cite what exists, omit what never did.

Its stop signal: a fourth round would not earn its cost. The leftovers
were wording at a definition site, which is the class the consumption
gate's integrity audit reads with two quotes per defect at the same tier
over a broader scope. The document is done being reviewed in this loop.

Loop closed 2026-09-02 by the developer, on round 3's stop signal and
with every finding of every round disposed. Three architect rounds
ended concerns, blocking, concerns; every propagation gate episode
returned either CLEAN or hits that were dismissed with a written
counter-derivation, and none required a fix. The next reader is the
consumption gate's integrity audit, before the plan is written.

No episode or hit count appears here, and the omission is the lesson
rather than an oversight. Two drafts of this paragraph carried counts
and both were wrong: the first conflated this loop's gates with the
previous wave's, and the second froze a total that a later gate episode
invalidated by writing one more line into this very section — two
paragraphs below the sentence saying a growing ledger falsifies any
frozen number. The section reports what happened; the lines are the
count.

- hit dismissed 2026-09-02 — that the episode counts above invert the record, since all five `hit dismissed` lines sit under the round-1 heading and so come from one episode; counter: the placement rule writes gate lines under the *last* round's heading at gate time, so the gate before round 1 deferred its line to that stamp and the gate before round 2 wrote four more under the same heading — two episodes, five hits, and the third CLEAN before round 3. The count stands

That dismissal is worth more than the hit. The audit reconstructed the
history wrongly because gate lines carry no episode identity, which this
design refuses on the ground that losing it costs at most two extra
dispatches on the cheapest family. This is the refusal's first live
instance, and the cost it produced was a different one: not a re-run,
but a careful mechanical reader drawing a false conclusion from the
record. The refusal priced the operational loss and not the legibility
loss. It stands — but the seam it leaves is now measured rather than
assumed, and this line, written under round 3's heading by a gate that
ran after round 3, is itself the demonstration.
