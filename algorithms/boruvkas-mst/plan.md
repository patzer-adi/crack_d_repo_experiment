# Algorithm Lesson Plan: Borůvka's Algorithm

## Metadata
- **ID:** boruvkas-mst
- **Category:** Graph Algorithms (category_order 2)
- **Kind:** algorithm
- **Tier:** 3  (1=primer, 2=core, 3=advanced)
- **Interview relevance:** low

## Complexity
- **Time:** O(E log V)
- **Space:** O(V + E)
- **Notes:** Each round contracts the minimum outgoing edge of every component — naturally parallelisable.

## Prerequisites
- `kruskals-mst`
- `prims-mst`

## Key idea (short_note)
MST via parallel component contraction: in each round, every component picks its cheapest outgoing edge; the historical first MST algorithm (1926).

## Related LC problems
- (none)

## References
- Borůvka 1926
- CLRS problem 23-1

---

## Lesson outline

### 1. Motivation
[Why does this algorithm exist? What problem does it solve that simpler approaches cannot?
Start with the brute-force approach and show the cost. Then show the key insight.]

### 2. Core idea
[One-paragraph explanation of the central mechanism. No code yet — describe the invariant or
structure that makes the algorithm work.]

### 3. Step-by-step dry run
[Choose 1–2 concrete examples. Walk through every step showing state changes.
Use a table or annotated diagram for data structure state.]

### 4. Pseudocode
```
[Clean pseudocode, 10–20 lines]
```

### 5. Implementation (Python + C++)
[Both languages. Python for readability; C++ for performance-critical context.
Use the same conventions as existing lessons.]

### 6. Complexity analysis
[Derive time and space complexity from the pseudocode. Cover best/average/worst if they differ.]

### 7. Variants and extensions
[Other forms this algorithm takes, or common follow-up problems.]

### 8. Common pitfalls
[List 3–5 mistakes people make when implementing or applying this algorithm.]

## Output file
`algorithms/boruvkas-mst/lesson.html` — self-contained HTML, same style as lessons/ directory.
