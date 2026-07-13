---
ticket: none
date: 2026-07-13
status: implemented
grilled: 2026-07-13
architect: LGTM
branch: feature/process-rules
base: master
---

# Rules distribution for the working-process plugin

## Problem

The working-process plugin ships skills and agents, but the working process
itself is carried by rule files (`.claude/rules/*.md`): the preferred flow,
the spec/plan frontmatter and lifecycle, the Process directory conventions,
and the ticket frontmatter convention. Claude Code plugins have no native
rules component — a `rules/` directory inside a plugin is inert data the
runtime never loads. Without a distribution mechanism, a plugin user gets
the tools of the process but not the process.

This spec covers shipping the rule files with the plugin and the
install/update mechanism they require. It is the second spec of the plugin;
the plugin's components themselves are covered by
`2026-07-13-working-process-plugin-design.md`.

## Verified platform facts

Doc-verified (Claude Code docs, July 2026):

- `~/.claude/rules/` exists (user-level rules, loaded before project rules;
  project rules win on conflict).
- A rule file without a `paths:` field is loaded unconditionally at session
  start; with `paths:` it loads when a matching file is touched.
- Plugins cannot ship rules natively; the supported component list has no
  `rules/` entry.
- Symlinks inside `.claude/rules/` are supported, but the plugin cache path
  is versioned (`…/<plugin>/<version>/…`), so a symlink goes stale on every
  plugin update.

Empirically verified on Claude Code 2.1.207 (canary rules, headless runs):

- Rules in a subdirectory of `.claude/rules/` load, both unconditional and
  path-triggered ones — namespacing under `rules/working-process/` works.
- A non-markdown file (`.manifest.json`) next to rule files is ignored
  without errors.
- Rules load in headless sessions even when the workspace is untrusted
  (trust gates only `permissions.allow`).
- `claude plugin list --json` reports every installed plugin's `id`
  (`plugin@marketplace`), `version`, `enabled`, `installPath`, `scope`
  (`user` / `project`), and — for project scope — `projectPath`: a
  first-party way to resolve another plugin's files, with enough locality
  information for the discovery predicate. Caveat (verified live): the
  `enabled` flag is computed contextually — a project-scoped plugin
  reports `enabled: false` when listed from outside its own project — so
  predicates about sources in OTHER projects must not require it. Caveats observed:
  entries can repeat (per scope — dedupe by `id`) and `version` can be
  `"unknown"` (one more reason drift detection uses content hashes, never
  versions). The JSON shape is a CLI contract, not a formally versioned
  API: every consumer of it degrades gracefully when parsing fails.

## Approach

**Copy + manifest, engine + payload.** A plugin carries rule files as
plain data in `rules/`. One skill installs them by copying into a target
rules directory and records a manifest next to them; the same skill
performs updates and uninstall. A SessionStart hook detects upstream drift
and nudges.

The mechanism is split so future plugins never duplicate it:

- **Engine** — lives in working-process: the sync-rules skill, the drift
  hook, and the scripts. working-process is also the first payload (its own
  `rules/`).
- **Payload contract** (a missing-bits marketplace convention) — a plugin
  of this marketplace that wants to ship rules provides a `rules/`
  directory. Nothing else: no skill, no hook, no scripts of its own. The
  working-process dependency comes in two strengths, chosen per plugin:
  **soft** (the default — the plugin's own skills and agents work
  standalone; when working-process is also installed, its sync-rules skill
  picks the payload up) or **hard** (a `dependencies` entry on
  `working-process@missing-bits`, auto-installing it — and transitively
  superpowers — reserved for plugins whose process integration is their
  core).
- **Discovery** — the engine resolves payload plugins through
  `claude plugin list --json`. An entry counts as installed here only when
  its `scope` is `user`, or `project` with `projectPath` equal to the
  current project — plugins enabled solely in other projects are
  invisible. Then: deduped by `id` (project scope wins over user scope),
  `enabled` only, restricted to this marketplace (`@missing-bits` ids),
  filtered to plugins whose `installPath` contains `rules/`. This
  project-local predicate governs **install enumeration** only. The
  **orphan test** and the **hook's source resolution** are level-aware:
  for a project-level manifest they use the same local predicate, but for
  a user-level manifest they ignore `projectPath` — and, for
  project-scope entries, the contextually computed `enabled` flag too
  (see the platform-facts caveat) — a plugin installed at
  project scope anywhere on the machine legitimately backs a user-level
  rule set, which loads in every project. Each payload installs into its
  own namespace, `rules/<plugin-name>/`, with its own manifest.

