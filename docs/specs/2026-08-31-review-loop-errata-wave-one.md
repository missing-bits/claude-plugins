---
ticket: none
date: 2026-08-31
status: draft
architect: blocking (adjudicated 2026-09-01)
revises: ./2026-08-17-autonomous-review-loop-design.md
branch: feature/audit-errata
base: develop
---

# Review loop — errata wave one

## Problem

An integrity audit of the autonomous review loop returned eleven
defects, each proved by two quotes. Two were applied before the 0.14.0
release; nine stayed open. Three of those nine put the shipped rules in
contradiction with themselves, so the loop's own text tells a session
two different things at the same moment. They are cheap to remove and
cost nothing to decide, which is what separates this wave from the
follow-up spec.

The full report, its provenance, and the disposition of all eleven
defects live in
[`docs/audits/2026-08-29-autonomous-review-loop-integrity-audit.md`](../audits/2026-08-29-autonomous-review-loop-integrity-audit.md).
This document is the record of the wave, not a second copy of the audit.

## Scope

Six changes, all in `plugins/working-process/`:

1. **B6** — the all-Minor signal no longer prescribes fixing by grade.
   It said "Fix the residue"; the same rule says triage reads the fix's
   license, never the finding's grade. The bullet now routes the round
   through ordinary triage.
2. **B7** — a session may no longer close the loop alone. The all-Minor
   escalation is a question, so the resolution annotation records the
   developer's close and no session writes it without their answer.
3. **B8** — the reviewer's stop-signal ask lost its all-Minor
   precondition and now stands every round. A round can leave one
   Important behind and still not repay a re-read.
4. **C9** — a contested propagation hit is dismissed with a written
   counter-derivation and reported, never escalated as a held line. A
   hit is a report, not a question, so it never spends the round's one
   interruption. The `[hit]` severity-slot variant leaves the ledger.
5. **A3, first half** — the `held` shape gained a `counter:` clause.
   Two passages required a held line to carry counter-evidence and the
   closed grammar had no slot for it.
6. **Implementer question 1** — a diff-scoped brief's diff is taken
   against the previous round's `fixed` lines and their `<what changed>`
   clauses. These documents stay uncommitted through the rounds, so the
   ledger is the only durable account of the diff.

Round 2 added a seventh change the wave had to absorb: the propagation
gate needed a record of its own. Removing the `[hit]` variant had traded
a wrong shape for no shape, leaving the gate's ordinary case — a hit
found and fixed — with no home, no heading, and no route into the next
round's brief. The "Gate lines" subsection supplies both shapes.

Cluster A's five remaining defects are out of scope: they are one
unwritten state machine and belong to a follow-up spec treating the
ledger as loop state. Implementer questions 2, 3 and 5 stay open there
too, and four seams are carried to it:

- **Are gate episodes first-class ledger units?** Round 2 raised it and
  round 3 showed it doing unfunded work: the outstanding-hit state has
  no shape, which this wave ships as a stated gap rather than closing by
  accident.
- **Round 1 of this wave is a live instance of open defect A2** — a
  `blocking` heading under which every line is `fixed`, which the
  shipped rule forbids, produced under those rules by the session
  repairing them. The terminator is either wrong or unenforceable as
  written.
- **The glossary has no owner on the fix-wave path.** Three collisions
  in one wave; the grilling-session, its only maintainer, fires at spec
  authoring. The candidate placements are triage — a `fixed` line whose
  license is a glossary term, or whose change moves a term's meaning,
  owes a glossary check on the same line — or a standing enumeration
  target for the propagation gate, which reaches only the quoting case.
- **A stop signal cannot bind text that did not exist when it was
  given.** Round 3's own words, and a better argument than the one this
  wave used to override round 2: a stop signal judges the marginal value
  of re-reading a document, and round 3 found a Critical in a subsection
  no reviewer had seen. New design written after a stop signal should
  re-arm review rather than override it, and the signal should be scoped
  to the text it read.

## Decisions taken during the wave

