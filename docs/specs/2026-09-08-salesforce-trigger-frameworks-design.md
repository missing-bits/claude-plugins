---
ticket: none
date: 2026-09-08
status: draft
grilled: 2026-09-08
architect: LGTM
integrity: 2026-09-08 (sha: 366b99f)
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
- **Resolution is per file.** Every declaration whose scope covers the
  file is collected and ranked. The nearest does not simply win: a rule
  scopes by glob rather than by position, and unrankable declarations have
  no winner at all.
- **The migration case is deferred.** The first release serves one
  framework per path plus vendor exclusions.
- **No enforcement hook.** The protocol is advisory.

## Parts and boundaries

| Part | Owns | Deliberately excludes |
|---|---|---|
| `salesforce-triggers` (new skill) | framework-agnostic rules; the resolution protocol; the `framework-id` → path table; the questions a framework document answers; the fingerprint table, whose shipped rows come from the documents' fifth answer; the vendor-exclusion scope; `reference/choosing-a-framework.md` | trigger or handler code; bypass API names; the name of the dispatching class |
| `reference/framework-base-class.md`, `-metadata-driven.md`, `-frameworkless.md` | dispatch shape; the handler signature and the framework's own types; its fingerprint row; where the handler reads context; bypass and recursion API with its error semantics; test-isolation idiom; gotchas; framework-specific rules; two example units | layers below the handler; bulkification; test-class structure |
| `salesforce-apex` | naming, layers, bulkification, governor limits, sharing, error handling; the four framework-independent example units | the trigger section, reduced to a layer-table row pointing at `salesforce-triggers` |
| `salesforce-apex-testing` | test structure, factory, assertions, mocks | how to disable a handler in a test |
| `salesforce-code-review` | a resolution step before grading Apex, then handler selection by the signature the resolved framework document supplies | asking the developer — a background agent cannot |
| `salesforce-code-reviewer` | nothing — the skill owns the step, so the agent's card is unchanged | — |
| `/salesforce-review` | resolution before dispatch, passed in the prompt | — |
| `rules/salesforce-toolchain.md` | a routing line for `salesforce-triggers`; both documented declaration keys | the declaration itself, which belongs to the project |

`salesforce-triggers` must reach a session on its own `description:`,
because `salesforce-standards` declares no dependencies and supports a
Standalone install, where the Rules engine that carries its payload is
absent. The toolchain rule strengthens routing; it never gates it. For
the same reason `CLAUDE.md` is the declaration's primary home: it needs
no plugin. The review surface survives a Standalone install unchanged,
because the inline fallback in `salesforce-code-review` already defines
both slots this design writes to — a Summary carrying out-of-scope files
and a `## Project` section.

### Descriptions stay disjoint

`salesforce-apex` currently advertises "lightweight layering (one trigger
handler per object, service, selector, domain)", which would compete with
`salesforce-triggers` for a question about triggers. Its description drops
the trigger clause. The new skill's description reads:

> Use when writing or reviewing Apex triggers — one trigger per object,
> what belongs in the trigger body, resolving which trigger framework the
> project uses, and loading the matching framework guidance. Apex classes,
> layering and bulkification belong to salesforce-apex; Apex tests to
> salesforce-apex-testing.

This honours the constraint the plugin set itself in
`2026-07-20-salesforce-standards-design.md`: "Descriptions written
disjointly (no two skills compete for the same trigger)."

## Framework-independent rules

Rule ids carry the `trigger-` prefix; framework documents use
`trigger-base-class-`, `trigger-metadata-driven-` and
`trigger-frameworkless-`. A finding
citation names the skill, so ids never collide across framework documents.

**One trigger per object.** An object has one `.trigger` file. Several
handler calls inside that file are correct, in the order they must run;
the violation is a second trigger file, never a second line. Scope: triggers under the
directories listed in `packageDirectories` and outside `vendor-paths:` —
the same two layers the Exclusions section reads, stated by path rather
than by which package owns an object, since a vendor's trigger on a
standard object belongs to nobody by ownership and to the vendor by path.

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
testable without DML. The types a framework document lists as its own are
exempt: a base class reading `Trigger.*` is the framework doing its job.
This rule alone among the framework-independent ones needs a handler set,
so it goes ungraded wherever no signature supplies one.

(id: `trigger-context-below-handler`; severity: important; source: this
standard)

The earlier formulation, "read `Trigger.*` only in the handler", is false
for a base-class framework, where the base class reads it, and for a
handler dispatched on `Trigger.operationType`, where the trigger reads it.

**Naming.** A trigger is named `<Object>Trigger`. Pre-existing
non-conforming names stay; the convention binds new code. The dispatching
class is named by the framework document, not here — and each shipped
document carries that name as a rule of its own, at minor severity and
with the same stance on pre-existing names, so the convention leaves this
skill without leaving the standard.

(id: `trigger-naming`; severity: minor; source: this standard)

**The framework is declared.** The project declares its trigger framework.
The finding lands in the report's `## Project` section, and lands there
even when inference succeeded, because inference resolves a session while
a declaration resolves the project.

(id: `trigger-framework-declared`; severity: minor; source: this standard)

Sub-rules:

- two declarations cover one path with different values and neither is a
  subtree strictly containing the other, so neither wins (id:
  `trigger-framework-declared.ambiguous`; severity: important)

The group default grades an absent declaration, which announces itself:
resolution falls through to inference or to a question, and the reader
sees it happen. The sub-rule grades every case the protocol cannot
rank — a glob-scoped rule against a subtree-scoped `CLAUDE.md`, two rules
whose `paths:` differ, and `CLAUDE.md` beside `.claude/CLAUDE.md` in one
directory, whose subtrees are equal so neither contains the other.
Declarations that agree never reach the rule: ranking counts distinct
values, and agreement is not a collision. All of these hide: the project
has declared twice, so the letter of the rule is met while nothing can be
resolved from it,
and framework rules quietly go ungraded.

A root default with a nearer override is **not** this finding. Two
subtree-scoped declarations are comparable, the inner one wins, and
declaring a repository-wide default beside a per-package exception is a
configuration the protocol resolves — not a violation it grades. Stating
that disagreement belongs to the resolution record as a duty, never to a
rule as a grade. The two dispositions are therefore mutually exclusive: a
path has no declaration, or it has two the protocol cannot rank.

Bulkification stays with `salesforce-apex`. `salesforce-triggers` cites
`apex-bulkification` and `apex-bulkification.loop-on-trigger-path` and
carries no severity word of its own.

## What a framework document answers

Four questions, and a fifth for the documents this plugin ships. A missing
answer is stated to the developer, never filled from another framework.

1. **Dispatch** — the trigger body and the handler shape, as two files
   calling the same lower-layer methods the shipped example uses, plus the
   **signature** that makes a class one of this framework's handlers and
   the framework's **own types**, which are neither handlers nor layers
   below one.
2. **Context access** — where the handler reads `Trigger.*`.
3. **Bypass and recursion** — the API names *and* what happens when a
   limit is exceeded.
4. **Test isolation** — how to call the handler without DML, and how to
   disable it in a test.
5. **Fingerprint** — what identifies this framework in code, and so the
   row this document contributes to the skill's table. Every shipped
   document answers; the frameworkless answer is that nothing identifies
   it, which is why step (b) falls through to (c) rather than matching.

