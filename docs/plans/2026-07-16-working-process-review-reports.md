---
ticket: none
date: 2026-07-16
status: approved
adversary: LGTM
spec: ../specs/2026-07-16-working-process-review-reports-design.md
---

# Working-process 0.5.0 — Review-reports Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the shared review-report contract as a new rule in the working-process Rules payload, extend the two rules it touches, and release the plugin as 0.5.0 (spec: `docs/specs/2026-07-16-working-process-review-reports-design.md`).

**Architecture:** Payload-only release. Three rule-file changes in `plugins/working-process/rules/` — one new file (`review-reports.md`, the domain-agnostic report contract with its contract probe), two edits (`process-artifacts.md` gains `docs/code-review/` and the tightened mode-signal wording; `ticket-frontmatter.md` names the review-report field set) — plus README and version bump. No engine, skill, agent, or hook changes: the existing Rules engine distributes the delta through drift detection and sync-rules classification.

**Tech Stack:** Markdown (Claude Code rules), YAML frontmatter, POSIX sh (verification fixtures only), `claude` CLI.

## Global Constraints

- **Sequencing:** working-process 0.5.0 ships BEFORE python-standards 0.1.0 — the companion spec declares `working-process ≥ 0.5.0` as its assumed convention range. Nothing in this plan touches python-standards content.
- Public-repo hygiene: all committed text is English; no company or client names; no machine-specific paths (`/home/<user>/…`) — this plan's test commands use `$HOME` and `mktemp` for that reason.
- YAML frontmatter scalars containing `: ` (colon+space) are quoted. `claude plugin validate` does NOT check `rules/`, so rule frontmatter is additionally reviewed by hand in every task that writes one.
- Any change under `plugins/working-process/` bumps the plugin version in the same commit — this branch bumps `0.4.0 → 0.5.0` in Task 1 and keeps it.
- Conventional Commits 1.0.0, single subject line, no body, no trailers.
- Glossary terms bind all committed wording (`docs/domain/glossary.md`): Contract probe, Review report, Standards plugin, Standalone install, Ignored mode, Tracked mode, First-create question, Rules payload, Rules engine, Drift. Respect every `_Avoid_` ban — no "artifact folder", "self-ignore", unqualified "probe" or "discovery" (for the contract probe), "review output", "report file", "standards stack", "solo install", "rules plugin", "outdated rules".
- Plugin identity is untouched: `plugin.json` description, the marketplace catalog entry, and the repo-root README table row all stay as they are (marketplace-sync rule not triggered).
- Minimum verified platform stays Claude Code 2.1.207; no Requirements change.

---

### Task 1: New rule `review-reports.md` + version bump to 0.5.0

**Files:**
- Create: `plugins/working-process/rules/review-reports.md`
- Modify: `plugins/working-process/.claude-plugin/plugin.json` (version only)
- Modify: `docs/specs/2026-07-16-working-process-review-reports-design.md` (frontmatter: `branch`/`base`)
- Modify: `docs/plans/2026-07-16-working-process-review-reports.md` (frontmatter: `branch`/`base`)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the fifth payload file. Its contract-probe path pair (`<project>/.claude/rules/working-process/review-reports.md`, then `$HOME/.claude/rules/working-process/review-reports.md`) and its canonical filename command are verified byte-for-byte by Task 4. Task 2's `ticket-frontmatter.md` edit references this rule's frontmatter field names (`date`, `mode`, `ticket`, `scope`, `runid`, `standards`, `rerun-of`, `findings`) — they must match exactly.

- [ ] **Step 1: Cut the topic branch and stamp it into the process frontmatter**

```bash
git checkout -b feature/review-reports
```

Then, with the Edit tool, add to the frontmatter of BOTH `docs/specs/2026-07-16-working-process-review-reports-design.md` and this plan (below the `status:`/`spec:` lines):

```yaml
branch: feature/review-reports
base: feature/python-standards
```

