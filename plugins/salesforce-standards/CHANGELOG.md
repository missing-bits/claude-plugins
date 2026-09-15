# Changelog — salesforce-standards

Released versions, newest first. The marketplace serves what `master`
holds; `## Unreleased` collects what has landed on `develop` since the
last release.

## 0.4.0 — 2026-09-15

- The new `salesforce-triggers` skill carries the rules that hold
  whatever framework a project uses, and the trigger content leaves
  `salesforce-apex`.
- A resolution protocol identifies the project's trigger framework
  before Apex is graded, and three documents describe what each one
  expects — frameworkless, base-class, and metadata-driven — with a
  comparison for choosing among them.
- The toolchain rule routes triggers and documents the declaration keys,
  naming `.claude/CLAUDE.md` among the homes a declaration may take.
- The plugin ships this changelog.

## 0.3.1 — 2026-08-12

- The store-probe restatement in the code-review skill tests the
  Project-memory part directories, matching the updated review-reports
  contract. Behavior-compatible for every store the plugin ever created.

## 0.3.0 — 2026-08-05

- The review cascade grades from the tags: a plugin-level `rule-none`,
  a justify clause, the finding unit, candidate-gap offers, and a
  standalone fallback.
- `/salesforce-review` dispatches the reviewer in the background, with
  the first-create check gated by a store probe.
- The severity-in-tag model reaches the remaining area skills — lwc,
  flow, data-model, security-model, aura, and visualforce.
- A rerun can no longer inherit a prior report's counting policy.

## 0.2.0 — 2026-07-23

- Eight area skills: apex, apex-testing, lwc, flow, data-model,
  security-model, aura, and visualforce.
- The `salesforce-code-review` skill, the `salesforce-code-reviewer`
  agent, and the `/salesforce-review` command.
- The `salesforce-plan-review` checklist skill and the
  `salesforce-toolchain` Rules payload.
- Apex and apex-testing adopt the severity-in-tag model.

## 0.1.0 — 2026-07-20

- The plugin joins the marketplace.
