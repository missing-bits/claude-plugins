---
ticket: none
date: 2026-09-15
status: draft
adversary: concerns
spec: ../specs/2026-09-14-review-loop-errata-wave-five.md
branch: feature/process-wave-five
base: develop
---

# Review loop — errata wave five Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land the four changes of
`docs/specs/2026-09-14-review-loop-errata-wave-five.md` — the relay
header, the consultation relay and its floor's new site, the adversary's
`origin` field, and the dispatch record — across the `working-process`
plugin and this repo's glossary.

**Architecture:** Every deliverable is prose in a shipped rule, agent
card or glossary entry. There is no code and no test suite; a task's
test is the grep pair it publishes, run before and after the edit. Tasks
are drawn one per site, so no two touch the same text — `workflow.md`
takes three tasks because the wave edits three sections of it that share
no line.

**Tech Stack:** Markdown rule and agent files distributed as a Claude
Code Rules payload; `grep`, `tr` and `claude plugin validate` for
verification.

## Global Constraints

- **The spec is the source.** Where this plan and the spec disagree, the
  spec wins and the plan is wrong — except where *Deviations from the
  spec* below records a departure and its reason.
- **Prose wraps at 72 characters** in every rule, agent card and
  glossary file. Match the surrounding paragraph; never reflow a
  paragraph this plan does not change.
- **A check over prose normalizes whitespace first**
  (`tr -s '[:space:]' ' '`), so a phrase matches wherever a line wraps.
  Only a check anchoring something that cannot wrap — a path, a filename
  shape, a heading — is written plain.
- **Every step states its before value and its after value**, and an
  invariant says so and says why. The before values in this plan were
  measured against the files on 2026-09-15, not predicted.
- **`workflow.md` carries the literal `.claude/working-process/`
  exactly three times** when the wave is done — once where the store is
  named, once in each of the two filename shapes. The spec's own check
  expects three, so no other task may add a fourth.
- **The glossary binds.** `docs/domain/glossary.md` terms and `_Avoid_`
  bans govern this text. `Origin`, `Relay`, `Contribution`,
  `Consultation`, `Review report`, `Private memory` and `Process
  directory` are canonical here; `report file` is banned by **Review
  report**'s `_Avoid_` list and appears nowhere in a replacement block.
- **Public repo hygiene**: no machine-specific paths, no company or
  client names, all committed text in English.
- **The replacement texts already carry the elements-of-style pass.**
  It was applied to every Replace block at authoring, so an implementer
  copying a block verbatim is complying rather than skipping it. A block
  an implementer rewords leaves that guarantee and owes the pass again.
- **Commit messages are one line** — a conventional-commit subject, no
  body, no trailers.
- **Do not run `sync-rules`, do not bump the plugin version, and do not
  move the spec's `status`.** All three are the developer's, and the
  spec puts the first outside the wave.

## Deviations from the spec

Recorded here and beside the text they concern, so a reviewer trips over
the reason where the disagreement lives.

1. **Task 7 amends the glossary's Relay and Contribution entries, which
   the spec's W4 does not name.** Both state the floor
   this wave moves: **Relay** says a consultation's Contribution reaches
   the developer "attributed and substantially verbatim", and
   **Contribution** repeats it. The glossary binds specs, plans and
   reviews, so leaving them would ship a glossary contradicting the rule
   the same wave writes — the propagation duty an added field owes both
   ends of its chain. Task 7 carries the reason.
2. **Task 4 amends the two `*-consult` cards**, which the spec's W2 does
   not name either. Each tells its persona "the contract has it relayed
   attributed and substantially verbatim", which stops being true of the
   relay once the floor moves to the file. The sentence's purpose —
   write for the developer, not as a report to the dispatcher —
   survives the correction and is why the sentence stays rather than
   going.
3. **W3's glossary site is already in the file.** The **Origin** entry
   was minted at the grilling, so this plan verifies it as an invariant
   instead of writing it. Measured at authoring: one entry present.
4. **The consultation paragraph points at the filename shapes rather
   than repeating them.** The spec's check expects exactly three
   occurrences of `.claude/working-process/` in `workflow.md`, and
   Task 1 writes all three; Task 2 names "the timestamp shape of the two
   the verdict-agent dispatch subsection defines" instead.
5. **Task 6 says the resolution annotation is defined for `concerns`
   and `blocking` alone, where the spec says `concerns` alone.** The
   shipped rule is what the plan follows: the resolution-annotation
   bullet of `spec-plan-lifecycle.md` gives a `blocking` verdict the
   developer closes by explicit adjudication the same form, with the
   round's ledger record as its body note. So a `blocking` document
   has somewhere for the line to land and does not need the fix
   heading, which is what the sentence claims. Task 6 carries the
   reason.

## File structure

Modified:

- `plugins/working-process/rules/workflow.md` — Task 1 (the
  completion-notification bullet and the relay bullet, inside
  *Dispatching a verdict agent*), Task 2 (the consultation paragraph,
  above *Branch naming*) and Task 3 (one bullet in the triage list of
  *The review loop*). The three tasks share the file and touch no common
  line.
- `plugins/working-process/PERSONA_COMMON.md` — Task 4: the first bullet
  of *The reply* in the consultation contract.
- `plugins/working-process/agents/architect-consult.md` and
  `plugins/working-process/agents/system-designer-consult.md` — Task 4:
  one *Hard limits* bullet each.
- `plugins/working-process/agents/plan-adversary.md` — Task 5: the
  `Output` schema and the close of *Specs: decline*.
- `plugins/working-process/rules/spec-plan-lifecycle.md` — Task 6: one
  passage after the one-authorizer invariant in *The disposition
  ledger*.
- `docs/domain/glossary.md` — Task 7: **Relay** and **Contribution**
  amended, **Dispatch record** minted between them.

Created: nothing.

Not modified, and why: `plugins/working-process/README.md` describes the
relay-then-stamp sequence and names the files that hold the consultation
contract, and this wave changes neither — no count, list or file name in
it moves. The two `*-auditor` cards are out of scope by the spec's own
*Out of scope* section: audits write no dispatch record.

## Order and independence

