---
ticket: none
date: 2026-09-11
status: implemented
grilled: 2026-09-11
architect: blocking (adjudicated 2026-09-11)
revises: [./2026-08-17-autonomous-review-loop-design.md, ./2026-09-07-diff-scoped-chain-debt-design.md]
branch: feature/process-wave-four
base: develop
---

# Review loop — errata wave four

## Problem

Two outside cycles ran working-process 0.13.0 through 0.16.0 on real
client work and groomed their findings against each release. Three
items survived 0.16.0 from them, and this wave carries four more of this
repo's own, seven in all. Three of the seven were decisions the developer had
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

Three of the seven come from those cycles and live in this repo's
Private memory as lifted copies
(`idea-working-process-second-cycle`, `idea-working-process-sweep-verifier`),
each pointing at its authoritative source: W1's trigger, W2's cap
sentence and W7's author-facing rule. The other four are this repo's
own — W3 and W4 answer questions its own designs left open, W5 is a seam
in text it shipped, and W6 is the cross-project half of a convention it
adopted in 2026-07. This document records the decisions and the changes;
it does not repeat the evidence.

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
   away. Alternative declined: leaving it an open question until
   per-round commits stop being opt-in, which costs nothing now and
   re-derives the same argument later. The third option — a sha in
   place of the hash — was refused on construction rather than on
   preference: the hash must work on the default path, where no sha
   exists. `ruling: 2026-09-11`.
3. **`process-status` reports the plan co-firing in one line derived
   from its mapping, without judging it.** The rule already calls the
   Unresolved verdict / Chain debt duplicate on a plan deliberate
   (`spec-plan-lifecycle.md`, the Unresolved verdict owner leg). The
   report says so on one line where two confirmed hits share one
   document, and points at the classes' own owner legs — derived from
   the mapping, two hits in one file, in the shape the skill already
   uses when Misplaced stamp silences a neighbour. It neither calls the
   duplicate deliberate nor restates that it is one debt seen from two
   sides: both are process knowledge, and the skill's contract is to
   carry none. Round four sharpened this from a named pair of classes
   to the shape, for the reason the ruling already gave. Alternative
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
   round is discharged by recorded decline without any dispatch, as the
   Chain debt owner leg discharges its debt. The plan clause below
   carries the same exception, or it would forbid the very annotation
   this one requires. One thing the analogy does not carry: a `blocking`
   verdict closes by adjudication, which the glossary defines as the
   developer's own act, so on an implemented plan a session derives the
   `concerns` decline and never the adjudication. Without that clause
   such a plan would sit on the Unfinished-work list for good, reporting
   finished work as unfinished. `ruling: 2026-09-11`.

A sixth question from the chain-debt design — whether a future
undischarged instance gets the same retroactive decline as the live
one — turned out to be answered by the text that shipped:
`spec-plan-lifecycle.md` already derives the decline on an
`implemented` document from the Chain debt owner leg. No change.

## Scope

Seven changes in `plugins/working-process/`, and three in
`docs/domain/glossary.md` — two already applied and one owed (W5). The
Round heading sentence landed at grilling; the **Confirming round**
entry was minted there and amended by rounds one and two, so what stands
in the file is the wave's own work, not a prescription waiting on it.

