---
ticket: none
date: 2026-09-11
status: draft
grilled: 2026-09-11
architect: blocking
revises: [./2026-08-17-autonomous-review-loop-design.md, ./2026-09-07-diff-scoped-chain-debt-design.md, ./2026-08-27-audit-agents-design.md]
branch: feature/process-wave-four
base: develop
---

# Review loop — errata wave four

## Problem

Two outside cycles ran working-process 0.13.0 through 0.16.0 on real
client work and groomed their findings against each release. Seven
items survived 0.16.0. Three of them were decisions the developer had
not yet taken; four were sentences nobody had written; grilling found
two more decisions the rules had left implicit. Six are errata: they
remove a contradiction or write down what the rules already implied.
One is not — W1, with decisions 1, 4 and 5 and the term they need,
changes what closes a plan and withdraws a close path the shipped rules
granted. It rides here rather than in a spec of its own because its
alternatives are recorded beside its rulings, which is what a design
document's alternatives section would have carried, and because round
one found its rough edges to be one-clause fixes rather than a reshape
(developer ruling, 2026-09-11).

The findings live in this repo's Private memory as lifted copies
(`idea-working-process-second-cycle`, `idea-working-process-sweep-verifier`),
each pointing at its authoritative source. This document records the
decisions and the changes; it does not repeat the evidence.

## Decisions taken 2026-09-11

Five questions — three the shipped rules left open and two the
grilling found implicit in them. Each was put to the developer with its
options and cost; the answers below are rulings and carry that clause
where a ledger later cites them.

1. **A plan's loop closes only on a full-document round.** Today the
   confirming round fires on exactly one path — a diff-scoped `LGTM`.
   Two measured loops closed by other paths — a resolution annotation
   after a diff-scoped `concerns` — and owed no confirming round by the
   letter, yet in both the confirming round ran on the reviewer's
   recommendation and found the cycle's one Important. The rule now
   keys on the latest round heading rather than on the path: whatever
   ends a plan's rounds, one full-document round follows unless the
   latest verdict round already was full-document. Alternatives
   declined: keying on the reviewer's stop signal (a semantic read of
   free text that no lint can check, on a line every round writes) and
   widening only the annotation path (leaves the cap and all-Minor
   escalations uncovered). `ruling: 2026-09-11`.
2. **A round heading's sha, if one is ever written, stands beside the
   `integrity:` hash and never in its place.** Per-round commits are
   opt-in, so a sha exists only on that path; the `integrity:` hash is
   computed from the body and must work on a document nobody has
   committed, which is the default path. Something present only
   sometimes cannot replace something that must be present always. One
   sentence records it so a later session does not "tidy" the hash
   away. `ruling: 2026-09-11`.
3. **`process-status` reports the plan co-firing in one line derived
   from its mapping, without judging it.** The rule already calls the
   Unresolved verdict / Chain debt duplicate on a plan deliberate
   (`spec-plan-lifecycle.md`, the Unresolved verdict owner leg). The
   report adds one line where both classes hit the same plan — one debt
   seen from two sides, both settled through the confirming round, see
   that owner leg — derived from two hits sharing a file, in the shape
   the skill already uses when Misplaced stamp silences a neighbour. It does not say "deliberate": that is process
   knowledge, and the skill's contract is to carry none. Alternative
   declined: silence, which leaves the explanation where the confused
   reader never looks. `ruling: 2026-09-11`.

4. **"Latest round heading" means the highest ordinal, wherever it
   sits.** Grilling found the phrase undefined in both rules that use
   it while W1 makes it the key: the lifecycle rule prescribes the
   heading's shape and nothing about block order, and live ledgers run
   both ways — ten chronological, four newest-first, and one session
   on 2026-09-08 writing a spec one way and its plan the other. The
   ordinal is on every heading, including those predating the `scope`
   token, so it decides; block order stays unprescribed, since
   reordering closed documents is body editing and a state-aware lint
   can flag order later. The ordinal decides only while it never
   restarts, which nothing said: the heading grammar is silent and the
   workflow rule has a later round opening a new loop. So the rule now
   says it — ordinals run per document and per field and continue across
   loops, which is what the round cap's own derivation from the headings
   already assumed and what practice already does. Alternatives
   declined: mandating newest-first (leaves ten documents non-compliant)
   and reading file position (leaves four). `ruling: 2026-09-11`.

