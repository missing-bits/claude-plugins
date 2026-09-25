---
ticket: none
date: 2026-09-25
status: draft
grilled: 2026-09-25
architect: concerns
decisions: registered
branch: feature/plan-coverage
base: develop
---

# Plan coverage — every registered decision has an owner

A plan can drop a decision its design spec made, and today no reader
notices. This spec gives the design spec an enumerable register of the
decisions that need realization, puts each decision's identifier on the
plan tasks that realize it, and has the propagation auditor derive the
coverage from those two lists. The judgment of whether a cited task
really realizes its decision stays with the plan-adversary.

## Problem

Measured in an outside project: a spec carried an eight-row revisions
table, the plan implemented six rows, and no task owned row 6. Two
plan-adversary rounds, three propagation audits and the author's
self-review all passed the plan, because each read the plan against
itself — internal consistency, invented identifiers, wrong anchors — and
none carried "every decision has an owning task" in its brief. The gap
surfaced on the next live walk and cost two extra tasks.

What stands today:

- The plan-adversary's dimension 5 judges whether a plan covers every
  `new`, `changed` or `retired` **part** of a technical design. Nothing
  checks the design spec's decisions — with a technical design or
  without one.
- The propagation auditor walks nine mechanical duties. None is a
  coverage check, and none checks that a column naming another table's
  rows resolves.
- Design specs carry no uniform decision list: some have a numbered
  `## Decisions`, some `## Settled decisions`, some none. A numbered
  Markdown list is positional, so its "decision 5" moves when an item
  above it is added.

## Decisions

- **D1** — A design spec that sets `decisions: registered` in its
  frontmatter carries a `## Decisions` section: the decision register.
  Argued in *The register*.
- **D2** — The register is an index, never a copy: an entry is one
  identity paragraph — the identifier and a short statement of the
  decision — and may point at the section that argues it. Argued in
  *The register*.
- **D3** — Identifiers are stable, unique within the spec, and never
  positional or reused. An element of a list that needs realization on
  its own takes a child identifier (`D4.1`); a parent with children is a
  group and is never itself covered. Argued in *The register*.
- **D4** — The register lists every decision that needs realization,
  cross-cutting constraints and "leave X unchanged" rulings included —
  the latter realized as constraints. Rejected alternatives stay out.
  Argued in *What enters the register*.
- **D5** — An entry carries one state token or none:
  `withdrawn <reason>, ruling: <date>[; replaced by <id>]`. Only a leaf
  carries it, and the session writes it only on the developer's
  explicit decision. Argued in *Entry states*.
- **D6** — The spec author creates the register, with or without a
  grilling session; the grilling session updates it as decisions land.
  Argued in *Who writes the register*.
- **D7** — A plan descending from at least one registered spec carries
  `**Realizes:**` on every task, with identifiers or `none`, and
  identifiers on the specific Global Constraints entries that realize a
  constraint. Argued in *The plan's annotations*.
- **D8** — The lifecycle rule's sentence "changes no plan template"
  is revised: working-process adds exactly the D7, D18 and D19
  annotations, and the tool that writes plans keeps the rest of the
  template. Argued in *The
  plan's annotations*.
- **D9** — A new propagation duty derives coverage: every leaf
  identifier of every registered spec that is neither withdrawn nor
  deferred by the audited plan needs a realizing task or constraint,
  and the register itself must be well formed. Argued in *The coverage
  duty*.
- **D10** — A second new propagation duty checks table closure: where
  the rule defining a table declares that a column names rows of
  another table, every name resolves to exactly one row. Argued in
  *Table closure*.
- **D11** — The auditor's report gains one `decision-coverage:` block
  per spec the audited plan names — a summary line and, where the
  register could be counted, the map from identifier to citing sites —
  before the closing token, on clean runs too; `CLEAN`
  means no hit in the checks that ran. Argued in *The report*.
- **D12** — A coverage hit stays a hit, but its fix is triaged by
  license, and a fix needing a decision the spec does not make waits
  for the developer. The exception to "hits never wait" covers coverage
  hits alone. Argued in *Disposing of a coverage hit*.
- **D13** — Four gate-line shapes record that wait: `hit held`, and
  its three terminal rewrites `hit fixed …; ruling:`,
  `hit deferred …; ruling:` and `hit withdrawn …; ruling:`. `hit held`
  joins the Unfinished-work list. Argued in *Gate lines for a held
  hit*.
- **D14** — The plan-adversary gains a dimension judging each
  decision's realization: do the tasks and constraints citing it
  realize it in full together, and does a cited constraint actually
  bind. Argued in *Readers*.
- **D15** — The integrity auditor checks the register's completeness
  through its existing first lens, prompted by one sentence in its card.
  Argued in *Readers*.
