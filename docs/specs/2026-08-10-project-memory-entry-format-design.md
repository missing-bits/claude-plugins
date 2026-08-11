---
ticket: none
date: 2026-08-10
status: approved
grilled: 2026-08-10
architect: LGTM
branch: feature/memory-entry-format
base: develop
---

# Project-memory entry format — a canonical description and a tolerance clause

## Problem

The store's entry shape costs us in two places today.

**The index line has no source.** A Project-memory entry carries no summary of
itself. The one-line summary that makes an entry findable lives only in its
`INDEX.md` line, written by hand. Nothing ties it to the entry it points at,
so it drifts as the entry grows, and `memory-review-session` has nothing to
check it against — it can only ask whether the line reads well.

**Moving a fact into the store means translating it.** `migrate-memory` reads
home-dir memory, whose entries in practice carry `name` / `description` /
`metadata` frontmatter, and writes entries in an unrelated shape. The skill
restates each fact instead of moving it.

Underneath both sits a third fact: Auto-memory now keeps a per-project store
of its own, with its own conventions, so a developer writing into both juggles
two mental models for one act.

This spec fixes the first two. Both payoffs — a summary that cannot drift and
a migration that copies rather than translates — arrive with the change itself;
nothing here waits on a later decision.

## Terminology

This spec says **Auto-memory** for the harness mechanism and **Home-dir
memory** for the store it manages by default. Both are canonical; the grilling
session added the first and rewrote the second, which had been defined by a
path that `autoMemoryDirectory` can move. "Native memory" stays banned, and
"native format" would have inherited that ban.

## What the platform actually guarantees

Which parts of Auto-memory are contractual and which are merely observed
shapes every decision below.

**Documented** (`code.claude.com/docs/en/memory`): Home-dir memory sits by
default at `~/.claude/projects/<project>/memory/`, one directory per
repository, shared across worktrees, machine-local. Its entrypoint is
`MEMORY.md`, of which the first 200 lines or 25 KB load each session.
`autoMemoryDirectory` redirects the directory and is read from any settings
scope, honored in project scope once the workspace trust dialog is accepted;
the value must be absolute or start with `~/`. The documentation describes
entry files as "plain markdown you can edit or delete at any time". The single
documented frontmatter field is `modified`, an ISO timestamp the harness
writes into any memory file that already has frontmatter (v2.1.214+).

**Not documented**: the `name` / `description` / `metadata.type` shape and its
`user | feedback | project | reference` taxonomy. These are observable in the
shipped binary and in live sessions, but the published contract for entry
bodies is "any markdown". The surface has also moved repeatedly inside one
minor line — the 25 KB limit, the change in how the limit is counted, the
`modified` field, and the switch from silent truncation to an explicit error
all landed in separate releases.

The conclusion that shapes this spec: **there is no documented entry format to
adopt.** What follows therefore converges on good field names without ever
declaring Auto-memory the source of the plugin's format — recorded as
[ADR 0002](../domain/adr/0002-own-entry-format.md), since the hybrid decision
will meet the same question again.

## Decisions

### `description` becomes the canonical summary

Every entry carries a `description:` — one line, the summary that makes it
findable, and opens with an H1 carrying its title. The H1 was a habit before;
the projection makes it a requirement, because the whole `INDEX.md` line
projects from the entry, both halves of it: the link text from the H1, the
text after the dash from `description`.

```
- [H1 of the entry](file.md) — <description>
```

On drift the entry wins: the file is the entry, the index is a view of it.
Without code the strings must live in two files — the index exists precisely
to spare the reader the bodies — but naming an authority turns a subjective
review question into a mechanical one.

Both halves being derived has one consequence worth stating plainly: nobody
edits an index line directly any more. A wrong title is fixed in the entry's
H1, a stale summary in its `description`, and the line follows.

Registry files carry no frontmatter and no `description`: `INDEX.md` and
`ARCHIVE.md` are registers, not entries. Only `INDEX.md` is a projection.
`ARCHIVE.md` is the opposite — a closed entry keeps no body, so its archive
line is the sole surviving record of it, derived from nothing and
re-derivable from nothing.

### Plugin fields stay at the top level

