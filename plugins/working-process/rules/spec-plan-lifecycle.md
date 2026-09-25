---
paths:
  - "docs/specs/**"
  - "docs/technical-designs/**"
  - "docs/plans/**"
---

# Judged documents and plans — frontmatter and lifecycle

Design specs live in `docs/specs/`, technical designs in
`docs/technical-designs/`, plans in `docs/plans/`. All three open with a
YAML frontmatter block:

```yaml
---
ticket: ABC-123     # tracker reference; inline list when several; `none` without one
date: 2026-07-13    # ISO creation date
status: draft       # moves forward only: draft -> approved -> implemented
grilled: grilling   # optional: `grilling` while outcomes are pending; the ISO date once applied
architect: LGTM     # optional: latest architect verdict (LGTM | concerns | blocking)
adversary: LGTM     # optional: latest plan-adversary verdict (LGTM | concerns | blocking)
architect-fallback: <model> (degraded <date>)   # optional: verdict above produced below the prescribed tier (adversary-fallback: for plans)
integrity: <ISO date> (sha: <short-hash>[; with: <file>@<short-hash>])   # optional: date of the last integrity audit, the body hash it certifies, and — where a technical design was audited with it — that document and its hash
revises: ./<file>.md   # optional: documents this one departs from; inline list when several
spec: ../specs/<file>.md   # plans and technical designs: the design spec this document descends from; inline list when several, on a plan
technical-design: ../technical-designs/<file>.md   # optional: on a design spec, the technical design that develops it; on a plan, the technical design of each design spec it descends from that has one — inline list when several, each path relative to the plan
branch: feature/ABC-123-short-name   # optional: topic branch of the work
base: master        # optional: branch the topic branch was cut from
---
```

- `status` is linear and moves forward only. Review rounds are iterative
  and live in their own fields; `grilled`, `architect`, and `adversary`
  appear only once the corresponding step has run.
- An `implemented` document records what shipped at its release, and the
  surfaces it named are the current truth. Never build from one without
  diffing it against those surfaces first — the document is the archive,
  not the specification of what stands today. It is amended only in
  frontmatter, never in the body: a verdict certifies the body it was
  given, and an `integrity:` hash covers exactly that text. One class of
  body edit is excepted: a ledger annotation recording a process event,
  such as `, debt discharged <date>`, is a process record rather than a
  design amendment.
- `revises:` names the documents a newer one departs from — written on
  the newer document, pointing back, and never on the older one, which
  stays as its stamps left it. It records supersession, not lineage: a
  document that merely builds on another says so in its prose, and a
  plan's `spec:` pointer is lineage too. What `revises:` claims is that
  the named document's design no longer matches what shipped.
- A round that ends in `concerns` or `blocking` records its findings (or
  their disposition) in the document body — a verdict whose findings were
  never written down cannot be honestly resolved later.
- Concerns resolved without a fresh review round keep the verdict and
  gain a resolution date — `adversary: concerns (resolved 2026-07-16)` —
  plus a body note saying what resolved them. A fresh round replaces the
  whole value as usual. A `blocking` verdict the developer closes by
  explicit adjudication instead of a fresh round takes the same form with
  its own token — `architect: blocking (adjudicated 2026-08-17)` — and
  the round's ledger record as that body note. On a plan both wait for
  the confirming round: neither is written while the latest round
  heading is diff-scoped, unless the plan is already `implemented`,
  where the annotation — or the developer's adjudication — is written
  citing that standing decision. Its body note is written too: a note
  recording what resolved a verdict is a process record, which the
  implemented-document rule above excepts from its frontmatter-only
  clause, as it excepts `, debt discharged <date>`.
- A verdict produced below the prescribed tier (the model-selection
  heuristic in the workflow rule) gains a companion `architect-fallback:`
  / `adversary-fallback:` field: the family alias of the model that
  produced it, then `(degraded <ISO date>)` for anything other than the
  developer's deliberate choice (a cap refusal — including a consented
  one-tier drop — a silent platform substitution, or an under-dispatch
  the dispatcher did not knowingly decide) or `(chosen <ISO date>)`
  when the developer deliberately dispatched below the prescribed tier
  before any refusal. A dispatch at the prescribed tier gets no field.
- Both tokens carry a re-review offer at the document's next consumption
  gate — before plan-writing for a judged document, before
  implementation for a plan. Accepted: a fresh round at the prescribed
  tier replaces the
  verdict and removes the field (a fresh round that is itself below the
  prescribed tier refreshes the field's date instead, and the offer
  re-arms at the same gate). Declined: the field gains `, waived <date>`.
  Moving `status` to `implemented` with a bare fallback field stamps the
  waiver as part of the move.
