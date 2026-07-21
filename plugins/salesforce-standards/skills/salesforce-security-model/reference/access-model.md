# Worked access-model design: Opportunity

A worked example of the design questions from `SKILL.md` applied to one
object — `Opportunity`, chosen because it carries business-sensitive
data (deal amounts, discounts, close probability) and needs visibility
opened up for more than one persona.

## OWD choice: Private

**Reasoning**: deal financials and discount levels are exactly the kind
of business/sensitive data the OWD stance defaults to Private for (see
`SKILL.md`'s "Org-wide defaults"). A rep's pipeline is not something
every other rep, in every other territory, should see by default — a
wide-open OWD here would leak competitive deal terms and discount
patterns across the whole sales org. Nothing about `Opportunity` fits
the Public/reference-data carve-out, so Private is the floor, opened
selectively below.

## Role hierarchy considerations

Roles: `Sales_Rep` → `Sales_Manager_Region` → `Sales_Ops_Exec` — three
tiers, not one role per management layer. `Sales_Manager_Region` sees
every Opportunity owned by the reps below it in the hierarchy: exactly
the visibility a manager needs to review their team's pipeline, granted
automatically by hierarchy inheritance on top of the Private OWD, with no
separate sharing rule needed for that specific relationship.

**Why shallow, not org-chart-deep**: the actual sales org has more
management layers than this (team leads, regional VPs, a CRO), but none
of those intermediate layers change *who needs to see which
Opportunities* — they only change who manages whom. Modeling every one
of those layers as a role would mean every promotion or reporting-line
change forces a role-hierarchy edit that has nothing to do with data
access. Three access tiers cover every distinct visibility need this
object has.

## Sharing rules that open it further

Two additional groups need visibility the role hierarchy doesn't grant on
its own — a criteria-based case and an ownership-based case:

- **`Opportunity_EMEA_ToRegionalTeam`** (criteria-based): shares every
  Opportunity where `Region__c = 'EMEA'` with the EMEA regional support
  group, regardless of which rep owns it and regardless of role. Chosen
  because the access story here is "what region is this deal in," not
  "who owns it" — a criteria-based rule expresses that directly, where an
  ownership-based rule would require enumerating every EMEA rep's role
  instead of just filtering on the field that already says so.
- **`Opportunity_SquadDeals_ToSolutionEngineers`** (ownership-based):
  shares Opportunities owned by any rep on a given sales squad with that
  squad's assigned Solution Engineers, who sit outside the sales role
  hierarchy entirely. Chosen because the access story here genuinely is
  "who owns the record, on this squad" — the Solution Engineers need the
  same visibility a squad's manager would have, without being placed
  inside the sales management hierarchy (which would grant them
  visibility into every squad, not just their own).

Both rules carry a description stating why they exist and who requested
them, per `SKILL.md`'s sharing-rules documentation requirement.

## Permission sets that open capability, not just visibility

Sharing rules and the hierarchy grant *visibility*; permission sets grant
*what a user with that visibility can do*. For `Opportunity`:

| Permission set | Grants | How it's assigned | Reasoning |
|---|---|---|---|
| `Opportunity_Edit_Core` | Read/Create/Edit on `Opportunity`; edit on standard deal fields (Amount, Stage, Close Date) | Bundled into the `Sales_Rep` PSG | The base capability every rep needs to run their own pipeline — bundled into the persona group, never assigned as a standalone exception. |
| `Opportunity_Discount_Override` | Edit on `Discount_Percent__c` only | Assigned individually to the Deal Desk group, not bundled into any PSG | Deliberately narrow: most reps request a discount through an approval process rather than editing the field directly; the field-edit capability itself is scoped to the small group that adjudicates overrides, not to every rep who merely has edit on the object. |
| `Opportunity_Delete` | Delete on `Opportunity` | Assigned individually to Sales Ops, not bundled into any persona PSG | Delete is rare and consequential enough that it stays an explicit, individually-tracked grant rather than riding along inside a broader persona bundle where it would be easy to lose track of who actually has it. |

No capability above is a profile grant — every row is a permission set,
composed into a PSG where the capability belongs to a whole persona, or
assigned individually where it is a genuinely narrow exception (per
`SKILL.md`'s permission-set-first section and
[permission-set-patterns.md](permission-set-patterns.md)).
