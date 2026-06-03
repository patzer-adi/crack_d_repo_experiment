# Lesson Plan: Minimum Size Subarray Sum (LC #209)

> **Authored:** 2026-06-01.
> Python trace verified before HTML was written (see §10 below).
> lesson.html is complete and matches this plan in full.

## Metadata
- **Slug:** `minimum-size-subarray-sum`
- **LC #:** 209
- **Difficulty:** Medium
- **Topic:** Arrays / Sliding Window / Two Pointers
- **Archetype:** sliding_window (variable-size window, positive elements guarantee monotone sum)

## 1. Clarifying questions (§0)

1. **Q:** Are all elements positive integers?
   **A:** Yes — all nums[i] ≥ 1, target ≥ 1.
   **Unlocks:** Sum is strictly monotone as window grows, so shrinking from L is always safe — sliding window is valid.

2. **Q:** What if no subarray's sum reaches target?
   **A:** Return 0 — the problem defines 0 as the "impossible" sentinel.
   **Unlocks:** Initialise ans = INT_MAX; return 0 if ans was never updated.

3. **Q:** Do we need the subarray itself or just its length?
   **A:** Length only — no need to store indices.
   **Unlocks:** Only four integers needed: n, ans, s, L. O(1) space.

4. **Q:** Can the array be empty?
   **A:** No — 1 ≤ nums.length ≤ 10⁵.
   **Unlocks:** No empty-array guard needed; but must check the "no valid subarray" case at the end.

## 2. Kernel paragraph (§1)

Because every element is positive, adding an element to the right can only increase the running sum, and removing from the left can only decrease it. This monotone property means once the window sum ≥ target we never need to try a smaller R for the same L — we can just shrink L. The shrink-while-valid loop turns two nested loops into a single linear pass: R moves right n times, L moves right at most n times, so every element is visited at most twice → O(n).

## 3. Foundational concept visual (§1)

Animated sliding window strip (array cells, cyan = in window).
Steps show: expand R → add to sum → when sum ≥ target: record length, shrink L.
Variable row below strip: L, R, s, ans updated live.
5–8 steps on Example 1 ([2,3,1,2,4,3], target=7).

## 4. Translations (§3)

1. **Two nested loops → one expanding + one shrinking pointer**
   Keep running sum s and left pointer L. Advance R; add nums[R] to s. When s ≥ target, record length and shrink L until s < target. No inner restart needed.
   → O(n²) with break → O(n) amortized

2. **INT_MAX sentinel → 0-return for impossible case**
   Initialise ans = INT_MAX. After the loop, return `ans == INT_MAX ? 0 : ans`.
   → same O(1) space, cleaner termination

## 5. Algorithm in plain English (§4)

1. **Initialise** L = 0, s = 0, ans = ∞.
2. **Expand** R from 0 to n−1; **add** nums[R] to s.
3. While s ≥ target: **record** ans = min(ans, R−L+1); **subtract** nums[L] from s; **advance** L++.
4. **Return** ans == ∞ ? 0 : ans.

## 6. Examples for code viz + dry run (§6, §7)

| # | Input | Target | Expected | Speed |
|---|-------|--------|----------|-------|
| Ex 1 | [2,3,1,2,4,3] | 7 | 2 | Slow — 11 steps, multiple shrinks |
| Ex 2 | [1,4,4]        | 4 | 1 | Fast — 4 steps, single-element match |
| Ex 3 | [1,1,1,1,1]   | 11 | 0 | Edge — no valid subarray |

## 7. Corner cases (§8)

| Case | Input | Expected | Why |
|---|---|---|---|
| No valid subarray | [1,1,1,1,1], target=11 | 0 | Total sum < target; ans stays INT_MAX → return 0 |
| Single element equals target | [7], target=7 | 1 | Trivially satisfied; shrink loop fires once |
| Whole array is the answer | [1,2,3,4,5], target=15 | 5 | Must include every element |
| First element alone satisfies target | [7,2,2,3], target=7 | 1 | Shrink fires on R=0; rest of array is irrelevant |
| All elements equal target | [4,4,4], target=4 | 1 | Each single element satisfies; ans=1 after first shrink |

