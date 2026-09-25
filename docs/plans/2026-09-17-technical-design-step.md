---
ticket: none
date: 2026-09-17
status: draft
adversary: concerns
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
six changed rules and skills, four changed agent cards and the plugin
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
- **An anchor that ends mid-line runs to the line's end.** A
  replacement whose anchor stops mid-line leaves the rest of that line
  glued to the block's last line. Every anchor here ends at a line's
  end, and where the original line's tail matters the replacement
  carries it.
- **Counting after `tr` proves existence, not occurrence.** `tr`
  collapses a file to one line, so `grep -c` then reports 1 however
  many times a phrase appears. Where a check must prove a block landed
  once, it counts with `grep -o … | wc -l`, and it anchors on a phrase
  unique to the block rather than one the file already carries.
- **Checks are written for GNU grep and name the behaviour they need.**
  `-H` wherever a filename prefix is filtered on, since GNU grep prints
  none for a single named file; `-e` before any pattern that starts with
  `-`. Run them where `grep` is not wrapped by a shell function — for
  example `env -i PATH=/usr/bin:/bin bash --noprofile --norc` — because
  a wrapper that resolves to a different implementation answers a
  different question.
- **Every check carries its expected value as `# expect N`.** A check
  whose expectation is stated only in prose is a check no tool runs; one
  such check in Task 2 failed unnoticed for two rounds. The one
  exception is `claude plugin validate`, whose result is its exit
  status.
- **Every insertion quotes its anchor.** Each one reads "After the
  line:" or "After the lines:" on a line of its own — one spelling per
  line count, the same instruction — followed by the anchor lines in a
  fenced block and then the block to insert. A block that opens with a
  list marker or a table pipe joins the list or table it follows
  directly; any other block is a paragraph or heading of its own, one
  blank line after its anchor.
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
- Produces: the glossary terms every later task's prose leans on —
  `Design spec`, `Judged document`, `Technical design`, `Part`,
  `Contract`, `Vocabulary gap`, `Audit pair`, and `Origin` in its list
  form — plus ADR 0004 as the citable decision behind the class.

- [ ] **Step 1: Confirm every term the spec mints exists**

Run:

```bash
for t in "Design spec" "Judged document" "Technical design" "Part" \
         "Contract" "Vocabulary gap" "Origin" "Consumption gate" \
         "Audit pair"; do
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

`change` takes one value from the closed set `new | changed | retired |
unchanged`, and a domain adds no value to it: the column steers the
process, so its meaning belongs to the core, and a value outside the set
is an error the author corrects rather than a part that quietly escapes
the plan's coverage check.

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
kinds of contract, homes of state — from the domain's own skills:
through the Domain expertise duty the personas carry when the
working-process plugin is installed, which has them scan and load those
skills, and by reading the skills directly otherwise. No discovery
convention of its own ships here.

A kind of part, contract, or home of state that no domain skill names is
recorded in the document as a **vocabulary gap**: the author names the
kind, writes the gap down, and the architect round, when that agent is
available, judges the boundary, which is what it judges in any case.
Accumulated vocabulary gaps are either the specification of a
`<domain>-technical-design` skill or the evidence that none is needed.

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
grep -c '^| [0-9]' $F                       # expect 7
tr -s '[:space:]' ' ' < $F | grep -c 'new | changed | retired | unchanged'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'when that agent is available, judges the boundary'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'personas carry when the working-process plugin is installed'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'the personas already carry'  # expect 0
awk 'length > 72' $F | grep -v '^|' | wc -l  # expect 0
```

Each expected value is on its line: `7` skeleton rows (1–6 plus the
`7–8` row), `1` for the closed set, which wraps in the rule text and so
is counted through `tr`, and `0` over-wide prose lines.

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

After the line:

```
  - "docs/plans/**"
```

in the frontmatter, add:

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
  and the ticket-sourcing sentence at `:54`

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

- [ ] **Step 3: Let a technical design inherit its design spec's ticket**

Replace:

```
for one unit of work — a plan inherits its spec's ticket, and artifacts
```

with:

```
for one unit of work — a technical design and a plan inherit their
design spec's ticket, and artifacts
```

- [ ] **Step 4: Verify the catch-all no longer claims the directory**

Run:

```bash
F=plugins/working-process/rules/ticket-frontmatter.md
tr -s '[:space:]' ' ' < $F | grep -c 'technical designs and plans'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'Every other document under `docs/`'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c "a technical design and a plan inherit their design spec's ticket"  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c "a plan inherits its spec's ticket"  # expect 0
```

The second still stands: it is a catch-all, and the first bullet now
takes the new directory out of its reach.

- [ ] **Step 5: Commit**

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

After the line:

```
  - "docs/specs/**"
```

in the frontmatter, add:

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

After the lines:

```
written, while only the frontmatter stamp waits for the confirming
full-document round.
```

which close the offers paragraph, add:

```
A technical design is a judged document and takes the design spec's side
of every branch in this rule: the same fields, the same
consumption-gate semantics for a stale stamp, the same owner for an
unresolved verdict, and the same pair offer against chain debt. It is
not grilled — grilling stress-tests terminology against the project
glossary, and a technical design mints none: its vocabulary comes from
its design spec, which was grilled, and from the domain's own skills.
The names it does mint are part and component names, checked against
those skills where one exists and recorded as a vocabulary gap where
none does.

One mechanism it shares rather than owns: the integrity check is due on
it like any judged document, and one audit of the audit pair — the
design spec together with the technical design it names — discharges it,
so the `integrity:` stamp sits on the design spec and names both.
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
spec: ../specs/<file>.md   # plans and technical designs: the design spec this document descends from; inline list when several, on a plan
technical-design: ../technical-designs/<file>.md   # optional: on a design spec, the technical design that develops it; on a plan, the technical design of each design spec it descends from that has one — inline list when several, each path relative to the plan
```

- [ ] **Step 3: Write the five rules that keep the pair honest**

The field notes are the bullets under the frontmatter example.

After the line:

```
  up front, omitted entirely when there is no topic branch.
```

which ends the last of them, add:

```
- `technical-design:` is optional and appears once the technical design
  exists, so its absence means there is none rather than one nobody
  linked. It is new in kind: every other pointer records where a
  document came from, while this one names a document written later,
  and it gives a reader holding the design spec the structure that
  develops it. The author who creates the design writes both ends in
  the same turn — the design's `spec:` and the design spec's
  `technical-design:`. A plan's `technical-design:` names, for every
  design spec its `spec:` names that has a technical design, that
  technical design — an inline list when several, each entry the same
  document the design spec's own pointer names, its path written
  relative to the plan's directory rather than copied. A design spec
  with no technical design contributes no entry, so a plan from specs
  `a` and `b`, where only `a` names a design, carries that one design.
  One technical design per design spec.
```

- [ ] **Step 4: Say what the pointer does to a plan's interface blocks**

A plan naming a technical design must not redefine what that design
already defines.

After the line:

```
  One technical design per design spec.
```

which is Step 3's last line, add:

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
tr -s '[:space:]' ' ' < $F | grep -c "its path written relative to the plan's directory rather than copied"  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'contributes no entry'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'carries that `technical-design:` as well as its'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'where it carries both they must agree'  # expect 0
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
lines, through the hash command the pair clause depends on.

After the line:

```
  edits included; any change re-arms the stamp, a typo fix included.
```

which is the bullet's real last line, add:

```
  A design spec that names a technical design is audited with it as one
  target — an **audit pair** — and one stamp records it. The stamp
  lives on the design spec, names both documents and both body hashes,
  and the technical
  design carries no `integrity:` of its own — it owes the check like any
  judged document and discharges it jointly. The value takes the form
  `integrity: <date> (sha: <own-hash>; with: <file>@<their-hash>)`,
  where `<file>` is exactly the value the design spec's
  `technical-design:` pointer carries, read relative to the design
  spec's directory, so the gate can check that the recorded value still
  equals the pointer. Changing either document unsettles the pair, and
  the gate
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
applied and before the `integrity:` stamp — and where that audit read an
audit pair, it discharges the debt of both documents it read, annotating
each document's own unannotated diff-scoped `LGTM` headings; and any
later full-document
```

The decline path takes the same widening and a bound. Replace:

```
dispatcher writes it in every case: the developer declining the gate's
pair offer, written in the decline turn before the work that decline
licenses begins; an integrity audit, written once its dispositions are
```

with:

