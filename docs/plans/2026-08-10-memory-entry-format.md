---
ticket: none
date: 2026-08-10
status: implemented
adversary: blocking (resolved 2026-08-10)
branch: feature/memory-entry-format
base: develop
---

# Project-memory entry format Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every Project-memory entry a required `description`, make the whole `INDEX.md` line a projection of its entry, pin the plugin's own frontmatter fields to the top level, and tell the rules to leave other tools' frontmatter keys alone.

**Architecture:** A rules-and-skills plugin gains edits to one rule file, two SKILL.md files and its README. No executable code — every deliverable is Markdown. "Tests" are `claude plugin validate`, hand review of rule and skill frontmatter, and greps that prove the intended text landed and the unintended text did not.

**Tech Stack:** Claude Code Rules payloads (Markdown with optional `paths:`), skills (SKILL.md with YAML frontmatter), `claude` CLI.

**Spec:** `docs/specs/2026-08-10-project-memory-entry-format-design.md` (grilled 2026-08-10; architect round 1 `concerns`, resolved; round 2 `LGTM` on the amended spec).

## Global Constraints

- Public repo: no machine-specific paths (`/home/<user>/…`), no company or client names, all committed text English.
- Commit messages: ONE line, conventional-commit subject (`type:`/`type(scope):`), no body, no trailers (no `Co-Authored-By`).
- **No version bump on this branch** unless the change is dogfooded — the release PR from `develop` to `master` mints the bump. Dogfooding sets `0.4.0-dev.memory-entry-format` (Task 5 decides): the ANTICIPATED next release, never the shipped `0.3.0` with a suffix bolted on, which semver reads as older than what is already installed.
- `claude plugin validate .` and `claude plugin validate plugins/project-memory` must pass before each commit touching the plugin. `validate` does NOT check `rules/` or `skills/` frontmatter — review those by hand; quote any YAML scalar containing `: `.
- The core rule (`project-memory.md`) ships with NO `paths:` (always-on); the conventions rule keeps `paths:` for `docs/memory/**`, `.claude/memory/**`. This plan does not change either frontmatter block.
- Mentions of other plugins stay conditional ("when the project keeps…", "when the working-process rules are installed"). Committed project rules load for people who do not have those plugins.
- Glossary terms bind: **Auto-memory** is the harness mechanism, **Home-dir memory** the store it manages by default. "Native memory" is `_Avoid_`-banned — never write it.
- **Out of scope, do not touch:** `working-process`, `python-standards`, `salesforce-standards`; the index filename (`INDEX.md` stays); `ARCHIVE.md`'s format; any `autoMemoryDirectory` redirect.
- Do NOT create `evals/trigger-evals.json` or any eval artifact for the edited skills.

## Review rounds

- **Plan-adversary**, 2026-08-10, **Sonnet 5** — the prescribed tier for a
  small mechanical plan (one family below the most capable, never the
  cheapest), not a fallback. Verdict **blocking**: two Important, one Minor,
  all resolved inline. The round verified every anchor text in Tasks 2-5
  against the real files, and confirmed the plan's out-of-scope claims about
  the three other plugins and the surviving `^ticket:` sweep.
  1. Important — the dogfooding version `0.3.0-dev.memory-entry-format`
     reuses the already-released `0.3.0`, and a prerelease sorts below its own
     release, so `sync-rules` would read the update as a downgrade against an
     installed manifest recording `0.3.0` and trip its Direction gate.
     Resolved: the number is now the anticipated next release,
     `0.4.0-dev.memory-entry-format`, with the reason recorded in Task 5
     Step 2 and in Global Constraints.
  2. Important — Task 3 Step 3 verified both of that task's edits with one
     grep whose `description` alternative matches the skill's own YAML
     frontmatter, so it passed whether or not the step-4 rewrite landed.
     Resolved: one grep per edit, plus a negative check that the old step 4
     is gone rather than duplicated.
  3. Minor — Task 1 staged the glossary but its commit subject named only the
     spec, plan and ADR. Resolved: split into two commits, each naming what
     it carries.
