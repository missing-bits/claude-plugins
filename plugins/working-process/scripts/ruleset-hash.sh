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