- `integrity:` records an integrity audit — the run the
  `integrity-auditor` agent performs, when it is available — which the
  dispatcher stamps once the audit's dispositions are applied:
  `integrity: <ISO date> (sha: <short-hash>)`, the date for the reader and
  the hash for the check. The hash covers the text below the
  frontmatter's closing `---`, so writing the stamp never invalidates what
  it stamps. Where the audit also discharges a chain debt, the annotation
  is written before the hash is recomputed: the annotation lands inside
  the hashed body, so a stamp written first is stale the moment it lands.
  Stamper and gate run one command, so the comparison can never
  mismatch on convention:
  `sed '1,/^---$/d' <file> | shasum | cut -c1-7`
  — `shasum` rather than `sha1sum` because stock macOS ships only the
  former, and the two produce identical digests, so a GNU-only environment
  may substitute `sha1sum` without changing a recorded hash. The field
  carries no verdict: it answers whether the document was checked after
  its last edit, and that answer is a comparison rather than a clock. A
  recomputed hash differing from the stamped one means unaudited, same-day
  edits included; any change re-arms the stamp, a typo fix included.

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
- A judged document's consumption gate owns the recomputation: before
  plan-writing it
  recomputes the body hash and compares, a match meaning the standing
  stamp satisfies the gate and a mismatch firing the audit offer. Those
  are judged-document semantics — on a plan, a permitted target on
  explicit
  request, the stamp is informational and goes stale silently. Staleness
  joins no Unfinished-work entry: it is a recomputation, not a grep.
- Verdict agents self-report the model they ran on (family plus version);
  the dispatcher compares it against the dispatched and prescribed
  tiers before stamping, and each round's verdict, model, and date are
  recorded in the document body. Committed examples of the bare fallback form use
  placeholders (as above) so they never match the list below.
- `branch` and `base` appear once the topic branch exists — never guessed
  up front, omitted entirely when there is no topic branch.
- `technical-design:` is optional and appears once the technical design
  exists, so its absence means there is none rather than one nobody
  linked. On a design spec it is new in kind: every other pointer
  records where a document came from, while this one names a document
  written later, and it gives a reader holding the design spec the
  structure that develops it. The author who creates the design writes
  both ends in
  the same turn — the design's `spec:` and the design spec's
  `technical-design:`. A plan's `technical-design:` names, for every
  design spec its `spec:` names that has a technical design, that
  technical design — an inline list when several, each entry the same
  document the design spec's own pointer names, its path written
  relative to the plan's directory rather than copied. A design spec
  with no technical design contributes no entry, so a plan from specs
  `a` and `b`, where only `a` names a design, carries that one design.
  One technical design per design spec.
- Where a plan's `technical-design:` names documents, those documents
  define the interfaces. The plan's `**Interfaces:**` blocks reference
  the contracts they define and say which part of one each task
  implements or changes; they do not independently redefine those
  contracts. Where a plan names no technical design, the existing plan
  convention stands unchanged. This binds how the blocks are filled and
  changes no plan template — the template belongs to the tool that
  writes plans.

## Finding what revises a document

`revises:` points backward only, so the documents that departed from a
given one are found by sweeping for it. The line matches both the
single-reference and inline-list forms, `--no-ignore` reaches
ignored-mode artifacts, and the tolerant leading anchor finds the field
where a second writer relocated it:
`rg -l --no-ignore --crlf '^\s*revises:.*<file-stem>' docs/`

This is a lookup, not an Unfinished-work entry: a `revises:` pointer
owes nobody a next move, and the implemented-document principle above
already warns every reader of an archived document without it.

## The disposition ledger

The body record a `concerns` or `blocking` round owes has a canonical
shape, not an improvised one — practice produced three competing
conventions across six documents before it was written down. The rounds
live under one section, `## Review rounds`, and each round opens with a
heading:

    ### <ISO date> — <agent>, <model self-report>, <verdict> (round N[, <scope>])

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

Under the heading each finding takes one line, its disposition the
leading token:

    - open — [<Severity>] <claim>
    - held — [<Severity>] <claim>; question: <one closed question>; options: <the options and the session's recommendation>
    - fixed <date> — [<Severity>] <claim>; <authorizer>; <what changed>
    - declined <date> — [<Severity>] <claim>; <authorizer>; <why the document stands>

