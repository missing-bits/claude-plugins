---
ticket: none
date: 2026-11-14
status: implemented
decisions: registered
architect: blocking (adjudicated 2026-11-14)
integrity: 2026-11-14 (sha: 4d685b3)
branch: feature/delegation-boundaries
base: develop
---

# Delegation boundaries — provisional decisions and asks that only read

A session decides many things the developer never sees: a stand-in's
answer, a ruling sent to an implementer, a status move. Some of those
decisions turn out to be the developer's. A session also acts on a
question as if it were an order. This spec lets delegated decisions take
effect at once without asking, records them as provisional, and hands
them to the developer in one batch at the document's next status move,
or for a design document at its consumption gate.
It also limits a question or a stated fact to reading. It is package 2c
of the release queue, narrowed by a history analysis.

## Problem

A history analysis read four sources of Claude Code sessions (about 160
sessions, 2026-08-18 to 2026-11-14); a second pass re-derived each
report's claims from the transcripts and kept only what held. The
records stay local, in `.claude/working-process/history-analysis-2026-11-14/`.
Four findings bear on this spec:

- **A stand-in's calls were reversed.** In one project the developer
  let Codex stand in for them on document reviews. Of the session's eight
  provisional calls they later read, they reversed three; at least one of
  the three came from the stand-in (the time-zone field), and probably a
  second (tab switching on a page). The session also closed a `blocking` plan
  verdict on a stand-in consent given before that round ran. In another
  project, pasted Codex text was kept as `ruling:` lines after the
  developer called it a suggestion.
- **A session's own answer was wider than needed.** An implementer asked
  a security question no document settled; the session sent back its own
  ruling, which the developer narrowed two minutes later at the cost of
  one more implement-and-review cycle.
- **A session moved a status and skipped a step on its own.** One
  session set a design to `implemented` without the code-review step,
  "according to the recommendation".
- **A question became an action, in all four sources.** A question
  about validation rules led to edits and a deploy; a stated fact led
  to a record update in a shared org; a pasted audit led to an executor
  and two commits; "commit mise.html and push" pushed a different,
  guessed file; "merge" led to a version mint and a release push.

The developer's answer to the first finding sets the shape: a stand-in
exists so the developer is not asked again and again, so its decisions
take effect, and the developer reads them together at the end.

## Goals, non-goals, anti-goals

Goals:

- A delegated decision takes effect without asking, and the record says
  who made it.
- The developer reads every delegated decision once, in one batch,
  before the document they approve moves on.
- A question or a stated fact never changes state, and a request
  changes only what it names.

Non-goals:

- A goal or Stop hook treated as consent. None of the four sources
  shows it since ai-devcontainer v1.
- A separate rule that an author never reviews its own text. D1 and D4
  cover the cases the analysis found.
- A settings key or a file that records a delegation. The delegation is
  given in conversation and lives for that session.
- The model self-report check, which the analysis also found wanting.
  It is package 5's.
- Implementation-time records in a ledger. A plan's implementation has
  no ledger, and D5 keeps it that way.

Anti-goals — the change fails, even if it works, when:

- the developer is asked more often than before;
- a provisional decision reads like a developer's ruling in any record;
- reading for an answer becomes harder: a session hesitates to dispatch
  an agent that only gathers information.

## Decisions

- **D1** — A *provisional decision* is a decision no written decision
  licenses, taken by someone other than the developer: a stand-in's
  answer, or a session's answer to an implementer. It takes effect at
  once. In a review loop, its disposition line carries the authorizer
  `provisional: <date> (<author>)` wherever the developer's answer
  would have carried `ruling:`. Argued in
  *Provisional decisions*.
- **D2** — The developer names a *stand-in* in conversation, for that
  session. The stand-in answers the held findings the loop would put to
  the developer, and each answer is a provisional decision.
  An answer covers only the question put to it; a later event needs a
  new question. Every other act stays the developer's: loop control
  (round orders, cap and all-Minor escalations, a round after
  `blocking`), held gate hits, a fix the mechanism hold stops,
  adjudicating a `blocking` verdict, withdrawing or
  deferring a registered decision, and moving a `status`. A stand-in's
  answer is not developer contact; it may answer a `blocking` round's
  held findings, whose fixes land while the loop stays stopped. A session
  that loses the delegation on compaction asks again rather than guess.
  Argued in *The stand-in*.
