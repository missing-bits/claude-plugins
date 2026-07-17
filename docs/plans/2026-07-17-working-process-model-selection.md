---
ticket: none
date: 2026-07-17
status: implemented
adversary: LGTM
branch: feature/model-selection-guidance
base: master
---

# Model-Selection Dispatch Guidance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved spec
`docs/specs/2026-07-16-working-process-model-selection-design.md` — tier
heuristics, cap protocol, fallback-record grammar, re-review offers, and
dispatch verification for the working-process plugin's two review agents.

**Architecture:** Pure content changes to one plugin: two agent
definitions gain a dispatch directive and a model self-report, two
Rules-payload rules gain the heuristic/protocol and the frontmatter
grammar, the README documents both, and the plugin version bump delivers
the update. No scripts, hooks, or engine changes.

**Tech Stack:** Markdown + YAML frontmatter; `claude` CLI for validation;
`rg` for grep-contract checks.

## Global Constraints

- Public repo hygiene: English only, no machine paths, no company names
  (`.claude/rules/repo-hygiene.md`).
- Commits: one line, conventional-commit subject, no body, no trailers
  (`.claude/rules/commit-messages.md`).
- Frontmatter safety: quote any scalar containing `: `; `claude plugin
  validate` does NOT check `rules/` files — hand-check their YAML
  (`.claude/rules/plugin-authoring.md`).
- Naming discipline (spec "Tier heuristic" / "Fallback record"):
  guidance prose uses abstract tier language; family aliases (`haiku`,
  `sonnet`, `opus`, `fable`) appear only as illustrative examples or in
  record grammars; raw platform model IDs never appear in committed
  text.
- Committed examples of the bare fallback form must use placeholders
  (`<model>`, `<date>`) so they never match the pending grep.
- Version bump rides the same PR as the content changes
  (`.claude/rules/plugin-versioning.md`).

---

### Task 1: architect agent — dispatch directive + model self-report

**Files:**
- Modify: `plugins/working-process/agents/architect.md`

**Interfaces:**
- Produces: the `description:` directive text and the self-report
  convention ("family plus version") that Tasks 3–5 reference.

- [x] **Step 1: Append the dispatch directive to `description:`**

In the frontmatter, the quoted `description:` currently ends with:
`Not for failure-mode hunting on plans — that is plan-adversary."`
Replace that ending with:
`Not for failure-mode hunting on plans — that is plan-adversary. Dispatch on the most capable available model."`

- [x] **Step 2: Add the model self-report to the Report section**

The `## Report` section currently begins:

```markdown
## Report

1. **Assumed domains** — see above.
```

Insert a preamble line so it reads:

```markdown
## Report

The report opens with a one-line **model self-report** — the model this
review actually ran on, as family plus version (e.g. "opus 4.8") —
before any section; the dispatcher compares it against the dispatched
and prescribed tiers before stamping.

1. **Assumed domains** — see above.
```

- [x] **Step 3: Validate**

Run: `claude plugin validate plugins/working-process`
Expected: PASS (frontmatter parses; description quoted).

- [x] **Step 4: Commit**

```bash
git add plugins/working-process/agents/architect.md
git commit -m "feat(working-process): dispatch tier directive and model self-report in architect agent"
```

### Task 2: plan-adversary agent — dispatch directive + model self-report

**Files:**
- Modify: `plugins/working-process/agents/plan-adversary.md`

**Interfaces:**
- Produces: the scaled-dispatch directive text reused in Task 3 and the
  `"model"` output key consumed by dispatchers.

- [x] **Step 1: Append the dispatch directive to `description:`**

The `description:` currently ends with:
`Specs are out of scope — design review of a spec belongs to the architect agent.`
Replace that ending with:
`Specs are out of scope — design review of a spec belongs to the architect agent. Dispatch on a model scaled to the plan's size and risk — most capable for complex or risky plans, one family below for small mechanical ones; never the cheapest family.`

- [x] **Step 2: Add the `"model"` key to the Output JSON**

The `## Output` block is a 4-space-indented code block that currently
opens:

```
    {
      "verdict": "LGTM" | "concerns" | "blocking",
```

Keep the real indentation (4 spaces for the braces, 6 for keys) and
change it to:

```
    {
      "model": "<family plus version this review actually ran on, e.g. opus 4.8>",
      "verdict": "LGTM" | "concerns" | "blocking",
```

- [x] **Step 3: Validate**

Run: `claude plugin validate plugins/working-process`
Expected: PASS.

- [x] **Step 4: Commit**

```bash
git add plugins/working-process/agents/plan-adversary.md
git commit -m "feat(working-process): dispatch tier directive and model self-report in plan-adversary agent"
```

### Task 3: workflow rule — heuristic in steps 3/5 + cap protocol

**Files:**
- Modify: `plugins/working-process/rules/workflow.md`

**Interfaces:**
- Consumes: directive wording from Tasks 1–2 (keep it consistent).
- Produces: the "model selection" paragraph that Task 5's README section
  summarizes.

- [x] **Step 1: Extend step 3 (architect dispatch)**

Current step 3 ends:
`stamp its verdict into the spec's ``architect:`` frontmatter field.`
Append one sentence:
`Dispatch it on the most capable available model, named explicitly.`

- [x] **Step 2: Extend step 5 (adversary dispatch)**

Current step 5 ends:
`stamp its verdict into the plan's ``adversary:`` field.`
Append one sentence:
`Dispatch it on a model scaled to the plan's size, complexity, and risk — the most capable available for complex or risky plans, one family below for small mechanical ones — named explicitly.`

- [x] **Step 3: Add the model-selection paragraph**

After the existing paragraph that begins `After every architect or
plan-adversary round, record the verdict`, insert:

```markdown
Model selection for these dispatches: always name the model explicitly —
an omitted model inherits the session's model, defeating the heuristic
in both directions. Reviews are never dispatched on the cheapest
available family. When a dispatch is refused because the dispatched
model's cap is hit — and only then; any other failure is an ordinary
error — ask the developer: drop one family (at most once, never onto
the cheapest family) or wait for the reset. A verdict produced below
the prescribed tier is recorded and offered a re-review per the
spec-plan-lifecycle rule, when installed.
```

- [x] **Step 4: Hand-check the rule's YAML and validate**

`rules/workflow.md` has no frontmatter block today — confirm none was
added. Run: `claude plugin validate plugins/working-process`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add plugins/working-process/rules/workflow.md
git commit -m "feat(working-process): model-selection heuristic and cap protocol in workflow rule"
```

### Task 4: spec-plan-lifecycle rule — fallback grammar + re-review offer

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md`

**Interfaces:**
- Consumes: the token grammar and offer semantics verbatim from the
  spec's "Fallback record" and "Re-review offer" sections.
- Produces: the grep line Task 5's README block repeats.

- [x] **Step 1: Extend the frontmatter example**

After the `adversary: LGTM` line in the YAML example, add:

```yaml
architect-fallback: <model> (degraded <date>)   # optional: verdict above produced below the prescribed tier (adversary-fallback: for plans)
```

- [x] **Step 2: Add the fallback bullets**

After the existing resolved-concerns bullet (`Concerns resolved without
a fresh review round…`), insert three bullets:

```markdown
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
  gate — before plan-writing for a spec, before implementation for a
  plan. Accepted: a fresh round at the prescribed tier replaces the
  verdict and removes the field (a fresh round that is itself below the
  prescribed tier refreshes the field's date instead, and the offer
  re-arms at the same gate). Declined: the field gains `, waived <date>`.
  Moving `status` to `implemented` with a bare fallback field stamps the
  waiver as part of the move.
- Review agents self-report the model they ran on (family plus version);
  the dispatcher compares it against the dispatched and prescribed
  tiers before stamping, and each round's verdict, model, and date are
  recorded in the document body. Committed examples of the bare fallback form use
  placeholders (as above) so they never match the grep below.
```

- [x] **Step 3: Extend the grep list**

After the existing
`rg -l '^(architect|adversary): (blocking|concerns)$' docs/` line, add:

```
rg -l '^(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/
```

with the note: `— pending re-reviews; the waived annotation deliberately
defeats the anchor.`

- [x] **Step 4: Extend the lifecycle-offers paragraph**

