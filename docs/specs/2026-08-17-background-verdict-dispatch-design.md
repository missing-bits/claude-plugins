---
ticket: none
date: 2026-08-17
status: approved
grilled: 2026-08-17
architect: concerns (resolved 2026-08-17)
branch: feature/background-verdict-dispatch
base: develop
---

# Background dispatch for verdict agents

## Problem

The `architect` and `plan-adversary` agents block the session that
dispatches them. A review round runs 9–31 minutes (measured across the
#10 dogfooding runs), and for that whole time the developer's
interactive session sits idle. The plugin already solved this twice:
standards-plugin review dispatches "run in the background: a review
never blocks an interactive dispatching session" (review-reports rule),
and both consult agents carry `background: true` with matching
description text. The verdict agents are the same shape — a long,
self-contained run ending in one small deliverable — yet they still run
in the foreground, and no rule says what the session must do when a
verdict arrives as a task notification instead of a tool result.

## Design

### Dispatcher sequence — canonical in the workflow rule

A verdict-agent dispatch subsection in the workflow rule's dispatch
guidance defines the sequence; steps 3 and 5 reference it instead of
restating it. The workflow rule loads in every session (the plugin's
deliberate always-on exception), so the subsection is context every
session pays for — accepted deliberately: a single definition site
outweighs the context weight.

- A verdict-agent dispatch from an interactive session always runs in
  the background. The developer controls *whether* a review runs (every
  step stays an offer); an accepted dispatch runs in one mode. No
  foreground escape: a developer who wants to wait simply waits for the
  notification.
- A run with no interactive dispatcher cannot relay, so it never
  stamps — mirroring the review-reports precedent's deferral. On a
  document whose field is still unstamped, the next interactive touch
  re-offers the round through the Recovery section's offer loop; a
  round lost on an already-stamped document leaves no signal and is
  accepted as lost.
- A verdict agent writes nothing, so no directory question guards the
  agent itself; what the pre-dispatch check guards is the stamp turn.
  A pre-existing but undecided `docs/specs/` or `docs/plans/` would
  interrupt relay-and-stamp with the first-create question, so an
  undecided directory is resolved before dispatch.
- At dispatch, the session tells the developer the round is running in
  the background and its result will arrive as a task notification,
  with progress visible in the session's task list.
- On the completion notification, in one turn and in this order: verify
  the agent's model self-report against the dispatched and prescribed
  tiers (the lifecycle rule already requires the comparison), relay the
  report to the developer, then stamp the verdict. The stamp — the
  frontmatter field, any fallback record, and the body's round record —
  lands as a single edit, so no document ever holds a partial stamp.
  Where edit granularity forces separate writes, the body round record
  lands first: a mid-stamp death then leaves a round that visibly never
  closed, never a verdict whose findings were lost.
- The relay carries the verdict, the model self-report, and every
  finding in substance — narrative prose may be condensed, but no
  finding or its severity is ever dropped: the relay is the
  developer's veto point, and an omitted finding is a decision made
  for them. The full report stays in the agent's transcript.
- The stamp goes to the document named in the report, never to "the
  most recent dispatch".
- The sequence ends the delivery, not the loop: after relay and stamp
  the session may fix the document and dispatch a fresh round, or put
  its questions to the developer first — exactly as in a foreground
  round. The iterative review loop is intended behavior.
- At most one live round per document per field — a constraint the
  dispatching session enforces within itself; a parallel round from
  another session is accepted as undetectable, like the out-of-session
  edit below, and stays benign: both rounds record in the body, and
  the field holds the later stamp. Superseding a running round stops
  its dispatch when the platform offers a stop; otherwise the stale
  result is discarded on arrival — relayed as stale, never stamped.
- When the reviewed document changed after dispatch, the relay says so
  and the stamp — in this one case — waits for the developer's call at
  relay: stamp regardless, or discard and dispatch a fresh round. The
  only deliberate exception to same-turn stamping, and still no
  persistent state. Detection rests on the session's own conversational
  knowledge of edits; an out-of-session edit is accepted as
  undetectable, consistent with the no-marker recovery stance.
- When compaction leaves an in-flight dispatch unclear, the session
  checks its task list rather than guessing, and never fabricates a
  pending result.
- A background agent that dies or returns nothing is an ordinary error:
  relay the failure and offer a fresh dispatch on the same tier. The
  existing cap-refusal question (drop one family or wait) is untouched —
  a cap refusal surfaces synchronously at dispatch, before any
  background run starts (a platform assumption recorded under
  Recovery).

### Agent side — mirroring the consult pattern

Both verdict agents gain `background: true` in their frontmatter and
one description phrase: "runs in the background; the verdict arrives
as a task notification; the dispatcher stamps after relay, not
before". The description carries only that phrase — the full sequence
has exactly one definition site, the workflow rule.

Reports become self-describing, because a notification arrives as a
detached message that must survive compaction and parallel rounds:

- the architect's report opens with the reviewed document's path,
  followed by the model self-report line that opens it today — one
  reconciled order, not two claims on the first line;
- the plan-adversary's JSON output gains a `subject` key holding the
  reviewed plan's path.

The stamp routes by that subject, which makes parallel rounds on
different documents safe without any further rule.

### Recovery — deliberately no in-flight marker

The session's knowledge of a running dispatch (agent, subject, model,
date) stays conversational. The design rejects a persistent in-flight
marker (an `architect: pending` value): an abandoned session would
leave a durable lie in a committable document, and the field's clean
semantics — value equals latest verdict — would break. Recovery
without a marker is idempotent: a missing stamp means the round never
closed, so the lifecycle rule's existing offer loop re-offers the
review at the document's next touch. The worst case is a repeated run
— wasted compute, no corruption. That idempotence covers an unstamped field. A later round lost on an
already-stamped document leaves no signal — the field shows the prior
verdict and looks closed — and is accepted as invisible, like the
cross-session cases.

