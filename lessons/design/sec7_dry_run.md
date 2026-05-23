# Section 7 — Step 6: Dry run

> **Status (2026-05-21):** Canonical scaffold below is **required**. The
> `schema:§7 canonical *` lint rules (PLAN-019) fail any lesson that deviates
> on element ids, button onclick handlers, or function names. Same chassis as
> §6 / §2 but with the `dr-` prefix.

## Canonical scaffold (required)

```html
<!-- ═══ SECTION 7: DRY RUN ═══ -->
<div class="section dr-section">
  <p class="sec-label">Step 6</p>
  <p class="sec-title">[ section heading ]</p>
  <!-- ... problem-specific visual + state panels ... -->

  <div class="ctrl-row" style="margin-top:.75rem">
    <button class="ex-btn active" id="dr-ex0" onclick="drLoadEx(0)">[label 1]</button>
    <button class="ex-btn"        id="dr-ex1" onclick="drLoadEx(1)">[label 2]</button>
    <button class="ex-btn"        id="dr-ex2" onclick="drLoadEx(2)">[label 3]</button>
  </div>
  <div class="ctrl-row" style="margin-top:.5rem">
    <button class="ctrl-btn"     id="dr-bp"    onclick="drPrev()">← Prev</button>
    <button class="ctrl-btn pri" id="dr-bplay" onclick="drTogglePlay()">▶ Auto</button>
    <button class="ctrl-btn"     id="dr-bn"    onclick="drNext()">Next →</button>
    <button class="ctrl-btn"                   onclick="drReset()">↺ Reset</button>
    <span class="step-ctr" id="dr-sctr"></span>
  </div>
  <p class="kbd-hint"><kbd>←</kbd><kbd>→</kbd> step &nbsp;<kbd>Space</kbd> auto/pause &nbsp;<kbd>R</kbd> reset</p>
</div>
```

### Required ids

