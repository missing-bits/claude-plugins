# claude-plugins — domain glossary

Missing Bits marketplace of Claude Code plugins; its domain is the working
process the plugins support and the marketplace machinery that ships them.

## Language

**Process directory**:
A directory the working process creates in a project repo to hold work
artifacts (e.g. `docs/domain/`, `docs/specs/`, `docs/plans/`). Deliberately
narrow: configuration directories the process may also create (such as
`.claude/rules/` during a project-level rules install) are not Process
directories — their install questions are their own, defined where the
install is specified.
_Avoid_: artifact folder

**First-create question**:
The question — ignored mode or tracked mode — asked when a process
directory is created for the first time, or exists with no prior
decision: neither an observable signal (a `.gitignore` containing
exactly `*`, a git-tracked file) nor an explicit project instruction
declaring the mode (e.g. a CLAUDE.md note). Never asked when any of
these signals is present. A declared ignored mode is materialized by
whoever first acts on it — writing the `*` `.gitignore` — making the
decision observable; a declared tracked mode becomes observable with
the first committed file.
_Avoid_: self-ignore

**Ignored mode**:
A process directory with a `.gitignore` containing exactly `*`; its
contents stay out of the repo's git status. A `.gitignore` with any
other content (e.g. a local pocket's `local-*`) does not signal ignored
mode.

**Tracked mode**:
A process directory whose files are committed; detected by any git-tracked
file under it.

**Contract probe**:
The ordered path check a domain review skill — or a dispatching
review command, pre-dispatch — runs to find the installed
report contract: `<project>/.claude/rules/working-process/review-reports.md`,
then `$HOME/.claude/rules/working-process/review-reports.md` — first hit
wins, mirroring the Rules engine's project-over-user conflict rule. Part
of the review-reports contract: the paths may not drift independently.
_Avoid_: discovery, probe (unqualified)

**Store probe**:
The existence check a plugin other than project-memory runs to decide
whether the reviewed project keeps a Project-memory part: one test per
part, on the part's directory (`docs/memory/`, `.claude/memory/`) — never
on a file inside it. Three surfaces run it (the review-reports
Candidate-gap park offer and the two standards code-review restatements).
Distinct from the Contract probe, which finds the installed report
contract; the unqualified word stays banned there.
_Avoid_: index check, store check

**Review report**:
The single persistent document one code-review run writes under
`docs/code-review/` of the reviewed project — one run, one report,
written by the run's owner. Shape defined by the review-reports rule's
contract; a domain plugin's inline fallback is a strict subset of it,
never a different shape.
_Avoid_: review output, report file

**Finding**:
One graded problem a review round reports, cited with evidence — in a
design review (`architect`, `plan-adversary`) that is all it is. In a
Review report it additionally takes the counted shape the review-reports
contract defines: one violation class in one file, or at project level
when no existing file carries the violation — for tagged rules the rule
id names the class; for a Candidate gap the class is the one its offer
names. Its body enumerates every violating site — line numbers, or the
domain's stable key where lines do not apply. Cites exactly one rule id
(or `rule: none`); its severity is the cited rule's (a Candidate gap's
comes from the Authoring rubric). A finding with any site unfixed counts
as remaining in a rerun. Never what a Consultation returns — that is a
Contribution.
_Avoid_: issue, violation (as a name for the unit)

**Standards plugin**:
A domain plugin of this marketplace encoding coding standards for one
technology: area skills, a review stack that writes Review reports,
optionally a `*-plan-review` checklist and a Rules payload. A report's
`standards:` field names the standards plugin(s) the run reviewed
against.
_Avoid_: standards stack, domain-standards plugin

**Standalone install**:
A marketplace plugin used without working-process: its skills still load and
run, while anything depending on the working-process rules or Rules engine is
absent or degrades to the plugin's conditional-reference fallbacks (for a
standards plugin, review reports fall back to the inline subset and the
contract probe finds nothing). `solo` is NOT this — it is the run-owner mode
of a review run.
_Avoid_: solo install, solo profile

