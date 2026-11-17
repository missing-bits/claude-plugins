import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "plugins" / "working-process" / "scripts" / "document-check.py"
PHRASE = REPO / "plugins" / "working-process" / "scripts" / "phrase-check.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DocumentCheck(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = tmp.name
        subprocess.run(["git", "init", "-q", self.root], check=True)

    def write(self, rel, text, newline="\n"):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            f.write(text.replace("\n", newline))
        return path

    def run_check(self, path):
        return subprocess.run([sys.executable, str(SCRIPT), path], capture_output=True, text=True, cwd=self.root)

    def hits(self, r):
        return [l for l in r.stdout.splitlines() if not l.startswith("document-check:")]

    def summary(self, r, check):
        for l in r.stdout.splitlines():
            if l.startswith(f"document-check: {check} "):
                return l
        self.fail(r.stdout)

    def spec(self, body, rel="docs/specs/s.md", **kw):
        return self.write(rel, "---\ntitle: t\n---\n\n" + body, **kw)

    def test_type_by_path_then_frontmatter(self):
        m = load(SCRIPT, "dc")
        cases = [
            ("docs/technical-designs/x.md", "---\nspec: s.md\n---\n", "technical-design"),
            ("docs/tickets/A-1-x/A-1-x-technical-design.md", "---\ntitle: t\n---\n", "technical-design"),
            ("docs/plans/p.md", "---\nspec: s.md\n---\n", "plan"),
            ("docs/specs/s.md", "---\ntitle: t\n---\n", "spec"),
            ("docs/specs/n.md", "no frontmatter\n", "spec"),
        ]
        for rel, text, want in cases:
            path = self.write(rel, text)
            lines = text.splitlines()
            fm = {}
            if lines and lines[0] == "---":
                for l in lines[1:]:
                    if l == "---":
                        break
                    k, _, v = l.partition(":")
                    fm[k] = v.strip()
            self.assertEqual(m.doc_type(path, fm), want, rel)

    def test_named_section_wrong_side_is_hit(self):
        p = self.spec("## Gamma\n\nText.\n\nSee *Gamma* below.\n")
        r = self.run_check(p)
        self.assertEqual(r.returncode, 0, r.stderr)
        h = self.hits(r)
        self.assertEqual(len(h), 1, r.stdout)
        self.assertTrue(h[0].endswith("check: references"), h[0])
        self.assertIn(":9 ", h[0])

    def test_named_section_right_side_is_clean(self):
        p = self.spec("See *Gamma* below.\n\n## Gamma\n")
        r = self.run_check(p)
        self.assertEqual(self.hits(r), [])
        self.assertIn("references 1 checked, 0 not checked", self.summary(r, "references"))

    def test_unknown_name_is_not_checked(self):
        p = self.spec("See *Nowhere* below.\n\n## Gamma\n")
        r = self.run_check(p)
        self.assertEqual(self.hits(r), [])
        self.assertIn("references 0 checked, 1 not checked", self.summary(r, "references"))

    def test_duplicate_heading_not_checked(self):
        p = self.spec("## Gamma\n\nSee *Gamma* below.\n\n### Gamma\n")
        r = self.run_check(p)
        self.assertEqual(self.hits(r), [])
        self.assertIn("references 0 checked, 1 not checked", self.summary(r, "references"))

    def test_number_prefix_and_quotes(self):
        p = self.spec('## 3.2 Gamma\n\nSee "gamma" above.\n')
        r = self.run_check(p)
        self.assertEqual(self.hits(r), [])
        self.assertIn("references 1 checked", self.summary(r, "references"))

    def test_wrapped_sentence(self):
        p = self.spec("## Gamma\n\nWe come back to the\nmatter in *Gamma*\nbelow.\n")
        r = self.run_check(p)
        self.assertEqual(len(self.hits(r)), 1, r.stdout)

    def test_plan_task_reference(self):
        body = "### Task 1: a\n\n### Task 2: b\n\nSee Task 3 for more.\n"
        r = self.run_check(self.write("docs/plans/p.md", "---\nspec: s.md\n---\n\n" + body))
        h = self.hits(r)
        self.assertEqual(len(h), 1, r.stdout)
        self.assertTrue(h[0].endswith("check: references"))
        r = self.run_check(self.write("docs/plans/p.md", "---\nspec: s.md\n---\n\n" + body + "\n### Task 3: c\n"))
        self.assertEqual(self.hits(r), [])

    def test_bare_below_and_step_are_not_checked(self):
        p = self.spec("See below.\n\nStep 2 comes first.\n\nCited in §4.\n")
        r = self.run_check(p)
        self.assertEqual(self.hits(r), [])
        self.assertIn("references 0 checked, 3 not checked", self.summary(r, "references"))

    def test_step_label_is_not_a_reference(self):
        body = "### Task 1: a\n\n- [ ] **Step 1: Write it**\n\n- [ ] **Step 2** run\n\nStep 3: do.\n"
        r = self.run_check(self.write("docs/plans/p.md", "---\nspec: s.md\n---\n\n" + body))
        self.assertEqual(self.hits(r), [])
        self.assertIn("references 0 checked, 0 not checked", self.summary(r, "references"))

    def test_ledger_reads_last_round_only(self):
        wrong = "See *Gamma* below.\n"
        head = "## Gamma\n\n## Review rounds\n\n"
        early = self.spec(head + "### Round 1\n\n" + wrong + "\n### Round 2\n\nclean\n", rel="docs/specs/a.md")
        self.assertEqual(self.hits(self.run_check(early)), [])
        last = self.spec(head + "### Round 1\n\nclean\n\n### Round 2\n\n" + wrong, rel="docs/specs/b.md")
        self.assertEqual(len(self.hits(self.run_check(last))), 1)
        none = self.spec(head + wrong, rel="docs/specs/c.md")
        self.assertEqual(len(self.hits(self.run_check(none))), 1)

    def test_fenced_block_ignored(self):
        p = self.spec("## Gamma\n\n```\nSee *Gamma* below.\n```\n")
        r = self.run_check(p)
        self.assertEqual(self.hits(r), [])
        self.assertIn("references 0 checked, 0 not checked", self.summary(r, "references"))

    def test_crlf_document(self):
        p = self.spec("## Gamma\n\nSee *Gamma* below.\n", newline="\r\n")
        r = self.run_check(p)
        self.assertEqual(len(self.hits(r)), 1, r.stdout)

    def test_no_frontmatter_and_unclosed_frontmatter(self):
        r = self.run_check(self.write("docs/specs/n.md", "Plain.\n"))
        self.assertEqual(r.returncode, 0)
        self.assertEqual(len([l for l in r.stdout.splitlines() if l.startswith("document-check:")]), 3)
        r = self.run_check(self.write("docs/specs/u.md", "---\n## Gamma\n\nSee *Gamma* below.\n"))
        self.assertEqual(len(self.hits(r)), 1, r.stdout)
        self.assertIn(":4 ", self.hits(r)[0])

    def test_exit_codes(self):
        self.assertEqual(self.run_check(os.path.join(self.root, "missing.md")).returncode, 1)
        r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)

    def test_summary_lines_shape(self):
        r = self.run_check(self.spec("## Gamma\n\nSee *Gamma* below.\n"))
        tail = r.stdout.splitlines()[-3:]
        for line, name in zip(tail, ["references", "citations", "table-closure"]):
            self.assertRegex(line, rf"^document-check: {name} ")
        self.assertIn("table-closure not applicable", tail[2])

    def test_body_lines(self):
        m = load(SCRIPT, "dc")
        self.assertEqual(m.body_lines("---\na: b\n---\nx\n```\ny\n```\nz\n"), [(4, "x"), (8, "z")])
        self.assertEqual(m.body_lines("---\na\nx\n"), [(1, "---"), (2, "a"), (3, "x")])

    def test_normalise_is_phrase_checks(self):
        m = load(SCRIPT, "dc")
        self.assertEqual(m.normalise("- A  B"), load(PHRASE, "pc").normalise("- A  B"))


if __name__ == "__main__":
    unittest.main()
