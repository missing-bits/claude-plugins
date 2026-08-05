---
ticket: none
date: 2026-07-30
status: implemented
adversary: concerns (resolved 2026-07-30)
branch: feature/design-personas
base: develop
---

# Design Personas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the system designer persona and two verdict-free consultation
agents in the working-process plugin, per the grilled and architect-reviewed
spec `docs/specs/2026-07-28-working-process-design-personas-design.md`.

**Architecture:** Two personas (architect, system designer) single-sourced in
`*_PERSONA.md` files at the plugin root, with shared duties, the persona
boundary, and the consultation contract held once in `PERSONA_COMMON.md`.
Each persona gets a `*-consult` agent (one briefing in, one contribution
out, fresh isolated context, no verdict) and a `*-session` skill (live
main-thread dialogue); the architect keeps its verdict-bearing agent.
Selection between surfaces is lexical — trigger phrases and counterpoints
in `description:` fields. Two repo rules widen to stay consistent with the
new components.

**Tech Stack:** Claude Code plugin components (markdown agents/skills with
YAML frontmatter), `claude plugin validate`, git.

## Global Constraints

Every task's requirements implicitly include all of these:

- **Working directory**: the git worktree at `.claude/worktrees/design-personas/`
  (branch `feature/design-personas`, based on `develop`). All paths below are
  relative to that worktree root.
- **Baseline state**: trial artifacts already exist uncommitted in the
  worktree — `plugins/working-process/PERSONA_COMMON.md`,
  `SYSTEM_DESIGNER_PERSONA.md`, both `agents/*-consult.md`, plus edits to
  `ARCHITECT_PERSONA.md`, `agents/architect.md`,
  `skills/architect-session/SKILL.md`. Tasks below EDIT these files toward
  the exact content shown; do not assume they are absent, and do not
  recreate them from scratch when an Edit would do.
- **Public-repo hygiene**: all committed text in English; no machine paths
  (`/home/<user>/…`); no company or client names. ONE exception: quoted
  example trigger phrases inside a component's `description:` (skill or
  agent) and the README trigger lines mirroring them may be non-English —
  Task 3 Step 1 widens the repo-hygiene rule to exactly this scope before
  the first agent phrases ship (precedent: grilling-session's
  "przemagluj").
- **Commit messages**: exactly one line, conventional-commit style
  (`type:` or `type(scope):`), NO body, NO trailers — in particular no
  `Co-Authored-By` line, even though the default harness instruction asks
  for one; the user's instruction overrides it.
- **Never** create `evals/trigger-evals.json` or any eval artifact for any
  skill. Never push or open a PR as part of this plan; committing locally
  per the steps below is authorized by the developer's approval of this
  plan, pushing is not.
- **Frontmatter safety**: any YAML scalar containing `: ` (colon+space)
  must be quoted, or the component silently loads with empty metadata.
- **Validation**: after every change under `plugins/working-process/`, run
  both `claude plugin validate .` and
  `claude plugin validate plugins/working-process`; both must pass before
  the task's commit. `rules/` files are NOT covered by validation — review
  their text by hand.
- **Glossary bans bind prose** (`docs/domain/glossary.md`): never "mode"
  for a persona surface; a consultation returns a **contribution**, never
  a finding; the qualified persona form is "working-process persona",
  never "process persona"; unqualified "session" means the Claude Code
  conversation, `*-session` components are "session skills".
- **Plugin-internal references** use `${CLAUDE_PLUGIN_ROOT}/…` in agent and
  skill bodies. Persona files reference `PERSONA_COMMON.md` in prose (no
  variable) — deliberate, recorded in the spec §2; do not "fix" it.
- Plugin content never references this repo's `docs/domain/` artifacts by
  path as if they ship with the plugin — the plugin installs into other
  projects.

---

### Task 1: Baseline commit — process artifacts

**Files:**
- Commit (already written, no edits): `docs/specs/2026-07-28-working-process-design-personas-design.md`,
  `docs/domain/glossary.md`, `docs/domain/adr/0001-persona-independence.md`

**Interfaces:**
- Consumes: nothing.
- Produces: a clean baseline so later tasks' `git add` of plugin paths
  never drags unrelated docs along.

- [x] **Step 1: Verify the three artifacts are the only dirty docs paths**

Run: `git status --short docs/`
Expected: exactly `M docs/domain/glossary.md`, `?? docs/domain/adr/`,
`?? docs/specs/2026-07-28-working-process-design-personas-design.md`
(plus, after this plan file is saved,
`?? docs/plans/2026-07-30-working-process-design-personas.md` — include it).

- [x] **Step 2: Commit**

```bash
git add docs/specs/2026-07-28-working-process-design-personas-design.md docs/domain/glossary.md docs/domain/adr/0001-persona-independence.md docs/plans/2026-07-30-working-process-design-personas.md
git commit -m "docs: add design-personas spec, plan, glossary entries, and persona-independence ADR"
```

---

### Task 2: `PERSONA_COMMON.md` — consultation contract and reworked opening

**Files:**
- Modify: `plugins/working-process/PERSONA_COMMON.md`
- Modify: `plugins/working-process/ARCHITECT_PERSONA.md` (pointer sentence)
- Modify: `plugins/working-process/SYSTEM_DESIGNER_PERSONA.md` (pointer sentence)

**Interfaces:**
- Consumes: current trial `PERSONA_COMMON.md` (three sections: Domain
  expertise, Glossary and ADR duty, The boundary between the personas).
