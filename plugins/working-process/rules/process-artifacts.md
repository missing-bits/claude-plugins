---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
  - "docs/domain/**"
  - ".superpowers/**"
---

# Process directories and artifacts

A Process directory is a directory the working process creates in a
project repo to hold work artifacts: `docs/specs/`, `docs/plans/`,
`docs/domain/`, and the `.superpowers/` family at the repo root.

## First-create question

When creating a Process directory — or touching one that already exists
with no observable prior decision (neither a `.gitignore` containing `*`
nor any git-tracked file under it) — ASK the developer which mode the
directory gets. Assume no default:

- **Ignored mode**: write a `.gitignore` containing exactly `*` into the
  directory; its contents stay out of the repo.
- **Tracked mode**: no `.gitignore`; artifacts are committed like any
  other file.

Never ask when either signal is already present: a `.gitignore` with `*`
means ignored mode was chosen; a git-tracked file under the directory
(`git ls-files <dir>` non-empty) means tracked mode was chosen.

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
  across tickets (the domain glossary, `.gitignore` files) are exempt.
  Reuse the ticket already established for the current work; value format
  in the ticket-frontmatter rule.
