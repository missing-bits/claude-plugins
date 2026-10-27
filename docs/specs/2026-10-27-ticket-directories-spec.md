---
ticket: none
date: 2026-10-27
status: draft
grilled: 2026-10-27
architect: concerns (resolved 2026-10-27)
decisions: registered
branch: feature/ticket-directories
base: develop
---

# Ticket directories — a ticket's documents in one place

A project that works ticket by ticket keeps each ticket's material in
one directory: an analysis, a spike and its results, a handoff, a
brief, data files, a runbook. Its design spec, technical design and
plan live elsewhere, in `docs/specs/`, `docs/technical-designs/` and
`docs/plans/`, so they are not at hand when someone opens the ticket.
This spec lets a project opt into a ticket root under `docs/`: a new
document for a ticket goes into that ticket's directory, beside
everything else the ticket has.

## Problem

A client project the developer works in keeps `docs/jira/<key>-<topic>/`
per ticket, tracked in git, with the key in lower case
(`abc-1489-opportunity-team`). Reviewing a ticket meant opening that
directory and then searching three other directories for the documents
the working process wrote. The developer wants to open the ticket
directory and find everything.

The working process finds a document's class by its directory: the
three class directories appear 47 times in 13 plugin files — rule
`paths:` globs, process-status, `scripts/decision-coverage.py`, the
`dir.*` settings keys and relative frontmatter links. Since the
document-names convention (`spec-plan-lifecycle.md`, *Judged documents
and plans*), a new document's name carries its class
(`<prefix>-<topic>-spec.md`, `-technical-design.md`, `-plan.md`), so
the class no longer needs the directory.

## Goals, non-goals, anti-goals

Goals:

- With the ticket root set, a new design spec, technical design or plan
  for a ticket lands in that ticket's directory.
- Code-review reports for a ticket land in the same directory.
- A document written without a ticket can move into a ticket directory
  later, on the developer's command, with its chain and its links.
- A project that never sets the ticket root behaves as it does today.

Non-goals:

- CI runs. A review run in CI without a readable branch name falls back
  to `docs/code-review/`; no CI-specific behaviour is designed until a
  real pipeline is observed.
- Ticket references that yield no file prefix (`org/repo#123`): such a
  document is treated as having no ticket.
- Moving existing documents without a command.
- Dropping `date:` from process documents.

Anti-goals — the change fails, even if it works, when:

- a second directory appears for a ticket that already has one;
- a link between documents breaks;
- the process writes its frontmatter into a document that does not
  need it. A companion document may carry its own frontmatter; the
  process leaves it alone.

## Decisions

- **D1** — One team settings key, `ticket.root`, turns ticket
  directories on; unset keeps today's layout. Argued in *The setting*.
- **D2** — The key's value is a path under `docs/`, validated by the
  loader; the registry gains a path-valued key shape. Argued in *The
  setting*.
- **D3** — A document for a ticket goes to `<root>/<prefix>-<topic>/`,
  one level below the root; a document without a usable ticket stays in
  its class directory. Argued in *Placement*.
- **D4** — An existing ticket directory is found case-insensitively by
  `<prefix>-` among the root's immediate subdirectories, in the working
  tree and on the integration branch's remote-tracking ref (else its
  local branch); it is used whatever its topic. Argued in *Placement*.
- **D5** — Ticket directories count among the project's ticket-named
  files for the key case: a file prefix and a new directory take the
  case the existing ones use, else the tracker's. A new directory takes
  the topic of the document that creates it. Argued in *Placement*.
- **D6** — Several matching directories, or a document carrying several
  tickets, are put to the developer. Argued in *Placement*.
- **D7** — A process document's class is detected from its class
  suffix, or from its class directory for a document named before the
  document-names convention; the rules covering design specs,
  technical designs and plans
  load on suffix globs anchored at `docs/`, beside their directory
  globs, and still branch on the class, never on a file pattern.
  Argued in *Recognising a process document*.
- **D8** — A file matching a class suffix but carrying no `status:` in
  its frontmatter is not a process document: the process neither edits
  nor reports it. Argued in *Recognising a process document*.
- **D9** — A companion document in a ticket directory needs neither
  `ticket:` nor `date:`; process documents keep their full frontmatter.
  Argued in *Companion documents*.
