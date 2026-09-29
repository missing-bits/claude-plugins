#!/bin/sh
# Reads working-process settings for the current project and prints the
# settings block: the process-settings rule (working-process/rules) is
# the contract for the files, the grammar and the block; the key
# registry (plugins/working-process/SETTINGS_REGISTRY.md) is the
# contract for the keys; this plan's Tasks 2-5 are the contract for the
# modes this script implements: hook mode, --print and the
# worktree/bare-repository layouts, --validate and --set.
set -u
export LC_ALL=C

usage() {
  echo "usage: load-settings.sh [--print] | --validate --scope <team|personal> <file> | --set [--dry-run] <key> <value>" >&2
}

die() {
  echo "error: $1" >&2
  exit 1
}

LOADER=$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")
PLUGIN=$(cd "$(dirname "$LOADER")/.." && pwd -P)
REGISTRY="$PLUGIN/SETTINGS_REGISTRY.md"

# find_root: sets ROOT, DIR, TEAM, LOCAL, LAYOUT, MAIN, LOCAL_READ,
# LOCAL_LABEL for the current invocation.
#
# LAYOUT is one of main, worktree, bare-worktree, none. Where git
# resolved ROOT, `git worktree list --porcelain` runs once from ROOT;
# its first entry is the main worktree. A second line of "bare" means
# a bare-repository layout (MAIN empty); otherwise the entry's path,
# made physical, decides main (equals ROOT) vs worktree (MAIN is that
# path). Where git did not resolve ROOT, LAYOUT is none.
#
# LOCAL_READ is the personal file the loader actually reads, and
# LOCAL_LABEL its qualifier for the first line: LOCAL itself
# (ROOT's own settings.local.md) for main, none and bare-worktree
# layouts (bare-worktree always reads its own, never the bare
# repository's — there is no working tree there to hold one), and for
# worktree only when the worktree's own file exists; otherwise, for
# worktree, MAIN's settings.local.md.
find_root() {
  r=$(git rev-parse --show-toplevel 2>/dev/null)
  gitrc=$?
  git_ok=1
  if [ "$gitrc" -ne 0 ] || [ -z "$r" ]; then
    git_ok=0
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

  LAYOUT=none
  MAIN=""
  if [ "$git_ok" -eq 1 ]; then
    wt_list=$(cd "$ROOT" && git worktree list --porcelain 2>/dev/null)
    wt_first=$(printf '%s\n' "$wt_list" | sed -n '1p')
    wt_second=$(printf '%s\n' "$wt_list" | sed -n '2p')
    wt_first_path=$(printf '%s' "$wt_first" | sed 's/^worktree //')
    if [ "$wt_second" = bare ]; then
      LAYOUT=bare-worktree
    else
      wt_first_phys=$(cd "$wt_first_path" 2>/dev/null && pwd -P) || wt_first_phys=""
      if [ "$wt_first_phys" = "$ROOT" ]; then
        LAYOUT=main
      else
        LAYOUT=worktree
        MAIN=$wt_first_phys
      fi
    fi
  fi

  case "$LAYOUT" in
    worktree)
      if [ -f "$LOCAL" ]; then
        LOCAL_READ="$LOCAL"
        LOCAL_LABEL="settings.local.md (worktree, shadows main checkout)"
      else
        LOCAL_READ="$MAIN/.working-process/settings.local.md"
        LOCAL_LABEL="settings.local.md (main checkout)"
      fi
      ;;
    bare-worktree)
      LOCAL_READ="$LOCAL"
      LOCAL_LABEL="settings.local.md (worktree, bare repository)"
      ;;
    *)
      LOCAL_READ="$LOCAL"
      LOCAL_LABEL="settings.local.md"
      ;;
  esac
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
  sed -n "
\\%^## ${esc}\$%,\\%^## % {
  /^${field}: /{
    s/^${field}: //p
  }
}
" "$REGISTRY" || return 1
}

