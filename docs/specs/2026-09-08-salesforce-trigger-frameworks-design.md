---
date: 2026-09-08
status: draft
branch: feature/trigger-frameworks
base: develop
---

# salesforce-standards — trigger frameworks across projects

## Overview

`salesforce-standards` teaches one way to write an Apex trigger. Projects
use several, and the choice is mutually exclusive: a project on a
base-class framework cannot follow guidance written for a metadata-driven
one. This spec adds a `salesforce-triggers` skill that owns what holds
whatever framework a project uses, resolves which framework governs the
file at hand, and loads the matching guidance from a per-framework
document.

The design keeps the class of frameworks open. A project may use one this
plugin never ships — a homegrown dispatcher, fflib, TDTM, a fork — and
reaches the same guidance by naming its own document or skill in the
declaration.

## The problem

`salesforce-apex/SKILL.md` teaches a handler of static methods, dispatched
by conditional logic in the trigger body. Three approaches are in current
use across the projects this plugin serves:

1. **Base-class** — a `virtual TriggerHandler` class copied into the org.
   The trigger body reads `new OrderTriggerHandler().run();` and the
   handler overrides context methods.
2. **Metadata-driven** — execution order and bypasses live in Custom
   Metadata, so ordering changes without a code deployment.
3. **Frameworkless** — today's content.

Serving one approach and calling it the standard would leave two projects
in three following guidance that contradicts their code.

The skill also carries a defect this work fixes. `SKILL.md` requires a
trigger body of "a single delegating call — no `if`/`for`/field logic in
the `.trigger` file", while `reference/trigger-handler.md` shows a trigger
body branching on `Trigger.isBefore` and `Trigger.isInsert`.

## Settled decisions

The developer settled these; the spec records them rather than reopening
them.

- **All three approaches are served.** This is not an exercise in picking
  a winner.
- **The class of frameworks is open.** A fourth is expected. Its guidance
  may live in this plugin, in a document or skill inside the project, or
  in another plugin.
- **Resolution reads a declaration first**, infers from code second, and
  asks the developer third, presenting the case for and against each
  option.
- **The declaration lives in the project**, keyed so a grep finds it.
- **Per-framework guidance ships as `reference/` documents**, not as
  separate skills.
- **Resolution is per trigger file.** The search walks up from the file to
  the nearest declaration.
- **The migration case is deferred.** The first release serves one
  framework per path plus vendor exclusions.
- **No enforcement hook.** The protocol is advisory.

## Parts and boundaries

| Part | Owns | Deliberately excludes |
|---|---|---|
| `salesforce-triggers` (new skill) | framework-agnostic rules; the resolution protocol; the `framework-id` → path table; the questions a framework document answers; fingerprints; the vendor-exclusion scope; `reference/choosing-a-framework.md` | trigger or handler code; bypass API names; the name of the dispatching class |
| `reference/framework-base-class.md`, `-metadata.md`, `-none.md` | dispatch shape; where the handler reads context; bypass and recursion API with its error semantics; test-isolation idiom; gotchas; framework-specific rules; two example units | layers below the handler; bulkification; test-class structure |
| `salesforce-apex` | naming, layers, bulkification, governor limits, sharing, error handling; the four framework-independent example units | the trigger section, reduced to a layer-table row pointing at the hub |
| `salesforce-apex-testing` | test structure, factory, assertions, mocks | how to disable a handler in a test |
| `salesforce-code-review`, `salesforce-code-reviewer` | a resolution step before grading `.trigger` and `*TriggerHandler*.cls` | asking the developer — a background agent cannot |
| `/salesforce-review` | resolution before dispatch, passed in the prompt | — |
| `rules/salesforce-toolchain.md` | a routing line for the hub; the documented declaration key | the declaration itself, which belongs to the project |

The hub must reach a session on its own `description:`, because
`salesforce-standards` declares no dependencies and installs without
`working-process`, whose `sync-rules` skill is the only carrier for the
rules payload. The toolchain rule strengthens routing; it never gates it.
For the same reason `CLAUDE.md` is the declaration's primary home: it
needs no plugin.

### Descriptions stay disjoint

`salesforce-apex` currently advertises "lightweight layering (one trigger
handler per object, service, selector, domain)", which would compete with
the hub for a question about triggers. Its description drops the trigger
clause. The hub's description reads:

