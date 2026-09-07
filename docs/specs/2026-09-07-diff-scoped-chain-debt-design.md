---
ticket: none
date: 2026-09-07
status: draft
grilled: 2026-09-07
revises: [./2026-08-17-autonomous-review-loop-design.md, ./2026-09-02-ledger-as-finding-state-design.md]
branch: feature/audit-errata
base: develop
---

# What the loop owes after a diff-scoped LGTM

Wave three, package B. A review loop's first round reads the whole
document and every later round is diff-scoped, so a diff-scoped `LGTM`
certifies a chain rather than a fresh whole-document read. That chain
leaves a debt, the rules prescribe how to discharge it, and nothing
records whether anyone did.

## Problem

A spec's consumption gate offers a pair as one question — an integrity
audit, or a confirming full-document round — and a plan's loop takes one
confirming round before it may terminate. Both mechanisms work. Neither
leaves a mark that says the debt was paid.

**One document has already passed all the way through unpaid.**
`docs/specs/2026-08-27-audit-agents-design.md` ran `concerns`
(full-document) → `concerns` (diff-scoped) → `LGTM` (round 3,
diff-scoped), carries `architect: LGTM` and `status: implemented`, and
has no `integrity:` stamp. It reached plan-writing and implementation on
a chain nobody audited and nobody accepted. The gate never fired, and no
published command reports it.

## What measurement established

Wave two recorded this as a seam: "A plan's owed confirming round has no
Unfinished-work entry … no command matches it, so `process-status`
reports clean while a confirming round is owed." Checking that claim
against the repo overturned it, and the correction reshapes the package.

**A plan's owed confirming round is already surfaced.** The rules
withhold the frontmatter stamp on a plan's diff-scoped LGTM, so the field
keeps the previous round's verdict, and that verdict is always one the
**Unresolved verdict** command matches. The derivation has two legs, and
the second is the one the ancestor design already worried about:

- a diff-scoped round always has a predecessor, and that predecessor
  never returned `LGTM`, because an `LGTM` from a full-document round
  ends the loop;
- an annotated predecessor — `concerns (resolved <date>)` — is
  grep-clean, which the ancestor names outright. But annotating *is* the
  close, and "scoping never spans a close": the next round on a closed
  document is a new loop's first round, which reads the whole document
  and is therefore never diff-scoped. So a grep-clean field and a
  diff-scoped LGTM heading cannot co-occur under the live grammar.

The seam's premise fails on plans. It survives only for a document whose
headings predate the `scope` token, which the open seams below record.

**The unsurfaced state lives on specs.** A spec's diff-scoped LGTM *is*
stamped, so its field reads `LGTM` and no command fires. What such a spec
owes is the gate's pair offer rather than a round, and the gate's own
defeat token records only one of the three ways that offer can be
discharged.

**The token has never been written.** Every occurrence of
`, chain accepted <date>` in the repo is a definition or a plan step,
never a use. Renaming or redefining it therefore costs nothing, and that
free hand expires the first time a session writes one.

## The design

### The class and its anchor

`spec-plan-lifecycle.md` gains a sixth Unfinished-work class:

    - **Chain debt** — a diff-scoped `LGTM` heading carrying no
      record that what it owed was discharged.
      `rg -n --no-ignore --crlf '^### .*LGTM \(round [0-9]+, diff-scoped\)$' docs/`
      Scope: a hit counts only inside a `## Review rounds` section — the
      second entry to re-scope the default guard, for the reason the
      first one does.
      Owner: for a spec, the consumption gate's pair offer; for a plan,
      the confirming full-document round.

The anchor reads a record the round-heading grammar already produces, so
it works backwards: it reports the live instance with no new write
anywhere. The tail `$` is exact, and the annotation below defeats it —
the idiom the list already uses for `(resolved <date>)`,
`(adjudicated <date>)` and `, waived <date>`.

### The token

`, debt discharged <date>` replaces `, chain accepted <date>`.

