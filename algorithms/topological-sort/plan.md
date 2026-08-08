# Algorithm Lesson Plan: Topological Sort

## Metadata

- **ID:** topological-sort
- **Category:** Graph Algorithms (category_order 2), ramp_pos 3
- **Kind:** algorithm
- **Tier:** 1 (primer)
- **Interview relevance:** high
- **Archetype:** custom (directed-graph ordering — visual-led §1; the in-degree
  countdown is the thing to see).
- **Question the lesson answers:** order the nodes of a directed graph so every edge
  points forward. Ties are broken by smallest node id, so the answer is unique.

## Complexity

- **Time:** O(V + E) with a plain queue; O(V log V + E) for the lexicographically
  smallest order, because the ready set becomes a min-heap.
- **Space:** O(V)
- **Notes:** Only defined on a DAG. A cycle means no ordering exists.

## Prerequisites

- `bfs` (Kahn's algorithm is BFS over the ready set)

## 1. Clarifying questions

1. **Is the graph directed?** Yes — an edge `u → v` means u must come first. → an
   undirected graph has no topological order at all.
2. **Can it contain a cycle?** Yes, and then there is no answer. → the algorithm must
   *detect* that, not loop forever or return a wrong order.
3. **Is the order unique?** Usually not. → we break ties by smallest id so the result
   is deterministic and testable.
4. **What is the output for a cycle?** An empty list. → callers can check `size() != n`.

## 2. The insight (foundational concept)

A node is safe to place the moment nothing is still waiting to come before it — that
is, when its in-degree reaches zero. Placing it removes its edges, which may drop a
successor's in-degree to zero and make that node safe too. So the order builds itself
by a countdown, and no lookahead is ever needed.

## 3. Translations

1. Search all orderings → count incoming edges. Factorial to linear.
2. Rescan every node for "is it ready?" → decrement successors when a node is placed.
   O(V²) → O(V + E).
3. Detect a cycle separately → compare the placed count to V. A cycle falls out for free:
   if fewer than V nodes were placed, the leftovers all point at each other.

## 4. Algorithm

1. Count each node's in-degree by walking the edge list once.
2. Put every node with in-degree 0 into the ready set.
3. Take the **smallest** ready node, append it to the order.
4. For each successor, decrement its in-degree; if it hits 0, add it to the ready set.
5. Repeat until the ready set empties. If the order holds all V nodes, return it;
   otherwise the graph has a cycle — return an empty list.

## 5. Examples (hand-derived, then cross-checked by verify.py)

| # | input | answer | derivation |
|---|-------|--------|------------|
| EX0 | n=6, edges=[[5,2],[5,0],[4,0],[4,1],[2,3],[3,1]] | `[4,5,0,2,3,1]` | ready {4,5} → take 4, then 5; that frees 0 and 2; take 0, then 2 → 3 → 1 |
| EX1 | n=3, edges=[[0,1],[1,2],[2,0]] | `[]` | every node has in-degree 1, so the ready set is empty from the start |
| EX2 | n=4, edges=[[0,1],[0,2],[1,3],[2,3]] | `[0,1,2,3]` | a diamond: 0, then the smaller of {1,2}, then the other, then 3 |

## 6/7. Animation

- **§1 `siGenSteps`** — the in-degree countdown on the EX0 graph.
- **§2 `bfGenSteps`** — repeated full rescan: each round scans every node to find one
  with no unplaced predecessor. O(V²) with a scan counter.
- **§6 `cvGenSteps`** — one step per executed C++ line.
- **§7 `drGenSteps` (the oracle)** — Kahn's algorithm with smallest-first tie-breaking;
  terminal step carries `result` = the order, or `[]` on a cycle.

## 8. Independence (PLAN-019 G4)

`verify.py` enumerates **permutations in lexicographic order** and returns the first
one that satisfies every edge. It never computes an in-degree, never removes an edge,
and has no notion of a ready set — it just tests orderings. Tractable only because the
examples are tiny, which is exactly what an independent reference is for.

## 9. Complexity derivation

The in-degree pass reads every edge once: O(V + E). Each node enters and leaves the
ready set exactly once, and each edge is decremented exactly once when its source is
placed, so the main loop is O(V + E) too. Using a min-heap for smallest-first adds a
log V factor per insert and extract, giving O(V log V + E). Space is the in-degree
array plus the ready set: O(V).

## Output file

`algorithms/topological-sort/lesson.html`
