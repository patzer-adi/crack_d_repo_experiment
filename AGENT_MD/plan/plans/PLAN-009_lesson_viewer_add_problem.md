# PLAN-009: Lesson Viewer + Ad-Hoc Add-By-Link

**Created:** 2026-05-07
**Status:** Completed
**Addresses:** Feature 8 — round out the dashboard with a clean lesson-open link and the ability to add a problem ad-hoc by pasting a LeetCode URL.

---

## 1. Context & motivation

After PLAN-008, the dashboard (Feature 4–7) is fully functional: 150 problems listed, status toggles persist to disk, plans generated on demand, and all 8 skill files exist. Two gaps remain from the Feature 8 spec:

1. **Lesson viewer** — "Open ↗" buttons already exist for `generated`/`done` problems (added in PLAN-005), but the spec calls for a dedicated "View lesson" affordance. Current state: button is present; no UX refinement needed. This goal is already met — verified in §7 (Success criteria).

2. **Ad-hoc add-by-link** — entirely missing. The 150-problem bulk list covers the prep plan, but the user will occasionally encounter a problem outside the list (e.g., during a mock interview) and want to add it immediately without re-running the importer. The spec asks for: paste LC URL → modal collects LC#, name, difficulty, topic → appends to `data/problems.json`.

This plan delivers item 2 and formally closes item 1.

References:
- `AGENT_MD/spec.md` § FEATURE 8
- `AGENT_MD/plan/current_state_report.md` § Update 2026-05-07 [PLAN-005 through PLAN-008]
- `scripts/server.py` — existing endpoints: `PATCH /api/status`, `POST /api/write`
- `dashboard/index.html` — existing: `apiCall()`, toast, modal pattern, `applyFilters()`

---

## 2. Goals

- **G1** — `POST /api/add` endpoint in `scripts/server.py` appends a new problem object to `data/problems.json`; returns `{ ok: true, problem: {...} }` on success.
- **G2** — The endpoint validates the slug (must match `[a-z0-9-]+`, no `..`, no `/`), rejects duplicates (same slug already in the list), and rejects a non-positive or non-integer `number`.
- **G3** — `dashboard/index.html` has an "＋ Add problem" button in the filter bar that opens an "Add problem" modal.
- **G4** — The modal pre-fills the **slug** and a **name guess** from the pasted URL; user fills in **LC number**, **difficulty** (Easy/Medium/Hard dropdown), and **topic** (text input).
- **G5** — After a successful add, the new problem row appears immediately in the dashboard table (no page reload) and shows status badge "New".
- **G6** — Attempting to add a slug already in the list shows an inline error in the modal (no toast); the modal stays open for correction.
- **G7** — The "View lesson" affordance is confirmed working (existing "Open ↗" button enabled for `generated`/`done` problems) — no code change needed; documented as met.
- **G8** — `REPORT-009_lesson_viewer_add_problem.md` written and committed.

---

## 3. Non-goals

- Auto-scraping problem metadata from LeetCode.com (no outbound network from the server).
- Editing or deleting existing problem rows from the dashboard.
- Importing multiple problems in one paste operation.
- Changing the `lesson_status` field on add (always starts `new`).
- Any changes to `skills/` files or lesson generation — that is PLAN-007 territory.

---

## 4. Approach

### 4.1 Server — `POST /api/add`

Add a `do_POST` branch in `scripts/server.py` for path `/api/add` alongside the existing `/api/write`.

```python
def _handle_add(self):
    body = self._read_json_body()            # existing helper
    slug = body.get("slug", "").strip()
    number = body.get("number")
    name = body.get("name", "").strip()
    topic = body.get("topic", "").strip()
    difficulty = body.get("difficulty", "").strip()

    # Validate slug
    if not re.fullmatch(r'[a-z0-9-]+', slug):
        return self._send_json({"ok": False, "error": "Invalid slug"}, 400)
    # Validate difficulty
    if difficulty not in ("Easy", "Medium", "Hard"):
        return self._send_json({"ok": False, "error": "Invalid difficulty"}, 400)
    # Validate number
    if not isinstance(number, int) or number <= 0:
        return self._send_json({"ok": False, "error": "Invalid number"}, 400)

    with _lock:
        data = json.loads(PROBLEMS_JSON.read_text())
        problems = data["problems"]
        if any(p["slug"] == slug for p in problems):
            return self._send_json({"ok": False, "error": "Duplicate slug"}, 409)
        new_order = max(p["order"] for p in problems) + 1
        new_problem = {
            "order": new_order, "number": number, "name": name,
            "slug": slug, "url": f"https://leetcode.com/problems/{slug}/",
            "topic": topic, "difficulty": difficulty,
            "status": "new", "lesson_status": "new"
        }
        problems.append(new_problem)
        PROBLEMS_JSON.write_text(json.dumps(data, indent=2))
    self._send_json({"ok": True, "problem": new_problem})
```

`_read_json_body()` is a small private method that reads `Content-Length` bytes and parses JSON — identical to how `_handle_status` and `_handle_write` already work. If it already exists as a shared helper, use it directly; if not, extract it once as part of this task (touch only what is needed).

