# Coin Change — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `coin-change`
- **LC #:** 322
- **Difficulty:** Medium
- **Topic:** Dynamic Programming
- **Archetype:** `custom` (DP table — escape hatch per `design/archetypes.md`; none of two_pointer / sliding_window / prefix_scan / divide_conquer fit. The optimisation insight is *bottom-up subproblem table*, not a window or partition.)

## 1. Clarifying questions (§0)

1. **Q:** Can the same coin be used many times? **A:** Yes — unbounded. **Unlocks:** every `dp[i]` may look back at the *same* coin from `dp[i-c]`, so we don't track "used" — this is unbounded knapsack, not 0/1.
2. **Q:** What if the amount can't be made? **A:** Return `-1`. **Unlocks:** we need a sentinel ("not yet reachable") distinct from a real coin count — use `amount+1` or `inf`; convert at the end.
3. **Q:** Coin values — always positive integers? **A:** Yes, `1 ≤ coin ≤ 2³¹-1`. **Unlocks:** no zero coin to worry about (would loop forever) and no negatives (would invalidate the monotone subproblem ordering).
4. **Q:** What's the amount range? **A:** `0 ≤ amount ≤ 10⁴`. **Unlocks:** an `O(amount × coins)` table is ~10⁶ ops — comfortably linear. Also `amount=0` is legal: answer is `0`.

## 2. Kernel paragraph (§1)

To make amount `N` with the fewest coins, the *last* coin used must be some value `c` from the set — and then the remaining amount `N-c` is the same problem with a smaller target. So if we already know the best for every amount below `N`, the best for `N` is `1 + min(dp[N-c])` over coins `c ≤ N`. Build the table bottom-up from `dp[0]=0`. Amounts no coin can reach stay at the sentinel and surface as `-1`.

## 3. Foundational concept visual (§1)

A **1-D dp array** rendered as cells `dp[0..amount]`, indices shown above each cell. Animation walks i = 0, 1, 2, …, amount; at each step it highlights the current cell, draws arrows back to `dp[i-c]` for each coin `c`, and shows the candidate `dp[i-c]+1` values. The cell turns green with the chosen min. Cells still at the sentinel show "∞".

Canonical example for §1: `coins=[1,2,5], amount=6` → answer `2`. Six fill-steps after init give 7 total steps — within the 4–9 range.

## 4. Translations (§3)

1. **"Fewest coins for amount N"** → "1 + fewest coins for N − c, taken over all coins c". (The last-coin decomposition.)
2. **"For every amount below N"** → a 1-D table `dp[0..N]`, filled left-to-right. (Subproblem ordering.)
3. **"Impossible / not yet reached"** → sentinel value `amount+1` (or `inf`). Anything that stays sentinel at the end becomes `-1`.

## 5. Algorithm in plain English (§4)

1. Create `dp` of length `amount+1`, fill with sentinel `amount+1`; set `dp[0] = 0`.
2. For each target `i` from 1 to `amount`:
3. — For each coin `c`: if `c ≤ i`, candidate is `dp[i-c] + 1`; keep the smallest candidate as `dp[i]`.
4. After the table is filled, if `dp[amount] > amount`, return `-1`; else return `dp[amount]`.

## 6. Examples for code viz + dry run (§6, §7)

- **Fast example (§6 walkthrough):** `coins=[2], amount=3` → `-1`. Trace: dp=[0,∞,∞,∞] → i=1 no coin fits → i=2 coin=2 gives dp[0]+1=1 → i=3 no coin fits (3−2=1 still ∞). Returns -1. 4 fill-steps.
- **Slow example (§6/§7 main):** `coins=[1,2,5], amount=11` → `3`. 11 fill-steps after init → 12+ visualisation steps. Demonstrates min across 3 coins at most cells.
- **Dry run examples (§7, ≥3 buttons):**
  1. `coins=[1,2,5], amount=11` → `3`  *(slow main)*
  2. `coins=[2], amount=3` → `-1`  *(unreachable)*
  3. `coins=[1], amount=0` → `0`  *(zero amount)*
  4. `coins=[5,2,1], amount=7` → `2`  *(coins given out-of-order; answer 5+2)*

## 7. Corner cases (§8)

- **`amount = 0`** → return `0`. dp has one cell already set; loop never runs.
- **`amount` cannot be formed** (e.g. `coins=[2], amount=3`) → `dp[amount]` stays at sentinel; return `-1`.
- **Single coin that divides amount** (e.g. `coins=[3], amount=9`) → answer `3`; every third cell is reachable, the rest stay sentinel.
- **Coin larger than amount** is skipped by the `c ≤ i` guard — does not crash, just contributes nothing.
- **Duplicate coins** (problem guarantees distinct, but harmless if duplicated) — same answer, just wasted work.

## 8. Approaches comparison (§10)

