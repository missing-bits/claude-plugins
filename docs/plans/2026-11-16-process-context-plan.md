---
ticket: none
date: 2026-11-16
status: approved
spec: ../specs/2026-11-16-process-context-spec.md
branch: feature/process-context
base: develop
adversary: concerns (resolved 2026-11-16)
---

# Process Context Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the dispatcher's procedure, the disposition ledger, the
Unfinished-work list and the per-round commit convention out of the two
large rules into skill reference files, and leave pointers behind.

**Architecture:** Each moved text is extracted verbatim from the
merge base into a reference file, checked with a whitespace-normalised `diff`, and only
then has its pointers rewritten, so the rewrite is the whole visible
change. The sources are cut afterwards, one rule per task, and every
pointer into moved text is rewritten from the inventory below.

**Tech Stack:** Markdown, `bash`, `git`, `sed`, `grep`, `diff`, `wc`,
Python `unittest`, the `claude` CLI.

**Spec:** `docs/specs/2026-11-16-process-context-spec.md`

## Global Constraints

- **Realizes:** D1 — every moved text lands in the home its reader
  needs: always loaded (`workflow.md`), with a document class
  (`spec-plan-lifecycle.md`), or read when an activity starts (a skill).
  No task puts text in a fourth place.
- **Realizes:** D9 — text read when an activity starts lives in a skill
  directory under `plugins/working-process/skills/`. No file is added to
  or removed from `plugins/working-process/rules/`.
- **Realizes:** D11 — in an installed rule, a pointer to skill text
  names the skill and its reference, conditionally, and never a path or
  a file name: "the `review-loop` skill's procedure reference, when that
  skill is available", "its ledger reference", "the `process-status`
  skill's Unfinished-work reference".
- **Realizes:** D12 — text that moves whole moves unchanged but for the
  pointer rewrites this plan lists. Each extraction is checked with an
  empty `diff` before any rewrite; a difference this plan does not list
  is a defect.
- **Realizes:** D13 — `## Ticket directories` and `### Moving a document
  into a ticket directory` stay in `spec-plan-lifecycle.md`, untouched.
- No rule text changes meaning. A cut sentence moves to a named home or
  repeats text that stays; nothing leaves with its decision.
- No loader, hook or settings key is added. `sync-rules` is not edited.
- Pointer forms outside installed rules: `SKILL.md` and agent cards use
  `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/<FILE>.md`; a reference file
  names a sibling as "`LEDGER.md`, beside this file" and another skill's
  reference by skill and file name, since `${CLAUDE_PLUGIN_ROOT}` is
  substituted in skill and agent content, not in a file a session reads
  later; the registry keeps its `plugins/`-relative path.
- A mention is not a pointer. "The provisional batch", "a `hit held`
  line", "an Unfinished-work entry" name things and stay as written; a
  pointer says where a text lives ("the workflow rule defines", "below",
  "above") and is rewritten.