Rejected alternatives:

- **Symlink into the plugin cache** — breaks on every update (versioned
  cache path), cannot represent local modifications, and a committed
  symlink to a machine path is useless to a team.
- **Injecting rule content via SessionStart `additionalContext`** — defeats
  path-triggered loading; every rule would burden every session in every
  project. Rejected already in spec 1, upheld here.

A useful property of the copy approach: rules installed project-level and
committed work for teammates who do not have the plugin at all — the plugin
is needed only to install, update, and follow the full process, not for the
rules to load.

## Plugin structure

```
plugins/working-process/
├── rules/                          # plain data — not a Claude Code component
│   ├── workflow.md                 # no paths: — loads in every session once installed
│   ├── spec-plan-lifecycle.md      # paths: docs/specs/**, docs/plans/**
│   ├── process-artifacts.md        # paths: docs/specs/**, docs/plans/**, docs/domain/**, .superpowers/**
│   └── ticket-frontmatter.md       # paths: docs/**
├── skills/sync-rules/SKILL.md      # install + update + uninstall
├── hooks/hooks.json                # SessionStart → scripts/check-rules-drift.sh
└── scripts/
    ├── ruleset-hash.sh             # aggregate hash of a rules directory (shared)
    ├── write-manifest.sh           # the only writer of .manifest.json
    └── check-rules-drift.sh        # hook entry point
```

## Rule content requirements

