# PLAN-013: Algorithms Reference Inventory + Dashboard Integration

**Created:** 2026-05-16
**Status:** Draft
**Addresses:** The Masters-level Algorithm List PDF (`MustKnowAlgorithmList.pdf`) enumerates ~100 canonical CS algorithms across 15 categories — most of which are NOT LeetCode-shaped problems (QuickSort, KMP, Dijkstra, Floyd-Warshall, FFT, Union-Find, Segment Tree with lazy propagation, RSA, MapReduce, Voronoi diagrams, etc.) and therefore do not belong in `data/problems.json`. The user wants this reference inventory **visible in the dashboard but cleanly separated from the LC interview-prep track**, with a future intent to generate lessons for the algorithms themselves (not for "a LeetCode problem that uses this algorithm" — a lesson on the *algorithm* itself).

---

## 1. Context & motivation

### 1.1 What the PDF gives us

The PDF is a flat enumeration of ~100 algorithms grouped into 15 categories:

| # | Category | ~Count | Sample entries |
|---|---|---|---|
| 1 | Foundational | 13 | QuickSort, MergeSort, HeapSort, Binary Search, Hashing |
| 2 | Graph | 14 | BFS, DFS, Dijkstra, Bellman-Ford, A*, Kruskal, Prim, Ford-Fulkerson, Edmonds-Karp, Topological Sort, Kosaraju, Tarjan |
| 3 | Dynamic Programming | 9 | LCS, LIS, 0/1 Knapsack, TSP, Matrix Chain, Rod Cutting, Subset Sum, Edit Distance, Floyd-Warshall, Bell/Catalan |
| 4 | String | 7 | Naive, KMP, Rabin-Karp, Boyer-Moore, Suffix Array/Tree, Aho-Corasick, Z |
| 5 | Computational Geometry | 7 | Graham, Jarvis, Line-segment intersection, Closest pair, Voronoi, Delaunay, Sweep line, Rotating calipers |
| 6 | Numerical & Optimization | 8 | Newton-Raphson, Gradient Descent, Simulated Annealing, GA, Simplex, Interior Point, DTW, FFT |
| 7 | Data-Structure-Specific | 7 | AVL, Red-Black, Splay, Trie/TST, DSU, Fenwick (BIT), Segment Tree + Lazy, Bloom, Skip List |
| 8 | Advanced Graph | 5 | Planarity, Graph Coloring, Hungarian (Bipartite Matching), Spectral, PageRank |
| 9 | Cryptography & Security | 5 | RSA, Diffie-Hellman, ECC, AES/DES, SHA/MD5, Merkle |
| 10 | ML & Data Mining | 7 | k-NN, k-Means, Decision Trees, SVM, Apriori, EM, PCA |
| 11 | Parallel & Distributed | 5 | MapReduce, Paxos/Raft, Work Stealing, Bitonic/Hypercube Sort, DHT |
| 12 | Miscellaneous | 6 | Backtracking, D&C (Karatsuba, Strassen), Greedy (Activity Selection, Huffman), Randomized (Reservoir, QuickSelect), Monte Carlo, Approximation |
| 13 | Domain-Specific | 4 | Smith-Waterman, Needleman-Wunsch, Canny, RANSAC, TCP Congestion, B-Tree, LSM |
| 14 | Advanced Theoretical | 5 | Matrix Expo, Fast Modular Expo, Sieve, GCD/Extended/Modular Inverse, Vertex Cover, Set Cover, Min-Cut, Randomized QuickSort |
| 15 | Emerging | 3 | Shor's, Grover's, Q-Learning, DQN |

