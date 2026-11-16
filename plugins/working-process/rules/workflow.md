# Working process — preferred flow

A spec-driven flow for non-trivial work. Every step below is an offer:
suggest it, let the developer decline. A tool that is not installed
disables its suggestion — never the work itself.

1. **Idea → spec.** When the superpowers:brainstorming skill is
   available, start non-trivial features there; capture the agreed design
   as a spec in `docs/specs/` (with `ticket.root` set, see the
   ticket-directory paragraph below). When the working-process consult
   agents (`architect-consult`, `system-designer-consult`) are available, ask
   once, early in the design conversation, whether the two personas
   should be consulted as the design forms — unless `consult.personas`,
   read as the process-settings rule says, is set, which answers it
   unasked. The answers are yes / not now / not in this session, and
   "yes, and record" or "no, and record", which write the key through
   the loader's `--set` where a settings block names the loader; "not
   now" and "not in this session" are honoured for the Claude Code
   session only and are never recorded. After a yes, dispatch a
   consultation when it looks worth its cost, without asking again for
   that conversation, and state the consent decision whenever it is
   made or changed — and when a compacted conversation leaves the state
   of a consent given in this session unclear, ask again rather than
   guess; a recorded key is simply read again. On a
   genuinely ambiguous ask — in-thread dialogue or a fresh-context
   consultation? — ask one short question rather than silently picking a
   surface. While drafting a design spec, before its first review, ask
   the developer for a size target, what is dropped, what native
   behaviour already covers, and which risks are accepted; write the
   answers into the spec's non-goals and constraints, never into a
   separate brief file, so every reviewer reads them.
2. **Spec → grilling.** Once a spec exists, offer a grilling-session
   (when the working-process plugin is installed) to stress-test its
   language against the project's domain terms.
3. **Grilled spec → architect review.** Offer a dispatch of the
   working-process `architect` agent (when available), on the most
   capable available model, named explicitly; dispatch, stamping and
   the propagation gate before each round follow the `review-loop`
   skill's procedure reference, when that skill is available. When the
   `propagation-auditor` agent is available, offer a propagation audit
   at authoring time as well, after any multi-site edit; that offer
   stands outside the loop.
