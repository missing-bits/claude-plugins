---
ticket: "#1"
date: 2026-07-20
status: draft
grilled: 2026-07-20
architect: LGTM
branch: worktree-project-memory-spec
base: master
---

# Project memory — an in-repo, two-part memory store for working-process

## Problem

Claude Code's home-dir memory lives in the user's home directory
(`~/.claude/…/memory/`). It is per-user and outside the project, which
creates two problems for teams using working-process:

1. **Team-relevant project knowledge is siloed in one person's private
   memory.** Parked ideas, cross-ticket initiative state, and recurring
   operational gotchas accumulate in a single developer's home-dir memory —
   unversioned, invisible to the team, never reaching the repo, though the
   whole team would benefit.
2. **Per-user project notes have no home inside the project.** Recording or
   recalling anything about a project means working in the home directory
   instead of the project itself.

working-process should provide a convention for an in-repo memory store that
both the team and the individual developer can use, without abandoning the
home-dir memory that already works for cross-project and personal
facts.

## Scope

Two working-process **rules** (a Rules payload) plus the supporting glossary
terms and frontmatter-exemption edits. It defines *where* project memory
lives, *how* it loads, *what shape* its entries take, and *when* entries
leave. It does not replace home-dir memory and does not build any tooling
beyond the rule and its conventions.

## Design

### Two parts by location

Privacy is expressed by location, not by a per-directory mode question:

- **Team memory** — `docs/memory/`, committed, visible to everyone. A
  Process directory: the first-create tracked/ignored question applies as
  for any other. It may start in ignored mode to defer the commit while
  content accrues on disk; the flip to tracked is a manual, unprompted
  developer action — a `*`-only `.gitignore` self-ignores, so flipping means
  deleting it or force-adding, which Claude never performs or suggests (the
  existing "never suggest removing an existing ignore" rule fits this).
- **Private memory** — `.claude/memory/`, per-user, always git-ignored
  (`.gitignore` containing exactly `*`), never asked. It is **not** a
  Process directory — the glossary's Process-directory term deliberately
  excludes `.claude/` config dirs, and that stays true. Private memory is a
  distinct concept: a per-user store under the config namespace, governed
  solely by this rule, outside the first-create machinery.

### Layout and INDEX

Each part mirrors home-dir memory: a thin `INDEX.md` holding one-line
pointers, plus flat topic files read on demand. No per-category
subdirectories.

`INDEX.md` is **sectioned** (per part): a **Notes** section
(recall-on-demand) and an **Ideas** section (a browsable backlog). The Ideas
section lists each entry in its lifecycle state: parked (a link to its `idea-`
file), spec'd (a redirect line to the spec, no file), or dropped (a
struck-through tombstone with the reason). The section is one of three
consistent expressions of a single criterion — entry
*shape* — alongside the filename prefix and the frontmatter set. The `idea-`
prefix is authoritative; the INDEX section and the frontmatter set follow from
it, and the prefix wins if they ever disagree. Sections can graduate to
subdirectories later if a part grows noisy; the design does not do so
pre-emptively.

### Loading and routing — two rules

Two rules ship, mirroring the plugin's existing split (`workflow.md`
always-on + `process-artifacts.md` paths-scoped):

- **An always-on core rule** (no `paths:`, like `workflow.md`) — what loads
  and routes in every session: where the two parts live, "read each part's
  `INDEX.md` at session start when it exists, and pull a topic file only when
  its index line is relevant", and the routing contract below. Deliberately
  thin, so its every-session footprint stays small.
- **A paths-scoped conventions rule** (`paths: ["docs/memory/**",
  ".claude/memory/**"]`, like `process-artifacts.md`) — the detail (entry
  shapes, team-part scope, the lifecycle), which activates only when the
  session touches a memory file. Reading `INDEX.md` per the core triggers it,
  so a session that uses the store gets the detail right after start, while a
  session that never touches memory pays only for the thin core.