> Use when writing or reviewing Apex triggers — one trigger per object,
> what belongs in the trigger body, resolving which trigger framework the
> project uses, and loading the matching framework guidance. Apex classes,
> layering and bulkification belong to salesforce-apex; Apex tests to
> salesforce-apex-testing.

This honours the constraint the plugin set itself in
`2026-07-20-salesforce-standards-design.md`: "Descriptions written
disjointly (no two skills compete for the same trigger)."

## Hub rules

Rule ids carry the `trigger-` prefix; framework documents use
`trigger-base-class-`, `trigger-metadata-` and `trigger-none-`. A finding
citation names the skill, so ids never collide across framework documents.

**One trigger per object.** An object has one `.trigger` file. Several
handler calls inside that file are correct, in the order they must run;
the violation is a second trigger file, never a second line. Scope: the
directories listed in `packageDirectories`, excluding triggers on objects
a vendor package owns.

(id: `trigger-one-per-object`; severity: critical; kind: defect; source:
Salesforce Well-Architected, record-triggered decision guide; Apex
Developer Guide p. 282)

Sub-rules:

- the two triggers declare disjoint contexts (id:
  `trigger-one-per-object.disjoint-contexts`; severity: important)

The group default grades the dangerous case. Two triggers whose declared
contexts overlap fire in an order the platform leaves undefined, so the
same code yields different results between runs — irregular data
corruption, which the rubric grades critical. Disjoint contexts carry no
ordering risk today, yet they split an object's automation across files
and sit one context declaration away from the critical case.

**The trigger body delegates.** The body contains delegating calls and
nothing else — no conditional, loop or field logic.

(id: `trigger-body-delegates`; severity: important; source: Apex Developer
Guide, "Document Your Apex Code")

**Context stops at the handler.** Nothing below the handler reads
`Trigger.*`; context descends as parameters, which keeps the logic
testable without DML.

(id: `trigger-context-below-handler`; severity: important; source: this
standard)

The earlier formulation, "read `Trigger.*` only in the handler", is false
for a base-class framework, where the base class reads it, and for a
handler dispatched on `Trigger.operationType`, where the trigger reads it.

**Naming.** A trigger is named `<Object>Trigger`. Pre-existing
non-conforming names stay; the convention binds new code. The dispatching
class is named by the framework document, not here.

(id: `trigger-naming`; severity: minor; source: this standard)

**The framework is declared.** The project declares its trigger framework.
The finding lands in the report's `## Project` section, and lands there
even when inference succeeded, because inference resolves a session while
a declaration resolves the project.

(id: `trigger-framework-declared`; severity: minor; source: this standard)

Bulkification stays with `salesforce-apex`. The hub cites
`apex-bulkification` and `apex-bulkification.loop-on-trigger-path` and
carries no severity word of its own.

## What a framework document answers

Four questions, and a fifth for the documents this plugin ships. A missing
answer is stated to the developer, never filled from another framework.

1. **Dispatch** — the trigger body and the handler shape, as two files
   calling the same lower-layer methods the shipped example uses.
2. **Context access** — where the handler reads `Trigger.*`.
3. **Bypass and recursion** — the API names *and* what happens when a
   limit is exceeded.
4. **Test isolation** — how to call the handler without DML, and how to
   disable it in a test.
5. **Fingerprint** — what identifies this framework in code. Required for
   the documents shipped here, since step (b) of the protocol depends on
   it.

Question 3 earns its place: `setMaxLoopCount(1)` is a correct guard under
one base-class framework and silences automation under another. Names
alone cannot tell a reviewer which.

Framework-specific rules are optional. A document that carries none is
graded by hub rules alone, and the report says so. The tag grammar does
not become a public contract in this release, so a document from outside
this plugin is not graded on its framework rules at all.

## Resolution protocol

### The declaration

One line, one key:

```
trigger-framework: base-class
trigger-framework: trigger-actions
trigger-framework: frameworkless
trigger-framework: acme-dispatcher; doc-path: docs/acme-triggers.md
trigger-framework: acme-dispatcher; skill: acme-plugin:acme-triggers
```

Homes: the repository's `CLAUDE.md`, a directory's `CLAUDE.md`, a local
copy of `salesforce-toolchain.md`, or a project rule. A grep does not
distinguish them, so the design does not either.