4. **Spec → plan.** At the spec's consumption gate, before the plan is
   written, offer an integrity audit when the `integrity-auditor` agent
   is available: a fresh-context read of the whole design spec, and of
   its technical design where it names one, returning defects and the
   questions an implementer would have to ask. The offer fires unless a
   standing `integrity:` stamp still matches the recomputed body hash of
   every document the stamp names — a match means the standing stamp
   satisfies the gate, and the spec-plan-lifecycle rule owns that
   comparison. For a judged document whose LGTM came from a diff-scoped
   chain the offer takes the pair-offer form the `review-loop` skill's procedure reference
   defines, when that skill is available — one pair offer for an audit pair, never one per
   document — and narrows as that definition says when the auditor is
   absent.

   At the same gate, and before the integrity audit above, offer the
   technical design when the repository is one that has code. A
   declaration the project records binds and is never re-asked, in
   either direction. Its home is the settings key
   `design.technical-design-offer`, read as the process-settings rule
   says: `on` makes the offer at every consumption gate whether or not
   a manifest is present, `off` suppresses it. Until a project migrates
   to the key, a note in the project instructions Claude Code loads at
   session start — a `CLAUDE.md` at the repository root or in
   `.claude/` — or in the file such a note points at, declares it too;
   where the note and the key disagree, the key wins and the session
   says so. Without a declaration, a repository carrying a
   toolchain manifest — a file a language or platform toolchain reads
   to build, test or deploy it — gets the offer at every consumption
   gate and nothing is written; a repository carrying neither gets no
   offer. The core names no closed list of markers, and a domain's own
   skill may name the markers of its technology. A marker proves the
   repository holds code, never that this change needs decomposing, so
   the declaration is the signal and the marker only raises the
   question. The offer reads *open the `system-designer-session` skill,
   when available, and write the technical design?* — never *dispatch*,
   which names a background agent here. Where no skill covers the
   technology the document is still written, from generic knowledge and
   best effort: a tool that is not installed disables its suggestion,
   never the work. A design spec that already carries
   `technical-design:` has had its first pass: the pointer answers the
   offer, and the offer to write a design is not made again. The pointer
   confirms the link and nothing more — the design it names still takes
   every check it owes — and a pointer that resolves to no file is a
   broken link, reported as a finding, never a reason to offer a second
   design. A session may propose writing the declaration and never
   writes it unasked: the offer's answers include "yes, and record",
   which writes `on`, and "no, and record", which writes `off`, through
   the loader's `--set` where a settings block names the loader. A
   change may skip the document when it
   sits inside boundaries and contracts already settled and leaves the
   implementer no new responsibility split, placement, or ownership of
   state.

   Accepted, the session opens the `system-designer-session` skill when
   it is available and reads the technical-design rule, installed beside
   this one, before drafting — a path-scoped rule loads only when a
   matching file is read, and none exists yet — then writes the document
   to `docs/technical-designs/` following that rule. It writes both
   ends of the pair in the same turn — the design's `spec:` and the
   design spec's `technical-design:` — so no audit ever meets a
   half-written pair. The reviewer is the `architect` agent when that
   agent is available, whose card admits any judged document dispatched
   standalone, with the propagation audit gating that dispatch as it
   gates every verdict dispatch. The plan-adversary stays on plans.
   The plan written afterwards carries, beside its `spec:`, a
   `technical-design:` entry for every design spec it descends from that
   names a technical design — the same document, its path rewritten
   relative to the plan's own directory — so the plan-adversary always
   has each design to read.

   Where the technical-design offer is accepted, the audit waits until
   the design exists and its review dispositions are applied; the audit
   pair's sequencing at this gate is in the `review-loop` skill's
   procedure reference, when that skill is available.

   Before the plan's first line is written, whoever writes it — the
   session or a separate context — reads the plan-authoring rule,
   installed beside this one: a path-scoped rule loads only when a
   matching file is read, and a new plan has none yet. Then write the
   implementation plan with superpowers:writing-plans when available;
   plans live in `docs/plans/` (or the ticket directory, below). A
   brief that delegates plan-writing to a separate context names the
   spec-plan-lifecycle rule and the plan-authoring rule and requires
   reading both before the plan is written: the first carries the
   annotations a plan owes a registered design spec, the second the
   recurring defect classes and the check-writing rules, and a
   separate context cannot count on either loading.
5. **Plan → adversary review.** Before implementing a non-trivial plan,
   offer a working-process plan-adversary agent dispatch (when
   available); dispatch and stamping follow the `review-loop` skill's
   procedure reference, when that skill is available.
   Dispatch it on a model scaled to the plan's size, complexity, and
   risk — the most capable available for complex or risky plans, one
   family below for small mechanical ones — named explicitly.
6. **Implementation.** Test-driven when
   superpowers:test-driven-development is available; bugs go through
   superpowers:systematic-debugging when available. A question no
   document settles — an implementer's, or the session's own while it
   executes a plan — is answered by the session, and the answer is a
   provisional decision, which the `review-loop` skill's procedure reference
   defines under *The stand-in and the provisional batch*, when that skill is
   available. It is written when taken to
   `.claude/working-process/<stem>/provisional.md`, `<stem>` being the
   plan's basename or, where no plan exists, the design spec's: one
   line per decision — date, question, answer, author (`session` or
   `stand-in <name>`) — in a store kept out of git by a `.gitignore` containing
   exactly `*`, and no ledger line is written. The session that took them
   relays the list in its closing report; an answer there settles an
   item and is appended to its line, and the provisional batch at the
   `implemented` move carries what is still unanswered. An execution
   skill's own list, such as superpowers' "Rulings I made", is relayed
   as provisional decisions too.
7. **Implementation → code review.** When a `*-code-review` skill is
   installed for a domain the change touches, offer a review of the
   work's diff — once implementation is complete and before the plan's
   `status` moves to `implemented`, so a finding can still become work.
   Domains are judged as the plan-adversary judges them: from the change
   itself and the repo's own markers. Several domains touched mean one
   run per domain; orchestrating them into a single run is not this
   step. The step re-specifies no mechanics — the offer routes to
   whatever review surface the matched plugin ships, and that surface
   owns scope resolution, dispatch, and the report.