- Tasks 1, 2 and 3 all edit `workflow.md`. Task 1 runs first because
  Task 2's text points at the filename shapes Task 1 writes; Task 3 is
  independent of both. Every check anchors text rather than a line
  number, so the order is a convenience except for that one pointer.
- Task 3's bullet cites "the cross-document clause the
  spec-plan-lifecycle rule defines", which Task 6 writes. The citation
  names a rule and a clause rather than an anchor or a line, so it does
  not break if Task 6 runs later — but a reviewer reading Task 3 alone
  should know Task 6 is what makes it true.
- Task 5 is the only task touching an agent card that carries a schema;
  nothing else reads that schema, and the triage sentence Task 3 writes
  consumes the field by name rather than by position.
- `claude plugin validate` runs once, at Task 8, after every file has
  changed. Validation before then proves nothing about the end state,
  and it never reads `rules/` at all — see Task 8.

---

### Task 1: `workflow.md` — the relay header and the dispatch record

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the
  completion-notification bullet and the relay bullet of
  `## Dispatching a verdict agent`.

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: the two filename shapes and the store path that Task 2's
  consultation paragraph and Task 7's glossary entry both point at, and
  the three occurrences of `.claude/working-process/` the Global
  Constraints cap.

- [ ] **Step 1: Record the before values**

```bash
W=plugins/working-process/rules/workflow.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $W | grep -o 'The relay opens with one header line' | wc -l)"
echo "B $(n $W | grep -o 'finding list is never condensed' | wc -l)"
echo "C $(n $W | grep -o 'output style' | wc -l)"
echo "D $(grep -o '\.claude/working-process/' $W | wc -l)"
echo "E $(grep -o '\.working-process/' $W | wc -l)"
echo "F $(grep -c '<agent>-round-<N>\.md' $W)"
echo "G $(grep -c '<agent>-<date>-<HH-MM-SS>\.md' $W)"
echo "H $(n $W | grep -o 'git-ignored by a .\.gitignore. containing exactly' | wc -l)"
echo "I $(n $W | grep -o 'write the dispatch record defined below' | wc -l)"
echo "J $(n $W | grep -o 'Before writing a record the dispatcher ensures' | wc -l)"
```

Expected: `A 0`, `B 0`, `C 0`, `D 0`, `E 0`, `F 0`, `G 0`, `H 0`, `I 0`,
`J 0`.

`D` counts the store path; `E` counts a store path written without the
`.claude/` prefix, which the spec forbids. The two are not the same
count: `\.working-process/` needs a dot immediately before
`working-process`, and inside `.claude/working-process/` a slash sits
there, so `E` reads 0 over text `D` reads 3 over. `E` is therefore an
invariant at zero — it is the spec's own check that no bare store path
appears, and it must read 0 before and after.

- [ ] **Step 2: Put the record into the completion sequence**

Find:

```
- On the completion notification, in one turn and in this order:
  verify the agent's model self-report (the comparison the lifecycle
  rule defines), relay the report to the developer, check every
  citation the report supplies against what it names, then stamp the
  verdict (`LGTM` | `concerns` | `blocking`) into the reviewed
  document's `architect:` / `adversary:` frontmatter field. The
  citation check follows the relay rather than preceding it, because a
  wrong citation in conversation costs a correction while a wrong one
  in the record outlives the loop. The order
  has one named exception, defined under *What a diff-scoped LGTM
  certifies* below: a plan's diff-scoped LGTM.
```

Replace with:

```
- On the completion notification, in one turn and in this order:
  verify the agent's model self-report (the comparison the lifecycle
  rule defines), write the dispatch record defined below, relay the
  report to the developer, check every citation the report supplies
  against what it names, then stamp the verdict (`LGTM` | `concerns` |
  `blocking`) into the reviewed document's `architect:` /
  `adversary:` frontmatter field. The citation check follows the relay
  rather than preceding it, because a wrong citation in conversation
  costs a correction while a wrong one in the record outlives the
  loop. The order has one named exception, defined under *What a
  diff-scoped LGTM certifies* below: a plan's diff-scoped LGTM.
```

- [ ] **Step 3: Replace the relay bullet with five**

Find:

```
- The relay carries the verdict, the model self-report, and every
  finding in substance — condense narrative prose, never drop a
  finding or its severity.
```

Replace with:

```
- The dispatch record is written before the relay. The dispatcher
  saves what the agent returned, verbatim, under a four-line header —
  the date, the agent, the model self-report, and the subject — with
  no frontmatter and no `ticket`, since the record is evidence rather
  than a process artefact. It goes to `.claude/working-process/` at
  the repo root (`git rev-parse --show-toplevel`). A record survives
  compaction, the session's end and a branch switch, and no more; that
  bound is what the relay's condensation below leans on. Audits write
  none — a propagation gate's hits land in the ledger and an integrity
  audit's dispositions land as the edits it causes plus the
  `integrity:` stamp, so a record would give one fact a second home.
- The store is git-ignored by a `.gitignore` containing exactly `*`.
  Before writing a record the dispatcher ensures that file holds
  exactly that, rather than writing it once: the guard repairs a store
  directory made by hand, a file someone truncated, and a `git clean`
  that took the file and left the directory. A project already
  ignoring `.claude/` still gets the file, since the store may not
  depend on another file's contents.
- The record's name carries its agent and one discriminator:

      .claude/working-process/<stem>/<agent>-round-<N>.md
      .claude/working-process/<stem>/<agent>-<date>-<HH-MM-SS>.md

  `<stem>` is the reviewed document's basename without its extension,
  one directory per subject. A verdict agent takes the round ordinal,
  derived the way the heading will derive it — the highest ordinal the
  document's rounds carry, plus one, ordinals continuing across
  loops — because the record is written before that heading exists. A
  dispatch that reviews no document takes its subject as the stem,
  kebab-cased and capped at sixty characters, and the timestamp shape,
  having no ledger to draw an ordinal from; an `architect` dispatch on
  a bare question is one such, and the test is whether a document
  exists rather than which agent ran. Where a name is already taken,
  the new file appends the timestamp to the name it collided with —
  `<agent>-round-<N>-<date>-<HH-MM-SS>.md` — which settles the
  superseded round two sessions can produce on one ordinal without
  asking either to judge which report is stale.
- The relay opens with one header line, then one line per finding. The
  header carries the verdict, the model self-report, the finding count
  by severity, and how many decisions await the developer. Each
  finding takes one line — severity, origin, claim — except where the
  reviewer emits no origin: the `architect` reads one document and
  every finding it returns originates there, so an architect relay's
  line carries severity and claim alone.
- Condensation reaches narrative prose alone, whatever a session's
  output style prescribes. The finding list is never condensed, and no
  finding or its severity is ever dropped: the relay is the
  developer's standing veto, so a finding nobody printed is a finding
  nobody could overrule. Narrative is safe to condense because the
  dispatch record holds the full text, which makes an expansion a
  quotation rather than a reconstruction.
- The header's count of decisions is the findings for which the
  session can cite no license, derived at relay time from the report
  and the decisions already written down — before any ledger line
  exists, since `open` is written at stamp time and triage follows the
  stamp. The `held` lines the same round later writes are that count's
  check: they come to the same number, and a divergence means triage
  found a license the relay missed, triage lost one the relay claimed,
  or the oscillation tripwire held a finding that does carry a
  license. The third is lawful, so the check reports the number rather
  than asserting a fault. Verdicts that suspend autonomy — `blocking`,
  the spent round cap, the all-Minor signal — stay out of the count:
  they decide whether the loop continues rather than what a document
  says, and the relay reports them in its own right.
```

