---
ticket: none
date: 2026-09-28
status: draft
grilled: 2026-09-28
architect: concerns (resolved 2026-09-28)
decisions: registered
branch: feature/process-setup
base: develop
---

# process-setup — one sitting for a project's standing process answers

The working-process rules ask the same standing questions again and
again: whether a Process directory is tracked, whether the review loop
may run on its own, whether a technical design is offered. Each answer
is a stable property of a project or a person, yet most have no place
to live, so every fresh context asks again. This spec gives those
answers one home, `.working-process/`, loads them at every session start
through the plugin's own hook, and adds a `process-setup` skill that
collects them in one sitting. The rules then read a named key instead of
"the developer's own instructions".

## Problem

An inventory of the shipped plugins found 39 sites that ask or read a
standing answer. Most already have a visible home — a frontmatter stamp,
a manifest, a heading annotation. These do not; each asks a question
with no named place to record the answer:

- persona consultation consent, asked once per conversation;
- review-loop autonomy with per-round commits as its second clause,
  asked once per session;
- fast-forward or squash of the `.docs` branch, asked at every
  implementation-ready gate unless a `CLAUDE.md` note exists;
- the technical-design offer, re-offered at every consumption gate
  unless a `CLAUDE.md` declaration exists;
- the tracked or ignored mode of each Process directory — one question
  asked separately for `docs/specs/`, `docs/technical-designs/`,
  `docs/plans/`, `docs/domain/`, `docs/code-review/`, `docs/memory/` and
  the `.superpowers/` family.

Where the rules name a home at all, they name prose: "a durable
preference belongs in the developer's own instructions", or "a
`CLAUDE.md` note". Neither gives a line format a rule could find, and
neither separates what a team decides from what a person consents to.
Each fresh context therefore re-derives or re-asks, and each question
spends an interruption the review loop is otherwise careful with.

The inventory is kept with this spec's working records; its sources are
the rule files named in *Changes by file*.

## Decisions

- **D1** — Standing answers live in `.working-process/settings.md`
  (team, committed) and `.working-process/settings.local.md` (personal,
  git-ignored), at the repository root. Neither `CLAUDE.md` nor
  `AGENTS.md` carries them. Argued in *The settings files*.
- **D2** — Both files use one grammar: a `key: value` line at the start
  of a line, outside a fenced block; a key contains a dot; a value is a
  plain token; every other line is commentary. Argued in *The settings
  files*.
- **D3** — Every key has one scope, team or personal, fixed by the
  registry. A team key is read from the team file only; a personal key
  from the personal file only. A personal key in the team file is a
  suggestion — it proposes a default answer and never grants consent.
  Argued in *Scope and precedence*.
- **D4** — An invalid or duplicated value in the file that decides a key
  makes the key unset; it never exposes a value from another file.
  Argued in *Scope and precedence*.
- **D5** — In a worktree with no personal file, the loader reads the
  main checkout's personal file, found as the first entry of
  `git worktree list --porcelain`. A personal file created by hand in a
  worktree replaces that fallback wholly, and the loader says so.
  Argued in *Scope and precedence*.
- **D6** — One key registry in the plugin defines every key: name,
  scope, allowed values, default, the rule that reads it, and the
  question the skill asks. The skill, the loader and the rules keep no
  second definition of a key. Argued in *The key registry*.
- **D7** — The version-one keys. Argued in *The keys*.
  - **D7.1** — `dir.default`: `tracked` | `ignored`, team.
  - **D7.2** — `dir.docs/specs`: `tracked` | `ignored`, team, an
    optional exception to `dir.default`.
  - **D7.3** — `design.technical-design-offer`: `on` | `off`, team.
  - **D7.4** — `dispatch.propagation-auditor-tier`: `cheapest` |
    `mid` | `most-capable`, team; default `cheapest`.
  - **D7.5** — `docs-branch.merge`: `squash` | `fast-forward`, team.
  - **D7.6** — `consult.personas`: `yes` | `no`, personal.
  - **D7.7** — `review.autonomy`: `yes` | `no`, personal.
  - **D7.8** — `review.per-round-commit`: `yes` | `no`, personal.
  - **D7.9** — `dir.docs/technical-designs`, as D7.2.
  - **D7.10** — `dir.docs/plans`, as D7.2.
  - **D7.11** — `dir.docs/domain`, as D7.2.
  - **D7.12** — `dir.docs/code-review`, as D7.2.
  - **D7.13** — `dir..superpowers`, as D7.2.
  - **D7.14** — `dir.docs/memory`, as D7.2; always registered, asked
    and read only as D25 says.
- **D8** — Keys are never renamed. How a retired key is marked, and how
  the loader reports one, is settled with the first key actually
  retired. Argued in *The key registry*.
- **D9** — A SessionStart hook runs a loader that emits the effective
  value and source of every registered key, plus warnings, as plain
  standard output, which both hosts add to the session's context.
  Argued in *The loader*.
- **D10** — The loader stays silent when `.working-process/` does not
  exist, exits 0 on any error of its own, and caps its output at 4 KB,
  saying so when it truncates. Argued in *The loader*.
- **D11** — The loader is its own hook handler, registered without a
  matcher so it also runs on resume and compaction; it finds the
  registry relative to its own path and uses POSIX `sh`, `sed` and
  `awk`. Argued in *The loader*.
