---
ticket: none
date: 2026-09-14
status: approved
grilled: 2026-09-14
architect: concerns (resolved 2026-09-15)
revises: ./2026-07-28-working-process-design-personas-design.md
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
   claim. Narrative may be condensed, and the relay names the dispatch
   record decision 5 defines, so an expansion is a quotation rather
   than a reconstruction. The floor stays as written.

   The finding line carries what the finding carries. `origin` belongs
   to a plan review, so an architect relay's line reads severity and
   claim: the architect reads one document and every finding it returns
   originates there, making the field a constant. A constant field
   carries no information and invites a reviewer to manufacture variety
   it does not have.

   The count of decisions is derived rather than judged, and it is
   derived from what exists at relay time: the findings for which the
   session can cite no license. Triage's license test needs only the
   report and the decisions already written down, so the count is
   computable before any ledger line is. The `held` lines the same
   round later writes are that count's check — they must come to the
   same number, and a divergence means triage found a license the
   relay missed or lost one it claimed. Deriving the count from the
   lines themselves would have the header report a forecast, since
   `open` is written at stamp time and triage follows the stamp, which
   follows the relay. Verdicts that suspend autonomy — `blocking`, the
   spent round cap, the all-Minor signal — stay out of the count: they
   decide whether the loop continues rather than what a document says,
   and the relay already reports them in its own right.

   What makes the second clause load-bearing is new. Claude Code ships a
   built-in `Concise` output style that condenses by default and expands
   on request, which is the mechanism the developer wants for session
   length. It publishes what it never condenses: error reports, security
   warnings, and confirmations of destructive actions. A review relay is
   absent from that list. Length therefore has a second owner now, and
   the rule must name what that owner may not eat.

   That the rule's clause outranks the style's instruction is an
   assumption rather than a measurement. Both reach the model as
   instructions — a style's with every request, a rule's from the
   session's loaded instructions — and their relative precedence is
   unmeasured. The observable that falsifies it: a relay produced under
   the `Concise` style that drops a finding line. A project running the
   style is where the probe belongs, and until one runs it the wave
   proceeds on the assumption rather than on a result.
   `ruling: 2026-09-14`

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

   The move rests on decision 5's dispatch record, and on the bound
   that decision states: the record survives compaction, the session's
   end and a branch switch, and no further. The floor is met on the
   checkout that ran the dispatch. Without the record the floor would
   move into the session's own memory, which is where it already
   fails.

   Part of this re-aligns two shipped copies rather than relaxing
   anything. The obligation exists twice by design: `PERSONA_COMMON.md`
   carries the persona-facing copy and says so — *the dispatcher-facing
   copy of these obligations lives in the plugin's workflow rule; the
   two are edited together*. The persona copy kept the whole contract
   (*substantially verbatim — compression is allowed, merging is not;
   every recommendation and every named risk survives*); `workflow.md`
   kept neither half. It carries `attributed and substantially
   verbatim, disagreements presented as disagreements` and stops there:
   no recommendation clause, no named-risk clause, no one-bullet
   clause, and the word `compression` nowhere. Two copies declared
   edited together have drifted that far apart, and the dispatcher
   reads the emptier one — which is why consultation relays grew into
   walls while the agents' own card stated both the floor and the
   permission all along. The floor has therefore never bound the side
   that relays, which is the half of this defect the wave found last,
   and the reason W2 writes the floor rather than only its site. The
   design-personas spec
   (`./2026-07-28-working-process-design-personas-design.md`,
   `status: implemented`) is where both copies come from.

   What this wave changes beyond that re-alignment is the floor's site
   for consultations alone, and it says so rather than hiding the
   change inside a re-alignment. The floor's content is untouched:
   every recommendation and every named risk still survives, and two
   personas still never land in one bullet — in the file.

   The site is what `revises:` records. The design-personas document
   places the floor in the relay; after this wave a consultation's
   floor is met in the dispatch record, so that document's design no
   longer matches what ships, which is the lifecycle rule's own test
   for the pointer. The frontmatter therefore names it. What the
   pointer does not claim is that the floor lapsed: it holds, at a
   place the older document could not have named because no record
   existed then. `ruling: 2026-09-14`

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

   A licensed spec-origin fix follows the spec's own lifecycle rather
   than the plan's. Its disposition line lands under the spec's latest
   round heading, or as the resolution annotation the lifecycle rule
   already defines for a stamped document edited without a fresh round,
   and the plan's line points at it. One authorizer per line still
   holds — one authorizer, two documents, two lines — and the spec's
   stamp stops certifying words that are gone.

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