- **D10** — The ticket root and its ticket directories are not Process
  directories: tracked, with no first-create question, no `.gitignore`
  written by the process and no `dir.*` key reaching them; ignores the
  project sets inside them are respected. Argued in *Modes*.
- **D11** — The always-loaded workflow rule states where a ticket's
  documents go, including the reuse of an existing ticket directory,
  since the path-scoped lifecycle rule loads only once the first file
  is written. Argued in *Recognising a process document*.
- **D12** — Frontmatter links are relative to the document that holds
  them. Argued in *Links*.
- **D13** — `decision-coverage.py` recognises a technical design by the
  `-technical-design.md` suffix as well as by its directory. Argued in
  *Recognising a process document*.
- **D14** — A code-review report whose ticket the branch name gives
  goes to `<ticket directory>/code-review/`, unless it is local-only;
  any other report goes to `docs/code-review/`. Argued in *Review
  reports*.
- **D19** — A branch name follows the scheme `[<type>/]<key>[-<slug>]`,
  `<type>` any one segment and `<key>` a key shape; a name in the scheme
  whose ticket directory exists gives the review its ticket, while a
  name in the scheme without one, or a key shape outside the scheme, is
  asked about in an interactive session and gives no ticket otherwise.
  A review never creates a ticket directory. The ticket-frontmatter
  rule sources a new document's ticket from a branch by the same
  scheme. Argued in *Review reports*.
- **D20** — The review command resolves the report directory from the
  working tree before dispatch and hands the agent the path, and a solo
  run resolves it the same way before it writes; a run with no
  interactive dispatcher, an ambiguity
  nobody can answer, or a local-only report writes to
  `docs/code-review/`. Argued in *Review reports*.
- **D15** — Moving a document into a ticket directory is a procedure in
  the lifecycle rule, run by the session on the developer's command; no
  skill. Argued in *Moving a document*.
- **D16** — The move offers the document's whole chain. Argued in
  *Moving a document*.
- **D17** — The move rewrites every reference to and from each moved
  file, and stops for the developer before any body edit to an
  `implemented` document. Argued in *Moving a document*.
- **D21** — The move recomputes the `integrity:` hashes of a document
  whose body it rewrote, keeping the audit date, only where they matched
  before the move; it asks for no new audit. Argued in *Moving a
  document*.
- **D18** — The glossary gains *Ticket root*, *Ticket directory*,
  *Process document*, *Companion document*, *Class suffix* and *Class
  directory*, minted in the grilling session of 2026-10-27; *Process
  directory* names the ticket root among its exclusions, and *Review
  report* admits a ticket directory's `code-review/`.
  Argued in *Modes*.

## The setting

`ticket.root` is a team key in `SETTINGS_REGISTRY.md`, read by the
lifecycle, workflow, ticket-frontmatter, review-reports and
process-artifacts rules and by the python-standards and
salesforce-standards review commands, asked by process-setup. Its name says what it
decides; `dir.` is taken by mode keys and `docs.` would read as kin of
`docs-branch.merge`.

Every key today takes enumerated values, and three places rely on that:
the loader's `valid_value` and `do_set`, the registry test, and
process-setup's choices. The registry gains one non-enumerated token,
`values: <path>`, with `default: unset`. The loader accepts a `<path>`
value when it starts with `docs/`, names at least one segment after it,
contains no `..` segment and no trailing `/`; the settings grammar
already bars spaces and glob characters. The registry test admits the
token, and process-setup asks the question as free text.

The root lies under `docs/` because every lookup the process runs
already searches `docs/`: process-status's commands, the `ticket:`
sweep, the `revises:` lookup and the ticket-frontmatter rule's
`docs/**` load. A root elsewhere would force a settings path into
published commands.

## Placement

With `ticket.root` set, a new design spec, technical design or plan
whose `ticket:` yields a file prefix goes into the ticket directory
`<root>/<prefix>-<topic>/`, named by the document-names convention. The
prefix rule is that convention's. A ticket value yielding no prefix,
or `none`, leaves the document in its class directory.