- Produces: a fourth section `## The consultation contract` with a scoping
  clause; Tasks 3–6 reference it by that exact heading. Persona files
  point at the contract for consult dispatches.

- [x] **Step 1: Rework the file opening**

In `plugins/working-process/PERSONA_COMMON.md`, replace the two opening
paragraphs (everything between the `# ` title and `## Domain expertise`)
with:

```markdown
Every working-process persona carries the two duties below alongside its
own, respects the boundary between the personas, and — when dispatched in
consultation — is governed by the consultation contract that closes this
file. All four sections are defined only here, so they can never drift
between their consumers.

`plan-adversary` carries the same two duties without being a persona: it
holds its role inline rather than in a persona file, and neither the
boundary section nor the consultation contract binds it — its own charter
is the one the persona files state, failure hunting on plan mechanics.
```

- [x] **Step 2: Append the contract section**

At the end of the file, after the boundary section, append:

```markdown
## The consultation contract

This section binds `*-consult` dispatches and their dispatcher only. The
file's verdict-bearing consumers — `plan-adversary` directly, the
`architect` agent through its persona file — grade and stamp by duty, and
no sentence here overrides that.

A consultation is one dispatch: briefed once, answered once, nothing kept
alive. What the persona knows is what its briefing says.

The briefing — the dispatcher's obligations:

- carry the subject, the constraints that bind it, and — stated
  separately — what the developer has already decided against what is
  still open;
- point, don't paste: name files and areas rather than inviting
  exploration — what a consultation reads is what it costs;
- when both personas are consulted on one subject: one canonical briefing
  text given to both, each with its own focusing question appended, and
  no cross-persona content — neither is told what the other said. A
  cross-check dispatch ("the architect argued X; does that hold
  mechanically?") is legitimate on explicit request and is labelled as
  one, so the reply is read as a response rather than as an independent
  opinion.

The reply — a contribution, never a finding, never a verdict; nothing
from it is stamped into frontmatter:

- relayed to the developer attributed, in its own block, and
  substantially verbatim — compression is allowed, merging is not; every
  recommendation and every named risk survives, and text from two
  personas never lands in one bullet;
- disagreement between the personas is presented as a disagreement, with
  both positions — the choice is the developer's; the relaying thread may
  add its own opinion, marked as its own;
- a consultation is dispatched as a named background agent, so the
  developer can open its transcript and verify the relay rather than
  trust it.
```

- [x] **Step 3: Add the third leg to the boundary section**

Spec §2: "A consumer must not read a boundary that omits it" — and
`plan-adversary` (Task 6) reads only this file, never the persona files.
In `## The boundary between the personas`, after the two persona bullets
(system designer / architect), insert a third bullet:

```markdown
- **`plan-adversary`** asks *how this will fail in execution* — the third
  leg, standing outside the design-quality/mechanics split rather than
  inside it: a reviewer hunting failure on plan mechanics, not a persona.
```

- [x] **Step 4: Extend both persona files' pointer sentences**

Both edits are exact drop-in replace pairs. In
`plugins/working-process/ARCHITECT_PERSONA.md`, replace:

```markdown
judgement, and the boundary with the system
designer.
```

with:

```markdown
judgement, and the boundary with the system designer; a consult dispatch
is additionally governed by the consultation contract there.
```

In `plugins/working-process/SYSTEM_DESIGNER_PERSONA.md`, replace:

```markdown
duty that comes before any judgement, and the boundary with the architect.
```

with:

```markdown
duty that comes before any judgement, and the boundary with the
architect; a consult dispatch is additionally governed by the
consultation contract there.
```

- [x] **Step 5: Validate**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass.

- [x] **Step 6: Commit**

```bash
git add plugins/working-process/PERSONA_COMMON.md plugins/working-process/ARCHITECT_PERSONA.md plugins/working-process/SYSTEM_DESIGNER_PERSONA.md
git commit -m "feat(working-process): add shared persona file with consultation contract"
```

---

### Task 3: Consult agents — `background`, trigger phrases, contract deferral

**Files:**
- Modify: `plugins/working-process/agents/architect-consult.md` (full target content below)
- Modify: `plugins/working-process/agents/system-designer-consult.md` (full target content below)

**Interfaces:**
- Consumes: `PERSONA_COMMON.md` `## The consultation contract` (Task 2);
  persona files at the plugin root.
- Produces: the two dispatchable consult agents. Their `description:`
  trigger phrases are what Task 5's counterpoints and Task 7's workflow
  line rely on. Frontmatter keys: `disallowedTools: SendMessage`,
  `background: true`. Also widens the repo-hygiene exception (Step 1) —
  a prerequisite, or the agent descriptions below would ship non-English
  phrases the rule's letter covers only for skills.

- [x] **Step 1: Widen the repo-hygiene exception to agent descriptions**

In `.claude/rules/repo-hygiene.md`, replace:

```markdown
- all committed text is in English. One narrow exception: quoted example
  trigger phrases inside a skill's `description:`, and the `query` values of
  its trigger-eval files (`evals/trigger-evals.json`), may be non-English —
  both mirror how a developer actually asks, and the evals exercise exactly
  those phrases (precedent: grilling-session's "przemagluj"). The
  surrounding prose stays English.
```

with:

```markdown
- all committed text is in English. One narrow exception: quoted example
  trigger phrases inside a component's `description:` (skill or agent),
  the README trigger lines that mirror them, and the `query` values of
  trigger-eval files (`evals/trigger-evals.json`), may be non-English —
  all mirror how a developer actually asks, and the evals exercise
  exactly those phrases (precedent: grilling-session's "przemagluj").
  The surrounding prose stays English.
```