It names an **event** — this heading's debt was discharged on that date —
and never a property of the document. Events keep their meaning; a
property goes stale. The distinction is load-bearing: on the audit path
the discharge is conditional on a body hash, and a token claiming the
chain is *good* would contradict a later edit, while a token recording
what happened on a date never does.

**One word must be true on all three paths, and that test clears the
field by itself.** `accepted` is true only on the decline. `confirmed`
and `audited` are true only on one performance path each. `satisfied`
looked like continuity — the rules already say a matching stamp
"satisfies the gate" — and is a trap: satisfaction is discharge *by
performance*, so a waived debt is discharged without it, which makes the
word false on precisely the path that leaves no other trace. It fails
twice over, because the hash-match case also satisfies the gate and
writes no annotation, so the word would manufacture a symmetry that does
not hold. `met`, `paid`, `fulfilled` and `redeemed` carry the same
performance-only defect.

`discharged` is the genus word: English discharges an obligation by
performance *or* by release and declines to say which — the same refusal
this design makes about the reason clause. It is also the verb this
document reaches for unprompted whenever it explains the mechanism, while
every rejected candidate appears only where the token itself is being
argued about. The token should say what the prose already says.

The noun is `debt` rather than `chain` because the objects differ, as
this design's opening sentence already says: the chain leaves a debt. A
chain is an evidence structure and is not the kind of thing anyone
discharges. The house family is otherwise nounless — `(resolved <date>)`,
`(adjudicated <date>)`, `, waived <date>` all let the annotated record
supply the noun — so a bare `, discharged <date>` would fit the family
more strictly. It loses on one point that outweighs the five characters:
a round heading names an agent and a model, and a bare `discharged`
beside them invites a reader to think somebody was dismissed.

The comma is not decoration either. Parenthesised tokens qualify a value
— `concerns (resolved <date>)` changes what the verdict means — while
comma-appended tokens add a later event to a finished record. The
glossary calls a round heading "the immutable record of one dispatch",
and this annotation is written later, by a different actor, about a
different event, so it goes after the closing parenthesis rather than
inside it:

    ### <date> — architect, <model>, LGTM (round 3, diff-scoped), debt discharged <date>

Three paths discharge the debt, all three write the same token, and the
dispatcher writes it in every case:

- **the developer declining the gate's pair** — written in the decline
  turn, before the work the decline licenses begins. This is the only
  path whose trace exists nowhere else, which is what makes the
  annotation necessary rather than convenient, and writing it before the
  plan is the ledger's write-ahead discipline applied literally.
- **an integrity audit** — written once the audit's dispositions are
  applied, and before the `integrity:` stamp, for the reason the next
  section gives.
- **any later full-document round, at its stamping turn, whatever its
  verdict** — the debt is discharged by the reading, not by the grade. A
  confirming round returning `concerns` has paid the debt and left the
  loop running; without this clause its heading would sit bare and the
  anchor would fire forever.

**The gate's two arms cost differently, and the offer should say so.** An
integrity audit returns material for the dispatcher to dispose of and
leaves the verdict alone. A confirming round on a *spec* does something
larger: a spec's LGTM already ended its loop, and "scoping never spans a
close", so that round is a new loop's first round. It mints its own
verdict and stamps it — and a `concerns` there flips the field back from
`LGTM` while plan-writing is underway. That is the mechanism working
rather than failing, since finding a real problem before anything is
built on the spec is the whole point, but a developer choosing at the
gate is choosing between two very different prices and should be told
which is which. On a plan the question does not arise: there the
confirming round belongs to the same live loop, because a plan's
diff-scoped LGTM never terminated it.

A full-document round reads the whole document, so it annotates **every**
unannotated diff-scoped LGTM heading above it, not only the one it
immediately follows. A long plan loop can hold more than one — a
diff-scoped LGTM, a confirming round returning `concerns`, a fix wave, a
second diff-scoped LGTM — and one full-document read settles all of them
at once. Stating it this way removes the question of which heading a
round is "the confirmation for", which has no answer worth defining.

