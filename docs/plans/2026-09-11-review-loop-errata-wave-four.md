---
ticket: none
date: 2026-09-11
status: approved
adversary: concerns (resolved 2026-09-14)
spec: ../specs/2026-09-11-review-loop-errata-wave-four.md
branch: feature/process-wave-four
base: develop
---

# Review loop — errata wave four Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land the seven changes of
`docs/specs/2026-09-11-review-loop-errata-wave-four.md` in the
`working-process` plugin and this repo's glossary.

**Architecture:** Every deliverable is prose in a shipped rule, skill,
README or glossary entry. There is no code and no test suite; a task's
test is the grep pair the spec publishes, run before and after the edit.
Tasks are drawn one per file so no two touch the same text, except
`workflow.md`, whose two tasks edit sections that do not overlap.

**Tech Stack:** Markdown rule files distributed as a Claude Code Rules
payload; `grep`, `tr` and `claude plugin validate` for verification.

## Global Constraints

- **The spec is the source.** Where this plan and the spec disagree, the
  spec wins and the plan is wrong — except where *Deviations from the
  spec* below records a departure and its reason.
- **Prose wraps at 72 characters** in every rule, skill and glossary
  file. Match the surrounding paragraph; never reflow a paragraph this
  plan does not change.
- **A check over prose normalizes whitespace first**
  (`tr -s '[:space:]' ' '`), so a phrase matches wherever the line wraps.
  Only a check anchoring something that cannot wrap — a heading, a
  filename, a file count — is written plain, and none anchors a line
  ending.
- **Every step states its before value and its after value**, and an
  invariant says so and says why.
- **The glossary binds.** `docs/domain/glossary.md` terms and `_Avoid_`
  bans govern this text. `Confirming round`, `Round heading`, `Chain
  debt`, `Adjudication`, `Unfinished-work list` and `Disposition ledger`
  are canonical here.
- **Public repo hygiene**: no machine-specific paths, no company or
  client names, all committed text in English.
- **The replacement texts already carry the elements-of-style pass.**
  The repo requires it over changed prose in rules, skills, READMEs and
  the glossary; it was applied to every Replace block at authoring, so
  an implementer copying a block verbatim is complying rather than
  skipping it. A block an implementer rewords leaves that guarantee and
  owes the pass again.
- **Commit messages are one line** — a conventional-commit subject, no
  body, no trailers.
- **Do not run `sync-rules` and do not move the spec's `status`.** Both
  are the developer's, and the spec's *What this wave does not do* says
  so.

## Deviations from the spec

Recorded here and beside the text they concern, so a reviewer trips over
the reason where the disagreement lives.

1. **W3's sentence lands in the section's last paragraph**, the one
   opening "What per-round commits never do is replace the ledger". The
   spec says only "the per-round-commits paragraph" and the integrity
   audit reported the ambiguity (its question 6). That paragraph is the
   section's statement of what the mechanism does not do, which is what
   this sentence says. Task 3 carries the reason.
