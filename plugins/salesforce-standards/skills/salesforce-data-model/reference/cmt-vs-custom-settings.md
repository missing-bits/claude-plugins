# Custom Metadata Types vs Custom Settings

## Decision table

| Criterion | Custom Metadata Type (CMT) | Custom Setting — Hierarchy |
|---|---|---|
| What it holds | Configuration that is the same for every user and every environment once deployed | A value that legitimately differs by org default / profile / user |
| Moves through deployment | Yes — records are metadata; they ride change sets, unlocked/managed packages, and scratch-org deploys like any other component | No — the data is org-local; each environment needs it seeded or edited separately |
| Runtime access in Apex | SOQL query (`[SELECT ... FROM My_Type__mdt]`), or Flow's "Get Records" against the type | `getInstance()` / `getOrgDefaults()` — no query written at all |
| Built-in org → profile → user cascade | No — CMT has no per-running-user resolution; a query only ever returns the same records regardless of who's running it | Yes — this cascade is the type's defining feature |
| Editable by an admin directly in production | Yes, via Setup, but changes made this way aren't captured in the next deployment (the deploy overwrites them back to whatever's in source) | Yes, and that's often the point — the value can be flipped live without waiting on a deployment |
| Default choice | **Yes — start here for any new configuration** | Only when the cascade resolution above is actually needed |

## Worked example: Custom Metadata Type with records

**`Discount_Tier__mdt`** — discount tiers used by a pricing flow/Apex
service, the same for every user and every org once deployed.

| Field | Purpose |
|---|---|
| `DeveloperName` (standard on every CMT) | The stable key referenced at runtime — `Bronze`, `Silver`, `Gold` |
| `Minimum_Order_Amount__c` (Number) | The order-total threshold this tier applies from |
| `Discount_Percent__c` (Percent) | The discount applied at this tier |

Records: `Bronze` (`Minimum_Order_Amount__c` = 0, `Discount_Percent__c` =
0), `Silver` (1000, 5), `Gold` (5000, 10).

A pricing service queries by `DeveloperName`, never by record Id:

```
SELECT Discount_Percent__c FROM Discount_Tier__mdt WHERE DeveloperName = 'Gold'
```

**Why CMT here**: the tier thresholds are business configuration, not
per-user or per-org-instance data — every sandbox and every user sees
the same tiers. Adding a `Platinum` tier ships as part of a normal
deployment (a new record in source control), with no separate
per-environment data migration step, and the query-by-`DeveloperName`
pattern is exactly the "no hardcoded IDs" alternative from `SKILL.md`.

## Worked example: Hierarchy Custom Setting

**`Automation_Control__c`** (Hierarchy Custom Setting) — a per-profile
override letting a bulk data-load integration user skip trigger/flow
automation, resolved automatically without extra query logic.

| Field | Purpose |
|---|---|
| `Bypass_Automation__c` (Checkbox) | When true for the resolved level, automation short-circuits for the running context |

Rows:

- **Org Default**: `Bypass_Automation__c` = unchecked — automation runs
  normally for everyone by default.
- **Profile override — `Integration User`**: `Bypass_Automation__c` =
  checked — the integration user driving bulk data loads skips
  automation, without any code change.

Accessed in a trigger handler guard (or a Flow decision, via
`$Setup.Automation_Control__c.Bypass_Automation__c`):

```apex
if (Automation_Control__c.getInstance().Bypass_Automation__c) {
    return;
}
```

**Why a Hierarchy Custom Setting here, and not CMT**: the value must
resolve *differently depending on who is running the code* — the
default for everyone is "automation runs," but the Integration User
profile needs the opposite, and `getInstance()` gives that resolution
for free without the handler having to figure out "is this the
integration user?" itself. Support also needs to be able to flip this
live in production during an emergency load — no CMT deployment step
required.

This is a *different* bypass mechanism from the Custom-Permission
pattern described in `SKILL.md`'s validation-rules section (which gates
one validation rule's formula) — the two solve different problems:
gating a single declarative rule's formula (Custom Permission) versus
gating an entire automation path for a specific running-context
(Hierarchy Custom Setting). Pick whichever mechanism matches what's
actually being bypassed; don't reach for a Custom Setting to solve a
single validation rule's bypass, and don't reach for a Custom Permission
to solve a whole-automation-path, per-profile toggle.
