---
ticket: none
date: 2026-09-02
status: draft
adversary: blocking
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
- **A check that searches for prose uses `rg -U` and puts `\s+` between *every* pair of words in the pattern; a check that searches for an anchored structural pattern uses `grep`.** These files wrap prose at about 72 characters, so a searched phrase may straddle a line ending and a single-line `grep` then returns 0 where the phrase is plainly present. Four checks in this plan's earlier drafts had exactly that fault, found across three sweeps that each declared the class closed — which is why the constraint is now unconditional rather than applied where a wrap looks likely. Where the wrap falls is not something a reader reliably predicts, and a pattern that is uniformly `\s+` is correct whether or not it wraps, so no judgement is exercised and no instance can be missed. An anchored pattern like `^    - fixed <date>` or `^| \`ruling:` cannot straddle by construction, so single-line matching is correct there and multi-line matching would be misleading.
- **`rg -c` prints nothing and exits 1 when its pattern does not match** — it never prints `0`. A step asserting absence with `rg` therefore expects *no output*; only `grep -c`, which does print `0`, is given a numeric zero expectation.
- **An anchored check on an indented block publishes *both* anchors — exact and tolerant — and asserts their equality.** Never one alone, and never a per-site decision about which. The exact anchor (`^    ` for a grammar block, `^| ` for a table row) proves the prescribed text is well-formed at the indent the step prescribes; the tolerant anchor (`^\s*`) proves no variant survives anywhere else. Each alone has a blind spot that reads as success: the exact one passes while a leftover sits at another indent, the tolerant one passes while the prescribed block is mis-indented. Equality of the two counts is the assertion, and a divergence localizes which half failed.

  An earlier draft of this constraint made tolerance depend on the direction of the assertion — tolerant for "is it gone", exact for "is it present". That reasoning is sound and it is *why* the pair works, but it is a judgement exercised at every site, and the wrapped-phrase constraint above is the standing evidence for what that costs. Applying it, this plan got Task 11's Step 3 wrong: that step asserts both directions at once and the rule had no answer for it. Publishing both anchors always is mechanical, subsumes both directions, and cannot be misapplied. The lifecycle rule's own asymmetry — tolerant Unfinished-work anchors so a relocated field is still found, an exact `^\s+` on Misplaced stamp because there the indentation *is* the defect — is the reasoning this pair captures without asking any later reader to re-derive it.

  One case is copied rather than reasoned about: a check mirroring a command the rules publish reproduces it verbatim, the ledger anchor `^- ` included, which is strict by design so indented payload cannot match it.
- **Every check must return a different value before and after its step, and both values are stated.** A check whose before-value equals its after-value verifies nothing, however correct both numbers look — and it survives review precisely because nothing about it appears wrong. Task 11's Step 3 was exactly this: it counted a shape one task deletes and a later one restores, scoring `2` both before and after the entire plan. Where a count cannot distinguish the two states, assert something that can — a line ordering against text that does not exist until the work is done.

---

### Task 1: The four states, their shapes, and the write-ahead discipline

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the shapes block and bullets under `## The disposition ledger`

**Interfaces:**
- Produces: the four leading tokens `open`, `held`, `fixed <date>`, `declined <date>`, and the rule that a severity bracket is omitted when both legs hold. Tasks 2, 3, 5 and 7 all name these tokens.

- [ ] **Step 1: Write the failing check**

```bash
# The old five-shape block must still be present, and the new tokens absent.
f=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '^    - resolved <date> — \[<severity>\]' "$f"   # old shape, exact indent
grep -c '^\s*- resolved <date> — \[<severity>\]' "$f"    # old shape, any indent
grep -c '^    - declined <date>' "$f"                    # new shape, exact indent
grep -c '^\s*- declined <date>' "$f"                     # new shape, any indent
```

Each shape is counted twice, exact and tolerant, per the paired-anchor constraint above. The two counts for a shape must always match: a divergence means a line sits at an indent the grammar block does not use, which the single-anchor form of this check could not see in either direction.

- [ ] **Step 2: Run it to confirm the starting state**

Expected: `1`, `1`, `0`, `0` — the old shape present at the block's indent and nowhere else, the new shape absent everywhere.

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

