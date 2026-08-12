---
ticket: none
date: 2026-08-11
status: implemented
adversary: blocking (resolved 2026-08-11)
branch: feature/store-probe-decoupling
base: develop
---

# Store-probe decoupling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove every mention of project-memory's index filename from the
three foreign plugins — store probes test the part directories, registry-file
enumerations delegate to the conventions rule.

**Architecture:** Five wording edits across three plugins, nothing else. No
executable code — every deliverable is Markdown, so "tests" are anchored
greps proving the intended text landed (positive) and the index filename did
not survive (negative), plus a `git diff --name-only` proof that
project-memory stayed untouched.

**Tech Stack:** Claude Code Rules payloads and skills (Markdown), `rg`,
`claude` CLI.

**Spec:** `docs/specs/2026-08-11-store-probe-decoupling-design.md`
(grilled 2026-08-11; architect round skipped on the developer's call —
small mechanical change, twice consulted during the predecessor spec).

## Global Constraints

- Public repo: no machine-specific paths (`/home/<user>/…`), no company or
  client names, all committed text English.
- Commit messages: ONE line, conventional-commit subject
  (`type:`/`type(scope):`), no body, no trailers (no `Co-Authored-By`).
- **No version bump on this branch** — no dogfooding, so no `-dev.` suffix;
  the release PR from `develop` to `master` mints the bumps (patch for each
  of the three plugins, unless larger changes ride the same release).
- **Do not touch `plugins/project-memory/`** — no file of that plugin
  changes; the index filename stays `INDEX.md`.
- Glossary binds: the check is a **store probe**, never a bare "probe"
  (`_Avoid_: probe (unqualified)`); the probe tests the part's directory,
  never a file inside it.
- The two standards restatements may not drift from each other or from the
  review-reports contract: Task 2's two edits use ONE identical old/new
  text pair.
- Edit artifact and rule files with the Edit tool, never `sed -i`.
- Do NOT create `evals/trigger-evals.json` or any eval artifact.
- Verification greps run against the TARGET files, never against this plan
  (the plan's own line-wrapping differs from the files').

## Review rounds

- **Plan-adversary**, 2026-08-11, **Opus 5** (developer's explicit choice,
  above the Sonnet tier the heuristic prescribes for a small mechanical
  plan — no fallback record applies). Verdict **blocking**: 3 Important,
  8 Minor. The round reproduced all five edits in a scratch tree and
  sabotaged the checks; every Old block matched byte-for-byte and every
  line citation held. Findings, all against the verification layer:
  1. (Important) Task 2's three checks stay green when the banned bare
     "probe" replaces "store probe" — the new wrapping splits the term
     across a line break, so no grep gates it.
  2. (Important) The Task 4 untouched-proof (`git diff develop...`) cannot
     see an uncommitted stray edit to `plugins/project-memory/`; `|| true`
     also swallows git errors.
  3. (Important) The lifecycle close flips `status:` without recording
     this round's verdict and findings' disposition, which
     spec-plan-lifecycle mandates for a non-LGTM verdict.
  4. (Minor) "Verified state" says five lines; the sweep returns six
     lines across five edit sites.
  5. (Minor) Post-edit, `rg 'store probe'` finds one surface, not the
     glossary's three — same wrap as finding 1.
  6. (Minor) Task 3 silently widens the `ticket` exemption to include
     `ARCHIVE.md` (correct — working-process's list was stale since
     project-memory 0.2.0 — but a semantic change, to be stated).
  7. (Minor) "both stores present" / "both-stores" survive next to the
     new "per part" wording; the glossary says *part*.
  8. (Minor) Validation runs after the last commit and omits the
     per-plugin form the plugin-authoring rule mandates before each.
  9. (Minor) Restatement-vs-contract consistency is asserted, never
     checked — Task 2 only compares the two skills to each other.
  10. (Minor) The master negative check prints CLEAN when rg errors
      (e.g. wrong working directory).
  11. (Minor) draft → implemented skips `approved` with no note that the
      skip is deliberate.

  **Disposition (2026-08-11): all 11 accepted and folded into the tasks.**
  Findings 1+5+7: Task 1 now edits the whole bullet ("both parts", one
  edit) and Task 2's new text keeps "store probe" unbroken; both tasks
  grep for the term. Finding 2: Task 4 adds `git status --porcelain` and
  drops `|| true`. Finding 3: this section plus the frontmatter
  annotation, confirmed by Task 4 before the flip. Finding 4: "six lines
  across five edit sites". Finding 6: Task 3 states the `ARCHIVE.md`
  widening. Finding 8: Tasks 1-3 validate (both forms) before each
  commit. Finding 9: Task 4 Step 3 anchors all three surfaces. Finding
  10: Task 4 Step 1 pins the working directory and pairs a positive
  control. Finding 11: Task 4 Step 4 records the deliberate skip.

