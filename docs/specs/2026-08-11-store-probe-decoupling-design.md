---
ticket: none
date: 2026-08-11
status: implemented
grilled: 2026-08-11
branch: feature/store-probe-decoupling
base: develop
---

# Store probes — decoupling foreign plugins from the index filename

## Problem

Three plugins that are not project-memory hard-code the name of
project-memory's index file. Five surfaces carry the coupling:

- `plugins/working-process/rules/review-reports.md:198` — the Candidate-gap
  park offer checks `docs/memory/INDEX.md` and `.claude/memory/INDEX.md` to
  decide whether the reviewed project keeps a store. This is the **owning**
  statement of the check;
- `plugins/python-standards/skills/python-code-review/SKILL.md:77` and
  `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md:110` —
  deliberate standalone restatements of the same check, so the skills work
  without the working-process rules installed;
- `plugins/working-process/rules/process-artifacts.md:67` and
  `plugins/working-process/rules/ticket-frontmatter.md:23` — enumerate
  `INDEX.md` among the `ticket`-exempt registry files.

The coupling means any change to the store's layout is a change to four
plugins. Concretely: the deferred rename of the index to `MEMORY.md` — one
half of the parked Auto-memory hybrid decision — is today a breaking release
across all four, with a compatibility window whose worst state (a renamed
store under an old check) reads as "no store" and silently swallows the park
offer. After this change it is a single-plugin release.

The change also pays on its own: three plugins stop encoding another
plugin's internal layout — a defect whether or not the rename ever happens.

## Terminology

The check is a **store probe** — never a bare "probe", which the glossary
bans (`_Avoid_: probe (unqualified)` under **Contract probe**, a different
check that finds the installed report contract). The grilling session
(2026-08-11) added **Store probe** to the glossary.

## Decisions

### Store probes test the directory, not the index file

The three probe surfaces check that the directories `docs/memory/` and
`.claude/memory/` exist, not the index files inside them. The directory is
a stable adoption signal: it comes into being exactly at adoption — the
opt-in first-create flow materializes it, and Private memory's directory
always carries a `*`-only `.gitignore` — and no layout change inside the
store can move it. The check stays as mechanical as before: one
existence test per part, no file opened, equally dependable when a
code-review skill runs as a subagent.

The store-selection logic downstream of the probe is untouched: explicit
guidance wins; both parts present means ask; never offer to create a store.

### Registry-file enumerations delegate to the owning rule

The two working-process enumerations stop naming `INDEX.md` and instead
say what the exemption is for and who owns the list: the store's registry
files, per the project-memory conventions rule. The same principle let
`ARCHIVE.md` land in project-memory 0.2.0 without touching working-process;
extended to the index file, it keeps working-process out of every future
registry change. Idea entries keep carrying `ticket`; that
statement names a shape, not a file, and stays.

### The restatements change in the same release

The two standalone restatements in the standards skills are deliberate
copies of the review-reports contract and may not drift from it. All three
probe surfaces and both enumerations change in one release; the
marketplace-sync discipline (one bump per changed plugin, minted in the
release PR) carries the rest.

## What this does not change

- **project-memory itself.** No file of that plugin changes; the index
  filename stays `INDEX.md`. The rename remains deferred, coupled to the
  hybrid decision. After this change the filename survives outside
  project-memory only in repo artifacts — three glossary entries
  (**Archive**, **Live entry**, **Close (an entry)**) and the historical
  specs and plans — so the rename's scope is one plugin plus those
  documentation lines (architect consultation, 2026-08-11).
- **Probe semantics for adopted stores.** For any store the plugin created,
  directory-exists and index-exists are the same signal today, so no
  behavior changes for existing users. The one divergence is a directory
  created by hand without an index: the old check said "no store", the new
  one says "store". That reading is more honest — the directory is the
  adoption signal the first-create flow materializes — and the offer it
  gates is an offer, not a write.
- **The `ticket`-exemption semantics.** The same files are exempt; only
  the list moves.

## Alternatives considered

**Relying on session context** — the core project-memory rule already loads
the store's index at session start, so a reviewer could simply notice
whether a store is in context. Rejected: the code-review skills can run as
subagents, and whether user-level rules load into a subagent context — and
survive compaction — is unverified. A file-level check is predictable in
both environments.

**Deferring until the rename forces it** — rejected: bundling a
non-breaking cleanup into a breaking release maximizes the blast radius of
both. Sequenced first, the cleanup ships quietly and the rename shrinks to
one plugin.

## Component changes

**`working-process`** — `review-reports.md` (the owning probe statement),
`process-artifacts.md` and `ticket-frontmatter.md` (the two delegating
enumerations).

**`python-standards`** — one line in `python-code-review/SKILL.md`.

**`salesforce-standards`** — one line in `salesforce-code-review/SKILL.md`.

Three plugins bumped in the next release; the change is behavior-compatible
for every store the plugin ever created, so each sizes as a patch unless it
rides a release with larger changes.

## Versioning

No version bump on this branch. Both standards plugins are disabled on this
machine and working-process's change is not worth dogfooding alone, so no
`-dev.` suffix is minted; the release PR sizes the bumps.

## Glossary

The grilling session (2026-08-11) added **Store probe**: the existence
check a plugin other than project-memory runs on a Project-memory part's
directory, distinct from the Contract probe. The definition describes the
post-spec state — the directory, never a file inside it — and this branch
carries the implementation that makes it true.
