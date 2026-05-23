# PLAN-017: §1 animation, §7 multi-example, animation pacing

**Created:** 2026-05-20
**Status:** Completed
**Addresses:** Three convention changes surfaced during PLAN-015 execution: (1) §1 "The Insight" visuals should be animated with prev/next/auto controls instead of static; (2) §7 dry-run should be repositioned as multi-example practice rather than a re-walk of §6; (3) auto-mode animation speeds (especially brute-force at 300 ms) are too fast for teaching pace. These conventions must land before resuming the remaining 7 PLAN-015 lesson rewrites so they are authored against a stable target.

---

## 1. Context & motivation

While executing PLAN-015's first rewrite (maximum-subarray, 2026-05-20), the user reviewed the visual-led §1 output and raised four concerns:

1. **All animations should have button controls** — current §1 visuals (including the rewritten one) are static. The user wants §1 visuals animated with prev/next/auto/reset controls.
2. **Auto mode is too fast** — `bfTogglePlay` runs at 300 ms per step; the eye can't follow, defeating the teaching purpose.
3. **Cell colors vary per lesson** — each lesson defines its own `.fmp-cell`, `.fdn-cell`, `.sm-cell`, `.ks-cell`. The user explicitly chose to defer this work; recorded here for follow-up.
4. **§6 and §7 overlap** — both animate the optimal algorithm. Distinction needs to earn its keep.

After discussion the user decided: animate §1 with controls; reposition §7 as multi-example practice; defer color unification.

This plan implements the first two decisions plus the speed bump. It pauses PLAN-015 until the new conventions land, so the remaining 7 lessons are written once, not rewritten when conventions shift.

## 2. Goals

1. **§1 visuals are animated by default** — every lesson's §1 includes prev/next/auto/reset buttons and a step generator (`siGenSteps` or similar). The static-snapshot style is deprecated.

2. **§7 is reframed as multi-example dry-run practice** — three sample-input buttons, the reader picks any and walks through. Distinct from §6, which animates one example tied to code lines.

3. **Auto-mode speeds bumped** — `bfTogglePlay` 300 → 700 ms; `cvTogglePlay` 900 → 1100 ms; `drTogglePlay` 1100 → 1400 ms. Reader can follow the state changes at default speed without pausing.

4. **Lint enforces §1 animation presence** — `scripts/lint_lesson.py` requires the §1 markup to include a `prev/next/auto/reset` control row (heuristic: section has `<button class="ctrl-btn"` referencing `siNext` / `siPrev` / `siTogglePlay` or similar). Fails if not.

5. **Canonical patterns in `sec1_insight.md` include animation JS templates** — alongside the four archetype HTML patterns, each gets a JS step-generator skeleton (~20 lines) showing the shape `siGenSteps` should take per archetype.

6. **batch-lesson skill workflow updated** — the §1 authoring step explicitly references the animation requirement and points at the new canonical JS template.

**Measurable outcomes:**
- ✅ `static/lesson.js` shows the three new speed values
- ✅ `sec1_insight.md` has an "§1 animation conventions" section + four JS templates (one per archetype)
- ✅ `sec7_dry_run.md` opens with "§7 is multi-example practice for the reader, distinct from §6's single-example code walkthrough"
- ✅ `scripts/lint_lesson.py` rejects a §1 that has no animation control row (against a known-failing fixture, exit 1)
- ✅ `lint_lesson.py` accepts §1 with animation controls present (e.g., maximum-subarray after revision exits 0)
- ✅ `.claude/commands/batch-lesson.md` step 6 references "§1 animation generator per archetype template in `sec1_insight.md`"

## 3. Non-goals

- **Migrating existing lessons' §1 to animated form.** Only maximum-subarray is revised here (proof-of-concept). The other 7 PLAN-015 lessons land animated when PLAN-015 resumes; the remaining ~10 lessons follow their own cadence.
- **Uniform `.cell` color vocabulary** — user explicitly deferred.
- **Refactoring §6 step-generator to be sharable with §7** — §7 stays its own generator, just gets multi-example reframing in the design doc and template.
- **Touching shared JS helpers beyond the three speed constants** — no architecture changes to `static/lesson.js`.

## 4. Approach

### 4.1 Speed bumps (15 min)

Single edit to `static/lesson.js`:

```js
// before
function cvTogglePlay(){...setInterval(...,900);}
function drTogglePlay(){...setInterval(...,1100);}
function bfTogglePlay(){...setInterval(...,300);}

// after
function cvTogglePlay(){...setInterval(...,1100);}
function drTogglePlay(){...setInterval(...,1400);}
function bfTogglePlay(){...setInterval(...,700);}
```

