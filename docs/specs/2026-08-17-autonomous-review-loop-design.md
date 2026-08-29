---
ticket: none
date: 2026-08-17
status: draft
grilled: 2026-08-27
architect: concerns (resolved 2026-08-27)
---

# Autonomous remediation in the review loop

## Problem

After an architect or plan-adversary verdict, the dispatching session
today fixes the reviewed document when it has no questions for the
developer and dispatches a fresh round; when it has questions, the next
round waits for the answers. Nothing defines which findings the session
may fix alone, how findings it must not fix alone are held and
surfaced, or when the loop stops. The developer wants the loop to run
with minimal input — the session fixes what it can, and every decision
still lands on the developer's desk exactly once.

This spec builds on the background-dispatch mechanics that
`2026-08-17-background-verdict-dispatch-design.md` defined and
working-process has since shipped (the relay turn, the single-edit
stamp, subject routing, one live round per document per field) and
would be needed even without them: the triage boundary is about
authority, not delivery. It shares a release with the audit-agents
spec, whose propagation-auditor this loop names as a gate when
available.

## Design

### Consent — the loop is the offered unit

An autonomous re-dispatch is a step nobody individually offered, so the
workflow ethos ("every step is an offer") is met one level up: the
session asks once per Claude Code session, at the first verdict
dispatch, whether the review loop may run autonomously — yes / not now
/ not in this session — states the cap, and honours the answer without
re-asking, mirroring the consult-consent pattern of workflow step 1. A
durable preference belongs in the developer's own instructions and is
respected when present. Without consent, every round behaves as today:
relay, stamp, and the session's proposals wait for the developer.

### Triage — a citable license, not a judgment

A finding is self-fixable when the session can cite the decision that
licenses the fix: a statement in the document itself, a glossary term
or `_Avoid_` ban, a recorded ADR, or a previously resolved held line.
The citation is written into the finding's disposition line. No citable
license means the finding is held for the developer. When in doubt, it
is a decision — and is held.

The license test is the plugin's existing wording/decision boundary
(the elements-of-style clause "binds wording, never decisions";
grilling applies updates only as decisions land) applied to review
findings. Consequences the rule text states explicitly:

- Severity is not the line. A Minor finding can be decision-shaped (a
  naming call the developer already ruled on); a Critical can be
  self-fixable (a contradiction with a recorded ADR — the ADR is the
  license). Triage reads the fix's license, never the finding's grade.
- A contradiction between two decision-bearing statements is held;
  "fixing for consistency" must not silently pick a winner.
- A finding the session believes is wrong is held with the session's
  counter-evidence attached — never silently fixed, never silently
  dropped. The session never arbitrates between the reviewer and a
  recorded developer decision.
- Only written decisions license fixes. A decision settled in
  conversation becomes citable by being written into the document,
  which the fix itself accomplishes.

### The disposition ledger — state lives in the document

The lifecycle rule already requires a `concerns`/`blocking` round to
record its findings or their disposition in the document body. This
spec gives that record a grammar — one line per finding, with a
disposition token:

- `open` — written at stamp time, as part of the single-edit stamp the
  background spec defines. An `open` line surviving a session means the
  remediation never ran; the document's next touch re-offers it.
- `fixed` — self-fixed; the line cites the licensing decision and says
  in one clause what changed.
- `held` — needs the developer; the line carries the concrete question
  (or the dispute plus counter-evidence), phrased so one short answer
  resolves it.
- `resolved <date>` — closes a held line once the answer lands. The
  answer's substance goes into the document's design text; the ledger
  line points at it and never duplicates it. `resolved (declined)`
  records the developer keeping the document as it was.

The record's shape is canonical, not improvised — practice produced
three competing conventions across six documents before this spec. The
section is `## Review rounds`; a round opens with
`### <ISO date> — <agent>, <model self-report>, <verdict> (round N[, <scope>])` —
the scope token is part of the canonical shape, `diff-scoped` or
`full-document`, omitted only on a round that predates the
distinction; the recovery clause keys on its absence-of-`full-document`
reading, so a full round always says so;
each finding takes one line with an anchored leading token:

    - fixed — [<severity>] <claim>; license: <citation>; <what changed>
    - held — [<severity>] <claim>; question: <one short question>
    - open — [<severity>] <claim>
    - resolved <date> — [<severity>] <claim>; landed in <section>
    - resolved <date> (declined) — [<severity>] <claim>; <why the document stands>

