---
ticket: none
date: 2026-10-27
status: draft
grilled: 2026-10-27
architect: concerns (resolved 2026-10-27)
integrity: 2026-10-27 (sha: 371c6bb)
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
  tickets, are put to the developer: a choice among the existing
  directories, or, where no listed ticket has one, of the ticket whose
  directory is created. Argued in *Placement*.
- **D7** — A process document's class is detected from its class
  suffix, or from its class directory for a document named before the
  document-names convention; the rules covering design specs, technical
  designs and plans load on suffix globs anchored at `docs/`, beside
  their directory globs, and still branch on the class, never on a file
  pattern. Argued in *Recognising a process document*.
- **D8** — A file matching a class suffix or lying in a class
  directory, but carrying no `status:` in its frontmatter, is not a
  process document: the process neither edits nor reports it. Argued
  in *Recognising a process document*.
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
- **D14** — A code-review report whose ticket the branch name gives,
  or the developer names for it (D19), goes to
  `<ticket directory>/code-review/`, unless it is local-only;
  any other report goes to `docs/code-review/`. Argued in *Review
  reports*.
- **D19** — With `ticket.root` set, a branch name is read by the
  scheme `[<type>/]<key>[-<slug>]`, `<type>` any one segment and
  `<key>` a key shape, defined once in the workflow rule's *Branch
  naming*. For a review's placement, a name in the scheme whose ticket
  directory exists gives the ticket directory; a letters-hyphen-digits
  shape outside the scheme is asked about in an interactive session;
  anything else places the report in `docs/code-review/`, while the
  report's `ticket:` field derives as today. A review never creates a
  ticket directory. For a new document, the ticket-frontmatter rule
  reads the same scheme and confirms a ticket whose directory does not
  exist yet. Without `ticket.root`, branch sourcing is unchanged.
  Argued in *Review reports*.
- **D20** — The review command resolves the report directory from the
  working tree before dispatch and hands the agent the path, and a solo
  run resolves it the same way before it writes; a run with no
  interactive dispatcher, an ambiguity nobody can answer, or a
  local-only report writes to `docs/code-review/`. Argued in *Review
  reports*.
- **D15** — Moving a document into a ticket directory is a procedure in
  the lifecycle rule, run by the session on the developer's command; no
  skill. Argued in *Moving a document*.
- **D16** — The move offers the document's whole chain. Argued in
  *Moving a document*.
- **D17** — Inside `docs/`, the move rewrites each moved file's
  frontmatter links in both directions, the `with:` file of
  `integrity:`, `**Follows:**` lines and qualified decision
  identifiers; it lists, never rewrites, a path in body prose and any
  reference outside `docs/`, and stops for the developer before any
  body edit to an `implemented` document. Argued in *Moving a
  document*.
- **D21** — The move recomputes the `integrity:` hashes of a document
  whose body it rewrote, keeping the audit date, only where they matched
  before the move; it asks for no new audit. Argued in *Moving a
  document*.
- **D22** — The integration branch for the lookup is the one the
  project's instructions name, else the session asks once; the lookup
  reads its remote-tracking ref where one exists, else the local
  branch, never fetches, and skips a branch that exists nowhere,
  saying so. Argued in *Placement*.
- **D23** — A declined confirmation of a branch ticket falls through to
  the conversation and then to `none`, never to a second question; one
  answer about a branch's ticket serves the review and the
  ticket-frontmatter rule for the rest of the session, is not
  recorded, and is stated in the workflow rule's *Branch naming*.
  Argued in *Review reports*.
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
salesforce-standards review commands, asked by process-setup. Its name
says what it decides; `dir.` is taken by mode keys and `docs.` would read as kin of
`docs-branch.merge`.

Every key today takes enumerated values, and three places rely on that:
the loader's `valid_value` and `do_set`, the registry test, and
process-setup's choices. The registry gains one non-enumerated token,
`values: <path>`, with `default: unset`. The loader accepts a `<path>`
value when it starts with `docs/`, names at least one segment after it,
contains no `..` segment and no trailing `/`, and neither equals nor
lies inside a Process directory (`docs/specs/`, `docs/code-review/`,
and the rest the process-artifacts rule lists); the settings grammar
already bars spaces and glob characters. The registry test admits the
token, and process-setup asks the question as free text.