```
dispatcher writes it in every case: the developer declining the gate's
pair offer, written in the decline turn before the work that decline
licenses begins, and written for every document that offer named — a
declined offer over an audit pair discharges the chain debt of both.
What a decline never does is stand in for the audit itself: it writes
no `integrity:` stamp, leaves every other open finding open, and closes
no `blocking` verdict. "Do not run the audit" is a release from the
chain debt the offer named and from nothing else; an integrity audit,
written once its dispositions are
```

Both anchors in this step end at a line's end: the one above ends where
the next anchor, `applied and before the `integrity:` stamp; …`,
begins, so the two replacements touch disjoint lines and neither leaves
a tail glued to the other.

- [ ] **Step 5: Verify both directions**

Run:

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c 'with: <file>@<their-hash>' $F     # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'carries no `integrity:` of its own'   # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'recomputes both hashes'   # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'both documents it read'   # expect 1
tr -s '[:space:]' ' ' < $F | grep -c "exactly the value the design spec's"  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c "the technical design's path relative to the design"  # expect 0
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
  paragraph, and the two authoring enumerations at `:513-515` and
  `:546-547`

**Interfaces:**
- Consumes: the class branches from Task 5. **Task 5 must land first**
  — its Step 4 rewrites the sentence this task anchors on, so the anchor
  below is the post-Task-5 wording and does not exist before Task 5.
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

After the lines:

```
latest. Writing a plan from a judged document is that same seam: its
held questions are asked before the plan is written, whoever writes it.
```

which are Task 5 Step 4's wording, add:

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

- [ ] **Step 3: Name the technical design in two authoring enumerations**

Two sentences further down the section list the authoring phase as
spec and plan alone. Replace:

```
is about to start. During authoring — spec drafting, grilling, review
rounds, plan writing — it never makes that suggestion; the documents'
```

with:

```
is about to start. During authoring — spec drafting, grilling,
technical-design writing, review rounds, plan writing — it never makes
that suggestion; the documents'
```

and replace:

```
The loop runs on that branch for the whole authoring phase — the spec's
rounds and the plan's alike — and the topic branch takes it at the
```

with:

```
The loop runs on that branch for the whole authoring phase — the design
spec's rounds, the technical design's and the plan's alike — and the
topic branch takes it at the
```

- [ ] **Step 4: Verify**

Run:

```bash
F=plugins/working-process/rules/spec-plan-lifecycle.md
tr -s '[:space:]' ' ' < $F | grep -c 'The gate therefore runs in passes'     # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'precedes the joint integrity audit'    # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'in the same turn and by the same hand' # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'technical-design writing, review rounds'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c "the technical design's and the plan's alike"  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'spec drafting, grilling, review rounds'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c "the spec's rounds and the plan's alike"  # expect 0
```

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): run the consumption gate in passes"
```

---

### Task 9: The propagation auditor's author-facing duty

**Files:**
- Modify: `plugins/working-process/rules/propagation-duties.md:1-6`
  (`paths:`), its duty list, and the loads-at sentence at `:38-39`

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

After the line:

```
  - "docs/specs/**"
```

in the frontmatter, add:

```yaml
  - "docs/technical-designs/**"
```

- [ ] **Step 3: Add the pointer-pair duty as a table row**

The duties are a table keyed by the edit, not a bullet list.

After the line:

```
| copied a citation out of a review report | the file and line it names, read at the source | 8 |
```

which is the table's last row, add:

```
| added or repointed a `spec:` or `technical-design:` pointer | both targets; on a design spec or a technical design, that each pointer names the document that names it; on a plan, that its `technical-design:` entries resolve, from the plan's own directory, to exactly the technical designs its design specs name — none missing, none extra | 9 |
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

- [ ] **Step 5: Re-state where the rule loads**

Step 2 widens `paths:`, and the rule states its own loading in prose.
Replace:

```
shipped occurrence of the banned term — which is why this rule loads at
the domain directory as well as at specs and plans. And a count asserted
```

with:

```
shipped occurrence of the banned term — which is why this rule loads at
the domain directory as well as at design specs, technical designs and
plans. And a count asserted
```

- [ ] **Step 6: Verify, both counters against what they count**

Run:

```bash
F=plugins/working-process/rules/propagation-duties.md
grep -c '"docs/technical-designs/\*\*"' $F      # expect 1
grep -c '^| ' $F                                 # expect 11: header plus ten edit rows
grep -c 'nine duties fall due' $F                # expect 1
grep -c 'on a design spec or a technical design, that each pointer' $F  # expect 1
grep -c 'none missing, none extra' $F  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'as well as at design specs, technical designs and plans'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'as well as at specs and plans'  # expect 0
grep -c 'keyed by the ten edits' $F              # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'walks the same nine'  # expect 1
grep -c 'eight duties\|the nine edits\|same eight' $F   # expect 0
```

The last line is the deletion assertion, and it is the one that matters:
the old counters read as true prose and nothing but a recount catches
them.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/propagation-duties.md
git commit -m "feat(working-process): make the author check the pointer pair"
```

---

### Task 10: The workflow rule — the step and its gate offer

**Files:**
- Modify: `plugins/working-process/rules/workflow.md:36-56` (step 4,
  *Spec → plan*), including the audit sentence at `:38-41` and the
  pair-offer sentence at `:43-45`

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
   either direction; a session reads it from the project instructions
   Claude Code loads at session start — a `CLAUDE.md` at the repository
   root or in `.claude/` — or from the file such a note points at, which
   is the shape available until a standing home for a project's process
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
   two are then audited as one target — an audit pair. The gate makes
   one offer for that audit pair rather than one per document, and the
   offer
   names both documents, so declining it releases the chain debt of the
   two it named and nothing besides. Where the audit runs instead, it
   discharges that debt for both documents it read. The other arm stays
   per-document: choosing it dispatches one full-document architect
   round on each document, each discharging the debt of the one it read,
   and plan-writing waits for both verdicts. The brief
   confirms the auditor's two preconditions: every edit from the
```

- [ ] **Step 4: Name the class in the pair-offer sentence**

The sentence that sends a diff-scoped chain to the pair offer still
says "a spec". Replace:

```
   comparison. For a spec whose LGTM came from a diff-scoped chain the
   offer takes the pair form the verdict-agent dispatch subsection
   defines, and narrows as that definition says when the auditor is
```

with:

```
   comparison. For a judged document whose LGTM came from a diff-scoped
   chain the offer takes the pair-offer form the verdict-agent dispatch
   subsection defines — one pair offer for an audit pair, never one per
   document — and narrows as that definition says when the auditor is
```

The last line ends where the original did, so `   absent. The brief`,
Step 2's anchor, is untouched.

- [ ] **Step 5: Let the audit sentence read the pair**

Two lines above, the step still describes one document and one hash,
while Task 7 has the gate recompute both hashes of an audit pair. A
reader of this always-on rule alone would recompute the design spec's
hash, see a match, and never offer the audit after the technical design
changed. Replace:

```
   is available: a fresh-context read of the whole spec, returning
   defects and the questions an implementer would have to ask. The
   offer fires unless a standing `integrity:` stamp still matches the
   spec's recomputed body hash — a match means the standing stamp
```

with:

```
   is available: a fresh-context read of the whole design spec, and of
   its technical design where it names one, returning defects and the
   questions an implementer would have to ask. The offer fires unless a
   standing `integrity:` stamp still matches the recomputed body hash of
   every document the stamp names — a match means the standing stamp
```

The last line ends as the original did, so the next line and Step 4's
anchor stay untouched.

- [ ] **Step 6: Verify**

Run:

```bash
F=plugins/working-process/rules/workflow.md
tr -s '[:space:]' ' ' < $F | grep -c 'the declaration is the signal and the marker only raises the question'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'audited as one target'   # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'root or in `.claude/`'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'note at the repository root, or from'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'skill, when available, and write the technical design'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -o 'from generic knowledge and best effort' | wc -l  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'may name the markers of its technology'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'one offer for that audit pair'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'an audit pair'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'For a judged document whose LGTM'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'For a spec whose LGTM'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'every document the stamp names'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c "spec's recomputed body hash"  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'and plan-writing waits for both verdicts'  # expect 1
grep -c 'designer session' $F    # expect 0 — the glossary bans "session" for a skill
```

- [ ] **Step 7: Commit**

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
  architect card as Task 13 leaves it. The block paraphrases that card
  rather than quoting it, and the two tasks edit different files with
  no shared anchor, so numbering order is safe: between them the rule
  describes a card one task ahead of it, and nothing reads the card in
  that interval.
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

