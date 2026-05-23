# REPORT-012: Comprehensive Interview-Coverage Problem List

**Plan:** PLAN-012
**Completed:** 2026-05-16
**Author:** Claude (Opus 4.7) under user direction

---

## 1. Summary

Merged the legacy `problems/google_focused_reduced_dsa_sheet.md` (86 unique problems) and the dashboard-backed `data/problems.json` (153 problems) into a single comprehensive list of **210 problems** covering every pattern catalogued in PLAN-012 §1.2 (Union-Find as a named track, Bitmask DP, Segment Tree/BIT, sweep-line, KMP, reservoir sampling, Tree DP, Game-theory DP, multi-source BFS, Math, plus seven Google "signature" problems distributed into their natural pattern sections). The merged list ships as a single `data/problems.json` (Option A from PLAN-012 §4.4); no dashboard UI work was required. Two new schema fields — `tier` (1=foundational / 2=core / 3=advanced) and `ramp_pos` (within-section position) — encode the central design property: **every section reads as a difficulty ramp where each problem after the first introduces one new twist** (PLAN-012 §4.5, G7). The legacy markdown sheet is now regenerated from the JSON via `scripts/render_problem_sheet.py`, so the two sources cannot drift again.

## 2. Goals vs. actuals

| Goal (from plan §2) | Outcome | Evidence |
|---|---|---|
| G1 — All ⚠️/❌ patterns in §1.2 have ≥1 canonical problem | ✅ Met | Union-Find: 323/547/684/261/1319/721/947. Bitmask DP: 698/526/847. Segment Tree/BIT: 307/315. Sweep-line: 252/253/759/218. KMP: 28/459/686. Reservoir/weighted random: 380/382/528. Tree DP: 337/124. Game theory: 486/877. Multi-source BFS: 994/542/286/1162. Math: 50/69/7/8/204. |
| G2 — Dashboard renders cleanly; `/api/add` still works | ✅ Met | Smoke-tested server boot on port 8765; `/dashboard/` returns 200; `data/problems.json` serves 210 entries with all new schema fields populated. `/api/add` patched to default `tier=2, ramp_pos=999, twist="", tracks=[]`. |
| G3 — All prior `status`/`lesson_status` preserved | ✅ Met | Diff verification: 40 `status=done` preserved (identical), 10 `lesson_status=generated` preserved (identical), 0 mismatches or drops across 152 unique prior keys. |
| G4 — `section` field ≤ 20 distinct values | ✅ Met | Exactly 20 canonical sections (down from 35+ fragmented entries like "Sliding Window — 5", "— 4", "— 1"). |
| G5 — Option A ships end-to-end | ✅ Met | `data/problems.json` is the single source. Dashboard, `/api/add`, `new_lesson.py` all work unmodified. No new files served. |
| G6 — `google_focused_reduced_dsa_sheet.md` regenerated | ✅ Met | New file (16.8 KB) auto-generated from JSON; banner directs editors to the source. 88 problems carry `tracks: ["google_focused"]` (matches the original sheet's coverage plus 2 problems that were correctly deduped vs the original's cross-section repetition). |
| G7 — Every section is a difficulty ramp | ✅ Met (curated) | 20 sections, each ordered easy primer → medium core → hard capstone via `tier` + `ramp_pos`. Each problem carries a `twist` field naming the one new concept it introduces. Worked examples for Two Pointers and Sliding Window in PLAN-012 §4.5.3/§4.5.4. |
| `REPORT-012` written + `current_state_report.md` updated | ✅ Met | This file + entry added to `current_state_report.md`. |

## 3. Changes made

### 3.1 New files

