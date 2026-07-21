# Flow patterns — structural descriptions

Flows are authored in Flow Builder, not in a text file, so the patterns
below are described by element name and connection rather than shown as
copy-pasteable source. Build each one on the canvas using the shapes and
settings described.

## 1. Bulk-safe record-triggered flow structure

Scenario: `Account_AfterSave_SyncBilling` — when an Account's billing
address changes, push the update to every related, still-open
Opportunity so its billing snapshot stays in sync. Demonstrates: a
filtered entry, a Get outside any loop, a loop that only builds a
collection, and one collection-based Update Records call.

| Element | Type | What it does |
|---|---|---|
| **Start** | Object: `Account`, Trigger: "A record is updated", Entry Conditions: `BillingCity`, `BillingState`, `BillingPostalCode`, or `BillingCountry` changed (formula condition using `ISCHANGED()` per field), "Only when a record is updated to meet the condition requirements" = **On** | Keeps the interview from even starting for saves that don't touch billing fields |
| **Get_Open_Related_Opportunities** | Get Records | Queries `Opportunity` where `AccountId` = `{!$Record.Id}` AND `IsClosed` = false, stored into collection variable `colOpenOpportunities` — run once, outside any loop |
| **Loop_Open_Opportunities** | Loop | Iterates `colOpenOpportunities` into loop variable `loopOpportunity` |
| **Assignment_Stage_Billing_Update** | Assignment (inside the loop) | Copies the Account's new billing fields onto `loopOpportunity`'s billing snapshot fields, then **Add**s `loopOpportunity` to collection variable `colOpportunitiesToUpdate` — no Get, Update, or Delete element lives inside this loop, only this Assignment |
| **Update_Opportunities_Billing_Snapshot** | Update Records (after the loop, outside it) | Updates `colOpportunitiesToUpdate` in a single collection-based DML call | 
| **Fault path** | from `Update_Opportunities_Billing_Snapshot` | See pattern 2 below |
| **End** | End | Reached only from the Update element's default (success) path |

The rule this demonstrates: every element capable of Get/Update/Delete
sits **outside** `Loop_Open_Opportunities`; the only thing that happens
**inside** the loop is building the collection that the single
after-the-loop Update element consumes.

## 2. Fault-path pattern

Every DML or callout element connects **two** paths out: its default
(success) path and its fault path. The fault path never dead-ends —
it always reaches a named handling behavior before the interview ends.

Shared fault-handling branch, reusable by any DML/callout element in a
system-context flow:

| Element | Type | What it does |
|---|---|---|
| **Update_Opportunities_Billing_Snapshot** (or any DML/callout element) | Create/Update/Delete Records, Action | Its **Fault** connector (not the default connector) leads to the next element below |
| **Assignment_Build_Error_Details** | Assignment | Populates `varErrorMessage` from `{!$Flow.FaultMessage}` plus context (flow name, triggering record Id) |
| **Create_Flow_Error_Log** | Create Records | Creates one `Flow_Error_Log__c` record (or equivalent error-tracking object) carrying `varErrorMessage`, the flow's name, and the triggering record's Id — this is what makes the failure queryable after the fact, since a record-triggered flow has no user watching for a toast |
| **Send_Error_Alert_Email** | Action (Send Email Alert) | Notifies the owning team's queue/distribution list when the failure needs prompt human attention — omit only for genuinely low-stakes automation where the error log alone is a sufficient response |
| **End** | End | Reached from the fault branch, distinct from the success-path End |

Every DML/callout element in a flow connects its fault path into this
same branch (or an equivalent one) rather than each element inventing
its own handling — one shared, named fault branch per flow is easier to
audit than a scatter of ad-hoc ones.

## 3. Entry-conditions example

Scenario: `Case_BeforeSave_Defaults` — apply default field values to a
new Case before it saves, without re-running on every subsequent edit.

| Element | Type | What it does |
|---|---|---|
| **Start** | Object: `Case`, Trigger: "A record is created", Entry Conditions: none required beyond record creation — a before-save "on create" flow already runs exactly once per new record, so no additional filter is needed here | Runs once, at creation, never on later updates |
| **Decision_Needs_Default_Priority** | Decision | Outcome "Priority Blank" when `{!$Record.Priority}` is null; default outcome does nothing |
| **Assignment_Set_Default_Priority** | Assignment (off the "Priority Blank" outcome) | Sets `{!$Record.Priority}` = `"Medium"` directly on the triggering record — a before-save flow assigns fields on `$Record` itself instead of issuing an Update Records element, since the save that's already in flight commits the change with no extra DML |
| **End** | End | Both the "Priority Blank" and default outcomes reach it |

Contrast with an **after-save** entry-conditions case (as in pattern 1):
because an after-save flow re-evaluates on every subsequent update too,
its Start element's Entry Conditions plus "Only when a record is updated
to meet the condition requirements" are what keep it from re-running
its full interview — including the Get and loop — on saves that never
touched the fields it cares about.