Expected: `0`, `0`, `1`, `1` — the old shape gone at every indent, the new shape present at the block's indent and nowhere else. Each pair must match.

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
f=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '^| `ruling: <date>` |' "$f"     # exact: a table row starts at column 0
grep -c '^\s*| `ruling: <date>` |' "$f"  # any indent
```

- [ ] **Step 2: Run it**

Expected: `0` and `0`.

The pair matters here for a reason particular to Markdown: a table row indented by four spaces stops being a table and renders as a code block, silently, with no parse error. The exact anchor alone would report the row missing without saying why; the tolerant one alone would report it present while the table was broken. A divergence between the two is the diagnosis.

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

Expected: `1` and `1`, matching.

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
- Produces: the two historical shape lines, quoted verbatim, and the statement that they remain parseable. Task 5's fold and Task 11's Step 3 both rely on them being present in the file.

**This task reinstates shape lines Task 1 deleted.** Task 1 removes all five old shapes from the live block; this task writes two of them back, in a block explicitly labelled historical. Task 1's own post-edit check is therefore true only at Task 1's completion, and Task 11 accounts for the reinstated pair rather than expecting the file to be free of them.

- [ ] **Step 1: Write the failing check**

```bash
rg -U -c 'described\s+historical\s+forms' plugins/working-process/rules/spec-plan-lifecycle.md
```

- [ ] **Step 2: Run it**

Expected: no output.

- [ ] **Step 3: Add the paragraph**

```
Ledger lines written before this merge stay as written, as the `scope`
token's introduction already established. The shapes they use are kept
here as described historical forms rather than deleted:

    - resolved <date> — [<severity>] <claim>; landed in <section>
    - resolved <date> (declined) — [<severity>] <claim>; <why the document stands>

A reader must still parse pre-merge documents, and a fold against a
pre-design settled line cites a date off a token the live grammar no
longer produces. These two shapes are described, never minted: no
session writes a new line in either form.

Narrative prose between the lines of a `## Review rounds` section is
lawful and expected. This grammar governs headings, lines, and their
indented payload; a paragraph explaining why a wave went the way it did
belongs there too. A lint over the section reads the anchored lines and
ignores the prose.
```

- [ ] **Step 4: Run the check again**

Expected: `1`. Also confirm the reinstated shapes are present, which Task 11's Step 3 will re-assert:

```bash
f=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '^    - resolved <date> ' "$f"    # exact indent
grep -c '^\s*- resolved <date> ' "$f"     # any indent
```

Expected: `2` and `2`, matching. Task 1 left this at `0` and `0`, so the pair also proves this task ran rather than merely that the shapes exist somewhere.

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
rg -U -c 'The\s+date\s+each\s+line\s+carries\s+tells\s+a\s+gate\s+episode\s+apart' plugins/working-process/rules/spec-plan-lifecycle.md
```

- [ ] **Step 2: Run it**

Expected: `1`. The phrase wraps after "The date", so `grep` returns 0 here and `rg -U` is required.

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

Expected: no output.

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
rg -U -c 'A\s+resolved\s+held\s+line\s+is\s+a\s+recorded\s+decision' plugins/working-process/rules/spec-plan-lifecycle.md
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

Expected: no output, and `grep -c 'folding' plugins/working-process/rules/spec-plan-lifecycle.md` prints at least `2` (the clause table row from Task 2 and this paragraph).

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
rg -U -n 'review-loop\s+ledger\s+entry' plugins/working-process/rules/spec-plan-lifecycle.md
rg -U -c 'becomes\s+`resolved\s+<date>`' plugins/working-process/rules/spec-plan-lifecycle.md
```

- [ ] **Step 2: Run it**

Expected: the first reports two occurrences of `review-loop ledger entry` — one falling on a single line, in the paragraph about a re-scoped match scope, and one wrapping across a line ending, in the closing paragraph about the anchors. The second prints `1`.

Line numbers are deliberately not stated: Tasks 1–5 insert text above both occurrences, so any number quoted here would be wrong by the time this task runs. Match on the surrounding sentence instead.

**`rg -U` is not optional here.** The second occurrence breaks across a line ending, so a single-line `grep` finds only the first and reports the work half done. Any check for this phrase in this file is multi-line.

- [ ] **Step 3: Reword the first occurrence**

In the paragraph about the re-scoped match scope, change `the review-loop ledger entry below is the one that does` to `the review-loop entry below is the one that does`.

The glossary's **Disposition line** entry bans `ledger entry` as a name for a disposition line, and the sentence means the Unfinished-work list's own entry — the reword removes the collision without changing the referent.

**The second occurrence is not touched here.** It sits inside the block Step 4 replaces wholesale, and Step 4's replacement text already carries the reword. Rewording it now would leave Step 4 quoting text that no longer exists.

- [ ] **Step 4: Correct the close description, rewording the second occurrence as part of it**

Replace:

```
ledger entry anchors a leading disposition token instead, so there the
close is a rewrite — `open` or `held` becomes `resolved <date>`, and the
anchor stops matching.
```

with:

```
entry anchors a leading disposition token instead, so there the
close is a rewrite — `open` or `held` becomes `fixed <date>` or
`declined <date>`, and the anchor stops matching.
```

The word `review-loop` sits on the preceding line and is not part of either block, so dropping `ledger` from the start of the replacement is what completes the reword — the sentence then reads "the review-loop entry anchors a leading disposition token instead". Re-wrap the paragraph to the file's ~72-character habit after the edit.

- [ ] **Step 5: Run the check again**

Expected: both commands print nothing.

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

### Task 7: `workflow.md`'s three consumers of the retired token

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the triage paragraph under `### The review loop`, and the `### Terminators` list