- **D12** — A new always-on rule, `process-settings.md`, defines the
  files, the grammar, the block, the three-step read, and when a write
  happens; how a write happens belongs to the loader (D43), and the
  full by-hand resolution to a second rule, `process-settings-resolution.md`,
  path-scoped to `.working-process/**` so it loads only when a session
  reads the settings by hand; `process-settings.md` names it and tells
  the by-hand path to open it first. Argued in *Reading a key*.
- **D13** — A rule reads a key from the block in its context; without
  a trustworthy block, by the procedure D38 names; an unset key means
  the rule's behaviour before this change. Argued in *Reading a key*.
- **D14** — An answer given in the current session outranks the
  settings, compaction included. Argued in *Reading a key*.
- **D15** — Background agents never read settings; the dispatcher
  resolves every key it acts on. Argued in *Reading a key*.
- **D16** — Each site that asks a standing question today names its key
  and its behaviour when the key is unset, replacing "the developer's
  own instructions". Argued in *Changes to the rules*.
- **D17** — A settings key becomes a declared signal for a Process
  directory. At the first touch of a directory: a visible signal that
  agrees with the key, or stands where no key is set, governs; one
  contradicting the key is reported and the
  developer asked, with nothing changed; a key without a visible signal
  is applied unasked; with neither, the rule asks. Argued in *Directory
  modes*.
- **D18** — `.working-process/` is not a Process directory: it is never
  asked about, and the rule says so. Argued in *Directory modes*.
- **D19** — When a standing question is asked in ordinary work, its
  answers include "yes, and record", which writes the answer, through
  the loader's `--set`, to the file its scope names. There is no separate "record it?" question.
  Anyone may record a team key this way; the write names the team file.
  Argued in *Recording an answer*.
- **D20** — A `CLAUDE.md` note that declares a key's value keeps binding
  until it is migrated; where it and a settings value disagree, the
  settings value wins and the session says so. Argued in *Migration*.
- **D21** — The `process-setup` skill runs only on request. It shows
  the effective settings, asks about unset keys other than optional
  directory exceptions (D39), previews its changes, and writes by the
  rules D37 names. Argued in *The skill*.
- **D22** — The skill materializes a declared mode only in a Process
  directory that already exists and does not contradict it; it creates
  no directory. Argued in *The skill*.
- **D23** — On its first run the skill offers existing declarations and
  signals as candidates: directory signals as certain, prose notes in
  `CLAUDE.md` as the model's reading, to be confirmed. It never deletes
  a `CLAUDE.md` note without consent. Argued in *Migration*.
- **D24** — The first personal answer written creates
  `.working-process/.gitignore` holding the single line
  `settings.local.md`, beside the personal file; the loader's `--set`
  writes it (D43). Argued in *The loader*.
- **D25** — The skill asks about `dir.docs/memory` only when the
  project-memory plugin is installed, and the project-memory rule reads
  that key only when the working-process rules are installed. Argued in
  *The keys*.
- **D26** — Version one reads the working-process registry alone; no
  domain registry is read or discovered. Argued in *Out of scope*.
- **D27** — A repository test checks that every registered key is cited
  by the rule its entry names, that every key reference under the
  `rules/`, `skills/`, `agents/` and `commands/` of working-process,
  project-memory, python-standards and salesforce-standards is
  registered, that defaults validate, and that names are unique. Argued in *Verification*.
- **D28** — Repository tests run the loader on fixtures for
  precedence, suggestions, invalid and duplicate values, unknown keys,
  the worktree fallback, the size cap, silence and error exit, and
  `--set`'s insert, replace, duplicate report, destination and
  `.gitignore`, and `--set --dry-run` writing nothing. Argued in
  *Verification*.
- **D29** — A Claude Code dogfood run proves the block reaches a new
  session, a recorded question is not asked, and the block returns after
  compaction. Argued in *Verification*.
- **D30** — A Codex run proves the same loader delivers its block
  through a repository-level Codex hook, after trust and after
  compaction or resume. Argued in *Verification*.
- **D31** — The glossary's **First-create question** entry gains the
  settings key as a signal. Argued in *Changes by file*.
- **D32** — An absent `dir.<path>` exception inherits `dir.default`; an
  invalid one is unset and the rule asks, never inheriting. Argued in
  *The keys*.
- **D33** — The loader finds the repository root through
  `git rev-parse --show-toplevel`, then `CLAUDE_PROJECT_DIR`, then the
  working directory. Argued in *The loader*.
- **D34** — The loader offers `--print`, which emits the block to
  standard output, and `--validate --scope team|personal <file>`, which
  exits non-zero with its warnings when the file would not validate.
  Argued in *The loader*.
- **D35** — The propagation-auditor card stops prescribing the cheapest
  family and accepts the tier the dispatcher resolved from
  `dispatch.propagation-auditor-tier`, whose default stays `cheapest`;
  it still reports its family for the dispatcher's comparison. Argued in
  *Reading a key*.
- **D36** — Every line shaped like a key — a dotted name and a colon at
  the start of a line, outside a fence — is a settings line, validated,
  and diagnosed when its value is invalid; it is never commentary.
  Argued in *The settings files*.
- **D37** — A write inserts an absent key, replaces a present one, and
  on a duplicate replaces every line for the key with the value it
  writes and reports the lines it removed — the fresh answer is the
  resolution; after writing, it prints the fresh block, which
  supersedes the old one for the rest of the session. Argued in *The
  loader*.
