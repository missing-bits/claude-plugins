# claude-plugins — domain glossary

Missing Bits marketplace of Claude Code plugins; its domain is the working
process the plugins support and the marketplace machinery that ships them.

## Language

**Process directory**:
A directory the working process creates in a project repo to hold work
artifacts (e.g. `docs/domain/`, `docs/specs/`, `docs/plans/`). Deliberately
narrow: configuration directories the process may also create (such as
`.claude/rules/` during a project-level rules install) are not Process
directories — their install questions are their own, defined where the
install is specified.
_Avoid_: artifact folder

**First-create question**:
The question — ignored mode or tracked mode — asked when a process
directory is created for the first time, or exists with no observable
prior decision (neither a `.gitignore` containing exactly `*` nor a
git-tracked file). Never asked when either signal is present.
_Avoid_: self-ignore

**Ignored mode**:
A process directory with a `.gitignore` containing exactly `*`; its
contents stay out of the repo's git status. A `.gitignore` with any
other content (e.g. a local pocket's `local-*`) does not signal ignored
mode.

**Tracked mode**:
A process directory whose files are committed; detected by any git-tracked
file under it.

**Contract probe**:
The ordered path check a domain review skill runs to find the installed
report contract: `<project>/.claude/rules/working-process/review-reports.md`,
then `$HOME/.claude/rules/working-process/review-reports.md` — first hit
wins, mirroring the Rules engine's project-over-user conflict rule. Part
of the review-reports contract: the paths may not drift independently.
_Avoid_: discovery, probe (unqualified)

**Review report**:
The single persistent document one code-review run writes under
`docs/code-review/` of the reviewed project — one run, one report,
written by the run's owner. Shape defined by the review-reports rule's
contract; a domain plugin's inline fallback is a strict subset of it,
never a different shape.
_Avoid_: review output, report file

**Standards plugin**:
A domain plugin of this marketplace encoding coding standards for one
technology: area skills, a review stack that writes Review reports,
optionally a `*-plan-review` checklist and a Rules payload. A report's
`standards:` field names the standards plugin(s) the run reviewed
against.
_Avoid_: standards stack, domain-standards plugin

**Standalone install**:
A standards plugin installed without working-process — every skill
still works; review reports follow the plugin's inline fallback (a
strict subset of the shared contract) and the contract probe finds
nothing. `solo` is NOT this: it is the run-owner mode of a review run.
_Avoid_: solo install, solo profile

**Rules engine**:
The rules-distribution mechanism living in the working-process plugin: the
`sync-rules` skill, the drift hook, and their shared scripts. One engine
serves every Rules payload of the marketplace — payload plugins never copy
the mechanism.

**Rules payload**:
The `rules/` directory a plugin of this marketplace ships for distribution
by the Rules engine; installed into its own namespace,
`rules/<plugin-name>/`, next to a manifest. A plugin shipping one is a
payload plugin.
_Avoid_: rules plugin

**Drift**:
A mismatch between a Rules payload's current upstream content and the
state recorded at the last completed sync (the manifest's `rulesetHash`).
Detected by the drift hook, resolved by the `sync-rules` skill. Always a
content-hash comparison, never a plugin-version comparison.
_Avoid_: outdated rules

**Orphan**:
An installed rule set whose source plugin is no longer installed (or,
for a user-scope source, is disabled — a project-scoped source elsewhere
reports a contextual `enabled: false` and still counts as present);
detected during `sync-rules` state discovery, offered for removal or
adoption as the developer's own.

**Tier**:
A relative rung on the platform's current capability ladder of model
families ("most capable available", "mid"), resolved at dispatch time —
never a concrete model name. The prescribed tier is the tier the
model-selection heuristic assigns to a given dispatch.
_Avoid_: model level

**Degraded verdict**:
A review verdict produced below the prescribed tier by anything other
than the developer's deliberate choice — a cap refusal (including a
consented one-tier drop after it), a silent platform substitution, or
an under-dispatch the dispatcher did not knowingly decide. Marked by
the `(degraded <date>)` token in the `*-fallback` frontmatter field and
entitled to a re-review offer.
_Avoid_: capped verdict, lowered verdict

**Chosen verdict**:
A review verdict produced below the prescribed tier because the
developer deliberately dispatched below it, before any platform
refusal. Marked by the `(chosen <date>)` token in the `*-fallback`
field; carries the same re-review offer as a degraded verdict.
_Avoid_: voluntary degradation

**Fallback**:
The model that actually produced a degraded or chosen verdict, standing
in for the prescribed tier; named (as a family alias) in the value of
the `*-fallback` frontmatter field. A dispatch at the prescribed tier —
e.g. mid tier for a small mechanical plan per the heuristic — is not a
fallback.
_Avoid_: backup model, replacement model

**Fallback record**:
The `*-fallback` frontmatter field (`architect-fallback:` /
`adversary-fallback:`): the record that a verdict was produced below
the prescribed tier — the fallback's family alias plus an agency token,
`degraded` (unchosen: forced or unnoticed) or `chosen` (deliberate). A
bare record means the re-review offer is live; a fresh prescribed-tier
round removes it (a degraded one refreshes it), a waiver annotates it.
_Avoid_: sub-tier record

**Consumption gate**:
The workflow step at which a document's review verdict is about to be
relied on as the basis of further work — plan-writing for a spec,
implementation for a plan. Where re-review offers on fallback-recorded
verdicts fire.
_Avoid_: usage point

**Project memory**:
The in-repo, rule-loaded memory store the project-memory plugin defines, in
two parts — Team memory and Private memory — mirroring Home-dir memory's
thin-index-plus-on-demand-topic-files model, but living in the project.
Distinct from Home-dir memory, which it redirects project-scoped facts away
from. Each half is a *part* (Team memory, Private memory).
_Avoid_: project MEMORY.md, memory tier, memory layer

**Team memory**:
The committed part of Project memory, `docs/memory/`; the first-create
question applies — asked by the project-memory core rule — and it counts as a
Process directory when the working-process rules are installed. Holds
team-relevant parked ideas, cross-ticket state, and operational gotchas.

**Private memory**:
The per-user part of Project memory, `.claude/memory/`; always ignored, never
asked, and NOT a Process directory — a per-user store under the `.claude/`
config namespace, governed by the Project-memory rule.
_Avoid_: local memory

**Home-dir memory**:
The built-in Claude Code memory at `~/.claude/…/memory/`, auto-loaded by the
harness. The store the Project-memory rule redirects project-scoped writes
away from; it keeps cross-project and personal facts.
_Avoid_: native memory

**Idea entry**:
A Project-memory entry with the idea shape: an `idea-` filename prefix and
lifecycle frontmatter (`status` parked → spec'd | dropped, a `spec:` pointer,
`ticket`), as opposed to a plain note (the default shape, `ticket`-exempt,
recalled on demand). The prefix is the rule's selector for the lifecycle
frontmatter set.
_Avoid_: backlog item
