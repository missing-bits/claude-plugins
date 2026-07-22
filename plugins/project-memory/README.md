# project-memory

An in-repo memory store for Claude Code sessions, parallel to the built-in
home-dir memory but living in the project, in two parts:

- **Team memory** — `docs/memory/`, committed, shared with the team. Holds
  team-relevant parked ideas, cross-ticket state, and operational gotchas.
- **Private memory** — `.claude/memory/`, per-user, always git-ignored.

Each part holds a thin `INDEX.md` of live entries (loaded at session start),
an `ARCHIVE.md` of closed-entry lines (read on demand), and the live entry
bodies (pulled only when relevant).

## Rules

The plugin ships two rule files as a Rules payload:

- `project-memory.md` — the always-on core: loads each part's `INDEX.md`
  at session start, routes project-scoped facts to the store (best-effort)
  instead of home-dir memory, and owns Team memory's tracked/ignored
  first-create question. Always-on deliberately: index loading has no file
  path to scope on.
- `project-memory-conventions.md` — paths-scoped to the two store
  directories: note/idea entry shapes, team-memory scope, the gotcha↔ADR
  promotion offer, the live-only `INDEX.md` / on-demand `ARCHIVE.md` layout,
  and the closure lifecycle.

Adoption is opt-in: without an `INDEX.md` the core rule is a no-op — it
never scans, creates, or nags. The store exists only once you create it.

## Installation

Claude Code does not load plugin rules by itself. The payload is installed
by the working-process plugin's Rules engine:

1. `/plugin install project-memory@missing-bits`
2. `/plugin install working-process@missing-bits` (brings the engine)
3. Run the `working-process:sync-rules` skill and pick this payload.

The engine dependency is operational only — it installs and updates the
rule files. The rules' content does not require the working-process
*rules*: without them there is simply no Process-directory ceremony beyond
the core rule's own tracked/ignored question, no ADR/glossary promotion
offers, and no `ticket` frontmatter on idea entries. With them, `docs/memory/`
counts as a Process directory and the routing targets light up.

## Skills

- **memory-review-session** — an explicit-ask grooming conversation: audits
  `INDEX.md`/`ARCHIVE.md` consistency, then walks entries toward their correct
  lifecycle state (close finished notes, promote or drop ideas, split/merge,
  sharpen index lines). Recommends per entry; never bulk-cleans; never commits.
- **migrate-memory** — moves project-scoped facts about the current repo out
  of home-dir memory into this store (one direction), routing each to Team or
  Private memory and offering store adoption when none exists yet.

## Store layout

Each part keeps a thin `INDEX.md` of **live** entries (the only file read at
session start), an `ARCHIVE.md` of closed-entry lines (Done / Dropped, read on
demand), and the live entry bodies. A closed entry keeps no body — only its
one-line archive record.
