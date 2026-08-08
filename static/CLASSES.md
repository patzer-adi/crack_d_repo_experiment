# CSS class vocabulary — `static/lesson.css`

Feed this file to the lesson generator instead of the full CSS. Every class a lesson is allowed to use is listed here with a one-line purpose. Classes not listed are either problem-specific (inline `<style>`) or do not exist.

## Page frame

- `.header` / `.header-eyebrow` / `.header-meta` — top banner with title + LC link + badges
- `.badge` / `.badge-med` / `.badge-arr` — small inline tags (difficulty, topic)
- `.section` — top-level section container with bottom border
- `.section.cv-section` — section housing code visualization (keyboard router target)
- `.section.dr-section` — section housing dry run (keyboard router target)
- `.sec-label` — eyebrow above section title
- `.sec-title` — h2-equivalent section heading
- `p.body` — paragraph text

## Infobox

- `.infobox` / `.infobox-t` / `.infobox-d` — neutral panel with title + description
- `.infobox.success` / `.infobox.info` / `.infobox.danger` — colour variants

## Clarifying questions (§0)

- `.asgrid` — 2-col grid for clarifying cards
- `.acard` / `.acard-q` / `.acard-a` / `.acard-u` — Q / A / unlock (mono green) card

## Insight visuals (§1)

- `.number-line` / `.nl-wrap` / `.nl-num` / `.nl-label` — sorted array with index labels
- `.nl-num.fixed` / `.nl-num.ptr-l` / `.nl-num.ptr-r` / `.nl-num.match` — pointer states
- `.nl-label.f` / `.nl-label.l` / `.nl-label.r` — coloured pointer labels
- `.chain-box` / `.chain-row` / `.chain-sym` / `.chain-content` / `.chain-text` / `.chain-hl` / `.chain-note` / `.chain-example` — equivalence chain
- `.pill` / `.pill.ok` / `.pill.bad` / `.pill.n` — example pills
- `.arrow` — small mono arrow between pills

## Brute force (§2)

- `.bf-nums` / `.bf-num` / `.bf-idx` — index strip
- `.bf-num.bi` / `.bf-num.bj` / `.bf-num.bk` / `.bf-num.bmatch` — pointer states (i / j / k / match)

## Translations skeleton (§3)

- `.skeleton` — flex column container
- `.wt-item` / `.wt-num` / `.wt-body` / `.wt-name` / `.wt-desc` / `.wt-gain` — numbered translation card

## Algorithm in plain English (§4)

- `.algo-steps` / `.algo-step` / `.algo-n` / `.algo-t` — numbered procedure list

## Code (§5, §10)

- `pre.cb` — code block container
- `.kw` / `.fn` / `.cm` / `.nu` / `.tp` — syntax-highlight spans (keyword / function / comment / number / type)
- `.reveal-btn` — toggle button
- `.code-block` / `.code-block.open` — collapsible code container

## Code visualization (§6)

- `.cv-split` — 2-column grid
- `.cv-code-panel` — code panel (no scrollbar)
- `.cv-line` / `.cv-line.active` / `.cv-line.active-match` — line row + active highlight
- `.cv-line-num` / `.cv-line-code` — line-number + code spans
- `.cv-state-panel` — right column container
- `.cv-var-grid` — variable card grid
- `.cv-var-card` / `.cv-var-card.hl` / `.cv-var-card.hl-match` / `.cv-var-card.dim` — variable card states
- `.cv-var-name` / `.cv-var-val` — card text
- `.cv-narration` / `.cv-narration.is-match` / `.cv-narration.is-active` — per-step prose

## Dry run (§7)

