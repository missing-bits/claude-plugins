---
ticket: none
date: 2026-09-08
status: draft
adversary: concerns
spec: ../specs/2026-09-08-salesforce-trigger-frameworks-design.md
branch: feature/trigger-frameworks
base: develop
---

# Salesforce Trigger Frameworks Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `salesforce-triggers` skill — framework-independent trigger rules, the framework-resolution protocol, and three per-framework documents — and move trigger content out of `salesforce-apex` so the plugin serves base-class, metadata-driven and frameworkless projects, plus any framework a project documents itself.

**Architecture:** One new skill directory holds a hub `SKILL.md` and four `reference/` documents. The hub owns the rules and the protocol; each framework document answers the five questions the hub asks and carries its own signature, fingerprint row and rules. Four shipped surfaces change: `salesforce-apex` loses its trigger section and its worked example shrinks to the four framework-independent units, `salesforce-code-review` gains a resolution step, `/salesforce-review` resolves before dispatch, and the toolchain rule routes to the new skill and documents the two declaration keys. The reviewer agent's card is untouched.

**Tech Stack:** Markdown skill files with rule tags in the repo's tag grammar; Apex examples in fenced blocks that no compiler here checks; `grep`, `rg` and `awk` as the verification mechanism; `claude plugin validate` as the structural check.

## Global Constraints

- **The spec is the source.** Where this plan and `docs/specs/2026-09-08-salesforce-trigger-frameworks-design.md` disagree, the spec wins and the plan is wrong — except where the *Deviations from the spec* section below records a departure and its reason.
- **Rule tags follow `.claude/rules/standards-rule-tags.md`:** `(id: \`<rule-id>\`; severity: critical|important|minor[; kind: defect|hardening]; source: <source>)`, `kind` present exactly at critical, sub-rules under a `Sub-rules:` list with absolute severities never equal to the group default, no severity roll-up section anywhere. Cross-skill mentions cite the owning id and carry no severity word.
- **Rule ids:** `trigger-` in the hub, `trigger-base-class-`, `trigger-metadata-driven-` and `trigger-frameworkless-` in the framework documents. Findings cite `(standard: salesforce-triggers, rule: <id>)` for every one of them — a `reference/` document has no standard of its own.
- **The declaration keys never appear at the start of a line outside a fenced code block in any shipped file.** A line starting `trigger-framework:` or `vendor-paths:` in a shipped rule or skill would be read as a declaration by the very protocol it documents. Inline mentions sit in backticks mid-sentence; examples sit in fenced blocks. Task 11 sweeps for it.
- **Frontmatter safety:** no `description:` contains `: ` (colon-space); the two new descriptions are checked for it in Task 1 and Task 11.
- **No version bump.** `plugins/salesforce-standards/.claude-plugin/plugin.json` stays at `0.3.1`; the release PR mints the number, and this topic does not dogfood.
- **No eval files.** Neither `skill-creator` nor any agent writes `evals/trigger-evals.json` or any other eval file under the plugin — a standing decision of this repo. `skill-creator` may be used for `description:` tuning only.
- **Apex examples are valid, copy-pasteable Apex** for the file named above them, in the style of the existing `reference/` files: four-space indent, one class per block, explicit sharing keyword. No compiler runs here, so every block is written once into this plan and copied verbatim into the file — a fix to a shipped block is back-ported into this plan in the same wave.
- **Every framework document calls the same four lower-layer methods** the renamed `order-layers.md` defines: `OrderDomain.applyDefaults(List<Order>)`, `OrderDomain.validateStatusTransitions(List<Order>, Map<Id, Order>)`, `OrderDomain.filterNewlyActivated(List<Order>, Map<Id, Order>)` returning `List<Order>`, and `OrderService.activateFulfillment(List<Order>)`. Nothing else is called from a handler.
- **`claude plugin validate .` and `claude plugin validate plugins/salesforce-standards` must both pass** after every task.
- **Public-repo hygiene:** English only, no machine-specific paths, no company or client names, in files and commit subjects alike.
- **Commits are one line** — a conventional-commit subject, no body, no trailers of any kind.
- **Prose wraps at about 72 characters**, as the existing skills do; table rows, fenced code and tag lines run long.
- **Checks:** a check that searches for a prose phrase first normalizes whitespace — `tr -s '[:space:]' ' ' < "$file" | grep -o '<phrase>' | wc -l` — so a phrase straddling a line break is counted the same as one on a single line, with no judgement about where the wrap falls. A check asserting absence uses `grep -c` when it expects a printed `0` and `rg -l` when it expects no output — `rg -c` never prints `0`. Every check that verifies an edit states a before-value and an after-value that differ; a check that asserts an invariant says so on the step. Before-values below were measured on the tree at `develop` (`98de97e`) on 2026-09-08, which is the state the implementation branch starts from.
- **Branches.** Implementation runs on `feature/trigger-frameworks`, cut from `develop`. This plan and its spec live on `feature/trigger-frameworks.docs` and join the topic branch at the implementation-ready gate; the project has no `CLAUDE.md` note choosing fast-forward or squash, so the session asks once at that gate.

## Deviations from the spec

Recorded here and beside the text they concern, so a reviewer trips over the reason where the disagreement lives.

1. **The metadata-driven signature reads `header: TriggerAction.`, not `header: implements TriggerAction.`** The spec's example says `implements TriggerAction.` "matches … a class implementing something else besides", which holds only when the framework interface comes first: `implements Queueable, TriggerAction.BeforeInsert` does not contain that substring. The spec's own constraint — every test reduces to a grep — decides it. The shorter pattern matches every header naming a `TriggerAction.*` interface wherever it sits. Task 5 carries the sentence.
2. **One citation of the renamed file lives outside `salesforce-apex`.** The spec says "nothing outside the skill cites the filename"; `salesforce-apex-testing/reference/test-patterns.cls:4` does. Task 7 updates it, and the spec's sentence is reported as a spec defect rather than silently outrun — the plan corrects the file, not the claim.
3. **Context methods are overridden `public override`**, the form the fork's README shows, where the base class declares them `protected virtual`. Both compile; the spec prescribes neither.
4. **A `Framework types:` entry leaves the handler set even where its header matches the signature.** The spec says such types are "graded by no framework rule" and, separately, that "a class matching the signature is a handler on that match alone", without ordering the two. The plan orders them — the exemption wins — because every framework-owned class implementing the framework's own context interfaces would otherwise be graded as an action wherever the framework is vendored as source outside `vendor-paths:`; the metadata-driven framework ships two such classes, `MetadataTriggerHandler` and `TriggerActionFlow` (`TriggerActionFlow.cls:24`), and the second has a `Trigger_Action__mdt` record only where a Flow action is registered. The first spec sentence licenses the order; the spec's silence on it is reported. Task 1 carries the sentence in both the `Framework types:` bullet and the handler-set definition, and Task 5 names the instances.
5. **The hub does not say "as a minor rule".** The spec's Naming rule reads "each shipped document carries that name as a rule of its own, at minor severity"; a shipped surface restating a grade outside the tag is what `.claude/rules/standards-rule-tags.md` forbids, so the hub says "as a rule of its own" and the three documents' tags carry the grade. Not a spec defect — the tag rule binds plugin content, not design documents — but the phrase does not travel.

## File structure

Created:

- `plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md` — the hub: description, the five framework-independent rules, the framework-document contract and signature grammar, the resolution protocol.
- `plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-frameworkless.md`
- `plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-base-class.md`
- `plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-metadata-driven.md`
- `plugins/salesforce-standards/skills/salesforce-triggers/reference/choosing-a-framework.md` — the step (c) comparison.

Modified:

- `plugins/salesforce-standards/skills/salesforce-apex/SKILL.md` — description, intro, naming table, layers table, example pointer.
- `plugins/salesforce-standards/skills/salesforce-apex/reference/trigger-handler.md` → renamed `order-layers.md`, two sections removed.
- `plugins/salesforce-standards/skills/salesforce-apex/reference/bulkification.md:5` and `plugins/salesforce-standards/skills/salesforce-apex-testing/reference/test-patterns.cls:4` — the filename citation.
- `plugins/salesforce-standards/skills/salesforce-apex-testing/SKILL.md:12` — the layering sentence, which routed the handler to `salesforce-apex`.
- `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md` — Procedure step 2 gains the resolution step.
- `plugins/salesforce-standards/commands/salesforce-review.md` — a resolution step before dispatch.
- `plugins/salesforce-standards/rules/salesforce-toolchain.md` — routing line and the two keys.
- `plugins/salesforce-standards/README.md`, `plugins/salesforce-standards/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md` — the identity surfaces, in one commit.

