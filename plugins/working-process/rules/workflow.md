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
   is available: a fresh-context read of the whole spec, returning
   defects and the questions an implementer would have to ask. For a
   spec whose LGTM came from a diff-scoped chain the offer takes the
   pair form the verdict-agent dispatch subsection defines, and narrows
   as that definition says when the auditor is absent. Then write the
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
question appended, and tell neither what the other said. Relay each
contribution attributed and substantially verbatim, disagreements
presented as disagreements, and dispatch as a named background agent so
the transcript stays inspectable.

When `docs/domain/glossary.md` exists in the project, its canonical
terms and `_Avoid_` bans bind specs, plans, code identifiers, and
reviews.

When the `elements-of-style:writing-clearly-and-concisely` skill is
available, prose artifacts under `docs/` — specs, plans, ADRs, the
glossary — get its pass: invoke it before drafting a new document, and
run an explicit editing pass over the changed prose of an existing one.
The pass binds wording, never decisions. Without the skill there is no
substitute pass and no install nagging — the work proceeds normally.

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
  rule defines), relay the report to the developer, then stamp the
  verdict (`LGTM` | `concerns` | `blocking`) into the reviewed
  document's `architect:` / `adversary:` frontmatter field.
- The relay carries the verdict, the model self-report, and every
  finding in substance — condense narrative prose, never drop a
  finding or its severity.
- The stamp — the field, any fallback record, and the round record
  the lifecycle rule defines — lands as one edit, body record first
  where edit granularity forces separate writes, and goes to the
  document named in the report, never to "the most recent dispatch".
- The sequence ends the delivery, not the loop: after relay and stamp
  the session may fix the document and dispatch a fresh round, or put
  its questions to the developer first.
- At most one live round per document per field within the session;
  superseding a running round stops it when the platform offers a
  stop, otherwise the stale result is relayed as stale and never
  stamped.
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
without asking again. A durable preference in the developer's own
instructions is respected when present. Without consent every round
behaves as it did before: relay, stamp, and every proposal waits for
the developer.

Triage decides each finding by its license, never by its grade. A
finding is self-fixable when the session can cite the decision that
licenses the fix — a statement in the document itself, a glossary term
or `_Avoid_` ban, a recorded ADR, or a previously resolved `held`
line — and the citation goes on the finding's line in the disposition
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

When the `propagation-auditor` agent is available, a clean propagation
audit is the precondition for the dispatches it gates: the session
dispatches the audit over the document, fixes its hits, and repeats
until the audit returns no hits, so an expensive reader only ever meets
a mechanically consistent document. The gate fires before every
verdict-agent dispatch, first rounds included — authoring errors exist
before any repair; after a fix wave, before the next round; and before
an integrity audit. A hit's fix is licensed by its own derivation — a
recounted counter and an enumerated missed call site decide
themselves — so hits never wait for the developer; a hit the session
believes is wrong escalates as held, its line carrying `[hit]` in the
severity slot, because a hit stays ungraded even when contested.
Without the agent installed, every dispatch proceeds as it did before.

### Re-dispatch briefs

The first round reads the whole document; every later round is
diff-scoped. Its brief names what changed since the round it follows,
directs the reviewer to attack the previous wave's fixes first, and
forbids re-reviewing the rest — repair-born defects are the dominant
late-round class, and diff-scoping also ends stale-read findings.

Every brief states the loop's terminators outright — the cap and the
all-Minor signal below — rather than improvising them late, and asks
the reviewer for its own stop signal: when the round's remaining
findings are all Minor wording residue, say so and judge whether
another round earns its cost. That judgment concerns the next round's
marginal value, never whether the document is good enough, and it
informs the developer's decision rather than replacing it. Where the
ledger records a deviation from a reviewer's suggestion, the brief
invites refutation of the recorded rationale — a rationale is evidence
to attack, never a defence to protect.

### Terminators

- `LGTM` ends the loop — on a plan, only a full-document round's LGTM
  does.
- `blocking` suspends autonomy entirely: relay, stamp, stop. A blocking
  round licenses no self-fixes, because reshaping a design the reviewer
  judged broken as a whole is design work and re-enters through the
  design conversation. `concerns` is the autonomy zone.
- Round cap: three autonomous rounds per document per field without
  developer contact. Hitting the cap escalates in one batch — what was
  fixed, what remains, why — rather than halting silently, and any
  developer contact resets the count.
- All-Minor signal: two consecutive rounds whose findings are all Minor
  end the unattended run. Fix the residue, annotate
  `concerns (resolved <date>)`, and escalate with an offer of a fresh
  round instead of dispatching one.
- Oscillation tripwire: a finding re-raised against a `fixed` line is
  never re-fixed autonomously. Two readings of one license are a
  contested reading, so it escalates as held, the flip named.

The cap guards spend and the signal guards sense; both escalate, and
neither is a wall. Relay stays the developer's standing veto — every
report reaches them before the session acts on it — and a model-cap
refusal mid-loop is already developer contact: the drop-or-wait
question above is never answered autonomously.

### What a diff-scoped LGTM certifies

A diff-scoped LGTM certifies a chain rather than a fresh whole-document
read: round 1 read the whole document, and every later wave was
reviewed by the round that followed it. What that chain still owes
differs by document.

For a spec, the consumption gate before plan-writing offers the pair as
one question — an integrity audit or a confirming full-document round —
and never an offer followed by a re-offer of the option just declined.
When the `integrity-auditor` agent is absent the offer carries the
confirming round alone. Declining is the developer accepting the chain
explicitly, and the acceptance is recorded rather than remembered: the
dispatcher appends `, chain accepted <date>` to the diff-scoped LGTM
heading, and that annotation defeats the gate's re-ask.

For a plan the loop never terminates on a diff-scoped LGTM: one
full-document confirming round follows, and the confirming round's
verdict is the one stamped. That carries the single named exception to
the relay-then-stamp order above — a plan's diff-scoped LGTM is relayed
and its round record written, and only the frontmatter stamp waits for
the confirming round. Recovery therefore reads the ledger rather than
the stamp: a plan whose latest round heading is a diff-scoped LGTM that
no later full-document round follows is re-offered its confirming round
at the document's next touch, whatever the frontmatter says.

Scoping never spans a close. An annotation close ends the loop, and a
later round on the same document opens a new one, reading the whole
document again.

This subsection and the lifecycle rule's relay-then-stamp sentence
state the same ordering and are edited together.
