"""Tests for plugins/working-process/scripts/decision-coverage.py.

Each test builds its documents in a temporary directory, runs the script
on one of them and asserts the exact lines the contract names.
"""

import os
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = str(REPO / "plugins" / "working-process" / "scripts" / "decision-coverage.py")
DERIVATION = " — derivation: decision-coverage.py, "

SPEC_BASIC = """\
---
status: draft
decisions: registered
---

# S

## Decisions

- **D1** — One.
- **D2** — Two.
- **D3** — Group.
  - **D3.1** — Three one.
  - **D3.2** — Three two.

## Next

Text.
"""

PLAN_BASIC = """\
---
status: draft
spec: ../specs/s.md
---

# P

## Global Constraints

- **Realizes:** D2 — **No code** anywhere.
- **Commits are one line.**

## File structure

Text.

### Task 1: one

**Files:** a

**Realizes:** D1

- [ ] **Step 1: do**

### Task 2: two

**Realizes:** D3.1

### Task 3: three

**Realizes:** D3.2
"""


def dedent(text):
    return textwrap.dedent(text)


def line_of(text, needle):
    """1-based number of the first line containing needle."""
    for number, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return number
    raise AssertionError(f"{needle!r} not in text")


class Result:
    def __init__(self, proc):
        self.proc = proc
        self.lines = proc.stdout.splitlines()
        self.hits = [line for line in self.lines if DERIVATION in line]
        self.map = [line for line in self.lines if line.startswith("  ")]
        self.blocks = [line for line in self.lines if line.startswith("decision-coverage: ")]


class CoverageTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "specs").mkdir()
        (self.root / "plans").mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, relative, text):
        path = self.root / relative
        path.write_text(text, encoding="utf-8")
        return path

    def run_script(self, relative):
        proc = subprocess.run(
            [sys.executable, SCRIPT, str(self.root / relative)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stderr, "")
        return Result(proc)

    def assert_hit_at(self, result, filename, line, needle=None):
        prefix = f"{filename}:{line} — "
        found = [h for h in result.hits if os.path.basename(h.split(" — ")[0].rsplit(":", 1)[0]) == filename
                 and h.split(" — ")[0].endswith(f":{line}")]
        self.assertTrue(found, f"no hit at {prefix} in {result.lines}")
        if needle is not None:
            self.assertTrue(any(needle in h for h in found), f"{needle!r} not in {found}")

    # 1
    def test_01_full_coverage_with_global_constraint(self):
        self.write("specs/s.md", SPEC_BASIC)
        self.write("plans/p.md", PLAN_BASIC)
        result = self.run_script("plans/p.md")
        n = line_of(PLAN_BASIC, "- **Realizes:** D2")
        self.assertEqual(result.hits, [])
        self.assertEqual(result.lines, [
            "decision-coverage: ../specs/s.md 4/4 covered; inherited []; deferred []; uncovered []",
            "  D1 → Task 1",
            f'  D2 → Global Constraints, line {n}: "No code anywhere."',
            "  D3.1 → Task 2",
            "  D3.2 → Task 3",
        ])
        self.assertNotIn("CLEAN", result.proc.stdout)

    # 2
    def test_02_uncovered_leaf(self):
        self.write("specs/s.md", SPEC_BASIC)
        plan = PLAN_BASIC.replace("**Realizes:** D3.1", "**Realizes:** none")
        self.write("plans/p.md", plan)
        result = self.run_script("plans/p.md")
        self.assertEqual(len(result.hits), 1, result.lines)
        self.assertIn("D3.1", result.hits[0])
        self.assertIn(
            "decision-coverage: ../specs/s.md 3/4 covered; inherited []; deferred []; uncovered [D3.1]",
            result.lines)
        self.assertIn("  D3.1 → —", result.lines)

    # 3
    def test_03_fenced_grammar_instantiates_nothing(self):
        self.write("specs/s.md", dedent("""\
            ---
            decisions: registered
            ---

            ## Decisions

            - **D1** — One.
            """))
        plan = dedent("""\
            ---
            spec: ../specs/s.md
            ---

            ## Global Constraints

            ```
            - **Realizes:** D9 — quoted.
            ```

            ## Deferrals and predecessors

            ```
            **Defers:** D1 — x; ruling: 2026-01-01
            **Realizes:** D9
            ```

            ### Task 1: one

            **Realizes:** D1

            ```
            **Realizes:** D9
            ### Task 9: quoted
            ```
            """)
        self.write("plans/p.md", plan)
        result = self.run_script("plans/p.md")
        self.assertEqual(result.hits, [])
        self.assertNotIn("D9", result.proc.stdout)
        self.assertEqual(result.lines, [
            "decision-coverage: ../specs/s.md 1/1 covered; inherited []; deferred []; uncovered []",
            "  D1 → Task 1",
        ])

    # 4
    def test_04_task_without_realizes_line(self):
        self.write("specs/s.md", SPEC_BASIC)
        plan = PLAN_BASIC.replace("### Task 3: three\n\n**Realizes:** D3.2\n",
                                  "### Task 3: three\n\nNo annotation.\n\n### Task 4: four\n\n**Realizes:** D3.2\n")
        self.write("plans/p.md", plan)
        result = self.run_script("plans/p.md")
        self.assertEqual(len(result.hits), 1, result.lines)
        self.assert_hit_at(result, "p.md", line_of(plan, "### Task 3"), "Task 3")
        self.assertIn(
            "decision-coverage: ../specs/s.md 4/4 covered; inherited []; deferred []; uncovered []",
            result.lines)

    # 5
    def test_05_withdrawn_entry(self):
        spec = dedent("""\
            ---
            decisions: registered
            ---

            ## Decisions

            - **D1** — One.
            - **D2** — Two. Argued in *X*.
              withdrawn superseded by D1. See notes, ruling: 2026-01-01; replaced by D1.
            """)
        self.write("specs/s.md", spec)
        plan = dedent("""\
            ---
            spec: ../specs/s.md
            ---

            ### Task 1: one

            **Realizes:** D1, D2
            """)
        self.write("plans/p.md", plan)
        result = self.run_script("plans/p.md")
        self.assertEqual(len(result.hits), 1, result.lines)
        self.assert_hit_at(result, "p.md", line_of(plan, "**Realizes:** D1, D2"), "D2")
        self.assertEqual(result.blocks, [
            "decision-coverage: ../specs/s.md 1/1 covered; inherited []; deferred []; uncovered []",
        ])
        self.assertEqual(result.map, ["  D1 → Task 1"])

    # 6
    def assert_malformed(self, register, bad_line_needle):
        spec = "---\ndecisions: registered\n---\n\n## Decisions\n\n" + dedent(register)
        self.write("specs/s.md", spec)
        self.write("plans/p.md", dedent("""\
            ---
            spec: ../specs/s.md
            ---

            ### Task 1: one

            **Realizes:** D1
            """))
        result = self.run_script("plans/p.md")
        self.assertGreaterEqual(len(result.hits), 1, result.lines)
        self.assert_hit_at(result, "s.md", line_of(spec, bad_line_needle))
        self.assertEqual(result.blocks,
                         ["decision-coverage: ../specs/s.md not counted — malformed register"])
        self.assertEqual(result.map, [])

    def test_06a_duplicate_identifier(self):
        self.assert_malformed("""\
            - **D1** — One.
            - **D2** — Two.
            - **D1** — One again.
            """, "One again")

    def test_06b_child_without_parent(self):
        self.assert_malformed("""\
            - **D1** — One.
              - **D4.1** — Orphan.
            """, "Orphan")

    def test_06c_group_with_token(self):
        self.assert_malformed("""\
            - **D1** — One.
            - **D3** — Group. withdrawn old, ruling: 2026-01-01
              - **D3.1** — Child.
            """, "Group.")

    def test_06d_replaced_by_itself(self):
        self.assert_malformed("""\
            - **D1** — One.
            - **D2** — Two. withdrawn old, ruling: 2026-01-01; replaced by D2
            """, "Two.")

    def test_06e_replacement_cycle(self):
        self.assert_malformed("""\
            - **D1** — One. withdrawn old, ruling: 2026-01-01; replaced by D2
            - **D2** — Two. withdrawn old, ruling: 2026-01-01; replaced by D1
            - **D3** — Three.
            """, "One.")

    def test_06f_numbered_list(self):
        self.assert_malformed("""\
            1. **D1** — One.
            2. **D2** — Two.
            """, "1. **D1**")

    # 7
    def test_07_legacy_spec(self):
        self.write("specs/s.md", "---\nstatus: draft\n---\n\n# S\n\n## Decisions\n\n- **D1** — x.\n")
        self.write("plans/p.md", dedent("""\
            ---
            spec: ../specs/s.md
            ---

            ### Task 1: one

            No annotation.
            """))
        result = self.run_script("plans/p.md")
        self.assertEqual(result.lines,
                         ["decision-coverage: ../specs/s.md not checked — no decision register"])

    # 8
    def test_08_bare_identifier_in_multi_spec_plan(self):
        one = "---\ndecisions: registered\n---\n\n## Decisions\n\n- **D1** — One.\n"
        self.write("specs/a.md", one)
        self.write("specs/b.md", one)
        plan = dedent("""\
            ---
            spec: [../specs/a.md, ../specs/b.md]
            ---

            ### Task 1: one

            **Realizes:** ../specs/a.md#D1

            ### Task 2: two

            **Realizes:** D1
            """)
        self.write("plans/p.md", plan)
        result = self.run_script("plans/p.md")
        self.assert_hit_at(result, "p.md", line_of(plan, "**Realizes:** D1"), "D1")
        self.assertIn(
            "decision-coverage: ../specs/a.md 1/1 covered; inherited []; deferred []; uncovered []",
            result.lines)
        self.assertIn("  ../specs/a.md#D1 → Task 1", result.lines)
        self.assertIn(
            "decision-coverage: ../specs/b.md 0/1 covered; inherited []; deferred []; uncovered [../specs/b.md#D1]",
            result.lines)

    # 9
    def test_09_deferrals(self):
        self.write("specs/s.md", SPEC_BASIC)
        valid = PLAN_BASIC.replace("**Realizes:** D3.1", "**Realizes:** none").replace(
            "## File structure",
            "## Deferrals and predecessors\n\n**Defers:** D3.1 — later; ruling: 2026-01-01\n\n## File structure")
        self.write("plans/p.md", valid)
        result = self.run_script("plans/p.md")
        self.assertEqual(result.hits, [])
        self.assertIn(
            "decision-coverage: ../specs/s.md 3/3 covered; inherited []; deferred [D3.1]; uncovered []",
            result.lines)
        self.assertNotIn("  D3.1 → —", result.lines)

        cited = PLAN_BASIC.replace(
            "## File structure",
            "## Deferrals and predecessors\n\n**Defers:** D1 — later; ruling: 2026-01-01\n\n## File structure")
        self.write("plans/p.md", cited)
        result = self.run_script("plans/p.md")
        self.assertEqual(len(result.hits), 1, result.lines)
        self.assert_hit_at(result, "p.md", line_of(cited, "**Defers:** D1"), "D1")
        self.assertIn(
            "decision-coverage: ../specs/s.md 4/4 covered; inherited []; deferred []; uncovered []",
            result.lines)
        self.assertIn("  D1 → Task 1", result.lines)

    # 10
    def follows_case(self, spec, predecessor_status):
        self.write("specs/s.md", spec)
        self.write("plans/p0.md", dedent(f"""\
            ---
            status: {predecessor_status}
            spec: ../specs/s.md
            ---

            ### Task 1: earlier

            **Realizes:** D2
            """))
        plan = dedent("""\
            ---
            spec: ../specs/s.md
            ---

            ## Deferrals and predecessors

            **Follows:** ../plans/p0.md

            ### Task 1: one

            **Realizes:** D1
            """)
        self.write("plans/p.md", plan)
        return plan, self.run_script("plans/p.md")

    def test_10a_inherited_from_implemented_predecessor(self):
        spec = "---\ndecisions: registered\n---\n\n## Decisions\n\n- **D1** — One.\n- **D2** — Two.\n"
        _, result = self.follows_case(spec, "implemented")
        self.assertEqual(result.lines, [
            "decision-coverage: ../specs/s.md 2/2 covered; inherited [D2]; deferred []; uncovered []",
            "  D1 → Task 1",
            "  D2 → ../plans/p0.md (Task 1)",
        ])

    def test_10b_draft_predecessor_lends_nothing(self):
        spec = "---\ndecisions: registered\n---\n\n## Decisions\n\n- **D1** — One.\n- **D2** — Two.\n"
        plan, result = self.follows_case(spec, "draft")
        self.assert_hit_at(result, "p.md", line_of(plan, "**Follows:**"))
        self.assertIn(
            "decision-coverage: ../specs/s.md 1/2 covered; inherited []; deferred []; uncovered [D2]",
            result.lines)
        self.assertIn("  D2 → —", result.lines)

    def test_10c_inherited_citation_withdrawn_since(self):
        spec = ("---\ndecisions: registered\n---\n\n## Decisions\n\n- **D1** — One.\n"
                "- **D2** — Two. withdrawn obsolete, ruling: 2026-02-01\n")
        _, result = self.follows_case(spec, "implemented")
        self.assertEqual(result.hits, [])
        self.assertEqual(result.lines, [
            "decision-coverage: ../specs/s.md 1/1 covered; inherited []; deferred []; uncovered []",
            "  D1 → Task 1",
            "  withdrawn since: D2 ← ../plans/p0.md (Task 1)",
        ])

    # 11
    def test_11_spec_audited_alone(self):
        self.write("specs/s.md", SPEC_BASIC)
        result = self.run_script("specs/s.md")
        self.assertEqual(len(result.lines), 1, result.lines)
        self.assertTrue(result.lines[0].startswith("decision-coverage: "))
        self.assertTrue(result.lines[0].endswith("s.md register well formed"), result.lines)

        self.write("specs/s.md", SPEC_BASIC.replace("- **D2** — Two.", "- **D1** — Two."))
        result = self.run_script("specs/s.md")
        self.assertEqual(len(result.hits), 1, result.lines)
        self.assertEqual(len(result.blocks), 1)
        self.assertTrue(result.blocks[0].endswith("s.md not counted — malformed register"))

    # 12
    def test_12_repository_documents(self):
        spec = REPO / "docs" / "specs" / "2026-09-25-plan-coverage-design.md"
        plan = REPO / "docs" / "plans" / "2026-09-26-plan-coverage.md"
        ids = []
        in_register = False
        in_fence = False
        for line in spec.read_text(encoding="utf-8").splitlines():
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if line.startswith("## "):
                in_register = line.strip() == "## Decisions"
                continue
            match = re.match(r"^\s*- \*\*(D\d+(?:\.\d+)?)\*\*", line)
            if in_register and match:
                ids.append(match.group(1))
        leaves = [i for i in ids if not any(j.startswith(i + ".") for j in ids)]
        self.assertGreater(len(leaves), 0)

        proc = subprocess.run([sys.executable, SCRIPT, str(plan)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = Result(proc)
        self.assertEqual(result.hits, [])
        self.assertEqual(len(result.blocks), 1, result.lines)
        match = re.match(r"^decision-coverage: \S+ (\d+)/(\d+) covered;", result.blocks[0])
        self.assertIsNotNone(match, result.blocks[0])
        self.assertEqual((int(match.group(1)), int(match.group(2))), (len(leaves), len(leaves)))

        proc = subprocess.run([sys.executable, SCRIPT, str(spec)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.splitlines(),
                         [f"decision-coverage: {spec} register well formed"])


    # 13
    def test_13_technical_design_produces_no_output(self):
        (self.root / "docs" / "specs").mkdir(parents=True)
        (self.root / "docs" / "technical-designs").mkdir(parents=True)
        self.write("docs/specs/s.md", SPEC_BASIC)
        design = dedent("""\
            ---
            spec: ../specs/s.md
            ---

            # S — technical design

            Text.
            """)
        self.write("docs/technical-designs/s-technical-design.md", design)
        proc = subprocess.run(
            [sys.executable, SCRIPT,
             str(self.root / "docs" / "technical-designs" / "s-technical-design.md")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(proc.stderr, "")

    # 14
    def test_14_plan_under_plans_is_still_counted(self):
        self.write("specs/s.md", SPEC_BASIC)
        self.write("plans/p.md", PLAN_BASIC)
        result = self.run_script("plans/p.md")
        self.assertEqual(result.hits, [])
        match = re.match(r"^decision-coverage: \S+ (\d+)/(\d+) covered;", result.blocks[0])
        self.assertIsNotNone(match, result.blocks[0])
        self.assertEqual(match.group(1), match.group(2))


class UsageTest(unittest.TestCase):
    def test_usage_error(self):
        proc = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(len(proc.stderr.strip().splitlines()), 1)
        self.assertTrue(proc.stderr.startswith("decision-coverage: "), proc.stderr)

    def test_unreadable_file(self):
        proc = subprocess.run([sys.executable, SCRIPT, "/nonexistent/x.md"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(len(proc.stderr.strip().splitlines()), 1)
        self.assertTrue(proc.stderr.startswith("decision-coverage: "), proc.stderr)


if __name__ == "__main__":
    unittest.main()
