---
ticket: none
date: 2026-11-17
status: approved
grilled: 2026-11-17
architect: concerns (resolved 2026-11-17)
integrity: 2026-11-17 (sha: d31a3a4)
decisions: registered
branch: feature/document-check
base: develop
---

# Document check — the gate's mechanical half

The propagation gate calls documents clean where a script could have
proved them wrong. This spec ships `wp-document-check`, a script that
runs Document checks over the mechanical classes, and makes the
dispatcher run it, and the existing `decision-coverage` script, beside
the auditor rather than through it. It is package 4 of the release
queue, widened from technical designs to all three document classes on
the evidence below.

## Problem

Evidence gathered 2026-11-16 and 2026-11-17 from four sources (records
in the developer's private store, not committed): the technical-design
dogfood in a devcontainer project, gate records in a web-application
project and in a Salesforce project, and this repository's own review
rounds.

- **The gate misses what a parse settles.** About 70 defects passed a
  gate and surfaced later in an architect, adversary, integrity or
  implementation read. About 30 belonged to classes a script decides
  without judgment: an internal reference to a section that does not
  exist ("the remove sequences below"), a `path:line` citation outside
  its file or off its symbol, a quoted license that does not occur in
  the line it cites, a named document that does not exist, a
  technical-design table relation with no row behind it, and an
  `integrity:` stamp whose hash no longer matches (left out, see
  *Non-goals*).
- **The gate says "checked" where it did not check.** On those classes
  the auditor also reported "consistent" or `CLEAN`: Sonnet in 10 of 18
  controlled runs, Haiku in 4 of 4. Five consumer enumerations in the
  web-application project claimed "checked, no hit" and were wrong.
- **The auditor skips scripts it is told to run.** The card tells it
  to run `decision-coverage.py` and copy the output. In the Salesforce
  project, three of the four runs whose brief required the script's
  lines returned without them.

A rule asking the auditor to try harder has already failed: the card
already says "derive, never recall". What is missing is a Document check the
auditor cannot skip.

## Goals, non-goals, anti-goals

Goals:

- A gate never passes a document carrying a defect of a form the
  Document checks settle.
- The script runs on every gate, whatever the auditor does, unless the
  developer orders a dispatch without it (D8).
- The auditor never writes "checked, no hit" for a consumer enumeration
  it did not run.

Non-goals:

- Counters ("four rows" against the table below): recognising them
  needs a heuristic, and a heuristic's false hits would block the gate.
- Identifier occurrences in the script. The auditor already enumerates
  consumers; D7 makes it show its work.
- Running a plan's published commands — a harness job, not a text check.
- Semantic defects: contradictory behaviour, a lost qualifier, sequence
  order. They drove most integrity-audit finds and stay with the
  readers.
- Re-measuring Haiku against Sonnet on the gate.
- The `integrity:` stamp. After a licensed fix wave a stamp is stale by
  design, so on every gate but the consumption gate a stale stamp is
  expected; the consumption gate already recomputes and compares it.
- Launchers for the bash scripts in `scripts/`; their callers (hooks,
  the settings block, `sync-rules`) resolve them by path already.

Anti-goals:

- A script hit that needs judgment to confirm. A false hit blocks the
  gate and wastes a fix wave; what the script cannot settle goes to its
  `not checked` lines instead.
- The script's result reaching the auditor. The two read independently.

Constraints and estimates (estimates, never thresholds):

- The script is about 300–400 lines of Python 3.9+, standard library
  only; the plan about 6–8 tasks.
- Reused: the launcher from package 6, adapted by two lines (D4),
  `decision-coverage.py` (its logic untouched), and the declared table relations of
  the technical-design rule.
- Accepted risks: on macOS a `/usr/bin/python3` stub may open an
  install dialog rather than fail (untested, as for `wp-phrase-check`);
  the script covers fewer than the 30 or so known misses in mechanical
  classes — the stamp and backticked paths left it after round 1 — and
  the rest stays with the auditor or with nobody.

## Decisions

- **D1** — The plugin ships `bin/wp-document-check`, running
  `scripts/document-check.py`, on any design spec, technical design or
  plan. Argued in *The Document checks*.
- **D2** — The script reports a hit only where its parse settles the
  defect without judgment. Every form it cannot settle is counted on a
  `not checked` line, never reported as a hit. Argued in *The Document checks*.
- **D3** — Two Document checks run on every document: internal
  references and citations, a Markdown link target counting as a
  citation. Table closure runs on a
  technical design alone, on the segments D10 settles; the segments it
  leaves not checked stay the auditor's, under duty 11 (D12). Argued in
  *The Document checks*.
- **D4** — One launcher serves every Python script: `bin/wp-<name>`
  runs `scripts/<name>.py`, the name read from the launcher's own file
  name. `bin/` carries identical copies, never symlinks, which break in
  a Windows checkout. Argued in *One launcher*.
- **D5** — `decision-coverage` moves behind the launcher as
  `wp-decision-coverage`; its logic and output do not change. Argued in
  *One launcher*.
- **D6** — The dispatcher runs `wp-document-check` and, on a plan or a
  design spec, `wp-decision-coverage` before it dispatches the auditor,
  and disposes of their hits — fixed, dismissed, or held, which ends the
  episode as a held hit does today — until both scripts are clean of
  undisposed hits. That loop costs seconds and spends none
  of the episode's re-dispatches. It then dispatches the auditor, which
  no longer runs either script. The gate passes once every hit from
  either side is disposed. Argued in *Who runs it*.
- **D7** — The auditor's card forbids "checked, no hit" on a consumer
  enumeration unless the report shows the command it ran and the hit
  count from its output; without them the line reads `not checked`.
  Argued in *Who runs it*.
- **D8** — A script that cannot run — no Python 3.9+, a crash, any exit
  other than 0 — is an ordinary error, never a hit: the gate stops and
  its message goes to the developer. Where the message names a cause in
  a document, such as a `spec:` pointing at a missing file, the session
  may fix it and re-run; otherwise the developer decides, installing
  Python and re-running, or ordering the dispatch without Document
  checks, an answer that holds for the rest of the session. Nothing is
  written to the ledger. Argued in *Who runs it*.
- **D9** — A Markdown link or a `path:line` that does not resolve is a
  hit only when it names a directory, that directory exists, and a plan
  does not create the file in a `Create:` line; a bare file name and
  every other unresolved path are not checked. A missing backticked
  path carrying no line is not checked on any document. Whether git ignores the path
  plays no part. Argued in *The Document checks*.
- **D10** — Table closure resolves only the cell segments that equal a
  row of the target table, after parenthesised text is dropped and the
  cell is split at commas and semicolons. A segment naming more than
  one row and an empty side are hits; a segment naming no row is not
  checked. The declaration rows come from the plugin's own copy of the
  technical-design rule. Argued in *The Document checks*.
- **D11** — The scripts run at every point the gate fires — before a
  verdict dispatch, after a fix wave, before an integrity audit, and at
  the authoring-time offer, accepted or declined — whether or not the
  auditor is available.
  Without the auditor the gate is the scripts alone, and gate lines and
  the held batch apply to their hits unchanged; script re-runs are
  unbounded on purpose, since each costs seconds.
  Argued in *Who runs it*.
- **D12** — The duty numbering stays: duties 10 and 11 keep their
  numbers and their rows in the author's checklist rule. Duty 10's
  first line says the dispatcher's script performs it, and its steps
  stay as the definition the script implements. Duty 11 stays the
  auditor's for a name matching no row — the form D10 leaves not
  checked, named by form since the auditor never sees the script's
  output — and its text says the script resolves the rest as D10
  defines. Argued in *Who
  runs it*.
- **D13** — The scripts' output never reaches the auditor's brief, and
  the relay reports the scripts' dispositions and the auditor's hits
  together. Argued in *Who runs it*.
- **D14** — The plan sweeps every shipped sentence D1, D3, D5, D6, D8
  or D11 make false, enumerating them by grep, in a task of its own.
  Argued in *Who runs it*.
- **D15** — Under `## Review rounds` the Document checks read only the
  lines below the last round heading, the round in progress; earlier
  rounds record past states whose citations later waves moved, so
  checking them would breed a dismissal every gate. Argued in
  *Citations*.

## The Document checks

`wp-document-check <document>` reads one document and prints one line
per hit, then three summary lines — `references`, `citations`,
`table-closure` — then exits 0 whenever the
Document checks ran, hits or not; 1 when the document cannot be read; 2 on a
usage error — the exit codes `decision-coverage` already uses. A hit
names the site, the claim and the Document check, by the same three
names:

    <file:line> — <claim> — check: <check name>

A summary line counts what the Document check read and what it could not settle:

    document-check: references 14 checked, 3 not checked
    document-check: citations 9 checked, 4 not checked
    document-check: table-closure not applicable

The script's `table-closure` summary line replaces the card's
`table-closure:` line; the card's rule that no other document carries
that line goes with it.

The document type is read as `decision-coverage` reads it, the path
test first: `technical-designs/` directly under `docs/`, or a file name
ending `-technical-design.md` (a ticket directory's design), marks a
technical design; otherwise a frontmatter `spec:` field marks a plan,
and its absence a design spec. A technical design also carries `spec:`,
which is why the path decides first.

**Internal references.** A section named in italics or quotes beside
"below" or "above" resolves to a heading of the document, below or
above where the text says so, and a plan's "Task N" resolves to a task
heading. A name matching no heading may name another document's
section, so it is not checked; so are a bare "below", a `§N` (in this
repository it mostly cites another document) and a "Step N", whose
steps are list items numbered per task. What this catches is a named
section on the wrong side and a "Task N" with no task. Not caught: the
measured miss of a technical design citing "remove sequences below"
that did not exist — unformatted, and a name matching no heading
besides — and three step references pointing at the wrong, existing
steps after a renumbering; both take judgment, and stay the auditor's.

**Citations.** A `path:line` or `path:a-b` names an existing file, and
its line or range lies inside it; an unresolved path follows D9. Written `` `symbol` (path:line) ``,
the symbol also occurs on the cited line. Any other shape near a
citation is not checked. A `license:` or `ruling:` clause carrying a
double-quoted string and a location — a path, a `path:line` or a
heading of the same document — finds that string at the location,
normalised as `wp-phrase-check` normalises (a line's leading list or
quote marker dropped, lines joined, whitespace collapsed, case
ignored). A Markdown link target resolves to an existing file,
relative to the document or to the repository root, by the same D9
rule. A path that exists in the author's checkout resolves whether git
tracks it or not, since the gate runs there. A backticked path carrying
no line is counted and, when missing, not checked (D9): a design spec or
a technical design names files not yet written, and a plan names
conventions and placeholders as paths, so a missing one cannot be told
from a defect without judgment. Measured misses: nine `path:line`
citations off by lines in one plan; nine license quotes that did not
occur in the ruling they cited — ledger lines, which D15 keeps in
reach while their round is in progress. Not caught: a ledger citing a
"technical design round 2 integrity note" that never existed, and the
stale `.claude/memory/INDEX.md` names the spike found — prose and
backticked paths, which the auditor's consumer enumeration still
reaches.

**Table closure** (technical design only). For every relation the
technical-design rule declares, the script splits each cell as D10
says: `producer → consumer` at the arrow first, then at commas and
semicolons, `external: <name>` being no reference. Dropping
parenthesised text and splitting at semicolons reads more loosely than
the rule's comma grammar, on purpose: a prose cell still yields the
part names it holds, and since an unmatched segment is not checked
(D10), no hit arises that the rule's own grammar would not raise. It
reads the declaration table's rows from the plugin's own copy of the
rule, in the plugin's `rules/` directory beside `scripts/`, so the copy matches the script's version; the
splitting grammar is code, and a declaration that changes it changes
the script too. The `table-closure:` line moves here; a name matching
no row stays the auditor's, under duty 11 (D12). Real designs write prose in these cells — "the
platform", "Host tasks (`profile:new` once)" — so a strict reading
would block every design on prose; D10 trades recall for no false hit.
Caught: an empty side and a name matching several rows. Not caught:
the four measured relations naming no row, which stay the auditor's
under duty 11, and the false "tables absent", which was an auditor's
claim the script's count of relations now replaces.

## One launcher

Package 6 shipped one launcher for one script. Generalising it costs
two lines — the script path and the error message's name: the launcher derives `scripts/<name>.py` from its own name
`wp-<name>`, and each command in `bin/` is a copy of the same file. A
test asserts the copies are byte-identical and that each resolves to an
existing script.

`decision-coverage.py` runs today as
`python3 ${CLAUDE_PLUGIN_ROOT}/scripts/decision-coverage.py`, which has
no fallback where only `python` or `py -3` exists. Behind the launcher
it gains the fallback and the plugin keeps one convention for calling
its scripts. Only Python scripts get a launcher; the bash scripts gain
nothing from one.

## Who runs it

The dispatcher runs both scripts first, synchronously — each finishes in
seconds — and disposes of their hits until none is undisposed: `hit
fixed`, `hit dismissed` where the session believes one wrong, or, for a
`wp-decision-coverage` coverage hit only, `hit held`, which ends the
episode as today — the same ledger lines as the auditor's. Running them first means the
auditor reads the text the script fixes produced, rather than a text
those fixes are about to change, and a script re-run spends none of the
episode's two re-dispatches. Only then does the dispatcher send the
auditor, in the background as before, with nothing from the scripts in
its brief. The relay reports the scripts' dispositions and the
auditor's hits together.

The procedure's gate section and the card change together: the card
drops duty 10's "run the derivation" paragraph and its
`decision-coverage:` lines and the `table-closure:` line, since the
dispatcher now carries them. Every shipped sentence that D1, D3, D5,
D6, D8 or D11 make false changes with them — whatever the auditor did
that the scripts now do, the gate's precondition and order, and every
enumeration of the plugin's commands — and the plan enumerates those
sentences by grep. The spec names none of them: three gate runs each
found sites a list here had missed.

The scripts do not depend on the auditor (D11): they cost seconds and
cannot be skipped, so they run at every point the gate fires — at the
authoring-time offer too, whether or not it is accepted, since they
only read — and where the auditor is not installed they are the gate.
The duties keep their numbers (D12), so no "duty N" citation breaks.

The auditor keeps the consumer enumeration, the class the script leaves
alone, and the table-closure segments the script cannot settle. One
sentence in its card (D7) closes the gap the evidence showed: "checked,
no hit" on a changed identifier requires the command and the count from
its output in the report.

A script that cannot run is an error, as an agent that dies is (D8). A
launcher that finds no Python prints the interpreters it tried and
exits non-zero; a crash or an unreadable document exits non-zero too.
The dispatcher stops the gate and puts the message to the developer.
An unreadable document is often a document-side cause — `decision-coverage`
exits 1 on a `spec:` naming a missing file, which the auditor's card
makes a fixable hit today — so where the message names such a cause the
session fixes it and re-runs, as it would that hit. Otherwise the
developer installs Python and re-runs, or orders the dispatch anyway,
as they may order any step; that answer holds for the session, since a
deterministic failure would stop every later gate on the document.
Nothing reaches the ledger, and no held class or ledger shape is added.
The README already lists Python 3.9+ as a requirement.

## Settled for the plan

Calls made after the integrity audit, as the builder would make them;
none changes what is built:

- A name is matched to a heading after the `wp-phrase-check`
  normalisation, at any heading level; "beside" means in the same
  sentence. Fenced blocks are not read.
- A citation token is `path:line` or `path:a-b`, backticked or not;
  its path resolves against the document's directory, then the
  repository root. A bare file name is skipped whole (D9).
- A `Create:` line is read in the plan under check only, in the shape
  the writing-plans template gives it (`- Create: \`path\``). A URL or
  `#anchor` link target is not checked.
- In a `license:` or `ruling:` clause the first double-quoted string is
  the quote, and the location is the first `path:line`, path or
  italicised heading after it; a clause with neither is not checked.
- The scripts re-run before every auditor re-dispatch, since a fix wave
  can break what they check. Their gate lines carry the caption
  `(document-check)` or `(decision-coverage)` where today's carry the
  model.
- At a declined authoring-time offer the scripts' hits are shown to the
  developer and written nowhere, since no gate episode runs.
- The developer's order under D8 covers the failing document for the
  session and both scripts on it; without the auditor "the dispatch" is
  the one the gate guarded, and the relay says Document checks did not
  run.
- Table closure finds Parts, Contracts and State by their section
  headings and columns by header text, matching cells after stripping
  backticks and casefolding. A side holding only `external:` names is
  not empty; one holding only parenthesised text is.
- Duty 10's lead-in to its steps survives the card edit.
- The launcher reads its name from the path it was invoked by, before
  resolving symlinks. Exit 2 for no Python and for usage alike is
  intended: D8 treats every non-zero exit as an error.

## Verification

- Unit tests for each Document check against fixtures holding one known defect
  and its clean twin, drawn from the measured misses above.
- A run over every spec and plan in `docs/` of this repository and
  over two technical designs from other projects. The gate reads only
  documents not yet `implemented`, and on those no hit may be false
  (D2). Hits on `implemented` documents are listed and classified, not
  narrowed away. The first spike of 2026-11-17 found 30 there, 12 of
  them real (stale names, stale stamps, moved files) and 18 that a gate
  would dismiss; with the integrity stamp dropped and backticked paths
  not checked, most of both groups leave the gate's reach.
- The launcher test covers all three commands, and the copies' identity.
- A live gate in this repository with the plugin loaded from the
  checkout: the dispatcher runs both scripts before the auditor, and
  the relay carries their lines.

## Out of scope

Everything under *Non-goals*, and the tier of the auditor itself.

## Review rounds

Gate lines from the pre-round propagation episodes, 2026-11-17 (haiku). The first episode held a hit, so they stay here, before the first round heading.

- hit fixed 2026-11-17 — document type rule omits the `-technical-design.md` arm decision-coverage reads; added it
- hit fixed 2026-11-17 — glossary Decision coverage says "derived by the propagation auditor", which D6 changes; named in *Who runs it* among the surfaces that change
- hit fixed 2026-11-17 — PROCEDURE "the coverage duty's hits alone" goes false under D8; named in *Who runs it*
- hit fixed 2026-11-17 — PROCEDURE "the card writes those lines on every run" goes false under D3/D6; named in *Who runs it*
- hit fixed 2026-11-17 — LEDGER "`hit held` is scoped to the coverage duty's hits" goes false under D8; named in *Who runs it*
- hit fixed 2026-11-17 — normalisation parenthetical omits marker stripping; added it
- hit dismissed 2026-11-17 — bare "check" near a Hit at glossary.md:504, :522, :533 and spec D8; counter: 504 and 522 define the generic noun the ban qualifies, 533 is the term's own definition, and D8's "checking by hand" is a verb, not the noun the ban names
- hit dismissed 2026-11-17 — launcher, propagation gate, dispatcher, table closure, integrity stamp lack glossary entries; counter: duty 5 flags a name the source does not define, and each is defined at its source — spec D4 and the CHANGELOG (launcher), the workflow rule (propagation gate, dispatcher), card duty 11 and the technical-design rule's Declared table relations (table closure), the lifecycle rule (integrity stamp); the glossary is no closed dictionary
- hit dismissed 2026-11-17 — bare `check:` label in the hit-line template; counter: it is the output field's name, a literal the script prints, not prose; settled in grilling question 1
- hit fixed 2026-11-17 — "Five more sentences" enumerated four; replaced by a general clause plus the full list the gate found
- hit fixed 2026-11-17 — D10's semicolon and parenthesis drop is not in the rule's grammar; the Table closure paragraph now says it reads more loosely on purpose and can add no hit the rule would not
- hit fixed 2026-11-17 — the rule is not "beside the script"; now "in the plugin's rules/ directory beside scripts/"
- hit fixed 2026-11-17 — nine more consumers of the changed arrangement (README ×3, propagation-duties, workflow, LEDGER ×2, integrity-auditor, glossary Hit); *Who runs it* now states the class and lists them, the plan enumerates by grep
- hit fixed 2026-11-17 — the *Who runs it* list missed 14 more sites (PROCEDURE ×2, lifecycle ×2, technical-design rule, plan-adversary card, README ×4, propagation-duties, glossary Audit agent, SETTINGS_REGISTRY, decision-coverage docstring); list replaced by the class, the surfaces it spans, and the plan's grep
- hit fixed 2026-11-17 — the D8 held hit had no reachable terminal shape; D8 now names both closing lines, a ruling-carrying `hit dismissed` being the new shape; ruling: 2026-11-17
- hit fixed 2026-11-17 — the class in *Who runs it* omitted the gate-line sentences D8 falsifies (LEDGER:240, :253-254, :307, glossary Hit); class widened to "the held kinds and the gate lines' terminal shapes"
- hit fixed 2026-11-17 — D8's `hit fixed … ruling:` misuses the ruling shape, which records a decision the document now carries; install path now the ordinary `hit fixed` without `ruling:`, the dismissal keeps it
- hit fixed 2026-11-17 — "the settings registry" holds no old-arrangement sentence; the areas list is gone
- hit fixed 2026-11-17 — command-set enumerations (marketplace.json, plugin.json, root README) go stale under D1/D5; class now names "every enumeration of the plugin's commands"
- hit fixed 2026-11-17 — the record's "13 more sites" listed 14; corrected
- hit fixed 2026-11-17 — the launcher dismissal cited README and bin/, which do not define it; counter now cites spec D4 and the CHANGELOG
- hit fixed 2026-11-17 — the launcher dismissal's counter said the technical-design rule defines "table closure"; it now cites card duty 11 and the rule's Declared table relations

### 2026-11-17 — architect, fable 5.2, concerns (round 1, full-document)

Record: `.claude/working-process/2026-11-17-document-check-spec/architect-round-1.md`.

- fixed 2026-11-17 — [Important] F1: the `integrity:` stamp check reports a state the rules call expected (stale after a licensed fix wave), so every gate ends in a dismissal; ruling: 2026-11-17; the integrity stamp is dropped from the Document checks and listed as a non-goal; D3 now names three checks
- fixed 2026-11-17 — [Important] F2: D10 leaves a name matching no Parts row unchecked while D3 takes duty 11 off the auditor, so dangling names have no owner; ruling: 2026-11-17; duty 11 stays the auditor's for the segments the script reports not checked; D3, D12 and the Table closure paragraph say so
- fixed 2026-11-17 — [Important] F3: running the scripts beside the auditor makes it read a document the script fixes then change, spending the episode's re-dispatches; ruling: 2026-11-17; D6 runs both scripts first, disposes of their hits outside the episode bound, then dispatches the auditor; *Who runs it* argues the order
- fixed 2026-11-17 — [Important] F4: D8 writes one checkout's missing interpreter into a document's ledger as a held hit with a new shape; ruling: 2026-11-17; D8 now makes a script that cannot run an ordinary error the developer decides, with nothing in the ledger, reversing the 2026-11-17 ruling's ledger shapes
- fixed 2026-11-17 — [Important] F5: on plans, backticked convention paths and placeholders make hits the author must dismiss, against D2; ruling: 2026-11-17; D9 leaves a missing backticked path not checked on every document; Named documents checks links only
- fixed 2026-11-17 — [Minor] F6: Goal 1 promised the class where D2 delivers the forms a parse settles; license: D2; Goal 1 now says "a defect of a form the Document checks settle"
- fixed 2026-11-17 — [Minor] F7: D11 runs the scripts "at the authoring-time offer", an offer that may be declined; ruling: 2026-11-17; D11 and *Who runs it* say the scripts run at the authoring-time offer whether or not it is accepted
- fixed 2026-11-17 — [Minor] F7: D11 did not say gate lines, the held batch and the bound apply without the auditor; license: D11; D11 now says so
- fixed 2026-11-17 — [Minor] F8: the card keeps duties 10 and 11 as instructions and duty 11 stricter than D10; license: D10 and D12; D12 now has each duty's first line say the auditor does not perform it and duty 11 state what D10 checks
- fixed 2026-11-17 — [Minor] F9: the glossary's Decision coverage map was "derived by the propagation auditor", false under D6; license: D6; the entry now names `wp-decision-coverage` run by the dispatcher
- signal 2026-11-17 — F1–F5 need rulings; one diff-scoped round after them earns its cost, a third is unlikely to repay itself

Gate lines from the episode before round 2, 2026-11-17 (haiku):

- hit fixed 2026-11-17 — the F2 line says D3 names the owner of the unsettled table-closure segments, and D3 did not; D3 now does
- hit dismissed 2026-11-17 — ledger lines (the episode-2 class widening, F8's "each duty's first line", the "checking by hand" counter) describe text later waves replaced; counter: a ledger line records the document as that wave left it, and the F2 and F4 rulings later in the same round superseded those words
- hit dismissed 2026-11-17 — the round-1 record's line citations (spec, PROCEDURE, glossary:597) and its size match no committed state; counter: the record is the reviewer's verbatim report against the working copy it read, which the round's own fixes then moved, and its size was measured on that copy
- hit dismissed 2026-11-17 — bare "check" beside a hit at propagation-auditor.md:181 and :350; counter: the ban predates this change (minted with **Verification check**), the lines are shipped card text this spec does not reach, and the plan's sweep of the card under D12 can take them
- hit dismissed 2026-11-17 — launcher, integrity stamp, propagation gate, dispatcher, table closure lack glossary entries; counter: re-raised without new evidence against the dismissal of the first pre-round episode
- hit fixed 2026-11-17 — "Generalising it costs one line", while the launcher names its script on two lines (path and error message); now "two lines"
- hit dismissed 2026-11-17 — six round-1 record citations are off by two to seven lines (spec 255-258, 206-208, 299-300; PROCEDURE 351, 360-361; glossary 597); counter: the record is the reviewer's report copied verbatim and never corrected; the reviewed working copy was the parent commit plus the grilling's uncommitted edits (the glossary's new entry put 587 at 597), and the off-by-two citations are the reviewer's own; the relay checked each against the files and triage acted on the located text
- hit fixed 2026-11-17 — the glossary's Document check entry ran table closure on all three classes, against D3; it now says a technical design alone
- hit fixed 2026-11-17 — "package 4" names a queue item scoped to technical designs while D1 covers three classes; the opening now says the package was widened
- hit dismissed 2026-11-17 — bare "check" at propagation-auditor.md:215 beside a hit, and the earlier counter's :350, which reads "checks"; counter: as for :181, a ban older than this change on shipped card text the plan's card sweep takes; :350 was cited in error and needs nothing
- hit dismissed 2026-11-17 — the ledger's round-1 block carries two F7 lines for one finding; counter: F7 was split, one half held and ruled, the other fixed by license, so it takes one line per disposition
- hit dismissed 2026-11-17 — re-raises of the `check:` field name, the round-1 record's citations and size, the historical ledger lines, and the glossary gaps; counter: each is disposed earlier in this ledger and the run brings no new evidence

### 2026-11-17 — architect, fable 5.2, concerns (round 2, diff-scoped)

Record: `.claude/working-process/2026-11-17-document-check-spec/architect-round-2.md`. Ordered by the developer after the gate episode before it spent its re-dispatches.

- fixed 2026-11-17 — [Important] F1: D8's "any exit other than 0" makes a document-side failure (a `spec:` naming a missing file, which `decision-coverage` exits 1 on) an environment error, regressing what the shipped card makes a fixable hit; ruling: 2026-11-17; D8 and *Who runs it* let the session fix a document-side cause the message names and re-run; otherwise the developer decides
- fixed 2026-11-17 — [Minor] F2: how long the developer's "order the dispatch without Document checks" stands is unsaid, and a deterministic crash stops every later gate; ruling: 2026-11-17; D8 says the developer's order to dispatch without Document checks holds for the session
- fixed 2026-11-17 — [Minor] F3: the script loop listed only fixed and dismissed, and D11 applied an episode bound that counts nothing without the auditor; license: the procedure's held exception for coverage hits; D6 adds "or held, which ends the episode", D11 says script re-runs are unbounded on purpose
- fixed 2026-11-17 — [Minor] F4: duty 11's remainder was defined by script output the auditor never sees; license: the card's own "a name matching no row"; D12 and *Table closure* now name the form
- fixed 2026-11-17 — [Minor] F5: D9's exemption caught a backticked `path:line`; license: *Named documents* limits it to `.md` paths; D9 now says "a backticked path carrying no line"
- fixed 2026-11-17 — [Minor] F6: *Named documents* now reads only Markdown links — 0 in the 8 live documents — and catches neither measured miss; ruling: 2026-11-17; *Named documents* is dropped as a Document check; D3 names two checks and Citations resolves link targets by D9
- fixed 2026-11-17 — [Minor] F7: "about 30 of the 70" predates dropping the stamp and backticked paths; license: the spec's own Verification; Problem says "belonged", Constraints says the script covers fewer than the 30
- fixed 2026-11-17 — [Minor] F8: the glossary's Hit entry omitted `wp-decision-coverage` as a hit source after D6; license: D6; the entry now lists it
- signal 2026-11-17 — a third round is unlikely to earn its cost; F1 needs a ruling, F2–F8 are clause-level, and the joint integrity audit at the consumption gate reads the whole body

Round 2's `concerns` is resolved without a further round: the developer settled F1, F2 and F6 on 2026-11-17, the licensed Minor fixes landed, and the reviewer's stop signal judged a third round unlikely to repay itself; the integrity audit at the consumption gate reads the whole document.


Gate lines from the episode before the integrity audit, 2026-11-17 (haiku):

- hit dismissed 2026-11-17 — the glossary states in the present tense that `wp-document-check` and `wp-decision-coverage` run, and neither has shipped; counter: the glossary edits ride on this package's branch and merge with the implementation, so no shipped state ever carries one without the other
- hit dismissed 2026-11-17 — the shipped sites carrying the old invocation and output claim (README, PROCEDURE, the card) are not named; counter: *Who runs it* defers their enumeration to the plan's grep by design, after three runs found a named list stale
- hit dismissed 2026-11-17 — launcher, dispatcher, table closure, episode, integrity stamp, propagation gate and held batch lack glossary entries; counter: re-raised without new evidence against the pre-round dismissal
- hit dismissed 2026-11-17 — the round-2 record's spec citations no longer carry the text they quote; counter: the record is the reviewer's verbatim report on the copy it read, which the round's own fixes then moved