The mandated command is
`rg -n --no-ignore --crlf '^- (open|held) —' docs/` — the list's
hardening flags (`--no-ignore --crlf`), plus `-n` where the shipped
entries use `-l`, deliberately: this entry's hits are confirmed
against section membership, so line positions are needed. A match counts only when
the line sits inside a `## Review rounds` section — the body-side
analogue of the list's frontmatter guard, kept for the same reason: a
document quoting this grammar describes it rather than instantiating
it. A contested propagation hit takes the held shape with `[hit]` in
the severity slot (Sequencing) — the grammar's one severity-token
variant. A spec's accepted chain appends `, chain accepted <date>` to
its diff-scoped LGTM heading (Re-dispatch briefs) — the grammar's one
heading annotation.

The ledger is the ask-once mechanism: a resolved held line is a
recorded decision, so when a later round re-raises the same problem the
new finding is folded and cited against it — never re-asked.
Relitigation is prevented by state, not by the reviewer's memory.

A fix wave that deviates from a reviewer's suggestion records the
deviation and its rationale beside the text they concern — not only in
the ledger — so the next reviewer trips over the reason exactly where
the disagreement lives.

Two greppable anchors join the lifecycle rule's unfinished-work
discipline: `open` lines (a stamped round whose remediation never ran)
and `held` lines (pending developer questions). The `held` anchor is
load-bearing — a later LGTM round leaves the frontmatter greps clean
while a decision question still pends. No frontmatter counter mirrors
the lines: one home, one grep.

They join as ONE Unfinished-work entry — one class, an unfinished
review-loop ledger — whose entry text names both owners: an `open`
line's next move belongs to the document's next touch (the re-offer),
a `held` line's to the developer. The entry deliberately re-scopes the
list's frontmatter-only invariant for itself: its hits count inside a
`## Review rounds` section and nowhere else, and the lifecycle-rule
edit carries that re-scoping explicitly rather than leaving the plan
writer to reconcile the collision.

### Sequencing — the loop yields to the developer

After relay and stamp, the session triages every finding and applies
the licensed fixes. Then:

- Held set empty: dispatch the next round without asking, within the
  cap.
- Held set non-empty: batch the held questions into one message at the
  relay turn — per item: a one-line claim, why it is held, the
  question, and options with the session's recommendation — and wait.
  A fresh round dispatches only on a document with no findings awaiting
  the developer; a round over known-open decisions would re-report them
  at the loop's most expensive tier for zero information. The developer
  may explicitly order a round on the partial document; every step is
  an offer.

One batch per round is the minimal-input property stated as a
contract: the developer is interrupted exactly once per round, and
only when a decision is genuinely theirs.

Before any re-dispatch — held set empty or developer-ordered — the
propagation-auditor (audit-agents spec) gates the round when it is
available: the session dispatches it over the repaired document, fixes
its hits, and repeats until the audit comes back clean. A hit's fix is
licensed by its own derivation — a recounted counter or an enumerated
missed call site decides itself — so hits never wait for the developer;
a hit the session believes is wrong escalates as held, like any
contested finding — its held line carries the marker `[hit]` in the
severity slot, because a hit stays ungraded even when contested.
Without the auditor installed, the dispatch proceeds as before. Expensive reviewers read only mechanically consistent
documents — measured on a 22-round client cycle where roughly one
finding in ten was a counter or boundary sentence the top-tier reviewer
policed by prose.

### Re-dispatch briefs

The first round reads the whole document; every later round is
diff-scoped — briefed on what changed since the round it follows,
directed to attack the previous wave's fixes first, and forbidden from
re-reviewing the rest. Repair-born defects are the dominant late-round
class in both measured loops (this repo's 2026-08-25 run and a client
project's 22-round cycle, where twelve consecutive rounds traced one
round's repair to the next round's defect), and the one diff-scoped
round in that cycle had the best precision of all rounds at the lowest
reading cost. Diff-scoping also eliminates stale-read findings.

Every brief states the loop's terminators outright — the cap and the
all-Minor signal below — rather than improvising them late, and asks
the reviewer for its own stop signal: when the round's remaining
findings are all Minor wording residue, say so and judge whether
another round is worth its cost. That judgment concerns the NEXT
round's marginal value, never whether the document is good enough, and
it informs the developer's decision rather than replacing it.

