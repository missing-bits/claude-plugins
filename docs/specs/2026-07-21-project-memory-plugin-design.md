---
ticket: "#1"
date: 2026-07-21
status: implemented
grilled: 2026-07-21
architect: concerns (resolved 2026-07-21)
branch: feature/1-project-memory-plugin
base: master
---

# project-memory — extracting the memory rules into their own plugin

## Problem

Project memory shipped (working-process 0.8.0, spec
`2026-07-20-working-process-project-memory-design.md`) as two rule files
inside the working-process Rules payload: `project-memory.md` (always-on
core) and `project-memory-conventions.md` (paths-scoped). That placement
has three costs:

- **Context cost for everyone**: the always-on core loads in every
  session on every machine with a user-level working-process rules
  install — including users who never adopt the store.
- **Plugin scope**: working-process is the spec → plan → review flow;
  an in-repo memory store is a separate concern riding along.
- **Coupled adoption and versioning**: memory cannot be installed
  without the whole working-process payload, nor released on its own
  cadence.

Store-level adoption is already opt-in (the core rule is a no-op without
an `INDEX.md`); this spec makes the *install* opt-in too.

## Decision

Extract the two rules into a new payload plugin,
`plugins/project-memory/`. Independence is layered, and the two layers
must not be conflated: the rules' *content* does not require the
working-process rules to be installed (cross-references between the two
payloads become conditional in both directions, following the existing
payload convention — "mentions of skills and agents inside rule text
are conditional"), while *installation* requires the working-process
plugin like every Rules payload — distribution stays with the Rules
engine, and per the glossary, payload plugins never copy the mechanism.
This is deliberately NOT the glossary's "Standalone install", a term
scoped to standards plugins whose skills load without working-process;
a rules-only plugin has nothing that loads without the engine.

## New plugin shape

```
plugins/project-memory/
├── .claude-plugin/plugin.json   # 0.1.0
├── README.md
└── rules/
    ├── project-memory.md              # core, always-on (no paths:)
    └── project-memory-conventions.md  # paths: docs/memory/**, .claude/memory/**
```

- `plugin.json`: version `0.1.0`, no `dependencies` edge. A declared
  edge would truthfully encode the operational requirement, but it buys
  little and costs a chain: auto-installing working-process would
  transitively pull superpowers (working-process declares it), while
  still not delivering the rules — sync-rules is an interactive skill
  run, not an install side effect. The README carries the operational
  instruction instead, keeping the engine dependency operational-only.
- `README.md`: the store (two parts, thin `INDEX.md` + flat topic
  files), opt-in adoption, and install via `working-process:sync-rules`.
- Marketplace catalog (`.claude-plugin/marketplace.json`) gains a
  `project-memory` entry, and the repo root `README.md` plugin table
  gains its row — manifest, catalog entry, and README row land
  together, per the marketplace-sync rule. The name was never
  previously used as a public plugin name, so the `renames` map is not
  involved.
- The core rule stays always-on: loading `INDEX.md` at session start
  has no path to scope on. This keeps it a justified exception under
  the plugin-authoring rule's Rules-payload section; that rule's
  wording is updated to attribute the standing instance to the
  project-memory plugin instead of working-process.

## Rule text changes — content independence

Substance unchanged; only assumptions of working-process's presence are
reworded.

`project-memory.md` (core):

- The Adoption section carries the Team-memory tracked/ignored
  first-create question **self-contained**: both modes (ignored — a
  `.gitignore` containing exactly `*`; tracked — files committed) and
  the never-ask-when-a-signal-exists guard, without deferring to the
  process-artifacts rule for semantics. One conditional sentence
  remains: when the working-process rules are installed, `docs/memory/`
  counts as a Process directory there.
- Loading and Routing sections reference nothing working-process owns —
  unchanged.

`project-memory-conventions.md`:

- "a Process directory; the first-create question applies" becomes
  self-contained (the core rule asks); the Process-directory mention
  becomes conditional.
- Routing targets become conditional on the project actually keeping
  them: ADRs (`docs/domain/adr/`), the glossary, and the `ticket`
  frontmatter convention are referenced as "when the project keeps …
  (e.g. via working-process)". Without them, every entry simply stays a
  note. The `adr-candidate` flag stays — harmless without ADRs, it
  still marks decision-shaped notes for later review.
- Entry shapes, team-memory scope, gotcha↔ADR offer, and the
  no-empty-files lifecycle are unchanged.

Degradation without working-process: no Process-directory ceremony
beyond the core rule's own tracked/ignored question, no ADR/glossary
promotion offers, and `ticket` on idea entries only when the project
has such a convention.

## working-process side changes

- `rules/project-memory.md` and `rules/project-memory-conventions.md`
  are removed from the payload.
- `rules/process-artifacts.md`: `docs/memory/` stays listed as a
  Process directory with conditional wording ("when the project-memory
  rules are installed"); the paragraph attributing the tracked/ignored
  question to the memory core rule stays (still true — the rule now
  lives in the project-memory plugin, referenced conditionally); the
  `ticket` exemptions for memory files gain the same conditional
  prefix.
- `rules/ticket-frontmatter.md`: the Project memory field-set bullet
  gains the conditional prefix and points at the conventions rule in
  the project-memory plugin.
- `README.md`: "ships seven rule files" becomes five; the "Project
  memory" section shrinks to a pointer at the new plugin; the
  Process-directories section drops `docs/memory/` as a directory this
  plugin creates (moves to the project-memory README).
- `plugin.json`: version `0.8.0 → 0.9.0` (component removal is
  breaking; pre-1.0.0 breaking changes ride a minor bump). The
  description stays unchanged — it never named the memory pair.

## Migration

No migration story: the store shipped the day before this spec and the
only existing installs are the author's own machines. The generic
sync-rules flows already cover the transition unaided — updating a
working-process payload to 0.9.0 flags the two files as removed
upstream (ask remove / keep-as-own), and installing the project-memory
payload places them under `<target>/project-memory/`.

Deprecation ceremony: none. The plugin-versioning rule ties
deprecate-before-removing to "the major that removes it" — post-1.0.0
language; pre-1.0.0 the breaking change rides the minor bump, and the
interactive removed-upstream ask in sync-rules protects installs better
than a README deprecation notice would.

## Glossary supersessions

This design supersedes two glossary entries; the updates route through
a grilling-session after this spec, per process:

- **Project memory** (`docs/domain/glossary.md`): "the in-repo,
  rule-loaded memory store *working-process defines*" — now defined by
  the project-memory plugin.
- **Team memory**: "a Process directory (the first-create question
  applies)" — Process-directory status becomes conditional on the
  working-process rules being installed; the first-create question is
  carried by the memory core rule itself.

## Conscious duplication — first-create question semantics

The core rule restating the tracked/ignored semantics duplicates them
across two plugins (process-artifacts keeps the general definition).
Accepted deliberately: the semantics are small and stable, and the
alternative — a hard dependency on the working-process rules —
contradicts the content-independence decision. The parked idea
`idea-first-create-question-owner.md` (Private memory) already tracks
the general single-owner fix; implementation adds one line there noting
the copy now lives in the project-memory plugin.

## Alternatives considered

- **Keep the rules in working-process, slim the core**: reduces context
  cost only; adoption and scope stay coupled. Rejected.
- **Extension plugin (declared `dependencies` edge on
  working-process)**: orthogonal to content coupling and weighed on its
  own — the edge auto-installs the engine (and, transitively,
  superpowers) yet still leaves the rules unsynced, buying an install
  nudge at the cost of a dependency chain. Rejected; the README carries
  the instruction instead.
- **Minimal transplant (files moved as-is)**: leaves dead references to
  Process directories and `ticket` for installs without the
  working-process rules. Rejected in favour of conditional rewording.
- **Move + documented integration contract in both READMEs**:
  documenting a contract for consumers that do not exist yet;
  over-engineering today. Rejected.
- **Duplicating the sync engine for full operational independence**:
  contradicts the glossary's Rules-engine entry ("payload plugins never
  copy the mechanism"). Rejected.

## Validation

- `claude plugin validate .`, `claude plugin validate
  plugins/project-memory`, and `claude plugin validate
  plugins/working-process` all pass.
- Rule frontmatter reviewed by hand (`claude plugin validate` does not
  check `rules/`); the conventions rule keeps its `paths:` block, the
  core rule ships none.
- README counts and cross-references grepped for stale mentions of the
  moved files.

## Review rounds

- **Architect**, 2026-07-21, Fable 5 (prescribed tier): **concerns**.
  Findings and disposition: (1) Important — the no-`dependencies`
  choice leaned on the python-standards precedent, whose justification
  does not transfer (its skills load without working-process; a
  rules-only plugin has nothing that loads), and the extension-plugin
  alternative was rejected on grounds that applied to the chosen
  variant too. Resolved by re-arguing the decision on its real
  trade-off (transitive superpowers auto-install vs. an install nudge
  that still leaves rules unsynced); decision unchanged. (2) Minor —
  the repo README plugin-table row was missing from the new-plugin
  inventory; added per the marketplace-sync rule. (3) Minor — the
  working-process description change was a no-op (the description never
  named the pair); corrected to "unchanged".

## Out of scope

- Data in adopting projects (`docs/memory/`, `.claude/memory/`) — the
  store format is unchanged; nothing moves.
- Syncing any concrete machine's installed rules — a post-release
  sync-rules run, not part of this change.
- Memory-related skills (review/promotion tooling) — future work, not
  scaffolded now.
- The general first-create-question owner fix — stays a parked idea
  with its own future spec.
