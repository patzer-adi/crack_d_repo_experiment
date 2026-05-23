# Majority Element — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `majority-element`
- **LC #:** 169
- **Difficulty:** Easy
- **Topic:** Array
- **Archetype:** `custom` (Boyer-Moore Voting — streaming cancellation algorithm; no pointer movement or windowing; optimisation is vote-counting, not spatial).

## 1. Clarifying questions (§0)

1. **Q:** Is the majority element guaranteed to exist?
   **A:** Yes — the problem guarantees exactly one element appears more than ⌊n/2⌋ times.
   **Unlock:** We never need to handle "no majority found." Boyer-Moore's surviving candidate is always correct.

2. **Q:** Can we modify the input array?
   **A:** Not required. Boyer-Moore scans in one pass with no writes to the array.
   **Unlock:** O(1) extra space is achievable — no auxiliary storage needed.

3. **Q:** What are the constraints?
   **A:** 1 ≤ n ≤ 5×10⁴; elements are 32-bit integers.
   **Unlock:** Even O(n log n) sort easily fits. The interesting goal is O(n) time, O(1) space.

4. **Q:** Why not just use a hash map to count frequencies?
   **A:** A hash map gives O(n) time and O(n) space. It works, but we can do O(1) space.
   **Unlock:** This is the motivation for Boyer-Moore — the observation that votes cancel, so we only need to track one candidate at a time.

## 2. Kernel paragraph (§1)

If one element appears more than ⌊n/2⌋ times, the non-majority elements cannot outnumber it — no matter how they combine, the majority element always has votes to spare. Imagine tallying: keep a single `candidate` and a `count`. When you see the current candidate, increment count (a vote for it); when you see anything else, decrement count (a vote against). When count reaches zero, you've consumed equal "pro" and "anti" votes and can discard that entire prefix — whoever is majority was equally present on both sides, so it isn't eliminated. Reset candidate to the current element and start over. After one pass the surviving candidate holds the majority.

## 3. Foundational concept visual (§1)

A row of array cells with `candidate` and `count` displayed as two prominent boxes. The visual shows three color states for each cell:
- **Green** (same as candidate): count ticks up
- **Orange** (different from candidate): count ticks down
- **Wipe** (count hits 0): candidate resets to current element, cell flashes yellow

Concrete example: `[2, 1, 1, 2, 2]`. Show the candidate changing from 2→1→2, count going 1→0→1→0→1. Final candidate 2 survives and is circled green.

## 4. Translations (§3)

**Translation 1 — Brute force → hash map.**
The O(n²) approach counts each element by scanning the entire array for it. Instead, one pass builds a frequency map in O(n) time and O(n) space; then a second scan (or inline check) finds the key with count > n/2.
→ `O(n²) → O(n) time; O(1) → O(n) space (temporary hash map)`

**Translation 2 — Hash map → Boyer-Moore vote.**
The hash map stores counts for every distinct element. But we only need one answer. The key insight: when a non-candidate element cancels a candidate vote (count drops to 0), that entire matched pair can be discarded — neither side changed the majority relationship. We track only one candidate and one count. No hash map, no extra allocation.
→ `O(n) time, O(n) space → O(n) time, O(1) space`

## 5. Algorithm in plain English (§4)

1. Set `candidate = 0` and `count = 0`.
2. For each `num` in the array:
3. &nbsp;&nbsp;&nbsp;If `count` is 0, **reassign** `candidate = num` (start a fresh tally).
4. &nbsp;&nbsp;&nbsp;**Update** `count`: add 1 if `num == candidate`, subtract 1 otherwise.
5. After the loop, **return** `candidate` — it is the majority element.

## 6. Examples for code viz + dry run (§6, §7)

**Fast example:** `nums = [2, 2, 1, 1, 2]` → **2** (~5 viz steps)
- i=0: count=0 → candidate=2, count=1
- i=1: 2==2 → count=2
- i=2: 1≠2 → count=1
- i=3: 1≠2 → count=0
- i=4: count=0 → candidate=2, count=1
- Return 2.

**Slow example:** `nums = [2,2,2,1,2,1,2,1,2,1,2]` → **2** (11 viz steps; count oscillates but never resets after i=0; shows a dominant majority that never gets wiped)
- i=0: count=0 → candidate=2, count=1
- i=1: 2==2 → count=2
- i=2: 2==2 → count=3
- i=3: 1≠2 → count=2
- i=4: 2==2 → count=3
- i=5: 1≠2 → count=2
- i=6: 2==2 → count=3
- i=7: 1≠2 → count=2
- i=8: 2==2 → count=3
- i=9: 1≠2 → count=2
- i=10: 2==2 → count=3
- Return 2.

**Dry run example:** `nums = [2, 1, 1, 2, 2]` → **2** (shows candidate changing twice mid-stream; good for demonstrating the "wipe" behavior)
- i=0: count=0 → candidate=2, count=1
- i=1: 1≠2 → count=0
- i=2: count=0 → candidate=1, count=1  ← candidate changes to 1
- i=3: 2≠1 → count=0
- i=4: count=0 → candidate=2, count=1  ← candidate changes back to 2
- Return 2.

