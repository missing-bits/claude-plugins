---
ticket: none
date: 2026-08-24
status: implemented
grilled: 2026-08-24
architect: LGTM
branch: feature/process-status-riders
base: develop
---

# Process status, the review offer, and anchored-sweep hardening

Throughout this document *anchor* means a regex anchor — `^` or `$` —
and nothing else. The lifecycle rule's named section of grep commands is
the Unfinished-work list — not every published command belongs to it; a
command's output is a hit until the reader confirms it.

## Problem

Three increments ride the working-process 0.14.0 release. Two of them
edit the same list, so one spec decides all three; specing them apart
would fork it.

**Nobody runs the list.** The lifecycle rule publishes grep commands for
unfinished process work — a pending grilling, a bare `concerns` or
`blocking` verdict, a live fallback record. They answer exactly one
question ("what did the process leave unfinished?"), and today the
developer answers it only by remembering the commands.

**The flow ends at Implementation.** Both standards plugins ship a
`*-code-review` skill and a review command, yet no step offers the
review. The process reviews plans and specs on its own initiative and
reviews code only when asked.

**The store's readers assume a top-level field.** In a Hybrid store
Auto-memory relocates this plugin's lifecycle fields into its own
`metadata:` block — observed live on 2026-08-17, and by now routine:
measured on 2026-08-25, 10 of the 20 `idea-*` entries in this repo's
Private memory carry `status` there rather than at the top level, an
even split. The count is the one measurement this document quotes; the
co-writer keeps writing, so later readings will differ and every
argument below rests on the split being substantial, never on the
figure. One consequence is live rather than prospective. The grooming walk's audit
looks for `idea-*` entries whose `status` reads `spec'd` or `dropped`
while their body still lives; a relocated `status` reads to that check
as no `status` at all, so a closed idea slips through it. The published
ticket sweep, by contrast, meets no damage today — it covers `docs/`
and `.superpowers/`, the writer touches `.claude/memory/`, and Team
memory is never a Hybrid store — so there the tolerant form buys
resistance for the next anchored grep rather than a repair.

## Design

### The Unfinished-work list is the definition site

The lifecycle rule owns which classes of unfinished work exist; the
skill runs what the rule publishes. One definition site, so a new class
costs one edit in the rule and none in the consumers that run it. The
pending autonomous-review-loop spec already plans to publish two more
classes (`open` and `held` lines); under this contract it publishes them
and `process-status` reports them with no edit of its own.

The contract names its own scope: the lifecycle rule's Unfinished-work
list, not every `rg` command the payload contains. The
ticket-frontmatter rule publishes a sweep of its own, and that sweep
answers "which documents belong to this ticket" — a lookup, never
unfinished work.

The list changes shape to carry the contract:

- the list becomes a named section of the rule, so its boundary is
  structural rather than the reader's judgment. The name binds both
  sides and moves only when both move — the pattern the Contract
  probe's paths already set;
- each entry becomes a triple — the class name, its one-line command,
  and the owner of the next move — instead of a command buried in a
  paragraph;
- every command gains `--no-ignore`, so an ignored-mode Process
  directory stays visible; the ticket sweep already carries the flag;
- every command gains `--crlf`. An exact tail `$` misses a line ending
  `\r\n`, so a bare verdict saved on Windows reads as closed — a silent
  clean state the confirmation cannot rescue, because a hit that never
  fires never reaches it. The flag changes nothing on LF files, and
  this repo has none of the other kind;
- a fourth entry joins them, **Misplaced stamp**: a process field
  (`grilled`, `architect`, `adversary`, `*-fallback`) outside the top
  level of the frontmatter, at any value. Its owner leg names the
  developer, because no process surface owns moving a stamp back — the
  same fact the Out-of-scope section states from the other side. An
  owner is a mandatory leg, so the honest value goes on the entry
  rather than being left for the skill to infer;
- one sentence states what a command returns: hits, not Findings.

The owner rides the entry because the two promises otherwise collide:
the report names the owner of the next move, and a new class costs one
edit in the rule and none in the skill. Deriving the owner from the
rule's offers paragraph would be exactly the executor judgment this
design removes, and it already fails for Misplaced stamp, which no
offer covers. The entry *names* the owner and nothing more — the skill
still fires no offer, so the owner on the entry never becomes a second
trigger.

