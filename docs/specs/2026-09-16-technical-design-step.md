---
ticket: none
date: 2026-09-16
status: draft
grilled: 2026-09-16
architect: concerns (resolved 2026-09-16)
integrity: 2026-09-17 (sha: 171b93f)
branch: feature/technical-design-step
base: develop
---

# Technical design — a third document between spec and plan

A plan that designs the code and orders the work designs it badly. This
spec adds a third document class between the spec and the plan: a
**technical design**, answering what the thing is made of. The plugin
ships the contract; projects with code consume it.

## Why

Where no document names the structure, the plan becomes the place it is
decided. A plan that designs the code and orders the work at once locks
decomposition into task order: tasks arrive as feature slices, each one
appended to whatever file the previous slice touched, and nothing states
where a new responsibility belongs. Implementers working from a fresh
context cannot see their siblings, so they reproduce each other's local
rules. The structure that results is nobody's decision — it is the
residue of the order in which work happened to be scheduled, and it is
paid for after implementation, by whoever reads the code next.

Neither existing document holds that decision whole. The architect
persona already reviews boundaries, interfaces and alternatives, so
structure is reviewed — but it is reviewed scattered through a body
written about behaviour, where no reader sees the division at once and
the spec's stamp quietly covers more than it was written to certify. A
plan that carries the decision instead becomes a codebase without a
compiler: prose prescribing names and interfaces that nothing checks
until implementation contradicts them.

The failure is observable before it is expensive. Its tell is a project
whose specs name code identifiers scattered through prose while no
document lists them in one place, and whose plans map tasks to features
rather than to parts.

## The document

A technical design answers **what the thing is made of**, as the spec
answers what and why, and the plan answers in what order and verified
how. It lives in `docs/technical-designs/`, suffix
`-technical-design.md`.

The boundary that separates it from the spec is not files against
non-files. It runs between **identity** and **placement**: the spec
names parts by the name their consumers use and gives each one a
responsibility; the technical design decides what naming a part leaves
open — where it sits, what shape the contract on its border takes, who
writes it and who reads it, what is state and where it is
authoritative. Where naming a part fixes its location, the name is the
path and the spec carries it.

This repo ships that contract and does not execute it. Its own product
is prose, where a part's name is its path and behaviour is already the
shape of the contract, so a technical design here would duplicate two
existing documents. The consumers are projects with code. Their
vocabulary comes from any skill available in the session, whatever
published it — a standards plugin, or the project's own skills
directory. Where no such skill covers the technology, the document is
written from generic knowledge, best effort; that degradation path is
what makes the contract self-sufficient.

## When it fires

Repository markers govern by default; a declaration overrides them in
both directions.

| state | behaviour |
|---|---|
| a declaration the project records | binds, no question asked |
| no declaration, but the repository carries a toolchain manifest | the offer fires at every consumption gate; nothing is written |
| no declaration, no marker | no offer |

A marker is a file a language or platform toolchain reads to build, test
or deploy the repository — the file a developer would point at to say
what kind of project this is. The core defines that test and names no
closed list; a domain's own skill may name the markers of its
technology.

