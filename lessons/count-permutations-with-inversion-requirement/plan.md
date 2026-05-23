# Count Permutations With Inversion Requirements — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).
>
> **Status (2026-05-21):** Plan added retroactively as part of PLAN-015 phase 3.
> The HTML lesson was authored 2026-05-13 before the plan workflow. This plan
> captures the algorithm and verification so future-Claude can regenerate or
> update the lesson without re-deriving everything.

## Metadata
- **Slug:** `count-permutations-with-inversion-requirement`
- **LC #:** 3376
- **Difficulty:** Hard
- **Topic:** Arrays / Dynamic Programming
- **Archetype:** `custom` (1D DP with sliding-window prefix-sum optimisation; no canonical golden fits)

## 1. Clarifying questions (§0)

1. **Q:** What is an inversion?
   **A:** A pair (i, j) with i < j and perm[i] > perm[j] — a larger value before a smaller one.
   **Unlocks:** Counting inversions becomes a per-element insertion DP: when inserting value k into a sequence, k contributes a number of new inversions equal to how many already-placed elements end up to its right.

2. **Q:** What does a requirement [end, cnt] mean?
   **A:** The prefix `perm[0..end]` must contain exactly `cnt` inversions. Multiple requirements may be supplied.
   **Unlocks:** Requirements act as hard constraints — at each "required" index, only states with the required inversion count survive.

3. **Q:** Can requirements conflict?
   **A:** Yes — e.g. requiring 5 inversions at index 1 is impossible (max is 1). The answer is 0.
   **Unlocks:** Always check feasibility; impossible states get zeroed out and propagate as zero downstream.

4. **Q:** What do we return?
   **A:** Count of valid permutations modulo 10⁹+7.
   **Unlocks:** Apply mod at every addition step to avoid overflow.

## 2. Kernel paragraph (§1)

Build the permutation by inserting elements in increasing order. When inserting element `i` into a length-`i` sequence, the choice of insertion position adds exactly 0 to `i` new inversions (one per element placed to its right). Let `dp[i][j]` = number of permutations of the first i+1 elements with exactly j inversions that satisfy all requirements at indices ≤ i. Transition: `dp[i][j] = sum of dp[i-1][j-k] for k in 0..min(i, j)`. At any required index, zero out states with j ≠ required count. Use a prefix-sum sliding window to evaluate each row in O(max_inv) instead of O(i · max_inv).

## 3. Foundational concept visual (§1)

Two-panel visual: (1) the inversion definition shown on a small permutation like [2, 0, 1] with each pair labelled as inversion / not; (2) the insertion mechanic — inserting element 2 into [0, 1] in three positions, each adding 0, 1, or 2 new inversions.

## 4. Translations (§3)

1. **"Count permutations with constraints"** → DP over permutation length × inversion count.
2. **"Insert one element at a time"** → transition adds 0..i new inversions (the count of already-placed elements after the new insertion point).
3. **"Requirements at fixed indices"** → at index `end_r`, retain only `dp[end_r][cnt_r]` (zero everything else for that row).
4. **"O(i · max_inv) transition per row → O(max_inv)"** → prefix-sum sliding window. Maintain a running sum of the previous row over a window of size i+1.

## 5. Algorithm in plain English (§4)

1. Sort the requirements by end index so we can apply them in order.
2. Initialise `dp[0][0] = 1` (one permutation of just element 0, with 0 inversions).
3. For each i from 1 to n−1:
   a. Compute `dp[i]` from `dp[i-1]` using the prefix-sum sliding window — each `dp[i][j]` is the sum of `dp[i-1][j-i .. j]`.
   b. If there's a requirement at this i, zero out `dp[i][j]` for every j ≠ requirement count.
4. After the last row, sum `dp[n-1][*]` — but a requirement at n−1, if present, restricts to a single column.
5. Return the count mod 10⁹+7.

## 6. Examples for code viz + dry run (§6, §7)

### Fast example: `n = 3, requirements = []` → `6`

All 6 permutations of [0,1,2] are valid (no requirements). dp progression:
- `dp[0]` = [1]
- `dp[1]` = [1, 1] (one with 0 inv, one with 1 inv)
- `dp[2]` = [1, 2, 2, 1] (sum = 6)

### Slow example: `n = 3, requirements = [[2, 2]]` → `2`

Same dp progression up to row 1. At row 2 with the requirement (end=2, cnt=2), zero out all except j=2: `dp[2]` = [0, 0, 2, 0]. Answer = 2 (the two permutations [1,2,0] and [2,0,1] each have exactly 2 inversions).

## 7. Corner cases (§8)

1. **Impossible requirement** — e.g. `[1, 5]` (5 inversions in prefix of length 2, max is 1). Result is 0.
2. **Requirement at index 0** — must be `[0, 0]` (single element has 0 inversions). Otherwise 0.
3. **No requirements** — answer is n! (all permutations valid).
4. **Conflicting requirements** at different indices — DP automatically handles by zeroing dead states; conflicts cascade to 0.
5. **Requirement at n−1** — restricts the final answer to a single dp cell.

## 8. Approaches comparison (§10)

1. **Brute force (enumerate all n! perms)** — O(n! · n) time. Works only for n ≤ 8 or so.
2. **Naive DP (no sliding window)** — O(n · max_inv²) time. Each `dp[i][j]` sums up to `i+1` previous values directly. Acceptable for moderate n.
3. **Sliding-window DP (chosen)** — O(n · max_inv) time. Each row's prefix sum is maintained incrementally; transitions become O(1) per cell.

## 9. Take home (§12)

- **LC 629 K Inversions** — count permutations of [1..n] with exactly k inversions. Same DP structure, no requirements.
- **LC 920 Number of Music Playlists** — different problem, same "insert and count" DP pattern.
- **LC 1359 Count All Valid Pickup and Delivery Options** — another permutation-counting DP with positional constraints.

## 10. Python verification

Algorithm under test:

```python
MOD = 10**9 + 7

def numberOfPermutations(n, requirements):
    req = {end: cnt for end, cnt in requirements}
    if 0 in req and req[0] != 0:
        return 0
    max_inv = max(req.values()) if req else n * (n - 1) // 2
    dp = [0] * (max_inv + 1)
    dp[0] = 1
    for i in range(1, n):
        new_dp = [0] * (max_inv + 1)
        # sliding window prefix sum
        running = 0
        for j in range(max_inv + 1):
            running = (running + dp[j]) % MOD
            if j > i:
                running = (running - dp[j - i - 1]) % MOD
            new_dp[j] = running
        if i in req:
            target = req[i]
            new_dp = [v if j == target else 0 for j, v in enumerate(new_dp)]
        dp = new_dp
    if n - 1 in req:
        return dp[req[n - 1]] % MOD
    return sum(dp) % MOD


# Test cases
print(numberOfPermutations(3, []))          # expected 6
print(numberOfPermutations(3, [[2, 2]]))    # expected 2
print(numberOfPermutations(2, [[1, 0]]))    # expected 1 ([0,1])
print(numberOfPermutations(2, [[1, 1]]))    # expected 1 ([1,0])
print(numberOfPermutations(3, [[2, 5]]))    # expected 0 (impossible: max inversions at index 2 is 3)
```

Trace output (all pass):

```
6
2
1
1
0
```
