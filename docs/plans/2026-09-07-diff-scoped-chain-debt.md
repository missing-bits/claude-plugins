---
ticket: none
date: 2026-09-07
status: draft
adversary: concerns (resolved 2026-09-07)
spec: ../specs/2026-09-07-diff-scoped-chain-debt-design.md
branch: feature/audit-errata
base: develop
---

# Diff-Scoped Chain Debt Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the review loop a durable record that a diff-scoped LGTM's chain debt was discharged — a sixth Unfinished-work class that surfaces the debt, a three-path `, debt discharged <date>` annotation that closes it, and the four rule corrections the new class exposes.

**Architecture:** Two rule files change, the glossary gains one clause, and two specs gain a ledger annotation. `spec-plan-lifecycle.md` owns the record — the new class, the annotation's grammar, the ordering against the `integrity:` hash, the Unresolved-verdict owner leg, the stop-signal line shape, and three census sentences rewritten count-free. `workflow.md` owns the loop's behaviour — the gate's pair offer, the confirming round's authority, the instruction to record a stop signal, and the restored concurrency reasoning. The split follows the two rules' existing division of labour; no sentence moves between them.

**Tech Stack:** Markdown rule files distributed as a Rules payload; `rg` and `grep` commands published inside the rules are the enforcement mechanism; `claude plugin validate` is the structural check.

## Global Constraints

- **No code.** Every deliverable is prose in a Markdown file. The verification for each task is a check whose result changes, plus `claude plugin validate`.
- **Edit with the Edit tool, never `sed -i` or `printf >>`** — the process-artifacts rule requires it for artifacts under `docs/` and applies equally to rule files here.
- **Line width follows each file's existing habit** — prose wraps at ~72 characters; the indented grammar blocks and published command lines run long and stay on one line.
- **Public-repo hygiene:** English only, no machine-specific paths, no company or client names.
- **`claude plugin validate .` and `claude plugin validate plugins/working-process` must both pass** after every task.
- **The spec is the source.** Where this plan and `docs/specs/2026-09-07-diff-scoped-chain-debt-design.md` disagree, the spec wins and the plan is wrong.
- **No version bump.** `plugins/working-process/.claude-plugin/plugin.json` already carries a `-dev.audit-errata` discriminator; the release PR mints the real number.
- **The manifest is an authoring aid, not the proof.** This plan's task list is a hand-written enumeration of edit sites, and the architect's round-2 answer names its limit outright: the real "no consumer left behind" guarantee is the propagation gate that fires after multi-site edits, not this list. Task 13 runs that sweep; no task may treat its own completeness as established by being listed here.
- **A check that searches for prose uses `rg -U` and puts `\s+` between *every* pair of words in the pattern; a check that searches for an anchored structural pattern uses `grep`.** These files wrap prose at about 72 characters, so a searched phrase may straddle a line ending and a single-line `grep` then returns 0 where the phrase is plainly present. The constraint is unconditional rather than applied where a wrap looks likely: where the wrap falls is not something a reader reliably predicts, and a uniformly `\s+` pattern is correct whether or not it wraps, so no judgement is exercised and no instance can be missed. An anchored pattern like `^- \*\*Chain debt\*\*` or `^    - signal <date>` cannot straddle by construction, so single-line matching is correct there.
- **`rg -c` prints nothing and exits 1 when its pattern does not match** — it never prints `0`. A step asserting absence with `rg` therefore expects *no output*; only `grep -c`, which does print `0`, is given a numeric zero expectation.
- **An anchored check on an indented block publishes *both* anchors — exact and tolerant — and asserts their equality.** Never one alone, and never a per-site decision about which. The exact anchor (`^    ` for a grammar block, `^- ` for a list entry) proves the prescribed text is well-formed at the indent the step prescribes; the tolerant anchor (`^\s*`) proves no variant survives anywhere else. Each alone has a blind spot that reads as success: the exact one passes while a leftover sits at another indent, the tolerant one passes while the prescribed block is mis-indented. Equality of the two counts is the assertion, and a divergence localizes which half failed. One case is copied rather than reasoned about: a check mirroring a command the rules publish reproduces it verbatim.
- **Every check that verifies an edit must return a different value before and after its step, and both values are stated.** A check whose before-value equals its after-value verifies nothing, however correct both numbers look — and it survives review precisely because nothing about it appears wrong. A check that asserts an **invariant** rather than verifying an edit is exempt, and the exemption is claimed in words on the step rather than inferred by a later reader: Task 9's paired anchors stay at zero to prove a shape was cited rather than copied, Task 11's placeholder guard stays at zero to prove no `<date>` survived, and every check in Task 13 reports an end state. Each says so where it stands.

---

### Task 1: The Chain debt class

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the `## Unfinished-work list` section, inserting a sixth entry after **Unfinished review-loop ledger** and before **Pending re-review**

**Interfaces:**
- Produces: the class name **Chain debt** and its published command. Tasks 2, 6, 11, 12 and 13 all cite one or the other.

The owner leg carries a second sentence the spec does not, and the departure is recorded here because it sits beside the text it concerns. The spec says a decline "has nothing to derive from, and there the debt correctly re-surfaces and the developer declines again" — true while it was written, when no standing decision existed. The developer ruled on 2026-09-07 that completed work is not chased, which makes the decline derivable for a document already at `status: implemented` and licenses a session to write the annotation without asking. The spec's sentence still governs every document in flight, where a decline remains a fresh decision. This is a developer ruling taken after the spec closed, so it outranks the plan's "the spec is the source" constraint rather than breaching it; the constraint bars the plan from inventing design, not the developer from deciding.

The sentence lands on the **owner** leg, never on the scope leg. The spec refuses a `status` predicate in a class scope, because `process-status` states that a scope "narrows where a hit counts, never whether the file qualifies" — an owner leg says what the next move is and carries no such constraint.

The scope leg carries one addition too, smaller and licensed differently: `and carrying -n for the same reason`. The spec's block ends at "for the reason the first one does", but the command the spec itself prescribes carries `-n`, and the sibling entry already explains why — confirming section membership needs line positions. So the clause states what the spec's own command implies rather than adding a decision. It is recorded here because the task's other addition is, and an undocumented departure beside a documented one reads as an oversight.

This task also touches `docs/domain/glossary.md`, which the spec's Changes-by-file section says no implementation task covers. That sentence scopes the six changes the grilling session applied inline; developer ruling 2 postdates it and opens a seventh, recorded in Step 8.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '^- \*\*' "$f"                  # Unfinished-work entries, exact anchor
grep -c '^\s*- \*\*' "$f"               # same, tolerant anchor
grep -c '^- \*\*Chain debt\*\*' "$f"    # the new entry, exact anchor
grep -c '^\s*- \*\*Chain debt\*\*' "$f" # the new entry, tolerant anchor
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before this task: `5`, `5`, `0`, `0`. The first two must be equal (no `- **` entry sits at another indent); the last two must be equal at zero.

- [ ] **Step 3: Insert the entry**

Place it directly after the **Unfinished review-loop ledger** entry's `Owner:` line, before `- **Pending re-review**`:

```markdown
- **Chain debt** — a diff-scoped `LGTM` heading carrying no record that
  what it owed was discharged.
  `rg -n --no-ignore --crlf '^### .*LGTM \(round [0-9]+, diff-scoped\)$' docs/`
  Scope: a hit counts only inside a `## Review rounds` section — the
  second entry to re-scope the default guard, for the reason the first
  one does, and carrying `-n` for the same reason.
  Owner: for a spec, the consumption gate's pair offer; for a plan, the
  confirming full-document round. On a document already at
  `status: implemented` the debt is discharged by recorded decline
  without any dispatch: completed work is not re-reviewed, so the
  annotation is written citing that standing decision, and a document
  still in flight keeps the pair offer.
```

- [ ] **Step 4: Run the check again**

Expected after: `6`, `6`, `1`, `1`. Each pair must be equal; a divergence in the first pair means the entry landed at the wrong indent, a divergence in the second means the heading text is malformed.

- [ ] **Step 5: Verify the published command runs and finds both live instances**

```bash
rg -n --no-ignore --crlf '^### .*LGTM \(round [0-9]+, diff-scoped\)$' docs/
```

Expected: **four lines, plus one** if this plan's own ledger already holds a diff-scoped `LGTM` heading that nothing has annotated.

The fixed four are two live instances — one in `docs/specs/2026-08-27-audit-agents-design.md`, one in `docs/specs/2026-09-07-diff-scoped-chain-debt-design.md` — and two from this plan itself, where Tasks 11 and 12 quote a round heading verbatim at column 0 inside a fenced block, because the command matches a line, not a document.

The contingent fifth is this plan's own review loop reaching its terminating shape: a plan's loop ends on a diff-scoped `LGTM` followed by a confirming full-document round, and the rules that would annotate that heading are what this plan ships. So between the loop closing and Task 3 landing, the heading sits unannotated. Task 13 Step 4 owns it and explains why it is a real hit discharged there rather than noise — unlike the two quoted blocks, it sits inside a genuine `## Review rounds` section and the scope leg does not reject it.

Line numbers are not asserted — they move as the documents change.

The plan's own two lines are output the class rejects, not hits it reports. The scope leg confines a hit to a `## Review rounds` section, and these sit under `### Task` headings; the default guard exists for exactly this reason, in the lifecycle rule's own words — a document quoting the convention describes it rather than instantiating it. So this step confirms two things at once: the rule ships a command that runs, and the scope leg earns its keep on the first document that tests it.

Round 1 offered truncating the two `Find:` blocks so they stop matching, and that is declined here. The blocks must stay byte-exact to be executable, and a plan that mangled its own quotations to keep a grep quiet would be hiding the case the scope leg was written for. Restating the expected values is the repair; demonstrating the guard is the bonus.

- [ ] **Step 6: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 7: Widen the glossary's third discharge path**

The entry enumerates that path as "the developer's recorded decline of the gate's pair offer". On an implemented document the gate never fired, so there is no pair offer to decline — yet ruling 2 licenses exactly that discharge, and the owner leg now ships it. The enumeration must cover what the rule permits.

Find:

```markdown
full-document round whatever its verdict, or the developer's recorded
decline of the gate's pair offer. Recorded as `, debt discharged <date>`
```

Replace with:

```markdown
full-document round whatever its verdict, or the developer's recorded
decline — of the gate's pair offer, or, where the document is already
implemented and the gate never fired, of the question that offer would
have put. Recorded as `, debt discharged <date>`
```

- [ ] **Step 8: Verify the glossary edit**

```bash
g=docs/domain/glossary.md
rg -Uc "decline\s+of\s+the\s+gate's\s+pair\s+offer\." "$g"
rg -Uc 'the\s+gate\s+never\s+fired' "$g"
```

Expected before: `1`, then no output. Expected after: no output, then `1`.

- [ ] **Step 9: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md docs/domain/glossary.md
git commit -m "feat(working-process): add the Chain debt Unfinished-work class"
```

---

### Task 2: The Unresolved-verdict owner leg's plan exception

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the **Unresolved verdict** entry's `Owner:` leg under `## Unfinished-work list`

**Interfaces:**
- Consumes: the class name **Chain debt** from Task 1.
- Produces: nothing later tasks read.

The defect this fixes predates the package: the published leg licenses closing a plan's verdict with `concerns (resolved <date>)` while `workflow.md` forbids terminating a plan's loop on a diff-scoped LGTM. The new class only illuminates it. The replacement states the exception without a count, so a later document kind cannot make it stale.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/spec-plan-lifecycle.md
rg -Uc 'Owner:\s+a\s+fresh\s+round\s+at\s+the\s+prescribed\s+tier,\s+or\s+the\s+resolution\s+annotation\s+above\.' "$f"
rg -Uc 'the\s+confirming\s+full-document\s+round\s+closes\s+the\s+verdict' "$f"
rg -Uc 'one\s+debt\s+seen\s+from\s+two\s+sides' "$f"
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: `1`, then no output twice (`rg -c` prints nothing on no match).

- [ ] **Step 3: Replace the owner leg**

Find:

```markdown
  Owner: a fresh round at the prescribed tier, or the resolution
  annotation above.
```

Replace with:

```markdown
  Owner: a fresh round at the prescribed tier, or the resolution
  annotation above — except on a plan whose latest round heading is a
  diff-scoped `LGTM`, where the confirming full-document round closes
  the verdict and the annotation may not, since a plan's loop never
  terminates on that heading. Such a plan matches Chain debt as well:
  one debt seen from two sides, both extinguished by that round, and the
  duplicate is deliberate.
```

- [ ] **Step 4: Run the check again**

Expected after: no output for the first pattern (the old sentence is gone), then `1` and `1`.

- [ ] **Step 5: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "fix(working-process): the Unresolved-verdict owner leg no longer licenses skipping a plan's confirming round"
```

---

### Task 3: The three-path annotation replaces the retired token

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the annotation paragraph under `## The disposition ledger`, between "Every terminal line carries exactly one authorizer." and the historical-shapes block

**Interfaces:**
- Produces: the token `, debt discharged <date>` and its three discharge paths. Tasks 4, 6, 7, 11 and 12 all write or cite it.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/spec-plan-lifecycle.md
rg -Uc 'chain\s+accepted' "$f"
rg -Uc 'debt\s+discharged' "$f"
grep -c '^    ### <date> — architect, <model>, LGTM (round 3, diff-scoped), debt discharged <date>$' "$f"
grep -c '^\s*### <date> — architect, <model>, LGTM (round 3, diff-scoped), debt discharged <date>$' "$f"
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: `1`, no output, `0`, `0`. The two token counts run under `rg -c`, which prints nothing rather than `0` on no match; the two anchored counts run under `grep -c`, which does print `0`. The last two must be equal.

- [ ] **Step 3: Replace the paragraph**

Find:

```markdown
One annotation extends those shapes, and nothing else does. A spec whose
developer accepts a
diff-scoped chain at the consumption gate gains `, chain accepted <date>`
on that round's LGTM heading: the dispatcher appends it there on the
decline, and its presence defeats the gate's re-ask, as `, waived <date>`
defeats the re-review offer.
```

Replace with:

```markdown
One annotation extends those shapes, and nothing else does. A
diff-scoped `LGTM` heading gains `, debt discharged <date>` once the
chain debt it carries is discharged, and its presence defeats the
consumption gate's re-ask, as `, waived <date>` defeats the re-review
offer:

    ### <date> — architect, <model>, LGTM (round 3, diff-scoped), debt discharged <date>

The token goes after the closing parenthesis rather than inside it. A
parenthesised token qualifies a value — `concerns (resolved <date>)`
changes what the verdict means — while a comma-appended token adds a
later event to a finished record, and this annotation is written later,
by a different actor, about a different event.

Three paths discharge the debt, all three write the same token, and the
dispatcher writes it in every case: the developer declining the gate's
pair offer, written in the decline turn before the work that decline
licenses begins; an integrity audit, written once its dispositions are
applied and before the `integrity:` stamp; and any later full-document
round, at its stamping turn, whatever its verdict — the debt is
discharged by the reading, not by the grade. A full-document round reads
the whole document, so it annotates every unannotated diff-scoped `LGTM`
heading above it rather than only the one it follows.

The token carries a date and nothing else. Each path leaves its own
trace — an `integrity:` stamp, a later full-document heading, or
neither — and no consumer reads the path, so recording it would give one
fact a second home. Where a session discharges the debt and dies before
annotating, the annotation's own derivation licenses a later session to
write it; only the decline path has nothing to derive from, and there
the debt correctly re-surfaces and the developer declines again.
```

- [ ] **Step 4: Run the check again**

Expected after: no output, `2`, `1`, `1`. The `debt discharged` count of `2` covers the definition sentence and the heading example — the three-path paragraph says "discharge the debt" rather than repeating the token, so it does not add to the count. Tasks 4 and 6 each add one more occurrence to this file, which is why Task 13 expects `4` here rather than `2`. The last two must be equal.

- [ ] **Step 5: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): replace the decline-only chain token with the three-path debt-discharged annotation"
```

---

### Task 4: The annotation precedes the hash, and an implemented document admits it

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the `integrity:` frontmatter bullet and the `implemented` frontmatter bullet

**Interfaces:**
- Consumes: the token from Task 3.
- Produces: the ordering Task 12 follows when it re-stamps this package's own spec.

Two one-sentence insertions, in two different bullets, joined because both license the same annotation against a rule that would otherwise forbid or invalidate it.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/spec-plan-lifecycle.md
rg -Uc 'the\s+annotation\s+is\s+written\s+before\s+the\s+hash\s+is\s+recomputed' "$f"
rg -Uc 'One\s+class\s+of\s+body\s+edit\s+is\s+excepted' "$f"
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: no output for either.

- [ ] **Step 3: Insert the ordering sentence into the `integrity:` bullet**

Find:

```markdown
  frontmatter's closing `---`, so writing the stamp never invalidates what
  it stamps. Stamper and gate run one command, so the comparison can never
```

Replace with:

```markdown
  frontmatter's closing `---`, so writing the stamp never invalidates what
  it stamps. Where the audit also discharges a chain debt, the annotation
  is written before the hash is recomputed: the hash covers the
  `## Review rounds` section, so a stamp written first is stale the moment
  the annotation lands. Stamper and gate run one command, so the comparison can never
```

- [ ] **Step 4: Insert the body-edit exception into the `implemented` bullet**

Find:

```markdown
  frontmatter, never in the body: a verdict certifies the body it was
  given, and an `integrity:` hash covers exactly that text.
```

Replace with:

```markdown
  frontmatter, never in the body: a verdict certifies the body it was
  given, and an `integrity:` hash covers exactly that text. One class of
  body edit is excepted: a ledger annotation recording a process event,
  such as `, debt discharged <date>`, is a process record rather than a
  design amendment.
```

- [ ] **Step 5: Run the check again**

Expected after: `1` and `1`.

- [ ] **Step 6: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "fix(working-process): order the debt annotation before the integrity hash and license it on an implemented document"
```

---

### Task 5: The stop-signal line shape

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — a new paragraph under `## The disposition ledger`, after the narrative-prose paragraph and before `### Gate lines`

**Interfaces:**
- Produces: the line shape `- signal <date> — <what the reviewer judged the next round worth>`. Task 9 writes the instruction that produces it and cites this shape by reference.

The shape lives here because the ledger owns every other line shape; the instruction to write one lives in `workflow.md`, beside the ask that produces it. Splitting the rider this way is what the integrity audit settled.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '^    - signal <date> — ' "$f"     # exact anchor, grammar-block indent
grep -c '^\s*- signal <date> — ' "$f"      # tolerant anchor
rg -Uc 'a\s+stop\s+signal\s+owes\s+nobody\s+a\s+next\s+move' "$f"
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: `0`, `0`, and no output. The first two must be equal.

- [ ] **Step 3: Insert the paragraph**

Find:

```markdown
ignores the prose.

### Gate lines
```

Replace with:

```markdown
ignores the prose.

A reviewer's stop signal takes a line of its own, under the heading of
the round that gave it:

    - signal <date> — <what the reviewer judged the next round worth>

It carries the leading token `signal`, no severity — a judgment about
the next round's marginal value is not a finding — and no authorizer,
since nobody licensed it. It joins no anchor: a stop signal owes nobody
a next move, so it is closed the moment it is written, as a gate line
is. The workflow rule owns the ask that produces it.

### Gate lines
```

The `Find:` block spans the sentence's real line break and carries the
`### Gate lines` heading along, so the `Replace with:` block restores
that heading at the end. Quoting the sentence on one line would match
nothing: the file wraps it after "and".

- [ ] **Step 4: Run the check again**

Expected after: `1`, `1`, `1`. The first two must be equal; a divergence means the block sits at the wrong indent.

- [ ] **Step 5: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): give a reviewer's stop signal a ledger line shape"
```

---

### Task 6: Three census sentences rewritten count-free

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the payload paragraph under `## The disposition ledger`, the default-guard paragraph under `## Unfinished-work list`, and the anchor paragraph after the list

**Interfaces:**
- Consumes: the class from Task 1 and the token from Task 3 — the third rewrite names both.
- Produces: nothing later tasks read.