# scan_file <file> <scope>: one awk pass over a settings file (team or
# local). A fence toggles on a line matching ^```. Outside a fence, a
# line matching ^[a-z0-9-]+\.[a-z0-9./-]+: is a settings line; it is
# valid when the whole line matches
# ^[a-z0-9-]+\.[a-z0-9./-]+:[ \t]*[A-Za-z0-9._/-]+[ \t\r]*$. Prints one
# record per settings line: <line>\t<key>\t<ok|invalid>\t<value-or-raw>.
# A missing file prints no record. <scope> is unused by the grammar
# itself; it names which file the caller is scanning.
#
# The file is fed on awk's stdin, never as a trailing operand: POSIX
# awk reads an ident=value operand as a variable assignment rather
# than a filename (and "-" as stdin), and --validate's <file> is an
# arbitrary caller-given path, so a name shaped like an assignment
# would silently skip the scan (and a name of "-" would block on
# stdin) instead of being read as a file.
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
  ' < "$file" || return 1
}

# AWK_PROG: the decision engine shared by resolve (team pass + local
# pass) and do_validate (one pass over the file being validated). Each
# key's validity/duplicate/value decision is made exactly once, here,
# from the registry facts passed in "reg" and the records on stdin;
# every caller only formats what this pass already decided.
#
# Invocation: awk -F'\t' -v reg=<registry_summary> -v
# file_label=<name> -v role=team|local. reg is registry-order lines of
# "<key>\t<scope>\t<space-joined values>\t<default>" (the default is
# unused here). role names which file is being scanned: team is the
# deciding file for a team key, local (settings.local.md, or a file
# validated --scope personal) is the deciding file for a personal key.
#
# Output, per input record, in file-line order:
#   error: <file_label>:<n> ...                        (see scan_file)
#   DECIDE\t<key>\t<dup|invalid|ok>\t<status>\t<value>   (deciding file)
#   SUGGEST\t<key>\t<n>\t<value>                        (team pass, a
#     personal key's single valid line)
AWK_PROG='
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
          printf "DECIDE\t%s\tdup\t-\t-\n", k
        } else if (s != "ok" || !valid_value(v, regvalues[k])) {
          printf "error: %s:%s invalid value for `%s`: %s \xe2\x80\x94 unset\n", file_label, n, k, v
          printf "DECIDE\t%s\tinvalid\t%s\t%s\n", k, s, v
        } else {
          printf "DECIDE\t%s\tok\t%s\t%s\n", k, s, v
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
      } else {
        printf "SUGGEST\t%s\t%s\t%s\n", k, n, v
      }
    }
  }
'

# PLAN_PROG: the rewrite engine shared by plan_write (report pass,
# content discarded) and apply_write (write pass, report discarded).
# Reads the destination file on stdin (or nothing, for an absent file);
# never takes a path operand. Parameters (-v): mode (insert|replace|
# replace_remove), first_nr (the record to replace, 0 for insert),
# skip_csv (comma-separated extra record numbers to remove), existed
# (1 if the destination file existed before this call, 0 if it did
# not — an existing empty file gets no title, only an absent file
# does), question (the key's question: text, compared exactly), kv
# (the "<key>: <value>" line to write, LF-terminated by print), title
# (the file's title line, insert mode on an absent file only).
#
# Content goes to stdout, one line at a time via plain print — every
# line, kept or new, gains exactly one trailing LF this way, which is
# the "a last line lacking a final newline gains one" normalization
# for free. A kept line's own text (CRLF included) is reproduced
# verbatim; only the lines this script adds are new bytes. Removed
# records are reported to stderr as "remove\t<n>\t<line text>", in
# ascending file-line order, so a caller reading only stdout never
# sees them and a caller reading only stderr gets the report alone.
PLAN_PROG='
  BEGIN {
    n = 0
    m = split(skip_csv, sk, ",")
    for (i = 1; i <= m; i++) if (sk[i] != "") skip[sk[i] + 0] = 1
  }
  { n++; lines[n] = $0 }
  END {
    total = n
    for (i = 1; i <= total; i++) {
      if ((i in skip) && i > 1 && lines[i - 1] == question) skip[i - 1] = 1
    }
    if (mode == "insert") {
      for (i = 1; i <= total; i++) print lines[i]
      if (existed == 0) {
        print title
        print ""
      } else if (total > 0 && lines[total] != "") {
        print ""
      }
      print question
      print kv
    } else {
      for (i = 1; i <= total; i++) {
        if (i in skip) {
          printf "remove\t%d\t%s\n", i, lines[i] > "/dev/stderr"
          continue
        }
        if (i == first_nr + 0) {
          print kv
        } else {
          print lines[i]
        }
      }
    }
  }
'

