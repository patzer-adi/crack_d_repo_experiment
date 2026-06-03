# Lesson plan — 01 Matrix (LC 542)

## Metadata

- **Slug:** 01-matrix
- **LC #:** 542
- **Difficulty:** Medium
- **Topic:** Graphs — BFS / DFS
- **Archetype:** custom (grid multi-source BFS — no canonical match; adapts the same
  "densely-annotated visual" teaching structure used by rotting-oranges, since the
  insight is a synchronized distance wave over a grid that a single animated diagram
  makes obvious, with no chain-box required).
- **Twist (from problems.json):** multi-source BFS variant — every 0 is a source, and we
  write the distance to the nearest 0 out into each cell.

## 1. Clarifying questions

1. **How is distance measured — diagonal or orthogonal?** One step per orthogonal move;
   it is the grid shortest path, not Euclidean. → unlocks a 4-direction neighbour helper,
   +1 per hop.
2. **Is there always at least one 0?** Yes, guaranteed. → the BFS queue is never empty and
   there is no unreachable case.
3. **Search from each 1, or flood from the 0s?** Flood from every 0 at once; the first
   wave to touch a cell carries its answer. → unlocks multi-source BFS.
4. **Reuse the input grid for output?** Cleaner to allocate `dist` initialised to -1,
   which doubles as the visited marker. → dist == -1 means "not reached yet".

## 2. The insight (foundational concept)

Standing on each 1 and BFS-ing outward to its nearest 0 re-walks the grid once per cell —
O((mn)²). Reverse the framing: every 0 is a source. Seed a single BFS queue with **all**
zero-cells at distance 0, then let distance spread in synchronized rings. Because BFS
expands one ring at a time and all sources start together, the first time a cell is
reached is exactly its distance to the nearest 0 — one linear pass fills the whole matrix.

## 3. Translations

1. Search from each 1 → flood from every 0 (multi-source BFS). Drops the "which 1-cell"
   outer factor.
2. Re-walking settled cells → a `dist` matrix init to -1 that doubles as visited; each
   cell is stamped once. O((mn)²) → O(mn).
3. "Min over all sources" → first touch wins. BFS rings advance together, so the first
   arrival is the closest 0 — just check `dist == -1`, no comparison.

## 4. Algorithm (multi-source BFS, iterative)

1. Build `dist`: 0 for every 0-cell, -1 for every 1-cell.
2. Enqueue every 0-cell (the whole distance-0 frontier).
3. While the queue is non-empty: pop a cell, inspect its four orthogonal neighbours.
4. For each neighbour still at -1, set `dist = dist[cur] + 1` and enqueue; skip stamped
   neighbours (already reached by a closer 0).
5. When the queue drains, every cell holds its nearest-0 distance. Return `dist`.

## 5. Examples (hand-derived two ways: multi-source BFS and the two-pass DP in verify.py)

| # | mat | answer |
|---|-----|--------|
| EX0 single far source 3×3 | `[[0,1,1],[1,1,1],[1,1,1]]` | `[[0,1,2],[1,2,3],[2,3,4]]` (Manhattan from (0,0); deepest = 4) |
| EX1 two sources meet 3×3 | `[[0,1,1],[1,1,0],[1,1,1]]` | `[[0,1,1],[1,1,0],[2,2,1]]` (waves from (0,0) and (1,2) meet) |
| EX2 LC sample 3×3 | `[[0,0,0],[0,1,0],[1,1,1]]` | `[[0,0,0],[0,1,0],[1,2,1]]` (interior 1 + bottom row) |

The independent reference `verify.py` (textbook two-pass DP — no queue, separate from the
lesson's BFS oracle) reproduces all three, matching the LeetCode samples.

## 6/7. Animation

- §1 insight (`siGenSteps`): synchronized distance-wave BFS on a two-source 3×3
  (`[[0,1,1],[1,1,1],[1,1,0]]`), one step per ring; sources (green) flood the unknown
  (amber) cells, filling them (blue) with their distance, the just-reached ring ringed in
  info.
- §2 brute force (`bfGenSteps`): per-cell outward BFS with a cumulative "cell-scans"
  counter to feel the O((mn)²) cost of adjacent cells repeating each other's searches.
- §6 code-viz (`cvGenSteps`): multi-source BFS walked against the displayed C++ line by
  line, with variable cards (m / n / queue size / settled / max dist).
- §7 dry run (`drGenSteps`): the oracle. Per-ring growth on all three EX grids; terminal
  step carries `result` = the full distance matrix (deep-compared to the EX answer).

## Complexity

- Time: O(m·n) — each cell is enqueued at most once.
- Space: O(m·n) — the BFS queue in the worst case (e.g. an all-zero grid).
