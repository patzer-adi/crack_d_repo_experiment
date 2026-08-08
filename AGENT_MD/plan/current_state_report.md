# crack_d — Current State Report

**Date:** 2026-05-07
**Prepared for:** Session re-onboarding / next AI agent context
**Scope:** Full project audit after PLAN-001 (Pre-Work Setup) completion

---

<!-- 
  LIVING DOCUMENT — new updates go at the TOP below this comment block.
  
  Format each update as:
  
  ## Update — YYYY-MM-DD [Phase/Plan Name]
  - Bullet summary of what changed
  - Key files created/modified
-->

## Update — 2026-07-26 [PLAN-026: DP Ladder — Gentle DP On-Ramp — Completed]
- **Goal:** user request — "I'm struggling with DP; give me ~15 *easy* DP problems that gradually get harder, to solve before the medium/hard ones." The 211-set's DP topic has 33 problems but only **2 Easy**, so there was no gradient to climb.
- **DP Ladder** (`data/dp_ladder.json`, 15 entries, 5 ramp *stages*: First recurrences → Scan & compare → Take-or-skip choice → Grid DP the bridge → Counting DP). Difficulty ramps **Easy (7) → Medium (8)** and ends on Perfect Squares (Coin-Change-with-square-coins), the deliberate bridge into the 211's DP set. Each `details` blurb makes the recurrence derivable, per the lesson-design bar. **All 15 disjoint from basics/warmup/problems** — the catalogue is now 4 datasets = 70 + 30 + 15 + 211 = **326 problems, no double-entry**.
- **Placement, confirmed with the user:** a `General | DP Ladder` **view-switch inside the Warm-Up tab** (not a 7th tab — keeps the PLAN-025 6-tab nav), mirroring the Problems `Table | Roadmap` switch. General view is untouched; the ladder is its own dataset, *not* an edit to `warmup.json`.
- **Gate, test-first** (`scripts/check_dp_ladder.py`, new) — clone of `check_warmup.py`: exactly 15, required fields, kebab + unique + disjoint slugs (vs. problems/basics/warmup), unique non-colliding `lc_num`, canonical LC URL matching slug, stage order/contiguity, strictly increasing `order`, shared ⓘ hover-card contract, and the one new invariant — **difficulty non-decreasing across `order`** (the enforceable form of "gradually increasing"). `server.py`: one line — `dpladder` added to `STATUS_DATASETS`.
- **Dashboard** (`dashboard/index.html`) — `INFO_SOURCES`/`toggleSection`/`toggleStatus`-dispatch each gained a `dpladder` case; `DPLADDER` global + `loadDpLadder()` in the init `Promise.all`; the Warm-Up panel wrapped into `#wu-view-general` with a new `#wu-view-dpladder` sibling; `setWarmupView` + `renderDpLadder`/`buildDpLadderRow`/`updateDpLadderStats` reuse the Warm-Up row shape plus a difficulty badge; the pill delegation intercepts `wu-view` like `p-view`.
- **Verification:** `check_dp_ladder.py` exit 0 (15; 7 Easy → 8 Medium; disjoint). Headless Chromium/CDP against the local server: DP Ladder shows 15 rows / 5 stages / 15 badges / 15 ⓘ and correct stat chips; General view still renders its 30; switch flips both ways; toggling a row updates "X of 15 completed" and the PATCH persists to `dp_ladder.json` (also confirmed by direct `curl` PATCH → disk); 0 console errors; 390px overflow delta 0. `check_warmup.py`/`check_basics.py`/`check_roadmap.py`/`check_prerequisites.py` still green; `doctor.py` no new drift.
- **Files:** new `data/dp_ladder.json`, `scripts/check_dp_ladder.py`, `AGENT_MD/plan/plans/PLAN-026_dp_ladder.md`, `AGENT_MD/plan/reports/REPORT-026_dp_ladder.md`; modified `scripts/server.py`, `dashboard/index.html`, `CLAUDE.md`.
- **Still open (unchanged):** catalogue disjointness is enforced one-directionally from the newest dataset (ladder checked against the other three); making the other validators symmetric is a cheap future hardening. Still no cross-dataset "326 problems, N done" roll-up. Pre-existing `subsets` `lesson_status` drift untouched.

## Update — 2026-07-15 [PLAN-025: Nav De-clutter + Roadmap Polish — Completed]
- **Goal:** presentation-only follow-up after the user reviewed PLAN-023/024 live. No data or validator changes.
- **Roadmap sizing** — it rendered at a fixed ~980px canvas left-aligned in the 1400px content column, so on a wide screen it looked small with a big empty band to the right. Now the `<svg>` drops its fixed `width`/`height` for `viewBox` + `preserveAspectRatio` and is sized in CSS (`width:100%; min-width:920px; height:auto`): it scales **up** to fill the column (capped at 1400px by `.content`) and needs no horizontal scroll on large screens, while the `min-width` floor hands off to the container's own scroll on phones rather than shrinking labels into illegibility.
- **Roadmap legend** — the descriptive paragraph above the DAG was removed; the one legend-worthy bit of it (what an arrow means) became a `→ learn first` key, so the row now reads *→ learn first · complete · in progress · not started*.
- **Nav de-clutter** — dropped the `PRACTICE` / `LEARN` group labels and the parenthesised count on every tab (`Basics (70)`, `Problems (211)`, …); the hairline `.tab-group-sep` still separates the two groups. Removed the six `#tab-count-*` spans, the six JS lines that populated them, and the now-dead `.tab-btn span` / `.tab-group-label` CSS.
- **"X of Y completed"** — the counts moved onto each page. For the three Practice tabs the `done` chip now shows `${allDone} of ${allTotal} completed`, counted over the **whole** dataset (`ALL`/`BASICS`/`WARMUP`) — it is the one chip that deliberately ignores the active filter, because completion is a fact about the tab, not the search. The Learn tabs never had completion state; their totals already live in their own stats bars, so the nav count just went.
- **Verification:** 40 headless assertions, all passing — nav has 0 group-label and 0 tab-count elements; each Practice page shows the exact `X of Y completed` read from disk and it stays constant when a filter is applied; the roadmap SVG width equals its container (1352px in the 1400 column) with no scroll at 1024–1920px and its own scroll at 390/360; node click-through intact; 6 tabs × 8 viewports (1920→360) zero overflow; 0 console errors. Screenshotted nav + roadmap and eyeballed both.
- **Files:** modified `dashboard/index.html`; new `AGENT_MD/plan/plans/PLAN-025_nav_declutter_and_roadmap_polish.md`, `AGENT_MD/plan/reports/REPORT-025_nav_declutter_and_roadmap_polish.md`; docs (`README.md`, `CLAUDE.md`).

