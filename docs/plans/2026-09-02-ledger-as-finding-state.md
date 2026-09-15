---
ticket: none
date: 2026-09-02
status: implemented
adversary: concerns (resolved 2026-09-02)
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
- **Every check that verifies an edit must return a different value before and after its step, and both values are stated.** A check whose before-value equals its after-value verifies nothing, however correct both numbers look — and it survives review precisely because nothing about it appears wrong. Task 11's Step 3 was exactly this: it counted a shape one task deletes and a later one restores, scoring `2` both before and after the entire plan. Where a count cannot distinguish the two states, assert something that can — a line ordering against text that does not exist until the work is done.

  Two kinds of check verify no edit and are therefore outside this rule: a **claim-verification** check, which tests a standing assertion in the prose rather than a change (Task 2's Step 5, which counts published commands to confirm a "four of the five" claim), and an **end-state assertion** in a task that modifies nothing (all of Task 11, whose `Files:` line reads "none unless a check fails"). To keep the exemption from becoming the per-site judgement this plan spent three passes removing elsewhere, it is claimed rather than inferred: a check is exempt only where its own step says in words that it verifies no edit, and both exempt sites do.

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
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — after the paragraph beginning "One annotation extends those shapes", immediately before the `### Gate lines` heading

**The insertion point is chosen, not incidental.** The obvious place is straight after Task 2's clause table, and that is wrong: the shipped sentence "One annotation extends those shapes, and nothing else does" refers to the live shapes block, and Tasks 1–3 push roughly a hundred lines between the two. Inserting this task's historical block just above that sentence hands it a nearer and false antecedent — a reader would bind "those shapes" to the two forms this very task declares nobody may mint. Placing the block *after* that paragraph leaves the live shapes as the sentence's nearest shapes block, which is what it means, and costs no new prose in a rule the spec did not ask to reword.

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

Insert immediately after the paragraph ending "defeats the re-review offer" and immediately before the `### Gate lines` heading:

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
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the paragraph under `### Gate lines` beginning "Both are written at gate time"

No line number is given, and none should be: Tasks 1–3 insert well over fifty lines above this paragraph, so any number written here is wrong by the time the task runs. The prose locator is exact on its own. This is the class round 1 reported against Task 6, applied to the one other place that carried a stale number.

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

Expected: no output, and `grep -c 'folding' plugins/working-process/rules/spec-plan-lifecycle.md` prints at least `2` (the clause table row from Task 2 and this paragraph). Its before-value **at this task's own sequence point is `1`**, not `0`: the word is absent from the pristine file, but Task 2 has already written the clause-table row by the time Task 5 runs. The pair still discriminates, `1` to `2`. Measured during implementation, where a stated `0` was the first thing this step got wrong.

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
  whatever the verdict's grade. `concerns` is the autonomy zone.
```

The closing sentence is retained deliberately. The spec directs only the self-fix clause removed, and the sentence stays true under the new design: `blocking` still suspends rounds, `LGTM` still ends the loop, and `concerns` remains the one verdict the loop continues under autonomously. Deleting it would be an un-specced change riding along with a specced one.

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
w=plugins/working-process/rules/workflow.md
rg -U -c 'counting\s+only\s+rounds\s+that\s+returned\s+a\s+verdict' "$w"
rg -U -c 'a\s+message\s+from\s+the\s+developer' "$w"
rg -U -c 'refusal\s+mid-loop\s+is\s+already\s+developer\s+contact' "$w"
```

- [ ] **Step 2: Run it**

Expected: no output, no output, `1`.

**The first pattern is not the obvious one, deliberately.** An earlier draft checked `any developer contact resets the count`, which reads like the natural anchor for this bullet — but the replacement *retains* that sentence, so the pattern scores `1` on both sides and verifies nothing. The qualifier `counting only rounds that returned a verdict` is text the replacement introduces and the original lacks, so it discriminates. This is the plan's own before/after constraint catching a check that a repair to a different finding had just made vacuous.

The second phrase wraps after "a message" once written, so it is uniformly `\s+` like every prose pattern here. The third finds the consumer Step 4 reconciles.

**Enumerate the consumers of the term, not just the bullet.** This task redefines "developer contact" and the term is used elsewhere in the same file. Task 7 enumerates consumers of a retired *token*; this step does the same for a redefined *term*, which is the class round 2 found missing here.

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
  why — rather than halting silently, and any developer contact resets
  the count. Developer contact is a message from the developer: not a
  relay they read, not an escalation the session sent, not an unanswered
  batch. The count is derived from the round headings and the reset
  event is recorded nowhere, so the cap is best-effort by construction;
  a session that cannot count its own rounds escalates rather than
  assuming, since resetting to zero would let a long session grant
  itself three fresh rounds after every compaction.
```

Two details of this replacement are not in the spec, and both are recorded here rather than left to be re-derived:

- **The reset sentence is retained**, not dropped. An earlier draft let "without developer contact" imply the reset. The spec directs no deletion, and the definition this bullet adds makes the reset *more* worth stating explicitly, not less — the sentence now says precisely what event resets the count.
- **"counting only rounds that returned a verdict" is added**, and it is derivable rather than invented: the bullet's own next sentence says the count comes from the round headings, and a round that died without a verdict mints no heading. Stating it prevents a session from counting a crashed dispatch against its own budget.

- [ ] **Step 4: Reconcile the cap-refusal sentence with the new definition**

The file's closing paragraph says a model-cap refusal *is* developer contact. Step 3's definition says developer contact is a message from the developer, and a platform refusal is not one — so the two would ship contradicting each other. Replace:

```
refusal mid-loop is already developer contact: the drop-or-wait
question above is never answered autonomously.
```

with:

```
refusal mid-loop forces developer contact: the drop-or-wait
question above is never answered autonomously.
```

The behaviour is unchanged and was never in doubt — the loop cannot proceed until the developer answers the drop-or-wait question, which is a message. Only the claim changes, from the refusal *being* contact to *forcing* it, which is what the sentence always meant and what the new definition now requires it to say.

- [ ] **Step 5: Run the check again**

Expected: `1`, `1`, then nothing. All three are stated because each corresponds to one edit — Step 3 introduces the first two phrases, Step 4 removes the third — and a step asserting fewer would let an edit pass unverified.

- [ ] **Step 6: Validate and commit**

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
- Consumes: `license:` and `ruling:` from Task 2; the relitigation branch and the evidence-newness base from Task 5.
- Produces: nothing new.

**The evidence-newness base is carried as a pointer, not a copy.** The spec's Changes-by-file assigns `workflow.md` "the base against which evidence counts as new", and this task delivers it by naming where the definition lives rather than restating it — Task 5 writes the full definition into `spec-plan-lifecycle.md`, which is where the spec puts the record's grammar. A duplicated definition in two rule files is the drift the spec's own file split exists to prevent, and both files already cross-reference each other this way rather than restating. A reviewer who thinks the pointer is too thin should say so: the deviation from the reviewer's suggested full sentence is recorded here deliberately, and the rationale is the thing to attack.

- [ ] **Step 1: Write the failing check**

```bash
w=plugins/working-process/rules/workflow.md
rg -U -c 'always\s+in\s+scope\s+for\s+a\s+diff-scoped\s+round' "$w"
rg -U -c 'the\s+base\s+the\s+spec-plan-lifecycle\s+rule\s+defines' "$w"
```

- [ ] **Step 2: Run it**

Expected: no output from either. The second is what proves the evidence-newness base reached this file, which is the one thing the spec assigns here that a reader would otherwise look for in the lifecycle rule alone.

- [ ] **Step 3: Add the paragraph**

```
Diff-scoping forbids re-reviewing the document beyond the diff, and the
ledger is part of the document — so without a clause the reviewer is cut
off from the one section recording what the developer already decided.
The ledger is therefore always in scope for a diff-scoped round as
context, never as a review target, and what that protects is narrow:

- settled lines may be re-raised only with new evidence — new against
  what the folded line records, the base the spec-plan-lifecycle rule
  defines — which routes to `held` rather than to a fold. A line
  carrying `ruling:` is settled by that clause; a historical line
  written before this design, `resolved <date> (declined)` included,
  carries no authorizer clause and is settled by its token alone. Both
  are the developer's decisions, and both are protected on the same
  footing;
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

Expected: `1` and `1`. Both are stated because the paragraph delivers two things the spec assigns to this file — the ledger's standing place in a diff-scoped round, and the evidence-newness base — and a step asserting only the first would let the second go missing exactly as it did in this plan's first three drafts.

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

Expected, with two known hits:

- the **first** returns `docs/plans/2026-07-13-rules-distribution.md`, a body quotation of the convention rather than a frontmatter hit — confirm with `grep -n 'grilled: grilling'` on that file and check the line sits below the closing `---`;
- the **second** returned **this plan** throughout the review loop, whose own `adversary:` field carried a live verdict. That was a true unfinished-work hit, not a false positive. It cleared when the loop closed on 2026-09-02 with `adversary: concerns (resolved 2026-09-02)`, the annotation defeating the command's tail anchor exactly as an `LGTM` replacement would have. By the time an executor reaches this step the command returns nothing; if it returns this plan again, a later round reopened the loop and implementation has started early;
- the remaining three return nothing.

An earlier draft of this step claimed all four of the last commands were clean "as this plan was written", which its own frontmatter falsified on the day the step was written — the plan was carrying `adversary: blocking` at the time.

Beyond those, the process's own artifacts can falsify these expectations at execution time: a spec grilled or a round stamped between now and then is a real unfinished-work hit, not a defect in this plan. Investigate any extra hit against the document it names before continuing, exactly as Task 6's Step 6 directs — a hit here is a question about that document, never a reason to edit this one.

- [ ] **Step 2: Confirm no banned term returned**

```bash
rg -U -n 'ledger\s+entry' plugins/ docs/domain/ | grep -v '_Avoid_'
```

Expected: no output.

`ledger entry` is a two-word prose phrase, so this sweep obeys the prose constraint like any other: `rg -U` with `\s+`, never a single-line `grep`. The point is exact: a surviving banned use that happened to wrap as `ledger` / `entry` across a line ending is invisible to a literal-space pattern, and this command's whole job is to prove no use survives. An earlier draft ran `grep -rn 'ledger entry'` here — written, and then *edited*, during the very wave whose new constraint forbids it.

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

**Spec coverage.** Every section of the spec maps to a task: the states and severity omission and write-ahead to Task 1; the clauses and the authorizer rule to Task 2; historical shapes and lawful prose to Task 3; the gate discriminator to Task 4; the fold and the relitigation branch to Task 5; the Unfinished-work corrections to Task 6; the triage license sources, the tripwire and the blocking terminator — `workflow.md`'s three consumers of the retired token — to Task 7; the cap to Task 8; the diff-scoped reading scope to Task 9; wave one's line to Task 10. The glossary needs no task — the grilling already changed it.

**The refusals**, which the spec's Changes-by-file lists among the `spec-plan-lifecycle.md` changes, are mapped rather than waived. Three are decisions not to build and leave no prose behind. The two with a rule-side trace are already accounted for: the no-fourth-severity refusal rides Task 1, whose severity paragraph ends "This adds no fourth severity value; the glossary's three stand"; and the hit-outstanding refusal is already shipped prose, the stated-gap paragraph under `### Gate lines` beginning "Neither shape covers a hit left outstanding", which this wave leaves untouched because wave one wrote it and nothing in this design changes it. No task is therefore missing — but the mapping is stated here rather than assumed, since "needs no task" and "is already in the file" are different claims and only the second is true of these two.

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

### 2026-09-02 — implementation

All eleven tasks executed on `feature/audit-errata`, one commit each,
every check run and every stated value reproduced except one:

- fixed 2026-09-02 — [Minor] Task 5's Step 4 stated a before-value of `0` for its `folding` count, true of the pristine file but not of the file Task 5 actually meets — Task 2 writes the clause-table row first, so the real before-value at that sequence point is `1`; license: the measurement, taken during implementation; the step now states `1` and names the sequence point, and the check discriminates either way

The defect is the before/after constraint's own blind spot, and worth
naming: the constraint asks for a value *before the step*, and a plan
author naturally computes it against the document as it stands rather
than as the task will find it. Four rounds of review, two full
simulations and four propagation gates all reproduced the `0` without
challenging it, because every one of them measured the same thing the
author did. Only running the tasks in order exposed it. A stated
before-value in a multi-task plan is a claim about a *simulated
intermediate state*, and nothing but execution or an explicitly
sequenced simulation can check it.

Task 11's Step 5 propagation gate ran over the whole implemented change
set and returned CLEAN — no internal contradiction, no consumer left
behind, no counter wrong. It produced no hits, so it writes no gate
lines. Like the four before it, it omitted the model self-report the
workflow rule requires; five dispatches, five omissions, and the
reliance derivation is the one recorded under round 1's heading.

Everything else landed clean: Task 1 `0,0,1,1`; Task 2's paired table
row and the `6,1` anchor claim; Task 3's block placed after the
chain-accepted paragraph, with round 4's antecedent fix confirmed in the
file (the live shapes at line 132 remain the nearest block above the
"One annotation extends those shapes" sentence at 217, and the
historical block sits below it at 228–229); Tasks 4–9 each returning
exactly their stated after-values, with both sentences round 3 restored
verified present; Task 10's two gate lines; and Task 11's five published
commands returning only the known body-quotation hit.

**Loop closed 2026-09-02 by the developer**, with `adversary: concerns
(resolved 2026-09-02)` rather than a fifth round. What resolved it: round
4's single Minor was fixed in `e91da57`, and round 4 was a full-document
round whose reviewer stated that absent that one seam its verdict would
have been the terminating `LGTM`. The fix was one insertion-point change,
verified directly — the anchor text exists verbatim in the target, no
step still refers to the old location, and no check's value moves,
since Task 3's phrase check and Task 11's ordering assertion are both
position-independent within the section.

The loop ran four rounds and four propagation-gate episodes, every gate
returning CLEAN. Rounds 1 and 2 concentrated on check mechanics, round 3
read the prescribed rule prose against the spec, and round 4 simulated
the whole plan and re-tested every historically recurring class with no
recurrence. The developer was in contact at every round boundary, so the
round cap was never the binding constraint; the closure is a cost
judgment, taken with the reviewer's own stop signal in hand.

The plan is implementation-ready. The next gate is the developer's
`status` flip to `approved`.

### 2026-09-02 — plan-adversary, fable 5, concerns (round 4, full-document)

- fixed — [Minor] Tasks 1–3 insert roughly a hundred lines between the shipped sentence "One annotation extends those shapes, and nothing else does" and the shapes it refers to, and Task 3's block landed directly above that sentence — handing it a nearer and false antecedent, the two historical forms this plan declares nobody may mint; license: the plan's own statement that the historical shapes are described and never minted, which the drifted antecedent contradicts; Task 3's insertion point moves to after the chain-accepted paragraph and immediately before `### Gate lines`, restoring the live shapes block as the sentence's nearest antecedent with no new prose and no reworded rule text, and the task now records that the placement is chosen rather than incidental

This round would otherwise have carried the terminating verdict. The
reviewer said so outright: absent the antecedent seam, its verdict would
have been `LGTM`.

Its verification was the most complete of the four rounds, and it
confirmed both historically recurring classes are extinct rather than
merely quiet. Every stated before-value in the plan was executed against
the tree and reproduced, including the two known Task 11 hits. The whole
plan was applied to scratch copies: sixteen of sixteen Replace blocks
matched verbatim and uniquely, every after-check reproduced its stated
value, and Task 1's Step 6 was additionally checked at its own sequence
point rather than only at the end. Every edit-verifying check was
re-derived for vacuity, including the one this session had just rekeyed,
and no other check was found to have been made vacuous by the round-3
wave. No fifth wrapped-phrase instance exists, and every anchored check
is either paired or a verbatim copy of a published command.

It also cleared the round-3 deviation it was asked to attack rather than
protect: Task 9's pointer carries the base's substance inline — "new
against what the folded line records" — and defers to the lifecycle rule
only for the refinement, so a reader of `workflow.md` alone can apply the
rule. The reviewer declined to re-raise it. Task 8's un-specced qualifier
survived the same treatment: a heading is minted at stamp time and
carries the verdict, so a heading-derived count necessarily counts only
verdict-returning rounds, and the qualifier states a consequence rather
than adding a rule.

The spec mapping was verified in both directions — every Changes-by-file
item lands in a named task, and no task ships prose the spec does not
design or license.

Its stop signal: a fifth round does not earn its cost. The leftover was a
single insertion-point change whose correctness is verifiable by eye, and
the plan has now been fully simulated twice by two separate rounds with
zero recurrence in any historical class. The reviewer's recommendation to
the dispatcher was to apply the one fix, verify the single edit directly,
and treat a further full round as the developer's call rather than a
process necessity.

### 2026-09-02 — plan-adversary, fable 5, concerns (round 3, full-document)

- fixed — [Important] Task 9 omits the base against which evidence counts as new, which the spec's Changes-by-file assigns to `workflow.md`; the plan ships it only into `spec-plan-lifecycle.md` via Task 5, so an executor produces a `workflow.md` whose new-evidence judgment has no stated base in the file governing the round's behaviour; license: the spec, which the plan's own Global Constraint makes the winner on disagreement; the paragraph now carries the base as a pointer to the lifecycle rule's definition, a second check proves it reached the file, and the deviation from the reviewer's suggested full sentence is recorded in the task with its rationale — a duplicated definition across two rule files is the drift the spec's file split exists to prevent
- fixed — [Minor] Task 8's replacement silently dropped the shipped sentence "any developer contact resets the count" and added the un-specced qualifier "counting only rounds that returned a verdict"; license: the spec, which directs no deletion here; the reset sentence is retained — the new definition makes stating the reset event more valuable, not less — and the qualifier is kept with its derivation recorded, since the bullet's own next sentence says the count comes from the round headings and a round that died without a verdict mints none
- fixed — [Minor] Task 7's Step 5 deleted "`concerns` is the autonomy zone", which the spec did not direct removed and which stays true under the new design; license: the spec, which directs only the self-fix clause deleted; the sentence is retained in the replacement text and the task says why an un-specced deletion must not ride along with a specced one
- fixed — [Minor] Task 11's Step 1 claimed four commands return nothing "as this plan was written", which the plan's own `adversary:` frontmatter falsified on the day the step was written; license: the mechanical fact, verified in-session; the step now names this plan as the second known hit, says it is a true unfinished-work hit rather than a false positive, and states when it clears — at the confirming round's LGTM, before implementation
- fixed — [Minor] the self-review waived "the refusals", which the spec's Changes-by-file lists among the lifecycle rule's changes, without citing anything licensing the omission; license: the spec's own text plus the shipped rule; the two refusals with a rule-side trace are now mapped explicitly — no-fourth-severity rides Task 1's severity paragraph, hit-outstanding is already-shipped prose from wave one — and the self-review distinguishes "needs no task" from "is already in the file"

One defect was found by the session while applying the above, and it is
the wave's own most instructive moment. Retaining the reset sentence for
the second finding made Task 8's first check score `1` on both sides of
its edit — a check the repair itself rendered vacuous, in the plan whose
constraint against exactly that was written two rounds earlier. The
mechanical before/after comparison caught it immediately; reading would
not have, because the pattern still looked like the natural anchor for
the bullet. The check now keys on the qualifier the replacement
introduces:

- fixed — [Important] repairing the reset-sentence finding made Task 8's first check vacuous, since the phrase it searches is now present both before and after the edit; license: this plan's own before/after constraint; the check keys on `counting only rounds that returned a verdict` instead, which the original bullet lacks, and the step records why the obvious anchor is the wrong one

Answering the round's focusing question — whether a literal execution
leaves the two rule files saying exactly what the spec designed — the
reviewer's answer was "almost". It diffed every prescribed block against
the spec's sections and simulated the full task sequence: the states,
clauses, fold, historical forms, gate discriminator, Unfinished-work
corrections and all three retired-token consumers land as designed, and
no stranded consumer of `resolved`, `fixed`, `held` or "developer
contact" survives in either file. The single substantive gap was the
evidence-newness base above; the rest were un-specced additions,
deletions and false expectations.

The round confirmed both historically recurring classes are closed,
mechanically rather than by reading: every prose pattern is uniformly
`\s+`-separated and reproduced its stated before-value against the tree,
every anchored check is paired with both anchors agreeing in simulation,
and Task 11's Step 3 ordering assertion discriminates as intended.

Its stop signal: after these fixes land, another round buys little — the
prescribed prose has now been read hard against the spec and the whole
plan executed in simulation twice, so the remaining risk is concentrated
in the fix wave itself, and the economical shape is a short pass over
those edits rather than a fresh full read.

### 2026-09-02 — plan-adversary, fable 5, concerns (round 2, diff-scoped)

- fixed — [Important] Task 11's Step 2 banned-term sweep is itself in the wrapped-phrase class: `grep -rn 'ledger entry'` searches a two-word prose phrase with a literal space, so a surviving banned use wrapping as `ledger` / `entry` reads as clean — and the wave *edited this exact command* to add the `_Avoid_` filter without noticing its pattern; license: this plan's own prose-check constraint; the command is now `rg -U -n 'ledger\s+entry'` and the step records that the fifth instance of the class was written during the repair of the fourth
- fixed — [Minor] the wave-born before/after constraint is falsified by the plan's own checks — Task 2's Step 5 scores `6` and `1` on both sides because it verifies a prose claim rather than an edit, Task 11 edits nothing at all, and Task 5's Step 4 stated only an after-value — so the rule as written re-introduced the per-site judgement the wave had just spent three passes removing; license: the wave's own stated test, that a rule still asking the reader to classify the site is unfinished; the constraint is scoped to checks that verify an edit, the two exempt classes are named, and the exemption is claimed in each step's own words rather than inferred; Task 5's Step 4 now states its before-value, which is `0` rather than the `1` the round estimated
- fixed — [Minor] Task 4's `Files:` locator `spec-plan-lifecycle.md:~185-195` is stale by construction — the paragraph sits at line 178 today and lands near 255 once Tasks 1–3 insert above it — the same class round 1 reported against Task 6, repaired there and left standing here; license: round 1's finding, which defines the class; the number is gone and the step says why the prose locator is sufficient alone
- fixed — [Minor] Task 8 redefines "developer contact" but enumerates no consumers of the redefined term, leaving `workflow.md:322` asserting that a model-cap refusal *is* developer contact, which the new definition denies; license: Task 7's own precedent of enumerating a retired token's consumers, applied to a redefined term; Task 8 gains a check for the consumer and a step reconciling it to "forces developer contact", which is what the sentence always meant and leaves the behaviour unchanged

Answering the round's focusing question — where the fix wave repaired the
instance and missed the class — the reviewer found it **inside a single
command**: Task 11's Step 2 received round 1's `_Avoid_` filter while its
pattern stayed a single-line literal-space prose search, violating the
unconditional constraint the same wave had just written, in the one step
the wave was actively editing. Its secondary instance is Task 7 against
Task 8: the wave enumerated consumers of the retired *token* and never
asked the same question of the *term* Task 8 redefines.

The round verified the diff mechanically rather than by reading, as its
brief required — every Replace block matched verbatim and uniquely, every
starting-state expectation was reproduced against the tree, and the whole
plan was applied to scratch copies with every after-check re-run. That
simulation is what confirmed the vacuity repair in Task 11's Step 3 is
sound, and it is the reason the round's own stop signal rules out a third
diff-scoped pass.

Its stop signal: another diff-scoped round would not repay its cost — the
diff has been simulated to exhaustion and the leftovers were four
one-edit fixes, each licensed by the plan's own written constraints. What
the loop still owes is structural rather than marginal: on a plan only a
full-document round's LGTM terminates, so the confirming full-document
round is the right next dispatch, and it is also the only scope that can
reach the class behind the fourth finding — consumers of a redefined term
living outside the diff.

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

The propagation gate ran three times across this document's loop and
returned CLEAN every time: over the round-1 fix wave at `107dec0`, over
`4041e4f` after the developer-raised repairs, and over `c5339e6` before
the confirming round, each dispatch widening its positive scope as the
loop taught it what to look for. None produced a hit, so none writes a
gate line.

No run opened with the model self-report the workflow rule requires. The
second omitted it despite an emphatic instruction naming the first
omission, and the third returned the single word `CLEAN` and nothing
else. Three for three is a property of the agent rather than a one-off,
and the likely mechanism is that a self-report is neither a hunt target
nor a premise for classifying — the two kinds of instruction this agent
demonstrably acts on. Fixing it belongs in the agent's own card, where
the self-report becomes a duty instead of a request a brief can lose.
It is recorded here because the rule makes an unverified self-report a
reason to withhold reliance. Reliance is taken anyway, on a narrow derivation: the
guard exists to catch a silent substitution of the model actually run for
the one dispatched, and a propagation audit's prescribed rung is the
cheapest available family, which is what was named at dispatch. A
substitution could therefore only have run the audit *above* its
prescribed tier, which does not invalidate a structural CLEAN. Several of
the second run's specific claims — the quoted blocks at their stated
lines, and the `1, 1, 0, 0` starting state — were independently verified
in-session before it was dispatched.

Its stop signal: a re-round after the fix wave earns its cost, but
diff-scoped — the findings sit in check mechanics and two scope gaps,
not in the prescribed rule prose, which matched the spec everywhere it
was diffed. And a standing instruction for that round: **the
wrapped-phrase class has now produced four instances across two sweeps
that each declared completeness, so it is re-verified mechanically
rather than by reading.**