The severity bracket is omitted on a line whose sole authorizer is
`ruling:` **and** which no reviewer graded — both legs, never one:

    - fixed <date> — <claim>; ruling: <date>; <what changed>

`open` and `held` are the non-terminal states, and the only two the
Unfinished-work list anchors. `fixed` and `declined` are terminal and
say what became of the document: it changed, or it stands.

The two dates on a terminal line record different events and are both
written even when they coincide. The leading date is when the line
reached its terminal state; `ruling:` is when the decision it cites was
taken. On an ordinary developer-authorized line the two are the same day
and say so; on a fold they differ, and that divergence is the point of
carrying both.

The severity slot is a reviewer's grade, so it is omitted exactly where
there is none: a change the developer directed mid-round is not a
finding, and inventing a grade for it would be the same manufacture the
authorizer rule forbids. This adds no fourth severity value; the
glossary's three stand.

`fixed` and `resolved` merge because they were never two states. Both
mean the document changed on account of this finding, and they differed
only in who authorized it, which is now a clause. Merging also frees a
word the rules used for two objects — `concerns (resolved <date>)`
annotates a verdict, while `resolved <date>` annotated a finding.

- `open` — written at stamp time, before the findings are triaged. An
  `open` line surviving a session means the remediation never ran, and
  the document's next touch re-offers it.
- `held` — the finding needs the developer. The line carries the
  concrete question and the options with the session's recommendation;
  where the finding is disputed or contested, `counter:` carries the
  evidence the developer needs in order to answer, and the oscillation
  tripwire's named flip is that evidence.
- `fixed <date>` — the document changed on account of this finding. Its
  authorizer says who decided: `license:` where the session cited a
  written decision, `ruling:` where the developer did.
- `declined <date>` — the document stands. It always carries `ruling:`,
  because declining is a decision and triage gives a session no license
  to decide.

Each disposition line is written before the edit it describes, or with
it — never batched at the end of a wave. The dangerous failure is not a
session dying mid-round but a fix wave half-applied with no lines
written: the body has changed, nothing says which change belongs to
which finding, and the next round's brief reads a diff source that is
silently wrong. Writing contemporaneously makes a partial wave
self-evident, since `open` and `fixed` lines mixed under one heading say
exactly where the session stopped.

The leading token is a queryable state. Clauses are payload.

| clause | carries | on |
|---|---|---|
| `license: <citation>` | the written decision the session acted on | `fixed` |
| `ruling: <date>` | the developer authorized it; on a fold, the prior ruling's date followed by `folding <section or line quote>` naming what it folds against | `fixed`, `declined` |
| `question:` | the question, phrased so one short answer resolves it | `held` |
| `options:` | the options and the session's recommendation | `held` |
| `counter:` | the session's evidence where the finding is disputed or contested | `held` |
| `deviation: <section>` | where the rationale for departing from a reviewer's suggestion lives | `fixed` |

`question:` and `options:` are both required on a `held` line: the batch
that relays them is a transcript, and a session that dies between the
relay and the answer leaves the next session to re-derive the options,
possibly differently, so the developer answers a question that silently
changed. `counter:` and `deviation:` are conditional, written whenever
their condition holds.

Every terminal line carries exactly one authorizer.

A fix one review licenses can land in a document other than the
reviewed one — a plan review's finding whose `origin` names a judged
document is the
case the workflow rule names. The disposition line then lands in the
ledger of the document that changed, and the reviewed document's line
points at it in its `<what changed>` clause, naming that document and
the heading the line sits under: one authorizer, two documents, two
lines, and the invariant above holds on each. The pointer needs no
clause of its own — `<what changed>` already belongs to the `fixed`
line's shape, so the clause table stays closed. In the changed
document the line goes under its latest round heading, or with the
body note the resolution annotation above already owes, where that
document is stamped and no fresh round ran. A document whose loop
closed at `LGTM` has neither — the annotation is defined for `concerns`
and for a `blocking` verdict closed by adjudication, never for `LGTM` —
so the fix opens a heading of its own:

    ### <ISO date> — fix from <path of the reviewing document>

It carries no ordinal and no verdict, which keeps it out of the round
cap's derivation and out of the Unfinished-work commands that anchor a
round heading: it records a fix, not a round. Two stamps go stale as on
any body edit — the `integrity:` hash stops matching, and the verdict
stops certifying the words that changed.

