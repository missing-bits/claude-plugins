# Process settings

Standing answers — a directory's mode, the review loop's autonomy, the
technical-design offer — live in two files at the repository root, in
`.working-process/`: `settings.md`, the team's answers, committed like
any other file; and `settings.local.md`, one person's answers, kept
out of git by `.working-process/.gitignore`, which holds the line
`settings.local.md`. `.working-process/` is not
`.claude/working-process/`, the per-checkout dispatch-record store, and
it is not a Process directory: its team file is committed by
definition and its local file ignored by its own `.gitignore`, so it is
never asked about.

## The grammar

A settings line is `key: value` at the start of a line, outside a
fenced block: a lower-case dotted key — a first segment of letters,
digits and `-`, a dot, then letters, digits, `-`, `/` and `.` — a
colon, and a plain token of letters, digits, `.`, `_`, `/` and `-`,
with no quotes. Fences open and close on lines starting with three
backticks. Every line shaped like a key is a settings line and is
validated; an invalid value is diagnosed, never read past. Every other
line is commentary, leading whitespace included. The plugin's key
registry defines every key — its name, scope, allowed values, default,
readers and question — and nothing else does; a key is never renamed.

## Scope

Every key is a team key, read from the team file alone, or a personal
key, read from the personal file alone. A personal key in the team file
is a suggestion: it proposes a default answer and grants nothing. An
invalid or duplicated value in the deciding file makes the key unset;
it never lets a value from another file through. In a worktree without
a personal file, the main checkout's is read; a personal file made by
hand in a worktree replaces that wholly, and the block's first line
says which was read; a bare repository's worktree has no fallback.

## The block

At every session start — startup, resume, clear and compaction alike —
the plugin's loader emits one block as context. Its first line names
the block, the repository root, the loader's own path and the two
files read:

```
working-process settings (root: <path>; loader: <path>; team: settings.md; local: settings.local.md)
dir.default: tracked  [team]
dir.docs/specs: tracked  [inherited]
review.autonomy: yes  [local]
consult.personas: unset  [team suggests: yes]
docs-branch.merge: unset  [invalid in team]
error: settings.md:14 unknown key `review.autonmy` — ignored
```

Every registered key is listed, set or `unset`, with one source:
`[team]`, `[local]`, `[default]`, `[inherited]` — a directory
exception taking `dir.default` — `[team suggests: <value>]` beside
`unset`, or `[invalid in team]` and `[invalid in local]` beside
`unset`, a duplicate included. Errors follow as `error:` lines. A
block cut at the hook's 4 KB cap ends with
`incomplete: run <loader> --print`.

## Reading a key

1. Where no `.working-process/` directory exists — not in this
   checkout and, in a worktree, not in the main checkout either — every
   key is unset and nothing is run.
2. Otherwise take the key's value from the block in context; complete
   an incomplete block by running `--print` through the loader path the
   block's first line names.
3. With no block at all — hooks disabled, a plugin not yet trusted, a
   machine without the plugin — every key is unset. Never resolve the
   files by hand: without the registry a session cannot know a key's
   scope, and a team suggestion could be read as consent.
4. An unset key means the rule's behaviour before the key existed: the
   question is asked, or the offer made, as that rule says.

An answer given in the current session outranks the settings,
compaction included. Background agents — the verdict agents, the
auditors, the consult agents — never read settings: the dispatcher
resolves every key it acts on and carries the result in its brief. A
`CLAUDE.md` note that declares a key's value binds until it is
migrated; where the note and the settings disagree, the settings win
and the session says which note it overrode.

## When a write happens

A standing question asked in ordinary work offers "<answer>, and
record" beside its answers wherever the block in context names the
loader; choosing it runs `<loader> --set <key> <value>`, which writes
the key to the file its scope names — a personal key to the main
checkout's file from a worktree — creates the `.gitignore` beside a
personal file, and prints the fresh block, which supersedes the old
one for the rest of the session. A directory's first-create question
records that directory's own exception, never `dir.default`. The
`process-setup` skill, when available, collects every unset key in one
sitting and migrates `CLAUDE.md` notes. Where no block names the
loader, the option is withheld: the answer holds for the session, and
the session says it was not recorded. Nothing writes a settings file
directly; a team's suggestion for a personal key is the one
hand-written line. How a write happens — destination, insertion,
replacement, duplicates, validation — is the loader's alone.
