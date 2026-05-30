# House Robber II — lesson plan

> Workflow per PLAN-011 §4.8: fill this file first, verify with Python, get approval, then author HTML.

## Metadata
- **Slug:** `house-robber-ii`
- **LC #:** 213
- **Difficulty:** Medium
- **Topic:** Dynamic Programming
- **Archetype:** `custom` — circular variant of linear DP. Same per-index recurrence as House Robber I (LC 198), but the array is on a ring so the first and last houses are adjacent. Closest in *teaching structure* to `prefix_scan` (still a one-pass linear DP), but the surrounding logic is a case-split over endpoints, not a scan over neighbours.
- **Prerequisite:** [House Robber I](../house-robber/lesson.html). This lesson does **not** re-derive the rolling-pair DP — it shows how to reuse it once you spot the circle-breaking trick.

## 1. Clarifying questions (§0)

1. **Q:** Are the houses really arranged in a circle? What does "circle" mean for adjacency?
   **A:** Yes — the array is cyclic. House `0` and house `n-1` are neighbours, on top of all the usual `i ↔ i+1` neighbours. Every other rule from LC 198 still applies.
   **Unlocks:** The only difference from linear House Robber is one extra forbidden pair: `{0, n-1}`. That's the entire "twist."

2. **Q:** Can `n == 1`? Can `nums[i]` be 0?
   **A:** `1 ≤ n ≤ 100` and `0 ≤ nums[i] ≤ 1000`. A single house is allowed; values are non-negative.
   **Unlocks:** Special-case `n == 1` (no circle to worry about — just return `nums[0]`). Non-negative values mean skipping is never strictly forced to be better, but the recurrence handles ties cleanly.

