# PLAN-015: Lesson Drift Remediation

**Created:** 2026-05-19
**Status:** Completed
**Addresses:** Lessons generated after the four goldens drift from the golden bar — primarily in §1 ("The Insight"), where line counts run ½ to ⅓ of the golden depth and the equivalence-chain markup is often missing. This plan rewrites the affected lessons against the [PLAN-016](PLAN-016_self_healing_pipeline.md) lint gate.

> **Revision note:** An earlier Draft of this plan diagnosed the issue as a *schema* mismatch between plan.md (PLAN-011 format) and lesson.html (legacy panels-fixed). That was incomplete. The real drift is *content quality* in §1 — most affected lessons technically follow the PLAN-011 schema but produce shallow Insight sections that describe the algorithm instead of building the foundational concept. Scope rewritten accordingly.

---

## 1. Context & motivation

### 1.1 The drift, as measured

Surveying §1 line counts across all currently-generated lessons (one row per `<div class="section">` for §1):

| Lesson | §1 lines | chain-box | Verdict |
|---|---|---|---|
| 3sum (golden) | 90 | ✓ | bar |
| permutation-in-string (golden) | 91 | ✓ | bar |
| trapping-rain-water (golden) | 49 | (visual-led) | bar |
| median-of-two-sorted-arrays (golden) | 113 | ✓ | bar |
| valid-palindrome | 85 | ✓ but shallow | borderline; rewrite §1 chain content |
| find-the-duplicate-number | 45 | ✗ | drift — rewrite §1 |
| spiral-matrix | 41 | ✗ | drift — rewrite §1 |
| first-missing-positive | 32 | ✗ | drift — rewrite §1 |
| count-permutations-with-inversion-requirement | 57 | ✗ | drift + missing plan.md — rewrite |
| maximum-subarray | 25 | ✗ | severe drift — rewrite §1 |
| merge-intervals | 25 | ✗ | severe drift — rewrite §1 |
| product-of-array-except-self | 25 | ✗ | severe drift — rewrite §1 |
| move-zeroes | 17 | ✓ | tiny but easy problem — review, possibly skip |
| two-sum-ii-input-array-is-sorted | 17 | ✓ | tiny but easy problem — review, possibly skip |
| two-sum | 95 | ✓ | bar |
| container-with-most-water | 89 | ✓ | bar |
| repeated-substring-pattern | 86 | ✓ | bar |

**Definitive scope:** 7 lessons need §1 rewritten (find-the-duplicate-number, spiral-matrix, first-missing-positive, count-permutations, maximum-subarray, merge-intervals, product-of-array-except-self). 1 lesson needs §1 chain-box content deepened (valid-palindrome). 2 lessons need review against archetype expectations (move-zeroes, two-sum-ii).

### 1.2 Specific failure mode (per [lessons/design/sec1_insight.md](../../../lessons/design/sec1_insight.md))

The design spec mandates:

> Foundational concept first — not the algorithm. Before any algorithm is mentioned, establish what the problem is really asking in computational terms.
>
> Equivalence chain — every ≡ line gets a concrete pill example. Symbols alone do not teach.

Drifted lessons open §1 with phrasing like "Use array indices as a hash table" (first-missing-positive) or "Four boundaries, shrinking layer by layer" (spiral-matrix) — those are descriptions of the solution, not the conceptual setup that makes the solution obvious.

### 1.3 Dependency on PLAN-016

This plan executes against the lint gate from [PLAN-016](PLAN-016_self_healing_pipeline.md). Every rewrite must pass `python3 scripts/lint_lesson.py <slug>` before being marked `lesson_status=generated`. If PLAN-016 ships first, the audit baseline in `baseline_audit_2026-05-19.md` becomes the authoritative scope of this plan.

### 1.4 Schema drift (subset of the work)

A smaller, separate issue exists for two lessons:

