---
name: salesforce-apex-testing
description: Use when writing or reviewing Apex unit tests — test-class structure, TestDataFactory, assertions, mocking, Test.startTest/stopTest, and test data without SeeAllData. Apex-only; LWC jest tests belong to salesforce-lwc.
---

# Salesforce Apex Testing

Standards for Apex test classes: structure, test data, assertions,
mocking, and coverage. Cite rules in review findings as
`(standard: salesforce-apex-testing, rule: <id>)`; each rule names its
source — the Apex Developer Guide, or `this standard` (a recorded house
decision). Layering (handler/domain/service/selector) is
`salesforce-apex`'s concern, not restated here — a test exercises those
layers, it does not redefine them. LWC jest tests are out of scope —
see `salesforce-lwc`.

## Test-class structure

- **Naming**: `<Class>Test` for the class under test (e.g.
  `OrderServiceTest` for `OrderService`).
- **`@TestSetup`**: a single `static void` method building the data
  shared by every test method in the class, via `TestDataFactory`. It
  runs once per test method in its own transaction — same rolled-back
  snapshot each time, isolation per-method, setup cost paid once.
- **One behavior per test method.** A method name states the scenario
  and the expectation (e.g.
  `validateStatusTransitions_throwsWhenActivatingFromCancelled`) —
  not `testOrder1`. If a method needs "and" to describe what it checks,
  split it.
- **Arrange-Act-Assert**, in that order, inside every method — data
  setup, then the single action under test, then assertions. Comment
  the three sections in longer methods; keep the shape recognizable
  even when a method is short enough not to need the comments.
- A full worked class demonstrating all of the above is
  [reference/test-patterns.cls](reference/test-patterns.cls).

(id: `apex-test-structure`; severity: minor; source: Apex Developer
Guide — "Testing Apex Code"; the naming/AAA conventions are this
standard)

## TestDataFactory — the single source of test records

**One `TestDataFactory` class, per-object static methods, each with
sensible defaults and override parameters.** No test method builds an
`SObject` inline with `new Account(...)` — every record a test needs
comes from a `TestDataFactory` method, so a schema change is fixed in
one place instead of in every test file.

- Each builder takes a record count and returns the concrete SObject
  list type — `List<Account>`, `List<Order>` — not a generic
  `List<SObject>`: `createAccounts(Integer count)`.
- An overload accepts a `Map<String, Object>` of field overrides applied
  on top of the defaults:
  `createAccounts(Integer count, Map<String, Object> fieldOverrides)`.
- The factory inserts the records and returns them — a test method
  never calls `insert` on a factory-built list itself.
- A complete factory with two object builders (`Account`, `Order`) is
  [reference/TestDataFactory.cls](reference/TestDataFactory.cls).

(id: `apex-test-data-factory`; severity: important; source: this
standard)

## Assertions

**The `Assert` class** (`Assert.areEqual`, `Assert.areNotEqual`,
`Assert.isTrue`, `Assert.isFalse`, `Assert.fail`) — `System.assert*` is
legacy-only: keep it where it already exists in code you are not
otherwise touching, never write it in new tests.

- **Always pass a failure message** as the last argument — it tells you
  *why* a test failed without reopening the method.
- **Assert the actual behavior, not just "no exception was thrown."**
  A test that calls the method under test and stops passes even if the
  method silently did nothing. Assert the resulting state: the field
  value that changed, the record count created, the exception type and
  message for a failure path.

(id: `apex-test-assertions`; severity: important; source: this
standard — `System.assert*` is documented by Salesforce as legacy,
superseded by the `Assert` class)

Sub-rules:
- a test asserting only "no exception", with no check on the
  resulting state (id: `apex-test-assertions.no-state-check`;
  severity: critical; kind: hardening)
- legacy `System.assert*` instead of `Assert` in a new test (id:
  `apex-test-assertions.legacy-assert`; severity: minor)

## Mocking

- **`Test.setMock(HttpCalloutMock.class, ...)` for every callout, with
  no exceptions.** A test never makes a real HTTP callout.
- **The Stub API (`System.StubProvider`, `Test.createStub`)** for unit
  isolation where the code under test already takes its dependency
  through dependency injection (a constructor or setter parameter, e.g.
  a service that accepts a selector instance rather than instantiating
  one itself). Where no injection point exists, do not restructure
  production code purely to make it stubbable for one test — that
  restructuring is a `salesforce-apex` layering decision on its own
  merits, not a testing shortcut.
- **No mocking framework is mandated.** `HttpCalloutMock` and
  `StubProvider` are platform-native and sufficient; do not add a
  third-party mocking library to reach for.
- A callout test using `Test.setMock` is in
  [reference/test-patterns.cls](reference/test-patterns.cls).

(id: `apex-test-mocking`; severity: important; source: Apex Developer
Guide — "Test Classes for Behavior Verification with Mock Objects" and
"HTTP Callout Testing"; the DI-only Stub API stance and
no-mocking-framework stance are this standard)

Sub-rules:
- a real HTTP callout reachable from a test run instead of
  `Test.setMock` (id: `apex-test-mocking.real-callout`; severity:
  critical; kind: defect)

## Test.startTest / Test.stopTest

Wrap **only the action under test** — never the `TestDataFactory` setup
calls — in `Test.startTest()` / `Test.stopTest()`:

- Everything inside the block runs with a **fresh set of governor
  limits**, separate from setup.
- `Test.stopTest()` **runs queued asynchronous work (`@future`,
  `Queueable`, `Batchable`) synchronously** before returning — assert
  async effects only after `stopTest()`, not before.

(id: `apex-test-start-stop`; severity: important; source: Apex
Developer Guide — "Using the Test.startTest and Test.stopTest
Methods")

## No `SeeAllData`

**`@IsTest(SeeAllData=true)` is banned.** Every test creates the data it
needs through `TestDataFactory` and runs correctly in an org with none
of your organization's actual records — no reliance on an existing
Account, a picklist value already present, or any other ambient data.

(id: `apex-test-no-see-all-data`; severity: critical; kind: hardening;
source: Apex Developer Guide — "Data Access and Test Visibility"; this
standard bans the escape hatch entirely rather than scoping when it is
acceptable)

## Coverage is a floor, not a target

- The platform enforces **75%** organization-wide as a deploy minimum —
  this project's floor is **85%**, above that minimum.
- The floor is a gate, not a goal: a suite that hits 85% by asserting
  real behavior is worth more than one that hits 95% by executing code
  paths without checking what they did. When choosing where to spend
  effort, write the assertion that would catch a real regression before
  chasing the last few percentage points on an already-exercised class.
- Coverage percentage never substitutes for a code-review reading of
  what a test actually asserts — see "Assertions" above.

(id: `apex-test-coverage`; severity: important; source: Salesforce
platform deploy minimum (75%); the 85% floor and the
meaningful-assertions-outrank-percentage stance are this standard)
