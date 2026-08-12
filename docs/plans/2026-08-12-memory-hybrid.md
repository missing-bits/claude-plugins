---
ticket: none
date: 2026-08-12
status: implemented
adversary: blocking (resolved 2026-08-12)
branch: feature/memory-hybrid
base: develop
---

# Hybrid Private memory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename every store index to `MEMORY.md`, teach the core rule to
deduplicate loading and watch for redirect divergence, ship the
`redirect-memory` opt-in skill, and record the ADR 0002 confrontation as
ADR 0003.

**Architecture:** One plugin (`project-memory`) plus two repo artifacts
(ADR, glossary). Every deliverable is Markdown; "tests" are anchored greps
(positive and negative), `claude plugin validate` in both forms before each
commit, and hand review of skill/rule frontmatter. The rename is mechanical
(`replace_all` per file) followed by exact-text content edits per file.

**Tech Stack:** Claude Code Rules payloads and skills (Markdown with YAML
frontmatter), `rg`, `claude` CLI.

**Spec:** `docs/specs/2026-08-12-memory-hybrid-design.md` (grilled
2026-08-12; architect round 1 blocking — resolved; round 2 fresh, concerns
— resolved).

## Global Constraints

- Public repo: no machine-specific paths (`/home/<user>/…`), no company or
  client names, all committed text English. One narrow exception: quoted
  non-English trigger phrases inside a skill `description:`.
- Commit messages: ONE line, conventional-commit subject
  (`type:`/`type(scope):`), no body, no trailers (no `Co-Authored-By`).
- `claude plugin validate .` AND `claude plugin validate
  plugins/project-memory` pass before every commit touching the plugin.
  `validate` does not check `rules/` or skill body text — review YAML by
  hand; quote any scalar containing `: `.
- Glossary binds: **Auto-memory** (never "native memory"), **Hybrid
  store** (never "hybrid memory" / "hybrid mode"), **Environment**,
  **Home-dir memory**, **Store probe** (never bare "probe"). "Machine" is
  avoided where the path namespace is what matters.
- After all tasks, `INDEX.md` survives in `plugins/project-memory/` in
  EXACTLY TWO lines: the core rule's pre-rename detection and the
  conventions rule's old-name rename offer. Zero mentions anywhere else
  in the plugin (the bare word `INDEX` only additionally in the
  pre-existing, untouched eval query file).
- Keep greppable phrases unbroken on one line where a task says so —
  verification and future drift sweeps grep for them.
- Do NOT create `evals/trigger-evals.json` or any eval artifact.
- Do NOT touch other plugins; the store-probe decoupling already removed
  every foreign coupling.
- Version: Task 8 (developer-gated) sets `0.4.0-dev.memory-hybrid`; no
  other task touches `plugins/project-memory/.claude-plugin/plugin.json`
  (currently `0.4.0-dev.memory-entry-format`).
- Verification greps run against the TARGET files, never against this
  plan.

## Review rounds

- **Plan-adversary**, 2026-08-12, **Opus 5** (developer's explicit
  choice). Verdict **blocking**: 1 Critical, 4 Important, 10 Minor. The
  round reproduced every Old block, replace_all count, and grep
  expectation (all held); the findings target design gaps the greps
  cannot see:
  1. (Critical) Silent store blackout: the core rule looks only for
     `MEMORY.md`, while the rename offer lives in the paths-gated
     conventions rule that loads only when store files are touched — a
     pre-rename store stops loading and the Adoption clause can create a
     second index beside the orphan. Pre-rename detection must live in
     the core rule's Loading clause.
  2. (Important) The plugin description enumerates its skills in
     plugin.json, marketplace.json, and the root README table; shipping
     redirect-memory makes all three stale, and marketplace-sync demands
     one commit touching all three.
  3. (Important) The divergence check is unconditional in an always-on
     rule — it fires in projects with no store at all, against the
     rule's never-nags stance. Gate on `.claude/memory/` existing.
  4. (Important) The cap-error deferral points at a clause framed as
     Hybrid-only and paths-scoped away from the Home-dir index that
     migrate-memory actually writes. Word the budget unconditionally and
     keep the actionable recovery in the skill.
  5. (Important) The "enable hybrid memory" trigger instantiates the
     glossary ban (repo-hygiene's trigger exception covers language,
     never bans); the Task 9 sweep was shaped to miss it.
  6-15. (Minor) Bare `INDEX` word survives in two files unseen by the
     `INDEX\.md` greps; `an MEMORY.md` article break in README; Task 4's
     partial-line Old block; a by-eye check of a frontmatter block the
     core rule does not have; the glossary-commit contradiction between
     Tasks 7 and 9; Status reads only settings.local.json though other
     settings files are honored; "Edit tool… create the file" (Edit
     cannot create — Write when absent); the parked idea this spec
     graduates from is not closed at dogfood; only one payload re-synced
     (installed working-process copy is pre-decoupling); plan status
     should pass through `approved` at the adversary stamp.

  **Disposition (2026-08-12): all 15 accepted and applied.** Critical:
  the core rule's Loading clause gained the pre-rename detection (reads
  the old-named index meanwhile, Adoption keeps its hands off) — the
  plugin's surviving `INDEX.md` count is now two and every affected grep
  expectation was updated. Important 2: Task 6 grew the three identity
  surfaces with exact texts, one commit. Important 3: the divergence
  check is gated on `.claude/memory/` existing. Important 4: the budget
  clause worded unconditionally in the conventions rule; migrate-memory
  keeps the numbers and the recovery inline. Important 5: the trigger
  phrase is "enable the hybrid store" (canonical term) and the ban sweep
  now covers "hybrid memory". Minors: bare-INDEX edits in Tasks 1-2 with
  a whitelisted three-line sweep in Task 9; the README article fix; the
  full-line Old block in Task 4; the frontmatter by-eye check reworded
  (the core rule has none); the glossary-commit contradiction removed
  (Task 7 owns it); Status checks every honored settings file; Edit
  vs Write on a fresh settings file; Task 8 closes the graduated idea
  and syncs both payloads; plan status set to `approved` at this stamp.

