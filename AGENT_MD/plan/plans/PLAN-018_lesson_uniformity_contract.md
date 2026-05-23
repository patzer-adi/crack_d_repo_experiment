# PLAN-018: Lesson Uniformity Contract — Repo-Wide Backfill + Lint Tightening

**Created:** 2026-05-21
**Status:** Completed
**Addresses:** As of the start of this plan, the 17 generated lessons fell into three structurally distinct styles — 9 "canonical" (PLAN-015 animated rewrites), 6 "legacy goldens" (rich static §1 with chain-box but no animation), and 2 "stubs" (majority-element pair, ~24-line §1 with static trace table). Markers used three different formats (`═══ SECTION`, plain `SECTION`, `§N`). Several lessons used hard-coded hex colors instead of the centralised `var(--bg-info)` / `--bg-success)` / `--bg-warn)` palette. The user's directive: "Everything structurally should be the same — animation, controls, colours — everything. And future lesson generation should not have it."

---

## 1. Context & motivation

PLAN-015 brought 9 lessons to a new visual-led §1 standard. PLAN-016 + PLAN-017 captured the lint and animation conventions. But the lint had a `LEGACY_GOLDENS` allowlist that downgraded the animation requirement to a WARN for the 4 existing goldens + 4 deferred lessons. The user, on browsing the dashboard, found the resulting non-uniformity (different markers, missing animations, hard-coded colors) unacceptable. This plan closes that gap and tightens the lint so it cannot recur.

## 2. Goals

- All 17 generated lessons pass the strengthened lint with 0 WARN / 0 FAIL.
- The canonical §1 structure (animated 3-row layout · 3-layer legend · prev/auto/next/reset controls at 1400ms · `siGenSteps` step generator) is present in every lesson.
- Section markers are uniform: `<!-- ═══ SECTION N: TITLE ═══ -->` exactly.
- The centralised color palette (`var(--bg-info)` / `--bg-success)` / `--bg-warn)`) is enforced everywhere; hard-coded hexes are flagged.
- The lint's `LEGACY_GOLDENS` allowlist is drained — no more bypass for "old" lessons.
- Design doc (`lessons/LESSON_DESIGN.md`) explicitly mandates marker format and color palette so future generators don't re-introduce drift.

## 3. Scope

In-scope lessons (17 generated):
- **Canonical (9, already pass):** maximum-subarray, product-of-array-except-self, merge-intervals, first-missing-positive, spiral-matrix, find-the-duplicate-number, two-sum, repeated-substring-pattern, valid-palindrome.
- **Legacy goldens (6, animation backfill):** 3sum, container-with-most-water, permutation-in-string, trapping-rain-water, median-of-two-sorted-arrays, count-permutations-with-inversion-requirement.
- **Stubs (2, full §1 rewrite):** majority-element, majority-element-ii.

