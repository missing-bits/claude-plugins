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

- Claude Code ≥ 2.1.143.
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

## Process directories

The one directory this plugin creates in a project repo is
`docs/domain/` (glossary + ADRs). On first creation the developer is
asked whether it should be git-ignored (a `.gitignore` containing `*`)
or committed; an existing directory's state is respected without asking.