1. **W1 — plan close needs a full-document round** (decision 1).
   `workflow.md`, *What a diff-scoped LGTM certifies*: the plan
   paragraph generalizes from "never terminates on a diff-scoped LGTM"
   to "closes only when the latest verdict round was full-document",
   and the recovery sentence carries decision 1's trigger rather than
   the heading alone: a diff-scoped `LGTM` keeps the shipped "at the
   document's next touch", since that heading is itself an end, while a
   diff-scoped heading of any other verdict re-offers the round when
   something tries to end the plan's rounds — an annotation, an
   adjudication, a `status` move — or when a terminator that suspends
   autonomy has fired. Without that trigger the sentence would fire on a
   plan merely mid-loop between two diff-scoped rounds, where the loop
   rule prescribes a different next round: "Held set empty — dispatch
   the next round without asking, within the cap", and every later round
   diff-scoped. The paragraph also answers what a dispatching session
   needs and the recovery sentence alone does not: a session never
   judges that the rounds are ending. The terminators do — an `LGTM`, a
   `blocking`, the cap, the all-Minor signal — as does the developer
   closing the loop. While none has fired and the held set is empty, the
   next round is diff-scoped and the loop continues; the confirming
   round is owed the moment one fires, which is the moment a session
   would otherwise write the annotation. Leaving that to inference is
   what let the recovery sentence drift. The same paragraph's sentence "That round runs
   under the loop's standing consent like any other" is replaced rather
   than joined, since the two would contradict: the confirming round
   inherits the gating of whatever ended the rounds, autonomous only
   where autonomy still stands, because `blocking`, the round cap and
   the all-Minor signal each suspend it by their own terminator. What
   the replaced sentence also carried — that the round spends none of
   the round's one interruption — survives for the autonomous case and
   is stated of it. Four sentences in that section rename the
   spec's pair-offer arm from "confirming round" to "a full-document
   round" — the enumeration is `workflow.md:416`, `:419`, `:421` and
   `:424`, a snapshot of the file as it stands — so the term names one
   object. The numbers move once W6 inserts its heading above them; the
   checks anchor text rather than lines, so neither edit depends on the
   other's order.

   `spec-plan-lifecycle.md`, Unfinished-work list, Unresolved verdict
   owner leg: the plan exception widens to any plan whose latest heading
   is diff-scoped — the confirming round closes the verdict and the
   annotation may not. Its co-firing sentence narrows in the same edit,
   to "where that heading is an `LGTM`, such a plan matches Chain debt as
   well": that class's command keys on `LGTM`, so a diff-scoped
   `concerns` heading produces no second hit and the unnarrowed sentence
   would be false for the case W1 adds. The leg also gains the
   implemented-document decline of decision 5, in the shape the Chain
   debt leg uses — with the distinction that leg never needed, since it
   knows only `LGTM` headings: on an implemented plan a session derives
   the `concerns` decline, while a `blocking` heading waits for the
   developer's adjudication, which the glossary defines as their own
   act.

   The same rule's *The disposition ledger* section gains two sentences:
   the latest round heading is the one carrying the highest ordinal
   wherever it sits, and ordinals run per document and per field and
   continue across loops (decision 4). The glossary's **Round heading**
   entry gains the continuity half too, so the term reads without the
   rule beside it. The rule's resolution-annotation
   bullet — "Concerns resolved without a fresh review round keep the
   verdict and gain a resolution date" — gains the plan clause of
   decision 5: on a plan the annotation and the adjudication are written
   only once the latest round heading is full-document, unless the plan
   is already `implemented`, where the annotation is written citing that
   standing decision — the exception the owner leg carries, stated where
   the prohibition is, since an `implemented` document is amended in
   frontmatter and the annotation is the only lever left. The glossary
   gains **Confirming round**, minted at grilling and amended in this
   wave to carry the gating clause.
2. **W2 — what the terminators do not promise.** `workflow.md`, Terminators,
   Round cap bullet: one sentence saying a run of `blocking` verdicts is
   unbounded by the cap, because the cap counts autonomous rounds and
   `blocking` suspends autonomy — each continuation is the developer's
   own decision, so consenting to three rounds consents to three
   autonomous ones. The all-Minor bullet gains a plan clause in the same
   edit: it says today that the resolution annotation records the
   developer's close, which W1 makes untrue on a plan until the
   confirming round runs, so the sentence gains the qualifier "on a
   plan, once the confirming round has run". A session executing a terminator reads that
   terminator's bullet, not the section three pages down, and the cap
   bullet already carries plan-specific text, so the pointer belongs
   there.
3. **W3 — sha beside hash** (decision 2). `spec-plan-lifecycle.md`,
   the per-round-commits paragraph: one sentence.
4. **W4 — co-firing line** (decision 3). `process-status/SKILL.md`,
   Step 4, after the Misplaced stamp paragraph — and written as a shape
   rather than as a pair of class names: where two confirmed hits share
   one document, the report says so on one line and points at the
   classes' own owner legs. Naming the pair, or restating that they are
   one debt seen from two sides, would put the relationship in a second
   place and make the skill carry what it declares it does not — process
   knowledge of its own, where it takes the owner from the entry and
   never from its own knowledge. The shape also survives the next pair
   of classes without an edit, which is the same property the Misplaced
   stamp paragraph buys by keying on match semantics.
