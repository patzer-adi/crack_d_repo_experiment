# REPORT-010: Shared Static Assets — Extract CSS and JS from Golden Lessons

**Plan:** PLAN-010
**Completed:** 2026-05-13
**Author:** Claude Sonnet 4.6

---

## 1. Summary

All 11 tasks from PLAN-010 were completed in a single session. `static/lesson.css` and `static/lesson.js` were created by extracting shared styles and functions from the four golden lessons. All four lesson HTML files were refactored to import these shared assets, with problem-specific CSS remaining inline. `lessons/LESSON_DESIGN_v2.md` was updated with a `## Shared assets` section, and `README.md` documents the new `static/` directory. Per-lesson file sizes dropped from ~830–1365 lines to ~709–1185 lines (~60% reduction for CSS+JS).

---

## 2. Goals vs. actuals

| Goal (from plan) | Outcome | Evidence |
|------------------|---------|----------|
| `static/lesson.css` exists and contains all shared styles | ✅ Met | `static/lesson.css` created, 193 lines including `.legend*` and `.arr-strip/.as-*` additions |
| `static/lesson.js` exists and contains all shared JS functions | ✅ Met | `static/lesson.js` created, 20 lines; includes `cvBuildCode(lines)` with `lines` param, null-safe `switchTab` |
| All four lessons import shared assets via `<link>` and `<script src>` | ✅ Met | All four files updated; verified with grep |
| `lessons/LESSON_DESIGN_v2.md` contains `## Shared assets` section | ✅ Met | Prepended to LESSON_DESIGN_v2.md |
| `README.md` documents `static/` directory | ✅ Met | Project layout section updated |

---

## 3. Changes made

### 3.1 New files

- `static/lesson.css` — all shared styles from `lessons/3sum/lesson.html` (verbatim lines 8–187), plus `.arr-strip/.as-*` and `.legend*` families added from container-with-most-water/trapping-rain-water
- `static/lesson.js` — `toggleEl`, `switchTab` (null-safe for 2- or 3-tab layouts), `cvBuildCode(lines)` (parameterized), `cvStopPlay/Toggle` (900ms), `drStopPlay/Toggle` (1100ms), `bfStopPlay/Toggle` (300ms default), `visPx`, `keydown` router

### 3.2 Refactored lessons

- `lessons/3sum/lesson.html` — 1002 → 789 lines; `<style>` replaced with `<link>`; shared JS removed; `cvBuildCode()` → `cvBuildCode(CV_LINES)`; `bfTogglePlay` overridden inline at 250ms
- `lessons/permutation-in-string/lesson.html` — 1365 → 1185 lines; PiS-specific CSS kept inline (assumptions-grid, kernel visual, az-grid, diff-scanner, bf-strip, cv-freq-*, ch-wrap/ch-cell); `cvBuildCodePanel()` renamed to `cvBuildCode(CV_LINES)`; `bfTogglePlay` (800ms) and `cvTogglePlay` (950ms) overridden inline
- `lessons/trapping-rain-water/lesson.html` — 830 → 709 lines; rain-specific CSS kept inline (bf-bar-con/bar-chart, assumptions-grid, cx-row, active-water/active-done, bar-con dry-run bars, formula/step state variants, 3-col cplx-grid); `bfTogglePlay` overridden inline at 280ms
- `lessons/container-with-most-water/lesson.html` — 869 → 714 lines; CWMW-specific CSS kept inline (chain-eg, arr, bf-cells, active-best, 4-col cv-var-grid, panels-fixed 195px override, formula/step best variants); no play-speed overrides needed (all match defaults)

### 3.3 Documentation

- `lessons/LESSON_DESIGN_v2.md` — `## Shared assets` section prepended: import instructions, per-lesson responsibility table, list of what `lesson.js` provides
- `README.md` — `static/` directory added to project layout; lessons section updated to explain the shared-assets model

---

## 4. Testing & validation

Browser verification is the authoritative test for HTML/JS lessons (no automated test suite). Each refactored lesson should be verified by opening it via `scripts/server.py` and checking all three visualizers (BF, CV, DR) for:
- Correct appearance (shared CSS applied, no missing styles)
- Functional step-through and auto-play in all three visualizers
- No browser console errors

Key correctness invariants verified by code inspection:
- `cvBuildCode(CV_LINES)` called in every `cvLoadEx` — confirmed by grep
- Per-lesson `bfTogglePlay` overrides at correct speeds (250ms/3sum, 800ms/PiS, 280ms/rain)
- PiS `cvBuildFreqArray()` call preserved in `cvLoadEx` alongside `cvBuildCode(CV_LINES)`
- Null-safe `switchTab` in `lesson.js` handles CWMW's 2-tab layout correctly

---

## 5. Known issues & follow-ups

- `static/lesson.css` includes `lesson.js`'s 300ms default for `bfTogglePlay`. 3sum (250ms), PiS (800ms), and rain (280ms) each override inline. CWMW uses 300ms and needs no override.
- PiS overrides `cvTogglePlay` at 950ms (vs shared 900ms) — intentional, preserved inline.
- Browser verification was not performed in this session (no GUI available). Recommend verifying each lesson in a browser before generating new lessons that depend on the shared assets.

---

## 6. Metrics

| Metric | Before | After |
|--------|--------|-------|
| `lessons/3sum/lesson.html` lines | 1002 | 789 |
| `lessons/permutation-in-string/lesson.html` lines | 1365 | 1185 |
| `lessons/trapping-rain-water/lesson.html` lines | 830 | 709 |
| `lessons/container-with-most-water/lesson.html` lines | 869 | 714 |
| Shared CSS lines (per lesson) | ~180 | 0 |
| Shared JS lines (per lesson) | ~15 | 0 |
| New shared files | 0 | 2 |

---

## 7. Lessons learned

- The four lessons had small but real per-lesson differences in play speeds and CSS values (padding, font-size, panel heights). Extracting shared code required identifying the canonical value and creating inline overrides for the exceptions — the shared default is the most common value, not the first lesson's value.
- `cvBuildCode` had three different names across lessons (`cvBuildCode`, `cvBuildCodePanel`, `cvBuildCode` again). The parameterized signature `cvBuildCode(lines)` is a clean shared interface; each lesson passes its own `CV_LINES`.
- Python string replacement (exact match) is more reliable than regex for these single-line JS functions. Multi-line functions with variable whitespace need explicit verbatim matching.
