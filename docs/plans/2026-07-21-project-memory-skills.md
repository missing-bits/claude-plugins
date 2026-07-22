---
ticket: "#1"
date: 2026-07-21
status: implemented
adversary: concerns (resolved 2026-07-21)
branch: feature/1-project-memory-plugin
base: master
---

# project-memory 0.2.0 — Grooming Skills and Archive Format Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship project-memory 0.2.0 — two skills (`memory-review-session`, `migrate-memory`) and a store-format change (live-only `INDEX.md`, on-demand `ARCHIVE.md`, no `dropped/`).

**Architecture:** A rules-only plugin gains its first two skills plus edits to its two rule files. No executable code — every deliverable is Markdown (SKILL.md, rule files) or JSON (manifest, catalog). "Tests" are `claude plugin validate`, hand review of rule/skill frontmatter, conditionality greps, and skill-creator trigger evals (deferrable under a spend cap).

**Tech Stack:** Claude Code skills (SKILL.md with YAML frontmatter), Rules payloads (Markdown, optional `paths:`), `plugin.json`/`marketplace.json`, `claude` CLI, skill-creator for eval authoring.

**Spec:** `docs/specs/2026-07-21-project-memory-skills-design.md` (grilled, architect concerns resolved).

## Global Constraints

- Public repo: no machine-specific paths (`/home/<user>/…`), no company or client names, all committed text English.
- Commit messages: ONE line, conventional-commit subject (`type:`/`type(scope):`), no body, no trailers (no `Co-Authored-By`).
- This whole branch is ONE PR; the plugin version bumps once for the PR: project-memory `0.1.0 → 0.2.0` — minor via the 0.x rule (the store-format rewrite is breaking for existing stores; pre-1.0.0 breaking rides a minor), done in the packaging task (Task 5).
- Marketplace-sync: a plugin's name/description lives in three places — `plugin.json` (canonical), the `marketplace.json` catalog entry, and the repo `README.md` row. A description change touches all three in the SAME commit.
- `claude plugin validate .` and `claude plugin validate plugins/project-memory` must pass before each commit touching the plugin. `validate` does NOT check `rules/` or `skills/` frontmatter — review those by hand; quote any YAML scalar containing `: `.
- The core rule (`project-memory.md`) ships with NO `paths:` frontmatter (always-on); the conventions rule keeps `paths:` for `docs/memory/**`, `.claude/memory/**`.
- working-process is OUT OF SCOPE — no edits, no bump. The `ARCHIVE.md` ticket-exemption is delivered by the conventions rule (paths-scoped to `docs/memory/**`), to which working-process's `ticket-frontmatter` bullet delegates.
- `dropped/` does NOT exist — the architect review removed it. A drop leaves a one-line archive record; a body worth keeping promotes to an ADR or stays a live note.

## Review rounds

- **Plan-adversary**, 2026-07-21, **Opus 4.8** — the prescribed tier for a
  small mechanical plan (one family below the most capable), not a fallback.
  Verdict **concerns**: one Important, four Minor, all resolved inline.
  1. Important — a deferred eval RUN left trigger quality unverified
     ("parses" ≠ "triggers"). Resolved: Task 6 now gates on a lightweight
     inline trigger check (always runnable, no subagents) as the done-gate,
     with the full skill-creator harness deferrable and, if deferred, tracked
     as owed rather than silently skipped.
  2. Minor — Task 6 commit ran no `validate`; added a `validate` step (Task 6
     Step 4).
  3. Minor — `git add plugins/project-memory/skills` could miss scaffold
     output written elsewhere; Task 6 Step 4 now confirms staged paths via
     `git status` and stages the real path.
  4. Minor — Task 5 left the plugin README intro and a conventions bullet
     describing the 0.1.0 layout; Task 5 Step 4 now updates both.
  5. Minor — the conventions Entry-shapes idea bullet still implied a live
     `spec:` pointer after graduation; Task 2 Step 5 adds a closure clause
     (without touching the frozen Idea-entry frontmatter set).

---

### Task 1: Commit the process documents

**Files:**
- Commit (already written): `docs/specs/2026-07-21-project-memory-skills-design.md`
- Commit (already modified): `docs/domain/glossary.md`
- Commit (already written): `docs/plans/2026-07-21-project-memory-skills.md`
- Commit (already modified): `.claude/rules/repo-hygiene.md` — the quoted-trigger-phrase exception codified during the Fable architect re-review

**Interfaces:**
- Consumes: nothing.
- Produces: a clean baseline; later task diffs contain only implementation.