| id | Purpose |
|---|---|
| `dr-ex0`, `dr-ex1`, `dr-ex2` | Three example switch buttons |
| `dr-bplay` | Auto/Play button (static/lesson.js' drTogglePlay looks for this exact id) |
| `dr-sctr`  | Step counter span (`Step N / total`) |

### Required functions

```js
function drNext()  { /* if (drCur < drSteps.length - 1) { drCur++; drRender(drSteps[drCur]); } else drStopPlay(); */ }
function drPrev()  { /* if (drCur > 0) { drCur--; drRender(drSteps[drCur]); } */ }
function drReset() { /* drStopPlay(); drCur = 0; drRender(drSteps[0]); */ }
function drLoadEx(idx)   { /* set active ex-btn, regenerate steps, drCur=0, drRender */ }
function drGenSteps(...) { /* problem-specific; returns step list */ }
function drRender(st)    { /* reflects state; updates dr-sctr; toggles dr-bp/dr-bn disabled */ }
// drTogglePlay / drStopPlay are provided by static/lesson.js — do NOT redefine.
```

### Anti-patterns (lint fails)

- ❌ `drNextStep()` — must be `drNext()` (static.js calls `drNext`)
- ❌ Local `drTogglePlay` redefinition
- ❌ `<button>■ Stop</button>` — no Stop in canonical
- ❌ `id="dr-play"` — must be `id="dr-bplay"` (static.js looks for the `-b` variant)
- ❌ Legacy `dr-step-num` + `dr-step-max` — use single `dr-sctr` span with `Step N / total` text

## Purpose: multi-example practice, distinct from §6 (PLAN-017)

§7 is **reader practice across multiple inputs**, not a re-walk of §6. The distinction:

| Section | What it shows | Reader's role |
|---|---|---|
| §6 Code Viz | **One** example tied to the optimal algorithm's code lines | Watch one execution; understand what each code line does |
| §7 Dry Run | **Three** different example inputs; reader picks any | Step through unfamiliar inputs to confirm they can predict the algorithm's behaviour |

The two sections share a step generator skeleton but differ in inputs and in what's emphasised: §6 highlights the active code line; §7 has no code panel, just state evolution across switchable examples.

**Minimum required:** at least **three** example buttons (`<button class="ex-btn" onclick="drLoadEx(0)">`...`<button class="ex-btn" onclick="drLoadEx(2)">`) wired to `drLoadEx(idx)` which resets state and re-renders. One example should be "fast" (3–5 steps for the full loop), one "slow" (10–15 steps showing the interesting behaviour), and one should hit a corner case (empty, single element, all-same, etc.).

Default auto-play speed: **1400 ms** (slower than §6's 1100 ms — the reader is forming their own prediction at each step, not following along).

## Principles (from v2 §11, §12, §19, §20, §28)

### Every example should have a "slow" and a "fast" one
Pick examples where one finishes in **3–5 steps** (lets the reader see the full loop quickly) and one takes **10–15 steps** (shows the sliding behaviour, the dedup logic, or the edge case). Wire both into an example switcher. The pacing difference alone teaches algorithm behaviour that a single example cannot.

### Prime / setup steps must be traced individually
Never collapse initialisation into a single step. If the algorithm has a priming phase (e.g. building the initial window in Permutation in String), trace each character of that phase individually. The reader needs to see `diff` adjusting character-by-character during priming — a single "after priming, diff=4" step teaches nothing.

### Show every diff / boundary-crossing case explicitly
For any update logic with multiple input combinations (e.g. the diff counter: `freq[x]--` with `old==1 → diff--`, `old==0 → diff++`), enumerate all cases and prove each one. The rules must not feel magical.

**Known invariant** for character-counting diff counters:

```
freq[x]-- (s2 character entering window):
  old==1 → slot goes 1→0: mismatch resolved → diff--
  old==0 → slot goes 0→-1: new mismatch    → diff++

freq[x]++ (s2 character leaving window):
  old==-1 → slot goes -1→0: mismatch resolved → diff--
  old==0  → slot goes 0→+1: new mismatch    → diff++
```

This inversion is easy to get backwards. Always verify with a Python trace before shipping (see `design/python_verify.md`).

### Two diff-scanner examples: one match, one mismatch
Whenever showing a diff counter being computed slot-by-slot, always show **two side-by-side panels** — one where the result is `diff=0` (permutation found) and one where `diff>0` (no match). A single example with diff=0 makes the counter seem trivial. The mismatch case is what makes the counter's purpose clear.

### Hard-reset all state on example switch
When the reader switches examples, every piece of state must reset: frequency arrays, diff counters, loop indices, result arrays, animation timers, variable card highlights. A partial reset that leaves stale state from the previous example is the most common source of subtle bugs in step generators. **Reset everything, always.**

## Markup

- Container: `<div class="section dr-section">`.
- Visual strip: `.num-strip` containing `.ns-wrap` cells; cell classes `.fix`, `.pL`, `.pR`, `.done` for pointer states; label classes `.ns-lbl.L`, `.ns-lbl.R`, `.ns-lbl.f`.
- Fixed panels: `<div class="panels-fixed">` with `<div class="formula-panel">` (175px) and `<div class="step-panel">` (110px) — heights are fixed to prevent layout shift (see `design/layout.md`).
- Formula panel internals: `.formula-grid` with `.fitem-label` + `.fitem-val` + `.fitem-sub` cells; `.formula-eq` for the equation underneath.
- Step panel internals: `.step-what` (bold what) + `.step-why` (smaller why).
- Controls: `.ctrl-row` with prev / play / next / reset; example switcher buttons (`.ex-btn`).

## Step generator

`drGen(input)` returns step objects. `drRender(st)` reflects them. Each step has:

```js
{ pointers: { L: 0, R: 5, fixed: 2 }, formula: { … }, what: '…', why: '…', phase: 'match' | 'squeeze' | 'check' }
```

Default play speed: **1400 ms** (per PLAN-017; was 1100 ms — slowed for reader-paced prediction).

## Reference excerpts

| Archetype | File | Lines |
|---|---|---|
| Two-pointer | `lessons/3sum/lesson.html` | 319–358 |
| Sliding-window (priming traced char-by-char) | `lessons/permutation-in-string/lesson.html` | 512–555 |
| Prefix-scan | `lessons/trapping-rain-water/lesson.html` | 334–378 |
| Divide-conquer | `lessons/median-of-two-sorted-arrays/lesson.html` | 397–440 |

Also load `design/known_bugs.md` (diff-counter inversion + collapsed-priming bugs).
