---
ticket: none
date: 2026-08-27
status: implemented
grilled: 2026-08-27
architect: LGTM
---

# Audit agents — propagation-auditor and integrity-auditor

## Problem

Two measured review loops show verdict rounds spending most of their
cost on work that is not design review. In this repo's 8-round
background-verdict-dispatch loop, three consecutive rounds of the most
capable model hand-diffed every prescribed block against the shipped
files. In a client project's 22-round cycle, 9 architect and 13
adversary rounds produced 204 findings of which zero touched the
architecture: twelve consecutive rounds traced one round's repair to
the next round's defect, and roughly one finding in ten was a counter
or boundary sentence in prose — wrong in nearly every round, twice
wrong after being explicitly "verified". Separately, the architect
reviews textual integrity without a mandate: 11 of 15 findings in the
newest measured spec round were integrity-class, while
`ARCHITECT_PERSONA.md` names none of that duty.

Nobody in the process owns two questions: *did the repair land
everywhere it had to?* and *does the churned document still hold
together as a text?* Both are policed today by the most expensive
dispatches, casually and late.

## Design

### The category

An **Audit agent** (glossary) reports no verdict and stamps nothing: it
checks a document and returns material for the dispatcher's
disposition. It is dispatched as a gate before expensive work — a clean
audit is a precondition, never a judgment on the design. Audit agents
adopt no persona and are not persona surfaces. Two ship in this spec,
split by the nature of the work: procedural checking a cheap model does
well under instruction, and judgment reading that earns the top tier.

Rejected shapes, each measured against the evidence: one agent with two
dispatch modes (tier and output contract would change per dispatch,
making the definition conditional); the mechanical agent absorbing the
judgment lenses (judgment on the cheapest family contradicts the
46-item yield the full-context, top-tier run produced); the judgment
agent absorbing the mechanical duties (the top family doing procedural
work casually is the single largest cost inefficiency both loops
measured).

### propagation-auditor

The mechanical pass. Dispatched on the **cheapest available family**,
named explicitly — the inverse of the review rule, and the point: every
duty is procedural (parse, enumerate, count, diff), which a capable
model does casually badly and a cheap model does fine when told to
derive by counting. The workflow rule's "reviews are never dispatched
on the cheapest available family" stands untouched — an audit is not a
review.

**Output: hits** (glossary) — located, binary, each carrying its
derivation. The dispatcher confirms or dismisses each hit; a confirmed
hit's fix is licensed by the derivation itself (a recounted counter, an
enumerated missed consumer decides itself), so hits never wait for the
developer. A hit the dispatching session believes is wrong escalates to
the developer — never silently dismissed. A clean audit reports one
line — the literal token `CLEAN`. The report opens with the model self-report defined for both
auditors in the integrity-auditor's tier-verification paragraph.

**Dispatch points**: before every verdict-agent dispatch, first rounds
included — authoring errors exist before any repair; after a fix wave,
before the next round (the autonomous-loop spec names this gate,
conditionally); before an integrity audit; and offered after any
multi-site edit during authoring. When the agent is not installed,
every dispatch proceeds as today.

**Duties.** Each traces to a measured finding class; the agent file
phrases them domain-neutrally, with the marketplace's instantiation
beside each:

1. **Changed interface → consumer enumeration by parsing, never text
   match.** Measured: grep missed 2 of 11 call sites of a changed
   signature; an argument-counting parse missed zero. Here: a renamed
   rule section, skill, or anchor → every cross-reference.
2. **Prescribed block versus shipped file.** Every verbatim block a
   plan dictates, diffed against the file it targets — the
   recipe-and-record class that cost three hand-diff rounds.
3. **Added field, label, or state → carrier and consumer chains.**
   Flag defined-but-never-consumed and consumed-but-never-defined.
4. **Counters re-derived, never trusted.** Every count a document
   asserts is re-derived from what the tool would print or the list
   actually holds.
5. **Cross-document identifier diff.** A name the plan uses that the
   spec never defines is reported **as a spec gap, not a plan error** —
   the invention is the symptom. Measured: one such gap survived nine
   rounds as the cycle's deepest Important.
6. **Boundary sentences.** Frontmatter citations of another document's
   verdict or counts, table row counts, review-record arithmetic.
7. **Verification simulation.** The document's own verification
   commands, run against the document's own replacement texts, before
   any reviewer reads either.

### integrity-auditor

The judgment pass — the run is an **integrity audit**. Dispatched on
the **most capable available** tier, named explicitly, in a **fresh
context**: the agent must not inherit the editing session, because the
measured cause of textual decay was a ~900-line document churned inside
a session at roughly 650k tokens, and a reviewer carrying that context
carries the blind spot with it.