- **Plan-adversary round 2**, 2026-08-10, **Opus 5** — above the prescribed
  tier at the developer's request, so no fallback record. Verdict
  **blocking**: six Important, five Minor, all resolved inline. The round
  re-derived round 1's fixes and confirmed them, then found what round 1 had
  missed. Three findings were spec-level and are recorded as amendments in the
  spec itself.
  1. Important — the projection's left half had no source: nothing in the
     plugin required an entry to have an H1 (`rg -n 'H1' plugins/project-memory/`
     returned nothing). Resolved in the spec and in Task 2 Step 1.
  2. Important — migration would have destroyed the title: home-dir entries
     carry it only in `name`, which the plan dropped, while the next
     (unchanged) bullet deletes the source file. Resolved: `name` becomes the
     new entry's H1, its slug the filename.
  3. Important — the rule and the audit shipped contradictory instructions,
     one banning direct edits of an index line and the other prescribing
     exactly that. Resolved: one vocabulary — a line is re-projected from the
     entry, never authored.
  4. Important — Task 5's marketplace check asserted that `plugin.json` and
     the catalog carry the same description. They deliberately differ, and
     the grep never printed the catalog's line. Resolved: the check is now
     name-identity plus a `git diff --name-only` proving both files untouched.
  5. Important — two shipped surfaces still advertised "sharpening index
     lines": the skill's own `description:` frontmatter and README line 52.
     Resolved: both updated, with the trigger phrases held verbatim.
  6. Important — the "one grep per edit" standard from round 1 had been
     applied only in Task 3; Tasks 2 and 4 still verified several edits with
     one alternation. Resolved: split throughout, each with its own
     expectation.
  7. Minor — the `type` hint named a top-level key; the harness nests it under
     `metadata:`. Resolved.
  8. Minor — the dogfooded prerelease obliges the release to mint at
     `0.4.0` or higher, or the gate trips in reverse. Resolved: recorded in
     Task 5 Step 2.
  9. Minor — the sweep's `INDEX.md` grep over the other three plugins printed
     the same matches whether or not they were edited. Resolved: replaced
     with `git diff --name-only`, expecting empty.
  10. Minor — no task closed the lifecycle. Resolved: Task 5 Step 6.
  11. Minor — the README's `## Rules` enumeration of the conventions rule went
      stale. Resolved: extended in Task 5 Step 1.

---

### Task 1: Commit the process documents

**Files:**
- Commit (already written): `docs/specs/2026-08-10-project-memory-entry-format-design.md`
- Commit (already written): `docs/domain/adr/0002-own-entry-format.md`
- Commit (already modified): `docs/domain/glossary.md`
- Commit (already written): `docs/plans/2026-08-10-memory-entry-format.md`

**Interfaces:**
- Consumes: nothing.
- Produces: a clean baseline, so later task diffs contain only implementation.

- [ ] **Step 1: Verify the working tree holds only these four as changes**

Run: `git status --short`
Expected: `M docs/domain/glossary.md`, `?? docs/domain/adr/0002-own-entry-format.md`, `?? docs/specs/2026-08-10-project-memory-entry-format-design.md`, `?? docs/plans/2026-08-10-memory-entry-format.md` (order may vary). Anything else → stop and reconcile.

- [ ] **Step 2: Commit**

Two commits: the work's own documents, then the glossary the grilling session amended — a subject names everything it carries.

```bash
git add docs/specs/2026-08-10-project-memory-entry-format-design.md docs/plans/2026-08-10-memory-entry-format.md docs/domain/adr/0002-own-entry-format.md
git commit -m "docs: spec, plan and ADR for the project-memory entry format"
git add docs/domain/glossary.md
git commit -m "docs: add the Auto-memory term and rewrite Home-dir memory"
```

---

### Task 2: Teach the conventions rule the entry format

