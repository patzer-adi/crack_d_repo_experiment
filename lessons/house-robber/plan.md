# House Robber — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `house-robber`
- **LC #:** 198
- **Difficulty:** Medium
- **Topic:** Dynamic Programming
- **Archetype:** `custom` (linear DP, adapted from prefix_scan — per-index local recurrence with O(n) scan)

## 1. Clarifying questions (§0)

1. **Q:** Are the houses arranged in a line, or in a circle?
   **A:** A line. (Circle is LC 213 — House Robber II.)
   **Unlocks:** No wrap-around between nums[0] and nums[n−1]. Rules only forbid *consecutive* indices in the array.

2. **Q:** Can `nums[i]` be zero or negative?
   **A:** Constraint says `0 ≤ nums[i] ≤ 400`. Non-negative.
   **Unlocks:** Skipping a house never makes the answer worse (no penalty for staying home). We never have to *force* a rob; max already handles ties at zero.

3. **Q:** What is `n`? Can the array be empty?
   **A:** `1 ≤ n ≤ 100`. Always at least one house.
   **Unlocks:** No empty-array branch. A single house is the smallest base case and just returns `nums[0]`.

4. **Q:** Define "without alerting the police" — do we need the list of houses robbed, or only the total?
   **A:** Return the maximum total money only.
   **Unlocks:** We only need to track the running best value, not the chosen set. This is what lets us collapse a length-n DP table down to two scalars.

## 2. Kernel paragraph (§1)

Standing at house `i`, you face exactly two choices because adjacent houses are off-limits: **rob it** and pair its money with the best total you could have collected up to house `i−2` (everything before its neighbour), or **skip it** and carry forward the best total up to house `i−1`. Take the bigger of the two. Because each step only consults the two prior answers — not the whole history — you never build a table; you slide two scalars `prev2, prev1` across the array, and `prev1` at the end is the answer.

Recurrence: `best[i] = max(best[i-1], best[i-2] + nums[i])` with `best[-1] = best[-2] = 0`.

## 3. Foundational concept visual (§1)

A horizontal row of "house" bars with their money values on top. As the reader steps through, a moving `i` cursor highlights the current house. Two small pill cards above (`prev2`, `prev1`) show the rolling memory. A "decision panel" beside the current house shows the two candidates side-by-side:

```
   ROB:  prev2 + nums[i]  =  <number>
   SKIP: prev1            =  <number>
   →     cur = max(...)
```

The chosen candidate's pill is highlighted (success green for ROB, info blue for SKIP). After each step the houses already decided show their `best[i]` value beneath them, dim-coloured. 6 animation steps total for the example `[2,7,9,3,1]` (init + 5 indices); final step displays the answer 12.

## 4. Translations (§3)

1. **Exhaustive subset search → forbid adjacency in the subset.** The brute force iterates 2^n subsets and rejects any with two adjacent indices. O(2^n × n).
2. **Recursive choice at each house → top-down recurrence.** At index `i`, return `max(rob(i+2) + nums[i], rob(i+1))`. Pure recursion, exponential calls but only because we recompute identical subproblems.
3. **Memoize the recurrence → top-down DP.** Cache `rob(i)` in an array of size n. Each subproblem computed once → O(n) time, O(n) memory + O(n) call stack.
4. **Flip direction → bottom-up DP table.** Fill `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` left-to-right. Same O(n) time, O(n) memory, no recursion.
5. **Observe the dependency window is 2 → constant-space rolling pair.** `dp[i]` only reads `dp[i-1]` and `dp[i-2]`. Replace the array with two scalars `prev1, prev2`. O(n) time, **O(1) memory**.

## 5. Algorithm in plain English (§4)

1. **Initialise** `prev2 = 0` and `prev1 = 0`. These stand for "best up to two houses before the first" and "best up to the house before the first" — both empty, both zero.
2. **For each house `i`** from `0` to `n−1`:
3. **Compute the two candidates:** `rob = prev2 + nums[i]` (take this house, plus the best from two back) and `skip = prev1` (leave it, keep the best from one back).
4. **Take the maximum** as the new best up to `i`: `cur = max(rob, skip)`.
5. **Slide the window:** the *old* `prev1` becomes the *new* `prev2`, and `cur` becomes the *new* `prev1`. The order matters — assign `prev2 = prev1` **before** overwriting `prev1`.
6. **Return `prev1`** after the loop — by the slide rule, it holds `best[n−1]`, which is the answer.

## 6. Examples for code viz + dry run (§6, §7)

| # | Input | Expected | Used for | Why |
|---|---|---|---|---|
| 0 | `[1,2,3,1]` | `4` | Fast (cv ex0, dr ex0) | The canonical LC example. 4 indices, one SKIP forced at i=3. |
| 1 | `[2,7,9,3,1]` | `12` | Mid (cv ex1, dr ex1; also §1 animation) | Adjacency tension: huge nums[2]=9 forces SKIP at i=3. 5 indices. |
| 2 | `[2,1,1,2,3,1,5,4,6,2]` | `17` | Slow (cv ex2, dr ex2) | 10 indices → 10 visualisation steps. Mixed ROB/SKIP pattern; demonstrates the rolling pair never references anything past `prev2`. |

## 7. Corner cases (§8)

