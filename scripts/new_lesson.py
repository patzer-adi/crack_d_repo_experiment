#!/usr/bin/env python3
"""Scaffold a new lesson directory.

Usage:
    python3 scripts/new_lesson.py <slug>

Creates:
    lessons/<slug>/
        lesson.html   (copy of lessons/_template.html with {{TITLE}}, {{SLUG}},
                       {{LC_NUM}}, {{DIFFICULTY}}, {{TAGS}} substituted from
                       data/problems.json when the slug is present there;
                       otherwise inserts placeholders)
        plan.md       (stub for the human-review checkpoint described in
                       PLAN-011 §4.8)

Looks up the slug in data/problems.json for metadata. If the slug is not
found, exits with a non-zero status — add the problem via the dashboard's
"Add problem" flow first.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "lessons" / "_template.html"
PROBLEMS = ROOT / "data" / "problems.json"

SLUG_RE = re.compile(r"^[a-z0-9-]+$")

PLAN_STUB = """# {title} — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `{slug}`
- **LC #:** {lc_num}
- **Difficulty:** {difficulty}
- **Topic:** {topic}
- **Archetype:** <!-- two_pointer / sliding_window / prefix_scan / divide_conquer / custom — pick from design/archetypes.md -->

## 1. Clarifying questions (§0)
<!-- 4 Q/A/unlocks. See design/sec0_clarifying.md -->

## 2. Kernel paragraph (§1)
<!-- One paragraph from which the algorithm is derivable. -->

## 3. Foundational concept visual (§1)
<!-- What does the visual show? Bar chart? Number line? Frequency badges? -->

## 4. Translations (§3)
<!-- List every named optimisation, in order. -->

## 5. Algorithm in plain English (§4)
<!-- 4–6 imperative sentences. -->

## 6. Examples for code viz + dry run (§6, §7)
<!-- One fast (3–5 steps), one slow (10–15 steps). Include expected output. -->

## 7. Corner cases (§8)
<!-- 3–5 entries. -->

## 8. Approaches comparison (§10)
<!-- 2–3 approaches with one-paragraph trade-off each. -->

## 9. Take home (§12)
<!-- 2–4 related LC problems and what differs. -->

## 10. Python verification (BEFORE writing HTML)
<!-- Paste the Python trace output here once it matches expected on all examples. -->
"""


def find_problem(slug: str) -> dict | None:
    if not PROBLEMS.exists():
        return None
    data = json.loads(PROBLEMS.read_text())
    problems = data if isinstance(data, list) else data.get("problems", [])
    for p in problems:
        if p.get("slug") == slug:
            return p
    return None


def substitute_template(template: str, *, title: str, slug: str, lc_num: int,
                        difficulty: str, tags: str) -> str:
    return (
        template
        .replace("{{TITLE}}", title)
        .replace("{{SLUG}}", slug)
        .replace("{{LC_NUM}}", str(lc_num))
        .replace("{{DIFFICULTY}}", difficulty)
        .replace("{{TAGS}}", tags)
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: new_lesson.py <slug>", file=sys.stderr)
        return 2

    slug = sys.argv[1].strip()
    if not SLUG_RE.match(slug):
        print(f"slug must match {SLUG_RE.pattern}", file=sys.stderr)
        return 2

    problem = find_problem(slug)
    if problem is None:
        print(f"slug '{slug}' not found in data/problems.json — add it first "
              f"via the dashboard 'Add problem' flow.", file=sys.stderr)
        return 3

    out_dir = ROOT / "lessons" / slug
    if out_dir.exists():
        print(f"lessons/{slug}/ already exists — refusing to overwrite.",
              file=sys.stderr)
        return 4

    template_text = TEMPLATE.read_text()
    rendered = substitute_template(
        template_text,
        title=problem.get("name", slug),
        slug=slug,
        lc_num=int(problem.get("lc_num", 0)),
        difficulty=problem.get("difficulty", "Medium"),
        tags=problem.get("topic", ""),
    )

    out_dir.mkdir(parents=True)
    (out_dir / "lesson.html").write_text(rendered)
    (out_dir / "plan.md").write_text(PLAN_STUB.format(
        title=problem.get("name", slug),
        slug=slug,
        lc_num=problem.get("lc_num", "—"),
        difficulty=problem.get("difficulty", "—"),
        topic=problem.get("topic", "—"),
    ))

    print(f"created lessons/{slug}/lesson.html")
    print(f"created lessons/{slug}/plan.md")
    print()
    print("Next: fill plan.md, then run the Python algorithm trace "
          "(design/python_verify.md) before generating §1–§12 content.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