Each sentence encodes a census of the list and went stale the moment Task 1 added a sixth entry. Updating the numbers would repeat wave two's frozen-counter mistake; the sentences state properties instead, so a seventh class costs no accounting edit.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/spec-plan-lifecycle.md
rg -Uc 'Four\s+of\s+the\s+five\s+Unfinished-work\s+commands' "$f"
rg -Uc 'the\s+review-loop\s+entry\s+below\s+is\s+the\s+one\s+that\s+does' "$f"
rg -Uc 'Those\s+anchors\s+all\s+sit\s+on\s+a\s+frontmatter\s+field' "$f"
rg -Uc '[Aa]n\s+entry\s+publishing\s+its\s+own\s+scope' "$f"
```

The fourth pattern opens with `[Aa]` because the replacement idiom appears sentence-initially in one rewrite and mid-sentence in the other; `rg` is case-sensitive by default, so a bare `an` would silently miss half of what this step counts.

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: `1`, `1`, `1`, and no output for the fourth. The three stale sentences are present and the replacement idiom is absent.

- [ ] **Step 3: Rewrite the payload sentence**

Find:

```markdown
Payload costs nothing structurally. Four of the five Unfinished-work
commands anchor a frontmatter field and are held to the frontmatter
block by the list's default scope guard, so no body line reaches them at
all; the fifth is this ledger's own, anchored on `^- `, which an indented
continuation does not match.
```

Replace with:

```markdown
Payload costs nothing structurally. An Unfinished-work command under the
list's default scope guard is held to the frontmatter block, so no body
line reaches it at all; an entry publishing its own scope anchors a
leading disposition token or a round heading, and an indented
continuation matches neither.
```

- [ ] **Step 4: Rewrite the default-guard sentence**

Find:

```markdown
entry re-scopes it only by publishing its own match scope as a fourth
leg, and the review-loop entry below is the one that does.
```

Replace with:

```markdown
entry re-scopes it only by publishing its own match scope as a fourth
leg, and the entries below that do so say it there.
```

- [ ] **Step 5: Rewrite the anchor sentence**

Find:

```markdown
tolerate. Those anchors all sit on a frontmatter field; the review-loop
entry anchors a leading disposition token instead, so there the close is
a rewrite — `open` or `held` becomes `fixed <date>` or
`declined <date>`, and the anchor stops matching.
```

Replace with:

```markdown
tolerate. Those anchors sit on a frontmatter field wherever the default
guard holds. An entry publishing its own scope anchors a body line
instead — a leading disposition token or a round heading — and there the
close is a rewrite or an appended annotation: `open` or `held` becomes
`fixed <date>` or `declined <date>`, and a discharged chain debt gains
`, debt discharged <date>`. Either way the anchor stops matching.
```

- [ ] **Step 6: Run the check again**

Expected after: no output for the first three (all three stale sentences gone), then `2` for the fourth — the replacement idiom appears in the payload rewrite and the anchor rewrite. The default-guard rewrite uses "the entries below that do so", a different construction, and is verified by its own check below.

- [ ] **Step 7: Verify the default-guard rewrite landed**

```bash
rg -Uc 'the\s+entries\s+below\s+that\s+do\s+so\s+say\s+it\s+there' plugins/working-process/rules/spec-plan-lifecycle.md
```

Expected before this task: no output. Expected after: `1`.

- [ ] **Step 8: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 9: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "fix(working-process): state the list's anchor and payload properties without counting its entries"
```

---

### Task 7: The gate's pair offer and the confirming round's autonomy

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the two paragraphs under `### What a diff-scoped LGTM certifies` that follow the opening definition

**Interfaces:**
- Consumes: the token from Task 3.
- Produces: nothing later tasks read.

This is the second and last site of the retired token. It narrates the same mechanism independently of the lifecycle rule's definition site, so leaving it would ship a grep saying one word while the fix writes another — the exact defect the design names when arguing that class and token rename together. The surrounding property-not-event wording ("the developer accepting the chain … the acceptance is recorded") goes with it.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/workflow.md
rg -Uc 'chain\s+accepted' "$f"
rg -Uc 'debt\s+discharged' "$f"
rg -Uc 'the\s+acceptance\s+is\s+recorded\s+rather\s+than\s+remembered' "$f"
rg -Uc 'The\s+confirming-round\s+arm\s+therefore\s+blocks\s+plan-writing' "$f"
rg -Uc 'runs\s+under\s+the\s+loop.s\s+standing\s+consent' "$f"
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: `1`, then no output, then `1`, then no output twice. Both token counts run under `rg -c`, so the absent one prints nothing rather than `0`.

- [ ] **Step 3: Replace both paragraphs**

Find:

```markdown
For a spec, the consumption gate before plan-writing offers the pair as
one question — an integrity audit or a confirming full-document round —
and never an offer followed by a re-offer of the option just declined.
When the `integrity-auditor` agent is absent the offer carries the
confirming round alone. Declining is the developer accepting the chain
explicitly, and the acceptance is recorded rather than remembered: the
dispatcher appends `, chain accepted <date>` to the diff-scoped LGTM
heading, and that annotation defeats the gate's re-ask.

For a plan the loop never terminates on a diff-scoped LGTM: one
full-document confirming round follows, and the confirming round's
verdict is the one stamped. That carries the single named exception to
the relay-then-stamp order above — a plan's diff-scoped LGTM is relayed
and its round record written, and only the frontmatter stamp waits for
the confirming round. Recovery therefore reads the ledger rather than
the stamp: a plan whose latest round heading is a diff-scoped LGTM that
no later full-document round follows is re-offered its confirming round
at the document's next touch, whatever the frontmatter says.
```

Replace with:

```markdown
For a spec, the consumption gate before plan-writing offers the pair as
one question — an integrity audit or a confirming full-document round —
and never an offer followed by a re-offer of the option just declined.
When the `integrity-auditor` agent is absent the offer carries the
confirming round alone. The two arms cost differently and the offer says
so: an audit returns material for the dispatcher to dispose of and
leaves the verdict alone, while a confirming round on a spec is a new
loop's first round, since the spec's LGTM already closed its loop — it
mints its own verdict and stamps it, so a `concerns` there flips the
field back while plan-writing waits. The confirming-round arm therefore
blocks plan-writing; the audit arm does not, and plan-writing follows
its dispositions.

Declining is the developer discharging the chain debt by release rather
than by performance, and the discharge is recorded rather than
remembered: the dispatcher appends `, debt discharged <date>` to the
diff-scoped LGTM heading, in the shape the spec-plan-lifecycle rule
defines, and that annotation defeats the gate's re-ask. The other two
paths write the same token.

For a plan the loop never terminates on a diff-scoped LGTM: one
full-document confirming round follows, and the confirming round's
verdict is the one stamped. That round runs under the loop's standing
consent like any other — the rules mandate it, so it is no decision of
the developer's and spends none of the round's one interruption. It
carries the single named exception to the relay-then-stamp order above —
a plan's diff-scoped LGTM is relayed and its round record written, and
only the frontmatter stamp waits for the confirming round. Recovery
therefore reads the ledger rather than the stamp: a plan whose latest
round heading is a diff-scoped LGTM that no later full-document round
follows is re-offered its confirming round at the document's next touch,
whatever the frontmatter says.
```

- [ ] **Step 4: Run the check again**

Expected after: no output, `1`, no output, `1`, `1`.

- [ ] **Step 5: Confirm the retired token is gone from the whole repo's rule payload**

```bash
rg -Un --no-ignore 'chain\s+accepted' plugins/
```

Expected: no output. Before this task the lifecycle rule's occurrence was already removed by Task 3, so this step's before-value is one line (`workflow.md`) and its after-value is none.

- [ ] **Step 6: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): price the gate's two arms and move the decline path onto the debt token"
```

---

### Task 8: The confirming round counts against the cap

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the `Round cap` bullet under `### Terminators`

**Interfaces:**
- Consumes: nothing.
- Produces: nothing later tasks read.

The fact lands here and nowhere else: this bullet is where the count is defined, and restating it under `### What a diff-scoped LGTM certifies` would create the two-homes-for-one-fact defect the design refuses elsewhere. Task 7 owns the autonomy half for the same reason, in the subsection where the confirming round is introduced.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/workflow.md
rg -Uc "A\s+plan's\s+confirming\s+full-document\s+round\s+counts\s+like\s+any\s+other" "$f"
rg -Uc 'escalates\s+once\s+before\s+its\s+confirming\s+round' "$f"
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: no output for either.

- [ ] **Step 3: Extend the bullet**

Find:

```markdown
  itself three fresh rounds after every compaction.
```

Replace with:

```markdown
  itself three fresh rounds after every compaction. A plan's confirming
  full-document round counts like any other: the count folds round
  headings, and excluding one kind would mean classifying them — a
  second fragile derivation in the one place the rules already concede
  the cap is best-effort. A plan whose loop spent its three rounds
  therefore escalates once before its confirming round, which is the
  most expensive shape a round takes and the one a cap guarding spend
  should guard first.
```