Where a session discharges the gate and dies before annotating, the
annotation's own derivation licenses a later session to write it: the
later full-document heading or the `integrity:` stamp is on the page, and
a fix a derivation licenses never waits for the developer. Only the
decline path has nothing to derive from, and there the debt correctly
re-surfaces and the developer declines again.

The token carries a date and nothing else. No clause records which path
discharged the gate, because each path leaves its own trace — an
`integrity:` stamp, a later full-document heading, or neither — and no
named consumer reads the path. The gate's re-ask is defeated by the
annotation whatever discharged it, and the command matches whatever
discharged it. Inferring the path from those traces is a reading
convenience, never a rule: a developer may decline and later commission
an audit anyway, and the inference would then be wrong with nothing
depending on it.

### The annotation precedes the hash

On the audit path the order is: apply the audit's dispositions, write the
annotation, recompute the body hash, stamp `integrity:`.

The `integrity:` hash covers the text below the frontmatter's closing
`---`, which includes the `## Review rounds` section and the heading the
annotation lands on. A stamp written before the annotation is therefore
stale the moment the annotation is appended — dead on arrival, recording
a discharge its own hash disowns.

### The confirming round's authority

`workflow.md` states two things it has never stated.

**The confirming round counts against the round cap.** The count is
derived by folding the round headings, and excluding one kind of heading
would require classifying them — a full-document round *after* a
diff-scoped LGTM is confirming, another full-document round is not. That
is a second fragile derivation in the one place the rules already concede
the cap is best-effort, because the reset event is recorded nowhere.
Counting needs no new state and no new derivation.

The consequence is stated rather than hidden: a plan whose loop spent its
three rounds escalates once before its confirming round. That round is
the most expensive shape a round takes — a whole document at the
prescribed tier — so a cap that guards spend should guard it above all.
Escalation is one cheap batch, and developer contact resets the count
through machinery that already exists.

**The confirming round is autonomous under the loop's standing consent.**
The rules make it a consequence of the terminator rather than an offer:
"one full-document confirming round follows". The one-interruption
contract reserves interruptions for a decision genuinely the
developer's, and a mandated round is not one. Without consent nothing
changes, because every dispatch waits anyway.

### The Unresolved verdict owner leg

That entry's owner leg reads "a fresh round at the prescribed tier, or
the resolution annotation". On a plan whose latest heading is a
diff-scoped LGTM, writing `concerns (resolved <date>)` closes the verdict
while skipping the confirming round — which `workflow.md` forbids: "For a
plan the loop never terminates on a diff-scoped LGTM."

A published owner leg therefore licenses a move a sibling rule forbids.
The defect predates this package; the new class only illuminates it, and
shipping a report whose own remedy is forbidden would be a deliberate
self-injury. The leg gains a plan exception: there the confirming round
closes the verdict, not the annotation.

The entry also names the co-firing outright. On a plan in this state two
classes report — Unresolved verdict on the withheld stamp, Chain debt
on the bare heading — and that is one debt seen from two sides. The
confirming round extinguishes both. Nobody should build suppression
machinery for it, and nobody should "fix" the duplicate.

### The riders

Each is its own item, named separately on purpose: wave two's review
rounds twice caught un-specced changes riding along with specced ones.

**A stop signal gains a durable record.** The rules ask every reviewer to
judge whether another round earns its cost, then give that judgment no
home. It appears in no ledger shape and no clause, so it survives only in
a relay that compaction eats — and practice has already needed it twice,
once to justify overriding a signal and once to close a loop on one. The
signal gets one line under the round heading that gave it, outside every
anchor, because a signal is not a debt.

Its scope stays qualitative: any later fix wave or new design extinguishes
it, and the judgment belongs to the session that would close on it. Precise
scoping would need a snapshot or a hash of the text the reviewer read, and
this series has refused that machinery for better reasons than this one. The
record is what makes an override auditable, and the override was the real
event.

**The concurrency limit recovers its reasoning.** The rules say "at most
one live round per document per field within the session" and stop there.
The ancestor design decided the rest and the shipped rule dropped it: a
parallel round from another session is accepted as undetectable and stays
benign, since both rounds record in the body and the field holds the
later stamp. Restoring that is errata rather than design.

