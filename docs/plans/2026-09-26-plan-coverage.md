---
ticket: none
date: 2026-09-26
status: approved
adversary: concerns (resolved 2026-09-26)
spec: ../specs/2026-09-25-plan-coverage-design.md
branch: feature/plan-coverage
base: develop
---

# Plan coverage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land `docs/specs/2026-09-25-plan-coverage-design.md` — the
decision register, the plan annotations, the propagation auditor's
coverage and table-closure duties, the held coverage hit, and the two
readers' new checks — across the `working-process` plugin.

**Architecture:** Every deliverable is prose in a shipped rule, agent
card, skill or README. There is no code and no test suite; a task's test
is the check block it publishes, run before and after the edit, with the
before values measured against the files on 2026-09-26. The grammar has
one home — the spec-plan-lifecycle rule for the register and the plan
annotations, the technical-design rule for the table relations — and the
auditor's card names those sections by heading instead of repeating
them.

**Tech Stack:** Markdown rule, agent and skill files distributed as a
Claude Code plugin and Rules payload; `tr`, `grep`, `awk`, `python3` and
`claude plugin validate` for verification.

## Global Constraints

- **The spec is the source.** Where this plan and the spec disagree, the
  spec wins and the plan is wrong — except where *Deviations from the
  spec* below records a departure and its reason.
- **Prose wraps at 72 characters** in every rule, agent card, skill and
  README. Match the surrounding paragraph; never reflow a paragraph this
  plan does not change. Indented grammar examples and table rows are
  exempt, as they are everywhere in the rules.
- **Copy every Replace block verbatim.** The blocks already carry the
  elements-of-style pass; a block an implementer rewords owes the pass
  again, and its checks may stop matching.
- **Checks normalise whitespace and match fixed strings.** A prose check
  pipes the file through `tr -s '[:space:]' ' '` and counts with
  `grep -oF … | wc -l`, so a phrase matches wherever a line wraps and
  the count is the same under GNU grep and ugrep. Only a check anchoring
  something that cannot wrap — a heading, a table row, a command — reads
  the file plain.
- **The glossary binds.** `docs/domain/glossary.md` terms and `_Avoid_`
  bans govern every new sentence: **Decision register**, **Decision
  coverage**, **Hit**, **Gate line**, **Ruling** and **Judged document**
  are canonical; bare "coverage" for the decision coverage map, "decision
  log" and "mechanical finding" are banned.
- **Realizes:** D28.1 — **The architect agent's card gains nothing.**
  `plugins/working-process/agents/architect.md` is not modified by any
  task; Task 12 checks it.
- **Realizes:** D28.2 — **The plan-adversary's dimension 5 is
  unchanged.** Task 7 adds a dimension after it and touches none of its
  text; Task 7 and Task 12 check the section's hash.
- **Realizes:** D28.3 — **`superpowers:writing-plans` is not changed.**
  Nothing in this plan edits another plugin; the plan annotations live
  in the working-process lifecycle rule alone.
- **Public repo hygiene**: no machine-specific paths, no company or
  client names, all committed text in English.
- **Commit messages are one line** — a conventional-commit subject, no
  body and no trailer, not even `Co-Authored-By`. A subagent
  implementer's brief says so outright, since subagents add the trailer
  by default.
- **Commits land on `feature/plan-coverage`.** The document branch
  `feature/plan-coverage.docs` merges into it at the implementation-ready
  gate, before Task 1.
- **Do not run `sync-rules`, do not bump the plugin version, and do not
  move the spec's or this plan's `status`.** All three are the
  developer's.

## Deviations from the spec

Recorded here and beside the text they concern.

1. **Task 5 also rewrites the card's `description:` and Task 11 the
   README's "a clean audit reports the single line `CLEAN`".** The
   spec's *Changes by file* names only the card's "exactly two lines"
   sentence, but both texts state the contract D11.4 changes, and a
   changed interface reaches every consumer (propagation duty 1).
2. **Task 3 amends the lifecycle sentence "`open` and `held` are the
   non-terminal states, and the only two the Unfinished-work list
   anchors".** D13.2 makes the list anchor `hit held` as well, so the
   sentence would turn false beside the widened command.
3. **Task 3 renames "Neither shape covers a hit left outstanding" to
   "No gate-line shape covers…".** With four new shapes, "neither" no
   longer names two; the out-of-scope statement itself stands, as the
   spec's *Out of scope* keeps it.
4. **Task 6 narrows the workflow rule's "A hit is a report, not a
   question" to a dismissed hit.** D26 makes a held coverage hit the one
   hit that asks the developer something, so the sentence as written
   would contradict the exception the same task adds.
5. **The register grammar lives in the lifecycle rule alone; the
   auditor's duty 10 names its sections by heading.** The spec lists the
   grammar under the lifecycle rule and the steps under the card, and
   stating the grammar in both would give it two homes — the same reason
   D21 gives the table relations one home.
6. **The glossary is verified, not written.** The spec's *Changes by
   file* records the glossary entries as applied at the grilling and
   the reviews; commit `69b8dcb` holds them. Task 12 checks they stand.
7. **This plan carries `**Realizes:**` annotations although the
   convention ships with it.** The installed propagation auditor has no
   duty 10 yet, so Task 12 derives this plan's decision coverage with a
   script instead of relying on the gate; Task 13 then runs the changed
   card itself.
8. **Duties 10 and 11 read the grammar from the plugin's own copy of
   each rule, `${CLAUDE_PLUGIN_ROOT}/rules/…`.** The spec says the rule
   loads when the auditor reads the document, but Task 6 writes the
   premise that a separate context cannot count on a rule loading, and
   an installed copy may lag the card after an update. The path repeats
   none of the grammar, so D21 and Deviation 5 stand. Adversary round 1
   raised it; the developer ruled on 2026-09-26.
9. **Task 3 grants a `## Review rounds` section to "a document", where
   the spec says "a plan".** The spec also places a `hit held` line in a
   design spec audited alone, before its first round, and such a spec
   has no section yet either. Ruled on 2026-09-26.
10. **Task 2 and Task 5 state that an annotation counts only at its
    defined place.** The spec defines each line's place without saying
    that the same text elsewhere instantiates nothing, and this plan
    quotes `**Defers:** D6` in a code block while citing D6 — a false
    hit waiting for a text-matching auditor. Ruled on 2026-09-26.
11. **Task 3 Step 9 lets an open `hit held` line block the consumption
    gate.** The spec says a held hit blocks the dispatch its gate
    guards and is silent on the gate, so a developer who declined that
    dispatch would pass plan-writing over an unanswered decision.
    Adversary round 3 raised it; ruled on 2026-09-26.

## File structure

Modified, all under `plugins/working-process/`:

- `rules/spec-plan-lifecycle.md` — Task 1 (the `decisions:` field and
  the `## Decision register` section), Task 2 (the template sentence and
  the `## Plan annotations` section), Task 3 (the gate lines, the
  non-terminal sentence, the fix heading, the Unfinished-work entry).
- `rules/technical-design.md` — Task 4: the `## Declared table
  relations` section.
- `agents/propagation-auditor.md` — Task 5: duties 10 and 11, the
  output contract, the held-hit exception, one out-of-bounds bullet, the
  description.
- `rules/workflow.md` — Task 6: the held coverage hit in *The
  propagation gate*, the closing-token paragraph, and the delegating
  brief in step 4.
- `agents/plan-adversary.md` — Task 7: dimension 6.
- `agents/integrity-auditor.md` — Task 8: the register as a declared
  rule.
- `rules/propagation-duties.md` — Task 9: two rows, the duty-2 anchor
  case, the counters.
- `skills/grilling-session/SKILL.md` — Task 10: updating the register.
- `README.md`, `CHANGELOG.md` — Task 11.

Created: `plugins/working-process/scripts/decision-coverage.py` and
`tests/working-process/test_decision_coverage.py` (Task 14). Not
modified: `agents/architect.md` (D28.1), the
glossary (already applied — Deviation 6), and `process-status`, which
runs the Unfinished-work commands as the lifecycle rule publishes them
and names none itself.

## Order and independence

- Tasks 1, 2 and 3 edit the lifecycle rule in that order. Task 2's
  second anchor is the `## Finding what revises a document` heading,
  which Task 1's replacement keeps as its last line, so the anchor still
  matches once after Task 1.
- Task 5's duty 10 names the lifecycle sections Tasks 1 and 2 create,
  and its duty 11 names the heading Task 4 creates. Run Tasks 1, 2 and 4
  first; the names are the interface, recorded in each task's
  **Interfaces:** block.
- Task 6's exception points at the `hit held` line Task 3 defines, and
  Task 9's rows cite the duty numbers Task 5 creates.
- Tasks 7, 8 and 10 depend on nothing else in this plan.
- `claude plugin validate` runs once, in Task 12, after every file has
  changed. Task 13 runs the changed auditor card on fixtures and needs
  every earlier task landed. Tasks 14–16 were added during
  implementation, after Task 13 measured duty 10 unstable: Task 14
  writes the script, Task 15 points the card at it, and Task 16 re-runs
  Task 13 twice on the script-backed card.

---

### Task 1: Lifecycle rule — the `decisions:` field and the decision register

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the
  frontmatter block, the bullet list under it, and a new section before
  `## Finding what revises a document`.

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: the section heading `## Decision register`, which Task 5's
  duty 10 and Task 10's bullet name; the grammar of an identity
  paragraph, the `withdrawn` token and the declared rule.

**Realizes:** D1, D2, D3, D4, D5, D6, D17, D24

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^decisions: registered ' $F)"
echo "B $(grep -c '^## Decision register$' $F)"
echo "C $(n $F | grep -oF 'The register is an index, never a copy.' | wc -l)"
echo "D $(n $F | grep -oF 'withdrawn <reason>, ruling: <date>[; replaced by <id>]' | wc -l)"
echo "E $(n $F | grep -oF 'the register lists every decision in this spec that needs realization.' | wc -l)"
echo "F $(n $F | grep -oF 'never in a sweep' | wc -l)"
echo "G $(n $F | grep -oF 'a newer design spec carrying `revises:`' | wc -l)"
echo "H $(grep -c '^## Finding what revises a document$' $F)"
echo "I $(n $F | grep -oF 'the tombstone is its record' | wc -l)"
```

Expected: `A 0`, `B 0`, `C 0`, `D 0`, `E 0`, `F 0`, `G 0`, `H 1`, `I 0`.

- [ ] **Step 2: Add the field to the frontmatter block**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
revises: ./<file>.md   # optional: documents this one departs from; inline list when several
```

Replace with:

```
decisions: registered   # optional, design specs only: the body carries a decision register
revises: ./<file>.md   # optional: documents this one departs from; inline list when several
```

- [ ] **Step 3: Add the field's bullet**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
  One technical design per design spec.
- Where a plan's `technical-design:` names documents, those documents
```

Replace with:

```
  One technical design per design spec.
- `decisions:` is optional, on design specs only, and takes one value,
  `registered`: the spec carries a decision register, defined under
  *Decision register* below. It is a convention field rather than a
  process stamp — no review step writes it, and no Unfinished-work
  command reads it.
- Where a plan's `technical-design:` names documents, those documents
```

- [ ] **Step 4: Add the section**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
## Finding what revises a document
```

Replace with:

```
## Decision register

A design spec that sets `decisions: registered` carries a `## Decisions`
section — the decision register, the enumerable list of the decisions
the spec makes that need realization. The propagation auditor, when
that agent is available, derives a plan's decision coverage from it.

The register is an index, never a copy. An entry is one identity
paragraph — the identifier and a short statement of the decision — and
may name the section that argues it:

    - **D3** — <a short statement of the decision>. Argued in *<section>*. [state token]

      <optional prose, indented, after a blank line>

The identity paragraph is the list item's first paragraph: its opening
line and the continuation lines after it, up to the first of a blank
line, a nested list item, the next list item at the same or a higher
level, or the end of the section. A reader joins those lines,
normalising whitespace, before parsing, so a statement wrapped across
lines keeps its state token at the paragraph's end. Prose beneath the
blank line is free. The grammar enforces the paragraph's shape, never a
sentence count: restating the argument in the register would give the
decision two homes, and the first fix wave would leave the register
describing the decision's old form.

The identifier is the literal token `**D<n>**`, or `**D<n>.<m>**` for a
child, at the start of a list item under `## Decisions`; a child's item
nests under its parent's. Identifiers are unique within the spec and
never positional, renumbered or reused: a decision added mid-loop takes
the next free number. A Markdown numbered list is refused, because its
numbers are positions and move when an item is inserted above. An
element of a list that needs realization on its own takes a child
identifier. The parent of children is a group: it enters no count, a
citation of it covers none of its children, and it carries no state
token.

Every decision that needs realization enters, cross-cutting constraints
included. A ruling that something stays as it is enters too, since an
implementer can break it, and a plan realizes it as a constraint; no
kind of entry is exempt. A rejected alternative never enters: nobody
realizes it, and it already has homes — a spec's out-of-scope section,
a technical design's *Cuts not taken*.

An entry without a token is active. One state token exists, carried by
a leaf or not at all, and never by a group:

    withdrawn <reason>, ruling: <date>[; replaced by <id>]

