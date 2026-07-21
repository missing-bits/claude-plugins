---
name: salesforce-flow
description: Use when building or reviewing Salesforce Flows — naming, plan-before-build, bulk-safe patterns, fault paths, run context, one record-triggered flow per object and trigger moment, and the maintenance-only stance for Workflow Rules and Process Builder.
---

# Salesforce Flow

Standards for building and reviewing Salesforce Flows: naming, planning
discipline, bulk safety, fault handling, run context, and the boundary
with retired automation tools. Cite rules in review findings as
`(standard: salesforce-flow, rule: <id>)`; each rule names its source —
the Flow documentation, Salesforce Well-Architected, or `this standard`
(a recorded house decision). Apex-side layering is `salesforce-apex`'s
concern; object/field naming is `salesforce-data-model`'s; sharing and
access-model design beyond the run-context mechanics below is
`salesforce-security-model`'s.

Flows are authored in Flow Builder, not in a text editor — this skill
and its reference files describe structure (element names, connections,
settings) rather than XML to copy-paste.

## Naming

| Element | Convention | Example |
|---|---|---|
| Record-triggered flow | `<Object>_<TriggerMoment>_<Purpose>` | `Account_AfterSave_SyncBilling`, `Case_BeforeSave_Defaults` |
| Other flow types (screen, autolaunched, subflow) | `<Domain>_<Purpose>` | `Onboarding_CollectConsents` |
| Flow element (any type) | Verb-first label, Title Case with underscored words; Flow Builder derives the API name from the label | `Get_Related_Opportunities`, `Decision_Is_High_Priority` |
| Variable (scalar) | camelCase, `var` prefix | `varAccountId` |
| Variable (collection) | camelCase, `col` prefix, plural noun | `colRelatedContacts` |
| Loop variable | camelCase, `loop` prefix, singular noun matching its collection | `loopContact` (iterating `colRelatedContacts`) |

At least four worked examples across flow, element, and variable names
are in [reference/naming.md](reference/naming.md).

**Element names are not cosmetic — they are review citations.** Flow
metadata has no source-code line numbers, so a review finding against a
flow cites the element by name instead of a line; the `salesforce-code-review`
review stack orders these line-less findings alphabetically by cited
element name. A default label left un-renamed (`Get_Records_0`,
`Assignment_1`) makes every citation against it just as vague — rename
every element for what it does before saving the flow, not only the
ones that "matter."

(id: `flow-naming`; source: Flow documentation — "Naming Conventions for
Flows"; the record-triggered pattern, the other-flow-types pattern, and
the element/variable prefixes are this standard)

## Plan before you build

Sketch the flow before opening Flow Builder — on paper, in a doc, or as
a quick diagram:

- **Entry criteria**: which object, which trigger moment, and the exact
  entry-condition formula that keeps the flow off records it has no
  business touching.
- **Decision branches**: every fork the flow needs and what routes a
  record down each one.
- **Failure behavior**: for every element that writes or calls out, what
  happens when it fails — logged, retried, surfaced to a user, or some
  combination (see "Fault paths" below).

A flow built straight into the canvas tends to grow its branching and
its failure handling as afterthoughts; sketching first also surfaces
subflow candidates before the canvas is already tangled (see the next
section).

(id: `flow-plan-before-build`; source: this standard)

## One record-triggered flow per object and trigger moment

**At most one record-triggered flow per object per trigger moment**
(before-save, after-save, before-delete, …). When a second piece of
automation is needed for the same object and moment, add a Decision
element (or another branch off an existing one) to the existing flow —
never a second flow competing for the same trigger context. Two flows on
the same object and moment run in an order that is hard to reason about
and easy to get wrong when either one changes independently; one flow
with internal branching keeps the execution order visible on a single
canvas.

- **Orchestrate inside the flow**, not by flow proliferation: a Decision
  element per distinct scenario, each branch doing its own work.
- **Subflows** extract logic out of that single flow only when: the same
  logic is reused in two or more flows, OR a branch has grown complex
  enough that it no longer reads clearly on the canvas. Never extract a
  subflow for its own sake — a subflow that exists only to shorten one
  flow's canvas, with no reuse and no clarity gain, is an unjustified
  extraction and a review finding in the other direction.

(id: `flow-one-per-object-moment`; source: Salesforce Well-Architected —
record-triggered flow consolidation guidance; the subflow
reuse-or-clarity threshold is this standard)

## Bulk-safe patterns

A record-triggered flow runs once per triggering transaction against the
**entire batch** of records in it (up to 200), never once per record —
design every flow as if it always receives the maximum batch:

- **No Get Records, Update Records, or Delete Records inside a Loop
  element.** Query once before the loop (or not at all, using data
  already on `$Record`/`$Record__Prior`), build a collection variable
  inside the loop with an Assignment element ("Add" to a collection),
  and perform one collection-based Create/Update/Delete Records element
  after the loop ends.
- **Entry conditions keep the flow off irrelevant records.** Configure
  the start element's condition requirements (and, for after-save flows,
  "Only when a record is updated to meet the condition requirements") so
  the flow's interview doesn't even begin for records the automation has
  no reason to touch — this is cheaper than an early Decision exit and
  keeps unrelated saves from paying any of the flow's cost.
- **Collection variables, not repeated single-record operations,** are
  the unit of work for every DML and Get element outside a loop.

A full bulk-safe record-triggered structure — start, a filtered Get, a
loop that only assigns into a collection, and a single Update Records
after the loop — is in
[reference/flow-patterns.md](reference/flow-patterns.md).

(id: `flow-bulk-safe`; source: Flow documentation — "Bulkify Your Design";
Salesforce Well-Architected — bulkification guidance)

## Fault paths

**Every element that performs DML or a callout (Create Records, Update
Records, Delete Records, an Action/Apex/HTTP callout, a Submit for
Approval) connects both its default path and its fault path.** A fault
path is never left unconnected: Flow Builder's unhandled-fault default
surfaces a generic error to whatever invoked the interview, which for a
record-triggered (system-context, no user present) or scheduled flow
means the failure disappears with nobody seeing it.

- The fault connector leads to **named handling behavior** — at minimum,
  create a record of the failure (an error-log custom object, a platform
  event that commits independently of the failed transaction) so the
  failure is queryable after the fact; add a notification (email alert,
  a Slack/Chatter post) when the failure needs a human to act promptly.
- A missing fault path, or a fault path that dead-ends without doing
  anything observable, is a review finding regardless of how unlikely
  the element is to fail in practice.
- The fault-path pattern, including the shared error-logging branch
  multiple DML elements fault into, is in
  [reference/flow-patterns.md](reference/flow-patterns.md).

(id: `flow-fault-paths`; source: Flow documentation — "Fault Paths and
Fault Connectors")

## Run context

**Every flow's run context is an explicit choice, not whatever the
default happens to be.** Flow properties expose the choice directly:

| Context | Object/field permissions | Sharing rules |
|---|---|---|
| System Context Without Sharing | Bypassed | Bypassed |
| System Context With Sharing | Bypassed | Enforced |
| User Context | Enforced (running user's object/field permissions) | Enforced |

- **System Context Without Sharing** is the usual choice for background,
  record-triggered automation that must act regardless of who touched
  the triggering record — but state that reasoning where the flow is
  documented, since it means the flow can read and write fields and
  records the running user could not touch directly.
- **User Context** is the right choice for a screen flow or any flow
  whose whole point is to respect what the running user is allowed to
  see and do — an approval-request screen flow, a self-service data
  correction flow.
- Whichever is chosen, **name the sharing implication**: a
  without-sharing flow that writes to a field the running user's profile
  can't normally edit is a deliberate design decision, not an accidental
  side effect discovered later in a support ticket.

(id: `flow-run-context`; source: Flow documentation — "Set Flow Run
Context and Data Access")

## Retired automation

**Workflow Rules and Process Builder are maintenance-only.** No new
Workflow Rule and no new Process Builder process is ever created — Flow
is the migration target for every new piece of declarative automation,
and for any existing Workflow Rule or Process Builder process that needs
a change beyond a trivial fix. Existing ones are edited in place only
when the edit is small and low-risk; anything larger is rebuilt as a
Flow rather than extended in the retired tool.

(id: `flow-retired-automation`; source: Salesforce's own retirement
guidance for Workflow Rules and Process Builder — Flow is the sole
supported path for new declarative automation; this standard's
maintenance-only enforcement)

## Review severities

- **Critical**: a Get/Update/Delete Records element inside a Loop
  (`flow-bulk-safe`); a Create/Update/Delete Records or callout element
  with no fault path, or a fault path that does nothing observable
  (`flow-fault-paths`); a second record-triggered flow created on
  an object and trigger moment an existing flow already owns
  (`flow-one-per-object-moment`).
- **Important**: run context left unstated or undocumented, especially
  System Context Without Sharing with no reasoning given
  (`flow-run-context`); missing or overly broad entry conditions that let
  a flow's interview run on records it has no reason to touch
  (`flow-bulk-safe`); a subflow extracted with neither reuse nor a
  clarity justification (`flow-one-per-object-moment`); a new Workflow
  Rule or Process Builder process (`flow-retired-automation`).
- **Minor**: naming convention deviations on flows, elements, or
  variables, including default un-renamed element labels
  (`flow-naming`).