- **D16** — `propagation-duties.md`, the author's checklist, changes in
  three independent ways. Argued in *The author's checklist*.
  - **D16.1** — It gains a row each for the D9 and D10 duties.
  - **D16.2** — Its duty and edit counters are recounted.
  - **D16.3** — Its duty-2 row gains the anchor case the card states
    and the row omits.
- **D17** — A spec without the `decisions:` field is reported as
  `not checked` and yields no hit; existing specs migrate at a
  substantive revision, never in a sweep. Argued in *Legacy specs*.
- **D18** — A plan that leaves a registered decision unrealized says so
  in a `**Defers:**` line, one per decision, carrying the developer's
  ruling; the deferral binds that plan alone, and the spec names no
  plan. Argued in *Deferral*.
- **D19** — A plan continuing work an `implemented` plan began names
  that plan in a `**Follows:**` line and inherits the decisions its
  `**Realizes:**` annotations cite, never its deferrals. Argued in
  *Sequential plans*.

## The register

The register is the one enumerable source this check needs. Without it,
the list of decisions exists only in the reader's head, and the author
who dropped row 6 from the plan drops it from any list they write
afterwards.

An entry opens with its identity paragraph:

    - **D3** — <one sentence stating the decision, wrapped as the
      file wraps>. [state token]

      <optional prose, indented, after a blank line>

The identity paragraph is the list item's first paragraph: its opening
line and the continuation lines that follow it, up to the first of: a
blank line, a nested list item, the next list item at the same or a
higher level, or the end of the section. The auditor joins those lines,
normalising whitespace, and parses the result, so a sentence wrapped
across lines keeps its state token, which stands at the paragraph's
end. Prose beneath, after the blank line, is free.

The identifier is the literal token `**D<n>**` or, for a child,
`**D<n>.<m>**`, at the start of a list item under `## Decisions` — a
child's item nested under its parent's, where it opens the child's own
identity paragraph. A Markdown numbered list is refused on purpose: its
numbers are positions, and a positional reference breaks when an item
is inserted above it.

An entry states the decision briefly and, where the argument is long,
names the section that makes it. The grammar enforces the paragraph's
shape, never a sentence count: brevity is authoring guidance with no
mechanical reader. Restating the argument in the register would give
the decision two homes, and the first fix wave would leave the register
describing the decision's old form — the defect an integrity audit
exists to catch, manufactured by the register itself.

Identifiers are never renumbered and never reused. A decision added
mid-loop takes the next free number. A list whose elements each need
realization — the eight-row table of the measured failure — gives each
element a child identifier. Registering that table as one decision
would let one task citing it pass as 8/8 while realizing six rows,
which is the failure this spec exists to catch. The parent of children
is a group: it enters no count, citing it covers none of its children,
and it carries no state token. A withdrawal or a deferral of the whole
group is written for each of its leaves, since the leaves are what the
count reads.

## What enters the register

Every decision that needs realization enters, cross-cutting constraints
included. A ruling that something stays as it is — "leave the gate
order unchanged" — needs realization too, since an implementer can break
it; its realization is a Global Constraints entry. There is therefore no
exempt kind of entry, and no way to reach full coverage by declaring
decisions exempt.

A rejected alternative never enters: nobody realizes it, and it already
has homes — a spec's out-of-scope section, a technical design's *Cuts
not taken*.

## Entry states

An entry without a token is active. One state token exists, a leaf
carries it or not, and a group never does:

    withdrawn <reason>, ruling: <date>[; replaced by <id>]

The decision no longer stands. The entry stays as a tombstone that
reserves its identifier; `replaced by` names the successor where one
exists. A decision that still stands but one plan does not realize is
not a state of the entry at all — that is a deferral, and the plan
records it (see *Deferral*).

A tombstone keeps the identifier visibly taken, so a reuse shows up as
a duplicate, and a plan still citing it gets a hit that says why. Two
constraints bind `replaced by`: it names an identifier that exists in
the same register and differs from its own, and a chain of successors
never forms a cycle. A successor may itself be withdrawn.

A withdrawal is not a disposition of a hit: it changes what the spec
decides, so the session writes the token only on the developer's
explicit decision, and the edit lands in the spec's own ledger. That
edit leaves the spec's `integrity:` stamp stale, as any body edit does,
and correctly so. Withdrawing a decision of a spec already
`implemented` is no edit of its frozen body but a revision: a newer
design spec carries `revises:` and the register that stands.

The token's `ruling:` is a Ruling in the glossary's sense, dated with
the developer's decision rather than with the edit that recorded it.
It protects that decision from a reviewer's re-raise, never from the
developer, whose later ruling may revise it like any other.

