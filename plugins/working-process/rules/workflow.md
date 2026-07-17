# Working process — preferred flow

A spec-driven flow for non-trivial work. Every step below is an offer:
suggest it, let the developer decline. A tool that is not installed
disables its suggestion — never the work itself.

1. **Idea → spec.** When the superpowers:brainstorming skill is
   available, start non-trivial features there; capture the agreed design
   as a spec in `docs/specs/`.
2. **Spec → grilling.** Once a spec exists, offer a grilling-session
   (when the working-process plugin is installed) to stress-test its
   language against the project's domain terms.
3. **Grilled spec → architect review.** Offer a dispatch of the
   working-process architect agent (when available); stamp its verdict
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

After every architect or plan-adversary round, record the verdict
(`LGTM` | `concerns` | `blocking`) in the reviewed document's
`architect:` / `adversary:` frontmatter field.

Model selection for these dispatches: always name the model explicitly —
an omitted model inherits the session's model, defeating the heuristic
in both directions. Reviews are never dispatched on the cheapest
available family. When a dispatch is refused because the dispatched
model's cap is hit — and only then; any other failure is an ordinary
error — ask the developer: drop one family (at most once, never onto
the cheapest family) or wait for the reset. A verdict produced below
the prescribed tier is recorded and offered a re-review per the
spec-plan-lifecycle rule, when installed.

When `docs/domain/glossary.md` exists in the project, its canonical
terms and `_Avoid_` bans bind specs, plans, code identifiers, and
reviews.
