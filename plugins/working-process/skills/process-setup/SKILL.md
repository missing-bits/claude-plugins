---
name: process-setup
description: "Collect a project's standing process answers in one sitting — show the effective settings, ask about the unset keys, migrate CLAUDE.md notes, and record every answer through the settings loader. Use ONLY when the developer explicitly asks to set up or change the process settings (\"process setup\", \"set up the process settings\", \"ustaw ustawienia procesu\"). A single question answered in ordinary work records itself through its own \"and record\" option and is not a trigger."
---

# process-setup — one sitting for the standing answers

The loader is `${CLAUDE_PLUGIN_ROOT}/scripts/load-settings.sh`; the
registry beside it, `${CLAUDE_PLUGIN_ROOT}/SETTINGS_REGISTRY.md`, holds
every key's scope, values, default and question. Invoke the loader with
its absolute path as the first token of the command, so the
developer's prefix-matching permission rules apply. Never write a
settings file directly: every write is a `--set`.

## 1. Show the effective settings

Run `<loader> --print` from the repository root and show its block as
one table — key, value, source — with the first line's root and files
above it. Where the line says `no settings directory` — no
`.working-process/` in this checkout or, in a worktree, in the main
checkout — this is the first run: nothing is recorded yet, the hook
has been silent, and this skill makes the first write; `--set` creates
the directory. In a worktree whose own checkout has no
`.working-process/`, the block still lists the main checkout's
personal answers, with `team: settings.md (absent)`: team keys are
unset here until a team answer is written, which creates the
worktree's own `settings.md`.

On the first run — no settings file exists yet — gather the candidates
and show them beside the table, each to confirm:

- **Directory signals**, mechanical and shown as settled: for every
  Process directory the process-artifacts rule names that exists —
  `docs/specs/`, `docs/technical-designs/`, `docs/plans/`,
  `docs/domain/`, `docs/code-review/`, `.superpowers/`, and
  `docs/memory/` where the project-memory plugin is installed — read
  its mode: a `.gitignore` containing exactly `*` is ignored, a
  git-tracked file (`git ls-files <dir>` non-empty) is tracked, neither
  is undecided. Offer `dir.default` as the mode most decided
  directories carry, and each decided directory in the other mode as
  an exception (`dir.docs/plans: tracked`, say). A tie, or no decided
  directory: no candidate, and `dir.default` is asked like any unset
  key.
- **Prose notes**, the model's reading, never certain: read `CLAUDE.md`
  at the repository root and in `.claude/`, and any file such a note
  points at, for a sentence that settles a key — the technical-design
  offer declined, the `.docs` branch merge fixed, a directory declared
  always ignored. Offer each as `<key>: <value>`, quoting the sentence
  and its file, for the developer to confirm or reject.

The project-memory plugin counts as installed where a
`project-memory.md` rule is found under `<project>/.claude/rules/` or
`$HOME/.claude/rules/`.

## 2. Ask about what is unset

Ask about the unset keys only, one at a time, in the registry's order,
each with the registry's question, a recommendation, and the file the
answer goes to: a team key to `.working-process/settings.md`, a
personal key to `.working-process/settings.local.md` — in a worktree,
the main checkout's, and the preview in step 3 says so. A key whose
line reads `[team suggests: <value>]` is asked with that value as the
default answer. Skip `dir.docs/memory` where the project-memory plugin
is not installed. Directory exceptions are optional answers, not unset
ones: ask `dir.default`, then offer exceptions only when the developer
asks for them, `dir.docs/memory` among them. A candidate from step 1
the developer confirmed is an answer and is not asked again.

A team's suggestion for a personal key is the one line `--set` never
writes: where the developer wants one, say that it goes into
`settings.md` by hand, and that
`<loader> --validate --scope team .working-process/settings.md`
passes it with a notice.

## 3. Preview, then write

For each answer run `<loader> --set --dry-run <key> <value>` and show
what it prints: the file, the line it would insert or replace, the
duplicate lines it would remove, the `.gitignore` it would create, and
the note where a hand-made worktree file shadows the destination —
then `<loader> --set <key> <value>`. Where the preview shows lines a
duplicate would lose, show them before applying. Where `--set` exits
non-zero, show its message and stop for that key. The fresh block
`--set` prints supersedes the one from session start for the rest of
the session; read keys from it. In a bare repository's worktree the
loader has no main checkout: say plainly that a personal answer binds
this worktree only.

## 4. Materialize the declared modes

For each Process directory that already exists: where its key resolves
to ignored and the directory carries no visible signal, write the `*`
`.gitignore`; where it resolves to tracked, do nothing — the first
committed file makes it visible. Create no directory. Where a visible
signal contradicts the key, ask which stands: the signal — record the
matching value with `--set`; the key — say what the developer must do
by hand, since this skill never untracks or force-adds a file.

## 5. Migration and the reminder

A confirmed prose note is a `--set` like any answer; after it, offer to
remove the note that now duplicates the key, and never delete one
without consent. Until it is removed the note still binds, and where it
and the key disagree the key wins. Close by reminding the developer
that `.working-process/settings.md` and `.working-process/.gitignore`
belong in the work's commit, in the checkout they were written in; this
skill never commits.

A second run shows the same table and asks only about what is unset or
what the developer wants to change; it never replays the whole
questionnaire.