With `ticket.root` set, a new design spec, technical design or plan
whose `ticket:` yields a file prefix goes into the root's subdirectory
whose name starts with `<prefix>-`, ignoring case, in the working tree
or on the integration branch. Several matches go to the developer. Only
with none does it go into a new `<root>/<prefix>-<topic>/`, named by
the spec-plan-lifecycle rule's *Ticket directories*. Read that rule
before creating a ticket directory: it holds the lookup's commands, and
a path-scoped rule has not loaded before the first file is written.

Both audits offered above run in the background, so a gated dispatch
waits for its audit's task notification before it is issued — a
sequencing rule rather than a blocking call, running on the relay
machinery the `review-loop` skill's procedure reference defines, when that
skill is available.

Model selection for these dispatches: always name the model explicitly —
an omitted model inherits the session's model, defeating the heuristic
in both directions. Reviews are never dispatched on the cheapest
available family. Consultations — the `*-consult` agents — dispatch on
the most capable available model, named like any dispatch; a consultation
is not a review, returns no verdict, and never gets a fallback record or
a re-review offer. An audit is not a review either, and the
never-cheapest floor governs reviews alone: the `propagation-auditor`
dispatches on the tier `dispatch.propagation-auditor-tier` resolves
to — read as the process-settings rule says, `cheapest` unless the
project sets `mid` or `most-capable` — and the `integrity-auditor`
on the most capable available, each named explicitly; the key's value
is a tier, never a model name, and Claude Code resolves it through the
table below this paragraph. Both reports open
with a model self-report the dispatcher compares against the dispatched
and the prescribed rung before relying on the result, the transcript's
model deciding where the lifecycle rule says it does — a mismatched
propagation run earns no reliance, and a below-tier integrity run gets
no stamp. When a dispatch is refused because the dispatched
model's cap is hit — and only then; any other failure is an ordinary
error — ask the developer: drop one family (at most once, never onto
the cheapest family) or wait for the reset. A verdict produced below
the prescribed tier is recorded and offered a re-review per the
spec-plan-lifecycle rule, when installed.

| `dispatch.propagation-auditor-tier` | Claude Code rung |
|---|---|
| `cheapest` | the cheapest available family |
| `mid` | the family one below the most capable |
| `most-capable` | the most capable available |

Dispatching a consultation, when the consult agents are available: one
dispatch, briefed once. The briefing names the subject and where it
lives (the repo root at minimum), the constraints that bind it, and
settled decisions separated from open questions — pointing at files
rather than pasting them. It puts the question without the session's
own recommendation, since a persona handed an answer tends to return
it. A follow-up is a fresh cross-check dispatch,
never a resumption. When both personas are consulted on one subject,
give both the same canonical briefing, each with its own focusing
question appended, and tell neither what the other said. Dispatch as a
named background agent, so the transcript stays inspectable.

A contribution is written to its dispatch record before it is relayed,
named `.claude/working-process/<stem>/<agent>-<date>-<HH-MM-SS>.md` — `<stem>` the
subject, kebab-cased and capped at sixty characters, and a second record in the
same second taking the lowest free counter suffix, `-2` then `-3` — in a store at
the repo root kept out of git by a `.gitignore` containing exactly `*`: a consultation mints no round heading, so it has
no ordinal to derive, and several consultations of one persona on one
subject in one day are expected. The floor is met in that file —
attributed and substantially verbatim, compression allowed and merging
forbidden, every recommendation and every named risk surviving, and
text from two personas never landing in one bullet. The relay then
carries one paragraph per focusing question — or one per briefing,
where a single persona was consulted and none was appended — and the
path to the record. One thing stays in the relay whatever the floor
does: where the personas disagree, the disagreement is presented as a
disagreement with both positions, because a disagreement is the one
thing in a contribution the developer must decide and the digest
exists to raise decisions rather than bury them.

