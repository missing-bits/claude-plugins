---
ticket: none
date: 2026-10-27
status: draft
spec: ../specs/2026-10-27-ticket-directories-spec.md
branch: feature/ticket-directories
base: develop
---

# Ticket directories Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land `docs/specs/2026-10-27-ticket-directories-spec.md` — the
opt-in `ticket.root` key with a path-valued shape, ticket-directory
placement and lookup, class detection by suffix with the `status:` gate,
the move procedure, the branch-name scheme, and review-report placement
in working-process and both standards plugins.

**Architecture:** One code change carries a test cycle each: the
settings loader learns a `<path>` value token, and
`decision-coverage.py` learns the `-technical-design.md` suffix. Every
other deliverable is rule, skill, command or agent prose; its test is
the check block the task publishes (a `grep` that fails before the edit
and passes after), plus `claude plugin validate`. A scratch-project
dogfood closes the plan.

**Tech Stack:** POSIX `sh` and `awk` (`scripts/load-settings.sh`);
Python 3.9+ `unittest` (`tests/working-process/`); Markdown rules,
skills, commands and agent cards; `grep`, `git`, `claude plugin
validate`, and `claude --plugin-dir` for the dogfood.

**Spec:** `docs/specs/2026-10-27-ticket-directories-spec.md`

## Global Constraints

- **The spec is the source.** Where this plan and the spec disagree,
  the spec wins.
- **Realizes:** D1 — **A project without `ticket.root` behaves as
  today.** Every rule sentence this plan adds opens with, or sits under,
  "With `ticket.root` set"; no existing behaviour changes for an unset
  key.
- **Realizes:** D18 — **The glossary is already amended** (grilling
  session and fix waves, commits on this branch). No task edits
  `docs/domain/glossary.md`; every task uses its terms verbatim: ticket
  root, ticket directory, process document, companion document, class
  suffix, class directory.
- **Realizes:** D7 — **Rules branch on the class, never on a file
  pattern.** Prose says "a design spec", "a technical design", "a
  plan"; a suffix appears only where detection is described.
- **Key citation.** A file that starts citing `ticket.root` adds itself
  to that key's `read-by:` in `SETTINGS_REGISTRY.md` in the same task,
  so `test_settings_registry.py` stays green after every task.
- **No version bump.** Each changed plugin gets a line under
  `## Unreleased` in its `CHANGELOG.md` (Task 8); versions move only in
  the release PR.
- **English, repo hygiene.** No machine paths, no client names; the
  client project's directory appears only as `docs/jira/abc-…` examples.
- **Never read a credential's value or write one into a command.**

## Review Focus

1. A `ticket.root` of `docs/specs` or `docs/code-review/x` — the loader
   must refuse it (Task 1, cases in `test_load_settings.py`).
2. A lookup run from a subdirectory — the rule must prescribe
   `--full-tree` and the top level, or it silently misses (Task 3 check
   block greps both).
3. A companion document named `*-spec.md` without `status:` — no rule
   may add frontmatter to it (Task 3 gate sentence; Task 9 dogfood).
4. A branch `feature/phase-2-cleanup` in a project with `ticket.root` —
   a review asks nothing and creates no directory; a new spec confirms
   the ticket first (Tasks 5, 6, 7a; Task 9 dogfood).
5. A move of an uncommitted spec — `git mv` refuses an untracked file;
   the procedure must use `mv` and stage nothing (Task 4; Task 9).

---

### Task 1: `ticket.root` — registry entry, path validation, process-setup

**Realizes:** D1, D2

**Files:**
- Modify: `plugins/working-process/SETTINGS_REGISTRY.md` (preamble; new
  `## ticket.root` entry after `review.per-round-commit`)
- Modify: `plugins/working-process/scripts/load-settings.sh` (the awk
  `valid_value` at :207 and the `do_set` value check at :775-784)
- Modify: `plugins/working-process/skills/process-setup/SKILL.md`
- Test: `tests/working-process/test_settings_registry.py`,
  `tests/working-process/test_load_settings.py`

**Interfaces:**
- Produces: registry entry —
  `scope: team` · `values: <path>` · `default: unset` ·
  `read-by: working-process/skills/process-setup/SKILL.md` ·
  `question: Which directory under docs/ holds one directory per ticket, if the project keeps them?`
