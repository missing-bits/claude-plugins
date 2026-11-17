---
ticket: none
date: 2026-11-17
status: approved
adversary: blocking (adjudicated 2026-11-17)
spec: ../specs/2026-11-17-document-check-spec.md
branch: feature/document-check
base: develop
---

# Document check Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `wp-document-check` and `wp-decision-coverage` behind one launcher, and make the dispatcher run them before the propagation auditor at every gate.

**Architecture:** One bash launcher, copied per command, picks `scripts/<name>.py` by its own file name and the first Python 3.9+. A new standard-library script runs two Document checks on every design spec, technical design and plan, and table closure on a technical design. The gate procedure, the auditor's card and every shipped sentence describing the old arrangement change to put the scripts in the dispatcher's hands.

**Tech Stack:** Python 3.9+ standard library, bash, `unittest`; Markdown rules, agent cards and skill references.

**Spec:** `docs/specs/2026-11-17-document-check-spec.md` (approved, `integrity:` d31a3a4). Read it whole before Task 1; this plan cites its decisions and does not restate their arguments.

## Global Constraints

- Python 3.9+, standard library only; no third-party import anywhere.
- Every hit line has the shape `<file:line> — <claim> — check: <name>`, `<name>` one of `references`, `citations`, `table-closure`.
- Exit codes of `document-check.py`: 0 when the Document checks ran, hits or not; 1 when the document cannot be read; 2 on a usage error.
- **Realizes:** D2 — A hit only where the parse settles the defect; every unsettled form is counted on a `not checked` summary line.
- **Realizes:** D15 — Under `## Review rounds` the Document checks read only the lines below the last `### ` round heading.
- Committed text is English, no machine paths, no client names (repo-hygiene rule).
- Verification checks over text take the `wp-phrase-check` form the plan-authoring rule gives, run on each side of their step; where the command is not on `PATH`, run `python3 plugins/working-process/scripts/phrase-check.py` with the same arguments.
- Commits: one line, conventional-commit prefix, no body, no trailer.
- The plugin version becomes `0.20.0-dev.11.document-check` (Task 7).

**Deviation from the spec, recorded here:** *Settled for the plan* says the launcher reads its name "before resolving symlinks". The shipped test `test_symlinked_launcher_finds_script` invokes the launcher through a link named `link`, which that reading would break. The launcher reads its name from the resolved file instead, so a link of any name works and each copy in `bin/` still names its own script. The call was the session's; it changes nothing D4 decides.

## Review Focus

1. A document with no frontmatter, or one whose frontmatter never closes — the script must still run and type it as a design spec, never crash.
2. A `path:line` whose file exists but is binary or not UTF-8 — read with `errors="replace"`, never a traceback.
3. CRLF line endings — headings and table rows must parse as with LF.
4. A Windows checkout of `bin/` — copies must stay byte-identical and executable; a test pins both.
5. A technical design whose Parts table is absent — `table-closure` prints `not applicable`-style counts (0 relations), never a hit for a missing table.

---

### Task 1: One launcher for every Python script

**Files:**
- Modify: `plugins/working-process/bin/wp-phrase-check`
- Create: `plugins/working-process/bin/wp-decision-coverage`
- Create: `tests/working-process/test_wp_launcher.py`
- Delete: `tests/working-process/test_wp_phrase_check_launcher.py` (its tests move into the new file unchanged)

**Interfaces:**
- Produces: `bin/wp-<name>` runs `scripts/<name>.py`; `<name>` is the resolved file name without its `wp-` prefix. The no-Python message reads `wp-<name>: no Python 3.9 or later found; tried: …` and exits 2.

**Realizes:** D4, D5

- [ ] **Step 1: Move the launcher tests and add three.** Create `test_wp_launcher.py` holding every test of the old file, with `LAUNCHER` kept as the phrase-check launcher, plus:
  - `test_bin_copies_are_identical` — every file in `bin/` has the same bytes and the executable bit (`os.access(p, os.X_OK)`).
  - `test_each_launcher_has_its_script` — for every `bin/wp-<name>`, `scripts/<name>.py` exists.
  - `test_decision_coverage_launcher_runs` — with the `GOOD` python3 stub, `bin/wp-decision-coverage <a design spec fixture with decisions: registered and one register entry>` exits 0 and prints a line starting `decision-coverage:`.
  Delete the old file.

