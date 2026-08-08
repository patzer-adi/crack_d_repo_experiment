# Algorithm Lesson Plan: Breadth-First Search (BFS)

## Metadata

- **ID:** bfs
- **Category:** Graph Algorithms (category_order 2), ramp_pos 1
- **Kind:** algorithm
- **Tier:** 1 (primer)
- **Interview relevance:** high
- **Archetype:** custom (graph traversal — a node-link visual carries the insight,
  so the lesson is visual-led rather than chain-box led, matching the
  `rotting-oranges` teaching structure).
- **Question the lesson answers:** given an unweighted graph and a source, what is
  the shortest distance (in edges) to every node?

## Complexity

- **Time:** O(V + E)
- **Space:** O(V)
- **Notes:** Yields shortest-path distance in unit-weight graphs.

## Prerequisites

- `hash-table` (or any O(1) "have I seen this node?" structure)

## 1. Clarifying questions

1. **Is the graph weighted?** No — every edge costs 1. → unlocks BFS at all; a
   weighted graph needs Dijkstra.
2. **Directed or undirected?** Undirected here. → each edge goes into both
   adjacency lists.
3. **Is the graph connected?** Not necessarily. → unreachable nodes keep distance
   -1; do not assume every node is visited.
4. **Do we need the path or only the distance?** Distance here. → one `dist` array
   is enough; a `parent` array would reconstruct the path.

## 2. The insight (foundational concept)

A queue makes the search expand in rings. Everything at distance 0 comes out first,
then everything at distance 1, then distance 2. Because a node is claimed the very
first time it is reached, the ring it lands in is its shortest distance — no later
path can be shorter, because every shorter ring has already been emptied.

## 3. Translations

1. Enumerate every path → expand rings. Drops the factorial path count.
2. "Which path was shortest?" → claim each node once, on first arrival. The first
   arrival is provably the shortest, so no comparison is needed.
3. Separate `visited` set → `dist[v] != -1` doubles as the visited mark. One array,
   not two.

## 4. Algorithm

1. Set every distance to -1 ("not reached"), set `dist[src] = 0`, push `src`.
2. Pop the front node `u`.
3. For each neighbour `v` with `dist[v] == -1`, set `dist[v] = dist[u] + 1` and push `v`.
4. Repeat until the queue is empty.
5. Return `dist`. A -1 means unreachable.

## 5. Examples (hand-derived, then cross-checked by verify.py)

| # | input | answer | derivation |
|---|-------|--------|------------|
| EX0 | n=6, edges=[[0,1],[0,2],[1,3],[2,3],[3,4],[4,5]], src=0 | `[0,1,1,2,3,4]` | rings: {0} · {1,2} · {3} · {4} · {5} |
| EX1 | n=5, edges=[[0,1],[1,2],[3,4]], src=0 | `[0,1,2,-1,-1]` | 3 and 4 sit in a separate component |
| EX2 | n=4, edges=[[0,1],[1,2],[2,3],[3,0]], src=0 | `[0,1,2,1]` | a cycle: 3 is reached directly, so it is distance 1, not 3 |

## 6/7. Animation

- **§1 `siGenSteps`** — ring expansion on the EX0 graph. Pedagogical, no `result`.
- **§2 `bfGenSteps`** — DFS enumeration of *every simple path* from the source,
  keeping the shortest length seen per node. Counts paths explored, so the cost is
  visible. This is a genuinely different (exponential) method, not a slower BFS.
- **§6 `cvGenSteps`** — one step per executed C++ line, over the same three examples.
- **§7 `drGenSteps` (the oracle)** — the queue BFS itself; terminal step carries
  `result` = the distance array with -1 for unreachable.

## 8. Independence (PLAN-019 G4)

`verify.py` is **Bellman-Ford relaxation to a fixpoint**: repeatedly sweep the whole
edge list lowering `dist[v]` to `dist[u]+1` until a sweep changes nothing. No queue,
no rings, no notion of a frontier — a different algorithm that must land on the same
array. That makes the cross-check evidence rather than a restatement.

## 9. Complexity derivation

Each node is pushed at most once (the `dist[v] != -1` guard), so the pop loop runs V
times. Each pop scans that node's adjacency list, and over the whole run every edge
is scanned twice (once from each endpoint) — 2E work. Total O(V + E). Space is the
`dist` array plus a queue that never holds more than V nodes: O(V).

## Output file

`algorithms/bfs/lesson.html`