- Produces: the token `<path>` as the registry's one non-enumerated
  value, accepted by the loader when the value starts with `docs/`, has
  a segment after it, has no `..` segment and no trailing `/`, and
  neither equals nor lies inside `docs/specs`, `docs/technical-designs`,
  `docs/plans`, `docs/domain`, `docs/code-review` or `docs/memory`.

- [ ] **Step 1: Write the failing tests.**
  In `test_settings_registry.py`: rename `test_fourteen_keys_in_order`
  to `test_fifteen_keys_in_order` and append `"ticket.root"`; in
  `test_every_entry_is_well_formed`, accept `fields["values"] == "<path>"`
  as the one non-enumerated shape (skip the value regex and the
  default-in-values check for it). In `test_load_settings.py`, append
  `"ticket.root"` to `KEYS` (:23, registry order), and add
  `test_ticket_root_path_values`, using `--set ticket.root <v>` then
  reading the block:
  - `docs/jira` → exit 0, block line `ticket.root: docs/jira  [team]`;
  - `docs/tickets/active` → exit 0;
  - `jira`, `docs`, `docs/`, `docs/jira/`, `docs/../jira`,
    `docs/specs`, `docs/code-review/x` → `--set` exits 1 with
    ``error: invalid value for `ticket.root` `` on stderr;
  - the same invalid values written by hand into `settings.md` → block
    shows `ticket.root: unset  [invalid in team]` and an `error:` line.
- [ ] **Step 2: Run** `python3 -m unittest tests/working-process/test_settings_registry.py tests/working-process/test_load_settings.py`
  — expect failures in `test_fifteen_keys_in_order`,
  `test_precedence_and_defaults` (the block still has fourteen keys)
  and `test_ticket_root_path_values`, and nowhere else.
- [ ] **Step 3: Implement.**
  Registry: add the entry above; in the preamble, say `values:` is
  either ` | `-separated values or the token `<path>`, defined there.
  Loader: in awk, `valid_value(val, padded)` returns
  `valid_path(val)` when `padded == " <path> "`; add
  `valid_path(val)` beside it. In `do_set`, when the normalised values
  are `<path>`, call a POSIX shell `path_value_ok "$s_value"` with the
  same rules instead of the enumeration loop. The error text stays as
  today, with `(allowed: <path>)`.
  Skill: where process-setup asks a key's question, a key whose
  registry `values:` is `<path>` takes a free-text answer, offered with
  "leave unset" first; cite `ticket.root` by name.
- [ ] **Step 4: Run** the two test files — expect all pass; then
  `python3 -m unittest discover -s tests -p 'test_*.py'` — expect all
  pass.
- [ ] **Step 5: Commit** `feat(working-process): ticket.root settings key with a path value`.

### Task 2: `decision-coverage.py` recognises a technical design by suffix

**Realizes:** D13

**Files:**
- Modify: `plugins/working-process/scripts/decision-coverage.py:556-560`
- Test: `tests/working-process/test_decision_coverage.py`

**Interfaces:**
- Produces: `is_technical_design(display: str) -> bool` — true when a
  parent pair is `docs/technical-designs` **or** the file name ends in
  `-technical-design.md`.

- [ ] **Step 1: Write the failing test** `test_13b_technical_design_in_ticket_directory_produces_no_output`:
  the fixture of `test_13`, with the design at
  `docs/jira/abc-12-x/abc-12-x-technical-design.md` and `spec:
  ../../specs/s.md`; assert exit 0, empty stdout, empty stderr.
- [ ] **Step 2: Run** `python3 -m unittest discover -s tests/working-process -p test_decision_coverage.py -k 13b`
  — expect FAIL: the design is audited as a plan and prints hits.
- [ ] **Step 3: Implement** the suffix clause in `is_technical_design`;
  update its docstring.
- [ ] **Step 4: Run** the whole file — expect all pass.
- [ ] **Step 5: Commit** `feat(working-process): decision coverage recognises a technical design by its suffix`.

### Task 3: Rules — suffix globs, placement, lookup, gate, links, modes