## Verified state (2026-08-12, branch `feature/memory-hybrid`)

`rg -c 'INDEX\.md' plugins/project-memory/ -g '*'`: README.md 6,
project-memory-conventions.md 7, project-memory.md 4,
memory-review-session/SKILL.md 5, migrate-memory/SKILL.md 1 — 23 total.
The working tree already carries uncommitted, deliberate edits to
`docs/domain/glossary.md` (grilling outcomes) — they ride Task 7's commit,
which stages the whole file. The spec and this plan are untracked until
Task 9's commit. No other plugin mentions the filename (decoupling shipped
in `develop`).

---

### Task 1: Core rule — rename, loading dedup, divergence watch

**Files:**
- Modify: `plugins/project-memory/rules/project-memory.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the loading-section wording Tasks 2-6 stay consistent with —
  "unless the session context already carries that index" (dedup) and the
  divergence message contract ("say so plainly").

- [ ] **Step 1: Mechanical rename**

Edit tool, `replace_all: true`, old `INDEX.md` → new `MEMORY.md` (4
occurrences).

- [ ] **Step 2: Replace the Loading section**

Old (exact, post-rename):

```
## Loading

When a part's `MEMORY.md` exists, read it at session start and pull a topic
file only when its index line is relevant. If neither `MEMORY.md` exists this
rule is a no-op — it never scans, creates, or nags.
```

New:

```
## Loading

When a part's `MEMORY.md` exists, read it at session start and pull a topic
file only when its index line is relevant — unless the session context
already carries that index: in a Hybrid store, Auto-memory loads Private
memory's `MEMORY.md` itself, and reading it twice buys nothing. If neither
`MEMORY.md` exists this rule is a no-op — it never scans, creates, or nags.

One exception to the no-op: a part directory holding an `INDEX.md` and no
`MEMORY.md` is a store from before the rename, never "no store". Say so at
session start, point at the conventions rule's rename offer, and read the
old-named index as the part's index meanwhile — the Adoption clause must
never create a second index beside it.

