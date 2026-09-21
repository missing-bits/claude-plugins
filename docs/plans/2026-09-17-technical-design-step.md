---
ticket: none
date: 2026-09-17
status: draft
adversary: blocking
spec: ../specs/2026-09-16-technical-design-step.md
branch: feature/technical-design-step
base: develop
---

# Technical design step — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the contract for a third document class — the technical
design — across the `working-process` plugin: one new path-scoped rule,
six changed rules and skills, five changed agent cards and the plugin
README, with the glossary and ADR 0004 already landed during spec
authoring.

**Architecture:** Every deliverable is prose in a shipped rule, agent
card, skill description or README. There is no code and no test suite; a
task's test is the grep pair it publishes, run before and after the
edit. Tasks are drawn one per site, so no two touch the same text —
`spec-plan-lifecycle.md` takes four tasks and `workflow.md` three,
because the change edits sections of each that share no line. The
plugin ships this contract and does not execute it: no
`docs/technical-designs/` directory is created in this repo.

**Tech Stack:** Markdown rule, agent and skill files distributed as a
Claude Code Rules payload; `grep`, `tr` and `claude plugin validate` for
verification.

## Global Constraints

- **The spec is the source.** Where this plan and the spec disagree, the
  spec wins and the plan is wrong — except where *Deviations from the
  spec* below records a departure and its reason.
- **Prose wraps at 72 characters** in every rule, agent card, skill and
  README file. Match the surrounding paragraph; never reflow a paragraph
  this plan does not change.
- **A check over prose normalizes whitespace first**
  (`tr -s '[:space:]' ' '`), so a phrase matches wherever a line wraps.
  Only a check anchoring something that cannot wrap — a path, a filename
  shape, a heading, a frontmatter key — is written plain.
- **Every step states its before value and its after value.** The before
  values in this plan were measured against the files on 2026-09-17, not
  predicted.
- **`design document` appears five times in four shipped files** before
  this plan runs — twice in `agents/plan-adversary.md`, once each in
  `agents/architect.md`, `agents/integrity-auditor.md` and `README.md`.
  When the plan is done it appears zero times in those files. No task
  may introduce a sixth.
- **The glossary binds.** `docs/domain/glossary.md` terms and `_Avoid_`
  bans govern this text. `Design spec`, `Judged document`, `Technical
  design`, `Part`, `Contract`, `Vocabulary gap`, `Origin` and
  `Consumption gate` are canonical here. `design document` is banned by
  **Judged document**'s `_Avoid_` list and appears in no replacement
  block. `session` never names a skill — write
  `` `system-designer-session` skill``.
- **Public repo hygiene**: no machine-specific paths, no company or
  client names, all committed text in English.
- **Commit messages** are one conventional-commit line, no body, no
  trailers.
- **Paths in this plan are repo-relative.** Rule and agent files live
  under `plugins/working-process/`.

---

### Task 1: Verify the two documents already on disk

The spec's Parts table lists the glossary and ADR 0004 as parts of this
change. Both landed while the spec was authored and are already
committed, in `dc85b9b` together with the spec and this plan. This task
verifies them rather than writing them, so a later task never re-mints a
term that already exists, and it commits nothing.

**Files:**
- Verify: `docs/domain/glossary.md`
- Verify: `docs/domain/adr/0004-ceremonies-follow-the-reader.md`

**Interfaces:**
- Produces: the seven glossary terms every later task's prose leans on —
  `Design spec`, `Judged document`, `Technical design`, `Part`,
  `Contract`, `Vocabulary gap`, and `Origin` in its list form — plus ADR
  0004 as the citable decision behind the class.

- [ ] **Step 1: Confirm every term the spec mints exists**

Run:

```bash
for t in "Design spec" "Judged document" "Technical design" "Part" \
         "Contract" "Vocabulary gap" "Origin" "Consumption gate"; do
  printf '%-18s %s\n' "$t" \
    "$(grep -c "^\*\*${t}\*\*:" docs/domain/glossary.md)"
done
```

Expected: `1` for every term. A `0` means the glossary edit was lost —
stop and restore it from the spec's Parts table before continuing.

- [ ] **Step 2: Confirm `Origin` is a list and bans `both`**

Run:

```bash
grep -A8 '^\*\*Origin\*\*:' docs/domain/glossary.md | \
  tr -s '[:space:]' ' ' | grep -c 'Avoid.*`both`'
```

Expected: `1`. The list form is what Task 12 writes the adversary's
`origin` field against.

- [ ] **Step 3: Confirm ADR 0004 exists and names the class**

Run:

```bash
tr -s '[:space:]' ' ' < docs/domain/adr/0004-ceremonies-follow-the-reader.md | \
  grep -c 'judged document'
```

Expected: `1` or more.

- [ ] **Step 4: Confirm the gate entry carries the narrow ordering**

The entry must state the one dependency the spec settled, not the broad
one an earlier draft carried. Run:

```bash
grep -A12 '^\*\*Consumption gate\*\*:' docs/domain/glossary.md | \
  tr -s '[:space:]' ' ' | grep -c 'precede the joint integrity audit'
grep -c 'settles before anything' docs/domain/glossary.md
```

Expected: `1`, then `0`. The second is the deletion assertion: the broad
ordering — everything the design owes before anything its design spec
owes — was withdrawn by the spec's integrity ruling of 2026-09-17, and a
surviving copy would send Task 8's text into contradiction with a
canonical term.

- [ ] **Step 5: Nothing to commit**

The four documents are already in `dc85b9b`. This task writes nothing,
so it has no commit of its own; the wave that follows commits per round
on `feature/technical-design-step.docs`.

---

### Task 2: The new path-scoped rule

**Files:**
- Create: `plugins/working-process/rules/technical-design.md`

**Interfaces:**
- Produces: the section skeleton every later task refers to, the three
  definitions (part, contract, state), the closed `change` value set
  `new | changed | retired | unchanged`, and the term **vocabulary
  gap**. Task 12 reads the `change` set; Task 5 reads the skeleton's
  section 7–8 delegation to the lifecycle rule.

- [ ] **Step 1: Confirm the file does not exist**

Run: `ls plugins/working-process/rules/technical-design.md`
Expected: `No such file or directory`.

- [ ] **Step 2: Write the rule**

Create `plugins/working-process/rules/technical-design.md`:

```markdown
---
paths:
  - "docs/technical-designs/**"
---

# Technical design — what the thing is made of

A technical design answers what a thing is made of, as its design spec
answers what and why and the implementation plan answers in what order
and verified how. It lives in `docs/technical-designs/`, one file per
design spec, named `<topic>-technical-design.md`.

The boundary against the design spec runs between identity and
placement. The design spec names parts by the name their consumers use
and gives each one a responsibility. The technical design decides what
naming a part leaves open: where it sits, what shape the contract on
its border takes, who writes it and who reads it, what is state and
where that state is authoritative. Where naming a part fixes its
location, the name is the path and the design spec carries it.

## Section skeleton

| # | section | status | content |
|---|---|---|---|
| 1 | Scope | required | which design spec and which of its behaviours this structure realizes; the system boundary |
| 2 | Parts | required | `part \| kind \| change \| placement \| owns \| deliberately excludes`; a retirement is a `change: retired` row |
| 3 | Contracts | required | `producer → consumer \| crosses \| guarantee \| breaks when \| check`; a flow crossing three or more parts in fixed order becomes a numbered sequence |
| 4 | State | conditional | `record \| home \| written by \| read by \| lifecycle \| visible through` |
| 5 | Failure and repetition | conditional | what happens when a step does not finish, runs twice, runs beside another, or finds the other side absent |
| 6 | Cuts not taken | conditional | one line per rejected division and its reason |
| 7–8 | Open questions, Review rounds | from the spec-plan-lifecycle rule | as a design spec and a plan carry them today |

Three sections are required because only those three are never empty,
on prose or on code. A conditional section that is absent is named in
one line — "not applicable, because…" — never silently dropped.

`kind` answers what a part is; `placement` answers where it belongs —
its layer, module, package, service, or path, at the level the design
decision needs. The two coincide only where a domain convention derives
one from the other, and the cell is filled even then: a cell reading
`rules/` says the convention was applied deliberately, while an empty
one cannot be told apart from an omission.

`change` takes one of `new`, `changed`, `retired` or `unchanged`. The
set is closed and a domain adds no value to it: the column steers the
process, so its meaning belongs to the core, and a value outside the
set is an error the author corrects rather than a part that quietly
escapes the plan's coverage check.

Tests are not a section. What verifies a contract is the contract's
`check` column; when that check runs is the plan's business.

## The three definitions

A **part** has a resolvable identity, an explicit responsibility with
its exclusions, and a contract that lets its implementation change
without changing its consumers.

A **contract** is what a consumer may rely on without reading the
producer's body.

**State** is a record that outlives one interaction and is read by a
later one, with a home, a writer, a reader and an end.

Part and contract are two questions about one thing rather than
competing labels: a file may be a part, its signature a contract, and
the record it writes state.

## What earns a part its own row

Listing a part separately is a design decision. List it when leaving it
out would make an implementer decide a responsibility boundary, a
contract between parts, or the ownership of state. Keep inside a part
the details that merely carry out decisions already made — a public
method is usually a row in its part's contracts rather than a part of
its own.

Task boundaries never define part boundaries: the plan is organised
around the structure, not the structure around the plan. The grain
comes from the decisions the document exists to settle — the same
question an integrity audit asks of a design spec, which is what this
text would leave an implementer to decide.

## Domain vocabulary

The author takes the part vocabulary — kinds of part, placement rules,
kinds of contract, homes of state — from the Domain expertise duty the
personas already carry, which has them scan and load the domain's own
skills. No discovery convention of its own ships here.

A kind of part that no domain skill names is recorded in the document
as a **vocabulary gap**: the author names the kind, writes the gap
down, and the architect round judges the boundary, which is what it
judges in any case. Accumulated vocabulary gaps are either the
specification of a `<domain>-technical-design` skill or the evidence
that none is needed.

Where no skill covers the technology at all, the document is written
from generic knowledge, best effort. That degradation path is what
makes this contract self-sufficient.

## What the core closes

The core closes the three definitions above, the table columns, the
contract entry's fields, and the four questions of the failure section.
A domain adds rows and values — outside the closed `change` column —
never columns, and never redefines what qualifies: a kind of part it
names must still have a resolvable identity, an explicit
responsibility, and a contract its implementation can change behind.
```

