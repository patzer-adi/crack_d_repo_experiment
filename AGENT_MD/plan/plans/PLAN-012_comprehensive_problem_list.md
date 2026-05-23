# PLAN-012: Comprehensive Interview-Coverage Problem List

**Created:** 2026-05-16
**Status:** Draft
**Addresses:** The two existing problem inventories — `problems/google_focused_reduced_dsa_sheet.md` (86 unique LC#s, Google-flavoured) and `data/problems.json` (153 problems, the dashboard-backed working list) — together still leave several interview-relevant patterns thin or absent (Union-Find as a named track, Bitmask DP, Segment Tree / Fenwick, Sweep-line, KMP, Reservoir sampling, Tree DP, Game-theory DP, several Google "signature" problems). This plan (a) merges the two sources, (b) layers on the pattern coverage gaps to produce a single comprehensive list (~190 problems) that maximises pattern surface area for Google-style interviews, and (c) decides how the comprehensive list lives alongside the existing inventory.

---

## 1. Context & motivation

### 1.1 What we have today

| Source | Count | Structure | Used by |
|---|---|---|---|
| `problems/google_focused_reduced_dsa_sheet.md` | 86 unique (95 listed, 9 dupes between category and "Hard" sections) | Plain markdown tables grouped by category | Reference only — not parsed |
| `data/problems.json` | 153 | Structured JSON: `order, lc_num, name, url, slug, topic, difficulty, status, section, lesson_status` | Dashboard, lesson scaffolding (`scripts/server.py`, `dashboard/index.html`, `scripts/new_lesson.py`) |

`problems.json` is already a near-superset of the google-focused sheet. Only **13** google-focused problems are not yet in `problems.json` (enumerated in §4.1). The bigger question is not "which 13 to copy over" but **"are there patterns no list covers that a Google interviewer would credibly ask?"** — §4.2 catalogues those.

### 1.2 Pattern-coverage audit (across both lists combined)

| Pattern / DS | Status today | Verdict |
|---|---|---|
| Arrays, hashing, two-pointer, sliding window | Saturated | ✅ |
| Binary search (basic + on-answer) | Strong (704, 33, 153, 875, 1011, 4, 410, 162, 74, 981) | ✅ |
| Stack / monotonic stack | Covered (20, 155, 84, 739, 394, 496, 735, 853, 150) | ✅ |
| Linked list (incl. cycle, reorder, copy, LRU) | Covered (206, 21, 23, 19, 142, 146, 138, 143) | ✅ |
| Trees (DFS / BFS / construction / LCA / path) | Covered (104?, 226?, 102, 199, 236, 124, 297, 105, 543, 113, 114, 110, 235) — **104 & 226 actually missing from JSON** | ⚠️ tiny gap |
| BST (validate, kth, iterator, delete) | Covered (98, 230, 173, 450) | ✅ |
| Heap / Priority Queue | Strong (215, 347, 973, 295, 621, 767, 502, 355) | ✅ |
| Graphs — BFS / DFS / island | Strong (200, 695, 994, 130, 417, 286, 547, 261) | ✅ |
| Graphs — Topological / DAG | Covered (207, 210, 269) | ✅ |
| Graphs — Dijkstra / shortest path | Light (743, 787) | ⚠️ add 1631, 778 |
| Graphs — MST | None in JSON (1584 only in google sheet) | ⚠️ add 1584 |
| Graphs — Union-Find as a *named pattern* | Implicit only (684, 547, 261, 721) | ⚠️ formalise + add 323, 947, 1319 |
| Graphs — Bellman-Ford / 0-1 BFS | None | ⚠️ 787 doubles as Bellman-Ford-lite; OK |
| DP — 1D / Stock | Covered (70, 198, 213, 91, 152, 121, 309, 714) | ✅ |
| DP — 2D / LCS / Edit / Distinct subseq | Covered (1143, 72, 115, 10) | ✅ |
| DP — Knapsack | Covered (416, 494, 377, 322) | ✅ |
| DP — Grid | Covered (64, 120) | ✅ |
| DP — Palindrome / Interval | Covered (647, 516, 312) | ✅ |
| DP — Bitmask / state compression | **None** | ❌ add 847, 698, 526 |
| DP — Tree DP | Partial (124, 543, 110) | ⚠️ add 337 (House Robber III) |
| DP — Game theory / minimax | **None** | ❌ add 486, 877 |
| Backtracking (permutations/subsets/combinations) | Covered (46, 78, 39, 79, 22, 51, 131, 216, 17?) — **17 missing** | ⚠️ add 17, 40, 47, 90 (dedup variants) |
| Greedy / Intervals | Covered (55, 45, 56, 57, 435, 452, 134, 763, 846, 1899, 678, 406) | ✅ |
| Sweep line / Meeting Rooms | **None** | ❌ add 252, 253; optional 218 (Skyline) |
| Trie | Covered (208, 211, 212, 648); add 421 for Trie+Bit | ⚠️ minor |
| Bit manipulation | Covered (136, 190, 268, 371, 338, 231) | ✅ |
| Math / number theory | Light (29) | ⚠️ add 50 (Pow), 69 (Sqrt), 7 (Reverse Int), 8 (atoi), 204 (Primes) |
| Prefix sum / Diff array | Light (560, 525 missing from JSON; 209 covered) | ⚠️ add 304, 974, 1248 |
| Segment Tree / Fenwick (BIT) | **None** | ❌ add 307, 315 |
| String matching (KMP / Rabin-Karp / Z) | **None** beyond brute force (459 covered) | ❌ add 28, 686 |
| Reservoir / weighted random | **None** | ❌ add 380, 528, 382 |
| Multi-source BFS / matrix BFS | Partial (994, 286) | ⚠️ add 542, 1162 |
| Quickselect | Implicit (215) | ✅ |
| Concurrency | Out of scope | — skip |
| Design (LRU/LFU/Twitter/CircularQ/Q-from-Stack) | Covered (146, 460, 355, 622, 232) | ✅ |
| Google "signature" thinking problems | Light | ⚠️ add 489 (Robot Room Cleaner), 715 (Range Module), 1146 (Snapshot Array), 759 (Employee Free Time), 681 (Next Closest Time), 359 (Logger Rate Limiter), 904 (Fruit Baskets), 388 (Longest File Path) |

### 1.3 Technical debt in `problems.json` worth flagging now

The `section` field is fragmented because it was populated incrementally:
- "Sliding Window — 5", "Sliding Window — 4", "Sliding Window — 1" all exist as separate groups
- Same for Binary Search (— 4, — 5, — 1), Stack (— 5, — 2, — 1), Trees & BST (— 8, — 6), Graphs (— 10, — 8, — 2), Heaps (— 5, — 1, — 2), Dynamic Programming (— 14, — 8, — 3), Backtracking (— 5, — 3), Greedy (— 2, — 3, — 2), Tries (— 1, — 2, — 1), Bit Manipulation (— 1, — 4, — 1), Arrays (— 7, — 1)

The dashboard renders one collapsible group per *distinct* `section` string, so today the same topic appears multiple times in the sidebar. This is independent of the integration choice but is best fixed *during* the merge.

---

## 2. Goals

- **G1:** A single comprehensive list (~190 problems) exists that covers every pattern in §1.2 marked ⚠️ or ❌, with at least one canonical problem per pattern.
- **G2:** Every problem carries the existing `problems.json` schema (so dashboard + lesson scaffolding keep working unchanged).
- **G3:** `status` and `lesson_status` for the 153 existing problems are preserved verbatim (no progress lost).
- **G4:** Section names are normalised — exactly one `section` string per topic/pattern. Old `"Sliding Window — 5"` / `"Sliding Window — 4"` collapse to one `"Sliding Window"` (or similar canonical form).
- **G5:** The chosen integration approach (Option A, see §4.4) is implemented end-to-end and the dashboard renders the comprehensive list correctly.
- **G6:** `problems/google_focused_reduced_dsa_sheet.md` is regenerated from the merged data (or explicitly deprecated with a pointer) so the two sources can't drift again.
- **G7 (critical):** Within every section, problems are ordered as a **gradual difficulty ramp** — easy primer → medium core → medium-hard synthesis → hard capstone. Each problem after the first should introduce *one* new twist (not three), so the learner builds confidence step by step. This is the single most important property of the list and supersedes any other ordering preference. See §4.6.

---

## 3. Non-goals

- Authoring lessons for the new problems — that is downstream of this plan, scheduled per-problem via `/batch-lesson`.
- Re-ordering or curating beyond what topic-grouping demands. The "comprehensive" list is a *coverage map*, not a study schedule. Recommended study order can be a follow-up.
- Removing problems already in `problems.json`. The list only grows.
- Building a UI to filter by "google-only" vs "comprehensive" tracks unless Integration Option C is chosen.
- Touching `LESSON_DESIGN`, the renderer pipeline, or any of the PLAN-011 efficiency work.

---

## 4. Approach

### 4.1 Phase A — Backfill the 13 google-focused-only problems

Add to `problems.json` (preserving order semantics — append at end, assign new `order` values starting at 154):

| LC# | Name | Topic | Difficulty | Section (canonical) |
|---|---|---|---|---|
| 217 | Contains Duplicate | Arrays | Easy | Arrays & Hashing |
| 125 | Valid Palindrome | Two Pointers | Easy | Two Pointers |
| 167 | Two Sum II — Input Array Is Sorted | Two Pointers | Medium | Two Pointers |
| 283 | Move Zeroes | Two Pointers | Easy | Two Pointers |
| 169 | Majority Element | Arrays | Easy | Arrays & Hashing |
| 229 | Majority Element II | Arrays | Medium | Arrays & Hashing |
| 525 | Contiguous Array | Prefix Sum | Medium | Prefix Sum |
| 560 | Subarray Sum Equals K | Prefix Sum | Medium | Prefix Sum |
| 104 | Maximum Depth of Binary Tree | Trees | Easy | Trees |
| 226 | Invert Binary Tree | Trees | Easy | Trees |
| 141 | Linked List Cycle | Linked Lists | Easy | Linked Lists |
| 496 | Next Greater Element I | Monotonic Stack | Easy | Stack & Monotonic Stack |
| 1584 | Min Cost to Connect All Points | Graphs — MST | Medium | Graphs — Advanced |

### 4.2 Phase B — Add pattern-coverage problems (the real "comprehensive" delta)

Grouped by the gap each one closes (LC# / name / pattern):

**Union-Find (formalise as named pattern):** 323 Number of Connected Components in Undirected Graph · 947 Most Stones Removed · 1319 Number of Operations to Make Network Connected.

**Bitmask DP:** 847 Shortest Path Visiting All Nodes · 698 Partition to K Equal Sum Subsets · 526 Beautiful Arrangement.

**Tree DP:** 337 House Robber III.

**Game-theory DP:** 486 Predict the Winner · 877 Stone Game.

**Segment Tree / Fenwick BIT:** 307 Range Sum Query — Mutable · 315 Count of Smaller Numbers After Self.

**Sweep line / Interval scheduling:** 252 Meeting Rooms · 253 Meeting Rooms II · 759 Employee Free Time. (Optional stretch: 218 Skyline.)

**String matching (KMP / Z):** 28 Find the Index of First Occurrence · 686 Repeated String Match.

**Reservoir / weighted random:** 380 Insert Delete GetRandom O(1) · 528 Random Pick with Weight · 382 Linked List Random Node.

**Multi-source / matrix BFS:** 542 01 Matrix · 1162 As Far from Land as Possible.

**Shortest path variants:** 1631 Path With Minimum Effort · 778 Swim in Rising Water.

**Math / number theory:** 50 Pow(x, n) · 69 Sqrt(x) · 7 Reverse Integer · 8 String to Integer (atoi) · 204 Count Primes.

**Prefix-sum on hashes:** 304 Range Sum Query 2D — Immutable · 974 Subarray Sums Divisible by K · 1248 Count Number of Nice Subarrays.

**Backtracking dedup variants & classics:** 17 Letter Combinations of a Phone Number · 40 Combination Sum II · 47 Permutations II · 90 Subsets II.

**Trie + bitmask:** 421 Maximum XOR of Two Numbers in an Array.

**Google "signature" thinking problems:** 489 Robot Room Cleaner · 715 Range Module · 1146 Snapshot Array · 681 Next Closest Time · 359 Logger Rate Limiter · 904 Fruit Into Baskets · 388 Longest Absolute File Path.

Total Phase B additions: **~38 problems**. Phase A + B together: **~51 net-new problems**, bringing `problems.json` from 153 → ~204.

### 4.3 Phase C — Normalise sections (consolidation)

Replace the existing fragmented `section` strings with a canonical set of ~16:

```
Arrays & Hashing
Two Pointers
Sliding Window
Prefix Sum
Binary Search
Stack & Monotonic Stack
Linked Lists
Trees
BST
Heaps / Priority Queue
Graphs — BFS / DFS
Graphs — Advanced     (Topo, Dijkstra, MST, Bellman-Ford, Union-Find)
Dynamic Programming
Backtracking
Greedy / Intervals
Tries
Bit Manipulation
Math
Design
Ad-hoc / Signature
```

The remapping is a `slug → new_section` lookup table applied once. `status`, `lesson_status`, `lc_num`, `slug`, `url` are untouched. The `order` field is re-assigned within each section so the dashboard's group order stays stable.

### 4.4 Phase D — Integration: **Option A (locked)**

**Decision (2026-05-16):** In-place merge into `data/problems.json`. Single file, no clutter.

- Dashboard reads it as today; no UI work.
- Lesson scaffolding (`new_lesson.py`, `server.py /api/add`) keeps working unchanged.
- The legacy markdown sheet (`problems/google_focused_reduced_dsa_sheet.md`) is regenerated from the merged JSON via §4.5 so the two sources cannot drift. A lightweight `tracks: ["google_focused"]` array on each entry tells the renderer which problems to include.
- Effort: ~2 hr for merge + ~45 min for the regeneration script.

Options B (separate file) and C (per-entry `lists` tag with dashboard filter) were considered and rejected for clutter.

### 4.5 Difficulty ramp within each section (G7 — the most important property)

Every section is a *pedagogical ramp*. The reader should be able to start at problem 1 of any section, finish it, and feel ready for problem 2 — because problem 2 introduces *one* new twist on top of what problem 1 already established. By the end of the section, the reader has accumulated all the twists needed for the hard capstone(s).

#### 4.5.1 Schema additions

Two new fields on each problem entry:

| Field | Type | Purpose |
|---|---|---|
| `tier` | `1 \| 2 \| 3` | **1 = foundational** (pattern primer, must-do first), **2 = core** (pattern in its standard form, what an interview usually asks), **3 = advanced** (synthesis, hard capstone, or rare twist). Lets the reader filter "give me just tier-1 across all patterns for a one-week refresh." |
| `ramp_pos` | integer | Position within the section's ramp, starting at 1. Sorting a section by `ramp_pos` ascending yields the intended study order. Disambiguates problems of the same `tier` + `difficulty`. |

The existing `order` field is repurposed as a flat global integer derived from `(section_order × 1000) + ramp_pos` — so sorting the JSON by `order` reproduces the section grouping *and* the within-section ramp. The dashboard already groups by `section` then sorts by `order`, so no UI change is needed; the ramp is rendered automatically.

#### 4.5.2 Ramp construction rules

Each section's ramp is built by applying these rules in order:

1. **Start with the primer** — the simplest problem that establishes the pattern's *shape* (data structure + invariant). Difficulty Easy if one exists, else the simplest Medium.
2. **Add one twist per step** — examples of a "twist": a new state variable, a constraint on movement, a duplicate-handling rule, a 2D extension of a 1D solution, a transition to a different DS to back the pattern (e.g. set → heap), a stricter optimality requirement.
3. **No flat plateaus of three identical-difficulty problems** unless each adds a genuinely distinct twist. Two M's in a row is fine; three M's that all do "sliding window with frequency map" is not — collapse to one.
4. **Hard problems go last in the section.** Exception: a hard problem that is *the primer for a pattern variant only it exposes* (e.g. 42 Trapping Rain Water as the canonical two-pointer monotone-decision problem) can sit mid-ramp if its prerequisites are met.
5. **Cross-section dependencies are noted, not enforced.** If a problem requires a pattern from another section, note it in a `prereqs: [slug]` field (optional, schema-permitted) but don't reorder sections to satisfy it — the reader picks an order across sections separately.

#### 4.5.3 Worked example — Two Pointers ramp

| ramp_pos | LC# | Name | Tier | Diff | Twist introduced |
|---|---|---|---|---|---|
| 1 | 125 | Valid Palindrome | 1 | E | Two ends converge with skip rule |
| 2 | 283 | Move Zeroes | 1 | E | Read pointer + write pointer (fast/slow) |
| 3 | 167 | Two Sum II — Sorted | 1 | M | Converge to a target sum |
| 4 | 11 | Container With Most Water | 2 | M | Decision rule for which pointer to move |
| 5 | 15 | 3Sum | 2 | M | Outer fix + two-pointer inside; dedup |
| 6 | 42 | Trapping Rain Water | 3 | H | State (max-so-far on each side) carried with the pointer |

Each step adds exactly one concept. Reader who finishes 167 is ready for 11; reader who finishes 11 is ready for 15; etc.

#### 4.5.4 Worked example — Sliding Window ramp

| ramp_pos | LC# | Name | Tier | Diff | Twist introduced |
|---|---|---|---|---|---|
| 1 | 209 | Minimum Size Subarray Sum | 1 | M | Shrink window when sum exceeds target |
| 2 | 3 | Longest Substring Without Repeating Chars | 1 | M | Set/map state inside window |
| 3 | 1004 | Max Consecutive Ones III | 2 | M | Window invariant is a count budget |
| 4 | 1493 | Longest Subarray of 1s After Deleting One | 2 | M | Same as above with k=1 — reinforces the budget formulation |
| 5 | 567 | Permutation in String | 2 | M | Fixed-size window + frequency-map equality |
| 6 | 438 | Find All Anagrams in a String | 2 | M | Same comparison, all start positions |
| 7 | 424 | Longest Repeating Character Replacement | 2 | M | Window invariant = (len − max-freq) ≤ k |
| 8 | 904 | Fruit Into Baskets | 2 | M | Two-distinct constraint (k-distinct generalisation) |
| 9 | 76 | Minimum Window Substring | 3 | H | Full state-based shrink/grow with target satisfaction |
| 10 | 239 | Sliding Window Maximum | 3 | H | Monotonic deque *inside* the window — composite pattern |

Note 1004 and 1493 sit adjacent because they reinforce the same insight rather than introducing two new ones. They're both kept because 1493's edge case (must delete at least one) is interview-relevant.

#### 4.5.5 Operational implication

The seed file (task 3 in §5) is **not** "a flat list of additions" — it is a fully ordered ramp per section, with `tier` and `ramp_pos` assigned. The merge script does no ordering of its own; it just emits the seed in the prescribed order.

This means the analytic work to build the ramps (one per ~16 sections) is the bulk of effort in this plan — roughly 2–3 hr of careful curation. Tooling is trivial; curation is the value.

---

### 4.6 Phase E — Regenerate `google_focused_reduced_dsa_sheet.md` from data

Whichever option above is picked, the legacy markdown sheet is regenerated from the JSON via a script (`scripts/render_problem_sheet.py`) so the two sources cannot drift. Each problem entry can carry a `tracks` array (e.g. `["google_focused"]`) and the script filters on it. If Option A is picked, `tracks` is the lightweight tagging mechanism that gives us the regeneration without going full Option C.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | **Curate ramps per section** — for each of the ~16 canonical sections in §4.3, produce an ordered list of (lc_num, name, tier, ramp_pos, twist-introduced) following the rules in §4.5.2. Inputs: existing §4.1 + §4.2 problems plus everything already in `problems.json` belonging to that section. Output: `scripts/seeds/comprehensive_seed.yaml` (or `.json`). **This is the bulk of plan-execution effort.** | 3 hr | — |
| 2 | Walk the seed with the user, section by section, to lock the ramps. Two checkpoints minimum: (a) after Arrays/Two Pointers/Sliding Window/Binary Search/Stack/Linked Lists/Trees, (b) after the rest. Adjust on feedback. | 1 hr | 1 |
| 3 | Write `scripts/build_comprehensive_list.py` — one-shot merge that reads the seed, joins against current `problems.json` (key = `slug` fallback `lc_num`) to preserve `status` + `lesson_status`, applies §4.3 section normalisation, assigns `tier` + `ramp_pos` + recomputed `order = section_order × 1000 + ramp_pos`, adds `tracks: ["google_focused"]` to the relevant entries, writes a new `data/problems.json`. Emits a diff report (problems preserved / added / re-sectioned). | 1.5 hr | 2 |
| 4 | Back up `data/problems.json` to `data/problems.json.bak-2026-05-16`. Run merge. Review the diff report. Smoke-test dashboard: every section renders, every existing `status` value preserved, ramps render in the right order. | 45 min | 3 |
| 5 | Verify `scripts/server.py /api/add` still works (POST adds an Ad-hoc entry with the new schema fields defaulted to `tier=2, ramp_pos=999`). Patch defaults if needed. | 30 min | 4 |
| 6 | Write `scripts/render_problem_sheet.py` — regenerates `problems/google_focused_reduced_dsa_sheet.md` from the JSON, filtered on `tracks` containing `google_focused`, grouped by canonical section, ramps preserved. | 45 min | 4 |
| 7 | Regenerate the markdown sheet. Add a banner line at the top: *"Auto-generated from `data/problems.json`. Edit there, not here."* | 15 min | 6 |
| 8 | Update `AGENT_MD/plan/current_state_report.md` and write `AGENT_MD/plan/reports/REPORT-012_comprehensive_problem_list.md` summarising what landed. | 30 min | 7 |

Total estimated effort: **~8 hr**, of which **~4 hr is curation** (tasks 1+2) — the analytical core that determines whether the list is good.

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Losing `status` / `lesson_status` progress during merge | Medium | High | Merge script keys by `slug` (fallback `lc_num`); writes a diff report ("153 preserved, 51 added") before overwriting; backup `problems.json` first |
| Section renaming breaks existing lesson scaffolding | Low | Low | `section` is metadata only; `new_lesson.py` and the lesson HTML never read it back |
| Curated section name disagreement (e.g. is "Prefix Sum" its own section or a subtopic of "Arrays & Hashing"?) | Medium | Low | Decision made at task 3; documented in seed file |
| Dashboard toggle (Options B/C) introduces UI regressions | Medium | Medium | Option A avoids this; if B/C chosen, exercise filter combinations manually before commit |
| Newly added problems have inconsistent slugs vs LeetCode URLs (esp. for the ★ NeetCode-only ones already in JSON like 269, 261, 286) | Low | Low | Use LeetCode URL slug for problems with LC URL; mark NeetCode-only entries explicitly with `source: "neetcode"` |
| List grows unwieldy (~200) and dilutes focus | Medium | Medium | The list is a *coverage map*, not a study queue. Recommended study order (smaller curated tracks) can layer on top via Option C's `lists` tag (e.g. add a `must_do_first_50` track later) |
| `problems.json` becomes hard to edit by hand | Low | Low | Once seeded, edits flow through dashboard's `/api/add` and via `scripts/build_comprehensive_list.py` re-runs |

---

## 7. Success criteria

- [ ] G1 — All ⚠️/❌ patterns in §1.2 have ≥1 canonical problem in the merged list
- [ ] G2 — Dashboard renders the merged list with no errors; existing `/api/add` still works
- [ ] G3 — Diff report shows all 153 prior `status`/`lesson_status` values preserved
- [ ] G4 — `section` field has ≤20 distinct values (down from current 35+)
- [ ] G5 — Option A ships end-to-end: `data/problems.json` is the single source, dashboard untouched
- [ ] G6 — `google_focused_reduced_dsa_sheet.md` is regenerated from data and matches the original ±the merge additions
- [ ] G7 — Every section reads as a difficulty ramp; user signs off on the ramps in task 2's checkpoints
- [ ] `tier` and `ramp_pos` fields populated on every entry (defaults `tier=2, ramp_pos=999` only for ad-hoc legacy entries that don't fit a curated ramp — visible in the dashboard as "uncurated")
- [ ] `REPORT-012` written, `current_state_report.md` updated

---

## 8. Decisions (resolved 2026-05-16)

1. **Integration approach:** **Option A** — in-place merge into `data/problems.json`. No new files, no UI work.
2. **Google "signature" problems (489, 715, 1146, 681, 359, 904, 388):** **all 7 included**, placed in section "Ad-hoc / Signature" or distributed into their natural pattern sections (e.g. 489 → Backtracking, 715 → Design, 1146 → Binary Search, 904 → Sliding Window). Distribution decided per problem during ramp curation.
3. **218 Skyline Problem:** **kept** in Greedy / Intervals (or its own "Sweep Line" sub-grouping under that section).
4. **Concurrency / OS-style problems:** **out of scope.** Not added.
5. **Difficulty ramp + tier:** **yes, central to the plan.** Schema gets `tier: 1|2|3` and `ramp_pos: int`; within-section ordering follows §4.5 rules. This is G7 and the primary acceptance criterion.

---

## 9. References

- `problems/google_focused_reduced_dsa_sheet.md` — source list 1
- `data/problems.json` — source list 2 (and dashboard backend)
- `dashboard/index.html` — reads `data/problems.json` directly via fetch
- `scripts/server.py` — `/api/add` writes to `data/problems.json`
- `scripts/new_lesson.py` — scaffolds per-problem lesson dir; reads slug from `problems.json`
- `AGENT_MD/plan/plans/PLAN-009_lesson_viewer_add_problem.md` — most recent change to `/api/add` shape
