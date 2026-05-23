#!/usr/bin/env python3
"""Audit every lesson in lessons/ against PLAN-016 lint criteria.

Usage:
    python3 scripts/audit_lessons.py [--json]

Walks lessons/<slug>/lesson.html and invokes lint_lesson.lint_lesson() for each.
Prints a pass / warn / fail summary table.

Exit code: always 0 (audit reports state; failure is informational).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"

sys.path.insert(0, str(ROOT / "scripts"))
from lint_lesson import lint_lesson  # noqa: E402


def discover_slugs(only_generated: bool = True) -> list[str]:
    if only_generated:
        problems = json.loads((ROOT / "data/problems.json").read_text())
        return sorted(
            p["slug"] for p in problems
            if p.get("lesson_status") == "generated"
            and (LESSONS / p["slug"] / "lesson.html").exists()
        )
    slugs = []
    for path in sorted(LESSONS.iterdir()):
        if not path.is_dir():
            continue
        if path.name in {"design", "archive"}:
            continue
        if (path / "lesson.html").exists():
            slugs.append(path.name)
    return slugs


def render_text(rows: list[tuple[str, str, str]]) -> str:
    pass_count = sum(1 for _, status, _ in rows if status == "PASS")
    warn_count = sum(1 for _, status, _ in rows if status == "WARN")
    fail_count = sum(1 for _, status, _ in rows if status == "FAIL")

    lines = [
        "Lesson audit (PLAN-016 lint over all lessons)",
        "─" * 60,
    ]
    width = max((len(s) for s, _, _ in rows), default=10)
    for slug, status, details in rows:
        lines.append(f"  {status:5}  {slug:{width}}  {details}")
    lines.append("─" * 60)
    lines.append(
        f"  Totals: {pass_count} pass, {warn_count} warn, {fail_count} fail"
        f"  (of {len(rows)} lessons)"
    )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit all lessons against PLAN-016 lint")
    ap.add_argument("--json", action="store_true", help="emit JSON output")
    ap.add_argument("--all", action="store_true",
                    help="audit every lesson dir, including scaffolds (default: only generated)")
    args = ap.parse_args()

    slugs = discover_slugs(only_generated=not args.all)
    rows: list[tuple[str, str, str]] = []
    json_rows: list[dict] = []

    for slug in slugs:
        report = lint_lesson(slug, sections=[1])
        if report.failures:
            status = "FAIL"
            details = "; ".join(f.message or f.rule for f in report.failures)
        elif report.warnings:
            status = "WARN"
            details = "; ".join(w.message or w.rule for w in report.warnings)
        else:
            status = "PASS"
            details = ""
        rows.append((slug, status, details))
        json_rows.append({
            "slug": slug,
            "status": status,
            "failures": [{"rule": f.rule, "message": f.message} for f in report.failures],
            "warnings": [{"rule": w.rule, "message": w.message} for w in report.warnings],
        })

    if args.json:
        print(json.dumps(json_rows, indent=2))
    else:
        print(render_text(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