The whole format change lands in one rule file. The Entry shapes section gains a preamble (the `description` and the index projection) and a closing pair of paragraphs (field placement, tolerance). The existing note and idea bullets are untouched.

**Files:**
- Modify: `plugins/project-memory/rules/project-memory-conventions.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the `description` requirement, the index-projection rule with its drift authority, the top-level field placement, and the tolerance clause — all three later tasks apply them.

- [ ] **Step 1: Insert the `description` and projection paragraphs**

In `## Entry shapes`, directly after the paragraph beginning "Shape, not topic, is the criterion", insert:

```
Every entry opens with an H1 carrying its title and carries a `description:`
— one line, the summary that makes it findable. Its `INDEX.md` line is a
projection of the entry, both halves of it: the link text from the H1, the
text after the dash from `description`.

    - [H1 of the entry](file.md) — <description>

Quote the `description` scalar whenever it contains `: `, as index summaries
routinely do. Nothing parses entry frontmatter today, but an unquoted colon
makes the block invalid YAML the moment something does.

On drift the entry wins — the file is the entry, the index a view of it — so
an index line is never authored directly, only re-projected: correct the H1 or
the `description` first, then re-derive the line from them. `INDEX.md` and
`ARCHIVE.md` are registry files, not entries: no frontmatter, no
`description`, no H1 requirement.
```

- [ ] **Step 2: Append the field-placement and tolerance paragraphs**

At the end of `## Entry shapes`, after the **idea** bullet, add:

```
Every field this rule defines — `description`, `status`, `spec`, `ticket`,
`adr-candidate` — sits at the top level of the frontmatter, never nested
under a `metadata:` block. Nesting would break the anchored `^ticket:` sweep
the project's ticket convention publishes (when it keeps one), across the
whole project rather than only in the store.

Entries may carry frontmatter that other tools wrote. Leave unknown keys
alone: never remove them, never rewrite them, and never let one change an
entry's shape — the `idea-` prefix stays authoritative.
```

- [ ] **Step 3: Verify the text landed and the frontmatter did not move**

One grep per inserted passage — never a shared alternation. The word `description` alone is worthless as a check here: it recurs throughout the rule.

```bash
rg -n 'opens with an H1' plugins/project-memory/rules/project-memory-conventions.md
rg -n 'only re-projected' plugins/project-memory/rules/project-memory-conventions.md
rg -n 'sits at the top level' plugins/project-memory/rules/project-memory-conventions.md
rg -n 'Leave unknown keys' plugins/project-memory/rules/project-memory-conventions.md
head -5 plugins/project-memory/rules/project-memory-conventions.md
```

Expected: each of the four greps returns exactly one line; the file still opens with the `paths:` block listing `docs/memory/**` and `.claude/memory/**`.

- [ ] **Step 4: Verify no banned term and no unconditional cross-plugin claim**

```bash
rg -in 'native memory' plugins/project-memory/rules/project-memory-conventions.md
rg -n 'ticket convention' plugins/project-memory/rules/project-memory-conventions.md
```

Expected: first command finds nothing; second shows the sweep sentence carrying its "(when it keeps one)" hedge.

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate .
claude plugin validate plugins/project-memory
git add plugins/project-memory/rules/project-memory-conventions.md
git commit -m "feat(project-memory): require a description and derive the index line from the entry"
```

---

### Task 3: Give memory-review-session the mechanical checks

**Files:**
- Modify: `plugins/project-memory/skills/memory-review-session/SKILL.md`

**Interfaces:**
- Consumes: Task 2's H1, `description`, projection and tolerance rules.
- Produces: three audit defect checks, a format-debt clause, a narrowed entry-walk step 4, and a skill description that matches them.

- [ ] **Step 1: Add the format checks to the opening audit**

In `## Opening audit (mechanical)`, after the "empty or stub body files" bullet and before the `idea-*` bullet, insert:

```
- index lines whose text after the dash differs from the entry's
  `description` — the entry wins, so the fix is to confirm the entry and
  re-project the line, never to edit the line alone;
- index lines whose link text differs from the entry's H1 — same authority,
  same fix;
- frontmatter keys this plugin does not define: report them and move on,
  never remove them;
```

