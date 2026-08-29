---
ticket: none
date: 2026-08-27
status: implemented
adversary: blocking (adjudicated 2026-08-29)
branch: feature/review-loop-audits
base: develop
spec: [../specs/2026-08-17-autonomous-review-loop-design.md, ../specs/2026-08-27-audit-agents-design.md]
---

# Review Loop and Audit Agents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship both grilled-and-reviewed specs — the autonomous review
loop (`architect: concerns (resolved 2026-08-27)`) and the two audit
agents (`architect: LGTM`) — as one working-process release.

**Architecture:** Two new agents (`propagation-auditor`,
`integrity-auditor`) join the plugin's agent set; the workflow rule's
dispatcher section gains the autonomous loop and the audit offers; the
lifecycle rule gains the disposition-ledger grammar, its Unfinished-work
entry, the `integrity:` field, and the mirrored relay-then-stamp
exception; `ARCHITECT_PERSONA.md` narrows. Both specs' Changes-by-file
sections are the authority — every task below names its spec section,
and the implementer writes rule prose from the spec, never from this
plan's summaries. No code: every deliverable is Markdown rule text,
agent content, or manifest prose.

**Tech Stack:** Claude Code plugin content (Markdown rules and agents,
YAML frontmatter), `rg`, `claude plugin validate`, git.

## Global Constraints

- Public repo: English only, no machine paths, no client names
  (repo-hygiene rule).