Payload costs nothing structurally. An Unfinished-work command under the
list's default scope guard is held to the frontmatter block, so no body
line reaches it at all; an entry publishing its own scope anchors a
leading disposition token or a round heading, and an indented
continuation matches neither. Payload under a line is therefore invisible
to every published command, and where it runs long it belongs in
indented sub-bullets rather than in a longer line.

Two additions extend those shapes, and nothing else does: the
annotation here, and the cross-document fix heading above. A
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
licenses begins, and written for every document that offer named — a
declined offer over an audit pair discharges the chain debt of both.
What a decline never does is stand in for the audit itself: it writes
no `integrity:` stamp, leaves every other open finding open, and closes
no `blocking` verdict. "Do not run the audit" is a release from the
chain debt the offer named and from nothing else; an integrity audit,
written once its dispositions are
applied and before the `integrity:` stamp — and where that audit read an
audit pair, it discharges the debt of both documents it read, annotating
each document's own unannotated diff-scoped `LGTM` headings; and any
later full-document
round, at its stamping turn, whatever its verdict — the debt is
discharged by the reading, not by the grade. A full-document round reads
the whole document, so it annotates every unannotated diff-scoped `LGTM`
heading above it rather than only the one it follows.

The token carries a date and nothing else. Each path leaves its own
trace — an `integrity:` stamp, a later full-document heading, or
neither — and no consumer reads the path, so recording it would give one
fact a second home. Where a session discharges the debt and dies before
annotating, the annotation's own derivation licenses a later session to
write it; on a document still in flight only the decline path has
nothing to derive from, and there the debt correctly re-surfaces and the
developer declines again. On a document already `implemented` the
Chain debt entry's owner leg makes even that derivable, from the
standing decision it cites.

Ledger lines written before this merge stay as written, as the `scope`
token's introduction already established. The shapes they use are kept
here as described historical forms rather than deleted:

    - resolved <date> — [<severity>] <claim>; landed in <section>
    - resolved <date> (declined) — [<severity>] <claim>; <why the document stands>

A reader must still parse pre-merge documents, and a fold against a
pre-design settled line cites a date off a token the live grammar no
longer produces. These two shapes are described, never minted: no
session writes a new line in either form.

Narrative prose between the lines of a `## Review rounds` section is
lawful and expected. This grammar governs headings, lines, and their
indented payload; a paragraph explaining why a wave went the way it did
belongs there too. A lint over the section reads the anchored lines and
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

The propagation gate, when that agent is available, writes two shapes of
its own. They carry their own leading token and never a severity, because
a hit is a located detection the dispatcher confirms or dismisses, never
a graded finding:

    - hit fixed <date> — <the hit's claim>; <what changed>
    - hit dismissed <date> — <the hit's claim>; counter: <the derivation that refutes it>

Neither carries a license either, because a hit's fix is licensed by its
own derivation.

Both are written at gate time, under the last round's heading. The `hit`
token tells a gate line apart from that round's own findings; the date
does not, since a gate episode and the round it precedes commonly share
one. A gate still never mints a heading of its own, on the separate
ground that the round heading's grammar is closed and a gate is not a
round. The fix heading above is no counter-example: a gate's lines can
wait for the round that is coming, while a fix landing on a document
whose loop closed at `LGTM` waits for nothing. Writing at gate
time is what the lines are for: a dismissal must exist while the episode
is still re-dispatching, or the gate cannot terminate, and the next
diff-scoped brief is composed before its own round is stamped. A gate
before a document's first round has no heading to write under; its lines
wait for that round and are written at its stamp, the one case where
they do.

A gate episode always lands somewhere: its lines are the reason a later
reader need not re-derive what the session already settled.

Neither shape covers a hit left outstanding when the re-dispatch bound
in the workflow rule stops an episode. That state owes the developer a
decision, so neither `hit fixed` nor `hit dismissed` can honestly carry
it, and no anchor surfaces it today — a stated gap, not an oversight.
Until a shape exists, the workflow rule's report is its only record.

A `hit fixed` line puts the gate's ordinary work where the next
diff-scoped brief already looks, beside the round's `fixed` lines. A
`hit dismissed` line records a decision the developer was never asked to
make, so a later round cites it instead of re-deriving it and a session
that would dismiss the same hit differently argues against written words
rather than silence. Neither joins the unfinished-work anchors: both are
closed when written and owe nobody a next move.

A line carrying `ruling:` is a recorded developer decision, and what a
later round may do with it depends on what that round brings:

- re-raised without new evidence — folded and cited, never asked again;
  the fold produces `declined <date>` carrying `ruling:` with the prior
  ruling's date and a `folding` citation of the line it folds against,
  so the authorizer is cited rather than manufactured;
