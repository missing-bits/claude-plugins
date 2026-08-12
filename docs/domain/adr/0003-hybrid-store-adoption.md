---
ticket: none
---

# Private memory may double as the Auto-memory directory, opt-in

ADR 0002 closed with: "Making the store double as the Auto-memory
directory would reverse this decision, so that later choice has to face
it deliberately instead of sliding past it." This record is that choice,
faced. The hybrid adopts exactly two platform-owned identities — the
directory (`autoMemoryDirectory` may point at `.claude/memory/`) and the
index filename (`MEMORY.md`, the only name Auto-memory loads, adopted
globally so the format has no mode variants) — because in a Hybrid store
both pass ADR 0002's own test: they earn their place as the only way the
harness reads the store at all.

Everything else stands. The plugin defines its own entry format,
converges on Auto-memory's without adopting it, and keeps the tolerance
clause for keys the harness writes; an entry Auto-memory writes into a
Hybrid store is an ordinary note whose missing H1 is format debt. The
adoption is opt-in per developer and per Environment, carried by one key
in `.claude/settings.local.json` written and removed by the
redirect-memory skill; declining it leaves the store purely rule-driven.
ADR 0002 remains in force for the format — this record narrows it only
at the directory-and-name boundary.