- [ ] **Step 1: Verify the working tree holds only these four as changes**

Run: `git status --short`
Expected: `M docs/domain/glossary.md`, `M .claude/rules/repo-hygiene.md`, `?? docs/plans/2026-07-21-project-memory-skills.md`, `?? docs/specs/2026-07-21-project-memory-skills-design.md` (order may vary). Anything else → stop and reconcile.

- [ ] **Step 2: Commit — docs first, then the rule tweak**

```bash
git add docs/domain/glossary.md docs/specs/2026-07-21-project-memory-skills-design.md docs/plans/2026-07-21-project-memory-skills.md
git commit -m "docs: spec and plan for project-memory 0.2.0 grooming skills"
git add .claude/rules/repo-hygiene.md
git commit -m "chore: allow quoted non-English trigger phrases in skill descriptions"
```

---

### Task 2: Rewrite the store-format rules

Applies the format change to both rule files. The conventions rewrite **replaces** the Ideas-section description and the entire Lifecycle section — no appended contradiction.

**Files:**
- Modify: `plugins/project-memory/rules/project-memory-conventions.md`
- Modify: `plugins/project-memory/rules/project-memory.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the `ARCHIVE.md` (Done/Dropped) format, the INDEX-is-live-only invariant, and the closure routing that both skills apply.

- [ ] **Step 1: Replace the INDEX-sectioning paragraph in `project-memory-conventions.md`**

Replace (lines 22-26, the `INDEX.md is sectioned…` paragraph):

```
`INDEX.md` is sectioned per part: a **Notes** section (recall-on-demand) and
an **Ideas** section (a browsable backlog). The Ideas section lists each entry
in its lifecycle state: parked (a link to its `idea-` file), spec'd (a redirect
line to the spec, no file), or dropped (a struck-through tombstone with the
reason).
```

with:

```
`INDEX.md` holds only **live** entries, sectioned per part: a **Notes**
section (active notes, recall-on-demand) and an **Ideas** section (only
`parked` ideas, each a link to its `idea-` file). Closed entries — promoted,
finished, or dropped — do not live here; they move to `ARCHIVE.md` the moment
they close (see Lifecycle). `INDEX.md` is the only file read at session start,
so it never carries history.
```

- [ ] **Step 2: Add the Locations bullet for `ARCHIVE.md`**

In `project-memory-conventions.md`, after the Private memory bullet (line 20, before the INDEX paragraph), add a third Locations bullet:

```
- **Archive** `ARCHIVE.md` (per part) — the closed-entry record: one line per
  closed entry, in a **Done** or **Dropped** section. Read on demand only
  (e.g. answering "did we already consider this?"), never at session start. A
  `ticket`-exempt registry file like `INDEX.md`.
```

- [ ] **Step 3: Replace the Lifecycle section with closure routing**

Replace the whole `## Lifecycle — no empty files` section (lines 66-77) with:

```
## Lifecycle — closing entries

A live entry keeps a body only while it holds live content; a closed entry
keeps no body, only a one-line `ARCHIVE.md` record. The governing test: a
body survives closure only when no other artifact carries its content.

- **Promotion** (content moves to a spec, ADR, or the glossary): delete the
  body; move the `INDEX.md` line to `ARCHIVE.md` **Done** as a redirect
  pointer to the new home.
- **Closed note** (a work-state note after its release, an expired gotcha
  whose resolution now lives in code or docs): delete the body; write an
  `ARCHIVE.md` **Done** line naming where the detail now lives (spec/plan,
  release version, optionally a commit) plus the closure date. If a fragment
  has no home in any document, the entry is not yet closed — or that fragment
  becomes the Done line.
- **Dropped** (abandoned): write an `ARCHIVE.md` **Dropped** line — reason
  plus date — and delete the body. There is no body-retention directory: if
  the rejection analysis is worth keeping, that is the signal the entry is
  decision-shaped (offer an ADR — "rejected X because Y" — when the project
  records ADRs) or reference-shaped (keep it a live note); a kept body is
  then not dropped.
- **Obsolete** (no longer true, nothing worth pointing at): delete the body
  and its index line — no `ARCHIVE.md` record.

Never leave an empty or stub body file. `INDEX.md` and `ARCHIVE.md` are
registry files, not bodies: an empty section header in either is fine.
```

- [ ] **Step 4: Update the parts description in `project-memory.md` (core)**

Replace line 9:

```
Each part holds a thin `INDEX.md` (one-line pointers) plus flat topic files.
```