All four files are written from scratch for this plugin, in English, using
the glossary's canonical terms. Shared requirement — **graceful
degradation**: every mention of a skill or agent is conditional ("when the
X skill is available…"); a session without this plugin or without
superpowers must never be told to invoke something that is not there, and a
missing tool disables the suggestion, never blocks the work.

- **`workflow.md`** (always loaded): the preferred flow — idea →
  brainstorming → spec → grilling → architect review → plan → adversary
  review → implementation (test-driven; systematic debugging for bugs);
  suggestions are offers the developer may decline; review verdicts are
  stamped into the reviewed document's `architect:` / `adversary:`
  frontmatter fields; when `docs/domain/glossary.md` exists, its canonical
  terms and `_Avoid_` bans bind documents and identifiers.
- **`spec-plan-lifecycle.md`**: the spec/plan frontmatter block (`ticket`,
  `date`, `status`, process fields `grilled` / `architect` / `adversary`,
  branch fields `branch` / `base`); linear `status` lifecycle
  (draft → approved → implemented) with iterative review rounds living in
  the process fields; per-stage offers (grill a new spec, architect-review
  a grilled spec, adversary-review a plan before implementation); a
  suggestion to commit the work's documents when implementation starts
  (developer-authorized, tracked paths only); specs live in `docs/specs/`,
  plans in `docs/plans/`.
- **`process-artifacts.md`**: the First-create question in full — when a
  Process directory is first created, or exists with no observable prior
  decision (neither a `.gitignore` containing `*` nor a git-tracked file),
  ask: Ignored mode or Tracked mode; never ask when either signal is
  present. This extends the convention to `docs/specs/` and `docs/plans/`
  (deferred from spec 1). Also: Tracked-mode artifacts ride along with the
  commits of the work they belong to; artifact files are edited with the
  Edit tool, not shell one-liners; per-work artifacts carry a `ticket`
  frontmatter field, registry files (the glossary, `.gitignore`) are
  exempt.
- **`ticket-frontmatter.md`**: `ticket` value format (tracker short
  reference, never a URL; inline list form when several; explicit `none`);
  sourcing order for new documents (branch name → conversation → ask once);
  backfill when editing a document that lacks frontmatter (never
  interrupts with a question; `date` from git history); one-line search
  patterns for finding documents by ticket.

## Manifest

`.manifest.json`, written next to the installed rules
(`<target>/rules/working-process/.manifest.json`):

```json
{
  "manifestVersion": 1,
  "plugin": "working-process",
  "marketplace": "missing-bits",
  "pluginVersion": "0.2.0",
  "rulesetHash": "sha256:…",
  "files": {
    "workflow.md": { "hash": "sha256:…" },
    "spec-plan-lifecycle.md": { "hash": "sha256:…", "keptAgainst": "sha256:…" }
  }
}
```

In Tracked mode the manifest is committed together with the rules — it is
team state, naming the upstream content the team adopted (`rulesetHash`)
and the plugin version that wrote it (`pluginVersion`).

- `manifestVersion` — schema version of the manifest itself.
- `plugin` + `marketplace` — the payload's identity; how the engine maps a
  manifest back to its source plugin.
- `pluginVersion` — never a drift signal (the plugin version bumps on any
  plugin change, not only rule changes — and `claude plugin list` can
  report a version as `"unknown"`). Its one job beyond diagnostics is the
  direction warning in shared Tracked mode (see the update flow).
- `rulesetHash` — aggregate hash of the plugin's `rules/` content at the
  last completed sync (sha256 over the per-file `sha256sum` output, sorted
  under `LC_ALL=C`, with paths relative to the rules directory — pinned so
  a hash written on one machine compares equal on another); the hook's
  only input.
- `files.<name>.hash` — the local file's hash as of the last sync that
  **decided** that file's row (install, auto-update, overwrite, keep): the
  shipped content for installed / auto-updated / overwritten files, the
  developer's own content for kept ones. Silent rows leave it untouched —
  in particular, a silently kept local edit keeps its pristine baseline,
  so a later upstream change still routes through a question, never a
  clobber. This is the skill's per-file drift baseline.
- `files.<name>.keptAgainst` — present only after a "keep mine" decision:
  the hash of the upstream version the developer declined. The skill asks
  again only when the shipped hash differs from it.

The manifest format is normative — one key per line, exactly as above —
because the hook parses it with grep/sed. To keep writer and parser from
ever disagreeing, the skill never serializes the manifest free-form: all
writes go through the shared `write-manifest.sh`, the same
single-sourcing rule the hashing arithmetic follows.

## The sync-rules skill

One skill, three modes decided by state and intent: **install** (no
manifest at the chosen target), **update** (manifest present), **uninstall**
(on explicit request). Every mode operates per payload plugin; with several
payloads involved the skill iterates.

**Step 0 — state discovery,** always: enumerate payload plugins (the
discovery above; on a CLI or parse failure, fall back to the engine's own
`${CLAUDE_PLUGIN_ROOT}` payload and, if the developer is after another
plugin's rules, ask for its path) and scan both targets (`~/.claude/rules/`
and the project's `.claude/rules/`) for `*/.manifest.json`. Three findings
get reported before anything else:

- a payload installed at both levels — offer to consolidate (remove one);
  two copies load into the same session, the project copy winning on
  conflict;
- an **orphan** — a manifest whose source plugin is no longer installed (or
  is disabled): offer to remove the rule set or keep it as the developer's
  own (dropping the manifest);
- an installed payload with upstream drift — offer an update.

**Install:** when several discovered payloads are uninstalled, ask which to
install. Ask for the target — user-level (recommended: one install per
machine; rules without `paths:`, like the engine's `workflow.md`, then load
in every session by design, while path-triggered rules stay dormant outside
matching projects) or project-level (per-repo adoption, shareable with a
team — and loading for teammates who do not even have the plugin).
Project-level gets a second question in the spirit of the First-create
question: commit the rules to the repo (default — sharing is the usual
reason to install project-level) or keep them local — implemented as a
`.gitignore` containing `*` inside `rules/<plugin-name>/` itself (the
Ignored-mode pattern), never an edit to the repo's root `.gitignore`. Non-markdown files inside a namespace directory
(`.manifest.json`, this `.gitignore`) are expected and verified harmless.
Then copy the files and write the manifest — collision-aware: when the
target already contains same-named files (rules adopted by hand, or a
Tracked-mode checkout missing its manifest), those files take the
diff + ask path, never a blind copy.

**Update — drift table.** The deterministic part is scripted: for every
file, compare three hashes — *shipped* (plugin `rules/`), *pristine*
(manifest), *current* (disk):

Classification runs in three phases; phase order is normative, and within
a phase the first matching row wins. The phases exist so that every
keep-mine steady state is caught (phase 2) before the auto-update row
could clobber it, and so the missing-file rows are reachable at all.

**Phase 1 — presence.** A file missing on one of the three sides never
reaches hash comparison. A file present **only** on disk (in the
namespace but in neither plugin nor manifest) is the developer's own and
is none of the engine's business — ignored without comment:

| State | Action |
|---|---|
| in plugin only (new upstream) | install |
| in plugin and on disk, not in manifest (new upstream, collision with a developer file) | diff + ask: overwrite / keep — keep records `hash` = developer's file, `keptAgainst` = shipped |
| in manifest, not in plugin (removed upstream) | show, ask: remove / keep as the developer's own — either way the entry drops from the manifest |
| in manifest and plugin, not on disk (deleted locally) | silent when shipped == `keptAgainst` (restore already declined); otherwise ask whether to restore — declining records `keptAgainst` = shipped |

**Phase 2 — declined versions.** Any file with a `keptAgainst` entry:

| State | Action |
|---|---|
| shipped == `keptAgainst` | silent — this exact version was already declined |
| shipped ≠ `keptAgainst` | upstream moved past the declined version: diff + ask again — overwrite clears `keptAgainst`, keep re-anchors it to the new shipped hash |

**Phase 3 — hash comparison.** Everything else:

| State | Action |
|---|---|
| shipped == pristine == current | nothing |
| shipped == pristine, current ≠ pristine | nothing — a local edit with no upstream news is kept silently (conffile semantics); the pristine baseline stays, so the next upstream change asks instead of clobbering |
| shipped ≠ pristine, current == pristine | auto-update, refresh manifest hash |
| shipped ≠ pristine, current ≠ pristine | diff + ask: overwrite / keep — keep sets `keptAgainst` = shipped |

**Shared Tracked mode needs a direction stance, because hashes have
none.** The committed manifest (see the manifest section) makes the team
scenario tractable: rules in the repo may be newer than the local plugin —
a teammate with a newer working-process synced and committed. Silent
auto-update would downgrade the team's rules, and two teammates on
different plugin versions would ping-pong forever. The stance, with a
fixed point:

- For a project-level Tracked-mode target, every non-interactive write —
  the auto-update row and new-file installs alike — degrades to one batch
  confirmation (per-file diffs on request): one ceremony for all writes
  into a team-committed directory.
- The version gate runs at **every** level: when the manifest's
  `pluginVersion` is newer than the acting plugin's version (semver;
  versions read from `plugin.json` at the resolved install path, never
  from `claude plugin list`, whose `version` can be `"unknown"` — the
  comparison is skipped only if a side is still unreadable), the skill
  reacts before classification. Project-level Tracked mode: warn and
  **stop** — no rule writes, no manifest rewrite — unless the developer
  explicitly overrides; the committed manifest therefore only ever
  advances, the older side's correct move is
  `claude plugin update working-process`, and churn ends when versions
  converge — that is the fixed point. User level and Ignored mode: warn
  and confirm rather than stop — a `~/.claude` synced through a dotfiles
  repo recreates shared state, while a deliberate downgrade stays one
  confirmation away.
- User-level and Ignored-mode installs keep the silent auto-update when no
  direction warning fires.

The skill ends with a summary (auto-updated / decided / silenced counts)
and — unless the direction stop fired — rewrites the manifest in full,
including a fresh `rulesetHash`.

**Uninstall:** remove a payload's rules directory and manifest at the
chosen level. A payload plugin removed without this cleanup surfaces later
as an orphan (step 0). working-process itself has no such safety net — with
the engine gone, nothing detects anything — so the README instructs: run
sync-rules uninstall before uninstalling working-process. Documentation,
not mechanism; the plugin gets no signal when it is removed.

**Resilience:** an interrupted update self-heals on the next run — the
hashes describe the actual state, so no transactionality is built; a
corrupted or unreadable manifest degrades to treating every file as
modified (diff + ask) and offers to rebuild the manifest; hashing uses
`sha256sum` with a `shasum -a 256` fallback (macOS).

## The drift hook

`hooks/hooks.json` registers a SessionStart hook running
`check-rules-drift.sh`:

1. For each level (project first, then user), find installed manifests
   (`rules/*/.manifest.json`) and extract their `plugin` and `rulesetHash`
   with grep/sed — the core path has **no jq dependency**.
2. Resolve each manifest's source rules directory: the engine's own payload
   via `${CLAUDE_PLUGIN_ROOT}` (always, jq-free); other payloads via
   `claude plugin list --json`, which needs `jq` — when `jq` is absent,
   foreign payloads are silently skipped (no nudge; manual sync still
   works).
3. Compute each source's aggregate hash via the shared `ruleset-hash.sh`
   (the same arithmetic the skill uses — the two sides must never
   disagree) and compare with the manifest's `rulesetHash`.
4. On mismatch, emit one sentence of `additionalContext` per drifted
   payload, naming the payload and level and pointing at the sync-rules
   skill. The wording says the installed copy *differs* from the plugin's
   current content — never "outdated": drift is directionless, and in the
   shared Tracked-mode case the installed copy can be the newer side.
   The one direction the hook can see cheaply, it uses: when the
   manifest's `pluginVersion` is newer than the version in `plugin.json`
   at the source plugin's resolved install path (for the engine's own
   payload that is `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`,
   jq-free — both sides are one grep away; semver, skipped when a side is
   unreadable), the nudge points at `claude plugin update` instead of
   sync-rules. Equal hashes, no manifest, unresolvable source, or any
   failure: silence.

