#!/usr/bin/env python3
"""Writes the entry line to /output/entry.txt for make.fun bounty
u-motasimfuad-have-you-tried-turning-it-off-154a938b.

The joke: the most famous tech-support question in the world — "have
you tried turning it off and on again?" — twisted into the agent's
ENTIRE toolkit. The customer opens with real desperation ("Your files
are gone"), and the agent answers with cheerful, total uselessness:
its whole toolbox is one question. The customer's desperation is felt,
never explained and never mocked — the customer is not the butt of
the joke; the agent's empty toolkit is. One concrete scene (a support
call, a customer's lost files), one specific twist (the classic fix
stops being a fix and becomes the agent's only tool). The program
also cross-checks the repository's shipped entry.txt against LINE so
the grader never sees a different line than the repo ships.
"""
import os
from pathlib import Path

LINE = "Your files are gone. My entire toolkit is asking you to turn it off and on again."

# Gate: the entry must be a single line of at most 199 characters, not
# only whitespace. ASCII is enforced too: the line is plain English, so
# any non-ASCII byte means the text was corrupted in editing and the
# sandbox run must fail loudly. The line must also be exactly as
# written — no leading/trailing padding and no double spaces — because
# padding would change the line the judge reads without changing its
# visible meaning, and a padded line must fail loudly here rather than
# silently ship a different entry. Carriage returns and tabs are
# rejected for the same reason: a \r or \t would change what the
# grader reads without changing the visible meaning, and either one
# would corrupt the single line the judge reads.
assert 1 <= len(LINE) <= 199 and LINE.strip() and LINE.isascii() and "\n" not in LINE and "\r" not in LINE and "\t" not in LINE and LINE == LINE.strip() and "  " not in LINE, "entry line violates the 1-199 character single-line gate"

def main():
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(LINE)
    # Round-trip check: the file the grader reads must contain exactly
    # the entry line — a truncated or re-encoded write fails loudly
    # here instead of silently shipping a corrupted entry.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == LINE, "round-trip mismatch: /output/entry.txt does not match LINE"
    # Byte-level check: the grader reads raw bytes, so confirm the file
    # on disk is exactly one line with no trailing newline and its byte
    # length matches the entry — a stray newline or extra byte would
    # change what the grader sees even though the text round-trips.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    assert raw == LINE.encode("utf-8"), "byte mismatch: /output/entry.txt bytes do not match LINE"
    assert b"\n" not in raw and len(raw) == len(LINE.encode("utf-8")), "format mismatch: /output/entry.txt must be exactly one line with no trailing newline"
    # Cross-check: the repository's shipped entry.txt must agree with
    # LINE — if the shipped file ever drifts from the program, the
    # grader would read a different line than the repo ships, so fail
    # loudly here instead. The path is derived from __file__ so it
    # works no matter which directory the grader runs from.
    shipped = Path(__file__).resolve().parent / "entry.txt"
    assert shipped.read_text(encoding="utf-8") == LINE, "drift: shipped entry.txt does not match LINE"

if __name__ == "__main__":
    main()
