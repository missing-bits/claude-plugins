# project-memory

An in-repo memory store for Claude Code sessions, parallel to the built-in
home-dir memory but living in the project, in two parts:

- **Team memory** — `docs/memory/`, committed, shared with the team. Holds
  team-relevant parked ideas, cross-ticket state, and operational gotchas.
- **Private memory** — `.claude/memory/`, per-user, always git-ignored.

Each part holds a thin `MEMORY.md` of live entries (loaded at session start),
an `ARCHIVE.md` of closed-entry lines (read on demand), and the live entry
bodies (pulled only when relevant).

## Rules

The plugin ships two rule files as a Rules payload:

- `project-memory.md` — the always-on core: loads each part's `MEMORY.md`
  at session start (skipping an index Auto-memory already loaded), watches
  `autoMemoryDirectory` for divergence from the store path, routes
  project-scoped facts to the store (best-effort) instead of home-dir
  memory, and owns Team memory's tracked/ignored first-create question.
  Always-on deliberately: index loading has no file path to scope on.
- `project-memory-conventions.md` — paths-scoped to the two store
  directories: note/idea entry shapes, the required H1 and `description` and
  the index line projected from them, top-level placement of the plugin's own
  frontmatter fields, the tolerance clause for keys other tools wrote,
  team-memory scope, the gotcha↔ADR
  promotion offer, the live-only `MEMORY.md` / on-demand `ARCHIVE.md` layout,
  and the closure lifecycle.

Adoption is opt-in: without a `MEMORY.md` the core rule is a no-op — it
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
  `MEMORY.md`/`ARCHIVE.md` consistency, then walks entries toward their correct
  lifecycle state (close finished notes, promote or drop ideas, split/merge,
  sharpen entry descriptions). Recommends per entry; never bulk-cleans; never commits.
- **migrate-memory** — moves project-scoped facts about the current repo out
  of home-dir memory into this store (one direction), routing each to Team or
  Private memory and offering store adoption when none exists yet.
- **redirect-memory** — enables, disables, or inspects the Auto-memory
  redirect that makes Private memory a Hybrid store: one
  `autoMemoryDirectory` key in `.claude/settings.local.json`, written
  with the current environment's realpath, warned about honestly, and
  verified in the next session.

## Store layout

Each part keeps a thin `MEMORY.md` of **live** entries (the only file read at
session start), an `ARCHIVE.md` of closed-entry lines (Done / Dropped, read on
demand), and the live entry bodies. A closed entry keeps no body — only its
one-line archive record.

Every entry opens with an H1 and carries a one-line `description:` in its
frontmatter, and its index line is a projection of the two — link text from
the H1, summary from `description` — so index lines are re-derived, never
authored by hand. Frontmatter written by other tools is left alone.

## Hybrid store (opt-in)

With the redirect active, `.claude/memory/` is also the session's
Auto-memory directory: Claude Code loads the store's `MEMORY.md` itself
(200-line / 25 KB budget) and writes its own notes there as ordinary
entries — a missing H1 is format debt the review session pays down, and
foreign frontmatter keys are left alone. The redirect is per environment
(host, dev container, WSL — each has its own path namespace and trust
record) and per checkout; the losing side of a switch keeps rule-driven
loading and a plainly-worded divergence message. Team memory never joins
the redirect — Auto-memory's team mounts are server-backed, and the
committed, reviewed, branch-following store is the point of Team memory,
not a limitation.
