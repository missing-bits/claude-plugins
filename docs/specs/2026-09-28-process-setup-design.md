---
ticket: none
date: 2026-09-28
status: draft
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
  other key list. Argued in *The key registry*.
- **D7** — The version-one keys. Argued in *The keys*.
  - **D7.1** — `dir.default`: `tracked` | `ignored`, team.
  - **D7.2** — `dir.docs/specs`: `tracked` | `ignored`, team, an
    optional exception to `dir.default`.
  - **D7.3** — `design.technical-design-offer`: `on` | `off`, team.
  - **D7.4** — `dispatch.propagation-auditor-model`: `cheapest` |
    `one-above-cheapest` | `most-capable`, team; default `cheapest`.
  - **D7.5** — `docs-branch.merge`: `squash` | `fast-forward`, team.
  - **D7.6** — `consult.personas`: `yes` | `no`, personal.
  - **D7.7** — `review.autonomy`: `yes` | `no`, personal.
  - **D7.8** — `review.per-round-commit`: `yes` | `no`, personal.
  - **D7.9** — `dir.docs/technical-designs`, as D7.2.
  - **D7.10** — `dir.docs/plans`, as D7.2.
  - **D7.11** — `dir.docs/domain`, as D7.2.
  - **D7.12** — `dir.docs/code-review`, as D7.2.
  - **D7.13** — `dir..superpowers`, as D7.2.
  - **D7.14** — `dir.docs/memory`, as D7.2, registered only where the
    project-memory plugin is installed.
- **D8** — Keys are never renamed. A retired key stays in the registry
  marked `withdrawn <version>`, and the loader reports a withdrawn key
  it meets. Argued in *The key registry*.
- **D9** — A SessionStart hook runs a loader that emits the effective
  value and source of every registered key, plus warnings, as the
  hook's additional context. Argued in *The loader*.
- **D10** — The loader stays silent when `.working-process/` does not
  exist, exits 0 on any error of its own, and caps its output at 4 KB,
  saying so when it truncates. Argued in *The loader*.
- **D11** — The loader is its own hook handler, registered without a
  matcher so it also runs on resume and compaction; it finds the
  registry relative to its own path and uses POSIX `sh`, `sed` and
  `awk`. Argued in *The loader*.
- **D12** — A new always-on rule, `process-settings.md`, is the only
  definition of the files, the grammar, the block and the procedure for
  reading a key. Argued in *Reading a key*.
- **D13** — A rule reads a key from the block in its context; without a
  block, from the two files; an unset key means the rule's behaviour
  before this change. Argued in *Reading a key*.
- **D14** — An answer given in the current session outranks the
  settings, compaction included. Argued in *Reading a key*.
- **D15** — Background agents never read settings; the dispatcher
  resolves every key it acts on. Argued in *Reading a key*.
- **D16** — Each site that asks a standing question today names its key
  and its behaviour when the key is unset, replacing "the developer's
  own instructions". Argued in *Changes to the rules*.
- **D17** — A settings key becomes a declared signal for a Process
  directory. At the first touch of a directory: a visible signal
  governs; a visible signal contradicting the key is reported and the
  developer asked, with nothing changed; a key without a visible signal
  is applied unasked; with neither, the rule asks. Argued in *Directory
  modes*.
- **D18** — `.working-process/` is not a Process directory: it is never
  asked about, and the rule says so. Argued in *Directory modes*.
- **D19** — When a standing question is asked in ordinary work, its
  answers include "yes, and record", which writes the answer to the
  file its scope names. There is no separate "record it?" question.
  Argued in *Recording an answer*.
- **D20** — A `CLAUDE.md` note that declares a key's value keeps binding
  until it is migrated; where it and a settings value disagree, the
  settings value wins and the session says so. Argued in *Migration*.
- **D21** — The `process-setup` skill runs only on request. It shows
  the effective settings, asks only about unset keys, previews its
  changes, and writes by replacing a key's line in place. Argued in
  *The skill*.
- **D22** — The skill materializes a declared mode only in a Process
  directory that already exists and does not contradict it; it creates
  no directory. Argued in *The skill*.
- **D23** — On its first run the skill offers existing declarations and
  signals as candidates: directory signals as certain, prose notes in
  `CLAUDE.md` as the model's reading, to be confirmed. It never deletes
  a `CLAUDE.md` note without consent. Argued in *Migration*.
- **D24** — The skill writes `.working-process/.gitignore` holding the
  single line `settings.local.md` at its first write. Argued in *The
  skill*.
- **D25** — The skill asks about `dir.docs/memory` only when the
  project-memory plugin is installed, and the project-memory rule reads
  that key only when the working-process rules are installed. Argued in
  *The keys*.
- **D26** — Version one reads the working-process registry alone; no
  domain registry is read or discovered. Argued in *Out of scope*.