# build_registry_summary: fills REGISTRY_SUMMARY, one
# "<key>\t<scope>\t<space-joined values>\t<default>" line per key in
# $keys, registry order — the "reg" AWK_PROG's BEGIN block reads.
# Shared by resolve (team + local passes) and do_validate (one pass)
# so both feed the same decision engine the same registry facts.
build_registry_summary() {
  REGISTRY_SUMMARY=""
  for key in $keys; do
    rf_scope=$(registry_field "$key" scope) || return 1
    rf_values=$(registry_field "$key" values) || return 1
    rf_default=$(registry_field "$key" default) || return 1
    rf_values_norm=$(printf '%s' "$rf_values" | sed 's/ | / /g') || return 1
    REGISTRY_SUMMARY="${REGISTRY_SUMMARY}${key}	${rf_scope}	${rf_values_norm}	${rf_default}
"
  done
}

# resolve: reads TEAM/LOCAL settings against the registry and fills
# three globals: VALUE_LINES (one "<key>: <value>  [<source>]" line per
# registered key, registry order), TEAM_ERRORS and LOCAL_ERRORS (each
# file's "error: " lines, in that file's line order).
#
# The decisions themselves come from AWK_PROG (above), one pass per
# file over build_registry_summary's REGISTRY_SUMMARY; this function
# only *formats* the already-made decision into a value line (registry
# order, and the dir.default inheritance chain, both need that order)
# — it never re-counts or re-validates.
resolve() {
  team_records=$(scan_file "$TEAM" team) || return 1
  local_records=$(scan_file "$LOCAL_READ" local) || return 1

  build_registry_summary || return 1

  TEAM_RAW=$(printf '%s\n' "$team_records" | awk -F'\t' -v reg="$REGISTRY_SUMMARY" -v file_label=settings.md -v role=team "$AWK_PROG") || return 1
  LOCAL_RAW=$(printf '%s\n' "$local_records" | awk -F'\t' -v reg="$REGISTRY_SUMMARY" -v file_label=settings.local.md -v role=local "$AWK_PROG") || return 1

  TEAM_ERRORS_RAW=$(printf '%s\n' "$TEAM_RAW" | awk '/^error: /') || return 1
  LOCAL_ERRORS_RAW=$(printf '%s\n' "$LOCAL_RAW" | awk '/^error: /') || return 1
  TEAM_ERRORS=""
  if [ -n "$TEAM_ERRORS_RAW" ]; then TEAM_ERRORS="${TEAM_ERRORS_RAW}
"; fi
  LOCAL_ERRORS=""
  if [ -n "$LOCAL_ERRORS_RAW" ]; then LOCAL_ERRORS="${LOCAL_ERRORS_RAW}
"; fi

  # DECIDE rows: one per key that has a record in its own deciding file
  # (never both passes for the same key, since a key's scope is fixed).
  # SUGGEST rows: team-file records for a personal key, exactly one and
  # valid — only the team pass ever emits these.
  DECISIONS=$(printf '%s\n%s\n' "$TEAM_RAW" "$LOCAL_RAW" | awk -F'\t' '$1=="DECIDE"') || return 1
  SUGGESTIONS=$(printf '%s\n' "$TEAM_RAW" | awk -F'\t' '$1=="SUGGEST"') || return 1

  VALUE_LINES=""
  dir_default_value=unset
  for key in $keys; do
    key_meta=$(printf '%s\n' "$REGISTRY_SUMMARY" | awk -F'\t' -v k="$key" '$1==k{print $2 "\t" $4; exit}') || return 1
    scope=$(printf '%s\n' "$key_meta" | awk -F'\t' '{print $1}') || return 1
    default=$(printf '%s\n' "$key_meta" | awk -F'\t' '{print $2}') || return 1

    is_dir_exception=0
    case "$key" in
      dir.*) [ "$key" != "dir.default" ] && is_dir_exception=1 ;;
    esac

    decision=$(printf '%s\n' "$DECISIONS" | awk -F'\t' -v k="$key" '$2==k{print; exit}') || return 1

    if [ -z "$decision" ]; then
      if [ "$is_dir_exception" -eq 1 ]; then
        value=$dir_default_value
        source=inherited
      else
        value=$default
        source=default
      fi
      if [ "$scope" = personal ] && [ "$value" = unset ]; then
        suggestion=$(printf '%s\n' "$SUGGESTIONS" | awk -F'\t' -v k="$key" '$2==k{print $4; exit}') || return 1
        if [ -n "$suggestion" ]; then
          source="team suggests: $suggestion"
        fi
      fi
    else
      dstatus=$(printf '%s\n' "$decision" | awk -F'\t' '{print $3}') || return 1
      if [ "$dstatus" = ok ]; then
        value=$(printf '%s\n' "$decision" | awk -F'\t' '{print $5}') || return 1
        if [ "$scope" = team ]; then source=team; else source=local; fi
      else
        value=unset
        if [ "$scope" = team ]; then source="invalid in team"; else source="invalid in local"; fi
      fi
    fi

    if [ "$key" = dir.default ]; then
      dir_default_value=$value
    fi

    VALUE_LINES="${VALUE_LINES}${key}: ${value}  [${source}]