## Verified state (2026-08-11, branch `feature/store-probe-decoupling`)

`rg -n 'INDEX\.md' plugins/ --glob '!plugins/project-memory/**'` returns
exactly six lines across five edit sites (the review-reports probe wraps
onto two lines) — three probe surfaces plus two enumerations. A repo-wide
sweep excluding project-memory, specs, plans, and Private memory finds no
sixth surface; the two review commands delegate ("candidate-gap offers
verbatim") rather than restate.

---

### Task 1: Retarget the owning store probe (review-reports contract)

**Files:**
- Modify: `plugins/working-process/rules/review-reports.md:197-204`

**Interfaces:**
- Consumes: nothing.
- Produces: the contract wording the standards restatements (Task 2) mirror
  — "store probe: the directories, never a file inside them; both parts
  present means ask".

- [ ] **Step 1: Apply the edit**

One edit covering the whole Candidate-gap park bullet. It retargets the
probe AND fixes the adjacent terminology drift the glossary flags: the
store's halves are *parts* ("both stores" predates the term). Old (exact,
the full bullet):

```
- **Project-memory park** — only when the reviewed project keeps a
  Project-memory store (probe `docs/memory/INDEX.md` and
  `.claude/memory/INDEX.md`). The write is done by whoever accepts,
  never by the review run. Store selection: explicit guidance wins
  (project CLAUDE.md, the developer's own instructions, the store's
  conventions); otherwise with both stores present the offer asks the
  developer which one; with one store it names that one. No store — no
  offer, and never an offer to create a store.
```