**Realizes:** D3, D4, D5, D6, D7, D8, D10, D12, D22

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md`
  (frontmatter `paths:`; the naming paragraph near the top; the
  frontmatter-links examples)
- Modify: `plugins/working-process/rules/technical-design.md`
  (`paths:`; the "lives in `docs/technical-designs/`" sentence)
- Modify: `plugins/working-process/rules/propagation-duties.md` (`paths:`)
- Modify: `plugins/working-process/rules/process-artifacts.md`
  (`paths:`; one sentence on the ticket root)
- Modify: `plugins/working-process/SETTINGS_REGISTRY.md` (`read-by:` of
  `ticket.root` gains the files above that cite it)

**Interfaces:**
- Consumes: `ticket.root` (Task 1).
- Produces: the section *Ticket directories* in
  `spec-plan-lifecycle.md`, which Tasks 4, 5 and 7 point to by that
  name; it holds placement, the lookup commands and the gate.

- [ ] **Step 1: Write the check block** (save as
  `/tmp/…/t3-check.sh` in the session's scratch directory) and run it —
  expect every line to fail:
  - `grep -q 'docs/\*\*/\*-{spec,technical-design,plan}.md' rules/{spec-plan-lifecycle,propagation-duties,process-artifacts}.md`
  - `grep -q 'docs/\*\*/\*-technical-design.md' rules/technical-design.md`
  - `grep -q '^## Ticket directories' rules/spec-plan-lifecycle.md`
  - `grep -q -- '--full-tree -d --name-only' rules/spec-plan-lifecycle.md`
  - `grep -q 'git rev-parse --show-toplevel' rules/spec-plan-lifecycle.md`
  - `sed -n '/^## Ticket directories/,/^## [^T]/p' rules/spec-plan-lifecycle.md | grep -q 'status:'`
  - `grep -q 'ticket root' rules/process-artifacts.md`
- [ ] **Step 2: Edit.** Add the glob lines per the spec's
  *Recognising a process document* table, keeping every directory
  glob. In `spec-plan-lifecycle.md`, add `## Ticket directories` after
  the naming paragraph, carrying, in the spec's words: placement under
  `<root>/<prefix>-<topic>/` (D3); the case-insensitive `<prefix>-`
  lookup with the trailing hyphen, from the top level and with
  `git ls-tree --full-tree -d --name-only <ref> <root>/` on the
  integration branch, its remote-tracking ref first, no fetch, ask once
  where the project's instructions name no branch (D4, D22); new
  directory case and topic (D5); several matches or several tickets,
  including the no-directory case (D6); the `status:` gate in class
  suffixes and class directories alike (D8); "frontmatter links are
  relative to the document" with the sibling and `../../specs/`
  examples (D12). In `technical-design.md`, replace the location
  sentence with one deferring to *Ticket directories* when
  `ticket.root` is set. In `process-artifacts.md`, one sentence: the
  ticket root and its ticket directories are not Process directories —
  tracked, no first-create question, no `.gitignore` written, no
  `dir.*` key, project ignores respected, never force-added (D10).
- [ ] **Step 3: Run** the check block — expect every line to pass; run
  `python3 -m unittest tests/working-process/test_settings_registry.py`
  — expect pass.
- [ ] **Step 4: Run** `claude plugin validate plugins/working-process` —
  expect "Validation passed".
- [ ] **Step 5: Commit** `feat(working-process): ticket directories in the document rules`.

### Task 4: The move procedure

**Realizes:** D15, D16, D17, D21

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` (new
  `### Moving a document into a ticket directory` under *Ticket
  directories*)

**Interfaces:**
- Consumes: *Ticket directories* (Task 3); the hash command
  `sed '1,/^---$/d' <file> | shasum | cut -c1-7` already in the rule.

- [ ] **Step 1: Write the check block** and run it — expect failure.
  With `S='/^### Moving a document into a ticket directory/,/^##/p'`,
  each of `git mv`, `nothing is staged`, `implemented`,
  `listed, never rewritten` and `matched its body before the move`
  must pass `sed -n "$S" rules/spec-plan-lifecycle.md | grep -q '<phrase>'`.
- [ ] **Step 2: Edit.** Write the six steps of the spec's *Moving a
  document* as the procedure, on the developer's command only (D15):
  ticket source; the chain by `spec:`, `technical-design:`,
  `revises:`, `**Follows:**`, offered as one move (D16); naming and the
  legacy topic rule; `git mv` for tracked, `mv` for untracked, nothing
  staged; the rewritten references, the listed ones, the stop before a
  body edit to an `implemented` document (D17); the hash recompute only
  where it matched before (D21); the report.
- [ ] **Step 3: Run** the check block — expect pass.
- [ ] **Step 4: Commit** `feat(working-process): move a document into a ticket directory`.