- **D38** — Without a trustworthy block — none, or one marked
  incomplete — a session resolves keys by the loader's own procedure,
  through `--print` or, where the script is unreachable, by the full
  resolution in `process-settings-resolution.md`. Argued in *Reading a
  key*.
- **D39** — The skill asks about directory exceptions only when the
  developer asks for them. Argued in *The skill*.
- **D40** — The python and salesforce review commands and the
  project-memory rule, which restate the first-create predicate, adopt
  the settings key and its conflict question. Argued in *Changes to the
  rules*.
- **D41** — Personal answers are written where the loader reads them:
  in a worktree, to the main checkout's personal file, with its
  `.gitignore` beside it — for a skill write and a "yes, and record"
  answer alike. Where a hand-made worktree file shadows that
  destination, the preview says the write will not change the current
  worktree's answer. In a bare repository with linked worktrees there
  is no main checkout: the loader has no fallback and says so, and
  personal answers go to the current worktree's file, binding that
  worktree only, as the skill says. Argued in *Scope and precedence*.
- **D42** — `--print` is uncapped; only the hook's output carries the
  4 KB cap. Argued in *The loader*.
- **D43** — The loader owns every write of an answer through
  `--set <key> <value>`, the registry choosing the file by the key's
  scope: the destination (D41),
  the `.gitignore` beside a personal file, insertion, replacement and
  duplicate detection (D37), validation, and the fresh block printed on
  success, validating before it writes; `--set --dry-run` computes the
  same write and applies nothing, which the skill's preview uses. The
  skill, a "yes, and record" answer and migration all call it; none
  writes a settings file directly; the one hand-written line is a team's
  suggestion for a personal key, which `--validate --scope team`
  warns about and still passes. Argued in *The loader*.

## The settings files

Two files at the repository root, in a directory named for the plugin
rather than for any tool, since the plugin will also run natively in
Codex:

- `.working-process/settings.md` — the team's answers; committed like
  any other project file.
- `.working-process/settings.local.md` — one person's answers; kept out
  of git by `.working-process/.gitignore`, which holds the single line
  `settings.local.md`. The directory ignores its own local file, so the
  repository's root `.gitignore` is never touched.

Keeping the answers out of `CLAUDE.md` and `AGENTS.md` does three
things: the plugin loads them without depending on import support
(Codex documents none), a project's shared instructions stay free of
process machinery, and the answers fit a format a script can resolve.

A settings line is a `key: value` pair at the start of a line and
outside a fenced block. A key holds a dot — `review.autonomy`,
`dir.docs/specs` — so a line of prose such as `Note: see below` never
reads as a key. A value is a plain token: letters, digits, `.`, `_`,
`/` and `-`, with no quotes.

Recognizing a settings line and validating it are separate steps. Every
line shaped like a key — a dotted name and a colon at the start of a
line, outside a fence — is a settings line, whatever follows the colon,
and a value that is not a valid token for that key is diagnosed rather
than read past. So `review.autonomy: "no"` below `review.autonomy: yes`
is a duplicate, and the key is unset; it cannot hide as commentary and
leave the earlier consent standing. Fences open and close on lines
starting with three backticks; leading whitespace makes a line
commentary. Every other line is commentary, and `--set` writes each
key's question as a comment line above it, so the file explains itself. The
grammar follows the one precedent in the marketplace, the
`trigger-framework:` declaration of salesforce-standards: one line, one
key, found by a line-anchored match.

## Scope and precedence

Each key has one scope, and the scope decides which file is read:

| Key scope | Decided by | Ignored, with a warning |
|---|---|---|
| team | the team file, then the registry default | a line in the personal file |
| personal | the personal file, then the registry default | a line in the team file, shown as a suggestion |

A team can say that it would like personas consulted, but only each
person's own file grants that consent. A personal key in the team file
therefore surfaces as `unset [team suggests: yes]`, and the question for
that key offers the suggestion as its default answer.

An invalid value or a duplicated key in the deciding file leaves the key
unset, with a warning. It never lets a value from elsewhere through. The
failure this rules out is a mistyped `review.autonomy: noo` in a
personal file letting a team suggestion stand in for consent.

A worktree is a separate checkout, and an ignored file does not follow
into it. Where a worktree has no personal file of its own, the loader
reads the main checkout's, whose path is the first entry of
`git worktree list --porcelain` wherever the worktree lives. (The
parent of `git rev-parse --git-common-dir` is not a checkout path in
every layout, so it is not used.) One set of personal answers then
serves every worktree of a repository. A personal answer is written
where the loader reads it: `--set`, called from a worktree by the skill
or by a "yes, and record" answer alike, writes to the main checkout's
personal file and puts the `.gitignore` beside it, so a worktree never
gains a file of its own through a write. A personal file created in a
worktree by hand replaces the fallback wholly — no per-key merge — and
the loader's first line says which file it read; a write made from that
worktree still goes to the main checkout, and its preview says it will
not change the current worktree's answer.

A bare repository with linked worktrees has no main checkout: the first
porcelain entry is the bare repository itself, marked `bare`. There the
loader has no fallback and its first line says so, and a personal answer
goes to the current worktree's own file, with the skill saying plainly
that it binds that worktree only. Nothing is ever written inside the
bare repository.

A home-level file of personal defaults for every project is out of
version one.

## The key registry

One file in the plugin defines every key. Each entry carries the key's
name, its scope, its allowed values, its default (a value, or `unset`
where the rule asks), the rule file that reads it, and the question the
skill asks. The shape is fixed, one field per line under a heading
naming the key, so that the loader's `sed` and the repository test both
parse it without a Markdown parser — the same discipline the rules
manifest follows.