**Rules engine**:
The rules-distribution mechanism living in the working-process plugin: the
`sync-rules` skill, the drift hook, and their shared scripts. One engine
serves every Rules payload of the marketplace — payload plugins never copy
the mechanism.

**Rules payload**:
The `rules/` directory a plugin of this marketplace ships for distribution
by the Rules engine; installed into its own namespace,
`rules/<plugin-name>/`, next to a manifest. A plugin shipping one is a
payload plugin.
_Avoid_: rules plugin

**Drift**:
A mismatch between a Rules payload's current upstream content and the
state recorded at the last completed sync (the manifest's `rulesetHash`).
Detected by the drift hook, resolved by the `sync-rules` skill. Always a
content-hash comparison, never a plugin-version comparison.
_Avoid_: outdated rules

**Orphan**:
An installed rule set whose source plugin is no longer installed (or,
for a user-scope source, is disabled — a project-scoped source elsewhere
reports a contextual `enabled: false` and still counts as present);
detected during `sync-rules` state discovery, offered for removal or
adoption as the developer's own.

**Severity**:
The grading value a review finding carries: `critical | important |
minor`, fixed per rule in its rule tag and read off by the reviewer —
never judged per finding wherever a tag exists; a Candidate gap, having
no tag, is graded by the Authoring rubric. The value is canonical as a
word and its casing follows the syntax it sits in — lower case as a rule
tag's field value (`severity: minor`), capitalized in the ledger's
bracket slot (`[Minor]`). The collective noun is
"severity level" — never "tier", which stays reserved for the
model-capability ladder.
_Avoid_: severity tier

**Rule tag**:
The inline parenthesized annotation at a rule's (or sub-rule's)
definition site carrying its identity and grade:
`(id: <rule-id>; severity: critical|important|minor[; kind:
defect|hardening]; source: <source>)` — `kind` required exactly when
severity is critical, and the rule id backtick-wrapped inside the tag.
The single source of truth for severity; no roll-up section may
restate it.
_Avoid_: inline tag (unqualified), severity row

**Kind**:
The orthogonal facet on critical-severity rules: `defect` (a genuine
runtime/live-risk failure) or `hardening` (a standards-mandated
protection graded critical by house policy). A property of the rule,
assigned at authoring time — never judged per finding wherever a tag
exists; a critical Candidate gap is always `defect` (no standard exists
to mandate a hardening).
_Avoid_: runtime/hardening split, criticality class

**Authoring rubric**:
The severity guidance used when writing or editing a rule (and when
grading a Candidate gap). Canonical text lives in the repo authoring
rule and appears verbatim in exactly three other places — the
review-reports contract and the two code-review skills' standalone
fallbacks — never restated beyond those (including here). Lives at
authoring time; a reviewer never uses it to overrule a Rule tag.
_Avoid_: severity definitions, step-3 definition

**Candidate gap**:
A review finding that violates no defined rule: reported and counted
normally, cited `rule: none` (against the loaded domain skill lacking
the rule, or the standards plugin itself when no skill of the plugin
covers the concern — never asserted against a skill the run did not
read), graded by the Authoring rubric, and surfaced in the run's
reply as a candidate for a new rule — or, at a plugin-level citation, a
new skill — with offers to park it in Project memory (when a store
exists) or report it upstream, generalized. Never cited with an
invented rule id; the `rule: none` citation is the report's only
candidate-gap marker.
_Avoid_: uncited observation, unmatched finding

**Sub-rule**:
A dot-suffixed, tagged refinement of a rule whose violations grade
differently from the rule's default — its own entry under the rule's
prose, with its own absolute severity (and kind when critical). Its
identifier is the sub-id, `<group-id>.<suffix>`. A sub-rule whose
severity equals the group default is redundant and not created.
_Avoid_: sub-case, child rule, variant

