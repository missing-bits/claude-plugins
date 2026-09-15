---
ticket: none
date: 2026-08-29
agent: integrity-auditor
model: claude-opus-5
target: ../specs/2026-08-17-autonomous-review-loop-design.md
coverage: 429/429
---

# Integrity audit — the autonomous review loop spec

An `integrity-auditor` dispatch read
`docs/specs/2026-08-17-autonomous-review-loop-design.md` on a fresh
context and returned eleven defects and ten ranked implementer
questions at full coverage. The spec had already closed five architect
rounds, and the plan implementing it had closed thirteen plan-adversary
rounds. The audit therefore measures what a closed review loop leaves
behind, which is the claim the two-lens fresh-context design rests on.

This file is the report's home. The report lived only in the
dispatching session's transcript, so `process-status` read the repo
clean while nine of the eleven defects waited on a decision.

## Provenance

The dispatch disabled the installed `working-process` plugin and ran
the unreleased agent from the working tree:

```
claude -p --plugin-dir plugins/working-process --agent integrity-auditor \
  --model opus \
  "Audit target: docs/specs/2026-08-17-autonomous-review-loop-design.md — this
   bundle's most churned document (a restored draft plus five architect rounds
   and thirteen plan-adversary waves in two days). Its sibling is
   docs/specs/2026-08-27-audit-agents-design.md; the shipped surfaces are under
   plugins/working-process/. Run both lenses and report."
```

- Ran 2026-08-29 at 14:22 UTC on branch `feature/review-loop-audits`,
  working tree clean.
- The same run's `propagation-auditor` returned CLEAN on the sibling
  spec and one contested hit, verified false, on the target.
- The dispatched string records what ran. The agent's self-report holds
  at the rung and fails at the version, so it settles nothing finer.
- Local transcript: session `60d835b8-2000-46ad-9e24-81abca81b4d6`.

## Dispositions

The auditor clustered the eleven defects into five decisions. The
release applied D and E in `a998161`, which edited the spec and the
glossary. A, B and C stay open — they are design questions the audit
raised, not defects the release carries.

| # | Defect, in the order reported below | Cluster | State |
|---|---|---|---|
| 1 | `resolved <date>` closes a `held` line the document never writes | A | open |
| 2 | `blocking` rounds record `fixed`, which the same section forbids | A | open |
| 3 | The propagation gate raises a held line after the only delivery moment | C | fixed on `feature/audit-errata` |
| 4 | The all-Minor signal prescribes fixing by grade | B | fixed on `feature/audit-errata` |
| 5 | `concerns (resolved <date>)` is autonomous in one passage, offered in the next | B | fixed on `feature/audit-errata` |
| 6 | `held` carries no slot for the counter-evidence two passages require | A | slot landed on `feature/audit-errata`; the fuller `held` contract stays open |
| 7 | The closed grammar carries no deviation marker | A | open |
| 8 | The confirming round's durable marker has no anchor and no command | D | applied in `a998161` |
| 9 | The new Unfinished-work class contradicts a recorded property of the list | E | applied in `a998161` |
| 10 | The reviewer's stop signal covers all-Minor rounds only | B | fixed on `feature/audit-errata` |
| 11 | `resolved (declined)` appears in two forms | A | open |

The three open clusters read: **A** — the ledger grammar does not cover
what the loop does, five defects. **B** — three termination passages
contradict Triage and each other, three defects. **C** — the gate breaks
the one-interruption contract, one defect.

Four of the ten questions remain spec gaps rather than reading errors:
1, 2, 3 and 5. Question 1 closed with the errata below; 2, 3 and 5 stay
open.

Wave one landed on `feature/audit-errata`: all three B defects, the C
defect, the `counter:` slot of defect 6, and question 1's answer — the
previous round's `fixed` lines and their `<what changed>` clauses are
what a diff-scoped brief is taken against. Dropping the `[hit]` ledger
variant narrows a published convention, so the release carrying it is a
minor bump. Cluster A's remaining five defects belong to a follow-up
spec that treats the ledger as loop state.

## The report

Verbatim, as returned.

---

Preconditions: working tree is clean (`git status --porcelain` empty), so every conversation edit is on disk. The brief does not state a propagation-audit result; nothing in it reports hits, so I proceeded rather than stopping.

---

model: claude opus 5

---

## Defects

