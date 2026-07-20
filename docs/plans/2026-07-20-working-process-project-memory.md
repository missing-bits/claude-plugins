---
ticket: "#1"
date: 2026-07-20
status: draft
adversary: concerns (resolved 2026-07-20)
branch: worktree-project-memory-spec
base: master
---

# Project Memory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved spec
`docs/specs/2026-07-20-working-process-project-memory-design.md` — an in-repo,
two-part (Team `docs/memory/` + Private `.claude/memory/`) memory store for
working-process, delivered as two Rules-payload rules plus supporting edits.

**Architecture:** Pure content changes to one plugin. Two new rules: an
always-on core (`project-memory.md`, no `paths:`) carrying locations,
session-start load, and best-effort routing; a paths-scoped conventions rule
(`project-memory-conventions.md`) carrying entry shapes, team-memory scope,
gotcha↔ADR, and the no-empty-files lifecycle. Two sibling process rules gain a
`ticket`-exemption; the repo's plugin-authoring rule gains an always-on
exception note; the README documents the convention; the plugin version bump
delivers it. No scripts, hooks, or engine changes.

**Tech Stack:** Markdown + YAML frontmatter; `claude` CLI for validation; `rg`
for grep checks.

## Global Constraints

- Public-repo hygiene: English only, no machine paths, no company names
  (`.claude/rules/repo-hygiene.md`).
- Commits: one line, conventional-commit subject, no body, no trailers
  (`.claude/rules/commit-messages.md`). Committing/pushing happens only on the
  developer's explicit go.
- Frontmatter safety: quote any scalar containing `: `; `claude plugin
  validate` does NOT check `rules/` files — hand-check their YAML
  (`.claude/rules/plugin-authoring.md`).
- The core rule is **always-on** (no `paths:`) by design — a deliberate
  exception to the `paths:`-required convention, justified for a
  behaviour-shaping process rule (as `workflow.md` already is). The
  conventions rule IS `paths:`-scoped.
- Routing is **best-effort** — prose says facts *should* go to the store,
  never *always*; no `type`-keyed routing table (the native memory `type`
  field is not a stable interface).
- Terminology (`docs/domain/glossary.md`): a memory half is a **part**, never
  a "tier" or "layer"; use the canonical terms Project / Team / Private /
  Home-dir memory, Idea entry, note.
- Any change under `plugins/working-process/` bumps the plugin version in the
  same PR (`.claude/rules/plugin-versioning.md`).

## Preconditions (already in this branch)

- The spec (`docs/specs/2026-07-20-working-process-project-memory-design.md`),
  `grilled` + `architect: LGTM`.
- The glossary terms (Project / Team / Private / Home-dir memory, Idea entry)
  already added to `docs/domain/glossary.md` during spec authoring — no
  glossary task here.
- An ephemeral `.claude/memory/` dogfood exists in the worktree (git-ignored);
  it demonstrates the target on-disk shape but is not part of the deliverable.

---

### Task 1: Always-on core rule

**Files:**
- Create: `plugins/working-process/rules/project-memory.md`

**Interfaces:**
- Produces: the rule filename `project-memory.md` and the concept names Task 2
  and Task 5 reference; points at `project-memory-conventions` (Task 2).

- [ ] **Step 1: Write the core rule file**

Create `plugins/working-process/rules/project-memory.md` with EXACTLY this
content (no YAML frontmatter — its absence is what makes it always-on):

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
`INDEX.md` yet exists to trigger it), and — for Team memory (`docs/memory/`) —
carry the tracked/ignored first-create question before writing anything, since
the paths-scoped process-artifacts rule does not activate at `docs/memory/`.
Private memory (`.claude/memory/`) is always ignored, so it is never asked.

Entry shapes, team-memory scope, and the lifecycle live in the
project-memory-conventions rule, which loads when you touch a memory file.
```

- [ ] **Step 2: Verify it is always-on and hygienic**

Run: `head -1 plugins/working-process/rules/project-memory.md`
Expected: `# Project memory` (the first line is a heading — NO `---`, so no
`paths:`, so the rule loads every session).

Run: `rg -n 'should go to Project memory|best-effort|opt-in' plugins/working-process/rules/project-memory.md`
Expected: matches for the best-effort routing and opt-in adoption clauses.

