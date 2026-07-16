---
name: python-testing
description: Use when writing or reviewing Python tests — pytest suite structure and naming, fixtures and conftest.py placement, parametrization, and coverage configuration and expectations.
---

# Python testing

pytest standards. Cite rules in review findings as
`(standard: python-testing, rule: <id>)`. Everything runs via
`uv run pytest`.

## Suite structure

- `tests/` sits beside `src/` and mirrors the package: code in
  `src/pkg/profiles/loader.py` is tested in
  `tests/profiles/test_loader.py`. (id: `test-mirror`)
- Files are `test_<module>.py`; functions `test_<behavior>` named for
  the behavior, not the method (`test_missing_profile_raises`, not
  `test_load_2`). (id: `test-naming`)
- No logic in `tests/__init__.py`; shared helpers live in fixtures or
  plain modules imported explicitly. (id: `test-no-init-logic`)
- Slow or environment-needing tests carry a marker (e.g.
  `@pytest.mark.integration`) declared in `[tool.pytest.ini_options]
  markers` — the default run stays fast. (id: `test-markers`)

## Fixtures

- **Scope discipline**: function scope is the default; wider scopes
  (session, module) only for genuinely expensive, read-only resources —
  a session-scoped mutable fixture is a test-pollution bug waiting.
  (id: `test-fixture-scope`)
- **conftest.py at the nearest common ancestor** of its consumers —
  never one giant root conftest. (id: `test-conftest-placement`)
- **Factory fixtures over module-level state**: a fixture returns a
  builder (`make_profile(**overrides)`) so each test states what it
  cares about. (id: `test-factories`)
- `autouse=True` is rare and always carries a comment saying why every
  test needs it. Examples: [reference/conftest.py](reference/conftest.py).
  (id: `test-autouse-rare`)

## Parametrization

`pytest.mark.parametrize` with explicit `ids=` when cases are the same
behavior over different inputs; separate test functions when the
BEHAVIOR differs (different asserts = different test). Examples:
[reference/test-patterns.py](reference/test-patterns.py).
(id: `test-parametrize`)

## Mocking

Mock only at boundaries the code does not own (network, clock,
subprocess); prefer a fake or a real temp resource over a mock when
cheap. Never patch internals of the unit under test — that pins the
implementation, not the behavior. (id: `test-mock-boundaries`)

## Coverage

Measured with pytest-cov (`uv run pytest --cov=src`); new and changed
code ships with tests covering its behavior — reviewers judge coverage
of the CHANGE, not the historical total. A numeric repo-wide gate is a
per-project decision recorded in `pyproject.toml`, not assumed.
(id: `test-coverage-of-change`)

## Review severities

- Important: `test-mock-boundaries` (patched internals),
  `test-fixture-scope` (mutable wide-scope fixtures), a behavior change
  shipped with no covering test.
- Minor: everything else in this skill.