The decision no longer stands. The entry stays as a tombstone that
reserves its identifier, so a reuse shows up as a duplicate.
`replaced by` names an identifier of the same register other than its
own, and a chain of successors never forms a cycle; a successor may
itself be withdrawn. The token is recognized by its opening word alone:
the first segment after the full stop that ends the statement, and after
any "Argued in" pointer, that begins with `withdrawn`; it runs to the
paragraph's end, so its reason may hold a full stop. A segment so
opening that does not match the grammar is malformed, never prose.
Withdrawing a group is written on each of its leaves. A decision that
still stands but one plan does not realize is no state of the entry:
that plan defers it (see *Plan annotations*).

A withdrawal changes what the spec decides, so the session writes the
token only on the developer's explicit decision. Its `ruling:` is dated
with that decision; the edit lands in the spec's own ledger and leaves
the `integrity:` stamp stale, as any body edit does. On a spec whose
loop has closed, a withdrawal ruled outside any hit or finding writes
no ledger line: the tombstone is its record, since no diff-scoped round
follows a close. A spec already `implemented` takes no such edit: the
decision is withdrawn by a newer design spec carrying `revises:` and the
register that stands.

The spec's author creates the register while writing the spec, so a
design that never meets a grilling session still has one, and a
grilling session updates it as its decisions land. A spec carrying the
field declares a rule about itself: *the register lists every decision
in this spec that needs realization.* The integrity audit's first lens
verifies a document's declared rules in both directions, which gives
the register's completeness its reader.

A design spec without the field is legacy: the propagation audit
reports it as not checked and raises no hit, and a plan descending from
legacy specs alone carries no annotations. An existing spec migrates
when it is next substantively revised, never in a sweep. Every new
design spec is expected to set the field; its absence is reported, not
refused.

## Finding what revises a document
```

- [ ] **Step 5: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 1`, `D 1`, `E 1`, `F 1`, `G 1`, `H 1`, `I 1`.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): decision register in the lifecycle rule"
```

---

### Task 2: Lifecycle rule — the plan annotations

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the
  last sentence of the `**Interfaces:**` bullet, and a new section after
  `## Decision register`.

**Interfaces:**
- Consumes: the `## Decision register` section from Task 1, which the
  new section follows and cites.
- Produces: the section heading `## Plan annotations`, which Task 5's
  duty 10 names; the line shapes `**Realizes:**`, `**Defers:**`,
  `**Follows:**` and the heading `## Deferrals and predecessors`.

**Realizes:** D7, D8, D18, D19, D25, D30

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^## Plan annotations$' $F)"
echo "B $(n $F | grep -oF 'changes no plan template — the template belongs to the tool that writes plans.' | wc -l)"
echo "C $(n $F | grep -oF 'with one exception, defined under *Plan annotations* below' | wc -l)"
echo "D $(grep -c '^    \*\*Realizes:\*\* none$' $F)"
echo "E $(grep -c '^    \*\*Defers:\*\* D6 — <why>; ruling: <date>$' $F)"
echo "F $(grep -c '^    \*\*Follows:\*\* \.\./plans/<file>\.md$' $F)"
echo "G $(n $F | grep -oF 'so inheritance is not transitive' | wc -l)"
echo "H $(n $F | grep -oF '`../specs/<file>.md#D3`' | wc -l)"
echo "I $(n $F | grep -oF 'names this rule and requires reading it first' | wc -l)"
echo "J $(n $F | grep -oF 'describes the grammar and instantiates nothing' | wc -l)"
```

Expected: `A 0`, `B 1`, `C 0`, `D 0`, `E 0`, `F 0`, `G 0`, `H 0`, `I 0`,
`J 0`.

- [ ] **Step 2: Revise the template sentence**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
  convention stands unchanged. This binds how the blocks are filled and
  changes no plan template — the template belongs to the tool that
  writes plans.
```

Replace with:

```
  convention stands unchanged. This binds how the blocks are filled and
  changes no plan template. The template belongs to the tool that
  writes plans, with one exception, defined under *Plan annotations*
  below: this rule adds the `**Realizes:**` annotation on tasks and
  Global Constraints entries, and the `## Deferrals and predecessors`
  section with its `**Defers:**` and `**Follows:**` lines. The rest of
  the template stays with that tool.
```

- [ ] **Step 3: Add the section**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
## Finding what revises a document
```

Replace with:

```
## Plan annotations

A plan whose `spec:` names at least one registered design spec carries,
on every task, one line after its `**Files:**` block — after its
`**Interfaces:**` block where it has one — and before its first step:

    **Realizes:** D3, D5
    **Realizes:** none

`none` is a value, not an omission: without it a housekeeping task
cannot be told from an author who forgot. One decision may be cited by
several tasks, and a task split or merged in a fix wave stays covered as
long as the union of its identifiers survives. A cross-cutting
constraint is realized by the Global Constraints entry that states it,
and that entry opens with the same annotation as its first clause —
`**Realizes:** D9`. Only an entry that realizes a decision carries one,
and `none` is never written there. Citing the section as a whole
realizes nothing, and neither does citing a group: its leaves are what
a plan cites. `none` names no identifier, so it is never qualified.

A plan whose `spec:` names one spec writes bare identifiers. A plan
whose `spec:` names two or more — registered or legacy alike — qualifies
every identifier with its spec's path exactly as `spec:` writes it,
`../specs/<file>.md#D3`, wherever the plan or its audit names one. The
count of entries decides, never the count of registered ones, so
migrating a second spec out of legacy changes no annotation already
written.

Two more kinds of line form a section of their own, headed
`## Deferrals and predecessors` at the Global Constraints heading's
level and placed directly after that section. They state facts about
the whole plan rather than requirements of any task, so they stay out of
Global Constraints, which the plan template makes part of every task's
requirements:

    **Defers:** D6 — <why>; ruling: <date>
    **Follows:** ../plans/<file>.md

A `**Defers:**` line records that this plan leaves a standing decision
unrealized, one line per identifier, qualified as the annotations are.
The session writes it only on the developer's explicit decision, which
its `ruling:` dates. The deferral binds this plan alone: auditing any
other plan of the same spec, the decision counts, and the spec names no
plan. Deferring an undefined, withdrawn or group identifier is
malformed, and so is deferring one the plan also cites, locally or by
inheritance. A plan with neither kind of line carries no such
section, and in the pass for one spec a `**Defers:**` line naming
another spec's identifier is out of scope.

A `**Follows:**` line names a plan this one continues, by a path
relative to the plan. The predecessor shares at least one spec with
this plan's `spec:` and carries `status: implemented`, since only a
frozen body's citations cannot move. This plan inherits every
identifier the predecessor's `**Realizes:**` annotations cite for the
specs both plans name, and nothing else — never its `**Defers:**`
lines, and never its `**Follows:**` lines, so inheritance is not
transitive and a plan names every predecessor whose citations it relies
on. An inherited citation of an identifier the register withdrew after
the predecessor shipped covers nothing and raises no hit; a local
citation of it still does. Whether the predecessor's realization still
stands in the code is not this line's question: the diff the
implemented-document bullet above prescribes answers it.

An annotation, a `**Defers:**` line or a `**Follows:**` line counts
only at the place this section gives it: a task's line before its first
step, the opening clause of a Global Constraints entry, a line of
`## Deferrals and predecessors`. The same text inside a code block, or
quoted as an example, describes the grammar and instantiates nothing.

The plan's author writes these lines, whoever that author is. A session
writing a plan meets this rule by reading the design spec, and a brief
that delegates plan-writing to a separate context names this rule and
requires reading it first, as the workflow rule's step 4 says. A plan
lacking an annotation is caught at its first propagation gate, and an
identifier is added there only where the task's text actually realizes
the decision, never mechanically.

## Finding what revises a document
```

- [ ] **Step 4: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 0`, `C 1`, `D 1`, `E 1`, `F 1`, `G 1`, `H 1`, `I 1`,
`J 1`.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): plan annotations for decision coverage"
```

---

### Task 3: Lifecycle rule — the held gate line

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — the
  non-terminal sentence and the cross-document fix heading paragraph in
  `## The disposition ledger`; `### Gate lines`; the *Unfinished
  review-loop ledger* entry; the consumption-gate backstop sentence.

**Interfaces:**
- Consumes: the `**Defers:**` line and the `withdrawn` token from Tasks 1
  and 2, which two terminal shapes name.
- Produces: the `hit held` line and its three terminal shapes, which
  Task 5's card and Task 6's workflow exception point at; the widened
  command `rg -n --no-ignore --crlf '^- (open|held) —|^- hit held ' docs/`.

**Realizes:** D13.1, D13.2, D23, D28.4, D29

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^    - hit held <date> — ' $F)"
echo "B $(grep -c '^    - hit fixed <date> — <the hit.s claim>; <what changed>; ruling: <date>$' $F)"
echo "C $(grep -c '^    - hit deferred <date> — ' $F)"
echo "D $(grep -c '^    - hit withdrawn <date> — ' $F)"
echo "E $(grep -cF "rg -n --no-ignore --crlf '^- (open|held) —|^- hit held ' docs/" $F)"
echo "F $(grep -cF "rg -n --no-ignore --crlf '^- (open|held) —' docs/" $F)"
echo "G $(n $F | grep -oF 'Neither shape covers' | wc -l)"
echo "H $(n $F | grep -oF 'No gate-line shape covers' | wc -l)"
echo "I $(n $F | grep -oF 'the only two disposition states the Unfinished-work list anchors' | wc -l)"
echo "J $(n $F | grep -oF 'every later pre-round episode writes there too' | wc -l)"
echo "K $(n $F | grep -oF 'The same heading serves a register edit' | wc -l)"
echo "L $(n $F | grep -oF 'The ordinary `hit fixed` shape, without `ruling:`, stays' | wc -l)"
echo "M $(n $F | grep -oF 'writes two shapes of its own' | wc -l)"
echo "N $(n $F | grep -oF 'Both are written at gate time' | wc -l)"
echo "O $(n $F | grep -oF 'A document with no `## Review rounds` section gains one' | wc -l)"
echo "P $(n $F | grep -oF 'never joins a resolution note' | wc -l)"
echo "Q $(n $F | grep -oF '`held` lines or `hit held` gate lines stay open' | wc -l)"
```

Expected: `A 0`, `B 0`, `C 0`, `D 0`, `E 0`, `F 1`, `G 1`, `H 0`, `I 0`,
`J 0`, `K 0`, `L 0`, `M 1`, `N 1`, `O 0`, `P 0`, `Q 0`.

- [ ] **Step 2: Amend the non-terminal sentence**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
`open` and `held` are the non-terminal states, and the only two the
Unfinished-work list anchors. `fixed` and `declined` are terminal and
say what became of the document: it changed, or it stands.
```

Replace with:

```
`open` and `held` are the non-terminal states, and the only two
disposition states the Unfinished-work list anchors; the one gate line
it anchors, `hit held`, is defined under *Gate lines* below. `fixed`
and `declined` are terminal and say what became of the document: it
changed, or it stands.
```

- [ ] **Step 3: Let the fix heading serve a gate-licensed fix**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
round heading: it records a fix, not a round. Two stamps go stale as on
any body edit — the `integrity:` hash stops matching, and the verdict
stops certifying the words that changed.
```

Replace with:

```
round heading: it records a fix, not a round. Two stamps go stale as on
any body edit — the `integrity:` hash stops matching, and the verdict
stops certifying the words that changed. The same heading serves a
register edit that a plan's held gate line licensed, on a design spec
whose loop has closed at whatever verdict: the heading then names the
plan whose gate held the hit, and that plan's terminal gate line names
the heading and the line under it. Unlike a review-licensed fix, such an
edit never joins a resolution note, even on a `concerns (resolved)`
spec: that note records what resolved the verdict, and this edit
resolves none.
```

- [ ] **Step 4: Add the held shape to *Gate lines***

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
The propagation gate, when that agent is available, writes two shapes of
its own. They carry their own leading token and never a severity, because
a hit is a located detection the dispatcher confirms or dismisses, never
a graded finding:
```

Replace with:

```
The propagation gate, when that agent is available, writes gate lines of
its own: the two ordinary shapes here, and the held shape and its three
terminal rewrites below. Each carries its own leading token and never a
severity, because a hit is a located detection the dispatcher confirms
or dismisses, never a graded finding:
```

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
Neither carries a license either, because a hit's fix is licensed by its
own derivation.
```

Replace with:

```
Neither carries a license either, because a hit's fix is licensed by its
own derivation.

A hit of the coverage duty whose fix needs a decision no derivation
settles is held for the developer — the one exception the workflow rule
makes to hits never waiting. It takes a third shape, rewritten in place
to one of three terminal shapes, so its state always has one home:

    - hit held <date> — <the hit's claim>; question: <the missing decision>; options: <the options, with the session's recommendation>
    - hit fixed <date> — <the hit's claim>; <what changed>; ruling: <date>
    - hit deferred <date> — <the hit's claim>; ruling: <date>; Defers: <id>
    - hit withdrawn <date> — <the hit's claim>; ruling: <date>; <spec path>#<id>

