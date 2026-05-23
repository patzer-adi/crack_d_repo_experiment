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

`static/lesson.css` ships `@media (max-width: 680px)` rules that collapse two-column grids to one. Per-lesson markup should not introduce new fixed widths that break these rules.
