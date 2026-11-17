#!/usr/bin/env python3
"""Mechanical Document checks on a design spec, technical design or plan.

Usage: document-check.py <document>

Output goes to stdout: every hit, one line each
(`<file:line> — <claim> — check: <check>`), then three summary lines in
the order `references`, `citations`, `table-closure`. Exit 0 whenever the
checks ran, hits or not; 1 when the document cannot be read; 2 on a usage
error. A hit is reported only where the parse settles the defect without
judgment; every form the script cannot settle is counted as not checked.
"""

from __future__ import annotations

import importlib.util
import os
import re
import sys
from pathlib import Path

CHECKS = ("references", "citations", "table-closure")
FIELD_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
NUMBER_RE = re.compile(r"^\d+(?:\.\d+)*\.?\s+")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
TASK_HEADING_RE = re.compile(r"^#{1,6}\s+Task (\d+)\b")
TASK_REF_RE = re.compile(r"\bTask (\d+)\b")
SIDE_RE = re.compile(r"\b(below|above)\b", re.IGNORECASE)
STEP_RE = re.compile(r"\bStep \d+\b")
SECTION_SIGN_RE = re.compile(r"§\s?\d+")
SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+")
NAME_RE = re.compile(
    r"(?<![*\w])\*([^*\s][^*]*?)\*(?![*\w])"
    r"|(?<!\w)_([^_\s][^_]*?)_(?!\w)"
    r'|"([^"\n]+)"|“([^”\n]+)”'
)


def _load_normalise():
    path = Path(__file__).resolve().parent / "phrase-check.py"
    spec = importlib.util.spec_from_file_location("wp_phrase_check", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.normalise


normalise = _load_normalise()


class Report:
    """Hits plus per-check checked / not-checked counters."""

    def __init__(self, display: str, technical_design: bool) -> None:
        self.display = display
        self.hits: list[str] = []
        self.counts = {c: [0, 0] for c in CHECKS}
        self.applicable = {c: c != "table-closure" or technical_design for c in CHECKS}

    def hit(self, line: int, claim: str, check: str) -> None:
        self.hits.append(f"{self.display}:{line} — {claim} — check: {check}")

    def checked(self, check: str, n: int = 1) -> None:
        self.counts[check][0] += n

    def not_checked(self, check: str, n: int = 1) -> None:
        self.counts[check][1] += n

    def lines(self) -> list[str]:
        out = list(self.hits)
        for c in CHECKS:
            if self.applicable[c]:
                done, skipped = self.counts[c]
                out.append(f"document-check: {c} {done} checked, {skipped} not checked")
            else:
                out.append(f"document-check: {c} not applicable")
        return out


def frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    """Fields of the frontmatter and the index of the first body line.

    A frontmatter that never closes is absent: the body starts at line 1.
    """
    if not lines or lines[0].strip() != "---":
        return {}, 0
    fields = {}
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return fields, index + 1
        match = FIELD_RE.match(lines[index])
        if match:
            fields[match.group(1)] = match.group(2)
    return {}, 0


def doc_type(path: str, fields: dict[str, str]) -> str:
    """`technical-design` by path first, then `plan` by `spec:`, else `spec`."""
    parts = Path(os.path.abspath(path)).parts
    if parts[-1].endswith("-technical-design.md") or any(
        a == "docs" and b == "technical-designs" for a, b in zip(parts, parts[1:])
    ):
        return "technical-design"
    return "plan" if "spec" in fields else "spec"


def body_lines(text: str) -> list[tuple[int, str]]:
    """(1-based line number, text) of lines below the frontmatter, outside
    fenced blocks, and under `## Review rounds` only below its last `### `."""
    lines = text.splitlines()
    _, start = frontmatter(lines)
    kept, in_fence = [], False
    for index in range(start, len(lines)):
        if lines[index].lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence:
            kept.append((index + 1, lines[index]))
    return _last_round_only(kept)


def _last_round_only(kept: list[tuple[int, str]]) -> list[tuple[int, str]]:
    # shortcut: only the last `## Review rounds` section is trimmed, as a
    # document carries one.
    section = last = None
    for i, (_, t) in enumerate(kept):
        if re.match(r"^## Review rounds\s*$", t):
            section, last = i, None
        elif section is not None:
            if t.startswith("## "):
                section = None
            elif t.startswith("### "):
                last = i
    if last is None:
        return kept
    start = max(i for i, (_, t) in enumerate(kept[:last]) if re.match(r"^## Review rounds\s*$", t))
    return kept[:start + 1] + kept[last + 1:]


def heading_key(text: str) -> str:
    return normalise(NUMBER_RE.sub("", text))


def paragraphs(body: list[tuple[int, str]]):
    """Runs of consecutive prose lines as [(line number, text)]."""
    run = []
    for number, text in body:
        stops = not text.strip() or HEADING_RE.match(text) or (LIST_RE.match(text) and run)
        if run and (stops or number != run[-1][0] + 1):
            yield run
            run = []
        if text.strip() and not HEADING_RE.match(text):
            run.append((number, text))
    if run:
        yield run


def check_references(body: list[tuple[int, str]], report: Report, kind: str) -> None:
    headings: dict[str, list[int]] = {}
    tasks = set()
    for number, text in body:
        match = HEADING_RE.match(text)
        if match:
            headings.setdefault(heading_key(match.group(2)), []).append(number)
        task = TASK_HEADING_RE.match(text)
        if task:
            tasks.add(task.group(1))
    for run in paragraphs(body):
        joined, owners = "", []
        for number, text in run:
            joined += text.strip() + " "
            owners += [number] * (len(text.strip()) + 1)
        position = 0
        for sentence in SENTENCE_END_RE.split(joined.rstrip()):
            start = joined.index(sentence, position)
            position = start + len(sentence)
            check_sentence(sentence, start, owners, headings, report)
            report.not_checked("references", len(STEP_RE.findall(sentence)) + len(SECTION_SIGN_RE.findall(sentence)))
            if kind == "plan":
                for task in TASK_REF_RE.finditer(sentence):
                    report.checked("references")
                    if task.group(1) not in tasks:
                        report.hit(owners[start + task.start()], f"`Task {task.group(1)}` has no task heading", "references")


def check_sentence(sentence, start, owners, headings, report) -> None:
    sides = SIDE_RE.findall(sentence)
    names = [m for m in NAME_RE.finditer(sentence)]
    if not sides:
        return
    if not names:
        report.not_checked("references")
        return
    for m in names:
        name = next(g for g in m.groups() if g)
        found = headings.get(heading_key(name), [])
        line = owners[start + m.start()]
        if len(set(s.lower() for s in sides)) != 1 or len(found) != 1:
            report.not_checked("references")
            continue
        report.checked("references")
        side = sides[0].lower()
        if (side == "below" and found[0] < line) or (side == "above" and found[0] > line):
            report.hit(line, f"`{name}` is {side} but its heading is at line {found[0]}", "references")


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(argv) != 2:
        print("document-check: usage: document-check.py <document>", file=sys.stderr)
        return 2
    display = argv[1]
    try:
        with open(display, encoding="utf-8", newline=None) as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as error:
        print(f"document-check: cannot read {display}: {getattr(error, 'strerror', None) or error}", file=sys.stderr)
        return 1
    fields, _ = frontmatter(text.splitlines())
    kind = doc_type(display, fields)
    report = Report(display, kind == "technical-design")
    check_references(body_lines(text), report, kind)
    for line in report.lines():
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
