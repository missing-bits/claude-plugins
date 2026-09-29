---
ticket: none
date: 2026-09-28
status: approved
adversary: concerns (resolved 2026-09-29)
spec: ../specs/2026-09-28-process-setup-design.md
branch: feature/process-setup
base: develop
---

# process-setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land `docs/specs/2026-09-28-process-setup-design.md` — the
two settings files, the key registry, the loader with its four modes and
its SessionStart hook, the always-on `process-settings.md` rule, the
`process-setup` skill, and the rule, card and command edits that read a
named key instead of "the developer's own instructions".

**Architecture:** One POSIX `sh` script, `scripts/load-settings.sh`,
owns every read and every write of a settings file; it parses the
registry `SETTINGS_REGISTRY.md` at the plugin root with `sed` and
`awk`, and the same registry is what the skill asks from and the
consistency test checks. The rules cite a key by name and read it from
the block the hook puts in context; nothing else resolves a key. The
loader and its tests are code with a test cycle each; every other
deliverable is prose, whose test is the check block it publishes, run
before and after the edit.

**Tech Stack:** POSIX `sh` (dash), `sed`, `awk` and `git` for the
loader; Python 3.9+ `unittest` via `subprocess` for its tests and the
consistency test, following `tests/working-process/test_decision_coverage.py`;
Markdown rules, cards, skill and README distributed as a Claude Code
plugin and Rules payload; `tr`, `grep`, `awk`, `shasum` and
`claude plugin validate` for the prose checks; `jq` for Task 17's
reading of `claude plugin list --json`, and nowhere else.

## Global Constraints

- **The spec is the source.** Where this plan and the spec disagree, the
  spec wins and the plan is wrong — except where *Deviations from the
  spec* below records a departure and its reason.
- **Realizes:** D26 — **Version one reads the working-process registry
  alone.** The loader opens exactly one registry, found relative to its
  own path; no task discovers, lists or reads a registry of another
  plugin, and `salesforce-standards`' `trigger-framework:` and
  `vendor-paths:` declarations are not touched.
- **Realizes:** D8 — **Keys are never renamed, and no key is retired.**
  Every key this plan registers keeps its name in every task; the
  registry's header says so, and no task writes a retirement marker or a
  loader report for one — both wait for the first key actually retired.
- **Realizes:** D48 — **The grilling-session skill is not modified.**
  `plugins/working-process/skills/grilling-session/SKILL.md` keeps
  deferring to `process-artifacts.md`'s signal list; Task 16 checks its
  hash against `develop`.
- **The loader is POSIX.** `#!/bin/sh`, `set -u`, `export LC_ALL=C`,
  and only `sh`, `sed`, `awk`, `git`, `mkdir`, `mv`, `rm`, `cat`,
  `printf`, `dirname`, `basename`, `pwd` and `head`; no `jq`, no
  `bash`-only syntax, no `local` (function variables are global or
  passed positionally, since `shellcheck -s sh` rejects it as SC3043),
  no GNU-only flags. Every step that runs the loader
  runs it through `/bin/sh` (dash on the development machine) so a
  bashism fails here rather than on macOS.
- **The loader never reads stdin** — Claude Code and Codex feed a hook
  JSON on stdin, and a loader that waited on it would hang.
- **Prose wraps at 72 characters** in every rule, agent card, skill and
  README. Match the surrounding paragraph; never reflow a paragraph this
  plan does not change. Indented grammar examples, table rows, one-line
  `description:` values and lines inside fenced blocks are exempt, as
  they are everywhere in the rules.
- **Copy every Replace block verbatim.** The blocks already carry the
  elements-of-style pass; a block an implementer rewords owes the pass
  again, and its checks may stop matching.
- **Checks normalise whitespace and match fixed strings.** A prose check
  pipes the file through `tr -s '[:space:]' ' '` and counts with
  `grep -oF … | wc -l`, so a phrase matches wherever a line wraps and
  the count is the same under GNU grep and ugrep. Only a check anchoring
  something that cannot wrap — a heading, a table row, a command, a
  key line — reads the file plain.
- **The glossary binds.** `docs/domain/glossary.md` terms and `_Avoid_`
  bans govern every new sentence: **Standing answer**, **Settings key**,
  **Team key**, **Personal key**, **Settings line**, **Key registry**,
  **Settings block**, **First-create question**, **Process directory**
  and **Tier** are canonical; "preference", "config", "option", "flag",
  "shared setting", "private setting", "schema", "key list", "settings
  dump", "config context", "artifact folder" and "model level" are
  banned. A settings line is never called a declaration; a declaration
  is the prose note in `CLAUDE.md`.
- **Public repo hygiene**: no machine-specific paths, no company or
  client names, all committed text in English. Test fixtures use
  `tempfile` paths and `fixture@example.invalid` identities.
- **Commit messages are one line** — a conventional-commit subject, no
  body and no trailer, not even `Co-Authored-By`. A subagent
  implementer's brief says so outright, since subagents add the trailer
  by default.
- **Commits land on `feature/process-setup`.** The document branch
  `feature/process-setup.docs` merges into it at the implementation-ready
  gate, before Task 1.
- **Do not run `sync-rules`, do not move the spec's or this plan's
  `status`, and do not commit anything under `.claude/working-process/`.**
  All three are the developer's. The dogfood version string is the one
  version edit this plan makes (Task 15); the final bump belongs to the
  release PR.
- **`cp`, `mv` and `rm` are aliased `-i` on the development machine.**
  Every scripted copy or removal in this plan uses `command cp -f`,
  `command mv -f` or `command rm -rf`, and checks the effect on disk.
- **Tests are stdlib-only `unittest`, run by the system `python3`.** As
  `tests/working-process/test_decision_coverage.py` already does: no
  Python project, no `pyproject.toml`, no lockfile, no third-party
  import, and every test step in this plan runs `python3 -m unittest`
  as the machine provides it. The `Python 3.9+` floor in *Tech Stack*
  is a claim until Task 16 measures it once under an interpreter at
  the floor.

## Deviations from the spec

Recorded here and beside the text they concern.

1. **Task 8 also strikes "which a capable model does casually badly"
   from the first paragraph of the propagation auditor's tier section.**
   The spec strikes the card's second clause, "an over-tier run does
   this work casually badly — a false clean line would then feed the
   integrity gate unnoticed"; the first paragraph makes the same claim
   in five words, and a card keeping one copy would still call the
   evidence-backed choice the dangerous one.
2. **Task 15 writes `## Unreleased` entries for `python-standards` and
   `salesforce-standards` as well.** The spec's *Changes by file* names
   README and CHANGELOG entries for working-process and project-memory;
   the repository's plugin-versioning rule requires an entry for every
   plugin a topic changes, and Task 12 changes both review commands.
   Only working-process takes the `-dev` version, since only it is
   loaded from the checkout in the dogfood.
3. **Task 15 changes the plugin's `description:` in three places.** The
   spec names README and CHANGELOG; the description lists the plugin's
   skills, so a new skill changes it, and the marketplace-sync rule
   makes `plugin.json`, `marketplace.json` and the root README row one
   edit.
4. **Task 5 appends `settings.local.md` to an existing
   `.working-process/.gitignore` that lacks the line, and reports it.**
   D24 covers the file's creation and says nothing of one already there;
   the directory ignores its own local file by definition (*The
   settings files*), and a personal answer written into a file git would
   track breaks that definition.
5. **Task 5 opens a settings file it creates with one title line.** The
   spec says a created file holds the question and the key; a Markdown
   file that opens with a lower-case key line reads as a fragment, and
   the title is commentary under the grammar, so it changes no reading.
6. **Task 2 lists a duplicated key with the source `[invalid in team]`
   or `[invalid in local]`.** The spec hands the duplicated key's source
   to the plan and names a closed source set without a duplicate token;
   the `error:` line carries the distinction, so the set stays closed.
7. **Task 9 also says the session reports an overridden note.** The
   plan's block for the `docs-branch.merge` paragraph stated only that
   the key wins; D20 also has the session say which note it overrode, as
   workflow.md's technical-design site already says, and the developer
   ruled at implementation to add the clause.

## Settled format edges

The spec's *Open questions* hands these to the plan. Each is settled
here and realized where the task named says.

1. **The key line's regular expression and its whitespace** — Task 2.
   A line is a settings line when it matches the POSIX ERE
   `^[a-z0-9-]+\.[a-z0-9./-]+:` at column one, outside a fence: no
   leading whitespace, no whitespace before the colon. It is valid when
   the whole line matches
   `^[a-z0-9-]+\.[a-z0-9./-]+:[ \t]*[A-Za-z0-9._/-]+[ \t\r]*$` — any
   spaces or tabs after the colon, one token, then only spaces, tabs or
   a carriage return. Values compare exactly; `Yes` is not `yes`. A
   fence is a line starting with three backticks at column one; an
   indented one is commentary.
2. **A `dir.<path>` line's source when `dir.default` is unset or
   invalid, and a duplicated key's source** — Task 2. An absent
   exception always carries `[inherited]` and `dir.default`'s effective
   value, `unset` included, so the reader sees that it follows the
   default and that the default decides nothing. A duplicated key
   carries `[invalid in team]` or `[invalid in local]` (Deviation 6),
   and its `error:` line names every line of the duplicate.
3. **The first line's `local:` when no personal file exists** — Tasks 2
   and 3. Each file the loader looked for and did not find carries
   `(absent)` in the first line: `team: settings.md (absent)`,
   `local: settings.local.md (absent)`, and in a worktree
   `local: settings.local.md (main checkout, absent)` or
   `local: settings.local.md (worktree, bare repository, absent)`.
4. **A suggestion beside a `[local]` value** — Task 2. Never: a
   suggestion shows only beside `unset`. A personal key the personal file
   decides shows its value and `[local]` and nothing else; the team's
   suggestion was a default answer for a question the person has
   answered.
5. **The truncation line and the 4 KB cut** — Task 2. The cap is 4096
   bytes over the whole hook output. A block of at most 4096 bytes is
   emitted whole, with no `incomplete:` line. A longer one is cut on a
   line boundary: the loader emits whole lines while the running byte
   count plus the `incomplete:` line's length stays at or under 4096,
   then the `incomplete:` line, so the line it adds counts inside the
   cap — and the first line is never dropped.
6. **The tier table's form in `workflow.md`** — Task 8. A three-row
   Markdown table after the model-selection paragraph, keyed by the
   value and giving the Claude Code rung in the glossary's words.
7. **The "and record" wording for a non-yes/no answer and for the
   autonomy question's two clauses** — Tasks 7, 9, 10, 11 and 12. The
   option reads `<answer>, and record`, whatever the answer:
   "tracked, and record", "squash, and record", "on" and "off" behind
   the technical-design offer's "yes, and record" and "no, and record".
   The autonomy question records per clause: an answer may say "yes,
   and record; commits: not now", which writes `review.autonomy` and
   nothing for `review.per-round-commit`; "not now" and "not in this
   session" are never recorded, since they die with the session.

## File structure

Created:

- `plugins/working-process/SETTINGS_REGISTRY.md` — Task 1: the key
  registry, at the plugin root beside `PERSONA_COMMON.md`, since three
  consumers read it (the loader, the skill, the consistency test).
- `plugins/working-process/scripts/load-settings.sh` — Tasks 2–5: the
  loader; hook mode, `--print`, `--validate`, `--set`, `--set --dry-run`.
- `tests/working-process/test_settings_registry.py` — Tasks 1 and 14:
  the consistency test.
- `tests/working-process/test_load_settings.py` — Tasks 2–5: the loader
  tests.
- `plugins/working-process/rules/process-settings.md` — Task 6: the
  always-on rule.
- `plugins/working-process/skills/process-setup/SKILL.md` — Task 13.

Modified, under `plugins/working-process/` unless said otherwise:

- `hooks/hooks.json` — Task 2: the second SessionStart handler.
- `rules/workflow.md` — Task 7 (persona consent, the technical-design
  declaration, the autonomy question, the compaction clause) and Task 8
  (the propagation auditor's tier and the tier table).
- `agents/propagation-auditor.md`, `agents/integrity-auditor.md` —
  Task 8: the tier clauses.
- `rules/spec-plan-lifecycle.md` — Task 9: per-round commit consent,
  the `.docs` branch merge.
- `rules/process-artifacts.md`, `rules/review-reports.md` — Task 10:
  the settings key among the directory signals, the local pocket keyed
  to the resolved mode.
- `plugins/project-memory/rules/project-memory.md` — Task 11.
- `plugins/python-standards/commands/python-review.md`,
  `plugins/salesforce-standards/commands/salesforce-review.md` —
  Task 12.
- `README.md`, `CHANGELOG.md`, `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json` (repository root), root `README.md`,
  `plugins/project-memory/CHANGELOG.md`,
  `plugins/python-standards/CHANGELOG.md`,
  `plugins/salesforce-standards/CHANGELOG.md` — Task 15.

Not modified: `skills/grilling-session/SKILL.md` (D48),
`docs/domain/glossary.md` (D31 — already landed; Task 16 checks),
`scripts/check-rules-drift.sh`, `scripts/ruleset-hash.sh`,
`scripts/write-manifest.sh`, `skills/sync-rules/SKILL.md`. Adding
`rules/process-settings.md` changes the Rules payload hash
`ruleset-hash.sh` computes, so every installed copy gets the drift
nudge after this ships; the CHANGELOG says so.

## Order and independence

- Task 1 comes first: the loader (Tasks 2–5), the skill (Task 13) and
  the consistency test (Task 14) all read the registry's exact shape.
- Tasks 2, 3, 4 and 5 build one script in that order; each adds a mode
  or a layout and its tests, and the earlier tests keep passing.
- Task 6 names the block's first line and source tokens exactly as
  Task 2 prints them; run Task 2 first.
- Tasks 7, 8, 9, 10, 11 and 12 are prose edits, one file or one decision
  each, and depend on nothing but Task 1's key names. Task 8 edits
  `workflow.md` after Task 7; its anchor is untouched by Task 7.
- Task 13 needs Tasks 2–5 (it calls every loader mode) and Task 6 (it
  cites the rule).
- Task 14 needs every prose task, since it checks that each registry
  entry's readers cite the key.
- Task 15 needs every name the earlier tasks produced. Task 16 verifies
  the whole branch; Tasks 17 and 18 run the loader in the two hosts and
  need everything before them.

---

### Task 1: The key registry and its shape test

**Files:**
- Create: `plugins/working-process/SETTINGS_REGISTRY.md`
- Create: `tests/working-process/test_settings_registry.py`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: the registry path `${CLAUDE_PLUGIN_ROOT}/SETTINGS_REGISTRY.md`
  (`$(dirname "$0")/../SETTINGS_REGISTRY.md` from the loader); the
  heading shape `## <key>` and the five fields `scope:`, `values:`,
  `default:`, `read-by:`, `question:`, one per line in that order; the
  fourteen key names every later task cites; the parser
  `read_registry(path) -> dict[str, dict[str, str]]` in the test module,
  which Task 14 extends.

**Realizes:** D6, D7.1, D7.2, D7.3, D7.4, D7.5, D7.6, D7.7, D7.8, D7.9, D7.10, D7.11, D7.12, D7.13, D7.14

- [ ] **Step 1: Write the failing test**

`tests/working-process/test_settings_registry.py`, `unittest`, standard
library only. The parser is a module-level function so Task 14 can
reuse it:

```python
"""Consistency test for plugins/working-process/SETTINGS_REGISTRY.md.

The registry's shape is fixed — one `## <key>` heading per key, then the
five fields, one per line, in order — so this test and the loader's sed
parse it without a Markdown parser.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PLUGINS = REPO / "plugins"
REGISTRY = PLUGINS / "working-process" / "SETTINGS_REGISTRY.md"
FIELDS = ("scope", "values", "default", "read-by", "question")
KEY_RE = re.compile(r"^[a-z0-9-]+\.[a-z0-9./-]+$")
HEADING_RE = re.compile(r"^## (\S+)$")


def read_registry(path: Path) -> dict[str, dict[str, str]]:
    """Parse the registry into {key: {field: value}}, in file order.

    A heading opens an entry; the next five non-blank lines are its
    fields, `name: value`, in FIELDS order. Anything else is a defect and
    raises AssertionError with the line number.
    """
    entries: dict[str, dict[str, str]] = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        heading = HEADING_RE.match(lines[index])
        if not heading:
            index += 1
            continue
        key = heading.group(1)
        if key in entries:
            raise AssertionError(f"line {index + 1}: duplicate key {key}")
        fields: dict[str, str] = {}
        index += 1
        for name in FIELDS:
            while index < len(lines) and lines[index].strip() == "":
                index += 1
            if index >= len(lines) or not lines[index].startswith(f"{name}: "):
                raise AssertionError(f"line {index + 1}: expected `{name}: ` under {key}")
            fields[name] = lines[index][len(name) + 2:].strip()
            index += 1
        entries[key] = fields
    return entries


class RegistryShapeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.entries = read_registry(REGISTRY)

    def test_fourteen_keys_in_order(self) -> None:
        self.assertEqual(list(self.entries), [
            "dir.default", "dir.docs/specs", "dir.docs/technical-designs",
            "dir.docs/plans", "dir.docs/domain", "dir.docs/code-review",
            "dir..superpowers", "dir.docs/memory",
            "design.technical-design-offer", "dispatch.propagation-auditor-tier",
            "docs-branch.merge", "consult.personas", "review.autonomy",
            "review.per-round-commit",
        ])

    def test_every_entry_is_well_formed(self) -> None:
        for key, fields in self.entries.items():
            with self.subTest(key=key):
                self.assertRegex(key, KEY_RE)
                self.assertIn(fields["scope"], ("team", "personal"))
                values = fields["values"].split(" | ")
                self.assertTrue(all(re.fullmatch(r"[A-Za-z0-9._/-]+", v) for v in values), values)
                self.assertEqual(len(values), len(set(values)))
                self.assertTrue(fields["default"] == "unset" or fields["default"] in values,
                                fields["default"])
                for reader in fields["read-by"].split(", "):
                    self.assertTrue((PLUGINS / reader).is_file(), reader)
                self.assertTrue(fields["question"].endswith("?"), fields["question"])
                self.assertFalse(KEY_RE.match(fields["question"].split(":")[0]),
                                 "a question must not read as a key line")

    def test_scopes_and_defaults(self) -> None:
        personal = {k for k, f in self.entries.items() if f["scope"] == "personal"}
        self.assertEqual(personal, {"consult.personas", "review.autonomy", "review.per-round-commit"})
        self.assertEqual(self.entries["dispatch.propagation-auditor-tier"]["default"], "cheapest")
        others = {k: f["default"] for k, f in self.entries.items()
                  if k != "dispatch.propagation-auditor-tier"}
        self.assertEqual(set(others.values()), {"unset"})


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to see it fail**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_settings_registry.py' -v`
Expected: every test errors with `FileNotFoundError` on the registry.
(The directory name carries a hyphen, so discovery is the only form
that runs it; `python3 -m unittest tests.working-process…` cannot.)

- [ ] **Step 3: Write the registry**

`plugins/working-process/SETTINGS_REGISTRY.md`, exactly:

```
# working-process settings — the key registry

The one definition of every settings key. The `process-setup` skill
takes its questions from here, the loader `scripts/load-settings.sh`
its validation and defaults, and the repository's
`test_settings_registry.py` its consistency check; the rules name keys
and nothing more. The shape
is fixed so that `sed` and the test parse it without a Markdown parser:
one `## <key>` heading per key, then exactly these five fields, one per
line, in this order — `scope:` (`team` or `personal`), `values:` (the
allowed values, separated by ` | `), `default:` (a value, or `unset`
where the rule asks), `read-by:` (the files that read the key,
comma-separated, relative to `plugins/`) and `question:` (what the
skill asks, and the comment `--set` writes above the key). A `dir.`
key other than `dir.default` is an exception: absent, it inherits
`dir.default`'s effective value. A key is never renamed; the marker for
a retired key, and how the loader reports one, wait for the first key
that is retired.

## dir.default

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does a Process directory get unless an exception names it — tracked or ignored?

## dir.docs/specs

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does docs/specs/ get, as an exception to dir.default — tracked or ignored?

## dir.docs/technical-designs

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does docs/technical-designs/ get, as an exception to dir.default — tracked or ignored?

## dir.docs/plans

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does docs/plans/ get, as an exception to dir.default — tracked or ignored?

## dir.docs/domain

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does docs/domain/ get, as an exception to dir.default — tracked or ignored?

## dir.docs/code-review

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md, python-standards/commands/python-review.md, salesforce-standards/commands/salesforce-review.md
question: Which mode does docs/code-review/ get, as an exception to dir.default — tracked or ignored?

## dir..superpowers

scope: team
values: tracked | ignored
default: unset
read-by: working-process/rules/process-artifacts.md
question: Which mode does the .superpowers/ family get, as an exception to dir.default — tracked or ignored?

## dir.docs/memory

scope: team
values: tracked | ignored
default: unset
read-by: project-memory/rules/project-memory.md
question: Which mode does docs/memory/ get, as an exception to dir.default — tracked or ignored?

## design.technical-design-offer

scope: team
values: on | off
default: unset
read-by: working-process/rules/workflow.md
question: Is the technical design offered at every consumption gate (on) or never (off)?

## dispatch.propagation-auditor-tier

scope: team
values: cheapest | mid | most-capable
default: cheapest
read-by: working-process/rules/workflow.md, working-process/agents/propagation-auditor.md
question: Which tier runs the propagation gate — cheapest, mid or most-capable?

## docs-branch.merge

scope: team
values: squash | fast-forward
default: unset
read-by: working-process/rules/spec-plan-lifecycle.md
question: How does the topic branch take the .docs branch at the implementation-ready gate — squash or fast-forward?

## consult.personas

scope: personal
values: yes | no
default: unset
read-by: working-process/rules/workflow.md
question: May the architect and system-designer personas be consulted as a design forms?

## review.autonomy

scope: personal
values: yes | no
default: unset
read-by: working-process/rules/workflow.md
question: May the review loop run autonomously, within the round cap?

## review.per-round-commit

scope: personal
values: yes | no
default: unset
read-by: working-process/rules/workflow.md, working-process/rules/spec-plan-lifecycle.md
question: May the review loop commit the reviewed document once per round?
```

The `read-by:` lists name files that cite the key only after Tasks 7–12
land; Task 14 checks the citations, this task checks that the files
exist.

- [ ] **Step 4: Run the test to see it pass**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_settings_registry.py' -v`
Expected: 3 tests, `OK`.

Then confirm the loader's view of the same file — every heading is a
key and every key has exactly five fields:

```bash
F=plugins/working-process/SETTINGS_REGISTRY.md
echo "A $(grep -c '^## ' $F)"
echo "B $(grep -Ec '^(scope|values|default|read-by|question): ' $F)"
echo "C $(grep -c '^default: unset$' $F)"
```

Expected: `A 14`, `B 70`, `C 13`.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/SETTINGS_REGISTRY.md tests/working-process/test_settings_registry.py
git commit -m "feat(working-process): settings key registry"
```

---

### Task 2: The loader — hook mode, `--print`, the block and the grammar

**Files:**
- Create: `plugins/working-process/scripts/load-settings.sh`
- Create: `tests/working-process/test_load_settings.py`
- Modify: `plugins/working-process/hooks/hooks.json` — a second
  SessionStart handler.

**Interfaces:**
- Consumes: the registry from Task 1, at
  `$(dirname "$0")/../SETTINGS_REGISTRY.md`.
- Produces: the command `load-settings.sh` (hook mode) and
  `load-settings.sh --print`; the block's first line, key lines,
  `error:` lines and `incomplete:` line exactly as *The block* below
  prints them — Task 6's rule and Task 13's skill quote them; the test
  helpers `LoaderTest`, `settings()`, `run()`, `git_init()` that
  Tasks 3–5 extend.

**Realizes:** D1, D2, D3, D4, D9, D10, D11, D28, D32, D33, D34, D36, D42, D44

This task is code, so its steps are test-driven. The contract below is
the requirement for the reading side; Tasks 3–5 add the worktree
layouts, `--validate` and `--set` to the same script. The script is
one file; keep its functions named as the contract names them so the
later tasks extend rather than restructure.

**The contract — reading.**

- **Invocation.** No argument: hook mode. `--print`: the same block on
  stdout, uncapped, exit 0. Any other argument list not defined by
  Tasks 4 and 5: a one-line usage message on stderr, exit 2 — except in
  hook mode, which never prints to stderr and never exits non-zero.
  The script begins `#!/bin/sh`, `set -u`, `export LC_ALL=C`, and
  never reads stdin.
- **Paths.** `LOADER` is the script's own absolute path,
  `$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")`; `PLUGIN` is
  `$(cd "$(dirname "$LOADER")/.." && pwd -P)`; `REGISTRY` is
  `$PLUGIN/SETTINGS_REGISTRY.md`. `CLAUDE_PLUGIN_ROOT` is not read.
- **Root.** `find_root` sets `ROOT` to `git rev-parse --show-toplevel`
  when it succeeds (in a worktree, the worktree's own root), else
  `$CLAUDE_PROJECT_DIR` when set and non-empty, else `$PWD`, each made
  physical with `pwd -P`. `DIR` is `$ROOT/.working-process`, `TEAM`
  `$DIR/settings.md`, `LOCAL` `$DIR/settings.local.md`. Task 3 adds the
  layouts; in this task `LAYOUT` is always `main` and `LOCAL_LABEL` is
  `settings.local.md`.
- **The registry.** `registry_keys` prints every `## ` heading's key in
  file order; `registry_field <key> <field>` prints the field's value
  (`sed -n` from the key's heading to the next heading, then the
  `<field>: ` line, value after the two characters `: `). A registry
  that is missing or yields no key is a loader error: hook mode prints
  nothing and exits 0; every other mode prints
  `error: registry not found or empty at <REGISTRY>` on stderr and
  exits 1.
- **Silence.** In hook mode, when `$DIR` is not a directory, print
  nothing, exit 0. `--print` then prints exactly one line,
  `working-process settings (root: <ROOT>; loader: <LOADER>; no settings directory)`,
  and exits 0. Task 3 qualifies both for the worktree layout, where
  the main checkout's directory counts too.
- **The grammar** (`scan_file <file> <scope>`, one awk pass). A fence
  toggles on a line matching `^```` `. Outside a fence, a line matching
  the ERE `^[a-z0-9-]+\.[a-z0-9./-]+:` is a settings line; its key is
  the text before the first `:`; it is valid when the whole line
  matches `^[a-z0-9-]+\.[a-z0-9./-]+:[ \t]*[A-Za-z0-9._/-]+[ \t\r]*$`,
  its value the token between; otherwise it is invalid and its raw
  value is the text after the colon with spaces, tabs and a trailing
  carriage return stripped, shown as `(empty)` when nothing remains.
  Every other line — leading whitespace included — is commentary. The
  pass prints one record per settings line:
  `<line number>\t<key>\t<ok|invalid>\t<value or raw text>`. A missing
  file prints no record.
- **Resolution** (`resolve`), per registered key in registry order:
  - the deciding file is `$TEAM` for a team key, `$LOCAL` (or its
    fallback, Task 3) for a personal key; the other file is the
    foreign file;
  - records in the deciding file for the key: none → the default
    (`<default>  [default]`; for a `dir.` key other than `dir.default`,
    `dir.default`'s effective value — `unset` included — with
    `[inherited]`); exactly one, valid, value among `values:` → the
    value with `[team]` or `[local]`; exactly one, invalid or a value
    not among `values:` → `unset  [invalid in team|local]` and
    `error: <file>:<n> invalid value for `<key>`: <raw> — unset`;
    more than one → `unset  [invalid in team|local]` and
    `error: <file>:<n1>,<n2>[,…] duplicate key `<key>` — unset`, at
    most one error line per key per file, the duplicate taking
    precedence over an invalid value;
  - records in the foreign file for a personal key (the team file):
    exactly one and valid → where the key resolved to `unset  [default]`,
    the line becomes `unset  [team suggests: <value>]`; where the
    personal file decided it, nothing is shown; invalid → an `error:`
    line ending `— ignored` and no suggestion; more than one → a
    duplicate `error:` line ending `— ignored` and no suggestion;
  - records in the foreign file for a team key (the personal file):
    each → `error: settings.local.md:<n> team key `<key>` in the personal file — ignored`;
  - a settings line whose key is not registered, in either file →
    `error: <file>:<n> unknown key `<key>` — ignored`.
  Error lines come in file order, team file first, then line order;
  the `<file>` token is `settings.md` or `settings.local.md`, never a
  path.
- **The block** (`emit_block`): the first line,
  `working-process settings (root: <ROOT>; loader: <LOADER>; team: <TEAM_LABEL>; local: <LOCAL_LABEL>)`,
  where a label is the file's basename followed by ` (absent)` when the
  file does not exist (Task 3 adds the layout qualifiers, inside the
  same parentheses, before `absent`); then one line per registered key
  in registry order, `<key>: <value>  [<source>]` — two spaces before
  the bracket; then the `error:` lines. Nothing else, no blank lines.
- **The cap** (`cap_block`, hook mode only): 4096 bytes over the whole
  output. A block whose total byte count is at or under 4096 passes
  through whole, with no `incomplete:` line. Otherwise lines are
  emitted whole, in order, while the bytes so far plus the next line
  plus the length of `incomplete: run <LOADER> --print` plus its
  newline stay at or under 4096; where a line would exceed it, that
  line and every later one are dropped and
  `incomplete: run <LOADER> --print` closes the block, inside the
  4096. The first line is emitted whatever its length. `--print` never
  caps.
- **Errors of the loader's own.** Hook mode wraps everything: any
  failure — registry missing, `awk` absent or failing, an unset
  variable under `set -u`, an unreadable file — ends in no output and
  exit 0, the way `check-rules-drift.sh` ends. The mechanism is a
  subshell: `main` in hook mode runs the body that builds the block as
  `block=$(set -e; build_block 2>/dev/null); rc=$?` and prints only when
  `rc` is 0 — never `… || block=''` nor `if block=$(…)`, because bash
  ignores `set -e` inside a substitution tested by `||` or `if`, which
  would let a failing tool run on. Every failing command, `die`
  included, ends the subshell, its stderr is discarded and its partial
  output dropped; `$block` goes through `cap_block` to stdout only when
  `rc` is 0, and `main` exits 0 either way. `build_block` also returns
  non-zero from each tool call it makes (`|| return 1`), so the silence
  does not rest on `set -e` alone. Every other mode runs the same body with stderr
  kept and, where it fails, prints `error: loader failed` on stderr
  after whatever the failing tool wrote, exits 1 and prints nothing on
  stdout. The block is assembled in a variable and printed once at the
  end, so a failure midway prints nothing partial.

- [ ] **Step 1: Write the failing tests**

`tests/working-process/test_load_settings.py`. The helpers below are
the module; Tasks 3–5 add methods and cases to it and change none of
these:

```python
"""Tests for plugins/working-process/scripts/load-settings.sh.

Each test builds a project in a temporary directory, runs the loader
through /bin/sh from a chosen working directory, and asserts the exact
lines the contract names.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import unittest
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LOADER = (REPO / "plugins" / "working-process" / "scripts" / "load-settings.sh").resolve()
REGISTRY = REPO / "plugins" / "working-process" / "SETTINGS_REGISTRY.md"
GIT = ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
       "-c", "init.defaultBranch=main", "-c", "commit.gpgsign=false"]
KEYS = [  # registry order
    "dir.default", "dir.docs/specs", "dir.docs/technical-designs", "dir.docs/plans",
    "dir.docs/domain", "dir.docs/code-review", "dir..superpowers", "dir.docs/memory",
    "design.technical-design-offer", "dispatch.propagation-auditor-tier",
    "docs-branch.merge", "consult.personas", "review.autonomy", "review.per-round-commit",
]


def tree_hash(root: Path) -> str:
    """One digest over every file's path and bytes under root, for byte-identity checks."""
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


class Result:
    def __init__(self, proc: subprocess.CompletedProcess[str]) -> None:
        self.proc = proc
        self.out = proc.stdout
        self.err = proc.stderr
        self.code = proc.returncode
        self.lines = proc.stdout.splitlines()
        self.errors = [l for l in self.lines if l.startswith("error: ")]

    def line(self, key: str) -> str:
        """The block line for `key`, or an AssertionError."""
        for l in self.lines:
            if l.startswith(f"{key}: "):
                return l
        raise AssertionError(f"no line for {key} in {self.lines}")


class LoaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name).resolve()
        self.root = self.base / "proj"
        self.root.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def git(self, cwd: Path, *args: str) -> str:
        env = dict(os.environ, GIT_CEILING_DIRECTORIES=str(self.base))
        proc = subprocess.run(GIT + list(args), cwd=cwd, capture_output=True, text=True, env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout

    def git_init(self, path: Path | None = None) -> Path:
        """A repository with one empty commit at `path` (default: self.root)."""
        path = path or self.root
        path.mkdir(parents=True, exist_ok=True)
        self.git(path, "init", "-q")
        self.git(path, "commit", "-q", "--allow-empty", "-m", "fixture")
        return path

    def settings(self, root: Path, team: str | None = None, local: str | None = None,
                 gitignore: str | None = None) -> Path:
        """Create root/.working-process with the files given (None = absent)."""
        d = root / ".working-process"
        d.mkdir(parents=True, exist_ok=True)
        for name, text in (("settings.md", team), ("settings.local.md", local), (".gitignore", gitignore)):
            if text is not None:
                (d / name).write_text(text, encoding="utf-8")
        return d

    def run_loader(self, cwd: Path, *args: str, project_dir: str | None = None,
                   loader: Path = LOADER, path_prefix: Path | None = None) -> Result:
        env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT")}
        env["GIT_CEILING_DIRECTORIES"] = str(self.base)
        if project_dir is not None:
            env["CLAUDE_PROJECT_DIR"] = project_dir
        if path_prefix is not None:
            env["PATH"] = f"{path_prefix}{os.pathsep}{env.get('PATH', '')}"
        proc = subprocess.run(["/bin/sh", str(loader), *args], cwd=cwd, env=env,
                              capture_output=True, text=True, stdin=subprocess.DEVNULL)
        return Result(proc)

    def first_line(self, root: Path, team: str = "settings.md", local: str = "settings.local.md",
                   loader: Path = LOADER) -> str:
        return f"working-process settings (root: {root}; loader: {loader}; team: {team}; local: {local})"
```

Then the cases, one test method each (or a `subTest` table where the
cases share a shape), asserting the exact lines:

1. **Precedence and defaults.** `git_init()`; team `dir.default: tracked\n`,
   local `review.autonomy: yes\n`; hook mode from `self.root` → exit 0,
   empty stderr, `lines[0] == first_line(root)`, then exactly the 14 key
   lines in `KEYS` order and nothing after; among them
   `dir.default: tracked  [team]`, `dir.docs/specs: tracked  [inherited]`,
   `dir.docs/memory: tracked  [inherited]`,
   `dispatch.propagation-auditor-tier: cheapest  [default]`,
   `consult.personas: unset  [default]`, `review.autonomy: yes  [local]`.
   `--print` from the same place prints the identical text.
2. **Suggestion.** Team `consult.personas: yes\n`, no local file →
   `consult.personas: unset  [team suggests: yes]`, no `error:` line,
   first line ends `local: settings.local.md (absent))`. With local
   `consult.personas: no\n` → `consult.personas: no  [local]` and the
   string `suggests` appears nowhere in the output.
3. **Invalid in the deciding file.** Team `consult.personas: yes\n`,
   local `review.autonomy: noo\nconsult.personas: "no"\n` →
   `review.autonomy: unset  [invalid in local]`,
   `consult.personas: unset  [invalid in local]`, and the errors, in
   this order:
   ```
   error: settings.local.md:1 invalid value for `review.autonomy`: noo — unset
   error: settings.local.md:2 invalid value for `consult.personas`: "no" — unset
   ```
   The `consult.personas` line contains neither `yes` nor `suggests`.
4. **Duplicate.** Local `review.autonomy: yes\n\nreview.autonomy: no\n`
   → `review.autonomy: unset  [invalid in local]` and
   `error: settings.local.md:1,3 duplicate key `review.autonomy` — unset`;
   a duplicate where one line is also invalid gives the duplicate line
   alone.
5. **Unknown key, and a team key in the personal file.** Team
   `review.autonmy: yes\n` →
   `error: settings.md:1 unknown key `review.autonmy` — ignored`; local
   `dir.default: ignored\n` →
   `error: settings.local.md:1 team key `dir.default` in the personal file — ignored`
   and `dir.default: unset  [default]`.
6. **Inheritance.** Team `dir.default: ignored\ndir.docs/plans: tracked\n`
   → `dir.docs/plans: tracked  [team]`, `dir.docs/specs: ignored  [inherited]`,
   `dir..superpowers: ignored  [inherited]`. Team `dir.default: bogus\n`
   → `dir.default: unset  [invalid in team]`,
   `dir.docs/specs: unset  [inherited]`. Team
   `dir.default: tracked\ndir.docs/specs: bogus\n` →
   `dir.docs/specs: unset  [invalid in team]`.
7. **Fences and commentary.** Team file:
   ````
   # Team settings
   Note: dir.default: ignored
     dir.default: ignored
   ```
   dir.default: ignored
   ```
   dir.default: tracked
   ````
   → `dir.default: tracked  [team]` and no `error:` line. The same file
   with the last line removed → `dir.default: unset  [default]`.
8. **Whitespace.** Team `dir.default:\ttracked \r\n` → `[team]`; team
   `dir.default : tracked\n` → no settings line (commentary), so
   `[default]` and no error; team `dir.default:\n` →
   `error: settings.md:1 invalid value for `dir.default`: (empty) — unset`.
9. **Absent files and the first line.** `.working-process/` with only a
   team file → first line ends `team: settings.md; local: settings.local.md (absent))`;
   with only a local file → `team: settings.md (absent); local: settings.local.md)`.
   No `.working-process/` at all: hook mode → `out == ""`, `err == ""`,
   exit 0;
   `--print` → exactly one line,
   `working-process settings (root: {root}; loader: {LOADER}; no settings directory)`,
   exit 0.
10. **Root resolution.** No git, `project_dir=str(self.root)`, cwd a
    subdirectory `self.root / "sub"` → the first line names `self.root`
    and `err == ""`. No git and no project dir, cwd `self.root / "sub"`
    → names `self.root / "sub"`, `err == ""`. `git_init()`, cwd `self.root / "sub"`, project
    dir pointing elsewhere → names `self.root` (git wins).
11. **An error of the loader's own.** Copy `LOADER` to
    `self.base / "alone" / "scripts" / "load-settings.sh"` with no
    registry beside it; `.working-process/` present in `self.root`;
    hook mode → `out == ""`, `err == ""`, exit 0; `--print` → exit 1,
    `out == ""`, `err` contains `registry not found or empty`.
    Then a broken dependency: `shim = self.base / "shim"` holding an
    executable `awk` whose text is `#!/bin/sh\nexit 1\n` (mode
    `0o755`); team `dir.default: tracked\n`; hook mode with
    `path_prefix=shim` → `out == ""`, `err == ""`, exit 0; `--print`
    with the same prefix → exit 1, `out == ""`, `err` contains
    `loader failed`.
12. **The cap.** Team file of 200 lines `zz.k<i>: x` (`i` from 0) →
    hook mode: `len(out.encode()) <= 4096`, `out.endswith("\n")`,
    `lines[-1] == f"incomplete: run {LOADER} --print"`, `lines[0]` is
    the first line, `0 < len(errors) < 200`, and every error line is
    one of the 200 the file produces (none cut mid-line). `--print` →
    `len(errors) == 200` and no `incomplete:` line.
    Then the edge: team file of one line `zz.<pad>: x`, where `pad` is
    `k` repeated so that `--print`'s output is exactly 4096 bytes
    (measure once with `zz.k: x`, then lengthen the key by the
    difference: the error line echoes the key, so each added character
    adds one byte) → hook mode's `out` is byte-identical to `--print`'s
    and holds no `incomplete:` line. With one more `k` → hook mode's
    `len(out.encode()) <= 4096`, no `error:` line, and `lines[-1]` is
    the `incomplete:` line.
13. **Usage.** `--nonsense` → exit 2, `out == ""`, `err` one line
    starting `usage:`. `--print extra` → exit 2.

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_load_settings.py' -v 2>&1 | tail -n 5`
Expected: every test fails or errors — the script does not exist, so
`/bin/sh` exits 127.

- [ ] **Step 3: Write the script**

`plugins/working-process/scripts/load-settings.sh`, executable
(`chmod +x`), opening with `#!/bin/sh` and a comment block that names
the contract's home — the spec-plan-lifecycle rule is not it: the
process-settings rule (Task 6) defines the files, the grammar and the
block; the registry defines the keys; this plan's Tasks 2–5 the modes.
Match the contract above; add nothing it does not name. The functions:
`usage`, `die` (stderr + exit 1; the hook-mode wrapper, not `die`,
gives hook mode its silence),
`find_root`, `registry_keys`, `registry_field`, `scan_file`,
`resolve`, `emit_block`, `build_block` (the body `main` runs in the
subshell), `cap_block`, `main`. The block is built in a variable and
printed once.

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests/working-process -v`
Expected: every test in all three files passes.

Then run the script under dash by hand from this repository, which has
no `.working-process/`:

```bash
/bin/sh plugins/working-process/scripts/load-settings.sh; echo "rc=$?"
/bin/sh plugins/working-process/scripts/load-settings.sh --print; echo "rc=$?"
```

Expected: the first prints only `rc=0`; the second prints one line
ending `no settings directory)` and `rc=0`.

- [ ] **Step 5: Register the hook**

Replace the whole of `plugins/working-process/hooks/hooks.json` with:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/check-rules-drift.sh\""
          }
        ]
      },
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/load-settings.sh\""
          }
        ]
      }
    ]
  }
}
```

No `matcher` on either group, so both run on startup, resume, clear and
compaction. The loader is its own group rather than a second entry in
the first, since Codex budgets context per handler.

Verify:

```bash
python3 -c "import json; h=json.load(open('plugins/working-process/hooks/hooks.json'))['hooks']['SessionStart']; print(len(h), [g['hooks'][0]['command'].split('/')[-1] for g in h], all('matcher' not in g for g in h))"
claude plugin validate plugins/working-process
```

Expected: `2 ['check-rules-drift.sh"', 'load-settings.sh"'] True`, and
validation passes.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/scripts/load-settings.sh tests/working-process/test_load_settings.py plugins/working-process/hooks/hooks.json
git commit -m "feat(working-process): settings loader with hook mode and --print"
```

---

### Task 3: The loader — worktree and bare-repository layouts

**Files:**
- Modify: `plugins/working-process/scripts/load-settings.sh` —
  `find_root` gains the layout, `resolve` the fallback, `emit_block`
  the qualifiers.
- Modify: `tests/working-process/test_load_settings.py` — the layout
  helpers and cases 14–18.

**Interfaces:**
- Consumes: Task 2's script and helpers.
- Produces: `LAYOUT` (`main` | `worktree` | `bare-worktree` | `none`)
  and `MAIN` (the main checkout's root), which Task 5's destination
  logic reads; the `LOCAL_LABEL` qualifiers Task 6 quotes; the helpers
  `worktree()` and `bare()` Task 5's tests reuse.

**Realizes:** D5, D28, D41

**The contract — layouts.**

- `find_root` runs `git worktree list --porcelain` from `$ROOT` when git
  resolved the root. The first entry is the main worktree. Where its
  second line is `bare`, `LAYOUT=bare-worktree` and `MAIN` is empty.
  Where its path, made physical, equals `$ROOT`, `LAYOUT=main`.
  Otherwise `LAYOUT=worktree` and `MAIN` is that path. Where git did
  not resolve the root, `LAYOUT=none`. Paths are compared after
  `(cd "$p" && pwd -P)`, so a symlinked temporary directory compares
  equal on macOS.
- The personal file the loader reads (`LOCAL_READ`) and its label:
  - `main` or `none`: `$ROOT/.working-process/settings.local.md`,
    label `settings.local.md`;
  - `worktree`, the worktree's own file present:
    the worktree's, label `settings.local.md (worktree, shadows main checkout)`;
  - `worktree`, no own file: `$MAIN/.working-process/settings.local.md`,
    label `settings.local.md (main checkout)`;
  - `bare-worktree`: the worktree's own, label
    `settings.local.md (worktree, bare repository)`.
  Where the file the label names does not exist, `, absent` is added
  inside the parentheses — `settings.local.md (main checkout, absent)`,
  `settings.local.md (worktree, bare repository, absent)` — or
  ` (absent)` where there were none. The team file is always
  `$ROOT/.working-process/settings.md`.
- Error lines from the fallback file still name `settings.local.md`.
- The fallback is read only for the personal file. The team file is
  the current checkout's, `$ROOT/.working-process/settings.md`, and
  where it does not exist every team key takes its default and the
  label reads `settings.md (absent)`: a team answer travels with the
  branch that commits it (D50, spec *Scope and precedence*), so the
  main checkout's team file is never read from a worktree.
- Silence in the worktree layout. `LAYOUT=worktree` is silent in hook
  mode, and prints the `no settings directory` line under `--print`,
  only when neither `$DIR` nor `$MAIN/.working-process` is a
  directory. Where only the main checkout's exists, the block is
  emitted — `team: settings.md (absent)`, the personal file read from
  the main checkout — because D5 reads the main checkout's personal
  file wherever the worktree has none of its own, and D41 writes a
  personal answer where the loader reads it: `--set` from such a
  worktree writes the main checkout's file (Task 5, case 30), and the
  next session in that worktree must read it. The other layouts keep
  Task 2's test on `$DIR` alone.

- [ ] **Step 1: Write the failing tests**

Add to `LoaderTest`:

```python
    def worktree(self, main: Path, name: str) -> Path:
        """A linked worktree of `main` at main.parent/name on a new branch."""
        path = main.parent / name
        self.git(main, "worktree", "add", "-q", str(path), "-b", name)
        return path

    def bare(self, src: Path, name: str = "bare.git", worktree: str = "bwt") -> Path:
        """A bare clone of `src` with one linked worktree; returns the worktree."""
        bare = src.parent / name
        self.git(src.parent, "clone", "-q", "--bare", str(src), str(bare))
        path = src.parent / worktree
        self.git(bare, "worktree", "add", "-q", str(path), "main")
        return path
```

Cases:

14. **Fallback.** `main = git_init()`; `settings(main, team="dir.default: tracked\n", local="review.autonomy: yes\n")`;
    `wt = worktree(main, "wt")`; `settings(wt, team="dir.default: ignored\n")`;
    run from `wt` → `review.autonomy: yes  [local]`,
    `dir.default: ignored  [team]`, first line
    `first_line(wt, local="settings.local.md (main checkout)")`.
15. **Fallback absent.** As 14 without the main's local file → first
    line `local="settings.local.md (main checkout, absent)"` and
    `review.autonomy: unset  [default]`.
16. **Shadow.** As 14 plus `local="review.autonomy: no\n"` in `wt` →
    `review.autonomy: no  [local]`, first line
    `local="settings.local.md (worktree, shadows main checkout)"`, and
    `yes` appears on no line.
17. **Bare.** `src = git_init()`; `bwt = bare(src)`; `settings(bwt, team="dir.default: tracked\n")`;
    run from `bwt` → first line
    `local="settings.local.md (worktree, bare repository, absent)"`;
    then with `local="review.autonomy: yes\n"` in `bwt` →
    `review.autonomy: yes  [local]` and
    `local="settings.local.md (worktree, bare repository)"`.
18. **Worktree without a settings directory.** `main = git_init()` with
    `settings(main, team="dir.default: tracked\n", local="review.autonomy: yes\n")`,
    `wt = worktree(main, "wt")` without `.working-process/` → hook mode
    from `wt` prints the block: exit 0, first line
    `first_line(wt, team="settings.md (absent)", local="settings.local.md (main checkout)")`,
    `review.autonomy: yes  [local]`, `dir.default: unset  [default]` —
    the main checkout's team file is not read. Then `main` and `wt`
    both without `.working-process/` → hook mode from `wt` prints
    nothing, exit 0; `--print` prints the one `no settings directory`
    line naming `wt`.

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_load_settings.py' -v 2>&1 | tail -n 5`
Expected: cases 14–18 fail on the first line or the fallback value —
case 18 on the block Task 2's script withholds; every Task 2 case
passes.

- [ ] **Step 3: Extend the script**

Add the layout to `find_root`, `LOCAL_READ` and `LOCAL_LABEL` to
`resolve`/`emit_block`, and the worktree silence test to `build_block`,
as the contract says. `git worktree list --porcelain` runs once; its
first two lines are all `find_root` reads.

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests/working-process -v`
Expected: every test passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/scripts/load-settings.sh tests/working-process/test_load_settings.py
git commit -m "feat(working-process): settings loader reads the main checkout's personal file from a worktree"
```

---

### Task 4: The loader — `--validate`

**Files:**
- Modify: `plugins/working-process/scripts/load-settings.sh` —
  `do_validate`.
- Modify: `tests/working-process/test_load_settings.py` — cases 19–21.

**Interfaces:**
- Consumes: `scan_file` and `registry_field` from Task 2.
- Produces: the command
  `load-settings.sh --validate --scope team|personal <file>`, its
  `error:`, `notice:` and summary lines, and its exit codes, which
  Task 13's skill names for a hand-edited file.

**Realizes:** D28, D34, D46

**The contract — validation.**

- `--validate --scope <team|personal> <file>`: the two options in that
  order, then one path. Anything else, a scope other than the two, or a
  file that cannot be read → `usage:` on stderr, exit 2.
- The file is scanned as the deciding file of its scope. Each finding
  is one line on stdout, in line order:
  - `error: <basename>:<n> unknown key `<key>` — ignored`;
  - `error: <basename>:<n> invalid value for `<key>`: <raw> — unset`
    for a key of the file's scope; `— ignored` for a personal key in a
    file validated as `team`;
  - `error: <basename>:<n1>,<n2>[,…] duplicate key `<key>` — unset`, or
    `— ignored` for a personal key in a file validated as `team`, once
    per key;
  - `error: <basename>:<n> team key `<key>` in the personal file — ignored`
    for every line of a team key in a file validated as `personal`,
    whatever its value, and no other line for it;
  - `notice: <basename>:<n> personal key `<key>` in the team file — a suggestion`
    when the scope is `team` and the line is valid.
- The last line is `<basename>: <e> error(s), <m> notice(s)`, written
  with the literal words `errors` and `notices` (`0 errors, 1 notices`
  is accepted ugliness over a plural rule). Exit 1 when `e > 0`, else
  0. A notice never fails.
- `<basename>` is the file's basename as given, so a candidate file
  named otherwise (`settings.md.new`) reports under its own name.

- [ ] **Step 1: Write the failing tests**

19. **A suggestion passes.** File `t.md` = `consult.personas: yes\ndir.default: tracked\n`
    with `--scope team` → exit 0, stdout exactly:
    ```
    notice: t.md:1 personal key `consult.personas` in the team file — a suggestion
    t.md: 0 errors, 1 notices
    ```
20. **Each error kind fails.** One `subTest` per row; every row exits 1
    and its stdout contains the line given:
    - `--scope team`, `dir.default: bogus\n` →
      `error: t.md:1 invalid value for `dir.default`: bogus — unset`;
    - `--scope team`, `dir.default: tracked\ndir.default: ignored\n` →
      `error: t.md:1,2 duplicate key `dir.default` — unset`;
    - `--scope team`, `review.autonmy: yes\n` →
      `error: t.md:1 unknown key `review.autonmy` — ignored`;
    - `--scope personal`, `dir.default: tracked\n` →
      `error: t.md:1 team key `dir.default` in the personal file — ignored`;
    - `--scope team`, `consult.personas: maybe\n` →
      `error: t.md:1 invalid value for `consult.personas`: maybe — ignored`
      and no `notice:` line.
    Each row's last line is `t.md: 1 errors, 0 notices`.
21. **Usage.** `--validate t.md` (no scope), `--validate --scope both t.md`,
    `--validate --scope team missing.md` → exit 2, `out == ""`, `err`
    starts `usage:`.

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_load_settings.py' -v 2>&1 | tail -n 5`
Expected: cases 19 and 20 fail with exit 2 (the mode is unknown);
case 21 passes by accident and stays.

- [ ] **Step 3: Extend the script**

Add `do_validate` and its dispatch in `main`, reusing `scan_file` and
the registry lookups. The mode never consults `$ROOT`.

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests/working-process -v`
Expected: every test passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/scripts/load-settings.sh tests/working-process/test_load_settings.py
git commit -m "feat(working-process): settings loader validates a file for its scope"
```

---

### Task 5: The loader — `--set` and `--set --dry-run`

**Files:**
- Modify: `plugins/working-process/scripts/load-settings.sh` —
  `do_set`, `destination`, `plan_write`, `apply_write`.
- Modify: `tests/working-process/test_load_settings.py` — cases 22–34.

**Interfaces:**
- Consumes: `LAYOUT`, `MAIN`, `LOCAL_READ` from Task 3; `scan_file`,
  `registry_field`, `emit_block` from Task 2.
- Produces: the commands `load-settings.sh --set <key> <value>` and
  `load-settings.sh --set --dry-run <key> <value>`, their output lines
  and exit codes, which Task 6's rule, Task 13's skill and the "and
  record" answers in Tasks 7–12 call.

**Realizes:** D24, D28, D37, D41, D43, D49, D50

**The contract — writing.**

- `--set <key> <value>` and `--set --dry-run <key> <value>`; any other
  shape → `usage:`, exit 2. `--set` takes no scope: the registry fixes
  it.
- **Validation first.** An unregistered key →
  `error: unknown key `<key>`` on stderr, exit 1. A value not among the
  key's `values:` → `error: invalid value for `<key>`: <value> (allowed: <values as the registry writes them>)`
  on stderr, exit 1. Nothing is created before both pass.
- **Destination** (`destination`): a team key → `$ROOT/.working-process/settings.md`
  in the checkout the command runs in, label `settings.md`. A personal
  key: `LAYOUT` `main` or `none` → `$ROOT/.working-process/settings.local.md`,
  label `settings.local.md`; `worktree` → `$MAIN/.working-process/settings.local.md`,
  label `settings.local.md (main checkout)`, and where the current
  worktree has a personal file of its own, the note
  `note: settings.local.md in this worktree shadows the main checkout; this write will not change the current worktree's answer`
  is printed first; `bare-worktree` → the worktree's own file, label
  `settings.local.md (worktree, bare repository)`. Nothing is ever
  written inside a bare repository.
- **The plan** (`plan_write`), computed from the destination's current
  content, which may not exist: with no record for the key — *insert*:
  append, after a blank line where the file is non-empty and its last
  line is not blank, the key's `question:` text as one commentary line,
  then `<key>: <value>`; a file that does not exist is created with
  the title line `# working-process settings` (team) or
  `# working-process settings — personal` (personal), a blank line,
  then the question and the key line (Deviation 5). With exactly one
  record — *replace* that line in place with `<key>: <value>`, every
  other line untouched; where that record's value already equals
  `<value>` — compared as the grammar reads it, so a trailing `\r` does
  not count — *unchanged*, no write. With several records —
  *replace the first* in place and *remove* each later record's line,
  together with the line directly above it when that line equals the
  key's `question:` text exactly; other lines, blank lines included,
  stay.
- **Line endings.** The file is rewritten line by line, and two
  normalizations are the only bytes a write may change outside the
  lines it names: a last line lacking a final newline gains one, and
  the lines `--set` writes end in LF. A CRLF ending on an untouched
  line is preserved — the `\r` is part of the line's text and is
  written back; the grammar strips it only when reading the value. An
  *unchanged* file is not rewritten, so it gains nothing.
- **The `.gitignore`** beside a personal destination: absent → created
  holding the single line `settings.local.md`; present without a line
  equal to `settings.local.md` → that line appended (Deviation 4);
  present with it → untouched. Never touched for a team key.
- **Other errors** in the destination file (D49) are reported as the
  block would report them — `error: <basename>:<n> …` lines, computed
  before the write — and never block it.
- **Output** of `--set`, on stdout, in this order: the shadow note if
  any; the `error:` lines for other lines; one
  `removed <label>:<n> <line text>` per removed line, in line order,
  with the numbers of the file before the write; then one of
  `wrote <label>: <key>: <value> (inserted)`,
  `wrote <label>: <key>: <value> (replaced)`,
  `unchanged <label>: <key>: <value>`; then, where they happened,
  `created .working-process/settings.md`,
  `created .working-process/settings.local.md`,
  `created .working-process/.gitignore — commit it with settings.md`,
  `appended settings.local.md to .working-process/.gitignore`; then a
  blank line and the fresh block, resolved after the write exactly as
  `--print` prints it from the current checkout. Exit 0.
- **`--set --dry-run`** prints the same lines with `would remove`,
  `would write`, `would leave unchanged`, `would create`,
  `would append`, and the note and the `error:` lines unchanged; no
  block; it writes nothing and creates no directory. Exit 0 after a
  valid key and value, 1 and 2 as above.
- **Writes** go to `<file>.tmp.$$` beside the destination and are
  moved into place, as `write-manifest.sh` does, under the same
  `trap 'rm -f "$tmp"' EXIT`, cleared after the move, so a write that
  fails leaves no temp file behind; `.working-process/` is created
  with `mkdir -p` where absent (the first write in a project without
  settings — D51 — is this path, called by the skill).

- [ ] **Step 1: Write the failing tests**

Add a helper to `LoaderTest`:

```python
    QUESTION = "May the review loop run autonomously, within the round cap?"

    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")
```

Cases:

22. **Insert, personal, creating everything.** `git_init()`, no
    `.working-process/`; `--set review.autonomy yes` from `self.root`
    → exit 0; `self.root/.working-process/settings.local.md` reads
    `# working-process settings — personal\n\n{QUESTION}\nreview.autonomy: yes\n`;
    `.gitignore` reads `settings.local.md\n`; `settings.md` does not
    exist; stdout lines include, in order,
    `wrote settings.local.md: review.autonomy: yes (inserted)`,
    `created .working-process/settings.local.md`,
    `created .working-process/.gitignore — commit it with settings.md`,
    then a blank line, then the block whose first line is
    `first_line(root, team="settings.md (absent)")` and which carries
    `review.autonomy: yes  [local]`.
23. **Insert, team.** `--set dir.default tracked` → `settings.md` reads
    `# working-process settings\n\nWhich mode does a Process directory get unless an exception names it — tracked or ignored?\ndir.default: tracked\n`;
    no `.gitignore` is created; stdout has `wrote settings.md: dir.default: tracked (inserted)`
    and `created .working-process/settings.md`.
24. **Insert into an existing file.** Team file `# Team\n\ndir.default: tracked\n`
    (no trailing blank line); `--set docs-branch.merge squash` → the
    file reads the original, then `\nHow does the topic branch take the .docs branch at the implementation-ready gate — squash or fast-forward?\ndocs-branch.merge: squash\n`
    appended, and every earlier byte identical. The same fixture
    without its final newline (`write_bytes`) → a byte-identical
    result: the missing newline is added first.
25. **Replace.** Local `intro\n\n{QUESTION}\nreview.autonomy: yes\n\nconsult.personas: no\n`;
    `--set review.autonomy no` → the file differs from the original in
    exactly one line, `review.autonomy: no`; stdout has
    `wrote settings.local.md: review.autonomy: no (replaced)`. Then
    CRLF: local written as bytes
    `b"intro\r\nreview.autonomy: yes\r\nconsult.personas: no\r\n"`;
    `--set review.autonomy no` → `read_bytes()` equals
    `b"intro\r\nreview.autonomy: no\nconsult.personas: no\r\n"` — the
    untouched lines keep CRLF, the written line ends in LF.
26. **Unchanged.** The file of case 25 with `--set review.autonomy yes`
    → `tree_hash` of `.working-process` equal before and after; stdout
    has `unchanged settings.local.md: review.autonomy: yes` and the
    block. Then a CRLF record: local `b"review.autonomy: yes\r\n"` with
    `--set review.autonomy yes` → `unchanged`, `tree_hash` equal.
27. **Duplicate.** Local `{QUESTION}\nreview.autonomy: yes\nfoo\n{QUESTION}\nreview.autonomy: no\nbar\nreview.autonomy: maybe\n`;
    `--set review.autonomy no` → the file reads
    `{QUESTION}\nreview.autonomy: no\nfoo\nbar\n`; stdout has, in order,
    `removed settings.local.md:4 {QUESTION}`,
    `removed settings.local.md:5 review.autonomy: no`,
    `removed settings.local.md:7 review.autonomy: maybe`,
    `wrote settings.local.md: review.autonomy: no (replaced)`.
28. **Another line's error is reported, not blocking (D49).** Local
    `review.autonmy: yes\n`; `--set review.autonomy no` → exit 0, the
    file gains the question and key line after a blank line, stdout has
    `error: settings.local.md:1 unknown key `review.autonmy` — ignored`
    before `wrote settings.local.md: review.autonomy: no (inserted)`.
29. **Validation.** `--set review.autonomy maybe` → exit 1, `out == ""`,
    `err` = `error: invalid value for `review.autonomy`: maybe (allowed: yes | no)\n`,
    and no `.working-process/` created; `--set nosuch.key yes` → exit 1,
    `err` = `error: unknown key `nosuch.key`\n`; `--set review.autonomy`
    → exit 2.
30. **Destination from a worktree.** `main = git_init()`, `wt = worktree(main, "wt")`;
    `--set review.autonomy yes` from `wt` → `main/.working-process/settings.local.md`
    and `main/.working-process/.gitignore` exist with the case-22
    contents; `wt/.working-process/` does not exist; stdout has
    `wrote settings.local.md (main checkout): review.autonomy: yes (inserted)`,
    and the block at the end opens with
    `first_line(wt, team="settings.md (absent)", local="settings.local.md (main checkout)")`
    and carries `review.autonomy: yes  [local]` — the answer just
    written is read from the worktree (Task 3, case 18). Then
    `--set dir.default tracked` from `wt` → `wt/.working-process/settings.md`
    exists, `main/.working-process/settings.md` does not, and the block
    opens with `first_line(wt, local="settings.local.md (main checkout)")`
    and carries `dir.default: tracked  [team]`.
31. **Shadow.** As 30, plus `settings(wt, local="review.autonomy: no\n")`;
    `--set review.autonomy yes` from `wt` → `main`'s file gains the
    key, `wt`'s file is byte-identical, `lines[0]` is the shadow note
    verbatim, and the block at the end reads `review.autonomy: no  [local]`
    (the worktree's own file still decides).
32. **Bare.** `bwt = bare(git_init())`; `--set review.autonomy yes` from
    `bwt` → `bwt/.working-process/settings.local.md` and `.gitignore`
    exist; `tree_hash(bare.git)` equal before and after; stdout has
    `wrote settings.local.md (worktree, bare repository): review.autonomy: yes (inserted)`.
33. **Dry run.** For each of cases 22, 25, 27, 30 and 31, run
    `--set --dry-run` with the same arguments: exit 0, `tree_hash(self.base)`
    equal before and after, no `.working-process/` created where there
    was none, no line starting `working-process settings`, and stdout
    lines `would write …`, `would remove settings.local.md:4 {QUESTION}`
    (case 27), `would create .working-process/.gitignore — commit it with settings.md`
    (cases 22 and 30) and the shadow note (case 31) as the contract
    words them.
34. **An existing `.gitignore` without the line.** `settings(root, gitignore="*.bak\n")`;
    `--set review.autonomy yes` → `.gitignore` reads `*.bak\nsettings.local.md\n`,
    stdout has `appended settings.local.md to .working-process/.gitignore`.

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest discover -s tests/working-process -p 'test_load_settings.py' -v 2>&1 | tail -n 5`
Expected: cases 22–34 fail with exit 2 or on missing files; every
earlier case passes.

- [ ] **Step 3: Extend the script**

Add `destination`, `plan_write`, `apply_write` and `do_set`, and the
dispatch in `main`. `plan_write` computes every output line and the
new file content from the scan records; `apply_write` is the only
function that creates or moves a file, and `--dry-run` never calls it.

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests/working-process -v`
Expected: every test passes.

Then the round trip by hand, in a scratch directory, under dash:

```bash
W=$(mktemp -d); L=$(pwd)/plugins/working-process/scripts/load-settings.sh
(cd "$W" && git init -q && /bin/sh "$L" --set --dry-run review.autonomy yes && echo --- \
  && /bin/sh "$L" --set review.autonomy yes | head -n 4 && echo --- \
  && /bin/sh "$L" --validate --scope personal .working-process/settings.local.md; echo "rc=$?"; cat .working-process/.gitignore)
command rm -rf "$W"
```

Expected: the dry run prints `would write settings.local.md: review.autonomy: yes (inserted)`
and two `would create` lines and no block; the write prints
`wrote settings.local.md: review.autonomy: yes (inserted)`, the two
`created` lines and a blank line; the validation prints
`settings.local.md: 0 errors, 0 notices` and `rc=0`; the last line is
`settings.local.md`.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/scripts/load-settings.sh tests/working-process/test_load_settings.py
git commit -m "feat(working-process): settings loader writes an answer with --set"
```

---

### Task 6: The always-on rule `process-settings.md`

**Files:**
- Create: `plugins/working-process/rules/process-settings.md`

**Interfaces:**
- Consumes: the block's first line, source tokens, `error:` and
  `incomplete:` lines from Task 2; the layout qualifiers from Task 3;
  the `--set` command from Task 5.
- Produces: the rule name `process-settings`, which Tasks 7–13 cite as
  "read as the process-settings rule says"; the four-step read every
  reader defers to.

**Realizes:** D1, D2, D3, D4, D12, D13, D14, D15, D18, D19, D20, D38, D44

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/process-settings.md
ls $F 2>&1 | head -n 1
plugins/working-process/scripts/ruleset-hash.sh plugins/working-process/rules
```

Expected: `ls` reports no such file; the hash line is the payload's
current aggregate — write it down, Step 3 expects a different one.

- [ ] **Step 2: Write the rule**

`plugins/working-process/rules/process-settings.md`, no frontmatter
(an always-on process rule, the deliberate exception the
plugin-authoring rule names), exactly:

````
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
````

- [ ] **Step 3: Verify**

```bash
F=plugins/working-process/rules/process-settings.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(head -n 1 $F)"
echo "B $(grep -c '^## ' $F)"
echo "C $(grep -c '^working-process settings (root: <path>; loader: <path>; team: settings.md; local: settings.local.md)$' $F)"
echo "D $(n $F | grep -oF 'incomplete: run <loader> --print' | wc -l)"
echo "E $(n $F | grep -oF 'Never resolve the files by hand' | wc -l)"
echo "F $(n $F | grep -oF 'never `dir.default`' | wc -l)"
echo "G $(n $F | grep -oF 'is not `.claude/working-process/`' | wc -l)"
echo "H $(grep -c '^---$' $F)"
echo "I $(wc -l < $F)"
awk 'length > 72 && !/^working-process settings/ {print "long: " $0}' $F
plugins/working-process/scripts/ruleset-hash.sh plugins/working-process/rules
```

Expected: `A # Process settings`, `B 5`, `C 1`, `D 1`, `E 1`, `F 1`,
`G 1`, `H 0` (no frontmatter), `I` between 95 and 110, no `long:` line,
and a hash different from Step 1's — the Rules payload changed, which
is what makes every installed copy nudge for a re-sync.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/rules/process-settings.md
git commit -m "feat(working-process): process-settings rule"
```

---

### Task 7: Workflow rule — the consents and the technical-design declaration

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — step 1 of the
  flow (persona consent and the compaction clause), step 4 (the
  technical-design declaration and its "and record"), and the review
  loop's autonomy question.

**Interfaces:**
- Consumes: the key names from Task 1; the rule name and read from
  Task 6; the `--set` command from Task 5.
- Produces: nothing a later task reads; Task 14 checks that this file
  cites `consult.personas`, `review.autonomy`,
  `review.per-round-commit` and `design.technical-design-offer`.

**Realizes:** D14, D16, D19, D20

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/workflow.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $F | grep -oF 'a durable preference belongs in the developer' | wc -l)"
echo "B $(n $F | grep -oF 'A durable preference in the developer' | wc -l)"
echo "C $(n $F | grep -oF 'until a standing home for a project' | wc -l)"
echo "D $(n $F | grep -oF 'unless `consult.personas`' | wc -l)"
echo "E $(n $F | grep -oF '`design.technical-design-offer`' | wc -l)"
echo "F $(n $F | grep -oF 'records the first clause alone' | wc -l)"
echo "G $(n $F | grep -oF 'a recorded key is simply read again' | wc -l)"
echo "H $(n $F | grep -oF 'which writes `on`' | wc -l)"
echo "I $(n $F | grep -oF 'the key wins and the session says so' | wc -l)"
echo "J $(n $F | grep -oF 'and record' | wc -l)"
echo "K $(n $F | grep -oF 'leaves the current consent state unclear' | wc -l)"
```

Expected: `A 1`, `B 1`, `C 1`, `D 0`, `E 0`, `F 0`, `G 0`, `H 0`,
`I 0`, `J 0`, `K 1`.

- [ ] **Step 2: Persona consent reads `consult.personas`**

Find in `plugins/working-process/rules/workflow.md`:

```
   should be consulted as the design forms — yes / not now / not in this
   session (honoured for the Claude Code session only; a durable
   preference belongs in the developer's own instructions and is
   respected when present). After a yes, dispatch a consultation when it
   looks worth its cost, without asking again for that conversation, and
   state the consent decision whenever it is made or changed — and when
   a compacted conversation leaves the current consent state unclear,
   ask again rather than guess. On a
```

Replace with:

```
   should be consulted as the design forms — unless `consult.personas`,
   read as the process-settings rule says, is set, which answers it
   unasked. The answers are yes / not now / not in this session, and
   "yes, and record" or "no, and record", which write the key through
   the loader's `--set` where a settings block names the loader; "not
   now" and "not in this session" are honoured for the Claude Code
   session only and are never recorded. After a yes, dispatch a
   consultation when it looks worth its cost, without asking again for
   that conversation, and state the consent decision whenever it is
   made or changed — and when a compacted conversation leaves the state
   of a consent given in this session unclear, ask again rather than
   guess; a recorded key is simply read again. On a
```

- [ ] **Step 3: The technical-design declaration names its key**

Find in `plugins/working-process/rules/workflow.md`:

```
   At the same gate, and before the integrity audit above, offer the
   technical design when the repository is one that has code. A
   declaration the project records binds and is never re-asked, in
   either direction; a session reads it from the project instructions
   Claude Code loads at session start — a `CLAUDE.md` at the repository
   root or in `.claude/` — or from the file such a note points at, which
   is the shape available until a standing home for a project's process
   answers exists. Without a declaration, a repository carrying a
```

Replace with:

```
   At the same gate, and before the integrity audit above, offer the
   technical design when the repository is one that has code. A
   declaration the project records binds and is never re-asked, in
   either direction. Its home is the settings key
   `design.technical-design-offer`, read as the process-settings rule
   says: `on` makes the offer at every consumption gate whether or not
   a manifest is present, `off` suppresses it. Until a project migrates
   to the key, a note in the project instructions Claude Code loads at
   session start — a `CLAUDE.md` at the repository root or in
   `.claude/` — or in the file such a note points at, declares it too;
   where the note and the key disagree, the key wins and the session
   says so. Without a declaration, a repository carrying a
```

Find in `plugins/working-process/rules/workflow.md`:

```
   design. A session may propose writing the declaration and never
   writes it unasked. A change may skip the document when it
```

Replace with:

```
   design. A session may propose writing the declaration and never
   writes it unasked: the offer's answers include "yes, and record",
   which writes `on`, and "no, and record", which writes `off`, through
   the loader's `--set` where a settings block names the loader. A
   change may skip the document when it
```

- [ ] **Step 4: The autonomy question reads its two keys**

Find in `plugins/working-process/rules/workflow.md`:

```
without asking again. The same question carries a second clause wherever
the lifecycle rule's per-round commits are available: whether the loop
may commit the reviewed document once per round. One question, two
answers, asked once. A durable preference in the developer's own
instructions is respected when present. Without consent every round
behaves as it did before: relay, stamp, and every proposal waits for
the developer.
```

Replace with:

```
without asking again. The same question carries a second clause wherever
the lifecycle rule's per-round commits are available: whether the loop
may commit the reviewed document once per round. One question, two
answers, asked once. Each clause has a settings key, `review.autonomy`
and `review.per-round-commit`, read as the process-settings rule says:
a set key answers its clause unasked, and only an unset clause is
asked. A yes or no may be given "and record" per clause — "yes, and
record; commits: not now" records the first clause alone — which
writes that clause's key through the loader's `--set` where a settings
block names the loader; "not now" and "not in this session" are never
recorded. Without consent every round
behaves as it did before: relay, stamp, and every proposal waits for
the developer.
```

- [ ] **Step 5: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 0`, `C 0`, `D 1`, `E 1`, `F 1`, `G 1`, `H 1`,
`I 1`, `J 6`, `K 0`.

`J 6`: two "and record" answers in step 1, two behind the
technical-design offer, and two in the autonomy paragraph.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): workflow consents and the technical-design declaration read settings keys"
```

---

### Task 8: The propagation gate's tier — workflow table and the two auditor cards

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the
  model-selection paragraph and a table after it.
- Modify: `plugins/working-process/agents/propagation-auditor.md` — the
  `description:` line and `## Your tier, and the self-report that proves it`.
- Modify: `plugins/working-process/agents/integrity-auditor.md` — one
  out-of-bounds bullet.

**Interfaces:**
- Consumes: the key `dispatch.propagation-auditor-tier` and its values
  from Task 1; Task 7's edits to `workflow.md`, none of which touch
  this task's anchors.
- Produces: the tier table Task 15's README names; Task 14 checks that
  `workflow.md` and the propagation auditor's card cite the key.

**Realizes:** D35, D47

- [ ] **Step 1: Record the before values**

```bash
W=plugins/working-process/rules/workflow.md
P=plugins/working-process/agents/propagation-auditor.md
I=plugins/working-process/agents/integrity-auditor.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $W | grep -oF 'dispatches on the cheapest available family and the `integrity-auditor`' | wc -l)"
echo "B $(grep -c '^| `cheapest` | the cheapest available family |$' $W)"
echo "C $(grep -c '^| `most-capable` | the most capable available |$' $W)"
echo "D $(n $W | grep -oF 'never a model name' | wc -l)"
echo "E $(n $P | grep -oF 'You run on the cheapest available family' | wc -l)"
echo "F $(n $P | grep -oF 'casually badly' | wc -l)"
echo "G $(n $P | grep -oF 'Run it on the cheapest available family' | wc -l)"
echo "H $(n $P | grep -oE 'resolved from (the project.s )?`dispatch\.propagation-auditor-tier`' | wc -l)"
echo "I $(n $P | grep -oF 'A project may choose a higher tier' | wc -l)"
echo "J $(head -n 5 $P | grep -c '^description: "')"
echo "K $(n $I | grep -oF 'on the cheapest available family, and re-running' | wc -l)"
echo "L $(n $I | grep -oF 'on the tier the dispatcher resolved for it' | wc -l)"
```

Expected: `A 1`, `B 0`, `C 0`, `D 0`, `E 1`, `F 2`, `G 1`, `H 0`,
`I 0`, `J 1`, `K 1`, `L 0`.

- [ ] **Step 2: The workflow rule resolves the tier from the key**

Find in `plugins/working-process/rules/workflow.md`:

```
never-cheapest floor governs reviews alone: the `propagation-auditor`
dispatches on the cheapest available family and the `integrity-auditor`
on the most capable available, each named explicitly. Both reports open
```

Replace with:

```
never-cheapest floor governs reviews alone: the `propagation-auditor`
dispatches on the tier `dispatch.propagation-auditor-tier` resolves
to — read as the process-settings rule says, `cheapest` unless the
project sets `mid` or `most-capable` — and the `integrity-auditor`
on the most capable available, each named explicitly; the key's value
is a tier, never a model name, and Claude Code resolves it through the
table below this paragraph. Both reports open
```

Find in `plugins/working-process/rules/workflow.md`:

```
the prescribed tier is recorded and offered a re-review per the
spec-plan-lifecycle rule, when installed.

Dispatching a consultation, when the consult agents are available: one
```

Replace with:

```
the prescribed tier is recorded and offered a re-review per the
spec-plan-lifecycle rule, when installed.

| `dispatch.propagation-auditor-tier` | Claude Code rung |
|---|---|
| `cheapest` | the cheapest available family |
| `mid` | the family one below the most capable |
| `most-capable` | the most capable available |

Dispatching a consultation, when the consult agents are available: one
```

- [ ] **Step 3: The propagation auditor accepts the resolved tier**

Find in `plugins/working-process/agents/propagation-auditor.md`:

```
Run it on the cheapest available family, named explicitly — every duty is procedural, and the never-cheapest rule governs reviews, which an audit is not.
```

Replace with:

```
Run it on the tier the dispatcher resolved from `dispatch.propagation-auditor-tier`, named explicitly — the cheapest available family by default, since every duty is procedural, and the never-cheapest rule governs reviews, which an audit is not.
```

The anchor is inside the one-line `description:` value; the value
stays one quoted line.

Find in `plugins/working-process/agents/propagation-auditor.md`:

```
You run on the cheapest available family, named explicitly at dispatch —
the inverse of the rule governing verdict dispatches, and the point of
the split: every duty below is procedural (parse, enumerate, count,
diff), which a capable model does casually badly and a cheap model does
well when told to derive by counting.
```

Replace with:

```
You run on the tier the dispatcher resolved from the project's
`dispatch.propagation-auditor-tier`, named explicitly at dispatch. Its
default is the cheapest available family — the inverse of the rule
governing verdict dispatches, and the point of the split: every duty
below is procedural (parse, enumerate, count, diff), which a cheap
model does well when told to derive by counting. A project may choose
a higher tier, and the dispatched string records which.
```

Find in `plugins/working-process/agents/propagation-auditor.md`:

```
ignore. The dispatched string is the record of what ran. Your exposure runs upward: below the cheapest family
there is no rung, but an omitted model inherits the session's model, and
an over-tier run does this work casually badly — a false clean line would
then feed the integrity gate unnoticed. A mismatched run earns no
reliance and is re-dispatched at the right rung.
```

Replace with:

```
ignore. The dispatched string is the record of what ran. An omitted
model inherits the session's model, which is why the dispatcher names
one; a family other than the dispatched one, in either direction, is a
mismatch. A mismatched run earns no
reliance and is re-dispatched at the right rung.
```

- [ ] **Step 4: The integrity auditor's bullet follows the resolved tier**

Find in `plugins/working-process/agents/integrity-auditor.md`:

```
  boundary sentences. That pass runs before yours, on the cheapest
  available family, and re-running it here spends the tier on arithmetic.
```

Replace with:

```
  boundary sentences. That pass runs before yours, on the tier the
  dispatcher resolved for it — the cheapest available family unless the
  project set another — and re-running it here spends the tier on
  arithmetic.
```

- [ ] **Step 5: Verify**

Run the Step 1 command again, then `claude plugin validate plugins/working-process`.

Expected: `A 0`, `B 1`, `C 1`, `D 1`, `E 0`, `F 0`, `G 0`, `H 2`,
`I 1`, `J 1`, `K 0`, `L 1`, and validation passes.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/workflow.md plugins/working-process/agents/propagation-auditor.md plugins/working-process/agents/integrity-auditor.md
git commit -m "feat(working-process): the propagation gate's tier is a settings key"
```

---

### Task 9: Lifecycle rule — per-round commit consent and the `.docs` branch merge

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the
  consent-question paragraph and the merge paragraph under the
  per-round commits convention.

**Interfaces:**
- Consumes: the keys `review.per-round-commit` and `docs-branch.merge`
  from Task 1; the rule name from Task 6.
- Produces: nothing a later task reads; Task 14 checks the two
  citations.

**Realizes:** D16, D20

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $F | grep -oF 'so a `CLAUDE.md` note — at the repo root or beside the documents — records it where it binds, and a session with no such note asks at the gate' | wc -l)"
echo "B $(n $F | grep -oF '`docs-branch.merge`' | wc -l)"
echo "C $(n $F | grep -oF '`review.per-round-commit`' | wc -l)"
echo "D $(n $F | grep -oF 'squash, and record' | wc -l)"
echo "E $(n $F | grep -oF 'the key winning where the two disagree' | wc -l)"
echo "F $(n $F | grep -oF 'while the suggestion may not. A set' | wc -l)"
```

Expected: `A 1`, `B 0`, `C 0`, `D 0`, `E 0`, `F 0`.

- [ ] **Step 2: The consent question reads its key**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
mechanism — and a "no" leaves the authoring phase exactly as this
paragraph describes it. That is why it may be asked during authoring
while the suggestion may not.
```

Replace with:

```
mechanism — and a "no" leaves the authoring phase exactly as this
paragraph describes it. That is why it may be asked during authoring
while the suggestion may not. A set `review.per-round-commit`, read as
the process-settings rule says, is that standing authorization already
given or withheld, and the clause is not asked; unset, it is asked as
the workflow rule's review loop says, "and record" among its answers.
```

- [ ] **Step 3: The merge choice reads its key**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
implementation-ready gate: by fast-forward where the history is wanted
whole, by squash where it is not. That choice belongs to the project
rather than the session, so a `CLAUDE.md` note — at the repo root or
beside the documents — records it where it binds, and a session with no
such note asks at the gate. Either way the document branch survives the
```

Replace with:

```
implementation-ready gate: by fast-forward where the history is wanted
whole, by squash where it is not. That choice belongs to the project
rather than the session, so the settings key `docs-branch.merge` —
`squash` or `fast-forward`, read as the process-settings rule says —
records it where it binds. Until a project migrates to the key, a
`CLAUDE.md` note — at the repo root or beside the documents — declares
it too, the key winning where the two disagree. A session with neither
asks at the gate, and the answers include "squash, and record" and
"fast-forward, and record", which write the key through the loader's
`--set` where a settings block names the loader. Either way the
document branch survives the
```

- [ ] **Step 4: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 1`, `C 1`, `D 1`, `E 1`, `F 1`.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): per-round commit consent and the docs-branch merge read settings keys"
```

---

### Task 10: Directory modes — the settings key among the signals, the local pocket on the resolved mode

**Files:**
- Modify: `plugins/working-process/rules/process-artifacts.md` — the
  first-create paragraph, the signal paragraph, the `docs/memory/`
  paragraph.
- Modify: `plugins/working-process/rules/review-reports.md` — the first
  sentence of `## Local pocket (tracked mode only)`.

**Interfaces:**
- Consumes: the `dir.` keys from Task 1; the rule name from Task 6; the
  `--set` command from Task 5.
- Produces: the four-step order Tasks 11 and 12 restate for their own
  directories; Task 14 checks that this file cites `dir.default` and
  the six exceptions it owns.

**Realizes:** D17, D18, D32, D45

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/process-artifacts.md
R=plugins/working-process/rules/review-reports.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $F | grep -oF 'git-tracked file under it, and no explicit project instruction declaring the mode) — ASK' | wc -l)"
echo "B $(n $F | grep -oF 'no settings key deciding it' | wc -l)"
echo "C $(n $F | grep -oF 'Never ask when any signal is already present: only' | wc -l)"
echo "D $(n $F | grep -oF 'Never ask when any signal is already present. Two signals are visible' | wc -l)"
echo "E $(n $F | grep -oF '`dir..superpowers`' | wc -l)"
echo "F $(grep -c '^[1-4]\. ' $F)"
echo "G $(n $F | grep -oF 'never `dir.default`, which only the `process-setup` skill writes' | wc -l)"
echo "H $(n $F | grep -oF 'it is configuration, never asked about' | wc -l)"
echo "I $(n $F | grep -oF 'reads its own exception, `dir.docs/memory`' | wc -l)"
echo "J $(n $R | grep -oF 'When the first-create question resolves to tracked mode for `docs/code-review/`' | wc -l)"
echo "K $(n $R | grep -oF 'or unasked by a signal or a settings key' | wc -l)"
```

Expected: `A 1`, `B 0`, `C 1`, `D 0`, `E 0`, `F 0`, `G 0`, `H 0`,
`I 0`, `J 1`, `K 0`.

- [ ] **Step 2: The first-create paragraph names the key**

Find in `plugins/working-process/rules/process-artifacts.md`:

```
When creating a Process directory — or touching one that already exists
with no prior decision (no `.gitignore` containing exactly `*`, no
git-tracked file under it, and no explicit project instruction
declaring the mode) — ASK the developer which mode the directory gets.
Assume no default:
```

Replace with:

```
When creating a Process directory — or touching one that already exists
with no prior decision (no `.gitignore` containing exactly `*`, no
git-tracked file under it, no settings key deciding it, and no explicit
project instruction declaring the mode) — ASK the developer which mode
the directory gets. Assume no default:
```

- [ ] **Step 3: The signal paragraph gains the key and the order**

Find in `plugins/working-process/rules/process-artifacts.md`:

```
Never ask when any signal is already present: only a `.gitignore`
containing exactly `*` means ignored mode was chosen — one with any
other content (e.g. a local pocket's `local-*`) signals nothing by
itself; a git-tracked file under the directory (`git ls-files <dir>`
non-empty) means tracked mode was chosen; and an
explicit project instruction declaring the mode (e.g. a CLAUDE.md
note that a directory is always git-ignored) counts as the decision.
A declared ignored mode is materialized by whoever first acts on it —
writing the `*` `.gitignore` — making the decision observable; a
declared tracked mode becomes observable with the first committed
file. This rule owns the signal list; other surfaces reference it
rather than restating it (the self-contained restatements of the review commands
and the project-memory core rule are the justified exceptions).
```

Replace with:

```
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
```

- [ ] **Step 4: The `docs/memory/` paragraph names its reader**

Find in `plugins/working-process/rules/process-artifacts.md`:

```
`docs/memory/`'s tracked/ignored first-create question is asked by the
project-memory plugin's core rule (when installed), not this one — it is
listed above only so `docs/memory/` counts as a Process directory for the
conventions below.
```

Replace with:

```
`docs/memory/`'s tracked/ignored first-create question is asked by the
project-memory plugin's core rule (when installed), not this one, and
that rule reads its own exception, `dir.docs/memory`, in the same
order — it is listed above only so `docs/memory/` counts as a Process
directory for the conventions below.
```

- [ ] **Step 5: The local pocket fires on the resolved mode**

Find in `plugins/working-process/rules/review-reports.md`:

```
When the first-create question resolves to tracked mode for
`docs/code-review/`, also write `docs/code-review/.gitignore`
```

Replace with:

```
When `docs/code-review/` resolves to tracked mode — by the first-create
question, or unasked by a signal or a settings key, in the order the
process-artifacts rule gives — also write `docs/code-review/.gitignore`
```

- [ ] **Step 6: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 1`, `C 0`, `D 1`, `E 1`, `F 4`, `G 1`, `H 1`,
`I 1`, `J 0`, `K 1`.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/process-artifacts.md plugins/working-process/rules/review-reports.md
git commit -m "feat(working-process): a settings key joins the directory-mode signals"
```

---

### Task 11: Project-memory rule — `dir.docs/memory` and the conflict question

**Files:**
- Modify: `plugins/project-memory/rules/project-memory.md` — the
  "Never ask when a prior decision is present" paragraph under
  `## Adoption`.

**Interfaces:**
- Consumes: the key `dir.docs/memory` from Task 1; the order from
  Task 10, restated here because this rule stands alone.
- Produces: nothing a later task reads; Task 14 checks the citation.

**Realizes:** D7.14, D25, D40

- [ ] **Step 1: Record the before values**

```bash
F=plugins/project-memory/rules/project-memory.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $F | grep -oF 'first committed file. Private memory' | wc -l)"
echo "B $(n $F | grep -oF '`dir.docs/memory`' | wc -l)"
echo "C $(n $F | grep -oF 'is the declared mode too' | wc -l)"
echo "D $(n $F | grep -oF 'reported and the developer asked which stands' | wc -l)"
echo "E $(n $F | grep -oF 'When the working-process rules are installed' | wc -l)"
```

Expected: `A 1`, `B 0`, `C 0`, `D 0`, `E 1`.

- [ ] **Step 2: Add the key and the conflict question**

Find in `plugins/project-memory/rules/project-memory.md`:

```
`.gitignore`), a declared tracked mode becomes observable with the
first committed file. Private memory (`.claude/memory/`) is always
ignored, so it is never asked. When the working-process rules are installed,
```

Replace with:

```
`.gitignore`), a declared tracked mode becomes observable with the
first committed file. When the working-process rules are installed,
the settings key `dir.docs/memory` — read as that plugin's
process-settings rule says, its effective value with `dir.default`
already applied — is the declared mode too: a visible signal that
agrees with it, or stands where it is unset, governs; a visible signal
that contradicts it is reported and the developer asked which stands,
nothing changed until they answer; the key with no visible signal is
applied unasked; and where the question is asked, its answers include
"tracked, and record" and "ignored, and record", which write
`dir.docs/memory` through the loader's `--set` where a settings block
names the loader. Private memory (`.claude/memory/`) is always
ignored, so it is never asked. When the working-process rules are installed,
```

- [ ] **Step 3: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 2`, `C 1`, `D 1`, `E 2`.

- [ ] **Step 4: Commit**

```bash
git add plugins/project-memory/rules/project-memory.md
git commit -m "feat(project-memory): the core rule reads dir.docs/memory"
```

---

### Task 12: The python and salesforce review commands — `dir.docs/code-review`

**Files:**
- Modify: `plugins/python-standards/commands/python-review.md` — step 2.
- Modify: `plugins/salesforce-standards/commands/salesforce-review.md` —
  step 3.

**Interfaces:**
- Consumes: the key `dir.docs/code-review` from Task 1; the order from
  Task 10, restated because each command stands alone.
- Produces: nothing a later task reads; Task 14 checks both citations.

**Realizes:** D40

- [ ] **Step 1: Record the before values**

```bash
n() { tr -s '[:space:]' ' ' < "$1"; }
for F in plugins/python-standards/commands/python-review.md plugins/salesforce-standards/commands/salesforce-review.md; do
  echo "$F"
  echo "A $(n $F | grep -oF 'exactly `*`, no git-tracked file under it, and no explicit project instruction declaring the mode (signal list owned by the process-artifacts rule) — ask the developer now: ignored or tracked mode.' | wc -l)"
  echo "B $(n $F | grep -oF '`dir.docs/code-review`' | wc -l)"
  echo "C $(n $F | grep -oF 'with no block the key is unset' | wc -l)"
  echo "D $(n $F | grep -oF 'the key with no visible signal is applied unasked' | wc -l)"
done
```

Expected, for each file: `A 1`, `B 0`, `C 0`, `D 0`.

- [ ] **Step 2: Rewrite the predicate in both commands**

The anchor is the same text in both files, at step 2 of the python
command and step 3 of the salesforce command.

Find in `plugins/python-standards/commands/python-review.md` and in
`plugins/salesforce-standards/commands/salesforce-review.md`:

```
   `docs/code-review/` carries no decision — no `.gitignore` of
   exactly `*`, no git-tracked file under it, and no
   explicit project instruction declaring the mode (signal list owned
   by the process-artifacts rule) — ask the developer now: ignored or
   tracked mode.
```

Replace with, in each:

```
   `docs/code-review/` carries no decision — no `.gitignore` of
   exactly `*`, no git-tracked file under it, no settings key
   `dir.docs/code-review` in a settings block in context (its
   effective value, `dir.default` already applied; with no block the
   key is unset), and no explicit project instruction declaring the
   mode (signal list owned by the process-artifacts rule) — ask the
   developer now: ignored or tracked mode, "and record" among the
   answers where the block names the loader, which writes
   `dir.docs/code-review` through the loader's `--set`. A visible
   signal that contradicts the key is reported and the developer asked
   which stands, nothing changed until they answer; the key with no
   visible signal is applied unasked, the ignored mode by writing the
   `*` `.gitignore`.
```

- [ ] **Step 3: Verify**

Run the Step 1 command again, then `claude plugin validate .`.

Expected, for each file: `A 0`, `B 2`, `C 1`, `D 1`; validation
passes.

- [ ] **Step 4: Commit**

```bash
git add plugins/python-standards/commands/python-review.md plugins/salesforce-standards/commands/salesforce-review.md
git commit -m "feat(standards): the review commands read dir.docs/code-review"
```

---

### Task 13: The `process-setup` skill

**Files:**
- Create: `plugins/working-process/skills/process-setup/SKILL.md`

**Interfaces:**
- Consumes: `--print`, `--set --dry-run`, `--set` and `--validate` from
  Tasks 2–5 and their output lines; the registry path from Task 1; the
  rule from Task 6.
- Produces: the skill name `process-setup`, which Task 15's README and
  descriptions and Task 17's dogfood invoke.

**Realizes:** D21, D22, D23, D25, D39, D45, D51, D52

The developer ruled on 2026-09-28 that `skill-creator` is not required
for this skill, and no `evals/` directory is created.

- [ ] **Step 1: Record the before values**

```bash
ls plugins/working-process/skills/process-setup 2>&1 | head -n 1
```

Expected: no such directory.

- [ ] **Step 2: Write the skill**

`plugins/working-process/skills/process-setup/SKILL.md`, exactly:

````
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
````

- [ ] **Step 3: Verify**

```bash
F=plugins/working-process/skills/process-setup/SKILL.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^name: process-setup$' $F)"
echo "B $(head -n 4 $F | grep -c '^description: "')"
echo "C $(grep -c '^## [1-5]\. ' $F)"
echo "D $(n $F | grep -oF '<loader> --set --dry-run <key> <value>' | wc -l)"
echo "E $(n $F | grep -oF 'Never write a settings file directly' | wc -l)"
echo "F $(n $F | grep -oF 'never replays the whole questionnaire' | wc -l)"
echo "G $(n $F | grep -oF 'Create no directory' | wc -l)"
echo "H $(n $F | grep -oF 'binds this worktree only' | wc -l)"
echo "I $(n $F | grep -oF 'exceptions only when the developer asks for them' | wc -l)"
ls plugins/working-process/skills/process-setup/
awk 'NR > 4 && length > 72 && !/^`/ {print "long: " $0}' $F
claude plugin validate plugins/working-process
```

Expected: `A 1`, `B 1`, `C 5`, `D 1`, `E 1`, `F 1`, `G 1`, `H 1`, `I 1`,
the directory holds `SKILL.md` alone, no `long:` line, and validation
passes.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/skills/process-setup/SKILL.md
git commit -m "feat(working-process): process-setup skill"
```

---

### Task 14: The consistency test — citations and references

**Files:**
- Modify: `tests/working-process/test_settings_registry.py` — the
  citation and reference checks.

**Interfaces:**
- Consumes: `read_registry` and `KEY_RE` from Task 1; the citations
  Tasks 7–13 wrote.
- Produces: nothing a later task reads.

**Realizes:** D27

- [ ] **Step 1: Write the failing test**

Add to `tests/working-process/test_settings_registry.py`:

```python
FENCE_RE = re.compile(r"^```")
TOKEN_RE = re.compile(r"`([^`\n]+)`")
SCAN_PLUGINS = ("working-process", "project-memory", "python-standards", "salesforce-standards")
SCAN_DIRS = ("rules", "skills", "agents", "commands")


def unfenced_text(path: Path) -> str:
    """The file's text with every fenced block removed, fences included."""
    kept, fence = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE_RE.match(line):
            fence = not fence
            continue
        if not fence:
            kept.append(line)
    return "\n".join(kept)


class RegistryConsistencyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.entries = read_registry(REGISTRY)
        self.prefixes = tuple(sorted({key.split(".", 1)[0] + "." for key in self.entries}))

    def test_every_reader_cites_its_key_literally(self) -> None:
        for key, fields in self.entries.items():
            for reader in fields["read-by"].split(", "):
                with self.subTest(key=key, reader=reader):
                    self.assertIn(f"`{key}`", unfenced_text(PLUGINS / reader))

    def test_every_reference_is_registered(self) -> None:
        unregistered = []
        for plugin in SCAN_PLUGINS:
            for sub in SCAN_DIRS:
                for path in sorted((PLUGINS / plugin / sub).rglob("*.md")):
                    for token in TOKEN_RE.findall(unfenced_text(path)):
                        if "<" in token or not KEY_RE.match(token):
                            continue
                        if not token.startswith(self.prefixes):
                            continue
                        if token not in self.entries:
                            unregistered.append(f"{path.relative_to(PLUGINS)}: `{token}`")
        self.assertEqual(unregistered, [])
```

A reference is a backticked span whose whole text has a key's shape and
starts with a registered prefix (`dir.`, `design.`, `dispatch.`,
`docs-branch.`, `consult.`, `review.`); a span holding `<` is a
placeholder such as `dir.<path>` and is skipped; fenced blocks are
skipped whole. A file path such as `review-reports.md` has the shape
but not a prefix, so it is not a reference.

Then prove the check can fail, by putting one reader back to its state
before Task 10 — from history, since Task 10 committed its edit:

```bash
F=plugins/working-process/rules/process-artifacts.md
git show develop:$F > $F
python3 -m unittest discover -s tests/working-process -p 'test_settings_registry.py' 2>&1 | tail -n 1
git checkout -- $F
git status --porcelain -- $F
```

Expected: `FAILED (failures=7)` — the `develop` copy cites none of the
seven `dir.` keys whose `read-by:` names it, and `unittest` counts one
failure per failed `subTest`; then `git status` prints nothing, the
file restored to Task 10's committed text.

- [ ] **Step 2: Run the test to see it pass**

Run: `python3 -m unittest discover -s tests/working-process -v`
Expected: every test passes, the two new ones included — every
`read-by` file cites its key, and no unregistered reference exists
under the four plugins.

- [ ] **Step 3: Commit**

```bash
git add tests/working-process/test_settings_registry.py
git commit -m "test(working-process): registry citations and references"
```

---

### Task 15: README, CHANGELOG, descriptions and the dogfood version

**Files:**
- Modify: `plugins/working-process/README.md` — the components list,
  the propagation-auditor bullet, `## Model selection`, `## Process
  rules`, a new `## Process settings` section, `## Process directories`.
- Modify: `plugins/working-process/CHANGELOG.md` — bullets under
  `## Unreleased`.
- Modify: `plugins/working-process/.claude-plugin/plugin.json` — the
  version and the description.
- Modify: `.claude-plugin/marketplace.json` and the root `README.md` —
  the description (Deviation 3).
- Modify: `plugins/project-memory/CHANGELOG.md`,
  `plugins/python-standards/CHANGELOG.md`,
  `plugins/salesforce-standards/CHANGELOG.md` — an `## Unreleased`
  heading each (Deviation 2).

**Interfaces:**
- Consumes: every name the earlier tasks produced.
- Produces: the version `0.18.0-dev.3.process-setup`, which Task 17's
  dogfood loads.

**Realizes:** none

- [ ] **Step 1: Record the before values**

```bash
R=plugins/working-process/README.md
C=plugins/working-process/CHANGELOG.md
J=plugins/working-process/.claude-plugin/plugin.json
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $R | grep -oF '**`process-setup` skill**' | wc -l)"
echo "B $(n $R | grep -oF 'background on the cheapest available family, because every duty is procedural' | wc -l)"
echo "C $(n $R | grep -oF '`propagation-auditor` dispatches on the cheapest available family, since' | wc -l)"
echo "D $(n $R | grep -oF 'The plugin ships seven rule files' | wc -l)"
echo "E $(n $R | grep -oF 'The plugin ships eight rule files' | wc -l)"
echo "F $(grep -c '^## Process settings$' $R)"
echo "G $(n $R | grep -oF 'unless `dir.default` or the directory' | wc -l)"
echo "H $(n $C | grep -oF 'process-setup' | wc -l)"
echo "I $(grep -c '"version": "0.18.0-dev.2.plan-coverage"' $J)"
echo "J $(grep -rlF 'process-status and sync-rules skills' $J .claude-plugin/marketplace.json README.md | wc -l)"
echo "K $(grep -rlF 'process-status, process-setup and sync-rules skills' $J .claude-plugin/marketplace.json README.md | wc -l)"
for f in plugins/project-memory/CHANGELOG.md plugins/python-standards/CHANGELOG.md plugins/salesforce-standards/CHANGELOG.md; do echo "L $f $(grep -c '^## Unreleased$' $f)"; done
```

Expected: `A 0`, `B 1`, `C 1`, `D 1`, `E 0`, `F 0`, `G 0`, `H 0`,
`I 1`, `J 3`, `K 0`, and `L … 0` for each of the three changelogs.

- [ ] **Step 2: The components list gains the skill**

Find in `plugins/working-process/README.md`:

```
- **`sync-rules` skill** — installs, updates, and uninstalls the rule
```

Replace with:

```
- **`process-setup` skill** — collects a project's standing process
  answers in one sitting: shows the effective settings, asks about the
  unset keys, migrates `CLAUDE.md` notes and directory signals as
  candidates, and records every answer through the settings loader.
  Triggers: "process setup" / "set up the process settings".
- **`sync-rules` skill** — installs, updates, and uninstalls the rule
```

- [ ] **Step 3: The propagation-auditor bullet and the model-selection paragraph name the tier key**

Find in `plugins/working-process/README.md`:

```
  nothing, ends in no verdict, and stamps nothing. Dispatched in the
  background on the cheapest available family, because every duty is
  procedural; the workflow gates every verdict-agent dispatch and every
```

Replace with:

```
  nothing, ends in no verdict, and stamps nothing. Dispatched in the
  background on the tier the project's
  `dispatch.propagation-auditor-tier` resolves to — the cheapest
  available family unless the project sets another — because every
  duty is procedural; the workflow gates every verdict-agent dispatch
  and every
```

Find in `plugins/working-process/README.md`:

```
An audit is not a review, and that floor governs reviews alone: the
`propagation-auditor` dispatches on the cheapest available family,
since every duty it walks is procedural, and the `integrity-auditor` on
the most capable available tier — each named like any other dispatch.
```

Replace with:

```
An audit is not a review, and that floor governs reviews alone: the
`propagation-auditor` dispatches on the tier the project's
`dispatch.propagation-auditor-tier` resolves to — `cheapest`, `mid` or
`most-capable`, the first unless the project sets another, since every
duty it walks is procedural; the workflow rule carries the table — and
the `integrity-auditor` on the most capable available tier, each named
like any other dispatch.
```

- [ ] **Step 4: The rules count and the new section**

Find in `plugins/working-process/README.md`:

```
The plugin ships seven rule files in `rules/` — the preferred workflow
(always loaded once installed), frontmatter and lifecycle for judged
documents and plans, what a technical design must contain
```

Replace with:

```
The plugin ships eight rule files in `rules/` — the preferred workflow
(always loaded once installed), the process settings
(`process-settings.md`, always loaded: the settings files, their
grammar, the block and how a key is read), frontmatter and lifecycle
for judged documents and plans, what a technical design must contain
```

Find in `plugins/working-process/README.md`:

```
## Process directories
```

Replace with:

```
## Process settings

Standing answers — a directory's mode, the review loop's autonomy and
per-round commits, persona consultation, the technical-design offer,
the `.docs` branch merge, the propagation gate's tier — live in
`.working-process/settings.md` (the team's, committed) and
`.working-process/settings.local.md` (one person's, ignored by the
directory's own `.gitignore`), as `key: value` lines. The key registry
`SETTINGS_REGISTRY.md` at the plugin root defines every key. A second
SessionStart hook runs `scripts/load-settings.sh`, which emits every
key's effective value and source as one block the rules read; the same
script offers `--print`, `--validate --scope team|personal <file>`,
`--set <key> <value>` and `--set --dry-run <key> <value>`, and owns
every write. Set the answers in one sitting with the `process-setup`
skill, or record one as you answer its question — "yes, and record".
The block is plain standard output, capped at 4 KB in the hook and
uncapped under `--print`; in a worktree the main checkout's personal
file is read and written.

## Process directories
```

Find in `plugins/working-process/README.md`:

```
code-review run, shape defined by the review-reports rule). On first
creation the developer is asked whether the directory should be
git-ignored (a `.gitignore` containing exactly `*`) or committed; an
existing directory's state is respected without asking. A tracked-mode
```

Replace with:

```
code-review run, shape defined by the review-reports rule). On first
creation the developer is asked whether the directory should be
git-ignored (a `.gitignore` containing exactly `*`) or committed —
unless `dir.default` or the directory's own exception key settles it,
in which case nothing is asked; an existing directory's state is
respected without asking, and one contradicting the key is reported.
A tracked-mode
```

- [ ] **Step 5: The CHANGELOG entries**

Find in `plugins/working-process/CHANGELOG.md`:

```
  the decision register, the plan annotations and the held gate line,
  which the updated agents expect.
```

Replace with:

```
  the decision register, the plan annotations and the held gate line,
  which the updated agents expect.
- Standing process answers get one home: `.working-process/settings.md`
  (the team's, committed) and `.working-process/settings.local.md`
  (personal, ignored by the directory's own `.gitignore`), one
  `key: value` grammar, and a key registry (`SETTINGS_REGISTRY.md`)
  defining every key's scope, values, default, readers and question.
- A second SessionStart handler, `scripts/load-settings.sh`, emits every
  key's effective value and source as one plain-text block, capped at
  4 KB; the same loader offers `--print`, `--validate` and `--set`
  (with `--dry-run`) and owns every write — in a worktree, to the main
  checkout's personal file.
- New always-on rule `process-settings.md`: the files, the grammar, the
  block, how a key is read and when a write happens. Run a rules
  re-sync after this update to install it.
- New `process-setup` skill: shows the effective settings, asks about
  the unset keys, offers `CLAUDE.md` notes and directory signals as
  candidates, and records every answer through the loader.
- The rules read named keys instead of "the developer's own
  instructions": `consult.personas`, `review.autonomy`,
  `review.per-round-commit`, `design.technical-design-offer`,
  `docs-branch.merge`, `dispatch.propagation-auditor-tier`, and
  `dir.default` with its per-directory exceptions; a standing question
  asked in ordinary work offers "<answer>, and record".
- The propagation gate's tier is a setting: the auditor's card accepts
  the tier the dispatcher resolved, `cheapest` by default, and the
  workflow rule carries the Claude Code tier table.
- The local pocket of `docs/code-review/` fires on the resolved tracked
  mode, however it was settled.
```

Find in `plugins/project-memory/CHANGELOG.md`:

```
## 0.5.1 — 2026-09-15
```

Replace with:

```
## Unreleased

- When the working-process rules are installed, the core rule reads the
  settings key `dir.docs/memory` as Team memory's declared mode, gains
  the conflict question for a visible signal that contradicts it, and
  offers "and record" with its first-create question.

## 0.5.1 — 2026-09-15
```

Find in `plugins/python-standards/CHANGELOG.md`:

```
## 0.3.2 — 2026-09-15
```

Replace with:

```
## Unreleased

- `/python-review` reads the settings key `dir.docs/code-review` from a
  settings block in context before asking the first-create question,
  and asks which stands when a visible signal contradicts it.

## 0.3.2 — 2026-09-15
```

Find in `plugins/salesforce-standards/CHANGELOG.md`:

```
## 0.4.0 — 2026-09-15
```

Replace with:

```
## Unreleased

- `/salesforce-review` reads the settings key `dir.docs/code-review`
  from a settings block in context before asking the first-create
  question, and asks which stands when a visible signal contradicts it.

## 0.4.0 — 2026-09-15
```

- [ ] **Step 6: The version and the description, in three places**

In `plugins/working-process/.claude-plugin/plugin.json`, change the
`version` value from `0.18.0-dev.2.plan-coverage` to
`0.18.0-dev.3.process-setup` — `develop` carries `-dev.2`, so the next
number is 3, and the discriminator is the branch's short name, since
the topic has no issue.

In the same file, in `.claude-plugin/marketplace.json` and in the
root `README.md`, find the text
`process-status and sync-rules skills` and replace it with
`process-status, process-setup and sync-rules skills` — once in each
file, the same edit.

- [ ] **Step 7: Verify**

Run the Step 1 command again, then both validations.

Expected: `A 1`, `B 0`, `C 0`, `D 0`, `E 1`, `F 1`, `G 1`, `H 1`,
`I 0`, `J 0`, `K 3`, `L … 1` for each of the three changelogs, and:

```bash
grep -c '"version": "0.18.0-dev.3.process-setup"' plugins/working-process/.claude-plugin/plugin.json
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: `1`, both pass.

- [ ] **Step 8: Commit**

```bash
git add plugins/working-process/README.md plugins/working-process/CHANGELOG.md plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md plugins/project-memory/CHANGELOG.md plugins/python-standards/CHANGELOG.md plugins/salesforce-standards/CHANGELOG.md
git commit -m "docs(working-process): README, changelogs and dogfood version for process-setup"
```

---

### Task 16: Final verification

**Files:**
- Test: the whole branch, the glossary, and this plan.

**Interfaces:**
- Consumes: every task above.
- Produces: nothing.

**Realizes:** D31, D48

- [ ] **Step 1: Validate and run every test**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
python3 -m unittest discover -s tests/working-process 2>&1 | tail -n 3
/bin/sh plugins/working-process/scripts/load-settings.sh; echo "hook rc=$?"
if shellcheck --version >/dev/null 2>&1; then shellcheck -s sh plugins/working-process/scripts/load-settings.sh && echo shellcheck-ok; else echo "shellcheck absent: install it (mise use -g shellcheck)"; fi
if command -v uv >/dev/null; then uv run --python 3.9 --no-project python -m unittest discover -s tests/working-process 2>&1 | tail -n 1; else echo "uv absent: the 3.9 floor is not measured here"; fi
```

Expected: both validations pass; the tests end `OK`; the hook prints
nothing but `hook rc=0` (this repository has no `.working-process/`);
`shellcheck-ok` where shellcheck runs, or the `shellcheck absent` note
(a mise shim with no version set counts as absent); and
`OK` once more from the run under Python 3.9 — the floor *Tech Stack*
claims, measured once — or the `uv absent` note, which the report
repeats so the floor is known to be unmeasured.

- [ ] **Step 2: Check what must not change**

```bash
git diff --stat develop -- plugins/working-process/skills/grilling-session/SKILL.md plugins/working-process/scripts/check-rules-drift.sh plugins/working-process/scripts/ruleset-hash.sh plugins/working-process/skills/sync-rules/SKILL.md | tail -n 1
```

Expected: no output — the grilling-session skill stays as it is
(D48), and the drift check,
the hasher and the sync-rules skill are untouched.

- [ ] **Step 3: Check the glossary entry D31 names**

```bash
G=docs/domain/glossary.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^\*\*First-create question\*\*:$' $G)"
echo "B $(n $G | grep -oF 'nor a `dir.*` **Settings key**' | wc -l)"
echo "C $(n $G | grep -oF 'an observable signal that contradicts a settings key is reported and the developer asked which stands' | wc -l)"
echo "D $(grep -c '^\*\*Key registry\*\*:$' $G)"
```

Expected: `A 1`, `B 1`, `C 1`, `D 1` — the entry gained the settings
key at the grilling, as D31 records; nothing here writes it.

- [ ] **Step 4: Check line width of the changed prose**

```bash
for f in $(git diff --name-only develop -- 'plugins/*/rules/*.md' 'plugins/*/agents/*.md' 'plugins/*/skills/*/SKILL.md' 'plugins/*/commands/*.md' 'plugins/*/README.md' 'plugins/*/CHANGELOG.md' plugins/working-process/SETTINGS_REGISTRY.md); do
  git diff -U0 develop -- "$f" | grep '^+[^+]' | cut -c2- \
    | LC_ALL=C.UTF-8 awk -v f="$f" 'length > 72 && !/^ {4}/ && !/^\|/ && !/^description:/ && !/^question:/ && !/^read-by:/ && !/^working-process settings/ {print f": "$0}'
done
```

Expected: no output. Table rows, one-line `description:` values, the
registry's `question:` and `read-by:` fields and the block example's
first line are exempt.

- [ ] **Step 5: Derive this plan's decision coverage**

```bash
python3 plugins/working-process/scripts/decision-coverage.py docs/plans/2026-09-28-process-setup.md | grep -v '^  '
```

Expected: one line,
`decision-coverage: ../specs/2026-09-28-process-setup-design.md 65/65 covered; inherited []; deferred []; uncovered []`,
and no hit line. Sixty-five is the register's leaf count — D1–D52 less
the group D7, plus D7.1–D7.14; a register edit since changes it, and
the two counts stay equal.

- [ ] **Step 6: Report**

No commit. Report the results to the developer, and leave `sync-rules`
and both documents' `status` to them. Tasks 17 and 18 follow.

---

### Task 17: Claude Code dogfood — the skill records, a new session reads, compaction returns the block

**Files:**
- Test: a scratch project outside the repository, and the evidence file
  `.claude/working-process/2026-09-28-process-setup/task-17-dogfood.md`.

**Interfaces:**
- Consumes: every task above; the version from Task 15.
- Produces: nothing.

**Realizes:** D29

The unit tests prove the loader; only a session proves that plain
standard output from a plugin hook reaches the context, that a rule
reads the block instead of asking, and that compaction brings it back.
Three sessions run in one scratch project, the plugin loaded from the
checkout with `--plugin-dir` and the changed rules copied project-scope
into the scratch project. The user-scope install still carries the old
rules at `~/.claude/rules/working-process/`, and Claude Code loads
user- and project-level rules both — neither set overrides the other —
so the old set is moved aside for the run, with the developer's
consent, and restored after.

- [ ] **Step 1: Build the scratch project — ask the developer first**

A `--plugin-dir` session collides with an installed plugin of the same
name that is active in the scratch directory, so each such install —
the user-scope one, and a project-scope one only where it belongs to
the scratch directory; one scoped to another project is left alone —
is disabled for the run and restored after; and
the user-scope rules are moved aside so that only the new rules are in
context. Both change the developer's own configuration, so ask two
questions before running: may the installed plugin be disabled for the
run, and may `~/.claude/rules/working-process/` be moved aside for the
run. Without the first the dogfood cannot run. Without the second it
runs with both rule sets in context, and Step 6 says so in the
evidence file: Step 5 is then weaker evidence, since a reply may have
followed the old workflow rule's "a durable preference belongs in the
developer's own instructions" rather than the new text.

```bash
R=$(git rev-parse --show-toplevel)
W=${TMPDIR:-/tmp}/process-setup-dogfood
command rm -rf "$W"
mkdir -p "$W/docs/specs" "$W/docs/plans" "$W/.claude/rules/working-process"
command cp -f "$R"/plugins/working-process/rules/*.md "$W/.claude/rules/working-process/"
printf '%s\n' '# Fixture' '' 'This repository does not get the technical-design offer.' > "$W/CLAUDE.md"
printf '[project]\nname = "fixture"\n' > "$W/pyproject.toml"
printf '*\n' > "$W/docs/plans/.gitignore"
(cd "$W" && git init -q && git add -A && git -c user.name=fixture -c user.email=fixture@example.invalid commit -qm fixture)
command -v jq >/dev/null || { echo "jq absent: install it (mise use jq) before this task"; exit 1; }
ls "$W/.claude/rules/working-process" | wc -l
claude plugin list --json | jq -r --arg w "$W" '.[] | select(.id=="working-process@missing-bits" and .enabled and (.scope=="user" or .projectPath==$w)) | .scope' > "$W/was"; echo "was=$(tr '\n' ' ' < "$W/was")"
ls "$HOME/.claude/rules/working-process" | wc -l > "$W/rules-count"; echo "rules-count=$(cat "$W/rules-count")"
echo both > "$W/rules-state"
```

Expected: `8` rule files copied; `was=` followed by the scopes in which
the plugin is enabled — `user`, `project`, both or none, one per line
in `$W/was`; `rules-count=` the number of rule files in the user-scope
copy (7 where the payload before this change is installed). Steps 2
and 6 run in shells of their own and read the three files.
The fixture carries one prose note (a technical-design declaration to
migrate), one ignored-mode directory (`docs/plans/`) and one undecided
directory (`docs/specs/`, which exists and holds nothing) — the
first-run candidates of the skill.

- [ ] **Step 2: Silence before adoption**

First the installed plugin, in every scope Step 1 recorded:

```bash
R=$(git rev-parse --show-toplevel); W=${TMPDIR:-/tmp}/process-setup-dogfood
for s in $(cat "$W/was"); do claude plugin disable working-process@missing-bits --scope "$s"; done
claude plugin list --json | jq -r --arg w "$W" '[.[] | select(.id=="working-process@missing-bits" and .enabled and (.scope=="user" or .projectPath==$w))] | length'
```

Expected: `0` — no enabled install active in the scratch directory
remains. An install scoped to another project is neither listed nor
touched, so nothing is written to this repository's tracked
`.claude/settings.json`; `git -C "$R" status --porcelain .claude/settings.json`
prints nothing.

Then, only where the developer consented in Step 1, the user-scope
rules:

```bash
W=${TMPDIR:-/tmp}/process-setup-dogfood
command mv -f "$HOME/.claude/rules/working-process" "$W/user-rules-aside" && [ ! -e "$HOME/.claude/rules/working-process" ] && echo aside > "$W/rules-state"; cat "$W/rules-state"
```

Expected: `aside`; without consent the block is skipped and
`$W/rules-state` keeps `both`.

Then the session:

```bash
R=$(git rev-parse --show-toplevel); W=${TMPDIR:-/tmp}/process-setup-dogfood
(cd "$W" && claude -p --plugin-dir "$R/plugins/working-process" \
  "Quote verbatim every line in your context that begins with 'working-process settings'. If there is none, print exactly NONE.") | tee "$W/run-1.txt"
```

Expected: `NONE` — the hook is silent where `.working-process/` does
not exist.

- [ ] **Step 3: The skill records — an interactive session**

Run, in a terminal, `cd "$W" && claude --plugin-dir "$R/plugins/working-process"`,
then invoke the skill by asking for "process setup". Expected of the
skill, step by step: it runs `--print` and shows the `no settings
directory` line; it offers `docs/plans/` ignored as the only decided
directory and `dir.default: ignored` from it, and the `CLAUDE.md`
sentence as `design.technical-design-offer: off`, both to confirm;
confirm both. Then answer the unset keys (the tier key is not asked:
its default `cheapest` stands): `docs-branch.merge` squash, `consult.personas` no,
`review.autonomy` yes, `review.per-round-commit` no; decline
exceptions. For each answer it shows a `--set --dry-run` preview, then
writes; it offers to remove the `CLAUDE.md` note — accept; in its
step 4 it writes `docs/specs/.gitignore` holding `*` — with
`dir.default: ignored` confirmed, `docs/specs/` inherits ignored and
carries no visible signal (D17 step 3, D22) — and writes none into
`docs/plans/`, which already has one; it reminds you to commit
`settings.md` and `.working-process/.gitignore`. Then `/exit`.

```bash
W=${TMPDIR:-/tmp}/process-setup-dogfood
cat "$W/.working-process/settings.md"; echo ---; cat "$W/.working-process/settings.local.md"; echo ---; cat "$W/.working-process/.gitignore"; echo ---; cat "$W/CLAUDE.md"; echo ---; cat "$W/docs/specs/.gitignore"
```

Expected: the team file holds `dir.default: ignored`,
`design.technical-design-offer: off`, `docs-branch.merge: squash`,
each under its question; the personal file `consult.personas: no`,
`review.autonomy: yes`, `review.per-round-commit: no`; the
`.gitignore` the single line `settings.local.md`; `CLAUDE.md` without
the technical-design sentence; `docs/specs/.gitignore` the single line
`*`. A skill that wrote a settings file with anything but `--set`,
asked about a key already answered, or left `docs/specs/` without its
`.gitignore`, fails the test.

- [ ] **Step 4: A new session receives the block**

```bash
R=$(git rev-parse --show-toplevel); W=${TMPDIR:-/tmp}/process-setup-dogfood
(cd "$W" && claude -p --plugin-dir "$R/plugins/working-process" \
  "Quote verbatim every line in your context that begins with 'working-process settings', 'dir.default', 'design.technical-design-offer' or 'review.autonomy'. If there is none, print exactly NONE.") | tee "$W/run-2.txt"
```

Expected: the first line naming `$W` as the root and the loader under
the checkout, then `dir.default: ignored  [team]`,
`design.technical-design-offer: off  [team]`,
`review.autonomy: yes  [local]`. `NONE`, or a block from another root,
fails the test: plain standard output did not reach the session.

- [ ] **Step 5: A recorded question is not asked, and compaction returns the block**

Run `cd "$W" && claude --plugin-dir "$R/plugins/working-process"` again
and put these three prompts, recording each reply verbatim:

1. "We are at a design spec's consumption gate in this repository.
   Would you offer to write the technical design? Answer in one line
   and name what decides it." Expected: no offer, citing
   `design.technical-design-offer: off`.
2. "You are about to dispatch the first verdict agent of this session.
   Would you ask me whether the review loop may run autonomously and
   whether it may commit per round? Answer in one line per clause and
   name what decides each." Expected: neither clause is asked —
   `review.autonomy: yes` and `review.per-round-commit: no` from the
   block.
3. `/compact`, then "Quote verbatim every line in your context that
   begins with 'working-process settings' or 'review.autonomy'."
   Expected: the first line and `review.autonomy: yes  [local]` — the
   hook ran again on compaction.

A reply that asks either question, offers the design, or finds no
block after `/compact` fails the test; report it with the reply text
and do not adjust the expectation.

- [ ] **Step 6: Restore, keep the evidence, clean up**

```bash
R=$(git rev-parse --show-toplevel); W=${TMPDIR:-/tmp}/process-setup-dogfood
for s in $(cat "$W/was"); do claude plugin enable working-process@missing-bits --scope "$s"; done
echo "enabled=$(claude plugin list --json | jq -r --arg w "$W" '[.[] | select(.id=="working-process@missing-bits" and .enabled and (.scope=="user" or .projectPath==$w))] | length') expected $(grep -c . "$W/was")"
[ -d "$W/user-rules-aside" ] && command mv -f "$W/user-rules-aside" "$HOME/.claude/rules/working-process"
echo "rules-count=$(ls "$HOME/.claude/rules/working-process" | wc -l) expected $(cat "$W/rules-count")"; [ -e "$W/user-rules-aside" ] && echo "aside still present"
D="$R/.claude/working-process/2026-09-28-process-setup"; mkdir -p "$D"
{ echo '# Task 17 — Claude Code dogfood, 2026-09-28'; echo; echo '## rules'; case $(cat "$W/rules-state") in aside) echo 'user-scope rules moved aside for the run; only the new rules were in context';; *) echo 'both rule sets in context: the user-scope copy was not moved aside, so Step 5 is weaker evidence';; esac; echo; echo '## run-1'; cat "$W/run-1.txt"; echo; echo '## run-2'; cat "$W/run-2.txt"; echo; echo '## files'; cat "$W/.working-process/settings.md" "$W/.working-process/settings.local.md"; echo '--- docs/specs/.gitignore'; cat "$W/docs/specs/.gitignore"; echo; echo '## step 5 replies'; } > "$D/task-17-dogfood.md"
```

Then paste the three Step 5 replies under `## step 5 replies`, and
remove the scratch project with `command rm -rf "$W"` — after the
rules are back in place, since the moved-aside copy lives under `$W`.

Expected: `enabled=` equal to its `expected` — every scope Step 1
recorded is enabled again; `rules-count=` equal to its `expected` and
no `aside still present` line — the user-scope rules are back on disk;
the evidence file lives in the dispatch-record store, whose `*`
`.gitignore` keeps it local, and its `## rules` section says which
case held. Where it says both rule sets were in context, the report to
the developer repeats that Step 5 is weaker evidence. No commit.

---

### Task 18: Codex check — the same loader through a repository-level hook

**Files:**
- Test: a scratch project outside the repository, and the evidence file
  `.claude/working-process/2026-09-28-process-setup/task-18-codex.md`.

**Interfaces:**
- Consumes: the loader from Tasks 2–5.
- Produces: nothing.

**Realizes:** D30

No Codex plugin packaging is involved: a repository-level
`.codex/hooks.json` names the loader by its absolute path in the
checkout, in the same JSON shape the plugin's `hooks.json` uses
(recorded on 2026-09-28 from the Codex hooks documentation in
`.claude/working-process/2026-09-28-process-setup/codex-2026-09-28-13-37-08.md`).
A hook needs trust before it runs, which the `/hooks` panel grants in
an interactive session, so the first session is interactive; the
resume runs non-interactively through `codex exec resume`, where the
session id comes from the `--json` event stream of the first `exec`
call, never from the newest file under `~/.codex/sessions/`.

- [ ] **Step 1: Build the scratch project**

```bash
R=$(git rev-parse --show-toplevel)
W=${TMPDIR:-/tmp}/process-setup-codex
command rm -rf "$W"; mkdir -p "$W/.codex" "$W/.working-process"
printf '%s\n' 'dir.default: tracked' 'consult.personas: yes' > "$W/.working-process/settings.md"
cat > "$W/.codex/hooks.json" <<EOF
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "$R/plugins/working-process/scripts/load-settings.sh" }
        ]
      }
    ]
  }
}
EOF
(cd "$W" && git init -q && git add -A && git -c user.name=fixture -c user.email=fixture@example.invalid commit -qm fixture)
python3 -c "import json; print(json.load(open('$W/.codex/hooks.json'))['hooks']['SessionStart'][0]['hooks'][0]['command'])"
```

Expected: the loader's absolute path under the checkout. (`$R` is a
machine path inside a scratch file that is never committed; the
hygiene rule binds committed text.)

- [ ] **Step 2: Trust the hook and read the block — an interactive session**

Run `cd "$W" && codex -s read-only`, open `/hooks`, and trust the
SessionStart hook the panel lists for this repository. Then put:
"Quote verbatim every line in your context that begins with
'working-process settings', 'dir.default' or 'consult.personas'. If
there is none, print exactly NONE." Record the reply. Where the block
was not there on the first prompt — the hook ran before it was
trusted — start a new `codex -s read-only` session in `$W` and put the
same prompt.

Expected: the first line naming `$W` as the root, `dir.default: tracked  [team]`
and `consult.personas: unset  [team suggests: yes]`. `NONE` after a
trusted hook fails the test. Then `/compact` and put the prompt again.
Expected: the same lines — the hook ran on compaction. Then `/exit`.

- [ ] **Step 3: The block after a resume — non-interactive**

```bash
W=${TMPDIR:-/tmp}/process-setup-codex
(cd "$W" && printf '%s' "Quote verbatim every line in your context that begins with 'working-process settings' or 'dir.default'. If there is none, print exactly NONE." \
  | codex exec -s read-only -C "$W" --json - > "$W/exec-1.jsonl")
ID=$(grep -o '"thread_id":"[^"]*"' "$W/exec-1.jsonl" | head -n 1 | cut -d'"' -f4); echo "id=$ID"
(cd "$W" && printf '%s' "Again: quote verbatim every line in your context that begins with 'working-process settings' or 'dir.default'." \
  | codex exec resume "$ID" -c sandbox_mode="read-only" - -o "$W/exec-2.txt")
cat "$W/exec-2.txt"
```

Expected: `id=` followed by a session id, and `exec-2.txt` holding the
first line and `dir.default: tracked  [team]` — the resumed session
received the block again. Where the id key in the stream is not
`thread_id`, read the first event of `exec-1.jsonl` and take the
session id it carries; where `exec-1.jsonl` shows the hook untrusted
in non-interactive mode, the interactive `/compact` result of Step 2
stands as the compaction proof and this step records the resume as not
provable non-interactively.

- [ ] **Step 4: Keep the evidence, clean up**

```bash
R=$(git rev-parse --show-toplevel); W=${TMPDIR:-/tmp}/process-setup-codex
D="$R/.claude/working-process/2026-09-28-process-setup"; mkdir -p "$D"
{ echo '# Task 18 — Codex check, 2026-09-28'; echo; echo '## hooks.json'; cat "$W/.codex/hooks.json"; echo; echo '## step 2 replies'; echo; echo '## step 3'; cat "$W/exec-2.txt"; } > "$D/task-18-codex.md"
command cp -f "$W/exec-1.jsonl" "$D/task-18-exec-1.jsonl"
```

Then paste the Step 2 replies under `## step 2 replies` and remove the
scratch project with `command rm -rf "$W"`. No commit. Report the
results of Tasks 17 and 18 to the developer.

## Review rounds

### Loop closed — 2026-09-29

Resolved without a fresh round on the developer's choice: the latest
round, 3, read the whole document and returned `concerns` with one
Important and five Minor findings, all fixed under cited licenses (F16–
F21 below), and the adversary judged a further round not worth its
cost. The developer approved the plan and chose a fast-forward of the
document branch.

### 2026-09-29 — plan-adversary, fable 5.1, concerns (round 3, full-document)

- fixed 2026-09-29 — [Important] F16: the dogfood fixture has no toolchain manifest, so no technical-design offer fires with the key set or unset; license: spec D29 ("a recorded question is not asked") and the workflow rule's manifest-raised offer; Task 17 Step 1 writes a `pyproject.toml`
- fixed 2026-09-29 — [Minor] F17: Task 17 Step 3 expected the tier key to be asked though its default is `cheapest`; license: Task 13 ("Ask about the unset keys only"); dropped from the answer list, with the reason
- fixed 2026-09-29 — [Minor] F18: hook mode's empty stderr was untested where `git rev-parse` fails; license: spec D10; cases 9 and 10 assert `err == ""`
- fixed 2026-09-29 — [Minor] F19: `local` would fail Task 16's `shellcheck -s sh`; license: the POSIX Global Constraint; the constraint bans `local`
- fixed 2026-09-29 — [Minor] F20: `command -v shellcheck` is true for a mise shim with no version; license: Task 16's own expectation; presence tested with `shellcheck --version`, with the mise install as the remedy
- fixed 2026-09-29 — [Minor] F21: no-git fixtures depended on `TMPDIR` lying outside every repository; license: spec D28 (fixtures); `run_loader` and `git()` set `GIT_CEILING_DIRECTORIES` to the fixture base
- signal 2026-09-29 — a further round does not earn its cost; the fixes are one-liners licensed by the plan or the spec, and the Minors are better left to implementation and code review; the plan is ready to build once they land

### 2026-09-29 — plan-adversary, fable 5.1, blocking (round 2, diff-scoped)

- fixed 2026-09-29 — [Important] F11: `block=$(set -e; …) || block=''` fails where `/bin/sh` is bash; license: spec D10; Task 2 prescribes `block=$(set -e; build_block 2>/dev/null); rc=$?`, bans the `||` and `if` forms, and has `build_block` return non-zero from each tool call
- fixed 2026-09-29 — [Important] F12: Task 17 disabled every enabled install, a project-scope install of another project included; license: Task 17's own aim (the collision with `--plugin-dir` in the scratch directory); Steps 1, 2 and 6 read `claude plugin list --json` filtered to installs active in the scratch directory, and Step 2 checks the tracked settings stay clean
- fixed 2026-09-29 — [Minor] F13: the function list gave `die` a silent exit in hook mode; license: Task 2's own wrapper contract; `die` always exits 1
- fixed 2026-09-29 — [Minor] F14: *unchanged* was byte-exact while the grammar tolerates a trailing CR; license: spec D37; *unchanged* compares the record's value, and case 26 gains a CRLF record
- fixed 2026-09-29 — [Minor] F15: F4's license cited a private note and platform documentation, and the committed ledger pointed at a per-user store; ruling: 2026-09-29; the developer approved the dogfood procedure — disable only the install active in the scratch directory, move the user-scope rules aside only with consent at run time — and F4's line now carries that ruling
- hit fixed 2026-09-29 — Task 17 Step 1's intro still disabled "every enabled install"; now only the installs active in the scratch directory
- hit fixed 2026-09-29 — Task 17's `jq` calls had no Tech Stack entry and no availability guard; Tech Stack names it, Step 1 stops with an install hint where it is absent
- hit dismissed 2026-09-29 — round 1's F7 line quotes the mechanism F11 later replaced; counter: a ledger line records what its wave changed at the time, and F11's line records the replacement, so the history is complete and editing F7's line would rewrite it
- signal 2026-09-29 — another round earns its cost only over the two Important fixes, and a confirming full-document round is owed anyway; the Minors alone do not justify one

### 2026-09-29 — plan-adversary, fable 5.1, blocking (round 1, full-document)

- hit fixed 2026-09-29 — Task 8's check H expected 2 literal "resolved from `…tier`" matches, but the card edit inserts "the project's"; the grep now admits it
- hit fixed 2026-09-29 — Task 15's check H expected 2 "process-setup" in the CHANGELOG, the edit yields 1; expected 1
- hit fixed 2026-09-29 — Task 16 Step 2 expected no diff against develop for the glossary, which the spec's grilling already changed on this branch; the glossary left out of that check (Step 3 checks its content)
- fixed 2026-09-29 — [Important] F1: a worktree without `.working-process/` is silent though the main checkout has settings, narrowing D5 without a Deviation; license: spec D5 and D41 (the loader reads the main checkout's personal file wherever the worktree has none of its own, and a personal answer is written where the loader reads it), with D50 and *Scope and precedence* keeping the team file the current checkout's; Task 3's contract gains the worktree silence test over `$DIR` or `$MAIN/.working-process` and states that the main checkout's team file is never read, case 18 expects the block with `team: settings.md (absent)` and the main checkout's personal answer and keeps the silent case for two checkouts without the directory, case 30 expects the fresh block to carry the answer just written, Task 3 Step 2's expectation and Task 2's Silence bullet point at it, Task 13 §1 says what `no settings directory` means in a worktree and what such a worktree sees, and step 1 of the process-settings rule's *Reading a key* (Task 6) names the checkout — no directory in this checkout or, in a worktree, in the main checkout — so a worktree session reads the block the hook emits from the main checkout's settings
- fixed 2026-09-29 — [Important] F2: Task 14's mutation proof stashes an already committed edit and so cannot fail; license: the plan's own Task 10 Step 7 and *Order and independence* (the edit is committed before Task 14 runs); the proof restores `process-artifacts.md` from `develop` with `git show`, expects `FAILED (failures=7)` — one per `dir.` key the file reads — and restores with `git checkout --`, checked by `git status --porcelain`
- fixed 2026-09-29 — [Important] F3: Task 17 expects no `.gitignore` in `docs/specs/` although `dir.default: ignored` makes the skill write one (D22, D17 step 3); license: spec D22 and D17 step 3; Step 1 calls `docs/specs/` undecided rather than tracked, Step 3 expects `docs/specs/.gitignore` holding `*`, prints it and fails the run where it is missing, and Step 6 stores it in the evidence file
- fixed 2026-09-29 — [Important] F4: Task 17's disable guard counts two installed scopes and never disables; user- and project-level rules both load, so "a project copy wins" is false; ruling: 2026-09-29; Step 1 records every scope where the plugin is enabled in `$W/was` and the user-scope rules count, and asks two consents; Steps 2 and 6 disable and enable per scope with `--scope` and count the enabled installs; Step 2 moves `~/.claude/rules/working-process/` aside only with consent, Step 6 restores it and checks the count on disk, and the evidence file's `## rules` section says which case held and that Step 5 is weaker evidence where both sets were in context; the "wins on conflict" sentence is gone
- fixed 2026-09-29 — [Important] F5: the Python 3.9 floor is asserted and never exercised; tests run on the system interpreter unstated; license: the plan's own *Tech Stack* claim (`Python 3.9+`) and the precedent `tests/working-process/test_decision_coverage.py`; a Global Constraint states the tests are stdlib-only `unittest` run by the system `python3` with no Python project or lockfile, and Task 16 Step 1 runs the suite once under `uv run --python 3.9 --no-project`, printing a note where uv is absent
- fixed 2026-09-29 — [Minor] F6: the `incomplete:` reservation cuts blocks that fit under 4096 bytes; license: spec D10 (caps its output at 4 KB, saying so when it truncates — a block under the cap is not truncated); Settled format edge 5 and Task 2's cap bullet emit a block of at most 4096 bytes whole and reserve the `incomplete:` line only when a cut is needed, and case 12 gains the edge fixture at exactly 4096 bytes and one byte over
- fixed 2026-09-29 — [Minor] F7: hook-mode silence on failure names no mechanism beyond `die`; license: spec D10 (exits 0 on any error of its own; its other modes report failure); Task 2's *Errors of the loader's own* names the subshell — `block=$(set -e; build_block 2>/dev/null) || block=''`, printed only on success, exit 0 — and `error: loader failed` with exit 1 in the other modes; `build_block` joins the function list, `run_loader` gains `path_prefix`, and case 11 gains an `awk` shim exiting 1 with empty stdout, empty stderr and exit 0 in hook mode and exit 1 under `--print`
- fixed 2026-09-29 — [Minor] F8: the rule says the `.gitignore` holds "the single line" while Deviation 4 allows more; license: Deviation 4; Task 6's rule text reads "which holds the line `settings.local.md`"; the README sentence Task 15 writes makes no line-count claim and stands
- fixed 2026-09-29 — [Minor] F9: `--set`'s "every other byte untouched" is unprovable without a trailing newline or with CRLF; the temp file has no cleanup trap; license: spec D37 (a write inserts, replaces and reports; every other line stays untouched) and the precedent `scripts/write-manifest.sh`; Task 5's contract says "every other line untouched", gains a *Line endings* bullet — a missing final newline is added, CRLF is preserved on untouched lines, the written line ends in LF — and the `trap 'rm -f "$tmp"' EXIT`; case 24 gains the no-final-newline fixture and case 25 the CRLF fixture, read as bytes
- fixed 2026-09-29 — [Minor] F10: the review commands' "and record" names neither the key nor `--set`; license: spec D45 (a first-create question answered "and record" writes the exception for the directory asked about); Task 12's replacement says the answer writes `dir.docs/code-review` through the loader's `--set`, and check B expects 2
- signal 2026-09-29 — another round earns its cost: F1 and F4 change the loader contract and the dogfood procedure, F2 and F3 are wrong verification steps; one diff-scoped round over the fixes should suffice