A marker proves the repository holds code, never that a given change
needs decomposing, so narrowing the test to exclude a repository that
finds the offer unhelpful would buy the exclusion with a worse test.
The declaration is the signal and it outranks the marker; the marker only
raises the question. This repository is a case in point: its product is
prose, and `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
and its CI workflows are files a platform reads to deploy it, so the
offer reaches it and it declines by declaration. Until the declaration
has a surface, that decline has nowhere to live and the offer stands —
which is the deferral below, made visible rather than argued away.

Where the declaration lives is deferred. This spec fixes only what it
must do: a project states the answer once, the statement binds without
being re-asked, and a session can read it without being told where to
look. The surface itself belongs to the wider question of where a
project's standing process answers live — a `CLAUDE.md` note, or a file
it points at, is the shape available today and the one an implementation
may assume until that question is settled.

The offer reads *open the `system-designer-session` skill and write the
technical design?* — never *dispatch*, which in this plugin names a
background agent — rather than *does the Parts section suffice?*: a
project that
has not been writing structural sections has none to compute from, so a
trigger derived from one would first have to force the section it then
measures. A session may **propose** writing the declaration and never
writes it unasked.

When the offer is accepted, the **integrity audit waits** for the
document's dispositions to reach the spec: an audit is a fresh read of a
settled spec, and decomposition is the last step that can unsettle one.
This is the only ordering the gate has: the glossary's Consumption gate
entry names five things due there and fixes the order of this one pair
alone, leaving the rest unordered as they were.

## Author and reviewer

The author is the **`system-designer-session` skill**, in the main
thread. The
reviewer is the `architect` agent, whose card already admits "any design
document dispatched standalone", with the propagation audit gating the
dispatch as it gates every verdict dispatch. The plan-adversary stays on
plans.

## Section skeleton

| # | section | status | content |
|---|---|---|---|
| 1 | Scope | required | which spec and which of its behaviours this structure realizes; the system boundary |
| 2 | Parts | required | `part \| kind \| change \| placement \| owns \| deliberately excludes`; a retirement is a `change: retired` row |
| 3 | Contracts | required | `producer → consumer \| crosses \| guarantee \| breaks when \| check`; a flow crossing three or more parts in fixed order becomes a numbered sequence |
| 4 | State | conditional | `record \| home \| written by \| read by \| lifecycle \| visible through` |
| 5 | Failure and repetition | conditional | what happens when a step does not finish, runs twice, runs beside another, or finds the other side absent |
| 6 | Cuts not taken | conditional | one line per rejected division and its reason — the material the architect grades |
| 7–8 | Open questions, Review rounds | from the lifecycle rule | as a spec and a plan carry them today |

Three sections are required because only those three are never empty,
on prose or on code. A conditional section that is absent is named in
one line — "not applicable, because…" — which the system-designer
persona already requires of itself.

`placement` names where a part belongs in the system's structure — its
layer, module, package, service, or path, at the level the design
decision needs. `kind` answers what a part is; `placement` answers where
it belongs, and the two coincide only where a domain convention derives
one from the other. Record the location even then: a cell reading
`rules/` says the convention was applied deliberately, while an empty
one cannot be told apart from an omission. The table in this spec keeps
five columns — a design spec names identity, and placement is the
technical design's business.

`tests` is not a section: it returns as the contract's `check` column.
The document says **what** verifies a contract, the plan says **when**
that runs. What leaves the plan is the interface prescription its tasks
carry today in their `**Interfaces:**` blocks.

The plan-adversary's coverage dimension reads the `change` column: the
plan must cover every part marked `new`, `changed` or `retired`; one
part may span several tasks and one task several parts. A part carried
as `unchanged` context needs none. The column's values are
`new | changed | retired | unchanged` and the set is closed to domains —
it steers the process, so its meaning belongs to the core. A value
outside the set is an error the author corrects, never a part that
quietly escapes the coverage check.

Its `origin` field becomes a list of named documents — `design-spec`,
`technical-design`, `implementation-plan` — and `both` retires with it.
The triage clause in `workflow.md` that reads the field retires `both`
with it, and its hold widens: a finding originating in *either* judged
document is held unless a written decision licenses the edit, since
changing a technical design from inside a plan review is as much a
design decision as changing a design spec. Each holds against its own
document's ledger, by the cross-document clause the lifecycle rule
already defines.
Today `both` means the plan and the spec, unambiguously because there
are two documents; with three it stops saying which two, and triage
branches on that value. A list answers the question triage actually
asks — is any origin the design spec, since editing one from inside a
plan review is design work — and it takes a new document class without a
new decision, where explicit pairs would grow by the square.

A part has a resolvable identity, an explicit responsibility with its
exclusions, and a contract that lets its implementation change without
changing its consumers. What earns a part its own row is a design
decision: list it separately when leaving it out would make an
implementer decide a responsibility boundary, a contract between parts,
or the ownership of state, and keep inside a part the details that
merely carry out decisions already made. A public method is usually a
row in its part's contracts rather than a part of its own.

Task boundaries never define part boundaries — the plan is organised
around the structure, not the structure around the plan. The grain comes
from the decisions the document exists to settle, which is the same
question the integrity audit asks of a spec: what would this text leave
an implementer to decide? It comes neither from the plan nor from a
domain vocabulary, which a project may not have.

A contract is what a consumer may rely on without reading the producer's
body. Part and contract are two questions about one thing rather than
competing labels: a file may be a part, its signature a contract, and
the record it writes state. State is a record that outlives one
interaction and is read by a later one, with a home, a writer, a reader
and an end.

## Domain extension

The author takes the part vocabulary — kinds of part, placement rules,
kinds of contract, homes of state — from the **Domain expertise** duty
the personas already carry, which has them scan and load the domain's
skills. No new discovery convention ships with this change.

A kind of part that no domain skill names is recorded in the document as
a **vocabulary gap** — a term this change mints, kept apart from the
review cascade's candidate gap, which is a graded and counted finding
with a reviewer for its producer. Accumulated vocabulary gaps are either
the specification of a `<domain>-technical-design` skill or the evidence
that none is needed; the decision is then made on evidence rather than
remembered.

The core closes the three definitions, the table columns, the contract
entry's fields, and the four questions of the failure section. A domain
adds rows and values — outside the closed `change` column — never
columns, and never redefines what qualifies:
a kind of part it names must still have a resolvable identity, an
explicit responsibility, and a contract its implementation can change
behind.

## The class and its three cards

The lifecycle rule branches between documents in several places, and
every branch is really about the class rather than the filename. The
glossary mints **judged document** for the class a design spec and a
technical design share, against an implementation plan, and ADR 0004
records why the class decides what a document owes.

The class is deliberately not called a design document, the phrase three
agent cards use today, because both members carry "design" in their
names and the phrase would read as one of them rather than as both. All
three cards move to the minted term in the same change:

> `plan-adversary`, today "Handed a spec (a design document, not an
> implementation plan)?" — reads "Handed a judged document (a design
> spec or a technical design, not an implementation plan)?", and the
> phrase later in the same section, "to a design document and would
> misfire as findings", takes the same term.

> `architect`, today "a grilled spec (primary target) or any design
> document dispatched standalone" — reads "a grilled design spec
> (primary target) or any judged document dispatched standalone"

> `integrity-auditor`, whose description opens "Judgment audit of a
> churned design document" — takes the minted term there too.

The plugin README paraphrases the architect's card and carries the same
phrase, so it moves with them: five occurrences in four files, which is
the whole of the shipped text using the retired name.

## What the integrity audit reads

The auditor reads a spec as the whole basis an implementer builds from.
Once a spec defers structure to a technical design, that basis is two
documents, and a check of one against a remembered copy of the other has
no place to stop: an audit's dispositions edit both, each edit unsettles
the other's record, and the document that produced the change is the one
the spec calls its last producer of changes.

So the pair is audited as one target. Before plan-writing, a single
integrity audit reads the design spec and its technical design whole,
and judges three things: each document against itself, the two against
each other, and whether the pair together suffices for an implementer.
It may report defects in either. Its card carries the four cases
explicitly:

> A design spec with no technical design is a single target. A design
> spec that names one is audited together with it, both documents the
> target and neither the other's context. A plan, a permitted target on
> request, is the target alone and reads the documents its `spec:` and
> `technical-design:` name as context. A technical design is never a
> target alone: its audit is its design spec's. No other field carries
> context;
> `revises:` names a document whose design no longer matches what
> shipped, and reading an archive as authority is how a stale claim
> re-enters a live one.

Its second lens, which today reads "has no other context: no
conversation, no author to ask", is narrowed to match:

> Read the document again as a careful implementer who must build from
> this text, the documents audited with it, and the documents its
> `spec:` and `technical-design:` name, and has no other context: no
> conversation, no author to ask.

A third edit follows from the first: the card's coverage tell reports
one line count and one highest line cited, which is how a partial read
exposes itself. A pair has two documents to read partially, so the tell
reports a pair of numbers per document. Without it the one risk peculiar
to a joint target — one document read whole, the other skimmed — is the
one thing the tell cannot show.

These edits land together — any one alone leaves the card contradicting
itself, which is the defect class this auditor hunts.

One stamp records the pair. It lives on the design spec, names both
documents and both body hashes, and the technical design carries no
`integrity:` of its own. That is not the design shedding a ceremony: it
owes the check like any judged document and discharges it jointly, which
ADR 0004's principle allows, since the class decides what a document
owes and not how many dispatches discharge it.

    integrity: 2026-09-16 (sha: abc1234; with: x-technical-design.md@def5678)

Changing either document unsettles the pair, and the gate recomputes
both hashes to see it. The two pointers are what identify the pair, so
an added, removed or repointed `technical-design:` unsettles it too.

**Ending the check.** The stamp lands as it does today, once the audit's
dispositions are applied, and this change asks for no confirming read
before it. Merging the pair into one target already removed the loop
that made one seem necessary: with a single stamp there is no second one
to invalidate, and the risk that dispositions leave text nobody re-read
is the risk every audited spec already carries. A declined offer behaves
as a declined offer does today, and this spec changes nothing about it.

**One offer, and what it discharges.** The pair earns one offer at the
gate rather than one per document. Both documents keep their own chain
debt from a diff-scoped round, and the pair audit may discharge both at
once; the record says which debts it discharged, so the design's missing
stamp never reads as an outstanding one and never draws a second offer
for a check already done. The other arm stays per-document: a
full-document architect round discharges the debt of the document it
read.

## The term

With two judged documents in the process, the bare word *spec* stops
saying which one a sentence means, and the `origin` values are where the
three documents first stand side by side. The glossary mints **design
spec** as the name, with *spec* recorded as its short form, so the new
surfaces this change writes — the `origin` values, the technical-design
rule, ADR 0004 — carry the full name from their first line, and existing
sentences take it as they are touched.

The frontmatter field keeps its name. `spec:` is read by plans, by the
lifecycle rule and by the Unfinished-work commands, which grep the
literal string; renaming a field others rely on is a propagation event
with its own audit, and it buys nothing this change needs.

## Parts and boundaries

| part | kind | change | owns | deliberately excludes |
|---|---|---|---|---|
| `technical-design.md` rule | path-scoped rule | new | the skeleton, the three definitions, what a technical design must contain | every lifecycle sentence, and the gate that decides the document is written at all |
| `spec-plan-lifecycle.md` | path-scoped rule | changed | `paths:` covering the new directory; the class name at each branch point; the new pointer's meaning, optionality and cardinality; `spec:` widening from plans to technical designs; the stamp's grammar and when it is stale against the pair it names; the gate's one fixed ordering and its single batch; the design's `status` moving with the plan's | the skeleton |
| `propagation-duties.md` | path-scoped rule | changed | `paths:` covering the new directory; the author's duty to check both pointers resolve and name each other | — |
| `process-artifacts.md` | always-on rule | changed | `docs/technical-designs/` among the Process directories | — |
| `ticket-frontmatter.md` | path-scoped rule | changed | the new directory's field set, which its per-directory list would otherwise cut to `ticket` + `date` | — |
| `process-status` skill | skill | changed | the directories its status pass covers | the commands themselves, which the lifecycle rule publishes |
| `workflow.md` | always-on rule | changed | the step's position, the gate's offer and what fires it, the authoring step that writes both pointers, and the triage clause that reads `origin` | the document's contents |
| `propagation-auditor` card | agent card | changed | the document class it audits, today "a spec or plan"; the pointer pair among what it checks | — |
| `integrity-auditor` card | agent card | changed | which documents are its target in each case, what it may read as context, the second lens's premise, and the coverage tell's shape for a joint target | which gaps are structural |
| `plan-adversary` card | agent card | changed | `origin` as a list of named documents; the coverage dimension | the document's contents |
| glossary | reference document | changed | `Part`, `Contract`, `Technical design`, `Judged document`, `Design spec`, `Vocabulary gap`, `Origin` rewritten as a list of named documents, and the `Consumption gate` entry's count and ordering | — |
| `architect` card | agent card | changed | the class name in what it accepts | its duties |
| ADR 0004 | reference document | new | why a class owes the ceremonies it owes | the ceremonies themselves |
| plugin README | reference document | changed | the class name where it paraphrases the architect's card; the `integrity:` value shape in the field table | the two pointer fields, which are not stamped |

The new rule is path-scoped so the skeleton loads only while a technical
design is open — which is why it cannot own the offer that decides a
design gets written. That offer fires at a consumption gate, before any
such document exists and with the new rule therefore unloaded, so the
always-on `workflow.md` owns the trigger, the offer and the step; the
session reads the path-scoped rule once the offer is accepted and it
sits down to write. The new rule carries no lifecycle sentence either:
the lifecycle rule loads beside it through its own `paths:`, and a
second home for one fact is how the two drift.

Frontmatter carries the chain: `spec:` on the technical design and
`technical-design:` on the plan, both pointing back at the document they
descend from, as every pointer in this process does today.

The design spec gains a `technical-design:` pointer of its own, and that
one is new in kind: it names a document written later. The existing
pointers record where a document came from; this one gives a reader
holding the spec the structure that develops it, which is the move
anyone makes who sits down to plan, to review, or to change the thing a
month later. Without it the only answer is to search the designs for the
one naming this spec.

Five rules keep the pair honest. The field is optional and appears once
the technical design exists, so its absence means there is none rather
than one nobody linked. The author who creates the design writes both
ends in the same turn — the design's `spec:` and the spec's
`technical-design:`. The propagation audit checks that both targets
exist and that the two pointers name each other. A plan keeps its own
`spec:` and `technical-design:`, and where it carries both, they must
agree with the pair. One technical design per design spec, until
something measured asks for more.

Neither pointer joins the README's field table, which holds stamped
fields only — but `integrity:` is in that table, so its entry carries
the extended value shape.

The pointer also opens a hole the body hash cannot see. `integrity:`
certifies the body below the frontmatter, so neither adding this field
nor editing the technical design moves the design spec's hash — yet both
change the basis its audit was given. The pair audit closes that hole;
the section on what the integrity audit reads carries the mechanism.

## Lifecycle

A technical design is a **judged document**, the class a design spec
already belongs to, against an implementation plan. It is not grilled:
grilling stress-tests a document's terminology against the project
glossary, and a technical design mints no terminology — its vocabulary
comes from the design spec, which was grilled, and from the domain's
own skills. The names it does mint are part and component names, and
those are checked against the domain's own skills where such a skill is
available — and where none is, the author names the kind, records a
vocabulary gap, and the architect round judges the boundary, which is
what it judges in any case. The lifecycle rule branches
between the two in several places, and the technical design takes the
spec's side of every one: the same fields, the same consumption-gate
semantics for a stale stamp, the same owner for an unresolved verdict,
and the same pair offered against chain debt, which declining
discharges. One mechanism it shares rather than owns: the integrity
check is due on it like any judged document, and one audit of the pair
discharges it, so the `integrity:` stamp sits on the design spec and
names both. ADR 0004 records why the class earns those
ceremonies — its next reader still judges it — so the next document
class answers by naming its reader rather than by renegotiating each
branch.

Two consequences the rule must state rather than imply. The design's own
consumption gate is plan-writing, the same moment as the design spec's,
and one ordering binds the two: writing the design and applying its
review dispositions precedes the joint integrity audit, because the
design is the last producer of changes to the spec and certifying the
spec's body before the design's questions are answered stamps a body
about to change. The dependency reaches no further — the broader reading,
that every item the design owes precedes every item the spec owes, is
too wide for a pair the audit reads as one.

The gate therefore runs in passes. The first pass decides whether a
technical design is written at all; where the offer is accepted, the
gate suspends until the design exists and its review dispositions are
applied, then resumes and collects the questions the documents' current
state raises. Answers already given stay binding unless the basis they
rested on changed. The gate asks its questions in one batch, as a review
round does, rather than firing each offer in turn — a batch being every
question answerable at that pass, never every question the gate will
ever ask. And the
design's `status` reaches `implemented` with the plan's, in the same
turn and by the same hand, since otherwise the rule freezing an
implemented document's body never reaches it.

## What it costs

Accepting a technical design raises the cost of authoring and of review,
and the raise is not spread across the process: it lands on the offer.
Declined, the step costs one question at a gate. Accepted, it adds an
architect loop over the new document; the integrity check stays one
audit, widened to read the pair rather than doubled. Verdicts stay
separate and the integrity check merges — the two operations move
differently, and saying so is what keeps a reader from counting
dispatches and concluding the process doubled.

The tiers matter more than the count. Propagation gates run on the
cheapest available family, so the extra dispatches they add are not a
proportional cost; the architect rounds and the integrity audit run at
the most capable tier, and beside them sits the author's time and the
developer's, one batch of questions per round. What moves the total is
the number of rounds, the size of the documents, and how much a design
sends back to its design spec.

The justification is that structure is settled before implementation
rather than during it, and that the rework implementation would
otherwise force does not happen. That is a hypothesis, not a measured
result: what this change has observed is the symptom of *not* having the
document, never the cost of keeping one. The balance is for validation
to settle.

A change may skip the technical design when it sits inside boundaries
and contracts already settled, and the implementer is left to decide no
new responsibility split, no placement, and no ownership of state — the
same test that decides whether a part earns a row.

Validation on a code project measures both sides: elapsed time, tokens
by model tier, rounds per document, and the interruptions that needed a
developer decision, against the structural decisions still discovered
during implementation and the rework they caused. One project carrying
the document is not a comparison, so the arm it is read against is named
before the measurement starts — a change in the same project that met
the skip criterion above, or that project's own history before the
document existed.

Reviewing the design spec and the technical design as one dispatch would
cut some of this, and is deliberately not proposed here: the two
documents have different subjects, and merging their reviews would
change what a verdict certifies.

## Out of scope

- Renaming existing specs to `-spec.md`: 28 files plus every `spec:` and
  `revises:` pointer, for a disambiguation the new directory already
  provides.
- A background agent authoring the document; a `<domain>-technical-design`
  skill; and the domain half — the kinds of part a technology recognizes
  and where each one belongs — which the domain's own skills carry.

## Known limitations

1. **This repo cannot dogfood the document.** It ships a contract it
   will not execute, which is the same condition under which the
   system-designer persona went a year without a dispatch. Validation
   must run on a code project's spec.
2. **Implementation discoveries have nowhere to land, and this document
   will feel it first.** A document already `implemented` has a frozen
   body, and a discovery that invalidates one of its sentences fits
   neither a supersession pointer nor the ledger, which records review
   dispositions rather than implementation events. That gap predates
   this change and its answer is the same for two documents as for
   three, so this spec does not invent one. It does move the weight:
   what implementation overturns is usually structure — this class must
   split, that boundary sits wrong — so the technical design becomes the
   most frequent casualty of a gap nobody has closed.
3. **The author inherits the spec's blind spot.** A session writes the
   document in the context that already assumed a decomposition, and
   questioning that assumption is the document's purpose. Until a
   fresh-context author exists, the only fresh readings of the document
   are the architect round, the propagation gate, and the integrity
   audit it shares with its design spec.

## Open questions

None outstanding; the decisions above were settled with the developer on
2026-09-16, informed by an architect and a system-designer consultation
whose records live under `.claude/working-process/technical-design-step/`.

## Review rounds

### 2026-09-16 — architect, fable 5.1, blocking (round 1, full-document)

Full-document read. Five Important, four Minor. Record:
`.claude/working-process/technical-design-step/architect-round-1.md`.

Correction, recorded at round 2: the four Minor lines below were written
`fixed` before their edits existed. F6, F7, F8 and F9 landed only after
round 2 found them still open, and they are re-listed in round 2's
dispositions. The lines stand as written so the error is legible.

- fixed 2026-09-16 — [Important] F1: the technical design's Parts
  section carries the same five columns as the design spec's, so the
  identity/placement boundary the spec draws has nowhere to land;
  ruling: 2026-09-16; the technical design's table gains a `placement`
  column, the design spec's keeps five, and the clause parts `kind`
  (what a part is) from `placement` (where it belongs), requiring the
  cell to be filled even where a domain convention derives it.
- fixed 2026-09-16 — [Important] F2: the gate's offer has two owners,
  and the path-scoped rule cannot fire it, loading only while a
  technical design is open while the offer fires before any design
  exists; license: the document's own statement that the new rule is
  path-scoped, read together with `workflow.md` owning the step; the
  trigger, the offer and the step belong to the always-on rule, and the
  path-scoped rule is read once the offer is accepted.
- fixed 2026-09-16 — [Important] F3: the new frontmatter fields and the
  date comparison the gate was to run had no owning row; license:
  applying the ownership the document already declares; field meaning,
  optionality, cardinality and staleness go to the lifecycle rule,
  writing both pointers to the authoring step in `workflow.md`, and
  checking the pair to the propagation auditor and its author-facing
  rule, with the misplaced exclusion returned to its own row.
- fixed 2026-09-16 — [Important] F4: a day-resolution comparison passes
  same-day edits, and in this process whole loops fit inside one day, so
  the mechanism misses its dominant case; ruling: 2026-09-16; the date
  comparison is withdrawn — no precision of dates catches an edit that
  changes a design without opening a round — and the audit stamp records
  the identity and body hash of each document read as context, with the
  gate recomputing both.
- fixed 2026-09-16 — [Important] F5: the design takes the spec's side at
  every branch, so a code project pays two architect loops and two
  top-tier integrity audits per feature, and the spec named neither the
  cost nor why the design's own audit is not redundant; ruling:
  2026-09-16; the cost is recorded rather than argued away, with the
  tier distinction that makes the count misleading, the benefit stated
  as a hypothesis validation must settle, a criterion for skipping the
  document, and what validation measures on both sides. Merging the two
  reviews stays out of scope.
- fixed 2026-09-16 — [Minor] F6: the spec falsifies the glossary's
  Consumption gate entry — a fifth item and one ordering — while saying
  it leaves the entry standing; license: the entry is this change's own
  artifact; the entry is updated.
- fixed 2026-09-16 — [Minor] F7: "session" names a skill, which the
  glossary's Session skill entry bans; license: that `_Avoid_` ban; the
  `system-designer-session` skill is named.
- fixed 2026-09-16 — [Minor] F8: the table omits two dispatched
  consumers of the two-directory enumeration, one of which assigns field
  sets per directory; license: an enumerated missed consumer, decided by
  its own derivation; the rows are added.
- fixed 2026-09-16 — [Minor] F9: "the verified-interfaces table leaving
  the plan" names an artifact no plan convention defines; license: the
  named artifact does not exist; plans carry per-task `**Interfaces:**`
  blocks, and the sentence names those.

- signal 2026-09-16 — the reviewer expects the next round to close on
  `concerns` or `LGTM`, judging the repairs local rather than a
  redesign.

### 2026-09-16 — architect, fable 5.1, blocking (round 2, diff-scoped)

Diff-scoped over round one's fix wave. Two Important, seven Minor.
Record:
`.claude/working-process/technical-design-step/architect-round-2.md`.

- fixed 2026-09-16 — [Important] F10: the three clauses guard the pair
  against invalidation by the stamp, never by the audit's dispositions,
  which on the spec's dominant path re-arm the offer without end;
  ruling: 2026-09-16; the pair is audited as one target.
  One integrity audit before plan-writing reads the design spec and its
  technical design whole, judging each against itself, the two against
  each other, and the pair's sufficiency; one stamp on the design spec
  names both documents and both hashes, and the design carries no
  `integrity:` of its own. The check ends by confirmation — the auditor
  reads what the dispositions changed and what it did to both, and the
  stamp waits for that confirmation — or by a recorded waiver, which
  leaves no current stamp, never refreshes an older one, and closes this
  passage through the gate alone. The pair earns one offer, and the
  record says which debts it discharged. Superseded by this ruling:
  the context-reading clause of round one's B1, and the design's own
  `integrity:` field. What the original finding said, for the record:
  the context record's three clauses guarded against
  invalidation by stamping, which never moved a body hash; what moves it
  is an audit's dispositions, and the spec makes the technical design
  the last producer of changes to its design spec, so the mechanism has
  no terminator on its own main path. The reviewer offers two shapes and
  the choice is the developer's: an offer whose decline is recorded like
  chain debt, or one audit of the pair with no `integrity:` on the
  design. No license for either.
- fixed 2026-09-16 — [Important] F11: the set of context documents, on
  which both the stamp's content and clause 2's "insufficient" depend,
  is not fixed by a closed field list, and the spec calls `revises:` a
  pointer too; license: the lifecycle rule's own definition of
  `revises:`, which names a document whose design no longer matches what
  shipped; context is now the closed pair `spec:` and
  `technical-design:`, with `revises:` excluded in both places.
- fixed 2026-09-16 — [Minor] F12: extending the `integrity:` grammar
  changes a stamped field the README's field table documents, and the
  exclusion was written for pointers; license: an enumerated consumer;
  `integrity:` carries the extended value shape in the field table and
  the exclusion narrows to the two pointers.
- fixed 2026-09-16 — [Minor] F13: the gate's batched questions and the
  design's `status` coupling are lifecycle sentences with no owning
  cell; license: applying the ownership already declared; both join the
  lifecycle rule's row.
- fixed 2026-09-16 — [Minor] F14: validation measures both sides on one
  project that has the document, so the avoided-rework hypothesis has no
  comparison arm, and "what this change has measured" overstates a
  symptom; license: the document's own claim; "measured" became
  "observed", and validation names the arm it is read against.
- fixed 2026-09-16 — [Minor] F15, F16, F17, F18: the four round-one
  Minors, re-raised because their `fixed` lines were written before the
  edits existed; license: the licenses of F7, F6, F8 and F9 in round
  one, unchanged; all four landed for real this time and were verified
  on disk — the skill named rather than "session", the glossary's
  Consumption gate entry at five items with the one fixed ordering, rows
  for `ticket-frontmatter.md` and the `process-status` skill, and the
  interface prescription named as the `**Interfaces:**` blocks that
  exist.

- signal 2026-09-16 — a further round is unearned until the developer
  settles F10, since a round before that choice repeats the finding at
  the most expensive tier; after it, a diff-scoped round three over the
  context-record paragraph should close on `LGTM` or `concerns`.

The propagation gate before round three, under this heading because a
gate mints none of its own:

- hit dismissed 2026-09-16 — five occurrences of "design document" still
  stand in the shipped cards and README, against the prescribed
  replacements; counter: the prescriptions are promises, not landed
  changes. This spec has no plan yet, and editing shipped plugin content
  before one exists would put implementation ahead of the process that
  reviews it. The anchors the edits need all exist, which is what the
  duty checks for a promised change.
- hit fixed 2026-09-16 — the superseded context-record passage survived
  its own replacement, leaving two accounts of one mechanism; the block
  is deleted and the pair audit is the only account.
- hit fixed 2026-09-16 — the stamp's worked example appeared in two
  shapes, `with:` and `context:`; the surviving example is the pair form.
- hit fixed 2026-09-16 — the claim about the glossary's Consumption gate
  entry described the entry as it stood before this change's own edit to
  it.

### 2026-09-16 — architect, fable 5.1, concerns (round 3, diff-scoped)

Diff-scoped over round two's fix wave. The prescribed tier refused the
dispatch on a spend cap, so the round ran on Opus 5, one family below,
and again on Fable 5.1 once the cap reset — the same brief, the same
document byte for byte, no edit between them. Both records stand:
`architect-round-3.md` (Opus 5, `blocking`, four Important and five
Minor) and `architect-round-3-2026-09-16-15-21-40.md` (Fable 5.1,
`concerns`, one Important and six Minor). The stamped verdict is the
prescribed tier's, so no `architect-fallback:` field is owed: the field
records that the stamped verdict was produced below tier, and this one
was not. The below-tier run is recorded here and in its own dispatch
record, and nothing is re-reviewed on its account.

What the two runs shared: the stamping moment, the waiver with no home,
the second lens reopening a closed context set, the missing fourth case,
the duplicated README paragraph, and the judgement that ADR 0004's added
sentence keeps its principle. Opus alone found the coverage tell left
counting one document for a target that had become two. Fable alone
found the retired word "context" surviving in the glossary and the
table, the cost correction contradicting itself two sentences on, and —
the reading that decided the wave — that the confirming read was a
second mechanism for a failure the merge to one target had already
removed.

The two runs number their findings independently and the numbers
collide, so every line below names its run.

- fixed 2026-09-16 — [Important] Fable F19, Opus F19: the confirming
  read is a second mechanism for a failure the merge to one target had
  already removed; ruling: 2026-09-16, variant (a); the confirming read
  is withdrawn, the stamp lands once dispositions are applied as it does
  for every audited document today, and the spec says so rather than
  raising a standard it does not also raise for a lone design spec.
- fixed 2026-09-16 — [Minor] Fable F21, F22 and [Important] Opus F21:
  the card's second lens and its case list reopened a context set the
  merge had closed; license: the card's own closed set and the
  document's own statement that a technical design carries no
  `integrity:`; the second lens repeats the pair, and a technical design
  is never a target alone.
- fixed 2026-09-16 — [Minor] Fable F23: the cost correction contradicts
  itself two sentences on; license: the document's own words; the
  contradiction left with the mechanism that caused it.
- fixed 2026-09-16 — [Minor] Fable F24, Opus F23: ADR 0004's added
  sentence asserts its licence rather than deriving it; license: ADR
  0004's own principle; the sentence now derives its licence from the
  reader.
- fixed 2026-09-16 — [Minor] Fable F25: the retired word "context"
  survives in the glossary and the table; license: the document's own
  words; "context" gives way to the pair wherever the design is a
  co-target, in the spec and in the glossary's Consumption gate entry.
- fixed 2026-09-16 — [Important] Opus F22: the coverage tell still
  counts one document for a target that had become two; license: the
  tell exists to expose a partial read, and a joint target doubles what
  can be read partially; the card reports a pair of numbers per
  document.
- fixed 2026-09-16 — [Minor] Opus F27: the README field-table paragraph
  stands twice, verbatim, from the F12 wave; license: its own
  derivation; the duplicate is deleted.
- fixed 2026-09-16 — [Minor] Opus F26: the `integrity-auditor` row's
  `owns` cell lacks the target selection the spec prescribes to the
  card; license: an enumerated consumer, the class of F13 and F17; the
  cell names which documents are its target in each case. Recorded
  2026-09-17: the edit landed in this wave and no line was written for
  it at the time.
- declined 2026-09-16 — [Minor] Fable F20, [Important] Opus F20: the
  waiver has no home. A declined audit offer has had no record since
  before this change, and naming one here would widen a spec already
  touching fourteen parts; ruling: 2026-09-16; the spec says only that a
  declined offer behaves as it does today, and the gap and its
  consequence for chain debt's promised trace are recorded in the
  developer's memory store. Corrected 2026-09-17: the line read "twelve
  parts" and the table carried fourteen when it was written. The count
  is corrected; the decision is not reopened.

- signal 2026-09-16 — Fable judges a fourth round unearned under variant
  (a) and recommends closing the loop at `concerns` once these land.
  This is the cap round, so a fourth is the developer's to order.

### Loop closed — 2026-09-16

Three rounds, one of them run twice on two model families. Every finding
of every round is disposed: fixed under a license or a ruling, except
one declined with its reason recorded and its gap parked in the
developer's memory store. Correction, recorded at the integrity audit of
2026-09-17: this sentence was not true when it was written. Two of the
below-tier run's findings carried no line — Opus F26, whose edit had
landed unrecorded, and Opus F24, which nothing had addressed and which
the audit re-found. Both are disposed now, F26 in round three and F24 in
the audit's own block. The prescribed tier's last verdict was
`concerns`, and it is resolved here rather than by a fourth round —
Fable's own stop signal judged a fourth unearned under the ruling taken,
and round three was the cap in any case, so a further round would have
been the developer's to order.

What remains for the consumption gate, before any plan is written: an
integrity audit of this document. It has no technical design and will
not have one — this repository ships the contract and does not execute
it — so the audit takes the first of the four cases this spec defines,
a design spec as a single target.

### Integrity audit — 2026-09-17, integrity-auditor, fable 5.1

The consumption gate's audit, single target, fresh context, dispatched at
the prescribed tier after a `CLEAN` propagation gate. Eleven defects and
sixteen implementer questions; the coverage tell reported the whole
document. Every citation was checked against what it names before any
line below was written. The eleven are disposed in thirteen lines: two
defects share one line, one defect takes two, one implementer question
was promoted to a defect, and one round-three finding the ledger had
never recorded is disposed here.

- fixed 2026-09-17 — the class section counted two agent cards where its
  own body quotes three and ADR 0004 says three plus the README;
  license: the document's own enumeration; the count reads three and
  "Both cards" reads "All three cards".
- fixed 2026-09-17 — the integrity-auditor's prescribed block was
  introduced as three cases and carries four since round three added
  one; license: the ledger's own record of that addition; both mentions
  read four.
- fixed 2026-09-17 — "Four rules keep the pair honest" was followed by
  five; license: the enumeration itself; the count reads five.
- fixed 2026-09-17 — Known limitation 3 named the architect round and
  the propagation gate as the only fresh readings, denying the pair
  audit the fresh-read status the body grants it; license: the
  document's own statement that an audit is a fresh read; the audit
  joins the list.
- fixed 2026-09-17 — the Parts table's glossary row omitted `Origin`,
  which the body prescribes rewriting; license: the body's own
  prescription and the entry on disk; the row names it.
- fixed 2026-09-17 — no row owned `spec:` widening from plans to
  technical designs; license: the same; the lifecycle row names it.
- fixed 2026-09-17 — the round headings took none of the grammar the
  lifecycle rule prescribes, so neither the round cap's ordinal
  derivation nor the scope recovery could read them; license: the
  lifecycle rule's heading grammar; the three round headings take the
  prescribed shape, and round one is marked `full-document`.
- fixed 2026-09-17 — the frontmatter carried `architect-fallback: opus 5
  (degraded 2026-09-16)` and a sentence redefining the field as a record
  that a below-tier round ran; license: the lifecycle rule, where the
  field records that the stamped verdict was produced below tier and a
  dispatch at the prescribed tier gets no field. The stamped verdict is
  Fable's. The field is removed and the sentence says why none is owed.
- fixed 2026-09-17 — the gate's one fixed ordering cannot run on a first
  pass: the offer to write the technical design is itself an item of the
  design spec's gate, so the design owes no item until that offer is
  accepted, and the document never said the gate re-opens; ruling:
  2026-09-17; the dependency narrows to what its own rationale supports
  — writing the design and applying its review dispositions precedes the
  joint integrity audit — and the gate runs in passes, suspending on an
  accepted offer and resuming once the design exists, with answers
  already given staying binding unless their basis changed and a batch
  meaning every question answerable at that pass.
- fixed 2026-09-17 — [Minor] Opus F24, unrecorded in round three: the
  ordering does not say where the jointly owed item sits; ruling:
  2026-09-17; the same narrowing places it, since the joint audit is now
  the thing the ordering is about.
- fixed 2026-09-17 — a domain may add `change` values while the
  plan-coverage rule reads the column as a closed set, so a
  domain-added value escapes coverage; ruling: 2026-09-17; the values
  are `new | changed | retired | unchanged`, the set is closed to
  domains because the column steers the process, a value outside it is
  an error the author corrects, and the extension clause excepts the
  column.
- fixed 2026-09-17 — the marker test classifies this repository as
  carrying markers, against the document's claim that a repository whose
  product is prose carries none; ruling: 2026-09-17; the claim is
  removed rather than the test narrowed — a marker proves the repository
  holds code, never that a change needs decomposing, so narrowing the
  test to exclude one repository would buy the exclusion with a worse
  test. The declaration outranks the marker, this repository is named as
  a detected case that declines by declaration, and the missing
  declaration surface is made visible rather than argued away.
- fixed 2026-09-17 — the ledger's disposition lines took none of the
  grammar the lifecycle rule prescribes, and the gate block minted a
  heading the rule forbids; ruling: 2026-09-17; every line is rewritten
  to the prescribed shapes with severities recovered from the three
  dispatch records rather than re-graded, real dates and authorizers
  kept, the round-one correction note kept, the gate's lines moved under
  round two's heading in the `hit` shapes, and the two runs of round
  three disambiguated by run since their numbering collides.

The propagation gate over this wave, twice: three located hits, then
`CLEAN`.

- hit fixed 2026-09-17 — the section heading still read "its two cards"
  after the body was corrected to three; the heading reads three.
- hit fixed 2026-09-17 — the declined line's "twelve parts" against a
  table of fourteen; the count is corrected with a dated note and the
  decision left alone.
- hit fixed 2026-09-17 — the audit block's header counted eleven defects
  against thirteen disposition lines; the header reconciles them.

These lines sit here rather than under round three's heading, where the
gate-line rule would put them, because they belong to the audit's wave
and not to any round. That the rule has no place for them is a gap this
spec should answer: it designs a document class whose audits produce
dispositions, and the lifecycle rule says only that an audit's
dispositions land as edits plus the stamp, which leaves a `held` line
and a gate line homeless. Recorded here, not fixed here — the spec's
scope is the class, not the ledger's grammar.
