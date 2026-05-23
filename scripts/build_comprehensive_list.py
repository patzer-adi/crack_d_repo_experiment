#!/usr/bin/env python3
"""
PLAN-012 — merge the comprehensive seed into data/problems.json.

Reads:
    scripts/seeds/comprehensive_seed.yaml   (the per-section ramps)
    data/problems.json                      (existing list, source of status/lesson_status)

Writes:
    data/problems.json                      (overwrite; backup taken first)
    data/problems.json.bak-<timestamp>      (backup of the prior file)
    (stdout)                                (diff report)

Preservation rule: an existing problem's `status` and `lesson_status` are
carried over to the merged record when its slug (or, if slug is empty, its
lc_num) matches a seed entry.

Run with --dry-run to see the diff report without overwriting anything.
"""

from __future__ import annotations
import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEED_PATH = PROJECT_ROOT / "scripts" / "seeds" / "comprehensive_seed.yaml"
PROBLEMS_JSON = PROJECT_ROOT / "data" / "problems.json"


# Canonical section_order -> (key_in_yaml, display_title).
# Display title is what lands in the JSON `section` AND `topic` fields.
SECTION_TITLES: dict[int, tuple[str, str]] = {
    1:  ("arrays_and_hashing",   "Arrays & Hashing"),
    2:  ("two_pointers",         "Two Pointers"),
    3:  ("sliding_window",       "Sliding Window"),
    4:  ("prefix_sum",           "Prefix Sum"),
    5:  ("binary_search",        "Binary Search"),
    6:  ("stack_and_monotonic",  "Stack & Monotonic Stack"),
    7:  ("linked_lists",         "Linked Lists"),
    8:  ("trees",                "Trees"),
    9:  ("bst",                  "BST"),
    10: ("heaps",                "Heaps / Priority Queue"),
    11: ("graphs_bfs_dfs",       "Graphs — BFS / DFS"),
    12: ("graphs_advanced",      "Graphs — Advanced"),
    13: ("dynamic_programming",  "Dynamic Programming"),
    14: ("backtracking",         "Backtracking"),
    15: ("greedy_intervals",     "Greedy / Intervals"),
    16: ("tries",                "Tries"),
    17: ("bit_manipulation",     "Bit Manipulation"),
    18: ("math",                 "Math"),
    19: ("string_matching",      "String Matching"),
    20: ("design",               "Design"),
}


def slug_key(p: dict[str, Any]) -> str:
    """Stable key for matching seed entries to existing entries."""
    slug = (p.get("slug") or "").strip()
    if slug:
        return f"slug:{slug}"
    return f"lc:{p['lc_num']}"


def load_existing() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[tuple[str, list[dict[str, Any]]]]]:
    """Returns (raw list, index-by-key keeping the most-progressed duplicate, list of (key, dup-records))."""
    with PROBLEMS_JSON.open() as f:
        raw = json.load(f)
    # Detect duplicates by key.
    by_key: dict[str, list[dict[str, Any]]] = {}
    for p in raw:
        by_key.setdefault(slug_key(p), []).append(p)
    idx: dict[str, dict[str, Any]] = {}
    dupes: list[tuple[str, list[dict[str, Any]]]] = []
    # Status precedence: prefer the duplicate with the more advanced lesson_status / status.
    status_rank = {"done": 2, "in-progress": 1, "new": 0}
    lesson_rank = {"generated": 2, "in-progress": 1, "none": 0}
    def score(p: dict[str, Any]) -> tuple[int, int]:
        return (lesson_rank.get(p.get("lesson_status", "none"), 0),
                status_rank.get(p.get("status", "new"), 0))
    for key, records in by_key.items():
        if len(records) > 1:
            dupes.append((key, records))
            idx[key] = max(records, key=score)
        else:
            idx[key] = records[0]
    return raw, idx, dupes


def load_seed() -> dict[str, dict[str, Any]]:
    with SEED_PATH.open() as f:
        return yaml.safe_load(f)


