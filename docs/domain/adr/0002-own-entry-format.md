---
ticket: none
---

# Project memory defines its own entry format

Auto-memory keeps entries in a shape — `name`, `description`,
`metadata.type` with a four-value taxonomy — that the platform never
documents; the published contract for entry bodies is "any markdown", and the
surrounding surface moved four times inside one minor line. Project memory
therefore converges on that shape without adopting it: the plugin's rules
define every field on the plugin's own terms and adopt only fields that earn
their place there, so a field like `description` is kept because it gives the
index line a source, not because Auto-memory writes one. The asymmetry decides
it — the store holds durable, versioned, team-shared data in git, while the
format is a moving internal detail of a self-updating tool, and binding the
first to the second would pay for interoperability with other people's
repositories.

The consequence is that compatibility is textual rather than contractual: a
tolerance clause keeps unknown frontmatter keys intact so both writers can
share a file, and nothing in the rules calls Auto-memory the source of the
format. Making the store double as the Auto-memory directory would reverse
this decision, so that later choice has to face it deliberately instead of
sliding past it.
