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
  — so the agent never meets an undecided directory. The decided
  signals (including the declared-instruction signal) are owned by
  the process-artifacts rule. The dispatch itself runs in the
  background: a review never blocks an interactive dispatching
  session, and the run's owner writes the one report regardless of
  fore/background mode.
- A run with no interactive dispatcher (automation, nested agents)
  defers: it writes the report and leaves the directory undecided.
  This is safe because reports are never staged (see Committing); the
  next interactive touch asks per the process-artifacts rule.

## One run, one report

Each review run writes exactly one report, written by the run's owner
— the solo session or the dispatched reviewer agent.

## Filename

`<YYYY-MM-DD>-<scope-slug>-<runid>.md`, optionally prefixed `local-`
(see Local pocket). `<scope-slug>` is a short kebab-case slug of the
reviewed scope, matching the frontmatter `scope`. Both variable parts
come from the session itself — generating a filename MUST NOT run a
shell command or prompt the developer for anything:

- the date is today's date as the session already knows it;
- `runid` is 8 lowercase hex characters the run's owner generates
  itself — model-generated randomness suffices, because uniqueness is
  carried by date + scope + the collision rule below, not by the
  runid's entropy alone.

Never overwrite an existing report: check for an existing file with
the session's file tools (a read/list of the target path — never a
shell command), and on a collision generate a new runid and retry.
Same-day reports do not sort chronologically by name — an accepted
trade for a zero-prompt contract.

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

- `date`: ISO date of the run, matching the filename date.
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
  re-reviews, resolved among reports of the SAME scope — runids are
  model-generated and not globally unique, so the scope, not the runid
  alone, carries the identification. When set, the run's owner reads
  that report and notes the prior findings' disposition in Summary —
  fixed / remaining / new. Disposition tracks sites within a finding
  ("lines 42, 87 fixed; 130 remaining"); a partially fixed finding
  counts as remaining — a finding lives until its last site is fixed.
  Reports are self-describing (they may live git-ignored or in an
  archive outside the repo): rerun behavior never depends on anything
  unreadable from the reports themselves. When the prior report's
  findings do not follow the finding unit (a pre-convention report,
  readable off the report itself), the Summary disposition says so
  and maps prior findings best-effort; count deltas across that
  boundary are not comparable.
- `findings`: severity counts; they MUST equal the body.

## Run scope

A domain review command reviews only its own domain's files; files
outside the domain are noted in Summary as out of scope. A mixed run —
several standards plugins loaded at once — writes ONE report listing
every standards plugin in `standards:`. Per-finding attribution — which
rule id (and thus severity) a finding cites — stays domain-owned; the
citation form itself (`rule: none`, kind labels) is defined by this
rule.

## Layout

1. **Summary** — outcome, out-of-scope notes, and (for a rerun) the
   prior findings' disposition.
2. **`## Project` section**, present only when needed, always FIRST —
   before the per-file sections: the home of findings not
   attributable to an existing file (a missing lockfile, an absent
   manifest). Same severity subsections as a file section; findings
   ordered by rule id, `rule: none` findings last, ordered by
   violation-class name.
3. **Per-file sections**, each with **Critical → Important → Minor**
   subsections; findings within a subsection in ascending line order.
   Findings without a line anchor — files reviewed from metadata
   rather than source lines — are ordered by a domain-stated stable
   key: the reviewing domain names the key (e.g. cited element name,
   alphabetically) and applies it consistently.

A finding is one violation class in one file (or at project level):
for tagged rules the rule id names the class; for `rule: none`
findings the class is the one the candidate-gap offer names. The
finding's body enumerates every violating site — line numbers, or the
domain's stable key where lines do not apply — and the finding
anchors and sorts by its first violating site. One location violating
two rules yields two findings. `findings:` counts therefore mean: the
number of (violation class, file-or-project) pairs to fix.

Files with no findings and empty severity subsections are omitted. A
zero-findings run still writes the document.

## Finding citations

- A finding that violates a defined rule cites its most specific id:
  `(standard: <skill>, rule: <id>)` — the sub-id when a sub-rule
  matched, the group id otherwise. When a matching rule exists, the
  specific id is mandatory; a bare `(standard: <skill>)` citation is
  not a valid finding. A finding cites exactly one rule id — singular
  `rule:` key; its severity is the cited rule's.
- A finding no defined rule covers is still reported and counted:
  cited `(standard: <the loaded domain skill that lacks the rule>,
  rule: none)` — or, when no skill of the plugin covers the concern,
  at plugin level: `(standard: <plugin-name>, rule: none)`. A concern
  covered by the domain of an existing but not-yet-loaded skill is
  NOT a candidate gap — the reviewer loads that skill and grades by
  its tags; `rule: none` is never asserted against a skill the run
  did not read. In a mixed run the cited plugin is the one whose
  domain owns the finding's file; a project-level finding routes by
  its violation-class domain. Graded by the authoring rubric below;
  when graded critical — always `kind: defect` (hardening denotes a
  standards-mandated protection, and a `rule: none` finding has no
  standard mandating it); when graded below critical while touching
  data integrity, security or sharing, or a platform limit — the
  finding states in one clause why it falls short of critical. A
  plausible-looking rule id is never fabricated.
- Critical findings carry the rule's kind inline:
  `(standard: <skill>, rule: <id>, kind: defect|hardening)`; the
  Summary headline adds a prose breakdown, e.g.
  "critical: 33 — 12 defect, 21 hardening". Counts in `findings:` stay
  the three severity keys — kind adds no frontmatter field.
- When the loaded domain skill's rule tags carry no severity (a
  pre-adoption plugin version), the reviewer grades by that skill's own
  documented severities and omits the kind labels and breakdown rather
  than judging them per finding.

Authoring rubric (canonical in the owning repo's authoring rule;
this excerpt is verbatim-identical):

- **critical** — a defect that corrupts data, breaks security or
  sharing, or blows a platform limit on a bulk path;
- **important** — violates a standard in a way that forces rework or
  hides bugs;
- **minor** — naming, style, documentation.

## Candidate-gap offers

`rule: none` findings are candidate standards gaps. The `rule: none`
citation is the report's only candidate-gap marker; the proposals
live in the run's reply, never in the report. After writing the
report, the run's owner lists them in its reply — one line each:
violation class, proposed rule id, graded severity (a plugin-level
`rule: none` finding may propose a new skill instead of a new rule) —
and then offers, never performs unprompted:

- **Project-memory park** — only when the reviewed project keeps a
  Project-memory store (probe `docs/memory/INDEX.md` and
  `.claude/memory/INDEX.md`). The write is done by whoever accepts,
  never by the review run. Store selection: explicit guidance wins
  (project CLAUDE.md, the developer's own instructions, the store's
  conventions); otherwise with both stores present the offer asks the
  developer which one; with one store it names that one. No store — no
  offer, and never an offer to create a store.
- **Upstream report** — always offered: a report to the standards
  plugin's source repository, resolved at offer time from the installed
  marketplace's source metadata (e.g. `claude plugin marketplace
  list`); a non-public source (a directory-source marketplace, a
  direct install) degrades the offer to a generalized draft with no
  filing target. Two gates: acceptance produces the draft, shown in
  full; only explicit approval files anything. The draft carries the
  violation class and a proposed rule — never the reviewed project's
  code, identifiers, or name.

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

Project-root detection (each ecosystem's project marker file), rule ids
and their severities (defined in the standards skills' rule tags),
team-mode extensions, and the review procedure itself. The `rule: none`
citation form, the kind label rendering, and the candidate-gap offers
are contract-owned (defined above).
