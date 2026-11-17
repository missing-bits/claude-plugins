# review-loop — the dispatcher's procedure

## Dispatching a verdict agent

Dispatching a verdict agent (`architect`, `plan-adversary`), when
available:

- From an interactive session the dispatch always runs in the
  background — a review never blocks the session, mirroring the
  review-reports rule's precedent. A run with no interactive
  dispatcher cannot relay, so it never stamps; on a document whose
  field is still unstamped, the next interactive touch re-offers the
  round through the lifecycle rule's offer loop. A round lost on an
  already-stamped document leaves no signal and is accepted as lost —
  never corruption, only a missing re-run.
- Before dispatch, resolve any undecided Process directory
  (`docs/specs/`, `docs/technical-designs/`, `docs/plans/`) so the
  first-create question cannot interrupt the stamp turn.
- At dispatch, tell the developer the round is running in the
  background and its result will arrive as a task notification, with
  progress visible in the session's task list.
- On the completion notification, in one turn and in this order:
  verify the agent's model self-report (the comparison the lifecycle
  rule defines), write the dispatch record defined below, relay the
  report to the developer, check every citation the report supplies
  against what it names, then stamp the verdict (`LGTM` | `concerns` |
  `blocking`) into the reviewed document's `architect:` /
  `adversary:` frontmatter field. The citation check follows the relay
  rather than preceding it, because a wrong citation in conversation
  costs a correction while a wrong one in the record outlives the
  loop. The order has one named exception, defined under *What a
  diff-scoped LGTM certifies* below: a plan's diff-scoped LGTM.
- The dispatch record is written before the relay. The dispatcher
  saves what the agent returned, verbatim — extracted from the agent's
  transcript, never retyped, since a retyped record once shared none of
  its 23 lines with the report it claimed to hold. In Claude Code the
  task's output file is that transcript, and the report is the
  hand-back call's message:
  `jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="SubagentHandback") | .input.message' <transcript>`.
  Where that prints nothing, the agent's final assistant text is the
  report; where no transcript is readable, the record says it was
  copied from the relay. It goes under a header of the date,
  the agent, the model self-report, the subject, and — where a
  document was reviewed — its size, `size: <lines>`: the body's line
  count without the `## Review rounds` section, from
  `sed '1,/^---$/d' <file> | awk '/^## Review rounds/{s=1;next} /^## /{s=0} !s' | wc -l`,
  or with the `sed` stage dropped for a document without frontmatter —
  with no frontmatter and no `ticket`, since the record is evidence rather
  than a process artefact. It goes to `.claude/working-process/` at
  the repo root (`git rev-parse --show-toplevel`). A record survives
  compaction, the session's end and a branch switch, and no more; that
  bound is what the relay's condensation below leans on. Audits write
  none — a propagation gate's hits land in the ledger and an integrity
  audit's dispositions land as the edits it causes plus the
  `integrity:` stamp, so a record would give one fact a second home.
- The store is git-ignored by a `.gitignore` containing exactly `*`.
  Before writing a record the dispatcher ensures that file holds
  exactly that, rather than writing it once: the guard repairs a store
  directory made by hand, a file someone truncated, and a `git clean`
  that took the file and left the directory. A project already
  ignoring `.claude/` still gets the file, since the store may not
  depend on another file's contents.
- The record's name carries its agent and one discriminator:

      .claude/working-process/<stem>/<agent>-round-<N>.md
      .claude/working-process/<stem>/<agent>-<date>-<HH-MM-SS>.md

  `<stem>` is the reviewed document's basename without its extension,
  one directory per subject. A verdict agent takes the round ordinal,
  derived the way the heading will derive it — the highest ordinal the
  document's rounds carry, plus one, ordinals continuing across
  loops — because the record is written before that heading exists. A
  dispatch that reviews no document takes its subject as the stem,
  kebab-cased and capped at sixty characters, and the timestamp shape,
  having no ledger to draw an ordinal from; an `architect` dispatch on
  a bare question is one such, and the test is whether a document
  exists rather than which agent ran. Where a round-ordinal name is
  already taken, the new file appends the timestamp to it —
  `<agent>-round-<N>-<date>-<HH-MM-SS>.md` — which settles the
  superseded round two sessions can produce on one ordinal without
  asking either to judge which report is stale. A timestamp name
  collides only when a second record lands in the same second, where
  appending the same timestamp would reproduce the taken name, so it
  takes the lowest free counter suffix instead: `-2`, then `-3`.