The offer paragraph is the block Task 10 Step 2 inserted, directly above
the paragraph opening `   Where the technical-design offer is accepted`.

After the lines:

```
   implementer no new responsibility split, placement, or ownership of
   state.
```

which close it, add:

```
   Accepted, the session opens the `system-designer-session` skill when
   it is available and reads the technical-design rule, installed beside
   this one, before drafting — a path-scoped rule loads only when a
   matching file is read, and none exists yet — then writes the document
   to `docs/technical-designs/` following it. It writes both
   ends of the pair in the same turn — the design's `spec:` and the
   design spec's `technical-design:` — so no audit ever meets a
   half-written pair. The reviewer is the `architect` agent when that
   agent is available, whose card admits any judged document dispatched
   standalone, with the propagation audit gating that dispatch as it
   gates every verdict dispatch. The plan-adversary stays on plans.
   The plan written afterwards carries, beside its `spec:`, a
   `technical-design:` entry for every design spec it descends from that
   names a technical design — the same document, its path rewritten
   relative to the plan's own directory — so the plan-adversary always
   has each design to read.
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
tr -s '[:space:]' ' ' < $F | grep -c "its path rewritten relative to the plan's own directory"  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'the second copied from its design spec'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'a path-scoped rule loads only when a matching file is read'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'following the technical-design rule that loads there'  # expect 0
```

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): name the technical design's author and reviewer"
```

---

### Task 12: The workflow rule — the triage clause and the remaining class branches

**Files:**
- Modify: `plugins/working-process/rules/workflow.md:333-339` (the
  triage clause), `:169-171` (the Process directories resolved before a
  verdict dispatch), `:526-537` (the chain-debt pair offer), and three
  enumerations at `:127-128`, `:131-132` and `:149-150`

**Interfaces:**
- Consumes: `Origin` in its list form from Task 1.
- Produces: the widened hold, which Task 15 makes the adversary's report
  schema able to express.

- [ ] **Step 1: Measure the before state**

Run:

```bash
grep -n -e 'A finding whose `origin` names the spec' plugins/working-process/rules/workflow.md
```

Expected: one line. The measurement is by content rather than by line
number, because Tasks 10 and 11 insert some forty lines above this
clause and a positional `sed` would print unrelated bullets.

- [ ] **Step 2: Widen the hold to the class**

Replace:

```
- A finding whose `origin` names the spec is held unless a written
  decision licenses the edit, since editing a spec from inside a plan
  review is design work; `both` holds the same way, and its `held`
  line names in `options:` which half is fixable at once. A licensed
  spec-origin fix lands in the spec's own ledger and the plan's line
  points at it, by the cross-document clause the spec-plan-lifecycle
  rule defines — which also leaves the spec's `integrity:` stamp
  stale, as any body edit does.
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
  clause the spec-plan-lifecycle rule defines — which also leaves the
  design spec's `integrity:` stamp stale, as any body edit to either
  document of an audit pair does.
```

The anchor runs to the end of the bullet, so the replacement ends a
sentence rather than leaving the original line's tail glued to its last
line. The tail itself changes too: for an audit pair the stamp that
goes stale is the design spec's, whichever document was edited.

- [ ] **Step 3: Name the new directory before a verdict dispatch**

Replace:

```
- Before dispatch, resolve any undecided Process directory
  (`docs/specs/`, `docs/plans/`) so the first-create question cannot
  interrupt the stamp turn.
```

with:

```
- Before dispatch, resolve any undecided Process directory
  (`docs/specs/`, `docs/technical-designs/`, `docs/plans/`) so the
  first-create question cannot interrupt the stamp turn.
```

- [ ] **Step 4: Name the class at the chain-debt pair offer**

Each clause is considered on its own: the audit arm reads an audit pair
together, while the round arm stays per-document, and the paragraph
says both. It is rewrapped whole, since this task changes it. Replace:

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

with:

```
For a judged document, the consumption gate before plan-writing makes
the pair offer as one question — an integrity audit or a full-document
round — and never an offer followed by a re-offer of the option just
declined. When the `integrity-auditor` agent is absent the offer
carries the full-document round alone. For an audit pair the gate makes
one pair offer for both documents: its audit arm reads the two
together, while choosing its round arm dispatches one full-document
architect round on each document, and plan-writing waits until both
verdicts are settled under the rules any verdict follows. The two arms
cost differently and the
offer says so: an audit returns material for the dispatcher to dispose
of and leaves the verdict alone, while a full-document round on a
judged document is a new loop's first round, since that document's
LGTM already closed its loop — it mints its own verdict and stamps it,
so a `concerns` there flips the field back while plan-writing waits.
The full-document-round arm therefore blocks plan-writing; the audit
arm does not, and plan-writing follows its dispositions.
```

- [ ] **Step 5: Name the technical design in three enumerations**

None is a branch, but each reads as a complete list, and the technical
design belongs in all three: the glossary binds it, it is prose under
`docs/`, and Task 4 gives it the branch fields. Replace:

```
terms and `_Avoid_` bans bind specs, plans, code identifiers, and
reviews.
```

with:

```
terms and `_Avoid_` bans bind design specs, technical designs, plans,
code identifiers, and reviews.
```

Replace:

```
available, prose artifacts under `docs/` — specs, plans, ADRs, the
glossary — get its pass: invoke it before drafting a new document, and
```

with:

```
available, prose artifacts under `docs/` — design specs, technical
designs, plans, ADRs, the glossary — get its pass: invoke it before
drafting a new document, and
```

Replace:

```
name and this convention does not govern it. The work's spec and plan
record the result in their `branch:` field — the topic branch, not the
```

with:

```
name and this convention does not govern it. The work's design spec,
technical design and plan record the result in their `branch:` field —
the topic branch, not the
```

- [ ] **Step 6: Verify the retired value and the old branches are gone**

Run:

```bash
F=plugins/working-process/rules/workflow.md
tr -s '[:space:]' ' ' < $F | grep -c 'names a judged document'   # expect 1
grep -c '`both`' $F    # expect 0
grep -cF '(`docs/specs/`, `docs/technical-designs/`, `docs/plans/`) so the' $F  # expect 1
grep -cF '(`docs/specs/`, `docs/plans/`) so the' $F   # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'For a judged document, the consumption gate'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'dispatches one full-document architect round on each document'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'its round arm stays per-document'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'For a spec, the consumption gate'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'round on a spec is a new loop'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'bind design specs, technical designs, plans'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'bind specs, plans, code identifiers'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'design specs, technical designs, plans, ADRs'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'specs, plans, ADRs, the glossary'  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c "The work's design spec, technical design and plan"  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c "The work's spec and plan"  # expect 0
```

The second check is the deletion assertion: `both` retires with the
value, and a surviving mention would send triage down a branch the
adversary can no longer emit.

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): hold a finding from either judged document"
```

---

### Task 13: The architect card takes the class name

**Files:**
- Modify: `plugins/working-process/agents/architect.md:3` and the
  stamping sentence at `:56`

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

- [ ] **Step 3: Name the class in the stamping sentence**

The card's stamping sentence enumerates two classes. Replace:

```
convention (a YAML block with a `status` field) — spec and plan alike. A
```

with:

```
convention (a YAML block with a `status` field) — judged document and
plan alike. A
```

- [ ] **Step 4: Verify**

Run:

```bash
F=plugins/working-process/agents/architect.md
grep -c 'design document' $F        # expect 0
grep -c 'any judged document' $F    # expect 1
grep -c 'a grilled design spec' $F  # expect 1
grep -c 'spec and plan alike' $F    # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'judged document and plan alike'  # expect 1
```

- [ ] **Step 5: Commit**

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
  lens), `:120-122` (the defect entry), `:133-137` (the coverage tell)

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

- [ ] **Step 6: Let a defect entry name its file on a joint target**

The coverage tell reports per document; a defect entry must too, or a
defect found in either document of an audit pair cannot say which one
carries it. Replace:

```
Then the defects, one entry each:
```

with:

```
Then the defects, one entry each — on a joint target the entry opens
with the file, `<file>:<section or line>`, so a defect found in either
document of an audit pair says which one carries it:
```

- [ ] **Step 7: Verify all three edits landed and the old text is gone**

Run:

```bash
F=plugins/working-process/agents/integrity-auditor.md
grep -c 'design document' $F                                  # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'Four cases fix what you read'        # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'never a target alone'                # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'the documents audited with it'       # expect 1
grep -c 'coverage: <file>' $F                                 # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'document of an audit pair says which one carries it'  # expect 1
grep -c 'coverage: <target line count>' $F                    # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'Your primary target is a spec,'      # expect 0
```

The last two are deletion assertions.

- [ ] **Step 8: Commit**

```bash
git add plugins/working-process/agents/integrity-auditor.md
git commit -m "feat(working-process): audit a design spec and its technical design as one target"
```

---

### Task 15: The plan adversary reads a list of origins

**Files:**
- Modify: `plugins/working-process/agents/plan-adversary.md:46`, `:49`,
  `:51-55`, `:102`, the generic dimensions list at `:57-70`, the
  section heading at `:44` and the description at `:3`

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

The section's heading and the card's description state the same
binary. Replace:

```
## Specs: decline
```

with:

```
## Judged documents: decline
```

and, in the `description:` field, replace:

```
Specs are out of scope — design review of a spec belongs to the architect agent.
```

with:

```
Judged documents — a design spec or a technical design — are out of scope; design review of one belongs to the architect agent.
```

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

After the lines:

```
  broke?* Name it — the plan should have pre-empted it. Record it as a
  finding.
```

which close dimension 4, add:

```
### 5. Coverage of the technical design's parts

Read the Parts table of every technical design the plan's design
specs name, reaching each through the plan's `technical-design:`
entries or, where an entry is missing, through the design spec's own
pointer. A missing or extra entry is itself an Important finding whose
`origin` is `implementation-plan`. The plan must cover every part
marked `new`,
`changed` or `retired`; one part may span several tasks and one task
several parts, and a part carried as `unchanged` context needs none. An
uncovered part is an Important finding whose `origin` is
`implementation-plan`. A `change` value outside
`new | changed | retired | unchanged` is an Important finding whose
`origin` is `technical-design`: the set is closed, and an unknown value
would otherwise slip past this dimension unchecked.

The `**Interfaces:**` blocks are read here too. Where a technical design
applies to the plan, those blocks reference the contracts that design
defines and say which part of one each task implements or changes; a
block that redefines a contract independently is an Important finding
whose `origin` is `implementation-plan`. Where no technical design is
named, the existing plan convention stands and this paragraph is silent.
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
grep -c '^## Judged documents: decline' $F              # expect 1
grep -c '^## Specs: decline' $F                         # expect 0
grep -c 'Specs are out of scope' $F                     # expect 0
tr -s '[:space:]' ' ' < $F | grep -c 'Coverage of the technical design'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'A missing or extra entry is itself an Important finding'  # expect 1
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
  (description), duty 5 at `:112-116`, and its duty list

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
and the rule's table numbers its rows against them. After the line:

```
it rather than assuming either way.
```

which closes duty 8, add:

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
checked there starts from the design specs: for every `spec:` target
that names a technical design, the plan's `technical-design:` must hold
an entry resolving, from the plan's own directory, to that same
document. A missing entry, an extra one, or one resolving elsewhere is
a hit — the check reads each design spec's pointer, so a missing field
is found rather than skipped. A plan whose `spec:` is not named back is
not.
```

The second paragraph is what keeps this duty from firing on every plan
in the repository: the reciprocity check belongs to the design spec and
its technical design alone.

- [ ] **Step 4: Give duty 5 the sources of each document class**

Duty 5 diffs a document's names against "the spec" and reports the rest
as spec gaps. A technical design mints part names by design, so read
literally the gate before every architect round on one would return a
hit per minted name. Replace:

```
Diff the names one document uses against the names its sources define. A
name the plan uses that the spec never defines is a spec gap, not a plan
error — the invention is the symptom, and report it as the gap it is.
```

with:

```
Diff the names one document uses against the names its sources define —
for a plan, the design spec and the technical design its `spec:` and
`technical-design:` name; for a technical design, its design spec and
the domain skills available to its author. A name a plan uses that no
source defines is a gap in the source, not a plan error — the invention
is the symptom, and report it as the gap it is. A technical design mints
part names by design: a name it introduces as its own, or records as a
vocabulary gap, is never a hit. A name it presents as coming from its
design spec or a domain skill is checked at that source like any other —
the exception covers what the design mints, never the names it borrows.
```

The last sentence is the boundary: without it the minting exception
would switch off name checking for a whole document class.

- [ ] **Step 5: Verify**

Run:

```bash
F=plugins/working-process/agents/propagation-auditor.md
grep -c 'a design spec, a technical design or a plan' $F   # expect 1
grep -c 'a spec or plan' $F                                # expect 0
grep -c '^### 9\. The pointer pair' $F                     # expect 1
grep -c '^### [0-9]' $F                                    # expect 9
tr -s '[:space:]' ' ' < $F | grep -c 'is not named back is not'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c "the check reads each design spec's pointer"  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'never the names it borrows'  # expect 1
tr -s '[:space:]' ' ' < $F | grep -c 'A name the plan uses that the spec never defines'  # expect 0
```

The count of `###` headings must equal the duty count the
propagation-duties rule now states, or the rule's last column points at
a duty that does not exist.

- [ ] **Step 6: Commit**

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
  `:184-192` (the Rules payload enumeration and its count), `:243-244`
  (the directories the plugin creates)
- Modify: `plugins/working-process/skills/grilling-session/SKILL.md:8-13`
  (its copy of the flow line and its scope sentence)

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

The row is replaced whole, since both its value and its meaning change
and a table row is one line. Replace:

```
| `integrity` | `<ISO date> (sha: <short-hash>)` | last integrity audit — the date for the reader, the body hash for the check; the dispatcher writes it once the audit's dispositions land, and a spec's consumption gate recomputes the hash to decide whether the stamp still holds |
```

with:

```
| `integrity` | `<ISO date> (sha: <short-hash>[; with: <file>@<short-hash>])` | last integrity audit — the date for the reader, the body hash for the check; the dispatcher writes it once the audit's dispositions land, and a judged document's consumption gate recomputes the hash of every document the stamp names to decide whether the stamp still holds; where a design spec names a technical design the two are audited as one target — an audit pair — and one stamp on the design spec records both |
```

- [ ] **Step 5: Retire the premises in three more paraphrases**

Each replacement covers whole lines and is rewrapped, so no line runs
past 72 columns and nothing is glued to the next line. Replace:

```
  plans (plans only; handed a spec it declines toward the `architect`
  agent). Generic failure-mode dimensions live here; domain specifics
```

with:

```
  plans (plans only; handed a judged document it declines toward the
  `architect` agent). Generic failure-mode dimensions live here; domain
  specifics
```

Replace:

```
- **`propagation-auditor` agent** — the mechanical audit of a spec or
  plan: it parses every changed interface to enumerate its consumers,
```

with:

```
- **`propagation-auditor` agent** — the mechanical audit of a design
  spec, a technical design or a plan: it parses every changed interface
  to enumerate its consumers,
```

Replace:

```
  document, read on a fresh context: the document against itself, then
  the document as an implementer who must build from that text alone.
```

with:

```
  document, read on a fresh context: the document against itself, then
  the document as an implementer who must build from that text and
  whatever was audited with it.
```

The first two leave a short line where the original paragraph resumes;
that is the cost of an anchor ending at a line's end, and it keeps every
line within 72 columns.

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

- [ ] **Step 7: Re-count the directories the plugin creates**

Task 11 has the plugin's own step write into `docs/technical-designs/`,
and Task 3 makes it a Process directory with the first-create question,
so the README's count goes stale. Replace:

```
This plugin creates two directories in a project repo: `docs/domain/`
(glossary + ADRs) and `docs/code-review/` (Review reports — one per
```

with:

```
This plugin creates three directories in a project repo:
`docs/domain/` (glossary + ADRs), `docs/technical-designs/` (technical
designs, written when a project accepts the offer) and
`docs/code-review/` (Review reports — one per
```

- [ ] **Step 8: Bring the grilling-session skill's copy of the flow along**

The skill carries its own copy of the flow line and a scope sentence;
after Step 2 the two copies would disagree, and neither says that a
technical design is not grilled. In
`plugins/working-process/skills/grilling-session/SKILL.md`, replace:

```
idea → brainstorming (spec) → **grilling-session on the spec** →
architect review (an `architect` agent dispatch) → writing-plans (plan) →
plan-adversary on the plan → implementation → code review. Offer a
grilling once a spec
exists and before its implementation plan is written. Specs are the
primary target; plans and raw ideas are in scope too.
```

