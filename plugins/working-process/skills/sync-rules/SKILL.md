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