The rewrite happens once the gate has re-run over the changed document
and whatever depends on it, never on the developer's answer alone.
`hit fixed … ruling:` records that the document now carries the
decision the developer settled — a plan that realizes it, or a register
the ruling repaired; `hit deferred` records an approved `**Defers:**`
line in the plan, and `hit withdrawn` a register entry now a tombstone.
Each is written only where it names what happened, and none is
`hit dismissed`, because the gap was real when the hit fired. The
ordinary `hit fixed` shape, without `ruling:`, stays for every hit
whose fix its derivation licensed. `ruling:` on a gate line means what
it means on a disposition line, and a diff-scoped round treats the line
as settled.

A `hit held` line lives in the ledger of the document whose gate raised
it — the audited plan, or the design spec audited alone. Its leading
date is the gate's, and the terminal rewrite replaces it with the date
the line reached its terminal state. A held hit ends its gate episode
and blocks the dispatch the gate guards; the re-run after the
developer's answer is a fresh episode. A register edit the answer
causes is recorded in the spec's own ledger — under its latest round
heading while its loop is open, and under the fix heading above once
its loop has closed. A spec already `implemented` takes the edit by
revision instead, and the held hit waits for it.
```

- [ ] **Step 5: Place a holding pre-round episode's lines**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
Both are written at gate time, under the last round's heading. The `hit`
```

Replace with:

```
Each is written at gate time, under the last round's heading. The `hit`
```

The held paragraphs Step 4 inserts now stand between the shapes and
this sentence, so "Both" would name two of six shapes.

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
diff-scoped brief is composed before its own round is stamped. A gate
before a document's first round has no heading to write under; its lines
wait for that round and are written at its stamp, the one case where
they do.
```

Replace with:

```
diff-scoped brief is composed before its own round is stamped. A gate
before a document's first round has no heading to write under; its lines
wait for that round and are written at its stamp, the one case where
they do — unless the episode holds a hit, since the round its lines
would wait for cannot start. A pre-round episode holding at least one
hit writes every one of its lines, the `hit held` line and its siblings
alike, in the `## Review rounds` section before the first round
heading, and they stay there, rewrites included: no round produced
them, and one episode keeps one home. Once such lines stand there,
every later pre-round episode writes there too, holding or not, so the
document's pre-round gate history keeps one place. A document with no
`## Review rounds` section gains one, at its end, with its first gate
line.
```

- [ ] **Step 6: Reword the outstanding-hit gap and the anchors sentence**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
Neither shape covers a hit left outstanding when the re-dispatch bound
```

Replace with:

```
No gate-line shape covers a hit left outstanding when the re-dispatch bound
```

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
rather than silence. Neither joins the unfinished-work anchors: both are
closed when written and owe nobody a next move.
```

Replace with:

```
rather than silence. Neither joins the unfinished-work anchors: both are
closed when written and owe nobody a next move. A `hit held` line owes
the developer an answer, so it joins them until its terminal rewrite.
```

The first replacement runs one word past the wrap; Step 7 rewraps it.

- [ ] **Step 7: Rewrap the outstanding-hit paragraph**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
No gate-line shape covers a hit left outstanding when the re-dispatch bound
in the workflow rule stops an episode. That state owes the developer a
decision, so neither `hit fixed` nor `hit dismissed` can honestly carry
it, and no anchor surfaces it today — a stated gap, not an oversight.
Until a shape exists, the workflow rule's report is its only record.
```

Replace with:

```
No gate-line shape covers a hit left outstanding when the re-dispatch
bound in the workflow rule stops an episode. That state owes the
developer a decision, so neither `hit fixed` nor `hit dismissed` can
honestly carry it, and `hit held` is scoped to the coverage duty's
hits; no anchor surfaces it today — a stated gap, not an oversight.
Until a shape exists, the workflow rule's report is its only record.
```

- [ ] **Step 8: Widen the Unfinished-work entry**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
- **Unfinished review-loop ledger** — a disposition line nobody closed:
  an `open` line whose remediation never ran, or a `held` line whose
  question still waits.
  `rg -n --no-ignore --crlf '^- (open|held) —' docs/`
```

Replace with:

```
- **Unfinished review-loop ledger** — a disposition line or a held gate
  line nobody closed: an `open` line whose remediation never ran, or a
  `held` or `hit held` line whose question still waits. A gate line's
  date stands between its token and its dash, so the command takes an
  alternative rather than a third token inside the group.
  `rg -n --no-ignore --crlf '^- (open|held) —|^- hit held ' docs/`
```

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
  Owner: an `open` line belongs to the document's next touch, which
  re-offers the remediation; a `held` line belongs to the developer.
```

Replace with:

```
  Owner: an `open` line belongs to the document's next touch, which
  re-offers the remediation; a `held` or `hit held` line belongs to the
  developer.
```

- [ ] **Step 9: Let an open held hit block the consumption gate**

Find in `plugins/working-process/rules/spec-plan-lifecycle.md`:

```
A document's consumption gate is the backstop for its ledger: no judged
document passes to plan-writing, nor a plan to implementation, while
`held` lines stay open — an LGTM can leave the frontmatter clean while a
decision question still pends, so the gate asks those questions at the
latest. Writing a plan from a judged document is that same seam: its
held questions are asked before the plan is written, whoever writes it.
```

Replace with:

```
A document's consumption gate is the backstop for its ledger: no judged
document passes to plan-writing, nor a plan to implementation, while
`held` lines or `hit held` gate lines stay open — an LGTM can leave the
frontmatter clean while a decision question still pends, so the gate
asks those questions at the latest. A `hit held` line blocks until the
gate has re-run and rewritten it to a terminal shape, since declining
the dispatch it guarded decides nothing; a closed gate line blocks
nothing. Writing a plan from a judged document is that same seam: its
held questions are asked before the plan is written, whoever writes it.
```

- [ ] **Step 10: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 1`, `D 1`, `E 1`, `F 0`, `G 0`, `H 1`, `I 1`,
`J 1`, `K 1`, `L 1`, `M 0`, `N 0`, `O 1`, `P 1`, `Q 1`.

Then run the widened command over a fixture, to prove it matches both a
disposition line and a held gate line and nothing terminal:

```bash
d=$(mktemp -d); mkdir -p "$d/docs"
printf '%s\n' '## Review rounds' '- held — [Minor] x; question: q; options: o' \
  '- hit held 2026-09-26 — D4 uncovered; question: q; options: o' \
  '- hit fixed 2026-09-26 — D4 uncovered; task 7 added; ruling: 2026-09-26' \
  '- hit deferred 2026-09-26 — D4 uncovered; ruling: 2026-09-26; Defers: D4' > "$d/docs/p.md"
(cd "$d" && rg -n --no-ignore --crlf '^- (open|held) —|^- hit held ' docs/ | wc -l)
rm -rf "$d"
```

Expected: `2`.

- [ ] **Step 11: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): held gate line for coverage hits"
```

---

### Task 4: Technical-design rule — the declared table relations

**Files:**
- Modify: `plugins/working-process/rules/technical-design.md` — a new
  section at the end of the file.

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: the heading `## Declared table relations`, which Task 5's
  duty 11 names and nothing repeats.

**Realizes:** D10, D21

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/technical-design.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^## Declared table relations$' $F)"
echo "B $(grep -c '^| State `written by` | Parts `part` |$' $F)"
echo "C $(grep -c '^| State `read by` | Parts `part` |$' $F)"
echo "D $(grep -c '^| Contracts `producer → consumer`, each side | Parts `part` |$' $F)"
echo "E $(n $F | grep -oF '`external: <name>`' | wc -l)"
echo "F $(n $F | grep -oF 'is outside the relation' | wc -l)"
echo "G $(tail -n 1 $F)"
```

Expected: `A 0`, `B 0`, `C 0`, `D 0`, `E 0`, `F 0`,
`G responsibility, and a contract its implementation can change behind.`

- [ ] **Step 2: Add the section**

Find in `plugins/working-process/rules/technical-design.md`:

```
names must still have a resolvable identity, an explicit
responsibility, and a contract its implementation can change behind.
```

Replace with:

```
names must still have a resolvable identity, an explicit
responsibility, and a contract its implementation can change behind.

## Declared table relations

Where a column names rows of another table, the relation is declared
here, and this section is its only home. The propagation audit, when
that agent is available, resolves every declared relation and checks
nothing a declaration does not name: matching cell values would guess a
relation rather than read one.

| column | names rows of |
|---|---|
| Contracts `producer → consumer`, each side | Parts `part` |
| State `written by` | Parts `part` |
| State `read by` | Parts `part` |

A cell may name several rows, comma-separated, and
`producer → consumer` splits at the arrow before it splits at commas. A
party outside the system is written `external: <name>` and is no
reference. No side of these three relations may be empty: the
definitions above give every contract a consumer and every state record
a writer and a reader, so an empty cell, or one naming nothing, fails
the relation. A later declaration that admits an empty side says so
itself. Every other name resolves to exactly one row of Parts, because
a duplicated part name makes every reference to it ambiguous.

A Contracts flow written as a numbered sequence rather than a table row
is outside the relation: the skeleton gives the sequence no grammar a
parse could split, so its steps are not references.
```

- [ ] **Step 3: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 1`, `D 1`, `E 1`, `F 1`,
`G parse could split, so its steps are not references.`

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/rules/technical-design.md
git commit -m "feat(working-process): declared table relations in the technical-design rule"
```

---

### Task 5: Propagation auditor — duties 10 and 11 and the report

**Files:**
- Modify: `plugins/working-process/agents/propagation-auditor.md` — the
  `description:` line, two new duties after duty 9, `## Output`,
  `## What becomes of your hits`, `## Out of bounds`.

**Interfaces:**
- Consumes: the lifecycle headings `## Decision register` (Task 1) and
  `## Plan annotations` (Task 2); the technical-design heading
  `## Declared table relations` (Task 4); the `hit held` line (Task 3).
- Produces: duty numbers 10 and 11, which Task 9's rows cite; the report
  lines `decision-coverage:`, `withdrawn since:` and `table-closure:`,
  which Task 6's closing-token paragraph names.

**Realizes:** D9, D10, D11.1, D11.2, D11.3, D11.4, D12, D17, D22, D26, D27, D30

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/agents/propagation-auditor.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^### 10\. Decision coverage' $F)"
echo "B $(grep -c '^### 11\. Table closure' $F)"
echo "C $(n $F | grep -oF 'exactly two lines' | wc -l)"
echo "D $(n $F | grep -oF 'or the single line CLEAN' | wc -l)"
echo "E $(grep -c '^    decision-coverage: <spec path> ' $F)"
echo "F $(grep -c '^    table-closure: <document path> ' $F)"
echo "G $(grep -c '^      withdrawn since: ' $F)"
echo "H $(n $F | grep -oF '*Decision register* and *Plan annotations*' | wc -l)"
echo "I $(n $F | grep -oF '`## Declared table relations`' | wc -l)"
echo "J $(n $F | grep -oF 'is held for the developer' | wc -l)"
echo "K $(n $F | grep -oF 'means no hit in the checks that ran' | wc -l)"
echo "L $(awk '/^### /{c++} END{print c}' $F)"
echo "M $(head -n 5 $F | grep -c '^description: "')"
echo "N $(n $F | grep -oF '${CLAUDE_PLUGIN_ROOT}/rules/' | wc -l)"
echo "O $(n $F | grep -oF 'a code block or a quoted example describes the grammar' | wc -l)"
```

Expected: `A 0`, `B 0`, `C 1`, `D 1`, `E 0`, `F 0`, `G 0`, `H 0`, `I 0`,
`J 0`, `K 0`, `L 9`, `M 1`, `N 0`, `O 0`.

- [ ] **Step 2: Rewrite the description**

Find in `plugins/working-process/agents/propagation-auditor.md`:

```
re-derives every counter, and returns located hits with their derivation — or the single line CLEAN.
```

Replace with:

```
re-derives every counter, derives a plan's decision coverage from its design specs' decision registers, resolves the table relations the technical-design rule declares, and returns located hits with their derivation — or, where none fires, the token CLEAN after the report's decision-coverage and table-closure lines.
```

The anchor is the tail of the one-line `description:` value, so the
replacement keeps the line's closing text — `Verdict-free and
persona-free: …` — untouched after it. The value stays one quoted line.

- [ ] **Step 3: Add duties 10 and 11**

Find in `plugins/working-process/agents/propagation-auditor.md`:

```
is found rather than skipped. A plan whose `spec:` is not named back is
not a hit: no design spec names its plans.
```

Replace with:

```
is found rather than skipped. A plan whose `spec:` is not named back is
not a hit: no design spec names its plans.

### 10. Decision coverage — every registered decision has an owner

Runs on a plan, and on a design spec audited alone. The register's
grammar, its state token and the plan's annotations are defined in the
spec-plan-lifecycle rule, under *Decision register* and *Plan
annotations*. Read them in the plugin's own copy,
`${CLAUDE_PLUGIN_ROOT}/rules/spec-plan-lifecycle.md`, which matches this
card's version, rather than recalling them. Read a line only at the
place *Plan annotations* gives it: a code block or a quoted example
describes the grammar. For each spec the plan's `spec:` names:

1. Read the spec's `decisions:` field. Absent: the spec is legacy —
   write `not checked` for it and stop. Any value other than
   `registered`: a hit, `not counted`, stop.