with:

```
idea → brainstorming (design spec) → **grilling-session on the spec** →
architect review (an `architect` agent dispatch) → technical design
(when the repository has code) → writing-plans (plan) → plan-adversary
on the plan → implementation → code review. Offer a grilling once a
design spec exists and before its implementation plan is written.
Design specs are the primary target; plans and raw ideas are in scope
too. A technical design is not a grilling target: it mints no
terminology, its vocabulary coming from the design spec, which was
grilled, and from the domain's own skills; the part and component names
it does mint are checked against those skills.
```

- [ ] **Step 9: Verify, and sweep the plugin for the retired phrase**

Run:

```bash
grep -rcH 'design document' plugins/working-process/ | grep -v ':0$' | wc -l  # expect 0
grep -c 'seven rule files' plugins/working-process/README.md   # expect 1
grep -c 'six rule files' plugins/working-process/README.md     # expect 0
ls plugins/working-process/rules/*.md | wc -l                  # expect 7
grep -c 'creates three directories' plugins/working-process/README.md   # expect 1
grep -c 'creates two directories' plugins/working-process/README.md     # expect 0
grep -c 'recomputes the hash of every document the stamp names' plugins/working-process/README.md  # expect 1
grep -c "a spec's consumption gate recomputes the hash" plugins/working-process/README.md  # expect 0
tr -s '[:space:]' ' ' < plugins/working-process/skills/grilling-session/SKILL.md | grep -c 'A technical design is not a grilling target'  # expect 1
tr -s '[:space:]' ' ' < plugins/working-process/skills/grilling-session/SKILL.md | grep -c "and from the domain's own skills"  # expect 1
tr -s '[:space:]' ' ' < plugins/working-process/skills/grilling-session/SKILL.md | grep -c 'technical design (when the repository has code)'  # expect 1
tr -s '[:space:]' ' ' < plugins/working-process/skills/grilling-session/SKILL.md | grep -c 'agent dispatch) → writing-plans'  # expect 0
grep -rcH 'a spec or plan\|build from that text alone\|handed a spec' plugins/working-process/README.md | grep -v ':0$' | wc -l  # expect 0
```

Each expected value is on its line. The stated
count and the directory listing must agree — a README that counts its
own payload wrong is the failure this check exists for. The first and
last lines are the Global Constraint's closing sweep.

- [ ] **Step 10: Commit**

```bash
git add plugins/working-process/README.md plugins/working-process/skills/grilling-session/SKILL.md
git commit -m "docs(working-process): put the technical design in the README and grilling flow"
```

---

### Task 19: This repository's own declaration

Task 10 gives the declaration a readable surface, so this repository can
use it. Its product is prose, but `.claude-plugin/plugin.json`,
`.claude-plugin/marketplace.json` and the CI workflows are files a
platform reads to deploy it, so the marker test reaches it and without a
declaration the offer fires at every consumption gate. Writing the
declaration here also exercises the surface the plugin ships — the one
thing this repository can dogfood about a document class it will never
write.

**Files:**
- Modify: `CLAUDE.md` (repository root)

**Interfaces:**
- Consumes: the declaration surface from Task 10.
- Produces: nothing later tasks read. This is the plugin's contract used
  on its own repository, not part of the payload.

- [ ] **Step 1: Measure the before state**

Run:

```bash
grep -c 'technical design' CLAUDE.md   # expect 0
grep -n '^## ' CLAUDE.md
```

- [ ] **Step 2: Write the declaration**

After the line:

```
one per topic branch, git-ignored.
```

which closes the `## Worktrees and topic branches` section, add:

```markdown
## Technical designs

This repository does not get the technical-design offer by default. Its
product is prose: a part's name is its path and behaviour is already the
shape of the contract, so a technical design here would restate the
design spec and the plan. The declaration switches the default offer
off; it is not a ban. Ask for a technical design explicitly and the
step runs as it would anywhere else.
```

- [ ] **Step 3: Verify the declaration reads as a switch, not a ban**

Run:

```bash
grep -c 'does not get the technical-design offer by default' CLAUDE.md  # expect 1
grep -c 'it is not a ban' CLAUDE.md                                     # expect 1
```

Both matter. A declaration a later session reads as a prohibition would
refuse work the developer asked for, which is the failure the round-two
finding about conditionals was about, one level up.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: declare that this repository skips the technical-design offer"
```

---

### Task 20: Changelog and the dogfooding version

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

After the line:

```
Released versions of this plugin, newest first.
```

which is the changelog's preamble, add:

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
  `judged document` on the three agent cards that carried the old
  phrase and in the README; that phrase is retired.
- Run a rules re-sync after this update: the plan-adversary's `origin`
  values changed, and until the re-sync an installed workflow rule
  triages the new values by the old names.
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
tr -s '[:space:]' ' ' < plugins/working-process/CHANGELOG.md | grep -c 'triages the new values by the old names'  # expect 1
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
  `X.Y.Z-dev.<discriminator>` with no counter, while Task 20 mints
  `0.18.0-dev.1.technical-design-step`. The counter is the developer's
  decision of 2026-09-17 — `n` separates the successive dogfood releases
  of successive topics and increments on `develop`, which is the owner
  the counter lacked when an earlier attempt at it was declined. The
  rule's amendment is deliberately not part of this branch, so the
  divergence stands until that separate change lands. Task 20 follows
  the decision, not the current rule text.

- **A plan's `technical-design:` is mandatory, and a list.** The design
  spec says a plan keeps its own `spec:` and `technical-design:` and
  that, where it carries both, they must agree with the pair. The
  developer's rulings of 2026-09-24 and 2026-09-25 sharpen that: a plan
  carries a `technical-design:` entry for every design spec it names
  that has a technical design — an inline list when several, each path
  written relative to the plan — and a missing, extra or misresolving
  entry is a hit, found from the design specs' side (Tasks 6, 9, 11, 15
  and 16). Where this plan and the spec's sentence differ, the plan
  follows the rulings.

- **The technical-design rule words two component mentions
  conditionally where the design spec states them plainly.** The spec
  says the author takes vocabulary from "the Domain expertise duty the
  personas already carry" and that "the architect round judges the
  boundary". The spec describes a design; the rule Task 2 writes is a
  committed project-level rule that loads for people without the
  plugin, and the repository's plugin-authoring rule requires skill and
  agent mentions in such text to be conditional. The rule says "when the
  working-process plugin is installed" and "when that agent is
  available"; the design is unchanged.
- **The grilling-session skill is edited though the spec's Parts table
  names no row for it.** It carries a copy of the flow line the README
  carries, and once Task 18 changes one copy the two would disagree, so
  Task 18 changes both. The spec's own Lifecycle sentence — a technical
  design is not grilled — supplies the one sentence the skill gains.

## What this plan does not do

- It creates no `docs/technical-designs/` directory in this repository.
  The plugin ships the contract; this repo's product is prose and it
  declines the offer. The first project to accept the offer creates the
  directory, and the first-create question fires there.
- It does not settle where a project's standing process answers live.
  The spec defers that question; Task 10 names the shape available
  today — a `CLAUDE.md` note, or a file it points at — and Task 19 uses
  it for this repository. When the wider question is settled, the
  declaration moves with every other standing answer.
- **It does not validate the step on a code project.** The design
  spec calls its own justification a hypothesis, and its validation
  paragraph says what settles it: on one code project, cost — elapsed
  time, tokens by model tier, rounds per document, and the interruptions
  that needed a developer decision — against the structural decisions
  still discovered during implementation and the rework they caused,
  read against a comparison arm named before measuring starts. This
  repository cannot run that, since it declines the offer. The
  validation is a separate, open step the developer owns. Completing
  this plan's tasks shows the contract landed; it claims nothing about
  whether the step earns its cost.
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
- fixed 2026-09-21 — [Minor] the changelog task wrote the retired phrase
  one task after Task 18's plugin-wide sweep expects zero, so the sweep
  passed on its run and failed on a re-run, breaking the plan's own
  Global Constraint; license: that constraint; the changelog bullet
  names the new term and describes the old one without spelling it.
- fixed 2026-09-24 — [Important] the discharge widening covered the
  audit arm only, so with one joint offer for two documents a decline
  left undefined whether the technical design's chain debt was
  discharged and which headings were annotated; ruling: 2026-09-24,
  variant (a); a declined offer over an audit pair discharges the chain
  debt of both documents the offer named, the offer names them so a
  reader can see what the decline settles, and the same clause bounds
  it — a decline writes no `integrity:` stamp, leaves every other open
  finding open and closes no `blocking` verdict, so "do not run the
  audit" never reads as a wider release.
- fixed 2026-09-24 — [Minor] after Task 10 named `CLAUDE.md` as the
  readable declaration surface, the plan's "writes no declaration
  surface" bullet described a cost the plan itself had just made
  avoidable, and the spec's "this repository declines by declaration"
  had no deliverer; ruling: 2026-09-24, variant (a); new Task 19 writes
  this repository's declaration and the changelog task moves to 20. The
  declaration switches the default offer off rather than banning the
  document — a session asked for a technical design here still writes
  one — and its verify step asserts both halves, since a declaration a
  later session read as a prohibition would refuse work the developer
  asked for.
- fixed 2026-09-24 — [Minor] "the pair" named both the two documents and
  the two-armed chain-debt question, two sentences apart in one block;
  ruling: 2026-09-24, variant (a); the glossary mints **Audit pair** for
  the document sense, prose writes the full name wherever both senses
  stand close, and the term's own entry says so. The glossary and the
  design spec's Parts row changed for this, so the line lands in the
  design spec's ledger too, under
  `### 2026-09-24 — fix from docs/plans/2026-09-17-technical-design-step.md`,
  which leaves that spec's `integrity:` stamp stale by design.
