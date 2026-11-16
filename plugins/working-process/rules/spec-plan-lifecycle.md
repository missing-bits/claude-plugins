---
paths:
  - "docs/specs/**"
  - "docs/technical-designs/**"
  - "docs/plans/**"
  - "docs/**/*-{spec,technical-design,plan}.md"
---

# Judged documents and plans — frontmatter and lifecycle

Design specs live in `docs/specs/`, technical designs in
`docs/technical-designs/`, plans in `docs/plans/`.

A new document is named `<prefix>-<topic>-<class>.md`. The prefix is
the ticket key when the document has a ticket: `ticket-<n>` for a
numeric key (`ticket-42`), otherwise the key in the case the project's
ticket-named files already use, or the tracker's case where none exist
yet (`ABC-123`). Without a ticket the prefix is the ISO creation date
(`2026-07-13`). The class is `spec`, `technical-design` or `plan`, so
one topic's documents never share a name and each name tells its class.
A second design spec for the same ticket takes its own topic
(`ABC-123-login-errata-spec.md`). Documents named before this
convention keep their names. When the superpowers brainstorming or
writing-plans skill writes the document, these names override its
default file name. With `ticket.root` set, a document for a ticket goes
to a ticket directory: see *Ticket directories*.

All three open with a YAML frontmatter block:

```yaml
---
ticket: ABC-123     # tracker reference; inline list when several; `none` without one
date: 2026-07-13    # ISO creation date
status: draft       # moves forward only: draft -> approved -> implemented
grilled: grilling   # optional: `grilling` while outcomes are pending; the ISO date once applied
architect: LGTM     # optional: latest architect verdict (LGTM | concerns | blocking)
adversary: LGTM     # optional: latest plan-adversary verdict (LGTM | concerns | blocking)
architect-fallback: <model> (degraded <date>)   # optional: verdict above produced below the prescribed tier (adversary-fallback: for plans)
integrity: <ISO date> (sha: <short-hash>[; with: <file>@<short-hash>])   # optional: date of the last integrity audit, the body hash it certifies, and — where a technical design was audited with it — that document and its hash
decisions: registered   # optional, design specs only: the body carries a decision register
revises: ./<file>.md   # optional: documents this one departs from; inline list when several
spec: ../specs/<file>.md   # plans and technical designs: the design spec this document descends from; inline list when several, on a plan
technical-design: ../technical-designs/<file>.md   # optional: on a design spec, the technical design that develops it; on a plan, the technical design of each design spec it descends from that has one — inline list when several, each path relative to the plan
branch: feature/ABC-123-short-name   # optional: topic branch of the work
base: master        # optional: branch the topic branch was cut from
---
```

- `status` is linear and moves forward only. Review rounds are iterative
  and live in their own fields; `grilled`, `architect`, and `adversary`
  appear only once the corresponding step has run.
- Every `status` move is the developer's: it happens on their word, or
  under a note in the project's instructions that names that move.
  Under such a note the provisional batch the `review-loop` skill's procedure
  reference defines, when that skill is available,
  goes into the report announcing the move, and its lines stay
  `provisional:` until the developer answers; converting or rewriting
  them on an `implemented` document is a process record, which the
  frozen body below excepts.
- An `implemented` document records what shipped at its release, and the
  surfaces it named are the current truth. Never build from one without
  diffing it against those surfaces first — the document is the archive,
  not the specification of what stands today. It is amended only in
  frontmatter, never in the body: a verdict certifies the body it was
  given, and an `integrity:` hash covers exactly that text. One class of
  body edit is excepted: a ledger annotation recording a process event,
  such as `, debt discharged <date>`, is a process record rather than a
  design amendment.
- `revises:` names the documents a newer one departs from — written on
  the newer document, pointing back, and never on the older one, which
  stays as its stamps left it. It records supersession, not lineage: a
  document that merely builds on another says so in its prose, and a
  plan's `spec:` pointer is lineage too. What `revises:` claims is that
  the named document's design no longer matches what shipped.
- A round that ends in `concerns` or `blocking` records its findings (or
  their disposition) in the document body — a verdict whose findings were
  never written down cannot be honestly resolved later.
