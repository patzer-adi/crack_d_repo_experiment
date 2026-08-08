# Algorithm Lesson Plan: Dijkstra's Algorithm

## Metadata

- **ID:** dijkstras-algorithm
- **Category:** Graph Algorithms (category_order 2), ramp_pos 4
- **Kind:** algorithm
- **Tier:** 1 (primer)
- **Interview relevance:** high
- **Archetype:** custom (weighted-graph shortest path — visual-led §1; the thing to
  see is that the cheapest frontier node is already final).
- **Question the lesson answers:** given a weighted graph with non-negative weights
  and a source, what is the cheapest total weight to reach every node?

## Complexity

- **Time:** O((V + E) log V) with a binary heap
- **Space:** O(V)
- **Notes:** Requires non-negative weights. One negative edge breaks the greedy claim.

## Prerequisites

- `bfs` (Dijkstra is BFS where the queue is ordered by cost, not by arrival)
- `heap` / priority queue

## 1. Clarifying questions

1. **Can a weight be negative?** No. → this is the precondition the whole algorithm
   rests on; a negative edge means Bellman-Ford.
2. **Directed or undirected?** Undirected here. → each edge relaxes both ways.
3. **Is every node reachable?** No. → unreachable nodes stay at infinity and report -1.
4. **Do we need the path or only the cost?** Cost. → one `dist` array; add `parent[]`
   to rebuild the route.

## 2. The insight (foundational concept)

BFS works because every edge costs the same, so arrival order is cost order. With
weights that breaks — a two-edge route can be cheaper than a one-edge route. Dijkstra
restores it by always taking the *cheapest* unsettled node instead of the earliest.
Since no edge can reduce a total, nothing reachable later can undercut the cheapest
thing on the frontier, so its distance is already final.

## 3. Translations

1. Try every route → keep one best-known distance per node. Factorial to polynomial.
2. Scan all nodes for the cheapest unsettled one → keep them in a min-heap.
   O(V²) → O((V + E) log V).
3. Delete-and-reinsert on improvement → push a duplicate and skip stale pops
   (`d > dist[u]`). Cheaper than a decrease-key and just as correct.

## 4. Algorithm

1. Set every distance to infinity, `dist[src] = 0`, push `(0, src)`.
2. Pop the smallest `(d, u)`. If `d > dist[u]` it is a stale copy — discard it.
3. Otherwise `u` is settled: `dist[u]` is final.
4. For each edge `(u, v, w)`, if `dist[u] + w < dist[v]`, improve `dist[v]` and push
   `(dist[v], v)`.
5. Repeat until the heap empties. Report -1 for anything still at infinity.

## 5. Examples (hand-derived, then cross-checked by verify.py)

| # | input | answer | derivation |
|---|-------|--------|------------|
| EX0 | n=5, edges=[[0,1,4],[0,2,1],[2,1,2],[1,3,1],[2,3,5],[3,4,3]], src=0 | `[0,3,1,4,7]` | node 1 via 2 costs 1+2=3, beating the direct edge of 4 |
| EX1 | n=4, edges=[[0,1,2],[1,2,3]], src=0 | `[0,2,5,-1]` | node 3 has no edges at all |
| EX2 | n=4, edges=[[0,1,10],[0,2,3],[2,1,4],[1,3,2],[2,3,20]], src=0 | `[0,7,3,9]` | the two-hop route to 1 costs 7 against a direct 10; 3 is then 7+2=9, not 3+20 |

Every example is chosen so the direct edge is *not* the answer — that is the whole
point of weights.

## 6/7. Animation

- **§1 `siGenSteps`** — the settle order on EX0, showing the cheapest frontier node
  being finalised each round.
- **§2 `bfGenSteps`** — enumerate every simple route and keep the cheapest per node.
  Exponential, with a route counter.
- **§6 `cvGenSteps`** — one step per executed C++ line, including a stale-pop skip.
- **§7 `drGenSteps` (the oracle)** — the heap-based algorithm; terminal step carries
  `result` = the distance array with -1 for unreachable.

## 8. Independence (PLAN-019 G4)

`verify.py` is **Bellman-Ford**. It has no heap, no settled set and makes no greedy
choice — it just sweeps every edge n-1 times. Its correctness argument is induction on
the number of edges in a path, which is a completely different argument from
Dijkstra's "the cheapest frontier node is final". Two different proofs landing on the
same array is real evidence.

## 9. Complexity derivation

Each edge can improve its endpoint at most once per improvement, and every improvement
pushes one heap entry, so the heap holds at most O(E) entries. Every entry is pushed
and popped once at O(log E) = O(log V) each, giving O((V + E) log V). The stale-pop
check is O(1) and discards the extra copies. Space is the distance array plus the heap:
O(V) for the array, O(E) worst case for the heap.

## Output file

`algorithms/dijkstras-algorithm/lesson.html`
