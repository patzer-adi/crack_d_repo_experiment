# Maximum Product Subarray — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `maximum-product-subarray`
- **LC #:** 152
- **Difficulty:** Medium
- **Topic:** Dynamic Programming
- **Archetype:** `custom` (Kadane-style running DP — escape hatch per `design/archetypes.md`; none of two_pointer / sliding_window / prefix_scan / divide_conquer fit. The optimisation insight is *track both running max AND running min because a negative number flips them*, not a window or partition.)

## 1. Clarifying questions (§0)

1. **Q:** Must the subarray be contiguous? **A:** Yes — a *subarray*, not a subsequence. **Unlocks:** elements between picks cannot be skipped, so at each index `i` we only choose between "extend the previous run" and "start fresh at `i`". That's what makes a single linear scan possible.
2. **Q:** Can numbers be negative or zero? **A:** Yes — `-10 ≤ nums[i] ≤ 10`. **Unlocks:** the whole point of the problem. A negative can flip a tiny min into a huge max next step, and a zero resets the running product. Tracking only the running *max* would miss the flip.
3. **Q:** Is the array guaranteed non-empty? **A:** Yes — `1 ≤ n ≤ 2·10⁴`. **Unlocks:** we can safely seed both running variables and the answer with `nums[0]` — no empty-array edge case to defend.
4. **Q:** Does the answer fit in a 32-bit int? **A:** Yes, the problem guarantees every prefix product fits. **Unlocks:** we don't need long long or BigInt — plain `int` is enough in C++.

## 2. Kernel paragraph (§1)

A negative number isn't a dead end — it's a flipper. If the smallest (most negative) product so far is `−12` and the next element is `−4`, multiplying gives `48`, the new biggest. So at every index we must remember *both* the best and the worst running product ending right there. Each new element is either a fresh start, an extension of the best, or an extension of the worst — pick the max and min of those three and move on.

## 3. Foundational concept visual (§1)

A **two-track running state** rendered as the array on top with the current index highlighted, and two side-by-side cards underneath showing `cur_max` and `cur_min` updating after each step. Animation walks `i = 0, 1, …, n−1`; at each step it shows the three candidates `x`, `x·cur_max`, `x·cur_min`, then picks the new max/min. A third card holds `best` and pulses green when it updates.

Canonical example for §1: `nums=[-2,3,-4]` → answer `24`. Three iterations (init + 2 fills) emit 7 visualisation steps (init, then 3 substeps per iteration: cands → pick → check-best). Within the 4–9 range and the negative-flip moment lands cleanly.

## 4. Translations (§3)

1. **"Best subarray product ending at `i`"** → `cur_max = max(nums[i], nums[i]·prev_max, nums[i]·prev_min)`. (Three candidates: restart, extend-the-good, extend-the-bad.)
2. **"Worst subarray product ending at `i`"** → `cur_min = min(nums[i], nums[i]·prev_max, nums[i]·prev_min)`. (Same three candidates — keep both because the worst might become the best after one more negative.)
3. **"Global answer"** → `best = max(best, cur_max)` checked once per index. (We never need to compare against `cur_min` because a *running min* is, by definition, not the answer.)

## 5. Algorithm in plain English (§4)

1. Seed `cur_max = cur_min = best = nums[0]`.
2. For each `i` from 1 to `n-1`:
3. — Compute three candidates: `x = nums[i]`, `x · cur_max`, `x · cur_min`.
4. — Set `cur_max` to the largest of the three, `cur_min` to the smallest. (Must capture both before either overwrites the other — order matters when `nums[i] < 0`.)
5. — If `cur_max > best`, update `best`.
6. Return `best`.

## 6. Examples for code viz + dry run (§6, §7)

- **Fast example (§6 walkthrough):** `nums=[-2,3,-4]` → `24`. Trace: init → i=1 cands=(3,−6,−6) → cur_max=3, cur_min=−6 → i=2 cands=(−4,−12,24) → cur_max=24 (flip!), best=24. ~10 visualisation steps.
- **Slow example (§6/§7 main):** `nums=[2,-5,-2,-4,3]` → `24`. 5 elements → 5 iterations; each iteration shows candidate computation + max/min update + best check ≈ 3 substeps → ~15 viz steps. Shows cur_min growing in absolute value then flipping on the final element.
- **Dry run examples (§7, ≥3 buttons):**
  1. `nums=[2,3,-2,4]` → `6`  *(classic — negative breaks the run)*
  2. `nums=[-2,3,-4]` → `24`  *(negative flip restores the max)*
  3. `nums=[-2,0,-1]` → `0`  *(zero resets both running variables)*