- **count-permutations-with-inversion-requirement**: HTML exists but no plan.md. Must write plan.md in PLAN-011 format.
- **maximum-subarray, merge-intervals, product-of-array-except-self**: plan.md is PLAN-011 format but `## 10. Python verification` block may be missing or stale; verify and re-trace.

These are folded into the per-lesson tasks below rather than treated as a separate phase.

---

## 2. Goals

1. **All seven drifted lessons pass PLAN-016's lint** — `python3 scripts/lint_lesson.py <slug>` exits 0 after rewrite for: spiral-matrix, find-the-duplicate-number, first-missing-positive, maximum-subarray, merge-intervals, product-of-array-except-self, count-permutations-with-inversion-requirement.

2. **valid-palindrome §1 chain-box content deepened** to show real reductions (each ≡ row has a concrete pill example demonstrating the reduction, not a restatement). Currently structural but shallow.

3. **count-permutations gains a PLAN-011 plan.md** with Python verification trace.

4. **No regressions in already-passing lessons** — `scripts/audit_lessons.py` shows the same or fewer failing lessons after this plan completes vs. before. (The four goldens stay passing.)

5. **REPORT-015 documents** every rewrite, every lint result, and what was learned for future plans.

**Measurable outcomes (each is a single lint invocation):**
- ✅ `lint_lesson.py spiral-matrix` exits 0
- ✅ `lint_lesson.py find-the-duplicate-number` exits 0
- ✅ `lint_lesson.py first-missing-positive` exits 0
- ✅ `lint_lesson.py maximum-subarray` exits 0
- ✅ `lint_lesson.py merge-intervals` exits 0
- ✅ `lint_lesson.py product-of-array-except-self` exits 0
- ✅ `lint_lesson.py count-permutations-with-inversion-requirement` exits 0
- ✅ `lint_lesson.py valid-palindrome` exits 0 (was borderline; depth confirmed)

---

## 3. Non-goals

- **Rewriting the four golden lessons.** They are canonical references. No edits unless the lint reveals a bug that affects all lessons.
- **Rewriting easy/short-problem lessons (move-zeroes, two-sum-ii).** Their §1 is short because the problem is short. If lint warns but doesn't fail, leave them. If lint fails, address in a follow-up plan.
- **Bulk-converting pre-golden lessons** (lessons generated before 2026-05-08). They use the legacy panels-fixed format and a future plan can address them.
- **Implementing PLAN-011's deterministic spec→HTML renderer.** Still deferred.
- **§3 and §6 quality work.** PLAN-016 deferred §3/§6 inlining; their drift remediation is also deferred.

---

## 4. Approach

### 4.1 Execution order

1. **Confirm PLAN-016 is `Completed`** (or at least task 7 done — lint validated against goldens). If 016 is not done, stop and execute that plan first.
2. **Run audit baseline** (`python3 scripts/audit_lessons.py`) to confirm the exact lint failures match this plan's scope.
3. **Rewrite per lesson** in priority order (below). Each lesson:
   - Read its plan.md.
   - If plan.md fails schema (missing PLAN-011 sections or Python trace), fix plan.md first.
   - Rewrite §1 against the matching canonical pattern from `sec1_insight.md` (post-PLAN-016, this is inline in the section file).
   - Re-lint. Iterate until exit 0.
   - PATCH `lesson_status=generated`.

### 4.2 Priority order

**Highest priority (severe drift, simplest problems — fast wins):**
1. maximum-subarray (25-line §1, classic DP)
2. product-of-array-except-self (25-line §1, prefix_scan archetype)
3. merge-intervals (25-line §1, sorting + sweep)

**High priority (clear drift):**
4. first-missing-positive (32-line §1, custom archetype)
5. spiral-matrix (41-line §1, custom archetype)
6. find-the-duplicate-number (45-line §1, custom archetype)

