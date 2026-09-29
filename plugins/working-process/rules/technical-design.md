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
| 6 | Cuts not taken | conditional | one line per rejected division and its reason — the material the architect grades, when that agent is available |
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