2. Check that the register is well formed. Each of these is a hit: the
   field set with no `## Decisions` section; an identity paragraph that
   does not parse, including a child nested under a parent other than
   its own, a child whose parent does not exist, and a register written
   as a numbered list; a duplicate identifier; a segment opening with
   `withdrawn` that does not match the token's grammar; a group
   carrying a state token; a `replaced by` naming a missing identifier,
   its own, or a group, or closing a cycle. Where any fires, the counted
   set cannot be trusted: write `not counted` and stop.
3. Check the plan's `**Follows:**` lines. One naming a missing file, a
   plan sharing no spec with the audited plan, or a plan not at
   `status: implemented` is a hit, and lends nothing to the steps
   below. A predecessor lends identifiers only for the specs both plans
   name; in the pass for a spec it does not name, its line is out of
   scope rather than a hit.
4. Collect the cited set: every identifier the plan's `**Realizes:**`
   annotations cite, on tasks and Global Constraints entries, and every
   identifier inherited through the `**Follows:**` lines step 3
   accepted, each with the plan and site it comes from. A cited
   withdrawn identifier, a cited group and a cited identifier the
   register does not define are hits. The last is an error in the plan,
   never a gap in the spec — identifiers are minted only in the
   register — so duty 5 does not take it. An inherited citation of an
   identifier withdrawn since its predecessor shipped is skipped: not
   counted, not a hit, and listed apart in the report.
5. Check the plan's `**Defers:**` lines. One naming an undefined,
   withdrawn or group identifier, or one in the cited set, is a hit and
   subtracts nothing. In the pass for one spec, a line naming another
   spec's identifier is out of scope.
6. Collect the counted set: the leaf identifiers not withdrawn, less
   those the `**Defers:**` lines step 5 accepted name.
7. Report every counted identifier the cited set lacks, one hit per
   identifier. A task with no `**Realizes:**` line, in a plan whose
   `spec:` names a registered spec, is a hit too, and so is a bare
   identifier in a plan whose `spec:` names two or more specs.

Derive the map, never tally it: write each counted identifier with the
sites citing it, and let the fraction summarise the map, since a bare
count passes one omission offset by one duplicate. An identifier cited
by several tasks is legal.

On a design spec audited alone — the gate before its architect round —
run steps 1 and 2 only, so a malformed register is found before any plan
depends on it.

This duty proves that every declared decision has an owner. Whether the
register lists every decision the spec makes is the integrity auditor's
judgment, and whether the citing tasks realize their decision is the
plan-adversary's. Measured in an outside project: a plan realized six of
a spec's eight table rows, and two adversary rounds, three propagation
audits and the author's self-review passed it, because none carried
"every decision has an owning task" in its brief.

### 11. Table closure — a column naming another table's rows resolves

Runs on a technical design. Check only the relations the rule defining
the tables declares, never relations guessed from matching values: two
unrelated columns can share names by chance, and a relation whose every
reference is wrong would match nothing. The technical-design rule
declares them under its heading `## Declared table relations`, with how
each cell splits and which values are not references; read them in the
plugin's own copy, `${CLAUDE_PLUGIN_ROOT}/rules/technical-design.md`.
For each declared relation whose tables the document carries, every
name in the column resolves to exactly one row of the named table: a
name matching no row is a hit, and so is a name matching several. An
empty cell is a hit wherever the declaration gives the column no empty
side. A relation whose table the document does not carry is not
applicable and is not counted, and a table no declaration names is
outside this duty. Measured on 2026-09-16: walked duty by duty, none of
the first nine checked referential integrity between two tables of one
document.
```

- [ ] **Step 4: Rewrite the output contract**

Find in `plugins/working-process/agents/propagation-auditor.md`:

```
A clean audit runs to exactly two lines: the self-report above, then the
literal token.

    CLEAN

Add nothing after the token. The self-report opens every report, and a
clean run is the case where that is easiest to forget.

Otherwise, one entry per hit:

    <file:line or document section> — <one-sentence claim> — derivation: <the parse, enumeration, count, or diff that produced it>
```

Replace with:

```
Then one entry per hit, if any fired:

    <file:line or document section> — <one-sentence claim> — derivation: <the parse, enumeration, count, or diff that produced it>

Then the lines duties 10 and 11 write on every run, clean ones included.
On a plan, one `decision-coverage:` block per spec its `spec:` names:

    decision-coverage: <spec path> 7/8 covered; inherited [D2]; deferred [D6]; uncovered [D4.2]
      D1 → Task 2
      D2 → ../plans/<file>.md (Task 3)
      D3 → Task 4, Task 6
      D4.2 → —
      D9 → Global Constraints, line 42: "No code"
      D10 → ../plans/<file>.md (Global Constraints, line 38: "No code")
      …
      withdrawn since: D4 ← ../plans/<file>.md (Task 2)
    decision-coverage: <spec path> not counted — malformed register
    decision-coverage: <spec path> not checked — no decision register

The summary line opens the block. Under a counted spec the map follows,
one indented line per counted identifier naming every task and
constraint that cites it: a task by its heading's number, a Global
Constraints entry by the line it opens on and its opening words after
the annotation, in quotes, and an inherited site by its plan's path with
the site in parentheses. An uncovered identifier maps to `—` and is a
hit above as well. The fraction's denominator is duty 10's counted set,
and its numerator the counted identifiers in the cited set; a counted
set of zero reads `0/0 covered`. The summary line carries every slot, in
the example's order, an empty one written `[]`. `inherited [..]` lists
the covered identifiers whose only citation is a predecessor's; one also
cited locally counts as local, and its map line names both sites.
`deferred [..]` lists what the plan defers, never counted as covered. A
skipped inherited citation follows the map on a `withdrawn since:` line,
outside the fraction. Qualify every identifier as the plan's annotations
are. `not counted` carries no map, since its denominator cannot be
derived.

On a design spec audited alone, one line and no map:

    decision-coverage: <spec path> register well formed
    decision-coverage: <spec path> not counted — malformed register
    decision-coverage: <spec path> not checked — no decision register

On a technical design, one line, counting the declared relations the
duty resolved in that document; no other document gets one:

    table-closure: <document path> 3 relations checked
    table-closure: <document path> no declared relations

Where no hit fired, close with the literal token:

    CLEAN

`CLEAN` means no hit in the checks that ran, and a `not checked` line
bounds that guarantee in the report itself. A clean report is the
self-report, the lines above that apply to the document, and the token,
with nothing after it. The self-report opens every report, and a clean
run is the case where that is easiest to forget. A report carrying a hit
carries no `CLEAN`.
```

- [ ] **Step 5: State the held-hit exception**

Find in `plugins/working-process/agents/propagation-auditor.md`:

```
The dispatcher confirms or dismisses each hit. A confirmed hit's fix is
licensed by the derivation itself — a recounted counter and an enumerated
missed consumer decide themselves — so hits never wait for the developer,
and a hit the dispatching session believes is wrong reaches the developer
rather than a silent dismissal. Write each derivation to stand alone: the
dispatcher acts on it, never on your confidence.
```

Replace with:

```
The dispatcher confirms or dismisses each hit. A confirmed hit's fix is
licensed by the derivation itself — a recounted counter and an enumerated
missed consumer decide themselves — so hits never wait for the developer,
with one exception: a hit of duty 10 whose fix needs a decision no
derivation settles, such as the task an uncovered decision needs where
the decision leaves a choice open, is held for the developer. A hit the
dispatching session believes is wrong reaches the developer rather than
a silent dismissal. Write each derivation to stand alone: the dispatcher
acts on it, never on your confidence.
```

- [ ] **Step 6: Add the out-of-bounds bullet**

Find in `plugins/working-process/agents/propagation-auditor.md`:

```
- Prose quality, naming taste, and style.
```

Replace with:

```
- Judging whether a task realizes the decision it cites, or whether the
  register lists every decision its spec makes — the plan-adversary's
  and the integrity auditor's.
- Prose quality, naming taste, and style.
```

- [ ] **Step 7: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 0`, `D 0`, `E 6`, `F 2`, `G 1`, `H 1`, `I 1`,
`J 1`, `K 1`, `L 11`, `M 1`, `N 2`, `O 1`.

`E 6` is the three summary lines of a plan's block plus the three of a
spec audited alone; the map lines are indented six spaces and do not
match. `L 11` is nine duties plus two.

- [ ] **Step 8: Commit**

```bash
git add plugins/working-process/agents/propagation-auditor.md
git commit -m "feat(working-process): decision coverage and table closure duties"
```

---

### Task 6: Workflow rule — the held coverage hit, the report lines, the delegating brief

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — step 4 of the
  flow, and the first three paragraphs of `### The propagation gate`.

**Interfaces:**
- Consumes: the `hit held` line (Task 3), the report lines (Task 5),
  the `## Plan annotations` section (Task 2), which the brief sentence
  points at by rule name.
- Produces: nothing a later task reads.

**Realizes:** D11.4, D12, D20, D26

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/workflow.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $F | grep -oF 'so hits never wait for the developer.' | wc -l)"
echo "B $(n $F | grep -oF 'so hits never wait for the developer, with one named exception' | wc -l)"
echo "C $(n $F | grep -oF 'No other duty' | wc -l)"
echo "D $(n $F | grep -oF 'A hit is a report, not a question' | wc -l)"
echo "E $(n $F | grep -oF 'A dismissed hit is a report, not a question' | wc -l)"
echo "F $(n $F | grep -oF 'A `decision-coverage:` or `table-closure:` line is neither a hit' | wc -l)"
echo "G $(n $F | grep -oF 'A brief that delegates plan-writing to a separate context' | wc -l)"
```

Expected: `A 1`, `B 0`, `C 0`, `D 1`, `E 0`, `F 0`, `G 0`.

- [ ] **Step 2: Name the delegating brief's duty in step 4**

Find in `plugins/working-process/rules/workflow.md`:

```
   Then write the
   implementation plan with superpowers:writing-plans when available;
   plans live in `docs/plans/`.
```

Replace with:

```
   Then write the
   implementation plan with superpowers:writing-plans when available;
   plans live in `docs/plans/`. A brief that delegates plan-writing to a
   separate context names the spec-plan-lifecycle rule and requires
   reading it before the plan is written: that rule carries the
   annotations a plan owes a registered design spec, and a separate
   context cannot count on it loading.
```

- [ ] **Step 3: Add the coverage exception to the gate**

Find in `plugins/working-process/rules/workflow.md`:

```
an integrity audit. A hit's fix is licensed by its own derivation — a
recounted counter and an enumerated missed call site decide
themselves — so hits never wait for the developer.
```

Replace with:

```
an integrity audit. A hit's fix is licensed by its own derivation — a
recounted counter and an enumerated missed call site decide
themselves — so hits never wait for the developer, with one named
exception, for the coverage duty's hits alone.

The two coverage hits — a registered decision no task cites, and a task
lacking its `**Realizes:**` line — are triaged by license. Where a task
already does the work and lacks only its annotation, the task's text
licenses adding the identifier. Where no task realizes the decision and
the decision's text settles every choice the missing task requires, the
decision licenses writing it, and the next round's brief names it among
the previous wave's fixes. Where writing the task needs a choice the
decision does not make, the hit is held: its question is that missing
decision, not the gap, which is already established. Any other hit of
the coverage duty is fixed where its derivation settles the fix and held
where it does not, as when breaking a `replaced by` cycle means choosing
which entry stands. No other duty's hit is ever held.

A held hit ends its gate episode and blocks the dispatch the gate
guards, as a held finding blocks a fresh round, and the session puts its
question to the developer. The answer lands where the decision belongs —
in the spec's register, or as the plan's `**Defers:**` line — and the
gate re-runs over the changed document and whatever depends on it, as a
fresh episode; the dispatch goes out once that episode passes. The
spec-plan-lifecycle rule defines the `hit held` line and its terminal
shapes.
```

- [ ] **Step 4: Admit the report's non-hit lines**

Find in `plugins/working-process/rules/workflow.md`:

```
belongs to the dispatcher who reads. The rule is stated here rather
than generalised, because `CLEAN` is this agent's token and no other
report carries one.
```

Replace with:

```
belongs to the dispatcher who reads. The rule is stated here rather
than generalised, because `CLEAN` is this agent's token and no other
report carries one. A `decision-coverage:` or `table-closure:` line is
neither a hit nor a breach of the token's position: the card writes
those lines on every run, clean ones included, between the hits and the
token.
```

- [ ] **Step 5: Narrow the report-not-question sentence**

Find in `plugins/working-process/rules/workflow.md`:

```
developer. A hit is a report, not a question, so it never enters the
held batch and never spends the round's one interruption — the
developer reads the dismissal and keeps their standing veto over it.
```

Replace with:

```
developer. A dismissed hit is a report, not a question, so it never
enters the held batch and never spends the round's one interruption —
the developer reads the dismissal and keeps their standing veto over it.
```

- [ ] **Step 6: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 1`, `C 1`, `D 0`, `E 1`, `F 1`, `G 1`.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): held coverage hits in the propagation gate"
```

---

### Task 7: Plan-adversary — dimension 6, realization of registered decisions

**Files:**
- Modify: `plugins/working-process/agents/plan-adversary.md` — a new
  dimension after dimension 5, before `## Output`.

**Interfaces:**
- Consumes: nothing from earlier tasks at runtime; the annotations it
  reads are those Task 2 defines.
- Produces: nothing a later task reads.

