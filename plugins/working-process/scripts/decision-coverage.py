#!/usr/bin/env python3
"""Derive decision coverage for a plan, or check a design spec's register.

Usage: decision-coverage.py <document>

The grammar this script reads is defined in the spec-plan-lifecycle rule,
under *Decision register* and *Plan annotations*; the steps and the
report shapes are duty 10 and `## Output` of the propagation-auditor
card. Where this script and those texts disagree, the texts govern.

Output goes to stdout: every hit, one line each, then one
`decision-coverage:` block per spec. Exit 0 whenever the derivation ran,
hits or not; 2 on a usage error; 1 when the argument or a document it
names cannot be read. A technical design — a document under a
`technical-designs` directory directly under a `docs` directory —
produces no output; this duty does not cover it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TOOL = "decision-coverage.py"

ENTRY_RE = re.compile(r"^(\s*)- \*\*(D\d+(?:\.\d+)?)\*\*")
NUMBERED_RE = re.compile(r"^\s*\d+\.\s+\*\*D")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")
ATTEMPTED_ID_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+\*\*D\d")
STEP_RE = re.compile(r"^\s*-\s\[.\]")
TOKEN_START_RE = re.compile(r"\.\s+(withdrawn\b.*)$")
TOKEN_RE = re.compile(
    r"^withdrawn (.+), ruling: (\d{4}-\d{2}-\d{2})"
    r"(?:; replaced by (D\d+(?:\.\d+)?))?\.?$"
)
TASK_RE = re.compile(r"^### Task (\d+)")
FIELD_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$")


class Unreadable(Exception):
    """Raised when a document, or one it names, cannot be read."""


# --- reading -------------------------------------------------------------

def read_lines(path: str) -> list[str]:
    """Read `path` and split it into lines, raising `Unreadable` on failure."""
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read().splitlines()
    except (OSError, UnicodeDecodeError) as error:
        raise Unreadable(f"cannot read {path}: {error.strerror or error}")


def frontmatter(lines: list[str]) -> tuple[dict[str, tuple[str, int]], int]:
    """Fields between the `---` on line 1 and the next `---`.

    Returns ({key: (value, line number)}, index of the first body line).
    """
    fields = {}
    if not lines or lines[0].strip() != "---":
        return fields, 0
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return fields, index + 1
        match = FIELD_RE.match(lines[index])
        if match:
            fields[match.group(1)] = (match.group(2), index + 1)
    return fields, len(lines)


def spec_paths(value: str) -> list[str]:
    """`spec:` as a single path or an inline list `[a, b]`."""
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [item.strip().strip("'\"") for item in value.split(",") if item.strip()]


def unfenced(lines: list[str], start: int) -> list[tuple[int, str]]:
    """(line number, text) pairs of the body, fenced code blocks removed."""
    kept, in_fence = [], False
    for index in range(start, len(lines)):
        text = lines[index]
        if text.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept.append((index + 1, text))
    return kept


def _collapse(path: Path) -> str:
    """Lexically fold `..` segments, mirroring `os.path.normpath`."""
    root = path.root
    kept: list[str] = []
    for part in path.parts:
        if part == root and part:
            continue
        if part == "..":
            if kept and kept[-1] != "..":
                kept.pop()
            elif not root:
                kept.append(part)
        else:
            kept.append(part)
    return (root + "/".join(kept)) if kept or root else "."


def _abspath(path: str) -> str:
    """Make `path` absolute against the current directory, lexically."""
    given = Path(path)
    return _collapse(given if given.is_absolute() else Path.cwd() / path)


def resolve(base_display: str, written: str) -> str:
    """A path a document names, resolved against that document's directory."""
    return _collapse(Path(base_display).parent / written)


def same_file(a: str, b: str) -> bool:
    """Whether `a` and `b` name the same file once made absolute."""
    return _abspath(a) == _abspath(b)


# --- the register --------------------------------------------------------