Unchanged on purpose: `agents/salesforce-code-reviewer.md` (the skill owns the step; the card's "step 5" reference is why Task 8 adds to step 2 rather than renumbering).

---

### Task 1: The hub skill — rules and the framework-document contract

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md`

**Interfaces:**
- Produces: the seven rule ids `trigger-one-per-object`, `trigger-one-per-object.disjoint-contexts`, `trigger-body-delegates`, `trigger-context-below-handler`, `trigger-naming`, `trigger-framework-declared`, `trigger-framework-declared.ambiguous`; the `framework-id` table; the `Signature:` grammar with `header:`, `member:` and `Framework types:`; the heading `## Framework documents`, which Task 2 anchors on.
- Consumes: the four lower-layer method names from Global Constraints, by reference to `order-layers.md`, which Task 7 creates.

- [ ] **Step 1: Confirm the directory does not exist**

```bash
ls plugins/salesforce-standards/skills/salesforce-triggers 2>&1
```

Expected: `ls: cannot access ...: No such file or directory`.

- [ ] **Step 2: Write the file**

````markdown
---
name: salesforce-triggers
description: Use when writing or reviewing Apex triggers — one trigger per object, what belongs in the trigger body, resolving which trigger framework the project uses, and loading the matching framework guidance. Apex classes, layering and bulkification belong to salesforce-apex; Apex tests to salesforce-apex-testing.
---

# Salesforce triggers

Standards for Apex triggers that hold whatever trigger framework a
project uses, and the protocol that resolves which framework governs
the file at hand. Cite rules in review findings as
`(standard: salesforce-triggers, rule: <id>)`, the rules of a framework
document included; each rule names its source. Framework-specific
guidance — dispatch shape, bypass API, test isolation — lives in a
per-framework document under `reference/`, loaded once the framework is
resolved. Before the first trigger edit, and before grading the first
Apex file, run the protocol under "Resolving the framework" and write
the resolution record.

The layers below the handler — domain, service, selector — and
bulkification belong to `salesforce-apex`; Apex tests to
`salesforce-apex-testing`.

## Rules

These rules hold under every framework. Their ids carry the `trigger-`
prefix; a framework document's rules carry `trigger-<framework-id>-`.

### One trigger per object

An object has one `.trigger` file. Several handler calls inside that
file are correct, in the order they must run; the violation is a second
trigger file, never a second line. Scope: triggers under the
directories `packageDirectories` lists and outside `vendor-paths:` —
stated by path, because a vendor's trigger on a standard object belongs
to the vendor by path and to nobody by ownership.

(id: `trigger-one-per-object`; severity: critical; kind: defect; source:
Salesforce Well-Architected, record-triggered decision guide; Apex
Developer Guide p. 282)

Sub-rules:
- the two triggers declare disjoint contexts (id:
  `trigger-one-per-object.disjoint-contexts`; severity: important)

Two triggers whose declared contexts overlap fire in an order the
platform leaves undefined, so the same code yields different results
between runs. Disjoint contexts carry no ordering risk today, yet they
split an object's automation across files and sit one context
declaration away from the critical case.

### The trigger body delegates

The body contains delegating calls and nothing else — no conditional,
loop or field logic.

(id: `trigger-body-delegates`; severity: important; source: Apex
Developer Guide, "Document Your Apex Code")

### Context stops at the handler

Nothing below the handler reads `Trigger.*`; context descends as
parameters, which keeps the logic testable without DML. The types a
framework document lists under `Framework types:` are exempt — a base
class reading `Trigger.*` is the framework doing its job. This rule
needs a handler set, so it goes ungraded wherever no signature supplies
one.

(id: `trigger-context-below-handler`; severity: important; source: this
standard)

### Naming

A trigger is named `<Object>Trigger`. Pre-existing non-conforming names
stay; the convention binds new code. The dispatching class is named by
the framework document, which carries that name as a rule of its own.

(id: `trigger-naming`; severity: minor; source: this standard)

### The framework is declared

The project declares its trigger framework — the declaration under
"Resolving the framework". The finding lands in the report's
`## Project` section, and lands there even when inference succeeded:
inference resolves a session, a declaration resolves the project.

(id: `trigger-framework-declared`; severity: minor; source: this
standard)

Sub-rules:
- two declarations cover one path with different values and neither is
  a subtree strictly containing the other, so neither wins (id:
  `trigger-framework-declared.ambiguous`; severity: important)

The group default grades an absent declaration, which announces itself.
The sub-rule grades every case the protocol cannot rank — a glob-scoped
rule against a subtree-scoped `CLAUDE.md`, two rules whose `paths:`
differ, `CLAUDE.md` beside `.claude/CLAUDE.md` in one directory. A root
default with a nearer subtree override is not this finding: the inner
one wins, and the disagreement is stated in the resolution record.
Declarations that agree never reach the rule. The two dispositions are
mutually exclusive: a path has no declaration, or it has two the
protocol cannot rank.

### Bulkification

Owned by `salesforce-apex`: `apex-bulkification` and
`apex-bulkification.loop-on-trigger-path` grade the trigger path, and
this skill carries no grade of its own for it.

## Framework documents

One framework id names each shipped framework everywhere it appears —
declaration value, fingerprint row, document filename, rule prefix. A
shipped id names an approach, never a product: two base-class
frameworks share one document and one prefix.

| `framework-id` | Document | Rule prefix |
|---|---|---|
| `base-class` | `reference/framework-base-class.md` | `trigger-base-class-` |
| `metadata-driven` | `reference/framework-metadata-driven.md` | `trigger-metadata-driven-` |
| `frameworkless` | `reference/framework-frameworkless.md` | `trigger-frameworkless-` |

An id absent from this table is a framework this plugin does not ship.
Its declaration carries a `doc-path:` or a `skill:` locator, and this
table never grows to hold one. A `doc-path:` is read as a file relative
to the repository root; a `skill:` is invoked by its `plugin:skill`
name. A locator naming nothing takes the missing-document row of the
failure table. A document from outside this plugin is graded on the
rules above alone, never on its own framework rules; a signature
written in the grammar below buys it `trigger-context-below-handler`.

### What a document answers

Four questions, and a fifth for the documents this plugin ships. A
missing answer is stated to the developer, never filled from another
framework.

1. **Dispatch** — the trigger body and the handler shape, as two files
   calling the same lower-layer methods `salesforce-apex`'s
   `reference/order-layers.md` defines, plus the **signature** that
   makes a class one of this framework's handlers and the framework's
   **own types**, which are neither handlers nor layers below one.
2. **Context access** — where the handler reads `Trigger.*`.
3. **Bypass and recursion** — the API names *and* what happens when a
   limit is exceeded. `setMaxLoopCount(1)` guards under one base-class
   framework and silences automation under another; names alone cannot
   tell a reviewer which.
4. **Test isolation** — how to call the handler without DML, and how to
   disable it in a test.
5. **Fingerprint** — what identifies this framework in code: the row
   the document contributes to the fingerprint table below. The
   frameworkless answer is that nothing identifies it.

A document may add framework-specific rules, tagged like any rule here
under its prefix, and each shipped document carries the name of its
dispatching class as a rule of its own. A document carrying no rules is
graded by the rules above alone, and the report says so.

### The signature

The answer to question 1 is a block under a fixed heading, so a
session loading a document written elsewhere can tell whether the
contract is met — the base-class answer in full:

```
Signature:
  header: extends TriggerHandler
Framework types: TriggerHandler
```

- `header:` matches the type's declaration header — from the `class`
  or `interface` keyword to the opening brace, however the lines break.
  Modifiers before the keyword (`abstract`, `virtual`, `global`) sit
  outside the match. A comment, a string or a javadoc mention never
  counts.
- `member:` matches a method declaration line inside the type — where
  `handle(System.TriggerOperation`, the frameworkless answer, belongs.
- Matching ignores case, because Apex does. An optional namespace
  prefix is allowed before every type name: `extends acme.TriggerHandler`
  matches `extends TriggerHandler`.
- `Framework types:` names what the framework itself owns — a copied
  base class, a dispatcher. Absent and empty say the same thing:
  nothing. Its types are read to recognise the framework, graded by no
  framework rule, and exempt from `trigger-context-below-handler`. A
  type named here leaves the handler set even where its own header
  matches the signature: a framework class implementing the framework's
  own interfaces is the framework, not a handler.
- A filename glob may be added as a hint, never as the test.
- Only a malformed `Signature:` block fails the grammar.

A signature and a fingerprint share a technique and nothing else. A
fingerprint reads the whole project, matches anywhere, and yields a
label. A signature reads one class, matches in a named place, and
yields membership.

**The handler set** is the smallest fixed point of the classes matching
the signature, less the types `Framework types:` names, together with
the classes whose header `extends` a type already in the set — so
`OrderHandler extends BaseTriggerHandler`, an org's own layer over the
framework's, is graded. A class matching the signature is a handler on
that match alone unless `Framework types:` names it. The parent rules
govern **closure candidates** only — a class matching no signature whose header
carries `extends`:

- the parent is read from the repository even where it lies outside a
  diff-scoped run, so a full run and a diff-scoped run select the same
  handlers;
- a parent under a vendor path is read to recognise it and never
  graded;
- a parent absent from the repository leaves the candidate a
  non-handler. Such parents are reported in aggregate: one Summary line
  naming the distinct parents with a count each, ungraded. Most are
  platform types, `extends Exception` first. A namespace-qualified
  parent is the one worth a second look — as a reading hint, never as
  the test, since an unqualified absent parent can be the project's own
  base class where the repository is a partial view of the org.

Only top-level types are handlers. A document whose framework can
dispatch an inner type says so; such a type goes ungraded, and the
document says that too.

Every test in this skill reduces to a grep, a prefix comparison or a
glob match — never to parsing.
````

- [ ] **Step 3: Check the file's shape**

```bash
f=plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md
grep -c '(id:' "$f"                       # rule tags — no trailing space: a sub-rule tag wraps after `(id:`
grep -c 'severity: critical' "$f"         # the one critical rule
grep -c 'kind: defect' "$f"               # kind present exactly there
grep -c '^description: .*: ' "$f"         # frontmatter safety
grep -c '^## Framework documents$' "$f"   # Task 2's anchor
grep -c '^## Resolving the framework$' "$f"
```

Expected: `7`, `1`, `1`, `0`, `1`, `0`. The last is `0` here and `1` after Task 2; the fourth is an invariant and stays `0`.

- [ ] **Step 4: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
```

Expected: both pass — the new skill has a `name:` matching its directory and a quoted-safe description.

- [ ] **Step 5: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md
git commit -m "feat(salesforce-standards): add the salesforce-triggers skill with its framework-independent rules"
```

---

### Task 2: The hub skill — the resolution protocol

**Files:**
- Modify: `plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md` — insert a `## Resolving the framework` section directly before `## Framework documents`

**Interfaces:**
- Consumes: the heading `## Framework documents` from Task 1.
- Produces: the step letters (0), (a), (b), (c), (d); the fingerprint table; the resolution record's three-line shape; the failure table. Tasks 3–5 contribute rows to the fingerprint table by reference; Tasks 8 and 9 cite the step letters and the record.

- [ ] **Step 1: Measure before**

```bash
f=plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md
grep -c '^## ' "$f"
grep -c '^### ' "$f"
awk '/^```/{f=!f;next} !f' "$f" | grep -c '^trigger-framework:\|^vendor-paths:'
```

Expected: `2`, `8`, `0`. The first counts `## Rules` and `## Framework documents`; the second the six rule headings plus `### What a document answers` and `### The signature`; the third strips fenced blocks and counts declaration keys at line start outside them — an invariant that stays `0`.

- [ ] **Step 2: Insert the section**

Find the line `## Framework documents` and insert the following before it, followed by one blank line:

````markdown
## Resolving the framework

Three things are read from outside this skill, and they are not one
mechanism. A **signature** selects over a class's content and comes
from the framework document. A **declaration** resolves over a path,
comes from the project in several places, and carries a scope.
**`vendor-paths:`** filters over a path, comes from the repository root,
and carries no scope. Each is specified on its own; none inherits a
neighbour's rules.

### The declaration

One line, one key, in the body of a home file at the start of a line:

```
trigger-framework: base-class
trigger-framework: metadata-driven
trigger-framework: frameworkless
trigger-framework: acme-dispatcher; doc-path: docs/acme-triggers.md
trigger-framework: acme-dispatcher; skill: acme-plugin:acme-triggers
vendor-paths: force-app/nebula, force-app/vendor
```

- The key sits in the file's body, never in a rule's frontmatter, and a
  line inside a fenced code block does not count — which is how this
  file quotes the key without declaring one.
- One declaration per home, one value per key. The value is everything
  after the key, locator included: two homes naming one framework
  through different documents disagree.
- A shipped id carrying a locator is a contradiction: the shipped
  document is used and the locator reported. An id absent from the
  table below carrying no locator is a homegrown framework without a
  document.
- Two `trigger-framework:` lines in one home make that home
  unreadable; it is reported with the file, never resolved by picking a
  line.

**Homes** — the exact set a grep reads: `CLAUDE.md` and
`.claude/CLAUDE.md` at the repository root or in any directory above
the file, plus any rule file under `.claude/rules/` that sits outside a
directory carrying a Rules-engine manifest (`.manifest.json`). Grep
these files rather than waiting for the platform to load them: a
`CLAUDE.md` in a subdirectory loads only when a file there is read,
which a session about to write its first trigger has not done.

Not homes: a personal rule under `~/.claude/rules/`, which would follow
the developer between projects that disagree; `CLAUDE.local.md`,
personal and git-ignored, so a declaration there resolves the author's
sessions while every teammate and CI run reports it missing; and the
installed `salesforce-toolchain.md` copy, which the Rules engine owns
and overwrites at its next sync.

**Scope.** A `CLAUDE.md` scopes by position — the subtree of its
directory, and for `.claude/CLAUDE.md` the subtree of the directory
holding `.claude/`. A rule declaring `paths:` scopes by glob; a rule
declaring none scopes the whole repository, which is the root subtree
and ranks as one. Where a glob's coverage cannot be settled, the
pattern counts as covering: apply the matching the platform applies and
lean on `**`, `*`, `{a,b}` and root-relative paths alone.

**Ranking**, in three moves, every declaration keeping its own scope:

1. Count the distinct values. A root `CLAUDE.md` and a repository-wide
   rule naming the same framework agree; the record names both.
2. One distinct value — resolved.
3. More than one — the winner is the declaration whose scope is
   strictly contained in the scope of every declaration carrying a
   different value: subtree within subtree by path prefix, never a pair
   involving a glob. No such declaration means no winner, which the
   failure table turns into behaviour. `CLAUDE.md` beside
   `.claude/CLAUDE.md` in one directory carry equal subtrees, so
   neither contains the other; two rules with differing `paths:` are
   the same case.

### `vendor-paths:`

The second key, and the only other thing read from the project. It
lists what belongs to a package the project did not write, and the
scope is **declared, never inferred**: a package installed unlocked and
without a namespace, vendored as source, carries no platform signal
that marks it foreign.

- It resolves at the **repository root** alone. Every root home
  carries it — both root `CLAUDE.md` files and every rule file outside
  a payload directory, whatever its `paths:` — and several homes union.
  A scope rule would get an exclusion backwards.
- Its value is a list of **directory prefixes** relative to the root,
  not globs: a file is vendor when its path equals an entry or begins
  with the entry and a slash. That is the shape `packageDirectories`
  uses, so the two exclusion layers compose in one arithmetic.
- An absent key and an empty one say the same thing: nothing is vendor.
  An entry matching nothing on disk earns a note, the only signal an
  agent can give for a typo. An entry outside every package directory
  is redundant and passes in silence.
- Vendor code is never graded and never fingerprinted, and it is still
  **read** where recognition needs it: the discriminator separating the
  two base-class frameworks is a method name inside
  `TriggerHandler.cls`, which a project vendoring the framework as
  source puts under a vendor path.

### Steps

Resolution runs per file. For a trigger it decides which framework's
rules grade that trigger; for a class, the same from the declarations
covering the class's own path. Each step consumes what the one before
it produced.

| Step | Action |
|---|---|
| (0) | read `vendor-paths:` from the root homes and subtract it, with the directories outside `packageDirectories` (read from `sfdx-project.json`; where that file is absent this layer excludes nothing), from the repository's Apex files — what remains is the grading universe |
| (a) | grep the covering homes for `trigger-framework:` and rank them |
| (b) | fingerprint the grading universe, reading a framework's own types outside it where a fingerprint row points at a type `Framework types:` names |
| (c) | ask the developer, with `reference/choosing-a-framework.md` |
| (d) | select the resolved framework's handlers from the grading universe by its signature, closed over `extends` — the review surface alone |

Steps (0) through (c) serve a session writing a trigger and a review
run alike. A session about to write a trigger stops at the resolved
document; a review run takes step (d).

**Who repairs what.** Step (c) and a collision the protocol cannot rank
both need a person, so both belong to an interactive session. A
background agent asks nothing: it performs (0), (a) and (b) as
mechanical reads, enforces the rules it can resolve, and reports what
it cannot — step (c) and the offer to write a declaration are what it
never takes. A session does not settle an ambiguity in conversation
either, where the answer dies at the next compaction: it rescopes or
removes one of the competing homes until the declaration surface states
one framework per path. The fix is an edit, not an answer.

### Fingerprints

| Framework | Pattern |
|---|---|
| base-class | `extends TriggerHandler` with `new X().run()` |
| metadata-driven | `new MetadataTriggerHandler().run()` with `Trigger_Action__mdt` and `sObject_Trigger_Setting__mdt` records |
| fflib | `fflib_SObjectDomain.triggerHandler(` in the trigger body |
| TDTM | `TDTM_Config_API.run(` |
| dispatcher | `TriggerDispatcher.Run(`, or a handler implementing an interface with `IsDisabled()` |
| frameworkless | no pattern is not a fingerprint — go to step (c) |

Every pattern tolerates an optional namespace prefix in the form the
token's kind takes: `ns.` before a class name, `ns__` before an object
or Custom Metadata API name. Only the first three rows carry shipped
ids; `fflib`, `TDTM` and `dispatcher` are recognition labels naming what
was found, and a label becomes an id only when a declaration carries
it. The TDTM row is unverified against a real NPSP org: the pattern may
sit inside the package's own triggers under a vendor path, and the
subscriber-side signal may be `extends npsp.TDTM_Runnable`. A miss there
drops to step (c) and asks.

The base-class document separates two frameworks identical in the
trigger body and different in error semantics; its discriminator is a
method name inside `TriggerHandler.cls`, read when that document loads.

### The resolution record

Up to three lines, before the first trigger edit or the first graded
file:

```
Trigger framework: base-class — declared in force-app/billing/triggers/CLAUDE.md — loading framework-base-class.md
Vendor paths: 2 entries from CLAUDE.md
Handlers: 7 selected by the signature in framework-base-class.md
```

- The source reads `declared <file>`, `inferred <evidence>` or `asked`.
  It names every file that declares: where homes agree, all of them;
  where a nearer declaration beat a repository-wide default, both with
  the winner first. Where the document turns on a discriminator — the
  base-class case — the variant is named on this line.
- Any source other than `declared` ends with an offer to write the
  declaration, since a line in conversation dies at the next
  compaction. This skill never remembers a resolution; after compaction
  it reads the files again.
- The second and third lines say what the filter and the selector did,
  degrading in place — `none declared`, or the reason no handler set
  was selected. The `Handlers:` line appears only where step (d) ran.
  Without them "no framework findings" and "framework rules not graded"
  read identically.
- A monorepo yields one record per resolved framework with the paths it
  covers.

### Failure modes

| Situation | Behaviour |
|---|---|
| No declaration, fingerprint matches | infer, cite the file and pattern, offer to write the declaration |
| No declaration, no fingerprint | go to (c), saying no pattern matched in N triggers and asking whether the project is frameworkless or on a framework this plugin does not know |
| No triggers at all | go to (c) |
| A fingerprint matches a framework this plugin ships nothing for — fflib, TDTM, a dispatcher | the label is sound and only the document is missing: offer to write a project document, never substitute another framework's |
| Two subtree-scoped declarations disagree | the inner one wins, and the disagreement is always stated — never resolved silently |
| Two declarations cover the file with different values and neither is a subtree containing the other | no winner: name every file that declares, then work out with the developer which home survives and write that change — picking one silently would answer a question only the project can |
| The resolved document answers question 1 without a signature, or with one outside the grammar | skip the framework rules and `trigger-context-below-handler`, grade the rest, and name the document in the Summary — guessing a signature would repeat the mistake a filename pattern makes |
| A class matches two frameworks' signatures | grade it under the framework resolved for its own path — step (a) over the class — and name the other in the Summary |
| A closure candidate's `extends` parent is not in the repository | treat the class as a non-handler and count it on the Summary's one line of distinct unreadable parents; a class matching the signature itself is unaffected |
| The base-class framework arrives as a managed package, so `TriggerHandler.cls` cannot be read | select handlers as usual, grade every rule except those keyed to error semantics, and name in the Summary that the discriminator was unreadable — a guess between silencing and throwing is the one guess that turns a correct bypass into silenced automation |
| A home carries two `trigger-framework:` lines, or a shipped id with a locator | the home resolves nothing and is named; a shipped id keeps its shipped document and the stray locator is reported |
| `vendor-paths:` is absent and a directory is plainly third-party | grade it as the project's, since nothing declares otherwise, and note the directory with its evidence in the Summary — a note, not a finding, because no rule requires the key |
| A `vendor-paths:` entry matches nothing on disk | note it; nothing distinguishes a typo from a directory yet to be added |
| The declared document is missing | say so and grade by the framework-independent rules; never substitute another framework's document, since guidance for the wrong framework writes code that does not compile |
| A homegrown framework with no document | offer to write one, describing their code rather than a pattern from the internet |

Every note above lands among the Summary's out-of-scope notes, the slot
the review-report contract already defines; the declaration findings
land in `## Project`.
````

- [ ] **Step 3: Measure after**

```bash
f=plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md
grep -c '^## ' "$f"
grep -c '^### ' "$f"
grep -c '^## Resolving the framework$' "$f"
awk '/^```/{f=!f;next} !f' "$f" | grep -c '^trigger-framework:\|^vendor-paths:'
grep -c '^| (' "$f"                       # step rows
grep -c '^| No declaration' "$f"
```

Expected: `3`, `14`, `1`, `0`, `5`, `2`. The section adds six `###` headings — `The declaration`, `` `vendor-paths:` ``, `Steps`, `Fingerprints`, `The resolution record`, `Failure modes` — to Step 1's eight. The declaration-key count is the invariant from Step 1: the six example lines sit inside a fence, so stripping fences removes them, and the sentence "Two `trigger-framework:` lines" starts with a word.

- [ ] **Step 4: Check the section order**

```bash
grep -n '^## ' plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md
```

Expected: three lines, in this order — `## Rules`, `## Resolving the framework`, `## Framework documents`.

- [ ] **Step 5: Validate**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
```

Expected: both pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md
git commit -m "feat(salesforce-standards): add the trigger-framework resolution protocol"
```

---

### Task 3: The frameworkless framework document

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-frameworkless.md`

**Interfaces:**
- Consumes: the four lower-layer methods from Global Constraints; the `Signature:` grammar from Task 1.
- Produces: the rule ids `trigger-frameworkless-dispatching-class`, `trigger-frameworkless-entry-point`, `trigger-frameworkless-recursion-guard`; the signature `member: handle(System.TriggerOperation`.

- [ ] **Step 1: Write the file**

````markdown
# Frameworkless triggers

Framework id `frameworkless`. No base class and no metadata: the
trigger hands its context to one static entry point, and the handler
switches on the operation. Every rule here is cited
`(standard: salesforce-triggers, rule: trigger-frameworkless-<suffix>)`.

## Dispatch

The trigger reads the context once and passes it on. The handler owns
the switch, so `trigger-body-delegates` holds, and it takes the
operation as a parameter, so it is callable from a test without DML.

### `OrderTrigger.trigger`

```apex
trigger OrderTrigger on Order (before insert, before update, after update) {
    OrderTriggerHandler.handle(Trigger.operationType, Trigger.new, Trigger.oldMap);
}
```

### `OrderTriggerHandler.cls`

Routes each operation to the domain and service layers of
`salesforce-apex`'s `reference/order-layers.md`; no SOQL, no DML, no
business logic of its own. `with sharing`, the default for the handler
layer.

```apex
public with sharing class OrderTriggerHandler {

    @TestVisible
    private static Boolean disabled = false;

    public static void handle(System.TriggerOperation operation, List<Order> newOrders, Map<Id, Order> oldMap) {
        if (disabled) {
            return;
        }
        switch on operation {
            when BEFORE_INSERT {
                OrderDomain.applyDefaults(newOrders);
            }
            when BEFORE_UPDATE {
                OrderDomain.validateStatusTransitions(newOrders, oldMap);
            }
            when AFTER_UPDATE {
                List<Order> activated = OrderDomain.filterNewlyActivated(newOrders, oldMap);
                if (!activated.isEmpty()) {
                    OrderService.activateFulfillment(activated);
                }
            }
        }
    }
}
```

### Signature

```
Signature:
  member: handle(System.TriggerOperation
```

No `Framework types:` — nothing here belongs to a framework. A handler
is any top-level class declaring a method whose line carries
`handle(System.TriggerOperation`.

## Context access

The trigger reads `Trigger.operationType`, `Trigger.new` and
`Trigger.oldMap` once and passes them as parameters. The handler reads
nothing from `Trigger.*`, and neither does anything below it. On
insert `Trigger.oldMap` is null, so the `BEFORE_INSERT` branch never
touches `oldMap`.

## Bypass and recursion

Nothing in this shape bypasses or counts. The `disabled` flag above is
the bypass: `@TestVisible`, so a test can set it, and private, so
production code cannot. Recursion is the handler's own duty. A handler
whose after-context work performs DML that re-enters the same trigger
keeps a static set of ids already processed in this transaction and
skips them:

```apex
private static Set<Id> activatedThisTransaction = new Set<Id>();
```

What happens when a limit is exceeded: there is no limit to exceed. An
unguarded re-entry loops until a governor limit throws
`System.LimitException`, which no code catches, and the whole
transaction fails.

## Test isolation

Call the entry point with records built in memory — no `insert`, no
trigger context:

```apex
List<Order> orders = new List<Order>{ new Order(Status = null) };
OrderTriggerHandler.handle(System.TriggerOperation.BEFORE_INSERT, orders, null);
System.assertEquals('Draft', orders[0].Status);
```

To disable the handler in a test of other code that inserts orders,
set `OrderTriggerHandler.disabled = true` in the test and reset it in a
`finally` block.

## Fingerprint

Nothing identifies frameworkless code. The absence of every other
fingerprint is not a match: step (b) of the resolution protocol falls
through to step (c), which asks.

## Rules

**Dispatching class.** The handler is named `<Object>TriggerHandler`.
Pre-existing non-conforming names stay; the convention binds new code.

(id: `trigger-frameworkless-dispatching-class`; severity: minor;
source: this standard)

**One entry point.** Every call in the trigger body is a handler's
static `handle` method taking `System.TriggerOperation` and the
records — several handlers, several such calls. A call to a per-context
method instead — `handleBeforeInsert`, with or without a branch around
it — leaves that handler outside the signature, where no framework rule
reaches it. The rule is graded on the trigger for that reason: the
class it would grade cannot be selected.

(id: `trigger-frameworkless-entry-point`; severity: important; source:
this standard)

**Recursion guard.** A handler whose after-context work performs DML on
its own object, or on an object whose automation writes back, keeps a
static processed-id set and skips ids already seen. Nothing else in
this shape stops re-entry.

(id: `trigger-frameworkless-recursion-guard`; severity: important;
source: this standard)

## Gotchas

- `Trigger.new` is a `List<SObject>` and is assignable to a
  `List<Order>` parameter without a cast; `Trigger.oldMap` to
  `Map<Id, Order>` likewise.
- A `switch on` an enum needs no `when else`; an unlisted operation
  falls through and does nothing, which is the intended behaviour for
  a context the trigger does not declare.
- The `disabled` flag is per handler class. A test that inserts several
  objects disables each handler it must silence.
- The shape this plugin shipped before `salesforce-triggers` existed —
  static `handleBeforeInsert` methods and a trigger branching on
  `Trigger.isBefore` — now earns two findings on the trigger,
  `trigger-body-delegates` and, once the project resolves as
  `frameworkless`, `trigger-frameworkless-entry-point`, and its handler
  matches no signature. One fix clears all three: keep the methods, add
  one `handle` entry point that switches on the operation and calls
  them, and make the trigger call it.
````

- [ ] **Step 2: Check the file's shape**

```bash
f=plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-frameworkless.md
grep -c '(id: `trigger-frameworkless-' "$f"
grep -c 'severity: critical' "$f"
grep -c '^Signature:$' "$f"
grep -c '^  member: \|^  header: ' "$f"
grep -c '^### `Order' "$f"
grep -c 'OrderDomain\.\|OrderService\.' "$f"
```

Expected: `3`, `0`, `1`, `1`, `2`, `4`. The last counts the lines calling lower-layer methods — the three domain calls and one service call inside the handler block.

- [ ] **Step 3: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
git add plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-frameworkless.md
git commit -m "feat(salesforce-standards): add the frameworkless trigger document"
```

Expected: validation passes; one commit.

---

### Task 4: The base-class framework document

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-base-class.md`

**Interfaces:**
- Consumes: the four lower-layer methods; the `Signature:` grammar; the fingerprint row for `base-class` in Task 2's table.
- Produces: the rule ids `trigger-base-class-dispatching-class`, `trigger-base-class-bypass-restored`, `trigger-base-class-loop-count`; the discriminator pair `incrementCheckLoopCount` / `addToLoopCount`.

Facts below were read from the two frameworks' sources on 2026-09-08: `kevinohara80/sfdc-trigger-framework` (`src/classes/TriggerHandler.cls`) and `dschach/salesforce-trigger-framework` (`force-app/main/default/classes/TriggerHandler.cls`, `README.md`).

- [ ] **Step 1: Write the file**

````markdown
# Base-class trigger framework

Framework id `base-class`. One approach, two products: the original
`kevinohara80/sfdc-trigger-framework` and its maintained fork
`dschach/salesforce-trigger-framework`. Both are a `virtual` class
`TriggerHandler` copied into the org or installed as a package; a
handler extends it and overrides the context methods it needs. Every
rule here is cited
`(standard: salesforce-triggers, rule: trigger-base-class-<suffix>)`.

## Dispatch

### `OrderTrigger.trigger`

```apex
trigger OrderTrigger on Order (before insert, before update, after update) {
    new OrderTriggerHandler().run();
}
```

### `OrderTriggerHandler.cls`

Casts the context once in the constructor, then routes each context to
the domain and service layers of `salesforce-apex`'s
`reference/order-layers.md`; no SOQL, no DML, no business logic of its
own. `with sharing`, the default for the handler layer.

```apex
public with sharing class OrderTriggerHandler extends TriggerHandler {

    private List<Order> newOrders;
    private Map<Id, Order> oldMap;

    public OrderTriggerHandler() {
        this.newOrders = (List<Order>) Trigger.new;
        this.oldMap = (Map<Id, Order>) Trigger.oldMap;
    }

    public override void beforeInsert() {
        OrderDomain.applyDefaults(newOrders);
    }

    public override void beforeUpdate() {
        OrderDomain.validateStatusTransitions(newOrders, oldMap);
    }

    public override void afterUpdate() {
        List<Order> activated = OrderDomain.filterNewlyActivated(newOrders, oldMap);
        if (!activated.isEmpty()) {
            OrderService.activateFulfillment(activated);
        }
    }
}
```

### Signature

```
Signature:
  header: extends TriggerHandler
Framework types: TriggerHandler
```

`TriggerHandler` is the framework's own type: read to recognise the
framework, graded by no rule here, and exempt from
`trigger-context-below-handler`.

## Context access

The base class reads `Trigger.isExecuting` and `Trigger.operationType`
in `run()` to pick the context method — which is why it is a framework
type. The handler reads `Trigger.new` and `Trigger.oldMap` once, in its
constructor, into typed fields; the context methods and everything
below them read nothing from `Trigger.*`.

## Bypass and recursion

Common to both products, all static on `TriggerHandler` unless noted:

| Call | Effect |
|---|---|
| `TriggerHandler.bypass('OrderTriggerHandler')` | skips that handler for the rest of the transaction |
| `TriggerHandler.clearBypass('OrderTriggerHandler')` | restores it |
| `TriggerHandler.isBypassed('OrderTriggerHandler')` | asks |
| `TriggerHandler.clearAllBypasses()` | clears every bypass |
| `this.setMaxLoopCount(n)`, `this.clearMaxLoopCount()` | instance methods: cap how many times this handler's `run()` executes in one transaction |

The fork adds `bypass(Type)` and `bypass(List<String>)` overloads,
`bypassAll()` with `clearGlobalBypass()`, `setBypass(name, Boolean)`,
`bypassList()` and `getLoopCount(name)`, and its `setMaxLoopCount`
returns the handler so calls chain. The fork's README documents
`TriggerHandler.setGlobalBypass()`, which its source does not define —
the method is `bypassAll()`.

**What happens when the loop count is exceeded** is where the two
products part, and the difference sits in one private method of
`TriggerHandler.cls`:

| Product | Method | Behaviour |
|---|---|---|
| original | `addToLoopCount()` | throws `TriggerHandlerException('Maximum loop count of N reached in <handler>')`, and the DML fails |
| fork | `incrementCheckLoopCount()` | returns without running the handler; a `System.debug` line is the only trace, and the `throw` sits commented out beside `// Do not throw an exception if we exceed the loop count - just stop executing` |

So `setMaxLoopCount(1)` is a recursion guard under the original and
silences automation under the fork. The discriminator is read from
`TriggerHandler.cls` when this document loads, and the variant goes on
the resolution record's first line.

Where that file is unreadable — a managed package — a namespace or the
package version may still tell the two apart. Where nothing does, an
authoring session states both semantics and says the installed package
decides which holds; a review run grades every rule below except the
one keyed to error semantics, `trigger-base-class-loop-count`, and
names in the Summary that the discriminator was unreadable. Nobody
guesses between silencing and throwing.

## Test isolation

`run()` requires trigger context — the base class checks
`Trigger.isExecuting`, and the handler's constructor casts
`Trigger.new` — so the handler cannot be called without DML. Test the
layers below directly (`OrderDomain`, `OrderService`), and give the
handler one DML-backed test per context that asserts the outcome.

To disable the handler in a test of other code that inserts orders:

```apex
Account acc = TestDataFactory.createAccounts(1)[0];
TriggerHandler.bypass('OrderTriggerHandler');
try {
    TestDataFactory.createOrders(200, acc.Id);
} finally {
    TriggerHandler.clearBypass('OrderTriggerHandler');
}
```

The factory inserts the records itself, as `salesforce-apex-testing`
requires, and its `createOrders` takes the parent account's id; the
bypass wraps the call that fires the trigger.

## Fingerprint

`extends TriggerHandler` in a class header together with
`new X().run()` in a trigger body, an optional namespace prefix before
`TriggerHandler`. The discriminator: `incrementCheckLoopCount` in
`TriggerHandler.cls` means the fork, which silences;
`addToLoopCount` means the original, which throws.

## Rules

**Dispatching class.** The handler is named `<Object>TriggerHandler`.
Pre-existing non-conforming names stay; the convention binds new code.

(id: `trigger-base-class-dispatching-class`; severity: minor; source:
this standard)

**A bypass is restored.** In non-test code every `bypass(...)` is
paired with the matching `clearBypass(...)` in a `finally` block. A
bypass left set silences the object's automation for every caller
later in the same transaction.

(id: `trigger-base-class-bypass-restored`; severity: important; source:
this standard)

**The loop count is not the recursion logic.** Under the fork,
`setMaxLoopCount` drops the handler's work without a signal, so
re-entry is controlled by state — a static set of processed ids — and
any `setMaxLoopCount` call carries a comment naming the silencing.
Under the original, `setMaxLoopCount` is a legitimate guard, and a
count above 1 is justified in a comment. This rule is keyed to the
error semantics above and goes ungraded where the discriminator is
unreadable.

(id: `trigger-base-class-loop-count`; severity: important; source: this
standard)

## Gotchas

- The handler name a bypass string must match is derived from the
  class: the fork reads `toString()` (`getHandlerName()`) unless the
  constructor passed `super('OrderTriggerHandler')`. Prefer the fork's
  `bypass(OrderTriggerHandler.class)` overload where it exists — a Type
  cannot be misspelt.
- The context methods are `protected virtual` in the base class;
  overriding them `public override` widens access and compiles under
  both products, and is the form the fork's README shows.
- A handler constructed outside a trigger has null `Trigger.new`; the
  casts above are safe only because `run()` refuses to execute outside
  trigger context.
````

- [ ] **Step 2: Check the file's shape**

```bash
f=plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-base-class.md
grep -c '(id: `trigger-base-class-' "$f"
grep -c 'severity: critical' "$f"
grep -c '^Signature:$' "$f"
grep -c '^  header: extends TriggerHandler$' "$f"
grep -c '^Framework types: TriggerHandler$' "$f"
grep -c '^### `Order' "$f"
grep -c 'incrementCheckLoopCount\|addToLoopCount' "$f"
```

Expected: `3`, `0`, `1`, `1`, `1`, `2`, `4`. The last counts lines naming a discriminator method: two table rows and two lines in the Fingerprint section.

- [ ] **Step 3: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
git add plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-base-class.md
git commit -m "feat(salesforce-standards): add the base-class trigger framework document"
```

Expected: validation passes; one commit.

---

### Task 5: The metadata-driven framework document

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-metadata-driven.md`

**Interfaces:**
- Consumes: the four lower-layer methods; the `Signature:` grammar; the fingerprint row for `metadata-driven`.
- Produces: the rule ids `trigger-metadata-driven-dispatching-class`, `trigger-metadata-driven-action-registered`, `trigger-metadata-driven-bypass-restored`, `trigger-metadata-driven-order-explicit`; the signature `header: TriggerAction.`.

Facts below were read from `mitchspano/apex-trigger-actions-framework` on 2026-09-08: `TriggerBase.cls`, `TriggerAction.cls`, `MetadataTriggerHandler.cls`, and the field directories of `Trigger_Action__mdt` and `sObject_Trigger_Setting__mdt`.

- [ ] **Step 1: Write the file**

````markdown
# Metadata-driven trigger framework

Framework id `metadata-driven`. The reference implementation is
`mitchspano/apex-trigger-actions-framework`. One trigger per object
calls `new MetadataTriggerHandler().run()`, and Custom Metadata records
name the classes to run and their order — one
`sObject_Trigger_Setting__mdt` record per object, one
`Trigger_Action__mdt` record per action and context. An action is any
class implementing one of the `TriggerAction.*` interfaces; changing
the order is a metadata deployment, not a code one. Every rule here is
cited
`(standard: salesforce-triggers, rule: trigger-metadata-driven-<suffix>)`.

## Dispatch

### `OrderTrigger.trigger`

```apex
trigger OrderTrigger on Order (before insert, before update, after update) {
    new MetadataTriggerHandler().run();
}
```

### `OrderTriggerHandler.cls`

One class carrying the object's three actions, each an interface
method the framework calls with `List<SObject>` arguments. It routes to
the domain and service layers of `salesforce-apex`'s
`reference/order-layers.md`; no SOQL, no DML, no business logic of its
own. `with sharing`, the default for the handler layer.

```apex
public with sharing class OrderTriggerHandler implements TriggerAction.BeforeInsert, TriggerAction.BeforeUpdate, TriggerAction.AfterUpdate {

    public void beforeInsert(List<SObject> triggerNew) {
        OrderDomain.applyDefaults((List<Order>) triggerNew);
    }

    public void beforeUpdate(List<SObject> triggerNew, List<SObject> triggerOld) {
        Map<Id, Order> oldMap = new Map<Id, Order>((List<Order>) triggerOld);
        OrderDomain.validateStatusTransitions((List<Order>) triggerNew, oldMap);
    }

    public void afterUpdate(List<SObject> triggerNew, List<SObject> triggerOld) {
        Map<Id, Order> oldMap = new Map<Id, Order>((List<Order>) triggerOld);
        List<Order> activated = OrderDomain.filterNewlyActivated((List<Order>) triggerNew, oldMap);
        if (!activated.isEmpty()) {
            OrderService.activateFulfillment(activated);
        }
    }
}
```

### The metadata

Nothing in code names the class; the records do. One
`sObject_Trigger_Setting__mdt` record and three `Trigger_Action__mdt`
records deploy with the code:

| Record | Type | Key fields |
|---|---|---|
| `Order` | `sObject_Trigger_Setting__mdt` | `Object_API_Name__c = Order` |
| `Order_Before_Insert` | `Trigger_Action__mdt` | `Apex_Class_Name__c = OrderTriggerHandler`, `Before_Insert__c = Order`, `Order__c = 1` |
| `Order_Before_Update` | `Trigger_Action__mdt` | `Apex_Class_Name__c = OrderTriggerHandler`, `Before_Update__c = Order`, `Order__c = 1` |
| `Order_After_Update` | `Trigger_Action__mdt` | `Apex_Class_Name__c = OrderTriggerHandler`, `After_Update__c = Order`, `Order__c = 1` |

Each context field (`Before_Insert__c`, `Before_Update__c`,
`After_Insert__c`, `After_Update__c`, `Before_Delete__c`,
`After_Delete__c`, `After_Undelete__c`) is a lookup to the object's
setting record; a record enables exactly the contexts it fills.

### Signature

```
Signature:
  header: TriggerAction.
Framework types: TriggerBase, MetadataTriggerHandler, TriggerAction, TriggerActionFlow, FinalizerHandler
```

The pattern is `TriggerAction.` rather than `implements TriggerAction.`
on purpose: a class declared `implements Queueable,
TriggerAction.BeforeInsert` names the framework interface second, and a
header test is a substring match. Any header naming a `TriggerAction.*`
interface, wherever it sits in the `implements` list, selects the
class. Two framework classes match it themselves —
`MetadataTriggerHandler` and `TriggerActionFlow`, each implementing all
seven context interfaces — and both sit under `Framework types:`, which
removes them from the handler set; `TriggerActionFlowChangeEvent
extends TriggerActionFlow` is then a closure candidate whose parent is
not in the set, and stays out too. The framework types appear in the
repository only where the framework arrives as source; listing them
costs nothing where it does not.

## Context access

The framework reads `Trigger.*` in `TriggerBase.run()` and hands each
action `triggerNew` and `triggerOld` as `List<SObject>`. An action
reads nothing from `Trigger.*`; it casts the lists and, where it needs
the old records by id, builds `new Map<Id, Order>((List<Order>)
triggerOld)` — the framework passes no map.

## Bypass and recursion

| Call | Effect |
|---|---|
| `TriggerBase.bypass('Order')`, `clearBypass`, `isBypassed` | every action on the object; `Schema.SObjectType` overloads exist |
| `TriggerBase.clearAllBypasses()` | clears every object bypass |
| `MetadataTriggerHandler.bypass('OrderTriggerHandler')`, `clearBypass`, `isBypassed` | one action, by class name or `System.Type` |
| `MetadataTriggerHandler.clearAllBypasses()` | clears every action bypass |
| `Bypass_Execution__c` on either record type | disables the object or the action without a deployment of code |
| `Bypass_Permission__c`, `Required_Permission__c` | a custom permission whose holders skip the action, or without which it does not run |

**Recursion.** No loop count exists here. The framework counts how
often each record id has been seen in the update contexts —
`TriggerBase.idToNumberOfTimesSeenBeforeUpdate` and
`TriggerBase.idToNumberOfTimesSeenAfterUpdate`, both
`Map<Id, Integer>` — and leaves the decision to the action: one that
must act once checks that the count for the record is 1. What happens
when a limit is exceeded: nothing is exceeded. An action ignoring the
maps re-enters until a governor limit throws `System.LimitException`
and the transaction fails.

**A stale record fails the object.** `MetadataTriggerHandler`
instantiates each action with `Type.forName(Apex_Class_Name__c)`; a
name resolving to no class, or to a class not implementing the
context's interface, throws `MetadataTriggerHandlerException` — and
every DML on that object fails until the record is fixed.

## Test isolation

An action is a plain class: instantiate it and call the interface
method with records built in memory, no DML and no metadata read:

```apex
List<Order> orders = new List<Order>{ new Order(Status = null) };
new OrderTriggerHandler().beforeInsert(orders);
System.assertEquals('Draft', orders[0].Status);
```

To disable the handler in a test of other code that inserts orders,
call `MetadataTriggerHandler.bypass('OrderTriggerHandler')` before the
DML and `clearBypass` in a `finally` block; `TriggerBase.bypass('Order')`
silences every action on the object the same way.

## Fingerprint

`new MetadataTriggerHandler().run()` in a trigger body together with
`Trigger_Action__mdt` and `sObject_Trigger_Setting__mdt` records in the
repository — an optional `ns.` before the class and `ns__` before the
metadata API names. The row keys on records and the trigger body, never
on the framework's classes: the records sit in the repository whether
the framework arrives as an unlocked package or as source, while the
classes appear only in the second case.

## Inner classes

`Type.forName('Outer.Inner')` resolves, so an inner class can be
registered as an action. The signature grammar selects top-level types
only; an inner-class action is therefore not graded by the rules below,
and this document says so rather than leaving it to a reader. The
convention here is a top-level class per action or per object.

## Rules

**Dispatching class.** A class carrying an object's actions is named
`<Object>TriggerHandler`; where actions split by feature, each is
`<Object><Feature>Action`. Pre-existing non-conforming names stay; the
convention binds new code.

(id: `trigger-metadata-driven-dispatching-class`; severity: minor;
source: this standard)

**Every action is registered, and every record resolves.** Each
`Trigger_Action__mdt` record's `Apex_Class_Name__c` names a class in
the repository implementing the interface of every context the record
enables, and every class implementing one of the seven context
interfaces — `BeforeInsert` through `AfterUndelete` — has a record. A
stale name fails every DML on the object at runtime; an unregistered
action never runs. A `TriggerAction.DmlFinalizer` implementer is
selected as a handler by the signature but registered through a
different record type, so this rule leaves it alone.

(id: `trigger-metadata-driven-action-registered`; severity: important;
source: this standard)

**A bypass is restored.** In non-test code every `TriggerBase.bypass`
or `MetadataTriggerHandler.bypass` is paired with the matching
`clearBypass` in a `finally` block. A bypass left set silences
automation for every caller later in the same transaction.

(id: `trigger-metadata-driven-bypass-restored`; severity: important;
source: this standard)

**Order is explicit.** Every `Trigger_Action__mdt` record carries an
`Order__c` value, unique among the records enabling the same object and
context. Two actions on one order leave their sequence to the query.

(id: `trigger-metadata-driven-order-explicit`; severity: minor; source:
this standard)

## Gotchas

- `triggerOld` is a `List<SObject>`, not a map; build the map in the
  action.
- The Custom Metadata type and its records deploy together with the
  framework; a record naming a class that is not yet deployed fails the
  object's DML from the first save.
- Flow actions (`Flow_Name__c`) run through the same records and are
  outside this document.
````

- [ ] **Step 2: Check the file's shape**

```bash
f=plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-metadata-driven.md
grep -c '(id: `trigger-metadata-driven-' "$f"
grep -c 'severity: critical' "$f"
grep -c '^Signature:$' "$f"
grep -c '^  header: TriggerAction\.$' "$f"
grep -c '^### `Order' "$f"
grep -c '^| `Order' "$f"
```

Expected: `4`, `0`, `1`, `1`, `2`, `4`. The last counts the metadata table's record rows: one setting and three actions.

- [ ] **Step 3: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
git add plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-metadata-driven.md
git commit -m "feat(salesforce-standards): add the metadata-driven trigger framework document"
```

Expected: validation passes; one commit.

---

### Task 6: The step (c) comparison

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-triggers/reference/choosing-a-framework.md`

**Interfaces:**
- Consumes: the three framework ids and the recognition labels from Task 2.

- [ ] **Step 1: Write the file**

````markdown
# Choosing a trigger framework

Read at step (c) of the resolution protocol, when neither a declaration
nor a fingerprint settled the framework. Present the case for and
against each shipped approach; the developer chooses; the session
writes the declaration — a `trigger-framework:` line in the root
`CLAUDE.md` or the trigger directory's — so the question is not asked
again. The developer's existing code decides more than any argument
here: a project already extending a base class has chosen.

## Base-class (`base-class`)

**For.** One virtual class copied into the org, no metadata to
maintain, and a handler shape every Salesforce developer recognises.
Bypass and loop-count APIs come with it. Two products share the shape,
so hiring and code review carry over.

**Against.** Execution order within a context is the order of calls in
the handler, so reordering is a code deployment. The handler cannot be
called without DML, so handler tests are integration tests. The two
products differ in what an exceeded loop count does — one throws, one
silences — and the difference is a private method in a class the
project copied and may have edited.

## Metadata-driven (`metadata-driven`)

**For.** Order and bypasses live in Custom Metadata, so an admin can
reorder or disable an action without a deployment of code. An action
is a plain class implementing an interface, callable in a test without
DML. Permission-based bypasses come with it.

**Against.** A stale metadata record fails every DML on its object.
The dispatch is invisible in code — a reader must open the records to
learn what runs — and a trigger that runs nothing looks identical to
one that runs ten actions. The framework is a dependency the project
installs and upgrades.

## Frameworkless (`frameworkless`)

**For.** Nothing to install or upgrade; one static entry point per
object; the handler is callable in a test without DML. The whole
dispatch fits in twenty lines a newcomer reads in one sitting.

**Against.** Bypass and recursion control are the project's to write,
and each project writes them differently. Nothing recognises the shape
from outside, so the framework must be declared to be resolved.

## Something else

A recognition label — fflib, TDTM, a dispatcher — or a framework this
plugin has never seen: the framework is sound and only the document is
missing. Offer to write a project document describing the project's own
code, answering the four questions the `salesforce-triggers` skill
asks, and declare it with a `doc-path:` locator. Never compare it to
the three above — this plugin cannot write that comparison, and a
document written from a pattern found on the internet describes
somebody else's framework.
````

- [ ] **Step 2: Check the file's shape and the declaration-key invariant**

```bash
f=plugins/salesforce-standards/skills/salesforce-triggers/reference/choosing-a-framework.md
grep -c '^## ' "$f"
grep -c '^\*\*For\.\*\*\|^\*\*Against\.\*\*' "$f"
grep -c '^trigger-framework:\|^vendor-paths:' "$f"
```

Expected: `4`, `6`, `0`. The third is the invariant: the key is mentioned once, in backticks mid-sentence.

- [ ] **Step 3: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
git add plugins/salesforce-standards/skills/salesforce-triggers/reference/choosing-a-framework.md
git commit -m "feat(salesforce-standards): add the framework comparison for step (c)"
```

Expected: validation passes; one commit.

---

### Task 7: Move trigger content out of `salesforce-apex`

**Files:**
- Modify: `plugins/salesforce-standards/skills/salesforce-apex/SKILL.md:3`, `:8-17`, `:21-36`, `:43-60`
- Rename: `plugins/salesforce-standards/skills/salesforce-apex/reference/trigger-handler.md` → `order-layers.md`, then rewrite `:1-15` and delete `:17-62`
- Modify: `plugins/salesforce-standards/skills/salesforce-apex/reference/bulkification.md:5`
- Modify: `plugins/salesforce-standards/skills/salesforce-apex-testing/reference/test-patterns.cls:4`
- Modify: `plugins/salesforce-standards/skills/salesforce-apex-testing/SKILL.md:12` — the layering sentence

**Interfaces:**
- Produces: `reference/order-layers.md`, the file Tasks 1, 3, 4 and 5 already cite; the four remaining example units unchanged in content.

- [ ] **Step 1: Measure before**

```bash
a=plugins/salesforce-standards/skills/salesforce-apex/SKILL.md
grep -c 'TriggerHandler' "$a"
grep -c 'trigger-handler.md' "$a"
tr -s '[:space:]' ' ' < "$a" | grep -o 'one trigger per object' | wc -l
grep -c 'order-layers.md' "$a"
grep -c '(id:' "$a"
test -f plugins/salesforce-standards/skills/salesforce-apex/reference/trigger-handler.md && echo present
rg -l 'trigger-handler\.md' plugins/ | wc -l
grep -c 'salesforce-triggers' plugins/salesforce-standards/skills/salesforce-apex-testing/SKILL.md
```

Expected: `2`, `1`, `1`, `0`, `10`, `present`, `3`, `0`. The tag pattern carries no trailing space, because a sub-rule tag wraps after `(id:`; ten tags is the file's whole census, groups and sub-rules.

- [ ] **Step 2: Edit the description**

Find (line 3):

```
description: Use when writing or reviewing Apex backend code — naming, lightweight layering (one trigger handler per object, service, selector, domain), bulkification, governor limits, sharing keywords, and error handling. Apex unit tests belong to salesforce-apex-testing; access-model design to salesforce-security-model.
```

Replace with:

```
description: Use when writing or reviewing Apex backend code — naming, lightweight layering (service, selector, domain), bulkification, governor limits, sharing keywords, and error handling. Apex triggers and their handlers belong to salesforce-triggers; Apex unit tests to salesforce-apex-testing; access-model design to salesforce-security-model.
```

- [ ] **Step 3: Edit the intro**

Find:

```
Standards for Apex classes and triggers: naming, layering, bulk safety,
governor limits, sharing, and error handling. Cite rules in review
```

Replace with:

```
Standards for Apex classes: naming, layering, bulk safety, governor
limits, sharing, and error handling. Triggers and their handlers — one
trigger per object, the trigger body, the project's trigger framework —
belong to `salesforce-triggers`. Cite rules in review
```

- [ ] **Step 4: Edit the naming table and its tag**

Delete the row:

```
| Trigger handler | `<Object>TriggerHandler` | `AccountTriggerHandler` |
```

Find, in the `apex-naming` tag:

```
`LocalVariableNamingConventions`; the handler/selector/exception
patterns are this standard)
```

Replace with:

```
`LocalVariableNamingConventions`; the selector/exception patterns are
this standard)
```

- [ ] **Step 5: Edit the layers table and the bullets**

Find the two rows:

```
| Trigger | One line: hands the trigger context to its handler | Any conditional or business logic |
| Handler (`<Object>TriggerHandler`) | Routes each trigger event (before insert, after update, …) to domain and service calls | SOQL, DML, business logic itself |
```

Replace with one row:

```
| Trigger and handler | Dispatch: hand the trigger context to the layers below — the shape, one trigger per object and the project's framework are `salesforce-triggers`'s | SOQL, DML, business logic itself |
```

Delete the bullet:

```
- **One handler per trigger; one trigger per object.** The trigger body
  is a single delegating call — no `if`/`for`/field logic in the
  `.trigger` file.
```

Find:

```
- A complete worked example (trigger + handler + domain + selector +
  service for one object) is in
  [reference/trigger-handler.md](reference/trigger-handler.md).
```

Replace with:

```
- The four framework-independent units for one object — domain,
  selector, service, exception — are in
  [reference/order-layers.md](reference/order-layers.md); the trigger
  and handler that call them are in each `salesforce-triggers`
  framework document.
```

The `apex-layering` tag below the bullets is untouched.

- [ ] **Step 6: Rename the reference file and rewrite its head**

```bash
git mv plugins/salesforce-standards/skills/salesforce-apex/reference/trigger-handler.md plugins/salesforce-standards/skills/salesforce-apex/reference/order-layers.md
```

Then replace lines 1–15 (the title through the scenario paragraph) with:

```markdown
# Domain + selector + service — worked example

One object (standard `Order`), four compilation units, one fenced block
each — each block is valid, copy-pasteable Apex for the file named
above it. In a real org each block is its own `.cls` file (a `.cls`
file holds exactly one top-level type). The trigger and the handler
that call these units depend on the project's trigger framework and
live in the `salesforce-triggers` skill's framework documents; each of
them calls the same methods below, so the three examples are one
scenario.

Scenario: when an Order's `Status` field moves to "Activated", create
one fulfillment `Task` per order. The example demonstrates: a domain
class that owns the record-level status-transition rule, a selector
that owns all SOQL for `Order`, and a service that owns the DML
transaction — all bulk-safe, all with an explicit sharing declaration,
errors routed through a custom exception and a logger abstraction
rather than swallowed or left as bare `System.debug` calls.
```

Then delete the two sections `## \`OrderTrigger.trigger\`` and `## \`OrderTriggerHandler.cls\`` in full — from the `## \`OrderTrigger.trigger\`` heading up to, not including, the `## \`OrderDomain.cls\`` heading. The four remaining sections are untouched.

- [ ] **Step 7: Update the two citations**

`bulkification.md:5` — find `[trigger-handler.md](trigger-handler.md).` and replace with `[order-layers.md](order-layers.md).`

`test-patterns.cls:4` — find ` * as salesforce-apex's reference/trigger-handler.md): activating an Order` and replace with ` * as salesforce-apex's reference/order-layers.md): activating an Order`.

`salesforce-apex-testing/SKILL.md:12` — find:

```
decision). Layering (handler/domain/service/selector) is
`salesforce-apex`'s concern, not restated here — a test exercises those
layers, it does not redefine them. LWC jest tests are out of scope —
```

Replace with:

```
decision). Layering (domain/service/selector) is `salesforce-apex`'s
concern and the trigger handler `salesforce-triggers`'s, neither
restated here — a test exercises those layers, it does not redefine
them. LWC jest tests are out of scope —
```

- [ ] **Step 8: Measure after**

```bash
a=plugins/salesforce-standards/skills/salesforce-apex/SKILL.md
o=plugins/salesforce-standards/skills/salesforce-apex/reference/order-layers.md
grep -c 'TriggerHandler' "$a"
grep -c 'trigger-handler.md' "$a"
tr -s '[:space:]' ' ' < "$a" | grep -o 'one trigger per object' | wc -l
grep -c 'order-layers.md' "$a"
grep -c '(id:' "$a"
test -f plugins/salesforce-standards/skills/salesforce-apex/reference/trigger-handler.md && echo present
rg -l 'trigger-handler\.md' plugins/ | wc -l
grep -c '^## ' "$o"
grep -c 'Trigger\.' "$o"
grep -c '^```apex' "$o"
grep -c 'OrderProcessingException extends Exception' "$o"
grep -c 'salesforce-triggers' plugins/salesforce-standards/skills/salesforce-apex-testing/SKILL.md
```

Expected: `0`, `0`, `2`, `1`, `10`, no `present` line, `0`, `4`, `0`, `4`, `1`, `1`. The third rises from `1` to `2`: the deleted bullet carried the phrase once, and the intro's pointer sentence and the new layers row each carry it once — both pointing at `salesforce-triggers`, where the rule now lives. The `(id: ` count is an invariant — no rule leaves or arrives; `apex-naming` and `apex-layering` keep their ids. Before this task `order-layers.md` did not exist, so its four values have no before-state; the old file measured `6` headings, `8` `Trigger.` references and `6` Apex fences, and the drop to `4`, `0`, `4` is the two sections leaving.

- [ ] **Step 9: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
git add -A plugins/salesforce-standards/skills/salesforce-apex plugins/salesforce-standards/skills/salesforce-apex-testing/reference/test-patterns.cls plugins/salesforce-standards/skills/salesforce-apex-testing/SKILL.md
git commit -m "refactor(salesforce-standards): move trigger content out of salesforce-apex"
```

Expected: validation passes; one commit carrying a rename and four modified files.

---

### Task 8: Resolve before grading — the review skill and the command

**Files:**
- Modify: `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md:51-55` — Procedure step 2 gains a paragraph
- Modify: `plugins/salesforce-standards/commands/salesforce-review.md:9-37` — a new step 2, later steps renumbered

**Interfaces:**
- Consumes: the step letters, the record shape and the Summary/`## Project` slots from Task 2.

The review skill's step is added inside step 2 rather than as a new numbered step: the agent card says "per the skill's step 5", the skill's fallback says "exactly as in step 5", and the spec keeps the card unchanged. Renumbering would break the card's citation or force an edit the spec rules out.

- [ ] **Step 1: Measure before**

```bash
s=plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md
c=plugins/salesforce-standards/commands/salesforce-review.md
grep -c 'salesforce-triggers' "$s"
grep -c '^[0-9]\. ' "$s"
grep -c 'salesforce-triggers' "$c"
grep -c '^[0-9]\. ' "$c"
grep -c 'from step 2' "$c"
grep -c 'step 5' plugins/salesforce-standards/agents/salesforce-code-reviewer.md
```

Expected: `0`, `6`, `0`, `5`, `1`, `1`.

- [ ] **Step 2: Extend the review skill's step 2**

Find:

```
2. Load the standards skills relevant to the content under review:
   salesforce-apex for any Apex; salesforce-apex-testing,
   salesforce-lwc, salesforce-flow, salesforce-data-model,
   salesforce-security-model, salesforce-aura, salesforce-visualforce
   as the content demands.
```

Replace with:

```
2. Load the standards skills relevant to the content under review:
   salesforce-apex for any Apex; salesforce-apex-testing,
   salesforce-lwc, salesforce-flow, salesforce-data-model,
   salesforce-security-model, salesforce-aura, salesforce-visualforce
   as the content demands.
   Any Apex file in the run — a `.trigger` or a `.cls` alike — also
   loads `salesforce-triggers` and runs its resolution protocol before
   grading: steps (0) through (b), then step (d) for each resolved
   framework, loading that framework's document by path or name and
   selecting its handlers from the grading universe by the document's
   signature. Resolution runs per file, so a monorepo running two
   frameworks loads two documents and grades every class under the
   framework resolved for its own path. Step (c) is never taken here —
   a background agent asks nothing — and neither is the offer to write
   a declaration. A resolution record carried in the dispatch prompt is
   verified against the declarations on disk; on a mismatch the files
   are the authority. When resolution fails, grade the
   framework-independent rules, skip framework rules rather than guess
   them, note `trigger framework: unresolved — framework-specific rules
   not graded` among the Summary's out-of-scope notes, and report
   `trigger-framework-declared` (nothing declares the path) or
   `trigger-framework-declared.ambiguous` (two the protocol cannot rank)
   in `## Project`. Where resolution succeeds and the document supplies
   no signature, the same note names `trigger-context-below-handler`
   beside the framework rules. The skill's failure table names the
   other Summary notes: unreadable `extends` parents in aggregate, the
   two `vendor-paths:` notes, an unreadable discriminator.
```

- [ ] **Step 3: Add the command's resolution step**

Find the line beginning `2. Pre-dispatch first-create check` and insert before it:

```
2. Resolve the trigger framework when the scope holds any Apex file:
   load `salesforce-triggers` and run its protocol, steps (0) through
   (c) — this is the one review surface where step (c) may ask the
   developer. Write the resolution record, one per resolved framework
   with the paths it covers, and carry it in the dispatch prompt beside
   the directory-mode decision; the agent verifies it against the
   declarations on disk. Where step (c) resolved the framework, offer
   to write the declaration before dispatching.
```

Then renumber: the former step 2 becomes `3.`, 3 becomes `4.`, 4 becomes `5.`, 5 becomes `6.`; and in the new step 4 (the dispatch step) change `the directory-mode decision from step 2` to `the directory-mode decision from step 3`.

- [ ] **Step 4: Measure after**

```bash
s=plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md
c=plugins/salesforce-standards/commands/salesforce-review.md
grep -c 'salesforce-triggers' "$s"
grep -c '^[0-9]\. ' "$s"
grep -c 'salesforce-triggers' "$c"
grep -c '^[0-9]\. ' "$c"
grep -c 'from step 2' "$c"
grep -c 'from step 3' "$c"
grep -c 'step 5' plugins/salesforce-standards/agents/salesforce-code-reviewer.md
tr -s '[:space:]' ' ' < "$s" | grep -o 'trigger framework: unresolved' | wc -l
```

Expected: `1`, `6`, `1`, `6`, `0`, `1`, `1`, `1`. The skill's numbered-step count is an invariant at `6` — the addition sits inside step 2 — and the agent card's `step 5` is an invariant at `1`, which is the reason for that placement.

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
git add plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md plugins/salesforce-standards/commands/salesforce-review.md
git commit -m "feat(salesforce-standards): resolve the trigger framework before grading Apex"
```

Expected: validation passes; one commit.

---

### Task 9: The toolchain rule routes to the skill and documents the keys

**Files:**
- Modify: `plugins/salesforce-standards/rules/salesforce-toolchain.md:38-45`

**Interfaces:**
- Consumes: the two keys and the homes from Task 2.

The installed copy of this rule is not a declaration home — the Rules engine owns it — so the paragraph documents the keys without carrying them: every mention sits in backticks mid-sentence, and no line starts with either key.

- [ ] **Step 1: Measure before**

```bash
r=plugins/salesforce-standards/rules/salesforce-toolchain.md
grep -c 'salesforce-triggers' "$r"
grep -c '^trigger-framework:\|^vendor-paths:' "$r"
grep -c '^---$' "$r"
```

Expected: `0`, `0`, `2`. The last two are invariants: no key at line start, and the frontmatter block intact.

- [ ] **Step 2: Edit the routing paragraph and add the declaration paragraph**

Find:

```
When the salesforce-standards plugin's skills are available, load the
matching one before working: `salesforce-apex` (backend code),
`salesforce-apex-testing` (Apex tests), `salesforce-lwc` (Lightning
```

Replace with:

```
When the salesforce-standards plugin's skills are available, load the
matching one before working: `salesforce-apex` (backend code),
`salesforce-triggers` (Apex triggers and their handlers),
`salesforce-apex-testing` (Apex tests), `salesforce-lwc` (Lightning
```

Then append after the paragraph's last line (`available, the toolchain facts above still bind.`), separated by one blank line:

```
The project's trigger framework and its vendor code are declared in
the project, never in this rule: a line carrying the `trigger-framework:`
key and one carrying the `vendor-paths:` key, in the body of the root
`CLAUDE.md`, of a trigger directory's `CLAUDE.md`, or of a project rule
outside this payload — one framework per path, vendor prefixes at the
root. When the `salesforce-triggers` skill is available it reads both
keys and says how they rank; when it is not, the lines still record the
choice for the reader.
```

- [ ] **Step 3: Measure after**

```bash
r=plugins/salesforce-standards/rules/salesforce-toolchain.md
grep -c 'salesforce-triggers' "$r"
grep -c '^trigger-framework:\|^vendor-paths:' "$r"
grep -c '^---$' "$r"
grep -c 'trigger-framework:' "$r"
```

Expected: `2`, `0`, `2`, `1`. The key appears once, mid-line.

- [ ] **Step 4: Review the frontmatter by hand**

`claude plugin validate` does not check `rules/`. Open the file and confirm the `paths:` block is unchanged and the closing `---` still sits on line 23.

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
git add plugins/salesforce-standards/rules/salesforce-toolchain.md
git commit -m "feat(salesforce-standards): route triggers and document the declaration keys in the toolchain rule"
```

Expected: validation passes; one commit.

---

### Task 10: The identity surfaces

**Files:**
- Modify: `plugins/salesforce-standards/README.md:11-25`, `:45-65`
- Modify: `plugins/salesforce-standards/.claude-plugin/plugin.json` — `description` only
- Modify: `.claude-plugin/marketplace.json` — the `salesforce-standards` entry's `description`
- Modify: `README.md:21` — the `salesforce-standards` row

The marketplace-sync rule binds all four in one commit whenever a plugin's description changes. The version string is untouched.

- [ ] **Step 1: Measure before**

```bash
grep -c 'eight area skills' plugins/salesforce-standards/.claude-plugin/plugin.json
grep -c 'salesforce-triggers' plugins/salesforce-standards/README.md
sed -n '/^## Standards skills/,/^## Review/p' plugins/salesforce-standards/README.md | grep -c '^| `'
grep -c 'Apex triggers' .claude-plugin/marketplace.json README.md
grep '"version"' plugins/salesforce-standards/.claude-plugin/plugin.json
```

Expected: `1`, `0`, `8`, `.claude-plugin/marketplace.json:0` and `README.md:0`, `"version": "0.3.1",`.

- [ ] **Step 2: Edit `plugin.json`**

Find `eight area skills (Apex, Apex testing, LWC, Flow, data model, security model, maintenance-first Aura and Visualforce)` and replace with `nine area skills (Apex, Apex triggers, Apex testing, LWC, Flow, data model, security model, maintenance-first Aura and Visualforce)`.

- [ ] **Step 3: Edit the plugin README**

Find the row:

```
| `salesforce-apex` | naming, lightweight layers (trigger handler, service, selector, domain), bulkification, governor limits, sharing keywords, error handling |
```

Replace with two rows:

```
| `salesforce-apex` | naming, lightweight layers (service, selector, domain), bulkification, governor limits, sharing keywords, error handling |
| `salesforce-triggers` | one trigger per object, the trigger body, resolving the project's trigger framework — base-class, metadata-driven, frameworkless, or one the project documents itself — and loading its guidance |
```

Then insert a section before `## Review stack`:

```markdown
## Declaring the trigger framework

A project declares which trigger framework governs its triggers with a
`trigger-framework:` line in the body of its root `CLAUDE.md` or of the
trigger directory's, and lists code it did not write with a
`vendor-paths:` line at the root — directory prefixes, never globs. The
`salesforce-triggers` skill reads both, ranks nested declarations,
infers from code when nothing declares, and asks only from an
interactive session. A framework this plugin does not ship is declared
with a `doc-path:` or `skill:` locator pointing at the project's own
document.
```

- [ ] **Step 4: Edit the catalog and the repo README**

`.claude-plugin/marketplace.json` — find `area skills for Apex, LWC, Flow, data and security model plus maintenance-first legacy UI` and replace with `area skills for Apex, Apex triggers, LWC, Flow, data and security model plus maintenance-first legacy UI`.

`README.md:21` — find `area skills (Apex, LWC, Flow, data/security model, legacy UI)` and replace with `area skills (Apex, Apex triggers, LWC, Flow, data/security model, legacy UI)`.

- [ ] **Step 5: Measure after**

```bash
grep -c 'eight area skills' plugins/salesforce-standards/.claude-plugin/plugin.json
grep -c 'nine area skills' plugins/salesforce-standards/.claude-plugin/plugin.json
grep -c 'salesforce-triggers' plugins/salesforce-standards/README.md
sed -n '/^## Standards skills/,/^## Review/p' plugins/salesforce-standards/README.md | grep -c '^| `'
grep -c 'Apex triggers' .claude-plugin/marketplace.json README.md
grep -c '^trigger-framework:\|^vendor-paths:' plugins/salesforce-standards/README.md
grep '"version"' plugins/salesforce-standards/.claude-plugin/plugin.json
```

Expected: `0`, `1`, `2`, `9`, `.claude-plugin/marketplace.json:1` and `README.md:1`, `0`, `"version": "0.3.1",`. The `salesforce-triggers` count is two: the table row and the new section each name it once. The declaration-key count at line start is the plugin-wide invariant at `0`; the version line is an invariant too.

- [ ] **Step 6: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
git add plugins/salesforce-standards/README.md plugins/salesforce-standards/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md
git commit -m "docs(salesforce-standards): list the salesforce-triggers skill on the identity surfaces"
```

Expected: validation passes; one commit touching four files.

---

### Task 11: End-state sweep

**Files:** none modified unless a check fails; a failure is fixed in the task that owns the text, and this task re-runs.

Every check here reports an end state, so none has a before-value; the exemption is claimed on each.

- [ ] **Step 1: Structural validation**

```bash
claude plugin validate . && claude plugin validate plugins/salesforce-standards
```

Expected: both pass.

- [ ] **Step 2: No declaration key at line start outside a fence, anywhere in the plugin**

```bash
for f in $(rg -l 'trigger-framework:|vendor-paths:' plugins/salesforce-standards); do
  printf '%s %s\n' "$f" "$(awk '/^```/{f=!f;next} !f' "$f" | grep -c '^trigger-framework:\|^vendor-paths:')"
done
```

Expected: five lines, every one ending in ` 0`. Files listed: the hub `SKILL.md`, `choosing-a-framework.md`, the toolchain rule, the plugin README, and the code-review skill (which names `vendor-paths:` in its Summary-notes sentence). The command and the three framework documents name neither key and do not appear.

- [ ] **Step 3: Rule-tag census across the new skill**

```bash
d=plugins/salesforce-standards/skills/salesforce-triggers
grep -c '(id:' "$d/SKILL.md" "$d"/reference/*.md
grep -rc 'severity: critical' "$d"
grep -rn 'severity: critical' "$d" | grep -c 'kind: defect'
grep -rn 'severity: critical' "$d" | grep -vc 'kind: defect'
grep -rho 'severity: [a-z]*' "$d" | sort | uniq -c
```

Expected: `SKILL.md:7`, `choosing-a-framework.md:0`, `framework-base-class.md:3`, `framework-frameworkless.md:3`, `framework-metadata-driven.md:4`; one file with `1` critical and the rest `0`; `1`; `0`; and the tally `1 severity: critical`, `10 severity: important`, `6 severity: minor` — re-derived: important are `.disjoint-contexts`, `trigger-body-delegates`, `trigger-context-below-handler`, `.ambiguous`, two frameworkless, two base-class, two metadata-driven = 10; minor are `trigger-naming`, `trigger-framework-declared`, three dispatching-class rules, `order-explicit` = 6. The hub's prose sentence "`setMaxLoopCount(1)` guards …" and Task 1's sub-rule boundary prose carry no `severity:` word, so the tally counts tags alone.

- [ ] **Step 4: Sub-rule severities differ from their group default**

```bash
f=plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md
grep -n 'trigger-one-per-object`; severity\|disjoint-contexts`; severity\|trigger-framework-declared`; severity\|ambiguous`; severity' "$f"
```

Expected: four lines — `critical`, `important`, `minor`, `important`, in that order. Each sub-rule differs from its group.

- [ ] **Step 5: The renamed file has no survivors and every framework document cites it**

```bash
rg -l 'trigger-handler\.md' plugins/
rg -l 'order-layers\.md' plugins/salesforce-standards | sort
```

Expected: the first prints nothing. The second lists exactly: `plugins/salesforce-standards/skills/salesforce-apex-testing/reference/test-patterns.cls`, `plugins/salesforce-standards/skills/salesforce-apex/SKILL.md`, `plugins/salesforce-standards/skills/salesforce-apex/reference/bulkification.md`, `plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md`, `plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-base-class.md`, `plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-frameworkless.md`, `plugins/salesforce-standards/skills/salesforce-triggers/reference/framework-metadata-driven.md` — seven files.

- [ ] **Step 6: Disjoint descriptions**

```bash
grep -h '^description:' plugins/salesforce-standards/skills/salesforce-apex/SKILL.md plugins/salesforce-standards/skills/salesforce-triggers/SKILL.md | grep -c 'trigger handler'
grep -h '^description:' plugins/salesforce-standards/skills/*/SKILL.md | grep -c '^description: .*: '
```

Expected: `0` — neither description says "trigger handler", the phrase that made them compete; `0` — no description carries a second colon-space after the key's own. The second value was `0` before Task 1 as well and is an invariant.

- [ ] **Step 7: The four lower-layer methods are the only ones a handler calls**

```bash
grep -rho 'Order\(Domain\|Service\)\.[a-zA-Z]*' plugins/salesforce-standards/skills/salesforce-triggers/reference/ | sort | uniq -c
```

Expected: exactly four names — `OrderDomain.applyDefaults`, `OrderDomain.filterNewlyActivated`, `OrderDomain.validateStatusTransitions`, `OrderService.activateFulfillment` — each with count `3`, one per framework document. Every one is defined in `order-layers.md`:

```bash
grep -c 'public static void applyDefaults\|public static void validateStatusTransitions\|public static List<Order> filterNewlyActivated\|public static void activateFulfillment' plugins/salesforce-standards/skills/salesforce-apex/reference/order-layers.md
```

Expected: `4`.

- [ ] **Step 8: Hygiene and version**

```bash
rg -n '/home/' plugins/salesforce-standards .claude-plugin/marketplace.json README.md
grep '"version"' plugins/salesforce-standards/.claude-plugin/plugin.json
git log --format=%s develop..HEAD -- plugins/salesforce-standards .claude-plugin README.md | grep -c '(salesforce-standards)'
git log --format=%B develop..HEAD | grep -c 'Co-Authored-By'
```

Expected: the first prints nothing; `"version": "0.3.1",`; `10`, or more where a failed check sent a fix back through an owning task — the path filter keeps the document branch's `docs/` commits out of the count, and a commit under `## Developer rulings` touches no path listed; `0`.

- [ ] **Step 8a: The hub's document table names files that exist**

```bash
d=plugins/salesforce-standards/skills/salesforce-triggers
for p in $(grep -o 'reference/framework-[a-z-]*\.md' "$d/SKILL.md" | sort -u); do test -f "$d/$p" && echo "$p"; done
```

Expected: three lines — `reference/framework-base-class.md`, `reference/framework-frameworkless.md`, `reference/framework-metadata-driven.md`. An end-state check, so no before-value.

- [ ] **Step 9: Report**

State the end state to the developer: ten commits on `feature/trigger-frameworks`, every check above at its expected value, the spec notes this plan surfaced (Deviations 1, 2, 4 and 5) for the spec's ledger, and one item for the release PR's notes — a project on the frameworkless shape this plugin shipped before now earns `trigger-body-delegates` and `trigger-frameworkless-entry-point` per trigger until it adds the `handle` entry point (the Gotcha in `framework-frameworkless.md` names the fix). Do not move the plan's `status`; the developer flips it.

## Developer rulings

None yet. Rulings taken during execution are recorded here, one line each, dated.

## Review rounds

### 2026-09-08 — plan-adversary, fable 5.1, concerns (round 2, diff-scoped)

- fixed 2026-09-08 — [Important] The round-one fix named one instance of the class it repaired while the framework ships a second top-level class matching `header: TriggerAction.` — `TriggerActionFlow`, implementing all seven context interfaces at `TriggerActionFlow.cls:24` (the report cited `:23`), with a `Trigger_Action__mdt` record only where a Flow action is registered — so `action-registered` still fired on the framework vendored as source; license: Deviation 4's own reason, which the finding shows was incomplete rather than wrong; `TriggerActionFlow` joins `Framework types:`, Task 5 and Deviation 4 name the class of instance and both instances, and `TriggerActionFlowChangeEvent extends TriggerActionFlow` is named as a closure candidate that stays out
- fixed 2026-09-08 — [Minor] The handler-set definition still stated the pre-fix rule — "a handler on that match alone", unqualified — so the ordering lived only in the bullet above it (the report cited line 280; the bullet ends there); license: the round-one fix's own sentence; the definition now subtracts the `Framework types:` names in the fixed point and qualifies the match-alone sentence
- fixed 2026-09-08 — [Minor] `trigger-frameworkless-entry-point` said "the trigger's single call", colliding with the hub's `trigger-one-per-object` prose that several handler calls in one file are correct; license: that prose; the rule now grades every call's shape, not their number
- fixed 2026-09-08 — [Minor] The migration Gotcha and Task 11 Step 9 named one finding where the rewritten `entry-point` rule fires a second on the same trigger — two fixes from one wave describing one trigger, unreconciled; license: the rule's own text; both now name both ids and say one fix clears all three signals
- fixed 2026-09-08 — [Minor] The File-structure section kept `salesforce-apex-testing/SKILL.md` under "Unchanged on purpose" with a clause reading as a post-edit state opposite to what Task 7 writes; license: Task 7 Step 7; the file is in the Modified list with its line, and the clause is gone
- signal 2026-09-08 — another diff-scoped round does not repay its cost: the Important is a one-token list edit plus two sentences and its class is now bounded by the framework's class listing rather than by memory, and the four Minors are wording; the leftovers are worth one fix wave, then the confirming full-document round the rules mandate, where a re-introduced contradiction between the grammar bullet and the handler-set definition would surface. Not an all-Minor round

### 2026-09-08 — plan-adversary, fable 5.1, blocking (round 1, full-document)

- fixed 2026-09-08 — [Important] Task 4's test-isolation block calls `TestDataFactory.createOrders(200)`, which the plugin's own factory does not define; license: `salesforce-apex-testing/reference/TestDataFactory.cls:53` (`createOrders(Integer count, Id accountId)`) and the Global Constraint that every Apex block is copy-pasteable; the block now creates the account first and calls `createOrders(200, acc.Id)`
- fixed 2026-09-08 — [Important] `header: TriggerAction.` selects `MetadataTriggerHandler` itself and every `DmlFinalizer` implementer, and the hub orders nothing between "a handler on that match alone" and the `Framework types:` exemption, so `trigger-metadata-driven-action-registered` fires on the framework class wherever it is vendored as source; license: the spec's sentence that framework types are "graded by no framework rule"; the hub grammar now says a `Framework types:` entry leaves the handler set even where it matches, Task 5 names `MetadataTriggerHandler` as the instance, and `action-registered` is scoped to the seven context interfaces with `DmlFinalizer` implementers left alone. Recorded as Deviation 4, since the spec never orders the two sentences
- fixed 2026-09-08 — [Important] The hub restates a grade outside a tag, "as a minor rule", which no other surface may do; license: `.claude/rules/standards-rule-tags.md:24`; the hub now reads "as a rule of its own", and Deviation 5 records that the spec's phrase does not travel into shipped text
- fixed 2026-09-08 — [Minor] `trigger-frameworkless-entry-point` could never fire on a class, since a class without the entry point matches no signature; license: the rule's own text, which said so; the rule is now graded on the trigger — its single call is the `handle` entry point, and a per-context call leaves the handler unselectable
- fixed 2026-09-08 — [Minor] A consumer who followed 0.3.1's frameworkless shape earns `trigger-body-delegates` per trigger and matches no signature, and nothing told them; license: the spec's stance that pre-existing code is left alone where a rule says so, and the plan's own migration silence; `framework-frameworkless.md` gains a Gotcha naming the old shape and its mechanical fix, and Task 11 Step 9 flags it for the release notes
- fixed 2026-09-08 — [Minor] `salesforce-apex-testing/SKILL.md:12` still routes the handler layer to `salesforce-apex` while the plan declared the file unchanged; license: the spec's parts table, which gives the handler to `salesforce-triggers`; Task 7 now edits the sentence, adds the file to its commit, and the File-structure note says so
- fixed 2026-09-08 — [Minor] Task 11 Step 8 counted the ten most recent subjects, which a rulings commit or a re-run fix would make wrong in either direction; license: the plan's own Developer-rulings section and Task 11's re-run clause, which the check contradicted; the count is now path-filtered over `develop..HEAD` and expects ten or more
- fixed 2026-09-08 — [Minor] No check confirmed that the three document paths the hub table names exist on disk; license: Task 11's stated job as the end-state sweep; Step 8a now tests each path the table names
- signal 2026-09-08 — another round earns its cost only diff-scoped over the fixes to the second and third Important findings, the hub grammar change being the class that breeds repair-born defects; the five Minor leftovers are worth one fix wave, and the before-values and the API facts of Tasks 4 and 5 need no re-read
