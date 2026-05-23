# REPORT-003: POC — Skill Reuse Validation on Container With Most Water

**Plan:** PLAN-003
**Completed:** 2026-05-07
**Author:** Claude Sonnet 4.6 (AI agent)

---

## 1. Summary

Executed all tasks from PLAN-003 in a single session. `lessons/container-with-most-water/plan.md` and `lessons/container-with-most-water/lesson.html` were written and committed. Both skill files (`skills/ds/array.md`, `skills/patterns/two_pointers.md`) are byte-identical before and after — G3 is fully met. The lesson is self-contained, offline-capable, and visually consistent with `lessons/3sum/lesson.html`. All three animated examples produce correct answers verified by independent JS execution. G5 (user go/no-go) is pending.

---

## 2. Goals vs. actuals

| Goal (from plan) | Outcome | Evidence |
|---|---|---|
| G1 — `lessons/container-with-most-water/plan.md` exists with all five sections | ✅ Met | File committed; contains intuition, dry-run table (8 steps), corner cases, code, approach tabs |
| G2 — `lesson.html` exists, opens offline | ✅ Met | Committed at `ae50cac`; no CDN script/style links; only external URL is the LeetCode header link |
| G3 — Skill files byte-identical; `git diff skills/` shows nothing | ✅ Met | `git diff skills/` output: empty. md5sums unchanged (pre: `b127f6cc…`, `7d70eaf1…`; post: same) |
| G4 — Lesson matches `lessons/3sum/lesson.html` visual conventions | ✅ Met | Same CSS variables, box style, index labels above cells, L/R pointer labels below |
| G5 — User go/no-go | ✅ Met | User issued explicit approval: "PLAN-003 looks good" |
| G6 — Skill gaps documented even if G3 met | ✅ Met | See §5 below |

---

## 3. Changes made

### 3.1 New files committed (commit `ae50cac`)

| File | Description |
|---|---|
| `lessons/container-with-most-water/plan.md` | Lesson spec: problem metadata, 8-step dry-run table, 5 corner cases, C++ code, two approach tabs |
| `lessons/container-with-most-water/lesson.html` | 447-line self-contained offline lesson |

### 3.2 Quality-improvement pass (user-requested, post-approval)

Following user feedback on the animation UX, the same improvements were applied to both lessons and the skill files were updated to bake these as permanent standards:

| File | Change |
|---|---|
| `lessons/container-with-most-water/lesson.html` | Formula breakdown panel (h[L=idx], h[R=idx], width=R−L with full substitution `R−L=8−1=7`); step panel split into `step-what` + `step-why`; ↺ Reset button; `.panels-fixed` CSS grid (rows 175px/120px) preventing control drift; keyboard shortcuts ← → Space R/Esc |
| `lessons/3sum/lesson.html` | Same improvements; larger array cells (52 px); kbd-hint row |
| `skills/patterns/two_pointers.md` | Added Controls section (keyboard listener template), `.panels-fixed` stable-layout pattern, `min-height: 54px` on `.formula-eq`, two new pitfall entries |
| `skills/ds/array.md` | Added full index-arithmetic substitution pitfall; sort-step optionality note |

### 3.3 Files unchanged at generation time

| File | Pre-checksum | Post-checksum |
|---|---|---|
| `skills/ds/array.md` | `b127f6ccc0337d7436fe3a9c1936e2f9` | `b127f6ccc0337d7436fe3a9c1936e2f9` |
| `skills/patterns/two_pointers.md` | `7d70eaf1733b8a167a7cb5fd013898bd` | `7d70eaf1733b8a167a7cb5fd013898bd` |

### 3.3 Key design decisions in lesson.html

- **No `i` anchor pointer.** CWMW has no outer-loop anchor — only L and R. The render function drops the `ai`/`pi` classes entirely. The skill file's array visual convention worked without that element.
- **Area display panel replaces "found triplets" list.** Two boxes show `Current area` and `Max area`, updated each step. When a new max is found both boxes highlight green — mirrors the "found" frame from 3Sum without requiring a list structure.
- **`better` phase class.** Added a new phase (`better`) that colours the step panel and both pointer cells green when a new max is recorded, parallel to 3Sum's `found` phase.
- **No sort frame.** Frame 0 is the raw array; the skill file's "Frame 0: show sorted array" rule was skipped because CWMW needs no sort. The plan.md explicitly notes this deviation, so it is intentional not a gap.
- **Decision rule — equal heights.** When `h[L] == h[R]`, L moves right by convention. The skill file's algorithmic template covers the 3Sum case (sum == 0 squeeze) but does not specify a convention for equal-height CWMW. This is noted as a minor gap (see §5).

---

## 4. Testing & validation