**The oscillation tripwire keeps its held line.** The wave's reach for
change 4 was approved as general, on a recorded claim that the tripwire
carried the same defect. It does not: the tripwire fires inside triage,
before the round's relay, so its held line joins the single batch and
spends no second interruption — and what it escalates is a developer
decision about which reading of a license wins, not a mechanical hit.
It was instead connected to change 5: its named flip is the evidence
the new `counter:` clause carries. The architect round confirmed the
call.

**The shipped spec and plan stay as they are.** A propagation gate
found eight sites where
`docs/specs/2026-08-17-autonomous-review-loop-design.md` still
describes the pre-errata design. The drift is real. The session first
fixed all eight, on a false claim that an earlier commit had set a
precedent for amending an implemented spec; that commit edited the
document while it still carried `status: draft`. The edits were
reverted. The hits are dismissed instead: the spec records what shipped
in 0.14.0, and its architect verdict certifies the body text, which an
`integrity:` hash covers exactly. Editing the body would leave a stamp
pointing at text no reviewer read. This document's `revises:` field
carries the pointer instead.

**`revises:` was chosen over `superseded-by:`.** The architect proposed
a forward pointer on the older document. The developer rejected the
name as overstating a partial departure, and rejected a general
`references:` field as collapsing the distinction between lineage and
supersession. `revises:` points backward from the newer document, so no
stamped document is touched at all, and the lifecycle rule now carries
both the field and the principle that makes it sufficient: an
implemented document is an archive, and the surfaces it named are the
current truth.

## Changes by file

- `plugins/working-process/rules/workflow.md` — the propagation gate
  (dismissal, the written line, the two-re-dispatch bound, the pass
  condition), the re-dispatch briefs (the diff reference point, the
  unconditional stop-signal ask), and the all-Minor terminator.
- `plugins/working-process/rules/spec-plan-lifecycle.md` — the `held`
  shape's `counter:` clause, the "Gate lines" subsection with its
  `hit fixed` and `hit dismissed` shapes and their placement rule, the
  removal of the `[hit]` variant, the `revises:` and `spec:` fields, the
  implemented-document principle, and the "Finding what revises a
  document" lookup.
- `plugins/working-process/agents/integrity-auditor.md` — the
  propagation precondition and its STOP clause, plus the two surfaces
  stating the integrity audit's own bar as applied dispositions rather
  than a clean run.
- `plugins/working-process/agents/propagation-auditor.md` — the gate's
  pass condition in the description and the opening paragraph.
- `plugins/working-process/README.md` — the gate's pass condition.
- `plugins/working-process/.claude-plugin/plugin.json` — the dogfooding
  version `0.14.0-dev.audit-errata`.

Dropping the `[hit]` variant narrows a published convention, so the
release carrying this wave takes a minor bump rather than a patch.

## Review rounds

### 2026-08-31 — architect, opus 5, blocking (round 1, full-document)

- fixed — [Important] the gate's pass condition moved to "no confirmed hit remains" in one place and stayed "clean" in five others, one of which instructs the integrity auditor to stop; license: the change's own terminal condition, which the same paragraph contradicts; all six sites now state the passing bar, and `clean` survives only as the auditor's `CLEAN` output token
- fixed — [Important] removing the `[hit]` line left a dismissed hit with no durable record, against the rule's own "state prevents relitigation, not the reviewer's memory"; license: that sentence, plus the implementing plan's re-dispatch bound the rule had dropped; a `dismissed` line outside the finding grammar, and the two-re-dispatch bound restored
- fixed — [Minor] "the round's relay" had no referent before an integrity audit, which is not a round; license: the gate's own list of three firing points; now "the next report the session relays to the developer"
- fixed — [Minor] the `counter:` clause admitted only a finding the session disputes, while the tripwire case is one where it takes no side; license: the tripwire's own definition as a contested reading; widened to "disputed or contested"
- fixed — [Minor] "no session writes it on their behalf" forbade the session from writing the annotation at all, against the writing model everywhere else; license: the lifecycle rule's definition of the annotation as a dispatcher-written artifact; now "without their answer"
- dismissed 2026-08-31 — eight sites in the shipped spec and plan still describe the pre-errata design; counter: both carry `status: implemented` and record what shipped in 0.14.0, and the spec's architect verdict certifies a body an `integrity:` hash covers, so a body edit would un-certify text a reviewer did read; `revises:` carries the pointer instead

