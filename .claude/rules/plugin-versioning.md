---
paths:
  - "plugins/**"
---

# Plugin versioning

- Every plugin follows semver in its `.claude-plugin/plugin.json`
  `version` field.
- A commit/PR that changes ANY file under `plugins/<name>/` bumps that
  plugin's version IN THE SAME commit/PR. The `version` field is the
  update-delivery mechanism, not hygiene: pushing new commits without
  changing that string delivers nothing to existing users.
  - **patch** — wording or docs fixes, no behavior change;
  - **minor** — a new component or section, backward-compatible behavior
    additions;
  - **major** — rename or removal of a component, or a breaking change to
    a convention others rely on (the frontmatter process fields, the
    `*-plan-review` discovery convention, the plugin-root persona path —
    `ARCHITECT_PERSONA.md`).
  - Before 1.0.0, breaking changes ride a **minor** bump (semver's 0.x
    rule); major is reserved for the promotion to 1.0.0 and for breaking
    changes after it.
- Release tags use the `{plugin}--v{version}` format
  (`claude plugin tag --push`). Start tagging on the first external
  breakage report or when plugins in this marketplace pin each other —
  not before; tags can be backfilled onto the historical version-bump
  commits.
- Public rename or removal of a plugin: add an entry to the `renames` map
  in `.claude-plugin/marketplace.json` so installed copies migrate
  (Claude Code ≥ 2.1.193 only — older installs will not follow the
  rename), and never reuse a retired public name for a different plugin.
- Deprecate before removing: mark a component as deprecated in the plugin
  README (and its description) at least one minor release before the major
  that removes it.