### Steps

Resolution runs per trigger file, walking up from the file to the nearest
declaration.

| Step | Action |
|---|---|
| (a) | grep the candidate files for `trigger-framework:` — an explicit read, never a wait for context |
| (b) | fingerprint the project's own code, skipping vendor directories |
| (c) | ask the developer, with `reference/choosing-a-framework.md` |

Step (a) reads rather than waits because a `CLAUDE.md` in a subdirectory
loads lazily: Claude Code "discovers `CLAUDE.md` [...] in subdirectories
under your current working directory. Instead of loading them at launch,
they are included when Claude reads files in those subdirectories." A
session about to write its first trigger has read nothing in that
directory, which is exactly when resolution runs.

### Fingerprints

| Framework | Pattern |
|---|---|
| base-class | `extends TriggerHandler` with `new X().run()` |
| metadata-driven | `new MetadataTriggerHandler().run()` with `Trigger_Action__mdt` and `sObject_Trigger_Setting__mdt` records |
| fflib | `fflib_SObjectDomain.triggerHandler(` in the trigger body |
| TDTM | `TDTM_Config_API.run(` |
| dispatcher | `TriggerDispatcher.Run(`, or a handler implementing an interface with `IsDisabled()` |
| frameworkless | no pattern is not a fingerprint — go to step (c) |

The metadata-driven fingerprint keys on Custom Metadata records and the
trigger body, never on the framework's classes: the records sit in the
repository whether the framework arrives as an unlocked package or as
source, while the classes appear only in the second case.

The base-class document must also separate two frameworks that look
identical in the trigger body and differ in error semantics. The
discriminator is the method name inside `TriggerHandler.cls`:
`incrementCheckLoopCount` silences an exceeded loop count,
`addToLoopCount` throws.

### Exclusions

Two layers, not one: directories outside `packageDirectories`, and
triggers on objects a vendor package owns even when its source sits inside
a package directory. A logging package distributed unlocked and without a
namespace puts its classes in the org's own namespace beside the
project's. Reviews already exclude this material —
`salesforce-code-review/SKILL.md` states "never review third-party
libraries" — so the exclusion needs a scope, not a rule.

### The resolution record

One line, before the first trigger edit, carrying three fields — the
framework, the source, and the document loaded:

```
Trigger framework: base-class — declared in force-app/billing/triggers/CLAUDE.md — loading framework-base-class.md
```

The source reads `declared <file>`, `inferred <evidence>` or `asked`. Any
source other than `declared` ends with an offer to write the declaration:
a line in a conversation dies at the next compaction, a declaration
survives it. The hub never remembers a resolution; after compaction it
reads the files again.

### Failure modes

| Situation | Behaviour |
|---|---|
| No declaration, fingerprint matches | infer, cite the file and pattern, offer to write the declaration |
| No declaration, no fingerprint | go to (c), saying no pattern matched in N triggers and asking whether the project is frameworkless or on a framework this plugin does not know |
| No triggers at all | go to (c) |
| Two declarations disagree | the nearer one wins, the disagreement is always stated, and the session offers to reconcile them |
| The declared document is missing | say so and grade by hub rules; never substitute another framework's document, since guidance for the wrong framework writes code that does not compile |
| A homegrown framework with no document | offer to write one, describing their code rather than a pattern from the internet — the "dispatcher, handler, helper" division has no primary source |

## Review surface

`salesforce-code-review` gains a step: for `.trigger` and
`*TriggerHandler*.cls`, load the hub, resolve through (a) and (b), then
load the framework document by path or name.

Step (c) does not exist for a background agent, so `/salesforce-review`
resolves before dispatch and passes the record in the prompt, as it
already passes the directory mode. The agent verifies the record against
the declaration, which costs nothing.

When resolution fails, the run grades hub rules, skips framework rules
rather than guessing them, notes `trigger framework: unresolved —
framework-specific rules not graded` among the Summary's out-of-scope
notes, and reports `trigger-framework-declared` in the `## Project`
section. Both slots already exist in the review-report contract.

## Changes to shipped content

Three rules change owner, and the spec names each because a moved id
breaks a citation:

1. "One trigger per object" leaves `apex-layering` for
   `trigger-one-per-object`.
