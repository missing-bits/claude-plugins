/**
 * Single source of test records for this org's test classes.
 *
 * One builder per object, each with:
 *   - a plain overload (`createX(Integer count)`) that applies sensible
 *     defaults only;
 *   - an override overload (`createX(Integer count, Map<String, Object>
 *     fieldOverrides)`) that applies the same defaults, then layers the
 *     caller's field values on top before insert.
 *
 * No test method should ever build an SObject inline with `new Account(...)`
 * — call a builder here instead, so a schema change (a new required field,
 * a renamed picklist value) is fixed in one place instead of in every test
 * file that happens to construct that object.
 *
 * `@IsTest` marks this class visible only to test context — it does not
 * count against the org's Apex code size limit, and cannot be called from
 * non-test code.
 */
@IsTest
public class TestDataFactory {

    /**
     * Creates `count` Accounts with sensible defaults, inserted and returned.
     */
    public static List<Account> createAccounts(Integer count) {
        return createAccounts(count, new Map<String, Object>());
    }

    /**
     * Creates `count` Accounts with sensible defaults, then applies
     * `fieldOverrides` on top of every record before insert — e.g.
     * `createAccounts(1, new Map<String, Object>{ 'Industry' => 'Banking' })`.
     */
    public static List<Account> createAccounts(Integer count, Map<String, Object> fieldOverrides) {
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < count; i++) {
            Account acc = new Account(
                Name = 'Test Account ' + i,
                Industry = 'Technology'
            );
            applyOverrides(acc, fieldOverrides);
            accounts.add(acc);
        }
        insert accounts;
        return accounts;
    }

    /**
     * Creates `count` Orders for the given Account with sensible defaults,
     * inserted and returned.
     */
    public static List<Order> createOrders(Integer count, Id accountId) {
        return createOrders(count, accountId, new Map<String, Object>());
    }

    /**
     * Creates `count` Orders for the given Account with sensible defaults,
     * then applies `fieldOverrides` on top of every record before insert —
     * e.g. `createOrders(1, acc.Id, new Map<String, Object>{ 'Status' => 'Activated' })`.
     */
    public static List<Order> createOrders(Integer count, Id accountId, Map<String, Object> fieldOverrides) {
        List<Order> orders = new List<Order>();
        for (Integer i = 0; i < count; i++) {
            Order ord = new Order(
                AccountId = accountId,
                EffectiveDate = Date.today(),
                Status = 'Draft'
            );
            applyOverrides(ord, fieldOverrides);
            orders.add(ord);
        }
        insert orders;
        return orders;
    }

    /**
     * Applies each override onto the record by field API name. Generic
     * across every builder above — adding a new object builder never
     * requires a new override mechanism.
     */
    private static void applyOverrides(SObject record, Map<String, Object> fieldOverrides) {
        for (String fieldName : fieldOverrides.keySet()) {
            record.put(fieldName, fieldOverrides.get(fieldName));
        }
    }
}
