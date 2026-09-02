---
ticket: none
date: 2026-09-02
status: draft
spec: ../specs/2026-09-02-ledger-as-finding-state-design.md
branch: feature/audit-errata
base: develop
---

# Ledger as Finding State Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the disposition ledger's grammar so the leading token names a state and a clause names the authorizer, replacing five states with four and moving two shipped rules off the token they currently discriminate on.

**Architecture:** Two rule files change and one spec is normalized. `spec-plan-lifecycle.md` owns the record — states, shapes, clauses, gate lines, the Unfinished-work list. `workflow.md` owns the loop's behaviour — the tripwire, the terminators, the cap, what a round reads. The split follows the two rules' existing division of labour, so no sentence moves between them beyond what each task names.

**Tech Stack:** Markdown rule files distributed as a Rules payload; `rg` commands published inside the rules are the enforcement mechanism; `claude plugin validate` is the structural check.

## Global Constraints

- **No code.** Every deliverable is prose in a Markdown file. The verification for each task is a grep whose result changes, plus `claude plugin validate`.
- **Edit with the Edit tool, never `sed -i` or `printf >>`** — the process-artifacts rule requires it for artifacts under `docs/` and applies equally to rule files here.
- **Line width follows each file's existing habit** — prose wraps at ~72 characters; the indented grammar blocks and `rg` command lines run long and stay on one line.
- **Public-repo hygiene:** English only, no machine-specific paths, no company or client names.
- **`claude plugin validate .` and `claude plugin validate plugins/working-process` must both pass** after every task.
- **Historical ledger lines are never rewritten** to the new grammar. One task normalizes exactly one line, for a reason that task states.
- **No version bump.** `plugins/working-process/.claude-plugin/plugin.json` already carries `0.14.0-dev.audit-errata`; the release PR mints the real number. This branch dogfoods through `--plugin-dir` and project-level rules, neither of which is cache-keyed, so the discriminator needs no re-mint.
- **The spec is the source.** Where this plan and `docs/specs/2026-09-02-ledger-as-finding-state-design.md` disagree, the spec wins and the plan is wrong.

---

### Task 1: The four states, their shapes, and the write-ahead discipline

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the shapes block and bullets under `## The disposition ledger`

**Interfaces:**
- Produces: the four leading tokens `open`, `held`, `fixed <date>`, `declined <date>`, and the rule that a severity bracket is omitted when both legs hold. Tasks 2, 3, 5 and 7 all name these tokens.

- [ ] **Step 1: Write the failing check**

```bash
# The old five-shape block must still be present, and the new tokens absent.
grep -c '^    - resolved <date> — \[<severity>\]' plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '^    - declined <date>' plugins/working-process/rules/spec-plan-lifecycle.md
```

- [ ] **Step 2: Run it to confirm the starting state**

Expected: first command prints `1`, second prints `0`.

- [ ] **Step 3: Replace the shapes block**

Replace these five lines:

```
    - fixed — [<severity>] <claim>; license: <citation>; <what changed>
    - held — [<severity>] <claim>; question: <one short question>[; counter: <counter-evidence>]
    - open — [<severity>] <claim>
    - resolved <date> — [<severity>] <claim>; landed in <section>
    - resolved <date> (declined) — [<severity>] <claim>; <why the document stands>
```

with these four, plus the bracketless variant and the paragraphs that follow:

```
    - open — [<Severity>] <claim>
    - held — [<Severity>] <claim>; question: <one closed question>; options: <the options and the session's recommendation>
    - fixed <date> — [<Severity>] <claim>; <authorizer>; <what changed>
    - declined <date> — [<Severity>] <claim>; <authorizer>; <why the document stands>

The severity bracket is omitted on a line whose sole authorizer is
`ruling:` **and** which no reviewer graded — both legs, never one:

    - fixed <date> — <claim>; ruling: <date>; <what changed>

`open` and `held` are the non-terminal states, and the only two the
Unfinished-work list anchors. `fixed` and `declined` are terminal and
say what became of the document: it changed, or it stands.

The two dates on a terminal line record different events and are both
written even when they coincide. The leading date is when the line
reached its terminal state; `ruling:` is when the decision it cites was
taken. On an ordinary developer-authorized line the two are the same day
and say so; on a fold they differ, and that divergence is the point of
carrying both.

The severity slot is a reviewer's grade, so it is omitted exactly where
there is none: a change the developer directed mid-round is not a
finding, and inventing a grade for it would be the same manufacture the
authorizer rule forbids. This adds no fourth severity value; the
glossary's three stand.

`fixed` and `resolved` merge because they were never two states. Both
mean the document changed on account of this finding, and they differed
only in who authorized it, which is now a clause. Merging also frees a
word the rules used for two objects — `concerns (resolved <date>)`
annotates a verdict, while `resolved <date>` annotated a finding.
```