5. **On a plan, the resolution annotation and the adjudication wait
   for the full-document round; the round has no decline path.**
   Grilling asked what happens when the developer wants to close a plan
   whose latest heading is diff-scoped. The annotation is written only
   once the latest heading is full-document; until then the plan stays
   `adversary: concerns` unannotated, which the Unresolved verdict
   command matches, so the owed round is visible. The confirming round
   is the same loop's last round, and it inherits the gating of whatever
   ended the rounds: autonomous where autonomy still stands — a
   diff-scoped `LGTM`, or `concerns` inside the cap — and the
   developer's to order after `blocking`, the round cap or the all-Minor
   signal, each of which suspends autonomy by its own terminator. A
   developer who wants no further round leaves the plan open, and
   that is the honest state. Alternatives declined: a decline recorded
   with `, debt discharged <date>` on a `concerns` heading, which uses
   the Chain debt token outside the term's definition and would reopen
   a five-day-old concept; and treating the confirming round as a new
   loop after the annotation, which strips it of standing consent and
   leaves the plan clean for the Unfinished-work list between the two.
   The cost is stated: an in-flight plan gets no decline path where a
   spec has three discharge paths, and a later erratum may add one, on a
   measured plan whose confirming round earned nothing. A plan already
   at `status: implemented` is the exception, on the ground its sibling
   class already ships: completed work is not re-reviewed, so there the
   round is discharged by recorded decline without any dispatch, exactly
   as the Chain debt owner leg discharges its debt. Without that clause
   such a plan would sit on the Unfinished-work list for good, reporting
   finished work as unfinished. `ruling: 2026-09-11`.

A sixth question from the chain-debt design — whether a future
undischarged instance gets the same retroactive decline as the live
one — turned out to be answered by the text that shipped:
`spec-plan-lifecycle.md` already derives the decline on an
`implemented` document from the Chain debt owner leg. No change.

## Scope

Seven changes in `plugins/working-process/`, and three in
`docs/domain/glossary.md` — two applied at grilling (the Round heading
sentence, the Confirming round entry) and one owed (W5).

1. **W1 — plan close needs a full-document round** (decision 1).
   `workflow.md`, *What a diff-scoped LGTM certifies*: the plan
   paragraph generalizes from "never terminates on a diff-scoped LGTM"
   to "closes only when the latest verdict round was full-document",
   and the recovery sentence reads "latest round heading is diff-scoped,
   whatever its verdict". The same paragraph gains the gating sentence:
   the confirming round inherits the gating of whatever ended the
   rounds, autonomous only where autonomy still stands, since
   `blocking`, the round cap and the all-Minor signal each suspend it by
   their own terminator. Three sentences in that section rename the
   spec's pair-offer arm from "confirming round" to "a full-document
   round", so the term names one object.

   `spec-plan-lifecycle.md`, Unfinished-work list, Unresolved verdict
   owner leg: the plan exception widens to any plan whose latest heading
   is diff-scoped — the confirming round closes the verdict and the
   annotation may not. Its co-firing sentence narrows in the same edit,
   to "where that heading is an `LGTM`, such a plan matches Chain debt as
   well": that class's command keys on `LGTM`, so a diff-scoped
   `concerns` heading produces no second hit and the unnarrowed sentence
   would be false for the case W1 adds. The leg also gains the
   implemented-document decline of decision 5, in the shape the Chain
   debt leg already uses.

   The same rule's *The disposition ledger* section gains two sentences:
   the latest round heading is the one carrying the highest ordinal
   wherever it sits, and ordinals run per document and per field and
   continue across loops (decision 4). The rule's resolution-annotation
   bullet — "Concerns resolved without a fresh review round keep the
   verdict and gain a resolution date" — gains the plan clause of
   decision 5: on a plan the annotation and the adjudication are written
   only once the latest round heading is full-document. The glossary
   gains **Confirming round**, minted at grilling and amended in this
   wave to carry the gating clause.
