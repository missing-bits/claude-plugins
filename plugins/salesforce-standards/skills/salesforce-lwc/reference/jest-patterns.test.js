/**
 * Illustrative sfdx-lwc-jest tests for the ContactList component in
 * reference/component-patterns.js: a render assertion, a wire-adapter
 * mock (success and error), and an event-dispatch assertion.
 *
 * Real projects place this file at
 * lwc/contactList/__tests__/contactList.test.js — inside the component's
 * own bundle, next to contactList.js, per SKILL.md's test-placement rule.
 */
import { createElement } from 'lwc';
import ContactList from 'c/contactList';
import getContacts from '@salesforce/apex/ContactListController.getContacts';
import archiveContact from '@salesforce/apex/ContactListController.archiveContact';

// sfdx-lwc-jest auto-mocks @salesforce/apex/* imports; createApexTestWireAdapter
// swaps the wired Apex method for a controllable test double — `.emit(data)`
// drives the success path, `.error(message)` drives the error path — so a
// test never depends on a real Apex method executing against an org.
jest.mock(
    '@salesforce/apex/ContactListController.getContacts',
    () => {
        const { createApexTestWireAdapter } = require('@salesforce/sfdx-lwc-jest');
        return { default: createApexTestWireAdapter(jest.fn()) };
    },
    { virtual: true }
);

// The imperative Apex import is mocked as a plain jest function — no wire
// adapter involved, since archiveContact is called imperatively.
jest.mock(
    '@salesforce/apex/ContactListController.archiveContact',
    () => ({ default: jest.fn() }),
    { virtual: true }
);

const CONTACTS = [
    { Id: '003000000000001', Name: 'Jordan Lee' },
    { Id: '003000000000002', Name: 'Priya Nair' }
];

describe('c-contact-list', () => {
    afterEach(() => {
        // Every element created in a test must be torn down, or the next
        // test's assertions can see this test's leftover DOM.
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    // Render assertion: mount the component, push data through the mocked
    // wire adapter, then assert on the shadow DOM it produced. Reads
    // element.shadowRoot, never element directly — the template lives
    // inside the component's shadow boundary.
    it('renders one row per contact returned by the wire adapter', async () => {
        const element = createElement('c-contact-list', { is: ContactList });
        element.accountId = '001000000000001';
        document.body.appendChild(element);

        getContacts.emit(CONTACTS);
        // Wire emissions resolve on the microtask queue — flush it before
        // asserting on the DOM the component just re-rendered.
        await Promise.resolve();

        const rows = element.shadowRoot.querySelectorAll('[data-id]');
        // One <div> and one <lightning-button-icon> per contact.
        expect(rows).toHaveLength(CONTACTS.length * 2);
    });

    // Wire-adapter error path: emit an error instead of data and assert
    // the component falls back to its empty-state label rather than
    // throwing or rendering stale rows.
    it('shows the empty-state label when the wire adapter errors', async () => {
        const element = createElement('c-contact-list', { is: ContactList });
        element.accountId = '001000000000001';
        document.body.appendChild(element);

        getContacts.error('List has no rows for this object');
        await Promise.resolve();

        const emptyState = element.shadowRoot.querySelector('p');
        expect(emptyState).not.toBeNull();
        expect(element.shadowRoot.querySelectorAll('[data-id]')).toHaveLength(0);
    });

    // Event-dispatch assertion: a row click dispatches `select` — this
    // project's naming convention (short, lowercase, names the action).
    it('dispatches select with the clicked contact id', async () => {
        const element = createElement('c-contact-list', { is: ContactList });
        element.accountId = '001000000000001';
        document.body.appendChild(element);

        getContacts.emit(CONTACTS);
        await Promise.resolve();

        const selectHandler = jest.fn();
        element.addEventListener('select', selectHandler);

        const firstRow = element.shadowRoot.querySelector('[data-id]');
        firstRow.click();

        expect(selectHandler).toHaveBeenCalledTimes(1);
        expect(selectHandler.mock.calls[0][0].detail.contactId).toBe(
            CONTACTS[0].Id
        );
    });

    // Imperative-Apex assertion: archiving calls the mocked imperative
    // method directly (no wire adapter involved) and, on success,
    // dispatches `rowaction` describing what happened.
    it('dispatches rowaction after a successful archive', async () => {
        archiveContact.mockResolvedValue();
        const element = createElement('c-contact-list', { is: ContactList });
        element.accountId = '001000000000001';
        document.body.appendChild(element);

        getContacts.emit(CONTACTS);
        await Promise.resolve();

        const rowActionHandler = jest.fn();
        element.addEventListener('rowaction', rowActionHandler);

        const archiveButton = element.shadowRoot.querySelectorAll('[data-id]')[1];
        archiveButton.click();
        // Two microtask flushes: one for the awaited archiveContact call,
        // one for the awaited refreshApex call that follows it.
        await Promise.resolve();
        await Promise.resolve();

        expect(archiveContact).toHaveBeenCalledWith({
            contactId: CONTACTS[0].Id
        });
        expect(rowActionHandler).toHaveBeenCalledTimes(1);
        expect(rowActionHandler.mock.calls[0][0].detail).toEqual({
            action: 'archive',
            contactId: CONTACTS[0].Id
        });
    });
});
