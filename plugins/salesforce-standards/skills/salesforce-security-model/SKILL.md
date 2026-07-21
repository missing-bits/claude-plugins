---
name: salesforce-security-model
description: Use when designing Salesforce data access — org-wide defaults, role hierarchy, profiles vs permission sets (permission-set-first), sharing rules, and field-level security in code and UI. Sharing keyword mechanics in Apex belong to salesforce-apex.
---

# Salesforce Security Model

Standards for designing who can see and change what: org-wide defaults
(OWD), role hierarchy, the profile/permission-set split, sharing rules,
and field-level security (FLS). Cite rules in review findings as
`(standard: salesforce-security-model, rule: <id>)`; each rule names its
source — the sharing/security documentation, Salesforce
Well-Architected, or `this standard` (a recorded house decision).
**The `with sharing` / `without sharing` / `inherited sharing` keyword
mechanics in Apex are out of scope here** — see `salesforce-apex`; this
skill governs the access model those keywords enforce: what OWD, roles,
and sharing rules actually grant.

## Org-wide defaults

**OWD is the access floor, opened selectively — never the other
way.** Every access-widening mechanism (role hierarchy, a sharing rule,
manual sharing, an Apex-managed share) adds visibility on top of OWD;
none of them can narrow what OWD already grants. Set OWD to the
strictest level the data actually needs, then open it up deliberately
for the roles and rules that need more.

- **Private is the default stance for any object holding business or
  sensitive data** — accounts, opportunities, cases, contracts, and any
  custom object carrying financial, contractual, or personal data. Access
  is opened selectively afterward, through the role hierarchy and
  sharing rules described below — never by defaulting the object wide
  open "to keep things simple."
- **Public (Read Only or Read/Write) is reserved for reference or
  dictionary data** — lookup-style objects with no business or
  sensitivity consequence to broad visibility (a country/region
  picklist-backing object, a product catalog reference table, a price
  book referenced org-wide). A Public OWD carries a **stated
  justification** — one line, on the object or in its design record,
  saying why universal visibility is safe for this object (no sensitive
  fields, no business harm from any user seeing every record).
- A **Public OWD on a business/sensitive-data object with no stated
  justification is a review finding**, regardless of how convenient the
  wide-open default felt during initial build.

A full worked example — OWD choice, role-hierarchy tiers, the sharing
rules that open the object further, and the permission sets that grant
capability on top of that visibility, all reasoned through for one
object — is in
[reference/access-model.md](reference/access-model.md).

(id: `security-owd`; source: sharing/security documentation — "Control
Who Sees What"; the private-by-default stance and the reference-data
carve-out with its justification requirement are this standard)

## Role hierarchy

**The role hierarchy grants record visibility upward, on top of OWD —
never a substitute for OWD, never a way around it.** For any object
where OWD is stricter than Public, a role automatically sees every
record owned by, or already shared with, any role below it in the
hierarchy (this can be switched off per custom object via "Grant Access
Using Hierarchies" when hierarchy-based visibility isn't the intended
story for that object).

- **Keep it shallow.** A role hierarchy models tiers of access need, not
  every layer of the management org chart. A handful of tiers (an
  individual-contributor tier, a manager tier, an exec/ops tier) is
  usually enough regardless of how many people-management layers HR
  draws — every extra tier compounds implicit access grants nobody
  explicitly asked for, and widens the blast radius of "who can now see
  this" on every future reorg.
- **Decouple it from the org chart.** A role node represents an access
  tier, not a job title or a reporting line. A manager who needs no
  broader record visibility than their reports does not need a role
  above them; conversely, two peers in different reporting chains who
  both need visibility into a shared book of business can share one
  role. Name each role for the access tier it grants
  (`Sales_Manager_Region`, not `Reports_To_VP_Smith`) so the hierarchy
  keeps working after the next reorg renames the management chain
  underneath it.

(id: `security-role-hierarchy`; source: sharing/security documentation —
role hierarchy record-access grants; the shallow, org-chart-decoupled
design guidance is this standard, informed by Salesforce Well-Architected
access-model guidance)

## Permission-set-first

**Profiles are reduced to the login/defaults shell: login hours, login
IP ranges, default record type, and page-layout assignment — nothing
that grants a capability.** Every capability — object CRUD, field-level
access, Apex class or Visualforce page access, a custom permission, tab
visibility — is granted through a permission set instead, never through
the profile.

- **Permission set groups (PSGs) are persona bundles** (`Sales_Rep`,
  `Service_Agent`), each composed of narrow, single-capability permission
  sets. **Users are assigned the persona group**, not a pile of
  individual permission sets; the permission sets themselves stay
  capability-scoped building blocks, assigned individually only for a
  genuine one-off exception outside any persona's normal shape.