- **D3** — Provisional decisions reach the developer as one batch,
  delivered with the request for the document's next status move, and
  for a design spec or a technical design no later than its consumption
  gate. The developer confirms or reverses each. Confirmed, the line's
  `provisional:` becomes `ruling: <date>`. Reversed, the session applies
  the developer's answer at once and rewrites the line to the terminal
  state that answer gives — a reversed `fixed` may become `declined` or
  stay `fixed` with narrower text, a reversed `declined` becomes
  `fixed` — carrying `ruling: <date>`, the date of the developer's
  answer. A line a plan review writes into an already-consumed judged
  document travels in the plan's batch, and one answer settles both
  lines. A move made on the developer's word leaves no `provisional:`
  line, and an approval given before the request still gets the batch
  first. Argued in *The batch*.
- **D4** — A document's `status` moves only on the developer's word, or
  under a note in the project's instructions that names that move. Under
  such a note the batch goes into the report that
  announces the move, and reversals still land before the next work
  starts. Argued in *Status moves*.
- **D5** — At implementation time, a provisional decision is written
  when it is taken to `.claude/working-process/<stem>/provisional.md`,
  where `<stem>` is the plan's basename, or the design spec's where no
  plan exists — one line per decision: date, question, answer and
  author, `session` or `stand-in <name>`. The session that took them
  relays the list in its closing report; an answer there settles an
  item and is appended to its line, and the batch at the `implemented`
  move carries only what is still unanswered. No ledger line is
  written. An execution skill's
  own list, such as "Rulings I made", is relayed as provisional
  decisions. Argued in *Implementation*.
- **D6** — An ask licenses only what it asks for. A question or a stated
  fact asks for an answer: it licenses reading, with any tool, agents
  included, and never a change of state — an edit, a commit, an agent
  that writes, a push, a deploy, a write to a remote system, a release.
  A request licenses the change it names, on the object it names, and
  no further act with its own effect; an ambiguous object is asked
  about. Any other change needs a request for it, or a consent that
  covers it — given in this session, as a Standing answer, or by
  project instruction; where one looks needed, the session proposes it
  and waits. Records the rules owe — ledger lines, dispatch records,
  D5's file — are no change an ask must name. Argued in *Asks that only read*.
- **D7** — A line carrying `provisional:` is not settled. A reviewer may
  re-raise its finding like any `license:` line, and the oscillation
  tripwire does not apply to it. Until confirmed, neither the line nor
  the text its fix wrote licenses a later fix. Argued in *Provisional
  decisions*.

## Provisional decisions

The ledger already says who decided each fix: `license:` when the
session cited a written decision, `ruling:` when the developer decided.
A stand-in's answer is neither, and writing it as `ruling:` is the
error the analysis found — the record then claims the developer decided
what Codex proposed. A third authorizer keeps the record true and
keeps "every terminal line carries exactly one authorizer".

The author in the clause names who decided. In a ledger it is always
`stand-in <name>`, since triage gives a session no unlicensed decision
to take; `session` appears only in D5's file. A batch is then a query,
not a memory: every line under the
document's `## Review rounds` whose authorizer is `provisional:`.

A provisional line is not settled (D7). Settled lines are protected
because they record the developer's decision; this one records nobody's
yet. It sits with `license:` lines, which re-dispatch briefs already
leave open to attack. The oscillation tripwire guards against two
readings of one license; a provisional answer cites none, so a re-raise
against it goes through ordinary triage, and an unlicensed fix is held
or put to the stand-in as before.

Nor does a provisional answer license anything. Triage cites written
decisions, and a stand-in's fix writes one into the document; a later
fix citing that text would rest on an answer the developer has not read,
and the batch query would not find it. The text stays uncitable until
confirmed, so a dependent fix is held, answered and listed in its turn.

## The stand-in

The developer wants a stand-in to stand in: to answer what the developer
would answer, so the loop does not stop for them on a held question.
Those questions concern what the document says, and each answer leaves
a ledger line the batch reads back and the developer can reverse.

