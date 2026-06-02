# Lesson plan — Rotting Oranges (LC 994)

## Metadata

- **Slug:** rotting-oranges
- **LC #:** 994
- **Difficulty:** Medium
- **Topic:** Graphs — BFS / DFS
- **Archetype:** custom (grid multi-source BFS — no canonical match; adapts the
  prefix_scan "densely-annotated visual" teaching structure, since the insight is a
  synchronized wave over a grid that a single animated diagram makes obvious, with no
  chain-box required).
- **Twist (from problems.json):** primer for multi-source BFS — all rotten cells start
  in the queue together.

## 1. Clarifying questions

1. **Does rot spread diagonally?** No — only up/down/left/right. → unlocks a
   4-direction neighbour helper, not 8.
2. **Do all rotten oranges spread at the same time?** Yes, simultaneously each minute.
   → unlocks multi-source BFS: every rotten cell is a seed at minute 0.
3. **What if there are no fresh oranges to begin with?** Answer is 0 minutes. → unlocks
   an early return when fresh == 0.
4. **What if a fresh orange is walled off by empty cells?** It can never rot → return
   -1. → unlocks the leftover-fresh check after the BFS drains.

## 2. The insight (foundational concept)

Simulating one rotten orange at a time and rescanning the whole grid every minute is
O((mn)²). Reverse the framing: every rotten orange spreads at once. Seed a single BFS
queue with **all** rotten cells, then let the rot fan out in synchronized layers — one
layer = one minute. The number of layers is the answer; any fresh orange still standing
when the queue drains means -1.

## 3. Translations

1. Per-orange resimulation → one shared queue seeded with every rotten cell
   (multi-source). Drops the "which source" outer factor.
2. Rescan the whole grid each minute → process only the current frontier (level-order
   BFS). O((mn)²) → O(mn).
3. "Did anything change this round?" sentinel → a `fresh` counter. O(1) termination test,
   and the -1 case falls out (fresh > 0 at the end).

## 4. Algorithm (BFS, level-order, iterative)

1. Scan once: enqueue every rotten cell, count fresh.
2. If fresh == 0, return 0.
3. While the queue is non-empty and fresh remain: pop the whole current layer; for each
   cell rot its fresh orthogonal neighbours, decrement fresh, enqueue them.
4. After each full layer, minutes++.
5. When the queue drains, return minutes if fresh == 0 else -1.

## 5. Examples (hand-derived via /tmp/rot.py independent BFS reference)

| # | grid | answer |
|---|------|--------|
| EX0 typical 3×3 | `[[2,1,1],[1,1,0],[0,1,1]]` | `4` (wave: (0,0)→{(0,1),(1,0)}→{(0,2),(1,1)}→{(2,1)}→{(2,2)}) |
| EX1 impossible 3×3 | `[[2,1,1],[0,1,1],[1,0,1]]` | `-1` (the orange at (2,0) is sealed off by empties) |
| EX2 no-fresh 1×2 | `[[0,2]]` | `0` (nothing fresh to rot) |

The independent reference `/tmp/rot.py` (textbook timestamped BFS, separate from the
lesson's level-order oracle) reproduces all three, matching the known LC samples.

## 6/7. Animation

- §1 insight (`siGenSteps`): synchronized-wave BFS on EX0, one step per minute; the
  foundational visual is the grid with fresh (amber) / rotten (red) / just-rotted (info
  ring) cells fanning out.
- §2 brute force (`bfGenSteps`): repeated full-grid rescan per minute with a cumulative
  "cell-scans" counter to feel the O((mn)²) cost.
- §6 code-viz (`cvGenSteps`): level-order BFS walked against the displayed C++, line by
  line, with variable cards (m / n / fresh / minutes / queue size).
- §7 dry run (`drGenSteps`): the oracle. Per-minute wave growth on all three EX grids;
  terminal step carries `result` = minutes (or -1).

## Complexity

- Time: O(m·n) — each cell is enqueued at most once.
- Space: O(m·n) — the BFS queue in the worst case.
