# Aura events: worked examples and migration checklist

Two event kinds, side by side, with the decision rule annotated at each
step — then a checklist for assessing an Aura-to-LWC conversion.

## Decision rule

> Is the component that needs to react the direct container of the
> component that fires the event, inside the same containment tree?
>
> - **Yes** → component event. It reaches only that direct container —
>   an indirect ancestor needs its own attribute wiring on the
>   intermediate component, or a re-fire, since it doesn't bubble further
>   on its own.
> - **No** (siblings, unrelated parts of the page, no containment
>   relationship to exploit) → application event, and only then. Every
>   handler anywhere in the app receives it, so this is the wider,
>   costlier tool — reach for it because the component event genuinely
>   cannot reach the listener, not because it is easier to wire up.

## Component event: registration, firing, handling

A child component reports that a record was saved; its parent (anywhere
up its containment tree) reacts by refreshing its own data.

**1. Define the event** (`c/recordSaved.evt`):

```xml
<aura:event type="COMPONENT" description="Fired when a record has been saved">
    <aura:attribute name="recordId" type="Id"/>
</aura:event>
```

Decision-rule note: `type="COMPONENT"` is the whole scoping decision —
this event can only be handled by something in the firing component's
own tree.

**2. Register it on the firing component** (`c/recordEditForm.cmp`):

```xml
<aura:component>
    <aura:attribute name="recordId" type="Id"/>
    <aura:registerEvent name="recordSaved" type="c:recordSaved"/>
    <lightning:button label="Save" onclick="{!c.handleSave}"/>
</aura:component>
```

**3. Fire it from the controller/helper** (`recordEditFormController.js`):

```javascript
({
    handleSave: function (component, event, helper) {
        helper.saveRecord(component).then(function (savedId) {
            var saveEvent = component.getEvent("recordSaved");
            saveEvent.setParams({ recordId: savedId });
            saveEvent.fire();
        });
    }
})
```

Payload discipline note: the event carries only `recordId` — the one
thing a handler needs to act (e.g. refresh that record), not the whole
saved record or the form component's internal state.

**4. Handle it on the parent** (`c/recordListPanel.cmp`):

```xml
<aura:component>
    <c:recordEditForm recordId="{!v.selectedId}" recordSaved="{!c.handleRecordSaved}"/>
</aura:component>
```

```javascript
({
    handleRecordSaved: function (component, event, helper) {
        var savedId = event.getParam("recordId");
        helper.refreshList(component, savedId);
    }
})
```

The handler is wired as an attribute on the child tag
(`recordSaved="{!c.handleRecordSaved}"`) — this only works because the
parent directly contains the child; there is no separate subscribe step
the way an application event needs.

## Application event: registration, firing, handling

Two unrelated components on the same Lightning page — a filter panel and
a report widget dropped independently onto the page — need to stay in
sync on a selected date range. Neither contains the other, so a
component event cannot reach across; this is the genuine cross-tree case.

**1. Define the event** (`c/dateRangeChanged.evt`):

```xml
<aura:event type="APPLICATION" description="Fired when the selected date range changes">
    <aura:attribute name="startDate" type="Date"/>
    <aura:attribute name="endDate" type="Date"/>
</aura:event>
```

Decision-rule note: `type="APPLICATION"` — chosen here only because the
filter panel and the report widget have no containment relationship;
if the report widget were nested inside the filter panel, this would be
a component event instead.

**2. Fire it from the filter panel's controller**
(`filterPanelController.js`):

```javascript
({
    handleRangeSelected: function (component, event, helper) {
        var rangeEvent = $A.get("e.c:dateRangeChanged");
        rangeEvent.setParams({
            startDate: component.get("v.startDate"),
            endDate: component.get("v.endDate")
        });
        rangeEvent.fire();
    }
})
```

**3. Handle it in the report widget** — registered declaratively in
markup, not `$A.get`, so every instance of the widget on the page picks
it up (`c/reportWidget.cmp`):

```xml
<aura:component>
    <aura:handler event="c:dateRangeChanged" action="{!c.handleRangeChanged}"/>
</aura:component>
```

```javascript
({
    handleRangeChanged: function (component, event, helper) {
        var startDate = event.getParam("startDate");
        var endDate = event.getParam("endDate");
        helper.refreshReport(component, startDate, endDate);
    }
})
```

Blast-radius note: because this is an application event, *any* other
component on the page with a matching `<aura:handler event="c:dateRangeChanged">`
also receives it — that reach is the cost being paid for crossing the
containment boundary, and is exactly why a component event is preferred
whenever containment already provides the path.

## Migration-assessment checklist: Aura → LWC

Run this against one component before converting it. An unchecked item
is a named gap to resolve before or during the rewrite, not a surprise
found after.

- [ ] **Attributes**: every `<aura:attribute>` has a target `@api`
      property of an equivalent type; any attribute with a `default`
      value carries that default into the LWC property.
- [ ] **Conditional markup**: every `aura:if` branch and every
      CSS-class-toggle branch has an equivalent `template if:true`/
      `if:false` (or a computed CSS-class getter) in the LWC template.
- [ ] **Iteration**: every `aura:iteration` has an equivalent `for:each`
      (or `iterator:it`) with a `key` attribute on the repeated element.
- [ ] **Component events**: each one has an identified `CustomEvent`
      name and payload (`detail`), and every parent currently listening
      via `<aura:handler>`/attribute wiring is identified so its LWC
      counterpart listens the same way (`on<eventname>` on the child
      tag).
- [ ] **Application events**: each one has an identified Lightning
      Message Service channel, with every current `<aura:handler
      event="...">` listener identified so it gets a matching
      `subscribe` (and a matching `unsubscribe` in
      `disconnectedCallback`).
- [ ] **`force:recordData` usage**: mapped to `lightning-record-form`/
      `lightning-record-edit-form` (base layout) or `@wire(getRecord)`
      plus `updateRecord`/`deleteRecord` (custom layout), matching
      whichever the Aura component actually needed.
- [ ] **Apex methods called**: each `@AuraEnabled` method's signature is
      unchanged (or its call sites are updated); methods used as
      `@wire` targets are `cacheable=true` and perform no DML.
- [ ] **Consumer surfaces**: every place the Aura component is currently
      embedded (a Visualforce page, an Aura tab, another Aura component
      not yet converting) is identified — a surface that cannot host
      LWC directly needs a bridging plan, not a straight swap.
- [ ] **Styling**: any custom CSS is re-expressed against SLDS classes
      and styling hooks per `salesforce-lwc`'s styling standard, not
      copied over verbatim from the Aura component's stylesheet.
- [ ] **Tests**: existing coverage of the Aura component's behavior
      (manual test scripts, any Selenium/UI tests) has an LWC jest
      equivalent planned before the Aura version is retired — see
      `salesforce-lwc`'s jest-testing section.
