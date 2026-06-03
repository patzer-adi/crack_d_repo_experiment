# Algorithm Lesson Plan: MergeSort

## Metadata
- **ID:** merge-sort
- **Inventory source:** `data/algorithms.json`
- **Category:** Foundational Algorithms (category_order 1)
- **Kind:** algorithm
- **Tier:** 2  (1=primer, 2=core, 3=advanced)
- **Interview relevance:** high
- **Lesson path:** `algorithms/merge-sort/plan.md`

## Complexity
- **Time:** O(n log n) all cases
- **Space:** O(n) auxiliary; O(log n) for linked-list variant
- **Notes:** Stable; the canonical divide-and-conquer sort and the foundation for external sorting.

## Prerequisites
- `insertion-sort`

## Section 1: Explain The Algorithm
Imagine you have a large stack of playing cards to sort. Instead of sorting the whole stack at once, you split the stack in half, hand each half to a friend to sort, and then merge their sorted halves back together in order. To merge, you compare the top card of each sorted pile, take the smaller card, and place it at the bottom of your new sorted pile. You repeat this until both piles are empty. MergeSort does exactly this: recursively divides the array in half until it reaches single-element subarrays (which are sorted by definition), and then merges them back together.

Clarifying questions:
- Q: Is MergeSort stable?
  A: Yes, it preserves the relative order of duplicate elements because when two elements are equal during merge, we pick the one from the left subarray.
  unlocks: stable sorting behavior
- Q: Can we sort in-place?
  A: Standard array MergeSort requires O(n) auxiliary space to hold temporary values during merge, otherwise elements would be overwritten.
  unlocks: need for O(n) temporary buffers

Kernel paragraph:
MergeSort is a divide-and-conquer algorithm. The base case is a subarray of size 0 or 1, which is trivially sorted. In the recursive step, divide the subarray into left and right halves around the midpoint, sort each half recursively, and merge the two sorted halves back together into a single sorted subarray.

## Section 2: Visualize The Data Structure
MergeSort divides the array into segments, effectively building a recursive tree structure of function calls. During the merge step, it uses an auxiliary temporary array to write elements in sorted order before copying them back.

State:
- `left` boundary index (start of active range)
- `right` boundary index (end of active range)
- `mid` index (split point)
- `i` (index pointer inside left temporary subarray)
- `j` (index pointer inside right temporary subarray)
- `k` (target index pointer in original array)

Invariant:
A single element subarray is always sorted. Merging two sorted subarrays of size p and q yields a sorted subarray of size p + q.

Highlight rules:
- Blue (`var(--bg-info)`): active subarrays being divided or merged.
- Cyan (`#cffafe`): elements currently compared during merge.
- Green (`var(--bg-success)`): elements successfully merged and copied back in sorted order.
- Grey (`opacity: 0.35`): indices outside the current recursion scope.

## Section 3: Algorithm In Plain English
Naive sorting algorithms (like Insertion Sort or Bubble Sort) grow sorted sections slowly, checking elements repeatedly. MergeSort splits the problem in half and zips sorted lists together in linear time.

Named transformations:
- Nested comparisons (O(n²) sort) -> Divide and conquer (O(n log n) sort).

Steps:
1. If the current range has size 0 or 1, it is already sorted — return it.
2. Find the midpoint: `mid = left + (right - left) / 2`.
3. Recursively call MergeSort on the left half: `mergeSort(nums, left, mid)`.
4. Recursively call MergeSort on the right half: `mergeSort(nums, mid + 1, right)`.
5. Merge the two sorted halves: compare elements from each side and write them sorted into an auxiliary buffer.
6. Copy the sorted buffer elements back into `nums[left...right]`.

## Section 4: Interactive Visualization
A responsive array split/merge visualizer with step control, preset selector, speed adjuster, and custom array input.

