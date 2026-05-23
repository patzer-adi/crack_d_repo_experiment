# Shared Static Assets — Migration Plan

## Goal

Extract common CSS and JS from the following GOLDEN lesson HTML files into two shared files.
1. lessons/permutation-in-string/lesson.html
2. lessons/trapping-rain-water/lesson.html
3. lessons/container-with-most-water/lesson.html
4. lessons/3sum/lesson.html

New lessons only write problem-specific content — step generators and HTML sections.
Token cost per lesson drops ~70%.

## Target file structure

```
crack_d/
├── static/
│   ├── lesson.css          ← all shared styles (extracted once)
│   └── lesson.js           ← all shared functions (extracted once)
├── lessons/
│   ├── 3sum/lesson.html
│   ├── permutation-in-string/lesson.html
│   ├── trapping-rain-water/lesson.html
│   └── container-with-most-water/lesson.html
└── ...
```

## Step 1 — Create static/lesson.css

Extract the CSS block from `lessons/3sum/lesson.html` (the most complete reference).
Copy everything inside the `<style>` tag verbatim into `static/lesson.css`.

This includes: `:root` variables, `body`, `.header`, `.section`, `.infobox`, `.asgrid`,
`.acard`, `.chain-box`, `.skeleton`, `.wt-item`, `.algo-steps`, `.bf-*`, `.cv-split`,
`.cv-code-panel`, `.cv-line`, `.cv-state-panel`, `.cv-var-grid`, `.cv-var-card`,
`.cv-narration`, `.arr-strip`, `.as-*`, `.panels-fixed`, `.formula-panel`, `.step-panel`,
`.ctrl-row`, `.ctrl-btn`, `.ex-btn`, `.kbd-hint`, `.corner`, `.checklist`, `.tab-bar`,
`.tab-pane`, `.cplx-grid`, `.ccard`, `.takehome`, `.legend`, all `@media` queries.

**Do not** include any problem-specific styles (e.g. `.bf-bar-con` bar chart styles that
only exist in rain water — those stay inline in their lesson).

## Step 2 — Create static/lesson.js

Extract the shared JS functions from the lessons. These are identical across all lessons:

```javascript
// Controls — copy exactly from any golden lesson
function toggleEl(id, btn) { ... }
function switchTab(idx) { ... }

// Keyboard routing — copy exactly
function visPx(el) { ... }
document.addEventListener('keydown', e => { ... });

// Shared render helpers
function cvBuildCode(lines) { ... }      // builds the code panel from a lines array
function cvStopPlay() { ... }
function cvTogglePlay(bplayId, timer) { ... }
function drStopPlay() { ... }
function drTogglePlay(bplayId, timer) { ... }
function bfStopPlay() { ... }
function bfTogglePlay(bplayId, timer) { ... }
```

Note: `cvRender`, `drRender`, `bfRender` are NOT shared — they differ per problem
because the variable cards and strip visualizations are problem-specific.

## Step 3 — Refactor each existing lesson HTML

For each of the four golden lessons, replace the `<style>` block and shared JS with:

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Problem Name — Interactive Lesson</title>
  <link rel="stylesheet" href="../../static/lesson.css">
  <!-- problem-specific styles only, if any -->
  <style>
    /* only styles unique to this problem */
    /* e.g. .bf-bar-con for rain water bar chart */
  </style>
</head>
<body>
  <!-- all HTML sections unchanged -->

  <script src="../../static/lesson.js"></script>
  <script>
    /* PROBLEM-SPECIFIC ONLY — everything below differs per lesson */

    const EXAMPLES = [ ... ];           // input data
    const BF_EXAMPLES = [ ... ];        // brute force examples

    // Step generators — always unique per problem
    function cvGen(input) { ... }       // code visualization steps
    function drGen(input) { ... }       // dry run steps
    function bfGen(input) { ... }       // brute force steps

    // Render functions — unique per problem (different variable cards)
    function cvRender(st) { ... }
    function drRender(st) { ... }
    function bfRender(st) { ... }

    // Load functions — call shared play/stop, then problem render
    function cvLoadEx(idx) {
      cvStopPlay();
      cvCur = 0;
      [0,1,2].forEach(i => document.getElementById('cv-ex'+i).classList.toggle('active',i===idx));
      cvSteps = cvGen(EXAMPLES[idx]);
      cvBuildCode(CV_LINES);
      cvRender(cvSteps[0]);
    }
    // ... drLoadEx, bfLoadEx similarly

    // Init
    bfLoadEx(0);
    cvLoadEx(0);
    drLoadEx(0);
  </script>
</body>
```

## Step 4 — Update server.py

Verify `server.py` already serves files from `static/` — it serves all static files so
this should work with no changes. Test by opening one refactored lesson in the browser.

## Step 5 — Update LESSON_DESIGN.md

Add a note at the top:

```
## Shared assets

Do NOT generate lesson.css or the shared JS functions.
They live in static/lesson.css and static/lesson.js.
Every lesson HTML imports them with:
  <link rel="stylesheet" href="../../static/lesson.css">
  <script src="../../static/lesson.js"></script>

Only write:
- Problem-specific inline <style> (if any unique styles needed)
- EXAMPLES and BF_EXAMPLES data
- cvGen(), drGen(), bfGen() step generators
- cvRender(), drRender(), bfRender() render functions
- CV_LINES code line array
- LoadEx functions and init calls
```

## What stays in each lesson HTML (the only unique parts)

| Item | Shared? |
|------|---------|
| `:root` CSS variables | YES → lesson.css |
| All `.section`, `.infobox`, `.wt-item` etc. styles | YES → lesson.css |
| Problem-specific bar chart / strip styles | NO → inline |
| `toggleEl`, `switchTab`, keyboard handler | YES → lesson.js |
| `cvBuildCode`, play/stop/toggle functions | YES → lesson.js |
| `EXAMPLES` data | NO → inline |
| `cvGen`, `drGen`, `bfGen` step generators | NO → inline |
| `cvRender`, `drRender`, `bfRender` | NO → inline (diff per problem) |
| All HTML section content | NO → inline |

## Token savings per new lesson

| Before | After |
|--------|-------|
| ~400 lines CSS | ~0 lines CSS |
| ~200 lines shared JS | ~0 lines shared JS |
| ~150 lines step generators | ~150 lines step generators |
| ~250 lines HTML | ~250 lines HTML |
| **~1000 lines total** | **~400 lines total** |

Approximately 60% reduction in tokens per lesson generation.

## Implementation order

1. Create `static/lesson.css` from 3sum lesson
2. Create `static/lesson.js` with shared functions
3. Refactor `3sum/lesson.html` — test in browser, verify identical appearance
4. Refactor remaining three lessons one at a time, testing each
5. Update `LESSON_DESIGN.md` with shared assets note
6. Generate next lesson using the new slim template — verify it works