with:

```
Each part holds a thin `INDEX.md` (one-line pointers to live entries) plus
flat topic files, and an `ARCHIVE.md` of closed-entry lines read on demand —
never at session start.
```

- [ ] **Step 5: Reconcile the Entry-shapes idea bullet with the new lifecycle**

The Entry-shapes section still says an idea carries "a `spec:` pointer once it graduates" — but under the new Promotion routing a graduated idea has no live body. Do NOT change the frozen frontmatter set (the spec kept Idea-entry frontmatter unchanged); only add a closure clause. In `project-memory-conventions.md`, replace the idea bullet:

```
- **idea** (`idea-<slug>.md`) — a parked idea. Frontmatter: `status`
  (parked → spec'd | dropped), a `spec:` pointer once it graduates, and —
  when the project links documents to its issue tracker (e.g. the
  working-process ticket-frontmatter convention) — `ticket`.
```

with:

```
- **idea** (`idea-<slug>.md`) — a `parked` idea (a live entry). Frontmatter:
  `status` (parked → spec'd | dropped), a `spec:` pointer once it graduates,
  and — when the project links documents to its issue tracker (e.g. the
  working-process ticket-frontmatter convention) — `ticket`. On graduation or
  drop the body closes per the Lifecycle section; the `spec:` pointer then
  lives on the `ARCHIVE.md` Done redirect line, not a live file.
```

- [ ] **Step 6: Verify the rules render cleanly**

Run: `sed -n '9,30p' plugins/project-memory/rules/project-memory-conventions.md`
Expected: three Locations bullets (Team, Private, Archive) then the live-only INDEX paragraph; no surviving "struck-through tombstone" or "lifecycle state" wording.

Run: `grep -n "dropped/\|struck-through\|lifecycle state" plugins/project-memory/rules/`
Expected: no hits.

Hand-check frontmatter: `project-memory.md` still has NO frontmatter; `project-memory-conventions.md` still has only the `paths:` block.

- [ ] **Step 7: Commit**

```bash
git add plugins/project-memory/rules
git commit -m "feat(project-memory): live-only INDEX and an on-demand ARCHIVE format"
```

---

### Task 3: Add the memory-review-session skill

**Files:**
- Create: `plugins/project-memory/skills/memory-review-session/SKILL.md`

**Interfaces:**
- Consumes: the closure routing and `ARCHIVE.md` format from Task 2.
- Produces: the grooming skill; no later task depends on its internals.

- [ ] **Step 1: Write `SKILL.md`**

Write `plugins/project-memory/skills/memory-review-session/SKILL.md` exactly:

```markdown
---
name: memory-review-session
description: "Grooming session for a Project-memory store: audits INDEX/ARCHIVE consistency, then walks entries toward their correct lifecycle state — closing finished notes, promoting or dropping ideas, splitting or merging, sharpening index lines. Use ONLY when the developer explicitly asks to review or tidy Project memory (\"groom the store\", \"memory review\", \"przejrzyjmy memory\"). A routine memory read or write, or a question about an entry's content, is NOT a trigger."
---

# memory-review-session

An explicit-ask grooming conversation over a Project-memory part
(`docs/memory/` or `.claude/memory/`). The store's analogue of a
grilling-session: it applies the conventions rule's lifecycle, defining
nothing new, and recommends — it never bulk-cleans. Every deletion or closure
is per-entry consent; edits land inline as decisions are made. Never commits.

## When it runs

Only on a direct request to review or tidy the store. Routine memory
reads/writes and questions about an entry's content do NOT start a session —
mirroring the core rule's "never scans, creates, or nags" stance.

## Opening audit (mechanical)

From `INDEX.md` plus a directory listing, surface the worklist:

- dangling `INDEX.md` links (a line pointing at a missing file);
- body files with no `INDEX.md` line;
- empty or stub body files (a lifecycle violation);
- `idea-*` files whose `status` is `spec'd` or `dropped` but that still sit as
  live bodies;
- **sweep**: any closed line still in `INDEX.md` (legacy, or a botched close)
  moves to `ARCHIVE.md`. Under the invariant this should be empty; the sweep
  is the safety net.

## Entry walk (ordered, existential first)

One entry at a time, a recommendation with each:

1. **Should this entry exist at all?** Untrue → obsolete (delete, no archive
   line). Realized or subsumed by a spec, plan, glossary, or ADR → close with
   a Done line. This is how a released work-state note leaves the store.
