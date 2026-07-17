---
ticket: none
date: 2026-07-16
status: approved
grilled: 2026-07-17
architect: LGTM
branch: feature/model-selection-guidance
base: master
---

# Model-selection dispatch guidance for working-process review agents

## Problem

The working-process plugin ships two review agents — architect and
plan-adversary — whose verdicts gate the spec/plan lifecycle. The model
they run on is chosen by the dispatching session, and today nothing
guides that choice: an omitted model inherits the session's model, so a
session running on a cheap model silently drags its architect down with
it, and a session on the most capable model spends top-tier quota on a
three-line mechanical plan review.

Superpowers solves this for its implementer/reviewer dispatches with a
"Model Selection" section in the subagent-driven-development skill:
tiered heuristics, an explicit model on every dispatch, and an
escalation path. Working-process needs the equivalent for its own two
agents — and, because its verdicts are durable frontmatter stamps, it
additionally needs to handle the case where the prescribed tier is
unavailable (subscription cap) and a verdict is produced on a lower one.

## Scope

Guidance covers ONLY the plugin's own review agents: architect and
plan-adversary. General dispatch guidance for implementers, researchers,
and other subagents stays with superpowers' Model Selection section —
this spec neither duplicates nor overrides it.

## Verified platform facts

Doc-verified (Claude Code docs, July 2026):

- A session cannot query remaining model quota. `/usage` renders only in
  the UI; statusline JSON carries 5-hour/7-day used-percentage fields but
  only for the statusline script, with no back-channel to the model;
  hook inputs carry no usage fields; OTEL metrics are post-hoc exports.
- When a subscription hits a model-specific cap, requests on that model
  block with no auto-fallback; the developer recovers manually (switches
  model or waits for the reset). Subagent-dispatch behavior on a cap is
  undocumented — assume the dispatch fails rather than silently degrades.
- Subagent frontmatter supports `model:` (family alias, full model ID,
  or `inherit`; default `inherit`), and the dispatch-time model parameter
  overrides it. The agent `description:` is loaded into every session as
  the delegation-selection surface.

Consequences: proactive budget management is impossible; the only honest
mechanisms are an explicit model at dispatch, a reactive protocol when a
dispatch is refused on a cap, and a durable record when a verdict was
produced below the prescribed tier.

## Design

### Tier heuristic

Stated in abstract, relational tier language; committed guidance never
names concrete models, and any alias enumeration in examples is
illustrative — tiers resolve at dispatch time against the platform's
current family ladder (ordered cheapest to most capable). Definitions:

- **most capable available** — the top family of the current ladder
  (the harness's `best` alias resolves to it);
- **mid tier** — one family below the most capable available;
- **floor** — a review is never dispatched on the cheapest available
  family; at the floor the only offer is to wait for the cap reset (a
  verdict a silent substitution nevertheless produces there is a
  degraded verdict like any other — the process never invalidates it);
- **cap drop** — one family down the current ladder, once.

The heuristic:

- **architect** — always the most capable available model. Design review
  is an architecture task; it is also the process's most consequential
  gate, so it is never economized.
- **plan-adversary** — scaled to the plan's size, complexity, and risk:
  the most capable model for complex or risky plans, the mid tier for
  small mechanical ones.
- **The model is always specified explicitly at dispatch.** An omitted
  model inherits the session's model, which defeats the heuristic in
  both directions.

### Carriers

The decision is made by the dispatcher before the agent loads, so the
guidance must be visible in the dispatching session:

1. **Agent `description:` one-liners** — reach every session that has
   the plugin, without any rules install:
   - architect: "Dispatch on the most capable available model."
   - plan-adversary: "Dispatch on a model scaled to the plan's size and
     risk — most capable for complex or risky plans, one family below it
     for small mechanical ones; never the cheapest family."
   The description stays a directive of one sentence; the full protocol
   does not belong on the delegation-selection surface.
2. **`rules/workflow.md` steps 3 and 5** — the heuristic sentence at
   each dispatch offer, plus a shared short paragraph with the cap
   protocol (below).
3. **`rules/spec-plan-lifecycle.md`** — owns the frontmatter grammar,
   so the fallback field, its grep line, and the re-review offer
   semantics land there (see next sections).

### Cap protocol (reactive fallback)

When a dispatch is refused because the dispatched model's cap is hit —
and only then; any other dispatch failure is an ordinary error, not a
fallback trigger — the session asks the developer: **drop one tier or
wait for the reset**. Never both silently. Two independent constraints
bound the drop: it happens at most once (the cap-drop definition), and
it never lands on the cheapest family (the floor). When either blocks
it, the only offer is to wait.

### Dispatch verification

Subagent behavior when the dispatched model is capped is undocumented
(see Verified platform facts), and the cap protocol must not rest on an
assumption it cannot check. Each review agent therefore states the model
it actually ran on at the top of its report, and the dispatcher compares
that against the dispatched and prescribed tiers before stamping. A
verdict produced below the prescribed tier is a fallback event — fallback
field and re-review offer included — however it came about: a platform
substitution or a deliberate under-dispatch (every step is an offer,
economizing included). The self-report comparison is the detection
channel, not the definition: a silent substitution that stays at or
above the prescribed tier (possible when the dispatch was deliberately
above the heuristic) is no fallback event and gets no record. The token
in the record follows agency: `chosen` when the developer deliberately
chose the under-dispatch before any refusal, `degraded` otherwise (see
"Fallback record").

### Round provenance

Every review round leaves a note in the document body (the findings
sections already carry them), and each note records the verdict, the
model that produced it as **family plus version** (taken from the
agent's self-report, e.g. "opus 4.8"), and the date. This is the
document's audit trail across model generations: families alone hide
the difference between successive versions of the same family, and a
future developer deciding whether an old verdict deserves a fresh look
needs to know both what reviewed it and when. The frontmatter stays a
signal surface — verdict and fallback event only — while the body
carries the history.

### Fallback record

A verdict produced below the prescribed tier gets a companion frontmatter
field next to the untouched verdict field:

```yaml
architect: LGTM
architect-fallback: <model> (degraded <date>)
```

(`adversary-fallback:` for the plan-adversary.) Value grammar: the
platform's family alias of the model that produced the verdict, then
`(degraded <ISO date>)` or `(chosen <ISO date>)`. The two tokens split
by agency, not by mechanics:

- `degraded` — anything other than the developer's deliberate choice: a
  cap refusal (including a developer-consented one-tier drop after it —
  the cause is the refusal, not the consent), a silent platform
  substitution, or an under-dispatch the dispatcher did not knowingly
  decide (e.g. an accidentally inherited session model). The token
  deliberately does not claim which cause — the dispatcher cannot
  always know.
- `chosen` — the developer deliberately dispatched below the prescribed
  tier before any platform refusal (economizing is a legitimate offer
  to decline).

Committed documentation examples of the bare form
use placeholders, as above — a verbatim-matchable example at column 0
anywhere under `docs/` would be a permanent false positive for the
pending-re-review grep below.

- The verdict field keeps its existing grammar — `LGTM | concerns |
  blocking` plus the resolved-concerns annotation — so the lifecycle
  rule's anchored greps keep working unchanged.
- The fallback field records a *below-prescribed-tier event*, not
  routine provenance. A plan-adversary run deliberately dispatched on
  the mid tier per the heuristic gets no fallback field — a dispatch at
  the prescribed tier and a verdict below it are different facts, and
  only the second one calls for a record.
- The field's presence is the greppable "re-review pending" marker,
  for both tokens alike:
  `rg -l '^(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/`
- A fresh review round at the prescribed tier replaces the verdict field
  as usual and **removes** the fallback field. A declined re-review
  offer keeps the field and gains a waiver date —
  `architect-fallback: sonnet (degraded 2026-07-16, waived 2026-07-17)` —
  which the anchored grep deliberately skips, mirroring the
  resolved-concerns annotation pattern.

Family aliases (illustrative today: `haiku`, `sonnet`, `opus`, `fable`)
are acceptable in fallback records and dispatch mechanics — they are the
platform's own stable tier vocabulary, and a record of what happened is
history, not prescription. Committed guidance prose stays abstract.
Body round notes go one step finer — family plus version (see "Round
provenance") — but raw platform model IDs stay out of committed text
everywhere: family plus version carries the same information readably.

### Re-review offer

A fallback-recorded verdict — degraded or chosen — is a full verdict;
the process never invalidates it. Instead, in the plugin's "every step
is an offer" spirit, the workflow OFFERS a re-review on the prescribed
tier once one matters. Both tokens carry the offer: a forced constraint
may have lifted (a cap resets), and a deliberate economization may be
worth revisiting once the document is about to be relied on.

- **Which verdicts**: every fallback-recorded verdict that would
  otherwise end the review cycle — an `LGTM` immediately, and
  `concerns` at the moment they are resolved *without* a fresh round
  (the resolved-concerns path makes them exactly as terminal as an
  LGTM). Unresolved `concerns`/`blocking` need no offer: the follow-up
  round they force dispatches at the originally prescribed tier, and
  that round is the upgrade.
- **When it fires**: at the document's next consumption gate — before
  workflow step 4 (writing the plan) for a fallback-recorded spec
  verdict, before step 6 (implementation) for a fallback-recorded plan
  verdict. One prompt, at
  the moment the verdict is about to be relied on; never a session-start
  nag. The durable carrier across sessions is the fallback field itself.
- **When it dies**: accepting it runs a fresh round at the prescribed
  tier (replacing verdict, removing the field); declining it stamps the
  waiver date; and moving `status` to `implemented` with the field still
  bare stamps `waived <date>` as part of the move — expiry is
  representable in the grammar, so a bypassed gate cannot leave a
  forever-pending grep hit. An accepted re-review refused on a
  still-standing cap re-enters the cap protocol; when the fresh round is
  itself degraded, it replaces the verdict, refreshes the fallback field
  with the new date, and the offer re-arms at the same gate.

### Downgrade after approval

A prescribed-tier re-review may overturn a fallback-recorded LGTM after the
document already moved forward (spec approved, plan in flight). That is
the mechanism succeeding, not churn: the fresh verdict replaces the
field as usual, `status` stays forward-only and stands, the findings
land in the document body, and their disposition is decided like any
concerns round against work already in flight.

### Alternative considered: agent frontmatter `model:`

The harness's first-class mechanism — `model:` in the agent's own
frontmatter, overridable at dispatch — could pin the architect
mechanically. Rejected: the plan-adversary's scaling heuristic is
inexpressible in a static field, a hard default complicates the cap
dialogue (the dispatch would fail before the session can offer the
choice), and prose keeps the two agents symmetric. The frontmatter
default stays `inherit`; the prose directive's real job is preventing a
cheap main session from silently dragging the review down with it.

## Changes by file

- `plugins/working-process/agents/architect.md` — dispatch directive
  sentence in `description:`; report format gains a model self-report
  line at the top — family plus version (dispatch verification, round
  provenance).
- `plugins/working-process/agents/plan-adversary.md` — dispatch
  directive sentence in `description:`; same model self-report (family
  plus version) in the output format.
- `plugins/working-process/rules/workflow.md` — heuristic sentences in
  steps 3 and 5; short cap-protocol paragraph (drop-one-tier-or-wait,
  floor, explicit model, fallback field pointer).
- `plugins/working-process/rules/spec-plan-lifecycle.md` — fallback
  field in the frontmatter example and value grammar (both tokens:
  `degraded` unchosen — forced or unnoticed / `chosen` deliberate);
  fallback and waiver
  semantics (including waiver-on-`implemented`); re-review offer in the
  lifecycle-offers paragraph (firing gates, expiry, both tokens); round
  provenance note (round notes record verdict, model family plus
  version, date); new grep line for pending re-reviews, with the note
  that committed examples of the field must not verbatim-match it.
- `plugins/working-process/README.md` — document the new convention.
- `plugins/working-process/.claude-plugin/plugin.json` — minor version
  bump (pre-1.0 convention change rides a minor per the versioning
  rule). The next minor is claimed by the in-flight review-reports spec;
  this work takes whichever minor is free at merge time.

Delivery to installed copies rides the usual path: the rules-payload
change bumps the plugin version, and sync-rules picks up the drift.

## Out of scope

- Model guidance for any dispatch other than the two review agents
  (superpowers owns the general case).
- Proactive quota budgeting or developer-declared budgets — nothing to
  measure against (see Verified platform facts); revisit only if the
  platform exposes quota to sessions.
- Auto-retry or scheduled re-dispatch after a cap reset — reset times
  are not observable from a session.

## Architect findings (pre-spec standalone consultation, 2026-07-16)

The design direction was put to the architect agent as a standalone
question before this spec was written; verdict on the direction:
`blocking` — one Critical, three Important, all specifiable fixes. All
are applied in this spec:

1. **Critical — in-verdict provenance broke the lifecycle grammar.** The
   draft protocol stamped the model inside the verdict value
   (`architect: concerns (opus)`), silently breaking
   spec-plan-lifecycle's value grammar and anchored grep contract.
   Disposition: separate optional `*-fallback:` field; verdict grammar
   and greps untouched; the lifecycle rule change ships in the same
   version bump ("Degradation record", "Changes by file").
2. **Important — record the degradation event, not routine
   provenance.** A deliberate mid-tier adversary run and a cap-forced
   one were indistinguishable. Disposition: fallback field exists only
   on cap-forced degradation ("Degradation record").
3. **Important — offer lifecycle undefined.** Cap resets happen in
   other sessions; without a durable marker and defined firing gates the
   offer evaporates or nags. Disposition: field as carrier, consumption
   gates as firing points, expiry at `implemented` ("Re-review offer").
4. **Important — downgrade-after-approval undefined against
   forward-only `status`.** Disposition: specced ("Downgrade after
   approval").
5. **Minor — naming constraint self-contradictory.** Disposition:
   three-level rule — abstract prose, family aliases in records and
   mechanics, full model IDs banned ("Degradation record").
6. **Minor — frontmatter `model:` alternative unweighed.** Disposition:
   weighed and rejected with reasons ("Alternative considered").
7. **Minor — fallback unbounded, trigger unspecified.** Disposition:
   mid-tier floor for both agents; only cap errors trigger the protocol
   ("Tier heuristic", "Cap protocol").

The architect also recommended that "tier", "fallback", and "degraded
verdict" enter `docs/domain/glossary.md` during the grilling step —
deferred to grilling, where glossary changes belong.

## Architect findings (formal review round 1, 2026-07-16)

Verdict: `blocking` — two Important, two Minor. The disposition check
confirmed all seven pre-spec findings genuinely applied. All four
findings below were applied to this spec on 2026-07-16 (developer
decision on the mid-tier ambiguity: mid tier = one family below the most
capable available); a verification round follows.

1. **Important — tier ladder written for three families, platform ships
   four.** The alias enumeration (`opus`, `sonnet`, `haiku`) and the
   degradation example's one-step drop assume a 3-rung ladder;
   doc-verified aliases are `haiku`, `sonnet`, `opus`, `fable` plus
   `best`, making "the mid tier" ambiguous. Disposition: applied —
   relational definitions in "Tier heuristic" (mid tier = one family
   below the most capable available; floor = never the cheapest
   available family; cap drop = one family down, once); alias
   enumerations marked illustrative; the plan-adversary description
   one-liner reworded to match.
2. **Important — cap protocol trusts undocumented dispatch-on-cap
   behavior with no way to notice if it is wrong.** If a capped
   dispatch ever silently degrades instead of failing, the fallback
   field never gets written. Disposition: applied — new "Dispatch
   verification" section (model self-report line in both agents'
   reports; dispatcher compares before stamping; mismatch = cap-forced
   degradation); agent-file changes extended accordingly.
3. **Minor — the spec's own YAML example is a permanent false positive
   for the pending-re-review grep it defines.** Disposition: applied —
   placeholder form in the example, non-matchability requirement stated
   in "Degradation record" and in the lifecycle-rule change item.
4. **Minor — offer expiry at `implemented` has no grammar
   representation**, leaving a forever-pending grep hit when gates were
   bypassed. Disposition: applied — moving `status` to `implemented`
   with a bare fallback field stamps `waived <date>` ("Re-review
   offer").

## Architect findings (verification round 2, 2026-07-16)

Verdict: `concerns` — one Important, two Minor. All four round-1
dispositions verified as genuinely applied; the reviewing agent
self-reported its model (most capable available, no degradation) per
this spec's own dispatch-verification convention. All three findings
resolved in the spec text on 2026-07-16 without a fresh round:

1. **Important — "Dispatch verification" and "Degradation record"
   define two different triggers for the fallback field.** Verification
   stamped on any mismatch against the dispatched tier; the record
   exists only for verdicts below the prescribed tier — an upward
   substitution would have earned a degradation record and a downward
   re-review offer. Disposition: applied — trigger qualified to a
   mismatch below the dispatched tier; upward substitution explicitly
   gets no record ("Dispatch verification").
2. **Minor — cap protocol conflated the fallback tier with the floor**
   (a 3-family-ladder residue) inviting a drop-until-floor misreading.
   Disposition: applied — the two constraints stated independently: at
   most one drop, never onto the cheapest family ("Cap protocol").
3. **Minor — `(capped <date>)` hard-coded a cause the dispatcher cannot
   always know** (the platform documents non-cap silent substitutions).
   Disposition: applied — developer chose the cause-neutral token
   `(degraded <date>)`; grammar, examples, and grep updated, with a
   cause-neutrality note in "Degradation record".

## Architect findings (post-grilling round 3, 2026-07-16)

Verdict: `LGTM` — no findings. All round-2 resolutions verified as
applied; glossary conformance confirmed against the four terms added by
the grilling session (no `_Avoid_` bans violated, canonical senses
respected); the two-anchor composition (cap protocol anchored on the
prescribed tier, dispatch verification on the dispatched tier) verified
as deliberate and correct, since dispatched never exceeds prescribed.

Provenance: this round is itself the first live instance of this spec's
cap protocol — the prescribed top-family dispatch was refused on a
spend cap, the developer chose the one-family drop, and the reviewing
agent self-reported the fallback model per the dispatch-verification
convention. Hence the `architect-fallback` field this document carried
until round 4; the re-review offer fired at the consumption gate before
plan-writing and was accepted.

## Architect findings (re-review round 4 at the prescribed tier, 2026-07-17)

Verdict: `concerns` — one Important, two Minor. This prescribed-tier
round replaced the degraded round-3 LGTM and removed the
`architect-fallback:` field — the re-review mechanism working as
designed ("Downgrade after approval": the fresh verdict replaces the
field; findings land here). All round-1/2 dispositions and glossary
conformance re-verified as holding. All three findings applied to this
spec on 2026-07-17:

1. **Important — the degradation trigger contradicts the glossary's
   prescribed-tier anchor when a dispatch exceeds the prescribed
   tier.** A developer may deliberately dispatch above the heuristic
   (every step is an offer); a silent downward substitution to exactly
   the prescribed tier would then trip "Dispatch verification" (anchored
   on the dispatched tier) while "Degradation record" and the glossary
   (anchored on the prescribed tier) say no degradation happened.
   Disposition: applied — "Dispatch verification" now anchors the
   record on the prescribed tier (the record exists iff the verdict is
   below it) and names the self-report comparison as the detection
   channel, not the definition; the over-dispatch case explicitly gets
   no record.
2. **Minor — the floor is phrased as a production guarantee the
   verification path contradicts.** A silent substitution onto the
   cheapest family still yields a full (degraded) verdict. Disposition:
   applied — the floor definition now constrains dispatch, with the
   never-invalidate consequence stated inline ("Tier heuristic").
3. **Minor — an accepted re-review refused on a still-standing cap is
   unstated.** Disposition: applied — "Re-review offer" now states the
   recursive case: re-entry into the cap protocol, a degraded fresh
   round replaces the verdict and refreshes the field with the new
   date, and the offer re-arms at the same gate.

## Architect findings (verification round 5, 2026-07-17)

Verdict: `concerns` — one Minor. All three round-4 dispositions
verified as applied; prescribed-tier anchoring confirmed consistent
across the heuristic, record, glossary, offer, and verification;
platform facts re-verified against current docs.

1. **Minor — the cap-protocol trigger still said "the prescribed
   model's cap"**, the last surviving site of the dispatched=prescribed
   assumption round 4 removed elsewhere: a cap refusal on a deliberately
   over-dispatched model would literally classify as "an ordinary
   error" with no recovery path. Disposition: applied — the trigger now
   reads "the dispatched model's cap" ("Cap protocol"); the surrounding
   constraints already compose safely for the over-dispatch quadrant (a
   one-tier drop lands at or above the prescribed tier, so no
   degradation record results).

## Architect findings (verification round 6, 2026-07-17)

Verdict: `concerns` — one Minor. Round-5 disposition verified as
applied; prescribed-tier anchoring confirmed consistent across all six
sites; greps and glossary conformance clean.

1. **Minor — the deliberate under-dispatch quadrant was narrated as
   platform-forced.** A developer may deliberately dispatch below the
   prescribed tier; the iff rule correctly fires the record and offer,
   but "forced degradation … whatever the platform did" (and the
   glossary's "substitution" phrasing) claimed a cause that case lacks.
   Disposition: applied — "Dispatch verification" reworded
   cause-neutrally (platform substitution or deliberate
   under-dispatch), and the glossary's Degraded-verdict entry widened
   accordingly (an inline grilling touch, per the architect's routing
   suggestion).

## Architect findings (verification round 7, 2026-07-17)

Verdict: `concerns` — one Minor. Round-6 disposition verified as
applied and consistent (spec and glossary agree); prescribed-tier
anchoring re-confirmed across all six sites; grep hygiene holds.

1. **Minor — one "Degradation record" bullet still carries the
   pre-round-6 cause-anchored dichotomy**: "deliberate tier choice and
   cap-forced tier are different facts, and only the second one calls
   for a re-review" — false under the widened definition (a deliberate
   under-dispatch below the prescribed tier also gets the field and the
   offer); an implementer transcribing the bullet into the lifecycle
   rule could encode "cap-forced only". Suggested fix: re-anchor on the
   tier — "a dispatch at the prescribed tier and a verdict below it are
   different facts, and only the second one calls for a re-review."
   Disposition: applied via the developer's two-token amendment of
   2026-07-17 — the bullet is re-anchored on the tier, and the cause
   distinction moved into the token grammar (`degraded` forced /
   `chosen` deliberate, both carrying the re-review offer); the same
   amendment added the "Round provenance" convention (round notes
   record verdict, model family plus version, date).

## Architect findings (verification round 8, 2026-07-17)

Verdict: `concerns` (fable 5, 2026-07-17) — two Minor, purely lexical.
The two-token amendment verified as internally consistent (token split
by agency incl. the consented-drop case, both-token offer and grep,
round provenance vs the naming rule, spec ↔ glossary agreement); no
`_Avoid_` bans violated. Both findings applied 2026-07-17:

1. **Minor — the old wide "degraded" survived as the umbrella word at
   four live sites** where both tokens apply (dispatch-verification
   definition, firing gates, downgrade-after-approval, the carriers
   pointer), though the glossary no longer supports the wide sense.
   Disposition: applied — swept to the glossary's umbrella ("fallback
   event", "fallback-recorded verdict", "the fallback field"); the
   "Degradation record" section renamed "Fallback record" with its live
   references updated (historical findings sections keep the old name
   as history).
2. **Minor — the glossary's Consumption-gate entry still said the offer
   fires on "degraded" verdicts**, contradicting the Chosen entry.
   Disposition: applied — "fallback-recorded verdicts" (inline grilling
   touch).

## Architect verdict (verification round 9, 2026-07-17)

`LGTM` (fable 5, 2026-07-17) — no findings. The round-8 sweep verified
complete: the wide "degraded" survives nowhere in normative text (the
remaining occurrences are the narrow token, token enumerations, or
platform mechanics), spec and glossary agree word-for-sense, greps hold
with the example forms triple-protected, and round provenance is
honored from round 8 onward. The design is ready for the
implementation plan.

## Architect findings (post-delta-grilling round 10, 2026-07-17)

Verdict: `concerns` (fable 5, 2026-07-17) — three Minor, all summary
sites lagging the delta-grilled token recut (`chosen` = deliberate
unforced pre-refusal choice; `degraded` = default bucket incl.
unnoticed under-dispatch); the definitional core verified correct and
consistent, no earlier-round regression. All three applied 2026-07-17:

1. **Minor — the "Changes by file" token gloss said "`degraded` forced
   / `chosen` deliberate"**, false for degraded's new breadth.
   Disposition: applied — "`degraded` unchosen — forced or unnoticed /
   `chosen` deliberate", mirroring the glossary.
2. **Minor — the "Dispatch verification" token sentence, read alone,
   mis-tokened the consented cap drop** (also a deliberate choice).
   Disposition: applied — "deliberately chose the under-dispatch before
   any refusal".
3. **Minor — the glossary's Fallback-record entry dropped the
   prescribed-tier qualifier from the removal rule**, breaking the
   re-arm mechanism on a plain reading. Disposition: applied — "a fresh
   prescribed-tier round removes it (a degraded one refreshes it), a
   waiver annotates it" (inline grilling touch).

## Architect verdict (verification round 11, 2026-07-17)

`LGTM` (fable 5, 2026-07-17) — no findings. All three round-10
dispositions verified as applied and word-for-sense consistent with the
definitional core; no new drift; grep contract and round provenance
hold. Ready for the implementation plan.
