# Lesson plan — Pacific Atlantic Water Flow (LC 417)

## Metadata

- **Slug:** pacific-atlantic-water-flow
- **LC #:** 417
- **Difficulty:** Medium
- **Topic:** Graphs — BFS / DFS
- **Archetype:** custom (grid multi-source flood-fill — no canonical match; adapts the
  prefix_scan "densely-annotated visual" teaching structure, since the insight is a
  per-cell reachability property revealed by a flood, with no chain-box required).
- **Twist (from problems.json):** two reverse-flood sources (one per ocean); intersect
  the two reachable sets.

## 1. Clarifying questions

1. **Can water flow diagonally?** No — only up/down/left/right between orthogonal
   neighbours. → unlocks: a 4-direction neighbour helper, not 8.
2. **Does water flow on equal heights?** Yes — water flows to a neighbour of height
   ≤ current, so equal-height neighbours are connected both ways. → unlocks: the
   reverse-flood comparison must be `>=` (allow equal), not strict `>`.
3. **What touches each ocean?** Pacific = top row + left column; Atlantic = bottom row
   + right column. Corners touch both. → unlocks: the two seed sets for the floods.
4. **Output order / duplicates?** Any order, each cell once. → unlocks: a single pass
   over the grid collecting cells in both sets (we emit row-major).

## 2. The insight (foundational concept)

Forward-simulating where every cell's water drains is O((mn)²): a flood per cell.
Reverse the question. Stand on each ocean's shore and climb **uphill** (to neighbours
that are as tall or taller) — those are exactly the cells whose water can reach that
ocean. Two floods (one per ocean) give two reachable sets; their intersection is the
answer. O(mn) total.

## 3. Translations

1. Per-cell forward flood → reverse flood from the shore (drop the outer mn factor).
2. "Reaches an ocean" → membership in that ocean's reverse-reachable set.
3. Two booleans per cell → two visited grids `pac` / `atl`; answer = `pac && atl`.

## 4. Algorithm (BFS, iterative)

1. Seed a queue with every Pacific-border cell (top row + left col); same for Atlantic.
2. Flood each queue uphill: pop a cell, enqueue any unvisited neighbour with
   height ≥ the current cell's height.
3. Scan the grid; a cell is in the answer iff it is in both visited sets.

## 5. Examples (hand-derived via /tmp/paw.py independent reference)

| # | grid | answer (row-major) |
|---|------|--------------------|
| EX0 typical 3×3 | `[[1,2,2],[3,2,3],[2,4,1]]` | `[[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1]]` (excludes the two sink corners (0,0),(2,2)) |
| EX1 monotone 3×3 | `[[5,4,3],[4,3,2],[3,2,1]]` | `[[0,0],[0,1],[0,2],[1,0],[2,0]]` (the Pacific edge) |
| EX2 single-row 1×3 | `[[1,2,3]]` | `[[0,0],[0,1],[0,2]]` (row is both shores) |

Both the reverse-flood reference (`/tmp/paw.py`) and the forward brute-force reference
(`/tmp/paw_bf.py`) agree on all three, and the reverse reference reproduces the known
LC 5×5 sample answer `[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]`.

## 6/7. Animation

- §1 insight (`siGenSteps`): 6 milestone steps on EX0 — seed Pacific, flood, seed
  Atlantic, flood, intersect.
- §2 brute force (`bfGenSteps`): one forward flood per cell, with a "floods" counter to
  feel the O((mn)²) cost.
- §6 code-viz (`cvGenSteps`): iterative BFS walked against the displayed C++, line by
  line, with variable cards (phase / cell / pac / atl / both).
- §7 dry run (`drGenSteps`): the oracle. Per-pop frontier growth on all three EX grids;
  terminal step carries `result` = the row-major both-set.

## Complexity

- Time: O(m·n) — each cell enqueued at most once per ocean.
- Space: O(m·n) — two visited grids + queues.