### Task 5: Workflow rule — placement guard and branch scheme

**Realizes:** D11, D19, D22, D23

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` (the
  "where documents go" lines in the flow, ~:9 and ~:128; *Branch
  naming*, ~:233)
- Modify: `plugins/working-process/SETTINGS_REGISTRY.md` (`read-by:`)

**Interfaces:**
- Consumes: *Ticket directories* (Task 3).
- Produces: *Branch naming* holds the scheme `[<type>/]<key>[-<slug>]`
  and the session-answer sentence; Tasks 6 and 7 point to it.

- [ ] **Step 1: Write the check block** and run it — expect failure:
  `grep -q '\[<type>/\]<key>\[-<slug>\]' rules/workflow.md`;
  `grep -q 'read the spec-plan-lifecycle rule before creating a ticket directory' rules/workflow.md`;
  `grep -q 'fixes the shape and not the spelling' rules/workflow.md`
  (must still pass — the sentence stays).
- [ ] **Step 2: Edit.** The placement clause per the spec's
  *Recognising a process document*: with `ticket.root` set and a
  ticket, reuse the root's subdirectory starting with `<prefix>-`
  (ignoring case, working tree or integration branch), several to the
  developer, a new `<root>/<prefix>-<topic>/` only with none, and
  require reading the spec-plan-lifecycle rule before creating a ticket
  directory (D11). In *Branch naming*, add under "With `ticket.root`
  set": the scheme and key shapes, digits alone only at the key
  position, the reconciliation with "fixes the shape and not the
  spelling" (D19); the integration branch named by the project's
  instructions or asked once (D22); a declined confirmation falling
  through to the conversation and `none`, one answer per branch per
  session, nothing recorded (D23).
- [ ] **Step 3: Run** the check block — expect pass; registry test —
  expect pass.
- [ ] **Step 4: Commit** `feat(working-process): ticket placement and the branch scheme in the workflow rule`.

### Task 6: Ticket-frontmatter rule

**Realizes:** D9, D19, D23

**Files:**
- Modify: `plugins/working-process/rules/ticket-frontmatter.md`
  (*Field sets*; *Sourcing and backfill*, ~:51-60)
- Modify: `plugins/working-process/SETTINGS_REGISTRY.md` (`read-by:`)

**Interfaces:**
- Consumes: *Branch naming* (Task 5).

- [ ] **Step 1: Write the check block** and run it — expect failure:
  `grep -q 'companion document' rules/ticket-frontmatter.md`;
  `grep -q 'Branch naming' rules/ticket-frontmatter.md`;
  `grep -q 'confirm' rules/ticket-frontmatter.md`.
- [ ] **Step 2: Edit.** *Field sets*: the process-document set is
  chosen by class (class suffix or class directory), not by
  directory; a companion document in a ticket directory is exempt from
  `ticket` and `date` and its own frontmatter is left untouched (D9).
  *Sourcing and backfill*: with `ticket.root` set, the branch is read by
  *Branch naming*'s scheme, and a branch ticket whose ticket directory
  does not exist yet is stated and confirmed before the document is
  written — the order's one question (D19, D23). The backfill sentence
  exempts companion documents in a ticket directory.
- [ ] **Step 3: Run** the check block and the registry test — expect pass.
- [ ] **Step 4: Commit** `feat(working-process): ticket-frontmatter for ticket directories`.

### Task 7a: Review-report placement in working-process

**Realizes:** D14, D19, D20

**Files:**
- Modify: `plugins/working-process/rules/review-reports.md` (`paths:`;
  location; the `ticket` field line ~:79-81; *Local pocket* ~:230)
- Modify: `plugins/working-process/skills/process-status/SKILL.md`
  (`description:`)
- Modify: `plugins/working-process/README.md` (the directories it lists)
- Modify: `plugins/working-process/SETTINGS_REGISTRY.md` (`read-by:`
  gains `review-reports.md`)

**Interfaces:**
- Consumes: *Branch naming* (Task 5), *Ticket directories* (Task 3).
- Produces: the rule's placement section, which Task 7b's commands
  follow; the report directory reaches an agent as an absolute path in
  its dispatch prompt.

- [ ] **Step 1: Write the check block** and run it — expect each to fail:
  `grep -q 'docs/\*\*/code-review/\*\*' rules/review-reports.md`;
  `grep -q 'feature/phase-2-cleanup' rules/review-reports.md`;
  `grep -q 'fix-for-ABC-123' rules/review-reports.md`;
  `grep -q 'ticket directories' skills/process-status/SKILL.md`.
- [ ] **Step 2: Edit.** The placement rule and table for an
  interactive session, the unattended fallback, local-only reports to
  `docs/code-review/`, the skipped first-create check and pocket in a
  ticket directory, numeric keys as `"#42"`, solo runs through the
  Contract probe, standalone installs to `docs/code-review/`; the
  `ticket` field line derives as today with the row-3 and session
  answers as context, and names the one interactive question as the
  exception to "never blocks on a question" (D14, D19, D20). The
  process-status `description:` names ticket directories beside the
  class directories; the README lists the ticket root.
- [ ] **Step 3: Run** the check block, the full test suite and
  `claude plugin validate plugins/working-process` — expect pass.
- [ ] **Step 4: Commit** `feat(working-process): review reports in ticket directories`.

### Task 7b: Review commands of the standards plugins

**Realizes:** D20

**Files:**
- Modify: `plugins/python-standards/commands/python-review.md`,
  `plugins/python-standards/agents/python-code-reviewer.md`,
  `plugins/python-standards/skills/python-code-review/SKILL.md` (:104),
  `plugins/python-standards/README.md`
- Modify: the salesforce-standards counterparts (command, agent,
  `skills/salesforce-code-review/SKILL.md` :165, README)
- Modify: `plugins/working-process/SETTINGS_REGISTRY.md` (`read-by:`
  gains the two commands)

**Interfaces:**
- Consumes: the review-reports placement section (Task 7a).

- [ ] **Step 1: Write the check block** and run it — expect each to fail:
  `grep -q 'ticket.root' plugins/{python,salesforce}-standards/commands/*-review.md`;
  `grep -q 'writes the review report to docs/code-review/' plugins/{python,salesforce}-standards/agents/*.md`
  must **pass** before and **fail** after (the only-location claim is
  gone).
- [ ] **Step 2: Edit.** Each command resolves the directory before
  dispatch — working tree only, `ticket.root` from the settings block,
  per the review-reports rule — and passes it in the prompt; each agent
  writes to the directory the prompt names; each code-review skill's
  *Location* says "the directory the run resolved: `docs/code-review/`,
  or a ticket directory's `code-review/`"; each README follows.
- [ ] **Step 3: Run** the check block, the full test suite, and
  `claude plugin validate` on both standards plugins — expect pass.
- [ ] **Step 4: Commit** `feat: standards review commands place reports in ticket directories`.

### Task 8: Changelogs

**Realizes:** none

**Files:** `plugins/{working-process,python-standards,salesforce-standards}/CHANGELOG.md`

- [ ] **Step 1:** Add one line under `## Unreleased` per plugin: the
  opt-in `ticket.root` and what it moves (working-process); review
  reports in ticket directories (both standards plugins).
- [ ] **Step 2: Commit** `docs: changelog entries for ticket directories`.

### Task 9: Dogfood

**Realizes:** none

**Files:** none in the repo; the record goes to
`.claude/working-process/2d-ticket-directories/dogfood.md`.

- [ ] **Step 1:** Build a scratch git project (develop as integration
  branch, `ticket.root: docs/jira` in `.working-process/settings.md`,
  `docs/jira/abc-12-old/` with a `screens-spec.md` lacking `status:`).
  Rules load from installed copies, not from the plugin, so copy this
  branch's `plugins/working-process/rules/*.md` into the scratch
  project's `.claude/rules/working-process/`, and run every session
  with a temporary `CLAUDE_CONFIG_DIR`, so no user-level rule loads,
  and with `claude --plugin-dir` on this branch's three plugins. Before
  the cases, ask a session to quote the spec-plan-lifecycle rule's
  *Ticket directories* heading; no quote, no dogfood.
- [ ] **Step 2:** Run every case of the spec's *Verification* dogfood
  bullet, and the Review Focus items 3–5; record each prompt, the
  resulting tree (`find docs -type f`) and pass or fail.
- [ ] **Step 3:** Repeat the ticketless flow in a project without
  `ticket.root`: documents land in the class directories.
- [ ] **Step 4:** Report failures to the developer before any fix;
  a fix is a new task.
