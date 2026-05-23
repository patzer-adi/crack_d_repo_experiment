# Section 6 — Step 5: Code visualization

> **Status (2026-05-21):** Canonical scaffold below is **required**. The
> `schema:cv canonical scaffold` lint rule (PLAN-019) fails any lesson that
> deviates on button set, function names, or element ids. Sec 6 used to be
> principles-only; we are now contractual about the chassis because lessons
> generated from older scaffolds drifted on every visible axis (different
> button labels, different speeds, no keyboard support, ad-hoc state panels).

## Canonical scaffold (required)

Every `.cv-section` MUST use this exact HTML chassis. Algorithm-specific
content varies (which variables to show, whether an array preview sits below
the cv-split, etc.) but the structural elements below are checked by lint and
cannot be renamed or omitted.

```html
<!-- ═══ SECTION 6: CODE VISUALIZATION ═══ -->
<div class="section cv-section">
  <p class="sec-label">Step 5</p>
  <p class="sec-title">Code visualization — line by line</p>
  <p class="body">[ one-paragraph intro: what the reader is about to watch. ]</p>

  <div class="cv-split">
    <div id="cv-code-panel" class="cv-code-panel"><!-- built by cvBuildCode(CV_LINES) --></div>
    <div class="cv-state-panel">
      <div id="cv-var-grid" class="cv-var-grid">
        <!-- ≥ 3 variable cards. Each card: -->
        <div class="cv-var-card dim" id="cv-v-<name>">
          <div class="cv-var-name"><name></div>
          <div class="cv-var-val">—</div>
        </div>
        <!-- ... more cards ... -->
      </div>
      <!-- Optional: per-lesson auxiliary panel (hash table, freq[26], etc.) -->
      <div id="cv-narration" class="cv-narration">Press ▶ Auto or use the arrow keys to walk through.</div>
    </div>
  </div>

  <!-- Optional: full-width problem-specific visual under cv-split
       (array cells, matrix grid, interval timeline, etc.) -->
  <div id="cv-arr-con" style="background:var(--bg2);border:0.5px solid var(--border2);border-radius:var(--r2);padding:.875rem 1rem;margin:.875rem 0;"></div>

  <div class="ctrl-row" style="margin-top:.75rem">
    <button class="ex-btn active" id="cv-ex0" onclick="cvLoadEx(0)">[label 1]</button>
    <button class="ex-btn"        id="cv-ex1" onclick="cvLoadEx(1)">[label 2]</button>
    <button class="ex-btn"        id="cv-ex2" onclick="cvLoadEx(2)">[label 3]</button>
  </div>
  <div class="ctrl-row" style="margin-top:.5rem">
    <button class="ctrl-btn"     id="cv-bprev" onclick="cvPrev()">← Prev</button>
    <button class="ctrl-btn pri" id="cv-bplay" onclick="cvTogglePlay()">▶ Auto</button>
    <button class="ctrl-btn"     id="cv-bnext" onclick="cvNext()">Next →</button>
    <button class="ctrl-btn"                   onclick="cvReset()">↺ Reset</button>
    <span class="step-ctr" id="cv-sctr"></span>
    <span class="kbd-hint">keys <kbd>←</kbd> <kbd>→</kbd> <kbd>Space</kbd> <kbd>R</kbd></span>
  </div>
</div>
```

### Required ids (lint asserts)

| id | Purpose |
|---|---|
| `cv-code-panel`   | Code lines target for `cvBuildCode` |
| `cv-var-grid`     | Variable card container |
| `cv-narration`    | Per-step prose box |
| `cv-ex0`, `cv-ex1`, `cv-ex2` | Three example switch buttons |
| `cv-bprev`        | "← Prev" button (`disabled` toggled by cvRender) |
| `cv-bplay`        | "▶ Auto" play/pause button (referenced by static/lesson.js) |
| `cv-bnext`        | "Next →" button (`disabled` toggled by cvRender) |
| `cv-sctr`         | Step counter span (`Step N / total`) |

### Required functions

Each lesson must define these at top-level so static/lesson.js' keyboard
handler and play loop can find them. Naming is fixed (the static code is
not parameterised):

```js
function cvNext()        { /* if (cvCur < cvSteps.length - 1) { cvCur++; cvRender(cvSteps[cvCur]); } else cvStopPlay(); */ }
function cvPrev()        { /* if (cvCur > 0) { cvCur--; cvRender(cvSteps[cvCur]); } */ }
function cvReset()       { /* cvStopPlay(); cvCur = 0; cvRender(cvSteps[0]); */ }
function cvLoadEx(idx)   { /* sets active ex-btn, cvSteps = cvGenSteps(...), cvCur = 0, cvRender */ }
function cvGenSteps(...) { /* returns the step list — see "Step shape" below */ }
function cvRender(st)    { /* see "Render contract" below */ }
// cvTogglePlay / cvStopPlay are provided by static/lesson.js — do NOT redefine.
```

### Keyboard support

Provided by `static/lesson.js` automatically — IF the canonical function names
are present:

| Key | Action |
|---|---|
| `←` Arrow | `cvPrev()` |
| `→` Arrow | `cvNext()` |
| `Space`   | `cvTogglePlay()` (from static.js) |
| `R` / `Esc` | `cvReset()` |

The kbd-hint span advertises this in the UI. **Always include it** so readers
discover the keyboard interface.

### Default play speed

**1400 ms per step** — provided by `cvTogglePlay` in `static/lesson.js`. Do
not redefine `cvTogglePlay` locally just to change the speed; if a specific
problem genuinely needs a different cadence, set it in cvRender (e.g. clear and
restart the interval) and document the deviation in the lesson plan.

## Step shape

```js
{
  line: 7,              // which code line is "active" — matches CV_LINES[i].n
  phase: 'p1',          // optional: 'init' | 'active' | 'match' | 'done' | <problem-specific>
  arr: [...],           // optional: snapshot of the mutable data structure at this step
  changed: ['i','num'], // optional: list of card ids (or var names) that just changed — drives `.hl`
  narr: '...',          // human-readable prose for the narration box
  // ... any other state the lesson tracks (e.g. swap partner, hash-map entries, etc.)
}
```

`cvGenSteps` should snapshot all visualizable state into the step (`arr:
[...arr]` — pass-by-value). The renderer **never mutates or computes**; it
only reflects whatever is in the step.

## Render contract

```js
function cvRender(st) {
  // 1. Active code line
  document.querySelectorAll('#cv-code-panel .cv-line').forEach(el => el.classList.remove('active', 'active-match'));
  const lineEl = document.getElementById('cvL' + st.line);
  if (lineEl) lineEl.classList.add(st.phase === 'match' || st.phase === 'done' ? 'active-match' : 'active');

  // 2. Variable cards
  //    For each card: clear .hl/.hl-match/.dim, set value, then re-add .hl
  //    if its name is in st.changed, .hl-match if this step is the success
  //    moment for that card, or .dim if value is '—'.

  // 3. Narration box
  //    .cv-narration; add .is-active during normal steps, .is-match on
  //    terminal/success steps.

  // 4. Problem-specific visual (array, matrix, hash table)
  //    Redraw from st.arr (or st.matrix / st.seen / etc.). Never assume
  //    the previous render's state is still there — full repaint.

  // 5. Step counter + button enable state
  document.getElementById('cv-sctr').textContent = `Step ${cvCur + 1} / ${cvSteps.length}`;
  const bp = document.getElementById('cv-bprev'); if (bp) bp.disabled = cvCur === 0;
  const bn = document.getElementById('cv-bnext'); if (bn) bn.disabled = cvCur === cvSteps.length - 1;
}
```

## Variable cards — dim/highlight discipline

The dim/highlight pattern teaches **execution order**:

- A card starts dimmed (`opacity: 0.32` via `.dim`) and shows `—`.
- It gains `.hl` (cyan background) on the step that **assigns** it.
- On the step its value **leads to the answer**, it gains `.hl-match` (green).
- It loses `.hl`/`.hl-match` on subsequent steps when nothing changed.

A reader watching auto-play sees the cards light up in the order the algorithm
actually computes — which is more important than just "what is i right now."

## Problem-specific visual (optional)

If the algorithm's state is too large for variable cards (an n-element array,
an m×n matrix, a hash table), render it as a full-width visual below the
cv-split. Use canonical CSS variables for highlights:

- `var(--bg-info)` / `var(--border-info)` / `var(--text-info)` — current cursor / cell under inspection
- `var(--bg-success)` / `var(--border-success)` / `var(--text-success)` — finalised / matched value
- `var(--bg-warn)`    / `var(--border-warn)`    / `var(--text-warn)`    — pivot / swap partner / restart
- `var(--bg-danger)`  / `var(--border-danger)`  / `var(--text-danger)`  — invalid / out-of-range value

Do not hard-code hex colors. Lint flags any `#[0-9a-f]{3,6}` in `.cv-section`.

## Anti-patterns (lint will fail)

- ❌ `cvNextStep()` — must be `cvNext()` (static.js calls `cvNext`)
- ❌ Local `cvTogglePlay` redefinition (use static.js's; change cadence via cvRender if needed)
- ❌ `<button>■ Stop</button>` — no Stop button; Reset replaces it
- ❌ `<div class="step-ctr"><span id="cv-step-num">…</span>/<span id="cv-step-max">…</span></div>` — use `<span class="step-ctr" id="cv-sctr">` and write `Step N / total` into it
- ❌ Only 2 example buttons — must be 3 (fast / typical / edge)
- ❌ Hard-coded hex colors in `.cv-section` — use canonical CSS vars
- ❌ State panel built with inline-styled `<div>`s — use `cv-var-grid` + `cv-var-card`

## Reference

`lessons/two-sum/lesson.html` §6 (lines 316–354 + cvRender at 808–847) is the
canonical reference. `lessons/first-missing-positive/lesson.html` §6 is the
canonical reference for the **with-array-preview** variant.
