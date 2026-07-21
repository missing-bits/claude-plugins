---
name: salesforce-lwc
description: Use when building or reviewing Lightning Web Components — file and component structure, JavaScript conventions, wire vs imperative Apex, custom labels, component communication (events, Lightning Message Service), styling, and jest tests with sfdx-lwc-jest. New UI belongs here; Aura maintenance belongs to salesforce-aura.
---

# Salesforce LWC

Standards for building and reviewing Lightning Web Components: bundle
structure, JavaScript conventions, Apex integration, communication,
styling, and jest testing with `sfdx-lwc-jest`. Cite rules in review
findings as `(standard: salesforce-lwc, rule: <id>)`; each rule names its
source (the LWC Developer Guide, the `sfdx-lwc-jest` docs, or `this
standard` for a recorded house decision). All new UI work targets LWC;
Aura components are maintenance-only — see `salesforce-aura` for that
boundary. Apex-side layering (handler/service/selector) is
`salesforce-apex`'s concern; this skill covers only the shape of the
Apex methods an LWC calls (`@AuraEnabled`, `cacheable`).

## File and component structure

- **Bundle layout**: one folder per component holding
  `<name>.js` (the controller), `<name>.html` (the template), and
  `<name>.js-meta.xml` (exposure/targets metadata); `<name>.css` only
  when the component needs custom styling; a `__tests__/` folder for its
  jest tests.
- **Folders**: platform default — a flat `lwc/` directory, one folder per
  component, no feature-based sub-grouping layered on top, for
  consistency with the platform's own generators
  (`sf lightning generate component`).
- **Naming**: the folder and the exported class are both **camelCase**
  (`contactList`, `class ContactList`); markup usage is **kebab-case**
  with the namespace prefix (`<c-contact-list>`).
- **One component, one responsibility.** E.g. a component rendering a
  list *and* owning a separate modal's full edit form is two
  responsibilities — split into a parent (list, selection) and a child
  (the edit form), connected by `@api` properties down and a custom event
  up. Split when a template accumulates more than one reason to change,
  not on a line-count threshold.