When Private memory exists (`.claude/memory/` present) and
`.claude/settings.local.json` carries `autoMemoryDirectory`, compare its
value with the realpath of `<project>/.claude/memory`. On a mismatch, say
so plainly: the redirect points elsewhere in this session's filesystem
namespace, so Auto-memory is writing a stray store or none at all — the
platform gives no other visible signal. Never edit settings from this rule;
that is the redirect-memory skill's job, when it is available.
```

- [ ] **Step 2b: Fix the bare word left by the rename**

Old (exact, post-rename): `project-memory-conventions rule for the INDEX
sections and entry shapes (no` → New: `project-memory-conventions rule for
the index sections and entry shapes (no` (the generic word — no filename
survives here).

- [ ] **Step 3: Verify**

Run: `rg -c 'MEMORY\.md' plugins/project-memory/rules/project-memory.md`
Expected: `6` (4 renamed, minus the replaced Loading section's 2, plus the
new Loading text's 4)

Run: `rg -n 'INDEX\.md' plugins/project-memory/rules/project-memory.md`
Expected: exactly ONE line — the pre-rename detection ("holding an
`INDEX.md` and no `MEMORY.md`"). Zero or more than one fails.

Run: `rg -n '\bINDEX\b' plugins/project-memory/rules/project-memory.md`
Expected: the same single line (the bare word survives nowhere else —
Step 2b removed it).

Run: `rg -c 'Auto-memory is writing a stray store' plugins/project-memory/rules/project-memory.md`
Expected: `1` (the divergence message contract, unbroken on one line)

- [ ] **Step 4: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory`
Expected: both pass. Confirm the file still opens directly with
`# Project memory` and carries no frontmatter block — always-on by
design.

```bash
git add plugins/project-memory/rules/project-memory.md
git commit -m "feat(project-memory): rename the index to MEMORY.md and watch the redirect in the core rule"
```

---

### Task 2: Conventions rule — rename, budget, old-name offer, second writer

**Files:**
- Modify: `plugins/project-memory/rules/project-memory-conventions.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the old-name offer wording (one of the plugin's exactly TWO
  surviving `INDEX.md` mentions, beside the core rule's detection —
  Task 9's master grep counts on both) and the section-blind sentence
  Task 3 mirrors.

- [ ] **Step 1: Mechanical rename**

Edit tool, `replace_all: true`, old `INDEX.md` → new `MEMORY.md` (7
occurrences).

- [ ] **Step 2: Add the budget clause**

Old (exact, post-rename — the paragraph closing the Locations section):

```
they close (see Lifecycle). `MEMORY.md` is the only file read at session start,
so it never carries history.
```

New:

```
they close (see Lifecycle). `MEMORY.md` is the only file read at session
start, so it never carries history. The harness caps any index it loads —
200 lines / 25 KB; in a Hybrid store that is this file. Keep lines thin,
and when a write bounces off the cap, shorten the index rather than
retrying.
```

Then fix the bare word the rename leaves two paragraphs below, in Entry
shapes. Old (exact): `the INDEX section and frontmatter follow it` → New:
`the index section and frontmatter follow it`.

- [ ] **Step 3: Add the old-name offer (new subsection, directly after the paragraph edited in Step 2)**

Insert:

```
### Stores that predate the rename

A store whose live index is still named `INDEX.md` predates this
convention. Offer once to rename the file to `MEMORY.md` (`git mv` in a
tracked part, a plain rename in an ignored one) — content untouched, and
nothing to re-point: no plugin outside project-memory names the index
file. Declined, the offer rests for the session; the core rule keeps
reading the old-named index meanwhile, so nothing goes dark.
```

- [ ] **Step 4: Add the second-writer sentence to Entry shapes**

Old (exact — the tolerance-clause paragraph):

```
Entries may carry frontmatter that other tools wrote. Leave unknown keys
alone: never remove them, never rewrite them, and never let one change an
entry's shape — the `idea-` prefix stays authoritative.
```

New:

```
Entries may carry frontmatter that other tools wrote. Leave unknown keys
alone: never remove them, never rewrite them, and never let one change an
entry's shape — the `idea-` prefix stays authoritative. In a Hybrid store
Auto-memory is a second writer: an entry it writes is an ordinary note
whose missing H1 is format debt, and an index line it appends lands
section-blind — re-sectioning belongs to the grooming walk
(memory-review-session, when available), never to a routine write.
```

- [ ] **Step 5: Verify**

Run: `rg -c 'INDEX\.md' plugins/project-memory/rules/project-memory-conventions.md`
Expected: `1` (only the old-name offer)

Run: `rg -c 'shorten the index rather than retrying' plugins/project-memory/rules/project-memory-conventions.md`
Expected: `1`

Run: `rg -c 'section-blind' plugins/project-memory/rules/project-memory-conventions.md`
Expected: `1`

Run: `rg -c 'Stores that predate the rename' plugins/project-memory/rules/project-memory-conventions.md`
Expected: `1`

Run: `rg -c '\bINDEX\b' plugins/project-memory/rules/project-memory-conventions.md`
Expected: `1` (only the old-name offer's `INDEX.md`; the bare-word site is
gone)

- [ ] **Step 6: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory`
Expected: both pass. The `paths:` frontmatter block stays unchanged —
confirm by eye.

```bash
git add plugins/project-memory/rules/project-memory-conventions.md
git commit -m "feat(project-memory): MEMORY.md conventions - budget, old-name offer, second writer"
```

---

### Task 3: memory-review-session — rename, re-sectioning, Auto-memory debt

**Files:**
- Modify: `plugins/project-memory/skills/memory-review-session/SKILL.md`

**Interfaces:**
- Consumes: Task 2's section-blind sentence (this skill implements the
  "grooming walk" duty it names).
- Produces: nothing later tasks use.

- [ ] **Step 1: Mechanical rename**

Edit tool, `replace_all: true`, old `INDEX.md` → new `MEMORY.md` (5
occurrences, all in the body). Then one separate edit in the frontmatter
`description:` — it names the files without extensions: old
`audits INDEX/ARCHIVE consistency` → new `audits MEMORY/ARCHIVE
consistency`; confirm the description's quoting survives intact.

- [ ] **Step 2: Add the wrong-section audit bullet**

Old (exact — the sweep bullet, post-rename):

```
- **sweep**: any closed line still in `MEMORY.md` (legacy, or a botched close)
  moves to `ARCHIVE.md`. Under the invariant this should be empty; the sweep
  is the safety net.
```

New:

```
- index lines sitting in the wrong section (a section-blind writer —
  Auto-memory in a Hybrid store — appended them): move the line to its
  part's proper section; the entry body is untouched;
- **sweep**: any closed line still in `MEMORY.md` (legacy, or a botched close)
  moves to `ARCHIVE.md`. Under the invariant this should be empty; the sweep
  is the safety net.
```

- [ ] **Step 3: Extend the format-debt sentence**

Old (exact):

```
Entries written before these fields existed carry **format debt, not
defects**: an entry with no `description`, or with no H1 to project a title
from, is incomplete, not broken.
```

New:

```
Entries written before these fields existed — or written by Auto-memory,
which knows nothing of them — carry **format debt, not defects**: an entry
with no `description`, or with no H1 to project a title from, is
incomplete, not broken.
```

- [ ] **Step 4: Verify**

Run: `rg -c 'INDEX\.md' plugins/project-memory/skills/memory-review-session/SKILL.md || echo ABSENT`
Expected: `ABSENT`

Run: `rg -c 'section-blind writer' plugins/project-memory/skills/memory-review-session/SKILL.md`
Expected: `1`

Run: `rg -c 'or written by Auto-memory' plugins/project-memory/skills/memory-review-session/SKILL.md`
Expected: `1`

- [ ] **Step 5: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory`
Expected: both pass (validate checks skill frontmatter — the renamed
description must still parse).

```bash
git add plugins/project-memory/skills/memory-review-session/SKILL.md
git commit -m "feat(project-memory): review-session audits MEMORY.md and re-sections harness-appended lines"
```

---

### Task 4: migrate-memory — path-qualified stores, hybrid no-op

**Files:**
- Modify: `plugins/project-memory/skills/migrate-memory/SKILL.md`

**Interfaces:**
- Consumes: nothing.
- Produces: nothing later tasks use.

- [ ] **Step 1: Qualify the scan source**

Old (exact — the full opening of the Scan paragraph, so the sentence that
follows survives intact):

```
Read home-dir memory (`MEMORY.md` plus its entry files). Candidates are facts
```

New (the rename makes the bare filename ambiguous — every store name is
now qualified by path; re-wrap the paragraph after the edit):

```
Read home-dir memory — the Home-dir store's `MEMORY.md` and entry files,
under `~/.claude/projects/<project>/memory/` by default. Candidates are facts
```

- [ ] **Step 2: Add the hybrid no-op check (new paragraph directly under the `## Scan` heading, before the paragraph edited in Step 1)**

Insert:

```
First check for identity: when the Auto-memory redirect is active in this
environment (`autoMemoryDirectory` in `.claude/settings.local.json` equals
the realpath of `<project>/.claude/memory`), home-dir → Private is a no-op
— the two directories are one. Say so and skip the Private-memory
candidates; Team-memory moves are unaffected. Each environment keeps its
own Home-dir store, so run the migration where the notes live.
```

- [ ] **Step 3: Qualify the projection and deletion lines**

Old (exact):

```
- Project the entry's line into the target part's `INDEX.md` — link text from
  its H1, summary from its `description`, per the conventions rule.
- Delete the home-dir body file and its `MEMORY.md` line.
```

New:

```
- Project the entry's line into the target part's `MEMORY.md` — link text
  from its H1, summary from its `description`, per the conventions rule.
- Delete the home-dir body file and its line in the Home-dir store's
  `MEMORY.md`.
```

- [ ] **Step 4: Qualify the trace target**

Old (exact):

```
After moving one or more facts, leave a single roll-up line in home-dir
`MEMORY.md` — "project-scoped notes for <repo> migrated to its Project
memory, <date>" — not a per-entry pointer.
```

New:

```
After moving one or more facts, leave a single roll-up line in the Home-dir
store's `MEMORY.md` — "project-scoped notes for <repo> migrated to its
Project memory, <date>" — not a per-entry pointer.
```

- [ ] **Step 5: Defer the cap error to the conventions rule**

The general "shorten, don't retry" convention graduates to the
conventions rule (Task 2); this skill defers instead of restating. Old
(exact — the trace section's closing paragraph):

```
The harness loads that index and caps what it reads (200 lines or 25KB),
and a write past the cap comes back with an error telling you to shorten
it. Keep the trace to one line; on that error, report it and offer to
shorten the index rather than retrying the write.
```

New (the numbers and the recovery stay here — this skill is the only
surface loaded when the Home-dir trace is written; the conventions rule
owns the canonical statement):

```
The harness caps what it loads from that index — 200 lines / 25 KB, the
budget convention the conventions rule owns. Keep the trace to one line;
on a cap error shorten the index, never retry the write.
```

- [ ] **Step 6: Verify**

Run: `rg -c 'INDEX\.md' plugins/project-memory/skills/migrate-memory/SKILL.md || echo ABSENT`
Expected: `ABSENT`

Run: `rg -c 'no-op' plugins/project-memory/skills/migrate-memory/SKILL.md`
Expected: `1`

Run: `rg -c "Home-dir store's" plugins/project-memory/skills/migrate-memory/SKILL.md`
Expected: `3`

Run: `rg -c 'never retry the write' plugins/project-memory/skills/migrate-memory/SKILL.md`
Expected: `1`

- [ ] **Step 7: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory`
Expected: both pass.

```bash
git add plugins/project-memory/skills/migrate-memory/SKILL.md
git commit -m "feat(project-memory): migrate-memory path-qualifies stores and detects the hybrid no-op"
```

---

### Task 5: redirect-memory — the new skill

**Files:**
- Create: `plugins/project-memory/skills/redirect-memory/SKILL.md`

**Interfaces:**
- Consumes: the core rule's divergence contract (Task 1) and
  migrate-memory's no-op behavior (Task 4) — both referenced, neither
  restated.
- Produces: the skill name `redirect-memory` Tasks 6-7 mention.

- [ ] **Step 1: Write the skill (full content)**

```markdown
---
name: redirect-memory
description: "Enable, disable, or inspect the Auto-memory redirect that makes this project's Private memory a Hybrid store (autoMemoryDirectory in .claude/settings.local.json). Use ONLY when the developer explicitly asks to point Claude Code's own memory at the project store or back (\"enable the hybrid store\", \"redirect memory to the project\", \"włącz hybrydę\"). Not a routine memory read or write."
---

# redirect-memory

Points Auto-memory at this project's Private memory store — or points it
back. One key, one realpath: the skill writes `autoMemoryDirectory` into
`.claude/settings.local.json` and nothing else. Explicit-ask only; never
commits; never touches store content.

## Status (always first)

Read `.claude/settings.local.json` (when present) and report:

- no `autoMemoryDirectory` key in ANY honored settings file → redirect
  off; sessions here use their default Home-dir store. Before saying
  "off", also check `.claude/settings.json` (committed — honored despite
  its own schema note) and the user-level settings, and name the file
  that carries the key when one does;
- key equal to `realpath(<project>/.claude/memory)` → active in THIS
  environment;
- key differing → written from another environment (or the checkout
  moved): name both paths and which filesystem view each resolves in.

## Enable

1. Compute `realpath(<project>/.claude/memory)` — never accept a typed
   path. The store need not exist yet: asking for the redirect is the
   intent signal the core rule's adoption clause waits for, so offer to
   create Private memory (always ignored, never asked tracked/ignored).
2. Warn before writing — always. The settings file is per-checkout; the
   path is per-environment ("this path resolves only where this
   filesystem view exists"). A session on the losing side gets Home-dir
   memory only without trust or key; otherwise it manufactures a stray
   store at the foreign path, or runs with no working Auto-memory at
   all. A path-preserving bind mount (`-v "$PWD:$PWD"`-style) activates
   both sides at once — two writers on one index. Environment detection
   (`/.dockerenv`, `REMOTE_CONTAINERS` in env) only enriches this
   wording ("you are writing the container-side path"); never refuse.
3. Write the key preserving every other key in the file — the Edit tool
   when the file exists, the Write tool when it does not.
4. Offer a one-time `migrate-memory` pass (when that skill is available)
   for THIS environment's Home-dir store — each environment keeps its
   own, so migration runs where the notes live.
5. Verification, stated to the developer: settings are read at session
   start, so the redirect takes effect in the NEXT session. Start one,
   write a note, confirm the file lands in `.claude/memory/` — every
   failure mode of the redirect is silent by platform design.

## Disable

Name the asymmetry, then let the developer choose:

- **Remove the key** (the default): environment-neutral — every
  environment returns to its own default Home-dir store.
- **`autoMemoryEnabled: false`**: switches Auto-memory off in EVERY
  environment that trusts this checkout — the bigger hammer, written
  only on an explicit request for it.

Either way the store is untouched and the rule-driven loading continues.

## Boundaries

Writes exactly one settings file, never a committable one — the path has
no portable form. Never commits. Never creates or edits store content:
store creation is the core rule's offer, moving notes is
migrate-memory's, grooming is memory-review-session's.
```

- [ ] **Step 2: Verify**

Run: `rg -c 'name: redirect-memory' plugins/project-memory/skills/redirect-memory/SKILL.md`
Expected: `1`

Run: `rg -c 'INDEX\.md' plugins/project-memory/skills/redirect-memory/SKILL.md || echo ABSENT`
Expected: `ABSENT`

Run: `rg -c 'never refuse' plugins/project-memory/skills/redirect-memory/SKILL.md`
Expected: `1`

Run: `rg -ci 'hybrid mode|hybrid memory|native memor' plugins/project-memory/skills/redirect-memory/SKILL.md || echo CLEAN`
Expected: `CLEAN` (glossary bans — the trigger phrase deliberately says
"enable the hybrid store", the canonical term, so no exemption is
needed).

- [ ] **Step 3: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory`
Expected: both pass (the new skill's frontmatter parses; description
quoted — it contains `: `).

```bash
git add plugins/project-memory/skills/redirect-memory/SKILL.md
git commit -m "feat(project-memory): redirect-memory skill - the Hybrid store opt-in switch"
```

---

### Task 6: README, hybrid section, and the plugin's identity surfaces

**Files:**
- Modify: `plugins/project-memory/README.md`
- Modify: `plugins/project-memory/.claude-plugin/plugin.json` (description only)
- Modify: `.claude-plugin/marketplace.json` (project-memory entry description)
- Modify: `README.md` (repo root — the project-memory table row)

**Interfaces:**
- Consumes: names settled in Tasks 1-5 (`redirect-memory`, the divergence
  watch, the old-name offer).
- Produces: nothing later tasks use.

- [ ] **Step 1: Mechanical rename**

Edit tool, `replace_all: true`, old `INDEX.md` → new `MEMORY.md` (6
occurrences). Then fix the article the replace breaks: old (exact)
`without an `MEMORY.md`` → new `without a `MEMORY.md``.

- [ ] **Step 2: Extend the core-rule bullet**

Old (exact, post-rename):

```
- `project-memory.md` — the always-on core: loads each part's `MEMORY.md`
  at session start, routes project-scoped facts to the store (best-effort)
  instead of home-dir memory, and owns Team memory's tracked/ignored
  first-create question. Always-on deliberately: index loading has no file
  path to scope on.
```

New:

```
- `project-memory.md` — the always-on core: loads each part's `MEMORY.md`
  at session start (skipping an index Auto-memory already loaded), watches
  `autoMemoryDirectory` for divergence from the store path, routes
  project-scoped facts to the store (best-effort) instead of home-dir
  memory, and owns Team memory's tracked/ignored first-create question.
  Always-on deliberately: index loading has no file path to scope on.
```

- [ ] **Step 3: Add the redirect-memory skill bullet (after the migrate-memory bullet in `## Skills`)**

Insert:

```
- **redirect-memory** — enables, disables, or inspects the Auto-memory
  redirect that makes Private memory a Hybrid store: one
  `autoMemoryDirectory` key in `.claude/settings.local.json`, written
  with the current environment's realpath, warned about honestly, and
  verified in the next session.
```

- [ ] **Step 4: Add the hybrid section (after `## Store layout`)**

Insert:

```
## Hybrid store (opt-in)

With the redirect active, `.claude/memory/` is also the session's
Auto-memory directory: Claude Code loads the store's `MEMORY.md` itself
(200-line / 25 KB budget) and writes its own notes there as ordinary
entries — a missing H1 is format debt the review session pays down, and
foreign frontmatter keys are left alone. The redirect is per environment
(host, dev container, WSL — each has its own path namespace and trust
record) and per checkout; the losing side of a switch keeps rule-driven
loading and a plainly-worded divergence message. Team memory never joins
the redirect — Auto-memory's team mounts are server-backed, and the
committed, reviewed, branch-following store is the point of Team memory,
not a limitation.
```

- [ ] **Step 5: Verify**

Run: `rg -c 'INDEX\.md' plugins/project-memory/README.md || echo ABSENT`
Expected: `ABSENT`

Run: `rg -c 'Hybrid store \(opt-in\)' plugins/project-memory/README.md`
Expected: `1`

Run: `rg -c 'redirect-memory' plugins/project-memory/README.md`
Expected: `1`

- [ ] **Step 6: Update the three identity surfaces (marketplace-sync rule: one commit)**

The plugin description enumerates its skills, so shipping
`redirect-memory` changes it — and the marketplace-sync rule demands the
manifest, the catalog entry, and the repo README row move in the same
commit.

In `plugins/project-memory/.claude-plugin/plugin.json`, old (exact):
`a Rules payload plus memory-review-session and migrate-memory skills` →
new: `a Rules payload plus memory-review-session, migrate-memory, and
redirect-memory skills` (keep the JSON string on one line).

In `.claude-plugin/marketplace.json`, old (exact): `with grooming
(memory-review-session) and migration (migrate-memory) skills, shipped as
a Rules payload` → new: `with grooming (memory-review-session), migration
(migrate-memory), and the Auto-memory redirect (redirect-memory) skills,
shipped as a Rules payload` (one line).

In the repo root `README.md` table row, old (exact): `with
`memory-review-session` and `migrate-memory` skills, distributed as a
Rules payload` → new: `with `memory-review-session`, `migrate-memory`,
and `redirect-memory` skills, distributed as a Rules payload` (one line).

- [ ] **Step 7: Verify the surfaces agree**

Run: `rg -c 'redirect-memory' plugins/project-memory/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md`
Expected: `1` from each of the three files.

- [ ] **Step 8: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory`
Expected: both pass.

```bash
git add plugins/project-memory/README.md plugins/project-memory/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md
git commit -m "docs(project-memory): README, Hybrid store section, and identity surfaces for redirect-memory"
```

---

### Task 7: ADR 0003 and the glossary rename entries

**Files:**
- Create: `docs/domain/adr/0003-hybrid-store-adoption.md`
- Modify: `docs/domain/glossary.md` (the three entries naming `INDEX.md`:
  **Archive**, **Live entry**, **Close (an entry)**)

**Interfaces:**
- Consumes: the settled terms (Hybrid store, Environment) and skill name.
- Produces: nothing later tasks use.

- [ ] **Step 1: Write ADR 0003 (full content)**

```markdown
---
ticket: none
---

# Private memory may double as the Auto-memory directory, opt-in

ADR 0002 closed with: "Making the store double as the Auto-memory
directory would reverse this decision, so that later choice has to face
it deliberately instead of sliding past it." This record is that choice,
faced. The hybrid adopts exactly two platform-owned identities — the
directory (`autoMemoryDirectory` may point at `.claude/memory/`) and the
index filename (`MEMORY.md`, the only name Auto-memory loads, adopted
globally so the format has no mode variants) — because in a Hybrid store
both pass ADR 0002's own test: they earn their place as the only way the
harness reads the store at all.

Everything else stands. The plugin defines its own entry format,
converges on Auto-memory's without adopting it, and keeps the tolerance
clause for keys the harness writes; an entry Auto-memory writes into a
Hybrid store is an ordinary note whose missing H1 is format debt. The
adoption is opt-in per developer and per Environment, carried by one key
in `.claude/settings.local.json` written and removed by the
redirect-memory skill; declining it leaves the store purely rule-driven.
ADR 0002 remains in force for the format — this record narrows it only
at the directory-and-name boundary.
```

- [ ] **Step 2: Rename the three glossary entries**

Three Edit calls in `docs/domain/glossary.md`, each `INDEX.md` →
`MEMORY.md`:

1. **Archive** entry: `Distinct from a live entry (listed in \`INDEX.md\`)` →
   `(listed in \`MEMORY.md\`)`.
2. **Live entry** entry: `currently listed in \`INDEX.md\`` →
   `currently listed in \`MEMORY.md\``.
3. **Close (an entry)** entry: `Move an entry out of \`INDEX.md\`` →
   `Move an entry out of \`MEMORY.md\``.

- [ ] **Step 3: Verify**

Run: `rg -c 'INDEX\.md' docs/domain/glossary.md || echo ABSENT`
Expected: `ABSENT`

Run: `rg -c 'ADR 0002' docs/domain/adr/0003-hybrid-store-adoption.md`
Expected: `3`

Run: `rg -c '^ticket: none' docs/domain/adr/0003-hybrid-store-adoption.md`
Expected: `1`

- [ ] **Step 4: Commit** (docs only — no plugin validation needed, but it
  is free: run `claude plugin validate .` anyway)

```bash
git add docs/domain/adr/0003-hybrid-store-adoption.md docs/domain/glossary.md
git commit -m "docs: ADR 0003 and glossary for the Hybrid store"
```

Note: `docs/domain/glossary.md` also carries the earlier grilling edits
(Hybrid store, Environment, Auto-memory, Home-dir memory) — they belong to
this same commit; stage the whole file.

---

### Task 8: Dogfood (developer-gated)

**Files:**
- Modify: `plugins/project-memory/.claude-plugin/plugin.json`

**Interfaces:**
- Consumes: all content tasks committed.
- Produces: the version string Task 9's checks expect.

STOP and confirm with the developer before this task — it changes the
version and this machine's installed rules.

- [ ] **Step 1: Mint the dogfood version**

Edit `plugins/project-memory/.claude-plugin/plugin.json`:
`"version": "0.4.0-dev.memory-entry-format"` →
`"version": "0.4.0-dev.memory-hybrid"` (same anticipated release, this
topic's discriminator; the release PR strips it while minting the final
≥ 0.4.0).

- [ ] **Step 2: Validate, then commit**

Run: `claude plugin validate . && claude plugin validate plugins/project-memory`
Expected: both pass.

```bash
git add plugins/project-memory/.claude-plugin/plugin.json
git commit -m "chore(project-memory): dogfood version for the memory-hybrid topic"
```

- [ ] **Step 3: Sync and adopt locally (outside git)**

With the developer driving: run `working-process:sync-rules` with
explicit sources for BOTH payloads — `plugins/project-memory/rules` AND
`plugins/working-process/rules` (the marketplace serves GitHub master, so
discovery alone will not see this working tree, and the installed
working-process copy predates the store-probe decoupling — left stale, it
keeps enumerating the old index filename against the renamed store). Then
offer the store rename this repo's own Private memory is now eligible for
(`.claude/memory/INDEX.md` → `MEMORY.md`, a plain rename — the store is
ignored), and close the parked idea this spec graduated from
(`.claude/memory/idea-native-memory-hybrid.md`): delete the body, move its
index line to `ARCHIVE.md` **Done** as a redirect to
`docs/specs/2026-08-12-memory-hybrid-design.md`, per the conventions
lifecycle. Enabling the redirect itself stays a separate, explicit
`redirect-memory` ask.

---

### Task 9: Whole-branch verification and lifecycle close

**Files:**
- Modify: `docs/specs/2026-08-12-memory-hybrid-design.md` (frontmatter `status:`)
- Modify: `docs/plans/2026-08-12-memory-hybrid.md` (frontmatter `status:`)

**Interfaces:**
- Consumes: everything committed.
- Produces: the branch ready for merge to `develop`.

- [ ] **Step 1: Master rename check**

```bash
cd "$(git rev-parse --show-toplevel)"
rg -c 'MEMORY\.md' plugins/project-memory/ -g '*' | sort
rg -n 'INDEX\.md' plugins/project-memory/
rg -n '\bINDEX\b' plugins/project-memory/
```

Expected: every plugin file that names the index names `MEMORY.md`; the
second command prints EXACTLY TWO lines — the core rule's pre-rename
detection ("holding an `INDEX.md` and no `MEMORY.md`") and the
conventions rule's old-name offer ("still named `INDEX.md`"). The third
command prints exactly THREE lines: those two plus the untouched
pre-existing eval query in
`skills/memory-review-session/evals/trigger-evals.json`. Any other line
fails the task.

- [ ] **Step 2: Glossary-ban sweep over the shipped plugin content**

Run: `git diff develop... -- plugins/ | rg -i 'native memor|hybrid mode|hybrid memory' || echo CLEAN`
Expected: `CLEAN`. The sweep deliberately covers only `plugins/` — the
spec, this plan, and the glossary's `_Avoid_` lists legitimately quote
the banned terms; the shipped plugin content may not use them.

- [ ] **Step 3: Untouched-proof**

Run: `git status --porcelain -- plugins/ | rg -v 'project-memory' || echo CLEAN`
Expected: `CLEAN` (no stray edits in other plugins, committed or not).

Run: `git diff --name-only develop... -- plugins/ | rg -v 'project-memory' || echo CLEAN`
Expected: `CLEAN`.

- [ ] **Step 4: Flip lifecycle status**

The two architect rounds and their dispositions are recorded in the
spec's Review rounds section; the fresh-round verdict is annotated
resolved. With the developer's confirmation, set `status: implemented` in
the spec's and this plan's frontmatter (Edit tool), then commit both with
any remaining `docs/` changes of this work:

```bash
git add docs/specs/2026-08-12-memory-hybrid-design.md docs/plans/2026-08-12-memory-hybrid.md
git commit -m "docs: spec and plan for the memory hybrid"
```

(Commit only with the developer's authorization, as always.)
