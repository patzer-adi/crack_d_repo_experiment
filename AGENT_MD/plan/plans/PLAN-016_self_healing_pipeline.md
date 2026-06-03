# PLAN-016: Self-Healing Lesson Generation Pipeline

**Created:** 2026-05-19
**Status:** Completed
**Addresses:** Lessons generated after the four goldens drift in §1 quality (sec-by-sec content is shallow, "describes the algorithm" instead of "builds the foundational concept"). No mechanism today detects this before `lesson_status=generated`. This plan adds a lean, machine-checkable gate and inlines canonical §1 markup so the goldens never need full-file loads.

---

## 1. Context & motivation

### 1.1 The observed drift

Across lessons generated between 2026-05-15 and 2026-05-19, §1 ("The Insight") consistently runs at ½ to ⅓ of the golden line count, and most omit the equivalence-chain markup that the design spec ([lessons/design/sec1_insight.md](../../../lessons/design/sec1_insight.md)) names as the key teaching device.

Concrete counts of §1 line length:

| Lesson | §1 lines | chain-box | Verdict |
|---|---|---|---|
| 3sum (golden) | 90 | ✓ | golden bar |
| permutation-in-string (golden) | 91 | ✓ | golden bar |
| trapping-rain-water (golden) | 49 | (visual-led) | golden bar |
| median-of-two-sorted-arrays (golden) | 113 | ✓ | golden bar |
| valid-palindrome | 85 | ✓ but shallow | borderline |
| find-the-duplicate-number | 45 | ✗ | drift |
| spiral-matrix | 41 | ✗ | drift |
| first-missing-positive | 32 | ✗ | drift |
| maximum-subarray | 25 | ✗ | severe drift |
| merge-intervals | 25 | ✗ | severe drift |
| product-of-array-except-self | 25 | ✗ | severe drift |

### 1.2 Why it happened

The PLAN-011 design system separated principles (in `sec<N>_*.md`) from canonical examples (line ranges in goldens). Operationally, that means an agent authoring §1 of a new lesson must load both the principles file and the right range of a golden. In practice, the agent often skips the golden excerpt — the section files describe the rule but never *show* the markup pattern. Output regresses to a generic paragraph + small visual that satisfies the section's *existence* but not its *depth*.

### 1.3 Why a self-healing pipeline matters

- **Detection now is manual.** A human has to open a new lesson, open a golden, and eyeball the difference. That gate has clearly been bypassed.
- **Token cost of "load full golden for reference"** is 15–25k tokens per archetype. Doing it correctly today is the *expensive* path; doing it lazily produces the drift.
- **Inverting the cost curve.** If the canonical pattern is *inline in the section file*, the cheap path is also the correct path. Drift becomes the harder option.

### 1.4 Token economics

Current per-lesson generation (when discipline holds):

```
Loaded once per session:    ~9k tok  (index + archetypes + verify + classes + template)
Per section authoring:      31k tok  (13 × sec file + 13 × golden line range)
Authoring output:           21k tok  (plan.md + lesson.html written)
─────────────────────────────────────
Total per lesson:          ~61k tok
```

Loading the *full* golden lesson.html instead of the named line range (the common failure) adds 15–25k tok per archetype touched. Inlining the canonical pattern into the section file (≈30 added lines per section × ≈600 tok/line) costs ~3k more in the always-loaded path but eliminates the per-archetype golden excerpt (~1.5k saved per section × 13 sections = 19k saved).

**Net effect of inlining §1 alone:** -3.5k tok per lesson. Inlining §1/§3/§6: -10k tok per lesson.

---

## 2. Goals

1. **Inline canonical §1 markup** for all four archetypes into `lessons/design/sec1_insight.md`. After this change, authoring §1 needs only this one file — no golden excerpt load.

2. **Add machine-checkable acceptance criteria** to `sec1_insight.md` so §1 quality becomes pass/fail without LLM judgment for the structural parts.