- The relay opens with one header line, then one line per finding. The
  header carries the verdict, the model self-report, the finding count
  by severity, how many decisions await the developer, and — where a
  document was reviewed — its size and the change since the previous
  record of the same document and agent; with no earlier record
  carrying a `size:` line it shows the size alone. The relay reports
  the number and judges nothing. Each
  finding takes one line — severity, origin, claim — except where the
  reviewer emits no origin: the `architect` reads one document and
  every finding it returns originates there, so an architect relay's
  line carries severity and claim alone.
- Condensation reaches narrative prose alone, whatever a session's
  output style prescribes. The finding list is never condensed, and no
  finding or its severity is ever dropped: the relay is the
  developer's standing veto, so a finding nobody printed is a finding
  nobody could overrule. Narrative is safe to condense because the
  dispatch record holds the full text, which makes an expansion a
  quotation rather than a reconstruction — so the relay names that
  record's path, and the developer can open what was condensed.
- The header's count of decisions is the findings for which the
  session can cite no license, plus those whose suggested fix adds a
  mechanism and carries out no `ruling:` (the hold under *The review
  loop*), derived at relay time from the report and the decisions
  already written down — before any ledger line exists, since `open`
  is written at stamp time and triage follows the stamp. The `held`
  lines the same round later writes are that count's check: they come
  to the same number, and a divergence means triage found a license
  the relay missed, triage lost one the relay claimed, triage placed a
  fix on the other side of the mechanism line than the relay did, or
  the oscillation tripwire held a finding that does carry a license.
  The last is lawful, so the check reports the number rather
  than asserting a fault. Verdicts that suspend autonomy — `blocking`,
  the spent round cap, the all-Minor signal — stay out of the count:
  they decide whether the loop continues rather than what a document
  says, and the relay reports them in its own right.
- A citation the report supplies — a file and line, an identifier, a
  count — is checked against what it names before it is written into
  the document or acted on by a fix. A precise citation reads like
  verification and is not one, and the dispatcher who copies it into
  the ledger launders a reviewer's evidence into the project's record.
  The check is cheap and its absence is measured: one cycle relayed a
  line number off by one and an identifier that did not exist, both
  quoted with exact positions, both caught later by a propagation
  audit rather than at the relay. This is the citation's analogue of
  the model self-report comparison above — the same duty, on the other
  thing a report asserts about the world.
- The stamp — the field, any fallback record, and the round record `LEDGER.md`, beside this file, defines — lands as one edit, body record first
  where edit granularity forces separate writes, and goes to the
  document named in the report, never to "the most recent dispatch".
  The same exception splits that one edit: on a plan's diff-scoped
  LGTM the round record lands while the frontmatter stamp waits for
  the confirming round.
- The sequence ends the delivery, not the loop: after relay and stamp
  the session may fix the document and dispatch a fresh round, or put
  its questions to the developer first.
- At most one live round per document per field within the session;
  superseding a running round stops it when the platform offers a
  stop, otherwise the stale result is relayed as stale and never
  stamped. A parallel round from another session is accepted as
  undetectable and stays benign: both rounds record in the body and the
  field holds the later stamp. One consequence postdates that decision —
  a diff-scoped LGTM certifies a chain, so an interleave punches a hole
  no round ever read. The discharge paths are the mitigation, since an
  audit and a full-document round each read the whole document, and a
  heading-derived cap over-counts under interleave, which escalates
  early.
- When the reviewed document changed after dispatch — known only
  conversationally; an out-of-session edit is accepted as
  undetectable — the relay says so and the stamp waits for the
  developer's call.
