#!/usr/bin/env python3
"""Flip lesson_status/lesson_path in data/algorithms.json for gated lessons.

Usage: python3 scripts/wire_algo_lesson.py <id> [<id> ...]

Refuses any id whose algorithms/<id>/lesson.html does not exist. Run this only
AFTER all three gates pass — it is the dashboard-visible switch (PLAN-027 §5).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALGOS = ROOT / "data" / "algorithms.json"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 scripts/wire_algo_lesson.py <id> [<id> ...]", file=sys.stderr)
        return 1
    data = json.loads(ALGOS.read_text())
    by_id = {a["id"]: a for a in data}
    rc = 0
    for algo_id in sys.argv[1:]:
        entry = by_id.get(algo_id)
        if entry is None:
            print(f"ERROR: '{algo_id}' not in algorithms.json", file=sys.stderr)
            rc = 1
            continue
        rel = f"algorithms/{algo_id}/lesson.html"
        if not (ROOT / rel).exists():
            print(f"ERROR: {rel} does not exist — not wiring", file=sys.stderr)
            rc = 1
            continue
        entry["lesson_status"] = "generated"
        entry["lesson_path"] = rel
        print(f"wired {algo_id}")
    ALGOS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
