---
ticket: none
date: 2026-09-02
status: draft
grilled: 2026-09-02
revises: [./2026-08-17-autonomous-review-loop-design.md, ./2026-08-31-review-loop-errata-wave-one.md]
branch: feature/audit-errata
base: develop
---

# The disposition ledger as finding state

## Problem

An integrity audit of the autonomous review loop proved eleven defects.
Wave one closed the contradictions that made shipped rules disagree with
themselves. Five stayed open as one cluster, because they share a cause:
the ledger keeps needing tokens for paths nobody anticipated.

The cause is structural. **The grammar encodes the path in the state
token.** `fixed` means the session acted; `resolved` means a held
question closed. Add a path — the developer present in the round, ruling
without anything ever being held — and the grammar needs a fourth token,
then a fifth. Practice has already taken that path. Every `resolved`
line in wave one's record closes a `held` line nobody wrote, and two
`resolved (declined)` lines record a transition the grammar does not
define at all.

A second assumption is wrong in the same way. The grammar treats the
developer as asynchronous, reachable only through `held`. The loop runs
with the developer in the conversation.

## What this design is

The state machine is over **one finding**, not over the loop. Three
levels the shipped grammar conflates:

- a **round heading** records one dispatch and never changes;
- a **disposition line** carries the mutable state of one finding;
- a **gate line** carries the state of one hit — a smaller machine
  sharing the container but not the vocabulary.

Loop state proper — the round count, the all-Minor signal, the
diff-scoped chain — is derived by folding the headings. It is stored
nowhere, and this design stores it nowhere.

## The states

Four, replacing five.

    - open — [<Severity>] <claim>
    - held — [<Severity>] <claim>; question: <one closed question>; options: <the options and the session's recommendation>
    - fixed <date> — [<Severity>] <claim>; <authorizer>; <what changed>
    - declined <date> — [<Severity>] <claim>; <authorizer>; <why the document stands>

`open` and `held` are the non-terminal states, and the only two the
Unfinished-work list anchors. `fixed` and `declined` are terminal and
say what became of the document: it changed, or it stands.

`fixed` and `resolved` merge because they were never two states. Both
mean the document changed on account of this finding; they differed only
in who authorized the change, which is now a clause. Merging also frees
a word the rules currently use for two objects — `concerns (resolved
<date>)` annotates a verdict, while `resolved <date>` annotated a
finding.

## The clauses

The leading token is a queryable state. Clauses are payload.

| clause | carries | on |
|---|---|---|
| `license: <citation>` | the written decision the session acted on | `fixed` |
| `ruling: <date>` | the developer authorized it | `fixed`, `declined` |
| `question:` | the question, phrased so one short answer resolves it | `held` |
| `options:` | the options and the session's recommendation | `held` |
| `counter:` | the session's evidence where the finding is disputed or contested | `held` |
| `deviation: <section>` | where the rationale for departing from a reviewer's suggestion lives | `fixed` |

`question:` and `options:` are both required on a `held` line: the batch
that relays them is a transcript, and a session that dies between the
relay and the answer leaves the next session to re-derive the options —
possibly differently, so the developer answers a question that silently
changed. `counter:` and `deviation:` are conditional, written whenever
their condition holds.

Every terminal line carries exactly one authorizer, `license:` or
`ruling:`. A `declined` line always carries `ruling:`: declining is a
decision, and triage gives a session no license to decide.

Payload costs nothing structurally. The Unfinished-work commands anchor
on `^- `, so an indented continuation under a disposition line matches
no command and disturbs no consumer. Where payload runs long, it
belongs in indented sub-bullets rather than in a longer line.

## What the authorizer buys

Two shipped rules discriminate on the token today, and they do opposite
things: the oscillation tripwire escalates a finding re-raised against a
`fixed` line, and the relitigation clause folds one re-raised against a
`resolved` line. Merging the tokens would collapse that distinction, so
both move to the clause:

- re-raised against `license:` — two readings of one license, a
  contested reading, escalates as held with the flip named;
- re-raised against `ruling:` — a recorded developer decision, folded
  and cited, never asked again.

This is stronger than what it replaces. Today both rules key on a proxy:
`resolved` happens to imply the developer. After the change the
predicate says what it means.

## Write-ahead

**Each disposition line is written before the edit it describes, or with
it — never batched at the end of a wave.**

The dangerous failure is not a session dying mid-round; it is a fix wave
half-applied with no lines written. The body has changed, nothing says
which change belongs to which finding, and the next round's brief reads
a diff source that is silently wrong. Writing contemporaneously makes a
partial wave self-evident: `open` and `fixed` lines mixed under one
heading say exactly where the session stopped.

This costs no notation. The rule already prescribes `open` at stamp
time; this extends the same discipline to every later transition.

## The cap is best-effort

The round cap guards spend, not correctness, and it survives no
compaction — the count is derived from headings, but the reset event is
not recorded anywhere.

**Developer contact is a message from the developer.** Not a relay they
read, not an escalation the session sent, not an unanswered batch. That
matches what unattended means, and it needs no notation.

**A session that cannot count its own rounds escalates rather than
assuming.** Resetting to zero after a compaction fails in the wrong
direction: a long session could grant itself three fresh rounds after
every compaction. Treating a lost count as its own reason to ask costs
nothing and bounds the spend the cap exists to bound.

## Gate lines

