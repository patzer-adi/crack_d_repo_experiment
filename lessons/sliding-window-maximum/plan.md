# Sliding Window Maximum — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `sliding-window-maximum`
- **LC #:** 239
- **Difficulty:** Hard
- **Topic:** Sliding Window / Monotonic Deque
- **Archetype:** `sliding_window` (problem framing) — but the optimization being
  taught is a **monotonic deque**, not a frequency-diff counter. We borrow the
  window framing from `permutation-in-string` and write a custom deque step
  generator (no archetype golden carries this pattern).

## 1. Clarifying questions (§0)

1. **Q: How many results do we return?**
   A: `n − k + 1` — one max per window. The first window starts at index 0,
   the last starts at `n − k`.
   **Unlocks:** We only record after the window is full (i ≥ k − 1).

2. **Q: Can elements be negative or zero?**
   A: Yes — `−10⁴ ≤ nums[i] ≤ 10⁴`. So 0 is not a safe sentinel for "missing"
   or "smaller than everything".
   **Unlocks:** Compare values directly. Never use 0 or −1 as a magic value.

3. **Q: Can k exceed the array length?**
   A: No — guaranteed `1 ≤ k ≤ n`. We never have to return an empty result or
   handle an under-sized array.
   **Unlocks:** Skip k>n guard. Inner loops are well-defined.

4. **Q: Can the array contain duplicates?**
   A: Yes. If two equal values are both in the window, either one is a valid
   "max". The algorithm doesn't need to break the tie — but the "pop back
   while ≤" rule keeps things tidy by evicting older duplicates.
   **Unlocks:** Use `≤` (not `<`) when popping from the back of the deque.

## 2. Kernel paragraph (§1)

For each window of size k we want a max. The brute force re-scans all k
elements every time the window slides — O(n·k). Key observation: when a new
value `v` enters the window at index `i`, every smaller value to its left is
**permanently dominated**. Those smaller values can never beat `v` for any
future window that contains `v`, because `v` itself sits in those windows
too, and the window only loses elements from its left. So we can discard
dominated values as soon as we see them. The set of "still-possibly-maxima"
indices forms a sequence whose values are monotonically decreasing
left-to-right. The front of this sequence is always the current window's
max — until its index slides out of the window's left edge, at which point we
drop it.

## 3. Foundational concept visual (§1)

A bar chart of nums (heights = values) with the current window highlighted as
a tinted band. Below the bars, a row of "deque slots" shows the indices that
are still live candidates. As we sweep `i` left to right, smaller back-of-deque
entries grey out and disappear (dominated by the new value), and any front
entry whose index slides past the window's left edge greys out too. The slot
labeled "current max" reads the value at the deque's front.

This visual makes the kernel sentence visible: **the deque is the chain of
"could still be max" candidates, monotonically decreasing in value, in
left-to-right index order.**

Animation: 8 steps over the canonical LC example `[1,3,−1,−3,5,3,6,7]`, k=3 —
one step per "decision point" (push, pop-back, pop-front, record).

## 4. Translations (§3)

| Plain-English phrase | Code construct |
|---|---|
| "sliding window of size k" | `[i−k+1 .. i]` once `i ≥ k−1` |
| "still-candidate maxima" | `dq: deque[int]` storing indices |
| "discard smaller values to the left" | `while dq and nums[dq[-1]] ≤ nums[i]: dq.pop()` |
| "add the new candidate" | `dq.append(i)` |
| "front fell out of the window" | `if dq[0] ≤ i − k: dq.popleft()` |
| "record the current window's max" | `if i ≥ k−1: out.append(nums[dq[0]])` |

## 5. Algorithm in plain English (§4)

1. Create an empty deque (it stores **indices**, not values).
2. Walk `i` from 0 to n−1.
3. Pop from the **back** of the deque while its value is ≤ `nums[i]` (those
   indices are now dominated).