- `.num-strip` / `.ns-wrap` / `.ns-idx` / `.ns-cell` / `.ns-lbl` — number strip
- `.ns-cell.fix` / `.ns-cell.pL` / `.ns-cell.pR` / `.ns-cell.done` — pointer states
- `.ns-lbl.f` / `.ns-lbl.L` / `.ns-lbl.R` — coloured pointer labels
- `.arr-strip` / `.as-wrap` / `.as-cell` / `.as-lbl` — bar-chart strip (CWMW pattern)
- `.as-cell.pL` / `.as-cell.pR` / `.as-cell.pbest` — bar pointer states
- `.panels-fixed` — fixed-height grid (175px formula, 110px step)
- `.formula-panel` / `.formula-panel.is-match` / `.formula-panel.is-squeeze` — formula display
- `.formula-grid` / `.fitem-label` / `.fitem-val` / `.fitem-sub` — formula cells
- `.formula-eq` / `.eq-hl` — equation line
- `.step-panel` / `.step-panel.match` / `.step-panel.squeeze` — step panel
- `.step-what` / `.step-why` — bold what + smaller why

## Controls

- `.ctrl-row` — flex row for controls
- `.ctrl-btn` / `.ctrl-btn.pri` — primary / secondary button
- `.ex-btn` / `.ex-btn.active` — example switcher button
- `.step-ctr` — "Step n/N" indicator
- `.kbd-hint` + `kbd` — keyboard shortcut hint

## Corner cases (§8)

- `.corner` / `.cnum` / `.corner-title` / `.corner-body` — numbered corner-case card

## Production checklist (§9)

- `.checklist` / `.chk-item` / `.chk-icon` / `.chk-text` — green-check checklist row

## Approaches (§10)

- `.tab-bar` / `.tab-btn` / `.tab-btn.active` — tab strip
- `.tab-pane` / `.tab-pane.active` — tab body
- `.tag` / `.tag-time` / `.tag-space` — complexity tags

## Complexity (§11)

- `.cplx-grid` / `.ccard` / `.ccard-l` / `.ccard-v` / `.ccard-n` — 2-card complexity grid

## Take home (§12)

- `.takehome` — left-accent block for related-problems list

## Legend (any section)

- `.legend` / `.leg-item` / `.leg-dot` / `.leg-label` — colour-key strip

## Algorithm lessons only — `static/algo.css` (PLAN-027)

Loaded **in addition to** `lesson.css` by `algorithms/<id>/lesson.html`. LC lessons
under `lessons/` never load it. Painted by `gvPaint` / `dpPaint` / `stripPaint` in
[`static/algo.js`](./algo.js) — do not hand-roll the SVG in a lesson.

- `.gv-wrap` / `.gv-svg` — scroll guard + the viewBox SVG that scales to any width
- `.gv-edge` / `.hot` / `.tree` / `.bad` / `.dim` — edge states (looking at it / kept / rejected / faded)
- `.gv-node` / `.cur` / `.queue` / `.seen` / `.bad` — node states (current / waiting / settled / failed)
- `.gv-id` / `.gv-lbl` / `.gv-lbl.on` / `.gv-w` / `.gv-w.hot` — node id, node caption, edge weight
- `.gv-legend` / `.gv-cap` / `.gv-counter` — colour key, mono caption line, live cost counters
- `.gv-strip` / `span.set` / `span.cur` — chip row for a per-node array (dist[], parent[], …)
- `.dp-wrap` / `.dp-table` — DP table with row/column headers, scrolls inside its own wrapper
- `.dp-table td` states: `.set` / `.cur` / `.src` / `.best` / `.bad` / `.dim`

## Layout & mobile

- `body` is capped at 1100px (do not override; see `design/layout.md`).
- `@media (max-width: 680px)` collapses two-column grids — do not introduce new fixed widths that break this.
- `@media (max-width: 480px)` (phone, PLAN-020) trims padding, scales type down, wraps long `code`, hides `.kbd-hint`, and relaxes `.panels-fixed` to auto heights. Keep problem-specific wide visuals container-sized or wrap them in `overflow-x: auto`. The render gate enforces no overflow at 390px — see `design/layout.md` §Mobile.

## Notes

- Do not invent new class names without adding them here. If you find yourself wanting a new class, prefer inline `<style>` in the lesson HTML (problem-specific markup) and document the class in this file when it has reused in ≥ 2 lessons (then move to `static/lesson.css`).
- This file is the **input** the lesson generator should receive. Do not include `static/lesson.css` in generation prompts.