## 7. Corner cases (§8)

1. **n=1 (e.g. `[7]`):** count=0 → candidate=7, count=1. Loop ends. Return 7. A single element is trivially majority.
2. **All identical (e.g. `[3,3,3,3]`):** count climbs 1,2,3,4; candidate stays 3. No wipe ever needed.
3. **Minority at start, majority takes over (e.g. `[1,2,2,2,2]`):** candidate=1 then wiped at i=1 to candidate=2, count builds up. Confirms wipe can happen at index 1.
4. **Two-value alternating (e.g. `[1,2,1,2,1]`):** candidate resets at every wipe but majority (1) always claims the final slot. count never exceeds 1.
5. **Candidate changes multiple times (e.g. `[2,1,1,2,2]`):** illustrated in dry-run example. Candidate changes 2→1→2. Final correct answer 2 survives.

## 8. Approaches comparison (§10)

**Approach 1 — Boyer-Moore Voting (taught).**
Maintain `candidate` and `count`; cancel votes on mismatches; reset on zero. **O(n) time, O(1) space**. Requires that majority is guaranteed to exist (if not, a second O(n) verification pass is needed). Hardest to explain intuitively but trivial to implement.

**Approach 2 — Hash map.**
Count all elements in a `unordered_map`, return the key with count > n/2. **O(n) time, O(n) space**. Straightforward to derive and requires no special insight. Good first answer in an interview before optimizing.

**Approach 3 — Sort.**
Sort the array; `nums[n/2]` is always the majority element (it occupies the median). **O(n log n) time, O(1) or O(n) space** (depending on sort). Elegant correctness argument but the O(n log n) factor is hard to beat in an interview without a strong reason.

## 9. Take home (§12)

- **229. Majority Element II** — same voting idea extended to k=3 buckets; find all elements appearing > n/3 times. Requires maintaining two candidates simultaneously.
- **1150. Check If a Number Is Majority Element in a Sorted Array** — binary search for first/last occurrence of `target`; length ≥ n/2+1 confirms majority. Sorted structure makes O(log n) possible.
- **169. (self)** — the gateway to streaming / online algorithms; same cancel-and-reset idea underlies heavy-hitters sketches in data stream algorithms.
- **912. Sort an Array** — context for the sort approach; understanding in-place sort makes the `nums[n/2]` shortcut natural.

## 10. Python verification (BEFORE writing HTML)

```
=== Fast example: nums = [2, 2, 1, 1, 2] (expect 2) ===
candidate=0 count=0
  i=0 num=2: count==0 -> candidate=2, count=1
  i=1 num=2: num==candidate -> count=2
  i=2 num=1: num!=candidate -> count=1
  i=3 num=1: num!=candidate -> count=0
  i=4 num=2: count==0 -> candidate=2, count=1
Result: 2, Expected: 2 ✓

=== Slow example: nums = [2,2,2,1,2,1,2,1,2,1,2] (expect 2) ===
candidate=0 count=0
  i=0 num=2: count==0 -> candidate=2, count=1
  i=1 num=2: num==candidate -> count=2
  i=2 num=2: num==candidate -> count=3
  i=3 num=1: num!=candidate -> count=2
  i=4 num=2: num==candidate -> count=3
  i=5 num=1: num!=candidate -> count=2
  i=6 num=2: num==candidate -> count=3
  i=7 num=1: num!=candidate -> count=2
  i=8 num=2: num==candidate -> count=3
  i=9 num=1: num!=candidate -> count=2
  i=10 num=2: num==candidate -> count=3
Result: 2, Expected: 2 ✓

=== Dry run example: nums = [2, 1, 1, 2, 2] (expect 2) ===
candidate=0 count=0
  i=0 num=2: count==0 -> candidate=2, count=1
  i=1 num=1: num!=candidate -> count=0
  i=2 num=1: count==0 -> candidate=1, count=1
  i=3 num=2: num!=candidate -> count=0
  i=4 num=2: count==0 -> candidate=2, count=1
Result: 2, Expected: 2 ✓

=== Corner: nums=[7] (expect 7) ===
  i=0 num=7: count==0 -> candidate=7, count=1
Result: 7, Expected: 7 ✓

=== Corner: nums=[3,3,3,3] (expect 3) ===
  i=0: count==0 -> candidate=3, count=1
  i=1: num==candidate -> count=2
  i=2: num==candidate -> count=3
  i=3: num==candidate -> count=4
Result: 3, Expected: 3 ✓

=== Corner: nums=[1,2,2,2,2] (expect 2) ===
  i=0: count==0 -> candidate=1, count=1
  i=1: num!=candidate -> count=0
  i=2: count==0 -> candidate=2, count=1
  i=3: num==candidate -> count=2
  i=4: num==candidate -> count=3
Result: 2, Expected: 2 ✓
```

All 6 cases match expected.