- re-raised with new evidence — `held`, its `counter:` citing the prior
  ruling, because a session that folded this alone would arbitrate
  between a reviewer and a recorded developer decision.

Evidence is new relative to what the folded line records — its claim and
the reasoning its clauses carry — not relative to the reviewer's
wording. A session that cannot tell holds rather than folds.

A pre-design settled line carries no authorizer clause and is settled by
its token alone; a fold against one cites the date on that token, which
is when the developer decided.

State prevents relitigation, not the reviewer's memory.

## Unfinished-work list

One entry per class of unfinished process work: the class name, its
command, and the owner of the next move, plus its own match scope where
the entry re-scopes one. This section is the list — a
command published elsewhere, such as the ticket sweep in the
ticket-frontmatter rule, is a lookup and not part of it. The
`process-status` skill, when available, runs exactly what stands here,
and this heading is the name it keys on: the heading and the skill move
together or not at all.

A command returns hits, not Findings. A hit counts only when the
matching line sits inside the document's frontmatter block — between the
`---` on the file's first line and the `---` that closes it, never a
later pair — because a document quoting this convention in its body
describes it rather than instantiating it. That guard is the default. An
entry re-scopes it only by publishing its own match scope as a fourth
leg, and the entries below that do so say it there.

- **Grilling pending** — a session's outcomes are recorded and not yet
  applied.
  `rg -l --no-ignore --crlf '^\s*grilled: grilling' docs/`
  Owner: the grilling-session, when available.
- **Unresolved verdict** — a round ended in `concerns` or `blocking`
  and nothing closed it.
  `rg -l --no-ignore --crlf '^\s*(architect|adversary): (blocking|concerns)$' docs/`
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
- **Unfinished review-loop ledger** — a disposition line nobody closed:
  an `open` line whose remediation never ran, or a `held` line whose
  question still waits.
  `rg -n --no-ignore --crlf '^- (open|held) —' docs/`
  Scope: a hit counts only inside a `## Review rounds` section — this
  entry's own re-scoping of the guard above, kept for the same reason,
  since a document quoting the grammar describes it rather than
  instantiating it. Confirming section membership needs line positions,
  which is why this command carries `-n` where the others carry `-l`.
  Owner: an `open` line belongs to the document's next touch, which
  re-offers the remediation; a `held` line belongs to the developer.
- **Chain debt** — a diff-scoped `LGTM` heading carrying no record that
  what it owed was discharged.
  `rg -n --no-ignore --crlf '^### .*LGTM \(round [0-9]+, diff-scoped\)$' docs/`
  Scope: a hit counts only inside a `## Review rounds` section — the
  second entry to re-scope the default guard, for the reason the first
  one does, and carrying `-n` for the same reason.
  Owner: for a judged document, the consumption gate's pair offer; for a
  plan, the
  confirming full-document round. On a document already at
  `status: implemented` the debt is discharged by recorded decline
  without any dispatch: completed work is not re-reviewed, so the
  annotation is written citing that standing decision, and a document
  still in flight keeps the pair offer.
- **Pending re-review** — a verdict produced below the prescribed tier,
  neither refreshed nor waived.
  `rg -l --no-ignore --crlf '^\s*(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/`
  Owner: the re-review offer at the document's consumption gate.
- **Misplaced stamp** — a process field outside the top level of the
  frontmatter, at any value.
  `rg -l --no-ignore --crlf '^\s+(grilled|architect|adversary|architect-fallback|adversary-fallback|integrity):' docs/`
  Owner: the developer; no process surface owns moving a stamp back.
  The class suppresses per field: it hides any other class whose
  published command would match the relocated line — at most one, and
  for a field no other command names, such as `integrity`, none —
  itself excluded, since its own command matches every process field.
  Match semantics are the mapping, so a class published later needs no
  extra rule.

The tail anchors are exact on purpose: a `(resolved <date>)`,
`(adjudicated <date>)` or `, waived <date>` annotation defeats the
match, and that defeat is the recorded closed state. The leading
anchors are tolerant on purpose, so a relocated field is still found.
The Misplaced stamp command anchors `^\s+` instead, because there the
indentation is the defect it looks for rather than an accident to
tolerate. Those anchors sit on a frontmatter field wherever the default
guard holds. An entry publishing its own scope anchors a body line
instead — a leading disposition token or a round heading — and there the
close is a rewrite or an appended annotation: `open` or `held` becomes
`fixed <date>` or `declined <date>`, and a discharged chain debt gains
`, debt discharged <date>`. Either way the anchor stops matching.