- [ ] **Step 4: Replace the four state bullets below the block**

Replace the `open` / `fixed` / `held` / `resolved <date>` bullets with:

```
- `open` — written at stamp time, before the findings are triaged. An
  `open` line surviving a session means the remediation never ran, and
  the document's next touch re-offers it.
- `held` — the finding needs the developer. The line carries the
  concrete question and the options with the session's recommendation;
  where the finding is disputed or contested, `counter:` carries the
  evidence the developer needs in order to answer, and the oscillation
  tripwire's named flip is that evidence.
- `fixed <date>` — the document changed on account of this finding. Its
  authorizer says who decided: `license:` where the session cited a
  written decision, `ruling:` where the developer did.
- `declined <date>` — the document stands. It always carries `ruling:`,
  because declining is a decision and triage gives a session no license
  to decide.
```

- [ ] **Step 5: Add the write-ahead paragraph**

Immediately after those bullets, add:

```
Each disposition line is written before the edit it describes, or with
it — never batched at the end of a wave. The dangerous failure is not a
session dying mid-round but a fix wave half-applied with no lines
written: the body has changed, nothing says which change belongs to
which finding, and the next round's brief reads a diff source that is
silently wrong. Writing contemporaneously makes a partial wave
self-evident, since `open` and `fixed` lines mixed under one heading say
exactly where the session stopped.
```

- [ ] **Step 6: Run the check again**

Expected: first command prints `0`, second prints `1`.

- [ ] **Step 7: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both print `✔ Validation passed`.

- [ ] **Step 8: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): four ledger states, authorizer as a clause"
```

---

### Task 2: The clause table

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — after the state bullets from Task 1

**Interfaces:**
- Consumes: the four tokens from Task 1.
- Produces: the clause names `license:`, `ruling:`, `question:`, `options:`, `counter:`, `deviation:`. Tasks 5, 8 and 10 name `license:` and `ruling:`.

- [ ] **Step 1: Write the failing check**

```bash
grep -c '^| `ruling: <date>` |' plugins/working-process/rules/spec-plan-lifecycle.md
```

- [ ] **Step 2: Run it**

Expected: `0`.

- [ ] **Step 3: Add the table and its two rules**

After Task 1's write-ahead paragraph, add:

```
The leading token is a queryable state. Clauses are payload.

| clause | carries | on |
|---|---|---|
| `license: <citation>` | the written decision the session acted on | `fixed` |
| `ruling: <date>` | the developer authorized it; on a fold, the prior ruling's date followed by `folding <section or line quote>` naming what it folds against | `fixed`, `declined` |
| `question:` | the question, phrased so one short answer resolves it | `held` |
| `options:` | the options and the session's recommendation | `held` |
| `counter:` | the session's evidence where the finding is disputed or contested | `held` |
| `deviation: <section>` | where the rationale for departing from a reviewer's suggestion lives | `fixed` |

`question:` and `options:` are both required on a `held` line: the batch
that relays them is a transcript, and a session that dies between the
relay and the answer leaves the next session to re-derive the options,
possibly differently, so the developer answers a question that silently
changed. `counter:` and `deviation:` are conditional, written whenever
their condition holds.

Every terminal line carries exactly one authorizer.