One sentence is genuinely new, because the ancestor ruled before the
round sequence carried weight: a diff-scoped LGTM now certifies a chain,
so an interleave from another session punches a hole no round ever read.
The discharge paths are the mitigation — an audit and a full-document
round both read the whole document — so the gate this package makes
visible is what catches it. Under interleave a heading-derived cap
over-counts, which escalates early: the safe direction.

### Census sentences rewritten count-free

Three sentences encode a census of the list and go stale the moment it
grows:

- "the review-loop entry below is the one that does";
- "Four of the five Unfinished-work commands anchor a frontmatter field";
- "Those anchors all sit on a frontmatter field; the review-loop entry
  anchors a leading disposition token instead".

They are rewritten as properties rather than counts — commands under the
default guard never reach a body line; entries publishing their own scope
anchor a leading token or a heading, neither of which an indented
continuation matches. A seventh class then costs no accounting edit. Wave
two's frozen counters are the precedent, and updating the numbers would
repeat that mistake rather than end it.

### The live instance

`docs/specs/2026-08-27-audit-agents-design.md` gains
`, debt discharged <date>` on its round-3 heading, with a ruling recorded in
its own ledger.

That is a body edit on an `implemented` document, which the lifecycle
rule forbids: "amended only in frontmatter, never in the body". The
package licenses this one class of exception in a sentence — a ledger
annotation is a process record rather than a design amendment — and notes
that it re-arms any `integrity:` stamp, which after `implemented` is
already informational. Wave one set the precedent by normalizing its own
bare `dismissed` line, argued individually and traced in the document's
ledger.

Without the backfill the class ships with a permanent hit, and hits on
this list carry no durable disposition — there is no `hit dismissed` for
the Unfinished-work list.

## What the consultations contributed

Both personas were briefed identically from one canonical file, in fresh
contexts, and neither was told the other's answer. They agreed on the
vehicle, on a bare token, on the cap and autonomy answers, and on
rewriting the census sentences count-free. Two things each found alone
carried the design.

**The architect supplied the precedent that settles the layering
question.** Asked whether the Unfinished-work list backstopping a gate is
sound or a smell, it answered that **Pending re-review is already that
figure** — a frontmatter state awaiting an offer whose owner is "the
re-review offer at the document's consumption gate". Every class on the
list backstops a process step a session might sleep through. The chain
debt is the only offer-bearing state the index cannot see, so it is the
anomaly rather than the proposal.

It also weighed a rival this design had not considered: a frontmatter
qualifier (`architect: LGTM (diff-scoped)`), discharged by rewriting the
field. That costs no re-scope, no stale sentences, and would close the
live instance with a legal frontmatter edit. It loses on the point the
class exists for — detection would depend on a *new* write by the same
fleeting session the class protects against, so a document stamped before
the convention would be invisible. "A backstop that inherits the fragility
of what it backstops is a worse backstop."

**The system designer found both ordering leaks.** The annotation-before-hash
sequence above is its finding, verified here against the rule's own
statement of what the hash covers. So is the owner-leg defect, verified
against both texts. It also enumerated the five states a spec's chain can
occupy and showed that only the decline path lacks any other trace, which
is what makes the annotation necessary rather than convenient — and it
supplied the event-not-property constraint that decides the token's name.

Both derived the non-LGTM confirming round independently, unprompted, and
reached the same answer: the reading discharges the debt, not the grade.
Two fresh contexts, one conclusion, on the case the briefing had left
open.

Their only real divergence was in coverage rather than judgment: the
architect counted two stale census sentences and the designer three. The
designer's count is right.

### A third consultation, on the token alone

The developer commissioned one more architect consultation once the
design was otherwise settled, with the whole lexical sieve in the brief.
It refuted the token the session had proposed and supplied the test the
session had never articulated: **one word must be true on all three
paths.** The reasoning is folded into "The token" above; three of its
findings deserve recording as findings.