- [ ] **Step 4: Run the check again**

Expected after: `1` and `1`.

- [ ] **Step 5: Confirm the fact has exactly one home**

```bash
rg -Uc "confirming\s+full-document\s+round\s+counts\s+like\s+any\s+other" plugins/working-process/rules/workflow.md
```

Expected before: no output. Expected after: `1` — one occurrence, not two. A `2` here means the fact was also restated in `### What a diff-scoped LGTM certifies`, which this task forbids.

- [ ] **Step 6: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): count a plan's confirming round against the round cap"
```

---

### Task 9: The instruction to record a stop signal

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the paragraph under `### Re-dispatch briefs` that asks the reviewer for its stop signal

**Interfaces:**
- Consumes: the line shape from Task 5, cited by reference rather than restated.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/workflow.md
rg -Uc 'The\s+signal\s+is\s+recorded\s+where\s+a\s+later\s+session\s+can\s+cite\s+it' "$f"
grep -c '^    - signal <date> — ' "$f"
grep -c '^\s*- signal <date> — ' "$f"
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: no output, then `0` and `0`. The two zeros must stay zero after this task — the shape belongs to the lifecycle rule, and a copy here would be the second home this plan refuses.

- [ ] **Step 3: Insert the instruction**

Find:

```markdown
enough, and it informs the developer's decision rather than replacing
it. Where the ledger records a deviation from a reviewer's suggestion,
```

Replace with:

```markdown
enough, and it informs the developer's decision rather than replacing
it. The signal is recorded where a later session can cite it: one line
under the heading of the round that gave it, in the shape the
spec-plan-lifecycle rule defines. A signal surviving only in a relay
dies with the next compaction, and practice has needed it twice — once
to justify overriding one, once to close a loop on one. Where the ledger
records a deviation from a reviewer's suggestion,
```

- [ ] **Step 4: Run the check again**

Expected after: `1`, then `0` and `0` — unchanged. **These two assert an invariant rather than verify an edit**, which is what exempts them from the before-and-after rule: they prove the shape stayed in the lifecycle rule and was cited here rather than copied.

- [ ] **Step 5: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): record a reviewer's stop signal in the ledger"
```

---

### Task 10: The concurrency limit recovers its reasoning

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the "At most one live round" bullet under `## Dispatching a verdict agent`

**Interfaces:**
- Consumes: nothing.
- Produces: nothing later tasks read.

The ancestor design decided this and the shipped rule dropped it, so restoring it is errata. One sentence is genuinely new, because the ancestor ruled before the round sequence carried weight.

- [ ] **Step 1: Write the failing check**

```bash
f=plugins/working-process/rules/workflow.md
rg -Uc 'A\s+parallel\s+round\s+from\s+another\s+session\s+is\s+accepted\s+as\s+undetectable' "$f"
rg -Uc 'punches\s+a\s+hole\s+no\s+round\s+ever\s+read' "$f"
grep -c 'undetectable' "$f"
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: no output, no output, `1`. The single existing `undetectable` is the out-of-session-edit bullet three bullets below, which this task leaves alone.

- [ ] **Step 3: Extend the bullet**

Find:

```markdown
- At most one live round per document per field within the session;
  superseding a running round stops it when the platform offers a
  stop, otherwise the stale result is relayed as stale and never
  stamped.
```

Replace with:

```markdown
- At most one live round per document per field within the session;
  superseding a running round stops it when the platform offers a
  stop, otherwise the stale result is relayed as stale and never
  stamped. A parallel round from another session is accepted as
  undetectable and stays benign: both rounds record in the body and the
  field holds the later stamp. One consequence postdates that decision —
  a diff-scoped LGTM certifies a chain, so an interleave punches a hole
  no round ever read. The discharge paths are the mitigation, since an
  audit and a full-document round each read the whole document, and a
  heading-derived cap over-counts under interleave, which escalates
  early.
```

- [ ] **Step 4: Run the check again**

Expected after: `1`, `1`, `2`.

- [ ] **Step 5: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "fix(working-process): restore the concurrency limit's reasoning and name its one new consequence"
```

---

### Task 11: Backfill the live instance

**Files:**
- Modify: `docs/specs/2026-08-27-audit-agents-design.md` — the round-3 heading and a new line in its `## Review rounds` section

**Interfaces:**
- Consumes: the token from Task 3 and the body-edit licence from Task 4.

**The token's date is the discharge event's date, everywhere in this plan.** The spec rules that the annotation "names an event — this heading's debt was discharged on that date", so the date answers *when the discharge happened*, never when the edit was typed. On this document the discharge is the developer's decline, so the token reads `, debt discharged 2026-09-07` whatever day implementation lands. Task 12 resolves it the same way against its audit, and Task 13's contingent annotation against its confirming round. A ledger line's own leading date is a different date under a different rule — the ledger's — and the two are distinguished in Step 4.

**The developer's ruling is recorded and dated 2026-09-07** — see *Developer rulings* below. The backfill is the decline path exercised late, not a fourth path: no audit ran, no later full-document round was dispatched, and none ever will be, since the document is `implemented` and the work it designed has shipped. What remains is exactly what the decline path is — the developer looking at a chain nobody read whole and accepting it knowingly. Writing the token without that decision would have put a false claim in the record, since on this document no reading ever happened; the ruling is what makes the annotation true.

- [ ] **Step 1: Write the failing check**

