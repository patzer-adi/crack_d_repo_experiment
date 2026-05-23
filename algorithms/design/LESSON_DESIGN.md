# Algorithm Lesson Design

**Status:** Placeholder — full design spec to be written as PLAN-014.

Algorithm lessons follow the same visual conventions as LC lessons in `lessons/` but cover
canonical CS algorithms rather than specific LeetCode problems.

## Key differences from LC lessons

| Aspect | LC Lesson | Algorithm Lesson |
|---|---|---|
| Audience context | Interview preparation | CS fundamentals + interview prep |
| Input | Single LC problem instance | General algorithm with parameterised inputs |
| Code | C++ (primary) | Python (readability) + C++ (performance) |
| Complexity section | Brief, at the end of code | Full derivation as its own section |
| Variants | Not required | Expected (covers algorithm family) |
| Prerequisite chain | Implicit | Explicit (`prereqs` in data/algorithms.json) |

## Scaffolding

Use `scripts/new_algorithm.py <id>` to create `algorithms/<id>/plan.md` pre-filled with
metadata from `data/algorithms.json`.

## Full spec

See PLAN-014 (not yet authored) for the complete lesson template, CSS conventions, and
quality bar. Until PLAN-014 is written, follow the `lessons/LESSON_DESIGN.md` conventions
as closely as possible, adapting for the two-language (Python + C++) requirement.
