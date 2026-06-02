# Two Sum II — Input Array Is Sorted — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `two-sum-ii-input-array-is-sorted`
- **LC #:** 167
- **Difficulty:** Medium
- **Topic:** Two Pointers
- **Archetype:** two_pointer (converging pointers on a sorted array; canonical golden lessons/3sum/lesson.html)

## 1. Clarifying questions (§0)
1. Is the input guaranteed sorted ascending? → Yes — unlocks the two-pointer squeeze.
2. Exactly one solution? → Yes; return on first match, no element reused.
3. Index base of the answer? → 1-indexed; return `[L+1, R+1]`.
4. Negatives / duplicates allowed? → Yes; the squeeze relies only on order.

## 2. Kernel paragraph (§1)
Because the array is sorted, the smallest possible sum is the two leftmost elements and the
largest is the two rightmost. Put a pointer at each end and read the sum. Too small ⇒ the only
way to grow it is to drop the smallest element (L++); too big ⇒ drop the largest (R--). Each move
strictly tightens the window toward the target and discards an element that can never be part of
the answer, so one inward sweep either hits the target or proves no pair exists — O(n), O(1) space.

## 3. Foundational concept visual (§1)
Animated number strip on `[2,7,11,15], target 9` with an info-coloured `L` and warn-coloured `R`
converging; discarded cells dim, the matched pair turns success-green. Reader controls drive
`siGenSteps`. Plus a 4-row chain-box: problem ≡ fix R and seek its partner ≡ compare end-sum and
move the helpful pointer ≡ each discarded element is provably impossible.

## 4. Translations (§3)
1. Replace the inner loop with a hash map: O(n²) → O(n) time, O(n) space (generic Two Sum).
2. Exploit the sort with converging two pointers: O(n) space → O(1).
3. Return on first match (single-solution guarantee): early exit.

## 5. Algorithm in plain English (§4)
1. Place `L` at index 0, `R` at index n−1.
2. While `L < R`, compute `numbers[L] + numbers[R]`.
3. If it equals target, return `[L+1, R+1]`.
4. If too small, advance `L`.
5. If too large, retreat `R`.
6. Stop when pointers meet (a match is guaranteed first).

## 6. Examples for code viz + dry run (§6, §7)
| numbers | target | answer | role |
|---|---|---|---|
| `[2,7,11,15]` | 9 | `[1,2]` | medium |
| `[1,2,3,4,4,9,56,90]` | 8 | `[4,5]` | slow (long squeeze, duplicates) |
| `[-3,3,4]` | 0 | `[1,2]` | corner (negatives, fast) |

`drGenSteps(numbers, target)` is the correctness oracle; its terminal step carries `result` = the
1-indexed pair, checked against `EX[].answer` by `scripts/verify_animation.mjs`.

## 7. Corner cases (§8)
- Match on the first check (`[1,2], t=3`).
- Negative numbers (`[-3,3,4], t=0`).
- Duplicate values forming the pair (`[…,4,4,…], t=8`).
- 1-indexed output (the `+1` bug).
- Two-element array.

## 8. Approaches comparison (§10)
- Two pointers — O(n) / O(1); the answer for sorted input.
- Hash map — O(n) / O(n); generic, works unsorted, wastes space here.
- Binary search per element — O(n log n) / O(1); uses the sort only halfway.

## 9. Take home (§12)
- LC 1 Two Sum — unsorted; hash map is the right tool.
- LC 15 3Sum — fix one element, then this squeeze.
- LC 11 Container With Most Water — same converging pointers, different move rule.
- LC 18 4Sum — two fixes wrapping the squeeze.

## 10. Python verification (BEFORE writing HTML)
```
twoSum([2,7,11,15], 9)            -> [1, 2]   ✓
twoSum([1,2,3,4,4,9,56,90], 8)    -> [4, 5]   ✓
twoSum([-3,3,4], 0)               -> [1, 2]   ✓
```
