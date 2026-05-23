# PLAN-014: UI/UX Polish — Accessibility, Interactions & Discoverability

**Created:** 2026-05-18
**Status:** Draft
**Addresses:** Raise the crack_d web app from a functional 7.2/10 UI/UX baseline toward an 8.5+ rating by closing accessibility gaps, adding micro-interactions, and improving discoverability of problems and lessons.

---

## 1. Context & motivation

A UI/UX audit conducted on 2026-05-18 rated the dashboard and lesson pages at **7.2/10**. The fundamentals are solid (typography hierarchy, consistent design system via CSS variables, logical lesson flow), but the following gaps prevent the app from feeling polished:

- **Accessibility:** no ARIA labels, no documented focus styles, missing alt text on logo images, unverified keyboard navigation, secondary text colors may fail WCAG AA contrast.
- **Interaction feedback:** hover states are minimal, no loading/empty states, no transition animations on tab switches or table sorts.
- **Discoverability:** no search/filter on the problems list, no onboarding hint, no progress indication on lessons.
- **Theming:** no dark mode, despite a CSS-variable foundation that would make it cheap to add.
- **Mobile:** a single `@media(max-width:680px)` query covers all small-screen cases; tablet (681–1024px) and touch-target sizing are not addressed.

Recent layout work (width → 1270px, body font → 20px) improved readability but did not touch these structural gaps. This plan addresses them in priority order, biggest readability/accessibility wins first.

References:
- `AGENT_MD/plan/current_state_report.md` — overall project state
- `static/lesson.css` — shared lesson stylesheet
- `dashboard/index.html` — single-file dashboard
- `static/CLASSES.md` — CSS class reference

---

## 2. Goals

- **G1 (Accessibility — WCAG AA baseline):** every interactive element has a visible `:focus-visible` outline; every `<img>` has descriptive `alt` text; difficulty badges expose text labels to screen readers (not color-only); all body-text/background pairs verified ≥ 4.5:1 contrast.
- **G2 (Keyboard navigation):** the dashboard is fully operable with `Tab`, `Shift+Tab`, `Enter`, and `Esc` (modal close). Lesson-page interactive controls (step buttons, tab bar, reveal buttons) are keyboard-reachable in document order.
- **G3 (Micro-interactions):** all buttons, tabs, table rows, and chips have a perceptible hover/focus state with a ≤ 200ms transition. Tab-pane switches fade in.
- **G4 (Discoverability):** dashboard exposes a search box and difficulty/topic filters above the problems table. Empty/loading states render when applicable.
- **G5 (Dark mode):** a theme toggle persists user choice in `localStorage`; all CSS-variable-driven colors flip via `[data-theme="dark"]` on `<html>`.
- **G6 (Responsive breakpoints):** two new breakpoints (`≤480px` mobile, `481–1024px` tablet) verified manually in DevTools at 375×667, 768×1024, and 1280×800.
- **G7 (Lesson progress):** a tiny per-lesson "Read" toggle on the dashboard row, persisted in `localStorage`, with aggregate progress shown above the table.

Every goal is verifiable: visible attribute (G1, G3), manual keyboard walk (G2), feature presence (G4–G7), and contrast-check tool output (G1).

---

## 3. Non-goals

- **Server-side state.** Progress and theme are stored in `localStorage` only — no auth or sync across devices.
- **Backend search.** Filtering happens client-side on the in-memory problems list. No new API endpoints.
- **Animated tutorial overlay.** Saved for a future plan; this plan only adds a static onboarding hint.
- **Lesson-content rewrites.** Lesson HTML/JS bodies are not edited; only the shared `static/lesson.css` and lesson-template patterns are touched.
- **New illustrations or logo work.** The existing 3-logo rotation stays as-is.
- **Mobile-app or PWA wrapping.** Out of scope.

---

## 4. Approach

The work is split into six independent phases that can ship one at a time. Phases 1–2 are the highest-leverage (accessibility + interaction) and should ship first.

### 4.1 Phase 1 — Accessibility baseline (G1, G2)

1. Add `alt` text to the random logo in `dashboard/index.html` (it currently has a label, but verify and tighten).
2. Add a global `*:focus-visible { outline: 2px solid var(--text-info); outline-offset: 2px; }` rule to both `dashboard/index.html` inline CSS and `static/lesson.css`.
3. Augment difficulty badges in `dashboard/index.html` with an `aria-label` containing the literal difficulty word ("Easy/Medium/Hard") so screen readers don't rely on color alone.
4. Run contrast checks (tooling: any WCAG contrast checker) on `--text3` against `--bg`, `--bg2`, `--bg3`. Where < 4.5:1, darken `--text3` from `#6b6760` toward `#595550`.
5. Walk the dashboard and one lesson page with keyboard only; fix any element that can't receive focus or whose focus order is illogical.