```bash
f=docs/specs/2026-08-27-audit-agents-design.md
grep -c '^### 2026-08-27 — architect, fable 5, LGTM (round 3, diff-scoped)$' "$f"
rg -Uc 'debt\s+discharged' "$f"
grep -c 'ruling:' "$f"
grep -c '<date>' "$f"
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: `1`, no output (`rg -c` prints nothing on no match), `0`, `0`.

- [ ] **Step 3: Annotate the heading**

Find:

```markdown
### 2026-08-27 — architect, fable 5, LGTM (round 3, diff-scoped)
```

Replace with:

```markdown
### 2026-08-27 — architect, fable 5, LGTM (round 3, diff-scoped), debt discharged 2026-09-07
```

The date is the ruling's, not the implementation's, for the reason this task's preamble gives.

- [ ] **Step 4: Record the ruling in the ledger**

Append to the same round's lines, after the two existing `fixed` lines. **Two dates appear and they are not the same date.** The leading `<date>` is the implementation date — when this line reached its terminal state, under the ledger's rule. The date inside the quoted token is `2026-09-07`, because it quotes what Step 3 wrote on the heading and the token records the discharge event. No literal `<date>` may survive:

```markdown
- fixed <date> — this round's diff-scoped LGTM left a chain debt that nothing recorded, and the document reached `implemented` unpaid; ruling: 2026-09-07; the developer accepted the chain on the record — the decline path exercised late, since no audit ran, no later full-document round was dispatched, and none can be — and the heading gains `, debt discharged 2026-09-07`
```

Three dates therefore sit on this one line, each under its own rule: the leading date is the ledger's, `ruling:` is when the developer decided, and the quoted token's is the discharge event's. The ledger requires the first two even where they coincide. The severity bracket is omitted because the sole authorizer is `ruling:` and no reviewer graded it — both legs hold, as the ledger's own rule requires.

- [ ] **Step 5: Run the check again**

Expected after: `0` (the bare heading is gone), `2` (heading and ledger line), `1`, and `0`. The last stays `0` before and after, and **asserts an invariant rather than verifying an edit** — no literal `<date>` may exist in this document at any point. It is the only value here that distinguishes a correct edit from a placeholder left in place; without it every other number is identical whether the dates were substituted or not.

- [ ] **Step 6: Confirm the class no longer reports this document**

```bash
rg -n --no-ignore --crlf '^### .*LGTM \(round [0-9]+, diff-scoped\)$' docs/
```

Expected: one line fewer than Task 1 Step 5 returned — four dropping to three, or five dropping to four where this plan's own unannotated LGTM heading is present, which that step explains. The annotated heading drops out, leaving `docs/specs/2026-09-07-diff-scoped-chain-debt-design.md`, which Task 12 closes, plus this plan's own two quoted blocks, which the scope leg rejects, plus that contingent heading if it exists.

- [ ] **Step 7: Commit**

```bash
git add docs/specs/2026-08-27-audit-agents-design.md
git commit -m "docs: discharge the audit-agents spec's chain debt by recorded decline"
```

---

### Task 12: Discharge this package's own spec and re-stamp its hash

**Files:**
- Modify: `docs/specs/2026-09-07-diff-scoped-chain-debt-design.md` — the round-2 heading and the `integrity:` frontmatter field

**Interfaces:**
- Consumes: the token from Task 3 and the ordering from Task 4.

The spec is a second instance of its own subject: round 2 was diff-scoped and returned LGTM. Its debt was already discharged by the integrity audit at the consumption gate — the audit is one of the three paths — but the token that records it did not exist until Task 3 shipped. This task writes the annotation the audit earned, then re-stamps the hash, in exactly the order Task 4 prescribes.

- [ ] **Step 1: Write the failing check**

```bash
f=docs/specs/2026-09-07-diff-scoped-chain-debt-design.md
grep -c '^### 2026-09-07 — architect, fable 5, LGTM (round 2, diff-scoped)$' "$f"
grep -n '^integrity:' "$f"
sed '1,/^---$/d' "$f" | shasum | cut -c1-7
```

- [ ] **Step 2: Run it and confirm the before-values**

Expected before: `1`; the `integrity:` line reads `integrity: 2026-09-07 (sha: 4a838b2)`; and the recomputed hash is `4a838b2`, matching the stamp. If the recomputed hash already differs, stop — the document changed since the audit, and the stamp must not be carried forward over an unaudited edit.

- [ ] **Step 3: Annotate the heading**

Find:

```markdown
### 2026-09-07 — architect, fable 5, LGTM (round 2, diff-scoped)
```

Replace with:

```markdown
### 2026-09-07 — architect, fable 5, LGTM (round 2, diff-scoped), debt discharged 2026-09-07
```

- [ ] **Step 4: Recompute the hash**

```bash
sed '1,/^---$/d' docs/specs/2026-09-07-diff-scoped-chain-debt-design.md | shasum | cut -c1-7
```

Expected: a value other than `4a838b2`. Record it; the next step writes it.

- [ ] **Step 5: Re-stamp the field**

Replace `integrity: 2026-09-07 (sha: 4a838b2)` with `integrity: 2026-09-07 (sha: <the value from Step 4>)`.

- [ ] **Step 6: Verify stamp and body agree**

```bash
f=docs/specs/2026-09-07-diff-scoped-chain-debt-design.md
grep '^integrity:' "$f"
sed '1,/^---$/d' "$f" | shasum | cut -c1-7
```

Expected: the hash in the field equals the recomputed hash. The stamp covers the text below the frontmatter, so writing the field never invalidates what it stamps.

- [ ] **Step 7: Confirm the class reports nothing**

```bash
rg -n --no-ignore --crlf '^### .*LGTM \(round [0-9]+, diff-scoped\)$' docs/
```

Expected: one line fewer than Task 11 Step 6 returned — three dropping to **two**, or four dropping to three where this plan's own unannotated LGTM heading is present. The two that always remain are this plan's quoted blocks in Tasks 11 and 12, which sit outside any `## Review rounds` section and which the scope leg therefore rejects.

Both live instances are now discharged, so the class ships with no permanent **hit**. It does not ship with no permanent command *output*, and the difference is the whole point of the scope leg: a command returns lines, and confirmation turns a line into a hit. An earlier draft of this step claimed no permanent hit by asserting no output, which conflated the two.

This plan's own contingent heading is a real hit rather than rejected output, and it is not this task's to close — Task 13 Step 4 discharges it under the derivation licence, after every rule edit has landed.

- [ ] **Step 8: Commit**

```bash
git add docs/specs/2026-09-07-diff-scoped-chain-debt-design.md
git commit -m "docs: annotate this spec's discharged chain debt and re-stamp its integrity hash"
```

---

### Task 13: End-state sweep

**Files:**
- Modify, conditionally: `docs/plans/2026-09-07-diff-scoped-chain-debt.md` — Step 4's annotation, where this plan's own ledger holds an unannotated diff-scoped LGTM heading
- Modify, conditionally: whatever document Step 6's gate reports a hit against — the fix plus its gate line
- Otherwise none

**Every check in this task asserts an end state rather than verifying an edit**, which is the exemption the before-and-after constraint requires be claimed in words. The two writes above are conditional repairs the checks discover, not edits any check verifies. The task's purpose is to catch what a hand-written manifest cannot guarantee: the propagation gate is the real backstop, and Step 6 is where it runs.

- [ ] **Step 1: The retired token survives nowhere in shipped content**

```bash
rg -Un --no-ignore 'chain\s+accepted' plugins/ docs/domain/
```

Expected: one line — `docs/domain/glossary.md`, the `_Avoid_` ban that names it. Design documents under `docs/specs/` and `docs/plans/` keep their historical occurrences and are out of scope: an archived document records what it recorded.

- [ ] **Step 2: The new token appears in both rule files**

```bash
rg -Uc 'debt\s+discharged' plugins/working-process/rules/spec-plan-lifecycle.md
rg -Uc 'debt\s+discharged' plugins/working-process/rules/workflow.md
```

Expected: `4` and `1`. The lifecycle rule's four are Task 3's definition sentence and heading example, Task 4's body-edit exception, and Task 6's anchor rewrite. A zero on either side means one of the two rule files was missed — the split-vocabulary failure the design names.

- [ ] **Step 3: The Unfinished-work list has six entries and no accounting sentence**

```bash
f=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '^- \*\*' "$f"
grep -c '^\s*- \*\*' "$f"
rg -Uc 'Four\s+of\s+the\s+five' "$f"
```

Expected: `6`, `6`, and no output.

- [ ] **Step 4: Every published command in the list runs**

Run each `rg` command the `## Unfinished-work list` section publishes, exactly as written, from the repo root. Expected: each exits without a usage error. Hits are read against each entry's scope, and the whole sweep should report no unfinished work — no `grilled: grilling`, no open or held ledger line, no pending re-review, and no misplaced stamp.

One known line is rejected output rather than a hit, and is named here so an executor is not left deciding whether the sweep failed: the Grilling-pending command returns `docs/plans/2026-07-13-rules-distribution.md`, where `grilled: grilling` appears in the body as part of a quoted frontmatter example. The default guard rejects it — a document quoting the convention describes it rather than instantiating it — exactly as Task 12 Step 7 predicts its own rejected output.

Two classes need a word beyond that, because this plan is itself a document the sweep reads.

