# Changelog — working-process

Released versions, newest first. The marketplace serves what `master`
holds; `## Unreleased` collects what has landed on `develop` since the
last release.

## 0.17.0 — 2026-09-15

- A plan's review loop closes only on a full-document round: a
  diff-scoped LGTM certifies a chain, so one confirming round follows it
  and carries the stamp. The rules define which heading counts as the
  latest, widen the plan exception to the relay-then-stamp order, and
  bound what the round cap promises.
- The propagation duties ship as an author-facing rule, so an author
  meets them while writing rather than through the auditor's hits. Two
  hits on one document are reported as a shape, and the co-firing line
  states a shape rather than a judgment.
- The verdict relay opens with a header line — verdict, model
  self-report, findings by severity, decisions awaiting the developer —
  and every dispatch writes a record to `.claude/working-process/`
  before the relay. A consultation meets the same floor in its record,
  and its relay digests one paragraph per focusing question.
- The plan adversary emits each finding's origin, triage holds a
  spec-origin finding unless a written decision licenses the edit, and a
  licensed cross-document fix lands in the spec's own ledger.
- Feature work follows the published branch-naming convention,
  `feature/<ticket>-<short-name>`.
- The plugin ships this changelog.

## 0.16.0 — 2026-09-07

- A reviewer's citation is verified against what it names before it
  enters the record. A precise citation reads like verification and is
  not one, so the dispatcher checks the file, the line, and the
  identifier the report quotes.
- An audit report's body governs, never its closing token: located hits
  beside a `CLEAN` line mean the gate has not passed.
- The propagation audit parts a prescribed block from a reported one,
  and both identity surfaces name the partition.
- The integrity auditor's card states its measurements as facts rather
  than rates, and drops the threshold magnitudes.

## 0.15.0 — 2026-09-07

- Chain debt: a diff-scoped LGTM certifies a chain rather than a fresh
  whole-document read. Three paths discharge the debt — an integrity
  audit, a full-document round, or the developer's recorded decline —
  and all three write one `debt discharged` annotation.
- Errata wave one sharpens the loop: gate lines get their own shape, a
  `revises` field records what a document supersedes, and the
  terminators state what each one suspends.
- The disposition ledger gains four states and an authorizer clause, a
  clause table, and prose tolerance for the shapes earlier rounds wrote.
  Relitigation branches on the authorizer clause, and the ledger stands
  as context for a diff-scoped round.
- A reviewer's stop signal gets a ledger line, so a later session can
  cite what a round judged its leftovers to be worth.
- Per-round commits on a document branch, offered as the second clause
  of the loop's autonomy question.
- Developer contact is defined, the round cap is stated as best-effort,
  and a plan's confirming round counts against it.

## 0.14.0 — 2026-08-29

- Verdict agents run in the background: `architect` and `plan-adversary`
  return a self-describing report to a subject-keyed output, and the
  dispatcher relays before it stamps.
- Two audit agents join the family. `propagation-auditor` checks a spec
  or plan for mechanical consistency before an expensive dispatch;
  `integrity-auditor` reads a churned spec on a fresh context at the
  consumption gate. Neither grades nor stamps — a passing audit is a
  precondition for the work that follows.
- The autonomous review loop: triage by license rather than by grade, a
  disposition ledger carrying each finding's state, the `integrity:`
  stamp, and the terminators that end an unattended run.
- The new `process-status` skill reports what the process left
  unfinished in a repo, and publishes the unfinished-work list as a
  named section.
- A code review is offered after implementation, before a plan's
  `status` moves to `implemented`.
- The ticket sweep tolerates a relocated field, quotes hash-leading
  values, and bounds itself to one line.

## 0.13.0 — 2026-08-12

- The commit suggestion fires only at the implementation-ready gate.
- A Project-memory review is offered when a document reaches
  `implemented`.
- Prose under `docs/` routes through
  `elements-of-style:writing-clearly-and-concisely` when the skill is
  available.
- Store probes test the Project-memory part directories instead of the
  index filename, and the registry-file list delegates to the
  project-memory conventions rule.

## 0.12.0 — 2026-08-05

- The design personas ship as a pair: `architect-consult` and
  `system-designer-consult` return one contribution from a fresh
  context, and the `system-designer-session` skill runs the live
  counterpart. A shared persona file carries the consultation contract,
  and the workflow rule carries the dispatcher's duties.
- The workflow rule asks once per conversation whether the personas may
  be consulted as a design forms, and re-asks when compaction obscures
  the answer.
- Every persona surface resolves domain artifacts from the repo root.
- The review-reports contract names the finding unit, the citation
  rules, and background dispatch.
- The first-create question reads a declared instruction as the
  decision, and names how each mode is materialized.
- Trigger phrases across all surfaces are English.

## 0.11.0 — 2026-07-22

- The review contract owns its `rule-none` citations, labels findings by
  kind, and offers candidate gaps.

## 0.10.0 — 2026-07-22

- The project-memory rules leave this plugin for the `project-memory`
  plugin.

## 0.9.0 — 2026-07-20

- Line-less review findings sort by a stable key the domain states.

## 0.8.0 — 2026-07-20

- Project memory arrives as two rules: an always-on core rule and a
  `paths:`-scoped conventions rule. Notes are exempt from the ticket
  requirement.

## 0.7.0 — 2026-07-17

- Model selection: the workflow rule carries the tier heuristic and the
  cap protocol, both verdict agents carry the dispatch-tier directive
  and report their own model, and the lifecycle rule gains the
  `fallback` field with its re-review offer.

## 0.6.0 — 2026-07-17

- Report filenames drop the prompt text, and the process-artifacts and
  ticket-frontmatter rules cover review reports.

## 0.5.0 — 2026-07-16

- The review-reports rule.

## 0.4.0 — 2026-07-16

- Reviews record their findings, and a resolved concern carries an
  annotation.

## 0.3.0 — 2026-07-13

- The rules engine: the `sync-rules` skill installs, updates, and
  removes distributed rules, a SessionStart hook reports drift, and a
  single-writer manifest script guards the installed set.
- Four rules ship — workflow, spec-plan-lifecycle, process-artifacts,
  and ticket-frontmatter.
- The persona file becomes `ARCHITECT_PERSONA.md`.

## 0.2.0 — 2026-07-13

- The ruleset hashing script.

## 0.1.1 — 2026-07-13

- The `architect` and `plan-adversary` agents, the `architect-session`
  and `grilling-session` skills, and the plugin README.

## 0.1.0 — 2026-07-13

- The plugin manifest and the architect persona.
