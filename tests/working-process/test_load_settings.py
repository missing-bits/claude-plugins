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

    # 1. Precedence and defaults.
    def test_precedence_and_defaults(self) -> None:
        self.git_init()
        self.settings(self.root, team="dir.default: tracked\n", local="review.autonomy: yes\n")
        res = self.run_loader(self.root)
        self.assertEqual(res.code, 0)
        self.assertEqual(res.err, "")
        self.assertEqual(res.lines[0], self.first_line(self.root))
        self.assertEqual(res.lines[1:1 + len(KEYS)], [res.line(k) for k in KEYS])
        self.assertEqual(len(res.lines), 1 + len(KEYS))
        self.assertEqual(res.line("dir.default"), "dir.default: tracked  [team]")
        self.assertEqual(res.line("dir.docs/specs"), "dir.docs/specs: tracked  [inherited]")
        self.assertEqual(res.line("dir.docs/memory"), "dir.docs/memory: tracked  [inherited]")
        self.assertEqual(res.line("dispatch.propagation-auditor-tier"),
                          "dispatch.propagation-auditor-tier: cheapest  [default]")
        self.assertEqual(res.line("consult.personas"), "consult.personas: unset  [default]")
        self.assertEqual(res.line("review.autonomy"), "review.autonomy: yes  [local]")

        printed = self.run_loader(self.root, "--print")
        self.assertEqual(printed.out, res.out)

    # 2. Suggestion.
    def test_suggestion(self) -> None:
        self.git_init()
        self.settings(self.root, team="consult.personas: yes\n")
        res = self.run_loader(self.root)
        self.assertEqual(res.line("consult.personas"), "consult.personas: unset  [team suggests: yes]")
        self.assertEqual(res.errors, [])
        self.assertTrue(res.lines[0].endswith("local: settings.local.md (absent))"))

        self.settings(self.root, team="consult.personas: yes\n", local="consult.personas: no\n")
        res2 = self.run_loader(self.root)
        self.assertEqual(res2.line("consult.personas"), "consult.personas: no  [local]")
        self.assertNotIn("suggests", res2.out)

    # 3. Invalid in the deciding file.
    def test_invalid_in_deciding_file(self) -> None:
        self.git_init()
        self.settings(self.root, team="consult.personas: yes\n",
                      local="review.autonomy: noo\nconsult.personas: \"no\"\n")
        res = self.run_loader(self.root)
        self.assertEqual(res.line("review.autonomy"), "review.autonomy: unset  [invalid in local]")
        self.assertEqual(res.line("consult.personas"), "consult.personas: unset  [invalid in local]")
        self.assertEqual(res.errors, [
            "error: settings.local.md:1 invalid value for `review.autonomy`: noo — unset",
            "error: settings.local.md:2 invalid value for `consult.personas`: \"no\" — unset",
        ])
        self.assertNotIn("yes", res.line("consult.personas"))
        self.assertNotIn("suggests", res.line("consult.personas"))

    # 4. Duplicate.
    def test_duplicate(self) -> None:
        self.git_init()
        self.settings(self.root, local="review.autonomy: yes\n\nreview.autonomy: no\n")
        res = self.run_loader(self.root)
        self.assertEqual(res.line("review.autonomy"), "review.autonomy: unset  [invalid in local]")
        self.assertIn(
            "error: settings.local.md:1,3 duplicate key `review.autonomy` — unset",
            res.errors,
        )

    def test_duplicate_where_one_line_invalid_gives_duplicate_alone(self) -> None:
        self.git_init()
        self.settings(self.root, local="review.autonomy: yes\nreview.autonomy: noo\n")
        res = self.run_loader(self.root)
        dup_errors = [e for e in res.errors if "review.autonomy" in e]
        self.assertEqual(len(dup_errors), 1)
        self.assertIn("duplicate key", dup_errors[0])

    # 5. Unknown key, and a team key in the personal file.
    def test_unknown_key_and_team_key_in_personal_file(self) -> None:
        self.git_init()
        self.settings(self.root, team="review.autonmy: yes\n", local="dir.default: ignored\n")
        res = self.run_loader(self.root)
        self.assertIn(
            "error: settings.md:1 unknown key `review.autonmy` — ignored",
            res.errors,
        )
        self.assertIn(
            "error: settings.local.md:1 team key `dir.default` in the personal file — ignored",
            res.errors,
        )
        self.assertEqual(res.line("dir.default"), "dir.default: unset  [default]")

    # 6. Inheritance.
    def test_inheritance(self) -> None:
        self.git_init()
        self.settings(self.root, team="dir.default: ignored\ndir.docs/plans: tracked\n")
        res = self.run_loader(self.root)
        self.assertEqual(res.line("dir.docs/plans"), "dir.docs/plans: tracked  [team]")
        self.assertEqual(res.line("dir.docs/specs"), "dir.docs/specs: ignored  [inherited]")
        self.assertEqual(res.line("dir..superpowers"), "dir..superpowers: ignored  [inherited]")

        self.settings(self.root, team="dir.default: bogus\n")
        res2 = self.run_loader(self.root)
        self.assertEqual(res2.line("dir.default"), "dir.default: unset  [invalid in team]")
        self.assertEqual(res2.line("dir.docs/specs"), "dir.docs/specs: unset  [inherited]")

        self.settings(self.root, team="dir.default: tracked\ndir.docs/specs: bogus\n")
        res3 = self.run_loader(self.root)
        self.assertEqual(res3.line("dir.docs/specs"), "dir.docs/specs: unset  [invalid in team]")

    # 7. Fences and commentary.
    def test_fences_and_commentary(self) -> None:
        self.git_init()
        team = (
            "# Team settings\n"
            "Note: dir.default: ignored\n"
            "  dir.default: ignored\n"
            "```\n"
            "dir.default: ignored\n"
            "```\n"
            "dir.default: tracked\n"
        )
        self.settings(self.root, team=team)
        res = self.run_loader(self.root)
        self.assertEqual(res.line("dir.default"), "dir.default: tracked  [team]")
        self.assertEqual(res.errors, [])

        team_no_last = (
            "# Team settings\n"
            "Note: dir.default: ignored\n"
            "  dir.default: ignored\n"
            "```\n"
            "dir.default: ignored\n"
            "```\n"
        )
        self.settings(self.root, team=team_no_last)
        res2 = self.run_loader(self.root)
        self.assertEqual(res2.line("dir.default"), "dir.default: unset  [default]")

    # 8. Whitespace.
    def test_whitespace(self) -> None:
        self.git_init()
        self.settings(self.root, team="dir.default:\ttracked \r\n")
        res = self.run_loader(self.root)
        self.assertEqual(res.line("dir.default"), "dir.default: tracked  [team]")

        self.settings(self.root, team="dir.default : tracked\n")
        res2 = self.run_loader(self.root)
        self.assertEqual(res2.line("dir.default"), "dir.default: unset  [default]")
        self.assertEqual(res2.errors, [])

        self.settings(self.root, team="dir.default:\n")
        res3 = self.run_loader(self.root)
        self.assertIn(
            "error: settings.md:1 invalid value for `dir.default`: (empty) — unset",
            res3.errors,
        )

    # 9. Absent files and the first line.
    def test_absent_files_and_first_line(self) -> None:
        self.git_init()
        self.settings(self.root, team="dir.default: tracked\n")
        res = self.run_loader(self.root)
        self.assertTrue(res.lines[0].endswith("team: settings.md; local: settings.local.md (absent))"))

        local_only_root = self.base / "proj-local-only"
        self.git_init(local_only_root)
        self.settings(local_only_root, local="review.autonomy: yes\n")
        res2 = self.run_loader(local_only_root)
        self.assertTrue(res2.lines[0].endswith("team: settings.md (absent); local: settings.local.md)"))

        # No .working-process/ at all.
        empty_root = self.base / "empty"
        empty_root.mkdir()
        self.git_init(empty_root)
        res3 = self.run_loader(empty_root)
        self.assertEqual(res3.out, "")
        self.assertEqual(res3.err, "")
        self.assertEqual(res3.code, 0)

        res4 = self.run_loader(empty_root, "--print")
        self.assertEqual(res4.lines,
                          [f"working-process settings (root: {empty_root}; loader: {LOADER}; no settings directory)"])
        self.assertEqual(res4.code, 0)

    # 10. Root resolution.
    def test_root_resolution(self) -> None:
        sub = self.root / "sub"
        sub.mkdir(parents=True)
        res = self.run_loader(sub, "--print", project_dir=str(self.root))
        self.assertTrue(res.lines[0].startswith(f"working-process settings (root: {self.root};"))
        self.assertEqual(res.err, "")

        res2 = self.run_loader(sub, "--print")
        self.assertTrue(res2.lines[0].startswith(f"working-process settings (root: {sub};"))
        self.assertEqual(res2.err, "")

        self.git_init()
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        res3 = self.run_loader(sub, "--print", project_dir=str(elsewhere))
        self.assertTrue(res3.lines[0].startswith(f"working-process settings (root: {self.root};"))

    # 11. An error of the loader's own.
    def test_loader_own_errors(self) -> None:
        alone = self.base / "alone" / "scripts" / "load-settings.sh"
        alone.parent.mkdir(parents=True)
        alone.write_bytes(LOADER.read_bytes())
        alone.chmod(0o755)
        self.settings(self.root)

        res = self.run_loader(self.root, loader=alone)
        self.assertEqual(res.out, "")
        self.assertEqual(res.err, "")
        self.assertEqual(res.code, 0)

        res2 = self.run_loader(self.root, "--print", loader=alone)
        self.assertEqual(res2.code, 1)
        self.assertEqual(res2.out, "")
        self.assertIn("registry not found or empty", res2.err)

        shim = self.base / "shim"
        shim.mkdir()
        awk_shim = shim / "awk"
        awk_shim.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        awk_shim.chmod(0o755)
        self.settings(self.root, team="dir.default: tracked\n")

        res3 = self.run_loader(self.root, path_prefix=shim)
        self.assertEqual(res3.out, "")
        self.assertEqual(res3.err, "")
        self.assertEqual(res3.code, 0)

        res4 = self.run_loader(self.root, "--print", path_prefix=shim)
        self.assertEqual(res4.code, 1)
        self.assertEqual(res4.out, "")
        self.assertIn("loader failed", res4.err)

    # 12. The cap.
    def test_cap_two_hundred_lines(self) -> None:
        self.git_init()
        team = "".join(f"zz.k{i}: x\n" for i in range(200))
        self.settings(self.root, team=team)

        res = self.run_loader(self.root)
        self.assertLessEqual(len(res.out.encode()), 4096)
        self.assertTrue(res.out.endswith("\n"))
        self.assertEqual(res.lines[-1], f"incomplete: run {LOADER} --print")
        self.assertEqual(res.lines[0], self.first_line(self.root, local="settings.local.md (absent)"))
        self.assertTrue(0 < len(res.errors) < 200)
        for e in res.errors:
            self.assertIn("unknown key `zz.k", e)

        printed = self.run_loader(self.root, "--print")
        self.assertEqual(len(printed.errors), 200)
        self.assertNotIn("incomplete:", printed.out)

    def test_cap_edge_exact_and_over(self) -> None:
        self.git_init()
        # Measure once with a short key.
        self.settings(self.root, team="zz.k: x\n")
        base = self.run_loader(self.root, "--print")
        base_len = len(base.out.encode())
        diff = 4096 - base_len
        self.assertGreaterEqual(diff, 0)
        pad_key = "zz." + ("k" * (1 + diff))
        self.settings(self.root, team=f"{pad_key}: x\n")
        exact = self.run_loader(self.root, "--print")
        self.assertEqual(len(exact.out.encode()), 4096)

        hook_exact = self.run_loader(self.root)
        self.assertEqual(hook_exact.out.encode(), exact.out.encode())
        self.assertNotIn("incomplete:", hook_exact.out)

        pad_key_over = "zz." + ("k" * (2 + diff))
        self.settings(self.root, team=f"{pad_key_over}: x\n")
        hook_over = self.run_loader(self.root)
        self.assertLessEqual(len(hook_over.out.encode()), 4096)
        self.assertEqual(hook_over.errors, [])
        self.assertTrue(hook_over.lines[-1].startswith("incomplete:"))

    # 13. Usage.
    def test_usage(self) -> None:
        self.git_init()
        res = self.run_loader(self.root, "--nonsense")
        self.assertEqual(res.code, 2)
        self.assertEqual(res.out, "")
        self.assertEqual(len(res.err.splitlines()), 1)
        self.assertTrue(res.err.startswith("usage:"))

        res2 = self.run_loader(self.root, "--print", "extra")
        self.assertEqual(res2.code, 2)


if __name__ == "__main__":
    unittest.main()
