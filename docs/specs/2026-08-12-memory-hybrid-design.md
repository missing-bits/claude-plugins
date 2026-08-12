---
ticket: none
date: 2026-08-12
status: implemented
grilled: 2026-08-12
architect: concerns (resolved 2026-08-12)
branch: feature/memory-hybrid
base: develop
---

# Hybrid Private memory — opt-in redirect onto Auto-memory

## Problem

Claude Code ships its own memory mechanism, and the plugin's Private
memory duplicates it: two stores per project, two write paths, and the
harness's notes land in a directory the project never sees. The hybrid
makes `.claude/memory/` *be* the Auto-memory directory — opt-in per
developer and per environment — so Auto-memory itself reads the store's
index and writes its notes where the plugin's rules already govern.
Team memory (`docs/memory/`) cannot join the redirect (Auto-memory's
team mounts are server-backed; a repo directory cannot be a mount) and
does not need to: the core rule reads it in every mode, and living in git — reviewed,
branched with the work — is its differentiator, not a gap.

## Platform facts (CC 2.1.220, verified 2026-08-10, probes re-run 2026-08-11)

Everything below is empirical; none of it is documented contract.

- `autoMemoryDirectory` (settings) redirects the Auto-memory directory.
  The path must be absolute (`~/` expands); relative and `$VAR` paths are
  silently dropped and the session falls back to the default Home-dir
  directory.
- A *resolving* path is used blindly: a nonexistent absolute path is
  created (`mkdir -p`) and used without a word; an uncreatable path
  (permissions) is still named as the session's memory directory — no
  fallback either way. The only fallback is the trust gate: in an
  untrusted workspace, project and local settings are not consulted at
  all.
- Local and project settings are honored when the workspace is trusted,
  sandboxed, or the session is non-interactive. Committed
  `.claude/settings.json` IS honored (its own schema description says
  otherwise; the observed behavior wins), but the path's machine
  specificity rules it out anyway.
- Auto-memory loads exactly one index file: `MEMORY.md`, up to 200 lines
  / 25 KB. Other files in the directory — `INDEX.md`, `ARCHIVE.md` —
  stay invisible to it.
- `autoMemoryEnabled: false` removes the mechanism entirely.
- Auto-memory's entry shape (frontmatter `name` / `description` /
  `metadata.type`, `[[slug]]` links) is undocumented and has moved
  repeatedly; ADR 0002 already governs the plugin's stance toward it.
- Auto-memory's write-side curation — whether it consolidates or prunes
  index lines and entries on its own — is unprobed. The spec treats it
  as residual risk with a named backstop, never as fact.

## Decisions

### The index renames to `MEMORY.md`, globally

Every store's live index — both parts, hybrid or not — is `MEMORY.md`;
`ARCHIVE.md` stays. One name means no mode detection anywhere: rules,
skills, and docs speak with one voice, and in a hybrid store Auto-memory
loads exactly the file that is the index. The alternatives both pay
forever — a hybrid-only rename forks every sentence that names the index
into two variants, and keeping two indexes puts two writers behind two
catalogs of one directory, with drift built in and the session loading
both. The rename pays once, and the store-probe decoupling
(`docs/specs/2026-08-11-store-probe-decoupling-design.md`) already made
the installment small: no plugin other than project-memory names the
index file, so the scope is this plugin plus three glossary entries.

The rename has one internal cost worth naming: `MEMORY.md` then names
the home-dir and project indexes alike, so migrate-memory loses the
filename as its store discriminator — mitigated by qualifying every
store name with its path in that skill's wording.

Adopting the harness's entrypoint *name* is not adopting its format.
ADR 0002's test — adopt only what earns its place — is met: in a hybrid
store `MEMORY.md` is the only filename Auto-memory will load; elsewhere
the name is as arbitrary as `INDEX.md` was. Residual risk: if the
harness ever renames its entrypoint, non-hybrid stores carry a stale
name at zero functional cost.

Existing stores migrate mechanically: a session governed by the
conventions rule, finding a store whose index still bears the old name,
offers the rename once — and re-points nothing, because nothing outside
the plugin points at the filename any more.

### Opt-in is a dedicated skill

A new explicit-ask skill, `redirect-memory` — enable, disable, and
status in one skill, named for what it does per the `sync-rules`
pattern (settled at the 2026-08-12 grilling) — owns the switch. Enable:

