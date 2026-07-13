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
    # Level-aware predicate. The CLI computes `enabled` contextually — a
    # project-scoped plugin reports enabled=false outside its own project
    # — so for user-level manifests a project-scope entry counts
    # regardless of that flag; user-scope entries still require it.
    # Project-level manifests require user scope or this project's path.
    srcroot=$(printf '%s' "$LISTING" | jq -r \
      --arg id "$plugin@$marketplace" --arg pwd "$PROJ" --arg level "$level" '
      [ .[] | select(.id == $id)
        | select(if $level == "user"
            then (.scope == "project" or .enabled)
            else (.enabled and (.scope == "user" or .projectPath == $pwd))
            end) ]
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