Payload costs nothing structurally. Four of the five Unfinished-work
commands anchor a frontmatter field and are held to the frontmatter
block by the list's default scope guard, so no body line reaches them at
all; the fifth is this ledger's own, anchored on `^- `, which an indented
continuation does not match. Payload under a line is therefore invisible
to every published command, and where it runs long it belongs in
indented sub-bullets rather than in a longer line.
```

- [ ] **Step 4: Run the check again**

Expected: `1`.

- [ ] **Step 5: Verify the anchor claim against the file itself**

```bash
grep -c "rg -[a-z]* --no-ignore --crlf '\^" plugins/working-process/rules/spec-plan-lifecycle.md
grep -c "rg -n --no-ignore --crlf '\^- " plugins/working-process/rules/spec-plan-lifecycle.md
```

Expected: `6` and `1` — six published commands in the file, of which one anchors `^- `. Five of the six are Unfinished-work entries; the sixth is the `revises:` lookup, which is not one. If the first number is not 6, the claim "four of the five" is wrong and must be recounted before committing.

- [ ] **Step 6: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): the ledger's clause table"
```

---

### Task 3: Historical shapes, the pre-merge sentence, and lawful prose

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — after the clause table

**Interfaces:**
- Consumes: the merge from Task 1.
- Produces: the statement that `resolved <date>` and `resolved <date> (declined)` remain parseable historical forms. Task 5's fold and Task 11's normalization both rely on it.

- [ ] **Step 1: Write the failing check**

```bash
grep -c 'described historical forms' plugins/working-process/rules/spec-plan-lifecycle.md
```

- [ ] **Step 2: Run it**

Expected: `0`.

- [ ] **Step 3: Add the paragraph**

```
Ledger lines written before this merge stay as written, as the `scope`
token's introduction already established. The shapes they use —
`resolved <date>` and `resolved <date> (declined)` — are kept here as
described historical forms rather than deleted: a reader must still
parse pre-merge documents, and a fold against a pre-design settled line
cites a date off a token the live grammar no longer produces.

Narrative prose between the lines of a `## Review rounds` section is
lawful and expected. This grammar governs headings, lines, and their
indented payload; a paragraph explaining why a wave went the way it did
belongs there too. A lint over the section reads the anchored lines and
ignores the prose.
```

- [ ] **Step 4: Run the check again**

Expected: `1`.

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): retain historical ledger shapes, permit prose"
```

---

### Task 4: The gate discriminator

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md:~185-195` — the paragraph under `### Gate lines` beginning "Both are written at gate time"

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: no new names.

- [ ] **Step 1: Write the failing check**

```bash
grep -c 'The date each line carries tells a gate episode apart' plugins/working-process/rules/spec-plan-lifecycle.md
```

- [ ] **Step 2: Run it**

Expected: `1`.

- [ ] **Step 3: Replace the false reason, keeping the conclusion**

Replace:

```
Both are written at gate time, under the last round's heading. The date
each line carries tells a gate episode apart from that round's own
findings, so a gate never mints a heading of its own — the round
heading's grammar is closed, and a gate is not a round.
```

with:

```
Both are written at gate time, under the last round's heading. The `hit`
token tells a gate line apart from that round's own findings; the date
does not, since a gate episode and the round it precedes commonly share
one. A gate still never mints a heading of its own, on the separate
ground that the round heading's grammar is closed and a gate is not a
round.
```

- [ ] **Step 4: Run the check again**

Expected: `0`.

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "fix(working-process): the hit token discriminates a gate line, not the date"
```

---

### Task 5: The relitigation clause, rekeyed

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the paragraph beginning "A resolved held line is a recorded decision"

**Interfaces:**
- Consumes: `ruling:` and `license:` from Task 2; the historical-forms statement from Task 3.
- Produces: the three-way branch that Task 10's reviewer-scope text refers to.

- [ ] **Step 1: Write the failing check**

```bash
grep -c 'A resolved held line is a recorded decision' plugins/working-process/rules/spec-plan-lifecycle.md
```

- [ ] **Step 2: Run it**

Expected: `1`.

- [ ] **Step 3: Replace the paragraph**

Replace:

```
A resolved held line is a recorded decision. When a later round re-raises
the problem it settled, the new finding is folded and cited against that
line, never asked again — state prevents relitigation, not the
reviewer's memory.
```

with:

```
A line carrying `ruling:` is a recorded developer decision, and what a
later round may do with it depends on what that round brings:

- re-raised without new evidence — folded and cited, never asked again;
  the fold produces `declined <date>` carrying `ruling:` with the prior
  ruling's date and a `folding` citation of the line it folds against,
  so the authorizer is cited rather than manufactured;
- re-raised with new evidence — `held`, its `counter:` citing the prior
  ruling, because a session that folded this alone would arbitrate
  between a reviewer and a recorded developer decision.