The foreign-payload path costs one `claude plugin list --json` invocation
inside a SessionStart hook — a full CLI start-up. Accepted, bounded, and
avoided where possible: the call is wrapped in `timeout` where that
utility exists (`command -v timeout` — stock macOS historically lacks
it; run unwrapped there, mirroring the hashing fallback), and it is
skipped entirely when no foreign manifest exists (the common case today —
the engine's own payload never needs it).

The hook fires only when **upstream** changed since the last completed
sync. Per-file decisions ("keep mine") never re-trigger it — they are the
skill's business. Guards: pure POSIX sh, every branch failure-tolerant,
always `exit 0`. Both scripts take the rules directory and the install
namespace as arguments rather than hardcoding the engine's own payload.

## Versioning and documentation

- This change bumps the plugin to **0.2.0** (minor: new components).
- New components change the plugin's public identity: the `plugin.json`
  description, the marketplace catalog entry, and the README move together
  in the same commit, per this repo's marketplace-sync rule.
- The plugin README documents: the two-level install model, the update
  nudge, the uninstall-before-plugin-uninstall instruction, and the minimum
  Claude Code version (rules subdirectory loading and SessionStart
  `additionalContext` — verified on 2.1.207).

## Verification

- `claude plugin validate .` and `claude plugin validate
  plugins/working-process` pass.
- End-to-end, project-level, in a throwaway repo: install → files and
  manifest in place and rules load (canary check: subdirectory +
  path-trigger, as in the platform-fact verification); simulate an upstream
  change → hook nudges; run update → every drift-table row classified
  correctly against per-case fixtures.
- Engine + payload: a throwaway fixture plugin with a `rules/` directory,
  installed from a local marketplace — sync-rules discovers it, installs
  into `rules/<fixture-name>/`, the hook nudges on its drift, and
  uninstalling the fixture turns its rule set into a reported orphan.
  The negative case too: a user-level manifest whose source plugin is
  installed at project scope in a *different* project is not an orphan
  (the level-aware predicate ignores `projectPath` for user-level
  manifests).
- Direction gate: a fixture manifest whose `pluginVersion` exceeds the
  acting plugin's — the skill warns and stops with zero writes
  (project-level Tracked mode) or warns and asks (user level), and the
  hook's nudge switches to `claude plugin update`.
- Hook robustness: runs silently with no manifest, with a corrupted
  manifest, and on a PATH without `jq` and without `sha256sum` (for the
  engine's own payload; foreign payloads are skipped without `jq`).
- Interactive paths (target question, diff + ask) are exercised live by the
  developer.

## Other plugins of this marketplace shipping rules

Covered by the engine + payload split: a future domain plugin (Salesforce,
Java, Python, …) in this marketplace ships a `rules/` directory and is
picked up by working-process's sync-rules and drift hook automatically — no
mechanism duplication. Its dependency on working-process stays **soft** by
default (the plugin is fully usable standalone; rules become installable
when working-process is present) and is declared **hard** only when process
integration is the plugin's core. Plugins outside this marketplace are out
of scope by design — the discovery filter is explicit about that.

## Out of scope / follow-ups

- Resolved during this spec's grilling (applied to the repo rules and the
  glossary directly): the `*-session` naming convention binds
  conversation skills only, so `sync-rules` keeps its name; the Process
  directory term stays narrow (`.claude/rules/` is not one — the
  project-level install question is defined in this spec); this repo's
  authoring rule gained a "Rules payload" section for future payload
  plugins.
- Automatic writes at session start (full auto-sync) — rejected: a hook
  writing into `~/.claude/` every session is more trust than a nudge is
  worth.
- Migration tooling for users who maintain hand-copied versions of similar
  rules — the modified-file path of the update flow covers them adequately.
