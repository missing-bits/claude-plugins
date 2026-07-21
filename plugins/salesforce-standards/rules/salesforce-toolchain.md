---
paths:
  - "**/*.cls"
  - "**/*.trigger"
  - "**/lwc/**"
  - "**/aura/**"
  - "**/*.page"
  - "**/*.component"
  - "**/*.flow-meta.xml"
  - "**/*.workflow-meta.xml"
  - "**/*.object-meta.xml"
  - "**/*.field-meta.xml"
  - "**/*.recordType-meta.xml"
  - "**/*.validationRule-meta.xml"
  - "**/*.md-meta.xml"
  - "**/*.globalValueSet-meta.xml"
  - "**/*.permissionset-meta.xml"
  - "**/*.permissionsetgroup-meta.xml"
  - "**/*.sharingRules-meta.xml"
  - "**/*.profile-meta.xml"
  - "force-app/**"
  - "sfdx-project.json"
---

# Salesforce toolchain

This project follows the salesforce-standards toolchain:

- **sf CLI** is the only interface to orgs and deployments — retrieve,
  deploy, and run org tests through `sf`; no sfdx-era commands, no
  manual Setup changes to tracked metadata.
- **Salesforce Code Analyzer** (PMD + ESLint) is the linter:
  `sf code-analyzer run`.
- **Prettier with the Apex plugin** formats Apex, LWC, Aura, and
  Visualforce sources.
- **sfdx-lwc-jest** runs LWC unit tests.

When the salesforce-standards plugin's skills are available, load the
matching one before working: `salesforce-apex` (backend code),
`salesforce-apex-testing` (Apex tests), `salesforce-lwc` (Lightning
Web Components), `salesforce-flow` (Flows and retired automation),
`salesforce-data-model` (objects, fields, declarative data config),
`salesforce-security-model` (access design), `salesforce-aura` /
`salesforce-visualforce` (legacy UI maintenance). When they are not
available, the toolchain facts above still bind.
