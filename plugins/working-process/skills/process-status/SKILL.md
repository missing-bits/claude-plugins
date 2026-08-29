---
name: process-status
description: "Report what the working process left unfinished in this repo — a pending grilling, an unresolved verdict, a re-review nobody ran, a stamp in the wrong place. Use when the developer asks what is unfinished, what the process still owes, or for a status pass over docs/specs and docs/plans."
---

# process-status — what the process left unfinished

Runs the Unfinished-work list the lifecycle rule publishes and reports
what it finds. The rule owns which classes exist; this skill owns
nothing but running them, confirming their hits, and reporting. A class
this skill has never heard of works the moment the rule publishes it.

## Step 1 — read the list

Read the `## Unfinished-work list` section of
`${CLAUDE_PLUGIN_ROOT}/rules/spec-plan-lifecycle.md` — the payload copy
shipped beside this skill, never an installed copy under
`.claude/rules/`. The plugin releases skill and payload in one version,
so that copy is always in step with this skill.

Each entry carries three legs: the class name, one command, and the
owner of the next move. Take all three. An entry may carry a fourth, its
own match scope — where in a document its hits count; take that too
whenever the entry publishes one.

The read fails, and the report says so instead of reporting a clean
repo, when the section is missing or an entry lacks one of the three
legs. A run that could not read the list must never look like a run that
found no unfinished work. A missing fourth leg fails nothing: it means
the entry keeps the default scope.

## Step 2 — run each command

Run each entry's command exactly as published, from the repository root.
Never rewrite a command, add a path, or drop a flag: a command that
differs from the published one answers a different question.

## Step 3 — confirm every hit

A command returns hits. A hit becomes a report line only when its
matching line sits where the entry says its hits count. The default
scope is the document's frontmatter block: the file's opening `---` on
line 1 and its closing `---`. An entry publishing a scope of its own
replaces that default with what it publishes, and replaces nothing else.
Read the head of the file for the default scope, and the lines above the
match for a scope naming a section.

- The line sits inside the entry's scope → the hit is real.
- The line sits anywhere else → the document quotes the convention
  instead of instantiating it. Reject the hit.
- The file has no opening `---`, or none closing it → reject every hit in
  it, whatever scope the entry publishes. A process document always
  carries frontmatter, so a file without it is no process document at
  all; a file whose frontmatter never closes is broken for every consumer
  of frontmatter, so it surfaces on its next touch rather than here. An
  entry's own scope narrows where a hit counts, never whether the file
  qualifies. Say so if asked; never invent a class for it.

## Step 4 — report

Group by document, because the developer acts on a document. Under each
document, one line per confirmed hit: the class name, the field where
the class distinguishes fields, and the owner the entry carries. Read
the owner from the entry — never supply one from your own knowledge of
the process.

Misplaced stamp suppresses per field: it hides the one other class whose
published command would match the relocated line — itself excluded,
since its own command matches every process field. Match semantics are
the mapping, so you never need process knowledge to find it and a class
published later works the same way. Name the field on the line, so the
developer can see which class went quiet.

Close the report with:

- the rejected hits — how many, and in which documents — because
  over-rejection is the only way confirmation can quietly eat real
  unfinished work;
- what was checked: every class name from the list, so a clean run is a
  statement and never silence;
- one question, whether to take anything from the list.

Fire no offer yourself. Each class names its owner, and those owners
have their own gates; a second trigger for one of them belongs to
nobody.

## Out of scope

The Project memory store, documents merely in flight (`draft` or
`approved` with no further move), and any criterion this skill invents.
A new class of unfinished work arrives by being published on the list.
