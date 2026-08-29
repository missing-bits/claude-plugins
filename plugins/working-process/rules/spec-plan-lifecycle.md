---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
---

# Specs and plans — frontmatter and lifecycle

Specs live in `docs/specs/`, plans in `docs/plans/`. Both open with a
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
integrity: <ISO date> (sha: <short-hash>)   # optional: date of the last integrity audit, plus the body hash it certifies
branch: feature/ABC-123-short-name   # optional: topic branch of the work
base: master        # optional: branch the topic branch was cut from
---
```

- `status` is linear and moves forward only. Review rounds are iterative
  and live in their own fields; `grilled`, `architect`, and `adversary`
  appear only once the corresponding step has run.
- A round that ends in `concerns` or `blocking` records its findings (or
  their disposition) in the document body — a verdict whose findings were
  never written down cannot be honestly resolved later.
- Concerns resolved without a fresh review round keep the verdict and
  gain a resolution date — `adversary: concerns (resolved 2026-07-16)` —
  plus a body note saying what resolved them. A fresh round replaces the
  whole value as usual. A `blocking` verdict the developer closes by
  explicit adjudication instead of a fresh round takes the same form with
  its own token — `architect: blocking (adjudicated 2026-08-17)` — and
  the round's ledger record as that body note.
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
  gate — before plan-writing for a spec, before implementation for a
  plan. Accepted: a fresh round at the prescribed tier replaces the
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
  it stamps. Stamper and gate run one command, so the comparison can never
  mismatch on convention:
  `sed '1,/^---$/d' <file> | shasum | cut -c1-7`
  — `shasum` rather than `sha1sum` because stock macOS ships only the
  former, and the two produce identical digests, so a GNU-only environment
  may substitute `sha1sum` without changing a recorded hash. The field
  carries no verdict: it answers whether the document was checked after
  its last edit, and that answer is a comparison rather than a clock. A
  recomputed hash differing from the stamped one means unaudited, same-day
  edits included; any change re-arms the stamp, a typo fix included.
- A spec's consumption gate owns the recomputation: before plan-writing it
  recomputes the body hash and compares, a match meaning the standing
  stamp satisfies the gate and a mismatch firing the audit offer. Those
  are spec-gate semantics — on a plan, a permitted target on explicit
  request, the stamp is informational and goes stale silently. Staleness
  joins no Unfinished-work entry: it is a recomputation, not a grep.
- Verdict agents self-report the model they ran on (family plus version);
  the dispatcher compares it against the dispatched and prescribed
  tiers before stamping, and each round's verdict, model, and date are
  recorded in the document body. Committed examples of the bare fallback form use
  placeholders (as above) so they never match the list below.
- `branch` and `base` appear once the topic branch exists — never guessed
  up front, omitted entirely when there is no topic branch.

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

Under the heading each finding takes one line, its disposition the
leading token:

    - fixed — [<severity>] <claim>; license: <citation>; <what changed>
    - held — [<severity>] <claim>; question: <one short question>
    - open — [<severity>] <claim>
    - resolved <date> — [<severity>] <claim>; landed in <section>
    - resolved <date> (declined) — [<severity>] <claim>; <why the document stands>

- `open` — written at stamp time, before the findings are triaged. An
  `open` line surviving a session means the remediation never ran, and
  the document's next touch re-offers it.
- `fixed` — the session fixed the finding alone, licensed by a decision
  it can cite: a statement in the document itself, a glossary term or
  `_Avoid_` ban, a recorded ADR, or a previously resolved held line. The
  citation goes on the line. No citable license means the finding is
  held, and a finding that could go either way is a decision.
- `held` — the finding needs the developer. The line carries the
  concrete question, or the dispute plus the session's counter-evidence,
  phrased so one short answer resolves it.
- `resolved <date>` — closes a held line once the answer lands. The
  answer's substance goes into the document's design text; the ledger
  line points at it and never duplicates it.
  `resolved <date> (declined)` records the developer keeping the
  document as it was.

Two variants extend those shapes, and nothing else does. A contested hit
from the `propagation-auditor` agent, when it is available, takes the
held shape with `[hit]` in the severity slot, because a hit stays
ungraded even when contested. A spec whose developer accepts a
diff-scoped chain at the consumption gate gains `, chain accepted <date>`
on that round's LGTM heading: the dispatcher appends it there on the
decline, and its presence defeats the gate's re-ask, as `, waived <date>`
defeats the re-review offer.

A resolved held line is a recorded decision. When a later round re-raises
the problem it settled, the new finding is folded and cited against that
line, never asked again — state prevents relitigation, not the
reviewer's memory.

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
leg, and the review-loop ledger entry below is the one that does.

- **Grilling pending** — a session's outcomes are recorded and not yet
  applied.
  `rg -l --no-ignore --crlf '^\s*grilled: grilling' docs/`
  Owner: the grilling-session, when available.
- **Unresolved verdict** — a round ended in `concerns` or `blocking`
  and nothing closed it.
  `rg -l --no-ignore --crlf '^\s*(architect|adversary): (blocking|concerns)$' docs/`
  Owner: a fresh round at the prescribed tier, or the resolution
  annotation above.
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
- **Pending re-review** — a verdict produced below the prescribed tier,
  neither refreshed nor waived.
  `rg -l --no-ignore --crlf '^\s*(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/`
  Owner: the re-review offer at the document's consumption gate.