**Realizes:** D14, D30

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/agents/plan-adversary.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^### 6\. Realization of registered decisions$' $F)"
echo "B $(n $F | grep -oF 'realize it in full together' | wc -l)"
echo "D $(n $F | grep -oF 'the finding says the question is the developer' | wc -l)"
echo "C $(awk '/^### 5\./{f=1;print;next} f&&/^#/{exit} f' $F | shasum | cut -c1-7)"
```

Expected: `A 0`, `B 0`, `D 0`, `C c518b54`.

- [ ] **Step 2: Add the dimension**

Find in `plugins/working-process/agents/plan-adversary.md`:

```
named, the existing plan convention stands and this paragraph is silent.

## Output
```

Replace with:

```
named, the existing plan convention stands and this paragraph is silent.

### 6. Realization of registered decisions

Where a design spec the plan descends from sets `decisions: registered`,
read its decision register and the plan's `**Realizes:**` annotations in
the plan itself. The propagation audit has already established that
every counted decision is cited, and its report reaches the dispatcher,
not you. Judge each decision, never each site: one decision may span
several tasks and Global Constraints entries, so ask whether all the
sites citing it realize it in full together, and whether a cited
constraint actually binds the work it constrains. A decision realized
only in part — six rows of eight — is an Important finding whose
`origin` names `implementation-plan`. A deferral the developer ruled on
a `**Defers:**` line is not judged; a task that quietly depends on the
deferred decision anyway is a finding. Decisions inherited through a
`**Follows:**` line are taken as settled, since you read plans rather
than the code that realized them; a task that changes or undoes what an
inherited decision required is a finding against this plan. An
inherited citation of a decision the register has since withdrawn covers
nothing, and the withdrawal alone does not settle whether this plan
must undo what the predecessor built for it: judge the plan against the
decisions that stand, and where neither the withdrawal nor a successor
decision settles it, the finding says the question is the developer's.

## Output
```

- [ ] **Step 3: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `D 1`, `C c518b54` — dimension 5 is unchanged
(D28.2). The awk range stops at the next line
opening with `#`, which is dimension 6's heading after this task and
`## Output` before it.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/agents/plan-adversary.md
git commit -m "feat(working-process): plan-adversary judges realization of registered decisions"
```

---

### Task 8: Integrity auditor — the register as a declared rule

**Files:**
- Modify: `plugins/working-process/agents/integrity-auditor.md` — the
  last bullet of lens 1.

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: nothing a later task reads.

**Realizes:** D15

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/agents/integrity-auditor.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $F | grep -oF 'declares one such rule' | wc -l)"
echo "B $(grep -c '^### ' $F)"
```

Expected: `A 0`, `B 2`.

- [ ] **Step 2: Add the sentence**

Find in `plugins/working-process/agents/integrity-auditor.md`:

```
  field, and field by field for an entry the rule never claimed — the
  reverse direction is where the survivors hide.
```

Replace with:

```
  field, and field by field for an entry the rule never claimed — the
  reverse direction is where the survivors hide. A design spec carrying
  `decisions: registered` declares one such rule: its decision register
  lists every decision in the spec that needs realization. Check each
  entry against the text that argues it, and each decision the text
  makes against the register; a decision left only in a paragraph is a
  defect, and a rejected alternative without an entry is none.
```

- [ ] **Step 3: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 2` — the two lenses, since the task adds none.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/agents/integrity-auditor.md
git commit -m "feat(working-process): integrity auditor reads the decision register as a declared rule"
```

---

### Task 9: Propagation duties checklist — rows, anchor case, counters

**Files:**
- Modify: `plugins/working-process/rules/propagation-duties.md` — the
  opening paragraph, the second paragraph, the duty-2 row, and two new
  rows at the table's end.

**Interfaces:**
- Consumes: duty numbers 10 and 11 from Task 5.
- Produces: nothing a later task reads.

**Realizes:** D16.1, D16.2, D16.3

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/rules/propagation-duties.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $F | grep -oF 'nine duties fall due, keyed by the ten edits' | wc -l)"
echo "B $(n $F | grep -oF 'eleven duties fall due, keyed by the twelve edits' | wc -l)"
echo "C $(n $F | grep -oF 'walks the same nine as a gate' | wc -l)"
echo "D $(n $F | grep -oF 'walks the same eleven as a gate' | wc -l)"
echo "E $(n $F | grep -oF 'one an earlier task in the same document has already rewritten' | wc -l)"
echo "F $(grep -c '^| .* | 10 |$' $F)"
echo "G $(grep -c '^| .* | 11 |$' $F)"
echo "H $(grep -c '^| [a-z]' $F)"
```

Expected: `A 1`, `B 0`, `C 1`, `D 0`, `E 0`, `F 0`, `G 0`, `H 10`.

`H` counts the table's body rows — one per edit, each opening with a
lower-case verb; the header row opens with `You` and the separator with
`---`, so neither matches.

- [ ] **Step 2: Recount the opening paragraph**

Find in `plugins/working-process/rules/propagation-duties.md`:

```
Before a document goes to an expensive reader, nine duties fall due,
keyed by the ten edits that trigger them — one duty answers two
```

Replace with:

```
Before a document goes to an expensive reader, eleven duties fall due,
keyed by the twelve edits that trigger them — one duty answers two
```

- [ ] **Step 3: Recount the second paragraph**

Find in `plugins/working-process/rules/propagation-duties.md`:

```
When the `propagation-auditor` agent is available it walks the same
nine as a gate, and its card is their definition and keeps the
```

Replace with:

```
When the `propagation-auditor` agent is available it walks the same
eleven as a gate, and its card is their definition and keeps the
```

- [ ] **Step 4: Add the anchor case to the duty-2 row**

Find in `plugins/working-process/rules/propagation-duties.md`:

```
| prescribed a verbatim block | the anchor it targets — the text it replaces must exist in that file byte-exactly, and once | 2 |
```

Replace with:

```
| prescribed a verbatim block | the anchor it targets — the text it replaces must exist in that file byte-exactly, and once, and not be one an earlier task in the same document has already rewritten | 2 |
```

- [ ] **Step 5: Add the two rows**

Find in `plugins/working-process/rules/propagation-duties.md`:

```
technical designs its design specs name — none missing, none extra | 9 |
```

Replace with:

```
technical designs its design specs name — none missing, none extra | 9 |
| added, changed or withdrawn a register entry, or added, split or merged a plan task, or written a `**Defers:**` or `**Follows:**` line | the register against every `**Realizes:**` annotation, `**Defers:**` line and `**Follows:**` predecessor | 10 |
| written a column naming rows of another table | every name in it against that table | 11 |
```

- [ ] **Step 6: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 1`, `C 0`, `D 1`, `E 1`, `F 1`, `G 1`, `H 12`.

`H 12` is the twelve edits the recounted sentence claims, re-derived
from the rows (propagation duty 4), and eleven distinct duty numbers
stand in the last column:

```bash
grep '^| [a-z]' plugins/working-process/rules/propagation-duties.md | awk -F'|' '{print $(NF-1)}' | sort -u | wc -l
```

Expected: `11`.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/propagation-duties.md
git commit -m "feat(working-process): propagation duties checklist gains duties 10 and 11"
```

---

### Task 10: Grilling session — update the register as decisions land

**Files:**
- Modify: `plugins/working-process/skills/grilling-session/SKILL.md` —
  one bullet in `## Grilling mechanics`.

**Interfaces:**
- Consumes: the `## Decision register` heading from Task 1, cited by
  rule name.
- Produces: nothing a later task reads.

**Realizes:** D6

- [ ] **Step 1: Record the before values**

```bash
F=plugins/working-process/skills/grilling-session/SKILL.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $F | grep -oF 'decision register' | wc -l)"
```

Expected: `A 0`.

- [ ] **Step 2: Add the bullet**

Find in `plugins/working-process/skills/grilling-session/SKILL.md`:

```
- Apply glossary updates inline the moment a term settles — no batching.
```

Replace with:

```
- Apply glossary updates inline the moment a term settles — no batching.
- A spec carrying `decisions: registered` has a decision register,
  defined in the spec-plan-lifecycle rule: update it inline as each
  decision lands. A new decision takes the next free identifier, a
  sharpened one keeps its identifier, and a dropped one is withdrawn
  only on the developer's explicit decision.
```

- [ ] **Step 3: Verify**

Run the Step 1 command again.

Expected: `A 1`.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/skills/grilling-session/SKILL.md
git commit -m "feat(working-process): grilling session updates the decision register"
```

---

### Task 11: README and CHANGELOG

**Files:**
- Modify: `plugins/working-process/README.md` — the `plan-adversary` and
  `propagation-auditor` bullets, and a new section before
  `## Model selection`.
- Modify: `plugins/working-process/CHANGELOG.md` — bullets under
  `## Unreleased`.

**Interfaces:**
- Consumes: every name the earlier tasks produced.
- Produces: nothing a later task reads.

**Realizes:** none

- [ ] **Step 1: Record the before values**

```bash
R=plugins/working-process/README.md
C=plugins/working-process/CHANGELOG.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $R | grep -oF 'a clean audit reports the single line `CLEAN`' | wc -l)"
echo "B $(grep -c '^## Decision register$' $R)"
echo "C $(n $R | grep -oF 'realize it in full' | wc -l)"
echo "D $(n $R | grep -oF '`decision-coverage:` block' | wc -l)"
echo "E $(n $C | grep -oF 'decision register' | wc -l)"
echo "F $(grep -c '^## Unreleased$' $C)"
```

Expected: `A 1`, `B 0`, `C 0`, `D 0`, `E 0`, `F 1`.

- [ ] **Step 2: Update the plan-adversary bullet**

Find in `plugins/working-process/README.md`:

```
  come from `*-plan-review` checklist skills. Dispatched in the
  background, scaled to the plan's size and risk; the verdict arrives
  as a task notification and is stamped after relay.
```

Replace with:

```
  come from `*-plan-review` checklist skills. Where a design spec keeps
  a decision register, it also judges whether the tasks citing each
  decision realize it in full. Dispatched in the background, scaled to
  the plan's size and risk; the verdict arrives as a task notification
  and is stamped after relay.
```

- [ ] **Step 3: Update the propagation-auditor bullet**

Find in `plugins/working-process/README.md`:

```
  edit needs — re-derives every counter, and runs the document's own
  verification commands. Its
  unit is the hit: located, binary, and carrying the derivation that
  produced it; a clean audit reports the single line `CLEAN`. It grades
```

Replace with:

```
  edit needs — re-derives every counter, runs the document's own
  verification commands, derives a plan's decision coverage from its
  design specs' decision registers, and resolves the table relations
  the technical-design rule declares. Its unit is the hit: located,
  binary, and carrying the derivation that produced it. Every report
  also carries a `decision-coverage:` block per design spec and a
  `table-closure:` line per technical design, and a clean one ends in
  `CLEAN`. It grades
```

- [ ] **Step 4: Add the README section**

Find in `plugins/working-process/README.md`:

```
## Model selection
```

Replace with:

```
## Decision register

A design spec that sets `decisions: registered` carries a `## Decisions`
section listing, under stable identifiers (`D3`, `D4.1`), every
decision that needs realization. A plan descending from it marks each
task with `**Realizes:**` — the identifiers it realizes, or `none` —
and records deferrals and predecessor plans in a `## Deferrals and
predecessors` section. The propagation auditor derives the decision
coverage from the two lists, the plan-adversary judges whether the
citing tasks realize their decisions, and the integrity auditor checks
that the register lists every decision the spec makes. A spec without
the field is reported as not checked. The grammar lives in the
spec-plan-lifecycle rule.

## Model selection
```

- [ ] **Step 5: Add the CHANGELOG bullets**

Find in `plugins/working-process/CHANGELOG.md`:

```
- Run a rules re-sync after this update: the plan-adversary's `origin`
  values changed, and until the re-sync an installed workflow rule
  triages the new values by the old names.
```

Replace with:

```
- A design spec may carry a decision register: `decisions: registered`
  and a `## Decisions` section listing, under stable identifiers, every
  decision that needs realization, with `withdrawn` as its one state
  token.
- A plan descending from a registered spec marks every task with
  `**Realizes:**`, and records deferrals and predecessor plans in a
  `## Deferrals and predecessors` section.
- The propagation auditor gains two duties: decision coverage, reported
  in a `decision-coverage:` block per design spec, and table closure
  over the relations the technical-design rule declares, reported in a
  `table-closure:` line. A clean report carries those lines before
  `CLEAN`.
- A coverage hit whose fix needs a decision the spec does not make is
  held for the developer as a `hit held` gate line with three terminal
  shapes, and the Unfinished review-loop ledger command finds it.
- The plan-adversary judges whether the tasks citing a decision realize
  it in full, and the integrity auditor checks that the register lists
  every decision its spec makes.
- The propagation duties checklist gains rows for the two duties and
  the duty-2 anchor an earlier task has already rewritten.
- Run a rules re-sync after this update: the plan-adversary's `origin`
  values changed, and until the re-sync an installed workflow rule
  triages the new values by the old names. The re-sync also installs
  the decision register, the plan annotations and the held gate line,
  which the updated agents expect.
```

- [ ] **Step 6: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 1`, `C 1`, `D 1`, `E 2`, `F 1`.

