---
ticket: "#3"
date: 2026-07-20
status: implemented
adversary: LGTM
branch: feature/3-salesforce-standards
base: master
spec: ../specs/2026-07-20-salesforce-standards-design.md
---

# salesforce-standards Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `salesforce-standards` plugin (v0.1.0) — eight Salesforce standards skills, a review stack writing Review reports, a `salesforce-plan-review` checklist, a `salesforce-toolchain` Rules payload — plus the companion review-reports amendment in working-process (0.9.0), and register the plugin in the `missing-bits` marketplace.

**Architecture:** A single Standards plugin under `plugins/salesforce-standards/`: area skills with `reference/` examples, a `salesforce-code-review` skill that defers to the working-process review-reports contract via the Contract probe and carries a strict-subset inline fallback for a Standalone install, a `salesforce-code-reviewer` agent and `/salesforce-review` command on top of that skill, plus the Rules payload picked up by working-process's Rules engine. One companion edit lands in working-process itself: the review-reports rule gains the line-less-findings ordering provision this domain needs. No `dependencies` edge — a Standalone install is fully functional.

**Tech Stack:** Claude Code plugin system (plugin.json, marketplace.json, skills/SKILL.md, agents/*.md, commands/*.md, rules/*.md), git, jq.

## Global Constraints

- **Sequencing (plan-level):** Task 2 (the working-process companion amendment) MUST land before Task 13 (the review skill references the contract's line-less-findings provision and its fallback subsets the amended contract). Tasks 3–12 are independent of Task 2 and of each other.
- Assumed convention range: **working-process ≥ 0.6.0** (Process directory `docs/code-review/`, review-reports rule, consumer-carried filename element). NO `dependencies` entry in `plugin.json`; every mention of working-process inside plugin content is conditional ("when … is installed/available").
- **Content input:** official Salesforce documentation is the baseline — Apex Developer Guide, LWC Developer Guide, Salesforce Well-Architected, Flow documentation, Code Analyzer/PMD and Prettier-Apex docs — plus community consensus. Contested points are decided by the developer's explicitly stated preferences; when unstated, collect them as open questions for the developer. NEVER invent personal preferences.
- **Settled stances (verbatim in content, decided in the spec):** lightweight Apex layers without a library (one handler per trigger + service/selector/domain as a naming-and-structure convention; no fflib dependency; Apex Enterprise Patterns cited as inspiration, not a requirement); maintenance-first legacy UI (existing Aura/Visualforce held to the standards, new UI in LWC unless the platform forces legacy — e.g. Visualforce for PDF rendering, Aura where LWC support is missing); maintenance-only retired automation (Workflow Rules, Process Builder → Flow as the migration target); permission-set-first; application JavaScript lives in component bundles, static resources are for third-party libraries and assets; one record-triggered flow per object and trigger moment (before-save, after-save, before-delete, …).
- **Toolchain facts (verbatim in content):** sf CLI (the only interface to orgs and deployments), Salesforce Code Analyzer (PMD + ESLint) as the linter, Prettier with the Apex plugin as the formatter, sfdx-lwc-jest for LWC tests.
- **Naming rule:** ONE `salesforce-` family for every surface; skills are named for the activity (`salesforce-code-review`), the agent for the actor (`salesforce-code-reviewer`). Names are kebab-case.
- **Skill authoring:** every skill is authored with the `skill-creator` skill (scaffolding, `description:` tuning, evals) plus the `superpowers:writing-skills` discipline. Skill descriptions are written disjointly — no two skills compete for the same trigger.
- **Stance–surface coupling (architect's watch-rule):** any content edit that gives a skill a new stance must, in the same edit, give the review run scope and the Rules payload `paths:` the matching surface. Applies to every content task below.
- **Glossary binds wording** (docs/domain/glossary.md): Standards plugin, Standalone install, Contract probe, Review report, Rules payload, Rules engine. Respect every `_Avoid_` ban — never "standards stack", never "solo install", never "review output", never "rules plugin", never unqualified "probe".
- **Frontmatter safety:** quote any `description:` (or other scalar) containing `: ` (colon+space). `claude plugin validate` skips `rules/` — review the Rules payload frontmatter by hand.
- **Public-repo hygiene:** English only, no machine-specific paths, no company or client names — in every committed file and commit message.
- **Commits:** Conventional Commits, ONE line (single subject, no body, no trailers — no Co-Authored-By).
- All salesforce-standards tasks land at plugin version **0.1.0** (a new plugin on one topic branch — no per-commit bumps before the first release). The working-process companion amendment bumps working-process **0.8.0 → 0.9.0** in the same commit as its rule edit.
- Repo root during execution: the claude-plugins repository root, branch `feature/3-salesforce-standards`.

---

### Task 1: Plugin manifest and marketplace registration

Per the marketplace-sync rule, a new plugin lands with all three identity places at once — manifest, catalog entry, README row — in ONE commit.

**Files:**
- Create: `plugins/salesforce-standards/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json` (append to `plugins` array)
- Modify: `README.md` (repo root — add a plugin table row)

**Interfaces:**
- Produces: plugin name `salesforce-standards`, version `0.1.0` (consumed by every later task; the README of Task 15 and the verification of Task 16 use the name verbatim).

- [ ] **Step 1: Write `plugins/salesforce-standards/.claude-plugin/plugin.json`**

```json
{
  "name": "salesforce-standards",
  "description": "Salesforce coding standards for the sf CLI + Code Analyzer + Prettier-Apex + sfdx-lwc-jest toolchain: eight area skills (Apex, Apex testing, LWC, Flow, data model, security model, maintenance-first Aura and Visualforce), a code-review stack (salesforce-code-review skill, salesforce-code-reviewer agent, /salesforce-review command) writing review reports to docs/code-review/, a salesforce-plan-review checklist for plan reviews, and a salesforce-toolchain rule shipped as a Rules payload",
  "version": "0.1.0",
  "author": { "name": "Missing Bits (Jacek Nakonieczny)" },
  "license": "MIT",
  "keywords": ["salesforce", "standards", "apex", "lwc", "flow", "aura", "visualforce", "sf-cli", "review"]
}
```

No `dependencies` field — a Standalone install is fully functional by design.

- [ ] **Step 2: Add the catalog entry**

In `.claude-plugin/marketplace.json`, append to the `plugins` array (after the `python-standards` entry):

```json
{
  "name": "salesforce-standards",
  "source": "./plugins/salesforce-standards",
  "description": "Salesforce coding standards for the sf CLI toolchain: area skills for Apex, LWC, Flow, data and security model plus maintenance-first legacy UI, a code-review stack, a plan-review checklist, and a salesforce-toolchain rule"
}
```

- [ ] **Step 3: Add the README row**

In the repo root `README.md` plugin table, add below the `python-standards` row:

```markdown
| `salesforce-standards` | Salesforce coding standards for the sf CLI toolchain: area skills (Apex, LWC, Flow, data/security model, legacy UI), code-review stack, plan-review checklist, distributed toolchain rule |
```

- [ ] **Step 4: Validate**

Run: `jq -e '.name == "salesforce-standards" and .version == "0.1.0" and (has("dependencies") | not)' plugins/salesforce-standards/.claude-plugin/plugin.json`
Expected: `true`

Run: `jq -e '[.plugins[].name] == ["working-process", "python-standards", "salesforce-standards"] and (.plugins[2].source == "./plugins/salesforce-standards")' .claude-plugin/marketplace.json`
Expected: `true`

Run: `grep -c 'salesforce-standards' README.md`
Expected: `1`

- [ ] **Step 5: Commit (all three files — one commit, per marketplace-sync)**

```bash
git add plugins/salesforce-standards/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md
git commit -m "feat(salesforce-standards): register the plugin in the marketplace"
```

---

### Task 2: working-process companion amendment — line-less findings ordering

The review-reports contract orders findings "in ascending line order"; files reviewed from metadata (flows, declarative config) have no line anchor. The contract's owner amends the contract; the domain states the key. Precedent: the ticket-frontmatter companion edit carried by the review-reports spec.

**Files:**
- Modify: `plugins/working-process/rules/review-reports.md` (Layout section)
- Modify: `plugins/working-process/.claude-plugin/plugin.json` (version only)
- Modify: `docs/specs/2026-07-16-working-process-review-reports-design.md` (append an amendment record)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the contract's line-less-findings provision, referenced by Task 13's review skill and Task 16's verification; working-process version `0.9.0`.

- [ ] **Step 1: Amend the Layout section of `plugins/working-process/rules/review-reports.md`**

With the Edit tool, extend Layout item 2. Old text:

```markdown
2. **Per-file sections**, each with **Critical → Important → Minor**
   subsections; findings within a subsection in ascending line order.
```

New text:

```markdown
2. **Per-file sections**, each with **Critical → Important → Minor**
   subsections; findings within a subsection in ascending line order.
   Findings without a line anchor — files reviewed from metadata
   rather than source lines — are ordered by a domain-stated stable
   key: the reviewing domain names the key (e.g. cited element name,
   alphabetically) and applies it consistently.
```

- [ ] **Step 2: Bump the working-process version**

In `plugins/working-process/.claude-plugin/plugin.json`, confirm the current `version` is `0.8.0`, then change it to `0.9.0` (a backward-compatible contract addition → minor). If the current version is NOT `0.8.0`, STOP and consult the developer — Step 3's record and Task 16 Steps 3 and 6 hard-expect `0.9.0` and must be re-derived together.

- [ ] **Step 3: Append the amendment record to the review-reports spec**

Append to `docs/specs/2026-07-16-working-process-review-reports-design.md`, following that spec's existing amendment pattern:

```markdown
## Amendment — 2026-07-20: line-less findings ordering

The salesforce-standards review stack (ticket #3) surfaced a layout
gap: subsection ordering was defined only for line-anchored findings,
while flows and declarative metadata are reviewed from metadata and
cite elements by name. The Layout rule now states that findings
without a line anchor are ordered by a domain-stated stable key (the
reviewing domain names the key and applies it consistently). Additive
gap-filling — no existing report shape changes; shipped as
working-process 0.9.0.
```

- [ ] **Step 4: Validate**

Run: `grep -c 'domain-stated stable' plugins/working-process/rules/review-reports.md`
Expected: `1`

Run: `jq -r '.version' plugins/working-process/.claude-plugin/plugin.json`
Expected: `0.9.0`

Run: `grep -c 'line-less findings ordering' docs/specs/2026-07-16-working-process-review-reports-design.md`
Expected: `1`

Run: `claude plugin validate plugins/working-process`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/working-process/rules/review-reports.md plugins/working-process/.claude-plugin/plugin.json
git commit -m "feat(working-process): order line-less review findings by a domain-stated stable key"
```

The spec amendment record (Step 3) stays uncommitted here — `docs/`
documents are committed by the developer at Task 17's offer, per repo
precedent for contract-amendment records.

---

### Task 3: salesforce-apex skill

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-apex/SKILL.md`
- Create: `plugins/salesforce-standards/skills/salesforce-apex/reference/trigger-handler.cls`
- Create: `plugins/salesforce-standards/skills/salesforce-apex/reference/bulkification.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: skill name `salesforce-apex` (Tasks 12, 13, 15); the lightweight-layers convention consumed by Task 4's factory placement and Task 11's checklist wording.

- [ ] **Step 1: Collect the standards and settle contested points**

Author from the Apex Developer Guide, Salesforce Well-Architected, and PMD's Apex rulesets. Ask the developer to settle contested points before writing — at minimum: handler class naming pattern (e.g. `AccountTriggerHandler`), selector method/return conventions, custom exception conventions, and logging approach. Anything unsettled becomes an open question for the developer, never a silent assumption.

- [ ] **Step 2: Scaffold and author the skill**

Invoke the `skill-creator` skill for scaffolding and `description:` tuning; follow `superpowers:writing-skills` for content discipline. SKILL.md opens with exactly this frontmatter:

```yaml
---
name: salesforce-apex
description: Use when writing or reviewing Apex backend code — naming, lightweight layering (one trigger handler per object, service, selector, domain), bulkification, governor limits, sharing keywords, and error handling. Apex unit tests belong to salesforce-apex-testing; access-model design to salesforce-security-model.
---
```

Mandatory content (each a section or explicit rule; sourced per Step 1):

- Naming conventions (classes, methods, variables, constants) with the developer's contested-point choices.
- Lightweight layers: ONE handler per trigger, trigger body free of logic; service/selector/domain as a naming-and-structure convention with the responsibilities of each layer; no fflib dependency — Apex Enterprise Patterns cited as inspiration, not a requirement.
- Bulkification: no SOQL/DML in loops, collection-driven patterns, trigger paths always assume bulk.
- Governor limits: the budgets to design for (SOQL rows/queries, DML, CPU, heap), Limits-class checks where appropriate.
- Sharing in code: `with sharing` / `inherited sharing` as defaults, `without sharing` only with a stated justification — keyword mechanics only; access-model design belongs to salesforce-security-model (name the skill).
- Error handling: custom exceptions, no swallowed exceptions, the logging approach settled in Step 1.
- Rules cited by stable ids where useful for review findings (e.g. PMD rule names).

- [ ] **Step 3: Write the reference files**

- `reference/trigger-handler.cls`: a complete annotated example — trigger + handler + service + selector for one object, demonstrating the layer responsibilities and sharing declarations the SKILL.md prescribes.
- `reference/bulkification.md`: before/after example pairs — SOQL in loop → collection-driven query, DML in loop → collected DML, at least one governor-limit-aware pattern.

- [ ] **Step 4: Validate**

Run: `grep -c '^name: salesforce-apex$' plugins/salesforce-standards/skills/salesforce-apex/SKILL.md`
Expected: `1`

Run: `ls plugins/salesforce-standards/skills/salesforce-apex/reference/`
Expected: `bulkification.md  trigger-handler.cls`

Run: `grep -ci 'fflib' plugins/salesforce-standards/skills/salesforce-apex/SKILL.md`
Expected: at most mentions marking it as inspiration/not-required (spot-check by eye: never as a requirement).

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-apex/
git commit -m "feat(salesforce-standards): add salesforce-apex skill"
```

---

### Task 4: salesforce-apex-testing skill

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-apex-testing/SKILL.md`
- Create: `plugins/salesforce-standards/skills/salesforce-apex-testing/reference/TestDataFactory.cls`
- Create: `plugins/salesforce-standards/skills/salesforce-apex-testing/reference/test-patterns.cls`

**Interfaces:**
- Consumes: the layering convention from Task 3 (referenced by skill name, not duplicated).
- Produces: skill name `salesforce-apex-testing` (Tasks 12, 13, 15).

- [ ] **Step 1: Collect the standards and settle contested points**

Author from the Apex Developer Guide testing chapters. Ask the developer to settle: the TestDataFactory shape (one class vs per-object builders), the assertion style (`Assert` class vs legacy `System.assert*`), the mocking approach (`Test.setMock`, `Stub API`), and the coverage floor above the platform's 75% deploy minimum. Anything unsettled becomes an open question.

- [ ] **Step 2: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: salesforce-apex-testing
description: Use when writing or reviewing Apex unit tests — test-class structure, TestDataFactory, assertions, mocking, Test.startTest/stopTest, and test data without SeeAllData. Apex-only; LWC jest tests belong to salesforce-lwc.
---
```

Mandatory content:

- Test-class structure: naming (`<Class>Test`), `@TestSetup`, one behavior per test method, Arrange-Act-Assert.
- TestDataFactory as the single source of test records (shape settled in Step 1); no inline record creation in test methods.
- Assertions: the settled style, always with a failure message; asserting behavior, not just "no exception".
- Mocking: `Test.setMock` for callouts, the Stub API stance settled in Step 1.
- `Test.startTest`/`stopTest` around the action under test (fresh governor-limit context).
- `@IsTest(SeeAllData=true)` is banned — tests create their own data.
- Coverage as a floor not a target: the platform's 75% deploy minimum plus the floor settled in Step 1; meaningful assertions over coverage chasing.

- [ ] **Step 3: Write the reference files**

- `reference/TestDataFactory.cls`: a complete annotated factory in the settled shape — at least two object builders with sensible defaults and override parameters.
- `reference/test-patterns.cls`: annotated example tests — a bulk-path test (200 records), a negative test asserting a thrown exception, a callout test with `Test.setMock`, each using `Test.startTest`/`stopTest`.

- [ ] **Step 4: Validate**

Run: `grep -c '^name: salesforce-apex-testing$' plugins/salesforce-standards/skills/salesforce-apex-testing/SKILL.md`
Expected: `1`

Run: `grep -c 'SeeAllData' plugins/salesforce-standards/skills/salesforce-apex-testing/SKILL.md`
Expected: non-zero (the ban is stated).

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-apex-testing/
git commit -m "feat(salesforce-standards): add salesforce-apex-testing skill"
```

---

### Task 5: salesforce-lwc skill

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-lwc/SKILL.md`
- Create: `plugins/salesforce-standards/skills/salesforce-lwc/reference/component-patterns.js`
- Create: `plugins/salesforce-standards/skills/salesforce-lwc/reference/jest-patterns.test.js`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: skill name `salesforce-lwc` (Tasks 12, 13, 15); the static-resource placement stance cited by Task 13's run scope; the jest-testing home (spec boundary: NOT in salesforce-apex-testing).

- [ ] **Step 1: Collect the standards and settle contested points**

Author from the LWC Developer Guide and sfdx-lwc-jest docs. Ask the developer to settle: SLDS styling stance (utility classes vs custom CSS boundaries), custom event naming, and component folder conventions beyond the platform defaults. Anything unsettled becomes an open question.

- [ ] **Step 2: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: salesforce-lwc
description: Use when building or reviewing Lightning Web Components — file and component structure, JavaScript conventions, wire vs imperative Apex, custom labels, component communication (events, Lightning Message Service), styling, and jest tests with sfdx-lwc-jest. New UI belongs here; Aura maintenance belongs to salesforce-aura.
---
```

Mandatory content:

- File/component structure: bundle layout, one component one responsibility, naming (camelCase folder, kebab-case usage).
- JavaScript conventions: modern ES modules, private fields/getters discipline, no direct DOM manipulation outside the component, `@api`/`@track`/`@wire` usage rules.
- wire vs imperative Apex: wire for reactive reads, imperative for actions and parameterized one-shots; `cacheable=true` guidance.
- Custom labels for user-facing text — no hardcoded UI strings.
- Component communication: custom events up, properties down, Lightning Message Service across the DOM hierarchy; event naming as settled in Step 1.
- Styling: SLDS stance as settled in Step 1.
- Jest tests with sfdx-lwc-jest: the testing paragraph lives HERE (spec boundary — salesforce-apex-testing is Apex-only): test file placement, DOM assertions, mocking wire adapters.
- Placement stance (verbatim substance): application JavaScript lives in component bundles; static resources are for third-party libraries and assets.

- [ ] **Step 3: Write the reference files**

- `reference/component-patterns.js`: an annotated component JS module demonstrating wire vs imperative, event dispatch, and label import, with the matching HTML template sketched in a comment block.
- `reference/jest-patterns.test.js`: annotated jest tests — a render assertion, a wire-adapter mock, an event-dispatch assertion.

- [ ] **Step 4: Validate**

Run: `grep -c '^name: salesforce-lwc$' plugins/salesforce-standards/skills/salesforce-lwc/SKILL.md`
Expected: `1`

Run: `grep -c 'sfdx-lwc-jest' plugins/salesforce-standards/skills/salesforce-lwc/SKILL.md`
Expected: non-zero (jest home is here).

Run: `grep -c 'static resource' plugins/salesforce-standards/skills/salesforce-lwc/SKILL.md`
Expected: non-zero (placement stance present).

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-lwc/
git commit -m "feat(salesforce-standards): add salesforce-lwc skill"
```

---

### Task 6: salesforce-flow skill

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-flow/SKILL.md`
- Create: `plugins/salesforce-standards/skills/salesforce-flow/reference/flow-patterns.md`
- Create: `plugins/salesforce-standards/skills/salesforce-flow/reference/naming.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: skill name `salesforce-flow` (Tasks 12, 13, 15); the retired-automation stance cited by Task 13's run scope and Task 11's checklist.

- [ ] **Step 1: Collect the standards and settle contested points**

Author from the Flow documentation and Salesforce Well-Architected automation guidance. Ask the developer to settle: the flow naming pattern (e.g. `<Object>_<TriggerMoment>_<Purpose>` vs another scheme) and the subflow decomposition stance. Anything unsettled becomes an open question.

- [ ] **Step 2: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: salesforce-flow
description: Use when building or reviewing Salesforce Flows — naming, plan-before-build, bulk-safe patterns, fault paths, run context, one record-triggered flow per object and trigger moment, and the maintenance-only stance for Workflow Rules and Process Builder.
---
```

Mandatory content:

- Naming: the pattern settled in Step 1, applied to flows, elements, variables (element names are finding citations — see the review stack).
- Plan-before-build: sketch entry criteria, decision branches, and failure behavior before opening the builder.
- One record-triggered flow per object and trigger moment (before-save, after-save, before-delete, …); orchestrate inside the flow, not by flow proliferation.
- Bulk-safe patterns: no Get/Update elements inside loops, collection-based operations, entry conditions to keep the flow off irrelevant records.
- Fault paths: every DML/callout element has a fault connector with a named handling behavior — never a silent dead end.
- Run context: system vs user context choice is explicit; sharing implications named.
- Retired automation (verbatim substance): Workflow Rules and Process Builder are maintenance-only — no new ones; Flow is the migration target.

- [ ] **Step 3: Write the reference files**

- `reference/flow-patterns.md`: annotated patterns — a bulk-safe record-triggered flow structure, a fault-path pattern, an entry-conditions example (described structurally: element names and connections, since flows are builder-made).
- `reference/naming.md`: the settled naming pattern with at least four worked examples (flow names, element names, variable names).

- [ ] **Step 4: Validate**

Run: `grep -c '^name: salesforce-flow$' plugins/salesforce-standards/skills/salesforce-flow/SKILL.md`
Expected: `1`

Run: `grep -c 'trigger moment' plugins/salesforce-standards/skills/salesforce-flow/SKILL.md`
Expected: non-zero.

Run: `grep -c 'Process Builder' plugins/salesforce-standards/skills/salesforce-flow/SKILL.md`
Expected: non-zero (retired-automation stance present).

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-flow/
git commit -m "feat(salesforce-standards): add salesforce-flow skill"
```

---

### Task 7: salesforce-data-model skill

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-data-model/SKILL.md`
- Create: `plugins/salesforce-standards/skills/salesforce-data-model/reference/naming.md`
- Create: `plugins/salesforce-standards/skills/salesforce-data-model/reference/cmt-vs-custom-settings.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: skill name `salesforce-data-model` (Tasks 12, 13, 15); the declarative surfaces its standards govern (objects, fields, record types, validation rules, CMT records, global value sets) — cited by Task 13's run scope.

- [ ] **Step 1: Collect the standards and settle contested points**

Author from the object/field metadata documentation and Well-Architected data guidance. Ask the developer to settle: field API-name conventions (suffixes, abbreviations), the description-required policy (all fields vs custom only), and validation-rule naming. Anything unsettled becomes an open question.

- [ ] **Step 2: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: salesforce-data-model
description: Use when creating or naming Salesforce objects and fields — object and field naming, record types, validation rules, Custom Metadata Types vs Custom Settings, global value sets, hardcoded-ID bans, and field descriptions. Access to the data belongs to salesforce-security-model.
---
```

Mandatory content:

- Object and field naming: API-name conventions settled in Step 1; labels vs API names.
- Field descriptions: the policy settled in Step 1 — a field without a description is a review finding under that policy.
- Record types: naming, when a record type vs a picklist-driven variation.
- Validation rules: naming per Step 1, user-actionable error messages, bypass strategy (e.g. a permission-based bypass) named explicitly.
- Custom Metadata Types vs Custom Settings: CMT for deployable configuration, the narrow remaining cases for (hierarchy) Custom Settings.
- Global value sets for shared picklists; no duplicated inline value lists across objects.
- No hardcoded IDs — anywhere: not in code, formulas, flows, or validation rules; the alternatives (custom labels, CMT, queries by developer name).

- [ ] **Step 3: Write the reference files**

- `reference/naming.md`: the settled conventions with worked examples — objects, fields (each type), record types, validation rules.
- `reference/cmt-vs-custom-settings.md`: the decision table plus one worked example of each (a CMT type with records; a hierarchy Custom Setting), annotated with why.

- [ ] **Step 4: Validate**

Run: `grep -c '^name: salesforce-data-model$' plugins/salesforce-standards/skills/salesforce-data-model/SKILL.md`
Expected: `1`

Run: `grep -ci 'hardcoded' plugins/salesforce-standards/skills/salesforce-data-model/SKILL.md`
Expected: non-zero.

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-data-model/
git commit -m "feat(salesforce-standards): add salesforce-data-model skill"
```

---

### Task 8: salesforce-security-model skill

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-security-model/SKILL.md`
- Create: `plugins/salesforce-standards/skills/salesforce-security-model/reference/access-model.md`
- Create: `plugins/salesforce-standards/skills/salesforce-security-model/reference/permission-set-patterns.md`

**Interfaces:**
- Consumes: the sharing-keyword boundary from Task 3 (two homes: keyword mechanics there, access-model design here — reference by skill name).
- Produces: skill name `salesforce-security-model` (Tasks 12, 13, 15); the permission-set-first stance cited by Task 11's checklist; the declarative surfaces it governs (permission sets, sharing rules, profiles) — cited by Task 13's run scope.

- [ ] **Step 1: Collect the standards and settle contested points**

Author from the sharing/security documentation and Well-Architected access guidance. Ask the developer to settle: the OWD default stance (private-by-default vs case-by-case) and the permission-set-group usage policy. Anything unsettled becomes an open question.

- [ ] **Step 2: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: salesforce-security-model
description: Use when designing Salesforce data access — org-wide defaults, role hierarchy, profiles vs permission sets (permission-set-first), sharing rules, and field-level security in code and UI. Sharing keyword mechanics in Apex belong to salesforce-apex.
---
```

Mandatory content:

- Org-wide defaults: the stance settled in Step 1; OWD as the access floor, opened selectively.
- Role hierarchy: what it grants, keeping it shallow and org-chart-decoupled.
- Permission-set-first: profiles reduced to the login/defaults shell; capabilities granted by permission sets (and permission set groups per the Step 1 policy) — a capability added to a profile instead of a permission set is a review finding.
- Sharing rules: criteria vs ownership rules, naming, documenting why each exists.
- FLS: enforced in UI and code — `WITH USER_MODE` / `Security.stripInaccessible` for Apex touchpoints (mechanics of the keywords belong to salesforce-apex; name the skill).
- The design questions to answer before adding any access grant (who needs it, narrowest scope, expiry/review).

- [ ] **Step 3: Write the reference files**

- `reference/access-model.md`: a worked access-model design for one object — OWD choice, role considerations, the permission sets that open it, with the reasoning annotated.
- `reference/permission-set-patterns.md`: permission-set decomposition patterns (per-capability, per-app), naming, and an anti-pattern pair (profile-stuffed vs permission-set-first).

- [ ] **Step 4: Validate**

Run: `grep -c '^name: salesforce-security-model$' plugins/salesforce-standards/skills/salesforce-security-model/SKILL.md`
Expected: `1`

Run: `grep -c 'permission-set-first' plugins/salesforce-standards/skills/salesforce-security-model/SKILL.md`
Expected: non-zero.

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-security-model/
git commit -m "feat(salesforce-standards): add salesforce-security-model skill"
```

---

### Task 9: salesforce-aura skill

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-aura/SKILL.md`
- Create: `plugins/salesforce-standards/skills/salesforce-aura/reference/events.md`

**Interfaces:**
- Consumes: the maintenance-first stance (Global Constraints, verbatim substance); the LWC-preference boundary with Task 5 (reference by skill name).
- Produces: skill name `salesforce-aura` (Tasks 12, 13, 15).

- [ ] **Step 1: Collect the standards**

Author from the Aura components documentation. Contested points are unlikely (maintenance content); if any arise, ask the developer.

- [ ] **Step 2: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: salesforce-aura
description: Use when maintaining existing Aura components — markup, controller and helper JavaScript, component vs application events, and Lightning Data Service. Maintenance-first; new UI belongs to salesforce-lwc unless the platform forces Aura.
---
```

Mandatory content:

- Maintenance-first clause up front (verbatim substance): existing Aura code is held to these standards; new UI is built in LWC unless the platform forces Aura (where LWC support is missing) — new Aura surface without a named platform forcing reason is a review finding.
- Markup: attribute typing, expression discipline, `aura:if` vs CSS toggling.
- Controller vs helper: controllers thin (event wiring), logic in helpers; no business logic in components — delegate to Apex.
- Events: component events for parent-child, application events only for cross-tree needs; naming and payload discipline.
- Lightning Data Service (`force:recordData`) over ad-hoc Apex for single-record CRUD.
- Migration direction: what to check before converting a component to LWC (feature parity, event contracts).

- [ ] **Step 3: Write the reference file**

- `reference/events.md`: component vs application event worked examples — registration, firing, handling — with the decision rule annotated, plus one migration-assessment checklist for an Aura→LWC conversion.

- [ ] **Step 4: Validate**

Run: `grep -c '^name: salesforce-aura$' plugins/salesforce-standards/skills/salesforce-aura/SKILL.md`
Expected: `1`

Run: `grep -ci 'maintenance-first' plugins/salesforce-standards/skills/salesforce-aura/SKILL.md`
Expected: non-zero.

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-aura/
git commit -m "feat(salesforce-standards): add salesforce-aura skill"
```

---

### Task 10: salesforce-visualforce skill

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-visualforce/SKILL.md`
- Create: `plugins/salesforce-standards/skills/salesforce-visualforce/reference/controller-patterns.md`

**Interfaces:**
- Consumes: the maintenance-first stance (Global Constraints, verbatim substance); the LWC-preference boundary with Task 5 (reference by skill name).
- Produces: skill name `salesforce-visualforce` (Tasks 12, 13, 15).

- [ ] **Step 1: Collect the standards**

Author from the Visualforce Developer Guide. Contested points are unlikely (maintenance content); if any arise, ask the developer.

- [ ] **Step 2: Scaffold and author the skill**

Invoke `skill-creator`; follow `superpowers:writing-skills`. Frontmatter exactly:

```yaml
---
name: salesforce-visualforce
description: Use when maintaining existing Visualforce pages — standard controllers, extensions, custom controllers, view state discipline, and data binding. Maintenance-first; new UI belongs to salesforce-lwc unless the platform forces Visualforce (e.g. PDF rendering).
---
```

Mandatory content:

- Maintenance-first clause up front (verbatim substance): existing Visualforce is held to these standards; new UI is built in LWC unless the platform forces Visualforce (the canonical case: PDF rendering with `renderAs="pdf"`) — new Visualforce surface without a named platform forcing reason is a review finding.
- Controller choice ladder: standard controller → standard controller + extension → custom controller, and what justifies each step up.
- View state discipline: transient variables, minimal state, the view state limit as a design constraint.
- Data binding: bind through controller properties, no logic in expressions; `apex:repeat` discipline.
- Security: `escape="false"` requires a stated justification; FLS respected via the security-model standards (name salesforce-security-model, do not restate).

- [ ] **Step 3: Write the reference file**

- `reference/controller-patterns.md`: the controller-choice ladder with one worked example per rung, plus a view-state-reduction before/after pair, annotated.

- [ ] **Step 4: Validate**

Run: `grep -c '^name: salesforce-visualforce$' plugins/salesforce-standards/skills/salesforce-visualforce/SKILL.md`
Expected: `1`

Run: `grep -ci 'maintenance-first' plugins/salesforce-standards/skills/salesforce-visualforce/SKILL.md`
Expected: non-zero.

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 5: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-visualforce/
git commit -m "feat(salesforce-standards): add salesforce-visualforce skill"
```

---

### Task 11: salesforce-plan-review checklist skill

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-plan-review/SKILL.md`

**Interfaces:**
- Consumes: the working-process `*-plan-review` discovery convention (description starts with "Plan-review checklist for <domain>", ends with "invoked by the plan-adversary agent"); stances from Tasks 3, 6, 8 (referenced, not restated).
- Produces: skill name `salesforce-plan-review` (Task 15's README; Task 16's discovery verification).

- [ ] **Step 0: Confirm contested points with the developer**

Ask the developer to confirm the severity grades assigned in the checklist below before writing. This is a skill-content task; the Global Constraints content-input rule applies.

- [ ] **Step 1: Write `plugins/salesforce-standards/skills/salesforce-plan-review/SKILL.md`**

Invoke `skill-creator` for scaffolding; content below is the baseline, amended with the Step 0 outcomes:

```markdown
---
name: salesforce-plan-review
description: Plan-review checklist for Salesforce — metadata blast radius, governor limits at target volumes, security model, automation overlap, deployment dependencies and ordering; invoked by the plan-adversary agent.
---

# Salesforce plan-review checklist

Walk every dimension against the reviewed plan; nothing passes by
default. Every finding cites a plan quote or file path as evidence.
Severities noted per dimension bind — do not re-grade them.

## 1. Metadata blast radius

- The plan names every metadata type it touches and the components
  affected. A silent touch of shared metadata (profiles, permission
  sets, layouts, shared objects) → Important.
- A change to a shared object or field without listing its consumers
  (code, flows, reports, integrations) → Important.

## 2. Governor limits at target volumes

- SOQL or DML inside a loop planned on a trigger or bulk path →
  Critical.
- The plan states expected record volumes for every bulk path;
  unstated volumes on triggers, batch, or record-triggered flows →
  Important.

## 3. Security model

- A new object or field without a stated org-wide default, FLS, and
  permission-set assignment → Important.
- Planned Apex without a sharing declaration, or `without sharing`
  lacking a stated justification → Important.
- A capability granted to a profile where a permission set is the
  standard → Important.

## 4. Automation overlap

- A new trigger or record-triggered flow on an object that already has
  one for the same trigger moment, without an interaction note →
  Important.
- Any new Workflow Rule or Process Builder automation → Critical
  (retired surface; Flow is the target). Deliberately one grade above
  the code-review rubric's Important for the same surface: at plan
  time the design can still change; post-hoc review grades by the
  shared severity definitions.

## 5. Deployment dependencies and ordering

- Metadata with deploy-order dependencies (fields before permission
  sets and layouts, CMT types before their records) not sequenced in
  the plan → Important.
- Org changes outside sf CLI deployments (manual Setup steps) not
  flagged as manual steps with an owner → Important.
```

- [ ] **Step 2: Validate**

Run: `grep -c '^description: Plan-review checklist for Salesforce' plugins/salesforce-standards/skills/salesforce-plan-review/SKILL.md`
Expected: `1`

Run: `grep -c 'invoked by the plan-adversary agent' plugins/salesforce-standards/skills/salesforce-plan-review/SKILL.md`
Expected: `1`

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 3: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-plan-review/
git commit -m "feat(salesforce-standards): add salesforce-plan-review checklist skill"
```

---

### Task 12: Rules payload — rules/salesforce-toolchain.md

**Files:**
- Create: `plugins/salesforce-standards/rules/salesforce-toolchain.md`

**Interfaces:**
- Consumes: skill names from Tasks 3–10 exactly as defined there (conditional pointers only).
- Produces: the Rules payload picked up by working-process's Rules engine (Task 16 verifies the sync-rules install); this makes salesforce-standards a payload plugin.

- [ ] **Step 1: Write `plugins/salesforce-standards/rules/salesforce-toolchain.md`**

```markdown
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
```

- [ ] **Step 2: Hand-check the rule frontmatter**

`claude plugin validate` skips `rules/` — review by hand: the YAML block parses, all twenty `paths` entries are quoted, no scalar contains an unquoted `: `.

Run: `sed -n '1,23p' plugins/salesforce-standards/rules/salesforce-toolchain.md`
Expected: the frontmatter block exactly as written above.

- [ ] **Step 3: Validate conditionality**

Run: `grep -c 'When the salesforce-standards plugin' plugins/salesforce-standards/rules/salesforce-toolchain.md`
Expected: `1` (skill mentions are conditional — committed project-level rules load for people without the plugin).

- [ ] **Step 4: Commit**

```bash
git add plugins/salesforce-standards/rules/salesforce-toolchain.md
git commit -m "feat(salesforce-standards): add salesforce-toolchain Rules payload"
```

---

### Task 13: salesforce-code-review skill

**Sequencing gate:** Task 2 (the working-process line-less-ordering amendment) must be merged on this branch before this task starts — the fallback below subsets the AMENDED contract.

**Files:**
- Create: `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`

**Interfaces:**
- Consumes: skill names from Tasks 3–10; the Contract probe paths, the filename element, and the line-less-findings provision from `plugins/working-process/rules/review-reports.md` as amended by Task 2.
- Produces: skill name `salesforce-code-review` and its procedure, consumed verbatim by Task 14's agent and command; the `*-code-review` name pattern a future working-process review orchestrator will discover.

- [ ] **Step 0: Confirm the severity rubric with the developer**

Ask the developer to confirm the Critical/Important/Minor definitions
in the grading step below, including the deliberate one-grade gap
against Task 11's plan-time Critical for new retired automation
(plan-time: the design can still change; review-time: grade by the
shared severity definitions). This mirrors Task 11's Step 0.

- [ ] **Step 1: Read the amended contract**

Read `plugins/working-process/rules/review-reports.md` (post-Task-2). Confirm it contains the line-less-findings provision ("domain-stated stable key"). The inline fallback below must remain a STRICT SUBSET of that contract — if the released rule text differs from this plan's assumptions, the rule wins; adjust the fallback before writing.

- [ ] **Step 2: Write `plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`**

Invoke `skill-creator` for scaffolding and description tuning; the content baseline:

```markdown
---
name: salesforce-code-review
description: Use when auditing existing Salesforce code and metadata against the salesforce-standards skills — invoked by the /salesforce-review command or the salesforce-code-reviewer agent.
---

# Salesforce code review

Audit Salesforce code and metadata against the standards skills of
this plugin and write one Review report per run.

## Run scope

Review the files the standards skills cover:

- Apex: `*.cls`, `*.trigger`
- LWC bundles (`lwc/` directories)
- Aura bundles (`aura/` directories)
- Visualforce: `*.page`, `*.component`
- Flow metadata: `*.flow-meta.xml`
- Retired automation: `*.workflow-meta.xml` (Workflow Rules; Process
  Builder processes arrive as Flow metadata)
- Declarative data and access metadata: `*.object-meta.xml`,
  `*.field-meta.xml`, `*.recordType-meta.xml`,
  `*.validationRule-meta.xml`, `*.md-meta.xml` (Custom Metadata
  records), `*.globalValueSet-meta.xml`, `*.permissionset-meta.xml`,
  `*.permissionsetgroup-meta.xml`, `*.sharingRules-meta.xml`,
  `*.profile-meta.xml`

Static resources are in scope narrowly: flag NEW or MODIFIED custom
application JavaScript landing in a static resource (a placement
finding per salesforce-lwc); never review static-resource content
line-by-line; never review third-party libraries.

Files outside the domain that fall inside the requested scope are NOT
reviewed — list them in the report's Summary as out of scope.

## Metadata-reviewed files

Flow and declarative metadata files are reviewed from metadata, not
XML lines: findings cite elements by name (Flow elements, object and
field API names, permission-set grants). Within a severity subsection,
line-anchored findings come in ascending line order; findings without
a line anchor are ordered alphabetically by cited element name — this
domain's stable key under the shared contract's line-less-findings
provision.

## Procedure

1. Determine the scope: the current diff by default, or the files
   named by the caller.
2. Load the standards skills relevant to the content under review:
   salesforce-apex for any Apex; salesforce-apex-testing,
   salesforce-lwc, salesforce-flow, salesforce-data-model,
   salesforce-security-model, salesforce-aura, salesforce-visualforce
   as the content demands.
3. Grade every finding:
   - **Critical** — a defect that corrupts data, breaks security or
     sharing, or blows a governor limit on a bulk path.
   - **Important** — violates a standard in a way that forces rework
     or hides bugs (including new legacy-UI or retired-automation
     surface without a named platform forcing reason).
   - **Minor** — naming, style, documentation.
   Cite the standard for each finding (`standard: <skill>, rule: <id>`
   where the skill defines rule ids, e.g. PMD rule names).
4. Write the Review report (next section).
5. Reply with the report path and the findings grouped by severity; a
   zero-findings run still writes the report and states the result.

## Report contract

Run the Contract probe FIRST — do not assume the shared rule is in
context: check, in order,
`<project>/.claude/rules/working-process/review-reports.md`, then
`$HOME/.claude/rules/working-process/review-reports.md`; the first
file found wins. When the Contract probe succeeds, read that file and
follow it fully — **the installed working-process review-reports rule
supersedes the inline fallback below.**

## Inline fallback (Standalone install)

When the Contract probe finds nothing, this minimal contract applies —
a strict subset of the shared review-reports contract, never a
different shape:

- **Location**: `<project-root>/docs/code-review/`; create the
  directory if absent (the first-create mode question belongs to
  working-process's process-artifacts rule and is absent in a
  Standalone install).
- **Filename**: `<YYYY-MM-DD>-<scope-slug>-<runid>.md` — the date as
  the session knows it, `runid` 8 lowercase hex characters the run's
  owner generates itself; generated prompt-free (no shell commands, no
  questions). Never overwrite: check for an existing file with the
  session's file tools; on a collision generate a new runid and retry.
- **Frontmatter**: `ticket` (from context or branch, else `none`;
  never block on a question), `standards: salesforce-standards`,
  `findings: { critical: N, important: N, minor: N }` — the counts
  MUST equal the body.
- **Body**: a Summary section (scope reviewed, out-of-scope files,
  headline counts), then per-file sections with Critical → Important →
  Minor subsections — line-ascending within a subsection, line-less
  findings alphabetically by cited element name; omit no-findings
  files and empty severity sections; a zero-findings run still writes
  the document.
- Never stage or commit the report — committing is the developer's
  per-report decision.
- No git root, or the file cannot be written → emit the full report in
  the reply and state why no file was written.
```

- [ ] **Step 3: Validate**

Run: `grep -c 'supersedes the' plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`
Expected: `1` (precedence line present).

Run: `grep -c 'review-reports.md' plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`
Expected: `2` (both Contract probe paths, project then user order).

Run: `grep -c 'findings: { critical' plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`
Expected: `1` (shared counts key in the fallback).

Run: `grep -c 'alphabetically by cited element name' plugins/salesforce-standards/skills/salesforce-code-review/SKILL.md`
Expected: `2` (the stable key stated in both the metadata section and the fallback).

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 4: Commit**

```bash
git add plugins/salesforce-standards/skills/salesforce-code-review/
git commit -m "feat(salesforce-standards): add salesforce-code-review skill"
```

---

### Task 14: salesforce-code-reviewer agent and /salesforce-review command

Runs after Task 13 (both surfaces delegate to the skill).

**Files:**
- Create: `plugins/salesforce-standards/agents/salesforce-code-reviewer.md`
- Create: `plugins/salesforce-standards/commands/salesforce-review.md`

**Interfaces:**
- Consumes: skill name `salesforce-code-review` and its procedure (Task 13) — both surfaces delegate to it, never restate the contract.
- Produces: agent name `salesforce-code-reviewer` and command `/salesforce-review` (Task 15's README; Task 16's verification). One `salesforce-` family per the naming rule; agent = actor to the skill's activity.

- [ ] **Step 1: Write `plugins/salesforce-standards/agents/salesforce-code-reviewer.md`**

```markdown
---
name: salesforce-code-reviewer
description: "Reviews Salesforce code and metadata — a diff or named files — against the salesforce-standards skills, writes the review report to docs/code-review/, and returns findings by severity. Salesforce files only; out-of-domain files are noted in the report Summary as out of scope."
---

Code reviewer for Salesforce. FIRST ACTION: load the
`salesforce-code-review` skill of this plugin and follow it end to end
— run scope, standards skills, severity grading, the Contract probe,
and report writing.

- Review exactly what the dispatch prompt names: the given diff or the
  given files; nothing else.
- One run, one report — this agent is the run's owner (`mode: agent`
  when the shared review-reports contract applies).
- Never stage or commit the report.
- Reply with the report path and the findings grouped Critical →
  Important → Minor; zero findings is still a written report and a
  stated result.
```

- [ ] **Step 2: Write `plugins/salesforce-standards/commands/salesforce-review.md`**

```markdown
---
description: Review the current diff (or named files) against the Salesforce coding standards
---

Review Salesforce code and metadata against the salesforce-standards
skills.

1. Load the `salesforce-code-review` skill and follow it end to end.
2. Scope: `$ARGUMENTS` when given (named files); otherwise the current
   diff — staged plus unstaged changes, or, on a clean tree, the diff
   of the current branch against its base.
3. Salesforce files only, per the skill's run scope; note
   out-of-domain files in the report Summary as out of scope.
4. Write the review report per the skill's report contract and reply
   with the report path and findings by severity.
```

- [ ] **Step 3: Validate**

Run: `grep -c '^name: salesforce-code-reviewer$' plugins/salesforce-standards/agents/salesforce-code-reviewer.md`
Expected: `1`

Run: `grep -c 'docs/code-review/' plugins/salesforce-standards/agents/salesforce-code-reviewer.md`
Expected: `1` (report destination named in the agent description).

Run: `grep -c 'FIRST ACTION' plugins/salesforce-standards/agents/salesforce-code-reviewer.md`
Expected: `1` (the agent's skill-delegation line is load-bearing — a bare-name grep would be satisfied by the agent's own `salesforce-code-reviewer` name).

Run: `grep -c 'Load the .salesforce-code-review. skill' plugins/salesforce-standards/commands/salesforce-review.md`
Expected: `1` (the command delegates to the skill).

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 4: Commit**

```bash
git add plugins/salesforce-standards/agents/salesforce-code-reviewer.md plugins/salesforce-standards/commands/salesforce-review.md
git commit -m "feat(salesforce-standards): add salesforce-code-reviewer agent and /salesforce-review command"
```

---

### Task 15: Plugin README

**Files:**
- Create: `plugins/salesforce-standards/README.md`

**Interfaces:**
- Consumes: component names and contracts from Tasks 1–14 exactly as defined there. Runs after Task 14 (it documents the review stack).

- [ ] **Step 1: Write `plugins/salesforce-standards/README.md`**

```markdown
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
```

- [ ] **Step 2: Validate**

Run: `grep -c 'salesforce-apex\|salesforce-apex-testing\|salesforce-lwc\|salesforce-flow\|salesforce-data-model\|salesforce-security-model\|salesforce-aura\|salesforce-visualforce\|salesforce-code-review\|salesforce-plan-review\|salesforce-code-reviewer\|salesforce-review' plugins/salesforce-standards/README.md | awk '{print ($1>=12) ? "ok" : "missing components"}'`
Expected: `ok`

Run: `claude plugin validate plugins/salesforce-standards`
Expected: passes.

- [ ] **Step 3: Commit**

```bash
git add plugins/salesforce-standards/README.md
git commit -m "docs(salesforce-standards): add plugin README"
```

---

### Task 16: End-to-end verification

Runs the spec's Verification section. No plugin files change in this task; findings loop back into the task that owns the broken file.

**Files:**
- None created; fixes (if any) modify the owning task's files and follow that task's commit style.

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Structural validation**

Run: `claude plugin validate .` and `claude plugin validate plugins/salesforce-standards` (repo root).
Expected: both pass, no errors.

- [ ] **Step 2: Marketplace-sync check**

Run: `git log --format=%h -1 -- plugins/salesforce-standards/.claude-plugin/plugin.json` and `git show --stat <that-hash>`
Expected: the manifest's landing commit also touches `.claude-plugin/marketplace.json` and `README.md` (catalog entry + README row in the same commit as the manifest).

- [ ] **Step 3: Companion amendment check**

Run: `grep -c 'domain-stated stable' plugins/working-process/rules/review-reports.md; jq -r '.version' plugins/working-process/.claude-plugin/plugin.json`
Expected: `1` and `0.9.0` — the amended contract text and the bump landed together (Task 2's single commit; verify with `git log --format=%h -1 -- plugins/working-process/rules/review-reports.md` + `git show --stat`).

- [ ] **Step 4: Install from the local marketplace**

In a Claude Code session: `/plugin marketplace update missing-bits` (the local marketplace is already added on the development machine; otherwise `/plugin marketplace add <local path to this repo root>`), then `/plugin install salesforce-standards@missing-bits`.
Expected: install succeeds with no dependency resolution (no `dependencies` edge).

- [ ] **Step 5: Component visibility**

In the same session, confirm the skills list shows all ten skills under the plugin namespace (`salesforce-standards:salesforce-apex`, `-apex-testing`, `-lwc`, `-flow`, `-data-model`, `-security-model`, `-aura`, `-visualforce`, `-code-review`, `-plan-review`), the agent `salesforce-standards:salesforce-code-reviewer` appears among agent types, and `/salesforce-review` resolves as a command.

**Namespace quarantine (Steps 6–8):** a machine may carry another
installed plugin shipping identically named bare `salesforce-*` skills;
Steps 6–8 therefore run under clean profiles (fresh
`CLAUDE_CONFIG_DIR`) where no such plugin is enabled, and every
expected skill resolution below is namespace-qualified — bare-name
evidence proves nothing.

- [ ] **Step 6: /salesforce-review — shared contract profile (working-process installed)**

Under a clean profile with ONLY working-process (≥ 0.9.0, its rules installed via sync-rules) and salesforce-standards installed: in a scratch git repo containing a small Salesforce diff with deliberate standards violations (e.g. a SOQL query inside a trigger loop, a new field without a description, and a flow element missing a fault path), run `/salesforce-review`.
Expected: the Contract probe finds `review-reports.md`; the loaded skills resolve to the plugin's namespace (`salesforce-standards:salesforce-code-review`, `salesforce-standards:salesforce-apex`, …); the report lands in `docs/code-review/` with the SHARED format (full frontmatter set per the rule, `standards: salesforce-standards`); the flow finding cites its element by name and line-less findings order alphabetically; nothing staged.

- [ ] **Step 7: /salesforce-review — Standalone install profile**

Repeat Step 6 under a second clean profile with ONLY salesforce-standards installed and no working-process rules present.
Expected: the Contract probe finds nothing; the skill creates `docs/code-review/` without asking any mode question; the report carries exactly the fallback frontmatter (`ticket`, `standards: salesforce-standards`, `findings:` counts matching the body) with the Summary and per-file severity layout, line-less findings ordered alphabetically by cited element name.

- [ ] **Step 8: plan-adversary discovery**

Under the same clean profile as Step 6, dispatch the working-process plan-adversary agent on any Salesforce-touching plan (a plan referencing the scratch repo's changes qualifies).
Expected: its report shows `salesforce-standards:salesforce-plan-review` (namespace-qualified) was discovered and loaded as a domain checklist.

- [ ] **Step 9: sync-rules foreign payload install**

In a project with working-process rules installed, run the sync-rules skill after installing salesforce-standards.
Expected: it offers and installs `salesforce-toolchain.md` into the rules target under `rules/salesforce-standards/`; immediately afterwards the drift hook stays silent (manifest hash matches upstream). Additionally: the working-process 0.9.0 bump makes previously-installed working-process rule sets report drift — sync-rules updates them and the amended review-reports rule arrives; this is the expected delivery path, not a bug.

- [ ] **Step 10: Record deviations**

Any deviation is a bug in the owning task's file — fix it there, re-run the failed step, and commit the fix as `fix(salesforce-standards): <what>` (or `fix(working-process): <what>` for Task 2 regressions), single line.

---

### Task 17: Frontmatter closure

**Files:**
- Modify: `docs/specs/2026-07-20-salesforce-standards-design.md` (frontmatter `status` only)
- Modify: `docs/plans/2026-07-20-salesforce-standards.md` (frontmatter `status` only)

**Interfaces:**
- Consumes: Task 16 fully green.

- [ ] **Step 1: Mark the spec and the plan implemented**

With the Edit tool (not shell one-liners), change `status: approved` to `status: implemented` in the spec and the then-current `status` value to `status: implemented` in this plan.

- [ ] **Step 2: Offer the docs commit to the developer**

The repo's `docs/` directories are in tracked mode; the developer commits process documents collectively. List the touched documents (spec, this plan, the review-reports spec amendment) and remind that they belong with this work's commits — do NOT commit them unasked; committing stays with the developer.

## Adversary findings — 2026-07-20 round 1

Dispatched on Fable 5 (prescribed tier); verdict: blocking.

- **Important**: Task 16 Steps 6/8 ran on the developer's main
  profile, where another installed plugin ships identically named bare
  `salesforce-*` skills — both steps could pass by exercising the
  wrong plugin. → Fixed: Steps 6–8 run under clean profiles (namespace
  quarantine note), and all expected skill resolutions are
  namespace-qualified.
- **Important**: the permission-set-group policy Task 8 settles had no
  matching surface (stance–surface coupling violated by the plan's own
  watch-rule). → Fixed: `**/*.permissionsetgroup-meta.xml` added to
  the payload paths (twenty entries) and Task 13's run scope; the spec
  gained the same glob and run-scope mention.
- **Minor**: Task 2 committed the review-reports spec amendment while
  Task 17 listed it as developer-committed. → Fixed: dropped from Task
  2's commit; Task 17's offer owns it.
- **Minor**: Task 2's version contingency contradicted Task 16's hard
  `0.9.0` expectations. → Fixed: contingency replaced with STOP and
  consult the developer.
- **Minor**: Task 4 claimed a coverage-floor interface Task 11 never
  consumes. → Fixed: claim dropped.
- **Minor**: Task 14's delegation grep was vacuous (`salesforce-code-review`
  is a substring of the agent's own name). → Fixed: greps load-bearing
  phrases (`FIRST ACTION`; the command's delegation line).
- **Minor**: new retired automation graded Critical in Task 11 but
  Important in Task 13 with no stated reason. → Fixed: the one-grade
  gap is now stated as deliberate in both tasks, and Task 13 gained a
  Step 0 rubric confirmation mirroring Task 11's.

Round 2 (verification pass, Fable 5): all seven dispositions
confirmed — quarantined verification steps with namespace-qualified
evidence, twenty payload globs consistent across plan and spec,
Task 2/17 commit ownership reconciled, STOP-guarded version bump,
dangling interface removed, load-bearing delegation greps, the
severity gap stated as deliberate on both surfaces. No new findings.
Verdict: LGTM.

## Implementation record — 2026-07-20/21 (SDD, subagent-driven)

All 17 tasks executed via subagent-driven development on branch
`feature/3-salesforce-standards`, per-task spec+quality review with fix
loops, then a whole-branch review (Opus 4.8).

Deviations from the plan as written, all deliberate:

- **Task 3 reference format**: `salesforce-apex/reference/trigger-handler.cls`
  became `trigger-handler.md` — a single `.cls` cannot hold a trigger plus
  its classes (invalid Apex; IDE parse error), so the reference is a
  per-compilation-unit markdown walkthrough, each fenced block individually
  valid. Reviewer-approved.
- **Version**: the plugin stays at `0.1.0` across the whole branch per the
  plan's Global Constraints (no per-commit bump before first release); a
  final-review fixer's incidental bump to 0.1.1 was reverted (`935b7c3`).

Whole-branch review found one blocking severity-consistency defect —
`salesforce-flow`, `salesforce-aura`, `salesforce-visualforce` graded new
legacy-UI / retired-automation surface `Critical` where the code-review
rubric, `salesforce-decisions.md`, and the plan-review checklist pin
review-time to `Important` (the deliberate plan-time-vs-review-time gap).
Fixed in `432ab2a` (lowered the three domain skills to Important), together
with three recommended minors (WITH USER_MODE CRUD wording; aura events.md
summary nuance; LWC wire-error handling in the reference component).

Task 16 steps 1–3 (structural validation, marketplace-sync one-commit,
companion-amendment + 0.9.0 bump one-commit) passed in-session; steps 4–9
(local-marketplace install, `/salesforce-review` under both install
profiles, plan-adversary discovery of `salesforce-plan-review`, sync-rules
foreign-payload install) are the developer's interactive smoke test.

The working-process companion amendment (review-reports line-less-ordering
provision, 0.8.0 → 0.9.0) shipped in `ccad94d`; its review-reports spec
amendment record is written and awaits this docs commit.