Every other act stays with the developer, each for its own reason. A
round order, a cap or all-Minor escalation and a round after
`blocking` spend rounds; a spent round cannot be confirmed or reversed,
and the cap resets only on a message from the developer. Adjudicating a
`blocking` verdict and moving a status each close what the batch exists
to reopen; the analysis found exactly that, a `blocking` verdict closed
on a stand-in's consent. Withdrawing or deferring a registered decision
changes what the spec decides, and its grammar carries `ruling:` alone;
a held gate hit is such a missing decision, so it stays with the
developer too. A fix the mechanism hold stops is a cost decision, the
one the hold exists to put to the developer.

A stand-in's answer covers the question it was asked. The closed
`blocking` verdict rested on a consent given before the round that
produced it; no answer about a round can cover that round's outcome.

The delegation lives in conversation, like the loop's autonomy consent
when it is not recorded. A session that loses it on compaction asks
again rather than guess, as the consult consent already does.

## The batch

The developer chose one handover at the end of a document's review
loop, and the end the rules already give them is the status move they
make. A spec or a plan moves to `approved` when they approve it, so the
batch rides on that request: they read the decisions before they approve
what they shaped.

A design spec or a technical design is consumed before its approval can
matter: a plan written from a provisional line is rewritten when the
line is reversed. Its batch therefore falls due no later than its
consumption gate.

The terminators still end the rounds, and a loop can end well before
the developer approves; the batch waits for the next status move, or
for a design document's consumption gate, whichever comes first. At
that gate the batch is settled before the integrity audit, since a
reversal edits the audited body and, like any fix wave, runs the
propagation gate.

Each item is confirmed or reversed. A reversal is the developer's
ruling, so the session applies it at once and rewrites the line in
place: the token says what became of the document under the developer's
answer, and the authorizer is now theirs. Confirming converts the
authorizer alone. A rewrite in place keeps one home per finding, as the
held gate line's terminal rewrites already do.
On a move made on the developer's word, no `provisional:` survives,
and a document that moved with one still carrying it moved without its
batch. A move made under D4's project instruction carries its batch in
its report, and the lines stay `provisional:` until the developer
answers it; converting or rewriting them on an `implemented` document
is a process record, which the frozen body excepts.

A line a plan review writes into an already-consumed design spec, by
the lifecycle rule's cross-document clause, would find no later
consumption gate there. It travels in the plan's batch instead, and the
developer's one answer converts or rewrites both lines.

## Status moves

The lifecycle rule already treats approval as the developer's — "the
developer has approved the plan (the `status` flip to `approved`)" —
but says nothing of who may move a status to `implemented`. The
analysis found a session that did so on its own recommendation, with
the code review skipped. D4 states the owner for every move.

Some projects hand a move to the session. In one, a manager session
merges a verified package and closes its plan. A note in the project's
instructions that names the move keeps that working — no settings key
records a status move — and the batch then reaches the developer in the
merge report, and a reversal there is work before the next
package rather than a blocked merge.

## Implementation

During implementation an implementer asks questions no document
settles, and a session that answers each one alone takes a provisional
decision every time. Holding each for the developer would interrupt them
constantly, which the stand-in decision rejected. So the session
answers, records the answer as provisional, and the batch at the
`implemented` move carries it.

An implementation has no ledger, and its batch may fall due sessions
later, so the record cannot be the session's memory. The session writes
each decision when it takes it to a file in the dispatch-record store,
which survives compaction. The store belongs to one checkout, and the
`implemented` move may happen in another, so the session that took the
decisions relays the list in its closing report; the file is only the
net under its own compaction. An execution skill may
keep its own list — superpowers' inline executor ends with "Rulings I
made" — and the relay calls those items provisional, since the
developer made none of them.

A skipped process step is no provisional decision. Every step is an
offer the developer declines, and D4 keeps the `implemented` move
theirs, which is what the analysis found missing.

## Asks that only read

Every case in the fourth finding has one shape: the developer asked for
an answer, stated a fact or requested one change, and the session
changed something more. The
reversals all followed a change of state — an org write, a deploy, a
commit, a push, a release — and never a read.

So the line runs by effect, not by tool. Reading is always allowed: a
session that needs an agent to gather data or analyse a corpus may
dispatch one on a question. A change of state needs a request for that
change, and a request reaches no further than its object: "merge" asks
for a merge, not a release. A consent the developer gave — in this
session, as a Standing answer, or by project instruction — such as the
loop's per-round commits, is such a request and keeps working.

