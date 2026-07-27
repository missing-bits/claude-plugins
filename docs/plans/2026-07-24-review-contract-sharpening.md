---
ticket: "#10"
date: 2026-07-24
status: implemented
adversary: concerns (resolved 2026-07-24)
branch: feature/10-contract-sharpening
base: develop
---

# Review-report contract sharpening — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land the six contract decisions of
`docs/specs/2026-07-23-review-contract-sharpening-design.md` (grilled,
architect LGTM) across the review-reports contract, the
process-artifacts rule, both code-review skills, and both review
commands.

**Architecture:** Pure documentation/rule edits — no code. The
contract owns report shape and citation semantics; the
process-artifacts rule owns the first-create signal list; each skill's
cascade and inline fallback mirror only what the spec assigns them;
the commands become background dispatchers carrying the self-contained
pre-dispatch check. Every task is a set of exact text edits plus grep
verification.

**Tech Stack:** Markdown, `claude plugin validate`, `rg`/`grep`.

## Global Constraints

- Work in the `feature/10-contract-sharpening` worktree
  (`.claude/worktrees/contract-sharpening/`), branched off `develop`.
- NO version bumps on this branch (plugin-versioning rule: bumps land
  at the develop→master release PR). Task 9 mints `-dev.10`
  prerelease strings for dogfooding — that is not a release bump.
- The authoring rubric stays verbatim in exactly its four existing
  places (repo rule `.claude/rules/standards-rule-tags.md`, the
  contract, both inline fallbacks) — no task edits any rubric copy's
  three severity bullets.
- No new report frontmatter fields; `findings:` keeps its three keys.
- `.claude/rules/standards-rule-tags.md` is NOT edited.
- Commit messages: ONE line, conventional-commit subject, no body, no
  trailers (repo commit-messages rule).
- Public-repo hygiene: English, no machine paths, no client names.
- All `git`/file commands run from the worktree root
  (`.claude/worktrees/contract-sharpening/`).
- **Line-wrapping rule for edits:** NEVER rewrap any line of a
  replacement block — the verification greps are single-line matchers
  and every replacement block below is pre-wrapped so each grep
  phrase sits on one line. Apply replacement texts byte-exact.

## Review rounds

Adversary round 1 (2026-07-24, Fable 5): **blocking** — three
Important (verification arithmetic: phrases wrapped across line breaks
defeat single-line greps in Tasks 3/5/6/7; `rg -n | wc -l` counts
lines, not matches) and three Minor (Task 4 verify passing by
accident, contract referencing the declared-instruction signal one
commit before the rule defines it, empirical check unowned). All
amended: phrases unwrapped (line-wrapping rule above), verifications
switched to per-phrase `rg -c` checks, process-artifacts task moved
BEFORE the contract task, and the dogfooding gate added with explicit
pass criteria. Content edits were verified faithful (old-strings
byte-exact, agents exist, versions match).

