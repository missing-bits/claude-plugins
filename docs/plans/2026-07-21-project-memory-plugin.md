---
ticket: "#1"
date: 2026-07-21
status: approved
adversary: concerns (resolved 2026-07-21)
branch: feature/1-project-memory-plugin
base: master
---

# project-memory Plugin Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract the project-memory rules pair out of the working-process plugin into a new standalone payload plugin, `plugins/project-memory/` (0.1.0), releasing working-process as 0.9.0.

**Architecture:** A pure-content move with conditional rewording: the two rule files move into a new rules-only plugin whose content no longer assumes the working-process rules are installed, while working-process's remaining references to Project memory become conditional. Distribution stays with the working-process Rules engine (payload plugins never copy the mechanism). No code — every deliverable is a Markdown/JSON file; verification is `claude plugin validate` plus greps.

**Tech Stack:** Claude Code plugin manifests (`plugin.json`, `marketplace.json`), Rules payloads (Markdown with optional YAML `paths:` frontmatter), `claude` CLI for validation.

**Spec:** `docs/specs/2026-07-21-project-memory-plugin-design.md`

**Review rounds:** Plan-adversary, 2026-07-21, Opus 4.8 (prescribed tier for a small mechanical plan): **concerns** — two Minor findings, both resolved inline. (1) Task 5's Private-memory target could silently resolve to the worktree's own empty `.claude/memory/`; the Files entry now directs the write to the main working tree. (2) Task 2 Step 5's catalog insert needed the trailing comma after the `python-standards` entry spelled out; the step now says so.

## Global Constraints

- Public repo: no machine-specific paths, no company/client names, all committed text in English (repo-hygiene rule).
- Commit messages: ONE line, conventional-commit subject (`type:` / `type(scope):`), no body, no trailers.
- `claude plugin validate .` and `claude plugin validate plugins/<name>` must pass before every commit that touches a plugin.
- `claude plugin validate` does NOT check `rules/` — review rule frontmatter by hand; quote any YAML scalar containing `: `.
- A commit/PR that changes any file under `plugins/<name>/` bumps that plugin's version in the same commit/PR: project-memory lands at `0.1.0`, working-process moves `0.8.0 → 0.9.0`.
- Marketplace sync: a new plugin lands with manifest, catalog entry, and repo README row in the SAME commit; `plugin.json` description is canonical, catalog/README may shorten but never contradict.
- The project-memory core rule ships with NO `paths:` frontmatter (always-on, the justified exception); the conventions rule keeps `paths:` for `docs/memory/**` and `.claude/memory/**`.
- All work happens on branch `feature/1-project-memory-plugin` (already exists, based on `master`).

---

### Task 1: Commit the process documents (spec, glossary, this plan)

The spec, the glossary supersessions, and this plan were written during the
design sessions and are still uncommitted. Implementation starts by
committing them.

**Files:**
- Commit (already written): `docs/specs/2026-07-21-project-memory-plugin-design.md`
- Commit (already written): `docs/domain/glossary.md`
- Commit (already written): `docs/plans/2026-07-21-project-memory-plugin.md`

**Interfaces:**
- Consumes: nothing.
- Produces: a clean baseline commit; later tasks' diffs contain only implementation changes.

- [ ] **Step 1: Verify the working tree contains only these three files as changes**

Run: `git status --short`
Expected: exactly `M docs/domain/glossary.md`, `?? docs/plans/2026-07-21-project-memory-plugin.md`, `?? docs/specs/2026-07-21-project-memory-plugin-design.md` (order may differ). Anything else: stop and reconcile before committing.

- [ ] **Step 2: Commit**

```bash
git add docs/domain/glossary.md docs/specs/2026-07-21-project-memory-plugin-design.md docs/plans/2026-07-21-project-memory-plugin.md
git commit -m "docs: spec and plan for the project-memory plugin extraction"
```

---

### Task 2: Create the project-memory plugin and register it

One commit, per the marketplace-sync rule: plugin directory (manifest,
README, both rules), catalog entry, and repo README row land together.

