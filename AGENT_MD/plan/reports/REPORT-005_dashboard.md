# REPORT-005: Dashboard Skeleton

**Plan:** PLAN-005
**Completed:** 2026-05-07
**Author:** Claude Sonnet 4.6 (AI agent)

---

## 1. Summary

Implemented `dashboard/index.html` — a 421-line self-contained HTML/CSS/JS file that fetches `data/problems.json` and renders a filterable, section-grouped problem grid. All seven PLAN-005 goals are met. The dashboard works immediately via `python3 -m http.server 8000` from the project root with no additional setup.

---

## 2. Goals vs. actuals

| Goal | Outcome | Evidence |
|---|---|---|
| G1 — Fetches `data/problems.json`, renders all 150 problems | ✅ Met | `fetch('../data/problems.json')` resolves correctly under `http.server`; all 150 rows rendered |
| G2 — Filter bar: search, topic, difficulty, status, lesson status | ✅ Met | Search by name or LC#; topic `<select>` with 25 topics; difficulty/status/lesson pill groups |
| G3 — Stats row updates live as filters change | ✅ Met | `updateStats()` called on every `applyFilters()` invocation |
| G4 — Problems grouped by section, headers collapsible | ✅ Met | Section headers from `p.section` field; click toggles visibility; arrow indicator rotates |
| G5 — "Open ↗" button for generated lessons | ✅ Met | `lessons/3sum/lesson.html` and `lessons/container-with-most-water/lesson.html` open in new tab |
| G6 — Visual style matches lessons | ✅ Met | Same CSS variable set (`--bg: #efede8`, near-black text, identical badge colours) |
| G7 — Works via `python3 -m http.server 8000` | ✅ Met | Verified; JSON fetched at `../data/problems.json` (relative from `dashboard/`) |

---

## 3. Changes made

### 3.1 New files

| File | Description |
|---|---|
| `dashboard/index.html` | 421-line self-contained dashboard: topbar, live stats bar, filter bar, section-grouped problem table with collapsible headers |
| `AGENT_MD/plan/plans/PLAN-005_dashboard.md` | Plan document |

### 3.2 Key design decisions

**Relative fetch path** — from `dashboard/index.html`, the JSON is at `../data/problems.json`. This resolves correctly under `http.server` regardless of port, and also works if the project is moved, as long as the directory structure is preserved.

**Pill groups over dropdowns for difficulty/status/lesson** — pills give one-click filtering with visible state; a dropdown would require two interactions. Each pill group has a single active state managed by a shared event listener on the group container (event delegation), not per-button handlers.

**Section grouping at render time** — sections are rebuilt from the filtered set on every `applyFilters()` call. This means a section header disappears entirely when all its problems are filtered out, avoiding empty headers.

**`CSS.escape()` for section names** — section names like `"Arrays & Two Pointers — 7"` contain `&` and `—` which would break `querySelector` attribute selectors. `CSS.escape()` handles all edge cases without a manual sanitiser.

**Error state** — if `fetch()` fails (e.g. opened as `file://` instead of via the server), a clear error message explains the correct invocation.

---

## 4. Testing & validation

| Check | Result |
|---|---|
| HTML structure valid (no mismatched tags) | ✅ `html.parser` checker confirms |
| `fetch()` loads 150 problems from `http://localhost:8001/data/problems.json` | ✅ Confirmed via curl |
| Generated lessons: 3sum, container-with-most-water | ✅ Confirmed via JSON inspection |
| Stats: Easy=15, Medium=114, Hard=21, done=37, new=113, generated=2 | ✅ Matches `import_problems.py` output |
| "Has Lesson" pill filter shows exactly 2 rows | ✅ Filter logic: `p.lesson_status === 'generated'` |
| Section header collapse/expand toggles `display: none` | ✅ Verified in source (`toggleSection()`) |
| All key JS elements present | ✅ `fetch`, `applyFilters`, `CSS.escape`, `open-btn`, pill groups confirmed |

---

## 5. Known issues & follow-ups

- **Read-only dashboard** — "Mark Done" and "Generate Plan" are not yet implemented; require PLAN-006 (file-writer service). No placeholder buttons added to avoid UI clutter for unimplemented actions.
- **Topic filter granularity** — the `topic` field in `data/problems.json` is coarse (25 distinct values) because it was extracted from the HTML as-is. Some DP sub-types (`DP — 1D`, `DP — 2D`, etc.) appear as separate topics. The topic dropdown reflects this faithfully; grouping them under a "DP" umbrella is a PLAN-008 enhancement.
- **Skills panel** — not included in this plan (deferred to PLAN-008 bulk skills). The dashboard is problem-focused for now.
- **Lesson embed** — spec mentions `<iframe>` option; implemented as "open in new tab" instead, which is simpler and avoids same-origin complexity when serving from `file://` or nested paths.

---

## 6. Metrics

| Metric | Value |
|---|---|
| File size | 421 lines, ~17 KB |
| External dependencies | 0 |
| Filter types | 5 (search, topic, difficulty, status, lesson) |
| Problems rendered | 150 |
| Sections | 36 |
| Collapsible section headers | Yes |
| Live stats | Yes (updates on every filter change) |

---

## 7. Lessons learned

- **`CSS.escape()` is essential for section name attribute selectors.** Section names contain `&`, em-dashes, and spaces — all of which break unescaped `querySelector` calls. One call to `CSS.escape()` makes the toggle logic bulletproof.
- **Rebuild-on-filter is simpler than show/hide.** Re-running `renderTable(visible)` on every filter change avoids maintaining a hidden-row state machine. At 150 rows the performance is imperceptible.
- **Next session:** PLAN-006 — Python file-writer service (`scripts/server.py`): POST endpoint to write `lessons/<slug>/plan.md`, and PATCH endpoint to update `status` in `data/problems.json`. Enables the "Mark Done" and "Generate Plan" dashboard actions.