4. Push `i` onto the back.
5. If the **front** index is ≤ `i − k`, it's outside the current window —
   pop it from the front.
6. Once `i ≥ k − 1`, append `nums[dq[0]]` to the result.
7. Return the result list.

## 6. Examples for code viz + dry run (§6, §7)

**Fast example (§6 walkthrough):** `nums = [1,3,1,2], k = 2`
- Expected: `[3, 3, 2]`
- ~5 decision-point steps. Demonstrates push, pop-back, pop-front in
  compressed form.

**Slow example (§7 default):** `nums = [1,3,−1,−3,5,3,6,7], k = 3` (LC sample)
- Expected: `[3, 3, 5, 5, 6, 7]`
- ~16 decision-point steps. Covers the dramatic clearing at i=4 (value 5
  evicts three back entries) and the front-pop at i=6 (index 1 expires).

**§7 dry-run example buttons (≥ 3):**
1. `[1,3,−1,−3,5,3,6,7], k=3` → `[3,3,5,5,6,7]` (canonical LC).
2. `[5,4,3,2,1], k=3` → `[5,4,3]` (deque grows monotonically; front-pop on
   every step after the first window).
3. `[1,2,3,4,5], k=3` → `[3,4,5]` (every step clears the back to empty —
   shows the "rebuild from scratch" extreme).
4. `[7,7,7,7], k=2` → `[7,7,7]` (duplicates — proves `≤` not `<`).

## 7. Corner cases (§8)

| Case | Input | Expected | Why it's interesting |
|---|---|---|---|
| Single element | `[5], k=1` | `[5]` | Loop body runs once; window full on first step. |
| k = 1 | `[1,−1], k=1` | `[1,−1]` | Front-pop fires every iteration; result = nums. |
| k = n | `[9,11], k=2` | `[11]` | One window only; pop-back drains earlier larger value if monotone, otherwise survives. |
| Strictly decreasing | `[5,4,3,2,1], k=3` | `[5,4,3]` | Deque only grows from the back; front-pop drives the answer. |
| Strictly increasing | `[1,2,3,4,5], k=3` | `[3,4,5]` | Deque is cleared from the back on every step. |
| All equal | `[5,5,5,5], k=2` | `[5,5,5]` | `≤` pops equal-valued entries — older duplicates make way for newer ones (which expire later). |

## 8. Approaches comparison (§10)

| Approach | Time | Space | Trade-off |
|---|---|---|---|
| **Brute force (nested loop)** | O(n·k) | O(1) | Recompute max for every window from scratch. Simplest to write, but TLE on n=10⁵, k≈10⁵. |
| **Max-heap with lazy deletion** | O(n log n) | O(n) | Push (value, index) onto a heap. When popping the top, discard while its index is outside the window. Asymptotically slower than the deque, and uses a heavier data structure. Wins only when the language has no native deque. |
| **Monotonic deque** | O(n) | O(k) | Each index is pushed and popped at most once → amortized O(1) per step. The canonical answer. Subtler to derive but smaller, faster, and uses only a deque. |

## 9. Take home (§12)

- **LC 1438 — Longest Continuous Subarray With Absolute Diff ≤ Limit:**
  Two monotonic deques in parallel — one tracking max, one tracking min — so
  we can check `max − min ≤ limit` in O(1) per window. Same "dominated
  candidates" idea, applied twice.
- **LC 862 — Shortest Subarray with Sum at Least K:**
  Monotonic deque, but on **prefix sums** rather than raw values. The same
  "drop dominated entries from the back" rule unlocks O(n).
- **LC 84 — Largest Rectangle in Histogram:**
  Same family of monotonic-stack ideas — keep a stack whose values are
  monotonically increasing; pop when a smaller bar arrives to settle
  rectangles bounded on the right.
- **LC 480 — Sliding Window Median:**
  Sliding window again, but the per-window question is median, not max.
  Two heaps (or an order-statistic tree) replace the deque — the deque trick
  doesn't generalize beyond order-statistics endpoints (min/max).