**"The disposition ledger", ledger grammar vs. `## Review rounds` — the `resolved <date>` token is defined for one state and used for another, leaving `fixed` and `resolved` interchangeable with no stated rule.**
  quote A: "`resolved <date>` — closes a held line once the answer lands. The answer's substance goes into the document's design text; the ledger line points at it and never duplicates it."
  quote B: "- resolved 2026-08-27 — [Important] the ledger anchors joined the Unfinished-work list whose shipped invariant counts frontmatter hits only; landed in "The disposition ledger" (section-scoped match semantics, hardened command, one entry naming both owners)"
  *(No `held` line exists anywhere in the document, so no `resolved` line can be closing one; round 2 then carries `fixed` and `resolved 2026-08-27` side by side for the same class of session-applied fix.)*

**"Termination" vs. `## Review rounds` — the grammar has no token for a developer-directed fix, so the document's own `blocking` rounds record `fixed` (defined as self-fixed) lines, which the same section forbids.**
  quote A: "`blocking` suspends autonomy entirely: relay, stamp, stop — no self-fixes from a blocking round."
  quote B: "### 2026-08-27 — architect, fable 5, blocking (round 2, diff-scoped)" … "- fixed — [Important] the document state between a plan's diff-scoped LGTM and its confirming round was undefined, each reading breaking a recorded convention; license: this spec's own recovery philosophy"
  *(`fixed` is defined at "The disposition ledger" as "self-fixed"; rounds 1, 2 and 3 are all `blocking`.)*

**"Sequencing" — the propagation gate runs after the relay turn but can produce a held line, and the only stated delivery moment for held questions is the relay turn that has already passed.**
  quote A: "Held set non-empty: batch the held questions into one message at the relay turn — per item: a one-line claim, why it is held, the question, and options with the session's recommendation — and wait."
  quote B: "Before any re-dispatch — held set empty or developer-ordered — the propagation-auditor (audit-agents spec) gates the round when it is available … a hit the session believes is wrong escalates as held, like any contested finding — its held line carries the marker `[hit]` in the severity slot"
  *(The same section states "the developer is interrupted exactly once per round"; a gate escalation is a second interruption in the same round, or none.)*

**"Termination" vs. "Triage" — the all-Minor bullet prescribes fixing findings by grade, which the license test explicitly rules out as the basis for a fix.**
  quote A: "All-Minor signal: two consecutive rounds whose findings are all Minor end the unattended run — fix the residue, annotate `concerns (resolved <date>)`, and escalate with a fresh-round offer instead of dispatching again."
  quote B: "Severity is not the line. A Minor finding can be decision-shaped (a naming call the developer already ruled on); a Critical can be self-fixable (a contradiction with a recorded ADR — the ADR is the license). Triage reads the fix's license, never the finding's grade."

**"Termination" vs. "Termination" (loop closure) — the `concerns (resolved <date>)` annotation is an autonomous act in one passage and an offered choice in the next.**
  quote A: "All-Minor signal: two consecutive rounds whose findings are all Minor end the unattended run — fix the residue, annotate `concerns (resolved <date>)`, and escalate with a fresh-round offer instead of dispatching again."
  quote B: "Loop closure reuses existing machinery: after answers land, the session offers a fresh round (replacing the verdict as usual) or the lifecycle rule's `concerns (resolved <date>)` annotation with its body note"
  *(Under "Re-dispatch briefs" an annotation close also "ends the loop", so the difference decides whether a session may close a loop without the developer.)*

**"The disposition ledger" vs. the grammar block — the `held` shape has no slot for the counter-evidence two other passages require it to carry.**
  quote A: "`held` — needs the developer; the line carries the concrete question (or the dispute plus counter-evidence), phrased so one short answer resolves it."
  quote B: "    - held — [<severity>] <claim>; question: <one short question>"
  *("Triage" states the same requirement independently: "A finding the session believes is wrong is held with the session's counter-evidence attached".)*

