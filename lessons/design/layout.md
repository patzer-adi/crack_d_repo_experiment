# Cross-cutting — Layout, sizing, keyboard

## Principles (from v2 §22, §23, §24)

### Formula panel: fixed height, no layout shift
The `.panels-fixed` grid uses `grid-template-rows: 175px 110px` — fixed heights for the formula panel and step panel respectively. **This prevents the controls from jumping** as content changes, which is disorienting during step-through. The formula panel and step panel must never change height between steps.

If a panel's content threatens to overflow, shrink the font size or restructure the panel. Do not let it auto-grow.

### Use full page width
`body { max-width: 1100px }`. The code visualization and dry run both require two side-by-side panels. At 780px these feel cramped and produce horizontal scrollbars inside panels. **1100px is the minimum at which the layout breathes.**

This is enforced in `static/lesson.css` — do not override per lesson.

### Route keyboard shortcuts to the visible section
One global `keydown` handler, routing `←` / `→` / `Space` / `R` to whichever interactive section (`.cv-section` or `.dr-section`) has more pixels visible in the viewport. Uses `getBoundingClientRect()` to compare. The reader should never have to think about which widget has focus — **the keys follow their eyes**.

The router is implemented in `static/lesson.js` (see PLAN-010). Do not duplicate it per lesson.

## Per-lesson overrides

The only layout knob a lesson may override:

- Play speed for `bf`, `cv`, `dr` widgets. Defaults: 300 / 900 / 1100 ms. To override, define a problem-specific `bfTogglePlay` / `cvTogglePlay` / `drTogglePlay` in the inline `<script>` *before* the shared `<script src="../../static/lesson.js"></script>` is loaded.

## Mobile

`static/lesson.css` ships two breakpoints:

- `@media (max-width: 680px)` — collapses two-column grids to one (`.cv-split`, `.asgrid`, `.cplx-grid`), and reflows `.formula-grid` to 3 columns.
- `@media (max-width: 480px)` (phone, PLAN-020) — trims body side padding, scales the largest type down, reflows `.formula-grid` to 2 columns, lets long inline `code` / words wrap (`overflow-wrap`/`word-break`), hides the keyboard-only `.kbd-hint`, and **relaxes `.panels-fixed` to `auto` row heights** so the formula/step panels can grow instead of clipping. (The fixed 175px/110px heights exist to stop layout jump during *desktop* keyboard step-through; on a phone the panels stack and scroll, so the jump concern does not apply.)

Per-lesson markup must not introduce new fixed widths that break these rules. If a problem-specific visual is intrinsically wide (a bar chart of fixed-width cells, an absolutely-positioned timeline), either size it from the container's `clientWidth` or give its container `overflow-x: auto` so it scrolls inside its box rather than the page.

**Gate:** `scripts/render_check.mjs` asserts no horizontal page overflow at **both** 1000px (desktop) and 390px (phone). It re-drives the animations at phone width, so width-reactive renders are measured the way a phone visitor sees them.
