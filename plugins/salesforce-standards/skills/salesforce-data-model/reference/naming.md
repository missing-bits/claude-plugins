# Data model naming — worked examples

The settled convention from `SKILL.md`'s naming section, applied across
objects, every field type, record types, and validation rules. One rule
throughout: PascalCase words separated by underscores, no abbreviations,
`__c` suffix on every custom object and custom field API name.

## Objects

| Label | API name | Notes |
|---|---|---|
| `Service Contract` | `Service_Contract__c` | Two-word business term, both words kept in full |
| `Billing Adjustment` | `Billing_Adjustment__c` | Not `Bill_Adj__c` — no abbreviations |
| `Renewal Opportunity Line` | `Renewal_Opportunity_Line__c` | Three words, still fully spelled out |

## Fields, by type

| Field type | Label | API name | Notes |
|---|---|---|---|
| Text | `Shipping Reference` | `Shipping_Reference__c` | Plain business-term field |
| Number | `Unit Count` | `Unit_Count__c` | Not `Qty__c` |
| Currency | `Total Amount` | `Total_Amount__c` | The canonical settled example |
| Date | `Contract Start Date` | `Contract_Start_Date__c` | Redundant-looking but explicit — "Date" stays in both label and API name |
| Date/Time | `Last Sync Timestamp` | `Last_Sync_Timestamp__c` | "Timestamp" spelled in full, not `Ts__c` |
| Checkbox (Boolean) | `Is Active` | `Is_Active__c` | Reads as an assertion — see the `Has_`/`Is_` guidance in `SKILL.md` |
| Checkbox (Boolean) | `Has Signed Contract` | `Has_Signed_Contract__c` | Same pattern, `Has_` for possession/completion |
| Picklist | `Billing Sync Status` | `Billing_Sync_Status__c` | The canonical settled example |
| Formula | `Total With Tax` | `Total_With_Tax__c` | Named for what it computes, same convention as any other field — no special formula-field suffix invented |
| Lookup | `Primary Contact` | `Primary_Contact__c` | Relationship name derived automatically from the API name, no abbreviation in the base name |
| Master-Detail | `Parent Service Contract` | `Parent_Service_Contract__c` | Same convention; master-detail vs lookup is a relationship-type choice, not a naming one |

## Record types

| Label | API name | On object | When chosen (vs a picklist) |
|---|---|---|---|
| `Enterprise Account` | `Enterprise_Account` | `Account` | Enterprise accounts get a distinct page layout (additional fields: `Account_Tier__c`, `Dedicated_CSM__c`) and a distinct sharing rule criterion — structural difference, not just a value |
| `Renewal Opportunity` | `Renewal_Opportunity` | `Opportunity` | Renewal deals run a different approval process and expose a `Prior_Contract__c` lookup that new-business deals never see |

Contrast: a `Status__c` picklist (`Draft` / `Active` / `Closed`) on
either object stays a plain picklist, not three record types, because
every status shares the same layout, the same required fields, and the
same process — see `SKILL.md`'s record-type-vs-picklist guidance for the
structure-vs-value test.

## Validation rules

| Rule name | On object | What it checks |
|---|---|---|
| `Close_Date_Not_Past` | `Opportunity` | `CloseDate` is not before `TODAY()` on a new or edited open Opportunity |
| `Amount_Required_When_Won` | `Opportunity` | `Amount` is populated whenever `StageName` = `Closed Won` |
| `Contract_Start_Before_End` | `Service_Contract__c` | `Contract_Start_Date__c` is before `Contract_End_Date__c` |

Never `VR01_...`, `Validation_1`, or any numbered prefix — see
`SKILL.md`'s validation-rules section for why a number tells the next
reader nothing about what the rule enforces.
