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

    QUESTION = "May the review loop run autonomously, within the round cap?"

    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

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

    # 14. Fallback.
    def test_worktree_fallback(self) -> None:
        main = self.git_init()
        self.settings(main, team="dir.default: tracked\n", local="review.autonomy: yes\n")
        wt = self.worktree(main, "wt")
        self.settings(wt, team="dir.default: ignored\n")
        res = self.run_loader(wt)
        self.assertEqual(res.code, 0)
        self.assertEqual(res.err, "")
        self.assertEqual(res.line("review.autonomy"), "review.autonomy: yes  [local]")
        self.assertEqual(res.line("dir.default"), "dir.default: ignored  [team]")
        self.assertEqual(res.lines[0], self.first_line(wt, local="settings.local.md (main checkout)"))

    # 15. Fallback absent.
    def test_worktree_fallback_absent(self) -> None:
        main = self.git_init()
        self.settings(main, team="dir.default: tracked\n")
        wt = self.worktree(main, "wt")
        self.settings(wt, team="dir.default: ignored\n")
        res = self.run_loader(wt)
        self.assertEqual(res.lines[0],
                          self.first_line(wt, local="settings.local.md (main checkout, absent)"))
        self.assertEqual(res.line("review.autonomy"), "review.autonomy: unset  [default]")

    # 16. Shadow.
    def test_worktree_shadow(self) -> None:
        main = self.git_init()
        self.settings(main, team="dir.default: tracked\n", local="review.autonomy: yes\n")
        wt = self.worktree(main, "wt")
        self.settings(wt, team="dir.default: ignored\n", local="review.autonomy: no\n")
        res = self.run_loader(wt)
        self.assertEqual(res.line("review.autonomy"), "review.autonomy: no  [local]")
        self.assertEqual(res.lines[0],
                          self.first_line(wt, local="settings.local.md (worktree, shadows main checkout)"))
        self.assertNotIn("yes", res.out)

    # 17. Bare.
    def test_bare_repository(self) -> None:
        src = self.git_init()
        bwt = self.bare(src)
        self.settings(bwt, team="dir.default: tracked\n")
        res = self.run_loader(bwt)
        self.assertEqual(res.lines[0],
                          self.first_line(bwt, local="settings.local.md (worktree, bare repository, absent)"))

        self.settings(bwt, local="review.autonomy: yes\n")
        res2 = self.run_loader(bwt)
        self.assertEqual(res2.line("review.autonomy"), "review.autonomy: yes  [local]")
        self.assertEqual(res2.lines[0],
                          self.first_line(bwt, local="settings.local.md (worktree, bare repository)"))

    # 18. Worktree without a settings directory.
    def test_worktree_without_settings_directory(self) -> None:
        main = self.git_init()
        self.settings(main, team="dir.default: tracked\n", local="review.autonomy: yes\n")
        wt = self.worktree(main, "wt")
        res = self.run_loader(wt)
        self.assertEqual(res.code, 0)
        self.assertEqual(res.err, "")
        self.assertEqual(
            res.lines[0],
            self.first_line(wt, team="settings.md (absent)", local="settings.local.md (main checkout)"),
        )
        self.assertEqual(res.line("review.autonomy"), "review.autonomy: yes  [local]")
        self.assertEqual(res.line("dir.default"), "dir.default: unset  [default]")

        main2 = self.git_init(self.base / "main2")
        wt2 = self.worktree(main2, "wt2")
        res2 = self.run_loader(wt2)
        self.assertEqual(res2.out, "")
        self.assertEqual(res2.err, "")
        self.assertEqual(res2.code, 0)

        res3 = self.run_loader(wt2, "--print")
        self.assertEqual(
            res3.lines,
            [f"working-process settings (root: {wt2}; loader: {LOADER}; no settings directory)"],
        )
        self.assertEqual(res3.code, 0)

    def write_candidate(self, text: str) -> Path:
        """A standalone candidate file `t.md` outside any .working-process/."""
        path = self.base / "t.md"
        path.write_text(text, encoding="utf-8")
        return path

    # 19. A suggestion passes.
    def test_validate_suggestion_passes(self) -> None:
        candidate = self.write_candidate("consult.personas: yes\ndir.default: tracked\n")
        res = self.run_loader(self.base, "--validate", "--scope", "team", str(candidate))
        self.assertEqual(res.code, 0)
        self.assertEqual(
            res.out,
            "notice: t.md:1 personal key `consult.personas` in the team file — a suggestion\n"
            "t.md: 0 errors, 1 notices\n",
        )

    # 20. Each error kind fails.
    def test_validate_each_error_kind_fails(self) -> None:
        cases = [
            ("team", "dir.default: bogus\n",
             "error: t.md:1 invalid value for `dir.default`: bogus — unset"),
            ("team", "dir.default: tracked\ndir.default: ignored\n",
             "error: t.md:1,2 duplicate key `dir.default` — unset"),
            ("team", "review.autonmy: yes\n",
             "error: t.md:1 unknown key `review.autonmy` — ignored"),
            ("personal", "dir.default: tracked\n",
             "error: t.md:1 team key `dir.default` in the personal file — ignored"),
            ("team", "consult.personas: maybe\n",
             "error: t.md:1 invalid value for `consult.personas`: maybe — ignored"),
        ]
        for scope, text, expected_line in cases:
            with self.subTest(scope=scope, text=text):
                candidate = self.write_candidate(text)
                res = self.run_loader(self.base, "--validate", "--scope", scope, str(candidate))
                self.assertEqual(res.code, 1)
                self.assertIn(expected_line, res.lines)
                self.assertEqual(res.lines[-1], "t.md: 1 errors, 0 notices")
                if scope == "team" and text == "consult.personas: maybe\n":
                    self.assertEqual([l for l in res.lines if l.startswith("notice:")], [])

    # 21. Usage.
    def test_validate_usage(self) -> None:
        candidate = self.write_candidate("dir.default: tracked\n")
        missing = self.base / "missing.md"

        res = self.run_loader(self.base, "--validate", str(candidate))
        self.assertEqual(res.code, 2)
        self.assertEqual(res.out, "")
        self.assertTrue(res.err.startswith("usage:"))

        res2 = self.run_loader(self.base, "--validate", "--scope", "both", str(candidate))
        self.assertEqual(res2.code, 2)
        self.assertEqual(res2.out, "")
        self.assertTrue(res2.err.startswith("usage:"))

        res3 = self.run_loader(self.base, "--validate", "--scope", "team", str(missing))
        self.assertEqual(res3.code, 2)
        self.assertEqual(res3.out, "")
        self.assertTrue(res3.err.startswith("usage:"))

    # Regression: a candidate path shaped like an awk assignment
    # (ident=value) must still be read as a file, not treated as a
    # bare awk operand (which POSIX awk parses as a variable
    # assignment, falling through to read stdin instead of the named
    # file). Before the fix this printed a false-clean
    # "0 errors, 0 notices" / exit 0 here, since scan_file's awk
    # silently read the test's empty stdin instead of the real file.
    def test_validate_operand_shaped_filename_is_read_not_assigned(self) -> None:
        candidate = self.base / "x=y.md"
        candidate.write_text("dir.default: bogus\n", encoding="utf-8")
        # A bare relative name reproduces the ambiguity: awk's operand
        # grammar treats "ident=value" as an assignment only when the
        # whole operand matches it from the start, which an absolute
        # or slash-containing path never does. cwd=self.base with the
        # bare "x=y.md" argument is the shape that actually reaches
        # awk unresolved.
        res = self.run_loader(self.base, "--validate", "--scope", "team", "x=y.md")
        self.assertEqual(res.code, 1)
        self.assertIn(
            "error: x=y.md:1 invalid value for `dir.default`: bogus — unset",
            res.lines,
        )
        self.assertEqual(res.lines[-1], "x=y.md: 1 errors, 0 notices")

    # 22. Insert, personal, creating everything.
    def test_set_insert_personal_creates_everything(self) -> None:
        self.git_init()
        res = self.run_loader(self.root, "--set", "review.autonomy", "yes")
        self.assertEqual(res.code, 0)
        self.assertEqual(res.err, "")
        d = self.root / ".working-process"
        self.assertEqual(
            self.read(d / "settings.local.md"),
            f"# working-process settings — personal\n\n{self.QUESTION}\nreview.autonomy: yes\n",
        )
        self.assertEqual(self.read(d / ".gitignore"), "settings.local.md\n")
        self.assertFalse((d / "settings.md").exists())
        self.assertEqual(
            res.lines[:3],
            [
                "wrote settings.local.md: review.autonomy: yes (inserted)",
                "created .working-process/settings.local.md",
                "created .working-process/.gitignore — commit it with settings.md",
            ],
        )
        self.assertEqual(res.lines[3], "")
        self.assertEqual(res.lines[4], self.first_line(self.root, team="settings.md (absent)"))
        self.assertIn("review.autonomy: yes  [local]", res.lines)

    # 23. Insert, team.
    def test_set_insert_team(self) -> None:
        self.git_init()
        res = self.run_loader(self.root, "--set", "dir.default", "tracked")
        self.assertEqual(res.code, 0)
        d = self.root / ".working-process"
        question = ("Which mode does a Process directory get unless an exception "
                    "names it — tracked or ignored?")
        self.assertEqual(
            self.read(d / "settings.md"),
            f"# working-process settings\n\n{question}\ndir.default: tracked\n",
        )
        self.assertFalse((d / ".gitignore").exists())
        self.assertIn("wrote settings.md: dir.default: tracked (inserted)", res.lines)
        self.assertIn("created .working-process/settings.md", res.lines)

    # 24. Insert into an existing file.
    def test_set_insert_into_existing_file(self) -> None:
        original = "# Team\n\ndir.default: tracked\n"
        question = ("How does the topic branch take the .docs branch at the "
                    "implementation-ready gate — squash or fast-forward?")
        expected = original + f"\n{question}\ndocs-branch.merge: squash\n"

        self.git_init()
        self.settings(self.root, team=original)
        res = self.run_loader(self.root, "--set", "docs-branch.merge", "squash")
        self.assertEqual(res.code, 0)
        self.assertEqual(self.read(self.root / ".working-process" / "settings.md"), expected)

        root2 = self.git_init(self.base / "proj2")
        d2 = root2 / ".working-process"
        d2.mkdir(parents=True, exist_ok=True)
        (d2 / "settings.md").write_bytes(original[:-1].encode("utf-8"))
        res2 = self.run_loader(root2, "--set", "docs-branch.merge", "squash")
        self.assertEqual(res2.code, 0)
        self.assertEqual((d2 / "settings.md").read_bytes(), expected.encode("utf-8"))

    # 25. Replace.
    def test_set_replace(self) -> None:
        self.git_init()
        text = f"intro\n\n{self.QUESTION}\nreview.autonomy: yes\n\nconsult.personas: no\n"
        self.settings(self.root, local=text)
        local = self.root / ".working-process" / "settings.local.md"
        res = self.run_loader(self.root, "--set", "review.autonomy", "no")
        self.assertEqual(res.code, 0)
        expected = text.replace("review.autonomy: yes", "review.autonomy: no")
        self.assertEqual(self.read(local), expected)
        self.assertIn("wrote settings.local.md: review.autonomy: no (replaced)", res.lines)

        root2 = self.git_init(self.base / "proj-crlf")
        d2 = self.settings(root2)
        (d2 / "settings.local.md").write_bytes(
            b"intro\r\nreview.autonomy: yes\r\nconsult.personas: no\r\n")
        res2 = self.run_loader(root2, "--set", "review.autonomy", "no")
        self.assertEqual(res2.code, 0)
        self.assertEqual(
            (d2 / "settings.local.md").read_bytes(),
            b"intro\r\nreview.autonomy: no\nconsult.personas: no\r\n",
        )

    # 26. Unchanged.
    def test_set_unchanged(self) -> None:
        self.git_init()
        text = f"intro\n\n{self.QUESTION}\nreview.autonomy: yes\n\nconsult.personas: no\n"
        self.settings(self.root, local=text)
        before = tree_hash(self.root / ".working-process")
        res = self.run_loader(self.root, "--set", "review.autonomy", "yes")
        self.assertEqual(res.code, 0)
        after = tree_hash(self.root / ".working-process")
        self.assertEqual(before, after)
        self.assertIn("unchanged settings.local.md: review.autonomy: yes", res.lines)
        self.assertTrue(any(l.startswith("working-process settings (root:") for l in res.lines))

        root2 = self.git_init(self.base / "proj-crlf2")
        d2 = self.settings(root2)
        (d2 / "settings.local.md").write_bytes(b"review.autonomy: yes\r\n")
        before2 = tree_hash(d2)
        res2 = self.run_loader(root2, "--set", "review.autonomy", "yes")
        self.assertEqual(res2.code, 0)
        after2 = tree_hash(d2)
        self.assertEqual(before2, after2)
        self.assertIn("unchanged settings.local.md: review.autonomy: yes", res2.lines)

    # 27. Duplicate.
    def test_set_duplicate(self) -> None:
        self.git_init()
        text = (f"{self.QUESTION}\nreview.autonomy: yes\nfoo\n"
                f"{self.QUESTION}\nreview.autonomy: no\nbar\nreview.autonomy: maybe\n")
        self.settings(self.root, local=text)
        local = self.root / ".working-process" / "settings.local.md"
        res = self.run_loader(self.root, "--set", "review.autonomy", "no")
        self.assertEqual(res.code, 0)
        self.assertEqual(self.read(local), f"{self.QUESTION}\nreview.autonomy: no\nfoo\nbar\n")
        self.assertEqual(
            [l for l in res.lines if l.startswith("removed ") or l.startswith("wrote ")],
            [
                f"removed settings.local.md:4 {self.QUESTION}",
                "removed settings.local.md:5 review.autonomy: no",
                "removed settings.local.md:7 review.autonomy: maybe",
                "wrote settings.local.md: review.autonomy: no (replaced)",
            ],
        )

    # 28. Another line's error is reported, not blocking (D49).
    def test_set_other_line_error_not_blocking(self) -> None:
        self.git_init()
        self.settings(self.root, local="review.autonmy: yes\n")
        local = self.root / ".working-process" / "settings.local.md"
        res = self.run_loader(self.root, "--set", "review.autonomy", "no")
        self.assertEqual(res.code, 0)
        self.assertEqual(
            self.read(local),
            f"review.autonmy: yes\n\n{self.QUESTION}\nreview.autonomy: no\n",
        )
        err_idx = res.lines.index("error: settings.local.md:1 unknown key `review.autonmy` — ignored")
        wrote_idx = res.lines.index("wrote settings.local.md: review.autonomy: no (inserted)")
        self.assertLess(err_idx, wrote_idx)

    # 29. Validation.
    def test_set_validation(self) -> None:
        self.git_init()
        res = self.run_loader(self.root, "--set", "review.autonomy", "maybe")
        self.assertEqual(res.code, 1)
        self.assertEqual(res.out, "")
        self.assertEqual(res.err, "error: invalid value for `review.autonomy`: maybe (allowed: yes | no)\n")
        self.assertFalse((self.root / ".working-process").exists())

        res2 = self.run_loader(self.root, "--set", "nosuch.key", "yes")
        self.assertEqual(res2.code, 1)
        self.assertEqual(res2.err, "error: unknown key `nosuch.key`\n")

        res3 = self.run_loader(self.root, "--set", "review.autonomy")
        self.assertEqual(res3.code, 2)

    # 30. Destination from a worktree.
    def test_set_destination_from_worktree(self) -> None:
        main = self.git_init()
        wt = self.worktree(main, "wt")
        res = self.run_loader(wt, "--set", "review.autonomy", "yes")
        self.assertEqual(res.code, 0)
        main_d = main / ".working-process"
        self.assertEqual(
            self.read(main_d / "settings.local.md"),
            f"# working-process settings — personal\n\n{self.QUESTION}\nreview.autonomy: yes\n",
        )
        self.assertEqual(self.read(main_d / ".gitignore"), "settings.local.md\n")
        self.assertFalse((wt / ".working-process").exists())
        self.assertIn(
            "wrote settings.local.md (main checkout): review.autonomy: yes (inserted)",
            res.lines,
        )
        self.assertIn("review.autonomy: yes  [local]", res.lines)
        self.assertEqual(
            res.lines[res.lines.index("") + 1],
            self.first_line(wt, team="settings.md (absent)", local="settings.local.md (main checkout)"),
        )

        res2 = self.run_loader(wt, "--set", "dir.default", "tracked")
        self.assertEqual(res2.code, 0)
        self.assertTrue((wt / ".working-process" / "settings.md").exists())
        self.assertFalse((main / ".working-process" / "settings.md").exists())
        self.assertEqual(
            res2.lines[res2.lines.index("") + 1],
            self.first_line(wt, local="settings.local.md (main checkout)"),
        )
        self.assertIn("dir.default: tracked  [team]", res2.lines)

    # 31. Shadow.
    def test_set_shadow(self) -> None:
        main = self.git_init()
        wt = self.worktree(main, "wt")
        self.settings(wt, local="review.autonomy: no\n")
        res = self.run_loader(wt, "--set", "review.autonomy", "yes")
        self.assertEqual(res.code, 0)
        self.assertEqual(
            self.read(main / ".working-process" / "settings.local.md"),
            f"# working-process settings — personal\n\n{self.QUESTION}\nreview.autonomy: yes\n",
        )
        self.assertEqual(self.read(wt / ".working-process" / "settings.local.md"), "review.autonomy: no\n")
        self.assertEqual(
            res.lines[0],
            "note: settings.local.md in this worktree shadows the main checkout; "
            "this write will not change the current worktree's answer",
        )
        self.assertIn("review.autonomy: no  [local]", res.lines)

    # 32. Bare.
    def test_set_bare(self) -> None:
        src = self.git_init()
        bwt = self.bare(src)
        bare_git = src.parent / "bare.git"
        before = tree_hash(bare_git)
        res = self.run_loader(bwt, "--set", "review.autonomy", "yes")
        self.assertEqual(res.code, 0)
        self.assertTrue((bwt / ".working-process" / "settings.local.md").exists())
        self.assertTrue((bwt / ".working-process" / ".gitignore").exists())
        self.assertEqual(tree_hash(bare_git), before)
        self.assertIn(
            "wrote settings.local.md (worktree, bare repository): review.autonomy: yes (inserted)",
            res.lines,
        )

    # 33. Dry run.
    def test_set_dry_run(self) -> None:
        # Case 22: insert, personal, creating everything.
        self.git_init()
        base_hash = tree_hash(self.base)
        res = self.run_loader(self.root, "--set", "--dry-run", "review.autonomy", "yes")
        self.assertEqual(res.code, 0)
        self.assertEqual(tree_hash(self.base), base_hash)
        self.assertFalse((self.root / ".working-process").exists())
        self.assertFalse(any(l.startswith("working-process settings") for l in res.lines))
        self.assertIn("would write settings.local.md: review.autonomy: yes (inserted)", res.lines)
        self.assertIn("would create .working-process/settings.local.md", res.lines)
        self.assertIn(
            "would create .working-process/.gitignore — commit it with settings.md",
            res.lines,
        )

        # Case 25: replace.
        root25 = self.git_init(self.base / "proj25")
        text25 = f"intro\n\n{self.QUESTION}\nreview.autonomy: yes\n\nconsult.personas: no\n"
        self.settings(root25, local=text25)
        hash25 = tree_hash(root25 / ".working-process")
        res25 = self.run_loader(root25, "--set", "--dry-run", "review.autonomy", "no")
        self.assertEqual(res25.code, 0)
        self.assertEqual(tree_hash(root25 / ".working-process"), hash25)
        self.assertIn("would write settings.local.md: review.autonomy: no (replaced)", res25.lines)

        # Case 27: duplicate.
        root27 = self.git_init(self.base / "proj27")
        text27 = (f"{self.QUESTION}\nreview.autonomy: yes\nfoo\n"
                  f"{self.QUESTION}\nreview.autonomy: no\nbar\nreview.autonomy: maybe\n")
        self.settings(root27, local=text27)
        hash27 = tree_hash(root27 / ".working-process")
        res27 = self.run_loader(root27, "--set", "--dry-run", "review.autonomy", "no")
        self.assertEqual(res27.code, 0)
        self.assertEqual(tree_hash(root27 / ".working-process"), hash27)
        self.assertIn(f"would remove settings.local.md:4 {self.QUESTION}", res27.lines)
        self.assertIn("would remove settings.local.md:5 review.autonomy: no", res27.lines)
        self.assertIn("would remove settings.local.md:7 review.autonomy: maybe", res27.lines)
        self.assertIn("would write settings.local.md: review.autonomy: no (replaced)", res27.lines)

        # Case 30: destination from a worktree.
        main30 = self.git_init(self.base / "proj30")
        wt30 = self.worktree(main30, "wt30")
        base30_hash = tree_hash(self.base / "proj30")
        res30 = self.run_loader(wt30, "--set", "--dry-run", "review.autonomy", "yes")
        self.assertEqual(res30.code, 0)
        self.assertFalse((main30 / ".working-process").exists())
        self.assertFalse((wt30 / ".working-process").exists())
        self.assertIn(
            "would write settings.local.md (main checkout): review.autonomy: yes (inserted)",
            res30.lines,
        )
        self.assertIn(
            "would create .working-process/.gitignore — commit it with settings.md",
            res30.lines,
        )

        # Case 31: shadow.
        main31 = self.git_init(self.base / "proj31")
        wt31 = self.worktree(main31, "wt31")
        self.settings(wt31, local="review.autonomy: no\n")
        res31 = self.run_loader(wt31, "--set", "--dry-run", "review.autonomy", "yes")
        self.assertEqual(res31.code, 0)
        self.assertFalse((main31 / ".working-process").exists())
        self.assertEqual(
            res31.lines[0],
            "note: settings.local.md in this worktree shadows the main checkout; "
            "this write will not change the current worktree's answer",
        )

    # 34. An existing .gitignore without the line.
    def test_set_gitignore_appended(self) -> None:
        self.git_init()
        self.settings(self.root, gitignore="*.bak\n")
        res = self.run_loader(self.root, "--set", "review.autonomy", "yes")
        self.assertEqual(res.code, 0)
        self.assertEqual(
            self.read(self.root / ".working-process" / ".gitignore"),
            "*.bak\nsettings.local.md\n",
        )
        self.assertIn("appended settings.local.md to .working-process/.gitignore", res.lines)


if __name__ == "__main__":
    unittest.main()