2. **W2 — what the cap does not promise.** `workflow.md`, Terminators,
   Round cap bullet: one sentence saying a run of `blocking` verdicts is
   unbounded by the cap, because the cap counts autonomous rounds and
   `blocking` suspends autonomy — each continuation is the developer's
   own decision, so consenting to three rounds consents to three
   autonomous ones.
3. **W3 — sha beside hash** (decision 2). `spec-plan-lifecycle.md`,
   the per-round-commits paragraph: one sentence.
4. **W4 — co-firing line** (decision 3). `process-status/SKILL.md`,
   Step 4, after the Misplaced stamp paragraph.
5. **W5 — glossary wrap seam.** `docs/domain/glossary.md`, Chain debt:
   the clause "recorded decline — of the gate's pair offer, or, where
   …, of the question …" loses its comma pile; the term's meaning does
   not move.
6. **W6 — topic-branch naming.** `workflow.md` gains a short *Branch
   naming* paragraph near step 1: `feature/<ticket>-<short-name>`,
   `feature/<short-name>` where the ticket is `none`, auto-generated
   worktree names renamed to it before the first commit, and the
   `branch:` field recording the result. It goes to the workflow rule
   rather than to `ticket-frontmatter.md`, whose `paths: docs/**`
   frontmatter cannot fire at the moment the convention binds — a branch
   is cut before any `docs/` file of that work exists, and `workflow.md`
   is the payload's only unscoped rule and the owner of step 1. The
   ticket rule's sourcing paragraph, which already reads a ticket out of
   `feature/ABC-123-...`, gains a pointer rather than the convention.
   The repo-level half landed in this repo's `CLAUDE.md` on 2026-07-22;
   this is the cross-project half.
7. **W7 — the propagation duties as an author-facing rule.** A new
   rule file, `rules/propagation-duties.md`, scoped by `paths:` to
   `docs/specs/**`, `docs/plans/**` and `docs/domain/**` — the first
   two as the process-artifacts rule scopes them, the third because
   duty 1 fires when a glossary `_Avoid_` ban is minted, and a rule
   silent at the glossary would miss the one edit that duty names.
   Outside authoring it costs nothing; inside it, it loads for every
   reader of a matching document, dispatched agents included — the
   propagation-auditor among them, which already carries these duties in
   its card. That duplication is accepted, and bounded by what the rule
   holds: the trigger list and the enumeration each demands, keyed to
   the card's duty numbers, and none of the card's measurements. It keys the eight duties by
   the edit an author just made — changed an interface, prescribed a
   block, added a field or label, asserted a count, used a name the
   source does not define, reported another document's state, wrote a
   verification command, copied a reviewer's citation — and names the
   enumeration each demands, before the next dispatch pays for an
   audit. The agent card stays the gate's definition and keeps the
   measurements; the rule is the author's checklist and cites the card
   rather than restating its evidence. `README.md` moves from "five rule
   files" to six and names the new one.

## What this wave does not do

- **No decline path for an in-flight plan's confirming round**
  (decision 5). Such a plan stays unannotated and visible to the
  Unresolved verdict command until the round runs; the developer's only
  lever is to order the round or leave the plan open. An annotation
  written before the round would be a rule violation, and a violated
  plan is invisible to the list the way any violation is — the recovery
  clause in `workflow.md`, re-offer at the document's next touch, is
  what catches it. A state-aware lint reading headings by ordinal is
  where a mechanical check belongs. A plan already `implemented` is not
  this case: W1 gives it the recorded decline.
