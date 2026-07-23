---
name: python-cli
description: Use when building or extending a Python command-line tool — typer app and command structure, configuration handling, logging setup and error reporting for CLIs, and distribution via uv tool.
---

# Python CLI tools

Standards for command-line tools. Cite rules in review findings as
`(standard: python-cli, rule: <id>)`. Each rule names its source: a
PEP, an official doc, a Unix convention, or `this standard` (a recorded
house decision). Errors and logging for CLIs live here — there is no
separate errors/logging skill.

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
(id: `cli-typer-structure`; severity: minor; source: typer
documentation; the subcommands-over-flag-modes rule is this standard)

## Configuration

Precedence, strictest wins: **flags > environment variables > config
file > defaults**. A value settable in the file is settable by flag;
the flag names the file key (`--retry-count` ↔ `retry_count`).
Config file format is TOML — readable with the stdlib `tomllib`
(PEP 680), no parsing dependency; location follows the platform
convention (`platformdirs.user_config_dir(app_name)`) — never a dotfile
invented ad hoc in `$HOME`. (id: `cli-config-precedence`; severity:
minor; source: PEP 680 for tomllib, platformdirs documentation and the
XDG Base Directory specification for locations; the precedence order
is this standard)

## Logging and errors

- Logging goes to **stderr**; stdout is reserved for the command's
  DATA (so pipes work). (id: `cli-stderr-logs`; severity: important;
  source: the Unix stream convention as documented in CPython's
  `sys.stderr` docs)
- Default level INFO, `--verbose` switches DEBUG — configuration in
  [reference/logging-config.py](reference/logging-config.py);
  `print()` for diagnostics fails review (ruff `T201` when enabled;
  data output via `typer.echo`/`rich` is fine).
  (id: `cli-logging-config`; severity: minor; source: CPython Logging
  HOWTO; the INFO-default/--verbose split is this standard)
- **Expected failures** (bad input, missing file, remote refusal) end
  as one clear stderr message + exit code 1 — no traceback. Tracebacks
  are for bugs, and `--verbose` re-enables them for debugging.
  (id: `cli-errors-no-traceback`; severity: important; source: this
  standard)
- Exit codes: `0` success, `1` runtime failure, `2` usage error
  (typer's default for bad invocations). Scripts depend on these.
  (id: `cli-exit-codes`; severity: important; source: the Unix
  exit-status convention; usage-error 2 as documented by argparse and
  click/typer)

## Distribution

Tools install via `uv tool install <package>` (or run ad hoc with
`uvx <package>`), wired to the `[project.scripts]` entry point — the
entry-point convention itself belongs to python-project-layout.
(id: `cli-uv-tool`; severity: minor; source: uv documentation — tools)
