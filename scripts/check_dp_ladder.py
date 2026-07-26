#!/usr/bin/env python3
"""Validator for data/dp_ladder.json (PLAN-026).

The DP Ladder is a ~15-problem on-ramp for Dynamic Programming: it starts at
trivial Easy recurrences and *ramps* into a few gentle Mediums, giving someone
who struggles with DP a natural gradient to climb before attempting the
Medium/Hard DP problems in the 211-problem set. It renders as a second view
inside the Warm-Up tab. Checks, in order:

  1. The file parses and is a non-empty JSON array of exactly EXPECTED entries.
  2. Every entry has the required fields, all non-empty.
  3. `slug` is kebab-case, unique, AND disjoint from problems.json, basics.json,
     and warmup.json — the ladder *adds* problems, so any overlap with the three
     existing datasets is a curation bug. Checking the new set against all three
     is enough to keep the whole catalogue mutually disjoint.
  4. `lc_num` is a positive int, unique, and not already in the other datasets.
  5. `url` is the canonical LeetCode URL and its slug matches `slug`.
  6. `difficulty` is Easy or Medium AND is *non-decreasing* in file/order order
     (once a Medium appears, no later Easy). This is the enforceable form of
     "gradually increasing difficulty" — the ladder's whole reason to exist.
  7. `section` (the ramp *stage*) comes from the declared ordered list, stages
     appear in that order, and each stage's rows are contiguous.
  8. `order` values are unique and strictly increasing in file order.
  9. `status` is new|done.
 10. `details` + `example` satisfy the shared hover-card contract.
 11. Report: totals per stage and the Easy→Medium split.

Exit code 0 on pass, 1 on any violation. Stdlib only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from check_basics import check_hover_card

ROOT = Path(__file__).resolve().parent.parent
LADDER = ROOT / "data" / "dp_ladder.json"
PROBLEMS = ROOT / "data" / "problems.json"
BASICS = ROOT / "data" / "basics.json"
WARMUP = ROOT / "data" / "warmup.json"

EXPECTED = 15
REQUIRED = ("order", "lc_num", "slug", "name", "url", "section", "difficulty",
            "statement", "details", "example", "skill", "status")
SECTIONS = [
    "1 · First recurrences",
    "2 · Scan & compare",
    "3 · Take-or-skip choice",
    "4 · Grid DP — the bridge",
    "5 · Counting DP",
]
DIFF_RANK = {"Easy": 0, "Medium": 1}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LC_URL = re.compile(r"^https://leetcode\.com/problems/([a-z0-9-]+)/$")


def main() -> int:
    fatals: list[str] = []

    if not LADDER.exists():
        _summary(["dp_ladder.json missing"])
        return 1
    try:
        entries = json.loads(LADDER.read_text())
    except json.JSONDecodeError as e:
        _summary([f"dp_ladder.json is not valid JSON: {e}"])
        return 1
    if not isinstance(entries, list) or not entries:
        _summary(["dp_ladder.json must be a non-empty array"])
        return 1
    if len(entries) != EXPECTED:
        fatals.append(f"expected exactly {EXPECTED} problems, found {len(entries)}")

    # Disjointness net: every other dataset. Checking the new set against all
    # three keeps the whole catalogue mutually disjoint.
    other_slugs: set[str] = set()
    other_lc: set[int] = set()
    for path in (PROBLEMS, BASICS, WARMUP):
        if not path.exists():
            continue
        for p in json.loads(path.read_text()):
            if p.get("slug"):
                other_slugs.add(p["slug"])
            if isinstance(p.get("lc_num"), int):
                other_lc.add(p["lc_num"])

    seen_slugs: set[str] = set()
    seen_lc: set[int] = set()
    prev_order: int | None = None
    prev_rank: int = -1
    closed: set[str] = set()
    cur_section: str | None = None

    for i, e in enumerate(entries):
        tag = f"entry[{i}] ({e.get('slug', '?')})"

        for field in REQUIRED:
            if field not in e or e[field] in ("", [], None):
                fatals.append(f"{tag}: missing/empty required field '{field}'")

        slug = e.get("slug", "")
        if slug and not KEBAB.match(slug):
            fatals.append(f"{tag}: slug '{slug}' is not kebab-case")
        if slug in seen_slugs:
            fatals.append(f"{tag}: duplicate slug '{slug}'")
        if slug in other_slugs:
            fatals.append(f"{tag}: slug '{slug}' collides with problems/basics/warmup")
        seen_slugs.add(slug)

        lc = e.get("lc_num")
        if not isinstance(lc, int) or lc <= 0:
            fatals.append(f"{tag}: lc_num must be a positive integer")
        else:
            if lc in seen_lc:
                fatals.append(f"{tag}: duplicate lc_num {lc}")
            if lc in other_lc:
                fatals.append(f"{tag}: lc_num {lc} already in problems/basics/warmup")
            seen_lc.add(lc)

        url = e.get("url", "")
        m = LC_URL.match(url) if isinstance(url, str) else None
        if not m:
            fatals.append(f"{tag}: url '{url}' is not a canonical LeetCode problem URL")
        elif m.group(1) != slug:
            fatals.append(f"{tag}: url slug '{m.group(1)}' != slug '{slug}'")

        diff = e.get("difficulty")
        if diff not in DIFF_RANK:
            fatals.append(f"{tag}: difficulty '{diff}' — ladder is Easy or Medium only")
        else:
            if DIFF_RANK[diff] < prev_rank:
                fatals.append(f"{tag}: difficulty '{diff}' drops below an earlier "
                              f"problem — the ladder must be non-decreasing")
            prev_rank = max(prev_rank, DIFF_RANK[diff])

        sec = e.get("section")
        if sec not in SECTIONS:
            fatals.append(f"{tag}: section '{sec}' not one of the declared {len(SECTIONS)}")
        elif sec != cur_section:
            if sec in closed:
                fatals.append(f"{tag}: section '{sec}' is not contiguous")
            if cur_section is not None:
                if SECTIONS.index(sec) < SECTIONS.index(cur_section):
                    fatals.append(f"{tag}: section '{sec}' out of declared order")
                closed.add(cur_section)
            cur_section = sec

        order = e.get("order")
        if not isinstance(order, int):
            fatals.append(f"{tag}: order must be an integer")
        elif prev_order is not None and order <= prev_order:
            fatals.append(f"{tag}: order {order} not strictly increasing (prev {prev_order})")
        if isinstance(order, int):
            prev_order = order

        if e.get("status") not in ("new", "done"):
            fatals.append(f"{tag}: status '{e.get('status')}' must be 'new' or 'done'")

        fatals.extend(check_hover_card(tag, e))

    per_sec = {s: 0 for s in SECTIONS}
    for e in entries:
        if e.get("section") in per_sec:
            per_sec[e["section"]] += 1
    easy = sum(1 for e in entries if e.get("difficulty") == "Easy")
    medium = sum(1 for e in entries if e.get("difficulty") == "Medium")

    print("check_dp_ladder — PLAN-026")
    print("─" * 64)
    print(f"  entries: {len(entries)}  ({easy} Easy → {medium} Medium, disjoint from the rest)")
    for s in SECTIONS:
        print(f"    {per_sec[s]:>3}  {s}")
    print("─" * 64)
    _summary(fatals)
    return 1 if fatals else 0


def _summary(fatals: list[str]) -> None:
    for f in fatals:
        print(f"  ✗ {f}")
    if fatals:
        print(f"  => FAIL ({len(fatals)} violation(s))")
    else:
        print("  => OK")


if __name__ == "__main__":
    sys.exit(main())
