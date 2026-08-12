---
name: redirect-memory
description: "Enable, disable, or inspect the Auto-memory redirect that makes this project's Private memory a Hybrid store (autoMemoryDirectory in .claude/settings.local.json). Use ONLY when the developer explicitly asks to point Claude Code's own memory at the project store or back (\"enable the hybrid store\", \"redirect memory to the project\", \"włącz hybrydę\"). Not a routine memory read or write."
---

# redirect-memory

Points Auto-memory at this project's Private memory store — or points it
back. One key, one realpath: the skill writes `autoMemoryDirectory` into
`.claude/settings.local.json` and nothing else. Explicit-ask only; never
commits; never touches store content.

## Status (always first)

Read `.claude/settings.local.json` (when present) and report:

- no `autoMemoryDirectory` key in ANY honored settings file → redirect
  off; sessions here use their default Home-dir store. Before saying
  "off", also check `.claude/settings.json` (committed — honored despite
  its own schema note) and the user-level settings, and name the file
  that carries the key when one does;
- key equal to `realpath(<project>/.claude/memory)` → active in THIS
  environment;
- key differing → written from another environment (or the checkout
  moved): name both paths and which filesystem view each resolves in.

## Enable

1. Compute `realpath(<project>/.claude/memory)` — never accept a typed
   path. The store need not exist yet: asking for the redirect is the
   intent signal the core rule's adoption clause waits for, so offer to
   create Private memory (always ignored, never asked tracked/ignored).
2. Warn before writing — always. The settings file is per-checkout; the
   path is per-environment ("this path resolves only where this
   filesystem view exists"). A session on the losing side gets Home-dir
   memory only without trust or key; otherwise it manufactures a stray
   store at the foreign path, or runs with no working Auto-memory at
   all. A path-preserving bind mount (`-v "$PWD:$PWD"`-style) activates
   both sides at once — two writers on one index. Environment detection
   (`/.dockerenv`, `REMOTE_CONTAINERS` in env) only enriches this
   wording ("you are writing the container-side path"); never refuse.
3. Write the key preserving every other key in the file — the Edit tool
   when the file exists, the Write tool when it does not.
4. Offer a one-time `migrate-memory` pass (when that skill is available)
   for THIS environment's Home-dir store — each environment keeps its
   own, so migration runs where the notes live.
5. Verification, stated to the developer: settings are read at session
   start, so the redirect takes effect in the NEXT session. Start one,
   write a note, confirm the file lands in `.claude/memory/` — every
   failure mode of the redirect is silent by platform design.

## Disable

Name the asymmetry, then let the developer choose:

- **Remove the key** (the default): environment-neutral — every
  environment returns to its own default Home-dir store.
- **`autoMemoryEnabled: false`**: switches Auto-memory off in EVERY
  environment that trusts this checkout — the bigger hammer, written
  only on an explicit request for it.

Either way the store is untouched and the rule-driven loading continues.

## Boundaries

Writes exactly one settings file, never a committable one — the path has
no portable form. Never commits. Never creates or edits store content:
store creation is the core rule's offer, moving notes is
migrate-memory's, grooming is memory-review-session's.