Question 3 earns its place: `setMaxLoopCount(1)` is a correct guard under
one base-class framework and silences automation under another. Names
alone cannot tell a reviewer which.

For the base-class document, question 3 carries one duty more, because
the two frameworks answer it differently and the discriminator can be
unreadable — it is a method name inside `TriggerHandler.cls`, and a
managed package hides it. That document says what else tells them apart,
a namespace or a version, and what happens when nothing does: the rules
keyed to error semantics go ungraded, the Summary says which and why, and
no reviewer guesses, while the framework's other rules grade normally,
the project's own handlers being readable whatever carries their parent.
An authoring session has no Summary to write in, so it states both
semantics and says the installed package decides which holds — the
difference being whether `setMaxLoopCount(1)` guards or silences.

Question 1 carries a signature rather than a filename pattern, and the
distinction is the whole point. A review run already covers every Apex
class — `salesforce-code-review/SKILL.md` lists "Apex: `*.cls`,
`*.trigger`" — so nothing about handlers is a question of scope. What the
answer decides is which of those classes the framework's rules grade, and
no framework imposes a name on them: a metadata-driven project wires an
action through a free-text metadata field and an interface, and this
standard's own `trigger-naming` rule leaves pre-existing names alone. A
class called `LegacyAccountHandler` that implements
`TriggerAction.BeforeInsert` is a handler, and any name-matching pattern
misses it silently.

A signature and a fingerprint share a technique — a pattern matched
against source text — and nothing else. A fingerprint reads the whole
project, one match anywhere is enough, and it yields a label. A signature
reads one class, matches in a named place, and yields membership. Calling
them one mechanism is what let two rounds hand each of them the other's
domain.

The answer is a block under a fixed heading, in one grammar, so a session
loading a document written elsewhere can tell whether the contract is met
— the base-class answer, in full:

```
Signature:
  header: extends TriggerHandler
Framework types: TriggerHandler
```

`header:` matches the type's declaration header — from the `class` keyword
to the opening brace — which keeps a comment, a string or a javadoc
mention from counting. `implements TriggerAction.` there — the
metadata-driven answer — matches every one of that framework's
interfaces, a class implementing several, and a class implementing
something else besides. `member:` matches a method declaration line inside
the type, which is where the frameworkless answer,
`handle(System.TriggerOperation`, belongs and where a header match would
never look. A header runs from the `class` or `interface` keyword to the
opening brace however the line breaks fall, so a header split over lines
is still one header, and the modifiers before that keyword — `abstract`,
`virtual`, `global` — sit outside the match and never have to be
enumerated. Matching ignores case, because Apex does, and an optional
namespace prefix is allowed before every type name, because a framework
delivered as a managed package appears in project code as `extends
acme.TriggerHandler`. A document may add a filename glob as a hint, never
as the test.

The handler set is the smallest fixed point of the classes matching the
signature together with the classes whose header `extends` a type already
in the set. Without that closure, `OrderHandler extends
BaseTriggerHandler` — an org's own layer over the framework's — matches
no pattern and goes ungraded. The boundary between the two is worth
one sentence: a class matching the signature is a handler on that match
alone, and the parent rules below govern **closure candidates** — a class
matching no signature whose header carries `extends`. Otherwise
`OrderHandler extends acme.TriggerHandler`, a framework delivered as a
managed package, would be admitted by the namespace prefix and rejected
by the same paragraph.

The candidate is defined by what its header carries, never by what it
might turn out to be: the second reading is circular, and a rule that
fires on every unreadable parent would report most of a repository. Most
classes extending something the repository does not hold extend a
platform type, `extends Exception` first — the shipped example's own
`OrderProcessingException` does
(`salesforce-apex/reference/trigger-handler.md:177`). Unreadable parents
are therefore reported in aggregate: one Summary line naming the distinct
parents with a count each. Nothing about the line is graded, and a
namespace-qualified parent is the one worth a second look — as a reading
hint, never as the test. Making it the test was the sharper alternative
and was declined: it assumes an unqualified parent absent from the
repository is a platform type, which fails wherever the repository is a
partial view of the org — unretrieved unpackaged metadata, or a
neighbouring package in the org's own namespace, where the prefix is
optional. There the absent parent is the project's own base class, which
that test would skip in silence and the aggregate line names outright.

The closure reads parents from the repository even where a parent lies
outside a diff-scoped run, so a full run and a diff-scoped run select the
same handlers; a parent under a vendor path is read to recognise it and
never graded; a parent absent from the repository leaves a closure
candidate a non-handler, counted on that one Summary line. Only top-level
types are handlers — a metadata-driven action is instantiated by name and
`Outer.Inner` is addressable, so that document names the deviation rather
than leaving it to a reader. Naming it is all it does: the grammar has no
key for an exception, so such an action goes ungraded and the document
says so, which is the honest end of a rule that reduces to a grep.

`Framework types:` names what the framework itself owns — a copied base
class, a dispatcher. An absent field and an empty one say the same thing,
as they do for `vendor-paths:`, and that is the frameworkless answer; a
document omitting the field still has a signature, and only a malformed
`Signature:` block fails the grammar. The field is also the only place
those names are written: a Fingerprint answer that has to read inside a
framework's own class points at a type from here rather than repeating
it.

What the field buys is one exemption, which is why a document may leave
it out. Its types are read to recognise a framework, graded by no
framework rule, and exempt from `trigger-context-below-handler`, which
says so itself. Without them, a base-class project's own copy of
`TriggerHandler.cls` reads `Trigger.*`, matches no signature and sits
under no vendor path, and the rule fires on the framework.

Framework-specific rules are optional. A document that carries none is
graded by the framework-independent rules alone, and the report says so. The tag grammar does
not become a public contract in this release, so a document from outside
this plugin is not graded on its framework rules at all.

The signature grammar is public regardless — a deviation from the second
consultation, which proposed publishing it together with the tag grammar
and never separately. A document from another plugin must write its
signature in that grammar or its handlers cannot be selected, and
selection buys such a document `trigger-context-below-handler` alone. A
small return, and the grammar has to be published for even that, so the
two grammars move on their own schedules.

## Resolution protocol

One framework id names each shipped framework everywhere it appears —
declaration value, fingerprint row, document filename, rule prefix. A
shipped id names an **approach**, never a product, which is why two
base-class frameworks share one document and one prefix.
`salesforce-triggers` owns the table:

| `framework-id` | Document | Rule prefix |
|---|---|---|
| `base-class` | `reference/framework-base-class.md` | `trigger-base-class-` |
| `metadata-driven` | `reference/framework-metadata-driven.md` | `trigger-metadata-driven-` |
| `frameworkless` | `reference/framework-frameworkless.md` | `trigger-frameworkless-` |

An id absent from this table is a framework this plugin does not ship. Its
declaration carries a `doc-path:` or a `skill:` locator, and the table
never grows to accommodate one — that is the open class working as
intended.

A `doc-path:` is read as a file, relative to the repository root. A
`skill:` is invoked by its `plugin:skill` name, which is how the platform
addresses a skill and needs no path the project would have to know; a
skill whose plugin is not installed takes the missing-document row below,
since a locator naming nothing and a path naming nothing fail the same
way. This is not the slash-command invocation the design rejected: that
question was whether *our* per-framework guidance should be skills, and
loading a skill the project points at is a different act.

