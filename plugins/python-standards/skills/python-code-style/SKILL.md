---
name: python-code-style
description: Use when writing or reviewing Python code at the line and function level — naming, idioms, comprehensions and iteration patterns, and ruff as both linter and formatter with its pyproject.toml configuration. Project structure belongs to python-project-layout; type annotations to python-typing; tests to python-testing.
---

# Python code style

Line- and function-level standards. Each rule carries a stable id —
cite it in review findings as `(standard: python-code-style, rule: <id>)`.

## Toolchain

**ruff is BOTH the linter and the formatter** — `ruff check` and
`ruff format`. Never add black, isort, or flake8 alongside: ruff
replaces all three, and two formatters in one repo guarantee churn.
Configuration lives in `pyproject.toml` under `[tool.ruff]` — the
canonical, annotated block is in
[reference/ruff-config.toml](reference/ruff-config.toml). Copy it into
new projects; do not hand-roll a different rule selection without
recording why. (id: `style-ruff-only`)

## Naming (PEP 8)

| Element | Convention | Example |
|---|---|---|
| module / package | `snake_case`, short, no hyphens | `camera_profiles` |
| function / method | `snake_case`, verb-first | `load_profile()` |
| variable | `snake_case`, no abbreviations that save two letters | `retry_count` |
| constant | `UPPER_SNAKE` at module top | `DEFAULT_TIMEOUT` |
| class / exception | `CapWords`; exceptions end in `Error` | `ProfileNotFoundError` |
| private | single leading underscore; no `__name` mangling without a documented reason | `_parse_row()` |

(id: `style-naming`)

## Idioms

Before/after pairs for every rule below live in
[reference/idioms.md](reference/idioms.md).

- **Comprehensions for transforms, loops for effects.** A comprehension
  builds a value; side effects belong in a `for` loop. Nested
  comprehensions past two `for` clauses become loops.
  (id: `style-comprehensions`)
- **Early returns over arrow code.** Guard clauses first, happy path at
  the shallowest indent. (id: `style-early-return`)
- **EAFP over LBYL** when the operation itself reports failure
  (`try/except KeyError` over `if key in d` + lookup) — except at
  validation boundaries, where explicit checks read better.
  (id: `style-eafp`)
- **f-strings** (PEP 498) for interpolation — never `%` or `.format()`
  in new code. Logging calls use lazy `%s` formatting
  (`logger.info("x=%s", x)`) so the string is built only when emitted
  (ruff `G004`). (id: `style-fstrings`)
- **pathlib over os.path** (PEP 428) — `Path` objects end-to-end;
  convert to `str` only at library boundaries that demand it.
  (id: `style-pathlib`)

## Docstrings

- Every public function carries a docstring — a one-liner saying what
  it does is the minimum (PEP 257 governs the basics: triple quotes,
  imperative one-liners). Sections, when needed, use **Google style**
  (`Args:` / `Returns:` / `Raises:`) — compact and readable:

  ```python
  def load_profile(name: str) -> Profile:
      """Load a camera profile by name.

      Args:
          name: Registry key of the profile.

      Raises:
          ProfileNotFoundError: When the name is not registered.
      """
  ```

- Do not enable ruff's full `D` ruleset by default — it demands
  docstrings everywhere and drowns the useful ones.
- **An adopted project's enforced convention wins** (e.g. NumPy style
  with `D` rules in CI): consistency inside a codebase beats this
  skill's preference — respect it, do not convert.

(id: `style-docstrings`)

## Review severities

- Critical: none at this level (style never breaks production alone).
- Important: `style-ruff-only` violations (competing formatter/linter
  present), naming that misleads (`get_x()` that mutates).
- Minor: everything else in this skill.