**Group default**:
The severity a rule's own tag carries, applied to a finding that
violates the rule but matches none of its sub-rules. Every rule has
one — including rules with no sub-rules, where it is simply the rule's
severity.
_Avoid_: base severity, fallback severity

**Tier**:
A relative rung on the platform's current capability ladder of model
families ("most capable available", "mid"), resolved at dispatch time —
never a concrete model name. The prescribed tier is the tier the
model-selection heuristic assigns to a given dispatch.
_Avoid_: model level

**Degraded verdict**:
A review verdict produced below the prescribed tier by anything other
than the developer's deliberate choice — a cap refusal (including a
consented one-tier drop after it), a silent platform substitution, or
an under-dispatch the dispatcher did not knowingly decide. Marked by
the `(degraded <date>)` token in the `*-fallback` frontmatter field and
entitled to a re-review offer.
_Avoid_: capped verdict, lowered verdict

**Chosen verdict**:
A review verdict produced below the prescribed tier because the
developer deliberately dispatched below it, before any platform
refusal. Marked by the `(chosen <date>)` token in the `*-fallback`
field; carries the same re-review offer as a degraded verdict.
_Avoid_: voluntary degradation

**Adjudication**:
The developer's close of a `blocking` verdict without a fresh round,
written `blocking (adjudicated <date>)` in the document's frontmatter.
Closes a round; the finding-level counterpart is a Ruling.
_Avoid_: developer override, manual close

**Ruling**:
The developer's authorization of one finding's disposition, written as
the `ruling: <date>` clause on that finding's ledger line. Closes a
finding; the round-level counterpart is an Adjudication.
_Avoid_: developer decision (as the name), developer fix

**Fallback**:
The model that actually produced a degraded or chosen verdict, standing
in for the prescribed tier; named (as a family alias) in the value of
the `*-fallback` frontmatter field. A dispatch at the prescribed tier —
e.g. mid tier for a small mechanical plan per the heuristic — is not a
fallback.
_Avoid_: backup model, replacement model

**Fallback record**:
The `*-fallback` frontmatter field (`architect-fallback:` /
`adversary-fallback:`): the record that a verdict was produced below
the prescribed tier — the fallback's family alias plus an agency token,
`degraded` (unchosen: forced or unnoticed) or `chosen` (deliberate). A
bare record means the re-review offer is live; a fresh prescribed-tier
round removes it (a degraded one refreshes it), a waiver annotates it.
_Avoid_: sub-tier record

**Consumption gate**:
The workflow step at which a document's review verdict is about to be
relied on as the basis of further work — plan-writing for a spec,
implementation for a plan. Where re-review offers on fallback-recorded
verdicts fire.
_Avoid_: usage point

**Unfinished-work list**:
The named section of the spec-plan-lifecycle rule holding one entry per
class of unfinished process work — class name, grep command, the owner
of the next move, and optionally the entry's own match scope — and the
single definition site for which classes exist. A class that accepts
the default scope costs one edit in the rule and none in the consumers
that run it; a class that publishes its own scope costs a consumer edit
too, and the ledger class is the first. A command's output is hits to
confirm against the entry's scope — the frontmatter block by default —
never Findings.
_Avoid_: anchor list, debt list

**Misplaced stamp**:
A process field — `grilled`, `architect`, `adversary`, `*-fallback`,
`integrity` — sitting outside the top level of a document's
frontmatter, where the stamping steps put it. One entry of the Unfinished-work list detects it,
and the value is irrelevant: a misplaced `LGTM` is as malformed as a
misplaced `concerns`.
_Avoid_: malformed stamp, nested field

**Persona**:
A role plus its duties, single-sourced in one `*_PERSONA.md` file at the
working-process plugin root and adopted by one or more persona surfaces;
two exist — architect and system designer — their shared duties and mutual
boundary held once in `PERSONA_COMMON.md`. `plan-adversary` carries its
role inline and is a reviewer, not a persona; the org user roles the
salesforce-security-model skill calls personas are a different domain
entirely.
_Avoid_: role, hat