Two platform assumptions, stated so the wording can be revisited if
either proves wrong: a task notification is delivered once, to the
live session, and dies with it — an unrelayed verdict survives only in
the agent's transcript; and a cap refusal surfaces synchronously at
dispatch, before any background run starts.

## Changes by file

- `plugins/working-process/rules/workflow.md` — the new
  verdict-agent dispatch subsection; steps 3 and 5 gain a reference to it,
  and the rule's standalone "After every round … record the verdict"
  paragraph folds into that reference — the subsection's
  relay-then-stamp statement replaces it, leaving no third restatement.
- `plugins/working-process/agents/architect.md` — `background: true`;
  the description phrase; the report opens with the reviewed document's
  path.
- `plugins/working-process/agents/plan-adversary.md` — `background:
  true`; the description phrase; `subject` key in the JSON output.
- `plugins/working-process/rules/spec-plan-lifecycle.md` — "After any
  review round, stamp the verdict into the document's field" becomes
  "After any review round, relay the report to the developer, then
  stamp the verdict into the document's field"; nothing else moves.
  That sentence and the workflow rule's dispatcher-sequence subsection
  state the same ordering and are edited together — the plugin's
  existing device for a deliberate two-site statement.
- `plugins/working-process/rules/review-reports.md` — untouched; the
  new subsection cites it as precedent rather than restating it.

A minor working-process version bump at release; the change is
backward-compatible.

## Out of scope

- **Background plan-writing.** Consultation surfaced a real contract
  for it (an Assumed-decisions section, a fill-gaps-never-override
  boundary against the spec, ticket inheritance, a no-overwrite rule)
  and a persona disagreement over whether it needs a named agent. It
  is a separate feature riding the same mechanics and gets its own
  spec; the contract is parked in Private memory as its input.
- Consult agents and standards review commands — already background.
- Making the "plan without a verdict" state greppable — judged
  acceptable to leave invisible; revisit if a lost round ever hurts.

## Verification

