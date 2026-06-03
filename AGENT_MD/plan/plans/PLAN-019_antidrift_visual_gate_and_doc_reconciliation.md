# PLAN-019: Anti-Drift — Visual-Correctness Gate, Corpus Re-Verification, and Doc Reconciliation

**Created:** 2026-06-02
**Status:** Completed (2026-06-03 — see [REPORT-019](../reports/REPORT-019_antidrift_visual_gate_and_doc_reconciliation.md). G1–G3,G5–G7 met; G4 partial: mechanism + 2 exemplars landed, 26-lesson backfill and the 8/15 corpus remediation are tracked follow-ups.)
**Addresses:** The two quality gates verify a lesson's *shape* (`scripts/lint_lesson.py`) and one terminal *scalar* (`scripts/verify_animation.mjs`) but never the rendered animation, its intermediate steps, or its layout. Visually-broken lessons therefore pass both gates. Meanwhile the planning documents have drifted from reality — including a phantom forward-reference to this very plan.

---

## 1. Context & motivation

The project exists to produce **graphical intuition**. The gates defend the parts of a lesson that are *not* the point (section scaffolding + one final number) and never touch the part that is (the rendered, animated explanation). This plan closes that blind spot and reconciles the planning docs that are supposed to anchor the system.

### 1.1 The drift, as measured

A study on 2026-06-02 (see §8) surfaced concrete, verified defects that **passed both gates**:

- **§6 "phantom code line" bug.** `cvGenSteps` narrates the algorithm while pointing the code-panel highlight at line numbers that do not exist in that lesson's `CV_LINES`. The active line then never resolves, so the code panel sits inert through the core of the animation. A one-line scan (every `*GenSteps` `line:` target ∈ `CV_LINES` `n` set) found it in two lessons:
  - `lessons/pacific-atlantic-water-flow/lesson.html` — refs `29`, `35` (fixed during diagnosis).
  - `lessons/maximum-product-subarray/lesson.html` — refs `3,4,5,6,7,8,9,10,11,12,13,15` (still broken).
- **CSS layout overflow.** `.cv-code-panel` blew out of its grid track (grid-item `min-width:auto` + `white-space:pre`), hiding code in every lesson's §6. Fixed in `static/lesson.css` during diagnosis; nothing in either gate could detect it because the verifier runs in a DOM-less `node:vm` sandbox and the linter is text-only.
- **No corpus re-verification.** `scripts/audit_lessons.py` calls `lint_lesson(slug, sections=[1])` — the recommended "survey all lessons" tool only checks §1, and never re-runs the animation gate. A shared-asset change (the CSS fix above, or any `static/lesson.js` edit) can silently break all 28 lessons with nothing to catch it.
- **Tautology risk in the correctness gate.** The gate compares `drGenSteps` output to `answer:` values *in the same file*. Its validity rests entirely on those answers being hand-derived; an author who pastes generator output into `answer:` passes trivially. There is zero machine signal for this — the worst failure mode (`RETROFIT_STATUS_animation_gate.md`: "polished, uniform, WRONG").

### 1.2 Documentation drift

- `AGENT_MD/spec.md` — "Last Updated: 2026-05-07", Status "In Planning", Current Focus still "PLAN-003"; it predates 18 plans, 28 lessons, and the entire two-gate system. Its header forbids manual edits and promises end-of-session updates that stopped at PLAN-003.
- `AGENT_MD/plan/current_state_report.md` — update log stops at PLAN-013; its body §1 still reads "no working code, no lessons, no skill files yet," contradicting its own header.
- `CLAUDE.md` and `README.md` — both name PLAN-016 as "the latest plan" though PLAN-017 and PLAN-018 (and now this) exist.
- **Phantom PLAN-019.** `lessons/design/sec2_brute_force.md`, `sec6_code_viz.md`, and `sec7_dry_run.md` (dated 2026-05-21) attribute the §2/§6/§7 canonical-scaffold lint rules to "(PLAN-019)" — a plan that was never written. Those rules in fact shipped under the PLAN-018 lint-tightening effort. **Writing this document retires the phantom:** the reference now resolves to a real file, and PLAN-019 becomes the document of record for those scaffold rules (see §8.2) plus the new checks below.
- `README.md` further: states "All 26 lessons currently pass" (28 exist); describes a "Pauses for your review before writing HTML" step that `.claude/commands/batch-lesson.md` explicitly removed ("There is no manual approval checkpoint"); calls PLAN-012 "the durable fix … not yet planned" though PLAN-012 is a completed, unrelated plan.
- **Lifecycle gaps.** `REPORT-014` is missing (PLAN-014 has no report); two `REPORT-016` files exist (`_audit_baseline` + `_self_healing_pipeline`); `RETROFIT_STATUS_animation_gate.md` still lists step "c (not started)" though `batch-lesson.md` is already autonomous.

