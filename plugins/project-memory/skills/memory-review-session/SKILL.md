---
name: memory-review-session
description: "Grooming session for a Project-memory store: audits INDEX/ARCHIVE consistency, then walks entries toward their correct lifecycle state — closing finished notes, promoting or dropping ideas, splitting or merging, sharpening index lines. Use ONLY when the developer explicitly asks to review or tidy Project memory (\"groom the store\", \"memory review\", \"przejrzyjmy memory\"). A routine memory read or write, or a question about an entry's content, is NOT a trigger."
---

# memory-review-session

An explicit-ask grooming conversation over a Project-memory part
(`docs/memory/` or `.claude/memory/`). The store's analogue of a
grilling-session: it applies the conventions rule's lifecycle, defining
nothing new, and recommends — it never bulk-cleans. Every deletion or closure
is per-entry consent; edits land inline as decisions are made. Never commits.

## When it runs

Only on a direct request to review or tidy the store. Routine memory
reads/writes and questions about an entry's content do NOT start a session —
mirroring the core rule's "never scans, creates, or nags" stance.

## Opening audit (mechanical)

From `INDEX.md` plus a directory listing, surface the worklist:

- dangling `INDEX.md` links (a line pointing at a missing file);
- body files with no `INDEX.md` line;
- empty or stub body files (a lifecycle violation);
- `idea-*` files whose `status` is `spec'd` or `dropped` but that still sit as
  live bodies;
- **sweep**: any closed line still in `INDEX.md` (legacy, or a botched close)
  moves to `ARCHIVE.md`. Under the invariant this should be empty; the sweep
  is the safety net.

## Entry walk (ordered, existential first)

One entry at a time, a recommendation with each:

1. **Should this entry exist at all?** Untrue → obsolete (delete, no archive
   line). Realized or subsumed by a spec, plan, glossary, or ADR → close with
   a Done line. This is how a released work-state note leaves the store.
2. **Is it in the right part?** team ↔ private rebalance.
3. **Is it the right size and shape?** split an overgrown note, trim it, merge
   duplicates; a note that has grown into a mini-spec is a candidate for a
   real spec, not a longer note.
4. **Does the `INDEX.md` line summarize it well?** Recall depends on the
   one-liner — the cheapest tidiness there is.

## adr-candidate flags

Review notes carrying `adr-candidate: yes`. When a grilling-session is
available, offer a handoff to it for the promotion (it writes the ADR, not
this session). Without it, the flag simply stays and the session notes it and
moves on.

## Ideas section

Long-parked ideas → confirm still worth keeping, or drop (a Dropped line with
the reason). `spec'd` ideas → close the redirect to their spec.

## Boundaries

Applies the project-memory-conventions lifecycle; defines nothing new. Never
commits (committing stays with the developer). Recommends per entry — no bulk
deletion. Grilling-session, ADR, and glossary mentions above are conditional:
act on them only when those tools/artifacts are present.
