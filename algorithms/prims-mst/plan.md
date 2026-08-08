# Algorithm Lesson Plan: Prim's Algorithm

## Metadata

- **ID:** prims-mst
- **Category:** Graph Algorithms (category_order 2), ramp_pos 8
- **Kind:** algorithm
- **Tier:** 2 (core)
- **Interview relevance:** high
- **Archetype:** custom (minimum spanning tree — visual-led §1; the thing to see is
  one blob growing, as against Kruskal's many blobs merging).
- **Question the lesson answers:** connect every node for the least total weight,
  growing outward from a single starting node.

## Complexity

- **Time:** O(E log V) with a binary heap; O(V²) with a plain scan
- **Space:** O(V)
- **Notes:** The O(V²) form is faster on dense graphs, where E approaches V².

## Prerequisites

- `kruskals-mst` (same problem, opposite strategy)
- `heap` / priority queue

## 1. Clarifying questions

1. **Is the graph connected?** Not necessarily. → if the blob stops growing before it
   holds all V nodes, no spanning tree exists.
2. **Undirected?** Yes. → an MST is only defined on undirected graphs.
3. **Dense or sparse?** Decides the implementation. → heap for sparse, O(V²) scan for
   dense.
4. **Does the starting node matter?** No. → every start yields the same total weight,
   so node 0 is as good as any.

## 2. The insight (foundational concept)

Keep one connected blob and always absorb the cheapest edge leaving it. That edge is
the cheapest one crossing the cut between the blob and everything else, and the cut
property says such an edge belongs to some minimum tree. So the blob is always a
subtree of a correct answer, and it never has to be revised.

## 3. Translations

1. Try every spanning tree → grow one blob greedily. Exponential to polynomial.
2. Scan all edges for the cheapest leaving edge → keep candidates in a min-heap.
   O(V·E) → O(E log V).
3. Delete stale candidates → leave them in and skip on pop (`if (inTree[u]) continue`).
   A plain heap is enough; no decrease-key needed.

## 4. Algorithm

1. Push `(0, startNode)` — cost 0 to absorb the start itself.
2. Pop the cheapest `(w, u)`. If `u` is already in the blob, it is a stale candidate —
   skip it.
3. Otherwise absorb `u`: mark it, add `w` to the total, and count it.
4. Push every edge from `u` to a node not yet in the blob.
5. When the heap empties, return the total if all V nodes were absorbed; otherwise the
   graph was disconnected.

## 5. Examples (hand-derived, then cross-checked by verify.py)

| # | input | answer | derivation |
|---|-------|--------|------------|
| EX0 | n=6, 8 edges | `11` | absorb 1 (1-2), 2 (1-3), 2 (3-4), 3 (0-2), 3 (3-5) = 11; the 4s and the 6 are all skipped |
| EX1 | n=5, edges=[[0,1,2],[1,2,3],[3,4,1]] | `null` | the blob reaches only {0,1,2}; nodes 3 and 4 are in a separate piece |
| EX2 | n=3, triangle 1/2/3 | `3` | take 1 and 2; the weight-3 edge would close the triangle |

## 6/7. Animation

- **§1 `siGenSteps`** — the blob growing on EX0, with the cheapest leaving edge
  highlighted before each absorption.
- **§2 `bfGenSteps`** — rescan every edge each round to find the cheapest leaving one,
  with no heap. O(V·E), with a scan counter.
- **§6 `cvGenSteps`** — one step per executed C++ line, including a stale-pop skip.
- **§7 `drGenSteps` (the oracle)** — the heap version; terminal step carries `result` =
  the total weight, or `null` when disconnected.

## 8. Independence (PLAN-019 G4)

`verify.py` is **Kruskal** — sort the edge list once and accept any edge joining two
different union-find components. No blob, no heap, no notion of "leaving the tree". It
is the exact strategic opposite of Prim (merge many components versus grow one), which
makes it the sharpest available cross-check.

## 9. Complexity derivation

Each edge is pushed at most twice (once from each endpoint when that endpoint is
absorbed), so the heap holds O(E) entries. Every entry is pushed and popped once at
O(log E) = O(log V), giving O(E log V). The stale-pop check is O(1). Space is the
`inTree` array plus the heap: O(V) and O(E). On a dense graph, replacing the heap with
a scan for the cheapest leaving node gives O(V²), which beats O(E log V) once E ≈ V².

## Output file

`algorithms/prims-mst/lesson.html`