A `paths:`-scoped rule does not fire at session start (it triggers when a
matching file is read), so the session-start load and the write-redirect —
both of which must work even while editing non-memory files — live in the
always-on core, not the paths-scoped rule. Loading is therefore rule-based,
no hook required; the core rule being always-on is a deliberate exception to
the `paths:`-required convention for domain payloads, justified for a
behaviour-shaping process rule (as `workflow.md` already is).

**Routing (best-effort, not enforced).** A rule is context, not enforced
configuration: it steers where facts go, it does not guarantee it. The core
rule states that project-scoped facts *should* go to the store rather than
home-dir memory, and states the coexistence contract, because the harness's
own memory protocol pushes project facts to home-dir memory:

- Cross-project or purely personal facts → home-dir memory (unchanged; still
  auto-loaded by the harness).
- Project-scoped facts *should* go to the store: team-relevant to Team
  memory, per-user to Private memory.
- On collision for a project-scoped fact, the project store wins.

The redirect is inherently best-effort because "is this fact project-scoped?"
is a semantic judgement only the model can make — a hook sees a path, not
intent (see Alternatives considered). The cost of a miss is low and
recoverable: the fact lands in home-dir memory instead of the store, and can
be moved later. This is the same best-effort character home-dir memory already
has (the model already decides what to save and where).

**Inert by default; adoption is opt-in.** In a project that has not adopted
Project memory the rule is a no-op: it acts only when a store already exists
("read `INDEX.md` *when present*"). The rule never creates a store or nags to;
it offers creation only when the developer signals intent to record something
project-scoped. On first adoption — when no `INDEX.md` exists yet, so the
session-start read cannot trigger the paths-scoped conventions rule — the
core rule's creation-offer points at the conventions rule for the INDEX
sections and entry shapes, so the store is templated with shape guidance from
the start. For Team memory (`docs/memory/`) that same creation-offer also
carries the tracked/ignored first-create question — the paths-scoped
process-artifacts rule that normally owns it does not activate at
`docs/memory/`, so the always-on core is the only rule reliably present when
the store is first created. Private memory (`.claude/memory/`) is always
ignored and never asked. This matters because the core rule is always-on and,
at user scope, loads in every project — most of which will not have adopted
the mechanism.

### Entry shapes — note vs idea

The criterion that splits entries is **shape**, not topic.

- **note** (default, no prefix) — gotchas and cross-ticket state. A
  cross-ticket registry, so `ticket`-exempt like the glossary. Access pattern:
  recall on demand. A note may carry an optional `adr-candidate: yes`
  frontmatter field — a single presence flag (not a multi-value enum): present
  means "flagged for later ADR review", absent means not a candidate (no `no`
  stamped on every note). Sweep with `rg 'adr-candidate:'`.
- **idea** (`idea-<slug>.md` filename prefix) — a parked idea. Carries a
  lifecycle frontmatter set: `status: parked → spec'd | dropped`, a `spec:`
  pointer once it graduates, and `ticket`. Access pattern: browse the
  backlog. The `idea-` prefix is the rule's **selector** for this frontmatter
  set; notes and ideas otherwise share one flat directory and one `INDEX.md`.

Only ideas get a prefix, because only ideas are a distinct shape (a
lifecycle-bearing entry); gotchas and state share the note shape. Ideas
inherit the two-part structure — private parked ideas are possible in
`.claude/memory/idea-*.md`.

This folds the previously-floated standalone ideas ledger
(`docs/ideas/` as its own Process directory) into Project memory: parked
ideas are `idea-` entries, not a separate directory.

### Team-part scope and boundaries

Team memory owns, narrowly: **parked ideas**, **cross-ticket initiative
state**, and **operational gotchas**. It explicitly does not own — the rule
enumerates the redirect:

- a decision with a rationale and a real trade-off → an ADR
  (`docs/domain/adr/`);
- a canonical term or `_Avoid_` ban → the glossary;
- the todo/steps of one task → that work's plan;
- a unit of work tracked in the issue tracker → the `ticket`;
- any per-user fact → Private memory or home-dir memory.

### Lifecycle — the "no empty files" invariant

**A body file exists only while it holds live content with no more
authoritative home. No content ⇒ no file; a stub or empty file is never
left behind.** Body files and `INDEX.md` lines are separate: retiring an
entry never leaves an empty body file. Three cases:

- **Promotion** — content moves to a document home (a spec, an ADR, the
  glossary): delete the body file, and change its `INDEX.md` line into a
  redirect pointer to the new home (e.g. `→ docs/specs/…`). Uniform across
  idea → spec'd, gotcha → ADR, term → glossary. Redirect lines are cheap and
  **sweepable** (like tombstones), so the index does not become a graveyard.
- **Dropped** — abandoned with no promotion; the repo records nothing else:
  no body file, at most a one-line `INDEX.md` tombstone with the reason
  (`~~idea: X~~ — dropped: reason`), sweepable, to prevent re-proposal.
- **Obsolete** — the fact is no longer true (e.g. a gotcha whose pitfall was
  fixed in code) and there is no document to point at: delete outright, body
  and index line, no redirect. This applies the standard "delete memory that
  turned out wrong" discipline.

Pointers and tombstones are `INDEX.md` lines, never separate files.

### gotcha ↔ ADR boundary

There is no mechanical discriminator — a gotcha legitimately carries a reason,
so "has a rationale" does not separate the two. The rule instead:

- defaults every entry to a note/gotcha;
- when an entry has decision-shape (the existing ADR test: hard to reverse
  AND surprising without context AND a real trade-off existed) **offers**
  promotion to an ADR — the developer decides;
- treats misfiling as cheap and reversible: a gotcha promotes to an ADR
  later and then links to it.

The `adr-candidate` field (above) persists the "flagged decision-shaped but
promotion deferred" state so a decision does not rot as a plain gotcha. This
fits working-process's "every step is an offer" idiom.

### Terminology (glossary)

Terms added to `docs/domain/glossary.md`:

- **Project memory** — the in-repo, rule-loaded, two-part memory store,
  distinct from home-dir memory. _Avoid_: "project MEMORY.md".
- **Team memory** — the committed part, `docs/memory/`; a Process directory.
- **Private memory** — the per-user part, `.claude/memory/`; not a Process
  directory, always ignored, governed by this rule.
- **Home-dir memory** — the built-in harness memory (`~/.claude/…/memory/`),
  the store this rule redirects from. _Avoid_: "native memory".
- **Idea entry** — a Project-memory entry with the idea shape (`idea-`
  prefix + lifecycle frontmatter), as opposed to a plain **note**. _Avoid_:
  "backlog item".

Plus a ban: "tier" and "layer" are not used for the memory parts — "tier" is
a reserved glossary term for model families; the canonical word for a
Project-memory half is *part*.

### Alternatives considered

- **Privacy by mode (single directory).** One `docs/memory/` whose
  first-create question chooses tracked (team) or ignored (private).
  Rejected: the developer wants both simultaneously and a location-based
  mental model (`.claude/` = private, `docs/` = team); the local-pocket
  pattern could express "both" in one directory but at the cost of that
  mental model.
- **Extending "Process directory" to `.claude/memory/`.** Rejected: it would
  blur the clean "`.claude/` = config, `docs/` = artifacts" split the
  glossary maintains; a distinct concept is cheaper.
- **`adr-` filename prefix (symmetric to `idea-`).** Rejected: ADRs live in
  `docs/domain/adr/`, not memory, so a prefix meaning "belongs elsewhere" is
  a smell and forks the ADR home. A frontmatter `adr-candidate` flag delivers
  the reviewability without moving the file's identity.
- **A `PreToolUse` hook to enforce the redirect.** The only documented way to
  make memory writes deterministic — rules are context, not enforced config,
  and the other documented lever (the `autoMemoryDirectory` setting) relocates
  the *whole* memory dir to a machine-specific absolute path and cannot express
  the two-part split. Rejected for the first cut: a hook sees a path and
  content, not intent, so it cannot make the project-scoped judgement the
  routing turns on — it could only add a coarse "you are writing to home-dir
  memory from a project that has a store" guardrail that false-alarms on
  legitimate cross-project writes. It stays the escalation path if best-effort
  routing proves insufficient; its inability to classify scope is exactly why
  the rule is the primary instrument.
