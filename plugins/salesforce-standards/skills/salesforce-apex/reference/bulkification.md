# Bulkification — before/after pairs

One pair per rule in SKILL.md's "Bulkification" and "Governor limits"
sections. All examples use the `Order` / `Task` objects from
[trigger-handler.cls](trigger-handler.cls).

## apex-bulkification: SOQL in a loop → collection-driven query

```apex
// Before — one SOQL query per order; 200 orders = 200 queries,
// blowing past the 100-query synchronous limit.
for (Order o : triggerNewOrders) {
    Account acc = [SELECT Id, Name FROM Account WHERE Id = :o.AccountId];
    // ... use acc ...
}

// After — collect the working set, query once.
Set<Id> accountIds = new Set<Id>();
for (Order o : triggerNewOrders) {
    accountIds.add(o.AccountId);
}
Map<Id, Account> accountsById = new Map<Id, Account>(
    [SELECT Id, Name FROM Account WHERE Id IN :accountIds]
);
for (Order o : triggerNewOrders) {
    Account acc = accountsById.get(o.AccountId);
    // ... use acc ...
}
```

(PMD `OperationWithLimitsInLoop` / the deprecated `AvoidSoqlInLoops`
flags the "before" shape directly.)

## apex-bulkification: DML in a loop → collected DML

```apex
// Before — one insert per order; 200 orders = 200 DML statements,
// well past the 150-statement limit, and each is its own round trip.
for (Order o : activatedOrders) {
    Task t = new Task(Subject = 'Fulfill order ' + o.OrderNumber, WhatId = o.Id);
    insert t;
}

// After — build the full list, one DML statement for the whole batch.
List<Task> fulfillmentTasks = new List<Task>();
for (Order o : activatedOrders) {
    fulfillmentTasks.add(new Task(
        Subject = 'Fulfill order ' + o.OrderNumber,
        WhatId = o.Id
    ));
}
insert fulfillmentTasks;
```

(PMD `OperationWithLimitsInLoop` / the deprecated
`AvoidDmlStatementsInLoops` flags the "before" shape directly.)

## apex-governor-limits: budget-aware chunking

A batch/queueable step whose per-record work can itself issue SOQL or
DML needs to check its remaining budget before continuing, rather than
assuming the whole set always fits.

```apex
// Before — assumes the full scope always fits in one transaction;
// fails the whole batch once a large-enough scope hits a limit.
public void processScope(List<Order> scope) {
    for (Order o : scope) {
        reconcileWithExternalSystem(o); // may itself issue SOQL/DML
    }
}

// After — checks remaining budget per iteration; hands the remainder
// to a Queueable instead of running the batch off the edge of its limits.
public void processScope(List<Order> scope) {
    for (Integer i = 0; i < scope.size(); i++) {
        Boolean nearQueryBudget =
            Limits.getQueries() >= Limits.getLimitQueries() - 5;
        Boolean nearDmlBudget =
            Limits.getDmlStatements() >= Limits.getLimitDmlStatements() - 5;
        if (nearQueryBudget || nearDmlBudget) {
            List<Order> remainder = new List<Order>();
            for (Integer j = i; j < scope.size(); j++) {
                remainder.add(scope[j]);
            }
            System.enqueueJob(new OrderReconciliationQueueable(remainder));
            return;
        }
        reconcileWithExternalSystem(scope[i]);
    }
}
```

(id: `apex-governor-limits`; source: Apex Developer Guide — "Execution
Governors and Limits"; the `Limits`-class check pattern is this
standard)
