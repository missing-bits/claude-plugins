---
name: salesforce-visualforce
description: Use when maintaining existing Visualforce pages — standard controllers, extensions, custom controllers, view state discipline, and data binding. Maintenance-first; new UI belongs to salesforce-lwc unless the platform forces Visualforce (e.g. PDF rendering).
---

# Salesforce Visualforce

**Maintenance-first.** Existing Visualforce pages are held to every
standard here — being legacy is not a pass on quality. New UI is built
in LWC, never Visualforce, unless the platform genuinely forces it
(canonical case: PDF rendering via `renderAs="pdf"`, which LWC cannot
do). New Visualforce surface with no named platform-forcing reason is
itself a review finding — "the team already knows Visualforce" or "the
existing page is Visualforce" don't count; only a concrete platform gap
does. See `salesforce-lwc` for where new UI work belongs.

(id: `vf-maintenance-first`; severity: important; source: this
standard)

Cite rules in review findings as `(standard: salesforce-visualforce,
rule: <id>)`; each rule names its source — the Visualforce Developer
Guide, or `this standard` (a recorded house decision).

## Controller choice ladder

Three rungs, climbed only as far as the page's actual data shape
requires — each step up trades away automatic behavior the rung below
gave for free, so justify the step, don't default to it.

- **Standard controller** (`standardController="Account"`) is the
  default and stays the default until requirements exceed it. Reach for
  it alone when the page's data need is exactly what the platform
  generates for free: display, edit, or delete a single record, its
  standard related lists, and standard Save/Cancel/Delete behavior —
  nothing beyond what the record and its declared relationships already
  expose.
- **Standard controller + extension**
  (`extensions="AccountSummaryExtension"`) is justified the moment the
  page needs data or behavior the standard controller doesn't expose —
  an aggregate computed from related records, a custom action, extra
  validation before save — while the base record context, standard
  relationships, and default Save/Cancel semantics are still useful and
  worth keeping. The extension's constructor takes an
  `ApexPages.StandardController` and augments it; it does not replace
  the record the standard controller already manages.
- **Custom controller** (`controller="MyController"`) is justified only
  when the page's data shape diverges from a single record entirely —
  a multi-object wizard, a page not backed by any one record (a
  dashboard, a calculation-only page), or logic that needs full control
  over query, transaction, and navigation. This drops every standard
  controller behavior — the page implements query, save, and navigation
  itself. Reach for it only when standard controller + extension
  genuinely can't express the page, not as a default starting point.

One worked example per rung — including the Apex for the extension and
custom-controller rungs — is in
[reference/controller-patterns.md](reference/controller-patterns.md).

(id: `vf-controller-ladder`; severity: important; source: Visualforce
Developer Guide — "Standard Controllers", "Custom Controllers and
Controller Extensions"; the step-justification framing is this
standard)

Sub-rules:
- an extension used where standard controller alone would have
  sufficed (id: `vf-controller-ladder.needless-extension`; severity:
  minor)

## View state discipline

