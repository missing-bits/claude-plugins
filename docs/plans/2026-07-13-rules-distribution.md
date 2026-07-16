---
ticket: none
date: 2026-07-13
status: implemented
adversary: concerns (resolved 2026-07-16)
branch: feature/process-rules
base: master
spec: ../specs/2026-07-13-rules-distribution-design.md
---

# Rules Distribution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> **Adversary resolution (2026-07-16):** the 2026-07-13 round's findings predate the convention of recording them in the document, so they are not listed here. They were resolved during implementation — see `fix(working-process)` commits pinning `rulesetHash` to the source rules directory and ignoring the contextual enabled flag for user-level foreign sources.

**Goal:** Ship the working-process plugin's rule files and the engine that installs, updates, and uninstalls them (spec: `docs/specs/2026-07-13-rules-distribution-design.md`).

**Architecture:** Copy + manifest, engine + payload. The plugin carries four rule files as inert data in `rules/`; a `sync-rules` skill copies them into `~/.claude/rules/<plugin>/` or `<project>/.claude/rules/<plugin>/` next to a `.manifest.json`; a SessionStart hook compares content hashes and nudges on drift. Three POSIX sh scripts are the deterministic core: aggregate/per-file hashing, the single manifest writer, and the hook entry point.

**Tech Stack:** Markdown (Claude Code rules, skill), POSIX sh, `sha256sum`/`shasum`, `jq` (optional, foreign payloads only), `claude` CLI.

## Global Constraints

- All committed text is English; no company or client names; no machine-specific paths (`/home/<user>/…`) in committed files — this plan's test commands use `$HOME` and `mktemp` for that reason.
- All rule/skill content is written from scratch for this plugin; the only sources are the spec and this plan.
- YAML frontmatter scalars containing `: ` (colon+space) are quoted — `claude plugin validate` does NOT check `rules/`, so an unquoted scalar fails silently.
- Any change under `plugins/working-process/` bumps the plugin version in the same commit — this branch bumps to `0.2.0` in Task 1 and keeps it.
- Conventional Commits 1.0.0, single subject line, no body, no trailers.
- Hash prefix everywhere is `sha256:` followed by 64 lowercase hex chars.
- The hook never fails a session: every branch of `check-rules-drift.sh` ends in silence and `exit 0`.
- Minimum verified platform: Claude Code 2.1.207.

---

### Task 1: `ruleset-hash.sh` + version bump to 0.2.0

**Files:**
- Create: `plugins/working-process/scripts/ruleset-hash.sh`
- Modify: `plugins/working-process/.claude-plugin/plugin.json` (version only)

