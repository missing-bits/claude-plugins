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
  `ticket`-exempt registry file like `INDEX.md`.

`INDEX.md` holds only **live** entries, sectioned per part: a **Notes**
section (active notes, recall-on-demand) and an **Ideas** section (only
`parked` ideas, each a link to its `idea-` file). Closed entries — promoted,
finished, or dropped — do not live here; they move to `ARCHIVE.md` the moment
they close (see Lifecycle). `INDEX.md` is the only file read at session start,
so it never carries history.

## Entry shapes

Shape, not topic, is the criterion; the `idea-` prefix is authoritative (the
INDEX section and frontmatter follow it).

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
  body; move the `INDEX.md` line to `ARCHIVE.md` **Done** as a redirect
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

Never leave an empty or stub body file. `INDEX.md` and `ARCHIVE.md` are
registry files, not bodies: an empty section header in either is fine.
