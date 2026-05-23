# Binary Search — Skill File

## What it is
Repeatedly halve the search space by comparing a target to the middle element of a sorted range. Achieves O(log n) where a linear scan would be O(n). The key mental model: maintain an invariant — the answer (if it exists) always lies within `[lo, hi]`. Every frame eliminates the half that provably cannot contain the answer. Three variants:
- **Exact match:** return index when `nums[mid] == target`; return -1 if `lo > hi`.
- **Left boundary (first occurrence / insertion point):** keep searching left even after a match (`hi = mid - 1`); answer is `lo` at termination.
- **Right boundary (last occurrence):** keep searching right even after a match (`lo = mid + 1`); answer is `hi` at termination.

Applies beyond sorted arrays: any problem with a monotonic predicate (e.g. "is X a valid answer?") can be binary-searched on the answer space. Canonical problems: Binary Search, Search in Rotated Sorted Array, Find Minimum in Rotated Array, Koko Eating Bananas.

## Visual convention
Render the array using `skills/ds/array.md` conventions (boxes, index labels above).

- `lo` — left boundary: green cell (`--bg-success`), label `lo` in green below cell.
- `hi` — right boundary: amber cell (`--bg-warn`), label `hi` in amber below cell.
- `mid` — midpoint: blue cell (`--bg-info`), label `mid` in blue below cell. Computed as `lo + (hi - lo) / 2`.
- **Active range** (cells from `lo` to `hi` inclusive): full opacity.
- **Eliminated left half** (cells left of `lo`): `opacity: 0.25`, grey wash. Applied immediately after `lo` advances past them.
- **Eliminated right half** (cells right of `hi`): `opacity: 0.25`, grey wash.
- **Found cell:** green fill, green border. Shown in the final frame when `nums[mid] == target`.
- **Not-found state:** all cells at `opacity: 0.25` when `lo > hi`.
- For **rotated array** problems: show a subtle dividing line between the rotation point (the index where the array wraps) — a vertical dashed border between the two sorted halves.

## Animation rules

### Controls — required on every lesson
Every animated dry run must include four controls: ← Prev, ▶ Auto / ⏸ Pause, Next →, ↺ Reset.
Keyboard shortcuts: ← → for prev/next, Space for auto/pause, R or Esc for reset.
See `skills/patterns/two_pointers.md` for the keyboard listener snippet.

### Stable panel layout
Wrap formula-panel and step-panel in `.panels-fixed` grid (see `skills/patterns/two_pointers.md`).

### Formula panel — required
Show every frame:
```
lo = A    hi = B    mid = lo + (hi − lo) / 2 = A + (B − A) / 2 = C
nums[mid] = V    target = T
```
All arithmetic fully substituted. Never show `mid = 3` without tracing it to `lo + (hi - lo) / 2 = 0 + (6 - 0) / 2 = 3`.

### Step panel — structured reasoning
1. **What:** the comparison result (`nums[mid]=7 < target=9`).
2. **Why:** which half is eliminated and why (`left half cannot contain target → lo = mid + 1`).

### Frame sequencing
- **Frame 0:** full array at full opacity, `lo = 0`, `hi = n - 1`, `mid` computed and highlighted. Caption describes target and invariant.
- **Each iteration frame:** compute mid → compare → highlight eliminated half at `opacity: 0.25` → show new `lo` or `hi` → recompute mid.
- **Found frame:** `nums[mid] == target` → green cell, "Found at index C" caption.
- **Not-found frame:** `lo > hi` → all cells grey → "Target not found" caption.
- One decision per frame. Never combine the comparison and the pointer update in the same frame.

## Algorithmic template (C++)

Exact match:
```cpp
int search(vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;          // avoids overflow vs (lo+hi)/2
        if      (nums[mid] == target) return mid;
        else if (nums[mid] <  target) lo = mid + 1;
        else                          hi = mid - 1;
    }
    return -1;
}
```

Left boundary (first true position of a predicate):
```cpp
int lowerBound(vector<int>& nums, int target) {
    int lo = 0, hi = (int)nums.size();          // hi = n (open right boundary)
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < target) lo = mid + 1;
        else                    hi = mid;        // keep mid in range; answer may be mid
    }
    return lo;                                   // lo == hi at termination
}
```

Binary search on answer space (Koko Eating Bananas pattern):
```cpp
int minEatingSpeed(vector<int>& piles, int h) {
    int lo = 1, hi = *max_element(piles.begin(), piles.end());
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        long long hours = 0;
        for (int p : piles) hours += (p + mid - 1) / mid;   // ceil(p / mid)
        if (hours <= h) hi = mid;       // mid is feasible; try smaller
        else            lo = mid + 1;   // mid too slow; need faster
    }
    return lo;
}
```

## Common pitfalls
- Using `(lo + hi) / 2` instead of `lo + (hi - lo) / 2` — the former overflows for large indices; always use the latter. Show this in the formula panel.
- Off-by-one on `hi` initialisation: `hi = n` (open) vs `hi = n - 1` (closed) changes the loop condition and the termination state. Be explicit in the formula panel about which variant is in use.
- Moving both `lo` and `hi` in the same frame — one pointer update per frame; the greyed half must be shown before the new mid is computed.
- Not greying out the eliminated half immediately — the "half elimination" is the core visual; delaying it hides the algorithm's key property.
- Forgetting to show the `mid` recomputation after each pointer update — `mid` changes every iteration; the formula panel must reflect the new value.
- For boundary-search variants: not explaining why the code continues past a match — show explicitly "we found target but keep searching left/right for the boundary".
- For answer-space binary search: not showing the feasibility predicate evaluation as a formula — e.g. show `hours = sum(ceil(p / mid))` for each pile in the formula panel.
