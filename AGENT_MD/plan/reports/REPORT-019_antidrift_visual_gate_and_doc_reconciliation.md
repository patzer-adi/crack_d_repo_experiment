# REPORT-019: Anti-Drift — Visual-Correctness Gate, Corpus Re-Verification, and Doc Reconciliation

**Plan:** PLAN-019
**Completed:** 2026-06-03
**Author:** AI agent (Claude)

---

## 1. Summary

PLAN-019 closed the gates' blind spot for the project's actual goal — graphical
intuition — and reconciled the planning docs that had drifted from reality. The
durable machinery landed in full: a static §6 code-line check in the linter, a
headless **render gate** (`render_check.mjs`) that loads each lesson in Chromium
and asserts no JS error / every code-viz step lights a line / no overflow, an
independent `verify.py` cross-check wired into the correctness gate, a rewired
`audit_lessons.py` that is now a baseline-aware full-corpus regression gate, and
a `doctor.py` for lifecycle/reconciliation invariants. Running the new sweep
revealed substantial **pre-existing** corpus drift the §1-only audit had hidden:
15 lessons fail the full lint (§2/§6/§7 chassis) and 8 have real runtime/visual
bugs that passed both old gates. Per the agreed scope, those are recorded in
`scripts/audit_baseline.json` and deferred to a follow-up remediation batch; the
audit hard-fails any *new* regression. All doc-drift items were fixed and
`doctor.py` exits 0.

## 2. Goals vs. actuals

| Goal (from plan) | Outcome | Evidence |
|---|---|---|
| G1 — phantom-line lint check | ✅ Met | `lint_lesson.py` `§6:code-line refs resolve`; synthetic seed test catches `line:5 ∉ CV_LINES`; all 28 lessons pass it |
| G2 — corpus full-lint + gate regression sweep | ✅ Met | `audit_lessons.py` runs full lint (incl. §animation) + render, baseline-aware; exits 0 on current corpus; `classify()` unit-tested |
| G3 — headless render smoke test | ✅ Met | `render_check.mjs` (CDP, no npm); caught 8 real bugs; asserts overflow/console/active-line; 20 lessons pass clean |
| G4 — mechanical independence (`verify.py`) | ⚠️ Partial | Mechanism in `verify_animation.mjs` proven (pass / absent / wrong-→-exit-1); exemplars for rotting-oranges + pacific-atlantic; **26-lesson backfill tracked** (doctor info line) |
| G5 — lifecycle doctor | ✅ Met | `doctor.py` exits 0; checks bijection, phantom refs, lesson reconciliation, latest-plan, baseline sanity |
| G6 — doc reconciliation | ✅ Met | phantom PLAN-019 retired; duplicate REPORT-016 resolved; README/CLAUDE/spec/current_state/RETROFIT fixed; `doctor.py` green |
| G7 — fix `maximum-product-subarray` §6 | ✅ Met (reframed) | Its phantom-line report was a **false alarm** from a naive diagnostic scan; the robust check confirms refs [2..15] ⊆ CV_LINES [1..16], both gates green. `render_check` found a *separate* init-cascade runtime bug, now baselined for the batch |

## 3. Changes made

### 3.1 Gates & tooling
- `scripts/lint_lesson.py` — added JS-aware helpers (`js_strip`, `js_inline_scripts`, `js_extract_function`, `js_extract_array`) and the `§6:code-line refs resolve` check (cvGenSteps `line:` targets ⊆ `CV_LINES`).
- `scripts/render_check.mjs` — **new.** Headless Chromium via the DevTools Protocol over Node's built-in `WebSocket` (no npm). Drives cv/dr/si/bf; asserts no JS error, every §6 step lights an active code line, no horizontal page overflow. Strict (exit 1 on any failure); degrades to skip if no browser.
- `scripts/verify_animation.mjs` — added `runIndependence()`: runs `lessons/<slug>/verify.py` (if present) over the EX inputs and cross-checks its output against the declared answers; fails the gate on disagreement; absence is informational.
- `scripts/audit_lessons.py` — rewritten: full lint (all sections) + `render_check.mjs`, baseline-aware via `scripts/audit_baseline.json`; regression-gate exit semantics (`classify()`).
- `scripts/doctor.py` — **new.** Lifecycle/reconciliation invariants (status-aware plan↔report bijection, phantom plan refs, lesson/status reconciliation, latest-plan freshness, baseline sanity) + verify.py backfill info.
- `scripts/audit_baseline.json` — **new.** 15 lint + 8 render known pre-existing failures, grandfathered.