- signal 2026-09-21 — the reviewer judges a third round worth its cost
  only as the confirming full-document round the plan already owes, not
  as another diff-scoped pass. It reads both Important findings as one
  class again — a fix pinned to the wrong noun, an extension stopped
  halfway down a list — and expects the confirming round to close on
  `concerns` or `LGTM`, with no material for a fourth absent new
  evidence.

### 2026-09-24 — plan-adversary, fable 5.1, blocking (round 3, full-document)

The confirming round the plan owed. Five Important, eleven Minor.
Record:
`.claude/working-process/2026-09-17-technical-design-step/plan-adversary-round-3.md`.
The reviewer went past reading and simulated execution: it applied every
replacement of Tasks 2–19 in numbering order to copies of the files and
ran each published after-check. That found a class no before-state
measurement could see — a task whose anchor an earlier task destroys,
and checks that fail on the plan's own replacement text. Fifteen of
sixteen citations held against the files; the sixteenth is the grep
finding below, and it held too, in a different environment.

- fixed 2026-09-24 — [Important] Task 8 anchored its insertion on a
  sentence Task 5 Step 4 rewrites, and Task 5's own verify step asserts
  that sentence is gone, so in numbering order the anchor no longer
  existed when Task 8 ran; license: Task 5's deletion assertion, which
  fixes what text survives; Task 8 anchors on Task 5's wording and its
  Interfaces block states that Task 5 lands first.
- fixed 2026-09-24 — [Important] Task 2's check for the closed `change`
  set grepped a spelling the prescribed rule text never used; license:
  the design spec's spelling, `new | changed | retired | unchanged`,
  which the adversary's dimension 5 also quotes; the rule text takes
  that spelling, so rule, spec, card and check agree.
- fixed 2026-09-24 — [Important] Task 9 checked `walks the same nine`
  with a plain grep while its replacement wraps between "same" and
  "nine"; license: the plan's own Global Constraint that prose checks
  normalize whitespace first; the check runs through `tr`.
- fixed 2026-09-24 — [Important] Task 10 still checked the pre-round-2
  wording beside the check that replaced it, so it could not pass, and
  an implementer satisfying it would have deleted the conditional round
  two fixed as Important; license: the deletion the round-two fix
  implied and never made; the stale check is deleted. Third time in this
  work a superseded assertion survived its replacement.
- fixed 2026-09-24 — [Important] nothing wrote `technical-design:` onto
  a plan and neither duty 9 nor dimension 5 read its absence, so a plan
  written from an audit pair that omitted the pointer escaped the
  coverage check; ruling: 2026-09-24; a plan written from a design spec
  that names a technical design carries that pointer, the plan-writing
  step writes it, and both checks start from the design spec's pointer
  — so an omitted field is found rather than skipped. A plan from a
  design spec with no technical design carries none.
- fixed 2026-09-24 — [Minor] the `never the work` check was vacuous, the
  phrase already standing in the file, and every `tr | grep -c` check
  proves existence rather than occurrence; license: the check's own
  purpose; it counts a phrase unique to the block with `grep -o … | wc
  -l`, and a Global Constraint now says when to count that way.
- fixed 2026-09-24 — [Minor] an 86-character line in Task 7's block, and
  two anchors ending mid-line that would glue the original line's tail
  onto the block's last line; license: the plan's 72-column constraint;
  the line is rewrapped, both anchors run to their line's end, and a
  Global Constraint states the rule. Task 12's tail also carried a
  binary — the stamp going stale is the design spec's for either
  document of an audit pair — and says so now.
- fixed 2026-09-24 — [Minor] Task 12 measured its before-state by line
  number, and Tasks 10 and 11 insert some forty lines above it;
  license: the measurement's purpose; it greps the clause's content,
  with `-e` since the clause opens with a dash.
- fixed 2026-09-24 — [Minor] the reviewer found that `grep -rc` on a
  single named file prints a bare count, so the sweep's `grep -v ':0$'`
  filter would not suppress it; ruling: 2026-09-24; both results are
  true — GNU grep 3.11 prints a bare `0`, while this machine's `grep` is
  a shell function resolving to ugrep 7.8.4, which prints the prefix.
  The dispatcher's first reading, that the finding was refuted, was
  wrong: it measured a different implementation. The sweeps take `-H`,
  and a Global Constraint requires every check to name the behaviour it
  needs and to run where `grep` is not wrapped.
- fixed 2026-09-24 — [Minor] three spec/plan binaries in `workflow.md`
  stayed untouched — the pair-offer sentence, the Process directories
  resolved before a verdict dispatch, and the chain-debt pair offer;
  ruling: 2026-09-24; each is widened on its own terms, Task 10 taking
  the first and Task 12 the other two, with deletion assertions. The
  audit-pair exception is kept: the audit arm reads the pair together,
  while the round arm stays per-document.
- fixed 2026-09-24 — [Minor] the README's "creates two directories" went
  stale once the plugin's own step writes into `docs/technical-designs/`;
  license: the count's own derivation; Task 18 gains a step and a check
  for "three".
- fixed 2026-09-24 — [Minor] the changelog said the class is named on
  every agent card, where three of six take it; license: the count;
  the bullet names the three cards.
- fixed 2026-09-24 — [Minor] the rule defined a vocabulary gap as a kind
  of part only, narrower than the glossary term it mints; ruling:
  2026-09-24; the rule and the design spec both take the glossary's
  breadth — kinds of part, contract, and home of state. The spec change
  is recorded in that spec's ledger under
  `### 2026-09-24 — fix from docs/plans/2026-09-17-technical-design-step.md`.
- fixed 2026-09-24 — [Minor] the widened `spec:` comment admitted an
  inline list on a technical design, which may name one design spec;
  license: the plan's own "one technical design per design spec"; the
  list clause is scoped to plans.
- fixed 2026-09-24 — [Minor] the one-offer sentence dropped the spec's
  clause that the round arm stays per-document; license: the design
  spec's own sentence; Task 10's block carries it.
- fixed 2026-09-24 — [Minor] "one offer for that pair" used the bare
  word in the document sense three sentences from "the pair form" in the
  question sense; license: the Audit pair entry's `_Avoid_`; the block
  writes "audit pair" and its check follows.
After the wave, the dispatcher ran the sequential simulation the round
had shown was missing: every edit of Tasks 2–20 applied in numbering
order to copies of the files, each task's after-checks run in a clean
shell under GNU grep, and every edit-bearing step the parser could not
resolve reported rather than skipped. Its first run skipped one step
silently anyway — a filter meant for verify steps matched "validate"
inside "invalidates" — which was caught and fixed before any result was
trusted. The final run: 91 of 91 after-checks pass, no step
unsimulated, both sweeps silent, the plugin validates, and 64 of 65
non-zero checks fail on the pre-plan files, the sixty-fifth being a
deliberate invariant. The simulation also found these:

- hit fixed 2026-09-24 — three anchors named a position rather than
  text: "After the field notes", "after the five rules", and "After the
  offer paragraph", the last pointing at a block another task inserts;
  each now quotes the exact line it follows.
