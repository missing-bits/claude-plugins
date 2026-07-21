# salesforce-standards

Salesforce coding standards for the sf CLI toolchain: sf CLI is the
only interface to orgs and deployments, Salesforce Code Analyzer
(PMD + ESLint) is the linter, Prettier with the Apex plugin is the
formatter, sfdx-lwc-jest runs LWC tests. Standards follow official
Salesforce documentation and community consensus — Apex Developer
Guide, LWC Developer Guide, Salesforce Well-Architected — with the
author's preferences on contested points.

## Standards skills

| Skill | Scope |
|---|---|
| `salesforce-apex` | naming, lightweight layers (trigger handler, service, selector, domain), bulkification, governor limits, sharing keywords, error handling |
| `salesforce-apex-testing` | test-class structure, TestDataFactory, assertions, mocking, no SeeAllData, coverage as a floor |
| `salesforce-lwc` | component structure, JS conventions, wire vs imperative Apex, labels, events and LMS, styling, jest tests, static-resource placement stance |
| `salesforce-flow` | naming, plan-before-build, bulk-safe patterns, fault paths, run context, one record-triggered flow per object and trigger moment, retired-automation stance |
| `salesforce-data-model` | object/field naming, record types, validation rules, CMT vs Custom Settings, global value sets, no hardcoded IDs |
| `salesforce-security-model` | org-wide defaults, roles, permission-set-first, sharing rules, FLS |
| `salesforce-aura` | maintenance-first Aura: markup, controller/helper, events, LDS |
| `salesforce-visualforce` | maintenance-first Visualforce: controllers, extensions, view state, data binding |

Each skill ships `reference/` examples alongside its SKILL.md.
**Maintenance-first**: existing Aura/Visualforce is held to the
standards; new UI is built in LWC unless the platform forces the
legacy technology.

## Review stack

- **`salesforce-code-review` skill** — audits Salesforce code and
  metadata against the standards skills; writes one review report per
  run to `docs/code-review/`.
- **`salesforce-code-reviewer` agent** — reviews a diff or named
  files, writes the report to `docs/code-review/`, returns findings by
  severity.
- **`/salesforce-review` command** — review the current diff or named
  files. Salesforce files only; out-of-domain files are noted as out
  of scope.

Flows and declarative metadata are reviewed from metadata: findings
cite elements by name and order alphabetically by cited element name
where no line anchor exists.

When the working-process plugin's review-reports rule is installed
(detected by its contract probe), that rule's report contract is
authoritative; without it, the skill's minimal inline fallback applies
— a strict subset of the same contract, so the report shape never
depends on the install profile.

## working-process integration

- **`salesforce-plan-review` skill** — plan-review checklist
  discovered by the working-process plan-adversary agent when a
  reviewed plan touches Salesforce: metadata blast radius, governor
  limits at target volumes, security model, automation overlap,
  deployment dependencies and ordering.
- **`rules/salesforce-toolchain.md`** — a Rules payload distributed by
  working-process's sync-rules engine; states the toolchain and points
  at the skills conditionally.

Integration assumes working-process ≥ 0.6.0 when it is installed; the
plugin has no dependency on it — a standalone install is fully
functional, and every working-process mention in content is
conditional.