- When compaction leaves an in-flight dispatch unclear, check the task
  list rather than guess, and never fabricate a pending result.
- An agent that dies or returns nothing is an ordinary error: relay
  the failure and offer a fresh dispatch on the same tier.
- A consultation (`*-consult`) produces no verdict and nothing to
  record.

### The review loop

Rounds after the first form a loop, and the loop is the offered unit —
no single re-dispatch is offered on its own. At the session's first
verdict dispatch, ask once whether the loop may run autonomously — yes
/ not now / not in this session — state the round cap with the
question, and honour the answer for the rest of the Claude Code session
without asking again. The same question carries a second clause wherever
the per-round commits defined under *Per-round commits on a document branch* below are available: whether the loop
may commit the reviewed document once per round. One question, two
answers, asked once. Each clause has a settings key, `review.autonomy`
and `review.per-round-commit`, read as the process-settings rule says:
a set key answers its clause unasked, and only an unset clause is
asked. A yes or no may be given "and record" per clause — "yes, and
record; commits: not now" records the first clause alone — which
writes that clause's key through the loader's `--set` where a settings
block names the loader; "not now" and "not in this session" are never
recorded. Without consent every round
behaves as it did before: relay, stamp, and every proposal waits for
the developer.

Triage decides each finding by its license, never by its grade. A
finding is self-fixable when the session can cite the decision that
licenses the fix — a statement in the document itself, a glossary term
or `_Avoid_` ban, a recorded ADR, or a line carrying `ruling:` — and
the citation goes on the finding's line in the disposition
ledger `LEDGER.md` defines. Everything else is held
for the developer, and a finding that could go either way is a
decision. Consequences the loop states outright:

- Severity is not the line. A Minor finding can be a naming call the
  developer already ruled on; a Critical can be a contradiction with a
  recorded ADR, which the ADR itself licenses the session to fix.
- A contradiction between two decision-bearing statements is held:
  fixing for consistency would pick a winner silently.
- A finding the session believes is wrong is held with the session's
  counter-evidence attached — never fixed silently, never dropped
  silently. The session never arbitrates between a reviewer and a
  recorded developer decision.
- Only written decisions license fixes. A decision settled in
  conversation becomes citable by being written into the document,
  which the fix itself accomplishes. A line carrying `provisional:`
  licenses nothing until the developer confirms it, and neither does
  the text its fix wrote.
- A finding whose `origin` names a judged document — a design spec or a
  technical design — is held unless a written decision licenses the
  edit, since changing either from inside a plan review is design work.
  `origin` is a list, so a finding naming more than one holds the same
  way, and its `held` line names in `options:` which named document is
  fixable at once. A licensed fix lands in the ledger of the document
  that changed, and the plan's line points at it, by the cross-document
  clause `LEDGER.md` defines — which also leaves the
  design spec's `integrity:` stamp stale, as any body edit to either
  document of an audit pair does.
- A fix that adds a mechanism is held whatever its severity, and a
  license does not lift the hold. A fix adds a mechanism when it
  introduces something the document did not have: a part, a task, a
  command, an option or flag, a state file or field, or a recovery
  path. Giving an existing part a new check, branch or case adds one
  too, whichever way it moves what the part accepts. Rewording,
  correcting a value, deleting text, removing an input, option or case,
  and adding a test or a verification step that brings no new command
  or script add none. Two fixes stay outside the hold: one carrying out
  a line with `ruling:`, which the developer already decided, and a
  propagation-gate hit's fix, which its derivation licenses. A fix the
  session cannot place either way is held. The held line's `options:`
  recommend the smaller option where it meets the requirements and
  always include "accept as a documented limitation".

A fix wave that deviates from a reviewer's suggestion records the
deviation and its rationale beside the text they concern — not only in
the ledger — so the next reviewer trips over the reason exactly where
the disagreement lives.

Once the licensed fixes land, the loop either continues or yields:

- Held set empty — dispatch the next round without asking, within the
  cap.
