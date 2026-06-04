# Lesson plan — Number of Islands (LC 200)

## Metadata

- **Slug:** number-of-islands
- **LC #:** 200
- **Difficulty:** Medium
- **Topic:** Graphs — BFS / DFS
- **Archetype:** custom (grid connected-components — no canonical match; adapts the same
  "densely-annotated animated grid" teaching structure used by 01-matrix and
  rotting-oranges, since the insight is a scan + flood-fill that one animated diagram
  makes obvious, with no chain-box required).
- **Twist (from problems.json):** primer — grid DFS to mark connected components.

## 1. Clarifying questions

1. **What counts as "adjacent" — diagonals too?** Only the four orthogonal neighbours
   (up/down/left/right). Diagonal touches do NOT connect. → unlocks a 4-direction helper.
2. **May I mutate the input grid?** Usually yes; sinking each visited land cell to `'0'`
   is the cleanest "visited" marker. If mutation is banned, keep a separate `visited`
   matrix. → sink in place, or a parallel visited grid.
3. **Can the grid be empty, and how big can it get?** It may have 0 rows (→ 0 islands);
   otherwise up to ~300×300. → guard `grid.empty()`, a single linear pass is plenty.
4. **What are the cell values — chars or ints?** LeetCode passes `'1'`/`'0'` as `char`s.
   → compare against the character `'1'`, not the integer `1`.

## 2. The insight (foundational concept)

Standing on a land cell and re-exploring outward to identify "its" island re-counts the
same island from every one of its cells. Flip the bookkeeping: sweep the grid in
row-major order, and the **first** time you step onto land that no earlier flood has
claimed, it must be a brand-new island. Add one to the counter, then flood-fill that
island's whole body (sink every connected land cell to water) so every later step in the
sweep walks straight over it. The number of islands is simply the number of times the
sweep had to *start* a fresh flood.

## 3. Translations

1. "Which island does this cell belong to?" → "Is this the first cell of a new island?"
   Decide membership by sink-on-visit, not by re-search. Drops the per-cell re-exploration.
2. Re-walking claimed land → sink visited land to `'0'` (or mark `visited`); each cell is
   touched a constant number of times. O((mn)²) → O(mn).
3. "Count distinct components" → "count the number of flood *starts*." A component is
   discovered exactly once, at its first scan-order cell.

## 4. Algorithm (iterative DFS flood-fill, one function)

1. Walk every cell in row-major order.
2. Skip water (`'0'`) and already-sunk land.
3. On unclaimed land: `count++` (a new island), push the cell on a stack and sink it.
4. While the stack is non-empty, pop a cell and, for each orthogonal land neighbour, sink
   it and push it — this drains the whole connected island.
5. When the sweep ends, `count` is the number of islands. Return it.

(Iterative stack DFS is shown so the §6 visualization maps line-by-line and there is no
recursion-depth risk on a giant island; recursive DFS, BFS, and union-find are in §10.)

## 5. Examples (answers hand-derived by scan + flood; cross-checked in verify.py)

| # | grid | islands |
|---|------|---------|
| EX0 two islands 3×3 | `[[1,1,0],[0,0,0],[0,1,1]]` | **2** — {(0,0),(0,1)} and {(2,1),(2,2)} |
| EX1 diagonals don't connect 3×3 | `[[1,0,1],[0,1,0],[1,0,1]]` | **5** — every 1 is orthogonally isolated |
| EX2 LC-style 4×5 | `[[1,1,0,0,0],[1,1,0,0,0],[0,0,1,0,0],[0,0,0,1,1]]` | **3** — 2×2 block, lone centre, bottom-right pair |

The independent reference `verify.py` uses a **different algorithm** — iterative
label-min propagation (give every land cell a unique id, let orthogonal neighbours
repeatedly copy the smallest id until stable, then count distinct ids). No queue, no
flood; a genuinely separate route to the same counts, so the cross-check is not a
tautology. It reproduces 2 / 5 / 3.

## 6/7. Animation

- §1 insight (`siGenSteps`): scan + flood on a 3×4 grid (`[[1,1,0,1],[0,0,0,1],[1,0,1,1]]`,
  3 islands), one step per discovery — the scan cursor lands on fresh land, the whole
  island floods blue then settles green with its island number; claimed land is never
  recounted.
- §2 brute force (`bfGenSteps`): label-min propagation with cumulative "sweeps" and
  "cell-updates" counters, to feel the O((mn)²) cost of re-scanning the grid until labels
  stabilise (worst case = a snake-shaped island whose diameter ≈ mn).
- §6 code-viz (`cvGenSteps`): the iterative stack-DFS walked against the displayed C++ line
  by line, with variable cards (m / n / count / island size / cells sunk).
- §7 dry run (`drGenSteps`): the oracle. One step per island on all three EX grids; the
  terminal step carries `result` = the integer island count (deep-compared to EX answer).

## Complexity

- Time: O(m·n) — every cell is visited a constant number of times.
- Space: O(m·n) — the explicit stack (or visited marking) in the worst case of one big
  island.