### Three mechanisms, three shapes

The protocol reads three things from outside itself, and they are not one
mechanism. A **signature** selects over a class's content and comes from
the framework document. A **declaration** resolves over a path, comes from
the project in several places, and carries a scope. **`vendor-paths:`**
filters over a path, comes from one place, and carries no scope at all.
Two review rounds caught this design handing one of them another's rules
by default — a filter given a scope, a resolver read as content, a
selector scoped to the run — so each is specified separately below and
none inherits from a neighbour.

Each specification answers the same five questions, and answering four of
them is what bred the defects: where the thing is declared and in what
grammar; what it applies over and where in the order; what it returns,
including the value that means *unresolved*; who consumes that value and
in what words; and what makes a document carrying it conformant, tested
when the document loads. One constraint crosses all three: every test
reduces to a grep, a prefix comparison or a glob match, never to parsing.
The glob is the weakest of the three, the platform naming no dialect for
it, which is why a pattern whose coverage cannot be settled counts as
covering rather than being evaluated harder. A monorepo
holds thousands of Apex classes and the reader is a model with file tools.

### The declaration

One line, one key:

```
trigger-framework: base-class
trigger-framework: metadata-driven
trigger-framework: frameworkless
trigger-framework: acme-dispatcher; doc-path: docs/acme-triggers.md
trigger-framework: acme-dispatcher; skill: acme-plugin:acme-triggers
vendor-paths: force-app/nebula, force-app/vendor
```

The key sits in the file's body, at the start of a line — not in a rule's
frontmatter, whose keys belong to the platform's schema — and a line
inside a fenced code block does not count, which is what lets this spec
quote the key without declaring one. One declaration per home, one value
per key. The value is everything after the key, locator included: two homes
naming one framework through different documents disagree, and ranking
treats them as it treats any two values. A shipped id carrying a locator
is a contradiction: the shipped document is used and the locator
reported. An id absent from the table
carrying no locator is the homegrown-without-a-document case below. Two
`trigger-framework:` lines in one home make that home unreadable, which
is reported with the file rather than resolved by picking a line.

`vendor-paths:` is the second key of the surface, and the only other thing
the protocol reads from the project. It lists what belongs to a package
the project did not write. The scope is **declared, never inferred**: a
package installed unlocked and without a namespace, vendored as source,
sits in a package directory carrying no platform signal that marks it
foreign, so no amount of reading `sfdx-project.json` recovers it.

Unlike the framework key, it resolves at **the repository root** alone.
What counts as somebody else's code is a fact about the repository rather
than about a path inside it, and a scope rule would get an exclusion
backwards — an inner declaration narrowing it would re-include the vendor
directory it was written to remove.

Its value is a list of **directory prefixes** relative to the root, not
globs: a file is vendor when its path equals an entry or begins with that
entry and a slash. That is the shape `packageDirectories` already uses,
so the two exclusion layers compose in one arithmetic of prefixes; it
leaves no glob dialect to name and no question of whether an entry matches
a file or a directory; and it reduces the test to a prefix comparison
rather than a match an agent can get wrong. Nothing re-includes, so an
entry is a declaration to make narrowly.

Every root home carries the key — both root `CLAUDE.md` files and every
rule file outside a payload directory, whatever its `paths:`, since this
key has no scope for a glob to narrow — and several homes **union**,
which needs no order because exclusion is monotonic. An absent key and an
empty one say the same thing: nothing is vendor. An entry matching
nothing on disk earns a note, the only signal an agent can give for a
typo. An entry outside every package directory is redundant and passes in
silence, the first layer having excluded it already. A monorepo lists
every vendor path at the root and loses nothing but locality.

Homes, and the exact set a grep reads: `CLAUDE.md` and
`.claude/CLAUDE.md` at the repository root or in any directory above the
trigger file, plus any rule file under `.claude/rules/` that sits outside
a directory carrying a Rules-engine manifest — the manifest is what marks
a directory as an installed payload, so ownership becomes something a
grep can see. The protocol greps these files rather than waiting for the
platform to load them, which also settles a question the platform
documents nowhere: whether a nested `.claude/CLAUDE.md` is discovered at
all.

Three things are deliberately not homes. A declaration belongs to the
project, so a personal rule under `~/.claude/rules/` never carries one —
it would follow the developer between projects that disagree. Neither does
`CLAUDE.local.md`, on the same footing and for a sharper reason: it is
documented as personal, git-ignored preference, so declaring there would
resolve the author's own sessions while every teammate and every CI run
reported the declaration missing — the one reader who could fix it is the
one reader who never sees it. And the installed `salesforce-toolchain.md`
copy is not a home either: the
Rules engine owns that file, so its next sync either overwrites a
hand-added line or freezes the rule at the version that carried it, and
its `paths:` already covers `**/*.trigger` repo-wide — the same scope as
the root `CLAUDE.md`, which would manufacture a collision by construction.

Every declaration carries one, and the kinds are shaped differently. A
`CLAUDE.md` scopes itself by **position** — the subtree of the directory
holding it, and for `.claude/CLAUDE.md` the subtree of the directory
holding `.claude/`. A rule declaring `paths:` scopes itself by **glob**;
a rule declaring none scopes the whole repository, which is the root
subtree and ranks as one. Reading that rule as an unrankable glob would
cost the design its commonest comparison — a repository-wide default
against a per-package override — for nothing. A rule always sits at the
repository root whatever its glob says, so position tells nothing about
how narrow it is.

Ranking runs in three moves, and every declaration keeps its own scope
through all of them. First, count the **distinct values**: a root
`CLAUDE.md` and a repository-wide rule naming the same framework agree,
and the record names both. A project writes that redundancy without
thinking, and grading agreement is not grading a defect. Second, one
distinct value means resolved. Third, more than one means the winner is
the declaration whose scope is strictly contained in the scope of
**every** declaration carrying a different value — subtree within subtree
by path prefix, and never a pair involving a glob, since comparing a glob
to anything invents an answer the project never stated. Because nothing
is merged, a repository-wide default against a nearer override still has
two scopes to compare, and a chain of three candidates settles without a
case of its own.

No such declaration means no winner, which the next section turns into
behaviour rather than a tie-break. Two members of that set are worth
naming, because both look resolvable and are not. `CLAUDE.md` and
`.claude/CLAUDE.md` in one directory carry the same subtree, so neither
contains the other — and the platform documents nothing about what
happens when both exist, so a protocol picking one would claim knowledge
nobody has. Two rules with differing `paths:` are the same case for the
same reason.

Where a glob's coverage cannot be settled, the pattern counts as
covering. The platform names no dialect for `paths:`, so the protocol
applies the matching the platform applies and leans on `**`, `*`,
`{a,b}` and root-relative paths alone. A declaration that covers and
cannot be ranked is loud; one dropped from the set is silent.

### Steps

Resolution runs per file. For a trigger file it decides which framework's
rules grade that trigger; for a handler class it decides the same, from
the declarations covering the class's own path. Step (a) collects every
declaration whose scope covers the file — walking up the directory tree
for `CLAUDE.md` homes and reading `paths:` for rules — and then ranks
them as above.

The order is itself a contract: each step consumes what the one before it
produced.