The skill takes its questions from the registry, the loader takes its
validation from it, and the rules name keys and nothing more; no second
definition of a key exists to drift. A key is never renamed: renaming would
silently orphan every file that set it. Version one retires no key, so
the marker for a retired one and the loader's report of it wait for the
first key that is retired. The registry's exact path and heading shape are the
plan's to fix.

## The keys

Version one registers the keys whose question has no home today:

| Key | Scope | Values | Unset means | Read by |
|---|---|---|---|---|
| `dir.default` | team | `tracked` \| `ignored` | ask at first create | process-artifacts |
| `dir.<path>` | team | `tracked` \| `ignored` | absent: `dir.default` applies; invalid: ask | process-artifacts |
| `design.technical-design-offer` | team | `on` \| `off` | today's manifest-raised offer | workflow |
| `dispatch.propagation-auditor-tier` | team | `cheapest` \| `mid` \| `most-capable` | `cheapest` | workflow |
| `docs-branch.merge` | team | `squash` \| `fast-forward` | ask at the gate | spec-plan-lifecycle |
| `consult.personas` | personal | `yes` \| `no` | ask once per conversation | workflow |
| `review.autonomy` | personal | `yes` \| `no` | ask at the first verdict dispatch | workflow |
| `review.per-round-commit` | personal | `yes` \| `no` | ask with the autonomy question | workflow, spec-plan-lifecycle |

The `dir.<path>` exceptions exist for `docs/specs`,
`docs/technical-designs`, `docs/plans`, `docs/domain`,
`docs/code-review`, `.superpowers` and `docs/memory`. One default with
exceptions collapses what is today one question asked separately for
each directory into one question with rare exceptions. An exception has
three states. Absent, it inherits `dir.default`. Valid, it decides its
directory. Invalid, it is unset — the rule asks at that directory's
first create, and it does not inherit, for the reason D4 gives: an
error never lets another source's value through, and a directory's mode
decides what enters the repository. `docs/memory` is
the project-memory plugin's directory: the skill asks about it only
where that plugin is installed, and the project-memory rule reads the
key only where the working-process rules are installed, the pattern its
rule already uses for Process directories.

A key is `dir.` followed by the path exactly, so the `.superpowers`
exception is `dir..superpowers`; the double dot is the price of one
mapping with no special case for paths that start with a dot.

`design.technical-design-offer: on` makes the offer at every
consumption gate whether or not a toolchain manifest is present — the
declaration the workflow rule already honours — while an unset key
leaves today's behaviour, where only a manifest raises the offer; `off`
suppresses it.

The gate's value is a tier in the glossary's sense — a relative rung,
never a model name. `mid` is the glossary's own word for its rung, and
`most-capable` shortens the glossary's "most capable available";
`cheapest` is the workflow rule's, which prescribes "the cheapest
available family" for this agent today. Each host resolves the tier at dispatch through a table
of its own; version one ships only Claude Code's (Haiku for `cheapest`,
the family one below the most capable for `mid`, the most capable
available for `most-capable`). A Codex port adds its table; Codex's
current ladder has three rungs, which fit the three values, and its
separate reasoning-effort setting is the port's concern, not a
settings value. Consent values are `yes` and `no` alone. A
session-scoped answer — "not now", "not in this session" — is never a
key, because it dies with the session by definition.

Deliberately not keys in version one: process weight, whose readers do
not exist yet; the rules install level and commit mode, whose answer
the rules manifest's position already records; the review loop's round
cap, which stays fixed by the rule — making it a key would change the
rule's behaviour, not only where an answer is recorded, and unlike the
gate's tier (*Reading a key*) no evidence argues for that change; and
every
per-document artifact (stamps, chain debt, `ticket:`), which has its
own home.

## The loader

A script shipped with the plugin, registered as a second SessionStart
handler beside the rules-drift check. It reads the two settings files,
applies scope and precedence against the registry, and emits one block
as the hook's additional context:

```
working-process settings (root: <path>; team: settings.md; local: settings.local.md)
dir.default: tracked  [team]
review.autonomy: yes  [local]
consult.personas: unset  [team suggests: yes]
warning: settings.md:14 unknown key `review.autonmy` — ignored
```

The first line names the block, so a reader can find it among other
hooks' context, whose order is undocumented, and understand it without
the rule. Every registered key is listed, set or not, so a rule has one
place to read and never needs the registry. Warnings live in the block,
because nobody reads a hook's stderr: unknown keys, invalid values,
duplicates, a key in the wrong scope's file.

The output is capped at 4 KB. That is a byte cap, not a token
guarantee: Codex's documented per-handler threshold is about 2,500
tokens, above which it stores the context on disk and shows a preview,
and 4 KB of ordinary output sits under it with room to spare. The
dogfood checks it rather than the spec promising it. Where the cap
truncates, the last line says the block is incomplete; it never
truncates silently. A block for the version-one keys runs to about
1 KB. The block is plain standard output, which Claude Code adds to a
SessionStart session's context and Codex adds as developer context; no
JSON envelope wraps it, so an arbitrary root path or warning needs no
escaping — the constraint the drift check lives under, whose messages
may carry no quotes or backslashes, never reaches the loader.

The loader stays silent — no output at all — when `.working-process/`
does not exist, so a project that never adopted the settings pays
nothing. An error of the loader's own ends in silence and exit 0, as
the drift check does, and the rule's fallback (*Reading a key*) covers
the missing block.

