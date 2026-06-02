# Best Time to Buy and Sell Stock with Cooldown — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `best-time-to-buy-and-sell-stock-with-cooldown`
- **LC #:** 309
- **Difficulty:** Medium
- **Topic:** Dynamic Programming
- **Archetype:** `custom` (state-machine DP — escape hatch per `design/archetypes.md`; none of two_pointer / sliding_window / prefix_scan / divide_conquer fit. The optimisation insight is *each day you sit in one of three states (hold / sold / rest) and transitions between them are fixed*, not a window or partition.)

## 1. Clarifying questions (§0)

1. **Q:** Can I hold multiple stocks at once? **A:** No — at most one share at a time; must sell before buying again. **Unlocks:** state at any day is one of just three labels (holding / just-sold / resting); we don't need a count of held shares.
2. **Q:** What exactly does "cooldown" mean? **A:** The day immediately after a sell, you may not buy. **Unlocks:** a sell on day `d` forbids a buy on day `d+1` — so we need a separate "just sold" state distinct from "free to buy".
3. **Q:** How many transactions are allowed? **A:** As many as you like (subject to the one-share + cooldown rules). **Unlocks:** the DP must let the buy/sell cycle repeat — that's the difference from LC 121 (single transaction) where a single running min was enough.
4. **Q:** What are the input bounds? **A:** `1 ≤ n ≤ 5000`, `0 ≤ prices[i] ≤ 1000`. **Unlocks:** an `O(n)` single pass with three running ints is comfortably fast; we don't need full DP arrays.

## 2. Kernel paragraph (§1)

On any day you are in exactly one of three states: **hold** (currently own a share), **sold** (just sold today — tomorrow is cooldown), or **rest** (no share, free to buy tomorrow). The transitions are fixed: from rest you can stay or buy; from hold you can stay or sell; from sold you can only move into rest. Carry the best profit reachable in each state from one day to the next.

## 3. Foundational concept visual (§1)

A **three-track state machine** rendered as a row of prices on top with the current day highlighted, and three side-by-side cards underneath showing `hold`, `sold`, `rest` updating after each day. Animation walks `day = 0, 1, …, n−1`; at each step it shows the three transition computations, then the new values. The card whose value improved on this day pulses to make the active transition visible.

