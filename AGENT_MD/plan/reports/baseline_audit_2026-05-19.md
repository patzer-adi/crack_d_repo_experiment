# REPORT-016 (baseline audit): Lesson lint state at PLAN-016 gate landing

**Plan:** PLAN-016 (in-progress)
**Captured:** 2026-05-19
**Author:** AI agent (during PLAN-016 task 10)

> This is a baseline snapshot, captured the moment the lint gate first ran
> against all lessons. It is **not** the final REPORT-016 — that is written
> at PLAN-016 completion (task 14). Its purpose is to seed PLAN-015's
> remediation scope with the exact list of lessons the gate rejects.

---

## 1. Summary

`scripts/audit_lessons.py` walked all 19 lessons in `lessons/` and ran the
PLAN-016 lint on each. Results: **3 pass, 4 warn-only, 12 fail.**

The four canonical goldens (`3sum`, `permutation-in-string`,
`trapping-rain-water`, `median-of-two-sorted-arrays`) all show as WARN, not
PASS, because their `plan.md` predates the PLAN-011 schema. Their HTML §1
sections pass cleanly — the warnings are informational and concern only the
plan.md sidecar, not the lesson HTML the reader sees.

## 2. Audit output

```
Lesson audit (PLAN-016 lint over all lessons)
────────────────────────────────────────────────────────────
  WARN   3sum                                           plan.md schema warnings (legacy plan)
  FAIL   container-with-most-water                      longest body paragraph is 162 chars; minimum is 180
  FAIL   count-permutations-with-inversion-requirement  plan.md missing; §1: no chain-box; visual-led kernel 399 chars (max 350)
  FAIL   find-the-duplicate-number                      §1: no chain-box; visual-led kernel 587 chars (max 350)
  FAIL   first-missing-positive                         §1: 32 lines (< 45); no chain-box; only 26 visual lines (< 30)
  FAIL   majority-element                               section 1 (THE INSIGHT) comment marker not found
  FAIL   majority-element-ii                            section 1 (THE INSIGHT) comment marker not found
  FAIL   maximum-subarray                               §1: 25 lines (< 45); no chain-box; only 15 visual lines (< 30)
  WARN   median-of-two-sorted-arrays                    plan.md schema warnings (legacy plan)
  FAIL   merge-intervals                                §1: 25 lines (< 45); no chain-box; only 15 visual lines (< 30)
  FAIL   move-zeroes                                    §1: 17 lines (< 45); no sec-title; no body paragraph; no chain-box
  WARN   permutation-in-string                          plan.md schema warnings (legacy plan)
  FAIL   product-of-array-except-self                   §1: 25 lines (< 45); no chain-box; only 16 visual lines (< 30)
  PASS   repeated-substring-pattern                     —
  FAIL   spiral-matrix                                  §1: 41 lines (< 45); no chain-box; visual-led kernel 492 chars (max 350)
  WARN   trapping-rain-water                            plan.md schema warnings (legacy plan)
  PASS   two-sum                                        —
  FAIL   two-sum-ii-input-array-is-sorted               §1: 17 lines (< 45); no sec-title; no body paragraph; no chain-box
  PASS   valid-palindrome                               —
────────────────────────────────────────────────────────────
  Totals: 3 pass, 4 warn, 12 fail  (of 19 lessons)
```

## 3. Categorisation of failures

### 3.1 Confirmed quality drift (PLAN-015 §2 scope — already named)

These match the user's flagged set on 2026-05-19. PLAN-015 §2 already targets them:

| Slug | Why lint fails | Severity |
|---|---|---|
| spiral-matrix | §1 short (41 lines) + algorithm-dump kernel (492 chars) | High |
| find-the-duplicate-number | algorithm-dump kernel (587 chars) | High |
| first-missing-positive | §1 short (32 lines) + small visual + no chain-box | High |
| maximum-subarray | §1 severely short (25 lines) + no chain-box | High |
| merge-intervals | §1 severely short (25 lines) + no chain-box | High |
| product-of-array-except-self | §1 severely short (25 lines) + no chain-box | High |
| count-permutations-with-inversion-requirement | plan.md missing AND §1 visual-led kernel too long (399 chars) | High |

### 3.2 Additional discoveries (NOT in PLAN-015 scope yet)

The audit surfaced lessons the user hadn't flagged. These require a scope decision:

| Slug | Why lint fails | Recommendation |
|---|---|---|
| container-with-most-water | §1 has chain-box + 89 lines but kernel paragraph is only 162 chars (3 below the 180 floor) | Touch up kernel paragraph; ~10 min. Lesson is otherwise golden-quality. |
| majority-element | `<!-- SECTION 1: THE INSIGHT -->` comment marker missing entirely | Investigate — may use legacy section comment format. Add marker OR adjust lint to also accept legacy markers. |
| majority-element-ii | Same as majority-element | Same as majority-element |
| move-zeroes | §1 is 17 lines, no sec-title, no body paragraph | Lesson is for an easy problem (LC 283). §1 may have been deliberately minimal. Decide: rewrite to standard or document the carve-out. |
| two-sum-ii-input-array-is-sorted | §1 is 17 lines, no sec-title, no body paragraph | Same as move-zeroes — easy problem, minimal §1. Same decision. |

### 3.3 Warn-only (no action needed for PLAN-015)

The four named goldens warn on plan.md schema because their plan.md was authored before PLAN-011 (May 2026-05-08 to 2026-05-13, before PLAN-011 landed on 2026-05-14). Their HTML §1 sections pass cleanly. Backfilling plan.md to PLAN-011 schema for the goldens is a low-priority cleanup; the warning is informational.

| Slug | Warnings |
|---|---|
| 3sum | plan.md schema (3 missing PLAN-011 markers) |
| permutation-in-string | plan.md schema (3 missing PLAN-011 markers) |
| trapping-rain-water | plan.md schema (3 missing PLAN-011 markers) |
| median-of-two-sorted-arrays | plan.md schema (3 missing PLAN-011 markers) |

## 4. Impact on PLAN-015 scope

PLAN-015 currently lists 8 lessons (the 7 named in §1.1 + valid-palindrome chain-content deepening). The audit confirms 7 of those are lint-failing.

**valid-palindrome passes lint** structurally — the chain-box exists, kernel is 383 chars, line count is 85. PLAN-015 §2 still calls for *deepening the chain content* (each ≡ row showing a real reduction, not a restatement). This is a quality concern lint cannot catch — it remains as a Layer 2 (LLM self-review) concern, captured in PLAN-015's task 11.

**PLAN-015 should also decide:**
- Whether to expand scope to cover container-with-most-water (kernel touch-up, ~10 min).
- Whether the majority-element / majority-element-ii section-marker mismatch is a lint bug or a legacy lesson migration item.
- Whether to standardize move-zeroes / two-sum-ii §1 to the 45-line floor or carve them out as "trivial-problem" lessons.

These can be folded into PLAN-015 phase 3 (special cases) without adding a new plan.

## 5. Pass set (working as intended)

| Slug | Notes |
|---|---|
| repeated-substring-pattern | Recently authored, chain-box + 86-line §1. Functions as a 5th informal golden. |
| two-sum | 95-line §1 with chain-box. Authored 2026-05-14 alongside PLAN-011 landing. |
| valid-palindrome | 85-line §1 with chain-box. Structurally passes; chain content depth is a Layer 2 concern. |

---

## 6. What this baseline enables

- PLAN-015 can quote this exact failure list as its work definition.
- A re-run of `audit_lessons.py` after each PLAN-015 rewrite measures progress objectively.
- The four pass + four warn lessons act as a regression set — none of them should slip into FAIL after any future change.
