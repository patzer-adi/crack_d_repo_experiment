# Algorithm Lesson Plan: A* Algorithm

## Metadata

- **ID:** a-star
- **Category:** Graph Algorithms (category_order 2), ramp_pos 6
- **Kind:** algorithm
- **Tier:** 2 (core)
- **Interview relevance:** medium
- **Archetype:** custom (informed search on a grid — visual-led §1; the thing to see
  is the *shape* of the explored region narrowing toward the goal).
- **Question the lesson answers:** fewest steps from start to goal on a grid with
  walls, expanding as few cells as possible.

## Complexity

- **Time:** O(E log V) worst case — the same as Dijkstra
- **Space:** O(V)
- **Notes:** The heuristic changes the constant, never the bound. With h = 0 it *is*
  Dijkstra.

## Prerequisites

- `dijkstras-algorithm` (A* is Dijkstra ordered by g + h instead of g)

## 1. Clarifying questions

1. **What does a move cost?** One step, in four directions. → g is just a step count.
2. **What heuristic is admissible here?** Manhattan distance. → with 4-way moves and
   unit cost it can never over-estimate, because every step changes the Manhattan
   distance by exactly 1.
3. **Is the goal always reachable?** No. → return -1 when the open set empties.
4. **Do we need the route or the length?** Length. → g at the goal; a parent map would
   rebuild the route.

## 2. The insight (foundational concept)

Dijkstra spreads out evenly in every direction because it only knows what a route has
already cost. A* adds a guess of what is still left, and orders the frontier by
`f = g + h`. As long as the guess never over-estimates, the first time the goal comes
off the queue its cost is still optimal — but the search has spent its effort in the
direction of the goal instead of behind it.

## 3. Translations

1. Order by cost-so-far (`g`) → order by `g + h`. Same guarantee, far fewer cells.
2. Re-expand improved cells → keep the best `g` per cell and skip stale queue entries.
3. Scan for the cheapest `f` → a min-heap.

## 4. Algorithm

1. `g[start] = 0`; push `(h(start), 0, start)` onto a min-heap ordered by `f`.
2. Pop the smallest `f`. If it is the goal, return its `g` — that is the answer.
3. If the popped `g` is worse than the stored `g`, it is a stale copy; discard it.
4. For each open neighbour, if `g + 1` improves it, store it and push
   `(g + 1 + h(v), g + 1, v)`.
5. If the heap empties, the goal is unreachable — return -1.

## 5. Examples (hand-derived, then cross-checked by verify.py)

| # | input | answer | derivation |
|---|-------|--------|------------|
| EX0 | 5×5 with two wall bands, (0,0) → (4,4) | `8` | the Manhattan distance is 8 and a monotone route exists through the gaps at column 2 and column 4 |
| EX1 | 3×3 with a full wall row, (0,0) → (2,2) | `-1` | row 1 is solid, so the goal is sealed off |
| EX2 | 3×3 with a wall column, (0,0) → (0,2) | `6` | Manhattan says 2, but the only route goes down, across and back up — the heuristic is optimistic, which is exactly what makes it admissible |

EX2 is the important one: it shows h under-estimating, and A* still returning the true
answer.

## 6/7. Animation

- **§1 `siGenSteps`** — A* expansion order on EX0, showing the explored region leaning
  toward the goal.
- **§2 `bfGenSteps`** — uninformed BFS on the same grid, with a cells-expanded counter
  to compare against A*.
- **§6 `cvGenSteps`** — one step per executed C++ line, including a stale-pop skip.
- **§7 `drGenSteps` (the oracle)** — A* itself; terminal step carries `result` = the
  step count, or -1.

## 8. Independence (PLAN-019 G4)

`verify.py` is **plain BFS** — no heap, no heuristic, no f-value. This is the sharpest
possible check for A*, because the classic A* bug is an inadmissible heuristic: one
that over-estimates makes A* return a *longer* path than the true shortest. BFS on a
unit-cost grid is exactly the true shortest, so any such bug shows up as a mismatch.

## 9. Complexity derivation

The heuristic changes which cells are expanded, not the worst-case bound: with an
adversarial grid A* still expands every cell, giving Dijkstra's O(E log V). Each cell
is pushed once per improvement, each push and pop costs O(log V), and each expansion
scans 4 neighbours. Space is one g-value per cell plus the heap: O(V). The win is
entirely in the constant — on EX0 A* expands noticeably fewer cells than BFS, and the
gap widens with grid size.

## Output file

`algorithms/a-star/lesson.html`
