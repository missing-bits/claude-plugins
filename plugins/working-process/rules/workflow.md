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
4. **Spec → plan.** Write the implementation plan with
   superpowers:writing-plans when available; plans live in `docs/plans/`.
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

Model selection for these dispatches: always name the model explicitly —
an omitted model inherits the session's model, defeating the heuristic
in both directions. Reviews are never dispatched on the cheapest
available family. Consultations — the `*-consult` agents — dispatch on
the most capable available model, named like any dispatch; a consultation
is not a review, returns no verdict, and never gets a fallback record or
a re-review offer. When a dispatch is refused because the dispatched
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
  dispatcher cannot relay, so it never stamps; the next interactive
  touch closes the round through the lifecycle rule's re-offer loop.
- Before dispatch, resolve any undecided Process directory
  (`docs/specs/`, `docs/plans/`) so the first-create question cannot
  interrupt the stamp turn.
- At dispatch, tell the developer the round is running in the
  background and its result will arrive as a task notification, with
  progress visible in the session's task list. (This bullet is part of
  the spec's sequence — added there 2026-08-17, routed from this
  plan's adversary round 4.)
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

This subsection and the lifecycle rule's relay-then-stamp sentence
state the same ordering and are edited together.
