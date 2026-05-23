# REPORT-018: Lesson Uniformity Contract — Outcomes

**Plan:** [PLAN-018](../plans/PLAN-018_lesson_uniformity_contract.md)
**Status:** Completed
**Date:** 2026-05-21

---

## 1. Outcome at a glance

| Metric | Before | After |
|---|---|---|
| Generated lessons | 17 | 17 |
| Audit PASS | 9 | **17** |
| Audit WARN | 6 | 0 |
| Audit FAIL | 2 | 0 |
| Section marker variants | 3 (`═══ SECTION`, `SECTION`, `§N`) | **1** (`═══ SECTION N: TITLE ═══`) |
| Lessons with animated §1 | 9 | **17** |
| Lessons in LEGACY_GOLDENS allowlist | 9 | **0** |
| Lint rules in lint_lesson.py | 19 | 21 (+ marker canonical, + color palette) |

## 2. What shipped

5 commits on `master` between commit `a2060ab` and `5931fa1`:

1. `a2060ab` — chore(lessons): normalize section markers + audit by lesson_status
2. `84deea9` — feat(lessons): backfill animated §1 into 6 legacy goldens
3. `5b40eb4` — docs(lessons): add PLAN-011 schema to 5 legacy goldens' plan.md
4. `65803af` — feat(lessons): rewrite majority-element and majority-element-ii to canonical §1
5. `5931fa1` — feat(lint): strengthen uniformity contract — drop legacy bypass, add marker+color checks

Combined diff stat (across the 5 commits): roughly +1,400 lines of new §1 HTML/JS, +125 lines of plan.md schema, +53 lines of lint changes, –200 lines of stub or hex-color removal.

## 3. Per-lesson before/after

| Lesson | Pre-PLAN-018 | Post-PLAN-018 |
|---|---|---|
| 3sum | WARN (no animation, plan schema gap) | PASS |
| container-with-most-water | WARN (no animation, plan schema gap) | PASS |
| count-permutations-with-inversion-requirement | WARN (no animation) | PASS |
| find-the-duplicate-number | PASS | PASS (palette tightened) |
| first-missing-positive | PASS | PASS |
| majority-element | FAIL (24-line stub) | PASS (Boyer-Moore animation) |
| majority-element-ii | FAIL (27-line stub) | PASS (two-slot animation) |
| maximum-subarray | PASS | PASS |
| median-of-two-sorted-arrays | WARN (no animation, plan schema gap) | PASS |
| merge-intervals | PASS | PASS |
| permutation-in-string | WARN (no animation, plan schema gap) | PASS |
| product-of-array-except-self | PASS | PASS |
| repeated-substring-pattern | PASS | PASS (palette tightened) |
| spiral-matrix | PASS | PASS (palette tightened) |
| trapping-rain-water | WARN (no animation, plan schema gap) | PASS |
| two-sum | PASS | PASS |
| valid-palindrome | PASS | PASS |

## 4. Contract enforced by lint

A lesson now fails (not warns) if any of the following is missing:

- `<!-- ═══ SECTION N: TITLE ═══ -->` exactly for every section marker (titles drawn from the fixed list in `LESSON_DESIGN.md`).
- §1 has `siNext()`, `siPrev()`, `siTogglePlay()`, `siReset()` button bindings (≥ 3 of 4).
- §1 references a `siGenSteps` function definition somewhere in the lesson.
- Each of info / success / warn tiers appears (as bg-, text-, or border- variant) somewhere in the lesson.
- §1 has either a `chain-box` with ≥ 3 rows + 2 examples OR a "visual-led" §1 with ≥ 30 lines before kernel infobox AND kernel ≤ 350 chars.
- §1 line count ≥ 45.
- Kernel body paragraph ≥ 180 chars and not starting with "iterate"/"loop"/"first".
- `lesson.css` and `lesson.js` linked from `static/`.
- Plan.md has `## Metadata` + `Archetype:` + `## 1. Clarifying questions` (warn-only; legacy goldens have these now).

## 5. Cost paid

- Token spend: significant — roughly 30 minutes of focused editing per legacy lesson backfill (6 lessons) + 15 minutes per FAIL stub rewrite (2 lessons). The marker normalization was a one-shot script (< 1 min).
- Risk introduced: the strengthened lint will block any new lesson that doesn't comply. This is the intended behavior but means the batch-lesson skill will surface failures rather than warnings — author needs to iterate to PASS before PATCHing `lesson_status=generated`.

## 6. Lessons learned

- **Legacy carve-outs decay into noise.** The `LEGACY_GOLDENS` set was meant as a temporary bypass; it lingered for 4 plans (015 → 018) and protected what turned out to be straightforward backfill work. The lesson: bypasses should have a documented expiry condition or they become permanent.
- **Hard-coded hex colors are the easiest drift to introduce and the hardest to spot.** Three of the "PASS" PLAN-015 lessons had drifted to `#fee2e2` / `#3b82f6` / `#dcfce7` instead of `var(--bg-info)` etc. The new color-palette lint check catches this automatically.
- **Section markers were a no-cost consistency win** — a 70-line one-shot script turned 3 variant formats into one. Should have been done in PLAN-011 when the markers were first formalised.

## 7. Follow-ups (none scheduled)

- Decide whether to promote `move-zeroes` and `two-sum-ii-input-array-is-sorted` from scaffold to generated (requires full §1 build to PASS the lint).
- If find-the-duplicate-number's 4-pointer animation ever becomes a problem (e.g., lint extension to forbid hex), refactor the "meet" indicator to a canonical variant or document a per-lesson exception mechanism.
- The dashboard audit could be surfaced as a visible status (green/yellow/red) on each lesson card — currently you have to run `python3 scripts/audit_lessons.py` manually.