The indented block is six spaces, which is the bullet's two-space
content indent plus the four a code block needs. It renders as a code
block and is exempt from the wrap constraint, like every grammar example
the rules already carry.

- [ ] **Step 4: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 1`, `D 3`, `E 0`, `F 1`, `G 1`, `H 1`,
`I 1`, `J 1`.

`J 1` is the idempotent guard: the store's git-ignored state is ensured
before every record write rather than at a first use nothing defines.

`D 3` is the Global Constraints cap: once in the store sentence, once in
each filename shape, and a count of one would mean a shape went missing.
`E 0` is the invariant: any store path this wave wrote without the
`.claude/` prefix would raise it off zero.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): give the verdict relay a header and a dispatch record"
```

---

### Task 2: `workflow.md` — the consultation relay and its floor's site

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the
  `Dispatching a consultation` paragraph, between the model-selection
  paragraph and the glossary paragraph.

**Interfaces:**
- Consumes: Task 1's filename shapes, which this paragraph names rather
  than repeats.
- Produces: nothing later tasks read. Task 4 writes the persona-facing
  copy of the same floor and the two are edited together, as both files
  declare.

- [ ] **Step 1: Record the before values**

```bash
W=plugins/working-process/rules/workflow.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $W | grep -o 'compression' | wc -l)"
echo "B $(n $W | grep -o 'every recommendation and every named risk' | wc -l)"
echo "C $(n $W | grep -o 'never .\{0,12\}in one bullet' | wc -l)"
echo "D $(n $W | grep -o 'paragraph per focusing question' | wc -l)"
echo "E $(n $W | grep -o 'focusing question' | wc -l)"
echo "F $(grep -o '\.claude/working-process/' $W | wc -l)"
echo "G $(n $W | grep -o 'Relay each contribution attributed' | wc -l)"
```

Expected: `A 0`, `B 0`, `C 0`, `D 0`, `E 1`, `F 3`, `G 1`.

`A 0`, `B 0` and `C 0` are the measurement behind decision 2: the rule
that governs the dispatcher states no floor at all today. `E 1` counts
the briefing's existing mention of a focusing question, which this task
keeps; `F 3` is Task 1's cap, an invariant here.

- [ ] **Step 2: Rewrite the paragraph's close and add the shape**

Find:

```
never a resumption. When both personas are consulted on one subject,
give both the same canonical briefing, each with its own focusing
question appended, and tell neither what the other said. Relay each
contribution attributed and substantially verbatim, disagreements
presented as disagreements, and dispatch as a named background agent so
the transcript stays inspectable.
```

Replace with:

```
never a resumption. When both personas are consulted on one subject,
give both the same canonical briefing, each with its own focusing
question appended, and tell neither what the other said. Dispatch as a
named background agent, so the transcript stays inspectable.

A contribution is written to its dispatch record before it is relayed,
taking the timestamp shape of the two the verdict-agent dispatch
subsection defines: a consultation mints no round heading, so it has
no ordinal to derive, and several consultations of one persona on one
subject in one day are expected. The floor is met in that file —
attributed and substantially verbatim, compression allowed and merging
forbidden, every recommendation and every named risk surviving, and
text from two personas never landing in one bullet. The relay then
carries one paragraph per focusing question — or one per briefing,
where a single persona was consulted and none was appended — and the
path to the record. One thing stays in the relay whatever the floor
does: where the personas disagree, the disagreement is presented as a
disagreement with both positions, because a disagreement is the one
thing in a contribution the developer must decide and the digest
exists to raise decisions rather than bury them.
```

- [ ] **Step 3: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 1`, `D 1`, `E 2`, `F 3`, `G 0`.

`A 1` is the check the spec names as proof decision 2 landed. `E 2` is
the briefing's mention plus the relay's. `F 3` unchanged is the
deviation working: this paragraph points at the shapes instead of
repeating them.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): state the consultation floor and digest its relay"
```

---

### Task 3: `workflow.md` — triage holds a spec-origin finding

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — the consequences
  list of the triage paragraph in `### The review loop`, after the
  "Only written decisions license fixes" bullet.

**Interfaces:**
- Consumes: the field name `origin`, which Task 5 adds to the
  adversary's schema, and the cross-document clause Task 6 writes into
  the lifecycle rule — cited by rule and clause name, never by anchor.
- Produces: nothing later tasks read.

- [ ] **Step 1: Record the before values**

```bash
W=plugins/working-process/rules/workflow.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $W | grep -ow 'origin' | wc -l)"
echo "B $(n $W | grep -o 'editing a spec from inside a plan review is design work' | wc -l)"
echo "C $(n $W | grep -o 'Only written decisions license fixes' | wc -l)"
echo "D $(grep -ci 'owner' $W)"
```

Expected: `A 2`, `B 0`, `C 1`, `D 0`.

