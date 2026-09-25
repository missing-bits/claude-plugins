# Working process — preferred flow

A spec-driven flow for non-trivial work. Every step below is an offer:
suggest it, let the developer decline. A tool that is not installed
disables its suggestion — never the work itself.

1. **Idea → spec.** When the superpowers:brainstorming skill is
   available, start non-trivial features there; capture the agreed design
   as a spec in `docs/specs/`. When the working-process consult agents
   (`architect-consult`, `system-designer-consult`) are available, ask
   once, early in the design conversation, whether the two personas
   should be consulted as the design forms — yes / not now / not in this
   session (honoured for the Claude Code session only; a durable
   preference belongs in the developer's own instructions and is
   respected when present). After a yes, dispatch a consultation when it
   looks worth its cost, without asking again for that conversation, and
   state the consent decision whenever it is made or changed — and when
   a compacted conversation leaves the current consent state unclear,
   ask again rather than guess. On a
   genuinely ambiguous ask — in-thread dialogue or a fresh-context
   consultation? — ask one short question rather than silently picking a
   surface.
2. **Spec → grilling.** Once a spec exists, offer a grilling-session
   (when the working-process plugin is installed) to stress-test its
   language against the project's domain terms.
3. **Grilled spec → architect review.** Offer a dispatch of the
   working-process `architect` agent (when available); dispatch and
   stamping follow the verdict-agent dispatch subsection below.
   Dispatch it on the most capable available model, named explicitly.
   When the `propagation-auditor` agent is available, a propagation
   audit gates that dispatch and every later round — the dispatch
   subsection below defines the gate and its dispatch points. Offer the
   same audit at authoring time as well, after any multi-site edit;
   that offer stands outside the loop, so the definition below does not
   carry it.
4. **Spec → plan.** At the spec's consumption gate, before the plan is
   written, offer an integrity audit when the `integrity-auditor` agent
   is available: a fresh-context read of the whole design spec, and of
   its technical design where it names one, returning defects and the
   questions an implementer would have to ask. The offer fires unless a
   standing `integrity:` stamp still matches the recomputed body hash of
   every document the stamp names — a match means the standing stamp
   satisfies the gate, and the spec-plan-lifecycle rule owns that
   comparison. For a judged document whose LGTM came from a diff-scoped
   chain the offer takes the pair-offer form the verdict-agent dispatch
   subsection defines — one pair offer for an audit pair, never one per
   document — and narrows as that definition says when the auditor is
   absent.

   At the same gate, and before the integrity audit above, offer the
   technical design when the repository is one that has code. A
   declaration the project records binds and is never re-asked, in
   either direction; a session reads it from the project instructions
   Claude Code loads at session start — a `CLAUDE.md` at the repository
   root or in `.claude/` — or from the file such a note points at, which
   is the shape available until a standing home for a project's process
   answers exists. Without a declaration, a repository carrying a
   toolchain manifest — a file a language or platform toolchain reads
   to build, test or deploy it — gets the offer at every consumption
   gate and nothing is written; a repository carrying neither gets no
   offer. The core names no closed list of markers, and a domain's own
   skill may name the markers of its technology. A marker proves the
   repository holds code, never that this change needs decomposing, so
   the declaration is the signal and the marker only raises the
   question. The offer reads *open the `system-designer-session` skill,
   when available, and write the technical design?* — never *dispatch*,
   which names a background agent here. Where no skill covers the
   technology the document is still written, from generic knowledge and
   best effort: a tool that is not installed disables its suggestion,
   never the work. A design spec that already carries
   `technical-design:` has had its first pass: the pointer answers the
   offer, and the offer to write a design is not made again. The pointer
   confirms the link and nothing more — the design it names still takes
   every check it owes — and a pointer that resolves to no file is a
   broken link, reported as a finding, never a reason to offer a second
   design. A session may propose writing the declaration and never
   writes it unasked. A change may skip the document when it
   sits inside boundaries and contracts already settled and leaves the
   implementer no new responsibility split, placement, or ownership of
   state.

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
   manufactures a run of false defects; and the propagation gate below
   has passed, leaving no confirmed hit, when that agent is available.
   Then write the
   implementation plan with superpowers:writing-plans when available;
   plans live in `docs/plans/`.