New (keep "store probe" AND "never a file inside it" unbroken on their
lines — the drift sweeps and Task 4's cross-surface anchor grep for both):

```
- **Project-memory park** — only when the reviewed project keeps a
  Project-memory store (store probe: one existence test per part,
  on `docs/memory/` and `.claude/memory/` — the directory,
  never a file inside it). The write is done by whoever accepts,
  never by the review run. Store selection: explicit guidance wins
  (project CLAUDE.md, the developer's own instructions, the store's
  conventions); otherwise with both parts present the offer asks the
  developer which one; with one part it names that one. No store — no
  offer, and never an offer to create a store.
```

- [ ] **Step 2: Verify**

Run: `rg -c 'store probe' plugins/working-process/rules/review-reports.md`
Expected: `1`

Run: `rg -c 'both parts present' plugins/working-process/rules/review-reports.md`
Expected: `1`

Run: `rg -c 'INDEX\.md|both stores' plugins/working-process/rules/review-reports.md || echo ABSENT`
Expected: `ABSENT` (no INDEX.md left anywhere in the file — the probe was
its only mention — and no "both stores" either)

- [ ] **Step 3: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass (the plugin-authoring rule requires both forms before
every commit touching a plugin).

```bash
git add plugins/working-process/rules/review-reports.md
git commit -m "fix(working-process): point the store probe at the part directories"
```

---

### Task 2: Retarget both standards restatements (one text pair, two files)

**Files:**
- Modify: `plugins/python-standards/skills/python-code-review/SKILL.md:75-79`
- Modify: `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md:108-112`

**Interfaces:**
- Consumes: the Task 1 contract wording — this restatement condenses it and
  may not drift from it.
- Produces: nothing later tasks use.

- [ ] **Step 1: Apply the SAME edit to both files**

Both files carry this exact step-5 text (verbatim-identical in the two
skills; python at lines 75-79, salesforce at 108-112). Old:

```
   then follow the review-reports contract's Candidate-gap offers
   section: offer a Project-memory park when a store exists (probe
   `docs/memory/INDEX.md` and `.claude/memory/INDEX.md`; explicit
   guidance on store choice wins, both-stores means ask, never offer to
   create one) and always offer a generalized upstream report (target
```

New (in both files, character-for-character the same; "store probe"
unbroken on its line, "both-stores" becomes the glossary's "both parts"):

```
   then follow the review-reports contract's Candidate-gap offers
   section: offer a Project-memory park when a store exists
   (store probe: the `docs/memory/` and `.claude/memory/` directories,
   never a file inside them; explicit guidance on store choice wins,
   both parts means ask, never offer to create one) and always offer
   a generalized upstream report (target
```

- [ ] **Step 2: Verify both files**

Run: `rg -c 'store probe' plugins/python-standards/skills/python-code-review/SKILL.md plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`
Expected: each file reports `1`

Run: `rg -c 'INDEX\.md|both-stores' plugins/python-standards/skills/python-code-review/SKILL.md plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md || echo ABSENT`
Expected: `ABSENT` for both (the probe was each file's only INDEX.md
mention)

Run (drift check — the two step-5 paragraphs stay identical):

```bash
diff <(rg -A5 'offer a Project-memory park' plugins/python-standards/skills/python-code-review/SKILL.md) \
     <(rg -A5 'offer a Project-memory park' plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md)
```

Expected: no output (identical).

- [ ] **Step 3: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/python-standards && claude plugin validate plugins/salesforce-standards`
Expected: all pass.

```bash
git add plugins/python-standards/skills/python-code-review/SKILL.md plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md
git commit -m "fix: point both standards store-probe restatements at the part directories"
```

---

### Task 3: Delegate the two registry-file enumerations (working-process)

**Files:**
- Modify: `plugins/working-process/rules/process-artifacts.md:63-67`
- Modify: `plugins/working-process/rules/ticket-frontmatter.md:22-26`

**Interfaces:**
- Consumes: nothing from earlier tasks (independent of the probe edits).
- Produces: nothing later tasks use.

Note one deliberate semantic widening: the old enumerations name only
`INDEX.md`, a list stale since project-memory 0.2.0 added `ARCHIVE.md` as
a second registry file. Delegation makes the exemption follow the owning
rule's list (`INDEX.md` and `ARCHIVE.md` today), which is the point of
the change, not an accident.

- [ ] **Step 1: Edit `process-artifacts.md`**

Old (exact):

```
- Per-work artifacts (review reports, ADRs, task briefs, progress
  ledgers) carry a `ticket` frontmatter field; registry files that live
  across tickets (the domain glossary, `.gitignore` files, and — when the
  project-memory plugin's rules are installed — Project memory notes and
  `INDEX.md`) are exempt. Project-memory idea entries DO carry `ticket`
```

New:

```
- Per-work artifacts (review reports, ADRs, task briefs, progress
  ledgers) carry a `ticket` frontmatter field; registry files that live
  across tickets (the domain glossary, `.gitignore` files, and — when the
  project-memory plugin's rules are installed — Project memory notes and
  the store's registry files, whose list that plugin's conventions rule
  owns) are exempt. Project-memory idea entries DO carry `ticket`
```

- [ ] **Step 2: Edit `ticket-frontmatter.md`**

Old (exact):

```
- Project memory (`docs/memory/`, `.claude/memory/` — when the
  project-memory plugin's rules are installed): notes and `INDEX.md`
  are `ticket`-exempt registry files (like the glossary); idea entries
  (`idea-*.md`) carry `ticket`. See that plugin's
  project-memory-conventions rule.
```

New:

```
- Project memory (`docs/memory/`, `.claude/memory/` — when the
  project-memory plugin's rules are installed): notes and the store's
  registry files are `ticket`-exempt (like the glossary; the
  registry-file list belongs to that plugin's conventions rule); idea
  entries (`idea-*.md`) carry `ticket`. See that plugin's
  project-memory-conventions rule.
```

- [ ] **Step 3: Verify**

Run: `rg -c "whose list that plugin's conventions rule" plugins/working-process/rules/process-artifacts.md`
Expected: `1`

Run: `rg -c 'registry-file list belongs to' plugins/working-process/rules/ticket-frontmatter.md`
Expected: `1`

Run: `rg -c 'INDEX\.md' plugins/working-process/rules/process-artifacts.md plugins/working-process/rules/ticket-frontmatter.md || echo ABSENT`
Expected: `ABSENT` for both files.

- [ ] **Step 4: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass.

```bash
git add plugins/working-process/rules/process-artifacts.md plugins/working-process/rules/ticket-frontmatter.md
git commit -m "fix(working-process): delegate the registry-file list to the project-memory conventions rule"
```

---

### Task 4: Whole-branch verification and lifecycle close

**Files:**
- Modify: `docs/specs/2026-08-11-store-probe-decoupling-design.md` (frontmatter `status:`)
- Modify: `docs/plans/2026-08-11-store-probe-decoupling.md` (frontmatter `status:`)

**Interfaces:**
- Consumes: all Task 1-3 edits committed.
- Produces: the branch ready for merge to `develop`.

- [ ] **Step 1: Master check — the filename is gone, the term is on all three surfaces**

```bash
cd "$(git rev-parse --show-toplevel)"
rg -l 'store probe' plugins/ | wc -l
rg -n 'INDEX\.md' plugins/ --glob '!plugins/project-memory/**' || echo CLEAN
```

Expected: `3` (the three probe surfaces — a positive control proving rg
ran against the right tree, and the glossary's "three surfaces" claim made
greppable), then `CLEAN`. A count other than 3, or any line before CLEAN,
fails the task.

- [ ] **Step 2: Untouched-proof — project-memory saw no change on this branch**

Run: `git status --porcelain -- plugins/project-memory/`
Expected: no output (catches uncommitted strays the range diff below
cannot see).

Run: `git diff --name-only develop... -- plugins/project-memory/`
Expected: no output. No `|| true` — an erroring git call must fail loudly,
not read as success.

Run: `git diff --name-only develop... -- 'plugins/*/.claude-plugin/plugin.json'`
Expected: no output (no version string moved on this branch).

- [ ] **Step 3: Cross-surface consistency — restatements against the contract**

Run: `rg -c 'never a file inside' plugins/working-process/rules/review-reports.md plugins/python-standards/skills/python-code-review/SKILL.md plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`
Expected: `1` from each of the three files — the contract and both
restatements carry the same directory-not-file anchor. (Full semantic
consistency with the contract stays a human read; this anchors the part
a grep can hold.)

- [ ] **Step 4: Flip lifecycle status**

The adversary round (blocking, Opus 5, 2026-08-11) is recorded in the
Review rounds section with every finding's disposition, and the
frontmatter carries the resolution annotation — confirm both before the
flip. With the developer's confirmation, set `status: implemented` in the
spec's and this plan's frontmatter (Edit tool). The move from `draft` is
deliberate: the developer skipped the architect round and the `approved`
stage for this small mechanical change — recorded here so the spec's
missing approval reads as a decision, not an omission. Then commit both
documents together with any remaining `docs/` changes of this work
(glossary term, spec, plan):

```bash
git add docs/specs/2026-08-11-store-probe-decoupling-design.md docs/plans/2026-08-11-store-probe-decoupling.md docs/domain/glossary.md
git commit -m "docs: spec, plan and glossary for the store-probe decoupling"
```

(Commit only with the developer's authorization, as always.)
