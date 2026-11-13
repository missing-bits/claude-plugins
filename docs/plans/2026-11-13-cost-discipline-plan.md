---
ticket: none
date: 2026-11-13
status: approved
spec: ../specs/2026-11-13-cost-discipline-spec.md
branch: feature/cost-discipline
base: develop
---

# Cost discipline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the working-process reviewers and the session's triage ask whether a mechanism is worth having, and block only on Critical findings.

**Architecture:** Prose edits to one shared persona file, two agent cards, the workflow rule and the repo glossary. No script, no settings key, no new file. Each task edits one file and ends with a grep that proves the change landed and the replaced text is gone.

**Tech Stack:** Markdown agent cards and rules of a Claude Code plugin; `rg`, `claude plugin validate`.

**Spec:** `docs/specs/2026-11-13-cost-discipline-spec.md` — read its *A mechanism*, *Reviewers*, *Triage*, *Verdict threshold*, *Before drafting*, *Dropped stays dropped* and *Net growth* sections before the task that realizes them. Paths below are relative to the repository root; `plugins/working-process/` is abbreviated `wp/`.

## Global Constraints

- All committed text is English; no machine paths, no company or client names (repo-hygiene rule).
- Commit messages: one conventional-commit line, no body, no trailer.
- Rule text names skills and agents conditionally ("when the X agent is available").
- Every edited prose passage gets an elements-of-style pass when that skill is available; the pass changes wording, never decisions.
- The definition of a mechanism is worded identically in `wp/PERSONA_COMMON.md` and `wp/rules/workflow.md`: "A fix adds a mechanism when it introduces something the document did not have: a part, a task, a command, an option or flag, a state file or field, or a recovery path. Giving an existing part a new check, branch or case adds one too, whichever way it moves what the part accepts. Rewording, correcting a value, deleting text, removing an input, option or case, and adding a test or a verification step that brings no new command or script add none."
- Documents with `status: implemented` keep their wording; only live rules, cards and glossary entries change.
- Implementation commits go to `feature/cost-discipline`. The spec's per-round commits sit on `feature/cost-discipline.docs`; merging that branch into the topic branch happens at the implementation-ready gate, before Task 1.

## Review Focus

1. **A card read without the rules installed.** The architect and the plan-adversary must still have the definition and the non-goal sentence: both live in `PERSONA_COMMON.md`, which both cards reach. Task 1 checks the reach.
2. **Consultation personas read `PERSONA_COMMON.md` too.** The added text must not tell a consult agent to hold, grade or block anything. Task 1's wording addresses reviewers only.
3. **A dispatch with no reviewed document** (an architect question). No size line, and the relay shows no size. Task 4 states it.
4. **A previous record with no `size:` line** (every record written before this change). The relay shows the size without a change. Task 4 states it.
5. **A fix that carries out a developer's `ruling:`.** It must not be held a second time by D4. Task 4 states the exemption.

---

### Task 1: Shared persona text — definition and settled non-goals

**Files:**
- Modify: `wp/PERSONA_COMMON.md` (opening paragraph, and a new section after *The boundary between the personas*)

**Interfaces:**
- Produces: the section heading `## Cost discipline`, which Tasks 2 and 3 point to by name.

**Realizes:** D9


- [ ] **Step 1: Add `## Cost discipline` before `## The consultation contract`**, holding two paragraphs, both addressed to reviewers:
  - the definition, verbatim from Global Constraints;
  - non-goals: a design spec's non-goals are settled; a finding that would reintroduce one says what new evidence it brings, new against the spec's own text.
- [ ] **Step 2: Update the self-description in the opening paragraphs.** "the two duties below" and "All four sections" must match the file after Step 1; the new section is a section, not a duty — recount and reword so both counts are true.
- [ ] **Step 3: Verify.**
  Run: `rg -n '^## ' wp/PERSONA_COMMON.md; rg -c 'A fix adds a mechanism when' wp/PERSONA_COMMON.md; sed -n 1,12p wp/PERSONA_COMMON.md`
  Expected: five `## ` headings including `## Cost discipline`; count `1`; every count in the opening paragraphs matches the heading list just printed.
- [ ] **Step 4: Verify the reach.**
  Run: `rg -n 'PERSONA_COMMON' wp/agents/plan-adversary.md wp/ARCHITECT_PERSONA.md`
  Expected: one line in each file.
- [ ] **Step 5: Commit** — `git commit -m "feat(working-process): cost-discipline section in the shared persona file"`

### Task 2: Architect card — cheaper alternative, threshold, Critical scale

**Files:**
- Modify: `wp/agents/architect.md` (*Report* list, item 2 and item 3; the severity paragraph after it)

