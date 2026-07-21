/**
 * Illustrative LWC controller demonstrating the patterns from SKILL.md:
 * wire vs imperative Apex, cacheable guidance, custom labels, private
 * class fields, and event dispatch using this project's event-naming
 * convention (short lowercase noun/verb: `select`, `rowaction`).
 *
 * Bundle: lwc/contactList/contactList.js (this file) plus the sibling
 * files a real bundle needs — contactList.html, contactList.js-meta.xml,
 * and __tests__/contactList.test.js (see reference/jest-patterns.test.js
 * for the matching tests).
 *
 * Matching HTML template (contactList.html), sketched here rather than
 * as a fourth reference file since this reference is JS-focused. Every
 * identifier referenced from the template below (cardTitle, contacts,
 * labels, handleRowSelect, handleArchive) is defined in the class:
 *
 * <template>
 *   <lightning-card title={cardTitle} icon-name="standard:contact">
 *     <template if:true={contacts.length}>
 *       <template for:each={contacts} for:item="contact">
 *         <div key={contact.Id} class="slds-p-around_small slds-grid"
 *              data-id={contact.Id} onclick={handleRowSelect}>
 *           <span class="slds-col">{contact.Name}</span>
 *           <lightning-button-icon icon-name="utility:delete"
 *                                   data-id={contact.Id}
 *                                   onclick={handleArchive}>
 *           </lightning-button-icon>
 *         </div>
 *       </template>
 *     </template>
 *     <template if:true={wireError}>
 *       <p class="slds-text-body_small slds-text-color_error">
 *         {labels.wireErrorMessage}
 *       </p>
 *     </template>
 *     <template if:false={contacts.length}>
 *       <template if:false={wireError}>
 *         <p class="slds-text-body_small slds-text-color_weak">
 *           {labels.noContactsFound}
 *         </p>
 *       </template>
 *     </template>
 *   </lightning-card>
 * </template>
 */
import { LightningElement, api, wire } from 'lwc';
import { refreshApex } from '@salesforce/apex';
import getContacts from '@salesforce/apex/ContactListController.getContacts';
import archiveContact from '@salesforce/apex/ContactListController.archiveContact';
import noContactsFound from '@salesforce/label/c.No_Contacts_Found';
import contactListTitle from '@salesforce/label/c.Contact_List_Title';
import wireErrorMessage from '@salesforce/label/c.Contact_List_Wire_Error';

export default class ContactList extends LightningElement {
    // @api: the component's public contract. A parent supplies which
    // Account to list contacts for; that is the entire public surface —
    // nothing about how the list is fetched or rendered leaks out.
    @api accountId;

    // Every user-facing string is a custom label, never a literal in the
    // template or here.
    labels = {
        noContactsFound,
        wireErrorMessage,
        cardTitle: contactListTitle
    };

    // True private state via a JS private class field — inaccessible from
    // outside this class, unlike an `_wiredContactsResult` naming
    // convention would be. The template never reads this field directly;
    // it reads the `contacts` getter below.
    #wiredContactsResult;

    // wire for a reactive read: getContacts is cacheable=true (it runs no
    // DML), so the wire service can cache and dedupe it across every
    // component instance requesting the same accountId, and re-run it
    // automatically whenever accountId changes — no manual refresh call
    // to write or forget. The full result (data AND error) is kept, not
    // just result.data — a wire error must stay distinguishable from a
    // genuine empty list rather than falling through to it, mirroring the
    // try/catch below on the imperative path.
    @wire(getContacts, { accountId: '$accountId' })
    wiredContacts(result) {
        this.#wiredContactsResult = result;
    }

    get contacts() {
        return this.#wiredContactsResult?.data ?? [];
    }

    // Exposes the wire error separately so the template can render a
    // dedicated error state instead of silently reusing the "no contacts"
    // empty state for both a genuinely empty list and a failed fetch.
    get wireError() {
        return this.#wiredContactsResult?.error;
    }

    get cardTitle() {
        return this.labels.cardTitle;
    }

    // Custom event up: `select` is a short lowercase noun naming the
    // action, not `oncontactselect` or `onRowSelected` — the platform
    // lowercases event names regardless, and the listening side adds its
    // own `on` prefix.
    handleRowSelect(event) {
        const contactId = event.currentTarget.dataset.id;
        this.dispatchEvent(
            new CustomEvent('select', { detail: { contactId } })
        );
    }

    // Imperative Apex: archiving performs DML and is triggered by one
    // specific click rather than being naturally reactive to the
    // component's own properties — imperative, not wire. Always wrapped
    // in try/catch so a rejected promise never fails silently.
    async handleArchive(event) {
        event.stopPropagation();
        const contactId = event.currentTarget.dataset.id;
        try {
            await archiveContact({ contactId });
            // `rowaction` names the outcome of a row-scoped action, kept
            // distinct from `select` (which only signals which row was
            // chosen, not that something happened to it).
            this.dispatchEvent(
                new CustomEvent('rowaction', {
                    detail: { action: 'archive', contactId }
                })
            );
            await refreshApex(this.#wiredContactsResult);
        } catch (error) {
            this.dispatchEvent(
                new CustomEvent('rowaction', {
                    detail: { action: 'archive-error', contactId, error }
                })
            );
        }
    }
}
