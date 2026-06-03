# Algorithm Lesson Plan: Binary Search

## Metadata
- **ID:** binary-search
- **Inventory source:** `data/algorithms.json`
- **Category:** Foundational Algorithms (category_order 1)
- **Kind:** algorithm
- **Tier:** 1  (1=primer, 2=core, 3=advanced)
- **Interview relevance:** high
- **Lesson path:** `algorithms/binary-search/lesson.html`

## Complexity
- **Time:** O(log n)
- **Space:** O(1) iterative
- **Notes:** Requires the input to be sorted (or monotonic over the answer space).

## Prerequisites
- `linear-search`

## Key idea (short_note)
Halve the search range each step using a monotone predicate; foundation for 'binary search on the answer' problems.

## Related LC problems
- `binary-search`
- `search-a-2d-matrix`
- `find-minimum-in-rotated-sorted-array`
- `search-in-rotated-sorted-array`
- `find-peak-element`
- `time-based-key-value-store`
- `koko-eating-bananas`
- `capacity-to-ship-packages-within-d-days`
- `split-array-largest-sum`
- `median-of-two-sorted-arrays`

## References
- CLRS Ch 2.3
- https://en.wikipedia.org/wiki/Binary_search_algorithm

---

## Lesson outline

### Section 1: Explain The Algorithm In Plain English
Binary Search is the moment where sorted order starts paying rent. Instead of checking every value, we keep a live range of possible answers and use the middle value to decide which half cannot possibly contain the target.

Clarifying questions:
- Q: Is the array sorted?
  A: Yes, in non-decreasing order.
  unlocks: compare against the middle and discard half the range
- Q: What if the target is absent?
  A: Return -1.
  unlocks: loop while left <= right, otherwise exit and return -1

Kernel paragraph:
The invariant is simple: if the target exists, it is inside `[left, right]`. Each comparison at `mid` preserves that invariant while cutting the range roughly in half.

### Section 2: Visualize The Data Structure
Binary Search does not need a heap, queue, or stack. Its core structure is a shrinking interval: `left`, `right`, and the computed `mid`.

State:
- `left` index pointer (initially 0)
- `right` index pointer (initially n - 1)
- `mid` pointer (computed midpoint)
- `nums[mid]` (element being checked)

Invariant:
If the target is present in the array, it is guaranteed to be in the closed index range `[left, right]`.

Highlight rules:
- Blue (`var(--bg-info)`): current active search range.
- Cyan (`#cffafe`): the middle cell `mid` currently under inspection.
- Green (`var(--bg-success)`): the target element if found.
- Red (`var(--bg-danger)`): the half of the range being discarded.
- Grey (`opacity: 0.35`): eliminated/out-of-range cells.

### Section 3: Algorithm In Plain English
Linear scan checks elements one by one. Binary Search leverages sorting to inspect the midpoint and discard half the candidates at each step.

Named transformations:
- Linear scan -> Binary Search (gain: O(n) checks become O(log n) checks).

Steps:
1. Start with `left = 0` and `right = n - 1`.
2. While `left <= right`, compute `mid = left + (right - left) / 2`.
3. If `nums[mid] == target`, return `mid`.
4. If `nums[mid] < target`, move `left` to `mid + 1` (discard left half).
5. Otherwise, move `right` to `mid - 1` (discard right half).
6. If the range becomes empty (`left > right`), return `-1`.

### Section 4: Interactive Visualization
A responsive array visualizer with step control, preset selector, speed adjuster, and custom array/target input.

Controls:
- Play / pause: Toggle automatic transitions.
- Step forward: Advance trace index.
- Step backward: Decrement trace index.
- Reset: Hard-reset active example.
- Speed: Slow/Normal/Fast selection.
- Keyboard: Space (play/pause), ArrowLeft/ArrowRight (prev/next step), R (reset), 1/2/3 (load presets).
- Visible-section routing: Shortcuts route to either the concept visual or walkthrough depending on viewport visibility.

Built-in examples:
1. nums = `[1, 3, 5, 7, 9]`, target = `7`
2. nums = `[2, 4, 6, 8, 10, 12]`, target = `5`
3. nums = `[-10, -3, 0, 4, 4, 9, 12]`, target = `4`

Custom input:
- Format: comma-separated array of numbers, and target number.
- Limits: maximum array length of 14 for readability.
- Validation: numbers only, array must be sorted in non-decreasing order.

Trace frame fields:
- `line` (active C++ line index)
- `left` (current left boundary index)
- `right` (current right boundary index)
- `mid` (computed midpoint index, or null)
- `target` (sought value)
- `value` (nums[mid], or null)
- `result` (index or -1, or null if pending)
- `vars` (variables currently active/changing)
- `action` (plain-text description of current state change)
- `drop` (indices of cells being discarded, if any)
- `found` (index of match, if any)

### Section 5: C++ Code
The optimal iterative solution with explicit braces.

```cpp
int binarySearch(const vector<int>& nums, int target) {
    int left = 0;
    int right = static_cast<int>(nums.size()) - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (nums[mid] == target) {
            return mid;
        }

        if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}
```

### Section 6: Code Walkthrough
Step through the C++ code line by line with synchronized variable cards and array state.

Variable cards:
- `left` (first visible at line 2)
- `right` (first visible at line 3)
- `mid` (first visible at line 6)
- `nums[mid]` (first visible at line 8)
- `target` (always visible)

Line-to-visual mapping:
- Line 2: Initialize `left = 0`.
- Line 3: Initialize `right = nums.size() - 1`.
- Line 5: Loop check: is `left <= right`?
- Line 6: Calculate `mid = left + (right - left) / 2`.
- Line 8: Compare `nums[mid]` with `target`.
- Line 9: Match found, return `mid`.
- Line 12: Check if `nums[mid] < target`.
- Line 13: `left` updated to `mid + 1` (discard left).
- Line 15: `right` updated to `mid - 1` (discard right).
- Line 19: Range exhausted, return `-1`.

### Section 7: Time And Space Complexity
Derivations of complexity bounds.

Time: O(log n)
Every comparison halves the remaining search range. After k steps, the range is about n / 2^k. The search terminates when the range size is 0 or 1, requiring at most ⌈log₂ n⌉ steps.

Space: O(1)
The iterative version only stores indices `left`, `right`, and `mid` in local variables, utilizing a constant amount of extra memory.

Common misconception:
Binary Search only applies to sorted arrays. In reality, it works over any monotonic search space (such as a monotonic function or answer space) to find boundaries.

## Edge Cases
- Empty array: `left = 0`, `right = -1`. The loop `while (left <= right)` never executes, immediately returning `-1`.
- Single element match: `left = 0`, `right = 0`. `mid = 0`, matches target, returns 0.
- Single element no-match: `left = 0`, `right = 0`. `mid = 0`, doesn't match target, left/right adjusts such that `left > right`, returns -1.
- Target not found (larger than all): `left` index moves past the end, `left > right` triggers, returns -1.
- Target not found (smaller than all): `right` index moves below 0, `left > right` triggers, returns -1.

## Completion Checklist
- Lesson is based on the `data/algorithms.json` entry above.
- `lesson.html` uses the seven required sections.
- C++ code only.
- Three examples plus custom input.
- Keyboard controls work.
- Step backward works.
- Switching examples hard-resets all state.
- Trace is verified before HTML is marked generated.
