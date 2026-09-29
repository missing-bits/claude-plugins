---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
  - "docs/technical-designs/**"
  - "docs/domain/**"
  - "docs/code-review/**"
  - ".superpowers/**"
---

# Process directories and artifacts

A Process directory is a directory the working process creates in a
project repo to hold work artifacts: `docs/specs/`,
`docs/technical-designs/`, `docs/plans/`, `docs/domain/`,
`docs/code-review/`, `docs/memory/` (Team memory — when the
project-memory plugin's rules are installed), and the `.superpowers/` family
at the repo root.

## First-create question

When creating a Process directory — or touching one that already exists
with no prior decision (no `.gitignore` containing exactly `*`, no
git-tracked file under it, no settings key deciding it, and no explicit
project instruction declaring the mode) — ASK the developer which mode
the directory gets. Assume no default:

- **Ignored mode**: write a `.gitignore` containing exactly `*` into the
  directory; its contents stay out of the repo.
- **Tracked mode**: artifacts are committed like any other file; no
  `.gitignore` is written at first-create (a narrower one added later —
  e.g. the local pocket of `docs/code-review/` — does not change the
  mode).

Never ask when any signal is already present. Two signals are visible:
only a `.gitignore` containing exactly `*` means ignored mode was
chosen — one with any other content (e.g. a local pocket's `local-*`)
signals nothing by itself — and a git-tracked file under the directory
(`git ls-files <dir>` non-empty) means tracked mode was chosen. The
third is declared: the directory's settings key, read as the
process-settings rule says — `dir.default`, unless an exception names
the directory: `dir.docs/specs`, `dir.docs/technical-designs`,
`dir.docs/plans`, `dir.docs/domain`, `dir.docs/code-review` or
`dir..superpowers`, which covers the whole `.superpowers/` family. The
block lists each exception's effective value, an absent exception
inheriting `dir.default`; an invalid one is unset and never inherits.
Until a project migrates to the key, an explicit project instruction
declaring the mode (e.g. a CLAUDE.md note that a directory is always
git-ignored) declares it too, the key winning where the two disagree.
At the first touch of a directory, in this order:

1. a visible signal that agrees with the key, or stands where no key
   is set, governs;
2. a visible signal that contradicts the key is reported, and the
   developer asked which stands; nothing is changed until they answer;
3. a key with no visible signal is applied without asking — the ignored
   mode by writing the `*` `.gitignore`; the tracked mode needs no act
   and becomes visible with the first committed file. A step keyed to
   a resolved mode rather than to the question — the local pocket of
   `docs/code-review/` — fires whichever way the mode was settled;
4. with neither, ASK, as above. The answers include "tracked, and
   record" and "ignored, and record", which write the exception for the
   directory asked about — never `dir.default`, which only the
   `process-setup` skill writes — through the loader's `--set` where a
   settings block names the loader.

A declared ignored mode is materialized by whoever first acts on it —
writing the `*` `.gitignore` — making the decision observable; a
declared tracked mode becomes observable with the first committed
file. This rule owns the signal list; other surfaces reference it
rather than restating it (the self-contained restatements of the review commands
and the project-memory core rule are the justified exceptions).
`.working-process/`, the settings directory, is not a Process
directory: it is configuration, never asked about.

`docs/memory/`'s tracked/ignored first-create question is asked by the
project-memory plugin's core rule (when installed), not this one, and
that rule reads its own exception, `dir.docs/memory`, in the same
order — it is listed above only so `docs/memory/` counts as a Process
directory for the conventions below.

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
