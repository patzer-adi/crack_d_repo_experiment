#!/usr/bin/env python3
"""Project lifecycle / reconciliation doctor (PLAN-019 G5).

Asserts the invariants that keep the planning docs and the corpus honest — the
drift classes PLAN-019 was written to stop. Run it after any planning or lesson
change; it is cheap and has no external deps.

FATAL invariants (exit 1 if violated):
  1. Plan ↔ report bijection — every *Completed* PLAN-NNN has exactly one
     REPORT-NNN, and every REPORT-NNN has a matching PLAN-NNN (serial 000
     templates excluded). Draft/Approved/In-Progress/Abandoned plans need no
     report yet, so they are not flagged.
  2. No phantom plan references — every PLAN-NNN cited in a tracked text file
     has a matching plan file (catches the old "(PLAN-019)" dangling ref).
  3. Lesson/status reconciliation — {lessons/<slug>/lesson.html on disk} equals
     {slug : lesson_status == "generated"} in data/problems.json.
  4. "Latest plan" freshness — the highest PLAN-NNN mentioned in README.md and
     CLAUDE.md equals the highest plan serial on disk.
  5. Baseline sanity — every slug in scripts/audit_baseline.json is a real
     generated lesson.

INFO (reported, never fatal):
  - verify.py backfill progress (PLAN-019 G4): how many generated lessons have
     an independent reference yet.

Usage: python3 scripts/doctor.py [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLANS = ROOT / "AGENT_MD/plan/plans"
REPORTS = ROOT / "AGENT_MD/plan/reports"
LESSONS = ROOT / "lessons"


def serials(dir_: Path, prefix: str) -> dict[int, list[str]]:
    """Map serial -> [filenames] for PLAN-/REPORT- files (excluding 000)."""
    out: dict[int, list[str]] = {}
    for p in sorted(dir_.glob(f"{prefix}-*.md")):
        m = re.match(rf"{prefix}-(\d+)", p.name)
        if not m:
            continue
        n = int(m.group(1))
        if n == 0:
            continue
        out.setdefault(n, []).append(p.name)
    return out


def plan_status(n: int, files: list[str]) -> str:
    text = (PLANS / files[0]).read_text()
    m = re.search(r"\*\*Status:\*\*\s*([A-Za-z-]+)", text)
    return m.group(1) if m else "Unknown"


def check_bijection(fatals: list[str]) -> None:
    plans = serials(PLANS, "PLAN")
    reports = serials(REPORTS, "REPORT")
    for n, files in plans.items():
        if len(files) > 1:
            fatals.append(f"duplicate PLAN-{n:03d}: {files}")
    for n, files in reports.items():
        if len(files) > 1:
            fatals.append(f"duplicate REPORT-{n:03d}: {files}")
    # A report is required only once a plan is Completed; Draft/Approved/
    # In-Progress/Abandoned plans legitimately have none yet.
    for n in sorted(set(plans) - set(reports)):
        if plan_status(n, plans[n]) == "Completed":
            fatals.append(f"PLAN-{n:03d} is Completed but has no REPORT-{n:03d}")
    for n in sorted(set(reports) - set(plans)):
        fatals.append(f"REPORT-{n:03d} has no matching PLAN-{n:03d}")


def check_phantom_plan_refs(fatals: list[str]) -> None:
    have = set(serials(PLANS, "PLAN"))
    pat = re.compile(r"PLAN-(\d{3})")
    exts = {".md", ".py", ".mjs", ".json", ".html"}
    skip_dirs = {".git", "node_modules", "__pycache__", "archive"}
    refs: dict[int, set[str]] = {}
    for f in ROOT.rglob("*"):
        if f.is_dir() or f.suffix not in exts:
            continue
        if any(part in skip_dirs for part in f.parts):
            continue
        try:
            text = f.read_text(errors="ignore")
        except OSError:
            continue
        for m in pat.finditer(text):
            n = int(m.group(1))
            if n != 0 and n not in have:
                refs.setdefault(n, set()).add(str(f.relative_to(ROOT)))
    for n in sorted(refs):
        where = ", ".join(sorted(refs[n])[:4])
        fatals.append(f"phantom reference PLAN-{n:03d} (no plan file) cited in: {where}")


def check_lesson_reconciliation(fatals: list[str]) -> None:
    probs = json.loads((ROOT / "data/problems.json").read_text())
    generated = {p["slug"] for p in probs if p.get("lesson_status") == "generated"}
    on_disk = {d.name for d in LESSONS.iterdir()
               if d.is_dir() and (d / "lesson.html").exists() and d.name not in {"design", "archive"}}
    for slug in sorted(on_disk - generated):
        fatals.append(f"lesson on disk but lesson_status != generated: {slug}")
    for slug in sorted(generated - on_disk):
        fatals.append(f"lesson_status=generated but no lessons/{slug}/lesson.html")


def check_latest_plan(fatals: list[str]) -> None:
    have = serials(PLANS, "PLAN")
    if not have:
        return
    latest = max(have)
    for doc in ("README.md", "CLAUDE.md"):
        p = ROOT / doc
        if not p.exists():
            continue
        mentioned = [int(x) for x in re.findall(r"PLAN-(\d{3})", p.read_text())]
        top = max(mentioned) if mentioned else 0
        if top < latest:
            fatals.append(f"{doc} names PLAN-{top:03d} as latest but PLAN-{latest:03d} exists")


def check_baseline(fatals: list[str]) -> None:
    bf = ROOT / "scripts/audit_baseline.json"
    if not bf.exists():
        return
    data = json.loads(bf.read_text())
    probs = json.loads((ROOT / "data/problems.json").read_text())
    generated = {p["slug"] for p in probs if p.get("lesson_status") == "generated"}
    for dim in ("lint", "render"):
        for slug in data.get(dim, {}):
            if slug not in generated:
                fatals.append(f"audit_baseline.json[{dim}] lists '{slug}' which is not a generated lesson")


def verify_backfill() -> tuple[int, int, list[str]]:
    probs = json.loads((ROOT / "data/problems.json").read_text())
    generated = sorted(p["slug"] for p in probs if p.get("lesson_status") == "generated"
                       and (LESSONS / p["slug"] / "lesson.html").exists())
    missing = [s for s in generated if not (LESSONS / s / "verify.py").exists()]
    return len(generated) - len(missing), len(generated), missing


def main() -> int:
    ap = argparse.ArgumentParser(description="Project lifecycle/reconciliation doctor (PLAN-019 G5)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    fatals: list[str] = []
    check_bijection(fatals)
    check_phantom_plan_refs(fatals)
    check_lesson_reconciliation(fatals)
    check_latest_plan(fatals)
    check_baseline(fatals)
    have, total, missing = verify_backfill()

    if args.json:
        print(json.dumps({"fatals": fatals,
                          "verify_py": {"have": have, "total": total, "missing": missing}}, indent=2))
    else:
        print("doctor — lifecycle & reconciliation (PLAN-019 G5)")
        print("─" * 64)
        if fatals:
            for f in fatals:
                print(f"  ✗ {f}")
        else:
            print("  ✓ all invariants hold")
        print("─" * 64)
        print(f"  info: independent verify.py present on {have}/{total} generated lessons"
              + (f"; missing {len(missing)}" if missing else ""))
        print(f"  => {'FAIL' if fatals else 'OK'} ({len(fatals)} violation(s))")

    return 1 if fatals else 0


if __name__ == "__main__":
    sys.exit(main())