The duplicate check does not catch an author who overwrites a tombstone
with a new active decision under the same identifier; only a comparison
against an earlier version could. Never reusing an identifier stays an
authoring rule, and this spec claims no more for the tombstone than the
duplicate check gives.

## Who writes the register

The spec author creates the register while writing the spec, so a
design that never meets a grilling session still gets one. A grilling
session updates it as its decisions land, the way it already updates
the glossary and the ADRs.

The lifecycle rule states, for every spec carrying
`decisions: registered`, the rule the spec thereby declares about
itself: *the register lists every decision in this spec that needs
realization.* Declared rules are what the integrity auditor's first lens
verifies in both directions, which is how the register's completeness
gets a reader (see *Readers*).

## The plan's annotations

A plan whose `spec:` names at least one registered spec carries, on
every task, beside its `**Interfaces:**` block:

    **Realizes:** D3, D5
    **Realizes:** none

`none` is a value, not an omission. Without it the auditor cannot tell a
housekeeping task from an author who forgot, and it would either report
a false hit or miss a real one.

A cross-cutting constraint is realized by the Global Constraints entry
that states it, and that entry opens with the same annotation, as its
first clause — `**Realizes:** D9`. One shape serves both sites: the
values, the qualification of identifiers and the wrapping rules are
shared, and only the place differs. Citing the section as a whole
realizes nothing.

A plan descending from one spec uses bare identifiers. A plan descending
from several qualifies each identifier with that spec's path exactly as
the plan's `spec:` writes it — `../specs/<file>.md#D3` — since two specs
may share a basename, and a bare identifier in a multi-spec plan is a
hit.

The annotation sits on the task rather than in a table at the top of
the plan, for two reasons. Ownership is per task, which is the shape of
the measured failure. And an implementer who sees only their own task
learns from the annotation which decision it realizes.

This extends the plan template, and the lifecycle rule currently says
the plugin does not: "This binds how the blocks are filled and changes
no plan template — the template belongs to the tool that writes plans."
The sentence is revised to name the exception: working-process adds the
`**Realizes:**` annotation on tasks and constraint entries, the
`**Defers:**` lines of *Deferral* and the `**Follows:**` lines of
*Sequential plans*, and the rest of the template stays with the tool
that writes plans.

The plan's author writes the annotations, whoever that author is, and
the requirement lives in the lifecycle rule; the tool that writes plans
is not changed. A session writing the plan itself meets the rule when
it reads the design spec, since the rule loads on `docs/specs/**`. A
plan delegated to a separate context cannot count on that load, so the
delegating brief names the lifecycle rule and requires reading it
before the plan is written. A plan that lacks the annotations anyway is
caught at its first gate, and the missing lines take the triage of
*Disposing of a coverage hit*: an identifier is added by fix (a) only
where the task's text actually realizes the decision, never
mechanically.

## Deferral

A decision that stands, but that this plan does not realize, is
deferred by the plan, not by the spec:

    **Defers:** D6 — <why>; ruling: <date>

The lines close the Global Constraints section, after its last entry,
one line per deferred identifier, qualified as the plan's
`**Realizes:**` annotations are. They state facts about the whole plan,
never about the constraint entry above them. Each carries the
developer's ruling, and the session writes it only on the developer's
explicit decision.

The plan is the right home for three reasons. The deferral is a fact
about this plan — the decision still stands — so it binds this plan
alone by construction: auditing any other plan descending from the same
spec, the decision counts, and a later plan meant to take it over and
not doing so gets the coverage hit (see *Sequential plans*). The spec
names no plan, which keeps pointers running from the plan to the spec
as they always do. And an
`implemented` spec, whose body is frozen, never needs editing for a
later plan to defer one of its decisions.

A `**Defers:**` line naming an identifier the register does not define,
a withdrawn one or a group is a hit. So is one identifier both deferred
and cited by a `**Realizes:**` annotation in the same plan: the plan
cannot both realize and defer it. The plan-adversary does not judge a
deferral the developer ruled; it judges a plan whose other tasks quietly
depend on the deferred decision anyway.

## Sequential plans

Work on one spec can run through several plans in sequence: a later
plan picks up where an earlier one stopped. The later plan names each
such predecessor on a line of its own, closing the Global Constraints
section beside its `**Defers:**` lines:

    **Follows:** ../plans/<file>.md

The path is written relative to the plan. A predecessor must share at
least one spec with the later plan's `spec:` and carry
`status: implemented`: an implemented plan's body is frozen, so what it
cited is settled and the owner of a decision cannot move, while a draft
could lose a citation it lent. Whether that realization still stands
in the code is not coverage's question; the lifecycle rule's diff
against the named surfaces answers it. A predecessor lends identifiers
only for the specs both plans name: in the pass for a spec it does not
name, its `**Follows:**` line is out of scope rather than a hit. A
`**Follows:**` line naming a missing file, a plan sharing no spec with
the later plan, or a plan not yet implemented is a hit.

