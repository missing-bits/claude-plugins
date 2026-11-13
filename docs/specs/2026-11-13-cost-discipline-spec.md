---
ticket: none
date: 2026-11-13
status: implemented
decisions: registered
architect: concerns (resolved 2026-11-13)
branch: feature/cost-discipline
base: develop
---

# Cost discipline — reviews that ask whether a mechanism is worth having

Every review the working process runs asks how a document breaks. None
asks whether what it adds is worth having. This spec makes the
reviewers and the session's triage ask that question, and leaves the
decision to cut scope with the developer. It is package 2b-core of the
release queue: cost discipline without process weights.

## Problem

In ai-devcontainer v1, every review wave grew its plan and none shortened
one: four plans reached 6,714 lines. A search of every architect,
plan-adversary, integrity and Codex record from that work for
*over-engineer*, *YAGNI*, *KISS*, *simplif* and *scope creep* returns no
hits. Four mechanics made the documents grow:

- **A finding was fixed by adding a mechanism.** A Minor about
  `--ssh-retarget` became the new task `profile:ssh-retarget`, marked
  "(Recommended)" and accepted; sixteen minutes later the developer asked
  why it existed. An override validator grew to 629 lines because each
  bypass a reviewer found widened it; nobody proposed narrowing the input
  it accepted.
- **Recommendations favoured completeness.** The developer accepts the
  session's recommendation almost every time, so a recommendation acts
  as the decision. Nothing asked it to prefer the smaller option.
- **The verdict threshold kept code-dense plans blocked.**
  `blocking` = ≥1 Critical or ≥2 Important. v1 ran 17 plan-adversary
  rounds and reached LGTM in none. In v2, a 575-line KISS plan went
  `blocking` three times with no Critical finding, though every fix was
  licensed or a one-line ruling.
- **A requirement licensed unlimited mechanism.** One plan's rollback
  engine followed from three requirements in the design spec. Three
  `blocking` rounds in a row found defects in rollback logic the
  previous round's fixes had added. No step asked whether the
  requirement should be cut.

v2 worked because the developer did the cutting by hand. The reviewer
brief carried "block only on data loss, privacy or security, a broken
requirement; do not propose new mechanisms", and the architect returned
LGTM with ten one-line Minors.

Sources: the ai-devcontainer phase A and B analyses and the Codex
over-engineering review, kept in the developer's local process records.

## Goals, non-goals, anti-goals

Goals:

- A reviewer that proposes a fix adding a mechanism also names a cheaper
  way out.
- A fix that adds a mechanism reaches the developer before it lands, with
  the smaller option recommended where it meets the requirements.
- Only a Critical finding blocks; an Important is `concerns`.
- A mechanism the developer dropped does not come back without new
  evidence.
- The developer sees, every round, how much the document grew.

Non-goals:

- Process weights: the `process.weight` key, the `process-weight:` field,
  a `light` mode. They are package 2b-weight, held until this package's
  dogfood shows a need.
- A settings key for the verdict threshold. It waits for a project that
  wants the stricter threshold back.
- Growth thresholds or tripwires. The evidence calibrates none.
- A reviewer pass asking whether native behaviour covers a requirement
  at the spec stage. The question D8 adds while drafting is the only
  spec-stage change.
- Rules for an outside co-reviewer such as Codex.
- Asking the consultation question on every path; it returns to the
  errata package.

Anti-goals — the change fails, even if it works, when:

- it adds more mechanism to the process than it removes from documents;
- a data-loss, security or broken-requirement defect passes without
  `blocking`, outside a domain checklist's own grading (see *Verdict
  threshold*);
- the developer is interrupted over findings that carry no decision.

## Decisions

- **D1** — Where a finding's suggested fix adds a mechanism, the
  architect and the plan-adversary name at least one cheaper
  alternative beside it, within the same finding; the plan-adversary
  also names the requirement that forces the mechanism. Argued in
  *Reviewers*.
- **D2** — A diff-scoped round attacks the previous wave's fixes for
  added mechanism as well as for defects. Argued in *Reviewers*.
