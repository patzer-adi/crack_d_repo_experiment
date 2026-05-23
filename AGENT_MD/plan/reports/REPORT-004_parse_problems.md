# REPORT-004: Parse HTML Problem List → JSON

**Plan:** PLAN-004
**Completed:** 2026-05-07
**Author:** Claude Sonnet 4.6 (AI agent)

---

## 1. Summary

Implemented `scripts/import_problems.py` using Python stdlib `html.parser`. The script parses `problems/finalrepList.HTML` and writes `data/problems.json` — a 150-element JSON array with 9 fields per problem. All PLAN-004 goals G1–G8 are met.

One structural discovery required a fix during implementation: the problem list is split across **three separate `<table>` elements** (one per difficulty tier), not a single table with one `<tbody>`. The initial parser only handled the first `<tbody>` and produced 75 problems. The fix was to detect problem tables by the absence of a `class` attribute on `<table>` (schedule tables use `class="dtable"`) and accumulate rows across all three.

---

## 2. Goals vs. actuals

| Goal (from plan) | Outcome | Evidence |
|---|---|---|
| G1 — `scripts/import_problems.py` runs with no deps beyond stdlib | ✅ Met | `python3 scripts/import_problems.py` exits 0; imports: `json`, `os`, `re`, `sys`, `html.parser`, `html.unescape` only |
| G2 — `data/problems.json` is a valid JSON array of exactly 150 objects | ✅ Met | Script output: "Parsed 150 problems." |
| G3 — Slug derived from LeetCode URL, not name | ✅ Met | LC#15 → `"3sum"`, LC#11 → `"container-with-most-water"` (from `/problems/<slug>/` URL path) |
| G4 — `lesson_status: "generated"` for slugs with `lessons/` dir | ✅ Met | LC#15 and LC#11 → `"generated"`; all others → `"none"` |
| G5 — `status: "done"` / `"new"` from HTML | ✅ Met | 37 done, 113 new — matches `grep -c 'badge done'` / `'badge new'` in source HTML |
| G6 — Each problem has a `section` field from preceding banner | ✅ Met | 36 distinct section strings, all non-empty; e.g. `"Arrays & Two Pointers — 7"` |
| G7 — Script is idempotent | ✅ Met | Second run output byte-identical to first: `diff` showed no differences |
| G8 — Summary line printed; exits 1 if count ≠ 150 | ✅ Met | Prints done/new/generated counts; tested exit-code path during debugging |

---

## 3. Changes made

### 3.1 New files

| File | Description |
|---|---|
| `scripts/import_problems.py` | 112-line parser; `HTMLParser` subclass with table-scoping, section tracking, and `lesson_status` auto-detection |
| `data/problems.json` | 150-problem JSON array; 1994 lines with 2-space indent |

### 3.2 Key implementation decisions

**Table detection by class absence** — the HTML contains five `<table>` tags: three problem tables (no class) and two schedule tables (`class="dtable"`). The parser sets `_in_problem_table = True` only on `<table>` tags with no `class` attribute, and scopes all row parsing inside `<tbody>` to that flag. This is simpler than inspecting `<thead>` content and robust to column-order changes.

**Section banner tracking** — `<tr class="sec">` rows carry the section banner text (e.g. `"Arrays & Two Pointers — 7"`). The parser captures the text and stores it in `_section`; each subsequent problem row inherits the most-recently-seen value. HTML entities in section names (`&amp;`) are decoded via `html.unescape`.

**Column assignment** — columns 0–3 are handled in `</td>` (plain text extraction). Columns 4–5 (difficulty, status) are handled in `</span>` because the values live inside nested `<span>` elements; the outer `</td>` handler leaves those columns alone.

**Done/new detection** — `status` is determined from `<tr class="done-row">` on the row itself, not from the badge text (which would require string matching on "✓ Done"). This is more reliable and matches the HTML design intent.

---

## 4. Testing & validation

| Check | Result |
|---|---|
| Total parsed = 150 | ✅ Script output confirmed |
| done = 37, new = 113 | ✅ Matches `grep -c 'class="badge done"'` = 37 and `'class="badge new"'` = 113 |
| LC#15 slug = `"3sum"`, lesson_status = `"generated"` | ✅ Spot-checked in Python |
| LC#11 slug = `"container-with-most-water"`, lesson_status = `"generated"` | ✅ Spot-checked in Python |
| First entry: order=1, lc_num=1, name="Two Sum", slug="two-sum" | ✅ Correct |
| Last entry: order=150, lc_num=752, name="Open the Lock" | ✅ Correct |
| 36 distinct non-empty section strings | ✅ All present; HTML entities decoded |
| Second run byte-identical (`diff` clean) | ✅ Idempotency confirmed |
| Script exits 0 on success | ✅ Confirmed |

---

## 5. Known issues & follow-ups

- **Section name duplicates** — some section labels appear more than once in the HTML (e.g. `"Arrays — 7"` appears in Tier 1 and a different tier may have a different count suffix). Each problem correctly carries the banner text immediately preceding it, so the `section` field is accurate per-problem, but grouping by `section` alone is not unique. If the dashboard needs unique grouping, it should combine `section` + tier or use `topic` instead.
- **Schedule table rows** — there are `<tr>` rows in `class="dtable"` tables (study schedule) that the parser correctly skips. No action needed, but the file contains ~90 additional rows beyond the 150 problems.
- **`data/problems.json` committed to git** — this is intentional for the POC phase; the file is small (1994 lines) and useful as a stable snapshot. When the dashboard and lesson generation tooling stabilise, it may be regenerated on demand rather than committed.

---

## 6. Metrics

| Metric | Value |
|---|---|
| Script lines | 112 |
| Problems parsed | 150 |
| Done / New | 37 / 113 |
| Lesson status: generated | 2 (3sum, container-with-most-water) |
| Distinct sections | 36 |
| JSON file size | 1994 lines, ~58 KB |
| stdlib dependencies | `html.parser`, `json`, `os`, `re`, `sys` |
| Third-party deps | 0 |
| Debugging iterations | 2 (initial 75-problem parse → discovered 3-table split → fixed) |

---

## 7. Lessons learned

- **Inspect the HTML structure before writing the parser.** The three-table split was immediately visible in `grep -n "<tbody>\|<table"` output. Running that check before coding would have saved one debugging iteration.
- **Table class absence as a positive signal** — rather than whitelisting the problem table by position (first, second, third), detecting it by the absence of `class="dtable"` is more robust: it works regardless of table ordering and doesn't require a counter.
- **Column assignment in `</td>` vs `</span>`** — mixing end-tag handlers for different columns (0–3 in `</td>`, 4–5 in `</span>`) is slightly asymmetric but correct given the HTML structure. A comment in the code flags this so future maintainers don't inadvertently handle col 4/5 twice.
- **Next session:** PLAN-005 — Dashboard skeleton: `dashboard/index.html` reads `data/problems.json` and renders a filterable problem grid.
