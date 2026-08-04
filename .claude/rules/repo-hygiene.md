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
  trigger phrases inside a component's `description:` (skill or agent),
  the README trigger lines that mirror them, and the `query` values of
  trigger-eval files (`evals/trigger-evals.json`), may be non-English —
  all mirror how a developer actually asks, and the evals exercise
  exactly those phrases (precedent: project-memory's "przejrzyjmy
  memory"). The surrounding prose stays English.