(`base` is the branch the checkout above was cut from; if the spec docs were merged to `master` before execution starts, cut from `master` and write `base: master` instead. Either way: NO python-standards plugin content may land on the base branch before this release merges — the merge carries the base's ancestry to `master`, and 0.5.0 ships BEFORE python-standards 0.1.0.) Commit:

```bash
git add docs/specs/2026-07-16-working-process-review-reports-design.md docs/plans/2026-07-16-working-process-review-reports.md
git commit -m "docs: stamp review-reports topic branch into spec and plan frontmatter"
```

- [ ] **Step 2: Write `plugins/working-process/rules/review-reports.md`** (exactly this content)

`````markdown
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
`````

- [ ] **Step 3: Hand-review the frontmatter and verify it parses**

`claude plugin validate` does not check `rules/` — read the file's opening block yourself and confirm the only frontmatter key is `paths:` with the quoted glob, and that no unquoted scalar in it contains `: `. Then:

```bash
python3 -c "
import re
t = open('plugins/working-process/rules/review-reports.md').read()
m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
assert m and '\"docs/code-review/**\"' in m.group(1), 'paths frontmatter wrong'
print('frontmatter OK')
"
```

Expected: `frontmatter OK`.

- [ ] **Step 4: Test the canonical filename command**

```bash
OUT=$(printf '%s-%s\n' "$(date +%Y-%m-%d-%H%M%S)" "$(head -c 4 /dev/urandom | od -An -tx1 | tr -d ' \n')")
echo "$OUT" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{6}-[0-9a-f]{8}$' && echo FILENAME-CMD-OK
```

Expected: `FILENAME-CMD-OK` — 17-char timestamp, dash, 8 hex chars, exactly as the rule's Filename section states.

- [ ] **Step 5: Bump the plugin version**

In `plugins/working-process/.claude-plugin/plugin.json` change `"version": "0.4.0"` to `"version": "0.5.0"` (description and everything else unchanged). Run:

```bash
claude plugin validate . && claude plugin validate plugins/working-process
```

Expected: both pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/working-process/rules/review-reports.md plugins/working-process/.claude-plugin/plugin.json
git commit -m "feat(working-process): add review-reports rule, bump to 0.5.0"
```

---

### Task 2: Extend `process-artifacts.md` and `ticket-frontmatter.md`

**Files:**
- Modify: `plugins/working-process/rules/process-artifacts.md`
- Modify: `plugins/working-process/rules/ticket-frontmatter.md`

**Interfaces:**
- Consumes: the review-reports frontmatter field names from Task 1 (`date`, `mode`, `ticket`, `scope`, `runid`, `standards`, `rerun-of`, `findings`).
- Produces: `process-artifacts.md` whose `paths:` includes `"docs/code-review/**"` and whose mode-signal wording is the disambiguated form Task 4 verifies against the glossary; `ticket-frontmatter.md` whose field-set list names review reports.

- [ ] **Step 1: Rewrite `plugins/working-process/rules/process-artifacts.md`** (exactly this content — the `paths:` entry, the directory list, the Tracked-mode bullet, and the never-ask paragraph change; "Handling artifacts" is untouched)

```markdown
---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
  - "docs/domain/**"
  - "docs/code-review/**"
  - ".superpowers/**"
---

# Process directories and artifacts

A Process directory is a directory the working process creates in a
project repo to hold work artifacts: `docs/specs/`, `docs/plans/`,
`docs/domain/`, `docs/code-review/`, and the `.superpowers/` family at
the repo root.

## First-create question

When creating a Process directory — or touching one that already exists
with no observable prior decision (neither a `.gitignore` containing
exactly `*` nor any git-tracked file under it) — ASK the developer which
mode the directory gets. Assume no default:

- **Ignored mode**: write a `.gitignore` containing exactly `*` into the
  directory; its contents stay out of the repo.
- **Tracked mode**: artifacts are committed like any other file; no
  `.gitignore` is written at first-create (a narrower one added later —
  e.g. the local pocket of `docs/code-review/` — does not change the
  mode).

Never ask when either signal is already present: only a `.gitignore`
containing exactly `*` means ignored mode was chosen — one with any
other content (e.g. a local pocket's `local-*`) signals nothing by
itself; a git-tracked file under the directory (`git ls-files <dir>`
non-empty) means tracked mode was chosen.

## Handling artifacts

- Tracked mode: artifact updates ride along with the commits of the work
  they belong to — never leave them dirty. Committing stays with the
  developer.
- Never force-add an artifact into version control and never suggest
  removing an existing ignore.
- Edit artifact files (progress ledgers, the domain glossary, ADRs) with
  the Edit tool, not shell one-liners — `sed -i`/`printf >>` commands
  with unique text never match a standing permission rule and prompt on
  every call.
- Per-work artifacts (review reports, ADRs, task briefs, progress
  ledgers) carry a `ticket` frontmatter field; registry files that live
  across tickets (the domain glossary, `.gitignore` files) are exempt.
  Reuse the ticket already established for the current work; value format
  in the ticket-frontmatter rule.
```

- [ ] **Step 2: Rewrite `plugins/working-process/rules/ticket-frontmatter.md`** (exactly this content — only the Field sets list changes: a review-reports entry lands between the specs-and-plans and every-other-document entries)

```markdown
---
paths:
  - "docs/**"
---

# Ticket frontmatter

Documents under `docs/` open with a YAML frontmatter block linking them
to the issue tracker. The convention is tracker-agnostic — Jira, GitHub,
GitLab, or anything else; the field is always `ticket`.

## Field sets

- Specs and plans (`docs/specs/`, `docs/plans/`): `ticket` + `date` +
  `status` + the process and branch fields — details in the
  spec-plan-lifecycle rule.
- Review reports (`docs/code-review/`): the review-reports rule's
  frontmatter set — `date`, `mode`, `ticket`, `scope`, `runid`,
  `standards`, optional `rerun-of`, `findings` — not the bare
  `ticket`-only set of `.superpowers/**` artifacts.
- Every other document under `docs/`: `ticket` + `date`.
- Per-work process artifacts (`.superpowers/**`, ADRs): `ticket` only —
  see the process-artifacts rule.

## Values

- `ticket`: the tracker's short reference, never a URL — a Jira key
  (`ABC-123`), a GitHub/GitLab issue reference (`#123` or
  `org/repo#123`), or the project tracker's equivalent. Several tickets
  use the inline list form `[ABC-123, ABC-456]` — one greppable line,
  never a multi-line dash list. No ticket means an explicit
  `ticket: none`; the field is always present.
- `date`: the ISO creation date (`2026-07-13`).

## Sourcing and backfill

For a NEW document: branch name (`feature/ABC-123-...`) → conversation
context → ask the developer once; no answer means `none`. Never ask twice
for one unit of work — a plan inherits its spec's ticket, and artifacts
of the same session reuse the established value.

When editing an existing `docs/` document that has no frontmatter, add
the block as part of the edit — sourced from document content → branch →
conversation → `none`, never a question (asking is reserved for new
documents). `date` is the file's git creation date:
`git log --follow --format=%as -- <file> | tail -1`.

## Finding documents by ticket

The `ticket:` line matches both single-reference and inline-list forms;
`--no-ignore` reaches ignored-mode artifacts:
`rg -l --no-ignore '^ticket:.*ABC-123' docs/ .superpowers/`
```

- [ ] **Step 3: Hand-review both frontmatter blocks and verify the payload counts five files**

Read both opening blocks yourself (only `paths:` keys, quoted globs, no unquoted `: ` in scalars — validate does not check `rules/`). Then:

```bash
python3 -c "
import re
checks = {
  'plugins/working-process/rules/process-artifacts.md': '\"docs/code-review/**\"',
  'plugins/working-process/rules/ticket-frontmatter.md': '\"docs/**\"',
}
for p, needle in checks.items():
    t = open(p).read()
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    assert m and needle in m.group(1), p
    print(p, 'OK')
"
plugins/working-process/scripts/ruleset-hash.sh --list plugins/working-process/rules | wc -l
```

Expected: both `OK`; the count is `5`.

- [ ] **Step 4: Commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/process-artifacts.md plugins/working-process/rules/ticket-frontmatter.md
git commit -m "feat(working-process): extend process-artifacts and ticket-frontmatter for review reports"
```

---

### Task 3: Plugin README — five rules, `docs/code-review/` directory

**Files:**
- Modify: `plugins/working-process/README.md` (the "Process rules" opening paragraph and the "Process directories" section; nothing else)

**Interfaces:**
- Consumes: the rule and directory names from Tasks 1–2.
- Produces: README consistent with the shipped payload. The repo-root README table row, the catalog entry, and the `plugin.json` description are deliberately NOT touched (identity unchanged — see Global Constraints).

- [ ] **Step 1: Replace the "Process rules" opening paragraph**

In `plugins/working-process/README.md`, replace this paragraph:

```markdown
The plugin ships four rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, and ticket frontmatter. Claude Code does
not load plugin rules by itself: install them with the
`working-process:sync-rules` skill.
```

with:

```markdown
The plugin ships five rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, ticket frontmatter, and the
review-report contract (`review-reports.md`: where a code-review run
writes its Review report and what shape it takes; domain review skills
locate the installed contract via its contract probe — the
project-level then user-level install path, in that order). Claude
Code does not load plugin rules by itself: install them with the
`working-process:sync-rules` skill.
```

- [ ] **Step 2: Replace the "Process directories" section body**

Replace this paragraph:

```markdown
The one directory this plugin creates in a project repo is
`docs/domain/` (glossary + ADRs). On first creation the developer is
asked whether it should be git-ignored (a `.gitignore` containing `*`)
or committed; an existing directory's state is respected without asking.
```

with:

```markdown
This plugin creates two directories in a project repo: `docs/domain/`
(glossary + ADRs) and `docs/code-review/` (Review reports — one per
code-review run, shape defined by the review-reports rule). On first
creation the developer is asked whether the directory should be
git-ignored (a `.gitignore` containing exactly `*`) or committed; an
existing directory's state is respected without asking. A tracked-mode
`docs/code-review/` additionally carries a `.gitignore` with `local-*`
— the local pocket for reports the developer keeps out of git.
```

- [ ] **Step 3: Validate and commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/README.md
git commit -m "docs(working-process): document review-reports rule and code-review directory"
```

---

### Task 4: End-to-end verification + spec/plan closure

**Files:**
- Modify: `docs/specs/2026-07-16-working-process-review-reports-design.md` (status → implemented)
- Modify: `docs/plans/2026-07-16-working-process-review-reports.md` (status → implemented)

**Interfaces:**
- Consumes: everything above; the existing engine scripts `plugins/working-process/scripts/ruleset-hash.sh`, `write-manifest.sh`, `check-rules-drift.sh` by their released CLIs (unchanged by this plan).
- Produces: verified behavior per the spec's Verification section; closed process frontmatter; committed docs. After this task the release is ready to merge — and MUST land before any python-standards 0.1.0 work that consumes the contract.

- [ ] **Step 1: Validate and confirm the payload aggregate changed against the released baseline**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
T=$(mktemp -d)
git archive master plugins/working-process/rules | tar -x -C "$T"
OLD=$(plugins/working-process/scripts/ruleset-hash.sh "$T/plugins/working-process/rules")
NEW=$(plugins/working-process/scripts/ruleset-hash.sh plugins/working-process/rules)
echo "old=$OLD"; echo "new=$NEW"
[ "$OLD" != "$NEW" ] && echo HASH-CHANGED
rm -rf "$T"
```

Expected: both validations pass; two distinct `sha256:` values; `HASH-CHANGED`. (`master` carries the 0.4.0 payload — the released baseline. If 0.5.0 was already merged when re-running this, diff against the pre-release commit instead.)

- [ ] **Step 2: Drift-hook nudge on a 0.4.0-state install, then silence after sync**

Simulates a machine with the 0.4.0 rules installed at user level, then a completed sync:

```bash
P=$(pwd)/plugins/working-process
T=$(mktemp -d)
git archive master plugins/working-process/rules | tar -x -C "$T/"
OLDRULES="$T/plugins/working-process/rules"
TGT="$T/.claude/rules/working-process"; mkdir -p "$TGT"
cp "$OLDRULES"/*.md "$TGT/"
"$P/scripts/ruleset-hash.sh" --list "$OLDRULES" | \
  "$P/scripts/write-manifest.sh" "$TGT/.manifest.json" \
  working-process missing-bits 0.4.0 "$("$P/scripts/ruleset-hash.sh" "$OLDRULES")"
cd "$T"
# a) drifted: expect one JSON nudge naming working-process:sync-rules
HOME="$T" CLAUDE_PLUGIN_ROOT="$P" "$P/scripts/check-rules-drift.sh"
# b) sync-equivalent: copy current rules, rewrite manifest at 0.5.0 → silence
cp "$P/rules/"*.md "$TGT/"
"$P/scripts/ruleset-hash.sh" --list "$P/rules" | \
  "$P/scripts/write-manifest.sh" "$TGT/.manifest.json" \
  working-process missing-bits 0.5.0 "$("$P/scripts/ruleset-hash.sh" "$P/rules")"
OUT=$(HOME="$T" CLAUDE_PLUGIN_ROOT="$P" "$P/scripts/check-rules-drift.sh"); echo "rc=$? out=[$OUT]"
cd - >/dev/null; rm -rf "$T"
```

Expected: (a) one JSON line whose `additionalContext` contains `working-process:sync-rules` (the manifest's 0.4.0 is not newer than the local 0.5.0, so the drift wording wins, not the plugin-update direction); (b) `rc=0 out=[]`.

- [ ] **Step 3: sync-rules update classification — install row and auto-update rows (scripted hash evidence)**

Rebuild the same drifted state (self-contained — run from the repo root) and show the three hash sources the classifier reads:

```bash
P=$(pwd)/plugins/working-process
T=$(mktemp -d)
git archive master plugins/working-process/rules | tar -x -C "$T/"
OLDRULES="$T/plugins/working-process/rules"
TGT="$T/.claude/rules/working-process"; mkdir -p "$TGT"
cp "$OLDRULES"/*.md "$TGT/"
"$P/scripts/ruleset-hash.sh" --list "$OLDRULES" | \
  "$P/scripts/write-manifest.sh" "$TGT/.manifest.json" \
  working-process missing-bits 0.4.0 "$("$P/scripts/ruleset-hash.sh" "$OLDRULES")"
S=$("$P/scripts/ruleset-hash.sh" --list "$P/rules")     # shipped
C=$("$P/scripts/ruleset-hash.sh" --list "$TGT")          # current on disk
# review-reports.md: shipped only → install row
echo "$S" | grep -q '^review-reports\.md' && ! echo "$C" | grep -q '^review-reports\.md' && echo INSTALL-ROW
# process-artifacts.md and ticket-frontmatter.md: shipped differs, current == pristine → auto-update rows
for f in process-artifacts.md ticket-frontmatter.md; do
  SH=$(echo "$S" | grep "^$f" | cut -f2)
  CH=$(echo "$C" | grep "^$f" | cut -f2)
  PH=$(sed -n "s/.*\"$f\": { \"hash\": \"\([^\"]*\)\".*/\1/p" "$TGT/.manifest.json")
  [ "$SH" != "$PH" ] && [ "$CH" = "$PH" ] && echo "AUTO-UPDATE-ROW $f"
done
# workflow.md and spec-plan-lifecycle.md: untouched → silent rows
for f in workflow.md spec-plan-lifecycle.md; do
  SH=$(echo "$S" | grep "^$f" | cut -f2)
  PH=$(sed -n "s/.*\"$f\": { \"hash\": \"\([^\"]*\)\".*/\1/p" "$TGT/.manifest.json")
  [ "$SH" = "$PH" ] && echo "SILENT-ROW $f"
done
rm -rf "$T"
```

Expected: `INSTALL-ROW`, `AUTO-UPDATE-ROW process-artifacts.md`, `AUTO-UPDATE-ROW ticket-frontmatter.md`, `SILENT-ROW workflow.md`, `SILENT-ROW spec-plan-lifecycle.md` — exactly the spec's classification (install row for the new rule, auto-update rows absent local edits).

- [ ] **Step 4: Contract probe path resolution in both install scopes**

The contract-probe paths written in the rule must match the Rules engine's install layout (`<target>/.claude/rules/working-process/`) byte-for-byte in both scopes:

```bash
P=$(pwd)/plugins/working-process
grep -c '\.claude/rules/working-process/review-reports\.md' "$P/rules/review-reports.md"
# Mechanical tie to the engine's layout definition (not prose-reading):
# the engine's SKILL.md must still define the target as the rules
# directory itself and the payload namespace as <target>/<plugin-name>/ —
# the composition of those tokens with the plugin name "working-process"
# IS the probe path pair.
grep -c '\$HOME/.claude/rules/' "$P/skills/sync-rules/SKILL.md"
grep -c '<target>/<plugin-name>/' "$P/skills/sync-rules/SKILL.md"
```

Expected: the first grep prints `2` (the project-level and user-level path literals in the rule, no third variant); the two engine greps print non-zero — if either prints `0`, the engine's layout definition moved and the rule's probe paths MUST be re-derived before shipping (the glossary forbids independent drift). Also confirm by reading the rule's Contract probe section that path 1 is the `<project>` form and path 2 the `$HOME` form — project first, mirroring the engine's project-over-user conflict rule.

- [ ] **Step 5: Live check — plugin update, sync-rules run, rule loading** (interactive, driven by the developer)

PRECONDITION: the installed `working-process` plugin must source THIS
checkout with the 0.5.0 content — a marketplace added from the local
repo path, on this topic branch. A GitHub- or mirror-sourced install
fetches the released (pre-merge: 0.4.0) content and step 1's drift
nudge silently never fires — that is a broken precondition, not a
passing check. When the local-checkout setup is unavailable, run this
whole step POST-merge instead, before python-standards implementation
starts (the sequencing reminder below still holds).

1. `claude plugin update working-process` → the next session's start note nudges that installed rules differ (Drift).
2. Run the `working-process:sync-rules` skill → the update classifies `review-reports.md` as an install and `process-artifacts.md` + `ticket-frontmatter.md` as auto-updates (absent local edits; batched into one confirmation on a project-level tracked-mode target). After it finishes, the next session start is silent, and the synced file exists at the exact user-level probe path: `[ -f "$HOME/.claude/rules/working-process/review-reports.md" ]`.
3. In a throwaway project with the rules installed, touch a file under `docs/code-review/` and ask the session: "Which rules about docs/code-review are loaded? Does your context include a review-report contract and a Process-directory rule naming docs/code-review/?" → yes for both (the extended `process-artifacts.md` and the new `review-reports.md` — both carry `docs/code-review/**` in `paths:`).

- [ ] **Step 6: Close the process frontmatter and commit docs**

With the Edit tool:
- In `docs/specs/2026-07-16-working-process-review-reports-design.md`: `status: approved` → `status: implemented`.
- In this plan: `status: draft` (or the value current at that point) → `status: implemented`.

```bash
git add docs/specs/2026-07-16-working-process-review-reports-design.md docs/plans/2026-07-16-working-process-review-reports.md
git commit -m "docs: record review-reports spec and plan as implemented"
```

Sequencing reminder at hand-off: merge/ship this release (working-process 0.5.0) BEFORE starting python-standards 0.1.0 implementation — that plugin declares `working-process ≥ 0.5.0` and its review skill's contract probe expects this rule installable.

Coexistence note: review stacks authored before this contract may still write reports to their own historical locations; they migrate to `docs/code-review/` on their own release cycle, and until then a machine may legitimately carry two report locations. The contract binds writers to `docs/code-review/` — it does not retroactively relocate anything.

## Adversary findings — 2026-07-16 round 1

- **Important**: the Task 4 Step 5 live check could run pre-merge against
  a remote/mirror-sourced install, where the drift nudge silently never
  fires. → Fixed: explicit PRECONDITION (local-checkout marketplace on
  the topic branch) with a post-merge fallback timing.
- **Important**: the probe-path/engine-layout equivalence was asserted,
  not checked — the Step 4 fixture proved only that `cp` works. → Fixed:
  mechanical greps tie the rule's path literals to the engine SKILL.md's
  layout tokens, and Step 5(2) asserts the synced file at the exact
  user-level probe path.
- **Minor**: the spec's "unchanged except the components table" clause
  had no referent. → Fixed at source: the spec now says the catalog
  entry and repo-root README row are unchanged and names the plugin
  README's components documentation as the only identity-adjacent
  change (authoring ambiguity, not a dropped deliverable).
- **Minor**: cutting the topic branch from an unmerged base could carry
  python-standards content into master through this merge. → Fixed:
  Task 1 forbids python-standards plugin content on the base branch
  before 0.5.0 merges.
- **Minor**: review stacks predating the contract (writing to historical
  locations) were unenumerated. → Fixed: coexistence note at hand-off —
  they migrate on their own release cycle; the contract does not
  retroactively relocate reports.

Round 2 (confirmation pass): all five dispositions verified resolved —
the layout-tie greps confirmed against the real engine SKILL.md, the
precondition consistent with the merge-readiness interface, the spec
clause fixed at source. No new findings. Verdict: LGTM.