### 3.2 Lessons
- `lessons/pacific-atlantic-water-flow/lesson.html` — §6 phantom-line fix (landed during diagnosis 2026-06-02): `CV_LINES` now includes the `flood()` body; `cvGenSteps` walks real lines in code order.
- `lessons/rotting-oranges/verify.py`, `lessons/pacific-atlantic-water-flow/verify.py` — **new** independent brute-force references (timestamped BFS; forward downhill flood).
- `static/lesson.css` — `.cv-code-panel` overflow fix (landed during diagnosis 2026-06-02): `min-width:0` + `overflow-x:auto`; `.cv-line { min-width:max-content }`.

### 3.3 Docs
- Retired phantom "(PLAN-019)" by authoring this plan/report; `AGENT_MD/plan/reports/REPORT-016_audit_baseline.md` → `baseline_audit_2026-05-19.md` (+ 3 reference fixups).
- `README.md`, `CLAUDE.md` — "latest plan" → PLAN-019; corrected "26 lessons", the "pauses for review" contradiction, and the PLAN-012 misreference; documented the new scripts and three-gate bar.
- `AGENT_MD/spec.md` — historical banner. `AGENT_MD/RETROFIT_STATUS_animation_gate.md` — step-c marked done. `current_state_report.md` — PLAN-019 update entry + stale-body note.

## 4. Testing & validation

- `lint_lesson.py maximum-product-subarray` → `39 pass, 0 fail`; `node verify_animation.mjs maximum-product-subarray` → `3 verified`. Synthetic seed: `line:5 ∉ {1,2}` → flagged; clean → not.
- `verify_animation.mjs` independence: rotting-oranges & pacific-atlantic cross-check ✓ (exit 0); `two-sum` (no verify.py) → "none", exit 0; injected wrong verify.py → ✗, exit 1.
- `render_check.mjs --all` → 20 ok / 8 failed (the baselined set), exit 1 (strict).
- `audit_lessons.py` → `lint 12 pass · 15 known-fail · 0 NEW · render 20 pass · 8 known-fail · 0 NEW` → **exit 0**. `classify()` unit test: all 5 cases pass.
- `doctor.py` → **0 violations, exit 0**.

## 5. Known issues & follow-ups

- **Corpus remediation batch (approved scope).** Fix the 15 lint + 8 render baselined lessons (overlapping) and remove them from `scripts/audit_baseline.json` as they go green. Root causes are catalogued in the baseline file; notable: the shared `si-calc.innerHTML`-overwrite bug across 3sum / count-permutations / majority-element(-ii); maximum-product-subarray's init cascade; valid-palindrome's null-element `drRender` + non-canonical §6.
- **G4 backfill.** Add `lessons/<slug>/verify.py` to the remaining 26 generated lessons (doctor reports the count). Consider making `/batch-lesson` require `verify.py` for new lessons.
- **Optional hardening.** Wire `render_check.mjs` + `doctor.py` into a pre-commit/CI hook so a shared-asset (`static/`) edit re-checks the corpus automatically.

## 6. Metrics

- Corpus: 28 generated lessons. Render: 20 clean / 8 known-bad. Full lint: 12 pass / 1 warn / 15 known-fail. Independent `verify.py`: 2/28.
- New gate coverage: layout overflow, runtime JS errors, and code-line resolution — three failure classes previously invisible to both gates.

## 7. Lessons learned

- **The proxy isn't the product.** The old gates verified shape + one scalar and never the rendered animation; ~29% of the corpus shipped visibly broken. A 100-line headless render check closed the gap that two mature gates could not.
- **Diagnostic scans need the same rigor as gates.** The "maximum-product-subarray is broken" claim came from a regex that truncated `CV_LINES` at a `];` inside a C++ string. The robust linter (strings stripped first) corrected it. Throwaway analysis should strip strings too.
- **Surveys must cover what they claim.** `audit_lessons.py` advertised a corpus sweep but checked only §1, hiding §2/§6/§7 drift for the whole project. A "survey" that silently narrows scope is worse than none.
- **Baselines beat all-or-nothing.** Grandfathering known pre-existing drift turned an unshippable "fix 23 lessons first" into a usable regression gate today, with a list that can only shrink.