The tier is verified, not assumed: the auditor's report opens with a
model self-report (family plus version), and the dispatcher compares it
against the dispatched and prescribed tiers before stamping — a
below-tier run gets no stamp and is re-dispatched. Binary on purpose:
no `*-fallback`-style record machinery, because an unstamped audit
simply re-offers itself. The propagation-auditor's report opens with
the same one-line self-report, compared against the dispatched and
prescribed rung — the cheapest available family — for its exposure
runs the other way: below the cheapest there is no rung,
but an omitted model inherits the session's model, and an over-tier
run does this procedural work casually badly, so a false clean line
would feed the integrity gate unnoticed. A mismatched run earns no
reliance and is re-dispatched at the right rung.

*Observed limitation (2026-08-29).* A live dogfood dispatched two
propagation runs under one named model — the dispatched string was
`claude-haiku-4-5-20251001` both times — and they self-reported
"haiku 4" and "claude-3-5-haiku-20241022". At the rung the comparison
held: both self-reports land on the cheapest available family, so both
runs were relied on correctly. At family plus version it did not: the
two strings disagree, and neither matches the dispatched one. A model
knows its rung more reliably than its own version, so the version half
of the comparison can fire on an otherwise correct run. The
prescription above stands unchanged — narrowing it to the rung is the
developer's call, and this paragraph records the measurement rather
than pre-empting it.

**Preconditions**: every edit from the conversation written to disk —
the deliverable is text-to-text comparison, so one unsaved decision
manufactures a run of false defects; and a clean propagation audit,
when that agent is available, so the expensive read never polices
arithmetic.

**Target and moment**: primarily a spec, offered at the consumption
gate before plan-writing — after the architect round and after its
dispositions are applied, which is where churn accumulates. A plan is a
permitted target on explicit request, not a gated one.

**Duties — two lenses**, the judgment share left after the mechanical
split:

- *The document against itself*: decisions changed in one section and
  restated in their old form in another; claims undermined elsewhere;
  unworkable sequencing; and the most portable instruction of the
  proven prompt — **verify every rule the document declares about
  itself, in both directions**.
- *Sufficiency for an implementer*: read as a careful implementer who
  must build from this text and has no other context; report
  underspecified places, and a separate section of **ranked implementer
  questions** — a good question is worth more than a weak finding.

**Output**: defects, each proved by two quotes, plus the ranked
questions — never graded, never counted as Findings. The report names
the target's line count and the highest line it cites, so a partial
read exposes itself. The report returns to the dispatcher for
disposition like any relay.

**The stamp**: the dispatcher writes
`integrity: <ISO date> (sha: <short-hash>)` into the document's
frontmatter after dispositions are applied — the date for the reader,
the hash for the check. The hash is the short SHA-1 of the document
text below the frontmatter's closing `---`, so writing the stamp never
invalidates what it stamps; the canonical recipe, shared by stamper
and gate so the comparison can never mismatch on convention, is
`sed '1,/^---$/d' <file> | shasum | cut -c1-7`. `shasum` rather than
`sha1sum` because the rule installs machine-wide and stock macOS ships
only the former; the two produce identical digests, verified, so a
GNU-only environment may substitute `sha1sum` without changing any
recorded hash. Verdict-free, because the field answers
"was this checked after the last edit" — and the answer is a
comparison, not a clock: a recomputed hash differing from the stamped
one means unaudited, exactly, same-day edits included. (A bare date
fails precisely in the churn scenario the audit exists for — this
bundle's loop spec took seven amendment waves in one day. The
precedent is Drift's rule: always a content-hash comparison, never a
version comparison.) Any change re-arms the stamp, a typo fix
included — conservative on purpose. Staleness joins no Unfinished-work
list entry: it is a recomputation, not a frontmatter grep — and the
consumption gate owns that recomputation: before plan-writing it
recomputes the body hash and compares, a match meaning the standing
stamp satisfies the gate and a mismatch meaning the audit offer fires.
Those are spec-gate semantics: on a plan — a permitted target on
explicit request — the stamp is informational and goes stale silently,
with no plan-side owner.
As a stamped process field, `integrity` joins the Misplaced-stamp
enumeration: the glossary's field list gains it now, the detecting
Unfinished-work entry at implementation.

### The paired edit — narrowing the architect's card

`ARCHITECT_PERSONA.md` narrows in the same release: the architect
reviews the design — fit, boundaries, over-engineering, alternatives —
and when a round trips over integrity-class defects it notes them in
one line and defers to the integrity audit instead of spending the
round enumerating them. Without this edit the same findings arrive from
two surfaces at the top tier, and the component pays for nothing: 11 of
15 findings in the measured round were exactly this class. Released
alone, the audit would add a fifth offer and take nothing away — the
narrowing is the other half of the feature, not a courtesy.

### Naming

