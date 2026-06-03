# Contiguous Array — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `contiguous-array`
- **LC #:** 525
- **Difficulty:** Medium
- **Topic:** Prefix Sum / Arrays
- **Archetype:** `prefix_scan` — the core pattern is "scan left-to-right, compute a running prefix value (balance), and record when a prefix has been seen before." The array is binary (0s and 1s); the optimization is to treat mismatches as a **balance** (+1 for 1, −1 for 0) and find the longest window where the balance returns to a previously-seen value.

## 1. Clarifying questions (§0)

1. **"What does 'equal number of 0s and 1s' mean?"**
   *A:* A contiguous subarray where the count of 1s equals the count of 0s.
   *Unlocks:* We need to find the longest such contiguous window, not just any window.

2. **"How do I measure 'contiguous'?"**
   *A:* A subarray is defined by a start and end index; all elements between (inclusive) must be part of the answer.
   *Unlocks:* We must track the span, not just a pair of values.

3. **"If no balanced subarray exists, what should I return?"**
   *A:* Return 0 — the empty subarray has length 0 and is trivially balanced.
   *Unlocks:* The answer is always ≥ 0; the loop never fails to complete.

4. **"Can the input be all 0s, all 1s, or empty?"**
   *A:* Yes — edge cases include empty array (length 0), single element (length 0), all 0s, all 1s, or equal mix. The algorithm must handle all gracefully.
   *Unlocks:* Initialize the map with balance 0 at index −1 to account for subarrays starting at index 0.

## 2. Kernel paragraph (§1)

Convert the problem: instead of asking "how many 0s vs 1s?", ask "what is the **balance**?" Assign each 1 a value of +1 and each 0 a value of −1. Walk left-to-right and accumulate the balance. Whenever the balance *returns* to a value we've seen before, the subarray between the two positions has equal 0s and 1s (the balance change is 0). Record the first position at which each balance value occurs; the maximum span is the distance between the earliest and latest occurrence of any balance value.

A hash map answers "have I seen balance B before, and at what (earliest) index?" in O(1). So: maintain `balance → first_index`; at each position, compute the balance; if we've seen it, compute the span; track the max span.

## 3. Foundational concept visual (§1)

A horizontal strip of array cells, each marked 1 or 0. Below it, a running prefix sum line showing the balance at each position (starting at 0 before index 0, then +1 or −1 at each step). A "seen balance map" panel records the first occurrence of each balance value. When the balance line *dips back* to a value it hit before, that span is highlighted in success-green and the span length is recorded.

## 4. Translations (§3)

1. **From 'count 0s and 1s' to 'balance'.**
   Instead of separately counting 0s and 1s at each subarray, map 0 → −1 and 1 → +1. At any position, if the cumulative balance is 0, the subarray from start to here has equal 0s and 1s. More generally, if the balance at position j equals the balance at position i (i < j), then the subarray [i+1, j] has equal 0s and 1s — because the balance change is 0.
   Gain: explicit pair matching (O(n²) brute force) → implicit via a common prefix value.

2. **From 'track every subarray' to 'first occurrence of each balance'.**
   The length of a balanced subarray from index i to j is (j − i). To maximise this, for each balance value, we want the earliest index where it appears (to maximise j − i). A hash map stores balance → first_index; when we encounter a balance again, we compute (current_index − first_index) and update the max. One pass; O(1) per lookup.
   Gain: O(n²) brute force pair check → O(n) single-pass scan.

## 5. Algorithm in plain English (§4)

1. **Initialise** a hash map `first_balance` with `{0: -1}` (balance 0 occurs before the array starts, at index −1).
2. **Set** max_length = 0, balance = 0.
3. **Walk** `i` from `0` to `n−1`.
4. **Update** balance: if `nums[i] == 1`, add 1; else subtract 1.
5. **If** balance is in `first_balance`, compute `current_span = i − first_balance[balance]` and update max_length.
6. **Else** (first time seeing this balance), record `first_balance[balance] = i`.
7. **Return** max_length.

## 6. Examples for code viz + dry run (§6, §7)

**Fast example (3–5 steps):**
- Input: `nums = [0, 1]`
- Expected: `2`
- Path: balance starts at 0. i=0: nums[0]=0, balance=−1, first time, store −1→0. i=1: nums[1]=1, balance=0, seen before at −1, span=1−(−1)=2. max_length=2.

**Medium example (6–8 steps):**
- Input: `nums = [0, 0, 1, 0, 0, 0, 1, 1]`
- Expected: `6`
- Path: walk through, track balance. At i=3 balance=−1, match with i=0's balance. At i=7 balance=0, match init. Final answer is span from i=2 to i=7 (length 6: [1,0,0,0,1,1]).

**Slow example (10–12 steps) — complex balance wave:**
- Input: `nums = [1, 0, 0, 1, 1, 0, 1, 0]`
- Expected: `?` (to be computed in dry run)

## 7. Corner cases (§8)

1. **All 0s:** balance never returns to 0, max_length stays 0.
2. **All 1s:** balance never returns to 0, max_length stays 0.
3. **Single element:** array of length 1 can't have equal 0s and 1s, return 0.
4. **Empty array:** return 0 (no balanced subarray).
5. **Entire array is balanced:** e.g., [0, 1, 1, 0]. At the end, balance=0 (seen at −1), so span = n − (−1) = n.
6. **Multiple spans, one is max:** the algorithm tracks only the first occurrence of each balance, which is correct for maximising the span.

## 8. Algorithm complexity

- **Time:** O(n) — one pass; each step does an O(1) average hash probe and an O(1) average insert.
- **Space:** O(n) — the map stores at most n+1 entries (one per unique balance value).

## 9. Related problems

- **LC 560 — Subarray Sum Equals K:** same prefix-sum technique, but looking for a target sum instead of returning to the same balance.
- **LC 1099 — Two Sum Less Than K:** different problem, but shares the "maximize the span between two indices with a property" shape.
- **LC 1455 — Check If a Word Is Valid After Substitutions:** different domain, but the idea of "when does a repeated state occur?" is the same kernel.
