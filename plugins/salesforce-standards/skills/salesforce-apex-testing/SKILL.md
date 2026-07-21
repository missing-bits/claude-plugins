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
  runs once per test method in its own transaction (each test method
  starts from the same rolled-back snapshot), so setup cost is paid
  once even though isolation is per-method.
- **One behavior per test method.** A method name states the scenario
  and the expectation (e.g.
  `validateStatusTransitions_throwsWhenMovingBackwardFromActivated`) —
  not `testOrder1`. If a method needs "and" to describe what it checks,
  split it.
- **Arrange-Act-Assert**, in that order, inside every method — data
  setup, then the single action under test, then assertions. Comment
  the three sections in longer methods; keep the shape recognizable
  even when a method is short enough not to need the comments.
- A full worked class demonstrating all of the above is
  [reference/test-patterns.cls](reference/test-patterns.cls).

(id: `apex-test-structure`; source: Apex Developer Guide — "Testing
Apex Code"; the naming/AAA conventions are this standard)

## TestDataFactory — the single source of test records

**One `TestDataFactory` class, per-object static methods, each with
sensible defaults and override parameters.** No test method builds an
`SObject` inline with `new Account(...)` — every record a test needs
comes from a `TestDataFactory` method, so a schema change (a new
required field, a renamed picklist value) is fixed in one place instead
of in every test file that happens to construct that object.

- Each builder takes a record count and returns a `List<SObject>`:
  `createAccounts(Integer count)`.
- An overload accepts a `Map<String, Object>` of field overrides applied
  on top of the defaults, so a test that needs one specific field value
  doesn't get its own bespoke builder:
  `createAccounts(Integer count, Map<String, Object> fieldOverrides)`.
- The factory inserts the records and returns them — a test method
  never calls `insert` on a factory-built list itself.
- A complete factory with two object builders (`Account`, `Order`) is
  [reference/TestDataFactory.cls](reference/TestDataFactory.cls).

(id: `apex-test-data-factory`; source: this standard)

## Assertions

**The `Assert` class** (`Assert.areEqual`, `Assert.areNotEqual`,
`Assert.isTrue`, `Assert.isFalse`, `Assert.fail`) — `System.assert*` is
legacy-only: keep it where it already exists in code you are not
otherwise touching, never write it in new tests.

- **Always pass a failure message** as the last argument. A bare
  `Assert.areEqual(expected, actual)` tells you a test failed; the
  message is what tells you *why* without reopening the test method.
- **Assert the actual behavior, not just "no exception was thrown."**
  A test that calls the method under test and stops is not a test — it
  passes even if the method silently did nothing. Assert the resulting
  state: the field value that changed, the record count that was
  created, the exception type and message for a failure path.

(id: `apex-test-assertions`; source: this standard — `System.assert*`
is documented by Salesforce as legacy, superseded by the `Assert`
class)

## Mocking

- **`Test.setMock(HttpCalloutMock.class, ...)` for every callout, with
  no exceptions.** A test never makes a real HTTP callout — no test
  should depend on an external system being up, fast, or returning the
  same thing twice.
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

(id: `apex-test-mocking`; source: Apex Developer Guide — "Test
Classes for Behavior Verification with Mock Objects" and "HTTP Callout
Testing"; the DI-only Stub API stance and no-mocking-framework stance
are this standard)

## Test.startTest / Test.stopTest

Wrap **only the action under test** — never the `TestDataFactory` setup
calls — in `Test.startTest()` / `Test.stopTest()`:

- Everything inside the block runs with a **fresh set of governor
  limits**, separate from setup — a test that built 200 records before
  `startTest()` doesn't have those queries or DML statements counted
  against the limits the action under test actually needs to stay
  within.
- `Test.stopTest()` **runs queued asynchronous work (`@future`,
  `Queueable`, `Batchable`) synchronously** before returning — an
  action that enqueues async work needs its effects asserted only after
  `stopTest()`, not before.

(id: `apex-test-start-stop`; source: Apex Developer Guide — "Using the
Test.startTest and Test.stopTest Methods")

## No `SeeAllData`

**`@IsTest(SeeAllData=true)` is banned.** Every test creates the data it
needs through `TestDataFactory` and runs correctly in an org that has
none of your organization's actual records — no reliance on a specific
existing Account, a particular picklist value already present in the
org, or any other ambient data. A test that only passes because of data
that happens to exist in one particular sandbox is not a repeatable
test.

(id: `apex-test-no-see-all-data`; source: Apex Developer Guide —
"Data Access and Test Visibility"; this standard bans the escape hatch
entirely rather than scoping when it is acceptable)

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

(id: `apex-test-coverage`; source: Salesforce platform deploy minimum
(75%); the 85% floor and the meaningful-assertions-outrank-percentage
stance are this standard)

## Review severities

- **Critical**: `@IsTest(SeeAllData=true)` anywhere
  (`apex-test-no-see-all-data`); a real HTTP callout reachable from a
  test run instead of `Test.setMock` (`apex-test-mocking`); a test
  asserting only "no exception" with no check on the resulting state
  (`apex-test-assertions`).
- **Important**: inline `SObject` construction in a test method instead
  of `TestDataFactory` (`apex-test-data-factory`); `Assert`/`System.assert*`
  calls with no failure message (`apex-test-assertions`); setup code
  placed inside `Test.startTest`/`stopTest` (`apex-test-start-stop`).
- **Minor**: a test method naming deviation that obscures the scenario
  under test (`apex-test-structure`); `System.assert*` used in a new
  test instead of `Assert` (`apex-test-assertions`).
