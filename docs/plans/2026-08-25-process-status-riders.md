---
ticket: none
date: 2026-08-25
status: implemented
adversary: concerns (resolved 2026-08-25)
branch: feature/process-status-riders
base: develop
spec: ../specs/2026-08-24-process-status-and-anchor-hardening-design.md
---

# Process Status Riders Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the three increments of `docs/specs/2026-08-24-process-status-and-anchor-hardening-design.md` — a `process-status` skill, workflow step 7, and the anchored-sweep hardening — in working-process 0.14.0 plus one project-memory minor.

**Architecture:** The lifecycle rule gains a named `## Unfinished-work list` section whose entries are triples (class, command, owner); the new skill runs exactly what that section publishes and confirms every hit inside a frontmatter block. The workflow rule gains step 7. The store half rewrites one paragraph of the project-memory conventions rule and adds one audit clause to memory-review-session. Content lands first and the dogfood version bump last, so the plugin cache never serves pre-edit content under the dogfood string. No code — every deliverable is rule text, skill content, manifest fields, or README prose.

**Tech Stack:** Claude Code plugin content (Markdown rules and skills, YAML frontmatter), `rg`, `claude plugin validate`, git.

## Global Constraints

- Public repo: English only, no machine paths, no company names (repo-hygiene rule).
- Commits: one line, conventional prefix `type(scope):`, no body, no trailers (no `Co-Authored-By`).
- Frontmatter safety: any YAML scalar containing `: ` stays double-quoted. `claude plugin validate` does NOT check `rules/` files — review their frontmatter by hand.
- Rule text mentions skills and agents conditionally ("when available") — payload rules load for people without the plugin.
- No version bumps except Task 8. Never force-add ignored files; tracked `docs/` documents ride Task 10's closing commit, not per-task commits.
- `claude plugin validate .`, `claude plugin validate plugins/working-process` and `claude plugin validate plugins/project-memory` must pass before every commit.
- The spec is the contract: wording below is copied from it, and on a conflict the spec wins.
- **Recipe-and-record**: every replacement block below is verbatim shipped text and carries no author annotation, parenthetical, or commentary. A fix applied to shipped text during execution is back-ported into this plan's block in the same fix wave — drift means a re-run reverts the fix. Task 10 diffs every block against the shipped file and STOPs on a mismatch.
- No committed eval files: skills in this repo ship without `evals/trigger-evals.json`.
- The elements-of-style pass on every block below was applied at plan-authoring time. Executors ship the blocks byte-for-byte and never re-style them; a wording improvement is a plan amendment, not an execution-time edit.
- Prescribed tiers for this plan's own review rounds: plan-adversary on the most capable available family (the plan touches two plugins and a published contract other surfaces key on). A round at that tier needs no fallback record.

---

### Task 1: Lifecycle rule — the Unfinished-work list as a named section

Executor: implementer agent.

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md:56-66` (the placeholder sentence's pointer, and the greppable bullet it replaces)

**Interfaces:**
- Consumes: nothing.
- Produces: the `## Unfinished-work list` heading and its four entries — the name Task 4's skill keys on, and the commands Task 9 runs.

- [ ] **Step 1: Write the expected post-edit state to a scratchpad file and run every command against it**

Write the four commands to a file and run them over `docs/` before touching the rule, so the expected outputs in Step 4 are measured rather than assumed:

```bash
mkdir -p /tmp/psr && cat > /tmp/psr/commands.txt <<'EOF'
rg -l --no-ignore --crlf '^\s*grilled: grilling' docs/
rg -l --no-ignore --crlf '^\s*(architect|adversary): (blocking|concerns)$' docs/
rg -l --no-ignore --crlf '^\s*(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/
rg -l --no-ignore --crlf '^\s+(grilled|architect|adversary|architect-fallback|adversary-fallback):' docs/
EOF
while read -r c; do echo "--- $c"; eval "$c" || echo "(no hits)"; done < /tmp/psr/commands.txt
```

Expected: command 1 returns `docs/plans/2026-07-13-rules-distribution.md`, the fenced example the confirmation step rejects. Commands 3 and 4 return no hits.

Command 2 has one conditional extra hit: **this plan itself**, whenever its own `adversary:` field carries a bare `concerns` or `blocking`. That is not a failure of the command — the plan is genuinely an unresolved verdict until the round closes. Expect it while the field is bare, expect it absent once the field reads `LGTM` or carries a resolution annotation, and never edit the field to make a verification step pass.

- [ ] **Step 2: Re-point the placeholder sentence**

In `plugins/working-process/rules/spec-plan-lifecycle.md`, replace:

```
  placeholders (as above) so they never match the grep below.
```

with:

```
  placeholders (as above) so they never match the list below.
```

- [ ] **Step 3: Replace the greppable bullet with the named section**

Delete this bullet:

```
- Unfinished process work is greppable:
  `rg -l '^grilled: grilling' docs/` and
  `rg -l '^(architect|adversary): (blocking|concerns)$' docs/` — the
  anchored match deliberately skips resolved-concern annotations.
  `rg -l '^(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/`
  — pending re-reviews; the waived annotation deliberately defeats the
  anchor.
```

Insert this section immediately after the bullet list that contained it, before the `Lifecycle offers` paragraph:

```
## Unfinished-work list

One entry per class of unfinished process work: the class name, its
command, and the owner of the next move. This section is the list — a
command published elsewhere, such as the ticket sweep in the
ticket-frontmatter rule, is a lookup and not part of it. The
`process-status` skill, when available, runs exactly what stands here,
and this heading is the name it keys on: the heading and the skill move
together or not at all.

A command returns hits, not Findings. A hit counts only when the
matching line sits inside the document's frontmatter block — between the
`---` on the file's first line and the `---` that closes it, never a
later pair — because a document quoting this convention in its body
describes it rather than instantiating it.

- **Grilling pending** — a session's outcomes are recorded and not yet
  applied.
  `rg -l --no-ignore --crlf '^\s*grilled: grilling' docs/`
  Owner: the grilling-session, when available.
- **Unresolved verdict** — a round ended in `concerns` or `blocking`
  and nothing closed it.
  `rg -l --no-ignore --crlf '^\s*(architect|adversary): (blocking|concerns)$' docs/`
  Owner: a fresh round at the prescribed tier, or the resolution
  annotation above.
- **Pending re-review** — a verdict produced below the prescribed tier,
  neither refreshed nor waived.
  `rg -l --no-ignore --crlf '^\s*(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/`
  Owner: the re-review offer at the document's consumption gate.
