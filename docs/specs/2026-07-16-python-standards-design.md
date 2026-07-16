---
ticket: none
date: 2026-07-16
status: approved
grilled: 2026-07-16
architect: LGTM
branch: feature/python-standards
base: master
---

# python-standards — Python coding-standards plugin

## Overview

New plugin `python-standards` (v0.1.0) for the missing-bits
marketplace: skills encoding Python coding standards, a code-review
stack, and integration with the working-process plugin — the first
domain plugin to exercise both of working-process's integration
conventions (`*-plan-review` discovery and the Rules payload).

The shape — area skills with `reference/` examples, a review skill, a
reviewer agent, a review command, a plan-review checklist — is inspired
by the author's earlier domain-standards plugin work in another
marketplace, but is designed fresh here: this spec is the authoritative
construction, with improvements (chiefly the shared report contract,
companion spec `2026-07-16-working-process-review-reports-design.md`),
not a migration of existing content.

## Audience and toolchain

Primary use: CLI tools / automation and web services (APIs) — the
plugin author's own projects; author repositories will be supplied as
content input during implementation.

Standardized toolchain: **uv** (environments, dependencies, packaging
via pyproject.toml), **ruff** (lint + format), **pytest**, **pyright**
(type checking; chosen for typing-spec conformance, speed, plugin-free
pydantic v2 support, and Pylance parity — the typing skill notes
Astral's `ty` as the watched successor). Standards content: community
consensus (PEPs, PyPA packaging guide, official tool docs); the
author's preferences decide contested points.

## Skills (6)

Each skill: `SKILL.md` + `reference/` examples. Descriptions written
disjointly (no two skills compete for the same trigger); authored with
skill-creator + superpowers:writing-skills per repo convention.

| Skill | Scope |
|---|---|
| `python-code-style` | naming, idioms, ruff as lint+formatter, pyproject config |
| `python-project-layout` | uv, pyproject.toml, src layout, entry points, package versioning; module boundaries, dependency direction, when to split code; the mise↔uv boundary (one paragraph: mise pins tools incl. uv itself, uv owns the project's Python and venv — never two owners of the interpreter) |
| `python-typing` | annotations, strictness policy, protocols vs ABCs, pyright configuration; `ty` watch note |
| `python-testing` | pytest structure, fixtures, parametrization, coverage |
| `python-cli` | typer-based CLIs, config handling, logging, distribution via `uv tool` |
| `python-web-api` | tightly scoped: FastAPI layering (router → service → repo), pydantic models, async boundaries, HTTP error handling |

## Review stack

- `python-code-review` skill: audits code against the standards skills.
  Report contract: when the working-process review-reports rule is
  installed it is authoritative — "installed" means the contract probe
  defined by the companion spec succeeds (project-level then user-level
  rules target contains `working-process/review-reports.md`; the rule
  does not auto-load in review sessions). The skill carries a **minimal inline
  fallback** — severity scale Critical/Important/Minor, Summary, the
  shared `findings: { critical: N, important: N, minor: N }` frontmatter
  key, `ticket` and `standards: python-standards` frontmatter (required
  even standalone) — a strict subset of
  the shared contract, so report shape never depends on the install
  profile; marked "the installed working-process review-reports rule
  supersedes this". Reports go to `docs/code-review/`; a standalone
  install simply creates the directory (the first-create mode question
  belongs to working-process's process-artifacts rule and is absent in a
  standalone install).
- `py-code-reviewer` agent: reviews a diff or named files, writes the
  report, returns findings by severity. Its description names
  `docs/code-review/` as the report destination.
- `/py-review` command: review the current diff or named files.
- Naming rule (deliberate split, not drift): skills carry the full
  `python-` prefix (triggering surfaces, matched against prose);
  the reviewer agent and the command use the short `py-` prefix
  (frequently typed surfaces). `python-code-review` deliberately follows
  the `*-code-review` pattern a future working-process review
  orchestrator will discover (companion spec non-goal).
- Run scope per the shared contract: `/py-review` reviews Python files
  only and notes out-of-domain files in Summary as out of scope.

## working-process integration

- `python-plan-review` skill: plan-review checklist discovered by the
  plan-adversary agent — Python verification specifics: interpreter
  versions, lockfile behavior, async boundaries, typing limits, pytest
  coverage.
- Rules payload `rules/python-toolchain.md`, `paths: ["**/*.py",
  "pyproject.toml"]`: the toolchain (uv + ruff + pytest + pyright) and
  conditional pointers to the skills ("when available"). No mise
  content (machine setup, not code standard). Frontmatter reviewed by
  hand (validate skips `rules/`).
- Assumed convention range: **working-process ≥ 0.5.0** (Process
  directory `docs/code-review/` + review-reports rule); working-process
  0.5.0 ships first. No `dependencies` edge — a standalone install is
  fully functional;
  every working-process mention in content is conditional.

## Non-goals

- mise beyond the uv-boundary paragraph — deferred to a possible future
  `tools-standards` plugin.
- PyPI/wheel publishing standards (no consumer in the author's profile).
- Separate errors/logging or async skills (owned by python-cli and
  python-web-api respectively); data/ML content.

## Verification

- `claude plugin validate .` and `claude plugin validate
  plugins/python-standards` pass; marketplace catalog entry + README row
  land in the same commit as the manifest (marketplace-sync rule).
- Install from the local marketplace; the six standards skills and
  `python-plan-review` appear in the skills list; the agent appears
  under the plugin namespace.
- `/py-review` on a sample diff writes a report to `docs/code-review/`
  honoring the shared format (working-process installed) and the inline
  fallback (standalone install).
- A plan-adversary dispatch on a Python-touching plan discovers and
  loads `python-plan-review`.
- sync-rules installs `python-toolchain.md` as a foreign payload; the
  drift hook stays silent afterwards.

## Architect findings — 2026-07-16 round 1

Dual review (context-carrying + fresh reviewer); stricter grade kept.

- **Important (both reviewers)**: the inline fallback specified a
  verdict line absent from the shared contract — report shape would
  change with install profile, and the precedence line would strip the
  verdict. → Fixed: fallback is now a strict subset of the contract
  (severity scale, Summary with counts, `ticket`); no verdict element on
  either side.
- **Important (fresh)**: "when the rule is installed it is
  authoritative" named a condition without a mechanism. → Fixed: the
  contract probe (project- then user-level rules target) is now cited
  from the companion spec.
- **Minor (fresh)**: mixed `python-*` / `py-*` prefixes looked like
  drift. → Fixed: the split is now a stated rule (skills full prefix,
  typed surfaces short).

Round 2 (verification pass): all dispositions confirmed; two new minors
fixed inline — the fallback names the shared `findings:` counts key
(subset claim now exact), and standalone directory creation is stated (no
first-create question without working-process). Verdict: LGTM.