5. **Plan → adversary review.** Before implementing a non-trivial plan,
   offer a working-process plan-adversary agent dispatch (when
   available); dispatch and stamping follow the verdict-agent dispatch
   subsection below.
   Dispatch it on a model scaled to the plan's size, complexity, and
   risk — the most capable available for complex or risky plans, one
   family below for small mechanical ones — named explicitly.
6. **Implementation.** Test-driven when
   superpowers:test-driven-development is available; bugs go through
   superpowers:systematic-debugging when available.
7. **Implementation → code review.** When a `*-code-review` skill is
   installed for a domain the change touches, offer a review of the
   work's diff — once implementation is complete and before the plan's
   `status` moves to `implemented`, so a finding can still become work.
   Domains are judged as the plan-adversary judges them: from the change
   itself and the repo's own markers. Several domains touched mean one
   run per domain; orchestrating them into a single run is not this
   step. The step re-specifies no mechanics — the offer routes to
   whatever review surface the matched plugin ships, and that surface
   owns scope resolution, dispatch, and the report.

Both audits offered above run in the background, so a gated dispatch
waits for its audit's task notification before it is issued — a
sequencing rule rather than a blocking call, running on the relay
machinery the verdict-agent dispatch subsection already defines.

Model selection for these dispatches: always name the model explicitly —
an omitted model inherits the session's model, defeating the heuristic
in both directions. Reviews are never dispatched on the cheapest
available family. Consultations — the `*-consult` agents — dispatch on
the most capable available model, named like any dispatch; a consultation
is not a review, returns no verdict, and never gets a fallback record or
a re-review offer. An audit is not a review either, and the
never-cheapest floor governs reviews alone: the `propagation-auditor`
dispatches on the cheapest available family and the `integrity-auditor`
on the most capable available, each named explicitly. Both reports open
with a model self-report the dispatcher compares against the dispatched
and the prescribed rung before relying on the result — a mismatched
propagation run earns no reliance, and a below-tier integrity run gets
no stamp. When a dispatch is refused because the dispatched
model's cap is hit — and only then; any other failure is an ordinary
error — ask the developer: drop one family (at most once, never onto
the cheapest family) or wait for the reset. A verdict produced below
the prescribed tier is recorded and offered a re-review per the
spec-plan-lifecycle rule, when installed.

Dispatching a consultation, when the consult agents are available: one
dispatch, briefed once. The briefing names the subject and where it
lives (the repo root at minimum), the constraints that bind it, and
settled decisions separated from open questions — pointing at files
rather than pasting them. A follow-up is a fresh cross-check dispatch,
never a resumption. When both personas are consulted on one subject,
give both the same canonical briefing, each with its own focusing
question appended, and tell neither what the other said. Dispatch as a
named background agent, so the transcript stays inspectable.

A contribution is written to its dispatch record before it is relayed,
taking the timestamp shape of the two the verdict-agent dispatch
subsection defines: a consultation mints no round heading, so it has
no ordinal to derive, and several consultations of one persona on one
subject in one day are expected. The floor is met in that file —
attributed and substantially verbatim, compression allowed and merging
forbidden, every recommendation and every named risk surviving, and
text from two personas never landing in one bullet. The relay then
carries one paragraph per focusing question — or one per briefing,
where a single persona was consulted and none was appended — and the
path to the record. One thing stays in the relay whatever the floor
does: where the personas disagree, the disagreement is presented as a
disagreement with both positions, because a disagreement is the one
thing in a contribution the developer must decide and the digest
exists to raise decisions rather than bury them.

When `docs/domain/glossary.md` exists in the project, its canonical
terms and `_Avoid_` bans bind specs, plans, code identifiers, and
reviews.

