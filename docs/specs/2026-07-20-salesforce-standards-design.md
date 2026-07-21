---
ticket: "#3"
date: 2026-07-20
status: implemented
grilled: 2026-07-20
architect: LGTM
branch: feature/3-salesforce-standards
base: master
---

# salesforce-standards — Salesforce coding-standards plugin

## Overview

New plugin `salesforce-standards` (v0.1.0) for the missing-bits
marketplace: skills encoding Salesforce coding standards across the
platform's development surfaces — the modern core plus maintenance-first
legacy UI — a code-review stack on the shared review-report
contract, and integration with the working-process plugin
(`*-plan-review` discovery and the Rules payload).

The shape — area skills with `reference/` examples, a review skill, a
reviewer agent, a review command, a plan-review checklist, a Rules
payload — follows python-standards
(`2026-07-16-python-standards-design.md`), the first Standards plugin
on these conventions. Like python-standards, this is an original design
inspired by the author's earlier domain-standards plugin work in
another marketplace: this spec is the authoritative construction, not a
migration of existing content.

## Sources and toolchain

Standards content: official Salesforce documentation (Apex Developer
Guide, LWC Developer Guide, Salesforce Well-Architected) and community
consensus; the author's preferences decide contested points. One
contested point is settled up front: the Apex layering stance is
**lightweight layers without a library** — one handler per trigger plus
service/selector/domain as a naming-and-structure convention, no fflib
dependency; Apex Enterprise Patterns are cited as inspiration, not a
requirement.

Standardized toolchain: **sf CLI** (the only interface to orgs and
deployments), **Salesforce Code Analyzer** (PMD + ESLint) as the
linter, **Prettier with the Apex plugin** as the formatter,
**sfdx-lwc-jest** for LWC tests.

## Skills (8)

Each skill: `SKILL.md` + `reference/` examples. Descriptions written
disjointly (no two skills compete for the same trigger); authored with
skill-creator + superpowers:writing-skills per repo convention.

| Skill | Scope |
|---|---|
| `salesforce-apex` | naming, lightweight layers (trigger handler, service, selector, domain), bulkification, governor limits, sharing in code (`with`/`inherited sharing`), error handling |
| `salesforce-apex-testing` | test-class structure, TestDataFactory, assertions, mocking, `Test.startTest`/`stopTest`, no `SeeAllData`, coverage as a floor not a target |
| `salesforce-lwc` | file/component structure, JavaScript conventions, wire vs imperative Apex, custom labels, component communication (events, LMS), styling; the jest-testing paragraph (sfdx-lwc-jest) lives here — not in apex-testing; placement stance: application JavaScript lives in component bundles, static resources are for third-party libraries and assets |
| `salesforce-flow` | naming, plan-before-build, bulk-safe patterns, fault paths, run context, one record-triggered flow per object and trigger moment (before-save, after-save, before-delete, …); maintenance-only stance for retired automation (Workflow Rules, Process Builder) with Flow as the migration target |
| `salesforce-data-model` | object/field naming, Custom Metadata Types vs Custom Settings, no hardcoded IDs, field descriptions |
| `salesforce-security-model` | org-wide defaults, roles, profiles vs permission sets (permission-set-first), sharing rules, FLS in code and UI |
| `salesforce-aura` | maintenance-first: markup, controller/helper JavaScript, component vs application events, Lightning Data Service |
| `salesforce-visualforce` | maintenance-first: standard controllers, extensions, custom controllers, view state discipline, data binding |

Boundaries: LWC testing belongs to `salesforce-lwc`
(`salesforce-apex-testing` is Apex-only); sharing deliberately has two
homes — keyword mechanics in `salesforce-apex`, access-model design in
`salesforce-security-model`.

**Maintenance-first** (legacy UI stance): existing Aura and Visualforce
code is held to these standards, but new UI is built in LWC unless the
platform forces the legacy technology (e.g. Visualforce for PDF
rendering, Aura where LWC support is missing). The clause is explicit
in both skills and gives the review stack its basis for flagging new
legacy-UI surface.

## Review stack