- [ ] **Step 2: Observe the change absent.** Run `cd tests/working-process && python3 -m unittest test_wp_launcher` before Step 3 and record what it prints. `test_decision_coverage_launcher_runs` must fail; if it passes, stop as blocked. The two structural tests pass on today's one-file `bin/` — they guard copies, not this change — so prove them after Step 3 instead: flip one byte of `bin/wp-decision-coverage`, and separately rename `scripts/decision-coverage.py`, run them, record that each fails, and restore both.

- [ ] **Step 3: Generalise `bin/wp-phrase-check`.** After the symlink loop resolves `self`, set `name="${self##*/}"; name="${name#wp-}"`; the script path becomes `"$dir/../scripts/$name.py"`, the error message's prefix `wp-$name`, and the header comment names `scripts/<name>.py`. Copy the file to `bin/wp-decision-coverage` byte for byte, mode 100755 (`git update-index --chmod=+x` if the filesystem loses it).

- [ ] **Step 4: Run the launcher tests and the whole suite** — all pass, including the moved symlink test.

- [ ] **Step 5: Commit** — `feat(working-process): one launcher serves every Python script`

### Task 2: `document-check.py` — skeleton, document type, internal references

**Files:**
- Create: `plugins/working-process/scripts/document-check.py`
- Create: `plugins/working-process/bin/wp-document-check` (copy of the Task 1 launcher)
- Create: `tests/working-process/test_document_check.py`

**Interfaces:**
- Consumes: the Task 1 launcher.
- Produces: `main(argv: list[str]) -> int`; `doc_type(path: str, frontmatter: dict[str, str]) -> str` returning `"technical-design"`, `"plan"` or `"spec"`; `body_lines(text: str) -> list[tuple[int, str]]` — 1-based line numbers of lines outside fenced blocks, below the frontmatter, and under `## Review rounds` only below its last `### ` heading (D15) — with no `### ` heading yet, the whole section; a frontmatter that never closes is treated as absent, the body starting at line 1; `Report` holding hits and per-check `checked`/`not checked` counters, printed hits first, then exactly three summary lines in the order `references`, `citations`, `table-closure`.

**Realizes:** D1, D3

- [ ] **Step 1: Write the failing tests** in `test_document_check.py`, each a temporary repo (`git init` in a temp dir) and a document written into it:
  - `test_type_by_path_then_frontmatter` — `docs/technical-designs/x.md` with `spec:` → `technical-design`; `docs/tickets/A-1-x/A-1-x-technical-design.md` → `technical-design`; `docs/plans/p.md` with `spec:` → `plan`; a file without `spec:` → `spec`; a file without frontmatter → `spec`.
  - `test_named_section_wrong_side_is_hit` — `*Gamma* below` where `## Gamma` sits above → one hit, `check: references`.
  - `test_named_section_right_side_is_clean` — the clean twin.
  - `test_unknown_name_is_not_checked` — `*Nowhere* below` → no hit, `references` not-checked count 1.
  - `test_plan_task_reference` — a plan citing `Task 3` with only `### Task 1` and `### Task 2` → one hit; adding `### Task 3:` → none.
  - `test_bare_below_and_step_are_not_checked` — "see below", "Step 2", "§4" → no hit, three not checked.
  - `test_ledger_reads_last_round_only` — a citation-free wrong-side reference under an earlier `### ` round heading → no hit; the same under the last heading → one hit; the same in a `## Review rounds` with no `### ` heading → one hit.
  - `test_fenced_block_ignored` and `test_crlf_document` (Review Focus 3).
  - `test_no_frontmatter_and_unclosed_frontmatter` (Review Focus 1) — exit 0, three summary lines; with an unclosed `---`, a wrong-side reference after it → one hit.
  - `test_exit_codes` — missing file → 1; no argument → 2.
  - `test_summary_lines_shape` — stdout ends with three lines matching `^document-check: (references|citations|table-closure) `.
  Matching: a name and a heading compare after `wp-phrase-check`'s normalisation (load `normalise` from `scripts/phrase-check.py` with `importlib.util.spec_from_file_location`; no test imports it today, they run it by subprocess), at any heading level, ignoring a leading section number (`3.2 `); "beside" means the name and `below`/`above` sit in one sentence. Name the side by heading line versus citing line; a name matching more than one heading is not checked (add `test_duplicate_heading_not_checked`).

