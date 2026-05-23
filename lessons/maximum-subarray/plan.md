# Maximum Subarray — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `maximum-subarray`
- **LC #:** 53
- **Difficulty:** Medium
- **Topic:** Arrays / DP
- **Archetype:** `prefix_scan` (closest fit — single-pass running aggregate; canonical golden: `lessons/trapping-rain-water/lesson.html`. Note: this is fundamentally Kadane's 1D DP; we borrow only the visualisation template, not the two-pointer squeeze.)

## 1. Clarifying questions (§0)

1. **Q:** "Can the array contain only negative numbers?"
   **A:** Yes. The array has at least one element; it may be all negative.
   **Unlocks:** Rules out "track running sum, return 0 if it never goes positive." The answer for `[-3,-1,-4,-2]` is `-1`, not `0` — we must accept the **least bad** single element.

2. **Q:** "Must the subarray be contiguous?"
   **A:** Yes — that's the defining constraint.
   **Unlocks:** Frees us from any subset-sum machinery; we only consider windows defined by `(start, end)` pairs.

3. **Q:** "Do we return the sum, or the subarray itself?"
   **A:** Just the sum (the integer).
   **Unlocks:** No need to track start/end indices. Two integers — `cur` (best ending here) and `best` (best seen so far) — are enough.

4. **Q:** "Are we guaranteed at least one element?"
   **A:** Yes; the constraint is `n ≥ 1`.
   **Unlocks:** Initialise `cur = best = nums[0]` and start the loop at `i = 1`. No empty-array branch needed.

## 2. Kernel paragraph (§1)

For every position `i`, ask: "what is the largest sum of a contiguous subarray that **ends exactly at** `i`?" Call that `cur(i)`. The choice is binary: either extend the best subarray ending at `i-1` by appending `nums[i]`, or throw it away and start fresh at `nums[i]`. Restart wins exactly when the running sum was negative — adding it would only hurt. The global answer is the maximum of `cur(i)` over all `i`. One scan, two integers: `cur` (current best ending here) and `best` (max of `cur` seen so far).

## 3. Foundational concept visual (§1)

A horizontal row of `nums` cells. A blue "running window" highlight grows rightwards while `cur ≥ 0`, then snaps back to a single cell when `cur` would drop below the new element (restart). A small green "best so far" badge above the row updates whenever `cur` exceeds the previous best. The visual makes the "extend vs. restart" decision visible at every step.

## 4. Translations (§3)

1. **"Maximum sum over all contiguous subarrays"** → `max over i of (best subarray ending at i)`. Reduces a two-dimensional `(start, end)` search to a single pass over end positions.
2. **"Best subarray ending at i"** → `cur(i) = max(nums[i], cur(i-1) + nums[i])`. The DP recurrence — the only choice is "extend" or "restart at i".
3. **"Restart vs. extend"** → equivalent to: throw away any prefix whose running sum is negative. `cur(i) = nums[i] + max(0, cur(i-1))`.
4. **`cur(i)` only depends on `cur(i-1)`** → the DP array collapses to a single integer. O(n) time, O(1) extra space.

## 5. Algorithm in plain English (§4)

1. Initialise `cur = nums[0]` and `best = nums[0]`.
2. For each `i` from 1 to `n−1`:
   a. **Decide:** if `cur + nums[i] >= nums[i]`, extend (`cur = cur + nums[i]`); otherwise restart (`cur = nums[i]`). Equivalent to `cur = max(nums[i], cur + nums[i])`.
   b. **Record:** `best = max(best, cur)`.
3. Return `best`.

## 6. Examples for code viz + dry run (§6, §7)

### Fast example (9 steps): `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]` → `6`

The classic LC #53 example. Restarts at i=1 (drops -2) and i=3 (drops a negative running sum), then extends through `[4,-1,2,1] = 6`. Even after `-5` drops `cur` to 1, `best=6` survives.

### Slow example (11 steps): `nums = [5, -3, 2, 4, -7, 3, 2, 1, -2, 6, -3]` → `11`

11 steps walking through three regimes: an initial extension run (`5,-3,2,4` → cur peaks at 8), a near-restart that survives (`-7` drops cur to 1 but doesn't trigger a fresh start), a slow climb (`3,2,1` → cur hits 7), a small dip (`-2` → 5), and a closing burst (`+6` → cur=11, new best). Demonstrates that "extend" is the winning move even after a sharply negative element, as long as the running sum stays positive.

## 7. Corner cases (§8)

1. **Single element** — `[7]` → 7; `[-7]` → -7. Loop body never runs; we return the initial `best = nums[0]`.
2. **All negatives** — e.g. `[-3,-1,-4,-2]` → -1. Every step restarts (extending only worsens things). The answer is the largest single element. This is why `cur` and `best` initialise to `nums[0]`, not 0.
3. **All positives** — `[1,2,3]` → 6. Every step extends; no restart ever fires. `cur` and `best` move in lockstep.
4. **Single positive surrounded by negatives** — `[-5, 3, -5]` → 3. The lone positive briefly resets `cur`, sets `best = 3`, then drops back below.
5. **Zero in the mix** — `[0, -1, 2]` → 2. A `0` extends without changing `cur`. Equivalence: `nums[i] = 0` means "extend" and "restart" produce the same `cur`.

## 8. Approaches comparison (§10)

1. **Brute force (O(n²))** — for every `(start, end)` pair, sum and compare. With a running prefix sum the inner step is O(1), giving O(n²) total. Correct but TLEs for n in the hundred-thousands.
2. **Divide & conquer (O(n log n))** — split the array in half. The maximum subarray is either entirely in the left half, entirely in the right half, or crosses the midpoint. The cross-midpoint case requires an O(n) two-direction scan. Recurrence T(n) = 2T(n/2) + O(n) → O(n log n). Elegant but strictly worse than Kadane's; useful as an interview "what other approaches are there?".
3. **Kadane's (O(n), chosen)** — single pass, `cur` and `best` integers. Strictly dominates the other two on time. The DP recurrence collapses to two variables.

## 9. Take home (§12)

- **LC 152 Maximum Product Subarray** — same single-pass shape, but products flip sign on negatives, so we must track both a running max **and** a running min (the most-negative product can become the new max if multiplied by another negative).
- **LC 918 Maximum Sum Circular Subarray** — extend Kadane's: the answer is either a normal max-subarray, or `total − min-subarray` (the wraparound). One pass with min and max kadane.
- **LC 121 Best Time to Buy and Sell Stock** — same single-pass running variable idea, but the recurrence is `best = max(best, prices[i] − min_so_far)`.
- **LC 1567 Maximum Length of Subarray With Positive Product** — track running counts of positive vs. negative product run lengths instead of a sum.

## 10. Python verification (BEFORE writing HTML)

Algorithm under test:

```python
def max_subarray(nums):
    cur = best = nums[0]
    for i in range(1, len(nums)):
        cur = max(nums[i], cur + nums[i])
        best = max(best, cur)
    return best
```

Trace output (all four examples pass):

```
Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
  init: cur=-2, best=-2
  i=1 nums[i]=  1: cur=max(1, -2+1=-1)=  1 [restart]; best=1
  i=2 nums[i]= -3: cur=max(-3, 1+-3=-2)= -2 [extend]; best=1
  i=3 nums[i]=  4: cur=max(4, -2+4=2)=  4 [restart]; best=4
  i=4 nums[i]= -1: cur=max(-1, 4+-1=3)=  3 [extend]; best=4
  i=5 nums[i]=  2: cur=max(2, 3+2=5)=  5 [extend]; best=5
  i=6 nums[i]=  1: cur=max(1, 5+1=6)=  6 [extend]; best=6
  i=7 nums[i]= -5: cur=max(-5, 6+-5=1)=  1 [extend]; best=6
  i=8 nums[i]=  4: cur=max(4, 1+4=5)=  5 [extend]; best=6
Result:   6
Expected: 6
OK

Input: [5, -3, 2, 4, -7, 3, 2, 1, -2, 6, -3]
  init: cur=5, best=5
  i=1 nums[i]= -3: cur=max(-3, 5+-3=2)=  2 [extend]; best=5
  i=2 nums[i]=  2: cur=max(2, 2+2=4)=  4 [extend]; best=5
  i=3 nums[i]=  4: cur=max(4, 4+4=8)=  8 [extend]; best=8
  i=4 nums[i]= -7: cur=max(-7, 8+-7=1)=  1 [extend]; best=8
  i=5 nums[i]=  3: cur=max(3, 1+3=4)=  4 [extend]; best=8
  i=6 nums[i]=  2: cur=max(2, 4+2=6)=  6 [extend]; best=8
  i=7 nums[i]=  1: cur=max(1, 6+1=7)=  7 [extend]; best=8
  i=8 nums[i]= -2: cur=max(-2, 7+-2=5)=  5 [extend]; best=8
  i=9 nums[i]=  6: cur=max(6, 5+6=11)= 11 [extend]; best=11
  i=10 nums[i]= -3: cur=max(-3, 11+-3=8)=  8 [extend]; best=11
Result:   11
Expected: 11
OK

Input: [-3, -1, -4, -2]
  init: cur=-3, best=-3
  i=1 nums[i]= -1: cur=max(-1, -3+-1=-4)= -1 [restart]; best=-1
  i=2 nums[i]= -4: cur=max(-4, -1+-4=-5)= -4 [restart]; best=-1
  i=3 nums[i]= -2: cur=max(-2, -4+-2=-6)= -2 [restart]; best=-1
Result:   -1
Expected: -1
OK

Input: [1, 2, 3]
  init: cur=1, best=1
  i=1 nums[i]=  2: cur=max(2, 1+2=3)=  3 [extend]; best=3
  i=2 nums[i]=  3: cur=max(3, 3+3=6)=  6 [extend]; best=6
Result:   6
Expected: 6
OK
```
