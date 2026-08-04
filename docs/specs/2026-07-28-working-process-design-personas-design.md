---
ticket: none
date: 2026-07-28
status: draft
grilled: 2026-07-30
architect: concerns (resolved 2026-07-30)
branch: feature/design-personas
base: develop
---

# Design personas — a system designer alongside the architect

## Problem

The working-process plugin ships one design persona, the architect, across
two surfaces: the `architect` agent (formal design-quality review ending in a
verdict the dispatcher stamps into a document's `architect:` field) and the
`architect-session` skill (interactive in-session consultation, no
verdict). A third component, `plan-adversary`, hunts failure modes in
plans.

Two gaps follow. First, nobody owns the *mechanics* of a system — what its
parts are, what crosses the boundaries between them, what state it keeps,
how it behaves when loaded. The architect judges whether a shape is right;
it does not produce one, and its own persona file says so. A developer
forming a design has a critic available and no counterpart to help build
the thing being criticized.

Second, design expertise comes in only two shapes today: a formal review
that ends in a stamped verdict, or a conversation held in the main thread.
There is no way to ask a persona for a contribution from a fresh, isolated
context without also asking it for a verdict.

## Scope

This spec covers a second persona, the files that define both personas
without duplication, a consultation surface for each, and a consent-based
offer that brings them into a design conversation. It does not change the
spec/plan lifecycle, add a review gate, or alter what the `architect` agent
does with a document. Model-selection mechanics stay owned by the workflow
rule.

Two changes fall outside the plugin and are in scope deliberately: the repo
authoring rule learns the `*-consult` naming category, and the versioning
rule's prerelease grammar widens so a topic branch without an issue number
can still be dogfooded. Both are consequences of this change that would
otherwise leave a repo rule contradicting the code it governs.

One behaviour change to an existing verdict-bearing component is
**declared, not incidental**: `plan-adversary` starts sourcing its standing
duties from the shared persona file and thereby gains the domain-expertise
duty it does not have today. This is intended — a plan reviewer that
verifies load-bearing facts against documentation is strictly better — and
is called out because a silent widening of a gate's behaviour would not be.

### What was cut

An earlier draft orchestrated both personas through
`superpowers:brainstorming`: a warm-start spawn, two consultation
checkpoints, agents kept alive across the conversation and resumed by
message, a delta-briefing contract, and a record of what each persona had
been told. That machinery is gone; the reasoning is under non-goals,
because the argument is worth keeping even though the feature is not. What
survives from it is the *offer* — being asked, which cost nothing — not the
bookkeeping.

### Minimum viable version

So a later reader can judge whether the structure is earned: the minimum
that solves the stated problem is `SYSTEM_DESIGNER_PERSONA.md` plus
`system-designer-consult`. Everything else is added for a named reason —
`PERSONA_COMMON.md` because three components would otherwise carry
duplicate duty text that has already been observed to diverge;
`architect-consult` because the second half of the problem (a contribution
without a verdict) applies to the architect too, and its own agent cannot
suppress the verdict its report format requires;
`system-designer-session` because a skill body loads into the main thread
and can therefore carry the handoff into a consult dispatch, which no agent
file can.

## Verified platform facts

### Doc-verified (Claude Code docs, July 2026)

- A non-fork subagent "starts with a fresh, isolated context window. It
  doesn't see your conversation history, the skills you've already
  invoked, or the files Claude has already read."
- A fork "inherits the entire conversation so far instead of starting
  fresh. This drops the input isolation that subagents otherwise
  provide." Its first request reads the parent's cache.
- `SendMessage` "doesn't require agent teams to be enabled" and is in a
  background subagent's default tool pool. The sibling roster "appears
  only when the subagent's tools include `SendMessage` and at least one
  other agent has a name", and needs Claude Code 2.1.206 or later.
- A teammate's coordination tools override `tools` / `disallowedTools`.
- `disallowedTools` is a documented frontmatter key for both subagents and
  plugin agents: "Tools to deny, removed from inherited or specified
  list". `background` and `isolation` are likewise plugin-agent keys;
  `permissionMode`, `hooks`, and `mcpServers` are not available to them.
- A dispatching thread sees only an agent's `name` and `description` when
  choosing it; the agent's body becomes the subagent's system prompt.
- Subagent output is not shown to the developer; the dispatching thread
  receives it and relays what matters.
- "Latency matters. Subagents start fresh and may need time to gather
  context."
- "Subagents use the five-minute TTL even on a subscription, since the
  automatic one-hour TTL applies to the main conversation."
- The `memory` field takes `user | project | local` and grants the
  subagent a persistent directory across conversations.
- The default subagent nesting depth has changed across releases (5 on
  2.1.172–2.1.216, 1 on 2.1.217–2.1.218, 3 from 2.1.219).

### Locally verified (Claude Code 2.1.220)

- `claude plugin validate` passes at the repo root and for the plugin with
  the new `disallowedTools` key and quoted descriptions.
- `disallowedTools` with a bare string value loads without error.
- A consultation dispatched by pointing an agent at persona files on disk
  behaves as intended — this is how the trial described under Trial
  evidence was run.

### Undocumented — treated as unknown

- The minimum Claude Code version for `disallowedTools`, and what happens
  to an agent file carrying an unrecognized frontmatter key: ignored with
  the agent still loading, or the agent failing to load. The two branches
  have different consequences and both are covered under accepted risks.
- Whether an agent's body reaches the dispatching thread before dispatch.
  Treated as "no", which is why every dispatcher-facing obligation is
  duplicated into `description`.

## Design

### 1. Two personas, split by dimension

The two personas are distinguished by the question they answer, not by
their stance toward the material:

- the **system designer** asks *what the parts are and how they interact*;
- the **architect** asks *whether that shape is right*.

The system designer's dimensions: parts and responsibilities; interactions
and contracts; state and its lifecycle; behaviour under load;
observability; technology choice. The architect keeps its own: fit,
boundaries, over-engineering, alternatives, convention fit.

Proposing a decomposition is the designer's work; grading it is the
architect's. Each persona names and hands over what belongs to the other
rather than filling the gap itself.

The system designer must be able to answer "not applicable here", with one
line of why, for any dimension the subject genuinely lacks: six mechanics
dimensions create real pressure to fill them, and a persona that invents a
load profile for a markdown plugin spends the developer's attention on
noise. Dropping a dimension silently is the opposite failure — it is named
and dismissed. This licence stays in the designer's own persona file. It
cannot move to the shared file, because `plan-adversary` reads that file and its
own instruction is the opposite: walk every dimension, nothing passes by
default.

### 2. Persona files and single-sourcing

`PERSONA_COMMON.md` at the plugin root holds what is not specific to one
persona, and is read by both personas and by `plan-adversary`:

- the **domain-expertise duty** and the **glossary/ADR duty**;
- the **boundary between the personas**, including its third leg —
  `plan-adversary` asks *how this will fail in execution*, and stands
  outside the design-quality/mechanics split rather than inside it. A
  consumer must not read a boundary that omits it;
- the **consultation contract** of sections 6 and 7, which both
  `*-consult` agents would otherwise duplicate. This section carries its
  own scoping clause, mirroring the boundary's `plan-adversary` carve-out:
  it binds `*-consult` dispatches and their dispatcher only — the file's
  verdict-bearing consumers (`plan-adversary` directly, `architect` via
  its persona file) grade and stamp by duty, and must not read a sentence
  saying contributions are never graded as binding them. The file's
  opening ("All three are defined only here") is reworked when this
  fourth section lands.

The extraction is driven by evidence, not tidiness. A first draft
duplicated the boundary across both persona files and the two copies had
already diverged — four criteria against three — before anyone read them.
The same pattern then reappeared in the two `*-consult` files: roughly 70%
identical body text, with the divergence already started (one file carried
"formal review ending in a verdict belongs to the `architect` agent", the
other did not, though it is the architect that has the verdict-bearing
agent). The repo authoring rule sets the threshold at two consumers; this
is three and two respectively.

Two consequences to state rather than discover:

- **`plan-adversary` adopts the file whole**, gaining the domain-expertise
  duty. Declared in Scope. Its `*-plan-review` checklist mechanism becomes
  the first source under that duty rather than a parallel one.
- **The glossary duty's wording is looser in the shared file** ("must be
  called out, citing the file") than the two verdict-bearing agents need.
  Both `architect` and `plan-adversary` re-tighten it to "earns a finding"
  on their own surfaces; the spec says so for both, not only the architect.

The persona files stay at the plugin root under their current names, and
join `ARCHITECT_PERSONA.md` in the versioning rule's list of public
surfaces whose rename is a breaking change.

Persona files point at the shared file in prose rather than through
`${CLAUDE_PLUGIN_ROOT}`, because a persona file is read as raw text by an
agent that has already resolved its own root — the variable would not
expand. This is not an exception to the authoring rule, which bans absolute
paths and says nothing about prose; it is recorded only so nobody "fixes"
it into a variable.

### 3. Surfaces and how the right one gets chosen

| Surface | Persona | Input | Output | Context |
|---|---|---|---|---|
| `architect` agent | architect only | a document | verdict, stamped | fresh, isolated |
| `*-consult` agent | both | a briefing | contribution, never stamped | fresh, isolated |
| `*-session` skill | both | live dialogue | contribution, never stamped | the main thread |

The architect has three surfaces, the system designer two. The designer has
no verdict-bearing agent; its review counterpart is the existing architect
gate, which reads the spec the designer's contribution shaped.

**Why the architect needs a third surface.** Its own agent cannot serve as
a consultation: that agent's report format requires a Verdict section, so
any dispatch produces a verdict word, and a produced-but-unstamped verdict
is exactly the contamination the formal gate must not carry. The argument
belongs here rather than only in the non-goals table, or the third surface
reads as symmetry.

**Choosing between the two consultation surfaces.** The distinction is
isolation against interactivity: the consult agent protects the main
thread's context and is unshaped by the conversation so far; the session
skill supports live back-and-forth and immediate correction. That
distinction is real but it is *not* a phrase anyone says, and a surface is
selected from what the developer actually types. Today
`architect-session`'s description carries verbatim trigger phrases ("ask
the architect", "porozmawiajmy z architektem") under a hard "Use ONLY
when", while a consult agent would carry an abstract criterion. The session
skill would therefore win systematically — including on the very sentence
this spec calls ambiguous.

So the arbitration is lexical, not conceptual:

- each consult surface gets its own trigger phrases naming isolation or a
  second opinion ("konsultacja z architektem", "zapytaj designera na
  świeżo", "second opinion from the system designer", "consult the
  designer from a clean context");
- each session skill's description gains a counterpoint naming its consult
  agent by name, and vice versa;
- on a genuinely ambiguous request the main thread asks one short question
  — in-thread or from a fresh context — rather than silently picking. This
  matches the plugin's culture, where everything is an offer.

A session skill's body loads into the main thread, which gives it a job no
agent file can do: it carries the handoff, telling the developer how to
escalate the same question into a consult dispatch and what to brief it
with. That is the concrete reason `system-designer-session` exists beyond
symmetry.

### 4. Consultation mechanism — one dispatch, self-contained

A consult agent is dispatched when a consultation is wanted, answers once,
and is not kept alive. It is not resumed, not spawned ahead of need, and
carries `background` in its frontmatter so that running as a background
agent — which section 10 relies on for verifiability — is true by
construction rather than by the dispatcher's habit.

The isolation this buys is the point. Two worries motivated it: polluting
the main conversation's context with a persona's instructions, reasoning,
and file reads; and a persona's judgement being shaped by everything the
conversation has already committed to.

| | context pollution | conversation bias |
|---|---|---|
| persona loaded in-session | not solved | not solved |
| fork | solved | not solved (inherits the history) |
| fresh one-shot subagent | solved | solved |

Being self-contained removes the hardest problem the orchestrated draft
had. When a persona is kept alive, every later briefing must state what
changed since the previous one, the dispatcher must track what each
persona has already been told, and that record is exactly what a
compaction of the main thread destroys. A single dispatch has no delta to
compute and no state to lose, and cannot accumulate its own bias across
successive briefings.

The five-minute subagent cache TTL is the other reason not to hold a
persona open: a persona resumed after a human-length pause re-reads its
entire accumulated transcript uncached, every time. One dispatch pays for
its context once.

### 5. Independence between personas

When both personas are consulted on one subject, they are consulted
independently. Two agents that reconcile privately hand back one opinion
where the developer asked for two, and their disagreement is the most
useful thing they produce.

The mechanical half is `disallowedTools: SendMessage` on both consult
agents. This is not a relic of the orchestrated draft: consulting both
personas on one subject means two concurrent background dispatches, both
named, so the sibling roster would otherwise appear — and since the roster
needs 2.1.206 while the plugin's floor is 2.1.207, it is live on every
supported installation. The key therefore has real effect wherever the
plugin runs at all.

Two limits are recorded rather than papered over:

- consult agents keep the `Agent` tool, so a persona could spawn its own
  copy of the other persona and fold the result into one answer. Removing
  `Agent` is the worse trade: the domain-expertise duty asks for
  documentation verification, and both personas used a lookup subagent for
  exactly that during the trial. The limit is textual — helpers for search
  and documentation are allowed, a second working-process persona never is. The
  argument does not rest on helpers being available, since nesting depth
  has varied by release and has been 1; where no helper can be spawned,
  the duty's own "when available" wording governs and web lookup remains;
- `disallowedTools` binds only when the dispatch goes through the agent
  file. A dispatcher that pastes a persona inline gets no enforcement.

The substantive half is what the briefing says, and it decides the outcome
regardless of any tool: a briefing sentence saying "the architect raised X"
produces convergence with no message between agents at all. Hence section
6 — and hence that contract living inside the plugin, not only here.

### 6. Briefing contract

A consult agent knows only what its briefing says, so the briefing is a
defined artifact. Two of its three rules are invariants *across*
dispatches, which no agent can enforce because no agent sees the other's
briefing — the obligation is the dispatcher's. That makes its location
load-bearing: this spec does not ship with the plugin, so the contract
lives in `PERSONA_COMMON.md`, and the two cross-dispatch invariants — the
only rules no agent can enforce — are duplicated into each agent's
`description`, the only surface a dispatching thread reads before
choosing, as one sentence: "When both personas are consulted on one
subject, give both the same canonical briefing (each with its own
focusing question appended) and tell neither what the other said." The
plugin already uses this device — the `architect` agent's description
restates the stamping obligation from its body for the same reason.

The base case is **one** dispatch, which is the ordinary path now that
nothing fires on a schedule:

- **Contents**: the subject; the constraints that bind it; and, stated
  separately, what the developer has already decided against what is
  still open. A persona that cannot tell a settled decision from an open
  question either re-litigates the settled one or treats an open one as
  fixed.
- **Point, don't paste.** What a consultation reads is what it costs, so a
  briefing names the files and the area rather than inviting exploration.

When both personas are consulted on one subject, two further rules apply:

- **One canonical briefing text**, given to both, each with its own
  focusing question appended. Two personas briefed differently return two
  opinions about two different subjects, and nothing in the output would
  reveal it.
- **No cross-persona content.** Neither is told what the other said. A
  cross-check dispatch — "the architect argued X; does that hold
  mechanically?" — is legitimate on explicit request, and is labelled as
  one so the reply is read as a response rather than as an independent
  opinion.

### 7. Reporting contract

Subagent output never reaches the developer directly; the dispatching
thread relays it. That thread is both a lossy channel and the same actor
that wrote the briefing, so a silent synthesis would hand the developer
one reconciled opinion — the failure of section 5, moved one node closer.

- Each contribution is relayed **attributed, in its own block, and
  substantially verbatim**. Compression is allowed; merging is not. The
  checkable floor: every recommendation and every named risk survives, and
  text from two personas never lands in one bullet.
- Where the personas disagree, the disagreement is presented **as a
  disagreement**, with both positions, and the choice is the developer's.
- The relaying thread may add its own opinion, marked as its own.
- The developer can verify the relay rather than trust it: a consult agent
  is a named background agent, so its transcript can be opened and read.
  Naming the agent at dispatch is therefore part of this contract, not a
  nicety.
- A persona's output is a **contribution**, never a *finding* — that noun
  is reserved by the glossary for the graded unit of a verdict-bearing
  review round. One noun, used in the persona files, the agent bodies, and
  the descriptions alike.

### 8. The offer

Consultations are not something the developer must remember to ask for,
and not something that fires unasked. Once, early in a design
conversation, the main thread asks whether the two personas should be
consulted as the design forms. Three answers:

- **yes** — from then on, a consultation is dispatched when it looks
  worth its cost, without asking again for that design conversation;
- **not now** — nothing is dispatched, and the question may return for the
  next design;
- **not in this session** — the question does not return until a new
  session. It is labelled exactly that, because it is honoured for the
  session only: the plugin has no settings store, and writing the
  preference somewhere durable would be a write nobody authorized. A
  developer who wants it permanent puts it in their own instructions,
  which the rule respects when present.

Consent replaces counting offers. There is no fixed checkpoint list and no
warm start; after consent, the judgement of *when* a consultation earns its
cost is the main thread's, exercised the same way it decides to invoke any
skill. That is the whole of the automatic half — no orchestration state, no
briefing ledger, nothing kept alive.

Integration is one addition to `rules/workflow.md`, step 1, phrased
conditionally because payload rules load for people without the plugin.
Two collisions inside that rule have to be fixed in the same edit:

- the rule says "After every architect or plan-adversary round, record the
  verdict … in the reviewed document's `architect:` field". After this
  change "architect" names three components, so read cold the rule
  instructs stamping a consultation. It is tightened to the backticked
  `architect` **agent**, in both that sentence and step 3.
- the model-selection paragraph opens "Model selection for these
  dispatches" and says "Reviews are never dispatched on the cheapest
  available family". A consultation is not a review, so it is named there
  explicitly rather than left to inference — which keeps the tier
  mechanics in the one place that owns them and keeps the step-1 line
  short.

No new rule file is added, so the authoring rule's list of always-on
exceptions is untouched. The added lines do land in `workflow.md`, which is
the payload's only file without `paths:` — so they are resident in every
session on every machine with a user-level install. What this design avoids
is a *second* always-on file, not the cost of a few lines; the earlier
claim of "no addition to the always-on budget" was simply false.

Nothing a consultation produces is a verdict, and nothing is stamped. An
opinion from a consultation may never be carried into the `architect:`
field; only a dispatch of the `architect` agent writes it. Consultations
therefore have no fallback record and no re-review offer.

### 9. Cost

The classical load dimensions do not apply — one developer, one
conversation, no throughput, no concurrency, no bulk path. What remains is
a per-dispatch cost, bounded by construction: a consultation reads the
domain artifacts, the conventions, and what its briefing points at,
answers once, and ends. There is no re-billing across resumptions, no idle
agent, and no cost at all in a design conversation where consent was
declined.

Latency is paid at the moment of dispatch, on the most capable available
model. The consequence worth carrying forward is section 6's "point, don't
paste": what a consultation reads is what it costs.

### 10. Observability

- **Attribution** — a relayed contribution names its persona, and a
  disagreement is visible as one (section 7).
- **Verifiability** — the consult agents declare `background`, so they
  appear in the task panel and the developer can open a transcript and
  read what the persona actually read, rather than trusting the relay.
- **Consent state** — whether consultations are on for this design
  conversation is stated when it is decided and when it changes, so the
  developer is never guessing why a persona did or did not appear.

This design deliberately leaves **no durable record that a consultation
happened**: no frontmatter field, no required body note. That is the price
of cutting the bookkeeping, and it means the effect of the feature cannot
be measured after the fact by comparing specs. An earlier draft claimed it
could; the claim was a wish, not a mechanism, and is withdrawn.

## Non-goals and rejected alternatives

| Rejected | Reason |
|---|---|
| Orchestrating the personas through brainstorming | Built as a draft, then dropped. It required a warm-start spawn, personas kept alive and resumed, a delta-briefing contract, and a record of what each persona had been told — and that record is what a main-thread compaction destroys. The cost and the moving parts outgrew the value. The consent offer of section 8 keeps the benefit of not having to remember, with none of the bookkeeping |
| A designer verdict and a `designer:` field | A third gate in the lifecycle; the designer's output is spec content, which the existing architect gate reviews |
| Persona cross-talk | Opinions converge, and the debate leaves the developer's view |
| Agent teams | Not needed — messaging works without them — and teammate coordination tools override `disallowedTools`, which would break the enforcement in section 5 |
| `memory:` per-persona stores | A competing decision store beside `docs/domain/adr/` and Project memory; it also auto-enables file writes for the agent |
| Fork-based consultation | A fork inherits the conversation and "drops the input isolation" — it solves pollution but not bias, and bias isolation is the reason the surface exists. Its cache advantage is real and named, not hidden |
| Compaction as a persona switch | Summarization keeps conclusions and drops the deliberation that would let them be re-examined, so it does not de-bias. The cost objection is weaker than it first appears — the summarization request shares the conversation's prefix and reads the cache — so this rejection rests on fidelity, not on price |
| One consult persona covering both duties | Both roles in one context return the single reconciled opinion section 5 exists to prevent |
| One session surface for both personas | Weighed for completeness, since the objection above is much weaker in a session: the developer is present, sees the whole exchange, and picks. Rejected because a session skill is selected by trigger phrases, and one skill answering to both personas' phrases makes section 3's lexical arbitration impossible — the surface could no longer tell the developer which persona it is speaking as |
| Reusing the `architect` agent as its own consultation surface | Its report requires a Verdict section, so a consultation would produce a verdict word that cannot be suppressed without editing the agent. An earlier draft also argued the agent "expects a document"; that argument is false — its own definition accepts "any design document or question dispatched standalone" — and is withdrawn. That description phrase does need narrowing, so it stops competing head-on with `architect-consult` |
| A durable record that a consultation happened | Would reintroduce the bookkeeping just cut; the cost is stated in section 10 rather than hidden |
| The `best` model alias | The declarative form of "most capable available", fitting the glossary's tier definition, but absent from the subagent frontmatter table and skippable by an availability policy. Deferred, not dismissed |
| Editing `superpowers:brainstorming` | Another plugin's skill |

## Glossary additions

Settled in the 2026-07-30 grilling-session and already applied to
`docs/domain/glossary.md`:

- **Persona** — a role plus its duties, single-sourced in one
  `*_PERSONA.md` file at the plugin root and adopted by one or more
  persona surfaces. Left unqualified with a disambiguating clause rather
  than becoming "Process persona", the way **Tier** and **Severity**
  already settle their own collisions — `salesforce-security-model` uses
  "persona" for an org user role. The session also corrected the count:
  two personas, not three. `plan-adversary` reads no persona file and
  carries its role inline, so it is a reviewer, not a persona — which
  forced a clause into `PERSONA_COMMON.md`, since its opening claimed
  every carrier of those duties is a persona while this spec has
  `plan-adversary` sourcing them from exactly that file (done).
- **Persona surface** — the component that adopts a persona. Qualified,
  because the repo's own rules already use bare "surface" for a document
  location (`standards-rule-tags.md:19`,
  `working-process/rules/process-artifacts.md:43`). Its `_Avoid_: mode`
  bites six existing lines, all rewritten in the same session: the opening
  line of `agents/architect.md`, `skills/architect-session/SKILL.md` and
  both consult agents, plus the two consult-agent `description:` fields —
  the last mattering most, being the only text a dispatcher reads before
  dispatching.
- **Session skill** — the `*-session` component kind, which reserves
  unqualified "session" for the Claude Code conversation. Section 8's
  consent is scoped to the latter, and that is the one place where
  conflating the two would change behaviour.
- **Consultation** — a verdict-free exchange returning a contribution.
  Sharpened here: the discriminator is the absence of a verdict, not the
  absence of stamping, since an `architect` dispatch on a bare question
  also stamps nothing (`agents/architect.md`: "A bare question has nothing
  to stamp") and still grades.
- **Contribution** — what a consultation returns, relayed attributed and
  substantially verbatim; never graded, never counted.
- **Finding** — widened to two levels instead of staying report-only: the
  core is one graded problem a review round reports with evidence, and the
  counted per-file, single-`rule id` shape is what a Review report
  additionally imposes. `architect` and `plan-adversary` stop being
  undocumented exceptions, and section 7's reservation now rests on a
  term with one meaning. `_Avoid_` narrowed to "as a name for the unit",
  which leaves "one finding per issue" standing in both agents — there the
  two words are contrasted, not substituted.
- **Tier** — verified rather than changed: both uses in this spec are the
  canonical model ladder.

Of the two ADR candidates, one was written —
`docs/domain/adr/0001-persona-independence.md`, for section 5, because
`disallowedTools: SendMessage` on both agents reads as an arbitrary
restriction from the frontmatter alone. The prerelease-grammar widening
was declined an ADR on the grounds that the rule it edits can carry its
own rationale, which turns that sentence into a requirement of the edit
rather than an optional nicety.

## Files to touch

**Plugin, new**: `PERSONA_COMMON.md`, `SYSTEM_DESIGNER_PERSONA.md`,
`agents/architect-consult.md`, `agents/system-designer-consult.md`,
`skills/system-designer-session/SKILL.md`.

**Plugin, edited**: `ARCHITECT_PERSONA.md` (own duty plus a pointer;
boundary moved out); `agents/plan-adversary.md` (standing duties sourced
from the shared file, glossary duty re-tightened, its checklist mechanism
positioned under the domain-expertise duty);
`skills/architect-session/SKILL.md` ("both duties" is stale after the
extraction, the arbitration counterpoint, and the opening line off
"mode" — done); `agents/architect.md` (arbitration counterpoint, the "or
question dispatched standalone" phrase narrowed, glossary duty
re-tightened, and the opening line off "mode" — done); `rules/workflow.md` (the step-1
addition, the two collisions of section 8); `README.md` (components, and
the persona single-sourcing line, both stale); `.claude-plugin/plugin.json`
(description, and the version below).

**Repo**: `.claude/rules/plugin-authoring.md` — the naming convention says
"formal reviews that end in a verdict are agents" and knows no
verdict-free agent, so `*-consult` is added as a third category, or the
rule contradicts the components this change ships.
`.claude/rules/plugin-versioning.md` — the prerelease grammar's `dev`
channel takes the branch short-name as its discriminator when a topic has
no issue number (`0.11.0-dev.design-personas`), and the breaking-surface
list gains the two new persona paths. Widening the discriminator rather
than minting a channel keeps one channel for one purpose, and the rule
already anticipates its own extension: "Future channels extend this list
by editing this rule only — the release-guard workflow rejects every
prerelease on master, so new channels never need a CI change." Because the
grilling declined this decision an ADR on the grounds that the rule can
hold its own rationale, the edit must carry that one sentence inline —
otherwise the "why" survives nowhere.
`.claude-plugin/marketplace.json` and the repo `README.md`, which
enumerate components alongside the plugin description — all three in one
commit per the marketplace-sync rule.

**Version**: `0.11.0-dev.design-personas`. The branch cannot reuse
`0.11.0-dev.10`, which it inherits from develop: the plugin cache keys
content by version and that string is already consumed by the
contract-sharpening topic's dogfooding. Widening the discriminator makes
this branch dogfoodable, which matters because section 3's lexical
arbitration is the one thing in this design that cannot be verified any
other way. The release PR strips the suffix as it does any prerelease.

**Validation**: `claude plugin validate` at the repo root and for the
plugin. Rule frontmatter is reviewed by hand, since validation does not
cover `rules/`.

## Trial evidence

Before this spec was written, both personas were dispatched on the design
itself — briefed identically, with no channel between them, each pointed at
its persona files on disk. They were dispatched again on the spec.

What the trial does and does not establish. It establishes that the
charters hold: the architect named the mechanics dimensions and handed them
over instead of filling them; the designer dismissed the classical load
profile by name and then found the real cost profile behind section 9. It
also establishes the shape of section 4 — self-contained one-shot
consultations, nothing kept alive. It does **not** test the mechanical half
of section 5: the trial dispatched by path, and `disallowedTools` binds
only through the agent file, so the consulting agents did in fact hold
`SendMessage`. And it cannot test section 3's arbitration at all, which is
selection behaviour, not persona behaviour.

The consultations changed the design rather than ratifying it. From the
first round: the briefing and reporting contracts (sections 6 and 7), which
had been named but not specified, and a withdrawn false argument. From the
second: that the briefing contract had no owner and would not ship with the
plugin; that `background` could be declared rather than assumed; that the
"measure the outcome" claim was a wish; that "standalone install" has a
glossary meaning which made the earlier degradation path empty; that
"Mode" collides with existing canon; that the always-on budget claim
contradicted itself; that `workflow.md` already instructs stamping a
consultation; and that the stated reason for skipping dogfooding was
factually wrong.

Both rounds converged independently on the same three things, which is the
strongest evidence available that the two charters are not one charter
twice: the undefined briefing contract, the relaying thread as the
unguarded convergence point, and the weakness of a symmetry-only session
skill.

## Architect findings — 2026-07-30 round 1

Dispatched on Fable 5 (self-reported: fable 5; prescribed tier). Verdict:
concerns — one Important, five Minor. All resolved the same day; details
below, verdict annotated in frontmatter.

- **Important**: the consultation contract was routed into
  `PERSONA_COMMON.md` with no scoping — the file's verdict-bearing
  consumers (`plan-adversary` directly, `architect` transitively) would
  read "contributions are never graded" against their own verdict duty,
  and only the boundary section had a carve-out. → Fixed: §2 now specifies
  a scoping clause on the contract section (binds `*-consult` dispatches
  and their dispatcher only) and the rework of the file's "All three are
  defined only here" opening when the fourth section lands.
- **Minor**: "read by all three personas" contradicted the settled count
  (two personas; `plan-adversary` is a reviewer). → Fixed: "by both
  personas and by `plan-adversary`".
- **Minor**: "process persona" re-introduced the qualified form the
  grilling declined, in §5 and both consult-agent bodies. → Fixed in all
  three: "working-process persona".
- **Minor**: §7's reservation argument was stale after the same grilling
  ("the counted unit of a Review report" — Finding is two-level now). →
  Fixed: "the graded unit of a verdict-bearing review round".
- **Minor**: §6 said a singular "operative sentence" goes into the
  `description` fields without naming it, and the trial descriptions
  carried none of it — the only dispatcher-readable surface. → Fixed: §6
  now quotes the exact sentence (the two cross-dispatch invariants), and
  both trial descriptions carry it.
- **Minor**: "stays on the designer's own surface" misused the fresh
  Persona-surface term for what is a persona file. → Fixed: "in the
  designer's own persona file".

## Accepted risks

- **`disallowedTools` has no documented minimum version, and the failure
  mode is silent either way.** If an unrecognized key is ignored, the
  agent still loads and the mechanical half of section 5 becomes a no-op
  with nothing reporting it; if it prevents the agent from loading, the
  surface disappears from selection and the arbitration of section 3
  silently degrades to the session skill. Which of the two happens is
  undocumented for agent files. The substantive half — the briefing rule —
  does not depend on the key. Worth one empirical check on the oldest
  floor available.
- **Selection quality among four dispatchable agents is unverified.** After
  this change the plugin ships `architect`, `architect-consult`,
  `plan-adversary`, and `system-designer-consult`, with overlapping
  description surfaces. The trigger phrases and counterpoints of section 3
  are the mitigation; dogfooding under the new version string is how it
  gets checked before release.
- **The arbitration rule is guidance, not enforcement.** Nothing prevents a
  session skill from being invoked where a consult agent was the better
  choice. With trigger phrases in place this is no longer a systematic
  bias toward one surface, but it remains a judgement the descriptions can
  only inform.
- **`plan-adversary` gains a duty.** Declared in Scope rather than
  discovered later, and believed to be an improvement — but it is a
  behaviour change to a verdict-bearing gate, shipped in a change whose
  headline is a new persona.

## Amendment — 2026-07-30: domain artifacts resolve from the repo root

Found by the first dogfooding dispatch of `system-designer-consult`, on
itself: the glossary/ADR duty named its artifacts by relative path, so a
dispatch from a session whose working directory sits below the repo root
would conclude in good faith that no glossary exists — a silent
degradation of exactly the shape the Accepted risks list carries, but
unlisted. The consultation demonstrated it empirically (its own
environment started in a subdirectory) and proposed the fix applied
here: the shared glossary duty now resolves `docs/domain/` against the
repo root (`git rev-parse --show-toplevel`), all four agents defer to
that clause, and the briefing contract gains a bullet obliging the
dispatcher to name where the subject lives. Residual: a subject outside
any git repository still depends on that briefing line. The same
consultation also surfaced the consent state's unspecified lifecycle
across compaction; `rules/workflow.md` now says to re-ask when a
compacted conversation leaves it unclear.
