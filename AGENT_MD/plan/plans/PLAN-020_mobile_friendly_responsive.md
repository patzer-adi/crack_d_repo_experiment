# PLAN-020: Mobile-friendly responsive layout for lessons and dashboard

**Created:** 2026-06-04
**Status:** Completed
**Addresses:** The lessons and the dashboard are built for desktop widths; on a phone the wide dashboard tables overflow horizontally and lesson panels clip. Make the whole app usable on a small screen without a redesign.

> **Completed 2026-06-04** — implemented as specified; see [`REPORT-020`](../reports/REPORT-020_mobile_friendly_responsive.md). All 30 lessons pass the new 390px render-gate pass; dashboard has zero page overflow at 360/390px. One refinement vs. the plan: the dashboard tables use a wrapper `overflow-x:auto` scroll (keeps every column) rather than dropping Tier/Relevance columns — strictly more faithful and still CSS-only.

---

## 1. Context & motivation

The app has two HTML surfaces, both already shipping `<meta name="viewport" content="width=device-width, initial-scale=1.0">`:

1. **Lessons** — 30 × `lessons/<slug>/lesson.html` rendered against the shared
   `static/lesson.css` + `static/lesson.js`. `static/lesson.css:190` already has
   one breakpoint (`@media (max-width:680px)`) that collapses the two-column
   grids (`.cv-split`, `.asgrid`, `.cplx-grid`, `.formula-grid`, `.cv-var-grid`).
2. **Dashboard** — `dashboard/index.html` (single self-contained file, ~1700
   lines). `dashboard/index.html:417` already has one breakpoint
   (`@media (max-width:700px)`) that collapses the patterns grid, hides three
   table columns, and narrows the search box.

So the groundwork exists but is incomplete. Concrete gaps observed:

- **Dashboard tables overflow.** The Problems table has **9** columns
  (`dashboard/index.html:912`) and the Algorithms table has **7**
  (`dashboard/index.html:1097`). Hiding the current three is not enough; at
  ~390 px the remaining columns still force horizontal page scroll.
- **Lesson side padding + font sizes** are tuned for desktop. `body` keeps
  `padding: 2.5rem 1.5rem 5rem` (`static/lesson.css:12`) and large type
  (`h1` 33 px, `.sec-title` 26 px, `p.body` 20 px) at every width.
- **`.panels-fixed` clips.** Its rows are *fixed* heights
  `175px 110px` (`static/lesson.css:125`, mandated by
  `lessons/design/layout.md` to stop layout jump). When `.formula-grid`
  reflows from 5→3 columns on narrow screens the content can exceed 175 px and
  get clipped.
- **No phone-size breakpoint** on either surface (smallest is 680/700 px).
- **The render gate never tests mobile.** `scripts/render_check.mjs:35` fixes
  the viewport at `{ width: 1000, height: 900 }`, so its "no horizontal
  overflow" assertion (`scripts/render_check.mjs:131`) cannot catch a lesson
  that overflows on a phone.

This plan keeps the change deliberately small per the requester's constraint
("nothing fancy"): **CSS-only**, reuse the existing breakpoints, add **one**
phone-size breakpoint per surface, and progressively hide non-essential table
columns rather than rebuilding the tables as cards. No new tooling, no
framework, no JS restructuring.

---

## 2. Goals

- **G1:** No horizontal page scroll on either surface at **390 px** and at
  **360 px** viewport widths. (Code blocks `pre.cb` / `.cv-code-panel` may still
  scroll *internally* — that is intended and not page overflow.)
- **G2:** On a phone the Problems table shows, at minimum, the problem **name**,
  **difficulty**, **status**, and the **Open lesson** action; the Algorithms
  table shows **name**, **tier**, **relevance**, and **Lesson**. Hidden columns
  degrade gracefully (no empty gaps, no clipped text).
- **G3:** Every lesson's `.panels-fixed` formula/step panels show their content
  un-clipped at 390 px (no overflow inside the panel, no layout jump *within* a
  width — height may differ between desktop and phone).
- **G4:** Topbar tabs, stats bar, filter bar, action bar, and modals remain
  reachable and operable at 360 px (controls wrap or shrink; nothing is cut off
  the side of the screen).
- **G5:** `scripts/render_check.mjs` gains a mobile overflow pass so the
  existing quality gate (and `scripts/audit_lessons.py`) catch mobile
  regressions in future lessons. All 30 current lessons pass it.
- **G6:** Desktop appearance at ≥ 1000 px is unchanged (the new rules live only
  inside `max-width` media queries).

---

## 3. Non-goals

- **No table→card redesign.** Tables stay tables; we hide columns. Building a
  responsive card view per row is out of scope ("nothing fancy").