A diff-scoped LGTM certifies a chain, not a fresh whole-document read:
round 1 read the whole document, and every later wave was reviewed by
the round that followed it — that chain is what the stamped verdict
vouches for. For a spec the chain has a backstop: the consumption
gate's integrity audit (audit-agents spec, when available) re-reads the
whole text before anything is built on it. For a spec whose LGTM came
from a diff-scoped chain, the gate's offer is the pair from the start —
an integrity audit or a confirming full-document round, one question,
never an offer followed by a re-offer of the option just declined;
when the auditor is not installed, the offer carries the confirming
round alone, a tool that is not installed disabling its suggestion,
never the work. Declining is the developer explicitly accepting the
chain, and the acceptance is recorded, not remembered: `, chain
accepted <date>` appended to the diff-scoped LGTM heading — the
`, waived <date>` precedent — so the gate never re-asks. Every step an
offer. A plan's consumption gate
(implementation) carries no gated integrity audit, so a plan's loop
never terminates on a diff-scoped LGTM: when a diff-scoped round
returns LGTM on a plan, one full-document confirming round follows,
and the confirming round's verdict is the one stamped. The diff-scoped
LGTM is relayed and its round record written — the
`### <ISO date> — <agent>, <model self-report>, LGTM (round N,
diff-scoped)` heading is the durable marker that a confirming round is
owed — while the frontmatter stamp alone waits for the confirming
round. That is the one named exception to the relay-then-stamp
sequence, and it lands in both sentences of the co-edited pair: the
workflow rule's dispatch subsection and the lifecycle rule's
relay-then-stamp sentence declare themselves edited together, so the
exception cannot live in only one of them. Recovery reads the ledger,
not the stamp — and it is plan-scoped: a plan whose latest round
heading is a diff-scoped LGTM that no later full-document round
follows owes its confirmation, and the plan's next touch re-offers
it — whatever the frontmatter says, since an annotation-closed or
previously-approved document is grep-clean there. A spec's diff-scoped
LGTM owes nothing standing: it is the loop's normal terminal state,
settled at the consumption gate by the audit, the confirming round, or
the recorded acceptance above. Scoping never spans a close: an annotation close
ends the loop, and a later round on the same document is a new loop's
first round, reading the whole document.

When the ledger records a deviation from a reviewer's suggestion, the
next round's brief invites refutation of the recorded rationale — the
rationale is not a defence to be protected. Validated in both
directions in one measured round: the invited reviewer upheld the
deviation and refuted its recorded justification, and both corrections
were real.

### Termination

- `LGTM` ends the loop — for a plan, only a full-document round's
  LGTM does (Re-dispatch briefs). If held lines are still open (the question
  outlived its finding), the consumption gate is the backstop: a spec
  does not pass to plan-writing, nor a plan to implementation, with
  open held lines — they are asked there at the latest. The same guard
  covers the spec→plan seam: writing a plan from a spec with open held
  lines asks them first.
- `blocking` suspends autonomy entirely: relay, stamp, stop — no
  self-fixes from a blocking round. By the architect's own grammar,
  blocking means the design cannot deliver its purpose or overrides a
  recorded decision; reshaping that is design work and re-enters
  through the design conversation, not through remediation. `concerns`
  is the autonomy zone; `blocking` never is. (Rejected alternative:
  route blocking findings through ordinary triage and rely on the
  relay veto — fewer special cases, but it lets a session self-fix
  fragments of a design the reviewer judged broken as a whole.)
- Round cap: three autonomous rounds per document per field without
  developer contact. Hitting the cap escalates — one batch: what was
  fixed, what remains, why — rather than halting silently. Any
  developer contact resets the count; the cap bounds unattended spend,
  nothing else.
- All-Minor signal: two consecutive rounds whose findings are all
  Minor end the unattended run — fix the residue, annotate
  `concerns (resolved <date>)`, and escalate with a fresh-round offer
  instead of dispatching again. The cap guards spend, the signal guards
  sense; both are escalations, never walls. (Measured 2026-08-17 on a
  four-round hand-driven loop: the signal would have fired after round
  2, and rounds 3–4 found only what a later plan-adversary round
  catches anyway.)
- Oscillation tripwire: a finding re-raised against a `fixed` line is
  never re-fixed autonomously — two readings of the same license are a
  contested reading; it escalates as held, the flip named.