## 8. Approaches comparison (§10)

**Tab 1 — Sliding Window (optimal)**
Time: O(n). Space: O(1).
Expand R, shrink L while sum ≥ target. Valid only because all elements are positive (monotone sum). The "while" loop (not "if") handles multiple shrinks per R.

**Tab 2 — Prefix Sum + Binary Search**
Time: O(n log n). Space: O(n).
Build prefix sum array P. For each L, binary-search for smallest R such that P[R+1]−P[L] ≥ target. Valid because P is strictly increasing (positive elements). Dominated by sliding window but useful to know.

**Tab 3 — Brute Force**
Time: O(n²). Space: O(1).
Try every (L, R) pair. TLE on n = 10⁵. Only useful as a correctness reference.

## 9. Take home (§12)

- **LC #3 — Longest Substring Without Repeating Characters:** variable window, shrink on duplicate entry. Condition is character uniqueness, not sum.
- **LC #76 — Minimum Window Substring:** grow-then-shrink with a frequency map diff counter. Same chassis, harder validity condition.
- **LC #424 — Longest Repeating Character Replacement:** variable window, shrink when (len − max_freq) > k.
- **LC #930 — Binary Subarrays With Sum:** extends the pattern from minimum-length to counting.

## 10. Python verification (BEFORE writing HTML)

Verified 2026-06-01. All examples match expected output.

```
=== Example 1: nums=[2,3,1,2,4,3], target=7 ===
  BF result: 2
  R=0 added nums[R]=2 → s=2
  R=1 added nums[R]=3 → s=5
  R=2 added nums[R]=1 → s=6
  R=3 added nums[R]=2 → s=8
    s=8 >= target=7 → window=[0,3] len=4 ans=4, shrink: remove nums[L=0]=2
  R=4 added nums[R]=4 → s=10
    s=10 >= target=7 → window=[1,4] len=4 ans=4, shrink: remove nums[L=1]=3
    s=7 >= target=7 → window=[2,4] len=3 ans=3, shrink: remove nums[L=2]=1
  R=5 added nums[R]=3 → s=9
    s=9 >= target=7 → window=[3,5] len=3 ans=3, shrink: remove nums[L=3]=2
    s=7 >= target=7 → window=[4,5] len=2 ans=2, shrink: remove nums[L=4]=4
  Optimal result: 2  ✓

=== Example 2: nums=[1,4,4], target=4 ===
  BF result: 1
  R=0 added nums[R]=1 → s=1
  R=1 added nums[R]=4 → s=5
    s=5 >= target=4 → window=[0,1] len=2 ans=2, shrink: remove nums[L=0]=1
    s=4 >= target=4 → window=[1,1] len=1 ans=1, shrink: remove nums[L=1]=4
  R=2 added nums[R]=4 → s=4
    s=4 >= target=4 → window=[2,2] len=1 ans=1, shrink: remove nums[L=2]=4
  Optimal result: 1  ✓

=== Example 3: nums=[1,1,1,1,1], target=11 ===
  BF result: 0
  R=0 added nums[R]=1 → s=1
  R=1 added nums[R]=1 → s=2
  R=2 added nums[R]=1 → s=3
  R=3 added nums[R]=1 → s=4
  R=4 added nums[R]=1 → s=5
  Optimal result: 0  ✓
```

## Quality bar
- Self-contained HTML/CSS/JS, no CDN dependencies
- `.panels-fixed` layout (grid-template-rows: 175px 110px) to prevent control shift
- Formula breakdown panel showing L, R, s, ans per step
- Step panel split: `.step-what` (action taken) + `.step-why` (reasoning / window state)
- Keyboard shortcuts: ← → Space R/Esc
- ↺ Reset button, Reveal Code toggle (hidden by default), three approach tabs
- §1 animated window visual with siGenSteps / siRender / siTogglePlay at 1400ms