Commit this rule edit on its own, before the agent files:

```bash
git add .claude/rules/repo-hygiene.md
git commit -m "docs(rules): widen the non-English trigger-phrase exception to agent descriptions"
```

- [x] **Step 2: Write `agents/architect-consult.md` — exact full content**

```markdown
---
name: architect-consult
description: "Architect in consultation — judges whether a design's shape is right: fit to the stated problem, single-purpose units, speculative structure, alternatives weighed, convention fit. Answers once from a fresh, isolated context, working from a briefing rather than a document — a second opinion unshaped by the current conversation (\"konsultacja z architektem\", \"consult the architect from a clean context\", \"second opinion from the architect\"). Verdict-free by construction — it returns a contribution, and nothing it returns is stamped into frontmatter: for a formal review ending in LGTM | concerns | blocking and stamped into frontmatter, dispatch the architect agent instead; for a live back-and-forth in the main thread, use the architect-session skill. When both personas are consulted on one subject, give both the same canonical briefing (each with its own focusing question appended) and tell neither what the other said. Dispatch on the most capable available model, named, as a background agent."
disallowedTools: SendMessage
background: true
---

Consultation surface of the architect persona — the isolated one.
FIRST ACTION: read
`${CLAUDE_PLUGIN_ROOT}/ARCHITECT_PERSONA.md` and adopt it fully, including
the standing duties, the persona boundary, and the consultation contract
it points at; per the glossary duty, read `docs/domain/glossary.md` and
`docs/domain/adr/` before any judgement.

## Neither the `architect` agent nor `architect-session`

One persona, three surfaces. The `architect` agent reviews a document and
returns a verdict the dispatcher stamps into frontmatter. The
`architect-session` skill holds a live conversation in the main thread,
where follow-up questions and immediate correction matter most. This agent
answers from a fresh, isolated context — the main thread's context stays
clean, and nothing the conversation has already committed to shapes the
judgement — and returns no verdict at all.

## The dispatch

One briefing, one answer, self-contained: you are not resumed and not
spawned ahead of need, so the briefing is everything you know. Its shape —
and the shape of your reply — is the consultation contract in
`${CLAUDE_PLUGIN_ROOT}/PERSONA_COMMON.md`; follow it from there rather
than from any summary.
Treat a settled decision as settled unless it contradicts a recorded ADR,
which the glossary duty tells you how to handle.

Work the dimensions of your own duty. Where the briefing carries no
decomposition at all, say so and point at the system designer instead of
filling the gap. End with the questions you would need answered next, and
name plainly anywhere the briefing left you guessing — a briefing gap is
worth more to the developer than a confident answer built on it.

## Hard limits

- NO verdict, NO severity grading, NO frontmatter stamping. Your output
  is a contribution, never a finding.
- Never rewrite the developer's documents. Propose in your reply and let
  the dispatcher carry it.
- Write the reply for the developer, not as a report to the dispatcher —
  the contract has it relayed attributed and substantially verbatim.
- You may spawn helpers for search and documentation lookup — the
  domain-expertise duty often requires it. Never spawn another
  working-process persona: two personas reconciled inside one answer hand
  back one opinion where the developer asked for two.
```

- [x] **Step 3: Write `agents/system-designer-consult.md` — exact full content**

```markdown
---
name: system-designer-consult
description: "System designer in consultation — works out what a design is made of and how its parts behave together: parts and responsibilities, interactions and contracts, state and its lifecycle, behaviour under load, observability, technology choice. Answers once from a fresh, isolated context, working from a briefing — a second opinion unshaped by the current conversation (\"konsultacja z system designerem\", \"zapytaj designera na świeżo\", \"second opinion from the system designer\", \"consult the designer from a clean context\"). Verdict-free by construction: it returns a contribution — it grades nothing and nothing it returns is stamped into frontmatter. For a live back-and-forth in the main thread, use the system-designer-session skill instead. When both personas are consulted on one subject, give both the same canonical briefing (each with its own focusing question appended) and tell neither what the other said. Dispatch on the most capable available model, named, as a background agent."
disallowedTools: SendMessage
background: true
---

Consultation surface of the system designer persona — the isolated one.
FIRST ACTION: read
`${CLAUDE_PLUGIN_ROOT}/SYSTEM_DESIGNER_PERSONA.md` and adopt it fully,
including the standing duties, the persona boundary, and the consultation
contract it points at; per the glossary duty, read
`docs/domain/glossary.md` and `docs/domain/adr/` before any judgement.

## Not `system-designer-session`

One persona, two surfaces. The `system-designer-session` skill holds a
live conversation in the main thread, where follow-up questions and
immediate correction matter most. This agent answers from a fresh,
isolated context — the main thread's context stays clean, and nothing the
conversation has already committed to shapes the proposal.

## The dispatch

One briefing, one answer, self-contained: you are not resumed and not
spawned ahead of need, so the briefing is everything you know. Its shape —
and the shape of your reply — is the consultation contract in
`${CLAUDE_PLUGIN_ROOT}/PERSONA_COMMON.md`; follow it from there rather
than from any summary.
Treat a settled decision as settled unless it contradicts a recorded ADR,
which the glossary duty tells you how to handle.

Work the dimensions of your own duty and dismiss by name the ones that do
not apply. End with the questions you would need answered next, and name
plainly anywhere the briefing left you guessing — a briefing gap is worth
more to the developer than a confident proposal built on it.

## Hard limits

- NO verdict, NO severity grading, NO frontmatter stamping. Formal review
  ending in a verdict belongs to the `architect` agent. Your output is a
  contribution, never a finding.
- Never rewrite the developer's documents. Propose in your reply and let
  the dispatcher carry it.
- Write the reply for the developer, not as a report to the dispatcher —
  the contract has it relayed attributed and substantially verbatim.
- You may spawn helpers for search and documentation lookup — the
  domain-expertise duty often requires it. Never spawn another
  working-process persona: two personas reconciled inside one answer hand
  back one opinion where the developer asked for two.
```

