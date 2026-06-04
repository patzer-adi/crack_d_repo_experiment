# REPORT-020: Mobile-friendly responsive layout for lessons and dashboard

**Plan:** PLAN-020
**Completed:** 2026-06-04
**Author:** Claude (Opus 4.8) via Claude Code, pair-driven with the user

---

## 1. Summary

Made both app surfaces usable on a phone with CSS-only changes — no framework, no
JS behaviour changes, no table redesign. Lessons gained a `@media (max-width:480px)`
phone breakpoint; the dashboard's single 700px breakpoint became a two-tier
700px/480px scheme that hides low-value table columns and lets the wide tables
scroll inside their own wrapper. Two lessons (`container-with-most-water`,
`merge-intervals`) carried genuinely wide problem-specific visuals that needed
per-lesson fixes. The render gate (`scripts/render_check.mjs`) was extended to
assert no horizontal overflow at a phone viewport (390px) in addition to the
existing desktop (1000px) pass, so future lessons stay mobile-safe. All 30 lessons
pass both passes; the dashboard has zero page overflow at 360px and 390px across
all three tabs.

## 2. Goals vs. actuals

| Goal (from plan) | Outcome | Evidence |
|-------------------|---------|----------|
| **G1** No horizontal page scroll at 390px and 360px on both surfaces | ✅ Met | `render_check --all` → 30/30 pass (incl. 390px pass); dashboard headless check → delta=0 at 390px and 360px on problems/algorithms/patterns |
| **G2** Phone tables show the essential columns, hidden columns degrade gracefully | ✅ Met | Problems shows Problem/Difficulty/Status/Lesson; Algorithms keeps Name/Tier/Relevance/Lesson (via wrapper scroll, no data dropped). Screenshots at 390px confirm clean layout |
| **G3** `.panels-fixed` content un-clipped at 390px | ✅ Met | `@media(max-width:480px)` sets `.panels-fixed{grid-template-rows:auto auto}` + `overflow:visible`; render gate drives every dry-run at 390px with no overflow |
| **G4** Topbar/stats/filter/action bars + modals operable at 360px | ✅ Met | Topbar count badges hidden + chrome shrunk so logo+tabs fit one row; stats/filter bars wrap; action-bar wraps; add-form stacks. delta=0 at 360px |
| **G5** Mobile overflow pass in the gate; all 30 lessons pass; audit clean | ✅ Met | `render_check.mjs` mobile pass added; `audit_lessons.py` → `render: 30 pass · 0 NEW fail`, `=> OK (no new drift)` |
| **G6** Desktop (≥1000px) appearance unchanged | ✅ Met | Every new rule lives inside a `max-width` media query; `merge-intervals` width capped at 380px (its prior fixed value) so desktop is byte-identical |

## 3. Changes made

### 3.1 Render gate — phone overflow pass
- `scripts/render_check.mjs` — added `MOBILE = {width:390,height:844}`; extracted
  the overflow-measurement snippet into `OVERFLOW_JS` (embedded in `CHECKER`);
  after the desktop pass, `checkSlug` now re-sets the viewport to phone metrics,
  **re-runs `CHECKER` (re-driving animations so width-reactive renders recompute)**,
  measures overflow, and restores the desktop viewport. New failure reason
  `mobile horizontal overflow @390px: …`. Header comment updated.

### 3.2 Lessons — shared CSS
- `static/lesson.css` — new `@media (max-width:480px)` block: body padding
  `2.5rem 1.5rem` → `1.75rem 1rem`; `overflow-wrap:break-word` on body; type
  step-down (`h1` 26px, `.sec-title` 21px, `p.body` 17px, secondary text 16px);
  `code{overflow-wrap:anywhere;word-break:break-word}`; `.formula-grid` → 2 cols;
  `.panels-fixed` → auto rows; `.formula-panel,.step-panel{overflow:visible}`;
  `.kbd-hint{display:none}`.

### 3.3 Lessons — per-lesson visuals (only the two that overflowed)
- `lessons/container-with-most-water/lesson.html` — added `overflow-x:auto` to the
  `#si-strip` bar chart so its fixed-width bars scroll inside the box instead of
  the page.
- `lessons/merge-intervals/lesson.html` — `siRender` no longer hardcodes
  `containerWidth = 380`; it reads the track's parent `clientWidth` and caps at
  380 (`Math.min(380, parentW - 18)`), so the timeline shrinks to fit a phone but
  is unchanged on desktop.