Adversary round 2 (2026-07-24, Fable 5): **blocking** — three
Important (the dogfooding gate verified only the plugin cache while
the contract is read from the INSTALLED rule file, synced by content
hash — a stale contract would misattribute failures; the
declared-instruction signal forked in two remaining restatement
surfaces, grilling-session and the project-memory core rule; the
fallback `## Project` parenthetical dropped "same severity
subsections", letting a standalone shape drift) and three Minor
(glossary Contract probe term names only skills as probe runners; the
line-wrapping constraint listed four phrases instead of banning all
rewrapping; the gate rerun did not require launch via the review
command). All amended: sync-rules step and command-launch requirement
in the gate (Task 10), grilling-session reference in Task 2,
project-memory restatement as new Task 8, "same severity subsections"
in Tasks 4/6, Contract probe term extension in Task 1, blanket
no-rewrap constraint. Spec and its Review rounds updated to match
(post-LGTM amendments, no new decisions).

Adversary round 3 (2026-07-24, Fable 5): **concerns** — one Important
(the gate's conditional pass criteria could be vacuously satisfied by
a target that never triggers the new report paths) and four Minor
(zero-match audit grep exits 1 without `|| true`; both skills'
`description:` still named the command as invoker; the commands'
`mode: agent` parenthetical was unconditional, contradicting the
Standalone fallback; "at least one rerun" could ship one command
unexercised). Resolved same day without a fresh round: Task 10 now
requires one rerun per rewritten command with at least one target
whose prior report has file-less and `rule: none` findings, and Step 5
records exercised vs vacuous criteria; `|| true` added in Task 9;
description invoker-chain edits added to Tasks 4/6; the parenthetical
qualified "under the installed contract". Byte-exactness of all
old-strings and all grep arithmetic confirmed clean this round.

Dogfooding gate round 1 (2026-07-27, Task 10): five reruns across
five projects plus two first-run session transcripts. Passed: the
command path (contract probe, pre-dispatch first-create check,
background dispatch with a live session and task-notification
summary), single-rule citations in all reports, justify-not-critical
clauses, rerun dispositions with the convention boundary, the
first-review path, and the full candidate-gap reply machinery
(verbatim proposals, store probes, degraded upstream, consent gates).
Failed, two layers: reviewer agents folded systemic multi-file
violation classes into project-level findings (three targets — twice
self-chosen, once mandated by an aggregation instruction the
dispatching session added to the dispatch prompt on its own), one
rerun carried the prior report's counting convention forward for
comparability, and one report annotated `rule: none` citations with
"candidate gap, see reply". Fixes: three explicit bans appended to
both code-review skills' step 4, and a dispatch-prompt constraint
appended to both commands' step 3. Gate re-runs per Step 5; the
systemic-aggregation design tension is parked as a Private-memory
idea for a future family decision.

Dogfooding gate rounds 2–3 (2026-07-27). Round 2: the command-layer
constraint held (both dispatch prompts clean, shown by the
developer), but reruns exposed a loophole — the reviewer inherited
the prior report's counting-policy section, including its
now-stale claim about what the dispatch asked; fixed by sharpening
the rerun ban in both skills (no counting-policy/finding-unit-note
inheritance, no alleged prior-dispatch instructions, an unchanged
tree does not change the unit). Round 3, both commands: PASS on all
criteria. The python rerun unfolded the mechanical classes
(81→210 findings, boundary declared non-comparable, the
toolchain-config finding correctly kept project-level with
violations per file); the salesforce rerun — against a prior report
that was aggregated AND carried the stale dispatch claim — quoted
the ban, refused inheritance, re-derived every finding from source
(53→540, three corrections to the prior run), and ran on the
inherited session model, isolating the text effect. Residual risks
for the PR description: the first-create ask-path was never
exercised (every target already carried a decision signal), and the
python round-3 agent was explicitly dispatched on a stronger model
by its session (the salesforce round-3 run covers the weaker tier).
Gate: PASSED.

---

### Task 1: Commit the process documents

The spec and glossary changes already sit uncommitted in this
worktree (moved from the design session). This is the
implementation-ready gate — they ride ahead of the content commits.

**Files:**
- Commit (already modified): `docs/domain/glossary.md`
- Commit (already created):
  `docs/specs/2026-07-23-review-contract-sharpening-design.md`
- Commit (already created):
  `docs/plans/2026-07-24-review-contract-sharpening.md`

**Interfaces:**
- Produces: committed spec/plan/glossary that later tasks' texts
  mirror (glossary terms **Finding**, **Candidate gap**,
  **First-create question**).

- [ ] **Step 1: Verify the three files are the only dirty paths**

Run: `git status --short`
Expected: exactly `M docs/domain/glossary.md`,
`?? docs/specs/2026-07-23-review-contract-sharpening-design.md`,
`?? docs/plans/2026-07-24-review-contract-sharpening.md`.

- [ ] **Step 2: Flip the spec's status to approved**

In `docs/specs/2026-07-23-review-contract-sharpening-design.md`
frontmatter, change `status: draft` → `status: approved` (the plan
exists and the developer approved proceeding; the plan file's own
status flips at its adversary gate, not here).

- [ ] **Step 3: Extend the glossary Contract probe term**

In `docs/domain/glossary.md`, in the **Contract probe** term, replace:

```markdown
**Contract probe**:
The ordered path check a domain review skill runs to find the installed
report contract:
```

with:

```markdown
**Contract probe**:
The ordered path check a domain review skill — or a dispatching
review command, pre-dispatch — runs to find the installed
report contract:
```

- [ ] **Step 4: Commit**

```bash
git add docs/domain/glossary.md docs/specs/2026-07-23-review-contract-sharpening-design.md docs/plans/2026-07-24-review-contract-sharpening.md
git commit -m "docs(working-process): spec, plan, and glossary for review-contract sharpening"
```

---

### Task 2: `plugins/working-process/rules/process-artifacts.md` —
declared-instruction signal

Runs BEFORE the contract task so the contract's cross-reference to
the declared-instruction signal resolves at every commit boundary.

**Files:**
- Modify: `plugins/working-process/rules/process-artifacts.md`
- Modify: `plugins/working-process/skills/grilling-session/SKILL.md`

**Interfaces:**
- Produces: the owned signal list (three signals + materialization)
  that the contract and grilling-session reference (Task 3 Step 5,
  this task's Step 3) and the commands and project-memory core rule
  restate self-contained (Tasks 5, 7, 8).

- [ ] **Step 1: Extend the ask condition and add the third signal**

Replace:

```markdown
When creating a Process directory — or touching one that already exists
with no observable prior decision (neither a `.gitignore` containing
exactly `*` nor any git-tracked file under it) — ASK the developer which
mode the directory gets. Assume no default:
```

with:

```markdown
When creating a Process directory — or touching one that already exists
with no prior decision (no `.gitignore` containing exactly `*`, no
git-tracked file under it, and no explicit project instruction
declaring the mode) — ASK the developer which mode the directory gets.
Assume no default:
```

- [ ] **Step 2: Add the declared-decision paragraph with
  materialization**

Replace:

```markdown
Never ask when either signal is already present: only a `.gitignore`
containing exactly `*` means ignored mode was chosen — one with any
other content (e.g. a local pocket's `local-*`) signals nothing by
itself; a git-tracked file under the directory (`git ls-files <dir>`
non-empty) means tracked mode was chosen.
```

with:

```markdown
Never ask when any signal is already present: only a `.gitignore`
containing exactly `*` means ignored mode was chosen — one with any
other content (e.g. a local pocket's `local-*`) signals nothing by
itself; a git-tracked file under the directory (`git ls-files <dir>`
non-empty) means tracked mode was chosen; and an
explicit project instruction declaring the mode (e.g. a CLAUDE.md
note that a directory is always git-ignored) counts as the decision.
A declared ignored mode is materialized by whoever first acts on it —
writing the `*` `.gitignore` — making the decision observable; a
declared tracked mode becomes observable with the first committed
file. This rule owns the signal list; other surfaces reference it
rather than restating it (a self-contained command restatement is the
one justified exception).
```

- [ ] **Step 3: Close the grilling-session fork — reference the
  owned list**

In `plugins/working-process/skills/grilling-session/SKILL.md`,
replace:

```markdown
- The directory already exists? Never ask when a prior decision is
  observable: a `.gitignore` with `*` means ignored mode; any
  git-tracked file under it (`git ls-files docs/domain` non-empty) means
  tracked mode. Neither signal present? No decision was ever made — ask,
  exactly as on first creation.
```

with:

```markdown
- The directory already exists? Never ask when a prior decision is
  present — the decided signals (observable marks and the
  declared-instruction signal, with its materialization duty) are
  owned by the working-process process-artifacts rule; consult it. No
  signal present? No decision was ever made — ask, exactly as on
  first creation.
```

- [ ] **Step 4: Verify (per-phrase counts)**

```bash
rg -c "explicit project instruction" plugins/working-process/rules/process-artifacts.md
rg -c "materialized" plugins/working-process/rules/process-artifacts.md
rg -c "owned by the working-process process-artifacts rule" plugins/working-process/skills/grilling-session/SKILL.md
```
Expected: 2, then 1, then 1.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/rules/process-artifacts.md plugins/working-process/skills/grilling-session/SKILL.md
git commit -m "feat(working-process): declared-instruction signal with materialization in first-create convention"
```

---

### Task 3: Contract — `plugins/working-process/rules/review-reports.md`

All contract-owned decisions: finding unit + `## Project` (D1), rerun
disposition + self-describing boundary (D1), single citation (D2),
plugin-level `rule: none` + mixed-run routing (D3),
justify-not-critical (D4), candidate-gap marker (D5), background
dispatch sentence (D6).

**Files:**
- Modify: `plugins/working-process/rules/review-reports.md`

**Interfaces:**
- Consumes: the signal list from Task 2 (referenced, not restated).
- Produces: the contract text Tasks 4–7 mirror. Key phrases later
  tasks grep for: "one violation class in one file",
  "`## Project`", "counts as remaining", "exactly one rule id",
  "falls short of critical", "only candidate-gap marker",
  "never blocks an interactive dispatching session".

- [ ] **Step 1: Layout — finding unit and `## Project` section**

Replace:

```markdown
1. **Summary** — outcome, out-of-scope notes, and (for a rerun) the
   prior findings' disposition.
2. **Per-file sections**, each with **Critical → Important → Minor**
   subsections; findings within a subsection in ascending line order.
   Findings without a line anchor — files reviewed from metadata
   rather than source lines — are ordered by a domain-stated stable
   key: the reviewing domain names the key (e.g. cited element name,
   alphabetically) and applies it consistently.
```

with:

```markdown
1. **Summary** — outcome, out-of-scope notes, and (for a rerun) the
   prior findings' disposition.
2. **`## Project` section**, present only when needed, always FIRST —
   before the per-file sections: the home of findings not
   attributable to an existing file (a missing lockfile, an absent
   manifest). Same severity subsections as a file section; findings
   ordered by rule id, `rule: none` findings last, ordered by
   violation-class name.
3. **Per-file sections**, each with **Critical → Important → Minor**
   subsections; findings within a subsection in ascending line order.
   Findings without a line anchor — files reviewed from metadata
   rather than source lines — are ordered by a domain-stated stable
   key: the reviewing domain names the key (e.g. cited element name,
   alphabetically) and applies it consistently.

A finding is one violation class in one file (or at project level):
for tagged rules the rule id names the class; for `rule: none`
findings the class is the one the candidate-gap offer names. The
finding's body enumerates every violating site — line numbers, or the
domain's stable key where lines do not apply — and the finding
anchors and sorts by its first violating site. One location violating
two rules yields two findings. `findings:` counts therefore mean: the
number of (violation class, file-or-project) pairs to fix.
```

- [ ] **Step 2: `rerun-of` — site disposition and convention boundary**

Replace:

```markdown
  re-reviews, resolved among reports of the SAME scope — runids are
  model-generated and not globally unique, so the scope, not the runid
  alone, carries the identification. When set, the run's owner reads
  that report and notes the prior findings' disposition in Summary —
  fixed / remaining / new.
```

with:

```markdown
  re-reviews, resolved among reports of the SAME scope — runids are
  model-generated and not globally unique, so the scope, not the runid
  alone, carries the identification. When set, the run's owner reads
  that report and notes the prior findings' disposition in Summary —
  fixed / remaining / new. Disposition tracks sites within a finding
  ("lines 42, 87 fixed; 130 remaining"); a partially fixed finding
  counts as remaining — a finding lives until its last site is fixed.
  Reports are self-describing (they may live git-ignored or in an
  archive outside the repo): rerun behavior never depends on anything
  unreadable from the reports themselves. When the prior report's
  findings do not follow the finding unit (a pre-convention report,
  readable off the report itself), the Summary disposition says so
  and maps prior findings best-effort; count deltas across that
  boundary are not comparable.
```

- [ ] **Step 3: Finding citations — single citation, plugin-level
  `rule: none`, justify clause**

Replace:

```markdown
- A finding that violates a defined rule cites its most specific id:
  `(standard: <skill>, rule: <id>)` — the sub-id when a sub-rule
  matched, the group id otherwise. When a matching rule exists, the
  specific id is mandatory; a bare `(standard: <skill>)` citation is
  not a valid finding.
- A finding no defined rule covers is still reported and counted:
  cited `(standard: <the loaded domain skill that lacks the rule>,
  rule: none)`, graded by the authoring rubric below, and — when graded
  critical — always `kind: defect` (hardening denotes a
  standards-mandated protection, and a `rule: none` finding has no
  standard mandating it). A plausible-looking rule id is never
  fabricated.
```

with:

```markdown
- A finding that violates a defined rule cites its most specific id:
  `(standard: <skill>, rule: <id>)` — the sub-id when a sub-rule
  matched, the group id otherwise. When a matching rule exists, the
  specific id is mandatory; a bare `(standard: <skill>)` citation is
  not a valid finding. A finding cites exactly one rule id — singular
  `rule:` key; its severity is the cited rule's.
- A finding no defined rule covers is still reported and counted:
  cited `(standard: <the loaded domain skill that lacks the rule>,
  rule: none)` — or, when no skill of the plugin covers the concern,
  at plugin level: `(standard: <plugin-name>, rule: none)`. A concern
  covered by the domain of an existing but not-yet-loaded skill is
  NOT a candidate gap — the reviewer loads that skill and grades by
  its tags; `rule: none` is never asserted against a skill the run
  did not read. In a mixed run the cited plugin is the one whose
  domain owns the finding's file; a project-level finding routes by
  its violation-class domain. Graded by the authoring rubric below;
  when graded critical — always `kind: defect` (hardening denotes a
  standards-mandated protection, and a `rule: none` finding has no
  standard mandating it); when graded below critical while touching
  data integrity, security or sharing, or a platform limit — the
  finding states in one clause why it falls short of critical. A
  plausible-looking rule id is never fabricated.
```

- [ ] **Step 4: Candidate-gap offers — marker sentence and new-skill
  proposals**

Replace:

```markdown
`rule: none` findings are candidate standards gaps. After writing the
report, the run's owner lists them in its reply — one line each:
violation class, proposed rule id, graded severity — and then offers,
never performs unprompted:
```

with:

```markdown
`rule: none` findings are candidate standards gaps. The `rule: none`
citation is the report's only candidate-gap marker; the proposals
live in the run's reply, never in the report. After writing the
report, the run's owner lists them in its reply — one line each:
violation class, proposed rule id, graded severity (a plugin-level
`rule: none` finding may propose a new skill instead of a new rule) —
and then offers, never performs unprompted:
```

- [ ] **Step 5: Dispatcher bullet — background dispatch and signal
  reference**

Replace:

```markdown
- Dispatching a reviewer agent from an interactive session: the
  dispatcher runs the first-create check BEFORE dispatch and asks then
  — exactly as when the process creates `docs/specs/` or `docs/plans/`
  — so the agent never meets an undecided directory.
```

with:

```markdown
- Dispatching a reviewer agent from an interactive session: the
  dispatcher runs the first-create check BEFORE dispatch and asks then
  — exactly as when the process creates `docs/specs/` or `docs/plans/`
  — so the agent never meets an undecided directory. The decided
  signals (including the declared-instruction signal) are owned by
  the process-artifacts rule. The dispatch itself runs in the
  background: a review never blocks an interactive dispatching
  session, and the run's owner writes the one report regardless of
  fore/background mode.
```

- [ ] **Step 6: Verify (per-phrase counts)**

```bash
f=plugins/working-process/rules/review-reports.md
rg -c "one violation class in one file" $f   # expected: 1
rg -c "counts as remaining" $f               # expected: 1
rg -c "exactly one rule id" $f               # expected: 1
rg -c "falls short of critical" $f           # expected: 1
rg -c "only candidate-gap marker" $f         # expected: 1
rg -c "never blocks an interactive" $f       # expected: 1
rg -c "## Project" $f                        # expected: 1
```

- [ ] **Step 7: Commit**

```bash
git add plugins/working-process/rules/review-reports.md
git commit -m "feat(working-process): finding unit, citation rules, and background dispatch in review-reports contract"
```

---

### Task 4: `plugins/python-standards/skills/python-code-review/SKILL.md`

Cascade mirrors D3 + D4; Run-scope boundary replaces the
out-of-scope-note sentence; fallback absorbs the finding unit,
single citation, and `## Project`.

**Files:**
- Modify: `plugins/python-standards/skills/python-code-review/SKILL.md`

**Interfaces:**
- Consumes: contract phrases from Task 3 (mirrored, not referenced —
  the cascade must work standalone).
- Produces: the cascade text Task 6 parallels for salesforce.

- [ ] **Step 1: Extend the `rule: none` cascade bullet (D3 + D4)**

Replace:

```markdown
   - no defined rule covers the finding → report and count it anyway,
     cited `(standard: <the loaded skill that lacks the rule>,
     rule: none)`, graded by the authoring rubric in the review-reports
     contract; at critical its kind is always `defect`. Never invent a
     rule id.
```

with:

```markdown
   - no defined rule covers the finding → report and count it anyway,
     cited `(standard: <the loaded skill that lacks the rule>,
     rule: none)` — or `(standard: python-standards, rule: none)` when
     no skill of this plugin covers the concern. A concern covered by
     the domain of an existing but not-yet-loaded skill is NOT a
     candidate gap: load that skill and grade by its tags —
     `rule: none` is never asserted against a skill the run did not
     read. Graded by the authoring rubric in the review-reports
     contract; at critical its kind is always `defect`; when graded
     below critical while touching data integrity, security or
     sharing, or a platform limit, the finding states in one clause
     why it falls short of critical. Never invent a rule id.
```

- [ ] **Step 2: Single citation + Run-scope boundary (D2 + D3)**

Replace:

```markdown
   When a matching rule exists, citing its specific id is mandatory —
   a bare `(standard: <skill>)` citation is not a valid finding.
   Critical findings carry the rule's kind inline
   (`…, kind: defect|hardening`); the Summary headline breaks critical
   counts down by kind. Content matching no loaded domain skill stays a
   Summary out-of-scope note, not a finding.
```

with:

```markdown
   When a matching rule exists, citing its specific id is mandatory —
   a bare `(standard: <skill>)` citation is not a valid finding. A
   finding cites exactly one rule id; one location violating two
   rules yields two findings. Critical findings carry the rule's kind
   inline (`…, kind: defect|hardening`); the Summary headline breaks
   critical counts down by kind. The Run scope is given by the caller
   and never self-extended: within it, a Python-domain concern no
   rule covers is a counted `rule: none` finding (cascade above);
   files outside the domain (Run scope section) stay Summary
   out-of-scope notes.
```

- [ ] **Step 3: Fallback Body — finding unit and `## Project`**

Replace:

```markdown
- **Body**: a Summary section (scope reviewed, out-of-scope files,
  headline counts), then per-file sections with Critical → Important →
  Minor subsections, line-ascending within a subsection; omit
  no-findings files and empty severity sections; a zero-findings run
  still writes the document.
```

with:

```markdown
- **Body**: a Summary section (scope reviewed, out-of-scope files,
  headline counts); a `## Project` section FIRST when findings are
  not attributable to an existing file (same severity subsections as
  a file section; ordered by rule id, `rule: none` last by
  violation-class name); then per-file sections
  with Critical → Important → Minor subsections, line-ascending
  within a subsection; omit no-findings files and empty severity
  sections; a zero-findings run still writes the document. A finding
  is one violation class in one file (or at project level), its body
  enumerating every violating site, anchored by its first site; it
  cites exactly one rule id.
```

- [ ] **Step 4: Update the `description:` invoker chain**

After Task 5 the command no longer loads this skill — the agent does.
In the frontmatter, replace:

```markdown
description: Use when auditing existing Python code against the python-standards skills — invoked by the /python-review command or the python-code-reviewer agent.
```

with:

```markdown
description: Use when auditing existing Python code against the python-standards skills — invoked by the python-code-reviewer agent, which the /python-review command dispatches in the background.
```

- [ ] **Step 5: Verify (per-phrase counts)**

```bash
f=plugins/python-standards/skills/python-code-review/SKILL.md
rg -c "Content matching no loaded domain skill" $f || true  # expected: no output (0 matches)
rg -c "one violation class in one file" $f   # expected: 1
rg -c "exactly one rule id" $f               # expected: 2
rg -c "falls short of critical" $f           # expected: 1
rg -c "## Project" $f                        # expected: 1
rg -c "dispatches in the background" $f      # expected: 1
```

- [ ] **Step 6: Commit**

```bash
git add plugins/python-standards/skills/python-code-review/SKILL.md
git commit -m "feat(python-standards): plugin-level rule-none, justify clause, and finding unit in review cascade"
```

---

### Task 5: `plugins/python-standards/commands/python-review.md` —
background dispatcher

**Files:**
- Modify: `plugins/python-standards/commands/python-review.md`

**Interfaces:**
- Consumes: `python-code-reviewer` agent
  (`plugins/python-standards/agents/python-code-reviewer.md`, exists);
  probe paths owned by the contract; signal list owned by
  process-artifacts (both restated self-contained here by design).

- [ ] **Step 1: Rewrite the command body**

Replace the whole body (everything after the frontmatter):

```markdown
Review Python code against the python-standards skills.

1. Load the `python-code-review` skill and follow it end to end.
2. Scope: `$ARGUMENTS` when given (named files); otherwise the current
   diff — staged plus unstaged changes, or, on a clean tree, the diff of
   the current branch against its base.
3. Python files only (`*.py`, `pyproject.toml`); note out-of-domain
   files in the report Summary as out of scope.
4. Write the review report per the skill's report contract and reply
   as the python-code-review skill specifies (report path, severity
   summary, candidate gaps and offers).
```

with:

```markdown
Review Python code against the python-standards skills by dispatching
the reviewer agent in the background — the review must never block
this session.

1. Resolve the scope: `$ARGUMENTS` when given (named files);
   otherwise the current diff — staged plus unstaged changes, or, on
   a clean tree, the diff of the current branch against its base.
2. Pre-dispatch first-create check, gated on the contract probe:
   check `<project>/.claude/rules/working-process/review-reports.md`,
   then `$HOME/.claude/rules/working-process/review-reports.md` —
   first hit wins (paths owned by the review-reports contract;
   restated here so the command is self-contained). No contract found
   (Standalone install) → skip this step entirely. Contract found and
   `docs/code-review/` carries no decision — no `.gitignore` of
   exactly `*`, no git-tracked file under it, and no
   explicit project instruction declaring the mode (signal list owned
   by the process-artifacts rule) — ask the developer now: ignored or
   tracked mode.
3. Dispatch the `python-code-reviewer` agent in the BACKGROUND with
   the resolved scope. Python files only (`*.py`, `pyproject.toml`);
   the agent notes out-of-domain files in the report Summary as out
   of scope and writes the one report itself (`mode: agent` under the
   installed contract).
4. Tell the developer: the review is running in the background; the
   summary arrives as a task notification, not inline; progress via
   `/tasks`; the report will land under `docs/code-review/`.
5. When the run's notification arrives, relay its reply to the
   developer: report path, findings by severity, and the
   candidate-gap offers verbatim.
```

- [ ] **Step 2: Verify (per-phrase counts)**

```bash
f=plugins/python-standards/commands/python-review.md
rg -c "BACKGROUND" $f              # expected: 1
rg -c "task notification" $f       # expected: 1
rg -c "contract probe" $f          # expected: 1
rg -c "python-code-reviewer" $f    # expected: 1
```

- [ ] **Step 3: Commit**

```bash
git add plugins/python-standards/commands/python-review.md
git commit -m "feat(python-standards): python-review dispatches the reviewer in the background with probe-gated first-create check"
```

---

### Task 6: `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`

Salesforce mirror of Task 4 — same three edits, salesforce texts.

**Files:**
- Modify:
  `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`

**Interfaces:**
- Consumes: contract phrases from Task 3 (mirrored).

- [ ] **Step 1: Extend the `rule: none` cascade bullet (D3 + D4)**

Replace:

```markdown
   - no defined rule covers the finding → report and count it anyway,
     cited `(standard: <the loaded skill that lacks the rule>,
     rule: none)`, graded by the authoring rubric in the review-reports
     contract; at critical its kind is always `defect`. Never invent a
     rule id.
```

with:

```markdown
   - no defined rule covers the finding → report and count it anyway,
     cited `(standard: <the loaded skill that lacks the rule>,
     rule: none)` — or `(standard: salesforce-standards, rule: none)`
     when no skill of this plugin covers the concern. A concern
     covered by the domain of an existing but not-yet-loaded skill is
     NOT a candidate gap: load that skill and grade by its tags —
     `rule: none` is never asserted against a skill the run did not
     read. Graded by the authoring rubric in the review-reports
     contract; at critical its kind is always `defect`; when graded
     below critical while touching data integrity, security or
     sharing, or a platform limit, the finding states in one clause
     why it falls short of critical. Never invent a rule id.
```

- [ ] **Step 2: Single citation + Run-scope boundary (D2 + D3)**

Replace:

```markdown
   When a matching rule exists, citing its specific id is mandatory —
   a bare `(standard: <skill>)` citation is not a valid finding.
   Critical findings carry the rule's kind inline
   (`…, kind: defect|hardening`); the Summary headline breaks critical
   counts down by kind (e.g. "critical: 33 — 12 defect, 21 hardening").
   Content matching no loaded domain skill stays a Summary out-of-scope
   note, not a finding.
```

with:

```markdown
   When a matching rule exists, citing its specific id is mandatory —
   a bare `(standard: <skill>)` citation is not a valid finding. A
   finding cites exactly one rule id; one location violating two
   rules yields two findings. Critical findings carry the rule's kind
   inline (`…, kind: defect|hardening`); the Summary headline breaks
   critical counts down by kind (e.g. "critical: 33 — 12 defect,
   21 hardening"). The Run scope is given by the caller and never
   self-extended: within it, a Salesforce-domain concern no rule
   covers is a counted `rule: none` finding (cascade above); files
   outside the domain (Run scope section) stay Summary out-of-scope
   notes.
```

- [ ] **Step 3: Fallback Body — finding unit and `## Project`**

Replace:

```markdown
- **Body**: a Summary section (scope reviewed, out-of-scope files,
  headline counts), then per-file sections with Critical → Important →
  Minor subsections — line-ascending within a subsection, line-less
  findings alphabetically by cited element name; omit no-findings
  files and empty severity sections; a zero-findings run still writes
  the document.
```

with:

```markdown
- **Body**: a Summary section (scope reviewed, out-of-scope files,
  headline counts); a `## Project` section FIRST when findings are
  not attributable to an existing file (same severity subsections as
  a file section; ordered by rule id, `rule: none` last by
  violation-class name); then per-file sections
  with Critical → Important → Minor subsections — line-ascending
  within a subsection, line-less findings alphabetically by cited
  element name; omit no-findings files and empty severity sections; a
  zero-findings run still writes the document. A finding
  is one violation class in one file (or at project level), its body
  enumerating every violating site, anchored by its first site; it
  cites exactly one rule id.
```

- [ ] **Step 4: Update the `description:` invoker chain**

After Task 7 the command no longer loads this skill — the agent does.
In the frontmatter, replace:

```markdown
description: Use when auditing existing Salesforce code and metadata against the salesforce-standards skills — invoked by the /salesforce-review command or the salesforce-code-reviewer agent.
```

with:

```markdown
description: Use when auditing existing Salesforce code and metadata against the salesforce-standards skills — invoked by the salesforce-code-reviewer agent, which the /salesforce-review command dispatches in the background.
```

- [ ] **Step 5: Verify (per-phrase counts)**

```bash
f=plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md
rg -c "Content matching no loaded domain skill" $f || true  # expected: no output (0 matches)
rg -c "one violation class in one file" $f   # expected: 1
rg -c "exactly one rule id" $f               # expected: 2
rg -c "falls short of critical" $f           # expected: 1
rg -c "## Project" $f                        # expected: 1
rg -c "dispatches in the background" $f      # expected: 1
```

- [ ] **Step 6: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md
git commit -m "feat(salesforce-standards): plugin-level rule-none, justify clause, and finding unit in review cascade"
```

---

### Task 7: `plugins/salesforce-standards/commands/salesforce-review.md`
— background dispatcher

**Files:**
- Modify: `plugins/salesforce-standards/commands/salesforce-review.md`

**Interfaces:**
- Consumes: `salesforce-code-reviewer` agent
  (`plugins/salesforce-standards/agents/salesforce-code-reviewer.md`,
  exists).

- [ ] **Step 1: Rewrite the command body**

Replace the whole body (everything after the frontmatter):

```markdown
Review Salesforce code and metadata against the salesforce-standards
skills.

1. Load the `salesforce-code-review` skill and follow it end to end.
2. Scope: `$ARGUMENTS` when given (named files); otherwise the current
   diff — staged plus unstaged changes, or, on a clean tree, the diff
   of the current branch against its base.
3. Salesforce files only, per the skill's run scope; note
   out-of-domain files in the report Summary as out of scope.
4. Write the review report per the skill's report contract and reply
   as the salesforce-code-review skill specifies (report path, severity
   summary, candidate gaps and offers).
```

with:

```markdown
Review Salesforce code and metadata against the salesforce-standards
skills by dispatching the reviewer agent in the background — the
review must never block this session.

1. Resolve the scope: `$ARGUMENTS` when given (named files);
   otherwise the current diff — staged plus unstaged changes, or, on
   a clean tree, the diff of the current branch against its base.
2. Pre-dispatch first-create check, gated on the contract probe:
   check `<project>/.claude/rules/working-process/review-reports.md`,
   then `$HOME/.claude/rules/working-process/review-reports.md` —
   first hit wins (paths owned by the review-reports contract;
   restated here so the command is self-contained). No contract found
   (Standalone install) → skip this step entirely. Contract found and
   `docs/code-review/` carries no decision — no `.gitignore` of
   exactly `*`, no git-tracked file under it, and no
   explicit project instruction declaring the mode (signal list owned
   by the process-artifacts rule) — ask the developer now: ignored or
   tracked mode.
3. Dispatch the `salesforce-code-reviewer` agent in the BACKGROUND
   with the resolved scope. Salesforce files only, per the skill's
   run scope; the agent notes out-of-domain files in the report
   Summary as out of scope and writes the one report itself
   (`mode: agent` under the installed contract).
4. Tell the developer: the review is running in the background; the
   summary arrives as a task notification, not inline; progress via
   `/tasks`; the report will land under `docs/code-review/`.
5. When the run's notification arrives, relay its reply to the
   developer: report path, findings by severity, and the
   candidate-gap offers verbatim.
```

- [ ] **Step 2: Verify (per-phrase counts)**

```bash
f=plugins/salesforce-standards/commands/salesforce-review.md
rg -c "BACKGROUND" $f                  # expected: 1
rg -c "task notification" $f           # expected: 1
rg -c "contract probe" $f              # expected: 1
rg -c "salesforce-code-reviewer" $f    # expected: 1
```

- [ ] **Step 3: Commit**

```bash
git add plugins/salesforce-standards/commands/salesforce-review.md
git commit -m "feat(salesforce-standards): salesforce-review dispatches the reviewer in the background with probe-gated first-create check"
```

---

### Task 8: `plugins/project-memory/rules/project-memory.md` —
declared-instruction signal restatement

The project-memory core rule owns the `docs/memory/` first-create
question and must stand without working-process — so it restates the
third signal self-contained (the spec's second justified restatement)
instead of referencing the process-artifacts rule.

**Files:**
- Modify: `plugins/project-memory/rules/project-memory.md`

**Interfaces:**
- Consumes: the signal semantics from Task 2 (restated, not
  referenced).

- [ ] **Step 1: Add the declared-instruction signal**

Replace:

```markdown
Never ask when a prior decision is observable: a `.gitignore` containing
exactly `*` means ignored was chosen; any git-tracked file under the
directory means tracked. Private memory (`.claude/memory/`) is always
ignored, so it is never asked.
```

with:

```markdown
Never ask when a prior decision is present: a `.gitignore` containing
exactly `*` means ignored was chosen; any git-tracked file under the
directory means tracked; and an
explicit project instruction declaring the mode (e.g. a CLAUDE.md
note) counts as the decision — a declared ignored mode is
materialized by whoever first acts on it (writing the `*`
`.gitignore`), a declared tracked mode becomes observable with the
first committed file. Private memory (`.claude/memory/`) is always
ignored, so it is never asked.
```

- [ ] **Step 2: Verify (per-phrase counts)**

```bash
f=plugins/project-memory/rules/project-memory.md
rg -c "explicit project instruction" $f   # expected: 1
rg -c "materialized" $f                   # expected: 1
```

- [ ] **Step 3: Commit**

```bash
git add plugins/project-memory/rules/project-memory.md
git commit -m "feat(project-memory): declared-instruction signal in the docs/memory first-create question"
```

---

### Task 9: Cross-file audit, validation, and `-dev.10` prerelease

**Files:**
- Modify: `plugins/working-process/.claude-plugin/plugin.json`
- Modify: `plugins/python-standards/.claude-plugin/plugin.json`
- Modify: `plugins/salesforce-standards/.claude-plugin/plugin.json`

**Interfaces:**
- Consumes: everything above.
- Produces: a branch ready for the dogfooding gate (Task 10) with
  distinct cache version strings.

- [ ] **Step 1: Cross-file consistency audit**

Run each; expected results as noted:

```bash
# The superseded sentence is gone everywhere (rg exits 1 on the
# expected zero matches — the || true keeps the audit green):
rg -l "Content matching no loaded domain skill" plugins/ || true  # no matches
# The rubric is still verbatim in exactly its 3 plugin copies (+ repo rule = 4):
rg -l "corrupts data, breaks security" plugins/ .claude/rules/    # exactly 4 files
# The finding unit is stated in contract + both fallbacks:
rg -l "one violation class in one file" plugins/                  # exactly 3 files
# Both commands background-dispatch:
rg -l "BACKGROUND" plugins/python-standards/commands/ plugins/salesforce-standards/commands/   # exactly 2 files
```

- [ ] **Step 2: Plugin validation**

Run:
```bash
claude plugin validate . && for p in working-process python-standards salesforce-standards; do claude plugin validate plugins/$p; done
```
Expected: all pass. (Run under bash, not zsh — see the #8 ledger
note.)

- [ ] **Step 3: Mint `-dev.10` prerelease versions for dogfooding**

Per the plugin-versioning rule (dogfooding needs a changed version
string; final numbers are minted by the release PR): in each of the
three manifests change only the `version` value —

- `plugins/working-process/.claude-plugin/plugin.json`:
  `"version": "0.11.0"` → `"version": "0.11.0-dev.10"`
- `plugins/python-standards/.claude-plugin/plugin.json`:
  `"version": "0.2.0"` → `"version": "0.2.0-dev.10"`
- `plugins/salesforce-standards/.claude-plugin/plugin.json`:
  `"version": "0.2.0"` → `"version": "0.2.0-dev.10"`

- [ ] **Step 4: Re-validate and commit**

```bash
claude plugin validate .
git add plugins/working-process/.claude-plugin/plugin.json plugins/python-standards/.claude-plugin/plugin.json plugins/salesforce-standards/.claude-plugin/plugin.json
git commit -m "chore: mint -dev.10 prerelease versions for contract-sharpening dogfooding"
```

- [ ] **Step 5: Report**

Reply with the commit list (`git log --oneline develop..HEAD`) and the
audit results from Step 1. Task 10 (dogfooding gate) runs next, with
the developer.

---

### Task 10: Dogfooding gate (with the developer, before the PR to
develop)

The spec's empirical check, owned here. Runs in the developer's
projects — this task is executed together with the developer, who
reloads plugins and launches the review runs; the pass criteria are
checked against the reports they bring back.

**Files:**
- None in this repo (reports land in the reviewed projects).

**Interfaces:**
- Consumes: the `-dev.10` content from Task 9 (distinct cache version
  strings make the reload observable).

- [ ] **Step 1: Developer reloads plugins and verifies the cache**

The plugin cache must show the `-dev.10` directories for the three
plugins. Not observable → stop; dogfooding against stale content
proves nothing.

- [ ] **Step 2: Developer syncs the installed rules and verifies the
  contract**

The reviewer reads the contract from the INSTALLED rule file (content
hash via sync-rules, never plugin version) — a fresh cache does NOT
refresh it. Run the working-process sync-rules skill in the
dogfooding environment, then verify the installed contract carries
the new finding unit:

```bash
rg -c "one violation class in one file" "$HOME/.claude/rules/working-process/review-reports.md"
```
Expected: 1 (or the project-level copy when that is the installed
one). Not present → stop; the run would grade against the stale
contract and misattribute failures to this branch.

- [ ] **Step 3: Developer runs one review rerun per rewritten
  command**

Both commands changed, so both are exercised: one `/python-review`
run and one `/salesforce-review` run, each launched from an
interactive session — the command path is itself under test
(background dispatch, pre-dispatch check) — and each setting
`rerun-of` to its prior report's runid (same scope). Target choice is
NOT free: at least one target must be a codebase whose prior report
contains file-less findings AND `rule: none` findings, so the
`## Project` section, the plugin-level citation, and the justify
clause actually fire (the python codebase whose prior runs invented
two pseudo-file sections for absent-manifest findings qualifies —
see the spec's Motivation). A target that cannot trigger a criterion
leaves it vacuous; Step 5 records that.

- [ ] **Step 4: Check the report against the pass criteria**

All must hold:

- counts follow the finding unit: one finding per violation class per
  file, sites enumerated inside findings (no per-instance explosion,
  no cross-file folding, no self-declared "counting convention"
  section);
- `## Project` section used — first — if any file-less findings exist;
- every finding cites exactly one rule id (no plural `rules:`, no
  multi-id citations);
- any `rule: none` finding below critical touching data integrity,
  security or sharing, or a platform limit carries its one-clause
  justification;
- no "candidate gap" annotations inside the report body (the citation
  is the marker); proposals appear in the run's reply;
- the Summary disposition maps the prior findings and declares the
  pre-convention boundary (the prior report predates the finding
  unit), with count deltas marked non-comparable;
- the dispatching session was not blocked (review ran in the
  background; summary arrived as a task notification).

- [ ] **Step 5: Gate decision**

For each criterion record: exercised-and-passed, exercised-and-failed,
or vacuous (the targets never triggered it). All exercised criteria
pass → open the PR to develop, listing any vacuous criteria in the PR
description as explicitly accepted residual risk. Any criterion fails
→ the failure is a finding against this branch's texts; fix, re-run
this gate.