- writes `realpath(<project>/.claude/memory)` — computed, never typed by
  the developer — as `autoMemoryDirectory` into the project's
  `.claude/settings.local.json`, and names the activation environment in
  its output: the path resolves only where this filesystem view exists.
  That file is per-checkout, not per-machine — in a bind-mounted
  dev container, host and container read the same file through different
  path namespaces;
- warns, never refuses: environment detection (`/.dockerenv`,
  `REMOTE_CONTAINERS` in env) only enriches the warning's wording. The
  warning names the path-preserving-mount case (one key activating both
  sides at once) and states what the losing side gets — Home-dir memory
  only without trust or key; otherwise a manufactured stray store or no
  working Auto-memory. Both environment kinds are equally correct places
  to opt in; with disjoint namespaces the active side is simply the one
  that wrote last;
- offers a one-time `migrate-memory` pass for the facts accumulated in
  this environment's Home-dir store, stating the per-environment reach:
  each environment keeps its own Home-dir store, and migration runs
  where the notes live;
- ends with a verification step — write a note, confirm it lands in
  `.claude/memory/` — because every failure mode of the redirect is
  silent by platform design.

Disable names the undo asymmetry before acting: removing the key is
environment-neutral (every environment returns to its default), while
`autoMemoryEnabled: false` in a per-checkout file switches Auto-memory
off in every environment that trusts the checkout. The store itself is
never touched by either.

### Activation contract, stated once

The redirect is in effect exactly when settings are honored — trusted
workspace, sandbox, or non-interactive session: properties of the
environment and the session, never of the repo. Whether it lands on the
store is a separate question: the stored path must name the store in the
session's filesystem namespace, and mere resolution proves nothing,
because the platform manufactures a missing path. One absolute path in
one file still yields a guarantee worth naming, with one stated premise:
at most one Auto-memory writer per store, provided the environments'
path namespaces are disjoint at the store path — the normal
dev-container layout. A path-preserving bind mount (`-v "$PWD:$PWD"`-
style, or a `workspaceMount` that keeps the host path) defeats the
premise: the one key resolves on both sides, both trusted environments
are active at once, and two harnesses share one `MEMORY.md`. The
`redirect-memory` warning names this case alongside its container
wording.

What the losing side of last-write-wins gets follows from the platform
facts, not from a fallback story: a session with settings unconsulted
(untrusted) or no key in sight stays on its Home-dir store; a trusted
session whose stored path is creatable manufactures a stray store there
and writes to it; a trusted session whose stored path is uncreatable
runs with no working Auto-memory at all. The rule below makes the stray
and the broken cases visible.

### The rule deduplicates loading and watches for divergence

In a hybrid store the harness and the core rule would both load Private
memory's `MEMORY.md`. The rule defers: a part whose index the session
context already carries (the Auto-memory block) is not read again;
everywhere else — non-hybrid stores, untrusted sessions, subagents —
the rule loads it as today and remains the safety net. Additionally,
when Private memory exists and
`.claude/settings.local.json` carries `autoMemoryDirectory`, the
rule compares it with `realpath(<project>/.claude/memory)` and says so
plainly on mismatch. This check is mandatory, not decorative: the
platform has no fallback for a resolving-but-wrong path, so the rule's
message is the only visible signal in exactly the environment where the
redirect silently misses. A worktree carries no
`settings.local.json`, so the check raises no false alarms there.

The 200-line / 25 KB load budget becomes an explicit index convention:
lines stay thin, and the "index too long — shorten, don't retry" error
path graduates from migrate-memory to the conventions rule.

### Entries Auto-memory writes are first-class notes