- **Misplaced stamp** — a process field outside the top level of the
  frontmatter, at any value.
  `rg -l --no-ignore --crlf '^\s+(grilled|architect|adversary|architect-fallback|adversary-fallback|integrity):' docs/`
  Owner: the developer; no process surface owns moving a stamp back.
  The class suppresses per field: it hides the one other class whose
  published command would match the relocated line, and no other —
  itself excluded, since its own command matches every process field.
  Match semantics are the mapping, so a class published later needs no
  extra rule.

The tail anchors are exact on purpose: a `(resolved <date>)`,
`(adjudicated <date>)` or `, waived <date>` annotation defeats the
match, and that defeat is the recorded closed state. The leading
anchors are tolerant on purpose, so a relocated field is still found.
The Misplaced stamp command anchors `^\s+` instead, because there the
indentation is the defect it looks for rather than an accident to
tolerate. Those anchors all sit on a frontmatter field; the review-loop
ledger entry anchors a leading disposition token instead, so there the
close is a rewrite — `open` or `held` becomes `resolved <date>`, and the
anchor stops matching.

## Lifecycle offers

Each an offer the developer may decline, and each made
only when the tool is available: grill a fresh spec (grilling-session);
architect-review a grilled spec (architect agent dispatch);
adversary-review a plan before implementation (plan-adversary agent
dispatch); offer the pending re-review of a fallback-recorded verdict at
its consumption gate (fresh round at the prescribed tier); and when a
spec or plan moves to `implemented` and the memory-review-session skill
is available, offer a Project memory review — released work-state notes
close, resolved entries sweep to the archive. After any
review round, relay the report to the developer, then stamp the
verdict into the document's field — this sentence and the workflow
rule's verdict-agent dispatch subsection state the same ordering and
are edited together. The order has one named exception, defined in that
subsection: a plan's diff-scoped LGTM is relayed and its round record
written, while only the frontmatter stamp waits for the confirming
full-document round.

A document's consumption gate is the backstop for its ledger: a spec
does not pass to plan-writing, nor a plan to implementation, while
`held` lines stay open — an LGTM can leave the frontmatter clean while a
decision question still pends, so the gate asks those questions at the
latest. Writing a plan from a spec is that same seam: the held spec
questions are asked before the plan is written, whoever writes it.

The process suggests committing the work's documents under `docs/` at
exactly one point — the implementation-ready gate: the developer has
approved the plan (the `status` flip to `approved`) and implementation
is about to start. During authoring — spec drafting, grilling, review
rounds, plan writing — it never makes that suggestion; the documents'
uncommitted state is deliberate, not dirt in the process-artifacts
sense, and the developer may commit sooner on their own call. The
suggestion covers only paths git tracks or would track; deliberately
ignored documents are skipped silently, and committing itself stays
with the developer.

Ticket value format, sourcing order, and backfill live in the
ticket-frontmatter rule.
