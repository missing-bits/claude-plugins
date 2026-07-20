# Trigger + handler + domain + selector + service — worked example

One object (standard `Order`), six compilation units, one fenced block
each — each block is valid, copy-pasteable Apex for the file named
above it. In a real org each block is its own `.trigger`/`.cls` file
(a `.cls` file holds exactly one top-level type).

Scenario: when an Order's `Status` field moves to "Activated", create
one fulfillment `Task` per order. The example demonstrates: one
delegating trigger, a handler that routes but never queries or writes,
a domain class that owns the record-level status-transition rule, a
selector that owns all SOQL for `Order`, and a service that owns the
DML transaction — all bulk-safe, all with an explicit sharing
declaration, errors routed through a custom exception and a logger
abstraction rather than swallowed or left as bare `System.debug` calls.

## `OrderTrigger.trigger`

A single delegating call per trigger context — no conditional or field
logic in the trigger body itself.

```apex
trigger OrderTrigger on Order (before insert, before update, after update) {
    if (Trigger.isBefore) {
        if (Trigger.isInsert) {
            OrderTriggerHandler.handleBeforeInsert(Trigger.new);
        }
        if (Trigger.isUpdate) {
            OrderTriggerHandler.handleBeforeUpdate(Trigger.new, Trigger.oldMap);
        }
    }
    if (Trigger.isAfter && Trigger.isUpdate) {
        OrderTriggerHandler.handleAfterUpdate(Trigger.new, Trigger.oldMap);
    }
}
```

## `OrderTriggerHandler.cls`

Routes trigger events to Domain and Service; no SOQL, no DML, no
business logic of its own. `with sharing` — the default for the
handler layer.

```apex
public with sharing class OrderTriggerHandler {

    public static void handleBeforeInsert(List<Order> newOrders) {
        OrderDomain.applyDefaults(newOrders);
    }

    public static void handleBeforeUpdate(List<Order> newOrders, Map<Id, Order> oldMap) {
        OrderDomain.validateStatusTransitions(newOrders, oldMap);
    }

    public static void handleAfterUpdate(List<Order> newOrders, Map<Id, Order> oldMap) {
        List<Order> activated = OrderDomain.filterNewlyActivated(newOrders, oldMap);
        if (!activated.isEmpty()) {
            OrderService.activateFulfillment(activated);
        }
    }
}
```

## `OrderDomain.cls`

Per-record business rules on the in-memory set only: validation,
defaulting, state-transition checks. No SOQL, no DML, no callouts —
testable without a full trigger context. `inherited sharing` — pure
logic, runs in whatever context called it.

```apex
public inherited sharing class OrderDomain {

    private static final Set<String> VALID_TRANSITIONS_TO_ACTIVATED = new Set<String>{ 'Draft' };

    public static void applyDefaults(List<Order> newOrders) {
        for (Order o : newOrders) {
            if (o.Status == null) {
                o.Status = 'Draft';
            }
        }
    }

    public static void validateStatusTransitions(List<Order> newOrders, Map<Id, Order> oldMap) {
        for (Order o : newOrders) {
            Order old = oldMap.get(o.Id);
            Boolean statusChanged = o.Status != old.Status;
            Boolean movingToActivated = o.Status == 'Activated';
            Boolean fromValidState = VALID_TRANSITIONS_TO_ACTIVATED.contains(old.Status);
            if (statusChanged && movingToActivated && !fromValidState) {
                throw new OrderProcessingException(
                    'Order ' + o.Id + ' cannot move from ' + old.Status + ' to Activated.'
                );
            }
        }
    }

    public static List<Order> filterNewlyActivated(List<Order> newOrders, Map<Id, Order> oldMap) {
        List<Order> activated = new List<Order>();
        for (Order o : newOrders) {
            Order old = oldMap.get(o.Id);
            if (o.Status == 'Activated' && old.Status != 'Activated') {
                activated.add(o);
            }
        }
        return activated;
    }
}
```

## `OrderSelector.cls`

ALL SOQL for `Order` lives here. `select*By*` method naming.
`inherited sharing` — reusable from any caller.

```apex
public inherited sharing class OrderSelector {

    public List<Order> selectByIds(Set<Id> orderIds) {
        return [
            SELECT Id, OrderNumber, Status, AccountId
            FROM Order
            WHERE Id IN :orderIds
        ];
    }
}
```

## `OrderService.cls`

The business transaction: orchestrates the selector, builds the
bulk-safe DML, wraps failures in a domain exception, and reports
through the logger abstraction instead of swallowing or bare-debugging
them. `with sharing` — the default for the service layer, since this
is where DML happens.

```apex
public with sharing class OrderService {

    public static void activateFulfillment(List<Order> activatedOrders) {
        OrderSelector selector = new OrderSelector();
        Map<Id, Order> fullOrdersById = new Map<Id, Order>(
            selector.selectByIds(new Map<Id, Order>(activatedOrders).keySet())
        );

        // Collection-driven: build every Task first, one DML at the end —
        // never insert inside the loop. See reference/bulkification.md.
        List<Task> fulfillmentTasks = new List<Task>();
        for (Order o : fullOrdersById.values()) {
            fulfillmentTasks.add(new Task(
                Subject = 'Fulfill order ' + o.OrderNumber,
                WhatId = o.Id,
                Status = 'Not Started'
            ));
        }

        try {
            insert fulfillmentTasks;
        } catch (DmlException e) {
            // Logger abstraction — SKILL.md "Error handling": persist through
            // a central logger (e.g. a platform event), not System.debug.
            // AppLogger is illustrative; no specific library is mandated.
            AppLogger.error('OrderService.activateFulfillment', e);
            throw new OrderProcessingException(
                'Could not create fulfillment tasks for activated orders.', e
            );
        }
    }
}
```

## `OrderProcessingException.cls`

Custom exception, `<Domain>Exception`.

```apex
public class OrderProcessingException extends Exception {}
```
