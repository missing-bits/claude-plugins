---
name: migrate-memory
description: "Move project-scoped facts about the current repo out of Claude Code's home-dir memory and into this project's Project-memory store (one direction, home-dir → project), routing each to Team or Private memory. Use ONLY when the developer explicitly asks to migrate or move their notes into the project (\"migrate memory\", \"move my notes to the project\", \"przenieś notatki do projektu\"). Not for team↔private rebalancing (that is memory-review-session) and not a routine memory write."
---

# migrate-memory

An operational skill that repairs routing: home-dir memory is where
project-scoped facts land on a miss, and this is the "moved later" the
core rule promises. One direction only — home-dir → project. Never commits.

## When it runs

Only on a direct request to migrate notes into the project. team ↔ private
rebalancing belongs to memory-review-session; a routine memory write is not a
trigger.

## Scan

Read home-dir memory (`MEMORY.md` plus its entry files). Candidates are facts
**project-scoped to the current repo**, judged by content. Cross-project and
personal facts stay in home-dir memory — do not propose them. When a fact's
scope is unclear, ask; never guess.

## No store yet → offer adoption

If the project has no store, running this skill IS the signal of intent the
core rule requires: offer to create a part. Carry the tracked/ignored
first-create question for Team memory (Private is never asked — always
ignored). Declining adoption ends the skill with no writes.

## Per fact

Recommend move or leave. For a move, route per the core rule: team-relevant →
Team memory, per-user → Private memory. The developer decides each.

## Move mechanics

- Translate shape: a home-dir entry (`name`/`description`/`metadata`
  frontmatter) becomes a **note** or an `idea-<slug>.md` per the conventions
  rule — shape is the criterion, the `idea-` prefix authoritative.
- Add the entry's line to the target part's `INDEX.md`.
- Delete the home-dir body file and its `MEMORY.md` line.
- `ticket` frontmatter on a migrated idea only when the project keeps that
  convention (e.g. via working-process).

## Collision

If a fact already has a counterpart in the project store, the project store
wins: offer to merge into the project entry and remove the home-dir copy.

## Migration trace

After moving one or more facts, leave a single roll-up line in home-dir
`MEMORY.md` — "project-scoped notes for <repo> migrated to its Project
memory, <date>" — not a per-entry pointer.

## Boundaries

One direction only. Never commits. Works without working-process — the
`ticket` convention applies only when the project keeps it.