| Step | Action |
|---|---|
| (0) | read `vendor-paths:` from the root homes and subtract it, with the directories outside `packageDirectories`, from the repository's Apex files — what remains is the grading universe every later step works over, whether the caller is a review run or a session about to write a trigger |
| (a) | grep the covering homes for `trigger-framework:` and rank them — an explicit read, never a wait for context |
| (b) | fingerprint the grading universe, reading a framework's own types outside it where the Fingerprint answer points at one of the types `Framework types:` names |
| (c) | ask the developer, with `reference/choosing-a-framework.md` — the case for and against each of the three shipped approaches, plus a fourth entry sending a recognition label or an unknown framework to the homegrown-document path rather than to a comparison this plugin cannot write |
| (d) | select the resolved framework's handlers from the grading universe by its signature, closed over `extends` |

Steps (0) through (c) serve both surfaces. Step (d) belongs to the review
surface alone: a session about to write a trigger needs the resolved
document, not an enumeration of the project's handlers.

Vendor code is never graded and never fingerprinted, and it is still
**read** where recognition needs it. Those two verbs get two answers on
purpose: the discriminator separating the two base-class frameworks is a
method name inside `TriggerHandler.cls`, which a project vendoring the
framework as source puts under `vendor-paths:` — so a step forbidden to
read there could not tell the two frameworks apart.

**Who repairs what.** Step (c) and the collision between declarations the
protocol cannot rank both need a person, so both belong to an interactive
session. A background agent asks nothing: it enforces the rules it can
resolve and reports whatever it cannot. A session, in turn, does not
settle such an ambiguity in conversation — an answer there dies at the
next compaction while the ambiguity returns every session. It settles it
in the project, by rescoping or removing one of the competing homes until
the declaration surface states one framework per path and says so
unambiguously. The fix is an edit, not an answer.

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

Every pattern tolerates an optional namespace prefix, in the form the
token's kind takes: `ns.` before a class name, `ns__` before an object or
Custom Metadata API name. One form would recognise half of the
metadata-driven row, whose tokens are Custom Metadata API names rather
than classes. The allowance is made for the fingerprint's own reason
rather than the signature's: a fingerprint exists to recognise, and a
framework delivered as a package is exactly the case a literal
`extends TriggerHandler` would miss, sending a project that plainly has a
framework to the question asking whether it has one.

Only the first three rows carry shipped ids. `fflib`, `TDTM` and
`dispatcher` are recognition labels: they name what the pattern found so
the session can say it out loud, and they are products or families rather
than approaches. A label becomes an id only when something declares it,
and then it is the project's word, not this table's.

The metadata-driven fingerprint keys on Custom Metadata records and the
trigger body, never on the framework's classes: the records sit in the
repository whether the framework arrives as an unlocked package or as
source, while the classes appear only in the second case.

The base-class document must also separate two frameworks that look
identical in the trigger body and differ in error semantics. The
discriminator is the method name inside `TriggerHandler.cls`:
`incrementCheckLoopCount` silences an exceeded loop count,
`addToLoopCount` throws.

That file is unreadable where the framework arrives as a managed package.
What the base-class document owes then is stated with question 3 above,
beside the rest of that document's error-semantics duty.

### Exclusions

Two layers, not one: directories outside `packageDirectories`, and the
paths `vendor-paths:` declares. The first is read from
`sfdx-project.json`, and contributes nothing where that file is absent —
a repository in metadata-API format has no package directories, so its
universe is every Apex file the run covers minus `vendor-paths:`; the
second must be declared, because a package
installed unlocked and without a namespace and vendored as source sits in
a package directory with nothing marking it foreign. A logging package
distributed that way puts its classes in the org's own namespace beside
the project's, and its own triggers on its own objects are not the
project's to review. Reviews already exclude this material —
`salesforce-code-review/SKILL.md` states "never review third-party
libraries" — so the exclusion needs a scope, not a rule, and
`vendor-paths:` is where that scope is stated. It excludes material from
grading and from fingerprinting, never from reading: the Steps table above
states where recognition reaches into a vendor path and why it must.

### The resolution record

Up to three lines, before the first trigger edit. The first carries the
framework, the source and the document loaded; the other two carry what
the filter and the selector actually did, and the third belongs to the
review surface alone:

```
Trigger framework: base-class — declared in force-app/billing/triggers/CLAUDE.md — loading framework-base-class.md
Vendor paths: 2 entries from CLAUDE.md
Handlers: 7 selected by the signature in framework-base-class.md
```

The first line's source names every file that declares, not one: where
homes agree it lists them all, and where a nearer declaration beat a
repository-wide default it names both with the winner first, since the
disagreement is always stated. Resolution being per file, a monorepo
yields one record per resolved framework with the paths it covers, and
that is what `/salesforce-review` passes in the prompt; an agent finding
the record and the declaration disagree reports the mismatch and grades
by the declaration, the files being the authority. Where the resolved
framework's document turns on a discriminator its own question 3 names —
the base-class case — the variant is read when the document loads and
named on this first line, because it decides which of two error semantics
that document's rules carry.

The last two lines exist because an agent that cannot ask must at least
say which filter and which selector it applied. Without them, "no
framework findings" and "framework rules not graded" read identically.
Each degrades in place — `none declared`, or the reason no handler set was
selected — and the `Handlers:` line appears only where step (d) ran,
which is the review surface; an authoring session's record stops at the
document. The source reads `declared <file>`, `inferred <evidence>` or
`asked`. Any source other than `declared` ends with an offer to write the
declaration:
a line in a conversation dies at the next compaction, a declaration
survives it. `salesforce-triggers` never remembers a resolution; after compaction it
reads the files again.

### Failure modes

| Situation | Behaviour |
|---|---|
| No declaration, fingerprint matches | infer, cite the file and pattern, offer to write the declaration |
| No declaration, no fingerprint | go to (c), saying no pattern matched in N triggers and asking whether the project is frameworkless or on a framework this plugin does not know |
| No triggers at all | go to (c) |
| A fingerprint matches a framework this plugin ships nothing for — fflib, TDTM, a dispatcher | the label is sound and only the document is missing, so take the homegrown row below: offer to write a project document, never substitute another framework's |
| Two subtree-scoped declarations disagree | the inner one wins, and the disagreement is always stated — never resolved silently |
| Two declarations cover the file with different values and neither is a subtree containing the other — a glob-scoped rule against a `CLAUDE.md`, two rules whose `paths:` differ, or `CLAUDE.md` beside `.claude/CLAUDE.md` in one directory | no winner: name every file that declares, then work out with the developer which home survives and write that change. Picking one silently would answer a question only the project can, and answering it in conversation would leave the collision to recur next session |
| The resolved document answers question 1 without a signature, or with one that does not fit the grammar | skip the framework rules **and** `trigger-context-below-handler`, the one framework-independent rule needing a handler set; grade the rest and name the document in the Summary — a document that cannot say what its handlers are cannot have them graded, and guessing a signature would repeat the mistake a filename pattern already made |
| A class matches two frameworks' signatures | grade it under the framework resolved for its own path, which is step (a) over the class rather than over a trigger; where that path resolves to one framework and the class still matches another's signature, grade it under the resolved one and name the other in the Summary |
| A closure candidate's `extends` parent is not in the repository | treat the class as a non-handler and count it on the Summary's one line of distinct unreadable parents — a managed-package parent is unreadable by construction, assuming membership would grade a class no rule was written for, and naming each class individually would bury the signal under every custom exception. A class matching the signature itself is unaffected, parent or no parent |
| The base-class framework arrives as a managed package, so `TriggerHandler.cls` cannot be read | select handlers as usual, the signature matching the project's own classes, and grade every rule except those keyed to error semantics, naming in the Summary that the discriminator was unreadable — a guess between silencing and throwing is the one guess that turns a correct bypass into silenced automation |
| A home carries two `trigger-framework:` lines, or a shipped id with a locator | the home resolves nothing and is named; a shipped id keeps its shipped document and the stray locator is reported |
| `vendor-paths:` is absent and a directory is plainly third-party | grade it as the project's, since nothing declares otherwise, and note the directory with its evidence in the Summary — a note rather than a finding, because no rule requires the key |
| A `vendor-paths:` entry matches nothing on disk | note it; nothing distinguishes a typo from a directory yet to be added, and a typo silently excludes nothing |
| The declared document is missing | say so and grade by the framework-independent rules; never substitute another framework's document, since guidance for the wrong framework writes code that does not compile |
| A homegrown framework with no document | offer to write one, describing their code rather than a pattern from the internet — the "dispatcher, handler, helper" division has no primary source |

