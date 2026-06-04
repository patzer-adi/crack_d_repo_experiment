# Lesson plan — As Far from Land as Possible (LC 1162)

## Metadata

- **Slug:** as-far-from-land-as-possible
- **LC #:** 1162
- **Difficulty:** Medium
- **Topic:** Graphs — BFS / DFS
- **Archetype:** custom (grid multi-source BFS for the *max-min* — no canonical match;
  adapts the same "densely-annotated visual" teaching structure used by 01-matrix /
  rotting-oranges, since the insight is a synchronized distance flood over a grid that a
  single animated diagram makes obvious, with no chain-box required).
- **Twist (from problems.json):** multi-source BFS for the *max-min* (farthest water
  cell) — flood from every land cell, and the answer is the deepest wave (the last water
  cell reached), not a per-cell distance matrix.

## 1. Clarifying questions

1. **How is distance measured — diagonal or orthogonal?** One step per orthogonal move;
   it is the grid (Manhattan) shortest path, not Euclidean. → a 4-direction neighbour
   helper, +1 per hop.
2. **Do we return the cell or the distance?** Just the distance — the single maximum. →
   track one running max; no coordinates need to be remembered.
3. **What if the grid is all land, or all water?** Return -1: with no water there is no
   cell to measure, and with no land there is nothing to measure to. → guard for an empty
   queue or a full queue before flooding.
4. **Search outward from each water cell, or flood from all land at once?** Flood from
   every land cell. The first wave to reach a water cell is its distance to land, and the
   *last* water cell reached is the most isolated. → multi-source BFS seeded with every 1.

## 2. The insight (foundational concept)

Standing on each water cell and BFS-ing outward to its nearest land re-walks the grid once
per cell — O((n²)²). Reverse the framing: every land cell is a source. Seed a single BFS
queue with **all** land-cells at distance 0, then let distance spread in synchronized
rings. Because BFS expands one ring at a time and all sources start together, the first
time a water cell is reached is exactly its distance to the nearest land. The deepest wave
— the last water cell the flood reaches — is the answer. One linear pass.

## 3. Translations

1. Search from each water cell → flood from every land cell (multi-source BFS). Drops the
   "which water cell" outer factor.
2. Re-walking settled cells → a `dist` matrix init to -1 that doubles as visited; each
   cell is stamped once. O((n²)²) → O(n²).
3. "Max over per-cell searches" → the answer is just the deepest wave; keep one running
   max as cells are stamped (or read it off as the last non-empty wave number).

## 4. Algorithm (multi-source BFS, iterative)

1. Build `dist`: 0 for every land-cell, -1 for every water-cell.
2. Enqueue every land-cell (the whole distance-0 frontier).
3. If the queue is empty (no land) or holds every cell (no water), return -1.
4. While the queue is non-empty: pop a cell, inspect its four orthogonal neighbours. For
   each neighbour still at -1, set `dist = dist[cur] + 1`, update `ans = max(ans, dist)`,
   and enqueue; skip stamped neighbours.
5. When the queue drains, `ans` holds the largest distance any water cell reached. Return
   it.

## 5. Examples (hand-derived two ways: multi-source BFS and the two-pass DP in verify.py)

| # | grid | answer |
|---|------|--------|
| EX0 four corners 3×3 (LC ex1) | `[[1,0,1],[0,0,0],[1,0,1]]` | `2` (center (1,1) is wave 2; edge-mids wave 1) |
| EX1 single corner 3×3 (LC ex2) | `[[1,0,0],[0,0,0],[0,0,0]]` | `4` (deepest = opposite corner (2,2), Manhattan 4) |
| EX2 top-edge land 3×3 | `[[0,1,0],[0,0,0],[0,0,0]]` | `3` (deepest = (2,0)/(2,2), Manhattan 3) |

The independent reference `verify.py` (textbook two-pass DP distance transform — no queue,
separate from the lesson's BFS oracle) reproduces all three, matching the LeetCode samples.

## 6/7. Animation

- §1 insight (`siGenSteps`): synchronized distance flood on a two-source 3×3
  (`[[1,0,0],[0,0,0],[0,0,1]]`), one step per ring; land (green) floods the water (amber),
  filling each cell (blue) with its distance, the just-reached ring ringed in info, and
  the final farthest ring ringed in success.
- §2 brute force (`bfGenSteps`): per-water-cell outward BFS with a cumulative "cell-scans"
  counter and a running farthest, to feel the O((n²)²) cost of adjacent cells repeating
  each other's searches.
- §6 code-viz (`cvGenSteps`): multi-source BFS walked against the displayed C++ line by
  line, with variable cards (n / queue size / reached / sea left / ans).
- §7 dry run (`drGenSteps`): the oracle. Per-ring growth on all three EX grids; terminal
  step carries `result` = the integer answer (deep-compared to the EX answer). Degenerate
  all-land / all-water inputs would carry `result` = -1.

## Complexity

- Time: O(n²) — each cell is enqueued at most once.
- Space: O(n²) — the BFS queue in the worst case (e.g. an all-land grid).
