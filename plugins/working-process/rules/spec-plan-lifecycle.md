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
architect-fallback: <model> (degraded <date>)   # optional: verdict above produced below the prescribed tier (adversary-fallback: for plans)
branch: feature/ABC-123-short-name   # optional: topic branch of the work
base: master        # optional: branch the topic branch was cut from
---
```

- `status` is linear and moves forward only. Review rounds are iterative
  and live in their own fields; `grilled`, `architect`, and `adversary`
  appear only once the corresponding step has run.
- A round that ends in `concerns` or `blocking` records its findings (or
  their disposition) in the document body — a verdict whose findings were
  never written down cannot be honestly resolved later.
- Concerns resolved without a fresh review round keep the verdict and
  gain a resolution date — `adversary: concerns (resolved 2026-07-16)` —
  plus a body note saying what resolved them. A fresh round replaces the
  whole value as usual.
- A verdict produced below the prescribed tier (the model-selection
  heuristic in the workflow rule) gains a companion `architect-fallback:`
  / `adversary-fallback:` field: the family alias of the model that
  produced it, then `(degraded <ISO date>)` for anything other than the
  developer's deliberate choice (a cap refusal — including a consented
  one-tier drop — a silent platform substitution, or an under-dispatch
  the dispatcher did not knowingly decide) or `(chosen <ISO date>)`
  when the developer deliberately dispatched below the prescribed tier
  before any refusal. A dispatch at the prescribed tier gets no field.
- Both tokens carry a re-review offer at the document's next consumption
  gate — before plan-writing for a spec, before implementation for a
  plan. Accepted: a fresh round at the prescribed tier replaces the
  verdict and removes the field (a fresh round that is itself below the
  prescribed tier refreshes the field's date instead, and the offer
  re-arms at the same gate). Declined: the field gains `, waived <date>`.
  Moving `status` to `implemented` with a bare fallback field stamps the
  waiver as part of the move.
- Review agents self-report the model they ran on (family plus version);
  the dispatcher compares it against the dispatched and prescribed
  tiers before stamping, and each round's verdict, model, and date are
  recorded in the document body. Committed examples of the bare fallback form use
  placeholders (as above) so they never match the grep below.
- `branch` and `base` appear once the topic branch exists — never guessed
  up front, omitted entirely when there is no topic branch.
- Unfinished process work is greppable:
  `rg -l '^grilled: grilling' docs/` and
  `rg -l '^(architect|adversary): (blocking|concerns)$' docs/` — the
  anchored match deliberately skips resolved-concern annotations.
  `rg -l '^(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/`
  — pending re-reviews; the waived annotation deliberately defeats the
  anchor.

Lifecycle offers — each an offer the developer may decline, and each made
only when the tool is available: grill a fresh spec (grilling-session);
architect-review a grilled spec (architect agent dispatch);
adversary-review a plan before implementation (plan-adversary agent
dispatch); offer the pending re-review of a fallback-recorded verdict at
its consumption gate (fresh round at the prescribed tier); and when a
spec or plan moves to `implemented` and the memory-review-session skill
is available, offer a Project memory review — released work-state notes
close, resolved entries sweep to the archive. After any
review round, stamp the verdict into the document's field.

The process suggests committing the work's documents under `docs/` at
exactly one point — the implementation-ready gate: the developer has
approved the plan (the `status` flip to `approved`) and implementation
is about to start. During authoring — spec drafting, grilling, review
rounds, plan writing — it never makes that suggestion; the documents'
uncommitted state is deliberate, not dirt in the process-artifacts
sense, and the developer may commit sooner on their own call. The
suggestion covers only paths git tracks or would track; deliberately
ignored documents are skipped silently, and committing itself stays
with the developer.

Ticket value format, sourcing order, and backfill live in the
ticket-frontmatter rule.