## Review surface

`salesforce-code-review` gains a step, triggered by any Apex file in the
run — not a `.trigger` alone, since framework rules grade handler classes
and a change touching only those needs the same resolution. A `.trigger`
is merely the one artefact every framework has. The step loads
`salesforce-triggers` and runs the
protocol's steps in order, (0) through (b), then load each resolved
framework's document by path or name and take step (d), selecting that
framework's handler classes out of the grading universe by the signature
its Dispatch answer gives. Resolution runs per file throughout, so a
monorepo running two frameworks loads two documents and grades every
class under the framework resolved for its own path. Which classes the
framework rules grade is resolved, never hardcoded, because only the
framework knows what makes a class one of its handlers.

A background agent enforces standards and asks nothing, which bounds the
protocol rather than the agent. Steps (0), (a) and (b) are mechanical
reads it performs like any other; step (c) is the one it cannot take, and
so is the offer to write a declaration that follows an inference.
`/salesforce-review` resolves before dispatch and passes the record in
the prompt, as it already passes the directory mode, which spares the
agent that work and lets it verify the record against the declaration for
nothing. Dispatched any other way it resolves for itself, and where
resolution would need step (c) it reports the framework as unresolved —
choosing a framework for the project is as far outside its job as asking
for one.

When resolution fails, the run grades the framework-independent rules, skips framework rules
rather than guessing them, notes `trigger framework: unresolved —
framework-specific rules not graded` among the Summary's out-of-scope
notes, and reports the declaration rule in the `## Project` section —
`trigger-framework-declared` where nothing declares the path,
`trigger-framework-declared.ambiguous` where two the protocol cannot rank
do. Both slots already exist in the review-report contract, whose Summary is
"outcome, out-of-scope notes, and (for a rerun) the prior findings'
disposition" (`review-reports.md:117-118`) — so every note this design
adds, the aggregated unreadable parents and the two `vendor-paths:` notes
included, is an out-of-scope note rather than a new kind of content. Where
resolution succeeds and the document supplies no signature, the same note
names `trigger-context-below-handler` beside the framework rules, that
rule needing a handler set too.

## Changes to shipped content

Three shipped rules are touched, and the spec names each because a moved
id breaks a citation — one changes owner, one keeps its id and loses a
name from its scope, one stays put and is cited from the new skill:

1. "One trigger per object" leaves `apex-layering` for
   `trigger-one-per-object`.
2. `<Object>TriggerHandler` leaves `apex-naming`. `salesforce-triggers`
   names only `<Object>Trigger`.
3. `apex-bulkification` and its sub-rule stay put, cited by
   `salesforce-triggers`.

The frameworkless document adopts a dispatch shape that keeps
`trigger-body-delegates` true:

```apex
trigger OrderTrigger on Order (before insert, before update, after update) {
    OrderTriggerHandler.handle(Trigger.operationType, Trigger.new, Trigger.oldMap);
}
```

The handler switches on `System.TriggerOperation`. This fixes the defect
named above, makes the rule true for all three frameworks, and gives
the frameworkless handler what the frameworks already have: a dispatch
entry point callable from a test without DML.

The example splits rather than triples. `OrderDomain`, `OrderSelector`,
`OrderService` and `OrderProcessingException` do not depend on the
framework and stay in `salesforce-apex/reference/`. Each framework
document carries `OrderTrigger` and `OrderTriggerHandler` and calls the
same lower-layer methods, so the three examples are demonstrably one
scenario.

Those four units stay in one file, and the file is renamed —
`order-layers.md` — because `trigger-handler.md` would name a trigger and
a handler it no longer carries, which is the kind of thing this standard
exists to stop. The skill's pointer moves with it and nothing outside the
skill cites the filename; this spec's own citation of the old name
predates the rename and is left as the evidence it was.

## Evidence and its limits

Framework behaviour was read from source, not from documentation. Two
findings correct the documentation:

- The base-class fork documents `TriggerHandler.setGlobalBypass()`, which
  its source does not define. The method is `bypassAll()`.
- Its silent stop is deliberate. The `throw` sits commented out beside the
  line `// Do not throw an exception if we exceed the loop count - just
  stop executing`.

Three provenance notes are recorded so a later reader can judge them —
two citations weaker than the rest, and one claim carrying no citation at
all:

- Apex Developer Guide quotations come from the official PDF, fetched with
  TLS verification disabled after the HTML pages returned 403.
- Well-Architected quotations come from two consistent extractions of the
  same page rather than a byte-exact fetch.
- Apex's case-insensitivity, which the signature grammar relies on, is
  uncited. The language reference pages return 403 and the PDF was not
  extracted for it, so the claim rests on expert knowledge — as sound as
  it is unverified here.

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
context, but `salesforce-triggers` reads shipped and project-local documents by path in
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
  layer. fflib split domain from trigger handler in March 2021 and its
  sample code now separates them. The decision stands on the
  metadata-driven case, where the handler is the framework's own class.

A second consultation, on the three mechanisms above, followed two
blocking rounds that diagnosed one repeated failure. Its proposals are
adopted but one, three of them as choices rather than repairs:

- **`vendor-paths:` carries directory prefixes, not globs.** Prefixes
  compose with `packageDirectories` in one arithmetic and leave no dialect
  to name. The cost is that `**/nebula` cannot be written; a monorepo pays
  it by listing paths at the root, which this design already accepted.
- **A handler class is graded under the framework resolved for its own
  path.** The designer named this the developer's call, against grading by
  whichever signature matches anywhere in the run. Resolving per path is
  the generalisation round one already made for trigger files, and the
  alternative ungrades every class in a monorepo running two frameworks.
- **An undeclared vendor directory earns a note, not a rule.** A minor
  rule was the alternative, an analogue of `trigger-framework-declared`.
  The note is the narrower change and keeps clear of the ruling that this
  scope is declared and never inferred; the rule is an open question
  below.