- [ ] **Step 2: Observe them fail** with the script absent; record what each prints. Stop as blocked if any passes.

- [ ] **Step 3: Implement** the functions above; `citations` and `table-closure` report zero counts for now (`table-closure` prints `not applicable` on a non-technical design). Copy the launcher to `bin/wp-document-check` (byte-identical, 100755), and add `test_document_check_launcher_runs` to `test_wp_launcher.py`: with the `GOOD` stub, `bin/wp-document-check <a spec fixture>` exits 0 and prints three `document-check:` summary lines.

- [ ] **Step 4: Run** `test_document_check.py` and `test_wp_launcher.py` — pass.

- [ ] **Step 5: Commit** — `feat(working-process): wp-document-check with the internal-references check`

### Task 3: Citations and link targets

**Files:**
- Modify: `plugins/working-process/scripts/document-check.py`
- Modify: `tests/working-process/test_document_check.py`

**Interfaces:**
- Consumes: `body_lines`, `Report`, `doc_type` from Task 2.
- Produces: `check_citations(path: str, lines: list[tuple[int, str]], report: Report, root: str, created: set[str]) -> None`.

**Realizes:** D9

- [ ] **Step 1: Write the failing tests**, each with its clean twin:
  - `test_path_line_outside_file` — `` `sub/a.md:9` `` against a 3-line `sub/a.md` → hit; `:3` → none; `:2-3` → none; `:2-4` → hit.
  - `test_symbol_on_cited_line` — `` `alpha` (sub/a.md:2) `` where line 2 lacks `alpha` → hit; holds it → none.
  - `test_missing_file_rule` — `sub/missing.md:1` with `sub/` present → hit; `nodir/missing.md:1` → not checked; bare `missing.md:1` → not checked; in a plan, `` - Create: `sub/missing.md` `` above → not checked.
  - `test_link_target` — `[x](sub/missing.md)` with `sub/` present → hit; `[x](https://e.org)`, `[x](#anchor)` and `[x](sub/a.md#sec)` → not checked; an existing target → checked, no hit.
  - `test_backticked_path_without_line_never_hits` — `` `sub/missing.md` `` → not checked, on spec, plan and technical design alike.
  - `test_git_ignored_path_resolves` — a file listed in `.gitignore` that exists → checked, no hit.
  - `test_license_quote` — `license: "foo bar" sub/a.md:2` where line 2 reads `Foo\nbar` across a wrap within the window lines 2–4 → none; a quote absent from the file → hit; a quote with no location → not checked; the same three cases with `ruling:` in place of `license:` → the same results; a quote followed by an `*italic*` naming no heading of the document → not checked. The check reads both `license:` and `ruling:` clauses. Location precedence: first `path:line`, path, or `*italic heading*` after the quote; a `path:line` is searched in lines `line` to `line+2`, a path in the whole file, a heading in its section.
  - `test_binary_target` (Review Focus 2) — a non-UTF-8 file cited by `path:line` → no traceback, counted.
  Paths resolve against the document's directory, then the repository root (`git rev-parse --show-toplevel`, falling back to the current directory).

- [ ] **Step 2: Observe them fail**; record the output. Stop as blocked if any passes.

- [ ] **Step 3: Implement** `check_citations`; read cited files with `encoding="utf-8", errors="replace"`.

- [ ] **Step 4: Run** the test file — pass.

- [ ] **Step 5: Commit** — `feat(working-process): document-check citations and link targets`

### Task 4: Table closure

