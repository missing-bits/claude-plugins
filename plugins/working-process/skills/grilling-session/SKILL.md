---
name: grilling-session
description: Grilling session that stress-tests a spec (the primary target), plan, or raw idea against the project's domain glossary and recorded decisions, sharpens terminology, and applies glossary/ADR updates inline as decisions land. Use ONLY when the developer explicitly asks to be grilled ("grill me", "grilling session"); plain "build X" requests belong to brainstorming. Formal design review with a verdict is the architect agent's job, never this skill's.
---

## Place in the flow

idea → brainstorming (spec) → **grilling-session on the spec** →
architect review (an `architect` agent dispatch) → writing-plans (plan) →
plan-adversary on the plan → implementation → code review. Offer a
grilling once a spec
exists and before its implementation plan is written. Specs are the
primary target; plans and raw ideas are in scope too.

## Glossary first

FIRST ACTION: read `docs/domain/glossary.md` and `docs/domain/adr/` if
they exist. Canonical terms and `_Avoid_` bans bind your own wording from
the very first question — open the session already speaking the project's
language.

## Artifacts — the domain directory

The session writes to the project's domain directory, `docs/domain/`:

- `docs/domain/glossary.md` — canonical terms
  ([GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md))
- `docs/domain/adr/NNNN-slug.md` — recorded decisions
  ([ADR-FORMAT.md](./ADR-FORMAT.md))

### First-create question

- Creating `docs/domain/` for the first time? ASK the developer whether
  the directory should be git-ignored (write `docs/domain/.gitignore`
  containing exactly `*` — ignored mode) or committed (no `.gitignore` —
  tracked mode). Assume no default.
- The directory already exists? Never ask when a prior decision is
  present — the decided signals (observable marks and the
  declared-instruction signal, with its materialization duty) are
  owned by the working-process process-artifacts rule; consult it. No
  signal present? No decision was ever made — ask, exactly as on
  first creation.

## Frontmatter stamping

Stamp only documents that follow the frontmatter convention: the target
opens with a YAML block containing a `status` field. Otherwise skip
stamping silently — a raw idea has nothing to stamp. When the convention
applies (edit with the Edit tool):

- Session start: set `grilled: grilling`.
- Session end: replace it with the ISO date (e.g. `grilled: 2026-07-13`)
  — but ONLY once every decision, glossary update, and document amendment
  from the session has been applied.
- A session cut short leaves `grilling` in place on purpose: the
  Grilling pending class of the lifecycle rule's Unfinished-work list,
  which publishes the command and which `process-status` runs.

## Grilling mechanics

- Interview toward shared understanding: one question at a time, wait for
  the answer, and recommend an answer with every question.
- Never ask what code or project metadata can answer — read the source,
  grep, use domain CLIs instead.
- Glossary conflict → quote the definition and ask which meaning is
  intended. Fuzzy term → propose a canonical one. Probe edge cases.
  Verify claims against the code.
- Apply glossary updates inline the moment a term settles — no batching.
- ADRs are rare: offer one only when the decision is hard to reverse AND
  surprising without context AND a real trade-off existed.

## Closing the session

1. Apply every remaining outcome, then stamp the `grilled:` date (see
   above).
2. Tracked mode only: list the artifact files the session touched and
   remind the developer they belong in the current work's commit. Never
   commit — committing stays with the developer.
3. Offer the next step: an `architect` agent dispatch on the grilled
   document, with a domain hint gathered during this session.