`siTogglePlay` (§1) will be defined per-lesson at 1200 ms (between cv and dr — §1 is conceptual, slower is fine).

### 4.2 §1 animation convention (90 min)

Append to `lessons/design/sec1_insight.md`:

```markdown
## §1 animation conventions

Every §1 foundational visual MUST be animated with reader controls. The convention
mirrors §6/§7:

- Step generator function: name `siGenSteps(input)` returning an array of step objects
- State variables: `let siSteps=[]; let siCur=0; let siTimer=null;`
- Control row markup: prev/auto/next/reset buttons calling `siPrev() / siTogglePlay() / siNext() / siReset()`
- Auto-mode speed: 1200 ms (slower than dr; §1 is conceptual)
- Step count target: 4–8 steps for §1 (vs 10–15 for cv/dr). §1 builds intuition; brevity matters.

Each archetype's canonical pattern (below) shows the matching JS skeleton.
```

Then for each of the four archetype canonical patterns currently in `sec1_insight.md`, add a `<script>`-block template showing the siGenSteps shape. Per-archetype skeleton (~20 lines):

```html
<script>
  let siSteps = siGenSteps([INITIAL_INPUT]);
  let siCur = 0;
  let siTimer = null;
  function siGenSteps(input) {
    const steps = [];
    // archetype-specific state evolution:
    //   two_pointer: i / L / R movements
    //   sliding_window: window expansion + diff updates
    //   prefix_scan: walk index by index with running max/min
    //   divide_conquer: partition boundary movement
    return steps;
  }
  function siRender(st) { /* update DOM cells per st */ }
  function siNext() { if (siCur < siSteps.length - 1) { siCur++; siRender(siSteps[siCur]); } else siStopPlay(); }
  function siPrev() { if (siCur > 0) { siCur--; siRender(siSteps[siCur]); } }
  function siReset() { siStopPlay(); siCur = 0; siRender(siSteps[0]); }
  function siStopPlay() { clearInterval(siTimer); siTimer = null; document.getElementById('si-bplay').textContent = '▶ Auto'; }
  function siTogglePlay() {
    if (siTimer) { siStopPlay(); }
    else {
      document.getElementById('si-bplay').textContent = '⏸ Pause';
      siTimer = setInterval(() => { if (siCur < siSteps.length - 1) siNext(); else siStopPlay(); }, 1200);
    }
  }
  siRender(siSteps[0]);
</script>
```

### 4.3 §7 multi-example reframing (30 min)

Edit `lessons/design/sec7_dry_run.md`. Open with a clarifying paragraph:

> §7 is multi-example practice for the reader, distinct from §6's single-example code walkthrough. §6 ties one execution to the optimal algorithm's code lines so the reader sees what each line does. §7 provides 3 different example inputs the reader chooses from and walks through state-only (no code), to confirm they can predict the algorithm's behaviour on new inputs.

Then update the existing markup spec to require ≥ 3 example buttons (`<button class="ex-btn">`) and document that `drGenSteps` should accept any of the three.

### 4.4 Lint update (30 min)

Add to `scripts/lint_lesson.py` §1 checks:

```python
# §1 must have animation controls
control_btns = re.findall(r"siPrev\(\)|siNext\(\)|siTogglePlay\(\)|siReset\(\)", text)
if len(set(control_btns)) < 3:
    report.add("§1:animation controls present", False,
               f"§1 must include prev/next/auto/reset controls calling si* functions; found {len(set(control_btns))} of 4")
else:
    report.add("§1:animation controls present", True)
```

Acceptable variants: lessons may use `s1Prev/s1Next/...` or `siPrev/siNext/...` — but consistency within a lesson required.

Update `lessons/design/sec1_insight.md` acceptance criteria table to add this rule.

### 4.5 Revise maximum-subarray §1 as proof-of-concept (60 min)

Rebuild the foundational visual as an animated step-through. Each step shows: `nums[i]` highlighted as current; `cur` and `best` updating; an `extend` / `restart` badge appearing for that step. 9 steps (one per index of the canonical example).

Verify lint passes including the new animation-controls check.

### 4.6 Update batch-lesson skill (15 min)

In `.claude/commands/batch-lesson.md` step 6, add:

> When authoring §1: include the animation block per the archetype JS template in `sec1_insight.md`. §1 needs prev/next/auto/reset controls calling `siNext()` / `siPrev()` / `siTogglePlay()` / `siReset()`. Auto-mode runs at 1200 ms.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Edit `static/lesson.js` — bump bf/cv/dr speed defaults to 700/1100/1400 ms | 15 min | — |
| 2 | Add "§1 animation conventions" block to `sec1_insight.md` | 45 min | — |
| 3 | Add per-archetype JS step-generator skeletons (×4) to `sec1_insight.md` | 90 min | 2 |
| 4 | Update `sec1_insight.md` acceptance criteria — add animation-controls rule | 15 min | 2 |
| 5 | Reframe `sec7_dry_run.md` opening as multi-example practice | 30 min | — |
| 6 | Update `lint_lesson.py` — §1 must have prev/next/auto/reset controls | 45 min | 4 |
| 7 | Test lint: known-failing fixture must exit 1; goldens may still pass (they predate animation) | 15 min | 6 |
| 8 | Revise maximum-subarray §1 — animate the 9-step walkthrough | 90 min | 1, 3, 6 |
| 9 | Verify revised maximum-subarray passes lint (including animation-controls) | 10 min | 8 |
| 10 | Update `.claude/commands/batch-lesson.md` step 6 with §1 animation reference | 15 min | 3 |
| 11 | Re-run `audit_lessons.py` — confirm goldens warn (legacy static §1), maximum-subarray passes, others still fail as before | 15 min | 9 |
| 12 | Write REPORT-017 | 30 min | 11 |

**Total:** ~6 hours. One session.

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Goldens fail the new animation-controls lint (their §1 is static) | High | High | Treat goldens as legacy: lint rule emits **warning** when §1 has no animation controls AND lesson predates PLAN-017 (heuristic: check the data/problems.json `lesson_status` updated date, or simply downgrade to warn for the 4 named goldens by slug allowlist). Decision needed: warn vs fail. |
| Animating §1 requires significant DOM markup per lesson (each step needs cells updated) | Medium | Medium | Per-archetype JS templates in `sec1_insight.md` cut authoring cost by giving a known-good skeleton. First lesson (maximum-subarray) takes 90 min; subsequent should land in 45–60 min each. |
| §1 animation step count too high → lesson feels slow | Medium | Low | Convention says 4–8 steps for §1. Maximum-subarray will use 9 (one per index) — borderline. If reader feedback says too long, condense to 5–6 keyframes. |
| New speed defaults (1100/1400/1200 ms) feel slow to power users | Low | Low | Speeds are per-button defaults; user can still click Next manually. Slow-default favors first-time readers (the intended audience). |
| Lint regex for animation-controls misses a valid variant | Low | Medium | Test against maximum-subarray after authoring; if false positive, broaden regex. |

## 7. Success criteria

✅ **Speed bumps shipped:** `grep` `static/lesson.js` shows `bfTogglePlay` at 700, `cvTogglePlay` at 1100, `drTogglePlay` at 1400.

✅ **§1 animation conventions documented:** `sec1_insight.md` has the new section + 4 JS templates (one per archetype).

✅ **§7 reframed:** `sec7_dry_run.md` opens with the multi-example clarification.

✅ **Lint updated:** §1 animation-controls check present in `lint_lesson.py`; verified against maximum-subarray after revision (exits 0).

✅ **maximum-subarray §1 animated:** prev/next/auto/reset controls work in a browser; step generator walks 9 steps.

✅ **Audit baseline updated:** running `scripts/audit_lessons.py` reflects the new lint rule. The four goldens warn on missing animation controls (legacy status); maximum-subarray passes; other PLAN-015 targets still fail.

✅ **batch-lesson skill updated:** step 6 references the new §1 animation template.

✅ **REPORT-017 written:** documents what changed and confirms PLAN-015 can resume against the new conventions.

## 8. References

- [AGENT_MD/plan/plans/PLAN-015_lesson_generation_drift_remediation.md](PLAN-015_lesson_generation_drift_remediation.md) — paused pending this plan
- [AGENT_MD/plan/plans/PLAN-016_self_healing_pipeline.md](PLAN-016_self_healing_pipeline.md) — defined the lint gate this plan extends
- [lessons/design/sec1_insight.md](../../../lessons/design/sec1_insight.md) — file being extended
- [lessons/design/sec7_dry_run.md](../../../lessons/design/sec7_dry_run.md) — file being reframed
- [static/lesson.js](../../../static/lesson.js) — speed constants
- [scripts/lint_lesson.py](../../../scripts/lint_lesson.py) — new check added
- [.claude/commands/batch-lesson.md](../../../.claude/commands/batch-lesson.md) — workflow updated

---

## Decision gate for user

Before executing, confirm:

1. **Animation step count for §1:** convention says 4–8; maximum-subarray will use 9 (one per array index). Acceptable, or condense to 5–6 keyframes?
2. **Speed values OK?** bf 700 / cv 1100 / dr 1400 / si 1200 ms. Adjust if any feel off.
3. **Lint treatment of legacy goldens:** their §1 is static (no animation controls). Should lint **fail** them (forces backfill) or **warn** them (allows time)? I recommend warn.