- **D3** — The architect reports a requirement whose realization forces
  mechanism out of proportion to its value as a finding that suggests
  relaxing the requirement. Argued in *Reviewers*. withdrawn the
  mechanism a requirement forces appears in the plan, so the duty moves
  to the plan-adversary's D1 alternatives, and the architect's
  over-engineering lens covers the design side, ruling: 2026-11-13;
  replaced by D1
- **D4** — Triage holds every fix that adds a mechanism, whatever the
  finding's severity and whether or not a license exists. Argued in
  *Triage*.
- **D5** — A held finding's recommendation prefers the smaller option
  where it meets the requirements; "accept as a documented limitation"
  is always among the options. Argued in *Triage*.
- **D6** — `blocking` means at least one Critical finding, in both
  cards; two Important findings no longer block. Argued in *Verdict
  threshold*.
- **D7** — In the plan-adversary's scale, a requirement the plan does
  not deliver is Critical: a "done when" no phase delivers, a `new`,
  `changed` or `retired` part of a technical design no task covers, and
  a registered decision realized only in part. Argued in *Verdict
  threshold*.
- **D8** — While drafting a design spec, before its first review, the
  session asks the developer for a size target, what is dropped, what
  native behaviour already covers, and which risks are accepted; the
  answers land in the spec's non-goals and constraints. Argued in
  *Before drafting*.
- **D9** — A mechanism the developer drops is recorded as a non-goal in
  the design spec or as a `ruling:` line in the ledger; both reviewers
  treat the spec's non-goals as settled and re-raise one only with new
  evidence; a re-raised non-goal is held, the non-goal quoted in
  `counter:`. Argued in *Dropped stays dropped*.
- **D10** — A `declined` line for a finding the developer deferred ends
  with `; backlog`. Argued in *Backlog*. withdrawn it answers no goal,
  and a `declined` line's own clause can say "deferred", ruling:
  2026-11-13
- **D11** — The relay header carries the reviewed document's size,
  without its ledger, and the change since the previous round. The
  dispatch record's header gains a size line to make the change
  derivable. Argued in *Net growth*.
- **D12** — The architect's Critical also covers a stated requirement
  the design does not meet and a data-loss or security defect. Argued
  in *Verdict threshold*.

## A mechanism

A fix adds a mechanism when it introduces something the document did not
have: a part, a task, a command, an option or flag, a state file or
field, or a recovery path. Giving an existing part a new check, branch
or case adds one too, whichever way it moves what the part accepts,
since that is how v1's validator reached 629 lines: each fix closed a
bypass by adding a check. Rewording, correcting a value, deleting text,
removing an input, option or case, and adding a test or a verification
step that brings no new command or script add none. This is the definition D1, D2
and D4 share. Two files carry it: `PERSONA_COMMON.md`, which both cards
read before reviewing (the architect through its persona file), and the workflow rule, for the session's triage. The
glossary gets no entry: "mechanism" has ordinary uses in bound text, and
the defined phrase is "a fix adds a mechanism".

## Reviewers

The architect's persona already carries an over-engineering lens, but it
reads the design as a whole. A fix that adds a mechanism usually arrives
as the answer to one finding, and diff-scoped rounds then attack only
whether the fix is correct, so the lens never meets it.

D1 puts the cost question inside the finding that would cause the
mechanism. Beside a fix that adds one, the reviewer names at least one
cheaper alternative: narrowing the input, relying on the tool's native
behaviour, accepting the gap as a documented limitation, or deferring
it. The alternative sits in the same finding, so no separate list, grade
or section appears. The plan-adversary gets the same duty, since in v1
most mechanism-breeding findings were its own. It also names the
requirement that forces the mechanism, with `origin: design-spec`: the
mechanism a requirement forces first appears in the plan, where the
rollback engine of *Problem* did. Naming stays inside the card's
boundary, under which a finding whose origin names a judged document
"proposes no change to that document"; the workflow rule holds such a
finding, and the developer decides whether to relax the requirement.