**Files:**
- Create: `plugins/project-memory/.claude-plugin/plugin.json`
- Create: `plugins/project-memory/README.md`
- Create: `plugins/project-memory/rules/project-memory.md`
- Create: `plugins/project-memory/rules/project-memory-conventions.md`
- Modify: `.claude-plugin/marketplace.json` (plugins array)
- Modify: `README.md` (plugin table, after the `python-standards` row)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the plugin name `project-memory` and rule file names `project-memory.md` / `project-memory-conventions.md` that Task 3's conditional references point at.

- [ ] **Step 1: Write `plugins/project-memory/.claude-plugin/plugin.json`**

```json
{
  "name": "project-memory",
  "description": "In-repo project memory for Claude Code sessions — committed Team memory (docs/memory/) and git-ignored per-user Private memory (.claude/memory/), shipped as a Rules payload installed via the working-process sync-rules engine",
  "version": "0.1.0",
  "author": { "name": "Missing Bits (Jacek Nakonieczny)" },
  "license": "MIT",
  "keywords": ["memory", "notes", "ideas", "knowledge", "rules"]
}
```

No `dependencies` field — deliberate; see the spec's Decision section (a declared edge would transitively pull superpowers while still not delivering the rules, since sync-rules is an interactive skill run).

- [ ] **Step 2: Write `plugins/project-memory/rules/project-memory.md`** (always-on core — NO `paths:` frontmatter)

```markdown
# Project memory

An in-repo memory store parallel to Claude Code's home-dir memory, but living
in the project, in two parts:

- **Team memory** — `docs/memory/`, committed, shared with the team.
- **Private memory** — `.claude/memory/`, per-user, always git-ignored.

Each part holds a thin `INDEX.md` (one-line pointers) plus flat topic files.

## Loading

When a part's `INDEX.md` exists, read it at session start and pull a topic
file only when its index line is relevant. If neither `INDEX.md` exists this
rule is a no-op — it never scans, creates, or nags.

## Routing (best-effort)

Project-scoped facts *should* go to Project memory rather than home-dir memory;
home-dir memory keeps cross-project and personal facts and stays auto-loaded,
unchanged. This is best-effort, not enforced: a rule steers, it does not
guarantee. On a miss a fact lands in home-dir memory and can be moved later.

- team-relevant → Team memory;
- per-user → Private memory;
- on collision for a project-scoped fact, the project store wins.

## Adoption

Adoption is opt-in: the store exists only when the developer creates it. Offer
to create it only when the developer signals intent to record something
project-scoped — never proactively. On first creation, point at the
project-memory-conventions rule for the INDEX sections and entry shapes (no
`INDEX.md` yet exists to trigger it).

For Team memory (`docs/memory/`), ask the tracked/ignored question before
writing anything — this rule owns that question:

- **Ignored**: write a `.gitignore` containing exactly `*` into
  `docs/memory/`; its contents stay out of the repo.
- **Tracked**: files are committed like any other; no `.gitignore` is
  written.

Never ask when a prior decision is observable: a `.gitignore` containing
exactly `*` means ignored was chosen; any git-tracked file under the
directory means tracked. Private memory (`.claude/memory/`) is always
ignored, so it is never asked. When the working-process rules are installed,
`docs/memory/` additionally counts as a Process directory there.

Entry shapes, team-memory scope, and the lifecycle live in the
project-memory-conventions rule, which loads when you touch a memory file.
```

- [ ] **Step 3: Write `plugins/project-memory/rules/project-memory-conventions.md`**

