---
paths:
  - "**/*.py"
  - "pyproject.toml"
---

# Python toolchain

This project follows the python-standards toolchain:

- **uv** owns environments, dependencies, and packaging. Run project
  commands through `uv run`; change dependencies with `uv add` /
  `uv remove` (never hand-edit pyproject.toml dependencies plus manual
  pip); `uv.lock` is committed and refreshed in the same change.
- **ruff** is both linter and formatter — `ruff check` and `ruff format`;
  no black, isort, or flake8 alongside.
- **pytest** is the test runner: `uv run pytest`.
- **pyright** is the type checker: `uv run pyright`; public functions
  carry type annotations.

When the python-standards plugin's skills are available, load the
matching one before working: `python-code-style` (naming, idioms, ruff
configuration), `python-project-layout` (project structure, uv usage,
module boundaries), `python-typing` (annotations, pyright
configuration), `python-testing` (pytest conventions), `python-cli`
(typer CLIs), `python-web-api` (FastAPI services). When they are not
available, the toolchain facts above still bind.