An entry the harness writes is a note like any other. Missing H1 is
format debt — the existing memory-review-session machinery counts it
apart from defects and offers to pay it during the walk; `description`
it already writes; `metadata.type` and other foreign keys stay intact
under the conventions rule's tolerance clause. The index-line format is
already convergent (`- [title](file.md) — summary` on both sides), so a
line the harness appends is a legal projection — appended section-blind:
the harness knows nothing of the Notes/Ideas sectioning, its lines land
where it puts them, and re-sectioning belongs to the groom
(memory-review-session's existing audit and sweep). Auto-memory is
self-curating by design and its write-side behavior is unprobed: whether
it consolidates or prunes index lines is a stated residual risk, not a
verified fact, and the audit — dangling links, body files without lines,
the entry-wins drift rule — is the named backstop, absorbing exactly the
damage such curation could do. `ARCHIVE.md` stays invisible to it by
design; nothing instructs the harness to close entries, and a line its
curation removes is restored by the sweep.

## What this does not change

- **Team memory.** Rule-driven in every mode; the hybrid cannot and does
  not touch it.
- **The entry format.** ADR 0002 stands: the plugin defines its own
  format and converges without adopting. The hybrid adopts the directory
  identity and the entrypoint name — the two things that earn their
  place — and nothing else; ADR 0003 records that confrontation.
- **Store probes.** Foreign plugins test the part directories
  (post-decoupling), so the rename and the redirect are both invisible
  to them.
- **`ARCHIVE.md`** and the closed-entry lifecycle.

## Skills impact

- **`redirect-memory`** (new): as specified above.
- **`migrate-memory`**: with the hybrid active, home-dir → Private is a
  no-op by identity (same directory); the skill detects it and says so.
  Its wording qualifies store names by path — the rename removed the
  filename discriminator. Team-memory migration is unchanged.
- **`memory-review-session`**: no mechanical change; harness-written
  entries fall into the existing audit (missing H1/description = format
  debt).
- **README**: a hybrid section.

## ADR and glossary

ADR 0002 closes with: "Making the store double as the Auto-memory
directory would reverse this decision, so that later choice has to face
it deliberately instead of sliding past it." This spec is that choice,
faced: **ADR 0003** cites the sentence and splits what survives (own
entry format, tolerance clause) from what changes (directory identity,
index name). ADR 0002 remains in force.

Glossary: the three entries naming `INDEX.md` (**Archive**, **Live
entry**, **Close (an entry)**) update to `MEMORY.md`; **Auto-memory**
and **Home-dir memory** gained the redirect corrections at the grilling
session (2026-08-12), which also added two terms: **Hybrid store** — the
Private memory store that is the current session's Auto-memory
directory, a property of the session, never of the checkout — and
**Environment** — one filesystem view a session runs in, the unit the
redirect activates per.

## Documented limitations (not solved, stated)

- The redirect carries one absolute path with no portable form. With
  disjoint path namespaces that means at most one side of a checkout
  writes the store (last write wins); a path-preserving mount activates
  every side whose namespace contains the path, and the one-writer
  premise falls with it.
- The losing side of last-write-wins has no fallback story beyond the
  trust gate: untrusted or keyless sessions stay on their Home-dir
  store; trusted ones either manufacture a stray store at the foreign
  path or run with no working Auto-memory — the divergence check is the
  signal in both. Merging stray and Home-dir stores into the project
  store stays manual (`migrate-memory`, run per environment).
- A git worktree carries no `.claude/settings.local.json` and no Private
  store of its own: worktree sessions — including this repo's own
  feature workflow — sit on the inactive side silently (the divergence
  check stays quiet there by design: no key is present), and their
  Auto-memory writes land in a fresh, path-keyed Home-dir store of the
  worktree, stranded when the worktree is removed.
- Trust is per environment (and per volume where `~/.claude.json` lives
  in one); an environment that does not persist that file loses the
  activation on every rebuild.

## Out of scope

- Synchronizing or merging Home-dir stores with the project store.
- Automating the opt-in inside environment repos (a dev-container setup
  may write the key with its own in-container path from its own scripts;
  the plugin enables that by keeping the contract at "one key, one
  realpath" — and does not own it).
- Coordinating simultaneous host and container sessions beyond the
  degradation above.

## Alternatives considered

- **Two indexes in a hybrid store** (`INDEX.md` for the rule,
  `MEMORY.md` for the harness) — rejected: two writers, two catalogs,
  structural drift, double session load, and the harness's budget spent
  on a file the rule does not control.
- **Hybrid-only rename** — rejected: forks the format into permanent
  mode variants across every rule, skill, and doc, and every store visit
  starts with mode detection.
- **Committed settings as the opt-in carrier** — rejected: the path is
  environment-specific by requirement; committing it breaks every other
  checkout. Env vars and SessionStart hooks are verified dead ends: the
  harness reads its memory env vars from its own `process.env`, which a
  hook cannot reach — `$CLAUDE_ENV_FILE` feeds only the Bash tool's
  shell.
- **Refusing opt-in inside containers** — rejected: the container is the
  designed place to work in such setups, so its inside is the correct
  side to opt in from; the skill warns and names the environment
  instead.

## Review rounds

- **Architect**, 2026-08-12, **Fable 5**. Verdict **blocking**: 2
  Important, 2 Minor.
  1. (Important) The "at most one Auto-memory writer" guarantee is not
     structural: a path-preserving bind mount (`-v $PWD:$PWD`,
     `workspaceMount` at `${localWorkspaceFolder}`) makes one key resolve
     in both environments — two trusted sides simultaneously active, two
     harness writers on one `MEMORY.md`. Qualify the guarantee (disjoint
     namespaces at the store path), name the case in the skill's warning,
     reword the limitation.
  2. (Important) Second-writer coverage stops at the index-line format:
     the sectioned index (Notes/Ideas) meets a section-blind writer, and
     "Auto-memory never closes an entry" is an unverified write-side
     claim in a spec that pins every other fact to a probe. Decide where
     harness appends land (the groom as re-sectioning owner), and probe
     write-side curation or downgrade the claim to a stated residual risk
     with the audit named as backstop.
  3. (Minor) Component changes predate the grilling: "hybrid-memory"
     (instantiates a glossary ban), "all three existing skills" (the
     plugin ships two), "the mode term" (vague; two terms landed).
  4. (Minor) Worktree sessions — this repo's own feature workflow — sit
     on the inactive side with no settings file and no signal; the
     limitations section is silent on them.

  **Disposition (2026-08-12): all four accepted and applied.** Finding
  1: the one-writer guarantee now carries its disjoint-namespaces
  premise, the skill's warning and the limitations name the
  path-preserving-mount case. Finding 2: harness appends declared
  section-blind with the groom as re-sectioning owner; "never closes"
  replaced by a residual-risk statement with the audit as named backstop
  and a matching Platform-facts bullet (write-side curation unprobed —
  the probe was declined as unreliable to provoke; risk stated instead).
  Finding 3: Component changes re-read against the grilled body (two
  skills, `redirect-memory`, glossary line rewritten). Finding 4: a
  worktree limitation line added.

- **Architect, fresh round**, 2026-08-12, **Fable 5**. Verdict
  **concerns**: 1 Important, 4 Minor. Prior dispositions verified as
  genuinely resolved.
  1. (Important) The "inactive side degrades to its own Home-dir memory"
     narrative contradicts the spec's own platform facts: a *trusted*
     session on the losing side never returns to Home-dir memory — a
     creatable foreign path is manufactured (`mkdir -p`) and becomes a
     stray active store; an uncreatable one leaves no working Auto-memory
     at all. Home-dir degradation holds only for untrusted or keyless
     sessions. Replace the claim, everywhere it appears and in the
     skill's warning, with that trichotomy; "resolves" in the activation
     contract does not discriminate the store from a stray.
  2. (Minor) Worktree limitation understates: Home-dir stores are
     path-keyed, so each worktree gets a fresh store, stranded at
     cleanup; the glossary's "per Environment" could tighten to "per
     checkout path".
  3. (Minor) "Both conjuncts are properties of the environment" — only
     trust is environmental; sandbox and non-interactivity are
     per-session. Say "of the environment and the session".
  4. (Minor) The rename costs migrate-memory its filename discriminator
     (`MEMORY.md` then names home-dir and project indexes alike); the
     rename decision should name the cost, path-qualified store names the
     mitigation.
  5. (Minor) ADR 0003 is promised but missing from Component changes.

  **Disposition (2026-08-12): all five accepted and applied.** Finding
  1: the degradation story replaced by the fact-derived trichotomy in
  the activation contract, the limitations, and the skill's warning; the
  contract now separates "in effect" (settings honored) from "lands on
  the store", since resolution alone proves nothing. Finding 2: the
  worktree limitation names the fresh path-keyed store stranded at
  cleanup; the glossary's Home-dir memory tightened to "per checkout
  path". Finding 3: "of the environment and the session, never of the
  repo". Finding 4: the rename decision names the lost filename
  discriminator with path-qualified store names as mitigation, mirrored
  in Skills impact. Finding 5: ADR 0003 added to Component changes.

## Component changes

**`project-memory`** — the core rule (dedup + divergence check, rename),
the conventions rule (index name, budget convention, rename offer), both
existing skills' index-name mentions, the new `redirect-memory` skill,
README. Breaking rename → **minor** bump pre-1.0, minted in the
release PR; the release obligation ≥ 0.4.0 from the entry-format branch
still stands, so one shared final version covers both. Dogfooding on
this repo is the natural path (`0.4.0-dev.<discriminator>`).

**Glossary** — the two terms and two corrections landed at the grilling
(2026-08-12); the three `INDEX.md` entries update with the rename at
implementation.

**ADR 0003** — the confrontation record (`docs/domain/adr/`), written at
implementation per the ADR-and-glossary section.

**No other plugin changes** — the decoupling already removed every
foreign coupling to the store's layout.