**Persona surface**:
A component that adopts a persona and puts it to work: a verdict-bearing
agent (`architect`), a consult agent (`*-consult`), or a session skill
(`*-session`) — the architect has three, the system designer two. Short
form "surface" inside working-process material; unqualified "surface" in
the repo's own rules means something else, a document location where a
statement lives.
_Avoid_: mode, channel, entrypoint

**Audit agent**:
An agent whose report ends in no verdict and stamps nothing: it checks a
document and returns material for the dispatcher's disposition — hits
(`propagation-auditor`, the mechanical pass) or defects-with-quotes and
ranked questions (`integrity-auditor`, the judgment pass). Dispatched as
a gate before expensive work: the precondition is a disposed audit —
every hit fixed or dismissed, every defect applied or declined — never
an empty one, and never a judgment on the design. The third dispatch category beside Verdict agent
and Consultation: an audit agent adopts no persona and its output is
never a Contribution.
_Avoid_: sweep agent, verifier

**Hit**:
The unit a mechanical check returns — an Unfinished-work list command's
match or a propagation-auditor detection: located, binary, confirmed or
dismissed by the dispatcher, never graded. Graded problems are Findings
and belong to review rounds.
_Avoid_: mechanical finding

**Disposition ledger**:
The record a review loop keeps inside the reviewed document, under one
`## Review rounds` section: what each round found and what became of it.
It carries the loop's durable state, and nothing else does — the
session, the reviewer and the developer are all volatile, and these
documents stay uncommitted through the rounds. Per-finding and per-hit
state is written into it; loop-level state is derived from the round
headings and stored nowhere. The name comes from the terminal states
that dominate it in practice; a leading token names a state, terminal or
not.
_Avoid_: review log, findings table, round log

**Round heading**:
The immutable record of one dispatch, opening a round's block in the
disposition ledger: date, agent, model self-report, verdict, ordinal and
scope. The loop's derived state — round count, the all-Minor signal, the
diff-scoped chain — is read by folding these.
_Avoid_: round title, round record (for the heading alone)

**Disposition line**:
One line of the disposition ledger carrying the state of one Finding:
its leading token is that state, its clauses the payload. The unit the
ledger's state machine acts on.
_Avoid_: finding line, ledger entry

**Gate line**:
One line of the disposition ledger carrying the state of one Hit,
written by the propagation gate. It shares the container with
disposition lines and nothing else — its own leading token, no severity,
no license.
_Avoid_: hit line, audit line

**Verdict agent**:
An agent whose report ends in a verdict the dispatcher stamps into the
reviewed document's frontmatter — `architect` and `plan-adversary`.
Orthogonal to Persona: the architect is a persona surface, the
plan-adversary a plain reviewer. Consult agents are not verdict agents —
a consultation returns a Contribution and stamps nothing.
_Avoid_: review agent (unqualified), reviewer agent

**Relay**:
The delivery of a background agent's result to the developer before any
further action on it — a verdict agent's report before its stamp (the
verdict, the model self-report, and every finding in substance), a
consultation's Contribution attributed and substantially verbatim. The
developer's standing veto point.
_Avoid_: report back, forward (as the term)

**Session skill**:
A skill whose content is an open-ended conversation, named `*-session` —
`architect-session`, `grilling-session`, `memory-review-session` among
them. Some are persona surfaces, some adopt no persona at all
(`grilling-session`). Unqualified "session" always means the Claude Code
conversation instead: what a session-scoped consent decision lasts for,
and what a consult agent is isolated from.
_Avoid_: session (for the skill), conversational skill

**Consultation**:
A verdict-free exchange with a persona, returning a contribution and
stamping nothing. Verdict absence is the discriminator, not the absence of
stamping — an `architect` dispatch on a bare question also stamps nothing
(no document to stamp) yet still grades, so it stays a review round.
_Avoid_: informal review, advisory review

