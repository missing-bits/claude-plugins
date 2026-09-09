# Metadata-driven trigger framework

Framework id `metadata-driven`. The reference implementation is
`mitchspano/apex-trigger-actions-framework`. One trigger per object
calls `new MetadataTriggerHandler().run()`, and Custom Metadata records
name the classes to run and their order — one
`sObject_Trigger_Setting__mdt` record per object, one
`Trigger_Action__mdt` record per action and context. An action is any
class implementing one of the `TriggerAction.*` interfaces; changing
the order is a metadata deployment, not a code one. Every rule here is
cited
`(standard: salesforce-triggers, rule: trigger-metadata-driven-<suffix>)`.

## Dispatch

### `OrderTrigger.trigger`

```apex
trigger OrderTrigger on Order (before insert, before update, after update) {
    new MetadataTriggerHandler().run();
}
```

### `OrderTriggerHandler.cls`

One class carrying the object's three actions, each an interface
method the framework calls with `List<SObject>` arguments. It routes to
the domain and service layers of `salesforce-apex`'s
`reference/order-layers.md`; no SOQL, no DML, no business logic of its
own. `with sharing`, the default for the handler layer.

```apex
public with sharing class OrderTriggerHandler implements TriggerAction.BeforeInsert, TriggerAction.BeforeUpdate, TriggerAction.AfterUpdate {

    public void beforeInsert(List<SObject> triggerNew) {
        OrderDomain.applyDefaults((List<Order>) triggerNew);
    }

    public void beforeUpdate(List<SObject> triggerNew, List<SObject> triggerOld) {
        Map<Id, Order> oldMap = new Map<Id, Order>((List<Order>) triggerOld);
        OrderDomain.validateStatusTransitions((List<Order>) triggerNew, oldMap);
    }

    public void afterUpdate(List<SObject> triggerNew, List<SObject> triggerOld) {
        Map<Id, Order> oldMap = new Map<Id, Order>((List<Order>) triggerOld);
        List<Order> activated = OrderDomain.filterNewlyActivated((List<Order>) triggerNew, oldMap);
        if (!activated.isEmpty()) {
            OrderService.activateFulfillment(activated);
        }
    }
}
```

### The metadata

Nothing in code names the class; the records do. One
`sObject_Trigger_Setting__mdt` record and three `Trigger_Action__mdt`
records deploy with the code:

| Record | Type | Key fields |
|---|---|---|
| `Order` | `sObject_Trigger_Setting__mdt` | `Object_API_Name__c = Order` |
| `Order_Before_Insert` | `Trigger_Action__mdt` | `Apex_Class_Name__c = OrderTriggerHandler`, `Before_Insert__c = Order`, `Order__c = 1` |
| `Order_Before_Update` | `Trigger_Action__mdt` | `Apex_Class_Name__c = OrderTriggerHandler`, `Before_Update__c = Order`, `Order__c = 1` |
| `Order_After_Update` | `Trigger_Action__mdt` | `Apex_Class_Name__c = OrderTriggerHandler`, `After_Update__c = Order`, `Order__c = 1` |

Each context field (`Before_Insert__c`, `Before_Update__c`,
`After_Insert__c`, `After_Update__c`, `Before_Delete__c`,
`After_Delete__c`, `After_Undelete__c`) is a lookup to the object's
setting record; a record enables exactly the contexts it fills.

### Signature

```
Signature:
  header: TriggerAction.
Framework types: TriggerBase, MetadataTriggerHandler, TriggerAction, TriggerActionFlow, FinalizerHandler
```

The pattern is `TriggerAction.` rather than `implements TriggerAction.`
on purpose: a class declared `implements Queueable,
TriggerAction.BeforeInsert` names the framework interface second, and a
header test is a substring match. Any header naming a `TriggerAction.*`
interface, wherever it sits in the `implements` list, selects the
class. Two framework classes match it themselves —
`MetadataTriggerHandler` and `TriggerActionFlow`, each implementing all
seven context interfaces — and both sit under `Framework types:`, which
removes them from the handler set; `TriggerActionFlowChangeEvent
extends TriggerActionFlow` is then a closure candidate whose parent is
not in the set, and stays out too. The framework types appear in the
repository only where the framework arrives as source; listing them
costs nothing where it does not.

## Context access

The framework reads `Trigger.*` in `TriggerBase.run()` and hands each
action `triggerNew` and `triggerOld` as `List<SObject>`. An action
reads nothing from `Trigger.*`; it casts the lists and, where it needs
the old records by id, builds `new Map<Id, Order>((List<Order>)
triggerOld)` — the framework passes no map.

