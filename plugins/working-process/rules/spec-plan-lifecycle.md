---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
---

# Specs and plans — frontmatter and lifecycle

Specs live in `docs/specs/`, plans in `docs/plans/`. Both open with a
YAML frontmatter block:

```yaml
---
ticket: ABC-123     # tracker reference; inline list when several; `none` without one
date: 2026-07-13    # ISO creation date
status: draft       # moves forward only: draft -> approved -> implemented
grilled: grilling   # optional: `grilling` while outcomes are pending; the ISO date once applied
architect: LGTM     # optional: latest architect verdict (LGTM | concerns | blocking)
adversary: LGTM     # optional: latest plan-adversary verdict (LGTM | concerns | blocking)
branch: feature/ABC-123-short-name   # optional: topic branch of the work
base: master        # optional: branch the topic branch was cut from
---
```

- `status` is linear and moves forward only. Review rounds are iterative
  and live in their own fields; `grilled`, `architect`, and `adversary`
  appear only once the corresponding step has run.
- `branch` and `base` appear once the topic branch exists — never guessed
  up front, omitted entirely when there is no topic branch.
- Unfinished process work is greppable:
  `rg -l '^grilled: grilling' docs/` and
  `rg -l '^(architect|adversary): (blocking|concerns)' docs/`.

Lifecycle offers — each an offer the developer may decline, and each made
only when the tool is available: grill a fresh spec (grilling-session);
architect-review a grilled spec (architect agent dispatch);
adversary-review a plan before implementation (plan-adversary agent
dispatch). After any review round, stamp the verdict into the document's
field.

When implementation is about to start, suggest committing the work's
documents under `docs/` — only paths git tracks or would track;
deliberately ignored documents are skipped silently, and committing
itself stays with the developer.

Ticket value format, sourcing order, and backfill live in the
ticket-frontmatter rule.
