---
paths:
  - ".claude-plugin/**"
  - "plugins/*/.claude-plugin/**"
  - "README.md"
---

# Marketplace synchronization

A plugin's public identity lives in three places: its
`.claude-plugin/plugin.json`, its entry in the marketplace catalog
(`.claude-plugin/marketplace.json`), and the plugin table in the repo
`README.md`.

- The name is IDENTICAL in all three. The `plugin.json` description is
  canonical; the catalog entry and the README row may shorten it but never
  contradict it.
- Any edit to a plugin's name or description → touch all three places in
  the same commit.
- A new plugin lands with all three at once: manifest, catalog entry,
  README row.
- A rename or removal also updates the catalog's `renames` map — see the
  plugin versioning rule.
- A new cross-marketplace dependency requires its marketplace to be listed
  in the top-level `allowCrossMarketplaceDependenciesOn` field of the
  catalog, in the same commit as the dependency.