D2 adds one question to the diff-scoped brief's "attack the previous
wave's fixes first": did a fix add a mechanism the finding did not need?

D3 first gave the architect this duty. The architect reads the design
spec, where a requirement's mechanism is not yet written, and its
persona's over-engineering lens already asks the design-side question,
so D3 was withdrawn in favour of the plan-adversary's alternative above.

## Triage

The workflow rule's triage decides by license: a fix the session can
cite a written decision for is self-fixable. A requirement licenses any
amount of mechanism that enforces it, which is how v1 grew.

D4 adds one hold that a license does not lift: a fix that adds a
mechanism is held for the developer, whatever its severity. Most such
fixes would reach the developer anyway; the hold closes the path where
a licensed Minor became a task.

D5 sets the default of the held line's `options:`. The session
recommends the smaller option where it meets the requirements, and
"accept as a documented limitation" is always offered. The
recommendation still names the mechanism when nothing smaller meets the
requirement.

Two kinds of fix stay outside D4. A fix that carries out a `ruling:`
is not held again, because the developer has already decided it. A
propagation-gate hit is not held either, because its derivation
licenses its fix: a coverage hit that writes a missing task realizes a
decision the spec already registered. Where the session cannot tell
whether a fix adds a mechanism, it holds the fix, as the workflow rule
already prescribes for any doubtful case.

The held set grows by exactly the fixes D4 catches, and the round's one
batch carries them, so each round still interrupts the developer at most
once. A loop interrupts more often, by design: a round whose only
mechanism-adding fixes were licensed used to continue unasked, and now
stops for the developer. The relay header's count of decisions follows:
the workflow rule derives it from the findings with no license, and it
gains the fixes D4 holds, so the count and the round's `held` lines
still agree.

## Verdict threshold

Both cards define `blocking` as at least one Critical or two Important
findings (`plan-adversary.md`, `architect.md`). D6 drops the second leg
in both, so an Important finding gives `concerns`. `concerns` is the
autonomy zone, so a plan with Important findings and no Critical stays
inside the loop instead of suspending it.

The two scales differ. The architect's Critical covers "the design
cannot deliver its stated purpose" but names neither a single unmet
requirement nor a data-loss or security defect; both would be
Important, "a boundary or choice that forces rework if built as
designed". D12 adds both to its
Critical. Its requirement leg stays open on purpose: any single unmet
requirement blocks, as v2's brief asked, where D7 bounds the
plan-adversary to three enumerated cases. The plan-adversary's Critical names data loss, security,
a production outage and a broken deploy, and grades three undelivered
requirements as Important: a "done when" no phase delivers (dimension
1), an uncovered part of a technical design (dimension 5), and a
registered decision realized only in part (dimension 6). D7 adds the
undelivered requirement to its Critical and regrades those three, so
dropping the second leg lets no broken requirement through. The other
Important findings in those dimensions — a missing `technical-design:`
entry, an unknown `change` value, a redefined contract — describe a
defect in the documents rather than an undelivered requirement, and stay
Important.

One path stays open, as a documented limitation. A domain checklist's
severity wins over the generic scale, and the Salesforce plan-review
checklist grades three security-model defects Important — a missing
org-wide default or FLS, `without sharing` without a justification, a
capability on a profile. Today any two of them in one plan block it; after D6 they give
`concerns`. The loop still triages them, and a domain plugin that wants
one to block regrades it in its own checklist.

## Before drafting

v2's brief carried size targets, a list of what v1 dropped, accepted
risks and expectations for first use, and the documents written from it
stayed short. D8 makes the session ask for those answers while it
drafts the design spec, at step 1 of the workflow rule, before the
spec's first review. The answers go into the spec's non-goals and
constraints, never into a separate brief file, so every reviewer reads
them, D9 protects them, and no stamp goes stale. Asking later, at the
consumption gate, would edit a spec that a verdict and an `integrity:`
stamp already certify.

## Dropped stays dropped

