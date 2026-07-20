---
name: salesforce-apex
description: Use when writing or reviewing Apex backend code — naming, lightweight layering (one trigger handler per object, service, selector, domain), bulkification, governor limits, sharing keywords, and error handling. Apex unit tests belong to salesforce-apex-testing; access-model design to salesforce-security-model.
---

# Salesforce Apex

Standards for Apex classes and triggers: naming, layering, bulk safety,
governor limits, sharing, and error handling. Cite rules in review
findings as `(standard: salesforce-apex, rule: <id>)`; each rule names
its source — the Apex Developer Guide, Salesforce Well-Architected, a
PMD Apex rule name, or `this standard` (a recorded house decision).
Apex unit tests are out of scope here — see `salesforce-apex-testing`.
Access-model design (org-wide defaults, roles, sharing rules) is out of
scope here — see `salesforce-security-model`; this skill covers only
the `with sharing` / `without sharing` / `inherited sharing` keyword
mechanics.

## Naming

| Element | Convention | Example |
|---|---|---|
| Class | PascalCase, noun | `OrderService` |
| Interface | PascalCase, often an adjective | `Queueable` |
| Method | camelCase, verb-first | `activateFulfillment` |
| Variable / parameter | camelCase | `activatedOrders` |
| Constant (`static final`) | `UPPER_SNAKE_CASE` | `MAX_BATCH_SIZE` |
| Trigger handler | `<Object>TriggerHandler` | `AccountTriggerHandler` |
| Selector | `<Object>Selector`, methods `select*By*` | `AccountSelector.selectByIds(Set<Id>)` |
| Custom exception | `<Domain>Exception` | `OrderProcessingException` |

(id: `apex-naming`; source: Apex Developer Guide; PMD
`ClassNamingConventions`, `MethodNamingConventions`,
`FieldNamingConventions`, `FormalParameterNamingConventions`,
`LocalVariableNamingConventions`; the handler/selector/exception
patterns are this standard)

## Lightweight layers

**No fflib / Apex Enterprise Patterns dependency.** The layering below is
a naming-and-structure convention, not a library — fflib is cited only
as inspiration for teams that later want a fuller framework.

| Layer | Owns | Never does |
|---|---|---|
| Trigger | One line: hands the trigger context to its handler | Any conditional or business logic |
| Handler (`<Object>TriggerHandler`) | Routes each trigger event (before insert, after update, …) to domain and service calls | SOQL, DML, business logic itself |
| Domain (`<Object>Domain`, optional) | Per-record rules on the in-memory set: validation, defaulting, state-transition checks | SOQL, DML, callouts |
| Service (`<Object>Service`) | Orchestration: the business transaction, DML, callouts, chaining async work | Ad-hoc SOQL (asks the selector) |
| Selector (`<Object>Selector`) | ALL SOQL for its object — query methods only | DML, business logic |

- **One handler per trigger; one trigger per object.** The trigger body
  is a single delegating call — no `if`/`for`/field logic in the
  `.trigger` file.
