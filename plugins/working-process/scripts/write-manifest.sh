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