`E 2` is the first new bullet and the widened re-sync bullet.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/README.md plugins/working-process/CHANGELOG.md
git commit -m "docs(working-process): README and changelog for plan coverage"
```

---

### Task 12: Final verification

**Files:**
- Test: the whole plugin, the glossary, and this plan.

**Interfaces:**
- Consumes: every task above.
- Produces: nothing.

**Realizes:** none

- [ ] **Step 1: Validate the marketplace and the plugin**

```bash
claude plugin validate .
claude plugin validate plugins/working-process
```

Expected: both pass. Validation reads manifests and component
frontmatter, never `rules/`, so it proves the card's `description:`
still parses and nothing about the rules.

- [ ] **Step 2: Check what must not change**

```bash
git diff --stat develop -- plugins/working-process/agents/architect.md | tail -n 1
awk '/^### 5\./{f=1;print;next} f&&/^#/{exit} f' plugins/working-process/agents/plan-adversary.md | shasum | cut -c1-7
```

Expected: the first command prints nothing (D28.1); the second prints
`c518b54`, the hash Task 7 recorded (D28.2).

- [ ] **Step 3: Check the glossary entries stand**

```bash
G=docs/domain/glossary.md
echo "A $(grep -c '^\*\*Decision register\*\*:$' $G)"
echo "B $(grep -c '^\*\*Decision coverage\*\*:$' $G)"
echo "C $(tr -s '[:space:]' ' ' < $G | grep -oF 'a held hit it authorizes closes only once the gate has rechecked the fix' | wc -l)"
```

Expected: `A 1`, `B 1`, `C 1`.

- [ ] **Step 4: Check line width of the changed prose**

```bash
for f in rules/spec-plan-lifecycle.md rules/technical-design.md rules/workflow.md \
  rules/propagation-duties.md agents/propagation-auditor.md agents/plan-adversary.md \
  agents/integrity-auditor.md skills/grilling-session/SKILL.md README.md CHANGELOG.md; do
  git diff -U0 develop -- plugins/working-process/$f | grep '^+[^+]' | cut -c2- \
    | LC_ALL=C.UTF-8 awk -v f=$f 'length > 72 && !/^ {4}/ && !/^\|/ && !/^description:/ && !/^ {6}/ && !/   # / {print f": "$0}'
done
```

Expected: no output. Indented grammar examples, table rows, the
one-line `description:` and the lifecycle rule's commented frontmatter
lines, whose neighbours already run past the width, are exempt.

- [ ] **Step 5: Derive this plan's decision coverage**

The installed auditor has no duty 10 yet, so derive it here:

```bash
python3 - <<'EOF'
import re
spec = open('docs/specs/2026-09-25-plan-coverage-design.md').read()
reg = spec.split('\n## Decisions\n', 1)[1].split('\n## ', 1)[0]
ids = re.findall(r'^\s*- \*\*(D\d+(?:\.\d+)?)\*\*', reg, re.M)
groups = {i.split('.')[0] for i in ids if '.' in i}
leaves = [i for i in ids if i not in groups]
plan = open('docs/plans/2026-09-26-plan-coverage.md').read()
cited = set()
for v in re.findall(r'^(?:- )?\*\*Realizes:\*\* (.+)$', plan, re.M):
    v = v.split(' — ')[0]
    cited |= {x.strip() for x in v.split(',') if x.strip() != 'none'}
print(len(leaves), 'leaves;', len(set(leaves) & cited), 'cited;',
      'uncovered', sorted(set(leaves) - cited),
      'unknown', sorted(cited - set(leaves)))
EOF
```

Expected: `N leaves; N cited; uncovered [] unknown []`, the two counts
equal. `N` read 39 when this plan was written; a register edit since
changes it, and the line is right whatever `N` is.

- [ ] **Step 6: Carry the count forward**

No commit. Write down `N`; Task 13 expects it.

---

### Task 13: Run the changed auditor card on controlled cases

**Files:**
- Test: a fixture project outside the repository, and the evidence file
  `.claude/working-process/2026-09-26-plan-coverage/task-13-auditor-runs.md`.

**Interfaces:**
- Consumes: every task above, and `N` from Task 12 Step 5.
- Produces: nothing.

**Realizes:** none

The greps prove the text landed; only a run proves the card detects what
it claims. The run is scoped to duties 10 and 11, the two this plan
adds: they read documents and nothing else, so the auditor needs no
shell beyond resolving the repo root, and it never executes the
commands this plan quotes. Four cases: this plan, which must come out
fully covered although it quotes `**Defers:** D6` in a code block while
citing D6; a copy with one annotation removed, which must report exactly
that gap; the spec alone; and a technical design with one wrong
reference.

A tool denial, a file the auditor could not read, or a report missing
its expected lines fails the test. None of them is a clean result.

- [ ] **Step 1: Build the fixture project**

The fixture holds the inputs the two duties read and nothing more. The
card and the rule copies it reads through `${CLAUDE_PLUGIN_ROOT}` come
from the changed checkout; the installed user-scope rules still load in
the inner session, and the expectations rest on the card reading the
plugin's copy, as Deviation 8 prescribes. `git init` is there because
the card resolves the repo root with `git rev-parse --show-toplevel`.

```bash
R=$(git rev-parse --show-toplevel)
W=${TMPDIR:-/tmp}/plan-coverage-dogfood
command rm -rf "$W"
mkdir -p "$W/docs/specs" "$W/docs/plans" "$W/docs/domain" "$W/docs/technical-designs"
command cp -f "$R/docs/specs/2026-09-25-plan-coverage-design.md" "$W/docs/specs/"
command cp -f "$R/docs/plans/2026-09-26-plan-coverage.md" "$W/docs/plans/"
command cp -f "$R/docs/domain/glossary.md" "$W/docs/domain/"
sed 's/^\*\*Realizes:\*\* D15$/**Realizes:** none/' \
  "$W/docs/plans/2026-09-26-plan-coverage.md" > "$W/docs/plans/fixture-uncovered.md"
grep -c '^\*\*Realizes:\*\* D15$' "$W/docs/plans/fixture-uncovered.md" || true
```

Expected: `0` — Task 8's only annotation is gone from the copy, so D15
is cited nowhere else. `grep -c` exits 1 on a zero count, hence the
`|| true`.

Then write the table-closure pair, whose Contracts row names a part
`reder` that Parts does not carry, and commit the fixture:

```bash
W=${TMPDIR:-/tmp}/plan-coverage-dogfood
cat > "$W/docs/specs/fixture-design.md" <<'EOF'
---
ticket: none
date: 2026-09-26
status: draft
technical-design: ../technical-designs/fixture-technical-design.md
---

# Fixture

A fixture design spec for the table-closure duty.
EOF
cat > "$W/docs/technical-designs/fixture-technical-design.md" <<'EOF'
---
ticket: none
date: 2026-09-26
status: draft
spec: ../specs/fixture-design.md
---

# Fixture technical design

## Scope

The fixture spec's single behaviour.

## Parts

| part | kind | change | placement | owns | deliberately excludes |
|---|---|---|---|---|---|
| reader | rule | new | rules/ | reading | writing |
| writer | rule | new | rules/ | writing | reading |

## Contracts

| producer → consumer | crosses | guarantee | breaks when | check |
|---|---|---|---|---|
| writer → reder | file | a record | the file is missing | grep |

## State

| record | home | written by | read by | lifecycle | visible through |
|---|---|---|---|---|---|
| log | docs/ | writer | reader | per run | grep |

## Failure and repetition

Not applicable, because the fixture never runs.

## Cuts not taken

Not applicable, because nothing was cut.

## Open questions

None.
EOF
(cd "$W" && git init -q && git add -A \
  && git -c user.name=fixture -c user.email=fixture@example.invalid commit -qm fixture)
```

- [ ] **Step 2: Run the four audits — ask the developer first**

A `--plugin-dir` session collides with the installed plugin of the same
name, so the script disables it for the run and restores the state it
found, whatever the run prints. Disabling changes the developer's own
configuration: ask before running.

The guard is the inner session's permission set, not a list of allowed
tools, because `--allowedTools` only pre-approves and never forbids. The
developer's user settings stay in the run: `--setting-sources project`
would keep them out, but it also drops the agents `--plugin-dir` loads,
so the dispatch finds no auditor (measured on 2026-09-26, one flag at a
time). Their one risky allow rule is `Bash(claude plugin *)`, and
`--disallowedTools "Bash(claude *)"` denies that family, since a deny
rule wins over an allow rule. The harness itself pre-approves read-only
commands; in print mode every other prompt is denied, writes and
compound commands among them. `--tools` narrows the built-in set to
what the dispatch needs, and `--add-dir` admits the plugin directory the
card reads its rules from. These are the run's real limits: they block
the commands this plan quotes that change state, `claude plugin
disable` and `rm -rf` among them, and they isolate nothing else from
the developer's settings.

Each run's full event stream is kept, so the evidence is the dispatch
itself rather than what the outer session chose to print.

```bash
R=$(git rev-parse --show-toplevel)
W=${TMPDIR:-/tmp}/plan-coverage-dogfood
was=$(claude plugin list | grep -A3 'working-process@missing-bits' | grep -c 'Status: .*enabled')
restore() { [ "$was" = 1 ] && claude plugin enable working-process; }
trap restore EXIT
[ "$was" = 1 ] && claude plugin disable working-process
k=0
for f in docs/plans/2026-09-26-plan-coverage.md docs/plans/fixture-uncovered.md \
  docs/specs/2026-09-25-plan-coverage-design.md \
  docs/technical-designs/fixture-technical-design.md; do
  k=$((k+1))
  (cd "$W" && claude -p --plugin-dir "$R/plugins/working-process" \
    --add-dir "$R/plugins/working-process" \
    --disallowedTools "Bash(claude *)" \
    --tools "Agent,Read,Grep,Glob,Bash" \
    --allowedTools "Bash(git rev-parse:*)" "Bash(python3 */scripts/decision-coverage.py *)" \
    --output-format stream-json --verbose \
    "Dispatch the working-process:propagation-auditor agent on the haiku model over $f, in the foreground, and wait for its report. Tell it to walk only duties 10 and 11 of its card and to report in the card's output shape.") \
    > "$W/run-$k.jsonl" 2> "$W/run-$k.err"
  echo "$f" > "$W/run-$k.target"
done
restore; trap - EXIT
claude plugin list | grep -A3 'working-process@missing-bits' | grep 'Status:'
```

Expected: the last line shows the status the plugin had before the run.

- [ ] **Step 3: Extract each report and compare it with its expectation**

The report comes from the agent dispatch inside each stream, not from
the outer session's text. The card runs in the background by default,
so the dispatch's own tool result may only acknowledge the launch: the
extractor takes the report from the dispatched agent's last message,
marked by its `parent_tool_use_id`, and falls back to the tool result.
It names the dispatch it found, its agent type and model, every tool
result that reports a denial, and the report:

```bash
W=${TMPDIR:-/tmp}/plan-coverage-dogfood
cat > "$W/extract.py" <<'EOF'
import json, sys
calls, report, own, denials = {}, None, None, []
for line in open(sys.argv[1]):
    try:
        e = json.loads(line)
    except ValueError:
        continue
    m = e.get('message')
    m = m if isinstance(m, dict) else {}
    content = m.get('content')
    if e.get('parent_tool_use_id') in calls and m.get('role') == 'assistant':
        text = ' '.join(c.get('text', '') for c in content or [] if isinstance(c, dict))
        if text.strip():
            own = text
    for c in content if isinstance(content, list) else []:
        if c.get('type') == 'tool_use' and c.get('name') in ('Agent', 'Task'):
            i = c.get('input') or {}
            if i.get('subagent_type') == 'working-process:propagation-auditor':
                calls[c['id']] = i.get('model')
        if c.get('type') == 'tool_result':
            r = c.get('content')
            txt = r if isinstance(r, str) else ' '.join(x.get('text', '') for x in r or [])
            if c.get('is_error') or 'denied' in txt.lower():
                denials.append(txt[:200])
            if c.get('tool_use_id') in calls:
                report = txt
print('dispatches:', calls)
print('denials:', denials)
print('report:')
print(own or report)
EOF
for k in 1 2 3 4; do
  echo "##### $(cat "$W/run-$k.target")"
  python3 "$W/extract.py" "$W/run-$k.jsonl"
done | tee "$W/reports.txt"
```

For every run, expected: exactly one dispatch, of
`working-process:propagation-auditor` with model `haiku`, and a report.
No dispatch or no report fails the test, and the stream stays for
inspection. A denial fails it too, unless the stream shows the auditor
completing the same operation through an allowed alternative — the
denied `cat` followed by a `Read` of that file — since a complete report
does not prove the check behind it ran. The event shapes are the CLI's own; an
extractor that finds nothing in a stream that plainly holds a dispatch
is a test defect to fix, never a pass.

`CLEAN` here means no hit in duties 10 and 11 — the only checks that
ran. With `N` from Task 12 Step 5:

- **this plan** — a summary line beginning
  `decision-coverage: ../specs/2026-09-25-plan-coverage-design.md N/N covered`,
  `N` map lines under it, no hit, and `CLEAN` last. No hit names
  `**Defers:**` or D6: the quoted grammar instantiates nothing.
- **the uncovered copy** — a hit naming D15, a summary line with
  `N-1/N covered` and `uncovered [D15]`, a map line `D15 → —`, and no
  `CLEAN`.
- **the spec alone** — one `decision-coverage:` line ending
  `register well formed`, and `CLEAN`.
- **the technical design** — a hit naming `reder`, the line
  `table-closure: <document path> 3 relations checked`, and no `CLEAN`.

Every report opens with a `model:` line naming the haiku family. A
report that departs from its expectation, or that mentions a denied tool
or an unread file, fails the test: report it to the developer with the
report text, and do not adjust the expectation to fit.

- [ ] **Step 4: Keep the evidence, clean up**

```bash
R=$(git rev-parse --show-toplevel)
W=${TMPDIR:-/tmp}/plan-coverage-dogfood
D="$R/.claude/working-process/2026-09-26-plan-coverage"
{ echo '# Task 13 — auditor runs on controlled cases, 2026-09-26'; echo; cat "$W/reports.txt"; } \
  > "$D/task-13-auditor-runs.md"