**It caught the session's strongest argument as a trap.** `satisfied`
looked like continuity because the rules already say a matching stamp
"satisfies the gate". In the vocabulary of obligations this annotation is
reinventing, satisfaction is discharge *by performance*, and a waived
debt is discharged *without* it — so the word is false on exactly the
path the design calls indispensable. The session had proposed it as the
leading candidate.

**It rejected `closed` on stronger ground than the collision count.**
The annotation is defined to land on a heading whose loop may still be
running, and the same rule file says "an annotation close ends the loop".
The class name carried the collision inverted: a spec's loop *did* close
at the LGTM stamp, and `Unclosed chain` would assert otherwise. Class and
token were renamed together, because a split vocabulary — a grep saying
one word and the fix writing another — is worse than either name alone.

**It corrected the design's statement of its own meaning.** The sentence
read "discharged, or explicitly waived by the person entitled to waive
it". Waiver is a *mode* of discharge, so the disjunction was redundant —
and the redundancy mattered, because it is precisely the genus reading
that lets one word stay honest on three paths. The sentence now ends at
"discharged".

## What the grilling changed in the glossary

The grilling session found six defects, all in `docs/domain/glossary.md`,
and applied them inline. Four were pre-existing — this design only
brought them into contact with something that tested them.

**Two canonical sentences forbade what this design does.** The Round
heading was defined as "the immutable record of one dispatch", and this
annotation appends to it; the Disposition ledger declared that it carries
per-finding and per-hit state while "loop-level state is derived from the
round headings and stored nowhere", and this annotation stores something
that is neither. Both are now qualified rather than waived: a heading's
*dispatch-time fields* are immutable and a later event appends after the
closing parenthesis, and the ledger carries one obligation the
consumption gate owns — the chain debt — because no folding derives it.
The shipped `, chain accepted <date>` broke both sentences already; it
had simply never been written, so nothing tested them.

**Consumption gate named one of the four things it owns**, the re-review
offer, omitting the integrity audit, the pair question, and now the chain
debt. It enumerates all four, and says outright that nothing orders them
against each other yet.

**Hit promised a disposition half of its instances lack.** It read
"confirmed or dismissed by the dispatcher" across both kinds, but only a
propagation-auditor hit has shapes to record that in. An Unfinished-work
hit has no dismissal at all — its only disposition is ceasing to match.
The entry now parts the two, which is also the reason the live instance
needs a backfill rather than a recorded dismissal.

**Unfinished-work list asserted a cost this design disproved.** It said a
class publishing its own scope "costs a consumer edit too". Verified
against `process-status`: the consumer already reads section scopes
generically, so the cost was one-time, spent on the first such class. The
sentence now says that, count-free.

And the term itself, previously absent for both the chain and its debt:

> **Chain debt**:
> The obligation a diff-scoped LGTM leaves — the document was approved
> with no whole-document read at the end, and someone must still take
> responsibility for the part no round re-read, or explicitly decline to.
> Discharged three ways: an integrity audit, any later full-document
> round whatever its verdict, or the developer's recorded decline of the
> gate's pair offer. Recorded as `, debt discharged <date>` on that
> LGTM's round heading — the record says only that it happened and when,
> never how or how well. Distinct from the chain itself, the
> round-one-plus-reviewed-waves structure the LGTM certifies.
> _Avoid_: chain accepted, chain closed, unclosed chain

The bare word "chain" folds into this entry rather than minting a second
one. A standalone entry becomes warranted only if rule text starts
predicating things of the chain itself.

One deliberate near-miss to note: the Unfinished-work list's own glossary
entry bans "debt list" as a name for the list. A single class named Chain
debt does not breach that ban, but nothing has come closer, and a second
debt-flavoured class would.

## Changes by file

- `plugins/working-process/rules/spec-plan-lifecycle.md` — the sixth
  Unfinished-work class and its scope leg; the annotation paragraph
  rewritten from the decline-only `, chain accepted <date>` to the
  three-path `, debt discharged <date>`; the `integrity:` bullet's
  annotation-before-hash ordering; the Unresolved verdict owner leg's
  plan exception and its note on the deliberate co-firing; the three
  census sentences rewritten count-free; and the one-sentence licence for
  a ledger annotation on an `implemented` document.
