---
ticket: none
date: 2026-07-13
status: approved
adversary: LGTM
branch: feature/working-process
base: master
spec: ../specs/2026-07-13-working-process-plugin-design.md
---

# working-process Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `working-process` plugin (grilling-session and architect-session skills, architect and plan-adversary agents) and register it in the `missing-bits` marketplace.

**Architecture:** A single Claude Code plugin under `plugins/working-process/`: two interactive skills, two review agents, and one shared persona file at the plugin root loaded by both architect-mode components via `${CLAUDE_PLUGIN_ROOT}`. The marketplace catalog references the plugin by relative path and allows its one cross-marketplace dependency (superpowers).

**Tech Stack:** Claude Code plugin system (plugin.json, marketplace.json, skills/SKILL.md, agents/*.md), git, jq for JSON validation.

## Global Constraints

- All committed text is in English.
- All plugin text is authored for this plugin from scratch — never import or paraphrase-copy text from other plugins; behavior comes from the spec only.
- Claude Code ≥ 2.1.143 is the supported floor (dependency enable/disable cascade).
- Names are kebab-case: plugin `working-process`; skills `grilling-session`, `architect-session`; agents `architect`, `plan-adversary`.
- `plugin.json`: version `0.1.0`, license `MIT`, author `Jacek Nakonieczny`, dependency `{ "name": "superpowers", "marketplace": "claude-plugins-official" }`.
- `allowCrossMarketplaceDependenciesOn` is a TOP-LEVEL field of `marketplace.json` (sibling of `plugins`), value `["claude-plugins-official"]`.
- Commits: Conventional Commits 1.0.0, single subject line, no body, no trailers (no Co-Authored-By).
- Every component's first action chain includes the glossary-first rule: read `docs/domain/glossary.md` and `docs/domain/adr/` when they exist (agents: right after the persona load).
- Repo root during execution: the claude-plugins repository root, branch `feature/working-process`.

---

### Task 1: Plugin manifest and shared persona

**Files:**
- Create: `plugins/working-process/.claude-plugin/plugin.json`
- Create: `plugins/working-process/PERSONA.md`

**Interfaces:**
- Produces: plugin name `working-process` (consumed by Task 7's marketplace entry) and the persona path `${CLAUDE_PLUGIN_ROOT}/PERSONA.md` (consumed by Tasks 3 and 4).

- [ ] **Step 1: Write `plugins/working-process/.claude-plugin/plugin.json`**

```json
{
  "name": "working-process",
  "description": "Spec-driven working process on top of superpowers: grilling-session and architect-session skills plus architect and plan-adversary review agents; domain plugins hook in via *-plan-review checklist skills",
  "version": "0.1.0",
  "author": { "name": "Jacek Nakonieczny" },
  "license": "MIT",
  "keywords": ["process", "workflow", "spec", "plan", "review", "glossary", "adr", "architecture"],
  "dependencies": [
    { "name": "superpowers", "marketplace": "claude-plugins-official" }
  ]
}
```

- [ ] **Step 2: Write `plugins/working-process/PERSONA.md`**

```markdown
# The architect persona

Adopt the role of a seasoned software architect. Two duties, in this
order, plus a standing glossary duty.

## First duty — design quality

Evaluate how well the design is shaped — not how it might fail (failure
hunting belongs to plan-adversary):

- Fit: does the proposal solve exactly the stated problem — nothing
  missing, nothing extra?
- Boundaries: does every unit have a single purpose and a well-defined
  interface?
- Over-engineering: call out speculative structure — abstractions with a
  single consumer, generality nobody asked for, future-proofing beyond
  the task at hand.
- Alternatives: were realistic options weighed, and is the chosen one
  argued?
- Convention fit: does the design follow the project's established
  patterns and structures?

## Second duty — domain expertise

For every domain the subject touches (git, a language, a framework, a
platform, …), speak as an expert in that domain. Source the expertise in
this order:

1. **Skills available in the session** — scan them and load any that
   cover an assumed domain, whatever their naming scheme.
2. **Model knowledge** — where no skill covers a domain, review from your
   own knowledge with the expert role stated explicitly.

Never lean on recall for load-bearing facts: check official documentation
or search the web when available, and cite what you checked.

## Glossary and ADR duty

Before forming any judgement, read the project's domain artifacts when
they exist: `docs/domain/glossary.md` and `docs/domain/adr/`. Canonical
terms and `_Avoid_` bans bind your own wording. A subject that contradicts
a glossary term or a recorded ADR earns a finding (cite the file) — except
when it names the decision, argues for changing it, and routes the update
through a grilling-session: that is superseding a decision, not
contradicting it.
```

- [ ] **Step 3: Validate**

Run: `jq -e '.name == "working-process" and .version == "0.1.0" and (.dependencies[0].marketplace == "claude-plugins-official")' plugins/working-process/.claude-plugin/plugin.json`
Expected: `true`

Run: `grep -c "docs/domain/glossary.md" plugins/working-process/PERSONA.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/.claude-plugin/plugin.json plugins/working-process/PERSONA.md
git commit -m "feat(working-process): scaffold plugin manifest and architect persona"
```

---

### Task 2: grilling-session skill

**Files:**
- Create: `plugins/working-process/skills/grilling-session/SKILL.md`
- Create: `plugins/working-process/skills/grilling-session/GLOSSARY-FORMAT.md`
- Create: `plugins/working-process/skills/grilling-session/ADR-FORMAT.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the skill name `grilling-session` referenced by Tasks 3, 4 (handoffs) and 6 (README); the domain-directory contract (`docs/domain/glossary.md`, `docs/domain/adr/NNNN-slug.md`, first-create question) that Tasks 4 and 5 rely on.

- [ ] **Step 1: Write `plugins/working-process/skills/grilling-session/SKILL.md`**

```markdown
---
name: grilling-session
description: Grilling session that stress-tests a spec (the primary target), plan, or raw idea against the project's domain glossary and recorded decisions, sharpens terminology, and applies glossary/ADR updates inline as decisions land. Use ONLY when the developer explicitly asks to be grilled ("grill me", "przemagluj"); plain "build X" requests belong to brainstorming. Formal design review with a verdict is the architect agent's job, never this skill's.
---

## Place in the flow

idea → brainstorming (spec) → **grilling-session on the spec** →
architect review (an `architect` agent dispatch) → writing-plans (plan) →
plan-adversary on the plan → implementation. Offer a grilling once a spec
exists and before its implementation plan is written. Specs are the
primary target; plans and raw ideas are in scope too.

## Glossary first

FIRST ACTION: read `docs/domain/glossary.md` and `docs/domain/adr/` if
they exist. Canonical terms and `_Avoid_` bans bind your own wording from
the very first question — open the session already speaking the project's
language.

## Artifacts — the domain directory

The session writes to the project's domain directory, `docs/domain/`:

- `docs/domain/glossary.md` — canonical terms
  ([GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md))
- `docs/domain/adr/NNNN-slug.md` — recorded decisions
  ([ADR-FORMAT.md](./ADR-FORMAT.md))

### First-create question

- Creating `docs/domain/` for the first time? ASK the developer whether
  the directory should be git-ignored (write `docs/domain/.gitignore`
  containing exactly `*` — ignored mode) or committed (no `.gitignore` —
  tracked mode). Assume no default.
- The directory already exists? Never ask when a prior decision is
  observable: a `.gitignore` with `*` means ignored mode; any
  git-tracked file under it (`git ls-files docs/domain` non-empty) means
  tracked mode. Neither signal present? No decision was ever made — ask,
  exactly as on first creation.

## Frontmatter stamping

Stamp only documents that follow the frontmatter convention: the target
opens with a YAML block containing a `status` field. Otherwise skip
stamping silently — a raw idea has nothing to stamp. When the convention
applies (edit with the Edit tool):

- Session start: set `grilled: grilling`.
- Session end: replace it with the ISO date (e.g. `grilled: 2026-07-13`)
  — but ONLY once every decision, glossary update, and document amendment
  from the session has been applied.
- A session cut short leaves `grilling` in place on purpose: greppable
  debt (`rg -l '^grilled: grilling' docs/`).

## Grilling mechanics

- Interview toward shared understanding: one question at a time, wait for
  the answer, and recommend an answer with every question.
- Never ask what code or project metadata can answer — read the source,
  grep, use domain CLIs instead.
- Glossary conflict → quote the definition and ask which meaning is
  intended. Fuzzy term → propose a canonical one. Probe edge cases.
  Verify claims against the code.
- Apply glossary updates inline the moment a term settles — no batching.
- ADRs are rare: offer one only when the decision is hard to reverse AND
  surprising without context AND a real trade-off existed.

## Closing the session

1. Apply every remaining outcome, then stamp the `grilled:` date (see
   above).
2. Tracked mode only: list the artifact files the session touched and
   remind the developer they belong in the current work's commit. Never
   commit — committing stays with the developer.
3. Offer the next step: an `architect` agent dispatch on the grilled
   document, with a domain hint gathered during this session.
```

- [ ] **Step 2: Write `plugins/working-process/skills/grilling-session/GLOSSARY-FORMAT.md`**

```markdown
# Format of glossary.md

Path: `docs/domain/glossary.md` (the domain directory).

## Shape

    # {Project} — domain glossary

    {One or two sentences on what this project/org is about.}

    ## Language

    **Booking**:
    {What a Booking IS, in one or two sentences.}
    _Avoid_: reservation, order

## Rules

- Be opinionated: one winner per synonym set; the losers go under
  `_Avoid_`.
- Keep entries tight — one or two sentences saying what the term IS, not
  what it does.
- Only project-specific language. Platform-generic concepts stay out.
  The test: could this entry appear unchanged in a random other project's
  glossary? Then it does not belong here.
- Cluster entries under subheadings once groups emerge; a single flat
  list is fine until then.
- Strong candidates: record types, personas/roles, integration names.
```

- [ ] **Step 3: Write `plugins/working-process/skills/grilling-session/ADR-FORMAT.md`**

```markdown
# Format of ADRs

Path: `docs/domain/adr/NNNN-slug.md`, numbered sequentially from `0001`.
Create the directory lazily, when the first ADR lands.

## Shape

    # {Short title}

    {One to three sentences: the context, the decision, the reason.}

A single paragraph is enough — the value is that the decision and its
"why" are written down, not the paperwork around it.

## Earned extras (only when they add something)

- `status` frontmatter:
  `proposed | accepted | deprecated | superseded by ADR-NNNN`
- **Considered options** — when the rejected paths will matter later.
- **Consequences** — when the fallout is non-obvious.

## Bar for writing one

All three must hold, or there is no ADR:

1. Reversing it later would cost real effort.
2. A future reader would ask "why on earth this way?".
3. Genuine alternatives were on the table.
```

- [ ] **Step 4: Validate**

Run: `grep -c '^name: grilling-session' plugins/working-process/skills/grilling-session/SKILL.md`
Expected: `1`

Run: `grep -c 'przemagluj' plugins/working-process/skills/grilling-session/SKILL.md`
Expected: `1` (bilingual trigger present)

Run: `ls plugins/working-process/skills/grilling-session/`
Expected: `ADR-FORMAT.md  GLOSSARY-FORMAT.md  SKILL.md`

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/skills/grilling-session/
git commit -m "feat(working-process): add grilling-session skill"
```

---

### Task 3: architect-session skill

**Files:**
- Create: `plugins/working-process/skills/architect-session/SKILL.md`

**Interfaces:**
- Consumes: `${CLAUDE_PLUGIN_ROOT}/PERSONA.md` (Task 1); skill name `grilling-session` (Task 2) and agent name `architect` (Task 4) in handoffs.

- [ ] **Step 1: Write `plugins/working-process/skills/architect-session/SKILL.md`**

```markdown
---
name: architect-session
description: In-session consultation with the architect persona — interactive design discussion with domain expertise and glossary duty. Use ONLY when the developer explicitly asks to talk to the architect ("ask the architect", "porozmawiajmy z architektem", "architect session"); generic design questions belong to brainstorming. A formal review with a verdict is the architect agent's job, never this skill's.
---

Consultation mode of the architect persona. FIRST ACTION: read
`${CLAUDE_PLUGIN_ROOT}/PERSONA.md` and adopt it fully — both duties and
the glossary/ADR duty (glossary before anything else).

## Running the session

- A live design conversation in the main thread: question the design,
  weigh alternatives, sketch options — steered by the persona's
  design-quality dimensions.
- Being interactive, you may simply ask the developer which domains
  matter instead of only inferring them.
- One topic at a time; take a position on every question discussed.

## Hard limits

- NO verdict and NO `architect:` stamping — those belong exclusively to
  an `architect` agent dispatch; the dispatch's fresh context, unbiased
  by this conversation, is precisely its value.
- Never rewrite the developer's documents unasked.

## Handing off

As decisions settle, point at the right next step:

- new or changed domain terms/decisions → a grilling-session (it records
  the glossary/ADR updates);
- a document ready for formal review → an `architect` agent dispatch,
  with a domain hint from this session.
```

- [ ] **Step 2: Validate**

Run: `grep -c '\${CLAUDE_PLUGIN_ROOT}/PERSONA.md' plugins/working-process/skills/architect-session/SKILL.md`
Expected: `1`

Run: `grep -c 'porozmawiajmy z architektem' plugins/working-process/skills/architect-session/SKILL.md`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add plugins/working-process/skills/architect-session/
git commit -m "feat(working-process): add architect-session skill"
```

---

### Task 4: architect agent

**Files:**
- Create: `plugins/working-process/agents/architect.md`

**Interfaces:**
- Consumes: `${CLAUDE_PLUGIN_ROOT}/PERSONA.md` (Task 1).
- Produces: agent name `architect` and verdict vocabulary `LGTM | concerns | blocking` with threshold `blocking = ≥1 Critical or ≥2 Important` (reused verbatim by Task 5).

- [ ] **Step 1: Write `plugins/working-process/agents/architect.md`**

```markdown
---
name: architect
description: "Architect reviewing design quality — a grilled spec (primary target) or any design document or question dispatched standalone. Domain expertise is inferred from the subject (a dispatch hint is verified, otherwise self-inferred) and declared up front. Verdict LGTM | concerns | blocking; the dispatcher stamps it into the reviewed document's architect: frontmatter field. Not for failure-mode hunting on plans — that is plan-adversary."
---

Formal review mode of the architect persona. FIRST ACTION: read
`${CLAUDE_PLUGIN_ROOT}/PERSONA.md` and adopt it fully; per its glossary
duty, read `docs/domain/glossary.md` and `docs/domain/adr/` right after
the persona, before any judgement.

## Domains — hybrid inference

- The dispatch prompt MAY carry a domain hint. Check it against the
  subject's content and the repo's markers (e.g. `sfdx-project.json`
  marks a Salesforce project); add any domain the dispatcher missed.
- No hint → infer the domains yourself from the same signals.
- Questions mid-run are impossible, so declare instead: every report
  opens with an **Assumed domains** section — each domain, where it came
  from (hint / inferred), and your confidence, stated in plain words when
  low. A wrong inference must be visible at the top of the report and
  cheap to fix by a re-dispatch with a corrected hint.

## Report

1. **Assumed domains** — see above.
2. **Findings** — one per issue: severity, section, a one-sentence claim,
   evidence (`file:line`, a quote from the subject, a documentation URL,
   or a glossary/ADR entry), and a suggestion. No filler, no style nits,
   no claims without a citation.
3. **Verdict** — `LGTM | concerns | blocking`; `blocking` = at least one
   Critical or two Important findings.
4. A few sentences of overall architectural opinion.

Severity is measured in design terms: `Critical` — the design cannot
deliver its stated purpose, or overrides a recorded decision without
naming and superseding it; `Important` — a boundary or choice that forces
rework if built as designed; `Minor` — naming, clarity, convention.

## Stamping

The dispatcher (not this agent) writes the verdict into the `architect:`
frontmatter field of any reviewed document that follows the frontmatter
convention (a YAML block with a `status` field) — spec and plan alike. A
bare question has nothing to stamp. The `architect-session` consultation
skill never writes this field — it is stamped only after THIS agent's
review.

## Out of bounds

- Failure-mode hunting on plan mechanics (named tests, commit messages,
  rollout) — plan-adversary owns that.
- Rewriting the reviewed document.
- Padding the findings list or grading style.
```

- [ ] **Step 2: Validate**

Run: `grep -c '^name: architect$' plugins/working-process/agents/architect.md`
Expected: `1`

Run: `grep -c '\${CLAUDE_PLUGIN_ROOT}/PERSONA.md' plugins/working-process/agents/architect.md`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add plugins/working-process/agents/architect.md
git commit -m "feat(working-process): add architect review agent"
```

---

### Task 5: plan-adversary agent

**Files:**
- Create: `plugins/working-process/agents/plan-adversary.md`

**Interfaces:**
- Consumes: agent name `architect` (Task 4) for the decline-specs pointer; verdict vocabulary and thresholds from Task 4, verbatim.
- Produces: the `*-plan-review` discovery convention documented for Task 6's README.

- [ ] **Step 1: Write `plugins/working-process/agents/plan-adversary.md`**

```markdown
---
name: plan-adversary
description: Adversarial reviewer for implementation plans. Hunts the most likely ways the plan is wrong, mis-scoped, or will break silently. Loads domain *-plan-review checklist skills for the domains the plan touches. Severity-graded findings with evidence. Use before implementing any non-trivial plan. Specs are out of scope — design review of a spec belongs to the architect agent.
---

Adversarial reviewer of implementation plans — the last gate before code.
Your deliverable is the punch list: the ways this plan regresses,
mis-scopes, or breaks without anyone noticing. Do not rewrite it. Do not
soften it.

FIRST ACTION: read `docs/domain/glossary.md` and `docs/domain/adr/` when
they exist. Canonical terms bind your wording, and a plan contradicting a
glossary term or a recorded ADR is a finding (evidence = that file).

## Ground rules

- Every finding cites evidence: `file:line`, a quote from the plan, a
  skill/reference path, or a domain `ruleId`.
- Severity `Critical | Important | Minor`. Generic scale: Critical = data
  loss, security, production outage, broken deploy; Important = breaks a
  mandatory standard with no immediate runtime failure; Minor = style,
  naming, docs. When a domain checklist assigns a severity to its rule,
  that severity wins — never re-grade it.
- One finding per issue. No filler. No claims without a citation.

## Domain checklists

Scan the available skills for names matching `*-plan-review`. For every
domain the plan touches — judged from its content and the repo's markers
(e.g. `sfdx-project.json` → Salesforce) — load the matching checklist and
walk its dimensions with the same rigor as the generic ones below.
Domains without a checklist get the generic dimensions only.

## Specs: decline

Handed a spec (a design document, not an implementation plan)? Decline
the review and point the dispatcher at the `architect` agent. Plan
mechanics — named tests, per-phase commits, concrete paths — do not apply
to a design document and would misfire as findings.

## Generic dimensions — walk every one; nothing passes by default

### 1. Scope against done-when

- Does every phase advance some "done when"? A phase mapped to none is
  scope creep.
- Is every "done when" delivered by some phase? A gap is Important.
- Refactors or future-proofing beyond the task → Minor, unless they
  widen the blast radius.

### 2. Verification

- The plan names the specific tests/checks it will run and where they
  execute — a bare "covered by tests" fails this dimension. New behavior
  without a named test → Important.
- A verification step that never exercises the changed path → finding.

### 3. Backwards compatibility

- Consumers of whatever the plan changes: enumerated? informed?
  migrated?
- Mixed-version windows during rollout addressed?

### 4. Plan smells

- Vague phase titles ("clean up", "improve") with no concrete file paths
  → finding.
- Phases without commit messages → finding.
- Unrelated changes bundled into one phase → split; Minor unless severe.
- Hard questions deferred to "we'll figure it out during implementation"
  → never approve.
- Finally ask: *if this ships exactly as written and still breaks, what
  broke?* Name it — the plan should have pre-empted it. Record it as a
  finding.

## Output

    {
      "verdict": "LGTM" | "concerns" | "blocking",
      "findings": [
        {
          "severity": "Critical" | "Important" | "Minor",
          "section": "<plan section or null>",
          "claim": "<one sentence>",
          "evidence": "<file:line | plan quote | ruleId | skill reference path>",
          "suggestion": "<the change to make>"
        }
      ]
    }

`blocking` = ≥1 Critical or ≥2 Important — revise before building.
`concerns` = worth surfacing, not blocking. `LGTM` = no findings.

## Stamping

The dispatcher (not this agent) writes the verdict into the `adversary:`
frontmatter field of any reviewed plan that follows the frontmatter
convention (a YAML block with a `status` field). A plan without the
convention gets no stamp.

## Out of bounds

- Rewriting the plan.
- Duplicating what mechanical gates already enforce (linters, analyzers
  on changed lines) — assume they run.
- Style nits.
- Approving a plan that defers hard questions to implementation time.
```

- [ ] **Step 2: Validate**

Run: `grep -c '^name: plan-adversary$' plugins/working-process/agents/plan-adversary.md`
Expected: `1`

Run: `grep -c -- '-plan-review' plugins/working-process/agents/plan-adversary.md`
Expected: `2` (description and the discovery section, none elsewhere)

- [ ] **Step 3: Commit**

```bash
git add plugins/working-process/agents/plan-adversary.md
git commit -m "feat(working-process): add plan-adversary review agent"
```

---

### Task 6: Plugin README

**Files:**
- Create: `plugins/working-process/README.md`

**Interfaces:**
- Consumes: component names and contracts from Tasks 1–5 exactly as defined there.

- [ ] **Step 1: Write `plugins/working-process/README.md`**

```markdown
# working-process

Tech-agnostic tooling for a spec-driven working process on top of the
`superpowers` plugin:

idea → brainstorming (spec) → grilling-session → architect review →
writing-plans (plan) → plan-adversary → implementation.

## Components

- **`grilling-session` skill** — stress-tests a spec (the primary
  target), plan, or raw idea against the project's domain glossary
  (`docs/domain/glossary.md`), sharpens terminology, and records
  decisions as ADRs. Triggers: "grill me" / "przemagluj".
- **`architect` agent** — formal design-quality review of a grilled spec
  or any design document dispatched standalone; verdict
  `LGTM | concerns | blocking`, stamped into the reviewed document's
  `architect:` frontmatter field by the dispatcher.
- **`architect-session` skill** — the same persona as an interactive
  in-session consultation: no verdict, no stamping; hands off to a
  grilling-session or an `architect` dispatch. Triggers: "ask the
  architect" / "porozmawiajmy z architektem".
- **`plan-adversary` agent** — adversarial review of implementation
  plans (plans only; handed a spec it declines toward the `architect`
  agent). Generic failure-mode dimensions live here; domain specifics
  come from `*-plan-review` checklist skills.

The architect persona is single-sourced in [PERSONA.md](./PERSONA.md),
shared by the `architect` agent and the `architect-session` skill. Every
component reads `docs/domain/glossary.md` and `docs/domain/adr/` first,
when they exist, so it speaks the project's language from its first
message.

## Requirements

- Claude Code ≥ 2.1.143.
- The `superpowers` plugin — declared as a dependency and installed
  automatically alongside this plugin.

## Extending with a domain checklist

Ship a skill named `<domain>-plan-review` in your domain plugin. Its
description starts with `Plan-review checklist for <domain>` and ends
with `invoked by the plan-adversary agent`. plan-adversary discovers the
skill by name and walks its dimensions whenever a reviewed plan touches
that domain — e.g. a `salesforce-plan-review` skill for Salesforce
projects. Domains without a checklist get the generic dimensions only.

## Frontmatter process fields

Stamped only in documents that open with a YAML frontmatter block
containing a `status` field:

| Field | Values | Meaning |
|---|---|---|
| `status` | `draft → approved → implemented` | document lifecycle |
| `grilled` | `grilling` \| ISO date | session open / all outcomes applied |
| `architect` | `LGTM` \| `concerns` \| `blocking` | latest architect verdict |
| `adversary` | `LGTM` \| `concerns` \| `blocking` | latest plan-adversary verdict |

Find unfinished work:

    rg -l '^grilled: grilling' docs/
    rg -l '^architect: (blocking|concerns)' docs/
    rg -l '^adversary: (blocking|concerns)' docs/

## Process directories

The one directory this plugin creates in a project repo is
`docs/domain/` (glossary + ADRs). On first creation the developer is
asked whether it should be git-ignored (a `.gitignore` containing `*`)
or committed; an existing directory's state is respected without asking.
```

- [ ] **Step 2: Validate**

Run: `grep -c 'grilling-session\|architect-session\|plan-adversary' plugins/working-process/README.md | awk '{print ($1>=3) ? "ok" : "missing components"}'`
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add plugins/working-process/README.md
git commit -m "docs(working-process): add plugin README"
```

---

### Task 7: Marketplace registration

**Files:**
- Modify: `.claude-plugin/marketplace.json` (replace whole file; current content has an empty `plugins` array)
- Modify: `README.md` (repo root — plugin table row)

**Interfaces:**
- Consumes: plugin name and description from Task 1.

- [ ] **Step 1: Replace `.claude-plugin/marketplace.json` with**

```json
{
  "name": "missing-bits",
  "owner": { "name": "Jacek Nakonieczny" },
  "description": "Missing Bits marketplace of Claude Code plugins",
  "allowCrossMarketplaceDependenciesOn": ["claude-plugins-official"],
  "plugins": [
    {
      "name": "working-process",
      "source": "./plugins/working-process",
      "description": "Spec-driven working process on top of superpowers: grilling-session and architect-session skills plus architect and plan-adversary review agents"
    }
  ]
}
```

- [ ] **Step 2: Update the plugin table in the repo `README.md`**

Replace:

```markdown
| Plugin | Description |
|--------|-------------|
| _(none yet)_ | |
```

with:

```markdown
| Plugin | Description |
|--------|-------------|
| `working-process` | Spec-driven working process: grilling-session and architect-session skills, architect and plan-adversary review agents |
```

- [ ] **Step 3: Validate**

Run: `jq -e '(.allowCrossMarketplaceDependenciesOn == ["claude-plugins-official"]) and (.plugins[0].name == "working-process") and (.plugins[0].source == "./plugins/working-process")' .claude-plugin/marketplace.json`
Expected: `true`

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/marketplace.json README.md
git commit -m "feat: register working-process in the marketplace"
```

---

### Task 8: End-to-end verification

**Files:**
- Modify: `docs/specs/2026-07-13-working-process-plugin-design.md` (frontmatter `status` only, after checks pass)

**Interfaces:**
- Consumes: everything above; runs the spec's Verification section.

- [ ] **Step 1: Structural validation**

Run: `claude plugin validate .` (from the repo root; if the subcommand is unavailable in the installed CLI version, skip — steps 2–3 cover the same ground end-to-end)
Expected: validation passes, no errors.

- [ ] **Step 2: Isolate from any same-named plugin**

The spec's Non-goals rule out coexistence of two plugins named `working-process`. Before installing, in the verification Claude Code session run `/plugin` and check the installed list: if a `working-process` plugin from any other marketplace is present, uninstall it (and remove its marketplace if no longer needed) — or run the whole verification under a clean profile (fresh `CLAUDE_CONFIG_DIR`).
Expected: no `working-process` plugin installed before Step 3.

- [ ] **Step 3: Install from the local marketplace (interactive Claude Code session)**

In a Claude Code session:
1. `/plugin marketplace add <local path to the claude-plugins repo root>`
2. `/plugin install working-process@missing-bits`

Expected: install succeeds; superpowers is auto-resolved as a dependency (or already present).

- [ ] **Step 4: Component visibility and persona resolution**

In the same session:
1. Confirm skills `working-process:grilling-session` and `working-process:architect-session` appear in the available-skills list.
2. Confirm agents `working-process:architect` and `working-process:plan-adversary` appear among available agent types (plugin agents surface under the plugin namespace), and that they come from `working-process@missing-bits` — no other same-named plugin is installed after Step 2.
3. Dispatch the `working-process:architect` agent with a trivial design question (e.g. "Review this idea: a single-file TODO CLI in Python").
Expected: the agent adopts the persona and its report opens with an **Assumed domains** section.

- [ ] **Step 5: First-create question behavior**

In a scratch git repo (e.g. under the session scratchpad):
1. Start a grilling-session on a raw idea; when it first writes to `docs/domain/`, it MUST ask ignored mode vs tracked mode.
2. Re-run in a repo where `docs/domain/.gitignore` (containing `*`) already exists: it MUST NOT ask and must operate in ignored mode.
3. Re-run in a repo where `docs/domain/glossary.md` is git-tracked: it MUST NOT ask and must operate in tracked mode.
4. Re-run in a repo where `docs/domain/` exists but has neither a `.gitignore` nor any git-tracked file: it MUST ask, as on first creation.
Expected: exactly the above; any deviation is a bug in Task 2's SKILL.md wording — fix and re-run.

- [ ] **Step 6: Mark the spec implemented and commit the process documents**

In `docs/specs/2026-07-13-working-process-plugin-design.md`, change frontmatter `status: approved` to `status: implemented`. Then commit all process documents of this work — the repo's `docs/` directories are in tracked mode by the developer's decision:

```bash
git add docs/specs/2026-07-13-working-process-plugin-design.md docs/plans/2026-07-13-working-process-plugin.md docs/domain/glossary.md
git commit -m "docs: add working-process spec, plan, and domain glossary"
```