## Lifecycle offers

Each an offer the developer may decline, and each made
only when the tool is available: grill a fresh spec (grilling-session);
architect-review a grilled design spec, and a technical design, which
is never grilled (architect agent dispatch);
adversary-review a plan before implementation (plan-adversary agent
dispatch); offer the pending re-review of a fallback-recorded verdict at
its consumption gate (fresh round at the prescribed tier); and when a
judged document or plan moves to `implemented` and the
memory-review-session skill
is available, offer a Project memory review — released work-state notes
close, resolved entries sweep to the archive. After any
review round, relay the report to the developer, then stamp the
verdict into the document's field — this sentence and the workflow
rule's verdict-agent dispatch subsection state the same
relay-before-stamp ordering and are edited together when that changes.
The subsection sequences further checks inside its own turn — the model
self-report before the relay, the report's citations after it — which
this sentence deliberately does not restate, so gaining one does not
make it stale. The order has one named exception, defined in that
subsection: a plan's diff-scoped LGTM is relayed and its round record
written, while only the frontmatter stamp waits for the confirming
full-document round.

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

A document's consumption gate is the backstop for its ledger: no judged
document passes to plan-writing, nor a plan to implementation, while
`held` lines stay open — an LGTM can leave the frontmatter clean while a
decision question still pends, so the gate asks those questions at the
latest. Writing a plan from a judged document is that same seam: its
held questions are asked before the plan is written, whoever writes it.

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

The process suggests committing the work's documents under `docs/` at
exactly one point — the implementation-ready gate: the developer has
approved the plan (the `status` flip to `approved`) and implementation
is about to start. During authoring — spec drafting, grilling,
technical-design writing, review rounds, plan writing — it never makes
that suggestion; the documents'
uncommitted state is deliberate, not dirt in the process-artifacts
sense, and the developer may commit sooner on their own call. The
suggestion covers only paths git tracks or would track; deliberately
ignored documents are skipped silently, and committing itself stays
with the developer.

Asking whether the loop may commit per round is not that suggestion, and
the difference is the speech act rather than the timing. The suggestion
above says a moment to commit has arrived; the consent question asks
once, before any round runs, for standing authorization to use a
mechanism — and a "no" leaves the authoring phase exactly as this
paragraph describes it. That is why it may be asked during authoring
while the suggestion may not.

One shape of that sooner call has a convention, because practice kept
reaching for it: **per-round commits on a document branch.** When the
developer authorizes it, the loop commits the reviewed document once per
round, as the round's last act. That boundary matches the ledger's own
unit — a round mutates the document several times (the stamp, the
triage, the fix wave, any gate episodes), and one commit after the wave
records what the round found together with what the session did about
it.

The commits go to a local branch named `<topic>.docs`, never to the
topic branch itself. Git refuses a ref nested under an existing branch,
so `feature/<ticket>-<short-name>/docs` cannot exist while its parent
does; the
suffix takes a dot because the branch convention already spends hyphens
on name parts, where `-docs` would read as a topic about documenting.

The loop runs on that branch for the whole authoring phase — the design
spec's rounds, the technical design's and the plan's alike — and the
topic branch takes it at the
implementation-ready gate: by fast-forward where the history is wanted
whole, by squash where it is not. That choice belongs to the project
rather than the session, so a `CLAUDE.md` note — at the repo root or
beside the documents — records it where it binds, and a session with no
such note asks at the gate. Either way the document branch survives the
merge, which keeps loop churn off any published branch until somebody
pushes it and leaves the surviving ref marking where authoring ended.

Both halves of "local" are worth knowing before relying on it. Churn
stays private, and the history dies with the working copy: a teammate
cannot see it, and a lost machine takes it. That is still more than the
alternative, where the same rounds live only in a transcript, but it
means "return the document to the state round three read" is a promise
about one clone rather than about the repository.

What per-round commits never do is replace the ledger. Git says which
lines changed; the ledger says with what intent and on whose license,
and a diff carries neither "narrowed the claim" nor a cited ADR. A
`<what changed>` clause may thin to a sentence where the commit carries
the detail; it does not go. Nor does a sha stand in for a hash: a round
heading that one day carried its commit's sha would name that round,
and it never stands in for the `integrity:` hash, which is computed from
the body and must work on a document nobody committed — the default
path, where no sha exists.

Ticket value format, sourcing order, and backfill live in the
ticket-frontmatter rule.