One proposal is declined. The designer would couple the signature grammar
to the tag grammar, publishing neither before the other. A foreign
document cannot write a conforming signature without the grammar, so
withholding it would leave every foreign document's handlers
unselectable, and with them the one framework-independent rule needing a
handler set — the reasoning
sits beside the clause it concerns, under "What a framework document
answers".

## Out of scope

- **Migration between frameworks.** Deferred, with it the rule that would
  grade a new file against a declared target.
- **The tag grammar as a public contract.** A document from another plugin
  is not graded on framework rules, so that grammar stays internal. The
  signature grammar does go public, so it is a convention others rely on
  in the sense `plugin-versioning` defines: a change to `header:`,
  `member:` or `Framework types:` takes the bump that rule prescribes.
- **Generality across the Standards family.** `python-standards` commits
  to one toolchain outright, so resolving between frameworks has a single
  instance today and stays local to this plugin. Should a second
  Standards plugin ever need it, the pattern is a candidate for the
  family rule ticket #14 defines, not something this spec anticipates.
- **Enforcement.** No hook ships. `PreToolUse` could deny a write to a
  `.trigger` file with no declaration in scope, and `InstructionsLoaded`
  could not help at all, having no decision control. The consequence is
  recorded rather than hidden: a session that writes a trigger without
  loading `salesforce-triggers` meets no obstacle, and review catches the miss
  afterwards through `trigger-framework-declared`.

## Open questions

- **Ticket.** None. The developer chose to open no issue and to name the
  branch `feature/trigger-frameworks`, without the issue number the
  repository convention prescribes. A ticket may still be opened before
  the pull request.
- **Whether the TDTM fingerprint keys on the subscriber's own code.**
  The row is `TDTM_Config_API.run(`. Round 5 noted, without grading it,
  that in a subscriber repository this call sits inside NPSP's packaged
  triggers rather than the project's code, and that the subscriber-side
  signal is more likely `extends npsp.TDTM_Runnable`. The row predates the
  namespace allowance and nobody has verified it against an NPSP org.
- **Whether an undeclared vendor directory should be graded.** Today it
  earns a note in the Summary. A minor rule — the analogue of
  `trigger-framework-declared` — would grade it, and the only argument
  against is that inference would then produce a finding. Undecided.
- **How many consumers run a framework other than frameworkless.**
  Unknown, and no longer load-bearing: the question tested the
  proportionality of shipping four skills, and this design ships one skill
  with three documents.

## Review rounds

### 2026-09-08 — architect, fable 5.1, blocking (round 1, full-document)

- fixed 2026-09-08 — [Important] The review step's file scope, `*TriggerHandler*.cls`, matches no handler class in a metadata-driven project, so that project's framework rules go ungraded; license: the parts table excludes the dispatching class's name from `salesforce-triggers`, and question 1 already owns the dispatch shape; the review step now resolves on `.trigger` alone and takes the handler glob from the framework document, which question 1 was extended to carry
- fixed 2026-09-08 — [Important] The `.ambiguous` sub-rule's wording fires on the nested-`CLAUDE.md` override the protocol itself resolves, and "competing" is left undefined; license: `.claude/rules/standards-rule-tags.md:40` requires a sub-rule that could overlap to draw its boundary explicitly; the sub-rule now names the unequal-shape no-winner case, and the text states that a root default with a nearer override is a configuration the protocol resolves rather than a violation it grades
- fixed 2026-09-08 — [Important] Naming the installed `salesforce-toolchain.md` copy a declaration home contradicts the parts table and manufactures the unequal-shape collision by construction; ruling: 2026-09-08; the copy is no longer a home, and the homes paragraph now says why — the Rules engine owns that file, and its `paths:` already covers `**/*.trigger` repo-wide
- fixed 2026-09-08 — [Important] The vendor-exclusion scope carries both the critical rule and step (b), yet the spec never says how that scope is known; ruling: 2026-09-08; a second declaration key, `vendor-paths:`, carries the scope, and the exclusions section states it is declared and never inferred, since a namespace-less package vendored as source carries no platform signal
- fixed 2026-09-08 — [Minor] The framework id appears in three vocabularies, and the `framework-id` → path table the skill is said to own is never given; license: the base-class document already covers two products, which chose approach ids over product ids; one id now names each framework everywhere, `trigger-actions` became `metadata-driven`, `-none` became `-frameworkless`, and the table is given
- fixed 2026-09-08 — [Minor] A fingerprint match on fflib, TDTM or dispatcher yields an id with no shipped document, and the failure-mode table states no next step; license: that table already routes a missing document to the homegrown row; a row now sends an inferred unshipped framework there
- fixed 2026-09-08 — [Minor] "A rule always sits at the repository root" omits user-level rules, and the `CLAUDE.md` homes omit `.claude/CLAUDE.md` and `CLAUDE.local.md`; license: the parts table already says the declaration belongs to the project, which excludes a personal rule; the homes paragraph now names the grep candidate set exactly and rules out `~/.claude/rules/`
- fixed 2026-09-08 — The fflib domain/handler split is dated April 2021 where the reviewer's cited commit is 2021-03-15; license: the reviewer's citation, offered as an ungraded aside; the date now reads March 2021
- hit fixed 2026-09-08 — the parts table still scoped the review step to `.trigger` and `*TriggerHandler*.cls` after the first finding's fix removed the second pattern everywhere else; the row now reads `.trigger` plus the handler glob the resolved framework document supplies
- signal 2026-09-08 — one diff-scoped round should close the document once the four Important findings land; a full-document re-read is warranted only if the first finding's repair moves the handler-shape question into the framework-document contract, and the Minor leftovers are worth a single fix wave rather than a round of their own

### 2026-09-08 — architect, fable 5.1, blocking (round 2, diff-scoped)

