# Controller patterns

One worked example per rung of the controller-choice ladder, followed by
a view-state-reduction before/after pair. Each example is annotated with
*why* it sits at that rung — the justification is the point, not the
markup.

## Rung 1 — standard controller alone

The page needs nothing beyond a single Account record and its standard
`Contacts` relationship — display fields, list related contacts. Nothing
here exceeds what `standardController` already provides for free, so no
Apex exists for this page at all.

```html
<apex:page standardController="Account">
  <apex:pageBlock title="Account Detail">
    <apex:pageBlockSection>
      <apex:outputField value="{!account.Name}"/>
      <apex:outputField value="{!account.Industry}"/>
      <apex:outputField value="{!account.AnnualRevenue}"/>
    </apex:pageBlockSection>

    <apex:pageBlockTable value="{!account.Contacts}" var="con">
      <apex:column value="{!con.Name}"/>
      <apex:column value="{!con.Email}"/>
    </apex:pageBlockTable>
  </apex:pageBlock>
</apex:page>
```

**Why this rung:** `account` and `account.Contacts` both come from the
standard controller's automatic record and relationship binding. There is
no additional data need and no custom action — reaching for an extension
or a custom controller here would add a class with nothing to justify
its existence.

## Rung 2 — standard controller + extension

The page still centers on one Account and still wants the standard
Save/Cancel behavior, but it also needs an aggregate — total open
pipeline — that the standard controller's relationship set doesn't
expose (an aggregate SOQL result isn't a related list). That single
additional data need is what justifies stepping up to an extension
while keeping the standard controller underneath it.

```html
<apex:page standardController="Account" extensions="AccountSummaryExtension">
  <apex:form>
    <apex:pageBlock title="Account Summary">
      <apex:outputField value="{!account.Name}"/>

      <apex:outputPanel id="pipelinePanel">
        <apex:outputText value="Open pipeline: {!openPipelineTotal}"/>
      </apex:outputPanel>

      <apex:commandButton value="Recalculate"
                           action="{!recalculatePipeline}"
                           reRender="pipelinePanel"/>
    </apex:pageBlock>
  </apex:form>
</apex:page>
```

```apex
public with sharing class AccountSummaryExtension {
    private final Account account;
    private transient Decimal openPipelineTotalCache;

    // Extension constructor: takes the StandardController, does not
    // replace it — `account` below is the same record the page's
    // apex:outputField bindings read.
    public AccountSummaryExtension(ApexPages.StandardController stdController) {
        this.account = (Account) stdController.getRecord();
    }

    public Decimal getOpenPipelineTotal() {
        if (openPipelineTotalCache == null) {
            openPipelineTotalCache = computeOpenPipeline();
        }
        return openPipelineTotalCache;
    }

    public PageReference recalculatePipeline() {
        openPipelineTotalCache = computeOpenPipeline();
        return null; // stay on the page; reRender refreshes the panel
    }

    private Decimal computeOpenPipeline() {
        AggregateResult[] results = [
            SELECT SUM(Amount) total
            FROM Opportunity
            WHERE AccountId = :account.Id AND IsClosed = false
            WITH USER_MODE
        ];
        Object total = results[0].get('total');
        return total == null ? 0 : (Decimal) total;
    }
}
```

**Why this rung:** the standard controller's record context and default
Save/Cancel are still exactly what's wanted — nothing about the page's
core behavior changed. The extension exists solely to add the one thing
the standard controller can't express: an aggregate computed from
related records. `openPipelineTotalCache` is `transient` because it is
always cheap to recompute and has no business surviving in the view
state between requests.

## Rung 3 — custom controller

A multi-step onboarding wizard collects data for an Account and a
Contact that don't exist yet, across three steps, before either is
inserted. No single record backs this page at any point before the
final step — the page's identity is the wizard flow itself, not a
record detail. That data shape is what a standard controller (bound to
one existing record) and an extension (which augments a standard
controller's existing record) cannot express, which is why this page
starts at a custom controller rather than climbing the ladder from
rung 1.

```html
<apex:page controller="OnboardingWizardController">
  <apex:form>
    <apex:pageBlock title="Step {!currentStep} of 3">
      <apex:pageBlockSection rendered="{!currentStep == 1}">
        <apex:inputField value="{!newAccount.Name}"/>
      </apex:pageBlockSection>

      <apex:pageBlockSection rendered="{!currentStep == 2}">
        <apex:inputField value="{!newContact.LastName}"/>
        <apex:inputField value="{!newContact.Email}"/>
      </apex:pageBlockSection>

      <apex:pageBlockSection rendered="{!currentStep == 3}">
        <apex:outputText value="Review and finish onboarding."/>
      </apex:pageBlockSection>

      <apex:pageBlockButtons>
        <apex:commandButton value="Back" action="{!previousStep}"
                             rendered="{!currentStep > 1}"/>
        <apex:commandButton value="Next" action="{!nextStep}"
                             rendered="{!currentStep < 3}"/>
        <apex:commandButton value="Finish" action="{!save}"
                             rendered="{!currentStep == 3}"/>
      </apex:pageBlockButtons>
    </apex:pageBlock>
  </apex:form>
</apex:page>
```

```apex
public with sharing class OnboardingWizardController {
    public Integer currentStep { get; private set; }
    public Account newAccount { get; set; }
    public Contact newContact { get; set; }

    public OnboardingWizardController() {
        currentStep = 1;
        newAccount = new Account();
        newContact = new Contact();
    }

    public void nextStep() { currentStep++; }
    public void previousStep() { currentStep--; }

    public PageReference save() {
        insert newAccount;
        newContact.AccountId = newAccount.Id;
        insert newContact;
        return new ApexPages.StandardController(newAccount).view();
    }
}
```

**Why this rung:** there is no `ApexPages.StandardController` to extend
— neither `newAccount` nor `newContact` is a persisted record when the
page loads, and the page's own state (`currentStep`) has no
relationship to any single record at all. A custom controller owns
query, DML, and navigation outright because the page's data model is
the wizard, not a record.

## View-state reduction — before/after

### Before

```apex
public with sharing class AccountDashboardController {
    // Every property below is plain (non-transient): all three are
    // serialized into the view state on every request/response
    // round trip, whether or not the current page render uses them.
    public List<Account> allAccounts { get; set; }
    public List<Opportunity> allOpportunities { get; set; }
    public Map<Id, List<Contact>> contactsByAccount { get; set; }

    public AccountDashboardController() {
        allAccounts = [
            SELECT Id, Name, Industry FROM Account
            WITH USER_MODE LIMIT 2000
        ];
        // Not read by this page's markup at all — pure view-state
        // weight with no rendering benefit.
        allOpportunities = [SELECT Id, Amount FROM Opportunity WITH USER_MODE];

        contactsByAccount = new Map<Id, List<Contact>>();
        for (Contact c : [SELECT Id, Name, AccountId FROM Contact WITH USER_MODE]) {
            if (!contactsByAccount.containsKey(c.AccountId)) {
                contactsByAccount.put(c.AccountId, new List<Contact>());
            }
            contactsByAccount.get(c.AccountId).add(c);
        }
    }
}
```

Three problems, all of the same shape: nothing here distinguishes what
must survive a postback from what merely happens to be sitting in a
property. `allOpportunities` isn't used by anything this page renders.
`contactsByAccount` is built once at construction and never mutated
again — it doesn't need to survive in the view state if it can be
rebuilt on the next request. `allAccounts` holds up to 2000 full records
when the page renders one screen's worth at a time.

### After

```apex
public with sharing class AccountDashboardController {
    private static final Integer PAGE_SIZE = 50;

    // A single Integer is the only thing that must actually survive
    // the postback — it's what the next request needs to know which
    // slice of accounts to fetch.
    public Integer pageNumber { get; set; }

    // transient: never serialized into the view state. Recomputed
    // per request from `pageNumber`, which is durable.
    private transient List<Account> pageOfAccountsCache;

    public AccountDashboardController() {
        pageNumber = 1;
    }

    public List<Account> getPageOfAccounts() {
        if (pageOfAccountsCache == null) {
            pageOfAccountsCache = [
                SELECT Id, Name, Industry
                FROM Account
                WITH USER_MODE
                ORDER BY Name
                LIMIT :PAGE_SIZE
                OFFSET :((pageNumber - 1) * PAGE_SIZE)
            ];
        }
        return pageOfAccountsCache;
    }

    public PageReference nextPage() {
        pageNumber++;
        pageOfAccountsCache = null; // force the next page's slice to be fetched
        return null;
    }
}
```

What changed is not compression of the same data — it's a different
question asked up front: what must persist across a postback, versus
what can be fetched fresh for the request that needs it? `pageNumber`
answers the first question; everything else (the account slice,
computed from it) answers the second and is marked `transient`.
`allOpportunities` and `contactsByAccount` are gone entirely, because
this page's rendering never needed them — dropping unused data is part
of view-state discipline, not a separate cleanup step.
