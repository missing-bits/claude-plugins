# Changelog — python-standards

Released versions of this plugin, newest first.

## 0.3.2 — 2026-09-15

- The plugin ships this changelog.

## 0.3.1 — 2026-08-12

- The store-probe restatement in the code-review skill tests the
  Project-memory part directories, matching the updated review-reports
  contract. Behavior-compatible for every store the plugin ever created.

## 0.3.0 — 2026-08-05

- The review cascade grades from the tags: a plugin-level `rule-none`,
  a justify clause, the finding unit, candidate-gap offers, and a
  standalone fallback.
- `/python-review` dispatches the reviewer in the background, with the
  first-create check gated by a store probe.
- A rerun can no longer inherit a prior report's counting policy.

## 0.2.0 — 2026-07-23

- Six area skills: code-style, project-layout, typing, testing, cli,
  and web-api.
- The `python-code-review` skill, the `python-code-reviewer` agent, the
  `/python-review` command, and the `python-plan-review` checklist
  skill.
- The `python-toolchain` Rules payload, with ruff's line length set to
  120.
- Every rule names its source — a PEP, an RFC, the official docs, or
  this standard. The web-api skill adopts RFC 9457 problem details with
  a `code` extension member, and the docstring norm is Google style with
  a project override.
- The area skills adopt the severity-in-tag model.

## 0.1.0 — 2026-07-16

- The plugin joins the marketplace.