`A 2` counts `origin` as a whole word: the two Task 1 wrote into the
relay bullet, with `originates` in that same bullet correctly left out —
which a bare `grep -o 'origin'` would have counted. Run this task after
Task 1, or the expectation is `A 0`; either way this task adds two, the
field name and `spec-origin`. `C` is an invariant: the bullet this task
follows must survive it. `D` is the collision check the spec publishes,
and it is an invariant in both directions: `owner` is spent on an actor
elsewhere in the process and must never name a document here.

- [ ] **Step 2: Add the spec-origin bullet**

Find:

```
- Only written decisions license fixes. A decision settled in
  conversation becomes citable by being written into the document,
  which the fix itself accomplishes.
```

Replace with:

```
- Only written decisions license fixes. A decision settled in
  conversation becomes citable by being written into the document,
  which the fix itself accomplishes.
- A finding whose `origin` names the spec is held unless a written
  decision licenses the edit, since editing a spec from inside a plan
  review is design work; `both` holds the same way, and its `held`
  line names in `options:` which half is fixable at once. A licensed
  spec-origin fix lands in the spec's own ledger and the plan's line
  points at it, by the cross-document clause the spec-plan-lifecycle
  rule defines — which also leaves the spec's `integrity:` stamp
  stale, as any body edit does.
```

- [ ] **Step 3: Verify**

Run the Step 1 command again.

Expected: `A 4`, `B 1`, `C 1`, `D 0`.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): hold a spec-origin finding at triage"
```

---

### Task 4: the persona-facing copies of the consultation floor

**Files:**
- Modify: `plugins/working-process/PERSONA_COMMON.md` — the first bullet
  of *The reply* in `## The consultation contract`.
- Modify: `plugins/working-process/agents/architect-consult.md` — one
  bullet in `## Hard limits`.
- Modify: `plugins/working-process/agents/system-designer-consult.md` —
  the same bullet in its own `## Hard limits`.

**Interfaces:**
- Consumes: Task 2's dispatcher-facing text. `PERSONA_COMMON.md`
  declares that the dispatcher-facing copy lives in the workflow rule
  and that the two are edited together, which is why this task exists:
  editing one alone would recreate, in the other direction, the drift
  this wave repairs.
- Produces: nothing later tasks read.

- [ ] **Step 1: Record the before values**

```bash
P=plugins/working-process/PERSONA_COMMON.md
AC=plugins/working-process/agents/architect-consult.md
SD=plugins/working-process/agents/system-designer-consult.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $P | grep -o 'relayed to the developer attributed' | wc -l)"
echo "B $(n $P | grep -o 'dispatch record' | wc -l)"
echo "C $(n $P | grep -o 'every recommendation and every named risk survives' | wc -l)"
echo "D $(n $P | grep -o 'edited together' | wc -l)"
echo "E $(n $AC | grep -o 'relayed attributed and substantially verbatim' | wc -l)"
echo "F $(n $SD | grep -o 'relayed attributed and substantially verbatim' | wc -l)"
echo "G $(n $AC | grep -o 'kept attributed and substantially verbatim' | wc -l)"
echo "H $(n $SD | grep -o 'kept attributed and substantially verbatim' | wc -l)"
```

Expected: `A 1`, `B 0`, `C 1`, `D 1`, `E 1`, `F 1`, `G 0`, `H 0`.

`C` and `D` are invariants: the floor's content does not move, only its
site, and the sentence declaring the two copies edited together is what
licenses this task.

- [ ] **Step 2: Move the floor's site in `PERSONA_COMMON.md`**

Find:

```
- relayed to the developer attributed, in its own block, and
  substantially verbatim — compression is allowed, merging is not; every
  recommendation and every named risk survives, and text from two
  personas never lands in one bullet;
```

Replace with:

```
- written to the dispatch record and relayed from it. The record holds
  the contribution attributed, in its own block, and substantially
  verbatim — compression is allowed, merging is not; every
  recommendation and every named risk survives, and text from two
  personas never lands in one bullet. The relay carries one paragraph
  per focusing question — or one per briefing, where none was
  appended — and the path to the record; the workflow rule defines
  that record and names it;
```

- [ ] **Step 3: Correct the same claim on the architect's card**

In `plugins/working-process/agents/architect-consult.md`, find:

```
- Write the reply for the developer, not as a report to the dispatcher —
  the contract has it relayed attributed and substantially verbatim.
```

Replace with:

```
- Write the reply for the developer, not as a report to the dispatcher —
  the contract has it kept attributed and substantially verbatim in the
  dispatch record, which the developer can open.
```

- [ ] **Step 4: Correct it on the system designer's card**

In `plugins/working-process/agents/system-designer-consult.md`, find:

```
- Write the reply for the developer, not as a report to the dispatcher —
  the contract has it relayed attributed and substantially verbatim.
```

Replace with:

```
- Write the reply for the developer, not as a report to the dispatcher —
  the contract has it kept attributed and substantially verbatim in the
  dispatch record, which the developer can open.
```

The two blocks are identical on purpose: the sentence is duplicated in
the shipped cards, and correcting one alone would leave the personas
disagreeing about where their own words land.

- [ ] **Step 5: Verify**

Run the Step 1 command again.

Expected: `A 0`, `B 1`, `C 1`, `D 1`, `E 0`, `F 0`, `G 1`, `H 1`.

`B 1` counts the one place the bullet names the term; its later mentions
read "the record", and the check anchors the whole phrase. `C 1` and
`D 1` unchanged prove the floor's content and the edited-together
declaration both survived.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/PERSONA_COMMON.md \
        plugins/working-process/agents/architect-consult.md \
        plugins/working-process/agents/system-designer-consult.md
git commit -m "feat(working-process): meet the consultation floor in the dispatch record"
```

---

### Task 5: `plan-adversary.md` — the `origin` field

**Files:**
- Modify: `plugins/working-process/agents/plan-adversary.md` — the
  `## Output` schema and the close of `## Specs: decline`.

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: the field name `origin` and its three values, which Task 3's
  triage bullet and the glossary's **Origin** entry both read.

- [ ] **Step 1: Record the before values**