**Files:**
- Modify: `plugins/working-process/scripts/document-check.py`
- Modify: `tests/working-process/test_document_check.py`

**Interfaces:**
- Consumes: `body_lines`, `Report`, `doc_type`.
- Produces: `declared_relations(rule_path: str) -> list[tuple[str, str, bool, str, str]]` — (table, column, each_side, target table, target column) parsed from the rule's `## Declared table relations` table; `check_tables(path: str, lines: list[tuple[int, str]], report: Report, relations: list[tuple[str, str, bool, str, str]]) -> None`. The rule path is `<script dir>/../rules/technical-design.md`.

**Realizes:** D10

- [ ] **Step 1: Write the failing tests:**
  - `test_relations_read_from_plugin_rule` — `declared_relations` on the shipped rule returns three rows, the Contracts row with `each_side` true.
  - `test_duplicate_part_name_is_hit` — two Parts rows named `cli`, a State `written by` naming `cli` → hit.
  - `test_empty_side_is_hit` — a Contracts `producer → consumer` cell `cli →` → hit; `—` → hit.
  - `test_external_only_side_is_not_empty` — `external: user → cli` → no hit.
  - `test_parenthesised_only_side_is_empty` — `(once) → cli` → hit.
  - `test_unmatched_segment_not_checked` — `the platform` → no hit, counted not checked.
  - `test_cells_match_after_backticks_and_case` — `` `CLI` `` resolves to row `cli`.
  - `test_missing_tables` (Review Focus 5) — a technical design without a Parts section → no hit, summary `table-closure 0 relations`.
  - `test_not_a_technical_design` — a spec → `table-closure not applicable`.
  Tables are found by section heading text (`Parts`, `Contracts`, `State`, after dropping a leading number) and columns by header text; a cell splits at `→` first when the declaration says `each side`, then at commas and semicolons, after parenthesised text is dropped.

- [ ] **Step 2: Observe them fail**; record. Stop as blocked if any passes.

- [ ] **Step 3: Implement** both functions; the summary line reads `document-check: table-closure <n> relations, <c> names checked, <u> not checked`.

- [ ] **Step 4: Run** the test file — pass.

- [ ] **Step 5: Commit** — `feat(working-process): document-check table closure`

### Task 5: Dogfood over real documents

**Files:**
- Create: `.claude/working-process/2026-11-17-document-check-plan/dogfood.md` (git-ignored record)

**Realizes:** none

- [ ] **Step 1: Run** `bin/wp-document-check` on every file in `docs/specs/` and `docs/plans/`, and on two technical designs: `.claude/working-process/technical-design-dogfood/gate-ab-2/case-A/docs/technical-designs/ai-devcontainer-technical-design.md`, resolved against the main checkout's root (the first line of `git worktree list`) since it is git-ignored and absent from a worktree, and one further design the controlling session supplies. A missing file is skipped and the record says so. This step is the controller's, since a subagent cannot reach other projects; save hits and summary lines to the record.

- [ ] **Step 2: Classify** every hit on a document whose `status:` is not `implemented` as true or false. Any false hit there is a defect of Task 2–4: fix the parse, add the false case as a test, and re-run. Hits on `implemented` documents are listed and classified, not fixed (spec *Verification*).

- [ ] **Step 3: Commit** any fix with its test — `fix(working-process): document-check <what>`. The record stays uncommitted.

### Task 6: The gate moves to the dispatcher

**Files:**
- Modify: `plugins/working-process/skills/review-loop/PROCEDURE.md` (*The propagation gate*)
- Modify: `plugins/working-process/skills/review-loop/LEDGER.md` (*Gate lines*)
- Modify: `plugins/working-process/agents/propagation-auditor.md` (Ground rules, duties 10 and 11, Output)

**Interfaces:**
- Consumes: the commands `wp-document-check <doc>` and `wp-decision-coverage <doc>`.

**Realizes:** D6, D7, D8, D11, D12, D13