**Lower priority (less drift, more work):**
7. count-permutations-with-inversion-requirement (57-line §1 AND missing plan.md)
8. valid-palindrome (85-line §1 — only chain-box content deepening needed)

### 4.3 Per-lesson rewrite procedure

For each lesson:

```
1. Read lessons/<slug>/plan.md and lesson.html.
2. Identify archetype from plan.md (or re-derive if missing).
3. Load lessons/design/sec1_insight.md — focus on the inline canonical pattern
   for the matching archetype. Do NOT open the full golden lesson.html.
4. Rewrite §1 in lesson.html, replacing problem-specific tokens in the
   canonical pattern. Target: line count ≥ 50, chain-box with ≥ 3 rows
   (each chain-row containing a chain-example), foundational visual,
   kernel infobox.
5. Run python3 scripts/lint_lesson.py <slug>. On failure, read the error,
   fix specifically what failed, re-lint.
6. Manual check: open the lesson in a browser. Does §1 build the concept
   before naming the algorithm?
7. PATCH lesson_status=generated.
```

### 4.4 Handling count-permutations (extra step)

This lesson has no plan.md. The procedure has an extra preface:

```
0a. Read existing lesson.html to extract problem statement, archetype,
    examples used.
0b. Write lessons/count-permutations-with-inversion-requirement/plan.md
    in PLAN-011 format with all sections through §10 Python verification.
0c. Run Python trace; paste output into plan.md §10.
0d. Then proceed with the normal §1 rewrite procedure.
```

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| **Phase 0: Preconditions** | | | |
| 1 | Verify PLAN-016 is Completed (or at least lint script exists and passes all four goldens) | 5 min | PLAN-016 |
| 2 | Run `python3 scripts/audit_lessons.py` — confirm scope matches this plan's lesson list | 10 min | 1 |
| **Phase 1: High-priority quality rewrites (severe drift)** | | | |
| 3 | maximum-subarray: rewrite §1 against prefix_scan canonical pattern | 60 min | 2 |
| 4 | product-of-array-except-self: rewrite §1 against prefix_scan canonical pattern | 60 min | 2 |
| 5 | merge-intervals: rewrite §1 against custom-archetype pattern (sort + sweep) | 75 min | 2 |
| **Phase 2: Medium-priority quality rewrites** | | | |
| 6 | first-missing-positive: rewrite §1 against custom-archetype pattern (array as hash table — but build that concept first) | 75 min | 2 |
| 7 | spiral-matrix: rewrite §1 against custom-archetype pattern (boundary shrinking) | 75 min | 2 |
| 8 | find-the-duplicate-number: rewrite §1 against custom-archetype pattern (Floyd's cycle on implicit list) | 75 min | 2 |
| **Phase 3: Special cases** | | | |
| 9 | count-permutations: write PLAN-011 plan.md with Python trace | 75 min | 2 |
| 10 | count-permutations: rewrite §1 | 60 min | 9 |
| 11 | valid-palindrome: deepen chain-box content (each ≡ row gets a real reduction + pill example) | 45 min | 2 |
| **Phase 4: Validation & closure** | | | |
| 12 | Run `audit_lessons.py` — confirm 7 previously-failing now pass | 10 min | 3–11 |
| 13 | Manual browser check on all 8 rewritten lessons | 30 min | 12 |
| 14 | PATCH `lesson_status=generated` for any lessons that aren't already (most should already be PATCHed during rewrite) | 10 min | 13 |
| 15 | Write REPORT-015 — outcomes, lint output before/after, lessons learned | 45 min | 14 |

**Total:** ~11 hours, split across 2–3 sessions:
- Session 1: tasks 1–5 (~3.5 hr)
- Session 2: tasks 6–10 (~5 hr)
- Session 3: tasks 11–15 (~2.5 hr)

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Lint script not available (PLAN-016 not built) | High if 016 deferred | Blocks plan | Task 1 hard-gates; if 016 isn't done, stop and finish 016 first. |
| Custom-archetype lessons (spiral-matrix, find-the-duplicate-number, first-missing-positive) don't fit any of the four canonical patterns cleanly | Medium | Medium | The four canonical patterns are starting templates, not rigid. Adapt the chain-box structure to the problem; lint enforces structural minimums, not exact match. |
| Rewriting §1 breaks something downstream in the lesson (links, JS references) | Low | Medium | Lint covers schema; manual browser check (task 13) verifies functionality. Section §1 has no JS hooks — safe to rewrite independently. |
| Time estimates blow up on custom-archetype lessons | Medium | Medium | Budget includes 75 min for the harder ones. If task 6 (first-missing-positive) takes 2 hours, pause and assess before doing 7 and 8. |
| User wants different priority order | Medium | Low | Priority is a recommendation. Order can shuffle without breaking the plan. |
| The "concept first, then algorithm" rewrite produces something the user doesn't agree is better | Medium | High | After task 3 (first lesson rewritten), pause and show the diff. If user rejects the approach, recalibrate before doing the next six. |
| Python trace for count-permutations is hard to produce (unknown problem) | Medium | Medium | If trace is blocked, partial credit: write plan.md without §10 trace, mark as a follow-up. Don't gate the lesson on this. |

---

## 7. Success criteria

✅ **Lint passes:**
- All 8 listed lessons (the 7 rewrites + valid-palindrome) exit 0 from `lint_lesson.py`.
- All 4 goldens still exit 0 (no regression).

✅ **Plan.md complete:**
- `lessons/count-permutations-with-inversion-requirement/plan.md` exists in PLAN-011 format.

✅ **Audit baseline improves:**
- Before-after diff in `REPORT-015` shows 8 fewer failures in `audit_lessons.py`.

✅ **Manual verification:**
- Each rewritten lesson, opened in a browser, has a §1 that builds the foundational concept before naming the algorithm. The reader can derive *why* the algorithm works, not just *what* it does.

✅ **No collateral damage:**
- No lesson previously passing lint now fails.
- No JS or static asset changes (this plan only touches lesson HTML and lesson plan.md).

✅ **Report written:**
- `REPORT-015` documents outcomes, lessons learned, and any follow-ups (e.g., move-zeroes / two-sum-ii if lint warned).

---

## 8. References

- [AGENT_MD/plan/plans/PLAN-016_self_healing_pipeline.md](PLAN-016_self_healing_pipeline.md) — the lint gate this plan executes against
- [AGENT_MD/plan/plans/PLAN-011_lesson_gen_efficiency.md](PLAN-011_lesson_gen_efficiency.md) — origin of the modular design
- [lessons/LESSON_DESIGN.md](../../../lessons/LESSON_DESIGN.md) — lean index
- [lessons/design/sec1_insight.md](../../../lessons/design/sec1_insight.md) — §1 principles (extended by PLAN-016 with inline canonical patterns)
- [lessons/design/archetypes.md](../../../lessons/design/archetypes.md) — archetype taxonomy for matching canonical patterns
- [AGENT_MD/plan/rules.md](../rules.md) — plan/report conventions
- Goldens for archetype reference: `lessons/3sum`, `lessons/permutation-in-string`, `lessons/trapping-rain-water`, `lessons/median-of-two-sorted-arrays`

---

## Decision gate for user

Before executing, confirm:

1. **Scope of 8 lessons matches your understanding** of which lessons drifted? (spiral-matrix, find-the-duplicate-number, first-missing-positive, maximum-subarray, merge-intervals, product-of-array-except-self, count-permutations, valid-palindrome)
2. **Priority order** — severe-drift trio first (maximum-subarray, product-of-array-except-self, merge-intervals), then custom-archetype, then special cases?
3. **Execute PLAN-016 first** to get the lint gate, then PLAN-015 against it?
4. **OK with 11 hours over 2–3 sessions** for the rewrites?