- [x] **Step 4: Validate**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass — this exercises the quoted descriptions (which
contain `: ` and escaped quotes) and the `background: true` key.

- [x] **Step 5: Commit**

```bash
git add plugins/working-process/agents/architect-consult.md plugins/working-process/agents/system-designer-consult.md
git commit -m "feat(working-process): add architect-consult and system-designer-consult agents"
```

---

### Task 4: `system-designer-session` skill (new)

**Files:**
- Create: `plugins/working-process/skills/system-designer-session/SKILL.md`

**Interfaces:**
- Consumes: `SYSTEM_DESIGNER_PERSONA.md`; the consultation contract
  heading (Task 2); the `system-designer-consult` agent name (Task 3).
- Produces: the designer's interactive surface. Do NOT create any
  `evals/` directory or `trigger-evals.json` for it.

- [x] **Step 1: Write the skill — exact full content**

```markdown
---
name: system-designer-session
description: "In-session consultation with the system designer persona — interactive work on what a design is made of: parts, contracts, state, behaviour under load, observability, technology choice. Use ONLY when the developer explicitly asks to talk to the system designer (\"ask the designer\", \"porozmawiajmy z designerem\", \"system designer session\"); generic design questions belong to brainstorming. For a second opinion from a fresh context unshaped by this conversation, dispatch the system-designer-consult agent instead — this skill can assemble its briefing."
---

Consultation surface of the system designer persona — the interactive
one. FIRST ACTION: read
`${CLAUDE_PLUGIN_ROOT}/SYSTEM_DESIGNER_PERSONA.md` and adopt it fully,
including the standing duties and the persona boundary it points at
(glossary before anything else).

## Running the session

- A live design conversation in the main thread: propose the
  decomposition, the contracts, the state, the behaviour under load —
  steered by the persona's mechanics dimensions, saying "not applicable
  here" out loud for any dimension the subject genuinely lacks.
- Being interactive, you may simply ask the developer which domains
  matter instead of only inferring them.
- One topic at a time; take a position on every question discussed.

## Hard limits

- NO verdict and NO frontmatter stamping — the designer has no
  verdict-bearing agent; a document this session shaped goes through the
  `architect` agent gate as usual.
- Never rewrite the developer's documents unasked.

## Handing off

As decisions settle, point at the right next step:

- new or changed domain terms/decisions → a grilling-session (it records
  the glossary/ADR updates);
- the same question, wanted from a fresh context unshaped by this
  conversation → a `system-designer-consult` dispatch. This skill runs in
  the main thread, so it assembles the briefing the consultation contract
  in `${CLAUDE_PLUGIN_ROOT}/PERSONA_COMMON.md` requires: the subject,
  the binding constraints,
  settled decisions separated from open questions, and pointers to files
  rather than pasted content;
- a document ready for formal review → an `architect` agent dispatch,
  with a domain hint from this session.
```

- [x] **Step 2: Validate**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass.

- [x] **Step 3: Commit**

```bash
git add plugins/working-process/skills/system-designer-session/SKILL.md
git commit -m "feat(working-process): add system-designer-session skill"
```

---

### Task 5: Architect surfaces — arbitration counterpoints and narrowing

**Files:**
- Modify: `plugins/working-process/agents/architect.md`
- Modify: `plugins/working-process/skills/architect-session/SKILL.md`

**Interfaces:**
- Consumes: agent name `architect-consult` (Task 3).
- Produces: descriptions that no longer compete head-on with the consult
  agent; glossary duty re-tightened to "earns a finding" on the
  verdict-bearing agent.

- [x] **Step 1: Narrow and counterpoint the `architect` agent description**

In `plugins/working-process/agents/architect.md`, in the `description:`
value, replace:

```
Architect reviewing design quality — a grilled spec (primary target) or any design document or question dispatched standalone.
```

with:

```
Architect reviewing design quality — a grilled spec (primary target) or any design document dispatched standalone; its report always ends in a verdict. For a verdict-free second opinion on a question, dispatch architect-consult instead.
```

The rest of the description is unchanged.

- [x] **Step 2: Re-tighten the glossary duty in the agent body**

In the same file, replace:

```markdown
Formal-review surface of the architect persona. FIRST ACTION: read
`${CLAUDE_PLUGIN_ROOT}/ARCHITECT_PERSONA.md` and adopt it fully; per its glossary
duty, read `docs/domain/glossary.md` and `docs/domain/adr/` right after
the persona, before any judgement.
```

with:

```markdown
Formal-review surface of the architect persona. FIRST ACTION: read
`${CLAUDE_PLUGIN_ROOT}/ARCHITECT_PERSONA.md` and adopt it fully; per its glossary
duty, read `docs/domain/glossary.md` and `docs/domain/adr/` right after
the persona, before any judgement. Re-tightening that duty's shared
floor: a subject contradicting a glossary term or a recorded ADR earns a
finding (evidence = that file), not only a call-out.
```

- [x] **Step 3: Extend the Stamping section to both consultation surfaces**

In the same file, replace:

```markdown
bare question has nothing to stamp. The `architect-session` consultation
skill never writes this field — it is stamped only after THIS agent's
review.
```

with:

```markdown
bare question has nothing to stamp. Neither consultation surface — the
`architect-session` skill or the `architect-consult` agent — ever writes
this field; it is stamped only after THIS agent's review.
```

- [x] **Step 4: Counterpoint and staleness fix in `architect-session`**

In `plugins/working-process/skills/architect-session/SKILL.md`:

(a) In `description:`, append before the closing sentence boundary — the
current value ends with "A formal review with a verdict is the architect
agent's job, never this skill's." Extend the value so it ends with:

```
A formal review with a verdict is the architect agent's job, never this skill's; for a second opinion from a fresh context unshaped by this conversation, dispatch the architect-consult agent instead — this skill can assemble its briefing.
```

The current value is an unquoted plain scalar with no `: ` inside, and
the appended text introduces none — quoting stays optional; if in doubt,
quote the whole value.

(b) Replace the stale opening (post-extraction "both duties" wording):

```markdown
Consultation surface of the architect persona — the interactive one.
FIRST ACTION: read
`${CLAUDE_PLUGIN_ROOT}/ARCHITECT_PERSONA.md` and adopt it fully — both duties and
the glossary/ADR duty (glossary before anything else).
```

with:

```markdown
Consultation surface of the architect persona — the interactive one.
FIRST ACTION: read
`${CLAUDE_PLUGIN_ROOT}/ARCHITECT_PERSONA.md` and adopt it fully, including
the standing duties and the persona boundary it points at (glossary
before anything else).
```

(c) In `## Handing off`, insert a new second bullet between the
grilling-session bullet and the formal-review bullet:

```markdown
- the same question, wanted from a fresh context unshaped by this
  conversation → an `architect-consult` dispatch. This skill runs in the
  main thread, so it assembles the briefing the consultation contract in
  `${CLAUDE_PLUGIN_ROOT}/PERSONA_COMMON.md` requires: the subject, the
  binding constraints,
  settled decisions separated from open questions, and pointers to files
  rather than pasted content;
```

- [x] **Step 5: Validate**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass.

- [x] **Step 6: Commit**

```bash
git add plugins/working-process/agents/architect.md plugins/working-process/skills/architect-session/SKILL.md
git commit -m "feat(working-process): tighten architect surfaces for consultation arbitration"
```

---

### Task 6: `plan-adversary` sources standing duties from the shared file

**Files:**
- Modify: `plugins/working-process/agents/plan-adversary.md`

**Interfaces:**
- Consumes: `PERSONA_COMMON.md` (Task 2) — its carve-out clause names
  `plan-adversary`.
- Produces: the declared behaviour change (spec Scope): plan-adversary
  gains the domain-expertise duty; its checklist scan becomes that duty's
  first source.

- [x] **Step 1: Replace the FIRST ACTION paragraph**

In `plugins/working-process/agents/plan-adversary.md`, replace:

```markdown
FIRST ACTION: read `docs/domain/glossary.md` and `docs/domain/adr/` when
they exist. Canonical terms bind your wording, and a plan contradicting a
glossary term or a recorded ADR is a finding (evidence = that file).
```

with:

```markdown
FIRST ACTION: read `${CLAUDE_PLUGIN_ROOT}/PERSONA_COMMON.md` and adopt
its standing duties — domain expertise and the glossary/ADR duty; the
boundary section and the consultation contract there carve you out by
name. Then, per that glossary duty, read `docs/domain/glossary.md` and
`docs/domain/adr/` when they exist. Canonical terms bind your wording,
and — re-tightening the shared file's "called out" floor — a plan
contradicting a glossary term or a recorded ADR is a finding
(evidence = that file).
```

- [x] **Step 2: Position the checklist mechanism under the duty**

In the same file, replace the `## Domain checklists` section body:

```markdown
Scan the available skills for names matching `*-plan-review`. For every
domain the plan touches — judged from its content and the repo's markers
(e.g. `sfdx-project.json` → Salesforce) — load the matching checklist and
walk its dimensions with the same rigor as the generic ones below.
Domains without a checklist get the generic dimensions only.
```

with:

```markdown
The first source under the shared file's domain-expertise duty: scan the
available skills for names matching `*-plan-review`. For every domain the
plan touches — judged from its content and the repo's markers (e.g.
`sfdx-project.json` → Salesforce) — load the matching checklist and walk
its dimensions with the same rigor as the generic ones below. Domains
without a checklist get the generic dimensions only, with the duty's
remaining sources (other skills, then verified model knowledge) covering
the expertise.
```

- [x] **Step 3: Validate**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass.

- [x] **Step 4: Commit**

```bash
git add plugins/working-process/agents/plan-adversary.md
git commit -m "feat(working-process): source plan-adversary standing duties from the shared persona file"
```

---

### Task 7: `rules/workflow.md` — consent offer and the two collisions

**Files:**
- Modify: `plugins/working-process/rules/workflow.md`

**Interfaces:**
- Consumes: agent names `architect-consult`, `system-designer-consult`
  (Task 3).
- Produces: the step-1 consent offer; "architect" disambiguated to the
  backticked `architect` agent; consultations named in the
  model-selection paragraph. This file is the payload's only always-on
  rule — keep the additions to the lines specified, nothing more.

- [x] **Step 1: Extend step 1**

Replace:

```markdown
1. **Idea → spec.** When the superpowers:brainstorming skill is
   available, start non-trivial features there; capture the agreed design
   as a spec in `docs/specs/`.
```

