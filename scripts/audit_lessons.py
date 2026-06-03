#!/usr/bin/env python3
"""Corpus-wide quality sweep over every generated lesson (PLAN-019 G2/G3).

Usage:
    python3 scripts/audit_lessons.py [--json] [--all] [--no-render]

For each generated lesson it runs the FULL linter (schema + §1 + §6 + §7 +
§animation — the §animation check already shells out to verify_animation.mjs,
so structural lint AND answer-correctness are both covered). It then runs the
headless render smoke test (scripts/render_check.mjs) once over the corpus and
folds the result in as a second column.

Baseline policy (PLAN-019): scripts/audit_baseline.json lists lessons with KNOWN
pre-existing lint/render drift (found when this sweep first ran the full lint +
render over the whole corpus — the old audit only checked §1). Those are
reported KNOWN-FAIL and do NOT break the sweep, so the audit is a REGRESSION
gate: a NEW failure (slug not baselined for that dimension) fails the audit, and
a baselined slug that now PASSES must be removed (the audit flags it so the list
only shrinks). Per-lesson lint_lesson.py and render_check.mjs stay strict, so
newly-authored lessons must be fully clean.

Exit code: 0 if no new lint/render failure and no stale baseline entry; else 1.
Use --no-render for a lint-only pass (no browser).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"
RENDER_SCRIPT = ROOT / "scripts" / "render_check.mjs"
AUDIT_BASELINE = ROOT / "scripts" / "audit_baseline.json"

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
        if not path.is_dir() or path.name in {"design", "archive"}:
            continue
        if (path / "lesson.html").exists():
            slugs.append(path.name)
    return slugs


def load_baseline() -> dict[str, dict]:
    if not AUDIT_BASELINE.exists():
        return {"lint": {}, "render": {}}
    data = json.loads(AUDIT_BASELINE.read_text())
    return {"lint": data.get("lint", {}), "render": data.get("render", {})}


def run_render(slugs: list[str]) -> dict[str, dict]:
    """Run render_check.mjs --json once; {slug: report}. {} if it could not run."""
    try:
        proc = subprocess.run(
            ["node", str(RENDER_SCRIPT), *slugs, "--json"],
            capture_output=True, text=True, timeout=600,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {}
    try:
        return {r["slug"]: r for r in json.loads(proc.stdout)}
    except json.JSONDecodeError:
        return {}


def classify(failed: bool, passed_clean: bool, baselined: bool) -> tuple[str, bool]:
    """Return (status, counts_as_audit_failure) for one dimension of one lesson."""
    if failed:
        return ("KNOWN-FAIL", False) if baselined else ("FAIL", True)
    if baselined:  # listed as known-bad but now clean → stale baseline entry
        return ("FIXED?", True)
    return ("PASS" if passed_clean else "WARN", False)


def main() -> int:
    ap = argparse.ArgumentParser(description="Corpus-wide lesson quality sweep (PLAN-019)")
    ap.add_argument("--json", action="store_true", help="emit JSON output")
    ap.add_argument("--all", action="store_true",
                    help="audit every lesson dir, including scaffolds (default: only generated)")
    ap.add_argument("--no-render", action="store_true", help="skip the headless render smoke test")
    args = ap.parse_args()

    slugs = discover_slugs(only_generated=not args.all)
    baseline = load_baseline()
    render = {} if args.no_render else run_render(slugs)
    render_ran = bool(render)

    rows: list[dict] = []
    audit_failed = False

    for slug in slugs:
        report = lint_lesson(slug, None)  # None => all sections (1,2,6,7) incl. §animation
        lint_status, lint_bad = classify(
            failed=bool(report.failures),
            passed_clean=not report.warnings,
            baselined=slug in baseline["lint"],
        )
        lint_detail = "; ".join(sorted({f.rule for f in report.failures})) if report.failures \
            else ("; ".join(w.message or w.rule for w in report.warnings) if report.warnings else "")
        audit_failed |= lint_bad

        render_status, render_detail = "—", ""
        if render_ran:
            r = render.get(slug)
            if r is None:
                render_status = "?"
            else:
                render_status, render_bad = classify(
                    failed=not r["ok"], passed_clean=True, baselined=slug in baseline["render"],
                )
                if not r["ok"]:
                    render_detail = "; ".join(r.get("reasons", []))
                elif render_status == "FIXED?":
                    render_detail = "render passes now — remove from audit_baseline.json[render]"
                audit_failed |= render_bad

        rows.append({
            "slug": slug,
            "lint": lint_status, "lint_detail": lint_detail,
            "render": render_status, "render_detail": render_detail,
        })

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        width = max((len(r["slug"]) for r in rows), default=10)
        print("Lesson audit — full lint + render, baseline-aware (PLAN-019 G2/G3)")
        print("─" * 80)
        for r in rows:
            detail = r["render_detail"] or r["lint_detail"]
            detail = (detail[:54] + "…") if len(detail) > 55 else detail
            print(f"  lint:{r['lint']:11} render:{r['render']:11} {r['slug']:{width}} {detail}")
        print("─" * 80)
        def n(dim, st): return sum(1 for r in rows if r[dim] == st)
        print(f"  {len(rows)} lessons")
        print(f"  lint:   {n('lint','PASS')} pass · {n('lint','WARN')} warn · "
              f"{n('lint','KNOWN-FAIL')} known-fail · {n('lint','FAIL')} NEW fail · {n('lint','FIXED?')} fixed(remove)")
        if render_ran:
            print(f"  render: {n('render','PASS')} pass · {n('render','KNOWN-FAIL')} known-fail · "
                  f"{n('render','FAIL')} NEW fail · {n('render','FIXED?')} fixed(remove)")
        else:
            print("  render: skipped" + (" (no node/browser?)" if not args.no_render else ""))
        print(f"  => {'FAIL (new regression or stale baseline)' if audit_failed else 'OK (no new drift)'}")

    return 1 if audit_failed else 0


if __name__ == "__main__":
    sys.exit(main())
