---
ticket: none
date: 2026-07-16
status: implemented
grilled: 2026-07-16
architect: LGTM
branch: feature/review-reports
base: feature/python-standards
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
- Tighten the mode-signal wording: ignored mode is signaled by a
  `.gitignore` containing **exactly** `*` — not by the mere presence of
  a `.gitignore`, since a tracked-mode `docs/code-review/` legitimately
  carries the local pocket's `.gitignore` with `local-*`. The rule that
  reads the signals owns this disambiguation.

### 2. `rules/ticket-frontmatter.md` (edit)

- The per-work field-set list names review reports explicitly: they live
  in `docs/code-review/` and carry the review-reports rule's frontmatter
  set — not the bare `ticket`-only set of `.superpowers/**` artifacts.

### 3. `rules/review-reports.md` (new)

`paths: ["docs/code-review/**"]`. The domain-agnostic report contract:

- **Location**: `<project-root>/docs/code-review/`; directory mode via
  the process-artifacts first-create question. An interactive run
  (`mode: solo`) asks it as normal. Dispatching an agent run from an
  interactive session: the dispatcher runs the first-create check BEFORE
  dispatch and asks then — exactly as when the process creates
  `docs/specs/` or `docs/plans/` — so the agent never meets an undecided
  directory. Only a run with no interactive dispatcher (automation,
  nested agents) defers: it writes the report and leaves the directory
  undecided, which is safe because reports are never staged (see
  Committing), and the next interactive touch asks per
  process-artifacts.
- **One run, one report**, written by the run's owner (solo session or
  dispatched reviewer agent).
- **Filename** (amended 2026-07-17, see the amendment record below):
  `<YYYY-MM-DD>-<scope-slug>-<runid>.md`, optionally `local-`-prefixed
  (see Local pocket). The date is the session's known today; `runid` is
  8 lowercase hex characters the run's owner generates itself.
  Generating a filename runs no shell command and prompts for nothing;
  never overwrite — on a collision, a new runid and retry.
- **Binding**: the contract binds any writer to `docs/code-review/` —
  domain review stacks are its primary consumers, not its only ones.