The root lies under `docs/` because every lookup the process runs
already searches `docs/`: process-status's commands, the `ticket:`
sweep, the `revises:` lookup and the ticket-frontmatter rule's
`docs/**` load. A root elsewhere would force a settings path into
published commands. Process-status's commands therefore stay as they
are; only its `description:`, which names the class directories as
where it looks, gains the ticket directories, or the skill would not
trigger for a status pass over a ticket.

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
below the top level prints nothing and exits 0. The integration branch
is the one topic branches are cut from, as the project's instructions
name it; where they do not, the session asks once — a document's
`base:` cannot serve, since the lookup runs before the document
exists. `<ref>` is its remote-tracking ref (`origin/develop`) where
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
developer, who picks one of the existing directories; while one
exists, the question offers no new directory, which anti-goal 1 rules
out. Where no listed ticket has a directory, the developer picks the
ticket whose directory is created. A review command
asks before dispatch, a session before it writes the document.

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
without it — matched by a class suffix or lying in a class directory —
belongs to the developer, and the process neither adds frontmatter to
it nor reports it, as the glossary's *Process document* says.

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
`<ticket directory>/code-review/`.

The branch scheme lives in the workflow rule's *Branch naming*, which
always loads and already owns branch names; the review-reports and
ticket-frontmatter rules point to it. With `ticket.root` set, the
process reads a branch name as `[<type>/]<key>[-<slug>]`: an optional
single segment of any type (`feature/`, `bugfix/`, `hotfix/`), then a
key shape — letters, a hyphen and digits (`ABC-123`), or digits alone
(`42`, which the prefix rule turns into `ticket-42`) — then an optional
slug. `feature/ABC-123-login`, `bugfix/ABC-1-x`, `ABC-123` and
`hotfix/42-crash` all fit. The section's "fixes the shape and not the
spelling" still holds: a project spells its keys as it likes, and the
process reads only the names that take this shape. Without
`ticket.root`, branch sourcing is unchanged.

In an interactive session a review places its report by this table:

| the branch name | the report goes to |
|---|---|
| fits the scheme, and the key's ticket directory exists | the ticket directory, no question |
| fits the scheme, no ticket directory (`feature/phase-2-cleanup`) | `docs/code-review/`, no question |
| carries a letters-hyphen-digits shape outside the scheme (`fix-for-ABC-123`, `release-ABC-123`) | asks for the ticket; an existing ticket directory for the answer takes the report, else `docs/code-review/` |
| carries no key shape (`feature/ticket-directories`) | `docs/code-review/`, no question |

Digits alone count as a key only at the scheme's key position, so
`feature/oauth2-login` or `chore/v1.2-migration` asks nothing. A run
with no interactive dispatcher writes to `docs/code-review/` whatever
the branch (D20). The one question is a named exception to the
review-reports rule's "a review run never blocks on a question", made
only in an interactive session.

The table decides placement only. The report's `ticket:` field derives
as the review-reports rule derives it today — from context or the
branch, else `none` — with the row-3 answer and the session's answer
about the branch counting as context. A review on `feature/ABC-77-login`
before the ticket's directory exists keeps `ticket: ABC-77` in
`docs/code-review/`; one on `feature/phase-2-cleanup` may carry
`ticket: PHASE-2` there, which creates nothing. A review never creates
a ticket directory: a ticket's directory appears with its first process
document.

The ticket-frontmatter rule sources a new document's ticket from the
branch name before the conversation, reading it by the same scheme.
With `ticket.root` set, a ticket read from the branch whose ticket
directory does not exist yet is stated and confirmed with the
developer before the document is written — `feature/phase-2-cleanup`
and `release/2026-10-27` fit the scheme and name no ticket. This is the
sourcing order's one question for the unit of work, never a second: a
declined confirmation falls through to the conversation and then to
`none`, never to another question. One answer about a branch's ticket
serves both rules for the rest of the session; nothing is recorded,
and a fresh session or a compaction may ask again. That sentence lives
in *Branch naming* beside the scheme, since the two rules that use the
answer load on different globs.

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
tracked mode, so no first-create question is asked, and a review that
writes there skips the `docs/code-review/` first-create check and the
local pocket. A numeric key from a branch fills `ticket:` as the
ticket-frontmatter rule writes it (`"#42"`), while its prefix is
`ticket-42`. A solo run follows the same placement through the
review-reports rule, which its Contract probe reads; a standards
plugin installed without the working-process rules sees no
`ticket.root` and writes to `docs/code-review/`. A local-only
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
   convention gains its class suffix, and its topic is its name
   without a leading date and a trailing `-design`, or its whole stem
   where neither is there. A tracked file moves with `git mv`; an
   untracked one — uncommitted, or in an ignored class directory —
   with `mv`, and nothing is staged, since committing stays with the
   developer.