Before creating a directory the session looks for one. It lists the
root's immediate subdirectories whose name starts with `<prefix>-`,
ignoring case — the trailing hyphen keeps `abc-14-` from matching
`abc-1489-` — in the working tree, listed from the repository's top
level (`git rev-parse --show-toplevel`), and on the integration branch
with `git ls-tree --full-tree -d --name-only <ref> <root>/`; without
`--full-tree` the path is read from the current directory, and a run
below the top level prints nothing and exits 0. The integration branch is
the one topic branches are cut from, as the project's instructions or
the document's `base:` name it; where neither names it, the session
asks once. `<ref>` is its remote-tracking ref (`origin/develop`) where
one exists, else the local branch; the session never fetches, which
stays with the developer, and a branch that exists nowhere skips the
second lookup and says so. The second lookup exists because a ticket's
directory may exist only on another branch, and git would merge a
second one in silently.

One match is used whatever its topic. No match: the session creates
the directory, with the topic of the creating document. Ticket
directories count among the project's ticket-named files of the
document-names convention, so a file prefix and a new directory take
the case the existing ones use — in the client project, lower case
(`abc-12-old/abc-12-login-spec.md`) — and with none, the tracker's.
Several matches, or a `ticket:` list of several keys, go to the
developer.

## Recognising a process document

The rules for judged documents and plans load on suffix globs anchored
at `docs/`, beside their directory globs, which stay for documents
named before the document-names convention:

| rule | added glob |
|---|---|
| `spec-plan-lifecycle.md` | `docs/**/*-{spec,technical-design,plan}.md` |
| `propagation-duties.md` | `docs/**/*-{spec,technical-design,plan}.md` |
| `process-artifacts.md` | `docs/**/*-{spec,technical-design,plan}.md` |
| `technical-design.md` | `docs/**/*-technical-design.md` |

Anchoring at `docs/` keeps the globs off files elsewhere in the repo.
The cost to every project, opted in or not: a file under `docs/` named
`*-plan.md` now loads these rules when read.

A ticket directory holds files a developer names freely; the client
project already has a `screens-spec.md` there. The lifecycle rule says:
a process document opens with frontmatter carrying `status:`; a file
that matches a class suffix without it belongs to the developer, and
the process neither adds frontmatter to it nor reports it.

Suffix globs fire only on a correctly named file, and the naming rule
itself is path-scoped: the lifecycle rule loads on the first Write of a
matching file, which is the write that creates a new directory. The
lookup that keeps a ticket to one directory must therefore load before
it. The workflow rule, which always loads, already says where
documents go; it gains: with `ticket.root` set and a ticket, in the
root's subdirectory whose name starts with `<prefix>-`, ignoring case,
in the working tree or on the integration branch — several go to the
developer — and only with none in a new `<root>/<prefix>-<topic>/`,
named by the lifecycle rule — and it ends by requiring the session to
read the spec-plan-lifecycle rule before creating a ticket directory,
since that rule holds the lookup's commands and cannot be counted on to
have loaded yet. The workflow rule already requires the same read of a
plan-writing brief for the same reason.

`decision-coverage.py` resolves links relative to the document it is
given and finds nothing on its own; its one directory assumption is
`is_technical_design()`, which requires a `docs/technical-designs/`
parent. A technical design in a ticket directory carries `spec:`, so
the script would audit it as a plan. The test also accepts a name
ending in `-technical-design.md`.

The ticket-frontmatter rule picks a field set by directory; it picks it
by class, read from the name or the class directory.

## Companion documents

A companion document — any file in a ticket directory that is neither
a process document nor a review report — needs neither `ticket:` nor
`date:`: the directory names the ticket and git keeps the dates. It may
carry frontmatter of its own; the process leaves it untouched.
Process documents in a ticket directory keep their full frontmatter,
which the process reads.

## Modes

The glossary's *Process directory* is deliberately narrow, and the
ticket root joins its exclusions: the root and its ticket directories
are tracked by the definition of `ticket.root`, never asked about, and
no `dir.*` key reaches a document inside them. `dir.docs/specs:
ignored` keeps governing design specs without a ticket. The process
writes no `.gitignore` under the root, and what the project's own
ignore rules exclude there — a `docs/jira/*/test-data/` line, say — it
respects and may still write to; it never force-adds such a file. The
process-artifacts rule says so in one sentence.

