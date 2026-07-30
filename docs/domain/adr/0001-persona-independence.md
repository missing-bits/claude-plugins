---
ticket: none
---

# Personas never consult each other

The working process fields two design personas — architect and system
designer, split by dimension rather than by stance — and a developer
dispatches them to get two independent readings of one subject. Both
consult agents therefore ship with `SendMessage` removed via
`disallowedTools`, plus a standing instruction never to spawn another
persona: two personas that reconcile before answering hand back one
opinion where the developer asked for two, and the reconciling happens
where nobody can inspect it. The main thread is left as the only place
the two readings meet, which is also the only place the developer can
weigh them against each other.
