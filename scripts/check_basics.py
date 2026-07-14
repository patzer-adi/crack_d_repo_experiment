#!/usr/bin/env python3
"""Validator for data/basics.json (PLAN-022 G5).

Run as the authoring gate for the Basics tab (language-agnostic programming
drills curated from the user's C practice sheet). Checks, in order:

  1. The file parses and is a non-empty JSON array.
  2. Every entry has the required fields, all non-empty.
  3. `slug` is kebab-case, unique within the file, AND disjoint from BOTH
     data/problems.json and data/warmup.json (so a future lesson for any
     dataset can never be ambiguous — collisions are real: `reverse-integer`,
     `power-of-two` and `palindrome-number` all exist on the LeetCode side).
  4. `order` values are unique and strictly increasing in file order.
  5. `difficulty` is Easy|Medium|Hard and non-decreasing in rank within each
     section — the "build up the difficulty gradually" requirement, enforced.
  6. `section` comes from the declared ordered list, sections appear in that
     order, and each section's rows are contiguous.
  7. Every `source` ref matches S<sec>[.<item>][a|b] (PDF traceability) or is
     the literal "new" (the 12 user-approved additions).
  8. `status` is new|done.
  9. PLAN-023: `details` is present and substantive, and `example` is an object
     with a non-empty `output` plus an optional `input` — these two feed the
     row's ⓘ hover card, so a missing one ships an empty popover.
 10. Report: totals per section and per difficulty.

Exit code 0 on pass, 1 on any violation. Stdlib only, matching the project's
other check scripts.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASICS = ROOT / "data" / "basics.json"
PROBLEMS = ROOT / "data" / "problems.json"
WARMUP = ROOT / "data" / "warmup.json"

REQUIRED = ("order", "slug", "name", "section", "difficulty",
            "statement", "details", "example", "source", "status")
MIN_DETAILS = 40   # a one-clause stub is not a hover card
SECTIONS = [
    "Output, Input & Variables",
    "Arithmetic & Expressions",
    "Conditionals",
    "Loop Fundamentals",
    "Digits, Divisors & Primes",
    "Interactive Programs & Loop Control",
    "Nested Loops & Patterns",
]
DIFF_RANK = {"Easy": 0, "Medium": 1, "Hard": 2}
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SOURCE_REF = re.compile(r"^S\d(\.\d+)*[ab]?$")


def check_hover_card(tag: str, e: dict) -> list[str]:
    """PLAN-023: validate the `details` + `example` pair behind the ⓘ hover card.

    Shared with check_warmup.py — both datasets render the same popover
    component, so they must agree on its shape.
    """
    bad: list[str] = []

    details = e.get("details")
    if not isinstance(details, str):
        bad.append(f"{tag}: details must be a string")
    elif len(details.strip()) < MIN_DETAILS:
        bad.append(f"{tag}: details too short ({len(details.strip())} < {MIN_DETAILS} chars)")

    ex = e.get("example")
    if not isinstance(ex, dict):
        bad.append(f"{tag}: example must be an object")
        return bad

    unknown = set(ex) - {"input", "output"}
    if unknown:
        bad.append(f"{tag}: example has unknown key(s) {sorted(unknown)}")
    out = ex.get("output")
    if not isinstance(out, str) or not out.strip():
        bad.append(f"{tag}: example.output is required and must be a non-empty string")
    if "input" in ex and (not isinstance(ex["input"], str) or not ex["input"].strip()):
        bad.append(f"{tag}: example.input, when present, must be a non-empty string")
    return bad


def main() -> int:
    fatals: list[str] = []

    if not BASICS.exists():
        _summary(["basics.json missing"])
        return 1

    try:
        entries = json.loads(BASICS.read_text())
    except json.JSONDecodeError as e:
        _summary([f"basics.json is not valid JSON: {e}"])
        return 1

    if not isinstance(entries, list) or not entries:
        _summary(["basics.json must be a non-empty array"])
        return 1

    # blank slugs exist in problems.json (LC premium entries) — never a collision
    other_slugs = {p.get("slug") for p in json.loads(PROBLEMS.read_text())}
    if WARMUP.exists():
        other_slugs |= {w.get("slug") for w in json.loads(WARMUP.read_text())}
    other_slugs.discard("")

    seen_slugs: set[str] = set()
    prev_order: int | None = None
    closed_sections: set[str] = set()   # sections we've moved past (contiguity)
    cur_section: str | None = None
    cur_diff_rank = 0

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
            fatals.append(f"{tag}: slug '{slug}' collides with problems.json/warmup.json")
        seen_slugs.add(slug)

        order = e.get("order")
        if not isinstance(order, int):
            fatals.append(f"{tag}: order must be an integer")
        elif prev_order is not None and order <= prev_order:
            fatals.append(f"{tag}: order {order} not strictly increasing (prev {prev_order})")
        if isinstance(order, int):
            prev_order = order

        sec = e.get("section")
        if sec not in SECTIONS:
            fatals.append(f"{tag}: section '{sec}' not one of the declared {len(SECTIONS)}")
        elif sec != cur_section:
            if sec in closed_sections:
                fatals.append(f"{tag}: section '{sec}' is not contiguous")
            if cur_section is not None:
                if SECTIONS.index(sec) < SECTIONS.index(cur_section):
                    fatals.append(f"{tag}: section '{sec}' out of declared order")
                closed_sections.add(cur_section)
            cur_section = sec
            cur_diff_rank = 0

        diff = e.get("difficulty")
        if diff not in DIFF_RANK:
            fatals.append(f"{tag}: difficulty '{diff}' not in {list(DIFF_RANK)}")
        else:
            rank = DIFF_RANK[diff]
            if rank < cur_diff_rank:
                fatals.append(f"{tag}: difficulty '{diff}' breaks the ramp within '{sec}'")
            cur_diff_rank = max(cur_diff_rank, rank)

        for ref in e.get("source", []) or []:
            if ref != "new" and not SOURCE_REF.match(ref):
                fatals.append(f"{tag}: source ref '{ref}' matches neither S<sec>.<item> nor 'new'")

        if e.get("status") not in ("new", "done"):
            fatals.append(f"{tag}: status '{e.get('status')}' must be 'new' or 'done'")

        fatals.extend(check_hover_card(tag, e))

    per_sec = {s: 0 for s in SECTIONS}
    per_diff = {d: 0 for d in DIFF_RANK}
    for e in entries:
        if e.get("section") in per_sec:
            per_sec[e["section"]] += 1
        if e.get("difficulty") in per_diff:
            per_diff[e["difficulty"]] += 1
    added = sum(1 for e in entries if "new" in (e.get("source") or []))

    print("check_basics — PLAN-022 G5")
    print("─" * 64)
    print(f"  entries: {len(entries)}   added-beyond-PDF: {added}")
    for s in SECTIONS:
        print(f"    {per_sec[s]:>3}  {s}")
    print("  difficulty: " + " · ".join(f"{per_diff[d]} {d}" for d in DIFF_RANK))
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