2. **W7's rule body writes the trigger list as a table**, which the spec
   does not prescribe — it prescribes the keying ("keys the eight duties
   by the edit an author just made") and the citation by duty number. A
   table is the shortest form that keeps trigger, enumeration and duty
   number on one row. Task 6 carries the reason.
3. **The spec disagrees with itself about the glossary, and the plan
   follows its body.** The Scope preamble says two glossary changes are
   already applied and one is owed; W1's body says the **Round heading**
   entry "gains the continuity half too". Measured at authoring: that
   clause is not in the file, so the preamble's count is one short and
   the body is right. Task 4 step 2 writes it and Task 7 sweeps it.
4. **W7's prose never writes the literal `docs/domain/**`.** The spec's
   own check expects exactly one line matching it, and the frontmatter
   entry is that line; a second mention in prose would make the check
   read 2 where the spec says 1. Task 6 says "the domain directory"
   instead.

## File structure

Modified:

- `plugins/working-process/rules/workflow.md` — Task 1 (the plan
  paragraph and the spec's pair-offer arm, inside *What a diff-scoped
  LGTM certifies*) and Task 2 (two Terminators bullets, plus a new
  `## Branch naming` section; the all-Minor qualifier moved into Task 1
  at review round one). The two tasks share the file and touch no common
  line.
- `plugins/working-process/rules/spec-plan-lifecycle.md` — Task 3: the
  Unresolved verdict owner leg, two sentences in *The disposition
  ledger*, the resolution-annotation bullet, and one sentence in the
  per-round-commits section.
- `plugins/working-process/rules/ticket-frontmatter.md` — Task 2: one
  pointer sentence in *Sourcing and backfill*.
- `docs/domain/glossary.md` — Task 4: the **Round heading** entry gains
  a clause; the **Chain debt** entry loses a comma pile.
- `plugins/working-process/skills/process-status/SKILL.md` — Task 5: one
  paragraph in Step 4.
- `plugins/working-process/README.md` — Task 6: the rule count and the
  new rule's name.

Created:

- `plugins/working-process/rules/propagation-duties.md` — Task 6.

## Order and independence

The integrity audit confirmed the seven items may be applied in any
order, with three caveats this plan fixes by its task order:

- Tasks 1 and 2 both edit `workflow.md`; Task 1 runs first so the line
  numbers the spec quotes (`:416`, `:419`, `:421`, `:424`) still hold
  when it reads them. Task 2 inserts a heading above those lines, which
  is why it runs second. Every check anchors text rather than a line, so
  the order is a convenience, not a dependency.
- Task 2's cap sentence assumes decision 1's semantics, which Task 1
  lands. Task 1 also carries the all-Minor qualifier, which review round
  one moved there from Task 2: without it, Task 1's own commit would
  leave `workflow.md` saying both that the annotation waits for the
  confirming round and that it records the developer's close.
- `claude plugin validate` runs once, at Task 7, after every file has
  changed; validation before then proves nothing about the end state.
  `sync-rules` never runs in this plan — the Global Constraints forbid
  it and the spec puts it outside the wave.

---

### Task 1: `workflow.md` — a plan's loop closes on a full-document round

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the section
  `### What a diff-scoped LGTM certifies`, its spec paragraph and its
  plan paragraph.

**Interfaces:**
- Produces: the phrases later tasks and checks depend on — `latest
  verdict round was full-document`, `inherits the gating of whatever
  ended`, and the preserved `at the document's next touch`.
- Consumes: nothing from earlier tasks.

- [ ] **Step 1: Record the before values**

Run from the repository root:

```bash
W=plugins/working-process/rules/workflow.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $W | grep -o 'never terminates on a diff-scoped LGTM' | wc -l)"
echo "B $(n $W | grep -o 'latest verdict round was full-document' | wc -l)"
echo "C $(n $W | grep -o 'inherits the gating of whatever ended' | wc -l)"
echo "D $(n $W | grep -o 'runs under the loop.s standing consent like any other' | wc -l)"
echo "E $(n $W | grep -o 'at the document.s next touch' | wc -l)"
echo "F $(n $W | grep -o 'or a confirming full-document round' | wc -l)"
echo "G $(n $W | grep -o 'confirming round alone' | wc -l)"
echo "H $(n $W | grep -o 'a confirming round on a spec' | wc -l)"
echo "I $(n $W | grep -o 'The confirming-round arm' | wc -l)"
echo "J $(n $W | grep -o 'records their close, and no session' | wc -l)"
echo "K $(n $W | grep -o 'on a plan, once the confirming round has run' | wc -l)"
```

Expected: `A 1`, `B 0`, `C 0`, `D 1`, `E 1`, `F 1`, `G 1`, `H 1`, `I 1`,
`J 1`, `K 0`.

If any differs, stop and report: the file is not the one this task was
written against.

- [ ] **Step 2: Replace the spec's pair-offer paragraph**

Find this paragraph and replace it whole. It renames the spec's arm from
"confirming round" to "a full-document round" in all four of its
sentences, so the term **Confirming round** names one object — the
plan's obligation — and nothing else.

Find:

```
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
```

Replace with:

```
For a spec, the consumption gate before plan-writing offers the pair as
one question — an integrity audit or a full-document round — and never
an offer followed by a re-offer of the option just declined. When the
`integrity-auditor` agent is absent the offer carries the full-document
round alone. The two arms cost differently and the offer says so: an
audit returns material for the dispatcher to dispose of and leaves the
verdict alone, while a full-document round on a spec is a new loop's
first round, since the spec's LGTM already closed its loop — it mints
its own verdict and stamps it, so a `concerns` there flips the field
back while plan-writing waits. The full-document-round arm therefore
blocks plan-writing; the audit arm does not, and plan-writing follows
its dispositions.
```

- [ ] **Step 3: Replace the plan paragraph**

Find this paragraph and replace it with three. The first generalizes the
trigger and states the gating; the second says who decides that the
rounds are ending; the third keeps the relay-then-stamp exception and
splits recovery by verdict.

Find:

```
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

Replace with:

```
For a plan the loop closes only when the latest verdict round was
full-document: whatever ends its rounds while the latest round heading
is diff-scoped, one confirming full-document round follows, and that
round's verdict is the one stamped. A round already full-document owes
no successor — it is the close. The confirming round inherits the gating
of whatever ended the rounds. Where autonomy still stands —
a diff-scoped `LGTM`, or a `concerns` inside the cap — the rules mandate
the round, so it is no decision of the developer's and spends none of
the round's one interruption. After `blocking`, the round cap or the
all-Minor signal it is the developer's to order, because each of those
suspends autonomy by its own terminator, and a round the rules mandate
cannot outrank a terminator that stopped the loop.

A session never judges that the rounds are ending. The terminators do,
as does the developer closing the loop. While none has fired and the
held set is empty, the next round is diff-scoped and the loop simply
continues; the confirming round is owed the moment one fires, which is
the moment a session would otherwise write the resolution annotation.

The plan case carries the single named exception to the relay-then-stamp
order above — a plan's diff-scoped LGTM is relayed and its round record
written, and only the frontmatter stamp waits for the confirming round.
Recovery therefore reads the ledger rather than the stamp. A plan whose
latest round heading is a diff-scoped `LGTM` that no later full-document
round follows is re-offered its confirming round at the document's next
touch, whatever the frontmatter says, since that heading is itself an
end. A latest heading of any other verdict is not an end, so there the
round is re-offered when something tries to end the rounds — an
annotation, an adjudication, a `status` move — or when a terminator that
suspends autonomy has fired.
```

- [ ] **Step 4: Qualify the all-Minor bullet**

This lands here rather than in Task 2 so that no commit leaves the rule
saying two things: Step 3 writes that the annotation waits for the
confirming round, and until this edit the all-Minor bullet still says the
annotation records the developer's close.

Find:

```
  until the developer answers it: the resolution annotation the
  spec-plan-lifecycle rule defines records their close, and no session
  writes it without their answer.
```

Replace with:

```
  until the developer answers it: the resolution annotation the
  spec-plan-lifecycle rule defines records their close — on a plan, once
  the confirming round has run — and no session writes it without their
  answer.
```

- [ ] **Step 5: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 1`, `C 1`, `D 0`, `E 1`, `F 0`, `G 0`, `H 0`, `I 0`,
`J 0`, `K 1`.

`E` is the declared invariant: the phrase survives because the `LGTM`
heading keeps it.

- [ ] **Step 6: Check the neighbours the rename must not touch**

The words "confirming round" stay wherever they name the plan's
obligation. Run:

```bash
grep -n 'confirming' plugins/working-process/rules/workflow.md
```

Expected: matches remain at the verdict-agent dispatch bullet ("waits
for the confirming round"), in the Round cap bullet (two), in the
all-Minor bullet Step 4 qualified, and in the paragraphs Step 3 wrote.
No match remains in the spec's pair-offer paragraph.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): close a plan's loop only on a full-document round"
```

---

### Task 2: `workflow.md` terminators and branch naming

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the `Round cap`
  bullet of `### Terminators`, and a new `## Branch naming` section. The
  `All-Minor signal` bullet belongs to Task 1 step 4.
- Modify: `plugins/working-process/rules/ticket-frontmatter.md` — one
  sentence in `## Sourcing and backfill`.

**Interfaces:**
- Consumes: Task 1's plan paragraph, whose semantics the cap sentence
  assumes.
- Produces: the `## Branch naming` heading that the ticket rule's
  pointer names.

- [ ] **Step 1: Record the before values**

```bash
W=plugins/working-process/rules/workflow.md
T=plugins/working-process/rules/ticket-frontmatter.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $W | grep -o 'unbounded by the cap' | wc -l)"
echo "D $(grep -c '^## Branch naming' $W)"
echo "E $(grep -c '^## Branch naming' $T)"
echo "F $(n $T | grep -o 'branch naming convention' | wc -l)"
```

Expected: `A 0`, `D 0`, `E 0`, `F 0`. The all-Minor qualifier that used
to sit in this task moved to Task 1 step 4, so that no commit leaves the
rule self-contradicting; its two checks moved with it.

- [ ] **Step 2: Extend the Round cap bullet**

Find:

```
  therefore escalates once before its confirming round, which is the
  most expensive shape a round takes and the one a cap guarding spend
  should guard first.
```

Replace with:

```
  therefore escalates once before its confirming round, which is the
  most expensive shape a round takes and the one a cap guarding spend
  should guard first. A run of `blocking` verdicts is unbounded by the
  cap, for the reason the cap is stated in: it counts autonomous rounds,
  and `blocking` suspends autonomy, so every continuation after one is
  the developer's own decision rather than a round the cap governs.
  Consenting to three rounds consents to three autonomous ones.
```

- [ ] **Step 3: Add the Branch naming section**

The words `## Dispatching a verdict agent` occur twice in this file —
once as the heading, and once inside backticks in the closing paragraph
of the section it names. Anchor on the pair below, which is unique.

Find:

```
The pass binds wording, never decisions. Without the skill there is no
substitute pass and no install nagging — the work proceeds normally.

## Dispatching a verdict agent
```

Replace with:

```
The pass binds wording, never decisions. Without the skill there is no
substitute pass and no install nagging — the work proceeds normally.

## Branch naming

Feature work happens on a topic branch named
`feature/<ticket>-<short-name>`, where `<ticket>` is the work's tracker
reference and `<short-name>` says what the work is, and
`feature/<short-name>` where there is no ticket. How a tracker's
reference is spelled in a branch name is the project's own — this
convention fixes the shape and not the spelling.

The branch of a worktree created with a generated name is renamed to
this shape before its first commit, so the branch a reader sees is the
branch the convention names; the worktree's own directory is a separate
name and this convention does not govern it. The work's spec and plan
record the result in their `branch:` field — the topic branch, not the
`<topic>.docs` branch a review loop's per-round commits use, which the
spec-plan-lifecycle rule names and which is a sibling of it rather than
a second topic branch. The ticket rule's sourcing order reads the
current branch name first when a new document needs a ticket.

## Dispatching a verdict agent
```

- [ ] **Step 4: Point the ticket rule at it**

In `ticket-frontmatter.md`, `## Sourcing and backfill`, find:

```
For a NEW document: branch name (`feature/ABC-123-...`) → conversation
context → ask the developer once; no answer means `none`. Never ask twice
for one unit of work — a plan inherits its spec's ticket, and artifacts
of the same session reuse the established value.
```

Replace with:

```
For a NEW document: branch name (`feature/ABC-123-...`) → conversation
context → ask the developer once; no answer means `none`. Never ask twice
for one unit of work — a plan inherits its spec's ticket, and artifacts
of the same session reuse the established value. The branch naming
convention that produces the names this order reads is the workflow
rule's, which is where a branch is cut — before any `docs/` file of that
work exists, and so before this rule loads. Where a branch name yields
no usable reference, the order above simply falls through to its next
source, as it does for any work whose branch carries none.
```

- [ ] **Step 5: Verify**

Run the Step 1 command again.

Expected: `A 1`, `D 1`, `E 0`, `F 1`.

`E` is the declared invariant: the section belongs to the workflow rule
and must never appear in the ticket rule.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/workflow.md plugins/working-process/rules/ticket-frontmatter.md
git commit -m "feat(working-process): bound the cap's promise and publish the branch-naming convention"
```

---

### Task 3: `spec-plan-lifecycle.md` — owner leg, ordinals, annotation, sha

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the
  Unresolved verdict owner leg in `## Unfinished-work list`; two
  sentences in `## The disposition ledger`; the resolution-annotation
  bullet near the top; one sentence in the per-round-commits section.

**Interfaces:**
- Consumes: Task 1's semantics — the owner leg and the annotation clause
  both state what Task 1's paragraph decided.
- Produces: nothing later tasks read.

- [ ] **Step 1: Record the before values**

```bash
L=plugins/working-process/rules/spec-plan-lifecycle.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $L | grep -o 'except on a plan whose latest round heading is a diff-scoped' | wc -l)"
echo "B $(n $L | grep -o 'highest ordinal' | wc -l)"
echo "C $(n $L | grep -o 'continue across loops' | wc -l)"
echo "D $(n $L | grep -o 'where that heading is an .LGTM.' | wc -l)"
echo "E $(n $L | grep -o 'wait for the confirming round' | wc -l)"
echo "F $(n $L | grep -o 'never stands in for the' | wc -l)"
echo "G $(n $L | grep -o 'feature/<ticket>-<short-name>/docs' | wc -l)"
```

Expected: `A 1`, `B 0`, `C 0`, `D 0`, `E 0`, `F 0`, `G 0`.

- [ ] **Step 2: Widen the Unresolved verdict owner leg**

Find:

```
  Owner: a fresh round at the prescribed tier, or the resolution
  annotation above — except on a plan whose latest round heading is a
  diff-scoped `LGTM`, where the confirming full-document round closes
  the verdict and the annotation may not, since a plan's loop never
  terminates on that heading. Such a plan matches Chain debt as well:
  one debt seen from two sides, both extinguished by that round, and the
  duplicate is deliberate.
```

Replace with:

```
  Owner: a fresh round at the prescribed tier, or the resolution
  annotation above — except on a plan whose latest round heading is
  diff-scoped, whatever its verdict, where the confirming full-document
  round closes the verdict and the annotation may not, since a plan's
  loop closes only on a full-document round. Such a plan matches Chain
  debt as well where that heading is an `LGTM`: one debt seen from two
  sides, both extinguished by that round, and the duplicate is
  deliberate. On a plan already at `status: implemented` the round is
  discharged by recorded decline without any dispatch, as the Chain debt
  leg discharges its own debt — a session derives that decline under a
  `concerns` heading, while a `blocking` one waits for the developer's
  adjudication, which is theirs to make.
```

The narrowing to `LGTM` rides with the widening because the Chain debt
command keys on `LGTM`: a diff-scoped `concerns` heading produces no
second hit, so the unnarrowed sentence would be false for exactly the
case this edit adds.

- [ ] **Step 3: Define the latest heading and the ordinals**

In `## The disposition ledger`, find this paragraph — the insertion goes
after it, so the replacement repeats it and adds the new one:

```
The scope token admits two values, `diff-scoped` and `full-document`,
and is omitted only on a round predating the distinction. A recovery
reading keys on the absence of `full-document`, so a full-document round
always says so.
```

Replace with:

```
The scope token admits two values, `diff-scoped` and `full-document`,
and is omitted only on a round predating the distinction. A recovery
reading keys on the absence of `full-document`, so a full-document round
always says so.

The latest round heading is the one carrying the highest ordinal,
wherever it sits in the section: no order is prescribed for the blocks
and live ledgers run both ways. Ordinals run per document and per field,
and continue across loops — a later loop opens at the next number rather
than at one, which is what the round cap's derivation from the headings
already assumed.
```

- [ ] **Step 4: Give the annotation bullet its plan clause**

Find:

```
  its own token — `architect: blocking (adjudicated 2026-08-17)` — and
  the round's ledger record as that body note.
```

Replace with:

```
  its own token — `architect: blocking (adjudicated 2026-08-17)` — and
  the round's ledger record as that body note. On a plan both wait for
  the confirming round: neither is written while the latest round
  heading is diff-scoped, unless the plan is already `implemented`,
  where the annotation — or the developer's adjudication — is written
  citing that standing decision. Its body note is written too: a note
  recording what resolved a verdict is a process record, which the
  implemented-document rule above excepts from its frontmatter-only
  clause, as it excepts `, debt discharged <date>`.
```

- [ ] **Step 5: Match the document-branch placeholder to the convention**

W6 mints `feature/<ticket>-<short-name>` for the topic branch, and this
rule writes the same slot as `feature/<issue>-<name>` inside its
document-branch paragraph. Two rules of one payload naming one slot
differently is the changed-interface class the wave's own new rule tells
an author to enumerate, so the older spelling joins the newer.

Find:

```
so `feature/<issue>-<name>/docs` cannot exist while its parent does; the
```

Replace with:

```
so `feature/<ticket>-<short-name>/docs` cannot exist while its parent
does; the
```

- [ ] **Step 6: Part the round sha from the integrity hash**

In the per-round-commits section, find the final paragraph:

```
What per-round commits never do is replace the ledger. Git says which
lines changed; the ledger says with what intent and on whose license,
and a diff carries neither "narrowed the claim" nor a cited ADR. A
`<what changed>` clause may thin to a sentence where the commit carries
the detail; it does not go.
```

Replace with:

```
What per-round commits never do is replace the ledger. Git says which
lines changed; the ledger says with what intent and on whose license,
and a diff carries neither "narrowed the claim" nor a cited ADR. A
`<what changed>` clause may thin to a sentence where the commit carries
the detail; it does not go. Nor does a sha stand in for a hash: a round
heading that one day carried its commit's sha would name that round,
and it never stands in for the `integrity:` hash, which is computed from
the body and must work on a document nobody committed — the default
path, where no sha exists.
```

This paragraph is the section's statement of what the mechanism does not
do, which is what the sentence says; the spec named only "the
per-round-commits paragraph", and the integrity audit reported that
ambiguity (deviation 1).

- [ ] **Step 7: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 1`, `C 1`, `D 1`, `E 1`, `F 1`, `G 1`.

- [ ] **Step 8: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): widen the plan exception, define the latest heading, part sha from hash"
```

---

### Task 4: the glossary — ordinal continuity and the Chain debt seam

**Files:**
- Modify: `docs/domain/glossary.md` — the **Round heading** entry and
  the **Chain debt** entry.

**Interfaces:**
- Consumes: Task 3's ordinal sentences, which this entry restates in the
  term's own voice.
- Produces: nothing later tasks read.

- [ ] **Step 1: Record the before values**

```bash
G=docs/domain/glossary.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^\*\*Confirming round\*\*:' $G)"
echo "B $(n $G | grep -o 'inherits the gating' | wc -l)"
echo "C $(n $G | grep -o 'A plan already .implemented. owes none' | wc -l)"
echo "D $(grep -c 'decline — of the gate' $G)"
echo "E $(n $G | grep -o 'continue across loops' | wc -l)"
```

Expected: `A 1`, `B 1`, `C 1`, `D 1`, `E 0`.

`A`, `B` and `C` are declared invariants: the **Confirming round** entry
was minted at the grilling and amended by review rounds one and two, so
it already stands in the file and this task must not disturb it.

- [ ] **Step 2: Give Round heading the continuity clause**

Find:

```
diff-scoped chain — is read by folding these. The latest round heading
is the one carrying the highest ordinal, wherever it sits in the
section: the rules prescribe no order for the blocks, and live ledgers
run both ways.
```

Replace with:

```
diff-scoped chain — is read by folding these. The latest round heading
is the one carrying the highest ordinal, wherever it sits in the
section: the rules prescribe no order for the blocks, and live ledgers
run both ways. Ordinals run per document and per field, and continue
across loops rather than restarting.
```

- [ ] **Step 3: Undo the Chain debt comma pile**

Find:

```
once it terminates. Discharged three ways: an integrity audit, any later
full-document round whatever its verdict, or the developer's recorded
decline — of the gate's pair offer, or, where the document is already
implemented and the gate never fired, of the question that offer would
have put.
```

Replace with:

```
once it terminates. Discharged three ways: an integrity audit, any later
full-document round whatever its verdict, or the developer's recorded
decline. What they decline is the gate's pair offer — or, where the
document is already implemented and the gate never fired, the question
that offer would have put.
```

The term's meaning does not move; only the punctuation does.

- [ ] **Step 4: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 1`, `D 0`, `E 1`.

- [ ] **Step 5: Commit**

```bash
git add docs/domain/glossary.md
git commit -m "docs(glossary): carry ordinal continuity and clear the Chain debt comma pile"
```

---

### Task 5: `process-status` reports two hits on one document

**Files:**
- Modify:
  `plugins/working-process/skills/process-status/SKILL.md` — one
  paragraph in `## Step 4 — report`, after the Misplaced stamp
  paragraph.

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: nothing later tasks read.

- [ ] **Step 1: Record the before values**

```bash
S=plugins/working-process/skills/process-status/SKILL.md
echo "A $(tr -s '[:space:]' ' ' < $S | grep -o 'two confirmed hits share one document' | wc -l)"
echo "B $(grep -c 'Unresolved verdict and Chain debt' $S)"
```

Expected: `A 0`, `B 0`.

`B` is a declared invariant at zero: the line is written as a shape, and
naming the pair of classes would give the relationship a second home and
make this skill carry process knowledge it declares it has none of.

- [ ] **Step 2: Add the paragraph**

Find the end of the Misplaced stamp paragraph — the two lines below are
unique in the file:

```
published later works the same way. Name the field on the line, so the
developer can see which class went quiet.
```

Replace with:

```
published later works the same way. Name the field on the line, so the
developer can see which class went quiet.

Where two confirmed hits share one document, add one line beneath that
document's per-hit lines, naming the classes and pointing at their owner
legs:

    - two classes hit this document; one move may close both — see their owner legs

The line is the mapping read back — two hits, one file — and nothing
more: it does not say the duplicate is deliberate, and it does not
explain how the two relate, because both are process knowledge and this
skill carries none. A reader who wants the relationship finds it in the
legs the line points at.
```

- [ ] **Step 3: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 0`.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/skills/process-status/SKILL.md
git commit -m "feat(working-process): report two hits on one document as a shape"
```

---

### Task 6: the propagation duties as an author-facing rule

**Files:**
- Create: `plugins/working-process/rules/propagation-duties.md`
- Modify: `plugins/working-process/README.md` — the `## Process rules`
  paragraph.

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: a sixth file in `rules/`, which Task 7's file count reads.

- [ ] **Step 1: Record the before values**

```bash
echo "A $(ls plugins/working-process/rules/*.md | wc -l)"
echo "B $(grep -c 'six rule files' plugins/working-process/README.md)"
echo "C $(grep -c 'five rule files' plugins/working-process/README.md)"
```

Expected: `A 5`, `B 0`, `C 1`.

- [ ] **Step 2: Create the rule file**

Write `plugins/working-process/rules/propagation-duties.md` with exactly
this content:

````markdown
---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
  - "docs/domain/**"
---

# Propagation duties — the author's checklist

Before a document goes to an expensive reader, eight duties fall due,
keyed by the nine edits that trigger them — one duty answers two
different edits. This rule lists them by the edit an author has just
made, so the enumeration can be done at the desk instead of paid
for at the gate. The list below is complete as it stands and needs
nothing else to be usable.

When the `propagation-auditor` agent is available it walks the same
eight as a gate, and its card is their definition and keeps the
measurement behind each; the numbers in the last column are that card's,
so a hit it reports can be read back to the row that would have caught
it. Without the agent the rows still hold — what is lost is the second
pair of eyes, not the duties.

| You have just… | Enumerate | Duty |
|---|---|---|
| changed an interface — a signature, a name, a heading, an anchor, a field | every consumer, by parsing the structure that defines them, never by text match | 1 |
| prescribed a verbatim block | the anchor it targets — the text it replaces must exist in that file byte-exactly, and once | 2 |
| reported a change already made | that block against the shipped file, both ways: one that never landed, and shipped text a block no longer matches | 2 |
| added a field, label or state | both ends of its chain — what writes it, and what reads it | 3 |
| asserted a count | the count itself, re-derived from what the tool prints or what the list holds | 4 |
| used a name your source does not define | the source's own names; an invented name is a gap in the source rather than an error in yours | 5 |
| reported another document's state | that sentence, against that document | 6 |
| written a verification command | the command, run against your own replacement text | 7 |
| copied a citation out of a review report | the file and line it names, read at the source | 8 |

Two of these fire where an author does not expect them. A newly minted
glossary `_Avoid_` ban is a changed interface, so duty 1 reaches every
shipped occurrence of the banned term — which is why this rule loads at
the domain directory as well as at specs and plans. And a count asserted
about another document is duties 4 and 6 at once: re-derive it, then
read it back at its source.

Self-checking never replaces a gate where one runs. A fresh context
finds what an author's eye has stopped seeing; what this buys is a
shorter list for it to find, which is what makes the round after it
cheaper.
````

- [ ] **Step 3: Update the README**

Find:

```
The plugin ships five rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, ticket frontmatter, and the review-report
contract (`review-reports.md`: where a code-review run writes its
Review report and what shape it takes; domain review skills locate the
installed contract via its contract probe — the project-level then
user-level install path, in that order). Claude Code
does not load plugin rules by itself: install them with the
`working-process:sync-rules` skill.
```

Replace with:

```
The plugin ships six rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, ticket frontmatter, the propagation
duties keyed by the edit that triggers them (`propagation-duties.md`,
loaded while a spec, plan or domain document is open), and the
review-report contract (`review-reports.md`: where a code-review run
writes its Review report and what shape it takes; domain review skills
locate the installed contract via its contract probe — the
project-level then user-level install path, in that order). Claude Code
does not load plugin rules by itself: install them with the
`working-process:sync-rules` skill.
```

- [ ] **Step 4: Verify**

Run the Step 1 command again, plus the rule's own scope check:

```bash
echo "D $(grep -c 'docs/domain/\*\*' plugins/working-process/rules/propagation-duties.md)"
```

Expected: `A 6`, `B 1`, `C 0`, `D 1`.

`D` is 1 because the frontmatter entry is the only line carrying that
literal; the prose says "the domain directory" for exactly that reason
(deviation 3).

- [ ] **Step 5: Read the new frontmatter back**

`claude plugin validate` does not check `rules/` — a rule file is not a
plugin component — so an unquoted `: ` in a scalar fails silently at
load time and nothing in Task 7 would catch it. Read the block back and
compare it:

The check compares the written block against the prescribed one
literally. It uses no YAML parser: `python3 -c 'import yaml'` fails on
this host, and a plan must not make its only guard depend on a package
nobody declared.

```bash
diff <(sed -n '1,6p' plugins/working-process/rules/propagation-duties.md) - <<'EOF'
---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
  - "docs/domain/**"
---
EOF
```

Expected: no output and exit status 0. Any output is the diff between
what was written and what the plan prescribes; fix the file, not the
check.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/propagation-duties.md plugins/working-process/README.md
git commit -m "feat(working-process): ship the propagation duties as an author-facing rule"
```

---

### Task 7: end-state sweep

**Files:**
- Modify: none. This task only verifies and reports.

**Interfaces:**
- Consumes: every preceding task's deliverable.
- Produces: the report the developer reads before deciding what follows.

- [ ] **Step 1: Run every check the spec publishes**

```bash
cd "$(git rev-parse --show-toplevel)"
W=plugins/working-process/rules/workflow.md
L=plugins/working-process/rules/spec-plan-lifecycle.md
T=plugins/working-process/rules/ticket-frontmatter.md
S=plugins/working-process/skills/process-status/SKILL.md
G=docs/domain/glossary.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "W1a  $(n $W | grep -o 'never terminates on a diff-scoped LGTM' | wc -l)  want 0"
echo "W1b  $(n $W | grep -o 'latest verdict round was full-document' | wc -l)  want 1"
echo "W1c  $(n $W | grep -o 'inherits the gating of whatever ended' | wc -l)  want 1"
echo "W1d  $(n $W | grep -o 'runs under the loop.s standing consent like any other' | wc -l)  want 0"
echo "W1e  $(n $W | grep -o 'at the document.s next touch' | wc -l)  want 1 (invariant)"
echo "W1f  $(n $W | grep -o 'or a confirming full-document round' | wc -l)  want 0"
echo "W1g  $(n $W | grep -o 'confirming round alone' | wc -l)  want 0"
echo "W1h  $(n $W | grep -o 'a confirming round on a spec' | wc -l)  want 0"
echo "W1i  $(n $W | grep -o 'The confirming-round arm' | wc -l)  want 0"
echo "W1j  $(n $L | grep -o 'except on a plan whose latest round heading is a diff-scoped' | wc -l)  want 0"
echo "W1k  $(n $L | grep -o 'highest ordinal' | wc -l)  want 1"
echo "W1l  $(n $L | grep -o 'continue across loops' | wc -l)  want 1"
echo "W1m  $(n $L | grep -o 'where that heading is an .LGTM.' | wc -l)  want 1"
echo "W1n  $(n $L | grep -o 'wait for the confirming round' | wc -l)  want 1"
echo "W1o  $(grep -c '^\*\*Confirming round\*\*:' $G)  want 1 (invariant)"
echo "W1p  $(n $G | grep -o 'inherits the gating' | wc -l)  want 1 (invariant)"
echo "W1q  $(n $G | grep -o 'A plan already .implemented. owes none' | wc -l)  want 1 (invariant)"
echo "W1r  $(n $G | grep -o 'continue across loops' | wc -l)  want 1"
echo "W2a  $(n $W | grep -o 'unbounded by the cap' | wc -l)  want 1"
echo "W2b  $(n $W | grep -o 'records their close, and no session' | wc -l)  want 0"
echo "W2c  $(n $W | grep -o 'on a plan, once the confirming round has run' | wc -l)  want 1"
echo "W3   $(n $L | grep -o 'never stands in for the' | wc -l)  want 1"
echo "W4a  $(n $S | grep -o 'two confirmed hits share one document' | wc -l)  want 1"
echo "W4b  $(grep -c 'Unresolved verdict and Chain debt' $S)  want 0 (invariant)"
echo "W5   $(grep -c 'decline — of the gate' $G)  want 0"
echo "W6a  $(grep -c '^## Branch naming' $W)  want 1"
echo "W6b  $(grep -c '^## Branch naming' $T)  want 0 (invariant)"
echo "W6c  $(n $T | grep -o 'branch naming convention' | wc -l)  want 1"
echo "W7a  $(ls plugins/working-process/rules/*.md | wc -l)  want 6"
echo "W7b  $(grep -c 'docs/domain/\*\*' plugins/working-process/rules/propagation-duties.md)  want 1"
echo "W7c  $(grep -c 'six rule files' plugins/working-process/README.md)  want 1"
```

Expected: every line's value equals its `want`. Report any that does
not, with the file and the phrase.

- [ ] **Step 2: Validate the plugin and the marketplace**

```bash
claude plugin validate plugins/working-process && claude plugin validate .
```

Expected: both pass. This is the declared invariant `W7d` — they passed
before the wave, and a wave that only adds a rule file must not be what
breaks them. What it does not cover is the rule file itself: `validate`
reads plugin components, and `rules/` is not one, so the new file's
frontmatter is checked by Task 6 step 5 and by nothing here.

- [ ] **Step 3: Confirm the payload changed, and say what that does not mean**

```bash
echo "repo     $(plugins/working-process/scripts/ruleset-hash.sh plugins/working-process/rules)"
CACHE=$(claude plugin list --json | python3 -c 'import json,sys; print(next(p["installPath"] for p in json.load(sys.stdin) if p["id"]=="working-process@missing-bits"))')
echo "cache    $(plugins/working-process/scripts/ruleset-hash.sh "$CACHE/rules")"
echo "manifest $(grep -o '"rulesetHash": "[^"]*"' ~/.claude/rules/working-process/.manifest.json)"
```

Expected: `repo` differs from `cache`, and `cache` still equals
`manifest`.

Read that result carefully, because the obvious reading is wrong. The
difference proves the payload changed **in this checkout**. It is not
drift any installed copy can see: the drift hook hashes
`$CLAUDE_PLUGIN_ROOT/rules`, and `sync-rules` discovers its source from
the `installPath` that `claude plugin list` reports — both of which are
the installed plugin cache, not this working tree. The cache stays at
its released version until a release or a `-dev` dogfood install puts
this branch there. So `sync-rules` run today would report no drift and
would re-copy the old rules, and the developer would keep running the
process under them while believing this wave was installed.

- [ ] **Step 4: Confirm the wrap width did not worsen**

The constraint is "match the surrounding paragraph", not a hard column:
every one of these files already carries long lines this wave does not
touch, and `docs/domain/glossary.md` gained one more from the wave's own
authoring before implementation began. So the check compares against
stated counts rather than against a git baseline, which would move under
it.

Both `awk` calls are pinned to a UTF-8 locale. `length` counts bytes
under `LC_ALL=C`, and these files are full of em dashes, so the same
command reports 19 for `workflow.md` instead of 3 — the six stated
numbers are character counts and only hold as such.

```bash
while read -r f want; do
  now=$(LC_ALL=C.UTF-8 awk 'length > 72 && $0 !~ /^\|/' "$f" | wc -l)
  printf '%-58s was %-3s now %s\n' "$f" "$want" "$now"
done <<'EOF'
plugins/working-process/rules/workflow.md 3
plugins/working-process/rules/spec-plan-lifecycle.md 36
plugins/working-process/rules/ticket-frontmatter.md 1
plugins/working-process/skills/process-status/SKILL.md 3
docs/domain/glossary.md 50
plugins/working-process/README.md 7
EOF
LC_ALL=C.UTF-8 awk 'length > 72 && $0 !~ /^\|/' plugins/working-process/rules/propagation-duties.md | wc -l
```

The loop reads its pairs rather than splitting a string: `set -- $pair`
would work in bash and silently fail in zsh, which does not word-split
an unquoted parameter, and this repo's sessions run zsh.

Expected: `now` equals `was` for all six — the replacement texts are
wrapped, so none of them adds a long line — and `0` for the new rule
file, whose table rows the `awk` skips.

On a count that grew, rewrap the offending paragraph in the file that
owns it and commit it as `style(working-process): rewrap <file>`. Do not
reflow a paragraph this wave did not change.

- [ ] **Step 5: Report the end state**

State to the developer: seven changes landed across six files, one file
created, every published check at its expected value, and
`claude plugin validate` passing for the plugin and the marketplace.
Then state the delivery gap in its own sentence: this branch's rules are
not the rules any session is running, and will not be until the plugin
cache carries this branch: either through a release, or through a
prerelease install whose version convention the repo's plugin-versioning
rule defines and whose install procedure is the developer's own. Neither
the drift hook nor `sync-rules` will announce that, because both read
the cache. Name the two things this plan deliberately
left undone — the install, and moving the spec's `status` to
`implemented` — and that both are theirs.

Do not commit in this task; there is nothing to commit.

## Self-review

**Spec coverage.** W1 → Tasks 1, 3 and 4 (its `workflow.md`,
`spec-plan-lifecycle.md` and glossary halves). W2 → Task 2. W3 → Task 3
step 5. W4 → Task 5. W5 → Task 4 step 3. W6 → Task 2 steps 3 and 4.
W7 → Task 6. Every check in the spec's Verification section appears in
Task 7 step 1, and each also appears in the before/after pair of the
task that produces it. The spec's three exclusions produce no task by
design, and Task 7 step 3 turns one of them — the owed install — into a
statement of what is and is not delivered rather than silence.

**Placeholder scan.** No step says TBD, "handle appropriately", or
"similar to Task N"; every edit carries its find text and its
replacement text in full.

**Consistency.** The phrases the checks anchor are the phrases the
replacement texts contain, verified by reading each replacement against
its check: `latest verdict round was full-document` (Task 1 step 3),
`inherits the gating of whatever ended` (same), `unbounded by the cap`
(Task 2 step 2), `on a plan, once the confirming round has run` (Task 1
step 4), `highest ordinal` and `continue across loops` (Task 3 step 3
and Task 4 step 2), `where that heading is an LGTM` (Task 3 step 2),
`wait for the confirming round` (Task 3 step 4), `never stands in for
the` (Task 3 step 5), `two confirmed hits share one document` (Task 5
step 2), `branch naming convention` (Task 2 step 4), `six rule files`
(Task 6 step 3).

Every step reference above was re-derived after round one moved the
all-Minor qualifier into Task 1 and renumbered two tasks; three were
stale and are corrected here.

## Review rounds

### 2026-09-11 — plan-adversary, fable 5.1, blocking (round 1, full-document)

The propagation gate returned `CLEAN` beforehand, so this round wrote no
gate lines. Every citation was checked before anything was written here,
the drift-hook and sync-rules source paths included — the finding that
cost this plan its most confident sentence.

- fixed 2026-09-11 — [Important] the new plan paragraph dropped decision 1's "unless the latest verdict round already was full-document" clause, reading as an unconditional obligation — a plan closed by a full-document round would owe another one; license: decision 1's own text and the glossary's **Confirming round** entry, which conditions the obligation on a diff-scoped latest heading; the sentence now carries "while the latest round heading is diff-scoped" and says outright that a full-document round is the close
- fixed 2026-09-11 — [Important] Task 7 told the developer the repo-versus-manifest hash difference was "the drift the developer clears by running `sync-rules`", while both the drift hook and that skill read their source from the installed plugin cache rather than this checkout — so the command would report no drift, re-copy the old rules, and leave the developer running the process under them while believing the wave was installed; license: `check-rules-drift.sh`, which hashes `$CLAUDE_PLUGIN_ROOT/rules`, and the sync-rules skill's step 0, which discovers its source from `installPath`; the step now compares three hashes, states that the difference proves only that the payload changed here, and names what actually delivers it — a release or a `-dev` dogfood install
- fixed 2026-09-11 — [Important] the new rule named the `propagation-auditor` agent unconditionally and pointed at "the agent's card" as its definition, where committed project-level rules load for readers without the plugin; license: `.claude/rules/plugin-authoring.md`, which requires agent mentions in rule text to be conditional; the rule now states the eight classes as its own complete list and makes the agent, its card and the duty numbers a conditional second paragraph
- fixed 2026-09-11 — [Important] the branch convention minted a name shape the ticket rule must decode — a bare leading number — while only one end of that chain was written: nothing said how the number reads back, nor that an `org/repo#123` reference cannot survive a branch name; license: the ticket rule's own sourcing order and its requirement that a `#`-leading value be quoted, plus the new rule's duty-3 row demanding both ends of a chain; the pointer now states all three read-backs
- fixed 2026-09-11 — [Minor] the plan claimed Task 1 "keeps the rule self-consistent at every commit" while Task 1's own commit would leave `workflow.md` saying both that the annotation waits for the confirming round and that it records the developer's close, the repair landing only in Task 2; license: the spec's sentence that W1 makes that bullet untrue on a plan; the qualifier and its two checks moved into Task 1 as step 4, and the order section says why
- fixed 2026-09-11 — [Minor] the annotation bullet's implemented-plan exception freed only "the annotation" while the owner leg written in the same task has a `blocking` heading waiting for the developer's adjudication — read literally the bullet forbade that adjudication; license: the spec's clause that a session derives the `concerns` decline and never the adjudication, which leaves the adjudication the developer's to write; the bullet now names both
- fixed 2026-09-11 — [Minor] "A worktree created with a generated name is renamed to this shape" named the wrong object: the shape is a branch name, and this repo keeps the worktree directory at its own path regardless; license: this repo's `CLAUDE.md`, which fixes that directory independently; the sentence now renames the branch and says the worktree's directory is a separate name
- fixed 2026-09-11 — [Minor] the wrap check flagged lines over 78 while the constraint says 72, and skipped every indented line — which is where three replacements land — with no repair path for a non-zero count; license: the plan's own Global Constraint; the check is now a before/after comparison against the merge base, since `workflow.md` already carries three long lines this wave does not touch, and it names the rewrap commit
- fixed 2026-09-11 — [Minor] `claude plugin validate` was presented as the invariant guarding the new rule file, which it cannot be: it does not read `rules/` at all, so an unquoted `: ` would fail silently at load time; license: `.claude/rules/plugin-authoring.md`, which says so and asks for a hand review; Task 6 gained a frontmatter read-back with a YAML parse, and Task 7 says what validate does not cover
- fixed 2026-09-11 — [Minor] no step invoked the elements-of-style pass the repo mandates over changed prose, and an implementer copying verbatim text could not run it without deviating; license: `.claude/rules/elements-of-style.md`; a Global Constraint now records that every Replace block carries the pass from authoring, and that rewording a block forfeits the guarantee
- hit fixed 2026-09-11 — round one's wave moved the all-Minor qualifier into Task 1 and renumbered two tasks, leaving three step references in the Self-review section pointing at steps that had become something else — W6 at "Task 2 steps 4 and 5" where it is now 3 and 4, the qualifier's phrase at "Task 2 step 3", and the branch pointer at "Task 2 step 5"; the gate that preceded this round returned `CLEAN` and its body claimed to have checked that very mapping, so the dispatcher found these by re-deriving every step citation mechanically rather than by reading. All three corrected, and the section now records that the derivation was re-run
- signal 2026-09-11 — another round earns its cost: the four Important repairs change rule text the wave hangs on and the report the developer acts on, so a diff-scoped read aimed at those four first is worth it; what remains after that is wording, one threshold and one added step

### 2026-09-11 — plan-adversary, fable 5.1, blocking (round 2, diff-scoped)

Scoped to round one's wave. The reviewer verified the delivery repair
against the hook script and the sync-rules skill and found it factually
sound — the one repair this round was told to attack first. Two others
did not survive execution on this branch. Every citation checked here,
including the two that needed running rather than reading.

- fixed 2026-09-11 — [Important] round one's repair placed "A round already full-document owes no successor — it is the close." immediately before "It inherits the gating…", rebinding the pronoun to the closing round, so the shipped rule would say the closing round inherits gating — the opposite object from decision 5; license: the spec's own sentence, which makes the confirming round the subject; the sentence now names it
- fixed 2026-09-11 — [Important] the rebuilt wrap check baselined on the merge base with `develop`, but `docs/domain/glossary.md` was already edited on this branch before implementation begins — 49 long lines at the merge base against 50 now — so the step would report growth on a file the wave may not touch and order a rewrap the same step forbids; license: the measurement itself, run at this commit; the check now compares against six stated counts measured before implementation, which cannot move under it
- fixed 2026-09-11 — [Important] the frontmatter read-back, which Task 7 declares the only check of the new rule file, imported PyYAML — `python3 -c 'import yaml'` fails on this host, so the plan's sole guard would have died before asserting anything; license: that failure, reproduced at this commit; the check is now a literal `diff` of the first six lines against the prescribed block, with no dependency
- fixed 2026-09-11 — [Important] the branch convention justified itself with a false claim about git: `git check-ref-format` accepts both `feature/#123-short-name` and a `/`-bearing form, so "the punctuation a ref cannot carry" and "cannot survive a branch name" would have shipped an untruth in rule text; license: those two commands, run at this commit; the section now gives the true reasons — a `#` is awkward unquoted in a shell, a `/` adds a hierarchy level the shape does not parse — and the read-back says the `org/repo#123` form is not carried by the convention
- fixed 2026-09-11 — [Important] the delivery repair removed every `sync-rules` invocation from Task 7 while the Order section still said "`sync-rules` and `claude plugin validate` run once, at Task 7" — contradicting the Global Constraint, the spec's exclusion and the rewritten task; license: those three; the bullet now says validate runs there and `sync-rules` never runs in this plan
- fixed 2026-09-11 — [Minor] Task 1 step 6's expected `grep` output listed three sites for "confirming" and omitted the all-Minor bullet that step 4 had just written into the same file; license: step 4's own edit; the expectation now names four
- fixed 2026-09-11 — [Minor] three descriptors still credited Task 2 with the all-Minor bullet after the qualifier moved to Task 1 — the File structure entry, Task 2's Files block and its Interfaces block; license: the move itself, recorded in round one's ledger; all three now name the Round cap bullet alone
- fixed 2026-09-11 — [Minor] two replacement blocks written in round one's wave exceeded the 72-column constraint the plan commits to, so Task 7 step 4 would have reported `workflow.md` growing and ordered a `style:` commit to repair a defect the plan prescribed verbatim; license: the constraint; both paragraphs are rewrapped inside their Replace blocks, and every Replace block was re-measured — the one line still over 72 is an existing line carried through unchanged
- fixed 2026-09-11 — [Minor] the rewritten rule said "eight classes of change owe an enumeration. This rule lists them" and then listed nine rows, because one duty answers two different edits — a counter that does not re-derive, inside the rule whose duty 4 is counters; license: the card's eight duties against the table's nine triggers; the sentence now says eight duties keyed by nine edits
- fixed 2026-09-11 — [Minor] the delivery gap named "a release, or a `-dev` dogfood install" as its route while no repo text describes that install — the version convention is in the plugin-versioning rule and the procedure only in the developer's own notes; license: those two locations; the report now says where each half lives instead of naming a step nobody documented
- hit fixed 2026-09-11 — the wrap check round two rebuilt used `for pair in "<file> <count>"` with `set -- $pair`, which relies on word splitting that zsh does not do — run on this host every file name arrived with its count appended and `awk` failed on all six, so the step would have died at the implementer's shell; the gate before this round returned `CLEAN` without running it, and the dispatcher found it by running it; the loop now reads its pairs from a heredoc, verified on this host, and the step says why
- signal 2026-09-11 — a third round pays only as a short diff-scoped read: five Important repairs are one sentence or one command each, but two of them changed verification commands that must be run on this branch rather than read. The dispatcher ran both — the `diff` heredoc returns 0 against its own prescribed block, and the six stated wrap counts were measured at this commit — so what is left is Minor: descriptions, numbering and two wrapped lines

### 2026-09-11 — plan-adversary, fable 5.1, blocking (round 3, diff-scoped)

Scoped to round two's wave, as that round's stop signal asked. The
reviewer ran both repaired commands on this host rather than reading
them, and checked its other claims by command too. One correction to the
brief it was given: the dispatcher told it the round cap was spent, which
was wrong — the developer answered before each of rounds 2 and 3, so each
reset the count. The cap has one round left; `blocking` is what stops the
loop here, not the cap.

- fixed 2026-09-11 — [Important] the six stated wrap counts hold only under a UTF-8 locale: `awk 'length'` counts bytes under `LC_ALL=C`, and these files are full of em dashes, so the same command reports 19 for `workflow.md` against the stated 3, 57 against 36 for the lifecycle rule and 72 against 50 for the glossary — the step would then report growth on text the plan prescribes verbatim and order the rewrap it forbids, which is the failure round two repaired for a different cause; license: the measurement, run both ways at this commit; both `awk` calls are now pinned to `LC_ALL=C.UTF-8` and the step says the numbers are character counts
- fixed 2026-09-11 — [Important] the branch convention's second justification was also false: `bash -c 'echo feature/#123-short-name'` and `zsh -fc` both print the name, and only zsh with `extendedglob` set fails, so "awkward to type unquoted in a shell" does not hold either; license: those three runs; the convention now states the shape and argues for it not at all, and says why — two attempts at a reason shipped claims that did not hold, and a naming convention does not owe one
- fixed 2026-09-11 — [Important] the convention reduced "a GitHub or GitLab issue" to its number alone while the ticket rule defines that phrase as `#123` **or** `org/repo#123`, so a cross-repo ticket would land as `feature/123-short-name` and read back as a same-repo reference; license: the spec's W6, which asks for four things — the two name shapes, the rename before the first commit, and the `branch:` record — and for no encoding rule at all; the developer asked why a branch convention was deciding how to write a GitHub ticket, and the answer was that round one's F4 admitted material the spec never scoped, which then cost rounds two and three three findings between them. W6 is cut back to the spec: the shape names `<ticket>` and defers to the ticket rule for what a ticket value is, and the pointer says only that the sourcing order falls through when a branch yields no reference — which is what that order already did
- fixed 2026-09-11 — [Minor] Task 6 step 5 still opened "Read the block back and parse it" one paragraph before "It uses no YAML parser" — a leftover of the version round two removed; license: that removal; the clause now says "compare it"
- fixed 2026-09-11 — [Minor] Task 7 step 4 said "four of these files already carry long lines" where all six do — a counter that does not re-derive, in the step the new rule's duty 4 is about; license: the six measured counts; it now says every one
- fixed 2026-09-11 — [Minor] checks `J` and `K`, moved into Task 1 by round one, had after values and no before values, against the Global Constraint that every step states both; license: that constraint; both `echo` lines moved into step 1 and their before values are measured and stated, `J 1` and `K 0`
- fixed 2026-09-11 — [Minor] the branch-naming section, read alone, left no room for the `<topic>.docs` branch this very work runs on, so the plan's own `branch:` field looked like a violation of the convention it ships; license: the spec-plan-lifecycle rule, which defines that branch as a sibling of the topic branch rather than a second one; the section now says the field records the topic branch and names the document branch as the sibling it is
- signal 2026-09-11 — a fourth round pays only as a few minutes on three sentences and one command line, and after this wave all three are settled: the third was dissolved rather than answered, by cutting the text that raised it. The residue belongs to the full-document confirming round the plan owes before its loop closes, which will read these repairs in place rather than in isolation
- signal 2026-09-11 — a scope note the dispatcher owes the next reader: W6 grew past its spec item at round one and shrank back at round three. Three findings across three rounds were spent on text the spec never asked for, and none of them was wrong — the cost was admitting the scope, not reviewing it

### 2026-09-12 — plan-adversary, fable 5.1, concerns (round 4, full-document)

The confirming round the plan owed before its loop could close, and the
first non-`blocking` verdict it has returned. The gate ran full-scope
first and returned `CLEAN`; the reviewer then re-ran the plan's own
commands rather than reading them, and reported finding no disagreement
between the Order, Self-review, Deviations sections and the tasks —
after the scope cut the document says one thing. Every citation checked
here, including the branch this repo carries.

- fixed 2026-09-12 — [Important] the round-three cut left a subordinate clause, "where `<ticket>` is the work's tracker reference as the ticket-frontmatter rule defines it", which binds the slot to that rule's value forms and so answers the developer's question in the opposite direction: this repo's own `feature/12-python-content` becomes non-compliant with the rule the repo ships, and a session obeying "renamed before its first commit" would rewrite it to carry a `#`; license: this repo's `CLAUDE.md`, whose example is `feature/6-salesforce-standards`, and the spec's W6, which names the shape and no value clause; the section now says the spelling is the project's own and fixes only the shape
- fixed 2026-09-12 — [Minor] "The ticket rule reads the ticket back out of the recorded name" overstates that rule, whose sourcing order reads the current branch name as the first of three sources for a new document, before any `branch:` field exists; license: that order; the sentence now says what it does
- fixed 2026-09-12 — [Minor] after the edit the resolution-annotation bullet said a resolution carries "a body note saying what resolved them" and that on an implemented plan the frontmatter entry "is the only lever left", while the implemented-document bullet excepts ledger process records from its frontmatter-only clause — so the shipped rule left open whether the note is written; ruling: 2026-09-12; the clause now says the body note is written too, on that same exception, and names `, debt discharged <date>` as the exception's other instance
- fixed 2026-09-12 — [Minor] W4 described the co-firing line where the integrity audit had handed the plan "W4's literal line shape" as its agenda, and never said whether the line joins or replaces the per-hit lines the same step prescribes; license: that agenda item, recorded in the spec's ledger; the step now says the line goes beneath the per-hit lines and shows it
- fixed 2026-09-12 — [Minor] the spec disagrees with itself about the glossary — its Scope preamble counts the **Round heading** continuity clause as already applied while W1's body says the entry gains it, and the clause is measurably absent — and the plan followed the body without recording the disagreement or sweeping the edit; license: the measurement; a fourth Deviation records it and Task 7 sweeps it as `W1r`
- fixed 2026-09-12 — [Minor] W6 mints `feature/<ticket>-<short-name>` while `spec-plan-lifecycle.md` writes the same slot as `feature/<issue>-<name>` in its document-branch paragraph, so the wave would ship two rules of one payload naming one slot differently — the changed-interface class the wave's own new rule tells an author to enumerate; license: that duty and the spec's choice of `<ticket>` for a tracker-agnostic rule; Task 3 gains a step that matches the older spelling to the newer
- signal 2026-09-12 — another round would not repay: the one Important is a clause cut whose correctness is checked by reading `CLAUDE.md` beside the text, which needs no fresh context, and the rest is wording, one ruling and one Deviations entry. With this heading full-document the loop may close by annotation

The loop closes here. Four rounds — `blocking`, `blocking`, `blocking`,
`concerns` — returned thirty-three findings and every one is terminal:
thirty carry `license:`, three carry `ruling:`, and no `open` or `held`
line remains. The last round was full-document, so the confirming round
this plan owed is the round that produced the standing verdict rather
than one still due. Five propagation gates ran, two found hits and the
dispatcher found two more by running commands a gate only reads.

What the verdict's `concerns` still names is the residue round four
judged not worth another read: wording, one Deviations entry, and the
ruling recorded above. Nothing in it blocks execution, which is why the
close is an annotation rather than a fresh round.
