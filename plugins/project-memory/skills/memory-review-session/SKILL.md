---
name: memory-review-session
description: "Grooming session for a Project-memory store: audits MEMORY/ARCHIVE consistency, then walks entries toward their correct lifecycle state — closing finished notes, promoting or dropping ideas, splitting or merging, sharpening entry descriptions. Use ONLY when the developer explicitly asks to review or tidy Project memory (\"groom the store\", \"memory review\", \"przejrzyjmy memory\"). A routine memory read or write, or a question about an entry's content, is NOT a trigger."
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

From `MEMORY.md`, a directory listing, and each entry's frontmatter and H1,
surface the worklist:

- dangling `MEMORY.md` links (a line pointing at a missing file);
- body files with no `MEMORY.md` line;
- empty or stub body files (a lifecycle violation);
- index lines whose text after the dash differs from the entry's
  `description` — the entry wins, so the fix is to confirm the entry and
  re-project the line, never to edit the line alone;
- index lines whose link text differs from the entry's H1 — same authority,
  same fix;
- frontmatter keys this plugin does not define: report them and move on,
  never remove them;
- `idea-*` files whose `status` is `spec'd` or `dropped` but that still sit as
  live bodies;
- index lines sitting in the wrong section (a section-blind writer —
  Auto-memory in a Hybrid store — appended them): move the line to its
  part's proper section; the entry body is untouched;
- **sweep**: any closed line still in `MEMORY.md` (legacy, or a botched close)
  moves to `ARCHIVE.md`. Under the invariant this should be empty; the sweep
  is the safety net.

Entries written before these fields existed — or written by Auto-memory,
which knows nothing of them — carry **format debt, not defects**: an entry
with no `description`, or with no H1 to project a title from, is
incomplete, not broken. Title drift on such an entry is part of the
same debt — its index line predates the projection, so a link text disagreeing
with the H1 of an entry that has no `description` is re-projected when the
debt is paid, not reported as drift. Count the debt and list it apart from the
defects above — a dangling link is a fault in the store, a missing
`description` is work the store has not had yet — and offer to fill it in
during the walk.

## Entry walk (ordered, existential first)

One entry at a time, a recommendation with each:

1. **Should this entry exist at all?** Untrue → obsolete (delete, no archive
   line). Realized or subsumed by a spec, plan, glossary, or ADR → close with
   a Done line. This is how a released work-state note leaves the store.
2. **Is it in the right part?** team ↔ private rebalance.
3. **Is it the right size and shape?** split an overgrown note, trim it, merge
   duplicates; a note that has grown into a mini-spec is a candidate for a
   real spec, not a longer note.
4. **Is the `description` right?** Recall depends on it. The `MEMORY.md` line
   is only its projection, so judge the `description` itself and let the line
   follow.

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