```bash
A=plugins/working-process/agents/plan-adversary.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '"origin"' $A)"
echo "B $(grep -c '"plan" | "spec" | "both"' $A)"
echo "C $(grep -c 'Handed a spec' $A)"
echo "D $(n $A | grep -o 'Naming a document is not reviewing it' | wc -l)"
echo "E $(grep -ci 'owner' $A)"
echo "F $(grep -c '"section": "<plan section or null>",' $A)"
```

Expected: `A 0`, `B 0`, `C 1`, `D 0`, `E 0`, `F 1`.

`C` is the spec-boundary invariant the spec names: this wave must not
disturb the decline. `E` is the `owner` collision check, an invariant at
zero in both directions.

- [ ] **Step 2: Add the field to the schema**

Find:

```
          "section": "<plan section or null>",
```

Replace with:

```
          "section": "<plan section or null>",
          "origin": "plan" | "spec" | "both",
```

The three values sit on one line, matching how the schema already writes
`verdict` and `severity`.

- [ ] **Step 3: Place the field inside the spec boundary**

Find:

```
Handed a spec (a design document, not an implementation plan)? Decline
the review and point the dispatcher at the `architect` agent. Plan
mechanics — named tests, per-phase commits, concrete paths — do not apply
to a design document and would misfire as findings.
```

Replace with:

```
Handed a spec (a design document, not an implementation plan)? Decline
the review and point the dispatcher at the `architect` agent. Plan
mechanics — named tests, per-phase commits, concrete paths — do not apply
to a design document and would misfire as findings.

Naming a document is not reviewing it. A finding whose `origin` is
`spec` or `both` says where the defect traces to and proposes no change
to the spec, so this boundary holds: what to do about a spec-origin
finding is the dispatcher's, and its own rules hold one for the
developer unless a written decision licenses the edit.
```

The sentence lands here rather than under `## Output` because the
boundary it qualifies is stated here, and a reader who wonders whether
`origin: spec` breaches the decline is reading this section.

- [ ] **Step 4: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 1`, `D 1`, `E 0`, `F 1`.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/agents/plan-adversary.md
git commit -m "feat(working-process): emit the finding's origin from the plan adversary"
```

---

### Task 6: `spec-plan-lifecycle.md` — the cross-document clause

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` — after
  the one-authorizer invariant in `## The disposition ledger`.

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: the clause Task 3's triage bullet cites by name.

- [ ] **Step 1: Record the before values**

```bash
L=plugins/working-process/rules/spec-plan-lifecycle.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(n $L | grep -o 'Every terminal line carries exactly one authorizer' | wc -l)"
echo "B $(n $L | grep -o 'other than the reviewed one' | wc -l)"
echo "C $(grep -c '^    ### <ISO date> — fix from' $L)"
echo "D $(n $L | grep -o 'one authorizer, two documents, two lines' | wc -l)"
echo "E $(n $L | grep -o 'One annotation extends those shapes' | wc -l)"
echo "F $(n $L | grep -o 'Two additions extend those shapes' | wc -l)"
echo "G $(n $L | grep -o 'is no counter-example' | wc -l)"
```

Expected: `A 1`, `B 0`, `C 0`, `D 0`, `E 1`, `F 0`, `G 0`.

`A` is the invariant the spec names: the clause must leave "every
terminal line carries exactly one authorizer" standing, because the
clause is what makes it hold across two documents rather than an
exception to it.

`E`, `F` and `G` belong to the two sentences Steps 3 and 4 amend. The
rule says today that one annotation extends the heading shapes and
nothing else does, and gives a gate's heading-lessness the ground that
the round heading's grammar is closed. Step 2 mints a heading, so
leaving those sentences would ship a rule contradicting itself —
`ruling: 2026-09-15`.

- [ ] **Step 2: Write the clause**

Find:

```
Every terminal line carries exactly one authorizer.
```

Replace with:

```
Every terminal line carries exactly one authorizer.

A fix one review licenses can land in a document other than the
reviewed one — a plan review's finding carrying `origin: spec` is the
case the workflow rule names. The disposition line then lands in the
ledger of the document that changed, and the reviewed document's line
points at it in its `<what changed>` clause, naming that document and
the heading the line sits under: one authorizer, two documents, two
lines, and the invariant above holds on each. The pointer needs no
clause of its own — `<what changed>` already belongs to the `fixed`
line's shape, so the clause table stays closed. In the changed
document the line goes under its latest round heading, or with the
body note the resolution
annotation above already owes, where that document is stamped and no
fresh round ran. A document whose loop closed at `LGTM` has neither —
the annotation is defined for `concerns` and `blocking` alone — so the
fix opens a heading of its own:

    ### <ISO date> — fix from <path of the reviewing document>

It carries no ordinal and no verdict, which keeps it out of the round
cap's derivation and out of the Unfinished-work commands that anchor a
round heading: it records a fix, not a round. Two stamps go stale as on
any body edit — the `integrity:` hash stops matching, and the verdict
stops certifying the words that changed.
```

- [ ] **Step 3: Admit the fix heading to the closed shape set**

Find:

```
One annotation extends those shapes, and nothing else does. A
diff-scoped `LGTM` heading gains `, debt discharged <date>` once the
```

Replace with:

```
Two additions extend those shapes, and nothing else does: the
annotation here, and the cross-document fix heading above. A
diff-scoped `LGTM` heading gains `, debt discharged <date>` once the
```

- [ ] **Step 4: Say why a gate still mints no heading**

Find:

```
one. A gate still never mints a heading of its own, on the separate
ground that the round heading's grammar is closed and a gate is not a
round. Writing at gate
```

Replace with:

```
one. A gate still never mints a heading of its own, on the separate
ground that the round heading's grammar is closed and a gate is not a
round. The fix heading above is no counter-example: a gate's lines can
wait for the round that is coming, while a fix landing on a document
whose loop closed at `LGTM` waits for nothing. Writing at gate
```

- [ ] **Step 5: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 1`, `D 1`, `E 0`, `F 1`, `G 1`.

`E 0` is the point of Step 3: the sentence claiming one extension is
gone, replaced by the one claiming two.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): land a cross-document fix in its own ledger"
```

---

