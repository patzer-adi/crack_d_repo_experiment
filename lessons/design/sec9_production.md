# Section 9 — Step 8: Production readiness checklist

## Principle (from v2 §21)

Section 9 is a **visual checklist with green checkmarks**, not prose. One line per item. Each item has a bold label and a one-sentence explanation. The format trains the interview habit of running through edge cases before calling code done.

## Cover at minimum

- Empty input
- All-same input
- No-match case
- Integer overflow (especially for sum / product algorithms)
- Off-by-one in loop bounds
- Any problem-specific edge case (e.g. dedup correctness in 3Sum, priming completeness in sliding-window)

## Format

```
✓ Empty input — return early on null or size < 3
✓ Integer overflow — cast to long before summing or use a 64-bit accumulator
✓ Off-by-one — outer loop is i ≤ n−3, inner pointers are L = i+1 and R = n−1
✓ Dedup output — skip i when nums[i] == nums[i-1]; skip L/R after recording a triplet
```

Distinct from §8 (per-input narrative). §9 is a flat checklist of *categories* to remember.

## Markup

- Container: `<div class="section">` with `.sec-title` "Production readiness".
- Checklist: `<div class="checklist">` containing one `<div class="chk-item">` per row.
- Each row: `.chk-icon` (green circle with ✓) + `.chk-text` (use `<b>` for the label, plain text for the explanation).

## Length

5–8 items. Fewer feels incomplete; more starts to overlap with the corner-cases section.

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 385–397 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 582–595 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 405–417 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 467–480 |
