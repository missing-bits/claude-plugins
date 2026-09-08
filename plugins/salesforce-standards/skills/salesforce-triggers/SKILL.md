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
