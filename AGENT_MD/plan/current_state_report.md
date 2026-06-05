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
