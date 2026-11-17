# process-status — the Unfinished-work list

## Unfinished-work list

One entry per class of unfinished process work: the class name, its
command, and the owner of the next move, plus its own match scope where
the entry re-scopes one. This section is the list — a
command published elsewhere, such as the ticket sweep in the
ticket-frontmatter rule, is a lookup and not part of it. The
`process-status` skill, when available, runs exactly what stands here,
and this heading is the name it keys on: the heading and the skill move
together or not at all.

A command returns hits, not Findings. A hit counts only when the
matching line sits inside the document's frontmatter block — between the
`---` on the file's first line and the `---` that closes it, never a
later pair — because a document quoting this convention in its body
describes it rather than instantiating it. That guard is the default. An
entry re-scopes it only by publishing its own match scope as a fourth
leg, and the entries below that do so say it there.

- **Grilling pending** — a session's outcomes are recorded and not yet
  applied.
  `rg -l --no-ignore --crlf '^\s*grilled: grilling' docs/`
  Owner: the grilling-session, when available.
- **Unresolved verdict** — a round ended in `concerns` or `blocking`
  and nothing closed it.
  `rg -l --no-ignore --crlf '^\s*(architect|adversary): (blocking|concerns)$' docs/`
  Owner: a fresh round at the prescribed tier, or the resolution
  annotation the spec-plan-lifecycle rule defines — except on a plan whose latest round heading is
  diff-scoped, whatever its verdict, where the confirming full-document
  round closes the verdict and the annotation may not, since a plan's
  loop closes only on a full-document round. Such a plan matches Chain
  debt as well where that heading is an `LGTM`: one debt seen from two
  sides, both extinguished by that round, and the duplicate is
  deliberate. On a plan already at `status: implemented` the round is
  discharged by recorded decline without any dispatch, as the Chain debt
  leg discharges its own debt — a session derives that decline under a
  `concerns` heading, while a `blocking` one waits for the developer's
  adjudication, which is theirs to make.
- **Unfinished review-loop ledger** — a disposition line or a held gate
  line nobody closed: an `open` line whose remediation never ran, or a
  `held` or `hit held` line whose question still waits. A gate line's
  date stands between its token and its dash, so the command takes an
  alternative rather than a third token inside the group.
  `rg -n --no-ignore --crlf '^- (open|held) —|^- hit held ' docs/`
  Scope: a hit counts only inside a `## Review rounds` section — this
  entry's own re-scoping of the guard above, kept for the same reason,
  since a document quoting the grammar describes it rather than
  instantiating it. Confirming section membership needs line positions,
  which is why this command carries `-n` where the others carry `-l`.
  Owner: an `open` line belongs to the document's next touch, which
  re-offers the remediation; a `held` or `hit held` line belongs to the
  developer.
- **Chain debt** — a diff-scoped `LGTM` heading carrying no record that
  what it owed was discharged.
  `rg -n --no-ignore --crlf '^### .*LGTM \(round [0-9]+, diff-scoped\)$' docs/`
  Scope: a hit counts only inside a `## Review rounds` section — the
  second entry to re-scope the default guard, for the reason the first
  one does, and carrying `-n` for the same reason.
  Owner: for a judged document, the consumption gate's pair offer; for a
  plan, the
  confirming full-document round. On a document already at
  `status: implemented` the debt is discharged by recorded decline
  without any dispatch: completed work is not re-reviewed, so the
  annotation is written citing that standing decision, and a document
  still in flight keeps the pair offer.
- **Pending re-review** — a verdict produced below the prescribed tier,
  neither refreshed nor waived.
  `rg -l --no-ignore --crlf '^\s*(architect|adversary)-fallback: [a-z0-9-]+ \((degraded|chosen) [0-9-]+\)$' docs/`
  Owner: the re-review offer at the document's consumption gate.
- **Misplaced stamp** — a process field outside the top level of the
  frontmatter, at any value.
  `rg -l --no-ignore --crlf '^\s+(grilled|architect|adversary|architect-fallback|adversary-fallback|integrity):' docs/`
  Owner: the developer; no process surface owns moving a stamp back.
  The class suppresses per field: it hides any other class whose
  published command would match the relocated line — at most one, and
  for a field no other command names, such as `integrity`, none —
  itself excluded, since its own command matches every process field.
  Match semantics are the mapping, so a class published later needs no
  extra rule.

The tail anchors are exact on purpose: a `(resolved <date>)`,
`(adjudicated <date>)` or `, waived <date>` annotation defeats the
match, and that defeat is the recorded closed state. The leading
anchors are tolerant on purpose, so a relocated field is still found.
The Misplaced stamp command anchors `^\s+` instead, because there the
indentation is the defect it looks for rather than an accident to
tolerate. Those anchors sit on a frontmatter field wherever the default
guard holds. An entry publishing its own scope anchors a body line
instead — a leading disposition token or a round heading — and there the
close is a rewrite or an appended annotation: `open` or `held` becomes
`fixed <date>` or `declined <date>`, and a discharged chain debt gains
`, debt discharged <date>`. Either way the anchor stops matching.