4. **Two items left this wave during brainstorming.** Both departures
   are recorded here so a later reader finds the reasoning rather than
   a gap. What never entered the wave at all is listed under *Out of
   scope* instead, which is where a reader looks for it.
   `ruling: 2026-09-14`

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

5. **A dispatch record is written to disk before it is relayed.** The
   relay may condense narrative only because the full text stays
   recoverable, and a copy living in the session dies at the next
   compaction — twice over in this repo's own history. So the
   dispatcher writes what the agent returned to a file, then names that
   file in the relay. The artefact is a **dispatch record**: one
   background dispatch, one file. It is not a Review report, which is
   the persistent, counted document a code-review run writes under
   `docs/code-review/`.

   The store is `.claude/working-process/`, under the `.claude/`
   namespace and git-ignored by a `.gitignore` containing exactly `*`
   written at its first use. It is git-ignored rather than in **Ignored
   mode**: the glossary defines that term for a Process directory, and
   the point of the paragraph below is that this store is not one.
   Private memory is described the same way — *always ignored*, with no
   mode named. The location is what settles its mode. A
   directory the process creates in a repo to hold work artifacts is a
   Process directory and owes the first-create question, and
   `.superpowers/` at the repo root is one. Private memory is the
   standing exception, and it is excepted by its own definition rather
   than by a rule about prefixes: the glossary says outright that
   `.claude/memory/` is *not a Process directory — a per-user store
   under the `.claude/` config namespace*, and the process-artifacts
   rule says the same. The dispatch record takes that shape: W4's
   glossary entry carries the same exclusion in the same words, so the
   store is outside the class by its own definition and the class needs
   no amendment.

   What the store guarantees is bounded, and decision 2 leans on the
   bound rather than on a promise. A dispatch record survives what the
   session does not: compaction, the end of the session, a branch
   switch. It does not survive `git clean -fdx`, which removes ignored
   files, nor does it reach a second Environment or a reviewer reading
   the document branch. That is the same durability Private memory has
   and the same the developer relies on daily.

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

       .claude/working-process/<stem>/<agent>-round-<N>.md
       .claude/working-process/<stem>/<agent>-<date>-<HH-MM-SS>.md

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
   rule, and the pointer to the dispatch record. It states that
   condensation reaches narrative alone, whatever a session's output
   style says.

2. **W2 — the consultation relay shape and its floor's site.** Two
   sites, edited together because they declare themselves so.

   `workflow.md`, the *Dispatching a consultation* paragraph: one
   paragraph per focusing question — or per briefing, where none was
   appended — then the path to the contribution. The paragraph states
   the floor as well as its site, because the rule states no floor
   today: it carries `attributed and substantially verbatim,
   disagreements presented as disagreements` and nothing more. So the
   dispatcher-facing copy gains the whole contract — compression yes,
   merging no, every recommendation and every named risk surviving, two
   personas never in one bullet — with the file named as where it is
   met. A rule that never states a floor is why this floor went
   unenforced on the side that relays.

   `PERSONA_COMMON.md`, the relay bullet of *The reply*: the same move
   of the floor's site, so the two copies agree. That file already
   carries the whole floor and the permission, and it declares that the
   dispatcher-facing copy lives in the workflow rule and the two are
   edited together. Editing one alone would recreate, in the other
   direction, the very drift this wave names as the defect it repairs.

