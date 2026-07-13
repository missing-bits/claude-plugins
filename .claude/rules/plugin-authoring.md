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
- Names are kebab-case. Interactive skills are named `*-session`; formal
  reviews that end in a verdict are agents.
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