```markdown
---
paths:
  - "docs/memory/**"
  - ".claude/memory/**"
---

# Project memory — conventions

## Locations

- **Team memory** `docs/memory/` — the tracked/ignored question applies,
  asked by the project-memory core rule. It may start ignored to defer the
  commit; the flip to tracked is a manual, unprompted developer action (a
  `*`-only `.gitignore` self-ignores, so flipping means deleting it or
  force-adding — which Claude never does or suggests). When the
  working-process rules are installed, the directory counts as a Process
  directory there.
- **Private memory** `.claude/memory/` — always git-ignored (`.gitignore`
  containing exactly `*`), never asked: a per-user store under the
  `.claude/` config namespace.

`INDEX.md` is sectioned per part: a **Notes** section (recall-on-demand) and
an **Ideas** section (a browsable backlog). The Ideas section lists each entry
in its lifecycle state: parked (a link to its `idea-` file), spec'd (a redirect
line to the spec, no file), or dropped (a struck-through tombstone with the
reason).

## Entry shapes

Shape, not topic, is the criterion; the `idea-` prefix is authoritative (the
INDEX section and frontmatter follow it).

- **note** (no prefix) — a gotcha or cross-ticket state; a cross-ticket
  registry, exempt from any per-work `ticket` convention the project keeps.
  It may carry an optional `adr-candidate: yes` frontmatter flag — presence
  marks a decision-shaped note for later ADR review
  (`rg 'adr-candidate:'`); absent means not a candidate.
- **idea** (`idea-<slug>.md`) — a parked idea. Frontmatter: `status`
  (parked → spec'd | dropped), a `spec:` pointer once it graduates, and —
  when the project links documents to its issue tracker (e.g. the
  working-process ticket-frontmatter convention) — `ticket`.

## Team-memory scope

Team memory owns only parked ideas, cross-ticket initiative state, and
operational gotchas. Route elsewhere — each target only where the project
keeps it (e.g. via working-process):

- a decision with a rationale and a real trade-off → an ADR
  (`docs/domain/adr/`), when the project records ADRs;
- a canonical term or `_Avoid_` ban → the domain glossary, when the project
  keeps one;
- the todo/steps of one task → that work's plan;
- a unit of work tracked in the issue tracker → the `ticket`;
- any per-user fact → Private memory or home-dir memory.

Without such a target, an entry simply stays a note.

## gotcha vs ADR

Default every entry to a note. When an entry is decision-shaped — hard to
reverse AND surprising without context AND a real trade-off existed — and
the project records ADRs, offer to promote it to an ADR; the developer
decides. A promoted note links to its ADR.

## Lifecycle — no empty files

A body file exists only while it holds live content; never leave an empty or
stub file.

- **Promotion** (content moves to a spec, ADR, or the glossary): delete the
  body file, and turn its `INDEX.md` line into a redirect pointer to the new
  home. Redirect lines are sweepable.
- **Dropped** (abandoned, nothing else records it): no body file — a one-line
  `INDEX.md` tombstone with the reason.
- **Obsolete** (no longer true, no document to point at): delete the body file
  and its index line.
```

- [ ] **Step 4: Write `plugins/project-memory/README.md`**

```markdown
# project-memory

An in-repo memory store for Claude Code sessions, parallel to the built-in
home-dir memory but living in the project, in two parts:

- **Team memory** — `docs/memory/`, committed, shared with the team. Holds
  team-relevant parked ideas, cross-ticket state, and operational gotchas.
- **Private memory** — `.claude/memory/`, per-user, always git-ignored.

Each part holds a thin `INDEX.md` (one-line pointers) plus flat topic
files: the index loads at session start, topic files are pulled only when
relevant.

## Rules

The plugin ships two rule files as a Rules payload:

- `project-memory.md` — the always-on core: loads each part's `INDEX.md`
  at session start, routes project-scoped facts to the store (best-effort)
  instead of home-dir memory, and owns Team memory's tracked/ignored
  first-create question. Always-on deliberately: index loading has no file
  path to scope on.
- `project-memory-conventions.md` — paths-scoped to the two store
  directories: note/idea entry shapes, team-memory scope, the gotcha↔ADR
  promotion offer, and the no-empty-files lifecycle.

Adoption is opt-in: without an `INDEX.md` the core rule is a no-op — it
never scans, creates, or nags. The store exists only once you create it.

## Installation

Claude Code does not load plugin rules by itself. The payload is installed
by the working-process plugin's Rules engine:

1. `/plugin install project-memory@missing-bits`
2. `/plugin install working-process@missing-bits` (brings the engine)
3. Run the `working-process:sync-rules` skill and pick this payload.

The engine dependency is operational only — it installs and updates the
rule files. The rules' content does not require the working-process
*rules*: without them there is simply no Process-directory ceremony beyond
the core rule's own tracked/ignored question, no ADR/glossary promotion
offers, and no `ticket` frontmatter on idea entries. With them, `docs/memory/`
counts as a Process directory and the routing targets light up.
```

