# REPORT-017: §1 animation, §7 multi-example, animation pacing

**Plan:** PLAN-017
**Completed:** 2026-05-20
**Author:** AI agent (Claude, opus-4-7)

---

## 1. Summary

Adopted three convention changes raised during PLAN-015 execution. §1 "The Insight" visuals are now mandatorily **animated with reader controls** (prev/auto/next/reset) instead of static multi-frame diagrams. §7 "Dry Run" is reframed as multi-example practice (≥ 3 example buttons) distinct from §6's single-example code walkthrough. Default auto-play speeds bumped: `bfTogglePlay` 300 → 700 ms, `cvTogglePlay` 900 → 1100 ms, `drTogglePlay` 1100 → 1400 ms (with new §1 `siTogglePlay` at 1200 ms).

Lint extended to enforce the animation requirement. The four named goldens (`3sum`, `permutation-in-string`, `trapping-rain-water`, `median-of-two-sorted-arrays`) are slugs-allowlisted to warn-only on the animation rule — they predate this convention and will backfill in a future plan. maximum-subarray was used as the proof-of-concept and is now the **only lesson passing** the post-PLAN-017 lint; PLAN-015's scope expands to bring all other lessons up.

## 2. Goals vs. actuals

| Goal (from plan §2) | Outcome | Evidence |
|---|---|---|
| §1 visuals animated by default | ✅ Met | sec1_insight.md has "§1 animation conventions" block + acceptance criteria addendum; lint enforces |
| §7 reframed as multi-example practice | ✅ Met | sec7_dry_run.md opens with "Purpose: multi-example practice, distinct from §6" + ≥ 3 example buttons requirement |
| Auto-mode speeds bumped | ✅ Met | static/lesson.js: bf 700, cv 1100, dr 1400 (was 300/900/1100) |
| Lint enforces §1 animation presence | ✅ Met | scripts/lint_lesson.py: two new §1 rules ("animation controls present", "step generator defined") with LEGACY_GOLDENS allowlist for warn-only treatment |
| Canonical patterns include JS skeletons | ✅ Met | sec1_insight.md has "Animation step-generator templates" section with shared control wiring + 4 per-archetype step-shape skeletons |
| batch-lesson skill updated | ✅ Met | step 6 includes §1 animation requirement + §7 multi-example requirement |
| 4 goldens warn (not fail) on animation rule | ✅ Met | audit shows 4 WARN; lessons pass with `[legacy golden — backfill in future plan]` prefix on the warning message |
| maximum-subarray passes lint as proof-of-concept | ✅ Met | 19 pass / 0 warn / 0 fail. §1 line count 167. Animation controls present. siGenSteps walks 9 steps on the canonical example |

## 3. Changes made

### 3.1 Static assets

- [`static/lesson.js`](../../../static/lesson.js) — three setInterval values bumped: `bfTogglePlay` 300→700, `cvTogglePlay` 900→1100, `drTogglePlay` 1100→1400. No other changes.

### 3.2 Design files

- [`lessons/design/sec1_insight.md`](../../../lessons/design/sec1_insight.md) — three new sections added:
  - "§1 animation conventions (PLAN-017)" — required markup, required JS, step-count target, speed rationale
  - "Acceptance criteria addendum (animation, PLAN-017)" — hard-check rules for lint + legacy-golden carve-out note
  - "Animation step-generator templates (PLAN-017)" — shared control wiring (copy-verbatim) + 4 per-archetype step-shape skeletons (two_pointer, sliding_window, prefix_scan, divide_conquer) + reuse-with-cv note
- [`lessons/design/sec7_dry_run.md`](../../../lessons/design/sec7_dry_run.md) — opening "Purpose" block added, distinguishing §7 (multi-example, 3+ inputs, no code panel) from §6 (single example tied to code). Default speed updated to 1400 ms.

### 3.3 Lint

- [`scripts/lint_lesson.py`](../../../scripts/lint_lesson.py) — added `LEGACY_GOLDENS` set at module level. Extended `lint_section1()` to accept `slug` parameter. Two new checks: "§1:animation controls present" (requires ≥ 3 of siPrev/siNext/siTogglePlay/siReset referenced from §1 markup) and "§1:step generator defined" (requires `function siGenSteps` somewhere in the lesson). Both rules severity = "warn" when slug ∈ LEGACY_GOLDENS, else "fail".