- [ ] **Step 1: Count the anchors before the edit**, each with `--side before`:
  - `PROCEDURE.md`: "the coverage duty's hits alone" 1→0; "No other duty's hit is ever held" 1→0; "the card writes those lines on every run" 1→0; "Without the agent installed, every dispatch proceeds as it did before" 1→0; "wp-document-check" 0→1; "wp-decision-coverage" 0→1.
  - `propagation-auditor.md`: "Run the derivation, never walk it by hand" 1→0; "a hit of duty 10 whose fix needs a decision" 1→0; "and so is a name matching several" 1→0; "The summary line opens the block" 1→1 with `--unchanged` (the shapes move, they are not deleted); "Then the lines duties 10 and 11 write on every run" 1→0; "checked, no hit" 0→1; "wp-decision-coverage" 0→1.
  - `LEDGER.md`: "`hit held` is scoped to the coverage duty's hits" 1→0; "A hit of the coverage duty whose fix needs a decision" 1→0; "(document-check)" 0→1; "(decision-coverage)" 0→1.
  Each new term is written once where the plan asks for it; if the text needs it twice, change the `--after` value in both the plan's report and the check, and say why. This is an accepted limitation: Step 2 leaves the wording to the implementer, so the plan cannot fix every after-count in advance.

- [ ] **Step 2: Edit `PROCEDURE.md`'s gate section** to say, in its own words: the dispatcher runs `wp-document-check` and, on a plan or a design spec, `wp-decision-coverage` before dispatching the auditor, disposes of their hits (fixed, dismissed, or for a coverage hit held), re-runs them before every re-dispatch, and only then sends the auditor with nothing from them in its brief (D6, D13); script re-runs are unbounded; without the auditor the scripts are the gate (D11); a script that cannot run stops the gate and goes to the developer, the session fixing a document-side cause the message names, the developer's order to proceed holding for the session and the failing document, nothing in the ledger (D8); the scripts also run at the authoring-time offer, accepted or declined, their hits shown and written nowhere when declined (D11); the relay reports both sides together (D13). Replace the four falsified sentences counted in Step 1, the "Without the agent installed" sentence included (D11 makes the scripts the gate there).

- [ ] **Step 3: Edit the card.** Ground rules gain D7's sentence: "checked, no hit" on a changed identifier needs the command run and the hit count from its output in the report, else the line reads `not checked`. Duty 10's first line says the dispatcher's `wp-decision-coverage` performs it. Split the "Run the derivation" paragraph: everything from "Run the derivation" up to "The steps below define what the script does." goes; that sentence and the steps after it stay, "Derive the map, never tally it" included, as the definition the script implements (D12). Duty 11's first line says `wp-document-check` resolves the segments that equal a Parts row and the auditor keeps a name matching no row (D12); its body narrows to that case, dropping the several-match and empty-cell hits the script now raises. *What becomes of your hits* drops its duty-10 held exception, since the auditor no longer performs duty 10. Output loses everything the auditor no longer writes. The `decision-coverage:` shapes — the plan's block, the map prose after it and the design-spec-alone shapes — move, unchanged, to the end of duty 10, as the definition of `wp-decision-coverage`'s output; "Then the lines duties 10 and 11 write on every run", the `table-closure:` lines and the sentence forbidding a `table-closure:` line elsewhere go; it keeps the self-report, the hit shape and `CLEAN`, and the clean-report sentence ("A clean report is the self-report, the lines above…") is rewritten to name only what remains.

- [ ] **Step 4: Edit `LEDGER.md`'s gate lines** so the held exception names coverage hits from `wp-decision-coverage` alone, and gate lines carry the caption `(document-check)` or `(decision-coverage)` where a script raised them — a label for the human reader; no command parses it.

- [ ] **Step 5: Count the anchors after**, the same calls with `--side after`; all pass.

- [ ] **Step 6: Commit** — `feat(working-process): the dispatcher runs the Document checks before the auditor`

### Task 7: Sweep every falsified sentence, version and changelog