## Update — 2026-07-14 [PLAN-024: Topic Roadmap + crack_IT Branding — Completed]
- **Goal:** the user supplied a hand-drawn topic dependency diagram (`data/dsa_plan_2.png`) and asked where it could be used, plus `crackIT.png` as the new logo.
- **The diagram was rebuilt as data, not embedded.** Its *structure* was the valuable part; its *numbers* were the NeetCode roadmap's, not this repo's — it claims Arrays & Hashing 20 (we have 13) and Trees 30 (we have 13), splits DP into 1-D/2-D (we have one section of 33), and has **no node for six real topics holding 48 of our problems** (Prefix Sum, BST, Design, Bit Manipulation, Math, String Matching). Embedding it would have put a headline graphic on the page contradicting the table beneath it, and it would go stale on the next problem added.
- **Roadmap view** (`data/roadmap.json`, 20 nodes · 27 edges · 7 layers · single root). The Problems tab now has a **`Table | Roadmap` view switch** — *not* a 7th tab, because both are views of the same 211 problems and six tabs is already the practical limit of a nav row (PLAN-023). Rendered as hand-built SVG (20 nodes with declared layers needs no layout library): each node shows the topic, a `done/total`, and a progress bar, coloured complete / in-progress / not-started, with arrowheads carrying direction (prerequisite → dependent). Every node is a `role="button"`/`tabindex=0` group that opens its topic in the table on click **or** Enter/Space. `goToTopic()` (the Algorithms/Foundations topic pills) now forces the table view — landing on Problems with the roadmap showing would hide the very rows the jump exists to reveal.
- **The load-bearing invariant: `roadmap.json` stores edges and layout ONLY — never a count.** Every `done/total` is derived from `problems.json` at render time. `scripts/check_roadmap.py` (new, red-first) **fails if any node has a `count`/`total`/`n` field**, if any `problems.json` topic lacks a node (it would silently vanish from the map while its problems sat in the table), if an edge dangles, or if the graph has a cycle or back-edge — checked twice, by Kahn's algorithm *and* strict layer monotonicity. That turns "derive, don't transcribe" from a convention into an invariant; the PNG's staleness is structurally impossible here.
- **Two data defects found and fixed.** (1) `minimum-time-to-finish-the-race` (LC 2188) carried `topic: "DP"` / `section: "Ad-hoc"` — a 1-problem topic beside the 32-problem `Dynamic Programming`, and the only member of an `Ad-hoc` section. Folded into Dynamic Programming; `topic` and `section` sets now agree across the dataset for the first time. (2) That immediately broke `check_prerequisites.py`, which caught a dangling `"DP"` alias in the `dynamic-programming` Foundations card — dropped.
- **Branding** — logo pinned to `crackIT.png` (the topbar was running `img/logo_${Math.floor(Math.random()*3)+1}.png`, i.e. **a different logo on every page load**). Derived `crackIT_wordmark.png` for the bar (the full lockup's "Intuition Lab" subline renders ~7px tall at the 30px phone height and reads as smudge) and `favicon.png` from the cracked `c` glyph (the site had no favicon at all). `alt` + `<title>` corrected to `crack_IT — Intuition Lab`.
- **A real bug the viewport sweep caught, and it was the logo's fault.** The topbar overflowed the page between ~901px and ~1050px: the new wordmark is 5.6:1 where the old lockups were ~2.5:1, so at the same height it is ~90px wider, and six tabs + a wider mark exceeded 1000px — while the topbar's `overflow-x: auto` only began at the ≤900px breakpoint. **Same class of bug PLAN-023 fixed for the table wrappers, same fix:** make the rule unconditional. A breakpoint-scoped responsive rule only protects the widths *below* it.
- **Verification:** 45 headless assertions, all passing — including **every node's rendered `done/total` compared against `problems.json` row by row** (summing to exactly 211), colour classes against known cases, click *and* keyboard activation, the map updating live when a problem is marked done (Design 0/12 → 1/12, then reverted), and zero page overflow across **8 viewports** (1440 → 360px) with the DAG scrolling in its own container. PLAN-023's suite re-run unchanged: ALL PASS. Also *rendered it and looked at it*, which caught two things no assertion had: the edges had no arrowheads (the legend promised arrows) and the legend's colour keys wrapped mid-sentence.
- **Files:** new `data/roadmap.json`, `scripts/check_roadmap.py`, `dashboard/img/crackIT_wordmark.png`, `dashboard/img/favicon.png`, `AGENT_MD/plan/plans/PLAN-024_topic_roadmap_and_branding.md`, `AGENT_MD/plan/reports/REPORT-024_topic_roadmap_and_branding.md`; modified `dashboard/index.html`, `data/problems.json`, `data/prerequisites.json`, `README.md`, `CLAUDE.md`.
- **Still open:** `data/dsa_plan_2.png` is now a design reference, not an asset — it belongs in `AGENT_MD/`, not `data/` (which otherwise holds only JSON the app loads). Node `why` text is mouse-only tooltip; the PLAN-023 ⓘ card would surface it on touch. Still no cross-dataset "311 problems, N done" roll-up. Pre-existing `subsets` drift untouched.

## Update — 2026-07-14 [PLAN-023: Tab Architecture + Warm-Up Tab + Richer Problem Detail — Completed]
- **Goal:** three linked user requests — (a) write the Basics problems in a bit more detail, with a small ⓘ that on hover gives fuller guidance and a sample input/output; (b) rearrange and logically rename the tabs now that there are six; (c) add a tab of 30 easy LeetCode problems. Mobile-friendly throughout, per UI/UX best practice.
- **Tab architecture** — the dashboard's five tabs rendered in *the order they were built*, which put Basics (the easiest material) last and Problems (the hardest) first, with no grouping. Now **six tabs in two labelled groups**: **Practice** (Basics 70 → Warm-Up 30 → Problems 211, in the order you walk them) ‖ **Learn** (Foundations · Patterns · Algorithms). The split is *things you solve* (status toggle, difficulty, a ramp) vs *things you read* (reference, no completion state). **Prerequisites → Foundations**; `TAB_ALIASES` redirects `#prerequisites` so existing links still resolve. `TABS` is declared in topbar order and is the single source of truth for routing + rendering.
- **Warm-Up** (`data/warmup.json`, 30 entries, 9 sections: Arrays & Hashing → Strings → Two Pointers & Sliding Window → Binary Search → Stack → Linked Lists → Trees → Math & Bits → Dynamic Programming). Fills the cliff between Basics (ends at nested loops and prime factorisation — no hash maps, no trees, no recursion) and the 211-problem DSA set (73% Medium/Hard, assumes all of it). Each problem carries a `skill` field naming the one transferable idea it teaches (a running accumulator, converging two pointers, the recursive tree template, a first DP recurrence), shown as a pill so the tab reads as a curriculum rather than a list. **All 30 are disjoint from the 211** — the catalogue is now 70 + 30 + 211 = **311 problems, no double-entry**.
- **Richer detail** — all 70 Basics entries gained `details` (2–3 sentences: the trap, the edge case, the reason) and `example` (`{input?, output}`; input omitted for the six problems that take no input). These live behind a compact **ⓘ hover card** — one `.info-card` at `<body>` level, re-anchored per trigger, so the table's `overflow-x` can never clip it. Opens on mouse hover, tap, **and** keyboard focus; closes on Escape / outside click. On phones (≤560px) it docks as a bottom sheet. Row stays a scannable one-liner.
- **Gates, test-first** (`scripts/check_warmup.py`, new) — exactly 30 entries, **all Easy**, slug *and* `lc_num` disjoint from `problems.json`/`basics.json`, `url` slug matching `slug`, section order/contiguity. `check_basics.py` extended with the same `details`/`example` contract (shared `check_hover_card`, imported by both) and its disjointness widened to cover `warmup.json` — which is what caught the one real collision, Basics' `palindrome-number` vs LeetCode 9 (Basics renamed to `numeric-palindrome`; the LC slug is canonical and can't move). Both validators run red on seeded fixtures (11 faults, all caught) before going green. `server.py`: one line — `warmup` added to `STATUS_DATASETS`, since PLAN-022 had already made `PATCH /api/status` dataset-aware.
- **Verification & two real defects found.** Headless CDP check, 45 assertions, all passing: tab structure, 30/70 rows, ⓘ across all three input modes, `#prerequisites` redirect, status toggle round-tripping to disk, 6 tabs × **7 viewports** (1440/1000/820/768/600/390/360) with zero overflow, 0 console errors, Problems still 211 rows. The check caught **(1)** hover gated on `matchMedia('(hover: hover)')` — a device-level query that misclassifies hybrid laptops; rewritten to branch on `event.pointerType`, an event-level fact; and **(2)** a **pre-existing** overflow bug — `overflow-x: auto` on the table wrappers was scoped inside `@media (max-width: 480px)`, so a 768px tablet in portrait scrolled the whole page sideways (Problems 192px, Algorithms 151px). PLAN-020's gate only ever checked 390/360, so nothing had looked between 481 and 900px. Now unconditional.
- **Files:** new `data/warmup.json`, `scripts/check_warmup.py`, `AGENT_MD/plan/plans/PLAN-023_tab_architecture_and_warmup.md`, `AGENT_MD/plan/reports/REPORT-023_tab_architecture_and_warmup.md`; modified `data/basics.json`, `scripts/check_basics.py`, `scripts/server.py`, `dashboard/index.html`, `README.md`, `CLAUDE.md`.
- **Still open (unchanged):** the source PDF is not committed (Appendix A of PLAN-022 is the durable transcription); no cross-dataset progress roll-up ("311 problems, 42 done") — deliberately deferred; the pre-existing `subsets` `lesson_status` drift `doctor.py` reports is unrelated to tab work and was not touched.