**"Re-dispatch briefs" vs. the grammar block — the next round's brief must read deviations back out of the ledger, but the closed grammar carries no deviation marker.**
  quote A: "When the ledger records a deviation from a reviewer's suggestion, the next round's brief invites refutation of the recorded rationale — the rationale is not a defence to be protected."
  quote B: "    - fixed — [<severity>] <claim>; license: <citation>; <what changed>"
  *(The grammar's variants are enumerated as closed: "the grammar's one severity-token variant" and "the grammar's one heading annotation".)*

**"Re-dispatch briefs" vs. "The disposition ledger" — the heading that marks a plan's owed confirming round is named the durable marker, but no anchor or command detects it.**
  quote A: "the `### <ISO date> — <agent>, <model self-report>, LGTM (round N, diff-scoped)` heading is the durable marker that a confirming round is owed"
  quote B: "Two greppable anchors join the lifecycle rule's unfinished-work discipline: `open` lines (a stamped round whose remediation never ran) and `held` lines (pending developer questions)."
  *(The mandated command is `rg -n --no-ignore --crlf '^- (open|held) —' docs/`, which matches no heading; the recovery clause itself concedes "an annotation-closed or previously-approved document is grep-clean there".)*

**"The disposition ledger" / "Changes by file" vs. the glossary's Unfinished-work list entry — the new class is given non-frontmatter match semantics and costs a consumer edit, contradicting a recorded property of the list, and no glossary edit is routed.**
  quote A: "The entry deliberately re-scopes the list's frontmatter-only invariant for itself: its hits count inside a `## Review rounds` section and nowhere else" … "`plugins/working-process/skills/process-status/SKILL.md` — the hit-confirmation step takes an entry's own published match scope when the entry re-scopes it"
  quote B (`docs/domain/glossary.md`, **Unfinished-work list**): "the single definition site for which classes exist, so a new class costs one edit in the rule and none in the consumers that run it. A command's output is hits to confirm against the frontmatter block, never Findings."

**"Re-dispatch briefs" vs. `## Review rounds` closing paragraph — the reviewer's stop signal is defined only for an all-Minor round, and the document's own loop closes on it after a round whose single finding is Important.**
  quote A: "asks the reviewer for its own stop signal: when the round's remaining findings are all Minor wording residue, say so and judge whether another round is worth its cost."
  quote B: "Loop closed 2026-08-27 by the resolution annotation, on round 5's own alternative: the single finding was a two-clause routing edit with no design content, fixed as suggested, and the whole-text backstop is the consumption gate's integrity audit this release ships"
  *(Round 5's only line reads "- fixed — [Important] the round-4 gate behavior was fully designed in the body and routed to no file edit".)*

**"The disposition ledger" — the declined-resolution token is given two forms, one dated and one not, in the same section that calls the shape canonical.**
  quote A: "`resolved (declined)` records the developer keeping the document as it was."
  quote B: "    - resolved <date> (declined) — [<severity>] <claim>; <why the document stands>"

---

## Ranked implementer questions

1. **What is a diff-scoped brief's diff taken against?** "briefed on what changed since the round it follows" names no source for the previous state — no snapshot, no commit, no recorded hash — and the lifecycle rule keeps these documents deliberately uncommitted through the review rounds. Without an answer the central mechanism of "Re-dispatch briefs" cannot be built.
2. **How do the two release-mates' consumption-gate offers compose in `workflow.md`?** The audit-agents spec fires the integrity-audit offer only on an `integrity:` body-hash mismatch ("a match meaning the standing stamp satisfies the gate"); this spec fires the pair question on any diff-scoped-chain LGTM. Which governs a spec carrying both a matching stamp and a diff-chain LGTM?
3. **Is the confirming full-document round after a plan's diff-scoped LGTM autonomous, and does it count against the three-round cap?** It is prescribed as mandatory ("one full-document confirming round follows"), which sits oddly with both the cap and the every-step-is-an-offer ethos.
4. **When a contested `[hit]` escalates at the propagation gate, does the round wait for the answer, and does that escalation reset the cap count?** The gate is specified to "repeat until the audit comes back clean", a state a contested hit never reaches.
5. **What counts as "developer contact" for the cap reset?** A held batch the developer has not yet answered, a relay the developer read silently, and the cap escalation itself are all candidates, and the choice decides whether the cap can ever bind.
6. **What is the exact vocabulary and case of the `[<severity>]` slot?** The glossary fixes `critical | important | minor` in lowercase; the document's own ledger writes `[Important]` and `[Minor]`, and the one variant `[hit]` is lowercase. The deferred grammar lint depends on this.
7. **What shape does a single Unfinished-work entry with two owners take?** The list's entry format is "class name, grep command, and the owner of the next move" (singular); this spec routes one entry "whose entry text names both owners", and `process-status` must render it.
8. **What distinguishes "not now" from "not in this session" in the consent question,** given the same sentence says the session "asks once per Claude Code session … and honours the answer without re-asking"?
9. **What closes the loop when a held answer lands and the developer accepts neither the fresh round nor the annotation?** Both arms are offers; the document names no third state and no `resolved` line can be written without one of them.
10. **Are ledger lines flush-left or indented?** The canonical block is presented indented four spaces while the mandated command anchors on `^-`; the difference decides whether the document's own grammar block is self-matching.

---

coverage: 429 lines; highest line cited 429
