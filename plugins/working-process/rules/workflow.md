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
4. **Spec → plan.** Write the implementation plan with
   superpowers:writing-plans when available; plans live in `docs/plans/`.
5. **Plan → adversary review.** Before implementing a non-trivial plan,
   offer a working-process plan-adversary agent dispatch (when
   available); stamp its verdict into the plan's `adversary:` field.
6. **Implementation.** Test-driven when
   superpowers:test-driven-development is available; bugs go through
   superpowers:systematic-debugging when available.

After every architect or plan-adversary round, record the verdict
(`LGTM` | `concerns` | `blocking`) in the reviewed document's
`architect:` / `adversary:` frontmatter field.

When `docs/domain/glossary.md` exists in the project, its canonical
terms and `_Avoid_` bans bind specs, plans, code identifiers, and
reviews.
