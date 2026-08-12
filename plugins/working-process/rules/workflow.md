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
   working-process `architect` agent (when available); stamp its verdict
   into the spec's `architect:` frontmatter field.
   Dispatch it on the most capable available model, named explicitly.
4. **Spec → plan.** Write the implementation plan with
   superpowers:writing-plans when available; plans live in `docs/plans/`.
5. **Plan → adversary review.** Before implementing a non-trivial plan,
   offer a working-process plan-adversary agent dispatch (when
   available); stamp its verdict into the plan's `adversary:` field.
   Dispatch it on a model scaled to the plan's size, complexity, and
   risk — the most capable available for complex or risky plans, one
   family below for small mechanical ones — named explicitly.
6. **Implementation.** Test-driven when
   superpowers:test-driven-development is available; bugs go through
   superpowers:systematic-debugging when available.

After every round of the `architect` agent or plan-adversary, record the
verdict (`LGTM` | `concerns` | `blocking`) in the reviewed document's
`architect:` / `adversary:` frontmatter field. A consultation
(`*-consult`) produces no verdict and nothing to record.

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
