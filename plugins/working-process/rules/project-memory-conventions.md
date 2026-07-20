---
paths:
  - "docs/memory/**"
  - ".claude/memory/**"
---

# Project memory — conventions

## Locations

- **Team memory** `docs/memory/` — a Process directory; the first-create
  tracked/ignored question applies. It may start ignored to defer the commit;
  the flip to tracked is a manual, unprompted developer action (a `*`-only
  `.gitignore` self-ignores, so flipping means deleting it or force-adding —
  which Claude never does or suggests).
- **Private memory** `.claude/memory/` — always git-ignored (`.gitignore`
  containing exactly `*`), never asked, and NOT a Process directory: a
  per-user store under the `.claude/` config namespace.

`INDEX.md` is sectioned per part: a **Notes** section (recall-on-demand) and
an **Ideas** section (a browsable backlog). The Ideas section lists each entry
in its lifecycle state: parked (a link to its `idea-` file), spec'd (a redirect
line to the spec, no file), or dropped (a struck-through tombstone with the
reason).

## Entry shapes

Shape, not topic, is the criterion; the `idea-` prefix is authoritative (the
INDEX section and frontmatter follow it).

- **note** (no prefix) — a gotcha or cross-ticket state. `ticket`-exempt (a
  cross-ticket registry, like the glossary). It may carry an optional
  `adr-candidate: yes` frontmatter flag — presence marks a decision-shaped
  note for later ADR review (`rg 'adr-candidate:'`); absent means not a
  candidate.
- **idea** (`idea-<slug>.md`) — a parked idea. Frontmatter: `status`
  (parked → spec'd | dropped), a `spec:` pointer once it graduates, and
  `ticket`.

## Team-memory scope

Team memory owns only parked ideas, cross-ticket initiative state, and
operational gotchas. Route elsewhere:

- a decision with a rationale and a real trade-off → an ADR (`docs/domain/adr/`);
- a canonical term or `_Avoid_` ban → the glossary;
- the todo/steps of one task → that work's plan;
- a unit of work tracked in the issue tracker → the `ticket`;
- any per-user fact → Private memory or home-dir memory.

## gotcha vs ADR

Default every entry to a note. When an entry is decision-shaped — hard to
reverse AND surprising without context AND a real trade-off existed — offer to
promote it to an ADR; the developer decides. A promoted note links to its ADR.

## Lifecycle — no empty files

A body file exists only while it holds live content; never leave an empty or
stub file.

- **Promotion** (content moves to a spec, ADR, or the glossary): delete the
  body file, and turn its `INDEX.md` line into a redirect pointer to the new
  home. Redirect lines are sweepable.
- **Dropped** (abandoned, nothing else records it): no body file — a one-line
  `INDEX.md` tombstone with the reason.
- **Obsolete** (no longer true, no document to point at): delete the body file
  and its index line.
