# Section 11 — Step 10: Complexity

## Principle

A two-card grid: time on the left, space on the right. Each card has the big-O symbol prominently and a one-sentence explanation of why that bound holds.

This section is intentionally short. The complexity has already been hinted at throughout (§3 translations carry `.wt-gain` lines, §10 tabs carry `.tag-time`/`.tag-space`). Section 11 just centralises it.

## Format

```
Time          O(n²)
              Outer loop is n iterations; the inner two-pointer pass is O(n).

Space         O(1) auxiliary
              The result vector is output, not auxiliary.
```

## Markup

- Container: `<div class="section">` with `.sec-title` "Complexity".
- Grid: `<div class="cplx-grid">` containing two `<div class="ccard">`.
- Each card: `.ccard-l` (label: "Time" / "Space"), `.ccard-v` (big-O value in mono), `.ccard-n` (one-sentence explanation).

## Style

- Distinguish **input** space from **auxiliary** space when relevant. "O(1) auxiliary" is the honest framing when the result vector is technically output but counted as space by some grading rubrics.
- For recursive algorithms call out stack depth separately if it differs from auxiliary heap space.

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 421–430 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 619–628 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 452–462 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 504–513 |
