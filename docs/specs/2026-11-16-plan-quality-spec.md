---
ticket: none
date: 2026-11-16
status: approved
grilled: 2026-11-16
architect: concerns (resolved 2026-11-16)
integrity: 2026-11-16 (sha: b40d9eb)
decisions: registered
branch: feature/plan-quality
base: develop
---

# Plan quality — checks that cannot be written wrong

Implementation plans keep shipping the same classes of defect in their
verification steps, and every reviewer catches them afresh. This spec
stops them at authoring time with a helper that makes the common check
impossible to write wrong, one rule about test reds, and the defect
classes that keep recurring, written where the author meets them. It
is package 6 of the release queue.

## Problem

Evidence from three projects, gathered 2026-11-16 (records in the
developer's private store, not committed):

- **This repository** — prose plans whose checks are `grep` runs. The
  process-context plan passed five propagation-gate episodes, and
  nearly every gate hit was a defect in a verification check: a phrase
  wrapped across lines, letter case after a wrap, whitespace, a count
  no correct text could reach, a shell variable no step set, a
  verification check that passed with nothing to examine. Seven earlier review loops show the same classes.
- **A web-application project** — 31 findings in 18 of 31
  plan-adversary rounds concerned tests that could not fail, could not
  pass, or failed for the wrong reason; 17 line or path anchors went
  stale.
- **A Salesforce project** — 11 of 30 checked predictions of a failing
  test's message were wrong, and one plan spent five Important findings
  on them before the project switched to observing the failure instead
  of predicting it. That switch at once exposed a test that could never
  fail. Counts drifted in 18 or more places; 12 line citations were off
  by one.

What recurs is the class, not the instance. A rule that asks the author
to judge each site ("use a multiline match where a phrase might wrap")
keeps failing at the rate the judgment fails; what closed a class in
the past was one uniform form applied everywhere.

## Goals, non-goals, anti-goals

Goals:

- A verification check over text is written in one form that already
  handles wrapping, case and whitespace, and that shows its result
  before and after its step.
- A plan states how to observe a failing test, never what message it
  will print.
- The author of a plan reads the defect classes that keep recurring
  while writing it, from one text the plan-adversary also reads.

Non-goals:

- Changes to `superpowers:writing-plans` or any other plugin.
- The other plan-authoring classes recorded in the developer's notes;
  they stay there as background.
- A permission mechanism for the helper. It runs under the user's
  permission mode, as superpowers' own scripts do.
- The propagation gate's script (release-queue package 4). It may later
  reuse the helper's normalisation; nothing here prepares for that.

Anti-goals — the package fails, even if it works, when:

- the same classes still appear in plans written after it;
- the helper brings a defect class of its own;
- a session or an agent has to ask for permission repeatedly to run it.

Accepted risks, by the developer's decision (2026-11-16):

- In the default (manual) permission mode the first run in a
  repository asks once.
- Whether the launcher skips the Windows store placeholder where it
  comes first on `PATH` is not observed.
- A plugin with a top-level `bin/` does not install on claude.ai or in
  Cowork; working-process is used in Claude Code, and the plugin's
  README states the requirement.

A throwaway spike on 2026-11-16 observed the rest: the normalised count
found a wrapped phrase grep missed (1 against 0) and a wrapped,
capitalised one (9 against 2); a plugin's `bin/` reached both a
headless session and its subagent; the default (manual) permission
mode asked, as the first accepted risk says, and auto mode ran it
without asking. On Windows, in the Claude Code CLI, the same `bin/`
reached the session and its subagent through Git Bash, and the
launcher found `python3`.

Size target: the spec under 270 lines, revised from 200 after the
builder check and two review rounds; the helper a few hundred lines
with its tests; the rule under 80 lines. (Author's call.)

## Decisions

- **D1** — The working-process plugin ships `bin/wp-phrase-check`, which Claude
  Code puts on the Bash tool's `PATH` while the plugin is enabled, so a
  plan calls it by name in any project. Argued in *Running everywhere*.
- **D2** — `wp-phrase-check` normalises before it matches: lines joined,
  whitespace collapsed, case ignored, a line's leading list or quote
  marker dropped; a match never spans two files, and matches do not
  overlap. A phrase is found whatever the file's wrapping. Argued in
  *The helper*.
- **D3** — Every `wp-phrase-check` run prints the expected value and the
  actual one and exits non-zero on a mismatch. It also prints how much
  it read, and a named path that is missing or unreadable, or a run
  that read no file, exits non-zero. A count mismatch is reported
  before vacuity. Argued in *The helper*.
- **D4** — `wp-phrase-check` requires the count before its step and after
  it, both as numbers, and fails a check whose two counts are equal
  unless the author declares the step leaves it unchanged. A plan runs
  the check on each side of its step, and each run verifies the actual
  count against that side's number — except where a file does not
  exist on one side: a step that creates a file runs the after side
  only, and one that deletes it the before side only, since an absent
  file counts zero by construction. A file the step creates or deletes
  gets a check of its own, apart from the files present on both
  sides. Argued in *The helper*.
- **D5** — `bin/wp-phrase-check` is a short bash launcher that finds
  Python 3.9 or later (`python3`, then `python`, then `py -3`, each
  confirmed by its version) and runs the implementation, which sits in
  the plugin's `scripts/` and which the launcher finds from its own
  path; with none found it prints which
  commands it tried and exits non-zero. Argued in *Running everywhere*.
- **D6** — A plan never predicts the message a failing test prints. It
  prescribes the observation: run the test with the change absent —
  before it is written, or with it reverted — record what it prints in
  the implementer's report, and restore the change where it was
  reverted. A test
  that does not fail stops the task as blocked. Argued in *Observing a
  failure*.
- **D7** — One new rule, `plan-authoring.md`, path-scoped to plans
  (`docs/plans/**`, `docs/**/*-plan.md`), holds the recurring defect
  classes, the failing-test rule and the check-writing rules the helper
  cannot enforce, and names `wp-phrase-check` as the form for text
  checks, when the plugin is enabled. Argued in *The defect classes*.
- **D8** — The plan-adversary card reads that rule's shipped copy at
  `${CLAUDE_PLUGIN_ROOT}/rules/plan-authoring.md`; the rule, titled
  "Plan authoring — recurring defect classes", is the single text, and
  its title does not call it a checklist, the propagation-duties rule's
  word. Argued in *The defect classes*.
- **D11** — The plugin's README states that working-process needs
  Claude Code, not claude.ai or Cowork, and Python 3.9 or later under
  any of the launcher's three names. Argued in *Goals, non-goals,
  anti-goals*.
- **D10** — Plan-writing, in session or delegated, reads the
  plan-authoring rule before the plan's first line is written:
  `workflow.md` step 4 states that read for both cases, as it already
  does for the technical-design rule, and its sentence naming the
  lifecycle rule for a delegated plan-writer names this rule too. A
  path-scoped rule loads when a matching file is read, and a new plan
  has none to read before its first write, after the plan template has shaped the
  draft. Argued in *The defect classes*.
- **D9** — The rule names seven defect classes: a check or test that
  cannot fail; an expected value fitted to the author's view instead of
  the state the previous task leaves; anchors by line number; defects
  born of a repair; checking the artifact the consumer loads; fixes in
  one wave that undo each other; the same discipline one site away.
  Argued in *The defect classes*.

## The helper

`wp-phrase-check` answers one question about a set of files: how many times
does this phrase occur. The plan's check is a call such as

    wp-phrase-check <path>... --phrase "<words>" --before <n> --after <m> --side before|after

and the helper does what authors kept getting wrong by hand. It joins
each file's lines and collapses every run of whitespace to one space,
and it compares without case, so a phrase split across lines, a
capital after a wrap and a doubled space all count. It prints the
expected value, the actual value and the files it read, and exits
non-zero on a mismatch, so a check never passes in silence. It says how
many files and lines it read, and a missing or unreadable path, or a
run that read nothing, fails, so a mistyped path cannot pass a removal
check. (Developer's ruling, 2026-11-16.)

A check is vacuous when its result is the same before and after the
step it verifies. The plan runs the same check twice, once before its
step and once after, each run naming its side and verifying the actual
count against that side's number, so a before count is observed and
never only declared — but for a file the step creates or deletes, whose
absent side counts zero by construction and is not run (D4). The helper requires both counts, as numbers, and
fails a check whose two counts match unless the author passes a flag
declaring that the step leaves the phrase unchanged — a ruling that
something stays as it is, say. Leaving a count unchanged becomes a
statement the author makes, never an oversight. This catches the
text-check side of the class that recurred in all three projects; for
tests, D6's observation does the same. A git revision as the
before-state is not offered: plans run uncommitted unless the
developer consents to commits. (Developer's ruling, 2026-11-16.)

Author's calls on the details:

- Normalising also drops a line's leading Markdown markers — list
  bullets, numbers, blockquote `>` — so a phrase wrapped inside a list
  item or a quote still matches. A match never spans two files, and
  matches do not overlap.
- Each count is the total over the files named; there is no region
  scoping. The before/after pair is what ties a check to the lines a
  step writes.
- A count mismatch is reported before vacuity, so the author first
  sees the wrong number (the spike reported vacuity on a check whose
  count was also wrong).
- The implementation needs Python 3.9 or later and is tested with
  `unittest`, beside the plugin's existing tests; the launcher's
  fallbacks are tested with stub binaries on a crafted `PATH`.

The exact flag names are the plan's to settle, within D2–D4.

## Running everywhere

Claude Code puts a plugin's `bin/` on the Bash tool's `PATH`, and on
Windows that tool runs in Git Bash, which the plugin's hooks already
need. Python 3 is under different names across systems: `python` is
absent on Debian and Python 2 on old systems, and on Windows `python3`
can be a store placeholder. The launcher therefore tries each name and
confirms the version before running, and fails loudly rather than
running the wrong interpreter. The plugin's one Python script calls
`python3` alone; the helper runs from a plan in any project, in
environments the plugin's maintainers never see, so it carries the
fallbacks. (Developer's ruling, 2026-11-16.) The implementation sits beside the
plugin's other scripts, and the launcher finds it from its own path:
`CLAUDE_PLUGIN_ROOT` is not in the Bash tool's environment.

## Observing a failure

Predicting a test's failure message is the step reviewers spent most
on in one project and that its own implementers abandoned for an
observation. An observation cannot be wrong, and it exposes a test
that never fails, which a prediction hides. A plan therefore prescribes
the observation and records nothing in advance. The implementer
records what it saw in its report — the plan is a reviewed document
and stays as approved — and observes it with the change absent, before
it is written or with it reverted. A test that does not fail then stops
the task as blocked, since it proves nothing. (Developer's ruling, 2026-11-16.)

## The defect classes

The plan's author is the reader who can prevent a defect; the
plan-adversary catches it a round later. The classes live where the
author meets them: a rule that loads when a plan file is read,
beside the propagation-duties rule. The adversary's card points at the
same rule, so there is one text. Because a new plan has no file to read
before its first write, step 4 of `workflow.md` asks the
plan-writer to read it first (D10). (Developer's ruling, 2026-11-16.)

The rule holds three things:

- the seven classes of D9, each in a sentence or two with the question
  an author asks before handing the plan on;
- the failing-test rule of D6;
- the check-writing rules the helper does not enforce — compute an
  expected value against the state the previous task leaves; a check
  correct text can satisfy; the change a step makes, as the
  before/after pair states it, never a total fitted to the file; where a check runs on both
  sides, the two calls are the same but for the side; prefer a text anchor to a
  line number.

The rule names `wp-phrase-check` as the form for text checks, conditionally,
as rule text names a plugin's tools. Its `paths:` are `docs/plans/**`
and `docs/**/*-plan.md`, the latter reaching plans in ticket
directories. The adversary's card reads the shipped copy
at `${CLAUDE_PLUGIN_ROOT}/rules/plan-authoring.md`, so it reaches the
rule whether or not `sync-rules` installed it. (Author's calls.)

## Verification

- `wp-phrase-check` carries its own tests: a phrase wrapped across
  lines, a capital after a wrap, doubled whitespace, a missing or
  unreadable path and a run that reads no file (D3), the files and
  lines a run read printed on success (D3), a count that
  differs from its side's number (D4), an equal before/after pair
  failing and passing once declared unchanged (D4), each launcher
  fallback and the no-Python failure.
- A live session in this repository runs `wp-phrase-check` by name, and a
  subagent does too.
- The new rule installs through `sync-rules`; `claude plugin validate`
  passes.
- The plugin's identity surfaces, changelog and dev version follow, as
  for any component.

## Out of scope

- Rewriting existing plans to use the helper.
- A check over code (an AST or a test runner); the helper reads text.

## Review rounds

Gate lines from the pre-round propagation episode, 2026-11-16 (haiku). The episode held hits, so they stay here, before the first round heading.

- hit fixed 2026-11-16 — bare "check" beside "hit" in *Problem*, banned by the glossary's **Verification check**; now "gate hit" and "verification check"
- hit fixed 2026-11-16 — D1 argued in *The helper*, which does not argue shipping or `PATH`; now *Running everywhere*
- hit fixed 2026-11-16 — the brace pattern `docs/**/*-{spec,technical-design,plan}.md` was called a plan pattern but also matches specs and technical designs; the rule's `paths:` are now `docs/plans/**` and `docs/**/*-plan.md`
- hit fixed 2026-11-16 — the accepted risk said "a manual permission mode" and the spike paragraph "the default permission mode", never stated to be one; both now say "the default (manual) permission mode"
- hit dismissed 2026-11-16 — `docs/**/*-plan.md` also matches a companion document in a ticket directory, which is no plan; counter: a `paths:` glob cannot read frontmatter, `technical-design.md` already scopes the same way, and a short rule loading beside a companion document costs little and decides nothing
- hit dismissed 2026-11-16 — the lifecycle rule still uses the brace glob this spec rejected for a plan pattern; counter: the lifecycle rule governs all three document classes, so the brace glob is right there; it is wrong only as a plans-only scope

### 2026-11-16 — architect, fable 5.2, concerns (round 1, full-document)

Record: `.claude/working-process/2026-11-16-plan-quality-spec/architect-round-1.md`. The gate lines above belong to this round's pre-round episode.

- fixed 2026-11-16 — [Important] a top-level `bin/` makes the whole plugin uninstallable on claude.ai and Cowork; ruling: 2026-11-16; a third accepted risk, and the README states the requirement
- fixed 2026-11-16 — [Important] the before count could be declared rather than observed; ruling: 2026-11-16; D4 and *The helper* now run the check on each side of its step, each run verifying that side's number
- fixed 2026-11-16 — [Important] a check over a mistyped path read nothing and still passed; ruling: 2026-11-16; D3 and *The helper* now fail a missing or unreadable path and a run that read nothing
- fixed 2026-11-16 — [Important] the rule loaded only at the plan's first write, after the template shaped the draft; ruling: 2026-11-16; new D10 — `workflow.md` step 4 asks plan-writing to read the rule first
- fixed 2026-11-16 — [Minor] the three-name interpreter search was not argued against the plugin's `python3` requirement; ruling: 2026-11-16; *Running everywhere* now says why the helper carries the fallbacks
- fixed 2026-11-16 — [Minor] D5 did not say how the launcher finds the implementation without `CLAUDE_PLUGIN_ROOT`; license: the plugins reference, *Where each variable resolves*; *Running everywhere* now says it finds it from its own path
- fixed 2026-11-16 — [Minor] D6 assumed the change exists, while test-first work observes the failure before it is written; license: `workflow.md` step 6, test-driven where the skill is available; D6 now says "with the change absent — before it is written, or with it reverted"
- fixed 2026-11-16 — [Minor] the rule's "property of the lines a step writes" did not match the helper's only form, a total; license: D4's before/after pair; the rule's item now names the change the pair states
- signal 2026-11-16 — one diff-scoped round earns its cost if the helper's contract changes (F2, F3); if all four Important are disposed by rewording or accepted, a further round is unlikely to repay itself

Gate lines from the episode before round 2, 2026-11-16 (haiku):

- hit fixed 2026-11-16 — *Verification*'s test list missed D3's missing-path and no-file cases and D4's side-number and declared-unchanged cases; added
- hit fixed 2026-11-16 — the call form in *The helper* still showed `--expect`; it now carries `--before`, `--after` and a side
- hit fixed 2026-11-16 — D6 said a never-failing test "stops the task as blocked" and *Observing a failure* "is reported as blocked"; both now say it stops the task as blocked
- hit fixed 2026-11-16 — the size target said under 200 lines while the body is about 255; restated as under 260
- hit fixed 2026-11-16 — "a zero-hit check" beside the glossary's Hit; the test list no longer uses the phrase
- hit fixed 2026-11-16 — "machine" where the `PATH` is what matters, banned by the glossary's **Environment**; reworded twice
- hit dismissed 2026-11-16 — round 1 has eight `fixed` lines for seven findings; counter: F5 carried two suggestions, disposed separately, one by ruling and one by license
- hit fixed 2026-11-16 — an author's-call bullet still named `--expect`, which the call form dropped; it now speaks of each count
- hit fixed 2026-11-16 — *Verification* had no test for D3's printing of what a run read; added
- hit dismissed 2026-11-16 — no test for a missing or non-numeric `--before`/`--after`; counter: required integer arguments are rejected by the standard argument parser before the helper runs, so a test would test the library

### 2026-11-16 — architect, fable 5.2, concerns (round 2, diff-scoped)

Record: `.claude/working-process/2026-11-16-plan-quality-spec/architect-round-2.md`.

- fixed 2026-11-16 — [Important] D3's missing-path failure and D4's two runs collided on a step that creates or deletes a file; ruling: 2026-11-16; D4 now runs only the side on which the file exists, the helper unchanged
- fixed 2026-11-16 — [Minor] the two runs of one check are two copies nothing ties together; license: the anti-goal that the helper bring no defect class of its own; the rule's check-writing items now say the two calls are identical but for the side
- fixed 2026-11-16 — [Minor] D10's edit clause bound only the delegated case while its scope named both; license: D10's own scope clause and `workflow.md` step 4's precedent for the technical-design rule; D10 now has step 4 state the read for both cases
- signal 2026-11-16 — another round earns its cost only if F1 changes the helper (option b); settled by rule text or accepted, a third round is unlikely to repay itself, and the integrity audit reads the whole document

Round 2's `concerns` is resolved without a further round: the developer settled its one Important finding on 2026-11-16 by rule text, and the reviewer's stop signal judged a third round unlikely to repay itself; the integrity audit at the consumption gate reads the whole document.

Gate lines from the episode before the integrity audit, 2026-11-16 (haiku):

- hit fixed 2026-11-16 — the size target said under 260 while the body is 265; restated as under 270
- hit fixed 2026-11-16 — *The helper* and the rule's item still stated two runs unconditionally after D4 gained its create/delete exception; both now carry it
- hit fixed 2026-11-16 — D4's exception was keyed to "a file" while a call names several; a created or deleted file now gets a check of its own
- hit fixed 2026-11-16 — the pre-round gate lines' note said they move under the first heading, while the lifecycle rule keeps a held-hit episode's lines before it; the note now says they stay
- hit fixed 2026-11-16 — the round 2 close said "one held finding" where the line is `fixed … ruling:`; now "one Important finding"
- hit fixed 2026-11-16 — a gate line's "what changed" misquoted the text it changed; corrected to "stops the task as blocked"
- hit fixed 2026-11-16 — "the plugin's other scripts call `python3`" while one Python script exists; now "the plugin's one Python script"
- hit dismissed 2026-11-16 — the round 2 record cites `workflow.md:98` where the sentence is on 97; counter: the error sits in the dispatch record, which no gate edits, and the spec carries no line number
- hit dismissed 2026-11-16 — "defect class" and "text anchor" have no glossary entry; counter: plain words in their ordinary sense; the grilling minted only the two check terms