- Concerns resolved without a fresh review round keep the verdict and
  gain a resolution date — `adversary: concerns (resolved 2026-07-16)` —
  plus a body note saying what resolved them. A fresh round replaces the
  whole value as usual. A `blocking` verdict the developer closes by
  explicit adjudication instead of a fresh round takes the same form with
  its own token — `architect: blocking (adjudicated 2026-08-17)` — and
  the round's ledger record as that body note. On a plan both wait for
  the confirming round: neither is written while the latest round
  heading is diff-scoped, unless the plan is already `implemented`,
  where the annotation — or the developer's adjudication — is written
  citing that standing decision. Its body note is written too: a note
  recording what resolved a verdict is a process record, which the
  implemented-document rule above excepts from its frontmatter-only
  clause, as it excepts `, debt discharged <date>`.
- A verdict produced below the prescribed tier (the model-selection
  heuristic in the workflow rule) gains a companion `architect-fallback:`
  / `adversary-fallback:` field: the family alias of the model that
  produced it, then `(degraded <ISO date>)` for anything other than the
  developer's deliberate choice (a cap refusal — including a consented
  one-tier drop — a silent platform substitution, or an under-dispatch
  the dispatcher did not knowingly decide) or `(chosen <ISO date>)`
  when the developer deliberately dispatched below the prescribed tier
  before any refusal. A dispatch at the prescribed tier gets no field.
- Both tokens carry a re-review offer at the document's next consumption
  gate — before plan-writing for a judged document, before
  implementation for a plan. Accepted: a fresh round at the prescribed
  tier replaces the
  verdict and removes the field (a fresh round that is itself below the
  prescribed tier refreshes the field's date instead, and the offer
  re-arms at the same gate). Declined: the field gains `, waived <date>`.
  Moving `status` to `implemented` with a bare fallback field stamps the
  waiver as part of the move.
- `integrity:` records an integrity audit — the run the
  `integrity-auditor` agent performs, when it is available — which the
  dispatcher stamps once the audit's dispositions are applied:
  `integrity: <ISO date> (sha: <short-hash>)`, the date for the reader and
  the hash for the check. The hash covers the text below the
  frontmatter's closing `---`, so writing the stamp never invalidates what
  it stamps. Where the audit also discharges a chain debt, the annotation
  is written before the hash is recomputed: the annotation lands inside
  the hashed body, so a stamp written first is stale the moment it lands.
  Stamper and gate run one command, so the comparison can never
  mismatch on convention:
  `sed '1,/^---$/d' <file> | shasum | cut -c1-7`
  — `shasum` rather than `sha1sum` because stock macOS ships only the
  former, and the two produce identical digests, so a GNU-only environment
  may substitute `sha1sum` without changing a recorded hash. The field
  carries no verdict: it answers whether the document was checked after
  its last edit, and that answer is a comparison rather than a clock. A
  recomputed hash differing from the stamped one means unaudited, same-day
  edits included; any change re-arms the stamp, a typo fix included.

  A design spec that names a technical design is audited with it as one
  target — an **audit pair** — and one stamp records it. The stamp
  lives on the design spec, names both documents and both body hashes,
  and the technical
  design carries no `integrity:` of its own — it owes the check like any
  judged document and discharges it jointly. The value takes the form
  `integrity: <date> (sha: <own-hash>; with: <file>@<their-hash>)`,
  where `<file>` is exactly the value the design spec's
  `technical-design:` pointer carries, read relative to the design
  spec's directory, so the gate can check that the recorded value still
  equals the pointer. Changing either document unsettles the pair, and
  the gate
  recomputes both hashes to see it; because the two pointers are what
  identify the pair, an added, removed or repointed `technical-design:`
  unsettles it too.
- A judged document's consumption gate owns the recomputation: before
  plan-writing it
  recomputes the body hash and compares, a match meaning the standing
  stamp satisfies the gate and a mismatch firing the audit offer. Those
  are judged-document semantics — on a plan, a permitted target on
  explicit
  request, the stamp is informational and goes stale silently. Staleness
  joins no Unfinished-work entry: it is a recomputation, not a grep.