### 2026-09-01 — architect, opus 5, blocking (round 2, diff-scoped)

Two gate episodes precede this round. The first died on an SSL failure
before returning; per the workflow rule an infrastructure death is an
ordinary error, re-dispatched fresh and never resumed, consuming no cap
budget. Its partial output named one hit, confirmed by hand, and a hand
check found a second of the same class. The second episode ran clean of
its own and returned two more.

- hit fixed 2026-08-31 — the new `revises:` field joined the process-field set without joining the Misplaced-stamp class's published command; the field name joined the command's alternation, and round 2 then reversed this as finding four
- hit fixed 2026-08-31 — the `dismissed` line shape entered the round record without the Unfinished-work list stating whether it joins the anchors; the rule now says it stays out, because a dismissal is closed when written and owes nobody a next move
- hit fixed 2026-08-31 — this document's own `architect:` value read `blocking (2026-08-31, round 1)`, a form the grammar does not define, so the Unresolved-verdict command — anchored on `$` after the verdict — did not match it and the wave record hid its own open verdict from the sweep; the value became bare `blocking` with the round detail staying in the round heading, and the adjudication annotation replaced it at close, in the form the rule defines
- hit dismissed 2026-08-31 — `integrity-auditor.md` lines 3 and 11 still say "a clean audit is a precondition"; counter: both name the integrity audit gating plan-writing ("the work **it** gates"), not the propagation gate this wave re-phrased, and the parallel lines in `propagation-auditor.md` were both changed because both name the gate. Round 2 sharpened the claim: `clean` is loose there too, since the real bar is an applied-dispositions stamp, and the wording is corrected rather than defended
- hit fixed 2026-09-01 — the authoring-time gate after the fix wave reported this document's `architect:` value as contradicting a ledger line that called the value bare `blocking`; the contradiction was real and its direction inverted — `blocking (adjudicated 2026-09-01)` is the form the rule defines, and the ledger line had gone stale at the adjudication; the line now records both states
- hit fixed 2026-09-01 — the same episode had no landing place under the placement rule this wave had just written, which covered only a gate preceding a round; the developer settled it as the next round's heading, falling back to the last round's where no next round comes — an authoring-time audit or a document closing on an annotation
- hit fixed 2026-09-01 — the glossary's **Audit agent** entry still read "a clean audit is a precondition", the exact phrasing both agent cards moved away from in this wave, leaving the canonical definition site stale against its own instances; the entry now states the precondition as a disposed audit — every hit fixed or dismissed, every defect applied or declined — the general form covering both agents' specific bars

