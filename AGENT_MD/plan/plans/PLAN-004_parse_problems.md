# PLAN-004: Parse HTML Problem List → JSON

**Created:** 2026-05-07
**Status:** Approved
**Addresses:** Feature 3 in `AGENT_MD/spec.md` — extract the 150-problem table from `problems/finalrepList.HTML` into `data/problems.json` so that downstream features (dashboard, plan generator, bulk lesson tooling) have a structured data source.

---

## 1. Context & motivation

The curated problem list lives in `problems/finalrepList.HTML` — a hand-crafted HTML file with a 150-row table (order#, LC#, problem name + URL, topic, difficulty, status). Every downstream feature depends on this data in a machine-readable form:

- **Dashboard (PLAN-005):** needs `lc_num`, `name`, `topic`, `difficulty`, `status`, `slug` to display the problem grid and filter by topic/difficulty.
- **Plan generator (PLAN-007):** needs `name`, `slug`, `url`, `topic`, `difficulty` to pre-populate a `lessons/<slug>/plan.md`.
- **Lesson viewer (PLAN-009):** needs `slug` to resolve `lessons/<slug>/lesson.html`.

PLAN-003 closed the POC loop. This plan creates the thin data-extraction layer that feeds everything else.

---

## 2. Goals

- **G1:** `scripts/import_problems.py` exists and runs without dependencies beyond the Python 3 standard library (`html.parser`, `json`, `os`, `re`).
- **G2:** Running `python3 scripts/import_problems.py` produces `data/problems.json` — a JSON array of 150 objects, one per problem, with the fields defined in §4.2.
- **G3:** The `slug` field is derived from the LeetCode URL (e.g. `https://leetcode.com/problems/3sum/` → `"3sum"`), **not** computed from the name — URL slugs are stable and match the problem name as LeetCode intends.
- **G4:** Problems that already have a `lessons/<slug>/` directory get `"lesson_status": "generated"`; all others get `"lesson_status": "none"`.
- **G5:** Problems marked `✓ Done` in the HTML get `"status": "done"`; all others get `"status": "new"`.
- **G6:** Section banners (`<tr class="sec">`) are parsed and each problem carries a `"section"` field with the banner text (e.g. `"Arrays & Two Pointers — 7"`), preserving the original grouping structure.
- **G7:** The script is idempotent — running it twice produces the same output with no side effects.
- **G8:** A basic validation pass at script end prints a summary: total problems parsed, `done` count, `new` count, `generated` count, and flags if the count is not 150.

---

## 3. Non-goals

- No dashboard HTML — that is PLAN-005.
- No automatic lesson generation — that is PLAN-007.
- No watch mode or file-system listener.
- No third-party libraries (no `beautifulsoup4`, `lxml`, etc.) — stdlib `html.parser` only.
- No schema validation beyond the summary check in §G8.

---

## 4. Approach

### 4.1 HTML structure of `problems/finalrepList.HTML`

The file contains a `<table>` with two row types relevant to parsing:

```html
<!-- Section banner — marks start of a topic group -->
<tr class="sec"><td colspan="6">Arrays &amp; Two Pointers — 7</td></tr>

<!-- Problem row (done) -->
<tr class="done-row">
  <td>1</td>
  <td class="num">1</td>
  <td><a href="https://leetcode.com/problems/two-sum/" target="_blank">Two Sum</a></td>
  <td class="topic">Arrays</td>
  <td><span class="badge e">Easy</span></td>
  <td><span class="badge done">✓ Done</span></td>
</tr>

<!-- Problem row (new) — same structure, no class="done-row" -->
<tr>
  <td>3</td>
  ...
  <td><span class="badge new">New</span></td>
</tr>
```

The parser must handle:
- HTML entities (`&amp;` in section names)
- Nested tags inside `<td>` (`<a>`, `<span>`)
- `class="done-row"` on `<tr>` as the done/new discriminator
- `class="sec"` on `<tr>` to identify section banners

### 4.2 Output JSON schema

`data/problems.json` — a JSON array, one object per problem, in original order (1–150):

```json
[
  {
    "order": 1,
    "lc_num": 1,
    "name": "Two Sum",
    "slug": "two-sum",
    "url": "https://leetcode.com/problems/two-sum/",
    "topic": "Arrays",
    "difficulty": "Easy",
    "status": "done",
    "lesson_status": "none",
    "section": "Arrays & Two Pointers — 7"
  },
  ...
]
```

Field definitions:

| Field | Type | Source |
|---|---|---|
| `order` | int | First `<td>` in the row (1-based, 1–150) |
| `lc_num` | int | Second `<td class="num">` |
| `name` | str | Text content of `<a>` in third `<td>` |
| `slug` | str | Path segment from the LeetCode URL (regex `problems/([^/]+)/`) |
| `url` | str | `href` attribute of `<a>` in third `<td>` |
| `topic` | str | Text content of `<td class="topic">` |
| `difficulty` | str | Text of `<span class="badge ...">` in fifth `<td>` — `"Easy"`, `"Medium"`, or `"Hard"` |
| `status` | str | `"done"` if `<tr class="done-row">`, else `"new"` |
| `lesson_status` | str | `"generated"` if `lessons/<slug>/` exists, else `"none"` |
| `section` | str | Text of most-recently-seen `<tr class="sec">` banner |

### 4.3 Implementation — `scripts/import_problems.py`

Use a single-pass `html.parser.HTMLParser` subclass. State machine tracks:
- `_in_sec` — currently inside a `<tr class="sec">` row
- `_in_row` — currently inside a `<tr class="done-row">` or regular `<tr>` problem row
- `_col` — 0-indexed column counter within the current row
- `_cur` — dict accumulating fields for the current problem row
- `_section` — most recently seen section banner text

The parser ignores `<thead>` rows by checking that `_col == 0` data matches a digit (order number).

After parsing, the script iterates over `lessons/` to set `lesson_status = "generated"` for matching slugs, then writes `data/problems.json` with `indent=2`.

### 4.4 Script location and invocation

```
scripts/import_problems.py   ← new file
data/problems.json           ← generated output (gitignored or committed)
```

Invocation from project root:
```bash
python3 scripts/import_problems.py
```

Expected terminal output:
```
Parsed 150 problems.
  done:      82
  new:       68
  generated:  2  (3sum, container-with-most-water)
Output: data/problems.json
```

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Inspect `problems/finalrepList.HTML` — confirm row structure, entity encoding, and edge cases | 5 min | — |
| 2 | Write `scripts/import_problems.py` using `html.parser` per §4.3 | 30 min | 1 |
| 3 | Run script; inspect first 5 and last 5 entries in `data/problems.json` for correctness | 5 min | 2 |
| 4 | Verify slug field: `3sum` and `container-with-most-water` have `lesson_status: "generated"` | 2 min | 3 |
| 5 | Verify total count is 150 and done/new counts look correct against the HTML visually | 5 min | 3 |
| 6 | Run script a second time — confirm output is byte-identical (idempotency G7) | 2 min | 3 |
| 7 | Commit `scripts/import_problems.py` and `data/problems.json`; write REPORT-004 | 10 min | 5 |

Total estimate: ~1 hour.

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| HTML entity encoding breaks text extraction | Medium | Low | Use `html.unescape()` on all collected text; test against section name `"Arrays &amp; Two Pointers"` |
| Some rows not matching expected column count (e.g. colspan rows) | Low | Medium | Guard `_col` with a max of 5; skip rows where `order` is not a digit |
| Slug extraction fails for non-standard LC URLs | Low | Medium | Regex `problems/([^/]+)/` is robust; fall back to `name.lower().replace(' ', '-')` with a warning |
| `data/` directory not writable | Very low | Low | Directory exists (`.gitkeep` from PLAN-001); no mkdir needed |
| Problem count ≠ 150 | Low | High | Script prints warning and exits with code 1 if count is wrong — catches partial parse early |

---

## 7. Success criteria

- [ ] **G1** — `scripts/import_problems.py` runs with `python3 scripts/import_problems.py` and exits 0.
- [ ] **G2** — `data/problems.json` is a valid JSON array of exactly 150 objects.
- [ ] **G3** — Slug for LC #15 is `"3sum"`, for LC #11 is `"container-with-most-water"` — derived from URL.
- [ ] **G4** — LC #15 (3sum) and LC #11 (CWMW) have `"lesson_status": "generated"`; others have `"none"`.
- [ ] **G5** — LC #15 and LC #11 have `"status": "done"` (per the HTML); verify at least one `"new"` entry exists.
- [ ] **G6** — Each problem has a non-empty `"section"` field matching the preceding section banner.
- [ ] **G7** — Running the script twice produces byte-identical `data/problems.json`.
- [ ] **G8** — Summary line in terminal output matches: 150 total, done + new = 150, generated count matches `ls lessons/` directory count.
- [ ] REPORT-004 written; plan status set to `Completed`.

---

## 8. References

- `problems/finalrepList.HTML` — source HTML; inspect with `head -100` to confirm structure before parsing
- `data/` — output directory (exists from PLAN-001; contains `.gitkeep`)
- `scripts/` — script directory (exists from PLAN-001; contains `.gitkeep`)
- `AGENT_MD/spec.md` — Feature 3 task list
- `AGENT_MD/plan/rules.md` — §3 plan template, §5 style rules
- `AGENT_MD/plan/reports/REPORT-003_skill_reuse_cwmw.md` — confirms POC milestone complete; PLAN-004 is unblocked
- Python docs: [`html.parser`](https://docs.python.org/3/library/html.parser.html), [`json`](https://docs.python.org/3/library/json.html)