The paragraph `Lifecycle offers — each an offer the developer may
decline…` lists three offers. Append a fourth:
`offer the pending re-review of a fallback-recorded verdict at its
consumption gate (fresh round at the prescribed tier).`

- [x] **Step 5: Hand-check YAML frontmatter**

The rule's `paths:` block must be unchanged and parseable; the new
example line lives inside a fenced code block, so it cannot break the
frontmatter. Visually confirm.

- [x] **Step 6: Grep-contract check**

Run: `rg -l '^(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' plugins/ docs/`
Expected: no hits (the example uses `<model>`/`<date>` placeholders and
is indented inside a YAML block).

- [x] **Step 7: Commit**

```bash
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): fallback field and re-review offer in spec-plan-lifecycle rule"
```

### Task 5: README — document the convention

**Files:**
- Modify: `plugins/working-process/README.md`

**Interfaces:**
- Consumes: field grammar from Task 4, heuristic wording from Task 3.

- [x] **Step 1: Extend the frontmatter fields table**

In "## Frontmatter process fields", after the `adversary` row, add:

```markdown
| `architect-fallback` / `adversary-fallback` | `<model> (degraded <date>)` \| `<model> (chosen <date>)` \| `…, waived <date>` | verdict produced below the prescribed tier (`degraded` = unchosen, `chosen` = deliberate); re-review pending until re-reviewed or waived |
```

- [x] **Step 2: Extend the unfinished-work grep block**

Add to the existing block:

```
rg -l '^(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/
```

- [x] **Step 3: Add the "Model selection" subsection**