It finds the repository root through `git rev-parse --show-toplevel`,
then `CLAUDE_PROJECT_DIR`, then the working directory — in a worktree,
the worktree's own root — and the registry
relative to its own path rather than through `CLAUDE_PLUGIN_ROOT`, which
a Codex port may not provide. The git root comes first on purpose: the team file is a committed
property of the repository, so a project rooted below its git toplevel
still reads the settings at the git root. The drift check reads
`CLAUDE_PROJECT_DIR` first; the two hooks may differ there, and that
difference is deliberate. It is registered without a matcher, so it
runs on startup, resume, clear and compaction alike, and a compacted
conversation gets its settings back. It is its own handler rather than a
branch of the drift check, because Codex budgets context per handler.
It uses POSIX `sh`, `sed` and `awk`, all part of a POSIX base system,
and no `jq`: unlike the drift check, whose foreign-payload branch needs
`jq` and skips itself without it, the loader has no optional
dependency. Two modes serve the skill and the no-hook path:
`--print` emits the same block to standard output, uncapped — the 4 KB
cap guards the hook's context budget, and a skill or a session
recovering from a truncated block needs the whole of it — and
`--validate --scope team|personal <file>` checks a candidate file
against the scope it is meant for, printing its warnings and exiting
non-zero when the file would not validate. A warning alone fails
nothing: a personal key in the team file is reported as a suggestion
and the file still validates, which is the check a hand-written
suggestion gets. A third mode writes:
`--set <key> <value>` takes no scope argument — the registry fixes each
key's scope, so the file follows from the key — and resolves the
destination —
in a worktree the main checkout's personal file, in a bare-repository
worktree its own (*Scope and precedence*) — creates the file and, for a
personal file, the `.gitignore` beside it; inserts an absent key under
its question as a comment, replaces a present key's line in place, and
on a duplicate replaces every line for that key with the one it writes
and reports the lines it removed — the developer has just answered the
question the duplicate caused, so that answer resolves it without a
second question. The written line takes the first duplicate's place;
each later duplicate goes, with the question comment directly above
it, the one exception to leaving every other line untouched; validates the result against the key's registry scope
before anything is written, so no `--set` ever leaves
a file that would not validate; and on success prints the fresh
block. `--set --dry-run` resolves the same destination and prints what
the write would do — the file, the line it would insert or replace, the
duplicate lines it would remove, the `.gitignore` it would create, and
the shadow warning where a hand-made worktree file would hide the
result — and writes nothing. Every other
line and comment stays untouched, and an unchanged file is not
rewritten. Writing lives in one place because its destination logic is
exactly what drifts when three writers restate it. Only the hook mode
swallows its errors and exits 0; the other three report failure.

## Reading a key

A new always-on rule, `process-settings.md`, defines the files, their
grammar, the block, the three-step read below, and when a write
happens. The rules that read a key cite it and restate none of it. It
stays short because every session and every dispatched agent loads it:
the full by-hand resolution — needed only where no hook ran and the
loader cannot be reached — lives in a second rule of the payload,
`process-settings-resolution.md`, scoped by `paths:` to
`.working-process/**`. The Rules engine copies every rule file and
Claude Code loads a rule without `paths:` at every launch, so a file
merely "beside the rule" would be always-on; path-scoped, it loads
exactly when a session reads a settings file by hand, which is the
by-hand path and nothing else — the shape `process-artifacts.md`
already uses. The trigger is a file read through the Read tool, not a
`cat` in a shell, so `process-settings.md` also names the file and
tells a session on the by-hand path to open it before touching the
settings, and correctness does not depend on which tool reads them.
How a write happens belongs to the loader (*The loader*).

To read a key, a session:

1. takes its value from the settings block in its context, unless the
   block says it is incomplete;
2. without a trustworthy block — none arrived because hooks are
   disabled or a Codex plugin is not yet trusted, or the block says it
   is incomplete — resolves the key by the loader's own procedure:
   running `--print` where the script is reachable, otherwise following
   the full resolution — scope, the worktree fallback, defaults,
   duplicates and invalid values — in `process-settings-resolution.md`,
   never a shortcut through the files;
3. where the key is unset, behaves as the rule did before this change:
   the question is asked, or the offer made, exactly as today.

An answer given in the current session outranks the settings, so a
developer who says "not in this session" after the block granted
consent is not overruled by the next compaction. The rule's existing
clause for a compacted conversation whose consent state is unclear now
covers only such session answers; a recorded key is simply read again.

Background agents — the verdict agents, the auditors, the consult
agents — never read settings. Every version-one key is consumed by the
dispatcher: it picks the gate's model, decides the loop, makes the
offer, settles the directory. Nothing depends on a subagent-start hook.
One card changes all the same: the propagation auditor's states that it
runs on the cheapest family and treats an upward mismatch as a fault,
which would contradict a team that set a higher tier. It instead
accepts the tier its dispatcher resolved and still opens its report
with its family, so the dispatcher's comparison keeps working. The
card's argument for the cheap family — that its duties are procedural
— becomes the argument for the default, and the card says a project
may choose otherwise. Its second clause, that "an over-tier run does
this work casually badly — a false clean line would then feed the
integrity gate unnoticed", is struck: the evidence below records the
opposite, and a card keeping it would call the evidence-backed choice
the dangerous one.

