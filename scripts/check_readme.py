#!/usr/bin/env python3
"""Check the hand-maintained counts and tables in README.md."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


text = README.read_text(encoding="utf-8")
lines = text.splitlines()

timeline_start = text.index("## Chronological Blog Timeline")
timeline_end = text.index("\n---", timeline_start)
timeline_lines = [
    line for line in text[timeline_start:timeline_end].splitlines()
    if re.match(r"^\| \d{4}-\d{2}-\d{2} \|", line)
]

dates = [date.fromisoformat(line.split("|")[1].strip()) for line in timeline_lines]
if dates != sorted(dates):
    fail("timeline is not in ascending date order")

timeline_urls = []
for line in timeline_lines:
    match = re.search(r"https://yam\.gift/[^)]+", line)
    if not match:
        fail(f"timeline row has no yam.gift link: {line}")
    timeline_urls.append(match.group(0))

if len(timeline_urls) != len(set(timeline_urls)):
    fail("timeline contains duplicate blog links")

papers_start = text.index("## Papers")
papers_end = text.index("## Chronological Blog Timeline", papers_start)
paper_lines = [
    line for line in text[papers_start:papers_end].splitlines()
    if line.startswith("|")
    and line.count("|") == 7
    and not line.startswith("|---")
    and not line.startswith("| Abbr")
]

track_count = len(re.findall(r"^### Track \d{2} —", text, re.MULTILINE))

if not timeline_lines:
    fail("timeline has no entries")
if not paper_lines:
    fail("paper index has no entries")
if not track_count:
    fail("track overview has no entries")

for line_number, line in enumerate(lines, start=1):
    if line.startswith("| 20") and line.count("|") != 5:
        fail(f"malformed timeline table row at line {line_number}")

print(
    f"README OK: {len(timeline_lines)} deep dives, "
    f"{len(paper_lines)} curated works, {track_count} tracks"
)