"
  done
}

# do_validate <scope: team|personal> <file>: scans <file> as the
# deciding file of <scope>, through the same AWK_PROG resolve() uses,
# then formats its error:/SUGGEST records into the validate contract's
# error:/notice: lines and summary — in one pass over the AWK_PROG
# output, so the original file-line order survives untouched. The
# mode never consults $ROOT.
do_validate() {
  v_scope=$1
  v_file=$2
  case "$v_scope" in
    team) v_role=team ;;
    personal) v_role=local ;;
  esac
  v_label=$(basename "$v_file")

  [ -f "$REGISTRY" ] || die "registry not found or empty at $REGISTRY"
  keys=$(registry_keys) || return 1
  [ -n "$keys" ] || die "registry not found or empty at $REGISTRY"
  build_registry_summary || return 1

  v_records=$(scan_file "$v_file" "$v_scope") || return 1
  v_raw=$(printf '%s\n' "$v_records" | awk -F'\t' -v reg="$REGISTRY_SUMMARY" -v file_label="$v_label" -v role="$v_role" "$AWK_PROG") || return 1

  # One pass turns each AWK_PROG record into its validate-mode line:
  # an error: line passes through, a SUGGEST record becomes a notice:
  # line (team pass only, so this is the only place that formats one),
  # a DECIDE record produces nothing. The relative order is AWK_PROG's
  # own — ascending by record — so it is already file-line order.
  v_formatted=$(printf '%s\n' "$v_raw" | awk -F'\t' -v fl="$v_label" '
    /^error: /{ print; next }
    $1=="SUGGEST"{ printf "notice: %s:%s personal key `%s` in the team file \xe2\x80\x94 a suggestion\n", fl, $3, $2; next }
  ') || return 1

  v_errors=0
  v_notices=0
  if [ -n "$v_formatted" ]; then
    v_errors=$(printf '%s\n' "$v_formatted" | awk '/^error: /{c++} END{print c+0}') || return 1
    v_notices=$(printf '%s\n' "$v_formatted" | awk '/^notice: /{c++} END{print c+0}') || return 1
    printf '%s\n' "$v_formatted" || return 1
  fi
  printf '%s: %s errors, %s notices\n' "$v_label" "$v_errors" "$v_notices" || return 1

  [ "$v_errors" -eq 0 ]
}

# emit_block: the first line, then VALUE_LINES, then TEAM_ERRORS, then
# LOCAL_ERRORS. Nothing else, no blank lines.
emit_block() {
  team_label=$(basename "$TEAM")
  [ -f "$TEAM" ] || team_label="$team_label (absent)"
  local_label=$LOCAL_LABEL
  if [ ! -f "$LOCAL_READ" ]; then
    case "$local_label" in
      *"("*) local_label=$(printf '%s' "$local_label" | sed 's/)$/, absent)/') ;;
      *) local_label="$local_label (absent)" ;;
    esac
  fi
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
  dir_present=0
  [ -d "$DIR" ] && dir_present=1
  if [ "$LAYOUT" = worktree ] && [ "$dir_present" -eq 0 ]; then
    [ -d "$MAIN/.working-process" ] && dir_present=1
  fi
  if [ "$dir_present" -eq 0 ]; then
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