When the `elements-of-style:writing-clearly-and-concisely` skill is
available, prose artifacts under `docs/` — specs, plans, ADRs, the
glossary — get its pass: invoke it before drafting a new document, and
run an explicit editing pass over the changed prose of an existing one.
The pass binds wording, never decisions. Without the skill there is no
substitute pass and no install nagging — the work proceeds normally.

## Branch naming

Feature work happens on a topic branch named
`feature/<ticket>-<short-name>`, where `<ticket>` is the work's tracker
reference and `<short-name>` says what the work is, and
`feature/<short-name>` where there is no ticket. How a tracker's
reference is spelled in a branch name is the project's own — this
convention fixes the shape and not the spelling.

The branch of a worktree created with a generated name is renamed to
this shape before its first commit, so the branch a reader sees is the
branch the convention names; the worktree's own directory is a separate
name and this convention does not govern it. The work's spec and plan
record the result in their `branch:` field — the topic branch, not the
`<topic>.docs` branch a review loop's per-round commits use, which the
spec-plan-lifecycle rule names and which is a sibling of it rather than
a second topic branch. The ticket rule's sourcing order reads the
current branch name first when a new document needs a ticket.

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
  (`docs/specs/`, `docs/plans/`) so the first-create question cannot
  interrupt the stamp turn.
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
  saves what the agent returned, verbatim, under a four-line header —
  the date, the agent, the model self-report, and the subject — with
  no frontmatter and no `ticket`, since the record is evidence rather
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
  by severity, and how many decisions await the developer. Each
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
  session can cite no license, derived at relay time from the report
  and the decisions already written down — before any ledger line
  exists, since `open` is written at stamp time and triage follows the
  stamp. The `held` lines the same round later writes are that count's
  check: they come to the same number, and a divergence means triage
  found a license the relay missed, triage lost one the relay claimed,
  or the oscillation tripwire held a finding that does carry a
  license. The third is lawful, so the check reports the number rather
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
- The stamp — the field, any fallback record, and the round record
  the lifecycle rule defines — lands as one edit, body record first
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
the lifecycle rule's per-round commits are available: whether the loop
may commit the reviewed document once per round. One question, two
answers, asked once. A durable preference in the developer's own
instructions is respected when present. Without consent every round
behaves as it did before: relay, stamp, and every proposal waits for
the developer.

Triage decides each finding by its license, never by its grade. A
finding is self-fixable when the session can cite the decision that
licenses the fix — a statement in the document itself, a glossary term
or `_Avoid_` ban, a recorded ADR, or a line carrying `ruling:` — and
the citation goes on the finding's line in the disposition
ledger the spec-plan-lifecycle rule defines. Everything else is held
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
  which the fix itself accomplishes.
- A finding whose `origin` names the spec is held unless a written
  decision licenses the edit, since editing a spec from inside a plan
  review is design work; `both` holds the same way, and its `held`
  line names in `options:` which half is fixable at once. A licensed
  spec-origin fix lands in the spec's own ledger and the plan's line
  points at it, by the cross-document clause the spec-plan-lifecycle
  rule defines — which also leaves the spec's `integrity:` stamp
  stale, as any body edit does.

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
  document — every step is an offer.

One batch per round is the contract: the developer is interrupted once
per round, and only over a decision that is genuinely theirs.

### The propagation gate

When the `propagation-auditor` agent is available, a passing propagation
gate is the precondition for the dispatches it gates: the session
dispatches the audit over the document, fixes its hits, and repeats
until no confirmed hit remains, so an expensive reader only ever meets
a mechanically consistent document. The gate fires before every
verdict-agent dispatch, first rounds included — authoring errors exist
before any repair; after a fix wave, before the next round; and before
an integrity audit. A hit's fix is licensed by its own derivation — a
recounted counter and an enumerated missed call site decide
themselves — so hits never wait for the developer.

A report's body governs, never its closing token. Where a report lists
located hits and also carries `CLEAN`, the hits are the report and the
gate has not passed. It has happened more than once on the cheapest
family, and once under a brief that ruled the combination out in as
many words — so emphasis on the writing side is spent, and the guard
belongs to the dispatcher who reads. The rule is stated here rather
than generalised, because `CLEAN` is this agent's token and no other
report carries one.