- `salesforce-code-review` skill: audits Salesforce code against the
  standards skills. Report contract: when the working-process
  review-reports rule is installed it is authoritative — "installed"
  means the contract probe succeeds (project-level then user-level
  rules target contains `working-process/review-reports.md`; the rule
  does not auto-load in review sessions). The skill carries a **minimal
  inline fallback** — severity scale Critical/Important/Minor, Summary,
  the shared `findings: { critical: N, important: N, minor: N }`
  frontmatter key, `ticket` and `standards: salesforce-standards`
  frontmatter (required even standalone), and the filename element —
  `<YYYY-MM-DD>-<scope-slug>-<runid>.md`, generated prompt-free, never
  overwriting (collision → new runid) — a strict subset of the
  shared contract, so report shape never depends on the install
  profile; marked "the installed working-process review-reports rule
  supersedes this". Reports go to `docs/code-review/`; a standalone
  install simply creates the directory (the first-create mode question
  belongs to working-process's process-artifacts rule and is absent in
  a standalone install).
- `salesforce-code-reviewer` agent: reviews a diff or named files,
  writes the report, returns findings by severity. Its description
  names `docs/code-review/` as the report destination.
- `/salesforce-review` command: review the current diff or named files.
- Naming rule: ONE `salesforce-` family for every surface; skills are
  named for the activity (`salesforce-code-review`), the agent for the
  actor (`salesforce-code-reviewer`) — the same convention
  python-standards settled on 2026-07-17. `salesforce-code-review`
  follows the `*-code-review` pattern a future working-process review
  orchestrator will discover (non-goal here).
- Run scope per the shared contract: `/salesforce-review` reviews the
  files the standards skills cover — Apex (`.cls`, `.trigger`), LWC,
  Flow metadata, Aura bundles, Visualforce (`.page`, `.component`),
  and the declarative metadata the data-model and security-model
  skills govern (object and field metadata, record types, validation
  rules, Custom Metadata records, global value sets, permission sets
  and permission set groups, sharing rules, profiles), plus Workflow
  Rules
  (`*.workflow-meta.xml`) — the retired-automation surface the flow
  skill's maintenance-only stance flags; Process Builder processes
  already arrive as Flow metadata — and notes out-of-domain files in
  Summary as out of scope. Static resources are in scope narrowly: a run flags
  new or modified custom application JavaScript landing in a static
  resource (a placement finding per `salesforce-lwc`), never
  line-level content review; third-party libraries are not reviewed
  at all.
  Flow and declarative metadata files are reviewed from metadata:
  findings cite elements by name (Flow elements, object/field API
  names), not XML line numbers, and within a severity subsection they
  are ordered alphabetically by cited element name — the
  domain-stated stable key under the contract's line-less-findings
  provision (companion amendment, see working-process integration).

## working-process integration

- `salesforce-plan-review` skill: plan-review checklist discovered by
  the plan-adversary agent — Salesforce verification specifics:
  metadata blast radius, governor limits at target volumes, security
  model (org-wide defaults and FLS for new fields), automation overlap
  (trigger vs flow on the same object), deployment dependencies and
  ordering.
- Rules payload `rules/salesforce-toolchain.md`, `paths: ["**/*.cls",
  "**/*.trigger", "**/lwc/**", "**/aura/**", "**/*.page",
  "**/*.component", "**/*.flow-meta.xml", "**/*.workflow-meta.xml",
  "**/*.object-meta.xml",
  "**/*.field-meta.xml", "**/*.recordType-meta.xml",
  "**/*.validationRule-meta.xml", "**/*.md-meta.xml",
  "**/*.globalValueSet-meta.xml", "**/*.permissionset-meta.xml",
  "**/*.permissionsetgroup-meta.xml", "**/*.sharingRules-meta.xml",
  "**/*.profile-meta.xml", "force-app/**", "sfdx-project.json"]`
  — `**/lwc/**` and `**/aura/**` catch component bundles regardless of
  the package directory name (their files are plain `.js`/`.html`, so
  only the platform-fixed bundle directories identify them outside the
  default `force-app/` layout); the metadata-suffix globs do the same
  for flows and the declarative surfaces, whose `-meta.xml` suffixes
  are platform-fixed. Deliberately no static-resource glob: editing a
  vendored library must not load the toolchain rule — the placement
  standard fires from review, and components consuming the resource
  load the rule via their own paths. The toolchain
  facts (sf CLI, Code Analyzer, Prettier + Apex plugin, sfdx-lwc-jest)
  and conditional pointers to the skills ("when available").
  Frontmatter reviewed by hand (validate skips `rules/`).
- Companion amendment (ships with this work as a working-process
  minor): the review-reports rule gains one bullet — findings without
  a line anchor are ordered by a domain-stated stable key — closing
  the contract gap this plugin's metadata-reviewed files expose.
  This spec's alphabetical-by-cited-element-name ordering is that
  stated key. Precedent: the ticket-frontmatter companion edit carried
  by the review-reports spec.
