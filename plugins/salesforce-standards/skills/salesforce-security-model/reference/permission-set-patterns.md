# Permission-set decomposition patterns

## Per-capability decomposition

Split a single object's permissions along **action**, not along
"everything this role touches." Each permission set grants one
capability, narrowly:

| Permission set | Grants |
|---|---|
| `Opportunity_Read` | Read on `Opportunity` and its standard fields |
| `Opportunity_Edit_Core` | Read/Create/Edit on `Opportunity`, standard deal fields |
| `Opportunity_Discount_Override` | Edit on `Discount_Percent__c` only |
| `Opportunity_Delete` | Delete on `Opportunity` |

A user's actual capability is the **union** of whichever of these their
assigned PSG (or, rarely, an individual assignment) includes. Splitting
this finely means a future capability change — granting discount-edit to
a second team, revoking delete from everyone — touches one narrow
permission set, not a re-audit of a monolithic "Opportunity access"
permission set that quietly also grants five unrelated things.

## Per-app decomposition

Where several objects form one coherent workflow, a permission set can
bundle *related* capabilities across objects — as long as the bundle
still represents one narrow, nameable capability rather than "whatever
this persona needs":

| Permission set | Grants |
|---|---|
| `CaseIntake_Core` | Create/Edit on `Case`; Read on `Account`, `Contact` (enough to look up the requester) |
| `CaseEscalation` | Edit on `Case.Status`/`Case.Priority` beyond intake defaults; Read on `Escalation_Note__c` |

The distinction from a profile-stuffed bundle (below) is that each of
these still names one workflow-shaped capability — intake, escalation —
rather than "everything a Service Agent could ever need," which belongs
one level up, at the PSG.

## Naming

- **Permission set**: `<Object|Area>_<Capability>` —
  `Opportunity_Discount_Override`, `Case_Escalate`, `Account_Edit`. The
  name states what the set grants without opening it.
- **Permission set group (persona bundle)**: the persona noun, Title
  Case with underscores — `Sales_Rep`, `Service_Agent`. A PSG's
  description lists which permission sets it bundles and why each one
  belongs to that persona.

## Anti-pattern pair: profile-stuffed vs permission-set-first

**Profile-stuffed** (avoid): a `Sales Rep` profile directly grants
Opportunity CRUD, Discount edit, Account edit, and five Apex class
accesses, all as profile-level settings.

| Symptom | Why it hurts |
|---|---|
| Every capability lives on one profile object | Auditing "who can override a discount" means reading every field of the profile, not one named permission set — nothing is queryable by capability |
| A second persona needing *most* of the same access (e.g., a Sales Ops role that needs everything a rep has, plus delete) must either duplicate the whole profile or get a second, diverging profile | No reuse — profiles don't compose |
| A capability change (revoke discount-edit from reps) means editing the profile, re-testing everyone on it | Blast radius is "everyone on this profile," even when the change was meant for a subset |

**Permission-set-first** (the standard): the `Sales_Rep` PSG bundles
`Opportunity_Edit_Core` + `Account_Edit`, each independently reusable;
`Opportunity_Discount_Override` is assigned separately only to Deal Desk;
a `Sales_Ops` PSG bundles `Opportunity_Edit_Core` + `Opportunity_Delete`,
reusing the same `Opportunity_Edit_Core` set the `Sales_Rep` PSG also
uses instead of duplicating it.

| Symptom (of doing it right) | Why it helps |
|---|---|
| Each capability is one named, independently queryable permission set | "Who can override a discount" is answered by reading `Opportunity_Discount_Override`'s assignments, nothing else |
| Personas compose from shared building blocks | `Sales_Ops` reuses `Opportunity_Edit_Core` rather than duplicating its grants |
| A capability change touches one permission set | Revoking discount-edit from Deal Desk doesn't touch `Sales_Rep`, `Sales_Ops`, or anything else that doesn't include that set |

The profile, in both the good and bad case, still exists — it just stays
reduced to the login/defaults shell (per `SKILL.md`'s
permission-set-first section) in the good case, and grows capability
grants it should never have carried in the bad case.