- **D27** — A repository test checks that every registered key is cited
  by the rule its entry names, that every key cited under the plugin's
  `rules/`, `skills/` and `agents/` is registered, that defaults
  validate, and that names are unique. Argued in *Verification*.
- **D28** — Repository tests run the loader on fixtures for
  precedence, suggestions, invalid and duplicate values, unknown keys,
  the worktree fallback, the size cap, silence and error exit. Argued
  in *Verification*.
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
  family and accepts the tier the dispatcher resolved, still reporting
  its family for the dispatcher's comparison. Argued in *Reading a key*.
- **D36** — Every line shaped like a key — a dotted name and a colon at
  the start of a line, outside a fence — is a declaration, validated,
  and diagnosed when its value is invalid; it is never commentary.
  Argued in *The settings files*.
- **D37** — A write inserts an absent key, replaces a present one, and
  on a duplicate asks which line stands; after writing, the writer
  prints the fresh block, which supersedes the old one for the rest of
  the session. Argued in *The skill*.
- **D38** — Without a trustworthy block — none, or one marked
  incomplete — a session resolves keys by the loader's own procedure,
  through `--print` or by applying the rule's full resolution by hand.
  Argued in *Reading a key*.
- **D39** — The skill asks about directory exceptions only when the
  developer asks for them. Argued in *The skill*.
- **D40** — The python and salesforce review commands and the
  project-memory rule, which restate the first-create predicate, adopt
  the settings key and its conflict question. Argued in *Changes to the
  rules*.

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

Recognizing a declaration and validating it are separate steps. Every
line shaped like a key — a dotted name and a colon at the start of a
line, outside a fence — is a declaration, whatever follows the colon,
and a value that is not a valid token for that key is diagnosed rather
than read past. So `review.autonomy: "no"` below `review.autonomy: yes`
is a duplicate, and the key is unset; it cannot hide as commentary and
leave the earlier consent standing. Fences open and close on lines
starting with three backticks; leading whitespace makes a line
commentary. Every other line is commentary, and the skill writes each
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
serves every worktree of a repository. The skill, run in a worktree,
writes personal answers to the main checkout's file, so a worktree
never gains a file of its own through the skill. A personal file
created in a worktree by hand replaces the fallback wholly — no
per-key merge — and the loader's first line says which file it read.

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
key list exists to drift. A key is never renamed: renaming would
silently orphan every file that set it. A retired key keeps its entry
with `withdrawn <version>`, and the loader reports it as withdrawn
rather than unknown. The registry's exact path and heading shape are the
plan's to fix.

## The keys

Version one registers the keys whose question has no home today:

| Key | Scope | Values | Unset means | Read by |
|---|---|---|---|---|
| `dir.default` | team | `tracked` \| `ignored` | ask at first create | process-artifacts |
| `dir.<path>` | team | `tracked` \| `ignored` | absent: `dir.default` applies; invalid: ask | process-artifacts |
| `design.technical-design-offer` | team | `on` \| `off` | today's manifest-raised offer | workflow |
| `dispatch.propagation-auditor-model` | team | `cheapest` \| `one-above-cheapest` \| `most-capable` | `cheapest` | workflow |
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

The gate model is a tier, not a model name, so a Codex port can map it
onto its own families. Consent values are `yes` and `no` alone. A
session-scoped answer — "not now", "not in this session" — is never a
key, because it dies with the session by definition.

Deliberately not keys in version one: process weight, whose readers do
not exist yet; the rules install level and commit mode, whose answer
the rules manifest's position already records; the review loop's round
cap, which stays fixed by the rule — making it a key would change the
rule's behaviour, not only where an answer is recorded; and every
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
duplicates, a key in the wrong scope's file, a withdrawn key.

The output is capped at 4 KB. That is a byte cap, not a token
guarantee: Codex's documented per-handler threshold is about 2,500
tokens, above which it stores the context on disk and shows a preview,
and 4 KB of ordinary output sits under it with room to spare. The
dogfood checks it rather than the spec promising it. Where the cap
truncates, the last line says the block is incomplete; it never
truncates silently. A block for the version-one keys runs to about
1 KB. Paths and warnings in the block are escaped as JSON requires
when the hook emits its JSON envelope.

The loader stays silent — no output at all — when `.working-process/`
does not exist, so a project that never adopted the settings pays
nothing. An error of the loader's own ends in silence and exit 0, as
the drift check does, and the rule's fallback (*Reading a key*) covers
the missing block.

It finds the repository root through `git rev-parse --show-toplevel`,
then `CLAUDE_PROJECT_DIR`, then the working directory — in a worktree,
the worktree's own root — and the registry
relative to its own path rather than through `CLAUDE_PLUGIN_ROOT`, which
a Codex port may not provide. It is registered without a matcher, so it
runs on startup, resume, clear and compaction alike, and a compacted
conversation gets its settings back. It is its own handler rather than a
branch of the drift check, because Codex budgets context per handler.
It uses POSIX `sh` with `sed` and `awk`, the drift check's toolchain,
and no `jq`. Two modes serve the skill and the no-hook path:
`--print` emits the same block to standard output, and
`--validate --scope team|personal <file>` checks a candidate file
against the scope it is meant for, printing its warnings and exiting
non-zero when the file would not validate. Only the hook mode swallows
its errors and exits 0; the other two report failure.

