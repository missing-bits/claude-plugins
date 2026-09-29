#!/bin/sh
# Reads working-process settings for the current project and prints the
# settings block: the process-settings rule (working-process/rules) is
# the contract for the files, the grammar and the block; the key
# registry (plugins/working-process/SETTINGS_REGISTRY.md) is the
# contract for the keys; this plan's Tasks 2-5 are the contract for the
# modes this script implements (hook mode and --print here; the
# worktree/bare layouts, --validate and --set in later tasks).
set -u
export LC_ALL=C

usage() {
  echo "usage: load-settings.sh [--print]" >&2
}

die() {
  echo "error: $1" >&2
  exit 1
}

LOADER=$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")
PLUGIN=$(cd "$(dirname "$LOADER")/.." && pwd -P)
REGISTRY="$PLUGIN/SETTINGS_REGISTRY.md"

# find_root: sets ROOT, DIR, TEAM, LOCAL, LAYOUT, LOCAL_LABEL for the
# current invocation. LAYOUT is always "main" here; Task 3 adds the
# worktree/bare layouts and their LOCAL fallback.
find_root() {
  r=$(git rev-parse --show-toplevel 2>/dev/null)
  gitrc=$?
  if [ "$gitrc" -ne 0 ] || [ -z "$r" ]; then
    if [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then
      r=$CLAUDE_PROJECT_DIR
    else
      r=$PWD
    fi
  fi
  ROOT=$(cd "$r" 2>/dev/null && pwd -P) || return 1
  DIR="$ROOT/.working-process"
  TEAM="$DIR/settings.md"
  LOCAL="$DIR/settings.local.md"
  LAYOUT=main
  LOCAL_LABEL="settings.local.md"
}

# registry_keys: every "## " heading's key, in file order.
registry_keys() {
  sed -n 's/^## \(.*\)$/\1/p' "$REGISTRY"
}

# registry_field <key> <field>: the field's value for that key (sed -n
# from the key's heading to the next heading, then the "<field>: "
# line, value after the two characters ": ").
registry_field() {
  key=$1
  field=$2
  esc=$(printf '%s' "$key" | sed 's/\./\\./g') || return 1
  sed -n "\\%^## ${esc}\$%,\\%^## %{ /^${field}: /{ s/^${field}: //p } }" "$REGISTRY" || return 1
}

# scan_file <file> <scope>: one awk pass over a settings file (team or
# local). A fence toggles on a line matching ^```. Outside a fence, a
# line matching ^[a-z0-9-]+\.[a-z0-9./-]+: is a settings line; it is
# valid when the whole line matches
# ^[a-z0-9-]+\.[a-z0-9./-]+:[ \t]*[A-Za-z0-9._/-]+[ \t\r]*$. Prints one
# record per settings line: <line>\t<key>\t<ok|invalid>\t<value-or-raw>.
# A missing file prints no record. <scope> is unused by the grammar
# itself; it names which file the caller is scanning.
scan_file() {
  file=$1
  scope=$2
  [ -f "$file" ] || return 0
  awk '
    BEGIN { infence = 0 }
    {
      line = $0
      if (line ~ /^```/) { infence = !infence; next }
      if (infence) next
      if (match(line, /^[a-z0-9-]+\.[a-z0-9.\/-]+:/)) {
        key = substr(line, 1, RLENGTH - 1)
        rest = substr(line, RLENGTH + 1)
        if (line ~ /^[a-z0-9-]+\.[a-z0-9.\/-]+:[ \t]*[A-Za-z0-9._\/-]+[ \t\r]*$/) {
          status = "ok"
        } else {
          status = "invalid"
        }
        val = rest
        sub(/^[ \t]+/, "", val)
        sub(/[ \t\r]+$/, "", val)
        if (status == "invalid" && val == "") val = "(empty)"
        printf "%d\t%s\t%s\t%s\n", NR, key, status, val
      }
    }
  ' "$file" || return 1
}

# resolve: reads TEAM/LOCAL settings against the registry and fills
# three globals: VALUE_LINES (one "<key>: <value>  [<source>]" line per
# registered key, registry order), TEAM_ERRORS and LOCAL_ERRORS (each
# file's "error: " lines, in that file's line order).
resolve() {
  team_records=$(scan_file "$TEAM" team) || return 1
  local_records=$(scan_file "$LOCAL" local) || return 1

  registry_summary=""
  for key in $keys; do
    rf_scope=$(registry_field "$key" scope) || return 1
    rf_values=$(registry_field "$key" values) || return 1
    rf_values_norm=$(printf '%s' "$rf_values" | sed 's/ | / /g') || return 1
    registry_summary="${registry_summary}${key}	${rf_scope}	${rf_values_norm}
"
  done

  AWK_ERR_PROG='
    BEGIN {
      n_reg = split(reg, reglines, "\n")
      for (ri = 1; ri <= n_reg; ri++) {
        if (reglines[ri] == "") continue
        split(reglines[ri], f, "\t")
        regscope[f[1]] = f[2]
        regvalues[f[1]] = " " f[3] " "
      }
    }
    function valid_value(val, padded,    needle) {
      needle = " " val " "
      return index(padded, needle) > 0
    }
    NF == 0 { next }
    {
      i = NR
      rn[i] = $1; rk[i] = $2; rs[i] = $3; rv[i] = $4
      total = i
      k = $2
      if (!(k in regscope)) next
      keyscope = regscope[k]
      if (role == "team") { is_deciding = (keyscope == "team") } else { is_deciding = (keyscope == "personal") }
      if (is_deciding) {
        dcount[k]++
        dlines[k] = (dlines[k] == "" ? $1 : dlines[k] "," $1)
      } else if (role == "team") {
        fcount[k]++
        flines[k] = (flines[k] == "" ? $1 : flines[k] "," $1)
      }
    }
    END {
      for (i = 1; i <= total; i++) {
        n = rn[i]; k = rk[i]; s = rs[i]; v = rv[i]
        if (!(k in regscope)) {
          printf "error: %s:%s unknown key `%s` \xe2\x80\x94 ignored\n", file_label, n, k
          continue
        }
        keyscope = regscope[k]
        if (role == "team") { is_deciding = (keyscope == "team") } else { is_deciding = (keyscope == "personal") }
        if (is_deciding) {
          if (k in demitted) continue
          demitted[k] = 1
          if (dcount[k] > 1) {
            printf "error: %s:%s duplicate key `%s` \xe2\x80\x94 unset\n", file_label, dlines[k], k
          } else if (s != "ok" || !valid_value(v, regvalues[k])) {
            printf "error: %s:%s invalid value for `%s`: %s \xe2\x80\x94 unset\n", file_label, n, k, v
          }
          continue
        }
        if (role == "local") {
          printf "error: %s:%s team key `%s` in the personal file \xe2\x80\x94 ignored\n", file_label, n, k
          continue
        }
        if (k in femitted) continue
        femitted[k] = 1
        if (fcount[k] > 1) {
          printf "error: %s:%s duplicate key `%s` \xe2\x80\x94 ignored\n", file_label, flines[k], k
        } else if (s != "ok" || !valid_value(v, regvalues[k])) {
          printf "error: %s:%s invalid value for `%s`: %s \xe2\x80\x94 ignored\n", file_label, n, k, v
        }
      }
    }
  '

  TEAM_ERRORS_RAW=$(printf '%s\n' "$team_records" | awk -F'\t' -v reg="$registry_summary" -v file_label=settings.md -v role=team "$AWK_ERR_PROG") || return 1
  LOCAL_ERRORS_RAW=$(printf '%s\n' "$local_records" | awk -F'\t' -v reg="$registry_summary" -v file_label=settings.local.md -v role=local "$AWK_ERR_PROG") || return 1
  TEAM_ERRORS=""
  if [ -n "$TEAM_ERRORS_RAW" ]; then TEAM_ERRORS="${TEAM_ERRORS_RAW}
"; fi
  LOCAL_ERRORS=""
  if [ -n "$LOCAL_ERRORS_RAW" ]; then LOCAL_ERRORS="${LOCAL_ERRORS_RAW}
"; fi

  VALUE_LINES=""
  dir_default_value=unset
  for key in $keys; do
    scope=$(registry_field "$key" scope) || return 1
    values=$(registry_field "$key" values) || return 1
    default=$(registry_field "$key" default) || return 1
    values_norm=$(printf '%s' "$values" | sed 's/ | / /g') || return 1

    if [ "$scope" = team ]; then
      deciding_matches=$(printf '%s\n' "$team_records" | awk -F'\t' -v k="$key" 'NF && $2==k') || return 1
    else
      deciding_matches=$(printf '%s\n' "$local_records" | awk -F'\t' -v k="$key" 'NF && $2==k') || return 1
    fi
    count=0
    if [ -n "$deciding_matches" ]; then
      count=$(printf '%s\n' "$deciding_matches" | awk 'END{print NR}') || return 1
    fi

    is_dir_exception=0
    case "$key" in
      dir.*) [ "$key" != "dir.default" ] && is_dir_exception=1 ;;
    esac

    if [ "$count" -eq 0 ]; then
      if [ "$is_dir_exception" -eq 1 ]; then
        value=$dir_default_value
        source=inherited
      else
        value=$default
        source=default
      fi
      if [ "$scope" = personal ] && [ "$value" = unset ]; then
        foreign_matches=$(printf '%s\n' "$team_records" | awk -F'\t' -v k="$key" 'NF && $2==k') || return 1
        fcount=0
        if [ -n "$foreign_matches" ]; then
          fcount=$(printf '%s\n' "$foreign_matches" | awk 'END{print NR}') || return 1
        fi
        if [ "$fcount" -eq 1 ]; then
          fstatus=$(printf '%s\n' "$foreign_matches" | awk -F'\t' '{print $3}') || return 1
          fvalue=$(printf '%s\n' "$foreign_matches" | awk -F'\t' '{print $4}') || return 1
          in_list=0
          for v in $values_norm; do
            [ "$v" = "$fvalue" ] && in_list=1
          done
          if [ "$fstatus" = ok ] && [ "$in_list" -eq 1 ]; then
            source="team suggests: $fvalue"
          fi
        fi
      fi
    elif [ "$count" -eq 1 ]; then
      status=$(printf '%s\n' "$deciding_matches" | awk -F'\t' '{print $3}') || return 1
      dval=$(printf '%s\n' "$deciding_matches" | awk -F'\t' '{print $4}') || return 1
      in_list=0
      for v in $values_norm; do
        [ "$v" = "$dval" ] && in_list=1
      done
      if [ "$status" = ok ] && [ "$in_list" -eq 1 ]; then
        value=$dval
        if [ "$scope" = team ]; then source=team; else source=local; fi
      else
        value=unset
        if [ "$scope" = team ]; then source="invalid in team"; else source="invalid in local"; fi
      fi
    else
      value=unset
      if [ "$scope" = team ]; then source="invalid in team"; else source="invalid in local"; fi
    fi

    if [ "$key" = dir.default ]; then
      dir_default_value=$value
    fi

    VALUE_LINES="${VALUE_LINES}${key}: ${value}  [${source}]
"
  done
}

# emit_block: the first line, then VALUE_LINES, then TEAM_ERRORS, then
# LOCAL_ERRORS. Nothing else, no blank lines.
emit_block() {
  team_label=$(basename "$TEAM")
  [ -f "$TEAM" ] || team_label="$team_label (absent)"
  local_label=$LOCAL_LABEL
  [ -f "$LOCAL" ] || local_label="$local_label (absent)"
  printf 'working-process settings (root: %s; loader: %s; team: %s; local: %s)\n' "$ROOT" "$LOADER" "$team_label" "$local_label"
  printf '%s' "$VALUE_LINES"
  printf '%s' "$TEAM_ERRORS"
  printf '%s' "$LOCAL_ERRORS"
}

# build_block: the body main runs (wrapped) in both modes. Assembles
# the whole block via printf and returns non-zero from each tool call
# it makes, so silence does not rest on `set -e` alone.
build_block() {
  find_root || return 1
  if [ ! -d "$DIR" ]; then
    if [ "$MODE" = print ]; then
      printf 'working-process settings (root: %s; loader: %s; no settings directory)\n' "$ROOT" "$LOADER" || return 1
    fi
    return 0
  fi
  [ -f "$REGISTRY" ] || die "registry not found or empty at $REGISTRY"
  keys=$(registry_keys) || return 1
  [ -n "$keys" ] || die "registry not found or empty at $REGISTRY"
  resolve || return 1
  emit_block || return 1
}

# cap_block: 4096 bytes over the whole output (hook mode only). At or
# under the cap the block passes through whole; otherwise whole lines
# are emitted while they fit alongside the reserved "incomplete:" line,
# which then closes the block, inside the 4096. The first line is
# always emitted.
cap_block() {
  printf '%s\n' "$1" | awk -v loader="$LOADER" '
    BEGIN { limit = 4096; inc = "incomplete: run " loader " --print"; inc_bytes = length(inc) + 1 }
    { lines[NR] = $0 }
    END {
      total = 0
      for (i = 1; i <= NR; i++) total += length(lines[i]) + 1
      if (total <= limit) {
        for (i = 1; i <= NR; i++) printf "%s\n", lines[i]
        exit 0
      }
      used = 0
      for (i = 1; i <= NR; i++) {
        lb = length(lines[i]) + 1
        if (i == 1) {
          printf "%s\n", lines[i]
          used += lb
          continue
        }
        if (used + lb + inc_bytes <= limit) {
          printf "%s\n", lines[i]
          used += lb
        } else {
          printf "%s\n", inc
          used += inc_bytes
          break
        }
      }
    }
  '
}

main() {
  case "${1-}" in
    "")
      if [ "$#" -gt 0 ]; then
        usage
        exit 2
      fi
      MODE=hook
      ;;
    --print)
      if [ "$#" -gt 1 ]; then
        usage
        exit 2
      fi
      MODE=print
      ;;
    *)
      usage
      exit 2
      ;;
  esac

  if [ "$MODE" = hook ]; then
    block=$(set -e; build_block 2>/dev/null)
    rc=$?
    if [ "$rc" -eq 0 ] && [ -n "$block" ]; then
      cap_block "$block"
    fi
    exit 0
  fi

  block=$(set -e; build_block)
  rc=$?
  if [ "$rc" -eq 0 ]; then
    printf '%s\n' "$block"
    exit 0
  fi
  echo "error: loader failed" >&2
  exit 1
}

main "$@"
