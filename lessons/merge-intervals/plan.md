# Merge Intervals — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `merge-intervals`
- **LC #:** 56
- **Difficulty:** Medium
- **Topic:** Arrays / Sorting
- **Archetype:** `custom` (sort + sweep / line-sweep — none of the four standard archetypes fit; using `lessons/design/sec*.md` principles only, no canonical-golden excerpts)

## 1. Clarifying questions (§0)

1. **Q:** "Are the input intervals sorted?"
   **A:** No — they arrive in arbitrary order.
   **Unlocks:** We must sort first. Sorting by start key is what turns an O(n²) all-pairs overlap check into a single linear sweep.

2. **Q:** "Are intervals closed or half-open? Do `[1,4]` and `[4,7]` overlap?"
   **A:** Per LC 56, intervals are closed and touching counts as overlapping. `[1,4]` ∪ `[4,7]` = `[1,7]`.
   **Unlocks:** The overlap test is `next.start <= open.end` (≤, not strict <).

3. **Q:** "Can intervals be identical or fully contained in one another?"
   **A:** Yes — duplicates and full containment are allowed.
   **Unlocks:** Use `max(open.end, next.end)` when extending — the next interval's end can be smaller (containment) or equal (duplicate) without breaking anything.

4. **Q:** "Can the input be empty?"
   **A:** Per LC 56 the constraint is `intervals.length >= 1`, but defending against empty input is cheap.
   **Unlocks:** A single early-return guard for empty input; otherwise we can safely seed the sweep with `intervals[0]`.

## 2. Kernel paragraph (§1)

The problem becomes trivial the moment we sort by start. Once sorted, scan the list keeping a single "open" interval. For each next interval: if its start is ≤ the open interval's end, the two overlap — extend the open interval's end to `max(open.end, next.end)`. Otherwise the open interval is finalised (push it to the output) and the next interval becomes the new open one. The reason this works without rechecking earlier intervals: because input is sorted by start, once we see a next start that exceeds the current open end, every interval after it has a start that's even larger — none of them can overlap with the open interval either.

## 3. Foundational concept visual (§1)

A horizontal axis with intervals drawn as horizontal bars at staggered y-positions, then a second axis below showing the same intervals after sorting (now monotonically left-aligned by start). A green "open" bar at the bottom slides and grows as the sweep proceeds; whenever a non-overlapping interval is encountered, the current green bar locks (turns dark green / "finalised") and a new green bar starts.

## 4. Translations (§3)

1. **"Find every overlap"** → `if next.start <= open.end then they overlap`. The overlap test for two intervals reduces to a single comparison once we know which one starts earlier.
2. **Sort by start** → guarantees that if `next.start > open.end`, no interval after `next` overlaps `open` either (their starts are all ≥ `next.start`). This is what justifies a single sweep instead of an all-pairs check.
3. **Sweep with a single "open" interval** → maintain one mutable `[s, e]` pair. Extend its `e` on overlap; otherwise emit it and replace it with the new interval.
4. **Extend = `e = max(open.end, next.end)`** → covers containment (`next.end < open.end`) and duplicates (`next.end == open.end`) without a special case.

## 5. Algorithm in plain English (§4)