The ledger already settles a line carrying `ruling:`: a later round may
re-raise it only with new evidence. A drop agreed in conversation but
never written down has no such protection. D9 requires the drop to be
written, either as a non-goal in the design spec or as a `ruling:` line,
and adds one sentence to `PERSONA_COMMON.md`, which both cards read
before reviewing:
the spec's non-goals are settled,
and a finding that would reintroduce one says what new evidence it
brings.

A non-goal carries no date, so a re-raise cannot be folded against it
the way the lifecycle rule folds a re-raise of a `ruling:` line. The
session holds it instead, quoting the non-goal in `counter:`; that
follows from the workflow rule as it stands, which holds a finding the
session believes is wrong with its counter-evidence, so no new sentence
ships for it. `PERSONA_COMMON.md` carries only the reviewer's half,
beside the definition: non-goals are settled, and evidence counts as
new against the spec's own text.

## Backlog

D10 proposed a `; backlog` ending on `declined` lines for deferred
findings. It answered no goal, and two glossary entries ban the word ("backlog item", "backlog"), so
it was withdrawn: a `declined` line's own clause can say the finding is
deferred, and D5's "accept as a documented limitation" stays.

## Net growth

v1's plans grew 30–94 % across their reviews, and nobody saw the numbers
until the retrospective. D11 shows them at every relay: the reviewed
document's line count, counted from the end of the frontmatter and
excluding the `## Review rounds` section, and the change since the
previous round's dispatch record of the same document and agent. The
dispatch record's header gains a fifth line, `size: <lines>`, which is
where the previous count comes from. The relay reports the number and
judges nothing. A dispatch with no reviewed document carries no size
line, and a round with no earlier record carrying one reports the size
without a change. Every live rule and glossary entry that calls the
header "four-line" lists its fields instead, size "where a document was
reviewed", so no line count goes false; documents already `implemented`
keep their wording.

## Verification

- Both cards carry the new threshold, and no file in `plugins/` still
  says "two Important" or "≥2 Important".
- A dogfood replays the plan-adversary on the v2 plan as it stood at its
  first round. Expected: no `blocking` verdict, and every finding whose
  fix adds a mechanism names a cheaper alternative.
- A dogfood of one review loop on a scratch spec seeded with a Minor whose
  natural fix adds a task. Expected: the fix is held, its recommendation
  is the smaller option, and the relay header shows size and change.
- The same dogfood seeds a design-level security defect into the
  scratch spec — a requirement or decision that itself exposes data, not
  a failure the architect would have to hunt for.
  Expected: the architect grades it Critical, and the verdict is
  `blocking`.

## Out of scope

- Weights, a threshold setting and growth tripwires (see *Goals, non-goals, anti-goals*).
- Reviewing the rules themselves for size; this package governs
  documents the process reviews.

## Changes by file

- `PERSONA_COMMON.md` — the definition in *A mechanism*; D9's settled
  non-goals, with evidence new against the spec's text; its self-description by counts ("the
  two duties", "All four sections") follows the new content.
- `agents/architect.md` — D1, D6, D12.
- `agents/plan-adversary.md` — D1 with the named requirement, D6, D7.
- `docs/domain/glossary.md` — D11 in the *Relay* entry's header and the
  *Dispatch record* entry's four-line header.
- `rules/workflow.md` — D2 in *Re-dispatch briefs*; D4 and D5 in *The
  review loop*; D4 in the relay header's count of decisions; D8 in step
  1; D11 in the dispatch record and relay bullets; the definition in *A
  mechanism*.
- `CHANGELOG.md` of working-process.
- `.claude/working-process/release-queue.md` (local) — 2b-core status.

## Calls made by the author

- The definition of a mechanism lists six kinds plus widening an
  existing part; deleting, narrowing, tests and verification steps add
  none.
- D11 reads the previous count from the dispatch record rather than
  adding a field to the round heading, whose grammar is closed.
- The plan-adversary gets D1 too, not only the architect, because most
  mechanism-breeding findings in v1 were its own.
