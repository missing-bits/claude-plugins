---
ticket: none
date: 2026-09-07
status: implemented
revises: ./2026-08-27-audit-agents-design.md
branch: feature/audit-errata
base: develop
---

# Auditor self-report errata — the CLEAN contract and the rung narrowing

Wave three, package A. Two corrections to the audit agents, both licensed
by measurements the audit-agents design already recorded, and one of them
by a decision that design explicitly left to the developer.

## The measurement that prompted it

Five `propagation-auditor` dispatches across the wave-two review loop
(2026-09-02), every one on `claude-haiku-4-5-20251001`, every one asked
for the model self-report its card mandates. **All five omitted it.**
Emphasis escalated and changed nothing: the second brief called the
requirement mandatory and named the first omission as its reason; the
third asked plainly and got back the single word `CLEAN`.

The first diagnosis — move the duty into the agent card — was wrong, and
reading the card is what disproved it. The duty was already there twice:
a section explaining the reasoning, and an output template opening the
`## Output` section. An instruction present in the card *and* in every
brief was dropped anyway, which rules out placement and repetition as
the lever.

## Defect 1: an early-exit path that swallows the self-report

`propagation-auditor.md` told the agent to open with the self-report and
then said a clean audit "reports one line and nothing else". The second
sentence reads as governing the whole report. **All five omissions were
clean runs**, and the third returned literally one line — exactly what
the absolute reading prescribes.

The defect originates in the design, not the card: the audit-agents spec
says "A clean audit reports one line — the literal token `CLEAN`" and
then, in the next sentence, "The report opens with the model
self-report". The card implemented the spec faithfully.

**Fixed** by counting the self-report into the clean report: a clean
audit runs to exactly two lines, and the instruction to add nothing is
scoped to what follows the token.

`integrity-auditor.md` carries a second, unmeasured instance of the same
class — "say so in one line and stop" on the unmet-precondition path.
Fixed the same way. Repairing one instance of a mechanical fault and
leaving its sibling is the failure this branch measured five times over
in a different class, so the class is closed rather than the instance.

## Defect 2: a self-report finer than its consumer, and unreliable

Both auditor cards asked for "family plus version". The workflow rule
compares "against the dispatched and the prescribed rung" — the family.
The version was therefore precision the consumer never read, and the
audit-agents design had already measured it as untrustworthy: two runs
under one identical dispatched string reported "haiku 4" and
"claude-3-5-haiku-20241022", the second a different model entirely.

That design recorded the measurement and stopped there, in its own words:
"The prescription above stands unchanged — narrowing it to the rung is
the developer's call, and this paragraph records the measurement rather
than pre-empting it." **The developer made that call on 2026-09-07.**

**Fixed** in both cards, prose and output template: report the family
alone, with the reason stated where the instruction lives.

## Deliberately out of scope

Verdict agents keep "family plus version". Four sites still carry it —
the lifecycle rule, `architect.md`, `plan-adversary.md`, and the README —
and the measurement covers propagation runs only. Narrowing a verdict
agent's self-report is a separate question with separate evidence, and
folding it in here would be the un-specced change riding along with a
specced one that this branch's own review rounds flagged twice.

The README's generic "Agents self-report" became false the moment the
auditors narrowed, so it now names both cases: verdict agents report
family plus version, the audit agents report the family.

## The prediction, and its confirmation

Package A shipped a falsifiable claim, which is why it went first: **a
clean propagation run should now return two lines rather than one.**

**Confirmed 2026-09-07.** The first gate dispatched after the fix — a
propagation audit over this errata's own change set, which the Process
section below records as previously ungated — returned:

    model: haiku

    CLEAN

Two lines. The brief deliberately **did not ask for the self-report**, so
the line came from the card alone; and it names the family without a
version, which is the narrowing this errata also made. One observation
confirms both halves.

The contrast is the evidence: five dispatches before the fix, every one
clean, every one omitting the self-report, several of them asking for it
in the brief emphatically. One dispatch after the fix, clean, self-report
present, brief silent. Emphasis never moved it; the card did.

One confound remains stated rather than hidden. This branch still has no
non-CLEAN propagation run, so "clean" and "omitted" never varied
independently before the fix — the pre-fix correlation was perfect and
unisolated, and the post-fix run is a single observation. The mechanism
is now the best-supported explanation rather than a proven one.
`integrity-auditor` has no clean path and was never implicated; its
unmet-precondition path, fixed here as the same class, remains
unmeasured.

## Process

No verdict round ran. The verdict and audit agents were unavailable in
the session that made these edits, so the propagation gate that normally
precedes a dispatch could not run either — including over this errata.
The changes are three files, and each carries its rationale beside the
text it governs; an architect round remains worth offering.

**The gate ran on 2026-09-07** once the agents returned, over this
errata's own change set, and returned CLEAN across four classes:
consumers left behind, internal contradictions, claim fidelity in this
document, and recomputed counters. That closes the gate debt above and
supplied the confirmation recorded in the previous section.