**Interfaces:**
- Consumes: `license:` and `ruling:` from Task 2; the merge from Task 1.
- Produces: nothing new.

The merge in Task 1 retires `resolved` as a disposition token, and `workflow.md` reads it in three places: the triage paragraph's list of license sources, the oscillation tripwire, and the blocking terminator. All three are fixed here, in one file, so no consumer of the retired token is left behind.

- [ ] **Step 1: Write the failing check**

```bash
rg -U -c 'a\s+previously\s+resolved\s+`held`\s+line' plugins/working-process/rules/workflow.md
rg -U -c 'a\s+finding\s+re-raised\s+against\s+a\s+`fixed`\s+line' plugins/working-process/rules/workflow.md
rg -U -c 'licenses\s+no\s+self-fixes' plugins/working-process/rules/workflow.md
```

- [ ] **Step 2: Run it**

Expected: `1`, `1` and `1`. Each pattern names text this task removes, so each fails if its step is skipped; a looser pattern such as `A blocking` would pass either way and verifies nothing.

- [ ] **Step 3: Rekey the triage paragraph's license sources**

The triage paragraph lists what a session may cite to license a self-fix, and one item names a state the live grammar stops producing. Replace:

```
licenses the fix — a statement in the document itself, a glossary term
or `_Avoid_` ban, a recorded ADR, or a previously resolved `held`
line — and the citation goes on the finding's line in the disposition
```

with:

```
licenses the fix — a statement in the document itself, a glossary term
or `_Avoid_` ban, a recorded ADR, or a line carrying `ruling:` — and
the citation goes on the finding's line in the disposition
```

A held line the developer answered now terminates as `fixed <date>` or `declined <date>` carrying `ruling:`, so the authorizer clause is what identifies a recorded developer decision, whatever token the line ends on. The reword also picks up pre-design settled lines, which the old wording missed.

- [ ] **Step 4: Rekey the tripwire**

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

- [ ] **Step 5: Delete the self-fix prohibition**

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

- [ ] **Step 6: Run the check again**

Expected: all three commands print nothing. Each corresponds to one of Steps 3, 4 and 5, so a skipped step is the one that still prints `1`.

- [ ] **Step 7: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): move workflow.md off the retired resolved token"
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
rg -U -c 'any\s+developer\s+contact\s+resets\s+the\s+count' plugins/working-process/rules/workflow.md
rg -U -c 'a\s+message\s+from\s+the\s+developer' plugins/working-process/rules/workflow.md
```

- [ ] **Step 2: Run it**

Expected: `1`, then no output. The first phrase wraps after "any" and the second wraps after "a message" once written, so both are uniformly `\s+` — the second is the instance that made the constraint unconditional.

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

Expected: the first command prints nothing, the second prints `1`. Both are stated because the replacement deletes the first phrase and introduces the second, so each command changes value and a step that asserted only one would let half the edit pass unverified.

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
rg -U -c 'always\s+in\s+scope\s+for\s+a\s+diff-scoped\s+round' plugins/working-process/rules/workflow.md
```

- [ ] **Step 2: Run it**

Expected: no output.

- [ ] **Step 3: Add the paragraph**

