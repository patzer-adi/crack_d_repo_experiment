# PLAN-003: POC — Skill Reuse Validation on Container With Most Water

**Created:** 2026-05-07
**Status:** Completed
**Addresses:** Feature 2 in `AGENT_MD/spec.md` — prove that `skills/ds/array.md` and `skills/patterns/two_pointers.md` are reusable templates by generating a coherent lesson for a second problem **without modifying either skill file**.

---

## 1. Context & motivation

PLAN-002 produced the first end-to-end lesson (`lessons/3sum/lesson.html`) and was approved by the user. Per the spec architectural principle:

> *"Skills are reusable templates, not per-problem rewrites. A skill file is validated only when a second problem uses it unchanged."*

Until a second problem consumes the same skill files without requiring edits, the skill files are still drafts. This plan runs that validation on **Container With Most Water (LC #11)** — an Array + Two Pointers problem with a meaningfully different decision rule from 3Sum, making it a genuine test of skill generality.

Key differences from 3Sum that stress-test the skill files:
- **No sort step.** Array is not sorted as a prerequisite; the two-pointer logic works on the original order.
- **Different decision rule.** Instead of comparing a sum to a target, we compute `area = min(h[L], h[R]) * (R - L)` and move the pointer with the *shorter* height inward.
- **Single numeric result** (max area) rather than a set of triplets — the side panel and "found" display will look different.

If the skill files need edits to produce a coherent lesson for this problem, those edits are documented as "skill template gaps" in §5 of REPORT-003 before any bulk work begins (PLAN-004 onward).

---

## 2. Goals

- **G1:** `lessons/container-with-most-water/plan.md` exists and contains: problem metadata, skill file references, the full dry-run walkthrough on `[1,8,6,2,5,4,8,3,7]`, corner cases, and the two-approach tab spec.
- **G2:** `lessons/container-with-most-water/lesson.html` exists, was generated from `plan.md` + the two existing skill files, and opens in the browser with no network dependency.
- **G3:** `skills/ds/array.md` and `skills/patterns/two_pointers.md` are **byte-identical** before and after this plan. Verified by `git diff skills/` showing no changes.
- **G4:** The lesson visually matches the conventions of `lessons/3sum/lesson.html` — same box style, same L/R pointer markers below cells, same index labels above cells.
- **G5:** User performs a go/no-go quality review and explicitly approves before PLAN-004 begins.
- **G6:** Any skill file gaps discovered (content in the skill file that had to be worked around or was missing) are documented in REPORT-003 §5, even if G3 is met.

---

## 3. Non-goals

- No modifications to `skills/ds/array.md` or `skills/patterns/two_pointers.md`. Changes to skill files belong to a future bulk-skills plan after PLAN-003 surfaces the gaps.
- No additional skill files (e.g. a "monotone property" pattern file). The lesson may reference the concept in text but must not depend on a new skill file.
- No Python scripts, no dashboard, no parsing of `problems/finalrepList.HTML`.
- No third problem. Skill reuse is validated by two problems; the third adds no new signal here.

---

## 4. Approach

### 4.1 Problem overview

**Container With Most Water — LC #11**

Given an integer array `height` of length `n`, find two lines at indices `L` and `R` such that the container formed with the x-axis holds the most water:

```
area = min(height[L], height[R]) * (R - L)
```

Return the maximum area. The array is *not* sorted — the two-pointer technique works directly on the given order because of a greedy argument: the shorter of the two lines is the limiting factor, so moving the longer line inward can never increase the area; moving the shorter line inward might.

**Decision rule (differs from 3Sum):**
- If `height[L] < height[R]`: move L right (`L++`).
- If `height[L] > height[R]`: move R left (`R--`).
- If `height[L] == height[R]`: move either (both are correct; convention: move L right).

**Time:** O(n). **Space:** O(1).

### 4.2 Content for `lessons/container-with-most-water/plan.md`

The plan.md that drives lesson generation. Sections:

**Problem metadata:**
- Name: Container With Most Water
- Number: 11
- Link: https://leetcode.com/problems/container-with-most-water/
- Difficulty: Medium
- Topic: Arrays

**Skill files:** `skills/ds/array.md`, `skills/patterns/two_pointers.md`

**Intuition section:**
- Brute force: try every pair (i, j) — O(n²). Too slow.
- Greedy insight: the area is limited by the *shorter* line. Moving the taller line inward can only decrease or maintain the width, and cannot increase the height limit. So moving the taller line is never beneficial — always move the shorter one.
- No sorting needed. The greedy argument works on any array order because we always keep the currently tallest candidate on each side.

**Animated dry run on `[1, 8, 6, 2, 5, 4, 8, 3, 7]`:**

| Step | L (idx, h) | R (idx, h) | Area | max_area | Decision |
|------|-----------|-----------|------|----------|----------|
| 0 | 0, h=1 | 8, h=7 | min(1,7)×8 = 8 | 8 | h[L]<h[R] → move L |
| 1 | 1, h=8 | 8, h=7 | min(8,7)×7 = 49 | 49 | h[L]>h[R] → move R |
| 2 | 1, h=8 | 7, h=3 | min(8,3)×6 = 18 | 49 | h[L]>h[R] → move R |
| 3 | 1, h=8 | 6, h=8 | min(8,8)×5 = 40 | 49 | h[L]==h[R] → move L |
| 4 | 2, h=6 | 6, h=8 | min(6,8)×4 = 24 | 49 | h[L]<h[R] → move L |
| 5 | 3, h=2 | 6, h=8 | min(2,8)×3 = 6 | 49 | h[L]<h[R] → move L |
| 6 | 4, h=5 | 6, h=8 | min(5,8)×2 = 10 | 49 | h[L]<h[R] → move L |
| 7 | 5, h=4 | 6, h=8 | min(4,8)×1 = 4 | 49 | h[L]<h[R] → move L |
| Done | L=6 ≥ R=6 | — | — | **49** | — |

Show `max_area` updating in a side annotation; show the decision label before the pointer moves.

**Corner cases:**
| Case | Input | Expected | Why |
|---|---|---|---|
| Minimum input | `[1, 1]` | `1` | Only one pair possible; L=0, R=1, area=min(1,1)×1=1 |
| All same height | `[5,5,5,5]` | `15` | Best is outermost pair: min(5,5)×3=15 |
| Monotone increasing | `[1,2,3,4,5]` | `6` | L=0,R=4: min(1,5)×4=4; L=1,R=4: min(2,5)×3=6; L=2,R=4: min(3,5)×2=6; ties at 6 |
| Monotone decreasing | `[5,4,3,2,1]` | `6` | Mirror of above |
| One very tall line | `[1,100,1]` | `2` | Tall centre line is irrelevant; best is outer pair min(1,1)×2=2 |

**Code (C++, Reveal toggle, two approach tabs):**

Tab 1 — Two Pointers, O(n):
```cpp
int maxArea(vector<int>& height) {
    int L = 0, R = height.size() - 1, best = 0;
    while (L < R) {
        best = max(best, min(height[L], height[R]) * (R - L));
        if (height[L] < height[R]) L++;
        else                       R--;
    }
    return best;
}
```

Tab 2 — Brute Force, O(n²) (for contrast, not recommended):
```cpp
int maxArea_brute(vector<int>& height) {
    int best = 0, n = height.size();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            best = max(best, min(height[i], height[j]) * (j - i));
    return best;
}
```

**Quality bar:** Match `lessons/3sum/lesson.html` style — same warm grey background (`#efede8`), same dark text, same 15px body font, C++ code, interactive step-through with Prev/Next/Auto controls.

### 4.3 Skill reuse validation method

Before generating the lesson, snapshot the skill files:

```bash
md5sum skills/ds/array.md skills/patterns/two_pointers.md
```

After generation and review, run the same command and diff. If the hashes match, G3 is met. If any edit was needed, document it in REPORT-003 §5 as a skill template gap.

### 4.4 How Claude in VS Code executes this

After `lessons/container-with-most-water/plan.md` is committed, paste into Claude in VS Code:

```
Read these files in full:
1. lessons/container-with-most-water/plan.md
2. skills/ds/array.md
3. skills/patterns/two_pointers.md

Generate lessons/container-with-most-water/lesson.html following the plan exactly.

Requirements:
- Single self-contained HTML file. No CDN links. All CSS and JS inline.
- Must work offline. No internet required after generation.
- Same visual style as lessons/3sum/lesson.html:
  background #efede8, near-black text, 15px body font, C++ code only.
- Animate the dry run from §2 using the array.md and two_pointers.md visual conventions.
- Side panel shows current area and max_area updated each step (no "found triplets" list — single max value instead).
- Two approach tabs: Two Pointers (primary, animated) and Brute Force (code + text, no animation).
- Reveal Code toggle — hidden by default.
```

### 4.5 Verification

```bash
python3 -m http.server 8000
# Open http://localhost:8000/lessons/container-with-most-water/lesson.html
# Disconnect Wi-Fi — reload — must still work
git diff skills/   # must show nothing
```

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Snapshot skill file checksums: `md5sum skills/ds/array.md skills/patterns/two_pointers.md` | 1 min | — |
| 2 | Write `lessons/container-with-most-water/plan.md` using §4.2 content | 15 min | — |
| 3 | Commit `lessons/container-with-most-water/plan.md` | 2 min | 2 |
| 4 | Paste §4.4 prompt into Claude in VS Code; receive `lesson.html` | 10–20 min | 3 |
| 5 | Serve via `python3 -m http.server 8000`; step through animation; verify dry-run table matches §4.2 | 10 min | 4 |
| 6 | Disconnect Wi-Fi; reload — confirm offline | 2 min | 5 |
| 7 | Run `git diff skills/` — confirm zero changes (G3) | 1 min | 4 |
| 8 | Side-by-side visual check against `lessons/3sum/lesson.html` — same box style, L/R markers, index labels (G4) | 5 min | 5 |
| 9 | Document any skill file gaps in notes (even if G3 is met — surface subtle workarounds) | 5 min | 8 |
| 10 | Commit `lesson.html`; write REPORT-003; flip plan to Completed | 15 min | 8 |

Total estimate: ~1 hour.

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Skill files need minor wording changes to work for CWMW | Medium | Medium | Document as gap in REPORT-003 §5; do not block G3 — treat any change as a signal to refine skill templates in PLAN-008 (bulk skills). |
| Generated lesson uses wrong decision rule (moves taller instead of shorter) | Medium | High | Verify against dry-run table in §4.2 step-by-step; reject and regenerate with a more explicit constraint in plan.md if wrong. |
| "Found triplets" display from 3Sum pattern bleeds into CWMW lesson | Low | Low | plan.md §4.4 explicitly says "single max value, not a list of triplets". If it appears, instruct Claude to remove it. |
| Area computation uses `(R - L)` correctly (not `(R - L + 1)`) | Low | High | Check step 0 of dry run: L=0, R=8, area must be 8 (not 9). Catch during task 5. |
| Visual style drifts from 3Sum lesson (wrong bg or font size) | Low | Medium | plan.md §4.2 quality bar names the exact values (`#efede8`, 15px, C++). Verify in task 8. |

---

## 7. Success criteria

- [ ] **G1** — `lessons/container-with-most-water/plan.md` exists with all five sections (intuition, dry run table, corner cases, code, approach tabs).
- [ ] **G2** — `lessons/container-with-most-water/lesson.html` exists and opens offline without errors.
- [ ] **G3** — `git diff skills/` shows no changes to either skill file.
- [ ] **G4** — Lesson renders array boxes with index labels above and L/R pointer labels below, matching the `skills/ds/array.md` visual convention.
- [ ] **G5** — User issues explicit go/no-go. If go: POC milestone complete; proceed to PLAN-004 (HTML→JSON parser).
- [ ] **G6** — REPORT-003 §5 documents any skill gaps found, even if G3 is met.
- [ ] REPORT-003 written; PLAN-003 status set to `Completed`.
- [ ] `spec.md` Feature Index Feature 2 flipped to ✅; Codebase Inventory updated.

---

## 8. References

- `AGENT_MD/spec.md` — Feature 2 task list, Architectural Principles (skill reuse validation)
- `AGENT_MD/plan/rules.md` — §3 plan template, §5 style rules
- `AGENT_MD/plan/reports/REPORT-002_poc_3sum_lesson.md` — confirms skill files are drafted and lesson style is approved
- `skills/ds/array.md` — must remain unchanged
- `skills/patterns/two_pointers.md` — must remain unchanged
- `lessons/3sum/lesson.html` — visual quality bar and style reference
- `problems/finalrepList.HTML` — row #3: `11 — Container With Most Water — Arrays — Medium — ✓ Done`
