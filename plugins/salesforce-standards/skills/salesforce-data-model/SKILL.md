---
name: salesforce-data-model
description: Use when creating or naming Salesforce objects and fields — object and field naming, record types, validation rules, Custom Metadata Types vs Custom Settings, global value sets, hardcoded-ID bans, and field descriptions. Access to the data belongs to salesforce-security-model.
---

# Salesforce Data Model

Standards for declarative data-model design: object and field naming,
record types, validation rules, configuration storage (Custom Metadata
Types vs Custom Settings), global value sets, and the ban on hardcoded
IDs. Cite rules in review findings as
`(standard: salesforce-data-model, rule: <id>)`; each rule names its
source — the object/field metadata documentation, Salesforce
Well-Architected, or `this standard` (a recorded house decision).
**Access to the data is out of scope here** — org-wide defaults,
profiles, permission sets, field-level security, and sharing rules
belong to `salesforce-security-model`; this skill governs only the shape
of the data model itself.

## Object and field naming

| Element | Label | API name |
|---|---|---|
| Custom object | Title Case business term | PascalCase words separated by underscores, `__c` suffix, no abbreviations |
| Custom field | Title Case business term | PascalCase words separated by underscores, `__c` suffix, no abbreviations |

Examples: label `Total Amount` → API name `Total_Amount__c`; label
`Billing Sync Status` → API name `Billing_Sync_Status__c`.

- **Label and API name serve different audiences and change on
  different terms.** The Label is what users see on page layouts,
  reports, and list views — rename it freely as the business's
  vocabulary shifts; the Translation Workbench handles it per language.
  The API name is what every formula, validation rule, flow, Apex class,
  and integration references — decide it carefully at creation, because
  renaming it later means finding and fixing every reference, not just
  relabeling a UI string.
- **No abbreviations, ever, in the API name** — `Total_Amount__c`, not
  `Tot_Amt__c`. An abbreviation reads differently to every person who
  didn't coin it, and a full word costs nothing once autocomplete exists
  in every tool that edits metadata.
- **Boolean (checkbox) fields read as an assertion**: `Is_` or `Has_`
  plus the condition being asserted — `Is_Active__c`,
  `Has_Signed_Contract__c` — never a bare noun that leaves the true/false
  meaning to be guessed (`Active__c` could mean either "is active" or
  "activation date").
- The same PascalCase-with-underscores, no-abbreviation rule applies
  uniformly across every field type (text, number, currency, date,
  picklist, formula, lookup, master-detail) — there is one field-naming
  convention, not one per type.
- **Record type API names** follow the identical convention, mirroring
  their label: label `Enterprise Account` → API name
  `Enterprise_Account`.

At least one worked example per field type, plus object and record-type
examples, is in [reference/naming.md](reference/naming.md).

(id: `data-model-naming`; source: object/field metadata documentation —
"Name Field Values"; the underscore-PascalCase, no-abbreviation
convention and the boolean assertion-naming guidance are this standard)

## Field descriptions

**Every custom object and every custom field carries a description.**
The description states two things, at minimum: what the object/field is
*for*, and *who or what writes it* (a user role, an integration, a flow,
a formula). A description that repeats the label
(`Total_Amount__c` — "The total amount") without saying what populates
it or why it exists satisfies the letter of the policy but not its
purpose — write it for the next person who opens Setup with no other
context.

**A missing description is a review finding** — this policy has no
"custom fields only, standard objects exempt" carve-out and no severity
floor below which it's skipped: every custom object, every custom field,
gets one.

(id: `data-model-descriptions`; source: this standard)

## Record types

- **Naming**: a record type's label is the business term for the
  variation it represents (`Enterprise Account`, `Renewal Opportunity`);
  its API name mirrors that label under the same convention as objects
  and fields (see above).
- **Record type vs a picklist-driven variation** — the question is
  whether the variation changes *structure* or only a *value*:
  - Choose a **record type** when the variation needs its own page
    layout, its own required/visible fields, its own picklist value
    subset (via record-type-scoped picklist values), its own sharing
    rule criteria, or its own process (approval process, assignment
    rule) keyed off the record type itself.
  - Choose a **picklist field** (plain or restricted, on a single record
    type) when the variation is *only* a different value on an
    otherwise-identical record — the same layout, the same required
    fields, the same process applies regardless of which value is
    selected. A `Status__c` picklist with values `Draft`/`Active`/
    `Closed` does not need three record types if every status shares the
    same layout and required fields.
  - A record type introduced only to gate a handful of picklist values
    per "type" — with no layout, sharing, or process difference — is
    over-modeling: the picklist field alone would have done the job with
    far less to maintain (one more layout, one more set of
    record-type-visibility assignments per profile, for every future
    change).

(id: `data-model-record-types`; source: Salesforce Well-Architected —
record type vs picklist guidance; the record-type naming convention is
this standard)

## Validation rules

- **Naming**: descriptive, underscore-separated, no numbered prefixes —
  `Close_Date_Not_Past`, `Amount_Required_When_Won`. Never
  `VR01_CloseDate` or `Validation_Rule_3`: a number tells the next
  person nothing about what the rule checks, and renumbering after an
  insertion or deletion churns unrelated rules for no reason.
- **User-actionable error messages.** The error message text names the
  field at fault (when field-level placement doesn't already point to
  it) and states what to change — not just that something is wrong.
  "Amount is required when Stage is Closed Won" tells the user what to
  do; "Invalid data" does not, and turns every trip of the rule into a
  support ticket.