- **No JS behaviour changes.** The keyboard router, animation drivers, filter
  logic, and bulk-select flow are untouched. (The bulk-select checkbox column is
  simply hidden on phones; the desktop flow is unaffected.)
- **No change to the `body` max-width or the fixed-height layout contract** on
  desktop. The discrepancy between `static/lesson.css:12` (`max-width:1270px`)
  and the docs (`lessons/design/layout.md` says 1100 px) is noted but **not**
  resolved here.
- **No new build step, bundler, or dependency.** Everything stays static files.
- **No PWA / offline / install-prompt / touch-gesture features.**
- **No redesign of the lesson typography system** beyond proportional
  down-scaling inside the phone breakpoint.

---

## 4. Approach

Three edits: lesson CSS, dashboard CSS, and the render gate. The two surfaces do
not share a stylesheet, so each gets its own breakpoint additions.

### 4.1 Lessons — `static/lesson.css`

Keep the existing `@media (max-width:680px)` block (`static/lesson.css:190-194`)
as-is and **add a phone block** `@media (max-width:480px)` after it:

1. **Reduce side padding:** `body { padding: 1.75rem 1rem 4rem; }` — reclaims
   ~16 px of horizontal space per side.
2. **Down-scale the largest type** so headings don't dominate a phone:
   `.header h1 → 26px`, `.sec-title → 21px`, `p.body → 17px`,
   `.infobox-d / .corner-body / .chk-text / .algo-t → 16px`. (Proportional, not
   a redesign; values chosen to keep the existing hierarchy.)
3. **Un-clip `.panels-fixed`:** inside this block set
   `.panels-fixed { grid-template-rows: auto auto; }` and give the formula/step
   panels a `min-height` instead of a fixed height. This trades the "no layout
   jump" guarantee (a *desktop* concern from `lessons/design/layout.md`) for
   "content is visible" on phones, where the panels stack and scroll anyway.
4. **Collapse `.formula-grid` to 2 columns** at 480 px (it is 5 on desktop, 3 at
   680 px) — five formula cells never fit a phone row.
5. **Hide keyboard-only affordances:** `.kbd-hint { display:none; }` — the
   ←/→/Space/R hints are meaningless without a keyboard; the on-screen
   prev/play/next/reset buttons remain.
6. **Confirm wrapping holds:** `.ctrl-row`, `.legend`, `.number-line`,
   `.num-strip`, `.bf-nums`, `.arr-strip` already use `flex-wrap:wrap`; verify no
   per-lesson inline style defeats it (caught by the render gate, §4.3).

### 4.2 Dashboard — `dashboard/index.html` `<style>`

Keep the existing `@media (max-width:700px)` block
(`dashboard/index.html:417-421`) and refine it into a **two-tier** scheme:

1. **`@media (max-width:700px)` (tablet) — extend the existing block:**
   - Patterns grid → 1 column (already present).
   - Problems table: hide `.col-order`, `.col-lc`, `.col-topic` (add `.col-order`
     to the existing `.col-lc, .col-topic` hide).
   - Algorithms table: hide `.col-time` (already), `.col-order`.
   - Reduce `.content` and bar paddings from `24px` → `14px`.
2. **`@media (max-width:480px)` (phone) — new block:**
   - Problems table: additionally hide `.col-check` and `.col-xlinks`
     (Algorithms). Remaining: **Problem / Difficulty / Status / Lesson** (G2).
   - Algorithms table: additionally hide `.col-kind`. Remaining:
     **Name / Tier / Relevance / Lesson** (G2).
   - Topbar: `.topbar { padding: 0 12px; }`, `.topbar-logo { height: 34px; }`,
     `.tab-btn { padding: 0 10px; font-size: 15px; }` so logo + 3 tabs fit.
   - Action bar: `.action-bar { padding: 10px 14px; gap: 10px; flex-wrap: wrap; }`
     and allow `.action-bar-label` to shrink.
   - `.add-row { grid-template-columns: 1fr; }` so the add-problem form stacks.
   - `.filter-search { width: 100%; }` and let the filter bar wrap (already
     `flex-wrap:wrap`).
   - Reduce `th`/`td` horizontal padding to `5px` to buy width.

   The stats bar and filter bar already `flex-wrap`, so they need no structural
   change beyond padding.

### 4.3 Verification — `scripts/render_check.mjs`

Add a **second overflow measurement at a mobile viewport** to the existing
per-lesson run so the gate enforces G1/G3 going forward:

1. After the current desktop pass, re-set the page viewport to
   `{ width: 390, height: 844, deviceScaleFactor: 1, mobile: true }` (mirrors the
   call at `scripts/render_check.mjs:225`), re-run the in-page overflow checker
   (the block at `scripts/render_check.mjs:131-138`), and fail the lesson if the
   mobile `scrollWidth − clientWidth` exceeds the existing `OVERFLOW_TOL`.
