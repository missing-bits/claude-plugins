"""Tests for plugins/working-process/scripts/phrase-check.py."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = str(REPO / "plugins" / "working-process" / "scripts" / "phrase-check.py")


class PhraseCheck(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = tmp.name

    def write(self, name, content):
        path = os.path.join(self.dir, name)
        with open(path, "wb" if isinstance(content, bytes) else "w", **({} if isinstance(content, bytes) else {"newline": "", "encoding": "utf-8"})) as f:
            f.write(content)
        return path

    def run_check(self, *args):
        return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)

    def ok(self, path, phrase, before, after, side="after", actual=None, *extra):
        p = self.run_check(path, f"--phrase={phrase}", "--before", str(before), "--after", str(after), "--side", side, *extra)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        if actual is not None:
            self.assertIn(f"actual: {actual}", p.stdout)
        return p

    def test_wrapped_phrase_counts(self):
        self.ok(self.write("a.md", "alpha beta\ngamma delta\n"), "beta gamma", 0, 1, actual=1)

    def test_capital_after_wrap(self):
        self.ok(self.write("a.md", "the quick\nBrown fox\n"), "quick brown", 0, 1, actual=1)

    def test_doubled_whitespace(self):
        path = self.write("a.md", "alpha  \t beta\n")
        self.ok(path, "alpha beta", 0, 1, actual=1)
        self.ok(path, "alpha   beta", 0, 1, actual=1)

    def test_crlf_wrap_counts(self):
        self.ok(self.write("a.md", b"alpha\r\nbeta\r\n"), "alpha beta", 0, 1, actual=1)

    def test_bom_does_not_hide_first_word(self):
        self.ok(self.write("a.md", b"\xef\xbb\xbfalpha beta\n"), "alpha beta", 0, 1, actual=1)

    def test_list_and_quote_markers_dropped(self):
        path = self.write("a.md", "- alpha\n  beta\n> gamma\n> delta\n1. one\n   two\n2) three\n* four\n+ five\n")
        for phrase in ("alpha beta", "gamma delta", "one two three four five"):
            self.ok(path, phrase, 0, 1, actual=1)

    def test_nested_markers_dropped(self):
        self.ok(self.write("a.md", "> - alpha\n> beta\n"), "alpha beta", 0, 1, actual=1)

    def test_inline_markup_untouched(self):
        path = self.write("a.md", "**alpha** beta\n---\n-dash\n# head\n")
        self.ok(path, "alpha beta", 1, 0, actual=0)
        self.ok(path, "**alpha** beta --- -dash # head", 0, 1, actual=1)

    def test_phrase_normalised_like_text(self):
        self.ok(self.write("a.md", "alpha beta\n"), "- Alpha\n  BETA", 0, 1, actual=1)

    def test_phrase_starting_with_hyphen(self):
        self.ok(self.write("a.md", "use --side here\n"), "--side", 0, 1, actual=1)

    def test_no_match_across_files(self):
        a = self.write("a.md", "alpha\n")
        b = self.write("b.md", "beta\n")
        p = self.run_check(a, b, "--phrase=alpha beta", "--before", "1", "--after", "0", "--side", "after")
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("actual: 0", p.stdout)

    def test_matches_do_not_overlap(self):
        self.ok(self.write("a.md", "aa aa aa\n"), "aa aa", 0, 1, actual=1)
        self.ok(self.write("b.md", "ab ab ab ab\n"), "ab ab", 0, 2, actual=2)

    def test_total_over_files_and_what_was_read(self):
        a = self.write("a.md", "x\nalpha\n")
        b = self.write("b.md", "alpha\nalpha\ny\n")
        p = self.run_check(a, b, "--phrase=alpha", "--before", "0", "--after", "3", "--side", "after")
        self.assertEqual(p.returncode, 0, p.stdout)
        lines = p.stdout.splitlines()
        self.assertEqual(lines[0], "wp-phrase-check: PASS")
        for want in ("expected: 3 (before 0, after 3)", "actual: 3", "read: files 2, lines 5"):
            self.assertIn(want, lines)
        self.assertTrue(any(l.endswith("a.md: lines 2, matches 1") for l in lines))
        self.assertTrue(any(l.endswith("b.md: lines 3, matches 2") for l in lines))

    def test_same_path_twice_counts_twice(self):
        a = self.write("a.md", "alpha\n")
        p = self.run_check(a, a, "--phrase=alpha", "--before", "0", "--after", "2", "--side", "after")
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("read: files 2, lines 2", p.stdout)

    def test_empty_file_is_read(self):
        p = self.ok(self.write("a.md", ""), "alpha", 1, 0, actual=0)
        self.assertIn("read: files 1, lines 0", p.stdout)

    def test_side_selects_the_number(self):
        path = self.write("a.md", "alpha\n")
        self.ok(path, "alpha", 1, 0, side="before")
        p = self.run_check(path, "--phrase=alpha", "--before", "1", "--after", "0", "--side", "after")
        self.assertEqual(p.returncode, 1)
        self.assertIn("fail: count mismatch: expected 0 on side after, found 1", p.stdout)

    def test_mismatch_fails(self):
        path = self.write("a.md", "alpha\n")
        p = self.run_check(path, "--phrase=alpha", "--before", "0", "--after", "2", "--side", "after")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stdout.splitlines()[0], "wp-phrase-check: FAIL")
        self.assertIn("fail: count mismatch: expected 2 on side after, found 1", p.stdout)

    def test_equal_counts_fail_unless_declared(self):
        path = self.write("a.md", "alpha\n")
        for side in ("before", "after"):
            p = self.run_check(path, "--phrase=alpha", "--before", "1", "--after", "1", "--side", side)
            self.assertEqual(p.returncode, 1)
            self.assertIn("fail: vacuous", p.stdout)
        p = self.run_check(path, "--phrase=alpha", "--before", "1", "--after", "1", "--side", "after", "--unchanged")
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertNotIn("fail:", p.stdout)

    def test_mismatch_reported_before_vacuity(self):
        path = self.write("a.md", "alpha\n")
        p = self.run_check(path, "--phrase=alpha", "--before", "2", "--after", "2", "--side", "after")
        self.assertEqual(p.returncode, 1)
        self.assertIn("fail: count mismatch", p.stdout)
        self.assertIn("fail: vacuous", p.stdout)
        self.assertLess(p.stdout.index("fail: count mismatch"), p.stdout.index("fail: vacuous"))

    def test_missing_path_fails(self):
        p = self.run_check(os.path.join(self.dir, "nope.md"), "--phrase=alpha", "--before", "1", "--after", "0", "--side", "after")
        self.assertEqual(p.returncode, 1)
        self.assertIn("actual: not counted", p.stdout)
        self.assertTrue(any(l.startswith("fail:") and l.endswith("no such file") for l in p.stdout.splitlines()))
        self.assertNotIn("fail: count mismatch", p.stdout)

    def test_directory_fails(self):
        p = self.run_check(self.dir, "--phrase=alpha", "--before", "1", "--after", "0", "--side", "after")
        self.assertEqual(p.returncode, 1)
        self.assertTrue(any(l.startswith("fail:") and l.endswith("not a file") for l in p.stdout.splitlines()))

    def test_invalid_utf8_fails(self):
        path = self.write("a.md", b"\xff\xfe alpha\n")
        p = self.run_check(path, "--phrase=alpha", "--before", "0", "--after", "1", "--side", "after")
        self.assertEqual(p.returncode, 1)
        self.assertTrue(any(l.startswith("fail:") and l.endswith("not valid UTF-8") for l in p.stdout.splitlines()))

    @unittest.skipIf(os.name == "nt" or (hasattr(os, "geteuid") and os.geteuid() == 0), "chmod 0 does not block")
    def test_unopenable_file_fails(self):
        path = self.write("a.md", "alpha\n")
        os.chmod(path, 0)
        p = self.run_check(path, "--phrase=alpha", "--before", "0", "--after", "1", "--side", "after")
        self.assertEqual(p.returncode, 1)
        self.assertTrue(any(l.startswith("fail:") and "cannot be read" in l for l in p.stdout.splitlines()))

    def test_one_bad_path_fails_the_run(self):
        a = self.write("a.md", "alpha\n")
        p = self.run_check(a, os.path.join(self.dir, "nope.md"), "--phrase=alpha", "--before", "0", "--after", "1", "--side", "after")
        self.assertEqual(p.returncode, 1)
        self.assertIn("actual: not counted", p.stdout)
        self.assertIn("read: files 1, lines 1", p.stdout)

    def test_no_path_fails(self):
        p = self.run_check("--phrase=alpha", "--before", "1", "--after", "0", "--side", "after")
        self.assertEqual(p.returncode, 1)
        self.assertIn("fail: read no file", p.stdout)

    def test_blank_phrase_is_usage_error(self):
        path = self.write("a.md", "alpha\n")
        p = self.run_check(path, "--phrase=   ", "--before", "0", "--after", "1", "--side", "after")
        self.assertEqual(p.returncode, 2)

    def test_negative_count_is_usage_error(self):
        path = self.write("a.md", "alpha\n")
        p = self.run_check(path, "--phrase=alpha", "--before=-1", "--after", "0", "--side", "after")
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main()