This key does change the rule's behaviour where a project sets it,
which is the ground on which the round cap stays out of version one. It
enters anyway, on evidence rather than on "someone may want it": the
workflow rule already records that a report carrying hits beside
`CLEAN` "has happened more than once on the cheapest family", and a
measurement on 2026-09-28, over two states of another project's design
spec and technical design that a later integrity audit found defective,
had the cheapest family return `CLEAN` in all four of its runs, while
one tier up located real defects in every one of its runs. A project that
has seen that must be able to move its gate without editing the
plugin. The round cap has no such evidence behind it.

## Changes to the rules

Each site that asks a standing question today names its key and says
what happens when the key is unset. "The developer's own instructions"
in those sentences becomes the key:

- `workflow.md` — persona consultation (`consult.personas`), loop
  autonomy and per-round commits (`review.autonomy`,
  `review.per-round-commit`), the technical-design offer
  (`design.technical-design-offer`; the sentence that reads a
  declaration "until a standing home for a project's process answers
  exists" is rewritten to cite the key), and the propagation auditor's
  tier (`dispatch.propagation-auditor-tier`).
- `spec-plan-lifecycle.md` — the per-round commit consent
  (`review.per-round-commit`) and the fast-forward or squash of the
  `.docs` branch (`docs-branch.merge`).
- `process-artifacts.md` — the settings key joins the directory
  signals (*Directory modes*).
- `review-reports.md` and the grilling-session skill defer to
  `process-artifacts.md`'s signal list and gain nothing of their own.
- The python and salesforce review commands restate the predicate so
  each stands alone, and today skip the question whenever a visible
  signal exists. They adopt the settings key and D17's order, including
  the conflict question.
- `project-memory.md` — `dir.docs/memory` counts as the declared mode when
  the working-process rules are installed, and its "never ask when a
  prior decision is present" gains the conflict question: a visible
  signal that contradicts the key is reported and the developer asked.
- `agents/propagation-auditor.md` — the tier clause, as *Reading a key*
  says, including the struck over-tier sentence.

## Directory modes

`process-artifacts.md` today reads two visible signals — a
`.gitignore` holding exactly `*` means ignored, a git-tracked file means
tracked — and a declared instruction, "materialized by whoever first
acts on it". A settings key becomes that declared instruction's named
form. At the first touch of a Process directory:

1. a visible signal that agrees with the key, or stands where no key
   is set, governs;
2. a visible signal that contradicts the key is reported, and the
   developer asked which stands; nothing is changed until they answer;
3. a key with no visible signal is applied without asking — the ignored
   mode by writing the `*` `.gitignore`, the tracked mode by the first
   committed file;
4. with neither, the rule asks, as today.

`.working-process/` is not `.claude/working-process/`, the per-checkout
dispatch-record store; `process-settings.md` tells the two apart in one
sentence. `.working-process/` itself is configuration, not a Process
directory:
its team file is committed by definition and its local file ignored by
its own `.gitignore`. It is never asked about, and `process-artifacts.md`
says so, so it cannot become one more first-create question.

## Recording an answer

When a standing question is asked in ordinary work, its answers gain
one option: "yes, and record" (or "no, and record"). Choosing it runs
the loader's `--set`, which writes the answer to the file the key's
scope names and prints the fresh block. The rule decides when a write
happens; the loader decides how. There is no second question: the
developer is interrupted once, as the review loop's one-batch-per-round
contract intends. A session never records an answer the developer did
not choose to record. Where `--set` cannot run — the loader unreachable
on the no-hook path — the option is withheld: the answer holds for the
session, and the session says it was not recorded.

Anyone may record a team key this way, not only whoever ran the setup.
The team file is an ordinary committed file, so the change shows in the
diff and passes the same review as any other; the session says, when
it writes, that the answer lands in the team's file.

## Migration

Some projects already hold answers elsewhere: directory signals, a
`CLAUDE.md` note declining the technical-design offer, a note fixing the
squash choice. A `CLAUDE.md` note keeps binding until it is migrated.
Where a note and a settings value disagree, the settings value wins and
the session says which note it overrode.

On its first run the skill gathers the existing answers as candidates.
Directory signals are mechanical and shown as settled. Prose notes are
not parseable, so the skill offers its reading of each as the model's
reading, with the note's location, for the developer to confirm. It
never deletes a note without consent; a confirmed move is a `--set`,
and after it the skill offers
to remove the note that now duplicates the key.

## The skill

`process-setup` runs only when the developer asks for it; nothing
nudges them to run it. A run:

1. calls the loader's `--print` and shows the effective settings as one
   table — key, value, source — together with the first-run candidates
   (*Migration*);
2. asks only about unset keys, one at a time, with a recommendation,
   saying for each which file the answer goes to; a team suggestion is
   offered as the default answer to a personal key; project-memory's key
   is skipped where that plugin is not installed. Directory exceptions
   are not unset answers but optional ones: the skill asks
   `dir.default` and offers exceptions only when the developer asks for
   them;
3. previews each answer with `--set --dry-run`, which also shows the
   `.gitignore` it would create beside a personal file, then writes it
   with `--set`; where the preview shows a duplicate, the lines the
   write would remove are shown before it is applied. The fresh block
   `--set` prints supersedes the one from session start for the rest of the
   session;
4. materializes a declared mode in each Process directory that already
   exists and does not contradict it, and reports every contradiction;
   it creates no directory;

A team's suggestion for a personal key is the one settings line
`--set` never writes: it goes into the team file by hand, and the
loader shows it as a suggestion.

A second run shows the same table and asks only about what is unset or
what the developer wants to change. It never replays the whole
questionnaire.

## Verification

- **Consistency test** (repository, beside the decision-coverage
  tests): every registered key is cited by the rule its entry names;
  every key reference is registered, where a reference is a
  backticked token with a registered key's shape — a dotted name
  starting with one of the registry's prefixes — under the `rules/`,
  `skills/`, `agents/` and `commands/` of working-process,
  project-memory, python-standards and salesforce-standards, examples in
  fenced blocks excluded; every default validates; no name repeats.
- **Loader tests** on fixtures: team and personal precedence; a
  personal key in the team file shown as a suggestion; an invalid value
  in the deciding file leaving the key unset without exposing another
  file's value; a duplicate key leaving it unset; an unknown key warned
  about; the worktree fallback, on a real `git worktree` in a temporary
  directory; the 4 KB cap and its truncation line; silence without
  `.working-process/`; silence and exit 0 on an error of its own;
  `--set` inserting an absent key, replacing a present one, replacing
  a duplicated key's every line and reporting the removed ones,
  `--set --dry-run` printing the destination, the line, the lines a
  duplicate would lose, the `.gitignore` and the shadow warning while
  leaving every file byte-identical, writing a personal answer to the
  main checkout from a worktree with its `.gitignore`, and to the
  worktree's own file in a bare-repository layout.
- **Claude Code dogfood**, with the plugin loaded from the checkout: the
  skill records settings; a new session receives the block; a recorded
  question is not asked; after `/compact` the block is back. The run
  confirms that plain standard output reaches the session.
- **Codex check**: in a scratch project, a repository-level
  `.codex/hooks.json` runs the same loader; the block reaches the model
  once the hook is trusted, and again after compaction or resume. No
  Codex plugin packaging is involved.

## Out of scope

- Process weight — its own package, which adds the key together with the
  rules that read it.
- Home-level personal defaults shared by every project.
- Domain registries. A domain plugin may one day add its own registry,
  discovered the way the plan-adversary discovers `*-plan-review`
  skills; version one reads only the working-process registry, and no
  convention is fixed for the others yet. salesforce-standards'
  `trigger-framework:` and `vendor-paths:` declarations stay where they
  are.
- Keys for the rules install level and commit mode.
- A configurable round cap.
- Packaging working-process as a Codex plugin; the Codex check proves
  only the loader.

## Changes by file

- New: the `process-setup` skill; the key registry; the loader script
  with its `--print`, `--validate` and `--set` modes; the
  always-on `process-settings.md` rule and the path-scoped
  `process-settings-resolution.md` holding the full by-hand resolution; a second SessionStart handler in
  `hooks/hooks.json`.
- `rules/workflow.md`, `rules/spec-plan-lifecycle.md`,
  `rules/process-artifacts.md` — as *Changes to the rules* and
  *Directory modes* say.
- `agents/propagation-auditor.md` — the tier clause.
- `plugins/project-memory/rules/project-memory.md` — the conditional
  `dir.docs/memory` key and its conflict question.
- `plugins/python-standards/commands/python-review.md`,
  `plugins/salesforce-standards/commands/salesforce-review.md` — the
  restated first-create predicate.
- `docs/domain/glossary.md` — **First-create question** gains the
  settings key as a signal, through a grilling session on this spec.
- Tests under `tests/working-process/`.
- README and CHANGELOG entries under `## Unreleased` for working-process
  and project-memory; a `-dev` dogfood version.

## Open questions

None.

## Review rounds

### Loop closed — 2026-09-28

Resolved without a fresh architect round, on the developer's choice
after round 3's stop signal: round 3 returned three Minor findings, all
fixed under cited licenses (F14–F16 above), and the architect judged a
further round not worth its cost. The consumption gate's integrity
audit reads the whole document next.

### 2026-09-28 — architect, fable 5.1, concerns (round 3, diff-scoped)

- fixed 2026-09-28 — [Minor] F14: D43 stayed absolute after the F11 ruling made the suggestion hand-written, and `--validate` was not said to pass it; license: the round-2 F11 ruling; D43 covers every write of an answer and names the exception, *The loader* says a warning alone fails nothing
- fixed 2026-09-28 — [Minor] F15: a duplicate's rewrite had no stated shape; license: D37 and *The settings files* ("so the file explains itself"); the line takes the first duplicate's place, later duplicates go with their question comments
- fixed 2026-09-28 — [Minor] F16: the path-scoped rule loads on a Read, not a shell `cat`, and the pointer from `process-settings.md` was lost in the F8 rewrite; license: the round-2 F8 ruling; D12 and *Reading a key* restore the pointer
- signal 2026-09-28 — a further round would not earn its cost; land the three Minors and let the consumption-gate integrity audit read the whole

### 2026-09-28 — architect, fable 5.1, blocking (round 2, diff-scoped)

- fixed 2026-09-28 — [Important] F8: the reference file beside the rule would load at every launch; ruling: 2026-09-28; D12, D38, *Reading a key* and *Changes by file* make it `process-settings-resolution.md`, path-scoped to `.working-process/**`
- fixed 2026-09-28 — [Important] F9: a refused duplicate left the resolving write unowned and forced a second question; ruling: 2026-09-28; D37, *The loader*, *The skill* and the loader tests: `--set` replaces every line for the key and reports the removed ones
- fixed 2026-09-28 — [Important] F10: the skill's preview needed the write's destination logic, which only `--set` holds; license: D21 and D43 ("none writes a settings file directly"); `--set --dry-run` added to *The loader* and D43, *The skill* step 3 previews through it, step 5 folded in
- fixed 2026-09-28 — [Minor] F11: `--set --scope` duplicated the registry's scope; ruling: 2026-09-28; `--set <key> <value>` takes no scope, the registry picks the file, and a team suggestion for a personal key is written by hand (*The skill*)
- fixed 2026-09-28 — [Minor] F11 (part): validation order unstated; license: D43 ("validation"); `--set` validates before anything is written
- fixed 2026-09-28 — [Minor] F12: the card's over-tier clause survived into the default's argument though the spec's own evidence contradicts it; license: the round-1 F1 ruling; *Reading a key* and *Changes to the rules* strike it
- fixed 2026-09-28 — [Minor] F13: "yes, and record" had no behaviour where the loader is unreachable; license: D43; *Recording an answer* withholds the option and says the answer holds for the session only
- fixed 2026-09-28 — the key-exclusion criterion was absolute in *The keys* and qualified in *Reading a key* (integrity note, ungraded); license: the round-1 F1 ruling; *The keys* now carries the qualified form
- hit fixed 2026-09-28 — *The loader*'s list of what `--set --dry-run` prints lacked the duplicate lines *The skill* step 3 now previews; added
- hit fixed 2026-09-28 — `--set --dry-run` had no test in D28 or *Verification*; both now name it
- signal 2026-09-28 — one more diff-scoped round earns its cost: F8, F9 and F10 change contracts; if that wave lands as suggested the round after should close the loop; the leftovers are worth nothing alone

### 2026-09-28 — architect, fable 5.1, blocking (round 1, full-document)

- hit fixed 2026-09-28 — spec used the newly banned "key list" at D6 and *The key registry*; reworded to "definition of a key"
- hit fixed 2026-09-28 — *The loader* called sh+sed+awk with no jq "the drift check's toolchain"; the drift check uses no awk and conditional jq; reworded
- hit fixed 2026-09-28 — D27's scope (one plugin, three directories) disagreed with *Verification* (four plugins, commands/ included); D27 widened
- hit fixed 2026-09-28 — the glossary's Key registry entry used its own banned term "key list"; reworded to "second definition of a key" (re-dispatch 1; its report carried CLEAN beside the hit, body governs)
- hit fixed 2026-09-28 — "its three values use the glossary's own words" was untrue for `cheapest`, which the glossary never uses; reworded to name the workflow rule as its source (re-dispatch 2, the episode's last; fix verified by grep, no third run)
- fixed 2026-09-28 — [Important] F1: the tier key changes the rule's behaviour, the criterion that excludes the round cap; D35 strips the card's rationale without a replacement; ruling: 2026-09-28; the key stays, argued in *Reading a key* on the recorded CLEAN-beside-hits history and the gate-tier measurement; D35 turns the card's cheap-family argument into the default's argument
- fixed 2026-09-28 — [Important] F2: the in-flow "yes, and record" write has no owner; ruling: 2026-09-28; new D43, the loader's `--set` owns every write; D12, D19, D37, *Recording an answer*, *The skill* and *Migration* call it
- fixed 2026-09-28 — [Minor] F3: plain stdout or a JSON envelope left undecided; ruling: 2026-09-28; D9 and *The loader* choose plain stdout, the dogfood confirms
- fixed 2026-09-28 — [Minor] F4: the by-hand resolution in an always-on rule; ruling: 2026-09-28; D12, D38 and *Reading a key* move it to a reference file read on the no-hook path
- fixed 2026-09-28 — [Minor] F5: the `withdrawn` marker and its loader report have no v1 instance; ruling: 2026-09-28; D8 and *The key registry* defer both to the first retired key; never-rename stays
- fixed 2026-09-28 — [Minor] F6: the loader's root order differs from the drift hook's with no stated reason; license: D33 and D1 ("at the repository root"); *The loader* says the git root binds deliberately
- fixed 2026-09-28 — [Minor] F7: two `working-process` directories with different jobs; license: glossary **Dispatch record**; *Directory modes* names the record store and makes `process-settings.md` tell the two apart
- fixed 2026-09-28 — D17's first step was qualified by its second without saying so (integrity note, ungraded); license: D17; step 1 now names the signal that agrees or stands alone
- fixed 2026-09-28 — D7.3's `on` and unset both produced an offer with the difference unstated (integrity note, ungraded); license: the workflow rule's technical-design declaration; *The keys* states the three behaviours
- hit fixed 2026-09-28 — D24 still had the skill write the personal `.gitignore`, which D43 gives to `--set`; D24 now names `--set`
- hit fixed 2026-09-28 — *The settings files* had the skill write each key's question comment; now `--set`
- hit fixed 2026-09-28 — *Scope and precedence* had the skill write in a worktree and place the `.gitignore`; now `--set`, called by the skill or a "yes, and record" answer
- hit fixed 2026-09-28 — "`mid` and `most-capable` are the glossary's own words" overclaimed for `most-capable`, which shortens "most capable available"; reworded (re-dispatch 1; the run self-reported haiku while its transcript metadata shows claude-sonnet-5, the dispatched model)
- signal 2026-09-28 — another round earns its cost only after F1 and F2 are decided; one diff-scoped round over those changes should close the loop; the Minors alone do not justify one
