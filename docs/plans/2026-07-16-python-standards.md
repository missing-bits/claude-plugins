---
ticket: none
date: 2026-07-16
status: implemented
adversary: LGTM
branch: feature/python-standards
base: master
spec: ../specs/2026-07-16-python-standards-design.md
---

# python-standards Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `python-standards` plugin (v0.1.0) — six Python standards skills, a review stack writing Review reports, a `python-plan-review` checklist, and a `python-toolchain` Rules payload — and register it in the `missing-bits` marketplace.

**Architecture:** A single Standards plugin under `plugins/python-standards/`: area skills with `reference/` examples, a `python-code-review` skill that defers to the working-process review-reports contract via the Contract probe and carries a strict-subset inline fallback for a Standalone install, a `python-code-reviewer` agent and `/python-review` command on top of that skill, plus the Rules payload picked up by working-process's Rules engine. No `dependencies` edge — a Standalone install is fully functional.

**Tech Stack:** Claude Code plugin system (plugin.json, marketplace.json, skills/SKILL.md, agents/*.md, commands/*.md, rules/*.md), git, jq.

## Global Constraints

- **Sequencing (plan-level):** Tasks 10–12 (the review stack and the README that documents it) assume working-process **0.5.0 is released — or at least its `rules/review-reports.md` content is frozen** — because the fallback must stay a strict subset of that contract and copy its canonical filename command verbatim, and the README consumes the review-stack contracts from Tasks 10–11. Tasks 1–9 do not depend on it and can proceed independently, in any interleaving with the working-process 0.5.0 work. If Tasks 10–11 executed against frozen-but-unreleased content, Task 13 Step 6a re-verifies the command byte-identity against the RELEASED rule.
- Assumed convention range: **working-process ≥ 0.5.0** (Process directory `docs/code-review/` + review-reports rule). NO `dependencies` entry in `plugin.json`; every mention of working-process inside plugin content is conditional ("when … is installed/available").
- **Content input:** community consensus is the baseline — PEPs, the PyPA packaging guide, official tool docs (uv, ruff, pytest, pyright, typer, FastAPI, pydantic). The developer's repositories are ILLUSTRATIVE CONTEXT only: they show the kinds of projects the skills serve, and do NOT define the developer's Python preferences — never derive a preference from them silently. Contested points are decided by the developer's explicitly stated preferences; when unstated, collect them as open questions for the developer. NEVER invent personal preferences.
- **Toolchain facts (verbatim in content):** uv (environments, dependencies, packaging via pyproject.toml), ruff (lint + format), pytest, pyright (typing-spec conformance, speed, plugin-free pydantic v2 support, Pylance parity — with Astral's `ty` noted as the watched successor).
- **Naming rule (amended 2026-07-17, developer decision):** ONE `python-` family for every surface; skills are named for the activity (`python-code-review`), the agent for the actor (`python-code-reviewer`). The original `py-` short-prefix split was dissolved after implementation — occurrences in this plan were renamed accordingly. Names are kebab-case.
- **Skill authoring:** every skill is authored with the `skill-creator` skill (scaffolding, `description:` tuning, evals) plus the `superpowers:writing-skills` discipline. Skill descriptions are written disjointly — no two skills compete for the same trigger.
- **Glossary binds wording** (docs/domain/glossary.md): Standards plugin, Standalone install, Contract probe, Review report, Rules payload, Rules engine. Respect every `_Avoid_` ban — never "standards stack", never "solo install", never "review output", never "rules plugin", never unqualified "probe".
- **Frontmatter safety:** quote any `description:` (or other scalar) containing `: ` (colon+space). `claude plugin validate` skips `rules/` — review the Rules payload frontmatter by hand.
- **Public-repo hygiene:** English only, no machine-specific paths, no company or client names — in every committed file and commit message.
- **Commits:** Conventional Commits, ONE line (single subject, no body, no trailers — no Co-Authored-By).
- All tasks land at plugin version **0.1.0** (a new plugin on one topic branch — no per-commit bumps before the first release).
- Repo root during execution: the claude-plugins repository root, branch `feature/python-standards`.

---

### Task 1: Plugin manifest and marketplace registration

Per the marketplace-sync rule, a new plugin lands with all three identity places at once — manifest, catalog entry, README row — in ONE commit.

**Files:**
- Create: `plugins/python-standards/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json` (append to `plugins` array)
- Modify: `README.md` (repo root — add a plugin table row)

**Interfaces:**
- Produces: plugin name `python-standards`, version `0.1.0` (consumed by every later task; the README of Task 12 and the verification of Task 13 use the name verbatim).

- [ ] **Step 1: Write `plugins/python-standards/.claude-plugin/plugin.json`**

```json
{
  "name": "python-standards",
  "description": "Python coding standards for the uv + ruff + pytest + pyright toolchain: six area skills, a code-review stack (python-code-review skill, python-code-reviewer agent, /python-review command) writing review reports to docs/code-review/, a python-plan-review checklist for plan reviews, and a python-toolchain rule shipped as a Rules payload",
  "version": "0.1.0",
  "author": { "name": "Missing Bits (Jacek Nakonieczny)" },
  "license": "MIT",
  "keywords": ["python", "standards", "uv", "ruff", "pytest", "pyright", "typer", "fastapi", "review"]
}
```

No `dependencies` field — a Standalone install is fully functional by design.

- [ ] **Step 2: Add the catalog entry**

In `.claude-plugin/marketplace.json`, append to the `plugins` array (after the `working-process` entry):

```json
{
  "name": "python-standards",
  "source": "./plugins/python-standards",
  "description": "Python coding standards for the uv + ruff + pytest + pyright toolchain: area skills, a code-review stack, a plan-review checklist, and a python-toolchain rule"
}
```

- [ ] **Step 3: Add the README row**

In the repo root `README.md` plugin table, add below the `working-process` row:

```markdown
| `python-standards` | Python coding standards for uv + ruff + pytest + pyright: area skills, code-review stack, plan-review checklist, distributed toolchain rule |
```

- [ ] **Step 4: Validate**

Run: `jq -e '.name == "python-standards" and .version == "0.1.0" and (has("dependencies") | not)' plugins/python-standards/.claude-plugin/plugin.json`
Expected: `true`

Run: `jq -e '[.plugins[].name] == ["working-process", "python-standards"] and (.plugins[1].source == "./plugins/python-standards")' .claude-plugin/marketplace.json`
Expected: `true`

Run: `grep -c 'python-standards' README.md`
Expected: `1`

- [ ] **Step 5: Commit (all three files — one commit, per marketplace-sync)**

```bash
git add plugins/python-standards/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md
git commit -m "feat(python-standards): register the plugin in the marketplace"
```

---

### Task 2: Content input collection + python-code-style skill

**Files:**
- Create: `plugins/python-standards/skills/python-code-style/SKILL.md`
- Create: `plugins/python-standards/skills/python-code-style/reference/ruff-config.toml`
- Create: `plugins/python-standards/skills/python-code-style/reference/idioms.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: skill name `python-code-style` (referenced by Task 9's rule pointers, Task 10's review skill, Task 12's README); the content-input repository list reused by Tasks 3–7.

- [ ] **Step 1: Ask the developer for the content-input repositories**

This is a prerequisite, not optional: ask the developer for the paths or URLs of their Python repositories to use as illustrative context (per the spec, they do NOT define preferences — contested points are settled by asking the developer). Record the answer for reuse by Tasks 3–7 in this session. Author standards from community consensus (PEPs, ruff docs) plus the developer's explicit answers; anything unsettled becomes an open question for the developer, never a silent assumption.

- [ ] **Step 2: Mine the inputs for code-style conventions**

Read representative modules and each repository's `pyproject.toml` `[tool.ruff]` section. Note: naming patterns, lint rule selections, line length, quote style, import ordering, docstring conventions. Where repositories disagree with each other, ask the developer which wins.

- [ ] **Step 3: Scaffold and author the skill**

Invoke the `skill-creator` skill for scaffolding and `description:` tuning; follow `superpowers:writing-skills` for content discipline. SKILL.md opens with exactly this frontmatter:

```yaml
---
name: python-code-style
description: Use when writing or reviewing Python code at the line and function level — naming, idioms, comprehensions and iteration patterns, and ruff as both linter and formatter with its pyproject.toml configuration. Project structure belongs to python-project-layout; type annotations to python-typing; tests to python-testing.
---
```

Mandatory content (each a section or explicit rule; sourced per Steps 1–2):

- Naming conventions (modules, functions, variables, constants, classes) per PEP 8 with the developer's contested-point choices.
- Idioms: comprehensions vs loops, early returns, EAFP vs LBYL guidance, f-strings, pathlib over os.path.
- ruff is BOTH linter and formatter (`ruff check`, `ruff format`) — no black/isort/flake8 alongside; configuration lives in `pyproject.toml` under `[tool.ruff]`, pointing at `reference/ruff-config.toml`.
- Rules cited by stable ids where useful for review findings (e.g. ruff rule codes).

- [ ] **Step 4: Write the reference files**

- `reference/ruff-config.toml`: the canonical `[tool.ruff]` / `[tool.ruff.lint]` / `[tool.ruff.format]` block as mined in Step 2 — a complete, copy-pasteable configuration, annotated with comments.
- `reference/idioms.md`: before/after example pairs for each idiom the SKILL.md names (one pair per idiom minimum).

- [ ] **Step 5: Validate**

Run: `grep -c '^name: python-code-style' plugins/python-standards/skills/python-code-style/SKILL.md`
Expected: `1`

Run: `ls plugins/python-standards/skills/python-code-style/reference/`
Expected: `idioms.md  ruff-config.toml`

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 6: Commit**

```bash
git add plugins/python-standards/skills/python-code-style/
git commit -m "feat(python-standards): add python-code-style skill"
```

---

### Task 3: python-project-layout skill

**Files:**
- Create: `plugins/python-standards/skills/python-project-layout/SKILL.md`
- Create: `plugins/python-standards/skills/python-project-layout/reference/pyproject.toml`
- Create: `plugins/python-standards/skills/python-project-layout/reference/src-layout.md`

**Interfaces:**
- Consumes: the content-input repositories collected in Task 2.
- Produces: skill name `python-project-layout` (Tasks 9, 10, 12); the mise↔uv boundary paragraph (single home — no other component repeats it).

- [ ] **Step 1: Confirm the content input**

Confirm the content-input repositories from Task 2 are available in this session; in a fresh session, ask the developer for them again before authoring anything.

- [ ] **Step 2: Mine the inputs for layout conventions**

Read each repository's `pyproject.toml` (build system, entry points, versioning), directory tree (src layout or not), and module structure (package boundaries, internal imports). Ask the developer to settle contested points (e.g. dynamic vs static versioning). The PyPA packaging guide and uv docs are the consensus baseline.

- [ ] **Step 3: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: python-project-layout
description: Use when creating a Python project or restructuring one — uv-managed environments and dependencies, pyproject.toml, src layout, entry points, package versioning, module boundaries and dependency direction, and when to split code. Line-level style belongs to python-code-style; in-service layer architecture (router/service/repository) to python-web-api.
---
```

Mandatory content:

- uv owns environments, dependencies, and packaging: `uv init`, `uv add`/`uv remove`, `uv lock`/`uv sync`, `uv run`; `uv.lock` is committed.
- pyproject.toml as the single project manifest: metadata, `requires-python`, dependencies, entry points (`[project.scripts]`), tool sections.
- src layout, package versioning per the mined convention.
- Module boundaries: dependency direction, single-purpose modules, when to split code into a new module or package (the concrete thresholds mined in Step 2).
- The mise↔uv boundary — EXACTLY one paragraph, this content (wording may be polished, facts may not drift):

```markdown
## Tool ownership — mise and uv

mise pins developer tools on the machine — including uv itself — while uv
owns the project's Python interpreter and virtual environment
(`requires-python`, `uv python pin`, `.venv`). Never give the interpreter
two owners: the project's Python version lives in pyproject.toml and uv's
pin, never in a mise config; mise's job ends at delivering uv.
```

No other mise content anywhere in the plugin (spec non-goal — deferred to a possible future tools-standards plugin).

- [ ] **Step 4: Write the reference files**

- `reference/pyproject.toml`: a complete annotated example manifest — metadata, `requires-python`, dependencies, `[project.scripts]` entry point, build system, tool sections referenced from the other skills' configs by name only (no duplication).
- `reference/src-layout.md`: the canonical directory tree plus two module-boundary examples (one "keep together", one "split now") mined from the inputs.

- [ ] **Step 5: Validate**

Run: `grep -c '^name: python-project-layout' plugins/python-standards/skills/python-project-layout/SKILL.md`
Expected: `1`

Run: `grep -c 'mise' plugins/python-standards/skills/python-project-layout/SKILL.md`
Expected: the count of mentions inside the single boundary paragraph and its heading only (spot-check by eye that no other section mentions mise).

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 6: Commit**

```bash
git add plugins/python-standards/skills/python-project-layout/
git commit -m "feat(python-standards): add python-project-layout skill"
```

---

### Task 4: python-typing skill

**Files:**
- Create: `plugins/python-standards/skills/python-typing/SKILL.md`
- Create: `plugins/python-standards/skills/python-typing/reference/pyright-config.toml`
- Create: `plugins/python-standards/skills/python-typing/reference/typing-patterns.md`

**Interfaces:**
- Consumes: the content-input repositories collected in Task 2.
- Produces: skill name `python-typing` (Tasks 9, 10, 12); the pyright rationale + `ty` watch note (single home).

- [ ] **Step 1: Confirm the content input**

Confirm the Task 2 repositories are available in this session; in a fresh session, ask the developer again before authoring.

- [ ] **Step 2: Mine the inputs for typing conventions**

Read `[tool.pyright]` sections, annotation density on public vs private functions, protocol vs ABC usage, pydantic model patterns. Ask the developer to settle the strictness policy (e.g. `strict` vs `standard` mode, per-directory overrides).

- [ ] **Step 3: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: python-typing
description: Use when adding or tightening Python type annotations — annotation policy and strictness, protocols vs ABCs, and pyright configuration in pyproject.toml. Runtime validation models are covered where they live (python-web-api for pydantic in APIs).
---
```

Mandatory content:

- Annotation policy: what must be annotated (public functions at minimum), modern syntax (`X | None`, builtin generics), `typing` vs `collections.abc` imports.
- Strictness policy as settled in Step 2, with the `[tool.pyright]` configuration pointing at `reference/pyright-config.toml`.
- Protocols vs ABCs: when structural typing wins, when a nominal base is right.
- The tool-choice rationale + watch note — EXACTLY this substance (single home; wording may be polished, facts may not drift):

```markdown
## Type checker — pyright, watching ty

pyright is the standard type checker: typing-spec conformance, speed,
pydantic v2 support without plugins, and parity with Pylance in the
editor. Astral's `ty` is the watched successor — revisit this choice when
`ty` reaches a stable release; until then it is not part of the toolchain.
```

- [ ] **Step 4: Write the reference files**

- `reference/pyright-config.toml`: the canonical `[tool.pyright]` block for pyproject.toml, annotated, matching the strictness policy.
- `reference/typing-patterns.md`: worked examples — a Protocol vs an ABC for the same seam, a generic function, a `TypedDict`-vs-model decision, narrowing patterns.

- [ ] **Step 5: Validate**

Run: `grep -c '^name: python-typing' plugins/python-standards/skills/python-typing/SKILL.md`
Expected: `1`

Run: `grep -c 'watched successor' plugins/python-standards/skills/python-typing/SKILL.md; grep -c 'pyright' plugins/python-standards/skills/python-typing/SKILL.md`
Expected: `1` and non-zero (the ty watch note is present as a load-bearing phrase, and pyright content is present).

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 6: Commit**

```bash
git add plugins/python-standards/skills/python-typing/
git commit -m "feat(python-standards): add python-typing skill"
```

---

### Task 5: python-testing skill

**Files:**
- Create: `plugins/python-standards/skills/python-testing/SKILL.md`
- Create: `plugins/python-standards/skills/python-testing/reference/conftest.py`
- Create: `plugins/python-standards/skills/python-testing/reference/test-patterns.py`

**Interfaces:**
- Consumes: the content-input repositories collected in Task 2.
- Produces: skill name `python-testing` (Tasks 8, 9, 10, 12).

- [ ] **Step 1: Confirm the content input**

Confirm the Task 2 repositories are available in this session; in a fresh session, ask the developer again before authoring.

- [ ] **Step 2: Mine the inputs for testing conventions**

Read test directory structure, conftest.py fixtures, parametrization style, coverage configuration and thresholds, test naming. Ask the developer to settle contested points (coverage threshold, mocking policy).

- [ ] **Step 3: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: python-testing
description: Use when writing or reviewing Python tests — pytest suite structure and naming, fixtures and conftest.py placement, parametrization, and coverage configuration and expectations.
---
```

Mandatory content:

- Suite structure: `tests/` mirroring the package, test file and function naming, no test logic in `__init__.py`.
- Fixtures: scope discipline, conftest.py placement (nearest common ancestor), factory fixtures over module-level state.
- Parametrization: `pytest.mark.parametrize` with ids, when to parametrize vs write separate tests.
- Coverage: the configuration (`[tool.coverage]` or pytest-cov flags) and the expectation settled in Step 2; running via `uv run pytest`.

- [ ] **Step 4: Write the reference files**

- `reference/conftest.py`: annotated example fixtures — one per scope pattern the SKILL.md names (function-scope factory, session-scope resource, autouse used sparingly with the justification comment).
- `reference/test-patterns.py`: annotated example tests — a parametrized test with ids, a fixture-consuming test, an exception-asserting test (`pytest.raises`).

- [ ] **Step 5: Validate**

Run: `grep -c '^name: python-testing' plugins/python-standards/skills/python-testing/SKILL.md`
Expected: `1`

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 6: Commit**

```bash
git add plugins/python-standards/skills/python-testing/
git commit -m "feat(python-standards): add python-testing skill"
```

---

### Task 6: python-cli skill

**Files:**
- Create: `plugins/python-standards/skills/python-cli/SKILL.md`
- Create: `plugins/python-standards/skills/python-cli/reference/cli-skeleton.py`
- Create: `plugins/python-standards/skills/python-cli/reference/logging-config.py`

**Interfaces:**
- Consumes: the content-input repositories collected in Task 2; entry-point conventions from Task 3 (referenced by skill name, not duplicated).
- Produces: skill name `python-cli` (Tasks 9, 10, 12). Errors/logging standards for CLIs live HERE (spec non-goal: no separate errors/logging skill).

- [ ] **Step 1: Confirm the content input**

Confirm the Task 2 repositories are available in this session; in a fresh session, ask the developer again before authoring.

- [ ] **Step 2: Mine the inputs for CLI conventions**

Read the CLI projects among the inputs: typer app structure, config file handling, logging setup, exit-code discipline, how they are installed. Ask the developer to settle contested points (config format and location, log format).

- [ ] **Step 3: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: python-cli
description: Use when building or extending a Python command-line tool — typer app and command structure, configuration handling, logging setup and error reporting for CLIs, and distribution via uv tool.
---
```

Mandatory content:

- typer as the CLI framework: app/subcommand structure, options vs arguments, help text discipline.
- Config handling: precedence (flags over env over config file), format and location as settled in Step 2.
- Logging and errors for CLIs: logging configuration (pointing at `reference/logging-config.py`), user-facing error messages vs tracebacks, exit codes.
- Distribution via `uv tool install` / `uvx`, wired to the `[project.scripts]` entry point defined per the python-project-layout skill (name the skill, do not restate its content).

- [ ] **Step 4: Write the reference files**

- `reference/cli-skeleton.py`: a complete minimal typer application demonstrating the structure the SKILL.md prescribes — app, one subcommand with an option and an argument, config loading, error-to-exit-code handling.
- `reference/logging-config.py`: the canonical logging setup for a CLI as settled in Step 2, annotated.

- [ ] **Step 5: Validate**

Run: `grep -c '^name: python-cli' plugins/python-standards/skills/python-cli/SKILL.md`
Expected: `1`

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 6: Commit**

```bash
git add plugins/python-standards/skills/python-cli/
git commit -m "feat(python-standards): add python-cli skill"
```

---

### Task 7: python-web-api skill

**Files:**
- Create: `plugins/python-standards/skills/python-web-api/SKILL.md`
- Create: `plugins/python-standards/skills/python-web-api/reference/layering.py`
- Create: `plugins/python-standards/skills/python-web-api/reference/error-handling.py`

**Interfaces:**
- Consumes: the content-input repositories collected in Task 2.
- Produces: skill name `python-web-api` (Tasks 8, 9, 10, 12). Async standards live HERE (spec non-goal: no separate async skill).

- [ ] **Step 1: Confirm the content input**

Confirm the Task 2 repositories are available in this session; in a fresh session, ask the developer again before authoring.

- [ ] **Step 2: Mine the inputs for web-API conventions**

Read the web-service projects among the inputs: router/service/repository layering, pydantic model organization, async usage, error-response shape. Ask the developer to settle contested points (dependency-injection style, error envelope shape).

- [ ] **Step 3: Scaffold and author the skill — TIGHTLY scoped**

Invoke `skill-creator`; follow `superpowers:writing-skills`. The spec scopes this skill tightly: FastAPI layering, pydantic models, async boundaries, HTTP error handling — nothing else (no deployment, no ORM standards, no auth frameworks). Frontmatter exactly:

```yaml
---
name: python-web-api
description: Use when building or extending a FastAPI web service — router, service, and repository layering, pydantic request and response models, async boundaries, and HTTP error handling.
---
```

Mandatory content:

- Layering: router → service → repository, dependency direction, what each layer may import; FastAPI dependency injection at the router layer only.
- pydantic v2 models: request/response models separate from domain objects, validation at the boundary.
- Async boundaries: async route handlers, no blocking IO inside async paths (name the offenders: sync HTTP clients, `time.sleep`, unpooled DB drivers), where sync code is acceptable and how it is offloaded.
- HTTP error handling: exception-to-status mapping, the error envelope settled in Step 2, no stack traces in responses.

- [ ] **Step 4: Write the reference files**

- `reference/layering.py`: a compact router → service → repository example for one resource, annotated with the layer rules it demonstrates.
- `reference/error-handling.py`: exception classes, the exception handler wiring, and the error-envelope model, annotated.

- [ ] **Step 5: Validate**

Run: `grep -c '^name: python-web-api' plugins/python-standards/skills/python-web-api/SKILL.md`
Expected: `1`

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 6: Commit**

```bash
git add plugins/python-standards/skills/python-web-api/
git commit -m "feat(python-standards): add python-web-api skill"
```

---

### Task 8: python-plan-review checklist skill

**Files:**
- Create: `plugins/python-standards/skills/python-plan-review/SKILL.md`

**Interfaces:**
- Consumes: the working-process `*-plan-review` discovery convention (description starts with "Plan-review checklist for <domain>", ends with "invoked by the plan-adversary agent").
- Produces: skill name `python-plan-review` (Task 12's README; Task 13's discovery verification).

- [ ] **Step 0: Confirm contested points with the developer**

Ask the developer to confirm: the severity grades assigned in the checklist below, and the coverage stance (reuse the coverage threshold settled in Task 5 Step 2 — dimension 5 must reference that settled value, not restate its own). This is a skill-content task; the Global Constraints content-input rule applies to it like to Tasks 2–7.

- [ ] **Step 1: Write `plugins/python-standards/skills/python-plan-review/SKILL.md`**

Invoke `skill-creator` for scaffolding; content below is the baseline, amended with the Step 0 outcomes:

```markdown
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
- Coverage-threshold regressions waved through without a decision →
  Minor.
```

- [ ] **Step 2: Validate**

Run: `grep -c '^description: Plan-review checklist for Python' plugins/python-standards/skills/python-plan-review/SKILL.md`
Expected: `1`

Run: `grep -c 'invoked by the plan-adversary agent' plugins/python-standards/skills/python-plan-review/SKILL.md`
Expected: `1`

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 3: Commit**

```bash
git add plugins/python-standards/skills/python-plan-review/
git commit -m "feat(python-standards): add python-plan-review checklist skill"
```

---

### Task 9: Rules payload — rules/python-toolchain.md

**Files:**
- Create: `plugins/python-standards/rules/python-toolchain.md`

**Interfaces:**
- Consumes: skill names from Tasks 2–7 exactly as defined there (conditional pointers only).
- Produces: the Rules payload picked up by working-process's Rules engine (Task 13 verifies the sync-rules install); this makes python-standards a payload plugin.

- [ ] **Step 1: Write `plugins/python-standards/rules/python-toolchain.md`**

```markdown
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
```

No mise content — machine setup is not a code standard (spec non-goal).

- [ ] **Step 2: Hand-check the rule frontmatter**

`claude plugin validate` skips `rules/` — review by hand: the YAML block parses (exactly two `paths` entries, `"**/*.py"` and `"pyproject.toml"`, both quoted), no scalar contains an unquoted `: `.

Run: `head -5 plugins/python-standards/rules/python-toolchain.md`
Expected: the frontmatter block exactly as written above.

- [ ] **Step 3: Validate conditionality**

Run: `grep -c 'When the python-standards plugin' plugins/python-standards/rules/python-toolchain.md`
Expected: `1` (skill mentions are conditional — committed project-level rules load for people without the plugin).

Run: `grep -ci 'mise' plugins/python-standards/rules/python-toolchain.md`
Expected: `0`

- [ ] **Step 4: Commit**

```bash
git add plugins/python-standards/rules/python-toolchain.md
git commit -m "feat(python-standards): add python-toolchain Rules payload"
```

---

### Task 10: python-code-review skill (0.5.0-DEPENDENT)

**Sequencing gate:** before starting, confirm working-process 0.5.0 is released — or its `rules/review-reports.md` content is frozen (present in this repo under `plugins/working-process/rules/`). If neither holds, STOP this task (and Task 11) and continue with any remaining independent task.

**Files:**
- Create: `plugins/python-standards/skills/python-code-review/SKILL.md`

**Interfaces:**
- Consumes: skill names from Tasks 2–7; the Contract probe paths and the canonical filename command from working-process 0.5.0's `rules/review-reports.md`.
- Produces: skill name `python-code-review` and its procedure, consumed verbatim by Task 11's agent and command; the `*-code-review` name pattern a future working-process review orchestrator will discover.

- [ ] **Step 1: Read the frozen contract**

Read working-process 0.5.0's `rules/review-reports.md` (in this repo: `plugins/working-process/rules/review-reports.md`). Extract verbatim: the canonical shell command generating timestamp+runid for report filenames. The inline fallback below must remain a STRICT SUBSET of that contract — if the released rule's frontmatter set or layout differs from the spec's description, the rule wins; adjust the fallback accordingly before writing.

- [ ] **Step 2: Write `plugins/python-standards/skills/python-code-review/SKILL.md`**

Invoke `skill-creator` for scaffolding and description tuning; the content baseline:

```markdown
---
name: python-code-review
description: Use when auditing existing Python code against the python-standards skills — invoked by the /python-review command or the python-code-reviewer agent.
---

# Python code review

Audit Python code against the standards skills of this plugin and write
one Review report per run.

## Run scope

Review Python files only (`*.py` and `pyproject.toml`). Files outside
the domain that fall inside the requested scope are NOT reviewed — list
them in the report's Summary as out of scope.

## Procedure

1. Determine the scope: the current diff by default, or the files named
   by the caller.
2. Load the standards skills relevant to the code under review:
   python-code-style always; python-project-layout, python-typing,
   python-testing, python-cli, python-web-api as the content demands.
3. Grade every finding:
   - **Critical** — a defect that corrupts data, breaks security, or
     crashes the happy path.
   - **Important** — violates a standard in a way that forces rework or
     hides bugs.
   - **Minor** — naming, style, documentation.
   Cite the standard for each finding (`standard: <skill>, rule: <id>`
   where the skill defines rule ids).
4. Write the Review report (next section).
5. Reply with the report path and the findings grouped by severity; a
   zero-findings run still writes the report and states the result.

## Report contract

Run the Contract probe FIRST — do not assume the shared rule is in
context: check, in order,
`<project>/.claude/rules/working-process/review-reports.md`, then
`$HOME/.claude/rules/working-process/review-reports.md`; the first file
found wins. When the Contract probe succeeds, read that file and follow
it fully
— **the installed working-process review-reports rule supersedes the
inline fallback below.**

## Inline fallback (Standalone install)

When the Contract probe finds nothing, this minimal contract applies —
a strict subset of the shared review-reports contract, never a
different shape:

- **Location**: `<project-root>/docs/code-review/`; create the
  directory if absent (the first-create mode question belongs to
  working-process's process-artifacts rule and is absent in a
  Standalone install).
- **Filename**: `<YYYY-MM-DD-HHMMSS>-<scope-slug>-<runid>.md`,
  generated with: <the canonical command copied VERBATIM from the
  released review-reports rule in Step 1>.
- **Frontmatter**: `ticket` (from context or branch, else `none`; never
  block on a question), `standards: python-standards`,
  `findings: { critical: N, important: N, minor: N }` — the counts MUST
  equal the body.
- **Body**: a Summary section (scope reviewed, out-of-scope files,
  headline counts), then per-file sections with Critical → Important →
  Minor subsections, line-ascending within a subsection; omit
  no-findings files and empty severity sections; a zero-findings run
  still writes the document.
- Never stage or commit the report — committing is the developer's
  per-report decision.
- No git root, or the file cannot be written → emit the full report in
  the reply and state why no file was written.
```

Replace the `<the canonical command …>` placeholder with the actual command extracted in Step 1 before saving — the SKILL.md ships with the literal command, byte-identical to the shared contract's.

- [ ] **Step 3: Validate**

Run: `grep -c 'supersedes the' plugins/python-standards/skills/python-code-review/SKILL.md`
Expected: `1` (precedence line present).

Run: `grep -c 'review-reports.md' plugins/python-standards/skills/python-code-review/SKILL.md`
Expected: `2` (both Contract probe paths, project then user order).

Run: `grep -c 'findings: { critical' plugins/python-standards/skills/python-code-review/SKILL.md`
Expected: `1` (shared counts key in the fallback).

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 4: Commit**

```bash
git add plugins/python-standards/skills/python-code-review/
git commit -m "feat(python-standards): add python-code-review skill"
```

---

### Task 11: python-code-reviewer agent and /python-review command (0.5.0-DEPENDENT)

Same sequencing gate as Task 10 (they can run back-to-back once the gate opens).

**Files:**
- Create: `plugins/python-standards/agents/python-code-reviewer.md`
- Create: `plugins/python-standards/commands/python-review.md`

**Interfaces:**
- Consumes: skill name `python-code-review` and its procedure (Task 10) — both surfaces delegate to it, never restate the contract.
- Produces: agent name `python-code-reviewer` and command `/python-review` (Task 12's README; Task 13's verification). One `python-` family per the amended naming rule; agent = actor to the skill's activity.

- [ ] **Step 1: Write `plugins/python-standards/agents/python-code-reviewer.md`**

```markdown
---
name: python-code-reviewer
description: "Reviews Python code — a diff or named files — against the python-standards skills, writes the review report to docs/code-review/, and returns findings by severity. Python files only; out-of-domain files are noted in the report Summary as out of scope."
---

Code reviewer for Python. FIRST ACTION: load the `python-code-review`
skill of this plugin and follow it end to end — run scope, standards
skills, severity grading, the Contract probe, and report writing.

- Review exactly what the dispatch prompt names: the given diff or the
  given files; nothing else.
- One run, one report — this agent is the run's owner (`mode: agent`
  when the shared review-reports contract applies).
- Never stage or commit the report.
- Reply with the report path and the findings grouped Critical →
  Important → Minor; zero findings is still a written report and a
  stated result.
```

- [ ] **Step 2: Write `plugins/python-standards/commands/python-review.md`**

```markdown
---
description: Review the current diff (or named files) against the Python coding standards
---

Review Python code against the python-standards skills.

1. Load the `python-code-review` skill and follow it end to end.
2. Scope: `$ARGUMENTS` when given (named files); otherwise the current
   diff — staged plus unstaged changes, or, on a clean tree, the diff of
   the current branch against its base.
3. Python files only (`*.py`, `pyproject.toml`); note out-of-domain
   files in the report Summary as out of scope.
4. Write the review report per the skill's report contract and reply
   with the report path and findings by severity.
```

- [ ] **Step 3: Validate**

Run: `grep -c '^name: python-code-reviewer$' plugins/python-standards/agents/python-code-reviewer.md`
Expected: `1`

Run: `grep -c 'docs/code-review/' plugins/python-standards/agents/python-code-reviewer.md`
Expected: `1` (report destination named in the agent description).

Run: `grep -c 'python-code-review' plugins/python-standards/agents/python-code-reviewer.md plugins/python-standards/commands/python-review.md | grep -c ':0$'`
Expected: `0` (both surfaces delegate to the skill).

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 4: Commit**

```bash
git add plugins/python-standards/agents/python-code-reviewer.md plugins/python-standards/commands/python-review.md
git commit -m "feat(python-standards): add python-code-reviewer agent and /python-review command"
```

---

### Task 12: Plugin README

**Files:**
- Create: `plugins/python-standards/README.md`

**Interfaces:**
- Consumes: component names and contracts from Tasks 1–11 exactly as defined there.
- GATED with Tasks 10–11 (Global Constraints, Sequencing): the README
  documents the review stack, so it is written only after Task 11.

- [ ] **Step 1: Write `plugins/python-standards/README.md`**

```markdown
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
- **`python-code-reviewer` agent** — reviews a diff or named files, writes
  the report to `docs/code-review/`, returns findings by severity.
- **`/python-review` command** — review the current diff or named files.
  Python files only; out-of-domain files are noted as out of scope.

When the working-process plugin's review-reports rule is installed
(detected by its contract probe), that rule's report contract is
authoritative; without it, the skill's minimal inline fallback applies —
a strict subset of the same contract, so the report shape never depends
on the install profile.

Naming is a deliberate split: skills carry the full `python-` prefix
(triggering surfaces), the agent and the command use the short `py-`
prefix (typed surfaces).

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
```

- [ ] **Step 2: Validate**

Run: `grep -c 'python-code-style\|python-project-layout\|python-typing\|python-testing\|python-cli\|python-web-api\|python-code-review\|python-plan-review\|python-code-reviewer\|python-review' plugins/python-standards/README.md | awk '{print ($1>=10) ? "ok" : "missing components"}'`
Expected: `ok`

Run: `claude plugin validate plugins/python-standards`
Expected: passes.

- [ ] **Step 3: Commit**

```bash
git add plugins/python-standards/README.md
git commit -m "docs(python-standards): add plugin README"
```

---

### Task 13: End-to-end verification

Runs the spec's Verification section. No plugin files change in this task; findings loop back into the task that owns the broken file.

**Files:**
- None created; fixes (if any) modify the owning task's files and follow that task's commit style.

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Structural validation**

Run: `claude plugin validate .` and `claude plugin validate plugins/python-standards` (repo root).
Expected: both pass, no errors.

- [ ] **Step 2: Marketplace-sync check**

Run: `git log --format=%h -1 -- plugins/python-standards/.claude-plugin/plugin.json` and `git show --stat <that-hash>`
Expected: the manifest's landing commit also touches `.claude-plugin/marketplace.json` and `README.md` (catalog entry + README row in the same commit as the manifest).

- [ ] **Step 3: Install from the local marketplace**

In a Claude Code session: `/plugin marketplace add <local path to this repo root>` (already added on this machine — then `/plugin marketplace update missing-bits` instead), `/plugin install python-standards@missing-bits`.
Expected: install succeeds with no dependency resolution (no `dependencies` edge).

- [ ] **Step 4: Component visibility**

In the same session, confirm the skills list shows all eight skills under the plugin namespace (`python-standards:python-code-style`, `-project-layout`, `-typing`, `-testing`, `-cli`, `-web-api`, `-code-review`, `-plan-review`), the agent `python-standards:python-code-reviewer` appears among agent types, and `/python-review` resolves as a command.

- [ ] **Step 5: /python-review — shared contract profile (working-process installed)**

In a scratch git repo containing a small Python diff with a deliberate standards violation (e.g. an unannotated public function plus a blocking call in an async route), with working-process ≥ 0.5.0 installed and its rules installed via sync-rules: run `/python-review`.
Expected: the Contract probe finds `review-reports.md`; the report lands in `docs/code-review/` with the SHARED format (full frontmatter set per the rule, filename from the canonical command); nothing staged.

- [ ] **Step 6: /python-review — Standalone install profile**

Repeat Step 5 under a clean profile (fresh `CLAUDE_CONFIG_DIR`) with ONLY python-standards installed and no working-process rules present.
Expected: the Contract probe finds nothing; the skill creates `docs/code-review/` without asking any mode question; the report carries exactly the fallback frontmatter (`ticket`, `standards: python-standards`, `findings:` counts matching the body) with the Summary and per-file severity layout.

- [ ] **Step 6a: Canonical filename command byte-identity**

Extract the canonical timestamp+runid command from `plugins/python-standards/skills/python-code-review/SKILL.md` and from `plugins/working-process/rules/review-reports.md` (the RELEASED 0.5.0 content, not a frozen draft) and diff them.
Expected: byte-identical — the companion spec makes the command quotable byte-for-byte for permission allowlists. If Tasks 10–11 executed against frozen-but-unreleased content, this step is mandatory after the 0.5.0 release and any difference reopens Task 10.

- [ ] **Step 7: plan-adversary discovery**

Dispatch the working-process plan-adversary agent on any Python-touching plan (this plan qualifies).
Expected: its report shows `python-plan-review` was discovered and loaded as a domain checklist.

- [ ] **Step 8: sync-rules foreign payload install**

In a project with working-process rules installed, run the sync-rules skill after installing python-standards.
Expected: it offers and installs `python-toolchain.md` into the rules target under `rules/python-standards/`; immediately afterwards the drift hook stays silent (manifest hash matches upstream).

- [ ] **Step 9: Record deviations**

Any deviation is a bug in the owning task's file — fix it there, re-run the failed step, and commit the fix as `fix(python-standards): <what>` (single line).

---

### Task 14: Frontmatter closure

**Files:**
- Modify: `docs/specs/2026-07-16-python-standards-design.md` (frontmatter `status` only)
- Modify: `docs/plans/2026-07-16-python-standards.md` (frontmatter `status` only)

**Interfaces:**
- Consumes: Task 13 fully green.

- [ ] **Step 1: Mark the spec and the plan implemented**

With the Edit tool (not shell one-liners), change `status: approved` to `status: implemented` in the spec and `status: draft` (or the then-current value) to `status: implemented` in this plan.

- [ ] **Step 2: Offer the docs commit to the developer**

The repo's `docs/` directories are in tracked mode; the developer commits process documents collectively. List the touched documents (spec, this plan, glossary if the work amended it) and remind that they belong with this work's commits — do NOT commit them unasked; committing stays with the developer.

## Adversary findings — 2026-07-16 round 1

- **Important**: Task 12 (README) was declared gate-independent while
  consuming Tasks 10–11's contracts. → Fixed: Tasks 10–12 now share the
  sequencing gate; Task 12 carries an explicit GATED note.
- **Important**: the fallback's canonical filename command byte-identity
  was asserted but never verified end-to-end. → Fixed: Task 13 Step 6a
  diffs the command between the skill and the RELEASED 0.5.0 rule;
  mandatory re-run when Tasks 10–11 executed against frozen content.
- **Minor**: Task 8 wrote checklist content without the ask-the-developer
  step. → Fixed: Step 0 confirms severity grades and the coverage stance
  (reusing Task 5's settled threshold).
- **Minor**: description disjointness gaps (project-layout↔web-api,
  code-style↔testing). → Fixed: carve-out clauses added to both
  descriptions.
- **Minor**: vacuous `grep -ci 'ty '` verification. → Fixed: greps the
  load-bearing phrase `watched successor`, expected exactly 1.

Round 2 (confirmation pass): all five dispositions verified resolved —
gate/Step 6a consistent, Step 0 is confirmation not invention,
descriptions frontmatter-safe, grep exercises the changed path. No new
findings. Verdict: LGTM.

Amendment (2026-07-17, post-implementation, developer decision): the
`py-` short-prefix split was dissolved — the agent is
`python-code-reviewer`, the command `/python-review`; one `python-`
family throughout, skills named for the activity and the agent for the
actor. All names in this plan were updated in place; the round-1
"prefix drift" finding's historical wording stands as recorded.
Architect consultation on the final names: LGTM (keep all three).

Amendment (2026-07-17, prompt-free filenames): the shared contract
dropped the canonical shell command (working-process 0.6.0 — smoke-test
finding: a permission prompt on every fresh profile). The fallback's
Filename bullet now specifies date-only + model-generated runid; Task 13
Step 6a (byte-identity check) is obsolete — there is no command to
compare. The subset invariant is preserved: both sides changed in the
same release.

Closure record (2026-07-17): Task 13 steps 1, 2, 3, 6a, 8 passed
(structural validation; one-commit registration; local-marketplace
install without dependency resolution; canonical command byte-identity
against the released rule; real user-level Rules-payload install with a
silent drift hook over both manifests). Steps 4–6 (component
visibility, /python-review under the shared-contract and Standalone
profiles) are the developer's smoke test on their Python projects;
step 7 (plan-adversary discovery of python-plan-review) verifies
organically on the next Python-touching plan review. Any smoke-test
finding loops back per Task 13 step 9.
