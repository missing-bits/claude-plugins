---
ticket: none
date: 2026-11-16
status: approved
spec: ../specs/2026-11-16-plan-quality-spec.md
branch: feature/plan-quality
base: develop
adversary: concerns (resolved 2026-11-16)
---

# Plan Quality Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship `wp-phrase-check`, the `plan-authoring.md` rule and the
two reads that put that rule in front of a plan's author and its
reviewer.

**Architecture:** A Python script in the plugin's `scripts/` counts a
phrase over normalised text and verifies the count against the number
its side expects. A bash launcher in the plugin's new `bin/` finds a
Python 3.9 or later and runs the script, so a plan calls the command by
name. One path-scoped rule holds the defect classes, the failing-test
rule and the check-writing rules; the plan-adversary card and
`workflow.md` step 4 each gain a read of it.

**Tech Stack:** Python 3.9+ standard library (`argparse`, `re`),
`unittest`, bash, Markdown.

**Spec:** `docs/specs/2026-11-16-plan-quality-spec.md`

## Global Constraints

- Every command runs from the repository root, on the topic branch
  `feature/plan-quality`.
- The script uses the standard library only and runs on Python 3.9:
  it opens with `from __future__ import annotations`.
- Committed text is English and carries no path under a home
  directory, no client name and no project name. The rule describes
  its evidence generically.
- Commit messages are one line, conventional-commit form, no body and
  no trailer. A commit step runs only where the developer has
  authorized commits for this plan's execution.
- No step predicts what a failing run prints. A red step says: run it
  with the change absent and record what it prints in the report. A
  run that does not fail with the change absent stops the task: report
  `BLOCKED` under superpowers:subagent-driven-development, or stop and
  report to the developer when executing inline.
- Per task, run only that task's new test file. The whole suite runs
  once, in Task 6.
- From Task 3 on, every verification check over text is a
  `wp-phrase-check` call by its checkout path,
  `plugins/working-process/bin/wp-phrase-check`: the installed plugin
  does not carry the command yet. A check on a file present on both
  sides runs on each side of its step, the two calls identical but for
  `--side`. A file the step creates runs the after side only.
- Every expected count below was computed against the state the
  previous task leaves, with develop at `8449fc7`. Steps find their
  place by text, never by line number.
- New and edited Markdown under `plugins/` gets the
  `elements-of-style:writing-clearly-and-concisely` pass when that
  skill is available. The pass binds wording, never a decision; the
  blocks this plan gives verbatim have had theirs.
- Glossary terms bind: **Verification check** and **Vacuous check** as
  `docs/domain/glossary.md` defines them; never "sanity check",
  "no-op check" or "dead check".

## Review Focus