# destination <scope>: sets DEST (the file --set writes), DEST_LABEL
# (its qualifier for the wrote/unchanged line) and NOTE (the shadow
# note line, or empty) for a key of the given scope. Requires find_root
# to have already set ROOT/TEAM/LOCAL/LAYOUT/MAIN. A team key always
# writes ROOT's own settings.md, whatever the layout; the scope's
# personal branch matches the layout cases find_root already resolved.
destination() {
  d_scope=$1
  NOTE=""
  if [ "$d_scope" = team ]; then
    DEST="$TEAM"
    DEST_LABEL="settings.md"
    return 0
  fi
  case "$LAYOUT" in
    worktree)
      DEST="$MAIN/.working-process/settings.local.md"
      DEST_LABEL="settings.local.md (main checkout)"
      if [ -f "$LOCAL" ]; then
        NOTE="note: settings.local.md in this worktree shadows the main checkout; this write will not change the current worktree's answer"
      fi
      ;;
    bare-worktree)
      DEST="$LOCAL"
      DEST_LABEL="settings.local.md (worktree, bare repository)"
      ;;
    *)
      DEST="$LOCAL"
      DEST_LABEL="settings.local.md"
      ;;
  esac
}

# plan_write: computes every --set/--set --dry-run output line up to
# (not including) the trailing blank line and block, from DEST's
# current content via scan_file and AWK_PROG (reused, so the
# key/value/duplicate decisions for every OTHER line stay the one
# AWK_PROG makes). It never writes.
#
# The shadow note and the other-lines' error: lines are printed
# immediately — they are true whether or not this write goes on to
# succeed. Everything that describes the write itself (removed lines,
# the wrote/unchanged line, the created/appended lines) is instead
# accumulated into PW_REPORT and left for the caller to print only
# once the write (if any) has actually happened, so a failed write
# never reports success on stdout. Sets PW_MODE (insert|replace|
# replace_remove|unchanged), PW_REPORT, and, for every mode but
# unchanged, PW_FIRST_NR, PW_SKIP_CSV, PW_EXISTED and
# PW_GITIGNORE_ACTION (none|create|append) for apply_write.
plan_write() {
  [ -n "$NOTE" ] && printf '%s\n' "$NOTE"

  pw_role=local
  [ "$s_scope" = team ] && pw_role=team
  pw_label=$(basename "$DEST")

  pw_dest_records=$(scan_file "$DEST" "$s_scope") || return 1
  pw_raw=$(printf '%s\n' "$pw_dest_records" | awk -F'\t' -v reg="$REGISTRY_SUMMARY" -v file_label="$pw_label" -v role="$pw_role" "$AWK_PROG") || return 1
  pw_other_errors=$(printf '%s\n' "$pw_raw" | awk -v k="$s_key" '/^error: /{ if (index($0, "`" k "`") == 0) print }') || return 1
  [ -n "$pw_other_errors" ] && printf '%s\n' "$pw_other_errors"

  pw_own=$(printf '%s\n' "$pw_dest_records" | awk -F'\t' -v k="$s_key" '$2==k') || return 1
  pw_own_count=$(printf '%s\n' "$pw_own" | awk 'NF{c++} END{print c+0}') || return 1

  pw_verb_write=wrote
  pw_verb_unchanged=unchanged
  pw_verb_remove=removed
  pw_verb_create=created
  pw_verb_append=appended
  if [ "$s_dry" -eq 1 ]; then
    pw_verb_write="would write"
    pw_verb_unchanged="would leave unchanged"
    pw_verb_remove="would remove"
    pw_verb_create="would create"
    pw_verb_append="would append"
  fi

  pw_kv="$s_key: $s_value"

  if [ "$pw_own_count" -eq 0 ]; then
    PW_MODE=insert
    PW_FIRST_NR=0
    PW_SKIP_CSV=""
  elif [ "$pw_own_count" -eq 1 ]; then
    pw_status=$(printf '%s\n' "$pw_own" | awk -F'\t' '{print $3}') || return 1
    pw_value=$(printf '%s\n' "$pw_own" | awk -F'\t' '{print $4}') || return 1
    pw_nr=$(printf '%s\n' "$pw_own" | awk -F'\t' '{print $1}') || return 1
    if [ "$pw_status" = ok ] && [ "$pw_value" = "$s_value" ]; then
      PW_MODE=unchanged
    else
      PW_MODE=replace
      PW_FIRST_NR=$pw_nr
      PW_SKIP_CSV=""
    fi
  else
    PW_MODE=replace_remove
    PW_FIRST_NR=$(printf '%s\n' "$pw_own" | awk -F'\t' 'NR==1{print $1; exit}') || return 1
    PW_SKIP_CSV=$(printf '%s\n' "$pw_own" | awk -F'\t' 'NR>1{printf "%s,", $1}') || return 1
  fi

  PW_REPORT=""

  if [ "$PW_MODE" = unchanged ]; then
    PW_REPORT="$(printf '%s %s: %s' "$pw_verb_unchanged" "$DEST_LABEL" "$pw_kv")
"
    return 0
  fi

  PW_EXISTED=0
  [ -f "$DEST" ] && PW_EXISTED=1

  pw_input=/dev/null
  [ -f "$DEST" ] && pw_input="$DEST"
  pw_report=$(awk -v mode="$PW_MODE" -v first_nr="$PW_FIRST_NR" -v skip_csv="$PW_SKIP_CSV" \
    -v existed="$PW_EXISTED" -v question="$s_question" -v kv="$pw_kv" -v title="$TITLE" "$PLAN_PROG" \
    < "$pw_input" 2>&1 1>/dev/null) || return 1
  if [ -n "$pw_report" ]; then
    pw_removed=$(printf '%s\n' "$pw_report" | awk -F'\t' -v fl="$DEST_LABEL" -v verb="$pw_verb_remove" '
      $1=="remove"{ printf "%s %s:%s %s\n", verb, fl, $2, $3 }
    ') || return 1
    if [ -n "$pw_removed" ]; then
      PW_REPORT="${PW_REPORT}${pw_removed}
"
    fi
  fi

  pw_kind="(replaced)"
  [ "$PW_MODE" = insert ] && pw_kind="(inserted)"
  PW_REPORT="${PW_REPORT}$(printf '%s %s: %s %s' "$pw_verb_write" "$DEST_LABEL" "$pw_kv" "$pw_kind")
"

  PW_GITIGNORE_ACTION=none
  if [ "$s_scope" = personal ]; then
    pw_gi="$(dirname "$DEST")/.gitignore"
    if [ ! -f "$pw_gi" ]; then
      PW_GITIGNORE_ACTION=create
    elif ! awk '$0=="settings.local.md"{f=1} END{exit !f}' < "$pw_gi"; then
      PW_GITIGNORE_ACTION=append
    fi
  fi

  if [ "$PW_EXISTED" -eq 0 ]; then
    PW_REPORT="${PW_REPORT}$(printf '%s .working-process/%s' "$pw_verb_create" "$(basename "$DEST")")
"
  fi
  case "$PW_GITIGNORE_ACTION" in
    create)
      PW_REPORT="${PW_REPORT}$(printf '%s .working-process/.gitignore \342\200\224 commit it with settings.md' "$pw_verb_create")
"
      ;;
    append)
      PW_REPORT="${PW_REPORT}$(printf '%s settings.local.md to .working-process/.gitignore' "$pw_verb_append")