## Reading a key

A new always-on rule, `process-settings.md`, is the one definition of
the files, their grammar, the block and the reading procedure. The
rules that read a key cite it and restate none of it.

To read a key, a session:

1. takes its value from the settings block in its context, unless the
   block says it is incomplete;
2. without a trustworthy block — none arrived because hooks are
   disabled or a Codex plugin is not yet trusted, or the block says it
   is incomplete — resolves the key by the loader's own procedure:
   running `--print` where the script is reachable, otherwise applying
   `process-settings.md`'s full resolution by hand — scope, the
   worktree fallback, defaults, duplicates and invalid values — never a
   shortcut through the files;
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
with its family, so the dispatcher's comparison keeps working.

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
  tier (`dispatch.propagation-auditor-model`).
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
- `project-memory.md` — `dir.docs/memory` counts as a declaration when
  the working-process rules are installed, and its "never ask when a
  prior decision is present" gains the conflict question: a visible
  signal that contradicts the key is reported and the developer asked.
- `agents/propagation-auditor.md` — the tier clause, as *Reading a key*
  says.

## Directory modes

`process-artifacts.md` today reads two visible signals — a
`.gitignore` holding exactly `*` means ignored, a git-tracked file means
tracked — and a declared instruction, "materialized by whoever first
acts on it". A settings key becomes that declared instruction's named
form. At the first touch of a Process directory:

1. a visible signal governs;
2. a visible signal that contradicts the key is reported, and the
   developer asked which stands; nothing is changed until they answer;
3. a key with no visible signal is applied without asking — the ignored
   mode by writing the `*` `.gitignore`, the tracked mode by the first
   committed file;
4. with neither, the rule asks, as today.

`.working-process/` itself is configuration, not a Process directory:
its team file is committed by definition and its local file ignored by
its own `.gitignore`. It is never asked about, and `process-artifacts.md`
says so, so it cannot become one more first-create question.

## Recording an answer

When a standing question is asked in ordinary work, its answers gain
one option: "yes, and record" (or "no, and record"). Choosing it writes
the answer to the file the key's scope names, creating the file and its
`.gitignore` where they are missing. There is no second question: the
developer is interrupted once, as the review loop's one-batch-per-round
contract intends. A session never records an answer the developer did
not choose to record.

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
never deletes a note without consent; after a confirmed move it offers
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
3. previews the change to each file, validates it with
   `--validate --scope`, and writes: an absent key is added, under its
   question as a comment; a present key's line is replaced in place; a
   duplicated key is shown with both lines and the developer chooses
   which stands. Every other line and comment stays untouched, and an
   unchanged file is not written. After writing, it prints the fresh
   block, which supersedes the one from session start for the rest of
   the session — the same holds for a "yes, and record" answer;
4. materializes a declared mode in each Process directory that already
   exists and does not contradict it, and reports every contradiction;
   it creates no directory;
5. writes `.working-process/.gitignore` at its first write.

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
  `.working-process/`; silence and exit 0 on an error of its own.
- **Claude Code dogfood**, with the plugin loaded from the checkout: the
  skill records settings; a new session receives the block; a recorded
  question is not asked; after `/compact` the block is back. The run
  also settles whether the SessionStart hook takes plain standard output,
  the JSON `additionalContext` shape the drift check uses, or both.
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

- New: the `process-setup` skill; the key registry; the loader script;
  the `process-settings.md` rule; a second SessionStart handler in
  `hooks/hooks.json`.
- `rules/workflow.md`, `rules/spec-plan-lifecycle.md`,
  `rules/process-artifacts.md` — as *Changes to the rules* and
  *Directory modes* say.
- `agents/propagation-auditor.md` — the tier clause.
- `plugins/project-memory/rules/project-memory.md` — the conditional
  `dir.docs/memory` declaration and its conflict question.
- `plugins/python-standards/commands/python-review.md`,
  `plugins/salesforce-standards/commands/salesforce-review.md` — the
  restated first-create predicate.
- `docs/domain/glossary.md` — **First-create question** gains the
  settings key as a signal, through a grilling session on this spec.
- Tests under `tests/working-process/`.
- README and CHANGELOG entries under `## Unreleased` for working-process
  and project-memory; a `-dev` dogfood version.

## Open questions

- The name `one-above-cheapest` for the middle gate tier.
- `dir..superpowers` carries a double dot because the path starts with
  one; the plan may keep it or fix a mapping for leading-dot paths.