## 7. Corner cases (§8)

- **Single element** (`nums=[-3]`) → return `-3`. Init already seeds best; loop never runs.
- **All negatives, even count** (`nums=[-2,-3,-4]`) → answer 12 (`-3·-4`). Demonstrates that ignoring negatives loses the answer.
- **Zero in the middle** (`nums=[-2,0,-1]`) → answer 0. Zero collapses both running products; the rebuild starts fresh.
- **Forgetting to snapshot** (using new `cur_max` while computing `cur_min`) → wrong answers on `nums=[-2,3,-4]`. Capture both candidates before overwriting either.
- **Only tracking running max** → fails the moment two negatives meet (`nums=[-2,-3]` would return -2 instead of 6).

## 8. Approaches comparison (§10)

| Approach | Time | Space | Trade-off |
|---|---|---|---|
| Brute force — every subarray | O(n²) | O(1) | Two nested loops compute the product of every `nums[i..j]`. Correct but quadratic. The "checks" counter makes the cost feel real on `n=2·10⁴`. |
| Single-pass DP with `cur_max` only | O(n) | O(1) | **Wrong.** Misses negative-flip cases. Useful as a trap to discuss. |
| Single-pass DP with `cur_max` + `cur_min` | O(n) | O(1) | Chosen approach. One linear pass, two running variables, constant space. |
| Two-pass forward/backward product | O(n) | O(1) | Multiply left-to-right, reset on zero; repeat right-to-left; answer is the max seen. Same asymptotic, two scans. Mention as a clever alternative. |

## 9. Take home (§12)

- **Maximum Subarray** (LC 53) — Kadane's original. Same running-state shape, but only `cur_sum` (no min) because addition doesn't flip signs.
- **Best Time to Buy and Sell Stock** (LC 121) — single running variable `min_so_far`; same "running state" template but no flip.
- **House Robber** (LC 198) — running DP with two states (rob, skip); same pattern of "carry two running values forward".
- **Maximum Product of Three Numbers** (LC 628) — not contiguous, but the same min-tracking trick: the answer might be `largest · second · third` or `most_negative · second_negative · largest`.

## 10. Python verification (BEFORE writing HTML)

```
===== nums=[2, 3, -2, 4] (expect 6) =====
Init: cur_max=2 cur_min=2 best=2
i=1 x=3: cands=(3,6,6) -> cur_max=6 cur_min=3 best=6
i=2 x=-2: cands=(-2,-12,-6) -> cur_max=-2 cur_min=-12 best=6
i=3 x=4: cands=(4,-8,-48) -> cur_max=4 cur_min=-48 best=6
Result: 6

===== nums=[-2, 0, -1] (expect 0) =====
Init: cur_max=-2 cur_min=-2 best=-2
i=1 x=0: cands=(0,0,0) -> cur_max=0 cur_min=0 best=0
i=2 x=-1: cands=(-1,0,0) -> cur_max=0 cur_min=-1 best=0
Result: 0

===== nums=[-2, 3, -4] (expect 24) =====
Init: cur_max=-2 cur_min=-2 best=-2
i=1 x=3: cands=(3,-6,-6) -> cur_max=3 cur_min=-6 best=3
i=2 x=-4: cands=(-4,-12,24) -> cur_max=24 cur_min=-12 best=24
Result: 24

===== nums=[2, -5, -2, -4, 3] (expect 24) =====
Init: cur_max=2 cur_min=2 best=2
i=1 x=-5: cands=(-5,-10,-10) -> cur_max=-5 cur_min=-10 best=2
i=2 x=-2: cands=(-2,10,20) -> cur_max=20 cur_min=-2 best=20
i=3 x=-4: cands=(-4,-80,8) -> cur_max=8 cur_min=-80 best=20
i=4 x=3: cands=(3,24,-240) -> cur_max=24 cur_min=-240 best=24
Result: 24

===== nums=[0] (expect 0) =====
Init: cur_max=0 cur_min=0 best=0
Result: 0

===== nums=[-3] (expect -3) =====
Init: cur_max=-3 cur_min=-3 best=-3
Result: -3

===== nums=[-2, -3, -4] (expect 12) =====
Init: cur_max=-2 cur_min=-2 best=-2
i=1 x=-3: cands=(-3,6,6) -> cur_max=6 cur_min=-3 best=6
i=2 x=-4: cands=(-4,-24,12) -> cur_max=12 cur_min=-24 best=12
Result: 12
```

All seven examples pass assertion against expected values. The trace is the source of truth for `cvGen` / `drGen` step generators.