- **A SessionStart hook injecting the indexes.** The plugin already ships a
  SessionStart hook, so a one-line "project memory present" pointer is cheap
  and would make discovery reliable. Left optional: the always-on core rule
  already loads every session, so no hook is needed for loading; the pointer
  is a future reliability aid, not required.

## Changes by file

- `plugins/working-process/rules/` — two new rules. An **always-on core**
  (`project-memory.md`, no `paths:`) carrying the two parts and their
  locations, the session-start load, and the best-effort routing/coexistence
  contract. A **paths-scoped conventions rule** (`project-memory-conventions.md`,
  `paths:` on the memory dirs) carrying the note/idea shapes and the `idea-`
  selector, the `adr-candidate` flag, the sectioned INDEX, the team-part scope
  with its redirect table, and the no-empty-files lifecycle.
- `.claude/rules/plugin-authoring.md` — a one-line note that behaviour-shaping
  process rules are the deliberate always-on exception to the `paths:`-required
  convention (which targets domain-standards payloads); `workflow.md` and the
  Project-memory core rule are the instances.
- `plugins/working-process/rules/process-artifacts.md` — add Project memory
  **notes and `INDEX.md`** to the `ticket`-exempt registry list (idea entries
  are topic files that DO carry `ticket`, so they are not exempt); add
  `docs/memory/` to the Process-directory enumeration (documentation only —
  NOT to the rule's `paths:`; the always-on core rule is the sole owner of the
  first-create question, and paths-scoping here would double-ask in the
  tracked-uncommitted window); note Private memory as the explicit
  non-Process-directory exception.
- `plugins/working-process/rules/ticket-frontmatter.md` — reflect the same
  `ticket` exemption (notes + `INDEX.md`) for the store's registry files.
- `plugins/working-process/README.md` — document the new convention.
- `plugins/working-process/.claude-plugin/plugin.json` — minor version bump
  (a new rule is a backward-compatible addition; pre-1.0 convention).
- `docs/domain/glossary.md` — the terms above (landed with this spec).

Delivery to installed copies rides the usual path: the rules-payload change
bumps the plugin version and sync-rules picks up the drift. The
work-marketplace mirror needs a manual sync after release.

## Out of scope

- Any tooling beyond the rule and its conventions (no capture/recall
  commands, no index generator).
- A migration tool. Moving existing home-dir project memories into the store
  is a one-time operational step after the rule ships, not part of this work.
- Changes to home-dir memory behavior — it is only redirected from,
  never disabled.

## Provenance

Brainstormed, taken through an architect-session consultation, and grilled
(as a raw idea, pre-spec) on 2026-07-20 before this spec was written. The
grilling settled: the ideas-ledger fold, Private memory as a non-Process
directory, the gotcha↔ADR offer model, the `adr-candidate` field, the
sectioned INDEX, and the no-empty-files lifecycle (including the promotion
redirect and the obsolete-vs-dropped split). Filed as issue #1.

## Architect findings (formal review round 1, 2026-07-20)

Verdict: `concerns` (fable 5, 2026-07-20) — dispatched at the prescribed tier
(most capable available), so no fallback field. Three Important, four Minor;
all localized, none touching the design's spine (two-part store, note/idea
shapes, no-empty-files lifecycle, gotcha↔ADR offer — all sound). An
independent official-docs check ran in parallel and corroborated I1–I3.

**Important**

1. **I1 — `type`-keyed routing binds to a taxonomy the native memory model
   does not expose.** The `type: user|feedback|project|reference` routing
   paragraph codes against an interface not present in native memory
   (free-form markdown: index + topic files). The field does exist in the
   current harness but is not a documented, stable interface — unsafe for a
   distributable rule. Disposition: delete the type-routing paragraph; the
   three plain-language routing bullets above it already express the same
   routing on a real discriminator.