**Chain debt on this plan.** A plan's loop terminates on a diff-scoped LGTM followed by a confirming full-document round, so by the time this task runs, this plan's own `## Review rounds` section may hold a diff-scoped LGTM heading. That is a real hit, not noise, and it is **discharged here rather than held**: a later full-document heading is on the page, and Task 3's own text says the annotation's derivation licenses a later session to write it.

Append the bare `, debt discharged <date>` token to that heading, and nothing else, `<date>` being the confirming round's date — the discharge event's, by the rule Task 11's preamble states once for the whole plan. The confirming round's heading is what licenses the write, so it belongs in the session's derivation — never inside the token, which Task 3 rules "carries a date and nothing else" precisely so one fact gets no second home.

The two lines Tasks 11 and 12 quote inside fenced blocks are a different matter and stay — they sit outside any `## Review rounds` section and the scope leg rejects them.

**Unresolved verdict on this plan.** A `blocking` or `concerns` round closed by annotation rather than by a fresh round leaves the field matching until the annotation lands. Read the field, and if a round's disposition is still open, that is unfinished work the developer owns rather than something this task closes.

Any other hit that survives is reported to the developer rather than fixed here.

- [ ] **Step 5: Validate the plugin**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 6: Dispatch the propagation gate**

Dispatch the `propagation-auditor` agent on the cheapest available family, named explicitly, over this branch's change set. The brief derives its own changed-interface list rather than receiving one: an earlier round in this series was handed a list of tokens to hunt, hunted exactly those, and returned CLEAN while missing an entire changed interface the brief had described only as context. Write the brief as positive scope — what to report — never as a prohibition. Fix confirmed hits under their own derivation and record each as a gate line under the last round heading of the document it concerns; dismiss a hit only in writing, with its counter-derivation.

- [ ] **Step 7: Report and hand back**

Report to the developer: what the sweep found, what the gate returned, whether the `propagation-auditor` reported its model, and any hit still outstanding.

Commit first, if Step 4 or Step 6 wrote anything. Those writes are process artifacts and ride along with the work's commits rather than being left dirty:

```bash
git add -A docs/
git commit -m "docs: discharge this plan's own chain debt and close the gate's hits"
```

Where neither step wrote, there is nothing to commit and this step is skipped.

Report one thing more, which no earlier step covers: **the installed rule copies under `.claude/rules/working-process/` now drift.** They are a consumer of every sentence this plan rewrote — both carry the retired token today — and no task edits them, because a Rules payload is distributed by the `sync-rules` engine rather than by hand. Offer that run. The drift hook is the designed backstop, which is why this is a hand-back line rather than a task; leaving it unsaid would let the session's own rules stay a version behind the ones it just shipped. A missing self-report is expected rather than anomalous — the prescribed rung is already the cheapest family, so a silent substitution could only run the audit above tier, which does not invalidate a structural CLEAN. Then offer the plan-adversary round: `status` moves to `approved` on the developer's word, not this task's.

---

## Developer rulings

The questions the spec put to the developer, all answered 2026-09-07. They are recorded here rather than in the spec: the spec is audited and hash-stamped, so amending it would re-arm the stamp and break Task 12's precondition for no gain. The lifecycle rule already routes them here — held spec questions are asked before the plan is written.

1. **The live instance is backfilled.** The developer accepts the audit-agents spec's chain on the record, as the decline path exercised late. Task 11 runs and cites `ruling: 2026-09-07`.
2. **Completed work is not chased.** A document found in this state later gets the same recorded decline without any dispatch — no audit, no confirming round. Task 1's owner leg carries this as a standing decision so a future session can cite it instead of re-asking; the paragraph under that task records how it departs from the spec's narrower sentence and why the departure is the developer's to make. A document still in flight keeps the pair offer, where a decline remains a fresh decision.

3. **`process-status` stays untouched.** The original question was aimed at the wrong surface: the skill groups hits by document and reports "the owner the entry carries", so Task 2's `one debt seen from two sides` explanation already rides to the report on the owner leg the skill copies. Whether a long leg arrives whole or condensed does not matter, because two adjacent lines whose owners both name the confirming round read as one job. The developer ruled on 2026-09-07 to leave the skill alone, so the spec's `No process-status edit at all` refusal now covers reporting as well as scope, and a skill that correlates class pairs — which would need extending for every future pair — is refused rather than deferred.

## Review rounds

### 2026-09-07 — plan-adversary, fable 5, concerns (round 3, full-document)

The confirming round the loop owed. It simulated all thirteen tasks in
order against the live payload files: every `Find:` block matches
byte-exactly and uniquely **at its execution moment**, none broken by an
earlier task's edit to the same file; every stated before-value and
after-value verifies, end-state counts included; the counting chain
resolves; Task 12's hash precondition holds. The recorded deviation on
Task 1 Step 5 survived attack — Tasks 11 and 12 need those headings
byte-exact as Edit anchors, so truncating them would trade a quiet grep
for two broken edits.

- fixed 2026-09-07 — [Important] Task 11's two substitution instructions contradict each other, so the token's date is unresolved: Step 3 writes the ruling's date into the heading while Step 4 orders the implementation date for both occurrences and calls it the same substitution, and every published check passes with either date written; license: the spec's ruling that the token "names an event — this heading's debt was discharged on that date", plus the ledger's own rule that a terminal line's leading date is when the line reached that state; the token's date is now stated once as the discharge event's date, Step 4 distinguishes the leading date from the quoted token's date, and Task 13's contingent annotation carries the same rule
- fixed 2026-09-07 — [Minor] Task 13 can write two documents — Step 4's contingent annotation and Step 6's gate lines — while its `Files:` line says it modifies nothing, which is also the line the before-and-after exemption rests on, and no step commits them; license: the process-artifacts rule that artifact updates ride along with their work's commits and are never left dirty; the `Files:` line now names both conditional writes, the exemption is re-anchored to the checks rather than to the task, and a conditional commit step closes them
- fixed 2026-09-07 — [Minor] the before-and-after constraint claims Task 13 is the sole exempt task while Tasks 9 and 11 both carry deliberate invariant guards that score the same value before and after; license: the constraint's own requirement that an exemption be claimed in words rather than inferred, which both guards already do; the constraint now exempts any check whose step declares it asserts an invariant, and the "sole exempt task" claim is gone
- fixed 2026-09-07 — [Minor] Task 1's scope leg adds ", and carrying `-n` for the same reason", which the spec's prescribed block does not contain, recorded nowhere — unlike the owner-leg addition the same task documents at length; license: the spec's own prescribed command, which carries `-n`, and the sibling entry that explains why; the addition is now recorded beside the owner-leg departure it sits next to
- fixed 2026-09-07 — [Minor] the glossary's Chain debt entry enumerates the third discharge path as "the developer's recorded decline of the gate's pair offer", which no longer covers the instance developer ruling 2 licenses — an implemented document where the gate never fired and so offered no pair to decline; license: ruling 2 itself, plus the spec's own reasoning for the live instance that the gate which should have asked never fired; Task 1 gains a glossary step, and the departure from the spec's "no implementation task covers these" is recorded there
- fixed 2026-09-07 — [Minor] Task 13 Step 4 predicts a hit-clean sweep without predicting its known rejected output: the Grilling-pending command returns one line today, a body quote of the frontmatter example in `docs/plans/2026-07-13-rules-distribution.md`; license: Task 12 Step 7's own practice of naming rejected output so an executor is not left deciding whether the sweep failed; the step now names that line and why the default guard rejects it

