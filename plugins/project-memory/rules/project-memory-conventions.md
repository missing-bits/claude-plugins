---
paths:
  - "docs/memory/**"
  - ".claude/memory/**"
---

# Project memory — conventions

## Locations

- **Team memory** `docs/memory/` — the tracked/ignored question applies,
  asked by the project-memory core rule. It may start ignored to defer the
  commit; the flip to tracked is a manual, unprompted developer action (a
  `*`-only `.gitignore` self-ignores, so flipping means deleting it or
  force-adding — which Claude never does or suggests). When the
  working-process rules are installed, the directory counts as a Process
  directory there.
- **Private memory** `.claude/memory/` — always git-ignored (`.gitignore`
  containing exactly `*`), never asked: a per-user store under the
  `.claude/` config namespace.
- **Archive** `ARCHIVE.md` (per part) — the closed-entry record: one line per
  closed entry, in a **Done** or **Dropped** section. Read on demand only
  (e.g. answering "did we already consider this?"), never at session start. A
  `ticket`-exempt registry file like `MEMORY.md`.

`MEMORY.md` holds only **live** entries, sectioned per part: a **Notes**
section (active notes, recall-on-demand) and an **Ideas** section (only
`parked` ideas, each a link to its `idea-` file). Closed entries — promoted,
finished, or dropped — do not live here; they move to `ARCHIVE.md` the moment
they close (see Lifecycle). `MEMORY.md` is the only file read at session
start, so it never carries history. The harness caps any index it loads —
200 lines / 25 KB; in a Hybrid store that is this file. Keep lines thin,
and when a write bounces off the cap, shorten the index rather than retrying.

### Stores that predate the rename

A store whose live index is still named `INDEX.md` predates this
convention. Offer once to rename the file to `MEMORY.md` (`git mv` in a
tracked part, a plain rename in an ignored one) — content untouched, and
nothing to re-point: no plugin outside project-memory names the index
file. Declined, the offer rests for the session; the core rule keeps
reading the old-named index meanwhile, so nothing goes dark.

## Entry shapes

Shape, not topic, is the criterion; the `idea-` prefix is authoritative (the
index section and frontmatter follow it).

Every entry opens with an H1 carrying its title and carries a `description:`
— one line, the summary that makes it findable. Its `MEMORY.md` line is a
projection of the entry, both halves of it: the link text from the H1, the
text after the dash from `description`.

    - [H1 of the entry](file.md) — <description>

Quote the `description` scalar whenever it contains `: `, as index summaries
routinely do. Nothing parses entry frontmatter today, but an unquoted colon
makes the block invalid YAML the moment something does.

On drift the entry wins — the file is the entry, the index a view of it — so
an index line is never authored directly, only re-projected: correct the H1 or
the `description` first, then re-derive the line from them. `MEMORY.md` and
`ARCHIVE.md` are registry files, not entries: no frontmatter, no
`description`, no H1 requirement.

- **note** (no prefix) — a gotcha or cross-ticket state; a cross-ticket
  registry, exempt from any per-work `ticket` convention the project keeps.
  It may carry an optional `adr-candidate: yes` frontmatter flag — presence
  marks a decision-shaped note for later ADR review
  (`rg 'adr-candidate:'`); absent means not a candidate.
- **idea** (`idea-<slug>.md`) — a `parked` idea (a live entry). Frontmatter:
  `status` (parked → spec'd | dropped), a `spec:` pointer once it graduates,
  and — when the project links documents to its issue tracker (e.g. the
  working-process ticket-frontmatter convention) — `ticket`. On graduation or
  drop the body closes per the Lifecycle section; the `spec:` pointer then
  lives on the `ARCHIVE.md` Done redirect line, not a live file.

Every field this rule defines — `description`, `status`, `spec`, `ticket`,
`adr-candidate` — sits at the top level of the frontmatter, never nested
under a `metadata:` block. Nesting would break the anchored `^ticket:` sweep
the project's ticket convention publishes (when it keeps one), across the
whole project rather than only in the store.

Entries may carry frontmatter that other tools wrote. Leave unknown keys
alone: never remove them, never rewrite them, and never let one change an
entry's shape — the `idea-` prefix stays authoritative. In a Hybrid store
Auto-memory is a second writer: an entry it writes is an ordinary note
whose missing H1 is format debt, and an index line it appends lands
section-blind — re-sectioning belongs to the grooming walk
(memory-review-session, when available), never to a routine write.

When the `elements-of-style:writing-clearly-and-concisely` skill is
available, entry prose gets its pass: invoke it before writing a new body
or `description`, and run an explicit editing pass when reshaping one.
The pass binds wording, never an entry's content or lifecycle; entries
Auto-memory writes on its own keep their own voice. Without the skill
there is no substitute pass.

## Team-memory scope

Team memory owns only parked ideas, cross-ticket initiative state, and
operational gotchas. Route elsewhere — each target only where the project
keeps it (e.g. via working-process):

- a decision with a rationale and a real trade-off → an ADR
  (`docs/domain/adr/`), when the project records ADRs;
- a canonical term or `_Avoid_` ban → the domain glossary, when the project
  keeps one;
- the todo/steps of one task → that work's plan;
- a unit of work tracked in the issue tracker → the `ticket`;
- any per-user fact → Private memory or home-dir memory.

Without such a target, an entry simply stays a note.

## gotcha vs ADR

Default every entry to a note. When an entry is decision-shaped — hard to
reverse AND surprising without context AND a real trade-off existed — and
the project records ADRs, offer to promote it to an ADR; the developer
decides. A promoted note links to its ADR.

## Lifecycle — closing entries

A live entry keeps a body only while it holds live content; a closed entry
keeps no body, only a one-line `ARCHIVE.md` record. The governing test: a
body survives closure only when no other artifact carries its content.

- **Promotion** (content moves to a spec, ADR, or the glossary): delete the
  body; move the `MEMORY.md` line to `ARCHIVE.md` **Done** as a redirect
  pointer to the new home.
- **Closed note** (a work-state note after its release, an expired gotcha
  whose resolution now lives in code or docs): delete the body; write an
  `ARCHIVE.md` **Done** line naming where the detail now lives (spec/plan,
  release version, optionally a commit) plus the closure date. If a fragment
  has no home in any document, the entry is not yet closed — or that fragment
  becomes the Done line.
- **Dropped** (abandoned): write an `ARCHIVE.md` **Dropped** line — reason
  plus date — and delete the body. There is no body-retention directory: if
  the rejection analysis is worth keeping, that is the signal the entry is
  decision-shaped (offer an ADR — "rejected X because Y" — when the project
  records ADRs) or reference-shaped (keep it a live note); a kept body is
  then not dropped.
- **Obsolete** (no longer true, nothing worth pointing at): delete the body
  and its index line — no `ARCHIVE.md` record.

Never leave an empty or stub body file. `MEMORY.md` and `ARCHIVE.md` are
registry files, not bodies: an empty section header in either is fine.
