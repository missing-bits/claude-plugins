---
name: python-cli
description: Use when building or extending a Python command-line tool — typer app and command structure, configuration handling, logging setup and error reporting for CLIs, and distribution via uv tool.
---

# Python CLI tools

Standards for command-line tools. Cite rules in review findings as
`(standard: python-cli, rule: <id>)`. Errors and logging for CLIs live
here — there is no separate errors/logging skill.

## Framework — typer

typer is the CLI framework: type-hint-driven, subcommand-friendly,
help text for free. Structure:

- one `typer.Typer()` app per tool, subcommands as functions —
  `tool run`, `tool list`, never flag-switched modes (`tool --run`);
- **arguments** for what the command operates ON (required, positional);
  **options** for how it behaves (defaults, `--flags`);
- every command and option carries help text — a CLI whose `--help`
  needs external docs fails review.

Complete skeleton: [reference/cli-skeleton.py](reference/cli-skeleton.py).
(id: `cli-typer-structure`)

## Configuration

Precedence, strictest wins: **flags > environment variables > config
file > defaults**. A value settable in the file is settable by flag;
the flag names the file key (`--retry-count` ↔ `retry_count`).
Config file format is TOML — readable with the stdlib `tomllib`
(PEP 680), no parsing dependency; location follows the platform
convention (`platformdirs.user_config_dir(app_name)`) — never a dotfile
invented ad hoc in `$HOME`. (id: `cli-config-precedence`)

## Logging and errors

- Logging goes to **stderr**; stdout is reserved for the command's
  DATA (so pipes work). (id: `cli-stderr-logs`)
- Default level INFO, `--verbose` switches DEBUG — configuration in
  [reference/logging-config.py](reference/logging-config.py);
  `print()` for diagnostics fails review (ruff `T201` when enabled;
  data output via `typer.echo`/`rich` is fine).
  (id: `cli-logging-config`)
- **Expected failures** (bad input, missing file, remote refusal) end
  as one clear stderr message + exit code 1 — no traceback. Tracebacks
  are for bugs, and `--verbose` re-enables them for debugging.
  (id: `cli-errors-no-traceback`)
- Exit codes: `0` success, `1` runtime failure, `2` usage error
  (typer's default for bad invocations). Scripts depend on these.
  (id: `cli-exit-codes`)

## Distribution

Tools install via `uv tool install <package>` (or run ad hoc with
`uvx <package>`), wired to the `[project.scripts]` entry point — the
entry-point convention itself belongs to python-project-layout.
(id: `cli-uv-tool`)

## Review severities

- Important: `cli-stderr-logs` (data/log stream mixing breaks pipes),
  `cli-exit-codes` (wrong codes break scripting),
  `cli-errors-no-traceback` for expected failures.
- Minor: everything else in this skill.
