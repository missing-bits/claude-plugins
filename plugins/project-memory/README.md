# project-memory

An in-repo memory store for Claude Code sessions, parallel to the built-in
home-dir memory but living in the project, in two parts:

- **Team memory** — `docs/memory/`, committed, shared with the team. Holds
  team-relevant parked ideas, cross-ticket state, and operational gotchas.
- **Private memory** — `.claude/memory/`, per-user, always git-ignored.

Each part holds a thin `INDEX.md` (one-line pointers) plus flat topic
files: the index loads at session start, topic files are pulled only when
relevant.

## Rules

The plugin ships two rule files as a Rules payload:

- `project-memory.md` — the always-on core: loads each part's `INDEX.md`
  at session start, routes project-scoped facts to the store (best-effort)
  instead of home-dir memory, and owns Team memory's tracked/ignored
  first-create question. Always-on deliberately: index loading has no file
  path to scope on.
- `project-memory-conventions.md` — paths-scoped to the two store
  directories: note/idea entry shapes, team-memory scope, the gotcha↔ADR
  promotion offer, and the no-empty-files lifecycle.

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
