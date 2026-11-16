# review-loop — the ledger grammar

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

`open` and `held` are the non-terminal states, and the only two
disposition states the Unfinished-work list anchors; the one gate line
it anchors, `hit held`, is defined under *Gate lines* below. `fixed`
and `declined` are terminal and say what became of the document: it
changed, or it stands.

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
  written decision, `ruling:` where the developer did, `provisional:`
  where a stand-in did.
- `declined <date>` — the document stands. It always carries `ruling:`,
  or `provisional:` where a stand-in declined it, because declining is
  a decision and triage gives a session no license
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
| `provisional: <date> (stand-in <name>)` | a stand-in the developer named decided it, on that date; it licenses nothing until the developer confirms it in the provisional batch, when it becomes `ruling:` | `fixed`, `declined` |
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
stops certifying the words that changed. The `integrity:` stamp is
read at the consumption gate alone: one gone stale after the plan was
written is expected and owes no new audit. The same heading serves a
register edit that a plan's held gate line licensed, on a design spec
whose loop has closed at whatever verdict: the heading then names the
plan whose gate held the hit, and that plan's terminal gate line names
the heading and the line under it. Unlike a review-licensed fix, such an
edit never joins a resolution note, even on a `concerns (resolved)`
spec: that note records what resolved the verdict, and this edit
resolves none.

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

The propagation gate, when that agent is available, writes gate lines of
its own: the two ordinary shapes here, and the held shape and its three
terminal rewrites below. Each carries its own leading token and never a
severity, because a hit is a located detection the dispatcher confirms
or dismisses, never a graded finding:

    - hit fixed <date> — <the hit's claim>; <what changed>
    - hit dismissed <date> — <the hit's claim>; counter: <the derivation that refutes it>

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

Each is written at gate time, under the last round's heading. The `hit`
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

A gate episode always lands somewhere: its lines are the reason a later
reader need not re-derive what the session already settled.

No gate-line shape covers a hit left outstanding when the re-dispatch
bound in the workflow rule stops an episode. That state owes the
developer a decision, so neither `hit fixed` nor `hit dismissed` can
honestly carry it, and `hit held` is scoped to the coverage duty's
hits; no anchor surfaces it today — a stated gap, not an oversight.
Until a shape exists, the workflow rule's report is its only record.

A `hit fixed` line puts the gate's ordinary work where the next
diff-scoped brief already looks, beside the round's `fixed` lines. A
`hit dismissed` line records a decision the developer was never asked to
make, so a later round cites it instead of re-deriving it and a session
that would dismiss the same hit differently argues against written words
rather than silence. Neither joins the unfinished-work anchors: both are
closed when written and owe nobody a next move. A `hit held` line owes
the developer an answer, so it joins them until its terminal rewrite.

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

A line carrying `provisional:` is not settled: it records nobody's
decision yet, so a re-raise against it is ordinary triage, as against a
`license:` line, and nothing here folds it.

State prevents relitigation, not the reviewer's memory.
