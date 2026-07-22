# Missing Bits — Claude Code plugins marketplace

This repo *is* the `missing-bits` Claude Code plugin marketplace: its
product is the plugins themselves — their skills, agents, hooks, and
distributed rules.

## Layout

- `plugins/<name>/` — one directory per plugin (manifest under
  `.claude-plugin/`, plus `skills/`, `agents/`, `hooks/`, `rules/`).
- `.claude-plugin/marketplace.json` — the marketplace catalog.
- `docs/specs/`, `docs/plans/` — spec-driven working-process artifacts.

## Conventions

Repo conventions load automatically from `.claude/rules/` — plugin
authoring, versioning, marketplace sync, and public-repo hygiene. They
override defaults; follow them.

## Worktrees and topic branches

Feature work happens on a topic branch named `feature/<issue>-<short-name>`
(e.g. `feature/6-salesforce-standards`), branched off `master`. When an
isolated workspace is used, its git worktree lives at
`.claude/worktrees/<short-name>/` — one per topic branch, git-ignored.

## Authoring skills

When creating or editing a skill in any plugin, use the `skill-creator`
skill (when available) for scaffolding, `description:` tuning, and evals.
It complements `superpowers:writing-skills` — the content-authoring
discipline — rather than replacing it. Details in the plugin-authoring
rule.