Known limit (session's provisional decision, 2026-11-16): `--phrase` is normalised like the text, so a phrase that itself opens with a list or quote marker loses it; the helper prints the normalised phrase, which the author reads.

Inputs the spec implies and its *Verification* list does not name.
Each has its test in the task that owns the code.

1. A file with CRLF line endings: a phrase wrapped across a CRLF
   counts like any other (Task 1, `test_crlf_wrap_counts`).
2. A file opening with a UTF-8 byte-order mark: a phrase at the very
   start still counts (Task 1, `test_bom_does_not_hide_first_word`).
3. A phrase that starts with a hyphen, such as the name of one of the
   command's own arguments: written `--phrase=<words>`, it counts
   (Task 1, `test_phrase_starting_with_hyphen`).
4. A path containing a space: the launcher passes it through whole
   (Task 2, `test_path_with_space_survives_launcher`).
5. An empty file: it was read, holds zero lines and counts zero, so a
   removal check over it passes and says `lines 0` (Task 1,
   `test_empty_file_is_read`).

## File Structure

| File | Change | Responsibility |
|---|---|---|
| `plugins/working-process/scripts/phrase-check.py` | create | normalise, count, verify, print, exit |
| `plugins/working-process/bin/wp-phrase-check` | create | find Python 3.9+, run the script |
| `tests/working-process/test_phrase_check.py` | create | the script's behaviour |
| `tests/working-process/test_wp_phrase_check_launcher.py` | create | the launcher's fallbacks |
| `plugins/working-process/rules/plan-authoring.md` | create | the rule |
| `plugins/working-process/agents/plan-adversary.md` | modify | read the rule at FIRST ACTION |
| `plugins/working-process/rules/workflow.md` | modify | step 4 reads the rule before plan-writing |
| `plugins/working-process/README.md` | modify | component, requirements, rule count, permission entry |
| `plugins/working-process/CHANGELOG.md` | modify | `## Unreleased` entries |
| `plugins/working-process/.claude-plugin/plugin.json` | modify | description, dogfood version |
| `.claude-plugin/marketplace.json`, `README.md` | modify | description names the command |

---

### Task 1: The phrase-check script

**Files:**
- Create: `plugins/working-process/scripts/phrase-check.py`
- Test: `tests/working-process/test_phrase_check.py`

**Interfaces:**
- Produces, for Task 2 and every later check — the command line:

      phrase-check.py [<path>...] --phrase <words> --before <n> --after <m> --side before|after [--unchanged]

  Exit `0` pass; `1` check failure (a path problem, no path named, a
  count mismatch, a vacuous pair); `2` usage error, which `argparse`
  raises by itself.
- Produces — functions, so the tests and the script agree on names:
  `normalise(text: str) -> str`,
  `count_phrase(text: str, phrase: str) -> int`,
  `read_text(path: str) -> str` (raises `Unreadable`, whose message is
  the reason), `main(argv: list[str] | None = None) -> int`.

**Realizes:** D2, D3, D4

**The contract the tests pin**

*Normalisation* (`normalise`), in this order:

1. Split into lines with `str.splitlines()`.
2. From each line drop leading whitespace, then every leading marker,
   repeatedly: `>` with any whitespace after it; `-`, `*` or `+`
   followed by whitespace or the line's end; digits followed by `.` or
   `)` and then whitespace or the line's end. As one pattern:
   `^\s*(?:(?:>\s*|(?:[-*+]|\d+[.)])(?:\s+|$)))*`.
3. Join the lines with one space, collapse every run matching `\s+` to
   one space, strip both ends, apply `str.casefold()`.

Nothing else is stripped: headings (`#`), table pipes, task-list boxes
(`[ ]`), emphasis and code markers stay, so `---` and `**bold**` are
untouched. `--phrase` goes through the same function. A phrase empty
after normalising is a usage error (exit `2`).

*Counting* (`count_phrase`): `normalise(text).count(normalise(phrase))`
per file, summed over the files named. `str.count` does not overlap,
and counting per file never spans two files. A path named twice counts
twice.

*Reading* (`read_text`): a path is a file. The shell expands globs;
the script expands nothing and refuses a directory. Open in binary and
decode as `utf-8-sig`. The reasons, verbatim: `no such file`,
`not a file`, `cannot be read (<strerror>)`, `not valid UTF-8`.
"Read no file" means no path reached the script.

*Arguments*: `--before` and `--after` are required non-negative
integers (a negative is a usage error); `--side` is required;
`--unchanged` declares that the step leaves the count as it is.
`expected` is the number of the side named.

*Output*, one shape, all on stdout:

    wp-phrase-check: PASS
    phrase: "<normalised phrase>"
    side: after
    expected: 1 (before 0, after 1)
    actual: 1
    read: files 1, lines 79
      <path as given>: lines 79, matches 1

A failing run prints `wp-phrase-check: FAIL` on the first line and
appends one `fail:` line per reason, in this fixed order:

    fail: <path>: <reason>
    fail: read no file
    fail: count mismatch: expected <n> on side <side>, found <k>
    fail: vacuous: before and after are both <n>; pass --unchanged if the step leaves the phrase as it is

With a path problem or no path, `actual:` reads `not counted`, the
`read:` block lists the files that were read, and neither count line
is evaluated. Otherwise the mismatch line and the vacuity line are
evaluated independently, so a run can print both, mismatch first. The
vacuity line fires on either side whenever `--before` equals `--after`
without `--unchanged`.

The helper does not know whether a file exists on the other side. A
step that creates or deletes a file runs only the side where the file
exists, with `0` as the absent side's number; the rule of Task 3 says
so, and the script needs nothing for it (spec round 2 ruling: "the
helper unchanged").

- [ ] **Step 1: Write the tests**

`tests/working-process/test_phrase_check.py`, one `unittest.TestCase`.
Follow `test_decision_coverage.py`: `REPO = Path(__file__).resolve().parents[2]`,
`SCRIPT` under `plugins/working-process/scripts/`, each test in a
`tempfile.TemporaryDirectory`, the script run with
`subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)`.
Two helpers: `write(name, content) -> str` (bytes when given bytes)
and `run(*args)`. Below, `B/A/S` abbreviates
`--before B --after A --side S`; "→ 0" is the exit code; quoted text
must appear in stdout.

| Test | File content | Call | Asserts |
|---|---|---|---|
| `test_wrapped_phrase_counts` | `alpha beta\ngamma delta\n` | phrase `beta gamma`, 0/1/after | → 0, `actual: 1` |
| `test_capital_after_wrap` | `the quick\nBrown fox\n` | `quick brown`, 0/1/after | → 0, `actual: 1` |
| `test_doubled_whitespace` | `alpha  \t beta\n` | `alpha beta`, then `alpha   beta`, each 0/1/after | both → 0, `actual: 1` |
| `test_crlf_wrap_counts` | bytes `alpha\r\nbeta\r\n` | `alpha beta`, 0/1/after | → 0, `actual: 1` |
| `test_bom_does_not_hide_first_word` | bytes `\xef\xbb\xbfalpha beta\n` | `alpha beta`, 0/1/after | → 0, `actual: 1` |
| `test_list_and_quote_markers_dropped` | `- alpha\n  beta\n> gamma\n> delta\n1. one\n   two\n2) three\n* four\n+ five\n` | `alpha beta`; `gamma delta`; `one two three four five`; each 0/1/after | each → 0, `actual: 1` |
| `test_nested_markers_dropped` | `> - alpha\n> beta\n` | `alpha beta`, 0/1/after | → 0, `actual: 1` |
| `test_inline_markup_untouched` | `**alpha** beta\n---\n-dash\n# head\n` | `alpha beta`, 1/0/after; then `**alpha** beta --- -dash # head`, 0/1/after | both → 0; `actual: 0`, then `actual: 1` |
| `test_phrase_normalised_like_text` | `alpha beta\n` | `--phrase=- Alpha\n  BETA` (a real newline), 0/1/after | → 0, `actual: 1` |
| `test_phrase_starting_with_hyphen` | `use --side here\n` | `--phrase=--side`, 0/1/after | → 0, `actual: 1` |
| `test_no_match_across_files` | `a.md`: `alpha\n`; `b.md`: `beta\n` | both paths, `alpha beta`, 1/0/after | → 0, `actual: 0` |
| `test_matches_do_not_overlap` | `aa aa aa\n`; then `ab ab ab ab\n` | `aa aa`, 0/1/after; `ab ab`, 0/2/after | → 0 `actual: 1`; → 0 `actual: 2` |
| `test_total_over_files_and_what_was_read` | `a.md`: `x\nalpha\n`; `b.md`: `alpha\nalpha\ny\n` | both paths, `alpha`, 0/3/after | → 0; first line `wp-phrase-check: PASS`; `expected: 3 (before 0, after 3)`; `actual: 3`; `read: files 2, lines 5`; a line ending `a.md: lines 2, matches 1`; one ending `b.md: lines 3, matches 2` |
| `test_same_path_twice_counts_twice` | `alpha\n` | the path twice, `alpha`, 0/2/after | → 0, `read: files 2, lines 2` |
| `test_empty_file_is_read` | empty | `alpha`, 1/0/after | → 0, `read: files 1, lines 0`, `actual: 0` |
| `test_side_selects_the_number` | `alpha\n` | `alpha`, 1/0/before; then 1/0/after | → 0; then → 1 with `fail: count mismatch: expected 0 on side after, found 1` |
| `test_mismatch_fails` | `alpha\n` | `alpha`, 0/2/after | → 1; first line `wp-phrase-check: FAIL`; `fail: count mismatch: expected 2 on side after, found 1` |
| `test_equal_counts_fail_unless_declared` | `alpha\n` | `alpha`, 1/1/before; 1/1/after; 1/1/after with `--unchanged` | → 1 with `fail: vacuous`; → 1 with `fail: vacuous`; → 0 with no `fail:` |
| `test_mismatch_reported_before_vacuity` | `alpha\n` | `alpha`, 2/2/after | → 1; stdout holds both `fail: count mismatch` and `fail: vacuous`, the first at the lower index |
| `test_missing_path_fails` | none | a path that does not exist, `alpha`, 1/0/after | → 1; `actual: not counted`; a `fail:` line ending `no such file`; no `fail: count mismatch` |
| `test_directory_fails` | none | the temporary directory itself, `alpha`, 1/0/after | → 1; a `fail:` line ending `not a file` |
| `test_invalid_utf8_fails` | bytes `\xff\xfe alpha\n` | `alpha`, 0/1/after | → 1; a `fail:` line ending `not valid UTF-8` |
| `test_unopenable_file_fails` | `alpha\n`, then `os.chmod(path, 0)` | `alpha`, 0/1/after | → 1; `fail:` line containing `cannot be read`. Skip when `os.name == "nt"` or `os.geteuid() == 0` |
| `test_one_bad_path_fails_the_run` | `a.md`: `alpha\n` | `a.md` and a missing path, `alpha`, 0/1/after | → 1; `actual: not counted`; `read: files 1, lines 1` |
| `test_no_path_fails` | none | no path, `alpha`, 1/0/after | → 1; `fail: read no file` |
| `test_blank_phrase_is_usage_error` | `alpha\n` | `--phrase=   `, 0/1/after | → 2 |
| `test_negative_count_is_usage_error` | `alpha\n` | `alpha`, `--before=-1 --after 0 --side after` | → 2 |

A missing or non-numeric `--before`, `--after` or `--side` gets no
test: `argparse` rejects it before the script's own code runs (spec
ledger, the dismissed gate line before round 2).

- [ ] **Step 2: Observe the tests with the script absent**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_phrase_check.py'`

Record in the report the summary line it prints and the first failure
or error in full. If the run ends `OK`, stop: `BLOCKED`. A file-level
failure here shows only that the tests reach for the script; Step 4 is
what shows each test can fail.

- [ ] **Step 3: Write `plugins/working-process/scripts/phrase-check.py`**

Shebang `#!/usr/bin/env python3`, a module docstring carrying the
usage line and the exit codes, the four functions of **Interfaces**,
`TOOL = "wp-phrase-check"` for the output's first line, and
`if __name__ == "__main__": sys.exit(main())`. Declare the paths as
`nargs="*"` so that no path reaches the script's own "read no file"
failure instead of an `argparse` error. The `--help` text says that a
phrase starting with a hyphen is written `--phrase=<words>`.
`chmod +x` the file.

- [ ] **Step 4: Run the tests, then show two of them can fail**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_phrase_check.py'`
Passes when the last line is `OK`.

Then, twice, weaken the script and re-run the same command, recording
which tests fail each time, and restore the script after each:
(a) delete the marker pattern from `normalise`; (b) make the vacuity
reason never fire. If either weakening leaves the run `OK`, stop:
`BLOCKED`. Run the command once more after restoring; it ends `OK`.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/scripts/phrase-check.py tests/working-process/test_phrase_check.py
git ls-files -s plugins/working-process/scripts/phrase-check.py
```

The second command's line starts `100755`. If it starts `100644`, run
`git update-index --chmod=+x plugins/working-process/scripts/phrase-check.py`
and check again.

```bash
git commit -m "feat(working-process): phrase-check script for plan verification checks"
```

---

### Task 2: The launcher

**Files:**
- Create: `plugins/working-process/bin/wp-phrase-check`
- Test: `tests/working-process/test_wp_phrase_check_launcher.py`

**Interfaces:**
- Consumes: `scripts/phrase-check.py` and its command line (Task 1).
- Produces: the command `wp-phrase-check`, taking the script's
  arguments unchanged and returning its exit code. With no usable
  Python it exits `2` and prints one line on stderr:

      wp-phrase-check: no Python 3.9 or later found; tried: python3 (<why>), python (<why>), py -3 (<why>)

  where `<why>` is `not found` or `rejected`.

**Realizes:** D1, D5

**The contract the tests pin**

- `#!/usr/bin/env bash`. The launcher resolves its own path from
  `${BASH_SOURCE[0]}`, following symbolic links in a loop with
  `readlink` and joining a relative target to the link's directory —
  no `readlink -f` and no `realpath`, which stock macOS lacks.
  Directory names come from parameter expansion and `cd … && pwd`, so
  `readlink` is the only external command it calls. The script is
  `<launcher's directory>/../scripts/phrase-check.py`;
  `CLAUDE_PLUGIN_ROOT` is not read.
- Candidates, in order: `python3`, `python`, `py -3`. A candidate
  whose first word `command -v` does not find is `not found`. One that
  is found runs
  `-c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'`
  with stdout and stderr discarded; a non-zero exit is `rejected`.
  That one line is valid in Python 2, so an old interpreter answers
  and is rejected, never run.
- The first accepted candidate is run with
  `exec "${candidate[@]}" "$script" "$@"`, the candidate held as an
  array so `py -3` stays two words.

- [ ] **Step 1: Write the tests**

`tests/working-process/test_wp_phrase_check_launcher.py`, one
`unittest.TestCase`, skipped whole when `os.name == "nt"`. Each test
builds a directory of stubs and runs
`subprocess.run([BASH, LAUNCHER, *args], env={"PATH": stub_dir}, capture_output=True, text=True)`
with `BASH = shutil.which("bash")`. The stub directory always holds a
symbolic link to the real `readlink` (`shutil.which("readlink")`) and
nothing else from the system, so no real interpreter is reachable.
Stubs are executable files starting `#!<BASH>`:

- *good*: `exec <sys.executable> "$@"`;
- *old*: `if [ "$1" = "-c" ]; then exit 1; fi; echo WRONG-INTERPRETER; exit 0`;
- *good py*: `[ "$1" = "-3" ] || exit 9; shift; exec <sys.executable> "$@"`.

`PASSING` names the arguments of a run that passes: a temporary file
holding `alpha\n`, `--phrase alpha --before 0 --after 1 --side after`.

| Test | Stubs | Call | Asserts |
|---|---|---|---|
| `test_python3_runs` | `python3` good | `PASSING` | → 0; stdout starts `wp-phrase-check: PASS` |
| `test_old_python3_is_skipped_for_python` | `python3` old, `python` good | `PASSING` | → 0; stdout starts `wp-phrase-check: PASS`; `WRONG-INTERPRETER` nowhere in stdout |
| `test_py_launcher_is_last_resort` | `py` good py | `PASSING` | → 0; stdout starts `wp-phrase-check: PASS` |
| `test_no_python_names_what_it_tried` | `python3` old | `PASSING` | → 2; stdout empty; stderr holds `python3 (rejected)`, `python (not found)` and `py -3 (not found)` |
| `test_exit_code_passes_through` | `python3` good | the same file, `--phrase alpha --before 0 --after 2 --side after` | → 1; stdout starts `wp-phrase-check: FAIL` |
| `test_symlinked_launcher_finds_script` | `python3` good | the launcher run through a symbolic link made in a second temporary directory, `PASSING` | → 0; stdout starts `wp-phrase-check: PASS` |
| `test_path_with_space_survives_launcher` | `python3` good | the file named `two words.md`, otherwise `PASSING` | → 0; a stdout line ending `two words.md: lines 1, matches 1` |

- [ ] **Step 2: Observe the tests with the launcher absent**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_wp_phrase_check_launcher.py'`

Record the summary line and the first failure or error in full. If the
run ends `OK`, stop: `BLOCKED`.

- [ ] **Step 3: Write `plugins/working-process/bin/wp-phrase-check`**

To the contract above; `chmod +x` it. Keep it short: resolve, try the
three candidates collecting each `<why>`, `exec` the first accepted,
otherwise print the stderr line and `exit 2`.

- [ ] **Step 4: Run the tests, then show the version test can fail**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_wp_phrase_check_launcher.py'`
Passes when the last line is `OK`.

Then make the launcher accept every found candidate without the
version test, re-run, record which tests fail, and restore it. If the
run stays `OK`, stop: `BLOCKED`. Re-run after restoring; it ends `OK`.

- [ ] **Step 5: Run the command by its checkout path**

Run: `plugins/working-process/bin/wp-phrase-check README.md --phrase "Missing Bits" --before 2 --after 2 --unchanged --side after`

Passes when it exits `0` and prints `wp-phrase-check: PASS` and
`actual: 2`. This is the first real run on this host; later tasks
depend on it.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/bin/wp-phrase-check tests/working-process/test_wp_phrase_check_launcher.py
git ls-files -s plugins/working-process/bin/wp-phrase-check
```

The second command's line starts `100755`; otherwise run
`git update-index --chmod=+x plugins/working-process/bin/wp-phrase-check`
and check again.

```bash
git commit -m "feat(working-process): wp-phrase-check launcher in the plugin bin"
```

---

### Task 3: The plan-authoring rule

**Files:**
- Create: `plugins/working-process/rules/plan-authoring.md`

**Realizes:** D6, D7, D9

- [ ] **Step 1: Write the rule**

The file's whole content, verbatim. The `paths:` values are quoted
scalars; `claude plugin validate` does not read `rules/`, so read the
frontmatter by eye once written.

`````markdown
---
paths:
  - "docs/plans/**"
  - "docs/**/*-plan.md"
---

# Plan authoring — recurring defect classes

A plan's verification steps keep failing in the same few ways. Read
this before the plan's first line is written, and ask each class's
question of every task before handing the plan on. The plan-adversary
agent, when available, reads the same text.

## Seven classes

1. **A check or test that cannot fail.** It passes whether or not the
   step did its work: a test green without the change, a count equal
   before and after, a search over a path that holds nothing. *What
   does this print with the step undone?*
2. **An expected value fitted to the author's view.** The value was
   read off the tree the author had open, while the check runs on the
   tree the previous task leaves. *Did I compute it on that tree?*
3. **An anchor by line number.** A line number goes stale with the
   first edit above it, an earlier task of the same plan included.
   *Does the step find its place by text that will still be there?*
4. **A defect born of a repair.** A fix written between review rounds
   gets less care than the first draft, and most late findings come
   from one. *Have I re-run every check the fix touches?*
5. **A check of an artifact the consumer does not load.** The step
   verifies the source while the consumer reads an installed, built or
   cached copy. *Which file does the consumer open?*
6. **Fixes in one wave that undo each other.** One fix restores the
   phrase another fix's check counts, or two rewrite one sentence.
   *Does any fix in this wave change what another relies on?*
7. **The same discipline one site away.** A finding marks one site,
   and its neighbours usually share the defect: the next task, the
   sibling file, the other side of a pair. *Where else does the rule
   I just applied hold?*

## A failing test is observed, never predicted

A plan never states the message a failing test will print. It
prescribes the observation: run the test with the change absent —
before the change is written, or with it reverted — record what the
run prints in the implementer's report, and restore the change where
it was reverted. The plan stays as approved. A test that passes with
the change absent proves nothing, and the task stops as blocked: an
implementer reports its execution skill's blocked status (`BLOCKED` in
superpowers' subagent-driven-development skill, when available), and a
session executing the plan itself stops and reports to the developer.

## Writing a verification check

When the `wp-phrase-check` command is available — the working-process
plugin puts it on the Bash tool's `PATH` while enabled — every
verification check over text takes its form:

    wp-phrase-check <path>... --phrase "<words>" --before <n> --after <m> --side before|after

It joins lines, collapses whitespace, ignores case and drops a line's
leading list or quote marker, and it prints the expected count, the
actual count and what it read. Without the command, normalise by hand
— `tr -s '[:space:]' ' '`, then a case-insensitive count — and state
both numbers beside the check.

The command cannot enforce the rest:

- Run the check on each side of its step, the two calls identical but
  for `--side`.
- Give a file the step creates or deletes a check of its own, run only
  on the side where the file exists; the absent side's number is `0`.
- State the change the step makes, as the before/after pair, never a
  total fitted to the file as the author found it.
- Write a check that correct text can satisfy. When satisfying a check
  forces an odd edit, the check is the defect.
- Pass `--unchanged` only to state that the step leaves the phrase as
  it is; equal numbers without it fail.

Classes 2 and 3 bind every check as well and are stated once, above.
`````

What the text settles, for the reviewer of this plan:

- The seven classes are D9's, in D9's order, each with its question.
- Classes 2 and 3 are also two of the spec's five check-writing
  items. Each is stated once, as a class; the check-writing list
  carries the other three and points back.
- "Blocked" is `BLOCKED` in superpowers:subagent-driven-development
  and, inline, a stop reported to the developer.
- The command is named conditionally. Without it the author
  normalises by hand and states both numbers.
- The created-or-deleted-file case of D4 lives here, in the second
  check-writing item; the command takes no argument for it.

- [ ] **Step 2: Verify the rule, after side only (the step created the file)**

```bash
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/plan-authoring.md --phrase "Plan authoring — recurring defect classes" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/plan-authoring.md --phrase "docs/**/*-plan.md" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/plan-authoring.md --phrase "never states the message" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/plan-authoring.md --phrase "stops as blocked" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/plan-authoring.md --phrase "wp-phrase-check" --before 0 --after 2 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/plan-authoring.md --phrase "absent side's number" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/plan-authoring.md --phrase "checklist" --before 0 --after 0 --unchanged --side after
```

Each exits `0`. The last one states D8's ban on the word in this rule:
the count stays zero by declaration. Then the seven class names, one
call each, every one expecting `--before 0 --after 1 --side after` on
the same file: `cannot fail`, `fitted to the author's view`,
`anchor by line number`, `born of a repair`,
`the consumer does not load`, `undo each other`, `one site away`.

Run: `wc -l < plugins/working-process/rules/plan-authoring.md`
Passes when it prints `79`; the spec's size target is under 80.

Run: `sh plugins/working-process/scripts/ruleset-hash.sh --list plugins/working-process/rules | grep -c 'plan-authoring.md'`
Passes when it prints `1`: the listing is what `sync-rules` installs
from. Before this task the same command printed `0`.

- [ ] **Step 3: Commit**

```bash
git add plugins/working-process/rules/plan-authoring.md
git commit -m "feat(working-process): plan-authoring rule with the recurring defect classes"
```

---

### Task 4: The two reads — adversary card and workflow step 4

**Files:**
- Modify: `plugins/working-process/agents/plan-adversary.md` (the
  FIRST ACTION paragraph)
- Modify: `plugins/working-process/rules/workflow.md` (step 4, the
  paragraph beginning `Then write the`)

**Realizes:** D8, D10

- [ ] **Step 1: Run the before side**

```bash
plugins/working-process/bin/wp-phrase-check plugins/working-process/agents/plan-adversary.md --phrase "rules/plan-authoring.md" --before 0 --after 1 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/agents/plan-adversary.md --phrase "(evidence = that file)." --before 1 --after 1 --unchanged --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/workflow.md --phrase "plan-authoring rule" --before 0 --after 2 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/workflow.md --phrase "requires reading it before the plan is written" --before 1 --after 0 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/workflow.md --phrase "superpowers:writing-plans when available" --before 1 --after 1 --unchanged --side before
```

Each exits `0`. A non-zero exit here means the tree is not the one
this plan was written against: stop and report.

- [ ] **Step 2: Edit the card**

In `plugins/working-process/agents/plan-adversary.md`, the FIRST
ACTION paragraph ends `(evidence = that file).` Leave it as it is and
add, after one blank line, this paragraph:

```markdown
Then read `${CLAUDE_PLUGIN_ROOT}/rules/plan-authoring.md`, "Plan
authoring — recurring defect classes": the text the plan's author
wrote from. A step that shows one of its seven classes, predicts the
message a failing test prints, or breaks one of its check-writing
rules is a finding (evidence = the plan quote and that rule's
heading).
```

The card's `description:` stays as it is; no severity is assigned, so
the card's generic scale grades the finding.

- [ ] **Step 3: Edit `workflow.md` step 4**

Replace the paragraph of step 4 that begins `Then write the` and ends
`context cannot count on it loading.` with this one, keeping the
three-space indent of the step's other paragraphs:

```markdown
   Before the plan's first line is written, whoever writes it — the
   session or a separate context — reads the plan-authoring rule,
   installed beside this one: a path-scoped rule loads only when a
   matching file is read, and a new plan has none yet. Then write the
   implementation plan with superpowers:writing-plans when available;
   plans live in `docs/plans/` (or the ticket directory, below). A
   brief that delegates plan-writing to a separate context names the
   spec-plan-lifecycle rule and the plan-authoring rule and requires
   reading both before the plan is written: the first carries the
   annotations a plan owes a registered design spec, the second the
   recurring defect classes and the check-writing rules, and a
   separate context cannot count on either loading.
```

The lifecycle rule's sentence "as the workflow rule's step 4 says"
stays true and is not edited.

- [ ] **Step 4: Run the after side**

```bash
plugins/working-process/bin/wp-phrase-check plugins/working-process/agents/plan-adversary.md --phrase "rules/plan-authoring.md" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/agents/plan-adversary.md --phrase "(evidence = that file)." --before 1 --after 1 --unchanged --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/workflow.md --phrase "plan-authoring rule" --before 0 --after 2 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/workflow.md --phrase "requires reading it before the plan is written" --before 1 --after 0 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/rules/workflow.md --phrase "superpowers:writing-plans when available" --before 1 --after 1 --unchanged --side after
```

Each exits `0`.

Run: `claude plugin validate plugins/working-process`
Passes when it reports the plugin valid; the card's frontmatter was
not touched, and this shows it still parses.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/agents/plan-adversary.md plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): plan-writing and the plan-adversary read the plan-authoring rule"
```

---

### Task 5: README, identity surfaces, changelog, dogfood version

**Files:**
- Modify: `plugins/working-process/README.md`
- Modify: `plugins/working-process/CHANGELOG.md`
- Modify: `plugins/working-process/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `README.md`

