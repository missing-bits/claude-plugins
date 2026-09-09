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

The base class reads `Trigger.isExecuting` and the context flags in
`run()` to pick the context method — `Trigger.operationType` in the
fork, `Trigger.isBefore`, `Trigger.isInsert` and their siblings in the
original — which is why it is a framework type. The handler reads `Trigger.new` and `Trigger.oldMap` once, in its
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
| fork | `incrementCheckLoopCount()` | returns without running the handler; the `throw` sits commented out inside that method, and the `System.debug` line fires only with `showDebug` on — by default nothing is logged |

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
