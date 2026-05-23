#!/usr/bin/env python3
"""
Scaffold a new algorithm lesson directory from data/algorithms.json.

Usage:
    python3 scripts/new_algorithm.py <id> [<id> ...]

Creates:
    algorithms/<id>/plan.md   — starter plan document (editable)

Does NOT generate lesson HTML — that is a manual or /batch-lesson step.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALGOS_JSON   = PROJECT_ROOT / "data" / "algorithms.json"


def load_algos() -> dict[str, dict]:
    with ALGOS_JSON.open() as f:
        data = json.load(f)
    return {e["id"]: e for e in data}


PLAN_TEMPLATE = """\
# Algorithm Lesson Plan: {name}

## Metadata
- **ID:** {id}
- **Category:** {category} (category_order {category_order})
- **Kind:** {kind}
- **Tier:** {tier}  (1=primer, 2=core, 3=advanced)
- **Interview relevance:** {interview_relevance}

## Complexity
- **Time:** {time}
- **Space:** {space}
{notes_line}
## Prerequisites
{prereqs_list}

## Key idea (short_note)
{short_note}

## Related LC problems
{related_lc_list}

## References
{references_list}

---

## Lesson outline

### 1. Motivation
[Why does this algorithm exist? What problem does it solve that simpler approaches cannot?
Start with the brute-force approach and show the cost. Then show the key insight.]

### 2. Core idea
[One-paragraph explanation of the central mechanism. No code yet — describe the invariant or
structure that makes the algorithm work.]

### 3. Step-by-step dry run
[Choose 1–2 concrete examples. Walk through every step showing state changes.
Use a table or annotated diagram for data structure state.]

### 4. Pseudocode
```
[Clean pseudocode, 10–20 lines]
```

### 5. Implementation (Python + C++)
[Both languages. Python for readability; C++ for performance-critical context.
Use the same conventions as existing lessons.]

### 6. Complexity analysis
[Derive time and space complexity from the pseudocode. Cover best/average/worst if they differ.]

### 7. Variants and extensions
[Other forms this algorithm takes, or common follow-up problems.]

### 8. Common pitfalls
[List 3–5 mistakes people make when implementing or applying this algorithm.]

## Output file
`algorithms/{id}/lesson.html` — self-contained HTML, same style as lessons/ directory.
"""


def make_plan(algo: dict) -> str:
    notes_line = f"- **Notes:** {algo['complexity']['notes']}\n" \
        if algo['complexity'].get('notes') else ""
    prereqs = algo.get("prereqs", [])
    prereqs_list = "\n".join(f"- `{p}`" for p in prereqs) if prereqs else "- (none)"
    related = algo.get("related_lc", [])
    related_list = "\n".join(f"- `{s}`" for s in related) if related else "- (none)"
    refs = algo.get("references", [])
    refs_list = "\n".join(f"- {r}" for r in refs) if refs else "- (none)"
    return PLAN_TEMPLATE.format(
        name=algo["name"],
        id=algo["id"],
        category=algo["category"],
        category_order=algo["category_order"],
        kind=algo["kind"],
        tier=algo["tier"],
        interview_relevance=algo["interview_relevance"],
        time=algo["complexity"]["time"],
        space=algo["complexity"]["space"],
        notes_line=notes_line,
        prereqs_list=prereqs_list,
        short_note=algo["short_note"],
        related_lc_list=related_list,
        references_list=refs_list,
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/new_algorithm.py <id> [<id> ...]", file=sys.stderr)
        return 1

    algos = load_algos()
    errors = 0
    for algo_id in sys.argv[1:]:
        algo = algos.get(algo_id)
        if not algo:
            print(f"ERROR: '{algo_id}' not found in data/algorithms.json", file=sys.stderr)
            errors += 1
            continue

        dest_dir = PROJECT_ROOT / "algorithms" / algo_id
        dest_dir.mkdir(parents=True, exist_ok=True)

        plan_path = dest_dir / "plan.md"
        if plan_path.exists():
            print(f"SKIP (already exists): {plan_path.relative_to(PROJECT_ROOT)}")
        else:
            plan_path.write_text(make_plan(algo))
            print(f"Created: {plan_path.relative_to(PROJECT_ROOT)}")

    return errors


if __name__ == "__main__":
    sys.exit(main())