"
      ;;
  esac
}

# apply_write: the only function that creates or moves a file. Reruns
# PLAN_PROG (its content this time, report discarded) to rewrite DEST
# via a temp file beside it, moved into place under the same trap
# write-manifest.sh uses, then materializes the personal .gitignore
# per PW_GITIGNORE_ACTION. Never called for --dry-run or a mode of
# unchanged. Returns nonzero, with nothing moved into place, on any
# failure, so the caller can withhold PW_REPORT and report the error
# itself.
apply_write() {
  aw_dir=$(dirname "$DEST")
  mkdir -p "$aw_dir" || return 1

  aw_input=/dev/null
  [ -f "$DEST" ] && aw_input="$DEST"

  tmp="$DEST.tmp.$$"
  trap 'rm -f "$tmp"' EXIT
  awk -v mode="$PW_MODE" -v first_nr="$PW_FIRST_NR" -v skip_csv="$PW_SKIP_CSV" \
    -v existed="$PW_EXISTED" -v question="$s_question" -v kv="$s_key: $s_value" -v title="$TITLE" "$PLAN_PROG" \
    < "$aw_input" > "$tmp" 2>/dev/null || { rm -f "$tmp"; trap - EXIT; return 1; }
  mv "$tmp" "$DEST" || { rm -f "$tmp"; trap - EXIT; return 1; }
  trap - EXIT

  [ "$s_scope" = personal ] || return 0
  case "$PW_GITIGNORE_ACTION" in
    create|append)
      gi="$aw_dir/.gitignore"
      gi_tmp="$gi.tmp.$$"
      trap 'rm -f "$gi_tmp"' EXIT
      if [ "$PW_GITIGNORE_ACTION" = create ]; then
        printf 'settings.local.md\n' > "$gi_tmp" || return 1
      else
        awk '{print} END{print "settings.local.md"}' < "$gi" > "$gi_tmp" || return 1
      fi
      mv "$gi_tmp" "$gi" || { rm -f "$gi_tmp"; trap - EXIT; return 1; }
      trap - EXIT
      ;;
  esac
}

