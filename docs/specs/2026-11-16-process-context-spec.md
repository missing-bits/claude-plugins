---
ticket: none
date: 2026-11-16
status: approved
grilled: 2026-11-16
architect: concerns (resolved 2026-11-16)
integrity: 2026-11-16 (sha: a74a36c)
decisions: registered
branch: feature/process-context
base: develop
---

# Process context — load a rule where its reader needs it

The working process ships two large rules. One loads into every session
of every project; the other loads whenever anyone, a background agent
included, reads a process document. Most of both is read by nobody at
the moment it loads. This spec moves text to the place and the moment
its reader needs it and changes no decision the text carries. It is
package 7 of the release queue.

## Problem

Measured on `develop`, 2026-11-15, in characters, rounded:

| Rule | Loads | Size |
|---|---|---|
| `workflow.md` | every session, every agent | about 52,000 |
| `spec-plan-lifecycle.md` | any read of a design spec, technical design or plan | about 60,000 |

`workflow.md` spends about 33,000 of its characters on `## Dispatching
a verdict agent` and its six subsections. Only a session that is about
to dispatch a review needs them; a session writing code in an unrelated
project pays for them anyway.

`spec-plan-lifecycle.md` spends about 18,700 characters on the
disposition ledger and its gate lines, which matter only while a
round's findings are disposed, and about 5,600 on the Unfinished-work
list, which one skill reads by path. A background agent that reads a design spec receives the
whole rule, though it stamps nothing and disposes nothing.

A measurement on 2026-11-15 shows the cost in one number: a Haiku agent that
read twenty lines of a design spec had four rules injected, and the run
used about 97,000 tokens.

## Goals, non-goals, anti-goals

Goals:

- The always-loaded part of `workflow.md` is as small as the offers
  allow — estimated at about 15,000 characters, from about 52,000.
- A read of a process document no longer loads the disposition ledger,
  the Unfinished-work list or the per-round commit convention —
  estimated at about 32,000 characters, from about 60,000.
- Text that serves one activity loads when that activity starts.

Every figure in this spec is an estimate that sizes the change. None is
an acceptance threshold: no gate, audit or review re-derives one as a
count or fails the change on it.

Non-goals:

- Rules of other plugins. They are path-scoped already.
- A per-file size limit as a design constraint. The Claude Code
  documentation describes one for path-scoped rules (40,000 characters
  on a 200K context window); the agent measured above received a 59,541-character
  rule whole, so the limit is not observed here and sets no target.
- Any change to what the process decides, offers or records, beyond
  telling a moved text's reader where it now lives (D10).

Anti-goals — the change fails, even if it works, when:

- a moved sentence changes meaning, or a rule that bound a session
  before no longer reaches it at the moment it applies, beyond what the
  accepted risks below name;
- a pointer in a rule, card, skill, script or the glossary names a
  section that no longer exists where it points;
- the change adds a loader, a hook or a settings key.

Accepted risks, by the developer's decision (2026-11-16):

- A session may skip reading an on-demand text and act from memory.
  One sentence in the always-loaded rule names each read moment; no
  mechanism enforces it. A brief written from memory may likewise omit
  the ledger reference's path that D10 asks it to carry. Moments
  outside the four that also lean on moved text — naming a stand-in
  mid-session, reading a propagation report while authoring, a
  completion notification after a compaction — rest on the same
  pointer sentence.
- A verdict dispatch with no document, such as an architect asked a
  bare question, rests on that sentence alone.
- A session that loads the installed rules without the plugin, or with
  an older plugin that lacks the skill, cannot reach the moved text.
  Every pointer sentence is conditional — "when the `review-loop` skill
  is available" — as this repository's plugin-authoring convention
  requires of rule text naming a skill.

## Decisions

- **D1** — Every piece of rule text has one of three homes, chosen by
  who reads it and when: always loaded, loaded with a document class,
  or read when an activity starts. Argued in *Three homes*.
- **D2** — The always-loaded `workflow.md` keeps the seven steps and the
  cross-cutting text *The always-loaded rule* lists, and one sentence
  per on-demand text naming its read moment. A step cut to its offer
  loses no decision: a cut sentence moves to a named home or repeats
  text that stays. Step 6 is no offer and stays whole but for its
  pointers. Argued in *The always-loaded rule*.