- D4 exempts fixes carrying out a `ruling:` and propagation-gate hits;
  a doubtful case is held.
- D11 omits the size line without a document and the change without an
  earlier record.
- D2 lives in the workflow rule's brief composition only; the cards are
  unchanged by it.

## Review rounds

### 2026-11-13 — architect, fable 5.2, blocking (round 1, full-document)

- hit fixed 2026-11-13 — the glossary's *Dispatch record* entry calls the header four-line and *Changes by file* did not list it; added to *Changes by file*
- hit fixed 2026-11-13 — the glossary's *Relay* entry restates the relay header D11 changes; added to *Changes by file*
- hit fixed 2026-11-13 — *A mechanism* named rules and cards as the definition's consumers while *Changes by file* put it in workflow.md only; both cards now carry it
- hit fixed 2026-11-13 — the glossary had no entry for the minted term; *Changes by file* adds a *Mechanism* entry
- hit fixed 2026-11-13 — the lifecycle sentence "Two additions extend those shapes" gains D10's ending and the spec gave no new wording; *Backlog* now says it becomes three
- hit fixed 2026-11-13 — the "four-line" sweep reached implemented documents; *Net growth* limits it to live rules and glossary entries
- hit fixed 2026-11-13 — *Out of scope* cited a *Non-goals* heading that does not exist; it now cites *Goals, non-goals, anti-goals*
- hit dismissed 2026-11-13 — D9's non-goal protection needs a workflow.md brief edit; counter: D9 puts the protection in both cards, which every round reads, and the brief's ledger clause covers ledger lines a reviewer cannot otherwise see as settled (the architect agreed in round 1)
- hit fixed 2026-11-13 — the non-goals called D8 "the brief question"; reworded to the question D8 adds while drafting
- hit fixed 2026-11-13 — the "defer to backlog" option on held lines had no *Changes by file* entry; added under workflow.md with D5
- fixed 2026-11-13 — [Important] F1: anti-goal 2 is not secured: the architect's Critical names no requirement, data-loss or security leg, and domain checklists grade security defects Important, which D6 turns into `concerns`; ruling: 2026-11-13; D12 adds unmet requirements, data loss and security to the architect's Critical, *Verdict threshold* records checklist-graded Importants as a documented limitation, *Verification* seeds a security defect
- fixed 2026-11-13 — [Important] F2: the mechanism definition misses widening an existing part (the 629-line validator) and is unclear on tests and steps; ruling: 2026-11-13; *A mechanism* counts widening an existing part and excludes tests and verification steps
- fixed 2026-11-13 — [Important] F3: D3 sits on the architect, who never sees the mechanism a requirement forces; the plan-adversary does; ruling: 2026-11-13; D1 gives the plan-adversary the requirement-relaxing alternative, D3 withdrawn and replaced by D1
- fixed 2026-11-13 — [Minor] F4+F5: D10 answers no goal and mints "backlog", a word the glossary bans twice; ruling: 2026-11-13; D10 withdrawn, *Backlog* records why, the lifecycle rule leaves *Changes by file*
- fixed 2026-11-13 — [Minor] F7: a re-raised non-goal has no fold and no base for new evidence; ruling: 2026-11-13; D9 and *Dropped stays dropped* hold a re-raised non-goal with the non-goal quoted in `counter:`
- fixed 2026-11-13 — [Minor] F8: three copies of the definition where PERSONA_COMMON.md, read by both cards, would make two, and a glossary term collides with ordinary uses of "mechanism"; ruling: 2026-11-13; the definition moves to PERSONA_COMMON.md and the workflow rule, the glossary entry is dropped
- fixed 2026-11-13 — [Minor] F6: D4 changes the relay header's decision count and the per-loop interruption count; license: D4; *Triage* states both consequences, *Changes by file* lists the relay-count bullet
- fixed 2026-11-13 — [Minor] F9: "says five" is false for a dispatch without a document; license: D11 (no size line without a document); *Net growth* lists fields instead of a count
- fixed 2026-11-13 — the *Verification* dogfood had "not now" write `; backlog`, against *Backlog*; license: *Backlog* and *Calls made by the author*; reworded to "defer to backlog"
- signal 2026-11-13 — one more diff-scoped round earns its cost, attacking the F1 and F2 fixes; Minors only expected after it
- hit dismissed 2026-11-13 — *A mechanism* says two files carry the definition while neither does yet; counter: a design spec states the target state, *Changes by file* prescribes the edit, and F8's "moves" records the spec's change, not a shipped one
- hit dismissed 2026-11-13 — two earlier gate lines and the *Verification* fix line name D10's backlog ending, now withdrawn; counter: ledger lines record what each wave did at the time, and the F4+F5 line records the withdrawal
- hit fixed 2026-11-13 — *Verdict threshold* said "two of them block" of per-finding grades; reworded to "any two of them in one plan block it"
- hit fixed 2026-11-13 — *Verdict threshold* misquoted the architect's Important; now quotes the card in full
- hit fixed 2026-11-13 — *A mechanism* and *Dropped stays dropped* said both cards read PERSONA_COMMON.md first, while the architect reaches it through its persona file; reworded to "read before reviewing"
- hit fixed 2026-11-13 — the non-goal sends the consult question to the errata package while the local release queue still listed it under 2b-core; the queue now moves it to package 5, the spec stands
- hit fixed 2026-11-13 — *Backlog* said the glossary bans "backlog" twice, while one entry bans "backlog item"; reworded to name both entries
- hit fixed 2026-11-13 — the local release queue's 2b-core scope still carried the withdrawn `; backlog` ending; the queue now records it as dropped, its 2b-weight and 2b+ designs left as written

