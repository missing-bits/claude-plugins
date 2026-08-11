---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
  - "docs/domain/**"
  - "docs/code-review/**"
  - ".superpowers/**"
---

# Process directories and artifacts

A Process directory is a directory the working process creates in a
project repo to hold work artifacts: `docs/specs/`, `docs/plans/`,
`docs/domain/`, `docs/code-review/`, `docs/memory/` (Team memory — when the
project-memory plugin's rules are installed), and the `.superpowers/` family
at the repo root.

## First-create question

When creating a Process directory — or touching one that already exists
with no prior decision (no `.gitignore` containing exactly `*`, no
git-tracked file under it, and no explicit project instruction
declaring the mode) — ASK the developer which mode the directory gets.
Assume no default:

- **Ignored mode**: write a `.gitignore` containing exactly `*` into the
  directory; its contents stay out of the repo.
- **Tracked mode**: artifacts are committed like any other file; no
  `.gitignore` is written at first-create (a narrower one added later —
  e.g. the local pocket of `docs/code-review/` — does not change the
  mode).

Never ask when any signal is already present: only a `.gitignore`
containing exactly `*` means ignored mode was chosen — one with any
other content (e.g. a local pocket's `local-*`) signals nothing by
itself; a git-tracked file under the directory (`git ls-files <dir>`
non-empty) means tracked mode was chosen; and an
explicit project instruction declaring the mode (e.g. a CLAUDE.md
note that a directory is always git-ignored) counts as the decision.
A declared ignored mode is materialized by whoever first acts on it —
writing the `*` `.gitignore` — making the decision observable; a
declared tracked mode becomes observable with the first committed
file. This rule owns the signal list; other surfaces reference it
rather than restating it (the self-contained restatements of the review commands
and the project-memory core rule are the justified exceptions).

`docs/memory/`'s tracked/ignored first-create question is asked by the
project-memory plugin's core rule (when installed), not this one — it is
listed above only so `docs/memory/` counts as a Process directory for the
conventions below.

## Handling artifacts

- Tracked mode: artifact updates ride along with the commits of the work
  they belong to — never leave them dirty. Committing stays with the
  developer.
- Never force-add an artifact into version control and never suggest
  removing an existing ignore.
- Edit artifact files (progress ledgers, the domain glossary, ADRs) with
  the Edit tool, not shell one-liners — `sed -i`/`printf >>` commands
  with unique text never match a standing permission rule and prompt on
  every call.
- Per-work artifacts (review reports, ADRs, task briefs, progress
  ledgers) carry a `ticket` frontmatter field; registry files that live
  across tickets (the domain glossary, `.gitignore` files, and — when the
  project-memory plugin's rules are installed — Project memory notes and
  the store's registry files, whose list that plugin's conventions rule
  owns) are exempt. Project-memory idea entries DO carry `ticket`
  and are not exempt. Team memory (`docs/memory/`) is a Process
  directory; Private memory (`.claude/memory/`) is not — it is the
  per-user store defined by the project-memory plugin's rules.
  Reuse the ticket already established for the current work; value format
  in the ticket-frontmatter rule.