- Held set non-empty — batch the held questions into one message at the
  relay turn (per item: the claim in one line, why it is held, the
  question, and the options with the session's recommendation), then
  wait. A fresh round dispatches only on a document with nothing
  awaiting the developer, since a round over known-open decisions
  re-reports them at the loop's most expensive tier for no
  information. The developer may still order a round on the partial
  document — every step is an offer. Where a stand-in is named, the
  held findings go to it instead, and once its answers land the loop
  continues as with the held set empty: a `provisional:` line awaits
  only the provisional batch, never the next round.

One batch per round is the contract: the developer is interrupted once
per round, and only over a decision that is genuinely theirs.

### The stand-in and the provisional batch

The developer may name a *stand-in* in conversation — another agent or
tool that answers for them — for the rest of the Claude Code session; a
session that loses the delegation on compaction asks again rather than
guess. The stand-in answers the held findings a round would put to the
developer, and each answer is a *provisional decision*: it takes effect
at once, and its disposition line carries
`provisional: <date> (stand-in <name>)` where the developer's answer
would carry `ruling:`. An answer covers only the question put to it; a
later event needs a new question. A stand-in may answer a `blocking`
round's held findings, whose fixes land while the loop stays stopped.
Every other act stays the developer's: round orders, cap and all-Minor
escalations, a round after `blocking`, held gate hits, a fix the
mechanism hold stops, adjudicating a `blocking` verdict, withdrawing or
deferring a registered decision, and moving a `status`. A stand-in's
answer is not developer contact, so it resets no cap. During
implementation it may also answer the questions the workflow rule's step 6 describes.

Provisional decisions reach the developer as one *provisional batch*:
every line under the document's `## Review rounds` whose authorizer is
`provisional:`, and at a plan's `implemented` move the unanswered items
of its provisional list. It is delivered with the request for the document's
next status move, and for a design spec or a technical design no later
than its consumption gate, settled there before the integrity audit
since a reversal edits the audited body. An approval given before the
request still gets the batch first. A line a plan review writes into an
already-consumed judged document travels in the plan's batch, and one
answer settles both lines. The developer confirms or reverses each
item. Confirmed, `provisional:` becomes `ruling: <date>`, the date of
the answer. Reversed, the session applies the answer at once and
rewrites the line in place to the terminal state the answer gives — a
reversed `fixed` may become `declined` or stay `fixed` with narrower
text, a reversed `declined` becomes `fixed` — carrying `ruling:`, and
runs the propagation gate over the change as after any fix wave. A move
made on the developer's word leaves no `provisional:` line behind.

### The propagation gate

A passing propagation gate is the precondition for the dispatches it
gates, so an expensive reader only ever meets a mechanically consistent
document. The gate fires before every verdict-agent dispatch, first
rounds included — authoring errors exist before any repair; after a fix
wave, before the next round; and before an integrity audit. It runs in
two steps. First the session runs the Document checks itself, from the
repository root: `wp-document-check <document>` and, on a plan or a
design spec, `wp-decision-coverage <document>`. Each finishes in
seconds, so the session disposes of their hits — fixed, dismissed, or,
for a coverage hit, held — and re-runs both until neither prints an
undisposed hit. These re-runs are unbounded and spend none of the
episode's re-dispatches. Then, when the `propagation-auditor` agent is
available, the session dispatches the audit over the document, with
nothing from the scripts in its brief, fixes its hits, and repeats until
no confirmed hit remains; before every re-dispatch the scripts run again
first, since a fix wave can break what they check. The gate passes once
every hit from either side is disposed, and the relay reports the
scripts' dispositions and the auditor's hits together. Without the
agent installed the scripts are the gate, and the gate lines and the
held batch apply to their hits unchanged. A hit's fix is licensed by its
own derivation — a recounted counter and an enumerated missed call site
decide themselves — so hits never wait for the developer, with one named
exception, for coverage hits alone.

The two coverage hits — a registered decision no task cites, and a task
lacking its `**Realizes:**` line — are triaged by license. Where a task
already does the work and lacks only its annotation, the task's text
licenses adding the identifier. Where no task realizes the decision and
the decision's text settles every choice the missing task requires, the
decision licenses writing it, and the next round's brief names it among
the previous wave's fixes. Where writing the task needs a choice the
decision does not make, the hit is held: its question is that missing
decision, not the gap, which is already established. Any other hit of
the coverage duty is fixed where its derivation settles the fix and held
where it does not, as when breaking a `replaced by` cycle means choosing
which entry stands. No other hit, from a script or the auditor, is
ever held.

A held hit ends its gate episode and blocks the dispatch the gate
guards, as a held finding blocks a fresh round, and the session puts its
question to the developer. The answer lands where the decision belongs —
in the spec's register, or as the plan's `**Defers:**` line — and the
gate re-runs over the changed document and whatever depends on it, as a
fresh episode; the dispatch goes out once that episode passes. `LEDGER.md` defines the `hit held` line and its terminal
shapes.

A report's body governs, never its closing token. Where a report lists
located hits and also carries `CLEAN`, the hits are the report and the
gate has not passed. It has happened more than once on the cheapest
family, and once under a brief that ruled the combination out in as
many words — so emphasis on the writing side is spent, and the guard
belongs to the dispatcher who reads. The rule is stated here rather
than generalised, because `CLEAN` is this agent's token and no other
report carries one. A script's `document-check:` or
`decision-coverage:` summary line is not a hit either: each script
prints its summary on every run, clean ones included.

A script that cannot run — no Python 3.9+, a crash, any exit other
than 0 — is an ordinary error, never a hit: the gate stops and the
session puts the script's message to the developer. Where the message
names a cause in a document, such as a `spec:` naming a missing file,
the session fixes it and re-runs. Otherwise the developer decides:
install Python and re-run, or order the dispatch without the Document
checks. That order holds for the rest of the session, for the failing
document and both scripts on it; without the agent, the dispatch so
ordered is the one the gate guarded, and the relay says the Document
checks did not run. Nothing is written to the ledger.

The scripts also run at the authoring-time offer of an audit, whether
the offer is accepted or declined, since they only read. Accepted, the
offer runs a gate episode as above. Declined, no episode runs: the
session shows the scripts' hits to the developer and writes them
nowhere.

A hit the session believes is wrong is dismissed, never silently: the
session writes the `dismissed` line `LEDGER.md` defines and reports the dismissal in the next report it relays to the
developer. A dismissed hit is a report, not a question, so it never
enters the held batch and never spends the round's one interruption —
the developer reads the dismissal and keeps their standing veto over it.
The written line is what makes the gate terminate: a dismissed hit
recurs on every re-dispatch, so a gate waiting on a hitless audit would
wait forever, and a dismissal nobody wrote down would be re-derived
from nothing every round. Both dispositions take the gate lines `LEDGER.md` defines.

Two re-dispatches bound one gate episode — the run before a single
dispatch, never the document's lifetime, so every round gets its own
gate. A third is not attempted. The session reports the hits still
outstanding, with the standing of a dismissal, and holds the dispatch
the gate was guarding: a gate that cannot come clean has not done the
one job the expensive reader depends on. The report names what keeps
recurring, since fixes breeding fresh hits is the failure this bound
exists to catch. It stays a report — the developer may order the
dispatch anyway, as they may order any step — so it never becomes a
second question in a round that already spent its one.

### Re-dispatch briefs

The first round reads the whole document; every later round is
diff-scoped. Its brief names what changed since the round it follows,
directs the reviewer to attack the previous wave's fixes first —
including whether a fix added a mechanism its finding did not need — and
forbids re-reviewing the rest — repair-born defects are the dominant
late-round class, and diff-scoping also ends stale-read findings.

The ledger supplies what changed. The previous round's `fixed` lines and
their `<what changed>` clauses, together with any gate lines under the
same heading, are the record of that wave, so the brief cites them and
needs no snapshot, commit, or hash. Where the loop is not committing per
round, the ledger is the only durable account of the diff; where it is,
the commit carries the lines and the ledger still carries the intent. The
brief cites the ledger either way.

Diff-scoping forbids re-reviewing the document beyond the diff, and the
ledger is part of the document — so without a clause the reviewer is cut
off from the one section recording what the developer already decided.
The ledger is therefore always in scope for a diff-scoped round as
context, never as a review target, and what that protects is narrow:

- settled lines may be re-raised only with new evidence — new against
  what the folded line records, the base `LEDGER.md` defines — which routes to `held` rather than to a fold. A line
  carrying `ruling:` is settled by that clause; a historical line
  written before this design, `resolved <date> (declined)` included,
  carries no authorizer clause and is settled by its token alone. Both
  are the developer's decisions, and both are protected on the same
  footing;
- `held` lines carry questions already put, so a round does not
  duplicate one;
- lines carrying `provisional:` record nobody's decision yet, so they
  are not settled and a reviewer may re-raise them like `license:`
  lines;
- `fixed` lines carrying `license:` get no protection at all — the
  previous round's are the diff and are named as the first thing to
  attack, and older ones are simply unprotected, since a reviewer told
  not to re-raise a fix would lose the property diff-scoping was
  adopted for.

The reviewer learns what it may not reopen, never what it may not find.
Naming the section rather than copying its lines keeps the brief from
growing with the round count.

Every brief states the loop's terminators outright — the cap and the
all-Minor signal below — rather than improvising them late, and asks
the reviewer for its own stop signal: judge whether another round earns
its cost, and say what the round's leftovers are worth. The ask stands
every round, whatever grades the findings carry — a round can leave one
Important behind and still not repay a re-read. That judgment concerns
the next round's marginal value, never whether the document is good
enough, and it informs the developer's decision rather than replacing
it. The signal is recorded where a later session can cite it: one line
under the heading of the round that gave it, in the shape `LEDGER.md` defines. A signal surviving only in a relay
dies with the next compaction, and practice has needed it twice — once
to justify overriding one, once to close a loop on one. Where the ledger
records a deviation from a reviewer's suggestion,
the brief invites refutation of the recorded rationale — a rationale is
evidence to attack, never a defence to protect.

### Terminators

- `LGTM` ends the loop — on a plan, only a full-document round's LGTM
  does.
- `blocking` suspends autonomy entirely: relay, stamp, stop — no further
  round without the developer. It licenses no separate fix prohibition,
  because triage already holds what the prohibition was reaching for: a
  design reshape has no citable license by construction, so it is held
  whatever the verdict's grade. `concerns` is the autonomy zone.
- Round cap: three autonomous rounds per document per field without
  developer contact, counting only rounds that returned a verdict.
  Hitting the cap escalates in one batch — what was fixed, what remains,
  why — rather than halting silently, and any developer contact resets
  the count. Developer contact is a message from the developer: not a
  relay they read, not an escalation the session sent, not an unanswered
  batch. The count is derived from the round headings and the reset
  event is recorded nowhere, so the cap is best-effort by construction;
  a session that cannot count its own rounds escalates rather than
  assuming, since resetting to zero would let a long session grant
  itself three fresh rounds after every compaction. A plan's confirming
  full-document round counts like any other: the count folds round
  headings, and excluding one kind would mean classifying them — a
  second fragile derivation in the one place the rules already concede
  the cap is best-effort. A plan whose loop spent its three rounds
  therefore escalates once before its confirming round, which is the
  most expensive shape a round takes and the one a cap guarding spend
  should guard first. A run of `blocking` verdicts is unbounded by the
  cap, for the reason the cap is stated in: it counts autonomous rounds,
  and `blocking` suspends autonomy, so every continuation after one is
  the developer's own decision rather than a round the cap governs.
  Consenting to three rounds consents to three autonomous ones.
- All-Minor signal: two consecutive rounds whose findings are all Minor
  end the unattended run. Triage the round as always — by license, never
  by grade — and escalate with an offer of a fresh round instead of
  dispatching one. The escalation is a question, so the loop stays open
  until the developer answers it: the resolution annotation the
  spec-plan-lifecycle rule defines records their close — on a plan, once
  the confirming round has run — and no session writes it without their
  answer.
- Oscillation tripwire: a finding re-raised against a line carrying
  `license:` is never re-fixed autonomously. Two readings of one license
  are a contested reading, so it escalates as held, the flip named. A
  re-raise against a line carrying `ruling:` is the relitigation case
  instead, and `LEDGER.md` owns it. A line carrying
  `provisional:` cites no license, so a re-raise against it goes
  through ordinary triage and the tripwire does not apply.

The cap guards spend and the signal guards sense; both escalate, and
neither is a wall. Relay stays the developer's standing veto — every
report reaches them before the session acts on it — and a model-cap
refusal mid-loop forces developer contact: the drop-or-wait question the workflow rule's model selection asks is never answered autonomously.

### What a diff-scoped LGTM certifies

A diff-scoped LGTM certifies a chain rather than a fresh whole-document
read: round 1 read the whole document, and every later wave was
reviewed by the round that followed it. What that chain still owes
differs by document.

For a judged document, the consumption gate before plan-writing makes
the pair offer as one question — an integrity audit or a full-document
round — and never an offer followed by a re-offer of the option just
declined. When the `integrity-auditor` agent is absent the offer
carries the full-document round alone. For an audit pair the gate makes
one pair offer for both documents: its audit arm reads the two
together, while choosing its round arm dispatches one full-document
architect round on each document that carries the debt, and
plan-writing waits until every verdict so dispatched is settled under
the rules any verdict follows; the joint integrity audit stays a check
of its own. The two arms cost differently and the
offer says so: an audit returns material for the dispatcher to dispose
of and leaves the verdict alone, while a full-document round on a
judged document is a new loop's first round, since that document's
LGTM already closed its loop — it mints its own verdict and stamps it,
so a `concerns` there flips the field back while plan-writing waits.
The full-document-round arm therefore blocks plan-writing; the audit
arm does not, and plan-writing follows its dispositions.

Declining is the developer discharging the chain debt by release rather
than by performance, and the discharge is recorded rather than
remembered: the dispatcher appends `, debt discharged <date>` to the
diff-scoped LGTM heading, in the shape `LEDGER.md` defines, and that annotation defeats the gate's re-ask. The other two
paths write the same token.

For a plan the loop closes only when the latest round heading is
full-document: whatever ends its rounds while that heading
is diff-scoped, one confirming full-document round follows, and that
round's verdict is the one stamped. A round already full-document owes
no confirming round — it is the close. The confirming round inherits the gating
of whatever ended the rounds. Where autonomy still stands —
a diff-scoped `LGTM`, or a `concerns` inside the cap — the rules mandate
the round, so it is no decision of the developer's and spends none of
the round's one interruption. After `blocking`, the round cap or the
all-Minor signal it is the developer's to order, because each of those
suspends autonomy by its own terminator, and a round the rules mandate
cannot outrank a terminator that stopped the loop.

A session never judges that the rounds are ending. The terminators do,
as does the developer closing the loop. While none has fired and the
held set is empty, the next round is diff-scoped and the loop simply
continues; the confirming round is owed the moment one fires, which is
the moment a session would otherwise write the resolution annotation.

The plan case carries the single named exception to the relay-then-stamp
order above — a plan's diff-scoped LGTM is relayed and its round record
written, and only the frontmatter stamp waits for the confirming round.
Recovery therefore reads the ledger rather than the stamp. A plan whose
latest round heading is a diff-scoped `LGTM` that no later full-document
round follows is re-offered its confirming round at the document's next
touch, whatever the frontmatter says, since that heading is itself an
end. A latest heading of any other verdict is not an end, so there the
round is re-offered when something tries to end the rounds — an
annotation, an adjudication, a `status` move — or when a terminator that
suspends autonomy has fired.

Scoping never spans a close. An annotation close ends the loop, and a
later round on the same document opens a new one, reading the whole
document again.

After any
review round, relay the report to the developer, then stamp the
verdict into the document's field — this sentence and the bullet list under *Dispatching a verdict agent* above state the same relay-before-stamp ordering.
That list sequences further checks inside its own turn — the model
self-report before the relay, the report's citations after it — which
this sentence deliberately does not restate, so gaining one does not
make it stale. The order has one named exception, defined under *What a diff-scoped LGTM certifies* above: a plan's diff-scoped LGTM is relayed and its round record
written, while only the frontmatter stamp waits for the confirming
full-document round.

### The audit pair at the consumption gate

Where the technical-design offer is accepted, the audit waits: the
design is the last producer of changes to its design spec, and the
two are then audited as one target — an audit pair. The gate makes
one offer for that audit pair rather than one per document, and the
offer
names both documents, so declining it releases the chain debt of the
two it named and nothing besides. Where the audit runs instead, it
discharges that debt for both documents it read. The other arm stays
per-document: choosing it dispatches one full-document architect
round on each document that carries chain debt, each discharging the
debt of the one it read, and plan-writing waits for every verdict so
dispatched. The brief
confirms the auditor's two preconditions: every edit from the
conversation is written to disk, since one unsaved decision
manufactures a run of false defects; and the propagation gate above
has passed, leaving no confirmed hit, when that agent is available.

### Per-round commits on a document branch

Asking whether the loop may commit per round is not the lifecycle rule's commit suggestion, and
the difference is the speech act rather than the timing. That suggestion says a moment to commit has arrived; the consent question asks
once, before any round runs, for standing authorization to use a
mechanism — and a "no" leaves the authoring phase exactly as that rule describes it. That is why it may be asked during authoring
while the suggestion may not. A set `review.per-round-commit`, read as
the process-settings rule says, is that standing authorization already
given or withheld, and the clause is not asked; unset, it is asked as *The review loop* above says, "and record" among its answers.

One shape of the sooner commit the lifecycle rule leaves to the developer has a convention, because practice kept
reaching for it: **per-round commits on a document branch.** When the
developer authorizes it, the loop commits the reviewed document once per
round, as the round's last act. That boundary matches the ledger's own
unit — a round mutates the document several times (the stamp, the
triage, the fix wave, any gate episodes), and one commit after the wave
records what the round found together with what the session did about
it.

The commits go to a local branch named `<topic>.docs`, never to the
topic branch itself. Git refuses a ref nested under an existing branch,
so `feature/<ticket>-<short-name>/docs` cannot exist while its parent
does; the
suffix takes a dot because the branch convention already spends hyphens
on name parts, where `-docs` would read as a topic about documenting.

The loop runs on that branch for the whole authoring phase — the design
spec's rounds, the technical design's and the plan's alike — and the
topic branch takes it at the implementation-ready gate: by fast-forward
where the history is wanted whole, by squash where it is not. That
choice belongs to the project rather than the session, so the settings
key `docs-branch.merge` — `squash` or `fast-forward`, read as the
process-settings rule says — records it where it binds. Until a project
migrates to the key, a `CLAUDE.md` note — at the repo root or beside the
documents — declares it too, the key winning where the two disagree and
the session saying so. A session with neither asks at the gate, and the
answers include "squash, and record" and "fast-forward, and record",
which write the key through the loader's `--set` where a settings block
names the loader. Either way the document branch survives the merge,
which keeps loop churn off any published branch until somebody pushes it
and leaves the surviving ref marking where authoring ended.

Both halves of "local" are worth knowing before relying on it. Churn
stays private, and the history dies with the working copy: a teammate
cannot see it, and a lost machine takes it. That is still more than the
alternative, where the same rounds live only in a transcript, but it
means "return the document to the state round three read" is a promise
about one clone rather than about the repository.

What per-round commits never do is replace the ledger. Git says which
lines changed; the ledger says with what intent and on whose license,
and a diff carries neither "narrowed the claim" nor a cited ADR. A
`<what changed>` clause may thin to a sentence where the commit carries
the detail; it does not go. Nor does a sha stand in for a hash: a round
heading that one day carried its commit's sha would name that round,
and it never stands in for the `integrity:` hash, which is computed from
the body and must work on a document nobody committed — the default
path, where no sha exists.