**Interfaces:**
- Consumes: `## Cost discipline` in `wp/PERSONA_COMMON.md` (Task 1).

**Realizes:** D1, D6, D12


- [ ] **Step 1: Findings (item 2).** Add: where a finding's suggestion adds a mechanism (definition in `PERSONA_COMMON.md`, *Cost discipline*), the finding names at least one cheaper alternative beside it — narrowing the input, the tool's native behaviour, accepting the gap as a documented limitation, or deferring it.
- [ ] **Step 2: Verdict (item 3).** Replace "`blocking` = at least one Critical or two Important findings" with "`blocking` = at least one Critical finding". The sentence wraps across two lines in the card.
- [ ] **Step 3: Critical.** Extend the Critical definition to also cover a stated requirement the design does not meet, and a data-loss or security defect. Leave Important and Minor unchanged.
- [ ] **Step 4: Verify.**
  Run: `rg -n -U 'two\s+Important' wp/agents/architect.md; rg -n 'at least one Critical finding' wp/agents/architect.md; rg -n 'cheaper alternative' wp/agents/architect.md; rg -n -i 'security defect' wp/agents/architect.md`
  Expected: the first prints nothing; each of the other three prints one line.
- [ ] **Step 5: Commit** — `git commit -m "feat(working-process): architect blocks on Critical only and names cheaper alternatives"`

### Task 3: Plan-adversary card — cheaper alternative, threshold, undelivered requirements

**Files:**
- Modify: `wp/agents/plan-adversary.md` (*Ground rules* severity bullet; dimensions 1, 5 and 6; *Output* verdict line)

**Interfaces:**
- Consumes: `## Cost discipline` in `wp/PERSONA_COMMON.md` (Task 1).

**Realizes:** D1, D6, D7