- **D3** — The verdict-dispatch procedure, with the review loop, the
  stand-in, the propagation gate, re-dispatch briefs, the terminators
  and the diff-scoped LGTM, leaves `workflow.md` for a new skill,
  `review-loop`, which a session invokes before it dispatches a verdict
  agent, at a consumption gate, before a `status` move, and before it
  writes a ledger line. Its `SKILL.md` is short and routes each moment
  to the reference files it needs; the procedure is one reference. Its
  description names the four moments. Argued in
  *The dispatcher's procedure*.
- **D4** — The disposition ledger and its gate lines leave
  `spec-plan-lifecycle.md` for a reference file of that skill. Argued
  in *The dispatcher's procedure*.
- **D5** — The lifecycle rule splits by document class: a shared part
  for all three classes, and one part each for what only a design spec,
  only a technical design's audit pair, and only a plan needs. withdrawn
  the gain after D4 and D6 does not repay three more rule files,
  ruling: 2026-11-16
- **D6** — More text leaves the path-scoped rule for the one activity
  that uses it: the Unfinished-work list becomes a reference file of
  the `process-status` skill; the per-round commit convention and the
  relay-then-stamp sentence of *Lifecycle offers* join the
  `review-loop` skill. Argued in *What leaves the lifecycle rule*.
- **D7** — The consultation paragraphs in `workflow.md` shrink to the
  offer and a pointer; the contract in `PERSONA_COMMON.md` stays the
  single text. Argued in *The always-loaded rule*. withdrawn an
  installed rule cannot point at `PERSONA_COMMON.md` (D11), and about
  2,000 characters do not repay a pointer nobody can follow, ruling:
  2026-11-16
- **D8** — Text moves verbatim; nothing is redrafted, the steps of
  `workflow.md` included. A move is verified by diffing the moved text
  against its source, and every pointer by resolving it. Argued in
  *Verification*. withdrawn D2 shortens the steps, so text no longer
  moves verbatim everywhere, ruling: 2026-11-16
- **D9** — The home for text read when an activity starts is a skill,
  never a file among the installed rules. Argued in *Three homes*.
- **D10** — The brief of any agent dispatched on a document carrying a
  `## Review rounds` section — a reviewer or an auditor — gives it the
  path of the ledger reference and asks it to read it, since it no longer
  receives the ledger grammar with the document. Argued in *The
  dispatcher's procedure*.