(id: `lwc-structure`; source: LWC Developer Guide — "Create a Lightning
Web Component"; folder-flatness and one-responsibility are this standard)

## JavaScript conventions

- **Modern ES modules** — `import`/`export`, classes extending
  `LightningElement`; no `require`, no global namespace pollution.
- **True private state as private class fields** (`#internalState`), not
  a `_prefixed` convention — a `#field` is genuinely inaccessible, where
  an underscore is only a naming hint. Expose a getter for whatever
  derived value the template needs; never the private field itself.
- **No DOM manipulation outside the component's own shadow boundary.**
  `this.template.querySelector(...)` reads the component's own rendered
  markup; a component never reaches into `document` for another
  component's DOM or a page-level element. Cross-component effects go
  through `@api` properties, events, or Lightning Message Service (see
  "Component communication"), never a shared DOM reference.
- **`@api`**: the component's public contract — properties and methods a
  parent is allowed to set or call. Keep this surface minimal and named
  for what the caller supplies (`accountId`), not for an internal
  implementation detail.
- **`@track`**: needed only when a property holds an object or array
  mutated in place (a nested field changed, an item pushed) rather than
  reassigned — wholesale reassignment is already reactive without it.
  `@track` on every property signals the component is mutating state it
  should instead be replacing.
- **`@wire`**: see the next section.

(id: `lwc-js-conventions`; source: LWC Developer Guide — "JavaScript
Fundamentals", "Reactivity"; the private-fields-over-underscore-prefix
stance is this standard)

## wire vs imperative Apex

- **`@wire` for reactive reads.** An Apex method whose result the
  component simply displays — a record, a related list — is wired: LWC
  re-invokes it automatically whenever a reactive parameter (`$accountId`)
  changes, with no manual refresh call to write or forget.
- **Imperative (`await someApexMethod(params)`) for actions and
  parameterized one-shots.** DML, a callout, or any call triggered by a
  specific user action (a button click, a save) is imperative — it isn't
  naturally reactive to the component's own properties, and running it as
  a side effect of a wire would be surprising. Wrap every imperative call
  in `try`/`catch`; an uncaught rejected promise fails silently in the
  console instead of reaching the user.
- **`cacheable=true`** on the Apex method only when it **performs no
  DML** and is safe to serve from cache across components requesting the
  same parameters — this is what makes it eligible to be `@wire`d. A
  method that writes data is never `cacheable=true`, and is therefore
  always called imperatively, never wired.
- Both patterns, side by side, are in
  [reference/component-patterns.js](reference/component-patterns.js).

(id: `lwc-wire-vs-imperative`; source: LWC Developer Guide — "Call Apex
Methods", "Wire Service"; Apex Developer Guide — "Using
`@AuraEnabled(cacheable=true)`")

## Custom labels

**Every user-facing string is a custom label** (`import someLabel from
'@salesforce/label/c.SomeLabel'`) — a template or JS file never contains
a hardcoded UI string (button text, an error message, an empty-state
sentence): a label can be translated and edited without a code
deployment, a hardcoded string can't. The one exception is a string
that is genuinely not user-facing — a CSS class name, a `data-*`
attribute value, a console-only debug message.

(id: `lwc-custom-labels`; source: LWC Developer Guide — "Access Static
Text with Custom Labels")

## Component communication

- **Custom events up, properties down.** A child never calls a method on
  its parent and never reaches up the DOM tree — it dispatches a
  `CustomEvent` and lets whatever is listening decide what to do; a
  parent hands data down only through the child's `@api` properties.
- **Event naming**: a short, lowercase noun or verb naming the action or
  outcome, not the implementation — `select`, `rowaction`, `valuechange`.
  The platform lowercases event names and the listener adds its own `on`
  prefix (`onselect`), so an event never carries an `on` prefix itself;
  camelCase (`onRowAction`) gets silently lowercased anyway.
- **Lightning Message Service (LMS)** for communication that crosses the
  DOM hierarchy — components with no parent/child relationship, sibling
  components dropped onto the same page independently, or an
  LWC-to-Aura bridge. Define a message channel, `publish` from the
  sender, `subscribe` in the receiver's `connectedCallback`, and always
  `unsubscribe` in `disconnectedCallback` — a forgotten unsubscribe keeps
  a destroyed component receiving messages it can no longer act on.
- Event dispatch (`select`, `rowaction`) is demonstrated in
  [reference/component-patterns.js](reference/component-patterns.js).

(id: `lwc-communication`; source: LWC Developer Guide — "Custom Events",
"Lightning Message Service"; the event-naming convention is this
standard)

## Styling

**SLDS utility classes and styling hooks (design tokens) are the base for
every component's styling.** Reach for a class (`slds-grid`,
`slds-p-around_medium`) or a styling hook
(`--slds-c-button-color-background`) before writing any custom CSS —
they track the platform's design system automatically, including theme
changes a hand-rolled color value would silently miss.

- **Custom CSS only where SLDS genuinely cannot express the need** — a
  layout SLDS has no utility for, a one-off visual detail no styling hook
  exposes. When it is used, add a short comment in the CSS (or the JS
  right above the class usage) stating *why* SLDS couldn't cover it, so a
  later reviewer isn't left guessing whether the custom rule was actually
  necessary or just convenient.
- A component's `.css` file, when present, styles only that component's
  own shadow DOM — never a global selector reaching outside it.

(id: `lwc-styling`; source: LWC Developer Guide — "Style Components with
SLDS"; the custom-CSS-needs-justification stance is this standard)

## Jest tests with sfdx-lwc-jest

**Jest testing for LWC lives here — `salesforce-apex-testing` is
Apex-only.** `sfdx-lwc-jest` runs component tests against a lightweight
DOM (jsdom), auto-mocking `@salesforce/*` scoped imports so a test never
needs a real org.

- **Test file placement**: inside the component's own bundle, in a
  `__tests__/` folder next to the component's `.js` file —
  `lwc/contactList/__tests__/contactList.test.js` for `contactList.js` —
  so the test moves, renames, or gets deleted with the component instead
  of drifting out of sync in a separate tree.
- **DOM assertions**: `createElement` from `lwc` builds the component,
  `document.body.appendChild` mounts it, and assertions read
  `element.shadowRoot.querySelector`/`querySelectorAll` — never
  `element.querySelector` directly, since the component's markup lives
  inside its shadow root. Any state change triggering a re-render (a wire
  emission, a property set after mount) needs an
  `await Promise.resolve()` (or a small microtask-flushing helper) before
  the next assertion, since LWC re-renders on the microtask queue, not
  synchronously.
- **Mocking wire adapters**: `jest.mock` the `@salesforce/apex/...` wire
  import and replace it with `createApexTestWireAdapter` (or
  `registerApexTestWireAdapter`, from `@salesforce/sfdx-lwc-jest`), then
  drive it with `.emit(data)` for the success path or `.error(message)`
  for the error path — a test never depends on a real Apex method
  executing.
- A full example — render, a wire-adapter mock (success and error), and
  an event-dispatch assertion — is
  [reference/jest-patterns.test.js](reference/jest-patterns.test.js).

(id: `lwc-jest`; source: `sfdx-lwc-jest` documentation — "Writing
Lightning Web Components Tests")

## Placement: component bundles vs static resources

**Application JavaScript lives in component bundles; static resources
are for third-party libraries and assets** — never for a component's own
logic. Use a static resource to vendor a third-party JS/CSS library
loaded via `loadScript`/`loadStyle` (a charting library, a PDF renderer),
or to hold non-code assets (images, PDFs, fonts). A component's own
behavior — anything this skill's JavaScript conventions govern — belongs
in its bundle's `.js` file, not smuggled into a static resource as a
script the bundle merely loads.

(id: `lwc-placement`; source: this standard)

## Review severities

- **Critical**: an Apex method marked `cacheable=true` that performs DML
  (`lwc-wire-vs-imperative`); a hardcoded user-facing string in a
  template or JS file (`lwc-custom-labels`); DOM access reaching outside
  the component's own shadow root, including into another component's
  markup (`lwc-js-conventions`).
- **Important**: an imperative Apex call with no `try`/`catch`
  (`lwc-wire-vs-imperative`); a custom event named with an `on` prefix or
  camelCase instead of a short lowercase noun/verb
  (`lwc-communication`); custom CSS with no in-code justification comment
  (`lwc-styling`); an LMS `subscribe` with no matching `unsubscribe` in
  `disconnectedCallback` (`lwc-communication`); component logic placed in
  a static resource instead of the bundle (`lwc-placement`).
- **Minor**: `@track` used on a property that is only ever reassigned,
  never mutated in place (`lwc-js-conventions`); a jest test asserting via
  `element.querySelector` instead of `element.shadowRoot.querySelector`
  (`lwc-jest`); folder or naming convention deviations
  (`lwc-structure`).