**Contribution**:
What a consultation returns: reasoning, options, and the questions the
persona would need answered next, relayed to the developer attributed and
substantially verbatim. Never graded and never counted — the graded,
counted unit is a Finding, which belongs to verdict-bearing reviews.
_Avoid_: consultation finding, recommendation

**Project memory**:
The in-repo, rule-loaded memory store the project-memory plugin defines, in
two parts — Team memory and Private memory — mirroring Home-dir memory's
thin-index-plus-on-demand-topic-files model, but living in the project.
Distinct from Home-dir memory, which it redirects project-scoped facts away
from. Each half is a *part* (Team memory, Private memory).
_Avoid_: project MEMORY.md, memory tier, memory layer

**Team memory**:
The committed part of Project memory, `docs/memory/`; the first-create
question applies — asked by the project-memory core rule — and it counts as a
Process directory when the working-process rules are installed. Holds
team-relevant parked ideas, cross-ticket state, and operational gotchas.

**Private memory**:
The per-user part of Project memory, `.claude/memory/`; always ignored, never
asked, and NOT a Process directory — a per-user store under the `.claude/`
config namespace, governed by the Project-memory rule.
_Avoid_: local memory

**Auto-memory**:
The harness's own memory mechanism — the notes Claude Code writes for itself,
their `MEMORY.md` index and its load budget, and the `autoMemoryDirectory` /
`autoMemoryEnabled` settings that place and disable it. The mechanism, never a
store: the store it manages by default is Home-dir memory. Project memory
borrows none of its machinery — even a Hybrid store only points the harness
at the plugin's directory.
_Avoid_: native memory, auto memory (unhyphenated)

**Home-dir memory**:
The store Auto-memory manages when no redirect points it elsewhere — one
per checkout path and per Environment, kept by default under
`~/.claude/projects/<project>/memory/`; a default, not a definition, since
`autoMemoryDirectory` may place it anywhere. The store the Project-memory
rule redirects project-scoped writes away from; it keeps cross-project and
personal facts.
_Avoid_: native memory

**Hybrid store**:
The Private memory store that is the current session's Auto-memory
directory — the opt-in redirect (`autoMemoryDirectory` pointing at
`.claude/memory/`) honored in that session and landing on the store. A property of the
session, never of the checkout: the same store may be hybrid in one
environment and plain in another. Team memory is never one — Auto-memory's
team mounts are server-backed, so a repo directory cannot join.
_Avoid_: hybrid memory, hybrid mode

**Environment**:
One filesystem view a session runs in — its own path namespace, settings
home (`~/.claude`), and trust record: the host, a dev container, a WSL
distro. The unit the redirect activates per, and the unit each Home-dir
memory store belongs to; one checkout may be visible from several
environments through different absolute paths.
_Avoid_: machine (where the path namespace is what matters)

**Idea entry**:
A Project-memory entry with the idea shape: an `idea-` filename prefix and
lifecycle frontmatter (`status` parked → spec'd | dropped, a `spec:` pointer,
`ticket`), as opposed to a plain note (the default shape, `ticket`-exempt,
recalled on demand). The prefix is the rule's selector for the lifecycle
frontmatter set.
_Avoid_: backlog item

**Archive**:
The closed-entry record of a Project-memory part — `ARCHIVE.md`, holding one
line per closed entry in a **Done** or **Dropped** section, read on demand and
never at session start. Distinct from a live entry (listed in `MEMORY.md`): a
closed entry keeps no body, only its archive line.
_Avoid_: archive folder, backlog

**Live entry**:
A Project-memory entry currently listed in `MEMORY.md` — an active note or a
`parked` idea. The only entries reachable at session start (via the index).
Opposite of an archived (closed) entry.
_Avoid_: active entry, open entry

**Close (an entry)**:
Move an entry out of `MEMORY.md` when it reaches a terminal state — Done (its
content now lives in a spec, ADR, glossary, or another artifact) or Dropped
(abandoned) — leaving a one-line Archive record. Deleting an obsolete entry is
NOT a close: it leaves no Archive line.
_Avoid_: retire, archive (verb)