3. **W3 — the origin field.** Four sites, edited together:
   `agents/plan-adversary.md` gains `origin` in the `Output` schema
   with its three values and one sentence placing it inside the card's
   existing spec boundary; `workflow.md` gains the triage sentence
   decision 3 defines, beside the existing license clause;
   `docs/domain/glossary.md` carries the **Origin** entry grilling
   already minted; and `spec-plan-lifecycle.md` gains the
   cross-document clause its ledger grammar lacks — where a fix lands
   in a document other than the reviewed one, that document's ledger
   takes the disposition line and the reviewed document's line points
   at it. The grammar owns where a line lands, so the clause belongs
   there rather than in the rule that invokes it, and `every terminal
   line carries exactly one authorizer` stands: one authorizer, two
   documents, two lines.

4. **W4 — the dispatch record.** Two sites. `workflow.md`, the
   verdict-agent dispatch bullet list and the consultation paragraph:
   both gain the write-then-relay duty and the path shape decision 5
   defines, stating where the path is that the store is git-ignored, so
   a reader never meets the path without that fact.
   `docs/domain/glossary.md` gains a **Dispatch record** entry, since
   the rules now name an artefact the glossary does not define and the
   nearest defined term, **Review report**, is a different object under
   `docs/code-review/`.
   That entry carries the store's exclusion in the words **Private
   memory** uses — not a Process directory, a store under the
   `.claude/` namespace — so the exclusion lives where the term is
   defined rather than in the rule that uses it.

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
  0 — the check that proves decision 2 landed. It also contains the
  floor's three clauses — every recommendation, every named risk, never
  in one bullet — expected 1 each, and 0 today.
- `PERSONA_COMMON.md` names the dispatch record as where a
  consultation's floor is met: expected 1, where today its relay bullet
  places the floor in the relay alone.
- `spec-plan-lifecycle.md` contains the cross-document clause: expected
  1, and `every terminal line carries exactly one authorizer` is
  unchanged: expected 1, an invariant.
- `workflow.md` contains a phrase naming one paragraph per focusing
  question: expected 1.
- `plan-adversary.md` contains `"origin"` inside the `Output` block:
  expected 1, with its three values on the same line.
- No `owner` names a document in `plan-adversary.md` or `workflow.md`:
  expected 0, the check that proves the collision stayed resolved.
- `plan-adversary.md` still contains its spec-boundary sentence:
  expected 1, an invariant this wave must not disturb.
- `workflow.md` contains the spec-origin triage sentence: expected 1.
- `workflow.md` contains the two filename shapes: expected 1 each. The
  path `.claude/working-process/` is expected 3 — once where the store
  is named and once inside each shape — so the check states three
  rather than one, and a count of one would mean a shape went missing.
  The sentence naming the store git-ignored: expected 1.
- `glossary.md` contains a `**Dispatch record**:` entry: expected 1.
- `workflow.md` contains no `.working-process/` outside the
  `.claude/` prefix: expected 0.
- `glossary.md` contains an `**Origin**:` entry: expected 1.
- `claude plugin validate` passes for the plugin and the marketplace:
  an invariant.

## Review rounds

### 2026-09-14 — architect, fable 5.1, blocking (round 1, full-document)