- Verdict agents self-report the model they ran on (family plus version);
  the dispatcher compares it against the dispatched and prescribed
  tiers before stamping, and each round's verdict, model, and date are
  recorded in the document body. A self-report cannot reveal a
  substituted model — thirteen runs dispatched on one family ran on
  another while reporting the dispatched one — so where the agent's
  transcript is readable (in Claude Code, the task's output file) the
  model the API recorded, read as its family, decides the comparison:
  `jq -r 'select(.type=="assistant") | .message.model' <transcript> | sort -u`.
  Where it differs from the self-report, the record, the round heading
  and the relay carry the transcript's model, the self-report beside it
  in parentheses. Without a readable transcript, or where the command
  prints nothing, the self-report comparison runs as before and the
  relay calls it unchecked, never a match. Committed examples of the
  bare fallback form use
  placeholders (as above) so they never match the Unfinished-work list.
- `branch` and `base` appear once the topic branch exists — never guessed
  up front, omitted entirely when there is no topic branch.
- `technical-design:` is optional and appears once the technical design
  exists, so its absence means there is none rather than one nobody
  linked. On a design spec it is new in kind: every other pointer
  records where a document came from, while this one names a document
  written later, and it gives a reader holding the design spec the
  structure that develops it. The author who creates the design writes
  both ends in
  the same turn — the design's `spec:` and the design spec's
  `technical-design:`. A plan's `technical-design:` names, for every
  design spec its `spec:` names that has a technical design, that
  technical design — an inline list when several, each entry the same
  document the design spec's own pointer names, its path written
  relative to the plan's directory rather than copied. A design spec
  with no technical design contributes no entry, so a plan from specs
  `a` and `b`, where only `a` names a design, carries that one design.
  One technical design per design spec.
- `decisions:` is optional, on design specs only, and takes one value,
  `registered`: the spec carries a decision register, defined under
  *Decision register* below. It is a convention field rather than a
  process stamp — no review step writes it, and no Unfinished-work
  command reads it.
- Where a plan's `technical-design:` names documents, those documents
  define the interfaces. The plan's `**Interfaces:**` blocks reference
  the contracts they define and say which part of one each task
  implements or changes; they do not independently redefine those
  contracts. Where a plan names no technical design, the existing plan
  convention stands unchanged. This binds how the blocks are filled and
  changes no plan template. The template belongs to the tool that
  writes plans, with one exception, defined under *Plan annotations*
  below: this rule adds the `**Realizes:**` annotation on tasks and
  Global Constraints entries, and the `## Deferrals and predecessors`
  section with its `**Defers:**` and `**Follows:**` lines. The rest of
  the template stays with that tool.

## Ticket directories

With `ticket.root` set, a new design spec, technical design or plan
whose `ticket:` yields a file prefix goes into the ticket directory
`<root>/<prefix>-<topic>/`, one level below the ticket root and named as
above. A ticket value yielding no prefix, or `none`, leaves the document
in its class directory.

Before creating a directory, look for one. List the root's immediate
subdirectories whose name starts with `<prefix>-`, ignoring case; the
trailing hyphen keeps `abc-14-` from matching `abc-1489-`. Search two
places:

- the working tree, listed from the repository's top level
  (`git rev-parse --show-toplevel`);
- the integration branch, with
  `git ls-tree --full-tree -d --name-only <ref> <root>/`. Without
  `--full-tree` git reads the path from the current directory, and a run
  below the top level prints nothing and exits 0.

The integration branch is the one topic branches are cut from, as the
project's instructions name it; where they name none, ask once. A
document's `base:` cannot serve, since the lookup runs before the
document exists. `<ref>` is the branch's remote-tracking ref
(`origin/develop`) where one exists, else the local branch. Never fetch:
that stays with the developer. A branch that exists nowhere skips the
second lookup; say so.

One match is used whatever its topic. With no match, create the
directory with the topic of the creating document. A file prefix and a
new directory take the case the project's existing ticket-named files
and directories use, else the tracker's case. Several matches, or a
`ticket:` list of several keys, go to the developer, who picks one of
the existing directories; while one exists, offer no new directory. Where
no listed ticket has a directory, the developer picks the ticket whose
directory is created. A review command asks before dispatch, a session
before it writes the document.

With `ticket.root` set, a process document opens with frontmatter
carrying `status:`. A file matching a class suffix or lying in a class
directory, but without `status:` in its frontmatter, is not a process
document: it belongs to the developer, and the process neither adds
frontmatter to it nor reports it.

Frontmatter links are relative to the document that holds them. In a
ticket directory the documents of one chain are siblings
(`spec: ./ABC-123-login-spec.md`); a link from a ticket directory to a
class directory climbs further (`../../specs/<file>.md`). The
`../specs/<file>.md` examples in the frontmatter block above read as
relative links, not as templates.

### Moving a document into a ticket directory

With `ticket.root` set, a document written without a ticket may later
belong to one. Move it only on the developer's command, never on the
session's initiative. Six steps:

1. **Ticket.** Take the document's `ticket:` value, or the command's
   when that value is `none`. Where several tickets apply, ask which one.
2. **Chain.** Find the documents the moved one links to and those that
   link to it, by `spec:`, `technical-design:`, `revises:` and
   `**Follows:**`. Offer to move them together, as one move.
3. **Names and moving.** Each moved file takes the convention's full
   name in the ticket directory and keeps its own topic. A file named
   before the convention gains its class suffix; its topic is its name
   without a leading date and a trailing `-design`, or its whole stem
   where neither is there. Move a tracked file with `git mv`, an
   untracked one (uncommitted, or in an ignored class directory) with
   `mv`; nothing is staged, since committing stays with the developer.
4. **References.** Before any rewrite, compare each affected
   document's `integrity:` hashes (its own `sha:` and any `with:` hash)
   with the bodies as they stand, and note which matched. Then rewrite
   inbound and outbound frontmatter links, the `with:` file in
   `integrity:`, `**Follows:**` lines, and qualified decision
   identifiers (`<file>.md#D3`) in bodies. A body edit that an
   `implemented` document would need stops the move and goes to the
   developer; its frontmatter may change, since the `integrity:` hash
   covers the body only.
5. **Hashes.** A rewritten path changes no content, so the move asks
   for no new audit. Recompute after the rewrite, with the hash command
   above, only a hash noted in step 4 as one that
   matched its body before the move, and keep the audit date. A hash
   that did not match stays as it was: recomputing it would stamp edits
   nobody audited.
6. **Report.** References outside `docs/` and paths in body prose are
   listed, never rewritten. Report every path rewritten, every
   reference left alone, and each untracked file that now lies in the
   tracked ticket directory.

## Decision register

A design spec that sets `decisions: registered` carries a `## Decisions`
section — the decision register, the enumerable list of the decisions
the spec makes that need realization. The propagation auditor, when
that agent is available, derives a plan's decision coverage from it.

The register is an index, never a copy. An entry is one identity
paragraph — the identifier and a short statement of the decision — and
may name the section that argues it:

    - **D3** — <a short statement of the decision>. Argued in *<section>*. [state token]

      <optional prose, indented, after a blank line>

The identity paragraph is the list item's first paragraph: its opening
line and the continuation lines after it, up to the first of a blank
line, a nested list item, the next list item at the same or a higher
level, or the end of the section. A reader joins those lines,
normalising whitespace, before parsing, so a statement wrapped across
lines keeps its state token at the paragraph's end. Prose beneath the
blank line is free. The grammar enforces the paragraph's shape, never a
sentence count: restating the argument in the register would give the
decision two homes, and the first fix wave would leave the register
describing the decision's old form.

The identifier is the literal token `**D<n>**`, or `**D<n>.<m>**` for a
child, at the start of a list item under `## Decisions`; a child's item
nests under its parent's. Identifiers are unique within the spec and
never positional, renumbered or reused: a decision added mid-loop takes
the next free number. A Markdown numbered list is refused, because its
numbers are positions and move when an item is inserted above. An
element of a list that needs realization on its own takes a child
identifier. The parent of children is a group: it enters no count, a
citation of it covers none of its children, and it carries no state
token.

Every decision that needs realization enters, cross-cutting constraints
included. A ruling that something stays as it is enters too, since an
implementer can break it, and a plan realizes it as a constraint; no
kind of entry is exempt. A rejected alternative never enters: nobody
realizes it, and it already has homes — a spec's out-of-scope section,
a technical design's *Cuts not taken*.

An entry without a token is active. One state token exists, carried by
a leaf or not at all, and never by a group:

    withdrawn <reason>, ruling: <date>[; replaced by <id>]

The decision no longer stands. The entry stays as a tombstone that
reserves its identifier, so a reuse shows up as a duplicate.
`replaced by` names an identifier of the same register other than its
own, and a chain of successors never forms a cycle; a successor may
itself be withdrawn. The token is recognized by its opening word alone:
the first segment after the full stop that ends the statement, and after
any "Argued in" pointer, that begins with `withdrawn`; it runs to the
paragraph's end, so its reason may hold a full stop. A segment so
opening that does not match the grammar is malformed, never prose.
Withdrawing a group is written on each of its leaves. A decision that
still stands but one plan does not realize is no state of the entry:
that plan defers it (see *Plan annotations*).

A withdrawal changes what the spec decides, so the session writes the
token only on the developer's explicit decision. Its `ruling:` is dated
with that decision; the edit lands in the spec's own ledger and leaves
the `integrity:` stamp stale, as any body edit does. On a spec whose
loop has closed, a withdrawal ruled outside any hit or finding writes
no ledger line: the tombstone is its record, since no diff-scoped round
follows a close. A spec already `implemented` takes no such edit: the
decision is withdrawn by a newer design spec carrying `revises:` and the
register that stands.

The spec's author creates the register while writing the spec, so a
design that never meets a grilling session still has one, and a
grilling session updates it as its decisions land. A spec carrying the
field declares a rule about itself: *the register lists every decision
in this spec that needs realization.* The integrity audit's first lens
verifies a document's declared rules in both directions, which gives
the register's completeness its reader.

A design spec without the field is legacy: the propagation audit
reports it as not checked and raises no hit, and a plan descending from
legacy specs alone carries no annotations. An existing spec migrates
when it is next substantively revised, never in a sweep. Every new
design spec is expected to set the field; its absence is reported, not
refused.

## Plan annotations

A plan whose `spec:` names at least one registered design spec carries,
on every task, one line after its `**Files:**` block — after its
`**Interfaces:**` block where it has one — and before its first step:

    **Realizes:** D3, D5
    **Realizes:** none

`none` is a value, not an omission: without it a housekeeping task
cannot be told from an author who forgot. One decision may be cited by
several tasks, and a task split or merged in a fix wave stays covered as
long as the union of its identifiers survives. A cross-cutting
constraint is realized by the Global Constraints entry that states it,
and that entry opens with the same annotation as its first clause —
`**Realizes:** D9`. Only an entry that realizes a decision carries one,
and `none` is never written there. Citing the section as a whole
realizes nothing, and neither does citing a group: its leaves are what
a plan cites. `none` names no identifier, so it is never qualified.

A plan whose `spec:` names one spec writes bare identifiers. A plan
whose `spec:` names two or more — registered or legacy alike — qualifies
every identifier with its spec's path exactly as `spec:` writes it,
`../specs/<file>.md#D3`, wherever the plan or its audit names one. The
count of entries decides, never the count of registered ones, so
migrating a second spec out of legacy changes no annotation already
written.

Two more kinds of line form a section of their own, headed
`## Deferrals and predecessors` at the Global Constraints heading's
level and placed directly after that section. They state facts about
the whole plan rather than requirements of any task, so they stay out of
Global Constraints, which the plan template makes part of every task's
requirements:

    **Defers:** D6 — <why>; ruling: <date>
    **Follows:** ../plans/<file>.md

A `**Defers:**` line records that this plan leaves a standing decision
unrealized, one line per identifier, qualified as the annotations are.
The session writes it only on the developer's explicit decision, which
its `ruling:` dates. The deferral binds this plan alone: auditing any
other plan of the same spec, the decision counts, and the spec names no
plan. Deferring an undefined, withdrawn or group identifier is
malformed, and so is deferring one the plan also cites, locally or by
inheritance. A plan with neither kind of line carries no such
section, and in the pass for one spec a `**Defers:**` line naming
another spec's identifier is out of scope.

A `**Follows:**` line names a plan this one continues, by a path
relative to the plan. The predecessor shares at least one spec with
this plan's `spec:` and carries `status: implemented`, since only a
frozen body's citations cannot move. This plan inherits every
identifier the predecessor's `**Realizes:**` annotations cite for the
specs both plans name, and nothing else — never its `**Defers:**`
lines, and never its `**Follows:**` lines, so inheritance is not
transitive and a plan names every predecessor whose citations it relies
on. An inherited citation of an identifier the register withdrew after
the predecessor shipped covers nothing and raises no hit; a local
citation of it still does. Whether the predecessor's realization still
stands in the code is not this line's question: the diff the
implemented-document bullet above prescribes answers it.

An annotation, a `**Defers:**` line or a `**Follows:**` line counts
only at the place this section gives it: a task's line before its first
step, the opening clause of a Global Constraints entry, a line of
`## Deferrals and predecessors`. The same text inside a code block, or
quoted as an example, describes the grammar and instantiates nothing.

The plan's author writes these lines, whoever that author is. A session
writing a plan meets this rule by reading the design spec, and a brief
that delegates plan-writing to a separate context names this rule and
requires reading it first, as the workflow rule's step 4 says. A plan
lacking an annotation is caught at its first propagation gate, and an
identifier is added there only where the task's text actually realizes
the decision, never mechanically.

## Finding what revises a document

`revises:` points backward only, so the documents that departed from a
given one are found by sweeping for it. The line matches both the
single-reference and inline-list forms, `--no-ignore` reaches
ignored-mode artifacts, and the tolerant leading anchor finds the field
where a second writer relocated it:
`rg -l --no-ignore --crlf '^\s*revises:.*<file-stem>' docs/`

This is a lookup, not an Unfinished-work entry: a `revises:` pointer
owes nobody a next move, and the implemented-document principle above
already warns every reader of an archived document without it.

## Lifecycle offers

Each an offer the developer may decline, and each made
only when the tool is available: grill a fresh spec (grilling-session);
architect-review a grilled design spec, and a technical design, which
is never grilled (architect agent dispatch);
adversary-review a plan before implementation (plan-adversary agent
dispatch); offer the pending re-review of a fallback-recorded verdict at
its consumption gate (fresh round at the prescribed tier); and when a
judged document or plan moves to `implemented` and the
memory-review-session skill
is available, offer a Project memory review — released work-state notes
close, resolved entries sweep to the archive.

A technical design is a judged document and takes the design spec's side
of every branch in this rule: the same fields, the same
consumption-gate semantics for a stale stamp, the same owner for an
unresolved verdict, and the same pair offer against chain debt. It is
not grilled — grilling stress-tests terminology against the project
glossary, and a technical design mints none: its vocabulary comes from
its design spec, which was grilled, and from the domain's own skills.
The names it does mint are part and component names, checked against
those skills where one exists and recorded as a vocabulary gap where
none does.

One mechanism it shares rather than owns: the integrity check is due on
it like any judged document, and one audit of the audit pair — the
design spec together with the technical design it names — discharges it,
so the `integrity:` stamp sits on the design spec and names both.

A document's consumption gate is the backstop for its ledger: no judged
document passes to plan-writing, nor a plan to implementation, while
`held` lines or `hit held` gate lines stay open, nor a judged document
while its `provisional:` lines do — an LGTM can leave the
frontmatter clean while a decision question still pends, so the gate
asks those questions at the latest. A `hit held` line blocks until the
gate has re-run and rewritten it to a terminal shape, since declining
the dispatch it guarded decides nothing; a closed gate line blocks
nothing. Writing a plan from a judged document is that same seam: its
held questions are asked before the plan is written, whoever writes it.

A technical design's own consumption gate is plan-writing, the same
moment as its design spec's, and one ordering binds the two: writing
the design and applying its review dispositions precedes the joint
integrity audit, because the design is the last producer of changes to
the design spec and certifying that body before the design's questions
are answered stamps a body about to change. The dependency reaches no
further — every other item of the two gates stays unordered.

The gate therefore runs in passes. The first pass decides whether a
technical design is written at all. Where the offer is accepted, the
gate suspends until the design exists and its review dispositions are
applied, then resumes and collects the questions the documents' current
state raises. Answers already given stay binding unless the basis they
rested on changed. Each pass asks its questions in one batch, as a
review round does — a batch being every question answerable at that
pass, never every question the gate will ever ask.

A technical design's `status` reaches `implemented` with its plan's, in
the same turn and by the same hand, since otherwise the rule freezing an
implemented document's body never reaches it.

The process suggests committing the work's documents under `docs/` at
exactly one point — the implementation-ready gate: the developer has
approved the plan (the `status` flip to `approved`) and implementation
is about to start. During authoring — spec drafting, grilling,
technical-design writing, review rounds, plan writing — it never makes
that suggestion; the documents'
uncommitted state is deliberate, not dirt in the process-artifacts
sense, and the developer may commit sooner on their own call. The
suggestion covers only paths git tracks or would track; deliberately
ignored documents are skipped silently, and committing itself stays
with the developer.
One shape of that sooner commit, per-round commits on a document
branch, has a convention: when the `review-loop` skill is available,
its procedure reference holds it, with the document branch's merge at
this gate.

The disposition ledger — the round headings, disposition lines and gate
lines a document carries under `## Review rounds` — is defined in the
`review-loop` skill's ledger reference, when that skill is available.
The Unfinished-work list is the `process-status` skill's
Unfinished-work reference, when that skill is available.

Ticket value format, sourcing order, and backfill live in the
ticket-frontmatter rule.
