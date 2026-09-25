---
paths:
  - "docs/specs/**"
  - "docs/technical-designs/**"
  - "docs/plans/**"
  - "docs/domain/**"
---

# Propagation duties — the author's checklist

Before a document goes to an expensive reader, nine duties fall due,
keyed by the ten edits that trigger them — one duty answers two
different edits. This rule lists them by the edit an author has just
made, so the enumeration can be done at the desk instead of paid
for at the gate. The list below is complete as it stands and needs
nothing else to be usable.

When the `propagation-auditor` agent is available it walks the same
nine as a gate, and its card is their definition and keeps the
measurement behind each; the numbers in the last column are that card's,
so a hit it reports can be read back to the row that would have caught
it. Without the agent the rows still hold — what is lost is the second
pair of eyes, not the duties.

| You have just… | Enumerate | Duty |
|---|---|---|
| changed an interface — a signature, a name, a heading, an anchor, a field | every consumer, by parsing the structure that defines them, never by text match | 1 |
| prescribed a verbatim block | the anchor it targets — the text it replaces must exist in that file byte-exactly, and once | 2 |
| reported a change already made | that block against the shipped file, both ways: one that never landed, and shipped text a block no longer matches | 2 |
| added a field, label or state | both ends of its chain — what writes it, and what reads it | 3 |
| asserted a count | the count itself, re-derived from what the tool prints or what the list holds | 4 |
| used a name your source does not define | the source's own names; an invented name is a gap in the source rather than an error in yours | 5 |
| reported another document's state | that sentence, against that document | 6 |
| written a verification command | the command, run against your own replacement text | 7 |
| copied a citation out of a review report | the file and line it names, read at the source | 8 |
| added or repointed a `spec:` or `technical-design:` pointer | both targets; on a design spec or a technical design, that each pointer names the document that names it; on a plan, that its `technical-design:` entries resolve, from the plan's own directory, to exactly the technical designs its design specs name — none missing, none extra | 9 |

Two of these fire where an author does not expect them. A newly minted
glossary `_Avoid_` ban is a changed interface, so duty 1 reaches every
shipped occurrence of the banned term — which is why this rule loads at
the domain directory as well as at design specs, technical designs and
plans. And a count asserted
about another document is duties 4 and 6 at once: re-derive it, then
read it back at its source.

Self-checking never replaces a gate where one runs. A fresh context
finds what an author's eye has stopped seeing; what this buys is a
shorter list for it to find, which is what makes the round after it
cheaper.
