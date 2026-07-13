# working-process

Tech-agnostic tooling for a spec-driven working process on top of the
`superpowers` plugin:

idea → brainstorming (spec) → grilling-session → architect review →
writing-plans (plan) → plan-adversary → implementation.

## Components

- **`grilling-session` skill** — stress-tests a spec (the primary
  target), plan, or raw idea against the project's domain glossary
  (`docs/domain/glossary.md`), sharpens terminology, and records
  decisions as ADRs. Triggers: "grill me" / "przemagluj".
- **`architect` agent** — formal design-quality review of a grilled spec
  or any design document dispatched standalone; verdict
  `LGTM | concerns | blocking`, stamped into the reviewed document's
  `architect:` frontmatter field by the dispatcher.
- **`architect-session` skill** — the same persona as an interactive
  in-session consultation: no verdict, no stamping; hands off to a
  grilling-session or an `architect` dispatch. Triggers: "ask the
  architect" / "porozmawiajmy z architektem".
- **`plan-adversary` agent** — adversarial review of implementation
  plans (plans only; handed a spec it declines toward the `architect`
  agent). Generic failure-mode dimensions live here; domain specifics
  come from `*-plan-review` checklist skills.

The architect persona is single-sourced in [PERSONA.md](./PERSONA.md),
shared by the `architect` agent and the `architect-session` skill. Every
component reads `docs/domain/glossary.md` and `docs/domain/adr/` first,
when they exist, so it speaks the project's language from its first
message.

## Requirements

- Claude Code ≥ 2.1.207 (verified — rules distribution needs subdirectory
  rules loading; the skills and agents alone work on ≥ 2.1.143).
- The `superpowers` plugin — declared as a dependency and installed
  automatically alongside this plugin.

## Extending with a domain checklist

Ship a skill named `<domain>-plan-review` in your domain plugin. Its
description starts with `Plan-review checklist for <domain>` and ends
with `invoked by the plan-adversary agent`. plan-adversary discovers the
skill by name and walks its dimensions whenever a reviewed plan touches
that domain — e.g. a `salesforce-plan-review` skill for Salesforce
projects. Domains without a checklist get the generic dimensions only.

## Frontmatter process fields

Stamped only in documents that open with a YAML frontmatter block
containing a `status` field:

| Field | Values | Meaning |
|---|---|---|
| `status` | `draft → approved → implemented` | document lifecycle |
| `grilled` | `grilling` \| ISO date | session open / all outcomes applied |
| `architect` | `LGTM` \| `concerns` \| `blocking` | latest architect verdict |
| `adversary` | `LGTM` \| `concerns` \| `blocking` | latest plan-adversary verdict |

Find unfinished work:

    rg -l '^grilled: grilling' docs/
    rg -l '^architect: (blocking|concerns)' docs/
    rg -l '^adversary: (blocking|concerns)' docs/

## Process rules

The plugin ships four rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, and ticket frontmatter. Claude Code does
not load plugin rules by itself: install them with the
`working-process:sync-rules` skill.

- **Two targets**: user level (`~/.claude/rules/`, recommended — one
  install per machine) or project level (`.claude/rules/`, per-repo
  adoption; committed rules also work for teammates without the plugin).
- **Updates**: a SessionStart hook compares content hashes and leaves a
  one-line note when the installed rules differ from the plugin's
  current ones; run sync-rules to review. Locally modified files are
  never overwritten silently.
- **Uninstalling the plugin**: run sync-rules uninstall FIRST — the
  plugin gets no signal on its own removal, and rule sets left behind
  lose their update detection.
- **Other plugins**: any plugin of this marketplace can ship a `rules/`
  directory; this plugin's engine discovers, installs, and updates those
  payloads the same way.
- **Requirements**: Claude Code with rules support incl. subdirectories
  (verified on 2.1.207); `jq` only for payloads of other plugins.

## Process directories

The one directory this plugin creates in a project repo is
`docs/domain/` (glossary + ADRs). On first creation the developer is
asked whether it should be git-ignored (a `.gitignore` containing `*`)
or committed; an existing directory's state is respected without asking.