Out of scope (per user's "16 lessons" framing):
- `move-zeroes` and `two-sum-ii-input-array-is-sorted` — exist as scaffolds in `lessons/` but `lesson_status != "generated"` in `data/problems.json`. The audit was updated (Phase 1) to filter by lesson_status so these no longer appear in the report.

## 4. Approach — five phases

Each phase shipped as its own commit on master.

### Phase 1: marker normalization + design doc + audit filter
- `/tmp/normalize_markers.py` (one-shot) rewrote 70 markers across 7 lessons to the canonical `═══ SECTION N: TITLE ═══` format.
- `LESSON_DESIGN.md` "Always true" block: added explicit marker rule.
- `scripts/audit_lessons.py`: filter by `lesson_status=generated` by default; `--all` opts back in.
- Commit: `a2060ab chore(lessons): normalize section markers + audit by lesson_status`.

### Phase 2: animated §1 backfill into 6 legacy goldens
- Each lesson gained a 3-row visual + 3-layer legend + controls + `siGenSteps` step generator, preserving existing chain-box / kernel-cols reasoning where present.
- Problem-specific examples: two-pointer (cwmw, 3sum, trw), sliding window (perm-in-string), binary-search-on-partition (median-of-two), DP-table fill (count-permutations).
- Commit: `84deea9 feat(lessons): backfill animated §1 into 6 legacy goldens`.

### Phase 2b: plan.md schema for 5 legacy goldens
- `/tmp/patch_legacy_plans.py` (one-shot) added `## Metadata` + Archetype line + `## 1. Clarifying questions` to 5 legacy plan.md files (the 6th, count-permutations, was already updated by PLAN-015).
- Each insertion is annotated "Plan added retroactively (2026-05-21)" so readers know the HTML predates the notes.
- Commit: `5b40eb4 docs(lessons): add PLAN-011 schema to 5 legacy goldens' plan.md`.

### Phase 3: rewrite 2 FAIL stubs to canonical
- `majority-element`: Boyer-Moore vote-cancellation animation on `[2,2,1,1,1,2,2]`.
- `majority-element-ii`: two-slot Boyer-Moore generalisation on `[1,2,3,1,2,3,1,2]` with triple-cancel pivot markers and a verification-pass terminal step.
- Commit: `65803af feat(lessons): rewrite majority-element and majority-element-ii to canonical §1`.

### Phase 4: lint strengthening
- `scripts/lint_lesson.py`:
  - `LEGACY_GOLDENS` drained to the empty set (the bypass is gone).
  - New `schema:section markers canonical` check rejects any marker not matching `<!-- ═══ SECTION N: TITLE ═══ -->`.
  - New `§1:color legend uses canonical palette` check requires each of info / success / warn to appear (as bg-, text-, or border- variant) somewhere in the lesson.
- 3 minor color-vocabulary fixes (find-the-duplicate-number, repeated-substring-pattern, spiral-matrix) replaced hard-coded hexes with canonical vars.
- Commit: `5931fa1 feat(lint): strengthen uniformity contract — drop legacy bypass, add marker+color checks`.

## 5. Non-goals

- Move-zeroes / two-sum-ii: deliberately out of scope. They are scaffolds (lesson_status ≠ generated). Whether to flesh them out to canonical or define a "trivial-problem tier" is a separate decision.
- The §1 animation in find-the-duplicate-number uses 4 pointer states (slow / fast / meet / entry) — more than the 3-tier palette accommodates. Two cells (the "slow" and "meet" indicators) retain custom hex / inline coloring because the algorithm legitimately needs 4 distinct colors. The lint's color check is satisfied by the canonical info / success / warn presence in the legend; the 4th tier (purple "meet") is a documented exception, not drift.
- `static/lesson.css` palette additions (no new color tiers introduced).
- Section 2–12 uniformity (only §1 is contractually animated; later sections vary per problem by design).

## 6. Acceptance criteria (machine-checkable)

- `python3 scripts/audit_lessons.py` reports `17 pass, 0 warn, 0 fail (of 17 lessons)`.
- `python3 scripts/lint_lesson.py <slug>` for every slug in `data/problems.json` with `lesson_status=generated` emits `0 fail`.
- `LEGACY_GOLDENS` in `scripts/lint_lesson.py` is `set()` (empty).
- `lessons/LESSON_DESIGN.md` "Always true" block documents the marker format and the color palette rule.

## 7. Risk / follow-ups

- **find-the-duplicate-number's 4th color:** if the lint is ever extended to forbid non-canonical hex colors, this lesson would need rework. Defer until needed.
- **Scaffolds (move-zeroes, two-sum-ii):** they exist in the lessons tree but aren't visible to the audit. If the user wants to promote them to generated status, they'll have to be brought up to PLAN-017 standard first (else the lint fails). The batch-lesson skill already enforces this.
- **17 lessons is not the final count.** Future lessons generated via `/batch-lesson` automatically inherit the contract because the lint is the hard gate before `lesson_status=generated`. No further structural drift is possible without an explicit allowlist edit.
