# Move Zeroes — lesson plan

> **Workflow:** Fill this file first. The lesson HTML is generated only
> after this plan is reviewed (see PLAN-011 §4.8).

## Metadata
- **Slug:** `move-zeroes`
- **LC #:** 283
- **Difficulty:** Easy
- **Topic:** Two Pointers
- **Archetype:** two_pointer (stable read/write compaction; canonical golden lessons/3sum/lesson.html)

## 1. Clarifying questions (§0)
1. Must the relative order of non-zero elements be preserved? → Yes (stable) — rules out sorting.
2. In-place with O(1) space, or may we allocate? → In-place is the target; a copy is only a baseline.
3. What counts as a zero — only integer `0`? → Yes, the literal value 0; predicate is `!= 0`.
4. Can the array be empty or all zeros? → Yes; both valid, must not crash.

## 2. Kernel paragraph (§1)
Stop moving zeros; pull the non-zeros forward instead. Keep a `slow` write slot at the first
position that has not yet received a confirmed non-zero, and sweep a `fast` reader across the
array. Each time the reader hits a non-zero, swap it into `nums[slow]` and advance `slow`.
Visiting and placing both left-to-right preserves the non-zeros' order for free, and every slot
the write pointer leaves behind is a finished non-zero — so the zeros trail at the back with no
second pass.

## 3. Foundational concept visual (§1)
Animated number strip on `[0,1,0,3,12]`: a warn-coloured `w` (write slot) and an info-coloured
`r` (reader). Settled non-zeros in `[0, slow)` turn success-green. Reader controls (prev / auto /
next / reset) drive `siGenSteps`. Plus a 4-row chain-box reducing "move zeros back" ≡ "pull
non-zeros forward" ≡ "stream + copy to front" ≡ "swap so the displaced zero parks at the tail".

## 4. Translations (§3)
1. Reuse the front of the array as the output buffer (since `fast ≥ slow`): O(n) space → O(1).
2. Swap instead of overwrite + zero-fill: two passes → one pass.
3. Skip the no-op swap when `slow == fast`: fewer writes on zero-light inputs.

## 5. Algorithm in plain English (§4)
1. Set `slow = 0`.
2. Sweep `fast` from 0 to n−1.
3. If `nums[fast] == 0`, skip (leave `slow`).
4. Otherwise swap `nums[slow]` and `nums[fast]`, then advance `slow`.
5. End: `[0, slow)` is non-zeros in order, `[slow, n)` is zeros.

## 6. Examples for code viz + dry run (§6, §7)
| nums | answer | role |
|---|---|---|
| `[0,1,0,3,12]` | `[1,3,12,0,0]` | canonical / medium |
| `[4,0,5,0,0,3,0,8]` | `[4,5,3,8,0,0,0,0]` | slow (long, many swaps) |
| `[0,0,1]` | `[1,0,0]` | corner (leading zeros, fast) |

`drGenSteps` is the correctness oracle; its terminal step carries `result` = final array, checked
against `EX[].answer` by `scripts/verify_animation.mjs`.

## 7. Corner cases (§8)
- Empty array — loop never runs.
- All zeros — `slow` never moves; array untouched.
- No zeros — every step `slow == fast`; guard skips all swaps.
- Leading zeros — reader skips them; one swap pulls the first non-zero forward.
- Single element — at most one self-swap.

## 8. Approaches comparison (§10)
- Two-pointer swap — O(n) / O(1), one pass, stable. The interview answer.
- Overwrite + zero-fill — O(n) / O(1) but two passes, always writes every slot.
- Copy to new array — O(n) / O(n), easiest to reason about, violates in-place.

## 9. Take home (§12)
- LC 27 Remove Element — same compaction, predicate `!= val`.
- LC 26 Remove Duplicates from Sorted Array — advance write slot on change.
- LC 75 Sort Colors — three-way partition (Dutch flag).
- LC 905 Sort Array By Parity — partition by predicate, two pointers.

## 10. Python verification (BEFORE writing HTML)
```
moveZeroes([0,1,0,3,12])       -> [1, 3, 12, 0, 0]      ✓
moveZeroes([4,0,5,0,0,3,0,8])  -> [4, 5, 3, 8, 0, 0, 0, 0]  ✓
moveZeroes([0,0,1])            -> [1, 0, 0]             ✓
```