1. **Sort** `intervals` by start. (Stable order isn't required.)
2. **Initialise** the output list and the "open" interval `open = intervals[0]`.
3. **For each `next` in `intervals[1..]`:**
   a. If `next.start <= open.end`, **extend**: `open.end = max(open.end, next.end)`.
   b. Otherwise, **finalise**: push `open` to the output, then `open = next`.
4. After the loop, **flush** the final `open` to the output.
5. Return the output.

## 6. Examples for code viz + dry run (§6, §7)

### Fast example (~6 steps): `[[1,3], [2,6], [8,10], [15,18]]` → `[[1,6], [8,10], [15,18]]`

Already sorted. One merge ([1,3] + [2,6] → [1,6]), then two non-overlapping intervals are emitted unchanged. The classic LC #56 example.

### Slow example (10 sweep steps + sort step): `[[8,12], [1,4], [14,20], [7,9], [22,25], [2,5], [13,15], [24,28]]` → `[[1,5], [7,12], [13,20], [22,28]]`

8 intervals presented out of order, so the sort step is visible (input ≠ sorted). After sorting, the sweep alternates extend/finalise across four merge groups, producing 4 final intervals. Visualisation steps: 1 sort + 1 init + 7 iterations + 1 flush = 10 steps.

## 7. Corner cases (§8)

1. **Single interval** — `[[1,2]]` → `[[1,2]]`. Loop body never runs; we flush the seeded `open` and return.
2. **Touching at endpoint** — `[[1,4], [4,7]]` → `[[1,7]]`. The overlap test must use `≤`, not `<`. With `<`, touching intervals would be wrongly emitted as separate.
3. **Fully contained** — `[[1,10], [3,5]]` → `[[1,10]]`. The `max` in the extend step keeps `open.end = 10`; the contained interval contributes nothing new.
4. **Identical duplicates** — `[[2,5], [2,5]]` → `[[2,5]]`. Same path as containment; `max(5, 5) = 5`.
5. **None overlap** — `[[1,2], [3,4], [5,6]]` → unchanged. Every iteration takes the finalise branch; the output equals the (sorted) input.

## 8. Approaches comparison (§10)

1. **Brute force — repeated all-pairs merge** — scan every pair, merge any that overlap, repeat until a full pass produces no merges. Worst-case O(n³) (or O(n²) with Union-Find). Easy to get wrong on pairs that newly overlap *after* an earlier merge.
2. **Sort + sweep (chosen)** — O(n log n) for the sort, O(n) for one sweep. Total O(n log n). Easy to argue correct: sort makes overlap a local condition.
3. **Connected-components view** — build a graph with one node per interval and an edge between any two that overlap, then output one merged interval per component. Same time complexity as sort+sweep but more code and worse constants. Useful framing for related problems where intervals are on a graph already.

## 9. Take home (§12)

- **LC 57 Insert Interval** — same merge logic, but only one new interval is being inserted into an already-sorted list. O(n) without a sort.
- **LC 252/253 Meeting Rooms / Meeting Rooms II** — same sort-by-start. Variant 1 just asks "any overlap?"; variant 2 asks "max simultaneous overlaps" (heap of end-times).
- **LC 435 Non-overlapping Intervals** — sort by *end* (not start) to greedily keep the earliest-ending interval, minimizing removals.
- **LC 1288 Remove Covered Intervals** — sort by start asc, end desc, then count the strictly increasing-end intervals.

## 10. Python verification (BEFORE writing HTML)

Algorithm under test:

```python
def merge(intervals):
    arr = sorted(intervals, key=lambda x: x[0])
    if not arr: return []
    out = []
    open_iv = list(arr[0])
    for s, e in arr[1:]:
        if s <= open_iv[1]:
            open_iv[1] = max(open_iv[1], e)
        else:
            out.append(open_iv)
            open_iv = [s, e]
    out.append(open_iv)
    return out
```

Trace output (all five examples pass):

```
Input:    [[1, 3], [2, 6], [8, 10], [15, 18]]
Sorted:   [[1, 3], [2, 6], [8, 10], [15, 18]]
  init open = [1, 3]
  i=1 [2,6]: s(2) <= open.end(3) → extend; open = [1, max(3,6)=6]
  i=2 [8,10]: s(8) >  open.end(6) → finalise [1, 6]; open = [8,10]
  i=3 [15,18]: s(15) >  open.end(10) → finalise [8, 10]; open = [15,18]
  flush final open: [15, 18]
Result:   [[1, 6], [8, 10], [15, 18]]
Expected: [[1, 6], [8, 10], [15, 18]]
OK

Input:    [[8, 12], [1, 4], [14, 20], [7, 9], [22, 25], [2, 5], [13, 15], [24, 28]]
Sorted:   [[1, 4], [2, 5], [7, 9], [8, 12], [13, 15], [14, 20], [22, 25], [24, 28]]
  init open = [1, 4]
  i=1 [2,5]: s(2) <= open.end(4) → extend; open = [1, max(4,5)=5]
  i=2 [7,9]: s(7) >  open.end(5) → finalise [1, 5]; open = [7,9]
  i=3 [8,12]: s(8) <= open.end(9) → extend; open = [7, max(9,12)=12]
  i=4 [13,15]: s(13) >  open.end(12) → finalise [7, 12]; open = [13,15]
  i=5 [14,20]: s(14) <= open.end(15) → extend; open = [13, max(15,20)=20]
  i=6 [22,25]: s(22) >  open.end(20) → finalise [13, 20]; open = [22,25]
  i=7 [24,28]: s(24) <= open.end(25) → extend; open = [22, max(25,28)=28]
  flush final open: [22, 28]
Result:   [[1, 5], [7, 12], [13, 20], [22, 28]]
Expected: [[1, 5], [7, 12], [13, 20], [22, 28]]
OK

Input:    [[1, 4], [4, 7]]
Sorted:   [[1, 4], [4, 7]]
  init open = [1, 4]
  i=1 [4,7]: s(4) <= open.end(4) → extend; open = [1, max(4,7)=7]
  flush final open: [1, 7]
Result:   [[1, 7]]
Expected: [[1, 7]]
OK

Input:    [[1, 10], [3, 5]]
Sorted:   [[1, 10], [3, 5]]
  init open = [1, 10]
  i=1 [3,5]: s(3) <= open.end(10) → extend; open = [1, max(10,5)=10]
  flush final open: [1, 10]
Result:   [[1, 10]]
Expected: [[1, 10]]
OK

Input:    [[1, 2], [3, 4], [5, 6]]
Sorted:   [[1, 2], [3, 4], [5, 6]]
  init open = [1, 2]
  i=1 [3,4]: s(3) >  open.end(2) → finalise [1, 2]; open = [3,4]
  i=2 [5,6]: s(5) >  open.end(4) → finalise [3, 4]; open = [5,6]
  flush final open: [5, 6]
Result:   [[1, 2], [3, 4], [5, 6]]
Expected: [[1, 2], [3, 4], [5, 6]]
OK
```