| Path | Purpose |
|---|---|
| `scripts/seeds/comprehensive_seed.yaml` | 499-line single source of truth for all 210 problems, organised as ordered ramps per section with per-problem `tier`, `ramp_pos`, `twist`, and `tracks` annotations. |
| `scripts/build_comprehensive_list.py` | Merge script. Reads seed + existing `problems.json`, preserves `status`/`lesson_status` by slug-key, applies canonical section names, computes `order = section_order × 1000 + ramp_pos`. Emits a diff report; refuses to drop orphans without `--keep-orphans` or `--force`. |
| `scripts/render_problem_sheet.py` | Markdown regenerator. `--track google_focused` (default) writes `problems/google_focused_reduced_dsa_sheet.md`; `--all` writes `problems/comprehensive_dsa_sheet.md`. |
| `problems/comprehensive_dsa_sheet.md` | New 37 KB sheet covering the full 210-problem list. |
| `AGENT_MD/plan/plans/PLAN-012_comprehensive_problem_list.md` | The plan this report addresses. |
| `AGENT_MD/plan/reports/REPORT-012_comprehensive_problem_list.md` | This report. |

### 3.2 Modified files

| Path | Change |
|---|---|
| `data/problems.json` | Overwritten with 210 entries (was 153). All entries now carry `tier`, `ramp_pos`, `twist`, `tracks`. `section` values normalised to 20 canonical titles. `topic` aligned to section. `order` recomputed to encode (section_order, ramp_pos). Prior file backed up to `data/problems.json.bak-20260516-180525`. |
| `scripts/server.py` | `/api/add` patched to default the new schema fields (`tier=2, ramp_pos=999, twist="", tracks=[]`) so ad-hoc additions remain compatible with the dashboard. |
| `problems/google_focused_reduced_dsa_sheet.md` | Regenerated from `data/problems.json` filtered on `tracks: ["google_focused"]`. Top-of-file banner directs editors to the JSON source. Tables now carry `Difficulty`, `Tier`, and `Twist` columns (in addition to LC #, Problem, Link). |

### 3.3 Schema additions to `data/problems.json`

```jsonc
{
  // ... existing fields ...
  "tier": 1,                  // 1=foundational, 2=core, 3=advanced
  "ramp_pos": 1,              // 1-indexed position in this section's ramp
  "twist": "set membership — the primer for using a hash structure",
  "tracks": ["google_focused"]
}
```

The dashboard does not currently render any of these new fields, but it does not break on their presence (HTTP 200, all 210 rows rendered, filters unchanged).

## 4. Per-section counts

| § | Section | Count | `google_focused`-tagged |
|---|---|---|---|
| 1 | Arrays & Hashing | 13 | 7 |
| 2 | Two Pointers | 6 | 6 |
| 3 | Sliding Window | 10 | 6 |
| 4 | Prefix Sum *(new)* | 5 | 2 |
| 5 | Binary Search | 10 | 6 |
| 6 | Stack & Monotonic Stack | 9 | 6 |
| 7 | Linked Lists | 9 | 6 |
| 8 | Trees | 13 | 7 |
| 9 | BST | 5 | 3 |
| 10 | Heaps / Priority Queue | 9 | 4 |
| 11 | Graphs — BFS / DFS | 13 | 5 |
| 12 | Graphs — Advanced *(topo, DSU, Dijkstra, MST, bitmask BFS)* | 17 | 5 |
| 13 | Dynamic Programming | 32 | 13 |
| 14 | Backtracking | 12 | 5 |
| 15 | Greedy / Intervals *(incl. sweep-line)* | 14 | 4 |
| 16 | Tries | 5 | 3 |
| 17 | Bit Manipulation | 6 | 0 |
| 18 | Math *(new — Pow, Sqrt, atoi, sieve, etc.)* | 7 | 0 |
| 19 | String Matching *(new — strStr/KMP, 459, 686)* | 3 | 0 |
| 20 | Design | 12 | 0 |
| | **TOTAL** | **210** | **88** |

## 5. Status preservation diff

| Metric | Before (153 entries) | After (210 entries) | Delta |
|---|---|---|---|
| `status=done` | 40 | 40 | 0 |
| `status=new` | 113 | 170 | +57 (new additions default to `new`) |
| `lesson_status=generated` | 10 | 10 | 0 |
| `lesson_status=none` | 143 | 200 | +57 |

One input duplicate was collapsed: `slug:open-the-lock` (LC 752) appeared twice in the prior JSON — once as "Open the Lock" (order 139, Graphs) and once as "Open the Lock (BFS variant)" (order 150, Design). Both had `status=new, lesson_status=none`, so the dedup was lossless.

## 6. Decisions made during checkpoints

**Checkpoint 1 (batch 1: Arrays through Trees):**
- `53 Maximum Subarray` and `152 Maximum Product Subarray` moved out of Arrays into Dynamic Programming (they ARE the Kadane primer).
- `5 Longest Palindromic Substring` moved out of Sliding Window into DP — Palindrome (not actually a sliding-window problem).
- BST split into its own §9, separate from generic Trees §8 (Tree ramp focuses on recursion patterns; BST ramp on ordered-tree invariants).
- Three structural decisions confirmed via `AskUserQuestion`: Kadane → DP (recommended); Graphs split into two sections — BFS/DFS + Advanced (recommended); Google signature problems distributed into natural pattern sections (recommended).

**Checkpoint 2 (batch 2: BST through Design):**
- New "String Matching" 3-problem section added (28 strStr / KMP, 459, 686).
- Segment Tree / BIT problems (307, 315) placed inside Design rather than getting their own micro-section, keeping total section count at 20.
- DP ramp interleaves mini-arcs A–J (Linear → Stock → Grid → Jump → Knapsack → Subsequence → Palindrome → Bitmask → Game → Hard) by escalating difficulty rather than running each cluster fully before the next.

## 7. Files NOT changed (intentional non-goals)

- `dashboard/index.html` — unchanged. The new schema fields are silently ignored by the existing renderer; `tier`/`twist` are not surfaced yet (the user can add a tier filter / twist tooltip in a follow-up if desired).
- `scripts/new_lesson.py` — unchanged. Scaffolding reads `slug`, `name`, `lc_num` only.
- `lessons/` directory — no lesson HTML/plan files touched. Lesson authoring for the 57 new problems is downstream of this plan (via `/batch-lesson <slug> ...`).
- `LESSON_DESIGN.md` and the rest of the PLAN-011 substrate — unchanged.

## 8. Risk follow-ups

- **No automated test** asserts the merge is lossless on subsequent runs. If someone edits `problems.json` by hand and then re-runs `build_comprehensive_list.py`, the seed will overwrite those edits. **Mitigation:** edits should flow through either the dashboard (`/api/add` for new problems) or the seed file (for changes to the curated 210). If the user wants a guard, add `scripts/build_comprehensive_list.py --check` (exit non-zero on diff) and wire it into a pre-commit hook in a follow-up.
- **`new_lesson.py` does not surface the `twist` field** in scaffolded plans. Could be a useful prompt hint for lesson authoring; deferred.
- **The dashboard does not yet expose `tier` as a filter.** Pure UX gap — the data is there; a one-line filter addition in `dashboard/index.html` would surface "show only tier-1 across all sections" for a fast pattern-primer pass.

## 9. References

- [PLAN-012 — Comprehensive Interview-Coverage Problem List](../plans/PLAN-012_comprehensive_problem_list.md)
- [scripts/seeds/comprehensive_seed.yaml](../../../scripts/seeds/comprehensive_seed.yaml)
- [scripts/build_comprehensive_list.py](../../../scripts/build_comprehensive_list.py)
- [scripts/render_problem_sheet.py](../../../scripts/render_problem_sheet.py)
- [data/problems.json](../../../data/problems.json)
- [problems/google_focused_reduced_dsa_sheet.md](../../../problems/google_focused_reduced_dsa_sheet.md)
- [problems/comprehensive_dsa_sheet.md](../../../problems/comprehensive_dsa_sheet.md)