An ambiguous request names the change but not its object — "commit
mise.html and push" when no such file is tracked. The session asks which
object is meant; a guess acted on is a change nobody requested.

## Parts touched

- `plugins/working-process/rules/workflow.md` — D2 and D3 in the review
  loop, D3's batch named *the provisional batch* to keep it apart from
  the per-round held batch; D7 in *Re-dispatch briefs*' protection list
  and the oscillation tripwire, and its no-license clause in triage's
  list of what licenses a fix; D5 under step 6; D6 as a section beside
  *Credentials*.
- `plugins/working-process/rules/spec-plan-lifecycle.md` — the
  `provisional:` clause in the clause table under *The disposition
  ledger* and the terminal-line definitions (D1, D3); the status-move
  owner (D4), in one place for every move; D7 beside the re-raise
  protection; the consumption gate's backstop sentence gains
  `provisional:` lines beside `held` and `hit held` for a judged
  document only, never a plan's passage to implementation (D3).
- `docs/domain/glossary.md` — **Provisional decision** and **Stand-in**;
  **Ruling** gains a pointer to its provisional counterpart.
- `plugins/working-process/CHANGELOG.md` — an `## Unreleased` entry.

## Out of scope

- How a stand-in is reached (Codex CLI, a pasted reply). The developer's
  own instructions cover the mechanics.
- A check that a status moved with no `provisional:` line left. The
  process-status skill could report it later; nothing here requires it.
- The harness's own guidance on irreversible actions. D6 narrows the
  cases the analysis found — a question, a fact, a request exceeded —
  and does not restate the rest.

## Review rounds

### 2026-11-14 — architect, fable 5.2, blocking (round 1, full-document)

- hit fixed 2026-11-14 — *Parts touched* named an "authorizer table" the lifecycle rule does not have; it now names the clause table under *The disposition ledger*
- hit fixed 2026-11-14 — *Problem* said two of the three reversals came from the stand-in while the verification confirms one; it now says at least one, probably two
- fixed 2026-11-14 — [Important] F1: D2 hands the stand-in round orders and cap and all-Minor escalations, which have no ledger line, cannot be reversed, never reach the batch and lift every spend bound; ruling: 2026-11-14; D2 and *The stand-in* narrow the stand-in to held findings and held hits, loop control stays the developer's, a stand-in answer is not developer contact
- fixed 2026-11-14 — [Important] F2: a stand-in answer to a held hit can withdraw or defer a registered decision, whose grammars (`withdrawn …, ruling:`, `**Defers:** …; ruling:`) and `decision-coverage.py` know only `ruling:`; ruling: 2026-11-14; D2 keeps withdrawing and deferring a registered decision with the developer
- fixed 2026-11-14 — [Important] F3: D1's "a session's choice to skip a process step" lets a session skip any gate provisionally, reverses "every step is an offer … let the developer decline", and has no record outside implementation; ruling: 2026-11-14; D1 drops the skipped step, *Implementation* says why
- fixed 2026-11-14 — [Important] F4: no rule says when a judged document moves to `approved`, the consumption gate passes on `provisional:` lines, and D3's list omits the technical design and a spec's `implemented` move; ruling: 2026-11-14; D3 names the next status move and, for a judged document, no later than its consumption gate; *The batch* argues it
- fixed 2026-11-14 — [Important] F5: D5 keeps implementation-time decisions in the session's account, a memory across compaction, under a heading "Rulings I made"; ruling: 2026-11-14; D5 writes each decision when taken to `.claude/working-process/<plan stem>/provisional.md`, a skill's own list is relayed as provisional
- fixed 2026-11-14 — [Important] F6: "standing consent" collides with glossary **Standing answer** (a settings line) and names no home; ruling: 2026-11-14; D4, D6, *Status moves* and *Asks that only read* say Standing answer or project instruction, no new term
- fixed 2026-11-14 — [Minor] F8: nothing says a `provisional:` line, or text its fix wrote, licenses no later fix; ruling: 2026-11-14; D7 and *Provisional decisions* add that neither the line nor its text licenses a fix until confirmed
- fixed 2026-11-14 — [Minor] F9: two cases in finding 4 are requests exceeded, not questions, and the ambiguous-object rule has no register entry; ruling: 2026-11-14; D6 opens with an ask licensing only what it asks for, a request reaches no further than its object
- fixed 2026-11-14 — [Minor] F7: *The batch*'s "no `provisional:` survives the status move" is false under D4's report; license: D4; *The batch* scopes the invariant to moves made on the developer's word
- fixed 2026-11-14 — [Minor] F10: D3's fixed↔declined rewrite reads as binary while finding 2 was a narrowing; license: D3 ("the terminal state that answer gives"); D3's two cases are now examples, including a narrowing
- signal 2026-11-14 — another round only after the developer rules on F1–F6, a diff-scoped one over the rewritten D1–D3; the Minors are worth a sentence each and no round
- hit fixed 2026-11-14 — the intro still named a skipped step among the decisions a session takes unseen, after F3 dropped it; it now names a status move
- hit fixed 2026-11-14 — D4, *The batch* and *Status moves* let a Standing answer name a status move, while a Standing answer is a settings line and no registered key records one; they now name a project instruction alone, D6 and *Asks that only read* keep Standing answer, which the per-round commits exemplify
- hit fixed 2026-11-14 — the F10 rewrite dropped D3's reversed-`declined` case; D3 carries it again beside the narrowing
- hit dismissed 2026-11-14 — the `provisional:` chain names no reading surface; counter: the reader is the session gathering the batch at the status-move request, which D3 puts into workflow.md's review loop, and *Out of scope* defers a process-status check by design
- hit dismissed 2026-11-14 — the round-1 signal says "rewritten D1–D3" while the wave touched D1–D7; counter: a signal records what the reviewer judged at the time, and the reviewer foresaw D1–D3 as the rewrite
- hit dismissed 2026-11-14 — D5 puts `provisional.md`, not a dispatch record, into the dispatch-record store; counter: the record naming grammar governs records only, the store is the per-checkout git-ignored home that survives compaction, and D5 mints the file by name
- hit fixed 2026-11-14 — a gate line placed the per-round commits example in D6, where only *Asks that only read* carries it; the line now names both
- hit fixed 2026-11-14 — *Problem* called the second reversal "the settings tabs" while the records name tab switching on a page; relabelled