### 4.2 Phase 2 — Micro-interactions (G3)

1. Standardize on a single transition token: `--t-fast: 150ms` and `--t-med: 220ms`, defined in `:root` of both stylesheets.
2. Add `transition: background var(--t-fast), border-color var(--t-fast), color var(--t-fast);` to `.tab-btn`, `.ctrl-btn`, `.ex-btn`, `.reveal-btn`, `.prob-row` (dashboard), and `.chip` classes.
3. Add a 220ms fade-in (`@keyframes fadeIn`) to `.tab-pane.active`.
4. Add `cursor:pointer` audit on clickable elements that lack it.

### 4.3 Phase 3 — Search & filters (G4)

1. Add a `<input type="search">` and two `<select>` controls (difficulty, topic) inside `dashboard/index.html` just above the problems table.
2. Bind them to the existing render loop: client-side filter the in-memory problems array by case-insensitive title substring AND difficulty AND topic.
3. Render a `.empty-state` row (icon + "No problems match your filters") when the filtered set is empty.
4. Render a `.loading-state` skeleton if the fetch for `data/problems.json` hasn't resolved (currently it loads synchronously enough that this may be a no-op — verify).

### 4.4 Phase 4 — Dark mode (G5)

1. Move all color literals in `:root` of `static/lesson.css` and `dashboard/index.html`'s inline CSS into a `:root, :root[data-theme="light"]` block.
2. Add a `:root[data-theme="dark"]` block with palette overrides (warm dark like `#1a1816` background, `#e8e4de` text — matches the existing warm cream feel inverted).
3. Add a small `<button id="theme-toggle">` in the dashboard topbar (icon-only on small screens) that toggles `<html>`'s `data-theme` attribute and writes to `localStorage`.
4. On lesson pages, inject the same toggle into the header. Since lesson HTML is per-problem, place it via a small `<script>` at the bottom of `static/lesson.css`'s sibling — actually requires a tiny inline `<script>` in each lesson, OR an entry in the lesson template; verify with the lesson generation pipeline (PLAN-011) before deciding.
5. On page load, read `localStorage.theme` and apply before first paint to avoid flash.

### 4.5 Phase 5 — Responsive breakpoints (G6)