mkdir -p "$D/task-13-streams"
command cp -f "$W"/run-*.jsonl "$W"/run-*.err "$D/task-13-streams/"
command rm -rf "$W"
```

The file and the streams beside it are the test's evidence, not a
dispatch record: audits write none. It lives in the store, whose `*` `.gitignore` keeps it local.

- [ ] **Step 5: Report**

No commit. Report the results of Task 12 and of this task to the
developer, and leave `sync-rules`, the version and both documents'
`status` to them.

---

### Task 14: The coverage derivation script and its tests

**Files:**
- Create: `plugins/working-process/scripts/decision-coverage.py`
- Create: `tests/working-process/test_decision_coverage.py`

**Interfaces:**
- Consumes: the grammar Tasks 1 and 2 wrote into
  `rules/spec-plan-lifecycle.md` (*Decision register*, *Plan
  annotations*) and the report shapes Task 5 wrote into the auditor card
  (duty 10 and `## Output`).
- Produces: the command
  `python3 plugins/working-process/scripts/decision-coverage.py <document>`,
  which Task 15's card text runs as
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/decision-coverage.py <document>`.

**Realizes:** D31

This task is code, so its steps are test-driven rather than
Find/Replace. The contract below is the requirement; the tests encode
it, and the script is written to pass them. Python 3.9 or later, the
standard library only, no third-party package.

**The contract.**

- Invocation: one positional argument, the path of a plan or a design
  spec, relative to the working directory or absolute. Paths the
  document names (`spec:`, `**Follows:**`) resolve against the
  document's own directory. Output goes to stdout; exit code 0 whenever
  the derivation ran, hits or not; 2 on a usage error or an unreadable
  file, with a one-line message on stderr.
- A plan is a document whose frontmatter carries `spec:`; a design spec
  is one that does not. Frontmatter is the block between the `---` on
  the first line and the next `---`. `spec:` is a single path or an
  inline list `[a, b]`.
- Fenced code blocks — a line opening with three backticks toggles a
  fence — are skipped everywhere: nothing inside one is an entry, an
  annotation or a heading.
- **Register** (per spec): the `decisions:` field absent → the block
  line `decision-coverage: <spec> not checked — no decision register`
  and nothing else for that spec. Any value other than `registered` → a
  hit and `not counted — malformed register`. Otherwise the register is
  the `## Decisions` section, up to the next line opening `## `; no such
  section → a hit and `not counted`. An entry is a line matching
  `^(\s*)- \*\*(D\d+(?:\.\d+)?)\*\*`; indentation of two or more spaces
  marks a child. Its identity paragraph is that line plus the
  continuation lines up to a blank line, the next line opening a list
  item, or the section's end, joined with single spaces. Malformed, each
  a hit: a numbered-list entry (`^\s*\d+\.\s+\*\*D`), a duplicate
  identifier, a child `D<n>.<m>` not nested under entry `D<n>` or whose
  parent does not exist, a group carrying a state token, a state token
  not matching the grammar, a `replaced by` naming a missing
  identifier, itself or a group, and a `replaced by` chain closing a
  cycle. Any malformation → `not counted` for that spec, and its other
  checks stop.
- **State token**: the first segment of the identity paragraph that
  begins with `withdrawn` right after a full stop and whitespace; it
  runs to the paragraph's end and must match
  `withdrawn <reason>, ruling: <YYYY-MM-DD>[; replaced by <id>]`,
  optionally ending with a full stop. A group is an entry with children;
  a leaf is every other entry.
- **Plan annotations**: tasks are `### Task <n>` headings; a task's
  `**Realizes:**` line is a line opening `**Realizes:** ` between its
  heading and the next line opening `#`; its value is `none` or a
  comma-separated list. Global Constraints entries are lines opening
  `- **Realizes:** ` inside `## Global Constraints`; the identifiers
  run up to the first ` — `. `**Defers:** <id> — <why>; ruling: <date>`
  and `**Follows:** <path>` lines count only inside
  `## Deferrals and predecessors`.
- **Qualification**: where `spec:` names two or more specs, every
  identifier is written `<spec path as spec: writes it>#<id>`; a bare
  one is a hit. Each spec's pass reads only the identifiers qualified
  with its path; a `**Defers:**` line for another spec is out of scope
  there.
- **Steps**, per registered spec, in order — the duty's steps 3 to 7:
  check each `**Follows:**` line (missing file, no shared spec, or
  `status` other than `implemented` → a hit, and the line lends
  nothing); collect the cited set from local annotations and from each
  accepted predecessor's annotations for the specs both name (an
  identifier cited locally and inherited counts as local); a cited
  withdrawn identifier, group or undefined identifier is a hit, except
  an inherited citation of an identifier withdrawn since, which is
  skipped and listed; check each `**Defers:**` line (undefined,
  withdrawn, group, or in the cited set → a hit, and it subtracts
  nothing); the counted set is the leaves not withdrawn less the
  accepted deferrals; every counted identifier the cited set lacks is a
  hit. A task with no `**Realizes:**` line, in a plan whose `spec:`
  names a registered spec, is a hit.
- **A design spec audited alone** runs the register checks only and
  prints `register well formed`, `not counted — malformed register` or
  `not checked — no decision register`.
- **Output**, in this order: every hit, one line each,
  `<path>:<line> — <claim> — derivation: decision-coverage.py, <step>`;
  then, per spec in `spec:` order, its block, exactly as the auditor
  card's `## Output` shows it:

      decision-coverage: <spec> <c>/<n> covered; inherited [..]; deferred [..]; uncovered [..]
        <id> → <site>, <site>
        withdrawn since: <id> ← <predecessor path> (<site>)

  `<spec>` is the path as `spec:` writes it. Map lines follow the
  register's order, one per counted identifier; an uncovered one maps to
  `—`. A site is `Task <n>`, or
  `Global Constraints, line <line>: "<words>"` where `<words>` are the
  first six words after the annotation clause with `**` and backticks
  removed, or `<predecessor path> (<site>)`. Local sites come before
  inherited ones. Every slot is always present, an empty one `[]`, and
  identifiers inside slots follow register order. The script prints no
  `CLEAN`: other duties may still hit.

- [ ] **Step 1: Write the failing tests**

`tests/working-process/test_decision_coverage.py`, `unittest`, each
test building its documents in a `tempfile.TemporaryDirectory()` and
running the script with `subprocess.run([sys.executable, SCRIPT,
path], capture_output=True, text=True)`, where `SCRIPT` is resolved
from the test file's location. One test per case, asserting the exact
lines named:

1. A registered spec with `D1`, `D2` and a group `D3` with `D3.1`,
   `D3.2`; a plan whose three tasks cite `D1`, `D3.1`, `D3.2` and whose
   Global Constraints entry `- **Realizes:** D2 — **No code** anywhere.`
   → `decision-coverage: ../specs/s.md 4/4 covered; inherited []; deferred []; uncovered []`,
   map line `  D2 → Global Constraints, line <n>: "No code anywhere."`
   with `<n>` that entry's line, and no hit line.
2. The same plan with one task's `D3.1` replaced by `none` → a hit
   naming `D3.1`, `3/4 covered`, `uncovered [D3.1]`, `  D3.1 → —`.
3. A plan quoting `**Realizes:** D9` and `**Defers:** D1 — x; ruling: 2026-01-01`
   inside a fenced block, while citing `D1` in a task → no hit, and no
   `D9` anywhere in the output.
4. A task with no `**Realizes:**` line → a hit naming that task.
5. A register entry `D2` ending
   `. withdrawn superseded by D1. See notes, ruling: 2026-01-01; replaced by D1.`
   → `D2` absent from the counted set, a plan citing `D2` gets a hit.
6. Malformed registers, one test each: a duplicate `D1`; a child `D4.1`
   with no `D4`; a group carrying a token; `replaced by` naming itself;
   `D1 → D2 → D1` as a cycle; a numbered list → each a hit and
   `not counted — malformed register`, no map.
7. A spec with no `decisions:` → `not checked — no decision register`,
   and a plan descending from it alone needs no `**Realizes:**` lines.
8. A plan whose `spec:` names two registered specs, citing a bare `D1`
   → a hit on the bare identifier.
9. A valid `**Defers:** D2 — later; ruling: 2026-01-01` → `D2` out of
   the counted set and in `deferred [D2]`; a `**Defers:**` naming a
   cited identifier → a hit, and the identifier still counted.
10. `**Follows:** ../plans/p0.md` naming an implemented predecessor that
    cites `D2` → `D2` covered, `inherited [D2]`,
    `  D2 → ../plans/p0.md (Task 1)`; the predecessor at `status: draft`
    → a hit and `D2` uncovered; the predecessor citing a `D2` the
    register has since withdrawn → a `withdrawn since:` line and no hit.
11. A registered spec audited alone → `register well formed`; with a
    duplicate → `not counted — malformed register`.
12. The repository's own documents: the script over
    `docs/plans/2026-09-26-plan-coverage.md` prints no hit and a summary
    whose two counts equal the register's leaves; over
    `docs/specs/2026-09-25-plan-coverage-design.md`, `register well formed`.

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3 -m unittest discover -s tests/working-process -v`
Expected: every test fails or errors, the script not existing yet.

- [ ] **Step 3: Write the script**

`plugins/working-process/scripts/decision-coverage.py`, executable,
opening with `#!/usr/bin/env python3` and a docstring naming the
contract's home — the spec-plan-lifecycle rule's *Decision register*
and *Plan annotations*, and duty 10 of the propagation-auditor card.
Match the contract above; add nothing it does not name.

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3 -m unittest discover -s tests/working-process -v`
Expected: every test passes, output pristine.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/scripts/decision-coverage.py tests/working-process/test_decision_coverage.py
git commit -m "feat(working-process): decision coverage derivation script"
```

---

### Task 15: The auditor runs the script

**Files:**
- Modify: `plugins/working-process/agents/propagation-auditor.md` — the
  opening paragraph of duty 10.
- Modify: `plugins/working-process/README.md` — the `## Decision
  register` section.
- Modify: `plugins/working-process/CHANGELOG.md` — one bullet under
  `## Unreleased`.

**Interfaces:**
- Consumes: the command Task 14 produces.
- Produces: nothing a later task reads.

**Realizes:** D31

- [ ] **Step 1: Record the before values**

```bash
C=plugins/working-process/agents/propagation-auditor.md
R=plugins/working-process/README.md
L=plugins/working-process/CHANGELOG.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $C | grep -oF 'scripts/decision-coverage.py <document>' | wc -l)"
echo "B $(n $C | grep -oF 'never walk it by hand' | wc -l)"
echo "C $(n $R | grep -oF 'scripts/decision-coverage.py' | wc -l)"
echo "D $(n $L | grep -oF 'scripts/decision-coverage.py' | wc -l)"
```

Expected: `A 0`, `B 0`, `C 0`, `D 0`.

- [ ] **Step 2: Duty 10 runs the script**

Find in `plugins/working-process/agents/propagation-auditor.md`:

```
place *Plan annotations* gives it: a code block or a quoted example
describes the grammar. For each spec the plan's `spec:` names:
```

Replace with:

```
place *Plan annotations* gives it: a code block or a quoted example
describes the grammar.

Run the derivation, never walk it by hand:
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/decision-coverage.py <document>`,
once per audited document, as a single command from the repository
root. It performs the steps below and prints this duty's hits and
`decision-coverage:` lines in the report's shapes; copy its output into
your report unchanged, neither recounting nor reordering it. If it exits
non-zero, or you cannot run it, report that as a hit naming the command
and its message, and write no `decision-coverage:` line — never derive
the sets yourself. The steps below define what the script does. For
each spec the plan's `spec:` names:
```

- [ ] **Step 3: The README names the script**

Find in `plugins/working-process/README.md`:

```
the field is reported as not checked. The grammar lives in the
spec-plan-lifecycle rule.
```

Replace with:

```
the field is reported as not checked. The grammar lives in the
spec-plan-lifecycle rule. The auditor derives the decision coverage by
running `scripts/decision-coverage.py` with `python3`, so a session
that asks before running a command asks once for it.
```

- [ ] **Step 4: The CHANGELOG names the script**

Find in `plugins/working-process/CHANGELOG.md`:

```
- The propagation duties checklist gains rows for the two duties and
  the duty-2 anchor an earlier task has already rewritten.