- [ ] **Step 5: Add the catalog entry to `.claude-plugin/marketplace.json`**

Append to the `plugins` array. The `python-standards` object is currently the LAST array element and has no trailing comma — add a comma after its closing brace, then insert:

```json
    {
      "name": "project-memory",
      "source": "./plugins/project-memory",
      "description": "In-repo project memory: committed Team memory and git-ignored per-user Private memory, shipped as a Rules payload installed via working-process sync-rules"
    }
```

- [ ] **Step 6: Add the plugin-table row to the repo root `README.md`**

After the `python-standards` row:

```markdown
| `project-memory` | In-repo project memory: committed Team memory (`docs/memory/`) and per-user Private memory (`.claude/memory/`), distributed as a Rules payload |
```

- [ ] **Step 7: Validate**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory`
Expected: both print `Validation passed`.

Hand-check the rule frontmatter (validate does not cover `rules/`): the core rule has NO frontmatter; the conventions rule's frontmatter contains only the `paths:` block with the two globs; no unquoted `: ` inside any YAML scalar.

- [ ] **Step 8: Commit**

```bash
git add plugins/project-memory .claude-plugin/marketplace.json README.md
git commit -m "feat(project-memory): extract the project-memory rules into their own plugin"
```

---

### Task 3: Remove the pair from working-process and make its references conditional

**Files:**
- Delete: `plugins/working-process/rules/project-memory.md`
- Delete: `plugins/working-process/rules/project-memory-conventions.md`
- Modify: `plugins/working-process/rules/process-artifacts.md`
- Modify: `plugins/working-process/rules/ticket-frontmatter.md`
- Modify: `plugins/working-process/README.md`
- Modify: `plugins/working-process/.claude-plugin/plugin.json` (version only)

**Interfaces:**
- Consumes: the plugin name `project-memory` and its two rule file names from Task 2.
- Produces: working-process 0.9.0 with five payload rules; conditional wording other tasks do not touch.

- [ ] **Step 1: Delete the two rule files**

```bash
git rm plugins/working-process/rules/project-memory.md plugins/working-process/rules/project-memory-conventions.md
```

- [ ] **Step 2: Edit `plugins/working-process/rules/process-artifacts.md`**

Three edits (use the Edit tool):

(a) In the opening paragraph, replace:

```
`docs/domain/`, `docs/code-review/`, `docs/memory/` (Team memory), and the
`.superpowers/` family at the repo root.
```

with:

```
`docs/domain/`, `docs/code-review/`, `docs/memory/` (Team memory — when the
project-memory plugin's rules are installed), and the `.superpowers/` family
at the repo root.
```

(b) Replace the paragraph:

```
`docs/memory/`'s tracked/ignored first-create question is asked by the
project-memory core rule, not this one — it is listed above only so
`docs/memory/` counts as a Process directory for the conventions below.
```

with:

```
`docs/memory/`'s tracked/ignored first-create question is asked by the
project-memory plugin's core rule (when installed), not this one — it is
listed above only so `docs/memory/` counts as a Process directory for the
conventions below.
```

(c) In the "Handling artifacts" bullet, replace:

```
  across tickets (the domain glossary, `.gitignore` files, Project memory
  notes and `INDEX.md`) are exempt. Project-memory idea entries DO carry
  `ticket` and are not exempt. Team memory (`docs/memory/`) is a Process
  directory; Private memory (`.claude/memory/`) is not — it is the
  per-user store defined by the project-memory rule.
```

with:

```
  across tickets (the domain glossary, `.gitignore` files, and — when the
  project-memory plugin's rules are installed — Project memory notes and
  `INDEX.md`) are exempt. Project-memory idea entries DO carry `ticket`
  and are not exempt. Team memory (`docs/memory/`) is a Process
  directory; Private memory (`.claude/memory/`) is not — it is the
  per-user store defined by the project-memory plugin's rules.
```

- [ ] **Step 3: Edit `plugins/working-process/rules/ticket-frontmatter.md`**

Replace the Project memory bullet:

```
- Project memory (`docs/memory/`, `.claude/memory/`): notes and `INDEX.md`
  are `ticket`-exempt registry files (like the glossary); idea entries
  (`idea-*.md`) carry `ticket`. See the project-memory-conventions rule.
```

with:

```
- Project memory (`docs/memory/`, `.claude/memory/` — when the
  project-memory plugin's rules are installed): notes and `INDEX.md`
  are `ticket`-exempt registry files (like the glossary); idea entries
  (`idea-*.md`) carry `ticket`. See that plugin's
  project-memory-conventions rule.
```

- [ ] **Step 4: Edit `plugins/working-process/README.md`**

Three edits:

(a) In "## Process rules", replace:

```
The plugin ships seven rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, ticket frontmatter, the review-report
contract (`review-reports.md`: where a code-review run writes its
Review report and what shape it takes; domain review skills locate the
installed contract via its contract probe — the project-level then
user-level install path, in that order), and the project memory pair
(`project-memory.md`, always-on core; `project-memory-conventions.md`,
paths-scoped conventions — see "Project memory" below). Claude Code
does not load plugin rules by itself: install them with the
`working-process:sync-rules` skill.
```

with:

```
The plugin ships five rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, ticket frontmatter, and the review-report
contract (`review-reports.md`: where a code-review run writes its
Review report and what shape it takes; domain review skills locate the
installed contract via its contract probe — the project-level then
user-level install path, in that order). Claude Code
does not load plugin rules by itself: install them with the
`working-process:sync-rules` skill.
```

(b) In "## Process directories", replace:

```
This plugin creates two directories in a project repo: `docs/domain/`
(glossary + ADRs) and `docs/code-review/` (Review reports — one per
code-review run, shape defined by the review-reports rule) — plus
`docs/memory/` (Team memory) once you adopt Project memory. On first
```

with:

```
This plugin creates two directories in a project repo: `docs/domain/`
(glossary + ADRs) and `docs/code-review/` (Review reports — one per
code-review run, shape defined by the review-reports rule). On first
```

(c) Replace the whole "## Project memory" section (heading plus its one paragraph, currently the last section of the file):

```
## Project memory

An in-repo memory store, in two parts: **Team memory** (`docs/memory/`,
committed) and **Private memory** (`.claude/memory/`, per-user, git-ignored).
Each holds a thin `INDEX.md` plus flat topic files. Two rules ship it: an
always-on core (`project-memory.md`) that loads the index and routes
project-scoped facts to the store (best-effort) instead of home-dir memory,
and a paths-scoped conventions rule (`project-memory-conventions.md`) with the
note/idea entry shapes, team-memory scope, gotcha↔ADR offer, and the
no-empty-files lifecycle. Adoption is opt-in — the store exists only once you
create it.
```

with:

```
## Project memory

The in-repo Project memory store ships as its own plugin, `project-memory`
— a Rules payload this plugin's engine installs and updates like any
other. When its rules are installed alongside these, `docs/memory/` (Team
memory) counts as a Process directory and memory entries follow the
`ticket` conventions above.
```

(d) One consistency check, no blind edit: `grep -n "docs/memory" plugins/working-process/README.md` — any hit outside the "## Project memory" section gets the same conditional treatment as (a)/(b); expected remaining hits after (a)–(c): only inside the new "## Project memory" section.

- [ ] **Step 5: Bump the version in `plugins/working-process/.claude-plugin/plugin.json`**

Change only:

```json
  "version": "0.8.0",
```

to:

```json
  "version": "0.9.0",
```

The description stays unchanged — it never named the memory pair (spec, Review rounds finding 3).

- [ ] **Step 6: Validate and grep for leftovers**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass.

Run: `grep -rn "project-memory" plugins/working-process/`
Expected: hits ONLY in `rules/process-artifacts.md`, `rules/ticket-frontmatter.md`, and `README.md`, all inside "when … installed"-style conditional sentences. No hits in `skills/`, `agents/`, `hooks/`, `scripts/`.

Run: `ls plugins/working-process/rules/`
Expected: exactly `process-artifacts.md  review-reports.md  spec-plan-lifecycle.md  ticket-frontmatter.md  workflow.md` (five files).

- [ ] **Step 7: Commit**

```bash
git add -A plugins/working-process
git commit -m "feat(working-process): drop the project-memory pair in favour of the project-memory plugin"
```

---

### Task 4: Update the repo-internal authoring rule

**Files:**
- Modify: `.claude/rules/plugin-authoring.md`

**Interfaces:**
- Consumes: the plugin name `project-memory` from Task 2.
- Produces: nothing downstream; keeps the repo's own conventions truthful.

- [ ] **Step 1: Edit the always-on standing-instances sentence**

In `.claude/rules/plugin-authoring.md`, "Rules payload" section, replace:

```
  always-on (no `paths:`) so they fire every session — `workflow.md` and
  the project-memory core rule are the standing instances. The `paths:`-
```

with:

```
  always-on (no `paths:`) so they fire every session — working-process's
  `workflow.md` and the project-memory plugin's core rule are the standing
  instances. The `paths:`-
```

- [ ] **Step 2: Commit**

```bash
git add .claude/rules/plugin-authoring.md
git commit -m "chore: attribute the always-on rules exception to the project-memory plugin"
```

---

### Task 5: Annotate the parked idea (Private memory — no commit)

**Files:**
- Modify: `.claude/memory/idea-first-create-question-owner.md` — in the MAIN working tree's Private memory (git-ignored). A git worktree is itself a repo root and its own `.claude/memory/` is empty, so resolve the path against the main working tree (the directory `git worktree list` prints first), never against the worktree — a write to the wrong copy fails silently (ignored file: no diff, no status change).

**Interfaces:**
- Consumes: nothing.
- Produces: nothing downstream; keeps the parked general-fix idea aware of both copies of the first-create semantics (spec, "Conscious duplication" section).

- [ ] **Step 1: Append one paragraph to the idea file**

Append to `.claude/memory/idea-first-create-question-owner.md`:

```markdown
Update 2026-07-21 (project-memory extraction, ticket #1): the memory-side
copy of the tracked/ignored semantics now lives in the project-memory
plugin's core rule — the general fix has two places to clean up
(working-process `process-artifacts.md` + project-memory `project-memory.md`).
```

No commit — Private memory is git-ignored.

---

### Task 6: Final verification sweep

**Files:** none created or modified; read-only checks.

**Interfaces:**
- Consumes: everything above.
- Produces: the evidence for claiming the work done.

- [ ] **Step 1: Validate everything**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory && claude plugin validate plugins/working-process && claude plugin validate plugins/python-standards`
Expected: all pass.

- [ ] **Step 2: Marketplace-sync consistency**

Run: `grep -n "project-memory" .claude-plugin/marketplace.json README.md plugins/project-memory/.claude-plugin/plugin.json`
Expected: the name string `project-memory` present in all three; descriptions consistent (catalog/README shorten the manifest's, never contradict it).

- [ ] **Step 3: Repo hygiene**

Run: `grep -rn "/home/" plugins/project-memory/ docs/specs/2026-07-21-project-memory-plugin-design.md docs/plans/2026-07-21-project-memory-plugin.md`
Expected: no hits (no machine-specific paths in committed files).

- [ ] **Step 4: Rule-count and stale-reference greps**

Run: `grep -rn "seven rule" plugins/`
Expected: no hits.

Run: `grep -rln "project memory pair" plugins/`
Expected: no hits.

- [ ] **Step 5: Report**

Summarize commits and validation results to the developer. Do NOT push, do NOT open a PR, do NOT run sync-rules on any machine — each needs its own explicit authorization; the spec also defers the developer's own installed-rules sync to a post-release step.
