# REPORT-021: Prerequisites section — foundational knowledge layer

**Plan:** PLAN-021
**Completed:** 2026-06-05
**Author:** Claude (Opus 4.8) via Claude Code, pair-driven with the user

---

## 1. Summary

Added a fourth dashboard tab, **Prerequisites**, that names and explains the
foundational knowledge a learner should hold before attempting the 211 problems —
at three levels: data structures, core algorithms, and base concepts. It is backed
by a new `data/prerequisites.json` (16 entries) rendered as cards that reuse the
Patterns-tab card chrome, each with a plain-language analogy, a lucid explanation,
short code snippets, pitfalls, a complexity line, and a **topic-derived
"→ N problems" cascade** (zero edits to the problem records). Three cards (Hash
Map, Binary Search, Recursion) carry a lightweight inline step-animation from a
new `dashboard/prereq-anims.js`. A test-first data gate, `scripts/check_prerequisites.py`,
enforces the dataset contract — most importantly that every cascade topic is real,
so a prerequisite can never silently map to zero problems. The seed set covers
20/21 topics (208/211 problems, 98.6 %). Adding the 4th tab initially widened the
shared topbar past 390 px; this was fixed by letting the tab strip scroll inside
the topbar at ≤480 px, restoring zero horizontal overflow on every tab.

## 2. Goals vs. actuals