2. Report it as a distinct reason string (e.g. `mobile horizontal overflow @390px`)
   so failures are self-explanatory.
3. Preserve the existing "no browser found → skip with exit 0" degradation
   (`scripts/render_check.mjs` header) — the mobile pass must not make the gate
   harder to run in CI-less environments.

The dashboard is a single static file with no render gate; its mobile layout is
verified **manually** in browser device-emulation at 360 px and 390 px
(see §4 testing in the report). No automated dashboard gate is added (nothing
fancy).

### 4.4 Documentation touch-ups

- `lessons/design/layout.md` §"Mobile": note the new `480px` phone breakpoint and
  the `.panels-fixed → auto` exception on phones.
- `static/CLASSES.md` §"Layout & mobile": same one-line note.
- Both edits are small and keep the generator's guidance honest (the lesson
  generator reads these, not the full CSS).

---

## 5. Task breakdown

Test-first per `rules.md §5.11`: for CSS the "test" is the render-gate overflow
assertion at the mobile viewport — wire that first, watch it flag the gaps, then
fix CSS until green.

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Add mobile (390 px) overflow pass to `scripts/render_check.mjs` (§4.3) | 45 min | — |
| 2 | Run `node scripts/render_check.mjs --all` to capture the baseline list of lessons that overflow on mobile | 15 min | 1 |
| 3 | Add `@media (max-width:480px)` block to `static/lesson.css` (§4.1) | 1 hr | 2 |
| 4 | Re-run the gate on `--all`; fix any per-lesson inline width that still overflows | 45 min | 3 |
| 5 | Extend/split the dashboard media queries into 700 px + 480 px tiers (§4.2) | 1.5 hr | — |
| 6 | Manually verify dashboard at 360/390 px (Problems, Algorithms, Patterns tabs; filter; bulk-select action bar; add-problem modal) | 45 min | 5 |
| 7 | Update `lessons/design/layout.md` + `static/CLASSES.md` mobile notes (§4.4) | 15 min | 3 |
| 8 | Run `scripts/audit_lessons.py` (full lint + render, baseline-aware) and confirm no regressions; write `REPORT-020` | 30 min | 4,5,6,7 |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `.panels-fixed → auto` reintroduces layout jump on phones | Medium | Low | Jump only matters during keyboard step-through, which is a desktop interaction; on phone panels stack and the page scrolls regardless. Scope the change strictly inside the 480 px block. |
| A lesson has a problem-specific inline `<style>` with a fixed width that overflows on mobile | Medium | Medium | Task 2's gate run surfaces the exact offenders by class name (`overflow.widest`); fix each inline rule. |
| Hiding the Algorithms/Topic columns removes info a phone user wants | Low | Low | The full table stays on desktop; the problem name remains a link to the lesson, which carries the detail. Revisit only if requested. |
| Mobile render pass slows the gate or flakes | Low | Low | Reuse the already-loaded page (just re-set viewport + re-measure); no second page load. Keep the no-browser skip path. |
| Down-scaling fonts makes lessons feel cramped | Low | Low | Values are a proportional step-down, not a flat shrink; verify by eye on one lesson before applying corpus-wide (CSS is shared, so it applies once). |

---

## 7. Success criteria

- [ ] G1: `node scripts/render_check.mjs --all` passes with the new 390 px pass;
      manual check shows no horizontal page scroll on the dashboard at 360/390 px.
- [ ] G2: Problems and Algorithms tables show the required columns on a phone;
      hidden columns leave no gaps.
- [ ] G3: `.panels-fixed` content is fully visible at 390 px on every lesson.
- [ ] G4: Topbar, stats/filter/action bars, and modals operable at 360 px.
- [ ] G5: The mobile overflow pass is in `render_check.mjs` and all 30 lessons
      pass; `scripts/audit_lessons.py` reports no new failures.
- [ ] G6: Visual diff at ≥ 1000 px shows no change (all edits inside
      `max-width` queries).
- [ ] `REPORT-020` written; this plan's status set to `Completed`.

---

## 8. References

- `static/lesson.css:12` — `body` sizing; `:190-194` — existing 680 px breakpoint
- `static/CLASSES.md` §"Layout & mobile"
- `lessons/design/layout.md` — fixed-height contract + "Mobile" section
- `dashboard/index.html:417-421` — existing 700 px breakpoint;
  `:912` Problems `<th>` set; `:1097` Algorithms `<th>` set
- `scripts/render_check.mjs:35` (viewport), `:131-138` (overflow checker),
  `:225` (viewport-set call)
- `scripts/audit_lessons.py` — corpus lint + render
- `AGENT_MD/plan/rules.md` — document conventions