- **A capability added to a profile instead of a permission set is a
  review finding** — no exception for "it's just one small checkbox."
  A profile-level grant applies silently to every user on that profile,
  is invisible to permission-set-based access-review tooling, and
  re-couples a capability to login-shell settings that have nothing to
  do with it.
- Decomposition patterns (per-capability vs per-app permission sets),
  naming, and a worked profile-stuffed-vs-permission-set-first
  anti-pattern pair are in
  [reference/permission-set-patterns.md](reference/permission-set-patterns.md).

(id: `security-permission-set-first`; source: Salesforce Well-Architected
— least-privilege, permission-set-first access-model guidance; the PSG
persona-bundle composition and the profile-as-review-finding stance are
this standard)

## Sharing rules

Two kinds, chosen by what actually determines who should see the record:

- **Ownership-based** sharing rule: shares records owned by a role,
  role-and-subordinates, or public group with another role or group.
  Choose this when access should follow *who owns the record*.
- **Criteria-based** sharing rule: shares records matching a field-based
  filter (e.g., `Region = 'EMEA'`, `Status = 'Escalated'`), regardless of
  who owns them. Choose this when access should follow *what the record
  is*, independent of ownership.
- **Naming**: `<Object>_<What>_To<Audience>` —
  `Case_Escalated_ToSupportManagers`, `Account_EMEA_ToRegionalTeam`. The
  name states the condition and the audience without needing to open the
  rule to find out what it does.
- **Document why each rule exists.** Every sharing rule's description
  states the business reason it was created and, where known, who
  requested it. An undocumented sharing rule is unreviewable once the
  person who built it has moved on — nobody can tell whether it is still
  needed or safe to remove.

(id: `security-sharing-rules`; source: sharing/security documentation —
criteria-based and ownership-based sharing rules; the naming convention
and the documented-why requirement are this standard)

## Field-level security (FLS)

FLS is enforced in two places, and both are required — a field hidden on
a page layout with no FLS restriction underneath is still readable and
editable through any other layout, the API, or an integration.

- **In the UI**: field-level security is granted through permission sets
  (never through profiles, per permission-set-first above). Page-layout
  field visibility is presentation only — it controls what a given
  layout shows, not what the running user is actually permitted to
  read or edit; FLS on the permission set is the real control.
- **In code**: enforce FLS (and sharing) at the query and DML boundary
  rather than trusting system-context access. Name the mechanism, not the
  keyword details — `WITH USER_MODE` on SOQL enforces the running user's
  FLS and sharing on the query itself; `Security.stripInaccessible`
  strips fields the running user can't access from a record or record
  list before it's used or returned. **The keyword mechanics
  (`with sharing` / `without sharing` / `inherited sharing` and how they
  interact with these) belong to `salesforce-apex`** — this skill only
  names which touchpoint to reach for.
- A query or DML operation touching business/sensitive data that runs in
  system context with neither of these enforcement steps, and no
  documented reason it must bypass user access, is a review finding.

(id: `security-fls`; source: sharing/security documentation — field-level
security enforcement; Apex Developer Guide — `WITH USER_MODE` and
`Security.stripInaccessible` (mechanics: `salesforce-apex`))

## Before adding any access grant

Before creating or widening **any** access grant — a sharing rule, a
permission set's object/field additions, a PSG assignment, a manual
share, an OWD change — answer three questions and record the answers
where the grant lives (the permission set/sharing rule description, the
design record):

1. **Who specifically needs this** — named as a role or persona, not
   "just in case" or "for everyone, to be safe."
2. **What is the narrowest scope that satisfies that need** — read vs
   edit, one field vs the whole object, one team vs the whole org?
3. **Does this expire, and how is it reviewed** — a temporary project
   grant, an integration user's access, a one-off manual share all get a
   revisit date; a grant with no expiry still gets a named periodic
   review point.

An access grant made without answering these — especially anything
labeled "temporary" with no revisit date attached — is how permanent,
unreviewed access drift accumulates; answer them at grant time, not after
an audit finds the leftover.

(id: `security-access-grant-questions`; source: this standard, informed
by Salesforce Well-Architected least-privilege access-model guidance)

## Review severities

- **Critical**: a Public OWD on a business/sensitive-data object with no
  stated justification (`security-owd`); a query or DML operation on
  business/sensitive data running in system context with no
  FLS/sharing enforcement step and no documented reason (`security-fls`).
- **Important**: a capability granted on a profile instead of a
  permission set (`security-permission-set-first`); a role hierarchy
  grown to mirror the full management org chart instead of access tiers
  (`security-role-hierarchy`); an undocumented sharing rule, or an
  ownership/criteria choice that doesn't match the actual access story
  (`security-sharing-rules`); an access grant added without a recorded
  who/scope/expiry answer (`security-access-grant-questions`).
- **Minor**: sharing-rule naming deviations (`security-sharing-rules`);
  permission set or permission set group naming deviations
  (`security-permission-set-first`).