Dogfooding in this repo, in two stages matching what a round can
exercise. Pre-implementation rounds — starting with this spec's own
architect review — verify the dispatcher sequence hand-driven: the
session stays free, the verdict arrives as a notification, and the
stamp lands after the relay. The shipped agent and rule changes are
verified only after the topic branch's dogfood version bump and a
rules re-sync — the plugin cache keys content by version.

## Review rounds

### 2026-08-17 — architect, fable, concerns

Four Minor findings, all wording-level, all fixed the same day before
the next round:

1. Two "opens with" claims on the architect's report — reconciled: the
   document path first, then the model self-report.
2. Single-edit atomicity across non-contiguous regions unnamed — the
   write ordering is now stated: body round record before the
   frontmatter field.
3. The first-create bullet borrowed a justification that does not
   transfer — rewritten to name the real consumer, the stamp turn.
4. "One new paragraph" undersized a ten-bullet sequence entering the
   always-on rule — sized honestly, the context trade-off recorded.

### 2026-08-17 — architect, fable, concerns (round 2)

Four Minor findings, all wording-level, fixed the same day before the
next round:

1. The cap-refusal timing claim was a second platform assumption stated
   as fact — now mirrored in the revisitable platform-assumption
   paragraph.
2. The changed-after-dispatch exception named no detection basis — now
   stated: conversational knowledge only; an out-of-session edit is
   accepted as undetectable.
3. The relay-then-stamp ordering will live in two rules — the lifecycle
   bullet now carries the edited-together note.
4. Dangling "new paragraph" referent — now "subsection".

### 2026-08-17 — architect, fable, concerns (round 3)

Two Minor findings, both wording-level, fixed the same day:

1. The non-interactive dispatcher had an obligation it cannot meet —
   the sequence now defines the deferral: no relay possible means no
   stamp, and the next interactive touch closes the round via the
   existing re-offer loop.
2. Verification conflated two dogfoods — now split: hand-driven
   dispatcher rounds before implementation, shipped artifacts after
   the dogfood version bump and rules re-sync.

### 2026-08-17 — architect, fable, concerns (round 4; resolved 2026-08-17 without a fresh round)

Two Minor findings, both enumeration-completeness, fixed the same day.
The session halted the loop after four consecutive all-Minor rounds
(4, 4, 2, 2 findings) and annotated the concerns resolved instead of
dispatching a fifth round; the developer accepted the resolution the
same day:

1. The workflow rule's standalone verdict-recording paragraph escaped
   the change enumeration — Changes by file now folds it into the
   subsection reference.
2. The one-live-round constraint read as absolute — now scoped to the
   dispatching session, the cross-session case accepted as
   undetectable like the out-of-session edit.

Post-resolution addition, 2026-08-17: a dispatch-time announcement
bullet joined the sequence (the session tells the developer the round
runs in the background and the result arrives as a notification) —
routed from the implementation plan's adversary round 4, which flagged
the plan shipping it beyond this spec's enumeration.

### 2026-08-17 — architect, fable, concerns (round 5)

One Important finding and one Minor:

1. Important — the Recovery guarantee ("a missing stamp means the
   round never closed, so the offer loop re-offers at the next touch")
   holds only for an unstamped field. On any round after the first the
   field already carries a verdict, and the lifecycle rule's greppable
   anchors match only bare `blocking|concerns` values — a document
   reading `LGTM` or `concerns (resolved …)` presents as fully closed,
   so a lost later round leaves no signal and silently vanishes. Not
   the out-of-scope unverdicted case: this is a verdicted-but-stale
   state Recovery claims to close and cannot. Suggested: scope the
   Recovery claim to rounds on an unstamped field and fold the
   stamped-document lost round into the accepted-invisible bucket, or
   give the offer loop a visible trigger.
2. Minor — the spec names the new subsection "dispatcher-sequence"
   while both edited-together consumers ship "verdict-agent dispatch
   subsection"; two names for one two-site statement invite the drift
   the edited-together device exists to prevent. Suggested: rename the
   spec's references to match the shipped heading.

Resolution note, 2026-08-17: both findings fixed the same day — the
recovery claim narrowed in the spec and the shipped rule, and the
subsection references unified to the heading's name.