### 3.4 Dashboard — CSS
- `dashboard/index.html` `<style>` — the lone `@media (max-width:700px)` became
  two tiers:
  - `≤700px` (tablet): also hides `.col-order`; tightens `.content` / bar padding.
  - `≤480px` (phone): shrinks topbar (`.topbar` padding, `.topbar-logo` 30px,
    `.tab-btn` 14px) and **hides the tab count badges** (`.tab-btn span`) so the
    logo + 3 tabs fit one row; hides `.col-check`/`.col-xlinks` (Problems) and
    `.col-kind` (Algorithms); gives each table wrapper
    (`[data-section-body]`,`[data-algo-section-body]`) `overflow-x:auto`; stacks
    `.add-row`; wraps `.action-bar`; full-width search.

### 3.5 Documentation
- `lessons/design/layout.md` — rewrote §Mobile (both breakpoints, the
  `.panels-fixed` auto-height exception, the container-sizing guidance, and the
  390px gate).
- `static/CLASSES.md` — added the 480px breakpoint line to §"Layout & mobile".
- `README.md` — render-check description now states desktop+phone widths; added a
  "Responsive / mobile (PLAN-020)" subsection; updated the `render_check.mjs`
  layout-tree one-liner.

## 4. Testing & validation

- **Gate, baseline before fix:** `node scripts/render_check.mjs --all` → 25 ok, 5
  failed (`container-with-most-water`, `find-the-duplicate-number`,
  `majority-element-ii`, `maximum-product-subarray`, `merge-intervals`) — all on
  mobile overflow.
- **Gate, after fix:** `node scripts/render_check.mjs --all` → **30 ok, 0 failed.**
  The global CSS (padding + wrap) fixed 3; the two per-lesson visuals fixed the
  rest. Progression observed: 5 → 2 → 1 → 0, confirming the gate is discriminating.
- **Corpus audit:** `python3 scripts/audit_lessons.py` → `render: 30 pass · 0 NEW
  fail`, `lint: 0 NEW fail`, `=> OK (no new drift)`. (Pre-existing lint KNOWN-FAILs
  and one WARN are baseline-grandfathered, untouched by this work.)
- **Dashboard:** served over `http://127.0.0.1:8099`, loaded headless at 390px and
  360px, switched through problems/algorithms/patterns — `delta=0` (no page
  overflow) in all six combinations. Screenshots at 390px confirm the topbar fits
  one row, tables show the right columns, and the Algorithms table scrolls within
  its wrapper to reveal Tier/Relevance/Lesson.
- **Diagnosis method:** a throwaway script (`scripts/_diag_overflow.mjs`,
  deleted) walked each overflowing element's ancestor chain to distinguish
  *clipped* wide elements (`.cv-line` inside a scrollable panel — a red herring)
  from true page-overflow contributors. This is what revealed the real causes were
  heterogeneous (long `<code>`, unbreakable plain-text tokens, fixed-width bar
  strips, a hardcoded 380px timeline) rather than the code panel.

## 5. Known issues & follow-ups

- **Dashboard has no automated render gate.** It is a single static file; its
  mobile layout was verified manually (headless device-emulation). A future plan
  could add a dashboard render smoke test if it becomes a recurring concern.
- **Body max-width discrepancy untouched (deliberate non-goal).**
  `static/lesson.css` caps `body` at 1270px while `lessons/design/layout.md` and
  `static/CLASSES.md` say 1100px. Not a mobile issue; left for a doc/CSS
  reconciliation pass.
- **The `.panels-fixed` no-jump guarantee is relaxed on phones only.** During
  keyboard step-through the panels can change height between steps at ≤480px —
  acceptable because step-through is a desktop interaction and phones have no
  keyboard.

## 6. Metrics

| Surface | Before (page overflow @390px) | After |
|---|---|---|
| Lessons (30) | 5 overflow | 0 overflow |
| Dashboard — problems | overflow (scrollW 453) | fits (390) |
| Dashboard — algorithms | overflow (scrollW 532) | fits (390) |
| Dashboard — patterns | overflow (scrollW 453) | fits (390) |

Lines changed: `static/lesson.css` +14, `dashboard/index.html` ~+20, two lesson
files +2/+3, `render_check.mjs` ~+20. No JS dependency added.

## 7. Lessons learned

- **The overflow gate's "widest element" report can mislead.** It uses
  `getBoundingClientRect`, which ignores ancestor clipping, so a code line clipped
  inside an `overflow:auto` panel reports a huge rect that is *not* the page
  overflow source. Walking the ancestor chain for an unclipped element is what
  found the real culprits. Worth keeping that distinction in mind for future gate
  work.
- **Driving animations at desktop then peeking at mobile is not a real mobile
  test.** Width-reactive JS (the merge-intervals timeline) only recomputes when it
  re-renders, so the gate now re-drives at phone width — which both validates the
  fix and mirrors what a phone visitor actually sees.
- **"Nothing fancy" paid off:** the wrapper-scroll (`overflow-x:auto` on the
  existing table-wrapper divs) preserved every column with one CSS line and no JS,
  beating the planned column-dropping approach on faithfulness.