- fixed 2026-09-08 — [Important] The handler-glob repair swapped one naming-convention scope for another: every `.cls` is already in the run scope, so the pattern's real job is selecting which classes framework rules grade, and no framework imposes handler names — a legacy-named class implementing `TriggerAction.BeforeInsert` matches no glob and goes ungraded; license: the Fingerprints table already recognises frameworks by content pattern, the mechanism this repair was missing; question 1 now supplies a signature, the review step selects handlers by it out of the classes already covered, a glob is demoted to an optional hint, and a failure row covers a document that answers question 1 without one
- fixed 2026-09-08 — [Important] The `.ambiguous` sub-rule grades "two declarations of unequal shape" while the ranking rule leaves two globs unrankable and equal in shape, so two project rules declaring the same path fall between the sub-rule and the group default; license: the rule's own closing sentence already states the boundary as "two the protocol cannot rank"; the sub-rule, its prose, the review section and the failure row now all read that way, and the second pairing is named outright
- fixed 2026-09-08 — [Important] `CLAUDE.local.md` is listed as a declaration home although the same paragraph excludes personal rules because a declaration belongs to the project; declaring there resolves the author's session while every teammate and CI reports the declaration finding; license: the recorded license of the round-one fix excludes a personal file on exactly this footing; the file is no longer a home, and the paragraph says why in terms of who can see the finding
- fixed 2026-09-08 — [Important] `vendor-paths:` borrowed the declaration surface's homes but no resolution rule: nothing states what the globs are relative to or how values combine across homes, nearest-wins is backwards for an exclusion, and no step reads the key that the critical rule's scope depends on; ruling: 2026-09-08; the key resolves at the repository root alone with root-relative globs, which removes the combination question rather than answering it, and step (a) now reads it
- fixed 2026-09-08 — [Minor] `trigger-one-per-object` scopes by object ownership while Exclusions scopes by path, so a vendor trigger on a standard object is skipped by one and counted by the other; license: the Exclusions section, rewritten in the previous wave, already states the scope by path; the rule now reads "under `packageDirectories` and outside `vendor-paths:`"
- fixed 2026-09-08 — [Minor] "The ids name an approach, never a product" is contradicted by the `fflib` and `TDTM` fingerprint rows, which the same wave calls sound ids; license: the id table the same paragraph introduces holds three rows, so the principle was always about shipped ids; the principle now says so, and the remaining fingerprint rows are named recognition labels
- fixed 2026-09-08 — [Minor] The homes set is called exact while one member is defined by ownership, which a grep cannot see; license: the glossary defines a Rules payload as installed beside a manifest, which makes ownership mechanical; the member is now "a rule file outside a directory carrying a Rules-engine manifest"
- fixed 2026-09-08 — this wave left two sentences carrying the old "unequal shape" boundary, in the specificity paragraph and in "Who repairs what"; license: the same sentence that licensed the sub-rule's repair; both now read "the protocol cannot rank". No reviewer graded this and no gate detected it — the session's own sweep found it, so the line carries no severity and is not a gate line
- signal 2026-09-08 — a diff-scoped round 3 over these repairs earns its cost, since each Important fix reshapes a mechanism and that is the class breeding the next round's defects; a full-document re-read now would read text about to change, so the chain debt is better discharged by the integrity audit at the consumption gate, and the three Minor leftovers belong in round 3's diff rather than a round of their own

### 2026-09-08 — architect, fable 5.1, concerns (round 3, diff-scoped)

- fixed 2026-09-08 — [Important] The managed-package base-class case falls between two clauses of the same wave: `extends acme.TriggerHandler` satisfies both the namespace-prefix allowance in the signature grammar and the parent-absent row that makes an unreadable parent a non-handler, and the discriminator separating the two base-class frameworks is unreadable in a managed package, so even a selected handler cannot be graded on question 3; ruling: 2026-09-08; the allowance stands and the parent rules were scoped to closure candidates, a class matching the signature being a handler on that match alone; the base-class document now owes a second answer for an unreadable source, and the rules keyed to error semantics go ungraded with the Summary saying why rather than a reviewer guessing between silencing and throwing
- fixed 2026-09-08 — [Minor] "Identical values collapse" is written as merging declarations, so move three has no scope to rank and the three-candidate chain the same paragraph claims to settle has none for the merged value; the value compared is also never said to include the locator; license: the same paragraph claims to settle a chain of three candidates, which the finding shows it cannot; move one now counts distinct values while every declaration keeps its scope, nothing is merged, and the declaration grammar states that the value is everything after the key, locator included
- fixed 2026-09-08 — [Minor] `Framework types:` is mandatory in form while its empty value already means none, and a document omitting it loses its whole signature — against the sibling key, where an absent and an empty value say the same thing; license: the `vendor-paths:` paragraph already states that an absent key and an empty one say the same thing; the field is now optional on that footing, only a malformed `Signature:` block fails the grammar, and the paragraph says what the field buys — one exemption — so a foreign author knows when to write it
- fixed 2026-09-08 — [Minor] The signature grammar is published while Out of scope still says the grammar stays internal and `plugin-versioning` gains no new breaking surface, which that rule counts as a convention others rely on; "unreachable" also overstates what withholding it would cost; license: `.claude/rules/plugin-versioning.md:46-47` grades a breaking change to a convention others rely on; Out of scope now scopes its claim to the tag grammar and names the signature grammar as a published convention the bump rule covers, and "unreachable" became the concrete cost — every foreign document's handlers unselectable, and with them the one rule needing a handler set
- fixed 2026-09-08 — [Minor] Step (0), step (d) and the resolution record are defined in review-run vocabulary although the protocol runs at authoring time too, where there is no run and no handler set is needed; license: the resolution record is written "before the first trigger edit", which is the authoring surface the document already serves; step (0) now subtracts from the repository's Apex files for either caller, a sentence assigns steps (0) to (c) to both surfaces and step (d) to the review surface alone, and the `Handlers:` line appears only where step (d) ran
- fixed 2026-09-08 — [Minor] One type name is carried by `Framework types:` and by the Fingerprint answer for two consumers, against the one-mechanism-one-shape discipline the same wave introduced; license: the `Three mechanisms, three shapes` subsection, written in the same wave, forbids exactly this; `Framework types:` is now the only place those names are written and step (b) points at a type from that field rather than naming one of its own
- fixed 2026-09-08 — the F2 repair left the `.ambiguous` prose saying "identical values collapse before ranking", which the same wave had replaced with counting distinct values and merging nothing; license: the sentence the repair itself wrote; the prose now says ranking counts distinct values and agreement is not a collision. The session's own sweep found it — no reviewer graded it and no gate ran over it
- fixed 2026-09-08 — the review-surface paragraph still read "out of the Apex classes the run already covers" and named one framework document, lagging the per-file resolution this wave had already adopted; license: the Steps section states that resolution runs per file and the deviations section records the decision; the paragraph now selects out of the grading universe, loads each resolved framework's document, and says that a monorepo running two frameworks grades every class under the framework resolved for its own path. The reviewer noted the lag in one line without grading it and left it to the integrity audit; the propagation gate returned CLEAN over it
- hit dismissed 2026-09-08 — round one's `hit fixed` line says the parts table row now reads "`.trigger` plus the handler glob the resolved framework document supplies", while the row reads "handler selection by the signature the resolved framework document supplies"; counter: the ledger is chronological, and round two's own `fixed` line records replacing that glob with a signature and demoting the glob to an optional hint — a round-one line describing the round-one state is correct history, and the gate's brief was at fault for asking whether every historical line matches the current text
- signal 2026-09-08 — the stop signal is conditional on the held finding: under option (a) round 4 does not repay its cost, the Minor leftovers being self-fixable and the noted lag already owed to the integrity audit at the consumption gate; under option (b) one diff-scoped round over the base-class document's contract earns its cost, that being a reshaped mechanism again. The Minor leftovers are worth a single fix wave, not a round of their own

### 2026-09-08 — architect, fable 5.1, concerns (round 4, diff-scoped)