### 2026-11-13 — architect, fable 5.2, concerns (round 2, diff-scoped)

- fixed 2026-11-13 — [Important] R2-1: the F2 definition counted the validator's fixes both as widening and as narrowing; license: the F2 ruling and *Problem*'s validator example; *A mechanism* keys on a new check, branch or case, replaces "narrowing" with removing an input, option or case, and exempts a test or verification step only when it brings no new command or script
- fixed 2026-11-13 — [Minor] R2-2: anti-goal 2 still names the path the F1 limitation accepts; license: the F1 ruling; anti-goal 2 now excepts a domain checklist's own grading
- fixed 2026-11-13 — [Minor] R2-3: D12's "a stated requirement the design does not meet" is open-ended, so a single unmet goal now blocks on the architect where D7 bounds the adversary to three cases; ruling: 2026-11-13; the leg stays open, *Verdict threshold* states that any single unmet requirement blocks
- fixed 2026-11-13 — [Minor] R2-4: D1's requirement-relaxing alternative breaks the plan-adversary's boundary ("proposes no change to that document"); license: plan-adversary.md, *Judged documents: decline*; D1 and *Reviewers* now have the adversary name the requirement, the developer decides whether to relax it
- fixed 2026-11-13 — [Minor] R2-5: the held re-raise of a non-goal sits in PERSONA_COMMON.md, whose readers never triage, while the workflow rule already holds a disputed finding with `counter:`; ruling: 2026-11-13; folding the F7 line; *Dropped stays dropped* derives the hold from the workflow rule, PERSONA_COMMON.md keeps the reviewer half, *Changes by file* follows
- fixed 2026-11-13 — [Minor] R2-6: the seeded security defect tests grading only if the architect hunts for it, which its persona disclaims; license: ARCHITECT_PERSONA.md's own duty; *Verification* seeds a design-level defect
- fixed 2026-11-13 — PERSONA_COMMON.md describes itself by counts the move makes false; license: its own text; *Changes by file* has the counts follow the new content
- signal 2026-11-13 — another architect round does not earn its cost; the leftovers are worth one batch to the developer

Resolved 2026-11-13 without a fresh round: the developer accepted the round-2 recommendations and closed the loop on the reviewer's stop signal; every round-2 finding is `fixed` above.