- **The Chain debt term keeps its meaning.** It names what a diff-scoped
  `LGTM` leaves. W1 gives a plan a broader obligation, owned by the
  workflow rule, and does not fold it into the term.
- **The sync-rules install is the developer's.** Adding a rule file
  changes the payload's ruleset hash, so every rules target carrying
  this payload drifts until `sync-rules` updates it — this machine's is
  user-level, at `~/.claude/rules/working-process/`. Running it is not a
  commit on this branch and not part of this wave.
- **Nothing here reaches `superpowers:writing-plans`.** The mutation
  proof, the spec-coverage duty, the seam checklist, the authoring bans
  and the platform-API class stay in the valuable package; each needs
  a design decision this wave does not take.

## Verification

Each change is checked by grep against the shipped file, whitespace
normalized so a wrapped phrase still matches; a check states both its
before and after value.

- W1, `workflow.md`, whitespace-normalized: `grep -o 'never terminates on a diff-scoped LGTM' | wc -l` — 1 before, 0 after; `grep -o 'latest verdict round was full-document' | wc -l` — 0 before, 1 after; `grep -o 'inherits the gating of whatever ended' | wc -l` — 0 before, 1 after (round one's F1); `grep -o 'a confirming round on a spec' | wc -l` — 1 before, 0 after (round one's M1, the spec arm renamed).
- W1, `spec-plan-lifecycle.md`: `grep -c 'whose latest round heading is a$' ` — the owner leg's line — 1 before, 0 after. Whitespace-normalized: `grep -o 'highest ordinal' | wc -l` — 0 before, 1 after (decision 4); `grep -o 'continue across loops' | wc -l` — 0 before, 1 after (round one's F2); `grep -o 'where that heading is an .LGTM.' | wc -l` — 0 before, 1 after (round one's F3); `grep -o 'wait for the confirming round' | wc -l` — 0 before, 1 after (decision 5).
- W1, glossary: `grep -c '^\*\*Confirming round\*\*:' docs/domain/glossary.md` — 1 before and after, a declared invariant, the entry having landed at grilling; `tr -s '[:space:]' ' ' < docs/domain/glossary.md | grep -o 'inherits the gating' | wc -l` — 1 before and after, a declared invariant: round one's F1 reached the entry, so this text landed with that fix wave rather than with the prescribed rule edits.
- W2: `tr -s '[:space:]' ' ' < plugins/working-process/rules/workflow.md | grep -o 'unbounded by the cap' | wc -l` — 0 before, 1 after.
- W3: `tr -s '[:space:]' ' ' < plugins/working-process/rules/spec-plan-lifecycle.md | grep -o 'never stands in for the' | wc -l` — 0 before, 1 after.
- W4: `grep -c 'Unresolved verdict and Chain debt' plugins/working-process/skills/process-status/SKILL.md` — 0 before, 1 after.
- W5: `grep -c 'decline — of the gate' docs/domain/glossary.md` — 1 before, 0 after.
- W6: `grep -c '^## Branch naming' plugins/working-process/rules/workflow.md` — 0 before, 1 after; the same command against `ticket-frontmatter.md` — 0 before and after, a declared invariant, since round one moved the section out of that rule; `tr -s '[:space:]' ' ' < plugins/working-process/rules/ticket-frontmatter.md | grep -o 'branch naming convention' | wc -l` — 0 before, 1 after (the pointer that replaces it).
- W7: `ls plugins/working-process/rules/*.md | wc -l` — 5 before, 6 after; `grep -c 'docs/domain/\*\*' plugins/working-process/rules/propagation-duties.md` — no file before, 1 after; `grep -c 'six rule files' plugins/working-process/README.md` — 0 before, 1 after; `claude plugin validate plugins/working-process` passes after.

## Review rounds

### 2026-09-11 — architect, fable 5.1, blocking (round 1, full-document)

The propagation gate ran first and returned `CLEAN`, so this round wrote
no gate lines. Every citation the report supplied — twenty of them,
across four rule files, the glossary, a skill, an agent card, the repo
`CLAUDE.md` and two other specs — was checked against what it names
before anything was written here, and all twenty hold.

- fixed 2026-09-11 — [Important] the confirming round was asserted to run "under the same standing consent" on every path that can end a plan's rounds, while `blocking`, the round cap and the all-Minor signal each suspend autonomy by their own terminator; license: those three terminators' own text (`workflow.md:366`, `:371`, `:389`), which the shipped sentence at `:437` was never written against; decision 5, the W1 scope item and the glossary entry now say the round inherits the gating of whatever ended the rounds, autonomous only where autonomy still stands
- fixed 2026-09-11 — [Important] "highest ordinal" was well-defined only if ordinals never restart, which nothing wrote down while `workflow.md:449` has a later round opening a new loop; license: the round cap's own derivation, which counts by folding round headings and is unsound under restarting ordinals; decision 4 and the W1 scope item now add the clause — ordinals run per document and per field and continue across loops
- fixed 2026-09-11 — [Important] widening the Unresolved verdict owner leg left its own co-firing sentence false for the case W1 adds, since the Chain debt command keys on `LGTM` and a diff-scoped `concerns` heading produces no second hit; license: that command, published in the same rule; the W1 scope item now narrows the sentence to "where that heading is an `LGTM`" in the same edit that widens the leg
- fixed 2026-09-11 — [Important] W6 placed the branch-naming convention in `ticket-frontmatter.md`, whose `paths: docs/**` frontmatter cannot fire when a branch is cut before any `docs/` file of that work exists; license: that rule's own frontmatter, and `workflow.md` being the payload's only unscoped rule and the owner of step 1; W6 now lands the paragraph in `workflow.md` and leaves the ticket rule a pointer
- fixed 2026-09-11 — [Minor] the minted **Confirming round** entry said a spec owes none while `workflow.md` used the same words for the spec's pair-offer arm; ruling: 2026-09-11; the term stays plan-only and W1 renames the spec arm to "a full-document round" in the three sentences that carry it
- fixed 2026-09-11 — [Minor] the sync-rules exclusion described a project-level install removed during this very round and called it "Ignored mode", which the glossary defines for Process directories only; license: the glossary's Process directory entry, which names `.claude/rules/` as not one; the bullet now states the mechanism — the ruleset hash changes and every target carrying the payload drifts until `sync-rules` runs — and names this machine's user-level target
- fixed 2026-09-11 — [Minor] decision 5's stated cost covered in-flight plans only, leaving a plan that reaches `implemented` with a diff-scoped latest heading a permanent Unresolved verdict resident; ruling: 2026-09-11; the implemented-document decline of the sibling Chain debt leg now extends to the confirming round, on the ground that leg already ships — completed work is not re-reviewed
- fixed 2026-09-11 — [Minor] W7's "costs nothing outside authoring" ignored that the rule loads for every reader of a matching document, the propagation-auditor included, which already carries these duties; license: that agent's card; the item now accepts the duplication and bounds the rule to the trigger list plus duty numbers, with none of the card's measurements
- fixed 2026-09-11 — [Minor] "None needs a design of its own" was contradicted by the document's own content; ruling: 2026-09-11; the Problem section now says six errata and one design item, and why W1 rides here rather than in a spec of its own
- hit fixed 2026-09-11 — the W1 glossary check stated 0 before for "inherits the gating" while the fix wave had just written that clause into the entry, so the check would have failed against a correct tree; the check is now a declared invariant at 1, like the Confirming round entry check beside it. Re-simulating all twenty before-values found no second instance
- signal 2026-09-11 — another round earns its cost: F1 to F4 change rule
  text the whole wave hangs on and F1 touches an entry minted at
  grilling, so the fix wave deserves a diff-scoped read; the leftovers
  after it are worth little, being wording and one honest cost statement
