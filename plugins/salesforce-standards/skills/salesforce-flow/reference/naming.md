# Flow naming — worked examples

The settled pattern, from `SKILL.md`'s Naming section, applied across
flow names, element names, and variable names.

## Flow names

| Flow | Type | Pattern | Why |
|---|---|---|---|
| `Account_AfterSave_SyncBilling` | Record-triggered, after-save | `<Object>_<TriggerMoment>_<Purpose>` | Object `Account`, moment `AfterSave`, purpose `SyncBilling` — syncs billing data to related records once the Account row has committed |
| `Case_BeforeSave_Defaults` | Record-triggered, before-save | `<Object>_<TriggerMoment>_<Purpose>` | Object `Case`, moment `BeforeSave`, purpose `Defaults` — applies default field values before the record commits, with no extra DML |
| `Onboarding_CollectConsents` | Screen flow | `<Domain>_<Purpose>` | Not record-triggered, so no object or trigger moment applies — `Onboarding` is the domain, `CollectConsents` the purpose |
| `Refund_RequestApproval` | Autolaunched flow (invoked from Apex/Screen Flow) | `<Domain>_<Purpose>` | Domain `Refund`, purpose `RequestApproval` — a reusable autolaunched flow, not tied to one object's trigger context |
| `Billing_CalculateProration` | Subflow | `<Domain>_<Purpose>` | Extracted because the proration math is reused by two parent flows — see the subflow decomposition stance in `SKILL.md` |

Trigger-moment tokens for record-triggered flows: `BeforeSave`,
`AfterSave`, `BeforeDelete` (there is no `AfterDelete` record-triggered
context — use a Platform Event or Apex trigger for after-delete needs).

## Element names

Verb-first, Title Case with underscored words — Flow Builder derives the
API name from the label automatically.

| Element | Type | Example name |
|---|---|---|
| Get Records | Query | `Get_Open_Related_Opportunities` |
| Decision | Branch | `Decision_Is_High_Priority` |
| Assignment | Build a collection | `Assignment_Build_Task_List` |
| Loop | Iterate a collection | `Loop_Open_Opportunities` |
| Update Records | DML | `Update_Opportunities_Billing_Snapshot` |
| Create Records | DML (error logging) | `Create_Flow_Error_Log` |
| Action | Callout/notification | `Send_Error_Alert_Email` |

A default, un-renamed label (`Get_Records_0`, `Assignment_1`,
`Decision_1`) never ships — see `SKILL.md`'s naming section for why:
these names are exactly what a review finding cites when there's no
line number to point at.

## Variable names

| Variable | Kind | Example name |
|---|---|---|
| Scalar (single value) | `var` prefix, camelCase | `varAccountId`, `varErrorMessage` |
| Collection | `col` prefix, camelCase, plural noun | `colRelatedContacts`, `colOpportunitiesToUpdate` |
| Loop variable | `loop` prefix, camelCase, singular noun matching its collection | `loopContact` (iterates `colRelatedContacts`), `loopOpportunity` (iterates `colOpenOpportunities`) |

The prefix is what makes a variable's shape legible from its name alone
on the resource panel, without opening its definition: `varX` is always
one value, `colX` is always a collection, `loopX` only ever exists
inside the Loop element that produced it.
