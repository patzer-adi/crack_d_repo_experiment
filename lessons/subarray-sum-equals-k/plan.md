# Subarray Sum Equals K — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata

- **Slug:** `subarray-sum-equals-k`
- **LC #:** 560
- **Difficulty:** Medium
- **Topic:** Prefix Sum / Arrays
- **Archetype:** `prefix_scan` — the core pattern is "scan left-to-right, compute a running prefix value (cumulative sum), record when a prefix has been seen before, and count how many times the complement (sum - k) has appeared."

## 1. Clarifying questions (§0)

1. **"What is a 'contiguous subarray'?"**
   *A:* A contiguous subarray is defined by a start and end index. All elements between (inclusive) must be included.
   *Unlocks:* We track positions and compute sums over ranges.

2. **"If no subarray sums to K, what do I return?"**
   *A:* Return 0 — no such subarray exists.
   *Unlocks:* Answer is always ≥ 0; initialize count = 0.

3. **"Can K be negative, zero, or very large?"**
   *A:* Yes — K can be any integer. Elements can also be negative.
   *Unlocks:* No constraints on values; use a prefix-sum approach which handles negative numbers naturally.

4. **"Do I need to return indices, or just the count?"**
   *A:* Just the count of subarrays. Return type is an integer.
   *Unlocks:* We count, not track, so use a frequency map.

## 2. Kernel paragraph (§1)

As you walk left-to-right through the array, maintain the cumulative sum. At each position i, ask: "how many times have I seen the value (current_sum - K) before?" Each such occurrence represents a subarray ending at i that sums to K. A hash map answers "have I seen value c before, and how many times?" in O(1). So: maintain `prefix_sum → count` of all prefixes seen so far; at each i, compute the current prefix sum, check how many times (current_sum - K) appears in the map, add that count to the result, then increment the map entry for the current prefix sum.

## 3. Foundational concept visual (§1)

A horizontal strip of array cells with values. Below it, a running prefix-sum line showing the cumulative sum at each position (starting at 0 before index 0). A "prefix sum map" panel shows the frequency of each prefix value. When the current sum differs from a previously-seen sum by exactly K, that's a match — the subarray between them sums to K.

## 4. Translations (§3)

1. **From 'check every subarray' to 'prefix sums and their complements'.**
   Instead of checking all O(n²) subarrays, note that if `prefix[j] - prefix[i-1] = K`, then the subarray [i, j] sums to K. Equivalently, if the current prefix sum is S and we've seen (S - K) before, then every occurrence of (S - K) marks the start of a subarray that ends here with sum K. We just need to count.
   Gain: O(n²) pair check → implicit via prefix recurrence.

2. **From 'count per prefix' to 'frequency map, one pass'.**
   For each unique prefix sum value, we want to know "how many times have I seen it?" so that when we encounter it again (shifted by K), we can count the matches. Maintain `prefix_sum → frequency`; at each position, probe for (current_sum - K), add its count to the result, then increment the map entry for the current sum. One pass; each step is O(1) average.
   Gain: O(n²) brute force → O(n) hash-map lookup.

## 5. Algorithm in plain English (§4)

1. **Initialise** a hash map `prefix_count` with entry {0: 1}. The entry for 0 is initialized to 1 because an empty prefix (before any elements) has sum 0.
2. **Set** count = 0 and prefix_sum = 0.
3. **Walk** `i` from `0` to `n−1`.
4. **Update** prefix_sum by adding `nums[i]`.
5. **Compute** complement = prefix_sum - K.
6. **If** complement is in `prefix_count`, add `prefix_count[complement]` to count.
7. **Increment** `prefix_count[prefix_sum]` by 1.
8. **Return** count after the loop completes.

## 6. Examples for code viz + dry run (§6, §7)

**Fast example (4–6 steps):**
- Input: `nums = [1, 1, 1], k = 2`
- Expected: `2` (subarrays [1,1] at indices [0,1] and [1,2])
- Path: prefix sums are 0, 1, 2, 3. At i=1, sum=2, complement=0, found 1 match. At i=2, sum=3, complement=1, found 1 match. Total: 2.

**Medium example (8–10 steps):**
- Input: `nums = [1, 2, 1, 2, 1], k = 3`
- Expected: `4` (subarrays [1,2], [2,1], [1,2], [2,1])
- Path: walk through, track prefix sums and their frequencies.

**Slow example (12–15 steps) — with negatives:**
- Input: `nums = [1, -1, 1, 2, 1], k = 2`
- Expected: `?` (to be computed in dry run)

## 7. Corner cases (§8)

1. **All elements are 0:** prefix sums are all 0. If k=0, every subarray sums to 0 — answer is n(n+1)/2.
2. **All elements are K:** prefix sums form a sequence 0, K, 2K, 3K, ... At each step, if (sum - K) exists, count it.
3. **No subarray sums to K:** answer is 0.
4. **Negative K:** e.g., k = -5. Same algorithm; no special case.
5. **Single element = K:** e.g., [5], k = 5. At i=0, sum=5, complement=0, found 1. Answer: 1.
6. **Empty array:** loop never runs, count stays 0. Correct.
7. **Why initialise prefix_count[0] = 1?** The empty prefix (before any elements) has sum 0. If a subarray from index 0 to i sums to K, then prefix[i] - prefix[-1] = K, i.e., prefix[i] = K. We'd look for (prefix[i] - K) = 0, which is the empty prefix. So we need {0: 1} to count subarrays starting at index 0.

## 8. Algorithm complexity

- **Time:** O(n) — one pass; each step does an O(1) average hash probe and an O(1) increment.
- **Space:** O(n) — the map stores at most n unique prefix sums.

## 9. Related problems

- **LC 525 — Contiguous Array:** same prefix-sum technique, but checking for balance (equal 0s and 1s) instead of a target sum.
- **LC 523 — Continuous Subarray Sum:** asks if there exists a subarray summing to K modulo some divisor. Uses (sum % m) as the prefix key.
- **LC 974 — Subarray Sums Divisible by K:** similar; asks for subarrays whose sum is divisible by K. Use (sum % K) as the prefix key.
- **LC 1099 — Two Sum Less Than K:** asks for the maximum sum *less than* K. Hash map breaks (range query); optimal is sort + two-pointer.
