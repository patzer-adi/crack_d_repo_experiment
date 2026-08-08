# Algorithm Lesson Plan: Depth-First Search (DFS)

## Metadata

- **ID:** dfs
- **Category:** Graph Algorithms (category_order 2), ramp_pos 2
- **Kind:** algorithm
- **Tier:** 1 (primer)
- **Interview relevance:** high
- **Archetype:** custom (graph traversal — visual-led §1, same structure as `bfs`).
- **Question the lesson answers:** which nodes are connected to which? Split the
  graph into its connected components.

## Complexity

- **Time:** O(V + E)
- **Space:** O(V)
- **Notes:** Recursion depth can reach V — use an explicit stack on large graphs.

## Prerequisites

- `stack` (or the call stack, which is the same thing)

## 1. Clarifying questions

1. **Is the graph connected?** Not necessarily. → the search must be restarted from
   every node that is still unvisited.
2. **Directed or undirected?** Undirected. → components are symmetric; on a directed
   graph "connected" splits into weak and strong, which is a different algorithm.
3. **How deep can it go?** Up to V nodes. → prefer an explicit stack; recursion
   overflows around 10^4–10^5 frames.
4. **Does visit order matter?** Not for components. → any order works, so we sort
   each component before returning to make the answer unique.

## 2. The insight (foundational concept)

DFS commits. It follows one edge as far as it goes before ever looking at the second
option, so it drains one whole component before touching another. That is what makes
it a component finder: everything reached from a start node in a single dive is
exactly one component, and the next unvisited node begins the next one.

## 3. Translations

1. Compare every pair of nodes → one dive per component. Reachability is transitive,
   so a single walk settles a whole group.
2. Sweep the edge list until labels stop changing → visit each node once. O(V·E) → O(V + E).
3. Separate `visited` set → mark on push, so a node can never enter the stack twice.

## 4. Algorithm

1. Mark every node unvisited; start with an empty component list.
2. For each node `s` in order: if it is already visited, skip it.
3. Otherwise push `s`, mark it visited, and run the stack loop — pop `u`, add it to
   the current component, push every unvisited neighbour (marking as you push).
4. When the stack empties, the component is complete. Sort it and record it.
5. Return the list of components.

## 5. Examples (hand-derived, then cross-checked by verify.py)

| # | input | answer | derivation |
|---|-------|--------|------------|
| EX0 | n=7, edges=[[0,1],[1,2],[0,2],[3,4],[5,6]] | `[[0,1,2],[3,4],[5,6]]` | a triangle, then two separate edges |
| EX1 | n=5, edges=[[0,1],[1,2],[2,3],[3,4]] | `[[0,1,2,3,4]]` | one path — a single component |
| EX2 | n=4, edges=[] | `[[0],[1],[2],[3]]` | no edges, so every node is its own component |

## 6/7. Animation

- **§1 `siGenSteps`** — the dive: one component drained completely before the next starts.
- **§2 `bfGenSteps`** — label propagation: give each node its own label, then sweep the
  whole edge list lowering labels until nothing changes. O(V·E), with a sweep counter.
- **§6 `cvGenSteps`** — one step per executed C++ line.
- **§7 `drGenSteps` (the oracle)** — explicit-stack DFS with restarts; terminal step
  carries `result` = the component list.

## 8. Independence (PLAN-019 G4)

`verify.py` is **union-find**. It never traverses the graph: it merges the endpoints
of every edge and then reads off the equivalence classes. No stack, no visiting, no
notion of a dive — a different mechanism that must agree.

## 9. Complexity derivation

Every node is pushed at most once because it is marked at push time, so the pop loop
runs V times in total across all restarts. Each pop scans one adjacency list, and
every edge is scanned from both ends — 2E. Total O(V + E). The sort of each component
adds O(V log V) overall, which we accept to make the answer canonical. Space is the
visited array plus a stack bounded by V: O(V).

## Output file

`algorithms/dfs/lesson.html`