```

Replace with:

```
- The propagation duties checklist gains rows for the two duties and
  the duty-2 anchor an earlier task has already rewritten.
- The decision coverage is derived by `scripts/decision-coverage.py`,
  which the auditor runs with `python3` (3.9 or later, standard library
  only), rather than by the auditor walking the steps itself.
```

- [ ] **Step 5: Verify**

Run the Step 1 command again, then `claude plugin validate
plugins/working-process`.

Expected: `A 1`, `B 1`, `C 1`, `D 1`, and validation passes.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/agents/propagation-auditor.md plugins/working-process/README.md plugins/working-process/CHANGELOG.md
git commit -m "feat(working-process): the propagation auditor runs the coverage script"
```

---

### Task 16: Run Task 13 twice more on the script-backed card

**Files:**
- Test: the Task 13 fixture, and the evidence files
  `.claude/working-process/2026-09-26-plan-coverage/task-13-auditor-runs-<k>.md`.

**Interfaces:**
- Consumes: Tasks 14 and 15, and Task 13's steps.
- Produces: nothing.

**Realizes:** none

- [ ] **Step 1: Run Task 13 in full, twice**

Run Task 13's Steps 1–4 two times in a row, asking the developer once
before the first — the plugin is disabled and restored around each.
After each run, rename the evidence file and streams directory to carry
the run's number, `-2` and `-3`, so neither overwrites the other.

- [ ] **Step 2: Compare**

Expected: both runs meet every expectation of Task 13 Step 3 with the
numbers exact — `N/N` on this plan, `N-1/N` with `uncovered [D15]` on
the copy, `register well formed` on the spec, `3 relations checked`
and the `reder` hit on the technical design — and each report's
`decision-coverage:` lines equal the script's own output over the same
document, run directly. Two agreeing runs are the acceptance criterion,
not a statistical proof of reliability; a single departure fails the
task and goes to the developer with both reports.

- [ ] **Step 3: Report**

No commit. Report both runs to the developer.

## Review rounds

### 2026-09-26 — plan-adversary, fable 5.1, blocking (round 1, full-document)

- fixed 2026-09-26 — [Important] D13.2 realized only in part: the spec's leaf widens the Unfinished review-loop ledger entry's name, description and command, and Task 3 keeps the name; ruling: 2026-09-26; option (a) — the spec's register contradicted its argued section, and D13.2 now keeps the name: the line sits in `../specs/2026-09-25-plan-coverage-design.md` under `### Loop closed — 2026-09-26`
- fixed 2026-09-26 — [Important] duties 10 and 11 send the auditor to rules by name with no path, while Task 6 states a separate context cannot count on the rule loading; license: Task 6's Replace ("a separate context cannot count on it loading") and the `${CLAUDE_PLUGIN_ROOT}` precedent in `plan-adversary.md`; deviation: *Deviations from the spec* 8 — both duties read the plugin's copy always, not only when the installed rule is absent, since an installed copy may lag the card
- fixed 2026-09-26 — [Important] Task 3 leaves *Gate lines* opening with "writes two shapes of its own" and "Both are written at gate time" beside the new held shape; license: propagation duty 4 and Deviation 3's own reason; Task 3 Step 4 rewrites the opener, Step 5 turns "Both" into "Each", checks M–N added
- fixed 2026-09-26 — [Important] the changed auditor card ships with no named test that runs it; ruling: 2026-09-26; new Task 13 runs the card from the checkout on four targets — this plan, a copy missing D15, the spec alone, a technical design with a wrong reference — with the expected count `N` derived by Task 12 rather than fixed
- fixed 2026-09-26 — [Minor] Task 3 Step 3 routes a gate-licensed register edit to the fix heading at whatever closing verdict, while a review-licensed fix on a `concerns (resolved)` document joins the resolution note; license: D29 ("where the spec's loop is closed, under the cross-document fix heading"); the sentence now states the divergence and its reason, check P added
- fixed 2026-09-26 — [Minor] "A plan with no `## Review rounds` section gains one", while a held line can land in a design spec audited alone; ruling: 2026-09-26; "A document", recorded as Deviation 9, check O added
- fixed 2026-09-26 — [Minor] duty 10 has no guard against a document quoting the annotation grammar, and this plan quotes `**Defers:** D6` while citing D6; ruling: 2026-09-26; Task 2 states that a line counts only at its defined place — Global Constraints entries included — and that a code block or quoted example instantiates nothing, and duty 10 reads lines only there; Deviation 10, checks J (Task 2) and O (Task 5) added, and Task 13 runs the case
- fixed 2026-09-26 — [Minor] the commit constraint "no trailers, `Co-Authored-By` included" reads two ways; license: the developer's commit rule (`.claude/rules/commit-messages.md`); reworded to "no body and no trailer, not even `Co-Authored-By`"
- signal 2026-09-26 — another round pays only after the four Important findings land; it can be diff-scoped, and the leftovers were one fix wave plus one batch of held questions, not a fresh full read

### 2026-09-26 — plan-adversary, fable 5.1, blocking (round 2, diff-scoped)

- fixed 2026-09-26 — [Important] Task 13's `claude -p` runs grant the auditor no Bash, so duty 7's commands are denied and a clean expectation certifies a run that never simulated; ruling: 2026-09-26; option (b) — the run walks duties 10 and 11 only, the inner session gets `--allowedTools "Agent Read Grep Glob Bash(git rev-parse:*)"`, `CLEAN` there means no hit in those two duties, and a tool denial, an unread file or a missing expected line fails the test; deviation: Task 13 — none of the suggested grants, since a broad Bash grant would let the auditor execute the commands this plan quotes
- fixed 2026-09-26 — [Important] Task 13's fixture has no `develop` ref and no history, so the plan's own `git diff … develop` commands and the commit Deviation 6 names fail there; ruling: 2026-09-26; with duties 6 and 7 out of the run, the fixture carries only the inputs duties 10 and 11 read, plus `git init` for the card's `git rev-parse`; the `git archive develop` step is gone
- fixed 2026-09-26 — [Minor] Task 13 claims the rules come from the checkout, while the installed user-scope rules still load, and the project-scope copy only doubles them; license: Deviation 8 (the card reads `${CLAUDE_PLUGIN_ROOT}/rules/`); the project-scope copy is dropped and Step 1 says the user-scope rules still load and the expectations rest on the plugin's copy
- fixed 2026-09-26 — [Minor] Task 13's evidence file is called a dispatch record and given its header, though audits write none; license: glossary **Dispatch record** and the workflow rule ("Audits write none"); the file is `task-13-auditor-runs.md`, called the test's evidence, with a plain heading
- fixed 2026-09-26 — [Minor] Task 13's plugin re-enable runs only on the success path; ruling: 2026-09-26; the script records the plugin's status before the run and restores exactly that state from an `EXIT` trap, then prints the status to compare
- fixed 2026-09-26 — [Minor] Task 12 Step 6 says `N` is not fixed while Step 5 fixes it at 39; license: Step 6's own sentence; Step 5 now expects the two counts equal, noting 39 as the value at writing
- signal 2026-09-26 — another round pays only after the two Important findings land; it can stay diff-scoped and narrow, then the confirming full-document round follows

### 2026-09-26 — plan-adversary, fable 5.1, concerns (round 3, full-document)

- fixed 2026-09-26 — [Minor] the new `hit held` state has an anchor and an owner but no reader at the consumption gate: the lifecycle rule's backstop sentence blocks plan-writing and implementation on open `held` lines alone, and no step of Task 3 widens it; ruling: 2026-09-26; option (a) — new Task 3 Step 9 adds `hit held` gate lines to the backstop, blocking until the gate re-runs and rewrites the line to a terminal shape, a closed gate line blocking nothing; Deviation 11, check Q added
- fixed 2026-09-26 — [Minor] Task 13 compares "each report" with its expectation, while `claude -p` prints the outer session's text, so a wrapper line before `model:` would fail a correct run; license: Task 13's stated purpose (the run proves what the card detects); Step 3 now compares the auditor's report from its `model:` line to its last line and discards wrapper text
- signal 2026-09-26 — another round does not earn its cost; both leftovers are Minor, one held for the developer and one licensable, together one small fix wave rather than a re-read

### Loop closed — 2026-09-26

The developer closed the loop on 2026-09-26 without a fourth round,
after round 3's two Minors were fixed and a propagation gate returned
clean. Round 3 was the confirming full-document round, no ledger line is
`open` or `held`, and its stop signal judged another round not worth its
cost.

After the close, a second opinion from Codex, relayed by the developer,
found three more defects. Their fixes landed after round 3, so no
adversary round has read them; the propagation gate that followed did.

- fixed 2026-09-26 — [Important] Task 13's `--allowedTools` only pre-approves and forbids nothing, so the user settings' `Bash(claude plugin *)` still reached the auditor; ruling: 2026-09-26; the run now takes `--setting-sources project`, `--tools` and `--add-dir` for the plugin directory the card reads, and Step 2 says the guard is the permission set
- fixed 2026-09-26 — [Important] Task 13 kept the outer session's printed text, not evidence that the changed card ran; ruling: 2026-09-26; each run saves its `stream-json` event stream, and Step 3 extracts the dispatch's agent type, model, denials and report from it, keeping the streams as evidence
- fixed 2026-09-26 — [Important] Task 7 dropped part of D30: the spec has the plan-adversary judge whether a withdrawn inherited decision must be undone, and send it to the developer where nothing settles it; ruling: 2026-09-26; dimension 6 now says so, Task 7 cites D30, check D added

The spec's third integrity audit changed the prescribed texts of
Tasks 1, 2 and 5, in four lines below, each recorded in the spec's
ledger under
`### 2026-09-26 — integrity audit, fable, at the consumption gate (third)`.
The fifth line, on Task 13, comes from Codex's second opinion instead:

- fixed 2026-09-26 — the state-token recognizer named the paragraph's final segment; license: the spec's *The register*, as fixed there; Task 1 now names the first segment after the statement that begins with `withdrawn`
- fixed 2026-09-26 — duty 10 inherited through unvalidated `**Follows:**` lines and subtracted unvalidated `**Defers:**` lines, and the map keyed a Global Constraints entry by the annotation; ruling: 2026-09-26; Task 5 reorders the steps, keys the entry by its line and its words after the annotation, and states the summary slots and `0/0 covered`
- fixed 2026-09-26 — the plan annotations did not say that `none` is never qualified, that an empty section is absent, or that another spec's `**Defers:**` line is out of scope; license: the spec's *The plan's annotations* and *Deferral*, as fixed there; Task 2 says so
- fixed 2026-09-26 — the withdrawal ruled outside any hit had no ledger home on a closed loop; ruling: 2026-09-26; Task 1 says the tombstone is its record there, check I added
- fixed 2026-09-26 — Task 13's extractor took the report from the dispatch's tool result, which for a background card may only acknowledge the launch; license: Task 13's stated purpose; the prompt asks for a foreground dispatch and the extractor reads the dispatched agent's last message, falling back to the tool result
- hit fixed 2026-09-26 — the sentence opening this block counted three changed texts over five lines; it now names Tasks 1, 2 and 5 in four lines and gives the fifth its own source

Task 13's first run, during implementation, found three departures in
the card and four defects in the task's own harness. The card fix
landed as `f8e743b`; the harness fixes are in Task 13 above, and the
evidence is the run's record in the dispatcher's store.

- fixed 2026-09-26 — the haiku auditor counted the Contracts relation once per side, wrote a `table-closure:` line on a plan's report, and opened reports with narration; license: D27 and the spec's *Table closure* ("3 relations checked", "A document other than a technical design gets no line"), and the card's own "Open with the self-report"; the card now counts one relation per declaration row, forbids the line on any other document, and puts `model:` first with nothing before it (`f8e743b`)
- fixed 2026-09-26 — Task 13's harness: `--setting-sources project` dropped the agents `--plugin-dir` loads, the extractor failed on an event whose `message` is a string, `grep -c` exits 1 on a zero count, and the step overstated the run's permission limits; ruling: 2026-09-26; the run now denies `Bash(claude *)` instead, the extractor skips such events, the count takes `|| true`, and Step 2 states the real limits
- fixed 2026-09-26 — Task 13 failed any denial, or on the draft wording passed any complete report; ruling: 2026-09-26; a denial fails the test unless the stream shows the same operation completed through an allowed alternative, since a complete report does not prove its check ran (Codex's second opinion)
- fixed 2026-09-26 — Task 13's second run measured duty 10 unstable on the cheapest family (34/37 and 31/32 where 39 leaves stand), each miss following a denied compound command; ruling: 2026-09-26; the derivation becomes a script — spec D31, recorded in the spec under `### 2026-09-26 — fix from ../plans/2026-09-26-plan-coverage.md` — and Tasks 14–16 add it, point the card at it and re-run Task 13 twice; Task 13's run allows that one script, and the narration before `model:` is accepted as a known departure of the cheapest family, the workflow rule's reading of the body guarding it
- fixed 2026-09-26 — Task 16's first double run matched every number but printed a `decision-coverage:` line on the technical design and dropped the `model:` line from two reports; ruling: 2026-09-26; the script skips a document under `docs/technical-designs/` and the card runs it on plans and design specs only, with its output copied below the `model:` line (`d737769`, test `4bf5c3a`); the second double run met every expectation, numbers exact both times