- [ ] **Step 3: Verify the rule's own claims**

Run:

```bash
F=plugins/working-process/rules/technical-design.md
grep -c '^| [0-9]' $F                       # skeleton rows
grep -c 'new | changed | retired | unchanged' $F
awk 'length > 72' $F | grep -v '^|' | wc -l  # over-wide non-table lines
```

Expected: `7` skeleton rows (1–6 plus the `7–8` row), `1` for the closed
set, `0` over-wide prose lines.

- [ ] **Step 4: Validate the plugin**

Run: `claude plugin validate plugins/working-process`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/rules/technical-design.md
git commit -m "feat(working-process): add the technical-design rule"
```

---

### Task 3: The new Process directory

**Files:**
- Modify: `plugins/working-process/rules/process-artifacts.md:1-8` and
  the Process-directory sentence at `:12-16`

**Interfaces:**
- Produces: `docs/technical-designs/` as a named Process directory, so
  the first-create question fires for it and Task 4 can assign it a
  field set.

- [ ] **Step 1: Measure the before state**

Run:

```bash
F=plugins/working-process/rules/process-artifacts.md
grep -c 'technical-designs' $F
sed -n '2,8p' $F
```

Expected: `0`, and a `paths:` block of five globs, the last
`.superpowers/**`.

- [ ] **Step 2: Add the glob**

In the frontmatter, after the `"docs/plans/**"` line, insert:

```yaml
  - "docs/technical-designs/**"
```

- [ ] **Step 3: Add the directory to the prose list**

Replace:

```
project repo to hold work artifacts: `docs/specs/`, `docs/plans/`,
`docs/domain/`, `docs/code-review/`, `docs/memory/` (Team memory — when the
```

with:

```
project repo to hold work artifacts: `docs/specs/`,
`docs/technical-designs/`, `docs/plans/`, `docs/domain/`,
`docs/code-review/`, `docs/memory/` (Team memory — when the
```

- [ ] **Step 4: Verify both sites**

Run:

```bash
F=plugins/working-process/rules/process-artifacts.md
grep -c '"docs/technical-designs/\*\*"' $F   # expect 1
tr -s '[:space:]' ' ' < $F | grep -c '`docs/specs/`, `docs/technical-designs/`, `docs/plans/`'  # expect 1
```

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/rules/process-artifacts.md
git commit -m "feat(working-process): count docs/technical-designs among Process directories"
```

---

### Task 4: The new directory's field set

**Files:**
- Modify: `plugins/working-process/rules/ticket-frontmatter.md:13-15`

**Interfaces:**
- Consumes: the directory named in Task 3.
- Produces: the guarantee that a technical design carries the full
  process field set rather than the bare `ticket` + `date` its
  per-directory list would otherwise give it.

- [ ] **Step 1: Measure the before state**

Run:

```bash
tr -s '[:space:]' ' ' < plugins/working-process/rules/ticket-frontmatter.md | \
  grep -o 'Specs and plans (`docs/specs/`, `docs/plans/`)'
```

Expected: one match.

- [ ] **Step 2: Widen the first field-set bullet**

Replace:

```
- Specs and plans (`docs/specs/`, `docs/plans/`): `ticket` + `date` +
  `status` + the process and branch fields — details in the
  spec-plan-lifecycle rule.
```

with:

```
- Design specs, technical designs and plans (`docs/specs/`,
  `docs/technical-designs/`, `docs/plans/`): `ticket` + `date` +
  `status` + the process and branch fields — details in the
  spec-plan-lifecycle rule.
```

- [ ] **Step 3: Verify the catch-all no longer claims the directory**

Run:

```bash
F=plugins/working-process/rules/ticket-frontmatter.md
tr -s '[:space:]' ' ' < $F | grep -c 'technical designs and plans'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'Every other document under `docs/`'  # expect 1
```

The second still stands: it is a catch-all, and the first bullet now
takes the new directory out of its reach.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/rules/ticket-frontmatter.md
git commit -m "feat(working-process): give technical designs the process field set"
```

---

### Task 5: The lifecycle rule — scope and the class at each branch

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md:1-6`
  (`paths:`), `:7-10` (title and opener), `:73-75` (the re-review
  offer's gate), `:100-104` (the `integrity:` recomputation), `:229-231`
  (the cross-document clause), `:447-448` (Chain debt's owner leg),
  `:481-495` (Lifecycle offers), `:504-509` (the consumption-gate
  backstop)

**Interfaces:**
- Consumes: `Judged document` from Task 1.
- Produces: the rule loading for `docs/technical-designs/**`, and the
  six branch sentences listed in Step 3 reading the class rather than a
  filename. Six, not "every" — the blanket claim hid which sentences
  were covered and which were merely unvisited. Tasks 6, 7 and 8 edit
  other sections of this file and must not touch these lines.

- [ ] **Step 1: Measure the before state**

Run:

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
sed -n '2,5p' $F
grep -c 'judged document' $F        # expect 0
grep -c 'technical-design' $F       # expect 0
```

- [ ] **Step 2: Widen the rule's scope**

In the frontmatter, after `  - "docs/specs/**"`, insert:

```yaml
  - "docs/technical-designs/**"
```

- [ ] **Step 3: Name the class at all six branch sentences**

The rule branches on the document in six places. Two are the offers
paragraph and the backstop below; the other four are the title and
opener, the re-review offer's gate, the `integrity:` recomputation, and
the Chain debt entry's owner leg. The last of these is read verbatim by
the `process-status` skill, which is told never to supply an owner from
its own knowledge of the process, so a stale owner there misinstructs a
component that cannot correct it.

First, the title and opener. Replace:

```
# Specs and plans — frontmatter and lifecycle
```

with:

```
# Judged documents and plans — frontmatter and lifecycle
```

and replace:

```
Specs live in `docs/specs/`, plans in `docs/plans/`. Both open with a
```

with:

```
Design specs live in `docs/specs/`, technical designs in
`docs/technical-designs/`, plans in `docs/plans/`. All three open with a
```

Then the offers paragraph. Replace:

```
architect-review a grilled spec (architect agent dispatch);
```

with:

```
architect-review a grilled design spec, and a technical design, which
is never grilled (architect agent dispatch);
```

Then replace:

```
spec or plan moves to `implemented` and the memory-review-session skill
```

with:

```
judged document or plan moves to `implemented` and the
memory-review-session skill
```

- [ ] **Step 4: Widen the consumption-gate backstop**

Replace:

```
A document's consumption gate is the backstop for its ledger: a spec
does not pass to plan-writing, nor a plan to implementation, while
`held` lines stay open — an LGTM can leave the frontmatter clean while a
```

with:

```
A document's consumption gate is the backstop for its ledger: no judged
document passes to plan-writing, nor a plan to implementation, while
`held` lines stay open — an LGTM can leave the frontmatter clean while a
```

The next sentence of the same paragraph is a seventh branch and has to
move with it. Replace:

```
latest. Writing a plan from a spec is that same seam: the held spec
questions are asked before the plan is written, whoever writes it.
```

with:

```
latest. Writing a plan from a judged document is that same seam: its
held questions are asked before the plan is written, whoever writes it.
```

- [ ] **Step 5: Name the class at the three remaining branches**

Replace:

```
  gate — before plan-writing for a spec, before implementation for a
  plan. Accepted: a fresh round at the prescribed tier replaces the
```

with:

```
  gate — before plan-writing for a judged document, before
  implementation for a plan. Accepted: a fresh round at the prescribed
  tier replaces the
```

Replace:

```
- A spec's consumption gate owns the recomputation: before plan-writing it
```

with:

```
- A judged document's consumption gate owns the recomputation: before
  plan-writing it
```

and, in the same bullet:

```
  are spec-gate semantics — on a plan, a permitted target on explicit
```

becomes

```
  are judged-document semantics — on a plan, a permitted target on
  explicit
```

The cross-document clause cites a value the reviewer will no longer
emit. Replace:

```
reviewed one — a plan review's finding carrying `origin: spec` is the
```

with:

```
reviewed one — a plan review's finding whose `origin` names a judged
document is the
```

Finally the Chain debt entry's owner leg, which `process-status` reads
literally. Replace:

```
  Owner: for a spec, the consumption gate's pair offer; for a plan, the
```

with:

```
  Owner: for a judged document, the consumption gate's pair offer; for a
  plan, the
```

- [ ] **Step 6: State that a technical design is not grilled**

After the offers paragraph, add:

```
A technical design is a judged document and takes the design spec's side
of every branch in this rule: the same fields, the same
consumption-gate semantics for a stale stamp, the same owner for an
unresolved verdict, and the same pair offered against chain debt. It is
not grilled — grilling stress-tests terminology against the project
glossary, and a technical design mints none: its vocabulary comes from
its design spec, which was grilled, and from the domain's own skills.
The names it does mint are part and component names, checked against
those skills where one exists and recorded as a vocabulary gap where
none does.

One mechanism it shares rather than owns: the integrity check is due on
it like any judged document, and one audit of the pair discharges it, so
the `integrity:` stamp sits on the design spec and names both.
```

Without that last sentence this block and Task 7's contradict each
other four hundred lines apart — "the same consumption-gate semantics
for a stale stamp" against "carries no `integrity:` of its own".

- [ ] **Step 7: Verify**

Run:

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '"docs/technical-designs/\*\*"' $F         # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'no judged document passes to plan-writing'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'It is not grilled'   # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'One mechanism it shares rather than owns'   # expect 1
grep -c '^# Judged documents and plans' $F          # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'for a judged document, the consumption' # expect 1
grep -c 'for a spec, the consumption' $F            # expect 0
grep -c 'spec-gate semantics' $F                    # expect 0
grep -c 'plan-writing for a spec' $F                # expect 0
grep -c 'origin: spec' $F                           # expect 0
grep -c 'the held spec questions' $F                # expect 0
```

The last three are deletion assertions: each names a branch sentence
this task replaces, and a survivor would leave the rule saying both
things at once.

- [ ] **Step 8: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): branch the lifecycle on the document class"
```

---

### Task 6: The lifecycle rule — the two pointers

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md:16-26`
  (the frontmatter example) and the field notes below it

**Interfaces:**
- Consumes: the class branches from Task 5.
- Produces: `technical-design:` and the widened `spec:`, which Task 9
  makes the propagation auditor check and Task 11 makes the authoring
  step write.

- [ ] **Step 1: Measure the before state**

Run:

```bash
grep -n 'spec: \.\./specs/' plugins/working-process/rules/spec-plan-lifecycle.md
```

Expected: one line, commented `plans only`.

- [ ] **Step 2: Widen `spec:` and add `technical-design:`**

Replace:

```
spec: ../specs/<file>.md   # plans only: the spec this plan implements; inline list when several
```

with:

```
spec: ../specs/<file>.md   # plans and technical designs: the design spec this document descends from; inline list when several
technical-design: ../technical-designs/<file>.md   # optional, on a design spec and on a plan: the technical design that develops this design spec
```

- [ ] **Step 3: Write the five rules that keep the pair honest**

After the field notes, add:

```
- `technical-design:` is optional and appears once the technical design
  exists, so its absence means there is none rather than one nobody
  linked. It is new in kind: every other pointer records where a
  document came from, while this one names a document written later,
  and it gives a reader holding the design spec the structure that
  develops it. The author who creates the design writes both ends in
  the same turn — the design's `spec:` and the design spec's
  `technical-design:`. A plan keeps its own `spec:` and
  `technical-design:`, and where it carries both they must agree with
  the pair. One technical design per design spec.
```

- [ ] **Step 4: Say what the pointer does to a plan's interface blocks**

A plan naming a technical design must not redefine what that design
already defines. Add after the five rules:

```
- Where a plan's `technical-design:` names a document, that document
  defines the interfaces. The plan's `**Interfaces:**` blocks reference
  the contracts it defines and say which part of one each task
  implements or changes; they do not independently redefine those
  contracts. Where a plan names no technical design, the existing plan
  convention stands unchanged. This binds how the blocks are filled and
  changes no plan template — the template belongs to the tool that
  writes plans.
```

- [ ] **Step 5: Verify**

Run:

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '^technical-design: ' $F                   # expect 1
grep -c 'plans and technical designs' $F           # expect 1
grep -c 'plans only' $F                            # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'they do not independently redefine those contracts'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'One technical design per design spec'  # expect 1
```

The third check is the deletion assertion: the old `plans only` comment
must be gone, not merely contradicted further down.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): add the technical-design pointer pair"
```

---

### Task 7: The lifecycle rule — the pair stamp

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md:21`
  (the frontmatter example) and `:81-105` (the `integrity:` notes)

**Interfaces:**
- Consumes: the pointers from Task 6.
- Produces: the `with:` value shape, which Task 14 makes the auditor
  emit and Task 18 documents in the README's field table.

- [ ] **Step 1: Measure the before state**

Run:

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c 'with: ' $F        # expect 0
grep -n 'sha: <short-hash>' $F
```

Expected: `0`, and two lines carrying the bare value shape.

- [ ] **Step 2: Extend the frontmatter example**

Replace:

```
integrity: <ISO date> (sha: <short-hash>)   # optional: date of the last integrity audit, plus the body hash it certifies
```

with:

```
integrity: <ISO date> (sha: <short-hash>[; with: <file>@<short-hash>])   # optional: date of the last integrity audit, the body hash it certifies, and — where a technical design was audited with it — that document and its hash
```

- [ ] **Step 3: Write the pair clause**

The bullet does not end where that sentence does — it runs twelve more
lines, through the hash command the pair clause depends on. Anchor on
the bullet's real last line, `a typo fix included.`, and add after it:

```
  A design spec that names a technical design is audited with it as one
  target, and one stamp records the pair. The stamp lives on the design
  spec, names both documents and both body hashes, and the technical
  design carries no `integrity:` of its own — it owes the check like any
  judged document and discharges it jointly. The value takes the form
  `integrity: <date> (sha: <own-hash>; with: <file>@<their-hash>)`,
  where `<file>` is the technical design's path relative to the design
  spec. Changing either document unsettles the pair, and the gate
  recomputes both hashes to see it; because the two pointers are what
  identify the pair, an added, removed or repointed `technical-design:`
  unsettles it too.
```

- [ ] **Step 4: Widen the discharge paths to a pair**

The three discharge paths describe annotating one document. Replace:

```
applied and before the `integrity:` stamp; and any later full-document
```

with:

```
applied and before the `integrity:` stamp — and where that audit read a
pair, it discharges the debt of both documents it read, annotating each
document's own unannotated diff-scoped `LGTM` headings; and any later
full-document
```

- [ ] **Step 5: Verify both directions**

Run:

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c 'with: <file>@<their-hash>' $F     # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'carries no `integrity:` of its own'   # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'recomputes both hashes'   # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'both documents it read'   # expect 1
```

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): record a pair audit in one integrity stamp"
```

---

### Task 8: The lifecycle rule — the gate's passes and the status move

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md`,
  Lifecycle offers section, after the consumption-gate backstop
  paragraph

**Interfaces:**
- Consumes: the class branches from Task 5.
- Produces: the ordering and the pass structure Task 10's gate offer
  fires inside.

- [ ] **Step 1: Measure the before state**

Run:

```bash
tr -s '[:space:]' ' ' < plugins/working-process/rules/spec-plan-lifecycle.md | \
  grep -c 'runs in passes'
```

Expected: `0`.

- [ ] **Step 2: Write the ordering and the passes**

After the paragraph ending `the held spec questions are asked before the
plan is written, whoever writes it.`, add:

```
A technical design's own consumption gate is plan-writing, the same
moment as its design spec's, and one ordering binds the two: writing
the design and applying its review dispositions precedes the joint
integrity audit, because the design is the last producer of changes to
the design spec and certifying that body before the design's questions
are answered stamps a body about to change. The dependency reaches no
further — every other item of the two gates stays unordered.

The gate therefore runs in passes. The first pass decides whether a
technical design is written at all. Where the offer is accepted, the
gate suspends until the design exists and its review dispositions are
applied, then resumes and collects the questions the documents' current
state raises. Answers already given stay binding unless the basis they
rested on changed. Each pass asks its questions in one batch, as a
review round does — a batch being every question answerable at that
pass, never every question the gate will ever ask.

A technical design's `status` reaches `implemented` with its plan's, in
the same turn and by the same hand, since otherwise the rule freezing an
implemented document's body never reaches it.
```

- [ ] **Step 3: Verify**

Run:

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
tr -s '[:space:]' ' ' < $F | grep -c 'The gate therefore runs in passes'     # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'precedes the joint integrity audit'    # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'in the same turn and by the same hand' # expect 1
```

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): run the consumption gate in passes"
```

---

### Task 9: The propagation auditor's author-facing duty

**Files:**
- Modify: `plugins/working-process/rules/propagation-duties.md:1-6`
  (`paths:`) and its duty list

**Interfaces:**
- Consumes: the pointers from Task 6.
- Produces: the author's duty to check both pointers resolve and name
  each other — the mechanical half of the pair's honesty.

- [ ] **Step 1: Measure the before state**

Run:

```bash
F=plugins/working-process/rules/propagation-duties.md
sed -n '2,5p' $F
grep -c 'technical-design' $F   # expect 0
grep -c '^| ' $F                # expect 10: header plus nine edit rows
```

The separator row (`|---|---|---|`) carries no space after the pipe and
never matches this pattern — which is why the count is ten and not
eleven.

- [ ] **Step 2: Widen the rule's scope**

In the frontmatter, after `  - "docs/specs/**"`, insert:

```yaml
  - "docs/technical-designs/**"
```

- [ ] **Step 3: Add the pointer-pair duty as a table row**

The duties are a table keyed by the edit, not a bullet list. Append a
row after the `copied a citation out of a review report` row:

```
| added or repointed a `spec:` or `technical-design:` pointer | both targets, and that each pointer names the document that names it; on a plan, that its `spec:` and `technical-design:` name a design spec and the design that design spec names | 9 |
```

- [ ] **Step 4: Re-derive the two counters the row invalidates**

The rule opens by counting its own duties and the edits that key them.
Replace:

```
Before a document goes to an expensive reader, eight duties fall due,
keyed by the nine edits that trigger them — one duty answers two
different edits.
```

with:

```
Before a document goes to an expensive reader, nine duties fall due,
keyed by the ten edits that trigger them — one duty answers two
different edits.
```

and replace:

```
When the `propagation-auditor` agent is available it walks the same
eight as a gate, and its card is their definition and keeps the
```

with:

```
When the `propagation-auditor` agent is available it walks the same
nine as a gate, and its card is their definition and keeps the
```

- [ ] **Step 5: Verify, both counters against what they count**

Run:

```bash
F=plugins/working-process/rules/propagation-duties.md
grep -c '"docs/technical-designs/\*\*"' $F      # expect 1
grep -c '^| ' $F                                 # expect 11: header plus ten edit rows
grep -c 'nine duties fall due' $F                # expect 1
grep -c 'keyed by the ten edits' $F              # expect 1
grep -c 'walks the same nine' $F                 # expect 1
grep -c 'eight duties\|the nine edits\|same eight' $F   # expect 0
```

The last line is the deletion assertion, and it is the one that matters:
the old counters read as true prose and nothing but a recount catches
them.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/propagation-duties.md
git commit -m "feat(working-process): make the author check the pointer pair"
```

---

### Task 10: The workflow rule — the step and its gate offer

**Files:**
- Modify: `plugins/working-process/rules/workflow.md:36-56` (step 4,
  *Spec → plan*)

**Interfaces:**
- Consumes: the passes from Task 8.
- Produces: the offer that decides a technical design gets written, and
  the marker test that fires it. The offer lives in the always-on rule
  because it fires before any technical design exists, with the
  path-scoped rule of Task 2 therefore unloaded.

- [ ] **Step 1: Measure the before state**

Run:

```bash
F=plugins/working-process/rules/workflow.md
grep -c 'technical design' $F   # expect 0
sed -n '36,38p' $F
```

Expected: `0`, and step 4 opening `4. **Spec → plan.** At the spec's
consumption gate, before the plan is`.

- [ ] **Step 2: Insert the new offer at a byte-exact anchor**

The insertion point is byte-exact, not positional: an earlier draft said
"after the step's existing offer sentence", and that sentence ends
mid-line, so the block could land before or after the pair-form sentence
that also says "the offer". Replace:

```
   absent. The brief
```

with:

```
   absent.

   At the same gate, and before the integrity audit above, offer the
   technical design when the repository is one that has code. A
   declaration the project records binds and is never re-asked, in
   either direction; a session reads it from a `CLAUDE.md` note at the
   repository root, or from the file such a note points at, which is
   the shape available until a standing home for a project's process
   answers exists. Without a declaration, a repository carrying a
   toolchain manifest — a file a language or platform toolchain reads
   to build, test or deploy it — gets the offer at every consumption
   gate and nothing is written; a repository carrying neither gets no
   offer. The core names no closed list of markers, and a domain's own
   skill may name the markers of its technology. A marker proves the
   repository holds code, never that this change needs decomposing, so
   the declaration is the signal and the marker only raises the
   question. The offer reads *open the `system-designer-session` skill,
   when available, and write the technical design?* — never *dispatch*,
   which names a background agent here. Where no skill covers the
   technology the document is still written, from generic knowledge and
   best effort: a tool that is not installed disables its suggestion,
   never the work. A session may propose writing the declaration
   and never writes it unasked. A change may skip the document when it
   sits inside boundaries and contracts already settled and leaves the
   implementer no new responsibility split, placement, or ownership of
   state.

   The brief
```

Three things ride in that block beyond the offer itself. The
`CLAUDE.md` sentence is what makes a declaration readable — without it
the rule says a declaration binds while no session can find one, and no
project could ever silence the offer. The `when available` clause sits
on the skill and not on the offer: this rule's own preamble says a tool
that is not installed disables its suggestion and never the work, and
the spec carries a degradation path for exactly that case, so gating
the offer on the tool would make the work vanish with it. The
domain-marker sentence is the spec's, and had no other task.

- [ ] **Step 3: Order the audit behind the technical-design offer**

Step 2 already moved `The brief` onto its own paragraph. Now name which
offer the ordering is about — "the offer" alone reads as the pair offer
two sentences above. Replace:

```
   The brief
   confirms the auditor's two preconditions: every edit from the
```

with:

```
   Where the technical-design offer is accepted, the audit waits: the
   design is the last producer of changes to its design spec, and the
   two are then audited as one target. The gate makes one offer for the
   pair rather than one per document, and where the audit discharges
   chain debt it discharges it for both documents it read. The brief
   confirms the auditor's two preconditions: every edit from the
```

- [ ] **Step 4: Verify**

Run:

```bash
F=plugins/working-process/rules/workflow.md
tr -s '[:space:]' ' ' < $F | grep -c 'system-designer-session` skill and write the technical design'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'the declaration is the signal and the marker only raises the question'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'audited as one target'   # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'from a `CLAUDE.md` note at the repository root'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'skill, when available, and write the technical design'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'never the work'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'may name the markers of its technology'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'one offer for the pair'  # expect 1
grep -c 'designer session' $F    # expect 0 — the glossary bans "session" for a skill
```

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): offer the technical design at the consumption gate"
```

---

### Task 11: The workflow rule — the authoring step writes both pointers

**Files:**
- Modify: `plugins/working-process/rules/workflow.md`, step 4, after the
  offer added in Task 10

**Interfaces:**
- Consumes: the offer from Task 10, the pointers from Task 6, and the
  architect card sentence Task 13 writes. **Task 13 must land first** —
  this task quotes that card, and quoting a phrase the card does not yet
  carry is the propagation duty on prescribed blocks failing by our own
  hand. Execute 13 before 11, or swap their numbers.
- Produces: the one turn in which both ends of the pair are written, so
  Task 9's duty never finds a half-written pair.

- [ ] **Step 1: Measure the before state**

Run:

```bash
tr -s '[:space:]' ' ' < plugins/working-process/rules/workflow.md | \
  grep -c 'writes both ends'
```

Expected: `0`.

- [ ] **Step 2: Write the authoring step**

After the offer paragraph, add:

```
   Accepted, the session opens the `system-designer-session` skill when
   it is available and writes the document to `docs/technical-designs/`,
   following the technical-design rule that loads there. It writes both
   ends of the pair in the same turn — the design's `spec:` and the
   design spec's `technical-design:` — so no audit ever meets a
   half-written pair. The reviewer is the `architect` agent when that
   agent is available, whose card admits any judged document dispatched
   standalone, with the propagation audit gating that dispatch as it
   gates every verdict dispatch. The plan-adversary stays on plans.
```

Both tool mentions are conditional, as every neighbouring step in this
rule is: committed project-level rules load for people who do not have
the plugin installed.

- [ ] **Step 3: Verify**

Run:

```bash
F=plugins/working-process/rules/workflow.md
tr -s '[:space:]' ' ' < $F | grep -c 'writes both ends of the pair in the same turn'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'The plan-adversary stays on plans'   # expect 1
```

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): name the technical design's author and reviewer"
```

---

### Task 12: The workflow rule — the triage clause reads a list

**Files:**
- Modify: `plugins/working-process/rules/workflow.md:333-339`

**Interfaces:**
- Consumes: `Origin` in its list form from Task 1.
- Produces: the widened hold, which Task 15 makes the adversary's report
  schema able to express.

- [ ] **Step 1: Measure the before state**

Run:

```bash
sed -n '333,339p' plugins/working-process/rules/workflow.md
```

Expected: the clause opening `- A finding whose `origin` names the spec
is held unless a written` and carrying ``both` holds the same way`.

- [ ] **Step 2: Widen the hold to the class**

Replace:

```
- A finding whose `origin` names the spec is held unless a written
  decision licenses the edit, since editing a spec from inside a plan
  review is design work; `both` holds the same way, and its `held`
  line names in `options:` which half is fixable at once. A licensed
  spec-origin fix lands in the spec's own ledger and the plan's line
  points at it, by the cross-document clause the spec-plan-lifecycle
  rule defines
```

with:

```
- A finding whose `origin` names a judged document — a design spec or a
  technical design — is held unless a written decision licenses the
  edit, since changing either from inside a plan review is design work.
  `origin` is a list, so a finding naming more than one holds the same
  way, and its `held` line names in `options:` which part is fixable at
  once. A licensed fix lands in the ledger of the document that
  changed, and the plan's line points at it, by the cross-document
  clause the spec-plan-lifecycle rule defines
```

- [ ] **Step 3: Verify the retired value is gone**

Run:

```bash
F=plugins/working-process/rules/workflow.md
tr -s '[:space:]' ' ' < $F | grep -c 'names a judged document'   # expect 1
grep -c '`both`' $F    # expect 0
```

The second check is the deletion assertion: `both` retires with the
value, and a surviving mention would send triage down a branch the
adversary can no longer emit.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): hold a finding from either judged document"
```

---

### Task 13: The architect card takes the class name

**Files:**
- Modify: `plugins/working-process/agents/architect.md:3`

**Interfaces:**
- Consumes: `Judged document` from Task 1.
- Produces: the card sentence Task 11's authoring step cites when it
  says the architect admits any judged document standalone.

- [ ] **Step 1: Measure the before state**

Run:

```bash
grep -c 'design document' plugins/working-process/agents/architect.md
```

Expected: `1`.

- [ ] **Step 2: Rename the class in the description**

Replace, in the `description:` field:

```
a grilled spec (primary target) or any design document dispatched standalone
```

with:

```
a grilled design spec (primary target) or any judged document dispatched standalone
```

- [ ] **Step 3: Verify**

Run:

```bash
F=plugins/working-process/agents/architect.md
grep -c 'design document' $F        # expect 0
grep -c 'any judged document' $F    # expect 1
grep -c 'a grilled design spec' $F  # expect 1
```

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/agents/architect.md
git commit -m "feat(working-process): let the architect card name the judged-document class"
```

---

### Task 14: The integrity auditor reads a pair

The spec requires these three edits to land together: any one alone
leaves the card contradicting itself, which is the defect class this
auditor hunts.

**Files:**
- Modify: `plugins/working-process/agents/integrity-auditor.md:3`
  (description), `:76-81` (Target and moment), `:101-103` (the second
  lens), `:133-137` (the coverage tell)

**Interfaces:**
- Consumes: the pointers from Task 6 and the stamp from Task 7.
- Produces: the four cases, the narrowed second lens, and the
  coverage tell's per-document shape.

- [ ] **Step 1: Measure the before state**

Run:

```bash
F=plugins/working-process/agents/integrity-auditor.md
grep -c 'design document' $F                       # expect 1
grep -c 'coverage: <target line count>' $F         # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'Your primary target is a spec'  # expect 1
```

- [ ] **Step 2: Bring the description in line with the duties below it**

The description paraphrases all three edits, so renaming the class
alone would leave it stating premises this task retires. Replace:

```
Judgment audit of a churned design document, read on a fresh context — primarily a spec at the consumption gate before plan-writing
```

with:

```
Judgment audit of a churned judged document, read on a fresh context — primarily a design spec at the consumption gate before plan-writing, together with its technical design where it names one
```

and replace:

```
reads it once more as an implementer who must build from this text and has no other context
```

with:

```
reads it once more as an implementer who must build from this text, the documents audited with it, and the documents its `spec:` and `technical-design:` name, and has no other context
```

- [ ] **Step 3: Write the four cases**

Replace:

```
Your primary target is a spec, audited at the consumption gate before
plan-writing: after the architect round and after its dispositions are
applied, which is where the churn accumulates. A plan is a permitted
target on explicit request, never a gated one. Read the whole target,
first line to last.
```

with:

```
Your primary target is a design spec, audited at the consumption gate
before plan-writing: after the architect round and after its
dispositions are applied, which is where the churn accumulates. Four
cases fix what you read:

A design spec with no technical design is a single target. A design
spec that names one is audited together with it, both documents the
target and neither the other's context. A plan, a permitted target on
explicit request, never a gated one, is the target alone and reads the
documents its `spec:` and `technical-design:` name as context. A
technical design is never a target alone: its audit is its design
spec's.

No other field carries context. `revises:` names a document whose
design no longer matches what shipped, and reading an archive as
authority is how a stale claim re-enters a live one.

Read the whole target, first line to last — every document of it.
```

- [ ] **Step 4: Narrow the second lens**

Replace:

```
Read the document again as a careful implementer who must build from this
text and has no other context: no conversation, no author to ask.
```

with:

```
Read the document again as a careful implementer who must build from
this text, the documents audited with it, and the documents its `spec:`
and `technical-design:` name, and has no other context: no
conversation, no author to ask.
```

- [ ] **Step 5: Give the coverage tell a pair of numbers**

Replace:

```
    coverage: <target line count> lines; highest line cited <n>
```

with:

```
    coverage: <file> <line count> lines, highest line cited <n>[; <file> …]
```

and extend the sentence below it:

```
The tell is how a partial read exposes itself, so report both numbers
even when they embarrass the run. A joint target reports a pair per
document: one document read whole while the other was skimmed is the
one risk peculiar to a pair, and a single pair of numbers cannot show
it.
```

- [ ] **Step 6: Verify all three edits landed and the old text is gone**

Run:

```bash
F=plugins/working-process/agents/integrity-auditor.md
grep -c 'design document' $F                                  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'Four cases fix what you read'        # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'never a target alone'                # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'the documents audited with it'       # expect 1
grep -c 'coverage: <file>' $F                                 # expect 1
grep -c 'coverage: <target line count>' $F                    # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'Your primary target is a spec,'      # expect 0
```

The last two are deletion assertions.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/agents/integrity-auditor.md
git commit -m "feat(working-process): audit a design spec and its technical design as one target"
```

---

### Task 15: The plan adversary reads a list of origins

**Files:**
- Modify: `plugins/working-process/agents/plan-adversary.md:46`, `:49`,
  `:51-55`, `:102`, and the generic dimensions list at `:57-70`

**Interfaces:**
- Consumes: the triage clause from Task 12 and the `change` set from
  Task 2.
- Produces: the `origin` list in the report schema and the coverage
  read of the `change` column.

- [ ] **Step 1: Measure the before state**

Run:

```bash
F=plugins/working-process/agents/plan-adversary.md
grep -c 'design document' $F                       # expect 2
grep -c '"origin": "plan" | "spec" | "both"' $F    # expect 1
grep -c '^### [0-9]' $F                                 # expect 4
```

- [ ] **Step 2: Rename the class in both sentences**

Replace:

```
Handed a spec (a design document, not an implementation plan)? Decline
```

with:

```
Handed a judged document (a design spec or a technical design, not an
implementation plan)? Decline
```

Replace `to a design document and would misfire as findings.` with
`to a judged document and would misfire as findings.`

- [ ] **Step 3: Make `origin` a list**

Replace:

```
          "origin": "plan" | "spec" | "both",
```

with:

```
          "origin": ["design-spec" | "technical-design" | "implementation-plan", …],
```

- [ ] **Step 4: Retire the old values from the card's own prose**

The schema is not the only place the card names `origin` values.
Replace:

```
Naming a document is not reviewing it. A finding whose `origin` is
`spec` or `both` says where the defect traces to and proposes no change
to the spec, so this boundary holds: what to do about a spec-origin
finding is the dispatcher's, and its own rules hold one for the
developer unless a written decision licenses the edit.
```

with:

```
Naming a document is not reviewing it. A finding whose `origin` names a
judged document — a design spec or a technical design — says where the
defect traces to and proposes no change to that document, so this
boundary holds: what to do about such a finding is the dispatcher's,
and its own rules hold one for the developer unless a written decision
licenses the edit.
```

- [ ] **Step 5: Add the coverage read of the `change` column**

Append to the generic dimensions:

```
### 5. Coverage of the technical design's parts

Where the plan's `technical-design:` names a document, read its Parts
table. The plan must cover every part marked `new`, `changed` or
`retired`; one part may span several tasks and one task several parts,
and a part carried as `unchanged` context needs none. An uncovered part
is an Important finding whose `origin` is `implementation-plan`. A `change` value
outside `new | changed | retired | unchanged` is an Important finding
whose `origin` is `technical-design`: the set is closed, and an unknown
value would otherwise slip past this dimension unchecked.

The `**Interfaces:**` blocks are read here too. Where the plan names a
technical design, those blocks reference the contracts that design
defines and say which part of one each task implements or changes; a
block that redefines a contract independently is an Important finding
whose `origin` is `implementation-plan`. Where no technical design is
named, the existing plan convention stands and this paragraph is
silent.
```

- [ ] **Step 6: Verify**

Run:

```bash
F=plugins/working-process/agents/plan-adversary.md
grep -c 'design document' $F                            # expect 0
grep -c '"origin": \["design-spec"' $F                  # expect 1
grep -c '"origin": "plan"' $F                           # expect 0
grep -c '`spec` or `both`' $F                           # expect 0
grep -c 'spec-origin' $F                                # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'Coverage of the technical design'  # expect 1
grep -c '^### [0-9]' $F                                 # expect 5
```

The two zeros are deletion assertions. A card whose prose still admits
`both` while its schema cannot emit it contradicts itself, which is the
defect class this very agent is dispatched to find.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/agents/plan-adversary.md
git commit -m "feat(working-process): read origin as a list and cover the design's parts"
```

---

### Task 16: The propagation auditor's class and the pointer pair

**Files:**
- Modify: `plugins/working-process/agents/propagation-auditor.md:3`
  (description) and its duty list

**Interfaces:**
- Consumes: the pointers from Task 6.
- Produces: the pointer-pair check in the agent that gates every
  expensive dispatch.

- [ ] **Step 1: Measure the before state**

Run:

```bash
F=plugins/working-process/agents/propagation-auditor.md
grep -c 'a spec or plan' $F      # expect 1
grep -c 'technical-design' $F    # expect 0
```

- [ ] **Step 2: Widen the class in the description**

Replace `Mechanical propagation audit of a spec or plan before an
expensive dispatch` with `Mechanical propagation audit of a design spec,
a technical design or a plan before an expensive dispatch`.

- [ ] **Step 3: Add the pointer-pair duty as a ninth numbered duty**

The card's duties are `### 1.` through `### 8.` headings, not bullets,
and the rule's table numbers its rows against them. Add after duty 8's
last paragraph:

```
### 9. The pointer pair

Where a design spec carries `technical-design:`, or a technical design
carries `spec:`, open both targets and confirm each names the document
that names it. A pointer resolving to a missing file, or to a document
pointing elsewhere, is a hit — the pair identifies the integrity
audit's target, so a broken half silently narrows what the next audit
reads.

A plan is scoped differently and must not be read as half a pair. Its
`spec:` names a design spec, which never names the plan back; what is
checked there is that its `spec:` and `technical-design:` name a design
spec and the technical design that design spec names. A plan whose two
pointers disagree with the pair is a hit; a plan whose `spec:` is not
named back is not.
```

The second paragraph is what keeps this duty from firing on every plan
in the repository: the reciprocity check belongs to the design spec and
its technical design alone.

- [ ] **Step 4: Verify**

Run:

```bash
F=plugins/working-process/agents/propagation-auditor.md
grep -c 'a design spec, a technical design or a plan' $F   # expect 1
grep -c 'a spec or plan' $F                                # expect 0
grep -c '^### 9\. The pointer pair' $F                     # expect 1
grep -c '^### [0-9]' $F                                    # expect 9
tr -s '[:space:]' ' ' < $F | grep -c 'is not named back is not'  # expect 1
```

The count of `###` headings must equal the duty count the
propagation-duties rule now states, or the rule's last column points at
a duty that does not exist.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/agents/propagation-auditor.md
git commit -m "feat(working-process): check the pointer pair in the propagation audit"
```

---

### Task 17: The process-status skill covers the new directory

**Files:**
- Modify: `plugins/working-process/skills/process-status/SKILL.md:3`

The skill's body owns nothing but running the published commands, so the
directory it covers lives in its `description:` alone.

**Interfaces:**
- Consumes: the directory from Task 3.

- [ ] **Step 1: Measure the before state**

Run:

```bash
grep -c 'docs/specs and docs/plans' plugins/working-process/skills/process-status/SKILL.md
```

Expected: `1`.

- [ ] **Step 2: Widen the description**

Replace `a status pass over docs/specs and docs/plans` with
`a status pass over docs/specs, docs/technical-designs and docs/plans`.

- [ ] **Step 3: Verify**

Run:

```bash
F=plugins/working-process/skills/process-status/SKILL.md
grep -c 'docs/specs, docs/technical-designs and docs/plans' $F   # expect 1
grep -c 'docs/specs and docs/plans' $F                            # expect 0
```

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/skills/process-status/SKILL.md
git commit -m "feat(working-process): cover technical designs in the status pass"
```

---

### Task 18: The plugin README

**Files:**
- Modify: `plugins/working-process/README.md:6-9` (the flow line), `:18`
  (the architect paraphrase), `:47-49` (the adversary paraphrase),
  `:53-54` (the propagation-auditor paraphrase), `:66-68` (the
  integrity-auditor paraphrase), `:133` (the `integrity` field row),
  `:184-192` (the Rules payload enumeration and its count)

**Interfaces:**
- Consumes: every earlier task. This is the reader-facing summary and it
  is edited last, so it describes what shipped rather than what was
  planned.

- [ ] **Step 1: Measure the before state**

Run:

```bash
F=plugins/working-process/README.md
grep -c 'design document' $F                       # expect 1
grep -c 'sha: <short-hash>' $F                     # expect 1
grep -n 'idea → brainstorming' $F
```

- [ ] **Step 2: Put the step in the flow line**

Replace:

```
idea → brainstorming (spec) → grilling-session → architect review →
integrity audit → writing-plans (plan) → plan-adversary →
```

with:

```
idea → brainstorming (design spec) → grilling-session → architect
review → technical design (when the repository has code) → integrity
audit → writing-plans (plan) → plan-adversary →
```

- [ ] **Step 3: Rename the class in the architect paraphrase**

Replace `or any design document dispatched standalone; verdict` with
`or any judged document dispatched standalone; verdict`.

- [ ] **Step 4: Extend the `integrity` field row**

Replace the `Values` cell `` `<ISO date> (sha: <short-hash>)` `` with

```
`<ISO date> (sha: <short-hash>[; with: <file>@<short-hash>])`
```

and append to its `Meaning` cell:

```
; where a design spec names a technical design the two are audited as one target and one stamp records the pair, on the design spec
```

- [ ] **Step 5: Retire the premises in three more paraphrases**

Replace `handed a spec it declines toward the `architect`` with
`handed a judged document it declines toward the `architect``.

Replace `the mechanical audit of a spec or` with
`the mechanical audit of a design spec, a technical design or a`.

Replace `the document as an implementer who must build from that text
alone.` with `the document as an implementer who must build from that
text and whatever was audited with it.`

- [ ] **Step 6: Re-count the Rules payload, which Task 2 changed**

The README enumerates the rule files and states their number; Task 2
ships a seventh. Replace:

```
The plugin ships six rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, ticket frontmatter, the propagation
duties keyed by the edit that triggers them (`propagation-duties.md`,
loaded while a spec, plan or domain document is open), and the
```

with:

```
The plugin ships seven rule files in `rules/` — the preferred workflow
(always loaded once installed), frontmatter and lifecycle for judged
documents and plans, what a technical design must contain
(`technical-design.md`, loaded while one is open), Process directory
conventions, ticket frontmatter, the propagation duties keyed by the
edit that triggers them (`propagation-duties.md`, loaded while a design
spec, technical design, plan or domain document is open), and the
```

- [ ] **Step 7: Verify, and sweep the plugin for the retired phrase**

Run:

```bash
grep -rc 'design document' plugins/working-process/ | grep -v ':0$'
grep -c 'seven rule files' plugins/working-process/README.md   # expect 1
grep -c 'six rule files' plugins/working-process/README.md     # expect 0
ls plugins/working-process/rules/*.md | wc -l                  # expect 7
grep -rc 'a spec or plan\|build from that text alone\|handed a spec' \
  plugins/working-process/README.md | grep -v ':0$'
```

Expected: no output from the first and last, `1`, `0`, `7`. The stated
count and the directory listing must agree — a README that counts its
own payload wrong is the failure this check exists for. The first and
last lines are the Global Constraint's closing sweep.

- [ ] **Step 8: Commit**

```bash
git add plugins/working-process/README.md
git commit -m "docs(working-process): put the technical design in the README flow"
```

---

### Task 19: Changelog and the dogfooding version

**Files:**
- Modify: `plugins/working-process/CHANGELOG.md`
- Modify: `plugins/working-process/.claude-plugin/plugin.json`

**Interfaces:**
- Consumes: every earlier task.

- [ ] **Step 1: Measure the before state**

Run:

```bash
head -8 plugins/working-process/CHANGELOG.md
grep '"version"' plugins/working-process/.claude-plugin/plugin.json
```

- [ ] **Step 2: Write the `## Unreleased` entry**

Add at the top of the changelog, under its one-line preamble:

```markdown
## Unreleased

- New `technical-design` rule: a third document class between the design
  spec and the plan, saying what a thing is made of — section skeleton,
  the definitions of part, contract and state, and the closed `change`
  value set.
- The consumption gate offers the document where the repository has
  code, and runs in passes when the offer is accepted.
- A design spec and its technical design are audited as one target, with
  one `integrity:` stamp on the design spec naming both.
- `origin` on a plan-adversary finding is a list of named documents;
  `both` retires.
- The class a design spec and a technical design share is named
  `judged document` on every agent card and in the README; the phrase
  those surfaces carried before is retired.
```

- [ ] **Step 3: Set the dogfooding version**

The topic branch dogfoods this plugin, so it takes a `-dev` suffix
hanging off a version above what `develop` carries. Read the current
`develop` version first and bump the minor, then suffix:

```bash
git show develop:plugins/working-process/.claude-plugin/plugin.json | grep version
```

Set `version` to `0.18.0-dev.1.technical-design-step`. Measured
2026-09-17: `develop` carries `0.17.0`, and no `-dev.<n>.` has ever been
minted in this repository, so this topic is the counter's first use and
takes `1`. Re-read `develop` before committing — if it moved, the
version hangs off whatever it carries now and the counter takes the next
integer above the highest one develop holds.

The counter is its own dot-separated identifier, so semver compares it
numerically and successive dogfooding builds of one topic order
correctly: `dev.1.x` < `dev.2.x` < `dev.10.x`. Measured 2026-09-17
against the `semver` reference implementation, alongside the two
spellings that fail — `dev.<n>-<slug>` puts the number inside an
alphanumeric identifier and sorts `1 < 10 < 2`, while a bare
`dev.<slug>` sorts alphabetically by topic and carries no order at
all. This topic is the counter's first use, so it takes `1`.

- [ ] **Step 4: Verify**

Run:

```bash
claude plugin validate plugins/working-process
grep -c '^## Unreleased$' plugins/working-process/CHANGELOG.md   # expect 1
```

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/CHANGELOG.md plugins/working-process/.claude-plugin/plugin.json
git commit -m "chore(working-process): changelog and dogfooding version for the technical-design step"
```

---

## Deviations from the spec

- **`process-artifacts.md` is path-scoped, not always-on.** The spec's
  Parts table calls it an always-on rule. The file carries a `paths:`
  block of five globs, so Task 3 adds the new directory to that block as
  well as to the prose list. Without the glob the rule would not load
  for a technical design, and the first-create question it owns would
  never fire for the new directory. The spec's row is wrong about the
  kind; it is right about what the part owns.

- **The dogfooding version uses a counter the versioning rule does not
  yet carry.** `.claude/rules/plugin-versioning.md` describes
  `X.Y.Z-dev.<discriminator>` with no counter, while Task 19 mints
  `0.18.0-dev.1.technical-design-step`. The counter is the developer's
  decision of 2026-09-17 — `n` separates the successive dogfood releases
  of successive topics and increments on `develop`, which is the owner
  the counter lacked when an earlier attempt at it was declined. The
  rule's amendment is deliberately not part of this branch, so the
  divergence stands until that separate change lands. Task 19 follows
  the decision, not the current rule text.

## What this plan does not do

- It creates no `docs/technical-designs/` directory in this repository.
  The plugin ships the contract; this repo's product is prose and it
  declines the offer. The first project to accept the offer creates the
  directory, and the first-create question fires there.
- It writes no declaration surface. Where a project records the
  declaration is deferred by the spec, so this repo keeps receiving the
  offer at every consumption gate until that question is settled. That
  is a known cost, recorded in the spec.
- It renames no existing spec to `-spec.md`, and adds no
  `<domain>-technical-design` skill. Both are out of scope in the spec.
- **It changes no plan template.** The `**Interfaces:**` block shape
  belongs to `superpowers:writing-plans`, another vendor's plugin, and
  modifying it is not this work. The spec's sentence about the interface
  prescription leaving the plan is delivered instead as a contract on
  how the existing blocks are filled: where a technical design exists it
  defines the interfaces, and the blocks reference its contracts rather
  than restating them (Task 6, and the adversary's dimension 5 in Task
  15). A separate ticket earns its keep only if validation shows the
  existing block shape cannot reference a design usefully.

## Review rounds

### 2026-09-17 — plan-adversary, fable 5.1, blocking (round 1, full-document)

Full-document read. Eleven Important, eight Minor. Record:
`.claude/working-process/2026-09-17-technical-design-step/plan-adversary-round-1.md`.
Every citation the report supplied was checked against what it names
before any line below was written; none missed.

- fixed 2026-09-17 — [Important] Task 5 promised "every branch reading
  the class" and edited two, leaving four spec/plan binaries untouched,
  one of them read verbatim by `process-status`, which is told never to
  supply an owner from its own knowledge; license: ADR 0004, where the
  rule's branches say which class they mean rather than which filename;
  Task 5 now names six branch sentences explicitly, its Interfaces
  claim says six rather than every, and its verify step carries a
  deletion assertion per branch.
- fixed 2026-09-17 — [Important] `origin: spec` and `both` survived in
  two shipped files no task touched, so the adversary's card would
  contradict its own schema; license: the design spec, where `both`
  retires with the value; `plan-adversary.md:51-55` joins Task 15 and
  `spec-plan-lifecycle.md:229-231` joins Task 5, both with deletion
  assertions.
- fixed 2026-09-17 — [Important] Task 5 wrote "the same consumption-gate
  semantics for a stale stamp" while Task 7 wrote "carries no
  `integrity:` of its own", and the plan dropped the spec's reconciling
  sentence; license: the design spec's own sentence, quoted verbatim;
  Task 5 Step 6 now carries "One mechanism it shares rather than owns…".
- fixed 2026-09-17 — [Important] Tasks 9 and 16 appended a bullet to a
  "duty list" that is a table in one file and `### 1.`–`### 8.` headings
  in the other, and left the counters binding them stale; license: the
  files' own structure and the counters' own derivation; Task 9 adds a
  table row and re-derives eight/nine to nine/ten, Task 16 adds
  `### 9.`, and both verify the heading count against the stated one.
- fixed 2026-09-17 — [Important] the card's pointer-pair duty was scoped
  wider than the rule's and would have turned every plan's `spec:` into
  a hit, while the spec's third check — a plan's two pointers agreeing
  with the pair — had no deliverer; license: the design spec, which
  scopes reciprocity to the design spec and its technical design and
  states the plan clause separately; Task 16's duty now separates the
  two and says a plan whose `spec:` is not named back is not a hit.
- fixed 2026-09-17 — [Important] the README counts "six rule files" and
  Task 2 ships a seventh; license: the counter's own derivation; Task 18
  gains the enumeration, the count, and a check comparing the stated
  number against `ls rules/*.md | wc -l`.
- fixed 2026-09-17 — [Important] the rule said a recorded declaration
  binds while nothing said where a session reads one, so no project
  could ever silence the offer; license: the design spec, which fixes
  that a session reads it without being told where to look and names
  the `CLAUDE.md` shape an implementation may assume; Task 10's block
  now names that surface.
- fixed 2026-09-17 — [Important] the new rule text named the
  `system-designer-session` skill and the `architect` agent
  unconditionally; license: the repo's plugin-authoring rule, where
  mentions of skills and agents inside rule text are conditional because
  committed project-level rules load for people without the plugin;
  both mentions in Tasks 10 and 11 now carry "when available".
- fixed 2026-09-17 — [Important] the spec's "One offer, and what it
  discharges" paragraph had no delivering task and the lifecycle rule's
  discharge paths still described one document; license: the design
  spec's paragraph; the one-offer sentence joins Task 10 and the
  discharge widening joins Task 7 as its own step.
- fixed 2026-09-17 — [Important] the glossary's Consumption gate entry
  still carried the broad ordering the spec's integrity ruling withdrew,
  so Task 8's text contradicted a canonical term; license: the design
  spec's narrowed ordering, ruled 2026-09-17; the entry now reads
  "writing the technical design and applying its review dispositions
  precede the joint integrity audit", and Task 1 Step 4 greps that
  phrase instead of counting items. The glossary edit lands in this
  plan's wave because the spec is stamped and its ledger closed.
- fixed 2026-09-17 — [Important] Task 10's insertion point was
  positional and Step 3's "the offer" could have referred to the pair
  offer two sentences above; license: the propagation duty on prescribed
  blocks, which requires a byte-exact anchor; Step 2 anchors on
  `absent. The brief` and Step 3 says "the technical-design offer".
- fixed 2026-09-17 — [Minor] Task 1 called the glossary and ADR
  uncommitted and committed them in a step that would have found nothing
  to commit; license: the repository state, `dc85b9b`; the task states
  they are committed and its last step commits nothing.
- fixed 2026-09-17 — [Minor] Task 7's anchor named a paragraph end that
  does not exist — the sentence closes mid-bullet and the bullet runs
  twelve more lines; license: the file itself; the anchor moves to the
  bullet's real last line.
- fixed 2026-09-17 — [Minor] four paraphrase sites kept the premises the
  tasks retire, in the auditor's description and three README bullets;
  license: the design spec, which retires the phrase and narrows the
  lens; Task 14 Step 2 rewrites the description's three clauses and Task
  18 gains the three README sites.
- fixed 2026-09-17 — [Minor] the lifecycle rule's title and opener
  stayed binary after its scope widened to three classes; license: the
  design spec, which puts technical designs under this rule; Task 5
  Step 3 rewrites both.
- fixed 2026-09-17 — [Minor] the new coverage dimension named `origin`
  values in prose while the schema three lines up emits literals;
  license: the schema in the same task; the dimension writes the
  literals. Renumbered 5 at round 2.
- fixed 2026-09-17 — [Minor] Task 11 quotes a card sentence Task 13
  writes, an ordering dependency the plan did not state; license: the
  propagation duty on prescribed blocks, which this would breach by our
  own hand; Task 11's Interfaces block states the dependency outright.
- fixed 2026-09-17 — [Minor] the changelog credited the plugin with
  glossary terms that live in this repository and not in the plugin;
  license: the changelog's own scope line; the bullet keeps the shipped
  half only.
- fixed 2026-09-17 — [Minor] two spec sentences had neither a task nor a
  not-done line: the domain skill naming its technology's markers, and
  the interface prescription leaving the plan; ruling: 2026-09-17; the
  marker sentence joins Task 10's block, and the interface sentence is
  delivered as a contract rather than a template change — where a
  technical design exists it defines the interfaces and the plan's
  `**Interfaces:**` blocks reference its contracts rather than restating
  them (Task 6 Step 4, enforced by the adversary's new coverage
  dimension in Task 15), with the `superpowers:writing-plans` template
  explicitly out of
  scope. The developer chose this over both declaring the sentence
  undelivered and editing another vendor's plugin.
- hit fixed 2026-09-21 — Task 9's before-state step still counted
  bullet-list lines, a measurement left over from the bullet its Step 3
  no longer writes; it counts the duty table's rows instead.
- hit fixed 2026-09-21 — Task 9's verify step expected twelve table
  lines, counting a separator row that `^| ` never matches because it
  carries no space after the pipe; measured against the file, the
  before count is ten and the after count eleven.
- signal 2026-09-17 — the reviewer judges a second round worth its cost
  after this wave and says it should be diff-scoped: most Important
  findings are one class, consumers no task enumerated, which a
  propagation gate should catch once the plan names those sites. It
  expects round two to close on `concerns` or `LGTM`, and judges this
  round's leftovers insufficient to earn a third without new evidence.

### 2026-09-21 — plan-adversary, fable 5.1, blocking (round 2, diff-scoped)

Diff-scoped over round one's fix wave. Two Important, six Minor. Record:
`.claude/working-process/2026-09-17-technical-design-step/plan-adversary-round-2.md`.
Every citation was checked against what it names; none missed. The
reviewer read the recorded deviation and declined to refute it, having
verified in the `superpowers:writing-plans` skill that the
`**Interfaces:**` block is indeed that plugin's.

- fixed 2026-09-21 — [Important] round one's fix hung the conditional on
  the offer rather than on the tool, so the technical design would never
  be offered where the skill is absent and the work would vanish with
  its tool; license: this rule's own preamble, "a tool that is not
  installed disables its suggestion — never the work itself", and the
  design spec's degradation path, where a document with no covering
  skill is written from generic knowledge; the offer now fires on
  declaration and marker alone, `when available` sits on the skill, and
  the block says outright that the document is still written without
  one.
- fixed 2026-09-21 — [Minor] the backstop widened to "no judged
  document" while the next sentence of the same paragraph stayed
  spec-only, leaving a seventh branch one line below the sixth; license:
  ADR 0004, as for the other six; Task 5 Step 4 extends through that
  sentence and its verify step asserts the old wording is gone.
- fixed 2026-09-21 — [Minor] the new coverage dimension was numbered 6
  in a list whose last heading is 4, and the before-state count carried
  no expected value to catch it; license: the count's own derivation
  from the file; the dimension is 5, the before count expects 4 and the
  after count 5, and three stale references to "dimension 6" are
  rewritten.
- fixed 2026-09-21 — [Minor] the rewritten auditor description said the
  implementer lens reads "the documents its pointers name" while the
  body two steps later excludes `revises:` — the description restating a
  premise the body retires, which is the defect that step existed to
  remove; license: the design spec, which narrows context to the two
  pointers; the description names `spec:` and `technical-design:`.
- fixed 2026-09-21 — [Minor] Task 19 wrote the retired phrase into the
  changelog one task after Task 18's plugin-wide sweep expects zero, so
  the sweep passed on its run and failed on a re-run, breaking the
  plan's own Global Constraint; license: that constraint; the changelog bullet
  names the new term and describes the old one without spelling it.
- held — [Important] the discharge widening covers the audit arm only,
  so with one joint offer for two documents a decline leaves undefined
  whether the technical design's chain debt is discharged and which
  headings are annotated; question: does declining the joint offer
  discharge the chain debt of both documents, or only the design
  spec's?;
  options: (a) both, since one offer covered both and the developer
  released both by the same act — recommended, because the alternative
  makes one offer produce two different outcomes; (b) only the design
  spec's, leaving the design's debt to its own later reading.
- held — [Minor] after Task 10 names `CLAUDE.md` as the readable
  declaration surface, the plan's "writes no declaration surface" bullet
  describes a cost the plan itself just made avoidable, and the spec's
  "this repository declines by declaration" has no deliverer; question:
  does this change write this repository's own declaration, dogfooding
  the surface it ships?; options: (a) yes, one step adding the
  declaration to this repo's `CLAUDE.md` — recommended, since the
  surface now exists and the alternative leaves us clicking the offer
  away at every gate; (b) no, and the bullet is rewritten to say the
  surface exists and this repo's declaration is deliberately a separate
  change.
- held — [Minor] the wave uses "the pair" for the design spec and its
  technical design while the glossary already uses "pair offer" and
  "pair question" for the two-arm chain-debt question, and one block
  puts both senses two sentences apart; question: which sense keeps the
  bare word, and what is the other called?; options: (a) mint a glossary
  term for the document pair — `audit pair` reads best — and leave
  "pair offer" alone, recommended because the offer sense is already
  written into three glossary entries and a shipped rule; (b) rename the
  offer side; (c) qualify every occurrence in prose and mint nothing.
  This is spec-origin: the design spec is where the second sense enters.
- signal 2026-09-21 — the reviewer judges a third round worth its cost
  only as the confirming full-document round the plan already owes, not
  as another diff-scoped pass. It reads both Important findings as one
  class again — a fix pinned to the wrong noun, an extension stopped
  halfway down a list — and expects the confirming round to close on
  `concerns` or `LGTM`, with no material for a fourth absent new
  evidence.