A request to verify one claim goes by the claim's kind: a mechanical
check to the `propagation-auditor`, an empirical one to a scripted
measurement, a judgment to a consultation. A verdict agent reviews a
document and is never dispatched to verify a single claim.

When `docs/domain/glossary.md` exists in the project, its canonical
terms and `_Avoid_` bans bind design specs, technical designs, plans,
code identifiers, and reviews.

When the `elements-of-style:writing-clearly-and-concisely` skill is
available, prose artifacts under `docs/` — design specs, technical
designs, plans, ADRs, the glossary — get its pass: invoke it before
drafting a new document, and
run an explicit editing pass over the changed prose of an existing one.
The pass binds wording, never decisions. Without the skill there is no
substitute pass and no install nagging — the work proceeds normally.

## Credentials

Never read a credential's value — `gh auth token`, a token or key file,
a keyring — or write one into a command. Report a check that needs
authentication the developer did not provide as not checked.

## Asks and their reach

An ask licenses only what it asks for. A question or a stated fact asks
for an answer: it licenses reading, with any tool, agents included, and
never a change of state — an edit, a commit, an agent that writes, a
push, a deploy, a write to a remote system, a release. A request
licenses the change it names, on the object it names, and no further
act with its own effect: "merge" asks for a merge, not a release. Where
the object is ambiguous — a named file that does not exist — ask which
is meant; a guess acted on is a change nobody requested. Any other
change needs a request for it, or a consent that covers it — given in
this session, as a Standing answer, or by project instruction, such as
the review loop's per-round commits; where one looks needed, propose it
and wait. Records these rules owe — ledger lines, dispatch records, the
implementation's provisional list — are no change an ask must name.

## Branch naming

Feature work happens on a topic branch named
`feature/<ticket>-<short-name>`, where `<ticket>` is the work's tracker
reference and `<short-name>` says what the work is, and
`feature/<short-name>` where there is no ticket. How a tracker's
reference is spelled in a branch name is the project's own — this
convention fixes the shape and not the spelling.

The branch of a worktree created with a generated name is renamed to
this shape before its first commit, so the branch a reader sees is the
branch the convention names; the worktree's own directory is a separate
name and this convention does not govern it. The work's design spec,
technical design and plan record the result in their `branch:` field —
the topic branch, not the
`<topic>.docs` branch a review loop's per-round commits use, which the
`review-loop` skill's procedure reference names, when that skill is available,
and which is a sibling of it rather than
a second topic branch. The ticket rule's sourcing order reads the
current branch name first when a new document needs a ticket.

With `ticket.root` set, the process reads a branch name as
`[<type>/]<key>[-<slug>]`: an optional one-segment `<type>` (`feature/`,
`bugfix/`, `hotfix/`), then a `<key>` — letters, a hyphen and digits
(`ABC-123`), or digits alone (`42`) — then an optional slug.
`feature/ABC-123-login`, `ABC-123` and `hotfix/42-crash` fit. Digits
alone count only at the key position, so `feature/oauth2-login` names
no key. The convention above still fixes the shape and not the
spelling: a project spells its keys as it likes, and the process reads
only the names that take this shape.

With `ticket.root` set, the integration branch is the one the project's
instructions name, else the session asks once. A declined confirmation
of a branch's ticket falls through to the conversation and then to
`none`, never to a second question. One answer about a branch's ticket
serves every rule that reads it for the rest of the session; nothing is
recorded, and a fresh session or a compaction may ask again.

## Dispatching a verdict agent

When the `review-loop` skill is available, invoke it — the first time
in a conversation, and again after a compaction — before dispatching a
verdict agent (`architect`, `plan-adversary`), at a consumption gate,
before a `status` move, and before writing a ledger line. Its procedure
reference holds the dispatch procedure, the review loop, the stand-in
and the provisional batch, the propagation gate, re-dispatch briefs,
the terminators and what a diff-scoped LGTM certifies; its ledger
reference holds the disposition ledger and its gate lines.

When the `process-status` skill is available, its Unfinished-work
reference holds the Unfinished-work list; the skill reads it when the
developer asks what the process left unfinished.
