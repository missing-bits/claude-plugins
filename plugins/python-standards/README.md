# python-standards

Python coding standards for the uv + ruff + pytest + pyright toolchain:
uv owns environments, dependencies, and packaging; ruff is linter and
formatter; pytest runs the tests; pyright checks types (with Astral's
`ty` as the watched successor). Standards follow community consensus —
PEPs, the PyPA packaging guide, official tool docs — with the author's
preferences on contested points.

## Standards skills

| Skill | Scope |
|---|---|
| `python-code-style` | naming, idioms, ruff as lint + formatter, pyproject config |
| `python-project-layout` | uv, pyproject.toml, src layout, entry points, module boundaries, the mise↔uv ownership boundary |
| `python-typing` | annotations, strictness policy, protocols vs ABCs, pyright configuration |
| `python-testing` | pytest structure, fixtures, parametrization, coverage |
| `python-cli` | typer CLIs, config handling, logging, distribution via uv tool |
| `python-web-api` | FastAPI layering (router → service → repository), pydantic models, async boundaries, HTTP error handling |

Each skill ships `reference/` examples alongside its SKILL.md.

## Review stack

- **`python-code-review` skill** — audits Python code against the
  standards skills; writes one review report per run to
  `docs/code-review/`.
- **`python-code-reviewer` agent** — reviews a diff or named files,
  writes the report to `docs/code-review/`, returns findings by
  severity.
- **`/python-review` command** — review the current diff or named
  files. Python files only; out-of-domain files are noted as out of
  scope.

When the working-process plugin's review-reports rule is installed
(detected by its contract probe), that rule's report contract is
authoritative; without it, the skill's minimal inline fallback applies —
a strict subset of the same contract, so the report shape never depends
on the install profile.

Naming is one `python-` family throughout; skills are named for the
activity (`python-code-review`), the agent for the actor
(`python-code-reviewer`) — the same activity/actor distinction
working-process draws between its `*-session` skills and its review
agents.

## working-process integration

- **`python-plan-review` skill** — plan-review checklist discovered by
  the working-process plan-adversary agent when a reviewed plan touches
  Python: interpreter versions, lockfile behavior, async boundaries,
  typing limits, pytest coverage.
- **`rules/python-toolchain.md`** — a Rules payload distributed by
  working-process's sync-rules engine; states the toolchain and points
  at the skills conditionally.

Integration assumes working-process ≥ 0.5.0 when it is installed; the
plugin has no dependency on it — a standalone install is fully
functional, and every working-process mention in content is conditional.
