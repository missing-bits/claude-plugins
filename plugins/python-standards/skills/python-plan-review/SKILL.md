---
name: python-plan-review
description: Plan-review checklist for Python — interpreter versions, lockfile behavior, async boundaries, typing limits, pytest coverage; invoked by the plan-adversary agent.
---

# Python plan-review checklist

Walk every dimension against the reviewed plan; nothing passes by
default. Every finding cites a plan quote or file path as evidence.
Severities noted per dimension bind — do not re-grade them.

## 1. Interpreter and environment

- The plan names the Python version it targets, consistent with the
  project's `requires-python`. Unstated or conflicting versions →
  Important.
- Steps that install or run outside `uv run` / the uv-managed
  environment (bare `pip install`, system Python) → Important.

## 2. Lockfile behavior

- A dependency change without `uv add`/`uv lock` and `uv.lock` committed
  in the same task → Important.
- Pinning or upgrading transitive dependencies by hand-editing
  pyproject.toml → Important.

## 3. Async boundaries

- Blocking calls planned inside async paths (sync HTTP clients,
  `time.sleep`, unpooled DB access) → Critical on a request path,
  Important elsewhere.
- Background tasks without named cancellation or error handling →
  Important.

## 4. Typing limits

- New public functions without planned annotations, or plans that
  silence pyright (`# type: ignore`, config exclusions) without a stated
  justification → Important.
- Untyped dict-shaped data crossing a service boundary where a model is
  the standard → Important; inside a module → Minor.

## 5. Pytest coverage

- New behavior without a named pytest test (file plus test name) →
  Important.
- A planned test that never exercises the changed code path → Important.
- Coverage expectations follow the coverage-of-change stance
  (python-testing, `test-coverage-of-change`): the review judges the
  CHANGE's tests; a numeric repo-wide threshold applies only when the
  project records one, and waving a recorded threshold regression
  through without a decision → Minor.
