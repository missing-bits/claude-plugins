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
import subprocess
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
# A step's own label (`**Step 1: ...`, `Step 1:`) is no reference.
STEP_RE = re.compile(r"(?<!\*\*)\bStep \d+\b(?!:)")
SECTION_SIGN_RE = re.compile(r"§\s?\d+")
SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+")
NAME_RE = re.compile(
    r"(?<![*\w])\*([^*\s][^*]*?)\*(?![*\w])"
    r"|(?<!\w)_([^_\s][^_]*?)_(?!\w)"
    r'|"([^"\n]+)"|“([^”\n]+)”'
)
PATH_TOKEN = r"(?:\.{1,2}/)*\w[\w./-]*\.\w+"
CITE_RE = re.compile(rf"(?<![\w/:.-])({PATH_TOKEN}):(\d+)(?:-(\d+))?(?!\w)")
SYMBOL_CITE_RE = re.compile(rf"`([^`]+)`\s*\(`?({PATH_TOKEN}):(\d+)`?\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
BACKTICK_RE = re.compile(r"`([^`\s]+)`")
CREATE_RE = re.compile(r"^\s*[-*]\s*Create:\s*`([^`]+)`")
CLAUSE_RE = re.compile(r"\b(?:license|ruling):\s*(?:\"([^\"]+)\"|“([^”]+)”)")
LOCATION_RE = re.compile(
    rf"(?<![\w/:.-])(?P<path>{PATH_TOKEN})(?::(?P<line>\d+))?(?!\w)|\*(?P<head>[^*\n]+)\*"
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
        self.relations = 0

    def hit(self, line: int, claim: str, check: str) -> None:
        self.hits.append(f"{self.display}:{line} — {claim} — check: {check}")

    def checked(self, check: str, n: int = 1) -> None:
        self.counts[check][0] += n

    def not_checked(self, check: str, n: int = 1) -> None:
        self.counts[check][1] += n

    def lines(self) -> list[str]:
        out = list(self.hits)
        for c in CHECKS:
            if c == "table-closure" and self.applicable[c]:
                done, skipped = self.counts[c]
                out.append(
                    f"document-check: {c} {self.relations} relations, {done} names checked, {skipped} not checked"
                )
            elif self.applicable[c]:
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


AFTER_RE = re.compile(r"\s*(?:[\w-]+\s+){0,2}(below|above)\b", re.IGNORECASE)
BEFORE_RE = re.compile(r"\b(below|above)[,:]?\s*$", re.IGNORECASE)


def check_sentence(sentence, start, owners, headings, report) -> None:
    if not SIDE_RE.search(sentence):
        return
    names = list(NAME_RE.finditer(sentence))
    if not names:
        report.not_checked("references")
        return
    for m in names:
        # A name is a reference only beside a side word: it closes
        # `<= 2 words + below|above`, or `below|above[,:]` opens it.
        after = AFTER_RE.match(sentence, m.end())
        before = BEFORE_RE.search(sentence[: m.start()])
        if not (after or before):
            continue
        name = next(g for g in m.groups() if g)
        found = headings.get(heading_key(name), [])
        line = owners[start + m.start()]
        if len(found) != 1:
            report.not_checked("references")
            continue
        report.checked("references")
        side = (after or before).group(1).lower()
        if (side == "below" and found[0] < line) or (side == "above" and found[0] > line):
            report.hit(line, f"`{name}` is {side} but its heading is at line {found[0]}", "references")


def repo_root(path: str) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], cwd=os.path.dirname(os.path.abspath(path)),
            capture_output=True, text=True,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except OSError:
        pass
    return os.getcwd()


def created_paths(lines: list[tuple[int, str]]) -> set[str]:
    return {os.path.normpath(m.group(1)) for _, t in lines if (m := CREATE_RE.match(t))}


class Resolver:
    """Paths resolve against the document's directory, then the repository root."""

    def __init__(self, path: str, root: str, created: set[str]) -> None:
        self.bases = [os.path.dirname(os.path.abspath(path)), root]
        self.created = created
        self.cache: dict[str, list[str] | None] = {}

    def file(self, rel: str, kind=os.path.isfile) -> str | None:
        for base in self.bases:
            full = os.path.normpath(os.path.join(base, rel))
            if kind(full):
                return full
        return None

    def lines(self, full: str) -> list[str]:
        if full not in self.cache:
            with open(full, encoding="utf-8", errors="replace") as handle:
                self.cache[full] = handle.read().splitlines()
        return self.cache[full]

    def missing_is_defect(self, rel: str) -> bool:
        """D9: a directory-named path whose directory exists and no Create: line makes."""
        if "/" not in rel.removeprefix("./"):
            return False
        norm = os.path.normpath(rel)
        root = self.bases[1]
        made = any(os.path.normpath(os.path.join(root, c)) == os.path.normpath(os.path.join(b, norm))
                   for b in self.bases for c in self.created)
        parent = os.path.dirname(rel)
        return not made and any(os.path.isdir(os.path.join(b, parent)) for b in self.bases)


def check_citations(
    path: str, lines: list[tuple[int, str]], report: Report, root: str, created: set[str]
) -> None:
    res = Resolver(path, root, created)
    owner_lines = [(n, t) for n, t in lines if not CREATE_RE.match(t)]
    for number, text in owner_lines:
        symbols = {m.start(2): m.group(1) for m in SYMBOL_CITE_RE.finditer(text)}
        for m in CITE_RE.finditer(text):
            rel, first = m.group(1), int(m.group(2))
            last = int(m.group(3)) if m.group(3) else first
            if "/" not in rel.removeprefix("./"):  # D9: a bare file name is skipped whole
                report.not_checked("citations")
                continue
            full = res.file(rel)
            if full is None:
                if res.missing_is_defect(rel):
                    report.checked("citations")
                    report.hit(number, f"`{rel}` does not exist", "citations")
                else:
                    report.not_checked("citations")
                continue
            report.checked("citations")
            body = res.lines(full)
            if first < 1 or last > len(body) or last < first:
                report.hit(number, f"`{m.group(0)}` lies outside `{rel}` ({len(body)} lines)", "citations")
                continue
            symbol = symbols.get(m.start(1))
            if symbol and not m.group(3) and symbol not in body[first - 1]:
                report.hit(number, f"`{symbol}` is not on `{rel}` line {first}", "citations")
        for m in LINK_RE.finditer(INLINE_CODE_RE.sub("", text)):
            target = m.group(1)
            if re.match(r"^[A-Za-z][\w+.-]*:|^#", target) or "#" in target:
                report.not_checked("citations")
            elif res.file(target, os.path.exists):
                report.checked("citations")
            elif res.missing_is_defect(target):
                report.checked("citations")
                report.hit(number, f"link target `{target}` does not exist", "citations")
            else:
                report.not_checked("citations")
        for m in BACKTICK_RE.finditer(text):
            token = m.group(1)
            if "/" in token and ":" not in token and re.fullmatch(r"[\w./-]+", token):
                if res.file(token):
                    report.checked("citations")
                else:
                    report.not_checked("citations")
    check_quotes(lines, report, res)


def check_quotes(lines, report, res) -> None:
    for run in paragraphs(lines):
        joined, owners = "", []
        for number, text in run:
            joined += text.strip() + " "
            owners += [number] * (len(text.strip()) + 1)
        for clause in CLAUSE_RE.finditer(joined):
            quote = normalise(clause.group(1) or clause.group(2))
            following = CLAUSE_RE.search(joined, clause.end())
            where = locate(joined[clause.end():following.start() if following else None], lines, res)
            number = owners[clause.start()]
            if where is None:
                report.not_checked("citations")
                continue
            report.checked("citations")
            if quote not in normalise(" ".join(where)):
                report.hit(number, f"quote \"{clause.group(1) or clause.group(2)}\" is not at its cited location", "citations")


def locate(rest, lines, res):
    """Lines the first location after a quote names, or None when it settles none."""
    for m in LOCATION_RE.finditer(rest):
        if m.group("head"):
            return section(lines, m.group("head"))
        if "/" not in m.group("path").removeprefix("./"):
            continue
        full = res.file(m.group("path"))
        if full is None:
            return None
        body = res.lines(full)
        if m.group("line"):
            first = int(m.group("line"))
            return body[first - 1:first + 2] or None
        return body
    return None


def section(lines, name):
    key = heading_key(name)
    for i, (_, t) in enumerate(lines):
        m = HEADING_RE.match(t)
        if m and heading_key(m.group(2)) == key:
            level, out = len(m.group(1)), []
            for _, u in lines[i + 1:]:
                n = HEADING_RE.match(u)
                if n and len(n.group(1)) <= level:
                    break
                out.append(u)
            return out
    return None


def declared_relations(rule_path: str) -> list[tuple[str, str, bool, str, str]]:
    """(table, column, each_side, target table, target column) rows of the rule's
    `## Declared table relations` table."""
    with open(rule_path, encoding="utf-8") as handle:
        lines = list(enumerate(handle.read().splitlines(), 1))
    rows = _table_rows(lines, "Declared table relations")
    out = []
    for _, cells in rows[1:]:
        left = re.fullmatch(r"(\w+) `([^`]+)`(, each side)?", cells[0]) if len(cells) > 1 else None
        right = re.fullmatch(r"(\w+) `([^`]+)`", cells[1]) if len(cells) > 1 else None
        if left and right:
            out.append((left.group(1), left.group(2), bool(left.group(3)), right.group(1), right.group(2)))
    return out


def _cells(text: str) -> list[str]:
    return [c.strip() for c in text.strip().strip("|").replace("\\|", "\0").split("|")]


def _table_rows(lines: list[tuple[int, str]], section_name: str) -> list[tuple[int, list[str]]]:
    """(line, cells), header row first, separator dropped, of the first table under the heading."""
    key = heading_key(section_name)
    rows, inside = [], False
    for number, text in lines:
        m = HEADING_RE.match(text)
        if m:
            if inside:
                break
            inside = heading_key(m.group(2)) == key
        elif inside and text.lstrip().startswith("|"):
            if not re.fullmatch(r"[\s|:-]+", text):
                rows.append((number, [c.replace("\0", "|") for c in _cells(text)]))
        elif inside and rows:
            break
    return rows


def _clean(cell: str) -> str:
    return normalise(cell.replace("`", ""))


def check_tables(
    path: str, lines: list[tuple[int, str]], report: Report,
    relations: list[tuple[str, str, bool, str, str]],
) -> None:
    for table, column, each_side, target, target_column in relations:
        rows, goal = _table_rows(lines, table), _table_rows(lines, target)
        if not rows or not goal:
            continue
        col = next((i for i, h in enumerate(rows[0][1]) if _clean(h) == _clean(column)), None)
        tcol = next((i for i, h in enumerate(goal[0][1]) if _clean(h) == _clean(target_column)), None)
        if col is None or tcol is None:
            continue
        report.relations += 1
        names = [_clean(r[tcol]) for _, r in goal[1:] if len(r) > tcol]
        for line, row in rows[1:]:
            if len(row) <= col:
                continue
            raw = re.sub(r"\([^)]*\)", "", row[col])
            if each_side:
                sides = raw.split("→")
                if len(sides) != 2:
                    report.not_checked("table-closure")
                    continue
            else:
                sides = [raw]
            for side in sides:
                segments = [s.strip() for s in re.split(r"[,;]", side) if s.strip() not in ("", "—", "-", "–")]
                if not segments:
                    report.checked("table-closure")
                    report.hit(line, f"`{column}` cell `{row[col]}` has an empty side", "table-closure")
                for seg in segments:
                    if seg.lower().startswith("external:"):
                        continue
                    found = names.count(_clean(seg))
                    if found == 0:
                        report.not_checked("table-closure")
                    else:
                        report.checked("table-closure")
                        if found > 1:
                            report.hit(line, f"`{seg}` names {found} rows of {target}", "table-closure")


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
    body = body_lines(text)
    check_references(body, report, kind)
    check_citations(display, body, report, repo_root(display), created_paths(body) if kind == "plan" else set())
    if kind == "technical-design":
        rule = Path(__file__).resolve().parent.parent / "rules" / "technical-design.md"
        check_tables(display, body, report, declared_relations(str(rule)))
    for line in report.lines():
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