### 1.3 Why now

Two of the visual defects above already shipped to the corpus undetected. Each new lesson widens the exposure. The cheapest durable fix — a structural scan plus a render smoke test — is small and reusable, and it directly serves the project's only real goal.

---

## 2. Goals

Each goal is pass/fail verifiable.

- **G1 — Phantom-line lint.** `lint_lesson.py` gains a §6 check: every `cvGenSteps`/`drGenSteps`/`siGenSteps`/`bfGenSteps` `line:` target must exist in the lesson's `CV_LINES`. `python3 scripts/lint_lesson.py maximum-product-subarray` exits non-zero before G7's fix and `0` after; all other generated lessons still exit `0`.
- **G2 — Corpus re-verification.** `scripts/audit_lessons.py` runs the full linter (all sections) **and** `verify_animation.mjs` over every `lesson_status: generated` lesson, and exits non-zero if any lesson FAILs. Running it on the current corpus exits `0`.
- **G3 — Render smoke test.** A new `scripts/render_check.mjs <slug>` loads `lesson.html` in a headless browser, walks every cv and dr step, and asserts: (a) no uncaught console error, (b) the `cvL<line>` element for each step resolves, (c) no element's right edge exceeds its container (overflow). It fails on a lesson with the pre-fix CSS or a phantom line, and passes on the current corpus.
- **G4 — Mechanical independence.** Each generated lesson carries `lessons/<slug>/verify.py` (an independent brute-force reference); a gate step runs it and asserts its output equals the lesson's `EX[].answer`, decoupling the ground truth from `drGenSteps`.
- **G5 — Lifecycle doctor.** `scripts/doctor.py` asserts and reports: every `PLAN-NNN` has exactly one `REPORT-NNN` and vice-versa; every `PLAN-NNN` referenced in any tracked file has a matching plan file; `{slug : lesson.html on disk}` == `{slug : lesson_status=="generated"}`; the "latest plan" string in `README.md` and `CLAUDE.md` equals the highest plan serial. Exits non-zero while any invariant is violated.
- **G6 — Doc reconciliation.** The phantom PLAN-019 reference resolves (this file); `spec.md` and `current_state_report.md` are either refreshed or banner-marked "historical — see README + CLAUDE"; the README "26 lessons" / "pauses for review" / "PLAN-012 not yet planned" / "latest PLAN-016" errors are corrected; the missing `REPORT-014` and duplicate `REPORT-016` are resolved; `RETROFIT_STATUS` step-c marked done. `python3 scripts/doctor.py` (G5) exits `0`.
- **G7 — Fix `maximum-product-subarray` §6.** Its `cvGenSteps` walks only real `CV_LINES`, and the cv terminal `result` equals each `EX.answer`. Both gates green.

---

## 3. Non-goals