The later plan inherits every identifier its predecessors'
`**Realizes:**` annotations cite, and nothing else: a predecessor's
`**Defers:**` lines are never inherited, so a decision an earlier plan
deferred counts in the later one until that plan realizes or defers it
itself. Nor are its `**Follows:**` lines: inheritance is not
transitive, so a plan drawing on a chain names every implemented
predecessor whose citations it relies on. The coverage map shows an inherited identifier with the plan it
comes from — `D3 → ../plans/<file>.md (Task 4)`.

The automatic alternative — excluding whatever any other plan of the
same spec cites — was refused: two draft plans could each exempt the
other from one decision, and a plan's result would change when an
unrelated draft appeared. Splitting one spec's decisions across plans
written in parallel needs a contract of its own, and this spec does not
design one.

Inherited coverage is taken as settled, not re-judged. A predecessor
passed its own review and shipped, and the plan-adversary reads plans,
not the code that implemented them, so it cannot re-verify that work.
What it judges is the later plan: a task that changes or undoes what an
inherited decision required is a finding against the plan under review.

## The coverage duty

A tenth propagation duty runs on a plan. For each spec the plan's
`spec:` names:

1. Read the spec's `decisions:` field. Absent, report `not checked`
   (see *The report*) and stop for that spec. Present with any value
   other than `registered`, report a hit and `not counted`, and stop.
2. Check the register is well formed. Each of these is a hit: the field
   set with no `## Decisions` section; an identity paragraph that does
   not parse; a duplicate identifier; an unknown state token; a group
   carrying a state token; a `replaced by` naming a
   missing identifier, its own, or closing a cycle. Where any of them
   fires, the counted set cannot be trusted: report `not counted` and
   stop for that spec.
3. Collect the counted set: the leaf identifiers that are not
   withdrawn, less those the audited plan's `**Defers:**` lines name.
   The `**Defers:**` lines are checked as *Deferral* says, and the
   `**Follows:**` lines as *Sequential plans* says; identifiers a
   predecessor realized count as cited, from that predecessor.
4. Collect every identifier the plan's `**Realizes:**` annotations
   cite, on tasks and constraint entries. A cited withdrawn identifier
   and a cited group are hits, and so is a cited identifier the
   register does not define. That last is an error in the plan, never
   a gap in the spec: identifiers are minted only in the register, so a
   plan citing one the register lacks has mistyped or invented it.
   Duty 5 does not take it, since duty 5 reads an undefined name as a
   gap in its source.
5. Report every counted identifier that no task and no constraint
   cites: one hit per identifier.

The coverage list is derived, never tallied. The auditor writes the map
from identifier to citing sites, and the fraction is that map's summary;
a bare count would pass one omission offset by one duplicate. A task
carrying no `**Realizes:**` line in a plan the convention binds is a
hit. An identifier cited by several tasks is legal — one decision, many
tasks — and a task split or merged in a fix wave passes as long as the
union of its identifiers survives.

On a registered design spec audited on its own — the gate before its
architect round — the duty runs steps 1 and 2 alone, so a malformed
register is found before any plan depends on it.

The duty proves that every *declared* decision has an owner. Whether
the register faithfully lists the spec's decisions is judgment, and
belongs to the integrity auditor (see *Readers*).

## Table closure

An eleventh propagation duty, independent of coverage. It answers "does
the named element exist?", where coverage answers "does every required
element have an owner?" — correct references can coexist with a missed
decision, so neither subsumes the other. Measured on 2026-09-16: walked
duty by duty, none of the nine current duties checks referential
integrity between two tables of one document.

The duty checks declared relations only, never guessed ones. Matching
cell values would be a false detector: two unrelated columns can share
names by chance, and a relation whose every reference is wrong would
match nothing and go unseen. The relation is declared by the rule that
defines the table's columns, which is also the rule that closes them,
so the auditor knows the relation before it compares a single cell and
no document needs an annotation of its own. The technical-design rule
declares the first ones:

| column | names rows of |
|---|---|
| Contracts `producer → consumer`, each side | Parts `part` |
| State `written by` | Parts `part` |
| State `read by` | Parts `part` |

