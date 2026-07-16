---
name: python-typing
description: Use when adding or tightening Python type annotations — annotation policy and strictness, protocols vs ABCs, and pyright configuration in pyproject.toml. Runtime validation models are covered where they live (python-web-api for pydantic in APIs).
---

# Python typing

Annotation standards and the type checker. Cite rules in review
findings as `(standard: python-typing, rule: <id>)`.

## Type checker — pyright, watching ty

pyright is the standard type checker: typing-spec conformance, speed,
pydantic v2 support without plugins, and parity with Pylance in the
editor. Astral's `ty` is the watched successor — revisit this choice when
`ty` reaches a stable release; until then it is not part of the toolchain.

Run it as `uv run pyright`; configuration lives in `pyproject.toml`
under `[tool.pyright]` — canonical block in
[reference/pyright-config.toml](reference/pyright-config.toml).
(id: `typing-pyright`)

## Annotation policy

- **Every public function and method is fully annotated** — parameters
  and return type, including `-> None`. Private helpers may rely on
  inference when the types are obvious from one screen of context.
  (id: `typing-public-api`)
- **Modern syntax only**: `X | None` over `Optional[X]`, `list[str]`
  over `List[str]`, `collections.abc` (`Iterable`, `Callable`) over
  their deprecated `typing` twins. ruff `UP` enforces this.
  (id: `typing-modern-syntax`)
- **No `Any` laundering**: an `Any` that enters at a boundary is
  narrowed or validated before it spreads; `cast()` carries a comment
  saying why it is safe. (id: `typing-no-any-laundering`)

## Strictness

New projects run pyright in **strict** mode. An adopted codebase starts
in `standard` mode with per-directory `strict` overrides, ratcheting up
— never down. Blanket `# type: ignore` is banned; each ignore names the
error code (`# type: ignore[arg-type]`) and survives only with a reason.
(id: `typing-strictness`)

## Protocols vs ABCs

- **Protocol** (structural) when you own the call site but not the
  implementations — plugins, adapters, anything third parties provide.
- **ABC** (nominal) when you own the hierarchy and want shared behavior
  or invariants enforced in a base class.
- Never both for one seam. Worked example:
  [reference/typing-patterns.md](reference/typing-patterns.md).
(id: `typing-protocol-vs-abc`)

## Review severities

- Important: `typing-no-any-laundering`, unexplained `type: ignore`,
  public API without annotations.
- Minor: everything else in this skill.
