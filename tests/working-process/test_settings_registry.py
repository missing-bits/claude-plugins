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


if __name__ == "__main__":
    unittest.main()
