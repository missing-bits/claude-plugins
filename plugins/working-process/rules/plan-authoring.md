---
paths:
  - "docs/plans/**"
  - "docs/**/*-plan.md"
---

# Plan authoring — recurring defect classes

A plan's verification steps keep failing in the same few ways. Read
this before the plan's first line is written, and ask each class's
question of every task before handing the plan on. The plan-adversary
agent, when available, reads the same text.

## Seven classes

1. **A check or test that cannot fail.** It passes whether or not the
   step did its work: a test green without the change, a count equal
   before and after, a search over a path that holds nothing. *What
   does this print with the step undone?*
2. **An expected value fitted to the author's view.** The value was
   read off the tree the author had open, while the check runs on the
   tree the previous task leaves. *Did I compute it on that tree?*
3. **An anchor by line number.** A line number goes stale with the
   first edit above it, an earlier task of the same plan included.
   *Does the step find its place by text that will still be there?*
4. **A defect born of a repair.** A fix written between review rounds
   gets less care than the first draft, and most late findings come
   from one. *Have I re-run every check the fix touches?*
5. **A check of an artifact the consumer does not load.** The step
   verifies the source while the consumer reads an installed, built or
   cached copy. *Which file does the consumer open?*
6. **Fixes in one wave that undo each other.** One fix restores the
   phrase another fix's check counts, or two rewrite one sentence.
   *Does any fix in this wave change what another relies on?*
7. **The same discipline one site away.** A finding marks one site,
   and its neighbours usually share the defect: the next task, the
   sibling file, the other side of a pair. *Where else does the rule
   I just applied hold?*

## A failing test is observed, never predicted

A plan never states the message a failing test will print. It
prescribes the observation: run the test with the change absent —
before the change is written, or with it reverted — record what the
run prints in the implementer's report, and restore the change where
it was reverted. The plan stays as approved. A test that passes with
the change absent proves nothing, and the task stops as blocked: an
implementer reports its execution skill's blocked status (`BLOCKED` in
superpowers' subagent-driven-development skill, when available), and a
session executing the plan itself stops and reports to the developer.

## Writing a verification check

When the `wp-phrase-check` command is available — the working-process
plugin puts it on the Bash tool's `PATH` while enabled — every
verification check over text takes its form:

    wp-phrase-check <path>... --phrase "<words>" --before <n> --after <m> --side before|after

It joins lines, collapses whitespace, ignores case and drops a line's leading
list or quote marker, and it prints the expected count, the actual count and
what it read. Without the command, normalise by hand — `tr -s '[:space:]' ' '`,
then count matches, not lines (`grep -oiF -- "<words>" | wc -l`) — and state
both numbers beside the check.

The command cannot enforce the rest:

- Run the check on each side of its step, the two calls identical but
  for `--side`.
- Give a file the step creates or deletes a check of its own, run only
  on the side where the file exists; the absent side's number is `0`.
- State the change the step makes, as the before/after pair, never a
  total fitted to the file as the author found it.
- Write a check that correct text can satisfy. When satisfying a check
  forces an odd edit, the check is the defect.
- Pass `--unchanged` only to state that the step leaves the phrase as
  it is; equal numbers without it fail.

Classes 2 and 3 bind every check as well and are stated once, above.
