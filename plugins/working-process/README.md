# working-process

Tech-agnostic tooling for a spec-driven working process on top of the
`superpowers` plugin:

idea → brainstorming (spec) → grilling-session → architect review →
integrity audit → writing-plans (plan) → plan-adversary →
implementation → code review — with a propagation audit gating every
verdict dispatch and the integrity audit itself.

## Components

- **`grilling-session` skill** — stress-tests a spec (the primary
  target), plan, or raw idea against the project's domain glossary
  (`docs/domain/glossary.md`), sharpens terminology, and records
  decisions as ADRs. Triggers: "grill me" / "grilling session".
- **`architect` agent** — formal design-quality review of a grilled spec
  or any design document dispatched standalone; verdict
  `LGTM | concerns | blocking`, stamped into the reviewed document's
  `architect:` frontmatter field by the dispatcher. Dispatched in the
  background on the most capable available model; the verdict arrives
  as a task notification and is stamped after the dispatcher relays
  the report. A round that trips over integrity-class textual defects —
  a contradiction between two sections, a count adrift from its list, a
  reference that drifted from what it names — notes the class in one
  line and leaves the enumeration to the integrity audit.
- **`architect-session` skill** — the same persona as an interactive
  in-session consultation: no verdict, no stamping; hands off to a
  grilling-session or an `architect` dispatch. Triggers: "ask the
  architect" / "architect session".
- **`architect-consult` agent** — the architect as a one-shot
  consultation from a fresh, isolated context: one briefing in, one
  contribution out, no verdict, nothing stamped. Dispatched as a named
  background agent on the most capable available model. Triggers:
  "second opinion from the architect" / "consult the architect from a
  clean context".
- **`system-designer-consult` agent** — the system designer persona
  (parts, contracts, state, behaviour under load, observability,
  technology choice) as the same kind of one-shot consultation.
  Triggers: "second opinion from the system designer" / "consult the
  designer from a clean context".
- **`system-designer-session` skill** — the system designer as an
  interactive in-session consultation; hands off to a grilling-session,
  a `system-designer-consult` dispatch (assembling its briefing), or an
  `architect` dispatch. Triggers: "ask the designer" / "system designer
  session".
- **`plan-adversary` agent** — adversarial review of implementation
  plans (plans only; handed a spec it declines toward the `architect`
  agent). Generic failure-mode dimensions live here; domain specifics
  come from `*-plan-review` checklist skills. Dispatched in the
  background, scaled to the plan's size and risk; the verdict arrives
  as a task notification and is stamped after relay.
- **`propagation-auditor` agent** — the mechanical audit of a spec or
  plan: it parses every changed interface to enumerate its consumers,
  diffs every prescribed block against the file it targets, re-derives
  every counter, and runs the document's own verification commands. Its
  unit is the hit: located, binary, and carrying the derivation that
  produced it; a clean audit reports the single line `CLEAN`. It grades
  nothing, ends in no verdict, and stamps nothing. Dispatched in the
  background on the cheapest available family, because every duty is
  procedural; the workflow gates every verdict-agent dispatch and every
  integrity audit on a passing run — no confirmed hit outstanding — and
  offers the same audit at authoring time after any multi-site edit.
- **`integrity-auditor` agent** — the judgment audit of a churned
  document, read on a fresh context: the document against itself, then
  the document as an implementer who must build from that text alone.
  It reports defects, each proved by two located quotes, beside a ranked
  list of the questions an implementer would have to ask; it grades
  nothing and ends in no verdict. Dispatched in the background on the
  most capable available tier, and offered at a spec's consumption gate
  before the plan is written. Once its dispositions land, the dispatcher
  records the run in the spec's `integrity:` field.
- **`process-status` skill** — reports what the process left unfinished
  in the current repo: a pending grilling, an unresolved verdict, an
  unfinished review-loop ledger (an `open` or `held` disposition line,
  counted only inside a `## Review rounds` section), a re-review nobody
  ran, a stamp outside the top level of a frontmatter block. Runs the
  Unfinished-work list the lifecycle rule publishes and fires none of
  the offers those classes name. Triggers: "what is unfinished" /
  "process status".
- **`sync-rules` skill** — installs, updates, and uninstalls the rule
  files shipped by plugins of this marketplace (Rules payloads); see the
  "Process rules" section.

Each persona is single-sourced in its file at the plugin root —
[ARCHITECT_PERSONA.md](./ARCHITECT_PERSONA.md) and
[SYSTEM_DESIGNER_PERSONA.md](./SYSTEM_DESIGNER_PERSONA.md) — with the
shared duties, the persona boundary, and the consultation contract held
once in [PERSONA_COMMON.md](./PERSONA_COMMON.md). `plan-adversary`
sources its standing duties from the same shared file without being a
persona; the two `*-auditor` agents inherit neither persona nor standing
duties and carry what they need in their own files. Every component
reads `docs/domain/glossary.md` and `docs/domain/adr/` first, when they
exist, so it speaks the project's language from its first message.

## Requirements

- Claude Code ≥ 2.1.207 (verified — rules distribution needs subdirectory
  rules loading; the skills and agents alone work on ≥ 2.1.143).
- The `superpowers` plugin — declared as a dependency and installed
  automatically alongside this plugin.
