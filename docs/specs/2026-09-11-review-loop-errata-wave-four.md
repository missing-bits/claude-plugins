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
two more decisions the rules had left implicit. None needs a
design of its own, and each is cheap to remove — which is what makes
this a wave of errata rather than a fifth follow-up spec.

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
   can flag order later. Alternatives declined: mandating newest-first
   (leaves ten documents non-compliant) and reading file position
   (leaves four). `ruling: 2026-09-11`.

5. **On a plan, the resolution annotation and the adjudication wait
   for the full-document round; the round has no decline path.**
   Grilling asked what happens when the developer wants to close a plan
   whose latest heading is diff-scoped. The annotation is written only
   once the latest heading is full-document; until then the plan stays
   `adversary: concerns` unannotated, which the Unresolved verdict
   command matches, so the owed round is visible and the confirming
   round is the same loop's last round under the same standing consent.
   A developer who wants no further round leaves the plan open, and
   that is the honest state. Alternatives declined: a decline recorded
   with `, debt discharged <date>` on a `concerns` heading, which uses
   the Chain debt token outside the term's definition and would reopen
   a five-day-old concept; and treating the confirming round as a new
   loop after the annotation, which strips it of standing consent and
   leaves the plan clean for the Unfinished-work list between the two.
   The cost is stated: plans get no decline path where specs have three
   discharge paths. A later erratum may add one, on a measured plan
   whose confirming round earned nothing. `ruling: 2026-09-11`.

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
   whatever its verdict". `spec-plan-lifecycle.md`, Unfinished-work
   list, Unresolved verdict owner leg: the plan exception widens the
   same way — the confirming round closes the verdict and the annotation
   may not, on any plan whose latest heading is diff-scoped. The same
   rule's *The disposition ledger* section gains one sentence defining
   the latest round heading by ordinal (decision 4); the glossary's
   Round heading entry already carries it, applied at grilling. The
   rule's resolution-annotation bullet — "Concerns resolved without a
   fresh review round keep the verdict and gain a resolution date" —
   gains the plan clause of decision 5: on a plan the annotation and
   the adjudication are written only once the latest round heading is
   full-document. The glossary gains **Confirming round**, minted at
   grilling: both rules use the phrase throughout for the object W1 keys
   on, and no entry defined it.
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
6. **W6 — topic-branch naming.** `ticket-frontmatter.md` gains a short
   *Branch naming* section: `feature/<ticket>-<short-name>`,
   `feature/<short-name>` where the ticket is `none`, auto-generated
   worktree names renamed to it before the first commit, and the
   `branch:` field recording the result. The rule's sourcing paragraph
   already assumes this shape; the section makes the assumption a
   convention. The repo-level half landed in this repo's `CLAUDE.md`
   on 2026-07-22; this is the cross-project half.
7. **W7 — the propagation duties as an author-facing rule.** A new
   rule file, `rules/propagation-duties.md`, scoped by `paths:` to
   `docs/specs/**`, `docs/plans/**` and `docs/domain/**` — the first
   two as the process-artifacts rule scopes them, the third because
   duty 1 fires when a glossary `_Avoid_` ban is minted, and a rule
   silent at the glossary would miss the one edit that duty names. It
   costs nothing outside authoring. It keys the eight duties by
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

- **No decline path for a plan's confirming round** (decision 5). A
  plan whose latest heading is diff-scoped stays unannotated and
  visible to the Unresolved verdict command until the round runs; the
  developer's only lever is to order the round or leave the plan open.
  An annotation written before the round would be a rule violation,
  and a violated plan is invisible to the list the way any violation
  is — the recovery clause in `workflow.md`, re-offer at the document's
  next touch, is what catches it. A state-aware lint reading headings by
  ordinal is where a mechanical check belongs.
- **The Chain debt term keeps its meaning.** It names what a diff-scoped
  `LGTM` leaves. W1 gives a plan a broader obligation, owned by the
  workflow rule, and does not fold it into the term.
- **The sync-rules install is the developer's.** Adding a rule file
  changes the payload's ruleset hash; the project-level install under
  `.claude/rules/working-process/` is Ignored mode and updates by
  running `sync-rules`, which is not a commit on this branch.
- **Nothing here reaches `superpowers:writing-plans`.** The mutation
  proof, the spec-coverage duty, the seam checklist, the authoring bans
  and the platform-API class stay in the valuable package; each needs
  a design decision this wave does not take.

## Verification

Each change is checked by grep against the shipped file, whitespace
normalized so a wrapped phrase still matches; a check states both its
before and after value.