## 10. Python verification (BEFORE writing HTML)

```
=== verify nums=[1, 3, -1, -3, 5, 3, 6, 7], k=3 ===
  i=0 v=1: push idx=0; deque indices=[0] values=[1]
  i=1 v=3: pop back idx=0 (nums[0]=1 <= 3)
  i=1 v=3: push idx=1; deque indices=[1] values=[3]
  i=2 v=-1: push idx=2; deque indices=[1, 2] values=[3, -1]
  i=2: window=[0..2] max=nums[1]=3; result=[3]
  i=3 v=-3: push idx=3; deque indices=[1, 2, 3] values=[3, -1, -3]
  i=3: window=[1..3] max=nums[1]=3; result=[3, 3]
  i=4 v=5: pop back idx=3 (nums[3]=-3 <= 5)
  i=4 v=5: pop back idx=2 (nums[2]=-1 <= 5)
  i=4 v=5: pop back idx=1 (nums[1]=3 <= 5)
  i=4 v=5: push idx=4; deque indices=[4] values=[5]
  i=4: window=[2..4] max=nums[4]=5; result=[3, 3, 5]
  i=5 v=3: push idx=5; deque indices=[4, 5] values=[5, 3]
  i=5: window=[3..5] max=nums[4]=5; result=[3, 3, 5, 5]
  i=6 v=6: pop back idx=5 (nums[5]=3 <= 6)
  i=6 v=6: pop back idx=4 (nums[4]=5 <= 6)
  i=6 v=6: push idx=6; deque indices=[6] values=[6]
  i=6: window=[4..6] max=nums[6]=6; result=[3, 3, 5, 5, 6]
  i=7 v=7: pop back idx=6 (nums[6]=6 <= 7)
  i=7 v=7: push idx=7; deque indices=[7] values=[7]
  i=7: window=[5..7] max=nums[7]=7; result=[3, 3, 5, 5, 6, 7]
Actual:   [3, 3, 5, 5, 6, 7]
Expected: [3, 3, 5, 5, 6, 7]
OK

=== verify nums=[1, 3, 1, 2], k=2 ===
  i=0 v=1: push idx=0; deque indices=[0] values=[1]
  i=1 v=3: pop back idx=0 (nums[0]=1 <= 3)
  i=1 v=3: push idx=1; deque indices=[1] values=[3]
  i=1: window=[0..1] max=nums[1]=3; result=[3]
  i=2 v=1: push idx=2; deque indices=[1, 2] values=[3, 1]
  i=2: window=[1..2] max=nums[1]=3; result=[3, 3]
  i=3 v=2: pop back idx=2 (nums[2]=1 <= 2)
  i=3 v=2: push idx=3; deque indices=[1, 3] values=[3, 2]
  i=3: pop front idx=1 (expired, window starts at 2)
  i=3: window=[2..3] max=nums[3]=2; result=[3, 3, 2]
Actual:   [3, 3, 2]
Expected: [3, 3, 2]
OK

=== verify nums=[5, 4, 3, 2, 1], k=3 ===
  ... result [5, 4, 3] (matches; deque only grows from the back; front-pop drives output)
OK

=== verify nums=[1, 2, 3, 4, 5], k=3 ===
  ... result [3, 4, 5] (matches; deque cleared to one element on each step)
OK

=== verify nums=[5, 5, 5, 5], k=2 ===
  ... result [5, 5, 5] (matches; ≤ pops equal-valued back entries)
OK

=== verify nums=[1, -1], k=1 ===
  ... result [1, -1] (matches; k=1 means front-pop fires every iteration)
OK

=== verify nums=[9, 11], k=2 ===
  ... result [11] (matches; single window)
OK

=== verify nums=[7], k=1 ===
  ... result [7] (matches; single element)
OK
```

All 8 example cases verified against expected outputs. The Python trace above
is the source of truth for `cvGen` and `drGen` step generators.
