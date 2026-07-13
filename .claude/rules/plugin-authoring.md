---
paths:
  - "plugins/**"
---

# Plugin authoring conventions

- **Frontmatter safety**: quote any `description:` (or other scalar) that
  contains `: ` (colon+space) — unquoted it breaks the YAML parse and the
  component silently loads with empty metadata.
- **Validate before committing**: `claude plugin validate .` and
  `claude plugin validate plugins/<name>` must both pass.
- Names are kebab-case. Skills whose content is an open-ended
  conversation are named `*-session`; formal reviews that end in a verdict
  are agents. Operational skills may prompt for decisions without being
  sessions — they are named for what they do (e.g. `sync-rules`).
- A shared asset moves to the plugin root only when it has at least two
  consumers; with one consumer it stays in that consumer's directory.
- Reference files inside a plugin via `${CLAUDE_PLUGIN_ROOT}/…` (works in
  both skill and agent content), never via absolute paths.
- When editing text that names a superpowers skill or agent (handoffs,
  flow descriptions), verify the name against the currently installed
  superpowers release — the dependency carries no version constraint, so
  an upstream rename breaks handoffs silently.
- Public-repo hygiene rules live in the repo-wide
  [repo-hygiene](./repo-hygiene.md) rule.

## Rules payload

A plugin of this marketplace that ships a `rules/` directory (picked up by
working-process's sync-rules engine) additionally follows:

- Every domain rule carries a `paths:` frontmatter block. A rule without
  `paths:` loads in every session on machines with a user-level install —
  in a domain plugin that is a red flag needing explicit justification.
- Mentions of skills and agents inside rule text are conditional ("when
  the X skill is available…") — committed project-level rules load for
  people who do not have the plugin.
- Frontmatter safety applies doubly: `claude plugin validate` does NOT
  check `rules/` (it is not a plugin component), so an unquoted `: ` in a
  scalar fails silently at load time. Review rule frontmatter by hand.
- Any change under `rules/` bumps the plugin version like any other file
  (see [plugin-versioning](./plugin-versioning.md)) — the bump is what
  delivers the update nudge to installed copies.