Canonical example for §1: `prices=[1,2,3,0,2]` → answer `3` (LC's own example). 5 days → 6 steps (init + 5 day-frames). Within the 4–9 range and shows the dip-and-rebuy pattern cooldown enables.

## 4. Translations (§3)

1. **"Day-by-day decision"** → three running variables `hold`, `sold`, `rest` indexed by day. (Each labels the best profit you can have *ending the day* in that state.)
2. **"After selling, tomorrow is forbidden"** → split "not holding" into two states (`sold` for today, `rest` for any later day). The cooldown is encoded by `rest[d] = max(rest[d−1], sold[d−1])`. Yesterday's `sold` is the earliest source of today's `rest`.
3. **"Snapshot before overwrite"** → compute the three new values from yesterday's snapshot before assigning any of them. If you update `hold` first and then use the new `hold` inside the `sold` formula, you've used today's value where yesterday's belonged.

## 5. Algorithm in plain English (§4)

1. Seed `hold = -prices[0]` (paid for day-0 share), `sold = 0`, `rest = 0`.
2. For each `day` from `1` to `n−1`, let `p = prices[day]`.
3. — Compute `new_hold = max(hold, rest − p)` (keep holding, or buy today from rest).
4. — Compute `new_sold = hold + p` (sell today's stock).
5. — Compute `new_rest = max(rest, sold)` (stay resting, or yesterday-sold becomes today-rest).
6. — Assign all three at once: `hold, sold, rest = new_hold, new_sold, new_rest`.
7. Return `max(sold, rest)` — the best ending in a non-holding state.

## 6. Examples for code viz + dry run (§6, §7)

- **Fast example (§6 walkthrough):** `prices=[1,2,4]` → `3`. Trace: init hold=-1 sold=0 rest=0 → day1 hold=-1 sold=1 rest=0 → day2 hold=-1 sold=3 rest=1. ~10 viz steps with substeps per day.
- **Slow example (§6/§7 main):** `prices=[6,1,3,2,4,7]` → `6`. 6 days × ~3 substeps per day → ~18 viz steps. Shows the buy-after-dip pattern and cooldown forcing one day of inaction.
- **Dry run examples (§7, ≥3 buttons):**
  1. `prices=[1,2,3,0,2]` → `3`  *(LC's canonical — dip on day 3 triggers a second trade)*
  2. `prices=[3,2,1]` → `0`  *(monotone decrease — no profit; rest dominates throughout)*
  3. `prices=[2,1,4,5,2,9,7]` → `10`  *(two separate trades separated by cooldown)*

## 7. Corner cases (§8)

- **Single day** (`prices=[5]`) → return `0`. Loop body never runs; default `max(sold, rest) = max(0, 0) = 0`. Guard `n < 2` to skip the loop cleanly.
- **Monotonically decreasing** (`prices=[3,2,1]`) → `0`. `hold` stays negative; `sold` never beats `0`; `rest` stays at `0`. Don't initialise `sold` to `-∞` thinking you must "track a sale" — `0` is the correct baseline (the no-trade outcome).
- **All same price** (`prices=[4,4,4,4]`) → `0`. Any sell exactly cancels the buy. Algorithm naturally returns `0` because `sold = hold + p = -p + p = 0`.
- **Cooldown-forced skip** — on `prices=[1,2,3]` the right answer is "buy day 0, sell day 2" for `+2`. A naive "sum every up-step" greedy would propose `+1` (day 0→1) plus `+1` (day 1→2) for `+2` — but that requires buying day 1, which is cooldown after selling day 1. The state machine forbids it automatically.
- **Forgetting to snapshot** — using the just-updated `hold` inside the `sold` formula on day `d` mixes day `d`'s value with day `d−1`'s. Always compute `new_hold`, `new_sold`, `new_rest` first, then assign together.

## 8. Approaches comparison (§10)

| Approach | Time | Space | Trade-off |
|---|---|---|---|
| Brute force — recursion over all (buy, sell, cooldown) sequences | O(2ⁿ) | O(n) stack | Branches at every day into "buy / sell / hold". Exponential — useless past n≈20 but illustrates the search space the "feel the cost" counter visualises. |
| 2-D DP table `dp[day][state]` | O(n) | O(n) | Same recurrence, tabulated. Easy to debug because you can print the table; needless memory at this n. |
| Three rolling ints (chosen) | O(n) | O(1) | Same recurrence; only the previous day matters, so we collapse the DP to `hold`, `sold`, `rest`. Chosen approach. |
| Peak-valley greedy with cooldown | O(n) | O(1) | Scan valleys and peaks; pretend a sell costs one extra day. Correct on simple inputs but fragile when two short trades beat one long one — easy to get wrong. Mention only as a trap. |

## 9. Take home (§12)

- **Best Time to Buy and Sell Stock** (LC 121) — single transaction, no cooldown. Same "running variable" template, just one (`min_so_far`).
- **Best Time to Buy and Sell Stock II** (LC 122) — unlimited transactions, no cooldown. Add every up-step; collapses to a one-line greedy.
- **Best Time to Buy and Sell Stock with Transaction Fee** (LC 714) — same state machine but only two states (hold / cash); each sell deducts a fee.
- **House Robber** (LC 198) — same "DP with a forbidden adjacency" shape; rob/skip becomes hold/rest, and skipping the next house is the cooldown.

## 10. Python verification (BEFORE writing HTML)

```
===== prices=[1, 2, 3, 0, 2] (expect 3) =====
Init day0 p=1: hold=-1 sold=0 rest=0
day1 p=2: hold=-1 sold=1 rest=0
day2 p=3: hold=-1 sold=2 rest=1
day3 p=0: hold=1 sold=-1 rest=2
day4 p=2: hold=1 sold=3 rest=2
Result: 3

===== prices=[1] (expect 0) =====
Result: 0

===== prices=[1, 2, 4] (expect 3) =====
Init day0 p=1: hold=-1 sold=0 rest=0
day1 p=2: hold=-1 sold=1 rest=0
day2 p=4: hold=-1 sold=3 rest=1
Result: 3

===== prices=[6, 1, 3, 2, 4, 7] (expect 6) =====
Init day0 p=6: hold=-6 sold=0 rest=0
day1 p=1: hold=-1 sold=-5 rest=0
day2 p=3: hold=-1 sold=2 rest=0
day3 p=2: hold=-1 sold=1 rest=2
day4 p=4: hold=-1 sold=3 rest=2
day5 p=7: hold=-1 sold=6 rest=3
Result: 6

===== prices=[3, 2, 1] (expect 0) =====
Init day0 p=3: hold=-3 sold=0 rest=0
day1 p=2: hold=-2 sold=-1 rest=0
day2 p=1: hold=-1 sold=-1 rest=0
Result: 0

===== prices=[2, 1, 4, 5, 2, 9, 7] (expect 10) =====
Init day0 p=2: hold=-2 sold=0 rest=0
day1 p=1: hold=-1 sold=-1 rest=0
day2 p=4: hold=-1 sold=3 rest=0
day3 p=5: hold=-1 sold=4 rest=3
day4 p=2: hold=1 sold=1 rest=4
day5 p=9: hold=1 sold=10 rest=4
day6 p=7: hold=1 sold=8 rest=10
Result: 10
```

All six examples pass assertion against expected values. The trace is the source of truth for `cvGen` / `drGen` step generators.