- The Domain layer is where an object's own business rules live
  (e.g. "an Order can only move from Draft to Activated, never
  backward") — keep it independent of Handler/Service so those rules
  are testable without triggering full orchestration.
- A complete worked example (trigger + handler + domain + selector +
  service for one object) is in
  [reference/trigger-handler.cls](reference/trigger-handler.cls).

(id: `apex-layering`; source: Salesforce Well-Architected; Apex
Enterprise Patterns / fflib cited as inspiration only, never a
requirement — this standard)

## Bulkification

- **No SOQL or DML inside a loop** — collect the working set (`Set<Id>`,
  `List<SObject>`), query or write once outside the loop.
- Every trigger-path method assumes it may run against up to 200 records
  in one invocation — never code "the single-record case" and add bulk
  handling later.
- Before/after pairs and a governor-limit-aware chunking pattern are in
  [reference/bulkification.md](reference/bulkification.md).

(id: `apex-bulkification`; source: Apex Developer Guide — "Bulk Apex
Triggers"; PMD `OperationWithLimitsInLoop` — the current rule; older PMD
versions expose the same finding as the now-deprecated
`AvoidSoqlInLoops` / `AvoidDmlStatementsInLoops`)

## Governor limits

Design to these per-transaction budgets (Apex Developer Guide —
"Execution Governors and Limits"):

| Resource | Synchronous | Asynchronous |
|---|---|---|
| SOQL queries issued | 100 | 200 |
| Rows returned by SOQL | 50,000 | 50,000 |
| DML statements | 150 | 150 |
| Rows processed by DML | 10,000 | 10,000 |
| CPU time | 10,000 ms | 60,000 ms |
| Heap size | 6 MB | 12 MB |

- Use the `Limits` class (`Limits.getQueries()` /
  `Limits.getLimitQueries()`, `Limits.getDmlStatements()` /
  `Limits.getLimitDmlStatements()`, `Limits.getCpuTime()`,
  `Limits.getHeapSize()`, and their `getLimit*` counterparts) to check
  remaining budget before a step that might approach it — e.g. before
  deciding whether to process a chunk synchronously or hand it to a
  `Queueable`.
- A budget-aware pattern is the third pair in
  [reference/bulkification.md](reference/bulkification.md).

(id: `apex-governor-limits`; source: Apex Developer Guide — "Execution
Governors and Limits")

## Sharing in code

Every class explicitly declares its sharing keyword — never leave it
implicit:

- **`with sharing`** — the default for user-facing classes: service and
  handler layers.
- **`inherited sharing`** — the default for reusable, callable-from-
  anywhere layers (selectors, domain classes) that should run in
  whatever context called them rather than fix one.
- **`without sharing`** — only with a one-line comment stating why (e.g.
  a system-context integration process that must see across the org).
  An undeclared or unjustified `without sharing` is a review finding.

This section covers keyword mechanics only. **Access-model design** —
what the org-wide defaults, roles, and sharing rules actually grant —
belongs to `salesforce-security-model`.

(id: `apex-sharing`; source: Apex Developer Guide — "Using the
`with sharing` or `without sharing` Keywords"; PMD
`ApexSharingViolations`)

## Error handling

- **Custom exceptions per domain area** — `<Domain>Exception` (e.g.
  `OrderProcessingException`, `IntegrationException`), extending
  `Exception`. Catch specific exceptions before generic ones; never
  catch bare `Exception` and discard it.
- **No empty or silently-swallowed catch blocks.** A catch either
  recovers, rethrows (optionally wrapped in a domain exception), or logs
  and rethrows — it never just returns or does nothing.
- **Logging is a central abstraction, not `System.debug`.** `System.debug`
  is a development-time tool only — it is not durable, not queryable in
  production, and does not survive a transaction rollback. Route errors
  (especially integration/callout failures) through one logging
  abstraction that supports levels (error/warn/info) and persists
  integration errors past a rollback (e.g. via a platform event, since
  those commit independently of the triggering transaction's outcome).
  No specific logging library is mandated — Nebula Logger is a
  reasonable off-the-shelf implementation of this pattern, cited as an
  example, not a requirement.

(id: `apex-error-handling`; source: PMD `EmptyCatchBlock`,
`DebugsShouldUseLoggingLevel`; the central-logger-abstraction and
`System.debug`-is-dev-only stances are this standard)

## Review severities

- **Critical**: SOQL/DML in a loop reachable from a trigger path
  (`apex-bulkification`); a class doing SOQL/DML without a sharing
  declaration (`apex-sharing`, PMD `ApexSharingViolations`); an empty or
  swallowed catch block (`apex-error-handling`).
- **Important**: logic or SOQL placed outside its owning layer
  (`apex-layering`); a generic `Exception` catch/throw instead of a
  domain exception; an undocumented `without sharing`.
- **Minor**: naming convention deviations (`apex-naming`); `System.debug`
  used as the only error-reporting mechanism in a non-trivial catch.