A declaration says how its cells split: a cell may name several rows,
comma-separated, and `producer → consumer` splits at the arrow before
it splits at commas. It says which values are not references: a party
outside the system is written `external: <name>` and is not resolved.
An empty cell, or one naming nothing, is a hit in all three relations
above, since the rule's own definitions give every contract a consumer
and every state record a writer and a reader. A later declaration that
admits an empty side says so itself. Every other name resolves to
exactly one row of the named table: a name matching no row is a hit,
and so is a name matching several, since a duplicated key makes every
reference to it ambiguous.

The declarations have one home, the rule that defines the tables, under
a fixed heading in the shape of the table above. The auditor's card
names that heading and repeats none of it; the rule loads when the
auditor reads a technical design, which is the only document these
relations bind. A project whose rules declare nothing gives the duty
nothing to cover, and it says so.

A table no rule declares a relation for is not checked by this duty,
and nothing says it was: the report states what the duty covers, and a
document's ad-hoc tables are outside it. So is a Contracts flow written
as a numbered sequence rather than a table row: the rule gives the
sequence no grammar a parse could split, so its steps are not
references this duty resolves, and the declaration says so.

## The report

The auditor's report today is either located hits or exactly two lines,
`model:` and `CLEAN`, with nothing after the token. Coverage adds a
block per spec the audited plan names, written after the hits and
before the token, and present whether or not any hit fired:

    decision-coverage: <spec path> 7/8 covered; deferred [D6]; uncovered [D4.2]
      D1 → Task 2
      D3 → Task 4, Task 6
      D9 → Global Constraints: No code
      …
    decision-coverage: <spec path> not counted — malformed register
    decision-coverage: <spec path> not checked — no decision register

The summary line opens the block, and under a counted spec the map
follows it, one indented line per counted identifier, naming every task
and constraint that cites it; an uncovered identifier maps to nothing
and is also a hit above. The map is what the fraction summarises, so a
reader can check the one against the other. The fraction's denominator
is the counted set of step 3; identifiers the audited plan defers are
listed apart and never counted as covered. `not counted`
follows a malformed register, whose hits stand above it, and carries no
map, since its denominator cannot be derived.

A clean audit of a plan therefore runs to the self-report, one block
per spec, and `CLEAN`. `CLEAN` means no hit in the checks that ran,
and a `not checked` line bounds that guarantee in the report itself, so
a dispatcher never re-reads a spec to learn what the audit covered.

The contract changes in two places edited together: the card's
sentence "a clean audit runs to exactly two lines", and the workflow
rule's paragraph saying a report's body governs, never its closing
token — which gains that a `decision-coverage:` line is neither a hit
nor a violation of the token's position.

The name differs from the integrity auditor's `coverage:` line on
purpose: that line reports how much of a document the audit read, and
two report lines sharing one token for two facts would invite a
dispatcher to read one as the other.

## Disposing of a coverage hit

The detection is mechanical and runs where the measured failure slipped
through: at the gate, on the cheapest family, before the plan-adversary.
The fix is not always mechanical. "Handle retries" does not settle the
limit or the idempotency a task realizing it must state, so writing the
missing task can require a decision nobody has made. A coverage hit
therefore stays a hit — located, ungraded, never a finding — and the
dispatcher classifies its fix by license:

- **(a)** A task already does the work and lacks only its annotation.
  The task's text licenses adding the identifier; the session fixes it.
- **(b)** No task realizes the decision, and the decision's text
  settles every choice writing that task requires. The decision
  licenses the new task; the session writes it, and the next round's
  brief names it among the previous wave's fixes, which the round
  attacks first.
- **(c)** Writing the task needs a choice the decision does not make.
  The question is that missing decision — not the coverage gap, which
  is already established. The hit is held for the developer.

A held hit blocks the dispatch its gate guards, as a held finding
already blocks a fresh round. The answer lands where the decision
belongs: in the spec as a new or a sharpened register entry, or as the
entry's `withdrawn` token where the developer drops the decision; in
the plan as a `**Defers:**` line where the developer defers it. The
plan is then fixed and the gate re-run, and the plan-adversary
dispatches only once the gate passes.

The workflow rule's "hits never wait for the developer" gains one named
exception, for coverage hits alone. Every other hit keeps a fix
licensed by its own derivation.

## Gate lines for a held hit

The lifecycle rule's two gate-line shapes gain a third, and three
terminal rewrites of it:

    - hit held <date> — <the hit's claim>; question: <the missing decision>; options: <the options, with the session's recommendation>
    - hit fixed <date> — <the hit's claim>; <what changed>; ruling: <date>
    - hit deferred <date> — <the hit's claim>; ruling: <date>; Defers: <id>
    - hit withdrawn <date> — <the hit's claim>; ruling: <date>; <spec path>#<id>