### Task 7: the glossary — Dispatch record, Relay, Contribution

**Files:**
- Modify: `docs/domain/glossary.md` — the **Relay** entry, a new
  **Dispatch record** entry after it, and the **Contribution** entry.

**Interfaces:**
- Consumes: Task 1's store path and durability bound, which the new
  entry restates in the term's own voice.
- Produces: nothing later tasks read.

- [ ] **Step 1: Record the before values**

```bash
G=docs/domain/glossary.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "A $(grep -c '^\*\*Origin\*\*:' $G)"
echo "B $(grep -c '^\*\*Dispatch record\*\*:' $G)"
echo "C $(n $G | grep -o "consultation's Contribution attributed and substantially verbatim" | wc -l)"
echo "D $(n $G | grep -o 'NOT a Process directory' | wc -l)"
echo "E $(n $G | grep -o 'held attributed and substantially verbatim in its Dispatch record' | wc -l)"
echo "F $(grep -c '^\*\*Review report\*\*:' $G)"
```

Expected: `A 1`, `B 0`, `C 1`, `D 1`, `E 0`, `F 1`.

`A 1` is W3's third site, already delivered: the **Origin** entry was
minted at the grilling, so this task verifies it rather than writing it
(deviation 3). `D 1` counts **Private memory**'s exclusion, which the
new entry copies in the same words; after this task it is `2`. `F` is an
invariant — **Review report** stays the distinct term the new entry
contrasts itself with.

- [ ] **Step 2: Amend Relay and mint Dispatch record**

Find:

```
**Relay**:
The delivery of a background agent's result to the developer before any
further action on it — a verdict agent's report before its stamp (the
verdict, the model self-report, and every finding in substance), a
consultation's Contribution attributed and substantially verbatim. The
developer's standing veto point.
_Avoid_: report back, forward (as the term)
```

Replace with:

```
**Relay**:
The delivery of a background agent's result to the developer before any
further action on it — a verdict agent's report before its stamp (a
header carrying the verdict, the model self-report and the counts, then
one line per finding, that list never condensed), a consultation's
Contribution digested one paragraph per focusing question. Either way it
names the Dispatch record holding the full text. The developer's
standing veto point.
_Avoid_: report back, forward (as the term)

**Dispatch record**:
The file a dispatcher writes before relaying a background agent's
result — one dispatch, one file, holding what the agent returned
verbatim under a four-line header (date, agent, model self-report,
subject). Kept per subject under `.claude/working-process/<stem>/`,
git-ignored, and NOT a Process directory — a per-checkout store under
the `.claude/` config namespace, as Private memory is a per-user one. It
survives compaction, the session's end and a branch switch, and no more:
that bound is what lets a Relay condense. Never a Review report, the
counted document a code-review run writes under `docs/code-review/`.
_Avoid_: dispatch log, transcript file
```

The exclusion is worded as **Private memory** words its own, which is
what keeps the store outside the Process-directory class by definition
rather than by a rule about prefixes. The two differ where the facts
do — Private memory is per-user, a dispatch record store per-checkout.

- [ ] **Step 3: Amend Contribution**

Find:

```
**Contribution**:
What a consultation returns: reasoning, options, and the questions the
persona would need answered next, relayed to the developer attributed and
substantially verbatim. Never graded and never counted — the graded,
counted unit is a Finding, which belongs to verdict-bearing reviews.
```

Replace with:

```
**Contribution**:
What a consultation returns: reasoning, options, and the questions the
persona would need answered next, held attributed and substantially
verbatim in its Dispatch record and relayed from there as a digest.
Never graded and never counted — the graded, counted unit is a Finding,
which belongs to verdict-bearing reviews.
```

- [ ] **Step 4: Verify**

Run the Step 1 command again.

Expected: `A 1`, `B 1`, `C 0`, `D 2`, `E 1`, `F 1`.

- [ ] **Step 5: Commit**

```bash
git add docs/domain/glossary.md
git commit -m "docs(glossary): mint the dispatch record and move the relay's floor"
```

---

### Task 8: end-state sweep

**Files:** none modified. This task reads.

**Interfaces:**
- Consumes: every earlier task.
- Produces: the report the developer acts on.

- [ ] **Step 1: Run every check the spec publishes**

```bash
W=plugins/working-process/rules/workflow.md
P=plugins/working-process/PERSONA_COMMON.md
A=plugins/working-process/agents/plan-adversary.md
L=plugins/working-process/rules/spec-plan-lifecycle.md
G=docs/domain/glossary.md
n() { tr -s '[:space:]' ' ' < "$1"; }
echo "01 $(n $W | grep -o 'The relay opens with one header line' | wc -l)"
echo "02 $(n $W | grep -o 'finding list is never condensed' | wc -l)"
echo "03 $(n $W | grep -o 'output style' | wc -l)"
echo "04 $(n $W | grep -o 'compression' | wc -l)"
echo "05 $(n $W | grep -o 'every recommendation and every named risk' | wc -l)"
echo "06 $(n $W | grep -o 'never .\{0,12\}in one bullet' | wc -l)"
echo "07 $(n $W | grep -o 'paragraph per focusing question' | wc -l)"
echo "08 $(n $P | grep -o 'dispatch record' | wc -l)"
echo "09 $(n $L | grep -o 'other than the reviewed one' | wc -l)"
echo "10 $(n $L | grep -o 'Every terminal line carries exactly one authorizer' | wc -l)"
echo "11 $(grep -c '"origin"' $A)"
echo "12 $(grep -c '"plan" | "spec" | "both"' $A)"
echo "13 $(grep -ci 'owner' $A) $(grep -ci 'owner' $W)"
echo "14 $(grep -c 'Handed a spec' $A)"
echo "15 $(n $W | grep -o 'editing a spec from inside a plan review is design work' | wc -l)"
echo "16 $(grep -c '<agent>-round-<N>\.md' $W) $(grep -c '<agent>-<date>-<HH-MM-SS>\.md' $W)"
echo "17 $(grep -o '\.claude/working-process/' $W | wc -l) $(grep -o '\.working-process/' $W | wc -l)"
echo "18 $(n $W | grep -o 'git-ignored by a .\.gitignore. containing exactly' | wc -l)"
echo "19 $(grep -c '^\*\*Dispatch record\*\*:' $G)"
echo "20 $(grep -c '^\*\*Origin\*\*:' $G)"
```

