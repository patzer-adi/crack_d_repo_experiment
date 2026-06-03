# Lesson Plan: Binary Search (LC #704)

## Metadata
- **Slug:** `binary-search`
- **LC #:** 704
- **Difficulty:** Easy
- **Topic:** Binary Search
- **Tier:** 1 (primer)
- **Twist:** half-the-range invariant
- **Archetype:** binary_search (classic closed-interval)

---

## §1 — The Concept

### Plain-English explanation
Imagine you're looking up a word in a dictionary. You don't start from page 1 —
you open the book in the middle. If your word comes before the middle word,
you ignore the right half. If it comes after, you ignore the left half. You
repeat this on the surviving half until you find the word or run out of pages.
Binary search is exactly that: repeatedly cut the remaining search space in half
by comparing the middle element to the target.

### Key insight (one sentence)
Because the array is **sorted**, a single comparison with the middle element
lets you permanently eliminate half the remaining candidates.

### Concept visual description
A sorted array `[-5, -3, 0, 4, 7, 9, 12]` with coloured markers:
- `lo = 0` (blue, left edge)
- `hi = 6` (blue, right edge)
- `mid = 3` (amber, computed midpoint)
- `target = 7` shown above the strip
- After comparison `nums[mid]=4 < 7`: left half (indices 0–3) fades to grey;
  `lo` jumps to `mid+1=4`. The surviving half `[7, 9, 12]` stays bright.

### Kernel (infobox text)
Maintain the invariant that the target, if it exists, is always within
`[lo, hi]`. At each step, compute `mid = lo + (hi−lo)/2`. If `nums[mid] ==
target`, return `mid`. If `nums[mid] < target`, the target must be in the right
half — set `lo = mid + 1`. If `nums[mid] > target`, set `hi = mid - 1`. When
`lo > hi`, the target is not in the array. Each step halves the range, so the
loop runs at most ⌈log₂ n⌉ times.

---

## §2 — Data Structure Visual

### Primary DS
Sorted array with `lo`, `hi`, `mid` index markers.

### Invariants to show
- The array is **never modified** — binary search is purely a read operation.
- `lo ≤ hi` is the loop condition; when it breaks, the target is absent.
- `mid` is always **inside** `[lo, hi]`: `lo + (hi − lo) / 2` (integer division).
- After each step, the surviving range is exactly half the previous one.

### Visual layout
A horizontal strip of cells. Above each cell: its index (0-based).
- `lo` arrow below left boundary cell, blue
- `hi` arrow below right boundary cell, blue
- `mid` arrow below middle cell, amber
- Eliminated cells: grey background
- Current surviving range: default (bright) background
- Match cell: green background

---

## §3 — Algorithm in Plain English

1. **Initialise** `lo = 0` and `hi = n − 1` (the full array).
2. **Loop** while `lo ≤ hi`:
3. **Compute** `mid = lo + (hi − lo) / 2` (avoids integer overflow).
4. **Compare** `nums[mid]` to `target`:
   - If equal → **return** `mid`.
   - If `nums[mid] < target` → **set** `lo = mid + 1` (eliminate left half).
   - If `nums[mid] > target` → **set** `hi = mid - 1` (eliminate right half).
5. **Return** `−1` (target not found).

---

## §4 — Interactive Animation

### Preset examples

| # | Input | Target | Expected | Teaches |
|---|-------|--------|----------|---------|
| 1 | `[-1, 0, 3, 5, 9, 12]` | `9` | `4` | typical — found after 2 comparisons |
| 2 | `[-1, 0, 3, 5, 9, 12]` | `2` | `-1` | not found — lo crosses hi |
| 3 | `[1]` | `1` | `0` | single-element array — match on first step |

### Custom input spec
Two fields:
- **Array:** comma-separated integers (must be sorted — show warning if not)
- **Target:** single integer
Validation: parse as integers, verify sorted order, non-empty.

### Visual conventions

| Colour | Used for |
|--------|----------|
| Blue (info)     | `lo` and `hi` boundary cells + range highlight |
| Amber (warn)    | `mid` cell |
| Green (success) | matched cell |
| Red (danger)    | eliminated half (brief red flash before greying out) |
| Grey            | eliminated / out-of-range cells |

### Step narration examples

- Step 3: `mid = 2`, `nums[2] = 3`. Target is `9`. Since `3 < 9`, move `lo` to `mid+1 = 3`. Left half eliminated.
- Step 5: `mid = 4`, `nums[4] = 9`. Target is `9`. Match found — return index 4.
- Step 4 (not-found path): `lo = 4 > hi = 3`. Search space exhausted — target `2` is absent. Return −1.