- hit fixed 2026-09-14 — the spec cited seven `Owner:` legs where the Unfinished-work list carries six; recounted against the list's entries and corrected to six
- fixed 2026-09-14 — [Important] the header's decisions count was derived from `held` lines that do not exist at relay time, since `open` is written at stamp time and triage follows the stamp; ruling: 2026-09-14; the count is now the findings for which the session can cite no license, computable from the report and the decisions already written, and the round's later `held` lines are its check
- fixed 2026-09-14 — [Important] `.working-process/` at the repo root is a Process directory by the glossary's definition, and the spec declared its mode without amending the class; ruling: 2026-09-14; the store moved to `.claude/working-process/`, inside the carve-out the glossary already grants and Private memory already occupies, so no class is amended and no project is asked
- fixed 2026-09-14 — [Important] decisions 2 and 5 disagreed about what the file is, one calling it guaranteed and the other ephemeral by construction; ruling: 2026-09-14; decision 5 now states the bound — it survives compaction, the session's end and a branch switch, and not `git clean -fdx`, a second Environment or the document branch — and decision 2 leans on that bound rather than on a promise
- fixed 2026-09-14 — [Important] the triage clause licensed editing a spec from a plan's fix wave and said nothing about where that edit is recorded or what it does to the spec's standing stamp; ruling: 2026-09-14; a spec-origin fix now follows the spec's own lifecycle — its line lands under the spec's latest round heading or as the resolution annotation, and the plan's line points at it
- fixed 2026-09-14 — [Minor] decision 2 argued the floor's move from the unboundedness of a contribution's count, where the real asymmetry is the unit's shape; license: `agents/plan-adversary.md`'s Output schema, which gives a finding a `claim` slot a relay carries in one line while a contribution has no delimited unit; the argument now runs from shape and survives a twenty-finding round
- fixed 2026-09-14 — [Minor] `revises:` was declined on the design-personas document although that document names the relay as the floor's site and this wave moves it; ruling: 2026-09-14, overturning the decline; the developer's stated ground for the decline — that the document is git-ignored and unlinkable — was refuted by checking the index, where all 28 files of `docs/specs/` are tracked; the pointer is added
- fixed 2026-09-14 — [Minor] "one paragraph answering each focusing question" has no value where a single persona is consulted and no focusing question was appended; license: the workflow rule's consultation paragraph, which appends one only when both personas are consulted; the shape now reads per focusing question, or per briefing where none was appended
- fixed 2026-09-14 — [Minor] the filename shape assumes a ledger ordinal for every verdict agent, which an `architect` dispatch on a bare question does not have; license: the glossary's **Consultation** entry, which records exactly that case; such a dispatch now takes the timestamp shape
- fixed 2026-09-14 — [Minor] the spec stated as settled that a rule's condensation clause outranks an output style's system-prompt instruction, where the relative precedence is unmeasured; ruling: 2026-09-14; decision 1 now marks it an assumption and names the observable that falsifies it — a relay under `Concise` that drops a finding line
- fixed 2026-09-14 — [Minor] "report" and "report store" collided with the glossary's **Review report**, a different object under `docs/code-review/`; license: that glossary term; the artefact is now a **dispatch record**, and W4 gains the glossary entry that mints it
- signal 2026-09-14 — another round earns its cost: the four Important findings each reshape a sentence in the decision they concern, and repair-born drift between decisions 2 and 5 is the likely failure of that wave, so a diff-scoped round two attacking those fixes is worth a top-tier read; the Minors need no round of their own

### 2026-09-14 — architect, fable 5.1, concerns (round 2, diff-scoped)

- fixed 2026-09-14 — [Important] the `revises:` ruling landed in the frontmatter and the ledger but decision 2's closing paragraph still ruled the pointer absent, leaving two `ruling:` statements in contradiction; license: the round-one ledger line carrying `ruling: 2026-09-14, overturning the decline`, which settles which of the two stands; the paragraph now states what the pointer records — the older document places the floor in the relay, this wave meets a consultation's floor in the dispatch record, so its design no longer matches what ships — and no longer argues the overturned position
- fixed 2026-09-14 — [Minor] decision 5 argued the store's exclusion from a prefix-based carve-out the glossary does not state; license: the glossary's **Private memory** entry and the process-artifacts rule, which except that store by its own definition rather than by its prefix; the argument now runs from that precedent and W4's **Dispatch record** entry carries the same exclusion in the same words
- fixed 2026-09-14 — [Minor] decision 2 said the shipped rule dropped the permission, where the permission ships in the persona-facing copy; license: `PERSONA_COMMON.md`, which carries *compression is allowed, merging is not* and declares that the dispatcher-facing copy lives in the workflow rule and the two are edited together; W2 is now stated as re-aligning two copies that drifted, which is the stronger claim and names a defect in the shipped plugin
- signal 2026-09-14 — a further round does not earn its cost on the present text: the Important was a held decision plus a paragraph rewrite and the Minors are one sentence each; where the fixes leave anything behind, the consumption gate's integrity audit is the right reader for it