Expected, in order: `1`, `1`, `1`, `1`, `1`, `1`, `1`, `1`, `1`, `1`,
`1`, `1`, `0 0`, `1`, `1`, `1 1`, `3 0`, `1`, `1`, `1`.

Line `13` is the collision check in both files. Line `17` reads two
different things: the store path, expected three, and a store path
written without the `.claude/` prefix, expected zero — the spec's own
check, and zero because the pattern needs a dot immediately before
`working-process`, where `.claude/working-process/` puts a slash. Lines
`10`, `13`, `14`, `17`'s second half and `20` are invariants:
they read the same before and after the wave, and each is here because
something in it could have disturbed them.

- [ ] **Step 2: Validate the plugin and the marketplace**

```bash
claude plugin validate plugins/working-process && claude plugin validate .
```

Expected: both pass.

What this does not cover: `validate` reads the manifest and the
component frontmatter, never a rule's body — `rules/*.md` is not a
component, so nothing here proves a rule file parses or says what it
means. The agent cards Tasks 4 and 5 touched do have frontmatter, and
none of those edits goes near it.

- [ ] **Step 3: Confirm no line this wave wrote breaks the wrap**

The check reads the diff, not the files: a whole-file count of long
lines moves whenever anything else moves and cannot tell this wave's
lines from the ones already there. Two forms are excluded because they
cannot wrap — lines indented four spaces or more are grammar examples,
a form the rules use throughout, and the JSON schema line Task 5 adds is
one of them; table rows begin with a pipe.

```bash
BASE=$(git merge-base HEAD develop)
git diff "$BASE"..HEAD -- plugins/working-process docs/domain/glossary.md \
  | grep '^+' | grep -v '^+++' | sed 's/^+//' \
  | LC_ALL=C.UTF-8 awk 'length > 72 && $0 !~ /^    / && $0 !~ /^\|/ {print "("length") "$0}'
```

Report how many added lines the check examined before reporting the
result, so an empty output is read as "none of N broke the wrap" rather
than as a command that matched nothing:

```bash
git diff "$BASE"..HEAD -- plugins/working-process docs/domain/glossary.md \
  | grep -c '^+[^+]'
```

Expected: no output from the first command. Any line it prints is one
this wave added; rewrap it in the file that owns it and commit as
`style(working-process): rewrap <file>`. Do not reflow a paragraph this
wave did not change — it will not appear here anyway.

- [ ] **Step 4: Confirm the two declared-together copies agree**

```bash
n() { tr -s '[:space:]' ' ' < "$1"; }
for f in plugins/working-process/rules/workflow.md \
         plugins/working-process/PERSONA_COMMON.md; do
  echo "$f $(n $f | grep -o 'every recommendation and every named risk' | wc -l)" \
       "$(n $f | grep -o 'compression' | wc -l)"
done
```

Expected: each file reports `1 1`.

This is the wave's own defect turned into a check. `PERSONA_COMMON.md`
declares that the dispatcher-facing copy lives in the workflow rule and
the two are edited together; they had drifted until this wave, with the
persona copy holding the whole floor and the rule holding none of it.
Equal counts are what the declaration claims.

- [ ] **Step 5: Report the end state**

State to the developer: four changes landed across seven files, nothing
created, every published check at its expected value, and
`claude plugin validate` passing for the plugin and the marketplace.

Then state the delivery gap in its own sentence: this branch's rules are
not the rules any session is running, and will not be until the plugin
cache carries this branch — either through a release, or through a
prerelease install whose version convention the repo's plugin-versioning
rule defines and whose install procedure is the developer's own. Neither
the drift hook nor `sync-rules` will announce that, because both read
the cache rather than this checkout.

Name the three things this plan deliberately left undone — the install,
the version bump, and moving the spec's `status` to `implemented` — and
that all three are theirs.

Do not commit in this task; it modifies no file.

## Self-review

**Spec coverage.** W1 → Task 1. W2 → Task 2 (`workflow.md`) and Task 4
(`PERSONA_COMMON.md`, plus the two consult cards deviation 2 adds). W3 →
Task 5 (`plan-adversary.md`), Task 3 (`workflow.md`), Task 6
(`spec-plan-lifecycle.md`) and Task 7's invariant on the **Origin**
entry the grilling already minted. W4 → Task 1 (`workflow.md`, verdict
side), Task 2 (consultation side) and Task 7 (the glossary entry). The
spec's four Out-of-scope entries produce no task by construction. Every
check in the spec's *Verification* section appears in Task 8 Step 1,
with the path count corrected to three as the integrity audit ruled.

**Placeholder scan.** Every step carries the literal text to write and
the command to run. The only bracketed tokens are `<stem>`, `<agent>`,
`<N>`, `<date>`, `<HH-MM-SS>` and `<ISO date>`, which are the shipped
rules' own placeholders and are meant to reach the file verbatim.

**Type consistency.** The field is `origin` in all four places that name
it — the schema (Task 5), the triage bullet (Task 3), the glossary entry
(already in the file) and the relay's finding line (Task 1). Its values
are `plan`, `spec`, `both` everywhere. The store path is
`.claude/working-process/<stem>/` in Tasks 1 and 7 and is named rather
than spelled in Task 2, which is what holds the count at three. The
artefact is a **dispatch record** in every task; `report file` appears
nowhere, being banned by **Review report**'s `_Avoid_` list.

## Review rounds

### 2026-09-15 — plan-adversary, fable 5.1, blocking (round 1, full-document)

The propagation gate ran three times before this dispatch. Its lines are
written here, under the first round heading, as the grammar directs for
an episode that precedes a document's first round.