2. **I2 — the redirect (the design's whole value over native memory) rests on
   a rule, which is best-effort context, not an enforced write-destination.**
   Docs: memory/CLAUDE.md are context, not enforced config; real overrides are
   a `PreToolUse` hook or the `autoMemoryDirectory` setting (whole-dir,
   machine-specific, not committable). The spec's hook hedge aims at loading
   (SessionStart), not write-redirect (PreToolUse). Disposition: state the
   redirect is best-effort (a miss = a fact lands in home-dir, not the repo —
   the coexistence contract already leans this way) AND add a `PreToolUse`-hook
   option to "Alternatives considered", arguing why rule-only suffices for the
   first cut.
3. **I3 — the planned `paths:` block conflicts with the rule's always-on
   jobs.** The rule must load `INDEX.md` at session start and redirect facts
   learned while editing arbitrary files; a `paths:`-scoped rule loads
   conditionally and would miss both. Disposition: ship the rule WITHOUT
   `paths:` (always-on — still a rule, not a hook), and note in
   plugin-authoring that always-on is the deliberate exception for
   behavior-shaping process rules (the `paths:`-required convention targets
   domain-standards payloads).

**Minor**

- **M1** — "defer then flip to tracked" has no agent support, and a `*`-only
  `.gitignore` self-ignores; state the flip is a manual, unprompted developer
  action (Claude never assists), or add a deferral-intent signal.
- **M2** — `adr-candidate: possible | yes` has no stated behavioral
  difference; collapse to a presence flag or define what each value changes.
- **M3** — the `ticket`-exemption wording says "topic files", but idea topic
  files DO carry `ticket`; scope the exemption to notes + `INDEX.md`.
- **M4** — three encodings of shape (INDEX section, `idea-` prefix,
  frontmatter) with no tie-break; name the prefix authoritative, the rest
  derived.

**Resolution (2026-07-20, no fresh round).** All seven findings applied on the
developer's decisions:
- **I1** — the `type`-routing paragraph deleted; routing keeps the three
  plain-language bullets on a real discriminator.
- **I2** — routing stated as best-effort ("should"), with the rationale that
  the project-scoped judgement is semantic (model-only); a `PreToolUse`-hook
  alternative added to "Alternatives considered" and rejected for the first
  cut (cannot classify scope).
- **I3** — loading/routing recut into an always-on core rule plus a
  paths-scoped conventions rule (option b); the always-on exception noted for
  plugin-authoring; a new "inert by default, adoption opt-in" property added.
- **M1** — the ignored→tracked flip stated as a manual, unprompted developer
  action.
- **M2** — `adr-candidate` collapsed to a single presence flag.
- **M3** — the `ticket` exemption scoped to notes and `INDEX.md` (idea entries
  carry `ticket`).
- **M4** — the `idea-` prefix named authoritative over INDEX section and
  frontmatter.

A fresh architect verification round is offered before plan-writing.

## Architect findings (verification round 2, 2026-07-20)

Verdict: `LGTM` (fable 5, 2026-07-20) — prescribed tier, no fallback. All seven
round-1 dispositions verified as genuinely applied (not cosmetic; the
resolution note is accurate); glossary conformance clean (no `_Avoid_` bans —
"part"/"layer" not "tier", "home-dir memory" not "native memory"); no
regressions. One Minor, applied:

1. **Minor — first-adoption shape seam.** In an already-adopted project there
   is no seam: the core reads each part's `INDEX.md` at session start, which
   matches the conventions rule's `docs/memory/**` glob and loads it before any
   non-memory file is edited. The residual gap is the *first-adoption* session
   only — no `INDEX.md` exists yet, so the conventions rule does not trigger,
   and the store is created under the core alone (which carries locations,
   load, and routing but not the sectioned-INDEX/entry-shape conventions); the
   one moment that templates all future entries could lack shape guidance.
   Disposition: applied — the core rule's creation-offer now points at the
   conventions rule for the INDEX sections and entry shapes (see "Loading and
   routing", inert-by-default).

Neutral note (not a defect): I3 was implemented richer than its literal "one
always-on rule" disposition — a two-rule split (always-on core + paths-scoped
conventions), disclosed as "option b". Vetted on its own merits and sound
(keeps the always-on footprint thin, reuses the `workflow.md` /
`process-artifacts.md` precedent).
