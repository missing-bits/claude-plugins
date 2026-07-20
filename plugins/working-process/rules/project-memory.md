# Project memory

An in-repo memory store parallel to Claude Code's home-dir memory, but living
in the project, in two parts:

- **Team memory** — `docs/memory/`, committed, shared with the team.
- **Private memory** — `.claude/memory/`, per-user, always git-ignored.

Each part holds a thin `INDEX.md` (one-line pointers) plus flat topic files.

## Loading

When a part's `INDEX.md` exists, read it at session start and pull a topic
file only when its index line is relevant. If neither `INDEX.md` exists this
rule is a no-op — it never scans, creates, or nags.

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
project-memory-conventions rule for the INDEX sections and entry shapes (no
`INDEX.md` yet exists to trigger it), and — for Team memory (`docs/memory/`) —
carry the tracked/ignored first-create question before writing anything, since
the paths-scoped process-artifacts rule does not activate at `docs/memory/`.
Private memory (`.claude/memory/`) is always ignored, so it is never asked.

Entry shapes, team-memory scope, and the lifecycle live in the
project-memory-conventions rule, which loads when you touch a memory file.