**Files:**
- Modify: whatever the Step 1 grep lists, expected among `plugins/working-process/{README.md, SETTINGS_REGISTRY.md, rules/workflow.md, rules/propagation-duties.md, rules/spec-plan-lifecycle.md, rules/technical-design.md, rules/plan-authoring.md, agents/integrity-auditor.md, agents/plan-adversary.md, skills/review-loop/SKILL.md, scripts/decision-coverage.py}`, `docs/domain/glossary.md`, `README.md`, `.claude-plugin/marketplace.json`, `plugins/working-process/.claude-plugin/plugin.json`, `plugins/working-process/CHANGELOG.md`

**Realizes:** D14

- [ ] **Step 1: Read** the spec's `## Decisions` (`docs/specs/2026-11-17-document-check-spec.md`) — the D-numbers below refer to it. **Enumerate** with `grep -rn -i -E 'decision-coverage|decision coverage|table-closure|table closure|table relations|coverage duty|propagation audit|propagation-auditor|propagation gate|wp-phrase-check|when that agent is available' plugins/working-process README.md .claude-plugin docs/domain/glossary.md --exclude=CHANGELOG.md`; `tests/` lies outside the paths searched. Record each hit in the report as `changes` (it states something D1, D3, D5, D6, D8 or D11 make false) or `stands`, with one line of reason. The grep runs on the tree Task 6 leaves, so the sites Task 6 already rewrote show as `stands`.

- [ ] **Step 2: Edit every `changes` site.** `rules/workflow.md`'s authoring-time offer ("When the `propagation-auditor` agent is available, offer a propagation audit at authoring time") is a `changes` site whatever Step 1 grades: it gains D11's clause that the scripts run at that offer, accepted or declined, whether or not the auditor is available. Command enumerations (plugin.json description, marketplace.json, root README, plugin README) name `wp-phrase-check`, `wp-document-check` and `wp-decision-coverage`; README's Python requirement names all three; `decision-coverage.py`'s docstring points at duty 10 for the steps and the `decision-coverage:` shapes, and at the card's `## Output` for the hit line it prints.

- [ ] **Step 3: Re-run the Step 1 grep** and confirm every remaining hit is either a `stands` site or an edited `changes` site, re-reading each edited site against D1, D3, D5, D6, D8 and D11 and recording the result.

- [ ] **Step 4: Version and changelog.** `plugin.json` version `0.20.0-dev.11.document-check`; `## Unreleased` gains entries for the launcher, `wp-document-check`, the gate order and D7.

- [ ] **Step 5: Validate** — `claude plugin validate .` and `claude plugin validate plugins/working-process` pass; the whole test suite passes.

- [ ] **Step 6: Commit** — `docs(working-process): name the document checks wherever the gate is described`

### Task 8: Live gate

**Files:** none changed

**Realizes:** none

This task is the controlling session's, run after the developer relaunches with the plugin from the checkout; a subagent implementer skips it. Distributed rules load from the installed copies, which lag Task 7's edits until sync-rules runs; that is an accepted limitation of this check, and the record says which copy was loaded.

- [ ] **Step 1: Command resolution** — in a session with the plugin loaded from this checkout (`--plugin-dir plugins/working-process`), confirm `wp-document-check` and `wp-decision-coverage` resolve by name in the Bash tool and in a subagent.

- [ ] **Step 2: Run one gate** on this plan by the new procedure: scripts first, then the auditor; the relay carries the scripts' summary lines and the auditor's report. Record the result in the dogfood record.

## Review rounds

Gate lines from the pre-round propagation episode, 2026-11-17 (haiku). The episode spent its re-dispatches; the developer ordered the round.

