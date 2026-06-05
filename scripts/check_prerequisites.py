#!/usr/bin/env python3
"""Validator for data/prerequisites.json (PLAN-021 G6).

Run as the authoring gate for the Prerequisites tab. Checks, in order:

  1. The file parses and is a non-empty JSON array.
  2. Every entry has the required fields from data/prerequisites.schema.json,
     `id` is unique + kebab-case, `level`/`group` are in their enums, and each
     `snippets[]` entry has a non-empty `label` + `code`.
  3. Every value in an entry's `topics[]` exists in data/problems.json's set of
     `topic` values — so the "-> N problems" cascade can never silently resolve
     to zero (the failure mode a per-problem field would hide).
  4. Every `animation` id referenced by an entry is registered in
     dashboard/prereq-anims.js (appears there as a quoted string).
  5. Coverage: the union of `topics[]` must cover >= 90% of the 211 problems,
     so essentially every problem can see at least one prerequisite.

Exit code 0 on pass, 1 on any violation. Dependency-light (stdlib only), to
match the project's other check scripts.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREREQS = ROOT / "data" / "prerequisites.json"
PROBLEMS = ROOT / "data" / "problems.json"
SCHEMA = ROOT / "data" / "prerequisites.schema.json"
ANIMS = ROOT / "dashboard" / "prereq-anims.js"

COVERAGE_MIN = 0.90
KEBAB = re.compile(r"^[a-z0-9-]+$")


def main() -> int:
    fatals: list[str] = []

    if not PREREQS.exists():
        print(f"  ✗ {PREREQS.relative_to(ROOT)} does not exist yet")
        _summary(["prerequisites.json missing"])
        return 1

    try:
        entries = json.loads(PREREQS.read_text())
    except json.JSONDecodeError as e:
        _summary([f"prerequisites.json is not valid JSON: {e}"])
        return 1

    schema = json.loads(SCHEMA.read_text())
    required = schema["definitions"]["entry"]["required"]
    props = schema["definitions"]["entry"]["properties"]
    level_enum = props["level"]["enum"]
    group_enum = props["group"]["enum"]

    problems = json.loads(PROBLEMS.read_text())
    valid_topics = {p.get("topic") for p in problems if p.get("topic")}

    anim_text = ANIMS.read_text() if ANIMS.exists() else ""

    if not isinstance(entries, list) or not entries:
        fatals.append("prerequisites.json must be a non-empty array")
        _summary(fatals)
        return 1

    seen_ids: set[str] = set()
    covered_topics: set[str] = set()

    for i, e in enumerate(entries):
        tag = f"entry[{i}] ({e.get('id', '?')})"

        for field in required:
            if field not in e:
                fatals.append(f"{tag}: missing required field '{field}'")

        eid = e.get("id", "")
        if eid and not KEBAB.match(eid):
            fatals.append(f"{tag}: id '{eid}' is not kebab-case")
        if eid in seen_ids:
            fatals.append(f"{tag}: duplicate id '{eid}'")
        seen_ids.add(eid)

        if e.get("level") not in level_enum:
            fatals.append(f"{tag}: level '{e.get('level')}' not in {level_enum}")
        if e.get("group") not in group_enum:
            fatals.append(f"{tag}: group '{e.get('group')}' not in {group_enum}")

        for j, s in enumerate(e.get("snippets", []) or []):
            if not s.get("label"):
                fatals.append(f"{tag}: snippets[{j}] missing label")
            if not s.get("code"):
                fatals.append(f"{tag}: snippets[{j}] missing/empty code")

        topics = e.get("topics", []) or []
        if not topics:
            fatals.append(f"{tag}: topics[] is empty (no cascade)")
        for t in topics:
            if t not in valid_topics:
                fatals.append(f"{tag}: topic '{t}' is not a real problems.json topic")
            else:
                covered_topics.add(t)

        anim = e.get("animation")
        if anim and f"'{anim}'" not in anim_text and f'"{anim}"' not in anim_text:
            fatals.append(f"{tag}: animation '{anim}' not registered in {ANIMS.name}")

    # Coverage: how many of the 211 problems sit under a covered topic.
    covered = sum(1 for p in problems if p.get("topic") in covered_topics)
    total = len(problems)
    pct = covered / total if total else 0.0
    if pct < COVERAGE_MIN:
        fatals.append(
            f"coverage {pct:.1%} < {COVERAGE_MIN:.0%} "
            f"({covered}/{total} problems under a mapped topic)"
        )

    print("check_prerequisites — PLAN-021 G6")
    print("─" * 64)
    print(f"  entries: {len(entries)}   topics covered: {len(covered_topics)}/{len(valid_topics)}")
    print(f"  problem coverage: {covered}/{total} ({pct:.1%})")
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
