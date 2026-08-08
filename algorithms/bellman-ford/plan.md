# Algorithm Lesson Plan: Bellman-Ford Algorithm

## Metadata

- **ID:** bellman-ford
- **Category:** Graph Algorithms (category_order 2), ramp_pos 5
- **Kind:** algorithm
- **Tier:** 2 (core)
- **Interview relevance:** medium
- **Archetype:** custom (weighted shortest path with negatives — visual-led §1; the
  thing to see is "after round k, every route of k edges is priced").
- **Question the lesson answers:** shortest distances from a source when weights may
  be negative — and whether a negative cycle makes the question meaningless.

## Complexity

- **Time:** O(V·E)
- **Space:** O(V)
- **Notes:** Handles negative weights and *detects* negative cycles, which Dijkstra
  cannot do at all.

## Prerequisites

- `dijkstras-algorithm` (as the thing that breaks when a weight goes negative)

## 1. Clarifying questions

1. **Can weights be negative?** Yes — that is the entire reason to use this. → rules
   out Dijkstra.
2. **Can there be a negative cycle?** Yes. → then "shortest" has no answer, and the
   algorithm must say so rather than return numbers.
3. **Directed or undirected?** Directed. → a negative edge in an *undirected* graph is
   already a negative cycle, since you can walk it back and forth.
4. **What marks an unreachable node?** `null`, not -1. → with negative weights -1 is a
   perfectly legal distance, so a numeric sentinel would be ambiguous.

## 2. The insight (foundational concept)

A shortest route in a graph with no negative cycle never repeats a node, so it uses at
most V-1 edges. Relaxing *every* edge once is enough to extend every correct answer by
one more edge. So after k rounds, every node reachable by a route of k edges or fewer
holds its true distance — and V-1 rounds cover every possible route.

## 3. Translations

1. Track *which* routes → just relax every edge, blindly. Order does not matter.
2. Loop forever until stable → stop after V-1 rounds. The bound is the proof.
3. Separate negative-cycle search → run **one more** round. Anything that still
   improves must be riding a cycle that pays.

## 4. Algorithm

1. Set every distance to infinity except `dist[src] = 0`.
2. Repeat V-1 times: for every edge `(u, v, w)`, if `dist[u] + w < dist[v]`, lower
   `dist[v]`.
3. Run one extra round. If any edge still improves, a negative cycle is reachable —
   report that and stop.
4. Otherwise return the distances, with `null` for anything still at infinity.

## 5. Examples (hand-derived, then cross-checked by verify.py)

| # | input | answer | derivation |
|---|-------|--------|------------|
| EX0 | n=5, the CLRS Fig 24.4 graph, src=0 | `{dist:[0,2,4,7,-2], neg:false}` | 0→3 costs 7; 3→2 is -3 giving 4; 2→1 is -2 giving 2; 1→4 is -4 giving -2 |
| EX1 | n=3, edges=[[0,1,1],[1,2,-1],[2,1,-1]], src=0 | `{dist:null, neg:true}` | the cycle 1→2→1 costs -2, so distances fall forever |
| EX2 | n=4, edges=[[0,1,4],[1,2,-2]], src=0 | `{dist:[0,4,2,null], neg:false}` | node 3 has no incoming edge; a negative weight is fine on its own |

EX0 deliberately contains negative edges but no negative cycle — the case Dijkstra
would silently get wrong.

## 6/7. Animation

- **§1 `siGenSteps`** — round by round on EX0, showing which distances become final
  after each round and why the round number bounds the route length.
- **§2 `bfGenSteps`** — enumerate every simple route and keep the cheapest. Correct
  only because a negative cycle is absent, and factorial in cost.
- **§6 `cvGenSteps`** — one step per executed C++ line, including the detection round.
- **§7 `drGenSteps` (the oracle)** — the V-1 rounds plus the detection round; terminal
  step carries `result` = `{dist, neg}`.

## 8. Independence (PLAN-019 G4)

`verify.py` is **Floyd-Warshall**. It is an all-pairs dynamic program over an
intermediate-vertex index, with no rounds, no source until the final row is read, and
a completely different negative-cycle rule (a negative entry on the diagonal rather
than a late improvement). Different recurrence, different detection, same answer.

## 9. Complexity derivation

Each round scans the whole edge list: O(E). There are V-1 rounds plus one detection
round, so O(V·E) in total. Space is one distance per node: O(V). The bound is tight in
the worst case — a path graph where the edges are relaxed in exactly the wrong order
needs every one of the V-1 rounds.

## Output file

`algorithms/bellman-ford/lesson.html`
