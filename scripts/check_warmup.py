#!/usr/bin/env python3
"""Validator for data/warmup.json (PLAN-023 G4).

The Warm-Up tab is 30 *easy* LeetCode problems that bridge Basics (no data
structures) and Problems (the 211-problem DSA set). Checks, in order:

  1. The file parses and is a non-empty JSON array of exactly EXPECTED entries.
  2. Every entry has the required fields, all non-empty.
  3. `slug` is kebab-case, unique, AND disjoint from data/problems.json and
     data/basics.json — the whole point of Warm-Up is that it *adds* 30
     problems, so any overlap with the 211 is a curation bug, not a feature.
  4. `lc_num` is a positive int, unique, and not already in problems.json.
  5. `url` is the canonical LeetCode URL and its slug matches `slug` — a
     mismatch means the row links somewhere other than what it describes.
  6. `difficulty` is Easy for every entry. Warm-Up is the on-ramp; a Medium
     here belongs in Problems instead.
  7. `section` comes from the declared ordered list, sections appear in that
     order, and each section's rows are contiguous.
  8. `order` values are unique and strictly increasing in file order.
  9. `status` is new|done.
 10. `details` + `example` satisfy the shared hover-card contract.
 11. Report: totals per section.

Exit code 0 on pass, 1 on any violation. Stdlib only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from check_basics import check_hover_card

ROOT = Path(__file__).resolve().parent.parent
WARMUP = ROOT / "data" / "warmup.json"
PROBLEMS = ROOT / "data" / "problems.json"
BASICS = ROOT / "data" / "basics.json"

EXPECTED = 30
REQUIRED = ("order", "lc_num", "slug", "name", "url", "section", "difficulty",
            "statement", "details", "example", "skill", "status")
SECTIONS = [
    "Arrays & Hashing",
    "Strings",
    "Two Pointers & Sliding Window",
    "Binary Search",
    "Stack",
    "Linked Lists",
    "Trees",
    "Math & Bits",
    "Dynamic Programming",
]
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LC_URL = re.compile(r"^https://leetcode\.com/problems/([a-z0-9-]+)/$")


def main() -> int:
    fatals: list[str] = []

    if not WARMUP.exists():
        _summary(["warmup.json missing"])
        return 1
    try:
        entries = json.loads(WARMUP.read_text())
    except json.JSONDecodeError as e:
        _summary([f"warmup.json is not valid JSON: {e}"])
        return 1
    if not isinstance(entries, list) or not entries:
        _summary(["warmup.json must be a non-empty array"])
        return 1
    if len(entries) != EXPECTED:
        fatals.append(f"expected exactly {EXPECTED} problems, found {len(entries)}")

    dsa = json.loads(PROBLEMS.read_text())
    dsa_slugs = {p.get("slug") for p in dsa} - {""}
    dsa_lc = {p.get("lc_num") for p in dsa}
    other_slugs = set(dsa_slugs)
    if BASICS.exists():
        other_slugs |= {b.get("slug") for b in json.loads(BASICS.read_text())}

    seen_slugs: set[str] = set()
    seen_lc: set[int] = set()
    prev_order: int | None = None
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
            fatals.append(f"{tag}: slug '{slug}' collides with problems.json/basics.json")
        seen_slugs.add(slug)

        lc = e.get("lc_num")
        if not isinstance(lc, int) or lc <= 0:
            fatals.append(f"{tag}: lc_num must be a positive integer")
        else:
            if lc in seen_lc:
                fatals.append(f"{tag}: duplicate lc_num {lc}")
            if lc in dsa_lc:
                fatals.append(f"{tag}: lc_num {lc} already in data/problems.json")
            seen_lc.add(lc)

        url = e.get("url", "")
        m = LC_URL.match(url) if isinstance(url, str) else None
        if not m:
            fatals.append(f"{tag}: url '{url}' is not a canonical LeetCode problem URL")
        elif m.group(1) != slug:
            fatals.append(f"{tag}: url slug '{m.group(1)}' != slug '{slug}'")

        if e.get("difficulty") != "Easy":
            fatals.append(f"{tag}: difficulty '{e.get('difficulty')}' — Warm-Up is Easy-only")

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

    print("check_warmup — PLAN-023 G4")
    print("─" * 64)
    print(f"  entries: {len(entries)} (all Easy, all disjoint from the 211)")
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