- hit fixed 2026-09-15 — Task 4 expected the phrase `dispatch record` twice where its replacement names the term once, later mentions reading "the record"; recounted by applying the replacement to a scratch copy, corrected to one, and the same figure corrected in Task 8's sweep line
- hit fixed 2026-09-15 — the bare store-path check expected three where `\.working-process/` cannot match inside `.claude/working-process/`, a slash sitting where the pattern needs a dot; measured on constructed text, corrected to zero and declared an invariant, and four counts moved from `grep -c` to `grep -o | wc -l` so they count occurrences rather than lines
- hit dismissed 2026-09-15 — Task 7's Find block was reported as failing the byte-exact duty for covering only part of the **Contribution** entry; counter: a Find block is a substring and the duty is byte-exact and unique, measured at exactly one occurrence, and applying the replacement leaves that entry's `_Avoid_` line in place
- hit fixed 2026-09-15 — the Self-review claimed the spec has five Out-of-scope entries where its section lists four; recounted against the section's bullets and corrected to four
- hit fixed 2026-09-15 — Task 8's end-state report claimed four changes across six files where the plan's own `Modify:` lines name seven distinct paths, the Task 4 bullet carrying two of them; enumerated those lines and corrected to seven
- fixed 2026-09-15 — [Important] Task 3's `A` counted `origin` as a bare substring, so `originates` in Task 1's relay bullet leaked in and both expectations were wrong in both directions; license: the plan's Global Constraints, which require a step's values measured rather than predicted; the check is now `grep -ow` and the expectations are 2 and 4, verified by simulating both tasks on a scratch copy
- fixed 2026-09-15 — [Important] Task 6 said the resolution annotation is defined for `concerns` and `blocking` alone where the spec says `concerns` alone, departing from the spec with no Deviations entry; license: `spec-plan-lifecycle.md`'s resolution-annotation bullet, which gives an adjudicated `blocking` verdict the same form with the round's ledger record as its body note; deviation 5 now records the departure and its ground
- fixed 2026-09-15 — [Important] the collision rule said only that the new file appends the timestamp, leaving two sessions to spell one name two ways, where the spec's integrity audit routed the exact concatenation to this plan; license: spec decision 5, which decides the append, and that routing; the bullet now carries `<agent>-round-<N>-<date>-<HH-MM-SS>.md`, measured not to disturb either filename check
- fixed 2026-09-15 — [Important] Task 6 mints a heading shape inside `## Review rounds` while `spec-plan-lifecycle.md` keeps "One annotation extends those shapes, and nothing else does" and, for gate lines, "the round heading's grammar is closed", so the shipped rule would contradict itself after the edit; ruling: 2026-09-15; Task 6 gains Steps 3 and 4 amending both sentences — the shape set now admits two additions, the annotation and the fix heading, and the gate sentence says why the fix heading is no counter-example, a gate's lines being able to wait for the round that is coming — plus checks E, F and G anchoring the amended text
- fixed 2026-09-15 — [Important] the store's git-ignored guarantee rested on a `.gitignore` "written at its first use" with nothing defining first use, so a store directory already present without the file never got one and its records became untracked files a `git add -A` would commit; ruling: 2026-09-15; the guard is idempotent — before every record write the dispatcher ensures the file holds exactly `*`, which repairs a directory made by hand, a truncated file and a `git clean` that took the file and left the directory — the store bullet is split so the guard stands on its own, and check J anchors it
- fixed 2026-09-15 — [Minor] Task 2 said a consultation records nothing one sentence after saying a contribution is written to its record; license: the glossary's **Consultation** entry, whose discriminator is stamping rather than recording; the clause now says a consultation mints no round heading, which is the property the ordinal argument actually needs
- fixed 2026-09-15 — [Minor] the store path carried no base, where the plugin's own shared file records that a dispatch inherits a working directory possibly below the root and that the miss is silent; license: `PERSONA_COMMON.md`'s glossary-duty paragraph, which resolves its own path against the repo root for that reason; the bullet now says at the repo root and names the command
- fixed 2026-09-15 — [Minor] "the reviewed document's line points at it" named no clause while the ledger's clause table is closed; license: the `fixed` line's own shape, whose `<what changed>` clause carries the pointer without a new row; the clause now says so and states that the table stays closed
- signal 2026-09-15 — a further round earns its cost only as a diff-scoped read over Tasks 1 and 6, where the fixes reshape rule text and repair-born defects are the likely failure; the counter fix and the deviation entry are mechanical and the propagation gate verifies them without a round, and the three Minors are one sentence each

### 2026-09-15 — plan-adversary, fable 5.1, concerns (round 2, diff-scoped)

- held — [Important] the collision rule appends the timestamp to the name it collided with, which settles the ordinal shape but not the timestamp shape: two dispatches of one agent on one subject landing in the same second collide on `<agent>-<date>-<HH-MM-SS>.md`, and appending the same timestamp reproduces a name already taken, so the second record overwrites the first; question: how does a timestamp-shape collision resolve?; options: (a) scope the timestamp append to the ordinal shape, which is the case spec decision 5 gives as its reason, and give the timestamp shape the lowest free counter suffix, `-2` then `-3` — recommended, deterministic and clock-free, with the spec's decision 5 sentence corrected by the cross-document clause this wave defines; (b) sub-second precision in every timestamp name, which changes the filename shape the developer settled and Task 1's `G` check; (c) state the collision as accepted, which loses a record rather than merely misordering one; counter: the finding traces to both documents — spec decision 5 states the append for every taken name under `ruling: 2026-09-14`, so its spec half is not the session's to edit
- held — [Minor] spec decision 3 says the resolution annotation "is defined for `concerns` alone" where the shipped rule defines it for an adjudicated `blocking` as well; the plan already follows the rule through deviation 5, so only the spec carries the error, and it would freeze into an `implemented` document amendable only in frontmatter; question: correct the spec's clause now, while the spec is still `approved`?; options: (a) correct it through the cross-document clause this wave defines, landing the line with the spec's existing resolution note and pointing at it from here, accepting that the spec's `integrity:` stamp goes stale as the rule says any body edit makes it — recommended, and one spec edit can carry the spec half of the finding above with it, so the stamp goes stale once rather than twice; (b) leave the spec as it stands, relying on deviation 5 to record the disagreement
- signal 2026-09-15 — a further round does not earn its cost: the Important is a one-or-two-sentence fix the propagation gate verifies mechanically, and the Minor is held for the developer whatever a round finds, being spec-origin; a diff-scoped round three would mostly re-confirm a small patch