### 2026-11-14 — architect, fable 5.2, blocking (round 2, diff-scoped)

- fixed 2026-11-14 — [Important] F11: D5's file lives in a per-checkout store, so a batch is lost silently when the `implemented` move happens in another checkout, as in the manager case *Status moves* names (re-raises F5 with new evidence); ruling: 2026-11-14; D5 and *Implementation* make the deciding session relay the list in its closing report, the file only the compaction net
- fixed 2026-11-14 — [Important] F12: *The batch*'s "the lines convert once the developer has read it" writes `ruling:` without the developer's word; license: D3 and the second anti-goal; *The batch* converts the lines on the developer's answer
- fixed 2026-11-14 — [Minor] F13: D6's "Standing answer" excludes an unrecorded session consent the old "standing consent" covered; license: the workflow rule's session-scoped answers; D6 and *Asks that only read* name a consent given in this session, as a Standing answer or by project instruction
- fixed 2026-11-14 — [Minor] F14: D6's "nothing past it" is unqualified, and *Out of scope* still describes the old D6; license: *Problem* finding 4; D6 forbids a further act with its own effect, *Out of scope* describes the new D6
- fixed 2026-11-14 — [Minor] F15: D7's reversal clause names `license:` lines the prohibition beside it makes impossible (re-raises F8 with new evidence); ruling: 2026-11-14; the reversal clause is cut from D7 and *Provisional decisions*
- fixed 2026-11-14 — [Minor] F16: D3's consumption-gate clause has no site in *Parts touched*; license: D3; *Parts touched* adds the lifecycle backstop sentence, which gains `provisional:` lines
- signal 2026-11-14 — no further round earns its cost unless F11 takes the main-checkout mechanism; the Minors are a sentence each, the integrity-class items go to the consumption-gate audit
- hit fixed 2026-11-14 — F13's clause said *Asks that only read* names the three consent sources while only D6 did; the section now names them
- hit dismissed 2026-11-14 — the glossary has no **Stand-in** or **Provisional decision** entry; counter: *Parts touched* prescribes both entries and the **Ruling** pointer, which land with the implementation