with:

```markdown
1. **Idea → spec.** When the superpowers:brainstorming skill is
   available, start non-trivial features there; capture the agreed design
   as a spec in `docs/specs/`. When the working-process consult agents
   (`architect-consult`, `system-designer-consult`) are available, ask
   once, early in the design conversation, whether the two personas
   should be consulted as the design forms — yes / not now / not in this
   session (honoured for the Claude Code session only; a durable
   preference belongs in the developer's own instructions and is
   respected when present). After a yes, dispatch a consultation when it
   looks worth its cost, without asking again for that conversation, and
   state the consent decision whenever it is made or changed. On a
   genuinely ambiguous ask — in-thread dialogue or a fresh-context
   consultation? — ask one short question rather than silently picking a
   surface.
```

- [x] **Step 2: Tighten "architect" to the agent in step 3 and the stamping sentence**

Replace:

```markdown
3. **Grilled spec → architect review.** Offer a dispatch of the
   working-process architect agent (when available); stamp its verdict
```

with:

```markdown
3. **Grilled spec → architect review.** Offer a dispatch of the
   working-process `architect` agent (when available); stamp its verdict
```

and replace:

```markdown
After every architect or plan-adversary round, record the verdict
(`LGTM` | `concerns` | `blocking`) in the reviewed document's
`architect:` / `adversary:` frontmatter field.
```

with:

```markdown
After every round of the `architect` agent or plan-adversary, record the
verdict (`LGTM` | `concerns` | `blocking`) in the reviewed document's
`architect:` / `adversary:` frontmatter field. A consultation
(`*-consult`) produces no verdict and nothing to record.
```

- [x] **Step 3: Name consultations in the model-selection paragraph**

Replace:

```markdown
in both directions. Reviews are never dispatched on the cheapest
available family.
```

with:

```markdown
in both directions. Reviews are never dispatched on the cheapest
available family. Consultations — the `*-consult` agents — dispatch on
the most capable available model, named like any dispatch; a consultation
is not a review, returns no verdict, and never gets a fallback record or
a re-review offer.
```

- [x] **Step 4: Hand-review and validate**

`rules/` is not covered by `claude plugin validate` — re-read the whole
file top to bottom checking: the file still has no YAML frontmatter (it
is the deliberate always-on rule), every mention of a skill or agent is
conditional ("when available"), and no line exceeds the file's plain-text
conventions. Then run
`claude plugin validate . && claude plugin validate plugins/working-process`
(unaffected, but confirms nothing else broke).

- [x] **Step 5: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): add consultation consent offer to the workflow rule"
```

---

### Task 8: Repo rules — `*-consult` category and prerelease widening

**Files:**
- Modify: `.claude/rules/plugin-authoring.md`
- Modify: `.claude/rules/plugin-versioning.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the naming category Task 3's agents instantiate; the version
  grammar Task 9's `0.11.0-dev.design-personas` requires. The versioning
  edit MUST carry its rationale inline — the grilling declined this
  decision an ADR on exactly that condition.

- [x] **Step 1: Add the `*-consult` category to the authoring rule**

In `.claude/rules/plugin-authoring.md`, replace:

```markdown
- Names are kebab-case. Skills whose content is an open-ended
  conversation are named `*-session`; formal reviews that end in a verdict
  are agents. Operational skills may prompt for decisions without being
  sessions — they are named for what they do (e.g. `sync-rules`).
```

with:

```markdown
- Names are kebab-case. Skills whose content is an open-ended
  conversation are named `*-session`; formal reviews that end in a verdict
  are agents; verdict-free consultation agents — one briefing in, one
  contribution out, from a fresh isolated context — are named `*-consult`.
  Operational skills may prompt for decisions without being
  sessions — they are named for what they do (e.g. `sync-rules`).
```

- [x] **Step 2: Widen the `dev` discriminator in the versioning rule**

In `.claude/rules/plugin-versioning.md`, replace:

```markdown
- Dogfooding unreleased content needs a changed version string — the
  plugin cache keys content by version. A topic branch that dogfoods a
  plugin sets `X.Y.Z-dev.<issue>` on it (the issue number the branch
  name carries); the suffix flows into develop as-is. A topic that
  does not dogfood never touches the version. On a version-line merge
  conflict between parallel topics, the merging topic's own
  `-dev.<issue>` wins — both strings are provisional. The release PR
```

with:

```markdown
- Dogfooding unreleased content needs a changed version string — the
  plugin cache keys content by version. A topic branch that dogfoods a
  plugin sets `X.Y.Z-dev.<discriminator>` on it — the issue number the
  branch name carries, or the branch short-name when the topic has no
  issue (e.g. `-dev.design-personas`). Widening the discriminator
  instead of minting another channel keeps one channel for one purpose;
  the discriminator only needs to be unique among parallel topics. The
  suffix flows into develop as-is. A topic that
  does not dogfood never touches the version. On a version-line merge
  conflict between parallel topics, the merging topic's own
  `-dev.<discriminator>` wins — both strings are provisional. The release PR
```

and replace:

```markdown
- Prerelease grammar: `-<channel>.<discriminator>`. Defined channels:
  `dev.<issue>` (topic-branch dogfooding, above) and `rc.<n>` (release
```

with:

```markdown
- Prerelease grammar: `-<channel>.<discriminator>`. Defined channels:
  `dev.<discriminator>` (topic-branch dogfooding, above) and `rc.<n>` (release
```

- [x] **Step 3: Add the two persona paths to the breaking-surface list**