`status`, `spec`, `ticket` and `adr-candidate` remain top-level keys, never
nested under `metadata:`. Two reasons, and the first is decisive: the
`ticket-frontmatter` rule publishes an anchored sweep,
`rg -l --no-ignore '^ticket:.*ABC-123' docs/ .superpowers/`, which nesting
breaks across the whole repository, not merely in the store. Second, nesting
would mean *relying* on the observed behavior that the harness folds unknown
top-level keys into `metadata` — and the failure is asymmetric. If that folding
stops, top-level fields lose nothing, since a reader simply ignores them;
restructuring `metadata` would force a rewrite of every file.

### Unknown frontmatter keys are preserved

The conventions rule gains a tolerance clause: entries may carry frontmatter
written by other tools; the plugin's rules and skills leave unknown keys
alone; an unknown key never changes an entry's shape, and the `idea-` prefix
stays the authoritative discriminator.

One sentence makes the store safe to share with any other writer, `modified`
included.

### `name` is not adopted

The filename already carries identity and the H1 carries the title. A third
encoding would need a tie-break rule for the case where they disagree. Finding
M4 of the 2026-07-20 round settled exactly that ambiguity — "three encodings
of shape … with no tie-break" — by naming the `idea-` prefix authoritative and
the rest derived.

### `type` is read, never written

The plugin does not write `metadata.type`. Its values do not partition the
plugin's space — a note and an idea are both "project" — and they answer a
question the store does not ask.

It is useful in one direction only, and only weakly: when `migrate-memory`
reads home-dir entries, `type: user` and `type: feedback` are a hint that a
fact may be personal rather than project-scoped, so the skill considers those
entries last. The hint never decides. The plugin's routing turns on whether a
fact is scoped to this repository, not on the harness's taxonomy — a per-user
fact about this repo belongs in Private memory ("per-user → Private memory"),
and only personal, cross-project facts stay in Home-dir memory. Content
judgment remains the criterion and overrides the hint, so no candidate is
dropped before the developer sees it.

