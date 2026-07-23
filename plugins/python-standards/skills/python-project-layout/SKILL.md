---
name: python-project-layout
description: Use when creating a Python project or restructuring one — uv-managed environments and dependencies, pyproject.toml, src layout, entry points, package versioning, module boundaries and dependency direction, and when to split code. Line-level style belongs to python-code-style; in-service layer architecture (router/service/repository) to python-web-api.
---

# Python project layout

Project-level standards. Cite rules in review findings as
`(standard: python-project-layout, rule: <id>)`. Each rule names its
source: a PEP, an official doc, or `this standard` (a recorded house
decision).

## uv owns the project

uv manages environments, dependencies, and packaging — end to end:

- `uv init` scaffolds; `uv add` / `uv remove` edit dependencies (never
  edit the dependency list by hand and `pip install` never appears);
- `uv lock` / `uv sync` maintain the environment; **`uv.lock` is
  committed** — reproducibility is the point;
- `uv run <cmd>` executes inside the project environment — no manual
  venv activation in docs or scripts.

(id: `layout-uv-owns`; severity: minor; source: uv documentation —
projects and lockfile concepts)

Sub-rules:
- `uv.lock` not committed (id: `layout-uv-owns.uncommitted-lock`;
  severity: important)

## Tool ownership — mise and uv

mise pins developer tools on the machine — including uv itself — while uv
owns the project's Python interpreter and virtual environment
(`requires-python`, `uv python pin`, `.venv`). Never give the interpreter
two owners: the project's Python version lives in pyproject.toml and uv's
pin, never in a mise config; mise's job ends at delivering uv.

(id: `layout-interpreter-owner`; severity: important; source: uv
documentation — Python versions; the single-owner boundary is this
standard)

## pyproject.toml — the single manifest

All project metadata lives in `pyproject.toml`: name, version,
`requires-python`, dependencies, entry points (`[project.scripts]`) —
the `[project]` table per PEP 621 — plus the build system (PEP 517/518)
and every tool's configuration section. No `setup.py`, `setup.cfg`, or
`requirements.txt` in new projects. Annotated example:
[reference/pyproject.toml](reference/pyproject.toml).
(id: `layout-single-manifest`; severity: minor; source: PEP 621,
PEP 517/518)

Static `version = "x.y.z"` in `[project]` is the default (PEP 440
version format); dynamic versioning only with a recorded reason.
(id: `layout-static-version`; severity: minor; source: PEP 440 for the
format; the static-first stance is this standard)

## src layout

Packages live under `src/<package_name>/` — imports resolve against the
installed package, never the working directory, so tests catch packaging
mistakes. Tests live in `tests/` beside `src/`, never inside the
package. Canonical tree: [reference/src-layout.md](reference/src-layout.md).
(id: `layout-src`; severity: minor; source: PyPA Python Packaging User
Guide, "src layout vs flat layout")

## Module boundaries

- **Dependency direction is one-way**: concrete edges point at
  abstractions/util modules, never back; an import cycle is always a
  boundary bug, not a style choice. (id: `layout-dep-direction`;
  severity: important; source: this standard)
- **One purpose per module.** A module named for what it does
  (`retry.py`, `profiles.py`) — a `utils.py` grab-bag is a smell after
  the second unrelated addition. (id: `layout-single-purpose`;
  severity: minor; source: this standard)
- **When to split**: split a module when it serves two audiences
  (callers import disjoint halves), or when its top-level names stop
  fitting one sentence. Do NOT split on line count alone — a cohesive
  400-line module beats two coupled 200-line ones.
  (id: `layout-when-to-split`; severity: minor; source: this standard)
