# PLAN-005: Dashboard Skeleton

**Created:** 2026-05-07
**Status:** In-Progress
**Addresses:** Feature 4 in `AGENT_MD/spec.md` — a single `dashboard/index.html` that renders all 150 problems from `data/problems.json` with filters, stats, and direct lesson links.

---

## 1. Context & motivation

`data/problems.json` exists (PLAN-004 complete). The user now needs a visual interface to navigate the 150-problem list, see which lessons are already generated, and open them. The dashboard is read-only for now — status persistence and plan generation require PLAN-006 (file-writer) and PLAN-007 respectively.

---

## 2. Goals

- **G1:** `dashboard/index.html` fetches `data/problems.json` via `fetch()` and renders all 150 problems without page reload.
- **G2:** Filter bar: search by name, filter by topic, difficulty (All/Easy/Medium/Hard), status (All/Done/New), and lesson status (All/Generated/None).
- **G3:** Stats row shows total, done count, new count, and generated-lesson count — updated as filters change.
- **G4:** Problems grouped by section (from `section` field) with collapsible section headers.
- **G5:** Problems with `lesson_status: "generated"` show an "Open" button that opens `lessons/<slug>/lesson.html` in a new tab.
- **G6:** Visual style matches the lesson files (CSS variables: `--bg: #efede8`, near-black text, same badge colours).
- **G7:** Works via `python3 -m http.server 8000` from project root; no other server needed.

## 3. Non-goals

- No "Mark Done" persistence — requires PLAN-006 file-writer.
- No "Generate Plan" — requires PLAN-006 + PLAN-007.
- No skill file viewer — deferred to PLAN-008.
- No lesson iframe embed — open in new tab is sufficient.

## 4. Approach

Single self-contained `dashboard/index.html`. On `DOMContentLoaded`, fetch `../data/problems.json` (relative path works under `http.server`). Build the table from the JSON. Filter functions re-render the visible rows without re-fetching. Section headers are rendered as separator rows; they hide when all problems in the section are filtered out.

## 5. Task breakdown

| # | Task | Est. |
|---|------|------|
| 1 | Write `dashboard/index.html` — HTML skeleton, CSS, fetch + render logic, filters | 45 min |
| 2 | Serve and verify: `python3 -m http.server 8000`, open dashboard, check stats and filters | 10 min |
| 3 | Commit; write REPORT-005; update current_state_report | 10 min |

## 6. Success criteria

- [ ] G1–G7 above all verified manually
- [ ] Filtering by "Generated" shows exactly 2 problems (3Sum, CWMW) and opens their lesson.html correctly
- [ ] REPORT-005 written; plan status → Completed

## 7. References

- `data/problems.json` — data source
- `lessons/3sum/lesson.html`, `lessons/container-with-most-water/lesson.html` — lesson targets
- `AGENT_MD/spec.md` Feature 4 task list