The loop closed here on 2026-09-15, by the developer's decision and on
round 2's own stop signal, without a third round. What resolved the
concerns: every finding of both rounds reached a terminal disposition —
ten in round 1, three in round 2 — and the held set was empty at each
close. The four Important findings of round 1 were decided by the
developer and repaired; round 2 confirmed that the drift it had been
dispatched to hunt did not occur, and its own three findings were
licensed and fixed. Nothing was declined and no deviation from a
reviewer's suggestion was recorded, so the ledger above is the whole
account.

One thing this loop produced that belongs to the plugin rather than to
this spec: `PERSONA_COMMON.md` declares that the dispatcher-facing copy
of the consultation-relay obligations lives in `workflow.md` and that
the two are edited together, and they have drifted — the persona copy
kept `compression is allowed, merging is not` and the rule copy did
not. W2 repairs that drift, which makes it a defect fix rather than the
addition this spec first took it for.

### 2026-09-15 — integrity audit, fable, at the consumption gate

Coverage tell: 425 lines read, highest line cited 424 — a whole-document
read. Seven defects and twelve implementer questions; every defect's two
quotes were checked against the files they name before any disposition
was written, and all seven held.

- fixed 2026-09-15 — decision 1 and W1 still called the artefact a "report file" after the rename to dispatch record; license: the glossary's **Review report** entry, whose `_Avoid_` list carries `report file` verbatim; both now name the dispatch record
- fixed 2026-09-15 — decision 4's heading promised three items — two that left and one never in the wave — where its body describes two; license: the document itself, whose *Out of scope* section is where what never entered is listed; the heading now claims two and points at that section for the rest
- fixed 2026-09-15 — the verification check expected `.claude/working-process/` once in `workflow.md`, where the two prescribed filename shapes each carry the prefix; license: the check's own derivation, as a recounted expectation decides itself; the expectation is three, and the check now says a count of one would mean a shape went missing
- fixed 2026-09-15 — decision 5 and W4 called the store's state **Ignored mode**, a glossary term defined for a Process directory, in a paragraph arguing the store is not one; license: the glossary's **Ignored mode** and **Private memory** entries, the second describing the same shape as *always ignored* with no mode named; both now say git-ignored
- fixed 2026-09-15 — decision 2 claimed `workflow.md` "kept the floor and lost the permission" where the rule kept neither: it carries `attributed and substantially verbatim, disagreements presented as disagreements` and nothing else, with zero matches for all three floor clauses; ruling: 2026-09-15; the claim is corrected and W2 now writes the floor into the rule as well as the permission, on the ground that a dispatcher-facing rule stating no floor is why the floor went unenforced on the side that relays
- fixed 2026-09-15 — W2 edited `workflow.md` alone while `PERSONA_COMMON.md` places the consultation floor in the relay, so the wave would have recreated its own named defect in the other direction; ruling: 2026-09-15; `PERSONA_COMMON.md` joins W2 as a second site, edited together as both files declare
- fixed 2026-09-15 — decision 3 prescribed where a disposition line lands, which is `spec-plan-lifecycle.md`'s grammar, while W3 named three sites and not that rule; ruling: 2026-09-15; the rule joins W3 as a fourth site and carries the cross-document clause its grammar lacks, leaving `every terminal line carries exactly one authorizer` intact
