# Lesson Design — Index

> **Loading rule:** This file is the only design doc that should be loaded by
> default. Files under `lessons/design/` are referenced from the table below.
> **Load them only when authoring the matching lesson section. Do NOT preload.**
>
> An agent following this index correctly pulls in ~1.5k tokens of design
> guidance per section instead of the ~4.6k tokens of the legacy monolithic
> `LESSON_DESIGN_v2.md`.

---

## Always true

- **Shared assets.** `static/lesson.css` and `static/lesson.js` are sourced once (PLAN-010). Every lesson imports them with:
  ```html
  <link rel="stylesheet" href="../../static/lesson.css">
  <script src="../../static/lesson.js"></script>
  ```
  Do not regenerate, copy, or inline their contents. For class vocabulary load `static/CLASSES.md` — feed that to the generator, never the full CSS.

- **Reader assumption.** The reader has already tried this problem and failed. Skip basics; explain the insight.

- **Mandatory section order.** Sections 0 through 12 below, in that order, no skipping, no merging.

- **Template.** Start every new lesson from [`lessons/_template.html`](./_template.html). It is the section skeleton with class names already in place. Replace `<!-- PER-PROBLEM: ... -->` markers only.

- **Section markers (exact format).** Every section opens with `<!-- ═══ SECTION N: TITLE ═══ -->`. The `═══` decorations are required. Use `SECTION N`, never `§N`. Titles are uppercase from the fixed list (CLARIFYING QUESTIONS, THE INSIGHT, BRUTE FORCE, TRANSLATIONS, ALGORITHM IN PLAIN ENGLISH, CODE, CODE VISUALIZATION, DRY RUN, CORNER CASES, PRODUCTION READINESS, APPROACHES, COMPLEXITY, TAKE HOME). Lint enforces this.

---

## Token budget per lesson

Authoring one lesson should fit in ~60k tokens of read context. If a session loads more, something redundant is being read.

| Item | Tokens (~) | Load |
|---|---|---|
| `LESSON_DESIGN.md` (this file) | 1.5k | once |
| `design/archetypes.md` | 0.5k | once |
| `design/python_verify.md` | 1.0k | once (for plan trace) |
| `static/CLASSES.md` | 2.0k | once |
| `lessons/_template.html` | 4.0k | once |
| `design/sec<N>_*.md` (loaded per section, ×13) | 12k | per section |
| Inline canonical §1 pattern (one of four in `sec1_insight.md`) | 1.5k | when authoring §1 |
| `plan.md` being authored | 3k | written |
| `lesson.html` being authored | 18k | written |
| **Total** | **~42k read + ~21k written ≈ 63k** | |

**Do NOT load:**
- Full golden `lesson.html` files (788–1184 lines each, +15–25k tok). Use the inline canonical pattern in `design/sec1_insight.md` instead; load other goldens only via the named line range in a section file's "Reference excerpts" block.
- `static/lesson.css` (full file). Use `static/CLASSES.md` for class vocabulary.
- `lessons/archive/LESSON_DESIGN_v2.md` (legacy monolith, 239 lines). The partitioned `design/` files supersede it.
- Sibling lesson `plan.md` or `lesson.html` "for inspiration". Re-derive archetype, examples, and pacing per problem.

---

## Section index — load on demand

| §  | Title                          | Load when authoring this section                                |
|----|--------------------------------|------------------------------------------------------------------|
| 0  | Before you code                | `design/sec0_clarifying.md`                                      |
| 1  | The Insight                    | `design/sec1_insight.md` + `design/known_bugs.md`                |
| 2  | Step 1: Brute force            | `design/sec2_brute_force.md`                                     |
| 3  | Step 2: Translations           | `design/sec3_translations.md`                                    |
| 4  | Step 3: Algorithm in English   | `design/sec4_algorithm_english.md`                               |
| 5  | Step 4: Code                   | `design/sec5_code.md` + `design/code_style.md`                   |
| 6  | Step 5: Code visualization     | `design/sec6_code_viz.md` + `design/code_style.md`               |
| 7  | Step 6: Dry run                | `design/sec7_dry_run.md` + `design/known_bugs.md`                |
| 8  | Step 7: Corner cases           | `design/sec8_corner_cases.md`                                    |
| 9  | Step 8: Production checklist   | `design/sec9_production.md`                                      |
| 10 | Step 9: Approaches             | `design/sec10_approaches.md`                                     |
| 11 | Step 10: Complexity            | `design/sec11_complexity.md`                                     |
| 12 | Take home                      | `design/sec12_take_home.md`                                      |

Each `design/sec<N>_*.md` ends with a **Reference excerpts** block pointing to line ranges in the canonical golden. Open only the linked range — never the full golden file.

---

## Before any HTML is written

1. Load [`design/archetypes.md`](./design/archetypes.md) to classify the problem and choose the canonical golden.
2. Load [`design/python_verify.md`](./design/python_verify.md) and run a Python trace of the algorithm against every planned example. Do not start the HTML until the trace matches expected output.

## Per-lesson, after the spec is approved

Load [`design/layout.md`](./design/layout.md) once for page-width / formula-panel / keyboard router constraints.

---

## Quality bar

Reference goldens (do **not** load wholesale):

- `lessons/3sum/lesson.html`
- `lessons/permutation-in-string/lesson.html`
- `lessons/trapping-rain-water/lesson.html`
- `lessons/median-of-two-sorted-arrays/lesson.html`

Always use the **Reference excerpts** ranges in each section file.

---

## Provenance

Files under `lessons/design/` were partitioned verbatim from `lessons/LESSON_DESIGN_v2.md` per [PLAN-011](../AGENT_MD/plan/plans/PLAN-011_lesson_gen_efficiency.md) on 2026-05-14. The monolith is retained at [`lessons/archive/LESSON_DESIGN_v2.md`](./archive/LESSON_DESIGN_v2.md) as historical reference (moved per PLAN-016 on 2026-05-20).
