---
name: salesforce-aura
description: Use when maintaining existing Aura components — markup, controller and helper JavaScript, component vs application events, and Lightning Data Service. Maintenance-first; new UI belongs to salesforce-lwc unless the platform forces Aura.
---

# Salesforce Aura

**Maintenance-first.** Existing Aura components are held to every
standard in this skill — being legacy is not a pass on quality. But new
UI is built in LWC, never Aura, unless the platform genuinely forces
Aura (a surface where LWC support is missing). New Aura surface added to
a review without a named platform-forcing reason is itself a review
finding — "the team already knows Aura" or "the existing component is
Aura" are not forcing reasons; only a concrete platform gap is. See
`salesforce-lwc` for where new UI work belongs and how it is built.

Cite rules in review findings as `(standard: salesforce-aura, rule:
<id>)`; each rule names its source — the Aura Components Developer
Guide, or `this standard` (a recorded house decision).

## Markup

- **Attribute typing**: every `<aura:attribute>` declares a specific
  `type` (`Id`, `String`, `Boolean`, `Integer`, `SObject`, a `List` or
  `Map` of one of these) — never the generic `Object` as an escape
  hatch, which defers a wrong-shaped value to a runtime error instead of
  a markup-time catch. Give attributes with a sensible default a
  `default="..."` value instead of leaving every caller to supply it.
- **Expression discipline**: an expression (`{!v.someAttribute}`,
  `{!c.handleClick}`) reads a single attribute or invokes a single
  controller action — never inline arithmetic, string concatenation, or
  a multi-step conditional (e.g. `{!v.a + v.b > v.c ? 'x' : 'y'}`).
  Compute a derived value once in the controller/helper and expose it
  through a dedicated attribute for the markup to read — logic in
  markup hides from review and can't be unit tested.
- **`aura:if` vs CSS-class toggling**: `aura:if` destroys and rebuilds
  the DOM subtree it hides — `init`/`render` re-run on every flip, and
  server-side data (e.g. a `force:recordData` load) can be re-fetched.
  Reach for `aura:if` when the branches are genuinely different content,
  or the hidden branch shouldn't even exist in the DOM (an admin-only
  panel, an expensive component that must not mount until needed).
  Reach for CSS-class toggling (`aura:id` + `component.find(...).set
  ("class", ...)`, or a computed class attribute) when the markup just
  needs to show/hide — a dropdown, a validation message, an
  expand/collapse — especially when toggling is frequent or the
  branch's state (scroll position, an in-progress edit) must survive
  it.

(id: `aura-markup`; source: Aura Components Developer Guide — "Component
Markup", "Conditional Markup with aura:if"; the toggling decision rule is
this standard)

## Controller vs helper

- **Controllers are thin.** A `<name>Controller.js` function only wires
  a DOM/component event to behavior: read what the event carries, hand
  it to a helper, and (when needed) apply the helper's result back onto
  the component. A controller action with a multi-line conditional, a
  loop, or a direct Apex call has grown logic that belongs in the
  helper.
- **Helpers hold the logic.** `<name>Helper.js` is where the actual work
  lives — validation, data shaping, the Apex call and its callback,
  anything beyond one line of reasoning — and what more than one
  controller action can call, so shared behavior lives in one place
  instead of being copy-pasted across handlers.
- **No business logic in the component at all.** A calculation encoding
  a business rule (a discount formula, an eligibility check, a status
  transition) belongs in Apex — an `@AuraEnabled` method invoked from
  the helper — never in the controller or helper. Component JavaScript
  orchestrates UI and shapes data for display; it is never the system
  of record for a rule Apex could enforce once and share across every
  caller (Flow, integrations, other UI).

(id: `aura-controller-helper`; source: Aura Components Developer Guide —
"Client-Side Controllers", "Helper Methods"; the thin-controller and
no-business-logic stances are this standard)

## Events

- **Component events for parent-child.** When the interaction is
  contained inside a component's own containment tree — a child
  notifying its direct container — define a component event
  (`<aura:event type="COMPONENT">`), register it with
  `<aura:registerEvent>`, and have the containing component catch it the
  way a component event is actually caught: an attribute on the child's
  tag matching the registered event name (`<c:child
  recordSaved="{!c.handleIt}"/>`), or the firing component handling its
  own event directly. `<aura:handler>` is the application-event
  mechanism (or a component self-handling its own registered event) —
  it is not how a parent catches a child's component event. A component
  event only reaches its direct container this way; an indirect ancestor
  needs its own explicit attribute wiring on the intermediate component,
  or that component re-firing its own event upward — it does not bubble
  further on its own.