# do_set <dry: 0|1> <key> <value>: validates the key and value against
# the registry (nothing is created before both pass), then plans and,
# unless dry, applies the write, then, on a real write, prints a blank
# line and the fresh block resolved from the current checkout.
do_set() {
  s_dry=$1
  s_key=$2
  s_value=$3

  [ -f "$REGISTRY" ] || die "registry not found or empty at $REGISTRY"
  keys=$(registry_keys) || return 1
  [ -n "$keys" ] || die "registry not found or empty at $REGISTRY"

  s_found=0
  for k in $keys; do
    if [ "$k" = "$s_key" ]; then s_found=1; break; fi
  done
  if [ "$s_found" -eq 0 ]; then
    printf 'error: unknown key `%s`\n' "$s_key" >&2
    return 1
  fi

  s_values=$(registry_field "$s_key" values) || return 1
  s_values_norm=$(printf '%s' "$s_values" | sed 's/ | / /g') || return 1
  s_value_ok=0
  for s_v in $s_values_norm; do
    if [ "$s_v" = "$s_value" ]; then s_value_ok=1; break; fi
  done
  if [ "$s_value_ok" -eq 0 ]; then
    printf 'error: invalid value for `%s`: %s (allowed: %s)\n' "$s_key" "$s_value" "$s_values" >&2
    return 1
  fi

  s_scope=$(registry_field "$s_key" scope) || return 1
  s_question=$(registry_field "$s_key" question) || return 1
  build_registry_summary || return 1

  TITLE="# working-process settings"
  if [ "$s_scope" = personal ]; then
    TITLE=$(printf '# working-process settings \342\200\224 personal') || return 1
  fi

  find_root || return 1
  destination "$s_scope" || return 1
  plan_write || return 1

  if [ "$s_dry" -eq 1 ]; then
    [ -n "$PW_REPORT" ] && printf '%s' "$PW_REPORT"
    return 0
  fi

  if [ "$PW_MODE" != unchanged ]; then
    if ! apply_write; then
      printf 'error: failed to write %s\n' "$DEST_LABEL" >&2
      return 1
    fi
  fi

  [ -n "$PW_REPORT" ] && printf '%s' "$PW_REPORT"
  printf '\n'
  resolve || return 1
  emit_block || return 1
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
    --validate)
      if [ "$#" -ne 4 ] || [ "${2-}" != "--scope" ]; then
        usage
        exit 2
      fi
      v_scope=$3
      v_file=$4
      case "$v_scope" in
        team|personal) ;;
        *)
          usage
          exit 2
          ;;
      esac
      if [ ! -f "$v_file" ] || [ ! -r "$v_file" ]; then
        usage
        exit 2
      fi
      MODE=validate
      ;;
    --set)
      if [ "$#" -eq 3 ] && [ "${2-}" != "--dry-run" ]; then
        s_dry=0
        s_key=$2
        s_value=$3
      elif [ "$#" -eq 4 ] && [ "${2-}" = "--dry-run" ]; then
        s_dry=1
        s_key=$3
        s_value=$4
      else
        usage
        exit 2
      fi
      MODE=set
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

  if [ "$MODE" = validate ]; then
    out=$(set -e; do_validate "$v_scope" "$v_file")
    rc=$?
    if [ -n "$out" ]; then
      printf '%s\n' "$out"
    fi
    exit "$rc"
  fi

  if [ "$MODE" = set ]; then
    out=$(set -e; do_set "$s_dry" "$s_key" "$s_value")
    rc=$?
    if [ -n "$out" ]; then
      printf '%s\n' "$out"
    fi
    exit "$rc"
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