The skill reads the list from the payload copy shipped beside it,
`${CLAUDE_PLUGIN_ROOT}/rules/spec-plan-lifecycle.md`, never from an
installed copy. The plugin releases skill and payload in one version, so
that copy is always in step with the skill, while an installed copy can
only lag. This inverts the Contract probe deliberately: there the
installed copy governs the shape of a report written in the reviewed
project, whereas here the list governs what the skill itself runs.

### A command finds hits; the skill confirms them

A command's semantic target is the frontmatter block, which a regex
cannot express — and the gap is not theoretical. Run the list's three
current commands over this repo — Misplaced stamp arrives with this
spec — and exactly one document matches:
`docs/plans/2026-07-13-rules-distribution.md:267`, where the plan quotes
the lifecycle rule's own example frontmatter inside a fenced block. The
plan's real frontmatter carries `status: implemented` and no `grilled:`
field. One hit, and it documents the convention rather than instantiating
it.

So the skill confirms every hit before reporting it: the matching line
must sit inside the document's frontmatter block, between the opening
`---` and its closing pair. A document with no frontmatter block
therefore yields nothing, however its body reads. The confirmation
carries the precision a command cannot, which is what lets every command
take the tolerant `^\s*` form without paying for it.

### The uniform shape of an anchored sweep

Every anchored grep over a frontmatter field is written
`^\s*<field>:`. Where a sweep anchors its tail, the `$` stays exact:
the lifecycle commands rely on it, because an annotation such as
`(resolved 2026-07-16)`, `(adjudicated 2026-08-17)` or `, waived
2026-08-01` defeats the match, and that defeat **is** the recorded
closed state. Softening a tail would reopen every closed document onto
the list.

One rule replaces a per-surface judgment. The store has a second writer
that nests fields; specs and plans have none, so uniformity buys
resistance there rather than repair — and it costs nothing, because the
frontmatter confirmation already rejects the quoted examples that a
tolerant leading anchor would otherwise catch.

### Placement in the store: one writer's preference, every reader's tolerance

Auto-memory rewrites the frontmatter of any entry it touches, so
relocation is not an accident to repair but the standing behaviour of a
co-writer that writes more often than the rules do. Repair is a loop
nobody wins, and ADR 0003 already set the posture for harness-caused
deviation: tolerate it, and count it as format debt rather than a
defect.

The conventions rule therefore stops asserting an invariant the
environment violates across half the measured entries, and states the
rules that stay true:

- the rules write a field the entry lacks at the top level, where the
  index projection and a human reader look first;
- every reader accepts the field anywhere inside the frontmatter block,
  and where two copies exist the top-level one wins. The read names no
  block of the harness: ADR 0002 declines to bind that shape, and the
  tolerant form already covers any nesting depth;
- no rewrite exists solely to move a field, and an unsolicited report
  of one is a nag. A grooming walk the developer asked for is not
  unsolicited, so its standing report of the co-writer's keys stands.

Writing a duplicate deliberately stays out. `status` is the one field of
the set that changes, and two copies of a changing value with nobody to
reconcile them is a dual-write: an idea's graduation would update one
copy and leave the other reading `parked`. Today each entry holds
exactly one copy, because the co-writer relocates rather than copies,
and the read rule is what makes that harmless.

A write to a field the entry already carries updates it where it sits.
Only a field the entry lacks is created, and it is created at the top
level. Where two copies exist, a write takes the top-level one, which
mirrors the read's precedence rather than inventing a second rule. So no
write produces a second copy and no write moves one, which is what makes
the three rules above readable together: the tolerant read carries the
difference, and the co-writer's block is never restructured and never
the target of a field's creation. Updating a value where it already sits
is not a violation of that — it is the case the rule exists for.
Top-level placement is therefore where fields are created, not a
property of existing entries — the honest statement, since half of them
say otherwise.

One consequence lands in the grooming walk: its audit reads `status`
wherever it sits inside the frontmatter, so a closed idea with a
relocated field stops slipping through the lifecycle check.

### process-status — the report

The skill reads the list, runs each command over the project, confirms
each hit, and reports.

The report groups by document, because the developer acts on a document
and not on a class of hit. Each line names the class and the owner the
entry carries — the re-review offer rides the consumption gate before
plan-writing, a pending grilling belongs to the grilling-session, and so
on. The skill reads that owner rather than knowing it.

