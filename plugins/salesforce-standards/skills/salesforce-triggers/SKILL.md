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
declaration away from the case the group default grades.

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