- [ ] **Step 2: Add the format-debt clause under the audit list**

Directly after the audit's bullet list, before `## Entry walk`, add:

```
Entries written before these fields existed carry **format debt, not
defects**: an entry with no `description`, or with no H1 to project a title
from, is incomplete, not broken. Count the debt and list it apart from the
defects above — a dangling link is a fault in the store, a missing
`description` is work the store has not had yet — and offer to fill it in
during the walk.
```

- [ ] **Step 3: Narrow entry-walk step 4**

Replace step 4 of `## Entry walk (ordered, existential first)`:

```
4. **Does the `INDEX.md` line summarize it well?** Recall depends on the
   one-liner — the cheapest tidiness there is.
```

with:

```
4. **Is the `description` right?** Recall depends on it. The `INDEX.md` line
   is only its projection, so judge the `description` itself and let the line
   follow.
```

- [ ] **Step 4: Update the skill's own `description:` frontmatter**

Line 3 still advertises the behavior this task narrows ("sharpening index lines"), which is now wrong: the session sharpens the entry, and the line follows. In `description:`, replace

```
splitting or merging, sharpening index lines.
```

with

```
splitting or merging, sharpening entry descriptions.
```

Change nothing else on that line. The quoted trigger phrases — `"groom the store"`, `"memory review"`, `"przejrzyjmy memory"` — stay verbatim, and the sentence order stays as it is: `description:` is what makes the skill trigger, so every other word is load-bearing. Do NOT create or update any eval file.

- [ ] **Step 5: Verify each edit separately and the untouched boundaries**

One grep per edit — never a shared one. The bare word `description` is worthless as a check here: the skill's own frontmatter contains it, so it matches whether or not the work landed.

```bash
rg -n 're-project the line' plugins/project-memory/skills/memory-review-session/SKILL.md
rg -n 'link text differs' plugins/project-memory/skills/memory-review-session/SKILL.md
rg -n 'never remove them' plugins/project-memory/skills/memory-review-session/SKILL.md
rg -n 'format debt, not' plugins/project-memory/skills/memory-review-session/SKILL.md
rg -n 'Is the .description. right' plugins/project-memory/skills/memory-review-session/SKILL.md
rg -n 'sharpening entry descriptions' plugins/project-memory/skills/memory-review-session/SKILL.md
rg -n 'line summarize it well|sharpening index lines' plugins/project-memory/skills/memory-review-session/SKILL.md
rg -n 'never bulk-cleans|Never commits' plugins/project-memory/skills/memory-review-session/SKILL.md
rg -n 'przejrzyjmy memory' plugins/project-memory/skills/memory-review-session/SKILL.md
```

Expected: greps one to six each return exactly one line; the seventh returns NOTHING (both old strings replaced, not duplicated); the eighth shows the "recommends per entry, never commits" boundaries intact; the ninth confirms the trigger phrase survived the frontmatter edit.

- [ ] **Step 6: Validate and commit**

```bash
claude plugin validate plugins/project-memory
git add plugins/project-memory/skills/memory-review-session/SKILL.md
git commit -m "feat(project-memory): audit description, index projection and foreign frontmatter keys"
```

---

### Task 4: Simplify migrate-memory and teach it the index cap

Three edits: the scan gains a weak ordering hint, the move mechanics stop translating frontmatter, and the migration trace learns its error path.

**Files:**
- Modify: `plugins/project-memory/skills/migrate-memory/SKILL.md`

**Interfaces:**
- Consumes: Task 2's field placement and tolerance rules.
- Produces: nothing later tasks depend on.

- [ ] **Step 1: Add the ordering hint to the scan**

At the end of `## Scan`, after "When a fact's scope is unclear, ask; never guess.", add:

```
A `type:` of `user` or `feedback` — nested under `metadata:`, where the
harness writes it — hints that the fact may be personal rather than scoped to
this repository, so consider those entries last. The hint never decides: a
per-user fact ABOUT this repo belongs in Private memory, and content stays the
criterion.
```

- [ ] **Step 2: Replace the shape-translation bullet in Move mechanics**

Replace:

```
- Translate shape: a home-dir entry (`name`/`description`/`metadata`
  frontmatter) becomes a **note** or an `idea-<slug>.md` per the conventions
  rule — shape is the criterion, the `idea-` prefix authoritative.
```

with:

```
- Carry the shape across: a home-dir entry becomes a **note** or an
  `idea-<slug>.md` per the conventions rule — shape is the criterion, the
  `idea-` prefix authoritative. `description` moves over unchanged. `name`
  and `metadata` do not survive as fields, but `name` carries the entry's
  only title, so it becomes the new entry's H1 and its slug the filename —
  dropped as a field, kept as information. Add the plugin's own fields per
  the conventions rule.
```

- [ ] **Step 3: Add the cap to the migration trace**

At the end of `## Migration trace`, add:

```
The harness loads that index and caps what it reads (200 lines or 25KB), and
a write past the cap comes back with an error telling you to shorten it. Keep
the trace to one line; on that error, report it and offer to shorten the
index rather than retrying the write.
```

- [ ] **Step 4: Verify the edits and that the direction is unchanged**

One grep per edit — never a shared one.

```bash
rg -n 'The hint never decides' plugins/project-memory/skills/migrate-memory/SKILL.md
rg -n 'becomes the new entry.s H1' plugins/project-memory/skills/migrate-memory/SKILL.md
rg -n 'shorten the index' plugins/project-memory/skills/migrate-memory/SKILL.md
rg -n 'Translate shape' plugins/project-memory/skills/migrate-memory/SKILL.md
rg -n 'One direction only|Never commits' plugins/project-memory/skills/migrate-memory/SKILL.md
```

Expected: the first three each return exactly one line (Steps 1, 2 and 3 respectively); the fourth returns NOTHING (the old bullet replaced, not duplicated); the fifth shows the direction and commit boundaries intact.

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate plugins/project-memory
git add plugins/project-memory/skills/migrate-memory/SKILL.md
git commit -m "feat(project-memory): move entries without translating frontmatter, and respect the home-dir index cap"
```

---

### Task 5: README, dogfooding decision, and the final sweep

**Files:**
- Modify: `plugins/project-memory/README.md`
- Modify (only if dogfooding): `plugins/project-memory/.claude-plugin/plugin.json`

**Interfaces:**
- Consumes: Tasks 2-4.
- Produces: the shipped state of the branch.

- [ ] **Step 1: Update the plugin README**

Three edits in this file. First, in `## Store layout`, after "A closed entry keeps no body — only its one-line archive record.", add:

```
Every entry opens with an H1 and carries a one-line `description:` in its
frontmatter, and its index line is a projection of the two — link text from
the H1, summary from `description` — so index lines are re-derived, never
authored by hand. Frontmatter written by other tools is left alone.
```

Second, in `## Rules`, the conventions-rule bullet enumerates what that rule holds and is now short by four items. Replace

```
  directories: note/idea entry shapes, team-memory scope, the gotcha↔ADR
```

with

```
  directories: note/idea entry shapes, the required H1 and `description` and
  the index line projected from them, top-level placement of the plugin's own
  frontmatter fields, the tolerance clause for keys other tools wrote,
  team-memory scope, the gotcha↔ADR
```

Third, at `README.md:52`, the memory-review-session bullet still promises "sharpen index lines". Replace that phrase with `sharpen entry descriptions`.

- [ ] **Step 2: Decide dogfooding**

The plugin's rules are installed on this machine, so trying the new conventions means shipping them through the Rules engine, which keys on the version string.