Misplaced stamp takes precedence per field, not per document: a
misplaced `grilled:` suppresses only the class that reads `grilled`,
while a correctly placed `architect: concerns` in the same document
still reports as unfinished work. Suppression follows the untrustworthy
field and stops there. A document carrying both appears once, with a
line for each — grouping by document already guarantees that.

A clean repo produces a statement, never silence: the report names what
it checked and found nothing. A silent clean run and a broken run read
alike, and the run that reports nothing is exactly the one the developer
cannot verify. Two consequences follow from the same argument. An empty
or unparseable list is an error the report states outright — a run that
found no list must never read like a run that found no unfinished work.
With the list a named section, "unparseable" is bounded: the section is
missing, or an entry lacks a leg of its triple. And the report shows its rejected hits, counted and
named, because over-rejection is the one way the confirmation — this
design's central mechanism — can quietly eat real unfinished work.

The report closes with one question — whether to take anything from the
list. The skill fires no offer the lifecycle rule defines; those offers
have an owner and a gate, and a second trigger for one of them would
duplicate the owner.

Three things stay out of the report: the Project memory store, documents
merely in flight (`draft` or `approved` with no further move), and any
criterion the skill invents. A future class reaches the report by being
published on the list, never by being taught to the skill.

### Step 7 — implementation to code review

The flow gains a step: when a `*-code-review` skill is installed for a
domain the change touches, offer a review of the work's diff. The offer
fires once implementation is complete and before the plan's `status`
moves to `implemented`. Findings can mean more work, so the review
precedes the flip that declares the work finished; the memory-review
offer stays at the flip, where it belongs.

Skill discovery mirrors the `*-plan-review` convention the
plan-adversary already uses: match installed skills by name, for the
domains the change touches. No match, no offer — the rule's standing
ethos already says that a tool which is absent disables its own
suggestion.

The step re-specifies no mechanics, and it makes no assumption about
which surface carries them: the offer routes to whatever review surface
the matched plugin ships. Today both standards plugins pair the skill
with a command, and the step keys on the skill because that is the name
the discovery convention matches; a future plugin shipping the skill
alone still gets the offer, and its own surface decides how the run
happens.

The domain plugin owns those mechanics: its
review command resolves the scope, runs the pre-dispatch first-create
check, dispatches in the background, and writes one Review report under
the review-reports contract. Where a change touches several domains,
each domain gets its own run; the step says so, so nobody invents a
mixed run here. Orchestrating domains into one run is the parked review
orchestrator, not this step.

The offer does not join the lifecycle rule's offer list. That list is
keyed to a document's state and fields; a code review is keyed to code.
The workflow rule loads in every session, so step 7 fires on its own,
and a second statement would buy the list's completeness at the price of
a second source of truth.

## Changes by file

- `plugins/working-process/skills/process-status/SKILL.md` — new skill:
  the contract, the confirmation step, the report shape.
- `plugins/working-process/rules/spec-plan-lifecycle.md` — the
  Unfinished-work list as a named section whose entries are triples,
  `^\s*`, `--no-ignore` and `--crlf` on each command, the Misplaced
  stamp entry and its per-field precedence, the hits-not-Findings
  sentence.
- `plugins/working-process/rules/workflow.md` — step 7.
- `plugins/working-process/rules/ticket-frontmatter.md` — `^\s*ticket:`
  in "Finding documents by ticket".
- `plugins/project-memory/rules/project-memory-conventions.md` — the
  top-level requirement becomes a write place plus a tolerant read with
  top-level precedence, and the sweep-fragility justification goes with
  it; a prospective clause requires `^\s*<field>:` and `--crlf` of any
  future anchored grep over store fields.
- `plugins/project-memory/skills/memory-review-session/SKILL.md` — the
  opening audit reads `status` wherever it sits inside the frontmatter.