Evidence is new relative to what the folded line records — its claim and
the reasoning its clauses carry — not relative to the reviewer's
wording. A session that cannot tell holds rather than folds.

A pre-design settled line carries no authorizer clause and is settled by
its token alone; a fold against one cites the date on that token, which
is when the developer decided.

State prevents relitigation, not the reviewer's memory.
```

- [ ] **Step 4: Run the check again**

Expected: `0`, and `grep -c 'folding' plugins/working-process/rules/spec-plan-lifecycle.md` prints at least `2` (the clause table row from Task 2 and this paragraph).

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): relitigation branches on the authorizer clause"
```

---

### Task 6: The Unfinished-work section's two corrections

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the closing paragraph of `## Unfinished-work list`, and the two sentences at the section's head and tail that read "review-loop ledger entry"

**Interfaces:**
- Consumes: the four tokens from Task 1.
- Produces: nothing new.

- [ ] **Step 1: Write the failing check**

```bash
rg -U -n 'review-loop\s+ledger entry' plugins/working-process/rules/spec-plan-lifecycle.md
grep -c 'becomes `resolved <date>`' plugins/working-process/rules/spec-plan-lifecycle.md
```

- [ ] **Step 2: Run it**

Expected: the first prints three lines covering two occurrences — one whole at line 228, one wrapped across lines 271–272 — and the second prints `1`.

**`rg -U` is not optional here.** The second occurrence breaks across a line ending, so a single-line `grep` finds only the first and reports the work half done. Any check for this phrase in this file is multi-line.

- [ ] **Step 3: Reword both "review-loop ledger entry" occurrences**

Change each to `review-loop entry`. The glossary's **Disposition line** entry bans `ledger entry` as a name for a disposition line, and both sentences mean the Unfinished-work list's own entry — the reword removes the collision without changing the referent.

- [ ] **Step 4: Correct the close description**

Replace:

```
ledger entry anchors a leading disposition token instead, so there the
close is a rewrite — `open` or `held` becomes `resolved <date>`, and the
anchor stops matching.
```

with:

```
review-loop entry anchors a leading disposition token instead, so there
the close is a rewrite — `open` or `held` becomes `fixed <date>` or
`declined <date>`, and the anchor stops matching.
```

- [ ] **Step 5: Run the check again**

Expected: `rg -U -n 'review-loop\s+ledger entry'` prints nothing, and the second command prints `0`.

- [ ] **Step 6: Run the published command against the repo**

```bash
rg -n --no-ignore --crlf '^- (open|held) —' docs/
```

Expected: no output. A hit here means a real unfinished line, not a defect in this task; investigate before continuing.

- [ ] **Step 7: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "fix(working-process): ledger close names the merged tokens"
```

---

### Task 7: The oscillation tripwire and the blocking terminator

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the `### Terminators` list

**Interfaces:**
- Consumes: `license:` from Task 2.
- Produces: nothing new.

- [ ] **Step 1: Write the failing check**

```bash
grep -c 'a finding re-raised against a `fixed` line' plugins/working-process/rules/workflow.md
grep -c 'A blocking' plugins/working-process/rules/workflow.md
```

- [ ] **Step 2: Run it**

Expected: `1` and `1`.

- [ ] **Step 3: Rekey the tripwire**

Replace:

```
- Oscillation tripwire: a finding re-raised against a `fixed` line is
  never re-fixed autonomously. Two readings of one license are a
  contested reading, so it escalates as held, the flip named.
```

with:

```
- Oscillation tripwire: a finding re-raised against a line carrying
  `license:` is never re-fixed autonomously. Two readings of one license
  are a contested reading, so it escalates as held, the flip named. A
  re-raise against a line carrying `ruling:` is the relitigation case
  instead, and the spec-plan-lifecycle rule owns it.
```

- [ ] **Step 4: Delete the self-fix prohibition**

Replace:

```
- `blocking` suspends autonomy entirely: relay, stamp, stop. A blocking
  round licenses no self-fixes, because reshaping a design the reviewer
  judged broken as a whole is design work and re-enters through the
  design conversation. `concerns` is the autonomy zone.
```

with:

```
- `blocking` suspends autonomy entirely: relay, stamp, stop — no further
  round without the developer. It licenses no separate fix prohibition,
  because triage already holds what the prohibition was reaching for: a
  design reshape has no citable license by construction, so it is held
  whatever the verdict's grade.
```

- [ ] **Step 5: Run the check again**

Expected: first command prints `0`.

- [ ] **Step 6: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): tripwire keys on license, blocking drops its fix ban"
```

---

### Task 8: The cap's contact definition

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the `Round cap` bullet in `### Terminators`

**Interfaces:**
- Consumes: nothing.
- Produces: nothing new.

- [ ] **Step 1: Write the failing check**

```bash
grep -c 'any developer contact resets the count' plugins/working-process/rules/workflow.md
grep -c 'a message from the developer' plugins/working-process/rules/workflow.md
```

- [ ] **Step 2: Run it**

Expected: `1` and `0`.

- [ ] **Step 3: Replace the bullet**

Replace:

```
- Round cap: three autonomous rounds per document per field without
  developer contact. Hitting the cap escalates in one batch — what was
  fixed, what remains, why — rather than halting silently, and any
  developer contact resets the count.
```

with:

```
- Round cap: three autonomous rounds per document per field without
  developer contact, counting only rounds that returned a verdict.
  Hitting the cap escalates in one batch — what was fixed, what remains,
  why — rather than halting silently. Developer contact is a message
  from the developer: not a relay they read, not an escalation the
  session sent, not an unanswered batch. The count is derived from the
  round headings and the reset event is recorded nowhere, so the cap is
  best-effort by construction; a session that cannot count its own
  rounds escalates rather than assuming, since resetting to zero would
  let a long session grant itself three fresh rounds after every
  compaction.
```

- [ ] **Step 4: Run the check again**

Expected: second command prints `1`.

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): define developer contact, state the cap is best-effort"
```

---

### Task 9: What a diff-scoped round may read

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — `### Re-dispatch briefs`, after the ledger-supplies-what-changed paragraph

**Interfaces:**
- Consumes: `license:` and `ruling:` from Task 2; the relitigation branch from Task 5.
- Produces: nothing new.

- [ ] **Step 1: Write the failing check**

```bash
grep -c 'always in scope for a diff-scoped round' plugins/working-process/rules/workflow.md
```

- [ ] **Step 2: Run it**

Expected: `0`.

- [ ] **Step 3: Add the paragraph**

```
Diff-scoping forbids re-reviewing the document beyond the diff, and the
ledger is part of the document — so without a clause the reviewer is cut
off from the one section recording what the developer already decided.
The ledger is therefore always in scope for a diff-scoped round as
context, never as a review target, and what that protects is narrow:

- lines carrying `ruling:` may be re-raised only with new evidence,
  which routes to `held` rather than to a fold;
- `held` lines carry questions already put, so a round does not
  duplicate one;
- `fixed` lines carrying `license:` get no protection at all — the
  previous round's are the diff and are named as the first thing to
  attack, and older ones are simply unprotected, since a reviewer told
  not to re-raise a fix would lose the property diff-scoping was
  adopted for.

The reviewer learns what it may not reopen, never what it may not find.
Naming the section rather than copying its lines keeps the brief from
growing with the round count.
```

- [ ] **Step 4: Run the check again**

Expected: `1`.

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): the ledger is standing context for a diff-scoped round"
```

---

### Task 10: Normalize wave one's bare gate line

**Files:**
- Modify: `docs/specs/2026-08-31-review-loop-errata-wave-one.md:157` and its `## Review rounds` section

**Interfaces:**
- Consumes: the `hit dismissed` shape, which wave one itself shipped.
- Produces: nothing.

- [ ] **Step 1: Write the failing check**

```bash
rg -n --no-ignore --crlf '^- dismissed ' docs/
```

- [ ] **Step 2: Run it**

Expected: one hit, `docs/specs/2026-08-31-review-loop-errata-wave-one.md:157`.

- [ ] **Step 3: Add the `hit` token**

Change `- dismissed 2026-08-31 — eight sites in the shipped spec…` to `- hit dismissed 2026-08-31 — eight sites in the shipped spec…`, leaving the rest of the line untouched.

- [ ] **Step 4: Record the edit in wave one's own ledger**

Under wave one's last round heading, add:

```
- hit fixed <today's ISO date> — this document's own bare `- dismissed 2026-08-31` line predated the `hit dismissed` shape its wave went on to define; the token is added, and nothing else on the line changes
```

Wave one carries an adjudicated verdict, and editing a stamped document's body without a trace there is the thing wave one itself refused to do.

- [ ] **Step 5: Run the check again**

Expected: no output.

- [ ] **Step 6: Commit**

```bash
git add docs/specs/2026-08-31-review-loop-errata-wave-one.md
git commit -m "docs: normalize wave one's bare gate line to the shape it defined"
```

---

### Task 11: Whole-payload verification

**Files:**
- Modify: none unless a check fails

**Interfaces:**
- Consumes: every earlier task.

- [ ] **Step 1: Run every published Unfinished-work command**

```bash
rg -l --no-ignore --crlf '^\s*grilled: grilling' docs/
rg -l --no-ignore --crlf '^\s*(architect|adversary): (blocking|concerns)$' docs/
rg -n --no-ignore --crlf '^- (open|held) —' docs/
rg -l --no-ignore --crlf '^\s*(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/
rg -l --no-ignore --crlf '^\s+(grilled|architect|adversary|architect-fallback|adversary-fallback|integrity):' docs/
```

Expected: the first returns `docs/plans/2026-07-13-rules-distribution.md`, which is a body quotation of the convention and not a frontmatter hit — confirm with `grep -n 'grilled: grilling'` on that file and check the line sits below the closing `---`. The other four return nothing.

- [ ] **Step 2: Confirm no banned term returned**

```bash
grep -rn --include='*.md' 'ledger entry' plugins/ docs/domain/
```

Expected: no output.

- [ ] **Step 3: Confirm the old grammar is gone from the rules**

```bash
grep -n 'resolved <date> — \[' plugins/working-process/rules/spec-plan-lifecycle.md
```

Expected: no output outside the historical-forms paragraph from Task 3. If the paragraph quotes the shape, that single hit is correct.

- [ ] **Step 4: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 5: Dispatch the propagation gate**

Run the `propagation-auditor` agent on the cheapest available family over the whole change set, with a positive scope: report only internal contradictions, consumers left behind, and recomputed counters that are wrong. Fix or dismiss each hit with a written derivation, recording dismissals as gate lines in this plan's ledger.

- [ ] **Step 6: Commit any fixes**

```bash
git add -A plugins/ docs/
git commit -m "fix(working-process): close the propagation gate on the ledger rewrite"
```

---

## Self-review

**Spec coverage.** Every section of the spec maps to a task: the states and severity omission and write-ahead to Task 1; the clauses and the authorizer rule to Task 2; historical shapes and lawful prose to Task 3; the gate discriminator to Task 4; the fold and the relitigation branch to Task 5; the Unfinished-work corrections to Task 6; the tripwire and blocking terminator to Task 7; the cap to Task 8; the diff-scoped reading scope to Task 9; wave one's line to Task 10. The glossary needs no task — the grilling already changed it. The four refusals need no task: they are decisions not to build, and Task 1's severity paragraph carries the only one with prose consequences.

**Placeholders.** None. Every step carries the literal text to write or the literal command to run.

**Name consistency.** `license:`, `ruling:`, `question:`, `options:`, `counter:`, `deviation:`, `folding`, `fixed <date>`, `declined <date>`, `open`, `held`, `hit fixed`, `hit dismissed` are spelled identically in Tasks 1, 2, 5, 6, 7, 9 and 10.

**One defect the self-review caught.** Task 6's check first asserted two
single-line matches for `review-loop ledger entry`. Only one occurrence
sits on a single line; the other wraps across a line ending, so `grep`
finds one, and an executor would have read that as the work half done.
The check is now `rg -U`, with the reason stated on the step. Every
other phrase check in this plan was re-run against the working tree
before the plan was saved: the five-shape block, the close description,
the tripwire wording, the bare `dismissed` line, and the command counts
all match what their steps expect.

**Known seam.** Task 2's Step 5 verifies the "four of the five" anchor claim by counting published commands. That count includes the `revises:` lookup, which is not an Unfinished-work entry — the step says so, but a future command added to either group will make the assertion wrong before the prose is. It is a check with a short shelf life, deliberately kept because the alternative is trusting the claim.