A `hit held` line is rewritten in place to one of the three terminal
shapes, so the state always has one home. The rewrite happens after the
gate re-runs over the changed spec and plan, never on the developer's
answer alone. `hit fixed … ruling:` records that the developer settled
the missing decision and the plan now realizes it. `hit deferred`
records an approved deferral, now a `**Defers:**` line in the plan, and
`hit withdrawn` a decision the
developer dropped, its register entry now a tombstone. Neither is
`hit dismissed`, because the gap was real when the hit fired. The
ordinary `hit fixed` shape, without `ruling:`, stays as it is for every
hit whose fix its derivation licensed.

`ruling:` on a gate line means what it means on a disposition line: the
developer decided. A diff-scoped round treats such a line as settled,
as it treats any line carrying `ruling:`.

Placement follows the existing rule, with one exception. A gate after a
round writes its lines under that round's heading. A gate before a
plan's first round has no heading to write under, and the existing rule
makes its lines wait for that round's stamp — which a held hit cannot
do, since the round it waits for cannot start. A pre-round gate
episode that holds at least one hit therefore writes every one of its
lines — the `hit held` line and its siblings alike — in the
`## Review rounds` section before the first round heading, and they
stay there, rewrites included: no round produced them, and one episode
keeps one home. A pre-round episode that holds nothing keeps the
existing rule.

`hit held` joins the Unfinished-work list by widening the *Unfinished
review-loop ledger* entry's command to match it, within that entry's
existing scope — inside a `## Review rounds` section, where the
pre-round line also sits. Its owner is the developer, as for any `held`
line. The three terminal shapes stop matching, which is their closed
state.

## Readers

Each check has one owner:

| check | owner | kind |
|---|---|---|
| every cited identifier exists | propagation auditor, coverage duty (new) | mechanical |
| every counted identifier is cited; the register is well formed | propagation auditor, coverage duty (new) | mechanical |
| a column naming rows of another table resolves | propagation auditor, table-closure duty (new) | mechanical |
| the sites citing a decision realize it in full together; a cited constraint binds | plan-adversary, new dimension | judgment |
| the register lists every decision in the spec that needs realization | integrity auditor, lens 1 (existing) | judgment |
| a technical design's parts are covered by tasks | plan-adversary, dimension 5 (unchanged) | judgment |

The plan-adversary's new dimension sits beside dimension 5. It reads
the annotations in the plan itself, never the auditor's report, which
reaches the dispatcher rather than the adversary; the gate has already
established that every counted identifier is cited. The unit it judges
is the decision, never the single site: one decision split across
several tasks is legal, so the question is whether all the tasks and
constraints citing it realize it in full together. A decision they
realize only in part — six rows of eight — is an Important finding with
`origin` naming the plan. The plan's own deferrals are judged as
*Deferral* says.

The integrity auditor needs no new lens. Its first lens verifies every
rule a document declares about itself, in both directions, and a
registered spec declares one (see *Who writes the register*): each entry
rests on the spec's text, and each decision in the text that needs
realization has an entry. A rejected alternative without an entry is
therefore no defect.
One sentence in the card names the register as such a declared rule. A
decision left only in a paragraph is then a defect the audit proves with
two quotes, at the consumption gate, right before plan-writing.

The architect gains nothing. A decision missing from the register is an
integrity-class defect, which the architect persona already hands to
the integrity audit; a second owner would duplicate that check at the
most expensive tier.

## The author's checklist

`propagation-duties.md` keys the duties by the edit an author has just
made, and gains three things:

- a row for the coverage duty — *added, changed or withdrawn a register
  entry, or added, split, merged, deferred or followed in a plan* → the
  register against every `**Realizes:**` annotation, `**Defers:**` line
  and `**Follows:**` predecessor;
- a row for the table-closure duty — *written a column naming rows of
  another table* → every name against that table;
- the third anchor case the duty-2 row omits, which the card states:
  "one an earlier task in the same document has already rewritten".

The rule's counters — "nine duties, keyed by the ten edits" — are
recounted as part of the same edit.

## Legacy specs

A spec without the `decisions:` field is legacy: the audit reports
`decision-coverage: … not checked` for it and raises no hit. A field
carrying any other value than `registered` is not legacy but a
malformed register (see *The coverage duty*). A plan descending from
legacy specs alone carries no `**Realizes:**` lines. An existing spec
migrates when it is next substantively revised, never in a sweep;
its plan then meets coverage hits at its next gate.

`not checked` is visible in every report, but nothing forces a new spec
to set the field. A project-level statement that the convention is
adopted — under which a new spec without a register would be a hit —
needs a durable home for a project's standing process answers, and none
exists yet. Until that home exists, the field is expected in every new
design spec and its absence is reported, not refused.

## Out of scope

