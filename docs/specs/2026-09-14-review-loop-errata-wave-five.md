---
ticket: none
date: 2026-09-14
status: draft
grilled: 2026-09-14
architect: blocking
branch: feature/process-wave-five
base: develop
---

# Review loop — errata wave five

Four defects in how a review's result reaches the developer. The loop
decides well and reports badly: a relay arrives as a wall of prose, a
consultation arrives as two walls, a finding names the section it
concerns but never the document it came from, and nothing the relay
condenses survives the session that condensed it.

## Problem

The developer has asked four times, in four different sessions, for the
same thing: *summarise the agents' findings in short bullets, which
decisions are mine* (2026-08-19); *what did the architect return — so
only minor finds, nothing touching design or critical decisions*
(2026-08-25); *a short, substantive bullet list of the code review*
(2026-09-07); and, first, simply *too much reading, can you shorten it*
(2026-08-10). Four asks for one missing contract.

The rules define a relay's floor and nothing about its shape. The floor
is a safety property rather than a style: a relay is the developer's
standing veto, so a finding nobody printed is a finding nobody could
overrule. Shape was left to the session, and the session chose prose.

A second defect sits beside it. Consultations return contributions
rather than findings, and two personas answering one briefing produce
the longest output the process generates. The rule governing that relay
reads `Relay each contribution attributed and substantially verbatim`
and says nothing more. Its own spec says more — see decision 2.

The third defect is about provenance rather than length. After an
adversary round found a runbook order contradicting the spec's delivery
split, the developer asked which documents were up for correction
(2026-08-17); on 2026-08-26 they ordered both sweeps by hand, because
nothing in the report said which document a finding belonged to. The
adversary's finding schema carries `section` and names no document, the
ledger records dispositions on the reviewed document alone, and the
propagation auditor catches an invented name rather than a misplaced
decision.

The fourth defect is what makes the first two safe to fix. A relay may
condense only what a reader can still recover, and today the full text
lives in the session alone. This repo has measured that failure twice
in one day: a requirement stated in a dispatch rather than a file was
invisible to the gate meant to check it, and an implementation wave's
only durable account of itself was a ledger written on purpose. Shorten
a relay without a file behind it and the process trades a wall of text
for a hole.

## Decisions

1. **The relay leads with a fixed header, and the finding list is never
   condensed.** The header carries the verdict, the model self-report,
   the finding count by severity, and how many decisions await the
   developer. Each finding then takes one line — severity, origin,
   claim. Narrative may be condensed, and the relay names the agent's
   report file so an expansion is a quotation rather than a
   reconstruction. The floor stays as written.

   The finding line carries what the finding carries. `origin` belongs
   to a plan review, so an architect relay's line reads severity and
   claim: the architect reads one document and every finding it returns
   originates there, making the field a constant. A constant field
   carries no information and invites a reviewer to manufacture variety
   it does not have.

   The count of decisions is derived rather than judged: it is the
   number of `held` lines this round wrote. The ledger grammar already
   defines `held` as the finding that needs the developer, and requires
   `question:` and `options:` on every such line, so the count is a
   count of lines and a later reader can recompute it. Verdicts that
   suspend autonomy — `blocking`, the spent round cap, the all-Minor
   signal — stay out of it: they decide whether the loop continues
   rather than what a document says, and the relay already reports them
   in its own right.

   What makes the second clause load-bearing is new. Claude Code ships a
   built-in `Concise` output style that condenses by default and expands
   on request, which is the mechanism the developer wants for session
   length. It publishes what it never condenses: error reports, security
   warnings, and confirmations of destructive actions. A review relay is
   absent from that list. Length therefore has a second owner now, and
   the rule must name what that owner may not eat. `ruling: 2026-09-14`