- **D11** — A pointer in an installed rule to text that lives in a
  skill names the skill and its reference file, conditionally ("when
  the skill is available"), never by path: an installed rule cannot know the
  plugin's versioned directory. Only a session that invoked the skill
  knows the absolute path, and it passes that path on where a brief
  needs it (D10). Argued in *Three homes*.
- **D12** — Text that moves whole (D3, D4, D6) moves unchanged but for
  its pointers, and is diffed against its source. Argued in
  *Verification*.
- **D13** — Ticket directories, with the procedure for moving a
  document into one, stay in the lifecycle rule. Argued in *What leaves
  the lifecycle rule*.
- **D14** — The implementation rewrites the glossary's **Unfinished-work
  list** entry to name its new home. Argued in *What leaves the
  lifecycle rule*.
- **D15** — The plugin's identity surfaces name the new skill:
  `plugin.json`, the marketplace catalog entry and the repo README row.
  Argued in *Verification*.

## Three homes

| Home | Reader | Mechanism |
|---|---|---|
| Always loaded | every session | a rule without `paths:` |
| With a document class | whoever reads that document | a rule with `paths:` |
| When an activity starts | the session doing it | a skill, invoked on a pointer |

The test for a piece of text: *who needs this, and what are they doing
when they need it?* A background agent reading a design spec needs the
frontmatter contract and nothing about dispatching. A session about to
dispatch needs the whole procedure and has no reason to hold it before.

The second home uses `paths:`, which Claude Code loads on a read of a
matching file. The patterns are the lifecycle rule's own, the brace
pattern `docs/**/*-{spec,technical-design,plan}.md` included, so
documents in a ticket directory match.

The third home is a skill, by the developer's decision (2026-11-16).
Claude Code's own guidance for task-specific instructions that need not
sit in context is a skill, loaded when invoked. A skill ships and
updates with the plugin, so it cannot go stale the way an installed
rule copy does until the next `sync-rules`; and a file among the
installed rules would need a `paths:` matching nothing to stay
unloaded. The price is one skill description, always in context.

A pointer to the third home names the skill and the reference file —
"when the `review-loop` skill is available, its ledger reference" — and
never a path. Rules
install under the home directory while a skill lives in the plugin's
versioned cache directory, so a written path goes stale at the next
release. A session that invoked the skill has its base directory and
can pass the absolute path to an agent's brief.

## The always-loaded rule

`workflow.md` keeps:

- the seven numbered steps, each but step 6 cut to its offer: what is offered,
  when, and which tool makes it available;
- model selection and the tier table;
- Credentials, Asks and their reach, Branch naming;
- the glossary and elements-of-style paragraphs, the ticket-directory
  paragraph, and the verify-routing sentence;
- one pointer sentence per on-demand text.

A step cut to its offer loses no decision. Each cut sentence either
moves to a named home or repeats text that stays; it never leaves with
the decision it carries.

Step 4 is the largest step, at about 5,900 characters: it carries the
technical-design offer's declaration rules and the audit pair's
sequencing. The offer stays. The sequencing moves to the `review-loop`
skill, whose reader is the session at the consumption gate — one of
its read moments — and not every reader of a document.

Step 6 is no offer. It is the only home of the provisional list: its
path, its line shape and the duty to relay it. It stays whole; only its
pointers into moved text are rewritten. Its pointer to the record
store's `.gitignore` guard gives way to the guard itself, stated inline
— a `.gitignore` containing exactly `*` — so writing the provisional
list needs no read of the skill.

The two consultation paragraphs stay as they are. They are the
dispatcher-facing copy of the contract in `PERSONA_COMMON.md`, and the
two are edited together. An installed rule cannot name that file's
path, and the paragraphs cost about 2,000 characters. One pointer in
them changes: the record name they borrow from the dispatch
subsection is stated inline — `<agent>-<date>-<HH-MM-SS>.md`, under a
`.gitignore` containing exactly `*` — since dispatching a consultation
is none of the read moments.

## The dispatcher's procedure

`## Dispatching a verdict agent` and everything under it, with the
disposition ledger and its gate lines, form one text with one reader:
the session running a review loop. They become the `review-loop` skill.
Its `SKILL.md` is short: for each read moment it names the reference
file to read. Two reference files sit beside it — the dispatch
procedure and the ledger grammar. A single body would run to about
9,000 tokens, while Claude Code advises keeping `SKILL.md` under 500
lines and, after a compaction, re-attaches only the first 5,000 tokens
of each invoked skill; the terminators would drop silently. A short
body survives a compaction whole and tells the session to invoke the
skill again, which re-reads the references it routes to; a ledger-line
write reads the grammar without the procedure. The skill's description names the four read moments,
since where the rules were never synced it is the only trigger. The session invokes it at four moments, the first in a
conversation and again after a compaction: before it dispatches a
verdict agent, at a consumption gate, before a `status` move, and before
it writes a ledger line. The last three can come with no round in
sight — the pair offer lives in the procedure and its
`, debt discharged` annotation in the ledger grammar, so a consumption
gate reads both references; a `status` move delivers the provisional batch, and an
answer to a held batch, given in a later session, is written as a
`ruling:` line before anything is dispatched. The skill carries
instructions and nothing else — it dispatches no agent and runs no
round.

The four read moments are listed in three places: the always-loaded
pointer sentence, the skill's description and its `SKILL.md`. The three
are edited together.

The two rules today promise to keep the relay-then-stamp ordering in
step: the dispatch subsection of `workflow.md` and one sentence of
*Lifecycle offers*, with the plan's diff-scoped LGTM exception. That
sentence is the dispatcher's procedure too, so it joins the skill
(D6), and with both halves in one home the promise to edit them together ends.

Background agents stop receiving this text. Reviewers and auditors read
the documents they judge; none dispatches. One reader still needs the
ledger grammar: a reviewer or auditor whose document carries a `## Review rounds`
section — a diff-scoped round, a plan's confirming round, a pair
offer's round arm, a new loop after a close — reads the ledger and must
tell a settled `ruling:` line from a `provisional:` or `license:` one.
Its brief gives the path of the skill's ledger reference and asks the
reviewer to read it.

## What leaves the lifecycle rule

The lifecycle rule stays one rule for all three document classes. Besides
the ledger (D4), three pieces of text have one reader each and leave it:

- the Unfinished-work list, which the `process-status` skill reads by
  path today, becomes that skill's reference file;
- per-round commits on a document branch belong to the loop and join
  the `review-loop` skill;
- the relay-then-stamp sentence of *Lifecycle offers*, with its
  exception for a plan's diff-scoped LGTM, joins the same skill (see
  *The dispatcher's procedure*).

The glossary's **Unfinished-work list** defines the list as a section
of the lifecycle rule. The implementation rewrites that definition when
the list moves; the glossary describes what shipped, so the grilling
leaves it alone.

Ticket directories, with the procedure for moving a document into one,
stay in the lifecycle rule. `workflow.md` already tells a session to read
that text before it creates a ticket directory, since no file exists
yet to load it, and that pointer keeps working.

## Verification

- Text that moves unchanged (D3, D4, D6) is compared with its source
  after whitespace normalisation, and any difference other than a
  pointer rewrite is reported. A shortened step (D2) is checked by
  review against the first anti-goal.
- Every pointer into moved text is rewritten to the text's new home
  (D11), or deleted with its sentence where D2 shortens a step. A
  pointer names the text in many ways: by heading, by a phrase such as
  "the verdict-agent dispatch subsection below" or "the provisional
  batch the workflow rule defines", or by naming the rule that holds
  it — `workflow.md`'s *Branch naming* does so for per-round commits,
  and the `read-by:` lines of `SETTINGS_REGISTRY.md` do so for
  `review.autonomy`, `review.per-round-commit` and
  `docs-branch.merge`, which then name the `review-loop` skill's
  procedure reference — the file that cites the keys, as the registry
  test requires — in the registry's own repo-path form — the registry is no installed rule, so D11 does not
  bind it. Each rewritten pointer is then resolved against its new
  home. The
  plan enumerates every such pointer, in rules, skills, cards, the
  README, the registry and the glossary; no single search is complete,
  so the plan reads the kept text of both rules whole and searches the
  other files for each moved heading and its phrases.
- The shipped files are measured with `wc -m`, and the sizes are
  reported beside the estimates in *Goals*. A miss is reported, never a
  failure.
- One context measurement per document class: an agent reads a document of that class
  and reports which rule files were injected.
- `sync-rules` needs no change: no rule file is added or removed, and
  the two rules it installs only shrink.
- The plugin's identity surfaces name the new skill: `plugin.json`,
  the marketplace catalog entry and the repo README row.

## Out of scope

- Rewording for brevity outside steps 1–7 of `workflow.md`, beyond
  what a move forces.
- Splitting the lifecycle rule by document class (D5, withdrawn).
- The installed rule copies in a developer's home directory; they
  follow at the next `sync-rules`.

## Calls made by the author

- **Ticket directories stay path-scoped.** They have one reader, like
  the sections D6 moves, but no skill of their own and an always-loaded
  pointer that already works. Keeping them costs about 4,700 characters
  on every document read.
- **The skill is named `review-loop`.** It names the activity its
  reader is in, as the other skills of this plugin do.

## Review rounds

### 2026-11-16 — architect, fable 5.2, blocking (round 1, full-document)

The verdict follows the card installed at dispatch, 0.19.0-dev.4
(two Important = `blocking`);
the card on `develop` requires a Critical, which would make it
`concerns`. Record:
`.claude/working-process/2026-11-16-process-context-spec/architect-round-1.md`.
The developer ruled on 2026-11-16 to read it under the current card:
the field carries `concerns`.

- hit fixed 2026-11-16 — *Branch naming* in `workflow.md` names the lifecycle rule as the home of per-round commits, which D6 moves; *Verification* now names it
- hit fixed 2026-11-16 — the registry's `read-by:` lines for `docs-branch.merge` and `review.per-round-commit` go stale under D6; *Verification* now names them
- hit fixed 2026-11-16 — *Verification*'s two searches missed `per-round`, `docs-branch`, `relay-then-stamp`, `stand-in`, `diff-scoped` and excluded `workflow.md`; replaced
- hit dismissed 2026-11-16 — "read moment", "always-loaded", "path-scoped", "identity surface", "provisional batch", "ledger reference" have no glossary entry; counter: the grilling ruled no new terms, they are this spec's plain prose, and the provisional batch is defined in `workflow.md`
- hit fixed 2026-11-16 — the search missed pointers worded "verdict-agent dispatch subsection", "propagation gate below", "provisional batch"; the bullet drops its completeness claim and the plan reads the kept text whole
- hit fixed 2026-11-16 — the `read-by:` lines were only checked to resolve; the bullet now rewrites them to the skill
- hit dismissed 2026-11-16 — individual stays-text pointers are not listed in the spec; counter: the spec assigns their enumeration to the plan, and the bullet names every class they fall in
- hit fixed 2026-11-16 — rewritten `read-by:` lines conflicted with D11; D11 scoped to installed rules, the registry keeps its repo-path form (not re-audited: the episode's re-dispatch bound was reached)
- hit fixed 2026-11-16 — D2 said "the seven offers" and *The always-loaded rule* cut every step to its offer, while step 6 is no offer; both now except step 6
- hit fixed 2026-11-16 — the round 1 note named "the installed card" for a two-Important rule the card now installed lacks; the note names the card installed at dispatch, 0.19.0-dev.4
- hit dismissed 2026-11-16 — the round 1 record's `size: 283` re-derives as 284 on commit 751dc40; counter: the record measured the text as dispatched, before the stamp added the blank line ahead of `## Review rounds`
- hit dismissed 2026-11-16 — glossary gaps for the spec's prose terms, re-raised; counter: the dismissal above stands — the grilling ruled no new terms, and the hit brings no new evidence
- fixed 2026-11-16 — [Important] D2 cuts all seven steps to their offer but names a home for cut text only in step 4; step 6 is no offer; ruling: 2026-11-16; D2 and *The always-loaded rule* now say a cut sentence moves to a named home or repeats kept text, and step 6 stays whole with its pointers rewritten
- fixed 2026-11-16 — [Important] a session with the installed rules but without the plugin, or with an older one, finds pointers to a skill that does not exist; ruling: 2026-11-16; every pointer sentence is conditional (D11, *Three homes*), and a third accepted risk names this reader
- fixed 2026-11-16 — [Important] a single skill body of about 9,000 tokens loses its terminators when compaction keeps the first 5,000; ruling: 2026-11-16; D3 and *The dispatcher's procedure* now give a short `SKILL.md` routing each read moment to one of two reference files, the procedure and the ledger grammar
- fixed 2026-11-16 — [Minor] step 4's audit-pair sequencing was moving to the path-scoped lifecycle rule, whose reader is every document read; ruling: 2026-11-16; it moves to `review-loop`, read at the consumption gate
- fixed 2026-11-16 — [Minor] D10 handed the ledger reference to diff-scoped rounds only; ruling: 2026-11-16; D10 now covers any round on a document carrying `## Review rounds`
- fixed 2026-11-16 — [Minor] the spec did not say the skill's description carries the read moments, the only trigger where rules were never synced; ruling: 2026-11-16; D3 and *The dispatcher's procedure* say it names the four moments, the name stays

### 2026-11-16 — architect, fable 5.2, concerns (round 2, diff-scoped)

Record: `.claude/working-process/2026-11-16-process-context-spec/architect-round-2.md`.

- fixed 2026-11-16 — [Minor] the registry bullet named `SKILL.md` as the reader of three keys, but the short router will not cite them; license: `tests/working-process/test_settings_registry.py:116-120` requires every `read-by:` file to cite its key, and `SETTINGS_REGISTRY.md:13` defines `read-by:` as the files that read it; the bullet now names the skill's procedure reference
- fixed 2026-11-16 — [Minor] step 6 stays whole with its pointers rewritten, yet taking a provisional decision is none of the four read moments; ruling: 2026-11-16; *The always-loaded rule* now has step 6 state the record store's guard inline, a `.gitignore` containing exactly `*`
- declined 2026-11-16 — [Minor] the reviewer's card could read the ledger reference through `${CLAUDE_PLUGIN_ROOT}` instead of the dispatcher carrying its path; ruling: 2026-11-16; D10 stands, and the first accepted risk now names a brief that omits the path
- fixed 2026-11-16 — the four read moments live in three places with no statement that they move together; ruling: 2026-11-16; *The dispatcher's procedure* now says the three are edited together
- signal 2026-11-16 — a third round does not earn its cost: the round is all-Minor, the leftovers are one correction and two short answers, and the integrity audit at the consumption gate reads the whole document
- hit fixed 2026-11-16 — the spec used the bare word "probe" three times, which the glossary bans (`_Avoid_: … probe (unqualified)`); now "measurement"
- hit fixed 2026-11-16 — bare "pair" for the relay-then-stamp sentences, with a pair offer in view in the same section (`_Avoid_: pair (bare, where a pair offer is also in view)`); now "the promise to edit them together"

Round 2's `concerns` is resolved without a fresh round: the developer
answered both held findings on 2026-11-16 and chose the integrity audit
at the consumption gate over a third round, as the reviewer's stop
signal advised.