- The technical design's side of coverage — a Scope table mapping
  decisions to parts, contracts or state. It needs row keys the
  Contracts table and the Failure section do not have, and no measured
  failure calls for it yet. Dimension 5 stays as it is.
- Enforcing the register project-wide (see *Legacy specs*).
- A shape for a hit left outstanding when the gate's re-dispatch bound
  stops an episode. The lifecycle rule names that gap already; `hit
  held` is scoped to coverage hits by D12 and does not close it. The
  two share a shape but not a question: a held coverage hit waits on a
  decision the spec lacks, while an outstanding hit marks a gate that
  failed to converge, and folding the second in would widen D12's
  exception beyond the case it was argued for.
- Migrating this repository's existing specs.

## Changes by file

All under `plugins/working-process/` unless noted.

- `agents/propagation-auditor.md` — duties 10 (coverage) and 11 (table
  closure, naming the rule heading that holds the declarations); the
  `decision-coverage:` output line; the "exactly two lines" sentence;
  the coverage exception in *What becomes of your hits*.
- `agents/plan-adversary.md` — the realization-site dimension.
- `agents/integrity-auditor.md` — one sentence naming the register as a
  declared rule for lens 1.
- `rules/spec-plan-lifecycle.md` — the `decisions:` field in the
  frontmatter contract; the register's grammar, states and declared
  rule; the revised template sentence; the `**Realizes:**`,
  `**Defers:**` and `**Follows:**` annotations; the four gate-line
  shapes and the
  pre-round placement; the widened *Unfinished review-loop ledger*
  command.
- `rules/technical-design.md` — the declared relations of *Table
  closure*, under one fixed heading: which columns name rows of Parts,
  how their cells split, the `external:` value, and that a numbered
  sequence is outside the relation.
- `rules/workflow.md` — the coverage exception to "hits never wait";
  the `decision-coverage:` line beside the closing-token paragraph; in
  step 4, the duty of a brief delegating plan-writing to name the
  lifecycle rule and require reading it.
- `rules/propagation-duties.md` — the rows and counters of *The
  author's checklist*.
- `skills/grilling-session/SKILL.md` — updating the register as
  decisions land.
- `docs/domain/glossary.md` (repo) — applied at the grilling of
  2026-09-25: new **Decision register** and **Decision coverage**
  entries; **Ruling** widened to held hits and register state changes;
  **Hit** gained the held coverage hit. Amended by the review rounds:
  **Ruling** also covers a plan's deferral, and **Decision coverage**
  counts deferrals by the audited plan and citations inherited from an
  implemented predecessor.
- `README.md`, `CHANGELOG.md` — the new duties and the convention.

## Open questions

None at the time of writing.

## Review rounds

### 2026-09-25 — architect, fable 5.1, blocking (round 1, full-document)