- Glossary bans bind: no unqualified "probe" (write "measurement"), no
  bare "pair" where a pair offer is in view (write "audit pair" or "pair
  offer").
- English only, no machine paths, no company names. Commit messages are
  one-line conventional commits with no body and no trailer; commit only
  where the developer has authorized commits for this execution.
- No agent creates `evals/trigger-evals.json`.
- Run every command with `bash` from the repository root: `rg` is not on
  this plan's assumed path, and an interactive shell may alias `grep`.
- Every size is reported beside its estimate. A miss is reported, never
  a failure.

## Review Focus

- A session with the new plugin and unsynced old rules holds both
  copies; the skill's description must trigger alone. Task 1 pins the
  four read moments in the description.
- A session with the new rules and no plugin meets pointers to a skill
  it lacks; every pointer must be conditional. Tasks 2 and 3 grep for
  the conditional on each pointer line.
- After a compaction only `SKILL.md` returns; it must tell the session
  to invoke the skill again and re-read the references. Task 1 pins the
  sentence.
- A reviewer dispatched on a document with `## Review rounds` no longer
  receives the ledger grammar; the brief must carry the reference's
  path. Task 1 pins the sentence in `SKILL.md`.
- `process-status` must still fail loudly when it cannot read its list.
  Task 4 keeps the skill's failure rule and checks the heading it keys
  on.

## Settled questions

1. **Steps cut.** Step 3 loses its gate sentence and its "definition
   below" clause (Task 2, Step 3). Step 4 loses its sequencing, which
   moves; its two sentences repeating the lifecycle rule stay, since
   that rule is not loaded when the offer is accepted. Steps 1, 2, 5
   and 7 lose nothing: none of their sentences has a named home or a
   repeat in kept text. The projected `workflow.md` is about 19,500
   characters against the 15,000 estimate; the developer accepted the
   miss on 2026-11-16, and it is reported, not closed.
2. **Step 4.** The offer is base lines 45–113 and 131–137. The
   sequencing is base lines 115–130 and moves to `PROCEDURE.md`. The
   delegated plan-writer sentence (133–137) stays in step 4, so the
   lifecycle rule's "as the workflow rule's step 4 says" resolves
   unedited.
3. **Reference names.** `skills/review-loop/PROCEDURE.md`,
   `skills/review-loop/LEDGER.md`,
   `skills/process-status/UNFINISHED-WORK.md` — upper case, beside
   `SKILL.md`, as `grilling-session` names its own. Step 4's sequencing,
   the per-round commit convention and the relay-then-stamp sentence all
   go to `PROCEDURE.md`.
4. **Per-round convention.** It is lifecycle base lines 987–1045, from
   "Asking whether the loop may commit per round" to "where no sha
   exists." Afterwards the lifecycle rule cites neither
   `review.per-round-commit` nor `docs-branch.merge`, and the registry
   names `PROCEDURE.md` for both and for `review.autonomy`.
5. **Routing.** Verdict dispatch: both references. Consumption gate:
   both. `status` move: `PROCEDURE.md`. Ledger line: `LEDGER.md`.
6. **"Both audits offered above…"** stays in `workflow.md`; its reader
   may dispatch an audit outside the four moments. Its pointer is
   rewritten.
7. **Pointer forms.** See Global Constraints.
8. **The heading.** `UNFINISHED-WORK.md` keeps `## Unfinished-work
   list`, and `process-status` still keys on it. The sentence "the
   heading and the skill move together or not at all" moves with the
   section, unchanged and still true. Nothing replaces it in the
   lifecycle rule.
9. **Pointer sentences.** One per skill. `workflow.md` gets one for
   `review-loop` and one for the Unfinished-work reference.
10. **"Edited together."** Written once, as the closing sentence of
    `review-loop/SKILL.md`.
11. **Live checks.** Task 7, Step 5, after the developer installs the
    dogfood version and syncs the rules: one context measurement per
    document class, one `process-status` run, one `review-loop` trigger
    check. A miss is reported, never a failure.

## Pointer inventory

Line numbers are at the merge base
(`BASE=$(git merge-base HEAD develop)`). Each task anchors its edit on
the quoted text, since earlier tasks shift lines. Every bash block
assumes `BASE`, `W` and `L` as Task 1 Step 1 sets them; a fresh shell
sets all three again first. Rows match by the listed line, not by
text alone: W783 carries the same words as the W508 row and stays.

`plugins/working-process/rules/workflow.md`, kept text:

| Line | Pointer | Becomes |
|---|---|---|
| 37 | "the verdict-agent dispatch subsection below" | Task 2, Step 3 |
| 39–44 | "the dispatch subsection below defines the gate"; "the definition below" | cut, Task 2, Step 3 |
| 53–57 | "the verdict-agent dispatch subsection defines" | procedure reference |
| 129 | "the propagation gate below" | moves with 115–130 |
| 140–141 | "the verdict-agent dispatch subsection below" | procedure reference |
| 150–151 | "*The stand-in and the provisional batch* below" | procedure reference |
| 155–156 | "the dispatch-record store's `.gitignore` guard" | stated inline |
| 184–185 | "the verdict-agent dispatch subsection already defines" | procedure reference |
| 230–232 | "the two the verdict-agent dispatch subsection defines" | stated inline |
| 300–301 | "which the spec-plan-lifecycle rule names" | procedure reference |

Examined and left: 10, 133 and 200 ("below", kept targets); 52, 134,
178, 203 and 210 (lifecycle text that stays); 158, 281–283 (mentions).

`plugins/working-process/rules/spec-plan-lifecycle.md`, kept text:

| Line | Pointer | Becomes |
|---|---|---|
| 54 | "the provisional batch the workflow rule defines" | procedure reference |
| 167 | "the list below" | "the Unfinished-work list" |

Examined and left: 92 and 452 (workflow text that stays); 65–66, 83,
151, 189, 357, 360, 466, 930, 943–946 (mentions).

Other files:

| File and line | Pointer | Action |
|---|---|---|
| `skills/process-status/SKILL.md:8–11, 15–19` | the lifecycle rule's section | Task 4 |
| `skills/grilling-session/SKILL.md:60` | "the lifecycle rule's Unfinished-work list" | Task 5 |
| `README.md:93` (plugin) | "the lifecycle rule publishes" | Task 5 |
| `README.md:162` (plugin) | "section of the lifecycle rule" | Task 5 |
| `README.md:214–217` (plugin) | "relay-then-stamp sequence … in the workflow rule" | Task 5 |
| `SETTINGS_REGISTRY.md:106, 122, 130` | `read-by:` | Tasks 2 and 3 |
| `docs/domain/glossary.md:451` | "section of the spec-plan-lifecycle rule" | Task 5 |

Examined and left: `PERSONA_COMMON.md:87, 123` and both consult cards
(the consultation paragraphs stay); `README.md:74, 206, 288–290`
(plugin); `agents/plan-adversary.md:53`, `agents/integrity-auditor.md:64`,
`agents/propagation-auditor.md:153, 189–191` (mentions, or
*Decision register* and *Plan annotations*, which stay);
`rules/review-reports.md:42`, `rules/ticket-frontmatter.md:58`
(*Branch naming* stays); `rules/technical-design.md:34` (resolves
through the lifecycle rule's kept bullet and its new pointer paragraph);
`scripts/decision-coverage.py:6`; the glossary's **Disposition ledger**,
**Round heading**, **Gate line** and **Document branch** entries, which
name no home.

Pointers inside moved text are listed in the task that moves it.

---

### Task 1: The `review-loop` skill

**Files:**
- Create: `plugins/working-process/skills/review-loop/SKILL.md`
- Create: `plugins/working-process/skills/review-loop/PROCEDURE.md`
- Create: `plugins/working-process/skills/review-loop/LEDGER.md`

**Interfaces:**
- Produces: the skill name `review-loop`; the reference names
  `PROCEDURE.md` and `LEDGER.md`; the `PROCEDURE.md` headings
  `### The audit pair at the consumption gate` and
  `### Per-round commits on a document branch`.

**Realizes:** D3, D4, D6, D10

- [ ] **Step 1: Confirm the anchors**

```bash
BASE=$(git merge-base HEAD develop)
W=plugins/working-process/rules/workflow.md
L=plugins/working-process/rules/spec-plan-lifecycle.md
git show $BASE:$W | sed -n '115p;130p;322p;868p' | cut -c1-40
git show $BASE:$L | sed -n '470p;807p;914p;925p;987p;1045p' | cut -c1-40
```

Expected, in order: `   Where the technical-design offer is accep`,
`   has passed, leaving no confirmed hit, w`,
`## Dispatching a verdict agent`,
`` The `## Dispatching a verdict agent` secti``,
`## The disposition ledger`,
`State prevents relitigation, not the rev`,
`close, resolved entries sweep to the arc`, `full-document round.`,
`Asking whether the loop may commit per r`, `path, where no sha exists.`
A mismatch stops the task: the base moved.

- [ ] **Step 2: Extract the two references**

```bash
D=plugins/working-process/skills/review-loop; mkdir -p $D
{ printf '# review-loop — the dispatcher'\''s procedure\n\n'
  git show $BASE:$W | sed -n '322,867p'
  git show $BASE:$L | sed -n '914,925p' | sed '1s/^.*archive\. //'
  printf '\n### The audit pair at the consumption gate\n\n'
  git show $BASE:$W | sed -n '115,130p' | sed 's/^   //'
  printf '\n### Per-round commits on a document branch\n\n'
  git show $BASE:$L | sed -n '987,1045p'
} > $D/PROCEDURE.md
{ printf '# review-loop — the ledger grammar\n\n'
  git show $BASE:$L | sed -n '470,807p'
} > $D/LEDGER.md
```

- [ ] **Step 3: Verify the extraction is verbatim**

```bash
norm() { tr -s '[:space:]' '\n' | sed '/^$/d'; }
diff <(grep -v -e '^# review-loop' -e '^### The audit pair at' -e '^### Per-round commits on' $D/PROCEDURE.md | norm) \
     <({ git show $BASE:$W | sed -n '322,867p'; git show $BASE:$L | sed -n '914,925p' | sed '1s/^.*archive\. //'
         git show $BASE:$W | sed -n '115,130p'; git show $BASE:$L | sed -n '987,1045p'; } | norm)
diff <(sed '1,2d' $D/LEDGER.md | norm) <(git show $BASE:$L | sed -n '470,807p' | norm)
```

Expected: no output from either `diff`. Commit here where authorized
(`feat(working-process): review-loop references, extracted verbatim`),
so the next step's diff shows the rewrites alone.

- [ ] **Step 4: Rewrite the pointers in `PROCEDURE.md`**

Each row is one edit. Find the quoted phrase at the listed line by its
words: it may wrap onto the next line, and the same words elsewhere are
not this row's.

| Base line | Text | Becomes |
|---|---|---|
| W451 | "the round record the lifecycle rule defines" | "the round record `LEDGER.md`, beside this file, defines" |
| W490 | "the lifecycle rule's per-round commits" | "the per-round commits defined under *Per-round commits on a document branch* below" |
| W508, 533, 661, 670, 708, 740, 829 | "the spec-plan-lifecycle rule defines" | "`LEDGER.md` defines" |
| W644–645 | "The spec-plan-lifecycle rule defines" (wraps after "The") | "`LEDGER.md` defines" |
| W790 | "the spec-plan-lifecycle rule owns it" | "`LEDGER.md` owns it" |
| W592 | "step 6 describes" | "the workflow rule's step 6 describes" |
| W797–799 | "the drop-or-wait question above" | "the drop-or-wait question the workflow rule's model selection asks" |
| L916–918 | "this sentence and the workflow rule's verdict-agent dispatch subsection state the same relay-before-stamp ordering and are edited together when that changes" | "this sentence and the bullet list under *Dispatching a verdict agent* above state the same relay-before-stamp ordering" |
| L919 | "The subsection sequences" | "That list sequences" |
| L922–923 | "defined in that subsection" | "defined under *What a diff-scoped LGTM certifies* above" |
| W129 | "the propagation gate below" | "the propagation gate above" |
| L987 | "is not that suggestion" | "is not the lifecycle rule's commit suggestion" |
| L988–989 | "The suggestion above says" | "That suggestion says" |
| L991–992 | "exactly as this paragraph describes it" | "exactly as that rule describes it" |
| L996 | "as the workflow rule's review loop says" | "as *The review loop* above says" |
| L998 | "One shape of that sooner call" | "One shape of the sooner commit the lifecycle rule leaves to the developer" |

W783 ("the resolution annotation the spec-plan-lifecycle rule defines"),
W332 and W343 stay: their targets stay in the lifecycle rule. Base lines
868–873, the promise to edit two homes together, are not carried: the
spec ends that promise (*The dispatcher's procedure*), and the moved
sentence takes the paragraph's place.

- [ ] **Step 5: Rewrite the pointers in `LEDGER.md`**

| Base line | Text | Becomes |
|---|---|---|
| L580 | "the case the workflow rule names" | "the case `PROCEDURE.md`, beside this file, names" |
| L588 | "the resolution annotation above already owes" | "the resolution annotation the spec-plan-lifecycle rule already owes" |
| L661 | "the Chain debt entry's owner leg" | "the owner leg of the Chain debt entry, in the `process-status` skill's `UNFINISHED-WORK.md`," |
| L691 | "The workflow rule owns the ask" | "`PROCEDURE.md` owns the ask" |
| L708 | "the one exception the workflow rule makes" | "the one exception `PROCEDURE.md` makes" |
| L769 | "bound in the workflow rule" | "bound in `PROCEDURE.md`" |
| L773 | "the workflow rule's report" | "the report `PROCEDURE.md` prescribes" |

- [ ] **Step 6: Verify the rewrites**

```bash
grep -c 'subsection' $D/PROCEDURE.md                 # 0
grep -c 'workflow rule' $D/PROCEDURE.md              # 2 (step 6, model selection)
grep -c 'spec-plan-lifecycle rule' $D/PROCEDURE.md   # 1 (resolution annotation)
grep -c 'LEDGER.md' $D/PROCEDURE.md                  # 10 or more
grep -c 'workflow rule' $D/LEDGER.md                 # 0
grep -c 'annotation above' $D/LEDGER.md              # 0
grep -c 'edited together' $D/PROCEDURE.md            # 0
diff <(git show $BASE:$W | sed -n '322,867p') <(sed -n '/^## Dispatching a verdict agent/,$p' $D/PROCEDURE.md | sed '/^### The audit pair at/,$d')   # every hunk is a row above; works whether or not Step 3 was committed
```

- [ ] **Step 7: Write `SKILL.md`**

Author it with the `skill-creator` discipline for the description only;
create no eval file. The content, verbatim:

```markdown
---
name: review-loop
description: "The dispatcher's procedure for the working process's review loop, and the grammar of the disposition ledger. Invoke before dispatching a verdict agent (architect, plan-adversary), at a consumption gate (before plan-writing or implementation), before a status move on a design spec, technical design or plan, and before writing a ledger line under a document's Review rounds section — the first time in a conversation, and again after a compaction. Instructions only: it dispatches no agent and runs no round."
---

# review-loop — the dispatcher's procedure and the ledger

This skill carries instructions and nothing else. It dispatches no
agent and runs no round. Read the reference your moment needs, whole,
before you act:

| You are about to… | Read |
|---|---|
| dispatch a verdict agent | `PROCEDURE.md`, then `LEDGER.md` |
| pass a consumption gate | `PROCEDURE.md`, then `LEDGER.md` |
| move a `status` | `PROCEDURE.md` |
| write a ledger line | `LEDGER.md` |

- `${CLAUDE_PLUGIN_ROOT}/skills/review-loop/PROCEDURE.md` — dispatching
  a verdict agent, the review loop, the stand-in and the provisional
  batch, the propagation gate, re-dispatch briefs, the terminators, what
  a diff-scoped LGTM certifies, the audit pair at the consumption gate,
  and per-round commits on a document branch.
- `${CLAUDE_PLUGIN_ROOT}/skills/review-loop/LEDGER.md` — the disposition
  ledger under `## Review rounds`: round headings, disposition lines,
  gate lines.

After a compaction this body returns and the references do not. Invoke
the skill again at the next of the four moments and re-read what it
routes to.

A reviewer or an auditor no longer receives the ledger grammar with the
document it reads. When you dispatch any agent on a document that
carries a `## Review rounds` section, give its brief the absolute path
of `LEDGER.md` and ask it to read that file first.

The four moments are listed in three places — the workflow rule's
pointer sentence, this skill's description, and the table above — and
the three are edited together.
```

- [ ] **Step 8: Verify the skill**

```bash
S=$D/SKILL.md
grep -c 'again after a compaction' $S               # 1
grep -c 'absolute path' $S                          # 1
grep -c 'edited together' $S                        # 1
for m in 'verdict agent' 'consumption gate' 'status move' 'ledger line'; do
  sed -n '3p' $S | grep -c "$m"; done               # 1 four times
claude plugin validate plugins/working-process      # passes
python3 -m unittest discover -s tests/working-process 2>&1 | tail -1   # OK
```

- [ ] **Step 9: Commit** — `feat(working-process): review-loop skill`

### Task 2: Cut `workflow.md`

**Files:**
- Modify: `plugins/working-process/rules/workflow.md`
- Modify: `plugins/working-process/SETTINGS_REGISTRY.md:122, 130`

**Interfaces:**
- Consumes: the skill and reference names from Task 1.

**Realizes:** D2, D3

- [ ] **Step 1: Delete the moved procedure and write the pointer**

Delete from the line after `## Dispatching a verdict agent` to the end
of the file. Keep the heading. Under it write, verbatim:

```markdown
When the `review-loop` skill is available, invoke it — the first time
in a conversation, and again after a compaction — before dispatching a
verdict agent (`architect`, `plan-adversary`), at a consumption gate,
before a `status` move, and before writing a ledger line. Its procedure
reference holds the dispatch procedure, the review loop, the stand-in
and the provisional batch, the propagation gate, re-dispatch briefs,
the terminators and what a diff-scoped LGTM certifies; its ledger
reference holds the disposition ledger and its gate lines.

When the `process-status` skill is available, its Unfinished-work
reference holds the Unfinished-work list; the skill reads it when the
developer asks what the process left unfinished.
```

- [ ] **Step 2: Move step 4's sequencing out**

Replace base lines 115–130 ("Where the technical-design offer is
accepted, the audit waits: the" through "has passed, leaving no
confirmed hit, when that agent is available.") with, at the step's
three-space indent:

```markdown
Where the technical-design offer is accepted, the audit waits until
the design exists and its review dispositions are applied; the audit
pair's sequencing at this gate is in the `review-loop` skill's
procedure reference, when that skill is available.
```

The first clause repeats the lifecycle rule's *Lifecycle offers*
("writing the design and applying its review dispositions precedes the
joint integrity audit"). "Then write the implementation plan…" through
"…cannot count on it loading." stays as written.

- [ ] **Step 3: Shorten steps 3 and 4**

Step 3 becomes, verbatim:

```markdown
3. **Grilled spec → architect review.** Offer a dispatch of the
   working-process `architect` agent (when available), on the most
   capable available model, named explicitly; dispatch, stamping and
   the propagation gate before each round follow the `review-loop`
   skill's procedure reference, when that skill is available. When the
   `propagation-auditor` agent is available, offer a propagation audit
   at authoring time as well, after any multi-site edit; that offer
   stands outside the loop.
```

The cut sentence — the audit gates that dispatch and every later
round — repeats *The propagation gate* in `PROCEDURE.md`.

In step 4, keep the sentence opening "It writes both ends" (102–105)
and the sentence opening "The plan written afterwards carries"
(109–113). They repeat the lifecycle rule's `technical-design:` bullet,
but that rule is not loaded when the offer is accepted (developer's
ruling, 2026-11-16).

Steps 1, 2, 5 and 7 lose no sentence.

- [ ] **Step 4: Rewrite the remaining pointers**

| Base line | Text | Becomes |
|---|---|---|
| 53–55 | "the pair-offer form the verdict-agent dispatch subsection defines" | "the pair-offer form the `review-loop` skill's procedure reference defines, when that skill is available" |
| 140–141 | "dispatch and stamping follow the verdict-agent dispatch subsection below" | "dispatch and stamping follow the `review-loop` skill's procedure reference, when that skill is available" |
| 150–151 | "a provisional decision, defined under *The stand-in and the provisional batch* below" | "a provisional decision, which the `review-loop` skill's procedure reference defines under *The stand-in and the provisional batch*, when that skill is available" |
| 155–156 | "under the dispatch-record store's `.gitignore` guard" | "in a store kept out of git by a `.gitignore` containing exactly `*`" |
| 184–185 | "running on the relay machinery the verdict-agent dispatch subsection already defines" | "running on the relay machinery the `review-loop` skill's procedure reference defines, when that skill is available" |
| 230–232 | "taking the timestamp shape of the two the verdict-agent dispatch subsection defines:" | "named `.claude/working-process/<stem>/<agent>-<date>-<HH-MM-SS>.md` — `<stem>` the subject, kebab-cased and capped at sixty characters, and a second record in the same second taking the lowest free counter suffix, `-2` then `-3` — in a store at the repo root kept out of git by a `.gitignore` containing exactly `*`:" |
| 300–301 | "which the spec-plan-lifecycle rule names" | "which the `review-loop` skill's procedure reference names, when that skill is available," |

- [ ] **Step 5: Update the registry**

`SETTINGS_REGISTRY.md`: under `## review.autonomy`,
`read-by: working-process/skills/review-loop/PROCEDURE.md`; under
`## review.per-round-commit`,
`read-by: working-process/skills/review-loop/PROCEDURE.md, working-process/rules/spec-plan-lifecycle.md`
(Task 3 drops the second file).

- [ ] **Step 6: Verify**

```bash
W=plugins/working-process/rules/workflow.md
grep -c '^### ' $W                                   # 0
grep -c '^## Dispatching a verdict agent$' $W        # 1
grep -c 'subsection' $W                              # 0
grep -c 'subsection below\|gate below\|batch\* below\|definition below' $W   # 0
grep -c 'Oscillation tripwire\|round cap' $W        # 0
grep -c 'review\.autonomy\|review\.per-round-commit' $W           # 0
grep -n -A1 'review-loop' $W                          # read: every pointer sentence carries "when that skill is available"
grep -c '^1\. \|^2\. \|^3\. \|^4\. \|^5\. \|^6\. \|^7\. ' $W      # 7
grep -c 'consult.personas\|design.technical-design-offer\|dispatch.propagation-auditor-tier\|ticket.root' $W   # 4 or more
wc -m < $W                                           # report; estimate 15,000, projection about 19,500
python3 -m unittest discover -s tests/working-process 2>&1 | tail -1   # OK
```

Read the shortened steps 3 and 4 against the base text and confirm no
decision left without a home (the first anti-goal).

- [ ] **Step 7: Commit** — `refactor(working-process): workflow rule keeps the offers, the procedure moves to review-loop`

### Task 3: Cut the ledger and the loop's text from the lifecycle rule

**Files:**
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md`
- Modify: `plugins/working-process/SETTINGS_REGISTRY.md:106, 130`

**Interfaces:**
- Consumes: the skill and reference names from Task 1.

**Realizes:** D4, D6

- [ ] **Step 1: Delete the ledger**

Delete from `## The disposition ledger` through "State prevents
relitigation, not the reviewer's memory." and its blank line (base
470–808). `## Unfinished-work list` now follows *Finding what revises a
document*; Task 4 moves it.

- [ ] **Step 2: Delete the relay-then-stamp sentence**

In *Lifecycle offers*, delete from "After any" (mid-line, base 914)
through "…waits for the confirming full-document round." (925). The
paragraph ends "…resolved entries sweep to the archive."

- [ ] **Step 3: Delete the per-round commit convention**

Delete from "Asking whether the loop may commit per round" through
"…the default path, where no sha exists." (base 987–1045). To the
paragraph before it, which ends "committing itself stays with the
developer.", append:

```markdown
One shape of that sooner commit, per-round commits on a document
branch, has a convention: when the `review-loop` skill is available,
its procedure reference holds it, with the document branch's merge at
this gate.
```

- [ ] **Step 4: Rewrite the kept pointer and add the closing pointer**

Base 54: "the provisional batch the workflow rule defines" becomes "the
provisional batch the `review-loop` skill's procedure reference
defines, when that skill is available,".

Before the last paragraph ("Ticket value format, sourcing order…"),
add:

```markdown
The disposition ledger — the round headings, disposition lines and gate
lines a document carries under `## Review rounds` — is defined in the
`review-loop` skill's ledger reference, when that skill is available.
```

- [ ] **Step 5: Update the registry**

Under `## docs-branch.merge` and under `## review.per-round-commit`:
`read-by: working-process/skills/review-loop/PROCEDURE.md`.

- [ ] **Step 6: Verify**

```bash
L=plugins/working-process/rules/spec-plan-lifecycle.md
grep -c '^## The disposition ledger\|^### Gate lines' $L          # 0
grep -c 'State prevents relitigation\|hit dismissed' $L           # 0
grep -c 'relay-before-stamp\|subsection' $L                       # 0
grep -c 'docs-branch\.merge\|review\.per-round-commit\|<topic>\.docs' $L   # 0
grep -c 'workflow rule' $L                                        # 2 (model selection, step 4)
grep -c '^## Ticket directories$\|^### Moving a document into a ticket directory$' $L   # 2
diff <(git show $BASE:$L | sed -n '204,292p') <(sed -n '/^## Ticket directories$/,/^## Decision register$/p' $L | sed '$d')   # empty
grep -n -A1 'review-loop' $L                                       # read: every pointer sentence carries "when that skill is available"
grep -l 'review.per-round-commit' plugins/working-process/rules plugins/working-process/skills -r   # PROCEDURE.md only
grep -l 'docs-branch.merge' plugins/working-process/rules plugins/working-process/skills plugins/working-process/agents -r   # PROCEDURE.md and rules/process-settings.md (a fenced example there, no reader)
python3 -m unittest discover -s tests/working-process 2>&1 | tail -1   # OK
```

If either `grep -l` lists another file that cites the key in backticks
outside a fence, add it to that key's `read-by:` line.

- [ ] **Step 7: Commit** — `refactor(working-process): disposition ledger and per-round commits move to review-loop`

### Task 4: The Unfinished-work list joins `process-status`

**Files:**
- Create: `plugins/working-process/skills/process-status/UNFINISHED-WORK.md`
- Modify: `plugins/working-process/skills/process-status/SKILL.md:8-19`
- Modify: `plugins/working-process/rules/spec-plan-lifecycle.md`

**Interfaces:**
- Produces: `UNFINISHED-WORK.md`, whose `## Unfinished-work list`
  heading the skill keys on.

**Realizes:** D6

- [ ] **Step 1: Extract and verify**

```bash
U=plugins/working-process/skills/process-status/UNFINISHED-WORK.md
{ printf '# process-status — the Unfinished-work list\n\n'
  git show $BASE:$L | sed -n '809,900p'; } > $U
diff <(sed '1,2d' $U) <(git show $BASE:$L | sed -n '809,900p')    # empty
```

- [ ] **Step 2: Rewrite its pointers**

"the resolution annotation above" (base 835–836) becomes "the resolution
annotation the spec-plan-lifecycle rule defines". "the list below" does
not occur here. Nothing else changes: "This section is the list" and
"the heading and the skill move together or not at all" stay, and are
still true.

- [ ] **Step 3: Delete the section from the lifecycle rule**

Delete `## Unfinished-work list` through "Either way the anchor stops
matching." and its blank line (base 809–901). At base 167, "so they
never match the list below" becomes "so they never match the
Unfinished-work list". Extend the closing pointer paragraph from Task 3
with a second sentence:

```markdown
The Unfinished-work list is the `process-status` skill's
Unfinished-work reference, when that skill is available.
```

- [ ] **Step 4: Point the skill at its reference**

In `process-status/SKILL.md`: lines 8–11 become "Runs the
Unfinished-work list its reference file publishes and reports what it
finds. The list owns which classes exist; this skill owns nothing but
running them, confirming their hits, and reporting. A class this skill
has never heard of works the moment the list publishes it." Step 1's
first paragraph becomes "Read the `## Unfinished-work list` section of
`${CLAUDE_PLUGIN_ROOT}/skills/process-status/UNFINISHED-WORK.md`, the
reference file shipped beside this skill." The failure rule (lines
26–30) stays as written.

- [ ] **Step 5: Verify**

```bash
grep -c '^## Unfinished-work list$' $U               # 1
grep -c '^- \*\*' $U                                 # 6 (the six classes)
grep -c 'annotation above' $U                        # 0
grep -c '^## Unfinished-work list' $L                # 0
grep -c 'Misplaced stamp\|the list below' $L         # 0
grep -c 'rules/spec-plan-lifecycle.md\|lifecycle rule' plugins/working-process/skills/process-status/SKILL.md   # 0
grep -c 'skills/process-status/UNFINISHED-WORK.md' plugins/working-process/skills/process-status/SKILL.md      # 1
wc -m < $L                                           # report; estimate 32,000
claude plugin validate plugins/working-process       # passes
```

- [ ] **Step 6: Commit** — `refactor(working-process): Unfinished-work list becomes a process-status reference`

### Task 5: Pointers in other files

**Files:**
- Modify: `plugins/working-process/README.md:93, 162, 214-217`
- Modify: `plugins/working-process/skills/grilling-session/SKILL.md:60`
- Modify: `docs/domain/glossary.md:450-460`

**Realizes:** D14

- [ ] **Step 1: Plugin README**

Line 93: "the lifecycle rule publishes" becomes "its reference file
publishes". Line 162: "section of the lifecycle rule" becomes "section
of the `process-status` skill's `UNFINISHED-WORK.md`". Lines 214–217:
the relay-then-stamp sequence is attributed to the `review-loop` skill,
and the two audit offers stay with the workflow rule; read the
paragraph to its end and keep the re-sync advice true.

- [ ] **Step 2: `grilling-session`**

Line 60: "the Grilling pending class of the lifecycle rule's
Unfinished-work list" becomes "the Grilling pending class of the
Unfinished-work list, a reference of the `process-status` skill".

- [ ] **Step 3: Glossary**

The **Unfinished-work list** entry opens "The reference file of the
`process-status` skill, `UNFINISHED-WORK.md`, holding one entry per
class of unfinished process work"; "costs one edit in the rule" becomes
"costs one edit in the list". The rest of the entry and its `_Avoid_`
line stay. Run the elements-of-style pass over the changed sentences.

- [ ] **Step 4: Verify**

```bash
grep -rn 'lifecycle rule.*Unfinished-work\|Unfinished-work.*lifecycle rule\|Unfinished-work list. section of the lifecycle' \
  plugins/working-process README.md docs/domain | wc -l           # 0
grep -c 'section of the spec-plan-lifecycle rule holding' docs/domain/glossary.md   # 0
grep -c 'UNFINISHED-WORK.md' docs/domain/glossary.md plugins/working-process/README.md   # 1 or more each
```

- [ ] **Step 5: Commit** — `docs(working-process): pointers follow the moved text`

### Task 6: Identity surfaces, changelog, version

**Files:**
- Modify: `plugins/working-process/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json:10`
- Modify: `README.md:19`
- Modify: `plugins/working-process/README.md:88-95`
- Modify: `plugins/working-process/CHANGELOG.md`

**Realizes:** D15

- [ ] **Step 1: Name the skill in all three identity surfaces**

In each description's skill list, write "process-status, process-setup,
review-loop and sync-rules skills". `plugin.json` is canonical; the
catalog entry and the README row carry the same list.

- [ ] **Step 2: Plugin README**

After the `process-status` bullet add a `review-loop` bullet: what it
holds (the dispatcher's procedure and the ledger grammar, as two
reference files), its four read moments, and that it dispatches
nothing.

- [ ] **Step 3: Changelog**

Under the existing `## Unreleased` heading add:

```markdown
- The dispatcher's procedure — verdict dispatch, the review loop, the
  stand-in, the propagation gate, re-dispatch briefs, the terminators,
  the diff-scoped LGTM, per-round commits — leaves the workflow rule,
  and the disposition ledger leaves the lifecycle rule, for a new
  `review-loop` skill. Invoke it before a verdict dispatch, at a
  consumption gate, before a `status` move and before writing a ledger
  line. No decision changes.
- The Unfinished-work list is now a reference file of `process-status`.
- A brief for any agent dispatched on a document with a
  `## Review rounds` section carries the ledger reference's path.
- Run `sync-rules` after updating: both rules shrink.
```

- [ ] **Step 4: Dogfood version**

```bash
git log develop --format=%H -- plugins/working-process/.claude-plugin/plugin.json |
  while read c; do git show "$c:plugins/working-process/.claude-plugin/plugin.json"; done |
  grep -o 'dev\.[0-9]*\.' | sort -t. -k2 -n | tail -1
```

Expected today: `dev.8.` Set `"version": "0.20.0-dev.9.process-context"`.
If the command prints a higher number, take the next one.

- [ ] **Step 5: Verify**

```bash
grep -c 'review-loop' plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md
# 1 each
grep -c '"version": "0.20.0-dev.9.process-context"' plugins/working-process/.claude-plugin/plugin.json   # 1
claude plugin validate . && claude plugin validate plugins/working-process   # both pass
```

- [ ] **Step 6: Commit** — `chore(working-process): review-loop identity surfaces, changelog, dogfood version`

### Task 7: Final verification

**Files:**
- Test: `tests/working-process/test_settings_registry.py`

**Realizes:** none

- [ ] **Step 1: Tests and validation**

```bash
python3 -m unittest discover -s tests/working-process 2>&1 | tail -3   # Ran 77 tests … OK
claude plugin validate . && claude plugin validate plugins/working-process
git diff --name-status $BASE -- plugins/working-process/rules | grep -c '^[AD]'    # 0: no rule file added or removed
git diff $BASE --stat -- plugins/working-process/hooks plugins/working-process/scripts | wc -l   # 0
```

- [ ] **Step 2: Every moved heading is gone from its old home and present in its new one**

```bash
P=plugins/working-process
for h in 'The review loop' 'The stand-in and the provisional batch' 'The propagation gate' \
         'Re-dispatch briefs' 'Terminators' 'What a diff-scoped LGTM certifies'; do
  echo "$h: $(grep -c "^### $h\$" $P/rules/workflow.md) $(grep -c "^### $h\$" $P/skills/review-loop/PROCEDURE.md)"
done                                                  # 0 1 on every line
echo "$(grep -c '^### Gate lines$' $P/rules/spec-plan-lifecycle.md) $(grep -c '^### Gate lines$' $P/skills/review-loop/LEDGER.md)"   # 0 1
```

- [ ] **Step 3: Pointer sweep**

```bash
grep -rn 'dispatch subsection\|propagation gate below\|provisional batch the workflow\|relay-before-stamp ordering and are edited' \
  plugins README.md docs/domain | wc -l               # 0
grep -rn 'workflow rule' plugins/working-process docs/domain README.md
```

Read every line the second command prints and confirm its target still
stands in `workflow.md`: model selection, the tier table, step 4, step
6, *Branch naming*, the consultation paragraphs. Report any other.

- [ ] **Step 4: Sizes**

```bash
wc -m plugins/working-process/rules/workflow.md plugins/working-process/rules/spec-plan-lifecycle.md \
      plugins/working-process/skills/review-loop/*.md plugins/working-process/skills/process-status/*.md
wc -l plugins/working-process/skills/review-loop/SKILL.md      # under 500
```

Report each rule beside its estimate: about 15,000 and about 32,000.

- [ ] **Step 5: Live checks, on the checkout's plugin**

The marketplace tracks `develop` on GitHub, so the topic branch's
version cannot be installed through it before the merge. The checks use
the live-session recipe instead, on the real configuration (a scratch
`CLAUDE_CONFIG_DIR` cannot authenticate a live session). Setup, the
developer's act, since it changes their environment:

1. `claude plugin disable working-process`, so the checkout's copy does
   not collide with the installed one;
2. `sync-rules` with the checkout's `plugins/working-process/rules` as a
   developer-named source, so the user-level rules are the new ones;
3. every `claude -p` below carries `--plugin-dir plugins/working-process`
   (an absolute path where it runs outside the repository).

Confirm first:

```bash
grep -c 'State prevents relitigation' ~/.claude/rules/working-process/spec-plan-lifecycle.md            # 0
```

Every run below adds `--output-format stream-json --verbose`, so its
output carries the token usage and the tool calls the checks read.

1. **Context measurement, one per document class.** In a scratch
   directory outside the repository, create `docs/specs/x-spec.md`,
   `docs/technical-designs/x-technical-design.md` and
   `docs/plans/x-plan.md`, each with frontmatter carrying `status:`.
   From that directory, for each document, run
   `claude -p --model haiku "Read the first twenty lines of <doc>. Then list the rule files injected into your context."`.
   Expected: `spec-plan-lifecycle.md` among the injected files in all
   three runs; the precondition's grep already shows the ledger text is
   gone from that rule. Report the files and each run's
   token count beside the 97,000-token figure in the spec.
2. **`process-status`.** In this repository, run
   `claude -p "/working-process:process-status"`. Expected: the report
   names all six Unfinished-work classes, and its output shows
   `UNFINISHED-WORK.md` read from the checkout's
   `plugins/working-process/skills/process-status/`.
3. **`review-loop` trigger.** In this repository, run
   `claude -p "Dispatch the plan-adversary on docs/plans/2026-11-16-process-context-plan.md; stop before dispatching and say what you read first."`.
   Expected: the transcript shows the `review-loop` skill invoked
   before any dispatch. One run is a signal, not proof for every
   session.

A miss in any of the three is reported, never a failure.

Teardown, the developer's act: `claude plugin enable working-process`,
then `sync-rules` from the installed plugin. Its rules are older than the
checkout's, so the Rules engine's direction gate asks before writing;
confirm it.

- [ ] **Step 6: Closing report**

Report the sizes, the measurement, the `workflow.md` shortfall, and
every provisional decision taken.

## Review rounds

### 2026-11-16 — plan-adversary, opus 5.5, concerns (round 1, full-document)

Record: `.claude/working-process/2026-11-16-process-context-plan/plan-adversary-round-1.md`. The gate lines below come from the pre-round propagation episode (haiku, one re-dispatch, clean).

- hit fixed 2026-11-16 — Task 1 Step 3's first `diff` printed a stray empty line: the stripped title left its blank line; `norm` now drops empty lines
- hit fixed 2026-11-16 — Task 2 Step 6's grep for `half-written` cannot reach 0 once step 4's kept sentence stays; the alternative is dropped
- hit fixed 2026-11-16 — Task 3 Step 6 expected `docs-branch.merge` in `PROCEDURE.md` only; `rules/process-settings.md` carries it in a fenced example, no reader; expectation corrected
- hit fixed 2026-11-16 — `PROCEDURE.md` keeps "the drop-or-wait question above", whose referent stays in `workflow.md`; Task 1 Step 4 gains the W797–799 row
- hit dismissed 2026-11-16 — `PROCEDURE.md`, `LEDGER.md`, `UNFINISHED-WORK.md` are names no source defines; counter: the spec names the references by role and leaves their file names to the plan, and D11 forbids paths, not names
- hit fixed 2026-11-16 — (auditor's judgment note) the inline consultation record name dropped the sixty-character stem cap and the collision counter; the Task 2 row now carries both
- fixed 2026-11-16 — [Important] Task 7 Step 5's context measurement ran under the developer's old user-level rules and would report a false miss; ruling: 2026-11-16; it runs after the developer installs the dogfood version and syncs the rules, on the real configuration, since a scratch `CLAUDE_CONFIG_DIR` cannot authenticate a live session
- fixed 2026-11-16 — [Important] Task 4 Step 5 invoked `process-status` before the dogfood version existed; ruling: 2026-11-16; the invocation moves to Task 7 Step 5, after the dogfood install, and checks the new cache directory
- fixed 2026-11-16 — [Minor] the skill's trigger was checked by grep only; ruling: 2026-11-16; Task 7 Step 5 adds one `claude -p` run asked to dispatch a plan-adversary, whose transcript must show `review-loop` invoked
- fixed 2026-11-16 — [Minor] the moved per-round section opens with "is not that suggestion", whose antecedent stays in the lifecycle rule; license: spec D12, pointers rewritten; Task 1 Step 4 gains an L987 row and L988 shortens to "That suggestion says"
- fixed 2026-11-16 — [Minor] Task 1 Step 6 expected `workflow rule` once in `PROCEDURE.md`, while the W797–799 gate fix adds a second; license: the gate line above; expectation now 2
- fixed 2026-11-16 — [Minor] Task 7 Step 1's `git status` check is vacuous once tasks are committed; license: spec *Verification*, no rule file added or removed; now `git diff --name-status $BASE`, no new command
- fixed 2026-11-16 — [Minor] the inline consultation record name lost "at the repo root"; license: spec anti-goal 1, no moved sentence changes meaning; the row 230–232 replacement now says it
- signal 2026-11-16 — a diff-scoped round on this wave would not earn its cost; the confirming full-document round owed by the plan will read these fixes
- hit fixed 2026-11-16 — the Task 1 Step 4 "owns it" pair turned W790 into "the spec-plan-lifecycle rule `LEDGER.md` owns it"; the row splits and W790 rewrites the whole phrase
- hit fixed 2026-11-16 — W645 reads "The" (capital, wrapped) and missed the lowercase anchor, while a text match would wrongly catch W783; W644–645 has its own row and rows match by line
- hit fixed 2026-11-16 — `$BASE` and `$L` are used in Task 3, 4 and 7 blocks that never set them; the method paragraph says every block assumes Task 1 Step 1's variables and a fresh shell sets them again
- hit fixed 2026-11-16 — the Architecture line said "byte-for-byte" while the check normalises whitespace; now "verbatim" and "whitespace-normalised", as the spec's *Verification* says
- hit fixed 2026-11-16 — Task 1 Step 4's "match it by its words, not by one line" contradicted the method paragraph's "rows match by the listed line"; Step 4 now says to find the phrase at the listed line by its words

### 2026-11-16 — plan-adversary, opus 5.5, concerns (round 2, full-document)

Record: `.claude/working-process/2026-11-16-process-context-plan/plan-adversary-round-2.md`. The confirming round.

- declined 2026-11-16 — [Minor] the relay-then-stamp sentence would merge into the preceding paragraph; ruling: 2026-11-16; base W866 is "document again." and W867 is the blank line, so the extraction already ends with the paragraph break
- fixed 2026-11-16 — [Minor] Task 1 Step 6's `git diff --stat` passes vacuously when Step 3's optional commit did not happen; license: Global Constraints, commits only where authorized; now a `diff` of the base range against `PROCEDURE.md`, no new command
- fixed 2026-11-16 — [Minor] Tasks 2 and 3 Step 6 expected `grep -vc 'available'` to print 0 while the prescribed pointer text wraps; license: the plan's own verbatim replacement texts; now `grep -n -A1` read by eye
- fixed 2026-11-16 — [Minor] Task 7 Step 5's measurement prompt contained the phrase it asked about; license: the precondition's grep already proves the ledger text is gone; the phrase question is dropped
- fixed 2026-11-16 — [Minor] the live checks' plain `claude -p` output carried neither the token count nor the tool calls; ruling: 2026-11-16; every run adds `--output-format stream-json --verbose`
- fixed 2026-11-16 — [Minor] `claude plugin update` cannot deliver the topic's version, since the marketplace tracks `develop`; ruling: 2026-11-16; Task 7 Step 5 uses the live-session recipe — the installed plugin disabled, `sync-rules` from the checkout, `--plugin-dir` on every run — with a teardown
- signal 2026-11-16 — no further round earns its cost: all five findings are Minor and none changes moved text or a pointer target

Round 2's `concerns` is resolved without a further round: the developer answered the three held findings on 2026-11-16 and closed the loop on the reviewer's stop signal, since every finding was Minor and none touched moved text or a pointer target.