- `plugins/working-process/rules/workflow.md` — the confirming round's
  authority (counts against the cap, autonomous under consent) in
  `### Terminators` and `### What a diff-scoped LGTM certifies`; the
  stop-signal record in `### Re-dispatch briefs`; the restored
  concurrency reasoning and its one new consequence.
- `docs/domain/glossary.md` — **already done**, applied inline by the
  grilling session: the new **Chain debt** entry, plus corrections to
  **Round heading**, **Disposition ledger**, **Consumption gate**,
  **Hit** and **Unfinished-work list**. The section above says what each
  changed and why. No implementation task covers these.
- `docs/specs/2026-08-27-audit-agents-design.md` — the live instance's
  backfill: the annotation on its round-3 heading plus the ruling in its
  own ledger.
- `plugins/working-process/skills/process-status/SKILL.md` — **no
  change.** Verified: the skill already handles a section-scoped entry
  generically.

## Refusals

- **No reason clause on the token.** Each path leaves its own trace and no
  named consumer reads the path. A clause would be a second home for one
  fact.
- **No precise scope for the stop signal.** It would need a snapshot or a
  hash of what the reviewer read. Position in the ledger gives a coarse
  scope for free; precision is not worth its machinery, and this series
  has refused snapshots repeatedly.
- **No concurrency detection.** The ancestor's decision — undetectable and
  benign — is restored, not replaced. Engineering around it is expensive
  and the failure is already mitigated by the discharge paths.
- **No suppression machinery for the plan co-firing.** Two hits on one debt
  are documented instead. The Misplaced-stamp suppression works per line,
  and these are two different lines.
- **No `status` predicate in the class scope.** `process-status` states that
  an entry's scope "narrows where a hit counts, never whether the file
  qualifies". A document-level predicate would break that sentence and
  force a skill edit with new semantics.
- **No `process-status` edit at all.** Verified: the skill already handles a
  section-scoped entry generically — "for a scope naming a section, read the
  lines above the match as well" — rather than special-casing the
  review-loop entry.

## What this supersedes, and what it does not

The autonomous-loop design says a spec's diff-scoped LGTM "owes nothing
standing: it is the loop's normal terminal state, settled at the
consumption gate by the audit, the confirming round, or the recorded
acceptance above."

Read in full, that sentence is **right about the shape and silent about
the record**. It already names all three discharge paths — this package
invents none of them — and its claim is only that the *loop* owes
nothing further, which stands. What it never says is how a later reader
learns whether the gate settled anything, and the live instance is what
that silence costs: two of the three paths left no mark, the gate never
fired, and the document reached `implemented` with nobody able to tell.

So the correction is narrower than superseding a decision. The design's
`revises:` pointer records a departure in one respect: a spec's
diff-scoped LGTM does carry a standing obligation *until the gate is
recorded as settled*, where the ancestor treated the gate's existence as
settlement enough.

Wave two's recorded seam is corrected differently — not wrong that a gap
exists, wrong about which gap. Its premise about plans fails, and the
state it should have named lives on specs.

## Open seams

- **Release-mate consumption gates.** Three offers can be live at one spec
  gate — a standing `integrity:` stamp, a diff-scoped-chain LGTM, and a
  `*-fallback:` field — and no text orders, merges, or batches them, while
  the loop's one-interruption contract is scoped to rounds rather than
  gates. The developer put this outside the package.
- **Trailing whitespace defeats every exact tail anchor**, including this
  one, and fails toward false clean. The list chose that trade knowingly;
  headings are hand-written under more prose pressure than frontmatter
  fields, so exposure here is higher than at its neighbours. Not worth a
  per-class convention.
- **Headings predating the `scope` token.** `LGTM (round 4)` never matches
  the new command, which is correct, but the recovery reading "keys on the
  absence of `full-document`" and would call the same heading diff-scoped.
  The command and the recovery clause diverge on historical documents.
- **The deferred grammar lint** now has one more anchored line to check.