- Commits: one-line conventional-commit subject, no body, no trailers
  (commit-messages rule + the developer's global instruction).
- Frontmatter safety: quote any `description:` containing `: ` —
  `claude plugin validate` does NOT check `rules/` frontmatter, so
  review rule frontmatter by hand (plugin-authoring rule).
- Both validations pass before every commit:
  `claude plugin validate .` and
  `claude plugin validate plugins/working-process`.
- Glossary bans bind all shipped text: never `reviewer agent` /
  unqualified `review agent`, never `sweep agent`, never `verifier`,
  never `retire` as a closure verb; the two agents are **Audit
  agents**, their mechanical unit is a **hit** (`docs/domain/glossary.md`).
- Cross-plugin and cross-component mentions in rule text stay
  conditional ("when available") — rules load for people without the
  plugin (plugin-authoring rule, Rules payload section).
- Version: this topic dogfoods working-process, so it sets
  `0.14.0-dev.review-loop-audits` on the plugin (plugin-versioning
  rule); the release PR strips the suffix later. Never bump the release
  number on the topic branch.
- Executor audit: every task below is runnable by an implementer agent
  (file edits, `rg`, `claude plugin validate`, headless `claude -p`
  dispatches). The developer steps are the plan-approval status flip
  before execution (Task 1 Step 0), the final-gate review (Task 9
  Step 4), and Task 9's three conditional contacts — the mismatch STOP
  in Step 1, a contested propagation hit and decision-shaped integrity
  defects in Step 3; each carries an explicit STOP.

---

### Task 1: Topic branch and dogfood version

**Files:**
- Modify: `plugins/working-process/.claude-plugin/plugin.json` (the
  `version` field; currently `0.14.0-dev.process-status-riders`)
- Commit (already written, uncommitted at the gate): both specs, this
  plan, and `docs/domain/glossary.md` — the grilling's Audit agent and
  Hit entries plus the Misplaced-stamp field list gaining `integrity`.

**Interfaces:**
- Produces: branch `feature/review-loop-audits` off `develop`; version
  string `0.14.0-dev.review-loop-audits`; the process documents in the
  branch's history, so the rules and agents Tasks 2–8 write never cite
  glossary terms absent from the branch.

- [ ] **Step 0: STOP — approval gate**

Confirm the plan's frontmatter reads `status: approved` (the
developer's flip) AND that its `adversary:` field reads LGTM or
carries a closing annotation — the pair the Task 9 verdict sweep's
precondition relies on. Either check failing → stop; nothing below
runs.

- [ ] **Step 1: Create the branch**

```bash
git checkout develop && git checkout -b feature/review-loop-audits
```

- [ ] **Step 2: Set the dogfood discriminator**

In `plugins/working-process/.claude-plugin/plugin.json` set
`"version": "0.14.0-dev.review-loop-audits"` — same 0.14.0 line (it has
not released), new discriminator per the plugin-versioning rule's
one-channel-one-purpose clause.

- [ ] **Step 3: Validate**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass.

- [ ] **Step 4: Commit the version re-mint**

```bash
git add plugins/working-process/.claude-plugin/plugin.json
git commit -m "chore(working-process): start review-loop-audits topic, re-mint dev version"
```

- [ ] **Step 5: Commit the process documents**

The implementation-ready gate the lifecycle rule names — the plan is
approved and implementation starts now, so the work's `docs/`
artifacts enter the branch. The glossary is not optional here: Tasks
2–8 write rule and agent text citing Audit agent, Hit and the
`integrity` field, and those definitions live only in the working tree
until this commit.

```bash
git add docs/specs/2026-08-17-autonomous-review-loop-design.md \
        docs/specs/2026-08-27-audit-agents-design.md \
        docs/plans/2026-08-27-review-loop-and-audit-agents.md \
        docs/domain/glossary.md
git commit -m "docs: review-loop and audit-agents specs, plan and glossary entries"
```

---

### Task 2: `propagation-auditor` agent

**Files:**
- Create: `plugins/working-process/agents/propagation-auditor.md`
- Read first: `docs/specs/2026-08-27-audit-agents-design.md`
  (§The category, §propagation-auditor), `docs/domain/glossary.md`
  (Audit agent, Hit, Tier), an existing agent file for frontmatter
  shape (`plugins/working-process/agents/plan-adversary.md`).

**Interfaces:**
- Produces: the agent name `propagation-auditor` (Task 6's offers and
  Task 5's grammar cite it); the report contract — opens with a model
  self-report (family plus version), then hits each with location and
  derivation, or the single line `CLEAN`.

- [ ] **Step 1: Write the agent file**

Content requirements, all from spec §propagation-auditor (the spec text
is the authority — write from it, not from this list):

- Frontmatter: `name: propagation-auditor`; `description:` states the
  triggering contract — a mechanical, verdict-free audit gating
  expensive dispatches, returning hits, dispatched on the cheapest
  available family — quoted (it contains `: `); and
  `background: true`, per the spec and like every agent this plugin
  ships.
- Role inline (the plan-adversary pattern), no persona file, and a
  standing line that the agent adopts no persona and returns no
  verdict.
- The seven duties, each phrased domain-neutrally with the marketplace
  instantiation beside it, exactly as the spec lists them (interface →
  consumer enumeration by parsing; prescribed block vs shipped file;
  carrier and consumer chains; counters re-derived; cross-document
  identifier diff reported as a spec gap; boundary sentences;
  verification simulation).
- Output contract: the opening model self-report, then hits
  (location + one-line claim + derivation) or `CLEAN`; hits are never
  graded; severity words never appear.
- The glossary duty, so the plugin README's "Every component reads
  `docs/domain/glossary.md` and `docs/domain/adr/` first" stays true of
  the component set: duties 1 and 5 are where `_Avoid_` bans bite, and
  the release's own constraint is that glossary bans bind all shipped
  text. An audit agent adopts no persona, so the duty is stated in the
  agent body rather than inherited from `PERSONA_COMMON.md`.

- [ ] **Step 2: Validate and hand-check frontmatter quoting**

Run: `claude plugin validate plugins/working-process`
Expected: pass. Then visually confirm the `description:` scalar is
quoted.

- [ ] **Step 3: Commit**

```bash
git add plugins/working-process/agents/propagation-auditor.md
git commit -m "feat(working-process): add propagation-auditor audit agent"
```

---

### Task 3: `integrity-auditor` agent

**Files:**
- Create: `plugins/working-process/agents/integrity-auditor.md`
- Read first: `docs/specs/2026-08-27-audit-agents-design.md`
  (§integrity-auditor, §The paired edit), `docs/domain/glossary.md`,
  and `plugins/working-process/agents/plan-adversary.md` for
  frontmatter shape.

**Interfaces:**
- Produces: the agent name `integrity-auditor` and the run name
  "integrity audit" (Tasks 5–6 cite both); the report contract — opens
  with the model self-report, then defects each proved by two quotes,
  a separate section of ranked implementer questions, and the coverage
  tell (target line count + highest line cited). The agent never
  writes the `integrity:` stamp — the dispatcher does.

- [ ] **Step 1: Write the agent file**

Content requirements, all from spec §integrity-auditor:

- Frontmatter: `name: integrity-auditor`; `description:` — the
  judgment pass over a churned document on a fresh context, verdict-free,
  most capable available tier, primarily a spec before plan-writing —
  quoted; and `background: true`, per the spec.
- Role inline; fresh context stated as the mechanism (never inherit
  the editing session), with the preconditions: every conversation
  edit on disk, and a clean propagation audit when that agent is
  available (conditional mention).
- The two lenses verbatim in intent: document-against-itself
  (including verifying every rule the document declares about itself,
  in both directions) and sufficiency-for-an-implementer (ranked
  questions; a good question outranks a weak finding).
- Output contract: self-report, defects-with-two-quotes, ranked
  questions, coverage tell. No verdict, no severities, no stamp.
- The glossary duty, stated in the agent body for the same reason as
  the propagation-auditor's: an audit agent adopts no persona, so it
  inherits nothing from `PERSONA_COMMON.md`, and the plugin README
  claims the whole component set reads the glossary first.

- [ ] **Step 2: Validate and hand-check frontmatter quoting**

Run: `claude plugin validate plugins/working-process`
Expected: pass. Then visually confirm the `description:` scalar is
quoted — validate does not catch an unquoted `: `.

- [ ] **Step 3: Commit**

```bash
git add plugins/working-process/agents/integrity-auditor.md
git commit -m "feat(working-process): add integrity-auditor audit agent"
```

---

### Task 4: Narrow the architect's card

**Files:**
- Modify: `plugins/working-process/ARCHITECT_PERSONA.md` (the duties
  list; the Fit duty is the "nothing missing, nothing extra" bullet)
- Read first: `docs/specs/2026-08-27-audit-agents-design.md`
  (§The paired edit).

**Interfaces:**
- Produces: the narrowing sentence Task 8's README row summarizes.

- [ ] **Step 1: Add the narrowing**

One addition to the duties section, written from the spec: when a
round trips over integrity-class textual defects (contradictions,
counts-versus-lists, reference drift), the architect notes them in one
line and defers to the integrity audit rather than enumerating them.
A conditional clause ("when that agent is available") is the
implementer's call, with the honest rationale: a round may run where
dispatching another agent is impossible — not a shipping requirement;
the persona and the auditor travel in one plugin.

- [ ] **Step 2: Validate and commit**

Run: `claude plugin validate plugins/working-process` — pass, then:

```bash
git add plugins/working-process/ARCHITECT_PERSONA.md
git commit -m "feat(working-process): narrow architect card, integrity class defers to the audit"
```

---

### Task 5: Lifecycle rule and process-status — grammar, anchors, stamps

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` —
  five sites: the frontmatter field-set example block, the
  resolved-concerns annotation bullet (where `blocking (adjudicated
  <date>)` lands), the `## Unfinished-work list` section, the
  `## Lifecycle offers` consumption-gate sentence (the backstop for
  open `held` lines), and a new disposition-ledger section. NOT the relay-then-stamp sentence in `## Lifecycle
  offers` — that
  lands in Task 6's pair commit.
- Modify: `plugins/working-process/skills/process-status/SKILL.md` —
  the hit-confirmation step (Step 3).
- Read first: the loop spec's lifecycle bullet (the master list),
  §The disposition ledger, and its Changes-by-file process-status
  bullet; the audit spec's §The stamp.

**Interfaces:**
- Consumes: agent names from Tasks 2–3 (the `[hit]` variant cites the
  propagation-auditor).
- Produces: the canonical grammar Task 6's workflow clauses cite and
  Task 9 greps — section `## Review rounds`; heading
  `### <ISO date> — <agent>, <model self-report>, <verdict> (round N[, <scope>])`
  with its two admitted values, `diff-scoped` and `full-document`;
  lines `- fixed — [<severity>] <claim>; license: <citation>; <what changed>`,
  `- held — [<severity>] <claim>; question: <one short question>`,
  `- open — [<severity>] <claim>`,
  `- resolved <date> — [<severity>] <claim>; landed in <section>`,
  `- resolved <date> (declined) — [<severity>] <claim>; <why the document stands>`;
  the `[hit]` severity-slot variant; the `, chain accepted <date>`
  heading annotation; the command
  `rg -n --no-ignore --crlf '^- (open|held) —' docs/`; the
  `integrity:` field definition; and its canonical hash recipe,
  `sed '1,/^---$/d' <file> | shasum | cut -c1-7` — a dictated token
  like the grammar shapes, so Task 9 Step 1's character-for-character
  check covers its absence.

- [ ] **Step 1: Add the disposition-ledger grammar**

A new section written from the loop spec's §The disposition ledger:
the four tokens with their semantics and license citation, the
canonical record shapes above (verbatim — they are interface, not
prose), the `[hit]` variant, the `, chain accepted <date>` annotation
and its writer (the dispatcher, at the gate, on the developer's
decline — its presence defeats the gate's re-ask).

- [ ] **Step 2: Add the Unfinished-work entry**

One entry, from the loop spec: class "unfinished review-loop ledger",
the hardened command above, owner text naming both owners (an `open`
line → the document's next touch; a `held` line → the developer), and
the explicit re-scoping sentence: this entry's hits count inside a
`## Review rounds` section, an explicit exception to the list's
frontmatter guard, kept for the same quoting reason.

- [ ] **Step 3: Add the close forms and gates**

From the loop spec: `blocking (adjudicated <date>)` beside the
existing annotations (the tail-anchor sentence after the list already
names it — confirm consistency, do not duplicate); the
consumption-gate backstop for open `held` lines including the
spec→plan seam.

- [ ] **Step 4: Add the `integrity:` field**

From the audit spec §The stamp: the field joins the frontmatter set —
value `integrity: <ISO date> (sha: <short-hash>)`, the hash produced
by the canonical recipe shipped VERBATIM into this rule as the command
both the stamper and the consumption gate run:
`sed '1,/^---$/d' <file> | shasum | cut -c1-7` (portable — stock macOS
ships no `sha1sum`; the spec records that both tools yield identical
digests). Without the command in the shipped text, two sessions can
digest by different conventions and the gate reports "unaudited"
against a valid stamp. Recomputation owned by the consumption gate (spec-gate semantics; a plan's stamp is
informational and goes stale silently); the Misplaced-stamp detecting
entry's field alternation gains `integrity`. Do NOT touch
the verdict-agent self-report sentence — audit-agent tier verification lives
in the workflow rule (Task 6 Step 3), and attaching round-record
language to verdict-free audits would blur the glossary's
Verdict-agent/Audit-agent boundary.

- [ ] **Step 5: Extend process-status hit confirmation**

From the loop spec's process-status bullet: Step 1 of
`skills/process-status/SKILL.md` currently collects three legs per
entry (class, command, owner) — it gains an optional fourth, the
entry's own match scope, read when present; Step 3 then takes that
scope when the entry re-scopes it (the ledger entry's `## Review
rounds` sections); the frontmatter guard stays the default for every
entry publishing no scope of its own. Decide the neighbouring clause
too, rather than leaving it to first use: the skill's
reject-every-hit-in-a-file-without-a-frontmatter-block rule is a
FILE-LEVEL invariant that survives re-scoping — a process document
always has frontmatter, and a file lacking one is not a process
document — so a re-scoped entry narrows where a hit counts, never
whether the file qualifies.

- [ ] **Step 6: Validate and commit**

`claude plugin validate plugins/working-process` — pass, then:

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md plugins/working-process/skills/process-status/SKILL.md
git commit -m "feat(working-process): disposition ledger, integrity stamp and ledger-scoped hit confirmation"
```

---

### Task 6: Workflow rule — the loop, the audit offers, the exception pair

**Files:**
- Modify: `plugins/working-process/rules/workflow.md` — three sites:
  the numbered flow (the audit offers land around steps 3–5), the
  model-selection paragraph ("Reviews are never dispatched on the
  cheapest available family"), the verdict-agent
  dispatch subsection (`## Dispatching a verdict agent` to the end of
  the file, whose one-turn order is the "in one turn and in this
  order" bullet) — a range whose closing co-edit clause Step 4 verifies
  rather than edits.
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md` —
  ONLY the relay-then-stamp sentence in `## Lifecycle offers`: the pair's
  edited-together declaration binds the commit, so both rules'
  exception sentences land here, together.
- Read first: BOTH specs' Changes-by-file `workflow.md` bullets — the
  loop spec's bullet is the master list for this task; the audit spec's
  bullet adds the two offers and the tier sentences.

**Interfaces:**
- Consumes: agent names from Tasks 2–3; the canonical grammar tokens
  and the `integrity:` field semantics from Task 5 (the loop clauses
  cite `, chain accepted <date>`, diff-scoped headings, and the
  ledger-read recovery — all defined there).
- Produces: the loop's dispatcher clauses and the exact offer sentences
  Task 8's README summarizes; the relay-then-stamp exception, in both
  rules of the co-edited pair, one commit.

- [ ] **Step 1: Write the loop into the dispatch subsection**

From the loop spec's workflow bullet, in the dispatch subsection: the
consent question (once per session, yes / not now / not in this
session), the license test with its held-by-default rule, yield-on-held
and the one-batch shape, the re-dispatch brief duties (diff-scoping
with the forbidden-rest clause, terminators stated up front, the
reviewer's stop signal, invited refutation), the propagation gate
(conditional: "when the propagation-auditor is available") — stated
HERE as the canonical definition, since the dispatcher reads this
subsection at dispatch time, and carrying the FULL dispatch-point set
the audit spec settles, not just the loop's own: before every
verdict-agent dispatch, first rounds included (authoring errors exist
before any repair); after a fix wave, before the next round; and
before an integrity audit. Step 2's flow entry points at this
definition rather than restating it, so Task 9 Step 1 checks one
statement instead of two — the round
cap of three, the all-Minor signal, the oscillation tripwire,
blocking-suspends-autonomy, and relay as the standing veto — plus the
consumption-gate pair offer for a spec whose LGTM came from a
diff-scoped chain (audit or confirming round; auditor absent → the
confirming round alone; decline recorded as `, chain accepted <date>`)
and the plan-side recovery re-offer (a plan whose latest round heading
is a diff-scoped LGTM with no later full-document round is re-offered
its confirming round at the document's next touch). The
relay-then-stamp exception is written in Step 4, not here.

- [ ] **Step 2: Write the two audit offers**

From the audit spec's workflow bullet, into the numbered flow: the
integrity audit offered at the consumption gate before plan-writing —
the flow entry names the offer and points at Step 1's definition of
the reshaped pair form and its auditor-absent narrowing, never
restating that scope, exactly as the propagation half does; the
propagation
audit, whose gate the dispatch subsection defines (Step 1) — the flow
entry names the offer and points at that definition rather than
restating its scope, so the rule states the gate once. One propagation
dispatch point lies OUTSIDE the loop and therefore outside that
definition: the authoring-time offer after any multi-site edit. It
lands in the numbered flow as its own clause, since no loop-internal
definition can carry it. Both audits
are background dispatches, so state the sequencing the spec settles:
the gated dispatch waits for its audit's task notification before it
is issued — a sequencing rule, not a blocking call, reusing the relay
machinery the subsection already defines.

- [ ] **Step 3: Add the audit tier sentences**

In the model-selection paragraph, from the audit spec: audits are not
reviews — the propagation-auditor dispatches on the cheapest available
family and the integrity-auditor on the most capable available, both
named explicitly; both reports open with a model self-report the
dispatcher compares (dispatched and prescribed rung) before relying on
the result — a mismatched propagation run earns no reliance, a
below-tier integrity run gets no stamp.

- [ ] **Step 4: Land the relay-then-stamp exception in BOTH rules**

One edit wave, this task's commit: the exception sentence (a plan's
diff-scoped LGTM relays and writes its round record; only the
frontmatter stamp waits for the confirming full-document round) goes
into the workflow rule's dispatch subsection AND the lifecycle rule's
relay-then-stamp sentence in `## Lifecycle offers`, and the workflow
rule's closing co-edit clause still declares the pair edited together. The
pair's own declaration is why both files share this commit.

- [ ] **Step 5: Validate and commit**

`claude plugin validate plugins/working-process` — pass, then:

```bash
git add plugins/working-process/rules/workflow.md plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): review loop, audit offers and the relay-exception pair"
```

---

### Task 7: Repo authoring rule — the `*-auditor` naming line

**Files:**
- Modify: `.claude/rules/plugin-authoring.md` (the naming bullet
  listing `*-session`, verdict agents, `*-consult`)

**Interfaces:**
- Produces: the naming convention Task 8's README row relies on.

- [ ] **Step 1: Add the line**

Extend the naming bullet: a verdict-free audit agent returning
material for disposition is named `*-auditor`.

- [ ] **Step 2: Validate and commit**

Run: `claude plugin validate .`
Expected: pass — the constraint binds every commit, this one included.

```bash
git add .claude/rules/plugin-authoring.md
git commit -m "docs: add *-auditor to the component naming conventions"
```

---

### Task 8: Identity surfaces

**Files:**
- Modify: `plugins/working-process/README.md` (the agents section —
  two new rows after the `plan-adversary` row, the model-selection
  paragraph, the "Frontmatter process fields" table, the process-status
  row, the architect row, the flow line at the top — the release
  inserts the integrity audit before plan-writing and the propagation
  audit before verdict dispatches — and the re-sync paragraph — the audit offers
  and the `integrity` gate also live in the Rules payload, so they too
  await a rules re-sync after a plugin update), the root `README.md`
  plugin table row
  for working-process (it enumerates the agent set),
  `plugins/working-process/.claude-plugin/plugin.json` `description`,
  and the `.claude-plugin/marketplace.json` catalog entry — the
  marketplace-sync rule binds all identity surfaces in the same
  commit, and every one of them enumerates components today.

**Interfaces:**
- Consumes: agent names and offer sentences from Tasks 2–6, and the
  `*-auditor` naming line from Task 7.

- [ ] **Step 1: README rows and the fields table**

Two agent rows in the shipped style: what each auditor is, its tier,
its output unit, when the workflow offers it; the model-selection
paragraph gains the audit-tier sentence (cheapest for propagation,
most capable for integrity — audits are not reviews); the
"Frontmatter process fields" table gains an `integrity` row (the
date-plus-body-hash value, dispatcher-written, gate-recomputed); the
process-status row's class enumeration extends to the
unfinished review-loop ledger class and its section-scoped hits; the
architect agent's row gains the narrowing Task 4 ships —
integrity-class defects are noted and deferred, not enumerated.

- [ ] **Step 2: Sync the other three surfaces**

Update the root `README.md` working-process row, the plugin.json
`description`, and the catalog entry to the same component
enumeration. Then confirm:

Run: `rg -n 'audit' plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json plugins/working-process/README.md README.md`
Expected: all four surfaces name the two audit agents consistently.

- [ ] **Step 3: Validate and commit**

`claude plugin validate .` — pass, then:

```bash
git add plugins/working-process/README.md README.md plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json
git commit -m "docs(working-process): identity surfaces for the audit agents and the integrity field"
```

---

### Task 9: Closing gate — recipe-and-record diff and sweeps

**Files:**
- Read: every file Tasks 2–8 touched, against both specs.
- Modify: `docs/specs/2026-08-17-autonomous-review-loop-design.md`
  (the integrity dispositions, the `integrity:` stamp, the
  audit-outcome note), `docs/specs/2026-08-27-audit-agents-design.md`
  (propagation-hit fixes, if any), and any shipped file a
  fix-shipped-text resolution touches at Step 1's or item 3's STOP.

- [ ] **Step 1: Spec-vs-shipped diff (STOP on mismatch)**

For each Changes-by-file bullet in BOTH specs, confirm the shipped
file carries it; for every interface token this plan dictates
(the grammar shapes, the heading token, the annotation, the command,
the field value shape) confirm the shipped text matches CHARACTER
FOR CHARACTER. Any mismatch: STOP and put the fix-shipped-text-or-
return-to-spec decision to the developer — never reconcile silently.

- [ ] **Step 2: Mechanical sweeps, output quoted**

The ban sweep covers exactly the files this release creates or edits —
six pre-existing `reviewer agent`/`code-reviewer agent` hits live in
untouched standards plugins and the review-reports rule, and they are
out of this release's scope:

```bash
rg -in 'sweep agent|verifier|review agent|reviewer agent|\bretire' \
  plugins/working-process/agents/propagation-auditor.md \
  plugins/working-process/agents/integrity-auditor.md \
  plugins/working-process/rules/workflow.md \
  plugins/working-process/rules/spec-plan-lifecycle.md \
  plugins/working-process/skills/process-status/SKILL.md \
  plugins/working-process/ARCHITECT_PERSONA.md \
  plugins/working-process/README.md README.md \
  plugins/working-process/.claude-plugin/plugin.json \
  .claude-plugin/marketplace.json \
  docs/domain/glossary.md \
  docs/specs/2026-08-17-autonomous-review-loop-design.md \
  docs/specs/2026-08-27-audit-agents-design.md \
  .claude/rules/plugin-authoring.md
rg -n --no-ignore --crlf '^- (open|held) —' docs/
rg -l --no-ignore --crlf '^\s*(architect|adversary): (blocking|concerns)$' docs/
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: exactly four hits, all definitional or mention-position,
verified on the tree at plan time — the glossary's three `_Avoid_`
lines (Audit agent, Verdict agent, Close-an-entry), which are where
the bans are DEFINED and therefore match by construction, plus the
audit spec's Naming section mentioning `sweep-verifier`, the rejected
working name's recorded trail. Quote all four and judge them per the
glossary ban, like the plan's own exclusion; qualified forms (e.g.
"code-review agent" inside a longer name) are judged the same way. A
fifth hit fails the sweep.
This plan file itself stays off the sweep list deliberately: it names
the banned terms in mention position (the Global Constraints list and
these round records). The ledger sweep returns nothing. The verdict
sweep's precondition is this plan's own `adversary:` field being
LGTM or annotation-closed by execution time — the Task 1 Step 0
approval gate guarantees it — so it too returns nothing; a hit on
this plan here is a STOP, never an expected exception. Validations
pass.

- [ ] **Step 3: Dogfood both auditors on the bundle's own documents**

Per the audit spec's Verification section, on the dogfood version.
The session's own agent registry predates these agents, so every
dispatch here runs as a FRESH headless session (developer directive,
2026-08-27) — which also satisfies the integrity-auditor's
fresh-context requirement by construction:

```bash
claude plugin disable working-process   # name-collision guard; see the re-enable rule below
claude -p --plugin-dir plugins/working-process --agent propagation-auditor \
  --model <cheapest-available-family> "<target: the loop spec>"
claude -p --plugin-dir plugins/working-process --agent propagation-auditor \
  --model <cheapest-available-family> "<target: the audit spec>"
claude -p --plugin-dir plugins/working-process --agent integrity-auditor \
  --model <most-capable-available> "<target: the loop spec>"
claude plugin enable working-process
```

One discipline binds EVERY disable window in this task, so no step
restates it: re-enable the installed plugin and delete any fixture
before pausing at a STOP, on any dispatch failure, and on any unmet
Expected — every exit path restores the developer's live install and
leaves no scratch file behind.

`--agent` is what distinguishes the agent running from the session
improvising: without it a headless run performs the audit inline, the
self-report still matches and `CLEAN` is still emitted on request,
while the agent's duties, output contract and coverage tell go
unexercised. Before relying on any report, quote one agent-sourced
marker from it — a hit's `location + claim + derivation` triple, or
the integrity report's line-count coverage tell.

Both `--model` values resolve at dispatch time — the executor names
the family then (the glossary's Tier entry: a rung is never a concrete
model name at authoring time), and an omitted `--model` is forbidden:
it inherits the session default, the exact anti-pattern the shipped
workflow rule names. 

One guard covers the whole sequence: ANY spec edit made anywhere in
Step 3 — item 1's propagation fixes included — un-certifies what it
touched, so before the sequence proceeds it re-runs Step 2's ban-sweep
command UNCHANGED (its file list already carries both specs, so the
four-hit baseline and the Expected hold literally) and Step 1's
spec-vs-shipped diff over the touched sections.

Sequence, honoring the contract this run demonstrates:

1. Propagation audit over BOTH specs (cheapest available family,
   named at dispatch) — the audit spec's Verification says both, and
   a clean line on the loop spec is the integrity audit's own
   precondition. Before relying on any report, compare its opening
   model self-report against the dispatched and prescribed rung —
   a mismatch earns no reliance and re-dispatches. Then dispose of
   every hit: a confirmed hit is fixed, a contested one escalates to
   the developer as a third conditional STOP (never silently
   dismissed, per the audit spec). The terminal condition is NO
   CONFIRMED HITS REMAIN on either spec — not the literal `CLEAN`
   token, which a dismissed hit would keep out of reach forever. Two
   re-dispatches per spec; a third escalates instead of looping.
2. Integrity audit over the loop spec (most capable available, named
   at dispatch, fresh headless session). Compare its self-report
   before anything else — a below-tier run gets no stamp and is
   re-dispatched. Relay the report. Defects return to the dispatcher
   for disposition (the audit spec's contract); a decision-shaped
   defect is a conditional STOP — re-enable the plugin, the developer
   decides, everything else is applied directly.
3. Apply the dispositions, then RE-RUN Step 1's spec-vs-shipped diff
   over every spec section the fixes and dispositions touched — the
   same character-for-character bar, the same developer STOP on
   mismatch; an edit made after certification un-certifies what it
   touched. A mismatch resolved by editing the LOOP SPEC re-enters
   item 1 for that spec — propagation audit over the edited text to
   `CLEAN` — and then item 2, a fresh integrity dispatch, before any
   stamp; the integrity audit's propagation precondition holds on
   every pass, not only the first. A mismatch resolved by editing the
   AUDIT SPEC re-enters item 1 for that spec (propagation to `CLEAN`);
   no item-2 re-entry — the integrity target is the loop spec alone.
   The developer may
   explicitly waive the re-audit at that STOP, the waiver quoted in
   the Step 4 relay — and a waiver forfeits BOTH items 4 and 5: no
   stamp is written over text no audit read, the forfeiture is named
   in the Step 4 relay beside the quoted waiver, and the audit spec's
   stamp-and-re-arm verification stays owed, the developer its owner.
   A fix-shipped-text resolution proceeds unchanged. The stamp
   answers "was this checked after the last edit" and must never
   answer it falsely.
4. Stamp `integrity: <ISO date> (sha: <short-hash>)` into the loop
   spec — the hash computed by the audit spec's canonical recipe,
   `sed '1,/^---$/d' <file> | shasum | cut -c1-7`, the same command
   the consumption gate recomputes with. Quote the command and its
   output.
5. Observe the re-arm with a real, labeled edit: append the
   audit-outcome note to the loop spec's body (one sentence naming
   the run, its date, and its disposition count), recompute the body
   hash, observe the mismatch against the stamp — and STOP THERE.
   The re-armed (stale) stamp is the deliberate final state, named as
   such in the Step 4 relay: per the audit spec, a differing hash
   means "unaudited, exactly", and writing a fresh stamp over text no
   audit read is the false answer this sequence exists to forbid.
   Quote the stamped hash and the recomputed hash, so the mismatch is
   visible.

- [ ] **Step 3a: Exercise the changed process-status skill**

Task 5 changes the skill's own logic (an optional fourth leg in Step 1,
section-scoped confirmation in Step 3); a raw `rg` verifies the
command, not the skill. The run needs its own disable window (the installed copy is enabled
again by the end of Step 3, and the harness resolves a name collision
silently) and a fixture (the ledger sweep returns nothing on a clean
tree, so the changed confirmation branch would never execute):

```bash
claude plugin disable working-process
# fixture: a throwaway docs/ file WITH a valid frontmatter block (the
# skill rejects every hit in a file without one), carrying one
# `- held — [Important] …; question: …` line inside a
# `## Review rounds` section and one outside any section
claude -p --plugin-dir plugins/working-process "/process-status"
claude plugin enable working-process
```

This step produces EVIDENCE, not a pass/fail gate — quote the report
and let the developer read it at the Step 4 STOP. Quote three things:
the in-section line reported as a hit of the unfinished review-loop
ledger class with both owners named; the out-of-section line rejected;
and the two closers the skill's own final step mandates (the
rejected-hit count with its documents, and the explicit
every-class-name-checked statement) — which only the skill can
produce, so they show it ran rather than the session improvising.

- [ ] **Step 3b: Commit the gate's output**

The stamp and the audit-outcome note are this release's named
verification deliverable, and the process-artifacts rule forbids
leaving tracked artifacts dirty — so the developer's Step 4 review
starts from a clean tree.

```bash
git add docs/specs/2026-08-17-autonomous-review-loop-design.md \
        docs/specs/2026-08-27-audit-agents-design.md
git commit -m "docs: dogfood audit results, integrity stamp and re-arm evidence"
```

Any shipped file a STOP resolution touched joins this commit (or its
own, with a subject naming the fix).

- [ ] **Step 4: STOP — developer review**

Relay the diff results, sweep outputs, and both audit reports to the
developer. Three `status` moves and the release PR stay with the
developer: this plan to `implemented`, and both specs — which ship
their content in this release yet would otherwise stay recorded as
never approved, since process-status excludes in-flight documents and
no grep would ever surface them.

The loop spec's own Verification — running one full loop iteration
(consent asked once, a background round, licensed self-fixes with
citations, held questions batched, the ledger greppable) — is NOT run
by this plan and is not silently deferred: the loop spec's own
Verification section already carries the deferral (written 2026-08-29,
so it enters the branch with Task 1 Step 5's process-documents
commit), naming the developer as owner and the precondition —
`--plugin-dir` delivers agents but not the Rules payload, and the
loop's dispatcher behavior lives in the rules, so that run needs a
`sync-rules` re-sync first, the obligation the plugin README already
states after any update. The audit spec carries the twin deferral for
the architect narrowing's owed first live test. Neither invents a
ledger token the grammar does not admit.

## Review rounds

### 2026-08-27 — plan-adversary, fable 5, blocking (round 1, full-document)

- fixed — [Important] the section-scoped ledger hits would be structurally rejected by process-status Step 3's hard-coded frontmatter guard, and no task touched that consumer; license: the lifecycle rule's "match semantics are the mapping" clause plus the skill's runs-exactly-what-stands-here promise; the loop spec's Changes-by-file gains the process-status bullet and Task 6 Step 6 carries it
- fixed — [Important] no step wrote the audit spec's two workflow offers and the declared site count enumerated two of three; license: the audit spec's workflow bullet; Task 5 Step 2 writes both offers, the Files list names four sites
- fixed — [Important] the loop spec's plan-side recovery re-offer was routed to no task and no bullet; license: the spec's own round-5 routing precedent; declined to the spec — its workflow bullet gains the re-offer, Task 5 Step 1 carries it
- fixed — [Important] the ban sweep's Expected was unattainable (six pre-existing hits in untouched files); license: the adversary's own simulated run; the sweep scopes to release-touched files with the baseline stated
- fixed — [Important] the root README plugin-table row was missing from Task 8 while the marketplace-sync rule binds it in the same commit; license: the marketplace-sync rule's three-surface clause; Task 8 carries all four surfaces
- fixed — [Important] extending the lifecycle line-53 self-report sentence to audits was routed by neither spec and blurred the Verdict-agent/Audit-agent boundary; license: the audit spec's workflow routing plus the glossary; the extension is dropped, Task 6 Step 5 says so explicitly
- fixed — [Important] no live dispatch of either agent ran and the audit spec's named verification target was rewritten; license: the audit spec's Verification section; Task 9 Step 3 dispatches both auditors on the bundle's own documents, stamps `integrity:` and observes the re-arm
- fixed — [Minor] the literal `CLEAN` token was plan-minted; license: the release's own invented-name ⇒ spec gap rule; the audit spec now records the token
- fixed — [Minor] the Task 4 conditional-clause mandate rested on a false shipping premise; license: the plugin-authoring rule's Rules-payload scope plus the spec's unconditional §paired edit; reworded to an implementer choice with the honest rationale
- fixed — [Minor] the relay-then-stamp exception landed across two commits, violating the pair's edited-together declaration in intermediate history; license: the pair's own clause; Task 6 Step 4 lands both sentences in one commit
- fixed — [Minor] the plugin README's fields table gained no `integrity` row; license: the glossary's Misplaced-stamp enumeration; Task 8 Step 1 adds the row
- fixed — [Minor] the sweep never checked the `retire` closure-verb ban and omitted the Task 7 file; license: the plan's own Global Constraints; the sweep pattern and paths now cover both
- fixed — [Minor] the constraints claimed STOPs no task carried and the mismatch-STOP named no decider; license: the plan's own constraints section; Task 1 Step 0 gates on `status: approved`, Task 9 Step 1 names the developer

### 2026-08-27 — plan-adversary, fable 5, blocking (round 2, diff-scoped)

- fixed — [Important] the dogfood integrity audit violated the auditor's own precondition (no propagation audit over the loop spec first; the spec says both specs); license: the audit spec's precondition and Verification sentences; Step 3 runs propagation over both specs to a `CLEAN` line before the integrity dispatch
- fixed — [Important] the re-arm observation was unrunnable as sequenced (dispositions consumed pre-stamp; a verdict-free audit writes no round record to append); license: the audit spec's stamp-after-dispositions order plus the glossary's Audit-agent entry; the trigger is now a labeled audit-outcome body note appended after the stamp
- fixed — [Minor] Step 3's mid-task consent moment contradicted the constraints' two-developer-steps claim and borrowed the loop's triage authority; license: the audit spec's returns-to-the-dispatcher sentence plus the plan's own constraints; the conditional contacts are admitted in the constraints and marked as a STOP in Step 3
- fixed — [Minor] Task 6 consumed "the exception wording from Task 5" that Task 5 explicitly did not produce; license: the plan's own exclusion sentence; the interface names the real dependency (the grammar tokens and field semantics)
- fixed — [Minor] the workflow commit shipped text citing ledger conventions no rule yet defined; license: round 1's own intermediate-incoherence disposition; the lifecycle task now precedes the workflow task (Tasks 5 and 6 swapped — round-1 disposition pointers name the pre-swap numbering)
- fixed — [Minor] the plugin README's process-status row kept a four-class enumeration while the release adds a fifth class; license: the marketplace-sync rule; Task 8 Step 1 extends the row
- fixed — [Minor] the sweep's coverage claim omitted three files the release edits; license: the plan's own claim sentence; the list carries plugin.json, marketplace.json and the loop spec
- fixed — [Minor] the commit subject named only the lifecycle rule while the commit spanned three files; license: the commit-messages rule; both commit subjects renamed with the swap

Developer directive folded into this wave (2026-08-27): every Task 9
Step 3 dispatch runs as a fresh headless `claude -p` session with
`--plugin-dir` on the checkout — the session registry predates the new
agents, and headless freshness satisfies the integrity-auditor's
fresh-context requirement by construction.

### 2026-08-27 — plan-adversary, fable 5, blocking (round 3, diff-scoped)

- fixed — [Important] the integrity dispatch omitted `--model` and leaned on an unverified session default, the anti-pattern the release's own workflow text names; license: the shipped workflow rule's omitted-model sentence plus the audit spec's named-tier prescription; both dispatches pass `--model`, resolved at dispatch time
- fixed — [Important] the sequence claimed to honor the demonstrated contract yet compared no self-report before reliance or stamp; license: the audit spec's tier-verification paragraph; explicit compare steps precede both the `CLEAN` reliance and the stamp, re-dispatch on mismatch
- fixed — [Important] Step 3's spec edits followed Step 1's character-for-character certification with no return edge; license: Step 1's own bar; the sequence re-runs the diff over every touched spec section, same STOP
- fixed — [Important] the verdict sweep's Expected failed on this plan's own frontmatter under the exception the release ships; license: the approval-gate design this plan already carries; the precondition is stated and a self-hit is a STOP, never an expected exception
- fixed — [Important] the disable window spanned the conditional STOP and failure paths, leaving the developer's live install off; license: the scratchpad-dogfood recipe's own restore discipline; re-enable precedes every STOP and failure return
- fixed — [Minor] Task 8's Consumes contradicted Task 7's Produces; license: the two lines themselves; Consumes names Task 7's naming line
- fixed — [Minor] the sweep's coverage claim omitted the audit spec and silently excluded this plan file; license: the claim's own sentence; the audit spec joins the list and the mention-position exclusion is stated
- fixed — [Minor] the pinned concrete model id pre-resolved what the glossary resolves at dispatch time; license: the glossary's Tier entry; the code block carries family placeholders resolved by the executor

### 2026-08-27 — plan-adversary, fable 5, blocking (round 4, diff-scoped)

- fixed — [Important] the ban sweep's Expected was unattainable on the list member the round-3 wave added (the audit spec's recorded rejected-name trail matches `verifier`); license: the adversary's own simulated run plus the glossary's mention-position practice; the Expected states the one-hit baseline and fails on anything beyond it
- fixed — [Important] a return-to-spec resolution at the re-diff STOP edited the loop spec with text the integrity audit never read, and the stamp followed anyway; license: the audit spec's stamp-after-dispositions semantics ("was this checked after the last edit" must never answer falsely); a loop-spec edit re-enters the integrity dispatch before any stamp, waivable only explicitly with the waiver quoted
- fixed — [Minor] the verdict-sweep precondition cited a gate that never read the `adversary:` field; license: the two plan sentences themselves; Step 0 now confirms both `status: approved` and a closed `adversary:` value

### 2026-08-27 — plan-adversary, fable 5, blocking (round 5, diff-scoped)

- fixed — [Important] the re-entry edge skipped the propagation gate the release itself ships before every integrity audit; license: the audit spec's precondition sentence plus this plan's own Task 6 Step 2; a loop-spec edit re-enters item 1 to `CLEAN`, then item 2, on every pass
- fixed — [Important] the waived path flowed into an unconditional stamp whose fresh hash certified text the auditor never read; license: the audit spec's recomputed-hash semantics and its gate-offer machinery; a waiver releases the STOP but skips the stamp — the unstamped spec re-fires the gate's audit offer, the honest record

### 2026-08-27 — plan-adversary, fable 5, blocking (round 6, full-document)

- fixed — [Important] item 5's closing re-stamp wrote a fresh hash over the appended note no audit ever read — the defect round 5 blocked on the waiver path, committed on the clean path; license: the audit spec's "a differing hash means unaudited, exactly" plus its Verification mandating only the re-arm observation; item 5 ends at the quoted mismatch, the re-armed stale stamp the deliberate final state named in the Step 4 relay
- fixed — [Important] the waived path's "targets whichever stamped state exists" resolved to nothing runnable and its consumption-gate backstop had already passed; license: the audit spec's named verification and the plan's own sequencing; a waiver forfeits items 4–5 explicitly, the forfeiture named beside the quoted waiver, the verification owed with the developer as owner
- fixed — [Minor] the sweep pattern omitted the unqualified "review agent" ban from the plan's own constraints list; license: the glossary's Verdict-agent entry; the alternation extended, qualified forms judged like the mention-position practice
- fixed — [Minor] spec edits in item 3 followed Step 2's sweeps with no re-entry; license: the plan's own un-certification principle; any spec edit re-runs the ban sweep over the edited files before proceeding

### 2026-08-27 — plan-adversary, fable 5, concerns (round 7, full-document)

- fixed — [Important] the round-6 ban-sweep re-run scoped "over the edited files" made its own one-hit Expected unattainable on the typical path (loop-spec-only edits return zero hits); license: Step 1's never-reconcile-silently discipline plus the rounds 1 and 4 precedent for this class; the re-run is the Step 2 command UNCHANGED, whose file list already carries both specs
- fixed — [Minor] the re-entry edge named only the loop spec while item 1 fixes hits on both; license: the audit spec's both-specs Verification plus the plan's un-certification principle; an audit-spec edit re-enters item 1 for that spec, no item-2 re-entry
- fixed — [Minor] the stamp's hash recipe was executor-minted while its consumer is the cross-session consumption gate; license: the release's own invented-name ⇒ spec gap rule (the `CLEAN` precedent); the audit spec now carries the canonical command and item 4 quotes it
- fixed — [Minor] "Quote both recomputations" was a dangling counter left by round 6's truncation; license: the propagation-auditor's own duty 4 class; the instruction names the two hashes it means

### 2026-08-29 — plan-adversary, opus 5, blocking (round 8, full-document)

Tier note: the capability ladder changed between rounds — rounds 1–7 ran on a family no longer available, so this round's model is the prescribed tier resolved at dispatch time, not a degradation. No fallback record.

- fixed — [Important] the canonical hash recipe reached no shipped surface (spec plus a one-off dogfood command only), so stamper and gate in different sessions could digest by different conventions and the gate would report "unaudited" against a valid stamp; license: the recipe's own shared-by-both justification plus the release's invented-name ⇒ spec gap rule; Task 5 Step 4 ships the command verbatim into the lifecycle rule and Task 5's Produces carries it as a dictated token
- fixed — [Important] Task 9 declared itself read-only while Step 3 writes three classes of file, and no step committed its output — the stamp and audit-outcome note, this release's named verification deliverable, never entered the branch; license: the process-artifacts rule's never-leave-them-dirty clause; Task 9 gains a Modify list and Step 3b commits before the developer STOP
- fixed — [Important] `docs/domain/glossary.md` was routed by the audit spec, modified in the working tree since before round 1, carried by no task and swept by no command — the release's rules and agents would cite terms absent from the branch; license: the audit spec's own Changes-by-file bullet plus the verified `git status`; Task 1 Step 5 commits it at the implementation-ready gate and Step 2's sweep list and two-hit baseline cover it
- fixed — [Minor] Task 2's Produces carried the pre-swap Task 5/6 mapping, the sole surviving inversion; license: the tasks' own titles; the references are swapped
- fixed — [Minor] two Produces lines named consumers no step instantiated; license: the steps themselves; Task 1's cache-check clause is dropped (the re-mint stands on the versioning rule the plan already cites) and Task 8 Step 1 gains the architect row so Task 4's Produces is true

### 2026-08-29 — plan-adversary, opus 5, blocking (round 9, full-document)

- fixed — [Important] neither auditor's frontmatter decided `background:`, leaving the gate's blocking semantics undefined while pointing the implementer at a `background: true` exemplar; license: the four shipped agents all carrying the field, plus this release's invented-token ⇒ spec gap rule; the audit spec settles both agents at `background: true` and states the gate as a sequencing rule over the notification, and Tasks 2, 3 and 6 carry it
- fixed — [Important] the canonical recipe shipped `sha1sum` into a machine-wide rule, which stock macOS lacks — the gate would error into the false "unaudited" the shared recipe exists to prevent; license: the recipe's own portability purpose; raised to the audit spec as a spec edit, now `shasum`, with the identical-digest equivalence verified across `sha1sum`, `shasum` and `openssl sha1`
- fixed — [Important] the plan's own ledger headings carried a `, full-document` token the canonical grammar never defined, and Task 1 Step 5 commits this plan as the grammar's first exemplar; license: the grammar block's own interface status; the loop spec's shape now admits `diff-scoped` or `full-document`, and all three bundle documents' headings are normalized to it
- fixed — [Minor] item 1's spec edits escaped the un-certification guards scoped to item 3, and item 1 drove only the loop spec to `CLEAN`; license: the plan's own un-certification principle; one guard now covers any spec edit anywhere in Step 3, and item 1 holds one `CLEAN` bar for both specs
- fixed — [Minor] `resolved (declined)` had semantics but no record shape, leaving the implementer to mint one; license: the invented-token ⇒ spec gap rule; the loop spec's grammar block gains the shape
- fixed — [Minor] the ledger entry publishes four legs while process-status Step 1 collects three; license: the skill's own three-legs sentence; Task 5 Step 5 extends Step 1 to read an optional fourth leg before Step 3 consumes it
- fixed — [Minor] Task 3 dropped the by-hand `description:` quoting check Task 2 carries and named no frontmatter exemplar; license: Task 2's own step; both mirrored into Task 3
- fixed — [Minor] line locators were stale on arrival or went stale mid-task as earlier steps inserted text above them; license: the locators' own drift; every task body now cites content identifiers instead of numbers

### 2026-08-29 — plan-adversary, opus 5, blocking (round 10, full-document)

- fixed — [Important] round 9's heading-grammar fix reached the spec and the ledger headings but not Task 5's dictated-token list or the loop spec's own Changes-by-file bullet, so Task 9 Step 1 would certify the superseded grammar; license: the spec's grammar block as interface; both now carry `(round N[, <scope>])` and its two values
- fixed — [Important] the loop spec's own Verification was never run and its deferral was recorded nowhere the unfinished-work machinery could see; license: the spec's Verification section plus this plan's own waiver-path precedent for naming owed work; Step 4 records it as a `held` line with the developer as owner, naming the `sync-rules` precondition (`--plugin-dir` delivers agents, not the Rules payload the dispatcher behavior lives in)
- fixed — [Important] nothing established that either auditor was invoked AS an agent — a headless run with a hand-written prompt audits inline, matching self-report and emitting `CLEAN` while the duties and coverage tell go unexercised; license: the plan's own discriminating-observables discipline; the code block passes `--agent <name>` (verified present in `claude --help`) and the executor must quote one agent-sourced marker before relying on a report
- fixed — [Minor] the `resolved <date> (declined)` shape round 9 added to the spec was absent from Task 5's Produces, which Step 1 ships verbatim; license: the same invented-token rule round 9 applied spec-side; the shape joins the dictated list
- fixed — [Minor] the plugin README's "every component reads the glossary" claim was falsified by two components whose glossary duty no spec decided; license: the plan's own glossary-bans-bind-all-shipped-text constraint plus the propagation-auditor's duty 6 class; both agents state the duty in their bodies, since an audit agent adopts no persona and inherits nothing from `PERSONA_COMMON.md`

### 2026-08-29 — plan-adversary, opus 5, blocking (round 11, full-document)

- fixed — [Important] the `held` line round 10 mandated had no shape the shipped grammar admits (no severity, no question, no round heading), in the document committed as the grammar's first exemplar; license: the grammar block this plan ships verbatim plus the invented-token ⇒ spec gap rule; the deferral moved to the loop spec's own Verification section, where the run is defined — no ledger token invented
- fixed — [Important] Step 4's ledger write followed Step 3b's commit, leaving a tracked artifact dirty at the developer STOP — round 8's defect recurring on another file; license: the process-artifacts never-leave-them-dirty clause; the same move resolves it, the deferral now riding Step 3b's spec commit
- fixed — [Important] the propagation gate was routed into two workflow sites with no reconciliation, shipping one rule stated twice while the per-bullet diff passed on the duplicate; license: the audit spec treating them as one gate; the dispatch subsection is named canonical and the flow entry points at it
- fixed — [Important] the process-status skill gained logic no step ever ran — the plan verified the raw `rg` instead; license: round 1's own identification of that consumer as the one that would structurally reject the new hits; Step 3a runs the skill headless and quotes the report
- fixed — [Minor] the code block showed one propagation dispatch while item 1 mandates one per spec; license: item 1's own text; both invocations shown
- fixed — [Minor] Task 7 committed with no validation step; license: the plan's own every-commit constraint; the validate step added
- fixed — [Minor] the plugin README's re-sync paragraph was not extended to the audit offers, so the agents would ship with no installed rule offering them; license: the paragraph's own purpose; Task 8 Step 1 carries it

### 2026-08-29 — plan-adversary, opus 5, blocking (round 12, full-document)

- fixed — [Important] Step 3a ran after Step 3's block re-enabled the installed plugin, so the changed skill would run against a live name collision the harness resolves silently; license: the dogfood recipe's own collision guard and restore discipline; Step 3a carries its own disable/enable pair and requires the five-class marker only the plugin-dir copy can produce
- fixed — [Important] two round-11 fixes defeated each other — removing the last `held` line guaranteed zero ledger hits, so Step 3a's Expected was unattainable and the changed confirmation branch never executed; license: the sweep's own verified emptiness; Step 3a builds a two-line fixture (one in-section, one out) and expects both branches observed, deleting it before Step 3b
- fixed — [Important] the integrity-audit offer was routed into two workflow sites with no reconciliation — the defect round 11 fixed for the propagation gate and left standing for its sibling; license: the loop spec settling the pair as one reshaped offer; the flow entry points at the dispatch subsection's definition, mirroring the propagation wording
- fixed — [Important] the architect narrowing shipped with no named test and the audit spec's Verification clause naming one was neither run nor deferred — all three architect rounds on that spec predate the narrowing; license: the loop spec's own deferral precedent from round 11; recorded in the audit spec's Verification section with the developer as owner
- fixed — [Minor] both Files lists declared "four sites" their own steps contradict — under-enumerated in Task 5, over-enumerated in Task 6; license: the steps themselves, re-derived; Task 5 names five real sites, Task 6 names three edited plus one verified-not-modified
- fixed — [Minor] both specs would ship their content while recorded as never approved, and no grep would surface it; license: the lifecycle rule's linear `status`; Step 4's hand-off names three `status` moves, not one
- fixed — [Minor] the plugin README's flow line — the first thing a reader sees — omitted the two gates this release adds; license: the marketplace-sync identity discipline; Task 8 Step 1 carries it

### 2026-08-29 — plan-adversary, opus 5, blocking (round 13, full-document)

Diagnosis this round, and the reason the wave below removes seams rather than adding guards: 4 of 5 Importants sat in Task 9's harness, 1 in Task 6, none in Tasks 1–5 or 7–8 — the product half has gone two full rounds without a substantive finding while the harness produced five in two and was accelerating. The reviewer's own words: Step 3/3a had become "a second plan embedded in the first", where "every hardening fix adds a guard, and every guard adds a seam that the next round mines".

- fixed — [Important] two of the audit spec's four propagation dispatch points reached no step, because rounds 11–12 collapsed the gate to a statement sourced from the loop spec, whose gate is only "before any re-dispatch"; license: the audit spec's own dispatch-point list; Step 1's canonical statement now carries the full set and the authoring-time multi-site offer lands in the numbered flow as its own clause
- fixed — [Important] Step 3a's five-class marker rested on a false premise (the installed 0.13.0 copy ships no process-status skill at all) and discriminated nothing; license: the reviewer's verified install listing plus the skill's own mandated closers; the step invokes `/process-status` and quotes the two closers only the skill produces
- fixed — [Important] item 1's hard `CLEAN` bar had no path for a contested hit, which recurs on every re-dispatch and would put the bar out of reach forever; license: the audit spec's confirm-or-dismiss contract; a dismissal branch, a third conditional STOP in the executor-audit list, "no confirmed hits remain" as the terminal condition, and a two-re-dispatch bound
- fixed — [Important] Step 3a opened a disable window with no failure or STOP path, leaving the developer's install disabled and the fixture on disk; license: the dogfood recipe's restore discipline; ONE blanket sentence now binds every disable window in Task 9 and the per-step clause is deleted — a seam removed, not a guard added
- fixed — [Important] the fixture's shape was unspecified exactly where the changed consumer turns on it (the skill rejects every hit in a file without a frontmatter block, a clause Task 5 Step 5 never scoped); license: the skill's own text; Task 5 Step 5 decides it as a file-level invariant surviving re-scoping, and the fixture carries valid frontmatter
- fixed — [Minor] Step 4 routed the deferral to an action Step 3 does not carry and a commit that will not carry it — both deferrals are already on disk and ride Task 1 Step 5; license: the specs' own text; restated as fact
- fixed — [Minor] Task 6's Files count double-counted the co-edit clause, which sits inside the dispatch subsection the same list declares edited; license: the range's own definition; three sites, the clause verified in Step 4

Structural change, not a patch: Step 3a is demoted from a pass/fail gate to EVIDENCE the executor quotes and the developer reads at the Step 4 STOP.

Loop closed 2026-08-29 by developer adjudication — `blocking
(adjudicated 2026-08-29)`, the form the loop spec defines for a
blocking verdict a developer closes without a fresh round. The
adjudication rests on round 13's own diagnosis: the product tasks
(1–5, 7–8) went two full rounds without a substantive finding, every
round-13 finding was fixed with a cited license, and the remaining
risk sits in Task 9's verification harness, which round 13 advised
simplifying rather than reviewing further. Round 14 was dispatched
diff-scoped over the one product-side fix and stopped unread when the
adjudication landed; nothing from it is recorded. Known residual risk,
named rather than discovered later: Task 9's harness has not been
reviewed since the round-13 simplification, so its choreography is
the least-verified part of this plan.
