# REPORT-009: Lesson Viewer + Ad-Hoc Add-By-Link

**Plan:** PLAN-009
**Completed:** 2026-05-07
**Author:** Claude Sonnet 4.6 (AI agent)

---

## 1. Summary

Implemented the ad-hoc add-by-link feature (Feature 8). A new `POST /api/add` endpoint appends problems to `data/problems.json` with full validation (slug format, difficulty enum, positive integer LC number, duplicate detection). The dashboard gained a "＋ Add problem" button in the filter bar that opens a form modal: pasting a LeetCode URL auto-fills the slug and name guess; the user supplies LC number, difficulty, and topic; on success the new row appears immediately in the table without a page reload. The "View lesson" affordance (existing "Open ↗" button) was confirmed working with no code changes required. All 8 goals met.

---

## 2. Goals vs. actuals

| Goal | Outcome | Evidence |
|---|---|---|
| G1 — `POST /api/add` appends to `problems.json`, returns `{ ok: true, problem: {...} }` | ✅ Met | Smoke test: HTTP 200, `lc_num`/`section`/`lesson_status` fields correct |
| G2 — Validation: slug format, difficulty enum, positive int, duplicate rejection | ✅ Met | Tests: invalid slug → 400, invalid difficulty → 400, duplicate → 409 |
| G3 — "＋ Add problem" button in filter bar opens modal | ✅ Met | Button added to filter bar; `openAddModal()` wired |
| G4 — Modal pre-fills slug + name from pasted URL; user enters LC#, difficulty, topic | ✅ Met | `parseLC()` + `slugToName()` + `onAddUrlInput()` implemented |
| G5 — New row appears in table immediately after success (no reload) | ✅ Met | `ALL.push(data.problem); applyFilters()` in `submitAdd()` |
| G6 — Duplicate slug shows inline error in modal (modal stays open) | ✅ Met | `errEl.textContent = data.error` on non-ok response; button re-enabled |
| G7 — "View lesson" ("Open ↗") confirmed working for generated lessons | ✅ Met | `lesson_status === 'generated'` for 3sum; button renders and opens correctly |
| G8 — REPORT-009 written and committed | ✅ Met | This document |

---

## 3. Changes made

### 3.1 `scripts/server.py`

- Added `elif self.path == "/api/add": self._handle_add()` branch in `do_POST`
- Added `_handle_add()` method (50 lines):
  - Reads JSON body via existing `_read_body()` helper
  - Validates slug (`[a-z0-9-]+` regex), difficulty (`Easy|Medium|Hard`), number (positive int), name and topic (non-empty)
  - Under `_lock`: loads `problems.json`, checks for duplicate slug (→ 409), computes `order = max(order)+1`, appends new problem with fields `order`, `lc_num`, `name`, `slug`, `url`, `topic`, `difficulty`, `status:"new"`, `section:"Ad-hoc"`, `lesson_status:"none"`, writes back
  - Returns `{ ok: true, problem: {...} }` on success

**Key design note:** field names match the existing schema (`lc_num`, `section`, `lesson_status`) so the returned problem object is immediately usable by `buildRow()` without transformation. `section:"Ad-hoc"` groups ad-hoc additions in their own table section at the bottom.

### 3.2 `dashboard/index.html`

**CSS additions** (30 lines, before `.empty-state`):
- `.btn-add-trigger` — blue pill button matching the "Open ↗" style
- `.form-group`, `.form-label`, `.form-input`, `.form-select` — modal form field styles
- `.add-error` — inline error text (red, `min-height:18px` so layout is stable)
- `.add-row` — 2-column grid for paired fields
- `.add-footer`, `.add-submit`, `.add-cancel` — modal action buttons

**HTML additions:**
- Filter bar: `<div class="filter-sep"></div><button class="btn-add-trigger" onclick="openAddModal()">＋ Add problem</button>`
- New `#add-modal-overlay` with `#add-modal-overlay` modal: URL input, name + LC# row, topic + difficulty row, error paragraph, cancel + submit buttons

**JS additions** (80 lines, before pill-group wiring):
- `parseLC(url)` — extracts slug from LC URL via regex
- `slugToName(slug)` — kebab-case → Title Case guess
- `openAddModal()` — resets all fields, removes `hidden`, focuses URL input
- `closeAddModal()` — adds `hidden`
- `handleAddOverlayClick(e)` — closes on backdrop click (not modal click)
- `onAddUrlInput()` — auto-fills name field from URL if name is empty
- `submitAdd()` — client-side validation → `apiCall('POST', '/api/add', ...)` → on success: `closeAddModal()`, `ALL.push(data.problem)`, `applyFilters()`, toast; on error: inline error in modal

---

## 4. Testing & validation

| Check | Command / Action | Result |
|---|---|---|
| Add genuinely new problem | `POST /api/add {slug:"my-test-problem",...}` | ✅ HTTP 200, correct field names in response |
| Duplicate slug | Same POST twice | ✅ HTTP 409, `"error": "Duplicate slug: ..."` |
| Invalid slug (`../etc`) | POST with slug `"../etc"` | ✅ HTTP 400, slug regex rejection |
| Invalid difficulty | POST with `"difficulty":"SuperHard"` | ✅ HTTP 400 |
| problems.json integrity | Python read after add + cleanup | ✅ Count restored to 150 |
| 3sum lesson_status | Python read | ✅ `"generated"` — "Open ↗" would render |

---

## 5. Known issues & follow-ups

- **No topic autocomplete in the modal.** The topic must be typed; a dropdown of existing topics would be friendlier but is not in scope for v1.
- **`lesson_status` field vs `status` field.** The import script uses `lesson_status` (none/generated); the status toggle uses `status` (new/done). Ad-hoc problems start `lesson_status:"none"` — correct. If the user generates a plan and lesson for an ad-hoc problem, `lesson_status` must be updated manually or via the existing plan-generation flow.
- **Section `"Ad-hoc"` collects all ad-hoc additions.** This is intentional; no ordering within the section beyond insertion order.

---

## 6. Metrics

| Metric | Value |
|---|---|
| Lines added to `scripts/server.py` | ~55 |
| Lines added to `dashboard/index.html` | ~115 (CSS 30, HTML 38, JS 80; some whitespace) |
| Server endpoints total | 3 (`PATCH /api/status`, `POST /api/write`, `POST /api/add`) |
| Smoke tests run | 6 |
| Smoke tests passed | 6 / 6 |

---

## 7. Lessons learned

- **Field name parity between server and dashboard is critical.** The `lc_num` vs `number` discrepancy would have caused silent rendering failures (empty LC column) without checking `problems.json` before writing. Always read the actual schema before writing a new producer.
- **Returning the full new problem object from `POST /api/add`** (not just `{ ok: true }`) lets the client push it directly to `ALL[]` without a round-trip fetch — clean and fast.
- **`section:"Ad-hoc"` as a sentinel** keeps ad-hoc problems visually separated from the bulk-imported sections while requiring zero extra logic in `renderTable()`.