```
Diff-scoping forbids re-reviewing the document beyond the diff, and the
ledger is part of the document — so without a clause the reviewer is cut
off from the one section recording what the developer already decided.
The ledger is therefore always in scope for a diff-scoped round as
context, never as a review target, and what that protects is narrow:

- settled lines may be re-raised only with new evidence, which routes
  to `held` rather than to a fold. A line carrying `ruling:` is settled
  by that clause; a historical line written before this design,
  `resolved <date> (declined)` included, carries no authorizer clause
  and is settled by its token alone. Both are the developer's
  decisions, and both are protected on the same footing;
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

These expectations describe the repo as this plan was written, and the process's own artifacts can falsify them at execution time: a spec grilled or a round stamped between now and then is a real unfinished-work hit, not a defect in this plan. Investigate any extra hit against the document it names before continuing, exactly as Task 6's Step 6 directs — a hit here is a question about that document, never a reason to edit this one.

- [ ] **Step 2: Confirm no banned term returned**

```bash
grep -rn --include='*.md' 'ledger entry' plugins/ docs/domain/ | grep -v '_Avoid_'
```

Expected: no output.

The `grep -v` is not slack. The glossary's **Disposition line** entry defines the ban by writing the banned phrase — `_Avoid_: finding line, ledger entry` — so an unfiltered sweep necessarily hits the one line that must keep saying it, and the check could never pass in the correct end state. Filtering the definition site is what makes the sweep assert what it means: no *use* of the banned term survives.

- [ ] **Step 3: Confirm the live grammar is gone and the historical block remains**

```bash
f=plugins/working-process/rules/spec-plan-lifecycle.md
rg -U -n 'described\s+historical\s+forms' "$f" | cut -d: -f1   # the paragraph Task 3 adds
grep -n '^    - resolved <date> ' "$f"                          # exact: the block, well-formed
grep -c '^\s*- resolved <date> ' "$f"                           # tolerant: nothing else, any indent
```

Expected: the paragraph's line number prints; exactly two `resolved <date>` lines print, **both numbered greater than it**; and the tolerant count is `2`, equal to the number of exact-anchored hits.

**A bare count here would be vacuous, and was.** This step's first draft compared counts alone, and the file scores `2` and `2` *before* any task runs — the two shapes sit in the live block today, and Task 1 deleting them while Task 3 writes them back leaves the total unchanged. A check that passes identically in the starting and finishing states verifies nothing, and it would have gone unnoticed because both numbers are right. The line-ordering comparison is what makes the step discriminate: before implementation the introducing paragraph does not exist, and the shape lines sit above where it will be, so the assertion fails exactly when the work has not happened.

The two anchors then split the remaining work in opposite directions. The exact one says Task 3's block is well-formed at the grammar block's own indent — fewer than two hits means missing or mis-indented. The tolerant one says nothing matching the retired shape survives anywhere else at any indent — a count above the number of exact hits means a leftover the exact anchor cannot see, which is the live-block line Task 1 was supposed to delete. Neither anchor alone carries both claims.

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

**Spec coverage.** Every section of the spec maps to a task: the states and severity omission and write-ahead to Task 1; the clauses and the authorizer rule to Task 2; historical shapes and lawful prose to Task 3; the gate discriminator to Task 4; the fold and the relitigation branch to Task 5; the Unfinished-work corrections to Task 6; the triage license sources, the tripwire and the blocking terminator — `workflow.md`'s three consumers of the retired token — to Task 7; the cap to Task 8; the diff-scoped reading scope to Task 9; wave one's line to Task 10. The glossary needs no task — the grilling already changed it. The four refusals need no task: they are decisions not to build, and Task 1's severity paragraph carries the only one with prose consequences.

**Placeholders.** None. Every step carries the literal text to write or the literal command to run.

**Name consistency.** `license:`, `ruling:`, `question:`, `options:`, `counter:`, `deviation:`, `folding`, `fixed <date>`, `declined <date>`, `open`, `held`, `hit fixed`, `hit dismissed` are spelled identically in Tasks 1, 2, 5, 6, 7, 9 and 10.

**One defect class, four instances, and the lesson about how to close it.**
Task 6's check first asserted two single-line matches for
`review-loop ledger entry`; only one occurrence sits on a single line,
so `grep` found one and an executor would have read that as the work
half done. The self-review caught that instance **and treated it as
isolated** — which it was not. A propagation gate found two more of
exactly the same shape, in Tasks 4 and 8. A sweep then declared those
three complete, and the plan-adversary found a fourth: Task 8's own
post-edit pattern, written during the repair of the third.

Three sweeps, each declaring the class closed, each wrong. What finally
closed it was not a fourth sweep but a change of method. The constraint
above no longer says "use `rg -U` where a phrase might wrap" — a
judgement, re-exercised per pattern, wrong roughly a third of the time
here. It says every prose pattern is uniformly `\s+` between every pair
of words, which is correct whether or not the phrase wraps and so cannot
be misapplied. The lesson is not "sweep harder": a rule that requires a
prediction at each site will keep producing instances at the rate the
prediction fails, and the repair is to remove the prediction.

The same reasoning produced two further constraints during this wave —
one on `rg -c`'s zero behaviour, one on leading-anchor tolerance, the
latter raised by the developer. Each replaces a per-site judgement with
a mechanical rule.

Every other check was re-run against the working tree: the five-shape
block, the close description, the tripwire wording, the triage
paragraph, the bare `dismissed` line, and the command counts all match
what their steps expect.

**Known seam.** Task 2's Step 5 verifies the "four of the five" anchor claim by counting published commands. That count includes the `revises:` lookup, which is not an Unfinished-work entry — the step says so, but a future command added to either group will make the assertion wrong before the prose is. It is a check with a short shelf life, deliberately kept because the alternative is trusting the claim.

## Review rounds

### 2026-09-02 — plan-adversary, fable 5, blocking (round 1, full-document)

- fixed — [Important] Task 8's post-edit pattern uses literal spaces while the replacement it verifies wraps as "a message / from the developer", so the check false-fails against a correct edit — a fourth instance of the wrapped-phrase class, in the plan whose self-review had just declared that class swept; license: this plan's own Global Constraint on prose checks; the pattern is now uniformly `\s+`, and the constraint itself was rewritten from a per-site judgement into an unconditional rule so the class cannot recur
- fixed — [Important] Task 11's banned-term sweep expects no output from a command that necessarily hits the glossary's own `_Avoid_` line, so the check cannot pass in the correct end state; license: the glossary's **Disposition line** entry, whose ban is stated by writing the banned phrase; the sweep now filters the definition site with `grep -v '_Avoid_'` and the step says why that is not slack
- fixed — [Important] Task 6's Steps 3 and 4 prescribe overlapping edits: Step 3 rewords both occurrences, and the second opens Step 4's replace-this block, so Step 4 then targets text that no longer exists; license: Step 4's own replacement text, which already carried the reword; Step 3 is narrowed to the first occurrence and Step 4 completes the second as part of its block, each step saying so
- fixed — [Important] a consumer of the retired token is left behind — `workflow.md` licenses a self-fix off "a previously resolved `held` line", a state the live grammar stops producing, and no task touches it; license: the spec's merge of `fixed` and `resolved` plus its authorizer rule; Task 7 is rescoped from two consumers to all three in that file, retitled accordingly, and the triage paragraph now cites "a line carrying `ruling:`", which also picks up pre-design settled lines the old wording missed
- fixed — [Important] Task 3 claims the historical `resolved` shapes are "kept" while Task 1 deletes the shape lines and only the token names survive; Task 11's conditional expectation shows the plan has not decided its own end state; license: the spec's statement that the shapes are kept as described historical forms; Task 3 now writes both shape lines verbatim into its block, states that they are described and never minted, and warns that it reinstates lines Task 1 deleted; Task 11's expectation is now unconditional
- fixed — [Important] Task 6's Step 2 states absolute line numbers that Tasks 1–5 invalidate by inserting above them, so a literal executor reads a correct state as a failed check; license: this plan's own task ordering; the numbers are gone, replaced by the surrounding sentence as the locator, with a note saying why no number is quoted
- fixed — [Important] Task 7's Step 5 states only one of its two post-edit expectations, so the deletion the second pattern exists to verify passes unchecked if skipped; license: that step's own stated rationale that each pattern must fail if its step is skipped; the task now carries three checks for three steps and asserts all three
- fixed — [Minor] five "Expected: 0" lines sit on `rg -c` commands, which print nothing and exit 1 rather than printing 0; license: the measured behaviour of `rg -c`, verified in-session; a Global Constraint states it once and six steps — one more than the round found — now expect "no output"
- fixed — [Minor] Task 9's workflow text protects only lines carrying `ruling:`, narrower than the spec's Settled-lines tier, which includes historical token-settled lines; license: the spec's **Settled lines** bullet; the rule text now names both, protected on the same footing
- fixed — [Minor] Task 11's Step 1 asserts a repo state the process's own artifacts can falsify at execution time, without the investigate-versus-defect caveat Task 6's Step 6 carries; license: Task 6's Step 6, which carries exactly that caveat; the step now says an extra hit is a question about the document it names, never a reason to edit this plan

The developer authorized this fix wave despite the `blocking` verdict, which otherwise suspends autonomy. Every finding above carried a citable written license, and none was a design decision — the verdict's grade and the findings' licenses pointed in different directions, which is the case the loop's triage rule was written for.

Four further defects were raised by the developer during the wave,
outside the round. All four came from one observation — that the
anchored `grep` checks had no whitespace treatment — pursued
mechanically rather than site by site, the developer returning three
times because each answer still left a judgement in place:

- fixed — [Important] the anchored `grep` checks used an exact four-space leading anchor where the Unfinished-work list's own commands are deliberately tolerant, so a leftover line at a different indent would read as absent — the same false-clean failure as the wrapped-phrase class; license: the lifecycle rule's stated reasoning that leading anchors are tolerant on purpose and its Misplaced-stamp anchor exact because there the indentation is the defect; a third Global Constraint now ties anchor tolerance to the direction of the assertion, and Task 1's two anchors differ accordingly with the step saying why
- fixed — [Critical] Task 11's Step 3 was vacuous: it compared counts of the retired shape, and the file scores `2` and `2` *before* any task runs, since Task 1 deleting the two shapes while Task 3 writes them back leaves the total unchanged — the step passed identically in the starting and finishing states, and both numbers being right is why nobody noticed; license: the plan's own requirement that a check be capable of failing if its step were skipped; the step now compares the shape lines' line numbers against the introducing paragraph's, which does not exist before implementation, and the step records the vacuity so the next reader sees why the ordering comparison is there
- fixed — [Important] Task 8's Step 4 stated only one of its two post-edit expectations, leaving the deletion half of the edit unverified — the same defect the round found in Task 7, in the task next to it, and missed there; license: that round's finding on Task 7, which is a written decision about this exact shape; both expectations are now stated

- fixed — [Important] the repair above still made anchor tolerance depend on a per-site judgement — tolerant for "is it gone", exact for "is it present" — which is the same shape as the wrapped-phrase rule that produced four instances, and the developer said so after Tasks 1 and 3 kept their single exact anchors; license: this plan's own wrapped-phrase constraint, whose stated reason for going unconditional is that a rule requiring a prediction at each site keeps failing at the rate the prediction does; the constraint now requires *both* anchors on every anchored check with their equality as the assertion, and all five checks are paired

The vacuity above is the wave's most serious finding and none of the
three reviews caught it — not the self-review, not the propagation gate,
not the `blocking` round. It surfaced because the developer's anchor
question forced a mechanical audit of every anchored pattern, and the
audit asked a question reading never asks: does this check return a
different value before and after its task? That question is now worth
asking of every check in every plan, and Task 8's defect fell out of the
same sweep moments later.

The sequence is the lesson, more than any of the four repairs. The first
answer fixed the sites the developer pointed at. The second generalized
to a rule — but a rule with a judgement in it, and the judgement was
promptly got wrong on the one step that asserts both directions at once.
The third removed the judgement. Twice in one plan the same correction
was needed on the same class, and both times the intermediate stop
looked like a principled rule rather than an unfinished one. A
constraint that still asks the reader to classify the site is not
finished; the test is whether it can be applied without deciding
anything.

Answering the round's focusing question — what is still broken if every
stated check passes — the reviewer named three: the retired token still
licenses a self-fix in `workflow.md`, the rule claims to keep shapes it
deleted, and Task 7's deletion may silently not have happened. Two
checks fail against the *correct* state, which it called the more
dangerous direction, since an executor may "fix" the document to satisfy
a broken check.

Its stop signal: a re-round after the fix wave earns its cost, but
diff-scoped — the findings sit in check mechanics and two scope gaps,
not in the prescribed rule prose, which matched the spec everywhere it
was diffed. And a standing instruction for that round: **the
wrapped-phrase class has now produced four instances across two sweeps
that each declared completeness, so it is re-verified mechanically
rather than by reading.**