The two shapes stand. One stated reason does not: the rule claims the
date tells a gate episode apart from the round's own findings, and wave
one's own record disproves it — three `hit fixed 2026-09-01` lines sit
beside six `resolved 2026-09-01` disposition lines under one heading, and
two episodes share the date 2026-08-31. **The `hit` token is the
discriminator.** A wrong stated reason invites a later session to
correct the right practice, so the sentence is replaced rather than
dropped.

## What this does not build

Each refusal is recorded with its reason, so a later wave reopens it
with evidence rather than by taste.

- **No `hit outstanding` token.** A hit is mechanically re-derivable:
  the next gate episode regenerates it for the price of the cheapest
  agent in the system. A lost finding is gone forever; a lost hit is
  not. The state has also never occurred, and minting it would
  contradict two glossary entries that call a hit binary.
- **No `why:` clause on `held`.** Its value is drawn from a closed
  four-way set — no license, a contradiction between decisions, a
  disputed finding, or one that could go either way — which the
  `question:` phrasing already carries.
- **No episode identity for gates.** One consumer needs it — the
  re-dispatch bound's counter — and only across session loss. Losing it
  costs at most two dispatches on the cheapest family. Let it die with
  the session.
- **No structured block, sidecar file, or git as the diff source.** An
  LLM hand-writes this record either way, so structure buys checkability
  the writer's nature does not deliver; and the lifecycle rule keeps
  these documents uncommitted through the rounds on purpose.

## The blocking terminator loses its self-fix prohibition

`blocking` keeps its meaning — autonomy suspended, no further round
without the developer — and drops the clause forbidding self-fixes.

The prohibition's own rationale is about findings, while the
prohibition is stated on the verdict. **A design reshape has no citable
license by construction, so triage already holds it.** Wave one's round
1 is the evidence: five wording and consistency fixes, every one with a
clean citation, none a reshape, all forbidden only because the
reviewer's grade read `blocking`.

## Severity casing

All 163 severity slots in this repo capitalize, against a glossary that
fixed `critical | important | minor` in lower case. The grilling settled
it in the glossary rather than here: the value is canonical as a word,
and its casing follows the syntax it sits in — lower case as a rule
tag's field value, capitalized in the ledger's bracket slot. One
concept, two syntaxes, two rendering conventions, and no migration.

This design therefore states no casing rule of its own; it cites the
**Severity** entry. Deferring the question to a lint would have made the
lint's first act the condemnation of every committed line.

## Changes by file

- `plugins/working-process/rules/spec-plan-lifecycle.md` — the four
  states and their shapes, the clause table, the authorizer rule, the
  write-ahead sentence, the corrected gate discriminator, the refusals,
  and the relitigation clause rekeyed to `ruling:`. Two further sites
  the grilling found: the Unfinished-work section says a ledger close is
  `open` or `held` becoming `resolved <date>`, which the merge makes
  `fixed <date>` or `declined <date>`; and two sentences call the
  list's own entry a "review-loop ledger entry", a phrase the glossary
  now bans as a name for a disposition line, so both read
  "review-loop entry" instead.
- `plugins/working-process/rules/workflow.md` — the oscillation tripwire
  rekeyed to `license:`, the `blocking` terminator's prohibition
  deleted, and the cap's contact definition with its
  cannot-count escalation.
- `docs/domain/glossary.md` — already changed by the grilling, not by
  the implementation: six new terms (**Adjudication** and **Ruling** as
  a level-distinguishing pair; **Disposition ledger**, **Round
  heading**, **Disposition line** and **Gate line** for the structure
  the loop had been naming without defining), plus a **Severity**
  sentence putting casing under the syntax each value sits in. The
  refusal of `hit outstanding` is what keeps **Hit** binary.
- `docs/specs/2026-08-31-review-loop-errata-wave-one.md` — its bare
  `- dismissed 2026-08-31` line takes the `hit dismissed` shape the
  grammar defines.

Historical ledger lines stay as written. One sentence records that they
predate the merge, as the `scope` token's introduction already
established.

Merging a published token narrows a shipped convention, so the release
carrying this takes a minor bump.

## Seams this does not close

- **The glossary has no owner on the fix-wave path.** Three collisions
  in wave one, and a fourth arrived during this design's own
  consultation. The candidates are a triage duty — a `fixed` line whose
  license is a glossary term, or whose change moves a term's meaning,
  owes a glossary check — or a standing enumeration target for the
  propagation gate, which reaches only the quoting case.
- **A stop signal cannot bind text written after it was given.** New
  design written after a stop signal should re-arm review rather than
  override it, and the signal should be scoped to the text it read.
- **A plan's owed confirming round has no Unfinished-work entry.** The
  workflow rule calls the diff-scoped LGTM heading a durable marker and
  prescribes a recovery reading, but no command matches it, so
  `process-status` reports clean while a confirming round is owed.
- **Concurrent waves on one document are undetected and unsupported.**
  The store is an uncommitted file, and the one-live-round rule is
  scoped within a session. Declaring the limit is cheap; engineering
  around it is not.
- **The deferred grammar lint.** Roughly half of this design becomes
  mechanically checkable if it ships and stays convention if it does
  not.
- **Per-round commits, with a named trigger.** The lifecycle rule
  suggests committing only at the implementation-ready gate, while
  allowing the developer to commit sooner on their own call. If a loop
  starts committing each round, `hit fixed` loses its justification —
  the gate's diff would have a durable home elsewhere — `<what changed>`
  thins to a sentence, and the round heading can carry a commit hash.
  That trades this design's shapes for fewer, so it belongs to a later
  wave and not to this one.