**Realizes:** D11

- [ ] **Step 1: Derive the dogfood counter from develop**

```bash
git log develop -p --format= -- plugins/working-process/.claude-plugin/plugin.json | grep -o '^+.*-dev\.[0-9]*\.' | grep -o '[0-9]*\.$' | sort -n | tail -1
```

Written against a develop on which this prints `9.`, so the version is
`0.20.0-dev.10.plan-quality`: one above the highest counter in
develop's history, on the version develop already carries above the
released `0.19.0`, with the branch short-name as discriminator. If it
prints another number, use that number plus one in Step 3 and in both
runs of the version check, and say so in the report.

- [ ] **Step 2: Run the before side**

```bash
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "wp-phrase-check" --before 0 --after 2 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "eight rule files" --before 1 --after 0 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "nine rule files" --before 0 --after 1 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "plan-authoring.md" --before 0 --after 1 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "claude.ai or Cowork" --before 0 --after 1 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "for the propagation auditor's coverage duty." --before 1 --after 0 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/CHANGELOG.md --phrase "wp-phrase-check" --before 0 --after 1 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/CHANGELOG.md --phrase "plan-authoring.md" --before 0 --after 1 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md --phrase "wp-phrase-check" --before 0 --after 3 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/.claude-plugin/plugin.json --phrase "0.20.0-dev.9.process-context" --before 1 --after 0 --side before
plugins/working-process/bin/wp-phrase-check plugins/working-process/.claude-plugin/plugin.json --phrase "0.20.0-dev.10.plan-quality" --before 0 --after 1 --side before
```