In the same file, replace:

```markdown
    `*-plan-review` discovery convention, the plugin-root persona path —
    `ARCHITECT_PERSONA.md`).
```

with:

```markdown
    `*-plan-review` discovery convention, the plugin-root persona paths —
    `ARCHITECT_PERSONA.md`, `SYSTEM_DESIGNER_PERSONA.md`,
    `PERSONA_COMMON.md`).
```

- [x] **Step 4: Hand-review**

Re-read both edited rules end to end: rule files under `.claude/rules/`
are not validated by any tool; check no other line still says
`-dev.<issue>` (`grep -n 'dev\.<issue>' .claude/rules/plugin-versioning.md`
must return nothing).

- [x] **Step 5: Commit**

```bash
git add .claude/rules/plugin-authoring.md .claude/rules/plugin-versioning.md
git commit -m "docs(rules): add *-consult naming category and widen the dev prerelease discriminator"
```

---

### Task 9: Plugin identity, version, and the three synced surfaces

**Files:**
- Modify: `plugins/working-process/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `README.md` (repo root — the plugin table row)
- Modify: `plugins/working-process/README.md`

All four in ONE commit — the marketplace-sync rule requires plugin.json,
catalog, and repo README to move together on any description change; the
plugin README rides along.

**Interfaces:**
- Consumes: all shipped component names (Tasks 3–4); the widened grammar
  (Task 8) legalizing the version string.
- Produces: version `0.11.0-dev.design-personas` — the dogfooding key for
  the whole topic.

- [x] **Step 1: `plugin.json` — description and version**

Replace the `description` value with:

```
Spec-driven working process on top of superpowers: grilling-session, architect-session, system-designer-session and sync-rules skills, architect and plan-adversary review agents, architect-consult and system-designer-consult consultation agents, and process rules distributed as a Rules payload; domain plugins hook in via *-plan-review checklist skills and their own rules/ payloads
```

Replace the `version` value: `0.11.0-dev.10` → `0.11.0-dev.design-personas`.

- [x] **Step 2: `.claude-plugin/marketplace.json` — catalog description**

Replace the working-process entry's `description` value with:

```
Spec-driven working process on top of superpowers: grilling-session, architect-session, system-designer-session and sync-rules skills, architect and plan-adversary review agents, architect-consult and system-designer-consult consultation agents, plus distributed process rules
```

- [x] **Step 3: Repo `README.md` — the plugin table row**

Replace the `working-process` row's description cell with:

```
Spec-driven working process: grilling-session, architect-session, system-designer-session and sync-rules skills, architect and plan-adversary review agents, two verdict-free consultation agents, distributed process rules
```

- [x] **Step 4: Plugin `README.md` — components, single-sourcing, model selection**

(a) In `## Components`, after the `architect-session` entry, insert:

```markdown
- **`architect-consult` agent** — the architect as a one-shot
  consultation from a fresh, isolated context: one briefing in, one
  contribution out, no verdict, nothing stamped. Dispatched as a named
  background agent on the most capable available model. Triggers:
  "konsultacja z architektem" / "second opinion from the architect".
- **`system-designer-consult` agent** — the system designer persona
  (parts, contracts, state, behaviour under load, observability,
  technology choice) as the same kind of one-shot consultation.
  Triggers: "zapytaj designera na świeżo" / "second opinion from the
  system designer".
- **`system-designer-session` skill** — the system designer as an
  interactive in-session consultation; hands off to a grilling-session,
  a `system-designer-consult` dispatch (assembling its briefing), or an
  `architect` dispatch. Triggers: "ask the designer" / "porozmawiajmy z
  designerem".
```

(b) Replace the single-sourcing paragraph:

```markdown
The architect persona is single-sourced in [ARCHITECT_PERSONA.md](./ARCHITECT_PERSONA.md),
shared by the `architect` agent and the `architect-session` skill. Every
component reads `docs/domain/glossary.md` and `docs/domain/adr/` first,
when they exist, so it speaks the project's language from its first
message.
```

with:

```markdown
Each persona is single-sourced in its file at the plugin root —
[ARCHITECT_PERSONA.md](./ARCHITECT_PERSONA.md) and
[SYSTEM_DESIGNER_PERSONA.md](./SYSTEM_DESIGNER_PERSONA.md) — with the
shared duties, the persona boundary, and the consultation contract held
once in [PERSONA_COMMON.md](./PERSONA_COMMON.md). `plan-adversary`
sources its standing duties from the same shared file without being a
persona. Every component reads `docs/domain/glossary.md` and
`docs/domain/adr/` first, when they exist, so it speaks the project's
language from its first message.
```

(c) In `## Model selection`, after the sentence ending "one family below
for small mechanical ones.", insert:

```markdown
Consultations (the `*-consult` agents) dispatch on the most capable
available model as named background agents; they return no verdict, so
the fallback machinery below never applies to them.
```

- [x] **Step 5: Validate**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass (this exercises the edited JSON files).

- [x] **Step 6: Commit**

```bash
git add plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md plugins/working-process/README.md
git commit -m "feat(working-process): sync plugin identity and set dogfooding version 0.11.0-dev.design-personas"
```

---

### Task 10: Final verification sweep

**Files:**
- No new edits expected; fixes discovered here ride in a final
  `fix(working-process):` commit.

- [x] **Step 1: Validate both levels one last time**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both pass.

- [x] **Step 2: Glossary-ban greps — all must come back clean**

