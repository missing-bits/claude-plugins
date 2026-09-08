---
ticket: none
date: 2026-07-28
status: draft
---

# Multi-domain code review — design

## Overview

Two components that turn the branch-closeout code-review offer from a
list of commands the developer runs by hand into one resolved, offered
and dispatched review:

1. the **`code-review-dispatch`** skill — resolve which domains the
   changed files touch, offer the resolved targets, run one shared
   first-create check, fan out the domain reviewers in the background,
   relay their replies;
2. the **`code-reviewer`** agent — a generic review for changed files no
   installed standards plugin claims.

Split out of `docs/specs/2026-07-27-working-process-discipline-design.md`
on the architect session's recommendation (2026-07-28): that spec's five
changes are text edits to existing surfaces, while these two add plugin
components, report-contract semantics and canonical-term changes. Its
step 7 needs no edit when this lands — only what its offer dispatches
changes.

**This spec is not ready for an architect round.** Six open design
questions are recorded below; three of them (the two term changes and the
dispatch-discipline owner) came from the architect session that split the
work and must be answered before the design is coherent.

## Motivation

A repository holding two domains — Python services next to Salesforce
metadata is the live case — has two review commands, each reviewing its
own files and declaring the rest out of scope. The closeout offer that
names them one by one leaves the developer to work out which domains the
changed files touch, run each command, and reconcile the replies.

The knowledge needed to do that automatically is already published: each
`*-code-review` skill declares its domain's file set in a `## Run scope`
section (`python-code-review/SKILL.md:13` names `*.py` and
`pyproject.toml`; `salesforce-code-review/SKILL.md:15-27` names the Apex,
Visualforce, Flow and declarative-metadata sets), and the plan-adversary
already demonstrates the pattern of reading sibling plugins' skills to
resolve domains.

And whatever no domain claims is reviewed by nobody: in a mixed
repository that is most of the shell scripts, infrastructure definitions
and glue.

## Decisions

### 1. Multi-domain dispatch — the `code-review-dispatch` skill

A `working-process` skill. Deliberately neither of the other two shapes:

- **not an agent** — the contract requires the *dispatcher* to run the
  first-create check before dispatch ("so the agent never meets an
  undecided directory"), and a nested agent has nobody to ask; the
  contract classifies such a run as one that defers the decision;
- **not a command** — `/code-review` already carries a meaning in the
  harness, and `working-process` ships no commands today.

What it does, in order:

1. Resolve the scope: named files when given, otherwise the current diff
   — staged plus unstaged, or the branch against its base on a clean
   tree.
2. Resolve the targets: for every available `*-code-review` skill —
   plugin-provided or project-level — read its `## Run scope` section and
   match the scope's files against the file set it declares. A domain
   with no matching file is not a target. Files no domain claims become
   one further target, the generic review of decision 2.
3. **Offer the resolved targets; never impose them.** List each target
   with its file count and the paths it claims, and let the developer
   choose: all of them, a subset, or **none** — declining the whole
   review is a listed choice, not an inference from silence. A review the
   developer did not choose is not dispatched. Invoked from the closeout
   step, this single offer serves as both the consent to review and the
   selection of targets; invoked directly, it is the skill's first
   interaction. A declined offer is not repeated: the developer invokes
   the skill whenever they want it, and an offer that returns uninvited
   is nagging, which no step of this flow does.
4. Run the `docs/code-review/` first-create check ONCE — gated on the
   contract probe, exactly as the review commands gate it, so a
   Standalone install skips the question entirely — after the selection
   and before any dispatch, and pass the resulting decision to every
   dispatched run. Declining every target ends the run without asking it:
   a directory nothing will write to stays undecided. In tracked mode the
   local pocket (`docs/code-review/.gitignore` containing `local-*`) is
   written here, once, by the dispatcher — never by the fanned-out runs,
   which would race on one registry file.
5. Dispatch each selected domain's reviewer in the background with the
   scope narrowed to that domain. This skill adds target resolution, the
   offer, the one shared first-create check, the fan-out and the relay —
   nothing else. It never restates a domain's dispatch discipline and
   never adds a report-shaping instruction of its own; aggregation and
   counting policy, layout and severity policy stay where they are
   defined. **Where that discipline lives is open question 3.**
6. Relay each run's reply as its notification arrives — report path,
   findings by severity, candidate-gap offers verbatim — and close with a
   rollup: one line per dispatched target, plus anything left unreviewed
   (a dropped target, or a file no target could take).

The offer's shape, illustrated on a mixed repository — the exact wording
belongs to the skill, and this block is here for shape only, never to be
matched against or copied by a verification step:

```
Code review — 61 changed files on feature/1234-payment-retries (vs develop).

  1. python-standards       23 files   src/payments/**, tests/**
  2. salesforce-standards   29 files   force-app/main/default/{classes,objects}/**
  3. generic (no plugin)     7 files   infra/main.tf, scripts/deploy.sh,
                                       .github/workflows/release.yml, +4 more
     skipped                 2 files   uv.lock, docs/architecture.png

Each target runs as its own background review and writes its own report
under docs/code-review/.

Which targets — all three, a subset, or none? Nothing runs unless you pick it.
```

Paths accompany the counts because a mis-resolved domain is visible there
and nowhere else before dispatch; the generic target names its files
individually (up to a few, then a count) because it is the one target
whose composition nobody knows in advance. `skipped` is a line, not a
target: non-text and generated files cannot be chosen, but hiding them
would read as an oversight. Declining every target reports one line — no
review dispatched, `docs/code-review/` untouched.

**Report shape: N runs, N reports**, one per target. Each report's
`standards:` names that single plugin; the inline-list form stays
reserved for one run that loaded several standards plugins, which this is
not. `rerun-of` resolves per target, among reports of the same scope,
because a runid is unique only within that pairing — which makes the
scope slug's derivation load-bearing (open question 4).

This is not the shape the backlog entry assumed (one mixed report).
Independent runs are what makes the fan-out parallel and keeps each
reviewer's context to its own domain, and the contract already grants
each run exactly one report. Aggregation belongs in the reply, where the
candidate-gap offers already live — the same division the contract draws
for those offers.

The `## Run scope` section becomes load-bearing, so the contract names
it: one sentence in `review-reports` stating that a `*-code-review` skill
declares its domain's file set in a `## Run scope` section, which a
dispatcher reads to resolve targets. Both shipped skills already comply,
so the sentence records an existing convention rather than requesting a
change to either plugin.

### 2. Generic review for files no domain claims — the `code-reviewer` agent

**A `working-process` agent, and deliberately no skill.** The domain
plugins split procedure (a `*-code-review` skill) from run-owner (a
`*-code-reviewer` agent) because the procedure is where their standards
live. This reviewer has no standards plugin to load, so its procedure
sits inline in the agent file. A WP skill named `*-code-review` would be
worse than redundant: decision 1's resolution would match it, and its
`## Run scope` — everything — would swallow every domain's files.

What it reviews: language-agnostic defects — broken correctness, data
loss, security and secret handling, unhandled errors, dead or duplicated
logic, absent tests for new behavior. Non-text and generated files are
skipped and named as skipped rather than guessed at.

What it grades by: the authoring rubric, which the contract already
carries verbatim — **plus the reviewed project's own instructions**
(`CLAUDE.md`, project-level rules), read before grading. That addition
comes from the architect session: in a repository whose conventions are
written down but carried by no standards plugin — this marketplace being
the example, where a review would otherwise ignore `plugin-authoring`,
`plugin-versioning`, `standards-rule-tags` and `repo-hygiene` — a
reviewer that knows only the rubric produces findings that compete with
the project's rules instead of applying them. How such a finding cites
its source is part of open question 1.

Everything else is unchanged: `mode: agent`, one run one report, the same
layout, the same severity subsections.

**Recorded tension.** This is the first `working-process` component that
judges code rather than process. The boundary claim is that WP owns the
domain-agnostic fallback — the same role its report contract already
plays for a Standalone install — and that the rubric it grades by is
contract-owned, not invented by the agent. The counter-claim worth
hearing is that a review citing no standard has no authority to grade at
all. Decision 1 does not depend on decision 2: if the counter-claim
wins, unclaimed files are reported as unreviewed and nothing else
changes.

## Open questions

Nothing below is decided. The first three are the architect session's;
they are prerequisites, not polish.

1. **The `Candidate gap` term must change, or the citation must.** The
   glossary (`docs/domain/glossary.md:149-160`) defines a Candidate gap
   as a finding cited `rule: none`, and makes "surfaced in the run's
   reply as a candidate for a new rule, with offers to park it in Project
   memory or report it upstream" part of the definition. It also
   enumerates exactly two citation forms — against the loaded domain
   skill, or against the standards plugin. A generic run's
   `(standard: none, rule: none)` is a third form, and suppressing its
   offers contradicts the term. Note that only the **upstream** offer
   loses its addressee: the Project-memory park offer does not, and a
   missing standard for a whole technology is exactly what a store entry
   is for. Route through a grilling-session, which records glossary
   updates as they land.
2. **The `Contract probe` term gains a third runner.** The term names "a
   domain review skill — or a dispatching review command, pre-dispatch";
   `code-review-dispatch` is neither. #10 already had to extend this
   term once for the same reason. Same grilling-session.
3. **Who owns the dispatch discipline?** Decision 1 step 5 currently
   defers to each domain's review *command* — a user-facing surface, not
   an interface, and the surface #10 rewrote from scratch. The
   alternative is to move the discipline (contract probe, pre-dispatch
   first-create check, the ban on report-shaping instructions,
   background dispatch) into the report contract, which already owns
   neighbouring sentences, and have both the commands and this skill
   reference it. That is more churn now and one less cross-plugin
   dependency on an unversioned surface forever.
4. **Scope slug derivation for fan-out targets.** `rerun-of` resolves
   among reports of the same scope; the dispatcher narrows scope per
   target, so each target's slug must be stable across runs and distinct
   between targets, or rerun disposition silently degrades and same-day
   filenames collide more often.
5. **Two entry points to one review.** `/python-review` and this skill
   both start a Python review. State the division (commands as the
   single-domain, explicitly-scoped entry; the skill as resolve-and-fan-
   out) or make the commands delegate.
6. **Project-level `*-code-review` skills as first-class targets.** The
   companion spec already establishes the project-level path for
   `*-plan-review`. The symmetric move is free here, and it shrinks
   decision 2's target to genuinely unclaimed files. Worth stating
   explicitly rather than leaving to the reader of "every available
   skill".

## Surfaces and changes

| Surface | Change |
| --- | --- |
| `skills/code-review-dispatch/SKILL.md` | new file — target resolution, the offer, one shared first-create check, background fan-out, relay |
| `agents/code-reviewer.md` | new file — generic review, procedure inline |
| `rules/review-reports.md` | the `## Run scope` declaration a dispatcher reads; citation form and offer stance for a run with no standards plugin (pending question 1); possibly the dispatch discipline (question 3) |
| `rules/workflow.md` | step 7's code-review offer dispatches this skill when available |
| `plugins/working-process/.claude-plugin/plugin.json` | `description` enumerates components — add both |
| `.claude-plugin/marketplace.json` | catalog entry description — same enumeration |
| `README.md` | root table row — same enumeration |
| `plugins/working-process/README.md` | bullets for the new skill and agent |
| `docs/domain/glossary.md` | `Candidate gap` and `Contract probe` (via grilling-session) |

The three component enumerations are listed because the marketplace-sync
rule requires them to agree, with the manifest canonical — and because
the companion spec's own author missed exactly this consumer list until
an `rg` sweep surfaced it.

## Invariants

- Nothing is dispatched that the developer did not choose; declining
  everything is a listed choice; a declined offer is never repeated
  uninvited; a dropped target is reported as unreviewed rather than
  silently omitted.
- A dispatcher never shapes a report: it passes scope, the directory-mode
  decision and a prior runid, and no instruction about counting, layout
  or severity.
- No run cites a standard it did not read, and no run invents a rule id.
- One run, one report, written by the run's owner — the contract's
  existing rule, unmodified.

## Out of scope

- The **finding router** (review → local fix / plan / spec seed).
- Aggregating several targets into one report: a mixed single-run report
  stays contract-legal for a run that genuinely loads several standards
  plugins, and nothing here forecloses it.
- Standards content for the technologies the generic review covers.
  Promoting a recurring generic finding into a rule means a standards
  plugin for that technology — its own work, its own ticket.

## Versioning and validation

No version bump on the topic branch. Both components are new, so the
accumulated change is **minor** for `working-process`, sized in the
release PR.

This spec is the part of the original design that behavior can falsify,
so it carries the dogfooding gate, designed against the vacuity failure
of #10: a real mixed scope — Python files, Salesforce metadata and at
least one file no plugin claims, changed in one diff — dispatched through
the skill itself, not a hand-rolled dispatch. Pass criteria: the offer
lists three targets with their counts; a run where one target is dropped
dispatches only the rest and names the dropped one as unreviewed; the
accepted run writes three reports whose `standards:` name one plugin, the
other plugin, and `none`; each scope is narrowed to its target; the
first-create question is asked at most once; the local pocket is written
once; the generic report's citations match whatever question 1 settles. A
single-domain scope does not satisfy this gate.

The round runs against the *installed* payload, which the plugin cache
keys by version, so it needs a `-dev.<issue>` string.