1. **Single house — `[5]` → `5`.** The loop body runs once. `rob = 0+5 = 5`, `skip = 0`, `cur = 5`. Highlights why both `prev2` and `prev1` start at 0 (so a single house returns its own value).
2. **Two houses — `[3,10]` → `10`.** Adjacency makes them mutually exclusive; algorithm picks the larger. At `i=1`: `rob = 0+10 = 10` (since `prev2` was still 0 after i=0), `skip = 3`. This is the smallest case where the SKIP-vs-ROB tension is visible.
3. **Tie between rob and skip — `[4,4]` → `4`.** At `i=1`, `rob = 0+4 = 4` and `skip = 4`. `max` resolves the tie either way; the answer is still 4. Demonstrates we never need to break ties intentionally.
4. **All zeros — `[0,0,0,0]` → `0`.** Every step gives `rob = skip = cur = 0`. No special case needed because `nums[i] ≥ 0`.
5. **Maximum bait at position 1 — `[1,100,1,1,100]` → `200`.** The greedy "rob every other house starting at 0" picks indices 0,2,4 → 1+1+100 = 102 and misses the optimum. The DP correctly skips house 0 entirely and robs indices 1 and 4: `dp = [1, 100, 100, 101, 200]`. Confirms the rolling pair handles non-greedy interleavings.

## 8. Approaches comparison (§10)

1. **Top-down recursion + memo.** Most natural translation of the recurrence — write `rob(i) = max(rob(i+1), rob(i+2) + nums[i])` and cache. Easy to derive; pays O(n) memory plus O(n) recursion stack and constant function-call overhead. Useful pedagogically but never the final answer.
2. **Bottom-up DP array.** Fill a length-n `dp` array left-to-right. Iterative, no recursion, easy to debug step-by-step (you can print the whole table). O(n) time and O(n) memory. The version you'd write first in an interview before optimising.
3. **Rolling two-variable DP (final).** Same loop body, but only the last two `dp` values are kept as scalars. O(n) time, **O(1) memory**. The expected production answer. The slide step (`prev2 = prev1; prev1 = cur`) replaces the array write.

## 9. Take home (§12)

- **LC 213 — House Robber II.** Houses arranged in a circle; first and last are adjacent. Solve linear House Robber twice (excluding last, then excluding first) and take the max.
- **LC 337 — House Robber III.** Houses on a binary tree; each node returns `(robThis, dontRobThis)`. The same recurrence, on a tree post-order traversal.
- **LC 740 — Delete and Earn.** Reduce to House Robber by bucketing values: index *is* the value, weight *is* total of all occurrences. Same algorithm verbatim once you reframe.
- **LC 198 / 70 / 746 — Climbing Stairs / Min Cost Climbing Stairs.** Same shape of two-back recurrence (`dp[i] = f(dp[i-1], dp[i-2])`). Different operation (sum vs. max), same rolling-pair trick.

## 10. Python verification (BEFORE writing HTML)

```
=== §1 insight: nums = [2, 7, 9, 3, 1] ===
  i=0  nums[i]= 2  prev2= 0  prev1= 0  rob= 2  skip= 0  → cur= 2  [ROB ]
  i=1  nums[i]= 7  prev2= 0  prev1= 2  rob= 7  skip= 2  → cur= 7  [ROB ]
  i=2  nums[i]= 9  prev2= 2  prev1= 7  rob=11  skip= 7  → cur=11  [ROB ]
  i=3  nums[i]= 3  prev2= 7  prev1=11  rob=10  skip=11  → cur=11  [SKIP]
  i=4  nums[i]= 1  prev2=11  prev1=11  rob=12  skip=11  → cur=12  [ROB ]
  ANSWER: 12

=== Ex 0 — fast / classic: nums = [1, 2, 3, 1] ===
  i=0  nums[i]= 1  prev2= 0  prev1= 0  rob= 1  skip= 0  → cur= 1  [ROB ]
  i=1  nums[i]= 2  prev2= 0  prev1= 1  rob= 2  skip= 1  → cur= 2  [ROB ]
  i=2  nums[i]= 3  prev2= 1  prev1= 2  rob= 4  skip= 2  → cur= 4  [ROB ]
  i=3  nums[i]= 1  prev2= 2  prev1= 4  rob= 3  skip= 4  → cur= 4  [SKIP]
  ANSWER: 4

=== Ex 1 — alternating skip: nums = [2, 7, 9, 3, 1] ===
  i=0  → cur= 2  [ROB ]   (prev2=0 prev1=0 rob=2  skip=0)
  i=1  → cur= 7  [ROB ]   (prev2=0 prev1=2 rob=7  skip=2)
  i=2  → cur=11  [ROB ]   (prev2=2 prev1=7 rob=11 skip=7)
  i=3  → cur=11  [SKIP]   (prev2=7 prev1=11 rob=10 skip=11)
  i=4  → cur=12  [ROB ]   (prev2=11 prev1=11 rob=12 skip=11)
  ANSWER: 12

=== Ex 2 — slow / long: nums = [2, 1, 1, 2, 3, 1, 5, 4, 6, 2] ===
  i=0  → cur= 2  [ROB ]
  i=1  → cur= 2  [SKIP]
  i=2  → cur= 3  [ROB ]
  i=3  → cur= 4  [ROB ]
  i=4  → cur= 6  [ROB ]
  i=5  → cur= 6  [SKIP]
  i=6  → cur=11  [ROB ]
  i=7  → cur=11  [SKIP]
  i=8  → cur=17  [ROB ]
  i=9  → cur=17  [SKIP]
  ANSWER: 17

=== corners ===
  [5]            → 5
  [3, 10]        → 10
  [4, 4]         → 4
  [0, 0, 0, 0]   → 0
  [1,2,1,2,1,2]  → 6
```

All traces match expected (verified by `assert` on every example). Source: `tmp/house_robber_trace.py`.
