---
paths:
  - "**"
---

# Public-repo hygiene

This is a public repository. In every committed file — plugin content,
docs, README — and in commit messages:

- no machine-specific paths (`/home/<user>/…`): use repo-relative paths or
  placeholders;
- no company or client names;
- all committed text is in English. One narrow exception: quoted example
  trigger phrases inside a skill's `description:` may be non-English — they
  mirror how a developer actually asks (precedent: grilling-session's
  "przemagluj"). The surrounding prose stays English.