- **Every validation rule has an explicit bypass strategy**, named in
  the rule itself (a comment in the description field) or in the object's
  documentation — never an implicit "nobody thought about it." The
  house pattern is a **Custom Permission check**: a Custom Permission
  (e.g. `Bypass_Validation_Rules`) is added as an `AND` branch of the
  rule's formula (`AND( <rule condition>, NOT($Permission.Bypass_Validation_Rules) )`
  — the rule fires only when the condition is true AND the running user
  lacks the permission), and that Custom Permission is granted, via a
  permission set, only to the integration/data-load users who
  legitimately need to bypass it. This skill covers only the
  check-in-formula mechanism; *who* gets that permission set assigned is
  `salesforce-security-model`'s concern.
- A validation rule with no bypass path at all blocks every future
  legitimate exception (a one-time data correction, a migration load)
  behind an emergency deactivate-and-reactivate cycle in production —
  design the bypass in at creation time, not after the first incident.

(id: `data-model-validation-rules`; source: object/field metadata
documentation — validation rule formulas; the naming convention and the
Custom-Permission bypass pattern are this standard)

## Custom Metadata Types vs Custom Settings

**Default to Custom Metadata Types (CMT) for configuration.** CMT
records are metadata — they deploy with the package (change sets,
unlocked/managed packages, scratch-org deploys, `sf project deploy`)
exactly like any other component, so a new environment gets the
configuration automatically instead of needing it reseeded by hand.

**Custom Settings — specifically Hierarchy Custom Settings — remain for
one narrow case**: a value that must resolve differently depending on
*who is running the code*, automatically, with no extra query logic.
Hierarchy Custom Settings' `getInstance()` / `getOrgDefaults()` access
walks the org-default → profile → user cascade for free — CMT has no
equivalent per-user/per-profile resolution built in; a CMT query only
ever returns the same records regardless of who's running it, so CMT
fits org-wide, identical-for-everyone values only.

The decision table, plus a worked CMT example (a type with records) and
a worked Hierarchy Custom Setting example, annotated with why each
choice was made, are in
[reference/cmt-vs-custom-settings.md](reference/cmt-vs-custom-settings.md).

(id: `data-model-cmt-vs-settings`; source: Salesforce Well-Architected —
Custom Metadata Types as the configuration-storage default; the
Hierarchy-Custom-Settings-only-for-per-user-resolution boundary is this
standard)

## Global value sets

**A picklist's value list is defined once, in a Global Value Set, the
moment it's shared by a second field.** A field-local ("inline") value
list is acceptable only while the values genuinely belong to that one
field alone; the instant a second field needs the same values
(`Priority` on `Case` and on a custom object, `Region` on three
different objects), extract them into a Global Value Set and repoint
every field at it.

- **No duplicated inline value lists across objects.** Two fields
  independently listing `High`/`Medium`/`Low` will drift the moment
  someone adds a value to one and not the other — a Global Value Set is
  the single place that addition happens, and every field referencing it
  picks it up.
- Global Value Sets also support **field-specific restricted subsets**
  (a field can expose only some of the set's values) and per-record-type
  visibility, so extracting to a Global Value Set never forces every
  consuming field to expose every value.

(id: `data-model-global-value-sets`; source: object/field metadata
documentation — Global Value Sets)

## No hardcoded IDs

**A Salesforce record Id, RecordTypeId, queue Id, or similar
org-specific identifier is never hardcoded** — not as a string literal
in Apex, not in a formula, not in a Flow (a hardcoded value in a Decision
condition or an Assignment), not in a validation rule. Ids are
per-organization: a value copied from production does not exist, or
means something else, in a sandbox, a scratch org, or another
customer's org — a hardcoded Id is a deployment failure (or, worse, a
silent wrong-record bug) waiting for the next environment the code
lands in.

Alternatives, by what the hardcoded value was standing in for:

- **A configuration value or threshold** → a Custom Metadata Type
  record, queried or referenced by its `DeveloperName` (or via a
  Metadata Relationship field), never by its record Id.
- **A record type** → compare `RecordType.DeveloperName` (directly
  available in a formula, or via a query filter in Apex/Flow), never
  `RecordTypeId` as a literal.
- **A queue, group, or profile** → query it at runtime by its
  `DeveloperName` or unique `Name`, never embed the Id.
- **Static, translatable text (not an identifier)** → a Custom Label.
- **A user-facing display string that happens to vary by environment**
  → a Custom Label, not a hardcoded value baked into the logic.

The common thread: every alternative resolves the concrete Id **at
runtime, by a stable developer-facing name**, instead of baking in a
value that is only ever correct in the org it was copied from.

(id: `data-model-no-hardcoded-ids`; source: Salesforce Well-Architected —
avoid hardcoded IDs guidance)

## Review severities

- **Critical**: a hardcoded Id/RecordTypeId in code, a formula, a flow,
  or a validation rule (`data-model-no-hardcoded-ids`); a validation
  rule with no bypass strategy at all (`data-model-validation-rules`).
- **Important**: a missing description on a custom object or field
  (`data-model-descriptions`); a duplicated inline picklist value list
  that should be a Global Value Set (`data-model-global-value-sets`); a
  validation rule error message that doesn't tell the user what to
  change; a record type introduced with no layout, sharing, or process
  difference from a plain picklist (`data-model-record-types`); Custom
  Settings used for org-wide configuration that CMT should hold
  (`data-model-cmt-vs-settings`).
- **Minor**: naming convention deviations on objects, fields, record
  types, or validation rules (`data-model-naming`,
  `data-model-validation-rules`), including numbered validation-rule
  names.
