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
`salesforce-triggers` (Apex triggers and their handlers),
`salesforce-apex-testing` (Apex tests), `salesforce-lwc` (Lightning
Web Components), `salesforce-flow` (Flows and retired automation),
`salesforce-data-model` (objects, fields, declarative data config),
`salesforce-security-model` (access design), `salesforce-aura` /
`salesforce-visualforce` (legacy UI maintenance). When they are not
available, the toolchain facts above still bind.

The project's trigger framework and its vendor code are declared in
the project, never in this rule. A line carrying the `trigger-framework:`
key sits in the body of a `CLAUDE.md` — the root one, a trigger
directory's, or `.claude/CLAUDE.md` — or of a project rule outside this
payload, one framework per path. A line carrying the `vendor-paths:` key
sits in a root home alone — either root `CLAUDE.md` or a project rule —
as directory prefixes; a copy in a subdirectory is not read. When the
`salesforce-triggers` skill is available it reads both keys and says how
they rank; when it is not, the lines still record the choice for the
reader.
