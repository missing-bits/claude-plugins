---
ticket: none
date: 2026-07-13
status: implemented
grilled: 2026-07-13
architect: LGTM
branch: feature/working-process
base: master
---

# working-process plugin — design

## Context

`working-process` is the first plugin of the `missing-bits` marketplace:
tech-agnostic tooling for a spec-driven working process on top of the
`superpowers` plugin. The flow it supports:

idea → brainstorming (spec) → **grilling-session** on the spec →
**architect** review → writing-plans (plan) → **plan-adversary** on the
plan → implementation.

This is spec 1 of 2. Spec 2 (separate document, not yet written) will cover
shipping process rules (`.claude/rules/*.md`) with the plugin and the
install/update mechanism they require.

## Goals

- The plugin installs from the `missing-bits` marketplace and works in any
  project, with no assumptions about a specific company or environment.
- Its dependency on the `superpowers` plugin is declared and resolved
  automatically at install time.
- Directory-creating behavior asks the developer instead of assuming
  (first-create question, see below).

## Non-goals

- No rules distribution or installer (spec 2).
- No domain-specific review content — domain knowledge plugs in through
  the `*-plan-review` extension convention, never into this plugin.
- Coexistence with another installed plugin named `working-process` (from
  a different marketplace) is out of scope: skills and agents are
  namespaced by plugin name, so two same-named plugins would produce
  ambiguous identifiers — install one at a time.

## Design

### Components

Four components share one process; a common persona file is single-sourced.

**Glossary-first rule** — every component starts by reading
`docs/domain/glossary.md` and `docs/domain/adr/` when they exist (for the
agents, right after the persona load). Canonical terms and `_Avoid_` bans
bind the component's own language from its first message — a
grilling-session opens speaking the project's terms instead of arriving at
them through corrections.

**`grilling-session` skill** — interactive grilling session that
stress-tests a spec (the primary target), plan, or raw idea against the
project's domain glossary
(`docs/domain/glossary.md`) and recorded ADRs (`docs/domain/adr/`).
Mechanics:

- One question at a time, a recommendation per question; facts answerable
  from code or project metadata are read, not asked.
- Glossary updates are applied inline as terms resolve; ADRs are offered
  sparingly (hard to reverse + surprising without context + real
  trade-off).
- Frontmatter stamping, only in documents that open with a YAML block
  containing a `status` field: `grilled: grilling` at session start,
  replaced with the ISO date once every outcome is applied. An interrupted
  session deliberately leaves `grilling` behind as greppable debt.
- Formats for the glossary and ADRs ship as companion files in the skill
  directory (`GLOSSARY-FORMAT.md`, `ADR-FORMAT.md`).
- Trigger phrases are bilingual: "grill me" / "przemagluj".