**Interfaces:**
- Consumes: nothing.
- Produces: `ruleset-hash.sh <rules-dir>` → prints one line `sha256:<64 hex>` (aggregate of the directory's top-level `*.md` files, LC_ALL=C order, filenames relative — machine-independent). `ruleset-hash.sh --list <rules-dir>` → per file, one line `<name>\tsha256:<64 hex>` (tab-separated). Exit 1 on missing/invalid dir. Tasks 5 and 6 call both forms.

- [ ] **Step 1: Write the script**

```sh
#!/bin/sh
# Content hash of a rules directory: aggregate (default) or per-file --list.
# Aggregate = sha256 over the LC_ALL=C-sorted per-file hash listing with
# paths relative to the directory, so hashes compare equal across machines.
set -u

mode=hash
if [ "${1:-}" = "--list" ]; then
  mode=list
  shift
fi
dir=${1:?usage: ruleset-hash.sh [--list] <rules-dir>}
[ -d "$dir" ] || exit 1
cd "$dir" || exit 1

if command -v sha256sum >/dev/null 2>&1; then
  do_hash() { sha256sum "$@"; }
else
  do_hash() { shasum -a 256 "$@"; }
fi
# Refuse to run with a broken hash tool: a degenerate result would look
# like permanent drift to every consumer.
printf '' | do_hash >/dev/null 2>&1 || exit 1

listing=$(
  for f in *.md; do
    [ -f "$f" ] || continue
    do_hash "$f"
  done | LC_ALL=C sort -k 2
)

if [ "$mode" = "list" ]; then
  [ -n "$listing" ] || exit 0
  printf '%s\n' "$listing" | while read -r h f; do
    printf '%s\tsha256:%s\n' "$f" "$h"
  done
  exit 0
fi

agg=$(printf '%s\n' "$listing" | do_hash | cut -d ' ' -f 1)
[ -n "$agg" ] || exit 1
printf 'sha256:%s\n' "$agg"
```

Save with `chmod +x plugins/working-process/scripts/ruleset-hash.sh`.

Note: in the aggregate branch, `do_hash` reads stdin (no file arguments) — both `sha256sum` and `shasum -a 256` hash stdin when called without operands.

- [ ] **Step 2: Test determinism, ordering, drift sensitivity, --list**

```bash
T=$(mktemp -d)
printf 'alpha\n' > "$T/a.md"; printf 'beta\n' > "$T/b.md"; printf 'junk' > "$T/.manifest.json"
H1=$(plugins/working-process/scripts/ruleset-hash.sh "$T")
H2=$(plugins/working-process/scripts/ruleset-hash.sh "$T")
echo "$H1" | grep -Eq '^sha256:[0-9a-f]{64}$' && [ "$H1" = "$H2" ] && echo DETERMINISTIC
printf 'gamma\n' >> "$T/b.md"
H3=$(plugins/working-process/scripts/ruleset-hash.sh "$T")
[ "$H1" != "$H3" ] && echo DRIFT-SENSITIVE
plugins/working-process/scripts/ruleset-hash.sh --list "$T"
rm -rf "$T"
```

Expected: `DETERMINISTIC`, `DRIFT-SENSITIVE`, then exactly two `--list` lines (`a.md` then `b.md`, each `<tab>sha256:<hex>`) — the `.manifest.json` is not listed. Also: `plugins/working-process/scripts/ruleset-hash.sh /nonexistent; echo $?` prints `1`.

- [ ] **Step 3: Bump plugin version**

In `plugins/working-process/.claude-plugin/plugin.json` change `"version": "0.1.1"` to `"version": "0.2.0"`. Run `claude plugin validate . && claude plugin validate plugins/working-process` — expected: both pass.

- [ ] **Step 4: Commit**

```bash
git add plugins/working-process/scripts/ruleset-hash.sh plugins/working-process/.claude-plugin/plugin.json
git commit -m "feat(working-process): add ruleset hashing script, bump to 0.2.0"
```

---

### Task 2: `write-manifest.sh`

**Files:**
- Create: `plugins/working-process/scripts/write-manifest.sh`

**Interfaces:**
- Consumes: nothing.
- Produces: `write-manifest.sh <out-file> <plugin> <marketplace> <plugin-version> <ruleset-hash>` with file entries on stdin, one per line, tab-separated: `name<TAB>hash` or `name<TAB>hash<TAB>keptAgainst`. Writes the manifest atomically (tmp + `mv`) in the normative one-key-per-line format below. This is the ONLY writer of `.manifest.json` (Tasks 5 and 6 depend on the exact line format).

- [ ] **Step 1: Write the script**

```sh
#!/bin/sh
# The only writer of .manifest.json. The format is normative (one key per
# line, exactly as printed here): the drift hook parses it with sed.
set -u

out=${1:?usage: write-manifest.sh <out> <plugin> <marketplace> <version> <ruleset-hash>}
plugin=${2:?}; marketplace=${3:?}; version=${4:?}; ruleset=${5:?}

tmp="$out.tmp.$$"
trap 'rm -f "$tmp"' EXIT

tab=$(printf '\t')
{
  printf '{\n'
  printf '  "manifestVersion": 1,\n'
  printf '  "plugin": "%s",\n' "$plugin"
  printf '  "marketplace": "%s",\n' "$marketplace"
  printf '  "pluginVersion": "%s",\n' "$version"
  printf '  "rulesetHash": "%s",\n' "$ruleset"
  printf '  "files": {\n'
  first=1
  while IFS="$tab" read -r name hash kept; do
    [ -n "$name" ] || continue
    [ "$first" -eq 1 ] || printf ',\n'
    first=0
    if [ -n "${kept:-}" ]; then
      printf '    "%s": { "hash": "%s", "keptAgainst": "%s" }' "$name" "$hash" "$kept"
    else
      printf '    "%s": { "hash": "%s" }' "$name" "$hash"
    fi
  done
  printf '\n  }\n}\n'
} > "$tmp" || exit 1
mv "$tmp" "$out" || exit 1
trap - EXIT
```

Save with `chmod +x plugins/working-process/scripts/write-manifest.sh`.

- [ ] **Step 2: Test output format, keptAgainst, valid JSON**

```bash
T=$(mktemp -d)
printf 'a.md\tsha256:aaa\nb.md\tsha256:bbb\tsha256:ccc\n' | \
  plugins/working-process/scripts/write-manifest.sh "$T/.manifest.json" working-process missing-bits 0.2.0 sha256:fff
cat "$T/.manifest.json"
jq -e '.manifestVersion == 1 and .files."b.md".keptAgainst == "sha256:ccc" and (.files."a.md" | has("keptAgainst") | not)' "$T/.manifest.json" && echo VALID
grep -c '^  "rulesetHash": "sha256:fff",$' "$T/.manifest.json"
rm -rf "$T"
```

Expected: the printed manifest matches the spec's example shape exactly; `VALID`; the grep prints `1` (proving the sed-parseable one-key-per-line format).

- [ ] **Step 3: Commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/scripts/write-manifest.sh
git commit -m "feat(working-process): add single-writer manifest script"
```

---

### Task 3: Rules payload — `workflow.md` and `spec-plan-lifecycle.md`

**Files:**
- Create: `plugins/working-process/rules/workflow.md`
- Create: `plugins/working-process/rules/spec-plan-lifecycle.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the first two of four payload files hashed by Task 1's script and shipped by Tasks 5–6. `workflow.md` deliberately has NO `paths:` frontmatter (loads in every session once installed); `spec-plan-lifecycle.md` has `paths: docs/specs/**, docs/plans/**`.

- [ ] **Step 1: Write `plugins/working-process/rules/workflow.md`** (exactly this content)

```markdown
# Working process — preferred flow

A spec-driven flow for non-trivial work. Every step below is an offer:
suggest it, let the developer decline. A tool that is not installed
disables its suggestion — never the work itself.

1. **Idea → spec.** When the superpowers:brainstorming skill is
   available, start non-trivial features there; capture the agreed design
   as a spec in `docs/specs/`.
2. **Spec → grilling.** Once a spec exists, offer a grilling-session
   (when the working-process plugin is installed) to stress-test its
   language against the project's domain terms.
3. **Grilled spec → architect review.** Offer a dispatch of the
   working-process architect agent (when available); stamp its verdict
   into the spec's `architect:` frontmatter field.
4. **Spec → plan.** Write the implementation plan with
   superpowers:writing-plans when available; plans live in `docs/plans/`.
5. **Plan → adversary review.** Before implementing a non-trivial plan,
   offer a working-process plan-adversary agent dispatch (when
   available); stamp its verdict into the plan's `adversary:` field.
6. **Implementation.** Test-driven when
   superpowers:test-driven-development is available; bugs go through
   superpowers:systematic-debugging when available.

After every architect or plan-adversary round, record the verdict
(`LGTM` | `concerns` | `blocking`) in the reviewed document's
`architect:` / `adversary:` frontmatter field.

When `docs/domain/glossary.md` exists in the project, its canonical
terms and `_Avoid_` bans bind specs, plans, code identifiers, and
reviews.
```

- [ ] **Step 2: Write `plugins/working-process/rules/spec-plan-lifecycle.md`** (exactly this content)

````markdown
---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
---

# Specs and plans — frontmatter and lifecycle

Specs live in `docs/specs/`, plans in `docs/plans/`. Both open with a
YAML frontmatter block:

```yaml
---
ticket: ABC-123     # tracker reference; inline list when several; `none` without one
date: 2026-07-13    # ISO creation date
status: draft       # moves forward only: draft -> approved -> implemented
grilled: grilling   # optional: `grilling` while outcomes are pending; the ISO date once applied
architect: LGTM     # optional: latest architect verdict (LGTM | concerns | blocking)
adversary: LGTM     # optional: latest plan-adversary verdict (LGTM | concerns | blocking)
branch: feature/ABC-123-short-name   # optional: topic branch of the work
base: master        # optional: branch the topic branch was cut from
---
```

- `status` is linear and moves forward only. Review rounds are iterative
  and live in their own fields; `grilled`, `architect`, and `adversary`
  appear only once the corresponding step has run.
- `branch` and `base` appear once the topic branch exists — never guessed
  up front, omitted entirely when there is no topic branch.
- Unfinished process work is greppable:
  `rg -l '^grilled: grilling' docs/` and
  `rg -l '^(architect|adversary): (blocking|concerns)' docs/`.

Lifecycle offers — each an offer the developer may decline, and each made
only when the tool is available: grill a fresh spec (grilling-session);
architect-review a grilled spec (architect agent dispatch);
adversary-review a plan before implementation (plan-adversary agent
dispatch). After any review round, stamp the verdict into the document's
field.

When implementation is about to start, suggest committing the work's
documents under `docs/` — only paths git tracks or would track;
deliberately ignored documents are skipped silently, and committing
itself stays with the developer.

Ticket value format, sourcing order, and backfill live in the
ticket-frontmatter rule.
````

- [ ] **Step 3: Verify frontmatter parses and hash the payload**

```bash
python3 -c "
import re,sys
for p in ['plugins/working-process/rules/workflow.md','plugins/working-process/rules/spec-plan-lifecycle.md']:
    t=open(p).read()
    m=re.match(r'^---\n(.*?)\n---\n',t,re.S)
    print(p, 'frontmatter' if m else 'no-frontmatter')
"
plugins/working-process/scripts/ruleset-hash.sh --list plugins/working-process/rules
```

Expected: `workflow.md no-frontmatter`, `spec-plan-lifecycle.md frontmatter`; `--list` prints two lines.

- [ ] **Step 4: Commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/
git commit -m "feat(working-process): add workflow and spec-plan-lifecycle rules"
```

---

### Task 4: Rules payload — `process-artifacts.md` and `ticket-frontmatter.md`

**Files:**
- Create: `plugins/working-process/rules/process-artifacts.md`
- Create: `plugins/working-process/rules/ticket-frontmatter.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the remaining two payload files. `process-artifacts.md` has `paths: docs/specs/**, docs/plans/**, docs/domain/**, .superpowers/**`; `ticket-frontmatter.md` has `paths: docs/**`.

- [ ] **Step 1: Write `plugins/working-process/rules/process-artifacts.md`** (exactly this content)

```markdown
---
paths:
  - "docs/specs/**"
  - "docs/plans/**"
  - "docs/domain/**"
  - ".superpowers/**"
---

# Process directories and artifacts

A Process directory is a directory the working process creates in a
project repo to hold work artifacts: `docs/specs/`, `docs/plans/`,
`docs/domain/`, and the `.superpowers/` family at the repo root.

## First-create question

When creating a Process directory — or touching one that already exists
with no observable prior decision (neither a `.gitignore` containing `*`
nor any git-tracked file under it) — ASK the developer which mode the
directory gets. Assume no default:

- **Ignored mode**: write a `.gitignore` containing exactly `*` into the
  directory; its contents stay out of the repo.
- **Tracked mode**: no `.gitignore`; artifacts are committed like any
  other file.

Never ask when either signal is already present: a `.gitignore` with `*`
means ignored mode was chosen; a git-tracked file under the directory
(`git ls-files <dir>` non-empty) means tracked mode was chosen.

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

- [ ] **Step 2: Write `plugins/working-process/rules/ticket-frontmatter.md`** (exactly this content)

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

- [ ] **Step 3: Verify frontmatter of both files parses**

```bash
python3 -c "
import re
for p in ['plugins/working-process/rules/process-artifacts.md','plugins/working-process/rules/ticket-frontmatter.md']:
    t=open(p).read()
    m=re.match(r'^---\n(.*?)\n---\n',t,re.S)
    assert m and 'paths:' in m.group(1), p
    print(p,'OK')
"
plugins/working-process/scripts/ruleset-hash.sh --list plugins/working-process/rules | wc -l
```

Expected: both `OK`; the count is `4`.

- [ ] **Step 4: Commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/rules/
git commit -m "feat(working-process): add process-artifacts and ticket-frontmatter rules"
```

---

### Task 5: Drift hook — `check-rules-drift.sh` + `hooks/hooks.json`

**Files:**
- Create: `plugins/working-process/scripts/check-rules-drift.sh`
- Create: `plugins/working-process/hooks/hooks.json`

**Interfaces:**
- Consumes: `ruleset-hash.sh <dir>` (Task 1), the normative manifest line format (Task 2), `${CLAUDE_PLUGIN_ROOT}` env var, `$PWD` as the project directory.
- Produces: a SessionStart hook that prints either nothing or one line of `{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"…"}}` and always exits 0. Nudge wording is consumed verbatim by the sync-rules skill description (Task 6): drift → "run the working-process:sync-rules skill"; newer-manifest direction → "run: claude plugin update <plugin>".

- [ ] **Step 1: Write `plugins/working-process/scripts/check-rules-drift.sh`**

```sh
#!/bin/sh
# SessionStart drift hook for Rules payloads. Silence is the default:
# clean state, missing tools, unresolvable sources, and every failure
# end in no output and exit 0. Nudge messages must never contain double
# quotes or backslashes (they are printf'd into a JSON string).
set -u

ROOT=${CLAUDE_PLUGIN_ROOT:-}
[ -n "$ROOT" ] || exit 0
HASHER="$ROOT/scripts/ruleset-hash.sh"
[ -x "$HASHER" ] || exit 0
PROJ=${CLAUDE_PROJECT_DIR:-$PWD}

plugin_json_field() { # $1 plugin.json path, $2 key
  sed -n "s/.*\"$2\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" "$1" 2>/dev/null | head -n 1
}
manifest_field() { # $1 manifest path, $2 key — normative one-key-per-line format
  sed -n "s/^  \"$2\": \"\([^\"]*\)\",\{0,1\}\$/\1/p" "$1" 2>/dev/null | head -n 1
}

ENGINE_NAME=$(plugin_json_field "$ROOT/.claude-plugin/plugin.json" name)
ENGINE_VERSION=$(plugin_json_field "$ROOT/.claude-plugin/plugin.json" version)

# newer_than A B: true when A > B; plain three-part x.y.z only, else skip.
newer_than() {
  [ "$1" = "$2" ] && return 1
  case "$1$2" in *[!0-9.]*) return 1 ;; esac
  case "$1" in *.*.*) ;; *) return 1 ;; esac
  case "$2" in *.*.*) ;; *) return 1 ;; esac
  lower=$(printf '%s\n%s\n' "$1" "$2" | LC_ALL=C sort -t . -k 1,1n -k 2,2n -k 3,3n | head -n 1)
  [ "$lower" = "$2" ]
}

MESSAGES=""

# The plugin listing is fetched at most ONCE per hook run, lazily, on the
# first foreign manifest — the spec budgets exactly one CLI invocation.
LISTING=""
LISTING_STATE=unfetched # unfetched | ok | failed
get_listing() {
  case $LISTING_STATE in
    ok) return 0 ;;
    failed) return 1 ;;
  esac
  LISTING_STATE=failed
  command -v claude >/dev/null 2>&1 || return 1
  if command -v timeout >/dev/null 2>&1; then
    LISTING=$(timeout 10 claude plugin list --json 2>/dev/null) || return 1
  else
    LISTING=$(claude plugin list --json 2>/dev/null) || return 1
  fi
  LISTING_STATE=ok
}

check_manifest() { # $1 manifest path, $2 level (project|user)
  m=$1; level=$2
  plugin=$(manifest_field "$m" plugin)
  recorded=$(manifest_field "$m" rulesetHash)
  wrote=$(manifest_field "$m" pluginVersion)
  [ -n "$plugin" ] && [ -n "$recorded" ] || return 0

  if [ "$plugin" = "$ENGINE_NAME" ]; then
    srcroot=$ROOT
  else
    # Foreign payload: needs jq and the claude CLI; skipped silently without.
    command -v jq >/dev/null 2>&1 || return 0
    marketplace=$(manifest_field "$m" marketplace)
    [ -n "$marketplace" ] || return 0
    get_listing || return 0
    # Level-aware predicate: user-level manifests accept any scope;
    # project-level manifests require user scope or this project's path.
    srcroot=$(printf '%s' "$LISTING" | jq -r \
      --arg id "$plugin@$marketplace" --arg pwd "$PROJ" --arg level "$level" '
      [ .[] | select(.id == $id and .enabled)
        | select($level == "user" or .scope == "user" or .projectPath == $pwd) ]
      | sort_by(.scope) | .[0].installPath // empty' 2>/dev/null)
    [ -n "$srcroot" ] || return 0
  fi

  [ -d "$srcroot/rules" ] || return 0
  current=$("$HASHER" "$srcroot/rules" 2>/dev/null) || return 0
  [ -n "$current" ] || return 0
  [ "$current" = "$recorded" ] && return 0

  srcver=$(plugin_json_field "$srcroot/.claude-plugin/plugin.json" version)
  if [ -n "$wrote" ] && [ -n "$srcver" ] && newer_than "$wrote" "$srcver"; then
    MESSAGES="$MESSAGES Rules for $plugin installed at $level level were written by plugin version $wrote, newer than the local $srcver - run: claude plugin update $plugin."
  else
    MESSAGES="$MESSAGES Installed rules for $plugin at $level level differ from the plugin's current rules - run the working-process:sync-rules skill to review updates."
  fi
}

for level in project user; do
  case $level in
    # When the session starts in $HOME the two bases coincide — scan once,
    # as user level, so no manifest is checked (or nudged about) twice.
    project) [ "$PROJ" = "$HOME" ] && continue; base="$PROJ/.claude/rules" ;;
    user)    base="$HOME/.claude/rules" ;;
  esac
  [ -d "$base" ] || continue
  for m in "$base"/*/.manifest.json; do
    [ -f "$m" ] || continue
    check_manifest "$m" "$level" || :
  done
done

[ -n "$MESSAGES" ] || exit 0
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$MESSAGES"
exit 0
```

Save with `chmod +x plugins/working-process/scripts/check-rules-drift.sh`.

- [ ] **Step 2: Write `plugins/working-process/hooks/hooks.json`**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/scripts/check-rules-drift.sh\""
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 3: Test — silence with no manifest, nudge on drift, direction nudge, corruption, no-jq**

```bash
P=$(pwd)/plugins/working-process
T=$(mktemp -d); cd "$T"
# 1) no manifest anywhere under $T: silence
OUT=$(HOME="$T" CLAUDE_PLUGIN_ROOT="$P" "$P/scripts/check-rules-drift.sh"); echo "rc=$? out=[$OUT]"
# 2) in-sync manifest: silence
mkdir -p "$T/.claude/rules/working-process"
"$P/scripts/ruleset-hash.sh" --list "$P/rules" | \
  "$P/scripts/write-manifest.sh" "$T/.claude/rules/working-process/.manifest.json" \
  working-process missing-bits 0.2.0 "$("$P/scripts/ruleset-hash.sh" "$P/rules")"
OUT=$(HOME="$T" CLAUDE_PLUGIN_ROOT="$P" "$P/scripts/check-rules-drift.sh"); echo "rc=$? out=[$OUT]"
# 3) stale rulesetHash: drift nudge naming sync-rules
"$P/scripts/ruleset-hash.sh" --list "$P/rules" | \
  "$P/scripts/write-manifest.sh" "$T/.claude/rules/working-process/.manifest.json" \
  working-process missing-bits 0.2.0 sha256:0000
HOME="$T" CLAUDE_PLUGIN_ROOT="$P" "$P/scripts/check-rules-drift.sh"
# 4) newer manifest pluginVersion: direction nudge naming claude plugin update
"$P/scripts/ruleset-hash.sh" --list "$P/rules" | \
  "$P/scripts/write-manifest.sh" "$T/.claude/rules/working-process/.manifest.json" \
  working-process missing-bits 9.9.9 sha256:0000
HOME="$T" CLAUDE_PLUGIN_ROOT="$P" "$P/scripts/check-rules-drift.sh"
# 5) corrupted manifest: silence, rc 0
printf 'not json' > "$T/.claude/rules/working-process/.manifest.json"
OUT=$(HOME="$T" CLAUDE_PLUGIN_ROOT="$P" "$P/scripts/check-rules-drift.sh"); echo "rc=$? out=[$OUT]"
# 6) broken tools with a DRIFTED own manifest still in place: a failing
#    sha256sum/shasum stub (own path) and a failing jq stub (foreign
#    path) must both end in silence, rc 0 — never a false nudge
"$P/scripts/ruleset-hash.sh" --list "$P/rules" | \
  "$P/scripts/write-manifest.sh" "$T/.claude/rules/working-process/.manifest.json" \
  working-process missing-bits 0.2.0 sha256:0000
mkdir -p "$T/.claude/rules/other-plugin" "$T/bin"
printf '{\n  "manifestVersion": 1,\n  "plugin": "other-plugin",\n  "marketplace": "missing-bits",\n  "pluginVersion": "1.0.0",\n  "rulesetHash": "sha256:1111",\n  "files": {\n  }\n}\n' > "$T/.claude/rules/other-plugin/.manifest.json"
printf '#!/bin/sh\nexit 127\n' > "$T/bin/jq"; cp "$T/bin/jq" "$T/bin/sha256sum"; cp "$T/bin/jq" "$T/bin/shasum"; chmod +x "$T/bin/"*
OUT=$(HOME="$T" CLAUDE_PLUGIN_ROOT="$P" PATH="$T/bin:$PATH" "$P/scripts/check-rules-drift.sh"); echo "rc=$? broken=[$OUT]"
# 7) project-level branch: HOME points elsewhere, so PROJ != HOME and the
#    drifted manifest under $T/.claude/rules is found by the PROJECT scan
mkdir -p "$T/otherhome"
HOME="$T/otherhome" CLAUDE_PLUGIN_ROOT="$P" "$P/scripts/check-rules-drift.sh"
cd - >/dev/null; rm -rf "$T"
```

Expected: (1) `rc=0 out=[]`; (2) `rc=0 out=[]`; (3) one JSON line whose `additionalContext` contains `working-process:sync-rules`; (4) one JSON line containing `claude plugin update working-process`; (5) `rc=0 out=[]`; (6) `rc=0 broken=[]` — failing hash and jq stubs degrade to silence, never an error; (7) one JSON line whose `additionalContext` contains `at project level` (the same drifted manifest, now reached through the project scan because HOME differs from the session directory). Case 4's and case 7's output must also parse: pipe each to `jq .` and expect valid JSON.

- [ ] **Step 4: Commit**

```bash
claude plugin validate . && claude plugin validate plugins/working-process
git add plugins/working-process/scripts/check-rules-drift.sh plugins/working-process/hooks/hooks.json
git commit -m "feat(working-process): add SessionStart rules drift hook"
```

---

### Task 6: The `sync-rules` skill

**Files:**
- Create: `plugins/working-process/skills/sync-rules/SKILL.md`

**Interfaces:**
- Consumes: all three scripts by their Task 1/2 CLIs; the drift hook's nudge wording (Task 5); the payload files (Tasks 3–4).
- Produces: the operational skill `working-process:sync-rules` (install / update / uninstall).

- [ ] **Step 1: Write `plugins/working-process/skills/sync-rules/SKILL.md`** (exactly this content)

````markdown
---
name: sync-rules
description: "Install, update, or uninstall rule files shipped by plugins of the missing-bits marketplace (Rules payloads). Use when the developer asks to install, update, or remove distributed rules, when a session-start note says installed rules differ from a plugin's current rules, or right after installing a payload plugin."
---

# sync-rules — the Rules engine

Distributes Rules payloads (a plugin's `rules/` directory) into a rules
target. `<target>` IS the rules directory itself — `$HOME/.claude/rules/`
(user level) or `<project>/.claude/rules/` (project level) — and each
payload occupies exactly `<target>/<plugin-name>/`: its rule files plus a
`.manifest.json`. Never nest another `rules/` segment inside the target.
Three scripts do the deterministic work; never bypass them:

- `${CLAUDE_PLUGIN_ROOT}/scripts/ruleset-hash.sh [--list] <dir>` —
  aggregate or per-file content hashes.
- `${CLAUDE_PLUGIN_ROOT}/scripts/write-manifest.sh <out> <plugin>
  <marketplace> <version> <ruleset-hash>` with `name<TAB>hash[<TAB>keptAgainst]`
  lines on stdin — the ONLY way a manifest is ever written.
- The drift hook uses the same hashing; the two sides never disagree.

Modes by state and intent: **install** (no manifest at the chosen
target), **update** (manifest present), **uninstall** (explicit request).
With several payloads involved, iterate per payload.

## Step 0 — state discovery (always, before anything else)

1. Enumerate payload plugins: run `claude plugin list --json` and keep
   entries that are `enabled`, from this marketplace (id ends
   `@missing-bits`), and whose `installPath` contains a `rules/`
   directory. Locality: an entry counts as installed here when `scope`
   is `user`, or `project` with `projectPath` equal to the current
   project. Dedupe by `id`, project scope wins. If the CLI or its JSON
   fails, fall back to the engine's own payload
   (`${CLAUDE_PLUGIN_ROOT}/rules`) and, for any other payload the
   developer wants, ask for its path. A source path the developer names
   explicitly always overrides discovery for that payload. The named
   path is the rules directory ITSELF: substitute it wherever this flow
   says `<installPath>/rules`, and look for `.claude-plugin/plugin.json`
   in its parent directory; when none is there, the direction gate is
   skipped (no version to compare).
2. Scan both targets for `*/.manifest.json`. Read each manifest's
   `plugin`, `marketplace`, `pluginVersion`, `rulesetHash`.
3. Report findings before acting, in this order:
   - **Both levels installed** for one payload → offer to consolidate
     (remove one); both copies load, the project copy wins on conflict.
   - **Orphan** — a manifest whose source plugin is not installed or is
     disabled. Locality of the test mirrors the manifest's level:
     project-level manifests use the step-1 predicate; user-level
     manifests accept a source at ANY scope on the machine (a
     project-scoped plugin elsewhere legitimately backs a user-level
     rule set — that is NOT an orphan). Offer: remove the rule set, or
     keep it as the developer's own (delete just the manifest).
   - **Drift** — recorded `rulesetHash` differs from
     `ruleset-hash.sh <source>/rules` → offer an update.

## Direction gate (before any update write)

Compare the manifest's `pluginVersion` with the source plugin's version
read from `<installPath>/.claude-plugin/plugin.json` (never from
`claude plugin list`, whose version can be "unknown"). When the manifest
was written by a NEWER plugin than the local one (semver; skip the gate
only if a side is unreadable):

- project-level Tracked-mode target: warn and STOP — no rule writes, no
  manifest rewrite — unless the developer explicitly overrides. The
  correct move is `claude plugin update <plugin>`.
- any other target: warn, show both versions, and ask before continuing
  (a deliberate downgrade stays one confirmation away).

## Install

1. When discovery found more than one uninstalled payload, first ask
   WHICH payload(s) to install.
2. Ask for the target: user level (recommended — one install per
   machine; rules without `paths:` will load in every session) or
   project level (per-repo adoption, shareable with the team).
3. Project level only, second question (there is no default from
   observation alone — ask): commit the rules (usual reason for
   project-level) or keep them local. "Local" means writing a
   `.gitignore` containing exactly `*` INTO `<target>/<plugin-name>/` —
   never editing the repo's root `.gitignore`.
4. Copy `<installPath>/rules/*.md` into `<target>/<plugin-name>/`.
   Collision-aware: if a same-named file already exists there, show the
   diff and ask (overwrite / keep — "keep" records the developer's file
   hash plus `keptAgainst` = shipped hash in the manifest).
5. Write the manifest via write-manifest.sh: per-file lines from
   `ruleset-hash.sh --list` (adjusted for any kept files), aggregate
   from `ruleset-hash.sh`.

## Update — three-phase classification

Build the per-file hash table first: shipped
(`ruleset-hash.sh --list <installPath>/rules`), pristine (manifest
`files` entries), current (hash the files in the target namespace the
same way). Then classify every file name seen anywhere, phase order
normative, first match wins:

**Phase 1 — presence.** A file missing on any of the three sides never
reaches hash comparison. A file present only on disk (neither shipped
nor in the manifest) is the developer's own: ignore silently.

| State | Action |
|---|---|
| shipped only | install it |
| shipped + on disk, not in manifest | collision: diff + ask (keep → record hash=developer's, keptAgainst=shipped) |
| in manifest, not shipped (removed upstream — whether or not still on disk) | show; ask remove / keep as own — either way drop from manifest |
| manifest + shipped, not on disk | silent if shipped == keptAgainst; else ask once to restore (declining records keptAgainst=shipped) |

**Phase 2 — declined versions** (file has `keptAgainst`):

| State | Action |
|---|---|
| shipped == keptAgainst | silent — this exact version was declined |
| shipped != keptAgainst | diff + ask again: overwrite clears keptAgainst; keep re-anchors it to the new shipped hash |

**Phase 3 — hash comparison:**

| State | Action |
|---|---|
| shipped == pristine == current | nothing |
| shipped == pristine, current differs | nothing — local edit, no upstream news; baseline stays so the next upstream change asks |
| shipped differs, current == pristine | auto-update |
| shipped differs, current differs | diff + ask: overwrite / keep (keep sets keptAgainst=shipped) |

Tracked-mode ceremony: for a project-level Tracked-mode target, batch
ALL non-interactive writes (auto-updates and new-file installs) into one
confirmation, per-file diffs on request. User level and Ignored mode
write those silently.

Finish: summarize (auto-updated / asked / silenced counts), then — unless
the direction gate stopped the run — rewrite the manifest in full via
write-manifest.sh with a fresh aggregate `rulesetHash` and, as the
`pluginVersion` argument, the SOURCE plugin's version read from
`<installPath>/.claude-plugin/plugin.json` at this sync. Never echo the
old manifest's value back for a resolvable source; a developer-named
source WITHOUT a plugin.json is the one exception — it keeps the
manifest's existing `plugin`, `marketplace`, and `pluginVersion` values
unchanged (there is nothing to read). `hash` in the manifest is the
LOCAL file's hash as of this sync for every row that was decided
(install / auto-update / overwrite / keep); rows that stayed silent keep
their previous entry unchanged.

## Uninstall

On explicit request: delete `<target>/<plugin-name>/` (rules, manifest,
any Ignored-mode `.gitignore` written at install). Remind the developer that
uninstalling the working-process plugin itself removes the engine AND
the drift detection — rule sets left behind become invisible, so run
uninstall here first.

## Resilience

- Interrupted update: self-heals on the next run — hashes describe the
  actual state; build no transactionality.
- Corrupted or unreadable manifest: treat every file as modified
  (phase 3, diff + ask) and offer to rebuild the manifest.
- Tracked mode: after writing, remind the developer the changed files
  belong in the current work's commit; never commit for them.
````

- [ ] **Step 2: Validate plugin**

Run: `claude plugin validate . && claude plugin validate plugins/working-process` — expected: both pass, skill listed. Also `python3 -c "import re; t=open('plugins/working-process/skills/sync-rules/SKILL.md').read(); m=re.match(r'^---\n(.*?)\n---\n',t,re.S); assert m and 'description: \"' in m.group(1); print('frontmatter OK')"`.

- [ ] **Step 3: Commit**

```bash
git add plugins/working-process/skills/sync-rules/
git commit -m "feat(working-process): add sync-rules skill (rules engine)"
```

---

### Task 7: Identity sync — descriptions, README, marketplace catalog

**Files:**
- Modify: `plugins/working-process/.claude-plugin/plugin.json` (description)
- Modify: `.claude-plugin/marketplace.json` (working-process entry description)
- Modify: `README.md` (repo root — the plugin table row)
- Modify: `plugins/working-process/README.md`

**Interfaces:**
- Consumes: component names from Tasks 3–6.
- Produces: ALL identity places moved together in one commit (marketplace-sync rule: plugin.json description is canonical; the catalog entry and the repo-root README table row may shorten but never contradict).

- [ ] **Step 1: Update `plugin.json` description**

Replace the `description` value with:

```
"Spec-driven working process on top of superpowers: grilling-session, architect-session and sync-rules skills, architect and plan-adversary review agents, and process rules distributed as a Rules payload; domain plugins hook in via *-plan-review checklist skills and their own rules/ payloads"
```

- [ ] **Step 2: Update the marketplace catalog entry**

In `.claude-plugin/marketplace.json`, replace the working-process entry's `description` with:

```
"Spec-driven working process on top of superpowers: grilling-session, architect-session and sync-rules skills, architect and plan-adversary review agents, plus distributed process rules"
```

- [ ] **Step 3: Update the plugin table row in the repo-root `README.md`**

In the root README's plugin table, replace the working-process row's
description with:

```
Spec-driven working process: grilling-session, architect-session and sync-rules skills, architect and plan-adversary review agents, distributed process rules
```

- [ ] **Step 4: Extend `plugins/working-process/README.md`**

Add a section (adapt heading level to the file's existing structure):

```markdown
## Process rules

The plugin ships four rule files in `rules/` — the preferred workflow
(always loaded once installed), spec/plan frontmatter and lifecycle,
Process directory conventions, and ticket frontmatter. Claude Code does
not load plugin rules by itself: install them with the
`working-process:sync-rules` skill.

- **Two targets**: user level (`~/.claude/rules/`, recommended — one
  install per machine) or project level (`.claude/rules/`, per-repo
  adoption; committed rules also work for teammates without the plugin).
- **Updates**: a SessionStart hook compares content hashes and leaves a
  one-line note when the installed rules differ from the plugin's
  current ones; run sync-rules to review. Locally modified files are
  never overwritten silently.
- **Uninstalling the plugin**: run sync-rules uninstall FIRST — the
  plugin gets no signal on its own removal, and rule sets left behind
  lose their update detection.
- **Other plugins**: any plugin of this marketplace can ship a `rules/`
  directory; this plugin's engine discovers, installs, and updates those
  payloads the same way.
- **Requirements**: Claude Code with rules support incl. subdirectories
  (verified on 2.1.207); `jq` only for payloads of other plugins.
```

Also update the README's existing Requirements line: the old
`Claude Code ≥ 2.1.143` minimum becomes `Claude Code ≥ 2.1.207
(verified — rules distribution needs subdirectory rules loading; the
skills and agents alone work on ≥ 2.1.143)` so the file carries one
consistent version story.

- [ ] **Step 5: Validate and commit**

```bash
claude plugin validate .
claude plugin validate plugins/working-process
git add plugins/working-process/.claude-plugin/plugin.json .claude-plugin/marketplace.json README.md plugins/working-process/README.md
git commit -m "docs(working-process): document rules distribution, sync identity"
```

Expected: both validations pass.

---

### Task 8: End-to-end verification + spec/plan closure

**Files:**
- Modify: `docs/specs/2026-07-13-rules-distribution-design.md` (status → implemented)
- Modify: `docs/plans/2026-07-13-rules-distribution.md` (status → implemented)

**Interfaces:**
- Consumes: everything above.
- Produces: verified behavior per the spec's Verification section; closed process frontmatter; committed docs.

- [ ] **Step 1: Full drift-table fixture walk (scripted states, no skill)**

```bash
P=$(pwd)/plugins/working-process
T=$(mktemp -d)
SRC="$T/src/rules"; TGT="$T/tgt"; mkdir -p "$SRC" "$TGT"
printf 'one\n' > "$SRC/a.md"; printf 'two\n' > "$SRC/b.md"
# install-equivalent: copy + manifest
cp "$SRC"/*.md "$TGT/"
"$P/scripts/ruleset-hash.sh" --list "$SRC" | \
  "$P/scripts/write-manifest.sh" "$TGT/.manifest.json" fixture missing-bits 0.1.0 "$("$P/scripts/ruleset-hash.sh" "$SRC")"
# states: upstream change to a.md (auto-update row), local edit to b.md
# (silent-keep row), new upstream c.md (install row), delete b.md upstream
# later etc. — verify hashes classify as the plan's tables say:
printf 'one changed\n' >> "$SRC/a.md"
printf 'local\n' >> "$TGT/b.md"
printf 'three\n' > "$SRC/c.md"
echo "--- shipped:"; "$P/scripts/ruleset-hash.sh" --list "$SRC"
echo "--- current:"; "$P/scripts/ruleset-hash.sh" --list "$TGT"
echo "--- pristine (manifest):"; grep '"hash"' "$TGT/.manifest.json"
rm -rf "$T"
```

Expected: `a.md` shipped ≠ pristine, current == pristine (auto-update row); `b.md` shipped == pristine, current ≠ pristine (silent-keep row); `c.md` shipped-only (install row). This validates that the three hash sources give the classifier exactly the states the tables need.

- [ ] **Step 2: Live install (user level) + canary load check**

Interactive part, exercised by the developer with the plugin installed from this checkout (`/plugin marketplace add <repo-root>` or the already-installed plugin after `claude plugin update`): run the sync-rules skill, choose user level, verify:

```bash
ls "$HOME/.claude/rules/working-process/"
```

Expected: 4 rule files + `.manifest.json`. Then from any project: a fresh headless session `claude -p "Which working-process workflow rule is loaded? Answer yes/no: does your context include a rule describing a spec-driven preferred flow?" --model haiku` answers yes (workflow.md has no `paths:` and loads everywhere). The path-triggered rules stay dormant until a `docs/specs/**` file is touched — same canary technique as the spec's platform-fact verification.

- [ ] **Step 3: Project-level end-to-end in a throwaway repo**

Interactive, driven by the developer with the plugin installed. Create
two throwaway repos (`R=$(mktemp -d); cd "$R"; git init -q .`). In the
first, run the sync-rules skill → install → project level → answer the
second question with **local** and verify the Ignored-mode ignore file:
`.claude/rules/working-process/.gitignore` contains exactly `*`, plus 4
rule files and `.manifest.json` in the same directory. In the second
repo choose **commit** mode (no `.gitignore` is written; the files are
left for the developer's commit).

Then walk the classifier rows the scripted Step 1 cannot reach, against
a mutable source: make a scratch copy of the payload
(`cp -r <installPath>/rules "$R/src-rules"`) and drive updates by
pointing the skill at it (the discovery fallback accepts an explicit
path). Verify live: local edit + upstream change → diff + ask → **keep**
→ manifest entry gains `keptAgainst`; immediate re-run → silent
(declined version); bump the scratch source again → asked again (the
keptAgainst round-trip); delete an installed rule locally → asked once
to restore, declining stays silent on re-run; remove a file from the
scratch source → removed-upstream question. In the commit-mode repo also
verify the Tracked-mode ceremony: auto-updates and new-file installs
arrive as ONE batch confirmation. After any scratch-source update, assert
the rewritten manifest kept its previous `plugin`, `marketplace`, and
`pluginVersion` values (the scratch copy has no plugin.json — the
plugin.json-less exception in the skill's finish step).

- [ ] **Step 4: Fixture payload plugin — discovery, foreign drift, orphan (positive and negative)**

Build a SELF-SUFFICIENT throwaway marketplace: it carries a copy of
working-process (the engine) next to the fixture payload, so the real
marketplace can be removed while the engine stays installed — the
fixture marketplace must reuse the name `missing-bits`, or the
`@missing-bits` discovery filter would not match:

```bash
M=$(mktemp -d)
mkdir -p "$M/.claude-plugin" "$M/plugins/fixture-payload/.claude-plugin" "$M/plugins/fixture-payload/rules"
cp -r plugins/working-process "$M/plugins/working-process"
printf '{\n  "name": "missing-bits",\n  "owner": { "name": "Missing Bits" },\n  "allowCrossMarketplaceDependenciesOn": ["claude-plugins-official"],\n  "plugins": [\n    { "name": "working-process", "source": "./plugins/working-process" },\n    { "name": "fixture-payload", "source": "./plugins/fixture-payload" }\n  ]\n}\n' > "$M/.claude-plugin/marketplace.json"
printf '{ "name": "fixture-payload", "version": "0.0.1", "description": "fixture" }\n' > "$M/plugins/fixture-payload/.claude-plugin/plugin.json"
printf -- '---\npaths:\n  - "docs/**"\n---\n\n# Fixture rule\n' > "$M/plugins/fixture-payload/rules/fixture.md"
echo "$M"
```

Developer flow: remove the real missing-bits marketplace, add `"$M"`,
install working-process from it (user scope is fine), and install
fixture-payload at PROJECT scope in a throwaway repo. Pinning the
PLUGIN's scope matters: with the plugin project-scoped AND its rules
installed at project level, the foreign jq predicate's only true arm is
`.projectPath == $pwd` — the nudge's appearance actually verifies that
comparison instead of slipping through the `.scope == "user"` arm. Then:
sync-rules discovers fixture-payload and installs `fixture-payload/` at
PROJECT level in that repo; append a line to
`"$M/plugins/fixture-payload/rules/fixture.md"` AND bump the fixture's
`plugin.json` to `"version": "0.0.2"` in the same edit — the version
string is the update-delivery mechanism, an unbumped edit may deliver
nothing — then `claude plugin update fixture-payload` → the next
session's hook (in that repo) nudges for fixture-payload at project
level (foreign path, needs `jq`); `claude plugin uninstall
fixture-payload` → sync-rules step 0 reports the rule set as an
**orphan**.

Negative orphan case (setup first — a user-level rule set must exist):
reinstall fixture-payload at PROJECT scope in a second throwaway
project, run sync-rules there and install its rules at USER level this
time. From a third directory, sync-rules step 0 must NOT report that
user-level rule set as an orphan — its source plugin is project-scoped
elsewhere on the machine, which the level-aware predicate accepts for
user-level manifests. Afterwards, clean up in this order: sync-rules
uninstall of the user-level `fixture-payload/` rule set (a test rule
with `paths: docs/**` must not stay active in real sessions), remove the
fixture marketplace, restore the real one, reinstall working-process,
run a normal sync-rules update.

- [ ] **Step 5: Direction gate fixture**

```bash
# with working-process rules installed at user level (Step 2):
MF="$HOME/.claude/rules/working-process/.manifest.json"
sed -e 's/^  "pluginVersion": ".*",$/  "pluginVersion": "9.9.9",/' \
    -e 's/^  "rulesetHash": ".*",$/  "rulesetHash": "sha256:0000",/' \
    "$MF" > "$MF.tmp" && mv "$MF.tmp" "$MF"
WP=$(claude plugin list --json | jq -r '[.[]|select(.id=="working-process@missing-bits")][0].installPath')
CLAUDE_PLUGIN_ROOT="$WP" "$WP/scripts/check-rules-drift.sh"
```

Expected: a JSON nudge containing `claude plugin update working-process`
— the corrupted `rulesetHash` creates the drift, and the 9.9.9
`pluginVersion` makes the direction branch pick the plugin-update
wording over the sync-rules wording. Then run the sync-rules skill: it
must warn (user level → warn-and-ask, not hard stop) and, on decline,
write nothing. Restore the manifest by accepting a normal update
afterwards.

- [ ] **Step 6: Close the process frontmatter and commit docs**

- In `docs/specs/2026-07-13-rules-distribution-design.md`: set
  `status: implemented` (Edit tool).
- In this plan: set `status: implemented`.

```bash
git add docs/specs/2026-07-13-rules-distribution-design.md docs/plans/2026-07-13-rules-distribution.md docs/domain/glossary.md .claude/rules/plugin-authoring.md
git commit -m "docs: record rules-distribution spec and plan as implemented"
```

(The glossary and authoring-rule edits from the grilling session ride along here if not committed earlier.)
