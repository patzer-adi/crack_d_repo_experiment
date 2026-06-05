# Lesson plan — Subsets (LC 78)

## Metadata

- **Slug:** subsets
- **LC #:** 78
- **Difficulty:** Medium
- **Topic:** Backtracking
- **Archetype:** custom (combinatorial enumeration / backtracking decision tree — no
  match in the four-archetype table, which is array/grid-shaped; this is the escape-hatch
  case, so the step generators are written from scratch. It is the *first* backtracking
  lesson in the ramp, so the teaching object is the include/skip decision tree itself.)
- **Twist (from problems.json):** "primer: at each index, branch on (include, skip)" —
  every element is one independent yes/no choice, so the n choices form a binary decision
  tree with 2ⁿ leaves, one per subset. This is the canonical backtracking primer.

## 1. Clarifying questions

1. **Are the elements distinct?** Yes (LC 78 guarantees unique integers), so no subset is
   produced twice and we never need a de-dup guard. → the include/skip tree has no repeated
   leaves; the duplicate case is its own problem (Subsets II, LC 90).
2. **Does the empty set count, and the full set?** Yes — both are valid subsets. The empty
   set is the "skip everything" path; the full set is the "include everything" path. →
   the recursion must record a subset at *every* leaf, including the all-skip leaf.
3. **Does output order matter?** No — LeetCode accepts the 2ⁿ subsets in any order. → we are
   free to pick the order the recursion naturally emits (here: skip-branch first, so ∅ comes
   out first and the full set last). The lesson fixes one order so the animation, the oracle,
   and the independent reference can be compared exactly.
4. **How big can n get?** Up to ~20 (output is 2ⁿ). → any correct method is Θ(n·2ⁿ) because
   the *output itself* is that large; there is no sub-exponential approach to chase. The win
   is conceptual clarity, not asymptotics.

## 2. The insight (foundational concept)

A subset is not something to "find" — it is one **yes/no answer per element**: keep it, or
leave it out. With n elements that is n independent binary choices, so there are exactly
2ⁿ distinct answer-patterns, and each pattern is one subset. Lay the choices out one element
at a time and you get a binary decision tree: at depth i you branch on element i (skip ⟶
left, include ⟶ right); each of the 2ⁿ root-to-leaf paths spells out exactly one subset,
each appearing once. Walk the tree depth-first and you enumerate every subset with no
misses and no repeats. Backtracking = one shared `path`, push before the include branch and
pop after, so a single array is reused across all 2ⁿ paths.

## 3. Translations

1. Membership bitmask (number subsets 0..2ⁿ−1) → **recursive include/skip**. Same 2ⁿ work,
   but the recursion expresses the choice tree directly and extends to pruning and to the
   duplicate / constrained variants where a flat bitmask loop cannot.
2. Rebuild each subset from scratch → **one shared `path` with undo**. Push `nums[i]` before
   the include branch, pop it after — the array is mutated in place and only copied when a
   leaf is reached. This push/recurse/pop trio *is* backtracking.
3. "Stop and collect" → **record at every leaf**. When `i == n` all elements are decided, so
   the current `path` is exactly one finished subset; copy it into the result once.

## 4. Algorithm (recursive backtracking, skip-first)

1. Keep a result list `res` and a reusable `path`.
2. `dfs(i)`: if `i == n`, every element is decided — push a copy of `path` into `res` and
   return (this is one leaf / one subset).
3. Otherwise branch twice on element `i`: first **skip** it — `dfs(i + 1)` with `path`
   unchanged.
4. Then **include** it — `path.push_back(nums[i])`, `dfs(i + 1)`, then `path.pop_back()` to
   undo before returning to the caller.
5. Call `dfs(0)`; when it returns, `res` holds all 2ⁿ subsets.

## 5. Examples (hand-derived two ways: skip-first DFS and the bitmask in verify.py)

The oracle decides index 0 first and tries **skip before include**, so element 0 is the most
significant choice: ∅ (skip all) comes out first and the full set last.

| # | nums | answer (skip-first DFS order) |
|---|------|-------------------------------|
| EX0 (LC ex1) | `[1,2,3]` | `[[],[3],[2],[2,3],[1],[1,3],[1,2],[1,2,3]]` |
| EX1 (LC ex2) | `[0]`     | `[[],[0]]` |
| EX2          | `[7,8]`   | `[[],[8],[7],[7,8]]` |

The independent reference `verify.py` enumerates an integer `mask` from 0 to 2ⁿ−1 and reads
element `i` from bit `n−1−i` (so element 0 is the leftmost / most-significant bit). That
counting order reproduces the same lists in the same order as the recursion — a different
mechanism (no recursion, no call stack), so the cross-check is not a tautology. Verified by
hand for all three examples.

## 6/7. Animation

- §1 insight (`siGenSteps`): the **doubling frontier** on `[1,2,3]`. Start with one partial
  (∅); for each element every partial forks into skip / include, so the count doubles
  1 → 2 → 4 → 8. The include-copies light up; the final 8 leaves are the subsets. Shows *why*
  there are 2ⁿ and what a subset *is* (a choice vector), in the same skip-first order.
- §2 brute force (`bfGenSteps`): the **bitmask enumeration** — number every subset 0..2ⁿ−1
  and decode the bits. A running bit-test counter (n per pattern → n·2ⁿ) makes the cost
  concrete; framed as correct-but-rigid versus the recursion.
- §6 code-viz (`cvGenSteps`): the recursive C++ walked line by line — the `if (i==n)` leaf,
  the skip branch, the include push, and the `pop_back` backtrack — with variable cards
  (n / i / path / branch / subset count) and the result list growing below.
- §7 dry run (`drGenSteps`): the oracle. Depth-first over the decision tree, emitting one
  subset per leaf in skip-first order; the terminal step carries `result` = the full power
  set (deep-compared to the EX answer). Edge inputs `[0]` and `[7,8]` are included.

## Complexity

- Time: O(n · 2ⁿ) — there are 2ⁿ subsets and copying each finished `path` into the result is
  O(n). The output size alone forces this bound.
- Space: O(n) auxiliary — recursion depth and the single shared `path`; the output itself is
  O(n · 2ⁿ) but is required, not auxiliary.