The rules lean on six new terms — *Ticket root*, *Ticket directory*,
*Process document*, *Companion document*, *Class suffix*, *Class
directory* — minted in the glossary by the grilling session of
2026-10-27. The same session sharpened *Judged document*: the lifecycle
rule branches on the class, and a class suffix only detects it.

## Links

A frontmatter link is relative to the document that holds it. In a
ticket directory the documents of one chain are siblings
(`spec: ./ABC-123-login-spec.md`); a link from a ticket directory to a
class directory climbs further (`../../specs/…`). The lifecycle rule's
`../specs/<file>.md` examples read as relative links, not as templates.

## Review reports

The review-reports rule gains one placement rule. With `ticket.root`
set, a report whose ticket the current branch name gives goes to
`<ticket directory>/code-review/`. A branch name follows the scheme
`[<type>/]<key>[-<slug>]`: an optional single segment of any type
(`feature/`, `bugfix/`, `hotfix/`), then a key shape — letters, a
hyphen and digits (`ABC-123`), or digits alone (`42`, which the prefix
rule turns into `ticket-42`) — then an optional slug. `feature/ABC-123-login`,
`bugfix/ABC-1-x`, `ABC-123` and `hotfix/42-crash` all fit.

| the branch name | interactive session | no interactive dispatcher |
|---|---|---|
| fits the scheme, and the key's ticket directory exists | the ticket directory, no question | the ticket directory |
| fits the scheme, no ticket directory (`feature/phase-2-cleanup`) | asks whether the branch is ticket `PHASE-2`'s | `docs/code-review/` |
| carries a key shape outside the scheme (`jan/abc-123-fix`, `release-ABC-123`) | asks for the ticket | `docs/code-review/` |
| carries no key shape (`feature/ticket-directories`) | `docs/code-review/`, no question | `docs/code-review/` |

An answer holds for that branch until the session ends, so later
review rounds do not ask again; nothing is recorded. A review never
creates a ticket directory: a confirmed ticket whose directory does
not exist sends the report to `docs/code-review/`, and a ticket's
directory appears with its first process document.

The ticket-frontmatter rule sources a new document's ticket from the
branch name before the conversation; it reads the branch by the same
scheme, so one definition of a ticket in a branch name serves both.

The review command resolves the directory before dispatch, as it
already runs the first-create check before dispatch: it looks for the
ticket directory in the working tree only and hands the agent the
report directory's path. A review creates no directory, so the
integration-branch lookup, which exists to prevent a second one, has
nothing to guard; a directory present only on another branch sends the
report to `docs/code-review/`. An interactive solo run resolves the
directory the same way before it writes: resolving a directory is not
generating a file name, so the rule that file-name generation runs no
shell command and asks nothing still holds. Several matching
directories are asked about before dispatch in an interactive session;
a run with no interactive dispatcher writes to `docs/code-review/`,
like a report whose branch names no ticket — a detached HEAD in CI,
among others. Nothing blocks an unattended run.

`<ticket directory>/code-review/` inherits the ticket directory's
tracked mode, so no first-create question is asked. A local-only
report — one the local pocket would hold — always goes to
`docs/code-review/`, since the pocket works by writing a `.gitignore`
and the process writes none under the ticket root. The rule's `paths:`
gains `docs/**/code-review/**`. The python-standards and
salesforce-standards commands, agents, code-review skills and READMEs
name `docs/code-review/` as the only location; each learns that the
dispatch names the directory.

## Moving a document

A document written without a ticket may later belong to one. On the
developer's command the session moves it into the ticket directory; the
procedure lives in the lifecycle rule, since the rule already loads
when the session opens the document.

1. The ticket is the document's `ticket:` value, or the command's when
   that is `none`; several tickets go to the developer.
2. The session finds the chain — the documents the moved one links to
   and those that link to it, by `spec:`, `technical-design:`,
   `revises:` and `**Follows:**` — and offers to move them together.
3. Each moved file takes the convention's full name in the ticket
   directory, keeping its own topic; a file named before the
   convention gains its class suffix. A tracked file moves with
   `git mv`; an untracked one, in an ignored class directory, with `mv`
   and `git add`.
