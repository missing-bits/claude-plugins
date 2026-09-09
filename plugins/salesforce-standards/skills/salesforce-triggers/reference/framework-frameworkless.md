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
Assert.areEqual('Draft', orders[0].Status);
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
- The entry point is written `handle(System.TriggerOperation …)`
  verbatim. The signature is a substring test, so
  `handle(TriggerOperation …)` — identical to the compiler — matches no
  signature and leaves the class unselected.
- The shape this plugin shipped before `salesforce-triggers` existed —
  static `handleBeforeInsert` methods and a trigger branching on
  `Trigger.isBefore` — now earns two findings on the trigger,
  `trigger-body-delegates` and, once the project resolves as
  `frameworkless`, `trigger-frameworkless-entry-point`, and its handler
  matches no signature. One fix clears all three: keep the methods, add
  one `handle` entry point that switches on the operation and calls
  them, and make the trigger call it.
