---
ticket: none
date: 2026-07-16
status: draft
architect: LGTM
---

# Working-process 0.5.0 — review-reports convention

## Overview

Working-process takes ownership of code-review reports as a process
artifact: `docs/code-review/` becomes a Process directory, and a shared
review-report format ships as a new rule in the plugin's Rules payload.
Domain plugins (the first consumer is the upcoming `python-standards`)
do not carry their own authoritative report formats — they defer to
this rule when it is installed and keep only a minimal inline fallback
for standalone installs.

## Motivation

- Every domain plugin with a review stack needs a report contract;
  owning it centrally means each new domain plugin ships without its own
  authoritative format, and the contract evolves in one place.
- The Rules engine is the cross-plugin sharing mechanism this
  marketplace already owns — a rule lands at a known path under the
  chosen rules target (`<project>/.claude/rules/working-process/` or
  `$HOME/.claude/rules/working-process/`) and updates through the
  existing drift hook. A plugin-root file would not work:
  `${CLAUDE_PLUGIN_ROOT}` resolves to the referencing plugin, so one
  plugin cannot reliably path into another's install.
- `docs/code-review/` fits the visible-artifact pattern of `docs/specs/`
  and `docs/plans/`, and the process-artifacts rule already names review
  reports among per-work artifacts — this spec completes that claim.

## Changes

### 1. `rules/process-artifacts.md` (edit)

- Add `docs/code-review/` to the Process-directory list.
- Add `"docs/code-review/**"` to the rule's `paths:` frontmatter — today
  the rule does not even load in a session touching that directory.
- The first-create question (ignored mode vs tracked mode) applies to
  `docs/code-review/` exactly as to every other Process directory.

### 2. `rules/ticket-frontmatter.md` (edit)

- The per-work field-set list names review reports explicitly: they live
  in `docs/code-review/` and carry the review-reports rule's frontmatter
  set — not the bare `ticket`-only set of `.superpowers/**` artifacts.

### 3. `rules/review-reports.md` (new)

`paths: ["docs/code-review/**"]`. The domain-agnostic report contract:

- **Location**: `<project-root>/docs/code-review/`; directory mode via
  the process-artifacts first-create question.
- **One run, one report**, written by the run's owner (solo session,
  standalone reviewer agent, or aggregating team thread).
- **Filename**: `<YYYY-MM-DD-HHMMSS>-<scope-slug>-<runid>.md`; the rule
  carries one canonical shell command generating timestamp+runid, quoted
  verbatim so narrow permission allowlists can match it byte-for-byte.
- **Frontmatter**: `date`, `mode: solo | agent` (the value set extends
  only when a new run-owner kind actually ships — no speculative modes),
  `ticket` (derive from context or branch, else `none`; a review run
  never blocks on a question — a deliberate exception to the
  ticket-frontmatter rule's ask-once step for new documents), `scope`,
  `runid`, `findings: { critical: N, important: N, minor: N }`.
- **Layout**: Summary; per-file sections with Critical → Important →
  Minor subsections; line-ascending ordering; no-findings files and
  empty severity sections omitted; a zero-findings run still writes the
  document; frontmatter counts MUST equal the body.
- **Error fallbacks**: no git root, or file write impossible → emit the
  full report in the reply and state why no file was written.
- **Discovery (part of the contract)**: consumers must not assume this
  rule is in context — a review session touches source files, so the
  rule's `paths:` does not load it. A domain review skill detects the
  installed contract by probing, in order,
  `<project>/.claude/rules/working-process/review-reports.md` then
  `$HOME/.claude/rules/working-process/review-reports.md`, and reads the
  file it finds. When a session does touch `docs/code-review/**`, the
  engine loads the rule as usual.
- **Precedence line**: this rule supersedes any inline fallback format a
  domain plugin's review skill carries for standalone installs.

Domain-owned, out of this rule's scope: project-root detection (each
ecosystem's project marker file), finding citation sources (rule ids
from domain skills), team-mode extensions, and the review procedure
itself.

### 4. Version and identity

- Plugin version `0.4.0 → 0.5.0` (minor: new component + backward-
  compatible convention extension).
- README: Process rules section counts five rule files and documents the
  review-reports rule; the process-directories section adds
  `docs/code-review/`.
- `plugin.json` description unchanged (already says "process rules
  distributed as a Rules payload"); catalog and README row therefore
  unchanged except the components table.

## Non-goals

- Any python-standards content — companion spec
  `2026-07-16-python-standards-design.md`.
- Review procedures, severity rubric sources, or reviewer agents —
  domain plugins own those; this rule owns only the report contract.

## Verification

- `claude plugin validate .` and `claude plugin validate
  plugins/working-process` pass; review-reports.md frontmatter reviewed
  by hand (validate skips `rules/`).
- `ruleset-hash.sh` aggregate changes; after `claude plugin update`, the
  drift hook nudges and a sync-rules update classifies
  `review-reports.md` as an install row and `process-artifacts.md` as an
  auto-update row (absent local edits).
- A session touching `docs/code-review/**` loads the extended
  process-artifacts rule and the new review-reports rule; the probe
  paths named in the Discovery bullet resolve in both install scopes.

## Sequencing

Working-process 0.5.0 ships before python-standards 0.1.0, which
declares `working-process ≥ 0.5.0` as its assumed convention range.

## Architect findings — 2026-07-16 round 1

Dual review (context-carrying + fresh reviewer); stricter grade kept.

- **Important (fresh)**: consumer detection unspecified — the rule's
  `paths:` keeps it out of context during review sessions, so the
  precedence mechanism had no handshake. → Fixed: Discovery bullet in
  the contract (probe path pair, project then user).
- **Minor (fresh)**: "never ask" for `ticket` contradicted the
  ticket-frontmatter ask-once step while citing it. → Fixed: named a
  deliberate exception.
- **Minor (fresh)**: `mode: team` was speculative generality. → Fixed:
  `solo | agent` now; values extend when a new run-owner kind ships.
- **Minor (context)**: ticket-frontmatter field-set list would silently
  disagree with review reports' richer set. → Fixed: Changes §2 edits
  that rule too.
- **Minor (context)**: `branch`/`base` absent from this spec's
  frontmatter though authored on `feature/python-standards`. →
  Deliberate: the 0.5.0 implementation gets its own topic branch when it
  starts; the fields appear then.

Round 2 (verification pass): all dispositions confirmed — the Discovery
probe pair verified byte-consistent with the sync-rules engine's install
layout, project-first order matching its conflict rule. Verdict: LGTM.
