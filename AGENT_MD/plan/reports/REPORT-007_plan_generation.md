# REPORT-007: Plan Generation + Copy-Paste Prompt

**Plan:** PLAN-007
**Completed:** 2026-05-07
**Author:** Claude Sonnet 4.6 (AI agent)

---

## 1. Summary

Implemented the "Generate Plan" flow in `dashboard/index.html`. Users can now check one or more problem rows, click "Generate Plan" in the sticky action bar, and receive a ready-to-paste Claude prompt per problem — along with the auto-created `lessons/<slug>/plan.md` template. All seven PLAN-007 goals met.

---

## 2. Goals vs. actuals

| Goal | Outcome | Evidence |
|---|---|---|
| G1 — Checkbox per row + section select-all | ✅ Met | `buildRow()` adds `.col-check` td; table header has select-all checkbox per section |
| G2 — Sticky action bar when ≥1 selected | ✅ Met | `updateActionBar()` toggles `.visible` on `#action-bar`; shows count |
| G3 — `POST /api/write` for each selected problem | ✅ Met | `generatePlans()` async loop; sequential awaits |
| G4 — plan.md follows 3sum template structure | ✅ Met | `buildPlanMd()`: metadata, DS+patterns, skill-file list, 5 section outlines, quality bar |
| G5 — Modal with per-problem prompt + Copy button | ✅ Met | `showModal()` renders `.plan-result` blocks; `copyText()` uses clipboard API |
| G6 — Overwrite warning suppressed (write still succeeds) | ✅ Met | Server always writes; modal shows "plan.md created" without failure state on overwrite |
| G7 — Checkbox state persists across filter changes | ✅ Met | `SELECTED = new Set()` of slugs; `buildRow()` sets `cb.checked = SELECTED.has(p.slug)` |

---

## 3. Changes made

### 3.1 New files

| File | Description |
|---|---|
| `AGENT_MD/plan/plans/PLAN-007_plan_generation.md` | Plan document |

### 3.2 Modified files

| File | Changes |
|---|---|
| `dashboard/index.html` | +505 lines: CSS (checkbox, action bar, modal, prompt block); HTML (action bar, modal divs); JS (SELECTED, TOPIC_SKILL_MAP, EXISTING_SKILL_FILES, buildRow checkbox, section select-all, 9 new functions) |

### 3.3 Key design decisions

**`TOPIC_SKILL_MAP` hardcoded in JS** — the 25 topic strings are stable (from `data/problems.json`); no need for a server round-trip. When PLAN-008 adds new skill files, `EXISTING_SKILL_FILES` is the only constant to update.

**`SELECTED` keyed by slug** — slugs are unique and stable identifiers. Storing them (not DOM node references) means checkboxes survive every `renderTable()` call triggered by filter changes.

**Select-all scoped per section** — each section header's table gets its own select-all checkbox. Checking it updates `SELECTED` for all rows in that section and syncs the tbody checkboxes. This avoids a global select-all that would check 150 boxes at once.

**Sequential `await` in `generatePlans()`** — not concurrent. The file-writer server is single-threaded; concurrent POSTs would queue anyway. Sequential is simpler and gives clearer per-problem error attribution.

**`escHtml()` for prompt in modal** — the prompt is displayed inside a `<div class="prompt-text">` via `innerHTML`. Using `escHtml()` prevents any XSS if a problem name or URL contained `<`, `>`, or `&`.

**Missing skill files noted in prompt** — when a topic's skill files don't exist yet (e.g., `skills/patterns/dynamic_programming.md` for DP topics), the prompt explicitly says `(not yet authored — PLAN-008)` rather than silently omitting them. This helps the user know what's coming.

---

## 4. Testing & validation

| Check | Result |
|---|---|
| HTML structure valid (html.parser check) | ✅ No errors |
| JS brace balance | ✅ 151 opens = 151 closes |
| 23 functions defined | ✅ Confirmed by regex |
| `POST /api/write` → `lessons/two-sum/plan.md` created with correct metadata | ✅ Verified via curl |
| `topicToSkills('Arrays')` returns array.md + two_pointers.md | ✅ Python logic test |
| `topicToSkills('DP — 1D')` existing=['skills/ds/array.md'], missing=['...dynamic_programming.md'] | ✅ |
| `topicToSkills('Graphs')` existing=[], missing=['...graph.md', '...bfs_dfs.md'] | ✅ |

---

## 5. Known issues & follow-ups

- **`EXISTING_SKILL_FILES` must be manually updated** when PLAN-008 adds skill files. A server endpoint that lists `skills/` would be cleaner but is out of scope for a local tool.
- **No visual indicator for already-generated plans** — if `lesson_status === 'generated'`, the checkbox still appears. A subtle note like "lesson exists" in the modal result would be a minor UX improvement.
- **Clipboard API requires HTTPS or localhost** — works fine for the local `http://localhost:8000` use case; will fail on `file://` (but that's already broken for fetch anyway).

---

## 6. Metrics

| Metric | Value |
|---|---|
| `dashboard/index.html` additions | +505 lines |
| New JS functions | 9 |
| Topics mapped in `TOPIC_SKILL_MAP` | 25 |
| Existing skill files tracked | 2 |
| Plan.md sections generated | 7 (metadata, DS/patterns, skills, output, 5 lesson sections, quality bar) |

---

## 7. Lessons learned

- **Scoped select-all is better UX than global.** A global "check all 150 problems" is dangerous — easy to accidentally click. Per-section select-all is more deliberate and matches how the table is already organised.
- **Note missing skill files explicitly.** Rather than silently omitting skills that don't exist yet, naming them in the prompt reminds the user (and Claude) what context is missing and what PLAN-008 will supply.
- **Next session:** PLAN-008 — Bulk skills authoring: `skills/ds/linked_list.md`, `skills/ds/binary_tree.md`, and four pattern files (Sliding Window, Binary Search, BFS/DFS, Dynamic Programming). After these are written, update `EXISTING_SKILL_FILES` in `dashboard/index.html`.