- [ ] **Step 1: Ground rules.** Add the same cheaper-alternative sentence as Task 2 Step 1, plus: the finding also names the requirement that forces the mechanism, with `origin: design-spec`, and proposes no change to that document (the card's *Judged documents: decline* boundary stands).
- [ ] **Step 2: Critical scale.** In the generic scale, add "a requirement the plan does not deliver" to Critical.
- [ ] **Step 3: Regrade exactly three findings from Important to Critical:** dimension 1 "Is every 'done when' delivered by some phase? A gap is Important."; dimension 5 "An uncovered part is an Important finding"; dimension 6 "A decision realized only in part … is an Important finding". The other Important findings in dimension 5 stay Important.
- [ ] **Step 4: Verdict line.** Replace "`blocking` = ≥1 Critical or ≥2 Important" with "`blocking` = ≥1 Critical".
- [ ] **Step 5: Verify.**
  Run: `rg -n '2 Important' wp/agents/plan-adversary.md; rg -n 'A gap is Critical|uncovered part is a Critical|only in part.*Critical' wp/agents/plan-adversary.md; rg -c 'is an Important finding' wp/agents/plan-adversary.md; rg -n 'cheaper alternative' wp/agents/plan-adversary.md`
  Expected: the first prints nothing; the second prints three lines (a wrapped sentence may need `-U`); the count equals the count on `develop` minus two (`git show develop:plugins/working-process/agents/plan-adversary.md | rg -c 'is an Important finding'`); the last prints one line.
- [ ] **Step 6: Commit** — `git commit -m "feat(working-process): plan-adversary blocks on Critical only and grades undelivered requirements Critical"`

### Task 4: Workflow rule — definition, triage hold, brief, dispatch record size

**Files:**
- Modify: `wp/rules/workflow.md` (step 1; *Dispatching a verdict agent* bullets on the dispatch record, the relay header and the decision count; *The review loop* triage paragraph; *Re-dispatch briefs*)

**Realizes:** D2, D4, D5, D8, D11

- [ ] **Step 1: Step 1 of the flow (D8).** After the consult-persona sentences, add: while drafting a design spec, before its first review, the session asks the developer for a size target, what is dropped, what native behaviour already covers and which risks are accepted, and writes the answers into the spec's non-goals and constraints — no separate brief file.
- [ ] **Step 2: Triage (D4, D5).** After the paragraph opening "Triage decides each finding by its license", add the definition (verbatim, Global Constraints) and: a fix that adds a mechanism is held whatever its severity and whether or not a license exists; not held again when it carries out a `ruling:`, nor when it is a propagation-gate hit's fix; held when the session cannot tell. Its `options:` recommend the smaller option where it meets the requirements and always include "accept as a documented limitation".
- [ ] **Step 3: Decision count (D4).** In the bullet "The header's count of decisions is the findings for which the session can cite no license", add the fixes the cost hold catches, so the count still matches the round's `held` lines.
- [ ] **Step 4: Dispatch record (D11).** In the bullet that says "under a four-line header — the date, the agent, the model self-report, and the subject", list the fields instead of counting them and add `size: <lines>` where a document was reviewed: the body's line count without the `## Review rounds` section, from `sed '1,/^---$/d' <file> | awk '/^## Review rounds/{s=1;next} /^## /{s=0} !s' | wc -l`.
- [ ] **Step 5: Relay header (D11).** In the bullet "The relay opens with one header line", add the size and the change since the previous record of the same document and agent; no size without a reviewed document; no change when no earlier record carries a `size:` line; the relay judges nothing.
- [ ] **Step 6: Re-dispatch briefs (D2).** After "directs the reviewer to attack the previous wave's fixes first", add: including whether a fix added a mechanism its finding did not need.
- [ ] **Step 7: Verify.**
  Run: `rg -n 'four-line' wp/rules/workflow.md; rg -c 'A fix adds a mechanism when' wp/rules/workflow.md; rg -n 'size: <lines>' wp/rules/workflow.md; rg -n 'documented limitation' wp/rules/workflow.md; rg -n -i 'size target' wp/rules/workflow.md`
  Expected: the first prints nothing; count `1`; each of the others at least one line.
- [ ] **Step 8: Verify the size command** on the spec: `sed '1,/^---$/d' docs/specs/2026-11-13-cost-discipline-spec.md | awk '/^## Review rounds/{s=1;next} /^## /{s=0} !s' | wc -l` prints a number below `wc -l` of the file, and `rg -c '^## Review rounds' docs/specs/2026-11-13-cost-discipline-spec.md` prints `1`.
- [ ] **Step 9: Commit** — `git commit -m "feat(working-process): cost hold in triage, size in relays, brief while drafting"`

### Task 5: Glossary — relay header and dispatch record

**Files:**
- Modify: `docs/domain/glossary.md` (*Relay* and *Dispatch record* entries)

**Realizes:** D11

- [ ] **Step 1:** *Relay* — the header also carries the document's size and its change where a document was reviewed.
- [ ] **Step 2:** *Dispatch record* — replace "a four-line header (date, agent, model self-report, subject)" with the field list plus "size, where a document was reviewed".
- [ ] **Step 3: Verify.** Run: `rg -n 'four-line' docs/domain/glossary.md` — Expected: nothing. No *Mechanism* entry is added (spec, *A mechanism*).
- [ ] **Step 4: Commit** — `git commit -m "docs: glossary relay and dispatch record carry size"`

### Task 6: Changelog, validation, dogfood version and dogfood

**Files:**
- Modify: `wp/CHANGELOG.md`, `wp/.claude-plugin/plugin.json`, `.claude/working-process/release-queue.md` (local, not committed)

**Realizes:** none

- [ ] **Step 1: Changelog.** Add `## Unreleased` at the top with one bullet per user-visible change: Critical-only `blocking` in both cards; undelivered requirements Critical in the plan-adversary; the architect's Critical covers unmet requirements, data loss and security; cheaper alternatives in findings; the cost hold in triage; size in relays and dispatch records; the drafting question.
- [ ] **Step 2: Dogfood version.** Set `"version": "0.20.0-dev.5.cost-discipline"` (the highest on `develop` is `-dev.4.`).
- [ ] **Step 3: Validate.** Run: `claude plugin validate . && claude plugin validate plugins/working-process` — Expected: both pass. Run: `rg -n -U 'two\s+Important|≥2 Important' plugins/` — Expected: nothing.
- [ ] **Step 4: Commit** — `git commit -m "chore(working-process): changelog and dogfooding version for cost discipline"`
- [ ] **Step 5: Dogfood, plan-adversary.** With the plugin loaded from this checkout and its rules synced, dispatch the plan-adversary on the ai-devcontainer v2 plan as it stood at its first round (in the developer's ai-devcontainer checkout). Expected: no `blocking` verdict; every finding whose fix adds a mechanism names a cheaper alternative and, where a requirement forces it, the requirement. Record the result in `.claude/working-process/2026-11-13-cost-discipline-spec/dogfood.md`.
- [ ] **Step 6: Dogfood, loop.** On a scratch spec seeded with (a) a Minor whose natural fix adds a task and (b) a design-level security defect, run one architect round and triage it. Expected: (a) is held with the smaller option recommended; (b) is Critical and the verdict `blocking`; the relay header shows the size. Record in the same file.
- [ ] **Step 7: Release queue.** Mark 2b-core implemented with the commit range in `.claude/working-process/release-queue.md`.