**View state exists only on a page that contains `apex:form`** — it
carries postback state (the controller's field values) across that
form's submits. A form-less page (read-only, never posts back) has no
view state to discipline; everything below applies only to pages built
around `apex:form`.

On a page with a form, every non-transient property on the controller
(standard, extension, or custom) is serialized into the view state on
each request/response round trip. The view state has a fixed platform
limit — treat it as a design constraint from the start, not an incident
to react to once a page starts failing.

- **Mark computed and reconstructable data `transient`.** A cache,
  a lazily-computed value, or any collection that can be refetched or
  recomputed from a small piece of durable state (a record Id, a page
  number) does not need to survive in the view state — mark it
  `transient` and recompute it inside the getter or action method that
  needs it.
- **Keep the durable state to the minimum that must survive a
  postback** — a page number, a selected record Id, a wizard step
  index — not the query results or derived collections computed from
  it. If a value can be re-derived from something smaller that is
  already kept, keep the smaller thing and derive the value again on
  the next request.
- **Treat the view state limit as a design input, not an
  afterthought.** Visualforce caps view state at **170 KB per page**
  (Visualforce Developer Guide, "View State") — a fixed ceiling. A
  controller already holding a large result set, a wide related-record
  map, or several independent query results in non-transient properties
  will hit that ceiling as data grows — the fix is pagination, targeted
  queries, and `transient` caching designed in from the start, not a
  cleanup once the page starts erroring.

A before/after pair — a controller carrying unrelated query results in
plain properties, reduced to the one scalar it actually needs to persist
— is annotated in
[reference/controller-patterns.md](reference/controller-patterns.md).

(id: `vf-view-state`; severity: important; source: Visualforce Developer
Guide — "View State", "Reducing View State Size"; the durable-vs-transient
framing is this standard)

## Data binding

- **Bind through controller properties, not inline logic.** A page
  expression (`{!account.Name}`, `{!openPipelineTotal}`) reads a single
  controller property — not a multi-step conditional, arithmetic, or a
  side-effecting method call. Compute a derived or formatted value once
  in a controller getter and bind to that property directly; logic
  embedded in a page expression hides behavior from review and can't be
  unit-tested the way a controller method can. This does not ban a
  single-comparison `rendered`/`disabled` toggle
  (`rendered="{!currentStep == 1}"`, `disabled="{!isReadOnly}"`) — a
  plain comparison or boolean read driving whether a block shows or an
  input is enabled is idiomatic Visualforce control flow. What the rule
  bans is expression logic that *computes a displayed value* —
  arithmetic, string-building, or a multi-step conditional standing in
  for a controller property that should have carried that computed
  value in the first place.
- **`apex:repeat` (and `apex:pageBlockTable`/`apex:dataTable`) iterate
  over an already-fetched collection, never a getter that re-queries per
  call.** Visualforce's rendering lifecycle can invoke a bound getter
  more than once per request, so a getter that issues SOQL and is bound
  directly as a repeat's `value` turns one page render into a
  once-per-render (or per-row) query. Fetch the collection once — in the
  constructor, an action method, or a `transient`-cached getter — and
  bind the repeat to that already-populated property.

(id: `vf-data-binding`; severity: important; source: Visualforce
Developer Guide — "Expression Language", "Using apex:repeat"; the
getter-caching discipline is this standard)

Sub-rules:
- a page expression performing inline arithmetic or a multi-step
  conditional instead of reading a precomputed controller property (id:
  `vf-data-binding.inline-expression`; severity: minor)

## Security

- **`escape="false"` requires a stated justification.** Any output
  component (`apex:outputText`, `apex:outputField` and similar) rendered
  with `escape="false"` skips HTML-escaping and renders its value as raw
  markup — if that value can ever contain user-supplied or externally
  sourced content, this is a stored or reflected XSS opening. Use
  `escape="false"` only for content that is genuinely trusted or already
  sanitized (a rich-text field the platform itself sanitizes, static
  admin-authored markup), and record why the value is safe to render
  unescaped as a comment next to the attribute. No justification
  recorded is a review finding regardless of whether the current data
  happens to be safe.
- **Field-level security (FLS) is deferred to the security-model
  standards, not restated here** — see `salesforce-security-model` for
  how FLS is enforced at the query/DML boundary inside a custom
  controller or extension's Apex. A Visualforce controller that queries
  or saves business/sensitive data in system context with none of that
  enforcement in place is a finding under that skill, not a separate
  Visualforce-specific rule. System-context FLS in a controller or
  extension is graded by `security-fls` (salesforce-security-model).

(id: `vf-security`; severity: critical; kind: defect; source:
Visualforce Developer Guide — "Preventing Cross-Site Scripting (XSS)";
the justification requirement is this standard; FLS mechanics:
`salesforce-security-model`)