- signal 2026-09-07 — another round would not repay itself: the Important is a two-sentence repair plus one date rule stated once, the five Minors are one-sentence touches, and this round performed the whole-document read the loop owed, so nothing unread remains for a round 4 to certify; the leftovers are worth a fix wave and the developer's eyes on the date rule, not a re-read

Answering the round's focusing question — whether the pattern the first
two rounds found still holds — it narrowed again and did not close. Both
halves earlier rounds attacked are now sound, forward simulation
included, which was round 2's leftover. The residue moved one layer out
from wherever the last round pointed: date semantics *inside* the one
ledger line, the sweep commands Task 13 orders but the plan never ran,
and the plan's own exemption clause, which its own tasks contradict.
Three rounds, three addresses, one habit — the discipline holds wherever
a previous round looked and slips in the adjacent cell.

**The loop closes here, by the developer's decision of 2026-09-07.** All
six of this round's findings were fixed under the licenses their ledger
lines cite, leaving nothing open or held, and the reviewer's stop signal
judged a fourth round unable to repay itself: this round performed the
whole-document read the loop owed, so no unread text remains for another
round to certify, and what it left behind was six one-sentence repairs.
A plan's loop terminates only on a full-document `LGTM`, which this
round did not give, so the close is the resolution annotation rather
than a terminator — `concerns (resolved 2026-09-07)`, this paragraph
being the body note the lifecycle rule requires.

Scoping never spans a close: any later round on this plan opens a new
loop and reads the whole document again.

### 2026-09-07 — plan-adversary, fable 5, concerns (round 2, diff-scoped)

- fixed 2026-09-07 — [Important] fix 1's restated counts are right for today's tree and wrong for the tree the plan predicts at execution time: this plan's own loop terminates on a diff-scoped LGTM, that heading lands inside a real `## Review rounds` section where the scope leg does not reject it, and the rules that would annotate it ship during this very plan — so the three steps state absolutes that Task 13 Step 4 already contradicts in words; license: the plan's own constraint that a check must state the value it returns, plus Task 13 Step 4's written prediction of this exact ledger state, which makes the correction a recomputation rather than a decision; the three steps now state a fixed base plus one contingent line, each pointing at Task 13 Step 4 for why that line is a real hit discharged there
- fixed 2026-09-07 — [Minor] fix 5's "annotate the heading, citing the confirming round" reads as licensing a path clause inside the token, which Task 3's shipped grammar forbids — the token "carries a date and nothing else" precisely so one fact gets no second home; license: that sentence of Task 3; the instruction now names the bare token and puts the confirming round's heading where it belongs, in the session's derivation rather than in the annotation

The reviewer ran every published before-value against the live tree and
reports them all verifying, which is the property round 1 found missing.
It also declined to refute the recorded deviation on fix 1: truncating
the `Find:` blocks would trade executability for a quiet grep and hide
the case the scope leg exists for.

- signal 2026-09-07 — a dedicated round 3 would not repay itself: the Important's repair is one contingency sentence restated in three steps, self-licensed and verifiable by inspection, and the confirming full-document round this plan is owed regardless can absorb that check

Answering the round's focusing question — whether the fix wave repaired
the habit or only its six instances — the answer narrowed rather than
flipped. Simulation now happens: every restated value verifies against
the live tree, which round 1's did not. But it was run against the
authoring-time tree while the plan itself describes the execution-time
state that breaks three of those counts. So the failure moved from
"never ran the command" to "ran it at the wrong timepoint", and forward
simulation is the half still owed.

### 2026-09-07 — plan-adversary, fable 5, blocking (round 1, full-document)

- fixed 2026-09-07 — [Important] three verification steps publish false expected values, because the plan's own `Find:` blocks instantiate the anchor they verify: the published Chain-debt command returns four lines today, not two; license: the plan's own constraint that a check must return a stated value, plus the recomputation itself, which a recounted counter licenses; the three steps now state four, four-to-three and three-to-two, and each says why the plan's own two lines are output the scope leg rejects rather than hits; deviation: Task 1 Step 5, where the reviewer's alternative of truncating the `Find:` blocks is declined and the reason stated beside the text it concerns
- fixed 2026-09-07 — [Important] Task 11's ledger block carries literal `<date>` placeholders with no substitution instruction, and every check in the task passes with them left in; license: the plan's own constraint that a check whose value cannot distinguish the two states verifies nothing, plus the substitution instruction Step 3 already carries, whose absence in Step 4 was the asymmetry; Step 4 now demands the substitution for both occurrences and Step 1 gains `grep -c '<date>'`, expected `0` after, which is the one value a surviving placeholder changes
- fixed 2026-09-07 — [Minor] Task 5's placement anchor quotes a sentence that straddles a line wrap in the target file, so a single-line search for it returns nothing; license: the plan's own unconditional rule about wrapped prose, which the one task shipping no `Find:` block had escaped; Task 5 now carries a `Find:`/`Replace with:` pair anchored on the real line break plus the `### Gate lines` heading, verified unique and byte-exact
- fixed 2026-09-07 — [Minor] the token counts use single-line `grep -c`, against the plan's own unconditional rule that a prose search puts `\s+` between every pair of words; license: that constraint, which renounces exactly the reasoning that made these harmless — that every occurrence happens to be pinned inside a prescribed block; all seven sites now run `rg -Uc 'debt\s+discharged'` and `rg -Uc 'chain\s+accepted'`, and the four expectation lines they feed are restated for `rg -c` printing nothing where `grep -c` printed `0`
- fixed 2026-09-07 — [Minor] Task 13's expected-clean sweep can trip on this plan's own ledger once its loop closes on a diff-scoped LGTM, and the plan neither predicts the hit nor says which instruction wins; license: Task 3's own text that the annotation's derivation licenses a later session to write it, which settles the conflict without a new decision; Step 4 now names both self-referential classes, discharges the chain-debt hit under that derivation, and separates it from the two quoted blocks the scope leg rejects
- fixed 2026-09-07 — [Minor] the installed rule copies under `.claude/rules/working-process/` consume every changed sentence and no task names them; license: the plan's own consumer-enumeration duty, plus the sync-rules engine owning every Rules-payload write, which is why the repair is a hand-back offer and not a task that edits them; Task 13 Step 7 now reports the drift and offers the run

The reviewer's stop signal is recorded below in the line shape Task 5
ships. Writing it before that task lands dogfoods the shape rather than
minting an undefined one: the live grammar does not yet admit the line,
so until it does this record doubles as narrative prose, which the
section already permits.

- signal 2026-09-07 — one short diff-scoped round over the two Important fixes earns its cost, since the first fix touches `Find:` blocks three tasks depend on; a fresh full-document round would not repay itself, and the four Minors touch neither the design, the token, nor the derivations

Answering the round's focusing question — whether the plan avoided
mistaking the manifest for the proof or merely wrote the warning down —
the reviewer split the verdict, and the split is worth keeping. The
edit-site half held: every `Find:` block byte-matches its target, both
retired-token sites are covered, and Task 13 dispatches the propagation
gate with a derive-your-own-scope brief. The check half did not: the
four-line output behind the first Important was observable at authoring
time by running the plan's own flagship command over two documents the
plan itself edits. So the manifest is not mistaken for the proof — the
expected check outputs are.
