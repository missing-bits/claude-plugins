/**
 * Worked example of the patterns in SKILL.md, testing an illustrative
 * `OrderService` / `OrderDomain` pair (the same Order fulfillment scenario
 * as salesforce-apex's reference/trigger-handler.md): activating an Order
 * inserts one fulfillment Task per Order, and an Order can only move to
 * "Activated" from "Draft" — moving to "Activated" from any other status
 * (e.g. "Cancelled") throws.
 *
 * Naming: `<Class>Test` — this file is named test-patterns.cls because it
 * bundles three independent scenarios for the skill's reference material,
 * but a real test class in your org is named for the one class it tests,
 * e.g. `OrderServiceTest`.
 *
 * Every record comes from TestDataFactory — no inline `new Account(...)`
 * or `new Order(...)` in any test method.
 */
@IsTest
private class OrderServiceTest {

    @TestSetup
    static void setupTestData() {
        // Shared across every test method below; each method gets its own
        // rolled-back copy of this data since @TestSetup runs once per method.
        TestDataFactory.createAccounts(1);
    }

    /**
     * Bulk-path test: 200 records, Test.startTest/stopTest around the
     * action only, asserting the actual resulting state (Task count) —
     * not just that activateFulfillment() ran without throwing.
     */
    @IsTest
    static void activateFulfillment_createsOneTaskPerActivatedOrder() {
        // Arrange
        Account acc = [SELECT Id FROM Account LIMIT 1];
        List<Order> activatedOrders = TestDataFactory.createOrders(
            200,
            acc.Id,
            new Map<String, Object>{ 'Status' => 'Activated' }
        );

        // Act
        Test.startTest();
        OrderService.activateFulfillment(activatedOrders);
        Test.stopTest();

        // Assert
        Set<Id> orderIds = new Map<Id, Order>(activatedOrders).keySet();
        Integer taskCount = [SELECT COUNT() FROM Task WHERE WhatId IN :orderIds];
        Assert.areEqual(
            200, taskCount,
            'Expected exactly one fulfillment Task per activated Order.'
        );
    }

    /**
     * Negative test: asserts a specific thrown exception type and message,
     * not merely that "an exception happened."
     */
    @IsTest
    static void validateStatusTransitions_throwsWhenActivatingFromCancelled() {
        // Arrange
        Account acc = [SELECT Id FROM Account LIMIT 1];
        List<Order> cancelledOrders = TestDataFactory.createOrders(
            1,
            acc.Id,
            new Map<String, Object>{ 'Status' => 'Cancelled' }
        );
        Order cancelledOrder = cancelledOrders[0];

        // oldMap must reflect the pre-change state, so clone before mutating —
        // otherwise the "old" record and the "new" record are the same object.
        Map<Id, Order> oldMap = new Map<Id, Order>{ cancelledOrder.Id => cancelledOrder.clone(true) };
        Order movedToActivated = cancelledOrder.clone(true);
        movedToActivated.Status = 'Activated';

        // Act & Assert — Test.stopTest() must run whether or not the action
        // throws, so it brackets the try/catch rather than sitting inside it.
        Test.startTest();
        try {
            OrderDomain.validateStatusTransitions(new List<Order>{ movedToActivated }, oldMap);
            Assert.fail('Expected an OrderProcessingException when activating an Order from Cancelled.');
        } catch (OrderProcessingException e) {
            Assert.isTrue(
                e.getMessage().contains('cannot move from Cancelled to Activated'),
                'Exception message should explain the invalid transition; got: ' + e.getMessage()
            );
        }
        Test.stopTest();
    }

    /**
     * Callout test: Test.setMock intercepts the HTTP callout, so no real
     * request ever leaves the org. PricingIntegrationService is illustrative
     * — substitute whatever class in your codebase actually issues the
     * callout; the Test.setMock + inner HttpCalloutMock shape is the point.
     */
    @IsTest
    static void fetchExternalPrice_returnsPriceFromMockedCallout() {
        // Arrange
        Test.setMock(HttpCalloutMock.class, new PricingServiceMock());

        // Act
        Test.startTest();
        Decimal price = PricingIntegrationService.fetchExternalPrice('SKU-100');
        Test.stopTest();

        // Assert
        Assert.areEqual(
            19.99, price,
            'Expected the price parsed from the mocked callout response body.'
        );
    }

    /**
     * Canned HTTP response — no real endpoint is ever contacted. The same
     * shape (implements HttpCalloutMock, returns a fixed HttpResponse)
     * applies to any callout-making class, not just this one endpoint.
     */
    private class PricingServiceMock implements HttpCalloutMock {
        public HttpResponse respond(HttpRequest request) {
            HttpResponse response = new HttpResponse();
            response.setStatusCode(200);
            response.setBody('{"price": 19.99}');
            return response;
        }
    }
}
