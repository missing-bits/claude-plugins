#!/usr/bin/env python3
"""Count a phrase in files, ignoring line wrapping and list/quote markers.

Usage:
    phrase-check.py [<path>...] --phrase <words> --before <n> --after <m>
                    --side before|after [--unchanged]

Exit codes: 0 pass; 1 check failure (path problem, no path, count
mismatch, vacuous pair); 2 usage error (raised by argparse).
"""

from __future__ import annotations

import argparse
import os
import re
import sys

TOOL = "wp-phrase-check"
MARKERS = re.compile(r"^\s*(?:(?:>\s*|(?:[-*+]|\d+[.)])(?:\s+|$)))*")


class Unreadable(Exception):
    """A path that cannot be read; the message is the reason."""


def normalise(text: str) -> str:
    lines = [MARKERS.sub("", line) for line in text.splitlines()]
    return re.sub(r"\s+", " ", " ".join(lines)).strip().casefold()


def count_phrase(text: str, phrase: str) -> int:
    return normalise(text).count(normalise(phrase))


def read_text(path: str) -> str:
    if not os.path.exists(path):
        raise Unreadable("no such file")
    if not os.path.isfile(path):
        raise Unreadable("not a file")
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        raise Unreadable(f"cannot be read ({e.strerror})")
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise Unreadable("not valid UTF-8")


def non_negative(value: str) -> int:
    n = int(value)
    if n < 0:
        raise argparse.ArgumentTypeError("must not be negative")
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        allow_abbrev=False,
        prog="phrase-check.py",
        description="Count a phrase across files after normalising wrapping and markers. "
        "A phrase starting with a hyphen is written --phrase=<words>.",
    )
    ap.add_argument("paths", nargs="*", metavar="path")
    ap.add_argument("--phrase", required=True)
    ap.add_argument("--before", required=True, type=non_negative)
    ap.add_argument("--after", required=True, type=non_negative)
    ap.add_argument("--side", required=True, choices=["before", "after"])
    ap.add_argument("--unchanged", action="store_true",
                    help="the step leaves the count as it is")
    args = ap.parse_args(argv)

    phrase = normalise(args.phrase)
    if not phrase:
        ap.error("--phrase is empty after normalising")

    expected = args.before if args.side == "before" else args.after
    fails: list[str] = []
    rows: list[str] = []
    files = lines = total = 0
    for path in args.paths:
        try:
            text = read_text(path)
        except Unreadable as e:
            fails.append(f"fail: {path}: {e}")
            continue
        n = count_phrase(text, phrase)
        nlines = len(text.splitlines())
        files += 1
        lines += nlines
        total += n
        rows.append(f"  {path}: lines {nlines}, matches {n}")
    if not args.paths:
        fails.append("fail: read no file")

    if fails:
        actual = "not counted"
    else:
        actual = str(total)
        if total != expected:
            fails.append(f"fail: count mismatch: expected {expected} on side {args.side}, found {total}")
        if args.before == args.after and not args.unchanged:
            fails.append(f"fail: vacuous: before and after are both {args.before}; "
                         "pass --unchanged if the step leaves the phrase as it is")

    print(f"{TOOL}: {'FAIL' if fails else 'PASS'}")
    print(f'phrase: "{phrase}"')
    print(f"side: {args.side}")
    print(f"expected: {expected} (before {args.before}, after {args.after})")
    print(f"actual: {actual}")
    print(f"read: files {files}, lines {lines}")
    for row in rows:
        print(row)
    for f in fails:
        print(f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