2. `<Object>TriggerHandler` leaves `apex-naming`. The hub names only
   `<Object>Trigger`.
3. `apex-bulkification` and its sub-rule stay put, cited by the hub.

The frameworkless document adopts a dispatch shape that keeps
`trigger-body-delegates` true:

```apex
trigger OrderTrigger on Order (before insert, before update, after update) {
    OrderTriggerHandler.handle(Trigger.operationType, Trigger.new, Trigger.oldMap);
}
```

The handler switches on `System.TriggerOperation`. This fixes the defect
named above, makes the hub rule true for all three frameworks, and gives
the frameworkless handler what the frameworks already have: a dispatch
entry point callable from a test without DML.

The example splits rather than triples. `OrderDomain`, `OrderSelector`,
`OrderService` and `OrderProcessingException` do not depend on the
framework and stay in `salesforce-apex/reference/`. Each framework
document carries `OrderTrigger` and `OrderTriggerHandler` and calls the
same lower-layer methods, so the three examples are demonstrably one
scenario.

## Evidence and its limits

Framework behaviour was read from source, not from documentation. Two
findings correct the documentation:

- The base-class fork documents `TriggerHandler.setGlobalBypass()`, which
  its source does not define. The method is `bypassAll()`.
- Its silent stop is deliberate. The `throw` sits commented out beside the
  line `// Do not throw an exception if we exceed the loop count - just
  stop executing`.

Two citations carry weaker provenance, recorded so a later reader can
judge them:

- Apex Developer Guide quotations come from the official PDF, fetched with
  TLS verification disabled after the HTML pages returned 403.
- Well-Architected quotations come from two consistent extractions of the
  same page rather than a byte-exact fetch.

One provenance note matters for the rule that carries the most weight. The
phrase "one trigger per object" appears nowhere in the 825-page Apex
Developer Guide. The Guide supplies the reasoning — execution order is
undefined for two triggers on one object for the same event — while the
prescription lives in Well-Architected. The formulation everyone quotes
comes from a retired `developer.salesforce.com` wiki page written in 2014
by the author of the original base-class framework. The rule is sound; its
popular pedigree is authored content, not platform norm.

## Deviations from the consultations

Both personas were consulted on one briefing and disagreed about whether
per-framework guidance should ship as skills. The architect held that a
skill buys routing this design does not want and identity cost it pays
forever; the system designer held that skills with
`disable-model-invocation: true` cost no listing and unify loading.
Verification settled it: such a skill's description does stay out of
context, but the hub reads shipped and project-local documents by path in
either shape, so uniformity was not the deciding gain. Slash-command
invocation was, and nobody wanted it.

Two further deviations:

- **Resolution is per file, not per package.** The designer proposed the
  sfdx package as the unit. A package holding several application folders
  would then take one declaration for two answers. Walking up from the
  file generalises the designer's own nearest-wins rule, and the package
  keeps the job it is needed for: bounding vendor exclusions.
- **The fflib argument is dropped.** The architect argued that fflib names
  its handler `<Object>Domain`, colliding with this standard's Domain
  layer. fflib split domain from trigger handler in April 2021 and its
  sample code now separates them. The decision stands on the
  metadata-driven case, where the handler is the framework's own class.

## Out of scope

- **Migration between frameworks.** Deferred, with it the rule that would
  grade a new file against a declared target.
- **The tag grammar as a public contract.** A document from another plugin
  is not graded on framework rules, so the grammar stays internal and
  `plugin-versioning` gains no new breaking surface.
- **Enforcement.** No hook ships. `PreToolUse` could deny a write to a
  `.trigger` file with no declaration in scope, and `InstructionsLoaded`
  could not help at all, having no decision control. The consequence is
  recorded rather than hidden: a session that writes a trigger without
  loading the hub meets no obstacle, and review catches the miss
  afterwards through `trigger-framework-declared`.

## Open questions

- **Ticket.** None. The developer chose to open no issue and to name the
  branch `feature/trigger-frameworks`, without the issue number the
  repository convention prescribes. A ticket may still be opened before
  the pull request.
- **How many consumers run a framework other than frameworkless.**
  Unknown, and no longer load-bearing: the question tested the
  proportionality of shipping four skills, and this design ships one skill
  with three documents.
