---
paths:
  - "docs/**"
---

# Ticket frontmatter

Documents under `docs/` open with a YAML frontmatter block linking them
to the issue tracker. The convention is tracker-agnostic — Jira, GitHub,
GitLab, or anything else; the field is always `ticket`.

## Field sets

- Specs and plans (`docs/specs/`, `docs/plans/`): `ticket` + `date` +
  `status` + the process and branch fields — details in the
  spec-plan-lifecycle rule.
- Review reports (`docs/code-review/`): the review-reports rule's
  frontmatter set — `date`, `mode`, `ticket`, `scope`, `runid`,
  `standards`, optional `rerun-of`, `findings` — not the bare
  `ticket`-only set of `.superpowers/**` artifacts.
- Every other document under `docs/`: `ticket` + `date`.
- Project memory (`docs/memory/`, `.claude/memory/` — when the
  project-memory plugin's rules are installed): notes and the store's
  registry files are `ticket`-exempt (like the glossary; the
  registry-file list belongs to that plugin's conventions rule); idea
  entries (`idea-*.md`) carry `ticket`. See that plugin's
  project-memory-conventions rule.
- Per-work process artifacts (`.superpowers/**`, ADRs): `ticket` only —
  see the process-artifacts rule.

## Values

- `ticket`: the tracker's short reference, never a URL — a Jira key
  (`ABC-123`), a GitHub/GitLab issue reference (`#123` or
  `org/repo#123`), or the project tracker's equivalent. Several tickets
  use the inline list form `[ABC-123, ABC-456]` — one greppable line,
  never a multi-line dash list. No ticket means an explicit
  `ticket: none`; the field is always present.
- `date`: the ISO creation date (`2026-07-13`).

## Sourcing and backfill

For a NEW document: branch name (`feature/ABC-123-...`) → conversation
context → ask the developer once; no answer means `none`. Never ask twice
for one unit of work — a plan inherits its spec's ticket, and artifacts
of the same session reuse the established value.

When editing an existing `docs/` document that has no frontmatter, add
the block as part of the edit — sourced from document content → branch →
conversation → `none`, never a question (asking is reserved for new
documents). `date` is the file's git creation date:
`git log --follow --format=%as -- <file> | tail -1`.

## Finding documents by ticket

The `ticket:` line matches both single-reference and inline-list forms;
`--no-ignore` reaches ignored-mode artifacts:
`rg -l --no-ignore '^ticket:.*ABC-123' docs/ .superpowers/`
