---
paths:
  - "plugins/**"
---

# Plugin versioning

- Every plugin follows semver in its `.claude-plugin/plugin.json`
  `version` field.
- `develop` is the integration branch: topic branches merge into it
  WITHOUT version bumps — unfinished plugin updates accumulate there
  unreleased. `master` holds released state only; the marketplace
  serves it.
- The bump happens exactly once, in the release PR from `develop` to
  `master`: one commit bumps every plugin changed since the last
  release, sized by the total accumulated change per plugin. The
  `version` field is the update-delivery mechanism, not hygiene:
  merging to master without changing that string delivers nothing to
  existing users, so a release PR with no bumps for its changed
  plugins is invalid.
- Dogfooding unreleased content needs a changed version string — the
  plugin cache keys content by version. A topic branch that dogfoods a
  plugin sets `X.Y.Z-dev.<discriminator>` on it — the issue number the
  branch name carries, or the branch short-name when the topic has no
  issue (e.g. `-dev.design-personas`). Widening the discriminator
  instead of minting another channel keeps one channel for one purpose;
  the discriminator only needs to be unique among parallel topics. The
  suffix flows into develop as-is. A topic that
  does not dogfood never touches the version. On a version-line merge
  conflict between parallel topics, the merging topic's own
  `-dev.<discriminator>` wins — both strings are provisional. The release PR
  strips every `-dev` suffix while minting the final numbers; the
  `release-guard` workflow fails any PR to master that carries a
  prerelease version or a changed plugin without a bump.
- Prerelease grammar: `-<channel>.<discriminator>`. Defined channels:
  `dev.<discriminator>` (topic-branch dogfooding, above) and `rc.<n>` (release
  candidate — a freeze of develop dogfooded as one bundle when a
  release warrants whole-unit validation; minted by a release-prep
  commit and stripped by the release PR like any prerelease). Future
  channels extend this list by editing this rule only — the
  release-guard workflow rejects every prerelease on master
  (`*-*`), so new channels never need a CI change.
  - **patch** — wording or docs fixes, no behavior change;
  - **minor** — a new component or section, backward-compatible behavior
    additions;
  - **major** — rename or removal of a component, or a breaking change to
    a convention others rely on (the frontmatter process fields, the
    `*-plan-review` discovery convention, the plugin-root persona paths —
    `ARCHITECT_PERSONA.md`, `SYSTEM_DESIGNER_PERSONA.md`,
    `PERSONA_COMMON.md`).
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
