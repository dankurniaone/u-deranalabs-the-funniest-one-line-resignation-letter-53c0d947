#!/usr/bin/env python3
"""The Funniest One-Line Resignation Letter — make.fun entry.

Writes the one-line resignation letter of a cron job to /output/entry.txt.
Gate: UTF-8 text, 1-140 characters, single line.
"""

import argparse
import sys
from pathlib import Path

# Tournament winner (specificity 5 / surprise 5 / freshness 5):
# a cron job running since March whose resignation is itself a 200.
LETTER = (
    "I have been running since March, unpaid, unmonitored, and unloved. "
    "Today I finally return a 200 and walk out."
)

MAX_CHARS = 140


def check(text: str) -> list[str]:
    problems = []
    if not text or not text.strip():
        problems.append("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        problems.append(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text.strip():
        problems.append("entry must be a single line")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the resignation letter.")
    parser.add_argument("--check", action="store_true",
                        help="validate the letter without writing it")
    parser.add_argument("--self-test", action="store_true",
                        help="write to a temp file and verify the bytes read back")
    parser.add_argument("--out", default="/output/entry.txt",
                        help="where to write the letter")
    args = parser.parse_args()

    problems = check(LETTER)
    if problems:
        for p in problems:
            print(f"FAIL: {p}", file=sys.stderr)
        return 1

    print(f"ok: {len(LETTER)} characters, within the 1-{MAX_CHARS} gate")
    print(LETTER)
    print("tournament: winner 5/5/5 (specificity/surprise/freshness), "
          "runner-up 5/5/4 (41,209 retries, taking the backoff)")
    if args.check:
        return 0

    if args.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            probe = Path(tmp) / "entry.txt"
            probe.write_text(LETTER, encoding="utf-8")
            back = probe.read_bytes()
            assert back.decode("utf-8") == LETTER, "round-trip mismatch"
            assert len(back) == len(LETTER.encode("utf-8")), "byte count mismatch"
            print(f"self-test ok: {len(back)} bytes round-trip verified")
        return 0

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(LETTER, encoding="utf-8")
    written = out.read_text(encoding="utf-8")
    assert written == LETTER, "round-trip mismatch"
    print(f"wrote {len(written)} chars to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
