# PLAN-010: Shared Static Assets — Extract CSS and JS from Golden Lessons

**Created:** 2026-05-13
**Status:** Completed
**Addresses:** Each lesson HTML contains ~180 lines of duplicated CSS and ~200 lines of duplicated shared JS; extracting them once into `static/` cuts per-lesson token cost ~60%.

---

## 1. Context & motivation

All four golden lessons (`3sum`, `permutation-in-string`, `trapping-rain-water`,
`container-with-most-water`) inline identical CSS and shared JS functions.
As of 2026-05-13 the raw sizes are:

| Lesson | Lines |
|--------|-------|
| `lessons/3sum/lesson.html` | 1002 |
| `lessons/permutation-in-string/lesson.html` | 1365 |
| `lessons/trapping-rain-water/lesson.html` | 830 |
| `lessons/container-with-most-water/lesson.html` | 869 |

Roughly 380 lines (CSS + shared JS) in each file are identical boilerplate that
have no business being regenerated for every new lesson. This plan extracts them
once into `static/lesson.css` and `static/lesson.js` and refactors all four
lessons to import those files.

## 2. Goals

- `static/lesson.css` exists and contains all shared styles extracted verbatim from `lessons/3sum/lesson.html` lines 7–188.
- `static/lesson.js` exists and contains all shared JS functions: `toggleEl`, `switchTab`, `visPx`, the `keydown` handler, `cvBuildCode(lines)`, `cvStopPlay`, `cvTogglePlay`, `drStopPlay`, `drTogglePlay`, `bfStopPlay`, `bfTogglePlay`.
- All four golden lessons replace their `<style>` block with `<link rel="stylesheet" href="../../static/lesson.css">` and replace the inline shared JS with `<script src="../../static/lesson.js"></script>`.
- Each lesson renders identically in the browser after refactoring (no visual regression).
- `lessons/LESSON_DESIGN.md` and `lessons/LESSON_DESIGN_v2.md` both document that shared assets must not be regenerated per lesson.
- New lessons created after this plan only contain problem-specific content (~400 lines vs ~1000 lines).

## 3. Non-goals

- Modifying `scripts/server.py` — it already serves the project root via `SimpleHTTPRequestHandler(directory=PROJECT_ROOT)`, so `static/` is served automatically.
- Extracting the HTML section structure into a shared template.
- Minifying or bundling the assets.
- Adding a build step or asset pipeline.

## 4. Approach

### 4.1 CSS extraction

`lessons/3sum/lesson.html` lines 7–188 contain the `<style>` block. Copy
everything between (and not including) the `<style>` and `</style>` tags verbatim
into `static/lesson.css`. Do not include any problem-specific styles (e.g.
`.bf-bar-con` bar chart rules present only in rain water).

Cross-check against the other three lessons: any selector that only appears in
one lesson stays inline in that lesson.

### 4.2 JS extraction — `cvBuildCode` signature change

In `lessons/3sum/lesson.html` `cvBuildCode` is defined at line 735 as
`function cvBuildCode()` and reads the module-level constant `CV_LINES`
directly. In the shared version this must become `function cvBuildCode(lines)`
so every lesson can pass its own `CV_LINES` array. All call sites in the four
lessons must be updated to `cvBuildCode(CV_LINES)`.

All other extracted functions (`toggleEl`, `switchTab`, `visPx`, `keydown`
handler, `cvStopPlay`, `cvTogglePlay`, `drStopPlay`, `drTogglePlay`,
`bfStopPlay`, `bfTogglePlay`) are already parameter-clean and need no signature
changes.

### 4.3 Per-lesson refactoring

For each lesson:
1. Replace the entire `<style>…</style>` block with:
   ```html
   <link rel="stylesheet" href="../../static/lesson.css">
   ```
   followed by a `<style>` block containing **only** problem-specific styles (or
   nothing, if none exist).
