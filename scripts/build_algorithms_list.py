#!/usr/bin/env python3
"""
PLAN-013 — build data/algorithms.json from scripts/seeds/algorithms_seed.yaml.

Reads:
    scripts/seeds/algorithms_seed.yaml   (canonical algorithms inventory)
    data/algorithms.json                 (existing file — preserves lesson_status/lesson_path)

Writes:
    data/algorithms.json                 (overwrite; backup taken first)
    data/algorithms.json.bak-<timestamp> (backup of the prior file)
    (stdout)                             (diff report)

Preservation rule: an existing entry's `lesson_status` and `lesson_path` are
carried over when its `id` matches a seed entry.

Run with --dry-run to see the diff report without writing anything.
"""

from __future__ import annotations
import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEED_PATH    = PROJECT_ROOT / "scripts" / "seeds" / "algorithms_seed.yaml"
OUT_PATH     = PROJECT_ROOT / "data" / "algorithms.json"


CATEGORY_TITLES: dict[int, str] = {
    1:  "Foundational Algorithms",
    2:  "Graph Algorithms",
    3:  "Dynamic Programming",
    4:  "String Algorithms",
    5:  "Computational Geometry",
    6:  "Numerical and Optimization",
    7:  "Data Structures",
    8:  "Advanced Graph",
    9:  "Cryptography and Security",
    # 10 is intentionally absent (ML skipped per PLAN-013 §8)
    11: "Parallel and Distributed",
    12: "Miscellaneous",
    13: "Domain-Specific",
    14: "Advanced Theoretical",
    15: "Emerging Areas",
}


def load_existing() -> dict[str, dict]:
    """Load existing algorithms.json keyed by id; return {} if file absent."""
    if not OUT_PATH.exists():
        return {}
    with OUT_PATH.open() as f:
        data = json.load(f)
    return {e["id"]: e for e in data}


def load_seed() -> dict[str, dict]:
    with SEED_PATH.open() as f:
        return yaml.safe_load(f)


def build(seed: dict[str, dict], existing: dict[str, dict]) -> tuple[list[dict], dict]:
    merged: list[dict] = []
    stats = {"preserved": 0, "added": 0}

    for section_key, section in sorted(seed.items(), key=lambda kv: kv[1]["category_order"]):
        cat_order = section["category_order"]
        category  = section["category"]

        for e in section["entries"]:
            eid      = e["id"]
            ramp_pos = e["ramp_pos"]
            order    = cat_order * 1000 + ramp_pos

            record: dict = {
                "id":                   eid,
                "name":                 e["name"],
                "category":             category,
                "category_order":       cat_order,
                "ramp_pos":             ramp_pos,
                "order":                order,
                "kind":                 e["kind"],
                "tier":                 e["tier"],
                "interview_relevance":  e["interview_relevance"],
                "complexity": {
                    "time":  e["complexity"]["time"],
                    "space": e["complexity"]["space"],
                    **({"notes": e["complexity"]["notes"]} if "notes" in e["complexity"] else {}),
                },
                "prereqs":    list(e.get("prereqs", [])),
                "short_note": e["short_note"],
                "references": list(e.get("references", [])),
                "related_lc": list(e.get("related_lc", [])),
            }
            if "aliases" in e:
                record["aliases"] = list(e["aliases"])

            prior = existing.get(eid)
            if prior is not None:
                record["lesson_status"] = prior.get("lesson_status", "none")
                record["lesson_path"]   = prior.get("lesson_path", None)
                stats["preserved"] += 1
            else:
                record["lesson_status"] = "none"
                record["lesson_path"]   = None
                stats["added"] += 1

            merged.append(record)

    return merged, stats


def report(merged: list[dict], stats: dict, existing_count: int) -> None:
    print()
    print("=== Build report ===")
    print(f"Existing algorithms.json entries : {existing_count}")
    print(f"Output entries                   : {len(merged)}")
    print(f"  lesson_status preserved        : {stats['preserved']}")
    print(f"  new (lesson_status=none)       : {stats['added']}")
    print()
    print("Per-category counts:")
    by_cat: dict[str, int] = {}
    for e in merged:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + 1
    for co in sorted(CATEGORY_TITLES):
        cat = CATEGORY_TITLES[co]
        n = by_cat.get(cat, 0)
        print(f"  {co:>2}. {cat:<32} {n:>3}")

    # Warn on related_lc slugs that don't exist in problems.json (best-effort)
    problems_path = PROJECT_ROOT / "data" / "problems.json"
    if problems_path.exists():
        with problems_path.open() as f:
            lc_slugs = {p["slug"] for p in json.load(f) if p.get("slug")}
        bad = [(e["id"], s) for e in merged for s in e["related_lc"] if s not in lc_slugs]
        if bad:
            print()
            print(f"WARN: {len(bad)} related_lc slug(s) not in problems.json (cross-link chips will be skipped):")
            for eid, slug in bad:
                print(f"  {eid} -> {slug}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Report only; do not write algorithms.json.")
    args = ap.parse_args()

    seed     = load_seed()
    existing = load_existing()
    merged, stats = build(seed, existing)

    report(merged, stats, len(existing))

    if args.dry_run:
        print("\n--dry-run: not writing algorithms.json.")
        return 0

    if OUT_PATH.exists():
        ts  = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = OUT_PATH.with_suffix(f".json.bak-{ts}")
        shutil.copy2(OUT_PATH, bak)
        print(f"\nBackup: {bak.relative_to(PROJECT_ROOT)}")

    with OUT_PATH.open("w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {OUT_PATH.relative_to(PROJECT_ROOT)} ({len(merged)} entries).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