class Entry:
    """One register entry: an identifier, its line, and its nesting."""

    def __init__(self, ident: str, line: int, child: bool) -> None:
        self.ident = ident
        self.line = line
        self.child = child
        self.children = []
        self.token = None
        self.withdrawn = False
        self.replaced_by = None

    @property
    def group(self) -> bool:
        """Whether this entry is a group (has children)."""
        return bool(self.children)


class Register:
    """Outcome of steps 1 and 2 for one spec: legacy, malformed or counted."""

    def __init__(
        self,
        state: str,
        entries: dict[str, Entry] | None = None,
        hits: list[str] | None = None,
    ) -> None:
        self.state = state  # "legacy" | "malformed" | "ok"
        self.entries = entries or {}
        self.hits = hits or []

    def leaves(self) -> list[Entry]:
        """The register's leaf entries — those without children."""
        return [e for e in self.entries.values() if not e.group]


def hit(path: str, line: int, claim: str, step: str) -> str:
    """Format one derivation hit line."""
    return f"{path}:{line} — {claim} — derivation: {TOOL}, {step}"


def read_register(display: str, lines: list[str]) -> Register:
    fields, body_start = frontmatter(lines)
    if "decisions" not in fields:
        return Register("legacy")
    value, field_line = fields["decisions"]
    if value != "registered":
        return Register("malformed", hits=[hit(
            display, field_line,
            f"`decisions:` is `{value}`, not `registered`", "step 1")])

    body = unfenced(lines, body_start)
    start = next((i for i, (_, text) in enumerate(body)
                  if text.rstrip() == "## Decisions"), None)
    if start is None:
        return Register("malformed", hits=[hit(
            display, field_line,
            "`decisions: registered` but no `## Decisions` section", "step 2")])
    section = []
    for number, text in body[start + 1:]:
        if text.startswith("## "):
            break
        section.append((number, text))
    return parse_register(display, section)


def parse_register(display: str, section: list[tuple[int, str]]) -> Register:
    hits, entries, parent = [], {}, None

    def bad(line, claim):
        hits.append(hit(display, line, claim, "step 2"))

    for index, (number, text) in enumerate(section):
        if NUMBERED_RE.match(text):
            bad(number, "register entry written as a numbered list")
            continue
        match = ENTRY_RE.match(text)
        if not match:
            if LIST_ITEM_RE.match(text):
                indent = len(text) - len(text.lstrip())
                if indent == 0 or ATTEMPTED_ID_RE.match(text):
                    bad(number, "list item does not parse as a register entry")
            continue
        indent, ident = len(match.group(1)), match.group(2)
        child = indent >= 2
        paragraph = [text.strip()]
        for _, following in section[index + 1:]:
            if not following.strip() or LIST_ITEM_RE.match(following):
                break
            paragraph.append(following.strip())
        paragraph = " ".join(paragraph)

        if ident in entries:
            bad(number, f"duplicate identifier {ident}")
            continue
        entry = Entry(ident, number, child)
        if child:
            parent_id = ident.split(".")[0]
            if "." not in ident:
                bad(number, f"{ident} is nested but is not a child identifier")
                continue
            if parent_id not in entries:
                bad(number, f"child {ident} has no parent entry {parent_id}")
                continue
            if parent is None or parent.ident != parent_id:
                bad(number, f"child {ident} is not nested under {parent_id}")
                continue
            parent.children.append(entry)
        else:
            if "." in ident:
                bad(number, f"child {ident} is not nested under {ident.split('.')[0]}")
                continue
            parent = entry

        start = TOKEN_START_RE.search(paragraph)
        if start:
            token = start.group(1)
            parsed = TOKEN_RE.match(token)
            if not parsed:
                bad(number, f"{ident} carries a `withdrawn` segment that does not "
                            "match the state token's grammar")
            else:
                entry.token = token
                entry.withdrawn = True
                entry.replaced_by = parsed.group(3)
        entries[ident] = entry

    for entry in entries.values():
        if entry.group and entry.token:
            bad(entry.line, f"group {entry.ident} carries a state token")
        target = entry.replaced_by
        if target is None:
            continue
        if target == entry.ident:
            bad(entry.line, f"{entry.ident} is replaced by itself")
        elif target not in entries:
            bad(entry.line, f"{entry.ident} is replaced by {target}, which the register does not define")
        elif entries[target].group:
            bad(entry.line, f"{entry.ident} is replaced by group {target}")

    reported = set()
    for entry in entries.values():
        path, current = [], entry
        while current is not None and current.replaced_by in entries:
            if current.ident in path:
                cycle = path[path.index(current.ident):]
                key = frozenset(cycle)
                if len(cycle) > 1 and key not in reported:
                    reported.add(key)
                    first = min((entries[i] for i in cycle), key=lambda e: e.line)
                    bad(first.line, "`replaced by` chain closes a cycle: "
                                    + " → ".join(cycle + [cycle[0]]))
                break
            path.append(current.ident)
            current = entries[current.replaced_by]

    if hits:
        return Register("malformed", hits=hits)
    return Register("ok", entries=entries)