- **No teaching-content rewrites** beyond repairing the §6 code walks named in G7 (and the already-fixed pacific-atlantic). The insight prose, archetypes, and section order are out of scope.
- **No pixel-level visual regression** (screenshot diffing). G3 asserts *structural* visual facts (overflow, console errors, line resolution), not appearance.
- **No runtime dependency added to lessons.** Lessons stay self-contained, offline, stdlib/static-only. The render check (G3) may add a **dev-only** Node tool (e.g. Playwright) invoked by the gate, never imported by a lesson.
- **No changes to `data/problems.json` content** beyond what G5's disk/status reconciliation requires.
- **No retroactive rewrite of PLAN-018's history.** PLAN-019 adopts the scaffold-rule reference; it does not claim to have authored those rules first.

---

## 4. Approach

Four workstreams, ordered cheapest-and-highest-leverage first.

### 4.1 Workstream A — close the visual blind spot

1. **Phantom-line lint (G1).** In `lint_lesson.py`, parse `CV_LINES` `n` values and every `line:` integer in the four `*GenSteps`; report any target not in the set. This is a pure-text check (no Node), so it costs nothing and runs inside the existing lint.
2. **Render smoke test (G3).** Add `scripts/render_check.mjs`. It is the only mechanism that can see layout and runtime behaviour. Keep its asserts structural and deterministic so it can gate, not just inform.

### 4.2 Workstream B — corpus re-verification (G2)

Change `audit_lessons.py` to call `lint_lesson(slug)` with no `sections=[1]` restriction and to shell out to `verify_animation.mjs` per slug, aggregating a pass/fail table and a non-zero exit on any FAIL. Wire `render_check.mjs` (A2) in as a third column. This turns the "survey" tool into a real regression sweep — the thing that re-checks the corpus after any shared-asset edit.

### 4.3 Workstream C — mechanical independence (G4)

Standardise `lessons/<slug>/verify.py` as the committed, independent reference (the role `/tmp/rot.py` and `/tmp/paw.py` played ad hoc). Extend the gate to run it and cross-check against `EX[].answer`. This removes the honor-system tautology from the correctness gate.

### 4.4 Workstream D — doc reconciliation + doctor (G5, G6)

1. Write `scripts/doctor.py` for the lifecycle/reconciliation invariants (G5). Build it first so the doc fixes can be verified by it.
2. Apply the doc fixes (G6): retire the phantom (this file), correct the README/CLAUDE claims, banner or refresh `spec.md` and `current_state_report.md`, resolve the REPORT-014 / duplicate-REPORT-016 / RETROFIT-step-c gaps.

### 4.5 Sequencing

A1 → G7 (A1 gives the failing test that G7 must turn green) → A2 → B → C → D. A1 + G7 are a self-contained first slice that immediately removes a live defect.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Add phantom-line `line: ∈ CV_LINES` check to `scripts/lint_lesson.py` §6 (G1) | 1 hr | — |
| 2 | Fix `lessons/maximum-product-subarray/lesson.html` §6 walk so it passes task 1 + the gate (G7) | 1.5 hr | 1 |
| 3 | Write `scripts/render_check.mjs` headless loader + overflow / console / line-resolution asserts (G3) | 4 hr | — |
| 4 | Re-point `scripts/audit_lessons.py` to full lint + `verify_animation.mjs` + `render_check.mjs`, non-zero on FAIL (G2) | 2 hr | 1, 3 |
| 5 | Define `lessons/<slug>/verify.py` convention; add gate step cross-checking it against `EX[].answer` (G4) | 3 hr | — |
| 6 | Write `scripts/doctor.py` lifecycle/reconciliation invariants (G5) | 3 hr | — |
| 7 | Retire phantom PLAN-019 ref; correct README + CLAUDE "latest plan"/counts/review-step/PLAN-012; banner `spec.md` + `current_state_report.md` (G6) | 2 hr | 6 |
| 8 | Resolve missing `REPORT-014`, duplicate `REPORT-016`, `RETROFIT_STATUS` step-c (G6) | 1 hr | 6 |
| 9 | Write `REPORT-019`; update `current_state_report.md`; set this plan `Completed` | 1 hr | 1–8 |