- **Application events only for genuine cross-tree needs.** Reach for
  an application event (`<aura:event type="APPLICATION">`, fired with
  `$A.get("e.c:EventName")`) only when there is no containment
  relationship to exploit — siblings dropped independently onto the
  same page, or components in separate parts of the tree reacting to
  the same thing. Every component with a matching `<aura:handler>`
  anywhere in the app receives it, so reaching for one out of
  convenience where a component event would do widens the blast radius
  of a change and hides the real dependency graph.
- **Naming and payload discipline**: name an event for what happened,
  not the component that fired it (`RecordSaved`, not
  `AccountCardEvent`), and type every parameter explicitly — same
  discipline as component markup. Keep the payload to what a handler
  actually needs (the changed record's Id, the new value), not the
  whole record or firing component's state — a narrow payload keeps an
  event's contract legible without reading the firing component's code.
- Full worked examples — registering, firing, and handling both event
  kinds, with the decision rule annotated inline — are in
  [reference/events.md](reference/events.md).

(id: `aura-events`; source: Aura Components Developer Guide — "Component
Events", "Application Events"; the naming/payload discipline and the
component-first decision rule are this standard)

## Lightning Data Service

**`force:recordData` (Lightning Data Service) over ad-hoc Apex for
single-record CRUD.** Loading, creating, updating, or deleting one
record — a record detail panel, a quick-edit form, or a related-record
card — goes through `<force:recordData>` bound to the component, not a
hand-written `@AuraEnabled` method running its own SOQL/DML for the
same job. LDS gives that traffic sharing and FLS enforcement for free,
and caches/dedupes the record across every component on the page that
loads it, so two components showing the same record don't each issue
their own server round trip. Reserve Apex for what LDS cannot do:
multi-record operations, cross-object queries, aggregates, or
server-side business logic — never as the default path for
single-record CRUD just because it's the familiar pattern.

(id: `aura-lds`; source: Aura Components Developer Guide — "Lightning
Data Service")

## Migration direction

Converting an Aura component to LWC is a rewrite against the same
requirements, not a mechanical translation — check these before starting
so the LWC version doesn't quietly drop a capability the Aura version
had:

- **Feature parity**: every `<aura:attribute>` has a corresponding `@api`
  property; every `aura:if`/CSS-toggle branch and every `aura:iteration`
  has an equivalent `template if:true`/`for:each` block; anything
  relying on Aura-only markup (`aura:method`, `aura:valueChange`-style
  reactivity nuances) has a named LWC equivalent picked before the
  rewrite starts, not discovered mid-way.
- **Event contracts**: a component event becomes a `CustomEvent`
  dispatched from the child and listened for on the parent tag
  (`onrecordsaved`); an application event becomes Lightning Message
  Service, since LWC has no application-event equivalent. Every consumer
  of the Aura component's events — including any other Aura component
  still listening for them during a phased migration — is identified
  before the event names and payload shapes change underneath it.
- **`force:recordData` usage** maps to `lightning-record-form`/
  `lightning-record-edit-form` or `@wire(getRecord)`, depending on
  whether the Aura component used the base layout or built a custom one
  around LDS.
- **Consumer surfaces that can't host LWC directly**: an Aura component
  embedded inside a Visualforce page, an Aura tab, or another Aura
  component that itself isn't converting yet may need an Aura-to-LWC
  wrapper or bridging step rather than a straight swap.
- The full checklist, ready to run against a specific component, is in
  [reference/events.md](reference/events.md).

(id: `aura-migration`; source: Aura Components Developer Guide —
"Migrate from Aura to Lightning Web Components"; the checklist and its
consumer-surface item are this standard)

## Review severities

- **Critical**: business logic — a calculation, an
  eligibility or status rule — implemented in a component's controller
  or helper instead of delegated to Apex (`aura-controller-helper`); an
  application event fired where a component event would do, discovered
  by tracing an unnecessary cross-tree dependency (`aura-events`).
- **Important**: new Aura surface added with no named platform-forcing
  reason (Maintenance-first); an `<aura:attribute>` typed as `Object`
  with no justification (`aura-markup`); logic (a loop, a multi-line
  conditional, a direct Apex call) living in a controller action instead
  of a helper function (`aura-controller-helper`); an event payload
  carrying the whole record or firing component's state instead of the
  fields a handler actually needs (`aura-events`); a hand-written Apex
  method doing single-record CRUD that `force:recordData` could cover
  (`aura-lds`); a migration started without checking event-contract
  parity for existing consumers (`aura-migration`).
- **Minor**: an expression in markup performing inline arithmetic or
  concatenation instead of reading a precomputed attribute
  (`aura-markup`); `aura:if` used for a frequently-toggled, stateless
  visibility switch that CSS-class toggling would serve more cheaply
  (`aura-markup`); an event named after the firing component instead of
  what happened (`aura-events`).