## Update — 2026-07-14 [PLAN-022: Basics Tab — Language-Agnostic Programming Drills — Completed]
- **Goal:** a 5th dashboard tab, one rung below Prerequisites, for learn-to-program drills (I/O, arithmetic, conditionals, loops) — sourced from a user-supplied C practice sheet ("C - Program list July-Oct. 2025.pdf", Sections 1–3, not committed to the repo), refined, de-duplicated, difficulty-ramped, re-categorized, and stripped of any one language's syntax so they read as generic exercises. User approved the curated draft and asked for the set expanded to 70 problems.
- **Data** (`data/basics.json`, 70 entries, 7 sections: Output/Input & Variables → Arithmetic & Expressions → Conditionals → Loop Fundamentals → Digits/Divisors/Primes → Interactive Programs & Loop Control → Nested Loops & Patterns). 77 raw PDF items collapsed to 58 via merges (construct variants like if/else vs ternary vs switch folded into one problem with variant notes) and generalization (`sizeof`→"know your types", `scanf`-fails-on-spaces→line vs token input, ASCII table→character codes); one defective item (S3.4.8, "smallest ≤N divisible by 4 and 6" is always 12) restated as *largest* ≤N. 12 user-approved gap-filler problems added (temperature conversion, geometry, simple interest, sort-three, slab pricing, stream min/max/average, doubling series, digit sum, base conversion, strong number, guessing game, Floyd's triangle) for a shipped total of 70. Full per-item disposition (kept/merged/generalized/added/dropped) is Appendix A of PLAN-022. Difficulty mix: 32 Easy · 36 Medium · 2 Hard, non-decreasing within each section.
- **Gate, test-first** (`scripts/check_basics.py`) — written before the dataset (ran red on a broken fixture first). Validates required fields, kebab-case + unique slugs, **slug disjointness from `data/problems.json`** (real collisions exist: `reverse-integer`, `power-of-two`), strictly increasing `order`, declared-section membership + contiguity, non-decreasing difficulty rank per section, and `source` ref format (PDF ref or literal `"new"`). Exit 0.
- **Server** (`scripts/server.py`) — `PATCH /api/status` gained an optional `dataset` field (`"problems"` default | `"basics"`) mapping to the right JSON path under the existing lock; `lesson_status` writes are rejected for the basics dataset (no such field). Verified via direct `curl` PATCHes to both datasets plus 400/404 error paths before any UI wiring.
- **Dashboard** (`dashboard/index.html`) — 5th tab, minus-columns copy of the Problems-tab plumbing: `TABS` extended, `tab-panel-basics` markup (stats bar, search + section/difficulty/status filters), `loadBasics()` in the init `Promise.all`, `renderBasicsTable`/`buildBasicsRow`/`matchBasic`/`updateBasicsStats`, `toggleStatus` generalized to take a `dataset` argument, `toggleSection`'s attr map and the global pill-click dispatcher both extended for `bas-section`/`#tab-panel-basics`. No Lesson/URL/LC-number/cross-link columns (basics problems have no LeetCode page); the name cell shows the statement as a muted sub-line instead.
- **Verification:** `check_basics.py` exit 0. Headless (Chromium/CDP, ad-hoc script mirroring `render_check.mjs`'s launch pattern): 70 rows / 7 section headers rendered, tab count badge, stats bar, search + section filter all correct, status-toggle round-trips through the live server and back, zero horizontal overflow at 1000px/390px/360px, zero console errors, and Problems (211 rows) / Algorithms / Patterns / Prerequisites all still render with hash routing intact. `doctor.py` clean after bumping the README/CLAUDE.md latest-plan pointers (one pre-existing, unrelated drift noted: the `subsets` lesson's `lesson_status` field, from an earlier session, left as-is — out of scope). Docs: README (Basics tab subsection + `data/`/`scripts/` inventory lines), CLAUDE.md (latest plan → PLAN-022). REPORT-022 written; PLAN-022 → Completed.

## Update — 2026-06-05 [PLAN-021: Prerequisites Tab — Foundational Knowledge Layer — Completed]
- **Goal:** a place that names and explains the foundational knowledge (data structures / core algorithms / base concepts) a learner should hold *before* attempting the 211 problems, with a cascade showing which problems each prerequisite unlocks. Product decisions (confirmed with the user): a **new** Prerequisites tab (not folded into Patterns), the cascade **derived from each problem's `topic`** (no per-problem edits), and lean cards **plus a few hero animations** ("nothing fancy").
- **Data** (`data/prerequisites.json`, 16 entries) — 8 data-structure, 5 algorithm, 3 concept. Each card: tagline, plain-language **analogy**, lucid explanation, short code snippet(s), pitfalls, complexity, and a topic-derived **"→ N problems"** chip + clickable topic pills. The three authored `skills/ds/*.md` explainers (array, linked-list, binary-tree) were migrated in (they were previously unsurfaced in any UI). Coverage: **20/21 topics, 208/211 problems (98.6 %)** — only `String Matching` (3 problems) is uncovered (logged follow-up).
- **Gate, test-first** (`scripts/check_prerequisites.py` + `data/prerequisites.schema.json`) — written before the data (ran red); validates ids/fields/enums/snippets, that **every `topics[]` value is a real `problems.json` topic** (cascade can never silently resolve to zero), that referenced animations are registered, and coverage ≥ 90 %. Exit 0.
- **Dashboard** (`dashboard/index.html`) — 4th tab cloned from the Patterns plumbing: `TABS` extended, `tab-panel-prerequisites` markup, `loadPrerequisites()` in the init `Promise.all`, `renderPrereqs`/`buildPrereqCard`/`prereqProblemCount` (cascade by topic, reusing `goToTopic`/`toggleSection`/`mdInline`), and additive `.pre-*`/`.pa-*` CSS. Three **hero inline step-animations** (Hash Map, Binary Search, Recursion call-stack) live in new `dashboard/prereq-anims.js` (gate-exempt — dashboard widgets, not lessons).
- **Mobile:** the 4th tab widened the shared topbar past 390px; fixed by `.topbar{overflow-x:auto}` + hiding the spacer at ≤480px so the tab strip scrolls inside the bar. Headless overflow is **delta=0 at 360px & 390px on all four tabs**, in both mobile/desktop emulation; a diff-test against committed HEAD confirmed no regression (baseline 0 → mine 0).
- **Verification:** `check_prerequisites.py` exit 0; headless render = 16 cards / 3 sections / 3 animations mounted / 0 JS errors; `audit_lessons.py` no new drift; `doctor.py` latest-plan invariant satisfied. Docs: README (tab subsection + inventories), CLAUDE.md (latest plan → PLAN-021). REPORT-021 written; PLAN-021 → Completed.

## Update — 2026-06-04 [PLAN-020: Mobile-Friendly Responsive Layout — Completed]
- **Goal:** make lessons + dashboard usable on a phone, CSS-only, no framework / no JS-behaviour / no table redesign. No horizontal page scroll down to 360px on both surfaces.
- **Lessons** (`static/lesson.css`): new `@media (max-width:480px)` phone block — trims body padding, scales the largest type down, reflows `.formula-grid` to 2 cols, wraps long inline `code`/words, hides keyboard-only `.kbd-hint`, and relaxes `.panels-fixed` from fixed 175px/110px rows to `auto` so the dry-run formula/step panels grow instead of clipping (the no-jump guarantee is a desktop-only concern). The existing `@media (max-width:680px)` block is unchanged.
- **Two per-lesson visuals** needed real fixes (the rest were handled by the global CSS): `container-with-most-water` `#si-strip` bar chart got `overflow-x:auto`; `merge-intervals` `siRender` stopped hardcoding `containerWidth=380` and now sizes from the track's parent `clientWidth` capped at 380 (desktop byte-identical).
- **Dashboard** (`dashboard/index.html`): the lone `@media(max-width:700px)` became two tiers (700px tablet + 480px phone). Phone tier shrinks the topbar and **hides the tab count badges** so logo+3 tabs fit one row, hides low-value columns (`col-check`/`col-xlinks` on Problems, `col-kind` on Algorithms), and gives each table wrapper (`[data-section-body]`/`[data-algo-section-body]`) `overflow-x:auto` so the wide tables scroll inside their box — every column stays reachable, the page never scrolls sideways.
- **Gate extended:** `scripts/render_check.mjs` now asserts no horizontal overflow at **390px** as well as 1000px; it re-drives the animations at phone width so width-reactive renders are measured as a phone visitor sees them. New reason string `mobile horizontal overflow @390px`.
- **Verification:** `render_check --all` 30/30 (was 25/30 at mobile before fixes); `audit_lessons.py` → `render: 30 pass · 0 NEW fail`, `=> OK (no new drift)`; dashboard headless check delta=0 at 360px & 390px across all three tabs. Docs updated: `lessons/design/layout.md` §Mobile, `static/CLASSES.md`, `README.md`.
- REPORT-020 written; PLAN-020 → Completed.

## Update — 2026-06-03 [PLAN-019: Anti-Drift — Visual Gate, Corpus Re-Verification, Doc Reconciliation — Completed]
- **New machinery.** `scripts/render_check.mjs` (headless Chromium over the DevTools Protocol via Node's built-in WebSocket — no npm dep): loads each lesson, drives every animation, asserts no JS error, every §6 step lights an active code line, and no horizontal page overflow. `scripts/doctor.py`: plan↔report bijection (Completed plans only), no phantom plan references, lesson-disk ↔ `lesson_status` reconciliation, README/CLAUDE "latest plan" freshness, baseline sanity.
- **lint_lesson.py** gained a §6 "code-line refs resolve" check (every `cvGenSteps` `line:` must exist in `CV_LINES`) — catches the phantom-line class statically (the bug that left pacific-atlantic's code panel inert).
- **verify_animation.mjs** now also runs `lessons/<slug>/verify.py` if present (independent brute force; inputs in / answers out as JSON) and cross-checks against the declared `EX` answers — closes the tautology hole (PLAN-019 G4). Exemplars added for rotting-oranges and pacific-atlantic-water-flow; 26 lessons' backfill is tracked.
- **audit_lessons.py** rewired from a §1-only survey to a full-lint + render **regression gate**, baseline-aware via `scripts/audit_baseline.json`.
- **Finding:** running the full lint + render corpus-wide (the old audit only checked §1) revealed **15 lessons with pre-existing §2/§6/§7 lint drift** and **8 with real runtime/visual bugs** (e.g. 3sum's §1 animation throws when stepping past a pivot; valid-palindrome's §7 sets textContent on a null element). These are grandfathered in `audit_baseline.json` and slated for a follow-up remediation batch (the list only shrinks; new regressions hard-fail).
- **Doc reconciliation:** retired the phantom "(PLAN-019)" reference (this plan now exists); renamed the misnumbered `REPORT-016_audit_baseline.md` → `baseline_audit_2026-05-19.md` (resolves the duplicate-REPORT-016); updated README + CLAUDE "latest plan" → PLAN-019 and corrected the "26 lessons" / "pauses for review" / "PLAN-012" claims; banner-marked `AGENT_MD/spec.md` as historical; marked the RETROFIT step-c done. `python3 scripts/doctor.py` now exits 0.

> **Note on this report's lower body:** everything below the update log (Executive summary, §1–§8) is the original 2026-05-07 greenfield snapshot and is **stale** — it predates PLAN-004 onward. The update log above is the live record; for a code-derived view run `scripts/audit_lessons.py` and `scripts/doctor.py`.

## Update — 2026-05-16 [PLAN-013: Canonical CS Algorithms Reference — Completed]
- `data/algorithms.json` created: 121-entry canonical algorithms inventory across 14 categories (ML excluded by user decision), built from `scripts/seeds/algorithms_seed.yaml` (1731 lines). Covers Foundational, Graph, DP, String, Computational Geometry, Numerical/Optimization, Data Structures, Advanced Graph, Cryptography, Parallel/Distributed, Miscellaneous, Domain-Specific, Advanced Theoretical, Emerging Areas.
- Dashboard upgraded to tabbed view: `#problems` tab (all existing LC functionality intact) + `#algorithms` tab (filter bar: search / category / kind / relevance; stats bar; table grouped by category). Hash routing via `hashchange` event; back-button works. Default view: high + medium interview relevance (low hidden until toggled).
- Cross-linking: algorithm entries carry `related_lc` slug lists → blue chips under algorithm names. LC problem rows show purple chips for related algorithms. Both resolved at dashboard load from the `slugToAlgos` index — no changes to `problems.json`.
- `scripts/build_algorithms_list.py` builds `data/algorithms.json` from seed; preserves `lesson_status`/`lesson_path` on re-run. `scripts/render_algorithms_sheet.py` generates `algorithms/algorithms_reference.md` (121-entry markdown reference). `scripts/new_algorithm.py` scaffolds `algorithms/<id>/plan.md` from seed metadata.
- `algorithms/design/LESSON_DESIGN.md` placeholder written (Python + C++ two-language design, full spec deferred to PLAN-014). `data/algorithms.schema.json` authored (JSON Schema draft-07).
- 16 `related_lc` slugs reference LC problems outside the 210-problem list — build script warns; dashboard skips silently (aspirational cross-links).
- Smoke-tested: dashboard 200, algorithms.json 121 entries, problems.json 210 entries.
- REPORT-013 written; all G1–G8 success criteria met.

## Update — 2026-05-16 [PLAN-012: Comprehensive Interview-Coverage Problem List — Completed]
- `data/problems.json` rewritten from 153 → 210 entries via `scripts/build_comprehensive_list.py`. All prior `status` (40 done) and `lesson_status` (10 generated) preserved with zero drops, verified by slug-key diff. One input duplicate collapsed (LC 752 "Open the Lock" appeared twice — both with `status=new`, lossless dedup).
- 20 canonical sections (down from 35+ fragmented like "Sliding Window — 5"/"— 4"/"— 1"). Two new schema fields per entry: `tier: 1|2|3` (foundational/core/advanced) and `ramp_pos: int` (within-section position). `order` recomputed as `section_order × 1000 + ramp_pos` so dashboard's natural sort renders the difficulty ramp automatically with no UI change.
- Patterns newly covered (previously absent or thin across both source lists): Union-Find as a named track (323/547/684/261/1319/721/947), Bitmask DP (698/526/847), Segment Tree/BIT (307/315), sweep-line (252/253/759/218), KMP/string matching (28/459/686), reservoir + weighted random (380/382/528), Tree DP (337/124), Game-theory DP (486/877), multi-source BFS (994/542/286/1162), Math (50/69/7/8/204), seven Google "signature" problems distributed to natural sections (489/715/1146/681/359/904/388).
- `scripts/seeds/comprehensive_seed.yaml` is the single source of truth — 499 lines, per-section ordered ramps with `tier`, `ramp_pos`, `twist` (the one new concept this problem introduces vs its predecessor), and `tracks` annotations.
- `scripts/render_problem_sheet.py` regenerates `problems/google_focused_reduced_dsa_sheet.md` (88 problems carrying `tracks: ["google_focused"]`) and `problems/comprehensive_dsa_sheet.md` (full 210). Banner directs editors to the JSON source so the two cannot drift.
- `scripts/server.py /api/add` patched to default the new schema fields (`tier=2, ramp_pos=999, twist="", tracks=[]`) so ad-hoc dashboard additions remain compatible.
- Smoke-tested: dashboard returns 200, JSON serves 210 entries, all `status=done`/`lesson_status=generated` preserved.
- REPORT-012 written; PLAN-012 §7 all success criteria met.

## Update — 2026-05-14 [PLAN-011 Phase 1: Lesson-Generation Efficiency — In-Progress]
- `lessons/design/` directory created with 13 section files (`sec0_clarifying.md` … `sec12_take_home.md`) + 5 cross-cutting files (`layout.md`, `code_style.md`, `python_verify.md`, `known_bugs.md`, `archetypes.md`) — verbatim partition of the 28 principles in `LESSON_DESIGN_v2.md`. Each section file ends with a **Reference excerpts** table mapping the four archetypes (two-pointer, sliding-window, prefix-scan, divide-conquer) to specific line ranges in their canonical goldens.
- `lessons/LESSON_DESIGN.md` rewritten as the lean load-on-demand **index** (~720 tokens) with an explicit "do not preload" directive and a section→files table.
- `lessons/_template.html` (~7 KB) created as the section skeleton — every `class=` already in place, `<!-- PER-PROBLEM: ... -->` markers indicate what the generator fills.
- `static/CLASSES.md` (~110 lines) created as a flat class-vocabulary index, replacing the need to feed `static/lesson.css` into generation prompts.
- `lessons/design/spec_schema.json` (JSON Schema draft-07) defines the lesson spec format for Phase 2 (renderer).
- `scripts/new_lesson.py` scaffolds `lessons/<slug>/{lesson.html, plan.md}` from `data/problems.json` metadata. Smoke-tested on `two-sum` happy path + 4 error paths.
- `CLAUDE.md` updated to point at the new index + workflow.
- **Deferred to Phase 2 (PLAN-012):** `lessons/design/partials/*.html.tmpl`, `lessons/design/partials/js/<archetype>.js.tmpl`, `scripts/render_lesson.py`, `scripts/verify_algorithm.py`, spec extraction from existing four goldens, end-to-end token-budget verification.
- REPORT-011 written documenting Phase 1 scope, deferred Phase 2 substrate, and follow-up plan.

## Update — 2026-05-13 [PLAN-010: Shared Static Assets — Completed]
- `static/lesson.css` created (193 lines): all shared styles extracted verbatim from 3sum + `.legend*` and `.arr-strip/.as-*` additions
- `static/lesson.js` created (20 lines): `toggleEl`, `switchTab` (null-safe), `cvBuildCode(lines)`, play/stop/toggle for cv/dr/bf (900/1100/300ms defaults), `visPx`, `keydown` router
- All four golden lessons refactored to import shared assets; problem-specific CSS kept inline; per-lesson play-speed overrides applied (3sum 250ms, PiS 800ms+950ms cv, rain 280ms)
- `cvBuildCodePanel` in permutation-in-string renamed to `cvBuildCode(CV_LINES)` to match shared interface
- `lessons/LESSON_DESIGN_v2.md` updated with `## Shared assets` section; `README.md` updated with `static/` in project layout
- REPORT-010 written; all 5 goals met

## Update — 2026-05-07 [PLAN-009: Lesson Viewer + Ad-Hoc Add-By-Link — Completed]
- `POST /api/add` endpoint added to `scripts/server.py`: validates slug (`[a-z0-9-]+`), difficulty, positive-int LC number, duplicate detection (409); appends new problem with `lc_num`/`section:"Ad-hoc"`/`lesson_status:"none"` fields
- `dashboard/index.html`: "＋ Add problem" button in filter bar; form modal with URL → auto-fill slug+name, LC number, difficulty, topic fields; inline error on duplicate/validation failure; success pushes row to live table via `ALL.push` + `applyFilters()`
- "Open ↗" button for generated lessons confirmed working (no code change needed)
- REPORT-009 written; all 8 goals met

## Update — 2026-05-07 [PLAN-008: Bulk Skills Authoring — Completed]
- 6 skill files authored: `skills/ds/linked_list.md`, `skills/ds/binary_tree.md`, `skills/patterns/sliding_window.md`, `skills/patterns/binary_search.md`, `skills/patterns/bfs_dfs.md`, `skills/patterns/dynamic_programming.md`
- All 8 skill files now exist; all 25 topics in `data/problems.json` fully mapped with no "not yet authored" gaps
- `dashboard/index.html` `EXISTING_SKILL_FILES` updated to list all 8 files
- 10 C++ algorithmic templates, 40 common pitfalls documented across 4 pattern files
- REPORT-008 written

## Update — 2026-05-07 [PLAN-007: Plan Generation + Copy-Paste Prompt — Completed]
- `dashboard/index.html`: checkbox column per row + per-section select-all checkbox
- Sticky action bar appears when ≥1 problem checked; "Generate Plan" button
- `generatePlans()`: POSTs `lessons/<slug>/plan.md` via `POST /api/write` for each selected problem
- `buildPlanMd()`: generates plan template with problem metadata, DS+patterns inferred from `TOPIC_SKILL_MAP` (25 topics mapped), skill-file list, 5 lesson-section outlines, quality bar
- `buildPrompt()`: ready-to-paste Claude prompt listing only existing skill files; missing ones noted as PLAN-008
- Modal shows per-problem write status + copy-able prompt; REPORT-007 written

## Update — 2026-05-07 [PLAN-006: Python File-Writer Service — Completed]
- `scripts/server.py` written: 115 lines, stdlib only; subclasses `SimpleHTTPRequestHandler` with `directory=PROJECT_ROOT`
- `PATCH /api/status` — reads `data/problems.json`, updates slug's status, writes back atomically under lock
- `POST /api/write` — writes `lessons/*/plan.md` with 3-layer path validation: `..` check, resolve+prefix, pattern match
- `dashboard/index.html` updated: static status badges replaced with toggle buttons; `toggleStatus()` + toast; error message updated
- All G1–G7 goals met; 8 test cases validated; REPORT-006 written

## Update — 2026-05-07 [PLAN-005: Dashboard Skeleton — Completed]
- `dashboard/index.html` written: 421 lines, zero deps, works via `python3 -m http.server 8000`
- Filter bar: search by name/LC#, topic dropdown (25 topics), difficulty/status/lesson pills
- Stats bar: total, done/new, Easy/Medium/Hard, generated — all update live on filter change
- Problems grouped by section (36 sections), headers collapsible
- "Open ↗" button for problems with lesson_status=generated (currently 3sum + CWMW)
- Visual style matches lessons; REPORT-005 written

## Update — 2026-05-07 [PLAN-004: Parse Problems HTML → JSON — Completed]
- `scripts/import_problems.py` written and committed (112 lines, stdlib only)
- `data/problems.json` generated: 150 problems, 37 done / 113 new, 2 generated
- Key discovery: problem list split across 3 `<table>` elements (one per tier); fixed by detecting problem tables by absent `class` attribute vs `class="dtable"` schedule tables
- All G1–G8 goals met; idempotency verified; REPORT-004 written

## Update — 2026-05-07 [PLAN-003: Skill Reuse Validation (CWMW) — Completed, user approved]
- `lessons/container-with-most-water/plan.md` written: 8-step dry-run table, 5 corner cases, C++ code
- `lessons/container-with-most-water/lesson.html` generated: self-contained offline lesson, area/max-area display, two approach tabs
- Both skill files confirmed unchanged: `git diff skills/` empty; md5sums identical (G3 met)
- All 3 animated examples verified correct by independent execution (49, 1, 16)
- 6 skill template gaps found and all resolved in-session (formula opacity, layout stability, keyboard nav + 3 original)
- Quality-improvement pass applied to both lessons: formula panel, step-what/step-why, ↺ Reset, `.panels-fixed` layout, keyboard shortcuts
- G5 (user go/no-go) confirmed: "PLAN-003 looks good"
- REPORT-003 updated to reflect final state

## Update — 2026-05-07 [PLAN-002: POC 3Sum Lesson — Completed, pending user go/no-go]
- `skills/ds/array.md` written: box convention, index labels above, pointer labels below, 4 animation rules, 4 pitfalls
- `skills/patterns/two_pointers.md` written: L/R marker colours, decision labels, Python template, duplicate-skip framing
- `lessons/3sum/plan.md` written: problem metadata, 5-section lesson outline, dry-run walkthrough, corner cases table
- `lessons/3sum/lesson.html` generated: 683-line self-contained offline lesson, 3 interactive examples, two approach tabs (Sort+Two Pointers / HashSet), Reveal Code toggle
- All four files committed at `be3dd3f`
- REPORT-002 written; PLAN-002 status flipped to Completed
- G7 (user go/no-go quality review) pending

## Update — 2026-05-07 [PLAN-001: Pre-Work Setup — Completed]
- Git repository initialised on `master` branch; one clean commit (`e722f5d`)
- `.gitignore` created: ignores `__pycache__/`, `*.pyc`, `*.pyo`, `.DS_Store`
- Six skeleton directories created with `.gitkeep` placeholders: `dashboard/`, `scripts/`, `data/`, `skills/ds/`, `skills/patterns/`, `lessons/`
- Python 3.13.11 confirmed on path
- `PLAN-001_setup.md` → Completed; `REPORT-001_setup.md` written
- `spec.md` bumped to v1.1 (Python instead of Node, POC-first ordering, `problems/finalrepList.HTML` as import source)

---

## 1. Executive summary

`crack_d` is a greenfield personal DSA intuition tool. As of 2026-05-07, the project has a clean git skeleton and a fully articulated spec (v1.1) but **no working code, no lessons, and no skill files yet**. The sole existing asset beyond scaffolding is `problems/finalrepList.HTML` — a curated 150-problem Google L5 prep list with topic, difficulty, and per-problem done/new status. The immediate next step is PLAN-002 (POC): hand-author two skill files and a `plan.md` for 3Sum, then prompt Claude in VS Code to generate the first `lesson.html`. No infrastructure work should begin before this POC loop is validated.

Risk level: **Low** — no deployed system, no credentials, no dependencies. The only risk is that the POC lesson does not meet the quality bar; the spec explicitly gates all tooling work on this validation.

---

## 2. Source code inventory

### Project structure

| Path | Contents | Status |
|---|---|---|
| `AGENT_MD/spec.md` | Living spec v1.1 — 8 features fully defined | ✅ Active |
| `AGENT_MD/plan/plans/PLAN-001_setup.md` | Pre-work plan | ✅ Completed |
| `AGENT_MD/plan/reports/REPORT-001_setup.md` | Pre-work report | ✅ Written |
| `AGENT_MD/plan/rules.md` | Plan/report authoring conventions | ✅ Active |
| `problems/finalrepList.HTML` | 150-problem curated Google prep list | ✅ Source of truth |
| `dashboard/` | Empty (`.gitkeep`) | ⬜ Not started |
| `scripts/` | Empty (`.gitkeep`) | ⬜ Not started |
| `data/` | Empty (`.gitkeep`) | ⬜ Not started |
| `skills/ds/` | Empty (`.gitkeep`) | ⬜ Not started |
| `skills/patterns/` | Empty (`.gitkeep`) | ⬜ Not started |
| `lessons/` | Empty (`.gitkeep`) | ⬜ Not started |

### Key data in `problems/finalrepList.HTML`

The HTML file contains a 150-problem table with the following per-row fields:
- Order # (1–150)
- LC number (e.g. `15` for 3Sum)
- Problem name + LeetCode URL
- Topic / pattern tag (e.g. `Arrays`, `Sliding Window`, `Binary Search`)
- Difficulty badge (`Easy` / `Medium` / `Hard`)
- Status badge (`✓ Done` on `done-row` class rows, `New` otherwise)

This file is the import source for `scripts/import_problems.py` → `data/problems.json` (Feature 3 / PLAN-004).

---

## 3. Configuration audit

| Setting | Value | Notes |
|---|---|---|
| Python version | 3.13.11 | Exceeds 3.10+ requirement |
| Git branch | `master` | Single branch; no remotes |
| File-writer port (planned) | `localhost:5173` | `scripts/server.py` — not yet written |
| HTTP server port (planned) | `localhost:8000` | `python3 -m http.server 8000` from project root |
| Environment variables | None | No `.env` needed — local tool with no secrets |

---

## 4. Test suite status

| Suite | Passed | Failed | Notes |
|---|---:|---:|---|
| PLAN-001 verification commands | 5 | 0 | All goals confirmed by shell output |
| Unit tests | — | — | None exist yet; will add when `scripts/server.py` and `scripts/import_problems.py` are written |

---

## 5. Infrastructure & deployment

| Component | Status | Notes |
|---|---|---|
| Git repository | ✅ Initialised | Local only; no remote configured |
| CI/CD | ⬜ None | Personal local tool — not planned for v1 |
| Deployment | ⬜ None | Runs via `python3 -m http.server` locally |
| Python file-writer | ✅ Complete | `scripts/server.py` — serves static files + PATCH /api/status + POST /api/write |
| Dashboard | ⬜ Not started | `dashboard/index.html` — Feature 4 / PLAN-005 |

---

## 6. Feature progress

| Feature | Plan | Status |
|---|---|---|
| 0 — Pre-Work: Setup | PLAN-001 | ✅ Complete |
| 1 — POC: 3Sum lesson | PLAN-002 | ✅ Complete — user approved |
| 2 — POC: skill reuse (CWMW) | PLAN-003 | ✅ Complete — user approved |
| 3 — Parse HTML → JSON | PLAN-004 | ✅ Complete |
| 4 — Dashboard skeleton | PLAN-005 | ✅ Complete |
| 5 — Python file-writer | PLAN-006 | ✅ Complete |
| 6 — Plan generation + prompt | PLAN-007 | ✅ Complete |
| 7 — Bulk skills authoring | PLAN-008 | ✅ Complete |
| 8 — Lesson viewer + status + add-by-link | PLAN-009 | ✅ Complete |

---

## 7. Known issues & technical debt

- None. Fresh project. No issues discovered during PLAN-001.

---

## 8. Next actions (for the next agent session)

All v1 features (PLAN-001 through PLAN-009) are complete. The tool is usable end-to-end:
- Start server: `python3 scripts/server.py`
- Open: `http://localhost:8000/dashboard/`
- Select problems → Generate Plan → paste prompt into VS Code Claude extension
- Generated `lesson.html` files viewable via "Open ↗" button

Potential next work (Feature 9 from spec, or new features as needed):
- **Multi-approach handling refinement** (Feature 9 / P1): document multi-tab lesson patterns in skill files
- **Generate more lessons** using the existing plan-generation workflow
- **Backtracking pattern skill file**: 4 problems in the list use this topic; no skill file yet