- hit fixed 2026-11-17 — Task 7's grep did not exclude CHANGELOG.md though its text said so; the command now carries --exclude=CHANGELOG.md
- hit fixed 2026-11-17 — the card's "Then the lines duties 10 and 11 write on every run" goes false under Task 6 and no step counted it; Task 6 Steps 1 and 3 now name it
- hit fixed 2026-11-17 — the gate-line caption had no reader; Task 6 Step 4 says it labels the line for the human reader and no command parses it
- hit fixed 2026-11-17 — two Task 1 tests pass with the change absent; Step 2 now observes only the launcher test and proves the two structural guards by mutation after Step 3
- hit fixed 2026-11-17 — "import normalise by path, as the tests do": no test does; Step 1 now names importlib and says the tests run it by subprocess
- hit fixed 2026-11-17 — "as the model caption is today": gate lines carry none; now the model named in a gate-line group's lead-in
- hit fixed 2026-11-17 — Task 6 Step 3 could not keep the lead-in while deleting its paragraph; the step now splits the paragraph at "The steps below define what the script does."
- hit fixed 2026-11-17 — the card's Output removal list missed the map prose and the design-spec shapes; Step 3 now removes from "Then the lines…" through the table-closure lines and keeps the self-report, hit shape and CLEAN
- hit fixed 2026-11-17 — the caption's comparison named a model lead-in no gate-line group has; the comparison is gone
- hit fixed 2026-11-17 — the card's clean-report sentence refers to lines Step 3 deletes; Step 3 now rewrites it
- hit fixed 2026-11-17 — Task 7's grep missed README "decision coverage" and "table relations"; both terms added to the pattern

### 2026-11-17 — plan-adversary, opus 5.5, blocking (round 1, full-document)

Record: `.claude/working-process/2026-11-17-document-check-plan/plan-adversary-round-1.md`.

- fixed 2026-11-17 — [Critical] PROCEDURE's "Without the agent installed, every dispatch proceeds" and the card's duty-10 held exception go false and no step reached them; license: D11 and D6; Task 6 Step 1 counts both 1→0, Step 2 replaces the first, Step 3 drops the second
- fixed 2026-11-17 — [Important] Step 4 let the auditor's coverage hits be held; license: the spec's *Who runs it* ("for a `wp-decision-coverage` coverage hit only"); Step 4 names `wp-decision-coverage` alone
- fixed 2026-11-17 — [Important] Task 6 Step 3 deletes the only prose definition of the `decision-coverage:` report shapes while D5 keeps the output and the script's docstring defers to that text; ruling: 2026-11-17; Task 6 Step 3 moves the shapes under duty 10 unchanged, and Task 7's docstring points there
- fixed 2026-11-17 — [Important] Task 6's checks counted only deletions, so an empty Step 2 or 4 passed; license: the plan-authoring rule's class 1; Step 1 adds 0→1 counts for `wp-document-check`, `wp-decision-coverage`, `(document-check)` and `(decision-coverage)`
- fixed 2026-11-17 — [Important] Task 7 Step 3 could not be met by correct text; license: the plan-authoring rule; Step 3 accepts an edited `changes` site re-read against the decisions
- fixed 2026-11-17 — [Important] Task 8 needs a relaunched session a subagent cannot be; license: the plan's subagent-driven execution; Task 8 is the controlling session's
- fixed 2026-11-17 — [Important] Task 3/4 signatures lacked annotations; license: python-standards typing; `lines`, `report` and `relations` are annotated
- fixed 2026-11-17 — [Minor] duplicate headings unspecified; license: D2; a name matching several headings is not checked, with a test
- fixed 2026-11-17 — [Minor] `path#fragment` link targets unspecified; license: D2; not checked, in the link test
- fixed 2026-11-17 — [Minor] `body_lines` silent on a ledger without a round heading and an unclosed frontmatter; license: D15 and Review Focus 1; one clause each
- fixed 2026-11-17 — [Minor] duty 11's body still raised the script's hits; license: D12; Step 3 narrows the body to a name matching no row
- fixed 2026-11-17 — [Minor] Task 5's technical designs were the developer's to name at run time; license: the plan's subagent-driven execution; one path named, the step marked the controller's
- signal 2026-11-17 — one diff-scoped round after this wave earns its cost, a third unlikely; a full-document confirming round is owed at the close

Gate lines from the episode before round 2, 2026-11-17 (haiku):

- hit dismissed 2026-11-17 — the spec's ledger records *Who runs it* widened to "the held kinds and the gate lines' terminal shapes", absent from its body; counter: the architect round-1 F4 ruling later removed D8's ledger shapes and held class, so the widening was superseded and the body is current
- hit dismissed 2026-11-17 — Task 7's grep cannot reach LEDGER.md:240, :253-254, :307 (terminal shapes, `hit dismissed`); counter: after the F4 ruling D8 adds no shape and D6 holds only a coverage hit, so those sentences stay true and need no sweep

