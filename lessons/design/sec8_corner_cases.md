# Section 8 — Step 7: Corner cases

## Principle

Each corner case is one card explaining (a) what the input is, (b) why it is corner-ish, (c) what the algorithm returns and why. Three to five cards per lesson.

The format trains the reader to enumerate edge inputs *before* declaring a solution done — the same habit interviewers expect.

## Format

```
1. Empty input
   Input: []
   The for-loop body never executes; result stays empty. Returned as-is.

2. All-same input
   Input: [0,0,0,0]
   First iteration finds {0,0,0}; dedup-skip logic moves i past the remaining zeros.

3. No triplets sum to zero
   Input: [1,2,3]
   The while loop exhausts; result stays empty.
```

Distinct from §9 (production checklist), which is a flat checklist of *categories* to remember. §8 is per-input narrative.

## Markup

- Container: `<div class="section">` with `.sec-title` "Corner cases".
- Each case: `<div class="corner">` containing `.cnum` (number circle) + a body with `.corner-title` (input + label) + `.corner-body` (the explanation).

## Selection

- One empty / minimum-size input.
- One "all same" or otherwise degenerate input.
- One "no answer exists" input.
- One input that exercises the dedup / overflow / boundary logic specifically introduced by this problem.

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 359–384 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 556–581 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 379–404 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 441–466 |