2. **A floor sits where its unit has a shape.** A verdict relay keeps
   its floor in the relay: a finding arrives with a `claim` slot, so a
   relay carries every one of them in one line each and the veto stays
   whole however many arrive. A consultation's floor moves to the file:
   a contribution is prose with no delimited unit, so "every
   recommendation survives" cannot be carried in a relay at all without
   carrying the whole thing — which is the wall this wave exists to
   remove. The asymmetry is structural rather than numerical: a round
   of twenty findings still relays in twenty lines. The consultation
   relay then carries one paragraph per focusing question — or one per
   briefing, where a single persona was consulted and none was appended
   — and the path to the contribution.

   The move is possible only because decision 5 guarantees the file
   before the relay. Without it the floor would move to the session's
   own memory, which is where it already fails.

   Part of this restores rather than relaxes. The design-personas spec
   (`./2026-07-28-working-process-design-personas-design.md`,
   `status: implemented`) grants the compression: *Compression is
   allowed; merging is not. The checkable floor: every recommendation
   and every named risk survives, and text from two personas never
   lands in one bullet.* The shipped rule carries the floor and drops
   the permission — the word `compression` appears nowhere in
   `workflow.md` — so a rule read literally says *verbatim*, full stop,
   which is why consultation relays grew into walls.

   What this wave changes beyond that restoration is the floor's site
   for consultations alone, and it says so rather than hiding the
   change inside a restoration. The floor's content is untouched: every
   recommendation and every named risk still survives, and two personas
   still never land in one bullet — in the file. `revises:` stays
   absent even so, since the design-personas document's design is not
   superseded: its floor holds, at a place that document could not have
   named, because no file existed then. `ruling: 2026-09-14`

3. **The adversary emits the origin.** The finding schema gains
   `origin` beside `section`, valued `plan`, `spec`, or `both`. The
   reviewer saw the contradiction and knows which document is wrong;
   the dispatcher, who did not, is the one who had to ask. Naming the
   document a defect traces to is not a design review of the spec, so
   the card's `Specs are out of scope` boundary holds and says so.

   The triage consequence is a specialisation rather than a new axis:
   a finding originating in the spec is `held` unless a written
   decision licenses the edit. Triage already holds whatever no written
   decision licenses; what this adds is that spec origin is itself a
   reason to hold, since editing a spec from inside a plan review is
   design work.

   `both` holds like `spec`, and the `held` line names in its `options:`
   which half is fixable at once. A finding whose origin is both
   documents usually means the spec decided badly and the plan
   implemented that decision faithfully, so its plan half is often
   trivial and its spec half never is. Splitting the disposition would
   need a ledger line to carry two authorizers, which the grammar
   forbids and this wave does not reopen; `options:` already carries the
   options and the session's recommendation, so one answer licenses both
   halves.

   The field is named `origin` rather than `owner` because this process
   already spends `owner` on an actor: the Unfinished-work list's third
   leg names who makes the next move, six times over, and
   `review-reports.md` calls the author of a report the run's owner.
   Grilling minted **Origin** in the glossary, with `owner` for a
   document under its `_Avoid_`. `ruling: 2026-09-14`

4. **Two items left this wave during brainstorming, and one was never
   in it.** Both departures are recorded here so a later reader finds
   the reasoning rather than a gap. `ruling: 2026-09-14`

   The ban on process noise in code comments left because the developer
   refused all three of its delivery routes on a better ground than any
   of them: a rule in a distributed plugin imposes one developer's
   preference on everyone who installs it. The guidance belongs to a
   worker a project opts into. It now rides a proposed implementer
   agent, whose card body is neither a brief nor a dispatch and so can
   be lost by neither.

   The `process-status` class for documents living only on an unmerged
   branch left because measurement refuted every baseline that would
   let it travel. Counted on this repo: against `develop`, zero, which
   is correct; against what git itself reports as the default branch,
   twenty-plus, every one healthy; against each document's own `base:`
   field, eighteen false positives, because `base:` records where a
   branch was cut rather than where the document should live. The class
   needs the project's integration branch named, and the
   `process-status` contract forbids rewriting a published command.
   Its live instance is also gone, so nothing remains to test against.

5. **A report is written to disk before it is relayed.** The relay may
   condense narrative only because the full text stays recoverable, and
   a copy living in the session dies at the next compaction — twice
   over in this repo's own history. So the dispatcher writes the
   agent's report to a file, then names that file in the relay.

   The store is `.working-process/`, a git-ignored directory at the
   repository root, materialised with a `.gitignore` containing exactly
   `*` at its first write. This is a declaration rather than a
   first-create question: the artefacts are ephemeral by construction,
   so the mode follows from what they are and no project is asked.

   One directory per subject, named for it — `<stem>`, the reviewed
   document's basename without its extension. A consultation carrying
   no document takes its subject as the stem. Grouping by subject
   rather than by agent makes one wave one `ls` and one deletion, and
   it follows the shape `subagent-driven-development` already uses for
   its own workspace.

   A subject becomes a stem mechanically: the briefing's own naming of
   it, kebab-cased and capped at sixty characters. The briefing already
   has to name the subject, so nothing is invented. The limit is worth
   stating — two sessions phrasing one subject differently produce two
   directories — and it is small, since a document-less consultation is
   a one-off and a follow-up dispatcher sees the directory already
   there.

   Inside, the file names its agent and one discriminator:

       .working-process/<stem>/<agent>-round-<N>.md
       .working-process/<stem>/<agent>-<date>-<HH-MM-SS>.md

   A verdict agent takes the round ordinal, which the ledger already
   owns — except where it reviews no document and so has no ledger to
   own one, as an `architect` dispatch on a bare question does; that
   dispatch takes the timestamp shape. A consultation takes the
   timestamp too, because a consultation records nothing and so has no
   ordinal to derive, and because several consultations of one persona
   on one subject in one day are expected — a follow-up is a fresh
   dispatch rather than a resumption. The timestamp also orders them,
   which a counter would not.

   Where a name is already taken, the new file appends the timestamp.
   That covers the superseded round the rules already describe, whose
   stale result is relayed and never stamped: the two rounds share an
   ordinal, and the rule resolves it mechanically instead of asking a
   session to judge which report is the stale one. `ruling: 2026-09-14`