### 4.2 Dashboard — modal and wiring

Add a minimal "Add problem" modal alongside the existing Generate-plan modal. Reuse existing CSS classes (`.modal-overlay`, `.modal`) — no new styles needed beyond one `.add-modal` override for width if needed.

**URL parsing (client-side):**
```javascript
function parseLC(url) {
    const m = url.match(/leetcode\.com\/problems\/([a-z0-9-]+)/);
    return m ? m[1] : null;
}
function slugToName(slug) {
    return slug.split('-').map(w => w[0].toUpperCase() + w.slice(1)).join(' ');
}
```

**Modal fields:**
- URL input (paste here → auto-populate slug + name)
- Name text input (pre-filled, editable)
- LC number input (number, required)
- Topic text input (required)
- Difficulty select: Easy / Medium / Hard
- Inline error `<p class="add-error">` (empty by default, filled on validation failure)

**After success:**
- Push `result.problem` into the in-memory `PROBLEMS` array.
- Call `applyFilters()` to re-render the table.
- Close modal, show toast "Problem added".

**Button placement:** in the filter bar row (`#filter-bar`), after the existing filter controls. One `<button id="btn-add">＋ Add problem</button>`.

### 4.3 No changes to lesson_status logic

The "View lesson" button already works: `buildRow()` renders an "Open ↗" `<a>` when `p.lesson_status === 'generated' || p.lesson_status === 'done'`. This satisfies G7 without any code change.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Read `scripts/server.py` in full; extract `_read_json_body()` helper if body-reading is duplicated, then add `POST /api/add` branch with validation | 20 min | — |
| 2 | Add `parseLC()` + `slugToName()` helpers and "＋ Add problem" button to `dashboard/index.html` filter bar | 10 min | — |
| 3 | Add Add-problem modal HTML + `openAddModal()` / `closeAddModal()` / `submitAdd()` functions; wire URL input to auto-fill slug + name | 25 min | 2 |
| 4 | Wire `submitAdd()` to `apiCall('POST', '/api/add', ...)`, handle success (push to PROBLEMS, re-render), handle error (show inline error) | 15 min | 1, 3 |
| 5 | Manual smoke test: add a new problem, verify row appears; add duplicate, verify inline error; verify `data/problems.json` persists across page reload | 10 min | 4 |
| 6 | Verify G7: open a generated lesson (3Sum or CWMW) from dashboard; confirm "Open ↗" works; no code change if it does | 5 min | — |
| 7 | Write `REPORT-009_lesson_viewer_add_problem.md`; commit all changes | 10 min | 5, 6 |

**Total estimate: ~95 min**

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `_read_json_body()` does not exist as a shared helper in server.py — body-reading is inlined per handler | Med | Low | Extract it once (3 lines); this is a surgical addition, not a refactor |
| Modal CSS conflicts with existing Generate-plan modal if both are open simultaneously | Low | Low | Only one modal can be open at a time; reuse same overlay `hidden`/`visible` toggle pattern |
| `PROBLEMS` in-memory array is undefined at module scope if dashboard was refactored | Low | Low | Read `dashboard/index.html` before editing to confirm array name and scope |
| User pastes a non-standard LC URL (e.g., `/submissions/`) — `parseLC()` returns null | Med | Low | Slug field stays empty; submit button disabled until slug is non-empty — client-side guard |

---

## 7. Success criteria

The plan is fully implemented when all of the following pass:

| Criterion | Verifies |
|-----------|----------|
| `curl -s -X POST localhost:8000/api/add -H 'Content-Type: application/json' -d '{"slug":"climbing-stairs","number":70,"name":"Climbing Stairs","topic":"Dynamic Programming","difficulty":"Easy"}' \| python3 -m json.tool` returns `"ok": true` | G1 |
| Same curl a second time returns `"ok": false` with `"error": "Duplicate slug"` | G2, G6 |
| `grep climbing-stairs data/problems.json` shows the new entry | G1 |
| `http://localhost:8000/dashboard/index.html` shows "＋ Add problem" button; clicking it opens the modal | G3 |
| Pasting `https://leetcode.com/problems/climbing-stairs/` auto-fills slug + name | G4 |
| After submit, "Climbing Stairs" row appears in the table without page reload | G5 |
| Adding the same slug again shows inline error in the modal (modal stays open) | G6 |
| Clicking "Open ↗" on the 3Sum row opens `lessons/3sum/lesson.html` | G7 |
| `REPORT-009_lesson_viewer_add_problem.md` exists and `git log --oneline -1` shows the commit | G8 |

---

## 8. References

- `AGENT_MD/spec.md` § FEATURE 8
- `scripts/server.py` — current endpoints for pattern reference
- `dashboard/index.html` — `apiCall()`, `showToast()`, modal pattern, `applyFilters()`, `PROBLEMS` array
- `data/problems.json` — target file for appending
- `AGENT_MD/plan/rules.md` — authoring conventions