- hit fixed 2026-09-24 — Task 18 Step 5 nested backticks inside inline
  code, which Markdown cannot render and which left "handed a spec"
  standing after the task ran; its three edits are block replaces over
  whole lines.
- hit fixed 2026-09-24 — this wave's own edits left lines past 72
  columns in Task 2's rule text and Task 15's new dimension; each
  paragraph is rewrapped whole.
The propagation gate before round four found one more, and the
developer's question about which `CLAUDE.md` files load found another:

- hit fixed 2026-09-24 — the Goal counted five changed agent cards where
  the tasks change four — the architect, integrity-auditor,
  plan-adversary and propagation-auditor cards; Task 9 edits a rule; the
  Goal says four.
- hit fixed 2026-09-24 — Task 10 had a session read the declaration
  from a `CLAUDE.md` "at the repository root", narrower than the design
  spec, which names a `CLAUDE.md` note without a location. Measured the
  same day: Claude Code loads `.claude/CLAUDE.md` at session start as
  well, alone or beside a root `CLAUDE.md`, so a project keeping its
  instructions there would have a declaration the rule's literal
  wording never names. The sentence names both files, and its check
  asserts the root-only wording is gone.
- signal 2026-09-24 — the reviewer judges a further round worth its cost
  only after this wave and only as a full-document round, since a plan's
  loop cannot close on a diff-scoped one. It reads the five Important
  findings as three classes — checks never run on their own replacement
  text, an anchor an earlier task destroys, and one contract gap — and
  expects the next full-document round to close on `LGTM` or
  `concerns`.

### 2026-09-24 — plan-adversary, fable 5.1, blocking (round 4, full-document)

Full-document read. Two Important, five Minor. Record:
`.claude/working-process/2026-09-17-technical-design-step/plan-adversary-round-4.md`.
Every citation held against the files it names; the one platform fact —
that a path-scoped rule loads when a matching file is read — the
reviewer checked against Claude Code's documentation rather than recall.

- fixed 2026-09-25 — [Important] the propagation auditor's duty 5 read
  every name against "the spec" and reported the rest as spec gaps,
  while a technical design mints part names by design, so the gate
  before each architect round on one would have returned a hit per
  minted name; ruling: 2026-09-25; Task 16 gains a step giving duty 5
  each class's sources — for a plan, both documents its pointers name;
  for a technical design, its design spec and the domain skills — with
  minted part names and recorded vocabulary gaps exempt. The developer
  set the boundary: names a design presents as coming from its design
  spec or a domain skill are still checked at that source, so the
  exemption never switches name checking off for the class.
- fixed 2026-09-25 — [Important] the authoring step relied on "the
  technical-design rule that loads there", while a path-scoped rule
  loads only when a matching file is read and none exists at the moment
  of writing; license: the design spec's own sentence that the session
  reads the path-scoped rule once the offer is accepted and it sits down
  to write; Task 11 has the session read the rule before drafting.
- fixed 2026-09-25 — [Minor] the always-on audit sentence and the
  README's `integrity` row still described one hash and one document
  after Task 7 made the gate recompute both hashes of an audit pair;
  license: Task 7's own statement; Task 10 gains a step widening the
  sentence — which also read "the whole spec" where an audit pair has
  two documents — and Task 18 replaces the row whole, each with a
  deletion assertion.
- fixed 2026-09-25 — [Minor] the plan-adversary card's heading and
  description kept "Specs" over a paragraph that now declines judged
  documents; license: ADR 0004, where a branch names its class rather
  than a filename; Task 15 renames both, with deletion assertions.
- fixed 2026-09-25 — [Minor] the duty table's new row demanded
  reciprocity of every pointer, without the plan carve-out the card
  states; license: the card's own clause under the 2026-09-24 ruling;
  the row scopes reciprocity to a design spec or a technical design.
- fixed 2026-09-25 — [Minor] `<file>` in `with:` was defined as a
  path relative to the design spec while the spec's example carried a
  bare filename; ruling: 2026-09-25; `<file>` is exactly the value of
  the design spec's `technical-design:` pointer, read relative to the
  design spec's directory, so the gate can check the recorded value
  against the pointer. The spec's example is corrected in that spec's
  ledger under
  `### 2026-09-24 — fix from docs/plans/2026-09-17-technical-design-step.md`.
- fixed 2026-09-25 — [Minor] the 2026-09-24 ruling that makes a plan's
  `technical-design:` pointer mandatory sharpens the design spec's
  conditional, yet nothing recorded it while the Global Constraints say
  the spec wins where the two disagree; license: those constraints,
  which name the Deviations section as the one place a departure is
  recorded; a Deviations bullet cites the ruling.
The simulation, rebuilt in a fresh session from its memory entry, ran
after the wave: 106 of 106 after-checks pass, no step unsimulated, 71 of
72 non-zero checks fail on the pre-plan files (the seventy-second the
deliberate invariant), no new line past 72 columns, both sweeps silent,
the plugin validates. The rebuild first lost one anchor shape the old
parser knew, reported the step as unsimulated rather than passing it,
and was fixed before the result was read. A simulation proves the edits
land and their checks pass; it does not find a consumer no task names,
which is what this round's two Important findings were.

- signal 2026-09-24 — the reviewer judges another round worth its cost
  only after this wave and only as a full-document round, and expects it
  to close on `LGTM` or `concerns`. It reads both Important findings as
  a class earlier rounds met too: a consumer no task enumerated, and a
  delivery mechanism assumed rather than read.

### 2026-09-25 — plan-adversary, fable 5.1, concerns (round 5, full-document)

Full-document read, briefed to enumerate the consumers of every contract
the plan changes across the whole repository before reporting findings.
The enumeration covers ten contracts over all four plugins, personas,
skills, scripts and CI, each consumer mapped to a task or shown
unaffected; it is in the record. One Important, six Minor. Record:
`.claude/working-process/2026-09-17-technical-design-step/plan-adversary-round-5.md`.
Every citation held.

- fixed 2026-09-25 — [Important] the new rule's text named plugin
  components unconditionally — the personas' Domain expertise duty and
  the architect round — in a committed project-level rule that loads for
  people without the plugin, the class round one fixed in Tasks 10 and
  11 and left in Task 2; license: the repository's plugin-authoring
  rule; both mentions are conditional, Task 2's checks assert it, and a
  Deviations bullet records why the rule words them differently from the
  spec's prose.
- fixed 2026-09-25 — [Minor] the grilling-session skill carries its own
  copy of the flow line and a scope sentence, which would disagree with
  the README once Task 18 changed its copy; license: the design spec's
  Lifecycle sentence that a technical design is not grilled; Task 18
  gains a step for the skill, and a Deviations bullet records that the
  spec's Parts table names no row for it.
- fixed 2026-09-25 — [Minor] the propagation-duties rule's own sentence
  about where it loads stayed "specs and plans" after Task 9 widens its
  `paths:`; license: that widening; Task 9 gains a step and a deletion
  assertion.
- fixed 2026-09-25 — [Minor] six enumerations read as complete lists of
  spec and plan though the technical design belongs in each — the
  glossary's binding, the style pass, the branch field, two authoring
  enumerations, and ticket inheritance; license: ADR 0004's class and
  the fields Task 4 gives the technical design; Tasks 4, 8 and 12 each
  gain a step, every site with a deletion assertion.
- fixed 2026-09-25 — [Minor] on an audit pair a defect entry named no
  file, so a defect in either document could not say which; license: the
  design spec's "it may report defects in either", and the coverage tell
  already reporting per document; Task 14 gains a step.
- fixed 2026-09-25 — [Minor] four insertion instructions still named a
  position, and one, read literally, would put the declaration inside
  the section it was meant to follow; license: the propagation duty that
  an anchor is byte-exact; all five insertions of that shape — the four
  named and the changelog's — now quote the lines they follow in a
  fenced block. The reviewer's own suggested anchor for the offers
  paragraph, `full-document round.`, occurs three times in that file,
  so the block quotes two lines instead. Corrected at round six: six
  insertions changed shape, not five — Task 8 Step 2's inline anchor was
  reshaped too, for uniformity rather than because it named a position.
- fixed 2026-09-25 — [Minor] Task 11 left the implementer to choose
  whether to run Task 13 first; license: the plan's own anchors, which
  show no shared text between the two tasks; the Interfaces block says
  numbering order is safe and why.