3. **Build `scripts/lint_lesson.py`** that exits non-zero when a lesson fails §1 acceptance criteria. Runs in < 1 second per lesson.

4. **Build `scripts/audit_lessons.py`** that walks `lessons/*/lesson.html`, calls lint on each, and prints a pass/fail/warn table. Run on demand.

5. **Update `.claude/commands/batch-lesson.md`** so the skill invokes lint as a hard gate before PATCH `lesson_status=generated`, and adds a §1 self-review checkpoint that compares the new §1 against the inlined canonical pattern.

6. **Document the token budget** in `lessons/LESSON_DESIGN.md` so any future session can verify its loads.

7. **Archive `lessons/LESSON_DESIGN_v2.md`** to remove the temptation to load the 239-line monolith.

**Measurable outcomes:**
- ✅ All four goldens pass `scripts/lint_lesson.py --section 1` with zero warnings.
- ✅ All seven currently-drifted lessons (see §1.1) fail `scripts/lint_lesson.py --section 1`. (This sizes the PLAN-015 backfill.)
- ✅ batch-lesson skill refuses to PATCH `lesson_status=generated` when lint fails.
- ✅ `LESSON_DESIGN.md` has a "Token budget per lesson" block under 20 lines.
- ✅ `LESSON_DESIGN_v2.md` is renamed/moved to remove it from default load paths.

---

## 3. Non-goals

- Inlining §3 (Translations) and §6 (Code Viz) canonical patterns. They're high-drift candidates too, but §1 is the steepest. Deferred to a follow-up plan once §1 lands and we see the lint catching real drift.
- Lint for sections other than §0 metadata, §1 markup, and basic schema. Per-section deep checks for §3/§6/§10 deferred.
- LLM self-review for sections beyond §1.
- Rewriting any actual lesson content — that's PLAN-015's job. This plan only builds the gate.
- The deterministic spec→HTML renderer (PLAN-011 §4.5–4.6). Still deferred.

---

## 4. Approach

### 4.1 Inline canonical §1 patterns

Append to `lessons/design/sec1_insight.md` four blocks — one per archetype — each containing the actual HTML markup pattern (≈30–40 lines) lifted from the matching golden. Format:

```markdown
## Canonical pattern — two-pointer archetype

Source: lifted from `lessons/3sum/lesson.html` lines 54–143. The agent should
treat this as the section's structure; replace problem-specific tokens only.

\`\`\`html
<div class="section">
  <p class="sec-label">The Insight</p>
  <p class="sec-title">[PROBLEM-SPECIFIC INSIGHT TITLE]</p>
  <p class="body">[KERNEL PARAGRAPH WITH ALGEBRAIC OR LOGICAL TRANSFORMATION]</p>

  <!-- Foundational visual: number-line / bar chart / matrix -->
  <div style="margin:1.25rem 0">
    [PROBLEM-SPECIFIC VISUAL]
  </div>

  <div class="infobox success">
    <p class="infobox-t">The kernel</p>
    <p class="infobox-d">[ONE PARAGRAPH ALGORITHM SUMMARY]</p>
  </div>

  <p class="body" style="margin-top:1rem">Why [CORE TECHNIQUE] is the key:</p>
  <div class="chain-box">
    <div class="chain-row">
      <span class="chain-sym"></span>
      <div class="chain-content">
        <div class="chain-text">[THE PROBLEM RESTATED]</div>
        <div class="chain-note">the problem</div>
      </div>
    </div>
    <div class="chain-row">
      <span class="chain-sym">≡</span>
      <div class="chain-content">
        <div class="chain-text">[FIRST REDUCTION]</div>
        <div class="chain-note">[WHY THIS REDUCTION IS VALID]</div>
        <div class="chain-example">
          [CONCRETE PILL EXAMPLES showing the reduction in action]
        </div>
      </div>
    </div>
    <!-- Two more chain-rows: ≡ rows showing further reductions -->
  </div>
</div>
\`\`\`
```