### Formula row fields
`lo`, `hi`, `mid`, `nums[mid]`, `target`, `decision` (too small / too large / match)

---

## §5 — Code (C++ only)

### Algorithm to implement
Iterative binary search, closed interval `[lo, hi]`, `lo <= hi` loop condition.
Use `mid = lo + (hi - lo) / 2` to prevent overflow.

### Brute force
Linear scan: O(n) time, O(1) space. Checks every element in order.

### Complexity
- **Time:** O(log n) — range halves each iteration; at most ⌈log₂ n⌉ steps.
- **Space:** O(1) — only `lo`, `hi`, `mid`, and `result` integer variables.

---

## §6 — Code Walkthrough

### Variable cards

| Variable | First visible at line | Card label |
|----------|-----------------------|------------|
| `n`      | `int n = nums.size()` | n |
| `lo`     | `int lo = 0`          | lo |
| `hi`     | `int hi = n - 1`      | hi |
| `mid`    | `int mid = lo + ...`  | mid |
| `nums[mid]` | same line as mid   | nums[mid] |

### Array strip colour scheme
- Cells with index in `[lo..hi]`: blue background (active range)
- Cell at `mid`: amber border + amber text
- Cell at result (match): green
- Cells outside `[lo..hi]` (eliminated): grey

### Red-flash elements
When `lo > hi` (not-found termination), flash the entire remaining range red for
one step, then grey the whole array. This makes "why −1 is returned" visceral.

---

## §7 — Complexity

| | Big-O | Justification |
|-|-------|---------------|
| **Time** | O(log n) | Each iteration halves the remaining range; worst case ⌈log₂ n⌉ iterations. |
| **Space** | O(1) | Three integer variables (lo, hi, mid) plus the output index. |

---

## Corner cases

| Case | Input | Target | Expected | Why tricky |
|------|-------|--------|----------|------------|
| Empty array | `[]` | any | -1 | `hi = -1 < lo = 0` immediately |
| Single match | `[5]` | `5` | 0 | loop fires once, match on first mid |
| Single no-match | `[5]` | `3` | -1 | loop fires once, then lo > hi |
| Target at lo | `[1,3,5,7,9]` | `1` | 0 | mid always moves right |
| Target at hi | `[1,3,5,7,9]` | `9` | 4 | mid always moves left |

---

## Python verification trace

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        print(f"  lo={lo} hi={hi} mid={mid} nums[mid]={nums[mid]}")
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Example 1: [-1,0,3,5,9,12], target=9 → expected 4
print(binary_search([-1,0,3,5,9,12], 9))
# lo=0 hi=5 mid=2 nums[mid]=3  → lo=3
# lo=3 hi=5 mid=4 nums[mid]=9  → match! return 4

# Example 2: [-1,0,3,5,9,12], target=2 → expected -1
print(binary_search([-1,0,3,5,9,12], 2))
# lo=0 hi=5 mid=2 nums[mid]=3  → hi=1
# lo=0 hi=1 mid=0 nums[mid]=-1 → lo=1
# lo=1 hi=1 mid=1 nums[mid]=0  → lo=2
# lo=2 > hi=1 → return -1

# Example 3: [1], target=1 → expected 0
print(binary_search([1], 1))
# lo=0 hi=0 mid=0 nums[mid]=1 → match! return 0
```

---

## Related problems

- LC 74 (Search a 2D Matrix) — same binary search, treat 2D as flat sorted array via index arithmetic
- LC 153 (Find Minimum in Rotated Sorted Array) — BS without a target value; compare to right end
- LC 33 (Search in Rotated Sorted Array) — decide which half is sorted, then check if target lies there
- LC 875 (Koko Eating Bananas) — BS on the answer space, not the array itself

---

## Output file
`lessons/binary-search/lesson.html` — self-contained, offline-capable, no CDN dependencies.

## Quality checklist
- [x] Python trace run and verified for all 3 examples + corner cases
- [ ] §4 animation has 3 presets + custom input field
- [ ] Keyboard shortcuts work (← → Space R)
- [ ] §6 all variable cards start dimmed
- [ ] Hard-reset fires on example switch in both §4 and §6
- [ ] Code uses explicit braces on every block
- [ ] No CDN links, no external fonts, no external scripts
- [ ] Complexity matches trace output