The simulation ran after the wave: 127 of 127 after-checks pass, no step
unsimulated, 83 of 84 non-zero checks fail on the pre-plan files (the
last the deliberate invariant), no new line past 72 columns once one
glued tail was rewrapped, both sweeps silent, the plugin validates. The
finding about positional anchors exposed a fault in the simulator as
well: it had carried special cases that encoded what those instructions
meant rather than what they said, so it passed text an implementer
reading literally would have misapplied. Those cases are removed; the
simulator now accepts one explicit shape, "After the lines:" with the
anchor quoted in a block, and applies it byte-exactly.

Corrected at round six, and the correction matters more than the
figure it corrects. "127 of 127 after-checks pass" counted only the
checks annotated `# expect`. Seven verify commands stated their
expectation in prose, and the simulator never compared them; one of the
seven, Task 2's closed-set check, returned 0 against an expected 1. The
paragraph claimed coverage the tool did not have — the failure recorded
four times against the propagation gate. The shape it accepts is also
spelled two ways, "After the line:" and "After the lines:", and both
were simulated.

- signal 2026-09-25 — the reviewer judges another round worth its cost
  only as a diff-scoped pass over this wave, followed by the confirming
  full-document round, which it expects to close on `LGTM`; the consumer
  surface has now been walked plugin-wide, and a further full read for
  its own sake would find no more than this round did.

### 2026-09-25 — plan-adversary, fable 5.1, blocking (round 6, diff-scoped)

Diff-scoped over round five's fix wave. Two Important, four Minor.
Record:
`.claude/working-process/2026-09-17-technical-design-step/plan-adversary-round-6.md`.
Every citation held. The reviewer ran Task 2's checks itself and found
one that the dispatcher's simulation had reported as passing without
ever running it.

- fixed 2026-09-25 — [Important] Task 18's new step edited the
  grilling-session skill while its commit staged only the README, so
  the skill edit would have shipped in no commit; license: the step's
  own edit; the commit stages both files under a widened subject.
- fixed 2026-09-25 — [Important] Task 2's closed-set check was a plain
  grep over a phrase the rule text wraps, so it returns 0 against an
  expected 1, while the round-five paragraph said every after-check
  passed; license: the plan's Global Constraint that prose checks
  normalize whitespace; the check runs through `tr`, every one of the
  seven verify commands that stated its expectation in prose now carries
  `# expect`, a Global Constraint requires it of every check, and the
  round-five paragraph carries a correction naming what the simulator
  had not compared.
- fixed 2026-09-25 — [Minor] the grilling-session skill's new sentence
  named the design spec as a technical design's only vocabulary source,
  dropping the domain's own skills and the part names it does mint;
  license: the design spec's Lifecycle section and Task 5's block, which
  carry both; the sentence carries both, with a check.
- fixed 2026-09-25 — [Minor] the "After the lines:" shape never said
  whether a blank line separates an inserted block, and no check could
  catch a glued insert; license: the plan's own purpose for the shape,
  a block that lands where it is meant to; a Global Constraint states
  the convention, and the simulator applies the same one.
- fixed 2026-09-25 — [Minor] the round-five ledger counted five
  insertions reshaped where six were; license: the commit that changed
  them; a dated correction on that line.
- fixed 2026-09-25 — [Minor] the round-five paragraph named one
  spelling of the insertion shape where the plan uses two; license: the
  plan's text; a dated correction on that paragraph, and the Global
  Constraint names both spellings as one instruction.

The simulation ran after the wave, now reporting what it did not check
as well as what passed: 133 of 133 annotated checks pass, no verify
command left uncompared, no step unsimulated, 86 of 87 non-zero checks
fail on the pre-plan files (the last the deliberate invariant), no new
line past 72 columns, both sweeps silent, the plugin validates.

The propagation gate before the confirming round returned five located
hits, all dismissed:

- hit dismissed 2026-09-25 — `design document` still stands in
  `agents/architect.md`, `agents/integrity-auditor.md`,
  `agents/plan-adversary.md` (twice) and `README.md`, against checks
  that expect zero; counter: those checks assert the state after the
  plan runs, and the plan has not run. The five occurrences in four
  files are the before-state the Global Constraint names in those
  words, and the simulated tree after all twenty tasks carries zero.
- hit dismissed 2026-09-25 — the simulation "did not faithfully apply
  the prescribed text replacements to disk"; counter: it applies them to
  copies of the files by design, so that simulating a plan never
  executes it, and the copies carry every replacement.
- signal 2026-09-25 — the reviewer judges a further diff-scoped round
  not worth its cost over two one-line repairs and four count and
  wording items; the next reading worth paying for is the confirming
  full-document round, expected to close on `LGTM` if the simulation is
  re-run rather than restated. `blocking` leaves that round to the
  developer.

### 2026-09-25 — plan-adversary, fable 5.1, concerns (round 7, full-document)

The confirming full-document round. No Important, six Minor. Record:
`.claude/working-process/2026-09-17-technical-design-step/plan-adversary-round-7.md`.
An independent review of the same plan version by Codex (GPT-6),
written to
`.claude/working-process/2026-09-17-technical-design-step/codex-plan-review-2026-09-25-06-45-13.md`,
returned `blocking` on two Important findings and one Minor; its lines
below carry its own grades. The two reviewers overlapped on one finding;
Codex alone found the only correctness defect of the round, and its
reproduction was re-run and held. The stamped verdict is the loop
reviewer's. The developer ruled that one more full-document round
follows this wave, since it changes the plan's contract — the plan
pointer's cardinality, coverage completeness and the gate's behaviour —
and an annotation settles findings without assessing a changed contract.

- fixed 2026-09-25 — [Minor] the architect card's stamping sentence
  still read "spec and plan alike"; license: ADR 0004's class; Task 13
  gains a step, with a deletion assertion.
- fixed 2026-09-25 — [Minor] four insertions used an inline-anchor shape
  the insertion constraint did not define; license: that constraint's
  purpose; all eight insertions of any other shape now quote their
  anchor in a fenced block, the constraint covers every one, and the
  simulator's handlers for every other shape were removed with no step
  left unsimulated.
- fixed 2026-09-25 — [Minor] on an audit pair the round arm read two
  ways; ruling: 2026-09-25; choosing it dispatches one full-document
  architect round on each document, and plan-writing waits until both
  verdicts are settled under the rules any verdict follows (Tasks 10
  and 12).
- fixed 2026-09-25 — [Minor] the `technical-design:` example comment
  described the field in design-spec terms on a plan; license: the
  pointer semantics in Task 6's own note; the comment names each host.
- fixed 2026-09-25 — [Minor] Fable, and [Important] Codex: a plan may
  name several design specs while every sentence about its
  `technical-design:` assumed one; ruling: 2026-09-25; a plan's
  `technical-design:` is an inline list holding the design of every
  design spec it names that has one, and duty 9 checks completeness as
  well as correctness — none missing, none extra — with a worked example
  of two specs where one has no design (Tasks 6, 9, 11, 15 and 16, and
  the Deviations bullet).
- fixed 2026-09-25 — [Minor] a plugin update opens a window in which the
  new `origin` values meet an un-synced workflow rule; license: the
  README's standing re-sync sentence; the changelog names the re-sync.
- fixed 2026-09-25 — [Important] Codex: the authoring step copied the
  design spec's relative pointer into the plan, which names a different
  file wherever the two sit at different depths — reproduced with a
  nested spec, where the copy resolves outside `docs/`; license: duty 9's
  requirement that the entry name that same document, and every pointer
  in this process resolving from its own file; each entry is rewritten
  relative to the plan's directory, and duty 9 compares resolved
  targets.
- fixed 2026-09-25 — [Minor] Codex: the code-project validation the
  spec promises had neither a task nor an owner, so finishing the tasks
  could be mistaken for evidence that the workflow works on a code
  project; ruling: 2026-09-25; the developer owns the validation and
  tracks it outside this repository, and a not-done bullet records it
  as open, restates the spec's acceptance criteria, and says completing
  the tasks claims nothing about it. The plan does not say where it is
  tracked, since that store is per-user and a committed document must
  not point at it.

The simulation ran after the wave with every insertion handler but the
fenced shape removed: 142 of 142 annotated checks pass, no verify
command left uncompared, no step unsimulated, 91 of 92 non-zero checks
fail on the pre-plan files (the last the deliberate invariant), every
commit stages what its task edits, no new line past 72 columns, both
sweeps silent, the plugin validates.

- signal 2026-09-25 — the loop reviewer judged another round not worth
  its cost and a resolution annotation sufficient after the wave; the
  developer ruled otherwise for the reason recorded above.