- fixed 2026-09-08 — [Important] The closure-candidate boundary makes the parent-absent row either unreachable or universal: a class whose parent cannot be read cannot be shown to reach the set, so the row never fires; read loosely, every `extends` of an absent type qualifies, and the shipped example's own `OrderProcessingException extends Exception` puts every conforming project in the Summary on every run; license: the mechanism discipline requires every test to reduce to a grep, which a definition by what a class might become does not, and the shipped example at `salesforce-apex/reference/trigger-handler.md:177` proves the loose reading's cost; a candidate is now defined by what its header carries — matches no pattern, header carries `extends` — and unreadable parents are reported in aggregate on one ungraded Summary line of distinct parents with counts. The reviewer's sharper alternative, naming parents by namespace prefix, was declined: it would rest on an unverified claim about Apex name resolution, and the aggregate line needs none
- fixed 2026-09-08 — [Minor] The namespace-prefix allowance lives only in the signature paragraph, so the literal base-class fingerprint misses `extends acme.TriggerHandler` and an undeclared managed-package project falls to step (c), which asks whether it is frameworkless or on an unknown framework when neither is true; license: the same section calls a fingerprint tolerant and gives recognition as its job; every fingerprint pattern now tolerates an optional namespace prefix, stated on the fingerprint's own grounds rather than borrowed from the signature
- fixed 2026-09-08 — [Minor] The discriminator's second answer is written in review vocabulary only, leaving the authoring surface — which loads the same document before the first trigger edit — with no instruction; this is the class round 3 fixed elsewhere; license: round 3's own fix for this class, recorded under that round's heading; the paragraph now says an authoring session has no Summary to write in, so it states both semantics and says the installed package decides which holds
- fixed 2026-09-08 — [Minor] The base-class document's owed answer sits under the Fingerprints subsection instead of the section that enumerates what a framework document answers, so an author reading that document's interface misses it; license: that section's stated job is what a framework document answers, and its fifth item is already scoped to the documents this plugin ships; the duty moved beside question 3 and Fingerprints keeps a pointer
- signal 2026-09-08 — a round 5 over these fixes does not repay its cost: none of the four reshapes a mechanism, each being a definition tightened or a clause added and checkable by the session against the cited lines, and the whole-document debt is already routed to the integrity audit at the consumption gate. One conditional: taking the reviewer's shape (ii) for the Important finding — naming parents by namespace prefix — would give the document an unverified language claim, which deserves a provenance note rather than a round. The leftovers are worth one fix wave, then the gate

### 2026-09-08 — architect, fable 5.1, LGTM (round 5, diff-scoped), debt discharged 2026-09-08

- fixed 2026-09-08 — [Minor] The closure-candidate definition reads "matching no pattern" where the test is the signature; "pattern" is the Fingerprints table's column name, and the spec itself states that conflating signature with fingerprint cost two rounds; license: that statement, in the paragraph separating a signature from a fingerprint; the definition now reads "matching no signature"
- fixed 2026-09-08 — [Minor] The namespace clause names one prefix form, `ns.` before a class name, while the metadata-driven row's tokens are Custom Metadata API names, which a package prefixes `ns__`; a literal reading of the clause recognises half of that fingerprint and sends the project to step (c); license: the clause's own stated reason is that a fingerprint exists to recognise, which half a match defeats; the clause now gives the form per token kind, `ns.` before a class and `ns__` before an object or Custom Metadata API name. The `ns__` form is the reviewer's expert knowledge, uncited like the case-insensitivity claim the Evidence section already flags
- fixed 2026-09-08 — [Minor] The recorded rationale for declining the namespace-prefix test calls its premise unverified, where the premise is false for a repository that is a partial view of the org — an unqualified absent parent can be the project's own base class, which that test would skip silently and the aggregate line names outright; license: the session's own decision in that paragraph, which the reviewer strengthened rather than contested; the rationale now names the partial-view case instead of calling the premise unverified, which closes a door "unverified" left open
- hit fixed 2026-09-08 — "Three rules change owner" over-claims for two of its three items: `apex-naming` keeps its id in `salesforce-apex` and only loses `<Object>TriggerHandler` from its scope, and `apex-bulkification` explicitly stays put; the sentence now says three shipped rules are touched and names what happens to each. The defect predates every wave of this loop and survived five architect rounds and four gate episodes
- fixed 2026-09-08 — integrity audit: question 5 is required of every shipped document while the frameworkless row states that no pattern is a fingerprint, so one of the three shipped documents has nothing to answer with; license: that row; question 5 now says the frameworkless answer is that nothing identifies it, which is why step (b) falls through
- fixed 2026-09-08 — integrity audit: the parts table gives fingerprints to the skill and omits them from what a framework document owns, while question 5 and step (b) make them the document's answer; license: both statements stand and only their division was missing; the skill owns the table and the document contributes its row, and both table rows now say so
- fixed 2026-09-08 — integrity audit: a background agent is told to run steps (0) through (b), which includes inference, and also that choosing a framework is outside its job, while a bare dispatch was said to report everything unresolved; license: "a background agent enforces standards and asks nothing", which bounds the protocol rather than the agent; the paragraph now says (0), (a) and (b) are mechanical reads it performs, and step (c) plus the offer to write a declaration are what it cannot take
- fixed 2026-09-08 — integrity audit: a failure row calls `fflib`, `TDTM` and `dispatcher` ids where the Fingerprints paragraph states a label becomes an id only when something declares it; license: that paragraph; the row now reads "the label is sound"
- fixed 2026-09-08 — integrity audit: the resolution record opens as three lines written before the first trigger edit while the same section says an authoring session's record stops at the document; license: the later sentence, written in round 3's wave; the record now reads "up to three lines" with the third belonging to the review surface alone
- fixed 2026-09-08 — integrity audit: a Settled decision still reads "the search walks up from the file to the nearest declaration", superseded by collect-and-rank, where the nearest does not simply win and a glob-scoped rule is not ranked at all; license: the ranking section and the rulings recorded for it; the decision now states collect-and-rank and says the nearest does not simply win. The line survived five architect rounds because no diff ever touched it
- fixed 2026-09-08 — integrity audit: "every test reduces to a grep or a prefix comparison" is broken by the glob coverage test, which the document itself calls unsettleable on an unnamed dialect; license: the document's own glob fallback; the constraint now names three mechanical tests and says the glob is the weakest, which is why an unsettleable pattern counts as covering
- fixed 2026-09-08 — integrity audit: the deviations section says the second consultation's proposals are adopted and two paragraphs later declines one; license: the declining paragraph; the sentence now reads "adopted but one"
- fixed 2026-09-08 — integrity audit: "Two citations carry weaker provenance" introduces three bullets, the third being an uncited claim rather than a weak citation; license: the list itself; the sentence now reads three provenance notes, two weak citations and one claim carrying no citation. Four propagation gates re-derived counters over this sentence and none caught it
- fixed 2026-09-08 — integrity audit, sixteen ranked implementer questions: fourteen are answered in the spec — where the key sits and what a grep must not match, how a `doc-path:` and a `skill:` locator are followed, what the record carries beyond the simplest case, what triggers the review step, the header grammar's edges and the inner-class deviation's honest end, the dispatching class keeping a rule in each shipped document, the universe where `sfdx-project.json` is absent, what `choosing-a-framework.md` covers, both keys in the toolchain rule and the reviewer agent's card being unchanged, and the review-report Summary slot these notes take (`review-reports.md:117-118`). One is a design call the session took and named: the four remaining example units stay in one file, renamed `order-layers.md`, because the old name would promise a trigger and a handler the file no longer carries. One remains the developer's — whether the unverified TDTM fingerprint row ships as it stands — and it was already the open question the audit ranked as its only blocker
- signal 2026-09-08 — a further round buys nothing: all three leftovers are lexical or clarifying, each licensed by the document itself, and fit one fix wave without a round. This LGTM is diff-scoped, so the whole-document debt belongs to the integrity audit at the consumption gate, or to a confirming full-document round should the developer take that arm of the pair, never to another diff-scoped round