- **Misplaced stamp** — a process field outside the top level of the
  frontmatter, at any value.
  `rg -l --no-ignore --crlf '^\s+(grilled|architect|adversary|architect-fallback|adversary-fallback):' docs/`
  Owner: the developer; no process surface owns moving a stamp back.
  The class suppresses per field: it hides the one other class whose
  published command would match the relocated line, and no other —
  itself excluded, since its own command matches every process field.
  Match semantics are the mapping, so a class published later needs no
  extra rule.

The tail anchors are exact on purpose: a `(resolved <date>)`,
`(adjudicated <date>)` or `, waived <date>` annotation defeats the
match, and that defeat is the recorded closed state. The leading
anchors are tolerant on purpose, so a relocated field is still found.
The Misplaced stamp command anchors `^\s+` instead, because there the
indentation is the defect it looks for rather than an accident to
tolerate.

## Lifecycle offers
```

The trailing `## Lifecycle offers` heading is part of this edit, not decoration: the rule carries no other `##` heading today, so without it the new section would swallow every paragraph that follows it — the offers paragraph, the commit-gate paragraph, and the ticket pointer — and the structural boundary the skill keys on would exist only at the top edge.

The heading makes the sentence that followed it redundant in its opening, so the same edit re-opens that sentence. Replace:

```
Lifecycle offers — each an offer the developer may decline, and each made
```

with:

```
Each an offer the developer may decline, and each made
```

- [ ] **Step 4: Run the four published commands from the shipped rule**

Extract them from the file rather than retyping, so a typo in the rule is caught rather than reproduced:

```bash
rg -o --no-filename '`rg -l [^`]+`' plugins/working-process/rules/spec-plan-lifecycle.md | tr -d '`' > /tmp/psr/shipped.txt
diff /tmp/psr/commands.txt /tmp/psr/shipped.txt && echo IDENTICAL
while read -r c; do echo "--- $c"; eval "$c" || echo "(no hits)"; done < /tmp/psr/shipped.txt
```

Expected: `IDENTICAL`, then the same outputs as Step 1. The diff is the point — a typo inside a ninety-character regex is exactly what an eyeball comparison of four such lines waves through.

- [ ] **Step 5: Verify the rule's own YAML frontmatter still parses and no stale pointer remains**

```bash
head -5 plugins/working-process/rules/spec-plan-lifecycle.md
rg -n 'the grep below|Unfinished process work is greppable' plugins/working-process/rules/spec-plan-lifecycle.md || echo "no stale pointer"
```

Expected: the `paths:` block intact; "no stale pointer".

- [ ] **Step 6: Commit**

```bash
claude plugin validate plugins/working-process
git add plugins/working-process/rules/spec-plan-lifecycle.md
git commit -m "feat(working-process): publish the unfinished-work list as a named section"
```

---

### Task 2: Ticket sweep — tolerant leading anchor

Executor: implementer agent.

**Files:**
- Modify: `plugins/working-process/rules/ticket-frontmatter.md:54-58` (the "Finding documents by ticket" section)

**Interfaces:**
- Consumes: nothing.
- Produces: the tolerant ticket sweep the project-memory conventions rule's prospective clause (Task 5) refers to.

- [ ] **Step 1: Prove the current sweep goes blind on a relocated field**

```bash
mkdir -p /tmp/psr/tk && printf -- '---\nname: ""\nmetadata:\n  ticket: ABC-123\n---\n\n# Entry\n' > /tmp/psr/tk/nested.md
rg -l --no-ignore '^ticket:.*ABC-123' /tmp/psr/tk/ || echo "old form: no hits"
rg -l --no-ignore --crlf '^\s*ticket:.*ABC-123' /tmp/psr/tk/ || echo "new form: no hits"
```

Expected: "old form: no hits"; the new form returns `/tmp/psr/tk/nested.md`.

- [ ] **Step 2: Replace the sweep**

Replace:

```
The `ticket:` line matches both single-reference and inline-list forms;
`--no-ignore` reaches ignored-mode artifacts:
`rg -l --no-ignore '^ticket:.*ABC-123' docs/ .superpowers/`
```

with:

```
The `ticket:` line matches both single-reference and inline-list forms;
`--no-ignore` reaches ignored-mode artifacts, and the tolerant leading
anchor finds the field where a second writer relocated it:
`rg -l --no-ignore --crlf '^\s*ticket:.*ABC-123' docs/ .superpowers/`
```

- [ ] **Step 3: Run the shipped sweep against a real ticket value**

```bash
rg -o --no-filename '`rg -l --no-ignore --crlf [^`]+`' plugins/working-process/rules/ticket-frontmatter.md | tr -d '`'
rg -l --no-ignore --crlf '^\s*ticket:.*none' docs/ | head -3
```

Expected: one command printed, matching the block above; the second command returns documents (this repo's specs and plans carry `ticket: none`).

- [ ] **Step 4: Commit**

```bash
claude plugin validate plugins/working-process
git add plugins/working-process/rules/ticket-frontmatter.md
git commit -m "fix(working-process): tolerate a relocated field in the ticket sweep"
```

---

### Task 3: Workflow rule — step 7, and every surface that enumerates the flow

Executor: implementer agent.

**Files:**
- Modify: `plugins/working-process/rules/workflow.md:39-41` (after step 6)
- Modify: `plugins/working-process/skills/grilling-session/SKILL.md:8-11` (the "Place in the flow" line) and `:54-55` (a drifted copy of the Grilling-pending command)
- Modify: `plugins/working-process/README.md:6-7` (the flow line under the title)

**Interfaces:**
- Consumes: nothing.
- Produces: step 7's text; no other task depends on it.

The three files are the complete set of shipped surfaces enumerating the flow, established by
`rg -n '→ implementation' plugins/` (the other hits are historical documents under `docs/`, which are records and not consumers).

- [ ] **Step 1: Append step 7 to the workflow rule**

After step 6 ("**Implementation.** …"), insert:

```
7. **Implementation → code review.** When a `*-code-review` skill is
   installed for a domain the change touches, offer a review of the
   work's diff — once implementation is complete and before the plan's
   `status` moves to `implemented`, so a finding can still become work.
   Domains are judged as the plan-adversary judges them: from the change
   itself and the repo's own markers. Several domains touched mean one
   run per domain; orchestrating them into a single run is not this
   step. The step re-specifies no mechanics — the offer routes to
   whatever review surface the matched plugin ships, and that surface
   owns scope resolution, dispatch, and the report.
```

- [ ] **Step 2: Extend the grilling-session flow line**

Replace:

```
plan-adversary on the plan → implementation. Offer a grilling once a spec
```

with:

```
plan-adversary on the plan → implementation → code review. Offer a
grilling once a spec
```

- [ ] **Step 3: Extend the plugin README flow line**

Replace:

```
writing-plans (plan) → plan-adversary → implementation.
```

with:

```
writing-plans (plan) → plan-adversary → implementation → code review.
```

- [ ] **Step 4: Replace the drifted command in the grilling-session skill**

The same file carries a fork of the Grilling-pending command — old form, no tolerant anchor, no flags — which is the fork Task 7 Step 3 removes from the plugin README. Replace:

```
- A session cut short leaves `grilling` in place on purpose: greppable
  debt (`rg -l '^grilled: grilling' docs/`).
```

with:

```
- A session cut short leaves `grilling` in place on purpose: the
  Grilling pending class of the lifecycle rule's Unfinished-work list,
  which publishes the command and which `process-status` runs.
```

- [ ] **Step 5: Verify every flow enumeration moved, and the step numbering is unbroken**

```bash
rg -n '→ implementation\.' plugins/ || echo "no unextended flow line left"
rg -n '→ code review' plugins/
rg -n '^[0-9]\. \*\*' plugins/working-process/rules/workflow.md
rg -n "rg -l '\^grilled" plugins/working-process/rules/spec-plan-lifecycle.md plugins/working-process/skills/grilling-session/SKILL.md || echo "no old-form command in this task's files"
```

Expected, in order:

1. "no unextended flow line left". The period is the discriminator: the old lines end `→ implementation.` and the new ones continue `→ implementation → code review.`, so a bare `→ implementation` grep matches the corrected text too and would pass on either state.
2. **Three** hits, not two: the two arrow-notation surfaces, plus `plugins/working-process/rules/workflow.md`, where step 7's own title reads `**Implementation → code review.**`.
3. Steps 1 through 7, in order — this is what verifies the workflow rule's flow, whose enumeration is a numbered list that no arrow grep has ever matched.
4. "no old-form command in this task's files". The sweep is deliberately scoped: `plugins/working-process/README.md:105` still carries the old form at this point, and Task 7 Step 3 owns removing it. A plugins-wide sweep here would fail on a correct run.

If a check fails, the fix is in the plan, never in the shipped text: an executor must not edit a flow line, a command or a title to satisfy a failing expectation. Report the mismatch and stop.

- [ ] **Step 6: Validate and commit**

```bash
claude plugin validate plugins/working-process
git add plugins/working-process/rules/workflow.md plugins/working-process/skills/grilling-session/SKILL.md plugins/working-process/README.md
git commit -m "feat(working-process): offer a code review after implementation"
```

---

### Task 4: The process-status skill

Executor: implementer agent. Step 1's block is the final authored output: the `skill-creator` pass and the elements-of-style pass ran at plan-authoring time, so an executor ships the block byte-for-byte rather than re-scaffolding or re-tuning it — a description change is a plan amendment, since Task 10 diffs the block against the shipped file. Ship no `evals/` directory.

**Files:**
- Create: `plugins/working-process/skills/process-status/SKILL.md`

**Interfaces:**
- Consumes: the `## Unfinished-work list` heading and entry shape from Task 1.
- Produces: the skill directory name `process-status`, which Task 7's identity surfaces name.

This task settles the two questions the spec deferred to the plan: an unclosed frontmatter block, and whether a Misplaced stamp line names the field.

- [ ] **Step 1: Write the skill**

```markdown
---
name: process-status
description: "Report what the working process left unfinished in this repo — a pending grilling, an unresolved verdict, a re-review nobody ran, a stamp in the wrong place. Use when the developer asks what is unfinished, what the process still owes, or for a status pass over docs/specs and docs/plans."
---

# process-status — what the process left unfinished

Runs the Unfinished-work list the lifecycle rule publishes and reports
what it finds. The rule owns which classes exist; this skill owns
nothing but running them, confirming their hits, and reporting. A class
this skill has never heard of works the moment the rule publishes it.

## Step 1 — read the list

Read the `## Unfinished-work list` section of
`${CLAUDE_PLUGIN_ROOT}/rules/spec-plan-lifecycle.md` — the payload copy
shipped beside this skill, never an installed copy under
`.claude/rules/`. The plugin releases skill and payload in one version,
so that copy is always in step with this skill.

Each entry carries three legs: the class name, one command, and the
owner of the next move. Take all three.

The read fails, and the report says so instead of reporting a clean
repo, when the section is missing or an entry lacks a leg. A run that
could not read the list must never look like a run that found no
unfinished work.

## Step 2 — run each command

Run each entry's command exactly as published, from the repository root.
Never rewrite a command, add a path, or drop a flag: a command that
differs from the published one answers a different question.

## Step 3 — confirm every hit

A command returns hits. A hit becomes a report line only when its
matching line sits inside the document's frontmatter block: the file's
opening `---` on line 1 and its closing `---`. Read the head of the
file to decide.

- The line sits inside that block → the hit is real.
- The line sits anywhere else → the document quotes the convention
  instead of instantiating it. Reject the hit.
- The file has no opening `---`, or none closing it → treat it as having
  no frontmatter block and reject every hit in it. A file whose
  frontmatter never closes is broken for every consumer of frontmatter,
  so it surfaces on its next touch rather than here. Say so if asked;
  never invent a class for it.

## Step 4 — report

Group by document, because the developer acts on a document. Under each
document, one line per confirmed hit: the class name, the field where
the class distinguishes fields, and the owner the entry carries. Read
the owner from the entry — never supply one from your own knowledge of
the process.

Misplaced stamp suppresses per field: it hides the one other class whose
published command would match the relocated line — itself excluded,
since its own command matches every process field. Match semantics are
the mapping, so you never need process knowledge to find it and a class
published later works the same way. Name the field on the line, so the
developer can see which class went quiet.

Close the report with:

- the rejected hits — how many, and in which documents — because
  over-rejection is the only way confirmation can quietly eat real
  unfinished work;
- what was checked: every class name from the list, so a clean run is a
  statement and never silence;
- one question, whether to take anything from the list.

Fire no offer yourself. Each class names its owner, and those owners
have their own gates; a second trigger for one of them belongs to
nobody.

## Out of scope

The Project memory store, documents merely in flight (`draft` or
`approved` with no further move), and any criterion this skill invents.
A new class of unfinished work arrives by being published on the list.
```

- [ ] **Step 2: Validate the plugin and confirm the skill is discoverable**

```bash
claude plugin validate plugins/working-process
rg -n 'name: process-status' plugins/working-process/skills/process-status/SKILL.md
test ! -d plugins/working-process/skills/process-status/evals && echo "no evals dir"
```

Expected: validation passes; the name line prints; "no evals dir".

- [ ] **Step 3: Verify the description's YAML is safe**

The double quotes are deliberate and stay whatever the text contains — a later description edit that introduces `: ` would otherwise break the parse silently, and `claude plugin validate` does check skill frontmatter but the failure mode is empty metadata, not an error. Confirm the block parses and both keys survive:

```bash
python3 -c "import re,sys; t=open('plugins/working-process/skills/process-status/SKILL.md').read().split('---')[1]; import yaml; d=yaml.safe_load(t); print(sorted(d)); print(len(d['description']))"
```

Expected: `['description', 'name']` and a non-zero length — a silent parse failure would raise or drop the key.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/skills/process-status/SKILL.md
git commit -m "feat(working-process): add the process-status skill"
```

---

### Task 5: Project-memory conventions — write place, tolerant read, no repair

Executor: implementer agent.

**Files:**
- Modify: `plugins/project-memory/rules/project-memory-conventions.md:78-82`
- Modify: `plugins/project-memory/README.md:26` (the line summarizing what that rule covers)

**Interfaces:**
- Consumes: Task 2's tolerant sweep, which the prospective clause generalizes.
- Produces: the read rule Task 6's audit clause relies on.

- [ ] **Step 1: Replace the paragraph**

Replace:

```
Every field this rule defines — `description`, `status`, `spec`, `ticket`,
`adr-candidate` — sits at the top level of the frontmatter, never nested
under a `metadata:` block. Nesting would break the anchored `^ticket:` sweep
the project's ticket convention publishes (when it keeps one), across the
whole project rather than only in the store.
```

with:

```
Every field this rule defines — `description`, `status`, `spec`, `ticket`,
`adr-candidate` — is written at the top level of the frontmatter, which is
where the index projection and a human reader look first. That is a write
place, not an invariant: in a Hybrid store the harness relocates fields
into its own block, and it rewrites the frontmatter of any entry it
touches, so a repair is undone at its next write.

- A write creates a field the entry lacks at the top level, and updates
  a field the entry already carries where it sits. Where two copies
  exist, the write takes the top-level one.
- A read accepts the field anywhere inside the frontmatter block, and
  where two copies exist the top-level one wins. The read names no block
  of the harness — the format is that tool's own moving detail.
- Nothing rewrites an entry solely to move a field, and no surface nags
  about a relocated one. A grooming walk the developer asked for is not
  nagging, so its standing report of foreign keys stands.
- Never write a duplicate deliberately. `status` changes, and two copies
  of a changing value with nobody to reconcile them is a dual-write.

Any anchored grep over these fields is written `^\s*<field>:` with
`--crlf` from the start, so tolerance is built in rather than retrofitted
after a sweep goes blind.
```

- [ ] **Step 2: Update the plugin README's summary of that rule**

The README describes the rule's coverage in one clause, and it still names the invariant. Replace:

```
  the index line projected from them, top-level placement of the plugin's own
  frontmatter fields, the tolerance clause for keys other tools wrote,
```

with:

```
  the index line projected from them, the top-level write place and tolerant
  read of the plugin's own frontmatter fields, the tolerance clause for keys
  other tools wrote,
```

Both blocks keep the two-space continuation indent the README's list item uses; an exact-match edit fails without it.

- [ ] **Step 3: Verify the rule's frontmatter and the absence of the old justification**

```bash
head -6 plugins/project-memory/rules/project-memory-conventions.md
rg -n 'never nested|would break the anchored' plugins/project-memory/rules/project-memory-conventions.md || echo "old justification gone"
rg -n 'sits at the top level' plugins/project-memory/rules/project-memory-conventions.md || echo "invariant phrasing gone"
```

Expected: the `paths:` block intact; both "gone" messages.

- [ ] **Step 4: Verify the README and the rule agree**

```bash
rg -n 'place, not an invariant' plugins/project-memory/rules/project-memory-conventions.md
rg -n 'write place and tolerant' plugins/project-memory/README.md
rg -n 'top-level placement' plugins/project-memory/README.md || echo "stale summary gone"
```

Expected: one hit in the rule, one in the README, then "stale summary gone". The rule is matched on `place, not an invariant` rather than on `write place`, because the prescribed block wraps that phrase across a line break — a line-based grep for `write place` cannot match it there however faithfully the block is transcribed, and rewrapping the shipped text to suit a check is exactly the inversion this plan forbids.

- [ ] **Step 5: Commit**

```bash
claude plugin validate plugins/project-memory
git add plugins/project-memory/rules/project-memory-conventions.md plugins/project-memory/README.md
git commit -m "fix(project-memory): state the field's write place and a tolerant read"
```

---

### Task 6: Grooming audit — read `status` wherever it sits

Executor: implementer agent.

**Files:**
- Modify: `plugins/project-memory/skills/memory-review-session/SKILL.md:43-44`

**Interfaces:**
- Consumes: Task 5's read rule.
- Produces: nothing later tasks depend on; Task 9 exercises it.

- [ ] **Step 1: Measure the false negative this closes**

```bash
cd .claude/memory && for f in idea-*.md; do head -20 "$f" | grep -qE '^[[:space:]]+status:' && echo "relocated: $f"; done; cd - >/dev/null
```

Expected: a non-empty list — every one of those entries is invisible to the audit's lifecycle check today.

- [ ] **Step 2: Replace the audit bullet**

Replace:

```
- `idea-*` files whose `status` is `spec'd` or `dropped` but that still sit as
  live bodies;
```

with:

```
- `idea-*` files whose `status` is `spec'd` or `dropped` but that still sit as
  live bodies — read `status` wherever it sits inside the frontmatter, since
  a co-writer may have relocated it, and take the top-level copy where two
  exist;
```

- [ ] **Step 3: Verify**

```bash
rg -n 'read `status` wherever it sits' plugins/project-memory/skills/memory-review-session/SKILL.md
claude plugin validate plugins/project-memory
```

Expected: the clause prints; validation passes.

- [ ] **Step 4: Commit**

```bash
git add plugins/project-memory/skills/memory-review-session/SKILL.md
git commit -m "fix(project-memory): read a relocated status in the grooming audit"
```

---

### Task 7: Identity surfaces and the plugin README

Executor: implementer agent.

**Files:**
- Modify: `plugins/working-process/.claude-plugin/plugin.json:3` (`description`)
- Modify: `.claude-plugin/marketplace.json:10` (the working-process entry's `description`)
- Modify: `README.md:19` (the working-process table row)
- Modify: `plugins/working-process/README.md:48-50` (component list) and `:103-108` (the duplicated commands)

**Interfaces:**
- Consumes: the skill name `process-status` from Task 4.
- Produces: nothing later tasks depend on.

All three identity surfaces enumerate this plugin's skills by name, established by
`rg -n 'sync-rules' plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md`,
so a new skill touches all three in one commit (marketplace-sync rule).

- [ ] **Step 1: Add the skill to the three identity surfaces**

In `plugins/working-process/.claude-plugin/plugin.json`, replace `grilling-session, architect-session, system-designer-session and sync-rules skills` with `grilling-session, architect-session, system-designer-session, process-status and sync-rules skills`.

Make the identical substring replacement in `.claude-plugin/marketplace.json` and in the `README.md` table row.

- [ ] **Step 2: Add the component bullet to the plugin README**

Before the `sync-rules` bullet, insert:

```
- **`process-status` skill** — reports what the process left unfinished
  in the current repo: a pending grilling, an unresolved verdict, a
  re-review nobody ran, a stamp outside the top level of a frontmatter
  block. Runs the Unfinished-work list the lifecycle rule publishes and
  fires none of the offers those classes name. Triggers: "what is
  unfinished" / "process status".
```

- [ ] **Step 3: Replace the README's duplicated commands with a pointer**

The four commands at `plugins/working-process/README.md:103-108` are a fork of the rule's list and have already drifted — the README splits the verdict sweep into two lines where the rule publishes one. Replace:

```
Find unfinished work (the anchored match skips resolved concerns):

    rg -l '^grilled: grilling' docs/
    rg -l '^architect: (blocking|concerns)$' docs/
    rg -l '^adversary: (blocking|concerns)$' docs/
    rg -l '^(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/
```

with:

```
Finding unfinished work is one command per class, published as the
`## Unfinished-work list` section of the lifecycle rule — the exact
anchors live there, and the `process-status` skill runs them. The tail
anchors are exact, so a resolved-concern annotation drops out of the
match by design.
```

- [ ] **Step 4: Verify all four surfaces agree and the fork is gone**

```bash
rg -n 'process-status' plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md plugins/working-process/README.md
rg -n "rg -l '\^grilled" plugins/ || echo "no old-form command left anywhere"
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json')); json.load(open('plugins/working-process/.claude-plugin/plugin.json')); print('json ok')"
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: `process-status` in all four files; "no old-form command left anywhere" — this is where the plugins-wide sweep becomes true, since Task 1 fixed the rule, Task 3 the skill, and Step 3 above the README; "json ok"; both validations pass.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md plugins/working-process/README.md
git commit -m "docs(working-process): sync identity surfaces and README for process-status"
```

---

### Task 8: Dogfood version bump — after all content

Executor: implementer agent.

**Files:**
- Modify: `plugins/working-process/.claude-plugin/plugin.json` (`version`)

**Interfaces:**
- Consumes: every content task above, complete.
- Produces: the version string Task 9's session must observe.

- [ ] **Step 1: Check the arithmetic against the ecosystem, not just the syntax**

```bash
git show master:plugins/working-process/.claude-plugin/plugin.json | rg version
rg version plugins/working-process/.claude-plugin/plugin.json
git show master:plugins/project-memory/.claude-plugin/plugin.json | rg version
rg version plugins/project-memory/.claude-plugin/plugin.json
```

Expected, as measured on 2026-08-25: master carries working-process `0.12.0` and project-memory `0.3.0`; develop carries `0.14.0-dev.background-verdict-dispatch-3` and `0.4.0`. So `0.14.0` is still the unreleased minor, and a new discriminator on it sorts above the current one (`process-status-riders` > `background-verdict-dispatch-3` by prerelease comparison), which is what makes an update fetch it.

- [ ] **Step 2: Re-mint the discriminator**

Replace `"version": "0.14.0-dev.background-verdict-dispatch-3"` with `"version": "0.14.0-dev.process-status-riders"`.

Leave project-memory's version alone: its content change is dogfooded through `--plugin-dir` in Task 9, and the release PR mints its minor.

- [ ] **Step 3: Verify and commit**

```bash
rg version plugins/working-process/.claude-plugin/plugin.json
claude plugin validate plugins/working-process
git add plugins/working-process/.claude-plugin/plugin.json
git commit -m "chore(working-process): dogfood version for process-status-riders"
```

---

### Task 9: Dogfood verification — developer-driven

Executor: **the developer**. Every step here mutates installed state or needs a fresh session, so an implementer agent cannot run them. **STOP: do not start this task without the developer's explicit go-ahead.**

**Files:** none — this task observes.

**Interfaces:**
- Consumes: Tasks 1-8 committed.
- Produces: the record below, rewritten to state what actually ran if the executed path differs from the prescribed one.

- [ ] **Step 1: Load the working tree as a plugin in a fresh session**

Per the recorded dogfood recipe, run a fresh session with `--plugin-dir` pointing at this checkout, so both plugins' working-tree content is live without touching the real install.

- [ ] **Step 2: Verify the artifact the session actually loaded**

Check content, not a version string: confirm the loaded lifecycle rule carries the `## Unfinished-work list` heading and that the loaded `process-status` skill exists. A stale cache passes any check that only asks whether the dispatch worked.

- [ ] **Step 3: Run the skill and check the discriminating observable**

Ask for the process status. Expected: a report naming all four classes as checked, plus a rejected-hit line naming `docs/plans/2026-07-13-rules-distribution.md` — the fenced example the confirmation step rejects. A report that omits the rejection has skipped confirmation; a report that lists that file as unfinished work has skipped it the other way.

One entry is expected under Unresolved verdict rather than clean, for as long as this plan's own `adversary:` field carries a bare verdict: this plan. The right response is to close that verdict, never to edit the field so the report looks clean.

- [ ] **Step 4: Exercise the classes that this repo cannot produce naturally**

In a scratch copy outside the repo, or in a throwaway file under `docs/` reverted afterwards, create: a document with a bare `adversary: concerns`; a document with `grilled: grilling` relocated under a `metadata:` block beside a top-level `architect: concerns`; and a document quoting a bare verdict in its body. Expected: the first reports as an unresolved verdict; the second reports Misplaced stamp naming `grilled` while still reporting the top-level `architect: concerns`; the third is rejected.

- [ ] **Step 5: Confirm step 7 offers nothing here, and the audit clause reads a relocated status**

This work touches plugin content only, so no `*-code-review` skill matches a touched domain and step 7 correctly offers nothing.

Then the store half, which needs a constructed case for the same reason the `docs/` classes did: every live `idea-*` entry reads `status: parked`, and the audit's worklist fires only on `spec'd` or `dropped`, so a walk that honours Task 6's clause and one that ignores it produce identical output on today's store. In one of the relocated entries from Task 6 Step 1, set the **nested** `status` to `spec'd` without moving the field, run a memory-review-session over Private memory, confirm the audit flags that entry as a closed idea still sitting live, then revert the value. Without this the clause ships with a test that cannot fail.

- [ ] **Step 6: Exercise step 7's firing path on a real domain project**

The negative branch above proves only that the step stays silent. The spec's Verification section requires the positive one: in a Python or Salesforce checkout of the developer's own, with this plugin dogfooded, take a change to completion and confirm the offer fires before the plan's `status` would flip, names the matched domain, and hands off to that plugin's own review surface. **This step needs a checkout this repo does not contain.** If the developer prefers to defer it, record the deferral here with its date rather than deleting the step — an unverified firing path is a known gap, not a silent one.

- [ ] **Step 7: Record what ran**

Rewrite the steps above to match the executed path where it differed, and note the outcome.

**Executed 2026-08-25 by the controller session rather than the developer, on the developer's explicit go-ahead.** The loop stopped at this task and handed it over as the plan requires; the developer then asked the controller to run it, which is what authorizes the departure from the reserved executor. The delivery path was `claude -p --plugin-dir` against this checkout, so no installed state changed and no version re-mint was needed. Outcomes:

- Steps 1-2: the run loaded the working tree's plugin and named all four classes, Misplaced stamp among them — a class that exists only in this checkout, which is what distinguishes a fresh load from a stale cache. The report stated it had read the payload copy rather than `.claude/rules/`.
- Steps 3-4: on a scratch fixture repo the report was exactly the designed one. The fixture that matters carried a nested `grilled:` beside a top-level `architect: concerns`: the report named Misplaced stamp with its field, said Grilling pending was suppressed **for that field**, and still reported the verdict — per-field precedence, live. Two body-quoted lines were rejected with the reason. On this repo the report came back clean with the one known rejection at `docs/plans/2026-07-13-rules-distribution.md:267`.
- Step 5: step 7 correctly offered nothing — the branch changes twelve files, none a Python or Salesforce artifact, so no `*-code-review` skill matches a touched domain. The store's constructed case fired: one relocated `status` set to `spec'd` without moving the field, and the grooming audit flagged the entry as a closed idea still living, reading the value from its nested position. Reverted afterwards; the co-writer's own `modified:` key was left as it rewrote it.
- Step 6 **executed 2026-08-25**, against a constructed fixture rather than the developer's own project, once a mechanic became clear: step 7 lives in a rule, and rules do not arrive through `--plugin-dir` — they bind a session only when installed. The fixture therefore carried the new `workflow.md` and `spec-plan-lifecycle.md` installed at project level, exactly as sync-rules would place them, plus a real `src/calc.py` and a plan at `status: approved`; python-standards was loaded so a `*-code-review` skill existed. The session named step 7, placed it before the flip to `implemented` and quoted the window, judged the domain from the change and the repo's markers, found `python-code-review` installed, said one domain means one run, added no mechanics of its own, framed it as a declinable offer, and chained to the memory-review offer at the flip. Nothing about step 7 is now unverified.

  Two observations from setting that up, neither a defect in this plan. The rules installed on this host are a prior release and carry no step 7, so a session in this repo would not fire the offer until the release lands — which is the rules-payload delivery lag the plugin already documents. And this repo does hold `.py` and `.cls` files, but they are reference content shipped *inside* the standards plugins; whether a change to one of those counts as touching the Python domain is a question step 7's wording leaves open, and it is worth answering the first time it comes up rather than now.

The audit run also surfaced a defect nobody planted: `.claude/memory/idea-standards-skills-rework.md` carries `ticket: [#6, #12, #14]`, where `#` after a space opens a comment, so the flow sequence never closes and the whole frontmatter fails to parse. Out of this plan's scope, recorded for the store's next grooming walk.

If a content fix falls out of this task, apply it and back-port it into the block it came from. Then, before re-verifying, decide which delivery path the re-verification uses. Through `--plugin-dir` (Step 1's path) the working tree is read directly and no version change is needed. Through the plugin cache, the version string is the cache key, so the discriminator must **widen to a fresh value** — `0.14.0-dev.process-status-riders-2`, then `-3` — exactly as the previous topic did; re-running Task 8 Step 2 verbatim writes the same string and delivers nothing.

---

### Task 10: Closing — block-to-shipped diff, lifecycle flips, docs commit

Executor: implementer agent, except the flips, which need the developer's confirmation that Task 9 passed.

**Files:**
- Modify: `docs/specs/2026-08-24-process-status-and-anchor-hardening-design.md` (frontmatter `status`)
- Modify: `docs/plans/2026-08-25-process-status-riders.md` (frontmatter `status`)

**Interfaces:**
- Consumes: Tasks 1-9.
- Produces: the closing commit.

- [ ] **Step 1: Byte-compare every prescribed block against the shipped tree**

The Global Constraints promise a diff, so this step runs one. Each fenced block in this plan is prescribed shipped text in one of two directions: a block whose marker line ends `with:`, mentions inserting, or is written as ```markdown must appear **verbatim** in the tree afterwards; a block whose marker ends `replace:` or `delete this bullet:` must be **gone** from it. Marker matching is case-insensitive, and a block the grammar cannot place is reported and fails the step — a classifier that silently drops what it does not recognize reads exactly like a classifier that checked everything. A keyword grep passes on a paraphrase; this does not.

```bash
python3 - <<'PY'
import pathlib, re, sys
PLAN = pathlib.Path('docs/plans/2026-08-25-process-status-riders.md')
FILES = [
 'plugins/working-process/rules/spec-plan-lifecycle.md',
 'plugins/working-process/rules/workflow.md',
 'plugins/working-process/rules/ticket-frontmatter.md',
 'plugins/working-process/README.md',
 'plugins/working-process/skills/grilling-session/SKILL.md',
 'plugins/working-process/skills/process-status/SKILL.md',
 'plugins/working-process/.claude-plugin/plugin.json',
 '.claude-plugin/marketplace.json',
 'README.md',
 'plugins/project-memory/rules/project-memory-conventions.md',
 'plugins/project-memory/README.md',
 'plugins/project-memory/skills/memory-review-session/SKILL.md',
]
missing_files = [f for f in FILES if not pathlib.Path(f).exists()]
if missing_files:
    print("NOT YET CREATED:", missing_files)
blob = "\n".join(pathlib.Path(f).read_text() for f in FILES if pathlib.Path(f).exists())
lines, marker, i = PLAN.read_text().splitlines(), '', 0
present, absent, unclassified = [], [], []
while i < len(lines):
    if lines[i].startswith('```'):
        lang, body, i = lines[i][3:].strip(), [], i + 1
        while i < len(lines) and not lines[i].startswith('```'):
            body.append(lines[i]); i += 1
        block = "\n".join(body)
        m = marker.lower()
        if lang == 'bash' or not block.strip():
            pass
        elif lang == 'markdown' or m.endswith('with:') or 'insert' in m:
            present.append(block)
        elif m.endswith('replace:') or m.endswith('delete this bullet:'):
            absent.append(block)
        else:
            unclassified.append((marker[:70], block.splitlines()[0][:50]))
    elif lines[i].strip():
        marker = lines[i].strip()
    i += 1
EXPECTED = (14, 11)   # (present, absent); a plan amendment that adds or drops a
                      # fenced block updates these in the same wave, like any back-port
missing = [b.splitlines()[0][:70] for b in present if b not in blob]
ghosts  = [b.splitlines()[0][:70] for b in absent  if b in blob]
counts  = (len(present), len(absent))
print("blocks checked:", counts[0], "present /", counts[1], "absent; expected", EXPECTED)
print("UNCLASSIFIED (a block the grammar could not place):", unclassified or "none")
print("MISSING (prescribed, not shipped):", missing or "none")
print("SURVIVING (should be replaced):", ghosts or "none")
if counts != EXPECTED:
    print("COUNT DRIFT: a fenced block was added, dropped, or escaped the grammar")
sys.exit(1 if missing or ghosts or unclassified or counts != EXPECTED else 0)
PY
```

Expected: no "NOT YET CREATED" line, 14 present and 11 absent blocks checked against `EXPECTED`, all three lists "none", exit 0. Run before Task 4 the script reports the skill file as not yet created and every unapplied block as missing — that is the mechanism working, not a defect. **STOP on any entry at Task 10**: either the shipped text is wrong and gets fixed, or this plan drifted and the block gets back-ported in the same wave. A re-run of a drifted plan reverts shipped fixes.

The counts are enforced by the script, not left to a reader comparing printed numbers against prose — a shortfall means a fenced block escaped the grammar, and that is invisible in three "none" lists. One edit remains specified as prose rather than a fenced block and is therefore the only thing outside this check: Task 7 Step 1's identity-surface substring, covered by Task 7 Step 4's `process-status` grep across all four files.

- [ ] **Step 2: Run the full validation set and the two prose-edit checks**

```bash
claude plugin validate . && claude plugin validate plugins/working-process && claude plugin validate plugins/project-memory && echo "VALIDATE-OK"
rg -n '^## Lifecycle offers$' plugins/working-process/rules/spec-plan-lifecycle.md
rg -n 'Lifecycle offers — each an offer' plugins/working-process/rules/spec-plan-lifecycle.md || echo "sentence prefix removed"
```

Expected: "VALIDATE-OK"; the heading present; "sentence prefix removed".

- [ ] **Step 3: Confirm the repo's own anchors are clean**

Extract and run the commands from the shipped rule, without reaching for Task 1's scratch files — the developer-paced Task 9 sits between the two tasks and `/tmp` may have been cleared, which would read as command drift rather than a missing file:

```bash
rg -o --no-filename '`rg -l [^`]+`' plugins/working-process/rules/spec-plan-lifecycle.md | tr -d '`' > /tmp/psr-close.txt
while read -r c; do echo "--- $c"; eval "$c" || echo "(no hits)"; done < /tmp/psr-close.txt
```

Expected: four commands, and the only hit is the known rejected example. The `status` flip in Step 4 has nothing to do with this — no command on the list reads `status`. What must be clean is this plan's `adversary:` field: a bare `concerns` or `blocking` on it is an Unresolved verdict, so before the close it takes either a fresh round or this rule's resolution annotation with its body note. **STOP** if the field is bare.

- [ ] **Step 4: Flip both documents to `implemented`**

Set `status: implemented` in the spec and in this plan. The spec already carries `grilled: 2026-08-24` and `architect: LGTM`; this plan carries its own `adversary:` verdict by then.

- [ ] **Step 5: Commit the documents**

```bash
git add docs/specs/2026-08-24-process-status-and-anchor-hardening-design.md docs/plans/2026-08-25-process-status-riders.md docs/domain/glossary.md
git commit -m "docs: close the process-status riders spec and plan"
```

- [ ] **Step 6: Offer the Project memory review**

The lifecycle rule's offer at the `implemented` flip: released work-state notes close and resolved entries sweep to the archive. Three entries already closed during the spec's authoring; the remaining candidate is the `initiate` half of the review-driven remediation loop, whose body already points at the shipped step 7.

## Review rounds

### 2026-08-25 — plan-adversary, fable 5, blocking (round 1)

Three Important, six Minor; every finding fixed in this document. The round re-ran the plan's own verification claims and confirmed all seven, adding one the dispatcher had missed: the checkout stands on the topic branch with the spec, this plan and the glossary still uncommitted, which Task 10 Step 5 already covers.

- **fixed** — [Important] Task 3's verification expected `rg -n '→ implementation' plugins/` to list three files, but the workflow rule enumerates the flow as a numbered list and no arrow grep has ever matched it — so the "complete set of surfaces" claim rested on a grep blind to the file the task edits. The step now verifies the two arrow surfaces by `→ code review`, the workflow rule by its step numbering, and says which is which.
- **fixed** — [Important] `grilling-session/SKILL.md:55` shipped a drifted fork of the Grilling-pending command (old form, no flags), surviving a task that edits the same file while Task 7 removed the identical fork from the plugin README. Task 3 now replaces it with a pointer to the list.
- **fixed** — [Important] the spec's requirement that a run over a Python or Salesforce project demonstrate step 7 firing had no owning task; Task 9 gains that step, with an explicit deferral-with-date option because the checkout is not in this repo.
- **fixed** — [Minor] `project-memory/README.md:26` still summarized the conventions rule as "top-level placement"; Task 5 now updates it, and its prescribed block keeps the list item's two-space continuation indent, without which the exact-match edit would fail.
- **fixed** — [Minor] the new `## Unfinished-work list` was the rule's only H2, so it would swallow every following paragraph; Task 1 now adds a closing `## Lifecycle offers` heading in the same edit.
- **fixed** — [Minor] Task 10 Step 3 claimed the `status` flip clears the anchors, which no command on the list reads; the step now conditions the close on this plan's `adversary:` field and STOPs on a bare verdict.
- **fixed** — [Minor] Task 1 Step 4 compared four ninety-character regexes by eye; it now runs `diff`.
- **fixed** — [Minor] the `skill-creator` instruction in Task 4 collided with the recipe-and-record rule; Step 1's block is now declared the final authored output.
- **fixed** — [Minor] the repo's elements-of-style rule would have an executor re-style the verbatim blocks into Task 10's STOP; Global Constraints now states the pass ran at authoring time.

### 2026-08-25 — plan-adversary, fable 5, blocking (round 2)

Four Important, three Minor; every finding fixed. The round confirmed what round 1's fixes had left standing — every old-text block matching byte-for-byte, the identity-surface substring in all three files, Task 8's version arithmetic, Task 10 Step 6's memory claim, PyYAML — and found no unenumerated consumer. Two of the four Important were debris from round 1's own fixes, which is the failure mode this round was dispatched to hunt.

- **fixed** — [Important] round 1's rewritten flow verification had two false expectations: `→ implementation` is a substring of the corrected `→ implementation → code review`, so it matches either state, and `→ code review` also matches step 7's own title in the workflow rule. The step now greps `→ implementation\.` for the old state, expects three hits for the new one and says which file is the third, and forbids editing shipped text to satisfy a failing check.
- **fixed** — [Important] the same step swept all of `plugins/` for the old-form command while `plugins/working-process/README.md:105` legitimately still carries it until Task 7. The sweep is now scoped to the files this task edits, and the plugins-wide version moved to Task 7 Step 4, where it becomes true.
- **fixed** — [Important] Task 1 Step 1's recorded measurement said commands 2, 3 and 4 return no hits, but stamping this plan's own `adversary: blocking` made command 2 return this plan — a gate colliding with its own record. Task 1 Step 1 and Task 9 Step 3 now name the plan's own frontmatter as the one conditional hit, with the instruction never to edit the field to make a check pass.
- **fixed** — [Important] Global Constraints promised Task 10 diffs every block, while the step ran three keyword greps that pass on a paraphrase. Step 1 now extracts every fenced block from this plan and byte-compares it against the shipped tree in both directions — prescribed text must be present, replaced text must be gone. Verified by running it: all nine old-text blocks are detected verbatim in the tree today.
- **fixed** — [Minor] Task 4 Step 3 asserted the description contains `: `, which it does not; the step now states the quotes are deliberate regardless of content and keeps the parse check.
- **fixed** — [Minor] the rule and the skill defined the frontmatter boundary differently, the rule's wording admitting a later `---` pair mid-body; both now say the block opens on line 1.
- **fixed** — [Minor] suppression required a field-to-class mapping no entry published while the skill was barred from supplying process knowledge; both surfaces now say the mapping is the command's own pattern, which also keeps the future-class promise intact.

### 2026-08-25 — plan-adversary, fable 5, concerns (round 3)

One Important, two Minor; every finding fixed. First round below the blocking threshold. The round re-verified the whole round-2 wave against the tree — the flow discriminator, the scoped sweep, the conditional-hit clause, the identity substring, the version arithmetic, every old-text block — and found it sound; the one break was in the new mechanism, in the way this loop keeps breaking things.

- **fixed** — [Important] the block classifier implemented a narrower marker grammar than the contract it claimed, so three fenced blocks escaped both directions with no branch to report them: the absent side of Task 1 Step 2 (`replace:` lowercase against a case-sensitive test) and — worse — the step 7 text and the README component bullet, whose markers said "insert" in prose the grammar did not match. The plan's headline deliverable was never byte-checked. The grammar is now case-insensitive and accepts any marker mentioning an insert, an unclassified block fails the step loudly, and the expected block counts (13 present, 10 absent) are part of the expectation so a shortfall cannot hide inside three "none" lists. Re-verified after the fix: zero unclassified, all ten absent-kind blocks detected verbatim.
- **fixed** — [Minor] the suppression mapping asserted a uniqueness that fails on a literal reading — `(architect|adversary)-fallback` contains `architect`, and the Misplaced stamp command's own pattern names every process field, admitting a self-suppression reading. Both surfaces now phrase it as match semantics against the relocated line, with this class excluded.
- **fixed** — [Minor] three commit steps (Tasks 1, 2 and 5) omitted the validation the Global Constraints require before every commit; they now run it.

The dispatcher's own verification of the mechanism read "11 present / 9 absent" as success when it was a three-block shortfall — a count with no baseline proves nothing, which is why the counts are now written into the expectation.

### 2026-08-25 — plan-adversary, fable 5, concerns (round 4)

Three Minor, **no Important** — the first round with nothing above that grade. The round re-verified the whole round-3 wave: all 23 classifications direction-checked by hand and by run, no absent block a substring of its replacement, no present block pre-existing, the four commands' live outputs including the conditional hit, the consumer sweeps, the version arithmetic. It also answered the inversion attack: a marker phrased "insert X, then replace:" would misdirect a block, but a misdirected block fails loudly in both directions, so the silent class is only one that lands wrong-direction *and* coincidentally satisfies the inverted check.

- **fixed** — [Minor] Task 1 Step 3's prose instruction for the sentence prefix was self-contradictory: deleting `Lifecycle offers — ` mechanically yields a lowercase `each an offer`, while the stated result was capitalized, and no check distinguished them. The edit is now a fenced replace/with pair, so the byte-diff owns it — one prose-specified edit remains, and it has its own grep.
- **fixed** — [Minor] the block counts were declared part of the expectation while `sys.exit` ignored them, leaving drift to a reader comparing printed numbers against prose — the same mistake one level up from round 3's. The script now carries `EXPECTED = (14, 11)` and exits non-zero on drift.
- **fixed** — [Minor] the rule block read "hits, not findings" where the spec and the glossary both carry the canonical `Findings`; capitalized, since the Global Constraints make the spec's wording binding.

Re-verified after this wave: 14 present, 11 absent, zero unclassified, all eleven absent blocks detected verbatim in the tree, no present block already applied.

### 2026-08-25 — plan-adversary, fable 5, concerns (resolved 2026-08-25) (round 5)

One Important, two Minor; all fixed. The round was aimed at the dimensions the earlier four spent least on — task ordering, the executor split, and what the dogfood run proves versus claims — since the verification machinery had already had three rounds of attention. It re-verified the classifier, the four commands' live outputs, the records against the plan they describe, every spec deliverable's owning task, and the version arithmetic, and found the ordering windows benign.

- **fixed** — [Important] Task 9 Step 5's store check was vacuous: every live `idea-*` entry reads `status: parked`, and the audit's worklist fires only on `spec'd` or `dropped`, so a walk honouring Task 6's clause and one ignoring it produce identical output. The clause would have shipped with a test that cannot fail, while the `docs/` classes each had a discriminating observable. The step now constructs the case — set a relocated entry's nested `status` to `spec'd` without moving the field, confirm the audit flags it, revert.
- **fixed** — [Minor] Step 7 pointed at Task 8 Step 2 to "re-mint the discriminator", but that step writes a fixed string, so re-running it delivers nothing through the cache. The step now says the discriminator widens to a fresh value and names which delivery path needs it, `--plugin-dir` needing none.
- **fixed** — [Minor] Task 10 Step 3 reached back to Task 1's scratch file for its diff, across the developer-paced Task 9; it now re-extracts the commands from the shipped rule itself.

The round also flagged, ungraded and outside its subject, that the spec's round-4 record declared three findings and carried seven: inserting rounds 3 and 4 had split round 2's bullet list and the four orphans landed under round 4. Fixed in the spec, where every record now matches its own tally.

Asked whether a sixth round would earn its cost, the round answered no: after this wave the remaining risk lives in Task 9's execution rather than in the plan text, and the honest close is a resolution annotation. That answer is why this record carries one.