# --- the plan ------------------------------------------------------------

class Citation:
    """One `**Realizes:**`/Global-Constraints citation of a decision."""

    def __init__(self, token: str, line: int, site: str) -> None:
        self.token = token
        self.line = line
        self.site = site


class Plan:
    """A parsed plan document: its specs, citations, tasks, defers and follows."""

    def __init__(self, display: str, lines: list[str]) -> None:
        self.display = display
        fields, body_start = frontmatter(lines)
        self.fields = fields
        self.specs = spec_paths(fields["spec"][0]) if "spec" in fields else []
        self.status = fields.get("status", ("", 0))[0]
        self.citations = []   # Citation, in document order
        self.tasks = []       # (number, heading line, has a Realizes line, past first step)
        self.defers = []      # (line, token)
        self.follows = []     # (line, written path)
        self._parse(unfenced(lines, body_start))

    def _parse(self, body):
        section, task = None, None
        for index, (number, text) in enumerate(body):
            if text.startswith("#"):
                task = None
                match = TASK_RE.match(text)
                if match:
                    task = [match.group(1), number, False, False]
                    self.tasks.append(task)
                if text.startswith("## "):
                    section = text[3:].strip()
                continue
            if task is not None and STEP_RE.match(text):
                task[3] = True
                continue
            if task is not None and text.startswith("**Realizes:** "):
                if not task[3]:
                    task[2] = True
                    value = text[len("**Realizes:** "):].strip()
                    if value != "none":
                        for token in split_ids(value):
                            self.citations.append(Citation(token, number, f"Task {task[0]}"))
                continue
            if section == "Global Constraints" and text.startswith("- **Realizes:** "):
                rest = text[len("- **Realizes:** "):]
                ids, _, words = rest.partition(" — ")
                for following_number, following in body[index + 1:]:
                    if (not following.strip() or LIST_ITEM_RE.match(following)
                            or following.startswith("#")):
                        break
                    words += " " + following.strip()
                words = " ".join(words.replace("**", "").replace("`", "").split()[:6])
                site = f'Global Constraints, line {number}: "{words}"'
                for token in split_ids(ids):
                    self.citations.append(Citation(token, number, site))
                continue
            if section == "Deferrals and predecessors":
                if text.startswith("**Defers:** "):
                    token = text[len("**Defers:** "):].split(" — ")[0].strip()
                    self.defers.append((number, token))
                elif text.startswith("**Follows:** "):
                    self.follows.append((number, text[len("**Follows:** "):].strip()))


def split_ids(value: str) -> list[str]:
    """Split a comma-separated list of identifiers, dropping blanks."""
    return [item.strip() for item in value.split(",") if item.strip()]


def scoped(plan: Plan, token: str, spec_abs: str) -> str | None:
    """The identifier `token` names for the spec at spec_abs, or None.

    A plan naming one spec writes bare identifiers; one naming two or more
    qualifies each with the spec's path as its `spec:` writes it.
    """
    if len(plan.specs) >= 2:
        if "#" not in token:
            return None
        qualifier, ident = token.rsplit("#", 1)
        return ident if same_file(resolve(plan.display, qualifier), spec_abs) else None
    if len(plan.specs) == 1 and same_file(resolve(plan.display, plan.specs[0]), spec_abs):
        return token
    return None