1. Add `@media(max-width:480px)` for true mobile: shrink padding, stack header brand vertically, hide secondary table columns (LC#, Algorithms chips) behind an expand-row affordance.
2. Add `@media(481px <= width <= 1024px)` for tablet: keep the table but compact the chip column.
3. Manually verify at 375×667, 768×1024, 1280×800 in browser DevTools.

### 4.6 Phase 6 — Progress tracking (G7)

1. Add a checkbox in a new column `.col-done` on the dashboard rows; persist `{slug: true}` map under `localStorage.crackd_progress`.
2. Above the table, render `Solved: X / Y (Z%)` summary that updates on toggle.
3. No server sync — purely local.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Write Playwright (or manual checklist if no test infra) smoke test: dashboard loads, problems render, lesson opens — used as regression guard | 45 min | — |
| 2 | Phase 1: add `:focus-visible`, `alt` text, badge `aria-label`, contrast fix | 1 hr | 1 |
| 3 | Phase 1: keyboard walk + fix focus order issues | 30 min | 2 |
| 4 | Phase 2: add transition tokens + apply to interactive classes | 45 min | 2 |
| 5 | Phase 2: tab-pane fade-in + cursor audit | 30 min | 4 |
| 6 | Phase 3: search + filter UI + wire to render loop | 2 hr | 1 |
| 7 | Phase 3: empty-state + loading-state rendering | 30 min | 6 |
| 8 | Phase 4: refactor `:root` into themed blocks; add dark palette | 1 hr | 1 |
| 9 | Phase 4: theme toggle + localStorage + no-flash boot script | 1 hr | 8 |
| 10 | Phase 4: propagate toggle to lesson pages (coordinate with PLAN-011 template) | 45 min | 9 |
| 11 | Phase 5: add `≤480px` and `481–1024px` breakpoints; manual verify at 3 sizes | 1.5 hr | 4 |
| 12 | Phase 6: progress checkbox column + localStorage + summary line | 1 hr | 6 |
| 13 | Update `static/CLASSES.md` with new classes (`.empty-state`, `.loading-state`, `.theme-toggle`, `.col-done`, `.search-bar`, `.filter-bar`) | 20 min | 6, 9, 12 |
| 14 | Update `AGENT_MD/plan/current_state_report.md` (UI maturity section) | 20 min | 2–12 |
| 15 | Update `README.md` user-facing feature list (search, dark mode, progress) | 15 min | 6, 9, 12 |
| 16 | Update `lessons/LESSON_DESIGN.md` if dark-mode propagation changes template requirements | 15 min | 10 |
| 17 | Write `REPORT-014_uiux_polish.md` per `rules.md` §4 | 30 min | all |

Total estimate: ~12 hours, splittable across 4–6 sessions by phase.

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Dark mode palette uglifies the warm-cream brand identity | Medium | Medium | Prototype dark palette in a single lesson first; show side-by-side before propagating |
| Lesson-template change for theme toggle conflicts with PLAN-011 generation pipeline | Medium | High | Confirm with PLAN-011 owner / read the generation skill before editing template; add toggle via a single shared `<script src>` if possible |
| Client-side filter performance on large problem lists | Low | Low | Current list is < 200 items; debounce search input at 150ms if needed |
| `localStorage` quotas / privacy mode browsers | Low | Low | Wrap reads/writes in try/catch; fall back to in-memory state silently |
| Breakpoint changes break the existing 1270px desktop layout | Low | Medium | Add new media queries only; do not modify the desktop default block |
| Contrast darkening of `--text3` makes "secondary" text look primary | Low | Low | Adjust by minimum amount needed to hit 4.5:1; verify visually |

---

## 7. Success criteria

- [ ] **G1:** Manual axe DevTools (or equivalent) scan on dashboard + one lesson page reports zero "critical" or "serious" violations.
- [ ] **G2:** Keyboard-only walk completes: open dashboard → tab to search → tab to a row → Enter opens lesson → tab through lesson controls → Esc returns. No focus traps.
- [ ] **G3:** Every interactive class in `static/CLASSES.md` has a transition declared; tab-pane fade-in observed in DevTools timeline.
- [ ] **G4:** Search filters live as user types; difficulty + topic selects compose correctly; empty state renders when no matches.
- [ ] **G5:** Theme toggle flips dashboard and lesson; reload preserves choice; no white flash on dark-mode load.
- [ ] **G6:** Layouts verified at 375, 768, 1280 widths with no horizontal scroll and no overlapping elements.
- [ ] **G7:** Toggling "done" persists across reload; summary line updates immediately.
- [ ] `REPORT-014_uiux_polish.md` written per `rules.md` §4 with goals-vs-actuals table.
- [ ] `current_state_report.md` UI section updated.
- [ ] No regressions in existing rendered lessons (spot-check 5 lessons after each phase).

---

## 8. Files to be created or updated

### 8.1 Markdown files (documentation)

| File | Change | Why |
|------|--------|-----|
| `AGENT_MD/plan/plans/PLAN-014_uiux_polish.md` | **Create** | This plan |
| `AGENT_MD/plan/reports/REPORT-014_uiux_polish.md` | **Create** (at end) | Per `rules.md` §4 |
| `AGENT_MD/plan/current_state_report.md` | **Update** | Reflect new UI maturity, dark-mode availability, accessibility status |
| `static/CLASSES.md` | **Update** | Document new classes added in Phases 3–6 |
| `README.md` | **Update** | Surface user-visible features: search/filter, dark mode, progress tracking |
| `lessons/LESSON_DESIGN.md` | **Update (conditional)** | Only if Phase 4 changes the lesson template contract |
| `lessons/design/*.md` | **No change expected** | Per CLAUDE.md, load only when authoring matching sections; this plan doesn't author lesson content |

### 8.2 Code files

| File | Change | Phase |
|------|--------|-------|
| `dashboard/index.html` | Inline-CSS + DOM edits (focus styles, search/filter UI, theme toggle, progress column, breakpoints) | 1, 2, 3, 4, 5, 6 |
| `static/lesson.css` | Add focus styles, transition tokens, dark-mode `:root[data-theme="dark"]`, new breakpoints | 1, 2, 4, 5 |
| Lesson template (per PLAN-011 generation pipeline) | Inject theme-toggle markup once; verify generation still works | 4 |

---

## 9. References

- `AGENT_MD/plan/rules.md` — document conventions followed by this plan
- `AGENT_MD/plan/current_state_report.md` — project state snapshot to be updated
- `AGENT_MD/plan/plans/PLAN-005_dashboard.md` — original dashboard plan (context for current structure)
- `AGENT_MD/plan/plans/PLAN-011_lesson_gen_efficiency.md` — lesson generation pipeline that Phase 4 must coordinate with
- `static/lesson.css` — shared lesson stylesheet
- `static/CLASSES.md` — CSS class reference
- `dashboard/index.html` — single-file dashboard
- WCAG 2.1 AA contrast guidelines (external, no link per project policy)