**Coarse-grained interview relevance audit:**
- **High** (cellular to interviews): ~35 — Foundational sorting/search, BFS/DFS/Dijkstra/Topo/MST, DP classics, KMP, DSU, BIT, Segment Tree, Backtracking, Greedy, Reservoir/QuickSelect, Sieve, GCD, Modular Expo.
- **Medium** (sometimes asked, useful background): ~30 — A*, Bellman-Ford, Floyd-Warshall, Edmonds-Karp, Tarjan SCC, AVL/Red-Black, Trie, Skip List, Karatsuba, Strassen, FFT, Convex Hull, Sweep Line, RANSAC, Reservoir, Min-Cut, Vertex/Set Cover, Approximation.
- **Low** (mostly cultural / theoretical literacy): ~35 — Voronoi, Delaunay, Newton-Raphson, GA, SVM, Apriori, PCA (algorithmic), Paxos/Raft, MapReduce, Bitonic sort, DHT, RSA, Diffie-Hellman, ECC, AES, Merkle, k-NN, k-Means, EM, Smith-Waterman, Needleman-Wunsch, Canny, B-Tree, LSM, TCP, Shor, Grover, Q-Learning, DQN.

This distribution matters because it informs both **what to curate** and **what order to generate lessons in**.

### 1.2 Why this is NOT `data/problems.json`