```bash
# banned qualified persona form (only the "working-process persona(s)"
# compound may appear — the -i exclusion covers its capitalized and
# plural forms while still catching a bare "process personas"):
grep -rn -i 'process persona' plugins/working-process/ | grep -v -i 'working-process persona'
# banned "mode" for a persona surface — inspect any hit by eye:
grep -rn '\bmode\b' plugins/working-process/agents/ plugins/working-process/skills/architect-session/ plugins/working-process/skills/system-designer-session/ plugins/working-process/*.md
# a consultation never returns a "finding":
grep -rn -i 'finding' plugins/working-process/agents/architect-consult.md plugins/working-process/agents/system-designer-consult.md plugins/working-process/skills/system-designer-session/SKILL.md
```

Expected: first grep empty; second grep only "failure … modes" senses
(e.g. `SYSTEM_DESIGNER_PERSONA.md` "failure and recovery modes") or
review-report `mode:` mentions, never "X mode of the Y persona"; third
grep only the contrastive "never a finding" lines.

- [x] **Step 3: Cross-reference sweep**

```bash
# every plugin file naming the consult agents spells them correctly:
grep -rn 'consult' plugins/working-process/ .claude/rules/plugin-authoring.md | grep -v -- '-consult'
# no plugin file references this repo's ADR by path:
grep -rn '0001-persona-independence' plugins/
# version string consistent:
grep -rn 'design-personas' plugins/working-process/.claude-plugin/plugin.json
```

Expected: first grep only prose uses of "consultation/consulted"; second
grep empty; third grep exactly the one version line.

- [x] **Step 4: Confirm a clean tree**

Run: `git status --short`
Expected: empty (every task committed its files). If anything is dirty,
it belongs to a task above — finish that task rather than sweeping it in
here.

---

## Self-review record

Checked against the spec section by section: §1 dimensions and the
"not applicable" licence live in the persona files (baseline, Task 2
pointer edits); §2 single-sourcing incl. the two stated consequences
(Tasks 2, 6) and the versioning-list addition (Task 8); §3 surface table,
lexical arbitration — trigger phrases and counterpoints (Tasks 3, 4, 5)
plus the ask-on-ambiguity rule (Task 7);
§4 one-shot dispatch + `background` (Task 3); §5 independence —
`disallowedTools` retained, textual limit reworded to "working-process
persona" (Task 3); §6–7 the contract in `PERSONA_COMMON.md` with its
scoping clause and the invariant sentence in both descriptions (Tasks 2,
3); §8 the offer and the two workflow collisions (Task 7); §9 has no
implementable artifact (cost is an argument, not a mechanism); §10
attribution/verifiability via the contract and `background: true`
(Tasks 2, 3), consent-state line (Task 7). Non-goals introduce no tasks.
Files-to-touch list fully mapped: every file it names appears in exactly
one task above. Accepted risks: the `disallowedTools`-floor check and
selection-quality dogfooding happen after implementation under the
`-dev.design-personas` version, outside this plan.

## Adversary findings — 2026-07-30 round 1

Dispatched on Fable 5 (self-reported: fable 5; prescribed tier). Verdict:
blocking — three Important, three Minor. The round verified every quoted
replace-block in Tasks 5–9 character-exact against the worktree; the
blockers were coverage gaps, not stale old-strings. All six resolved the
same day by plan revision:

- **Important**: the boundary section's third leg (spec §2:
  "A consumer must not read a boundary that omits it") had no task —
  `plan-adversary` reads only `PERSONA_COMMON.md`. → Fixed: Task 2 Step 3
  adds the third bullet to the boundary section.
- **Important**: spec §3's ask-on-ambiguity bullet landed in no artifact.
  → Fixed: appended to the workflow.md step-1 addition (Task 7), the
  always-on main-thread surface where the picking happens.
- **Important**: Polish trigger phrases in *agent* descriptions and README
  bullets exceeded the repo-hygiene exception's letter ("a skill's
  `description:`"). → Fixed: Task 3 Step 1 widens the rule (own commit,
  before the first agent phrases ship); Global Constraints updated to
  match.
- **Minor**: Task 2's first pointer-edit old-string did not match
  `ARCHITECT_PERSONA.md` verbatim. → Fixed: verbatim ending quoted.
- **Minor**: neither consult description carried the noun "contribution"
  (spec §7: "the descriptions alike"). → Fixed in both target
  descriptions.
- **Minor**: the Task 10 banned-form grep masked the plural via
  `grep -v 'personas'`. → Fixed: case-insensitive exclusion of the
  legitimate compound only.

## Adversary findings — 2026-07-30 round 2

Fresh dispatch on the revised plan, Fable 5 (self-reported: fable 5;
prescribed tier). Verdict: concerns — two Minor, both introduced by the
round-1 revision; all six round-1 resolutions independently confirmed
against the worktree. Both resolved the same day; the frontmatter carries
`concerns (resolved 2026-07-30)`:

- **Minor**: Task 2 Step 4's replacement block was not a drop-in for its
  quoted old-string — it opened with a literal ellipsis and re-quoted
  text preceding the old-string, so a mechanical replace would corrupt
  the pointer sentence. → Fixed: both persona-file edits are now exact
  replace pairs, the designer file's quoted verbatim too.
- **Minor**: four agent/skill body sites referenced the shared file as
  bare `PERSONA_COMMON.md`, against the plan's own Global Constraint and
  the authoring rule (`${CLAUDE_PLUGIN_ROOT}/…` in bodies; the bare-name
  carve-out covers persona files only). → Fixed: all four sites use
  `${CLAUDE_PLUGIN_ROOT}/PERSONA_COMMON.md`.