4. The session rewrites every reference: inbound and outbound
   frontmatter links, the `with:` file in `integrity:`, `**Follows:**`
   lines and qualified decision identifiers (`<file>.md#D3`) in bodies.
   A body edit an `implemented` document would need stops the move and
   goes to the developer; the frontmatter of an `implemented` document
   may change, since the `integrity:` hash covers the body only.
   A rewritten path changes no content, so the move asks for no new
   audit: where a document's `integrity:` hashes — its own `sha:` and
   any `with:` hash — matched its body before the move, the session
   recomputes them with the lifecycle rule's hash command after the
   rewrite and keeps the audit date. A hash that did not match before
   the move stays as it was, since recomputing it would stamp edits
   nobody audited.
5. References outside `docs/` are listed, never rewritten.
6. The session reports every path it rewrote and every reference it
   left alone, and names each file that was untracked before the move
   and is tracked now.

## Verification

- Loader tests cover the `<path>` value: valid, outside `docs/`, `..`,
  trailing `/`.
- A `test_decision_coverage.py` case audits a technical design outside
  `docs/technical-designs/` as a technical design.
- A dogfood in a scratch project with `ticket.root: docs/jira` and one
  existing `abc-12-old/` directory: a spec for `ABC-12` lands in it; a
  spec for `ABC-77` creates `abc-77-<topic>/`; a `screens-spec.md`
  without `status:` stays untouched; a dated spec with `ticket: ABC-77`
  moves with its plan and every link resolves, an `integrity:` stamp
  that matched before the move matches after it; a review on
  `feature/ABC-12-x` writes to `abc-12-old/code-review/`, so does one
  on `bugfix/ABC-12-y` and one on `ABC-12`, and one on
  `feature/phase-2-cleanup` asks, then writes to `docs/code-review/`
  and creates no directory.
- In a project without `ticket.root`, the dogfood's ticketless flow
  writes to the class directories as today.

## Out of scope

- Nesting ticket directories below the root's first level.
- Changing `ticket.root` moves nothing: new documents go under the new
  root, and directories under the old one are moved by hand, outside
  the process.
- Detecting broken links after a manual move; the move procedure keeps
  links whole instead.
- A skill for the move; it returns only if sessions skip the procedure's
  steps in practice.

## Changes by file

- `SETTINGS_REGISTRY.md` — the `ticket.root` entry; the `<path>` value
  token in the preamble.
- `scripts/load-settings.sh` — `<path>` validation in `valid_value` and
  `do_set`.
- `tests/working-process/test_settings_registry.py`,
  `test_load_settings.py` — the token, the new key, the path cases.
- `skills/process-setup/SKILL.md` — a free-text question.
- `rules/spec-plan-lifecycle.md` — the suffix glob, placement, the
  `status:` gate, relative links, the move procedure.
- `rules/technical-design.md`, `rules/propagation-duties.md`,
  `rules/process-artifacts.md` — the suffix globs; process-artifacts
  also the ticket-root exclusion.
- `rules/workflow.md` — where a ticket's documents go.
- `rules/ticket-frontmatter.md` — field sets by class; companion
  documents in a ticket directory exempt; branch sourcing by the D19
  scheme.
- `rules/review-reports.md` — ticket placement of reports, the
  branch-ticket shape, the `docs/**/code-review/**` glob.
- `scripts/decision-coverage.py`, `tests/working-process/test_decision_coverage.py`
  — the suffix test.
- `skills/process-status/SKILL.md` — the directory list in its
  description.
- `docs/domain/glossary.md` — done in the grilling session and its
  fix wave: six new terms, the Process directory exclusion, the
  *Judged document* sentence, the *Review report* location.
- python-standards and salesforce-standards — the review command
  resolves the report directory before dispatch and hands its path to
  the agent; the agent, the code-review skill's location line and the
  README stop naming `docs/code-review/` as the only location.
- `CHANGELOG.md` of each changed plugin.

## Calls made by the author

- D5: ticket directories count among the ticket-named files, so a file
  and its directory share the key case; with none yet, the tracker's
  case, where the system-designer consultation suggested lower case.