- `plugins/working-process/.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `README.md`,
  `plugins/working-process/README.md` — the new skill in all three
  identity surfaces and in the plugin's component list.
- `docs/domain/glossary.md` — **Unfinished-work list** and **Misplaced
  stamp**, minted during this spec's grilling session and already
  applied.

Versions: working-process keeps `0.14.0`, the unreleased minor it
already carries, and dogfoods this branch as
`0.14.0-dev.process-status-riders`; the release PR strips the suffix.
project-memory takes a minor in the same release PR: the audit clause
adds behaviour, so a patch would misreport the change. It needs no
dogfood version of its own — the clause is exercised against this
repo's own store, which carries relocated entries in quantity.

## Out of scope

- **Orchestrating reviews across domains** — the parked review
  orchestrator; step 7 offers one run per domain and no more.
- **The `open` and `held` classes** — they belong to the
  autonomous-review-loop spec and reach the report through the same
  published list, with no edit to this skill.
- **Repairing a Misplaced stamp in `docs/`** — detection is what this
  spec buys, and the repair has no owner yet: the parked second-writer
  detector was scoped to the store, where this spec declines repair
  outright, so that entry closes or narrows with this work rather than
  standing as the docs-side owner.
- **Softening any tail anchor** — stated as a decision, not an
  omission.
- **Frontmatter hygiene beyond process fields** — a nested `ticket`,
  `date`, `status`, `branch` or `base` suppresses no class, so the list
  stays silent about it. `status` is named deliberately: its
  misplacement would mislead the lifecycle more than the others, and it
  is still not unfinished work, because no command on the list reads it.

## Verification

Dogfooding in this repo.

- All four commands run clean after the confirmation step, and the
  report says so by naming what it checked. The single hit —
  `docs/plans/2026-07-13-rules-distribution.md:267` — is rejected as
  documentation, which exercises the confirmation on the first run
  rather than on a constructed case.
- A temporary document with a bare `concerns` verdict, one with a
  misplaced `grilled:` beside a correctly placed `architect: concerns`,
  and one quoting either form in its body together prove the three
  outcomes: reported as unfinished work, reported as a Misplaced stamp
  with the neighbouring verdict still reported, and rejected.
- Step 7 is exercised by this work itself: the change touches plugin
  content only, so no `*-code-review` skill matches a touched domain and
  the step correctly offers nothing. A run over a Python or Salesforce
  project demonstrates the offer firing.
- The audit clause runs against this repo's Private memory, where the
  relocated entries are counted in the Problem section: every entry's
  lifecycle state is read, and no entry is rewritten to move the field
  back.
- The recorded scope of the parked hardening idea said "exactly one
  regex". This spec widens it to four commands plus a new class, and the
  memory entry closes with a pointer here rather than drifting.

## Consultations

Consultations return no verdict and stamp nothing; they are recorded
here for the trail, separately from the rounds below.

### 2026-08-25 — system designer, fable 5

Read the design as parts and contracts and raised ten gaps: the
class-to-owner mapping sitting in the skill rather than on the entry,
the list's boundary having no structural marker, undefined behaviour on
an empty list, four confirmation edge cases (a hit that no longer
reproduces, an unclosed frontmatter block, a duplicate stamp in `docs/`,
CRLF line endings), two holes in the store's write semantics, and a
report that shows no rejections.

### 2026-08-25 — architect, fable 5

Judged the same ten for fit, briefed unattributed so neither
consultation carried the other's authority. Seven landed in this
document: the entry triple, the named section, the empty-list error,
`--crlf`, the "never touched" rewording, the top-level copy on a write,
and the rejected-hit line. Two went to the plan as implementation
detail: the unclosed-block parse rule (this document's existing
decisions already forbid a fifth class, so no new sentence is needed)
and naming the field on a Misplaced stamp line. Three were declined —
a drift warning in the report (the drift hook owns that signal, and the
skill re-reading the installed copy's state would undercut the settled
inversion), a clause for a hit that no longer reproduces (the
confirmation reads the file at confirmation time, and the only
co-writer writes to a store this report excludes), and suspending
Misplaced stamp's suppression when a top-level copy exists (suppression
follows the untrustworthy field; the document still appears under its
Misplaced stamp line, and the proposal would import the store's
top-level-wins read into `docs/`, where no tolerant read is
established).

## Review rounds

### 2026-08-24 — architect, fable 5, LGTM (round 1)

Three Minor findings, all wording-level, all fixed in this document:

- the measured claim counted four commands where the rule publishes
  three today — the fourth arrives with this spec;
- the Problem section's "goes blind" overstated the live breakage: the
  published ticket sweep covers `docs/` and `.superpowers/`, the second
  writer touches `.claude/memory/`, and Team memory is never a Hybrid
  store, so no published command and the observed nesting intersect
  today;
- "surface" carried a third, unqualified sense against the glossary's
  reservation of the short form — now "consumer" and "owner".

#### Amendment after the round — 2026-08-25

The developer reopened the store half of the hardening, and the
amendment postdates the verdict above, which therefore does not cover
it. A fresh round is dispatched.

The design previously kept top-level placement as an invariant and
implied that the grooming walk restores a relocated field. Two facts
killed that: the walk does no such thing today — its audit reports
foreign keys and moves on — and Auto-memory rewrites the frontmatter of
any entry it touches, so a repair is undone at the co-writer's next
write. Measurement settled the direction: half the `idea-*` entries
already carry a relocated `status`, and the audit's lifecycle check goes
blind on every one of them. The rule now states a write place plus a
tolerant read, declines repair outright per ADR 0003's posture, and
bars a deliberate duplicate because `status` changes. The audit gains
one clause so the live false negative closes.

### 2026-08-25 — architect, fable 5, concerns (round 2)

One Important, four Minor. The round verified the amendment's factual
basis independently, including the minor-bump claim against the
versioning rule.

- **resolved 2026-08-25** — [Important] the write place, the duplicate
  bar and "nothing repairs" gave no consistent reading for the one
  operation the amendment exists for: writing `status` on an entry that
  already carries it in the co-writer's block. The developer decided
  update-in-place — a field the entry carries is updated where it sits,
  only a missing field is created, and creation goes to the top level.
  The substance lives in the placement section; this line does not
  repeat it.
- **fixed** — [Minor] the measured count read "11 of 20" and the store
  holds 10 of 20, an even split rather than a majority; recounted, and
  the number now appears once, dated, with the other places referring
  to it.
- **fixed** — [Minor] the Out-of-scope bullet named the parked
  second-writer detector as the owner of a repair this spec declines;
  re-scoped to the `docs/` case, with the store's refusal pointing at
  the placement section.
- **fixed** — [Minor] "either placement" now reads as any placement
  inside the frontmatter block, naming no block of the harness — ADR
  0002 declines to bind that shape.
- **fixed** — [Minor] "nothing nags" is scoped to unsolicited reports;
  a grooming walk the developer asked for is not a nag, and its
  standing report of foreign keys is intended.

### 2026-08-25 — architect, fable 5, concerns (round 3)

Dispatched on the spec as the seven consultation-driven amendments left
it. One Important, one Minor, both fixed the same day; the round found
no fault in the store half and confirmed `--crlf`'s behaviour by test.
The frontmatter verdict carries this round's resolution date — round 2's
annotation read identically, and only these records tell them apart.

- **fixed** — [Important] the owner leg of the Misplaced stamp entry
  was never named, though the design makes the owner mandatory and has
  the skill read rather than infer it. The entry now names the
  developer, licensed by the Out-of-scope section's own statement that
  no surface owns the repair.
- **fixed** — [Minor] "unparseable" covered only a missing section,
  while the triple makes a malformed entry possible; the error branch
  now names both.

### 2026-08-25 — architect, fable 5, LGTM (round 4)

Three Minor findings, no Important, none touching a settled decision.
The round re-ran the published commands, the tolerant forms and an
indented-field probe against this repo, and re-checked the versioning
and glossary claims, before judging. All three findings are fixed; the
verdict predates those fixes, each of which narrows a statement the
round itself flagged.

- **fixed** — [Minor] the preamble defined the Unfinished-work list as
  "the published set of grep commands", which the scope paragraph and
  the glossary both contradict — the ticket sweep is published and not
  on the list. The preamble now says what the glossary says.
- **fixed** — [Minor] the frontmatter-hygiene bullet enumerated four
  non-process fields and omitted `status`, the one whose misplacement
  would mislead the lifecycle most; it is now named, with the reason it
  still falls outside the list.
- **fixed** — [Minor] step 7 keyed its offer on a skill match while
  attributing every mechanic to a command, so the seam held by today's
  inventory rather than by contract. The step now states the
  assumption: the offer routes to whatever review surface the matched
  plugin ships. This was the round's one genuine design point, and the
  choice between stating the assumption and accepting the degradation
  was made here rather than put to the developer — a small call, open
  to reversal.
