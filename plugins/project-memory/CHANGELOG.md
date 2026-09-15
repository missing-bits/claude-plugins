# Changelog — project-memory

Released versions of this plugin, newest first.

## 0.5.1 — 2026-09-15

- The plugin ships this changelog.

## 0.5.0 — 2026-08-29

- The grooming audit reads a relocated `status` field, and the
  conventions rule states where the field is written alongside the
  tolerant read.
- The `adr-candidate` sweep anchors its grep per the rule's own clause.

## 0.4.0 — 2026-08-12

- Every entry opens with an H1 and carries a one-line `description:`.
  The index line is a projection of the two, and the entry wins on
  drift. The plugin's own frontmatter fields stay top-level, with a
  tolerance clause for keys other tools wrote.
- The live index renames `INDEX.md` to `MEMORY.md` in both parts;
  `ARCHIVE.md` keeps its name. The core rule reads a pre-rename store,
  and the conventions rule offers a one-time rename that a decline
  leaves readable.
- The Hybrid store arrives as an opt-in switch: the new
  `redirect-memory` skill points Claude Code's Auto-memory at
  `.claude/memory/` through `autoMemoryDirectory`, always as the current
  environment's realpath. The core rule deduplicates index loading and
  reports a divergent redirect.
- `memory-review-session` audits `MEMORY.md`, re-sections
  harness-appended lines, and scopes a walk as a first-class choice
  while the audit stays whole-part.
- `migrate-memory` path-qualifies store names and detects the hybrid
  no-op.
- Entry prose routes through
  `elements-of-style:writing-clearly-and-concisely` when the skill is
  available.

## 0.3.0 — 2026-08-05

- The `docs/memory` first-create question reads a declared instruction
  as the decision already made.
- Trigger evals cover the memory skills, including the cross-project
  pair.

## 0.2.0 — 2026-07-22

- The `memory-review-session` grooming skill and the `migrate-memory`
  home-dir-to-project skill.
- The index holds live entries only; closed entries move to an
  `ARCHIVE.md` read on demand.

## 0.1.0 — 2026-07-21

- The project-memory rules leave `working-process` for this plugin.
