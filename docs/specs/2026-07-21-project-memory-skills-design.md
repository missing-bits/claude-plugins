---
ticket: "#1"
date: 2026-07-21
status: implemented
grilled: 2026-07-21
architect: LGTM
branch: feature/1-project-memory-plugin
base: master
---

# project-memory 0.2.0 — grooming skills and an on-demand archive

## Problem

The project-memory plugin (0.1.0) ships rules only: it defines the store's
entry shapes and lifecycle but nothing *executes* the lifecycle. Two gaps
follow:

- **No grooming.** The rules define entry states (live, promoted, dropped,
  obsolete) but no component walks the store to apply the transitions.
  Entries that are done or subsumed by a spec/plan linger in the store's
  directory and in its `INDEX.md`, which every session reads at start.
- **No routing repair.** The core rule's routing is best-effort — "on a
  miss a fact lands in home-dir memory and can be moved later". Nothing is
  the *later*: moving project-scoped facts out of home-dir memory into the
  project store is a manual chore (done by hand for this repo on
  2026-07-20).

A third issue surfaced while designing the fix: the lifecycle keeps closed
entries (promotion redirects, drop tombstones) in `INDEX.md` forever, so
the always-read index accretes history with every closed piece of work.

## Decision

Ship project-memory 0.2.0 with two skills and one store-format change:

- **`memory-review-session`** — an explicit-ask grooming conversation that
  audits the store and walks entries toward their correct lifecycle state.
- **`migrate-memory`** — an operational skill that moves project-scoped
  facts from home-dir memory into the project store (one direction).
- **Store format** — `INDEX.md` holds only *live* entries; closed entries
  move to a per-part, read-on-demand `ARCHIVE.md` (one line each).

The unifying principle, and the developer's stated lens, is **tidiness
without bloat**: the file read at session start (`INDEX.md`) never pays for
history, and a body file survives closure only when no other artifact
already carries its content.

## Store format

### Layout (each part)

```
docs/memory/              (and, identically, .claude/memory/)
├── INDEX.md              # LIVE entries only — the sole file read at session start
├── ARCHIVE.md            # Done / Dropped sections — one line each, read on demand
└── <topic>.md, idea-*.md # live entry bodies
```

### INDEX invariant

`INDEX.md` holds **only live entries**: the Notes section lists active
notes, the Ideas section lists only `parked` ideas. A line moves to
`ARCHIVE.md` **at the moment the entry closes** — never waiting for a
sweep. Strikethrough tombstones disappear from `INDEX.md` entirely (they
belong to the archive). This is the tidiness lens as a hard invariant: the
start-of-session read cost is bounded by live work, not by project age.

### ARCHIVE.md

Read on demand only — typically to answer "did we already consider this?"
and during the review session's audit. Never read at session start (the
core rule's Loading section is unchanged). Two sections:

- **Done** — closed-because-resolved lines: a promoted idea's redirect to
  its spec/ADR/glossary home, or a finished note's one-line "what + where"
  (the spec/plan, the release version, optionally the commit). Each line
  carries a closure date. No body.
- **Dropped** — abandoned-entry tombstones: reason + date, one line. Body
  handling below.

### Closure routing (rewritten lifecycle)

The single test governs every closure — *a body file survives closure only
when no other artifact carries its content*:

- **Promotion** (idea's content moves to a spec, ADR, or the glossary):
  delete the body; write a Done redirect line. The target IS the archive of
  that content.
- **Closed note** (a work-state note after its release, an expired gotcha
  whose resolution now lives in code/docs): delete the body; write a Done
  line naming where the detail now lives. If some fragment has no home in
  any document, the entry is not yet closed — or that fragment becomes the
  Done line.
- **Dropped** (abandoned): write a Dropped tombstone line (reason + date);
  delete the body. There is no body-retention directory: if the rejection
  analysis is worth keeping, that is the signal the entry is
  decision-shaped — offer to promote it to an ADR ("rejected X because Y",
  when the project records ADRs), or keep it a live note; a kept body is
  then not dropped. A one-line reason is what the archive preserves.
- **Obsolete** (no longer true, nothing worth pointing at): delete body and
  index line, no trace — unchanged from 0.1.0.

`paths:` on the conventions rule (`docs/memory/**`, `.claude/memory/**`)
already covers `ARCHIVE.md`; no frontmatter change needed.

`ARCHIVE.md` is a `ticket`-exempt registry file, exactly like `INDEX.md`;
the conventions rule states this explicitly. The "working-process
untouched" scope holds by **delegation**, not by category: working-process's
`ticket-frontmatter` memory bullet ends "See the project-memory-conventions
rule", handing authority to the paths-scoped (`docs/memory/**`) conventions
rule that this edit updates to name `ARCHIVE.md`. Any file touching
`docs/memory/ARCHIVE.md` loads that rule, so the exemption is delivered
without a working-process edit. (working-process's own enumeration still
names only `INDEX.md`; adding `ARCHIVE.md` there is a one-line clarification
that would touch working-process, so it is left to a future working-process
update, not required here.)

## Skill: memory-review-session

A grooming conversation, the store's analogue of grilling-session.

- **Trigger — explicit ask only.** Fires only on a direct request ("groom
  the store", "przejrzyjmy memory", "memory review"). The `description:`
  carries a hard "Use ONLY when the developer explicitly asks…" plus
  anti-triggers: routine memory reads/writes and questions about an entry's
  content do NOT start a session. This mirrors the core rule's "never
  scans, creates, or nags" stance.
- **Opening audit** (mechanical, from `INDEX.md` + a directory listing):
  dangling `INDEX` links, body files with no index line, empty stubs
  (violating no-empty-files), `idea-*` files whose `status` is `spec'd`/
  `dropped` but still sit as live bodies, and a **sweep**: closed lines
  still in `INDEX.md` (legacy or transitional state) move to `ARCHIVE.md`.
  The audit produces the worklist.
- **Entry walk — ordered, existential first** (one entry at a time, a
  recommendation with each):
  1. *Should this entry exist at all?* Untrue → obsolete (no trace).
     Realized or subsumed by a spec, plan, glossary, or ADR → close with a
     Done line. This is the path a work-state note takes to leave the
     directory.
  2. *Is it in the right part?* team ↔ private rebalance.
  3. *Is it the right size and shape?* split an overgrown note, trim it,
     merge duplicates; a note that has grown into a mini-spec is a
     candidate for a real spec, not a longer note.
  4. *Does the INDEX line summarize it well?* one-liner quality — recall
     depends on it; the cheapest tidiness there is.
- **`adr-candidate` review:** when grilling-session is available, offer a
  handoff to it for promotion (grilling writes the ADR, not this session);
  without working-process the flag simply stays and the session notes it
  and moves on.
- **Ideas section:** long-parked → confirm or drop; spec'd → close the
  redirect.
- **Boundaries:** applies the conventions rule's lifecycle, defines nothing
  new; never commits; edits applied inline as decisions land (like
  glossary edits in grilling); recommends, never bulk-cleans — every
  deletion or closure is per-entry consent. Every grilling-session, ADR,
  and glossary mention is conditional ("when … available").

## Skill: migrate-memory

An operational skill (named for what it does; may prompt for decisions
without being a session, like sync-rules).

- **Trigger — explicit ask** ("migrate my notes to the project", "przenieś
  notatki do projektu").
- **Scan** home-dir memory (`MEMORY.md` + entry files). Candidates are
  project-scoped facts about the *current* repo, judged by content;
  uncertain cases are asked, never guessed. Cross-project and personal
  facts stay in home-dir memory — the skill does not even propose them.
- **No store yet → offer adoption:** creating a part per the core rule,
  carrying the tracked/ignored first-create question for Team memory
  (Private is never asked). This is the natural adoption entry point —
  running migrate-memory *is* the signal of intent the core rule requires.
  Declining adoption ends the skill with no writes.
- **Per fact, with a recommendation:** move or leave; if move, route team
  vs private per the core rule (team-relevant → Team, per-user → Private).
- **Move mechanics:** translate shape — a home-dir entry (`name`/
  `description`/`metadata` frontmatter) becomes a note or an `idea-*` per
  the conventions rule (shape is the criterion, the `idea-` prefix
  authoritative); add the `INDEX` line in the target part; delete the
  home-dir file and its `MEMORY.md` line.
- **Migration trace:** a single roll-up line in home-dir `MEMORY.md`
  ("project-scoped notes for <repo> migrated to its Project memory,
  <date>") — the precedent from this repo's 2026-07-20 migration; no
  per-entry pointers.
- **Collision** (a fact already has a project-store counterpart): the
  project store wins — offer to merge into the project entry and remove the
  home-dir copy.
- **Boundaries:** one direction only (team ↔ private rebalance is
  review-session's job); never commits; works fully without
  working-process — `ticket` on idea entries only when the project keeps
  that convention.

## Packaging

- New components under `plugins/project-memory/skills/`:
  `memory-review-session/SKILL.md`, `migrate-memory/SKILL.md`.
- Rule edits: `project-memory-conventions.md` — Locations gains
  `ARCHIVE.md` (declared a `ticket`-exempt registry file like `INDEX.md`);
  the Ideas-section description and the entire Lifecycle section are
  **replaced, not appended**, so no surviving sentence says spec'd/dropped
  ideas stay in `INDEX.md` as struck-through tombstones — they carry the
  INDEX-is-live-only invariant and the rewritten closure routing instead.
  And `project-memory.md` (the parts description names `ARCHIVE.md` as
  read-on-demand; Loading unchanged).
- `plugin.json`: `0.1.0 → 0.2.0` — a minor bump via the 0.x rule (pre-1.0.0
  breaking changes ride a minor): the store-format rewrite is breaking for
  existing stores, whose `INDEX.md` redirect/tombstone lines become invariant
  violations until the review-session sweep repairs them. The new skills are
  additive; the format change is what sets the bump's character. The
  description gains the skills, which per the marketplace-sync rule drags the
  catalog entry and the repo README row in the SAME commit.
- `README.md` (plugin): a Skills section and the archive-format note.

## Authoring, validation, testing

- Skills authored with `skill-creator` (scaffolding, `description:` tuning,
  evals) over `superpowers:writing-skills` (content discipline), per the
  plugin-authoring rule.
- `description:` fields carry hard triggers and anti-triggers; both contain
  `: `, so both must be quoted (frontmatter-safety). The Polish example
  trigger phrases ride the repo-hygiene rule's named exception for quoted
  trigger phrases in skill descriptions (codified this cycle; precedent:
  grilling-session's "przemagluj") — the surrounding prose stays English.
- Evals — at least two per skill: a positive (explicit request → fires) and
  a negative (routine memory op or content question → does NOT fire).
  migrate-memory adds a negative: a cross-project fact stays in home-dir.
- Validation: `claude plugin validate .` and `plugins/project-memory` pass;
  both SKILL.md and edited rule frontmatter reviewed by hand (validate does
  not cover `rules/`); a grep confirms every grilling-session / ADR /
  glossary / ticket mention in the new skills is conditional.
- Natural smoke tests, against the store's CURRENT state (this repo's
  Private memory was already hand-converted to the new format on
  2026-07-21, consuming the original sweep fixture): a
  `memory-review-session` run whose audit comes back clean with a no-op
  sweep — itself a useful negative — while the remaining live note
  (`python-standards` follow-ups) exercises the closed-note walk once its
  tails resolve; exercising the sweep branch needs a synthetic legacy line
  planted in `INDEX.md` for the test. `migrate-memory` on this host, where
  home-dir memory holds only cross-project facts — the correct result is
  "nothing to move", a second negative.

## Review rounds

- **Architect**, 2026-07-21, **Opus 4.8** — a consented one-family drop
  below the prescribed tier (Fable 5 refused on a monthly spend-limit cap),
  recorded as `architect-fallback: opus (degraded 2026-07-21)`; a re-review
  at the prescribed tier is offered at the plan-writing gate. Verdict
  **concerns**: one Important, two Minor, all resolved inline.
  1. Important — `dropped/` was a write-only graveyard: a retained body was
     reachable only by a raw directory listing (never from `ARCHIVE.md`,
     never at session start), it collided with the opening audit's "body
     with no index line" check, and it contradicted the design's own
     governing test. Resolved by removing `dropped/` entirely — a drop
     leaves a one-line Dropped record; analysis worth keeping is the signal
     to promote to an ADR or keep a live note, both read artifacts.
  2. Minor — the "working-process untouched" scope was argued by category;
     re-argued on **delegation** (the `ticket-frontmatter` memory bullet
     hands authority to the paths-scoped conventions rule this edit
     updates), which holds without a working-process edit.
  3. Minor — made explicit that the conventions rewrite **replaces** the
     Ideas-section description and the Lifecycle section rather than
     appending, so no contradictory INDEX/tombstone wording survives.

- **Architect re-review**, 2026-07-22, **Fable 5** (prescribed tier — the
  pending fallback re-review): **LGTM**, four Minors, all applied inline.
  (1) The 0.2.0 bump is now justified via the 0.x breaking-rides-minor rule
  (the format rewrite is breaking for existing stores), not as
  "backward-compatible"; the plan's Global Constraints line was fixed the
  same way. (2) The deferred one-line working-process clarification (adding
  `ARCHIVE.md` to the registry-file enumerations in BOTH ticket-frontmatter
  and process-artifacts) is now parked on the existing closeout-offer idea.
  (3) The Polish trigger phrases in skill descriptions ride a named
  repo-hygiene exception for quoted trigger phrases, codified this cycle
  (precedent: grilling-session's "przemagluj"). (4) The smoke test was
  restated against the store's current state — the original sweep fixture
  was consumed by the 2026-07-21 hand-conversion; a clean-audit/no-op-sweep
  run is the negative, and the sweep branch needs a synthetic legacy line.

## Out of scope

- **working-process is untouched** — no changes, no version bump. The
  memory-review offer at a spec/plan's `implemented` transition belongs in
  working-process's `spec-plan-lifecycle` rule (rules make offers; the
  session stays explicit-ask-only), and is deferred to the next
  working-process update — parked as `idea-memory-review-closeout-offer.md`,
  sibling to the parked post-implementation code-review offer; both should
  land in one future working-process spec touching that rule section once.
- **team ↔ private rebalance** as a standalone tool — it lives inside
  review-session's entry walk, not a separate skill.
- **Bidirectional or full-router migration** — migrate-memory is one
  direction (home-dir → project) by deliberate scope.

## Glossary

The grilling-session applied these to `docs/domain/glossary.md`:

- New terms **Archive** (the `ARCHIVE.md` closed-entry record), **Live
  entry** (an entry listed in `INDEX.md`), and **Close** (moving an entry
  to the archive at a terminal state) — the vocabulary for the format's
  closure layer.
- **Standalone install** generalized from "a standards plugin" to any
  marketplace plugin used without working-process (skills still load and
  run; rules/engine-dependent behavior degrades) — the widening the 0.1.0
  spec deferred until project-memory had skills, which it now does.
- **Idea entry** left unchanged: its lifecycle states are unaffected; only
  *where* each state lives changed, which the new terms carry.