- Optional companion: the `elements-of-style` plugin. When its
  `writing-clearly-and-concisely` skill is present, the process rules
  route prose artifacts under `docs/` through it; without it nothing
  changes. Not a dependency — install it yourself:

      /plugin marketplace add obra/superpowers-marketplace
      /plugin install elements-of-style@superpowers-marketplace

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
| `architect-fallback` / `adversary-fallback` | `<model> (degraded <date>)` \| `<model> (chosen <date>)` \| `…, waived <date>` | verdict produced below the prescribed tier (`degraded` = unchosen, `chosen` = deliberate); re-review pending until re-reviewed or waived |
| `integrity` | `<ISO date> (sha: <short-hash>)` | last integrity audit — the date for the reader, the body hash for the check; the dispatcher writes it once the audit's dispositions land, and a spec's consumption gate recomputes the hash to decide whether the stamp still holds |

A round ending in `concerns` or `blocking` records its findings in the
document body. Concerns later resolved without a fresh round keep the
verdict and gain a resolution date — `concerns (resolved 2026-07-16)` —
plus a body note saying what resolved them.

Finding unfinished work is one command per class, published as the
`## Unfinished-work list` section of the lifecycle rule — the exact
anchors live there, and the `process-status` skill runs them. The tail
anchors are exact, so a resolved-concern annotation drops out of the
match by design.

## Model selection

The architect is dispatched on the most capable available model; the
plan-adversary on a model scaled to the plan's size and risk — most
capable for complex or risky plans, one family below for small
mechanical ones. Consultations (the `*-consult` agents) dispatch on the most capable
available model; like the verdict agents, they run as named background
agents — consultations return no verdict, so the fallback machinery
below never applies to them. The model is always named explicitly at
dispatch, and reviews never dispatch on the cheapest available family.
A dispatch refused on the dispatched model's cap offers a one-family
drop (once) or waiting for the reset; a verdict produced below the
prescribed tier gets a fallback record and a re-review offer — grammar
and lifecycle in the spec-plan-lifecycle rule. Agents self-report the
model they ran on (family plus version) so the dispatcher can verify
before stamping.

An audit is not a review, and that floor governs reviews alone: the
`propagation-auditor` dispatches on the cheapest available family,
since every duty it walks is procedural, and the `integrity-auditor` on
the most capable available tier — each named like any other dispatch.
Both audits end in no verdict, so the fallback machinery leaves them
out as well, and both reports open with a model self-report the
dispatcher checks before relying on the run: a mismatched propagation
run earns no reliance, a below-tier integrity run no stamp.

The dispatcher's half of all this lives in the plugin's Rules payload —
the verdict agents' relay-then-stamp sequence and the two audit offers
in the workflow rule, the `integrity:` stamp and its
recompute-and-compare gate in the spec-plan-lifecycle rule. After a plugin update, run a rules
re-sync so the dispatcher side matches the agents; until then the
previously installed rules still carry the older record-the-verdict
obligation and make neither audit offer, so no round is lost and the
new gates merely stay silent.

## Process rules

The plugin ships five rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, ticket frontmatter, and the review-report
contract (`review-reports.md`: where a code-review run writes its
Review report and what shape it takes; domain review skills locate the
installed contract via its contract probe — the project-level then
user-level install path, in that order). Claude Code
does not load plugin rules by itself: install them with the
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

### Reducing permission prompts

sync-rules shells out to the plugin's scripts, the `claude` CLI, and
`cp`/`mkdir` into the rules target — each prompts for permission unless
allowed. Bash permission rules match the literal command text with `*`
wildcards allowed at any position (no `~` or variable expansion), which
permits a machine-independent form. Recommended entries — in
`~/.claude/settings.json` for yourself, or committed to a project's
`.claude/settings.json` for the whole team (they work unchanged on every
machine, and project-scoped plugin installs live under the same
per-user cache path):

```json
"permissions": {
  "allow": [
    "Bash(claude plugin list *)",
    "Bash(*/.claude/plugins/cache/missing-bits/*)",
    "Bash(*/.claude/plugins/cache/claude-plugins-official/superpowers/*)"
  ]
}
```

The second entry covers every script any plugin of this marketplace
ships; drop the `missing-bits/` segment to cover all marketplaces. The
third covers the scripts bundled with superpowers — the required
dependency, whose process skills (plan execution, review packaging)
shell out the same way. The drift hook itself runs as a plugin hook and
needs no allow entry.

## Process directories

This plugin creates two directories in a project repo: `docs/domain/`
(glossary + ADRs) and `docs/code-review/` (Review reports — one per
code-review run, shape defined by the review-reports rule). On first
creation the developer is asked whether the directory should be
git-ignored (a `.gitignore` containing exactly `*`) or committed; an
existing directory's state is respected without asking. A tracked-mode
`docs/code-review/` additionally carries a `.gitignore` with `local-*`
— the local pocket for reports the developer keeps out of git.

## Project memory

The in-repo Project memory store ships as its own plugin, `project-memory`
— a Rules payload this plugin's engine installs and updates like any
other. When its rules are installed alongside these, `docs/memory/` (Team
memory) counts as a Process directory and memory entries follow the
`ticket` conventions above.