Directly after the frontmatter-fields section (before "## Process
rules"), insert:

```markdown
## Model selection

The architect is dispatched on the most capable available model; the
plan-adversary on a model scaled to the plan's size and risk — most
capable for complex or risky plans, one family below for small
mechanical ones. The model is always named explicitly at dispatch, and
reviews never dispatch on the cheapest available family. A dispatch
refused on the dispatched model's cap offers a one-family drop (once)
or waiting for the reset; a verdict produced below the prescribed tier
gets a fallback record and a re-review offer — grammar and lifecycle in
the spec-plan-lifecycle rule. Agents self-report the model they ran on
(family plus version) so the dispatcher can verify before stamping.
```

- [x] **Step 4: Extend the two agent bullets in Components**

- Architect bullet: after `stamped into the reviewed document's
  ``architect:`` frontmatter field by the dispatcher.` append
  `Dispatched on the most capable available model.`
- Plan-adversary bullet: after `domain specifics come from
  ``*-plan-review`` checklist skills.` append `Dispatched scaled to the
  plan's size and risk.`

- [x] **Step 5: Commit**

```bash
git add plugins/working-process/README.md
git commit -m "docs(working-process): document model selection and fallback convention"
```

### Task 6: version bump + final verification

**Files:**
- Modify: `plugins/working-process/.claude-plugin/plugin.json`

**Interfaces:**
- Consumes: everything above; nothing after depends on this task.

- [x] **Step 1: Bump the version**

In `plugins/working-process/.claude-plugin/plugin.json`, change
`"version": "0.5.0"` to `"version": "0.6.0"`.
(0.5.0 shipped with review-reports — confirmed on master after the
2026-07-17 rebase; 0.6.0 is the next minor above every already-released
working-process version. Re-verify at merge time if master moves again.
The plugin `description` is unchanged, so no marketplace.json /
repo-README sync is needed.)

- [x] **Step 2: Full validation**

Run: `claude plugin validate . && claude plugin validate plugins/working-process`
Expected: both PASS.

- [x] **Step 3: Grep sweep**

```bash
rg -l '^(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/ plugins/
rg -i 'capped verdict|lowered verdict|backup model|replacement model|model level|usage point|voluntary degradation|sub-tier record' plugins/working-process/
rg -n 'claude-(fable|opus|sonnet|haiku)-' plugins/working-process/ || true
```

Expected: first — no hits (no false positives for the pending grep);
second — no hits (no glossary-banned phrases); third — no hits (no raw
model IDs in committed plugin text).

- [x] **Step 4: Commit**

```bash
git add plugins/working-process/.claude-plugin/plugin.json
git commit -m "chore(working-process): bump version to 0.6.0 for model-selection release"
```

## Done when (spec coverage)

- Both agents: directive in `description:`, model self-report in the
  report/output (Tasks 1–2) — spec "Carriers", "Dispatch verification".
- Workflow rule: heuristic at steps 3/5, cap protocol paragraph
  (Task 3) — spec "Tier heuristic", "Cap protocol".
- Lifecycle rule: fallback grammar (both tokens), re-review offer with
  gates/waiver/recursion, round provenance, pending grep (Task 4) —
  spec "Fallback record", "Re-review offer", "Round provenance".
- README: table row, grep, Model selection section, agent bullets
  (Task 5).
- Version bump delivers the update (Task 6).
- Out of scope, per the spec: superpowers guidance, sync-rules engine,
  proactive budgeting, auto-retry after cap reset.

## Adversary findings (round 1, 2026-07-17)

Verdict: `concerns` (opus 4.8, 2026-07-17 — dispatched and prescribed
mid tier, no fallback event) — five Minor fidelity/coverage findings.
All five applied 2026-07-17 in the same sync that carried the spec's
delta-grilling outcome into Task 4 (regrilled token boundary: `chosen`
= deliberate only, `degraded` = everything else):

1. Task 2 Step 2 quotes the plan-adversary Output block at column 0;
   the real block is 4-space indented — quote it with real indentation.
2. Task 1 Step 2 / Task 4 bullet 3 say the dispatcher compares the
   self-report "against the dispatched tier" only; the spec says
   "against the dispatched and prescribed tiers" — restore both halves.
3. README table row uses `<family>` where the canonical example uses
   `<model>` — align on `<model>`.
4. Task 6's merge-time version rule covers only the "abandoned" case;
   restate as "take the next minor above every already-released
   working-process version at merge time" so a delayed review-reports
   is not stranded.
5. End-to-end verification exercises only the plan-adversary; add a
   one-line architect dispatch (or justify the asymmetry).

Cleared as non-findings by the reviewer: "Downgrade after approval" is
explanatory, not rule text (no coverage gap); the frontmatter-example
comment sits in a fenced block (no parse risk); the `_Avoid_` sweep
covers the new text.

## Adversary findings (round 2, 2026-07-17)

Verdict: `concerns` (opus 4.8, 2026-07-17 — dispatched and prescribed
mid tier, no fallback event) — one Minor. All five round-1
dispositions verified as applied; Task 4 verified faithful to the
regrilled spec; edit anchors match the current files; grep contract
triple-protected. Applied 2026-07-17:

1. **Minor — the Task 6 glossary-ban sweep omitted the newest `_Avoid_`
   term "sub-tier record"** — the banned phrase most likely to surface
   in the Fallback-record text Task 4 writes. Disposition: applied —
   added to the `rg -i` alternation.

## Adversary verdict (round 3, 2026-07-17)

`LGTM` (opus 4.8, 2026-07-17 — dispatched and prescribed mid tier, no
fallback event) — no findings. Round-2 disposition verified as applied;
the plan needs no sync from the spec's round-10/11 summary-site fixes
(Task 4 already encodes their substance); all edit anchors verified
against the current files; grep contract triple-protected.

## Close-out (2026-07-17)

Implemented via subagent-driven execution, one reviewed task at a time.
Task 6 landed as 0.6.0 → **0.7.0**, not the scripted 0.5.0 → 0.6.0:
master released 0.6.0 mid-flight (prompt-free report filenames), the
branch was rebased, and the merge-time rule in Task 6 governed exactly
as written. Final whole-branch review: READY TO MERGE, no blocking
findings.

## Verification (end-to-end)

After all tasks: dispatch a working-process plan-adversary agent on any
small plan with an explicitly named mid-tier model and confirm (a) its
output opens with the `"model"` key carrying family plus version, and
(b) the dispatcher-side compare finds no mismatch. Also dispatch a
working-process architect agent on any small standalone design question
with an explicitly named model and confirm its report opens with the
family-plus-version self-report — `claude plugin validate` checks only
frontmatter, so the report-body carrier needs this live check. The
degradation/re-review path was already exercised during the spec's own
review rounds 3–4.