### 2026-11-17 — plan-adversary, opus 5.5, concerns (round 2, diff-scoped)

Record: `.claude/working-process/2026-11-17-document-check-plan/plan-adversary-round-2.md`. Ordered by the developer after round 1's `blocking`.

- fixed 2026-11-17 — [Important] the shapes move, duty 11's narrowing and LEDGER's held rewording had no failing count; license: the plan-authoring rule's class 1; Task 6 Step 1 adds "The summary line opens the block" 1→1 `--unchanged`, "and so is a name matching several" 1→0 and "A hit of the coverage duty whose fix needs a decision" 1→0
- fixed 2026-11-17 — [Important] the two new `body_lines` clauses had no asserting test; license: Task 2's own interface text; the two tests gain a heading-less ledger case and an unclosed-frontmatter case
- fixed 2026-11-17 — [Minor] the "written once" rule is a recovery path; license: the reviewer's own cheaper option; the sentence now states it as an accepted limitation
- fixed 2026-11-17 — [Minor] the docstring would point away from the hit line's shape; license: the card's `## Output`, which keeps the hit shape; the docstring points at both
- fixed 2026-11-17 — [Minor] the dogfood path does not exist in a worktree; license: CLAUDE.md's worktree convention; it resolves against the main checkout, a missing file is skipped and recorded
- signal 2026-11-17 — another diff-scoped round would not repay its cost; go straight to the full-document confirming round

Gate lines from the episode before the confirming round, 2026-11-17 (haiku):

- hit dismissed 2026-11-17 — the plan-quality plan names `test_wp_phrase_check_launcher.py`, which Task 1 deletes; counter: that plan is `implemented`, an archive record the implemented-document rule freezes
- hit fixed 2026-11-17 — the `**Realizes:**` lines stood before the `**Interfaces:**` blocks, where the lifecycle rule places them after; moved after (noted by the gate, outside its hits)

### 2026-11-17 — plan-adversary, opus 5.5, blocking (round 3, full-document)

Record: `.claude/working-process/2026-11-17-document-check-plan/plan-adversary-round-3.md`. The confirming round owed at the close.

- fixed 2026-11-17 — [Critical] Task 3 named only `license:` where the spec requires `license:` or `ruling:`; license: the spec's *Citations* and *Settled for the plan*; the test and the step name both, with `ruling:` twins
- fixed 2026-11-17 — [Important] an italic naming no heading could become a false hit; license: D2 and the spec's "a heading of the same document"; `test_license_quote` gains that case as not checked
- fixed 2026-11-17 — [Important] Task 7 classified against D-numbers its implementer cannot read; license: the plan's subagent-driven execution; Step 1 opens by reading the spec's `## Decisions`
- fixed 2026-11-17 — [Important] D11's authoring-time clause lived in PROCEDURE, which does not own the offer; license: D11 and `workflow.md`'s offer sentence; Task 7 Step 2 names that sentence a `changes` site
- fixed 2026-11-17 — [Minor] the launcher's header comment would name phrase-check in all copies; license: D4; Task 1 Step 3 rewords it
- fixed 2026-11-17 — [Minor] no test ran `wp-document-check` through its launcher; license: the spec's Verification; Task 2 adds `test_document_check_launcher_runs`
- fixed 2026-11-17 — [Minor] Task 5 Step 1's spliced sentence misread; license: class 4 of the plan-authoring rule; the sentence is split
- fixed 2026-11-17 — [Minor] the live gate reads installed rules that lag Task 7; license: the reviewer's cheaper option; Task 8 states it as an accepted limitation
- signal 2026-11-17 — the fixes are clause-level and spec-licensed; another full-document round would not repay its cost, a diff-scoped look at the four Critical and Important fixes suffices


Round 3's `blocking` is closed by the developer's adjudication of 2026-11-17 without a further round: every finding was fixed under a written license, and the reviewer's stop signal judged another full-document round not worth its cost.