4. The session rewrites these references: inbound and outbound
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
5. References outside `docs/` and paths in body prose are listed,
   never rewritten.
6. The session reports every path it rewrote and every reference it
   left alone, and names each untracked file that now lies in the
   tracked ticket directory.

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
  on `bugfix/ABC-12-y` and one on `ABC-12`; one on
  `feature/phase-2-cleanup` writes to `docs/code-review/` without a
  question and creates no directory; one on `fix-for-ABC-12` asks, and
  "ABC-12" sends it to `abc-12-old/code-review/`.
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
  also the ticket-root exclusion; technical-design also its "lives in
  `docs/technical-designs/`" sentence, which a ticket directory
  overrides.
- `README.md` of working-process — the directories it lists.
- `rules/workflow.md` — where a ticket's documents go; the branch
  scheme and the shared session answer in *Branch naming*.
- `rules/ticket-frontmatter.md` — field sets by class; companion
  documents in a ticket directory exempt; branch sourcing by the D19
  scheme.
- `rules/review-reports.md` — ticket placement of reports, the one
  interactive question as an exception to "never blocks on a question",
  the `docs/**/code-review/**` glob.
- `scripts/decision-coverage.py`, `tests/working-process/test_decision_coverage.py`
  — the suffix test.
- `skills/process-status/SKILL.md` — the ticket directories in its
  description (*The setting*).
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
- D21 recomputes only hashes that matched before the move, so a move
  never stamps unaudited edits.
- D20: an unattended run, or an ambiguity nobody can answer, writes
  to `docs/code-review/`, matching the CI non-goal.
- A move stages nothing and names each untracked file that now lies
  in the tracked ticket directory.
- The loader refuses a `ticket.root` equal to or inside a Process
  directory.
- Several matching directories offer only the existing ones.
- The `status:` gate holds in class directories too.
- A numeric branch key fills `ticket:` as `"#42"`, with the prefix
  `ticket-42`.
- A review writing to a ticket directory skips the `docs/code-review/`
  first-create check and the local pocket; a standalone standards
  install writes to `docs/code-review/`.
- A legacy file's topic is its name without a leading date and a
  trailing `-design`.

## Review rounds

### 2026-10-27 — integrity audit, fable, at the consumption gate

- fixed 2026-10-27 — closures of the audit's dispositions, found after the stamp: D6 had no outcome for a ticket list none of whose tickets has a directory; D8 lagged the gate's extension to class directories; move steps 4 and 5 lagged D17; three wrapped lines; ruling: 2026-10-27; D6, *Placement*, D8 and steps 4–5 amended, the stamp's hash recomputed without a new audit

- fixed 2026-10-27 — D19 asked about any key shape outside the scheme, the body only about letters-hyphen-digits; license: R4-3; D19 narrowed
- fixed 2026-10-27 — D19's "gives no ticket" contradicted the report's `ticket:` field; license: R4-2's ruling; D19 speaks of placement and leaves the field to its derivation
- fixed 2026-10-27 — D17 promised every reference, the procedure lists some; license: *Moving a document*; D17 names what is rewritten and what is listed
- fixed 2026-10-27 — the integration-branch lookup read a `base:` of a document not yet written; license: *Recognising a process document* (the lookup precedes the write); the project's instructions or one question
- fixed 2026-10-27 — the integration-branch procedure and the declined-confirmation and session-answer rules had no register entry; license: the register's own rule; D22 and D23
- fixed 2026-10-27 — the process-status change had no argument; license: *The setting*; the description gains the ticket directories, argued there
- fixed 2026-10-27 — `rules/technical-design.md`'s location sentence was missing from *Changes by file*; license: *Placement*; listed, with the working-process README
- fixed 2026-10-27 — the move had no path for an uncommitted file in a tracked class directory; license: the lifecycle rule (documents stay uncommitted while authored); any untracked file moves with `mv`, nothing staged
- fixed 2026-10-27 — eight implementer questions answered as author's calls: the root's Process-directory guard, existing-only choice on several matches, the gate in class directories, numeric keys, skipped checks in a ticket directory, solo and standalone runs, legacy topics, the README