> **Already landed during 2026-06-02 diagnosis (not re-counted above):** the `.cv-code-panel` overflow fix in `static/lesson.css`, and the `lessons/pacific-atlantic-water-flow/lesson.html` §6 phantom-line fix. Both are uncommitted pending review.

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Headless-browser dep (Playwright) adds setup friction to a stdlib-only project | Med | Med | Make `render_check.mjs` dev-only and optional in the gate; if the browser is absent, skip with a loud warning rather than blocking. Document install in `README.md`. |
| The overflow assert (G3) yields false positives on intentionally wide elements | Med | Low | Assert only on the §6 code panel and grid containers initially; allowlist by container id; tune thresholds against the known-good corpus. |
| `line: ∈ CV_LINES` check (G1) over-matches integers in narration strings | Low | Med | Parse only the `line:` field token, after stripping strings/comments (reuse the verifier's `stripStringsAndComments` approach). |
| Doc refresh re-introduces new hardcoded counts that drift again (G6) | Med | Low | Have `doctor.py` emit the live counts; reference the command in the docs instead of pasting numbers. |
| `verify.py` references (G4) themselves become stale or wrong | Low | Med | They must be independent brute force, not the optimal algorithm; reviewer checks they disagree in approach, and the gate fails loudly on mismatch. |
| Scope creep into rewriting lesson content | Med | Med | §3 fixes the §6 walks only; any insight/archetype change is a separate plan. |

---

## 7. Success criteria

PLAN-019 is complete when:

- G1 — `lint_lesson.py` rejects phantom `line:` targets; verified by `maximum-product-subarray` flipping fail→pass across task 2.
- G2 — `python3 scripts/audit_lessons.py` runs full lint + animation gate over all generated lessons and exits `0`.
- G3 — `node scripts/render_check.mjs <slug>` passes for every generated lesson and fails on a seeded overflow/phantom-line regression.
- G4 — every generated lesson has a `verify.py` whose output the gate confirms equals `EX[].answer`.
- G5 — `python3 scripts/doctor.py` exits `0` with all invariants green.
- G6 — no document references a non-existent PLAN/REPORT; `spec.md` and `current_state_report.md` are current or banner-marked; README/CLAUDE claims match reality (re-checked by G5).
- G7 — `maximum-product-subarray` passes both gates with a correct §6 walk.
- `REPORT-019` written; `current_state_report.md` updated; this plan marked `Completed`.

---

## 8. References

### 8.1 Code & docs touched or cited

- Gates: `scripts/lint_lesson.py`, `scripts/verify_animation.mjs`, `scripts/audit_lessons.py`
- New scripts: `scripts/render_check.mjs`, `scripts/doctor.py`, `lessons/<slug>/verify.py`
- Shared assets: `static/lesson.css`, `static/lesson.js`
- Lessons: `lessons/pacific-atlantic-water-flow/lesson.html` (fixed), `lessons/maximum-product-subarray/lesson.html` (task 2)
- Docs to reconcile: `AGENT_MD/spec.md`, `AGENT_MD/plan/current_state_report.md`, `README.md`, `CLAUDE.md`, `AGENT_MD/RETROFIT_STATUS_animation_gate.md`
- Authoring conventions: `AGENT_MD/plan/rules.md`

### 8.2 Phantom reference retired by this plan

These design docs forward-referenced "(PLAN-019)" for the §2/§6/§7 canonical-scaffold lint rules; this plan is now their document of record (the rules themselves shipped under the PLAN-018 lint-tightening effort):

- `lessons/design/sec2_brute_force.md` (`schema:§2 canonical *`)
- `lessons/design/sec6_code_viz.md` (`schema:cv canonical scaffold`)
- `lessons/design/sec7_dry_run.md` (`schema:§7 canonical *`)

### 8.3 Prior plans in this lineage

- PLAN-015 — lesson drift remediation (§1 content depth)
- PLAN-016 — self-healing pipeline (the animation-correctness gate)
- PLAN-017 — §1 animation, §7 multi-example, pacing
- PLAN-018 — lesson uniformity contract + lint tightening (shipped the scaffold rules §8.2 refers to)