Confirm by eye: no `type`-keyed routing table; no machine paths; no company
names; a memory half is called a "part".

- [ ] **Step 3: Validate the plugin still loads**

Run: `claude plugin validate plugins/working-process`
Expected: PASS (validation does not inspect `rules/`, but confirms the plugin
manifest and components are intact).

- [ ] **Step 4: Commit** (on the developer's go)

```bash
git add plugins/working-process/rules/project-memory.md
git commit -m "feat(working-process): project-memory always-on core rule"
```

---

### Task 2: Paths-scoped conventions rule

**Files:**
- Create: `plugins/working-process/rules/project-memory-conventions.md`

**Interfaces:**
- Consumes: the concept names from Task 1 (Team/Private memory, the store).
- Produces: the entry-shape, scope, and lifecycle conventions the README
  (Task 5) summarizes.

- [ ] **Step 1: Write the conventions rule file**

Create `plugins/working-process/rules/project-memory-conventions.md` with
EXACTLY this content:

```markdown
---
paths:
  - "docs/memory/**"
  - ".claude/memory/**"
---

# Project memory — conventions

## Locations

- **Team memory** `docs/memory/` — a Process directory; the first-create
  tracked/ignored question applies. It may start ignored to defer the commit;
  the flip to tracked is a manual, unprompted developer action (a `*`-only
  `.gitignore` self-ignores, so flipping means deleting it or force-adding —
  which Claude never does or suggests).
- **Private memory** `.claude/memory/` — always git-ignored (`.gitignore`
  containing exactly `*`), never asked, and NOT a Process directory: a
  per-user store under the `.claude/` config namespace.

`INDEX.md` is sectioned per part: a **Notes** section (recall-on-demand) and
an **Ideas** section (a browsable backlog). The Ideas section lists each entry
in its lifecycle state: parked (a link to its `idea-` file), spec'd (a redirect
line to the spec, no file), or dropped (a struck-through tombstone with the
reason).

## Entry shapes

Shape, not topic, is the criterion; the `idea-` prefix is authoritative (the
INDEX section and frontmatter follow it).

- **note** (no prefix) — a gotcha or cross-ticket state. `ticket`-exempt (a
  cross-ticket registry, like the glossary). It may carry an optional
  `adr-candidate: yes` frontmatter flag — presence marks a decision-shaped
  note for later ADR review (`rg 'adr-candidate:'`); absent means not a
  candidate.
- **idea** (`idea-<slug>.md`) — a parked idea. Frontmatter: `status`
  (parked → spec'd | dropped), a `spec:` pointer once it graduates, and
  `ticket`.

## Team-memory scope

Team memory owns only parked ideas, cross-ticket initiative state, and
operational gotchas. Route elsewhere:

- a decision with a rationale and a real trade-off → an ADR (`docs/domain/adr/`);
- a canonical term or `_Avoid_` ban → the glossary;
- the todo/steps of one task → that work's plan;
- a unit of work tracked in the issue tracker → the `ticket`;
- any per-user fact → Private memory or home-dir memory.

## gotcha vs ADR

Default every entry to a note. When an entry is decision-shaped — hard to
reverse AND surprising without context AND a real trade-off existed — offer to
promote it to an ADR; the developer decides. A promoted note links to its ADR.

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

- [ ] **Step 2: Hand-check the YAML frontmatter**

Run: `sed -n '1,4p' plugins/working-process/rules/project-memory-conventions.md`
Expected: a `---` block with a `paths:` list of the two memory globs. No
scalar contains `: ` unquoted (the two list items are quoted). This rule is
correctly `paths:`-scoped (passive — activates when a memory file is read).

Run: `rg -n 'idea-|no empty file|best-effort' plugins/working-process/rules/project-memory-conventions.md`
Expected: matches for the `idea-` selector and the lifecycle heading.

- [ ] **Step 3: Commit** (on the developer's go)

```bash
git add plugins/working-process/rules/project-memory-conventions.md
git commit -m "feat(working-process): project-memory paths-scoped conventions rule"
```

---

### Task 3: `ticket`-exemption in the two process rules

**Files:**
- Modify: `plugins/working-process/rules/process-artifacts.md`
- Modify: `plugins/working-process/rules/ticket-frontmatter.md`

- [ ] **Step 1: Extend the registry-exemption bullet in process-artifacts.md**

In `plugins/working-process/rules/process-artifacts.md`, find the bullet:

```
- Per-work artifacts (review reports, ADRs, task briefs, progress
  ledgers) carry a `ticket` frontmatter field; registry files that live
  across tickets (the domain glossary, `.gitignore` files) are exempt.
  Reuse the ticket already established for the current work; value format
  in the ticket-frontmatter rule.
```

Append to that bullet's exempt list so it reads — **preserving the trailing
"Reuse the ticket…" sentence** (it is part of the shipped bullet; do not drop
it):

```
- Per-work artifacts (review reports, ADRs, task briefs, progress
  ledgers) carry a `ticket` frontmatter field; registry files that live
  across tickets (the domain glossary, `.gitignore` files, Project memory
  notes and `INDEX.md`) are exempt. Project-memory idea entries DO carry
  `ticket` and are not exempt. Team memory (`docs/memory/`) is a Process
  directory; Private memory (`.claude/memory/`) is not — it is the
  per-user store defined by the project-memory rule. Reuse the ticket
  already established for the current work; value format in the
  ticket-frontmatter rule.
```

Then, in the SAME file, reconcile the Process-directory enumeration with the
glossary (Team memory is a Process directory). Change the opening sentence:

```
A Process directory is a directory the working process creates in a
project repo to hold work artifacts: `docs/specs/`, `docs/plans/`,
`docs/domain/`, `docs/code-review/`, and the `.superpowers/` family at
the repo root.
```

to include `docs/memory/`:

```
A Process directory is a directory the working process creates in a
project repo to hold work artifacts: `docs/specs/`, `docs/plans/`,
`docs/domain/`, `docs/code-review/`, `docs/memory/` (Team memory), and the
`.superpowers/` family at the repo root.
```

Do NOT add `docs/memory/` to this rule's `paths:`. The always-on
project-memory core rule is the SOLE owner of the Team-memory tracked/ignored
first-create question; paths-scoping process-artifacts to `docs/memory/` would
make its own ASK re-fire in the tracked-but-uncommitted window (tracked mode
writes no `.gitignore`, so there is no prior-decision signal). This enumeration
entry is documentation only — Team-memory handling is carried by the
paths-scoped project-memory-conventions rule.

- [ ] **Step 2: Add the exemption to ticket-frontmatter.md**

In `plugins/working-process/rules/ticket-frontmatter.md`, find the field-set
bullet:

```
- Every other document under `docs/`: `ticket` + `date`.
```

Add a bullet immediately after it:

```
- Project memory (`docs/memory/`, `.claude/memory/`): notes and `INDEX.md`
  are `ticket`-exempt registry files (like the glossary); idea entries
  (`idea-*.md`) carry `ticket`. See the project-memory-conventions rule.
```

- [ ] **Step 3: Verify**

Run: `rg -n 'Project memory notes and .INDEX.md.|idea entries DO carry' plugins/working-process/rules/process-artifacts.md`
Expected: the exemption sentence is present.

Run: `rg -n 'Reuse the ticket already established' plugins/working-process/rules/process-artifacts.md`
Expected: STILL present — the pre-existing trailing sentence was preserved, not dropped.

Run: `rg -n 'docs/memory/ .Team memory.' plugins/working-process/rules/process-artifacts.md`
Expected: `docs/memory/` in the Process-directory enumeration (prose).

Run: `sed -n '1,8p' plugins/working-process/rules/process-artifacts.md`
Expected: the `paths:` block UNCHANGED — no `docs/memory/**`.

Run: `rg -n 'Project memory .*ticket.-exempt|idea entries' plugins/working-process/rules/ticket-frontmatter.md`
Expected: the new bullet is present.

Confirm by eye: `ticket-frontmatter.md` frontmatter unchanged; `process-artifacts.md` `paths:` unchanged (no memory globs).

- [ ] **Step 4: Commit** (on the developer's go)

```bash
git add plugins/working-process/rules/process-artifacts.md plugins/working-process/rules/ticket-frontmatter.md
git commit -m "docs(working-process): ticket-exempt project-memory notes and INDEX"
```

---

### Task 4: Always-on exception note in plugin-authoring

**Files:**
- Modify: `.claude/rules/plugin-authoring.md`

- [ ] **Step 1: Add the exception note**

In `.claude/rules/plugin-authoring.md`, under the "## Rules payload" section,
find the bullet beginning "Every domain rule carries a `paths:` frontmatter
block. A rule without `paths:` loads in every session … a red flag needing
explicit justification." Append a sentence to that bullet:

```
Behaviour-shaping process rules are the deliberate exception: they load
always-on (no `paths:`) so they fire every session — `workflow.md` and the
project-memory core rule are the standing instances. The `paths:`-required
expectation targets domain-standards payloads, not these.
```

- [ ] **Step 2: Verify**

Run: `rg -n 'Behaviour-shaping process rules are the deliberate exception' .claude/rules/plugin-authoring.md`
Expected: the sentence is present, in the "## Rules payload" section.

- [ ] **Step 3: Commit** (on the developer's go)

```bash
git add .claude/rules/plugin-authoring.md
git commit -m "docs: note always-on process rules as the paths-exception"
```

---

### Task 5: README + version bump (delivery)

**Files:**
- Modify: `plugins/working-process/README.md`
- Modify: `plugins/working-process/.claude-plugin/plugin.json`

**Interfaces:**
- Consumes: the rule names and concepts from Tasks 1–2.

- [ ] **Step 1: Document the convention in the README**

In `plugins/working-process/README.md`, add a section (place it with the other
rule/convention descriptions, matching the file's existing heading style):

```markdown
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

- [ ] **Step 2: Bump the plugin version (minor)**

In `plugins/working-process/.claude-plugin/plugin.json`, change:

```json
  "version": "0.7.0",
```

to:

```json
  "version": "0.8.0",
```

(A new rule/component is a backward-compatible addition → minor bump, per the
pre-1.0 versioning convention.)

- [ ] **Step 3: Validate**

Run: `claude plugin validate plugins/working-process && claude plugin validate .`
Expected: BOTH PASS.

Run: `rg -n '"version": "0.8.0"' plugins/working-process/.claude-plugin/plugin.json`
Expected: the bumped version is present.

- [ ] **Step 4: Commit** (on the developer's go)

```bash
git add plugins/working-process/README.md plugins/working-process/.claude-plugin/plugin.json
git commit -m "docs(working-process): document project memory and bump to 0.8.0"
```

---

## Post-implementation (operational, out of task scope)

- Delivery to installed copies rides the usual path: the version bump makes
  `sync-rules` report drift; installers update via the sync-rules skill.
- The work-marketplace mirror of working-process needs a manual sync after
  release (see the mirror-sync note).
- Real dogfood adoption (a persistent `.claude/memory/` in the main checkout)
  happens after the rules land — not part of this plan.

## Self-review

- **Spec coverage:** two parts (T1/T2), loading + best-effort routing + no
  `type` table (T1), inert/opt-in + first-adoption pointer (T1), entry shapes
  + `idea-` selector + `adr-candidate` (T2), sectioned INDEX + three Ideas
  line-forms (T2), team scope + redirect table (T2), gotcha↔ADR (T2),
  no-empty-files lifecycle (T2), `ticket` exemption (T3), always-on exception
  (T4), README + version bump (T5), glossary terms (precondition, already in
  branch). All spec sections map to a task.
- **Placeholder scan:** none — every rule/edit shows its full content.
- **Consistency:** rule filenames `project-memory.md` / `project-memory-conventions.md`
  and the term "part" are used identically across tasks and match the spec and
  glossary.

## Plan-adversary findings (round 1, 2026-07-20)

Verdict: `blocking` (opus 4.8, 2026-07-20) — dispatched at the prescribed tier
for a small mechanical plan (one family below the most capable), so no
fallback field. Two Important, one Minor; all fixable, none touch the design
spine. No `*-plan-review` skill matched this domain (Salesforce/Python only);
reviewed from plugin-authoring + Rules-distribution expertise, every anchor
checked against live files.

1. **Important — Task 3's quoted CURRENT bullet is incomplete → the edit
   would silently drop shipped text.** `process-artifacts.md` bullet
   (lines 46-52) continues past "…are exempt." with "Reuse the ticket already
   established for the current work; value format in the ticket-frontmatter
   rule." Task 3's "so it reads:" block omits those two lines, and Step 3's
   grep only checks the new strings, so the loss is unverified. Disposition:
   correct the quoted current text + target block to preserve the "Reuse the
   ticket…" sentence; add it to the Step 3 grep. (Mechanical — will apply.)
2. **Important — the mandatory first-create question for Team memory is not
   wired.** `process-artifacts.md` owns the tracked/ignored ASK but is
   `paths:`-scoped away from `docs/memory/` and omits it from the
   Process-directory enumeration, so it never activates there; the always-on
   core rule (present at creation) carries no mode question and forwards to
   conventions only for INDEX/entry shapes. So the one rule guaranteed present
   when Team memory is created is silent on the ASK the spec promises.
   Disposition (NEEDS DEVELOPER DECISION — touches the spec): recommended —
   the core rule's creation-offer also carries/forwards the tracked-vs-ignored
   first-create question for Team memory (symmetric to the shape forward), and
   `process-artifacts.md`'s Process-directory enumeration is reconciled to list
   `docs/memory/`. Spec gains one sentence wiring the question into the core
   rule.
3. **Minor — "native home-dir memory" drifts toward the glossary `_Avoid_`
   ban on "native memory".** Core rule body (Task 1). Disposition: drop
   "native" → "Claude Code's home-dir memory". (Mechanical — will apply.)

**Resolution (2026-07-20).** All three applied; the developer approved I2's
wiring. I1 — Task 3's quoted current bullet corrected to include the trailing
"Reuse the ticket…" sentence, target block preserves it, Step 3 grep guards
it. I2 — the core rule's creation-offer (Task 1) now carries the
tracked/ignored first-create question for Team memory, and Task 3 reconciles
`process-artifacts.md`'s Process-directory enumeration + `paths:`; the spec's
inert-by-default section and Changes-by-file were updated to match. Minor —
"native" dropped. A fresh plan-adversary round is offered to clear the
`blocking` verdict before execution.

## Plan-adversary findings (round 2, 2026-07-20)

Verdict: `concerns` (opus 4.8, 2026-07-20) — prescribed tier, no fallback. The
round-1 `blocking` is genuinely cleared: all three round-1 fixes verified
truly applied, and both remaining findings are Minor (neither holds
implementation).

1. **Minor — the Task 3 `paths:` addition makes process-artifacts' first-create
   ASK compete with the core rule, and re-fires in the tracked-but-uncommitted
   window.** `process-artifacts.md` writes NO `.gitignore` in tracked mode, so a
   `docs/memory/` chosen tracked but not yet committed has neither signal → the
   guard's "no observable prior decision" branch re-asks on the next session
   that reads `docs/memory/INDEX.md`. Net-new from my I2 paths change (the
   `.claude/memory/**` glob is benign — Private always has a `*` `.gitignore`).
   Disposition (NEEDS DEVELOPER DECISION — spec-touching): recommended — drop
   the `docs/memory/**` `paths:` addition (the core rule already owns the
   Team-memory first-create ASK; the conventions rule already carries
   Team-memory handling). Keep the Process-directory *enumeration* entry for
   documentation, with a clause that the core rule is the single owner of that
   ASK. Update spec Changes-by-file to match.
2. **Minor — spec PROSE still used the glossary-banned "native memory" in six
   places** (and the architect's round-2 note wrongly claimed conformance
   clean); the shipped rule text was already clean, so it never affected the
   deliverable. Disposition: applied — the six spec prose uses and the glossary
   term's description reworded to "home-dir memory" / "built-in"; the `_Avoid_`
   ban line and the historical findings text left as-is.

**Resolution (2026-07-20, no fresh round; both Minor).** M1 — chose option A:
the `docs/memory/**` `paths:` addition was dropped (Task 3 + spec), so the
always-on core rule stays the sole owner of the Team-memory first-create ASK
and process-artifacts does not double-ask; the enumeration entry remains as
documentation. The general improvement — make process-artifacts reliably fire
the first-create question at creation time for ALL Process directories — is
parked in the WP ideas backlog, not this feature. M2 — already applied (spec
prose + glossary description cleaned of "native memory").