### 3.4 Skill

- [`.claude/commands/batch-lesson.md`](../../../.claude/commands/batch-lesson.md) — step 6 expanded with §1 animation requirement (canonical pattern + JS template references, function naming, speed) and §7 multi-example requirement. Self-review checklist (step 6b) updated to verify animation wiring.

### 3.5 Lesson

- [`lessons/maximum-subarray/lesson.html`](../../../lessons/maximum-subarray/lesson.html) — §1 fully revised as animated walkthrough. New markup: nums strip (current cell + run window highlighted), calculation panel (cur(i-1), nums[i], extend, restart, chosen cur, decision badge), cur/best display with ★ on new peak, caption that updates per step, control row. New script block: `siGenSteps` walks 9 steps over the canonical `[-2,1,-3,4,-1,2,1,-5,4]` example; `siRender` updates DOM; standard control wiring at 1200 ms auto-play.

### 3.6 Plan artifacts

- [`AGENT_MD/plan/plans/PLAN-017_animation_conventions.md`](../plans/PLAN-017_animation_conventions.md) — Draft → In-Progress → Completed (this report).

## 4. Testing & validation

### 4.1 Lint regression

```
--- goldens (exit 0, warn-only on animation rules) ---
3sum                          → exit 0  (14 pass, 5 warn, 0 fail)
permutation-in-string         → exit 0  (14 pass, 5 warn, 0 fail)
trapping-rain-water           → exit 0  (14 pass, 5 warn, 0 fail)
median-of-two-sorted-arrays   → exit 0  (14 pass, 5 warn, 0 fail)

--- maximum-subarray (proof-of-concept, exit 0) ---
maximum-subarray              → exit 0  (19 pass, 0 warn, 0 fail)

--- previously-passing lessons that now fail on animation rule ---
two-sum                       → exit 1  (animation controls missing)
valid-palindrome              → exit 1  (animation controls missing)
repeated-substring-pattern    → exit 1  (animation controls missing)
```

This is expected — the bar moved. Those three lessons need backfill in the resumed PLAN-015.

### 4.2 Manual verification

maximum-subarray §1 was visually inspected via the lesson HTML structure. The 9 steps walk the algorithm:

| step | i | action | cur | best | new peak? |
|---|---|---|---|---|---|
| 1 | 0 | init | -2 | -2 | ★ |
| 2 | 1 | restart | 1 | 1 | ★ |
| 3 | 2 | extend | -2 | 1 | — |
| 4 | 3 | restart | 4 | 4 | ★ |
| 5 | 4 | extend | 3 | 4 | — |
| 6 | 5 | extend | 5 | 5 | ★ |
| 7 | 6 | extend | 6 | 6 | ★ |
| 8 | 7 | extend | 1 | 6 | — |
| 9 | 8 | extend | 5 | 6 | — |

Reader can step through with prev/next, auto-play at 1200 ms, or reset to start over. Run window in the nums strip expands and snaps back on restart, making "extend or restart" visually obvious.

## 5. Known issues & follow-ups

### 5.1 PLAN-015 scope expands again

The pre-PLAN-017 audit baseline named 12 failing lessons. Post-PLAN-017 there are **14 failing lessons** — three previously-passing ones (`two-sum`, `valid-palindrome`, `repeated-substring-pattern`) dropped to FAIL because they lack animation. PLAN-015 scope needs updating:

| Lesson | Why it now fails | Effort |
|---|---|---|
| two-sum | no animation in §1 | ~45 min — chain-box present; just add animation wiring |
| valid-palindrome | no animation in §1 | ~45 min — chain-box present; just add animation wiring + deepen content per original PLAN-015 §2 |
| repeated-substring-pattern | no animation in §1 | ~45 min — chain-box present; just add animation wiring |

These three are quick wins (the structural work is done — just animation needed). Add to PLAN-015 phase 4 or as a separate priority-zero block.