### 2026-10-27 — architect, fable 5.1, concerns (round 4, diff-scoped)

- fixed 2026-10-27 — [Minor] R4-1: D14 placed a report only by the branch's ticket, while row 3 places it by the developer's answer; license: D19; D14 adds "or the developer names for it (D19)"
- fixed 2026-10-27 — [Minor] R4-2: the report's `ticket:` field was undefined for rows 1, 2 and 4; ruling: 2026-10-27; option (i) — the table decides placement only, the field derives as today with the row-3 and session answers as context
- fixed 2026-10-27 — [Minor] R4-3: "digits alone" made row 3 ask on `feature/oauth2-login`; license: R3-2's ruling (a name that suggests a ticket); row 3 counts only the letters-hyphen-digits shape, and digits alone count only at the key position
- fixed 2026-10-27 — [Minor] R4-4: no rule owned the shared session answer; license: R3-1 (the always-loaded owner); the sentence lives in *Branch naming*, listed in *Changes by file*

Resolved without a fresh round: four single-sentence fixes; no decision moved beyond R4-2's ruling.

### 2026-10-27 — architect, fable 5.1, blocking (round 3, diff-scoped)

- fixed 2026-10-27 — [Important] R3-1: the branch scheme sat in review-reports, while the workflow rule's *Branch naming* owns branch names and ticket-frontmatter defers to it; license: D19 ("one definition"); the scheme moves to *Branch naming*, reconciled with "fixes the shape and not the spelling", and the other two rules point to it
- fixed 2026-10-27 — [Important] R3-2: row 2's question changed nothing, and review-reports says a review never asks; ruling: 2026-10-27; option (a) — row 2 goes to `docs/code-review/` without a question, the one remaining question (row 3) is a named interactive exception whose answer also sets the report's `ticket:`
- fixed 2026-10-27 — [Minor] R3-3: the table's unattended column sent row 1 to the ticket directory against D20; license: D20 and the CI non-goal; the column is replaced by one sentence
- fixed 2026-10-27 — [Minor] R3-4: `jan/abc-123-fix` fits the scheme yet was listed outside it; license: D19; the example is `fix-for-ABC-123`
- fixed 2026-10-27 — [Minor] R3-5: no fall-through after a declined confirmation, and no shared answer between the two rules; license: ticket-frontmatter's "never ask twice"; a decline falls through to the conversation and `none`, and one answer serves both rules for the session
- fixed 2026-10-27 — [Minor] R3-6: the scheme changed branch sourcing in projects without `ticket.root`; license: goal 4; the scheme applies only with `ticket.root` set

### 2026-10-27 — architect, fable 5.1, concerns (round 2, diff-scoped)

- fixed 2026-10-27 — [Minor] R2-1: F1's fix put the lookup duty in the always-loaded workflow rule but left its commands in the lifecycle rule, which loads too late; license: D11; the workflow clause ends by requiring a read of the spec-plan-lifecycle rule before creating a ticket directory, the pattern the workflow rule already uses for a plan-writing brief
- fixed 2026-10-27 — [Minor] R2-2: the glossary's *Dispatch record* still located a review report under `docs/code-review/`; license: D18 and F3; the appositive names no location
- fixed 2026-10-27 — the reviewer's integrity note: D14 sent a local-only report to the ticket directory, and D20 had a solo run hand an agent the path; license: F2's ruling and F8; D14 excepts local-only reports, D20 separates the dispatched and the solo run

Resolved without a fresh round: both findings and the note are wording; no decision moved.

- fixed 2026-10-27 — D19 read a ticket only after `feature/`, so `bugfix/ABC-1-x` or a bare `ABC-123` branch lost its ticket; ruling: 2026-10-27; D19 and *Review reports* define the scheme `[<type>/]<key>[-<slug>]`, ask about a name outside it or without a ticket directory, and the ticket-frontmatter rule's branch sourcing reads the same scheme
- fixed 2026-10-27 — the branch-sourced ticket of a new document had no guard, so `feature/phase-2-cleanup` would give a spec `ticket: PHASE-2` and create its directory; ruling: 2026-10-27; with `ticket.root` set, a branch ticket without a ticket directory is confirmed before the document is written (D19, *Review reports*)

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