- Assumed convention range: **working-process ≥ 0.6.0** (the contract
  shape the inline fallback subsets — `docs/code-review/`,
  review-reports rule, consumer-carried filename element). The
  line-less-ordering bullet is additive gap-filling: against a 0.6.0–
  0.8.0 install the ordering is simply this domain's convention. No
  `dependencies` edge — a standalone install is fully functional; every
  working-process mention in content is conditional.

## Non-goals

- CI/CD — branching, pipelines, and deployments out of the first
  release's scope (a candidate future area skill).
- fflib / Apex Enterprise Patterns as a requirement — cited only as
  inspiration for the lightweight-layers stance.
- Review orchestration — `salesforce-code-review` only follows the
  `*-code-review` naming pattern; orchestration is a parked
  working-process idea.
- Org-configuration standards (feature flags, environments, scratch-org
  tooling beyond the toolchain facts).

## Verification

- `claude plugin validate .` and `claude plugin validate
  plugins/salesforce-standards` pass; marketplace catalog entry +
  README row land in the same commit as the manifest (marketplace-sync
  rule).
- Install from the local marketplace; the eight standards skills and
  `salesforce-plan-review` appear in the skills list; the agent appears
  under the plugin namespace.
- `/salesforce-review` on a sample diff writes a report to
  `docs/code-review/` honoring the shared format (working-process
  installed) and the inline fallback (standalone install).
- A plan-adversary dispatch on a Salesforce-touching plan discovers and
  loads `salesforce-plan-review`.
- sync-rules installs `salesforce-toolchain.md` as a foreign payload;
  the drift hook stays silent afterwards.
- The companion amendment lands in working-process: the amended
  `review-reports.md` carries the line-less-ordering bullet, the minor
  version bump delivers the drift nudge to installed copies, and a
  post-sync contract probe reads the amended rule.

## Architect findings — 2026-07-20 round 1

Dispatched on Fable 5 (prescribed tier); verdict: blocking.

- **Important — run scope vs skills**: the run-scope enumeration
  (Apex, LWC, Flow metadata, Aura, Visualforce) leaves
  `salesforce-data-model` and `salesforce-security-model` with no
  reviewable surface, contradicting "reviews the files the standards
  skills cover" — a new field with no description would be noted out
  of scope while the plugin ships that exact standard. → Fixed:
  run scope extended with the declarative surfaces the two skills
  govern; the developer's follow-up review broadened it further
  (record types, validation rules, Custom Metadata records, global
  value sets, profiles) and added the narrow static-resource placement
  clause.
- **Important — Flow ordering rewrites the contract**: alphabetical
  ordering for line-less findings is asserted as a substitution for
  the contract's "ascending line order", but ordering is
  contract-owned (not in the domain-owned carve-out list) and the
  contract's owner is working-process. → Fixed: the companion
  amendment (one bullet — findings without a line anchor order by a
  domain-stated stable key — plus a working-process minor bump) is now
  specified in the working-process integration section and ships with
  this work; the run-scope text references it instead of asserting a
  substitution.
- **Minor — payload paths omit Flow**: the `**/lwc/**`/`**/aura/**`
  rationale applies identically to `**/*.flow-meta.xml`; a flow-only
  edit outside `force-app/` loads no toolchain rule. → Fixed: the
  metadata-suffix globs are in `paths:` (flow, object, field, record
  type, validation rule, CMT record, global value set, permission set,
  sharing rules, profile); deliberately no static-resource glob.
- **Minor — fallback misses the filename element; stale range**: the
  inline-fallback enumeration omits the filename/no-overwrite element
  the 2026-07-17 contract amendment moved into consumers' fallbacks,
  and `≥ 0.5.0` names the pre-amendment contract. → Fixed: the
  fallback enumeration carries the filename element (prompt-free,
  never overwriting); the assumed range is `≥ 0.6.0`.

Round 2 (verification pass, Fable 5): all four dispositions confirmed;
the two new developer decisions (flow retired-automation stance, LWC
static-resource placement stance) judged sound. Two new minors fixed
inline — Workflow Rules (`*.workflow-meta.xml`) added to run scope and
payload paths (the flow stance now has its reviewable surface), and a
verification bullet added for the companion review-reports amendment.
Verdict: LGTM.
