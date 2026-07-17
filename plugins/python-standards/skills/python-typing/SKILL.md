---
name: python-typing
description: Use when adding or tightening Python type annotations — annotation policy and strictness, protocols vs ABCs, and pyright configuration in pyproject.toml. Runtime validation models are covered where they live (python-web-api for pydantic in APIs).
---

# Python typing

Annotation standards and the type checker. Cite rules in review
findings as `(standard: python-typing, rule: <id>)`. Each rule names
its source: a PEP, the typing spec, an official doc, or `this standard`
(a recorded house decision).

## Type checker — pyright, watching ty

pyright is the standard type checker: typing-spec conformance, speed,
pydantic v2 support without plugins, and parity with Pylance in the
editor. Astral's `ty` is the watched successor — revisit this choice when
`ty` reaches a stable release; until then it is not part of the toolchain.

Run it as `uv run pyright`; configuration lives in `pyproject.toml`
under `[tool.pyright]` — canonical block in
[reference/pyright-config.toml](reference/pyright-config.toml).
(id: `typing-pyright`; source: the Python typing spec —
typing.python.org — for conformance, pyright documentation for
configuration; the tool choice is this standard)

## Annotation policy

- **Every public function and method is fully annotated** (PEP 484 is
  the foundation) — parameters and return type, including `-> None`.
  Private helpers may rely on inference when the types are obvious from
  one screen of context. (id: `typing-public-api`; source: PEP 484; the
  public-minimum policy is this standard)
- **Modern syntax only**: `X | None` over `Optional[X]` (PEP 604),
  `list[str]` over `List[str]` (PEP 585), `collections.abc`
  (`Iterable`, `Callable`) over their deprecated `typing` twins. ruff
  `UP` enforces this. (id: `typing-modern-syntax`; source: PEP 604,
  PEP 585)
- **No `Any` laundering**: an `Any` that enters at a boundary is
  narrowed or validated before it spreads; `cast()` carries a comment
  saying why it is safe. (id: `typing-no-any-laundering`; source:
  PEP 484 defines `Any`'s escape-hatch semantics; the laundering ban is
  this standard)

## Strictness

New projects run pyright in **strict** mode. An adopted codebase starts
in `standard` mode with per-directory `strict` overrides, ratcheting up
— never down. Blanket `# type: ignore` is banned; each ignore names the
error code (`# type: ignore[arg-type]`) and survives only with a reason.
(id: `typing-strictness`; source: pyright documentation —
`typeCheckingMode`; the strict-for-new / ratchet-for-adopted policy is
this standard)

## Protocols vs ABCs

- **Protocol** (structural, PEP 544) when you own the call site but not
  the implementations — plugins, adapters, anything third parties
  provide.
- **ABC** (nominal) when you own the hierarchy and want shared behavior
  or invariants enforced in a base class.
- Never both for one seam. Worked example:
  [reference/typing-patterns.md](reference/typing-patterns.md).
(id: `typing-protocol-vs-abc`; source: PEP 544 for Protocol, the
CPython `abc` module docs for ABCs; the when-which rule is this
standard)

## Review severities

- Important: `typing-no-any-laundering`, unexplained `type: ignore`,
  public API without annotations.
- Minor: everything else in this skill.