- fixed 2026-09-25 — [Important] F1: the deferral lives in the spec, against the token's own meaning and the pointer direction; ruling: 2026-09-25; option (b) — the deferral moved to the plan as a `**Defers:**` line (D18, new section *Deferral*), the spec keeping `withdrawn` as its only state token (D5, *Entry states*), counted set in step 3, `hit deferred` and the glossary's **Decision coverage** and **Ruling** updated; a plan both deferring and realizing one identifier is a hit
- fixed 2026-09-25 — [Important] F2: the table-closure duty names no detector; ruling: 2026-09-25; deviation: *Table closure* — none of the offered options: relations are declared by the rule that defines the table's columns (the technical-design rule: Contracts and State columns → Parts), with cell splitting, `external:` and `—` values, and a duplicated key as a hit; value matching refused as a false detector; the unsupported task-to-part claim deleted; `rules/technical-design.md` added to *Changes by file*
- fixed 2026-09-25 — [Important] F3: an undefined cited identifier goes to duty 5, whose disposition treats it as a gap in the spec; license: *The register* (identifiers are the register's literal tokens, so none is minted elsewhere) and the propagation-auditor card's duty 5 ("a gap in the source, not a plan error"); step 4 of *The coverage duty* now reports it as a plan error of the coverage duty, and the *Readers* table's first row names that duty
- fixed 2026-09-25 — [Minor] F4: adding `decisions` to the Misplaced stamp command contradicts the glossary's definition of that term; license: glossary **Misplaced stamp** ("a process field … where the stamping steps put it"); the addition is dropped from *Changes by file*
- fixed 2026-09-25 — [Minor] F5: D2's "one sentence" has no reader; license: *The register*'s identity-paragraph grammar; D2 and *The register* now say "a short statement" and that the grammar enforces the paragraph's shape, not a sentence count
- fixed 2026-09-25 — [Minor] F6: a pre-round gate episode's lines land in two homes; license: *Gate lines for a held hit* ("no round produced it"); a pre-round episode holding a hit now writes all its lines before the first round heading
- fixed 2026-09-25 — [Minor] F7: the re-dispatch-bound hit shares `hit held`'s shape and the spec does not say why it stays out; license: D12 (the exception covers coverage hits alone); *Out of scope* now gives the reason
- fixed 2026-09-25 — [Minor] F8: two grammars carry one fact; ruling: 2026-09-25; option (a) — a constraint entry opens with `**Realizes:** D9` as its first clause, one shape for both sites
- signal 2026-09-25 — another round pays only after F1 is decided; then one diff-scoped round should suffice, and the Minors are worth a fix wave rather than a round of their own

### 2026-09-25 — architect, fable 5.1, concerns (round 2, diff-scoped)

- fixed 2026-09-25 — [Important] F9: a plan taking over from an earlier one gets a coverage hit for every decision the earlier plan already realized; ruling: 2026-09-25; option (c), narrowed to `implemented` predecessors — new D19 and section *Sequential plans*: a `**Follows:**` line names each predecessor of the same spec, the later plan inherits its `**Realizes:**` identifiers and never its deferrals, the map names the source plan, and step 3 counts inherited identifiers as cited; option (b) refused in the section, since two drafts could exempt each other; deviation: *Sequential plans* — the plan-adversary judges the later plan against inherited decisions, not the predecessor's implementation, which it cannot read
- fixed 2026-09-25 — [Minor] F11: no exact place for a `**Defers:**` line; ruling: 2026-09-25; option (a) — the lines close the Global Constraints section and state facts about the whole plan, not the entry above them; `**Follows:**` lines sit beside them
- fixed 2026-09-25 — [Minor] F10: `hit deferred` embeds the whole `**Defers:**` line; license: the `hit withdrawn` shape in *Gate lines for a held hit*, which points by identifier; the shape now ends `Defers: <id>`
- fixed 2026-09-25 — [Minor] F12: `—` is allowed in relations whose definitions exclude an empty side; license: `rules/technical-design.md`'s definitions of contract and state; an empty cell is now a hit in all three relations, and a later declaration admitting one must say so
- fixed 2026-09-25 — [Minor] F13: the cell split does not cover a numbered sequence; license: *Table closure* ("A table no rule declares a relation for is not checked"); a numbered sequence is now stated outside the relation, since the rule gives it no grammar to split
- fixed 2026-09-25 — [Minor] F14: the spec does not say where the auditor reads the declarations; license: D10 (the relation is "declared by the rule that defines the table"); the rule is now their one home under a fixed heading, the card names the heading and repeats nothing, and *Changes by file* says so
- signal 2026-09-25 — another round pays only after F9 is decided; the Minors are one fix wave, and if one realizing plan per spec is chosen an integrity audit may replace the round

### 2026-09-26 — architect, fable 5.1, concerns (round 3, diff-scoped)

- held — [Minor] F18: the `**Defers:**` and `**Follows:**` lines closing Global Constraints fall under the template's "Every task's requirements implicitly include this section"; counter: re-raises the F11 line carrying `ruling: 2026-09-25` with new evidence — round 2 cited only the section heading, not that sentence; question: add a clause exempting both kinds of line from that implicit inclusion, keeping the placement?; options: (a) yes — one clause in the revised template sentence (D8, *The plan's annotations*); (b) move both kinds of line into a block of their own after Global Constraints instead — recommended: (a), placement stays as ruled
- fixed 2026-09-26 — [Minor] F15: inheritance does not say whether it is transitive; license: *Sequential plans* ("and nothing else"); a predecessor's `**Follows:**` lines are now stated as not inherited, so a plan names every predecessor it relies on
- fixed 2026-09-26 — [Minor] F16: "what it realized is settled" claims more than a frozen body gives; license: `rules/spec-plan-lifecycle.md` (an implemented document "is the archive, not the specification of what stands today"); the sentence now rests on what the predecessor cited, and whether the realization still stands is sent to the lifecycle rule's diff
- fixed 2026-09-26 — [Minor] F17: the glossary's **Decision coverage** ignores inherited citations; license: D19; the entry now covers citations in an implemented predecessor, and *Changes by file* records the review-round amendments to the glossary
- fixed 2026-09-26 — [Minor] F19: a multi-spec plan gets a false "plan of another spec" hit in the pass for a spec its predecessor does not name; license: step 3 of *The coverage duty*, which runs per spec; a predecessor now shares at least one spec, lends identifiers only for shared specs, and is out of scope in the other passes
- signal 2026-09-26 — another round does not pay; the five Minors are one fix wave, and an integrity audit at the consumption gate — especially the two integrity-class questions the round named — is worth more than a fourth round