- resolved 2026-09-01 — [Important] a fixed propagation hit had no ledger line, so the diff-scoped brief's stated diff source could not see gate work; this document proved the hole by writing `- fixed — [hit]` lines in a severity slot the same wave deletes; landed in "Gate lines" (a `hit fixed` shape beside `hit dismissed`, both carrying their own leading token and no severity)
- resolved 2026-09-01 — [Important] the gate lines' placement had no referent before round 1 or before a round not yet dispatched; landed in "Gate lines" (they attach to the next round's heading and are written at its stamp, falling back to the last round's where no next round comes, rather than inventing a heading the closed grammar does not define). The first answer covered only a gate preceding a round; the authoring-time audit that followed this wave had no landing place under it, and the fallback closed that third case
- resolved 2026-09-01 — [Important] the two-re-dispatch bound did not say whether it counted per document or per gate episode, and "escalates" was undefined; landed in "The propagation gate" (per episode, no third attempt, and the outstanding hits reported with a dismissal's standing while the gated dispatch is held — a report the developer may override, never a second question)
- resolved 2026-09-01 — [Important] `revises` had joined the Misplaced-stamp command against the glossary's enumerated definition of the class as stamped fields "where the stamping steps put it"; landed in the Unfinished-work list (the alternation reverted, the class left stamp-only, the glossary untouched — `revises:` is authored like `branch:`, `base:` and `spec:`, none of which the class covers)
- resolved 2026-09-01 — [Minor] the dismissal of `integrity-auditor.md` proved the referent but not the claim; landed in `integrity-auditor.md` (both surfaces now say "an audit whose dispositions are applied", the bar the lifecycle rule actually sets)
- resolved 2026-09-01 — [Minor] `revises:` was unreachable from the document whose staleness it concerns, and `spec:` was carried by every plan and defined by no rule; landed in "Finding what revises a document" (a published reverse lookup mirroring the ticket sweep) and the frontmatter block (`spec:`, marked plans-only)

Round 2 asked for its own stop signal and answered that a third round
would not earn its cost: `blocking` suspends autonomy by the loop's own
terminator, and the leftovers were developer decisions rather than
wording residue another round would sharpen. The developer took all six
on 2026-09-01, which licensed the fixes above, and closed the verdict by
adjudication rather than a fresh round — the path the terminator exists
to route work into. That close was superseded when round 3 ran; the
adjudication had assumed no further round.

### 2026-09-01 — architect, opus 5, blocking (round 3, diff-scoped)

Dispatched over round 2's stop signal, on the argument that both its
premises had expired. Round 3 judged the override justified and supplied
a better argument for it, recorded as a seam below.

- resolved 2026-09-01 — [Critical] gate lines were written "when that round is stamped", later than both purposes the wave assigns them: the workflow rule makes the written line the thing that terminates the episode, and the next diff-scoped brief is composed before the round it belongs to is stamped. The discriminator "where no next round comes" was a fact about the future, undecidable at write time, and this document's own seven gate lines took the fallback branch — the practice was sound and the text described a different, broken procedure; landed in "Gate lines" (written at gate time under the last round's heading, the date token telling episodes apart from the round's findings, with one deferral for a gate before a document's first round; the fallback and its predicate are gone)
- resolved 2026-09-01 — [Important] the re-dispatch brief's published diff source named only `fixed` lines, so `hit fixed` lines fell outside it; landed in "Re-dispatch briefs" (the source now reads the round's `fixed` lines together with any gate lines under the same heading)
- resolved 2026-09-01 — [Minor] `hit fixed` dropped the `license:` clause its sibling shape declares mandatory without the definition site saying why; landed in "Gate lines" (one clause: neither shape carries a license, because a hit's fix is licensed by its own derivation)
- resolved 2026-09-01 — [Minor] the published `revises:` example used a plan-relative path, wrong for the field's commonest case; landed in the frontmatter block (`./<file>.md`, leaving `../specs/` to `spec:`, which is genuinely plans-only)
- resolved 2026-09-01 (declined) — [Important] the two-re-dispatch bound produces an outstanding-hit state no shape carries and no anchor surfaces; the document stands with the gap stated rather than closed: "Gate lines" now says outright that neither shape covers it, that it owes the developer a decision, and that the workflow rule's report is its only record until a shape exists. Designing that shape is the wave-two question of whether gate episodes are first-class ledger units, and answering it here would decide wave two by accident
- resolved 2026-09-01 (declined) — [Important] the glossary has no owner on the fix-wave path — the grilling-session fires at spec authoring, so an errata wave editing shipped rules bypasses it, and two of this wave's three instances were semantic where no mechanical pass could reach; the document stands because the fix is a process change to triage or to the gate's standing targets, not a wording change to this wave, and it is carried to wave two's list

Round 3's stop signal: no fourth round, and its reasons do not expire —
the Critical's repair is demonstrated by this document's own ledger and
needs no reviewer to confirm it, two findings are single-clause edits,
and two are decisions a fresh reviewer would restate rather than
resolve.

Seam for wave two, in round 3's words: a stop signal cannot bind text
that did not exist when it was given. It judges the marginal value of
re-reading a document, and this round found a Critical in a subsection
no reviewer had ever seen. New design written after a stop signal
re-arms review rather than overriding it, and a stop signal should be
scoped to the text it read.