| Aspect | `data/problems.json` (LC) | Proposed `data/algorithms.json` |
|---|---|---|
| Unit | A solvable problem | A named algorithm / data structure |
| Identifier | `lc_num` + `slug` (LeetCode-derived) | `id` (kebab-case, project-internal) |
| Per-entry status | `status: done\|new` (have you solved it?) | n/a — algorithms are *known*, not *solved* |
| Lesson framing | "Brute force → optimise → dry run → code" | "Motivation → invariant → pseudocode → complexity → implementation → variants" |
| Difficulty meaning | Easy/Medium/Hard (LC's verdict) | Interview-relevance + complexity-of-understanding (different axes) |
| Cross-link | None — each problem stands alone | `prereqs` (other algos), `related_lc` (LC problems that exercise it) |

The schemas don't fit. Mashing them together would require nullable LC fields on algorithm rows and nullable algorithm fields on LC rows — half-empty rows everywhere. The user explicitly said "do not mix" and the data shapes confirm that's the right call.

### 1.3 What "later generate lessons for these" means

A lesson for *Dijkstra* is fundamentally different from a lesson for *LC 743 Network Delay Time*:

- The LC lesson centers on **one input → one output**, walks the algorithmic choices needed for that specific shape, and ends with a working solution.
- An algorithm lesson centers on **the algorithm as a tool**: when it applies, why it works (invariants/proof sketch), how to implement it cleanly, what its variants are, what its limitations are, and pointers to representative problems (which are LC entries — that's the cross-link).

Different section template, different golden-reference set, different generator prompt. PLAN-011's `lessons/design/` infrastructure was built for LC lessons; this plan creates a sibling structure `algorithms/design/` (deliberate dir naming to mirror it, not reuse it) and a separate template.

---

## 2. Goals

- **G1:** `data/algorithms.json` exists with ~100 entries covering every algorithm in the PDF, each carrying: `id, name, category, aliases, tier, ramp_pos, interview_relevance, complexity, prereqs, short_note, references, related_lc, lesson_status, lesson_path`.
- **G2:** Entries are **organised as difficulty/dependency ramps within each category** — same principle as PLAN-012 §4.5. The reader can start at category position 1, finish, and feel ready for position 2.
- **G3:** The dashboard surfaces the algorithm inventory in a way that is **clearly separated from the LC track** but accessible from the same URL (no second site to remember). See §4.3 for option choice.
- **G4:** Cross-linking works both ways: each algorithm row shows which LC problems exercise it; each LC problem row optionally surfaces which algorithm(s) it instantiates.
- **G5:** `algorithms/<id>/` is the per-algorithm artifact directory (mirroring `lessons/<slug>/`), ready to receive a `lesson.html` later.
- **G6:** A small follow-up plan (PLAN-014) is scaffolded but not executed: it covers the algorithm-lesson template (`algorithms/design/`), a sample first lesson (one of the high-relevance ones, e.g. Dijkstra or KMP), and a generation workflow.

## 3. Non-goals

- Writing any algorithm lessons in this plan. PLAN-014 (or per-algorithm `/batch-algorithm` invocations) does that downstream.
- Removing, renaming, or restructuring anything in `data/problems.json`. The LC inventory is frozen vs this work.
- Building a graph-visualisation of the `prereqs` dependency DAG (nice-to-have for a future plan).
- Reproducing the PDF verbatim in markdown. The PDF is the source; the JSON is the structured working artifact. The PDF stays in `problems/` (or moves to `algorithms/`) as the original reference.
- Curating algorithms beyond the PDF's 15-category scope. If the user wants additions later (e.g. specific competitive-programming techniques), those go in a follow-up.
- Lesson-format design for algorithms. PLAN-014 handles that.

## 4. Approach

### 4.1 Schema for `data/algorithms.json`

Each entry:

```jsonc
{
  "id": "dijkstras-algorithm",                // kebab-case, stable, primary key
  "name": "Dijkstra's Algorithm",
  "category": "Graph Algorithms",             // one of the 15 canonical categories
  "category_order": 2,                        // section_order
  "ramp_pos": 5,                              // within-category ramp position
  "order": 2005,                              // = category_order * 1000 + ramp_pos
  "kind": "algorithm",                        // "algorithm" | "data_structure" (protocols stay under "algorithm")
  "aliases": ["Dijkstra", "SSSP"],
  "tier": 1,                                  // 1=foundational, 2=core, 3=advanced
  "interview_relevance": "high",              // "high" | "medium" | "low" (dashboard hides "low" by default)
  "complexity": {
    "time": "O((V+E) log V) with a binary heap",
    "space": "O(V)",
    "notes": "Requires non-negative edge weights"
  },
  "prereqs": ["bfs", "priority-queue", "greedy-paradigm"],
  "short_note": "Greedy shortest-path with a min-heap; relax outgoing edges of the closest unsettled vertex.",
  "references": [
    "CLRS Ch 24.3",
    "https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm"
  ],
  "related_lc": ["network-delay-time", "path-with-minimum-effort",
                 "cheapest-flights-within-k-stops", "swim-in-rising-water"],
  "lesson_status": "none",                    // "none" | "in-progress" | "generated"
  "lesson_path": null                         // "algorithms/dijkstras-algorithm/lesson.html" once authored
}
```

**Design choices:**
- **No `status` field.** Algorithms are *learned*, not *solved* — a binary done/not-done doesn't map well. The `lesson_status` field implicitly tracks engagement: `none` = haven't built the lesson yet, `generated` = lesson exists. If the user later wants a "I've reviewed this" toggle, it's a one-field addition.
- **`order` mirrors the PLAN-012 convention** so the dashboard sort-by-order naturally groups by category and respects within-category ramp.
- **`prereqs` is a list of algorithm `id`s** — not enforced as a real graph in this plan, but the data is shaped to support a dependency-graph visualisation in a future plan.
- **`related_lc` carries LC `slug`s** (not `lc_num`) — the dashboard can resolve these against `data/problems.json` on load to render a "see also" chip.

### 4.2 Curation from PDF

Approach: produce `scripts/seeds/algorithms_seed.yaml` (mirroring `comprehensive_seed.yaml`), one ordered ramp per category, ~100 entries total. For each entry: name + ramp_pos + tier + relevance + 1-line `short_note` + complexity + 1-3 prereqs + 1-5 LC cross-links if applicable.

**Curation pace:** doing this in three batches keeps the checkpoints small.
- Batch 1: categories 1–4 (Foundational, Graph, DP, String) — these are the core interview tracks and the categories with the densest `related_lc` cross-linking. ~43 entries.
- Batch 2: categories 5–10 (Geometry, Numerical/Opt, Data-Structure, Advanced Graph, Crypto, ML) — mid-relevance, less LC overlap. ~37 entries.
- Batch 3: categories 11–15 (Parallel/Distributed, Misc, Domain-Specific, Advanced Theoretical, Emerging) — sparse interview relevance but cultural-literacy value. ~20 entries.

Each batch ends with a checkpoint for user review (same shape as PLAN-012 checkpoints).

### 4.3 Dashboard integration — **Option B (locked)**

**Decision (2026-05-16):** Tabbed view in `dashboard/index.html`. One URL, one mental model.

- Top-of-page tab strip: `[ LC Problems | Algorithms ]`. Tab state mirrored to URL hash (`#problems` / `#algorithms`) so back/forward and bookmarks work.
- Each tab fetches its own JSON on activation; only one populates the table area at a time.
- Search/filter chips re-render per tab:
  - **LC tab** keeps the existing filters: topic dropdown, difficulty pills, status pills, lesson pill.
  - **Algorithms tab** gets a fresh filter strip: category dropdown, `kind` pills (algorithm | data_structure), tier pills (1/2/3), `interview_relevance` pills (high | medium | low), `lesson_status` pill.
- **`interview_relevance` filter defaults to "high + medium"** per §2 decision — the ~35 low-relevance entries are curated but hidden until the "low" pill is clicked. This preserves the full PDF coverage without dashboard noise.
- Shared chrome: header, theme, font, search input, stat-chip strip (each tab populates its own stats).
- **Effort:** ~5 hr (tab strip + URL routing + algorithm-flavoured filter bar + cross-link chip rendering).

Options A (separate page) and C (separate site) were considered and rejected in favour of UX cohesion.

### 4.4 Cross-linking algorithms ↔ LC problems

Two-way linkage with no schema pollution:

- **Algorithm → LC:** `related_lc: ["network-delay-time", ...]` on the algorithm side. The algorithms dashboard view resolves these against `data/problems.json` on load and renders them as clickable chips (clicking switches to the LC tab filtered by that slug).
- **LC → Algorithm:** computed on the fly in the LC dashboard view. For each LC problem, find algorithms whose `related_lc` contains this slug, render them as small chips on the row ("Practice for: Dijkstra ↗"). No edit to `data/problems.json` needed.

This is a derived index, not a source-of-truth duplication. If you add a new LC cross-link, you do it on the algorithm entry only.

### 4.5 Lesson format (for PLAN-014, scaffolded here)

A canonical algorithm lesson has different sections from an LC lesson:

| LC lesson section (PLAN-011) | Algorithm lesson section (new, for PLAN-014) |
|---|---|
| Clarifying questions | Motivation — when do you reach for this? |
| Foundational concept | Preconditions — what must be true of the input? |
| Brute force | Naive baseline (if any) and why it fails |
| Translations | Key insight — the trick |
| Algorithm steps | Pseudocode |
| Code | Invariant / correctness sketch |
| Examples (dry run) | Worked dry run on a small input |
| Edge cases | Complexity analysis |
| Approaches table | Reference implementation (Python + C++) |
| Take-home | Variants & extensions |
| | When to prefer over alternatives |
| | LC problems that exercise it (auto-rendered from `related_lc`) |

This plan only *scaffolds* the format: it creates an empty `algorithms/design/LESSON_DESIGN.md` placeholder pointing at PLAN-014. The actual template + golden + generator workflow is PLAN-014.

**Implementation-style decision (locked 2026-05-16):** algorithm lessons will use the **Python + C++** dual-panel style, same as LC lessons. Rationale: consistency with the existing lesson aesthetic and the user's preference for runnable reference code over pseudocode-only. Pseudocode still appears in the "Key insight / how it works" section but is not the sole code artifact. Schema implication: the `references` field stays for external links (CLRS, Wikipedia, papers) — canonical implementations live inside the lesson HTML, not in the inventory JSON.

### 4.6 Difficulty / dependency ramp within each category (G2)

Same principle as PLAN-012 §4.5: order each category so each step adds *one* new concept on top of the prior step. Examples (illustrative — not the final ramp):

**Graph Algorithms ramp (illustrative):**
1. BFS (primer — explore from a source, level order)
2. DFS (recursion or stack, pre/post ordering)
3. Topological Sort (DFS post-order or Kahn's queue)
4. Union-Find / DSU (linking-by-rank, path compression)
5. Dijkstra (greedy shortest path with PQ)
6. Bellman-Ford (relaxation, handles negative edges)
7. Floyd-Warshall (all-pairs via DP)
8. A* (heuristic-guided Dijkstra)
9. Kruskal's MST (DSU + sort edges)
10. Prim's MST (PQ + grow tree)
11. Boruvka's MST (parallel-friendly variant)
12. Ford-Fulkerson (augmenting paths)
13. Edmonds-Karp (Ford-Fulkerson with BFS)
14. Dinic's (level-graph + blocking flows)
15. Kosaraju's SCC (two DFS passes)
16. Tarjan's SCC (single DFS with lowlink)
17. Eulerian / Hamiltonian paths

The ramp respects: classic DFS/BFS before Dijkstra; DSU before Kruskal; basic shortest-path before all-pairs and heuristic; max-flow basics before augmenting variants.

Each category gets its own ramp during curation (§4.2).

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 0 | **(complete)** Resolve §8 decisions with user — done 2026-05-16 | — | — |
| 1 | Place `MustKnowAlgorithmList.pdf` at `algorithms/MustKnowAlgorithmList.pdf` (user must commit it into the repo; agent can't fetch from the conversation upload) | 5 min | — |
| 2 | Define schema, write `data/algorithms.schema.json` (lightweight JSON Schema for validation) | 1 hr | 1 |
| 3 | **Curate batch 1** — categories 1–4 (Foundational, Graph, DP, String). ~43 entries with ramps. Each carries `complexity`, `short_note`, `prereqs`, `related_lc`. | 3 hr | 2 |
| 4 | Checkpoint 1 — walk batch 1 with user, adjust | 30 min | 3 |
| 5 | **Curate batch 2** — categories 5–10 (Geometry, Numerical/Opt, Data-Structure, Advanced Graph, Crypto, ML). ~37 entries. | 2 hr | 4 |
| 6 | Checkpoint 2 — walk batch 2 with user, adjust | 20 min | 5 |
| 7 | **Curate batch 3** — categories 11–15 (Parallel, Misc, Domain-Specific, Advanced Theoretical, Emerging). ~20 entries. | 1 hr | 6 |
| 8 | Checkpoint 3 — walk batch 3 with user, adjust | 20 min | 7 |
| 9 | Write `scripts/build_algorithms_list.py` — converts `scripts/seeds/algorithms_seed.yaml` → `data/algorithms.json`. Validates schema, computes `order`, fills `lesson_path` based on existence of `algorithms/<id>/lesson.html`. | 1 hr | 8 |
| 10 | Run build, write `data/algorithms.json`, eyeball | 20 min | 9 |
| 11 | **Implement chosen integration option** (default B — tabbed view): add tab strip + URL hash routing to `dashboard/index.html`; fetch `data/algorithms.json` for the algorithms tab; render with algorithm-flavoured filter chips (category dropdown, tier pills, relevance pills, `lesson_status` pill) | 4 hr (Option B); 2 hr (A); 5 hr (C) | 1, 10 |
| 12 | Implement cross-linking: LC rows show "see-also algorithm" chips computed from `algorithms.json` on load; algorithm rows show clickable `related_lc` slug chips that switch tab and filter | 1.5 hr | 11 |
| 13 | Create `algorithms/<id>/` directories for all ~100 entries (empty, ready to receive a lesson). Scaffolded by `scripts/new_algorithm.py` (mirrors `new_lesson.py`). | 1 hr | 10 |
| 14 | Write `algorithms/design/LESSON_DESIGN.md` as a placeholder pointing at PLAN-014. Just enough so a future agent loading the file knows what to do. | 20 min | 13 |
| 15 | Stub PLAN-014 (the lesson-authoring plan) — write the goals + non-goals + open questions, leave §4 detailed approach for when PLAN-014 actually fires | 30 min | 14 |
| 16 | Write `REPORT-013` + update `current_state_report.md` | 30 min | 15 |

Total estimated effort: **~17 hr**, of which **~8 hr is curation** (tasks 3, 5, 7) — the analytical core.

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Categories from PDF don't map cleanly to interview prep buckets (e.g. "Foundational" sorts vs "Misc" backtracking — both interview-relevant but in different categories) | High | Medium | Categories follow the PDF verbatim for fidelity. A `tier` + `interview_relevance` field lets the dashboard filter across categories for "show me the high-relevance foundational set" — orthogonal axes. |
| `related_lc` slugs drift if LC entries are renamed in `problems.json` | Low | Low | Build script validates every slug in `related_lc` against current `data/problems.json` and warns on missing. |
| Lesson format for algorithms requires golden references that don't exist yet | Certain | Low | Explicitly deferred to PLAN-014. This plan only scaffolds the directory structure and the placeholder design file. |
| User adds an algorithm not in the PDF later | Medium | Low | Seed is YAML; appending is one entry. Build script is idempotent. |
| Some PDF entries are non-algorithms (e.g. "Hash tables, Hash maps, Open addressing, Separate chaining" — these are data structures and techniques, not single algorithms) | Certain | Low | Allow `kind: "data_structure"` or `kind: "technique"` as an optional field. Default `kind: "algorithm"`. Display same in dashboard. |
| Dashboard tab switcher (Option B) breaks existing add-problem modal or any other LC-only feature | Medium | Medium | Treat LC tab as the current `dashboard/index.html` near-verbatim; algorithms tab is additive. Smoke-test all existing LC features in the LC tab post-implementation. |
| `prereqs` graph has cycles or refers to missing IDs | Low | Low | Build script topological-sort-checks the `prereqs` DAG; fails build on cycles or dangling refs. |
| Inventory grows unwieldy at ~100 entries | Low | Low | The category grouping caps any single section to ≤17 items (graphs). Tier + relevance filters let the user thin the view. |

---

## 7. Success criteria

- [ ] G1 — `data/algorithms.json` exists with all PDF entries (~100), schema-valid
- [ ] G2 — Each category is an ordered ramp; user signs off on the ramps at the three checkpoints
- [ ] G3 — Dashboard surfaces algorithms via chosen integration option; LC track unaffected (smoke-tested)
- [ ] G4 — Cross-links render in both directions; clicking a chip navigates correctly
- [ ] G5 — `algorithms/<id>/` directories exist for every entry, empty and ready
- [ ] G6 — PLAN-014 stub exists with goals + non-goals
- [ ] `REPORT-013` written; `current_state_report.md` updated

---

## 8. Decisions (resolved 2026-05-16)

1. **Integration:** **Option B — tabbed view** in `dashboard/index.html` with URL hash routing (`#problems` / `#algorithms`). One URL, shared chrome, per-tab filter strip. Algorithms tab's `interview_relevance` filter defaults to "high + medium".
2. **Scope:** **All ~100 entries curated, "low" relevance hidden by default.** Full PDF coverage; dashboard relevance filter starts at "high + medium" and exposes "low" via a pill toggle. Three curation batches stay at 43 + 37 + 20 (categories 1–4, 5–10, 11–15).
3. **Kinds:** **Two kinds — `algorithm` vs `data_structure`.** AVL, Red-Black, Splay, Trie, TST, DSU, BIT, Segment Tree, Bloom Filter, Skip List get `kind: "data_structure"`. Protocols (RSA, AES, DH, Paxos, Raft) stay under `kind: "algorithm"` — pragmatic two-bucket split, no protocol kind.
4. **Lesson style for PLAN-014:** **Python + C++ dual-panel** (same as LC lessons). Pseudocode appears inline in the "key insight" section but isn't the sole code artifact. Schema's `references` field holds external links only (CLRS, Wikipedia, papers); canonical implementations live in the lesson HTML.
5. **Printable markdown summary:** **yes, regenerate** `algorithms/algorithms_reference.md` from the JSON via `scripts/render_algorithms_sheet.py` (mirrors `render_problem_sheet.py`). Two views: `--all` (full inventory) and `--relevance high` (high-relevance-only quick-scan).

---

## 9. References

- `MustKnowAlgorithmList.pdf` — source enumeration (uploaded by user in conversation; **task 0**: copy it into the repo at `algorithms/MustKnowAlgorithmList.pdf` so future agents can find it)
- `AGENT_MD/plan/plans/PLAN-012_comprehensive_problem_list.md` — the LC merge plan whose schema and ramp principles this plan mirrors
- `AGENT_MD/plan/plans/PLAN-011_lesson_gen_efficiency.md` — the lesson-generation infrastructure that PLAN-014 will extend for algorithm lessons
- `dashboard/index.html` — the LC dashboard whose chrome the algorithms view will share (under Option B)
- `data/problems.json` — the LC inventory that `related_lc` cross-links resolve against