| Goal (from plan) | Outcome | Evidence |
|-------------------|---------|----------|
| **G1** New Prerequisites tab, `#prerequisites` route, no JS error | ✅ Met | Headless: tab renders, `tab-count` `(16)`, 0 console/uncaught errors (the only 404 is the browser's automatic `favicon.ico`, present on every tab) |
| **G2** ≥15 entries across 3 levels, ≥90 % problem coverage | ✅ Met | 16 entries (8 data-structure, 5 algorithm, 3 concept); `check_prerequisites.py` → coverage **208/211 (98.6 %)**, 20/21 topics |
| **G3** Each card: tagline, analogy, explanation, ≥1 snippet, cascade chip | ✅ Met | `buildPrereqCard` renders all; screenshots confirm; first chip `34 problems →` (array's 4 topics) computed live |
| **G4** Reuse the three `skills/ds/*.md` explainers | ✅ Met | array / linked-list / binary-tree mental-model prose migrated into the matching entries' `explanation`/`analogy` |
| **G5** 1–3 hero inline animations, no overflow | ✅ Met | 3 registered + mounted (`anim-hash-map`, `anim-binary-search`, `anim-recursion`); headless confirms each `.pre-anim` contains a live `.pa-stage`; stepped via Prev/Next |
| **G6** `check_prerequisites.py` passes | ✅ Met | Exit 0: unique kebab ids, required fields, level/group enums, real topics, registered animations, coverage |
| **G7** Zero horizontal overflow at 360/390 px on the tab | ✅ Met | Headless `delta = 0` at 390 and 360 px, in both `mobile:true` and `mobile:false` emulation, on all four tabs |
| **G8** Existing tabs unchanged; audits green | ✅ Met | Regression test vs committed HEAD: baseline delta 0 → mine delta 0 after the topbar fix; `audit_lessons.py` and `doctor.py` green (see §4) |

## 3. Changes made

### 3.1 Data + schema + gate (test-first)
- `scripts/check_prerequisites.py` — **written first** (ran red against the absent
  data file). Validates ids, required fields (read from the schema), `level`/`group`
  enums, non-empty snippets, that every `topics[]` value exists in `problems.json`,
  that referenced animation ids are registered in `prereq-anims.js`, and that
  problem coverage ≥ 90 %. Stdlib only.
- `data/prerequisites.schema.json` — JSON-Schema contract mirroring the
  `algorithms.schema.json` convention (required fields, `level` enum, snippet shape).
- `data/prerequisites.json` — 16 entries. Data structures: Array, Hash Map/Set,
  Linked List, Stack & Queue, Binary Tree & BST, Heap, Graph, Trie. Core algorithms:
  Binary Search, BFS & DFS, Recursion, Sorting, Dynamic Programming. Foundational
  concepts: Big-O, Bit Manipulation, Math essentials.

### 3.2 Dashboard — Prerequisites tab (`dashboard/index.html`)
- Topbar: 4th `.tab-btn` (`tab-btn-prerequisites`); `TABS` array extended (generic
  `switchTab` + hash routing then work unchanged).
- New `tab-panel-prerequisites` markup: stats bar, filter bar (search + group),
  content container.
- State: `PREREQS`, `prereqFilters`; `loadPrerequisites()` added to the init
  `Promise.all`; re-render hooked into `buildCrossLinkIndices` so cascade counts
  populate once problems load.
- Render: `populatePrereqGroups`, `prereqProblemCount` (cascade by topic),
  `applyPrereqFilters`/`matchPrereq`, `updatePrereqStats`, `renderPrereqs` (grouped
  collapsible sections via the existing `toggleSection`, extended with a
  `pre-section` → `data-pre-section-body` mapping), and `buildPrereqCard` (analogy
  callout → explanation → animation mount → key ops → snippets → pitfalls →
  complexity → clickable topic pills). Reuses `escHtml`/`escAttr`/`mdInline`/`goToTopic`.
- CSS: `.pre-level*` level badges, `.pre-analogy` callout, `.pre-topic-pill`, and
  the `.pa-*` animation styles. New rules are additive and namespaced.

### 3.3 Hero animations (`dashboard/prereq-anims.js`, new)
- A generic `buildStepper(host, title, frames)` (Prev/Next over pre-rendered
  frames) plus `mountHashMap` (hashing → collision → O(1) lookup), `mountBinarySearch`
  (halving a sorted range to find 13), and `mountRecursion` (the `fact(3)` call stack
  growing then unwinding). Registered in `PREREQ_ANIMS`; mounted by `buildPrereqCard`.
- Loaded via a `<script src="prereq-anims.js">` tag before the inline script.
  Intentionally **out of the lesson render/verify gate** — these are dashboard
  widgets, not lessons.

### 3.4 Mobile fix (`dashboard/index.html`, `@media (max-width:480px)`)
- The 4th tab widened the shared topbar to 434 px (> 390). Fixed by
  `.topbar { overflow-x: auto }` + `.topbar-spacer { display: none }` at ≤480 px, so
  the tab strip scrolls inside the bar and never widens the page. This was the
  §4.5-anticipated mitigation.

### 3.5 Documentation
- `README.md` — `data/` + `scripts/` + `dashboard/` inventory entries; a new
  "Prerequisites tab (PLAN-021)" subsection; topbar-scroll note in the responsive
  section; "latest plan" pointer → PLAN-021.
- `CLAUDE.md` — "latest implementation plan" → PLAN-021.
- `AGENT_MD/plan/current_state_report.md` — new top entry.
- `AGENT_MD/plan/plans/PLAN-021_*.md` — status → Completed.

## 4. Testing & validation

- **Data gate, test-first:** `scripts/check_prerequisites.py` was created before the
  data and ran red (`prerequisites.json does not exist yet`). After authoring it
  reports `coverage 208/211 (98.6 %)`, 20/21 topics, **exit 0**. It also caught the
  intended failure mode mid-build: until `prereq-anims.js` existed it flagged the
  three referenced animations as unregistered.
- **Headless render (Chromium/CDP over the project's WebSocket pattern):** the
  Prerequisites tab renders **16 cards, 3 section headers, 3 animations mounted**
  (each `.pre-anim` contains a `.pa-stage`); stats read `208 problems reachable`;
  the cascade chip computes `34 problems →` for the first card.
- **Overflow (G7/G8):** measured `documentElement.scrollWidth − clientWidth` on all
  four tabs at 390 px and 360 px, in both `mobile:true` and `mobile:false` emulation.
  A regression test against the **committed HEAD** dashboard isolated the cause:
  baseline = delta 0; the 4th tab pushed it to 44; after the topbar-scroll fix it is
  **delta 0 everywhere** (baseline and mine identical).
- **Visual:** desktop and 390 px screenshots confirm the analogy callout, level
  badges, the hash-map animation stepping through buckets/collision, the clickable
  topic pills, and the phone topbar scrolling to reveal all four tabs.
- **Corpus / lifecycle:** `python3 scripts/audit_lessons.py` → no new drift;
  `python3 scripts/doctor.py` → latest-plan invariant satisfied (only the
  pre-existing `subsets` `lesson_status` item remains, untouched by this work).
- **Syntax:** `node --check dashboard/prereq-anims.js` OK.

## 5. Known issues & follow-ups

- **"String Matching" topic (3 problems) is uncovered** — the one gap below 100 %.
  A future `string-algorithms` prerequisite (KMP prefix function, Rabin–Karp rolling
  hash) would close it; coverage is 98.6 %, above the 90 % gate.
- **No committed automated render gate for the dashboard.** As with PLAN-020
  (REPORT-020 §5), the dashboard's render/overflow was verified manually via headless
  device emulation; the committed gate covers the *data* (`check_prerequisites.py`),
  not the rendered layout. A future plan could add a dashboard render smoke test.
- **Hero-animation count capped at 3.** More prerequisites could gain animations
  later; they are isolated in `prereq-anims.js` and registered by id, so adding one
  is a localised change. They remain gate-exempt by design.
- **Body max-width doc/CSS discrepancy** (carried from REPORT-020 §5) remains
  out of scope.

## 6. Metrics

| Aspect | Value |
|---|---|
| Prerequisite entries | 16 (8 data-structure · 5 algorithm · 3 concept) |
| Topics covered / total | 20 / 21 |
| Problems reachable via cascade | 208 / 211 (98.6 %) |
| Hero animations | 3 (hash map, binary search, recursion) |
| Horizontal overflow @360/390 px (all tabs) | delta = 0 (was 44 mid-build, pre-fix) |
| New files | `data/prerequisites.json`, `data/prerequisites.schema.json`, `scripts/check_prerequisites.py`, `dashboard/prereq-anims.js` |
| Problem records edited | 0 (cascade is topic-derived) |

## 7. Lessons learned

- **The topbar is shared chrome — a new tab is a global layout change.** Adding the
  4th tab widened the topbar and, because the `position:fixed; right:0` action bar
  then stretched to the widened document, the overflow first *appeared* to come from
  the action bar. Diff-testing against committed HEAD on the same harness pinned the
  real cause (the topbar) in one shot. Worth reaching for a baseline diff before
  chasing a "widest element" report.
- **Mobile emulation mode changes which element looks widest.** `mobile:true` vs
  `mobile:false` flagged different culprits for the *same* root overflow. Measuring
  both — and comparing to a known-good baseline — avoided a wrong fix.
- **A topic-derived cascade is the right call.** Zero edits to 211 records, the
  count stays correct as problems are added, and the validator's "topic must be real"
  rule makes the one dangerous failure mode (a silent zero) impossible. The cost is
  coarser granularity, which the many-to-many `topics[]` array absorbs.
- **Reusing the Patterns card chrome paid off.** The tab is a near-clone of the
  Patterns plumbing, so the new code is mostly data + three small render helpers,
  and it inherits the existing responsive behaviour for free.