Settled at the 2026-08-27 grilling, with the trail recorded:
`sweep-verifier` (the client postmortem's working name) rejected —
**sweep** in this repo's vocabulary is a mechanical `rg` command with
quoted output, which an agent is not; `coherence-auditor` rejected in
favour of **integrity-auditor**; `consistency-auditor` rejected as a
near-synonym collision with "coherence". The `*-auditor` suffix joins
the naming conventions: a verdict-free audit agent returning material
for disposition is named `*-auditor`.

## Changes by file

- `plugins/working-process/agents/propagation-auditor.md` — new; role
  inline (like plan-adversary), no persona file; `background: true`
  like every agent this plugin ships.
- `plugins/working-process/agents/integrity-auditor.md` — new; role
  inline; fresh-context and precondition duties stated in the agent
  body; `background: true`.

Both audits are background dispatches, so a gated dispatch waits for
its audit's task notification before it is issued — the gate is a
sequencing rule, not a blocking call, and it reuses the relay
machinery every other dispatch already uses.
- `plugins/working-process/ARCHITECT_PERSONA.md` — the narrowing.
- `plugins/working-process/rules/workflow.md` — the two offers (the
  integrity audit at the pre-plan consumption gate; the propagation
  audit before verdict dispatches and after multi-site edits) and the
  audit tier sentences: propagation on the cheapest available family,
  integrity on the most capable available, both named explicitly, with
  the review never-cheapest rule explicitly not applying to audits.
- `plugins/working-process/rules/spec-plan-lifecycle.md` — the
  `integrity:` field: placement, the date-plus-body-hash value, the
  canonical hash recipe verbatim (stamper and gate run the same
  command), and the recomputation semantics.
- `.claude/rules/plugin-authoring.md` — the `*-auditor` naming line.
- `docs/domain/glossary.md` — Audit agent and Hit entries (landed at
  the grilling); the Misplaced-stamp entry's field list gains
  `integrity` (landed at review round 1). The lifecycle rule's
  Misplaced-stamp detecting entry gains the field at implementation.
- Plugin README and manifest description — the identity surfaces the
  marketplace-sync rule binds.

A minor working-process version bump at release, shared with the
autonomous-review-loop spec.

## Out of scope

- The autonomous loop itself — its spec; the propagation gate is named
  conditionally in both directions.
- The propagation checklist as a distributed authoring rule (parked in
  Private memory) — the agent's duty list is self-contained; a future
  rule may mirror it for authors, never replace it.
- Seam-review checklist skills for the plan-adversary — parked
  separately; every Critical in the measured cycle lived in a seam, and
  that class belongs to the `*-plan-review` family, not to audits.
- Per-language machinery. In code repos a compiler owns duties 1–2;
  the agent file's domain-neutral phrasing lets a code project benefit
  without this spec shipping language support.

## Verification

Dogfooding on this bundle's own documents: run the propagation-auditor
over both specs before their architect rounds (cheapest family; expect
hits or a clean line — either proves the contract); run an integrity
audit on the autonomous-loop spec, this bundle's most churned document
(a restored draft plus seven amendment waves in one day), before
plan-writing; stamp `integrity:` and confirm a later edit re-arms it —
the recomputed body hash differs from the stamped one. Deferred, owner named (2026-08-29): all three architect rounds on this
spec predate the narrowing, so its first live test is owed — the
developer owns it, on the next architect round after release. The
sentence below states what that round should show.

The architect round on this spec doubles as the narrowing's
first live test: its report should defer integrity-class observations
rather than enumerate them.

## Review rounds

### 2026-08-27 — architect, fable 5, concerns (round 1, full-document)

- fixed — [Important] the tier the integrity audit depends on was asserted but unverifiable at stamp time; license: the lifecycle rule's model self-report convention plus this spec's own tier argument; the auditor self-reports, the dispatcher compares, a below-tier run gets no stamp
- fixed — [Minor] `integrity:` extended the Misplaced-stamp enumeration without touching it; license: the glossary's closed Misplaced-stamp field list plus this spec's own duty-5 class; the field list gains `integrity`, the detecting entry at implementation
- fixed — [Minor] the staleness recomputation had no named owner; license: this spec's own consumption-gate design; the gate recomputes the body hash and compares before the offer fires

### 2026-08-27 — architect, fable 5, concerns (round 2, diff-scoped)

- fixed — [Important] the tier guard covered only the below-tier direction while the propagation-auditor's exposure runs above (an over-tier run can return a false clean line the integrity gate silently relies on); license: the workflow rule's "in both directions" warning plus this spec's own casually-badly evidence; the propagation report opens with the same self-report, compared against the cheapest family
- fixed — [Minor] the recomputation owner was named only for the spec target while a plan may carry the stamp; license: this spec's own permitted-target sentence plus the sibling spec's no-gated-audit clause; scoped to spec-gate semantics, a plan's stamp informational and stale silently
- fixed — [Minor] "It joins no Unfinished-work list entry" contradicted the Misplaced-stamp detecting entry four lines later; license: the two sentences themselves; scoped to "Staleness joins no Unfinished-work list entry"

### 2026-08-27 — architect, fable 5, LGTM (round 3, diff-scoped)

- fixed — [Minor] the propagation comparison target named an absolute family where the mirrored mechanism compares dispatched against prescribed; license: the glossary's Tier entry (a rung resolves at dispatch time); the sentence now mirrors the integrity wording
- fixed — [Minor] the propagation-auditor's self-report duty lived only under the integrity-auditor heading; license: this spec's own tier-verification paragraph defining the duty for both auditors; the propagation Output paragraph now points at it