- **Dogfooding (default):** set `"version": "0.4.0-dev.memory-entry-format"` in `plugins/project-memory/.claude-plugin/plugin.json`, then run the `working-process:sync-rules` skill and pick the project-memory payload. The release PR strips the suffix.

  The number must be the anticipated NEXT release (`0.4.0`; the spec sizes this as a minor), not the currently shipped `0.3.0`. A prerelease sorts BELOW its own release in semver, so `0.3.0-dev.…` against an installed manifest recording `0.3.0` would trip the `sync-rules` Direction gate as a spurious downgrade — a warning-and-ask on a user-level target, a hard stop on a project-level Tracked one.

  The anticipation cuts both ways, and dogfooding creates an obligation because of it: the release PR must mint project-memory at **`0.4.0` or higher**. Mint it lower and the dogfooded machine now holds a manifest that outranks the released plugin, and the same gate trips in reverse for whoever dogfooded — recoverable only by rewriting the manifest by hand.
- **Not dogfooding:** leave `plugin.json` untouched. The rules on disk keep the old text until release.

Ask the developer which, and do only what they choose. Do not run `sync-rules` without being told to.

- [ ] **Step 3: Marketplace-sync check**

The marketplace-sync rule ties the plugin **name** across three files — `plugin.json`, the `marketplace.json` catalog entry and the root `README.md` row — while descriptions may legitimately differ: the catalog and README rows are allowed to shorten `plugin.json`'s wording, never to contradict it. They are already different strings today, so "identical descriptions" is the wrong thing to check.

This plan changes no name and no description, so the correct expectation is that all three are untouched:

```bash
git diff --name-only develop...HEAD -- .claude-plugin/marketplace.json README.md
git diff develop...HEAD -- plugins/project-memory/.claude-plugin/plugin.json
```

Expected: the first prints nothing. The second prints nothing if Step 2 chose not to dogfood, or exactly one changed line — `version` — if it did.

- [ ] **Step 4: Whole-branch sweep**

```bash
claude plugin validate .
claude plugin validate plugins/project-memory
rg -in 'native memory' plugins/
git diff --name-only develop...HEAD -- plugins/working-process plugins/python-standards plugins/salesforce-standards
git diff --stat develop...HEAD
```

Expected: both validates pass; no banned term; the third command prints NOTHING, which is what actually proves the other three plugins were left alone (grepping them for `INDEX.md` would print the same pre-existing matches either way); the diffstat lists only files under `plugins/project-memory/` and `docs/`.

- [ ] **Step 5: Commit**

```bash
git add plugins/project-memory/README.md
git commit -m "docs(project-memory): document the entry description and the derived index line"
```

If Step 2 chose dogfooding, commit the version separately:

```bash
git add plugins/project-memory/.claude-plugin/plugin.json
git commit -m "chore(project-memory): dogfood the entry format on a dev version"
```

- [ ] **Step 6: Close the lifecycle on both documents**

`status` moves forward only, and nothing so far has moved it. Set the plan's `status` to `implemented` and the spec's to `implemented` — both in one commit, at the very end, after Step 4's sweep passed.

```bash
rg -n '^status:' docs/specs/2026-08-10-project-memory-entry-format-design.md docs/plans/2026-08-10-memory-entry-format.md
```

Edit both frontmatter blocks with the Edit tool, then:

```bash
git add docs/specs/2026-08-10-project-memory-entry-format-design.md docs/plans/2026-08-10-memory-entry-format.md
git commit -m "docs: mark the entry-format spec and plan implemented"
```

Expected afterwards: `rg -l '^status: implemented' docs/` lists both files.

---

## Notes for the implementer

- Every deliverable here is prose that a model reads at runtime. Wording is the implementation: when an edit's exact text is given above, use it verbatim rather than paraphrasing.
- The spec's own reasoning for each edit lives in `docs/specs/2026-08-10-project-memory-entry-format-design.md`; ADR 0002 records why the plugin defines its own format instead of adopting the harness's. Read both before changing any wording this plan specifies.
- Existing entries in any store are NOT migrated by this plan. They gain `description` opportunistically, when `memory-review-session` next walks them. Do not write a migration pass.