2. Remove the shared JS functions from the inline `<script>`.
3. Add `<script src="../../static/lesson.js"></script>` immediately before the
   problem-specific `<script>`.
4. Update any `cvBuildCode()` call to `cvBuildCode(CV_LINES)`.
5. Open the lesson in a browser and confirm identical appearance and full
   interactivity before moving to the next lesson.

### 4.4 LESSON_DESIGN updates

Prepend a `## Shared assets` section to both `lessons/LESSON_DESIGN.md` and
`lessons/LESSON_DESIGN_v2.md` explaining that `lesson.css` and `lesson.js` must
not be regenerated, and listing exactly what each new lesson HTML must contain.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Extract CSS from `lessons/3sum/lesson.html` lines 7–188 into `static/lesson.css`; cross-check other three lessons for any selectors that are problem-specific and must stay inline | 30 min | — |
| 2 | Extract shared JS functions into `static/lesson.js`; change `cvBuildCode` signature to accept `lines` param | 30 min | 1 |
| 3 | Refactor `lessons/3sum/lesson.html`: add `<link>`, remove shared CSS/JS, add `<script src>`, update `cvBuildCode()` → `cvBuildCode(CV_LINES)` | 30 min | 2 |
| 4 | Open `lessons/3sum/lesson.html` in browser; verify all three visualizers (BF, CV, DR) work and appearance is identical to the pre-refactor snapshot | 15 min | 3 |
| 5 | Refactor `lessons/permutation-in-string/lesson.html` (same steps as task 3) | 30 min | 4 |
| 6 | Browser-verify `permutation-in-string` | 15 min | 5 |
| 7 | Refactor `lessons/trapping-rain-water/lesson.html`; keep `.bf-bar-con` bar chart styles inline | 30 min | 6 |
| 8 | Browser-verify `trapping-rain-water` | 15 min | 7 |
| 9 | Refactor `lessons/container-with-most-water/lesson.html` | 30 min | 8 |
| 10 | Browser-verify `container-with-most-water` | 15 min | 9 |
| 11 | Prepend `## Shared assets` section to `lessons/LESSON_DESIGN.md` and `lessons/LESSON_DESIGN_v2.md` | 15 min | 10 |

Total estimated time: ~4 hours 15 min (mostly sequential due to browser verification gates).

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| A CSS selector exists in 3sum but not in other lessons, causing missing styles after extraction | Low | High | Cross-grep all four lessons for every selector in the extracted CSS; keep any singleton selector inline |
| `cvBuildCode(lines)` call site missed in one lesson, causing JS reference error | Med | High | After each lesson refactor, open browser console and confirm no errors before proceeding |
| `../../static/` path is wrong for lessons served at a different depth | Low | High | Confirm the relative path resolves correctly for lessons at `lessons/<slug>/lesson.html` (two levels up = project root) |
| Browser caches old inline styles after refactoring | Low | Low | Hard-reload (Ctrl+Shift+R) during each browser verification step |

---

## 7. Success criteria

1. `static/lesson.css` and `static/lesson.js` exist and are non-empty.
2. All four golden lesson HTML files no longer contain a `<style>` block with `:root` variables or shared selectors.
3. All four lessons pass browser visual verification (appearance identical to pre-refactor).
4. No browser console errors on any lesson after refactoring.
5. `lessons/LESSON_DESIGN.md` and `lessons/LESSON_DESIGN_v2.md` both contain a `## Shared assets` section.

---

## 8. References

- `AGENT_MD/STATIC_MIGRATION_PLAN.md` — source spec for this plan
- `lessons/3sum/lesson.html` — CSS reference (lines 7–188), JS reference (lines 628+)
- `scripts/server.py` — confirms static file serving from project root (line 24)
- `lessons/LESSON_DESIGN_v2.md` — lesson authoring guide to be updated
- `AGENT_MD/plan/rules.md` — plan authoring conventions