### 5.2 Legacy goldens carry warnings

The 4 named goldens warn on:
- `plan.md` schema (predates PLAN-011)
- `§1:animation controls present` (predates PLAN-017)
- `§1:step generator defined` (predates PLAN-017)

A future plan should backfill these. Doing so is straightforward but multiplies the canonical-pattern work: each golden needs its §1 visual reworked as an animation, plus its plan.md migrated to PLAN-011 schema.

### 5.3 §7 multi-example requirement not yet lint-enforced

PLAN-017 documented the §7 ≥ 3 example button requirement in `sec7_dry_run.md` but did not extend lint to check it. Add as a §7 check in a future plan (when §7 quality becomes a concern). For now, the convention is documented and batch-lesson references it.

### 5.4 Speed tuning deferred to browser test

User chose to ship the 700/1100/1400/1200 ms defaults and tune from browser feedback. After they test the new speeds, adjust the four constants in `static/lesson.js` (and the `1200` literal in any lesson's `siTogglePlay`).

### 5.5 §1 step count 9 (vs convention 4–8)

maximum-subarray's animation has 9 steps (one per array index) — exceeds the documented 4–8 convention by one. Decision was made during user gating to walk every index for thoroughness. If subsequent §1 animations average longer than 8 steps, revisit the convention.

## 6. Metrics

### 6.1 Lint coverage shift

| State | Pre-PLAN-017 | Post-PLAN-017 | Delta |
|---|---|---|---|
| PASS | 3 | 1 | -2 (two-sum, valid-palindrome) … repeated-substring-pattern also dropped |
| WARN | 4 | 4 | unchanged (4 goldens — now with more warnings each) |
| FAIL | 12 | 14 | +2 (3 dropped from pass, 1 promoted from fail = maximum-subarray) |

The drop-to-fail of previously-passing lessons is expected and intentional — PLAN-017 raised the bar.

### 6.2 §1 size (maximum-subarray)

| | Before PLAN-015 | After PLAN-015 first pass (visual-led static) | After PLAN-017 (animated) |
|---|---|---|---|
| Lines | 25 | 76 | 167 |
| Visual lines before kernel | 15 | 66 | 47 |
| Kernel chars | 458 | 346 | 343 |
| Chain-box | no | no | no |
| Animation | no | no | yes (9 steps) |

The line count tripled from the original drift; the visual is now actually animated rather than static-rich.

## 7. Lessons learned

- **Raising lint thresholds reveals more drift than expected.** Pre-PLAN-017, three lessons were passing. Post-PLAN-017, only one. The bar moved and most lessons fell below — even ones that were perfectly fine under the prior bar. This is the right behavior for the gate (we now demand animation), but it means PLAN-015 scope grows whenever PLAN-017-style convention changes ship. Future convention changes should plan for the wave of newly-failing lessons.
- **Allowlisting works for legacy carve-outs.** The 4 named goldens are now slugs-allowlisted to warn-only on animation rules. This avoids forcing immediate backfill while still surfacing the work for future planning. Lesson: when conventions change retroactively, use slug allowlists for the lessons you don't want to break right now.
- **JS skeletons in design files cut authoring cost.** Adding the per-archetype `siGenSteps` templates to sec1_insight.md means future lessons don't need to invent the step-object shape from scratch. The first lesson (maximum-subarray) took ~90 min including design iteration; subsequent lessons should land in 45–60 min for §1 alone.
- **One file's edit triggers a cascade.** A single change to `static/lesson.js` (3 setInterval values) affects every lesson's autoplay speed. A change to `sec1_insight.md` affects every future §1. Centralized convention files have leverage — useful here, dangerous if changed carelessly. Worth documenting the leverage in the design files themselves so future editors know.
- **The user's "visuals/animations for intuition" reminder caught a real anti-pattern.** Even though my PLAN-015 first attempt passed lint, it was static — satisfying the letter but not the spirit. Lint rules can codify what we measure; they can't codify intent. The cycle of {build → user reviews → adjust convention → re-lint} is the corrective mechanism. Worth keeping the pattern: pause for review after the first lesson of a batch, not after the whole batch.
