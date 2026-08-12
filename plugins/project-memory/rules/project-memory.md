# Project memory

An in-repo memory store parallel to Claude Code's home-dir memory, but living
in the project, in two parts:

- **Team memory** — `docs/memory/`, committed, shared with the team.
- **Private memory** — `.claude/memory/`, per-user, always git-ignored.

Each part holds a thin `MEMORY.md` (one-line pointers to live entries) plus
flat topic files, and an `ARCHIVE.md` of closed-entry lines read on demand —
never at session start.

## Loading

When a part's `MEMORY.md` exists, read it at session start and pull a topic
file only when its index line is relevant — unless the session context
already carries that index: in a Hybrid store, Auto-memory loads Private
memory's `MEMORY.md` itself, and reading it twice buys nothing. If neither
`MEMORY.md` exists this rule is a no-op — it never scans, creates, or nags.

One exception to the no-op: a part directory holding an `INDEX.md` and no
`MEMORY.md` is a store from before the rename, never "no store". Say so at
session start, point at the conventions rule's rename offer, and read the
old-named index as the part's index meanwhile — the Adoption clause must
never create a second index beside it.

When Private memory exists (`.claude/memory/` present) and
`.claude/settings.local.json` carries `autoMemoryDirectory`, compare its
value with the realpath of `<project>/.claude/memory`. On a mismatch, say
so plainly: the redirect points elsewhere in this session's filesystem
namespace, so Auto-memory is writing a stray store or none at all — the
platform gives no other visible signal. Never edit settings from this rule;
that is the redirect-memory skill's job, when it is available.

## Routing (best-effort)

Project-scoped facts *should* go to Project memory rather than home-dir memory;
home-dir memory keeps cross-project and personal facts and stays auto-loaded,
unchanged. This is best-effort, not enforced: a rule steers, it does not
guarantee. On a miss a fact lands in home-dir memory and can be moved later.

- team-relevant → Team memory;
- per-user → Private memory;
- on collision for a project-scoped fact, the project store wins.

## Adoption

Adoption is opt-in: the store exists only when the developer creates it. Offer
to create it only when the developer signals intent to record something
project-scoped — never proactively. On first creation, point at the
project-memory-conventions rule for the index sections and entry shapes (no
`MEMORY.md` yet exists to trigger it).

For Team memory (`docs/memory/`), ask the tracked/ignored question before
writing anything — this rule owns that question:

- **Ignored**: write a `.gitignore` containing exactly `*` into
  `docs/memory/`; its contents stay out of the repo.
- **Tracked**: files are committed like any other; no `.gitignore` is
  written.

Never ask when a prior decision is present: a `.gitignore` containing
exactly `*` means ignored was chosen; any git-tracked file under the
directory means tracked; and an
explicit project instruction declaring the mode (e.g. a CLAUDE.md
note) counts as the decision — a declared ignored mode is
materialized by whoever first acts on it (writing the `*`
`.gitignore`), a declared tracked mode becomes observable with the
first committed file. Private memory (`.claude/memory/`) is always
ignored, so it is never asked. When the working-process rules are installed,
`docs/memory/` additionally counts as a Process directory there.

Entry shapes, team-memory scope, and the lifecycle live in the
project-memory-conventions rule, which loads when you touch a memory file.