# --- the derivation ------------------------------------------------------

class Audit:
    """Runs the coverage derivation for one plan, collecting hits and blocks."""

    def __init__(self, plan: Plan) -> None:
        self.plan = plan
        self.hits = []
        self.blocks = []
        self._predecessors = None

    def add(self, line: str) -> None:
        """Record a hit line, once per distinct line."""
        if line not in self.hits:
            self.hits.append(line)

    def predecessors(self) -> list[tuple[str, Plan, list[str]]]:
        """Step 3, once per plan: the accepted `**Follows:**` lines."""
        if self._predecessors is not None:
            return self._predecessors
        accepted = []
        own = [_abspath(resolve(self.plan.display, s)) for s in self.plan.specs]
        for line, written in self.plan.follows:
            display = resolve(self.plan.display, written)
            try:
                pred = Plan(display, read_lines(display))
            except Unreadable:
                self.add(hit(self.plan.display, line,
                             f"`**Follows:**` names {written}, which does not exist", "step 3"))
                continue
            theirs = [_abspath(resolve(display, s)) for s in pred.specs]
            shared = [s for s in own if s in theirs]
            if not shared:
                self.add(hit(self.plan.display, line,
                             f"`**Follows:**` names {written}, which shares no spec with this plan",
                             "step 3"))
                continue
            if pred.status != "implemented":
                self.add(hit(self.plan.display, line,
                             f"`**Follows:**` names {written}, which is at `status: "
                             f"{pred.status or '(none)'}`, not `implemented`", "step 3"))
                continue
            accepted.append((written, pred, shared))
        self._predecessors = accepted
        return accepted

    def check_spec(self, written: str) -> None:
        """Run steps 3 through 7 for one spec the plan names."""
        plan = self.plan
        spec_display = resolve(plan.display, written)
        spec_abs = _abspath(spec_display)
        register = read_register(spec_display, read_lines(spec_display))
        for line in register.hits:
            self.add(line)
        if register.state == "legacy":
            self.blocks.append(f"decision-coverage: {written} not checked — no decision register")
            return
        if register.state == "malformed":
            self.blocks.append(f"decision-coverage: {written} not counted — malformed register")
            return
        entries = register.entries
        multi = len(plan.specs) >= 2

        def show(ident):
            return f"{written}#{ident}" if multi else ident

        def problem(ident):
            if ident not in entries:
                return "which the register does not define"
            if entries[ident].group:
                return "which is a group"
            if entries[ident].withdrawn:
                return "which is withdrawn"
            return None

        # Step 3.
        predecessors = [(w, p) for w, p, shared in self.predecessors() if spec_abs in shared]

        # Step 4: local citations, then inherited ones.
        local, inherited, withdrawn_since = {}, {}, []
        for citation in plan.citations:
            ident = scoped(plan, citation.token, spec_abs)
            if ident is None:
                continue
            reason = problem(ident)
            if reason:
                self.add(hit(plan.display, citation.line,
                             f"cites {show(ident)}, {reason}", "step 4"))
            sites = local.setdefault(ident, [])
            if citation.site not in sites:
                sites.append(citation.site)
        for pred_written, pred in predecessors:
            for citation in pred.citations:
                ident = scoped(pred, citation.token, spec_abs)
                if ident is None:
                    continue
                site = f"{pred_written} ({citation.site})"
                if ident in entries and not entries[ident].group and entries[ident].withdrawn:
                    withdrawn_since.append((ident, site))
                    continue
                reason = problem(ident)
                if reason:
                    self.add(hit(pred.display, citation.line,
                                 f"inherited citation of {show(ident)}, {reason}", "step 4"))
                sites = inherited.setdefault(ident, [])
                if site not in sites:
                    sites.append(site)
        cited = set(local) | set(inherited)

        # Step 5.
        deferred = set()
        for line, token in plan.defers:
            ident = scoped(plan, token, spec_abs)
            if ident is None:
                continue
            reason = problem(ident)
            if reason is None and ident in cited:
                reason = "which this plan also cites"
            if reason:
                self.add(hit(plan.display, line, f"defers {show(ident)}, {reason}", "step 5"))
            else:
                deferred.add(ident)

        # Steps 6 and 7.
        order = list(entries)
        counted = [e.ident for e in register.leaves()
                   if not e.withdrawn and e.ident not in deferred]
        covered = [i for i in counted if i in cited]
        uncovered = [i for i in counted if i not in cited]
        only_inherited = [i for i in covered if i not in local]
        for ident in uncovered:
            self.add(hit(spec_display, entries[ident].line,
                         f"{show(ident)} is counted but no task or constraint cites it",
                         "step 7"))

        def slot(idents):
            return "[" + ", ".join(show(i) for i in idents) + "]"

        self.blocks.append(
            f"decision-coverage: {written} {len(covered)}/{len(counted)} covered; "
            f"inherited {slot(only_inherited)}; "
            f"deferred {slot([i for i in order if i in deferred])}; "
            f"uncovered {slot(uncovered)}")
        for ident in counted:
            sites = local.get(ident, []) + inherited.get(ident, [])
            self.blocks.append(f"  {show(ident)} → {', '.join(sites) if sites else '—'}")
        withdrawn_since.sort(key=lambda item: order.index(item[0]))
        for ident, site in withdrawn_since:
            self.blocks.append(f"  withdrawn since: {show(ident)} ← {site}")

    def plan_wide(self, registered: bool) -> None:
        """Step 7's plan-wide hits: missing annotations and bare identifiers."""
        plan = self.plan
        if registered:
            for number, heading_line, has_line, _ in plan.tasks:
                if not has_line:
                    self.add(hit(plan.display, heading_line,
                                 f"Task {number} carries no `**Realizes:**` line", "step 7"))
        if len(plan.specs) >= 2:
            tokens = [(c.line, c.token) for c in plan.citations] + plan.defers
            for line, token in sorted(tokens):
                if "#" not in token:
                    self.add(hit(plan.display, line,
                                 f"bare identifier {token} in a plan whose `spec:` names "
                                 f"{len(plan.specs)} specs", "step 7"))