## Scope

1. **W1 — the relay header and the uncondensable list.**
   `workflow.md`, the relay bullet under *Dispatching a verdict agent*.
   The bullet gains the header's contents, the one-line-per-finding
   rule, and the report-file pointer. It states that condensation
   reaches narrative alone, whatever a session's output style says.

2. **W2 — the consultation relay shape and its floor's site.**
   `workflow.md`, the *Dispatching a consultation* paragraph. One
   paragraph per focusing question — or per briefing, where none was
   appended — then the path to the contribution.
   The paragraph names where the floor is met — compression yes,
   merging no, every recommendation and every named risk surviving in
   the file — so a reader meets the floor and its site together.

3. **W3 — the origin field.** Three sites, edited together:
   `agents/plan-adversary.md` gains `origin` in the `Output` schema
   with its three values and one sentence placing it inside the card's
   existing spec boundary; `workflow.md` gains the triage sentence
   decision 3 defines, beside the existing license clause; and
   `docs/domain/glossary.md` carries the **Origin** entry grilling
   already minted.

4. **W4 — the report store.** `workflow.md`, the verdict-agent
   dispatch bullet list and the consultation paragraph: both gain the
   write-then-relay duty and the path shape decision 5 defines. The
   store's ignored mode is stated where the path is, so a reader never
   meets the path without the mode.

## Out of scope

- **Session length.** The `Concise` output style is configuration the
  developer sets, and this wave neither ships a style nor mentions one
  in a rule. A plugin *can* ship output styles, and `force-for-plugin`
  would override the user's own setting; a process plugin dictating a
  global response voice exceeds its remit.
- **A per-agent output style.** Not possible. Seventeen agent
  frontmatter fields are supported and none sets one; a subagent runs
  its own system prompt, so the session's style does not reach it
  either. An agent's response shape comes from its card body alone.
- **The relay of audits.** `propagation-auditor` returns located hits
  or one token, and `integrity-auditor` returns a structured report.
  Neither is prose that grew, so neither earns a shape this wave, and
  neither writes to the store either: a gate's hits already land in the
  ledger as `hit fixed` and `hit dismissed` lines, and an integrity
  audit's dispositions land as the edits it causes plus the
  `integrity:` stamp. Their durable home exists, so decision 5 would
  give one fact a second one.
- **A code review's reply.** One of the four asks in *Problem* — the
  short bullet list of a code review, 2026-09-07 — lands on a different
  surface: `review-reports.md` governs the run's reply and already
  prescribes part of it, one line per proposed rule. Giving the reply a
  shape is the same idea one rule over, and it belongs to a wave of its
  own. Admitting it here would repeat the scope creep wave four paid two
  review rounds for.

## Verification

Each check names the file, the phrase, and the value expected after the
change. Phrases normalise whitespace first, so a match survives the
wrap.

- `workflow.md` contains the header's four elements in the relay bullet,
  and one phrase naming the finding line as uncondensable: expected 1.
- `workflow.md` contains `compression`: expected ≥ 1, where today it is
  0 — the check that proves decision 2 landed.
- `workflow.md` contains a phrase naming one paragraph per focusing
  question: expected 1.
- `plan-adversary.md` contains `"origin"` inside the `Output` block:
  expected 1, with its three values on the same line.
- No `owner` names a document in `plan-adversary.md` or `workflow.md`:
  expected 0, the check that proves the collision stayed resolved.
- `plan-adversary.md` still contains its spec-boundary sentence:
  expected 1, an invariant this wave must not disturb.