- **Frontmatter**: `date`, `mode: solo | agent` (the value set extends
  only when a new run-owner kind actually ships — no speculative modes),
  `ticket` (derive from context or branch, else `none`; a review run
  never blocks on a question — a deliberate exception to the
  ticket-frontmatter rule's ask-once step for new documents), `scope`,
  `runid`, `standards` (what the run reviewed against: a single
  standards-plugin name, an inline YAML list when a mixed run loaded
  several, or `none` for an ad-hoc run — always present, value format
  mirroring `ticket`), optional `rerun-of` (the `runid` of the prior
  report this run re-reviews; when set, the run owner reads that report
  and notes the prior findings' disposition in Summary — fixed /
  remaining / new), `findings: { critical: N, important: N, minor: N }`.
- **Run scope**: a domain review command reviews only its own domain's
  files and notes out-of-domain files in Summary as out of scope; a
  mixed run (several standards plugins loaded at once) writes ONE report
  listing every standards plugin in `standards:`. Per-finding attribution
  (`standard: <skill>, rule: <id>` citations) stays domain-owned.
- **Layout**: Summary; per-file sections with Critical → Important →
  Minor subsections; line-ascending ordering; no-findings files and
  empty severity sections omitted; a zero-findings run still writes the
  document; frontmatter counts MUST equal the body.
- **Error fallbacks**: no git root, or file write impossible → emit the
  full report in the reply and state why no file was written.
- **Committing**: a review run never stages or commits its report —
  committing is the developer's explicit per-report decision, and an
  uncommitted review report is NOT process debt (a deliberate carve-out
  from the process-artifacts ride-along expectation, which is written
  for living artifacts; a review report is point-in-time). A report not
  worth keeping is simply deleted.
- **Local pocket (tracked mode only)**: when the first-create question
  resolves to tracked mode for `docs/code-review/`, also write
  `docs/code-review/.gitignore` containing `local-*` (a registry file —
  it rides with the work's commit). A review the developer requests as
  local-only gets a `local-` filename prefix and never appears in git
  status. Ignored mode needs no pocket — everything is local there. The
  mode signals stay unambiguous: only a `.gitignore` containing exactly
  `*` means ignored mode.
- **Contract probe (part of the contract)**: consumers must not assume
  this rule is in context — a review session touches source files, so
  the rule's `paths:` does not load it. A domain review skill detects
  the installed contract by the contract probe: checking, in order,
  `<project>/.claude/rules/working-process/review-reports.md` then
  `$HOME/.claude/rules/working-process/review-reports.md`, and reading
  the file it finds. When a session does touch `docs/code-review/**`,
  the engine loads the rule as usual.
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
  distributed as a Rules payload"); the marketplace catalog entry and
  the repo-root README row are therefore unchanged. The only
  identity-adjacent change is the plugin README's own components
  documentation (previous bullet).

## Non-goals

- Any python-standards content — companion spec
  `2026-07-16-python-standards-design.md`.
- Review procedures, severity rubric sources, or reviewer agents —
  domain plugins own those; this rule owns only the report contract.
- A review orchestrator that maps changed files to domains, discovers
  installed `*-code-review` skills, and dispatches multi-domain runs —
  a future working-process release. This contract is deliberately
  sufficient for it: an orchestrated run is a mixed run with a
  `standards:` list.
- Per-finding lifecycle tracking across runs (finding IDs, status
  mutation) — `rerun-of` plus the Summary disposition note is the
  supported re-review model until a real consumer demands more.

## Verification

- `claude plugin validate .` and `claude plugin validate
  plugins/working-process` pass; review-reports.md frontmatter reviewed
  by hand (validate skips `rules/`).
- `ruleset-hash.sh` aggregate changes; after `claude plugin update`, the
  drift hook nudges and a sync-rules update classifies
  `review-reports.md` as an install row and `process-artifacts.md` as an
  auto-update row (absent local edits).
- A session touching `docs/code-review/**` loads the extended
  process-artifacts rule and the new review-reports rule; the contract
  probe's paths resolve in both install scopes.

## Sequencing

Working-process 0.5.0 ships before python-standards 0.1.0, which
declares `working-process ≥ 0.5.0` as its assumed convention range.

## Architect findings — 2026-07-16 round 1

Dual review (context-carrying + fresh reviewer); stricter grade kept.

- **Important (fresh)**: consumer detection unspecified — the rule's
  `paths:` keeps it out of context during review sessions, so the
  precedence mechanism had no handshake. → Fixed: contract-probe bullet
  in the contract (ordered path pair, project then user).
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

Round 2 (verification pass): all dispositions confirmed — the contract
probe's path pair verified byte-consistent with the sync-rules engine's
install layout, project-first order matching its conflict rule.
Verdict: LGTM.

Round 3 (delta review after the 2026-07-16 grilling session):

- **Important**: the local pocket contradicted the mode-detection
  observables as worded in process-artifacts (any-`.gitignore` /
  loose-`*` phrasing) and the fix was routed to the wrong rule. →
  Fixed: §1 now tightens the signal to "a `.gitignore` containing
  exactly `*`" in the rule that reads it; glossary Ignored-mode and
  First-create entries tightened the same way.
- **Minor**: the Filename bullet omitted the `local-` prefix variant. →
  Fixed: cross-reference added.
- `standards:` / `rerun-of` semantics, mixed-run boundary, glossary-term
  usage: clean, no findings.

Round 4 (confirmation pass): both round-3 dispositions verified resolved
— §1 owns the mode-signal disambiguation consistently with §3, the
glossary, and process-artifacts' install wording. Verdict: LGTM.

Round 5 (confirmation after the python grilling deltas): three-tier
first-create handling consistent with Committing and process-artifacts;
no banned terms residual. One minor fixed inline — the One-run bullet's
"standalone reviewer agent" collided with the Standalone-install term
(now "dispatched reviewer agent"; the bullet's stale team-thread mention
dropped alongside, consistent with the round-1 mode fix). Verdict: LGTM
for both specs.

Amendment — prompt-free filenames (2026-07-17, shipped as 0.6.0): the
first real review run surfaced a permission prompt for the canonical
timestamp+runid shell command; the developer rejected allowlisting as
needless friction. The contract dropped the shell command entirely:
date-only filenames with a model-generated 8-hex runid, uniqueness
carried by date + scope + the never-overwrite/retry rule. The
byte-identity machinery (verbatim quoting, allowlist rationale, the
python plan's Step 6a check) is obsolete with it. Same-day reports no
longer sort chronologically by name — accepted. Consumers' inline
fallbacks change in the same release (subset invariant preserved).
Architect delta round on this amendment: concerns → three fixes applied
(`rerun-of` resolution scoped to same-scope reports since model runids
are not globally unique; collision detection named as a file-tool
existence check, never shell; frontmatter `date` tied to the filename
date) → confirmation round LGTM pending stamping below.

## Amendment — 2026-07-20: line-less findings ordering

The salesforce-standards review stack (ticket #3) surfaced a layout
gap: subsection ordering was defined only for line-anchored findings,
while flows and declarative metadata are reviewed from metadata and
cite elements by name. The Layout rule now states that findings
without a line anchor are ordered by a domain-stated stable key (the
reviewing domain names the key and applies it consistently). Additive
gap-filling — no existing report shape changes; shipped as
working-process 0.9.0.