5. **W5 — glossary wrap seam.** `docs/domain/glossary.md`, Chain debt:
   the clause "recorded decline — of the gate's pair offer, or, where
   …, of the question …" loses its comma pile; the term's meaning does
   not move.
6. **W6 — topic-branch naming.** `workflow.md` gains a short
   `## Branch naming` section, immediately before
   `## Dispatching a verdict agent` — the file's only other H2, so the
   new one closes the material that follows the numbered flow rather
   than swallowing it, and the flow's steps name no branch-creation
   moment to sit beside:
   `feature/<ticket>-<short-name>`,
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
  plan is invisible to the list the way any violation is. What catches
  it is the recovery clause as W1 rewrites it: an annotation is one of
  the events that try to end a plan's rounds, so writing one re-offers
  the confirming round rather than escaping it. The "next touch" reading
  belongs to the `LGTM` heading alone. A state-aware lint reading headings by ordinal is
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

Each change is checked by grep against the shipped file. Every check
over prose normalizes whitespace first, so a phrase still matches
wherever the line wraps; only a check anchoring something that cannot
wrap — a heading, a filename, a file count — is written plain, and none
anchors a line ending. A check states both its before and after value,
except where it declares itself an invariant and says why.

- W1, `workflow.md`, whitespace-normalized: `grep -o 'never terminates on a diff-scoped LGTM' | wc -l` — 1 before, 0 after; `grep -o 'latest verdict round was full-document' | wc -l` — 0 before, 1 after; `grep -o 'inherits the gating of whatever ended' | wc -l` — 0 before, 1 after, paired with `grep -o 'runs under the loop.s standing consent like any other' | wc -l` — 1 before, 0 after, the sentence it replaces (round one's F1, the pairing added by the integrity audit); `grep -o 'at the document.s next touch' | wc -l` — 1 before and after, a declared invariant: round four's F1 keeps that phrase for the `LGTM` heading and adds the other verdicts' trigger beside it rather than replacing it; one anchor per renamed sentence, each 1 before and 0 after — `grep -o 'or a confirming full-document round'` (`:416`), `grep -o 'confirming round alone'` (`:419`), `grep -o 'a confirming round on a spec'` (`:421`), `grep -o 'The confirming-round arm'` (`:424`). Round two anchored two of the four and round three the rest, which is why each now stands on its own sentence rather than on the count.
- W1, `spec-plan-lifecycle.md`: `grep -o 'except on a plan whose latest round heading is a diff-scoped' | wc -l` over the whitespace-normalized rule — the owner leg's antecedent — 1 before, 0 after. Whitespace-normalized: `grep -o 'highest ordinal' | wc -l` — 0 before, 1 after (decision 4); `grep -o 'continue across loops' | wc -l` — 0 before, 1 after (round one's F2); `grep -o 'where that heading is an .LGTM.' | wc -l` — 0 before, 1 after (round one's F3); `grep -o 'wait for the confirming round' | wc -l` — 0 before, 1 after (decision 5).
- W1, glossary: `grep -c '^\*\*Confirming round\*\*:' docs/domain/glossary.md` — 1 before and after, a declared invariant, the entry having landed at grilling; `tr -s '[:space:]' ' ' < docs/domain/glossary.md | grep -o 'inherits the gating' | wc -l` — 1 before and after, and `grep -o 'A plan already .implemented. owes none' | wc -l` over the same stream — 1 before and after: both declared invariants, since rounds one and two wrote those clauses into the entry rather than leaving them to the prescribed rule edits.
- W2: over the whitespace-normalized `workflow.md`, `grep -o 'unbounded by the cap' | wc -l` — 0 before, 1 after; `grep -o 'records their close, and no session' | wc -l` — 1 before, 0 after, paired with `grep -o 'on a plan, once the confirming round has run' | wc -l` — 0 before, 1 after: the removal and the arrival, since a removal alone proves only that the sentence moved (round three's F4).
- W3: `tr -s '[:space:]' ' ' < plugins/working-process/rules/spec-plan-lifecycle.md | grep -o 'never stands in for the' | wc -l` — 0 before, 1 after.
- W4: `tr -s '[:space:]' ' ' < plugins/working-process/skills/process-status/SKILL.md | grep -o 'two confirmed hits share one document' | wc -l` — 0 before, 1 after; `grep -c 'Unresolved verdict and Chain debt' plugins/working-process/skills/process-status/SKILL.md` — 0 before and after, a declared invariant: round four's F2 replaced the class pair with the shape, so the skill must never name them.
- W5: `grep -c 'decline — of the gate' docs/domain/glossary.md` — 1 before, 0 after.
- W6: `grep -c '^## Branch naming' plugins/working-process/rules/workflow.md` — 0 before, 1 after; the same command against `ticket-frontmatter.md` — 0 before and after, a declared invariant, since round one moved the section out of that rule; `tr -s '[:space:]' ' ' < plugins/working-process/rules/ticket-frontmatter.md | grep -o 'branch naming convention' | wc -l` — 0 before, 1 after (the pointer that replaces it).
- W7: `ls plugins/working-process/rules/*.md | wc -l` — 5 before, 6 after; `grep -c 'docs/domain/\*\*' plugins/working-process/rules/propagation-duties.md` — no file before, 1 after; `grep -c 'six rule files' plugins/working-process/README.md` — 0 before, 1 after; `claude plugin validate plugins/working-process` passes before and after — a declared invariant, since a wave that only adds a rule file must not be the thing that breaks the manifest.

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

### 2026-09-11 — architect, fable 5.1, concerns (round 2, diff-scoped)

Scoped to round one's fix wave. Every citation checked before anything
was written here: the four spec-arm sentences, the one H2 in
`workflow.md`, and each rule and glossary line the report names.

- fixed 2026-09-11 — [Important] the implemented-document decline of round one's M3 landed in decision 5 and the owner leg but not in the annotation-bullet clause the same wave prescribes, which forbids the annotation absolutely until the latest heading is full-document — so the plan it was meant to free would sit on the Unfinished-work list for good; license: decision 5's own ruling, which grants that decline, and the lifecycle rule's clause amending an `implemented` document in frontmatter only, which leaves the annotation the sole lever; the plan clause now carries the exception where the prohibition is
- fixed 2026-09-11 — [Minor] the Chain debt analogy carried derivability onto a `blocking` close, which the glossary defines as Adjudication — the developer's own act; license: that entry; decision 5 now says a session derives the `concerns` decline and never the adjudication
- fixed 2026-09-11 — [Minor] W1 said three sentences rename the spec's pair-offer arm where `workflow.md` carries four, and the check anchored only one of them, so `:419` would have survived and the term would name two objects again; license: the enumeration itself, `:416`, `:419`, `:421`, `:424`; the item now says four and names them, and the check gains the second anchor
- fixed 2026-09-11 — [Minor] the **Confirming round** entry, amended in this wave, states the obligation unconditionally while decision 5 exempts an implemented plan, where the sibling Chain debt entry carries its own exception in its definition; license: decision 5's ruling and that sibling's shape; the entry now carries the clause
- fixed 2026-09-11 — [Minor] the gating sentence of round one's F1 was placed in the diff-scoped-LGTM section while the terminators it names point nowhere at it, and the all-Minor bullet still says the resolution annotation records the developer's close — untrue on a plan once W1 lands; license: the cap bullet's own precedent of carrying plan-specific text, and that bullet's sentence being falsified by this wave; W2 now widens to the all-Minor bullet and says why the terminator's own bullet is where a session reads
- fixed 2026-09-11 — [Minor] W6 prescribed a paragraph "near step 1" while its check anchored an H2, and the flow's numbered steps name no branch-creation moment; license: the file's own structure — one H2, `## Dispatching a verdict agent`; the item now prescribes a `## Branch naming` section placed after the flow and before that H2
- signal 2026-09-11 — a third round has moderate value: the F1 repair is one clause in two places and the rest are one-line fixes, so if it runs it should be a short diff-scoped read of the F1 and F5 repairs; the leftovers after it are wording, one number and one heading

### 2026-09-11 — architect, fable 5.1, concerns (round 3, diff-scoped)

Scoped to round two's fix wave, as that round's stop signal asked. Every
citation checked first, the reviewer's note on this ledger's own seam
included.

- fixed 2026-09-11 — [Important] round two's F1 repair carried the implemented-plan exception into four places but the verdict distinction into only one: the owner-leg prescription said "in the shape the Chain debt leg already uses", a shape neutral about the verdict because that leg knows only `LGTM`, so read literally it licensed a session to write `blocking (adjudicated <date>)` — the developer's own act; license: decision 5's ruling and the glossary's **Adjudication** entry; the W1 prescription now carries the distinction into the rule text a session reads instead of leaving it in the spec
- fixed 2026-09-11 — [Minor] W6's placement phrase "after the numbered flow and before `## Dispatching a verdict agent`" spans five paragraphs, and the literal reading would pull them all under the new heading; license: the file's own structure, those paragraphs belonging to the flow rather than to branch naming; the item now says "immediately before" and says what that buys
- fixed 2026-09-11 — [Minor] the spec-arm rename enumerated four sentences and anchored two, leaving `:416` and `:424` to survive the edit — the same partial-anchor class round two had just repaired one layer down; license: the enumeration itself; the check now carries one anchor per renamed sentence
- fixed 2026-09-11 — [Minor] W2's check proved only the removal of the all-Minor bullet's close sentence and never named the clause replacing it, where every W1 check pairs a removal with an arrival; license: those checks' own shape; W2 now names the qualifier and the check anchors it 0 to 1
- hit fixed 2026-09-11 — reordering the ledger at the previous commit moved only the first line of round one's multi-line `signal`, leaving its three continuation lines under round two's signal; the reviewer reported it as an integrity note rather than a finding, and the lines are back under their own
- signal 2026-09-11 — a fourth round would not repay: what remains after this wave is a clause, a placement phrase and two anchors, none of which needs design judgment. The residue class — partial anchors and drifted ledger lines — is what an integrity audit proves with two quotes, so the chain debt is better discharged at the consumption gate by the audit arm than by another round

### 2026-09-11 — architect, fable 5.1, blocking (round 4, full-document)

Dispatched full-document against the reviewer's round-three stop signal,
on the developer's order, and the brief said so rather than letting the
override read as an oversight. The gate returned `CLEAN` beforehand.
Every citation checked, including the two that prove F1 — the loop
rule's own prescription for a plan mid-loop.

- fixed 2026-09-11 — [Important] W1's recovery sentence generalized to "latest round heading is diff-scoped, whatever its verdict", which makes a plan merely mid-loop between two diff-scoped rounds indistinguishable from one owing a confirming round — and for that state the loop rule prescribes something else, "Held set empty — dispatch the next round without asking, within the cap", every later round diff-scoped; the `LGTM` case was sound because that heading is itself an end; license: decision 1's own ruling, which keys on what ends a plan's rounds rather than on the heading alone; the sentence now carries that trigger and keeps "next touch" for `LGTM`
- fixed 2026-09-11 — [Important] W4 wrote the co-firing line as a pair of class names restating that they are one debt seen from two sides, putting the relationship in a second place and making the skill carry process knowledge it declares it has none of — it takes the owner from the entry, never from its own knowledge, and a later erratum changing the owner leg would have to edit the skill too; license: decision 3's own ruling, that the line is derived from the mapping without judging it, which "one debt" does not satisfy; W4 now publishes the shape — two confirmed hits sharing one document — and the check anchors that, with the class pair a declared invariant at zero
- fixed 2026-09-11 — [Minor] the Problem section attributed all seven items to the two outside cycles and pointed at two memory entries as the record, while those entries carry only W1, W2 and W7; W3, W4, W5 and W6 are this repo's own; license: those entries' contents; the section now splits three from four and names which is which
- fixed 2026-09-11 — the line enumeration W1 publishes is a snapshot that W6's heading will shift, and nothing said whether the two edits are ordered — the reviewer raised it as a line for the integrity class rather than as a graded finding, which is why this line carries no severity; ruling: 2026-09-11; the item now says the numbers are a snapshot and that the checks anchor text, so neither edit depends on the other's order
- signal 2026-09-11 — a fifth full round would not repay, and this is the second round to say so: both remaining repairs were clauses needing no whole-document context, and the residue class — provenance, a snapshot of line numbers — is what an integrity audit proves with two quotes more cheaply than a round. The reviewer noted that `blocking` suspends autonomy, so whether a short diff-scoped round or the audit follows is the developer's call

### 2026-09-11 — integrity audit, fable, at the consumption gate

Dispatched on a fresh context before plan-writing, on the developer's
call and on the reviewer's twice-given signal that the residue belonged
here rather than to a fifth round. Coverage 374 of 374 lines. It returned
eight defects, each proved by two quotes, and twelve ranked implementer
questions; the defects are disposed below and the questions are the
plan's input. Not a verdict: the audit grades nothing and stamps
nothing, so `architect: blocking` stands until it is closed.

Seven of the eight were one shape — a claim repaired in one place and
left stale in its neighbour — which is the shape four review rounds
passed over and this read caught in one pass.

- fixed 2026-09-11 — W1 added the gating sentence beside `workflow.md`'s "That round runs under the loop's standing consent like any other" without saying the shipped sentence goes, so the rule would carry both, and the check anchored only the arrival — against this document's own rule that a W1 check pairs a removal with an arrival; license: that rule, stated in the Verification section; W1 now says the sentence is replaced and keeps what it also carried, and the check carries the removal anchor
- fixed 2026-09-11 — the exclusion on the missing decline path said "next touch" catches an annotation written early, while round four had just reserved "next touch" for the `LGTM` heading; license: W1's own rewritten trigger, in which an annotation is one of the events that end a plan's rounds; the bullet now says the annotation is itself the trigger
- fixed 2026-09-11 — decision 3 still described the report line as a named pair of classes that are "one debt seen from two sides", the exact words round four's F2 removed from W4; license: decision 3's own ruling, that the line is derived from the mapping without judging it; the decision now states the shape and records that round four sharpened it
- fixed 2026-09-11 — the Problem section's first paragraph said seven items survived 0.16.0 from the two outside cycles while its second paragraph, rewritten in round four, said three; license: the two memory entries, which carry three; the first paragraph now splits the same way
- fixed 2026-09-11 — the decisions preamble said each was put to the developer with its options and cost, and decision 2 alone recorded no declined alternative; license: that preamble; decision 2 now records the option left on the table and why the third was refused on construction rather than preference
- fixed 2026-09-11 — the Scope preamble called both landed glossary changes "applied at grilling" while the **Confirming round** entry was minted there and amended by rounds one and two; license: those rounds' own `fixed` lines; the preamble now says what landed when
- fixed 2026-09-11 — W7's `claude plugin validate` check stated only an after value where the section's preamble requires both; license: that preamble; the check is a declared invariant, passing before and after, on the ground that adding a rule file must not be what breaks the manifest
- fixed 2026-09-11 — four of the twelve implementer questions were answerable from written decisions and are answered in the document rather than left to the plan: what event ends a plan's rounds for a dispatching session and not only for the re-offer (Q1, licensed by the terminators, which are what end them); the **Round heading** entry carrying decision 4's continuity clause so the term reads alone (Q9); this ledger's one severity-free line saying why it has none (Q10); and `revises:` dropping `2026-08-27-audit-agents-design.md`, since that design anticipated an author-facing mirror of the duties and W7 is that mirror rather than a departure from it (Q11, licensed by the lifecycle rule's definition of `revises:` as a claim that the named design no longer matches what shipped). The remaining eight are the plan's agenda: full replacement text for three rule passages, W7's rule body, W6's placeholder and renaming duty, W3's paragraph and sentence, W4's literal line shape, and W2's sentence placement
- fixed 2026-09-11 — the Verification preamble claimed every check normalizes whitespace while four were plain `grep -c`, one of them anchoring a line ending with `$` — which would pass or fail on where an editor wrapped the new sentence, the precise dependency the claim denied; license: the preamble's own claim; the preamble now says which checks are plain and why, and the line-ending anchor is replaced by a normalized phrase
