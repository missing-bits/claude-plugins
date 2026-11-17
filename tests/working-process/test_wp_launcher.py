"""Tests for the plugins/working-process/bin launchers."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BIN = REPO / "plugins" / "working-process" / "bin"
LAUNCHER = str(BIN / "wp-phrase-check")
BASH = shutil.which("bash")
READLINK = shutil.which("readlink")
PASSING = ["--phrase", "alpha", "--before", "0", "--after", "1", "--side", "after"]

GOOD = f'#!{BASH}\nexec {sys.executable} "$@"\n'
OLD = f'#!{BASH}\nif [ "$1" = "-c" ]; then exit 1; fi; echo WRONG-INTERPRETER; exit 0\n'
GOOD_PY = f'#!{BASH}\n[ "$1" = "-3" ] || exit 9; shift; exec {sys.executable} "$@"\n'


@unittest.skipIf(os.name == "nt", "bash launcher")
class Launcher(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = tmp.name
        self.stubs = os.path.join(self.dir, "stubs")
        os.mkdir(self.stubs)
        os.symlink(READLINK, os.path.join(self.stubs, "readlink"))
        self.file = os.path.join(self.dir, "in.md")
        with open(self.file, "w") as f:
            f.write("alpha\n")

    def stub(self, name, body):
        path = os.path.join(self.stubs, name)
        with open(path, "w") as f:
            f.write(body)
        os.chmod(path, 0o755)

    def run_launcher(self, *args, launcher=LAUNCHER):
        return subprocess.run([BASH, launcher, *args], env={"PATH": self.stubs}, capture_output=True, text=True)

    def assert_pass(self, r):
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(r.stdout.startswith("wp-phrase-check: PASS"), r.stdout)

    def test_python3_runs(self):
        self.stub("python3", GOOD)
        self.assert_pass(self.run_launcher(self.file, *PASSING))

    def test_old_python3_is_skipped_for_python(self):
        self.stub("python3", OLD)
        self.stub("python", GOOD)
        r = self.run_launcher(self.file, *PASSING)
        self.assert_pass(r)
        self.assertNotIn("WRONG-INTERPRETER", r.stdout)

    def test_py_launcher_is_last_resort(self):
        self.stub("py", GOOD_PY)
        self.assert_pass(self.run_launcher(self.file, *PASSING))

    def test_no_python_names_what_it_tried(self):
        self.stub("python3", OLD)
        r = self.run_launcher(self.file, *PASSING)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stdout, "")
        for s in ("python3 (rejected)", "python (not found)", "py -3 (not found)"):
            self.assertIn(s, r.stderr)

    def test_exit_code_passes_through(self):
        self.stub("python3", GOOD)
        r = self.run_launcher(self.file, "--phrase", "alpha", "--before", "0", "--after", "2", "--side", "after")
        self.assertEqual(r.returncode, 1)
        self.assertTrue(r.stdout.startswith("wp-phrase-check: FAIL"), r.stdout)

    def test_symlinked_launcher_finds_script(self):
        self.stub("python3", GOOD)
        other = tempfile.TemporaryDirectory()
        self.addCleanup(other.cleanup)
        link = os.path.join(other.name, "link")
        os.symlink(LAUNCHER, link)
        self.assert_pass(self.run_launcher(self.file, *PASSING, launcher=link))

    def test_bare_name_invocation_from_bin_dir(self):
        self.stub("python3", GOOD)
        r = subprocess.run([BASH, "wp-phrase-check", self.file, *PASSING], env={"PATH": self.stubs},
                           cwd=os.path.dirname(LAUNCHER), capture_output=True, text=True)
        self.assert_pass(r)

    def test_path_with_space_survives_launcher(self):
        self.stub("python3", GOOD)
        spaced = os.path.join(self.dir, "two words.md")
        with open(spaced, "w") as f:
            f.write("alpha\n")
        r = self.run_launcher(spaced, *PASSING)
        self.assert_pass(r)
        self.assertTrue(any(l.endswith("two words.md: lines 1, matches 1") for l in r.stdout.splitlines()), r.stdout)

    def test_bin_copies_are_identical(self):
        files = sorted(p for p in BIN.iterdir() if p.is_file())
        for p in files:
            self.assertTrue(os.access(p, os.X_OK), p)
            self.assertEqual(p.read_bytes(), files[0].read_bytes(), p)

    def test_each_launcher_has_its_script(self):
        for p in BIN.glob("wp-*"):
            script = BIN.parent / "scripts" / (p.name[3:] + ".py")
            self.assertTrue(script.is_file(), script)

    def test_decision_coverage_launcher_runs(self):
        self.stub("python3", GOOD)
        specs = os.path.join(self.dir, "docs", "specs")
        os.makedirs(specs)
        spec = os.path.join(specs, "s.md")
        with open(spec, "w") as f:
            f.write("---\ndecisions: registered\n---\n\n## Decisions\n\n- **D1** — One.\n")
        r = self.run_launcher(spec, launcher=str(BIN / "wp-decision-coverage"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(r.stdout.startswith("decision-coverage:"), r.stdout)


if __name__ == "__main__":
    unittest.main()