A model-cap refusal mid-loop is already a developer contact (the
workflow rule's drop-or-wait question) and is never answered
autonomously.

Loop closure reuses existing machinery: after answers land, the
session offers a fresh round (replacing the verdict as usual) or the
lifecycle rule's `concerns (resolved <date>)` annotation with its body
note — this loop gives that annotation its natural traffic. A
`blocking` verdict sometimes closes by explicit developer adjudication
rather than a fresh round; the recorded form is
`blocking (adjudicated <date>)`, with the round record as its body
note — convention, not improvisation (first executed 2026-08-17).

### Held questions across sessions

Pending held lines re-surface at the document's next touch and at the
consumption gate — not at session start. This matches the background
spec's recovery philosophy: the document is the durable state, and a
gap in it re-offers the step. (Rejected alternative: a session-start
"you owe two answers" digest — more proactive, but it makes every
session pay a scan for a state the gates already catch.)

## Changes by file

- `plugins/working-process/rules/workflow.md` — the dispatcher
  paragraph gains the loop: the consent question, the license test,
  yield-on-held and the batch shape, the re-dispatch brief duties
  (diff-scoping, terminators stated up front, the reviewer's stop
  signal, invited refutation), the propagation gate (conditional on
  the audit-agents spec's component), the round cap, the all-Minor
  signal, the oscillation tripwire, blocking-suspends-autonomy, the
  note that relay is the standing veto, and the one named exception
  to the relay-then-stamp sequence: a plan's diff-scoped LGTM relays
  and writes its round record, only the frontmatter stamp waiting for
  the confirming full-document round. The consumption-gate offer for a
  spec whose LGTM came from a diff-scoped chain lands here too — the
  pair question (integrity audit or confirming full-document round),
  the confirming-round-alone narrowing when the auditor is absent, and
  decline recorded as acceptance — reshaping the singular audit offer
  the audit-agents spec routes into this same rule. So does the
  plan-side recovery re-offer: a plan whose latest round heading is a
  diff-scoped LGTM that no later full-document round follows is
  re-offered its confirming round at the document's next touch.
- `plugins/working-process/skills/process-status/SKILL.md` — the
  hit-confirmation step takes an entry's own published match scope
  when the entry re-scopes it (the ledger entry's `## Review rounds`
  sections); the frontmatter guard stays the default for every entry
  that publishes no scope of its own.
- `plugins/working-process/rules/spec-plan-lifecycle.md` — the
  disposition grammar with its canonical record shapes (the contested-
  hit `[hit]` variant, the `, <scope>` heading token (`diff-scoped` | `full-document`), and the
  `, chain accepted <date>` heading annotation included) and license
  citation, the `open`/`held` entry in the Unfinished-work list with
  its re-scoped match semantics (hits count inside `## Review rounds`
  sections, an explicit exception to the list's frontmatter guard) and
  the hardened command shape, the `blocking (adjudicated <date>)`
  close form, the consumption-gate backstop for open held lines
  (including the spec→plan seam), and the relay-then-stamp exception
  mirrored into this rule's own sentence of the co-edited pair — the
  two rules declare that ordering edited together, so the exception
  lands in both or in neither. The `, chain accepted <date>`
  annotation's writer is named here: the dispatcher appends it at the
  gate on the developer's decline, and its presence defeats the gate's
  re-ask.
- `plugins/working-process/agents/architect.md`, `plan-adversary.md` —
  untouched. Triage is the dispatcher's judgment: the reviewer cannot
  see what the developer has decided in session, so a reviewer-side
  "needs-developer" label would be wrong exactly in the contested
  cases (rejected alternative).

A minor working-process version bump at release, shared with the
audit-agents spec; the change is backward-compatible.

## Out of scope

- Code-review remediation — triaging `*-code-review` findings into
  fix/plan/spec lanes is the parked review-driven remediation loop
  (Private memory), a different pipeline stage.
- Background plan-writing — its own parked feature; the seam guard
  here (held spec lines asked before plan-writing) binds it when it
  lands.
- Report-contract changes — both reviewer report shapes stay as the
  background spec leaves them.

## Verification

Dogfooding in this repo: run this spec through the loop it defines —
consent asked once, an architect round in the background, licensed
findings self-fixed with citations, held questions batched once per
round, and the ledger greppable afterwards.

Deferred, owner named (2026-08-29): the release ships without this
run. `--plugin-dir` delivers agents but not the Rules payload, and the
loop's dispatcher behavior lives in the rules, so the run needs a
`sync-rules` re-sync first — the obligation the plugin README already
states after any update. The developer owns it, on the first real spec
after release.

Platform fact already proven (2026-08-17, four headless runs): a
`claude -p` session survives a background dispatch, receives the task
notification, and completes the relay→stamp sequence — the loop can
run unattended.

Deferred, explicitly: a mechanical lint (hook) checking `## Review
rounds` line grammar and anchors is a later release's component,
designed then — nothing in this release depends on it.

## Review rounds

### 2026-08-27 — architect, fable 5, blocking (round 1, full-document)

- resolved 2026-08-27 — [Important] the ledger anchors joined the Unfinished-work list whose shipped invariant counts frontmatter hits only; landed in "The disposition ledger" (section-scoped match semantics, hardened command, one entry naming both owners)
- resolved 2026-08-27 — [Important] a diff-scoped LGTM silently changed what the stamped verdict certifies, with no backstop for plans; landed in "Re-dispatch briefs" (the certification chain stated; a plan's loop never terminates on a diff-scoped LGTM)
- resolved 2026-08-27 — [Important] the release rider shipped a lint hook the spec never designs; landed in "Verification" (deferred to a later release)
- resolved 2026-08-27 — [Minor] a contested hit escalated as held would carry a severity token hits do not have; landed in "Sequencing" (the `[hit]` marker)

### 2026-08-27 — architect, fable 5, blocking (round 2, diff-scoped)

- fixed — [Important] the document state between a plan's diff-scoped LGTM and its confirming round was undefined, each reading breaking a recorded convention; license: this spec's own recovery philosophy (the document is the durable state); the not-stamped reading chosen, the relay-then-stamp exception named in the workflow bullet, the Termination bullet qualified
- resolved 2026-08-27 — [Important] the spec-side backstop (integrity audit) is conditional and declinable with no stated absence behavior; landed in "Re-dispatch briefs" (an unaudited diff-chain LGTM re-offers at the consumption gate: integrity audit or a confirming full round; declining both accepts the chain explicitly)
- fixed — [Minor] "the hardened shape every Unfinished-work entry carries" misstated the shipped `-l` shape; license: the shipped lifecycle rule text; the sentence now names the flags and defends `-n` deliberately
- fixed — [Minor] the `[hit]` variant was absent from the canonical grammar block and the lifecycle bullet; license: this spec's own Sequencing decision; both now carry it

### 2026-08-27 — architect, fable 5, blocking (round 3, diff-scoped)

- fixed — [Important] the not-stamped reading's greppability guarantee failed on annotation-close and post-approval paths, and discarded the round record with the stamp; license: the workflow rule's stamp-as-one-edit definition plus this spec's own closure structure; the round record carved out as the durable marker, recovery reads the ledger, and an annotation close ends the loop so scoping never spans it
- fixed — [Important] the relay-then-stamp exception was routed to the workflow edit only, splitting a co-edited mirror pair; license: the pair's own edited-together clause in both shipped rules; the exception lands in both sentences and both Changes-by-file bullets name it
- fixed — [Minor] the inserted `[hit]` sentence orphaned the command sentence into a lowercase fragment; license: the sentences themselves; reconnected
- fixed — [Minor] the unavailable path re-offered an uninstalled tool; license: the workflow rule's not-installed-disables-suggestion ethos; the unavailable path carries the confirming round alone

### 2026-08-27 — architect, fable 5, concerns (round 4, diff-scoped)

- fixed — [Important] the recovery clause's unscoped subject made a spec's accepted chain re-offer its confirmation forever, with the acceptance unrecorded; license: this spec's own recovery philosophy (durable state, never memory) plus the shipped `, waived <date>` precedent; recovery scoped to plans, the gate's offer stated as the pair from the start, acceptance recorded as `, chain accepted <date>` on the heading
- fixed — [Minor] the load-bearing `, diff-scoped` token was absent from the canonical heading shape; license: this spec's own round-2 `[hit]` resolution, the same propagation class; the canonical shape and the lifecycle bullet carry it
- fixed — [Minor] the split re-offer re-offered the option just declined; license: round 2's resolved ledger line (the pair as one question); the gate's offer is the pair from the start

### 2026-08-27 — architect, fable 5, concerns (round 5, diff-scoped)

- fixed — [Important] the round-4 gate behavior was fully designed in the body and routed to no file edit, in a two-spec release where the sibling routes the singular audit offer this pair reshapes; license: this spec's own round-3 routing precedent plus its ledger discipline (the rule edit carries the re-scoping explicitly); both Changes-by-file bullets now carry the gate clauses

Loop closed 2026-08-27 by the resolution annotation, on round 5's own
alternative: the single finding was a two-clause routing edit with no
design content, fixed as suggested, and the whole-text backstop is the
consumption gate's integrity audit this release ships — the exact
mechanism this pair of specs defines.