- `workflow.md` contains the spec-origin triage sentence: expected 1.
- `workflow.md` contains `.working-process/` and the two filename
  shapes: expected 1 each, and the word naming the store ignored: 1.
- `glossary.md` contains an `**Origin**:` entry: expected 1.
- `claude plugin validate` passes for the plugin and the marketplace:
  an invariant.

## Review rounds

### 2026-09-14 — architect, fable 5.1, blocking (round 1, full-document)

- hit fixed 2026-09-14 — the spec cited seven `Owner:` legs where the Unfinished-work list carries six; recounted against the list's entries and corrected to six
- held — [Important] the header's decisions count is derived from `held` lines that do not exist at relay time: `open` is written at stamp time and triage follows the stamp, so the header forecasts triage rather than counting lines; question: does the header count findings the session can cite no license for, computed before any line is written, or does the count leave the header for the held batch?; options: (a) redefine as unlicensed findings and make the later `held` count the check that must equal it — my recommendation, since it keeps one number in the header and turns the ledger into its verification; (b) move the count into the held batch, which is where those decisions are actually put, leaving the header three elements
- held — [Important] `.working-process/` is a Process directory by the glossary's own definition, and the spec declares its mode without amending the class or the rule that owns the first-create question; question: earn the exception at the class, or place the store where the existing exception already applies?; options: (a) move the store under `.claude/working-process/`, inside the carve-out for configuration directories that the glossary already grants and Private memory already uses — my recommendation, one precedent, no glossary edit; (b) amend the **Process directory** entry and `process-artifacts.md` to name the store a derived, re-creatable cache outside the class
- held — [Important] decisions 2 and 5 disagree about what the file is: decision 2 moves a floor into it because decision 5 "guarantees" it, while decision 5 calls it ephemeral by construction and gives it no lifetime; question: what bounds the guarantee, and is that bound acceptable for the one artefact with no ledger behind it?; options: (a) state the lifetime in decision 5 — this checkout, until the `<stem>` directory is deleted — and have decision 2 cite the bound rather than a guarantee, my recommendation; (b) keep the consultation floor in the relay and move only its narrative to the file, which costs the wave its main saving; (c) give the store a close, as subagent-driven-development gives its workspace one
- held — [Important] the triage clause licenses editing a spec from a plan's fix wave and says nothing about where that edit is recorded or what it does to the spec's standing stamp; question: does a spec-origin fix follow the spec's own lifecycle?; options: (a) one sentence — the disposition line lands under the spec's latest round heading or as the lifecycle rule's resolution annotation, and the plan's line points at it, keeping one authorizer per line across two documents — my recommendation; (b) leave the recording unspecified and let each session decide, which is the state the wave set out to end
- fixed 2026-09-14 — [Minor] decision 2 argued the floor's move from the unboundedness of a contribution's count, where the real asymmetry is the unit's shape; license: `agents/plan-adversary.md`'s Output schema, which gives a finding a `claim` slot a relay carries in one line while a contribution has no delimited unit; the argument now runs from shape and survives a twenty-finding round
- held — [Minor] `revises:` is declined on the design-personas document although that document names the relay as the floor's site and this wave moves it; question: add `revises: ./2026-07-28-working-process-design-personas-design.md`?; options: (a) add it — the reviewer's reading is that the lifecycle rule's definition is met, and the pointer costs one line; (b) keep it absent on the recorded ground that the floor holds rather than lapses; counter: the decline carries `ruling: 2026-09-14`, so this is a re-raise against a recorded decision and belongs to the developer
- fixed 2026-09-14 — [Minor] "one paragraph answering each focusing question" has no value where a single persona is consulted and no focusing question was appended; license: the workflow rule's consultation paragraph, which appends one only when both personas are consulted; the shape now reads per focusing question, or per briefing where none was appended
- fixed 2026-09-14 — [Minor] the filename shape assumes a ledger ordinal for every verdict agent, which an `architect` dispatch on a bare question does not have; license: the glossary's **Consultation** entry, which records exactly that case; such a dispatch now takes the timestamp shape
- open — [Minor] the spec states as settled that a rule's condensation clause outranks an output style's system-prompt instruction, where the relative precedence is unmeasured
- open — [Minor] "report" and "report store" collide with the glossary's **Review report**, a different object under `docs/code-review/`
- signal 2026-09-14 — another round earns its cost: the four Important findings each reshape a sentence in the decision they concern, and repair-born drift between decisions 2 and 5 is the likely failure of that wave, so a diff-scoped round two attacking those fixes is worth a top-tier read; the Minors need no round of their own