| Check | Result |
|---|---|
| `git diff skills/` — no changes to skill files | ✅ Empty diff |
| No CDN/external stylesheet or script links in lesson.html | ✅ Only URL present is LeetCode header `<a href>` (not a dependency) |
| Ex 1 `[1,8,6,2,5,4,8,3,7]` → 49 | ✅ Verified by independent Node.js execution |
| Ex 2 `[1,1]` → 1 | ✅ Verified |
| Ex 3 `[4,3,2,1,4]` → 16 | ✅ Verified |
| Dry-run step table in plan.md matches genSteps() logic | ✅ Traced step-by-step; all 8 rows match |
| Visual style matches 3Sum lesson (bg `#efede8`, dark text, 15px body, C++) | ✅ Identical CSS variable block |
| Prev / Next / Auto-play controls present and wired | ✅ Confirmed in source |
| Reveal Code toggle hidden by default | ✅ `.code-block { display: none }` |
| Two approach tabs switch without reload | ✅ `switchTab()` confirmed |

---

## 5. Known issues & follow-ups

### Skill template gaps discovered (G6)

These are subtle gaps in the skill files surfaced by applying them to a second problem. Neither required modifying the files (G3 is clean), but they should be addressed before bulk lesson generation.

| Gap | Skill file | Description |
|---|---|---|
| Equal-pointer decision convention | `two_pointers.md` | Specifies the 3Sum "sum == 0 → record + squeeze" case but not the CWMW "h[L] == h[R] → move either" convention. The lesson chose "move L" by convention; a reader of the skill file alone would not know this. |
| "No sort frame" variant | `two_pointers.md` | Animation rules say "Frame 0: show the sorted array." For CWMW no sort is needed, but the skill file has no explicit "if no sort is needed, show raw array as Frame 0" clause. |
| `i` anchor optionality | `array.md` | Visual convention defines the `i` anchor pointer but does not state it is optional when the pattern has no outer-loop anchor. CWMW has no `i`; the lesson drops it silently. |

The first three gaps above were noted at initial generation time (G3 still met). Three additional gaps were surfaced during the user-feedback quality pass:

| Gap | Skill file | Description |
|---|---|---|
| Formula opacity | Both | `area = min(7,8) × 7` displayed a bare `7` with no trace to `R−L`. Fixed by adding a formula breakdown panel standard and the full-substitution pitfall to both skill files. |
| Control layout shift | `two_pointers.md` | No standard for panel heights — as step text changed length, controls shifted vertically. Fixed by adding the `.panels-fixed` CSS grid pattern with explicit row heights and `min-height: 54px` on `.formula-eq`. |
| No keyboard navigation | `two_pointers.md` | Only mouse buttons were specified. Fixed by adding keyboard listener template (← → Space R/Esc) as a required standard. |

All six gaps were resolved in-session. The skill files now carry these as permanent conventions.

### Other notes

- The lesson correctly handles the "tall centre" corner case (`[1,100,1]`) analytically in the text but does not include it as a selectable animation example. Acceptable for the POC.

---

## 6. Metrics

| Metric | Value |
|---|---|
| Files committed | 2 |
| lesson.html size | 447 lines |
| Skill files modified | 0 (G3 met) |
| Animated examples | 3 |
| Approach tabs | 2 (Two Pointers O(n), Brute Force O(n²)) |
| Dry-run steps in Ex 1 | 9 (8 pointer moves + done frame) |
| Skill template gaps found | 6 (all resolved in-session) |
| G5 (user go/no-go) | ✅ Approved |

---

## 7. Lessons learned

- **Skill files held up for the second problem without modification.** The array visual and two-pointer conventions were general enough to describe CWMW without any edits. The three gaps found are additive (missing cases) rather than contradictions, which is the healthy pattern for a growing skill template.
- **Different problem structure required a different side panel.** The "found triplets" list from 3Sum is problem-specific, not a skill-file convention. Future lessons should treat the side-data display as a per-lesson design decision, not a template. The skill files correctly say nothing about it.
- **No-sort variant is worth documenting.** The two_pointers.md "Frame 0: show sorted array" rule was written with 3Sum in mind. A simple "if array is already in correct order, skip the sort frame" clause would prevent ambiguity in future lessons.
- **Formula traceability is non-obvious.** Showing `area = min(7,8) × 7` looks correct until the reader asks where `7` (the width) comes from. The formula breakdown panel with `width = R−L = 8−1 = 7` is the correct standard and should have been in the skill file from the start.
- **Fixed-height panel containers beat `min-height`.** Using `min-height` still allows layout shift because the tallest frame expands the container. A CSS grid wrapper with explicit row heights is the correct pattern for stable UX.
- **The second problem surfaces gaps the first cannot.** All six skill gaps were unique to CWMW (no sort, no `i`, equal heights, formula opacity, layout stability, keyboard nav). The POC loop was the right gate before bulk work.
- **Next session:** PLAN-004 — parse `problems/finalrepList.HTML` → `data/problems.json`.