def build_merged(seed: dict[str, dict[str, Any]],
                 existing_idx: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """
    Returns (merged list sorted by order, stats dict).
    """
    merged: list[dict[str, Any]] = []
    seed_keys: set[str] = set()
    stats = {"preserved": 0, "added": 0, "re_sectioned": 0}

    # Index sections by their YAML key (so we don't depend on dict ordering).
    sections_by_key = {key: data for key, data in seed.items()}

    for section_order in sorted(SECTION_TITLES):
        yaml_key, title = SECTION_TITLES[section_order]
        if yaml_key not in sections_by_key:
            print(f"WARN: seed missing section '{yaml_key}' (#{section_order})", file=sys.stderr)
            continue
        sec = sections_by_key[yaml_key]
        if sec.get("section_order") != section_order:
            print(
                f"WARN: section '{yaml_key}' has section_order={sec.get('section_order')} "
                f"in seed but SECTION_TITLES expects {section_order}",
                file=sys.stderr,
            )

        for problem in sec["problems"]:
            key = slug_key(problem)
            seed_keys.add(key)
            existing = existing_idx.get(key)

            record: dict[str, Any] = {
                "order": section_order * 1000 + problem["ramp_pos"],
                "lc_num": problem["lc_num"],
                "name": problem["name"],
                "url": problem["url"],
                "slug": problem.get("slug", ""),
                "topic": title,
                "difficulty": problem["difficulty"],
                "section": title,
                "tier": problem["tier"],
                "ramp_pos": problem["ramp_pos"],
                "twist": problem["twist"],
                "tracks": list(problem.get("tracks", [])),
            }

            if existing is not None:
                record["status"] = existing.get("status", "new")
                record["lesson_status"] = existing.get("lesson_status", "none")
                stats["preserved"] += 1
                if existing.get("section") != title:
                    stats["re_sectioned"] += 1
            else:
                record["status"] = "new"
                record["lesson_status"] = "none"
                stats["added"] += 1

            merged.append(record)

    # Find orphans: existing entries whose key isn't in any seed section.
    orphans: list[dict[str, Any]] = []
    for key, p in existing_idx.items():
        if key not in seed_keys:
            orphans.append(p)

    return merged, stats, orphans


def report(stats: dict[str, int], merged: list[dict[str, Any]],
           orphans: list[dict[str, Any]], existing_count: int,
           dupes: list[tuple[str, list[dict[str, Any]]]]) -> None:
    print()
    print("=== Merge report ===")
    print(f"Existing problems.json entries : {existing_count}")
    if dupes:
        print(f"Duplicate keys in input        : {len(dupes)} (collapsed; status kept from most-progressed)")
        for key, records in dupes:
            print(f"  {key}:")
            for r in records:
                print(f"    order={r.get('order'):>4} lc={r.get('lc_num'):>4} "
                      f"name={r.get('name')!r} status={r.get('status')} lesson={r.get('lesson_status')}")
    print(f"Merged output entries          : {len(merged)}")
    print(f"  preserved (status carried)   : {stats['preserved']}")
    print(f"  added (new in seed)          : {stats['added']}")
    print(f"  re-sectioned                 : {stats['re_sectioned']}")
    print(f"Orphans (in JSON, not in seed) : {len(orphans)}")
    if orphans:
        print()
        print("  Orphan details — these would be DROPPED unless action is taken:")
        for p in orphans:
            print(f"    LC {p.get('lc_num'):>5}  {p.get('name'):<50} (slug='{p.get('slug')}', section='{p.get('section')}')")
    print()
    # Per-section count.
    by_section: dict[str, int] = {}
    for r in merged:
        by_section[r["section"]] = by_section.get(r["section"], 0) + 1
    print("Per-section counts in merged output:")
    for section_order in sorted(SECTION_TITLES):
        title = SECTION_TITLES[section_order][1]
        print(f"  {section_order:>2}. {title:<28} {by_section.get(title, 0):>4}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Report only; do not write problems.json.")
    ap.add_argument("--keep-orphans", action="store_true",
                    help="Append orphan entries to the merged output instead of dropping them.")
    ap.add_argument("--force", action="store_true",
                    help="Write even if orphans exist (default: refuse unless --dry-run).")
    args = ap.parse_args()

    seed = load_seed()
    existing_raw, existing_idx, dupes = load_existing()
    merged, stats, orphans = build_merged(seed, existing_idx)

    report(stats, merged, orphans, len(existing_raw), dupes)

    if orphans and args.keep_orphans:
        max_order = max(r["order"] for r in merged) if merged else 0
        for i, p in enumerate(orphans, start=1):
            # Preserve everything but bump order past the curated section block.
            entry = dict(p)
            entry["order"] = max_order + i
            # Ensure new schema fields exist with sane defaults.
            entry.setdefault("tier", 2)
            entry.setdefault("ramp_pos", 999)
            entry.setdefault("twist", "")
            entry.setdefault("tracks", [])
            entry.setdefault("section", "Uncurated")
            entry.setdefault("topic", "Uncurated")
            merged.append(entry)
        print(f"\n--keep-orphans: appended {len(orphans)} orphans under section 'Uncurated'.")

    if args.dry_run:
        print("\n--dry-run: not writing problems.json.")
        return 0

    if orphans and not args.keep_orphans and not args.force:
        print("\nRefusing to write: orphans would be dropped. Re-run with "
              "--keep-orphans (preserve under 'Uncurated') or --force (drop).", file=sys.stderr)
        return 2

    # Backup, then write.
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = PROBLEMS_JSON.with_suffix(f".json.bak-{ts}")
    shutil.copy2(PROBLEMS_JSON, bak)
    with PROBLEMS_JSON.open("w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"\nWrote {PROBLEMS_JSON.relative_to(PROJECT_ROOT)} ({len(merged)} entries).")
    print(f"Backup: {bak.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