2. **Is it in the right part?** team ↔ private rebalance.
3. **Is it the right size and shape?** split an overgrown note, trim it, merge
   duplicates; a note that has grown into a mini-spec is a candidate for a
   real spec, not a longer note.
4. **Does the `INDEX.md` line summarize it well?** Recall depends on the
   one-liner — the cheapest tidiness there is.

## adr-candidate flags

Review notes carrying `adr-candidate: yes`. When a grilling-session is
available, offer a handoff to it for the promotion (it writes the ADR, not
this session). Without it, the flag simply stays and the session notes it and
moves on.

## Ideas section

Long-parked ideas → confirm still worth keeping, or drop (a Dropped line with
the reason). `spec'd` ideas → close the redirect to their spec.

## Boundaries

Applies the project-memory-conventions lifecycle; defines nothing new. Never
commits (committing stays with the developer). Recommends per entry — no bulk
deletion. Grilling-session, ADR, and glossary mentions above are conditional:
act on them only when those tools/artifacts are present.
```

- [ ] **Step 2: Hand-check the frontmatter**

Run: `sed -n '1,4p' plugins/project-memory/skills/memory-review-session/SKILL.md`
Expected: the `description:` value is DOUBLE-QUOTED (it contains `: ` and embedded quotes escaped as `\"`), `name: memory-review-session` matches the directory.

Run: `claude plugin validate plugins/project-memory`
Expected: `Validation passed`.

- [ ] **Step 3: Commit**

```bash
git add plugins/project-memory/skills/memory-review-session
git commit -m "feat(project-memory): add memory-review-session grooming skill"
```

---

### Task 4: Add the migrate-memory skill

**Files:**
- Create: `plugins/project-memory/skills/migrate-memory/SKILL.md`

**Interfaces:**
- Consumes: the core rule's adoption + routing, the conventions rule's entry shapes.
- Produces: the migration skill; no later task depends on its internals.

- [ ] **Step 1: Write `SKILL.md`**

Write `plugins/project-memory/skills/migrate-memory/SKILL.md` exactly:

```markdown
---
name: migrate-memory
description: "Move project-scoped facts about the current repo out of Claude Code's home-dir memory and into this project's Project-memory store (one direction, home-dir → project), routing each to Team or Private memory. Use ONLY when the developer explicitly asks to migrate or move their notes into the project (\"migrate memory\", \"move my notes to the project\", \"przenieś notatki do projektu\"). Not for team↔private rebalancing (that is memory-review-session) and not a routine memory write."
---

# migrate-memory

An operational skill that repairs routing: home-dir memory is where
project-scoped facts land on a miss, and this is the "moved later" the
core rule promises. One direction only — home-dir → project. Never commits.

## When it runs

Only on a direct request to migrate notes into the project. team ↔ private
rebalancing belongs to memory-review-session; a routine memory write is not a
trigger.

## Scan

Read home-dir memory (`MEMORY.md` plus its entry files). Candidates are facts
**project-scoped to the current repo**, judged by content. Cross-project and
personal facts stay in home-dir memory — do not propose them. When a fact's
scope is unclear, ask; never guess.

## No store yet → offer adoption

If the project has no store, running this skill IS the signal of intent the
core rule requires: offer to create a part. Carry the tracked/ignored
first-create question for Team memory (Private is never asked — always
ignored). Declining adoption ends the skill with no writes.

## Per fact

Recommend move or leave. For a move, route per the core rule: team-relevant →
Team memory, per-user → Private memory. The developer decides each.

## Move mechanics

- Translate shape: a home-dir entry (`name`/`description`/`metadata`
  frontmatter) becomes a **note** or an `idea-<slug>.md` per the conventions
  rule — shape is the criterion, the `idea-` prefix authoritative.
- Add the entry's line to the target part's `INDEX.md`.
- Delete the home-dir body file and its `MEMORY.md` line.
- `ticket` frontmatter on a migrated idea only when the project keeps that
  convention (e.g. via working-process).

## Collision

If a fact already has a counterpart in the project store, the project store
wins: offer to merge into the project entry and remove the home-dir copy.

## Migration trace

After moving one or more facts, leave a single roll-up line in home-dir
`MEMORY.md` — "project-scoped notes for <repo> migrated to its Project
memory, <date>" — not a per-entry pointer.

## Boundaries

One direction only. Never commits. Works without working-process — the
`ticket` convention applies only when the project keeps it.
```

- [ ] **Step 2: Hand-check the frontmatter**