3. **Q:** Can I just run linear House Robber on the array as-is and patch the answer somehow?
   **A:** No clean patch exists. Linear HR may pick *both* `nums[0]` and `nums[n-1]` (they aren't adjacent in the linear view) — that's invalid here. You need the algorithm to *know* about the new constraint up front.
   **Unlocks:** This question forces the key insight — we must structurally exclude at least one of the two circle-joining endpoints.

4. **Q:** Do I need to return *which* houses are robbed, or just the total?
   **A:** Total money only.
   **Unlocks:** We can keep the rolling-pair O(1)-memory shape from LC 198 — no need to reconstruct subsets.

## 2. Kernel paragraph (§1)

In a circle of houses, the only thing that's new compared to a line is one extra adjacency: house `0` and house `n-1` are now neighbours. That means an optimal plan **cannot rob both endpoints** — at least one of them must be skipped. So split the problem into two linear sub-problems: one that forbids the last house (run linear House Robber on `nums[0 .. n-2]`), and one that forbids the first house (run linear House Robber on `nums[1 .. n-1]`). Take the larger of the two answers. Each sub-problem is just LC 198 — same rolling-pair recurrence, same O(n) time, same O(1) memory — applied twice.

Special case: `n == 1` has no circle to worry about and returns `nums[0]` directly.

## 3. Foundational concept visual (§1)

A row of houses laid out left-to-right, with a curved arc/label drawn from house `0` to house `n-1` showing the **extra circle-adjacency**. As the reader steps through:

- **SETUP:** all houses visible, arc lit up. Caption: "House 0 and house n-1 are now neighbours."
- **CASE A:** the last house dims out (greyed); the visible slice `nums[0..n-2]` is treated as a linear array; show the linear-HR answer (`caseA`) for it.
- **CASE B:** the first house dims out (greyed); the slice `nums[1..n-1]` is now the linear array; show its answer (`caseB`).
- **COMBINE:** both endpoints visible again; show `answer = max(caseA, caseB)` on a single result tile.

Phase indicator (`SETUP / CASE A / CASE B / COMBINE`) anchors the reader. Target: 5–6 animation steps for the canonical example `[1,2,3,1]` (n=4, answer 4).

## 4. Translations (§3)

1. **Translation 1 — Linear House Robber doesn't apply directly.** If we naively run LC 198 on the array, it might pick both `nums[0]` and `nums[n-1]` (they look 4 apart, not adjacent). That violates the circle constraint, so we get a wrong answer in general.
2. **Translation 2 — The extra constraint is one forbidden pair.** Compared to the linear problem, exactly one new rule is added: `{0, n-1}` can't both be robbed. So the optimum **excludes at least one** of those two indices.
3. **Translation 3 — Case-split on the excluded endpoint.** Either house `0` is skipped, or house `n-1` is skipped (or both — but "both" is dominated by either single case since values are non-negative). Enumerate the two cases:
   - **Case A:** skip house `n-1`. The remaining houses form a normal *line*: `nums[0..n-2]`.
   - **Case B:** skip house `0`. The remaining houses form a normal *line*: `nums[1..n-1]`.
4. **Translation 4 — Each case is just LC 198.** Inside each case the array is linear, so adjacency is back to "`i` ↔ `i+1`". Run the rolling-pair DP from House Robber I on the slice, get its best total.
5. **Translation 5 — Combine: take the bigger of the two cases.** The overall answer is `max(caseA, caseB)`. Plus the `n == 1` short-circuit so we don't try to call `linearRob` on an empty slice.

## 5. Algorithm in plain English (§4)

1. **If `n == 1`**, return `nums[0]`. (Single house, no circle to worry about.)
2. **Compute Case A** by running linear House Robber on `nums[0 .. n-2]`: skip the last house entirely, then apply the rolling-pair DP. Call the result `caseA`.
3. **Compute Case B** by running linear House Robber on `nums[1 .. n-1]`: skip the first house entirely, same DP. Call the result `caseB`.
4. **Return `max(caseA, caseB)`** — whichever endpoint we chose to drop, that's the better of the two plans.

## 6. Examples for code viz + dry run (§6, §7)

| # | Input | Expected | caseA | caseB | Used for | Why |
|---|---|---|---|---|---|---|
| 0 | `[2,3,2]` | `3` | `3` | `3` | fast (cv ex0, dr ex0; also §1 anim) | LC example 1 — small triangle where every pair is adjacent in the circle; both cases tie. Best minimal case for §1 animation. |
| 1 | `[1,2,3,1]` | `4` | `4` | `3` | mid (cv ex1, dr ex1) | LC example 2 — first time the two cases differ. Highlights that Case A and Case B can disagree, and the answer is the larger. |
| 2 | `[2,1,1,2,3,1,5,4,6,2]` | `17` | `17` | `15` | slow (cv ex2, dr ex2) | 10 houses → 60+ CV steps (every line of the two linear passes lights up). Demonstrates the rolling pair really doesn't care about the slice's actual length. |

## 7. Corner cases (§8)

1. **Single house — `[5]` → `5`.** The `n == 1` short-circuit returns `nums[0]`. Don't run either linear pass — Case A on an empty slice and Case B on an empty slice would both return 0, giving the wrong answer.
2. **Two houses — `[3, 10]` → `10`.** They're adjacent both linearly and on the circle, so we can rob exactly one. Case A on `[3]` returns 3; Case B on `[10]` returns 10; max is 10. The rolling pair still works on a single-element slice because the seeds are 0.
3. **Three houses, every pair adjacent in the circle — `[2, 3, 2]` → `3`.** This is LC example 1. In a triangle, every pair of houses is adjacent (linearly *and* via the circle), so you can only rob one — pick the biggest. Both Case A (`[2,3]` → 3) and Case B (`[3,2]` → 3) tie at 3.
4. **All same values — `[4, 4, 4, 4]` → `8`.** In a 4-cycle, the optimal robs two opposite houses (indices 0&2 or 1&3). Both Case A and Case B compute 8. Confirms the algorithm finds the alternating pattern even when greedy "pick the biggest" has no preference.
5. **Bait at both endpoints — `[100, 1, 1, 100]` → `101`.** Greedy "rob both 100s" is illegal because index 0 and index 3 are now adjacent. Both cases produce 101 (rob one 100 plus one of the 1s). This is the canonical example that *fails* if you mistakenly run linear HR on the original array (which would happily rob both 100s for 200).

## 8. Approaches comparison (§10)

1. **Two linear passes with a helper (production answer).** Define `linearRob(nums, lo, hi)` that runs the rolling-pair DP on the inclusive sub-range. Call it twice — once with `(0, n-2)` and once with `(1, n-1)` — and return the max. O(n) time, O(1) memory (we use four scalars total: `prev2`/`prev1` for each pass, reused or duplicated). Clean, idiomatic, and obviously correct.
2. **Two inlined linear passes.** Same algorithm, but without a helper function — just two for-loops back-to-back over the appropriate index ranges. Slightly longer code but no function-call overhead; sometimes preferred when the interviewer asks to "show all the logic in one function."
3. **Single pass with extra state (advanced, rarely needed).** It's possible to compute Case A and Case B simultaneously with parallel rolling pairs and per-index decisions about whether each "is allowed to include endpoint 0". This compresses two scans into one but is harder to read and offers no asymptotic gain. Mention it as a curiosity.

## 9. Take home (§12)

- **LC 198 — House Robber I** — the linear version. This problem reduces to two calls of LC 198, so the prerequisite is essential.
- **LC 337 — House Robber III** — same recurrence on a binary tree. Each node returns `(rob, dontRob)` and the parent picks `max(rob + leftDontRob + rightDontRob, dontRob_combined)`.
- **LC 740 — Delete and Earn** — bucket the values then run LC 198. Adjacency is on the *value axis*, not the index axis.
- **LC 152 — Maximum Product Subarray** — different problem but same case-split shape: track two parallel rolling answers (best-so-far that ends here positive, vs. that ends here negative).

## 10. Python verification (BEFORE writing HTML)

```
=== Ex 0 — classic triangle: nums = [2, 3, 2] ===
  Case A (exclude last):  linearRob(nums[0..1]) = 3
  Case B (exclude first): linearRob(nums[1..2]) = 3
  ANSWER = max(3, 3) = 3

=== Ex 1 — LC example 2: nums = [1, 2, 3, 1] ===
  Case A (exclude last):  linearRob(nums[0..2]) = 4
  Case B (exclude first): linearRob(nums[1..3]) = 3
  ANSWER = max(4, 3) = 4

=== Ex 2 — slow / long (n=10): nums = [2, 1, 1, 2, 3, 1, 5, 4, 6, 2] ===
  Case A (exclude last):  linearRob(nums[0..8]) = 17
  Case B (exclude first): linearRob(nums[1..9]) = 15
  ANSWER = max(17, 15) = 17

=== corner: single house: nums = [5] ===
  single house → 5

=== corner: two houses: nums = [3, 10] ===
  Case A (exclude last):  linearRob(nums[0..0]) = 3
  Case B (exclude first): linearRob(nums[1..1]) = 10
  ANSWER = max(3, 10) = 10

=== corner: all same: nums = [4, 4, 4, 4] ===
  Case A (exclude last):  linearRob(nums[0..2]) = 8
  Case B (exclude first): linearRob(nums[1..3]) = 8
  ANSWER = max(8, 8) = 8

=== corner: bait at endpoints: nums = [100, 1, 1, 100] ===
  Case A (exclude last):  linearRob(nums[0..2]) = 101
  Case B (exclude first): linearRob(nums[1..3]) = 101
  ANSWER = max(101, 101) = 101

=== corner: triplet: nums = [1, 2, 3] ===
  Case A (exclude last):  linearRob(nums[0..1]) = 2
  Case B (exclude first): linearRob(nums[1..2]) = 3
  ANSWER = max(2, 3) = 3
```

All examples and corners verified via assertion in `/tmp/hr2_trace.py`. Each Case-A / Case-B subproblem is just LC 198's rolling pair on a sub-range, so the trace also implicitly verifies the House Robber I logic.