A hit the session believes is wrong is dismissed, never silently: the
session writes the `dismissed` line the spec-plan-lifecycle rule
defines and reports the dismissal in the next report it relays to the
developer. A hit is a report, not a question, so it never enters the
held batch and never spends the round's one interruption — the
developer reads the dismissal and keeps their standing veto over it.
The written line is what makes the gate terminate: a dismissed hit
recurs on every re-dispatch, so a gate waiting on a hitless audit would
wait forever, and a dismissal nobody wrote down would be re-derived
from nothing every round. Both dispositions take the gate lines the
spec-plan-lifecycle rule defines.

Two re-dispatches bound one gate episode — the run before a single
dispatch, never the document's lifetime, so every round gets its own
gate. A third is not attempted. The session reports the hits still
outstanding, with the standing of a dismissal, and holds the dispatch
the gate was guarding: a gate that cannot come clean has not done the
one job the expensive reader depends on. The report names what keeps
recurring, since fixes breeding fresh hits is the failure this bound
exists to catch. It stays a report — the developer may order the
dispatch anyway, as they may order any step — so it never becomes a
second question in a round that already spent its one. Without the
agent installed, every dispatch proceeds as it did before.

### Re-dispatch briefs

The first round reads the whole document; every later round is
diff-scoped. Its brief names what changed since the round it follows,
directs the reviewer to attack the previous wave's fixes first, and
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
  what the folded line records, the base the spec-plan-lifecycle rule
  defines — which routes to `held` rather than to a fold. A line
  carrying `ruling:` is settled by that clause; a historical line
  written before this design, `resolved <date> (declined)` included,
  carries no authorizer clause and is settled by its token alone. Both
  are the developer's decisions, and both are protected on the same
  footing;
- `held` lines carry questions already put, so a round does not
  duplicate one;
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
under the heading of the round that gave it, in the shape the
spec-plan-lifecycle rule defines. A signal surviving only in a relay
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
  instead, and the spec-plan-lifecycle rule owns it.

The cap guards spend and the signal guards sense; both escalate, and
neither is a wall. Relay stays the developer's standing veto — every
report reaches them before the session acts on it — and a model-cap
refusal mid-loop forces developer contact: the drop-or-wait
question above is never answered autonomously.

### What a diff-scoped LGTM certifies

A diff-scoped LGTM certifies a chain rather than a fresh whole-document
read: round 1 read the whole document, and every later wave was
reviewed by the round that followed it. What that chain still owes
differs by document.

For a spec, the consumption gate before plan-writing offers the pair as
one question — an integrity audit or a full-document round — and never
an offer followed by a re-offer of the option just declined. When the
`integrity-auditor` agent is absent the offer carries the full-document
round alone. The two arms cost differently and the offer says so: an
audit returns material for the dispatcher to dispose of and leaves the
verdict alone, while a full-document round on a spec is a new loop's
first round, since the spec's LGTM already closed its loop — it mints
its own verdict and stamps it, so a `concerns` there flips the field
back while plan-writing waits. The full-document-round arm therefore
blocks plan-writing; the audit arm does not, and plan-writing follows
its dispositions.

Declining is the developer discharging the chain debt by release rather
than by performance, and the discharge is recorded rather than
remembered: the dispatcher appends `, debt discharged <date>` to the
diff-scoped LGTM heading, in the shape the spec-plan-lifecycle rule
defines, and that annotation defeats the gate's re-ask. The other two
paths write the same token.

For a plan the loop closes only when the latest verdict round was
full-document: whatever ends its rounds while the latest round heading
is diff-scoped, one confirming full-document round follows, and that
round's verdict is the one stamped. A round already full-document owes
no successor — it is the close. The confirming round inherits the gating
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

The `## Dispatching a verdict agent` section above — its bullet list
and every subsection under it, this one included — and the lifecycle
rule's relay-then-stamp sentence state the same relay-before-stamp
ordering and are edited together when that changes. The other checks
this section sequences inside the dispatch turn are its own; adding one
leaves that sentence correct.
