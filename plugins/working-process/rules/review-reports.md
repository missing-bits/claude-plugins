---
paths:
  - "docs/code-review/**"
---

# Review reports

The domain-agnostic contract for code-review reports. It binds any
writer to `docs/code-review/` — the review stacks of standards plugins
are its primary consumers, not its only ones. This rule supersedes any
inline fallback format a domain plugin's review skill carries for
standalone installs.

## Location and directory mode

Review reports live in `<project-root>/docs/code-review/` — a Process
directory; its ignored-vs-tracked mode comes from the first-create
question (process-artifacts rule). Who asks depends on who can:

- An interactive run (`mode: solo`) asks the first-create question as
  normal.
- Dispatching a reviewer agent from an interactive session: the
  dispatcher runs the first-create check BEFORE dispatch and asks then
  — exactly as when the process creates `docs/specs/` or `docs/plans/`
  — so the agent never meets an undecided directory.
- A run with no interactive dispatcher (automation, nested agents)
  defers: it writes the report and leaves the directory undecided.
  This is safe because reports are never staged (see Committing); the
  next interactive touch asks per the process-artifacts rule.

## One run, one report

Each review run writes exactly one report, written by the run's owner
— the solo session or the dispatched reviewer agent.

## Filename

`<YYYY-MM-DD-HHMMSS>-<scope-slug>-<runid>.md`, optionally prefixed
`local-` (see Local pocket). `<scope-slug>` is a short kebab-case slug
of the reviewed scope, matching the frontmatter `scope`. Generate
timestamp and runid with this exact command — quoted verbatim so a
narrow permission allowlist can match it byte-for-byte:

```sh
printf '%s-%s\n' "$(date +%Y-%m-%d-%H%M%S)" "$(head -c 4 /dev/urandom | od -An -tx1 | tr -d ' \n')"
```

The first 17 characters of the output are the timestamp; the final 8
hex characters are the `runid`.

## Frontmatter

```yaml
---
date: 2026-07-16
mode: solo
ticket: none
scope: payments-service
runid: 3f9c21ab
standards: python-standards
rerun-of: 9e4d10fc
findings: { critical: 0, important: 2, minor: 5 }
---
```

- `date`: ISO date of the run.
- `mode`: `solo | agent` — the run-owner kind. The value set extends
  only when a new run-owner kind actually ships.
- `ticket`: derive from context or branch, else `none` — a review run
  never blocks on a question. This is a deliberate exception to the
  ticket-frontmatter rule's ask-once step for new documents.
- `scope`: what was reviewed, matching the filename slug.
- `runid`: this run's id, matching the filename.
- `standards`: what the run reviewed against — a single standards-plugin
  name, an inline YAML list (`[python-standards, other-standards]`)
  when a mixed run loaded several, or `none` for an ad-hoc run. Always
  present; value format mirrors `ticket`.
- `rerun-of` (optional): the `runid` of the prior report this run
  re-reviews. When set, the run's owner reads that report and notes the
  prior findings' disposition in Summary — fixed / remaining / new.
- `findings`: severity counts; they MUST equal the body.

## Run scope

A domain review command reviews only its own domain's files; files
outside the domain are noted in Summary as out of scope. A mixed run —
several standards plugins loaded at once — writes ONE report listing
every standards plugin in `standards:`. Per-finding attribution
(`standard: <skill>, rule: <id>` citations) stays domain-owned.

## Layout

1. **Summary** — outcome, out-of-scope notes, and (for a rerun) the
   prior findings' disposition.
2. **Per-file sections**, each with **Critical → Important → Minor**
   subsections; findings within a subsection in ascending line order.

Files with no findings and empty severity subsections are omitted. A
zero-findings run still writes the document.

## Error fallbacks

No git root, or writing the file is impossible → emit the full report
in the reply and state why no file was written.

## Committing

A review run never stages or commits its report — committing is the
developer's explicit per-report decision, and an uncommitted review
report is NOT process debt. This is a deliberate carve-out from the
process-artifacts ride-along expectation, which is written for living
artifacts; a review report is point-in-time. A report not worth
keeping is simply deleted.

## Local pocket (tracked mode only)

When the first-create question resolves to tracked mode for
`docs/code-review/`, also write `docs/code-review/.gitignore`
containing `local-*` — a registry file that rides with the work's
commit. A review the developer requests as local-only gets a `local-`
filename prefix and never appears in git status. Ignored mode needs no
pocket — everything is local there. The mode signals stay unambiguous:
only a `.gitignore` containing exactly `*` means ignored mode.

## Contract probe

Consumers must not assume this rule is in context: a review session
touches source files, so this rule's `paths:` does not load it. A
domain review skill detects the installed contract by the contract
probe — checking, in order:

1. `<project>/.claude/rules/working-process/review-reports.md`
2. `$HOME/.claude/rules/working-process/review-reports.md`

and reading the first file it finds. The order mirrors the Rules
engine's project-over-user conflict rule; the paths are part of this
contract and may not drift independently of the engine's install
layout. When a session does touch `docs/code-review/**`, the engine
loads this rule as usual.

## Out of this rule's scope (domain-owned)

Project-root detection (each ecosystem's project marker file), finding
citation sources (rule ids from domain skills), team-mode extensions,
and the review procedure itself.