This deliberately does **not** reverse finding I1 of the 2026-07-20 round
("`type`-keyed routing binds to a taxonomy the native memory model does not
expose … not a documented, stable interface — unsafe for a distributable
rule"). That finding stands, and re-verification confirms its premise holds:
the taxonomy is still undocumented and the surface around it has kept moving.
Reading a field to classify someone else's data is not the same as coding a
distributable rule against it.

## Component changes

**`project-memory-conventions` rule** — the Entry shapes section gains the
required `description`, the index-projection statement with its drift
authority, the top-level placement of plugin fields with its reason, so that
no one "tidies" it later, and the tolerance clause.

**`migrate-memory`** — the "Translate shape" step shrinks to two acts: decide
the prefix, add the plugin's fields. `description` carries over unchanged,
which is the point of the convergence; `name` and `metadata.type` do not,
since the plugin writes neither. `name` still has to go somewhere, though: a
home-dir entry carries its title in that field and has no H1, so migration
turns `name` into the new entry's H1 and its slug into the filename. The field
is dropped, the information is not — and the step that deletes the source file
is irreversible, so this is not a detail to leave implied. The tolerance clause protects keys another
writer put in a file, not keys this skill chooses to import. Ordering by
`type` is the weak hint described above, never a filter. The skill keeps its
direction, its consent model, and its "never commits" boundary.

One error path the skill does not know about today: its migration trace writes
a roll-up line into the Home-dir index, which Auto-memory loads and therefore
caps at 200 lines or 25 KB. Past the cap the write returns an error. The skill
keeps the trace to one line and, on that error, shortens rather than retries.

**`memory-review-session`** — the opening audit gains three defect checks:
index lines whose text differs from their entry's `description`; index lines
whose link text differs from the entry's H1; and frontmatter keys the plugin
does not define, reported and never removed. The existing subjective step 4 of
the entry walk ("does the line summarize it well?") narrows to judging the
`description` itself, since the line is now derived from it.

Alongside them the audit gains one non-defect category. A missing
`description` is **format debt**, not a fault: the field is new, so every
entry a store already holds lacks it — nineteen in this repo's own Private
memory. Debt is counted and listed apart from the defects the audit opens
with; a dangling link is broken, an entry written before the field existed is
not. Note that only this check fires store-wide: drift needs both halves
present to disagree, so on an entry with no `description` there is nothing for
the drift check to compare. Drift stays a defect precisely because both halves
are there.

**README** — the entry-shape summary follows the rule.

No other plugin changes. `working-process` does read entry frontmatter — its
`ticket` sweep scans `docs/` and so reaches Team memory — but the field it
reads keeps its position and meaning, which is the point of the decision
above. The two standards plugins touch the store only through their
store-existence probes, which look at `INDEX.md` and never open an entry.

## Migration

None required. Nothing breaks: an entry without `description` still parses,
still loads, still points somewhere. What the change leaves behind is not a
migration but format debt, and it is repaid two ways. The systematic pass is
`memory-review-session`, which lists the debt and offers to fill it while it
walks; the incidental one is any write that needs an index line re-projected,
since the line can only be derived from a `description` that exists — so a
touch on a pre-format entry backfills the field rather than hand-writing the
line. No compatibility window, no detection of half-migrated stores, no
coordination across installs.

## Out of scope

- **The index rename and the hybrid**, together as one later decision.
  Renaming `INDEX.md` to `MEMORY.md` only pays if the store also becomes the
  Auto-memory directory; on its own it is a breaking change across four
  plugins for no operational gain, and it would hand one file two writers with
  contradictory invariants (the documented 200-line budget against the store's
  "live entries only, never carries history").
- **Decoupling the foreign-plugin probes** from the index filename — parked
  separately, non-breaking, and the prerequisite that would make that rename a
  single-plugin change.
- **A budget on the Project-memory index** and **adopting `modified`**: both
  belong to a store Auto-memory actually reads, which this one is not. The
  budget still binds where the plugin writes into Home-dir memory, handled
  under `migrate-memory` above.

## Alternatives considered

**Full compatibility with the Auto-memory entry shape** — also writing `name`
and `metadata.type` so entries are indistinguishable from Auto-memory's own.
Rejected: it reverses I1 without a new premise, and adds a fourth encoding of
an entry's shape beside the filename prefix, the index section, and the
frontmatter set.

**Convergence plus `name`** — rejected above; a field with no consumer is not
worth the tie-break rule it needs.

**Shrinking the plugin to Team memory only**, handing Private memory to the
harness and contributing conventions to it. Raised in consultation and worth
recording: Home-dir memory is per-project, private and machine-local, which is
what Private memory is, so the overlap is real. Rejected for now because it
costs the two-part symmetry, the `migrate-memory` story, and the location
model (`.claude/` private, `docs/` team) that was itself an argued decision —
and because it is a strategy question that should not ride inside a format
change. It belongs with the hybrid decision.

## Design inputs

Both working-process consultation personas ran on Opus 5 from one shared
briefing, each with its own focusing question, in the background, and neither
saw the other's contribution. A consultation returns no verdict, so nothing is
stamped.

The architect supplied the distinction underlying this spec — convergence (the
plugin defines its own format and happens to pick the same field names)
against referential adoption (the rule declares the plugin's shape to be
Auto-memory's shape, surrendering semantics) — and the asymmetry that decides
it: the store holds durable, versioned, team-shared data, while the format
remains a moving internal detail of a self-updating tool. The architect also
found I1 and argued that the rename bundles two changes.

The system designer supplied the delivery mechanics: skills ship with the
plugin version, rules reach a machine only through `sync-rules`, so "new
skills, old rules" is the default state right after an update. That is what
makes any rename of a rule-loaded filename unrecoverable from inside the
change, and why this spec contains no rename. The designer also caught that
after a rename both the source and the target index in `migrate-memory` would
be called `MEMORY.md` — in a skill whose whole job is moving lines between
them.

The two disagreed on one fact: whether project settings honor
`autoMemoryDirectory`. The documentation settles it — they do, once the
developer accepts the workspace trust dialog. Neither position affects this
spec.

## Glossary

Applied during the grilling session:

- **Auto-memory** added — the harness mechanism, explicitly never a store, so
  the `_Avoid_: native memory` ban has a positive counterpart;
- **Home-dir memory** rewritten as the store Auto-memory manages, its path
  demoted from definition to default.

## Architect findings (round 1, 2026-08-10)

Verdict: `concerns` (fable 5, 2026-08-10) — dispatched at the prescribed tier
(most capable available), so no fallback field. One Important, two Minor. The
round confirmed the claims the spec makes about the other four plugins, the
`^ticket:` sweep, the additive-migration property, and the versioning section,
and endorsed ADR 0002 against the ADR-format bar.

**Important**

1. **F1 — the `type` candidate filter misreads the plugin's own routing.** The
   spec claims the routing rules "send `user` and `feedback` facts elsewhere",
   but the core rule routes per-user *project-scoped* facts INTO the store
   ("per-user → Private memory"); only personal, non-project-scoped facts stay
   in Home-dir memory. A home-dir entry tagged `type: user` — "in this repo
   the developer prefers X" — is exactly a Private-memory candidate, and the
   filter drops it before the per-fact consent step, so the consent gate never
   catches the omission. The skill's canonical criterion is content, and the
   spec never says the filter is subordinate to it.

**Minor**

2. **F2 — migration's treatment of the source's Auto-memory keys is
   unspecified.** "Decide the prefix, add the plugin's fields" implies carrying
   the source frontmatter wholesale, including `name` and `metadata.type`,
   which collides with the spec's refusal to write either. The tolerance
   clause makes a lingering `name` harmless, so either choice works — but a
   distributable skill needs the sentence.
3. **F3 — the spec's own frontmatter carries a banned term.** The `branch:`
   value commits "native memory" — `_Avoid_` under both **Auto-memory** and
   **Home-dir memory** — into the document whose Terminology section declares
   that term banned.

**Resolution (2026-08-10, no fresh round).** All three applied:

- **F1** — the false claim about the plugin's routing is gone. `type` is now a
  weak ordering hint that content judgment overrides, stated together with the
  actual rule (a per-user fact about this repo belongs in Private memory), so
  nothing is dropped before the developer sees it.
- **F2** — migration carries `description` and leaves `name` and
  `metadata.type` behind, with the reason: the tolerance clause protects keys
  another writer put in a file, not keys this skill imports.
- **F3** — the topic branch renamed to `feature/memory-entry-format` and
  `branch:` updated. Nothing had been pushed, so the rename cost nothing.

The architect's suggestion outside the findings — spelling out that a derived
index line is never edited directly — was applied too.

## Architect findings (round 2, 2026-08-10)

Verdict: `LGTM` (fable 5, 2026-08-10) — dispatched at the prescribed tier, so
no fallback field. Four Minor, all wording reconciliations, all applied:

1. **M1** — the audit description still said "four mechanical checks" after
   the amendment reclassified the first one, the store count was 21 (which
   counted the two registry files this spec excludes from "entry"), and the
   claim that two checks fire store-wide contradicted the spec's own reason
   that drift needs both halves present. Applied: three defect checks plus one
   debt category, nineteen entries, only the debt check fires store-wide.
2. **M2** — calling `ARCHIVE.md` a view invited treating archive lines as
   regenerable; a closed entry keeps no body, so its line is the only record
   there is. Applied.
3. **M3** — "backlog" is `_Avoid_`-banned twice in the glossary, and this text
   ships into a grooming skill whose other subjects are parked ideas and
   closed entries, exactly where the ban applies. Applied: **format debt**.
4. **M4** — backfill was attributed only to the review session, while the
   shipped rule makes any re-projection require a `description` too. Applied
   in the Migration section.

The round also verified the platform-guarantees section against the live
documentation, both earlier amendments against the shipped rule and a live
Home-dir entry, and the cross-plugin claims. Two observations recorded outside
its findings, carried into the plan: index lines today carry status flavor
("parked (confirmed):") that will land inside `description` and can drift
against the `status` field with no mechanical check, and `description` values
routinely contain `: `, so the rule's example quotes the scalar.

## Amendments (2026-08-10, after plan-adversary round 2)

Writing the plan exposed three holes in this spec, all found by the second
plan-adversary round (Opus 5) and verified against the repo before being
applied here:

- **The projection had no left source.** Nothing in the plugin required an
  entry to have an H1, yet the index line's link text was defined as one.
  The `description` section now requires it.
- **Migration would have lost the title.** Home-dir entries carry their title
  only in `name`, which this spec declines to write, while the skill's next
  step deletes the source file. The `migrate-memory` section now routes `name`
  into the new entry's H1.
- **"Opportunistically" was never operationalized.** With the field new, the
  audit would have reported every existing entry as a defect. The
  `memory-review-session` section now separates format debt from defects.

None of the three reverses a decision or an architect finding; each makes
explicit what the design already assumed.

## Versioning

No version bump on this branch. Per the plugin-versioning rule the release PR
from `develop` to `master` mints the bump once; a `-dev.` suffix appears here
only if we dogfood the change before then. The change is additive and breaks
nothing, so it sizes as a minor.