- W1: `tr -s '[:space:]' ' ' < plugins/working-process/rules/workflow.md | grep -o 'never terminates on a diff-scoped LGTM' | wc -l` — 1 before, 0 after; `grep -o 'latest verdict round was full-document' | wc -l` over the same stream — 0 before, 1 after. `grep -c 'whose latest round heading is a$' plugins/working-process/rules/spec-plan-lifecycle.md` — the owner leg's line — 1 before, 0 after. Over the whitespace-normalized lifecycle rule: `grep -o 'highest ordinal' | wc -l` — 0 before, 1 after (decision 4); `grep -o 'wait for the confirming round' | wc -l` — 0 before, 1 after (decision 5). `grep -c '^\*\*Confirming round\*\*:' docs/domain/glossary.md` and `grep -c 'highest ordinal' docs/domain/glossary.md` — both 1 before and after: applied at grilling, declared invariants.
- W2: `tr -s '[:space:]' ' ' < plugins/working-process/rules/workflow.md | grep -o 'unbounded by the cap' | wc -l` — 0 before, 1 after.
- W3: `tr -s '[:space:]' ' ' < plugins/working-process/rules/spec-plan-lifecycle.md | grep -o 'never stands in for the' | wc -l` — 0 before, 1 after.
- W4: `grep -c 'Unresolved verdict and Chain debt' plugins/working-process/skills/process-status/SKILL.md` — 0 before, 1 after.
- W5: `grep -c 'decline — of the gate' docs/domain/glossary.md` — 1 before, 0 after.
- W6: `grep -c '^## Branch naming' plugins/working-process/rules/ticket-frontmatter.md` — 0 before, 1 after.
- W7: `ls plugins/working-process/rules/*.md | wc -l` — 5 before, 6 after; `grep -c 'docs/domain/\*\*' plugins/working-process/rules/propagation-duties.md` — no file before, 1 after; `grep -c 'six rule files' plugins/working-process/README.md` — 0 before, 1 after; `claude plugin validate plugins/working-process` passes after.

## Review rounds

### 2026-09-11 — architect, fable 5.1, blocking (round 1, full-document)

The propagation gate ran first and returned `CLEAN`, so this round wrote
no gate lines. Every citation the report supplied — twenty of them,
across four rule files, the glossary, a skill, an agent card, the repo
`CLAUDE.md` and two other specs — was checked against what it names
before anything was written here, and all twenty hold.

- open — [Important] the confirming round is asserted to run "under the
  same standing consent" on every path that can end a plan's rounds,
  while three of the four newly covered paths are terminators that
  suspend autonomy: `blocking` (`workflow.md:366`), the round cap
  (`:371`) and the all-Minor signal (`:389`). The shipped sentence at
  `:437` was written for the diff-scoped `LGTM` path alone, where
  autonomy still stands
- open — [Important] "latest round heading means the highest ordinal" is
  well-defined only if ordinals never restart, which nothing writes
  down: the heading grammar is silent and `workflow.md:449` says a later
  round on the same document opens a new loop. Practice continues the
  count (`2026-08-24-process-status-and-anchor-hardening-design.md:388`
  is `LGTM (round 1)`, `:420` is `concerns (round 2)`), but W1 keys on it
- open — [Important] widening the Unresolved verdict owner leg to any
  diff-scoped latest heading leaves its own co-firing sentence false: a
  `concerns` or `blocking` diff-scoped heading produces no Chain debt
  hit, because that class's command keys on `LGTM`
  (`spec-plan-lifecycle.md:378-383`). Decision 3 and W4 both rest on
  that sentence
- open — [Important] W6 puts the branch-naming convention in
  `ticket-frontmatter.md`, whose `paths: docs/**` frontmatter cannot fire
  at branch creation — step 1, typically before any `docs/` file exists.
  The only unscoped rule in the payload is `workflow.md`, which owns
  that step
- open — [Minor] the minted **Confirming round** entry says a spec owes
  none, while `workflow.md:416`, `:421` and `:424` use the same words for
  the spec's pair-offer arm
- open — [Minor] the sync-rules exclusion describes a project-level
  install that no longer exists and calls it "Ignored mode", a term the
  glossary defines for Process directories only — which `.claude/rules/`
  explicitly is not
- open — [Minor] decision 5's stated cost covers in-flight plans only: a
  plan reaching `implemented` with a diff-scoped latest heading becomes a
  permanent Unresolved verdict resident with no disposition, where the
  sibling Chain debt class already has an implemented-document decline
- open — [Minor] W7's "costs nothing outside authoring" overstates: the
  rule loads for every agent that reads a matching document, including
  the propagation-auditor, which already carries the same eight duties
- open — [Minor] "None needs a design of its own" is contradicted by the
  document's own content, since W1 reshapes what closes a plan and mints
  a glossary term
- signal 2026-09-11 — another round earns its cost: F1 to F4 change rule
  text the whole wave hangs on and F1 touches an entry minted at
  grilling, so the fix wave deserves a diff-scoped read; the leftovers
  after it are worth little, being wording and one honest cost statement
