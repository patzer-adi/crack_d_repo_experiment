# Section 2 — Step 1: Brute force

> **Status (2026-05-21):** Canonical scaffold below is **required**. The
> `schema:§2 canonical *` lint rules (PLAN-019) fail any lesson that deviates
> on element ids, button onclick handlers, or function names. Same chassis as
> §6 / §7 but with the `bf-` prefix. Note: BF uses `bf-play` (no `-b` prefix),
> unlike CV/DR which use `cv-bplay` / `dr-bplay`.

## Canonical scaffold (required)

```html
<!-- ═══ SECTION 2: BRUTE FORCE ═══ -->
<div class="section">
  <p class="sec-label">Step 1</p>
  <p class="sec-title">Brute force — feel the cost</p>
  <p class="body">[ one-paragraph framing: what the brute force does + its cost. ]</p>

  <div class="ctrl-row" style="margin-top:.75rem">
    <button class="ex-btn active" id="bf-ex0" onclick="bfLoadEx(0)">[label 1]</button>
    <button class="ex-btn"        id="bf-ex1" onclick="bfLoadEx(1)">[label 2]</button>
    <button class="ex-btn"        id="bf-ex2" onclick="bfLoadEx(2)">[label 3]</button>
  </div>
  <!-- Problem-specific visualization here (array, matrix, hash table, etc.) -->
  <!-- + state-line: i, j, sum, ops, etc. -->
  <div class="ctrl-row" style="margin-top:.5rem">
    <button class="ctrl-btn"     id="bf-prev" onclick="bfPrev()">← Prev</button>
    <button class="ctrl-btn pri" id="bf-play" onclick="bfTogglePlay()">▶ Auto</button>
    <button class="ctrl-btn"     id="bf-next" onclick="bfNext()">Next →</button>
    <button class="ctrl-btn"                  onclick="bfReset()">↺ Reset</button>
    <span class="step-ctr" id="bf-sctr"></span>
  </div>
  <div class="infobox danger" style="margin-top:.875rem">
    <p class="infobox-t" style="color:var(--text-danger)">Cost: O(...) time, O(...) space</p>
    <p class="infobox-d">[ why this is slow — the "checks" counter makes it visible. ]</p>
  </div>
  <button class="reveal-btn" onclick="toggleEl('code-bf',this)">▶ Reveal Code</button>
  <div id="code-bf" class="code-block"><pre class="cb">[ brute force C++ ]</pre></div>
</div>
```

### Required ids

| id | Purpose |
|---|---|
| `bf-ex0`, `bf-ex1`, `bf-ex2` | Three example switch buttons |
| `bf-play` | Auto/Play button (static/lesson.js' bfTogglePlay looks for this exact id — note no `-b` prefix) |
| `bf-sctr` | Step counter span (`Step N / total`) |

### Required functions

```js
function bfNext()  { /* if (bfCur < bfSteps.length - 1) { bfCur++; bfRender(bfSteps[bfCur]); } else bfStopPlay(); */ }
function bfPrev()  { /* if (bfCur > 0) { bfCur--; bfRender(bfSteps[bfCur]); } */ }
function bfReset() { /* bfStopPlay(); bfCur = 0; bfRender(bfSteps[0]); */ }
function bfLoadEx(idx)   { /* set active ex-btn, regenerate steps, bfCur=0, bfRender */ }
function bfGenSteps(...) { /* problem-specific O(n²) or O(n³) trace */ }
function bfRender(st)    { /* reflects state; updates bf-sctr; toggles bf-prev/bf-next disabled */ }
// bfTogglePlay / bfStopPlay are provided by static/lesson.js — do NOT redefine.
```

### Anti-patterns (lint fails)

- ❌ Local `bfTogglePlay` redefinition (use static.js's)
- ❌ `<button>■ Stop</button>` — no Stop in canonical
- ❌ Skipping the cost infobox — the "feel the cost" point requires the explicit O(n²) / O(n³) framing
- ❌ Static dump only (no Prev/Next/step counter) — every BF must be steppable

## Principles (from v2 §9, §10, §13)

### Get the first animation in front of the reader fast
The brute-force animation is the first thing that moves. A reader who scrolls past three sections of prose before seeing anything interactive will lose focus. The widget is small, auto-playable, and immediately shows why the naive approach is slow.

### Show the cost, not just the answer
The animation must make O(n²) or O(n³) visible. For 3Sum that means three nested loop indices stepping through all combinations with a live "checks" counter. For Trapping Rain Water that means the left scan and right scan for each bar. **The counter is the point** — the reader must *feel* why this is slow before the optimisation feels worthwhile.

### Hide code behind a reveal button
Even brute-force code is collapsed by default with a "▶ Reveal Code" button. A reader scanning for intuition should never be forced to scroll past C++. The reveal button signals "this is available when you're ready" without imposing it.

## Markup

- Container: `<div class="section">` with `.sec-label` "Step 1" and `.sec-title` "Brute force …".
- Animation panel: problem-specific layout. For array problems use `.bf-nums` containing `.bf-num` cells with classes `.bi`/`.bj`/`.bk` for the active indices and `.bmatch` for matches.
- Counter: visible `<span>` updating every animation tick. Label it clearly ("Checks", "Comparisons", "Scans").
- Controls: `.ctrl-row` with prev / play / next / reset buttons + example switcher (`.ex-btn`).
- Code reveal: `<button class="reveal-btn">` toggling `<div class="code-block">` → `.open`.

## Step generator

`bfGen(input)` returns an array of step objects. Each object describes the variables at that tick. The renderer (`bfRender(st)`) is purely visual: it never computes — it reflects state.

Default play speed: 300ms (overridable per lesson — see PLAN-010 notes in `static/lesson.js`).

## Pitfalls

- Do not animate brute force at the same speed as the optimised dry run. Brute force is **deliberately tedious** — speed 300ms is the default but slower for high-cost algorithms.
- Do not skip showing the failing combinations. The reader needs to see (i,j,k) tuples that produce non-zero sums before seeing the one that doesn't.

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 144–193 |
| Sliding-window | `lessons/permutation-in-string/lesson.html` | 251–297 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 163–205 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 215–267 |
