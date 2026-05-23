# REPORT-013: Canonical CS Algorithms Reference

**Plan:** PLAN-013
**Completed:** 2026-05-16
**Author:** Claude (Sonnet 4.6) under user direction

---

## 1. Summary

Implemented a 121-entry canonical CS algorithms inventory — separate from the LC problem list — covering 14 algorithm/data-structure categories from the user's MustKnowAlgorithmList.pdf (ISSC M.Sc. list, ~100 algorithms). The inventory ships as `data/algorithms.json` built from `scripts/seeds/algorithms_seed.yaml`. The dashboard gained a second tab ("Algorithms") with its own filter bar, stats, and table, while LC problem rows now show purple "related algorithm" chips and algorithm rows show blue LC problem chips. The ML/Data Mining category was excluded by user decision (PLAN-013 §8 decision 2); all other categories are present. The result is 121 entries across 14 categories, rendered clean at `http://localhost:8000/dashboard/#algorithms`.

## 2. Goals vs. actuals

| Goal (from plan §2) | Outcome | Evidence |
|---|---|---|
| G1 — All ~100 algorithms from the PDF inventoried | ✅ 121 entries across 14 categories (PDF had ~100; extras come from granular splits like SHA/AES/DES and Paxos/Raft) | `data/algorithms.json` 121 entries validated by `build_algorithms_list.py` report |
| G2 — Separate from LC problems (no mixing) | ✅ Two distinct files: `data/problems.json` (210 LC entries) and `data/algorithms.json` (121 algorithm entries). Neither file modified by the other. | Schema files are distinct; dashboard resolves cross-links at load time only |
| G3 — Tabbed dashboard (Option B: one URL, hash routing) | ✅ `#problems` / `#algorithms` hash routing; tab strip below topbar; back-button works via `hashchange` listener | `dashboard/index.html` tab strip + `switchTab()` + `initTabFromHash()` |
| G4 — Interview relevance filter; low hidden by default | ✅ Relevance pills: High+Medium active by default; Low pill inactive (adds to view when clicked) | `#af-rel` pill group with multi-select logic |
| G5 — Two kind values (algorithm / data_structure) | ✅ Kind filter pill (All / Algorithm / Data Structure); badge colours differ (blue for algo, purple for DS) | `badge-algo` / `badge-ds` CSS classes |
| G6 — Cross-linking without schema pollution | ✅ `related_lc` on algorithm entries → LC chips on algorithm rows; `slugToAlgos` index computed at dashboard load → purple chips on LC rows | `buildCrossLinkIndices()` + `xlink-chip` / `xlink-chip-lc` classes |
| G7 — Python + C++ lesson style planned | ✅ `algorithms/design/LESSON_DESIGN.md` placeholder written; `scripts/new_algorithm.py` scaffolds per-algorithm `plan.md` with full metadata and outline | Stub pointing at PLAN-014 for full spec |
| G8 — `data/algorithms.schema.json` authored | ✅ Complete JSON Schema draft-07 with all required fields, enums, and description annotations | `data/algorithms.schema.json` |
| `REPORT-013` written + `current_state_report.md` updated | ✅ | This file + entry in `current_state_report.md` |

## 3. Changes made

### 3.1 New files

| Path | Purpose |
|---|---|
| `data/algorithms.json` | 121-entry canonical algorithms inventory (built from seed) |
| `data/algorithms.schema.json` | JSON Schema draft-07 for the algorithms inventory |
| `scripts/seeds/algorithms_seed.yaml` | 1731-line seed (14 categories, ordered ramps, all metadata) |
| `scripts/build_algorithms_list.py` | Build script: seed → algorithms.json; preserves lesson_status on re-run |
| `scripts/render_algorithms_sheet.py` | Markdown sheet generator with optional `--relevance` filter |
| `scripts/new_algorithm.py` | Scaffolds `algorithms/<id>/plan.md` from algorithms.json metadata |
| `algorithms/design/LESSON_DESIGN.md` | Placeholder pointing at PLAN-014; notes differences from LC lessons |
| `algorithms/algorithms_reference.md` | Auto-generated reference sheet (all 121 entries, grouped by category) |
| `AGENT_MD/plan/plans/PLAN-013_algorithms_reference.md` | The plan this report addresses |
| `AGENT_MD/plan/reports/REPORT-013_algorithms_reference.md` | This report |

### 3.2 Modified files

| Path | Change |
|---|---|
| `dashboard/index.html` | Full rewrite: tab strip, algorithms tab (filter bar + stats + table), cross-link indices, hash routing. All existing LC problem functionality (status toggle, plan generation, add-problem modal, selection + action bar) preserved intact. |

### 3.3 Seed structure