Each exits `0`; a non-zero exit means the tree differs from the one
this plan was written against: stop and report.

- [ ] **Step 3: Edit the plugin README**

Four edits in `plugins/working-process/README.md`.

(a) *Components*: after the `sync-rules` skill's bullet, which ends
`"Process rules" section.`, add:

```markdown
- **`wp-phrase-check` command** — a plan's verification check over
  text. It counts a phrase after joining lines, collapsing whitespace,
  ignoring case and dropping list and quote markers, verifies the count
  against the number its side expects, and fails a check that could
  not show its step did anything. It ships in `bin/`, which Claude
  Code puts on the Bash tool's `PATH` while the plugin is enabled.
```

(b) *Requirements*: after the first bullet, which ends
`alone work on ≥ 2.1.143).`, add:

```markdown
- Claude Code itself, not claude.ai or Cowork: the plugin ships a
  top-level `bin/`, and a plugin that has one does not install there.
```

and replace the bullet that ends
`for the propagation auditor's coverage duty.` with:

```markdown
- Python 3.9 or later, standard library only. `wp-phrase-check` finds
  it as `python3`, `python` or `py -3`, in that order, and confirms
  each by its version; the propagation auditor's coverage duty calls
  `python3`.
```

(c) *Process rules*: `eight rule files` becomes `nine rule files`,
and the clause ending `plan or domain document is open), and the`
becomes `plan or domain document is open), the recurring defect
classes a plan's author reads (`plan-authoring.md`, loaded while a
plan is open), and the` — re-wrap the paragraph as the file wraps.

