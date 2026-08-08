# Algorithm Lesson Plan: Kruskal's Algorithm

## Metadata

- **ID:** kruskals-mst
- **Category:** Graph Algorithms (category_order 2), ramp_pos 7
- **Kind:** algorithm
- **Tier:** 2 (core)
- **Interview relevance:** high
- **Archetype:** custom (minimum spanning tree — visual-led §1; the thing to see is
  components merging, not a tree growing).
- **Question the lesson answers:** connect every node for the least total edge weight.
  Report the total, or that no spanning tree exists.

## Complexity

- **Time:** O(E log E) — dominated by the sort
- **Space:** O(V)
- **Notes:** Union-find with path compression makes the cycle test effectively O(1).

## Prerequisites

- `union-find` / disjoint set
- sorting

## 1. Clarifying questions

1. **Is the graph connected?** Not necessarily. → then there is no spanning tree;
   report that rather than returning the weight of a forest.
2. **Undirected?** Yes. → an MST is only defined on undirected graphs.
3. **Can weights repeat?** Yes. → the tree is not unique, but the total weight is, so
   the answer is still well-defined.
4. **Total weight or the actual edges?** The total. → the edge list falls out of the
   same loop if needed.

## 2. The insight (foundational concept)

Sort the edges and take them cheapest first, skipping any edge whose two ends are
already connected. The skip is the whole algorithm: an edge inside one component would
close a cycle, and a cycle's most expensive edge is always removable. Being greedy is
safe because the cheapest edge crossing any split of the nodes is always in some
minimum tree.

## 3. Translations

1. Try every spanning tree → sort once and sweep. Exponential to O(E log E).
2. "Does this edge close a cycle?" by traversal → union-find. O(V) per edge → ~O(1).
3. Separate connectivity check → count accepted edges. Fewer than V-1 means the graph
   was disconnected, so no spanning tree exists.

## 4. Algorithm

1. Sort all edges by weight, ascending.
2. Put every node in its own union-find set.
3. For each edge in order: if its endpoints are already in the same set, skip it —
   it would close a cycle.
4. Otherwise accept it, union the two sets, and add its weight to the total.
5. Stop after V-1 accepted edges. If the sweep ends with fewer, the graph is
   disconnected and no spanning tree exists.

## 5. Examples (hand-derived, then cross-checked by verify.py)

| # | input | answer | derivation |
|---|-------|--------|------------|
| EX0 | n=5, 7 edges | `16` | take 2 (0-1), 3 (1-2), 5 (1-4), 6 (0-3); the 7, 8 and 9 edges all close cycles |
| EX1 | n=4, edges=[[0,1,1],[2,3,1]] | `null` | two separate pieces — only 1 edge can be accepted, not 3 |
| EX2 | n=4, a 4-cycle of weight 5 plus a chord of weight 1 | `11` | take the chord 1 (0-2), then two of the 5s; the fourth closes a cycle |

## 6/7. Animation

- **§1 `siGenSteps`** — components merging as edges are accepted; rejected edges shown
  dashed.
- **§2 `bfGenSteps`** — enumerate every subset of V-1 edges, test whether it spans and
  is acyclic, keep the cheapest. Counts subsets tried.
- **§6 `cvGenSteps`** — one step per executed C++ line, including a `find` that returns
  equal roots.
- **§7 `drGenSteps` (the oracle)** — sort plus union-find; terminal step carries
  `result` = the MST weight, or `null` when disconnected.

## 8. Independence (PLAN-019 G4)

`verify.py` is **Prim's algorithm** — grow one blob from node 0, repeatedly absorbing
the cheapest edge that leaves it. No sort, no union-find, one component instead of
many. The cut property says both must reach the same total, so agreement is a real
cross-check of the greedy claim rather than a re-run of it.

## 9. Complexity derivation

Sorting E edges is O(E log E), which dominates. The sweep does two `find` calls per
edge; with path compression and union by size each is O(α(V)), effectively constant,
so the sweep is O(E·α(V)). Total O(E log E). Space is the parent and size arrays:
O(V). Note log E ≤ 2 log V, so this is often written O(E log V).

## Output file

`algorithms/kruskals-mst/lesson.html`