| Approach | Time | Space | Trade-off |
|---|---|---|---|
| Greedy (always take largest coin ≤ remaining) | O(amount/min_coin) | O(1) | **Wrong** in general — e.g. `coins=[1,3,4], amount=6`: greedy picks 4+1+1=3, optimum is 3+3=2. Mention only as a trap. |
| Recursive brute force with memoisation (top-down) | O(amount · |coins|) | O(amount) stack + table | Mirrors the kernel directly. Same complexity as bottom-up but pays recursion overhead and risks stack depth at amount=10⁴. |
| Bottom-up DP table | O(amount · |coins|) | O(amount) | Chosen approach. Iterative, no recursion, sentinel handles unreachable cleanly. |
| BFS over amounts | O(amount · |coins|) | O(amount) queue | Treat amounts as nodes, each coin as an edge of weight 1; shortest path from 0 to amount. Same complexity, slightly more memory pressure, sometimes faster to terminate on the first hit. |

## 9. Take home (§12)

- **Coin Change II** (LC 518) — *count* the number of ways, not the fewest. Same kernel, but coins iterate outside and amounts inside to avoid double-counting permutations.
- **Perfect Squares** (LC 279) — same template; the "coin set" is `{1, 4, 9, 16, …}`.
- **Word Break** (LC 139) — dp[i] becomes a boolean ("is prefix i breakable?") with words instead of coins; same last-piece decomposition.
- **Climbing Stairs** (LC 70) — degenerate case with coins `{1, 2}` and *count* of ways. Same recursion shape, simpler.

## 10. Python verification (BEFORE writing HTML)

```
===== FAST: coins=[2], amount=3 (expect -1) =====
Initial dp: ['0', 'inf', 'inf', 'inf']
i=1: no coin fits / no path -> dp[1]=inf
         dp = ['0', 'inf', 'inf', 'inf']
i=2: coin=2 -> dp[0]+1 = 0+1 = 1 -> dp[2]=1
         dp = ['0', 'inf', 1, 'inf']
i=3: no coin fits / no path -> dp[3]=inf
         dp = ['0', 'inf', 1, 'inf']
Result: -1

===== SLOW: coins=[1,2,5], amount=11 (expect 3) =====
Initial dp: ['0', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf']
i=1: coin=1 -> dp[0]+1 = 0+1 = 1 -> dp[1]=1
i=2: coin=1 -> dp[1]+1 = 2; coin=2 -> dp[0]+1 = 1 -> dp[2]=1
i=3: coin=1 -> dp[2]+1 = 2; coin=2 -> dp[1]+1 = 2 -> dp[3]=2
i=4: coin=1 -> dp[3]+1 = 3; coin=2 -> dp[2]+1 = 2 -> dp[4]=2
i=5: coin=1 -> dp[4]+1 = 3; coin=2 -> dp[3]+1 = 3; coin=5 -> dp[0]+1 = 1 -> dp[5]=1
i=6: coin=1 -> dp[5]+1 = 2; coin=2 -> dp[4]+1 = 3; coin=5 -> dp[1]+1 = 2 -> dp[6]=2
i=7: coin=1 -> dp[6]+1 = 3; coin=2 -> dp[5]+1 = 2; coin=5 -> dp[2]+1 = 2 -> dp[7]=2
i=8: coin=1 -> dp[7]+1 = 3; coin=2 -> dp[6]+1 = 3; coin=5 -> dp[3]+1 = 3 -> dp[8]=3
i=9: coin=1 -> dp[8]+1 = 4; coin=2 -> dp[7]+1 = 3; coin=5 -> dp[4]+1 = 3 -> dp[9]=3
i=10: coin=1 -> dp[9]+1 = 4; coin=2 -> dp[8]+1 = 4; coin=5 -> dp[5]+1 = 2 -> dp[10]=2
i=11: coin=1 -> dp[10]+1 = 3; coin=2 -> dp[9]+1 = 4; coin=5 -> dp[6]+1 = 3 -> dp[11]=3
Result: 3

===== CORNER: coins=[1], amount=0 (expect 0) =====
Initial dp: ['0']
Result: 0

===== CORNER: coins=[5,2,1], amount=7 (expect 2) =====
Initial dp: ['0', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf']
i=1: coin=1 -> dp[0]+1 = 1 -> dp[1]=1
i=2: coin=2 -> dp[0]+1 = 1; coin=1 -> dp[1]+1 = 2 -> dp[2]=1
i=3: coin=2 -> dp[1]+1 = 2; coin=1 -> dp[2]+1 = 2 -> dp[3]=2
i=4: coin=2 -> dp[2]+1 = 2; coin=1 -> dp[3]+1 = 3 -> dp[4]=2
i=5: coin=5 -> dp[0]+1 = 1; coin=2 -> dp[3]+1 = 3; coin=1 -> dp[4]+1 = 3 -> dp[5]=1
i=6: coin=5 -> dp[1]+1 = 2; coin=2 -> dp[4]+1 = 3; coin=1 -> dp[5]+1 = 2 -> dp[6]=2
i=7: coin=5 -> dp[2]+1 = 2; coin=2 -> dp[5]+1 = 2; coin=1 -> dp[6]+1 = 3 -> dp[7]=2
Result: 2
```

All four examples pass assertion against expected values. The trace is the source of truth for `cvGen` / `drGen` step generators.