## Bypass and recursion

| Call | Effect |
|---|---|
| `TriggerBase.bypass('Order')`, `clearBypass`, `isBypassed` | every action on the object; `Schema.SObjectType` overloads exist |
| `TriggerBase.clearAllBypasses()` | clears every object bypass |
| `MetadataTriggerHandler.bypass('OrderTriggerHandler')`, `clearBypass`, `isBypassed` | one action, by class name or `System.Type` |
| `MetadataTriggerHandler.clearAllBypasses()` | clears every action bypass |
| `Bypass_Execution__c` on either record type | disables the object or the action without a deployment of code |
| `Bypass_Permission__c`, `Required_Permission__c` | a custom permission whose holders skip the action, or without which it does not run |

**Recursion.** No loop count exists here. The framework counts how
often each record id has been seen in the update contexts —
`TriggerBase.idToNumberOfTimesSeenBeforeUpdate` and
`TriggerBase.idToNumberOfTimesSeenAfterUpdate`, both
`Map<Id, Integer>` — and leaves the decision to the action: one that
must act once checks that the count for the record is 1. What happens
when a limit is exceeded: nothing is exceeded. An action ignoring the
maps re-enters until a governor limit throws `System.LimitException`
and the transaction fails.

**A stale record fails the object.** `MetadataTriggerHandler`
instantiates each action with `Type.forName(Apex_Class_Name__c)`; a
name resolving to no class, or to a class not implementing the
context's interface, throws `MetadataTriggerHandlerException` — and
every DML on that object fails until the record is fixed.

## Test isolation

An action is a plain class: instantiate it and call the interface
method with records built in memory, no DML and no metadata read:

```apex
List<Order> orders = new List<Order>{ new Order(Status = null) };
new OrderTriggerHandler().beforeInsert(orders);
Assert.areEqual('Draft', orders[0].Status);
```

To disable the handler in a test of other code that inserts orders,
call `MetadataTriggerHandler.bypass('OrderTriggerHandler')` before the
DML and `clearBypass` in a `finally` block; `TriggerBase.bypass('Order')`
silences every action on the object the same way.

## Fingerprint

`new MetadataTriggerHandler().run()` in a trigger body together with
`Trigger_Action__mdt` and `sObject_Trigger_Setting__mdt` records in the
repository — an optional `ns.` before the class and `ns__` before the
metadata API names. The row keys on records and the trigger body, never
on the framework's classes: the records sit in the repository whether
the framework arrives as an unlocked package or as source, while the
classes appear only in the second case.

## Inner classes

`Type.forName('Outer.Inner')` resolves, so an inner class can be
registered as an action. The signature grammar selects top-level types
only; an inner-class action is therefore not graded by the rules below,
and this document says so rather than leaving it to a reader. The
convention here is a top-level class per action or per object.

## Rules

**Dispatching class.** A class carrying an object's actions is named
`<Object>TriggerHandler`; where actions split by feature, each is
`<Object><Feature>Action`. Pre-existing non-conforming names stay; the
convention binds new code.

(id: `trigger-metadata-driven-dispatching-class`; severity: minor;
source: this standard)

**Every action is registered, and every record resolves.** Each
`Trigger_Action__mdt` record's `Apex_Class_Name__c` names a class in
the repository implementing the interface of every context the record
enables, and every class implementing one of the seven context
interfaces — `BeforeInsert` through `AfterUndelete` — has a record. A
stale name fails every DML on the object at runtime; an unregistered
action never runs. A `TriggerAction.DmlFinalizer` implementer is
selected as a handler by the signature but registered through a
different record type, so this rule leaves it alone.

(id: `trigger-metadata-driven-action-registered`; severity: important;
source: this standard)

**A bypass is restored.** In non-test code every `TriggerBase.bypass`
or `MetadataTriggerHandler.bypass` is paired with the matching
`clearBypass` in a `finally` block. A bypass left set silences
automation for every caller later in the same transaction.

(id: `trigger-metadata-driven-bypass-restored`; severity: important;
source: this standard)

**Order is explicit.** Every `Trigger_Action__mdt` record carries an
`Order__c` value, unique among the records enabling the same object and
context. Two actions on one order leave their sequence to the query.

(id: `trigger-metadata-driven-order-explicit`; severity: minor; source:
this standard)

## Gotchas

- `triggerOld` is a `List<SObject>`, not a map; build the map in the
  action.
- The Custom Metadata type and its records deploy together with the
  framework; a record naming a class that is not yet deployed fails the
  object's DML from the first save.
- Flow actions (`Flow_Name__c`) run through the same records and are
  outside this document.