**`architect` agent** — formal design-quality review of a grilled spec
(primary target) or any design document or question dispatched standalone.
Judges problem–solution fit, component boundaries, YAGNI, alternatives,
and consistency with project conventions; adopts domain-expert roles
inferred from the subject (a dispatch hint is verified, otherwise
self-inferred) and declares assumed domains at the top of the report.
Findings carry severity (Critical / Important / Minor in design terms) and
evidence. Verdict `LGTM | concerns | blocking` (`blocking` = ≥1 Critical or
≥2 Important); the dispatcher stamps it in the reviewed document's
`architect:` frontmatter field. Failure-mode hunting on plans is out of its
scope (that is plan-adversary's job).

**`architect-session` skill** — the same persona as an interactive
in-session consultation: challenge, compare, sketch alternatives; may
simply ask the developer which domains matter. Hard limits: no verdict, no
`architect:` stamping — the formal review belongs exclusively to an
`architect` agent dispatch, whose fresh unbiased context is the point.
Hands off to `grilling-session` (new terms/decisions) or an `architect`
dispatch (document ready for review). Trigger phrases bilingual: "ask the
architect" / "porozmawiajmy z architektem".

**`plan-adversary` agent** — adversarial reviewer for implementation plans
(plans only: handed a spec, it declines and points at the `architect`
agent). Walks generic failure-mode dimensions — scope vs done-when,
verification, backwards compatibility, plan smells — plus domain
checklists: it discovers skills named `*-plan-review` and walks their
dimensions for the domains the plan touches. Severity-graded findings with
evidence; a domain checklist's severity mapping wins over generic
re-grading. Verdict thresholds match the architect agent's, and the
dispatcher stamps the verdict into the reviewed plan's `adversary:`
frontmatter field. Contradicting the project glossary or a recorded ADR
is a finding.

**Persona single-sourcing** — the architect persona (design-quality
dimensions, domain-expert role adoption, glossary/ADR duty) lives at the
plugin root, `PERSONA.md` — a neutral home for its two consumers: the
`architect` agent and the `architect-session` skill both load it via
`${CLAUDE_PLUGIN_ROOT}/PERSONA.md` as their first action.

### Extension convention

A domain plugin ships a skill named `<domain>-plan-review` whose
description starts with `Plan-review checklist for <domain>` and ends with
`invoked by the plan-adversary agent`. The agent discovers it by name and
walks its dimensions when the reviewed plan touches that domain (e.g. a
hypothetical `salesforce-plan-review` for Salesforce projects). Domains
without a checklist get the generic dimensions only.

### Superpowers dependency

The flow builds on superpowers skills (brainstorming, writing-plans), so
the plugin declares a hard dependency. A soft alternative (a README
recommendation, no `dependencies` entry) was considered and rejected: the
plugin's components hand off to superpowers skills by name, so a missing
superpowers install silently breaks the flow the plugin exists to support.

- `plugin.json`:

  ```json
  "dependencies": [
    { "name": "superpowers", "marketplace": "claude-plugins-official" }
  ]
  ```

- The marketplace allows the cross-marketplace dependency via the
  **top-level** `allowCrossMarketplaceDependenciesOn` field of
  `.claude-plugin/marketplace.json` (a sibling of `plugins`, not part of
  the plugin entry):

  ```json
  {
    "allowCrossMarketplaceDependenciesOn": ["claude-plugins-official"],
    "plugins": [ ... ]
  }
  ```

- Effect: `/plugin install working-process@missing-bits` auto-installs
  superpowers; enabling the plugin enables the dependency; disabling
  superpowers is blocked while working-process requires it. Requires
  Claude Code ≥ 2.1.143; the README notes the requirement.

### First-create question: ask, don't assume

Process directories are directories the working process creates in a
project repo; for this plugin that is `docs/domain/` (glossary + ADRs),
created by grilling-session.

- **First creation** of a process directory: the skill asks the developer
  whether the directory should be git-ignored (create a `.gitignore`
  containing `*` — ignored mode) or committed (no `.gitignore` — tracked
  mode). No default is assumed.
- **Directory already exists**: never ask when a prior decision is
  observable. A `.gitignore` with `*` means ignored mode; any git-tracked
  file under the directory means tracked mode. Neither signal present →
  no decision was ever made: ask, exactly as on first creation.
- Scope split: this spec applies the first-create question only where this
  plugin is in control (`docs/domain/` via grilling-session). Extending the
  convention to process directories created by other tooling
  (`docs/specs/`, `docs/plans/`) belongs to spec 2's rules.
- In tracked mode, the session ends by listing the artifact files it
  modified and reminding the developer they belong in the current work's
  commit; the skill never commits.

### Metadata and marketplace registration

- `plugin.json`: name `working-process`, author Jacek Nakonieczny, license
  MIT (matching the repo license), version 0.1.0, the dependency block
  above, and a description naming the four components.
- `.claude-plugin/marketplace.json`: `working-process` entry with source
  `./plugins/working-process`, plus the top-level
  `allowCrossMarketplaceDependenciesOn` field described above.
- Repo README: plugin table gains the `working-process` row.
- Plugin README: components overview, the extension convention, the
  frontmatter process fields (`status`, `grilled`, `architect`,
  `adversary`) with their value sets, and the superpowers/Claude Code
  version requirement.

## Verification

1. `/plugin marketplace add` pointing at the local repo path.
2. `/plugin install working-process@missing-bits` — superpowers is
   auto-resolved (or already present) and the install succeeds.
3. Skills `working-process:grilling-session` and
   `working-process:architect-session` and agents `architect` and
   `plan-adversary` are visible in the session.
4. The `architect` agent's persona path resolves: dispatch it against a
   trivial design question and confirm it adopts the persona and opens
   with an Assumed domains section.
5. Grill a scratch document in a scratch repo: confirm the first-create
   question fires on `docs/domain/` creation and does not fire when the
   directory already exists in either mode.

## Process notes

- Work happens on `feature/working-process` (base `master`) in
  `missing-bits/claude-plugins`.
- `docs/specs/`, `docs/plans/`, and `docs/domain/` in this repo are in
  tracked mode (no `.gitignore`) by the developer's decision.