Run: `sed -n '1,4p' plugins/project-memory/skills/migrate-memory/SKILL.md`
Expected: `description:` DOUBLE-QUOTED (contains `: ` and escaped quotes), `name: migrate-memory` matches the directory.

Run: `claude plugin validate plugins/project-memory`
Expected: `Validation passed`.

- [ ] **Step 3: Commit**

```bash
git add plugins/project-memory/skills/migrate-memory
git commit -m "feat(project-memory): add migrate-memory home-dir-to-project skill"
```

---

### Task 5: Packaging — version, description, catalog, READMEs

One commit, per marketplace-sync: the description change touches `plugin.json`, the catalog, and the repo README together; the plugin README documents the new skills and format.

**Files:**
- Modify: `plugins/project-memory/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `README.md` (repo root, the `project-memory` row)
- Modify: `plugins/project-memory/README.md`

**Interfaces:**
- Consumes: the two skills and the format from Tasks 2-4.
- Produces: the released 0.2.0 identity.

- [ ] **Step 1: Bump version and description in `plugin.json`**

Change:

```json
  "description": "In-repo project memory for Claude Code sessions — committed Team memory (docs/memory/) and git-ignored per-user Private memory (.claude/memory/), shipped as a Rules payload installed via the working-process sync-rules engine",
  "version": "0.1.0",
```

to:

```json
  "description": "In-repo project memory for Claude Code sessions — committed Team memory (docs/memory/) and git-ignored per-user Private memory (.claude/memory/); a Rules payload plus memory-review-session and migrate-memory skills",
  "version": "0.2.0",
```

- [ ] **Step 2: Update the catalog entry in `.claude-plugin/marketplace.json`**

Change the `project-memory` object's `description` to (shortening, not contradicting, the manifest):

```json
      "description": "In-repo project memory: committed Team memory and git-ignored per-user Private memory, with grooming (memory-review-session) and migration (migrate-memory) skills, shipped as a Rules payload"
```

- [ ] **Step 3: Update the repo README row in `README.md`**

Replace the `project-memory` table row with:

```markdown
| `project-memory` | In-repo project memory: committed Team memory (`docs/memory/`) and per-user Private memory (`.claude/memory/`), with `memory-review-session` and `migrate-memory` skills, distributed as a Rules payload |
```

- [ ] **Step 4: Update `plugins/project-memory/README.md` — intro, Rules bullet, and a Skills section**

First, replace the stale intro paragraph (lines 10-12):

```
Each part holds a thin `INDEX.md` (one-line pointers) plus flat topic
files: the index loads at session start, topic files are pulled only when
relevant.
```

with:

```
Each part holds a thin `INDEX.md` of live entries (loaded at session start),
an `ARCHIVE.md` of closed-entry lines (read on demand), and the live entry
bodies (pulled only when relevant).
```

Then update the conventions-rule bullet (line 23-25) — replace:

```
- `project-memory-conventions.md` — paths-scoped to the two store
  directories: note/idea entry shapes, team-memory scope, the gotcha↔ADR
  promotion offer, and the no-empty-files lifecycle.
```

with:

```
- `project-memory-conventions.md` — paths-scoped to the two store
  directories: note/idea entry shapes, team-memory scope, the gotcha↔ADR
  promotion offer, the live-only `INDEX.md` / on-demand `ARCHIVE.md` layout,
  and the closure lifecycle.
```

Then append after the "## Installation" section:

```markdown
## Skills

- **memory-review-session** — an explicit-ask grooming conversation: audits
  `INDEX.md`/`ARCHIVE.md` consistency, then walks entries toward their correct
  lifecycle state (close finished notes, promote or drop ideas, split/merge,
  sharpen index lines). Recommends per entry; never bulk-cleans; never commits.
- **migrate-memory** — moves project-scoped facts about the current repo out
  of home-dir memory into this store (one direction), routing each to Team or
  Private memory and offering store adoption when none exists yet.

## Store layout

Each part keeps a thin `INDEX.md` of **live** entries (the only file read at
session start), an `ARCHIVE.md` of closed-entry lines (Done / Dropped, read on
demand), and the live entry bodies. A closed entry keeps no body — only its
one-line archive record.
```

- [ ] **Step 5: Validate and check sync consistency**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory`
Expected: both pass.

Run: `grep -rn "0.2.0" plugins/project-memory/.claude-plugin/plugin.json && python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo JSON-OK`
Expected: version line shown, `JSON-OK`.