Controls:
- Play / pause: Toggle automatic transitions.
- Step forward: Advance trace index.
- Step backward: Decrement trace index.
- Reset: Hard-reset active example.
- Speed: Slow/Normal/Fast selection.
- Keyboard: Space (play/pause), ArrowLeft/ArrowRight (prev/next step), R (reset), 1/2/3 (load presets).
- Visible-section routing: Shortcuts route to either the concept visual or walkthrough depending on viewport visibility.

Built-in examples:
1. nums = `[5, 2, 4, 1, 3]`
2. nums = `[5, 4, 3, 2, 1]`
3. nums = `[2, 3, 2, 1, 3]`

Custom input:
- Format: comma-separated array of numbers.
- Limits: maximum array length of 10 for readability (recursion tree depth limit).
- Validation: numbers only, non-empty.

Trace frame fields:
- `line` (active C++ line index)
- `left` (left index boundary of current sort scope)
- `right` (right index boundary of current sort scope)
- `mid` (midpoint index, or null)
- `i` (left buffer index, or null)
- `j` (right buffer index, or null)
- `k` (nums index, or null)
- `array` (current state of array elements)
- `tempL` (elements inside temporary left buffer)
- `tempR` (elements inside temporary right buffer)
- `action` (plain-text description of current state change)

## Section 5: C++ Code
The recursive implementation with helper merge function.

```cpp
void merge(vector<int>& nums, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    vector<int> L(n1);
    vector<int> R(n2);

    for (int i = 0; i < n1; i++) {
        L[i] = nums[left + i];
    }
    for (int j = 0; j < n2; j++) {
        R[j] = nums[mid + 1 + j];
    }

    int i = 0;
    int j = 0;
    int k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            nums[k] = L[i];
            i++;
        } else {
            nums[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        nums[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        nums[k] = R[j];
        j++;
        k++;
    }
}

void mergeSort(vector<int>& nums, int left, int right) {
    if (left >= right) {
        return;
    }
    int mid = left + (right - left) / 2;
    mergeSort(nums, left, mid);
    mergeSort(nums, mid + 1, right);
    merge(nums, left, mid, right);
}
```

## Section 6: Code Walkthrough
Step through the C++ code line by line with synchronized variable cards and array state.

Variable cards:
- `left` (first visible at call)
- `right` (first visible at call)
- `mid` (first visible at split)
- `i` (first visible in merge loop)
- `j` (first visible in merge loop)
- `k` (first visible in merge loop)

Line-to-visual mapping:
- recursive split steps showing subdivision of active array indices.
- merge allocation and comparison steps showing copying to temporary buffers `L` and `R`, comparing, and writing back to `nums[k]`.

## Section 7: Complexity
Derivations of complexity bounds.

Time: O(n log n)
The recursion tree has a depth of log n. At each level of the tree, merging n elements across various segments takes O(n) time. The total runtime is O(n log n) in all cases (best, average, worst).

Space: O(n)
Requires an auxiliary array of size n to merge elements, alongside O(log n) recursion call stack depth.

Common misconception:
MergeSort always requires O(n) auxiliary space. For arrays, this is true. However, for linked lists, MergeSort can be implemented in O(1) auxiliary space (using only O(log n) call stack space) by re-linking nodes directly instead of allocating new elements.

## Edge Cases
- Empty array: `left = 0`, `right = -1`. The condition `left >= right` immediately returns.
- Single element: `left = 0`, `right = 0`. The condition `left >= right` returns immediately (already sorted).
- Array with all identical values: MergeSort performs all recursive splits and zips, stability ensures elements remain in their original positions.
- Reverse sorted array: Left and right buffers are compared; all elements in the right buffer are smaller than the left and get merged first.

## Completion Checklist
- Lesson is based on the `data/algorithms.json` entry above.
- `lesson.html` uses the seven required sections.
- C++ code only.
- Three examples plus custom input.
- Keyboard controls work.
- Step backward works.
- Switching examples hard-resets all state.
- Trace is verified before HTML is marked generated.