Repeat for sliding_window, prefix_scan, divide_conquer. The prefix_scan variant omits the chain-box (matching trapping-rain-water's visual-led style).

### 4.2 Machine-checkable acceptance criteria

Append to `sec1_insight.md`:

```markdown
## Acceptance criteria (machine-checkable)

§1 MUST contain (lint enforces):
  - Exactly one `<p class="sec-label">The Insight</p>` line.
  - Exactly one `<p class="sec-title">…</p>` line.
  - At least one `<p class="body">` paragraph ≥ 200 characters (the kernel paragraph).
  - Exactly one `<div class="infobox success">` block.
  - Either: a `<div class="chain-box">` with ≥ 3 `<div class="chain-row">` children
    AND at least 2 of those rows contain a `<div class="chain-example">`;
    OR: a foundational visual block ≥ 30 lines positioned BEFORE the `infobox success`.
  - Total §1 line count ≥ 50.

§1 MUST NOT (lint warns):
  - Begin the sec-title with "Use X as Y" or "Traverse <N> <thing>" — these
    are algorithm descriptions, not foundational concepts.
```

### 4.3 Lint script

`scripts/lint_lesson.py`:

```
Usage: python3 scripts/lint_lesson.py <slug> [--section N] [--strict]

Reads lessons/<slug>/lesson.html and lessons/<slug>/plan.md.
Exit 0 if pass, 1 if fail, 2 if warn-only.
Output: structured JSON when --json, human-readable otherwise.

Checks:
  Schema:
    - plan.md has '## Metadata' and 'Archetype:' line
    - plan.md has '## 1. Clarifying questions' (PLAN-011 marker)
    - lesson.html links static/lesson.css and static/lesson.js
    - lesson.html has 11 <div class="section"> blocks
  §1 (per acceptance criteria above):
    - sec-label / sec-title / kernel paragraph present
    - infobox success present
    - chain-box OR foundational visual ≥ 30 lines
    - §1 line count ≥ 50
  §1 warnings:
    - sec-title pattern flag (algorithm-description heuristic)
```

Implementation: stdlib only (re, pathlib, json). No HTML parser needed — line-based regex is sufficient and keeps the script under 300 lines.

### 4.4 Audit script

`scripts/audit_lessons.py`:

```
Usage: python3 scripts/audit_lessons.py [--json]

Iterates lessons/*/lesson.html, calls lint_lesson.py per slug.
Prints summary table:

  PASS  3sum
  PASS  permutation-in-string
  ...
  WARN  valid-palindrome           §1: sec-title heuristic flag
  FAIL  spiral-matrix              §1: no chain-box, foundational visual 12 lines
  FAIL  first-missing-positive     §1: line count 32 < 50

  Totals: 18 pass, 9 warn, 5 fail
```

Exit 0 always (audit reports state; failure is informational).

### 4.5 batch-lesson skill update

Append to `.claude/commands/batch-lesson.md` (step 6 becomes):

```
6. On approval, author lessons/<slug>/lesson.html section-by-section per the
   index in LESSON_DESIGN.md. For each section, load only the design file it
   names. Use static/CLASSES.md for class names.

   After §1 is written:
     a. Run python3 scripts/lint_lesson.py <slug> --section 1.
        If lint fails, rewrite §1 and re-lint.
     b. Self-review: load only the matching archetype's canonical pattern from
        sec1_insight.md. Verify the new §1 (i) builds a foundational concept
        before stating the algorithm, (ii) has concrete pill examples in any
        chain-row, (iii) doesn't open with "Use X as Y". Rewrite once if any
        fail; do NOT loop indefinitely.

   After all sections written:
     c. Run python3 scripts/lint_lesson.py <slug>. Hard stop if any check
        fails. Do NOT PATCH lesson_status=generated until lint exits 0.

   Then PATCH as before.
```

### 4.6 Token budget block in LESSON_DESIGN.md

Insert after "Always true" section:

```markdown
## Token budget per lesson

Authoring one lesson should fit in ~60k tokens of read context. If a session
loads more, something is being read that shouldn't be.

| Item | Tokens (~) | Load |
|---|---|---|
| LESSON_DESIGN.md (this file) | 1.5k | once |
| design/archetypes.md | 0.5k | once |
| design/python_verify.md | 1.0k | once (plan trace) |
| static/CLASSES.md | 2.0k | once |
| lessons/_template.html | 4.0k | once |
| design/sec<N>_*.md (×13) | 12k | per section |
| Inline canonical patterns (in sec files post-PLAN-016) | included above | per section |
| plan.md being authored | 3k | written |
| lesson.html being authored | 18k | written |
| **Total** | **~42k read + ~21k written ≈ 63k** | |

Do NOT load:
- Full golden lesson.html files (use sec file inline patterns + reference lines only)
- static/lesson.css (use CLASSES.md)
- LESSON_DESIGN_v2.md (archived in lessons/archive/)
- Sibling lesson plan.md or lesson.html (re-derive per problem)
```

### 4.7 Archive v2

`git mv lessons/LESSON_DESIGN_v2.md lessons/archive/LESSON_DESIGN_v2.md`. Update the one reference in `lessons/LESSON_DESIGN.md` footer.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Add "Acceptance criteria (machine-checkable)" block to `lessons/design/sec1_insight.md` | 20 min | — |
| 2 | Lift canonical §1 pattern from `3sum/lesson.html` lines 54–143, inline into `sec1_insight.md` as `## Canonical pattern — two-pointer` | 30 min | 1 |
| 3 | Repeat for sliding_window (permutation-in-string lines 160–250) | 30 min | 1 |
| 4 | Repeat for prefix_scan (trapping-rain-water lines 114–162) | 25 min | 1 |
| 5 | Repeat for divide_conquer (median-of-two-sorted-arrays lines 102–214) | 30 min | 1 |
| 6 | Write `scripts/lint_lesson.py` — schema + §1 checks per §4.3 | 90 min | 1 |
| 7 | Test lint against all four goldens — must exit 0 | 20 min | 6 |
| 8 | Test lint against three known-drifted lessons (spiral-matrix, first-missing-positive, maximum-subarray) — must exit 1 | 15 min | 6 |
| 9 | Write `scripts/audit_lessons.py` — wraps lint per §4.4 | 30 min | 6 |
| 10 | Run audit, capture output as `AGENT_MD/plan/reports/baseline_audit_2026-05-19.md` (informs PLAN-015 scope) | 15 min | 9 |
| 11 | Update `.claude/commands/batch-lesson.md` per §4.5 | 30 min | 6 |
| 12 | Insert "Token budget per lesson" block into `lessons/LESSON_DESIGN.md` per §4.6 | 15 min | — |
| 13 | `git mv lessons/LESSON_DESIGN_v2.md lessons/archive/LESSON_DESIGN_v2.md` and update one reference in `LESSON_DESIGN.md` | 10 min | — |
| 14 | Write REPORT-016 documenting outcomes and the audit baseline | 30 min | 11, 12, 13 |

**Total:** ~6 hours, splittable across two sessions (1–8 in session 1; 9–14 in session 2).

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Lint regex misses a valid §1 variant (false positive against a golden) | Medium | High | Task 7 is "must pass against all four goldens" — if it fails, fix the regex before proceeding. |
| Inlined canonical pattern drifts from the golden over time | Low | Medium | Each canonical block ends with "Source: lifted from `lessons/<x>/lesson.html` lines A–B (as of YYYY-MM-DD)". A follow-up plan can re-sync if a golden changes. |
| §1 line-count floor (50) excludes legitimately short prefix-scan style | Low | Medium | Trapping-rain-water §1 is 49 lines; we set floor to 50 deliberately so it would *just* fail. Adjust to 45 if task 7 reveals this is wrong. |
| LLM self-review (step 6b in batch-lesson) loops indefinitely rewriting §1 | Low | High | Explicit "Rewrite once if any fail; do NOT loop indefinitely" wording. After one rewrite, ship and let lint/audit be the final check. |
| Token budget block becomes stale as design evolves | Medium | Low | Budget is a guideline, not enforcement. Update during the same PR that changes a sec file's size. |
| Archiving v2 breaks a stale reference somewhere | Low | Low | `grep -r "LESSON_DESIGN_v2" .` before the rename to surface references. |

---

## 7. Success criteria

✅ **Inline canonical patterns:**
- `sec1_insight.md` has four `## Canonical pattern — <archetype>` blocks, each ≥ 30 lines, with "Source: lifted from … lines A–B" provenance.

✅ **Acceptance criteria documented:**
- `sec1_insight.md` has an "Acceptance criteria (machine-checkable)" block matching what lint enforces.

✅ **Lint operational:**
- `python3 scripts/lint_lesson.py 3sum` exits 0.
- `python3 scripts/lint_lesson.py permutation-in-string` exits 0.
- `python3 scripts/lint_lesson.py trapping-rain-water` exits 0.
- `python3 scripts/lint_lesson.py median-of-two-sorted-arrays` exits 0.
- `python3 scripts/lint_lesson.py spiral-matrix` exits 1.
- `python3 scripts/lint_lesson.py first-missing-positive` exits 1.

✅ **Audit operational:**
- `python3 scripts/audit_lessons.py` prints a pass/warn/fail table over all lessons.
- Output is captured into `baseline_audit_2026-05-19.md`.

✅ **batch-lesson enforces lint:**
- The skill step 6 explicitly calls lint and refuses PATCH on non-zero exit.

✅ **Token budget documented:**
- `LESSON_DESIGN.md` has the "Token budget per lesson" block ≤ 25 lines.

✅ **v2 archived:**
- `lessons/LESSON_DESIGN_v2.md` does not exist at that path; `lessons/archive/LESSON_DESIGN_v2.md` does.

---

## 8. References

- [lessons/LESSON_DESIGN.md](../../../lessons/LESSON_DESIGN.md) — current lean index (PLAN-011 output)
- [lessons/design/sec1_insight.md](../../../lessons/design/sec1_insight.md) — file this plan extends
- [lessons/design/archetypes.md](../../../lessons/design/archetypes.md) — four-archetype taxonomy
- [.claude/commands/batch-lesson.md](../../../.claude/commands/batch-lesson.md) — skill to update
- [AGENT_MD/plan/plans/PLAN-011_lesson_gen_efficiency.md](PLAN-011_lesson_gen_efficiency.md) — the infrastructure this plan enforces
- [AGENT_MD/plan/plans/PLAN-015_lesson_generation_drift_remediation.md](PLAN-015_lesson_generation_drift_remediation.md) — the companion remediation plan (executes against this plan's lint)
- [AGENT_MD/plan/rules.md](../rules.md) — plan/report conventions
- Reference goldens for canonical pattern extraction: `lessons/3sum/lesson.html`, `lessons/permutation-in-string/lesson.html`, `lessons/trapping-rain-water/lesson.html`, `lessons/median-of-two-sorted-arrays/lesson.html`

---

## Decision gate for user

Before executing, confirm:

1. **Scope acceptable?** §1 only — §3 (Translations) and §6 (Code Viz) inlining deferred to a follow-up.
2. **Line-count floor for §1 at 50?** trapping-rain-water (golden) is 49 — adjust to 45 if you want it inside the gate without exception.
3. **Build order — 016 before 015?** Building 016 first means PLAN-015's regeneration is automatically lint-verified. Reverse order is possible but the regenerations land without a gate.