(d) *Reducing permission prompts* stays as it is: the helper runs
under the user's permission mode, as superpowers' scripts do (spec,
non-goals; developer's ruling 2026-11-16).

- [ ] **Step 4: Edit the changelog, the identity surfaces and the version**

`plugins/working-process/CHANGELOG.md`: append to the `## Unreleased`
section, directly before the `## 0.19.0 — 2026-11-13` heading:

```markdown
- `wp-phrase-check`, a command the plugin puts on the Bash tool's
  `PATH`: a plan's verification check over text, counting a phrase
  whatever the file's wrapping, case or whitespace. Each run names its
  side, prints the expected count, the actual count and what it read,
  and fails on a mismatch, a missing or unreadable path, a run that
  read no file, or equal before and after counts not declared
  unchanged. A bash launcher finds Python 3.9 or later as `python3`,
  `python` or `py -3`.
- A new rule, `plan-authoring.md`, loaded while a plan is open: seven
  recurring defect classes, the rule that a plan prescribes observing
  a failing test and never predicts its message, and the check-writing
  rules. Plan-writing reads it before the plan's first line, and the
  plan-adversary reads the shipped copy.
- The plugin now needs Claude Code itself: with a top-level `bin/` it
  does not install on claude.ai or in Cowork.
```

The three descriptions gain the command, in one commit, each after the
words `integrity-auditor audit agents,`:

- `plugins/working-process/.claude-plugin/plugin.json`:
  `…audit agents, the wp-phrase-check command for a plan's
  verification checks over text, and process rules distributed as a
  Rules payload; …` — and `"version"` becomes
  `"0.20.0-dev.10.plan-quality"`.
- `.claude-plugin/marketplace.json`:
  `…audit agents, the wp-phrase-check command, plus distributed
  process rules`.
- `README.md`, the `working-process` row:
  ``…audit agents, the `wp-phrase-check` command, distributed process
  rules``.

Each JSON description stays one line.

- [ ] **Step 5: Run the after side**

```bash
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "wp-phrase-check" --before 0 --after 2 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "eight rule files" --before 1 --after 0 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "nine rule files" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "plan-authoring.md" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "claude.ai or Cowork" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/README.md --phrase "for the propagation auditor's coverage duty." --before 1 --after 0 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/CHANGELOG.md --phrase "wp-phrase-check" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/CHANGELOG.md --phrase "plan-authoring.md" --before 0 --after 1 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md --phrase "wp-phrase-check" --before 0 --after 3 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/.claude-plugin/plugin.json --phrase "0.20.0-dev.9.process-context" --before 1 --after 0 --side after
plugins/working-process/bin/wp-phrase-check plugins/working-process/.claude-plugin/plugin.json --phrase "0.20.0-dev.10.plan-quality" --before 0 --after 1 --side after
```

Each exits `0`.

Run: `ls plugins/working-process/rules/*.md | wc -l`
Passes when it prints `9`, the number the README now states.

Run: `python3 -c "import json; json.load(open('plugins/working-process/.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json')); print('ok')"`
Passes when it prints `ok`.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/README.md plugins/working-process/CHANGELOG.md plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md
git commit -m "docs(working-process): wp-phrase-check and plan-authoring in README, catalog and changelog"
```

---

### Task 6: Final verification

**Files:** none changed. A defect found here goes back to the task
that owns the file.

**Realizes:** D1, D7

- [ ] **Step 1: The whole suite, once**

Run: `python3 -m unittest discover -s tests/working-process`
Passes when the last line is `OK`. The count is the 77 tests develop
carries plus the 27 of Task 1 and the 7 of Task 2: `Ran 111 tests`.
Another count means a test was added, dropped or not collected: find
which before going on.

- [ ] **Step 2: Validate**

Run: `claude plugin validate .`
Run: `claude plugin validate plugins/working-process`
Each passes when it reports no error.

- [ ] **Step 3: Hygiene over the new files, by the command itself**

```bash
plugins/working-process/bin/wp-phrase-check plugins/working-process/bin/wp-phrase-check plugins/working-process/scripts/phrase-check.py plugins/working-process/rules/plan-authoring.md tests/working-process/test_phrase_check.py tests/working-process/test_wp_phrase_check_launcher.py --phrase "/home/" --before 0 --after 0 --unchanged --side after
```

Passes when it exits `0` and its `read:` line says `files 5`.

- [ ] **Step 4: Both files carry the executable bit in git**

Run: `git ls-files -s plugins/working-process/bin/wp-phrase-check plugins/working-process/scripts/phrase-check.py`
Passes when both lines start `100755`.

- [ ] **Step 5: A live session and a subagent run the command by name**

Executor: the controlling session, with the developer's go-ahead —
the step disables the installed `working-process` plugin while it
runs, so the checkout's copy loads without a name collision. Never
leave it disabled.

First observe the absent state: in a shell where the checkout's `bin/`
is not on `PATH`, run `wp-phrase-check --help` and record what it
prints.

```bash
claude plugin disable working-process
claude -p "Run this exact command with the Bash tool and print its output verbatim under the label SESSION: wp-phrase-check README.md --phrase wp-phrase-check --before 0 --after 1 --side after. Then dispatch one general-purpose subagent, tell it to run the same command with its Bash tool and return the output verbatim, and print what it returns under the label SUBAGENT." --plugin-dir plugins/working-process --allowedTools "Bash(wp-phrase-check *)" "Agent" "Task"
claude plugin enable working-process
```

Passes when the output holds `wp-phrase-check: PASS` and `actual: 1`
under both labels. A `command not found`, or a subagent that could not
run the command, fails the step: report it with the output, since D1
rests on this. Run `claude plugin list` afterwards and confirm
`working-process` is enabled.

- [ ] **Step 6: The rule installs — developer step, STOP**

Once the dogfood version is installed on the developer's host, the
developer runs the `working-process:sync-rules` skill and confirms
that `plan-authoring.md` lands in the rules target. The session does
not write to the user-level rules directory unasked. Until then the
`ruleset-hash.sh --list` result of Task 3 is the evidence that the
payload carries the file.

- [ ] **Step 7: Report**

The closing report carries: every recorded red observation (Tasks 1
and 2, and Step 5's absent state), the two weakening runs of Task 1
and the one of Task 2, the derived dogfood counter, the live check's
two outputs, and what was not checked — the Windows store placeholder
(an accepted risk of the spec) and any Claude Code version floor for a
plugin's `bin/`.

## Review rounds

Gate lines from the pre-round propagation episode, 2026-11-16 (haiku). The episode held hits, so they stay here, before the first round heading.

- hit fixed 2026-11-16 — Task 5 Step 5 expected `wp-phrase-check` 4 times in the plugin README after the edit; dropping the permission entry left 2; now 2
- hit fixed 2026-11-16 — "the dismissed hit" put a Hit in view of the plan's bare "check"; now "the dismissed gate line"

Both fixes change one value and one word; the episode was not re-dispatched over them, and the first adversary round reads the whole plan.

### 2026-11-16 — plan-adversary, opus 5.5, concerns (round 1, full-document)

Record: `.claude/working-process/2026-11-16-plan-quality-plan/plan-adversary-round-1.md`.

- fixed 2026-11-16 — [Minor] Task 5 Steps 2 and 5 carried different `--after` values for one check after the gate fix touched Step 5 only; license: Global Constraints, "the two calls identical but for `--side`"; Step 2 now `--after 2`
- fixed 2026-11-16 — [Minor] a phrase opening with a list or quote marker loses it under normalisation; provisional: 2026-11-16 (stand-in session); accepted as a documented limitation under *Review Focus*, no script option
- signal 2026-11-16 — both findings Minor with one-line fixes; another round would not earn its cost

The round was full-document, so it closes the loop: `concerns` is resolved by the two fixes above under the developer's standing instruction of 2026-11-16 to carry the work through implementation without asking unless a decision is genuinely theirs.