```
scripts/seeds/algorithms_seed.yaml (1731 lines)
├── foundational       (category_order: 1)   13 entries
├── graphs             (category_order: 2)   16 entries
├── dp                 (category_order: 3)   10 entries
├── strings            (category_order: 4)    8 entries
├── computational_geometry (5)                8 entries
├── numerical_optimization  (6)               8 entries
├── data_structures_category (7)             11 entries
├── advanced_graph     (8)                    5 entries
├── cryptography       (9)                    7 entries
│   [10 — ML/Data Mining — skipped]
├── parallel_distributed (11)                 6 entries
├── miscellaneous      (12)                   8 entries
├── domain_specific    (13)                   7 entries
├── advanced_theoretical (14)                 9 entries
└── emerging           (15)                   5 entries
```

### 3.4 Dashboard algorithms tab features

- **Grouped by category**, collapsible sections (same UX as LC problems tab)
- **Columns:** Ramp#, Name + aliases + short_note + LC chips, Kind badge, Tier badge, Relevance badge, Time complexity, Lesson status
- **Filter bar:** search (name/id/aliases), category select, kind pills (All/Algorithm/Data Structure), relevance pills (multi-select: High+Medium default, Low togglable)
- **Stats bar:** total visible, high/medium/low counts, algo/DS split, lessons generated
- **Cross-links:** purple chips under LC problem names show related algorithms; blue chips under algorithm names show related LC problems — both resolved from the `related_lc` field at load time with no schema changes to `problems.json`

## 4. Per-category counts

| # | Category | Entries |
|---|---|---|
| 1 | Foundational Algorithms | 13 |
| 2 | Graph Algorithms | 16 |
| 3 | Dynamic Programming | 10 |
| 4 | String Algorithms | 8 |
| 5 | Computational Geometry | 8 |
| 6 | Numerical and Optimization | 8 |
| 7 | Data Structures | 11 |
| 8 | Advanced Graph | 5 |
| 9 | Cryptography and Security | 7 |
| 11 | Parallel and Distributed | 6 |
| 12 | Miscellaneous | 8 |
| 13 | Domain-Specific | 7 |
| 14 | Advanced Theoretical | 9 |
| 15 | Emerging Areas | 5 |
| **Total** | | **121** |

## 5. Interview relevance breakdown

| Relevance | Count |
|---|---|
| high | 35 |
| medium | 55 |
| low | 31 |

Default dashboard view (high + medium): **90 entries** visible. Low entries require toggling the "Low" pill.

## 6. Validation

- **No duplicate IDs:** verified by `python3 -c "import yaml; ..."` parse + dedup check
- **All prereq IDs resolve:** every `prereqs` entry matches an `id` within the seed (validated before writing the seed)
- **16 related_lc slugs missing from problems.json:** these are valid LC problems not in the current 210-problem list (e.g., `erect-the-fence`, `design-skiplist`, `fibonacci-number`). Build script warns; dashboard silently skips them (no chip rendered). Logged as aspirational cross-links.
- **Smoke test:** `GET /data/algorithms.json` → 200, 121 entries; `GET /dashboard/` → 200; `GET /data/problems.json` → 200, 210 entries; cross-link indices built without error.

## 7. Decisions made during PLAN-013

| Decision | Choice | Rationale |
|---|---|---|
| Dashboard layout | Option B: tabbed, one URL, hash routing | User chose — keeps one URL, no clutter |
| Which algorithms | All ~100 from PDF; low relevance hidden by default | User: "better the merrier, low ones hidden" |
| Kind split | algorithm / data_structure | User: "two kinds" |
| Lesson style | Python + C++ | User: "same as LC lessons" |
| ML category | Excluded entirely | User: "skip ML category entirely" |
| Crypto granularity | SHA/AES/DES/DH/RSA/ECC as separate entries | User chose granular over grouped |
| Emerging areas | All 5 kept (Q-learning/DQN/Grover/Shor/blockchain) with low relevance | User: "keep all, relevance: low" |

## 8. What is NOT done (intentional non-goals)

- **Algorithm lesson HTML files** — none generated yet. `scripts/new_algorithm.py` + `algorithms/design/LESSON_DESIGN.md` provide the scaffolding; actual lessons are downstream of PLAN-014.
- **PLAN-014 (algorithm lesson template)** — stubbed as a to-do in `algorithms/design/LESSON_DESIGN.md`; full spec deferred.
- **`/api/add` for algorithms** — no server endpoint; algorithms are curated via the seed file only (by design, same pattern as problems).
- **Tier filter on LC tab** — still not surfaced in the dashboard (noted as a future UX addition in REPORT-012 §8).

## 9. References

- [PLAN-013 — Algorithms Reference](../plans/PLAN-013_algorithms_reference.md)
- [scripts/seeds/algorithms_seed.yaml](../../../scripts/seeds/algorithms_seed.yaml)
- [scripts/build_algorithms_list.py](../../../scripts/build_algorithms_list.py)
- [data/algorithms.json](../../../data/algorithms.json)
- [data/algorithms.schema.json](../../../data/algorithms.schema.json)
- [dashboard/index.html](../../../dashboard/index.html)
- [algorithms/algorithms_reference.md](../../../algorithms/algorithms_reference.md)