Run: `grep -c "memory-review-session\|migrate-memory" plugins/project-memory/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md`
Expected: each of the three files reports a non-zero count (name/skills present in all three).

- [ ] **Step 6: Commit**

```bash
git add plugins/project-memory/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md plugins/project-memory/README.md
git commit -m "feat(project-memory): release 0.2.0 — skills and archive format"
```

---

### Task 6: Trigger evals (skill-creator)

Authors the eval cases for both skills' `description:` triggering, runs a
lightweight inline trigger check (always runnable, no subagents — the
done-gate), and runs the full skill-creator harness if budget allows. Trigger
quality — not just "the YAML parses" — must be exercised before the skills are
called done; `parses` (Tasks 3/4 hand-checks) and `triggers` (here) are
different failure modes.

**Files:**
- Create: eval case files under the path the `skill-creator` scaffold writes to (do not invent a scheme — use whatever path the tool produces, confirmed in Step 4).

**Interfaces:**
- Consumes: the two SKILL.md `description:` fields.
- Produces: the eval cases; a trigger-check result and a harness run report or an explicit deferral marker.

- [ ] **Step 1: Invoke skill-creator to scaffold eval cases**

Use the `skill-creator` skill on `plugins/project-memory`. For each skill author at least: one POSITIVE case (an explicit request → skill fires) and one NEGATIVE case (a routine memory read/write or an entry-content question → does NOT fire). For `migrate-memory` add a NEGATIVE: a cross-project/personal fact must stay in home-dir (not migrated).

- [ ] **Step 2: Lightweight inline trigger check (required — the done-gate)**

Without dispatching subagents, read each `description:` against its authored
cases and confirm: the positive phrasings clearly fall inside the description's
trigger, and each negative phrasing clearly falls outside it (the anti-trigger
sentence covers it). If any case is ambiguous, tune the `description:` in the
SKILL.md (re-hand-check its frontmatter per Tasks 3/4 Step 2) and re-check.
This gate must pass before Task 7; it needs no budget.

- [ ] **Step 3: Full skill-creator harness (deferrable under a spend cap)**

Run the skill-creator eval harness (multi-run statistical trigger eval).
Expected: positives fire, negatives stay silent, across runs. If a spend cap
aborts it (as it did for python-standards), record the run as **deferred** in
the report and park a follow-up to run it when the cap resets — the skills
ship with the Step-2 gate passed and the statistical pass tracked as owed, NOT
silently unverified.

- [ ] **Step 4: Confirm staged paths, validate, commit**

Run: `git status --short plugins/project-memory` — confirm the scaffold's eval files actually appear as new/modified (if the scaffold wrote outside `skills/`, stage that real path too; do not assume `skills/` captured them).
Run: `claude plugin validate plugins/project-memory` — expected: `Validation passed` (eval files must not break the manifest).

```bash
git add plugins/project-memory
git commit -m "test(project-memory): trigger evals for the memory skills"
```

---

### Task 7: Final verification sweep

**Files:** none — read-only checks.

- [ ] **Step 1: Validate the whole marketplace**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory && claude plugin validate plugins/working-process && claude plugin validate plugins/python-standards`
Expected: all pass.

- [ ] **Step 2: working-process untouched**

Run: `git diff --name-only master..HEAD -- plugins/working-process`
Expected: no output (zero files) — the scope held.

- [ ] **Step 3: Conditionality of cross-plugin mentions**

Run: `grep -rn "grilling-session\|ADR\|glossary\|working-process\|ticket" plugins/project-memory/skills plugins/project-memory/rules`
Expected: every hit sits in a conditional clause ("when … available/installed", "when the project keeps …"), never an unconditional dependency.

- [ ] **Step 4: Repo hygiene**

Run: `grep -rn "/home/" plugins/project-memory docs/specs/2026-07-21-project-memory-skills-design.md docs/plans/2026-07-21-project-memory-skills.md`
Expected: no hits (no machine paths). Separately, scan the same files by eye for company or client names per the repo-hygiene rule — the name tokens themselves must not appear in committed text, including inside this check.

- [ ] **Step 5: No stale format wording**

Run: `grep -rn "dropped/\|struck-through" plugins/project-memory`
Expected: no hits.

- [ ] **Step 6: Report**

Summarize commits and validation. Do NOT push, open a PR, or run sync-rules on any machine without explicit authorization. Note that the spec's `architect-fallback: opus (degraded 2026-07-21)` carries a pending re-review offer at the next consumption gate (before implementation) — surfaced when Fable 5's cap resets.
```
