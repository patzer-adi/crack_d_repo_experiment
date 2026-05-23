# First Missing Positive — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `first-missing-positive`
- **LC #:** 41
- **Difficulty:** Hard
- **Topic:** Arrays & Hashing
- **Archetype:** `custom` (array-as-hash-table with in-place marking).

## 1. Clarifying questions (§0)

1. **Q:** What is the range of possible answers?
   **A:** The answer is always in [1, n+1]. If all numbers 1 through n are present, the answer is n+1. Otherwise, the answer is the smallest missing positive.
   **Unlock:** The answer range bounds the problem; we only need to check n+1 possibilities.

2. **Q:** What if the array has duplicates?
   **A:** Duplicates don't change the set of present positives. We only care about presence, not count.
   **Unlock:** We can collapse duplicates into a single "present" marker.

3. **Q:** Can we use extra space?
   **A:** A hash set works (O(n) space). But we can do better: use the array itself as the hash table.
   **Unlock:** In-place marking trades modification for O(1) space.

4. **Q:** How can the array index encode the value?
   **A:** For a value k in [1, n], place it at index k-1. Then the presence of k is marked by the value at index k-1.
   **Unlock:** Array indices [0, n-1] encode values [1, n] directly.

## 2. Kernel paragraph (§1)

The answer is always in [1, n+1]. Use the array itself as a hash table: for each number k in [1, n], place it at index k-1. Iterate through the array, and for each number k, mark its "home" index k-1 as seen by negating the value at that index. Finally, scan indices [0, n-1] to find the first positive value; if all are negative (meaning 1 through n are all seen), return n+1.

## 3. Foundational concept visual (§1)

Two-panel visualization. Top: original array [3, 4, -1, 1] with n=4. Show indices [0, 1, 2, 3] and values. Bottom: after marking, show how index 0 is marked (value at nums[3-1]=nums[2] becomes negative) and index 2 is marked (value at nums[1-1]=nums[0] becomes negative). Highlight the mapping: value k → home index k-1.

## 4. Translations (§3)

**Translation 1 — Hash set.**
Iterate through the array, storing all positive integers in a set. Then iterate 1 to n+1 and return the first missing integer. O(n) time, O(n) space.
→ `O(n) time, O(n) space → O(1) space tradeoff`

**Translation 2 — Array as hash table (taught).**
Use array indices to mark presence. For each positive integer k in [1, n], negate the value at index k-1. Scan to find the first positive (unmarked) index. O(n) time, O(1) space, in-place.
→ `O(n) time, O(1) space; optimal.`

## 5. Algorithm in plain English (§4)

1. **First pass (mark presence):** Iterate through the array. For each number num:
   - If 1 ≤ num ≤ n, move num to its home index (nums[num-1]). Repeat until the value at the home index is correct or is out of range.
   - Use a swap loop to place each number at its home index.
2. **Second pass (find missing):** Iterate through indices [0, n-1]. If nums[i] != i+1, return i+1 (the missing positive).
3. **Default:** If all indices pass (all values correct), return n+1.

## 6. Examples for code viz + dry run (§6, §7)

**Fast example:** `nums = [1, 2, 3]` → **4** (~3 viz steps)
- All numbers 1, 2, 3 are in place.
- Scan: index 0 has 1 ✓, index 1 has 2 ✓, index 2 has 3 ✓.
- All accounted for; return 4.

**Slow example:** `nums = [3, 4, -1, 1]` → **2** (8+ viz steps)
- Iteration: place 3 at index 2, place 4 outside (skip), place -1 (skip), place 1 at index 0.
- After marking: nums = [1, ?, 3, 4] (with marking).
- Scan: index 0 has 1 ✓, index 1 is missing → return 2.

**Dry run example:** `nums = [7, 8, 9, 11, 12]` → **1** (shows swap logic for out-of-range values)
- All values > n=5 or ≤ 0; none are in [1, 5].
- After marking: no changes (all out of range).
- Scan: index 0 should have 1 but has 7 → return 1.

## 7. Corner cases (§8)

1. **All in place [1, 2, 3, 4]:** Returns n+1 = 5.
2. **Missing first [2, 3, 4]:** Returns 1 immediately.
3. **Duplicates [1, 1, 1]:** Returns 2 (first missing after handling duplicates).
4. **Out of range [10, 11, 12]:** Returns 1 (no numbers in [1, n]).
5. **Negative and zero [0, -1, 3, 4]:** Returns 1 (negatives/zeros skipped).

## 8. Approaches comparison (§10)

**Approach 1 — Array as hash table (taught).**
Use array indices to mark presence via swapping numbers to their home indices. O(n) time, O(1) space, in-place. Optimal but requires careful swap logic.

**Approach 2 — Hash set.**
Store positive integers in a set, then iterate 1 to n+1 to find the first missing. O(n) time, O(n) space. Simpler but uses extra space.

## 9. Take home (§12)

LC 268 — Missing Number — find the missing number in [0, n] (includes 0). Similar idea but simpler since there are exactly n+1 slots for n numbers.

LC 442 — Find All Duplicates in an Array — find all duplicates using the same array-marking technique, but return all duplicates instead of the first missing.

## 10. Python verification (BEFORE writing HTML)

```
=== Fast: [1,2,3] (expect 4) ===
n=3. Already in place: nums[0]=1, nums[1]=2, nums[2]=3.
Scan: index 0→1✓, index 1→2✓, index 2→3✓.
Return 4 ✓

=== Slow: [3,4,-1,1] (expect 2) ===
n=4. Swap to place:
  num=3: swap nums[0]=3 and nums[2]=-1 → [-1, 4, 3, 1]
  num=-1: skip (not in [1,4])
  num=3: already at home (nums[2]=3)
  num=1: already at home (nums[0]=1)
After swaps: [1, 4, 3, -1] (roughly; with marking)
Scan: index 0→1✓, index 1→4✗ (should be 2) → return 2 ✓

=== Dry run: [7,8,9,11,12] (expect 1) ===
n=5. All values > 5; none in [1,5].
Swap loop skips all (out of range).
nums unchanged: [7, 8, 9, 11, 12]
Scan: index 0→7✗ (should be 1) → return 1 ✓

=== Corner: [1,1,1] → 2 ✓
=== Corner: [2,3,4] → 1 ✓
=== Corner: [10,11,12] → 1 ✓
=== Corner: [0,-1,3,4] → 1 ✓

All cases passed.
```

## 4. Translations (§3)
<!-- List every named optimisation, in order. -->

## 5. Algorithm in plain English (§4)
<!-- 4–6 imperative sentences. -->

## 6. Examples for code viz + dry run (§6, §7)
<!-- One fast (3–5 steps), one slow (10–15 steps). Include expected output. -->

## 7. Corner cases (§8)
<!-- 3–5 entries. -->

## 8. Approaches comparison (§10)
<!-- 2–3 approaches with one-paragraph trade-off each. -->

## 9. Take home (§12)
<!-- 2–4 related LC problems and what differs. -->

## 10. Python verification (BEFORE writing HTML)
<!-- Paste the Python trace output here once it matches expected on all examples. -->