def audit_plan(display: str, lines: list[str]) -> list[str]:
    """Run the derivation for a plan document, returning its output lines."""
    plan = Plan(display, lines)
    audit = Audit(plan)
    registered = False
    for written in plan.specs:
        spec_display = resolve(display, written)
        fields, _ = frontmatter(read_lines(spec_display))
        registered = registered or fields.get("decisions", ("", 0))[0] == "registered"
    for written in plan.specs:
        audit.check_spec(written)
    audit.plan_wide(registered)
    return audit.hits + audit.blocks


def audit_spec(display: str, lines: list[str]) -> list[str]:
    """Run the derivation for a spec audited alone, returning its output lines."""
    register = read_register(display, lines)
    outcome = {
        "legacy": "not checked — no decision register",
        "malformed": "not counted — malformed register",
        "ok": "register well formed",
    }[register.state]
    return register.hits + [f"decision-coverage: {display} {outcome}"]


def is_technical_design(display: str) -> bool:
    """The resolved path has `docs/technical-designs/` among its parents."""
    parts = Path(_abspath(display)).parts
    return any(a == "docs" and b == "technical-designs"
               for a, b in zip(parts, parts[1:]))


def main(argv: list[str]) -> int:
    """Parse argv, dispatch on document type, and print the derivation's output."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(argv) != 2:
        print("decision-coverage: usage: decision-coverage.py <plan or design spec>",
              file=sys.stderr)
        return 2
    display = argv[1]
    if is_technical_design(display):
        return 0
    try:
        lines = read_lines(display)
        fields, _ = frontmatter(lines)
        output = audit_plan(display, lines) if "spec" in fields else audit_spec(display, lines)
    except Unreadable as error:
        print(f"decision-coverage: {error}", file=sys.stderr)
        return 1
    for line in output:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
