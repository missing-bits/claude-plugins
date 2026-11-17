---
name: review-loop
description: "The dispatcher's procedure for the working process's review loop, and the grammar of the disposition ledger. Invoke before dispatching a verdict agent (architect, plan-adversary), at a consumption gate (before plan-writing or implementation), before a status move on a design spec, technical design or plan, and before writing a ledger line under a document's Review rounds section — the first time in a conversation, and again after a compaction. Instructions only: it dispatches no agent and runs no round."
---

# review-loop — the dispatcher's procedure and the ledger

This skill carries instructions and nothing else. It dispatches no
agent and runs no round. Read the reference your moment needs, whole,
before you act:

| You are about to… | Read |
|---|---|
| dispatch a verdict agent | `PROCEDURE.md`, then `LEDGER.md` |
| pass a consumption gate | `PROCEDURE.md`, then `LEDGER.md` |
| move a `status` | `PROCEDURE.md` |
| write a ledger line | `LEDGER.md` |

- `${CLAUDE_PLUGIN_ROOT}/skills/review-loop/PROCEDURE.md` — dispatching
  a verdict agent, the review loop, the stand-in and the provisional
  batch, the propagation gate, re-dispatch briefs, the terminators, what
  a diff-scoped LGTM certifies, the audit pair at the consumption gate,
  and per-round commits on a document branch.
- `${CLAUDE_PLUGIN_ROOT}/skills/review-loop/LEDGER.md` — the disposition
  ledger under `## Review rounds`: round headings, disposition lines,
  gate lines.

After a compaction this body returns and the references do not. Invoke
the skill again at the next of the four moments and re-read what it
routes to.

A reviewer or an auditor no longer receives the ledger grammar with the
document it reads. When you dispatch any agent on a document that
carries a `## Review rounds` section, give its brief the absolute path
of `LEDGER.md` and ask it to read that file first.

The four moments are listed in three places — the workflow rule's
pointer sentence, this skill's description, and the table above — and
the three are edited together.
