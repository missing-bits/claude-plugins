---
ticket: none
date: 2026-08-17
status: approved
adversary: concerns (resolved 2026-08-17)
branch: feature/background-verdict-dispatch
base: develop
---

# Background Verdict Dispatch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Verdict agents (`architect`, `plan-adversary`) dispatch in the background with notification→relay→stamp mechanics, per `docs/specs/2026-08-17-background-verdict-dispatch-design.md`.

**Architecture:** One canonical dispatcher sequence lands as an end-of-file subsection of the always-on workflow rule; both agent files gain `background: true` (exactly the spec's enumeration), a pointer phrase in the description, and a self-describing report subject; the lifecycle rule's closing sentence gains the relay-then-stamp ordering with an edited-together marker; the README's agent bullets and model-selection section follow. Content lands first, the dogfood version bump last, so the cache never serves pre-edit content under the first-pass string — any later content fix re-mints the discriminator (Task 8). No code — every deliverable is rule text, agent frontmatter, or README prose.

**Tech Stack:** Claude Code plugin content (Markdown rules, agent frontmatter), `claude plugin validate`, git.

## Global Constraints

- Public repo: English only, no machine paths, no company names (repo-hygiene rule).
- Commits: one line, conventional prefix `type(scope):`, no body, no trailers (no `Co-Authored-By`).
- Frontmatter safety: any YAML scalar containing `: ` stays double-quoted; `claude plugin validate` does NOT check `rules/` files — review their frontmatter by hand.
- Rule text mentions skills/agents conditionally ("when available") — rules load for people without the plugin.
- Never force-add ignored files; tracked `docs/` documents ride the closing commit (Task 9), not per-task commits.
- `claude plugin validate .` and `claude plugin validate plugins/working-process` must pass before every commit.
- The spec is the contract: wording below is copied from it; on a conflict the spec wins. The spec's change enumeration binds shipped BEHAVIOR; user-facing docs (the README, Task 6) follow the repo convention that they match shipped behavior, extending the enumeration without amending it.
- Prescribed tiers for this plan's own review rounds: the architect on the most capable available family; the plan-adversary one family below it (a small mechanical plan) — rounds 1–3 ran exactly there (opus, below fable), so no fallback record applies. A dispatch below these tiers lands the `*-fallback: <family> (chosen <date>)` record in the same stamp edit, resolved or waived before Task 9's flip.
- Rollout pairing: the plugin version delivers agent frontmatter immediately; the dispatcher sequence reaches a project only through a rules re-sync. The reverse window degrades sanely — the previously installed rules still carry the old "record the verdict" obligation, so no round is lost — and Task 6 states the pairing where users see it.

---

### Task 1: Topic branch and frontmatter branch fields

**Files:**
- Modify: `docs/specs/2026-08-17-background-verdict-dispatch-design.md` (frontmatter: `branch`, `base`)
- Modify: `docs/plans/2026-08-17-background-verdict-dispatch.md` (frontmatter: `branch`, `base`)

**Interfaces:**
- Consumes: `develop` at its current head.
- Produces: branch `feature/background-verdict-dispatch` (base `develop`) that every later task commits to. No commit in this task — `docs/` changes ride Task 9's closing commit.

- [ ] **Step 1: Create the topic branch off develop**

```bash
git checkout develop
git checkout -b feature/background-verdict-dispatch
```

- [ ] **Step 2: Record branch and base in the spec and plan frontmatter**

Append to BOTH documents' YAML frontmatter as the LAST fields — the documented field order puts `branch`/`base` after the review fields (spec-plan-lifecycle rule):

```yaml
branch: feature/background-verdict-dispatch
base: develop
```

- [ ] **Step 3: Verify placement**

Run: `rg -n "^(branch|base):" docs/specs/2026-08-17-background-verdict-dispatch-design.md docs/plans/2026-08-17-background-verdict-dispatch.md`
Expected: two matches per file, with line numbers inside each YAML frontmatter block — the block's final fields, directly above the closing `---`.

- [ ] **Step 4: Cross the implementation-ready gate**

Gate: this plan's standing `adversary:` verdict must first be `LGTM`
or carry the `(resolved <date>)` annotation with its body note — a
document is never approved-and-blocking. Then, with the developer's
explicit go-ahead (never silently), flip BOTH documents' frontmatter
to `status: approved` — the lifecycle's implementation-ready gate: the
plan is approved and implementation is about to start. This is also
where the process suggests committing the `docs/` documents;
committing stays with the developer, and the documents otherwise ride
Task 9's closing commit.

---

### Task 2: Dispatcher-sequence subsection in the workflow rule

**Files:**
- Modify: `plugins/working-process/rules/workflow.md`

**Interfaces:**
- Consumes: the rule's current structure — numbered steps 1–6, a standalone paragraph "After every round of the `architect` agent or plan-adversary, record the verdict…", then model-selection, consultation-dispatch, glossary, and elements-of-style paragraphs.
- Produces: a `## Dispatching a verdict agent` subsection at the END of the file (so the unrelated trailing paragraphs stay outside it); the standalone verdict-recording paragraph REMOVED (folded — no third restatement); steps 3 and 5 referencing the subsection.

- [ ] **Step 1: Delete the standalone verdict-recording paragraph**

Delete this paragraph (currently after step 6), including its trailing blank line:

```markdown
After every round of the `architect` agent or plan-adversary, record the
verdict (`LGTM` | `concerns` | `blocking`) in the reviewed document's
`architect:` / `adversary:` frontmatter field. A consultation
(`*-consult`) produces no verdict and nothing to record.
```

- [ ] **Step 2: Append the subsection at the end of the file**

After the elements-of-style paragraph (the file's current last paragraph), append:

```markdown
## Dispatching a verdict agent

Dispatching a verdict agent (`architect`, `plan-adversary`), when
available:

- From an interactive session the dispatch always runs in the
  background — a review never blocks the session, mirroring the
  review-reports rule's precedent. A run with no interactive
  dispatcher cannot relay, so it never stamps; the next interactive
  touch closes the round through the lifecycle rule's re-offer loop.
- Before dispatch, resolve any undecided Process directory
  (`docs/specs/`, `docs/plans/`) so the first-create question cannot
  interrupt the stamp turn.
- At dispatch, tell the developer the round is running in the
  background and its result will arrive as a task notification, with
  progress visible in the session's task list. (This bullet is part of
  the spec's sequence — added there 2026-08-17, routed from this
  plan's adversary round 4.)
- On the completion notification, in one turn and in this order:
  verify the agent's model self-report (the comparison the lifecycle
  rule defines), relay the report to the developer, then stamp the
  verdict (`LGTM` | `concerns` | `blocking`) into the reviewed
  document's `architect:` / `adversary:` frontmatter field.
- The relay carries the verdict, the model self-report, and every
  finding in substance — condense narrative prose, never drop a
  finding or its severity.
- The stamp — the field, any fallback record, and the round record
  the lifecycle rule defines — lands as one edit, body record first
  where edit granularity forces separate writes, and goes to the
  document named in the report, never to "the most recent dispatch".
- The sequence ends the delivery, not the loop: after relay and stamp
  the session may fix the document and dispatch a fresh round, or put
  its questions to the developer first.
- At most one live round per document per field within the session;
  superseding a running round stops it when the platform offers a
  stop, otherwise the stale result is relayed as stale and never
  stamped.
- When the reviewed document changed after dispatch — known only
  conversationally; an out-of-session edit is accepted as
  undetectable — the relay says so and the stamp waits for the
  developer's call.
- When compaction leaves an in-flight dispatch unclear, check the task
  list rather than guess, and never fabricate a pending result.
- An agent that dies or returns nothing is an ordinary error: relay
  the failure and offer a fresh dispatch on the same tier.
- A consultation (`*-consult`) produces no verdict and nothing to
  record.

This subsection and the lifecycle rule's relay-then-stamp sentence
state the same ordering and are edited together.
```

- [ ] **Step 3: Reference the subsection from steps 3 and 5**

In step 3, replace:

```markdown
   working-process `architect` agent (when available); stamp its verdict
   into the spec's `architect:` frontmatter field.
   Dispatch it on the most capable available model, named explicitly.
```

with:

```markdown
   working-process `architect` agent (when available); dispatch and
   stamping follow the verdict-agent dispatch subsection below.
   Dispatch it on the most capable available model, named explicitly.
```

In step 5, replace:

```markdown
   offer a working-process plan-adversary agent dispatch (when
   available); stamp its verdict into the plan's `adversary:` field.
```

with:

```markdown
   offer a working-process plan-adversary agent dispatch (when
   available); dispatch and stamping follow the verdict-agent dispatch
   subsection below.
```

- [ ] **Step 4: Verify structure and no third restatement**

Run: `rg -n "^## " plugins/working-process/rules/workflow.md`
Expected: exactly one match — `## Dispatching a verdict agent` (the file has no other `##` heading).
Run: `tail -2 plugins/working-process/rules/workflow.md`
Expected: the edited-together closing sentence — proving the subsection ends the file.
Run: `rg -c "After every round of" plugins/working-process/rules/workflow.md`
Expected: no match (the phrase sits on one line in the deleted paragraph; "record the verdict" itself is line-wrapped in the source and would never match).
Run: `rg -c "stamp the" plugins/working-process/rules/workflow.md`
Expected: `1` (the subsection's ordering bullet).

- [ ] **Step 5: Validate and commit**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both PASS.

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): verdict-agent dispatch sequence in workflow rule"
```

---

### Task 3: Architect agent — full background pattern and self-describing report

**Files:**
- Modify: `plugins/working-process/agents/architect.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: `background: true` — exactly the spec's enumeration, nothing beyond it (`disallowedTools` was considered and dropped: ADR 0001 scopes it to consult agents, and it cannot prevent a dispatcher-side resumption anyway); the description's pointer phrase (exact wording below, shared verbatim with Task 4); a report whose opening is claimed by exactly one labeled line — `**Subject**:` with the document path, then the model self-report.

- [ ] **Step 1: Add the frontmatter keys and description phrase**

Append to the end of the quoted `description` string (inside the closing quote, after "Dispatch on the most capable available model."):

```
 Runs in the background; the verdict arrives as a task notification, and the dispatcher stamps after relay, not before.
```

Below the `description:` line add:

```yaml
background: true
```

- [ ] **Step 2: Reword the Assumed-domains opener claim**

In the "Domains — hybrid inference" section, replace:

```markdown
- Questions mid-run are impossible, so declare instead: every report
  opens with an **Assumed domains** section — each domain, where it came
  from (hint / inferred), and your confidence, stated in plain words when
  low. A wrong inference must be visible at the top of the report and
  cheap to fix by a re-dispatch with a corrected hint.
```

with:

```markdown
- Questions mid-run are impossible, so declare instead: the report
  carries an **Assumed domains** section as its first numbered
  section — each domain, where it came from (hint / inferred), and your
  confidence, stated in plain words when low. A wrong inference must be
  visible near the top of the report and cheap to fix by a re-dispatch
  with a corrected hint.
```

- [ ] **Step 3: Reconcile the report opener**

In the "Report" section, replace:

```markdown
The report opens with a one-line **model self-report** — the model this
review actually ran on, as family plus version (e.g. "opus 4.8") —
before any section; the dispatcher compares it against the dispatched
and prescribed tiers before stamping.
```

with:

```markdown
The report opens with a labeled **Subject** line — the path of the
reviewed document (a bare question has no path — say so instead) —
then a one-line **model self-report** — the model this review actually
ran on, as family plus version (e.g. "opus 4.8") — before any section.
The dispatcher routes the stamp by the Subject line and compares the
self-report against the dispatched and prescribed tiers before
stamping.
```

- [ ] **Step 4: Verify exactly one opener claim, validate, commit**

Run: `rg -c "opens with" plugins/working-process/agents/architect.md`
Expected: `1`.
Check: the `description` value still opens and closes with one double quote and contains no unescaped `"`.
Run: `claude plugin validate plugins/working-process`
Expected: PASS.

```bash
git add plugins/working-process/agents/architect.md
git commit -m "feat(working-process): architect runs in background with self-describing report"
```

---

### Task 4: Plan-adversary agent — full background pattern and subject key

**Files:**
- Modify: `plugins/working-process/agents/plan-adversary.md`

**Interfaces:**
- Consumes: the same description phrase as Task 3 (verbatim).
- Produces: `background: true` — exactly the spec's enumeration; JSON output with a `subject` key the dispatcher routes the stamp by.

- [ ] **Step 1: Add the frontmatter keys and description phrase**

Append to the end of the (unquoted) `description` value, after "never the cheapest family.":

```
 Runs in the background; the verdict arrives as a task notification, and the dispatcher stamps after relay, not before.
```

The appended text contains no `: `, so the scalar stays safe unquoted.
Below the `description:` line add:

```yaml
background: true
```

- [ ] **Step 2: Add the `subject` key to the Output block**

Replace:

```
    {
      "model": "<family plus version this review actually ran on, e.g. opus 4.8>",
```

with:

```
    {
      "subject": "<path of the reviewed plan — the dispatcher routes the stamp by this, never by dispatch order>",
      "model": "<family plus version this review actually ran on, e.g. opus 4.8>",
```

- [ ] **Step 3: Validate and commit**

Run: `claude plugin validate plugins/working-process`
Expected: PASS.

```bash
git add plugins/working-process/agents/plan-adversary.md
git commit -m "feat(working-process): plan-adversary runs in background with subject-keyed output"
```

---

### Task 5: Lifecycle rule — relay-then-stamp ordering

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md`

**Interfaces:**
- Consumes: Task 2's subsection (the edited-together counterpart).
- Produces: the ordering sentence in the lifecycle rule, marked edited-together.

- [ ] **Step 1: Edit the closing sentence of the Lifecycle-offers paragraph**

Replace:

```markdown
After any
review round, stamp the verdict into the document's field.
```

with:

```markdown
After any
review round, relay the report to the developer, then stamp the
verdict into the document's field — this sentence and the workflow
rule's verdict-agent dispatch subsection state the same ordering and
are edited together.
```

- [ ] **Step 2: Verify the pairing exists on both sides**

Run: `rg -l "edited together" plugins/working-process/rules/`
Expected: both `workflow.md` and `spec-plan-lifecycle.md` listed.

- [ ] **Step 3: Validate and commit**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both PASS.

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): relay-then-stamp ordering in lifecycle rule"
```

---

### Task 6: README — agent bullets, model-selection contrast, rollout pairing

**Files:**
- Modify: `plugins/working-process/README.md`

**Interfaces:**
- Consumes: Tasks 3–4 shipped frontmatter (the README must match it).
- Produces: user-facing text consistent with background verdict dispatch, plus the rollout-pairing note.

- [ ] **Step 1: Update the architect bullet**

Replace:

```markdown
  `architect:` frontmatter field by the dispatcher. Dispatched on the most capable available model.
```

with:

```markdown
  `architect:` frontmatter field by the dispatcher. Dispatched in the
  background on the most capable available model; the verdict arrives
  as a task notification and is stamped after the dispatcher relays
  the report.
```

- [ ] **Step 2: Update the plan-adversary bullet**

Replace:

```markdown
  come from `*-plan-review` checklist skills. Dispatched scaled to the
  plan's size and risk.
```

with:

```markdown
  come from `*-plan-review` checklist skills. Dispatched in the
  background, scaled to the plan's size and risk; the verdict arrives
  as a task notification and is stamped after relay.
```

- [ ] **Step 3: Fix the model-selection contrast and add the rollout pairing**

In the "Model selection" section, replace (full source lines, the last
one ending mid-sentence):

```markdown
Consultations (the `*-consult` agents) dispatch on the most capable
available model as named background agents; they return no verdict, so
the fallback machinery below never applies to them. The model is always named explicitly at dispatch, and
```

with (re-wrapped to the file's width, the trailing sentence start
preserved):

```markdown
Consultations (the `*-consult` agents) dispatch on the most capable
available model; like the verdict agents, they run as named background
agents — consultations return no verdict, so the fallback machinery
below never applies to them. The verdict agents' relay-then-stamp
sequence lives in the workflow rule's Rules payload: after a plugin
update, run a rules re-sync so the dispatcher side of the behavior
matches the agents (until then the previously installed rules still
carry the older record-the-verdict obligation, so no round is lost).
The model is always named explicitly at dispatch, and
```

- [ ] **Step 4: Validate and commit**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both PASS.

```bash
git add plugins/working-process/README.md
git commit -m "docs(working-process): background verdict dispatch in README"
```

---

### Task 7: Dogfood version bump — after all content

**Files:**
- Modify: `plugins/working-process/.claude-plugin/plugin.json` (the `version` field)

**Interfaces:**
- Consumes: Tasks 2–6 committed (the content the string must key).
- Produces: version `0.14.0-dev.background-verdict-dispatch` minted AFTER every content edit, so the cache can never serve pre-edit content under this string.

- [ ] **Step 1: Set the dogfood version**

In `plugins/working-process/.claude-plugin/plugin.json` change:

```json
  "version": "0.13.0",
```

to:

```json
  "version": "0.14.0-dev.background-verdict-dispatch",
```

- [ ] **Step 2: Validate and commit the bump alone**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both PASS.

```bash
git add plugins/working-process/.claude-plugin/plugin.json
git commit -m "chore(working-process): dogfood version for background-verdict-dispatch"
```

---

### Task 8: Dogfood verification — developer-driven, both agents, fresh session

**Files:**
- No file changes; verification only.

**Interfaces:**
- Consumes: everything above, live under the dogfood version.
- Produces: the spec's verification stage two (shipped artifacts), for BOTH verdict agents.

- [ ] **Step 1: Make the shipped content live — STOP, developer-driven**

STOP and hand this step to the developer on their explicit go-ahead — a marketplace change, a plugin update, and a sync-rules run mutate the developer's installed state and are never run unbid (the review-reports, memory-hybrid, and memory-entry-format plans' precedent). The installed `missing-bits` marketplace is a GitHub clone pinned to released `master`, so it can never serve the dogfood version. With the developer driving: add (or update) a marketplace sourced from this checkout — `/plugin marketplace add <path to this repo root>` — install or update `working-process` from THAT marketplace, then run the `working-process:sync-rules` skill so the installed Rules payload picks up the new subsection and lifecycle sentence. The executor resumes at Step 2.

- [ ] **Step 2: Confirm the served version AND the installed content**

Run: `claude plugin list 2>/dev/null | grep -A1 working-process`
Expected: `0.14.0-dev.background-verdict-dispatch` (the string only — content follows).
Run: `rg -c "Dispatching a verdict agent" "$HOME/.claude/rules/working-process/workflow.md"` and `rg -c "edited together" "$HOME/.claude/rules/working-process/spec-plan-lifecycle.md"` — checking the project-level copy instead when that is the installed one.
Expected: `1` each. On a miss STOP — the dispatching session would run against the stale rules (the review-contract-sharpening plan's dogfood-gate precedent).

- [ ] **Step 3: Exercise an architect dispatch — a real round**

In a fresh session started after Step 1 (a running session keeps pre-sync rules), dispatch the `architect` agent on `docs/specs/2026-08-17-background-verdict-dispatch-design.md` (a real grilled document — no bare-question substitute, which would demonstrate neither the Subject opener nor stamp routing), on the most capable available model, named explicitly at dispatch. This is a live round: its verdict is stamped and its round record appended to the spec body like any other. Confirm the observables that prove the updated files loaded: the report opens with the labeled Subject line then the model self-report, the verdict arrives as a task notification, and the session relays before stamping. The immediate return is context, not evidence — background is the Agent tool's default, so a stale cache would also return immediately.
Expected: all three observed; any miss is a defect to fix before the release PR.

- [ ] **Step 4: Exercise a plan-adversary dispatch — a real round**

In the same fresh session, dispatch `plan-adversary` on `docs/plans/2026-08-17-background-verdict-dispatch.md` (this plan), one family below the most capable available model (a small mechanical plan), named explicitly at dispatch. This too is a live round: stamped and recorded in the plan body. Confirm: the dispatch returns immediately, the JSON output carries the `subject` key with the plan's path, and the session relays before stamping.
Expected: all three observed.

- [ ] **Step 5: Re-mint on any post-mint content fix**

Any content edit made after Task 7 minted the version string bumps the discriminator (`0.14.0-dev.background-verdict-dispatch-2`, `-3`, …) in its fix commit, then repeats Steps 1–2 before re-running Steps 3–4 — the cache keys content by version string, so a fix under an unchanged string re-dogfoods stale content (the design-personas topic needed three such re-mints).

- [ ] **Step 6: Final validation sweep**

Run: `claude plugin validate . && claude plugin validate plugins/working-process && rg -c "edited together" plugins/working-process/rules/workflow.md plugins/working-process/rules/spec-plan-lifecycle.md`
Expected: validations PASS; each rule file reports exactly `1`.

---

### Task 9: Closing — lifecycle flips and docs commit

**Files:**
- Modify: `docs/specs/2026-08-17-background-verdict-dispatch-design.md` (frontmatter `status`)
- Modify: `docs/plans/2026-08-17-background-verdict-dispatch.md` (frontmatter `status`, checked boxes)

**Interfaces:**
- Consumes: Task 8 passed; every round record present in both documents.
- Produces: the closed lifecycle the two preceding plans end with.

- [ ] **Step 1: Reconcile round records and review fields**

Check both documents' "Review rounds" sections list every architect/adversary round with verdict, model, and date — including Task 8's dogfood rounds. Reconcile the frontmatter fields: a verdict resolved without a fresh round carries the `(resolved <date>)` annotation with its body note; a live fallback record is resolved (fresh prescribed-tier round) or waived. STOP: a non-LGTM dogfood verdict that is neither resolved nor annotated blocks Step 2.

- [ ] **Step 2: Flip lifecycle status — with the developer's confirmation**

With the developer's explicit go-ahead (never silently), move `status: approved` → `status: implemented` in the spec and the plan (Task 1 Step 4 crossed the `draft` → `approved` gate).

- [ ] **Step 3: Commit the docs**

The glossary rides this commit because the grilling session edited it (two terms: Verdict agent, Relay) outside the plan's tasks and it is still uncommitted.

```bash
git add docs/specs/2026-08-17-background-verdict-dispatch-design.md docs/plans/2026-08-17-background-verdict-dispatch.md docs/domain/glossary.md
git commit -m "docs: background-verdict-dispatch spec, plan, and glossary terms"
```

- [ ] **Step 4: Offer the memory review**

The memory-review-session skill is available and a document just moved to `implemented`: offer the Project memory review (released work-state notes close, resolved entries sweep to the archive). The developer may decline.

## Review rounds

### 2026-08-17 — plan-adversary, opus, blocking (round 1)

Six Important, six Minor; all twelve addressed the same day in this
revision: subsection moved to end-of-file in bullet form (I1, M7);
the third "opens with" claim reconciled (I2); an adversary dogfood
dispatch added (I3); the version bump moved after the content commits
with an explicit plugin update and a fresh-session requirement (I4);
the rollout window analyzed — old installed rules keep the
record-the-verdict obligation, so no round is lost — and paired in the
README (I5); a closing task added mirroring the two preceding plans
(I6); `branch`/`base` appended last per the documented field order
(M8); the version-bump commit unbundled from docs (M9);
`disallowedTools: SendMessage` added to both agents, resumption of a
verdict round ruled out (M10); the bare-question alternative dropped
from the dogfood step (M11); the README's consumer lines enumerated
(M12).

### 2026-08-17 — plan-adversary, opus, blocking (round 2)

Five Important, five Minor; nine fixed the same day in this revision,
one rejected with counter-evidence:

1. Installed-copy content checks added to the dogfood task, with the
   marketplace refresh and a stop-on-miss (I1).
2. A discriminator re-mint step added for post-mint content fixes; the
   Architecture cache claim scoped to the first pass (I2).
3. Dogfood dispatches declared real rounds — stamped, recorded — with
   field reconciliation and a non-LGTM stop before the flip (I3).
4. `disallowedTools: SendMessage` dropped from both agents: it exceeds
   the spec's change enumeration, ADR 0001 scopes its rationale to
   consult agents, and the key cannot prevent resumption anyway (I4).
5. The `approved` gate restored: Task 1 flips both documents to
   `approved` with the developer's go-ahead; Task 9 moves
   `approved` → `implemented` (I5).
6. Dogfood dispatch models named explicitly (M6).
7. The subsection now cites the lifecycle rule for the self-report
   comparison and the round record instead of restating them (M7).
8. The architect's routing line gains the `**Subject**:` label,
   mirroring the JSON key (M8).
9. Task 2's structural verification restated to what rg/tail can
   actually prove (M9).
10. Rejected — glossary staging in the closing commit: `git status`
    shows `docs/domain/glossary.md` modified and uncommitted (the
    grilling session's two terms), so the staging is correct; a note
    now says why the glossary rides that commit (M10).

### 2026-08-17 — plan-adversary, opus, blocking (round 3)

One Critical, three Important, four Minor; six fixed the same day, two
rejected (one partially) with counter-evidence:

1. Critical — the dogfood string was a prerelease of the released and
   installed 0.13.0, sorting below it and reducing the release to a
   no-op: re-minted as `0.14.0-dev.background-verdict-dispatch`, the
   re-mint ladder rebased (C1).
2. The Task 1 placement check read the wrong end of the file — now an
   anchored rg on the frontmatter (I2).
3. Task 8 retitled developer-driven, with a STOP handing the
   marketplace refresh, plugin update, and sync-rules run to the
   developer on explicit go-ahead (I3).
4. Partially rejected — the claim that rounds 1–3 ran "at the top
   family": they ran on opus, one family below the most capable
   (fable), which IS the prescribed tier for a small mechanical plan,
   so no fallback record applies. The valid core — the plan never
   declared its prescribed tier — fixed with a Global Constraints line
   (I4).
5. Rejected — moving the subsection after the consultation paragraph
   re-raises round 1's finding I1 in reverse: mid-file placement puts
   the glossary and elements-of-style paragraphs under the new `##`
   heading, exactly what round 1 blocked. End-of-file placement
   stands; recorded as a reviewer flip-flop (M5).
6. A dispatch-time announcement bullet added to the subsection (M6).
7. Task 1's approved flip gated on the adversary verdict being LGTM or
   annotated resolved (M7).
8. A Global Constraints line reconciles the two readings of "the spec
   is the contract": the enumeration binds behavior; user-facing docs
   follow shipped behavior by repo convention (M8).

### 2026-08-17 — plan-adversary, opus, concerns (round 4)

One Important, four Minor, all fixed the same day; the reviewer also
re-checked and upheld the round-2/3 rejections:

1. The make-live path could not deliver topic-branch content — the
   installed missing-bits marketplace is a GitHub clone pinned to
   released master. Task 8 Step 1 now adds a checkout-sourced
   marketplace and updates from it, per the earlier plans' precedent
   (I1).
2. The paragraph-gone check was vacuous (the phrase is line-wrapped in
   the source) — re-anchored on the one-line fragment "After every
   round of" (M2).
3. The dispatch-time announcement bullet exceeded the spec's
   enumeration — routed into the spec as a one-line sequence addition,
   recorded there (M3).
4. "Returns immediately" proves nothing (background is the Agent
   tool's default) — the discriminating observables are now named: the
   Subject line and the subject key; immediacy demoted to context
   (M4).
5. The README quote started and ended mid-line — re-quoted as full
   lines with the replacement re-wrapped (M5).

Resolution note, 2026-08-17: all five round-4 findings fixed in this
revision (the list above says how); the developer accepted the
resolution in place of a fifth round after the 12→10→8→5 convergence
across four rounds.