- A ticket value yielding no prefix is treated as no ticket.
- The integration-branch lookup asks once where no instruction names
  the branch, reads the remote-tracking ref without fetching, and skips
  a branch that exists nowhere.
- An answer about a branch's ticket holds for the session and is not
  recorded.
- D21 recomputes only hashes that matched before the move, so a move
  never stamps unaudited edits.
- D20: an unattended run, or an ambiguity nobody can answer, writes
  to `docs/code-review/`, matching the CI non-goal.
- A move names each file it turns from untracked to tracked.

## Review rounds

### 2026-10-27 — architect, fable 5.1, concerns (round 2, diff-scoped)

- fixed 2026-10-27 — [Minor] R2-1: F1's fix put the lookup duty in the always-loaded workflow rule but left its commands in the lifecycle rule, which loads too late; license: D11; the workflow clause ends by requiring a read of the spec-plan-lifecycle rule before creating a ticket directory, the pattern the workflow rule already uses for a plan-writing brief
- fixed 2026-10-27 — [Minor] R2-2: the glossary's *Dispatch record* still located a review report under `docs/code-review/`; license: D18 and F3; the appositive names no location
- fixed 2026-10-27 — the reviewer's integrity note: D14 sent a local-only report to the ticket directory, and D20 had a solo run hand an agent the path; license: F2's ruling and F8; D14 excepts local-only reports, D20 separates the dispatched and the solo run

Resolved without a fresh round: both findings and the note are wording; no decision moved.

- fixed 2026-10-27 — D19 read a ticket only after `feature/`, so `bugfix/ABC-1-x` or a bare `ABC-123` branch lost its ticket; ruling: 2026-10-27; D19 and *Review reports* define the scheme `[<type>/]<key>[-<slug>]`, ask about a name outside it or without a ticket directory, and the ticket-frontmatter rule's branch sourcing reads the same scheme

### 2026-10-27 — architect, fable 5.1, blocking (round 1, full-document)

- fixed 2026-10-27 — [Important] F1: the lookup guarding anti-goal 1 sat in a path-scoped rule that loads only on the write creating the directory; license: anti-goal 1 and D4; D11 and *Recognising a process document* put the reuse of an existing ticket directory into the always-loaded workflow rule
- fixed 2026-10-27 — [Important] F2: the local pocket writes a `.gitignore`, which D10 and the glossary's *Ticket root* forbid under the root; ruling: 2026-10-27; option (a) — a local-only report always goes to `docs/code-review/` (D20, *Review reports*), D10 keeps no exception
- fixed 2026-10-27 — [Minor] F3: the glossary's *Review report* tied the report to `docs/code-review/`; license: D14; the entry admits a ticket directory's `code-review/`, D18 and *Changes by file* say so
- fixed 2026-10-27 — [Minor] F4: *Process document* recognised a document by its class suffix alone, excluding every document named before the convention; license: *Recognising a process document* (directory globs stay); the glossary entry and D7 add the class directory
- fixed 2026-10-27 — [Minor] F5: `git ls-tree` without `--full-tree` prints nothing below the top level and exits 0; license: anti-goal 1 and D4; *Placement* prescribes `--full-tree` and lists the working tree from `git rev-parse --show-toplevel`
- fixed 2026-10-27 — [Minor] F6: the review lookup carried the integration-branch check, which guards only directory creation; license: D19 (a review never creates a directory); *Review reports* and D20 look in the working tree only
- fixed 2026-10-27 — [Minor] F7: `read-by:` of `ticket.root` omitted the two review commands; license: D20 and the `dir.docs/code-review` precedent; *The setting* names them
- fixed 2026-10-27 — [Minor] F8: a solo review run had no step before writing; license: D14; *Review reports* and D20 have a solo run resolve the directory before it writes
- fixed 2026-10-27 — [Minor] F9: the brace-glob probe checks documented platform behaviour; license: the Claude Code memory docs (brace expansion, `src/**/*.{ts,tsx}`); the probe and its fallback are dropped from *Verification*
- fixed 2026-10-27 — *Ticket root* said every immediate subdirectory is a ticket directory, which a `templates/` subdirectory contradicts; ruling: 2026-10-27; the entry says the root holds the ticket directories
